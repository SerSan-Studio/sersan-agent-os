# 01 — SersanOutreach: stato, dipendenze, hosting, migrazione sul server fisico e punti di aggancio per gli agenti

**Data:** 2026-10-24 · **Repo studiato:** `C:/Users/alber/SerSanOutreach` (branch `main`, HEAD `cd185f09` del 2026-10-16, merge PR #776 «release/2026-10-15-auto-dm») [verificato: `git log -1`]
**Scopo:** materiale per il documento ai due CEO sul sistema multi-agente aziendale. Questo file descrive *cosa esiste davvero* nella piattaforma outbound interna, cosa serve per spostarla sul server fisico e dove un sistema di agenti può agganciarsi.

**Legenda.** Ogni fatto porta `[verificato: percorso o URL]` quando l'ho letto nel repo, `[non verificato]` quando è una deduzione mia, `non trovato` quando il dato non c'è nei file. Molti documenti del repo sono datati e si contraddicono (il repo stesso ne tiene un elenco di «superati»): dove conta, cito la misurazione più recente con la sua data.

---

## 0. In dieci righe

1. SersanOutreach è la piattaforma outbound **interna** di SerSan (LinkedIn + email), fork di OpenOutreach, tutta Python: FastAPI, Django, PostgreSQL, Celery, Playwright, Claude. Nessun invio parte senza un'approvazione umana (HITL) [verificato: `README.md`, `CLAUDE.md`].
2. È grande: 269 endpoint REST in 37 router, 70 modelli, 124 migrazioni Alembic, 45 task schedulati, 10.888 funzioni di test, 48 workflow GitHub [verificato: `docs/CODE_INVENTORY.md` snapshot `59caf685`; `ls .github/workflows`].
3. In produzione gira su **una VM Azure** (`vm-apps-01`) con Docker Compose, Traefik e WireGuard; il database è su **Supabase** (AWS eu-west-1). Il Terraform per Azure Container Apps nel repo **non è mai stato applicato** [verificato: `docs/DEPLOYMENT.md` banner, `docs/backup_strategy.md` §2, `CLAUDE.md`].
4. Volumi reali al 2026-10-05: **11 lead** nella finestra del funnel, 1 contattato, 1 risposta, 0 meeting, 0 won; 91 deal aperti **tutti senza valore** [verificato: `docs/growth_os_capability_map.md` intestazione].
5. Ultima prova live su LinkedIn: un invio **manuale** del 2026-09-25 con risposta registrata a mano; «Nothing automatic is proven live» (misura 2026-09-27) [verificato: `docs/linkedin_automatic_acceptance.md` tabella baseline].
6. L'email via Instantly è cablata e coperta da test, ma **nessuna mailbox né dominio è live** e la campagna di produzione è trattenuta dal 2026-09-09 per una deroga compliance non valida [verificato: `docs/growth_os_capability_map.md` riga 7, `docs/compliance_decision_checklist.md` §D0.1].
7. Il ledger di readiness dice **NOT READY** su tutti e quattro i verdetti (email, LinkedIn manuale, LinkedIn automatico, combinato) [verificato: `docs/PRODUCTION_READINESS.md` blocco generato].
8. Esistono già **due server MCP** nel repo: `mcp_server/` in sola lettura (19 tool) e `mcp_operator/` a scrittura controllata (14 operazioni), pensati per Claude Code / Claude Desktop [verificato: `mcp_server/README.md`, `mcp_operator/README.md`, conteggio in `mcp_server/tools.py` + `growth.py`, `mcp_operator/operations.py`].
9. Per spostarlo sul server fisico servono: gli 8 servizi del compose (7,4 GiB di tetti di memoria misurati), lo stack di monitoring separato, Traefik con Let's Encrypt, un ingresso HTTPS pubblico per i webhook Instantly e per l'estensione Chrome (che ha `outreach.sersan.io` cablato nel manifest), il runner GitHub self-hosted, il cron dei backup [verificato: `docker-compose.prod.yml`, `extension/manifest.json`, `scripts/ops/deploy_prod.sh`, `docs/INCIDENT_RUNBOOK.md`].
10. Rischi aperti principali: compliance email (deroga permanente ADR-004, decisioni D0 aperte), LinkedIn ToS (trasporto `extension_voyager` non idoneo, acceso sotto rischio accettato dall'owner), identità dei chiamanti in `observe`, MFA non attiva (7 staff, 0 iscritti), backup off-site assente, alert mai provati a raggiungere una persona [verificato: §6 sotto].

---

## 1. Cosa fa oggi e in che stato è

### 1.1 Cos'è

| | |
|---|---|
| Natura | Piattaforma outbound self-hosted LinkedIn + email con HITL prima di ogni invio; fork di OpenOutreach (GPLv3) [verificato: `README.md`] |
| Per chi | Strumento **interno** con cui SerSan fa il proprio outbound. Non è l'offerta: SerSan vende custom software, automazione e AI [verificato: `docs/sersan_company_profile.md` intestazione] |
| Stack | FastAPI + SQLAlchemy 2 async (:8000); Django 5.2 + Bootstrap/htmx/Alpine (:8001); PostgreSQL 15 con Alembic unico owner DDL; Celery con broker **PostgreSQL** (kombu sqla, niente Redis); Playwright stealth + Voyager API; Anthropic SDK; FastEmbed 384-dim + scikit-learn (GP regression + BALD) [verificato: `ARCHITECTURE.md`, `CLAUDE.md` §Architecture, `docs/architecture.md` §7] |
| Immagini | `python:3.12-slim` (backend, frontend, worker-email, beat); `mcr.microsoft.com/playwright/python:v1.50.0-noble` per worker-linkedin [verificato: `compose/*/Dockerfile`] |
| Modelli LLM | `claude-sonnet-4-6` per icebreaker v2, angle agent, judge offline e DM LinkedIn personalizzati; fallback opzionale OpenAI `gpt-4o` se Anthropic fallisce [verificato: `workers/email/copy_agent.py:926,1275`, `backend/clients/claude_angle_agent.py:31`, `backend/clients/icebreaker_judge.py:61`, `linkedin/personalization/service.py:438`] |

### 1.2 Le due pipeline

**Email** (consegna delegata a Instantly) [verificato: `docs/architecture.md` §2-3, `CLAUDE.md` §HITL invariant]:
`ingest (ogni 30 min) → validate RFC+MX (2 min) → enrich_v2 (Perplexity + Voyager + Apify in parallelo, poi Claude sceglie l'angle) → copy agent (solo icebreaker ≤ 2 righe, 10 validator hard-fail) → HITL review → push del lead nella campagna Instantly con custom variables → Instantly manda step 1..N → webhook (sent/opened/replied/bounced/unsubscribed) → Unibox`.
Dal 2026-10-04 (ADR-033, deciso da Alberto Tuveri con Alessandro Serratt) l'approvazione dello step 1 autorizza tutta la sequenza: SerSan non scrive bozze per gli step 2..N, li manda Instantly dai template sincronizzati [verificato: `docs/adr/ADR-033-step1-approval-authorizes-the-sequence.md` intestazione].

**LinkedIn** [verificato: `docs/architecture.md` §4, `docs/linkedin_inbrowser_send.md` §1]:
`search → enrich (Voyager) → qualify (GP+BALD, offline) → visit → connect (HITL) → check pending → DM (HITL) → follow-up step 2-3 (HITL)`.
In produzione il trasporto è **`extension_voyager`**: il server decide e prenota il messaggio approvato, l'**estensione Chrome** lo esegue nel browser del membro loggato (dispatch in due fasi con `/ext/dispatch-confirm` prima del click) e riporta una ricevuta; le lane Playwright server-side restano ferme. Dal 2026-10-14/15 esistono i modi di approvazione `auto_blank_invites` e `auto_linkedin`: un autopilot che, dentro l'envelope del pilot, redige e approva inviti senza nota e DM, entro i tetti giornalieri [verificato: `git log` commit del 2026-10-14 «feat(pilot): approval_mode auto_blank_invites» e 2026-10-15 «feat(pilot): approval_mode auto_linkedin»].

### 1.3 Dimensioni del codice [verificato: `docs/CODE_INVENTORY.md`, generato al commit `59caf685`]

| Artefatto | Conteggio |
|---|---:|
| File modello / classi SQLAlchemy | 50 / 70 |
| Router / endpoint REST | 39 file (37 con `APIRouter`) / **269** |
| Migrazioni Alembic (una sola head `5b1e9d0c7a42`) | 124 |
| File di test / funzioni di test | 1.244 / **10.888** |
| Task Celery-beat attivi | 45: coda `linkedin` 17, `default` 16, `email` 12 [verificato: conteggio su `workers/beat_schedule.py`, voci non commentate] |
| Task Celery definiti (email / linkedin / kpi) | 14 / 23 / 5 |
| Servizi compose (dev / prod) | 11 / 8 |
| ADR | 28 file in `docs/adr/` (ADR-001…ADR-033 con buchi) [verificato: `ls docs/adr`] |
| Workflow GitHub | 48, di cui 44 `prod_*` operativi sul runner self-hosted [verificato: `ls .github/workflows`] |

### 1.4 Stato live: volumi, cosa è provato e cosa no

**Volumi di produzione al 2026-10-05** [verificato: `docs/growth_os_capability_map.md`]: 11 lead nella finestra del funnel, 1 contattato, 1 risposta, 0 positive, 0 meeting, 0 won; 91 deal aperti, tutti senza valore. Import CSV usati; discovery Sales Navigator in `warn` (non ha mai portato un lead); inbound first-party mai esercitato in prod.

**Ledger di readiness** [verificato: `docs/PRODUCTION_READINESS.md`, blocco `READINESS:BEGIN..END`]: email pilot **NOT READY** (18 righe P0, 5 non PASS); LinkedIn pilot manuale **NOT READY** (16, 4); LinkedIn automatico **NOT READY** (17, 5); combinato **NOT READY** (21, 8). Attenzione: il blocco riporta «runtime evidence collected 2026-08-20» (commit `99a0de4c`): le evidenze runtime nel ledger sono di agosto anche se il file è stato rigenerato il 2026-10-16. Le misure più recenti sono nella capability map (2026-10-05) e nel record di accettazione LinkedIn (2026-09-27, aggiornato 2026-10-05).

Righe **FAIL** P0/P1/P2: email go-live gate live (nessuna mailbox attiva registrata, 1 campagna attiva senza id Instantly), recovery (cifrato + off-site + restore dal remoto), alert provati a raggiungere una persona, account LinkedIn che può agire (1/1 attivo fermo su `/checkpoint/`), backup cifrato at rest, auth hardening. Righe **UNKNOWN**: compliance email live, reply email e LinkedIn che provabilmente arrivano e fermano entrambi i canali, envelope LinkedIn non presidiato [verificato: stesso blocco].

**Capability → prova live** (estratto delle 25 righe) [verificato: `docs/growth_os_capability_map.md`]:

| Capability | Implementata | Provata live |
|---|---|---|
| Acquisizione prospect (CSV, inbound first-party, Sales Nav, vendor export) | sì | CSV sì; Sales Nav mai un lead; inbound mai esercitato |
| Enrichment (Perplexity/Anthropic/Apify) | sì | gira in prod; qualità mai benchmarkata |
| Generazione personalizzata email + LinkedIn | sì (+ corpus recorder, judge offline) | bozze esistono; corpus da prod mai registrato |
| HITL review con fingerprint del testo letto | sì (release #747) | **usata in prod** |
| LinkedIn multi-dipendente (estensione 1.6.x, team page) | sì | 1 profilo attivo; invio e reply **manuali** 2026-09-25; Michele non onboardato |
| Email via Instantly (mapping, push, DNS/warm-up, go-live gate) | sì | `email_dns`, `email_mailbox_state`, `email_compliance` **FAIL**; `email_provider_canary` mai raccolto |
| Unibox / ingest risposte | sì | `email_reply_ingestion`, `linkedin_reply_ingestion` mai raccolti |
| Meetings, deals, proposals, won/lost, revenue, reactivation, partner, blueprint | sì (entità, pagine, API) | 0 meeting, 0 won/lost, 0 partner deal, blueprint non usati |
| Action queue P0–P3 ed executive funnel | sì | renderizzano dati prod (letti via MCP il 2026-10-05) |
| MCP read (19 tool) + operator (14 op) | sì | read server eseguito contro prod il 2026-10-05 (tutti 200); quello **installato** non parte (config su worktree cancellato); operator non installato |

**LinkedIn misurato il 2026-09-27** [verificato: `docs/linkedin_automatic_acceptance.md`]: prod con `LINKEDIN_SEND_MODE=automation`, `LINKEDIN_TRANSPORT=extension_voyager`, `LINKEDIN_REQUIRE_PROXY=true`, `LINKEDIN_PROFILE_SELECTION_MODE=enforce`; 2 profili (uno sano e automatico, sender delle due campagne LinkedIn attive; uno `manual_only` **fermo su checkpoint**); 2 workspace con un membro ciascuno. Nota: il compose fissa `manual`/`disabled` come default, ma il `.env` della VM li sovrascrive [verificato: `docker-compose.prod.yml` header; stesso record]. Estensione 1.6.6 in prod al 2026-10-05, `1.6.8` nel manifest corrente [verificato: `extension/manifest.json`].

**Prestazioni** (bench 2026-10-10: 10.000 lead, 5 operatori + 5 reviewer, webhook, MCP, lane in background, 35 ms di latenza DB simulata): 2.073 richieste, **0 errori**, ogni effetto contato una volta; dashboard p95 6,7 s e readiness 6,4 s **sopra** i target 4-5 s; due P1 trovati e corretti (deal won *e* lost da due persone; KPI notturno che non finiva a 10k lead) [verificato: `docs/scale_test_2026-10.md` §3, §5.1].

---

## 2. Servizi esterni e API

| Servizio | A cosa serve | Variabili / requisiti | Costo o vincolo | Fonte |
|---|---|---|---|---|
| **Anthropic (Claude)** | icebreaker v2, angle agent, judge, DM LinkedIn | `ANTHROPIC_API_KEY`; modello `claude-sonnet-4-6` | key su **Tier 1** (30k token input/min): worker email a `BATCH_SIZE=4`, beat 180 s, concurrency 1 (~4 call/min, 5-10 min per 4 lead); Tier 2 ≈ 250 $ di deposito. Token per tentativo in `llm_generation_logs`, gauge `sersan_llm_tokens_today` e probe `run_llm_cost_probe`; **nessun listino prezzi in codice**, la conversione in denaro è lasciata a Grafana | [verificato: `CLAUDE.md` §Active Operational Workarounds; `workers/kpi/llm_cost.py`; `backend/metrics.py:177`] |
| **OpenAI** (opz.) | fallback del copy agent | `OPENAI_API_KEY`, modello `gpt-4o` | costo: non trovato | [verificato: `.env.example` 741-745, `copy_agent.py:926`] |
| **Perplexity** | enrichment (funding, news, lanci) via **Agent API** `https://api.perplexity.ai/v1/agent` con preset (`fast` di default) | `PERPLEXITY_API_KEY`, `PERPLEXITY_AGENT_PRESET` | costo: non trovato | [verificato: `workers/email/_enrich_client.py:17-19,215`, `README.md`] |
| **Apify** | hiring signals: actor `misceres/indeed-scraper` (annunci Indeed dell'azienda); seconda sorgente di segnali, opzionale | `APIFY_API_TOKEN` | costo: non trovato | [verificato: `workers/email/_apify_client.py:2-22`, `docs/DEPLOYMENT.md` §6] |
| **Instantly.ai** | consegna email: warmup, rotazione domini, invio sequenze, tracking, webhook, reply da Unibox | `INSTANTLY_API_KEY`, `INSTANTLY_API_BASE_URL`, `INSTANTLY_WEBHOOK_SECRET` (+ `_PREVIOUS`, `_KID`, `_ACTIVE_FROM`, `_PREVIOUS_EXPIRES_AT` per rotazione senza perdere eventi), `INSTANTLY_WORKSPACE_ID`; webhook pubblico `POST https://outreach.sersan.io/api/webhooks` con `X-Webhook-Secret` (token pre-condiviso: Instantly v2 non ha HMAC); 5 opzioni di campagna imposte da codice alla creazione (`stop_on_reply`, `open_tracking`, `match_lead_esp`, `disable_bounce_protect`, `insert_unsubscribe_header`); cap di volume **non** impostati di proposito | piano/costo: non trovato. Gate go-live: campagna linkata, ≥1 mailbox attiva registrata, SPF/DKIM/DMARC validi, ≥1 mailbox warmata, volume giornaliero in [1, 500] | [verificato: `.env.example` 759-795, `CLAUDE.md` §«Cosa SerSan impone a Instantly», `docs/email_go_live_gate.md`] |
| **Proxy residenziale** (IPRoyal) | egress per account LinkedIn **solo** se girano le lane Playwright server; gate `LINKEDIN_REQUIRE_PROXY=true` fail-closed | `PROXY_PROVISION_ENABLED`, `PROXY_GATEWAY_HOST=geo.iproyal.com`, `PROXY_GATEWAY_PORT=12321`, `PROXY_USERNAME_TEMPLATE`, `PROXY_PASSWORD_TEMPLATE`, `PROXY_DEFAULT_COUNTRY=it`; `proxy_url` cifrato per profilo | provider IPRoyal scelto; prodotto (Royal Residential a consumo o ISP statico «a IP/mese») e budget **non decisi**, nessuna cifra. Con il trasporto estensione «nessun proxy server è richiesto» | [verificato: `docs/HANDOFF_2026-07-22_proxy_prewarm.md` §2, `.env.example` 538-581 e 422-427] |
| **Telegram** | notifiche applicative in uscita (push KPI notturno, risposta non attribuibile) e receiver di Alertmanager | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (insieme); Alertmanager legge `bot_token_file` e un `chat_id` per receiver (oggi segnaposto `0`); token installato via `prod_alert_telegram.yml` | gratuito; **solo in uscita**: nessun comando in ingresso trovato | [verificato: `backend/services/operator_notify.py`, `infra/alertmanager/alertmanager.yml`, `.github/workflows/prod_alert_telegram.yml`] |
| **Slack** | storico: `SLACK_ALERT_WEBHOOK_URL` per push KPI e «alert destination» | non più presente in `.env.example`; Alertmanager è passato a Telegram | — | [verificato: grep `.env.example`; `docs/email_go_live_gate.md` lo cita ancora] |
| **Grafana / Prometheus / Loki / Alertmanager** | monitoring self-hosted sulla VM in compose **separato**; 4 dashboard versionate (`email_delivery`, `linkedin`, `linkedin_safety`, `prompt_quality`); 98 regole di alert | `GRAFANA_BASE_URL`, `GRAFANA_DASHBOARD_UID`, `GF_SECURITY_ADMIN_*`; Grafana su `/grafana` dietro Traefik forwardAuth (login staff Django) | nessun costo esterno. La stima «Azure Monitor ~40-60 $/mese» riguarda il disegno Container Apps mai attivato | [verificato: `infra/grafana/dashboards/`, `docs/monitoring_setup.md` §6, `docs/OPERATOR_GUIDE.md` §15] |
| **Supabase** | database di produzione: Postgres 17.6, session pooler, AWS eu-west-1, ~35 ms a round trip | `DATABASE_URL`, `DATABASE_URL_SYNC`, `DB_DSN`; pooler con **15 connessioni** totali misurate il 2026-09-28 | piano/costo: non trovato | [verificato: `docs/backup_strategy.md` §2, `.env.example` 45-64, `docs/perf_2026-10.md` §1] |
| **Azure** | VM `vm-apps-01` (RG `RG-SERSAN-MAIL`); Key Vault opzionale (`AZURE_KEY_VAULT_URL`); Blob GRS per backup off-site **non provisionato** | `AZURE_BACKUP_STORAGE_ACCOUNT`, `AZURE_BACKUP_CONTAINER` | costo VM: non trovato | [verificato: `docs/backup_offsite_azure.md:188-191`, `.env.example` 10-14, 630-639] |
| **GitHub** | repo privato `SerSan-AI-Studio/SerSanOutreach`, piano **Team** (nessun required reviewer sugli environment); CI su `ubuntu-latest`; deploy e 44 workflow `prod_*` su runner self-hosted `[self-hosted, prod-vm]` | `GOVERNANCE_READ_TOKEN` non impostato | blocco billing Actions avvenuto il 2026-09-26; token `gh` senza scope `workflow` (2026-08-31) | [verificato: `.github/workflows/prod_monitoring_stack.yml` commento, `deploy.yml`, `tests.yml`, `docs/linkedin_automatic_acceptance.md`, `docs/monitoring_setup.md`] |
| **Chrome Web Store** | pubblicazione dell'estensione (basta un listing unlisted) | — | **non pubblicata**: oggi install unpacked da sviluppatore, «the remaining blocker on self-serve onboarding» | [verificato: `extension/README.md` §Install] |
| AimFox | multi-account LinkedIn (99 $/mese/account, piano aprile) | — | **rimosso il 2026-10-10** | [verificato: `CLAUDE.md` §Playbook workers, `PROJECT_STATUS_REPORT.md:290`] |
| Apollo / Hunter | sorgenti lead nel diagramma | — | registro sorgenti: Apollo e inbound webhook «unavailable» | [verificato: `docs/architecture.md` §1, `docs/growth_os_capability_map.md` riga 1] |

---

## 3. Com'è ospitato oggi su Azure

### 3.1 Topologia reale (non quella del Terraform)

| Elemento | Stato | Fonte |
|---|---|---|
| **VM `vm-apps-01`** (Azure, RG `RG-SERSAN-MAIL`, IP WireGuard `10.40.20.4`) | host unico per prod, stage e monitoring; **15,6 GiB di RAM** condivisi; SKU, vCPU e disco: **non trovati** | [verificato: `docker-compose.prod.yml` commento INFRA-05, `docs/INCIDENT_RUNBOOK.md:18`, `docs/backup_offsite_azure.md:188`] |
| Deploy | `push su main → Tests (ubuntu-latest) → deploy.yml → runner self-hosted sulla VM → scripts/ops/deploy_prod.sh`: backup DB, tag `:previous`, checkout dello SHA passato in CI, build, preflight delle immagini, stop dei sender, migrate, start, health gate | [verificato: `scripts/ops/deploy_prod.sh` header, `docs/DEPLOYMENT.md` banner] |
| Layout su disco | `/opt/apps/sersan-outreach/prod/{compose.yml,.env,repo/}`, `/opt/apps/sersan-outreach/stage/`, `/opt/apps/sersan-outreach/grafana/compose.yml`, `/opt/apps/sersan-outreach/alertmanager/`, `/opt/apps/traefik/acme.json`, `/opt/backups/sersan/prod/`, `/var/lib/sersan/ops-evidence`, `/var/lib/node_exporter/textfile_collector` | [verificato: `docker-compose.prod.yml` header, `docs/INCIDENT_RUNBOOK.md`, `infra/monitoring/node-exporter.compose.yml`] |
| Ingresso | **Traefik** sulla VM (rete Docker esterna `edge`, container `compose-traefik-1`), certificati Let's Encrypt ACME (email `admin@sersan.io`, rinnovo 30 gg prima); `outreach.sersan.io` pubblico; `stage.`, `prometheus.`, `alertmanager.outreach.sersan.io` solo da WireGuard (allowlist `10.6.0.0/24` + `10.40.0.0/16`); DNS su Cloudflare | [verificato: `docs/INCIDENT_RUNBOOK.md` §5, `docs/OPERATOR_GUIDE.md` §15, `docker-compose.prod.yml` networks] |
| Accesso admin | WireGuard con split DNS (`DNS = 10.6.0.1`); il traffico passa da un «VPS WG» con IP pubblico distinto dalla VM; operazioni quotidiane senza SSH via `prod_ops.yml` | [verificato: `docs/OPERATOR_GUIDE.md` §15, `docs/INCIDENT_RUNBOOK.md`; provider del VPS: non trovato] |
| **Database** | **Supabase** (eu-west-1), Postgres 17.6, session pooler; il servizio `db` del compose (`postgres:15-alpine`, volume `sersan_pgdata_prod`) **esiste ancora ma è abbandonato**; RLS abilitata da `alembic/env.py` su ogni tabella nuova perché su Supabase `public` è anche superficie PostgREST | [verificato: `docs/backup_strategy.md` §2, `CLAUDE.md` §Supabase, `.env.example` 70-78] |
| Broker Celery | PostgreSQL via kombu sqla (`CELERY_BROKER_URL`); se su Supabase o sul container `db`: [non verificato] | [verificato: `CLAUDE.md`, `.env.example` 86-124] |
| Monitoring | Prometheus (scrape di backend prod/stage, worker 9100/9101/9102, beat 9099, Loki, Grafana, node_exporter, cAdvisor, pg_exporter prod/stage), Grafana, Loki + Promtail (label `logging: promtail` sui container), Alertmanager → Telegram; compose **separato e non versionato** nel repo; regole e scrape config sincronizzate solo via `workflow_dispatch` / script | [verificato: `infra/prometheus/prometheus.prod.yml`, `docker-compose.prod.yml` header, `docs/monitoring_setup.md`] |
| Infra Terraform «viva» | in un altro repo, `SerSan-AI-Studio/sersanrepos-projects`, applicata **a mano** da workstation; la VM ha `lifecycle { ignore_changes = all }` | [verificato: `docs/backup_offsite_azure.md` nota e §2] |

### 3.2 Il Terraform nel repo (mai applicato)

`infra/azure/main.tf` descrive Azure Container Apps: resource group, Container Apps Environment, Key Vault (RBAC, purge protection, ACL deny), VNet `10.0.0.0/16` con 2 subnet delegate e private DNS, PostgreSQL Flexible Server (default `B_Standard_B1ms`, 32 GB, SSL, backup 35 gg geo-redundant), 7 Container App (backend 0,5 vCPU/1 Gi 1-3 repliche; frontend 0,5/1; worker-linkedin 1,0/2 Gi max 1; worker-email 0,5/1 0-2; beat 0,25/0,5; Prometheus e Grafana 0,5/1 con Azure Files 50 + 5 GB), ruoli Key Vault Secrets User. Il backend `azurerm` per lo stato remoto è **commentato**; il job `terraform` è stato tolto da `deploy.yml`. Il ramo AWS (ECS Fargate, RDS) è uno scheletro [verificato: `infra/azure/main.tf`, `infra/modules/{container_app,database,key_vault,networking}/main.tf`, `docs/DEPLOYMENT.md`].

### 3.3 Backup oggi

- Dump notturno 03:00 (`scripts/ops/db_backup.sh`: `pg_dump | gzip -9`, cifrato con `age`, chiave privata **fuori** dalla VM per costruzione); retention 35 gg con pavimento di 3 file e protezione dell'artefatto provato dall'ultimo drill; drill di restore non distruttivo la domenica 04:00 [verificato: `docs/backup_strategy.md` §2-3, `docs/OPERATOR_GUIDE.md` §Backup].
- Destinazione: `/opt/backups/sersan/prod/` sulla VM: **un solo disco**, su un provider diverso dal database. Off-site Azure Blob GRS: codice vivo ma **no-op** finché `AZURE_BACKUP_STORAGE_ACCOUNT` è vuota; alternativa GitHub Releases documentata il 2026-10-09; lo script esce 7 (off-site non configurato) o 5 (configurato e fallito), 6 senza cifratura, 9 se la privata è sull'host [verificato: `docs/backup_offsite_azure.md`, `scripts/ops/db_backup.sh:336,476,586,983`].
- Misurato in prod 2026-10-06: 6,2 GB di dump, copie in chiaro accanto alle cifrate, permessi `-rw-rw-r--`; dal 2026-10-08 directory `0700`, file `0600`, chiaro rimosso solo dopo un drill riuscito con la chiave corrente [verificato: `docs/backup_strategy.md` §«Il chiaro su disco»].
- `FIELD_ENCRYPTION_KEY` (Fernet) cifra credenziali e cookie LinkedIn: senza di essa un dump è parziale; custodia nel password manager «da confermare» [verificato: `docs/backup_strategy.md` §5-6, `docs/runbooks/credential_compromise.md` tabella].

### 3.4 Costo mensile attuale

**Non trovato.** Nei file non c'è né lo SKU della VM né una fattura. Le sole cifre presenti: stima Azure Monitor ~40-60 $/mese e Azure Files ~3 $/mese per il disegno Container Apps **mai applicato** [verificato: `docs/monitoring_setup.md` §6-7]; deposito ~250 $ per passare Anthropic a Tier 2 [verificato: `CLAUDE.md`]; AimFox 99 $/mese/account, rimosso [verificato: `PROJECT_STATUS_REPORT.md:290`]. Instantly, Perplexity, Apify, Supabase, IPRoyal, VM Azure, VPS WireGuard: nessuna cifra nel repo.

---

## 4. Cosa serve per spostarlo sul server fisico

### 4.1 Servizi da portare

**Compose di prod (8 servizi)** [verificato: `docker-compose.prod.yml`]:

| Servizio | Immagine / build | Ruolo | Note |
|---|---|---|---|
| `db` | `postgres:15-alpine` | Postgres locale | oggi abbandonato (DB su Supabase); torna utile se si riporta il DB in casa |
| `migrate` | `compose/backend/Dockerfile` | one-shot: `manage.py migrate` + `alembic upgrade head` | `restart: on-failure` |
| `backend` | idem | FastAPI, uvicorn `--workers 2`, `expose 8000`, reti `edge` + `internal` | monta `/var/lib/sersan/ops-evidence` in sola lettura; healthcheck su `/health` |
| `frontend` | `compose/frontend/Dockerfile` (tailwind builder alpine + python slim) | Django, gunicorn 2 worker, `expose 8001`, alias `frontend-prod` su `edge`, `CONN_MAX_AGE=30` | `FASTAPI_INTERNAL_URL` pinnato al container name |
| `worker-linkedin` | `compose/worker-linkedin/Dockerfile` (Playwright 1.50 noble, Chromium) | coda `linkedin`, concurrency 1, pool solo, 1 replica, `stop_grace_period 630s` | con trasporto estensione non apre browser; volume `linkedin_captchas_prod` |
| `worker-email` | `compose/worker-email/Dockerfile` | coda `email`, concurrency 1 (throttle Tier 1), preflight prima di Celery | |
| `worker-default` | immagine di worker-email | coda `default` (KPI, segnali, reaper, trigger, probe) | |
| `beat` | immagine backend | scheduler con `PersistentScheduler`, volume `beat_data_prod`, metriche `:9099` | |

**Fuori dal compose ma necessari** [verificato: `docker-compose.prod.yml` header, `infra/monitoring/node-exporter.compose.yml`, `docs/INCIDENT_RUNBOOK.md`, `docs/backup_offsite_azure.md`]:
- **Traefik** (rete `edge` esterna, ACME Let's Encrypt, forwardAuth per Grafana, allowlist WireGuard).
- **Stack monitoring**: Prometheus, Grafana, Loki, Promtail, Alertmanager (con bind mount dei secrets), cAdvisor, node_exporter (con textfile collector), postgres_exporter. Compose non versionato: va ricostruito da `infra/prometheus/prometheus.prod.yml`, `infra/alertmanager/alertmanager.yml`, `infra/grafana/*`, `infra/monitoring/node-exporter.compose.yml` e dall'override generato da `scripts/ops/monitoring_compose.py`.
- **Runner GitHub self-hosted** con label `prod-vm` (deploy e 44 workflow `prod_*`).
- **Cron** backup 03:00 e drill domenica 04:00 (`install_backup_cron.sh --apply`), che sorgente `/opt/apps/sersan-outreach/prod/.env`.
- **WireGuard** per l'accesso admin (oggi via VPS hub).
- Opzionale: lo stack **stage** (`scripts/ops/deploy_stage.sh`).

### 4.2 RAM e CPU misurate [verificato: `docker-compose.prod.yml` commento INFRA-05, misure 2026-10-10]

| Servizio | Idle prod (MiB) | Picco scale test (MiB) | `mem_limit` | `pids_limit` |
|---|---:|---:|---:|---:|
| db | 166 | 261 | 1 g | 512 |
| backend | 291 | 433 | 1 g | 512 |
| frontend | 151 | 149 | 512 m | 256 |
| worker-linkedin | 156 (manual) | non misurato (Chromium 0,5-1,5 GiB se in automation) | 3 g | 1024 |
| worker-email | 186 | 254 | 768 m | 256 |
| worker-default | 220 | 189 | 768 m | 256 |
| beat | 140 | 121 | 384 m | 256 |
| **Somma tetti** | | | **7,4 GiB** su 15,6 | |

CPU: nessuna misura di prod nel repo (non trovato); il bench girava su 4 CPU / 8 GB con tre stack Supabase accanto [verificato: `docs/scale_test_2026-10.md` §3.2]. Log container limitati a 5 × 20 MB per servizio [verificato: `docker-compose.prod.yml` `x-logging`]. Il server HPE con 160 GB di RAM è molto sopra il fabbisogno; la GPU non serve a questo workload [non verificato: deduzione dalle misure].

### 4.3 Porte e reti

| Porta | Chi | Esposizione |
|---|---|---|
| 80/443 | Traefik | pubblica (app, webhook Instantly, estensione, unsubscribe) |
| 8000 / 8001 | backend / frontend | solo `expose` su reti Docker `edge` (Traefik) e `internal` |
| 5432 | Postgres | solo `internal` (se locale) |
| 9100 / 9101 / 9102 / 9099 | metriche worker-email / linkedin / default / beat | interne, scrape Prometheus |
| 9090, 9093, 3000, 3100, 8080, 9187 | Prometheus, Alertmanager, Grafana, Loki, cAdvisor, pg_exporter | Prometheus/Alertmanager solo da WireGuard; Grafana via `/grafana`; Loki solo via Grafana |
| 51820/udp | WireGuard | se il server diventa hub VPN [non verificato: porta del VPS attuale non trovata] |

[verificato: `docker-compose.prod.yml`, `infra/prometheus/prometheus.prod.yml`, `docs/OPERATOR_GUIDE.md` §15; le porte dello stack monitoring sono quelle di default delle immagini]

### 4.4 TLS e ingresso pubblico (il punto delicato)

- **Webhook Instantly**: `POST https://outreach.sersan.io/api/webhooks` deve essere raggiungibile da Internet con TLS valido; rate limit 1200/min per credenziale webhook accettata e 60/min per indirizzo senza credenziale [verificato: `CLAUDE.md` tabella Key Files riga `backend/routers/webhooks.py`]. Il mini PC router/firewall deve fare port-forward 80/443 verso il server e il DNS di `outreach.sersan.io` (su Cloudflare) va spostato sul nuovo IP [non verificato: conseguenza].
- **Estensione Chrome**: `host_permissions`, i `matches` dei content script e `ALLOWED_ORIGINS` in `background.js` sono cablati su `https://outreach.sersan.io`; cambiare dominio obbliga a ricostruire (`scripts/build_extension.py`) e reinstallare l'estensione sui Chrome dei membri [verificato: `extension/manifest.json`, `extension/README.md` §Hosts]. Conviene **tenere lo stesso dominio**.
- **Endpoint senza API key**: `/health`, `/health/ready`, `/api/unsubscribe` (token HMAC per destinatario, 400 senza), `/api/webhooks` (`X-Webhook-Secret`) [verificato: `README.md` §API].
- Django in prod: HSTS 1 anno, SSL redirect, cookie secure; `TRUSTED_PROXY_HOPS=1` (un solo reverse proxy davanti) [verificato: `docs/AUTH_HARDENING_CONTRACT.md` riga 6, `.env.example:603-608`].
- Se il server è dietro NAT d'ufficio con IP dinamico o CGNAT, servono IP statico o DDNS: da verificare con l'ISP [non verificato].

### 4.5 Proxy residenziale per LinkedIn

- Con il trasporto `extension_voyager` i DM e gli inviti partono dal **browser del membro**, dalla sua rete: il server non tocca linkedin.com e «nessun proxy server è richiesto» [verificato: `.env.example` 422-427, `docs/linkedin_inbrowser_send.md` §1].
- Il proxy serve solo se si riattivano le lane Playwright server-side: `LINKEDIN_REQUIRE_PROXY=true` è un gate fail-closed che skippa senza bruciare la coda HITL; un mismatch di paese solleva `SafetyStop`. Provider IPRoyal deciso, prodotto e budget **non decisi**; l'IP del server non va usato come egress LinkedIn (un IP datacenter condiviso ha già fatto scattare la verifica dispositivo) [verificato: `docs/HANDOFF_2026-07-22_proxy_prewarm.md` §2, `CLAUDE.md` §Safety gates, `extension/README.md` §In-browser execution].

### 4.6 Estensione Chrome

Versione `1.6.8`, Manifest V3; permessi `cookies, storage, tabs, alarms, scripting`; content script su `outreach.sersan.io` (e `localhost:8001` solo in dev) e sniffer `salesnav_sniffer.js` su `linkedin.com/sales/*`. Pairing automatico via `<meta name="sersan-pairing-code">` (bearer 30 gg, revocabile); polling di `/linkedin/ext/next-task/` ogni 30 s, conferma `/ext/dispatch-confirm/` prima del click, ricevuta su `/ext/task-result/`; Chrome deve restare aperto e loggato; heartbeat: 3 minuti di silenzio = OFFLINE. Build riproducibile con `build-info.json` e sha256; **non pubblicata** sul Web Store [verificato: `extension/manifest.json`, `extension/README.md`, `frontend/apps/linkedin/urls.py:35-39`, `backend/routers/linkedin.py:2145-3734`].

### 4.7 Database: restare su Supabase o riportarlo in casa

| Opzione | Pro | Contro | Fonte |
|---|---|---|---|
| Restare su Supabase | nessuna migrazione dati; copie indipendenti dal server; `DB_DSN` già pensato per un DB esterno | ~35 ms a round trip (misurato: le pagine seguono i round trip, non il costo delle query); pooler a 15 connessioni; `public` esposto via PostgREST se la Data API è accesa (mitigato da RLS per migration, non sulle viste) | [verificato: `docs/perf_2026-10.md` §2, `.env.example` 55-64, `CLAUDE.md` §Supabase] |
| Postgres locale sul server | latenza ~0; niente cap di connessioni; il servizio `db` del compose esiste già; Alembic ricrea lo schema (`alembic upgrade head`, 124 migrazioni) | DB e backup sullo stesso host: l'off-site diventa **obbligatorio**; serve un `pg_dump`/restore (`docs/runbooks/database_restore.md`, `db_restore.sh --target live --confirm` con i sender fermi); l'hook RLS è inerte fuori da Supabase, correttamente | [verificato: `docker-compose.prod.yml`, `docs/backup_strategy.md` §3] |

### 4.8 Backup off-site

Il codice c'è: upload immutabile su Azure Blob (`--auth-mode login`, 3 retry) oppure GitHub Releases; cifratura `age` con chiave privata off-host obbligatoria (`BACKUP_REQUIRE_ENCRYPTION`, `BACKUP_REQUIRE_OFFSITE`, `BACKUP_REQUIRE_KEY_OFFHOST` veri in prod); la readiness chiede **tre** ricevute separate (freshness, encryption, offsite) più un drill `source=offsite`. Sul server fisico servono: uno storage remoto (Blob GRS, GitHub Releases o altro), la variabile nel `.env` che il cron sorgente, e un drill contro la copia remota (`docs/runbooks/dr_closure_sequence.md`, mai eseguito) [verificato: `docs/backup_offsite_azure.md`, `docs/backup_strategy.md`, `docs/runbooks/dr_closure_sequence.md`].

### 4.9 Monitoraggio e alert

- La config Prometheus di prod **non viene dal repo** (`scripts/ops/sync_prometheus_config.sh --apply` la copia e verifica i target); 21 regole su 98 non erano mai state caricate al 2026-08-31; i sync sono dispatch manuali senza schedule [verificato: `docs/monitoring_setup.md` banner].
- Alertmanager → Telegram: `bot_token_file` in `/etc/alertmanager/secrets/` e `chat_id` per receiver (oggi `0`, che blocca il deploy della config finché non è compilato); al 2026-10-10 node_exporter era senza textfile collector e i secrets non erano montati nel compose della VM; `prod_monitoring_stack.yml -f action=apply` scrive un override per chiudere entrambi [verificato: `infra/alertmanager/alertmanager.yml`, `.github/workflows/prod_monitoring_stack.yml`].
- Sul nuovo host conviene **versionare** il compose di monitoring e Traefik nel repo: oggi sono l'unica metà di prod che vive solo sulla VM [verificato: `docs/HANDOFF_2026-07-20.md:213`].

### 4.10 Deploy e operazioni

Tutto il modello operativo presuppone un runner GitHub **sull'host**: `deploy.yml`, `prod_ops.yml` (log, restart, stato, disco, migrazioni senza SSH), `prod_launch_readiness.yml`, `prod_dr.yml`, `prod_emergency_stop.yml`, `prod_alert_*`, `prod_auth_*`, ecc. Sul server fisico: installare il runner con le stesse label `[self-hosted, prod-vm]`, ricreare `/opt/apps/...`, il `.env` (con `SERSAN_GIT_SHA` scritto dal deploy), `DB_DSN`, e verificare che `deploy_prod.sh` trovi Docker Compose [verificato: `scripts/ops/deploy_prod.sh`, `.github/workflows/deploy.yml:275`, `docs/INCIDENT_RUNBOOK.md`].

### 4.11 Checklist di migrazione (ordine proposto) [non verificato: proposta mia, basata sui vincoli sopra]

1. Rete: IP pubblico statico o DDNS, port-forward 80/443 sul mini PC router, WireGuard sul server o sul VPS esistente, DNS `outreach.sersan.io` pronto a cambiare.
2. Host: Docker + compose, utente `sersan`, directory `/opt/apps/sersan-outreach/{prod,stage,grafana,alertmanager}`, `/opt/backups/sersan/prod`, `/var/lib/sersan/ops-evidence`, `/var/lib/node_exporter/textfile_collector`.
3. Traefik con rete `edge` e ACME; test del certificato.
4. Runner GitHub self-hosted; `.env` di prod ricostruito dal password manager (`FIELD_ENCRYPTION_KEY`, `INTERNAL_API_KEY`, `DJANGO_SECRET_KEY`, chiavi API, `TELEGRAM_*`, `AUTH_IDENTITY_KEYS*`, `INSTANTLY_WEBHOOK_SECRET`).
5. Decisione DB (§4.7); se locale: restore non distruttivo da un dump `age`, poi `--target live --confirm` con i sender fermi.
6. `deploy_prod.sh` dal runner; smoke test (`scripts/smoke_test_deploy.py --env prod`, `prod_post_deploy_readiness.yml`).
7. Webhook Instantly puntato al nuovo host (stesso dominio); prova con `prod_email_canary.yml`.
8. Stack monitoring + Alertmanager con chat Telegram vere; `prod_sync_alert_rules.yml -f apply=true`; drill alert con ack (`docs/runbooks/alert_delivery_drill.md`).
9. Cron backup + off-site + drill remoto; readiness con le tre ricevute verdi.
10. Spegnere la VM Azure solo dopo una settimana di readiness stabile.

---

## 5. Punti di aggancio per un sistema di agenti

### 5.1 MCP read server `mcp_server/` — 19 tool, sola lettura strutturale [verificato: `mcp_server/README.md`, `tools.py`, `growth.py`]

| Gruppo | Tool |
|---|---|
| KPI e revisione (5) | `kpi_overview`, `variant_leaderboard`, `review_feedback`, `reply_digest`, `campaign_scoreboard` |
| Growth OS (14) | `growth_overview`, `action_queue`, `pipeline_overview`, `campaign_performance`, `funnel_breakdown`, `revenue_attribution`, `positive_replies`, `overdue_actions`, `meeting_summary`, `lost_deal_analysis`, `reactivation_candidates`, `partner_performance`, `linkedin_readiness`, `mailbox_readiness` |

Ogni risposta è un JSON con `as_of`, `window`, `scope`, `test_contacts`, `sources`, `open_in_app`; `null` è «sconosciuto», mai zero; denaro in centesimi per valuta, mai sommato tra valute; ogni tool legge **la stessa route della pagina** così da dire il numero che la dashboard mostra. Il client non può emettere scritture (test `tests/mcp/test_the_mcp_server_can_only_read.py`). Gira sulla macchina dell'operatore (`python -m mcp_server`, venv dall'extra `mcp` di `uv.lock`) con `SERSAN_API_BASE_URL`, `SERSAN_USER_ID`, `SERSAN_API_KEY_FILE`; dal 2026-10-03 firma ogni richiesta con `X-Caller-Token` (client `mcp-read`, chiave `AUTH_IDENTITY_KEYS__CLIENT_MCP_READ`). Vista **agenzia** con `SERSAN_MCP_ALLOW_UNSCOPED=1` (`system:mcp`). Funziona anche dalla app ChatGPT desktop (stdio); per claude.ai o ChatGPT web servirebbero un host HTTPS e un server OAuth (non esistono). `/api/kpi/summary` misurato a 28,7 s.

### 5.2 MCP operator `mcp_operator/` — 14 operazioni, ognuna un bottone dell'app [verificato: `mcp_operator/README.md`, `operations.py`]

`create_campaign_draft_from_blueprint`, `import_leads` (solo preview senza `confirm=true`), `generate_drafts` (max 3 persone per chiamata, mai approva), `list_review_queue`, `approve_message` (con `expected_fingerprint`: 409 `draft_changed` se il testo è cambiato), `reject_message` (una delle nove ragioni), `assign_owner`, `update_deal`, `record_next_action`, `record_meeting`, `change_deal_stage`, `assign_partner`, `reactivate_deal`, `pause_campaign`.
**Non esistono** launch, approvazione in blocco, send-control, cancellazioni, soppressioni, mailbox o domini: il client rifiuta tutto ciò che non è in `MUTATIONS`/`READS`, e dal 2026-10-09 anche il backend ha un tetto di route per il client `mcp-operator` (MCP-01). Richiede `SERSAN_USER_ID` (ogni cambiamento è di quella persona, ruolo di workspace verificato), marca `review_note = "via assistant (mcp-operator)"`, e **approvare non è inviare**: la send lane ricontrolla readiness, pilot, send mode, soppressione, reply e cap [verificato: anche `docs/audit/unaudited_areas_2026-10-09.md` MCP-01, MCP-09].

### 5.3 API REST (269 endpoint) [verificato: `backend/main.py` 389-465, `docs/CODE_INVENTORY.md`]

Prefissi: `/api/review`, `/api/onboarding`, `/api/campaigns`, `/api/leads`, `/api/inbound/first-party`, `/api/deals`, `/api/partners`, `/api/sequences`, `/api/authz`, `/api/mailboxes`, `/api/domains`, `/api/deliverability`, `/api/kpi`, `/api/growth`, `/api/reactivation`, `/api/unibox`, `/api/workspaces`, `/api/linkedin-groups`, `/api/search-keywords`, `/api/sales-nav-searches`, `/api/sales-nav-runs`, `/api/signal-events`, `/api/trigger-policies`, `/api/scoring-configs`, `/api/sales-nav`, `/api/sales-nav-staff`, `/api/signal-inbox`, `/api/body-template-variants`, `/api/linkedin`, `/api/prompts`, `/api/pilot`, `/api/system`, `/api/linkedin/manual`, `/api/linkedin/inbound`, `/api/send-control`, `/admin/sync`, `/admin/metrics`, `/api/webhooks`.
Autenticazione: `X-API-Key` (una chiave condivisa `INTERNAL_API_KEY`), `X-User-Id` per lo scoping (ometterlo = chiamante di sistema senza scoping), `X-Caller-Token` firmato per famiglia (`AUTH_IDENTITY_KEYS__*`: nove famiglie + due client MCP), modalità `observe`; rate limit slowapi 60/min per IP in memoria, un bucket per tutto il traffico Django→FastAPI [verificato: `.env.example` 181-321, `docs/AUTH_HARDENING_CONTRACT.md` §1 e riga 7].

### 5.4 Coda HITL e autopilot

Tabella `outreach_messages`: `pending_review → approved → sent` (email: `approved → sent_to_instantly → sent` via webhook). L'approvazione è legata al **fingerprint** del testo letto (`PATCH /api/review/{id}`); esiste anche `POST /api/review/bulk-approve` (non esposto all'operator MCP) [verificato: `backend/routers/review.py:637,812`, `CLAUDE.md`]. Il pilot (`pilot_configs`) ha tetti giorno/ora (default assoluti 100/25), finestra oraria nel fuso del prospect, allowlist ≤ 100, durata ≤ 60 gg, modi di approvazione `manual_all` / `manual_linkedin` / `auto_blank_invites` / `auto_linkedin`; `PILOT_MODE=enforce` vincola ogni campagna, e una campagna non configurata è **ferma**, non libera [verificato: `docker-compose.prod.yml` envelope, `docs/pilot_mode.md` §1-3, `git log` 2026-10-14/15]. La lane `li-autopilot` (ogni 30 min) è già un «agente» che redige e approva entro l'envelope [verificato: `workers/beat_schedule.py:85`, `docs/linkedin_inbrowser_send.md`].

### 5.5 Entità commerciali già pronte per gli agenti

| Entità | API / tabella | Note | Fonte |
|---|---|---|---|
| Eventi commerciali | `commercial_events`: `engaged`, `positive_reply`, `meeting_booked`, `meeting_held`, `qualified`, `proposal_sent`, `won`, `lost`; dedup key unica; trigger che rifiuta UPDATE/DELETE/TRUNCATE; `GET /api/growth/ceo-funnel` e `/members` | scritti solo da `backend/services/commercial_events.py`, idempotenti, nessun backfill | [verificato: `backend/models/commercial_event.py:3-35`, capability map riga 24] |
| Deals | `GET /api/deals/`, `/board`, `/{id}`, `PATCH /{id}`, `POST /{id}/stage`, `/{id}/partner`; `deal_activities` | valore in centesimi per valuta; 91 aperti senza valore | [verificato: `backend/routers/deals.py`] |
| Meetings | `POST /api/deals/{id}/meetings`, `/{meeting}/answer`, `/reschedule`; `GET /api/growth/meetings` | stati booked/held/cancelled/no_show/rescheduled, mossi solo da una persona | [verificato: `backend/routers/deals.py`, `CLAUDE.md` §CRM tracking] |
| Action queue | `GET /api/growth/action-queue` (P0–P3, `limit/tier/offset`), `POST …/{kind}/{id}/done|snooze|reopen|assign` | pagina `/growth/actions/` | [verificato: `backend/routers/growth.py`] |
| Revenue / funnel | `GET /api/growth/summary`, `/revenue`, `/lost-deals`, `/lead-sources` | per valuta, NULL ≠ 0, test contact esclusi | [verificato: `backend/routers/growth.py`] |
| Segnali e trigger (ADR-031) | `/api/signal-events` (`taxonomy`, `leads/{id}`, `score`, `first-party`, `reject`, `dashboard`, `outcomes`), `/api/trigger-policies`, `/api/scoring-configs`, `/api/signal-inbox`; lane `trigger-generation` ogni 15 min (`TRIGGER_GENERATION_MODE` off/observe/enforce, max 10) | redige DM LinkedIn su trigger, mai email | [verificato: `backend/routers/signal_events.py`, `.env.example` 430-436, `workers/beat_schedule.py:60`] |
| Inbound first-party | `POST /api/inbound/first-party/record`, `GET/PUT/DELETE /routes/{source_key}`, `POST /leads/{id}/route`; stato `inbound_held` | mai esercitato in prod | [verificato: `backend/routers/first_party_inbound.py`, capability map riga 1] |
| Risposte | `POST /api/webhooks` (Instantly), `POST /api/linkedin/inbound/record` (manuale), `inbound_events`, `/api/unibox/threads`, `/threads/{lead}/reply`, `/conversations/{lead}`, `/reconciliation/*` | classificatore keyword + `uncertain-reply hold` | [verificato: `backend/routers/unibox.py`, `backend/routers/manual_inbound.py`] |
| Kill switch | `GET/POST /api/send-control/`, `POST /api/send-control/email-campaigns/pause`, `PILOT_EMERGENCY_STOP`, `scripts/ops/emergency_stop.py` | un'emergenza email richiede kill switch **e** pausa Instantly | [verificato: `backend/routers/send_control.py`, `CLAUDE.md` §HITL] |
| Readiness | `GET /api/system/readiness`, `/readiness/evidence`, `/integrations`, self-test e canary email/LinkedIn | riporta `deployed_commit` | [verificato: `backend/routers/system.py`] |

### 5.6 Notifiche e canali verso le persone

- **Telegram** (uscita): `operator_notify.py` per push KPI notturno (`workers/kpi/alerts.py`, cooldown 24 h per campagna/metrica) e risposte non attribuibili; Alertmanager per gli alert infrastrutturali con drill + ack umano (`prod_alert_drill.yml`, `prod_alert_ack.yml`). Nessun bot con comandi in ingresso [verificato: `backend/services/operator_notify.py`, `workers/kpi/alerts.py`, `.github/workflows/prod_alert_ack.yml`].
- **Email transazionale Django** (`EMAIL_HOST`…): inviti e set-password; se vuoto, backend console (nessuna consegna, nessun errore) [verificato: `docs/DEPLOYMENT.md` §6].
- **Prometheus**: `/metrics` per servizio con metriche `sersan_*` (coda HITL, budget LinkedIn, caller identity, token LLM) [verificato: `backend/metrics.py`, `docs/monitoring_setup.md`].

### 5.7 Code Celery e scheduler

Tre code (`linkedin`, `email`, `default`) su broker Postgres senza visibility timeout: reaper con `QUEUE_BROKER_RECOVERY_MODE` (observe/enforce), lease 600+ s, DLQ rigiocabile con `scripts/ops/queue_dlq.py`; un agente può accodare task esistenti (es. `enrich_single_lead`, `run_kpi_aggregation`) o aggiungere una lane [verificato: `.env.example` 90-124, `docs/scale_test_2026-10.md` §1.2].

### 5.8 Estensione e browser del membro

L'estensione è l'esecutore «umano-in-sessione» per LinkedIn: polling, claim, conferma, ricevuta, hold dell'account su checkpoint/429/999, lettura del limite settimanale di inviti prima del click. Un agente non deve replicarla: deve solo lasciare messaggi `approved` dentro l'envelope [verificato: `extension/README.md` §executor contract, `docs/linkedin_inbrowser_send.md`].

### 5.9 Operazioni via GitHub

44 workflow `prod_*` eseguono sul runner dell'host: log/restart/disco, readiness, backup/DR, canary email e LinkedIn, self-test reply, emergency stop, stato LinkedIn, sync alert, chiavi identità, MFA preflight. Sono già un'interfaccia operativa per un agente ops (vincoli: solo da `main`, `gh` senza scope `workflow` non può modificarli) [verificato: `ls .github/workflows`, `.github/workflows/prod_monitoring_stack.yml`, `docs/monitoring_setup.md`].

### 5.10 Cosa manca per agenti «veri»

- Identità firmata in `enforce` (oggi `observe`; il 2026-10-03 797 richieste su 797 arrivavano senza token perché nessuna chiave è deployata) e una chiave per famiglia [verificato: `docs/AUTH_HARDENING_CONTRACT.md` riga 3, `docs/runbooks/auth_identity_rollout.md`].
- Il server MCP installato non parte (config su worktree cancellato); l'operator non è installato [verificato: capability map riga 20].
- Costo LLM: token sì, prezzi no; nessun alert di spesa [verificato: `workers/kpi/llm_cost.py`].
- Nessun bot Telegram/Slack in ingresso; nessun webhook inbound generico (`inbound webhook unavailable` nel registro sorgenti) [verificato: capability map riga 1].
- I server MCP sono stdio locali: per un orchestratore sul server servirebbe un trasporto HTTP + OAuth, che il repo descrive ma non ha [verificato: `mcp_server/README.md` §«What ChatGPT on the web, and claude.ai, would still need»].

---

## 6. Rischi aperti

| # | Rischio | Stato misurato | Cosa serve | Fonte |
|---|---|---|---|---|
| 1 | **Compliance email** | ADR-004: deroga **permanente** su indirizzo fisico, link unsubscribe cliccabile e privacy policy (opt-out testuale «Rispondi STOP» da ogni step); ADR-020 e ADR-030 proposti e non approvati; `compliance_jurisdiction` vuota su ogni campagna; la campagna «Ricerca Clienti» aveva deroga con autorità `sad`, invalidata il 2026-09-09: la send lane trattiene i messaggi in `approved`. La readiness email resta rossa per scelta | founder + legale: compilare `physical_address`/`sender_country` (Sersan Limited, 128 City Road, London EC1V 2NX) **oppure** registrare la deroga per esteso; decidere la giurisdizione (entità UK, destinatari IT: CAN-SPAM / GDPR-ePrivacy / PECR) | [verificato: `docs/compliance_decision_checklist.md` §D0, `docs/compliance/email_compliance_decision_2026-10-09.md` §0-2, `docs/adr/ADR-030…` intestazione] |
| 2 | **LinkedIn ToS / ban** | nessun trasporto ufficiale esiste (zero chiamate a `api.linkedin.com`, zero OAuth); `extension_voyager` è `browser_automation`, **non production-eligible**; acceso con `LINKEDIN_ACCEPT_UNAUTHORIZED_AUTOMATION_RISK` (log `OWNER-RISK OVERRIDE` a ogni invio); `auto_linkedin` approva DM senza persona; 1/1 account attivo fermo su checkpoint al momento del ledger; like/comment disabilitati (SO-185) | decisione esplicita dei CEO su quanto rischio d'account accettare; budget per account in `enforce`; `linkedin_partner_messaging` è registrato ma «idoneo, non posseduto» | [verificato: `docs/linkedin-transport-authority.md` §2-4, `docs/linkedin_inbrowser_send.md` §2, `docs/linkedin_automatic_acceptance.md`] |
| 3 | **Identità dei chiamanti** | `AUTH_IDENTITY_MODE=observe`; una sola `INTERNAL_API_KEY` accettata su ogni router (launch e bulk-approve inclusi); `X-User-Id` non firmato (ometterlo dà più accesso); nessuna chiave deployata; readiness `auth_hardening` FAIL | rampa `auth_identity_rollout.md` (chiavi → observe → preflight GO → enforce); `prod_auth_identity.yml` installa le chiavi client MCP senza SSH | [verificato: `docs/AUTH_HARDENING_CONTRACT.md` §1-2, `.env.example` 181-285, ledger P2] |
| 4 | **MFA** | `PRIVILEGED_MFA_MODE` non impostata (`observe`); 7 account staff attivi (id 1-7), 4 superuser, **0** iscritti (misura 2026-10-03); `enforce` oggi chiuderebbe fuori tutti; provider TOTP scritto in-tree | de-staffare chi non serve, iscrivere ≥ 2 superuser, poi `enforce` | [verificato: `docs/runbooks/staff_mfa.md` §1 e §6] |
| 5 | **Backup off-site** | assente (`backup_offsite` FAIL); dump cifrati su un disco solo; `FIELD_ENCRYPTION_KEY` nel password manager «da confermare»; chiusura DR mai eseguita | provisionare Blob GRS (PR `sersanrepos-projects#3` pronta) o GitHub Releases; drill `prod_dr.yml -f action=restore-offsite` | [verificato: `docs/backup_strategy.md` §6, `docs/backup_offsite_azure.md`, `docs/runbooks/dr_closure_sequence.md`] |
| 6 | **Alert mai provati** | destinazione, routing e ricezione umana **FAIL**; `chat_id` segnaposto; 21/98 regole mai caricate (2026-08-31); textfile collector e secrets non montati (2026-10-10) | chat Telegram vere, `prod_sync_alert_rules.yml -f apply=true`, drill con ack | [verificato: `docs/monitoring_setup.md`, `.github/workflows/prod_monitoring_stack.yml`, ledger P0] |
| 7 | **Metà di prod non versionata** | compose monitoring, Alertmanager, Traefik vivono solo sulla VM; Prometheus di prod non legge il repo | portarli nel repo prima della migrazione | [verificato: `docs/HANDOFF_2026-07-20.md:213`, `docs/monitoring_setup.md`] |
| 8 | **Supabase esposizione** | `public` raggiungibile da PostgREST se la Data API è accesa (impostazione «ALEX-ONLY», non verificabile dal repo); RLS per migration copre le tabelle, non le viste; pooler a 15 connessioni condiviso da tutti i servizi | verificare la dashboard Supabase; o riportare il DB in casa | [verificato: `CLAUDE.md` §Supabase, `docs/audit/supabase-exposure-2026-09-16.md`] |
| 9 | **Doc drift** | `HANDOVER.md`, `PROJECT_STATUS_REPORT.md`, `docs/DEPLOYMENT.md`, Terraform descrivono topologie mai esistite; il ledger porta evidenze runtime di agosto | fidarsi di `PRODUCTION_READINESS.md` + capability map + record di accettazione, rimisurando | [verificato: banner di quei file] |
| 10 | **Throughput e costo LLM** | Tier 1 limita a ~4 call/min; token contati, prezzi no | Tier 2 (≈ 250 $) e listino in Grafana | [verificato: `CLAUDE.md`, `workers/kpi/llm_cost.py`] |
| 11 | **Dipendenza da un solo browser** | con l'estensione, Chrome chiuso o PC in sleep = nessun invio; `delivery_unknown` trattiene il destinatario su ogni canale finché una persona riconcilia; Michele non onboardato | processo operativo e seconda persona onboardata | [verificato: `docs/linkedin_automatic_acceptance.md` §1, capability map riga 6] |
| 12 | **Operazioni prod da GitHub** | ogni `prod_*` è esecuzione di codice sulla VM per chi ha write access; il piano Team non permette required reviewer; mitigato con main-only + branch protection | valutare il piano GitHub o un gate esterno | [verificato: `docs/audit/unaudited_areas_2026-10-09.md` OPS-10/11] |
| 13 | **Prestazioni pagine** | dashboard p95 6,7 s e readiness 6,4 s sotto carico (bench, DB a 35 ms) | DB locale e/o ottimizzazione delle query del board | [verificato: `docs/scale_test_2026-10.md` §3.2, `docs/perf_2026-10.md` §2] |

---

## 7. Documenti da allegare (i più utili per i CEO)

| File | Perché |
|---|---|
| `C:/Users/alber/SerSanOutreach/docs/architecture.md` | diagrammi, stack, stato per componente, in italiano |
| `C:/Users/alber/SerSanOutreach/docs/growth_os_capability_map.md` | le 25 capability con «provato live» e i volumi reali |
| `C:/Users/alber/SerSanOutreach/docs/sersan_company_profile.md` | ICP, posizionamento, regole di copy: serve anche agli agenti di brief e offerta |
| `C:/Users/alber/SerSanOutreach/README.md` | overview, pipeline, API, variabili |
| `C:/Users/alber/SerSanOutreach/docs/PRODUCTION_READINESS.md` | il verdetto fail-closed e le righe rosse |
| `C:/Users/alber/SerSanOutreach/mcp_server/README.md` | i 19 tool MCP in lettura e le garanzie |
| `C:/Users/alber/SerSanOutreach/mcp_operator/README.md` | le 14 operazioni MCP controllate |
| `C:/Users/alber/SerSanOutreach/docker-compose.prod.yml` | servizi, limiti di memoria misurati, reti |
| `C:/Users/alber/SerSanOutreach/docs/backup_strategy.md` | stato reale di backup e DR |
| `C:/Users/alber/SerSanOutreach/docs/monitoring_setup.md` | stato reale di alert e monitoring |
| `C:/Users/alber/SerSanOutreach/docs/linkedin_inbrowser_send.md` | invio dal browser del membro e posizione sul ToS |
| `C:/Users/alber/SerSanOutreach/docs/compliance/email_compliance_decision_2026-10-09.md` | le decisioni di compliance per founder e legale |
| `C:/Users/alber/SerSanOutreach/extension/README.md` | l'estensione e il blocco della pubblicazione |
| `C:/Users/alber/SerSanOutreach/docs/CODE_INVENTORY.md` | i numeri del codice |
| `C:/Users/alber/SerSanOutreach/docs/scale_test_2026-10.md` | cosa regge e cosa no sotto carico |

---

## 8. Domande aperte (per Michele e Alessandro)

1. SKU, vCPU, disco e costo mensile della VM `vm-apps-01`, del VPS WireGuard e del piano Supabase: non sono nel repo.
2. Piani e costi reali di Instantly, Perplexity, Apify, IPRoyal: non sono nel repo.
3. Il database resta su Supabase o torna sul server fisico insieme al resto?
4. Si tiene il dominio `outreach.sersan.io` (necessario per non ricostruire l'estensione) e chi gestisce DNS Cloudflare e IP pubblico del server?
5. Chi decide le D0 di compliance (indirizzo fisico vero vs deroga registrata, giurisdizione) e con quale parere legale?
6. Quanto rischio d'account LinkedIn si accetta con `auto_linkedin`, e si compra il proxy IPRoyal (quale prodotto) o si resta solo sul browser dei membri?
7. Chi custodisce `FIELD_ENCRYPTION_KEY` e la chiave privata `age`, e dove va la copia off-site?
8. Il broker Celery sta su Supabase o sul container `db` abbandonato? (non verificato)
9. Quando si porta l'identità firmata a `enforce` e l'MFA dello staff: prima o dopo la migrazione?
