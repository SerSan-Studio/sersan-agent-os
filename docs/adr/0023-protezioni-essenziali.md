# ADR-0023: Protezioni essenziali per un sistema aziendale chiuso

**Data**: 2026-11-10

**Stato**: accettata

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)).

## Contesto

- La revisione 2 dello spec della milestone 1, cioè il documento tecnico del nucleo di motore e Cancello, aveva 27 criteri e molte difese: firme HMAC sulle richieste fra processi, con numero monouso e ±60 secondi; registro a catena con MAC e ancora esterna; codici per consegna e impronta della Porta; epoche per lo stop; tre barriere provate una per una; macchine separate ([ricerca/45 §6.1 e §6.2](../../ricerca/45-architettura-v3.md)).
- La proposta v2.1 chiedeva anche la chiave fisica FIDO2 sulle carte di offerte, contratti, fatture e primi contatti, e una revisione esterna di Cancello, motore e bot entro la settimana 21, per circa 3.560-5.940 € ([ADR-0003](0003-cancello-approvazioni.md); [ricerca/45 §9.1](../../ricerca/45-architettura-v3.md)).
- SerSan Agent OS è un sistema aziendale chiuso: quattro persone, rete interna, accesso da fuori solo attraverso NetBird e Pangolin ([ADR-0018](0018-accesso-oracle-netbird-pangolin.md)).
- Tutte e quattro le proposte del terzo giro hanno tagliato le difese oltre l'essenziale, e il giudice «essenziale» le ha pesate ([ricerca/45 §1.2](../../ricerca/45-architettura-v3.md); [ricerca/43, giudizio essenziale](../../ricerca/43-giudizio-essenziale.md)).

## Decisione

**Restano** ([ricerca/45 §2.5, §2.7, §6.1 e §6.2](../../ricerca/45-architettura-v3.md)):

- **Limiti fissi nel codice**, non nella configurazione: cancellazioni e credenziali sempre negate e senza esecutore; pagamenti senza esecutore, li fa una persona; i tipi d'azione sconosciuti negati. Valgono anche chiamando direttamente l'API del Cancello (AC-007).
- **Il Cancello unico esecutore** delle azioni esterne, con l'outbox: si registra prima dell'effetto, l'effetto esce una volta sola e un esito «incerto» va a una persona (AC-001, AC-010, AC-025, AC-026).
- **Stop di emergenza**: lo preme chiunque dei quattro, dal telefono o con `/stop` in Teams; lo tolgono Alessandro o Michele. È un interruttore che l'esecutore legge subito prima dell'effetto; annulla carte e finestre aperte; dopo lo sblocco ripartono solo i nuovi eventi (AC-015, D2).
- **Tetti**: di spesa per lavoro e per agente al mese, con avviso all'80% e stop al 100%; di quantità per classe al giorno; il freno delle catene ([ADR-0020](0020-autonomia-a-livelli.md); [ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md)).
- **Registro a sola aggiunta**: una tabella dove l'utente del Cancello può solo inserire e leggere, con i segreti oscurati, il valore prima e dopo delle scritture interne, conservata 90 giorni (AC-017).
- **«Annulla» e «Rettifica»**: «Annulla» di una scrittura interna non cancella nulla, rimette il valore precedente o segna la voce come annullata; «Rettifica» dopo un invio crea una carta L1 e abbassa la terna.
- **Il testo di terzi non porta ad azioni**: nella corsia N entra solo come campi e il codice sceglie i destinatari (AC-013) ([ADR-0021](0021-motore-a-due-corsie.md)).
- **Un token per processo** fra motore, Cancello e Porta, al posto delle firme; i ruoli separati del database restano.
- **Conformità minima**: riga AI su ciò che esce a L2 e L3; lista di soppressione unica, per cui un «no» blocca le azioni verso quel contatto su tutti i canali; dati a tre colori e oscuramento prima del cloud ([ADR-0009](0009-dati-tre-colori.md)); riga nel registro dei trattamenti per ogni agente nuovo; parere legale con tetto di 2.500 € ([ricerca/45 §2.6, §2.8 e §9.1](../../ricerca/45-architettura-v3.md)).
- **Prove a ogni modifica**: la batteria di prove gira con un comando, gratis, su Windows e al banco anche su Linux; è l'unica revisione obbligatoria (AC-023). Mattia rivede il codice.

**Escono** ([ricerca/45 §1.2, §6.2 e §9.1](../../ricerca/45-architettura-v3.md)):

- la chiave FIDO2 come secondo passo sulle carte. Le chiavi restano per l'accesso al board con NetBird;
- le firme HMAC con numero monouso (AC-012);
- il registro a catena con MAC e ancora esterna (AC-016);
- i codici per consegna, l'impronta della Porta e il controllo dei caratteri invisibili. Resta la garanzia vera: l'esecutore ricalcola l'impronta del testo e manda ciò che la persona ha visto (AC-009);
- le epoche dello stop e la prova separata delle tre barriere (AC-006);
- la revisione esterna obbligatoria, che diventa facoltativa: si fa se un cliente la chiede;
- la macchina separata obbligatoria per il Cancello: può stare sulla stessa VM del motore, decide Michele.

**Bilancio dei 27 criteri**: 14 restano, 9 si alleggeriscono o si spostano, 4 si tolgono (AC-006, AC-012, AC-016, AC-020) ([ricerca/45 §6.2](../../ricerca/45-architettura-v3.md)).

## Alternative considerate

### Alternativa: lo spec della revisione 2 così com'è

- **Pro**: difese a più strati anche contro un attaccante dentro la rete; era già scritto e rivisto ([ricerca/45 §6.1](../../ricerca/45-architettura-v3.md)).
- **Contro**: circa 3,5 giorni di sviluppo in più nella fase 1, che non sta nella capacità; la revisione esterna costa 3.560-5.940 € ([ricerca/45 §9.1 e §9.3](../../ricerca/45-architettura-v3.md)).
- **Perché no**: in un sistema chiuso, con quattro persone, queste difese proteggono da rischi molto più piccoli di quelli veri, che sono il destinatario sbagliato e il doppio invio. Contro quelli restano idempotenza, indirizzo esatto, controllo del contenuto e stop.

### Alternativa: affidarsi alle difese dell'Agent SDK e dei fornitori

- **Pro**: modalità auto, regole deny e tetti dell'SDK sono pronti ([ricerca/41 §8.2](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: Anthropic può spegnere la modalità auto lato server; i tetti dell'SDK sono stime del client ([ricerca/41 §8.2](../../ricerca/41-novita-al-9-novembre.md); [ADR-0004](0004-litellm-banca-token.md)).
- **Perché no**: i limiti fissi e il registro devono stare nel nostro codice e non dipendere dal modello.

## Conseguenze

### Positive

- Circa 3,5 giorni di sviluppo in meno nella fase 1 ([ricerca/45 §9.3](../../ricerca/45-architettura-v3.md)).
- Da 3.560 a 5.940 € in meno fra le spese una tantum ([ricerca/45 §9.1](../../ricerca/45-architettura-v3.md)).
- Nessuna chiave fisica da cercare per approvare dal telefono.

### Negative

- Il codice del Cancello non ha una revisione esterna obbligatoria ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).
- Chi entra nella rete interna con il token di un processo può chiamare il Cancello: resta comunque dentro i limiti fissi, i livelli e i tetti.

### Rischi

- **Un bug nel Cancello**: prove a ogni modifica, idempotenza, esito «incerto» a una persona, Mattia sul codice; revisione esterna se un cliente la chiede ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).
- **Un cliente o una certificazione chiedono di più**: le difese tolte sono descritte nella revisione 2 dello spec e si possono rimettere.

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §1.2, §2.5-2.8, §6.1, §6.2, §9.1, §9.3, §10](../../ricerca/45-architettura-v3.md)
- [ricerca/43, giudizio essenziale](../../ricerca/43-giudizio-essenziale.md)
- [ricerca/41, novità al 9 novembre, §8.2](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/42, proposta A §4](../../ricerca/42-proposta-A-motore-a-livelli.md), [proposta B §4](../../ricerca/42-proposta-B-orchestratore-pronto.md), [proposta C §4](../../ricerca/42-proposta-C-ibrido-abbonamenti.md) e [proposta D §4](../../ricerca/42-proposta-D-automazione-prima.md)
- [ADR-0003](0003-cancello-approvazioni.md), rivista da questa ADR; [ADR-0004](0004-litellm-banca-token.md); [ADR-0009](0009-dati-tre-colori.md); [ADR-0018](0018-accesso-oracle-netbird-pangolin.md)
