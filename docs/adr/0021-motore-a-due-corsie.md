# ADR-0021: Motore a due corsie: catene a schema e sessioni dell'Agent SDK nello stesso codice

**Data**: 2026-11-10

**Stato**: accettata; nota del 2026-11-12 da [ADR-0029](0029-corsia-s-sessioni-a-giri.md) e [ADR-0030](0030-bacheca-gruppi-specchi.md): le stesse regole valgono per le azioni delle due corsie, non per i passaggi fra agenti; la corsia S chiama l'API direttamente fino alla milestone 3 del PRD

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Dove girano i processi lo decide Michele, a cui resta l'infrastruttura ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).

## Contesto

- Nella v2 ogni agente era una sessione dell'Agent SDK di Claude, cioè Claude Code usato come libreria, con un processo per lavoro e un ponte (`propose_action`) verso il Cancello ([ADR-0001](0001-motore-agent-sdk.md)).
- Nel terzo giro la proposta «automazione prima» (P-D) e la proposta «motore a livelli» (P-A) sono finite a 0,3 punti l'una dall'altra, dentro il margine di giudizio. Tre giudici su quattro hanno chiesto di unirle ([ricerca/45 §1.1 e §1.2](../../ricerca/45-architettura-v3.md)).
- P-D faceva girare il lavoro ripetitivo come catene a schema dentro n8n. Le verifiche avversarie hanno chiesto di portare quella logica nel nostro codice: la licenza di n8n vieta la rivendita, il suo versionamento in git è una funzione Enterprise, un'esecuzione caduta per un crash non riprende da sola e i dati rossi finirebbero nella cronologia delle esecuzioni ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md); [ricerca/44](../../ricerca/44-verifiche-avversarie.md)).
- Il giudice di sicurezza del secondo giro chiama le catene dove il codice sceglie i passi e i destinatari «il disegno più robusto» contro le iniezioni di prompt, cioè le istruzioni nascoste nel testo di terzi ([ricerca/35, giudizio di sicurezza §3.2](../../ricerca/35-giudizio-sicurezza.md)).
- I tre agenti del pilota (Post-call, Analista chiamate, Report del mattino) riassumono, estraggono e scrivono: per loro basta una catena a schema ([ricerca/45 §1.2](../../ricerca/45-architettura-v3.md)).

## Decisione

**Un solo motore in TypeScript, con due corsie** ([ricerca/45 §1.2 e §3](../../ricerca/45-architettura-v3.md); [ADR-0010](0010-typescript-motore.md)):

- **Corsia N, catene deterministiche a schema.** Il codice sceglie i passi e i destinatari, presi dai dati; il modello scrive senza strumenti e restituisce campi a schema. Ogni passo ha una chiave d'idempotenza, così un passo ripetuto non produce un secondo effetto. Chiama l'API Messages, senza passare da Claude Code. Raccoglie il lavoro ripetitivo: riassumere, classificare, estrarre, scrivere da un modello fisso; sono circa 30-35 figure [stima] ([ricerca/45 §3.1 e §3.2](../../ricerca/45-architettura-v3.md)).
- **Corsia S, sessioni dell'Agent SDK con strumenti**, per le figure che decidono il passo dopo, leggono il web o usano più strumenti: brief, proposte, slide, Capo di gabinetto, Mappatore, Project manager e altre, circa 15-20 figure [stima]. Un solo runner con al massimo 6 sessioni insieme; escono il possesso, il battito e le riserve fra più runner ([ricerca/45 §3.1 e §3.2](../../ricerca/45-architettura-v3.md)).
- **La corsia S si costruisce subito dopo la milestone 1**, non alla settimana 9. Prima vengono il Cancello a livelli e le catene, perché servono a tutte e due le corsie ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Insieme alla corsia S arriva la bacheca degli agenti ([ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md)).
- **La milestone 1 usa solo la corsia N**: Cancello a livelli, catena «post-call» su una trascrizione verde di prova, registro degli eventi, Porta di prova ed esecutori di prova, sulle macchine di sviluppo con Windows e Node 22 ([ricerca/45 §6.1 e §12.1](../../ricerca/45-architettura-v3.md)).
- **Le due corsie hanno le stesse regole.** Ogni catena N e ogni sessione S carica le regole «Come lavoro» della persona per cui lavora, e ogni azione passa dal Cancello al livello della sua terna ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md); [ADR-0020](0020-autonomia-a-livelli.md)).
- **Passare da N a S è una promozione dentro lo stesso codice**, non una riscrittura. Le 57 figure restano tutte agenti, con nome, responsabile, tetto e riga nel registro ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md)).
- **Il codice sta nella repo privata `sersan-agent-os-codice`** (D4), insieme a PRD, spec e piani di sviluppo. Nella repo pubblica restano la proposta, la ricerca, i documenti di progetto e le ADR ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)).
- **Il modello lo dichiara ogni agente** nel registro ([ADR-0025](0025-un-modello-per-agente.md)). Nella corsia S resta Claude finché una prova non dimostra che un modello locale regge.

## Alternative considerate

### Alternativa: la logica nei flussi n8n, come in P-D

- **Pro**: era prima in classifica, con 76,6 punti; n8n ha già la finestra nativa con il nodo Wait e approvazioni in Teams ([ricerca/45 §1.1](../../ricerca/45-architettura-v3.md); [ricerca/41 §5](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: licenza che vieta la rivendita, git solo nella versione Enterprise, nessuna ripresa dopo un crash, dati rossi nella cronologia delle esecuzioni ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md)).
- **Perché no**: le catene a schema le prendiamo da P-D, ma le scriviamo nel nostro codice ([ricerca/45 §1.3](../../ricerca/45-architettura-v3.md)).

### Alternativa: tutto in sessioni dell'Agent SDK, come in P-A e nella v2

- **Pro**: un solo modo di far girare gli agenti, con la modalità auto e gli hook dell'SDK ([ricerca/41 §8.2](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: un processo di Claude Code per ogni lavoro pesa sulla RAM; il ponte verso il Cancello è il pezzo più rischioso della fase 1; la fase 1 non sta nella capacità ([ricerca/45 §1.2 e §3.2](../../ricerca/45-architettura-v3.md)).
- **Perché no**: la corsia S resta per chi ragiona a più passi; il lavoro ripetitivo costa meno e rischia meno nella corsia N ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md)).

### Alternativa: Hermes con il nostro Cancello, come in P-B

- **Pro**: canali, profili, bacheca e orari pronti ([ricerca/42, proposta B §2.2](../../ricerca/42-proposta-B-orchestratore-pronto.md)).
- **Contro**: ultima in classifica, con 67,7 punti; le quattro condizioni di [ADR-0012](0012-hermes-uscita.md) non sono soddisfatte ([ricerca/41 §3.4](../../ricerca/41-novita-al-9-novembre.md)).
- **Perché no**: Hermes resta un pilota in laboratorio; ne copiamo cinque idee, come `max_hops` e il blocco delle skill curate a mano ([ricerca/45 §1.3](../../ricerca/45-architettura-v3.md)).

## Conseguenze

### Positive

- La corsia N è la difesa più economica contro le iniezioni, perché il modello non sceglie né chi riceve né cosa si fa ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md)).
- Costa poco: Haiku 5.5 costa 0,10 $ per milione di token in ingresso e 0,50 $ in uscita ([ricerca/45 §3.2](../../ricerca/45-architettura-v3.md)).
- La milestone 1 non dipende da Claude Code né dagli aggiornamenti dell'SDK ([ricerca/45 §5, D6](../../ricerca/45-architettura-v3.md)).
- Rivendere il sistema alle PMI non incontra la licenza di n8n, perché la logica non sta in n8n ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).

### Negative

- Due modi di far girare gli agenti da mantenere, nello stesso codice.
- La corsia S chiede 12 GB di RAM con 6 sessioni e 20 GB con 12-16 ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- Anticipare la corsia S sposta lavoro dalla fase 2 ai mesi subito dopo la milestone 1: la stima va rifatta con Mattia, pezzo per pezzo ([ricerca/45 §9.3](../../ricerca/45-architettura-v3.md)).

### Rischi

- **L'Agent SDK cambia quasi ogni giorno**: versione fissata e prove a ogni aggiornamento; la corsia N non ne dipende ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).
- **Capacità della fase 1**: la settimana 8 può slittare alla 9 o alla 10; to-do in Jira ed evento in calendario entrano solo se c'è margine ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).

## Nota del 12 novembre 2026

- **«Le due corsie hanno le stesse regole» resta.** A ogni giro una sessione S carica le regole «Come lavoro» della persona, come una catena N. Ogni proposta di una sessione passa dal Cancello al livello della sua terna, attraverso lo strumento che propone ([ADR-0029](0029-corsia-s-sessioni-a-giri.md); [ADR-0001](0001-motore-agent-sdk.md), revisione del 12 novembre 2026).
- **I passaggi fra agenti non passano dal Cancello**, in tutte e due le corsie. Un passaggio è una riga della bacheca più un evento, scritti insieme dal motore. La frase «ogni azione passa dal Cancello» vale per le azioni che un agente propone, non per i passaggi. Così non si può più abbassare la terna dei passaggi di un agente ([ADR-0020](0020-autonomia-a-livelli.md)): al suo posto ci sono «Ferma» sul passaggio, il freno delle catene e lo stop ([ADR-0030](0030-bacheca-gruppi-specchi.md)).
- **Fino alla milestone 3 del PRD, quella delle prove con Microsoft e LiteLLM, le sessioni S chiamano l'API direttamente.** La corsia N fa già così, per una differenza dichiarata nello spec della milestone 1 (repo del codice); ora la stessa differenza vale anche per la corsia S ([ADR-0004](0004-litellm-banca-token.md); lo spec della milestone 2, repo del codice).

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §1, §3, §5, §6.1, §9.3, §10, §12.1](../../ricerca/45-architettura-v3.md)
- [ricerca/41, novità al 9 novembre, §3.4, §5 e §8.2](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/42, proposta A](../../ricerca/42-proposta-A-motore-a-livelli.md), [proposta B §2.2](../../ricerca/42-proposta-B-orchestratore-pronto.md) e [proposta D](../../ricerca/42-proposta-D-automazione-prima.md)
- [ricerca/44, verifiche avversarie](../../ricerca/44-verifiche-avversarie.md)
- [ricerca/35, giudizio di sicurezza §3.2](../../ricerca/35-giudizio-sicurezza.md)
- [ADR-0001](0001-motore-agent-sdk.md), rivista da questa ADR; [ADR-0010](0010-typescript-motore.md); [ADR-0012](0012-hermes-uscita.md)
