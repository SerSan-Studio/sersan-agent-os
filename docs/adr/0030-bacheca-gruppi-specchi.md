# ADR-0030: La bacheca è del motore, i gruppi si vedono nella Sala, gli specchi verso le chat aspettano una chat vera

**Data**: 2026-11-12

**Stato**: accettata; rivede [ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md) in tre punti: i passaggi non sono più azioni del Cancello, i gruppi stanno nella Sala finché non c'è il bot di Teams o Buzz, Buzz si prova quando Michele lo ammette e c'è una macchina Linux. [ADR-0006](0006-teams-chat-di-gruppo.md) rimanda ad ADR-0026 per Buzz e per i gruppi degli agenti: per quella parte segue questa revisione

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Michele ammette Buzz, dà la macchina Linux con Docker su cui gira e prepara il tenant per il bot di Teams ([ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0006](0006-teams-chat-di-gruppo.md)). «Continua» oltre il tetto lo preme una persona, e il suo nome resta scritto.

## Contesto

- ADR-0026 vuole una bacheca nostra in PostgreSQL, nel motore: ogni passaggio è una riga che fa partire il lavoro di un altro agente attraverso il registro degli eventi. Dice anche che i passaggi sono «azioni interne a L3», che i gruppi stanno all'inizio in Teams e che Buzz si prova presto ([ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- Nelle sette milestone del PRD il bot di Teams è la prova della milestone 3. Fino ad allora si approva dalla Sala di controllo, la pagina web locale che si usa anche dal telefono, ma solo sulla rete dell'ufficio ([docs/06-sviluppo.md](../06-sviluppo.md)).
- Il freno della milestone 1 c'è già per gli eventi: oltre 8 passaggi, o più di due rimbalzi della stessa coppia di agenti, l'evento va a una persona con «Continua?» ([ricerca/45 §2.7](../../ricerca/45-architettura-v3.md)). Il tetto in dollari della catena invece ferma il lavoro e lascia l'evento «fallito», e nessuna azione della Sala lo riprende (lo spec della milestone 1 e `docs/attivita.md`, repo del codice).
- Il Cancello porta a L1 anche le azioni interne doppie, cioè uguali nei 7 giorni, e quelle con più di 8 passaggi; il suo segnale di incidente serio nasce solo da una «Rettifica» su un'uscita esterna (lo spec della milestone 1, repo del codice).
- Buzz al 9 novembre: nessuna versione desktop dopo la 0.5.28 del 9 ottobre; la modifica che collega le approvazioni è ferma; con Claude le risposte possono sparire senza errore; nel codice non c'è un freno ([ricerca/41 §7](../../ricerca/41-novita-al-9-novembre.md); [ricerca/26 §7.3](../../ricerca/26-claude-agent-sdk.md); [ricerca/17 §5](../../ricerca/17-buzz.md)).
- Il relay di Buzz gira solo su Linux, e le macchine di sviluppo sono Windows senza Docker ([ricerca/17 §4](../../ricerca/17-buzz.md); [ricerca/45 §6](../../ricerca/45-architettura-v3.md)).
- Le fonti su Buzz danno solo le vie possibili per collegarlo (riga di comando, client Nostr, webhook); un ponte nostro sulla riga di comando compare solo come ripiego ([ricerca/17 §5](../../ricerca/17-buzz.md); [ricerca/20, proposta B](../../ricerca/20-proposta-B-buzz.md)).
- Il testo che arriva da una chat è input non fidato ([ricerca/28 §8.2](../../ricerca/28-chat-di-gruppo-self-hosted.md)). Il decisore potrebbe dire a quale agente tocca un messaggio, ma le sue soglie sono ancora una prima stima ([ricerca/47, Parte 2, «Altri punti»](../../ricerca/47-modelli-system-one.md); [ADR-0027](0027-decisore.md)).
- Lo stand-up degli agenti, prima del debrief, è fra i pezzi che la milestone 1 lascia alla milestone 2 ([docs/05-design.md §5.3](../05-design.md); lo spec della milestone 1, repo del codice).

## Decisione

**La bacheca è del motore, e un passaggio non passa dal Cancello. I gruppi si vedono nella Sala. Gli specchi verso Buzz e Teams si scrivono nello spec della milestone 2 (repo del codice), ma non si costruiscono finché non c'è una chat vera.**

La bacheca:

- **Uno schema `bacheca` nel database, scritto solo dal motore**, con tre tabelle: compiti, passaggi e messaggi. Passaggi e messaggi sono a sola aggiunta.
- **Un passaggio è una riga più un evento, nella stessa transazione**: nascono tutti e due o nessuno. Chi riceve si legge dalla tabella d'instradamento nel momento del passaggio. Il passaggio «analisi → follow-up» della milestone 1 diventa una riga della bacheca, con lo stesso evento di oggi.
- **Il passaggio non è un'azione del Cancello.** Rispetto ad ADR-0026 si perdono due cose: abbassare la terna dei passaggi di un agente, e la voce del passaggio nel registro del Cancello. Le sostituiscono «Ferma» sul passaggio, il freno e lo stop; i passaggi restano nel registro dei lavori e nella linea del tempo. Ciò che esce verso l'esterno passa sempre dal Cancello, al livello della sua terna ([ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md)).
- **Il cliente viene dai dati**, dal CRM del primo partecipante esterno, mai dal testo di un agente. Senza cliente, la riga va solo nel gruppo della squadra e in «Agenti». Una sessione S che passa lavoro sceglie solo l'agente, fra quelli ammessi per il suo profilo, e il testo: compito e cliente sono quelli della sessione ([ADR-0029](0029-corsia-s-sessioni-a-giri.md)).
- **Il freno tiene i numeri di oggi**: 8 passaggi, la stessa coppia al massimo due volte, il conteggio che riparte dall'ultimo messaggio di una persona.
- **Il tetto in dollari della catena porta l'evento a una persona con «Continua?».** «Continua» aggiunge alla catena radice una concessione, con chi e quando: il tetto vale tetto × (1 + concessioni), e tutti i lavori della stessa radice fermati per il tetto tornano in coda insieme.
- **«Riprova» per gli eventi falliti**, dalla Sala. Chiude un debito della milestone 1.
- **Lo stand-up è una catena N a orario, senza modello**, prima del debrief: per ogni agente scrive nel gruppo «Agenti» che cosa ha chiuso e che cosa aspetta, letto dalla bacheca e dal registro.

I gruppi:

- **Tre tipi**: per squadra, per cliente (interno), «Agenti». Non serve una tabella dei gruppi: la chiave del gruppo sta sulle righe.
- **Si vedono nella Sala finché non c'è il bot di Teams o Buzz**, in una vista nuova con una parte nuova nel flusso in diretta. La vista mostra anche gli esiti del Cancello per le proposte del compito, letti dalla linea del tempo. Accanto c'è la vista «Sessioni»: stato, giri, azioni e spesa delle sessioni S.
- **Una persona interviene su un compito o su un passaggio con tre azioni**: «Ferma», «Correggi» con un testo, «Rilancia». Il suo messaggio è un evento con i passaggi a zero. Un «Correggi» su un compito con più sessioni non chiuse fa nascere un evento per ogni sessione, così «Continua», «Scarta» o «Chiudi» su una sessione non toccano le altre (scelta del 13 novembre, nello spec).
- **Lo smistamento a testo libero dei messaggi delle persone non c'è. È un limite dichiarato della milestone 2.**

Che cosa aspetta:

- **Specchi verso Buzz, poi Teams: nessun codice finché non c'è una chat vera.** Il gruppo di lavoro si apre con il sì di Michele e una macchina Linux con Docker. Lo spec scrive già i prerequisiti:
  - un ruolo di token `specchio`, ammesso solo alle rotte di decisione del Cancello, a quelle della bacheca e alla rotta dell'incidente;
  - un colore massimo per ogni specchio (Buzz: verde);
  - il legame fra l'identità nella chat e una persona;
  - un agente tecnico «specchio», con una catena N sua che porta l'identificativo della riga, così un messaggio non vale mai come doppione;
  - il contratto dell'adattatore sulla riga di comando di Buzz, con un finto nella batteria;
  - un misuratore contato dalle due parti, che distingue i messaggi in attesa da quelli persi;
  - la rotta del Cancello per l'incidente «dati nel gruppo sbagliato».
- Prima di aprire il gruppo si rileggono le fonti su Buzz. **Soglie della prova dal vivo V5**: 200 messaggi in 5 giorni lavorativi, 0 persi, 0 doppi; una carta decisa da Buzz arriva al Cancello con l'identità giusta. «Buzz collegato e misurato», nella riga della milestone 2 del PRD, si chiude con V5, con priorità «importante».
- **La lettura del web resta fuori dalla milestone 2.** Lo spec scrive la milestone, il servizio che serve e chi lo installa. La forma è già scelta: una catena N «lettore» senza strumenti d'azione, che passa alla sessione solo campi a schema, con un passaggio della bacheca ([ADR-0029](0029-corsia-s-sessioni-a-giri.md)).

## Alternative considerate

### Alternativa: il passaggio come azione interna L3 del Cancello, come in ADR-0026

- **Pro**: la terna dei passaggi si può abbassare agente per agente; ogni passaggio ha la sua voce nel registro del Cancello ([ADR-0020](0020-autonomia-a-livelli.md)).
- **Contro**: una chiamata al Cancello per ogni passaggio, e la riga del passaggio in un posto diverso dall'azione, perché il Cancello non legge lo schema del motore. Un messaggio corto ripetuto, come «Fatto», varrebbe come doppione e diventerebbe una carta; il limite di 8 passaggi scatterebbe due volte.
- **Perché no**: pesa sull'autonomia senza proteggere un effetto esterno. Il passaggio resta nel motore, dove c'è già il freno.

### Alternativa: i gruppi subito in Teams

- **Pro**: è la casa scritta in ADR-0026 e ADR-0006: una chat vera sul telefono, con l'identità certa di chi scrive ([ADR-0006](0006-teams-chat-di-gruppo.md)).
- **Contro**: il bot di Teams è la prova della milestone 3, e servono registrazione e permessi del tenant, che sono di Michele ([docs/06-sviluppo.md](../06-sviluppo.md)).
- **Perché no**: la bacheca non dipende dalla chat; Teams arriva come specchio quando il bot c'è.

### Alternativa: costruire adesso lo specchio, contro un finto

- **Pro**: il codice sarebbe pronto il giorno del sì di Michele, e V5 sarebbe solo una verifica.
- **Contro**: l'interfaccia si disegnerebbe alla cieca, perché le fonti non descrivono un ponte verso Buzz ([ricerca/17 §5](../../ricerca/17-buzz.md)); i persi si contano dalle due parti, e l'altra parte non c'è; sarebbe codice da mantenere per mesi senza uso.
- **Perché no**: lo spec scrive contratto, prerequisiti e soglie; il codice segue spec, piano e prove quando si apre il gruppo.

### Alternativa: Buzz come casa degli agenti da subito

- **Pro**: è il modello dell'idea: agenti membri veri, con nome e proprietario ([ricerca/17](../../ricerca/17-buzz.md)).
- **Contro**: approvazioni non collegate, risposte che spariscono con Claude, nessun freno, permessi degli strumenti approvati in automatico, relay solo su Linux ([ricerca/17 §4, §5 e §8](../../ricerca/17-buzz.md); [ricerca/41 §7](../../ricerca/41-novita-al-9-novembre.md)).
- **Perché no**: l'aveva già scartata ADR-0026, e al 9 novembre i fatti non sono cambiati.

### Alternativa: lo smistamento a testo libero dei messaggi delle persone

- **Pro**: è ciò che ADR-0026 promette, «come in qualsiasi chat»; il decisore sveglierebbe un solo agente, e nel dubbio nessuno ([ricerca/47, Parte 2, «Altri punti»](../../ricerca/47-modelli-system-one.md)).
- **Contro**: il testo della chat è input non fidato e chiede un ingresso con identità certa; il quesito non è tarato ([ricerca/28 §8.2](../../ricerca/28-chat-di-gruppo-self-hosted.md); [ADR-0027](0027-decisore.md)).
- **Perché no**: i tre tasti coprono il correggere, fermare e rilanciare di ADR-0026. Il testo libero resta fuori, come limite dichiarato di questa milestone.

## Conseguenze

### Positive

- Riga ed evento nascono insieme: nessun passaggio senza lavoro, nessun lavoro senza riga.
- Il tetto della catena fa ciò che ADR-0026 prometteva, e un evento fallito si riprende.
- I gruppi si vedono dalla milestone 2 senza aspettare Michele, Teams o Buzz.
- Nessun codice di specchio da mantenere senza una chat che lo usi.

### Negative

- Il registro del Cancello non vede i passaggi, e la loro terna non si abbassa per agente.
- La Sala non è una chat: dal telefono funziona solo sulla rete dell'ufficio, e una persona non scrive testo libero.
- «Buzz collegato e misurato» probabilmente non si chiude nella milestone 2: dipende dal sì di Michele e da una macchina Linux con Docker.

### Rischi

- **Catene che girano in tondo**: il freno, il tetto e «Continua?» le fermano.
- **Un «Continua» dato alla leggera**: ogni concessione vale un solo tetto in più e porta il nome di chi l'ha data.
- **Dati di un cliente nel gruppo sbagliato**: il cliente viene dai dati, e la sessione non sceglie né compito né cliente ([ADR-0029](0029-corsia-s-sessioni-a-giri.md)). Nella milestone 2 le viste della Sala non si filtrano per persona, quindi un errore non mostra dati a nessuno di nuovo. La rotta che lo segnala come incidente serio entra con gli specchi ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)).
- **Testo di terzi dentro un passaggio**: il testo di un passaggio scritto da un modello porta il marchio «derivato da terzi», e una sessione che l'ha letto fa uscire verso l'esterno solo con una carta ([ADR-0029](0029-corsia-s-sessioni-a-giri.md)).
- **V5 misura il nostro specchio, non le risposte degli agenti dentro Buzz**: superarla non basta a fare di Buzz la casa degli agenti nel senso di ADR-0026 ([ricerca/26 §7.3](../../ricerca/26-claude-agent-sdk.md)).

## Fonti

- Lo spec della milestone 2 (repo del codice): bacheca, gruppi, rimandati, prove dal vivo e decisioni che cambiano
- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §2.4 e §2.7](../../ricerca/45-architettura-v3.md)
- [ricerca/17, Buzz, §4, §5 e §8](../../ricerca/17-buzz.md); [ricerca/20, proposta B](../../ricerca/20-proposta-B-buzz.md)
- [ricerca/26, Agent SDK, §7.3](../../ricerca/26-claude-agent-sdk.md); [ricerca/41, novità al 9 novembre, §7](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/28, chat di gruppo, §8.2](../../ricerca/28-chat-di-gruppo-self-hosted.md); [ricerca/47, Parte 2](../../ricerca/47-modelli-system-one.md)
- [docs/05-design.md §5.3](../05-design.md); [docs/06-sviluppo.md](../06-sviluppo.md)
- [ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md), rivista da questa ADR; [ADR-0006](0006-teams-chat-di-gruppo.md)
- [ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md); [ADR-0027](0027-decisore.md); [ADR-0029](0029-corsia-s-sessioni-a-giri.md)
