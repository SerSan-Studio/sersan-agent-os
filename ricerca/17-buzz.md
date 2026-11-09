# 17 — buzz di Block: la stanza comune fra persone e agenti (voce A7)

Data di rilevazione: **24 ottobre 2026**. Oggetto: https://github.com/block/buzz, "lo spazio di lavoro self-hosted dove persone e agenti AI stanno nelle stesse stanze", valutato come candidato per la chat condivisa fra agenti e persone (voce A7 di `ricerca/00-visione-funzionalita.md`) e per l'organigramma di agenti (voce G9).

**Metodo e fonti.**
- Il codice del repository all'HEAD `8599efb`, letto il 14-15 ottobre 2026.
- Il web al 24/10/2026: GitHub (API e pagine), la pagina di supporto di Block, l'App Store, il blog di ingegneria di Block, guide e recensioni di terzi.

**Legenda.**
- **[verificato: fonte]**: controllato sulla fonte indicata.
- **[codice 14/10]**: verificato nel codice al 14 ottobre. Il codice cambia ogni giorno, quindi va ricontrollato prima di decidere.
- **[non verificato]**: voce di terzi o deduzione mia.
- **[stima]**: un numero mio, con il ragionamento accanto.

---

## 0. In breve

1. **Che cos'è.** È una chat aziendale tipo Slack: canali, thread, DM, canvas, ricerca, app desktop e telefono. Ci aggiunge tre cose:
   - **gli agenti sono membri veri**, con una chiave propria, un proprietario, una memoria e una trascrizione del lavoro;
   - **workflow YAML** legati ai canali;
   - **un forge git**.

   Tutto gira su un relay Nostr che si ospita in casa: Postgres, Redis e S3/MinIO. La licenza è Apache-2.0. [verificato: README e API GitHub, 24/10]
2. **Maturità: pre-1.0 e molto attivo.** Questi i numeri:
   - 36.420 stelle, 4.818 fork, 3.010 commit;
   - ultima release desktop v0.5.28 del 9/10/2026, ultimo push il 24/10/2026;
   - lancio pubblico il 21/7/2026.

   Il README stesso scrive "Not finished". [verificato: API GitHub 24/10; README]
3. **Per A7 è il candidato più diretto visto finora.** È nato esattamente per "agenti e persone nelle stesse stanze":
   - un agente ne delega un altro con una @menzione;
   - le persone leggono tutto;
   - ogni agente ha la sua memoria cifrata per il proprietario.

   Copre bene A7, in parte A5, A6, C1, C6, E3 e G9. Non copre il resto della visione: Notion, database vettoriale, email, CRM, bot nelle call, telefonia (§6).
4. **Non è un orchestratore.** buzz è il *luogo* dove gli agenti parlano, non il *cervello* che li coordina ("il relay è la tubatura, non il cervello"). Gli agenti veri restano Claude Code, Codex, Goose, Hermes Agent, OpenClaw, Cursor e altri. Li collega l'harness `buzz-acp`. [codice 14/10; preset ricontrollati sul repo il 24/10]
5. **Tre lacune bloccanti per un uso aziendale. Al 24/10 nessuna è chiusa.**
   - **(a) Nessun freno nel codice ai giri fra agenti.** Gli autori stessi hanno visto una catena di più di 21 risposte fra tre agenti.
   - **(b) Le approvazioni nei workflow non funzionano.** Un passo `request_approval` fa fallire l'esecuzione. Le PR che le collegano sono aperte o chiuse senza merge.
   - **(c) I permessi degli strumenti sono approvati in automatico.** Di default vale `bypass-permissions`, e la chiave privata dell'agente sta nell'ambiente del suo processo.

   [codice 14/10; ricerca issue e PR su GitHub del 24/10]
6. **Sul server SerSan ci sta largo.** Il relay con i suoi servizi chiede pochi GB di RAM [stima]. I processi degli agenti pesano di più, ma 160 GB bastano per decine di agenti. La GPU non serve a buzz.
7. **Costo.**
   - Self-host: licenza 0 €.
   - Versione ospitata da Block su buzz.xyz: oggi gratuita, solo su invito, con limiti non ancora pubblicati e messaggi leggibili da Block.
   - Railway: 5-20 $/mese di piano più il consumo.

   Il costo vero sono i token dei modelli e il tempo di chi lo gestisce (§10).

**Raccomandazione.** Candidato forte per A7, da provare in pilota su un perimetro chiuso: un canale interno, 3-5 agenti, nessun dato di clienti. Va messo dietro tre protezioni nostre: freno ai giri, approvazioni esterne, agenti isolati in container. Non va usato come orchestratore né come "secondo cervello". La decisione finale va presa dopo il confronto con le alternative per A7 (Slack, Mattermost, Telegram e la chat di Hermes) negli altri rapporti di questa serie.

---

## 1. Che cos'è

| Aspetto | Fatto | Fonte |
|---|---|---|
| Identità | "A workspace where humans and agents build together, on a relay you own"; descrizione GitHub "A hive mind communication platform" | [verificato: README e API GitHub, 24/10] |
| Chi lo fa | Block, Inc. (Jack Dorsey), team `@block/buzz-oss-team`; prima si chiamava Sprout, rinominato in v0.3.17 | [codice 14/10] |
| Licenza | Apache-2.0: si può usare in azienda, modificare e copiare tenendo l'avviso | [verificato: API GitHub, 24/10] |
| Architettura | relay Rust (Axum) che salva ogni messaggio, reazione, workflow ed evento git come evento Nostr firmato; Postgres 17 (dati e ricerca full-text), Redis 7 (fan-out, anti-replay, rate limit: obbligatorio anche con un solo nodo), S3/MinIO (media e pacchetti git) | [codice 14/10] |
| Client | app desktop Tauri e React (macOS, Linux, Windows "alpha"), app mobile Flutter, CLI `buzz` pensata per gli agenti, web solo per inviti e per sfogliare le repo, console admin | [verificato: release GitHub 24/10; codice 14/10] |
| Che cosa non vuole essere | "Not blockchain", "Not an AI replacement plan", "Not finished" | [verificato: README, 24/10] |
| Dimensioni | circa 1,66 milioni di righe; 34 crate Rust; il relay da solo ha 159.289 righe | [codice 14/10] |

---

## 2. Maturità e stato al 24 ottobre 2026

| Indicatore | Valore | Fonte |
|---|---|---|
| Stelle / fork | 36.420 / 4.818 | [verificato: api.github.com/repos/block/buzz, 24/10] |
| Commit su `main` | 3.010 | [verificato: pagina GitHub, 24/10] |
| Issue e PR aperte | 3.667 in totale (la pagina dice circa 1,7k issue e 2k PR) | [verificato: API e pagina GitHub, 24/10] |
| Creato / lancio pubblico | repo creato il 06/03/2026; lancio pubblico il 21/07/2026 | [verificato: API GitHub; recensione hills-lab.hr del 28/07/2026] |
| Ultimo push | 24/10/2026 20:08 UTC | [verificato: API GitHub, 24/10] |
| Ultime release desktop | v0.5.28 il 09/10/2026; v0.5.27 il 06/10; v0.5.26 il 29/09: una ogni 3-7 giorni, nessuna nelle ultime due settimane | [verificato: API releases GitHub, 24/10] |
| App iOS | "Buzz - chat with your hive", Block, Inc., gratuita, v0.25.1 di circa il 23/10, iOS 16+, voto 4,2 su 5 con 64 recensioni; le recensioni segnalano risposte degli agenti che non compaiono finché non si riapre l'app e notifiche poco affidabili con relay self-hosted | [verificato: apps.apple.com id6779728271, 24/10] |
| Stato dichiarato nel README | "Works today": relay, canali, thread, DM, canvas, media, ricerca, audit, desktop, CLI, workflow YAML, git. "Being wired up": client mobile, approvazioni nei workflow, eventi del ciclo degli huddle. "Strong opinions, pending code": reputazione fra relay, push, funzioni di "cultura" | [verificato: README, 24/10]. Il README è indietro rispetto al codice: push e app mobile esistono [codice 14/10] |
| Documenti contro codice | circa 70 punti in cui documenti e codice divergono, nei due sensi | [codice 14/10] |
| Giudizio di terzi | "a pre-1.0 system with several important boundaries"; da provare "on a bounded internal project", non da usare per sostituire Slack e GitHub in tutta l'azienda | [non verificato: recensione hills-lab.hr, 28/07/2026] |

**Lettura.** È un progetto grande, finanziato e vivo, con un rilascio a settimana. È anche giovane (sette mesi) e ha migliaia di issue aperte. Va trattato come software in beta: le versioni vanno fissate e gli aggiornamenti provati prima di passarli in produzione.

---

## 3. Applicazioni disponibili

| Piattaforma | Stato al 24/10 | Fonte |
|---|---|---|
| macOS (Apple Silicon e Intel) | `.dmg` firmati, aggiornamento automatico | [verificato: asset della release v0.5.28] |
| Linux x86_64 | `.AppImage` e `.deb` | [verificato: asset della release v0.5.28] |
| Windows x64 | `Buzz_0.5.28_x64-setup_alpha-unsigned.exe`: alpha, non firmato (SmartScreen avvisa). Chiede Git Bash per lo strumento shell degli agenti. Senza tray: chiudere la finestra ferma tutti gli agenti locali. Niente provider per gli agenti remoti | [verificato: asset della release e README; codice 14/10] |
| iOS | in App Store (vedi §2). Chat, thread, DM, menzioni, huddle, trascrizione dal vivo dei propri agenti. Niente creazione o configurazione di agenti, niente approvazioni. Push solo con il gateway di Block, "not shipped to existing users" secondo il README mobile | [verificato: App Store, `mobile/README.md` 24/10; codice 14/10] |
| Android | il blog di Block del 29/07/2026 la dice su Google Play (pacchetto `xyz.block.buzz.mobile` secondo un articolo di terzi). La pagina del Play Store non si è caricata. Nel codice Android non ha push | [non verificato: pagina Play; verificato: blog engineering.block.xyz "A Buzz on your phone"; codice 14/10] |
| Telefono senza desktop | non previsto: il telefono si accoppia al desktop con un QR e ne riceve **la stessa chiave privata**, quindi non c'è una revoca per singolo dispositivo | [verificato: blog di Block 29/07; codice 14/10] |
| Web | solo la pagina d'invito e il browser delle repo; non è un client di chat | [codice 14/10] |
| CLI `buzz` | 23 gruppi e circa 120 comandi, uscita JSON e codici d'uscita fissi; è la voce degli agenti | [codice 14/10] |

**Per SerSan.** Il team lavora su Windows (almeno Alberto). Il desktop su Windows è il porto meno curato, e gli agenti gestiti "in locale" vivono dentro l'app desktop. Per avere agenti 24/7 bisogna farli girare sul server (§7), non sui PC.

---

## 4. Ospitarlo: requisiti e opzioni

| Opzione | Cosa comporta | Fonte |
|---|---|---|
| **Compose su un nodo** (`deploy/compose/`) | 5 container a regime: relay, `postgres:17-alpine`, `redis:7-alpine`, MinIO (fork Silo), `caddy:2-alpine` per il TLS automatico Let's Encrypt (`BUZZ_COMPOSE_TLS=true ./run.sh start`). `.env` con segreti stabili (`BUZZ_RELAY_PRIVATE_KEY`, `BUZZ_GIT_HOOK_HMAC_SECRET`, `RELAY_OWNER_PUBKEY`). Immagine da fissare per digest, perché `main` cambia a ogni merge. `./run.sh backup-hint` dà la lista per i backup | [verificato: `deploy/compose/README.md`, 24/10; guida SSD Nodes 11/10/2026] |
| Helm | chart con Postgres, Redis e S3 esterni e CronJob | [codice 14/10] |
| Railway | pulsante "Deploy on Railway" nel README | [verificato: README, 24/10] |
| **Ospitato da Block** (buzz.xyz) | "Block-hosted communities are free"; solo su invito; per ora fino a 3 community per account; limiti di spazio "will be published when they are final"; maggiorenni; messaggi, DM e media **non** cifrati end-to-end, quindi Block può accedervi; luogo dei dati non indicato. La CHANGELOG v0.5.28 dice "raise hosted community limit to fifty", in contrasto con le 3 della pagina di supporto | [verificato: block.github.io/buzz/support.html e CHANGELOG, 24/10] |
| Risorse hardware | **nessun requisito ufficiale**. Una guida di terzi scrive "A 2 vCPU, 4 GB plan is a starting point, not a number to trust" e dice che nessuno ha pubblicato misure | [verificato: guida SSD Nodes 11/10/2026; requisiti ufficiali: non trovati] |
| Sistema operativo | il relay è solo Linux (immagini amd64 e arm64). Su Windows non gira in modo nativo | [codice 14/10] |
| Rete | i client si collegano in `wss://` (TLS). Servono le porte 80 e 443 per Let's Encrypt, oppure un TLS proprio dietro VPN | [verificato: guida SSD Nodes] |
| Multi-utente | una community per host (sottodominio), ruoli owner, admin, member, guest e bot; inviti a tempo; moderazione; audit a catena di hash per community. Per 4 persone basta una community | [codice 14/10] |

---

## 5. Come lavorano gli agenti dentro buzz

| Tema | Stato reale | Fonte |
|---|---|---|
| **Entrata** | ogni agente ha una coppia di chiavi e un'attestazione firmata dal proprietario (NIP-OA); entra nei canali con il ruolo `bot` | [codice 14/10] |
| **Runtime (harness `buzz-acp`)** | di primo livello: Claude Code (via `claude-agent-acp`), Codex (`codex-acp`), Goose, `buzz-agent`. Preset nel desktop: Pi, Devin, Cursor (`cursor-agent acp`), Oh My Pi, Grok Build (con `--always-approve`), OpenCode, Kimi Code, Amp, **Hermes Agent** (`hermes-acp`), **OpenClaw** (`openclaw acp`, con l'avviso che i suoi strumenti girano nel gateway di OpenClaw e non vedono le variabili `BUZZ_*`). Più definizioni personalizzate. Da 1 a 32 sessioni parallele per agente (default 10) | [verificato: `presets.rs` su main, 24/10; codice 14/10] |
| Credenziali dei modelli | il README dell'harness chiede `ANTHROPIC_API_KEY` per Claude e `OPENAI_API_KEY` per Codex ("not a ChatGPT subscription"); il desktop invece guida Claude Code con il login della CLI. `buzz-agent` parla anche con endpoint compatibili OpenAI (Ollama, llama.cpp) | [codice 14/10] |
| Integrazione Hermes | esiste ma è fragile. Aperti: #6921 (su Windows il runtime Hermes gestito si blocca), #7172 (risposte doppie con Hermes 0.21, PR in bozza), #6221, #5621, #6541 (approvazione umana e ripresa per un agente Hermes esterno) | [verificato: ricerca issue GitHub, 24/10] |
| Integrazione Claude Code | aperta la #7375, "Base and system prompts not reaching claude-agent-acp" | [verificato: ricerca issue GitHub, 24/10] |
| **Chi sveglia un agente** | di default solo il proprietario (`respond_to = owner-only`), con una menzione o un DM. Gli agenti "fratelli" dello stesso proprietario passano anche loro. Altre politiche: `allowlist`, `anyone`, `nobody` | [codice 14/10] |
| **Menzioni e deleghe** | la delega è una @menzione; chi finisce deve menzionare chi ha delegato (regola scritta solo nel prompt). Un agente menzionato in un thread resta destinatario dei messaggi seguenti. Non esiste un oggetto "passaggio di lavoro" con obiettivo e tetto: i kind dei job (43001-43006) ci sono, ma nessuno li produce | [codice 14/10] |
| **Freno ai giri fra agenti** | **assente nel codice**. Il guasto documentato: più di 21 risposte in catena fra tre agenti nel canale di benvenuto, corretto solo nel prompt. Il freno proposto dagli autori (un budget di 6-10 risposte consecutive fra agenti per thread, azzerato da un messaggio umano) non c'è. Al 24/10 la ricerca su GitHub non trova PR con un tetto: la #8124 (merge del 06/10) tiene solo le risposte nel thread, e la #8045 propone tetti ma è aperta | [codice 14/10; verificato: ricerca issue e PR, 24/10] |
| **Memoria per agente** | NIP-AE: memoria cifrata fra agente e proprietario, sul relay. Il `core` (fino a 64 KB, consigliato sotto i 10 KB) entra all'apertura della sessione; il resto si legge con `buzz mem`. Un errore di lettura non vale mai come memoria vuota. Il proprietario la legge in sola lettura. **Non c'è una memoria condivisa fra agenti**: fanno da contesto comune le istruzioni di squadra, il canvas del canale e un `AGENTS.md` | [codice 14/10] |
| Persone, squadre, catalogo | la persona (nome, avatar, prompt, runtime, modello) genera gli agenti; la squadra è un elenco **piatto** con istruzioni comuni; si esportano come `.agent.json` o `.team.json` senza segreti; template di canale. Un agente può proporre la creazione di un altro agente come bozza, che il proprietario salva | [codice 14/10] |
| **Workflow: inneschi** | `message_posted`, `reaction_added`, `diff_posted`, `schedule` (cron in UTC o intervallo di almeno 60 s), `webhook` (`POST /hooks/{id}` con segreto), avvio manuale | [codice 14/10] |
| **Workflow: azioni** | funzionano `send_message` (con @menzione sveglia un agente con l'autorità del proprietario), `call_webhook` (con guardia SSRF, 10 s, risposta fino a 1 MiB) e `delay` fino a 270 s. Non funzionano `send_dm` e `set_channel_topic` (`NotImplemented`) né `add_reaction` (chiama una rotta che non esiste) | [codice 14/10] |
| **Workflow: approvazioni** | **non collegate**: ogni esecuzione che arriva a `request_approval` finisce `failed`, e il desktop scrive "Approval actions are not yet available in Desktop". Al 24/10 sono aperte la PR #8057 (sospendere e riprendere una volta sola) e la #7616 (azioni nel desktop); la #6688 (WF-08) e la #7833 sono chiuse senza merge | [codice 14/10; verificato: ricerca PR GitHub, 24/10] |
| Scatti pianificati | claim durevole per scatto (mai doppi), autorità del proprietario ricontrollata a ogni esecuzione; gli scatti persi a relay spento non si recuperano | [codice 14/10] |
| **Trascrizioni del lavoro** | trascrizione del turno dal vivo, cifrata per il proprietario e mai salvata dal relay (NIP-AO); il desktop può archiviarla in locale; dal telefono si legge | [codice 14/10] |
| **Costo per turno** | NIP-AM: un evento per turno con token in ingresso e uscita, costo stimato e cumulativo di sessione, cifrato al proprietario. Il desktop lo archivia, ma **nessuna schermata lo mostra** | [codice 14/10] |
| Fermare un agente | `!shutdown`, `!cancel`, `!rotate` dal proprietario; "Stop current turn" dal desktop (con più sessioni nello stesso canale risponde `ambiguous_target`); interruttore dopo 3 crash in 60 s | [codice 14/10] |
| **Voce e huddle** | chiamate di gruppo con agenti dentro (fino a 25 partecipanti, al massimo 20 agenti). STT e TTS **locali e solo in inglese** (Parakeet 110M, Pocket TTS); la voce dell'agente può essere clonata da un campione di 2-30 s. Nessun riassunto, nessuna registrazione. Gira nel desktop, non sul server | [codice 14/10] |
| **Integrazioni** | **nessuna nativa con Slack, email, HubSpot o Notion**. Si entra con: webhook in ingresso dei workflow, `call_webhook` in uscita, client Nostr di terzi, la CLI, e soprattutto i server MCP del runtime dell'agente (per esempio i connettori di Claude Code). Su GitHub nessuna issue chiede un bridge Slack o email; c'è una richiesta aperta di autenticazione servizio-servizio per il ponte HTTP (#6123) | [codice 14/10; verificato: ricerca issue, 24/10] |

---

## 6. Copertura della visione (A1–I4)

Legenda: **Sì** = buzz lo fa così com'è; **Parziale** = un pezzo c'è o si compone con poco; **No** = serve altro; **n.a.** = non è una funzione software.

| # | Voce della visione | Copertura | Come, o che cosa manca |
|---|---|---|---|
| A1 | Contesto totale: ogni riunione registrata e trascritta | Parziale | gli huddle interni si trascrivono, ma solo in inglese e senza registrazione; le call esterne (Meet, Zoom, Teams) no. Serve Fireflies o equivalente che spinge il testo con il webhook [codice 14/10] |
| A2 | Second brain relazionale (Notion) | No | canvas per canale e memoria per agente sono sostituti parziali; Notion resta, raggiunto dagli agenti via MCP |
| A3 | Database vettoriale | No | solo la ricerca full-text di Postgres, senza embedding [codice 14/10] |
| A4 | Orchestratore self-hosted | Parziale | buzz è il luogo, non l'orchestratore; può ospitare Hermes Agent come runtime con `hermes-acp` (integrazione con difetti aperti) |
| A5 | 25 agenti per ruolo (raccolta, pulizia, indicizzazione, azione) | Parziale | persone, squadre e canali per ruolo; ogni agente è un processo; nessuna gerarchia né livelli |
| A6 | Gli agenti imparano | Parziale | memoria per agente persistente; nessun auto-apprendimento né skill che si aggiornano da sole |
| **A7** | **Chat condivisa fra agenti, leggibile dagli umani** | **Sì** | è lo scopo del prodotto: menzioni, deleghe, thread, trascrizione dal vivo. Manca il freno ai giri (§8) |
| B1 | Post-call: punti e next step sul canale del cliente | Parziale | un canale per cliente sì, ma interno: il cliente non sta in buzz e non c'è un bridge Slack |
| B2 | Opportunità sul CRM | No | via MCP dell'agente o via SersanOutreach |
| B3 | Mail di follow-up | No | buzz non ha email; via MCP Gmail o SersanOutreach |
| B4 | To-do al team | Parziale | issue dei progetti (pensate per il codice) e promemoria, ma gli agenti non hanno un comando per i promemoria; per il resto Notion via MCP |
| B5 | Autonomia totale | Sì, anzi troppa | gli agenti agiscono senza approvazioni; è un rischio, non un pregio (§9) |
| C1 | Debrief del mattino | Parziale | workflow `schedule` (cron UTC) → messaggio che menziona l'agente del debrief; il calendario va letto via MCP |
| C2 | Agente dentro le call | No | gli huddle sono solo interni a buzz |
| C3 | Analisi della trascrizione con Claude | Sì, componendo | un agente Claude Code nel canale, con il testo arrivato dal webhook |
| C4 | Dettatura | Parziale | STT solo negli huddle e solo in inglese; note vocali senza trascrizione |
| C5 | Registro dei meeting di tutta l'azienda | Parziale | canali e ricerca full-text; nessuna struttura (pipeline, presenti) |
| C6 | Regole di lavoro per persona lette dagli agenti | Parziale | istruzioni d'agente e di squadra, canvas, memoria `core`; le regole in Notion via MCP |
| D1 | Portale CRM con pipeline pesata | No | il forge può ospitare il codice del portale, non lo fa |
| D2 | Brief pre-meeting da una email | No | un agente con MCP e SersanOutreach; buzz porta solo il risultato nel canale |
| D3 | Storico della relazione | No | come D2 |
| D4 | Slide automatiche | No | via MCP (moda.app, Canva) |
| D5 | Offerta automatica | No | agente più catalogo; buzz è solo il canale |
| E1-E2 | Curva d'apprendimento, vantaggio dei token bassi | n.a. | |
| E3 | Policy e banca dei token | Parziale | metrica di costo per turno cifrata (senza schermata) e rate limit per classe d'agente; **nessun tetto di budget** |
| E4 | Formazione | n.a. | |
| F1-F4 | Mappa dei processi dai metadati di Workspace | No | |
| F5 | AI diffusa in tutta l'organizzazione | Parziale | interfaccia familiare tipo Slack, app su telefono; chiunque menziona un agente (se il proprietario lo permette) |
| G1 | Canale delle call di vendita | Parziale | il canale sì; la trascrizione arriva da fuori |
| G2-G4 | Fit score, performance del sales, coaching | No | sono agenti da costruire; buzz consegna i report nei canali |
| G5 | Agente vocale "Andrea" che chiama le lead | No | niente telefonia; voce solo in inglese e solo negli huddle interni |
| G6 | Impara dai rifiuti | No | |
| G7-G8 | Risultati; analisi delle chiusure verso il marketing | No | |
| **G9** | **100+ agenti in organigramma** | Parziale | persone, squadre piatte e catalogo per community; nessun organigramma gerarchico; 100 agenti vogliono dire 100 processi da far girare |
| H1-H5, H7 | Formazione e adozione | n.a. | |
| H6 | Premio mensile | No | kudos e funzioni di "cultura" esistono solo nella visione di buzz [codice 14/10] |
| I1-I2, I4 | Avvertenze | n.a. | |
| I3 | Aree dove l'AI non si usa di proposito | Parziale | canali senza agenti, `respond_to: nobody` o `owner-only`; la regola resta organizzativa |

**Conteggio** sulle 34 righe con contenuto software (escluse le n.a.; F1-F4, G2-G4 e G7-G8 contano una riga ciascuna): 3 sì (A7, B5, C3), 15 parziali, 16 no. buzz copre la **stanza** della visione, non il **cervello** (A1-A3, D, F, G).

---

## 7. Come starebbe sul server SerSan

Hardware dal brief: HPE ProLiant DL380 Gen10 (presunto), 160 GB di RAM DDR4 ECC, NVIDIA Quadro RTX 4000 8 GB, controller Smart Array E208i-p, più un mini PC router/firewall con 4 porte i226-V. Modello di CPU e dischi: **non trovati** nel brief.

| Componente | Dove gira | RAM | CPU | Disco | Note |
|---|---|---|---|---|---|
| Relay, Postgres 17, Redis 7, MinIO, Caddy | una VM o un host Linux (Ubuntu) con Docker Compose | 4-8 GB [stima: il "punto di partenza" di terzi è 4 GB; raddoppio per Postgres e MinIO con media e git] | 2-4 vCPU [stima] | 50-100 GB all'inizio, su RAID [stima: testo e media di 4 persone; i media sono il grosso] | `events` partizionata per mese; full-text in Postgres. Backup: dump di Postgres, bucket MinIO, `.env` e chiave del relay (la chiave persa non si recupera) |
| Agenti (un `buzz-acp` e il runtime, per esempio Claude Code, per agente) | stesso host o una VM a parte, **un container per agente** | 0,5-1 GB per sessione attiva [stima non verificata, Node.js più i server MCP]; con 25 agenti e parallelismo 1-2: 15-50 GB | variabile; il carico vero è dal lato del fornitore del modello | pochi GB per agente (cartella di lavoro e cache) | 160 GB bastano. Conviene abbassare il parallelismo di default (10) a 1-2 per agente |
| GPU Quadro RTX 4000 | non serve a buzz | | | | utile solo se si usa `buzz-agent` con un modello locale su endpoint compatibile OpenAI (Ollama); con 8 GB di VRAM, modelli piccoli [stima] |
| Voce locale degli huddle | nei desktop degli utenti, non sul server | | | | solo inglese: per SerSan va sostituita (ElevenLabs) o lasciata spenta |
| Rete | il mini PC firewall | | | | due strade: (1) relay raggiungibile solo in VPN WireGuard, più semplice e sicura per 4 persone; (2) pubblico con Caddy e Let's Encrypt sulle porte 80 e 443, necessario per il webhook di Fireflies o per l'app iOS fuori VPN. In ogni caso il webhook va filtrato (§9) |

**Agenti 24/7 senza un PC acceso.** Gli agenti "gestiti" nascono nel desktop e, se locali, muoiono con lui. Su Windows chiudere la finestra li ferma tutti [codice 14/10]. Per il server ci sono tre strade:
- **(a) `buzz-acp` headless su Linux.** È un binario a sé, configurato con `BUZZ_RELAY_URL`, `BUZZ_PRIVATE_KEY` e `BUZZ_AUTH_TAG`. È quello che fa il Pod Kubernetes degli agenti remoti, con `buzz-acp` come processo 1 [codice 14/10]. Il percorso completo "creo l'agente dal desktop e lo faccio girare sul server sotto systemd o in un container" **non è documentato passo per passo** [non verificato].
- **(b) Il provider Kubernetes** (`buzz-backend-kubernetes`) su un k3s nel server. Il binario provider però non esiste per Windows, quindi il deploy va lanciato da un desktop macOS o Linux [codice 14/10].
- **(c) Un PC Linux sempre acceso con il desktop.** È la soluzione meno pulita.

**SersanOutreach.** Una volta spostato sul server, può parlare con buzz in due modi:
- in uscita, con un webhook verso `POST /hooks/{id}`, che crea un messaggio e menziona l'agente giusto;
- in entrata, con gli agenti che chiamano le sue API via MCP o con `call_webhook`.

---

## 8. Cosa manca e come colmarlo

| # | Lacuna | Gravità | Come colmarla | Sforzo [stima] |
|---|---|---|---|---|
| 1 | Nessun freno ai giri fra agenti | alta | patch nel nostro fork di `buzz-acp` con il freno proposto dagli autori: budget di 6-10 risposte consecutive fra agenti per thread, azzerato da un messaggio umano, con una riga di log. In più: agenti di proprietari diversi o con `respond_to: allowlist`, un solo agente "smistatore" per canale, workflow che non rispondono ad agenti | 1-3 giorni |
| 2 | Approvazioni dei workflow non collegate | alta | aspettare la PR #8057 oppure tenere le approvazioni **fuori** da buzz: la coda di approvazione umana di SersanOutreach, o un server MCP "chiedi approvazione" che posta nel canale e aspetta una reazione di una persona autorizzata. Mai approvazioni concesse da un agente (il prompt di heartbeat invita l'agente ad approvare: [codice 14/10]) | 2-5 giorni |
| 3 | Permessi degli strumenti in `bypass-permissions` e `allow_once` automatico | alta | il freno va messo sotto l'agente: un container per agente con utente non privilegiato, chiavi API e token MCP con scope minimo (per esempio CRM in sola lettura), regole di negazione del runtime ([non verificato] se `claude-agent-acp` rispetta le regole di `settings.json` di Claude Code); niente `--always-approve` (preset Grok) | 2-4 giorni per il modello di base |
| 4 | Chiave privata dell'agente nell'ambiente del processo | media | un container per agente, nessun altro segreto nello stesso ambiente, rotazione delle chiavi se un agente è compromesso. Il broker previsto dagli autori esiste solo come contratto [codice 14/10] | incluso nel punto 3 |
| 5 | Costo per turno senza schermata; nessun tetto | media | **una chiave API Anthropic per agente**: la console Anthropic dà l'uso per chiave, cioè la "banca dei token" per agente; oppure un piccolo cruscotto che legge gli eventi 44200 con la chiave del proprietario | 1-2 giorni |
| 6 | Nessuna integrazione con email, CRM, Notion, Slack | media | server MCP nel runtime degli agenti (Claude Code con i connettori), webhook in ingresso per Fireflies e SersanOutreach, `call_webhook` in uscita | per integrazione |
| 7 | Webhook in ingresso senza firma del corpo, anti-replay né rate limit; segreto anche come `?secret=` | media | metterlo dietro Caddy o n8n con allowlist di IP, firma HMAC verificata a monte e rate limit; segreto solo nell'header | 0,5-1 giorno |
| 8 | Nessuna memoria condivisa né base di conoscenza | media | Notion e un database vettoriale fuori da buzz, raggiunti via MCP; il canvas del canale come "memoria della stanza" | fuori da buzz |
| 9 | Organigramma piatto | bassa | organigramma in Notion o nel canvas di un canale `#organigramma`; squadre per area; un agente capo-squadra per canale | basso |
| 10 | Voce solo in inglese | bassa per A7, alta per G5 | gli huddle non servono alla visione; per G5 una soluzione telefonica a parte (ElevenLabs più telefonia) | fuori da buzz |
| 11 | Messaggi in chiaro in Postgres, indicizzati | bassa in self-host | disco cifrato (LUKS) e backup cifrati; chi gestisce il server legge tutto, e va detto al team | 0,5 giorni |
| 12 | Audit a catena senza chiave ("tamper-evident, not tamper-resistant") | bassa | copia periodica degli hash della catena fuori dal server | basso |
| 13 | Windows: desktop alpha, segreti oltre 2.560 byte scritti in chiaro su disco | media per chi usa Windows | agenti sul server, desktop Windows solo come client; controllare dove finisce il blob dei segreti | basso |

---

## 9. Rischi

| Rischio | Probabilità | Impatto | Mitigazione |
|---|---|---|---|
| Giri infiniti fra agenti che bruciano token | media (successo agli autori stessi) | costo e rumore nei canali | §8 punto 1, più un tetto di spesa per chiave API |
| Prompt injection: un testo esterno (email, trascrizione, webhook) entra in un canale e un agente con permessi pieni agisce | media | alto: invii, cancellazioni, dati verso terzi | §8 punti 2-3; un canale "ingresso" letto da agenti senza strumenti d'azione |
| Agente "confused deputy": con `respond_to: anyone` chiunque nel canale lo pilota con i permessi del proprietario | bassa con 4 persone | medio | `owner-only` o `allowlist`; accesso condiviso solo dove serve [codice 14/10] |
| Cambiamenti che rompono, a ritmo settimanale | alta | medio | fissare l'immagine per digest e la versione del desktop; aggiornare dopo prova |
| Integrazione Hermes o Claude Code instabile | media (issue aperte #6921, #7172, #7375) | medio | pilota con Claude Code via API e con `buzz-agent`; Hermes dopo |
| Dipendenza dal futuro di Block (roadmap, gateway push, ospitato) | media | basso in self-host (Apache-2.0, fork possibile) | self-host; nessuna dipendenza dal gateway push |
| Dati dei clienti su buzz.xyz (non cifrati, luogo non indicato, termini in beta) | dipende dalla scelta | alto per GDPR | non usare l'ospitato per dati dei clienti |
| Il team non lo adotta (doppia chat con Slack o WhatsApp) | media | alto | decidere se buzz sostituisce la chat interna o resta solo la stanza degli agenti |
| Lavoro di manutenzione su un server in casa | certa | tempo di Alberto | Compose, backup automatici, monitoraggio di `/_liveness` |

---

## 10. Costi

| Voce | Self-host sul server SerSan | Ospitato da Block (buzz.xyz) | Railway (alternativa cloud) |
|---|---|---|---|
| Licenza | 0 € (Apache-2.0) [verificato] | 0 €: "Block-hosted communities are free", limiti da pubblicare [verificato: pagina di supporto, 24/10] | 0 € |
| Infrastruttura | server già comprato; costo marginale di energia e disco **non calcolato** | 0 € | piano Hobby 5 $/mese o Pro 20 $/mese per workspace, più il consumo: RAM circa 10 $/GB-mese, vCPU circa 20 $/mese, volumi 0,15 $/GB-mese, object storage 0,015 $/GB-mese [verificato: railway.com/pricing, 24/10]. Con 2 vCPU e 4-8 GB: **circa 80-120 $/mese** [stima] |
| Agenti | girano sul server: 0 € di calcolo | **non ospita agenti**: girano comunque su macchine nostre | idem |
| Modelli (il costo vero) | token Anthropic: i 800 $/mese di crediti API coprono i primi agenti; Codex e OpenAI a parte | uguale | uguale |
| Tempo | installazione e messa in sicurezza: 3-5 giorni; patch e protezioni di §8: 1-2 settimane; manutenzione: alcune ore al mese [stima] | installazione quasi nulla; le protezioni degli agenti servono uguale | come self-host meno l'hardware |
| Vincoli | nessuno; dati in casa | solo su invito, fino a 3 community, maggiorenni, Block può leggere messaggi e media | dati presso Railway |

**Abbonamenti.** buzz non richiede abbonamenti. L'unico servizio a pagamento collegato è il fornitore dei modelli. Per gli agenti sul server conviene la **chiave API** (come chiede il README dell'harness), non il login degli abbonamenti Claude Team: se i posti Team possano alimentare agenti automatici 24/7 su un server è **[non verificato]** e va chiarito con i termini di Anthropic.

---

## 11. Domande aperte

1. buzz deve **sostituire** la chat interna del team (oggi Slack, WhatsApp o altro: non trovato) o restare solo la stanza degli agenti? Ne dipende l'adozione.
2. I clienti devono vedere i canali? B1 vuole il recap "sul canale Slack del cliente": buzz non ha un bridge, e far entrare un cliente vuol dire app, chiave Nostr e invito.
3. Relay solo in VPN o pubblico? Il webhook di Fireflies e l'app iOS fuori ufficio chiedono un endpoint pubblico.
4. Chi sono i proprietari degli agenti? Con proprietari diversi gli agenti non si svegliano a vicenda da "fratelli", e questo frena i giri.
5. Si accetta di mantenere un **fork** con il freno ai giri e le approvazioni, o si aspettano le PR di Block (#8057, #8045)?
6. Il sistema operativo del server (Proxmox, Ubuntu, Windows Server) non è nel brief. Il relay chiede Linux.

---

## Fonti

Locali:
- Codice del repository all'HEAD `8599efb` (14-15/10/2026).
- `C:/Users/alber/SerSan-AgentOS/ricerca/00-visione-funzionalita.md` (le voci A1-I4).

Web, rilevato il 24/10/2026:
- https://github.com/block/buzz e https://api.github.com/repos/block/buzz (stelle, fork, date, licenza)
- https://api.github.com/repos/block/buzz/releases (v0.5.26-v0.5.28 e i loro asset)
- https://raw.githubusercontent.com/block/buzz/main/README.md
- https://raw.githubusercontent.com/block/buzz/main/CHANGELOG.md (v0.5.27-v0.5.28)
- https://raw.githubusercontent.com/block/buzz/main/deploy/compose/README.md
- https://raw.githubusercontent.com/block/buzz/main/mobile/README.md
- https://raw.githubusercontent.com/block/buzz/main/desktop/src-tauri/src/managed_agents/discovery/presets.rs
- ricerche issue e PR su api.github.com/search (giri fra agenti, approvazioni, Hermes, Slack ed email)
- https://block.github.io/buzz/support.html (ospitato: gratuito, invito, 3 community, non E2E)
- https://apps.apple.com/us/app/buzz-chat-with-your-hive/id6779728271 (app iOS v0.25.1)
- https://engineering.block.xyz/blog/a-buzz-on-your-phone (29/07/2026: iOS e Android)
- https://railway.com/pricing

Terzi (voci, non fonti ufficiali):
- https://www.ssdnodes.com/learn/self-host-buzz-block-workspace-on-a-vps (11/10/2026)
- https://hills-lab.hr/field-notes/block-buzz-ai-agent-workspace-review/ (28/07/2026)
- https://decrypt.co/374026/jack-dorseys-block-launches-buzz-a-nostr-based-slack-and-github-rival-for-ai-agents (lancio di luglio)
- https://horadecodar.com.br/?p=40653 (pacchetto Android)

Non raggiunte:
- https://block.xyz/inside/introducing-buzz-where-humans-and-agents-work-together (errore "Header overflow")
- la pagina Google Play di `xyz.block.buzz.mobile` (contenuto non caricato)
