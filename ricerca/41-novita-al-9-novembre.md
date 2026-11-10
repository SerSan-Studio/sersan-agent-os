# Autonomia degli agenti: novità dal 25/10 al 9/11/2026

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **RAP4**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

**Metodo.** Prima di cercare ho letto ricerca/10, 11, 12, 17, 18, 26, 27, 36 §1-2.4 e la trascrizione di riferimento. Qui riporto solo novità e conferme utili. Le fonti sono documentazione ufficiale, changelog, registri npm e PyPI e API di GitHub, tutte lette il 9/11/2026. Se una funzione è precedente al 25/10 ma manca nei rapporti, lo scrivo («non nuova»).

Etichette:
- **[verificato: fonte, 9/11]**: letto da me oggi sulla fonte indicata.
- **[non verificato: motivo]**: dato di terzi, pagina non raggiungibile o prova non fatta.
- **[proposta]**: una mia indicazione, non un fatto.

Livelli di autonomia: L0 a mano, L1 carta, L2 finestra, L3 autonomo.

---

## 1. Claude Agent SDK e Claude Code

### 1.1 Versioni

| Pacchetto | Ultima versione | Data | Versioni uscite dal 26/10 | Fonte |
|---|---|---|---|---|
| Claude Code | 2.1.321 (canale stable: 2.1.311 del 26/10) | 9/11 | 9 | [verificato: registry.npmjs.org/@anthropic-ai/claude-code, 9/11] |
| Agent SDK TypeScript | 0.3.321 | 9/11 | 9 | [verificato: registry.npmjs.org/@anthropic-ai/claude-agent-sdk, 9/11] |
| Agent SDK Python | 0.2.180 | 9/11 | 6 | [verificato: pypi.org/pypi/claude-agent-sdk/json, 9/11] |

### 1.2 Modalità di permesso, compresa «auto» (conferme)

- **Le sei modalità.** `default` (nell'interfaccia «Manual»), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` [verificato: code.claude.com/docs/en/agent-sdk/permissions, 9/11].
- **Come lavora auto.** Un secondo modello, il classificatore, giudica ogni azione prima che parta. Blocca ciò che va oltre la richiesta, tocca infrastrutture sconosciute o sembra guidato da testo ostile. Giudica anche i messaggi che un agente manda a un altro. Le regole «ask» fanno comunque una domanda. Anthropic scrive che auto «does not guarantee safety». Anthropic può anche spegnere auto lato server: in quel caso la sessione parte in Manual [verificato: code.claude.com/docs/en/permission-modes, 9/11].
- **Dove funziona.** Va con la chiave della Console. Modelli ammessi: Opus 4.6 e successivi, Sonnet 4.6 e successivi, Haiku 5.5, Fable. Il classificatore di default è Sonnet 5 e si cambia con `CLAUDE_CODE_AUTO_MODE_MODEL` [verificato: permission-modes e feature-availability, 9/11].
- **Modalità di partenza.** Le sessioni interattive partono in auto dalla 2.1.283 (25/9). SDK e `-p` partono in Manual dalla 2.1.302 (16/10): per avere auto serve `permissionMode: "auto"` [verificato: permission-modes; date dal registro npm, 9/11].

### 1.3 Novità dopo il 25/10 che contano per l'autonomia

| Data | Versione | Cosa cambia | Fonte |
|---|---|---|---|
| 27/10 | SDK TS 0.3.312 | Le impostazioni dell'SDK espongono `autoMode`, `useAutoModeDuringPlan` e `permissions.disableAutoMode`: le regole di auto si scrivono da codice | [verificato: CHANGELOG di claude-agent-sdk-typescript, 9/11] |
| 30/10 | CC 2.1.314 | `permissions.blockWritesOutsideWorkingDirectories`: in ogni modalità, Write ed Edit rifiutano i percorsi fuori dalle cartelle di lavoro | [verificato: github.com/anthropics/claude-code CHANGELOG, 9/11] |
| 2-3/11 | CC 2.1.317, SDK TS 0.3.317, Python 0.2.177 | `onFailure: "block"` sugli hook: se la callback va in errore o risponde in modo non valido, l'azione è bloccata. Prima, un guardiano `PreToolUse` andato in errore lasciava passare la chiamata al flusso normale dei permessi | [verificato: code.claude.com/docs/en/agent-sdk/hooks; CHANGELOG, 9/11] |
| 3/11 | CC 2.1.318 | Gli agenti Managed Agents creati con `/claude-api managed-agents-onboard` partono con la policy `auto`, come nella Console | [verificato: CHANGELOG, 9/11] |
| 6/11 | CC 2.1.319 | `permissions.denyInsteadOfPrompting`: una chiamata che aspetterebbe una domanda viene negata e il turno continua, anche nei sottoagenti | [verificato: CHANGELOG, 9/11] |
| 6/11 | CC 2.1.319, SDK 0.3.319 | Compiti MCP: una chiamata MCP lunga va in background e il risultato arriva quando finisce. Nell'SDK servono `CLAUDE_AUTO_BACKGROUND_TASKS=1` e l'input in streaming | [verificato: CHANGELOG di CC e SDK, 9/11] |
| 6/11 | CC 2.1.319 | Auto dietro un gateway LLM con telemetria spenta: ciò che il server non può controllare viene chiesto o negato, senza ricadere sul classificatore locale. `CLAUDE_CODE_AUTO_MODE_SERVER=0` riattiva il classificatore locale | [verificato: CHANGELOG, 9/11] |
| 9/11 | SDK 0.3.321 | In auto, i rapporti dei sottoagenti in coda si risolvono con una sola chiamata al modello | [verificato: CHANGELOG SDK, 9/11] |
| 9/11 | API | Fable 5.2: 8 $ / 40 $ per milione di token, conservazione di 30 giorni obbligatoria, niente ZDR senza autorizzazione | [verificato: platform.claude.com/docs/en/release-notes/overview, 9/11] |

Due avvertenze:
- **Gateway.** Per far arrivare il controllo lato server di auto attraverso un gateway, il gateway deve inoltrare intatti l'header `anthropic-beta` e il campo `safeguards`, e restituire `safeguard_results`. Se non lo fa, Claude Code chiede da sé il giudizio al classificatore e quelle richieste si pagano in token [verificato: code.claude.com/docs/en/auto-mode-classifier-billing, 9/11]. Per LiteLLM vedi §7.
- **Strumenti `always_ask`.** In auto, il classificatore può approvare uno strumento marcato `always_ask` prima della nostra callback, a meno che lo strumento porti `destructiveHint: true` [verificato: code.claude.com/docs/en/agent-sdk/typescript, 9/11]. La data di introduzione non l'ho trovata.

### 1.4 Lavori in background, routine, sottoagenti, sessioni

- **Sessioni in background** (`claude --bg`, `claude agents`, supervisore).
  - Sono in anteprima di ricerca e girano sulla macchina locale.
  - Resistono a sospensioni e aggiornamenti, non allo spegnimento.
  - Funzionano con il login o con la chiave API.
  - [verificato: code.claude.com/docs/en/agent-view, 9/11]
- **Compiti programmati nel cloud** (le ex «routine»).
  - Sono in anteprima, sui piani Pro, Max, Ultra, Team ed Enterprise.
  - Partono a orario (non più di una volta l'ora), da una chiamata API (`/fire` con token) o da eventi GitHub.
  - Girano in auto e si fermano sulle regole «ask» o dopo blocchi ripetuti.
  - Appartengono al singolo account e agiscono «come te»; consumano l'uso dell'abbonamento.
  - Vogliono il login claude.ai, non la chiave API.
  - [verificato: code.claude.com/docs/en/routines, 9/11]
  - Novità: livello di effort per routine (2.1.312, 27/10); plugin dell'account caricati nelle esecuzioni (2.1.314, 30/10); ambiente predefinito dell'organizzazione e avviso se `/schedule` aggiunge connettori non chiesti (2.1.317, 2/11) [verificato: CHANGELOG, 9/11].
- **`/loop` e compiti programmati di Desktop.** Intervallo minimo di un minuto, con la macchina accesa. Dalla 2.1.319 il `/loop` autoregolato finisce quando un turno non si riprogramma [verificato: code.claude.com/docs/en/scheduled-tasks; CHANGELOG, 9/11].
- **Sottoagenti.**
  - `CLAUDE_CODE_SUBAGENT_EFFORT` (2.1.316, 31/10) [verificato: CHANGELOG, 9/11].
  - `/tasks` elenca i sottoagenti finiti, che si possono riaprire (2.1.319) [verificato: CHANGELOG, 9/11].
  - Le squadre di agenti restano sperimentali e non partono in `-p` né nell'SDK [verificato: code.claude.com/docs/en/agent-teams, 9/11].
- **Sessioni.** Nessuna funzione nuova. Dalla 0.3.317 c'è il messaggio `session_writes_lost`, che segnala una trascrizione non salvata per disco pieno [verificato: CHANGELOG SDK, 9/11].
- **Projects** (coordinatore con thread). Ancora non offerti sui piani Team ed Enterprise [verificato: code.claude.com/docs/en/claude-projects, 9/11].

### 1.5 Ambienti self-hosted (non nuovi, ma assenti nei rapporti)

- Dal 7/8/2026 (versione 2.1.224) le sessioni cloud di Claude Code, i compiti programmati e le sessioni di Claude Tag possono girare su runner nostri. È una beta pubblica su Team ed Enterprise, spenta di default [verificato: code.claude.com/docs/en/self-hosted-environments; CHANGELOG, 9/11].
- Restano in casa il codice, i file e i segreti. Prompt, risposte e risultati degli strumenti vanno ad api.anthropic.com, che conserva la trascrizione [verificato: stessa pagina, 9/11].
- Non sono disponibili con ZDR. Si pagano con l'uso Claude Code dell'organizzazione, non con la chiave API. Un runner serve un solo proprietario alla volta [verificato: stessa pagina, 9/11].

## 2. Claude Managed Agents e altre offerte ospitate di Anthropic

### 2.1 Cosa fanno, prezzi, dati (conferme)

- **Che cos'è.** Anthropic fa girare il ciclo dell'agente. Noi definiamo l'agente (modello, prompt, strumenti, MCP, skill), l'ambiente (sandbox nel cloud di Anthropic o self-hosted), le sessioni e gli eventi. È in beta con l'header `managed-agents-2026-04-01`, attivo per ogni account API, con la chiave della Console [verificato: platform.claude.com/docs/en/managed-agents/overview, 9/11].
- **Prezzi.**
  - Token al prezzo di listino, più 0,08 $ per ora di sessione, contata solo mentre la sessione è `running`.
  - Ricerca web: 10 $ ogni 1.000 ricerche.
  - Con `inference_geo: "us"` i token costano 1,1 volte.
  - [verificato: platform.claude.com/docs/en/about-claude/pricing, 9/11]
- **Dati.**
  - Le trascrizioni restano finché non le cancelliamo.
  - Non idoneo a ZDR né a HIPAA, sandbox self-hosted comprese.
  - La sede dei dati dello spazio di lavoro è solo «us». L'inferenza è «global» o «us». Nessuna opzione UE.
  - [verificato: overview; platform.claude.com/docs/en/manage-claude/data-residency, 9/11]
- **Sandbox self-hosted** (dal 19/5/2026). Esecuzione degli strumenti, file e uscite di rete stanno in casa; il ciclo resta da Anthropic. Input e output degli strumenti passano da Anthropic, che conserva skill e memory store [verificato: …/managed-agents/self-hosted-sandboxes; release notes, 9/11].

### 2.2 Funzioni di autonomia (precedenti al 25/10, mancanti o incomplete nei rapporti)

| Funzione | Dal | Cosa fa | Fonte |
|---|---|---|---|
| Deployment programmati | 9/6/2026 | Cron al minuto con fuso orario: l'agente apre le sessioni da solo | [verificato: …/managed-agents/scheduled-deployments; release notes, 9/11] |
| Policy `auto` | 10/9/2026 | Il server valuta ogni chiamata: la esegue, la nega oppure mette la sessione in pausa per un'approvazione | [verificato: …/managed-agents/permission-policies; release notes, 9/11] |
| Policy di default | — | Strumenti dell'agente `always_allow`, strumenti MCP `always_ask` | [verificato: permission-policies, 9/11] |
| Tetto di spesa per sessione | 7/8/2026 | Al tetto la sessione si ferma con `budget_reached` | [verificato: release notes, 9/11] |
| Multiagente e obiettivi (outcome) | 6/5/2026 | Coordinamento fra agenti e obiettivi definiti per la sessione | [verificato: release notes, 9/11] |
| Workflow dinamici | 9/10/2026 | Un programma che fa girare molti agenti a fasi | [verificato: release notes, 9/11] |
| Webhook | 6/5/2026, poi estesi | Avvisi su sessioni, deployment e memoria, senza interrogare l'API | [verificato: release notes, 9/11] |
| Memory store e «dreams» | memoria agganciabile alla sandbox self-hosted dal 19/8; dreams in anteprima limitata | I dreams riordinano la memoria: uniscono doppioni e tolgono voci vecchie | [verificato: release notes; overview, 9/11] |

### 2.3 Piattaforma: novità dopo il 25/10

- **29/10:** Usage and Cost Analytics API (beta). Filtra consumi e costi per chiave API e per utente o service account: con una chiave per agente diventa la banca dei token per agente [verificato: platform release notes, 9/11].
- **2/11:** message threads (beta) [verificato: platform release notes, 9/11].
- **5/11:** allowlist IP dell'organizzazione nella Console (beta). Una chiave rubata non funziona fuori dagli indirizzi ammessi [verificato: platform release notes, 9/11].
- **9/11:** Fable 5.2 [verificato: platform release notes, 9/11].
- Dal 25/10 al 9/11 le note non riportano nessuna funzione nuova di Managed Agents [verificato: platform release notes, 9/11].

### 2.4 Altre offerte ospitate

- **Claude Tag.**
  - Beta pubblica, solo in Slack, piani Team ed Enterprise.
  - Si paga a consumo con un tetto di spesa.
  - Fa lavori programmati e osserva i canali; le sessioni possono girare anche negli ambienti self-hosted.
  - [verificato: claude.com/docs/claude-tag/overview; self-hosted-environments, 9/11]
  - Una versione per Teams esiste solo come voce di stampa [non verificato: winbuzzer.com, 1/7/2026].
- **Claude Duet.** Anteprima solo per Pro e Max (21/10) [verificato: support.claude.com, release notes, 9/11].
- **Crediti API mensili.** Inclusi nei piani Max, Ultra e Team dal 7/10 [verificato: platform release notes, 9/11].
- **Claude apps gateway.**
  - Budget di gruppo condivisi (2.1.316) e report dei costi (2.1.317) [verificato: CHANGELOG, 9/11].
  - L'accesso resta solo con SSO, quindi serve alle persone e non agli agenti [verificato: ricerca/26 §4.4].

## 3. Hermes Agent

### 3.1 Versione

- **Ultima release:** v0.23.0, «The Hearth Release», del 5/11/2026. Prima sono uscite v0.22.6 (2/11) e v0.22.7 (3/11) [verificato: api.github.com/repos/NousResearch/hermes-agent/releases, 9/11].
- **Note di rilascio:** quelle della 0.23 sono complete. Quelle delle patch dicono ancora «undocumented here on purpose» [verificato: stessa fonte, 9/11].
- **Repository:** 262.054 stelle, 58.373 fork, 53.901 issue e PR aperte [verificato: api.github.com/repos/NousResearch/hermes-agent, 9/11].

### 3.2 Problemi di sicurezza e bug di Teams

La scheda #143547 è ancora aperta, aggiornata il 9/11. Conta 312 problemi: 161 rotti, 121 degradati, 9 di sicurezza e 21 estetici. Al 9/11 ne risultano 83 risolti su `main` e 228 senza correzione [verificato: github.com/NousResearch/hermes-agent/issues/143547, 9/11].

| Codice | Stato al 9/11 | Fonte |
|---|---|---|
| MSG-43 | Riprodotto dal vivo sulla v0.22.3; c'è una PR esterna da recuperare (#147977), non unita | [verificato: commento 6365457002 della #143547, 9/11] |
| GW-41 | Non ricontrollato su `main`; PR esterna #141877 da recuperare | [verificato: testo della #143547, 9/11] |
| KB-10 | Solo lettura del codice; PR esterna #141809 da recuperare | [verificato: testo della #143547, 9/11] |
| HR-6 | Riprodotto su `main` (commit bf0203a794) | [verificato: testo della #143547, 9/11] |
| CFG-12 (sicurezza, non tra le quattro di 36 §2.4) | I comandi del terminale ereditano ambiente e chiavi del client che ha avviato il gateway; riprodotto dal vivo sulla v0.22.4 | [verificato: commento 6365457002, 9/11] |
| #113578 (documenti su Teams) | Ancora aperto, ultimo aggiornamento il 2/11 | [verificato: api.github.com, issue 113578, 9/11] |

Nessuno dei quattro codici compare nell'elenco dei problemi risolti [verificato: testo della #143547, 9/11].

### 3.3 Funzioni di autonomia nella v0.23.0

[verificato: note della release v0.23.0, 9/11]

- **Stanze di gruppo.** Un bot capo, oppure lo smistamento `auto`, sceglie chi risponde. I cron possono scrivere in una stanza e svegliano solo i bot menzionati. Ogni stanza ha uno scopo e note condivise.
- **Freno ai giri fra bot.** `max_hops` (default 4) dopo l'ultimo messaggio umano.
- **Cron.** Un lavoro in corso si può fermare. Per i turni persi si sceglie la politica (`--catch-up on|off`).
- **Sottoagenti e bacheca.** I sottoagenti in background sopravvivono allo stop; i lavoratori della bacheca kanban funzionano di nuovo.
- **Skill.** `hermes curator lock` impedisce all'agente di riscrivere una skill curata a mano, anche in modalità YOLO. Le skill di base scendono da 58 a 44.
- **Spesa.** Gli strumenti MCP a pagamento dichiarano il prezzo. C'è un tetto per chat, che chiede conferma anche in YOLO.
- **Eventi.** Gli eventi MCP via webhook (sperimentali) avviano esecuzioni dell'agente.
- **Approvazioni.** Il cancello delle approvazioni intercetta più casi. Un gateway senza persona davanti salta gli hook non approvati invece di bloccarsi.
- **Migrazione.** Dalla v0.22.6 `hermes migrate` porta su Hermes gli utenti di Grok Bot [verificato: note v0.22.6, 9/11].

### 3.4 Le quattro condizioni di ricerca/36 §2.4

1. v0.23 uscita con note complete: **sì** [verificato: §3.1].
2. MSG-43, GW-41, KB-10 e HR-6 chiuse su `main`: **no** [verificato: §3.2].
3. Bug #113578 chiuso: **no** [verificato: §3.2].
4. Un aggiornamento che passa i 10 scenari: **non provato** [non verificato: prova non fatta].

## 4. Grok Bot

- **Prezzi invariati.** Premium 30 $, Super 100 $, Ultra 200 $, Teams da 30 $ a utente, Enterprise su trattativa. L'uso di modelli di terzi si paga a parte [verificato: cursor.com/pricing, 9/11].
- **Routine.**
  - Orari scritti in linguaggio naturale.
  - Eventi da Slack, GitHub, Linear, Sentry, PagerDuty, email e webhook. Il webhook è un `POST` con `Bearer`: la risposta 200 vuol dire «partita», non «finita».
  - Fino a 300 esecuzioni l'ora in totale e 200 per singola routine. Un limite condiviso fra utenti può farle fallire: è un problema noto.
  - Ogni esecuzione e ogni prova consuma uso.
  - [verificato: cursor.com/help/grok-bot/routines, 9/11]
  - Rispetto al 14/10 (ricerca/11 §2.4: 50 routine per Bot e almeno 5 minuti fra due esecuzioni) i limiti pubblicati sono diversi. La pagina non elenca più Microsoft Teams né X fra gli eventi [verificato: confronto con ricerca/11].
- **Dati e controlli.**
  - I computer girano solo negli USA e solo nel cloud di Cursor; niente installazione in casa.
  - La residenza dei dati offerta è solo «US-only».
  - Auto Review giudica shell, chiamate alle app, uso del computer, scritture delle automazioni e deleghe: lascia passare, chiede o nega. Renderla obbligatoria è possibile solo su Enterprise.
  - Registro delle azioni, audit log, controlli di rete e inference hooks sono solo Enterprise.
  - [verificato: docs.x.ai/grok-bot/security, 9/11]
- **Stato del servizio.** status.cursor.com ora rimanda a status.x.ai, che risponde 403 agli strumenti automatici [verificato: 9/11]. Un changelog ufficiale di novembre non l'ho trovato [non verificato: x.ai risponde 403].

## 5. n8n

- **Versioni.** Stable 2.46.7 e beta 2.47.3, entrambe del 9/11. n8n 3.0 (27/10) è una versione maggiore con modifiche incompatibili e uno strumento di migrazione; la 3.1 è del 3/11. Su GitHub le versioni 3.x sono segnate come prerelease [verificato: api.github.com/repos/n8n-io/n8n/releases; docs.n8n.io/release-notes, 9/11].
- **Approvazione umana sugli strumenti dell'AI Agent.**
  - L'agente si ferma e chi revisiona vede nome e parametri dello strumento. Se approva, lo strumento parte; se nega, l'agente riceve il rifiuto.
  - Canali: chat di n8n, Slack, Discord, Telegram, **Microsoft Teams**, Gmail, **Outlook**, WhatsApp Business Cloud, Google Chat.
  - Funziona anche quando un agente fa da strumento per un altro agente.
  - Durata massima dell'attesa e piani richiesti non sono indicati.
  - [verificato: docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools, 9/11]
- **Finestra L2 nativa.** Il nodo Wait, in attesa di un webhook o di un modulo, ha l'opzione «Limit Wait Time»: allo scadere il flusso riprende da solo. Durante l'attesa lo stato è salvato nel database [verificato: docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/, 9/11]. Dalla 2.30 le risposte «Send and Wait» riportano l'ora della risposta (`respondedAt`) [verificato: release notes, 9/11].
- **n8n Agents (anteprima).**
  - Agenti pubblicati su Slack, Telegram, Linear e **Microsoft Teams**, con orari da ogni ora fino a un cron personalizzato.
  - Approvazione degli strumenti sensibili in chat.
  - Self-hosted dalla 2.32.3 (21/7); la queue mode non è supportata; i canali self-hosted vogliono un `WEBHOOK_URL` pubblico.
  - [verificato: docs.n8n.io/build/build-and-manage-agents, 9/11]
  - Budget mensile e tetto di spesa per sessione dalla 2.43 (6/10) [verificato: release notes, 9/11].
  - Se valga anche per la Community Edition non è scritto [non verificato].
- **Microsoft.** Il nodo «Microsoft Agent 365 Trigger» fa agire un flusso come agente Microsoft 365: è in anteprima e richiede il programma Frontier di Microsoft. La 3.1 manda le tracce all'osservabilità di Agent 365 [verificato: release notes 2.7 e 3.1, 9/11].

## 6. Microsoft Copilot Studio e agenti per M365 e Teams

- **Trigger autonomi.**
  - Eventi (SharePoint, OneDrive, Planner, Dataverse) e ricorrenza. Ogni evento arriva all'agente come un messaggio e si paga come tale.
  - Servono l'orchestrazione generativa e **solo le credenziali di chi ha creato l'agente**.
  - L'amministratore può bloccarli.
  - [verificato: learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers-about, aggiornata il 3/11, letta il 9/11]
- **Tariffe in crediti** (pagina datata 30/10).
  - Risposta classica 1 credito, risposta generativa 2, azione dell'agente 5 (trigger, ragionamento profondo, computer use), grounding sul tenant 10, 100 azioni di flusso 13.
  - Con un modello di ragionamento si aggiungono 10 crediti ogni 1.000 token.
  - I flussi chiamati da un agente autonomo pagano crediti anche quando gli utenti hanno licenze Microsoft 365 Copilot.
  - Al 125 % della capacità prepagata gli agenti si bloccano.
  - [verificato: learn.microsoft.com/…/requirements-messages-management, 9/11]
- **Prezzo del credito.** Pacchetto da 25.000 crediti a 200 $ al mese; 0,01 $ a credito a consumo [non verificato: la pagina prezzi di Microsoft è andata in timeout; cifre da un riassunto di ricerca e da siti di terzi].
- **Nuovo «GitHub Copilot harness».** In anteprima pronta per la produzione da giugno 2026, con skill, memoria, MCP e altri agenti; fatturazione a consumo da agosto. Una licenza Microsoft 365 Copilot permette di costruire agenti su questo harness [verificato: learn.microsoft.com/…/whats-new e /billing-licensing, 9/11].
- **Agent 365.**
  - È il piano di governo degli agenti: identità Entra, accesso condizionato, osservabilità.
  - Disponibile dal 1/5/2026 a 15 $ per utente al mese [verificato: techcommunity.microsoft.com, post di un dipendente Microsoft del 9/3/2026, letto il 9/11].
  - Gli agenti di Copilot Studio vi si iscrivono (agosto 2026) e ricevono in automatico un Entra Agent ID (luglio 2026) [verificato: whats-new, 9/11].
- **Dove stanno i dati.**
  - Nella geografia Azure scelta, Regno Unito compreso, con eccezioni per canali come Teams e per i servizi esterni. I dati di attività stanno nella regione della casella Exchange dell'utente [verificato: learn.microsoft.com/…/data-location, 9/11].
  - Alcuni modelli esterni, Claude compreso, possono richiedere un trattamento fuori dalla geografia [verificato: whats-new, marzo 2026].
- **Novità recenti.** La pagina «What's new», aggiornata il 4/11, non elenca funzioni di ottobre né di novembre [verificato: 9/11].

## 7. Altro

- **Buzz.**
  - Nessuna release desktop dopo la v0.5.28 del 9/10.
  - La #7375 è ancora aperta.
  - La PR #8057, che sospende e riprende le approvazioni nei workflow, è aperta e ferma al 26/10.
  - Il repository è attivo (ultimo push il 9/11).
  - [verificato: api.github.com/repos/block/buzz, 9/11]
- **OpenAI.**
  - Agent Builder chiude il 30/11/2026; i sostituti indicati sono l'Agents SDK e i Workspace Agents di ChatGPT. Evals è in sola lettura dal 31/10 e chiude il 30/11 [verificato: developers.openai.com/api/docs/deprecations, 9/11].
  - Dots: nessuna novità ufficiale dopo il 25/10. La versione Pro resta esclusa in UE, Svizzera e Regno Unito; Business Premium è disponibile [non verificato: stampa di ottobre; le pagine OpenAI non le ho aperte].
  - Frontier (piattaforma di agenti per grandi aziende): solo vendita diretta, prezzi non pubblici [non verificato: stampa].
- **Paperclip v2026.1106.0 (6/11).**
  - Il runner nativo è ora il default per i nuovi agenti Claude, Codex, OpenCode e Pi.
  - Un modello fa da difesa contro le prompt injection.
  - Osservabilità via OTLP e un collegamento unico a Google Workspace.
  - Grok Bot e Muse entrano come fornitori sperimentali.
  - L'esperimento Pipelines è stato tolto.
  - Licenza MIT, 112.624 stelle.
  - [verificato: api.github.com/repos/paperclipai/paperclip/releases, 9/11]
- **LiteLLM.** La PR #36736 sull'inoltro degli header beta è stata chiusa senza unione il 2/11. L'ultima versione stabile è la v1.108.3 del 7/11 [verificato: api.github.com/repos/BerriAI/litellm, 9/11]. Se inoltri `safeguards` e `safeguard_results` [non verificato: va provato].
- **Agent Skills.** Il formato è stato donato all'Agentic AI Foundation il 22/10 e lo usano più di 70 piattaforme: aiuta a portare le skill da un motore all'altro [verificato: anthropic.com/news, 9/11].

---

## 8. Cosa cambia per la scelta dell'architettura

La trascrizione di riferimento descrive azioni verso l'esterno a L3:
- il post-call, che scrive al cliente e aggiorna il CRM «in modo totalmente autonomo» [verificato: trascrizione di riferimento, 4:42-5:07];
- il richiamo dei lead entro 90 secondi, 24 ore su 24 [verificato: trascrizione, 14:55-16:02];
- il coaching mandato dopo ogni call [verificato: trascrizione, 14:38-14:46].

Restano fissi tre limiti: niente cancellazioni né credenziali agli agenti, niente pagamenti automatici, stop d'emergenza sempre disponibile. Dentro questi limiti, l'architettura deve dare L3 a classi intere di azioni, non solo approvare una carta alla volta.

### 8.1 Chi offre quale livello oggi

| Opzione | L1 carta | L2 finestra | L3 dentro regole | Dove girano ciclo e dati |
|---|---|---|---|---|
| Motore sull'Agent SDK + Cancello | `defer` e carte, già native (§1.2) | da costruire, con un timer nel Cancello o con n8n | modalità auto, hook che bloccano se falliscono, regole deny, tetti (§1.3) | server SerSan; modelli via API |
| Managed Agents | `always_ask` (§2.2) | non nativa | policy `auto` o `always_allow`, budget, cron al minuto (§2.2) | ciclo e trascrizioni da Anthropic negli USA; sandbox anche in casa |
| Compiti programmati Claude Code | domande dentro la sessione | non nativa | auto di default, ma agiscono «come te» (§1.4) | cloud Anthropic o runner nostro; contenuto comunque ad Anthropic (§1.5) |
| n8n (flussi e Agents) | approvazioni in Teams e Outlook (§5) | **nativa**: Wait con limite di tempo (§5) | flussi diretti; Agents con budget | server SerSan |
| Hermes v0.23 | shell [ricerca/10 §4.2], MCP non fidati, spese (§3.3) | non trovata [non verificato] | YOLO, cron, stanze che si smistano da sole (§3.3) | server SerSan |
| Grok Bot | Allow once / Always / Deny; scade dopo circa 10 minuti senza persona [ricerca/11 §2.6] | non trovata [non verificato] | Auto Review, routine (§4) | cloud USA |
| Copilot Studio | raccolta di informazioni via Outlook, in anteprima [verificato: whats-new, novembre 2025] | non trovata [non verificato] | trigger con le credenziali di chi ha creato l'agente (§6) | M365, geografia Regno Unito |
| Buzz | approvazioni non collegate (§7) | no | sì, ma senza freni [ricerca/17 §0] | server SerSan |

### 8.2 Cosa cambia

1. **La base resta il motore sull'Agent SDK, e per l'autonomia ora è più forte.** Fra le opzioni compatibili con il board è l'unica che unisce due cose:
   - un giudice per ogni azione (la modalità auto), usabile con la chiave API;
   - blocchi deterministici che non dipendono dal modello: hook che bloccano se falliscono, deny, scritture solo nelle cartelle di lavoro, tetti di spesa.

   Hermes ha un modello giudice solo per i comandi di shell [verificato: §1.3, ricerca/10 §4.2; giudizio: proposta].
2. **Il Cancello passa dalla «carta per ogni azione» al «livello per classe d'azione».** Le classi d'azione e le regole «Sempre» di ricerca/36 §5.8 diventano la corsia L3; si aggiunge una corsia L2. Livelli iniziali proposti per avvicinarsi alla trascrizione [proposta]:
   - **L3:** azioni interne e reversibili (note, compiti, bozze, CRM interno, canale interno).
   - **L2, con finestra di 15-60 minuti:** messaggi esterni da modello verso destinatari già noti (follow-up dopo la call, recap al cliente).
   - **L1:** destinatari nuovi, importi, impegni contrattuali.
   - **L0:** tutto ciò che tocca credenziali o cancellazioni; i pagamenti non sono mai automatici.
   - Il richiamo entro 90 secondi può stare solo a L3, dentro regole strette (consenso, orari, tetti): nessuna finestra entra in 90 secondi.
3. **La finestra L2 si fa con n8n senza codice nuovo.** Il nodo Wait con limite di tempo porta in Teams la carta con il tasto «Ferma» e riprende da solo allo scadere; `respondedAt` registra chi ha risposto e quando. Il Cancello resta l'unico esecutore [verificato: §5; proposta].
4. **La modalità auto va usata per le azioni interne dei profili, non come cancello verso l'esterno.** Serve che valgano tre condizioni:
   - LiteLLM deve inoltrare `anthropic-beta`, `safeguards` e `safeguard_results`; altrimenti si pagano le richieste al classificatore locale, oppure, dalla 2.1.319, le azioni vengono negate (§1.3, §7);
   - gli strumenti del Cancello portano `destructiveHint: true`;
   - gli hook usano `onFailure: "block"`.

   Anthropic può spegnere auto lato server, quindi il sistema deve ricadere su L1 senza fermarsi [verificato: §1.2-1.3; proposta].
5. **Orari e ingressi restano a n8n.** I compiti programmati di Claude Code servono solo per le routine personali delle persone sui posti Team: agiscono come la persona, partono al massimo una volta l'ora e sono in anteprima. Possono girare sul DL380 con i runner self-hosted, ma il contenuto va comunque ad Anthropic [verificato: §1.4-1.5; proposta].
6. **Se un pezzo non sta sul server, Managed Agents è l'abbonamento più autonomo fra le offerte Claude ospitate.** Ha cron, policy auto, budget, webhook, multiagente e memoria. Il runtime costa poco (0,08 $ l'ora) e la sandbox può stare in casa. Ciclo e trascrizioni però restano da Anthropic negli USA, senza ZDR: quindi solo dati verdi e gialli, e le azioni esterne passano comunque dal Cancello via MCP [verificato: §2; proposta].
7. **Microsoft.** Copilot Studio porta trigger nativi in M365 con i dati nel Regno Unito. In cambio usa le credenziali di chi ha creato l'agente e si paga a crediti, anche quando l'agente parte da solo. Conviene solo per eventi M365 che n8n non vede bene. Agent 365 è governo degli agenti, non un motore [verificato: §6; proposta].
8. **Hermes.** Le funzioni nuove sono proprio quelle dell'autonomia di squadra: stanze che si smistano da sole, `max_hops`, cron nelle stanze, skill bloccabili, politica per i turni persi, tetti di spesa. Conviene copiarle nella nostra bacheca e nel canale «Agenti». Le condizioni di 36 §2.4 però non sono soddisfatte, quindi per quella regola Hermes resta al pilota in LAB [verificato: §3; proposta].
9. **Grok Bot, Dots e Claude Tag** sono le autonomie «pronte» più ampie. Stanno però fuori dal server, con dati negli USA (Grok Bot, Dots) o solo in Slack (Claude Tag), e i controlli più forti di Grok Bot sono solo Enterprise. Valgono come piloti su dati non sensibili, alla pari. **Paperclip** migliora e pilota Claude, Codex, Grok Bot e Muse: resta da provare come piano di controllo (organigramma, budget) sopra i nostri agenti [verificato: §2.4, §4, §7; proposta].
10. **Buzz e OpenAI Agent Builder oggi non aggiungono autonomia utilizzabile.** Buzz non ha approvazioni collegate e non rilascia da un mese; Agent Builder chiude il 30/11 [verificato: §7].

### 8.3 Prove da fare per prime [proposta]

1. Una sessione SDK con `permissionMode: "auto"` dietro LiteLLM. Si guarda se `/status` mostra «Auto mode server: Enabled»; se no, si misura il costo del classificatore locale.
2. Gli hook del Cancello con `onFailure: "block"` e gli strumenti con `destructiveHint: true`. Si fa andare in errore la callback e si controlla che l'azione resti bloccata.
3. Il follow-up dopo la call a L2: finestra di 30 minuti con n8n Wait e carta in Teams. Si conta quante volte qualcuno lo ferma.
4. Facoltativa: un agente Managed Agents per i brief pre-meeting, con la sandbox sul server, dati verdi, cron e tetto di spesa, per confrontarne autonomia e costo con il motore.
