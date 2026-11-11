# ADR-0022: Eventi e sveglia nel motore; n8n facoltativo, routine di Claude solo per uso personale

**Data**: 2026-11-10

**Stato**: accettata; rivista il 2026-11-11 da [ADR-0028](0028-instradamento-a-piu-motori.md): i compiti programmati servono anche la corsia T, avviati dal motore con il solo avvio API

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Se e come tenere n8n nel board lo decide Michele, a cui resta l'infrastruttura ([ADR-0011](0011-n8n-orari-integrazioni.md)).

## Contesto

- Gli agenti partono in due modi: **a orario** (il debrief delle 7:00, i bandi della mattina) e **su evento** (una trascrizione pronta, una mail arrivata, un modulo del sito). Chi li sveglia è la «sveglia» del sistema.
- Nella v2 la sveglia era n8n, il servizio di automazioni del board di Michele: lanciava i lavori a orario e riceveva i webhook, cioè le chiamate che un servizio fa quando succede qualcosa ([ADR-0011](0011-n8n-orari-integrazioni.md)).
- La sintesi del terzo giro teneva n8n «solo da avvio», per orari e webhook firmati verso `POST /eventi` ([ricerca/45 §1.2 e §3.1](../../ricerca/45-architettura-v3.md)).
- Le verifiche hanno trovato limiti concreti di n8n come sveglia: di serie lo Schedule Trigger non recupera gli orari persi mentre l'istanza è giù; un'esecuzione caduta per un crash viene marcata «crashed» e non riprende; n8n 3.0 cambia l'API ([ricerca/44, VER2 rilievo 3](../../ricerca/44-verifiche-avversarie.md); [ricerca/41 §5](../../ricerca/41-novita-al-9-novembre.md)).
- Sul banco di prova della fase 1 n8n entra solo se Michele lo ammette ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- Ci si è chiesti se la sveglia potessero farla le routine di Claude, cioè i compiti programmati nel cloud di Claude Code e di Claude Team ([ricerca/41 §1.4](../../ricerca/41-novita-al-9-novembre.md)).

## Decisione

**La sveglia sta nel motore, nel nostro codice** ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)).

- **Orari in una tabella del motore.** Ogni riga dice quale catena o sessione parte, a che ora e per chi; la tabella sta in git nella repo del codice. Il motore la legge ogni minuto e, per ogni orario dovuto, scrive un evento nel registro [proposta].
- **Orari persi.** Se il motore era fermo, alla ripartenza esegue una volta sola l'ultimo orario perso di ogni riga, come l'opzione «Run the Most Recent» di n8n. Un controllo alle 7:15 avvisa se il debrief non è partito [proposta, da [ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)].
- **Eventi su `POST /eventi`.** È l'unico ingresso del motore: lo chiamano la tabella degli orari, il lettore di Graph, la Porta e i servizi esterni che ci servono, come il modulo del sito e Instantly. Ogni mittente ha il suo token ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md); [ADR-0023](0023-protezioni-essenziali.md)).
- **Registro degli eventi** in PostgreSQL, con una chiave per evento (per esempio l'id della trascrizione) e lo stato «ricevuto / fatto / fallito». Lo stesso evento ricevuto due volte non fa partire due catene. Un compito fisso rimette in coda ciò che resta fermo e avvisa nel debrief ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- **Il delta di Graph lo legge il nostro codice.** Un lettore legge le trascrizioni di Teams ogni 5 minuti; il token delta avanza solo dopo che l'evento è registrato. Il testo rosso non passa da n8n: lo oscura e lo riassume il nostro servizio ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md); [ADR-0009](0009-dati-tre-colori.md)).
- **n8n diventa facoltativo.** Resta nel board di Michele per i collegamenti che servono; il sistema di agenti non ne dipende. Se un collegamento passa da n8n, n8n chiama `POST /eventi` e basta: non manda nulla a clienti o prospect, non tiene dati rossi nelle esecuzioni, gira con una versione 2.x fissata ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md); [ricerca/42, proposta D §4.4](../../ricerca/42-proposta-D-automazione-prima.md)).
- **Le routine di Claude restano per l'uso personale delle persone**: il riassunto della propria giornata, un promemoria, una ricerca che ciascuno lancia per sé. Nessun processo aziendale e nessun agente del sistema parte da una routine, perché le routine agiscono come la persona, partono al massimo una volta l'ora, sono in anteprima, dipendono dai limiti d'uso del posto e scavalcano il Cancello (i dettagli sono sotto, fra le alternative) ([ricerca/41 §1.4 e §8.2, punto 5](../../ricerca/41-novita-al-9-novembre.md)).

## Alternative considerate

### Alternativa: n8n come sveglia, cioè orari e webhook verso `POST /eventi`

- **Pro**: c'è già nel board ed è la scelta della sintesi del terzo giro ([ricerca/45 §1.2](../../ricerca/45-architettura-v3.md)).
- **Contro**: un servizio in più da cui dipende ogni lavoro; sul banco della fase 1 serve il sì di Michele; gli orari persi vanno impostati a mano; la versione 3.0 cambia l'API; le vulnerabilità del 2026 obbligano a patch rapide ([ricerca/44, VER2 rilievo 3](../../ricerca/44-verifiche-avversarie.md); [ricerca/41 §5](../../ricerca/41-novita-al-9-novembre.md); [ADR-0011](0011-n8n-orari-integrazioni.md)).
- **Perché no**: una tabella degli orari nel motore costa poco, sta in git e lascia ogni avvio nel registro degli eventi; n8n resta libero per i collegamenti del board.

### Alternativa: le routine di Claude come sveglia

- **Pro**: ci sono già nei piani Team, senza servizi da installare; partono a orario, da una chiamata API o da eventi GitHub ([ricerca/41 §1.4](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro** ([ricerca/41 §1.4 e §8.2](../../ricerca/41-novita-al-9-novembre.md); [ricerca/35, giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)):
  - appartengono al singolo account e agiscono «come te», cioè come la persona, non come l'agente;
  - partono al massimo una volta l'ora: il debrief alle 7:00 va, la lettura delle trascrizioni ogni 5 minuti no;
  - sono in anteprima;
  - consumano l'uso dell'abbonamento del posto, con i suoi limiti;
  - vogliono il login di claude.ai, non la chiave API, e il contenuto va comunque ad Anthropic;
  - includono di serie i connettori, scritture comprese: una scrittura scavalcherebbe il Cancello e il suo registro.
- **Perché no**: un processo aziendale non può dipendere dall'account e dai limiti di una persona, né passare fuori dal Cancello ([ADR-0011](0011-n8n-orari-integrazioni.md)).

### Alternativa: un timer di sistema sul server

- **Pro**: semplicissimo; la sintesi lo indicava come ripiego senza n8n ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- **Contro**: gli orari vivono fuori dal codice e fuori dal registro, e sulle macchine di sviluppo con Windows funziona in un altro modo.
- **Perché no**: il motore gira comunque sempre; la tabella dentro il motore fa lo stesso lavoro con le stesse prove su Windows e su Linux.

## Conseguenze

### Positive

- Un componente in meno da cui il sistema dipende; la fase 1 non aspetta n8n sul banco.
- Ogni avvio, a orario o su evento, lascia una riga nel registro: un crash a metà catena non perde la call e non manda due mail (criterio N9) ([ricerca/45 §6.3](../../ricerca/45-architettura-v3.md)).
- I dati rossi non entrano in n8n (criterio N10) ([ricerca/45 §6.3](../../ricerca/45-architettura-v3.md)).

### Negative

- La tabella degli orari e il recupero degli orari persi li scriviamo e manteniamo noi [stima: poche ore in più rispetto al registro degli eventi, che vale circa 1 giorno di sviluppo ([ricerca/45 §9.3](../../ricerca/45-architettura-v3.md))].
- I servizi esterni che mandano webhook vanno puntati su `POST /eventi`, che quindi va esposto dietro la porta d'ingresso del server.

### Rischi

- **Blackout di notte**: senza riaccensione automatica il debrief salta. La riaccensione dopo un blackout è il primo acquisto consigliato a Michele, a 0 € ([ricerca/45 §11](../../ricerca/45-architettura-v3.md)).
- **Un evento fermo** resta «ricevuto»: il compito fisso lo rimette in coda e lo segnala nel debrief ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).

## Revisione dell'11 novembre 2026

- La sveglia resta nel motore: orari e `POST /eventi` non cambiano, e nessun processo aziendale parte da un compito programmato a orario o da un evento di GitHub.
- Cambia la frase «Nessun processo aziendale e nessun agente del sistema parte da una routine». Per direttiva di Alberto il motore può avviare, sul posto della persona responsabile, un compito programmato di Claude Code con il solo avvio API: è la **corsia T**, per lo sviluppo di progetti in codice e i lavori lunghi di quattro agenti ([ADR-0028](0028-instradamento-a-piu-motori.md)).
- L'avvio lo decide il motore, dal suo registro, e passa dall'outbox del Cancello. Un'etichetta su una issue arriva come evento su `POST /eventi`, non come avvio da GitHub del compito ([ricerca/49 §1.2 e §3.5](../../ricerca/49-instradamento-a-piu-motori.md)).
- Le obiezioni scritte sopra restano vere; ADR-0028 dice come la corsia T le contiene: nessun connettore, consegna solo come pull request, conto per posto, ripiego sulla corsia S.

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §1.2, §3.1, §6.3, §9.3, §11](../../ricerca/45-architettura-v3.md)
- [ricerca/41, novità al 9 novembre, §1.4, §1.5, §5 e §8.2](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/44, verifiche avversarie, VER2](../../ricerca/44-verifiche-avversarie.md)
- [ricerca/42, proposta D §4.4](../../ricerca/42-proposta-D-automazione-prima.md)
- [ricerca/35, giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)
- [ADR-0009](0009-dati-tre-colori.md); [ADR-0011](0011-n8n-orari-integrazioni.md), rivista da questa ADR; [ADR-0028](0028-instradamento-a-piu-motori.md), che rivede questa ADR
- [ricerca/49, instradamento a più motori, §1.2, §3 e §3.5](../../ricerca/49-instradamento-a-piu-motori.md)
