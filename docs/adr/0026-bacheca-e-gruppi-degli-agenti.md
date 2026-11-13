# ADR-0026: Bacheca e gruppi di chat degli agenti, anticipati; Buzz provato presto

**Data**: 2026-11-10

**Stato**: accettata; rivista il 2026-11-12 da [ADR-0030](0030-bacheca-gruppi-specchi.md): i passaggi non sono azioni del Cancello, i gruppi stanno nella Sala finché non c'è Teams o Buzz, Buzz si prova quando Michele lo ammette e c'è una macchina Linux

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Michele ammette Buzz sul banco di prova e decide dove gira ([ADR-0006](0006-teams-chat-di-gruppo.md)).

## Contesto

- Nella trascrizione di riferimento gli agenti hanno una chat comune in cui si parlano: il messaggio di un agente fa partire il lavoro di un altro, senza che una persona lo smisti ([ricerca/38, AU-07 e §4](../../ricerca/38-autonomia-nella-trascrizione.md)).
- Nella v2 i passaggi fra agenti stavano nel motore, con un freno, e un solo canale «Agenti» di Teams li rispecchiava. Bacheca e canale arrivavano all'inizio della fase 2, per circa 5,5 giorni di sviluppo ([ADR-0006](0006-teams-chat-di-gruppo.md); [ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- Buzz, la chat open source per persone e agenti, era previsto sul banco solo dalla fase 4, per circa 6 giorni di sviluppo. Esce dal banco quando non perde più risposte e le sue approvazioni funzionano ([ADR-0006](0006-teams-chat-di-gruppo.md); [ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- Al 9 novembre Buzz non ha nuove versioni desktop dopo la 0.5.28 del 9 ottobre; la modifica che sospende e riprende le approvazioni nei workflow è aperta e ferma; il repository è attivo ([ricerca/41 §7](../../ricerca/41-novita-al-9-novembre.md)).
- Hermes ha funzioni utili per un gruppo di agenti: stanze che si smistano da sole, `max_hops`, cron nelle stanze, skill bloccabili, politica per i turni persi ([ricerca/41 §8.2, punto 8](../../ricerca/41-novita-al-9-novembre.md)).

## Decisione

**Una bacheca nostra, dove gli agenti si passano il lavoro, e gruppi di chat dove quel lavoro si vede e si discute** ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)).

- **La bacheca** sta in PostgreSQL, nel motore. Ogni passaggio è una riga: chi passa, a chi, che cosa, per quale catena. Un agente che scrive sulla bacheca fa partire il lavoro di un altro attraverso il registro degli eventi ([ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- **I gruppi di chat** mostrano la bacheca e accolgono le persone [proposta per la divisione]:
  - un gruppo per squadra, con gli agenti della squadra e le persone che la seguono;
  - un gruppo per cliente, interno, dove gli agenti che lavorano su quel cliente si passano il lavoro. Non è il canale condiviso con il cliente: lì scrive solo il Cancello ([ADR-0006](0006-teams-chat-di-gruppo.md));
  - un gruppo comune, «Agenti», dove si vedono tutti i passaggi e lo stand-up degli agenti ([ricerca/45 §1.3](../../ricerca/45-architettura-v3.md)).
- **Una persona può scrivere in un gruppo** per correggere, fermare o rilanciare un passaggio. Il suo messaggio azzera il conteggio dei passaggi.
- **Il freno** ([ricerca/45 §2.7](../../ricerca/45-architettura-v3.md)):
  - 8 passaggi per le catene dichiarate;
  - la stessa coppia di agenti non si rimbalza il lavoro più di due volte;
  - il conteggio parte dall'ultimo messaggio umano, come `max_hops` di Hermes;
  - un tetto in dollari per catena;
  - oltre il tetto arriva una carta «Continua?».
- **I passaggi fra agenti sono azioni interne a L3**; ciò che esce verso l'esterno passa dal Cancello al livello della sua terna ([ADR-0020](0020-autonomia-a-livelli.md)).
- **Quando**: subito dopo la milestone 1, insieme alla corsia S ([ADR-0021](0021-motore-a-due-corsie.md)). Fino ad allora i passaggi del pilota (per esempio dall'Analista chiamate al Post-call) stanno nel registro degli eventi ([ricerca/45 §4.1](../../ricerca/45-architettura-v3.md)).
- **Dove stanno i gruppi all'inizio**: in Teams, con la Porta e i nove bot di squadra ([ADR-0006](0006-teams-chat-di-gruppo.md); [ricerca/45 §6.4](../../ricerca/45-architettura-v3.md)).
- **Buzz si collega alla stessa bacheca e si prova presto**, non nella fase 4: sul banco di prova, con dati verdi, appena la bacheca c'è.
  - Se regge, cioè non perde risposte e ha le approvazioni collegate, diventa la casa degli agenti e i gruppi passano lì.
  - Se non regge, i gruppi restano in Teams e Buzz resta in prova.
- **Teams resta per le persone** e per le approvazioni dal telefono, con l'identità certa di chi preme ([ADR-0006](0006-teams-chat-di-gruppo.md)).

## Alternative considerate

### Alternativa: il solo canale «Agenti» di Teams, come nella v2

- **Pro**: è già nel disegno, con la Porta e l'identità di Entra ([ADR-0006](0006-teams-chat-di-gruppo.md)).
- **Contro**: un solo canale per tutti i passaggi diventa illeggibile con decine di agenti; arrivava all'inizio della fase 2 e Buzz solo nella fase 4 ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- **Perché no**: la chat fra agenti è uno dei principi della trascrizione di riferimento; con i gruppi per squadra e per cliente il lavoro si segue dove serve ([ricerca/38 §4](../../ricerca/38-autonomia-nella-trascrizione.md)).

### Alternativa: Buzz come casa degli agenti da subito

- **Pro**: è il modello dell'idea: agenti membri veri, con nome e proprietario ([ricerca/17](../../ricerca/17-buzz.md); [ADR-0006](0006-teams-chat-di-gruppo.md)).
- **Contro**: le approvazioni non sono collegate, con Claude le risposte possono sparire senza errore, e non ci sono nuove versioni da un mese ([ricerca/41 §7 e §8.2, punto 10](../../ricerca/41-novita-al-9-novembre.md); [ADR-0006](0006-teams-chat-di-gruppo.md)).
- **Perché no**: la bacheca è nostra e non dipende dalla chat; Buzz si prova presto sulla stessa bacheca e diventa la casa solo se supera i criteri.

### Alternativa: le stanze di gruppo di Hermes

- **Pro**: stanze che si smistano da sole, `max_hops`, cron nelle stanze ([ricerca/41 §8.2, punto 8](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: Hermes non soddisfa le quattro condizioni di [ADR-0012](0012-hermes-uscita.md) ([ricerca/41 §3.4](../../ricerca/41-novita-al-9-novembre.md)).
- **Perché no**: ne copiamo le idee nella nostra bacheca, non il prodotto ([ricerca/45 §1.3](../../ricerca/45-architettura-v3.md)).

## Conseguenze

### Positive

- Il lavoro fra agenti si vede subito dopo la milestone 1, nel gruppo della squadra o del cliente giusto.
- La bacheca non dipende dalla chat: Teams, Buzz o un canale futuro sono adattatori ([ADR-0006](0006-teams-chat-di-gruppo.md)).
- Una persona interviene in un gruppo come in qualsiasi chat.

### Negative

- Bacheca, gruppi e freno li scriviamo noi: circa 5,5 giorni di sviluppo per bacheca e canale, più circa 6 per Buzz, spostati prima nel piano ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)). La stima va rifatta con Mattia ([ricerca/45 §9.3](../../ricerca/45-architettura-v3.md)).
- Due chat da seguire finché Buzz è in prova.

### Rischi

- **Catene che girano in tondo**: il freno e la carta «Continua?» le fermano ([ricerca/45 §2.7](../../ricerca/45-architettura-v3.md)).
- **Buzz perde risposte**: resta in prova e i gruppi restano in Teams ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).
- **Dati di un cliente nel gruppo sbagliato**: ogni gruppo per cliente vede solo i passaggi di quel cliente; un errore così è un incidente serio e riporta a L1 tutte le classi esterne dell'agente ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)).

## Revisione del 12 novembre 2026

- **I passaggi fra agenti non sono azioni del Cancello.** Il punto «I passaggi fra agenti sono azioni interne a L3» non vale più. Un passaggio è una riga della bacheca più un evento, scritti insieme dal motore; chi riceve si legge dalla tabella d'instradamento al momento del passaggio. I passaggi si vedono nel registro dei lavori e nella linea del tempo ([ADR-0030](0030-bacheca-gruppi-specchi.md)).
- **Che cosa si perde, e che cosa lo sostituisce.** Non si può più abbassare la terna dei passaggi di un agente ([ADR-0020](0020-autonomia-a-livelli.md)), e il passaggio non ha più una voce nel registro del Cancello. Al loro posto ci sono «Ferma» sul passaggio, il freno e lo stop. Ciò che esce verso l'esterno passa ancora dal Cancello al livello della sua terna ([ADR-0021](0021-motore-a-due-corsie.md), nota del 12 novembre 2026).
- **I gruppi stanno nella Sala finché non c'è il bot di Teams o Buzz.** Il punto «Dove stanno i gruppi all'inizio: in Teams» non vale più. I tre tipi di gruppo restano: per squadra, per cliente, «Agenti». Nella Sala ogni persona vede tutti i gruppi: i gruppi letti solo da chi li segue arrivano con gli specchi. La vista dei gruppi mostra anche gli esiti del Cancello per le proposte del compito. Una persona scrive su un compito o su un passaggio con «Ferma», «Correggi» o «Rilancia»; nella milestone 2 non c'è lo smistamento dei messaggi a testo libero ([ADR-0030](0030-bacheca-gruppi-specchi.md)).
- **Buzz si prova quando Michele lo ammette e c'è una macchina Linux con Docker**, e non più appena c'è la bacheca. La prova chiede 200 messaggi in 5 giorni lavorativi, nessuno perso e nessuno doppio, e una carta decisa da Buzz che arriva al Cancello con l'identità giusta. Su Buzz vanno solo dati verdi. Lo spec della milestone 2 (repo del codice) scrive già i prerequisiti, senza codice ([ADR-0030](0030-bacheca-gruppi-specchi.md)).
- Il rischio «Dati di un cliente nel gruppo sbagliato» resta. La strada per dichiararlo come incidente al Cancello arriva con i gruppi rispecchiati in Buzz o in Teams.

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §1.3, §2.4, §2.7, §3.1, §4.1, §6.4, §9.3, §10](../../ricerca/45-architettura-v3.md)
- [ricerca/38, autonomia nella trascrizione, AU-07 e §4](../../ricerca/38-autonomia-nella-trascrizione.md)
- [ricerca/41, novità al 9 novembre, §3.4, §7 e §8.2](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/17, Buzz](../../ricerca/17-buzz.md)
- [ADR-0006](0006-teams-chat-di-gruppo.md), rivista da questa ADR per la parte su Buzz; [ADR-0012](0012-hermes-uscita.md); [ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md)
