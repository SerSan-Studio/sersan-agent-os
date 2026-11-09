# 12 — Altre piattaforme per un "organigramma di agenti" aziendale

Rilevazione: **24 ottobre 2026**. Ambito: le alternative a Hermes e Grok Bot (che hanno i loro rapporti) per costruire il sistema multi-agente di SerSan descritto in `00-visione-funzionalita.md`. Non è un listino completo (i prezzi di dettaglio li fa un altro rapporto): per ogni prodotto do fascia di prezzo, hosting, licenza, canali, multi-agente, memoria, routine, approvazioni e maturità.

**Come leggere i tag**
- **[verificato: fonte]**: letto oggi su pagina ufficiale, documentazione, API di GitHub, o in un rapporto locale già verificato (indicato con il percorso).
- **[non verificato: fonte]**: dato di terzi (blog, articoli, aggregatori) o snippet di ricerca senza aprire la pagina ufficiale.
- **[non verificato]**: conoscenza pregressa, nessuna fonte riletta oggi.
- Dati GitHub (stelle, licenza, ultimo push): letti oggi con l'API pubblica `api.github.com/repos/<repo>` alle ~20:35 UTC [verificato: API GitHub, 2026-10-24].

**Fasce di prezzo usate**: **0** = gratis o self-host senza licenza a pagamento; **€** = fino a ~30 $/utente/mese o a consumo basso; **€€** = 30-150 $/mese per utente o per team; **€€€** = oltre 150 $/mese o consumo che cresce con l'uso (minuti, ore, token).

---

## 0. In breve

1. **Nessun prodotto, da solo, fa tutto ciò che chiede la visione di Alberto.** I pezzi ci sono, ma vanno uniti: un piano di controllo con organigramma, una memoria a due database, un bot di riunione, un agente vocale e i connettori verso Slack, HubSpot e Google Workspace.
2. **Il pezzo più vicino all'"organigramma di agenti" è Paperclip** (MIT, self-host, 106.900 stelle [verificato: API GitHub]): organigramma con `reportsTo`, budget per agente con stop al 100%, approvazioni imposte dal runtime, routine cron/webhook, heartbeat, adattatori per Claude Code, Codex, Hermes e OpenClaw, connettori Slack/Teams/Telegram/Discord e Fireflies. Ha meno di otto mesi di vita e nessun team dichiarato [non verificato: fonti terze].
3. **L'offerta Anthropic copre molto e cresce ogni mese, ma non ha un organigramma.** Claude Tag in Slack (beta, Team/Enterprise, memoria per canale, modalità proattiva, limiti di spesa per canale) [verificato: anthropic.com/news/introducing-claude-tag]; Claude Managed Agents (beta, 0,08 $ per ora di sessione più i token, sandbox anche self-host sul proprio server, esecuzioni pianificate) [verificato: platform.claude.com]; crediti API mensili inclusi nel piano Team dal 7 ottobre [verificato: release notes]. **Non ho trovato** i "Projects con coordinatore e thread" citati nella richiesta: non risultano nelle release notes né nella documentazione letta.
4. **OpenAI non è una via per SerSan oggi**: Dots non è disponibile su Pro in UE, Svizzera e Regno Unito; Agent Builder (AgentKit) chiude il 30 novembre 2026 [non verificato: avviso riportato da terzi, pagina OpenAI in 403].
5. **Due prodotti open source della lista sono fermi o quasi**: Flowise è archiviato (README: "Flowise has been archived", ultimo push 13/08/2026) e Khoj non riceve push dal 2 agosto 2026 [verificato: API GitHub e README].
6. **Le licenze "aperte" non sono tutte uguali**: n8n (Sustainable Use License), Dify (Apache modificata), Open WebUI (licenza propria), Inngest (SSPL), Outline (BSL 1.1), Attendee (Elastic 2.0) vanno bene per uso interno ma non per rivendere il servizio [verificato: file LICENSE via API GitHub].
7. **Quattro combinazioni realistiche** (sezione 10): (A) Claude-first gestito, (B) Paperclip sul server con Claude come motore, (C) n8n + Claude API per i flussi deterministici, (D) eve/Chat SDK di Vercel su misura. La (B) con pezzi di (A) e (C) è quella che copre più funzioni della visione di Alberto con il server già comprato.

---

## 1. (a) L'offerta Anthropic

| Prodotto | Cosa fa per l'organigramma | Fatti chiave |
|---|---|---|
| **Claude Team / Enterprise** | Chat, Projects condivisi, Cowork, connettori, skill e plugin per tutti i 5 account | Projects condivisi con permessi su Team/Enterprise dal 1/8/2025 [verificato: release notes]; Cowork GA su macOS e Windows dal 9/4/2026, con analytics e OpenTelemetry per Team/Enterprise [verificato: release notes]; attività pianificate (ricorrenti e su richiesta) in Cowork dal 25/2/2026 [verificato: release notes]; memoria in Cowork **spenta di default** su Team ed Enterprise (25/8/2026) [verificato: release notes]; strumenti di scrittura del connettore Microsoft 365 (posta, calendario, OneDrive/SharePoint) dal 7/7/2026, con consenso Entra [verificato: release notes]; Salesforce in Claude (beta, 37 skill di vendita) dal 15/9/2026 [verificato: release notes]. Prezzo Team: circa 20 $/posto/mese annuale per il posto standard e 100 $ per il premium [non verificato: vantagepoint.io]. |
| **"Projects con coordinatore e thread"** | (richiesto) | **Non trovato**: nessuna voce nelle release notes da luglio a ottobre 2026 né nelle pagine lette [verificato: assenza in support.claude.com/en/articles/12138966]. Da chiedere ad Alberto la fonte. |
| **Claude Tag (Claude in Slack)** | Un "collega" @Claude per canale Slack, che scompone i compiti e lavora con gli strumenti concessi | Annunciato il 23/6/2026, beta per Team ed Enterprise, sostituisce la vecchia app Claude in Slack; memoria limitata ai canali scelti dall'admin ("un'impostazione per le vendite non condivide i ricordi con l'ingegneria"); modalità proattiva che segnala informazioni e riprende thread fermi; può pianificare i propri compiti e lavorare "ore o giorni"; l'admin sceglie strumenti per canale, vede il log di tutto ciò che @Claude ha fatto e chi l'ha chiesto, imposta limiti di spesa in token per organizzazione e per canale; consumo fatturato all'organizzazione con un "launch credit" iniziale senza importo indicato [verificato: anthropic.com/news/introducing-claude-tag]. Il credito sarebbe di 2.500 $ per organizzazioni Team con almeno 10 posti pagati [non verificato: techfinitive.com]: SerSan con 5 posti potrebbe non averne diritto. |
| **Dashboards e Motion** | Viste dati dal vivo; spiegoni animati esportabili in MP4 | Beta dall'8/10/2026; Dashboards su piani a pagamento (connessioni a Redshift, BigQuery, ClickHouse, Databricks, Snowflake, Salesforce), Motion solo Team ed Enterprise [non verificato: the-decoder.com, testingcatalog.com, digitaltrends.com]. Non compaiono nelle release notes lette oggi. |
| **Claude Duet** | Agente proattivo che guarda le app collegate | Research preview dal 21/10/2026 **solo Pro e Max**, non Team [verificato: release notes]. Esiste un clone self-host: `Anil-matcha/open-duet` (ex open-dots), Apache-2.0, 6.146 stelle, "AI coworkers (named agents)" [verificato: API GitHub]. |
| **Crediti API mensili su Team** | Pagano agenti e app propri sulla Claude Platform | Dal 7/10/2026 Max e Team ricevono crediti API mensili, da riscattare collegando un'organizzazione Console in Organization settings > Billing [verificato: release notes]. Da chiarire se gli 800 $/mese di SerSan sono questi crediti o il bundle startup. |
| **Claude Code: sessioni in background, Remote Control, routine** | Agenti che girano sul server e si guidano dal telefono | `claude --bg` e `claude agents --json` in research preview; Remote Control con "Trusted Devices" imponibili dall'admin Team/Enterprise dal 25/6/2026 [verificato: release notes]; routine cloud (`/schedule`) e attività pianificate di sessione. Con `ANTHROPIC_API_KEY` impostata **si spengono** Remote Control, routine, connettori claude.ai, Artifacts. |
| **Claude Code Channels** | Telegram, Discord, iMessage e webhook dentro una sessione aperta | Research preview; plugin Telegram, Discord, iMessage (solo macOS); allowlist con pairing; su Team/Enterprise **bloccati finché un Owner non li abilita** (`channelsEnabled`); con API key Console permessi di default; "Events only arrive while the session is open" [verificato: code.claude.com/docs/en/channels]. Esiste anche "Claude in Slack" di Claude Code, che apre una sessione cloud da una menzione @Claude [verificato: stessa pagina]. |
| **Claude Agent SDK** | Il motore con cui scrivere agenti propri (il "Claude Code programmabile") | Avvia un processo `claude` headless; permessi con hook `PreToolUse`, regole deny/ask, `canUseTool`; `maxBudgetUsd`, `maxTurns`; `resume` delle sessioni. Licenza "Commercial Terms" di Anthropic; chi costruisce per altri usa API key. |
| **Claude Managed Agents** | Agenti a lungo termine ospitati da Anthropic, con sandbox anche sul proprio server | Beta (header `managed-agents-2026-04-01`), attivo di default per ogni account API; concetti Agent / Environment / Session / Events; ambiente nel cloud Anthropic **o "self-hosted sandbox on your own infrastructure"**; strumenti Bash, file, web, MCP; **esecuzioni pianificate con cron** ("scheduled deployments"); non idoneo a Zero Data Retention [verificato: platform.claude.com/docs/en/managed-agents/overview]. Prezzo: token ai prezzi normali più **0,08 $ per ora di sessione** solo nello stato `running` (attesa e idle non contano) [verificato: platform.claude.com/docs/en/about-claude/pricing]. "Dynamic workflows" (fino a 1.000 agenti, 64 alla volta) dal 9/10 [non verificato: fonte terza]. |
| **Chat SDK di Vercel** | Un solo codice per bot su Slack, Teams, Google Chat, Discord, Telegram, WhatsApp | "A unified TypeScript SDK for building chat bots and agents", card JSX e streaming [verificato: chat-sdk.dev]; repo `vercel/chat` MIT, 2.420 stelle, push il 23/10 [verificato: API GitHub]. Non è di Anthropic ma è il modo più rapido di dare canali a un agente Claude scritto in proprio. |

Prezzi di riferimento dei modelli per le API (per milione di token, input/output): Opus 5.5 4 $/20 $, Sonnet 5.5 2 $/10 $, Haiku 5.5 0,10 $/0,50 $ fino a 100.000 token di prompt [verificato: platform.claude.com/docs/en/about-claude/pricing]. Una sessione Managed Agents accesa 24 ore su 24 per un mese costerebbe al massimo ~58 $ di solo runtime (730 h x 0,08 $), più i token.

### Tabella di sintesi (a)

| Prodotto | Prezzo | Hosting | Licenza | Canali | Multi-agente | Memoria | Routine | Approvazioni | Maturità 10/2026 |
|---|---|---|---|---|---|---|---|---|---|
| Claude Team/Enterprise | € a posto | SaaS | proprietaria | web, desktop, mobile | no (un utente per chat) | progetti; Cowork spenta di default su Team | sì (Cowork) | conferme in chat | GA |
| Claude Tag | a consumo, limiti di spesa | SaaS | proprietaria | Slack | un @Claude per canale | per canale | sì (proattiva) | log admin, strumenti per canale | beta |
| Dashboards / Motion | incluso | SaaS | proprietaria | app Claude | no | no | refresh dati | no | beta [non verificato] |
| Claude Code + Channels | abbonamento o API | sul proprio server | Commercial Terms | Telegram, Discord, iMessage, webhook | subagent, workflow, team sperimentali | file di progetto | `/loop`, `/schedule` | hook, permessi | GA + preview |
| Agent SDK | API o abbonamento | ovunque | Commercial Terms | da costruire | da costruire | da costruire | da costruire | hook, `canUseTool` | GA |
| Managed Agents | 0,08 $/h + token | Anthropic o sandbox propria | proprietaria | API (SSE) | dynamic workflows [non verificato] | stato di sessione | cron | policy dei permessi | beta |
| Chat SDK (Vercel) | 0 | ovunque [non verificato fuori Vercel] | MIT | Slack, Teams, GChat, Discord, Telegram, WhatsApp | no | adattatori di stato | no | card interattive | giovane |

---

## 2. (b) OpenAI

- **ChatGPT Business / Enterprise**: Business circa 20 $/utente/mese annuale (25 $ mensile), minimo 2 posti; "Business Premium" circa 100 $/125 $ con 5 volte l'uso dello standard [non verificato: madewell.ai, nocode.mba]. Enterprise a trattativa [non verificato].
- **AgentKit**: lanciato il 6/10/2025 (Agent Builder in beta, ChatKit ed Evals GA, Connector Registry in beta limitata) [non verificato: marktechpost.com]. Un avviso del 3/6/2026 sulla pagina OpenAI annuncerebbe che **Agent Builder ed Evals non saranno più disponibili dal 30 novembre 2026**, con l'invito a passare all'Agents SDK o ai "Workspace Agents" di ChatGPT [non verificato: therundown.ai, reflektlab.ai; openai.com risponde 403 a WebFetch].
- **Dots** (DevDay, 29/9/2026): agenti sempre accesi su GPT-6 Astra, ognuno con computer Linux e Chrome nel cloud; canali ChatGPT, Slack, Teams, SMS beta USA; trigger a orario e da Gmail, Slack, GitHub, MCP; regole a quattro livelli; auto-review con un secondo modello; memoria non visibile né modificabile; **Pro non disponibile in UE, Svizzera e Regno Unito**. Rollout su Pro, Business Premium ed Enterprise "nei mercati idonei", su Enterprise beta spenta di default [non verificato: aiagentslibrary.com, reworked.co]. Per SerSan (Londra + Sardegna) la disponibilità va confermata prima di qualsiasi ipotesi.
- **Codex**: agente di codice di OpenAI; non ho trovato oggi se e come sia incluso nei posti Business [non trovato].
- **open-dots / open-duet**: il repo `Anil-matcha/open-dots` ora reindirizza a `Anil-matcha/open-duet`, Apache-2.0 [verificato: API GitHub].

| Prodotto | Prezzo | Hosting | Licenza | Canali | Multi-agente | Memoria | Routine | Approvazioni | Maturità |
|---|---|---|---|---|---|---|---|---|---|
| ChatGPT Business/Ent. | € / trattativa | SaaS | proprietaria | web, app | Workspace Agents [non verificato] | sì | sì | sì | GA |
| AgentKit / Agent Builder | API | SaaS | proprietaria | ChatKit | grafo visuale | no | no | nodi di approvazione [non verificato] | **in chiusura 30/11/2026** [non verificato] |
| Dots | Pro 100 $ / Business Premium | SaaS + computer cloud | proprietaria | ChatGPT, Slack, Teams | uno o più "dot" | opaca | sì | 4 livelli + auto-review | appena lanciato; non su Pro UE/UK |
| open-duet | 0 | self-host | Apache-2.0 | (da verificare) | agenti con nome | sì [non verificato] | sì [non verificato] | gateway delle azioni | giovane |

---

## 3. (c) Open source self-host

Dati GitHub del 24/10/2026 [verificato: API GitHub]:

| Repo | Stelle | Licenza (da file) | Ultimo push | Note |
|---|---|---|---|---|
| openclaw/openclaw | 392.951 | MIT | 24/10 | agente personale 24/7 |
| NousResearch/hermes-agent | 256.766 | MIT | 24/10 | (rapporto a parte) |
| n8n-io/n8n | 208.496 | Sustainable Use License (fair-code) | 24/10 | |
| langgenius/dify | 159.434 | Apache 2.0 modificata | 24/10 | |
| open-webui/open-webui | 156.651 | "Open WebUI License" | 24/10 | |
| paperclipai/paperclip | 106.900 | MIT | 24/10 | |
| Mintplex-Labs/anything-llm | 67.516 | MIT | 24/10 | |
| microsoft/autogen | 61.549 | CC-BY-4.0 (documentazione; codice [non verificato]) | 16/10 | |
| crewAIInc/crewAI | 60.067 | MIT | 24/10 | |
| FlowiseAI/Flowise | 55.525 | Apache + parti enterprise | 13/08 | **archiviato** |
| LibreChat-AI/LibreChat | 46.256 | MIT | 24/10 | ex danny-avila |
| langchain-ai/langgraph | 43.834 | MIT | 24/10 | |
| khoj-ai/khoj | 37.810 | AGPL-3.0 | **02/08** | fermo da 12 settimane |
| letta-ai/letta | 25.244 | Apache-2.0 | 18/10 | |
| microsoft/agent-framework | 14.304 | MIT | 24/10 | |

Schede brevi:

- **OpenClaw**: gateway sempre acceso con WhatsApp (Baileys), Telegram e altri 30 canali; più agenti isolati nello stesso Gateway con workspace, identità, modello, strumenti e skill propri; squadra pronta (capo di gabinetto, ricercatore, scrittore, revisore) con passaggi e cancelli di approvazione; cinque tipi di schedule; chiamate con Twilio/Telnyx/Plivo; Google Meet, Teams, Zoom; "un Gateway è un solo dominio di fiducia", per più utenti serve un Gateway per tenant (`openclaw fleet`, sperimentale). WhatsApp via Baileys viola i termini di WhatsApp. Per un'azienda di 4 persone è un "dipendente" potente ma non un organigramma; Paperclip lo usa come runtime.
- **open-dots → open-duet**: vedi §2.
- **Paperclip**: "If OpenClaw is an employee, Paperclip is the company"; server Node con Postgres e UI React; organigramma con ruolo, capo, budget mensile e permessi, esportabile in SVG; delega a cascata dal "CEO" con strategia da approvare; bacheca task con checkout atomico; stadi di revisione imposti dal runtime "non dal prompt"; heartbeat e routine cron/webhook/API; budget per azienda, agente e progetto con avviso all'80% e stop al 100%; adattatori per Claude Code, Codex, Cursor, Gemini CLI, Hermes, OpenClaw e altri; connettori Slack, Discord, Telegram, Teams, GitHub, Gmail (lettura e bozze), Google Workspace, Asana, **Fireflies**; gateway degli strumenti "Allowed / Ask first / Off"; email per agente (AgentMail); segreti cifrati con riferimenti; memoria solo con connettori sperimentali (Mem0, Zep, Supermemory, Cognee, Honcho); nessuna gestione dei servizi su Windows (irrilevante sul server Linux). Avvio con `npx paperclipai onboard --yes`, nessun account richiesto [non verificato: contabo.com, rywalker.com]. Nato a marzo 2026, nessun team o finanziamento dichiarato [non verificato: fonti terze].
- **n8n**: automazione a nodi con funzioni AI native; Community Edition self-host gratuita senza limite di esecuzioni; cloud Starter ~20 €/mese (2.500 esecuzioni), Pro ~50 €/mese (10.000); Business self-host ~667 €/mese con SSO e Git [non verificato: jetadmin.io, sliplane.io]. La Sustainable Use License consente l'uso interno, non la rivendita come servizio [verificato: intestazione di LICENSE.md]. Forte per i flussi deterministici (post-call → Slack → HubSpot → email), debole come "chat fra agenti".
- **Dify**: piattaforma per workflow agentici e RAG con UI; Apache 2.0 modificata con condizioni (uso commerciale consentito anche come backend; limiti su multi-tenant e logo [non verificato nel dettaglio]) [verificato: intestazione di LICENSE].
- **Flowise**: **archiviato**; il README rimanda a "Future of Flowise" [verificato: README e API GitHub]. Da escludere.
- **CrewAI**: Crew (agenti con ruolo + task) e Flow (grafo con stato); executor ReAct; nessun gateway delle azioni; hook fail-open; memoria scritta in automatico da output non fidati; telemetria accesa; suite commerciale "AMP" con control plane e HITL via webhook. Libreria per programmatori Python, non piattaforma pronta.
- **LangGraph / LangChain Agents**: grafo con checkpoint a ogni passo, `interrupt()` per l'umano; il server con code, cron e webhook è un'immagine Docker chiusa (`langchain/langgraph-api`); niente sandbox, policy, budget, voce. Libreria, non organigramma.
- **Microsoft Agent Framework / AutoGen**: Agent Framework 1.0 GA il 3/4/2026 unisce Semantic Kernel e AutoGen; Semantic Kernel in manutenzione [non verificato: atlan.com]; AutoGen in manutenzione [non verificato: fonte in tedesco]. Repo MIT con 14.304 stelle [verificato: API GitHub]. Pensato per .NET/Python e Azure.
- **Letta (ex MemGPT)**: piattaforma per agenti con stato e memoria a blocchi (anche `read_only`) e "sleep-time agents"; Apache-2.0 [verificato: API GitHub]. Prezzo di Letta Cloud [non trovato].
- **Khoj**: "AI second brain" self-host su web e documenti; AGPL-3.0; nessun push dal 2/8/2026 [verificato: API GitHub]. Rischio di abbandono.
- **Open WebUI**: interfaccia chat self-host (Ollama, API OpenAI-compatibili); licenza propria derivata da BSD con clausole sul marchio [verificato: intestazione di LICENSE; dettaglio delle clausole non verificato]. Utile come chat interna sui modelli locali del server, non come orchestratore.
- **LibreChat**: clone di ChatGPT con agenti, MCP, skill e più fornitori (Anthropic incluso); MIT [verificato: API GitHub]. Come Open WebUI: interfaccia, non organigramma.
- **AnythingLLM**: app tutto-in-uno per RAG e agenti, desktop o Docker; MIT [verificato: API GitHub].

### Tabella di sintesi (c)

| Prodotto | Prezzo | Licenza | Canali | Multi-agente | Memoria | Routine | Approvazioni | Maturità |
|---|---|---|---|---|---|---|---|---|
| OpenClaw | 0 | MIT | 30+ (WhatsApp non ufficiale) | agenti isolati, squadra | file + struttura propria | 5 tipi | permessi a strati, pairing | molto usato, cambia ogni giorno |
| Paperclip | 0 | MIT | Slack, Teams, Telegram, Discord, email | **organigramma, deleghe, budget** | connettori sperimentali | cron, webhook, heartbeat | Ask first, revisori, Board | 8 mesi, molto attivo |
| n8n | 0 (CE) / € cloud | fair-code | via nodi | debole | via nodi | sì | nodi di attesa [non verificato] | maturo |
| Dify | 0 / € cloud | Apache modificata | API, web | workflow | RAG integrato | sì | [non verificato] | maturo |
| Flowise | — | — | — | — | — | — | — | **archiviato** |
| CrewAI | 0 / AMP a pagamento | MIT | da costruire | ruoli + task | automatica (rischiosa) | Flow | HITL via webhook (AMP) | maturo come libreria |
| LangGraph | 0 / piattaforma a pagamento | MIT | da costruire | grafo | checkpoint | server chiuso | `interrupt()` | maturo come libreria |
| MS Agent Framework | 0 | MIT | da costruire | sì | sì [non verificato] | [non verificato] | [non verificato] | GA 1.0 [non verificato] |
| Letta | 0 / cloud | Apache-2.0 | API | sì [non verificato] | **punto di forza** | sleep-time | [non verificato] | maturo |
| Khoj | 0 | AGPL-3.0 | web, app | no | sì | sì [non verificato] | no | fermo da agosto |
| Open WebUI / LibreChat / AnythingLLM | 0 | propria / MIT / MIT | web | agenti semplici | RAG | limitate | no | maturi come chat |

---

## 4. (d) SaaS agentici

- **Lindy**: agenti "dipendenti" con trigger e integrazioni; Plus ~30 $/utente/mese, Pro ~100 $, Max ~200 $ a crediti, nessun piano gratuito permanente [non verificato: nocode.mba, tinycommand.com; una fonte è il blog di Lindy]. Hosting SaaS USA [non verificato].
- **Relevance AI**: "AI workforce" con agenti e strumenti no-code; Free, Pro ~19-29 $/mese, Team ~234-349 $/mese, Enterprise [non verificato: fonti in conflitto].
- **Zapier Agents**: agenti sopra le 8.000+ integrazioni di Zapier; gratis 400 attività/mese, add-on Pro 33 $/mese per 1.500, piani Zapier a parte [non verificato: fonti terze].
- **Make**: scenari visuali con agenti AI su ogni piano a pagamento; Free 1.000 crediti/mese, Core da ~9-12 $/mese [non verificato: fonti terze]. Azienda europea (Praga) [non verificato].
- **Muse**: l'unico prodotto con questo nome trovato è **Muse di Meta**, agente personale lanciato l'8/9/2026, con "Muse for Small Business" il 29/9/2026 e piani Power 20 $/mese e Maximum 100 $/mese [non verificato: cnbc.com, tech-insider.org]. Se Alberto intendeva un altro prodotto, serve il nome o il sito.
- **Dots**: vedi §2.

| Prodotto | Prezzo | Hosting | Canali | Multi-agente | Memoria | Routine | Approvazioni | Maturità |
|---|---|---|---|---|---|---|---|---|
| Lindy | €€ a crediti | SaaS | email, Slack, telefono [non verificato] | sì | sì | sì | sì [non verificato] | maturo |
| Relevance AI | € / €€€ | SaaS | API, web | sì | sì | sì | sì [non verificato] | maturo |
| Zapier Agents | 0 / € + Zapier | SaaS | via Zapier | limitato | limitata | sì | [non verificato] | maturo |
| Make | 0 / € | SaaS (UE [non verificato]) | via moduli | limitato | limitata | sì | [non verificato] | maturo |
| Meta Muse | € / €€ | SaaS | app Meta | no | sì | sì | [non verificato] | nuovo |

Per tutti: nessun self-host, dati su server del fornitore, prezzi a crediti che crescono con gli agenti. Utili come prova rapida, non come base con il server già comprato.

---

## 5. (e) Infrastruttura per agenti durevoli

- **Vercel eve**: framework open source per agenti, presentato il 17/6/2026, **public preview**; un agente è una cartella di file; sessioni durevoli che riprendono dopo crash o deploy (Workflow SDK); approvazioni su qualsiasi azione; subagent con sandbox e contesto propri; schedule cron; canali "Slack, Discord, Teams, Telegram, Twilio, GitHub, and Linear included"; esempi con `anthropic/claude-opus-4.8` via AI Gateway; **"At launch eve deploys to Vercel, with support for other platforms on the way"**; nessuna memoria dedicata, solo `compaction` [verificato: vercel.com/blog/introducing-eve]. Repo `vercel/eve` Apache-2.0, 5.666 stelle [verificato: API GitHub]. I passi interrotti possono rigirare: gli effetti esterni vanno resi idempotenti [non verificato: guida terza]. Costo: piano Vercel più uso di Functions, Workflows e Sandbox [non verificato].
- **Temporal**: motore di workflow durevoli, server MIT self-host [verificato: API GitHub]; Temporal Cloud a consumo con piani Essentials da 100 $/mese e Business da 500 $/mese, azioni a 50 $ per milione, 1.000 $ di crediti per 90 giorni ai nuovi account [non verificato: snippet di temporal.io/pricing.md]. Robusto ma pesante per 4 persone.
- **Inngest**: funzioni a passi durevoli ed eventi; licenza **SSPL con licenza futura Apache 2.0** [verificato: intestazione di LICENSE.md] (una fonte terza scrive "Apache 2.0" per il self-host: è impreciso); cloud gratis fino a 50.000 passi/mese, poi da 20-99 $/mese secondo la fonte [non verificato: fonti terze in conflitto].
- Alternativa senza infrastruttura nuova: **Postgres sul server + coda durevole** (pg-boss/pgmq) o le routine di Paperclip, che hanno già coda durevole con coalescenza.

| Prodotto | Prezzo | Hosting | Licenza | Canali | Durabilità | Routine | Approvazioni | Maturità |
|---|---|---|---|---|---|---|---|---|
| Vercel eve | piano Vercel + uso | **solo Vercel al lancio** | Apache-2.0 | 7 inclusi | sì | cron | sì | preview |
| Temporal | 0 self-host / €€€ cloud | entrambi | MIT | no | **eccellente** | sì | via segnali | maturo |
| Inngest | 0 / € | entrambi | SSPL→Apache | no | sì | sì | `waitForEvent` [non verificato] | maturo |

---

## 6. (f) Memoria e knowledge

La visione prevede due basi: una relazionale (Notion) e una vettoriale [verificato: `00-visione-funzionalita.md` A2-A3].

- **Notion AI**: Business circa 20 $/membro/mese annuale con Notion AI, Agent, AI Meeting Notes ed Enterprise Search inclusi; i Custom Agents consumano crediti a 10 $ per 1.000 crediti mensili oltre al piano [non verificato: breeze.pm, krater.ai, coworker.ai]. SerSan ha già il connettore MCP di Notion.
- **Obsidian**: note Markdown in locale, gratis anche per uso aziendale; Sync e Publish a pagamento [non verificato]. Ottimo per un vault versionato con git, debole per più persone che scrivono insieme.
- **AFFiNE**: alternativa self-host a Notion/Miro; licenza mista (parti backend con licenza propria) [verificato: intestazione di LICENSE].
- **Outline**: wiki di team self-host; **BSL 1.1** con divieto di offrirlo come "Document Service" a terzi, uso interno ammesso [verificato: intestazione di LICENSE].
- **Mem0**: livello di memoria per agenti (estrazione e consolidamento dei fatti); Apache-2.0, 67.750 stelle [verificato: API GitHub]; usato anche da Pipecat per la memoria fra chiamate. Prezzo del cloud [non trovato].
- **Graphiti / Zep**: grafo di conoscenza temporale per agenti; Graphiti Apache-2.0, 32.180 stelle [verificato: API GitHub]; Zep cloud con piano gratuito a 10.000 crediti/mese, Flex 125 $/mese e Flex Plus 375 $/mese [non verificato: pricingsaas.com].
- **pgvector**: estensione vettoriale di Postgres, licenza PostgreSQL [verificato: intestazione di LICENSE]. Una sola base (Postgres) fa da relazionale e da vettoriale, ed è la stessa che usa Paperclip.
- **Qdrant**: database vettoriale Apache-2.0, 35.227 stelle [verificato: API GitHub]; cloud con piccolo piano gratuito [non verificato].
- **Weaviate**: BSD-3 fuori dalla cartella `wl`, "Weaviate License" dentro [verificato: intestazione di LICENSE].

| Prodotto | Prezzo | Hosting | Licenza | Ruolo | Maturità |
|---|---|---|---|---|---|
| Notion AI | € a membro + crediti agenti | SaaS | proprietaria | relazionale + agenti | maturo |
| Obsidian | 0 / € sync | locale | proprietaria gratuita | note | maturo |
| AFFiNE | 0 / € cloud | entrambi | mista | wiki/whiteboard | maturo |
| Outline | 0 / € cloud | entrambi | BSL 1.1 | wiki | maturo |
| Mem0 | 0 / cloud [non trovato] | entrambi | Apache-2.0 | memoria agenti | maturo |
| Graphiti / Zep | 0 / €€-€€€ | entrambi | Apache-2.0 / SaaS | grafo temporale | maturo |
| pgvector | 0 | self-host | PostgreSQL | vettoriale in Postgres | maturo |
| Qdrant | 0 / cloud | entrambi | Apache-2.0 | vettoriale | maturo |
| Weaviate | 0 / cloud | entrambi | BSD-3 + propria | vettoriale | maturo |

---

## 7. (g) Trascrizione delle riunioni

- **Fireflies** (citato nella visione): Pro ~10 $/posto/mese annuale (18 $ mensile), Business 19 $, Enterprise 39 $; API su tutti i piani [non verificato: confronti terzi]. Paperclip ha già un connettore Fireflies. Per la visione la qualità dei riassunti è bassa e vanno rifatti con regole proprie [verificato: `00-visione-funzionalita.md` C6].
- **Fathom** (Alberto ha un link sul desktop): registrazioni illimitate nel piano gratuito; Premium ~16 $, Team 15 $ (minimo 2), Business 25 $; API pubblica e MCP [non verificato: fonti terze].
- **tl;dv**: Pro ~18 $/utente/mese, Business ~59 $ [non verificato]; API [non trovato].
- **Otter**: Pro ~8,33 $, Business ~20 $ annuale; gratis 300 minuti/mese [non verificato]; API [non trovato].
- **Granola**: prende appunti dall'audio del computer senza bot nella call [non verificato]; Business 14 $, Enterprise 35 $; gratis 25 riunioni; API solo Enterprise secondo una fonte, MCP su tutti i piani secondo un'altra [non verificato: fonti in conflitto, una è il blog di Granola].
- **Recall.ai**: API di bot di riunione (Meet, Teams, Zoom) per costruire il proprio Fireflies; 0,50 $/ora di registrazione a consumo senza canone (prima 0,70 $), trascrizione integrata 0,15 $/ora, prime 5 ore gratis, conservazione gratuita 7 giorni [non verificato: snippet di recall.ai/blog e recall.ai/pricing, pagine non aperte].
- **Self-host**: **Vexa** (API di trascrizione open source per Meet, Teams e Zoom, bot che entra da solo; Apache-2.0, 2.906 stelle) [verificato: API GitHub]; **Meetily** (assistente "privacy first" con Parakeet/Whisper dal vivo e diarizzazione; MIT, 32.124 stelle; ora `Zackriya-Solutions/meetily`) [verificato: API GitHub]; **Attendee** ("The universal Meeting Bot API", **Elastic License 2.0**, 770 stelle) [verificato: API GitHub e LICENSE]. La trascrizione Whisper può girare sulla Quadro RTX 4000 da 8 GB del server con un modello quantizzato [non verificato: da provare].

| Prodotto | Prezzo | Hosting | Bot nella call | API / MCP | Maturità |
|---|---|---|---|---|---|
| Fireflies | € a posto | SaaS | sì | API tutti i piani [non verificato] | maturo |
| Fathom | 0 / € | SaaS | sì | API + MCP [non verificato] | maturo |
| tl;dv | € / €€ | SaaS | sì | [non trovato] | maturo |
| Otter | 0 / € | SaaS | sì | [non trovato] | maturo |
| Granola | 0 / € | SaaS + app | no [non verificato] | MCP; API Enterprise [non verificato] | maturo |
| Recall.ai | 0,50 $/h + 0,15 $/h | SaaS (API) | sì | è un'API | maturo |
| Vexa | 0 | self-host | sì | API propria | giovane, attivo |
| Meetily | 0 | locale | no (audio locale) [non verificato] | [non verificato] | attivo |
| Attendee | 0 | self-host | sì | API propria | giovane, ELv2 |

---

## 8. (h) Agente vocale ("Andrea") e numeri italiani

- **ElevenLabs Agents**: 0,08 $/minuto, con LLM e telefonia fatturati a parte; tariffa "burst" 0,16 $ oltre la concorrenza del piano; 15 minuti gratis [non verificato: getmacha.com, a8gent.com]. SerSan ha già ElevenLabs e la voce clonata nasce lì.
- **Vapi**: 0,05 $/minuto di piattaforma più costi dei fornitori a prezzo di costo; totale stimato 0,08-0,33 $/minuto [non verificato: fonti in conflitto].
- **Retell**: 0,055 $/minuto di infrastruttura più LLM, TTS e telefonia; slot di concorrenza 8 $/mese, numero verificato 10 $/mese [non verificato].
- **Bland**: tariffa unica 0,11-0,14 $/minuto secondo il piano, trasferimenti a parte [non verificato].
- **LiveKit Agents**: Apache-2.0 per il codice, "LiveKit Model License" per i modelli di fine turno; serve un server LiveKit (self-host o cloud); fine turno, interruzioni, telefonia; nessuna approvazione né memoria propria.
- **Pipecat**: BSD-2; pipeline a frame; Smart Turn v3.2 su CPU con italiano; telefonia con Twilio, Telnyx, Plivo, Exotel, Genesys, Vonage; chiamate in uscita, segreteria, trasferimento SIP; memoria via Mem0. Self-host sul server, voce da ElevenLabs.
- **Twilio / Telnyx per numeri italiani**: Twilio chiede per le aziende prova di indirizzo locale, partita IVA o registrazione, documento del rappresentante; prefisso mobile +393; niente chiamate d'emergenza [non verificato: snippet di twilio.com/guidelines/it/regulatory e /voice]. Requisiti Telnyx per l'Italia [non trovato]. AGCOM il 27/4/2026 ha approvato i "numeri brevi" per identificare i chiamanti legittimi, con obblighi per il telemarketing ancora da definire [non verificato: mobileecosystemforum.com]. Da valutare con un legale: Registro delle Opposizioni, consenso del collega per la voce clonata, obbligo di dire che si parla con un'AI [non verificato].

| Prodotto | Prezzo indicativo | Hosting | Licenza | Telefonia | Maturità |
|---|---|---|---|---|---|
| ElevenLabs Agents | 0,08 $/min + LLM + linea | SaaS | proprietaria | Twilio/SIP [non verificato] | maturo |
| Vapi | 0,05 $/min + componenti | SaaS | proprietaria | sì | maturo |
| Retell | 0,055 $/min + componenti | SaaS | proprietaria | sì | maturo |
| Bland | 0,11-0,14 $/min tutto incluso | SaaS | proprietaria | sì | maturo |
| LiveKit Agents | 0 + server | self-host o cloud | Apache-2.0 + licenza modelli | SIP | maturo |
| Pipecat | 0 + fornitori | self-host o Pipecat Cloud [non verificato] | BSD-2 | 6 operatori | maturo |
| Twilio / Telnyx | a minuto + numero | SaaS | — | numeri IT con documenti | maturo |

---

## 9. Tabella di sintesi generale (cosa copre la visione di Alberto)

Righe: i pezzi della visione; colonne: chi li dà già fatti. "Sì" = funzione pronta; "parz." = va completata; "—" = assente.

| Pezzo della visione | Claude Team + Tag + Managed Agents | Paperclip | n8n | eve + Chat SDK | OpenClaw | SaaS (Lindy & c.) |
|---|---|---|---|---|---|---|
| Organigramma con ruoli e capi | — | **sì** | — | parz. (subagent) | parz. (squadre) | parz. |
| Chat condivisa fra agenti | parz. (canale Slack per @Claude) | parz. (commenti task, chat agente) | — | parz. | parz. | parz. |
| Budget/token policy per agente | parz. (limiti per canale e org) | **sì** (80%/100%) | — | — | parz. | a crediti |
| Approvazioni umane | parz. (permessi, log) | **sì** (Ask first, revisori) | parz. | **sì** | sì | parz. |
| Routine (debrief del mattino) | sì (Cowork, cron Managed Agents) | sì | sì | sì | sì | sì |
| Post-call → Slack/HubSpot/mail | parz. (connettori) | parz. (Fireflies, Slack, Gmail) | **sì** | parz. | parz. | sì |
| Memoria relazionale + vettoriale | parz. (Projects, memoria di canale) | parz. (connettori sperimentali) | parz. | — | parz. | parz. |
| Bot di riunione | — | parz. (Fireflies) | via nodi | — | parz. (Meet/Teams/Zoom) | parz. |
| Agente vocale | — | — | via API | Twilio | Twilio/Telnyx | parz. |
| Gira sul server di SerSan | sandbox Managed Agents | **sì** | **sì** | **no al lancio** | sì | no |

---

## 10. Combinazioni realistiche per SerSan

Premessa comune: SerSan ha 5 account Claude Team, 800 $/mese di crediti API, il server DL380 (160 GB di RAM, Quadro RTX 4000 da 8 GB), ElevenLabs, moda.app e molti connettori MCP; SersanOutreach passa da Azure al server [verificato: richiesta di Alberto; `01-sersanoutreach.md`]. Gli agenti che girano 24 ore su 24 per l'azienda vanno pagati con **API key** (crediti), non con gli abbonamenti, perché i limiti dei piani "presumono un uso individuale ordinario".

### A. "Claude-first gestito": Claude Team + Claude Tag + Managed Agents

- **Pezzi**: Claude Tag in Slack con un canale per cliente o per funzione (memoria per canale, proattività, limiti di spesa); Managed Agents per i lavori lunghi e pianificati (debrief delle 5:30, post-call, brief pre-meeting) con **sandbox self-host sul server**; connettori MCP (Notion, HubSpot se presente, Google Workspace); Dashboards per la pipeline; Fireflies o Fathom per le riunioni; ElevenLabs Agents per "Andrea".
- **Costo**: posti Team già pagati; Claude Tag a consumo (credito di lancio forse non per 5 posti); Managed Agents 0,08 $/h + token sugli 800 $; Fireflies ~19 $/posto; ElevenLabs a minuto.
- **Cosa manca**: nessun **organigramma** né bacheca dei task fra agenti; nessuna "stanza" in cui gli agenti si parlano fuori da Slack; budget per agente solo come limiti per canale; memoria di canale non condivisa (voluto, ma la visione chiede il contrario per i dati aziendali); Managed Agents in beta e senza ZDR; Channels in research preview e da abilitare dall'Owner; i "Projects con coordinatore" **non risultano**; dipendenza totale da un fornitore che cambia le regole spesso (aprile e giugno 2026).

### B. "Paperclip sul server, Claude come motore" (la più completa)

- **Pezzi**: Paperclip in Docker sul DL380 come piano di controllo (organigramma, budget, routine, approvazioni, inbox dell'attenzione); runtime degli agenti = Claude Code / Agent SDK con API key, più Hermes come adattatore se il suo rapporto lo conferma; Postgres + pgvector come seconda memoria (eventualmente Graphiti per il grafo delle relazioni); Notion come base delle regole scritte; bot di riunione con Recall.ai (a consumo) o Vexa self-host; Slack come canale umano (connettore di Paperclip) e Claude Tag per le domande al volo; SersanOutreach collegato via API o MCP; "Andrea" con Pipecat sul server + ElevenLabs + numero Twilio italiano.
- **Costo**: 0 di licenze per Paperclip, pgvector, Vexa, Pipecat; consumo Claude sugli 800 $; Recall.ai 0,65 $/ora di riunione se non si usa Vexa; Twilio a minuto.
- **Cosa manca**: maturità (8 mesi, nessun team dichiarato, pipeline e status card ancora sperimentali) [non verificato: team]; memoria solo con connettori sperimentali, quindi la base a due database va costruita; nessuna voce; ogni connettore aziendale (HubSpot, CRM proprio) va scritto o preso da n8n; sicurezza da fare in casa (account separati, segreti, log immutabili); serve qualcuno che segua gli aggiornamenti di un repo molto attivo.

### C. "Flussi deterministici prima": n8n Community + Claude API

- **Pezzi**: n8n self-host sul server per i flussi fissi della visione (Fireflies/Fathom webhook → riassunto Claude con le regole in Notion → messaggio nel canale Slack del cliente → opportunità su HubSpot → bozza della mail → to-do); routine per il debrief del mattino; pgvector per la ricerca; Claude Tag per la parte conversazionale.
- **Costo**: n8n CE gratuito; consumo Claude; strumenti di riunione.
- **Cosa manca**: nessun organigramma, nessuna chat fra agenti, nessun budget per agente; la Sustainable Use License non permette di rivendere i flussi come servizio ai clienti di SerSan; è il modo più rapido per i primi risultati (post-call, debrief) ma non è il sistema multi-agente completo della visione.

### D. "Su misura con Vercel": eve + Chat SDK + Claude API

- **Pezzi**: agenti come cartelle di file in eve (approvazioni, subagent, schedule, canali Slack/Teams/Telegram/Twilio inclusi), Chat SDK per i canali, Claude via AI Gateway, Supabase/Postgres per la memoria; SerSan ha già i connettori Vercel e Supabase.
- **Costo**: piano Vercel a pagamento più uso; consumo Claude.
- **Cosa manca**: al lancio eve si distribuisce **solo su Vercel** ("support for other platforms on the way"), quindi il server non serve; public preview con API che possono cambiare; nessuna memoria né organigramma pronti; più codice da scrivere di B.

### Confronto rapido

| | A Claude-first | B Paperclip | C n8n | D eve |
|---|---|---|---|---|
| Organigramma e budget per agente | — | **sì** | — | — |
| Usa il server | in parte (sandbox) | **sì** | **sì** | no |
| Tempo al primo risultato | breve | medio | **breve** | medio-lungo |
| Rischio di maturità | beta Anthropic | progetto giovane | basso | preview |
| Lock-in | Anthropic | basso (MIT) | basso (uso interno) | Vercel |
| Cosa resta da costruire | organigramma, memoria condivisa | memoria, voce, connettori | quasi tutto l'agentico | quasi tutto |

Lettura consigliata per i CEO: B come ossatura, C per i flussi fissi del primo mese, A per la parte che vive in Slack. Le domande di budget sono: consumo API oltre gli 800 $, Recall.ai o Vexa, minuti vocali e numero italiano, eventuale Notion Business.

---

## 11. Domande aperte

1. Dove è stata vista la funzione "Projects con coordinatore e thread" di Claude? Non risulta nelle fonti ufficiali lette oggi.
2. Gli 800 $/mese sono i crediti API del piano Team (dal 7/10) o un credito del bundle startup? Cambia il budget reale.
3. SerSan ha diritto al credito di lancio di Claude Tag con 5 posti?
4. "Muse" è Meta Muse o un altro prodotto?
5. Dots è disponibile per un'azienda con sede a Londra su Business Premium o Enterprise?
6. Per "Andrea": base legale per la voce clonata del collega e per le chiamate in uscita in Italia (Registro delle Opposizioni, numeri brevi AGCOM, trasparenza AI).
7. HubSpot è già in uso o il CRM resta SersanOutreach? Decide quali connettori scrivere.
8. Quanti minuti di riunione al mese? Decide tra Fireflies/Fathom, Recall.ai e Vexa self-host.

---

## 12. Fonti (rilevazione 24/10/2026)

Ufficiali, lette oggi:
- https://support.claude.com/en/articles/12138966-release-notes
- https://www.anthropic.com/news/introducing-claude-tag
- https://platform.claude.com/docs/en/managed-agents/overview
- https://platform.claude.com/docs/en/about-claude/pricing
- https://code.claude.com/docs/en/channels
- https://vercel.com/blog/introducing-eve
- https://chat-sdk.dev/
- https://api.github.com/repos/{paperclipai/paperclip, openclaw/openclaw, Anil-matcha/open-duet, n8n-io/n8n, langgenius/dify, FlowiseAI/Flowise, crewAIInc/crewAI, langchain-ai/langgraph, microsoft/agent-framework, microsoft/autogen, letta-ai/letta, khoj-ai/khoj, open-webui/open-webui, LibreChat-AI/LibreChat, Mintplex-Labs/anything-llm, vercel/eve, vercel/chat, temporalio/temporal, inngest/inngest, toeverything/AFFiNE, outline/outline, mem0ai/mem0, getzep/graphiti, pgvector/pgvector, qdrant/qdrant, weaviate/weaviate, Zackriya-Solutions/meetily, Vexa-ai/vexa, attendee-labs/attendee, livekit/agents, pipecat-ai/pipecat, NousResearch/hermes-agent} e relativi `/license`
- https://raw.githubusercontent.com/FlowiseAI/Flowise/main/README.md

Locali:
- `C:/Users/alber/SerSan-AgentOS/ricerca/00-visione-funzionalita.md`

Terze parti (dati [non verificato]):
- https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/ ; https://felloai.com/openai-dots/ ; https://www.reworked.co/ai-news/the-biggest-announcements-from-openai-devday-dots-agents-new-500-plan/ ; https://www.aiagentslibrary.com/blog/openai-devday-2026/
- https://www.therundown.ai/tools/agent-builder ; https://reflektlab.ai/blog/openai-agent-builder/ ; https://www.marktechpost.com/2025/10/06/openai-debuts-agent-builder-and-agentkit-a-visual-first-stack-for-building-deploying-and-evaluating-ai-agents/
- https://www.madewell.ai/blog/chatgpt-business-pricing ; https://vantagepoint.io/blog/ai/claude-plans-tiers-explained-business
- https://the-decoder.com/claude-can-now-generate-animated-explainer-videos-and-live-data-dashboards-from-text-prompts/ ; https://www.testingcatalog.com/claude-launches-dashboards-and-motion-in-beta/ ; https://www.techfinitive.com/introducing-slacks-newest-team-member-claude-tag/
- https://contabo.com/blog/what-is-paperclip-ai/ ; https://rywalker.com/research/paperclip
- https://www.infoq.com/news/2026/06/vercel-eve-agents/ ; https://atlan.com/know/ai-agent/microsoft/semantic-kernel/
- https://www.cnbc.com/2026/09/29/meta-launches-muse-for-small-business-zuckerberg-pushes-enterprise-ai.html ; https://tech-insider.org/meta-muse-personal-ai-agent-launch-2026/
- https://www.nocode.mba/articles/best-ai-agent-builders-2026 ; https://tinycommand.com/ai-agents/lindy-ai-alternatives ; https://www.hyperclapper.com/blog-posts/relevance-ai-pricing-review-2026
- https://www.jetadmin.io/blog/n8n-pricing/ ; https://sliplane.io/blog/n8n-pricing
- https://temporal.io/pricing.md (snippet) ; https://automationatlas.io/answers/inngest-pricing-explained-2026/
- https://www.breeze.pm/articles/notion-ai-pricing ; https://pricingsaas.com/companies/getzep/diffs/2026W27
- https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter ; https://thenotetakers.com/otter-vs-fireflies-vs-fathom-vs-granola ; https://recall.ai/blog/new-recall-ai-pricing-for-2026 (snippet) ; https://www.recall.ai/pricing (snippet)
- https://www.getmacha.com/blog/elevenlabs-agents-pricing-explained ; https://stackbinary.io/insights/voice-ai-pricing-per-minute-2026 ; https://texttolab.com/blog/voice-agent-pricing
- https://www.twilio.com/en-us/guidelines/it/regulatory (snippet) ; https://mobileecosystemforum.com/2026/05/11/agcom-moves-to-short-calling-numbers-a-clear-signal-on-the-future-of-voice-trust-in-italy/
