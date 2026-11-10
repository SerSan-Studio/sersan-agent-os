# ADR-0001: Motore degli agenti costruito sull'Agent SDK di Claude

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata; Michele l'ha già recepita ([domande per Michele, "Già recepito"](../../DOMANDE-PER-MICHELE.md)); rivista il 2026-11-10 da [ADR-0021](0021-motore-a-due-corsie.md): l'Agent SDK diventa la corsia S del motore

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
