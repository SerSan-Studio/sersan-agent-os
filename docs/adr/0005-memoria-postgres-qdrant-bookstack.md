# ADR-0005: Memoria aziendale su PostgreSQL 16, Qdrant e BookStack, embedding in casa

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata

**Chi decide**: Michele Sanna (CPTO), perché questi servizi sono nel suo board ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)); per i dati rossi verso Claude Team decidono il parere legale, chiesto con la decisione 2 dei CEO, e la valutazione d'impatto, entro la settimana 3 ([proposta §5.6 e §14, decisione 2](../../PRESENTAZIONE-CEO.md)).

## Contesto

Il "secondo cervello" chiede due memorie sul nostro server: una relazionale, per processi, obiettivi, regole di lavoro e catalogo, e una vettoriale, che cerca per significato in trascrizioni, mail e documenti ([proposta §2.2](../../PRESENTAZIONE-CEO.md)). La prima versione usava Notion e PostgreSQL 17 con pgvector, l'estensione che aggiunge a PostgreSQL la ricerca vettoriale ([ricerca/25 §2, C02 e C11](../../ricerca/25-board-michele-e-delta.md)). Il board di Michele non ha Notion; ha PostgreSQL 16, Qdrant, BookStack e una pipeline che rende ricercabili i documenti e li serve con un MCP RAG, il servizio di ricerca che applica i permessi di chi chiede ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)). Molti dati sono rossi, cioè delicati: trascrizioni integrali, mail intere, documenti dei clienti, finanza ([proposta §5.6](../../PRESENTAZIONE-CEO.md)).

## Decisione

Ogni tipo di dato ha una sola fonte di verità ([proposta §5.5](../../PRESENTAZIONE-CEO.md)):

| Dove | Cosa contiene |
|---|---|
| BookStack, il wiki sul server | regole di lavoro di ciascuno ("Come lavoro"), processi, catalogo servizi, manuale degli agenti |
| PostgreSQL 16, sul server | registro e organigramma degli agenti, obiettivi, prezzi, registro dei meeting, decisioni, passaggi fra agenti |
| Qdrant, il database vettoriale sul server | trascrizioni, mail, documenti, dati di Sirius (fiscali, clienti, documenti), bandi, pagine di BookStack, issue di Jira |
| Jira | to-do e progetti |
| M365 | documenti, posta e calendario |

- **Embedding in casa**: gli embedding, il testo tradotto in numeri per cercarlo per significato, si calcolano sulla nostra GPU; il contenuto non esce ([proposta §5.5](../../PRESENTAZIONE-CEO.md)).
- **Ricerca ibrida**: per significato e per parole esatte (BM25), con un reranker che riordina i risultati ([proposta, appendice A, A3](../../PRESENTAZIONE-CEO.md)).
- **Una sola porta**, l'MCP RAG, per Claude Team e per gli agenti; per gli agenti il motore firma un token, cioè un lasciapassare digitale, di breve durata con l'identità della persona, mai scritto dal modello ([ricerca/36 §5.5](../../ricerca/36-architettura-v2.md)).
- **I numeri si calcolano** dal codice sui dati, non si cercano nel testo ([proposta §5.5](../../PRESENTAZIONE-CEO.md)).
- **Dati rossi**: a Claude Team arrivano solo oscurati, finché parere e valutazione d'impatto non decidono ([proposta §5.6](../../PRESENTAZIONE-CEO.md)).
- **Tempi**: memoria per gli agenti nella fase 2; ricerca con i permessi di ciascuno, anche da Claude Team, nella fase 3 ([proposta §11](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: Notion e PostgreSQL 17 con pgvector, come nella prima versione

- **Pro**: Notion ha tabelle vive filtrabili, che BookStack non ha ([ricerca/29 §3.3](../../ricerca/29-conoscenza-task-e-documenti.md)); con pgvector un solo database fa le due memorie ([ricerca/12 §6](../../ricerca/12-altre-piattaforme.md)).
- **Contro**: Notion è fuori dal board e costava 35,74 € al mese ([ricerca/33 §2.1](../../ricerca/33-costi-v2.md)); per i vettori il board usa Qdrant ([ricerca/25 §2, C11](../../ricerca/25-board-michele-e-delta.md)).
- **Perché no**: il board è vincolante ([ricerca/25, intestazione](../../ricerca/25-board-michele-e-delta.md)).

### Alternativa: Claude Team come deposito della memoria

- **Pro**: dalla fase 0 tutti e quattro ci lavorano ogni giorno, con chat, skill e progetti per squadra ([proposta §4.11 e §11](../../PRESENTAZIONE-CEO.md)).
- **Contro**: il piano Team non ha log di audit, cioè il registro di chi ha fatto cosa, né conservazione personalizzata, né la Compliance API per i controlli ([ricerca/36 §1.3](../../ricerca/36-architettura-v2.md)).
- **Perché no**: Claude Team è la finestra delle persone; la memoria resta sul server ([ricerca/36 §1.5](../../ricerca/36-architettura-v2.md)).

### Alternativa: mcp-memory come memoria aziendale

- **Pro**: è già nel board ([ricerca/29 §7.1](../../ricerca/29-conoscenza-task-e-documenti.md)).
- **Contro**: la versione di riferimento salva tutto in un file, senza utenti né permessi ([ricerca/29 §7.1](../../ricerca/29-conoscenza-task-e-documenti.md)).
- **Perché no**: resta un taccuino per ogni gruppo di agenti, mai con dati dei clienti ([ricerca/36 §5.5](../../ricerca/36-architettura-v2.md)).

## Conseguenze

### Positive

- Chiunque, anche da Claude Team, può chiedere "cosa ci siamo detti con X a settembre?" e avere la risposta con le fonti, vedendo solo ciò che può vedere ([proposta §5.5](../../PRESENTAZIONE-CEO.md)).
- Gli agenti leggono le regole di lavoro di ciascuno prima di ogni lavoro ([proposta §10](../../PRESENTAZIONE-CEO.md)).

### Negative

- BookStack chiede MySQL 8 o MariaDB 10.6, non PostgreSQL: MariaDB entra nel board, nei backup e nel monitoraggio ([ricerca/29 §3.1 e §3.3](../../ricerca/29-conoscenza-task-e-documenti.md)).
- Qdrant dà permessi per collezione, non per documento: quelli per documento li applica l'MCP RAG con filtri ([ricerca/36 §5.5](../../ricerca/36-architettura-v2.md)).

### Rischi

- **Dati rossi verso Claude Team**, che non ha un registro di audit: decisione entro la settimana 3 ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **Diritto alla cancellazione**: deve arrivare a PostgreSQL, Qdrant, ai log in Loki e ai backup ([ricerca/36 §5.7](../../ricerca/36-architettura-v2.md)).
- **Pezzi aperti**: la pipeline arriva con la fase F4 del board ([proposta, appendice A, A3](../../PRESENTAZIONE-CEO.md)); restano da chiarire cos'è Sirius e con cosa sostituire MinIO, l'archivio dei file, non più mantenuto ([domande per Michele, n. 11 e 25](../../DOMANDE-PER-MICHELE.md)).

## Fonti

- [Proposta per i CEO, §2.2, §4.11, §5.5, §5.6, §10, §11, §13, §14 e appendice A](../../PRESENTAZIONE-CEO.md)
- [ricerca/12, altre piattaforme, §6](../../ricerca/12-altre-piattaforme.md)
- [ricerca/25, il board di Michele, intestazione, §1 e §2](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/29, conoscenza, task e documenti, §3 e §7.1](../../ricerca/29-conoscenza-task-e-documenti.md)
- [ricerca/33, costi v2, §2.1](../../ricerca/33-costi-v2.md)
- [ricerca/36, architettura v2, §1.3, §1.5, §5.5 e §5.7](../../ricerca/36-architettura-v2.md)
- [Domande tecniche per Michele, n. 11 e 25](../../DOMANDE-PER-MICHELE.md)
