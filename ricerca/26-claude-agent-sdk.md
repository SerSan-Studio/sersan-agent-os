# 26 · Claude Agent SDK: il motore degli agenti sul nostro server

**Data di rilevazione:** 25/10/2026.
**Per:** Michele Sanna (CPTO), Alberto Tuveri e Mattia Scattu; il paragrafo «In breve» vale anche per Alessandro Serratt.
**La domanda di Michele:** l'hardware è già preso e tutto il resto deve stare in casa. Possiamo costruire gli agenti con l'Agent SDK di Claude ed evitare Hermes? Hermes non è escluso a priori: va confrontato.
**Vincolo fisso:** il board dell'infrastruttura di Michele (`allegati/infra/`). In cloud restano solo M365/Entra ID, Claude Team, API Anthropic dietro LiteLLM, Cloudflare, GitHub, Supabase, Vercel, Jira, Instantly e un S3 facoltativo. Azure esce [verificato: B].
**Metodo.** Documentazione ufficiale Anthropic letta il 25/10/2026 nella versione Markdown (code.claude.com e platform.claude.com). Context7 con le librerie `/websites/code_claude_en_agent-sdk` e `/websites/litellm_ai`. Registri npm e PyPI, API di GitHub, documentazione di LiteLLM e n8n. File del progetto 00-24.
**Etichette.** [verificato: codice] = letto nella fonte con quel codice (elenco nel §13). [non verificato] = stima, proposta o voce di terzi. gp = giorni-persona. Prezzi in dollari, IVA esclusa, rilevati il 25/10/2026.

---

## In breve

L'Agent SDK è Claude Code usato come libreria, in TypeScript e in Python. Dà il ciclo dell'agente, gli strumenti, le sessioni che si riprendono, i sottoagenti, gli hook che approvano o bloccano, i permessi, i server MCP, le skill, i plugin, l'output a schema e una stima dei costi con un tetto di spesa. Non dà gli orari, una bacheca dei compiti fra agenti, profili con nome che vivono nel tempo, una chat di gruppo né una memoria condivisa. Quasi tutto ciò che manca lo copre lo stack già previsto da Michele: n8n per orari e ingressi, LiteLLM per chiavi, budget e registri, i server MCP con PostgreSQL e Qdrant per la memoria. Restano da scrivere quattro pezzi nostri: il runner delle sessioni, il registro dei profili, la bacheca con il freno ai giri e l'adattatore verso la chat delle persone. **Il consiglio è costruire il motore sull'SDK in TypeScript e non adottare Hermes.** La stima è di circa 21 gp di base e 27 gp con la riserva del 30 %, cioè 4-5 settimane con Alberto e Mattia. Il Cancello resta un lavoro a parte, già stimato in circa 21 gp.

I punti che contano:

1. **Versioni di oggi.** SDK TypeScript 0.3.310 (23/10/2026) e Python 0.2.174 (24/10/2026). Ogni SDK porta dentro il suo binario di Claude Code (oggi 2.1.310). Esce una versione quasi ogni giorno: va fissata e aggiornata a ritmo nostro [verificato: R1, R2, R4, D2].
2. **Approvazioni native.** L'hook `PreToolUse` può dire consenti, nega, chiedi o rimanda. Con «rimanda» il turno si chiude e la sessione riparte ore dopo, quando una persona ha deciso. È esattamente la forma del Cancello [verificato: D7, D8, D9].
3. **Ospitarlo.** Un processo per sessione, circa 1 GiB di RAM, 1 CPU e 5 GiB di disco per agente come punto di partenza. Le sessioni si salvano in PostgreSQL con un adattatore di esempio ufficiale [verificato: D2, D5].
4. **Dietro LiteLLM.** Basta `ANTHROPIC_BASE_URL` più una chiave virtuale di LiteLLM. Anthropic stessa cita LiteLLM come proxy che inietta le chiavi. Il gateway deve inoltrare intatti gli header `anthropic-beta` e `anthropic-version`: su questo punto LiteLLM ha una correzione ancora aperta, quindi va provato [verificato: D3, D21, L1, L4].
5. **Autenticazione.** Gli agenti usano la chiave API, mai i posti Claude Team: il login degli abbonamenti serve all'uso ordinario delle app di Anthropic. L'uso interno con la nostra chiave, fatturato a noi, è consentito [verificato: D1, D23].
6. **`claude -p`.** È lo stesso motore da riga di comando, utile per lavori singoli lanciati da n8n o dai runner GitHub. Per decine di agenti l'SDK è più adatto [verificato: D19; proposta].
7. **ACP e Buzz.** L'adattatore `claude-agent-acp` (Apache-2.0, versione 0.95.0 del 23/10) porta gli agenti Claude dentro Buzz. Però in Buzz c'è un difetto aperto dal 5/9: le risposte di Claude possono sparire senza errore. Buzz resta un pilota interno [verificato: A1, A3].
8. **Hermes.** Nel nuovo quadro i suoi vantaggi si riducono. Slack e Notion non sono più nel cloud ammesso; gli orari li fa n8n; il Cancello si aggancia all'SDK in modo nativo, a Hermes no. Restano a Hermes i profili e la bacheca, che con l'SDK costano circa 4,5 gp [verificato: B, 10 §4; stima nostra].

---

## 1. Che cos'è oggi l'Agent SDK

### 1.1 Pacchetti e versioni

| Pacchetto | Versione al 25/10/2026 | Uscita | Licenza | Fonte |
|---|---|---|---|---|
| `@anthropic-ai/claude-agent-sdk` (TypeScript) | 0.3.310 | 23/10/2026 | Commercial Terms di Anthropic | [verificato: R1, R3] |
| `claude-agent-sdk` (Python) | 0.2.174 | 24/10/2026 | involucro MIT; il binario di Claude Code incluso resta sotto i Commercial Terms | [verificato: R2, R3, D1] |
| Claude Code (binario incluso nell'SDK) | 2.1.310 (canale stable: 2.1.308) | 23/10/2026 | Commercial Terms | [verificato: R4] |
| `@agentclientprotocol/claude-agent-acp` | 0.95.0, costruito sull'SDK 0.3.309 | 23/10/2026 | Apache-2.0 | [verificato: A1] |

- **Come funziona.** Quando il codice chiama `query()`, l'SDK avvia un processo `claude` separato e ci parla su stdin/stdout. Quel processo possiede la shell, la cartella di lavoro e le trascrizioni in JSONL. Una sessione è un processo [verificato: D2].
- **Il binario va con l'SDK.** La versione di Claude Code è fissata da quella dell'SDK: aggiornare l'SDK aggiorna anche Claude Code. Anthropic consiglia di prendere subito le patch e di leggere il changelog prima di ogni versione minore [verificato: D2].
- **Ritmo.** Il pacchetto TypeScript ha 333 versioni dal 27/9/2025, otto solo fra il 18 e il 23/10/2026 [verificato: R1]. È un bersaglio mobile: per esempio dalla 2.1.302 un'app senza modalità esplicita parte in `default` e nega ogni strumento che nessuna regola, hook o callback approva [verificato: D6].
- **Requisiti.** Node.js 18 o più per TypeScript, Python 3.10 o più per Python. Il binario è precompilato per Linux x64 e arm64, anche in versione musl [verificato: D2, R1].
- **Attività dei repository al 25/10/2026.** TypeScript 1.832 stelle e 238 issue e PR aperte; Python 8.346 stelle e 589 aperte [verificato: R3].

### 1.2 Dove si colloca rispetto agli altri strumenti Anthropic

| Strumento | Chi fa girare l'agente | Per noi |
|---|---|---|
| **Agent SDK** | noi, in un processo nostro | il motore degli agenti sul DL380 |
| **Claude Code CLI** (`claude -p`) | noi, da riga di comando | lavori singoli da n8n, prove, CI sui runner in casa |
| **Client SDK** (Messages API) | noi; il ciclo degli strumenti lo scriviamo noi | le chiamate semplici: riassunti, estrazioni, classificazioni |
| **Managed Agents** | Anthropic, nel suo cloud; gli strumenti possono girare in una sandbox nostra | escluso: il ciclo dell'agente e le sessioni starebbero da Anthropic, contro la regola «tutto in casa» |

[verificato: D1, D2; giudizio su Managed Agents: proposta nostra]

### 1.3 TypeScript o Python

- **TypeScript ha più hook.** Python non ha, fra gli altri, `SessionStart`, `SessionEnd`, `StopFailure`, `PostCompact`, `PreModelSwitch`, `TaskCreated` e `TaskCompleted` [verificato: D7].
- **TypeScript può preavviare i processi** con `startup()` e `prewarm()`, così il primo messaggio non paga l'avvio a freddo [verificato: D18].
- **Python tiene aperta una conversazione** con `ClaudeSDKClient` [verificato: D2].
- **Consiglio: TypeScript.** Più hook e avvio caldo.

---

## 2. Le funzioni, una per una

| Funzione | Cosa fa oggi | Come la usiamo | Fonte |
|---|---|---|---|
| **Ciclo e strumenti** | Gli strumenti di Claude Code: leggere, scrivere, modificare file, Bash, ricerca, WebFetch, WebSearch, sottoagenti. Con l'opzione `tools` si sceglie l'elenco. `effort` va da `low` a `max` | Ogni profilo ha solo gli strumenti che gli servono; `effort` basso per raccolta e smistamento | [verificato: D16, D18] |
| **Sessioni** | Continua, riprendi per ID, biforca (`forkSession`). L'ID arriva nel primo messaggio. Trascrizioni in `~/.claude/projects/`. `persistSession: false` non salva nulla | Un thread di chat = una sessione ripresa per ID. I lavori su dati sensibili non lasciano trascrizioni | [verificato: D4, D18] |
| **Sessioni su un database** | Interfaccia `SessionStore` con adattatori di esempio ufficiali per S3, Redis e **Postgres**, più una suite di test di conformità. La copia è «al meglio»: se fallisce, arriva un messaggio `mirror_error` e la sessione continua | Trascrizioni su PostgreSQL 16 (VLAN 40); avviso su `mirror_error` | [verificato: D5, D2] |
| **Sottoagenti** | Opzione `agents` con nome, prompt, strumenti, modello, effort e `maxTurns`. Tetti: profondità 3 di default, 20 in parallelo, `maxBudgetUsd` che conta anche i figli | Un profilo può delegare (per esempio il brief chiama un ricercatore web su Haiku). Profondità 1 per partire | [verificato: D10] |
| **Squadre di agenti** (agent teams) | Funzione della CLI interattiva: non si configura con le opzioni dell'SDK | Non ci serve: la bacheca la teniamo noi | [verificato: D17] |
| **Hook** | Funzioni nostre chiamate nel processo, in punti fissi: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact`, `Stop`, `SubagentStart`, `Notification` e altri. Timeout di default 600 s; se `PreToolUse` scade, lo strumento è bloccato | Il ponte verso il Cancello, l'audit, gli avvisi | [verificato: D7] |
| **Decisioni di un hook** | `allow`, `deny`, `ask`, `defer`, più la modifica dell'input. Se due hook non sono d'accordo vince `deny`, poi `defer`, poi `ask`, poi `allow` | `deny` per tutto ciò che non passa dal Cancello; `defer` per le carte che aspettano una persona | [verificato: D7, D8] |
| **Permessi** | Ordine fisso: hook, regole deny, regole ask, modalità, regole allow, callback `canUseTool`. Una regola deny vale anche in `bypassPermissions`. Modalità: `default`, `dontAsk`, `acceptEdits`, `bypassPermissions`, `plan`, `auto`. `bypassPermissions` non parte come root | Modalità `dontAsk` con un elenco chiuso di strumenti: ciò che non è permesso è negato, senza domande | [verificato: D6] |
| **Approvazioni lunghe** | `canUseTool` può restare in attesa senza limite. Per attese di ore conviene `defer`: il turno finisce con `stop_reason: "tool_deferred"`, il processo esce e la sessione riparte dopo. `defer` funziona solo se nel turno c'è una sola chiamata di strumento | Carta al Cancello, processo chiuso, ripresa al sì o al no | [verificato: D9, D8] |
| **Strumenti che chiedono sempre** | Uno strumento MCP con `_meta["anthropic/requiresUserInteraction"]` passa sempre dalla callback, anche se una regola lo consente | `propose_action` marcato così: nessuna regola lo può rendere automatico | [verificato: D6] |
| **Server MCP** | Tre trasporti: processo locale (stdio), HTTP o SSE, server dentro il nostro processo (`createSdkMcpServer`). Nomi `mcp__server__strumento`; permessi per server con il jolly. Gli strumenti MCP si caricano su richiesta (tool search). Attesa di connessione 30 s | Gli MCP di Michele (mcp-memory, MCP RAG, mcp-enrich), quelli di SersanOutreach e il nostro server «bacheca» | [verificato: D11, D16; B] |
| **Skill** | File `SKILL.md` letti dalle cartelle `.claude/skills/`; l'opzione `skills` limita quali usare. Non si registrano da codice | Skill per squadra in git, versionate e riviste | [verificato: D12] |
| **Plugin** | Pacchetti di skill, sottoagenti, hook e server MCP caricati da una cartella locale (`type: "local"`, l'unico tipo accettato) | Un plugin «sersan-guardrail» con hook e MCP del Cancello, uguale per tutti i motori | [verificato: D13; proposta] |
| **Output strutturato** | `outputFormat` con uno JSON Schema (anche da Zod o Pydantic). Il risultato arriva in `structured_output` dopo il lavoro a più passi. Errore dedicato se lo schema non viene rispettato | Recap della call, brief, campi del CRM: sempre a schema | [verificato: D14] |
| **Costi** | `total_cost_usd` e `modelUsage` per modello, anche per i sottoagenti. Sono **stime** fatte dal client con un listino interno, non la fattura. Il dato vero viene dalla Usage and Cost API o dalla Console | Le stime per il cruscotto; il conto vero da LiteLLM e dalla Console | [verificato: D15] |
| **Tetti** | `maxTurns` e `maxBudgetUsd`. Al tetto la sessione finisce con `error_max_turns` o `error_max_budget_usd`. La spesa può superare il tetto dell'ultima risposta | Tetto per lavoro nel registro dei profili; tetto per agente in LiteLLM | [verificato: D16] |
| **Contesto** | Tutti i modelli attuali hanno 1 milione di token di contesto e 128.000 di uscita | Il contesto non è il limite; il costo sì | [verificato: D28] |
| **Compattazione** | Vicino al limite l'SDK riassume la storia vecchia ed emette `compact_boundary`. Hook `PreCompact`; `/compact` a mano. Le regole fisse vanno nel `CLAUDE.md`, che si reinietta a ogni richiesta | Regole per persona e per squadra nel `CLAUDE.md` del profilo; trascrizione intera salvata prima del riassunto | [verificato: D16] |
| **Osservabilità** | OpenTelemetry da variabili d'ambiente: metriche, log e tracce. Prompt e input degli strumenti esclusi di default | Verso Prometheus, Loki e Grafana (VLAN 70) | [verificato: D2; B] |
| **Altro** | Checkpoint dei file, elenco dei to-do della sessione, `fallbackModel`, `taskBudget` (alfa), sandbox, `spawnClaudeCodeProcess` per lanciare il processo in un container o in una VM | `fallbackModel` da Sonnet a Haiku per i lavori non critici | [verificato: D18, D16] |
| **Workflow dinamici** | Uno script orchestra decine di sottoagenti; disponibile anche con la chiave API | Per lavori grandi una tantum (mappa dei processi, audit): non per il motore | [verificato: D27] |

**Prezzi dei modelli al 25/10/2026, per milione di token** [verificato: D28]:

| Modello | ID | Input | Output | Lettura dalla cache |
|---|---|---|---|---|
| Opus 5.5 | `claude-opus-5-5` | 4 $ | 20 $ | 5 % dell'input |
| Sonnet 5.5 | `claude-sonnet-5-5` | 2 $ | 10 $ | 5 % dell'input |
| Haiku 5.5 | `claude-haiku-5-5` | da 0,10 $ | da 0,50 $ | 10 % dell'input |
| Fable 5.1 | `claude-fable-5-1` | 10 $ | 50 $ | 2,5 % dell'input |

La Batch API costa la metà [verificato: D28]. Sono gli stessi prezzi del rapporto 14 [verificato: 14 §1.1].

---

## 3. Come si ospita sul nostro server

### 3.1 Il modello a processi

- Ogni sessione è un processo `claude` con la sua shell, la sua cartella e le sue trascrizioni. N sessioni insieme sono N processi [verificato: D2].
- Tre cose stanno su disco: le trascrizioni, i file `CLAUDE.md` e i file di lavoro. Nessuna sopravvive a un container ricreato, se non si salvano altrove [verificato: D2].
- Il processo figlio non ascolta sulla rete. Il nostro servizio riceve le richieste e chiama l'SDK [verificato: D2].

### 3.2 I quattro schemi di Anthropic e quale usiamo

| Schema | Cosa fa | Per noi |
|---|---|---|
| Sessioni effimere | un container per lavoro, distrutto alla fine | post-call, brief, offerte, debrief: un lavoro, un processo, poi fine |
| Sessioni lunghe | container sempre acceso con più processi | solo l'agente che smista i messaggi in chat, se serve |
| Sessioni ibride | il processo si spegne quando la sessione è ferma e riparte dal `SessionStore` | i thread di chat con le persone e le carte che aspettano un sì |
| Container multi-agente | più processi nello stesso container | sì, con cartella, configurazione e chiave separate per agente |

[verificato: D2; scelta: proposta nostra]

### 3.3 Risorse e posto nel DL380

- **Punto di partenza ufficiale:** 1 GiB di RAM, 5 GiB di disco e 1 CPU per agente. La memoria cresce con la durata della sessione. Formula: agenti per host = (RAM dell'host meno il sistema) diviso il picco di RAM di una sessione [verificato: D2].
- **Il costo vero sono i token.** Anthropic stima un container minimo a circa 0,05 $ l'ora, mentre una sessione lunga spende dollari in token [verificato: D2].
- **Sul DL380.** Con 8 sessioni insieme servono circa 8-12 GB [non verificato: stima su D2]. Il board lascia circa 53 GB di RAM liberi per crescere [verificato: B]. Ci stanno larghi.
- **Dove.** Una VM Proxmox con Docker, un container per famiglia di agenti. Proxmox raccomanda di annidare i container applicativi dentro una VM QEMU quando serve isolamento [verificato: P1]. La VLAN la decide Michele: la 30 APPS, dove stanno già n8n e LiteLLM, oppure una VLAN dedicata agli agenti [proposta].
- **Rete.** Il board vuole default-deny fra le VLAN, DATA senza internet e AI verso DATA solo per Qdrant [verificato: B]. Il motore esce solo verso LiteLLM e i server MCP. Non tocca PostgreSQL dei clienti se non attraverso un MCP [proposta].

### 3.4 Isolare un agente dall'altro

Anthropic indica cinque misure per più agenti nello stesso container [verificato: D2]:
1. `settingSources: []`, così l'agente non legge impostazioni e `CLAUDE.md` altrui;
2. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, perché la memoria automatica si carica comunque;
3. `CLAUDE_CONFIG_DIR` diverso per agente;
4. una cartella di lavoro (`cwd`) per agente;
5. regole d'uscita diverse per agente sul proxy.

Due insidie: in TypeScript l'opzione `env` **sostituisce** l'ambiente del processo, in Python lo integra [verificato: D2]. Per noi è un vantaggio: il processo riceve solo le variabili che gli passiamo, mai le chiavi del motore.

### 3.5 La coda dei lavori

- L'SDK non ha code né orari [verificato: D1, D2]. La coda la scriviamo noi.
- Proposta: una tabella dei lavori in PostgreSQL letta con `FOR UPDATE SKIP LOCKED`, un numero massimo di processi per profilo, e n8n che inserisce i lavori a orario o su webhook [non verificato: scelta progettuale da provare].

### 3.6 Limiti noti da gestire

| Limite | Cosa facciamo | Fonte |
|---|---|---|
| Nessun timeout complessivo della sessione | `maxTurns`, `maxBudgetUsd` e un nostro orologio che ferma il processo | [verificato: D2] |
| La memoria cresce nelle sessioni lunghe | sessioni brevi; processi riciclati | [verificato: D2] |
| Molti sottoagenti in parallelo urtano i limiti di frequenza | lotti piccoli; limiti per chiave in LiteLLM | [verificato: D2, L3] |
| Nessuna scadenza per singolo sottoagente | `maxTurns` nella definizione del sottoagente | [verificato: D2] |

### 3.7 Traffico verso Anthropic oltre ai modelli, e trascrizioni

- Con la chiave API, le **metriche d'uso** di Claude Code partono verso Anthropic di default. Non contengono codice né prompt. Si spengono tutte con `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` [verificato: D26].
- Il controllo di sicurezza di **WebFetch** chiama direttamente `api.anthropic.com`, non passa da LiteLLM. Si spegne con `skipWebFetchPreflight` [verificato: D26, D21]. Proposta: niente WebFetch diretto; le pagine web le legge Firecrawl, già sul server, tramite un MCP [proposta; B].
- Le **trascrizioni locali** restano in chiaro per 30 giorni (`cleanupPeriodDays`) [verificato: D26]. Vanno su un dataset ZFS cifrato, con la conservazione decisa nel rapporto 16 [proposta; 16 §6].

---

## 4. Dietro LiteLLM e con le chiavi

### 4.1 Come si collega

- Il motore imposta `ANTHROPIC_BASE_URL` sull'indirizzo di LiteLLM e passa una **chiave virtuale di LiteLLM**, non la chiave Anthropic [verificato: L1, L2].
- La chiave va in `ANTHROPIC_AUTH_TOKEN` (header `Authorization: Bearer`) o in `ANTHROPIC_API_KEY` (header `X-Api-Key`). Il primo ha la precedenza [verificato: D24].
- LiteLLM espone il formato Anthropic su `/v1/messages` [verificato: L1].
- Anthropic stessa elenca LiteLLM fra i proxy che iniettano le credenziali e limitano la frequenza. `ANTHROPIC_BASE_URL` sposta solo le chiamate ai modelli [verificato: D3].
- Anthropic non certifica i gateway di terzi e non supporta Claude Code verso modelli non Claude [verificato: D20].

### 4.2 Cosa deve fare LiteLLM perché funzioni

| Requisito | Perché | Fonte |
|---|---|---|
| Inoltrare intatti `anthropic-version` e `anthropic-beta`, senza filtrare i valori | le funzioni nuove viaggiano in `anthropic-beta`; se si perdono, le funzioni si rompono | [verificato: D21] |
| Inoltrare lo streaming evento per evento, compresi i `ping` | un gateway che accumula la risposta blocca Claude Code; senza ping scatta il timeout durante i ragionamenti lunghi | [verificato: D21] |
| Usare come nome di modello gli ID veri (`claude-sonnet-5-5`) | con un alias sconosciuto Claude Code presume 200.000 token di contesto e non manda effort e gestione del contesto | [verificato: D21] |
| Definire nel config i nomi che il motore chiede | altrimenti LiteLLM risponde «Invalid model name» | [verificato: L1] |

**Stato di LiteLLM al 25/10/2026.**
- Ultima versione v1.106.4, uscita il 25/10/2026 [verificato: L4].
- È aperta la PR #36736 «forward claude-code-20250219 beta header for anthropic provider», aggiornata il 13/10. È aperta anche la #44174 su un header `anthropic-beta` non inoltrato verso un altro fornitore [verificato: L4].
- Conclusione: la compatibilità va provata con un test di accettazione prima di mettere gli agenti in produzione [proposta].

### 4.3 Budget e conti: la banca dei token

- LiteLLM mette budget su chiave, team, utente e cliente: `max_budget` con `budget_duration` (per esempio `"30d"`), più limiti `tpm_limit`, `rpm_limit` e `max_parallel_requests` [verificato: L3].
- Di default **riserva il costo massimo prima della richiesta** e la rifiuta se sfora il budget. Serve PostgreSQL [verificato: L3].
- Claude Code manda con ogni richiesta `x-claude-code-session-id` e, per i sottoagenti, `x-claude-code-agent-id` e `x-claude-code-parent-agent-id` [verificato: D21].
- **Proposta di mappatura** [proposta]:
  - una chiave virtuale per agente, con il suo tetto mensile;
  - un team per squadra (outreach, vendite, marketing...);
  - un utente per persona, per i lavori lanciati a suo nome;
  - il conto vero ogni mese dalla Console, confrontato con LiteLLM [verificato: D15].

### 4.4 Il gateway di Anthropic non serve agli agenti

- Claude Code contiene anche un gateway di Anthropic (Claude apps gateway), che instrada anche verso l'API Anthropic [verificato: D22].
- Però l'accesso è solo con login SSO dal browser, senza token di servizio. Un agente senza persona davanti non si autentica [verificato: D22].
- Per gli agenti resta LiteLLM, come nel board [verificato: B].

### 4.5 I modelli locali non fanno da motore

- Tecnicamente LiteLLM può mandare l'SDK verso altri modelli [verificato: L2]. Anthropic non lo supporta per Claude Code [verificato: D20].
- Con 8 GB di VRAM nessun modello locale è adatto a usare strumenti in catena e a orchestrare: per questo lavoro serve Claude [verificato: 13 §2.3].
- Qwen3-4B, gli embedding e il reranker restano nella pipeline di Michele (Docling, filtro, Qdrant, MCP RAG) e nei lavori n8n [verificato: B]. Il motore li usa attraverso l'MCP RAG [proposta].

---

## 5. Termini d'uso e autenticazione

### 5.1 Cosa dicono le regole

- L'uso dell'SDK è regolato dai **Commercial Terms** di Anthropic, anche quando alimenta prodotti per i propri clienti [verificato: D1, R3].
- Senza un'approvazione di Anthropic, chi sviluppa con l'SDK non può offrire il login di claude.ai né i limiti degli abbonamenti nei propri prodotti. Deve usare la chiave API [verificato: D1].
- Il login OAuth degli abbonamenti (Free, Pro, Max, Team, Enterprise) serve all'uso ordinario di Claude Code e delle app di Anthropic. Chi costruisce servizi, anche con l'SDK, usa una chiave della Console o di un cloud provider [verificato: D23].
- È consentito configurare la propria chiave in un server o in un gestore di segreti per i propri utenti autorizzati, se l'uso è fatturato al titolare della chiave e non è rivenduto [verificato: D23].
- I limiti dichiarati dei piani Pro e Max presumono un uso individuale e ordinario di Claude Code e dell'SDK [verificato: D23].
- Marchio: si può scrivere «Powered by Claude»; non si può chiamare il prodotto «Claude Code» né imitarne l'aspetto [verificato: D1].

### 5.2 Cosa significa per SerSan

- **Agenti:** chiave API della Console, dietro LiteLLM, fatturata a Sersan Limited. È l'uso che le regole descrivono come consentito [verificato: D23; lettura nostra].
- **Persone:** i posti Claude Team restano per chat, Claude Code e Claude Team che ragiona sul RAG via MCP [verificato: B]. Non alimentano gli agenti [verificato: D23].
- **Se un giorno il sistema si offre ai clienti:** per chi fa girare Claude Code nei propri servizi, Anthropic chiede binario non modificato e nessuna rivendita del consumo; ogni utente finale usa la propria chiave o il proprio piano [verificato: D23]. Prima di offrirlo va chiesto ad Anthropic come si applica all'SDK [proposta].
- **La storia dei crediti per l'SDK:** a maggio 2026 Anthropic aveva annunciato un credito separato per SDK e `claude -p` sugli abbonamenti, poi sospeso a giugno [voce di stampa: W1, non verificata sulle pagine ufficiali]. Con la chiave API non ci tocca.

### 5.3 Cosa si perde con la chiave API

Con la chiave della Console non sono disponibili [verificato: D25]:
- le attività pianificate nel cloud (`/schedule`) e le sessioni nel cloud;
- Remote Control, Claude Code in Slack, l'app Desktop;
- l'estensione Chrome, computer use, Artifact, dettatura;
- i connettori di claude.ai.

Restano CLI, SDK, sottoagenti, hook, skill, plugin, MCP, sandbox, workflow e OpenTelemetry [verificato: D25]. Quindi orari e connettori li portiamo noi: n8n e i server MCP.

### 5.4 Dati

- Conservazione standard sull'API commerciale: 30 giorni. La conservazione zero (ZDR) si attiva per organizzazione, se Anthropic la concede [verificato: D26; 16 §5].
- I tre colori dei dati restano validi: il rosso esce solo dopo l'oscuramento locale [verificato: 22 §2].

---

## 6. Claude Code headless (`claude -p`)

- **Cos'è.** Lo stesso ciclo dell'SDK, lanciato da riga di comando. Opzioni utili: `--output-format json` o `stream-json`, `--json-schema`, `--max-budget-usd`, `--resume`, `--allowedTools`, `--permission-mode` [verificato: D19].
- **`--bare`.** Salta hook, skill, plugin, server MCP, memoria e `CLAUDE.md` trovati sul disco. Anthropic lo consiglia per gli script e le chiamate dall'SDK e dice che diventerà il default di `-p` [verificato: D19].
- **Attenzione senza `--bare`.** In `-p` Claude Code esegue gli hook e collega gli MCP della cartella anche se nessuno l'ha mai dichiarata fidata, senza chiedere [verificato: D19].
- **Permessi.** Dalla 2.1.302 un'esecuzione senza modalità parte in `default` e nega ciò che chiede permesso [verificato: D6].
- **Costi.** L'uscita JSON contiene `total_cost_usd` e il dettaglio per modello, sempre come stima [verificato: D19].
- **`defer`.** Il rinvio di uno strumento funziona solo in modalità non interattiva [verificato: D8].
- **Quando usarlo** [proposta]:
  - lavori singoli e brevi (un riassunto con strumenti, un controllo notturno) lanciati da n8n o dai runner GitHub in casa;
  - prove e collaudi.
- **Quando no** [proposta]: per decine di agenti con chat, approvazioni e sessioni riprese. Lì servono gli hook nel processo, l'input in streaming e il `SessionStore`, che sono comodi solo con l'SDK.

---

## 7. L'adattatore ACP e Buzz

### 7.1 Che cos'è ACP

- Agent Client Protocol: un protocollo comune fra i client (editor, chat) e gli agenti. In locale l'agente è un processo figlio che parla JSON-RPC su stdio; il supporto remoto (HTTP, WebSocket) è ancora in corso [verificato: A2].

### 7.2 `claude-agent-acp`

- È un agente ACP costruito sull'SDK TypeScript ufficiale [verificato: A1].
- Funzioni: richieste di permesso per gli strumenti, sottoagenti come sessioni figlie, server MCP del client, terminali, comandi slash, to-do, ripresa delle sessioni, una versione sperimentale del protocollo v2 [verificato: A1].
- Versione 0.95.0 del 23/10/2026, Apache-2.0, 2.690 stelle, 164 issue e PR aperte [verificato: A1].
- Zed lo offre come «Claude Agent» [verificato: ricerca web del 25/10, A1].

### 7.3 Dentro Buzz

- Buzz collega gli agenti con il suo harness `buzz-acp`; Claude entra proprio con `claude-agent-acp` [verificato: 17 §0; A3].
- **Difetto aperto, issue #7375** del 5/9/2026, senza commenti al 25/10/2026: con `buzz-acp` 0.5.22 e `claude-agent-acp` 0.70.0 il prompt di base di Buzz non arriva alla sessione. Le risposte restano nella sessione e non escono nel canale: sette risposte perse prima che qualcuno se ne accorgesse, con l'esito registrato come «ok» [verificato: A3].
- Restano aperte anche le tre lacune già viste: nessun freno ai giri, approvazioni nei workflow che falliscono, permessi approvati in automatico di default [verificato: 17 §0].
- Ultima release desktop di Buzz 0.5.28 del 9/10/2026; repository attivo il 25/10 [verificato: A4].

### 7.4 Consiglio

- Buzz resta un **pilota interno** senza dati dei clienti, come già deciso [verificato: 22 §1].
- Il motore non deve dipendere da Buzz. Se Buzz matura, i nostri agenti ci entrano via ACP [proposta].
- Perché lo stesso freno valga ovunque, i guardrail vanno nel plugin «sersan-guardrail» (hook a comando più MCP del Cancello) e non solo nel codice del runner. Che `claude-agent-acp` carichi i plugin e gli hook dalle impostazioni va provato [non verificato].

---

## 8. Cosa l'SDK non dà, e chi lo copre

| Serve al sistema | Cosa dà l'SDK | Cosa copre lo stack di Michele | Cosa resta da costruire |
|---|---|---|---|
| **Programmazione a orari** (debrief alle 7, bandi la notte) | niente; le attività pianificate di Claude Code richiedono l'abbonamento [verificato: D25] | **n8n**: trigger a orario e webhook; è già nel board, con il flusso bandi notturno [verificato: B] | un flusso n8n per profilo che inserisce un lavoro nella coda del motore (chiamata HTTP firmata) |
| **Ingressi** (Recall.ai, modulo del sito, Instantly) | niente | **n8n** con i webhook, esposti da Pangolin e Traefik [verificato: B] | verifica di firma e anti-replay; estrazione a schema senza strumenti [verificato: 22 §2] |
| **Bacheca dei compiti fra agenti** | solo i to-do dentro una sessione [verificato: D16, D18] | **PostgreSQL 16** per la tabella; **Jira** (cloud ammesso) come vista per le persone [verificato: B] | tabella dei compiti, server MCP «bacheca» (crea, prendi, aggiorna, passa, chiudi), freno ai giri (salti, lavori e dollari per catena) |
| **Profili con nome** | l'opzione `agents` e `agent` vale per una sessione, non per un'identità nel tempo [verificato: D10, D18] | segreti in **Infisical** o **Vaultwarden**; chiavi per agente in **LiteLLM** [verificato: B, L3] | registro dei profili in git: nome, responsabile, modello, effort, prompt, skill, MCP ammessi, chiave, orari, tetti |
| **Chat di gruppo** persone e agenti | niente | **Teams** (M365 in cloud); n8n manda e aspetta risposte in Teams [verificato: B, N1] | un bot Teams con i nomi degli agenti, thread = sessione, comandi `/stop` e `/stato`. Serve una registrazione Azure Bot a tenant singolo [verificato: M1] |
| **Memoria** | `CLAUDE.md` e memoria automatica, per cartella [verificato: D16, D2] | **mcp-memory**, **MCP RAG** con **Qdrant**, **PostgreSQL**, **BookStack** [verificato: B] | collegare gli MCP ai profili; regole per persona; `SessionStore` su PostgreSQL |
| **Banca dei token** | `maxBudgetUsd` per lavoro, come stima [verificato: D15] | **LiteLLM**: budget per chiave, team e utente, bloccati prima della richiesta [verificato: L3] | mappatura chiavi, squadre e persone; cruscotto mensile |
| **Approvazioni (Cancello)** | hook `PreToolUse` con `defer`, `canUseTool`, regole deny [verificato: D7, D8, D9] | n8n per portare le carte in Teams [verificato: N1] | il Cancello, lavoro a parte; il ponte hook-Cancello sta nel motore |
| **Audit e registri** | OpenTelemetry e trascrizioni [verificato: D2] | **Prometheus**, **Loki**, **Grafana**, **Wazuh** [verificato: B] | cruscotto per agente; registro del Cancello |
| **Segreti fuori dagli agenti** | schema a proxy consigliato [verificato: D3] | **LiteLLM** per i modelli, **Infisical** per il resto [verificato: B] | MCP che chiamano i servizi con le chiavi fuori dal container |
| **Lettura del web** | WebFetch, WebSearch [verificato: D16] | **Firecrawl** in casa [verificato: B] | un MCP sopra Firecrawl |
| **Modelli locali** | non come motore [verificato: D20] | **Ollama** con Qwen3-4B, **Infinity**, **Docling** [verificato: B] | niente: restano nella pipeline |

**Due note.**
- **n8n** ha la licenza Sustainable Use: va bene per l'uso interno, vieta la rivendita [verificato: 12 §0 punto 6]. Nel motore non mettiamo logica che dipenda da n8n; n8n chiama il motore e basta [proposta].
- **Open WebUI** parla con i modelli tramite LiteLLM, non con gli agenti del motore. Collegarlo al motore richiederebbe un'API compatibile OpenAI nel motore [non verificato].

---

## 9. SDK o Hermes, nel nuovo quadro

L'architettura del 24/10 aveva scelto Hermes perché profili, bacheca, cron e Slack erano già pronti [verificato: 22 §1]. Il board di Michele cambia tre premesse: Slack e Notion non sono nel cloud ammesso, gli orari li fa n8n e la chat delle persone è Teams [verificato: B].

| Criterio | Hermes | Motore nostro sull'SDK |
|---|---|---|
| Profili con nome | pronti [verificato: 10 §4.1] | da scrivere, circa 1,5 gp [stima] |
| Bacheca fra agenti | pronta, in SQLite [verificato: 10 §4.1] | da scrivere, circa 3 gp, in PostgreSQL [stima] |
| Orari | pronti | n8n, già previsto [verificato: B] |
| Teams | uno dei 22 canali del gateway [verificato: 10 §4.2] | bot da scrivere, circa 3,5 gp [stima] |
| Cancello | gli hook dell'SDK non ci sono | hook `PreToolUse` e `defer` nativi [verificato: D7, D8] |
| LiteLLM | che accetti un indirizzo Anthropic diverso era da provare [verificato: 22 §2] | documentato da Anthropic e da LiteLLM [verificato: D3, L2] |
| Separazione dei permessi | «single-tenant»: per permessi diversi servono istanze diverse [verificato: 10 §5] | cartella, configurazione e chiave per agente [verificato: D2] |
| Stabilità | 5 patch in 10 giorni, oltre 5.000 issue, conversazioni finite al profilo sbagliato [verificato: 22 §8, 10 §3, §6] | un pacchetto fissato; rilasci quasi quotidiani da seguire [verificato: R1] |
| Componenti da aggiornare entro 14 giorni (Cyber Essentials) | Hermes in Python, il suo gateway, il suo database | un pacchetto npm più il nostro codice [verificato: B; confronto nostro] |
| Chi lo conosce | nessuno di noi a fondo | codice nostro, conosciuto da poche persone (rischio del §11) |

**Giudizio** [proposta]:
- Il motore sull'SDK chiede circa 8 gp per profili, bacheca e chat, che Hermes ha già. Hermes però chiede a sua volta lavoro per il ponte verso il Cancello via MCP, per la prova con LiteLLM e per le istanze separate dove cambiano i permessi [non verificato: stima].
- In cambio: un componente grande in meno da aggiornare, il Cancello agganciato in modo nativo, permessi separati per agente, nessun bug noto di sessioni scambiate.
- **Consiglio: non adottare Hermes.** Lo si riprende solo se i primi 10 gp del motore non danno i risultati attesi alla prova del §10.4.

---

## 10. Il motore agenti sull'SDK: disegno e stima

### 10.1 Schema

```
PERSONE ── Teams (M365) · Claude Team (ragiona sul RAG via MCP) · Jira (vista dei compiti)
               │  bot Teams e webhook via Pangolin + Traefik (VLAN 20 EDGE)
═══════ DL380 · Proxmox VE · default-deny fra le VLAN ═══════════════════════════
VLAN 30 APPS
  n8n ─ orari per profilo · webhook firmati · Teams, Outlook, Jira ─┐
                                                                    ▼
  MOTORE AGENTI (nuovo, TypeScript, VM con Docker)
    runner: coda in PostgreSQL → un processo SDK per lavoro, tetti, /stop
    registro dei profili (git) · bacheca e freno ai giri (MCP «bacheca»)
    ponte verso il Cancello (hook PreToolUse, defer, ripresa)
    adattatore Teams · Buzz solo in pilota, via ACP
        │ ANTHROPIC_BASE_URL + chiave virtuale per agente
        ▼
  LiteLLM ── budget per agente, squadra e persona · registri ──► API Anthropic
  server MCP: mcp-memory · MCP RAG · mcp-enrich · SersanOutreach · Firecrawl
VLAN 40 DATA   PostgreSQL 16 (coda, bacheca, sessioni) · Qdrant · MinIO · Infisical
VLAN 70 OBSRV  OpenTelemetry → Prometheus · Loki · Grafana · Wazuh
CANCELLO (lavoro a parte): carte, esecutori unici con effetti, audit
```

[verificato: B per i servizi esistenti; il motore è una proposta]

### 10.2 I pezzi e i giorni

| # | Pezzo | Cosa contiene | gp di base |
|---|---|---|---|
| 1 | Runner delle sessioni | servizio TypeScript; coda in PostgreSQL; un processo per lavoro; cartella e configurazione per agente; `maxTurns`, `maxBudgetUsd`, orologio esterno; ripresa; `/stop`; risultato a schema | 3 |
| 2 | Registro dei profili | YAML in git con nome, responsabile, modello, effort, prompt, skill, MCP ammessi, chiave LiteLLM, orari, tetti; validazione; vista per i CEO | 1,5 |
| 3 | Ponte verso il Cancello | hook `PreToolUse` che interroga il Cancello; `defer` e ripresa al sì o al no; regole deny; modalità `dontAsk`; plugin «sersan-guardrail» | 2 |
| 4 | Bacheca e passaggi | tabella dei compiti; MCP «bacheca» con 5-6 strumenti; freno ai giri; specchio facoltativo in Jira | 3 |
| 5 | Orari e ingressi | flussi n8n per orari e webhook; chiamata firmata al runner; esito di ritorno | 1 |
| 6 | Chat con le persone | bot Teams a tenant singolo; nome dell'agente in ogni messaggio; thread = sessione; carte e comandi | 3,5 |
| 7 | Memoria | profili collegati a mcp-memory, MCP RAG e SersanOutreach; `SessionStore` su PostgreSQL; regole per persona nel `CLAUDE.md` | 1,5 |
| 8 | LiteLLM | chiavi virtuali, team e budget; ID veri dei modelli; test degli header; `fallbackModel` | 1 |
| 9 | Isolamento e rete | VM con Docker; un container per famiglia; utente non root; uscita solo verso LiteLLM e MCP; segreti da Infisical; traffico non essenziale spento | 1,5 |
| 10 | Osservabilità | OpenTelemetry verso Loki e Prometheus; cruscotto Grafana per agente (costo, errori, durata); avvisi | 1 |
| 11 | Collaudo e runbook | 10 scenari su stage; prova di aggiornamento dell'SDK; runbook per Mattia | 2 |
| | **Totale** | | **21** |

[non verificato: stime nostre, sul modello dei rapporti 20-E e 22]

- **Con la riserva del 30 %:** circa 27 gp [stima].
- **Nucleo minimo** (pezzi 1, 2, 3, 5, 8 e metà del 9): circa 9-10 gp. È in linea con i 10-15 gp già stimati per un runner al posto di Hermes [verificato: 22 §1; stima].
- **Calendario.** Con Alberto a 4,5 gp e Mattia a 1,5 gp a settimana [verificato: 22 §5], il motore completo richiede 4-5 settimane [stima].
- **Fuori da questa stima:**
  - il Cancello, circa 21 gp [non verificato: stima di 22 §1];
  - le fasi F1-F4 dell'infrastruttura di Michele [verificato: B];
  - il contenuto di ogni agente: prompt, skill e prove per squadra;
  - la migrazione di SersanOutreach.

### 10.3 Ordine consigliato

1. **Settimana 1:** pezzi 1, 2, 8. Un agente «debrief» che gira a orario da n8n, su stage, con chiave LiteLLM e tetto. Se LiteLLM non è ancora pronto (nel board arriva in F4), si parte su stage con una chiave diretta limitata nella Console [proposta; B].
2. **Settimana 2:** pezzi 3 e 7. Il post-call con la bozza della mail come carta, che aspetta il sì e riprende la sessione.
3. **Settimane 3-4:** pezzi 4, 6, 9, 10. Bacheca, bot Teams, isolamento, cruscotti.
4. **Settimana 5:** pezzo 11 e riserva.

### 10.4 Prova di accettazione (fine settimana 2)

Il motore passa se [proposta]:
- tre profili girano per una settimana su stage senza sessioni scambiate;
- nessun effetto esce senza una carta del Cancello;
- una carta lasciata in attesa per una notte riprende la sessione giusta al mattino;
- la spesa resta sotto il tetto in LiteLLM, e la stima dell'SDK differisce dalla Console meno del 10 %;
- un aggiornamento dell'SDK passa i 10 scenari.

Se fallisce un criterio, si valuta di nuovo Hermes con questi stessi scenari.

---

## 11. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| L'SDK esce quasi ogni giorno e cambia comportamenti (per esempio la modalità di default dalla 2.1.302) [verificato: R1, D6] | Versione fissata; aggiornamento ogni due settimane dopo i 10 scenari su stage; il ritmo rientra nei 14 giorni di Cyber Essentials [verificato: B] |
| LiteLLM non inoltra un header `anthropic-beta` e una funzione si rompe [verificato: L4] | Test di accettazione a ogni aggiornamento di LiteLLM o dell'SDK; riserva: chiave diretta per famiglia con limiti nella Console |
| Le stime di costo dell'SDK non sono la fattura [verificato: D15] | Budget in LiteLLM; confronto mensile con la Console |
| Iniezioni di istruzioni da mail, trascrizioni e pagine web [verificato: D3] | Nessuno strumento che invia; `dontAsk` con elenco chiuso; deny negli hook; uscita su allowlist; testo di terzi letto da sessioni senza strumenti [verificato: 22 §2] |
| Sessioni lunghe che crescono o si bloccano [verificato: D2] | `maxTurns`, `maxBudgetUsd`, orologio esterno, processi riciclati |
| Limiti di frequenza dell'API condivisi fra tutti gli agenti | `rpm_limit` e `tpm_limit` per chiave in LiteLLM [verificato: L3]; passaggio di Tier con un deposito [verificato: 22 §7] |
| Il bot Teams richiede una registrazione Azure Bot, mentre Azure esce [verificato: M1, B] | Decisione di Michele (domanda 1); in alternativa n8n per le sole carte in Teams [verificato: N1] |
| Trascrizioni in chiaro sul disco [verificato: D26] | `persistSession: false` per i lavori sensibili; dataset ZFS cifrato; conservazione del rapporto 16 |
| Codice nostro, conosciuto da poche persone | Mattia secondo manutentore dal primo giorno; runbook; revisioni incrociate |
| Anthropic cambia termini o prezzi | Chiave API; versioni fissate; memoria, bacheca e registro restano nostri |

---

## 12. Domande aperte

1. **Chat delle persone con gli agenti.** Un bot Teams, che richiede una registrazione Azure Bot a tenant singolo? Oppure solo le carte in Teams via n8n e la conversazione altrove (Buzz in pilota, Open WebUI)? Decide Michele.
2. **LiteLLM prima della fase F4?** Il motore dipende da LiteLLM. Si anticipa, o si parte su stage con una chiave diretta limitata?
3. **VLAN del motore.** La 30 APPS insieme a n8n e LiteLLM, o una VLAN dedicata agli agenti con regole proprie?
4. **Jira come vista dei compiti.** I compiti degli agenti si specchiano in Jira? Con quali dati, visto che Jira è in cloud (al massimo dati gialli)?
5. **Chi approva.** n8n registra l'ora della risposta in Teams [verificato: N1]. Il Cancello vuole l'identità verificata con Entra: come la riceve?
6. **Header di LiteLLM.** Il test sugli header `anthropic-beta` passa con la versione di LiteLLM che Michele installerà?
7. **Clienti.** Se un giorno il sistema si offre ai clienti, come si applicano all'SDK le condizioni di Anthropic sulla chiave di ogni utente finale? Va chiesto ad Anthropic.
8. **ZDR.** Chiediamo subito ad Anthropic la conservazione zero per l'organizzazione [verificato: 22 §9 punto 14]?
9. **Linguaggio.** TypeScript va bene anche per Mattia?
10. **Web.** Gli agenti leggono il web solo attraverso Firecrawl, o serve anche WebFetch con uscita diretta?

---

## 13. Fonti

Tutte le pagine sono state lette il 25/10/2026.

**Documentazione Anthropic**
- D1 Agent SDK overview: https://code.claude.com/docs/en/agent-sdk/overview
- D2 Hosting the Agent SDK: https://code.claude.com/docs/en/agent-sdk/hosting
- D3 Securely deploying AI agents: https://code.claude.com/docs/en/agent-sdk/secure-deployment
- D4 Work with sessions: https://code.claude.com/docs/en/agent-sdk/sessions
- D5 Persist sessions to external storage: https://code.claude.com/docs/en/agent-sdk/session-storage
- D6 Configure permissions: https://code.claude.com/docs/en/agent-sdk/permissions
- D7 Hooks nell'SDK: https://code.claude.com/docs/en/agent-sdk/hooks
- D8 Hooks reference, rinvio di uno strumento: https://code.claude.com/docs/en/hooks
- D9 Handle approvals and user input: https://code.claude.com/docs/en/agent-sdk/user-input
- D10 Subagents in the SDK: https://code.claude.com/docs/en/agent-sdk/subagents
- D11 Connect to external tools with MCP: https://code.claude.com/docs/en/agent-sdk/mcp
- D12 Extend agents with skills: https://code.claude.com/docs/en/agent-sdk/skills
- D13 Plugins in the SDK: https://code.claude.com/docs/en/agent-sdk/plugins
- D14 Structured outputs: https://code.claude.com/docs/en/agent-sdk/structured-outputs
- D15 Track cost and usage: https://code.claude.com/docs/en/agent-sdk/cost-tracking
- D16 How the agent loop works: https://code.claude.com/docs/en/agent-sdk/agent-loop
- D17 Use Claude Code features in the SDK: https://code.claude.com/docs/en/agent-sdk/claude-code-features
- D18 Agent SDK reference, TypeScript: https://code.claude.com/docs/en/agent-sdk/typescript
- D19 Run Claude Code programmatically: https://code.claude.com/docs/en/headless
- D20 Other LLM gateways: https://code.claude.com/docs/en/llm-gateway
- D21 Gateway compatibility guide: https://code.claude.com/docs/en/llm-gateway-protocol
- D22 Run Claude Code through a gateway: https://code.claude.com/docs/en/gateways
- D23 Legal and compliance: https://code.claude.com/docs/en/legal-and-compliance
- D24 Authentication: https://code.claude.com/docs/en/authentication
- D25 Feature availability: https://code.claude.com/docs/en/feature-availability
- D26 Data usage: https://code.claude.com/docs/en/data-usage
- D27 Dynamic workflows: https://code.claude.com/docs/en/workflows
- D28 Models overview e prezzi: https://platform.claude.com/docs/en/about-claude/models/overview
- Context7: libreria `/websites/code_claude_en_agent-sdk` (identificata), `/websites/litellm_ai` (consultata)

**Registri e repository**
- R1 npm `@anthropic-ai/claude-agent-sdk`: https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk
- R2 PyPI `claude-agent-sdk`: https://pypi.org/project/claude-agent-sdk/
- R3 https://github.com/anthropics/claude-agent-sdk-typescript e https://github.com/anthropics/claude-agent-sdk-python (README, LICENSE, statistiche via API)
- R4 npm `@anthropic-ai/claude-code`: https://www.npmjs.com/package/@anthropic-ai/claude-code

**ACP e Buzz**
- A1 https://github.com/agentclientprotocol/claude-agent-acp (README) e npm `@agentclientprotocol/claude-agent-acp`; https://zed.dev/acp/agent/claude-agent
- A2 https://agentclientprotocol.com/overview/introduction
- A3 https://github.com/block/buzz/issues/7375
- A4 https://github.com/block/buzz (API: release e ultimo push)

**LiteLLM, n8n, Microsoft, Proxmox**
- L1 https://docs.litellm.ai/docs/proxy/client_setup/claude_code
- L2 https://docs.litellm.ai/docs/tutorials/claude_agent_sdk
- L3 https://docs.litellm.ai/docs/proxy/users
- L4 https://github.com/BerriAI/litellm (release v1.106.4; PR #36736; issue #44174)
- N1 https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcptrigger ; https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools ; https://docs.n8n.io/changelog (n8n 2.30, 7/7/2026)
- M1 https://learn.microsoft.com/en-ie/MicrosoftTeams/platform/bots/how-to/authentication/auth-flow-bot
- P1 https://pve.proxmox.com/wiki/Linux_Container

**Stampa (non verificata sulle pagine ufficiali)**
- W1 https://www.theregister.com/ai-ml/2026/05/14/anthropic-tosses-agents-into-the-api-billing-pool/5240748 ; https://wmedia.es/en/tips/claude-code-agent-sdk-credit

**File del progetto**
- B `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt` (board di Michele, vincolante)
- 00 `ricerca/00-visione-funzionalita.md`; 01 `ricerca/01-sersanoutreach.md`; 10 `ricerca/10-hermes-agent.md`; 12 `ricerca/12-altre-piattaforme.md`; 13 `ricerca/13-modelli-open-source-sul-server.md`; 14 `ricerca/14-costi-abbonamenti-e-api.md`; 16 `ricerca/16-gdpr-ai-act-e-regole.md`; 17 `ricerca/17-buzz.md`; 20-E `ricerca/20-proposta-E-claude-native.md`; 22 `ricerca/22-architettura-scelta.md`
