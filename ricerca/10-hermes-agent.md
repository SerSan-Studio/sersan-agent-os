# Hermes Agent (Nous Research) allo stato del 24 ottobre 2026

Scheda per decidere se Hermes Agent può fare da orchestratore degli agenti di SerSan sul server di casa (Linux, GPU da 8 GB, 160 GB di RAM), con Claude come modello principale.

> **Aggiornamento del 25/10/2026.** Lo stato di oggi e la valutazione dentro il board dell'infrastruttura di Michele sono in `27-hermes-self-hosted.md`. Tre correzioni a questa scheda:
> - il bug #58032 è chiuso dal 7/7/2026, ma l'opzione `multiplex_profiles: false` è stata ritirata con la v0.22.0 [verificato: issue #58032; docs multi-profile-gateways];
> - il bug #141623 è chiuso dal 20/10/2026 [verificato: GitHub API];
> - i problemi aperti del gateway unico sono 273, di cui 9 di sicurezza (issue #143547) [verificato: GitHub, 25/10/2026].

**Come leggere le etichette.**
- **[verificato: fonte]**: il fatto l'ho letto io su una pagina ufficiale, sul repository o in un file locale, e la fonte è indicata.
- **[verificato: clone 1/10]**: il fatto viene dal clone locale del repository (HEAD `4e74031`, 1° ottobre 2026). Questi fatti hanno tre settimane e il progetto cambia ogni giorno: vanno ricontrollati sulla versione che si installa.
- **[non verificato]**: lo dicono terzi (articoli, blog, video) oppure è una mia stima, e lo dico.

Rilevazioni web fatte il 24 ottobre 2026.

---

## 1. In breve

1. **Hermes Agent è l'orchestratore scelto per la visione.** È il progetto di Nous Research: open source, si installa su una macchina propria, funziona con Claude e OpenAI, si dichiara "self-improving", e i suoi agenti si parlano tra loro.
2. **Il progetto è molto vivo e molto grande, quindi instabile.**
   - Sul repository: 256.800 stelle, 56.200 fork, 58.403 commit su `main`, più di 5.000 issue aperte e più di 5.000 PR aperte [verificato: github.com/NousResearch/hermes-agent, 24/10/2026].
   - Ultima release: v0.22.5 del 22-23 ottobre. In dieci giorni sono uscite cinque patch (v0.22.1 il 14/10, v0.22.2 il 15/10, v0.22.3 e v0.22.4 il 21/10) [verificato: pagina Releases].
   - Licenza MIT [verificato: repo e `LICENSE`].
3. **La raccolta da 90 milioni c'è stata.**
   - Annuncio: 7 ottobre 2026, 90 milioni di dollari [verificato: TNW, 7/10/2026, che riprende il Wall Street Journal].
   - Investitori nominati da TNW: NVIDIA, M12 (Microsoft), Samsung, Robot Ventures, Union Square Ventures, Y Combinator, Menlo Ventures.
   - Valutazione di 1,5 miliardi: la riporta il WSJ, Nous non l'ha comunicata [verificato: TNW].
   - Il round è una Series B guidata da Robot Ventures [non verificato: FourWeekMBA e altri, che citano TechCrunch].
   - I soldi vanno a "Hermes for Businesses".
   - Il video di ottobre che cita i 90 milioni è il notiziario settimanale di agentnative.inc [verificato: trascrizione del notiziario, non pubblicata in questa repo].
4. **Un'app iOS ufficiale per ora non esiste.**
   - Il video dice che "they're going to be releasing an iOS app" [verificato: trascrizione 03].
   - Secondo un articolo, l'annuncio su X conferma un'app mobile in arrivo, senza data [non verificato].
   - Le richieste per un'app ufficiale sono ancora aperte su GitHub (issue #11911, #50745). Le app iOS esistenti sono di terzi e si dichiarano non affiliate a Nous [non verificato: bitdoze, repo `dylan-buck/Hermes-iOS`].
5. **Con Claude, la via pulita è la chiave API Anthropic.**
   - La documentazione di Hermes dice che il login OAuth Anthropic "only works if you're on a Claude Max plan and have purchased extra usage credits". Il piano Pro è escluso [verificato: docs/integrations/providers].
   - Anthropic scrive che l'OAuth dei piani è pensato per Claude Code e per le app native, e che chi costruisce prodotti deve usare le chiavi API [verificato: code.claude.com/docs/en/legal-and-compliance].
   - Per SerSan: il motore di Hermes va sugli 800 $/mese di crediti API, non sui 5 account Team.
6. **Per un'azienda di 4 persone va bene come orchestratore di agenti sul server. Non va bene come "secondo cervello" né come confine di sicurezza.**
   - La memoria interna è piccola: due file da 2.200 e 1.375 caratteri, più la ricerca nelle sessioni passate.
   - Si dichiara "a single-tenant personal agent". Dentro un canale "all callers are equally trusted" [verificato: SECURITY.md su `main`, 24/10/2026].
   - La community segnala bug proprio nei setup con più profili su un solo gateway, cioè sessioni e contesti che finiscono al profilo sbagliato (§6).

---

## 2. Che cos'è

| Aspetto | Fatto | Fonte |
|---|---|---|
| Definizione | "The self-improving AI agent built by Nous Research"; About: "The agent that grows with you" | [verificato: README su GitHub, 24/10] |
| Architettura | Un ciclo di agente proprio in Python, una classe `AIAgent` che serve riga di comando, gateway di messaggistica, app desktop, API; chiama i modelli in tre formati (OpenAI, Responses, Anthropic) | [verificato: clone 1/10, `wd/developer-guide/architecture.md:263`, `agent-loop.md:41-79`] |
| Linguaggio | Python 3.14 per le installazioni ufficiali (`pyproject` ammette >=3.11,<3.15); app desktop Electron/TypeScript | [verificato: docs installation; clone `pyproject.toml:15`] |
| Licenza | MIT, "Copyright (c) 2025 Nous Research"; eccezioni: `plugins/security-guidance` Apache-2.0, extra `piper-tts` GPL | [verificato: clone `LICENSE`] |
| Primo rilascio pubblico | "February" sotto MIT (TNW); il copyright del file di licenza dice 2025 | [verificato: TNW 7/10; clone `LICENSE`]. Data esatta del primo commit: non trovata |
| Diffusione dichiarata | "cloned over 24 million times"; ~2,5% dei token mondiali | [non verificato: stime di Nous riportate da TNW] |
| Segnali recenti | Demo di Hermes nel keynote di Jensen Huang al GTC Berlin (21/10); plugin ufficiale Meshy (22/10); plugin "Spaces" di trycua (22/10) | [verificato: post X elencati su nousresearch.com, 24/10] |

---

## 3. Maturità

| Indicatore | Valore | Fonte |
|---|---|---|
| Stelle / fork | 256,8k / 56,2k | [verificato: GitHub 24/10] |
| Commit su main | 58.403 | [verificato: GitHub 24/10] |
| Issue / PR aperte | 5k+ / 5k+ | [verificato: GitHub 24/10] |
| Ultima release | v0.22.5 (note datate 22/10/2026), patch con ~81 PR; "many changes are undocumented here on purpose", note complete con v0.23.0 | [verificato: pagina Releases] |
| Ritmo | 5 release in 10 giorni (14, 15, 21, 21, 22-23 ottobre) | [verificato: pagina Releases] |
| Test | 5.711 file sotto `tests/` | [verificato: clone 1/10] |
| Documentazione indietro rispetto al codice | Esempio: il tetto di giri del sottoagente è 250 nel codice, 50 nella doc | [verificato: clone 1/10] |
| Vulnerabilità 2026 | Più CVE nel 2026, tra cui path traversal sul webhook del gateway (CVE-2026-14628, versioni fino a 2026.5.16, sfruttabile da remoto senza autenticazione secondo SentinelOne), autorizzazione dei webhook (CVE-2026-114463, corretta in v0.22.2), sandbox di `execute_code` (CVE-2026-9368, corretta in 0.11.0); nota CSA "9 CVEs in 4 Days" (maggio 2026) | [non verificato: SentinelOne, VulDB, GitHub Advisory, CSA; gravità diverse tra i database] |

**Giudizio.** Le funzioni sono mature e molto ampie. Il software è fragile per due motivi: il ritmo di cambiamento e le parti appena rifatte, come il gateway unificato con più profili. Per SerSan conviene fissare una versione e aggiornare con cadenza controllata, non inseguire ogni patch [stima, non verificato].

---

## 4. Cosa fa (le funzioni che servono alla visione)

### 4.1 Agenti multipli che si parlano e si delegano lavoro

| Meccanismo | Cosa fa | Funziona su server Linux senza desktop? | Fonte |
|---|---|---|---|
| **Profili** | Agenti con nome, ognuno con modello, persona (`SOUL.md`), memoria, skill, connettori, canali e cron propri | Sì (`hermes -p <nome>`) | [verificato: clone 1/10, `wdu/profiles.md:11`] |
| **`delegate_task`** | Sottoagenti con contesto vuoto, 10 in parallelo di default, risultato in background durevole, schema JSON di uscita, modello diverso per i figli | Sì | [verificato: clone 1/10, `tools/delegate_tool.py`]; v0.22.5 aggiunge "pluggable delegation backends" per modello o profilo [verificato: Releases] |
| **Kanban** | Bacheca SQLite durevole tra profili: stati, dipendenze, dispatcher che lancia un processo per card, decomposer che spezza una frase in 2-6 card, corsia di revisione, blocco "serve un umano" sbloccabile dal telefono | Sì | [verificato: clone 1/10, `wdf/kanban.md`, `kanban_db_dispatch.py`] |
| **Bot Mode** | Ogni profilo diventa un "Bot" con chat permanente; chat di gruppo da 2-6 Bot (al massimo 3 giri, 10 messaggi per invio); messaggi diretti tra agenti con `message_agent` | **In parte.** È un'interfaccia dell'app desktop. Su un server senza schermo i Bot si scrivono sul canale di messaggistica, ma `message_agent` resta nascosto finché non si impostano a mano due marcatori ("Bot Chat" e `ui_meta: hermes-bots`): "no CLI command writes the marker" | [verificato: docs/user-guide/bot-mode, 24/10] |
| **`hermes peer`** | Gateway su macchine diverse che si parlano senza il desktop in mezzo; un gateway dietro NAT può chiamare fuori ma non ricevere | Sì | [verificato: docs bot-mode] |
| **Slack multi-agente** | Più istanze o bot nello stesso canale; `allow_bots: "mentions"` consigliato, `"all"` può creare loop | Sì | [verificato: docs/user-guide/messaging/slack] |
| **A2A, Mixture of Agents** | Chiamare e farsi chiamare da agenti di altri framework; più modelli consultati e uno che decide | Sì | [verificato: clone 1/10] |
| **Lavoratori esterni** | Skill per pilotare Claude Code/Codex da terminale; contratto per far lavorare una card a una CLI esterna | Sì, ma il contratto era solo un abbozzo il 1/10 | [verificato: clone 1/10] |

### 4.2 Canali, routine, memoria, strumenti

| Area | Fatto | Fonte |
|---|---|---|
| Canali | Un gateway, molti canali: Telegram, Discord, Slack, WhatsApp, Signal, email, SMS, Matrix, Mattermost, Teams, Google Chat e altri (22 plugin di piattaforma) | [verificato: clone 1/10] |
| Slack | Solo Socket Mode, quindi niente URL pubblico; risponde in thread se menzionato; sessione per utente di default; bottoni di approvazione; il bot va invitato a mano nei canali | [verificato: docs Slack, 24/10] |
| Web/API | Hermes stesso si espone come API compatibile OpenAI (`/v1/chat/completions`, `/v1/responses`, `/v1/runs`) e le conversazioni come server MCP | [verificato: clone 1/10] |
| Cron/routine | Pianificazioni in linguaggio naturale; consegna su chat, canale o nella chat di un altro agente; job senza modello; sorveglianze che svegliano il modello solo se qualcosa cambia; stato "consegnato" separato da "eseguito"; routine per Bot | [verificato: clone 1/10; docs bot-mode] |
| Webhook | In ingresso con firma HMAC e strumenti ridotti di default; in uscita firmati | [verificato: clone 1/10] |
| Memoria | `MEMORY.md` (2.200 caratteri) e `USER.md` (1.375) sempre nel prompt; revisione dopo il turno che salva ricordi e skill; ricerca a testo pieno nelle sessioni; un provider esterno alla volta (Honcho, Mem0, Supermemory e altri); scritture in coda di approvazione se si vuole | [verificato: clone 1/10] |
| Skill | 58 incluse e 152 opzionali in formato `SKILL.md` (lo stesso di Claude Code); l'agente scrive e cura le proprie skill; registri esterni con scansione | [verificato: clone 1/10] |
| MCP | Client stdio e HTTP con OAuth; catalogo di 65 server approvati; caricamento degli schemi solo su richiesta | [verificato: clone 1/10] |
| Browser e computer | Strumenti browser (installabili o no: `--skip-browser`); computer use; "Bot Screen" che vuole un host Linux | [verificato: docs installation; clone 1/10, `wdf/bot-screen.md:46-47`] |
| Sandbox | Terminale in Docker con capacità tolte, sandbox cloud, segreti fuori dal sandbox (proxy in uscita spento di default) | [verificato: clone 1/10] |
| Voce | Voce nel terminale e nell'app, wake word, note vocali su Telegram/Discord, Google Meet (Linux/macOS) | [verificato: clone 1/10] |
| Telefono | Skill per SMS e chiamate **in uscita** (Bland.ai, Vapi); **niente chiamate in arrivo in tempo reale** | [verificato: clone 1/10] |
| Osservabilità e costi | `/usage`, `/insights` (token e costo per modello e canale), Langfuse, OpenTelemetry, rotazione chiavi, fornitore di riserva | [verificato: clone 1/10] |
| Sicurezza | Approvazione solo per i **comandi di shell pericolosi** (manuale, "smart" con modello giudice, off); senza umano, negato; `send_message` non è dato al modello; abbinamento con codice per chi può parlare all'agente; arresto d'emergenza `hermes pause` | [verificato: clone 1/10] |

### 4.3 Modelli: Claude, abbonamenti, locali

| Via | Come | Stato | Fonte |
|---|---|---|---|
| **API Anthropic** | `ANTHROPIC_API_KEY`, `--provider anthropic`, pagamento a token | Ufficiale e documentata | [verificato: docs providers, 24/10] |
| OAuth Claude | "only works if you're on a Claude Max plan and have purchased extra usage credits"; "Claude Pro subscribers cannot use this path"; tutto viene addebitato come uso extra anche se l'allowance del piano non è finita | Non adatta ai piani Team di SerSan (i piani Team non sono nominati) | [verificato: docs providers] |
| Claude Code come fornitore | Plugin "claude-subscription-directsdk": i turni passano dalla CLI di Claude Code, con il costo sull'abbonamento; v0.22.5 ne corregge le risposte lunghe tagliate | Esiste. La conformità alle regole di Anthropic è da valutare (§6) | [verificato: clone 1/10; Releases v0.22.5] |
| Codex/ChatGPT | Login con device code; quali piani valgano "not currently documented" | Documentata in parte | [verificato: docs providers] |
| **Ollama** | `http://localhost:11434/v1`; contesto di default 4.096 token sotto i 24 GB di VRAM, da alzare a mano | Supportato | [verificato: docs providers] |
| **vLLM** | `http://localhost:8000/v1`, serve `--enable-auto-tool-choice` e `--tool-call-parser` | Supportato | [verificato: docs providers] |
| llama.cpp, LM Studio, endpoint OpenAI-compatibili | Supportati; per llama.cpp serve `--jinja` per gli strumenti | Supportato | [verificato: docs providers] |
| **Vincolo chiave** | Hermes "requires at least 64,000 tokens of context for agent use with tools"; sotto, rifiuta l'avvio | Vincola i modelli locali piccoli | [verificato: docs providers] |
| Modelli per compito | Modello per canale, per job cron, per card, per sottoagenti e per compiti ausiliari (visione, riassunti) | Supportato | [verificato: clone 1/10] |

---

## 5. Cosa non fa (o fa male) per il caso SerSan

| Limite | Conseguenza per SerSan | Fonte |
|---|---|---|
| È "a single-tenant personal agent"; dentro un canale tutti gli autorizzati hanno la stessa fiducia; per separare i permessi servono istanze separate | Con 4 persone fidate va bene. I permessi diversi per persona (es. Mattia senza accesso ai dati finanziari) non esistono: servono profili o istanze separate | [verificato: SECURITY.md su main, 24/10] |
| "The only security boundary against an adversarial LLM is the operating system"; approvazioni e scanner sono euristiche | Hermes va chiuso in un container o in una VM con permessi minimi | [verificato: SECURITY.md su main] |
| Memoria interna piccola, nessun database relazionale o vettoriale aziendale incluso | Il "secondo cervello" (Notion e database vettoriale) va costruito fuori e collegato via MCP o skill | [verificato: clone 1/10] |
| Le approvazioni nel codice coprono solo i comandi di shell; mail, post e chiamate dipendono da regole scritte nel prompt delle skill | Gli invii verso clienti devono passare da SersanOutreach, che ha già l'approvazione umana, e non da strumenti di invio dati a Hermes | [verificato: clone 1/10] |
| Niente chiamate vocali in arrivo; telefono solo in uscita via Bland/Vapi | L'agente vocale "Andrea" (richiamata entro 90 s) non lo fa Hermes: serve una piattaforma vocale (es. ElevenLabs Agents) che Hermes al massimo pilota | [verificato: clone 1/10] |
| Bot Mode è un'interfaccia desktop; il pacchetto desktop per Linux è disattivato; il desktop macOS è "Apple Silicon only" | Sul server gira il gateway senza interfaccia; il team usa Slack o l'app desktop su Mac/Windows collegata al backend remoto | [verificato: docs installation; clone 1/10, `platform-support.md:48`, `wdu/desktop.md:450-540`] |
| Nessun CRM incluso | Il CRM resta SersanOutreach, oppure HubSpot via MCP o API | [non trovato nelle fonti lette] |
| Nessuna app iOS ufficiale | Telefono via Slack, Telegram o WhatsApp | [non verificato: §1 punto 4] |
| Nessun requisito hardware pubblicato | Va dimensionato da noi (§7) | [verificato: docs installation, "no minimums"] |

---

## 6. Rischi e problemi riportati

| Rischio | Dettaglio | Fonte |
|---|---|---|
| **Contesti che si mescolano tra profili/bot** | Disattivando `multiplex_profiles` restano sessioni orfane: il gateway continua a mandare messaggi al profilo sbagliato, che può usare il prompt di sistema sbagliato (#58032). Dopo la migrazione al gateway unico (v0.22.4) la ripresa delle sessioni dal desktop si rompe (#143150). Non si riesce a cancellare un bot secondario (#141623). C'è una issue di tracciamento per i problemi aperti del gateway unificato (#143547) | [verificato come esistenza delle issue tramite ricerca, 24/10; contenuto riassunto dal motore di ricerca, non letto pagina per pagina] |
| Instabilità e aggiornamenti | Cinque patch in dieci giorni; note di rilascio volutamente incomplete; documentazione indietro rispetto al codice | [verificato: Releases; clone 1/10] |
| Setup | Python 3.14 imposto dall'installer; su Linux minimali manca `libatomic`; Chromium vuole librerie di sistema; i servizi systemd partono con un PATH minimo | [verificato: docs installation]; il PATH [non verificato: blog di terzi] |
| WSL2 e database condiviso | Gateway che esce ogni due minuti su WSL2; conflitti SQLite quando più gateway di profilo scrivono sullo stesso database | [non verificato: blog di terzi, betterclaw.io] |
| Superficie esposta | Più CVE nel 2026 su webhook e adattatori del gateway | [non verificato: §3] |
| Termini Anthropic | L'OAuth dei piani (Free, Pro, Max, Team, Enterprise) è "intended exclusively for … ordinary use of Claude Code and other native Anthropic applications"; chi costruisce prodotti o usa l'Agent SDK deve usare chiavi API; i limiti dei piani presumono "ordinary, individual usage" | [verificato: code.claude.com legal-and-compliance]. Usare i 5 account Team come motore di Hermes 24/7 (plugin DirectSDK o `claude -p` a ciclo continuo) è una zona grigia: va usata la chiave API |
| Cambio di modello di business | Nous spinge ora i servizi a pagamento (Hermes for Business, Cloud, Portal); il nucleo resta MIT | [verificato: portal.nousresearch.com/business; TNW] |
| Sicurezza dei dati | Una bacheca e dei canali dove 25+ agenti leggono mail e trascrizioni sono un bersaglio di prompt injection; Hermes stesso dice che il contenimento è il sistema operativo | [verificato: SECURITY.md] |

---

## 7. Hardware e GPU

| Domanda | Risposta | Fonte |
|---|---|---|
| Requisiti minimi ufficiali | Non pubblicati: "no minimums or recommendations" | [verificato: docs installation] |
| Sistema | Linux x86_64/aarch64 con glibc e systemd, "We test on the latest Ubuntu" | [verificato: clone 1/10, `platform-support.md:21`] |
| Servizio | `hermes gateway install` (servizio utente) oppure `sudo hermes gateway install --system` (servizio di sistema all'avvio); watchdog systemd opzionale | [verificato: clone 1/10, `messaging/index.md:174-232,593-606`] |
| Container | `Dockerfile` e `docker-compose.yml` nel repo; layout ufficiale `/opt/hermes` e `/opt/data` | [verificato: clone 1/10; docs installation] |
| GPU | Hermes non la usa. Serve solo ai modelli locali ("ensure you have enough GPU VRAM") e a STT locale (faster-whisper) | [verificato: clone 1/10, `reference/faq.md:543`; docs Slack per faster-whisper] |
| Il server SerSan basta? | Per Hermes con Claude via API sì, largamente: il carico è CPU, SQLite e rete. La Quadro RTX 4000 da 8 GB non regge un modello locale con 64k di contesto e strumenti a buona velocità: il contesto di Ollama sotto i 24 GB di VRAM parte da 4.096 token e la cache KV di 64k su un modello 7-8B occupa molta memoria. Con i 160 GB di RAM DDR4-2133 si può scaricare sulla CPU, ma lentamente. Ruolo realistico della GPU: trascrizione Whisper, embedding per il database vettoriale, classificazioni brevi | Stima mia [non verificato]; il vincolo dei 64k e il default di Ollama sono [verificato: docs providers] |

---

## 8. Costo

| Voce | Costo | Fonte |
|---|---|---|
| Hermes Agent (software) | 0 €, MIT, self-hosted | [verificato: repo] |
| Modello principale Claude via API | A consumo, dentro gli 800 $/mese di crediti API Anthropic che SerSan ha già | [dato SerSan dal contesto del compito] |
| Nous Portal (facoltativo: modelli Nous, ricerca web, browser e immagini con un solo abbonamento) | Free 0 $; Plus 20 $/mese (22 $ di crediti); Super 100 $ (110 $); Ultra 200 $ (220 $). Sono crediti a consumo, non una tariffa fissa | [non verificato: siti di terzi; la pagina ufficiale ha risposto HTTP 429] |
| Hermes Cloud (istanza ospitata) | Addebito giornaliero dal credito Nous, uptime al secondo più lo storage; da fermo solo storage; minimo 2 $ di credito; 14 regioni, Londra compresa; inferenza e strumenti a parte. Taglie e prezzi non mostrati sulla pagina | [verificato: portal.nousresearch.com/cloud, 24/10] |
| | Small circa 0,32 $/giorno, Medium circa 0,56-0,59 $/giorno | [non verificato: terzi] |
| Hermes for Business (Team) | Saldo unico, tetti di spesa per membro, skill condivise, "Team Gateway" per Slack, Telegram, Discord e WhatsApp, tenant isolato **su infrastruttura Nous**, chiavi proprie dei fornitori ammesse. **Prezzi non pubblicati** | [verificato: portal.nousresearch.com/business, 24/10] |
| Enterprise | On-prem o cloud privato, SSO, SLA, onboarding: "Contact us" | [verificato: portal.nousresearch.com/business] |
| Server SerSan | Già acquistato; corrente e manutenzione non stimate | — |

**Lettura per SerSan.** La configurazione naturale non costa niente in licenze: Hermes self-hosted più chiave API Anthropic. Un abbonamento Nous serve solo se si vogliono gli strumenti ospitati di Nous (ricerca, browser cloud) invece di fornitori propri. Hermes for Business sposterebbe i dati sull'infrastruttura di Nous, in contrasto con la scelta del server di casa. Ha senso solo se il self-hosting si rivela troppo fragile, e il prezzo va chiesto.

---

## 9. Come si collocherebbe sul server SerSan

**Dove gira.**
- Una VM o un container Linux (Ubuntu) dedicato sul DL380, dietro il firewall del mini PC.
- Hermes gira come servizio di sistema (`sudo hermes gateway install --system`), con un utente dedicato e il processo intero chiuso nel container, come SECURITY.md chiede per i "shared deployments" [verificato: SECURITY.md §2.2].
- La versione resta fissata e si aggiorna con cadenza controllata [stima].

| Pezzo della visione | Ruolo di Hermes | Cosa resta fuori da Hermes |
|---|---|---|
| Orchestratore e 25+ agenti | **Profili**, uno per ruolo (raccolta, pulizia, indicizzazione, post-call, debrief, offerte, coaching vendite…), ognuno con modello e skill propri | — |
| Chat condivisa tra agenti (A7) | Canale Slack `#agenti` con i profili e `allow_bots: "mentions"`, più la **bacheca kanban** come registro durevole dei compiti e dei passaggi di mano; blocco "serve un umano" per le decisioni | La bacheca è l'unico registro affidabile dei compiti. La chat su Slack fa da vetrina, perché con `"all"` si rischiano loop [verificato: docs Slack] |
| Post-call (Fireflies → Slack, CRM, mail, to-do) | Webhook HMAC in ingresso che avvia il profilo post-call; consegna su Slack; chiamata alle API di SersanOutreach per opportunità e bozza della mail | L'invio della mail e l'opportunità passano da SersanOutreach con l'approvazione umana. Il webhook va esposto su internet (porta o tunnel): è la parte con più CVE storiche, va protetta |
| Debrief del mattino, brief pre-meeting | Cron in linguaggio naturale per profilo, consegna su Slack o DM | Dati: Gmail, Calendar, LinkedIn via MCP o API |
| Secondo cervello (Notion più vettoriale) | Legge e scrive tramite MCP (Notion) e una skill o un MCP per il database vettoriale | Il database vettoriale (es. pgvector o Supabase) e la pipeline di indicizzazione sono componenti separati |
| CRM fatto in casa | Hermes lo usa via API o MCP | Il CRM è SersanOutreach |
| Agente vocale "Andrea" | Al massimo prepara il contesto e riceve l'esito | Chiamate in uscita entro 90 s e 24/7: ElevenLabs Agents o equivalente, fuori da Hermes |
| Token policy e banca dei token | Modello per profilo, canale, card e job; `/insights` e Langfuse per token e costo; più chiavi e fornitore di riserva | Il budget per persona e il premio mensile sono processi interni |
| Modelli | Claude via API come principale (Opus o Sonnet per i ragionamenti, un modello più economico per i compiti ausiliari); modelli locali sulla GPU solo dove bastano | — |

**Cosa rende Hermes adatto.**
- Il gateway multi-canale, il cron, la bacheca kanban e i profili sono già pronti e sono esattamente i pezzi che la visione descrive.
- È MIT e self-hosted.
- Si collega a Slack senza URL pubblico.
- Parla MCP e usa lo stesso formato di skill di Claude Code.

**Cosa lo rende rischioso come fondamenta.**
- Il modello di fiducia è per un singolo utente.
- Ha bug aperti proprio sui setup con più profili.
- Cambia molto in fretta.
- Le approvazioni nel codice coprono solo la shell.

Il primo test dovrebbe essere piccolo e misurabile: 3 profili (post-call, debrief, raccolta), un canale Slack, la bacheca kanban, chiave API Anthropic, nessun invio diretto verso clienti. Si guarda per due settimane se le sessioni restano separate e se gli aggiornamenti rompono qualcosa [proposta, non verificato].

---

## 10. Domande aperte

1. Prezzi di Hermes for Business (Team) e taglie di Hermes Cloud: le pagine ufficiali non li mostrano, e quella dei piani ha risposto 429.
2. Annuncio ufficiale di Nous del 7 ottobre (testo e lead investor): non letto, perché non trovato tra gli ultimi post visibili su nousresearch.com.
3. Data e forma dell'app iOS ufficiale: nessuna fonte ufficiale trovata.
4. Stato attuale delle issue #58032, #143150, #141623, #143547 sulla v0.22.5: non controllato pagina per pagina.
5. Il connettore MCP per HubSpot o per SersanOutreach esiste nel catalogo dei 65? Non verificato.
6. Uso dei 5 account Claude Team per lavoratori `claude -p` lanciati da Hermes: conforme ai termini commerciali Team? Da chiarire con Anthropic. La pagina invita a "contact sales" per i casi dubbi.

---

## Fonti

- Repository: https://github.com/NousResearch/hermes-agent (24/10/2026); release: https://github.com/NousResearch/hermes-agent/releases; SECURITY.md: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/SECURITY.md
- Docs ufficiali: https://hermes-agent.nousresearch.com/docs/integrations/providers ; .../docs/user-guide/bot-mode ; .../docs/getting-started/installation ; .../docs/user-guide/messaging/slack
- Nous: https://nousresearch.com/ ; https://portal.nousresearch.com/business ; https://portal.nousresearch.com/cloud
- Anthropic: https://code.claude.com/docs/en/legal-and-compliance
- Raccolta: https://thenextweb.com/news/nous-research-90m-1-5bn-hermes-agent-wsj (7/10/2026); https://fourweekmba.com/ai-nous-research-closes-90m-series-b-at-a-1-5b-valuation/ ; https://cryptobriefing.com/nous-research-series-b-hermes-agent/ ; https://theaiinsider.tech/2026/10/08/nous-research-secures-90m-series-b-at-1-5b-valuation-to-bring-hermes-ai-agents-to-enterprises/
- App iOS: https://github.com/NousResearch/hermes-agent/issues/11911 ; https://github.com/NousResearch/hermes-agent/issues/50745 ; https://www.bitdoze.com/best-hermes-dashboards/ ; https://github.com/dylan-buck/Hermes-iOS
- Issue di affidabilità: https://github.com/NousResearch/hermes-agent/issues/58032 ; /143150 ; /141623 ; /143547 ; https://www.betterclaw.io/blog/hermes-agent-not-working
- CVE: https://www.sentinelone.com/vulnerability-database/cve-2026-14628/ ; https://vuldb.com/vuln/424854 ; https://github.com/advisories/GHSA-wm96-9gfh-vvgq ; https://labs.cloudsecurityalliance.org/research/csa-research-note-hermes-agent-cves-20260504-csa-styled/
- Prezzi Portal (terzi): https://standardcompute.com/alternatives/nous-portal ; https://openclawlaunch.com/guides/nous-portal
- Politica Anthropic (terzi): https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/ ; https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and
- File locali: la trascrizione del notiziario di agentnative.inc, non pubblicata in questa repo; clone locale del repository (HEAD 4e74031, 1/10/2026)
