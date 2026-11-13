# 50. L'Agent SDK di Claude al 12 novembre 2026 e la prova con il modello a copione

- **Data**: 13 novembre 2026. Le pagine web sono state lette il 12/11/2026. La prova è stata fatta il 12/11/2026.
- **Per chi**: chi scrive lo spec della milestone 2 (corsia S), cioè Alberto. Michele per le parti su chiave API, LiteLLM e RAM del server.
- **Domande a cui risponde**:
  1. Com'è l'SDK oggi: pacchetto, versione, requisiti, Windows.
  2. Che cosa serve per una sessione che può fare solo ciò che le diamo noi.
  3. Se le prove automatiche possono guidare l'SDK vero con un finto servizio dei modelli, senza chiave API.
  4. Che cosa fa davvero l'SDK su crash, ripresa, spesa, interruzione e chiusura.
  5. Che cosa resta da provare con la chiave.
- **Cosa aggiorna**: [ricerca/26](26-claude-agent-sdk.md), del 25 ottobre, e [ricerca/41 §8](41-novita-al-9-novembre.md), del 9 novembre. Che cosa è superato è al §9. Prepara la decisione sulla corsia S, [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md), che rivede [ADR-0001](../docs/adr/0001-motore-agent-sdk.md) e applica [ADR-0021](../docs/adr/0021-motore-a-due-corsie.md). La prova è la PROVA-M1, parte 2, dello spec della milestone 1 (repo del codice).
- **Legenda**:
  - `[verificato: fonte, data]`: letto sulla fonte indicata. U1-U23 rimandano all'elenco delle Fonti, tutte lette il 12/11/2026. «prova, E5» vuol dire: visto nei registri dell'esperimento E5 della prova del 12/11/2026;
  - `[non verificato: motivo]`: non controllato, stima della fonte, o ragionamento non provato;
  - `[proposta]`: una scelta di disegno, non un fatto.
- **Cosa non ho fatto**:
  - nessuna chiave API vera, nessun login, nessuna richiesta verso servizi veri;
  - nessuna prova sul server, su Linux o su una macchina senza Git;
  - nessuna prova senza le variabili che spengono il traffico non essenziale, per non rischiare traffico vero;
  - nessuna prova della modalità `dontAsk` né di `permissionMode`: la prova non imposta la modalità, e il messaggio `init` riporta `default` [verificato: prova, E1];
  - nessuna prova della modalità `auto`, di `CLAUDE_CODE_ATTRIBUTION_HEADER=0` né di `sessionId` insieme a `forkSession`.

### Parole usate spesso

- **Agent SDK**: la libreria `@anthropic-ai/claude-agent-sdk`. Ogni sessione avvia un processo figlio, `claude.exe` su Windows, che parla con il nostro codice su stdio.
- **Copione** (modello a copione): un finto servizio dei modelli. Risponde secondo uno scenario scritto prima, senza un modello vero. Quello della milestone 1 sta nella repo del codice.
- **SSE** (streaming): la risposta arriva a pezzi, evento per evento, invece che tutta insieme in JSON.
- **Giro**: un avvio dell'SDK, da un messaggio fino al risultato (`result`).
- **Biforcazione**: un giro che riparte da una sessione salvata (`resume`) con `forkSession: true`. Nasce una sessione nuova con un id nuovo; la vecchia resta com'era.
- **Base**: l'ultima sessione buona da cui parte il giro dopo.
- **Gancio** (hook): una funzione nostra che l'SDK chiama in punti fissi. `PreToolUse` scatta prima di ogni strumento e può permettere, negare, chiedere o rinviare (`defer`).
- **Diario degli effetti**: un registro tenuto dallo strumento. Per ogni chiamata salva la chiave (giro, numero d'ordine), gli argomenti e il risultato, così una ripetizione non rifà l'effetto.
- **Server MCP interno al processo**: gli strumenti nostri, creati con `createSdkMcpServer` dentro il processo del motore. Il loro nome è `mcp__<server>__<strumento>`.
- **`terminal_reason`**: il campo del risultato che dice perché il giro è finito (`completed`, `hook_stopped`, `aborted_tools`…).
- **Corsia S**: le sessioni dell'Agent SDK con strumenti ([ADR-0021](../docs/adr/0021-motore-a-due-corsie.md)).

---

## In breve

1. **L'SDK di oggi è la 0.3.322 (`latest`, 10/11/2026), con dentro Claude Code 2.1.322.** Sul canale `next` c'è la 0.3.323 del 12/11. Il binario arriva con il pacchetto, anche per Windows. Serve Node 18.14 o più; noi abbiamo Node 22. Git Bash non serve se la sessione non ha strumenti di serie [verificato: U1, U2, U4, U17; prova, E10].
2. **Sì, le prove automatiche possono guidare l'SDK vero contro un copione su 127.0.0.1, con una chiave finta.** Sessione, strumento nostro, ripresa, attesa di una persona, interruzione, biforcazione, crash e chiusura funzionano. Il proxy spia non ha visto nessun host esterno [verificato: prova, E1-E18].
3. **Il copione della milestone 1 va esteso.** L'SDK chiede sempre lo streaming SSE su `POST /v1/messages?beta=true`. Il copione di oggi risponde solo in JSON e dà allo strumento un nome fisso [verificato: prova, E2; U10].
4. **Per una sessione chiusa servono insieme**: `tools: []`, il nostro server MCP interno al processo, `settingSources: []`, `strictMcpConfig: true`, un gancio `PreToolUse` con `onFailure: "block"`, e un ambiente scritto tutto da noi. Su Windows l'opzione `env` non basta: Node rimette dieci variabili vere dell'utente, se non le impostiamo noi [verificato: U7, U9; prova, E3, E15, E17].
5. **`dontAsk` e il marchio «chiedi sempre» non vanno d'accordo.** In `dontAsk` uno strumento `always_ask` o con `requiresUserInteraction` viene negato, anche se una regola lo permette [verificato: U8]. Con `dontAsk`, scelta in ricerca/45 §6.1, il marchio pensato in ricerca/26 per `propose_action` va quindi tolto [proposta].
6. **Il rinvio con `defer` non è la strada per aspettare una persona.** Con lo strumento interno al processo la ripresa è instabile. Funziona invece lo schema semplice: lo strumento risponde «in attesa», il giro finisce, più tardi si riprende con l'esito [verificato: prova, E7, E7d].
7. **Fermare non è immediato in tutti i modi.** `interrupt()` chiude la chiamata al modello in pochi millisecondi. `abort()` e `close()` lasciano `claude.exe` vivo circa 7 secondi. E nessun freno provato (`interrupt()`, `maxBudgetUsd`, `maxTurns`) ferma uno strumento già chiesto dal modello: lo ferma solo un gancio che nega [verificato: prova, E6, E16, E18].
8. **Il disegno «ogni giro biforca dalla base, gli effetti hanno un numero d'ordine» regge.** La base resta identica byte per byte. Un giro ucciso a metà si rifà dalla stessa base, e il diario fa uscire l'effetto una volta sola [verificato: prova, E11, E12].
9. **Restano per un giro dal vivo con la chiave**: il comportamento vero del modello, i blocchi di ragionamento firmati, la cache dei prompt, gli errori veri del servizio, la spesa vera (§8).

---

## 1. I fatti di oggi sull'SDK

Le fonti sono le pagine ufficiali e il registro npm, lette il 12/11/2026. Quindici fatti critici sono stati riletti da un secondo lettore sulle stesse fonti: nessuno era sbagliato [verificato: verifica del 12/11/2026].

### 1.1 Pacchetto e versioni

| Cosa | Oggi | Fonte |
|---|---|---|
| Pacchetto | `@anthropic-ai/claude-agent-sdk` | [verificato: U1] |
| `latest` | 0.3.322, del 10/11/2026, con Claude Code 2.1.322 | [verificato: U1, U2] |
| `next` | 0.3.323, del 12/11/2026 | [verificato: U2] |
| Ritmo | 0.3.317 e 0.3.318 (3/11), 0.3.319 (6/11), 0.3.321 (9/11), 0.3.322 (10/11) | [verificato: U2] |
| Claude Code a parte | `latest` 2.1.322, `stable` 2.1.311, `next` 2.1.323 | [verificato: U18] |
| Licenza | «SEE LICENSE IN README.md»; l'uso segue i Commercial Terms | [verificato: U1, U3] |
| Dipendenze «peer» | `zod ^4.0.0`, `@anthropic-ai/sdk >=0.93.0`, `@modelcontextprotocol/sdk ^1.29.0` | [verificato: U1] |
| Cambi recenti | 0.3.300 `updatedInput` validato; 0.3.302 sottoagenti «fork» attivi di default; 0.3.311 Node 18.14; 0.3.314 un file escluso da `settingSources` dava ancora regole (corretto); 0.3.317 tolta la variante `file_unchanged`; 0.3.319 `session_writes_lost` solo a uscita 0. `onFailure` chiede la 0.3.317 o più. Nessuna voce dalla 0.3.300 alla 0.3.322 è marcata «breaking» | [verificato: U19, U15] |

Il binario incluso è fissato alla versione dell'SDK: si aggiorna aggiornando l'SDK [verificato: U5].

### 1.2 Requisiti e Windows

- **Node 18.14 o più**, dalla 0.3.311; prima bastava Node 18 [verificato: U1, U19].
- **Il binario è una dipendenza facoltativa per piattaforma**: Linux x64 e arm64 (anche musl), macOS x64 e arm64, Windows x64 e arm64. Un'installazione che salta le dipendenze facoltative (per esempio `npm ci --omit=optional`) resta senza binario. L'errore è `Native CLI binary for <platform>-<arch> not found`; il rimedio è reinstallare o usare `pathToClaudeCodeExecutable` [verificato: U1, U4, U6].
- **Su Windows** il binario è `claude.exe`. Dalla 0.3.309 si estrae in una cartella temporanea per utente, `claude-agent-sdk` [verificato: U6, U19].
- **Git for Windows è facoltativo**: serve solo agli strumenti Bash e Monitor. Con `tools: []` non serve [verificato: U17, U7].
- Claude Code chiede Windows 10 1809 o più (o Server 2019), 4 GB di RAM, x64 o ARM64 [verificato: U17].

### 1.3 Come gira

- Ogni `query()` avvia un processo `claude` figlio che parla su stdio. N sessioni sono N processi [verificato: U5].
- Il punto di partenza ufficiale è 1 GiB di RAM, 1 CPU e 5 GiB di disco per sessione appena avviata. La RAM cresce con la durata. Non c'è un tempo massimo per la sessione: si limita con `maxTurns` [verificato: U5].
- `query({ prompt, options })` restituisce un generatore di messaggi. `prompt` è una stringa oppure un flusso di messaggi utente (ingresso a flusso) [verificato: U6].
- Per fermare: `abortController`; `interrupt()`, solo con l'ingresso a flusso; `close()`, che termina il processo [verificato: U6]. Che cosa fanno davvero è al §3.2.

### 1.4 Una sessione che può fare solo ciò che le diamo

- **`tools: []`** toglie tutti gli strumenti di serie. Claude può usare solo i nostri strumenti MCP [verificato: U7].
- **Il nostro server dentro il processo**: `createSdkMcpServer({ name, version?, instructions?, tools?, alwaysLoad?, timeout? })`, con strumenti creati da `tool(nome, descrizione, schemaZod, gestore, extras?)` [verificato: U6, U7].
- Il gestore restituisce `{ content, structuredContent?, isError? }`. Un'eccezione non ferma il ciclo: diventa un risultato d'errore che Claude legge [verificato: U7].
- **`permissionMode: "dontAsk"`** nega senza domande tutto ciò che nessuna regola permette, senza chiamare `canUseTool` [verificato: U8].
- **Attenzione**: in `dontAsk` vengono negati anche gli strumenti con `permission_policy: "always_ask"` o con `_meta["anthropic/requiresUserInteraction"]`, anche se una regola li permette [verificato: U8].
- `tool()` in TypeScript non ha un campo `_meta`. Per gli strumenti interni al processo c'è `permission_policy` (`always_allow`, `always_ask`, `always_deny`), dalla 0.3.301 [verificato: U6, U7].
- Le regole «allow» con il jolly valgono solo dopo un prefisso `mcp__<server>__` esplicito; `"*"` da solo è ignorato [verificato: U8].
- `tools: []` toglie anche `AskUserQuestion`, `Agent`, `TaskCreate`, `ToolSearch` e `Skill` [verificato: U7, U22].
- La ricerca degli strumenti è attiva di default e rinvia anche gli strumenti dei server SDK. `alwaysLoad: true` li tiene nel prompt; `ENABLE_TOOL_SEARCH=false` la spegne. Se `ToolSearch` resti con `tools: []` non è scritto [verificato: U20, U7; il resto non verificato: nessuna pagina lo dice].

### 1.5 Che cosa entra comunque dalla macchina

- Senza `settingSources` l'SDK carica le impostazioni `user`, `project` e `local`. Con `settingSources: []` non le carica [verificato: U9].
- Si leggono comunque: `~/.claude.json` (si sposta con `CLAUDE_CONFIG_DIR`), la memoria automatica (si spegne con `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`), le impostazioni gestite della macchina (si tolgono solo dalla macchina), quelle gestite dal server se la chiave è di un'organizzazione (non si spengono dall'SDK) [verificato: U9].
- `strictMcpConfig: true` usa solo i server di `mcpServers` e ignora `.mcp.json`, impostazioni utente, plugin e connettori di claude.ai [verificato: U6].
- In TypeScript `env` **sostituisce** l'ambiente del processo figlio, non lo integra [verificato: U6]. Su Windows però non è del tutto vero: §3.2, E15.

### 1.6 Ganci e rinvio

- Le decisioni di `PreToolUse` sono `allow`, `deny`, `ask`, `defer`. Vince `deny`, poi `defer`, `ask`, `allow`. I ganci dello stesso evento girano in parallelo [verificato: U15].
- Il tempo di default di un gancio è 600 s. Un `PreToolUse` scaduto blocca la chiamata [verificato: U15].
- **`onFailure: "block"`** (dalla 0.3.317): un gancio che va in errore, o che non restituisce nulla, blocca l'azione. Senza, l'azione prosegue con l'avviso `hook_callback_failed`. `Stop`, `SubagentStop`, `TaskCompleted` e `TeammateIdle` ignorano l'opzione [verificato: U15].
- **`defer`** chiude il giro con `stop_reason: "tool_deferred"` e il campo `deferred_tool_use`. Vale solo in modo non interattivo e solo se nel giro c'è **una sola** chiamata di strumento: con più chiamate il rinvio è ignorato e lo strumento segue il flusso normale dei permessi [verificato: U13].
- Se alla ripresa lo strumento rinviato non c'è, il risultato è `tool_deferred_unavailable` [verificato: U13].

### 1.7 Il servizio dei modelli, le credenziali, il traffico

- Il modello si sposta con `ANTHROPIC_BASE_URL`. Claude Code chiama `POST /v1/messages?beta=true` in streaming SSE e legge evento per evento fino a `message_delta` e `message_stop`. Un servizio che accumula la risposta blocca Claude Code; i `ping` servono contro il timeout di inattività [verificato: U10].
- `count_tokens` è facoltativo. La documentazione cita anche una sonda `HEAD /api/hello`, che si può rifiutare, e `GET /v1/models` solo con la scoperta dei modelli [verificato: U10, U23].
- `ANTHROPIC_AUTH_TOKEN` va nell'intestazione `Authorization: Bearer`, `ANTHROPIC_API_KEY` in `x-api-key` [verificato: U23].
- Tempi di default: `API_TIMEOUT_MS` 600000, `CLAUDE_CODE_MAX_RETRIES` 10, controllo dello stream a 300000 ms [verificato: U6].
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` spegne metriche, sondaggi, aggiornamenti e il controllo del «fast mode». Non spegne il controllo di WebFetch (`skipWebFetchPreflight`) né l'installazione del marketplace ufficiale (`CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`) [verificato: U14, U23].

### 1.8 Sessioni, ripresa, spesa

- Le sessioni si salvano in `~/.claude/projects/<cartella codificata>/<id>.jsonl`, oppure sotto `CLAUDE_CONFIG_DIR/projects/`. `resume` riprende per id, se il file è sulla stessa macchina. `persistSession: false` impedisce la ripresa [verificato: U21].
- Biforcazione: `resume` più `forkSession: true`; il nuovo id arriva nel messaggio `init` [verificato: U21].
- `total_cost_usd` e `costUSD` sono **stime** del client con un listino interno, non la fattura. Ogni risultato, anche d'errore, porta `total_cost_usd`, `usage`, `num_turns` e `session_id` [verificato: U11, U22].
- `maxBudgetUsd` conta solo la spesa della chiamata in corso. Una sessione ripresa riporta anche la spesa di prima. Dopo un crash i costi possono essere a zero [verificato: U6, U11, U22].
- `query()` lancia un'eccezione dopo un risultato d'errore [verificato: U22].

### 1.9 Termini

- Chi costruisce servizi con l'Agent SDK usa la chiave API della Console o di un cloud. È ammesso configurare la propria chiave su un server per i propri utenti, se l'uso è fatturato al titolare e non rivenduto [verificato: U12].
- Il login dei piani serve all'uso ordinario di Claude Code e delle app di Anthropic. Il motore non lo usa mai ([ADR-0001](../docs/adr/0001-motore-agent-sdk.md), revisione dell'11/11; [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)) [verificato: U12, U3].

---

## 2. La prova: come è fatta e che cosa non usa

**Macchina**: Windows 11 Pro 10.0.22631, Node 22.17.1, npm 11.7.0, Git Bash [verificato: prova].

**Pacchetto**: `@anthropic-ai/claude-agent-sdk` 0.3.322, installato con `--save-exact`, con `claude.exe` 2.1.322 dal pacchetto `-win32-x64` (346.496.160 byte). `zod` 4.6.7 fissato a mano; npm ha messo `@anthropic-ai/sdk` 1.8.0 e `@modelcontextprotocol/sdk` 1.32.2. In tutto `node_modules` pesa 386 MB, di cui 331 MB il binario [verificato: prova, Ambiente].

**Come è fatta.** Tutto gira nella cartella della prova:
- un **servizio finto** dell'API Messages su 127.0.0.1, porta 47600. Risponde in JSON o in SSE secondo un copione, e registra ogni richiesta con il corpo intero;
- un **proxy spia** sulla porta 47601. Registra e rifiuta ogni richiesta che gli arriva. `HTTPS_PROXY` e `HTTP_PROXY` puntano a lui; `NO_PROXY` vale `127.0.0.1,localhost`;
- una **sessione SDK** con un solo strumento nostro, `proponi_azione`, su un server MCP interno al processo. Sette copioni: `base`, `vietati`, `lento`, `moltolento`, `attesa`, `misura`, `base_modello_ignoto`; per la parte 3 anche `giri`, `giri_crash`, `spesa`, `gancio`, `lento20`;
- un **banco** che fa girare gli esperimenti e un campionatore dei processi.

**Opzioni della sessione**: `tools: []`; `mcpServers` con il server `sersan` e `alwaysLoad: true`; `allowedTools: ["mcp__sersan__proponi_azione"]`; `settingSources: []`; `strictMcpConfig: true`; `systemPrompt` nostro; `model: "claude-sonnet-4-5"`; `maxTurns: 4`; `cwd` vuota; `stderr` su file [verificato: prova, Ambiente].

**Ambiente** costruito da zero. Dalla macchina passano solo `PATH` e le variabili di sistema di Windows. Casa, `APPDATA`, `LOCALAPPDATA`, `TEMP` e `TMP` puntano a cartelle finte della prova; `CLAUDE_CONFIG_DIR` a una cartella della prova. Più le variabili di spegnimento del §7.2 e `CLAUDE_CODE_MAX_RETRIES=1` [verificato: prova, Ambiente].

**Che cosa non usa**:
- nessun login e nessuna chiave vera: solo una chiave finta;
- nessuna richiesta verso servizi veri. La sessione si rifiuta di partire se la chiave non è quella finta, se `CLAUDE_CONFIG_DIR` non sta nella cartella della prova o se l'host del servizio non è 127.0.0.1 (o un host `.invalid` nel controllo E9) [verificato: prova, Ambiente];
- nessun file dell'utente: niente configurazione, niente memoria, niente impostazioni di Claude Code della macchina.

Il giro completo della parte 2 dura 3 minuti e 36 secondi, senza errori del banco; quello della parte 3 circa 6 minuti. Alla fine nessun processo della prova è rimasto acceso e nessuno ascolta sulle due porte [verificato: prova].

**È previsto che il banco entri nella repo del codice come comando a parte**, nel primo gruppo di lavoro della milestone 2, da rilanciare a ogni aggiornamento dell'SDK. Il PRD lo prevede già per il rischio «L'Agent SDK cambia quasi ogni giorno» [verificato: PRD, tabella dei rischi, repo del codice].

---

## 3. Gli esiti

### 3.1 Gli esperimenti, uno per riga

| Esp. | Che cosa si è fatto | Esito |
|---|---|---|
| E1 | Una sessione: il copione chiede `proponi_azione` con una mail di prova, poi chiude con un testo. Variante E2b senza `alwaysLoad` | Arriva in fondo: `success`, `completed`, 2 giri. Lo strumento è chiamato una volta con gli argomenti esatti. Nessun login, nessun browser. Senza `alwaysLoad` stesso risultato |
| E2 | Lettura di tutte le richieste al servizio. Variante E4b con un nome di modello ignoto | Solo `POST /v1/messages?beta=true`, sempre con `stream: true` (38 richieste su 38). Una richiesta per passo del modello. Nessuna chiamata nascosta. Con un nome ignoto la forma della richiesta cambia |
| E3 | Il copione chiede `Bash`, poi `Write` | Niente eseguito. Il modello riceve «No such tool available». La sessione chiude con `success`; la cartella resta vuota; `permission_denials` vuoto |
| E4 | Lettura del risultato e della spesa | La spesa la calcola `claude.exe` dai token che il servizio dichiara: 0,009 USD per 2 risposte con `claude-sonnet-4-5`, `costBasis: "list"`. Con un nome ignoto 0,012 USD, `costBasis: "unknown"` |
| E5 | Processo A finisce la sessione ed esce; processo B, nuovo, la riprende con `resume` | Funziona: B manda tutta la storia (5 messaggi), stesso id. Trascrizione dentro `CLAUDE_CONFIG_DIR`; alcuni file finiscono fuori |
| E6 | Servizio lento 10 s; sessione fermata dopo 5 s con `abort()`, `close()`, `interrupt()`, oppure uccidendo il processo node. E6b con 30 s | Solo `interrupt()` chiude la chiamata subito (6 ms). Con `abort()` e `close()` `claude.exe` muore circa 7 s dopo. Se muore node, `claude.exe` muore con lui. Nessun orfano |
| E7 | Lo strumento risponde «in attesa di una persona» con una carta; il giro finisce; un processo nuovo riprende con l'esito. E7d con il gancio `defer` | Lo schema «in attesa» funziona. Con `defer` la sospensione funziona, ma la ripresa no: `tool_deferred_unavailable` e uscita con codice 1 |
| E8 | Misure di memoria e processi; due sessioni insieme; E8c elenca i figli | 4 processi per sessione. Due sessioni vanno in parallelo senza interferenze. Numeri al §5 |
| E9 | Rete: giro completo guardato dal proxy spia; poi il servizio su host `.invalid` | Zero host esterni. Il controllo con `.invalid` prova che `claude.exe` usa davvero il proxy |
| E10 | Windows: `PATH` senza Git, bash, msys, mingw; cartelle dei programmi vuote | La sessione arriva in fondo. Git Bash non serve con `tools: []`. Nessun errore su stderr |
| E11 | Giro 1, poi due giri 2 biforcati dalla stessa base, poi un giro 3 | L'id nuovo arriva in `init`. La base resta identica byte per byte. Due biforcazioni danno due id. Ogni file copia tutta la storia |
| E12 | Crash subito dopo l'effetto dello strumento; ripetizione biforcata dalla stessa base, con il diario | Un solo effetto per giro. La chiamata ripetuta trova il diario e restituisce il risultato salvato. Il giro arriva in fondo |
| E13 | Dopo un crash, `resume` della sessione interrotta senza biforcare | L'SDK non rifà la chiamata e non dà errore: ripara la storia da sé. Se la chiamata era rimasta aperta, la chiude con un risultato finto «esito sconosciuto»; in tutti e due i casi aggiunge una risposta inventata. Da non usare |
| E14 | Lettura dei tipi del pacchetto 0.3.322 | Ci sono `forkSession`, `resumeSessionAt`, `resumeDropsTurn`, `sessionId`, `maxBudgetUsd`, `maxTurns`, `taskBudget`, `persistSession`, `strictMcpConfig`, `alwaysLoad`, `onFailure`, `includePartialMessages` |
| E15 | Dieci varianti dell'ambiente su Windows | Tutte arrivano in fondo. Ma Node rimette dieci variabili vere dell'utente quando mancano: vanno impostate tutte da noi |
| E16 | Spesa durante il giro; tetto nostro con `interrupt()`; `maxBudgetUsd`; `maxTurns` | Spesa esatta passo per passo solo con `includePartialMessages`. Nessun freno ferma lo strumento già chiesto, salvo il gancio che nega. `maxBudgetUsd` e `maxTurns` sforano di un passo |
| E17 | Gancio di sicurezza su due strumenti, uno pericoloso; il gancio nega, si rompe, o ferma | Senza `onFailure: "block"` un gancio rotto lascia passare tutto. `continue: false` senza `deny` non blocca lo strumento |
| E18 | Chiusura con servizio lento 20 s, in tre modi, anche con due sessioni | `interrupt()` più fine dell'ingresso (o `close()`): nessun processo entro 0,1-0,9 s. `close()` da solo: 7,1 s |

Tutte le righe: [verificato: prova, E1-E18].

### 3.2 I punti che contano

**Una sessione senza strumenti di serie non fa nulla da sé** (E3, E10). Una chiamata a `Bash` o `Write` torna al modello come errore «No such tool available: Bash. Bash is disabled for this session, in subagents as well as here.». Non è un diniego di permesso: per l'SDK quello strumento non esiste. `claude.exe` non avvia shell né altri programmi [verificato: prova, E3, E8c].

**Ripresa e attesa di una persona** (E5, E7, E7d).
- La trascrizione sta in `CLAUDE_CONFIG_DIR/projects/<cartella>/<id>.jsonl`, 17-22 KB per sessione. Contiene i testi interi: il messaggio, gli argomenti dello strumento con il testo della mail, e i corpi mandati al modello (voci `api-request-blob`) [verificato: prova, E5].
- Lo schema che funziona: lo strumento risponde `{"esito":"in attesa di una persona","carta":"carta-0001"}`, il giro finisce, il processo esce. Più tardi un processo nuovo riprende con «Esito dal Cancello: la carta carta-0001 è stata approvata.». Il servizio riceve la storia intera e lo strumento non viene richiamato. Non resta nessun processo acceso nell'attesa [verificato: prova, E7].
- Con `defer`: la sospensione funziona (`stop_reason: "tool_deferred"`, lo strumento non parte). La ripresa no. Ripresa a flusso senza messaggi: `tool_deferred_unavailable`, poi «Claude Code process exited with code 1». Ripresa con un prompt vuoto: prima lo stesso errore, poi un secondo risultato in cui lo strumento parte davvero. Sembra una corsa fra la ripresa e il collegamento del server interno [verificato il comportamento: prova, E7d; la causa non verificata]. Con un server MCP esterno non è stato provato.

**Interruzione e chiusura** (E6, E6b, E18).
- `abort()`: la chiamata al modello non viene troncata. `claude.exe` si chiude 7,0 s dopo, e il ciclo lancia «Operation aborted» anche se la sessione era finita bene [verificato: prova, E6, E6b].
- `close()`: il ciclo finisce subito, senza risultato. `claude.exe` resta vivo per altri 7,1 s con la chiamata aperta [verificato: prova, E6b, E18].
- `interrupt()`, con l'ingresso a flusso: la connessione si chiude in 6-26 ms. Il risultato ha `error_during_execution` e `terminal_reason: aborted_streaming` [verificato: prova, E6, E18].
- Seguito dalla fine dell'ingresso, `interrupt()` non lascia processi entro 0,13 s con una sessione e 0,8 s con due. Seguito da `close()`, entro 0,11 e 0,9 s, ma senza `result` [verificato: prova, E18].
- Una lezione anche per il motore: in una prima esecuzione node restava vivo 60 s per un timer non cancellato. Dopo la chiusura dell'SDK non devono restare timer o socket accesi [verificato: prova, E18].

**Giri biforcati e crash** (E11, E12, E13).
- Il disegno provato: ogni giro parte con `resume: <base>` e `forkSession: true`. Lo strumento tiene un diario con la chiave (giro logico, numero d'ordine della chiamata nel giro). L'effetto vero è una riga in un file a parte; in produzione sarebbe la carta consegnata al Cancello [verificato: prova, parte 3].
- L'id del giro nuovo arriva già nel messaggio `init`, prima di ogni richiesta. La base resta identica: stessa dimensione (17.244 byte), stessa impronta SHA-256, stessa data di modifica [verificato: prova, E11].
- Ogni file biforcato copia tutta la storia: 17 KB, poi 24, poi 31. Con un file per giro lo spazio cresce con il quadrato dei giri: i rami vecchi vanno cancellati [verificato: prova, E11].
- `total_cost_usd` riparte dal totale salvato: 0,009, poi 0,018, poi 0,027 USD. La spesa di un giro è la differenza con la base [verificato: prova, E11].
- Crash: il processo è ucciso 2 ms dopo la risposta dello strumento. Il tentativo B, biforcato dalla stessa base, trova la riga nel diario con gli stessi argomenti e restituisce il risultato salvato. In tutto un effetto per giro [verificato: prova, E12].
- `claude.exe` scrive il risultato dello strumento nella trascrizione prima di mandarlo al modello. Il file del tentativo morto resta: è un ramo da cancellare [verificato: prova, E12].
- Due limiti che la prova non toglie. Un modello vero, alla ripetizione, può chiedere un'altra cosa come chiamata 0: serve una regola quando gli argomenti differiscono [non verificato: il copione è deterministico]. Un crash fra l'effetto e la scrittura del diario lascerebbe un effetto non registrato: effetto e diario vanno scritti insieme [non verificato: ragionamento, non provato].
- Senza biforcare (E13): dopo il crash l'SDK aggiunge da sé un risultato in errore, «[Tool call interrupted: the session ended before this call's result was recorded, so its outcome is unknown. Check whether it took effect before relying on it or running it again.]», e una risposta dell'assistente inventata, «No response requested.». La scelta di rifare l'effetto passa al modello, che non ha il diario [verificato: prova, E13].

**Spesa e tetti** (E16).
- Senza `includePartialMessages`, i messaggi `assistant` portano i token d'ingresso giusti ma `output_tokens: 1`. La somma passo per passo dà 0,090045 invece di 0,1125 USD [verificato: prova, E16].
- Con `includePartialMessages: true` arrivano `message_start` (ingresso) e `message_delta` (uscita finale) di ogni passo. La somma dà esattamente 0,1125, uguale a `total_cost_usd` [verificato: prova, E16].
- Un tetto nostro più `interrupt()` ferma la richiesta successiva, ma **lo strumento già chiesto viene eseguito lo stesso**. Poi nella trascrizione l'azione risulta «rejected». L'effetto però c'è stato [verificato: prova, E16].
- Con il tetto anche nel gancio `PreToolUse`, che nega lo strumento: nessun effetto, una sola richiesta, `aborted_tools` [verificato: prova, E16].
- `maxBudgetUsd` di 0,01: lo strumento del primo passo parte, poi `error_max_budget_usd` con una spesa di 0,0375. `maxTurns` di 1: stesso schema, e il giro finisce senza testo finale. Il controllo avviene prima della richiesta successiva [verificato: prova, E16].

**Il gancio di sicurezza** (E17). Due strumenti in `allowedTools`: `proponi_azione` (ammesso) e `cancella_archivio` (fuori elenco). Decide solo il gancio.

| Prova | Che cosa è uscito | Fine del giro |
|---|---|---|
| Il gancio nega ciò che non è ammesso | solo la carta | `success`, `completed` |
| Il gancio lancia un'eccezione, senza `onFailure` o con `"continue"` | **l'effetto pericoloso e la carta** | `success`, `completed` |
| Il gancio lancia, `onFailure: "block"` | nulla | `success`, `completed`; tutte e due le chiamate in `permission_denials` |
| Stop d'emergenza, il gancio nega | nulla | il modello chiude con un testo |
| Stop, `continue: false` senza `deny` | **la carta: lo strumento parte lo stesso** | `success`, `hook_stopped` |
| Stop, `continue: false` più `deny` | nulla | `success`, `hook_stopped`, nessuna richiesta in più |

[verificato: prova, E17]. Un giro fermato dal gancio ha `subtype: success`: il motore deve leggere `terminal_reason`. Con `onFailure: "block"` la query fallisce all'avvio se `claude.exe` non supporta l'opzione [verificato: prova, E14, E17].

---

## 4. Che cosa chiede l'SDK al servizio dei modelli

È quanto basta per estendere il copione. Tutto ha funzionato con `claude.exe` 2.1.322 [verificato: prova, E2, E4, E9].

### 4.1 La richiesta

- `POST /v1/messages?beta=true`. La rotta va accettata anche con la query.
- Intestazioni utili: `x-api-key` (il copione non la deve controllare), `x-claude-code-session-id` (separa le sessioni parallele), `anthropic-beta`, `anthropic-version: 2023-06-01`. L'`user-agent` è `claude-cli/2.1.322 (external, sdk-ts, agent-sdk/0.3.322)`.
- `anthropic-beta` vale `claude-code-20250219,interleaved-thinking-2025-05-14,context-management-2025-06-27,thinking-token-count-2026-05-13,thinking-display-updates-2026-08-18`.
- Il corpo, con `claude-sonnet-4-5`:

```json
{
  "model": "claude-sonnet-4-5",
  "stream": true,
  "max_tokens": 32000,
  "system": [ {"type":"text","text":"x-anthropic-billing-header: ..."},
              {"type":"text","text":"You are a Claude agent, built on Anthropic's Claude Agent SDK.","cache_control":{"type":"ephemeral"}},
              {"type":"text","text":"<le nostre istruzioni>","cache_control":{"type":"ephemeral"}} ],
  "messages": [ {"role":"user","content":[ <4 blocchi <system-reminder>>, {"type":"text","text":"<messaggio>"} ]},
                {"role":"assistant","content":[{"type":"tool_use","id":"...","name":"mcp__sersan__proponi_azione","input":{...}}]},
                {"role":"user","content":[{"type":"tool_result","tool_use_id":"...","content":[{"type":"text","text":"<esito>"},{"type":"text","text":"<system-reminder>..."}],"cache_control":{"type":"ephemeral"}}]} ],
  "tools": [ {"name":"mcp__<server>__<strumento>","description":"...","input_schema":{...}} ],
  "metadata": {"user_id":"<JSON con device_id, account_uuid vuoto, session_id>"},
  "thinking": {"type":"enabled","budget_tokens":31999,"display":"updates"},
  "context_management": {"edits":[{"type":"clear_thinking_20251015","keep":"all"}]}
}
```

- Il primo messaggio dell'utente porta, prima del nostro testo, quattro blocchi `<system-reminder>`: l'ambiente (la cartella di lavoro completa, `Platform: win32`, `Shell: bash`, la versione del sistema), il nome del modello con la data di fine conoscenze, i token rimasti, la data di oggi. Ogni `tool_result` riceve in coda un altro `<system-reminder>` [verificato: prova, E2].
- Il `content` di un `tool_result` può essere una stringa, con `is_error: true` per gli errori.
- Con un nome di modello ignoto compaiono uno strumento `DeferredToolPlaceholder` con `defer_loading: true`, un messaggio `role: "system"` dentro `messages`, `thinking: {type:"adaptive"}`, `output_config: {effort:"high"}` e due intestazioni beta in più [verificato: prova, E4b].

### 4.2 La risposta a flusso

Con `content-type: text/event-stream`. Questa sequenza basta, senza blocchi di ragionamento:

```
event: message_start
data: {"type":"message_start","message":{"id":"msg_x","type":"message","role":"assistant","model":"<come richiesto>","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":1000,"output_tokens":1,"cache_creation_input_tokens":0,"cache_read_input_tokens":0}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"tool_use","id":"toolu_x","name":"mcp__sersan__proponi_azione","input":{}}}
   (per il testo: {"type":"text","text":""})

event: ping
data: {"type":"ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"input_json_delta","partial_json":"{\"tipo\":\"email\",...}"}}
   (per il testo: {"type":"text_delta","text":"..."})

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"tool_use","stop_sequence":null},"usage":{"output_tokens":100}}
   (per il testo: "end_turn")

event: message_stop
data: {"type":"message_stop"}
```

- `usage.input_tokens` di `message_start` e `usage.output_tokens` di `message_delta` finiscono in `usage` e in `total_cost_usd`. Il copione quindi decide la spesa con i token che dichiara [verificato: prova, E4].
- Gli errori vanno in JSON `{type:"error", error:{type, message}}` con lo stato HTTP. Con un 403 la sessione chiude con `is_error: true` e «Failed to authenticate. API Error: 403 …» [verificato: prova, E9].

### 4.3 Che cosa aggiungere al copione

1. Lo streaming SSE del §4.2, quando la richiesta ha `stream: true`.
2. Il `tool_use` con nome e argomenti presi dal copione. Oggi il copione usa il nome `strumento` e `{}` fissi. Il nome va scritto come `mcp__<server>__<strumento>`, oppure cercato per suffisso fra i `tools` della richiesta.
3. La scelta della risposta. Il meccanismo `passo:` del copione può restare: le nostre istruzioni arrivano intere come terzo blocco di `system`, quindi una riga `passo: <nome>` a inizio riga viene trovata. L'occorrenza del passo diventa il numero del giro. Servono in più condizioni sullo stato: c'è un `tool_result` in coda? L'ultimo messaggio dell'utente contiene una parola?
4. Il confronto con i testi deve ignorare i blocchi `<system-reminder>`.
5. I ritardi con chiusura anticipata, che il copione ha già, servono per l'interruzione.

[verificato: prova, «Che cosa chiede l'SDK al servizio dei modelli»]

---

## 5. I numeri misurati

Valgono per quella macchina (Windows 11 Pro, Node 22.17.1) e per sessioni brevi contro un servizio finto. Su un'altra macchina, o con sessioni lunghe, vanno rimisurati. «ws» è la memoria residente, «privata» la memoria privata, lette con `Get-CimInstance Win32_Process`.

| Misura | Valore |
|---|---|
| `claude.exe` durante un giro, in attesa del servizio | ws 168-185 MB, privata 323-342 MB |
| `claude.exe` a sessione ferma, ingresso aperto | ws 174-176 MB, privata 328-340 MB |
| node.exe che ospita l'SDK | ws circa 78 MB, privata circa 80 MB |
| Due sessioni insieme | per ognuna ws massima 183-185 MB, privata 321-331 MB; nessuna interferenza |
| Processi per sessione | 4: node.exe, `claude.exe` e un conhost.exe per ciascuno (11-12 MB l'uno) |
| Dall'SDK caricato alla prima richiesta al servizio | 0,49-1,66 s |
| Dalla nascita di node al caricamento dell'SDK | circa 0,2-0,3 s |
| `time_to_request_ms` (inizio del giro, richiesta) | 65-263 ms |
| `duration_ms` di una sessione di 2 passi, servizio istantaneo | 130-190 ms |
| `claude.exe` chiuso dopo `abort()` o `close()` | circa 7,0-7,1 s |
| Chiusura della chiamata dopo `interrupt()` | 6-26 ms |
| Disco | 17-22 KB di trascrizione per sessione; la cartella di configurazione 390 KB dopo 21 sessioni |
| Peso del binario | 331 MB per piattaforma |

[verificato: prova, E6, E6b, E8, E8c, E18]

In tutto circa 250 MB residenti per sessione attiva [verificato: prova, «Problemi e limiti»]. Il punto di partenza ufficiale resta 1 GiB per sessione appena avviata, e la RAM cresce con la durata [verificato: U5]. La prova non misura sessioni lunghe né il picco con molti strumenti.

---

## 6. Le sorprese

Ciò che la documentazione non dice, o dice diversamente.

1. **`close()` non chiude subito.** La documentazione dice «Forcefully ends the query». Nella prova il ciclo finisce subito, ma `claude.exe` resta vivo circa 7 s con la chiamata al modello aperta. Lo stesso con `abort()` [verificato: U6; prova, E6b, E18].
2. **`env` non sostituisce tutto l'ambiente su Windows.** La documentazione dice che lo sostituisce. Lo `spawn` di Node rimette, con i valori veri dell'utente, le variabili che mancano fra HOMEDRIVE, HOMEPATH, LOGONSERVER, PATH, SYSTEMDRIVE, SYSTEMROOT, TEMP, USERDOMAIN, USERNAME e WINDIR. Togliere `PATH` non toglie niente: si sostituisce solo impostandola noi. Compare anche `NoDefaultCurrentDirectoryInExePath`, innocua [verificato: U6; prova, E15].
3. **Nessun freno ferma uno strumento già chiesto.** `interrupt()`, `maxBudgetUsd` e `maxTurns` lasciano partire lo strumento dell'ultimo passo. Solo un gancio `PreToolUse` che nega lo ferma [verificato: prova, E16].
4. **La trascrizione può mentire sugli effetti.** Dopo un `interrupt()` uno strumento eseguito risulta «rejected». Dopo un crash un risultato può essere «outcome unknown». Che cosa è uscito lo dice solo il diario, o il Cancello [verificato: prova, E13, E16].
5. **La ripresa dopo un crash ripara la storia da sola**, con un risultato finto e una risposta inventata, senza errore (E13) [verificato: prova, E13].
6. **Il rinvio `defer` con uno strumento interno al processo è instabile alla ripresa**, anche con una sola chiamata nel giro (E7d) [verificato: prova, E7d].
7. **La forma della richiesta dipende dal nome del modello** (E4b), e con un nome ignoto la spesa passa a `costBasis: "unknown"`, con un listino non documentato [verificato: prova, E4, E4b].
8. **`continue: false` senza `deny` non blocca la chiamata già decisa.** Lo `stopReason` non compare in nessun messaggio dell'SDK: lo stop si riconosce da `terminal_reason: hook_stopped` [verificato: prova, E17].
9. **Un gancio rotto lascia passare anche lo strumento fuori elenco**, se manca `onFailure: "block"`. La documentazione dice che l'azione prosegue; la prova mostra che cosa vuol dire [verificato: U15; prova, E17].
10. **Alcuni file finiscono fuori da `CLAUDE_CONFIG_DIR`**: i registri del server MCP in `%LOCALAPPDATA%/claude-cli-nodejs/Cache/<cartella>/mcp-logs-sersan/`, le prove `fswatch-probe-*` in `%TEMP%/claude/`. Senza `LOCALAPPDATA`, i registri seguono `USERPROFILE\AppData\Local`. Con `CLAUDE_CODE_TMPDIR` non sono comparsi file `fswatch-probe-*`, né lì né in `TEMP`; dove vadano in quel caso non si è visto [verificato: prova, E5, E15; non verificato: la cartella con `CLAUDE_CODE_TMPDIR`].
11. **Il modello vede l'ambiente**: la cartella di lavoro completa, il sistema, la shell. Il blocco dice `Shell: bash` anche senza Git sul `PATH`; per quale strada `claude.exe` trovi bash non si è visto [verificato: prova, E2, E10].
12. **Nessuna sonda e nessun conteggio**: con le variabili di spegnimento non sono arrivati `HEAD /api/hello`, `count_tokens` né `GET /v1/models`, e nessuna chiamata a un modello piccolo o per i titoli [verificato: prova, E2, E9].
13. **`alwaysLoad` fa di più**: oltre a non rinviare gli strumenti, blocca l'avvio finché il server non è collegato, al massimo 5 s [verificato: prova, E14, dai tipi del pacchetto].
14. **Il blocco di attribuzione non disturba il copione.** La fonte temeva che servisse `CLAUDE_CODE_ATTRIBUTION_HEADER=0`; la riga `passo:` viene trovata lo stesso, perché le nostre istruzioni arrivano intere nel terzo blocco [verificato: prova, «Che cosa chiede l'SDK»].
15. **La modalità di partenza.** ricerca/41 §1.2 dice che SDK e `-p` partono in Manual dalla 2.1.302; U8 dice in generale che senza modalità si parte in `default`. Il CHANGELOG limita il cambio ai fornitori terzi «with telemetry off or fresh install» [verificato: U19]. Nella prova, senza modalità impostata, `init` riporta `default` [verificato: prova, E1]. Non pesa se lo spec imposta sempre la modalità.

---

## 7. Opzioni e variabili da fissare per ogni sessione S

Le voci vengono da due strade: la prova (provate) e la documentazione (non provate). Lo dico riga per riga.

### 7.1 Opzioni dell'SDK

| Opzione | Valore | Da dove |
|---|---|---|
| `tools` | `[]` | provata (E3, E10) |
| `settingSources` | `[]` | provata |
| `strictMcpConfig` | `true` | provata |
| `mcpServers` | il ponte come server interno al processo, con `alwaysLoad: true` | provata (E1, E14) |
| `allowedTools` | solo gli strumenti del ponte | provata |
| `hooks.PreToolUse` | `[{ hooks: [gancio], onFailure: "block" }]`, senza `matcher` | provata (E17) |
| `permissionMode` | `"dontAsk"`, come deciso in [ricerca/45 §6.1](45-architettura-v3.md) | **non provata**: nella prova la modalità non era impostata |
| `resume` e `forkSession` | `resume: <base>`, `forkSession: true` su ogni giro dopo il primo | provata (E11, E12) |
| `persistSession` | `true` (default): la biforcazione ha bisogno del file della base | provata: default in tutte le prove (E11, E12); tipo letto in E14 |
| `includePartialMessages` | `true` | provata (E16) |
| `maxBudgetUsd`, `maxTurns` | come rete di sicurezza, con margine | provata (E16) |
| `model` | un nome del listino, lo stesso della produzione | provata (E4b) |
| `cwd` | una cartella vuota e neutra: il percorso arriva al modello | provata (E2) |
| `env` | costruito da zero, §7.2 | provata (E15) |
| `stderr` | su file | provata |
| `prompt` | ingresso a flusso, per poter chiamare `interrupt()` | provata (E6, E18) |

### 7.2 Variabili d'ambiente, tutte impostate da noi

- **Isolamento** (provate, E15): `CLAUDE_CONFIG_DIR`, `USERPROFILE`, `HOME`, `HOMEDRIVE`, `HOMEPATH`, `APPDATA`, `LOCALAPPDATA`, `TEMP`, `TMP`, `CLAUDE_CODE_TMPDIR`, tutte su cartelle dell'area di lavoro.
- **Quelle che Node rimetterebbe con i valori veri** (provate, E15): `PATH` (vuoto, o solo `C:\Windows\System32`), `SYSTEMROOT`, `WINDIR`, `SYSTEMDRIVE`, `USERNAME`, `USERDOMAIN`, `LOGONSERVER`, con valori neutri. `USERPROFILE` va sempre impostata: senza, arriverebbe la casa vera dell'utente.
- **Servizio** (provate): `ANTHROPIC_API_KEY` e `ANTHROPIC_BASE_URL`.
- **Spegnimenti** (provati insieme, E9): `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, `DISABLE_AUTOUPDATER`, `DISABLE_UPDATES`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `DO_NOT_TRACK`, `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`, `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`, `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL`, `ENABLE_CLAUDEAI_MCP_SERVERS=false`, `DISABLE_COST_WARNINGS`.
- **Rete** (provate, E9): `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`. In prova il proxy spia; in produzione il proxy di uscita del motore, se c'è.
- **Ripetizioni**: `CLAUDE_CODE_MAX_RETRIES` (provata, con 1 e 0).
- **Dalla documentazione, non provate**: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` [U9], `CLAUDE_CODE_FORK_SUBAGENT=0` [U19], `ENABLE_TOOL_SEARCH=false` [U20]. Per le prove col copione anche `CLAUDE_CODE_ATTRIBUTION_HEADER=0` e `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` [U10; proposta della fonte]. Per il primo la prova mostra che il copione ne fa a meno (§6, punto 14).

---

## 8. Che cosa non si può provare senza chiave

- Il comportamento vero del modello: se chiama davvero il ponte, con quali argomenti, quanti giri fa, che cosa chiede alla ripetizione dopo un crash.
- I blocchi di ragionamento firmati e la ripresa con quei blocchi. Il copione non manda blocchi `thinking`, anche se la richiesta li chiede (`budget_tokens: 31999`).
- La cache dei prompt e il suo effetto sulla spesa.
- Gli errori veri del servizio: 429, 529, limiti di velocità. Il copione può solo imitarne lo stato HTTP.
- La spesa vera contro quella calcolata dal listino interno.
- La ricerca degli strumenti con molti strumenti MCP.
- Il traffico non essenziale senza le variabili di spegnimento.
- La modalità `auto`: dietro il copione il classificatore lato server non c'è [verificato: ricerca/41 §1.3].
- Le impostazioni gestite dal server, che arrivano con una chiave d'organizzazione: U9 non dice da quale indirizzo, né se passano da `ANTHROPIC_BASE_URL` [non verificato: buco nelle fonti].

Restano aperti anche punti che la prova non chiude: un ripiego su JSON se lo streaming fallisce; una libreria interna che ignori il proxy (servirebbe uno strumento di cattura di rete); `defer` con un server MCP esterno; `sessionId` insieme a `forkSession`; `taskBudget` [non verificato: non provati].

**Chi serve.** La chiave API della Console oggi non c'è. La crea chi amministra l'organizzazione Anthropic di SerSan (Michele o i CEO), con un tetto di spesa nella Console. LiteLLM arriva con la milestone 3 e lo installa Michele ([ADR-0004](../docs/adr/0004-litellm-banca-token.md)). Chi gestisce le macchine di sviluppo deve dire se ci sono impostazioni gestite (registro di Windows o file gestito) [verificato: fonti della raccolta, «Cosa dipende da persone»].

---

## 9. Che cosa è superato in ricerca/26 e ricerca/41 §8

### 9.1 In [ricerca/26](26-claude-agent-sdk.md)

| Dove | Che cosa diceva | Oggi |
|---|---|---|
| §1.1, versioni | SDK 0.3.310, Claude Code 2.1.310 | 0.3.322 e 2.1.322 (§1.1) [U1, U2] |
| §1.1, requisiti | Node 18 o più; binario per Linux x64 e arm64 | Node 18.14 o più; binario anche per macOS e Windows, `claude.exe` da 331 MB (§1.2) [U1, U19; prova] |
| §2, «Strumenti che chiedono sempre» | `propose_action` marcato con `_meta["anthropic/requiresUserInteraction"]` | in `dontAsk` quel marchio fa negare lo strumento; e `tool()` non ha `_meta`. Il marchio va tolto (§1.4) [U8, U6] |
| §2, «Approvazioni lunghe»; §8 e §10.2, pezzo 3 | `defer` per le carte che aspettano una persona, poi ripresa | con lo strumento interno al processo la ripresa è instabile; funziona lo schema «in attesa» più `resume` con l'esito (§3.2) [prova, E7, E7d] |
| §2, «Hook» | dice che un `PreToolUse` scaduto blocca; non parla del gancio che va in errore | senza `onFailure: "block"` un gancio rotto lascia passare tutto (§3.2) [U15; prova, E17] |
| §2, «Tetti» | la spesa può superare il tetto dell'ultima risposta | in più: lo strumento dell'ultimo passo parte lo stesso, e così con `maxTurns` (§3.2) [prova, E16] |
| §2, «Sessioni»; §11, trascrizioni | `persistSession: false` per i lavori sensibili | incompatibile con i giri biforcati, che hanno bisogno del file della base; resta la cancellazione a scadenza [prova, E14] |
| §2, «Costi» | `total_cost_usd` come stima | resta una stima; in più una sessione ripresa o biforcata riparte dal totale salvato: la spesa di un giro è una differenza [U11; prova, E11] |
| §3.4, isolamento | «il processo riceve solo le variabili che gli passiamo» | su Windows Node rimette dieci variabili vere; e alcuni file finiscono fuori da `CLAUDE_CONFIG_DIR` (§6, punti 2 e 10) [prova, E5, E15] |
| §3.6, «orologio che ferma il processo» | fermare il processo | prima `interrupt()`, poi la sequenza del §10; `close()` da solo lascia `claude.exe` vivo 7 s [prova, E18] |
| §2 e §10.2, pezzo 7 | `SessionStore` su PostgreSQL | con un solo runner su una macchina basta il disco sotto `CLAUDE_CONFIG_DIR` [U21; proposta della fonte, §10] |

La raccolta non segnala altri punti superati: la scelta dell'SDK in TypeScript, la chiave API e il ruolo di LiteLLM restano. La misura di RAM del §3.3 (1 GiB come punto di partenza) resta quella ufficiale; la prova aggiunge una misura su sessioni brevi (§5).

### 9.2 In [ricerca/41 §8](41-novita-al-9-novembre.md)

- **§8.1, riga «Motore sull'Agent SDK + Cancello»**: «`defer` e carte, già native». Le carte sì, `defer` no: vedi sopra [prova, E7d].
- **§8.2 punto 4, modalità `auto` per le azioni interne**: delle tre condizioni, `onFailure: "block"` è confermata necessaria dalla prova [prova, E17]. `destructiveHint` non è stato provato. L'inoltro di `anthropic-beta`, `safeguards` e `safeguard_results` richiede LiteLLM e la chiave. Il consiglio della raccolta è di non usare `auto` nella milestone 2 (§10).
- **§8.3, prova 2** (gancio in errore con `onFailure: "block"`, strumenti con `destructiveHint: true`): la parte su `onFailure` è fatta con il copione e passa [prova, E17]; `destructiveHint` resta da provare. **Prova 1** (`auto` dietro LiteLLM): resta, e chiede chiave e LiteLLM (§8).
- **§1.2, partenza in Manual dalla 2.1.302**: il CHANGELOG la limita ai fornitori terzi (§6, punto 15) [U19].

---

## 10. Che cosa ne segue per la corsia S

Tutto questo paragrafo è [proposta]. Le scelte vanno nella decisione sulla corsia S, [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md), e nello spec della milestone 2. Le basi sono [ADR-0001](../docs/adr/0001-motore-agent-sdk.md) (versione fissata, aggiornata dopo i dieci scenari; ponte come gancio di callback), [ADR-0021](../docs/adr/0021-motore-a-due-corsie.md) (un runner, al massimo 6 sessioni; Claude nella corsia S) e [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md) (router a più motori).

1. **Versione**: 0.3.322 fissata esatta, senza `^`. Prima di ogni aggiornamento si legge il changelog e si rilancia il banco.
2. **Il ponte, lo strumento `proponi_azione`** (il `propose_action` di ricerca/26), sta in `allowedTools`. Il Cancello decide dentro il gestore dello strumento: la `POST /v1/proposte` risponde come per la corsia N: l'azione parte, va in carta o in finestra, oppure è negata. Niente `permission_policy: "always_ask"`, che in `dontAsk` è negato.
3. **Il gancio `PreToolUse`** resta come seconda barriera: uno solo, senza `matcher`, con `onFailure: "block"`, con l'elenco degli strumenti ammessi, la forma della chiave e un solo elemento esterno per giro. Per lo stop d'emergenza: `deny` più `continue: false`. Lo spec della milestone 2 dà al gancio l'elenco degli strumenti, il tetto e una sola azione con effetto per risposta; il solo elemento esterno per giro lo controllano il ponte e il Cancello, con due barriere ([ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)).
4. **L'attesa di una carta L1** segue lo schema E7: il gestore risponde «in carta», il giro finisce, il motore conserva l'id. L'evento `esito.registrato` riprende la sessione con un messaggio che porta l'esito. Niente `defer` sugli strumenti interni al processo.
5. **Giri biforcati e diario**: ogni giro parte dalla base con `forkSession: true`. La base nuova è solo un giro arrivato al `result` con il `terminal_reason` atteso. Un giro morto a metà si rifà dalla stessa base, mai con un `resume` semplice. Il diario degli effetti sta nella stessa transazione della carta. Lo spec deve scrivere la regola per quando gli argomenti differiscono: la chiamata non si riusa e decide il Cancello, con una chiave di contenuto. [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md) sceglie altre regole: la riga del diario si scrive prima dell'effetto, e un giro rifatto diverso non fa effetti nuovi, la sessione si ferma e una persona vede che cosa era già uscito.
6. **Spesa**: il motore conta i token per passo con `includePartialMessages: true` e li moltiplica per il proprio listino, come la corsia N. Superato il tetto, il gancio nega ogni strumento e il motore chiama `interrupt()`. `maxBudgetUsd` e `maxTurns` restano come rete di sicurezza. Il motore prende l'eccezione del ciclo e legge il `result` già ricevuto.
7. **Il motore legge `terminal_reason`**, non solo `subtype`: `hook_stopped`, `aborted_tools`, `budget_exhausted`, `max_turns`.
8. **Chiusura** del motore, sessione per sessione e in parallelo: smettere di accettare messaggi; `await q.interrupt()`; chiudere l'ingresso e aspettare il `result` al massimo 2 s; poi `q.close()`; dopo altri 3 s, chiudere l'albero dei processi di `claude.exe`. Il giro interrotto non si riprende: al riavvio si rifà dalla base. Lo spec della milestone 2 sceglie in un altro modo la chiusura ordinata: prima aspetta la fine dei giri aperti, al più la durata massima del giro, e manda questa sequenza solo a quelli ancora aperti ([ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)).
9. **Ambiente**: l'elenco del §7.2, tutto scritto da noi, con `CLAUDE_CONFIG_DIR` per sessione, come al punto 10.
10. **Trascrizioni**: nella milestone 2 su disco, sotto `CLAUDE_CONFIG_DIR` per sessione, come decide [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md): le sessioni di clienti diversi non stanno nella stessa cartella. Lo spec della milestone 2 scarta il `SessionStore` su PostgreSQL, che copia la sessione solo «al meglio». Sono dati di terzi in chiaro: cancellazione a scadenza dei rami morti e delle basi vecchie. Il filtro di oscuramento della milestone 1 non le tocca [verificato: prova, «Problemi e limiti»].
11. **Strumenti di serie**: nessuno. Le regole «Come lavoro» della persona vanno nel `systemPrompt`. I sottoagenti restano fuori dalla milestone 2.
12. **Ricerca degli strumenti**: `alwaysLoad: true` sul nostro server e `ENABLE_TOOL_SEARCH=false`, per non dipendere da un comportamento non scritto. Lo spec della milestone 2 tiene solo `alwaysLoad: true` e controlla l'elenco degli strumenti all'avvio di ogni giro.
13. **Processi**: un processo per sessione attiva; le sessioni ferme si chiudono, perché la ripresa costa circa 1 s di avvio. Il numero di sessioni insieme si fissa su questa base e sulla misura del picco.
14. **Modalità `auto`**: mai nella milestone 2. Si riprende con LiteLLM e la chiave, nella milestone 3.
15. **Router a più motori**: nella milestone 2 del PRD, sul decisore che c'è, come decide la revisione del 12 novembre di [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md). Jev e LiteLLM restano nella milestone 3.
16. **Prove**: il copione della milestone 1 si estende come al §4.3. Le prove della corsia S avviano l'SDK vero, con il binario del pacchetto, un ambiente isolato per prova e il proxy spia come cintura: un host registrato fa fallire la prova. Il copione dichiara token noti, così le prove su spesa e tetti sono deterministiche. Il giro dal vivo con la chiave (§8) viene dopo, appena la chiave c'è.

---

## Fonti

**Pagine web, lette il 12/11/2026**
- U1 https://registry.npmjs.org/@anthropic-ai/claude-agent-sdk/latest
- U2 https://registry.npmjs.org/@anthropic-ai/claude-agent-sdk (campi `dist-tags` e `time`)
- U3 https://code.claude.com/docs/en/agent-sdk/overview.md
- U4 https://code.claude.com/docs/en/agent-sdk/quickstart.md
- U5 https://code.claude.com/docs/en/agent-sdk/hosting.md
- U6 https://code.claude.com/docs/en/agent-sdk/typescript.md (Options, Query, `tool()`, `createSdkMcpServer()`, SDKResultMessage, SDKSystemMessage, McpServerToolPolicy)
- U7 https://code.claude.com/docs/en/agent-sdk/custom-tools.md
- U8 https://code.claude.com/docs/en/agent-sdk/permissions.md
- U9 https://code.claude.com/docs/en/agent-sdk/claude-code-features.md
- U10 https://code.claude.com/docs/en/llm-gateway-protocol.md
- U11 https://code.claude.com/docs/en/agent-sdk/cost-tracking.md
- U12 https://code.claude.com/docs/en/legal-and-compliance.md
- U13 https://code.claude.com/docs/en/hooks.md («Defer a tool call for later»)
- U14 https://code.claude.com/docs/en/data-usage.md
- U15 https://code.claude.com/docs/en/agent-sdk/hooks.md
- U16 https://code.claude.com/docs/en/agent-sdk/user-input.md
- U17 https://code.claude.com/docs/en/setup.md
- U18 https://registry.npmjs.org/@anthropic-ai/claude-code (campo `dist-tags`)
- U19 https://raw.githubusercontent.com/anthropics/claude-agent-sdk-typescript/main/CHANGELOG.md (voci 0.3.300-0.3.322)
- U20 https://code.claude.com/docs/en/agent-sdk/tool-search.md
- U21 https://code.claude.com/docs/en/agent-sdk/sessions.md
- U22 https://code.claude.com/docs/en/agent-sdk/agent-loop.md
- U23 https://code.claude.com/docs/en/llm-gateway-connect.md
- Letta per la prova: https://code.claude.com/docs/en/env-vars
- Context7, libreria `/websites/code_claude_en_agent-sdk`, per un controllo incrociato su `dontAsk`, `alwaysLoad` e ricerca degli strumenti.

**La prova**
- La prova del 12/11/2026, parti 2 e 3, esperimenti E1-E18. I registri (`registri/E1` … `registri/E18`, `registri/verifica.txt`) e le copie delle pagine lette stanno nella cartella della prova. Il pacchetto provato è `@anthropic-ai/claude-agent-sdk` 0.3.322; i tipi letti sono quelli del suo `sdk.d.ts`.

**Documenti della repo**
- [ricerca/26, Agent SDK](26-claude-agent-sdk.md), per intero
- [ricerca/41, novità al 9 novembre, §1 e §8](41-novita-al-9-novembre.md)
- [ricerca/45, architettura v3, §3.1 e §6.1](45-architettura-v3.md)
- [ADR-0001](../docs/adr/0001-motore-agent-sdk.md) · [ADR-0004](../docs/adr/0004-litellm-banca-token.md) · [ADR-0021](../docs/adr/0021-motore-a-due-corsie.md) · [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md) · [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md) · [docs/adr/README.md](../docs/adr/README.md)

**Repo del codice** (citata senza collegamenti): il PRD (perimetro, milestone, tabella dei rischi), lo spec della milestone 1 (§2.4 e §11.2, PROVA-M1) e il server del copione della milestone 1.
