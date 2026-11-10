# ADR-0011: n8n per orari e integrazioni, il motore non lo duplica

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata; rivista il 2026-11-10 da [ADR-0022](0022-eventi-e-sveglia-nel-motore.md): la sveglia sta nel motore e n8n diventa facoltativo

**Chi decide**: Alberto e Michele, che guidano la costruzione ([proposta §10](../../PRESENTAZIONE-CEO.md)); n8n è già nel board di Michele, e le scelte sull'infrastruttura restano sue ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md), [proposta §14](../../PRESENTAZIONE-CEO.md))

## Contesto

- L'Agent SDK non ha né orari né una coda dei lavori: la coda la scriviamo noi ([ricerca/26 §3.5 e §8](../../ricerca/26-claude-agent-sdk.md)).
- Il board di Michele, il disegno dell'infrastruttura, ha già n8n, un servizio di automazioni con orari e webhook (chiamate che un servizio fa quando succede qualcosa); nel board è n8n che ogni notte fa girare la ricerca dei bandi ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)).
- L'architettura del primo giro, del 24/10, aveva scelto di non usare n8n; il board ha cambiato il quadro ([ricerca/22 §3](../../ricerca/22-architettura-scelta.md), [ricerca/25 §2, C27](../../ricerca/25-board-michele-e-delta.md)).

## Decisione

- **Orari e integrazioni li fa n8n, i budget li tiene LiteLLM, la memoria sta in PostgreSQL, Qdrant e BookStack: il motore non duplica nulla** ([proposta §5.3](../../PRESENTAZIONE-CEO.md), [ADR-0001](0001-motore-agent-sdk.md), [ADR-0004](0004-litellm-banca-token.md), [ADR-0005](0005-memoria-postgres-qdrant-bookstack.md)).
- n8n lancia i lavori a orario (il debrief delle 7:00, i bandi della notte) e riceve gli ingressi su webhook firmati, come il modulo del sito e Instantly, lo strumento delle campagne email. Per ogni lavoro inserisce una riga nella coda del motore, in PostgreSQL, con una chiamata HTTP firmata ([ricerca/26 §3.5 e §8](../../ricerca/26-claude-agent-sdk.md), [proposta, appendice A, G5](../../PRESENTAZIONE-CEO.md)).
- Porta nella memoria i dati che arrivano a orario, come le trascrizioni di Teams lette da Graph, l'API di Microsoft 365, e i numeri di Sirius, la fonte dei dati fiscali e dei clienti nel board ([ricerca/36 §7.3](../../ricerca/36-architettura-v2.md), [proposta, appendice A, K14](../../PRESENTAZIONE-CEO.md)).
- Tre regole:
  - n8n non manda nulla a clienti o prospect: ogni azione esterna passa dal Cancello, il nostro esecutore unico ([ricerca/25 §2, C27](../../ricerca/25-board-michele-e-delta.md), [ADR-0003](0003-cancello-approvazioni.md));
  - da internet si raggiungono solo i suoi webhook firmati, senza moduli pubblici ([ricerca/36 §4.5](../../ricerca/36-architettura-v2.md));
  - la logica del motore non dipende da n8n: n8n chiama il motore e basta ([ricerca/26 §8](../../ricerca/26-claude-agent-sdk.md)).
- Nessun processo aziendale gira sui compiti programmati di Claude Team: tutto ciò che è a orario resta in n8n ([ricerca/36 §5.6](../../ricerca/36-architettura-v2.md)).

## Alternative considerate

### Alternativa: una corsia d'ingresso nostra, senza n8n, come nel primo giro

- **Pro**: un componente in meno e nessuna licenza che vieta la rivendita ([ricerca/22 §3](../../ricerca/22-architettura-scelta.md)).
- **Contro**: rifà ciò che il board ha già e usa per i bandi ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)).
- **Perché no**: n8n resta nel board, e la sua licenza ammette l'uso interno ([ricerca/25 §2, C27](../../ricerca/25-board-michele-e-delta.md)).

### Alternativa: orari e webhook di Hermes

- **Pro**: in Hermes, l'orchestratore open source valutato come alternativa al motore, orari, canali, profili e bacheca funzionano senza scrivere codice ([ricerca/27 §9.5](../../ricerca/27-hermes-self-hosted.md)).
- **Contro**: nel board sono doppioni: orari e webhook li fa n8n, chiavi e budget LiteLLM ([ricerca/27 §9.3](../../ricerca/27-hermes-self-hosted.md)).
- **Perché no**: Hermes oggi non entra nel percorso dei clienti ([ADR-0012](0012-hermes-uscita.md)).

### Alternativa: i compiti programmati di Claude Team

- **Pro**: ci sono già nel piano Team, senza servizi da installare ([ricerca/35, giudizio CPTO §2](../../ricerca/35-giudizio-cpto.md)).
- **Contro**: sono in anteprima, appartengono a un solo account e agiscono a suo nome, non girano più di una volta l'ora ([ricerca/35, giudizio CPTO §2](../../ricerca/35-giudizio-cpto.md)); includono di serie tutti i connettori, scritture comprese, e una scrittura salterebbe il Cancello ([ricerca/35, giudizio sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)).
- **Perché no**: niente processi aziendali sull'account di una persona; i compiti personali restano per l'uso individuale ([ricerca/35, giudizio CEO §9](../../ricerca/35-giudizio-ceo.md)).

## Conseguenze

### Positive

- Nessun servizio nuovo per orari e ingressi, e il motore resta piccolo ([proposta §5.3](../../PRESENTAZIONE-CEO.md)).
- Ogni pezzo ha un solo padrone: n8n, LiteLLM e la memoria ([ricerca/36 §2.1](../../ricerca/36-architettura-v2.md)).

### Negative

- La licenza di n8n ammette l'uso interno ma vieta la rivendita: se offriremo il sistema alle PMI, n8n non può entrare in ciò che si rivende ([ricerca/25 §7, N13](../../ricerca/25-board-michele-e-delta.md), [proposta §2.3](../../PRESENTAZIONE-CEO.md)).
- n8n può scrivere fuori senza passare dal Cancello: dove si può, usa credenziali in sola lettura ([ricerca/25 §4.11, S13-11](../../ricerca/25-board-michele-e-delta.md)).
- Il nodo Teams di n8n registra solo l'ora della risposta, non chi approva: serve solo per gli avvisi ([ricerca/36 §5.6](../../ricerca/36-architettura-v2.md)).

### Rischi

- Nel 2026 n8n ha avuto una vulnerabilità grave (CVE-2026-21858, con CVSS 10, il punteggio di gravità massimo, secondo fonti di terzi non verificate): solo webhook firmati e patch entro 14 giorni ([ricerca/36 §4.5](../../ricerca/36-architettura-v2.md)).
- n8n arriva in casa con le fasi del board: finché non c'è il posto per gli agenti sul server, il pilota gira sul banco di prova del laboratorio ([proposta §11](../../PRESENTAZIONE-CEO.md), [domande per Michele, n. 2](../../DOMANDE-PER-MICHELE.md)).

## Revisione del 10 novembre 2026

- **Orari ed eventi passano al motore**: gli orari stanno in una tabella del motore, gli eventi entrano da `POST /eventi` e finiscono nel registro degli eventi, con una chiave per evento ([ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- **Il delta di Graph lo legge il nostro codice**, e il token delta avanza solo dopo che l'evento è registrato; il testo rosso non passa da n8n ([ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- **n8n diventa facoltativo**: resta nel board di Michele per i collegamenti che servono, ma il sistema di agenti non ne dipende. Se un collegamento passa da n8n, n8n chiama `POST /eventi` e basta ([ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- Regole in più per n8n, quando c'è: versione 2.x fissata, una sola istanza; nessun dato rosso nelle esecuzioni; per gli orari «If Execution Is Missed = Run the Most Recent» ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md); [ricerca/42, proposta D §4.4](../../ricerca/42-proposta-D-automazione-prima.md)).
- Le routine di Claude restano per l'uso personale: agiscono come la persona, partono al massimo una volta l'ora, sono in anteprima, dipendono dai limiti d'uso del posto e scavalcano il Cancello ([ricerca/41 §1.4 e §8.2](../../ricerca/41-novita-al-9-novembre.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- La regola che la logica del motore non dipende da n8n resta, ed è più forte: ora non ne dipende neanche l'avvio.

## Fonti

- [Proposta 2.1: §2.3, §5.3, §10, §11, §14, appendice A (G5, K14)](../../PRESENTAZIONE-CEO.md)
- [ricerca/25: il board di Michele, §1, §2 (C27), §4.11 (S13-11), §7 (N13)](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/26 §3.5 e §8: cosa l'SDK non dà e chi lo copre](../../ricerca/26-claude-agent-sdk.md)
- [ricerca/36 §2.1, §4.5, §5.6, §7.3: architettura v2](../../ricerca/36-architettura-v2.md)
- [ricerca/22 §3: la scelta del primo giro](../../ricerca/22-architettura-scelta.md)
- [ricerca/27 §9: cosa Hermes porta e cosa duplica](../../ricerca/27-hermes-self-hosted.md)
- [ricerca/35: giudizio del CEO §9](../../ricerca/35-giudizio-ceo.md), [giudizio del CPTO §2](../../ricerca/35-giudizio-cpto.md), [giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)
- [Domande per Michele, n. 2](../../DOMANDE-PER-MICHELE.md)
