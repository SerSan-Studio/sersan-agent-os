# 53. NVIDIA auto-ontology e il server MCP derivato: uno strato semantico per i numeri

- **Data**: 20 novembre 2026. Le fonti citate sono state lette il 20 novembre 2026. Un lettore ha raccolto i fatti nelle due repo, fissate a un commit; i fatti su cui poggia il giudizio li ho ricontrollati nel codice e sulle pagine di GitHub lo stesso giorno.
- **Revisione dello stesso giorno**: una verifica indipendente ha controllato le affermazioni del rapporto. Questa versione accoglie le sue correzioni. Le più importanti: il server MCP di lettura di SersanOutreach, che il primo testo non contava (§1.3); i voti di D ed E (§6.3); la regola sui dati rossi, ora uguale per A, B e C (§2).
- **Per chi**: Alberto, che ha dato la direttiva; Michele, a cui restano infrastruttura, fornitori e board; chi scriverà gli spec delle catene che calcolano numeri (Report del mattino, Banca dei token, Analista metriche, Controllo di gestione).
- **La direttiva di Alberto del 20 novembre 2026**, parola per parola: «in aggiunta , vedi se questa pubblicazione di nvidia ci puo servire e migliorare l'architettura : https://github.com/NVIDIA/auto-ontology , https://github.com/gogoymh/auto-ontology-mcp»
- **Domande a cui risponde**:
  1. Che cosa sono davvero le due pubblicazioni, rispetto a quello che il nome fa pensare? Nel progetto c'era già qualcosa di simile?
  2. Che cosa farebbero nel progetto, per quali agenti e funzioni, e che cosa chiedono al disegno: stack, modelli, GPU, dati che escono, sicurezza?
  3. Come stanno le alternative, con i sei criteri pesati del progetto?
  4. Migliorano l'architettura? Che cosa cambierebbe nei documenti, e a quali condizioni misurabili conviene riguardarle?
  5. Che cosa resta da chiedere alle persone, e che cosa non è verificato?
- **Le due repo lette**:
  - **auto-ontology** di NVIDIA, al commit [`43fa2d3`](https://github.com/NVIDIA/auto-ontology/tree/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168) del 19 novembre 2026; nel testo la chiamo «auto-ontology»;
  - **auto-ontology-mcp** dell'account gogoymh, al commit [`0fb5ecf`](https://github.com/gogoymh/auto-ontology-mcp/tree/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a) del 18 novembre 2026; nel testo la chiamo «il server MCP derivato».
  - I rimandi al codice puntano al file su quel commit, con le righe.
- **Cosa aggiorna**: la regola dei numeri di [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md) e di [docs/04-tech-stack.md §3](../docs/04-tech-stack.md); il riassunto delle valutazioni di [docs/02-alternative.md §10](../docs/02-alternative.md); la domanda 25 di [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md), con una domanda nuova. [ricerca/12 §6](12-altre-piattaforme.md) resta solo come confronto. Le revisioni proposte sono nel §9: nessuna ADR è stata modificata.
- **Legenda**:
  - `[verificato: fonte, data]`: letto sulla fonte indicata;
  - `[non verificato: motivo]`: stima, deduzione, o dato che la fonte primaria non conferma;
  - `[proposta]`: una scelta di disegno di questo rapporto;
  - `[calcolo]`: un conto fatto da me su dati citati.
- **Cosa non ho fatto**: niente installazioni; nessun file delle due repo eseguito; nessun account, nessuna chiave, nessuna chiamata ai modelli. Ho letto il codice e i metadati pubblici di GitHub (issue, pull request, classifiche) in sola lettura. Le istruzioni per agenti che le repo contengono (per esempio `AGENTS.md`, `CLAUDE.md` e le istruzioni che il server MCP derivato manda al client) le ho lette come dati e non seguite.

### Parole usate spesso

- **Strato semantico** (*semantic layer*): un catalogo che dice, per ogni parola del lavoro («cliente», «fattura», «margine»), dove sta nelle basi dati, come si collega al resto e come si calcola.
- **Ontologia**: nelle due repo vuol dire strato semantico. Non è l'ontologia formale dei linguaggi OWL o RDF.
- **Termine**: una parola del lavoro, con descrizione e sinonimi, legata a tabelle e colonne.
- **Misura**: un calcolo con un nome, scritto in SQL e rivisto da una persona; auto-ontology la chiama *SQL attribute*. **Misura certificata**: una misura che una persona ha controllato e firmato.
- **Join**: il collegamento fra due tabelle attraverso una colonna in comune.
- **Text-to-SQL**: un modello che riceve una domanda in parole e scrive la query SQL che la risponde.
- **Ciclo ReAct**: un modello che sceglie da solo, a ogni passo, quale strumento chiamare, finché non risponde.
- **Endpoint**: l'indirizzo di un servizio a cui un programma manda le richieste, per esempio quelle a un modello.
- **Embedding** e **reranker**: il vettore di numeri che rappresenta un testo per cercarlo per significato, e il modello che riordina i risultati della ricerca.
- **Rollback**: l'annullamento di una transazione del database, così che niente di ciò che ha fatto resti.
- **Release**: una versione pubblicata con un numero, che si può installare e citare.
- **MCP**: il protocollo con cui un agente usa strumenti esterni.
- **Apache Ossie**: una specifica aperta, in YAML o JSON, per scambiare strati semantici fra strumenti.

---

## In breve

1. **Il nome inganna: non è un'ontologia dei testi né un grafo per la memoria.** auto-ontology è uno strato semantico sopra basi dati SQL. Un modello lo genera dallo schema e da campioni dei dati. Poi un agente risponde alle domande; per quelle che chiedono un calcolo scrive SQL. Sul ramo principale non legge documenti e non produce OWL né RDF. Il server MCP derivato non è di NVIDIA. È un lavoro indipendente, nato il 6 novembre 2026: rifà la parte senza modelli su file SQLite e lascia il lavoro linguistico al modello del client. In più tiene una base di conoscenza personale in un vault Obsidian (§1, §3).
2. **Nel progetto c'erano la regola e, per il CRM, anche lo strumento.** [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md) dice che i numeri si calcolano dal codice sui dati. Il server MCP di lettura di SersanOutreach ha 19 strumenti. Quattordici danno i numeri del CRM con un nome (pipeline, funnel, vinti e persi, meeting e altri) e rispondono con lo stesso numero della pagina dell'applicazione. Il collegamento al motore è previsto dalla fase 2. Per i dati del sistema ricerca/29 propone un server MCP della memoria con strumenti a parametri. Mai valutati, invece, uno strato semantico generato sulle basi dati e un agente che scrive SQL (§1.3).
3. **Il caso più forte per adottarlo adesso è serio, ma non regge.** A favore: NVIDIA, licenza Apache-2.0, sviluppo quotidiano, sola lettura controllata, l'SQL restituito con ogni risposta, modelli intercambiabili, il governo dei significati fra molti agenti. Contro, oggi: le funzioni dove pesa di più arrivano dalle fasi 3-6. Il suo agente scrive SQL a ogni domanda di calcolo, mentre ADR-0005 vuole numeri calcolati dal codice. E le prove pubbliche sono deboli: il «#1» su BEAVER vale il 14,1% di risposte giuste, 0,1 punti sopra il secondo, con lo stesso modello Claude (§6.1, §6.2).
4. **I voti**, su 100: E. non fare niente adesso **78,5**; D. strato semantico scritto a mano **72,0**; C. server MCP derivato **51,0**; A. auto-ontology con i modelli di NVIDIA **49,5**; B. auto-ontology dietro LiteLLM **47,5**. Nessuna è esclusa, ma A, B e C rispettano i limiti fissi solo lontano dalle tabelle rosse, cioè proprio dalla finanza (§2, §6.3).
5. **auto-ontology (A e B): non ora.** Con i modelli di NVIDIA manda nomi, campioni e righe dei risultati a un fornitore fuori dal board. Dietro LiteLLM può ragionare con Claude, ma porta uno stack nuovo: Next.js, due servizi FastAPI, PostgreSQL 17 con pgvector accanto a Qdrant. Vuole vettori larghi 2048, mentre il nostro embedding arriva a 1024. Ha porte interne senza autenticazione, nessuna release e issue aperte che toccano i numeri, una proprio sui connettori PostgreSQL (408) (§5, §6.3).
6. **Il server MCP derivato (C): non ora.** È leggero, ma ha due settimane di vita, un autore principale, nessuna release e due correzioni di sicurezza aperte. Consegna al modello campioni e righe senza un colore e senza un filtro per cliente, due cose che le regole del ponte della corsia S chiedono ([ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)) (§5, §6.3).
7. **«Non fare niente adesso» vince, fuori dal margine.** E sta 6,5 punti sopra D. Il catalogo completo, con esecutore, strumenti, regola del router e cambio del controllo del contenuto, oggi non si ripaga. I numeri del CRM hanno già uno strumento. I lavori con numeri rossi, nelle assegnazioni proposte per il router, vanno a una catena N in casa; all'API e alla corsia S il rosso andrebbe solo oscurato. Le domande libere arrivano nella fase 3, e i documenti le danno ai testi (§4, §6.3, §7).
8. **Dell'idea resta una regola, che non costa lavoro in più.** Quando una catena calcola un numero che nessuno strumento esistente dà già, lo si definisce una volta sola, con un nome, e lo riusano le altre catene e i pannelli. Per i numeri del CRM la definizione è quella del server MCP di SersanOutreach. Gli agenti non scrivono SQL. È la revisione proposta per ADR-0005 (§7, §9).
9. **Apache Ossie, il formato aperto che auto-ontology esporta, è ancora una bozza** (versione 0.3.0.dev0). Non serve adesso (§3.3).
10. **Migliora l'architettura? Il prodotto no; l'idea solo come regola di scrittura.** Le condizioni misurabili per riguardare auto-ontology, il server derivato e il catalogo completo sono nel §8.

---

## 1. La direttiva: che cosa sono davvero, e che cosa c'era già

La direttiva chiede se le due pubblicazioni servono e se migliorano l'architettura. Il giudizio usa i sei criteri del progetto, come per ogni altra alternativa: niente è obbligatorio.

### 1.1 auto-ontology

| Il nome fa pensare a | Che cos'è | Fonte |
|---|---|---|
| un'ontologia ricavata da documenti e testi | uno strato semantico sopra basi dati SQL, ricavato dai **metadati** delle basi dati: schema, chiavi, viste, cronologia delle query e campioni dei valori | [verificato: [README, righe 12-20](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L12-L20); [docs/architecture.md, righe 126-133](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L126-L133), 20/11/2026] |
| un'ontologia formale (OWL, RDF) | sei elementi: termine, legame con tabelle e colonne, relazione, misura, provenienza, certificazione; si salvano in PostgreSQL con pgvector e si scambiano in Apache Ossie. Il README parla anche di «AI-ready knowledge graphs», ma nessun file produce OWL, RDF o SPARQL | [verificato: [README, righe 141-150](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L141-L150), [riga 16](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L16) e [righe 165-166](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L165-L166), 20/11/2026]; l'assenza dei formati [verificato: ricerca nel codice del lettore dei fatti, 20/11/2026] |
| un grafo di conoscenza per la memoria degli agenti | un **prodotto di analisi dei dati**: un agente che risponde a domande sui numeri, con il grafico in chat | [verificato: [README, righe 185-216](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L185-L216), 20/11/2026] |
| uno strumento che legge i nostri documenti | i documenti non entrano sul ramo principale. Una richiesta aperta il 18 novembre li chiede; il lavoro sta in una pull request non unita, intitolata «Replace NeMo Retriever with a fully hosted document extractor» | [verificato: [issue 571](https://github.com/NVIDIA/auto-ontology/issues/571); [pull request 386](https://github.com/NVIDIA/auto-ontology/pull/386), titolo e stato, 20/11/2026] |

Il README stesso dice quando serve [verificato: [README, righe 22-32](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L22-L32), 20/11/2026]:
- domande varie, aperte e ambigue;
- dati sparsi su molte fonti con definizioni in conflitto;
- significati da riusare e governare fra esecuzioni, squadre e agenti;
- un modello che non riesce a tenere tutta la documentazione;
- persone che chiedono con le parole del lavoro e vanno portate alla fonte giusta ([riga 29](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L29)).

E aggiunge: «With one well-modeled source and a fixed set of questions, direct SQL may be enough». Con una sola fonte ben modellata e domande fisse, l'SQL diretto può bastare.

### 1.2 Il server MCP derivato

- **Non è di NVIDIA.** Dichiara di non essere «affiliated with, sponsored by or endorsed by NVIDIA» [verificato: [README, riga 730](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L730), 20/11/2026]. Prende regole, prompt e parti di codice di auto-ontology e lo dichiara file per file [verificato: [NOTICE](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/NOTICE), 20/11/2026].
- **Non chiama auto-ontology.** Le sue dipendenze sono solo `fastmcp`, `pyyaml`, `sqlalchemy` e `sqlglot` [verificato: [pyproject.toml, righe 13-18](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/pyproject.toml#L13-L18), 20/11/2026].
- **Nessun modello nel server.** Leggere, estrarre, dare i nomi, giudicare e scrivere SQL lo fa il modello del client MCP. Il server tiene la parte deterministica: schema, profilo delle colonne, chiavi, validazione, archivio ed esecuzione in sola lettura, in file SQLite [verificato: [README, riga 34](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L34), 20/11/2026].
- **Due lavori**: lo strato semantico sulle basi SQL e una «personal knowledge base» per documenti, ricevute e appunti, con gli originali in un vault Obsidian [verificato: [README, righe 26-34](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L26-L34), 20/11/2026].
- **Che cosa lascia fuori** di auto-ontology: interfaccia web, utenti e permessi, rilevamento dei dati personali, ricerca per significato e scambio in Ossie. Esporta in un YAML suo [verificato: [README, riga 613](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L613), 20/11/2026].

### 1.3 Che cosa c'era già nel progetto

| Che cosa | Dove | Che cosa dice | Rapporto con le due repo |
|---|---|---|---|
| La regola dei numeri | [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md), «Decisione»; [docs/04-tech-stack.md §3](../docs/04-tech-stack.md) | «I numeri si calcolano dal codice sui dati, non si cercano nel testo» | è lo stesso problema che auto-ontology dichiara, risolto in un altro modo: il codice calcola, il modello non scrive SQL |
| **Il server MCP di lettura di SersanOutreach** | [PRESENTAZIONE-CEO.md §7.3](../PRESENTAZIONE-CEO.md); [docs/03-architettura.md](../docs/03-architettura.md); [docs/06-sviluppo.md](../docs/06-sviluppo.md); [README del server](../allegati/sersanoutreach/mcp_server-README.md) | 19 strumenti in sola lettura: KPI, coda delle azioni, pipeline, funnel, risposte positive, meeting, analisi dei deal persi. I 14 del Growth OS rispondono «with the number the app's page shows»; «Nothing is recomputed that a page shows, and nothing writes». Oggi le prese sono «pronte ma non collegate»: dalla fase 2 gli agenti le raggiungono dal motore con un accesso per squadra | per i numeri del CRM è già uno strumento con misure dal nome e una definizione sola, quella delle pagine. Nella corsia S la sessione usa solo strumenti del ponte, che incapsula gli strumenti esterni ([ADR-0001](../docs/adr/0001-motore-agent-sdk.md); [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)) |
| La memoria su PostgreSQL come server MCP | [docs/04-tech-stack.md](../docs/04-tech-stack.md), riga «Server MCP»; [ricerca/29 §7.1](29-conoscenza-task-e-documenti.md) | nella fase 2 un server MCP della memoria su PostgreSQL; ricerca/29 propone strumenti in lettura a parametri: `obiettivi()`, `meeting(cliente, periodo)`, `decisioni(cliente)` | per i dati del sistema c'è già la forma di uno strumento a parametri; ADR-0029 dice che gli strumenti nuovi «arrivano con l'agente che li chiede» |
| Il controllo del contenuto | [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md); [ADR-0027](../docs/adr/0027-decisore.md) | prima di un'uscita L2 o L3, cifre, prezzi e date che non vengono dal CRM portano l'azione a L1; cifre e date le trova il codice, le domande di significato le fa il decisore | protegge chi riceve da un numero inventato |
| Le fonti delle cifre nella corsia S | [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md), regole fisse del ponte | «le fonti (cifre e date) le mette il ponte, dai dati»; gli strumenti leggono solo i dati del cliente del compito; il colore è il più alto letto dalla sessione | uno strato semantico deve rispettare le stesse regole |
| Grafana sui numeri | [PRESENTAZIONE-CEO.md, appendice A, C5 e L3](../PRESENTAZIONE-CEO.md); [docs/04-tech-stack.md](../docs/04-tech-stack.md) | registro dei meeting e controllo di gestione in PostgreSQL, visti in Grafana | i pannelli non esistono ancora; avranno il loro SQL, scritto da persone |
| Grafi di conoscenza per la memoria | [ricerca/12 §6](12-altre-piattaforme.md); [ricerca/20, proposta G](20-proposta-G-ibrido.md); [ricerca/29 §7.1](29-conoscenza-task-e-documenti.md) | Graphiti e Zep, grafo temporale per agenti, «se serve»; mcp-memory, grafo in un file, resta un taccuino | riguardano i testi e la memoria degli agenti, non le basi dati |
| La ricerca nei testi | [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md); [docs/04-tech-stack.md §3](../docs/04-tech-stack.md) | Qdrant con ricerca ibrida e reranker, una sola porta (MCP RAG) | la base di conoscenza del server MCP derivato fa la stessa cosa in piccolo, per una persona |

**Mai valutati**: uno strato semantico generato sopra le basi dati, e un agente che scrive SQL. Il disegno va nella direzione opposta: nella corsia N il codice sceglie i passi e il modello scrive a schema senza strumenti ([ricerca/45 §1.2](45-architettura-v3.md)).

---

## 2. Come si giudica

- **Pesi**, gli stessi di [ricerca/45](45-architettura-v3.md) (riga 34, «Pesi del giudizio, fissati prima») e di [ricerca/52 §2](52-n8n-moda-elevenlabs.md): autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10.
- **Voti da 0 a 10** per criterio. Il totale è la somma di voto × peso, divisa per 10, quindi su 100.
- **Margine**: uno scarto fino a 3 punti sta dentro il margine di giudizio, come in [ricerca/46](46-obsidian-come-casa-dei-testi.md) e in ricerca/52. Dentro il margine si sceglie sulle condizioni e sui fatti, non sui totali [proposta].
- **Limiti fissi**: un'alternativa che viola un limite fisso è esclusa qualunque sia il totale. I limiti sono:
  - agli agenti mai cancellazioni né credenziali;
  - pagamenti mai automatici;
  - stop di emergenza sempre;
  - i dati rossi restano sul server, oppure vanno all'API di Anthropic dopo l'oscuramento locale, che toglie i dati personali che non servono ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)). Nel router il rosso va in chiaro solo a una regola, a una catena N in casa o a una persona; all'API e alla corsia S solo oscurato; alla corsia T mai ([ricerca/49 §2.2, regola 4](49-instradamento-a-piu-motori.md); [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)). La scala «1 → 2 → 6» di ADR-0028 è un'altra cosa: dice dove sale un lavoro rosso quando c'è un dubbio;
  - ogni azione verso fuori passa dal Cancello al suo livello ([ricerca/45 §2.5](45-architettura-v3.md); [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md)).
- **La stessa regola per tutti**: un'alternativa che può collegarsi alle tabelle rosse e farne uscire i valori senza oscuramento viola il limite. Si giudica quindi limitata alle tabelle non rosse, e lo si scrive [proposta].
- **Fornitori**: il giallo va solo ai fornitori del board con DPA ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)). I fornitori di modelli open-weight ricevono verde e giallo, mai rosso ([ADR-0025](../docs/adr/0025-un-modello-per-agente.md)); quali fornitori sono ammessi per il giallo lo decide Michele ([ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)). Un servizio nuovo sul server entra nel board con il sì di Michele e un responsabile delle patch ([ADR-0002](../docs/adr/0002-self-hosted-board-michele.md)). Nel tempo al valore il sì di Michele conta per ogni strumento nuovo [proposta]; ricerca/52 lo contava per ogni strumento fuori dal board.
- **Il ruolo confrontato**: dare agli agenti, e attraverso loro alle persone, numeri giusti presi dalle nostre basi dati.
- **Fuori perimetro**: gli strati semantici aperti già noti, che compilano misure con un nome in SQL (per esempio Cube o MetricFlow). La direttiva chiede di due repo, e nei documenti del progetto non sono mai comparsi. Se un giorno il catalogo completo (D) tornasse utile (§8), andrebbero confrontati allora [proposta].
- I voti sono un giudizio sui fatti raccolti [proposta].

---

## 3. I fatti

### 3.1 auto-ontology

**Come genera lo strato semantico.**
- Legge da ogni connessione tabelle, colonne, chiavi, viste e, dove il motore la espone, la cronologia delle query. Per ogni tabella campiona fino a 1.000 righe. I valori campionati, fino a 30 caratteri, entrano nei prompt che scrivono le descrizioni delle colonne [verificato: [docs/architecture.md, righe 141-160](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L141-L160); [semantic/visit_enter.py, righe 64 e 81](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/visit_enter.py#L64-L81); [semantic/deterministic.py, righe 116-129](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/deterministic.py#L116-L129), 20/11/2026].
- **Le colonne marcate come dati personali restano fuori.** Una colonna con l'etichetta PII non entra nella query di campionamento, e i suoi valori non arrivano mai a un prompt. L'etichetta può venire dal rilevamento automatico, da una persona o da una regola; i valori già salvati si tolgono quando l'etichetta arriva [verificato: [semantic/visit_enter.py, righe 498-503 e 903-907](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/visit_enter.py#L498-L503); [semantic/pii_values.py, righe 1-28](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/pii_values.py#L1-L28), 20/11/2026]. Il rilevamento automatico è spento di serie; se lo si accende, le colonne che le regole non sanno decidere vanno a un modello [verificato: [docs/architecture.md, riga 142](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L142), 20/11/2026].
- Un modello trova le chiavi esterne, scrive le descrizioni, dà i nomi ai termini e propone misure dalla cronologia delle query. Le chiavi trovate dal modello si confermano con una query sui dati. Tutte le chiamate di questa fase usano il modello di ragionamento, tre tabelle alla volta, al massimo 6 richieste insieme [verificato: [docs/architecture.md, righe 146-177](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L146-L177), 20/11/2026].
- La generazione è spenta finché un amministratore non la accende. Poi gira all'avvio, una volta al giorno e a richiesta, e tratta solo le tabelle senza termine. Le modifiche delle persone restano, tranne la scelta del join, che si rifà a ogni giro [verificato: [docs/architecture.md, righe 120-124 e 185-189](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L120-L124), 20/11/2026].
- Quando un passo del modello fallisce, la generazione salva un termine segnaposto come se fosse vero: è un bug aperto dal 16 novembre [verificato: [issue 533](https://github.com/NVIDIA/auto-ontology/issues/533), 20/11/2026].

**Come risponde.**
- Un ciclo ReAct: il modello di ragionamento parte senza schema e sceglie da solo gli strumenti `retrieve`, `run_sql` e `submit`. Limiti di serie: 24 chiamate a strumenti e 10 esecuzioni SQL per domanda. `run_sql` mostra al modello fino a 100 righe, entro 8.000 caratteri per risultato e 120 per cella [verificato: [docs/architecture.md, righe 197-203, 241-252 e 275-282](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L275-L282); [run_sql.py, riga 50](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/retrieval/text_to_sql/react/run_sql.py#L50), 20/11/2026].
- **Il modello scrive l'SQL a ogni domanda che chiede un calcolo.** Le domande sui dati stessi (quali tabelle ci sono, che cosa vuol dire un termine, come è definita una misura) hanno risposta senza SQL [verificato: [docs/architecture.md, righe 254-258](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L254-L258), 20/11/2026].
- Le misure rivedute arrivano al modello come definizioni da riusare. Certificare un elemento lo segna come rivisto, ma «doesn't change how the agent retrieves» [verificato: [docs/architecture.md, righe 190-191](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L190-L191), 20/11/2026]. Il README dice invece che le misure si riusano «so answers compute each measure the same way» [verificato: [README, riga 148](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L148), 20/11/2026]. Se il modello le riusi davvero dipende dal modello.
- **Chiarimenti.** L'agente della chat non li chiede: «The ReAct agent doesn't ask clarifying questions» [verificato: [docs/architecture.md, righe 262-271](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L262-L271), 20/11/2026]. Un agente collegato via MCP chiama prima `check_answerable`, che misura quanto lo strato copre la domanda, e poi chiede chiarimenti alla persona [verificato: [README, righe 117-129](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L117-L129); [docs/architecture.md, righe 304-318](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L304-L318), 20/11/2026]. Nel codice c'è anche un flusso facoltativo che decide se chiedere un chiarimento prima di scrivere SQL [verificato: [retrieval/interactive/clarify.py, righe 5-11](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/retrieval/interactive/clarify.py#L5-L11); [.env.example, righe 87-93](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/.env.example#L87-L93), 20/11/2026].
- Se nessuna query passa, rifiuta di rispondere [verificato: [docs/architecture.md, righe 262-269](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L262-L269), 20/11/2026].
- **Controlli prima dell'esecuzione**: nomi di tabelle e colonne confrontati con il catalogo; scritture e funzioni pericolose rifiutate sull'albero della query; esecuzione in una transazione di sola lettura [verificato: [retrieval/text_to_sql/react/run_sql.py, righe 5-18 e 52-85](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/retrieval/text_to_sql/react/run_sql.py#L52-L85), 20/11/2026]. Questi controlli fermano un nome sbagliato, non una query valida che calcola la cosa sbagliata [non verificato: deduzione].

**Modelli.**
- Quattro ruoli: ragionamento, senza ragionamento, embedding, reranker. Con una chiave `nvapi-` i valori di serie sono modelli Nemotron ospitati da NVIDIA (`integrate.api.nvidia.com`, `ai.api.nvidia.com`). Per i primi due ruoli è `nemotron-3.5-lightning-30b-a3b`, da 30 miliardi di parametri; poi un embedding da 1 miliardo e un reranker da 8 [verificato: [utils/model_config.py, righe 29-55](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/model_config.py#L29-L55); [README, righe 415-423](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L415-L423), 20/11/2026]. Dal nome, il primo è un modello a esperti con circa 3 miliardi di parametri attivi [non verificato: dal suffisso del nome].
- **Ripiego**: se la chiave non comincia con `nvapi-`, ogni campo non impostato prende i valori del gateway `inference-api.nvidia.com`, con nomi di modelli Claude [verificato: [utils/model_config.py, righe 15-18, 30 e 83-89](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/model_config.py#L83-L89), 20/11/2026]. La repo di valutazione di NVIDIA lo usa con una chiave «NVIDIA-internal» [verificato: [README di auto-ontology-eval, righe 132-135](https://github.com/NVIDIA/auto-ontology-eval/blob/e727e4d6e1e198355099de4803590bb3681793a4/README.md#L132-L135), 20/11/2026]. Anche le chiavi virtuali di LiteLLM cominciano con `sk-`: quindi con LiteLLM ogni campo va scritto [non verificato: deduzione].
- Si può puntare a qualunque endpoint compatibile con l'API di OpenAI, con modelli che sappiano rispondere a schema [verificato: [README, righe 425-431](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L425-L431), 20/11/2026]. Nel codice però solo i nomi che cominciano con `openai/`, `azure/` o `aws/` passano per il client OpenAI; tutti gli altri passano per il client di NVIDIA. Il nome viaggia così com'è, prefisso compreso [verificato: [utils/llm_invoke.py, righe 224-254](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/llm_invoke.py#L224-L254), 20/11/2026].
- Con l'API ospitata di NVIDIA la risposta a schema fallisce a intermittenza: bug aperto dal 6 novembre [verificato: [issue 440](https://github.com/NVIDIA/auto-ontology/issues/440), 20/11/2026].
- **Embedding.** La richiesta aggiunge tre campi propri di NVIDIA (`input_type`, `truncate`, `modality`). La colonna dei vettori è fissa a 2048 dimensioni [verificato: [utils/embedding.py, righe 188-199](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/embedding.py#L188-L199); [vdb/postgres.py, righe 176 e 283-304](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/vdb/postgres.py#L283-L304), 20/11/2026]. Una pull request aperta, la 411, fa restituire 2048 dimensioni ai modelli più larghi; quelli più stretti restano esclusi: «dimensions only shortens, so they need a configurable column width» [verificato: [pull request 411](https://github.com/NVIDIA/auto-ontology/pull/411), testo e stato, 20/11/2026]. Una colonna di larghezza configurabile oggi non la propone nessuna pull request [verificato: pull request aperte, 20/11/2026].
- Il reranker serve solo in un passo della generazione, le tabelle ponte; per rispondere non si usa [verificato: [docs/architecture.md, riga 177](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L177), 20/11/2026].
- **GPU.** Tutti e quattro i ruoli sono endpoint remoti, quindi con i modelli ospitati non serve una GPU locale; per il reranker lo dice anche il codice [verificato: [README, righe 244 e 425-431](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L425-L431); [utils/rerank.py, riga 29](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/rerank.py#L29), 20/11/2026]. Requisiti di memoria video per ospitare i modelli in casa: non trovati [non verificato: assenti nella documentazione]. I pesi del modello da 30 miliardi a 4 bit fanno circa 15 GB, quelli del reranker circa 4 GB, quelli dell'embedding in FP16 circa 2 GB [calcolo].

**Servizi, stack e porte.**
- I servizi:
  - un'interfaccia web in Next.js 16, con Better Auth e Prisma;
  - due servizi FastAPI, uno per le risposte e uno per la generazione;
  - PostgreSQL 17 con pgvector, che tiene catalogo, strato semantico, vettori e dati dell'applicazione;
  - pgAdmin, acceso di serie ma spegnibile;
  - facoltativi HashiCorp Vault e il servizio di previsioni KumoRFM.

  [verificato: [README, righe 265-272](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L265-L272); [frontend/package.json, riga 37](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/frontend/package.json#L37); [docker-compose.yml, righe 7 e 24-37](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docker-compose.yml#L24-L37); [helm/auto-ontology/values.yaml, righe 111-121](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/helm/auto-ontology/values.yaml#L111-L121), 20/11/2026]
- Python dalla 3.12 alla 3.13. Le immagini per amd64 e arm64 le costruisce il flusso di rilascio, e il chart Helm le prende da `nvcr.io` [verificato: [pyproject.toml, righe 7-8](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/pyproject.toml#L7-L8); [.github/workflows/release-docker.yml, righe 5-9](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/.github/workflows/release-docker.yml#L5-L9); [helm/auto-ontology/values.yaml, righe 143-146](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/helm/auto-ontology/values.yaml#L143-L146), 20/11/2026].
- **Porte interne senza autenticazione.** Il servizio delle risposte si fida dell'intestazione `x-auto-ontology-user-id` che l'interfaccia gli passa. Il servizio di generazione non ha autenticazione su ingest, cancellazione, azzeramento e compilazione. Il README chiede di tenere le porte 3001 e 3002 in una rete privata [verificato: [README, righe 274-279](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L274-L279), 20/11/2026]. Il file Docker Compose le pubblica senza indirizzo di bind, insieme a PostgreSQL e a pgAdmin `latest` sulla 5050 [verificato: [docker-compose.yml, righe 10-11, 25-29, 46-47 e 75-76](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docker-compose.yml#L46-L47), 20/11/2026].
- Il file di esempio delle variabili contiene credenziali d'esempio, da sostituire [verificato: [.env.example, righe 84-86](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/.env.example#L84-L86), 20/11/2026]. Qui non le ricopio.
- **Il server MCP ufficiale** ha 9 strumenti in sola lettura, fra cui `check_answerable` e `ask_question`. È un client HTTP dell'API, e ogni chiamata gira con i permessi della persona che è entrata [verificato: [README, righe 286-297](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L286-L297); [mcp/README.md, righe 58-74](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/mcp/README.md#L58-L74), 20/11/2026]. Di serie ascolta su `0.0.0.0:3003` e non fa parte di Compose né di Helm [verificato: [docs/mcp.md, righe 181-183](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/mcp.md#L181-L183); [docs/architecture.md, righe 77-80](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md#L77-L80), 20/11/2026]. Il suo pacchetto si chiama `auto-ontology-mcp`, come il server derivato, e si installa da GitHub perché non è su PyPI [verificato: [mcp/pyproject.toml, riga 13](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/mcp/pyproject.toml#L13); [mcp/README.md, righe 26-28](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/mcp/README.md#L26-L28), 20/11/2026].

**Che cosa esce dalla macchina.** Verso l'endpoint dei modelli, di serie quelli di NVIDIA [verificato: [README, righe 508-514](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L508-L514), 20/11/2026]:
- nomi di tabelle e colonne, e i valori campionati delle colonne non marcate come dati personali, nella generazione (vedi sopra);
- le domande;
- fino a 100 righe di risultato per ogni `run_sql`: per queste l'etichetta PII non vale;
- le colonne incerte per le regole sui dati personali, se si accende il rilevamento automatico.

Se si accende KumoRFM, le tabelle collegate si caricano su quel servizio ospitato [verificato: [README, righe 436-441](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L436-L441), 20/11/2026]. Nel codice non c'è telemetria; la telemetria di Next.js è spenta [verificato: ricerca nel codice del lettore dei fatti, 20/11/2026].

**Maturità.**
- Repo dell'organizzazione NVIDIA, creata su GitHub il 27 aprile 2026, ultimo aggiornamento il 20 novembre; licenza Apache-2.0; circa 14.000 stelle [verificato: api.github.com/repos/NVIDIA/auto-ontology, 20/11/2026].
- **Nessuna release** su GitHub; la versione nei file è la 1.3.0 [verificato: api.github.com/repos/NVIDIA/auto-ontology/releases; [pyproject.toml, riga 7](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/pyproject.toml#L7), 20/11/2026]. Il convertitore Ossie si installa da un commit fissato su git [verificato: [pyproject.toml, riga 39](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/pyproject.toml#L39), 20/11/2026].
- 1.404 commit sul ramo principale, 18 contributori, circa 2.200 funzioni di prova e verifiche automatiche verdi sulle ultime esecuzioni [verificato: metadati GitHub e conteggio nel codice del lettore dei fatti, 20/11/2026]. Fra il 18 e il 19 novembre gli ultimi commit sono 11 [verificato: api.github.com/repos/NVIDIA/auto-ontology/commits, fino al commit letto, 20/11/2026].
- **Issue aperte che toccano i numeri**:
  - con due colonne dallo stesso nome nel risultato, i connettori PostgreSQL, MySQL e SQLite restituiscono dati sbagliati ([issue 408](https://github.com/NVIDIA/auto-ontology/issues/408), etichetta «bug»);
  - con due basi collegate, la chat non esegue più SQL dopo che `retrieve` ha mostrato tabelle di tutte e due ([issue 585](https://github.com/NVIDIA/auto-ontology/issues/585), senza etichetta);
  - con le connessioni di PostgreSQL esaurite, il catalogo resta danneggiato ([issue 553](https://github.com/NVIDIA/auto-ontology/issues/553), etichetta «bug»);
  - i termini segnaposto salvati in silenzio ([issue 533](https://github.com/NVIDIA/auto-ontology/issues/533), etichetta «bug»).

  [verificato: titolo, etichette e stato, 20/11/2026]
- **Altre issue aperte che contano per noi**, segnate come miglioramenti: gli esempi di query della nostra installazione arrivano poco all'agente ([issue 542](https://github.com/NVIDIA/auto-ontology/issues/542)); filtri per riga e per colonna ([issue 427](https://github.com/NVIDIA/auto-ontology/issues/427)); regole sul movimento dei dati, con lo stato «read-only agent queries and PII tagging delivered; movement policy pending» ([issue 264](https://github.com/NVIDIA/auto-ontology/issues/264)) [verificato: titolo, etichette e stato, 20/11/2026].
- **Qdrant**: una pull request aperta, la 424, aggiunge Qdrant come archivio dei vettori a scelta; pgvector resta quello di serie [verificato: [pull request 424](https://github.com/NVIDIA/auto-ontology/pull/424), testo e stato, 20/11/2026].
- L'italiano non è citato né provato in nessuna delle due repo [verificato: ricerca nel codice del lettore dei fatti, 20/11/2026].

**Prove di efficacia.**
- **BEAVER, il «#1» del README.** Nella classifica auto-ontology ha 14,1 nel solo Setting 0, quello senza aiuti, con il modello Claude-Opus-5.5. Al secondo posto ReFoRCE, con lo stesso modello, ha 14,0. La misura è l'accuratezza di esecuzione, cioè la quota di risposte giuste in percento [verificato: [leaderboard.json, righe 3 e 35](https://github.com/beaverbench/beaverbench.github.io/blob/b69bb1bd4d3569559f54211c3dd30a26757dde49/data/leaderboard.json#L35); [settings.json](https://github.com/beaverbench/beaverbench.github.io/blob/b69bb1bd4d3569559f54211c3dd30a26757dde49/data/settings.json); [index.html](https://github.com/beaverbench/beaverbench.github.io/blob/b69bb1bd4d3569559f54211c3dd30a26757dde49/index.html), 20/11/2026].
- **BIRD-Interact, il «#2».** Reward 29,39 su 410 compiti della categoria Query, iscritto il 21 ottobre 2026 e segnato come verificato. Modello e utente simulato sono tutti e due Claude-Opus-4.8, in modalità c-interact. Nella stessa vista è primo AIDBS-DataAgent con 32,98, in modalità a-interact e con GPT-5.6-Luna come utente simulato. Le altre iscrizioni c-interact del file sono del 2025, con GPT-4o o Gemini-2.0-Flash come utente simulato [verificato: [script/task-category-results.js, righe 279-300 e 1172-1192](https://github.com/bird-interact/bird-interact.github.io/blob/7bd13d889fe95154c335deaf5e3b0218d06ad86b/script/task-category-results.js#L1172-L1192), 20/11/2026].
- **I risultati pubblicati usano Claude Opus, non Nemotron.** La repo di valutazione confronta lo stesso modello con e senza strato semantico, e non pubblica numeri riassuntivi [verificato: [README di auto-ontology-eval](https://github.com/NVIDIA/auto-ontology-eval/blob/e727e4d6e1e198355099de4803590bb3681793a4/README.md), 20/11/2026].
- **Qualità dello strato generato** (quanti termini o chiavi sono giusti): nessuna misura pubblicata [non verificato: non trovata].

### 3.2 Il server MCP derivato

- **Chi e quando.** Account gogoymh; repo creata il 6 novembre 2026, ultimo aggiornamento il 18. Ha 19 commit e 3 contributori, con 13, 5 e 1 commit. Licenza Apache-2.0; versione 0.6.1, nessuna release, nessun tag [verificato: api.github.com/repos/gogoymh/auto-ontology-mcp e /contributors, 20/11/2026; [pyproject.toml, riga 3](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/pyproject.toml#L3)].
- **Installazione** da GitHub, dal ramo principale, senza versione fissata; per aggiornarsi si rilancia con `--refresh` [verificato: [README, righe 220-223](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L220-L223), 20/11/2026]. Il nome del pacchetto è lo stesso del server MCP ufficiale di NVIDIA [verificato: [pyproject.toml, riga 2](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/pyproject.toml#L2), 20/11/2026].
- **35 strumenti in quattro gruppi**: `answer` (sempre acceso), `model`, `knowledge`, `share`. Con il solo gruppo `answer` restano lettura, esecuzione SQL e il salvataggio di esempi di query [verificato: [src/auto_ontology_mcp/server.py, righe 128-146](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/server.py#L128-L146), 20/11/2026]. Le etichette «sola lettura» o «distruttivo» degli strumenti sono indicazioni per il client, non vincoli [verificato: [server.py, righe 22-26](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/server.py#L22-L26), 20/11/2026].
- **Collegare una base dati**: `add_datasource` riceve dal modello un indirizzo SQLAlchemy, credenziali comprese. Si spegne con `AUTO_ONTOLOGY_ALLOW_DATASOURCE_TOOLS=0`, e allora le basi si aggiungono solo dalla riga di comando [verificato: [server.py, righe 176-199](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/server.py#L176-L199); [README, riga 632](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L632), 20/11/2026].
- **Password in chiaro**: gli indirizzi delle basi, password comprese, stanno in chiaro nel file `ontology.db` [verificato: [README, riga 632](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L632); [store.py, riga 26](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/store.py#L26), 20/11/2026].
- **Sola lettura su tre livelli**: un controllo sull'SQL, connessioni aperte in sola lettura, rollback di ogni transazione. Le query durano al massimo 30 secondi e restituiscono fino a 500 righe; di serie 100, e il tetto si regola con `AUTO_ONTOLOGY_MAX_ROWS`, anche sopra 500 [verificato: [README, righe 617-627](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L617-L627); [config.py, riga 105](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/config.py#L105); [service.py, riga 1807](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/service.py#L1807), 20/11/2026].
- **Due correzioni di sicurezza aperte.** La 16 tocca solo SQLite: un file aperto con un certo indirizzo restava scrivibile. La 19 limita i valori enormi che una funzione può costruire quasi subito, su tutti i motori, PostgreSQL compreso con `repeat()` [verificato: [pull request 16](https://github.com/gogoymh/auto-ontology-mcp/pull/16), file toccati; [pull request 19](https://github.com/gogoymh/auto-ontology-mcp/pull/19), testo; stato aperto, 20/11/2026].
- **Scrive file.** Il README dice che il server scrive in un posto solo, ma il codice scrive anche nel catalogo e nel vault Obsidian. Copia nel vault ogni file locale non nascosto con un'estensione da documento, immagine, foglio, audio o video (.pdf, .docx, .xlsx, .csv, .json e altre), fino a 100 MB, se il modello ne dà il percorso assoluto [verificato: [README, riga 617](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L617); [vault.py, righe 27-34 e 136-163](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/vault.py#L136-L163), 20/11/2026].
- **Trasporto HTTP**: il token si può passare anche nell'indirizzo, come parametro o come prima parte del percorso; `/health` e `/.well-known/` restano aperti [verificato: [http_auth.py, righe 1-11 e 20-52](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/http_auth.py#L20-L52), 20/11/2026]. Di serie il trasporto è stdio.
- **Ricerca solo per parole**: niente embedding. Per termini e colonne conta parole in comune, somiglianza di trigrammi e frasi; per i testi usa l'indice FTS5 di SQLite. Le istruzioni chiedono al modello di tradurre le domande nelle parole dello schema [verificato: [README, riga 611](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L611), 20/11/2026].
- **Costo sul client**: le definizioni degli strumenti pesano circa 52.000 caratteri a ogni richiesta con tutti i gruppi, circa 12.000 con il solo `answer` [verificato: [README, riga 581](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L581), 20/11/2026].
- **Dove vanno i dati**: tutto ciò che gli strumenti restituiscono entra nel contesto del modello del client, sotto i termini del suo fornitore [verificato: [README, riga 732](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L732), 20/11/2026].
- **Basi provate**: SQLite e PostgreSQL 17, Oracle se configurato; MySQL e DuckDB no [verificato: [README, riga 380](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md#L380), 20/11/2026].
- **Prove di efficacia**: l'unica misura sta nel testo di una pull request chiusa senza unione. In un giro di 440 domande su BIRD, registrato prima di cominciare, con Claude Sonnet 5.5 il guadagno è di 1,8 punti, con un intervallo da −0,7 a +4,3: la tabella lo giudica «inconclusive» [verificato: [pull request 11](https://github.com/gogoymh/auto-ontology-mcp/pull/11), tabella «440 questions», stato chiuso e non unito, 20/11/2026].

### 3.3 Apache Ossie

- È un progetto in incubazione della Apache Software Foundation, con licenza Apache-2.0: una specifica in JSON e YAML per scambiare strati semantici fra strumenti di analisi, AI e BI [verificato: [README di apache/ossie](https://github.com/apache/ossie/blob/6deb2fbadd569d2352433d961eb22fa26667d24c/README.md), 20/11/2026].
- La specifica descrive dataset, relazioni, campi con le dimensioni, e misure di un dataset o di tutto il modello [verificato: [core-spec/spec.md](https://github.com/apache/ossie/blob/6deb2fbadd569d2352433d961eb22fa26667d24c/core-spec/spec.md), 20/11/2026].
- **È una bozza**: «DRAFT version — in development, schema may change before 0.3.0 is released»; la versione scritta nei documenti è `0.3.0.dev0` [verificato: [core-spec/spec.md, righe 22 e 99](https://github.com/apache/ossie/blob/6deb2fbadd569d2352433d961eb22fa26667d24c/core-spec/spec.md#L22), 20/11/2026].
- Il convertitore per auto-ontology sta nella repo `apache/ossie-converters`, creata il 29 settembre 2026 [verificato: api.github.com/repos/apache/ossie-converters, 20/11/2026].

---

## 4. Che cosa farebbero nel progetto, per quali agenti e funzioni

Le funzioni che hanno bisogno di numeri presi dai dati, dall'elenco di [ricerca/00](00-visione-funzionalita.md) e dalla copertura di [PRESENTAZIONE-CEO.md, appendice A](../PRESENTAZIONE-CEO.md). La destinazione è quella proposta in [ricerca/49 §2.6](49-instradamento-a-piu-motori.md): 1 regola, 2 catena N in casa, 3 catena N via API, 4 sessione S, 5 corsia T.

| Funzione | Agente | Fase | Da dove vengono i numeri | Domande | Destinazione |
|---|---|---|---|---|---|
| C1 debrief del mattino | Report del mattino (corsia N) | 1, nel pilota | PostgreSQL 16 (meeting, decisioni, obiettivi) e Jira per i to-do | fisse | 3, oppure 2 per le parti rosse |
| C5 registro dei meeting e pipeline emersa | catena e pannello Grafana | 1-2 | PostgreSQL 16 | fisse | — |
| E3 banca dei token | Banca dei token (corsia N) | 1, 2 e 4 | database di LiteLLM | fisse | — |
| Numeri del lunedì | Analista metriche (corsia N) | 2 | Postiz in lettura e KPI di SersanOutreach | fisse | 1 per i dati, 3 per il commento |
| F4 ore per processo | Mappatore, analisi mensile | 4 | ore dei processi registrate in PostgreSQL | fisse | — |
| G8 vinti e persi | Analista vinto/perso | 3; oggi 0 chiusure | SersanOutreach | fisse | — |
| D1 pipeline pesata; K8 cruscotto della pipeline | Pipeline, che calcola la probabilità pesata | 5 | SersanOutreach; oggi 0 deal vinti e 91 senza valore | fisse, con definizioni delicate | 5 per costruire il portale; per i numeri non è data |
| G2 fit score; G7 tempo di richiamata e meeting nel debrief | qualificatore di SersanOutreach esteso alle call; debrief | 5 | SersanOutreach; per G7 la fonte non è scritta | fisse | — |
| K14 dati finanziari e obiettivi; L3 margini, cassa, distanza dagli obiettivi | Controllo di gestione (corsia N) | 3-6 e 6 | Sirius esportato in PostgreSQL, fase F4 del board; la finanza è rossa ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)) | fisse, ma il «margine» deve voler dire una cosa sola | 2 |
| L2 fatture, incassi e solleciti; K15 acquisti | Agente fatture; Agente acquisti | 6 | il sistema della decisione 22, Sirius oppure Invoice Ninja; per L2 «numeri da Postgres» ([ricerca/29 §8.4](29-conoscenza-task-e-documenti.md)) | fisse | 2 per leggere le fatture scansionate; per i numeri non è data |
| Domande libere alla memoria | Capo di gabinetto (corsia S) | 3 | K4 riguarda i testi, attraverso l'MCP RAG ([ricerca/29 §8.4](29-conoscenza-task-e-documenti.md)) | aperte | 4, giallo |

Fonti della tabella: [PRESENTAZIONE-CEO.md, §4 e appendice A](../PRESENTAZIONE-CEO.md) per agenti, fasi e fonti dei numeri; [ricerca/49 §2.4 e §2.6](49-instradamento-a-piu-motori.md) per le destinazioni; [DOMANDE-PER-MICHELE.md, n. 29](../DOMANDE-PER-MICHELE.md) per il sistema di fatturazione. «—» vuol dire che ricerca/49 non dà una destinazione per quel lavoro. Tutte le assegnazioni di ricerca/49 sono proposte.

**Cosa ne ricavo** [non verificato: lettura nostra].
- I numeri vengono da tre o quattro basi dati: il PostgreSQL del sistema, SersanOutreach, Sirius quando arriva, e lo strumento di fatturazione se non è Sirius. Il database di LiteLLM si aggiunge, ma non si sovrappone agli altri. Di Sirius non sappiamo ancora che cosa sia ([DOMANDE-PER-MICHELE.md, n. 25](../DOMANDE-PER-MICHELE.md)).
- **I numeri del CRM hanno già uno strumento**: il server MCP di lettura di SersanOutreach, con la definizione delle pagine (§1.3).
- Quasi tutte le domande sono fisse: report, rendiconti, pannelli. Le scrive chi scrive la catena, e oggi nessuna è ancora scritta.
- **I numeri rossi, nelle assegnazioni proposte, si calcolano in casa**: il Controllo di gestione va alla destinazione 2, la parte rossa del Report del mattino anche. All'API e a una sessione S il rosso arriverebbe solo oscurato ([ricerca/49 §2.2, regola 4, e §2.6](49-instradamento-a-piu-motori.md)).
- Che arrivino domande aperte sui numeri è una nostra lettura. I documenti danno al Capo di gabinetto le domande libere alla memoria, cioè i testi.
- Il README di auto-ontology dice che con una sola fonte ben modellata e domande fisse può bastare l'SQL diretto. Noi abbiamo tre o quattro basi, ma quasi solo domande fisse (§1.1).

---

## 5. Che cosa chiedono al disegno

| | A. auto-ontology con i modelli di NVIDIA | B. auto-ontology dietro LiteLLM | C. Server MCP derivato | D. Strato semantico scritto a mano |
|---|---|---|---|---|
| **Dove gira** | una macchina nuova nella VLAN APPS, più un PostgreSQL 17 con pgvector in DATA | come A | un processo nella macchina degli agenti, con file SQLite | nel motore: un catalogo in git, l'esecutore e gli strumenti S (§7) |
| **Servizi nuovi** | interfaccia Next.js, due servizi FastAPI, PostgreSQL 17 con pgvector | come A, più un modello di embedding a 2048 dimensioni da servire | nessuno; un pacchetto preso da GitHub | nessuno |
| **Modelli** | Nemotron ospitati da NVIDIA | Claude via LiteLLM, con un nome che comincia per `openai/`; embedding e reranker in casa o da un fornitore | nessuno nel server; ragiona il modello della sessione S | nessuno per calcolare; l'agente usa il suo modello solo per scegliere la misura |
| **GPU** | nessuna | vedi sotto | nessuna | nessuna |
| **Dati che escono, e verso chi** | nomi, campioni delle colonne non marcate PII, domande, fino a 100 righe per query: a NVIDIA, fuori dal board | gli stessi, ad Anthropic, fornitore del board; e a chi serve l'embedding, se non è in casa | campioni e fino a 500 righe: nel contesto di Claude, ad Anthropic | solo il risultato di una misura, con il colore che la misura dichiara |
| **Colore massimo** | solo tabelle non rosse; verde, e giallo con il sì di Michele | solo tabelle non rosse: le righe dei risultati vanno al modello senza oscuramento ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)) | come B | quello della misura; le misure rosse in chiaro solo alle destinazioni in casa, mai in chiaro nella corsia S ([ricerca/49 §2.2, regola 4](49-instradamento-a-piu-motori.md)) |
| **Credenziali** | delle basi dati, nel servizio o in Vault | come A | in chiaro in `ontology.db`; mai al modello se si spegne `add_datasource` | il ruolo della famiglia di agenti sul PostgreSQL del sistema, tenuto dal motore ([ricerca/29 §6.1](29-conoscenza-task-e-documenti.md)) |
| **Rete e porte** | le porte 3001 e 3002 vanno chiuse in rete: fidano di un'intestazione e non hanno autenticazione | come A; in più ogni campo dei modelli va scritto, perché con una chiave che non comincia per `nvapi-` i campi vuoti ripiegano sul gateway `inference-api.nvidia.com` | stdio dentro la macchina degli agenti, che non esce su internet: leggere SersanOutreach da Supabase chiederebbe un'uscita nuova | nessuna porta nuova: i numeri del CRM passano dal server MCP di SersanOutreach, come previsto dalla fase 2 |
| **Regole del ponte** ([ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)) | non le conosce: legge ogni tabella che gli si collega. Ha zone e permessi per persona, non per cliente del compito; i filtri per riga e colonna sono una issue aperta (427) | come A | non le conosce: nessun colore per risultato, nessun filtro per cliente | lo strumento dichiara il colore e filtra per cliente (§7) |
| **Registro** | il suo, dentro l'applicazione | il suo, più il conto di LiteLLM | nessuno nostro | ogni esecuzione registrata dal motore |
| **Board** | eccezione per il fornitore, più un servizio nuovo | un servizio nuovo, con il sì di Michele | un pacchetto nuovo, con il sì di Michele | nessun cambio |

Fonti della tabella: §3. Per la rete, [docs/04-tech-stack.md](../docs/04-tech-stack.md): la macchina degli agenti parla solo con LiteLLM, con i server MCP e con il Cancello; il database di SersanOutreach sta su Supabase, in Irlanda; nella rete del board, dalla VLAN AI verso DATA passa solo Qdrant. Le proposte della colonna D sono [proposta].

**La GPU per B.**
- Il modello di ragionamento di serie in casa non entra. I suoi pesi fanno circa 15 GB a 4 bit [calcolo].
- La RTX 4000 da 8 GB ha meno di 1 GB libero ([ADR-0014](../docs/adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §6.2](48-modelli-locali-e-gpu.md)).
- La scheda da 16 GB proposta è già piena per 13,6-14,3 GB ([ricerca/48 §5](48-modelli-locali-e-gpu.md)).
- Anche i modelli locali più adatti agli strumenti in catena chiedono 18-22 GB ([ricerca/48 §2h](48-modelli-locali-e-gpu.md)).
- Dal nome, è un modello a esperti con circa 3 miliardi di parametri attivi [non verificato: dal suffisso a3b]. Se tenere gli esperti nella RAM basti per la prova degli strumenti in catena non è verificato [non verificato: non provato].
- **L'embedding**: il nostro embedding dei testi, Qwen3-Embedding-0.6B, dà vettori fino a 1024 dimensioni ([ricerca/13 §7](13-modelli-open-source-sul-server.md)). Non arriva a 2048, e la pull request 411 non lo fa entrare. Per B serve quindi un secondo modello a 2048.
- Un embedding a 2048 dimensioni c'è: Qwen3-VL-Embedding-2B ([ricerca/48 §2b](48-modelli-locali-e-gpu.md)). In FP16 pesa circa 4 GB [calcolo] e oggi non ha posto. Altrimenti lo serve un fornitore, e allora nomi di tabelle, termini e domande vanno anche a lui.

**Altri tre punti.**
- **Un secondo archivio di vettori.** A e B portano pgvector accanto a Qdrant, contro la scelta di [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md) e la regola «una cosa, un posto» ([ricerca/46 §1, R-14](46-obsidian-come-casa-dei-testi.md)). Se la pull request 424 venisse unita, toglierebbe il secondo archivio di vettori, non PostgreSQL.
- **Testo che viene dai dati.** Nella generazione di A e B i campioni delle colonne non marcate PII entrano nei prompt, comprese le colonne di testo libero del CRM. Un'istruzione nascosta in un campo potrebbe finire nelle descrizioni scritte dal modello, che poi l'agente legge [non verificato: deduzione; non ho trovato difese dedicate].
- **SersanOutreach per A, B e C.** Leggere il suo database direttamente da Supabase crea una seconda definizione accanto a quella del suo server MCP. Per C, che gira nella macchina degli agenti, chiede in più un'uscita nuova verso internet; A e B girano in una macchina della VLAN APPS, dove sta anche l'applicazione di SersanOutreach con il suo database su Supabase ([docs/04-tech-stack.md](../docs/04-tech-stack.md)) [non verificato: deduzione dalla rete scritta in docs/04].

---

## 6. Le alternative a confronto

### 6.1 Il caso più forte a favore di auto-ontology adesso

Lo scrivo prima dei voti, come chiede il metodo, nella forma più forte che i fatti permettono.

1. **Il problema è il nostro.** ADR-0005 vuole numeri giusti, e il Cancello ha già un controllo per le cifre inventate. auto-ontology nasce proprio contro «a revenue metric answered faster is worth nothing if the number is wrong» (§1.1).
2. **Chi lo fa e come.** È dell'organizzazione NVIDIA, Apache-2.0, sviluppato ogni giorno, con circa 2.200 prove automatiche e verifiche verdi. Non ha telemetria (§3.1).
3. **È pronto e prudente.** Genera da solo il catalogo, con descrizioni, join e misure. Le persone lo correggono e lo certificano da un'interfaccia, che servirebbe anche a chi non scrive SQL. Controlla i nomi prima di eseguire ed esegue in sola lettura. Tiene fuori dai campioni le colonne marcate PII. Via MCP controlla la copertura con `check_answerable`, e il client chiede chiarimenti. Rifiuta se nessuna query passa e restituisce l'SQL con ogni risposta, che è ciò che il registro vuole (§3.1).
4. **Non lega a un fornitore.** Accetta endpoint compatibili con OpenAI, quindi Claude via LiteLLM. I risultati in classifica sono stati ottenuti proprio con Claude Opus. Esporta in un formato aperto (§3.1, §3.3).
5. **Parla con le nostre basi.** PostgreSQL è il primo dei suoi dieci connettori; anche Supabase è PostgreSQL. Con i modelli remoti gira senza GPU (§3.1).
6. **Prima si comincia, prima si impara.** Provandolo oggi sui dati di SersanOutreach, il catalogo sarebbe pronto quando arriva Sirius.
7. **Costa poco.** Licenza zero; si pagano i token dei modelli e un po' di server.
8. **Governa i significati fra molti agenti.** Fra i casi in cui conta, il README mette i significati da riusare e governare fra squadre e agenti ([riga 27](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md#L27)). Il sistema ha 57 agenti in più squadre ([ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)).
9. **Il server MCP ufficiale è in sola lettura**, e ogni chiamata gira con i permessi della persona (§3.1).

### 6.2 Perché oggi non regge

La risposta segue i punti del §6.1, uno per uno.

1. **Il problema.** È nostro, ma per i numeri del CRM lo risolve il server MCP di SersanOutreach, collegato al motore dalla fase 2, con i numeri delle sue pagine. Per gli altri c'è la regola di ADR-0005. auto-ontology lo risolve facendo scrivere l'SQL al modello a ogni domanda di calcolo, e la certificazione non cambia il recupero (§3.1). È il contrario di ADR-0005 e della corsia N, dove il codice calcola e il modello scrive attorno al numero.
2. **Chi lo fa.** Regge, ma non c'è una release. E ci sono issue aperte che toccano i numeri giusti, una proprio sui connettori PostgreSQL: colonne dallo stesso nome (408), due basi collegate (585), catalogo danneggiato (553), termini segnaposto (533) (§3.1).
3. **La prudenza.** I controlli fermano un nome sbagliato, non un numero sbagliato ma eseguibile. Le righe dei risultati vanno al modello senza oscuramento (§3.1, §5).
4. **Il fornitore e le prove.** Regge che accetti Claude via LiteLLM ed esporti in un formato aperto, anche se il formato è una bozza (§3.3). Ma le prove ottenute con Claude Opus sono deboli. Il «#1» su BEAVER è il 14,1% di risposte giuste nel solo Setting 0, 0,1 punti sopra il secondo, con lo stesso modello. Il «#2» su BIRD-Interact vale nella sola categoria Query, con Claude-Opus-4.8 come utente simulato, mentre le altre iscrizioni c-interact usano GPT-4o o Gemini-2.0-Flash (§3.1). Che il confronto non sia alla pari è una nostra lettura [non verificato: lettura nostra]. Con il server derivato, su 440 domande, il guadagno non è concludente; la repo di valutazione di NVIDIA non pubblica numeri riassuntivi (§3.2). Con domande difficili un agente che scrive SQL sbaglia spesso [non verificato: deduzione dalle classifiche].
5. **Le nostre basi.** PostgreSQL sì. Ma SersanOutreach si legge dal suo server MCP, non da Supabase. Le tabelle rosse non si possono collegare, perché le righe arriverebbero al modello senza oscuramento. In più servono un secondo archivio di vettori e un embedding a 2048 dimensioni che oggi non abbiamo (§5).
6. **Imparare presto.** Per generare lo strato bastano schema e campioni. Il limite non sono i volumi: mancano le domande vere da provare. Le funzioni dove uno strato semantico pesa di più arrivano dalle fasi 3-6: il Controllo di gestione aspetta l'esportazione di Sirius, la pipeline pesata le prime chiusure (§4).
7. **I costi.** La licenza è zero. Il costo vero è il servizio da tenere: quattro servizi, patch, porte da chiudere. E i token: fino a 24 turni del modello di ragionamento per domanda (§3.1).
8. **Il governo dei significati.** È il motivo giusto, ed è quello di D. Per i numeri che servono davvero, però, la stessa cosa la dà una definizione unica con un nome, senza un servizio nuovo. I numeri del CRM l'hanno già (§7).
9. **Il server MCP ufficiale.** Regge come prodotto. Ma nella corsia S la sessione usa solo gli strumenti del ponte, che mette persona e cliente dalla sessione e fa leggere solo i dati del cliente del compito. Il server di NVIDIA filtra per persona, non per cliente ([ADR-0001](../docs/adr/0001-motore-agent-sdk.md); [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)).

Infine il suo stesso README: con una sola fonte ben modellata e domande fisse può bastare l'SQL diretto. Noi abbiamo poche fonti e quasi solo domande fisse (§1.1, §4). **Il caso non regge oggi; reggerebbe alle condizioni del §8.**

### 6.3 I voti

Il ruolo confrontato: **dare agli agenti, e attraverso loro alle persone, numeri giusti presi dalle nostre basi dati.** Voti da 0 a 10; totale su 100.

| Alternativa | Autonomia (35) | Tempo al valore (20) | Costi (15) | Sicurezza essenziale (10) | Server e manutenzione (10) | Rischio (10) | Totale |
|---|---|---|---|---|---|---|---|
| **A. auto-ontology così com'è, con i modelli di NVIDIA**, solo tabelle non rosse | 7: risponde da solo anche a domande aperte; via MCP controlla la copertura e il client chiede chiarimenti; rifiuta se nessuna query passa. Ma per ogni domanda di calcolo il modello scrive l'SQL, e la certificazione non lega il recupero | 4: avvio rapido documentato; servono un servizio nuovo e il sì di Michele al fornitore, e le funzioni dove pesa arrivano dalla fase 3 | 6: licenza zero; i modelli ospitati si pagano a consumo, prezzo non trovato | 2: nomi, campioni, domande e righe a un fornitore fuori dal board; porte interne senza autenticazione | 4: quattro servizi e un PostgreSQL 17 con pgvector accanto a Qdrant | 2: un errore di configurazione su una tabella rossa la manda fuori dal board; nessuna release; bug aperti sui numeri | **49,5** |
| **B. auto-ontology dietro LiteLLM**, solo tabelle non rosse | 7: come A | 2: come A, più l'embedding a 2048 dimensioni che oggi non ha posto, i nomi `openai/` in LiteLLM, ogni campo dei modelli da scrivere e le prove | 6: licenza zero; Claude fino a 24 turni per domanda, almeno 3 chiamate per tabella nella generazione | 4: fornitore del board, giallo ammesso; le righe dei risultati senza oscuramento; nessun filtro per cliente | 2: lo stack di A più un modello di embedding da servire | 4: nessuna release; bug aperti sui numeri su PostgreSQL; numeri sbagliati ma eseguibili | **47,5** |
| **C. Server MCP derivato**, solo `answer`, sessione S come client, solo tabelle non rosse | 6: la sessione modella, risponde e può chiedere chiarimenti; ma il modello scrive l'SQL, e la ricerca è solo per parole: le domande in italiano vanno tradotte nelle parole dello schema | 4: un processo e file SQLite; ma servono il sì di Michele e il pacchetto fissato a un commit, il catalogo lo costruisce qualcuno con gli strumenti di scrittura, e il suo cliente, le domande aperte, arriva nella fase 3 | 8: niente licenza né modello suo; circa 12.000 caratteri di definizioni a ogni richiesta | 2: campioni e righe nel contesto di Claude senza colore né filtro per cliente; password in chiaro; strumenti distruttivi da spegnere a mano | 6: nessun servizio nuovo; codice di terzi da tenere | 2: due settimane di vita, un autore principale, nessuna release, nome in conflitto con NVIDIA, due correzioni di sicurezza aperte | **51,0** |
| **D. Strato semantico scritto a mano**: catalogo, esecutore, strumenti S, regola del router, controllo del contenuto (§7) | 8: ogni numero lo calcola il codice, con una definizione sola; la sessione S chiede per nome anche i numeri che nessuno strumento dà; fuori dal catalogo la domanda va a una persona | 4: come il codice del motore in ricerca/52, dove «ogni integrazione va scritta e provata»: esecutore, strumenti, regole, prove e ogni misura | 8: niente licenza né chiamate in più ai modelli; costa lo sviluppo | 8: niente esce per calcolare; colore e cliente nello strumento; ruolo in sola lettura | 8: nessun servizio nuovo; SQL da tenere allineato agli schemi, controllato dalle prove | 8: codice nostro; i rischi propri sono la copertura, il colore e il cliente delle misure aggregate, e un controllo del contenuto da non allentare (§7) | **72,0** |
| **E. Non fare niente adesso**: resta ciò che i documenti hanno già | 7: i numeri li calcola il codice delle catene. Dalla fase 2 la sessione S legge i KPI del CRM dal server MCP di SersanOutreach e, quando c'è, la memoria su PostgreSQL; gli strumenti nuovi arrivano con l'agente che li chiede. Manca una definizione unica per i numeri che nessuno strumento dà | 8: nulla da fare oggi | 10: zero | 8: come D | 8: nulla di nuovo; l'SQL di ogni catena da tenere | 7: la stessa misura scritta in due catene, o in una catena e in un pannello, può divergere | **78,5** |

Fonti dei voti: §3 per A, B e C; §1.3, §4, [ricerca/52 §3.4](52-n8n-moda-elevenlabs.md), [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md), [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md) e [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md) per D ed E.

**Calcolo** [calcolo]: A = (7×35 + 4×20 + 6×15 + 2×10 + 4×10 + 2×10) / 10 = 49,5; B = (7×35 + 2×20 + 6×15 + 4×10 + 2×10 + 4×10) / 10 = 47,5; C = (6×35 + 4×20 + 8×15 + 2×10 + 6×10 + 2×10) / 10 = 51,0; D = (8×35 + 4×20 + 8×15 + 8×10 + 8×10 + 8×10) / 10 = 72,0; E = (7×35 + 8×20 + 10×15 + 8×10 + 8×10 + 7×10) / 10 = 78,5.

**Sensibilità sulla coppia D-E** [calcolo]. E sta 6,5 punti sopra D, fuori dal margine.

| Ritocco | D | E | Scarto |
|---|---|---|---|
| voti della tabella | 72,0 | 78,5 | E +6,5 |
| tempo di D a 6 | 76,0 | 78,5 | E +2,5, dentro il margine |
| autonomia di E a 6 | 72,0 | 75,0 | E +3,0, dentro il margine |
| rischio di E a 6 | 72,0 | 77,5 | E +5,5 |
| rischio di E a 8 | 72,0 | 79,5 | E +7,5 |
| tempo di D a 6 e autonomia di E a 6 | 76,0 | 75,0 | D +1,0, dentro il margine |

E resta davanti con ogni ritocco singolo. D torna davanti solo con due ritocchi insieme, cioè con due dei voti della prima stesura, che la verifica ha mostrato non reggere sui fatti. Il tempo di D a 6 contraddice ricerca/52. L'autonomia di E a 6 ignora il server MCP di SersanOutreach.

**Le altre alternative.** Con autonomia 8 per B e C, che rispondono anche fuori da un catalogo, B sale a 51,0 e C a 58,0 [calcolo]: restano sotto D ed E di oltre 10 punti.

**Cosa ne ricavo** [non verificato: lettura nostra].
- A, B e C rispettano i limiti fissi solo lontano dalle tabelle rosse, cioè proprio dalla finanza, che è il caso dove uno strato semantico peserebbe di più (§4). A in più chiede il sì di Michele al fornitore.
- C sta sopra A e B perché è leggero, non perché sia più sicuro: ha gli stessi problemi di dati, e in più la maturità di un lavoro di due settimane.
- E vince fuori dal margine. Il catalogo completo di D oggi non si ripaga, per tre motivi. I numeri del CRM hanno già uno strumento con una definizione sola. I lavori con numeri rossi, nelle assegnazioni proposte, vanno a una catena N in casa; all'API e alla corsia S il rosso andrebbe solo oscurato. Le domande libere arrivano nella fase 3, e i documenti le danno ai testi.
- Di D resta una cosa sola, che non costa lavoro in più: la definizione unica, con un nome, per i numeri nuovi (§7).

---

## 7. Giudizio

**A. auto-ontology con i modelli di NVIDIA: non ora.** Si potrebbe usare solo sulle tabelle non rosse, con il verde, e il giallo solo con il sì di Michele al fornitore. Si riguarda alle condizioni del §8.

**B. auto-ontology dietro LiteLLM: non ora.** Solo tabelle non rosse. Si riguarda alle condizioni del §8.

**C. Server MCP derivato: non ora.** Si riguarda alle condizioni del §8. Nessuno lo installi intanto sui computer di lavoro con dati veri: le password resterebbero in chiaro e i risultati andrebbero al fornitore del client [proposta].

**E. Non fare niente adesso: sì, con una regola di scrittura** [proposta]:
1. **Non si costruisce niente adesso.** Niente catalogo, niente strumenti nuovi, niente cambi al Cancello.
2. **Uno strumento esistente vince.** Quando una catena ha bisogno di un numero che uno strumento esistente dà già, usa quello. Per il CRM è il server MCP di lettura di SersanOutreach, con la definizione delle sue pagine; per gli obiettivi, i meeting e le decisioni sarà il server MCP della memoria, quando c'è. Nessuna seconda definizione.
3. **Un numero nuovo si definisce una volta sola.** Quando una catena calcola un numero che nessuno strumento dà, lo si definisce una volta sola, con un nome, per esempio una vista nel database. Le altre catene e i pannelli di Grafana riusano quella.
4. **Gli agenti non scrivono SQL.** Lo scrive chi scrive la catena, come oggi.
5. **I numeri rossi** seguono la regola dei colori del router: in chiaro solo a una regola, a una catena N in casa o a una persona; all'API e alla corsia S solo oscurati ([ricerca/49 §2.2, regola 4](49-instradamento-a-piu-motori.md); [ADR-0009](../docs/adr/0009-dati-tre-colori.md); [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)).

**D. Strato semantico scritto a mano: non ora.** Se un giorno torna utile (§8), queste sono le sue parti e i suoi rischi, perché chi lo costruisce non debba ripartire da zero [proposta]:
- **Il catalogo**: un file in git con i termini (le parole del lavoro, con la definizione in italiano e i sinonimi) e le misure (nome, descrizione, SQL su viste, parametri, unità, colore del risultato, colonna del cliente, responsabile, data di certificazione, una prova con il valore atteso).
- **SersanOutreach non si riscrive in SQL.** Per i numeri del CRM il catalogo rimanda agli strumenti del suo server MCP di lettura, che il ponte incapsula ([ADR-0001](../docs/adr/0001-motore-agent-sdk.md)). L'SQL nostro resta per ciò che non ha uno strumento: il PostgreSQL del sistema, LiteLLM, Sirius quando arriva, lo strumento di fatturazione.
- **L'esecuzione**: il motore esegue con il ruolo della famiglia di agenti ([ricerca/29 §6.1](29-conoscenza-task-e-documenti.md)). Le letture restano libere, come prevede il disegno, e non passano dal Cancello ([docs/04-tech-stack.md](../docs/04-tech-stack.md), riga «Server MCP»). Ogni esecuzione la registra il motore.
- **La corsia S**: lo strumento dichiara il colore della misura, così il ponte lo conta fra quelli letti dalla sessione, come chiede ADR-0029. Nelle sessioni legate a un cliente si usano solo misure filtrate per quel cliente. Le misure aggregate su più clienti valgono solo nei compiti senza cliente.
- **Le misure rosse** si servono in chiaro solo alle destinazioni in casa (regola o catena N in casa), mai in chiaro nella corsia S: lì arrivano solo oscurate ([ricerca/49 §2.2, regola 4](49-instradamento-a-piu-motori.md)).
- **Il router**: una richiesta strutturata, cioè una misura con i suoi parametri, può andare a una regola. Una domanda in parole libere passa prima dal decisore ([ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)).
- **Il controllo del contenuto**: può accettare una cifra che porta l'identificativo di una misura solo per misure verdi o gialle, verso destinatari che il colore ammette. Ripetere il valore controlla il numero, non che la frase descriva quella misura: la domanda di significato resta al decisore ([ADR-0027](../docs/adr/0027-decisore.md)). Questo è un cambio di [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md) e di ADR-0027.
- **Le tappe**: catalogo, esecuzione e prove servono dalla prima misura; strumenti S e regola del router dalla fase 3; il cambio del controllo del contenuto solo se le uscite L2 e L3 lo chiedono. Il lavoro non è stimato.
- **Il formato**: nostro, vicino nella forma ad Apache Ossie (dataset, campi, misure, relazioni), senza dipendere dalla specifica finché è una bozza.

---

## 8. Migliora l'architettura? Quando riguardarla

**Il prodotto non migliora l'architettura oggi. L'idea sì, ma solo come regola di scrittura.** Per il CRM il progetto ha già uno strumento con misure dal nome; per la memoria lo avrà. ADR-0005 dice che i numeri li calcola il codice, ma non dice che cosa fare quando due catene calcolano lo stesso numero. La regola del §7 lo dice, senza servizi nuovi.

**Il catalogo completo (D) si riguarda** quando succede una di queste cose [proposta; soglie da tarare]:
- la stessa misura serve ad almeno tre catene o pannelli, e le definizioni cominciano a divergere;
- dalla fase 3, le richieste di un numero che nessuno strumento dà finiscono spesso nel libro delle proposte: per esempio più di dieci al mese, per tre mesi di fila.

**auto-ontology si riguarda quando valgono la 1 o la 2, e poi la 3 e la 4. Per le tabelle rosse serve anche la 5** [proposta; soglie da tarare]:
1. **Più fonti**: gli agenti leggono da almeno quattro basi dati SQL con definizioni che si sovrappongono. La soglia è nostra: il README parla di molte fonti in conflitto, senza un numero. Oggi sono il PostgreSQL del sistema, SersanOutreach con il suo server MCP, Sirius quando arriva, e lo strumento di fatturazione se non è Sirius (decisione 22; [DOMANDE-PER-MICHELE.md, n. 29](../DOMANDE-PER-MICHELE.md)). Il database di LiteLLM non si sovrappone agli altri.
2. **Domande fuori dagli strumenti**: le domande sui numeri che né gli strumenti né le definizioni con un nome coprono sono tante e varie. Si contano nel libro delle proposte, come sopra.
3. **Il prodotto è pronto per noi**:
   - una release con un numero di versione;
   - chiusi i bug 408, 533, 553 e 585;
   - unita la pull request 424, con Qdrant;
   - una colonna dei vettori di larghezza configurabile (oggi nessuna pull request: la 411 accorcia soltanto);
   - chiuse le issue 427, filtri per riga e colonna, e 264, regole sul movimento dei dati.
4. **Una nostra prova**, sulle domande vere raccolte con la condizione 2, con la risposta attesa scritta da una persona. Si contano le risposte giuste, i rifiuti giusti e i numeri sbagliati presentati come certi. Si adotta solo se i numeri sbagliati presentati come certi sono zero. Numero di domande e altre soglie si fissano prima della prova.
5. **Per le tabelle rosse**: il rosso va all'API solo oscurato ([ADR-0009](../docs/adr/0009-dati-tre-colori.md); [ricerca/49 §2.2](49-instradamento-a-piu-motori.md)), e auto-ontology mostra le righe al modello senza oscuramento. Serve quindi un modello di ragionamento in casa che passi la prova sugli strumenti in catena di [ADR-0025](../docs/adr/0025-un-modello-per-agente.md) e abbia posto in GPU, oppure l'oscuramento locale sul percorso verso il modello.

**Un uso più piccolo, da riguardare quando Sirius è noto** [proposta]. Se il suo schema ha molte tabelle con nomi poco chiari, per esempio più di cento, auto-ontology può servire una volta sola come generatore di una bozza. Si fa girare su una copia dello schema riempita di dati finti, così nessun valore vero esce. La bozza la rivede una persona e diventa una definizione nostra. I modelli sono quelli dietro LiteLLM, oppure quelli di NVIDIA se Michele li ammette per i dati verdi.

**Il server MCP derivato si riguarda** se esce su PyPI con un nome che non si scontra con quello di NVIDIA, con le correzioni di sicurezza unite e più di una persona attiva per almeno tre mesi. E comunque solo dopo un filtro nostro per colore e cliente davanti ai suoi risultati [proposta].

---

## 9. Dove toccherebbe i documenti

Sono proposte: nessuna ADR è stata modificata. Ogni revisione va datata il giorno in cui la si accetta; qui porta la data del 20 novembre 2026.

### 9.1 ADR-0005, la memoria

La decide il gruppo di progetto con Michele, a cui ADR-0005 affida la scelta.

> ## Revisione del 20 novembre 2026
>
> - La regola «i numeri si calcolano dal codice sui dati» si precisa. Quando una catena ha bisogno di un numero che uno strumento esistente dà già, usa quello: per il CRM il server MCP di lettura di SersanOutreach, per obiettivi, meeting e decisioni il server MCP della memoria, quando c'è.
> - Quando una catena calcola un numero che nessuno strumento dà, lo si definisce una volta sola, con un nome, per esempio una vista nel database. Le altre catene e i pannelli di Grafana riusano quella. Gli agenti non scrivono SQL (ricerca/53 §7).
> - I numeri rossi seguono la regola dei colori del router: in chiaro solo a una regola, a una catena N in casa o a una persona; all'API e alla corsia S solo oscurati (ADR-0009; ADR-0028; ricerca/49 §2.2).
> - NVIDIA auto-ontology, il server MCP derivato e un catalogo delle misure con strumenti propri sono stati valutati e non entrano ora; le condizioni per riguardarli sono in ricerca/53 §8.

### 9.2 Nessun'altra ADR, per ora

Il primo testo proponeva una revisione di ADR-0020 sul controllo del contenuto. Con la scelta di E non serve. Se un giorno si costruisce D, servono revisioni di [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md) e [ADR-0027](../docs/adr/0027-decisore.md) per il controllo del contenuto (§7, D). Il colore dichiarato dallo strumento sta dentro la regola di [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md) così com'è.

### 9.3 Altri documenti

- [docs/04-tech-stack.md §3](../docs/04-tech-stack.md): dopo «I numeri (pipeline, margini, budget) si calcolano dal codice sui dati», una frase con la regola del §9.1. Fra le alternative scartate, auto-ontology e il server MCP derivato, con il rimando a questo rapporto.
- [docs/02-alternative.md](../docs/02-alternative.md): una sottosezione 10.6, «Il 20 novembre: auto-ontology e lo strato semantico», come le altre valutazioni dopo il terzo giro.
- [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md): tre aggiunte alla domanda 25 su Sirius, e una domanda nuova, la 47 del §10.
- [ricerca/12 §6](12-altre-piattaforme.md) non si riscrive: questo rapporto aggiunge che uno strato semantico sulle basi dati è un'altra cosa rispetto ai grafi di conoscenza per la memoria.

---

## 10. Domande aperte per le persone

**Alberto**:
1. La direttiva nasce da un bisogno preciso? Quali domande sui numeri vorreste fare agli agenti, o farvi rispondere in chat? Diventano le domande della prova del §8, e mostrano se le domande aperte sui numeri ci sono davvero.

**Michele**:
2. Aggiunte alla domanda 25 di [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md), che oggi chiede che cos'è Sirius: come esporta, quante tabelle ha e con che nomi? Decide se serve il generatore di bozze del §8.
3. (Proposta di domanda 47) Le catene e i pannelli di Grafana possono leggere le stesse viste del PostgreSQL del sistema, con il ruolo per famiglia di agenti di [ricerca/29 §6.1](29-conoscenza-task-e-documenti.md)? È il seguito della domanda 31, dove i ruoli separati del database restano.

**Gruppo di progetto, con Michele**:
4. Si accetta la regola del §7 e la revisione di ADR-0005 del §9.1? Chi tiene l'elenco dei numeri definiti con un nome?

---

## 11. I buchi

Quello che le fonti non dicono, o che non ho potuto verificare:
- **L'embedding per B**: se il server di embedding del board accetti i tre campi di NVIDIA nella richiesta non l'ho verificato.
- **Il modello di serie in casa**: è un modello a esperti con circa 3 miliardi di parametri attivi (dal nome). Se tenere gli esperti nella RAM basti per la prova degli strumenti in catena non è verificato.
- **LiteLLM e i nomi `openai/`**: che un nome come `openai/claude-…` passi da LiteLLM ad Anthropic come si vuole va provato.
- **Prezzi e licenze dei modelli NVIDIA ospitati**: la repo rimanda ai termini di ciascun fornitore e modello; non li ho trovati.
- **Memoria video** per ospitare in casa i modelli di serie: non documentata; le cifre del §3.1 sono un mio calcolo sui soli pesi.
- **Italiano**: non provato in nessuna delle due repo.
- **Qualità dello strato generato**: nessuna misura pubblicata della precisione di termini e chiavi.
- **Le misure riusate**: il README dice che le misure rivedute fanno calcolare ogni numero allo stesso modo; la documentazione dell'architettura dice che la certificazione non cambia il recupero. Quanto il modello le riusi davvero non si sa.
- **I documenti in auto-ontology**: della pull request 386 ho letto solo titolo e stato. Il titolo parla di un estrattore «fully hosted», cioè di documenti mandati a un servizio esterno.
- **Le nostre basi**: quante tabelle hanno non è scritto; di Sirius non si sa ancora che cosa sia; per il tempo di richiamata (G7) la fonte non è scritta.
- **Le domande aperte sui numeri**: nessun documento dice che arriveranno; la domanda 1 del §10 serve a saperlo.
- **Ossie**: la specifica è una bozza e può cambiare prima della 0.3.0.

---

## Fonti

**NVIDIA auto-ontology, commit `43fa2d3`, letto il 20/11/2026** (link al file sul commit)
- [README.md](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/README.md) · [docs/architecture.md](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/architecture.md) · [docs/mcp.md](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docs/mcp.md) · [mcp/README.md](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/mcp/README.md) · [mcp/pyproject.toml](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/mcp/pyproject.toml)
- [auto_ontology/utils/model_config.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/model_config.py) · [auto_ontology/utils/llm_invoke.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/llm_invoke.py) · [auto_ontology/utils/embedding.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/embedding.py) · [auto_ontology/utils/rerank.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/utils/rerank.py) · [auto_ontology/vdb/postgres.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/vdb/postgres.py)
- [auto_ontology/semantic/visit_enter.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/visit_enter.py) · [auto_ontology/semantic/deterministic.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/deterministic.py) · [auto_ontology/semantic/pii_values.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/semantic/pii_values.py) · [auto_ontology/retrieval/text_to_sql/react/run_sql.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/retrieval/text_to_sql/react/run_sql.py) · [auto_ontology/retrieval/interactive/clarify.py](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/auto_ontology/retrieval/interactive/clarify.py)
- [docker-compose.yml](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/docker-compose.yml) · [pyproject.toml](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/pyproject.toml) · [frontend/package.json](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/frontend/package.json) · [.env.example](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/.env.example) · [.github/workflows/release-docker.yml](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/.github/workflows/release-docker.yml) · [helm/auto-ontology/values.yaml](https://github.com/NVIDIA/auto-ontology/blob/43fa2d3ac3cb00f79cce23b76d57a002b0cb0168/helm/auto-ontology/values.yaml)
- Issue: [264](https://github.com/NVIDIA/auto-ontology/issues/264) · [408](https://github.com/NVIDIA/auto-ontology/issues/408) · [427](https://github.com/NVIDIA/auto-ontology/issues/427) · [440](https://github.com/NVIDIA/auto-ontology/issues/440) · [533](https://github.com/NVIDIA/auto-ontology/issues/533) · [542](https://github.com/NVIDIA/auto-ontology/issues/542) · [553](https://github.com/NVIDIA/auto-ontology/issues/553) · [571](https://github.com/NVIDIA/auto-ontology/issues/571) · [585](https://github.com/NVIDIA/auto-ontology/issues/585)
- Pull request: [386](https://github.com/NVIDIA/auto-ontology/pull/386) · [411](https://github.com/NVIDIA/auto-ontology/pull/411) · [424](https://github.com/NVIDIA/auto-ontology/pull/424)
- Metadati: https://api.github.com/repos/NVIDIA/auto-ontology · https://api.github.com/repos/NVIDIA/auto-ontology/releases · https://api.github.com/repos/NVIDIA/auto-ontology/commits
- Repo di valutazione, commit `e727e4d`: [README.md](https://github.com/NVIDIA/auto-ontology-eval/blob/e727e4d6e1e198355099de4803590bb3681793a4/README.md)

**auto-ontology-mcp, commit `0fb5ecf`, letto il 20/11/2026**
- [README.md](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/README.md) · [NOTICE](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/NOTICE) · [pyproject.toml](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/pyproject.toml)
- [src/auto_ontology_mcp/server.py](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/server.py) · [src/auto_ontology_mcp/config.py](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/config.py) · [src/auto_ontology_mcp/http_auth.py](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/http_auth.py) · [src/auto_ontology_mcp/vault.py](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/vault.py) · [src/auto_ontology_mcp/store.py](https://github.com/gogoymh/auto-ontology-mcp/blob/0fb5ecf765e4cfbe3c86634c5c52a3b2e752923a/src/auto_ontology_mcp/store.py)
- Pull request: [11](https://github.com/gogoymh/auto-ontology-mcp/pull/11) · [16](https://github.com/gogoymh/auto-ontology-mcp/pull/16) · [19](https://github.com/gogoymh/auto-ontology-mcp/pull/19)
- Metadati: https://api.github.com/repos/gogoymh/auto-ontology-mcp · https://api.github.com/repos/gogoymh/auto-ontology-mcp/contributors

**Classifiche, lette il 20/11/2026**
- BEAVER, commit `b69bb1b`: [data/leaderboard.json](https://github.com/beaverbench/beaverbench.github.io/blob/b69bb1bd4d3569559f54211c3dd30a26757dde49/data/leaderboard.json) · [data/settings.json](https://github.com/beaverbench/beaverbench.github.io/blob/b69bb1bd4d3569559f54211c3dd30a26757dde49/data/settings.json) · [index.html](https://github.com/beaverbench/beaverbench.github.io/blob/b69bb1bd4d3569559f54211c3dd30a26757dde49/index.html)
- BIRD-Interact, commit `7bd13d8`: [script/task-category-results.js](https://github.com/bird-interact/bird-interact.github.io/blob/7bd13d889fe95154c335deaf5e3b0218d06ad86b/script/task-category-results.js)

**Apache Ossie, letto il 20/11/2026**
- [README](https://github.com/apache/ossie/blob/6deb2fbadd569d2352433d961eb22fa26667d24c/README.md) · [core-spec/spec.md](https://github.com/apache/ossie/blob/6deb2fbadd569d2352433d961eb22fa26667d24c/core-spec/spec.md) · https://api.github.com/repos/apache/ossie-converters

**Documenti della repo**
- [ricerca/00, le funzioni](00-visione-funzionalita.md) · [ricerca/12, altre piattaforme, §6](12-altre-piattaforme.md) · [ricerca/13, modelli open source sul server, §7](13-modelli-open-source-sul-server.md) · [ricerca/20, proposta G](20-proposta-G-ibrido.md) · [ricerca/29, conoscenza, §6.1, §7.1 e §8.4](29-conoscenza-task-e-documenti.md)
- [ricerca/45, architettura v3, riga 34, §1.2 e §2.5](45-architettura-v3.md) · [ricerca/46, §1](46-obsidian-come-casa-dei-testi.md) · [ricerca/48, §2b, §2h, §5 e §6.2](48-modelli-locali-e-gpu.md) · [ricerca/49, §2.4 e §2.6](49-instradamento-a-piu-motori.md) · [ricerca/52, §2 e §3.4](52-n8n-moda-elevenlabs.md)
- [PRESENTAZIONE-CEO.md, §4, §7.3 e appendice A](../PRESENTAZIONE-CEO.md) · [DOMANDE-PER-MICHELE.md, n. 25, 29 e 31](../DOMANDE-PER-MICHELE.md) · [docs/02-alternative.md](../docs/02-alternative.md) · [docs/03-architettura.md](../docs/03-architettura.md) · [docs/04-tech-stack.md, §3](../docs/04-tech-stack.md) · [docs/06-sviluppo.md](../docs/06-sviluppo.md)
- [README del server MCP di lettura di SersanOutreach](../allegati/sersanoutreach/mcp_server-README.md)
- [ADR-0001](../docs/adr/0001-motore-agent-sdk.md) · [ADR-0002](../docs/adr/0002-self-hosted-board-michele.md) · [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md) · [ADR-0009](../docs/adr/0009-dati-tre-colori.md) · [ADR-0014](../docs/adr/0014-seconda-gpu-blackwell.md) · [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md) · [ADR-0025](../docs/adr/0025-un-modello-per-agente.md) · [ADR-0027](../docs/adr/0027-decisore.md) · [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md) · [ADR-0029](../docs/adr/0029-corsia-s-sessioni-a-giri.md)
