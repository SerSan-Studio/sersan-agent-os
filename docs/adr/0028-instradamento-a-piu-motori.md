# ADR-0028: Instradamento a più motori, con la corsia T sui posti Claude Team

**Data**: 2026-11-11

**Stato**: accettata dal gruppo di progetto; la corsia T entra solo dopo la prova di [ricerca/49 §7](../../ricerca/49-instradamento-a-piu-motori.md) e la conferma scritta di Anthropic prima della milestone 3

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)), su direttiva di Alberto dell'11 novembre. Michele decide i fornitori ammessi per i dati gialli, le repo che entrano in corsia T e il runner sul nostro server ([ricerca/49 §9](../../ricerca/49-instradamento-a-piu-motori.md)).

## Contesto

- L'11 novembre Alberto ha dato tre direttive ([ricerca/49, intestazione](../../ricerca/49-instradamento-a-piu-motori.md)):
  - per i modelli System One l'italiano non è un problema;
  - serve un instradamento che colleghi Jev, i modelli open-weight sul server e le sessioni di Claude Team;
  - oltre all'API, il sistema deve avviare sessioni di Claude Code sui posti Team per i compiti costosi, come lo sviluppo di progetti in codice.
- Fino a oggi la regola era: gli agenti usano la chiave API, mai i posti di Claude Team ([ADR-0001](0001-motore-agent-sdk.md); [ADR-0004](0004-litellm-banca-token.md); [ricerca/26 §5](../../ricerca/26-claude-agent-sdk.md)). E i compiti programmati di Claude restavano per l'uso personale delle persone ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md); [ADR-0024](0024-abbonamenti-come-riserva.md)). Questa ADR cambia le due regole per la sola corsia T.
- La pagina legale di Claude Code riserva il login dei piani all'«ordinary use of Claude Code and other native Anthropic applications». Chi costruisce prodotti con l'Agent SDK deve usare la chiave API e non può «collect, store, or intermediate Claude.ai credentials or session tokens» ([ricerca/49 §1.1](../../ricerca/49-instradamento-a-piu-motori.md)).
- Anthropic offre un meccanismo ufficiale per avviare una sessione di Claude Code da un programma: il compito programmato con avvio via API. Il token vale per un solo compito, non legge nulla e la sessione consuma l'uso del posto. È in anteprima, e l'API è sperimentale ([ricerca/49 §1.2](../../ricerca/49-instradamento-a-piu-motori.md)).
- Per il piano Team un programma non può sapere quanto uso resta su un posto ([ricerca/49 §1.3](../../ricerca/49-instradamento-a-piu-motori.md)).
- Il piano Team include fino a 500 $ al mese di crediti API, che coprono l'API e l'Agent SDK ma non Claude Code ([ricerca/49 §1.3](../../ricerca/49-instradamento-a-piu-motori.md)).
- Il decisore c'è già ([ADR-0027](0027-decisore.md)); il registro dei modelli dichiara capacità e colori ammessi ([ADR-0025](0025-un-modello-per-agente.md)).

## Decisione

- **Un router nel motore**, nel nostro codice TypeScript, sceglie la destinazione di ogni lavoro in tre passi ([ricerca/49 §2](../../ricerca/49-instradamento-a-piu-motori.md)):
  1. **regole fisse nel codice**, senza modelli: stop, tipo di evento già noto, corsie ammesse per l'agente, colore, capacità, tetti di spesa, conto del posto, classi fisse del Cancello;
  2. **il decisore**, solo per gli eventi a testo libero, con sei domande chiuse: `lavoro`, `complessita`, `serve_strumenti`, `tocca_impegni`, `sviluppo_o_lungo`, `urgente`;
  3. **una tabella** in `config/instradamento.yaml`, in git, con le soglie di partenza.
- **Sei destinazioni**:
  1. una regola nel codice;
  2. una catena della corsia N su un modello open-weight sul nostro server;
  3. una catena della corsia N su Claude via API;
  4. una sessione della corsia S, con l'Agent SDK e la chiave API;
  5. la **corsia T**: una sessione di Claude Code su un posto Claude Team;
  6. una persona.
- **Il motore del decisore**: Jev 1.14.0, fissato e chiamato via LiteLLM, per i testi verdi, e per i gialli quando Michele ammette TypeSafe. Per i testi rossi o di colore ignoto, un modello in casa o le regole. L'italiano non è un freno, per decisione di Alberto; la prova in italiano serve a tarare le soglie. I criteri di sicurezza di [ADR-0027](0027-decisore.md) restano come obiettivo delle soglie, domanda per domanda: dove nessuna soglia li raggiunge, quella domanda la decidono le regole o una carta ([ricerca/49 §1.4](../../ricerca/49-instradamento-a-piu-motori.md)).
- **La corsia T** ([ricerca/49 §3](../../ricerca/49-instradamento-a-piu-motori.md)):
  - si avvia **solo con il compito programmato e l'avvio via API**, sul posto della persona responsabile del lavoro. All'inizio gira sulle macchine di Anthropic; dalla milestone 3 su un runner nostro, se Michele lo ammette;
  - ogni persona crea il suo compito e il suo token dal suo account. Il token sta nel gestore dei segreti;
  - il motore manda solo dati. Il lavoro lo descrivono le istruzioni salvate dalla persona;
  - **consegna**: un branch `claude/…` e una pull request in bozza. La pull request è la proposta; unire in `main` è una carta L1, come vuole la classe «Codice e infrastruttura»;
  - **nessun connettore**, rete «Limited», solo repo di SerSan ammesse da Michele e con l'app di Claude solo lì, GitHub collegato con l'app e non con `/web-setup`;
  - **regole di GitHub senza eccezioni**: `main` solo con pull request e l'approvazione di una persona diversa dall'ultima che ha fatto push; nessuna modifica ai workflow di GitHub. Il proxy di Anthropic non limita i branch, e la sessione fa push con l'identità GitHub della persona ([ricerca/49 §1.2 e §3.2](../../ricerca/49-instradamento-a-piu-motori.md));
  - solo dati verdi e gialli: **mai rosso, neanche oscurato**;
  - serve lo sviluppo di progetti in codice e i lavori lunghi di quattro agenti: Sviluppatori, Agente sito e SEO, Pipeline per il portale clienti, Sistemista per le pull request di aggiornamento. Quali altri agenti possono mandare in T i lavori lunghi non di codice lo decide Alberto dopo la prova. Non serve il lavoro quotidiano dei 57 agenti.
- **Il login dei posti non entra nel motore.** Niente login claude.ai sul server, niente token di `claude setup-token`, niente `claude --cloud` dal motore. Il motore tiene solo i token dei compiti, che non sono un login: avviano un solo compito, non leggono nulla e non chiamano il modello ([ricerca/49 §1.2](../../ricerca/49-instradamento-a-piu-motori.md)). Le sessioni in background e `claude --cloud` restano alle persone sui loro computer. Gli avvii da GitHub dei compiti programmati restano ai compiti personali: i lavori del motore entrano da `POST /eventi`.
- **Regole comuni**:
  - nel dubbio si sale di un gradino e non si scende mai. La scala è 1 → 2 → 3 → 4 → 6, e per il rosso 1 → 2 → 6;
  - **la corsia T non sta nella scala**: un dubbio non manda mai in T;
  - un dato rosso non esce dal server se non oscurato, e verso T mai;
  - ogni effetto verso l'esterno passa dal Cancello, qualunque sia la corsia. In T il Cancello avvia il lavoro e riceve la consegna. Sulle macchine di Anthropic, dentro la sessione, lo sostituiscono i limiti di configurazione e le regole `deny` della repo; sul runner nostro i ganci e il server MCP del Cancello possono entrare dall'immagine del runner, da provare nella milestone 3 ([ricerca/49 §3.5](../../ricerca/49-instradamento-a-piu-motori.md));
  - una risposta del decisore non alza mai un livello: in T e in S il codice ha lo stesso tetto, una pull request che entra in `main` solo con il sì di una persona;
  - l'avvio di T passa dall'outbox e non si ripete da solo, perché l'avvio non ha una chiave contro i doppioni.
- **A uso finito**: il motore tiene un conto per posto (al massimo 2 lavori T aperti e 4 consegne al giorno per persona). Un lavoro T ha una scadenza; se la consegna manca, il lavoro torna in coda dopo 5 ore oppure, se è urgente, ripiega sulla corsia S con un tetto di spesa per lavoro. Tutti questi numeri sono [proposta].
- **Milestone**: la milestone 1 non cambia. Il router e l'adattatore T di prova entrano nella milestone 2; T sui progetti veri nella milestone 3 ([ricerca/49 §8](../../ricerca/49-instradamento-a-piu-motori.md)).

## Alternative considerate

### Alternativa: solo API per tutto, come finora

- **Pro**: un solo modo di pagare e di controllare; tutto resta sotto i ganci del Cancello; con i crediti API del Team una parte della spesa è già coperta ([ricerca/49 §1.3](../../ricerca/49-instradamento-a-piu-motori.md)).
- **Contro**: lo sviluppo pesante si paga a token, circa 7-14 $ per mezza giornata [stima di ricerca/49 §1.5], mentre l'uso dei posti già pagati resta fermo. Non segue la direttiva di Alberto.
- **Perché no**: resta la strada di ripiego di T e il default per tutto ciò che non è sviluppo o lavoro lungo.

### Alternativa: il login dei posti dentro il motore

- **Pro**: l'Agent SDK o `claude -p` userebbero i posti per tutti gli agenti, a costo marginale zero.
- **Contro**: è il caso che la pagina legale di Anthropic esclude: un prodotto costruito con l'Agent SDK sopra il login dei piani, con il motore che custodisce i token delle persone ([ricerca/49 §1.1](../../ricerca/49-instradamento-a-piu-motori.md)). Anthropic può intervenire senza preavviso.
- **Perché no**: viola i termini. Scartata.

### Alternativa: Jev chiamato direttamente da ogni catena

- **Pro**: un passaggio in meno; ogni catena decide da sola.
- **Contro**: soglie sparse; nessun controllo del colore in un punto solo; la chiave di TypeSafe fuori da LiteLLM; ogni cambio di versione da rifare in ogni catena ([ADR-0027](0027-decisore.md); [ADR-0004](0004-litellm-banca-token.md)).
- **Perché no**: Jev è uno dei motori dietro il decisore, chiamato via LiteLLM.

### Alternativa: nessun instradamento, corsia fissata a mano per agente

- **Pro**: semplice e prevedibile; niente decisore per scegliere la corsia.
- **Contro**: un agente come lo Smistatore posta o il Capo di gabinetto riceve lavori molto diversi; con la corsia fissa, o tutto va in S e costa di più, o tutto va in N e i lavori difficili escono male. Non sfrutta i posti per lo sviluppo.
- **Perché no**: le corsie ammesse restano fissate per agente nel registro, che è il primo filtro; dentro quelle sceglie il router.

### Alternativa: la corsia T con le sessioni in background o con `claude --cloud` sul server

- **Pro**: più controllo sulla sessione; risultati leggibili in JSON.
- **Contro**: tutte e due chiedono sul server il login di una persona ([ricerca/49 §1.2](../../ricerca/49-instradamento-a-piu-motori.md)).
- **Perché no**: le usa la persona sul suo computer, non il motore.

### Alternativa: la corsia T con GitHub Actions e il token dell'abbonamento

- **Pro**: è un meccanismo ufficiale: `claude-code-action` accetta un token di `claude setup-token`, e allora le esecuzioni usano il piano invece dell'API ([ricerca/49 §1.2, B6 e B7](../../ricerca/49-instradamento-a-piu-motori.md)).
- **Contro**: il token vale un anno, chiama il modello e starebbe nei segreti di GitHub, leggibile da ogni workflow che lo usa; per un segreto condiviso Anthropic stessa consiglia la chiave API, perché il token è legato all'abbonamento di chi l'ha creato. Il motore avvierebbe un servizio nostro sopra il login di una persona.
- **Perché no**: il token del compito programmato è più stretto (un compito, nessuna lettura, nessuna chiamata al modello). GitHub Actions resta, con la chiave API, per la revisione automatica delle pull request.

### Alternativa: gli avvii da GitHub dei compiti programmati

- **Pro**: un'etichetta su una issue fa partire il lavoro senza codice nostro ([ricerca/49 §1.2, B2](../../ricerca/49-instradamento-a-piu-motori.md)).
- **Contro**: il lavoro partirebbe senza passare dal motore: niente conto per posto, niente registro, niente stop.
- **Perché no**: l'etichetta arriva al motore come evento, e il motore decide l'avvio ([ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).

## Conseguenze

### Positive

- I posti Team lavorano anche quando le persone non sono davanti, per lo sviluppo, dentro un meccanismo che Anthropic offre per questo.
- Una sola tabella in git dice dove va ogni lavoro e perché; ogni scelta lascia una riga nel registro.
- Jev, i modelli in casa, l'API e i posti stanno dietro un'unica regola sui colori.
- Il codice e i file delle sessioni T restano in casa quando c'è il runner nostro.

### Negative

- Lavoro in più nella milestone 2: router, adattatore T, lettore di GitHub, conto per posto, circa 4-6 gp [stima di ricerca/49 §8].
- T dipende da una funzione in anteprima con un'API sperimentale.
- L'uso di T toglie uso alla persona del posto, e il motore non lo vede prima di avviare.
- Ogni persona con T deve preparare il suo compito, il suo token e le regole della sua repo.

### Rischi

- **Anthropic legge l'uso in modo diverso dal nostro**: il motore non tocca il login; T solo per sviluppo e lavori lunghi della persona responsabile; conto per posto; conferma scritta prima della milestone 3 ([ricerca/49 §6](../../ricerca/49-instradamento-a-piu-motori.md)).
- **Una sessione T fa più di quanto deve**: nessun connettore, rete «Limited», `main` protetto senza eccezioni, nessuna modifica ai workflow di GitHub, unione solo con revisione, testo dell'avvio trattato come dato; nessun avvio vale come approvazione di un'azione.
- **Doppio avvio o avvio perso**: outbox con esito «incerto» e ricerca del branch su GitHub.
- **Dati sul cloud di Anthropic**: niente rosso; elenco delle repo ammesse; runner nostro dalla milestone 3.
- **La funzione cambia o sparisce**: adattatore separato e ripiego sulla corsia S senza toccare le catene.

## Fonti

- [ricerca/49, instradamento a più motori: §1 (i fatti), §2 (l'instradamento), §3 (la corsia T), §4 (dati e colori), §5 (costi), §6 (rischi), §7 (la prova), §8 (milestone), §9 (decisioni)](../../ricerca/49-instradamento-a-piu-motori.md)
- [ricerca/47, modelli System One e decisore](../../ricerca/47-modelli-system-one.md)
- [ricerca/45, architettura v3, §2.2 e §12](../../ricerca/45-architettura-v3.md)
- [ricerca/26, Agent SDK, §5](../../ricerca/26-claude-agent-sdk.md)
- [ADR-0001](0001-motore-agent-sdk.md), rivista da questa ADR; [ADR-0004](0004-litellm-banca-token.md), rivista; [ADR-0009](0009-dati-tre-colori.md); [ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md), rivista; [ADR-0024](0024-abbonamenti-come-riserva.md), rivista; [ADR-0025](0025-un-modello-per-agente.md), rivista; [ADR-0027](0027-decisore.md), rivista
