# SerSan Outbound Platform — Architettura Funzionale

## 1. OVERVIEW SISTEMA

```
                        LEAD SOURCES (Esterno)
    +-----------+----------+-----------+----------+------------+
    | Apollo.io | Apify    | CSV       | Hunter   | LinkedIn   |
    | (DB B2B)  | (Scrape) | (Manual)  | (Email)  | Pipeline   |
    +-----------+----------+-----------+----------+------------+
                           |
                  POST /api/leads/bulk-import
                           |
                           v
    +--------------------------------------------------------------+
    |                    PostgreSQL 15                               |
    | leads | campaigns | deals | outreach_messages | mailboxes     |
    +--------------------------------------------------------------+
       ^         ^         ^         ^         ^         ^
    +------+--------+----------+-----------+---------+---------+
    |FastAPI|Django  |Worker    |Worker     |Celery   |         |
    |:8000  |:8001   |Email x2  |LinkedIn x1|Beat     |         |
    |REST   |UI+HITL |Perplexity|Playwright |beat     |         |
    |API (*)|Unibox  |Claude    |Voyager    |sched.(*)|         |
    +-------+--------+----------+-----------+---------+---------+
```

(*) Quanti endpoint e quanti task di beat: `docs/CODE_INVENTORY.md`, che è
rigenerato e verificato in CI. Questo diagramma ne riportava di fissi (84 e 28)
e li ha visti invecchiare.

## 2. EMAIL PIPELINE (flusso dettagliato)

```
CSV / Apollo / Apify / Hunter
          |
          v
+---------------------------------------------------+
| STEP 1: INGEST (ogni 30 min)                      |
| channel='email', status='raw', email NOT NULL      |
| Action: status -> 'discovered'                     |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| STEP 2: EMAIL VALIDATION (ogni 2 min)             |
| Tool: email-validator (RFC 5321 + MX DNS)         |
| Valid -> email_validated=true                      |
| Invalid -> status='blocked'                        |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| STEP 3: ENRICHMENT (ogni 10 min)                  |
|                                                   |
| 3A: VOYAGER (coda linkedin, ha il browser)        |
|   Per lead con linkedin_url personale (/in/...)   |
|   -> get_profile() via Playwright                 |
|   -> Salva: headline, positions, education        |
|   -> lead.profile_data = {JSON strutturato}       |
|   Rate: ~80 profili/giorno per account            |
|                                                   |
| 3B: APIFY (coda email, REST API)                  |
|   Per lead con company nota                       |
|   -> Indeed Scraper (solo annunci dell'azienda)   |
|   -> Salva: offerte lavoro (hiring signals)       |
|   -> lead.intent_signals += hiring data           |
|                                                   |
| 3C: PERPLEXITY (coda email, REST API)             |
|   Per tutti i lead validated                      |
|   -> Ricerca: funding, news, product launches     |
|   -> Salva: intent_summary, angle, confidence     |
|   -> status -> 'enriched'                          |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| STEP 4: COPY GENERATION (ogni 3 min, Tier-1)      |
| LLM: Claude (Anthropic API)                       |
|                                                   |
| Input: profile_data + hiring + intent + angle     |
|                                                   |
| Genera SOLO icebreaker (max 2 righe):             |
|   "Ho visto che state cercando 3 figure sales     |
|    - quando un team commerciale raddoppia,        |
|    spesso il collo di bottiglia si sposta         |
|    sulla generazione pipeline..."                 |
|                                                   |
| Body = campaign.email_body_template (fisso)       |
| Subject = EmailSequenceStep.subject_template      |
|                                                   |
| Output: OutreachMessage (pending_review)          |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| STEP 5: HITL REVIEW (operatore umano)             |
|                                                   |
|  /review/                                         |
|  +--------+ +--------+ +--------+ +--------+     |
|  | Sara B.| | Marco R| | Luca P.| | Anna V.|     |
|  | OXIGEN.| | Acme   | | TechCo | | StartX |     |
|  |        | |        | |        | |        |     |
|  | "Ho vi-| | "Congr-| | "Il vo-| | "Ho no-|     |
|  |  sto..." |  atul..." |  stro.." |  tato.." |     |
|  |[ok][no]| |[ok][no]| |[ok][no]| |[ok][no]|     |
|  +--------+ +--------+ +--------+ +--------+     |
|                                                   |
| Approva / Rifiuta / Edita icebreaker              |
| Output: status -> 'approved'                       |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| STEP 6: PUSH TO INSTANTLY (ogni 5 min)            |
| approved → sent_to_instantly                       |
|                                                   |
| InstantlyClient.add_leads_to_campaign()           |
| Custom variables: {{icebreaker}}, {{custom_subject}}|
| Instantly gestisce: warmup, domain rotation,      |
| tracking, compliance                               |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| WEBHOOKS da Instantly → SerSan                    |
| POST /api/webhooks (X-Webhook-Secret header)      |
|                                                   |
| email_sent      → status = sent                   |
| email_opened    → opened_at                       |
| email_replied   → InboundEmail + stop sequence    |
| email_bounced   → status = failed                 |
| lead_unsubscribed → status = blocked              |
+---------------------------------------------------+
          |
          v
+---------------------------------------------------+
| UNIBOX — reply via Instantly API                  |
| Operatore risponde → Instantly invia nel thread   |
+---------------------------------------------------+
```

## 3. SEQUENCE ADVANCEMENT

Gli step 2..N li manda Instantly, non SerSan. L'approvazione dello step 1 li
autorizza (ADR-033).

```
STEP 1 approvato in HITL (icebreaker AI basato su segnale)
    |
    | send.py: push del lead nella campagna Instantly, una volta sola,
    | con le variabili dello step 1 (greeting, icebreaker,
    | custom_subject, opt_out_footer)
    v
INSTANTLY manda lo step 1, poi gli step 2..N da solo
    ai delay_days di ogni step, dai template sincronizzati da SerSan
    (`instantly_sync.build_sequences_payload`):
    {{greeting}} + {{icebreaker}} + body_template dello step
    + {{opt_out_footer}}, tutti con le variabili dello step 1.
    Oggetto: {{custom_subject}}, con "Re: " sugli step 2 e 3.
    -> nessuna review per messaggio: l'approvazione dello step 1
       copre la sequenza così come è sincronizzata in quel momento

In SerSan nessuna bozza per gli step 2..N (dal 2026-10-04):
    `sequence_advance.py` è stata rimossa, la send lane salta ogni
    riga email con sequence_step > 1 (resta approved, mai pushata) e
    la migration ea4669769f24 ha ritirato quelle ancora in
    pending_review (rejected, `step_sent_by_instantly`); la one-off
    e0284014bcae ha chiuso allo stesso modo quelle approved mai reclamate

EXIT: lead risponde (stop_on_reply) | risposta su LinkedIn (lead tolto
      dalle campagne Instantly) | unsubscribed | bounce
      | campagna in pausa su Instantly | max step
```

## 4. LINKEDIN PIPELINE

```
Search -> Enrich -> Qualify -> Visit -> Connect -> Check Pending
(LLM     (Voyager  (GP+LLM   (warm    (HITL     (backoff)
keywords) API)      BALD)     visit)   gate)
                                         |
                                         v
                               DM ------> Follow-up
                               (HITL      (HITL agent,
                                gate)      multi-turn)

Ogni SEND passa per HITL:
  pending_review -> [operatore approva] -> approved -> sent
```

## 5. UNSUBSCRIBE

```
Email con link -> Pagina del CLIENTE (hosted esternamente)
                       |
                       | POST /api/unsubscribe
                       | {"email": "...", "tenant_code": "camp-001", "token": "..."}
                       v
                  FastAPI SerSan
                  1. Verifica il token HMAC per (tenant_code, email) PRIMA di
                     qualunque query: assente o sbagliato -> 400, identico per
                     token, tenant e lead sconosciuti (ADR-030 §5)
                  2. Trova campaign per tenant_code, lead per email
                  3. Soppressione durevole a livello di identificatore
                     (backend/services/suppression.py) + lead 'unsubscribed'
                  4. Toglie il lead dalle campagne Instantly (best-effort)
                  5. Return 200 {"status": "ok"}
```

Il token si conia con `backend/services/unsubscribe_token.py::mint`; senza, la
pagina del cliente riceve sempre 400.

## 6. UNIBOX (Unified Inbox)

```
+------------------+ +--------------------------------------+
| Thread List      | | Conversation                         |
|                  | |                                      |
| * Sara Baroni    | | [Step 1 - sent]                      |
|   OXIGENIO       | | "Ho visto che state cercando..."     |
|   3 msg, 2h ago  | | [body template]                      |
|                  | |                                      |
| o Marco Rossi    | | [Reply from lead]                    |
|   Acme Corp      | | "Potrebbe essere interessante,       |
|   1 msg, 1d ago  | |  mi dica di piu."                    |
|                  | |                                      |
| o Luca Puddu     | | [Reply composer]                     |
|   M.Ela Int.     | | +----------------------------+ [>>]  |
|                  | | | Scrivi una risposta...     |       |
+------------------+ +----------------------------+--------+

Mailbox affinity: lead sempre dalla stessa casella
```

## 7. STACK TECNOLOGICO

| Layer | Tecnologia | Porta |
|---|---|---|
| Database | PostgreSQL 15, Alembic | :5432 |
| Backend API | FastAPI, SQLAlchemy 2.x async, Pydantic v2 | :8000 |
| Frontend UI | Django 5.2, Bootstrap 5, htmx | :8001 |
| Worker LinkedIn | Celery, Playwright stealth, Voyager API | (singleton) |
| Worker Email | Celery, Instantly API, LangChain + Claude | (x2) |
| Instantly.ai | Email delivery (warmup, rotation, tracking) | (external) |
| ML Pipeline | FastEmbed 384-dim, GP Classifier, BALD | (in LinkedIn worker) |
| Enrichment | Voyager + Apify + Perplexity | (cross-queue) |
| Infrastructure | Terraform (Azure + AWS), Docker Compose | |
| Encryption | Fernet AES-128 (SMTP pwd, LinkedIn pwd, cookies) | |

## 8. FRONTEND PAGES

| Pagina | URL | Funzionalita |
|---|---|---|
| Login | `/login/` | Username/password, redirect a dashboard |
| Dashboard | `/dashboard/` | KPI cards + Chart.js trend (sent/replied 30gg) |
| Unibox | `/unibox/` | Inbox unificata risposte, reply da stessa mailbox |
| Review Queue | `/review/` | Card HITL con lead brief + icebreaker, approve/reject |
| Campaigns | `/campaigns/` | Lista, crea, dettaglio + sequence step config |
| Leads | `/leads/` | Lista con filtri + CSV import + export CSV |
| Mailboxes | `/mailboxes/` | Registro dei sender: l'account Instantly di ogni indirizzo, warmup, attivo/disattivo (staff). Nessun invio SMTP parte da qui: la consegna è di Instantly |
| Domini | `/mailboxes/domains/` | Lista + crea dominio, stato SPF/DKIM/DMARC |
| LinkedIn | `/linkedin/` | Workspace: profili, feed HITL per-lead (queue connection / generate DM), signals, connect/settings + readiness panel, groups |
| Admin | `/admin/` | Django admin con Lead, Deal read-only |

## 9. API ENDPOINTS

| Prefix | Endpoints | Auth |
|---|---|---|
| `/api/review` | queue, stats, get, approve/reject | X-API-Key |
| `/api/campaigns` | CRUD + sequence steps | X-API-Key |
| `/api/leads` | CRUD + bulk-import + export/csv | X-API-Key |
| `/api/unibox` | threads, thread detail, reply | X-API-Key |
| `/api/mailboxes` | CRUD | X-API-Key |
| `/api/domains` | CRUD | X-API-Key |
| `/api/kpi` | daily, summary | X-API-Key |
| `/api/unsubscribe` | POST {email, tenant_code, token} | Nessuna API key: token HMAC per destinatario (400 senza) |
| `/api/webhooks` | Instantly events | `X-Webhook-Secret` |
| `/health` | GET status check | Public |

## 10. IMPLEMENTATION STATUS

| Componente | Stato |
|---|---|
| Email pipeline (ingest, validate, enrich_v2, copy, send, + monitor/warmup lanes — conteggi in `CODE_INVENTORY.md`; nota: `enrich_voyager` sta sulla coda linkedin) | COMPLETO |
| LinkedIn pipeline (search, enrich, qualify, visit, connect, dm, follow-up, ... — conteggi in `CODE_INVENTORY.md`) | COMPLETO |
| FastAPI (endpoint/router in `CODE_INVENTORY.md` + rate limiting) | COMPLETO |
| HITL Review UI (card layout) | COMPLETO |
| Unibox (unified inbox) | COMPLETO |
| CSV Import/Export | COMPLETO |
| Mailbox/Domain management (UI + API) | COMPLETO |
| Dashboard + Chart.js trend | COMPLETO |
| KPI aggregation task | COMPLETO |
| Django Admin (Lead, Deal read-only) | COMPLETO |
| Sequence step config UI | COMPLETO |
| Security (encryption, auth, non-root, rate limit) | COMPLETO |
| Docker dev + prod compose | COMPLETO |
| Terraform (Azure + AWS + networking + VNet) | COMPLETO |
| Voyager enrichment per email (linkedin queue) | COMPLETO |
| Apify hiring integration (email queue) | COMPLETO |
| Perplexity enrichment (with Voyager+Apify context) | COMPLETO |
| Test suite (email + API + LinkedIn/ML) | COMPLETO (27+ test files) |
| **Playbook: Blank connection request** | COMPLETO (LLM nota rimossa, always blank) |
| **Playbook: CRM tracking** (call_booked, good_conversations, job_change) | COMPLETO (8 campi Lead + 2 endpoint API + UI) |
| **Playbook: Sequenza 3 DM post-connessione** | COMPLETO (`sequence_advance_li.py`: step AI via Personalization v3, `linkedin/personalization/service.py::generate_personalized_dm`; altrimenti il template dello step scritto dall'operatore) |
| **Playbook: Boolean search su post** | COMPLETO (search_posts.py + SearchKeyword esteso) |
| **Playbook: Good Conversations + Job Change detection** | COMPLETO (check_job_changes.py + normalizzazione fuzzy) |
| **Playbook: LinkedIn Groups** | PARZIALE (modello + CRUD API + join_group worker + UI. group_dm skeleton) |
| **Playbook: Like + Comment pre-connessione** | STAGED (SO-185 — disabilitati per rischio ban) |
| LinkedIn Groups CRUD API | COMPLETO (backend/routers/linkedin_groups.py) |
| Celery task timeouts (10min hard, 9min soft) | COMPLETO |
| Worker Docker healthchecks (celery inspect ping) | COMPLETO |
| Backup strategy doc | COMPLETO (docs/backup_strategy.md) |
| Monitoring architecture doc | COMPLETO (docs/monitoring_setup.md) |
| Structured logging (structlog JSON) | COMPLETO |
| CI/CD (lint + test + build + Terraform deploy) | COMPLETO |
| Documentation (README, architecture, deployment, operator guide) | COMPLETO |

## 11. DOCUMENTATION

| Documento | Percorso | Contenuto |
|---|---|---|
| README | `README.md` | Overview, quick start, architecture, API, features |
| Architecture | `docs/architecture.md` | Questo file: diagrammi, stack, status |
| Deployment | `docs/DEPLOYMENT.md` | Step-by-step Azure deploy con Terraform |
| Operator Guide | `docs/OPERATOR_GUIDE.md` | Workflow quotidiano operatori |
| Compliance | `docs/compliance_decision_checklist.md`, `docs/adr/ADR-030-commercial-email-compliance-boundary.md` | Decisioni di compliance aperte e confine email commerciale |
| Project Rules | `CLAUDE.md` | Regole sviluppo, comandi, file chiave |
