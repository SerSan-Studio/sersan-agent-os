# 20 · Proposta E: Claude-native, demone sottile + Claude Agent SDK

**Per:** Alessandro Serratt e Michele Sanna, tramite Alberto Tuveri. **Autore:** architetto E di sette. **Data:** 24/10/2026.

**Legenda.** [verificato: fonte] = letto nella fonte; [non verificato] = stima o proposta. 00-18 sono i rapporti in `ricerca/`. Tutti i file richiesti esistono.

---

## 1. L'architettura in una pagina

Un **demone nostro, piccolo** (`sersand`) decide chi può agire, chiede il sì, esegue, conta i token, ricorda e traccia. **Claude è la forza lavoro**, a consumo sulla chiave API. Le persone restano sui posti Claude Team.

```
 PERSONE (4) ── Claude Team: chat, Projects, Claude Code, Claude Tag in Slack
      │  Slack: #agenti · #cliente-x · #call-vendita · DM     Telegram: carte, /stop
      ▼
 ┌─ sersand · TypeScript sul server ─────────────────────────────────────────────
 │ protocollo · policy · carte · outbox · audit · conservazione · redazione
 │ guardia anti-iniezione · report del mattino · banca dei token · routine
 │ registro degli agenti · passaggi fra agenti con freno
 │ porta dei modelli: aggiunge la chiave, conta, ferma a budget
 └──┬───────────────────┬────────────────────┬────────────────────┬────────────
    │                   │                    │                    │
  CHIAMATE            SESSIONI             MODELLI LOCALI       ESECUTORI
  Messages API,       Agent SDK su API     RTX 4000 8 GB:       (unici con effetti)
  JSON a schema,      key; utente Linux    giudice Qwen3-4B,    Slack · Gmail · moda
  Haiku/Sonnet/Opus   e cgroup per lavoro; embedding, Whisper;  SersanOutreach
                      web nella sandbox    redazione su CPU     ElevenLabs + Twilio
                      Managed Agents                            Metricool · Notion
    └── MEMORIA: Postgres 17 + pgvector (meeting, mail, documenti, eventi)
        + vault Markdown in git (regole per persona, processi, catalogo)
        + SersanOutreach (CRM: deal, meeting, eventi commerciali, to-do)
 INGRESSI: Recall.ai nelle call · webhook firmati via Cloudflare Tunnel · form lead
```

Le quattro regole del disegno:

1. **I modelli propongono, il codice esegue.** Nessun agente ha strumenti che inviano, pubblicano, pagano o cancellano: chiama `propose_action`, la policy risponde `allow/ask/deny`, con `ask` nasce una carta su Slack o Telegram, dopo il sì un esecutore agisce una volta sola.
2. **Due tipi di lavoro.** Riassumere, classificare ed estrarre sono chiamate dirette alla Messages API, da centesimi. Solo i lavori a più passi (brief, offerta, deck) aprono una sessione Agent SDK: Claude Code senza schermo, guardrail fuori dal prompt.
3. **Persone su abbonamento, automazioni su API**, come chiedono i termini Anthropic [verificato: 10 §1 punto 5]. Con la chiave si spengono Routines e connettori claude.ai: il demone usa server MCP propri.
4. **Locale solo dove vince**: privacy, embedding, audio [verificato: 13 §0 punti 5 e 8].

**Quanto codice.** Si scrivono **15.000-22.000 righe nuove** di TypeScript, 2.000-3.000 di Python e 30-40 file di prompt e skill [stima]. In tutto **119 giorni-persona in circa 20 settimane**; primo rilascio utile alla settimana 8 (§6).

---

## 2. Copertura A1-I4

Stati: **P** pronto, **A** da adattare, **C** da costruire, **S** in abbonamento.

| # | Componente | Stato | Fonte |
|---|---|---|---|
| A1 | Bot Recall.ai dichiarato nelle call; riunioni fisiche dal telefono; trascrizione in casa (faster-whisper, pyannote) | S + C | 14 §4; 13 §5 |
| A2 | Vault Markdown in git + CRM di SersanOutreach; Notion facoltativo come vista | A | 01 §5.5 |
| A3 | Postgres + pgvector; embedding e reranker Qwen3 0.6B locali | C | 13 §7 |
| A4 | `sersand` + sessioni Agent SDK | A | — |
| A5 | Registro: una riga per agente (ruolo, connettori, tetti); raccolta e pulizia come lavori Haiku o senza modello | A | — |
| A6 | Skill versionate; un agente revisore propone modifiche settimanali, una persona approva | C | — |
| A7 | `#agenti` su Slack, ogni agente col suo nome; passaggi registrati nel demone con freno | C | — |
| B1 | Recap automatico nel canale interno del cliente; in quello condiviso col cliente dopo carta | C | 00 B1 |
| B2 | Esecutore sulle operazioni di `mcp_operator` (`record_meeting`, `update_deal`) | A | 01 §5.2 |
| B3 | Bozza vera della mail + carta; invia l'esecutore | C | — |
| B4 | To-do commerciali nella coda azioni di SersanOutreach, gli altri nel vault | A | 01 §5.5 |
| B5 | Autonomia a gradini per classe d'azione (§5) | A | — |
| C1 | Report del mattino con sezioni (calendario, meeting, pipeline, carte, budget), 05:30 su Slack e Telegram | A | — |
| C2 | Bot Recall.ai al posto di chi manca | S | 14 §4 |
| C3 | Sonnet 5.5 con uscita a schema (punti, impegni, next step) | C | 13 §2.3 |
| C4 | Note vocali Slack e Telegram trascritte in casa; dettatura delle app Claude | C + P | 13 §5 |
| C5 | Registro dei meeting (presenti, esito, pipeline emersa), cercabile da Slack e Claude Code | C | 00 C5 |
| C6 | `regole/<persona>.md` nel prefisso in cache dei lavori per quella persona | C | — |
| D1 | Probabilità per stadio dagli `commercial_events`, con intervallo; serve storico (oggi 0 vinte) | C | 01 §1.4 |
| D2 | Sessione Agent SDK: segnali e storico di SersanOutreach, mail, calendario, web in sandbox Managed Agents | C | 01 §5.5; 18 §2.1 |
| D3 | Storico della relazione dentro il brief | C | 01 §5.5 |
| D4 | Deck dal server MCP di moda.app o con Claude Slides | S + C | 14 §6 |
| D5 | Opus 5.5: catalogo nel vault + trascrizione + brief → bozza → carta | C | 00 D5 |
| E1, E2, E4 | Argomenti per i CEO; formazione in H1 | n.a. | 00 §E |
| E3 | Banca dei token: porta dei modelli che ferma per persona, agente e catena | A | — |
| F1 | Job mensile sui log di Google Workspace, solo aggregati | C | 16 §1.2 |
| F2 | Agente intervistatore in DM Slack | C | 00 F2 |
| F3 | Mappa dei processi (Mermaid) nel vault | C | 00 F3 |
| F4 | Ore × frequenza → classifica delle automazioni | C | 00 F4 |
| F5 | Claude Team per tutti, Claude Tag nei canali, agenti in Slack | S | 18 §2.1 |
| G1 | `#call-vendita`; chi è sales e chi cliente da diarizzazione e invito | C | 13 §5 |
| G2 | Fit score dalla call + qualificatore GP+BALD di SersanOutreach | A | 01 §1.1 |
| G3 | Coaching solo all'interessato, niente emozioni | C | 16 §1.2 |
| G4 | Al responsabile solo indicatori aggregati, finché i CEO non decidono sull'alto rischio | C | 16 §4 |
| G5 | «Andrea»: ElevenLabs Agents + numero Twilio italiano; il demone verifica consenso e Registro delle opposizioni, poi chiama entro 90 s | S + C | 14 §3.4; 16 §2 |
| G6 | Esiti valutati ogni settimana; nuove aperture con carta e prova A/B | C | 00 G6 |
| G7 | KPI (tempo al richiamo, meeting fissati) nel report | C | 00 G7 |
| G8 | `lost_deal_analysis` + trascrizioni → temi per l'agente editoriale | A | 01 §5.1; 05 §5.6 |
| G9 | Organigramma generato dal registro (`reports_to` = persona responsabile) | A | — |
| G10 | Esito, non funzione | n.a. | 00 G10 |
| H1, H2, H5, H7 | Posti Team per tutti; ognuno possiede almeno un agente; formazione art. 4 AI Act | processo | 16 §4 |
| H3 | Assessment con l'intervistatore di F2 | C | 00 H3 |
| H4 | Più budget agli ambassador nella banca dei token | P | — |
| H6 | Classifica mensile delle automazioni per autore | C | 00 H6 |
| I1, I2 | Il contesto è A1-A3 | n.a. | 00 §I |
| I3 | Elenco delle esclusioni nella policy: niente voce o volto dei founder, niente DM dai loro profili, niente voti alle persone, niente emozioni | A | 05 §5.8 |
| I4 | Agenti del marketing (§4) | C | 05 §5 |

**Conteggio** sulle 43 righe con software: 12 da adattare, 24 da costruire, 2 in abbonamento, 3 in abbonamento più codice nostro, 1 pronta, 1 in parte pronta. Nessuna voce resta scoperta, ma due terzi sono codice da scrivere.

---

## 3. Server e abbonamenti

Proxmox con 128 GB bilanciati (8 moduli), come consiglia 15 §2.2 [verificato].

| Macchina virtuale | vCPU | RAM | Disco | Contenuto |
|---|---|---|---|---|
| apps-prod | 8 | 24 GB | 80 GB | SersanOutreach (tetti misurati 7,4 GiB [verificato: 01 §4.2]), `sersand`, adattatori Slack e Telegram, Traefik, `cloudflared` |
| apps-stage | 4 | 8 GB | 40 GB | prove |
| agenti | 8 | 24 GB | 100 GB | fino a 8 sessioni Agent SDK insieme, 0,5-1,5 GB ciascuna [stima] |
| gpu | 4 | 24 GB | 80 GB | RTX 4000: giudice Qwen3-4B, embedding e Whisper turbo [verificato: 13 §8]; reranker, pyannote e redazione su CPU |
| data | 4 | 24 GB | 300 GB | Postgres 17 + pgvector, vault in git |
| monitor + backup | 4 | 12 GB | dischi propri | Prometheus, Grafana, Loki, Proxmox Backup Server |

Totale 116 GB su 128. Dischi: 2 SSD in mirror ZFS più 1-2 TB di dati [stima]. Un 8B per i dati «solo locali» si carica quando serve, al posto del profilo sempre acceso [verificato: 13 §8].

**In abbonamento, e perché.**
- **Claude API**: con 8 GB nessun modello locale regge gli strumenti in italiano [verificato: 13 §2.3].
- **ElevenLabs + Twilio**: la voce telefonica chiede latenza bassa e numeri italiani [non verificato: 13 §6].
- **Recall.ai**: entrare in Meet, Zoom e Teams è un servizio; la trascrizione resta in casa [verificato: 14 §4].
- **Managed Agents**: le pagine web non fidate si leggono fuori dal server [proposta; prodotto in 12 §1].
- **Slack Pro** per persone e agenti; **Telegram**, gratis, per le carte sul telefono.
- **Claude Team e Claude Tag**: le persone, e le domande al volo nei canali con tetto di spesa [verificato: 12 §1]. Le Routines restano personali e in sola lettura [verificato: 05 §5 regola 5].

---

## 4. SersanOutreach e marketing

**SersanOutreach.** Si migra con le checklist di 01 §4.11 e 15 §7, con Postgres in casa: latenza quasi zero, backup off-site obbligatorio [verificato: 01 §4.7].
- Il demone usa la REST API e i due server MCP: 19 letture e 14 operazioni, mai invio né approvazione in blocco [verificato: 01 §5.1-5.2]. Servono trasporto HTTP per gli MCP, una chiave `agent-daemon` e l'identità in `enforce`, oggi in `observe` [verificato: 01 §5.10].
- SersanOutreach chiama un webhook firmato del demone su lead dal form, risposta positiva e meeting fissato.
- Su LinkedIn gli agenti non entrano: lasciano messaggi `approved` nell'envelope del pilot, eseguiti dall'estensione del membro [verificato: 01 §5.8]. Nessuna tecnica anti-rilevamento.

**Marketing.** Gli agenti entrano nei ruoli delle direttive del 22/10, non al posto dei sì [verificato: 05 §5]: *editoriale* (temi da call, `reply_digest`, obiezioni), *copy* (bozze EN/IT col controllo deterministico delle direttive), *metriche* (Metricool in lettura + KPI di SersanOutreach → numeri del lunedì), *visual* (moda, Higgsfield, HyperFrames, costo letto prima).

Oggi nessuna routine scrive su Metricool [verificato: 05 §3.7]. Proposta: la carta diventa il registro del sì (chi, quando, impronta del testo) e l'esecutore pubblica dopo; finché la regola non cambia, pubblica la sessione presidiata di Alberto. I post dei founder restano nativi.

---

## 5. Controllo e sicurezza

- **Carte.** Impronta del contenuto ricalcolata su Approva; una sola esecuzione; il silenzio non vale sì; dopo un crash l'outbox chiede di controllare invece di rifare; ruoli per classe. Proposta: Alessandro approva outbound e mail ai clienti, Michele offerte e affermazioni tecniche, Alberto infrastruttura e codice.
- **Autonomia a gradini.** L0: carta sempre. L1: regola «Sempre» stretta (destinatario, modello di testo, tetto), creata da una persona dopo 20 approvazioni senza modifiche. L2: controllo a campione. Mai per invii a freddo, offerte, cancellazioni, pagamenti [proposta]. «Andrea» parte in L1, solo per i lead con consenso.
- **Iniezioni.** Corsia `trusted/untrusted` scritta dal codice su ogni elemento; un turno che legge testo non fidato trasforma ogni effetto in carta; i contenuti di terzi li leggono sessioni senza strumenti; destinazioni per ID stabile.
- **Isolamento.** Utente Linux e cgroup per lavoro; nessuna chiave nel processo: le sessioni passano dalla porta dei modelli, che aggiunge la chiave, conta e ferma. Claude Code dietro `ANTHROPIC_BASE_URL` va provato [non verificato]; riserva: una chiave per famiglia di agenti con limiti in Console.
- **Audit e budget.** Eventi senza testo libero, catena di hash con ancora giornaliera, `forget` per persona o cliente, redazione dei segreti; tetti per persona, agente, routine e catena, avviso all'80 %, stop al 100 %.
- **GDPR.** API Anthropic con DPA nei termini commerciali, conservazione 30 giorni, nessuna regione UE [verificato: 16 §5]. Il giudice locale marca `local_only` ciò che non deve uscire; nomi e numeri si oscurano prima del cloud [verificato: 13 §2.3]. Audio ≤ 30 giorni, trascrizioni 24 mesi, log 90 giorni, metadati individuali ≤ 21 giorni [verificato: 16 §6 regola 8]. Registro dei trattamenti legato al codice da un test. Una sola lista di soppressione.
- **AI Act.** Chi scrive o parla a esterni si dichiara AI (art. 50, dal 2/8/2026); niente emozioni; valutare i sales è alto rischio dal 2/12/2027 [verificato: 16 §4]; con dipendenti in Italia vale lo Statuto art. 4 [verificato: 16 §1.2].
- **Stop.** `/stop` da Telegram o Slack ferma lavori, routine e chiamate.

---

## 6. Piano a fasi

Ipotesi: Alberto e Mattia, circa 6 giorni-persona a settimana [stima].

| Fase | Settimane | gg-persona | Cosa si vede alla fine |
|---|---|---|---|
| 0 · Server e SersanOutreach (comune a ogni proposta) | 1-3 | 14 | `outreach.sersan.io` servito dal server; backup off-site provato; Azure spenta dopo una settimana stabile |
| 1 · Nucleo e post-call | 3-8 | 35 | debrief alle 05:30 dalla settimana 5; poi ogni call registrata e trascritta in casa, con recap, opportunità, bozza della mail e to-do come carte su Slack e Telegram; banca dei token; `/stop` |
| 2 · Vendite e chat fra agenti | 9-13 | 30 | brief e deck prima di ogni meeting in calendario; offerta in bozza dopo la call; `#agenti` e organigramma; pipeline pesata v0; coaching all'interessato |
| 3 · Andrea e marketing | 14-17 | 25 | lead del form richiamato entro 90 s, 24/7, dopo il parere legale; numeri del lunedì e bozze dei post |
| 4 · Organizzazione | 18-20 | 15 | mappa dei processi e classifica delle automazioni; assessment; primo premio mensile |
| **Totale** | **20** | **119** | |

Fase 1 in dettaglio: nucleo del demone 9, ruoli e più proprietari 4, porta dei modelli 2, Slack e Telegram con le carte 6, host dei lavori su Linux 4, pipeline delle riunioni 4, memoria e ricerca 3, tre agenti (post-call, debrief, indicizzatore) 3.

---

## 7. Costi mensili

**Formule.**
- `Costo = Σ abbonamenti + API + 0,08 $ × ore Managed Agents + minuti di voce × tariffa + corrente − crediti API − VM Azure spenta`
- `API = Σ lavori n × (T_in × p_in + T_cache × 0,05 × p_in + T_scrittura_cache × 1,25 × p_in + T_out × p_out) + ricerche × 0,01 $`

Prezzi e cambio (0,8934) da 14 §1.1 [verificato]. Un brief su Sonnet (25 giri, 1 M token letti al 90 % da cache, 25.000 scritti) costa circa 0,70 $, un'offerta su Opus circa 1,30 $ [stima]. Chiamate semplici come in 14 §1.5; sessioni al mese: 30, 230 e 650 nei tre scenari [ipotesi].

| € al mese, IVA esclusa | Minimo | Consigliato | Completo |
|---|---|---|---|
| Claude Team, 5 posti premium | 0 (bundle) | 0 | 0 |
| API Anthropic | 54,70 | 195,65 | 486,90 |
| Managed Agents (0 / 300 / 900 ore) | 0 | 21,44 | 64,32 |
| Claude Tag, tetto | 0 | 44,67 | 89,34 |
| Slack | 0 (Free + Telegram) | 27,00 (Pro) | 60,00 (Business+) |
| Notion | 0 (vault) | 0 (vault) | 71,47 (Business) |
| Recall.ai (30 / 30 / 100 ore) | 17,42 | 17,42 | 58,07 |
| Voce: ElevenLabs + numeri + minuti Twilio | 0 | 170,28 | 493,61 |
| Metricool, moda, Higgsfield, Canva | 17,87 | 128,65 | 239,13 |
| Strumenti di SersanOutreach (Instantly, Apollo, Apify, proxy), uguali per tutte le proposte | 46,10 | 159,57 | 575,62 |
| Google Workspace (forse già pagato) | 27,20 | 54,40 | 54,40 |
| 1Password, backup, corrente, UPS | 134,32 | 146,99 | 165,07 |
| **Totale di listino** | **297,61** | **966,07** | **2.357,93** |
| coperto dai crediti API (fino a 714,70 €) | −54,70 | −217,09 | −551,22 |
| **Esborso con i crediti** | **242,91** | **748,98** | **1.806,71** |

Voci da 14 §11, tranne API, Managed Agents e Recall nel completo [stima]. La voce consigliata scende di 88,45 € se il grant ElevenLabs copre il piano. Spegnere Azure fa risparmiare circa 150 € [non verificato: 14 §9]. **A regime** si aggiungono 446,70 € di Claude Team; senza crediti da 800 $ [non verificato: 14 §1.4] l'esborso sale della riga coperta. Una tantum: UPS 1.163-1.293 € [non verificato: 14 §11.3]; nessuna GPU nuova per ora [verificato: 13 §10].

---

## 8. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| Anthropic nel 2026 ha cambiato due volte le regole sugli abbonamenti | chiave API; SDK e Claude Code a versione fissa; chiamate semplici instradabili altrove; dati e nucleo restano nostri |
| Crediti API non confermati: 800 $ al mese, 1.000 $ una tantum o 500 $ in comune [verificato: 14 §1.4] | tetti nella banca dei token; senza crediti il consigliato costa circa 217 € al mese di API |
| La chat fra agenti va costruita; Hermes, buzz e Grok Bot l'hanno pronta [verificato: 10 §4.1; 17 §5; 11 §2.5] | freno nel codice dal primo giorno; registro del demone come verità, Slack come vetrina |
| Sessioni Claude Code pesanti per lavori semplici | due tipi di lavoro; cache dei prompt; Batch API di notte |
| Managed Agents e Claude Tag in beta; Managed Agents fuori da Zero Data Retention [verificato: 12 §1] | solo web pubblico, niente dati dei clienti; facoltativi |
| Pipeline pesata senza storico: 0 trattative vinte al 05/10 [verificato: 01 §1.4] | mostrata con intervallo, provvisoria fino a 30-50 trattative chiuse [stima] |
| «Andrea»: consenso, Registro delle opposizioni, voce clonata [verificato: 16 §2] | parere legale prima della fase 3; voce sintetica, non di un collega; controlli nel codice |
| Un solo server in ufficio | UPS, mirror ZFS, backup off-site, ripartenza su cloud [verificato: 15 §6] |

---

## 9. Perché sceglierla, e perché no

**Perché sì.**
- Un solo fornitore di modelli, già pagato con posti e crediti; nessuna piattaforma di agenti in abbonamento.
- Dati dei clienti, memoria e CRM restano sul nostro server: nel cloud esce solo ciò che il codice lascia uscire.
- Ogni pezzo è nostro: si cambia un agente, un canale o un modello senza cambiare piattaforma.

**Perché no.**
- Molto codice da scrivere (15-22 mila righe): la «squadra di agenti che si parlano» arriva alla settimana 13, mentre Grok Bot la mostra subito [verificato: 11 §9].
- La manutenzione è nostra e dipende da due persone.
- Se Anthropic cambia prezzi o termini, il costo ricade su di noi.
- Sul telefono i CEO hanno carte e report in Slack e Telegram, non un'app di agenti con avatar.
