# ADR-0012: Hermes come uscita già prezzata, con le verifiche delle settimane 8 e 21

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata

**Chi decide**: Alberto e Michele, che guidano la costruzione ([proposta §10](../../PRESENTAZIONE-CEO.md)); alle verifiche delle settimane 8 e 21 si decide sui numeri, e i CEO decidono se finanziare la fase dopo ([proposta §1 e §11](../../PRESENTAZIONE-CEO.md))

## Contesto

- Hermes Agent è un orchestratore open source (licenza MIT) che dà pronti canali, profili con nome, bacheca dei compiti e orari ([ricerca/27, in breve](../../ricerca/27-hermes-self-hosted.md), [ricerca/36 §2.1](../../ricerca/36-architettura-v2.md)). Il primo giro di confronto, il 24/10, lo aveva scelto con 159 punti su 240 ([proposta, appendice B](../../PRESENTAZIONE-CEO.md)).
- Il board di Michele ha già n8n e LiteLLM, e Michele ha chiesto di valutare se si può evitare Hermes con l'Agent SDK di Claude, senza escluderlo a priori ([ricerca/25, in breve](../../ricerca/25-board-michele-e-delta.md), [proposta §5.7](../../PRESENTAZIONE-CEO.md)).
- Nel secondo giro quattro agenti giudici hanno dato 171,5 punti al motore sull'Agent SDK, 170 a Claude Team al centro e 137 a Hermes sul nostro server ([proposta §5.7](../../PRESENTAZIONE-CEO.md)).

## Decisione

- Il motore degli agenti è nostro, sull'Agent SDK ([ADR-0001](0001-motore-agent-sdk.md)). Hermes oggi non entra nel percorso dei clienti, ma resta una porta aperta con il costo già stimato ([proposta §5.7](../../PRESENTAZIONE-CEO.md), [ricerca/36 §2.4](../../ricerca/36-architettura-v2.md)).
- **Verifica della settimana 8**, sul banco di prova. I criteri tecnici, quelli che riguardano il motore: tre agenti per una settimana senza scambiarsi le sessioni; nessun effetto senza una carta del Cancello, anche nei dieci scenari di prova; una carta ferma la notte riprende il lavoro giusto al mattino; l'approvazione arriva dal telefono con l'identità giusta; la spesa resta nel tetto; un aggiornamento dell'SDK passa i dieci scenari entro 14 giorni; nessun dato rosso salvato. Accanto ci sono i criteri commerciali, come l'email attiva e i post dei founder ([proposta §11](../../PRESENTAZIONE-CEO.md)).
- **Verifica della settimana 21**, prima di passare alla memoria con i dati dei clienti: gli stessi criteri tecnici, sul server; la revisione esterna di Cancello, motore e bot fatta, con i rilievi gravi chiusi; nessuna risposta del lavoro di una persona finita in un canale aperto a tutti; tutti i servizi nuovi in inventario, con le patch entro 14 giorni; il backup 3-2-1 (tre copie, su due supporti, una fuori dall'ufficio) in funzione, con una prova di ripristino riuscita; la RAM misurata e la decisione d'acquisto presa ([proposta §11](../../PRESENTAZIONE-CEO.md)).
- Se un criterio tecnico fallisce, due settimane per correggere; se il problema è di struttura, proviamo Hermes sullo stesso banco con gli stessi scenari e decidiamo sui numeri. La prova costa 6-8 giorni di sviluppo, usarlo al posto del motore 26-33 con la riserva; Cancello, memoria, server MCP, bot e skill restano uguali ([proposta §5.7, §11 e §15](../../PRESENTAZIONE-CEO.md)).
- Hermes diventa il nostro orchestratore solo se chiude i suoi problemi di sicurezza: versione 0.23 uscita con note complete; chiuse le righe di sicurezza della sua scheda dei problemi (MSG-43, GW-41, KB-10, HR-6) e il difetto dei documenti su Teams (#113578); un aggiornamento che passa i dieci scenari senza interventi a mano ([proposta §5.7](../../PRESENTAZIONE-CEO.md), [ricerca/36 §2.4](../../ricerca/36-architettura-v2.md)).

## Alternative considerate

### Alternativa: Hermes come orchestratore subito

- **Pro**: è pronto oggi, con Teams, Telegram, WhatsApp e più di 25 altri canali, profili con nome, bacheca, skill che migliorano e una comunità enorme ([ricerca/36 §2.1 e §2.2](../../ricerca/36-architettura-v2.md)).
- **Contro**: il suo gateway unico, il processo che tiene insieme tutti i canali e i profili, ha 276 problemi aperti, 9 di sicurezza e 0 risolti; verso la memoria passa un valore fisso o il nome del profilo, non la persona; la bacheca funziona su un solo host; almeno 45 avvisi di sicurezza nel 2026 ([ricerca/36 §1.4 e §2.1](../../ricerca/36-architettura-v2.md)); funzioni doppie con n8n e LiteLLM ([proposta §5.7](../../PRESENTAZIONE-CEO.md)).
- **Perché no**: 137 punti contro 171,5, e Michele preferisce evitarlo ([proposta §5.7](../../PRESENTAZIONE-CEO.md), [ricerca/36 §1.4](../../ricerca/36-architettura-v2.md)).

### Alternativa: Claude Team al centro, senza un motore nostro

- **Pro**: è la più rapida a dare valore, e la sua fase zero è entrata nel piano ([proposta §5.7](../../PRESENTAZIONE-CEO.md)).
- **Contro**: da sola trasforma molti agenti in strumenti da aprire a mano ([proposta §5.7](../../PRESENTAZIONE-CEO.md)); il piano Team non ha registro di audit, e la proposta esponeva sei endpoint su internet invece di uno ([ricerca/36 §1.3](../../ricerca/36-architettura-v2.md)).
- **Perché no**: perde l'autonomia di 10 figure e manda più dati a un servizio senza registro ([ricerca/35, giudizio CPTO §5](../../ricerca/35-giudizio-cpto.md)).

## Conseguenze

### Positive

- L'uscita è scritta e ha un prezzo, e il costo al mese non cambia: la licenza è zero in entrambi i casi e si paga solo l'API ([proposta §12.1 e §15](../../PRESENTAZIONE-CEO.md)).
- Ogni pezzo sta dietro un'interfaccia: il motore parla con gli strumenti solo via MCP, il protocollo standard degli strumenti, con i modelli solo via LiteLLM, con l'esterno solo via Cancello ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)).

### Negative

- Bacheca fra agenti, profili con nome e bot per le chat li scriviamo noi, mentre Hermes li darebbe pronti, e i loro bug sono nostri ([proposta §5.3](../../PRESENTAZIONE-CEO.md), [ricerca/36 §2.2](../../ricerca/36-architettura-v2.md)).
- Se si usa l'uscita si perdono il runner, che avvia un processo per ogni lavoro, e il ponte verso il Cancello ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)).

### Rischi

- L'Agent SDK cambia quasi ogni giorno: versione fissata e aggiornamento ogni due settimane dopo i dieci scenari ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- Hermes potrebbe non chiudere i suoi problemi in tempo: allora resta solo un pilota confinato in laboratorio, con dati verdi ([ricerca/35, giudizio CPTO §5](../../ricerca/35-giudizio-cpto.md)).
- Cancello, motore e bot sono codice scritto su misura che nessuno ha ancora rivisto: revisione esterna entro la settimana 21 (decisione 5) ([proposta §13 e §14](../../PRESENTAZIONE-CEO.md)).

## Fonti

- [Proposta 2.1: §1, §5.3, §5.7, §10, §11, §12.1, §13, §14, §15, appendice B](../../PRESENTAZIONE-CEO.md)
- [ricerca/36: architettura v2, §1.3, §1.4, §2.1, §2.2, §2.4, §12](../../ricerca/36-architettura-v2.md)
- [ricerca/27: Hermes Agent tutto in casa](../../ricerca/27-hermes-self-hosted.md)
- [ricerca/25: il board di Michele, in breve](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/35: giudizio del CPTO §5](../../ricerca/35-giudizio-cpto.md)
