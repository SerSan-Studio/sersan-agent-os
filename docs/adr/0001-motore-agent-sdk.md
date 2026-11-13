# ADR-0001: Motore degli agenti costruito sull'Agent SDK di Claude

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata; Michele l'ha già recepita ([domande per Michele, "Già recepito"](../../DOMANDE-PER-MICHELE.md)); rivista il 2026-11-10 da [ADR-0021](0021-motore-a-due-corsie.md): l'Agent SDK diventa la corsia S del motore; rivista il 2026-11-11 da [ADR-0028](0028-instradamento-a-piu-motori.md): i posti Team servono la corsia T, il motore resta sulla chiave API; rivista il 2026-11-12 da [ADR-0029](0029-corsia-s-sessioni-a-giri.md): il ponte verso il Cancello è lo strumento che propone, il gancio prima degli strumenti nega soltanto, la versione è fissata con la prova a copione di [ricerca/50](../../ricerca/50-agent-sdk-e-prova-a-copione.md)

**Chi decide**: Michele Sanna (CPTO) con Alberto Tuveri per la scelta tecnica ([ricerca/36 §10](../../ricerca/36-architettura-v2.md)); i CEO per il via e il budget di ogni fase ([proposta §14, decisione 1](../../PRESENTAZIONE-CEO.md)).

## Contesto

SerSan vuole 57 agenti AI in nove squadre ([proposta §1](../../PRESENTAZIONE-CEO.md)). Serve un motore: il programma che avvia ogni agente con i suoi strumenti e un tetto di spesa. Il 24 ottobre era stato scelto Hermes Agent, open source, con profili, bacheca e canali già pronti ([proposta, appendice B](../../PRESENTAZIONE-CEO.md); [ricerca/22 §1](../../ricerca/22-architettura-scelta.md)). Il 25 ottobre Michele ha chiesto di valutare l'Agent SDK di Claude, senza escludere Hermes a priori ([proposta §5.7](../../PRESENTAZIONE-CEO.md); [ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)). Il suo board, il disegno vincolante dell'infrastruttura, ha già n8n per gli orari, LiteLLM per i budget e PostgreSQL, Qdrant e BookStack per la memoria ([proposta §5.3](../../PRESENTAZIONE-CEO.md)).

## Decisione

Il motore lo scriviamo noi sull'Agent SDK di Claude, cioè Claude Code usato come libreria: un processo per lavoro, con il profilo dell'agente, i suoi strumenti e un tetto di spesa. È la Proposta 1, prima nel confronto del 25 ottobre con 171,5 punti su 240 ([proposta §5.1 e §5.7](../../PRESENTAZIONE-CEO.md); [ricerca/34, Proposta 1](../../ricerca/34-proposta-1-agent-sdk.md)).

- **Solo ciò che manca**: il runner che avvia le sessioni, il registro dei profili, la bacheca fra agenti con un freno alle catene troppo lunghe, l'adattatore verso la chat ([ricerca/26, In breve](../../ricerca/26-claude-agent-sdk.md)).
- **Il Cancello nel motore**: prima di ogni strumento un hook, cioè una funzione nostra chiamata dall'SDK, chiede al Cancello; senza risposta in tempo, l'azione è bloccata ([proposta §5.3](../../PRESENTAZIONE-CEO.md); [ricerca/36 §1.2](../../ricerca/36-architettura-v2.md)).
- **La persona fino alla memoria**: i server MCP, le prese con cui un agente usa gli strumenti, ricevono l'identità di chi ha avviato il lavoro, così ognuno vede solo ciò che può vedere ([ricerca/36 §1.2](../../ricerca/36-architettura-v2.md)).
- **Chiave API, mai i posti di Claude Team** ([ricerca/26 §5.2](../../ricerca/26-claude-agent-sdk.md)); gli agenti parlano solo con LiteLLM, i server MCP e il Cancello ([proposta §5.4](../../PRESENTAZIONE-CEO.md)).
- **Versione fissata**, aggiornata ogni due settimane dopo dieci scenari di prova; nelle settimane 5-8 su una macchina di prova, poi sul server ([proposta §5.3, §11 e §13](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: Hermes Agent sul nostro server

- **Pro**: canali, profili, bacheca e skill, cioè procedure riusabili, sono già pronti ([ricerca/27 §9.5](../../ricerca/27-hermes-self-hosted.md)); la licenza costa zero, come per l'SDK ([proposta §12.1](../../PRESENTAZIONE-CEO.md)).
- **Contro**: 137 punti ([proposta §5.7](../../PRESENTAZIONE-CEO.md)); il gateway unico, il processo che tiene insieme canali e profili, ha 276 problemi aperti, 9 di sicurezza, e i permessi verso la memoria valgono per istanza, non per persona ([ricerca/36 §1.4](../../ricerca/36-architettura-v2.md)).
- **Perché no**: sicurezza e permessi per persona, e Michele preferisce evitarlo ([ricerca/35, giudizio CPTO §4.5 e §4.6](../../ricerca/35-giudizio-cpto.md)); resta un'uscita già stimata ([ADR-0012](0012-hermes-uscita.md)).

### Alternativa: Claude Team al centro

- **Pro**: 170 punti; dà valore prima, con ciò che SerSan paga già ([ricerca/34, Proposta 3, In breve](../../ricerca/34-proposta-3-claude-team-e-mcp.md)).
- **Contro**: dieci figure diventano skill da aprire a mano e 29 flussi fissi; il piano Team non ha log di audit, il registro di chi ha fatto cosa ([ricerca/36 §1.3](../../ricerca/36-architettura-v2.md)).
- **Perché no**: declassa troppi agenti; la sua fase zero, Claude Team per tutti dalla settimana 1, è entrata nel piano ([proposta §5.7](../../PRESENTAZIONE-CEO.md)).

### Alternativa: Managed Agents di Anthropic

- **Pro**: il ciclo dell'agente lo fa girare Anthropic, e gli strumenti possono girare in un nostro ambiente isolato (sandbox) ([ricerca/26 §1.2](../../ricerca/26-claude-agent-sdk.md)).
- **Contro**: il ciclo dell'agente e le sessioni starebbero nel cloud di Anthropic, fuori dal nostro server ([ricerca/26 §1.2](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: va contro la regola "tutto in casa" ([ADR-0002](0002-self-hosted-board-michele.md)).

## Conseguenze

### Positive

- Tutte le 57 figure sono agenti veri, senza doppioni con lo stack di Michele ([proposta §5.7](../../PRESENTAZIONE-CEO.md)).
- Strumenti solo via MCP, modelli solo via LiteLLM, esterno solo via Cancello: se il motore cambia, il resto resta ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)).

### Negative

- Bacheca, profili con nome e bot per le chat li scriviamo noi, mentre Hermes li darebbe pronti: sono giorni messi nel piano ([proposta §5.3 e §15](../../PRESENTAZIONE-CEO.md)).
- L'SDK cambia quasi ogni giorno: 333 versioni TypeScript dal 27/09/2025 ([ricerca/26 §1.1](../../ricerca/26-claude-agent-sdk.md)).

### Rischi

- **Il motore non regge**: verifiche alle settimane 8 e 21; se il problema è di struttura, si prova Hermes sullo stesso banco di prova ([proposta §11 e §13](../../PRESENTAZIONE-CEO.md)).
- **Codice su misura non ancora rivisto**: dieci scenari a ogni aggiornamento, revisione esterna entro la settimana 21 ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **Trappole di configurazione**: un hook "a comando", cioè un programma esterno, se scade non blocca; per questo il ponte verso il Cancello è un hook di callback dentro il motore ([ricerca/35, giudizio di sicurezza §2](../../ricerca/35-giudizio-sicurezza.md); [ricerca/36 §5.1](../../ricerca/36-architettura-v2.md)).

## Revisione del 10 novembre 2026

- Il motore resta sull'Agent SDK, ma come **corsia S**, accanto alla **corsia N** delle catene a schema, nello stesso codice TypeScript ([ADR-0021](0021-motore-a-due-corsie.md); [ricerca/45 §1.2 e §3.1](../../ricerca/45-architettura-v3.md)).
- La milestone 1 usa solo la corsia N. Il runner S, il ponte `propose_action` e il registro dei profili si costruiscono **subito dopo la milestone 1**, non alla settimana 9 ([ricerca/45](../../ricerca/45-architettura-v3.md), «Decisione del gruppo di progetto»).
- Un solo runner con al massimo 6 sessioni: escono il possesso, il battito e le riserve fra più runner ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- Il ponte verso il Cancello porta in un giro un pacchetto di scritture interne e un solo elemento esterno ([ricerca/45 §6.1](../../ricerca/45-architettura-v3.md)).
- Nella corsia S resta Claude finché una prova non dimostra che un modello locale regge ([ADR-0025](0025-un-modello-per-agente.md)).
- Managed Agents non è più solo un'alternativa scartata: è una riserva sui dati verdi, se il server è pieno o fermo ([ADR-0024](0024-abbonamenti-come-riserva.md)).
- La revisione esterna entro la settimana 21 non è più obbligatoria ([ADR-0023](0023-protezioni-essenziali.md)).

## Revisione dell'11 novembre 2026

- Il motore resta sulla chiave API: l'Agent SDK non usa mai il login dei posti Claude Team, come chiede la pagina legale di Anthropic ([ricerca/49 §1.1](../../ricerca/49-instradamento-a-piu-motori.md)).
- I posti Team servono una corsia nuova, la **corsia T**: il motore avvia, sul posto della persona responsabile, un compito programmato di Claude Code con l'avvio via API, per lo sviluppo di progetti in codice e i lavori lunghi. La consegna è un branch e una pull request ([ADR-0028](0028-instradamento-a-piu-motori.md)).
- La regola «chiave API, mai i posti di Claude Team» vale quindi per il motore e per i 57 agenti, non per la corsia T. Anche per T il motore non tiene il login di nessuno: tiene solo i token dei compiti, che avviano un solo compito, non leggono nulla e non chiamano il modello ([ricerca/49 §1.2](../../ricerca/49-instradamento-a-piu-motori.md)).

## Revisione del 12 novembre 2026

- **Il ponte verso il Cancello è lo strumento che propone, non il gancio.** A chiamare il Cancello è lo strumento `proponi_azione` (il `propose_action` della revisione del 10 novembre), che sta su un server MCP nostro dentro il processo del runner. Il Cancello risponde come nella corsia N: l'azione parte, va in carta o in finestra, oppure è negata. Il punto «Il Cancello nel motore» della Decisione, con un gancio che chiede al Cancello prima di ogni strumento, non vale più così: la garanzia è la stessa, la strada no ([ADR-0029](0029-corsia-s-sessioni-a-giri.md); [ricerca/50 §10, punti 2 e 3](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **Il gancio prima degli strumenti nega e basta.** È la seconda barriera: uno solo, su tutti gli strumenti, con `onFailure: "block"`, e non chiama mai il Cancello. La prova ha mostrato che senza quell'opzione un gancio che va in errore lascia passare tutto, e che nessun altro freno (interruzione, tetto di spesa, numero massimo di passi) ferma uno strumento già chiesto dal modello: lo ferma solo un gancio che nega ([ricerca/50 §3.2 e §6, punti 3 e 9](../../ricerca/50-agent-sdk-e-prova-a-copione.md)). Il rischio «Trappole di configurazione» resta, con questa correzione: il ponte non è più il gancio.
- **Niente pacchetto di scritture interne.** In un giro passa al più un'azione con effetto per ogni risposta del modello, ognuna con la sua voce nel diario, e al più un elemento esterno. Il punto della revisione del 10 novembre sul «pacchetto di scritture interne» non vale più ([ADR-0029](0029-corsia-s-sessioni-a-giri.md)).
- **L'identità arriva al ponte, non a server MCP esterni.** Una sessione usa solo gli strumenti del ponte: persona e cliente li mette il ponte dalla sessione, e le letture vedono solo i dati del cliente del compito. Il punto «La persona fino alla memoria» della Decisione vale così ([ADR-0029](0029-corsia-s-sessioni-a-giri.md)).
- **Una carta che aspetta una persona non usa il rinvio dell'SDK** (`defer`), che alla ripresa è instabile. Lo strumento risponde «in carta», il giro finisce, e l'esito della carta riprende la sessione ([ricerca/50 §3.2](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **La versione fissata oggi è la 0.3.322, esatta**, con dentro Claude Code 2.1.322 ([ricerca/50 §1.1](../../ricerca/50-agent-sdk-e-prova-a-copione.md)). La prova con il modello a copione (18 esperimenti, senza chiave API e senza traffico verso servizi veri) entra nella repo del codice come comando a parte, con sei misure in più (da E1 a E24): si rilancia a ogni cambio di versione, prima dei dieci scenari della corsia S ([ricerca/50 §2 e §3](../../ricerca/50-agent-sdk-e-prova-a-copione.md); lo spec della milestone 2, repo del codice).
- **Il login di Claude di chi usa la macchina non entra mai nella sessione.** L'ambiente del processo lo scrive tutto il motore, perché su Windows Node rimette i valori veri dell'utente per le variabili che mancano ([ricerca/50 §6, punto 2, e §7.2](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **Fino alla milestone 3 del PRD, quella di LiteLLM, le sessioni chiamano l'API direttamente**, non LiteLLM come dice la Decisione ([ADR-0021](0021-motore-a-due-corsie.md), nota del 12 novembre 2026).

## Fonti

- [Proposta per i CEO, §1, §5.1, §5.3, §5.4, §5.7, §11, §12.1, §13, §14, §15 e appendice B](../../PRESENTAZIONE-CEO.md)
- [Domande tecniche per Michele, "Già recepito"](../../DOMANDE-PER-MICHELE.md)
- [ricerca/22, l'architettura del primo giro, §1](../../ricerca/22-architettura-scelta.md)
- [ricerca/25, il board di Michele, §1](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/26, Agent SDK, In breve, §1.1, §1.2 e §5.2](../../ricerca/26-claude-agent-sdk.md)
- [ricerca/27, Hermes in casa, §9.5](../../ricerca/27-hermes-self-hosted.md)
- [ricerca/34, Proposta 1](../../ricerca/34-proposta-1-agent-sdk.md) e [Proposta 3, In breve](../../ricerca/34-proposta-3-claude-team-e-mcp.md)
- [ricerca/35, giudizio CPTO §4.5 e §4.6](../../ricerca/35-giudizio-cpto.md) e [giudizio di sicurezza §2](../../ricerca/35-giudizio-sicurezza.md)
- [ricerca/36, architettura v2, §1.2-1.4, §5.1, §10 e §12](../../ricerca/36-architettura-v2.md)
