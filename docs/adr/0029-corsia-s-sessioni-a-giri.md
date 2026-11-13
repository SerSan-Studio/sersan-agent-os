# ADR-0029: Corsia S: una sessione è una fila di giri, e il ponte verso il Cancello è uno strumento con regole fisse

**Data**: 2026-11-12

**Stato**: accettata dal gruppo di progetto; le scelte che poggiano sulla prova con il modello a copione si ricontrollano nella prova dal vivo V1, quando c'è la chiave API

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Michele, a cui resta l'infrastruttura, conferma per quanti giorni si tengono i file delle sessioni e dove gira il runner sul server ([ADR-0021](0021-motore-a-due-corsie.md)). Mattia, o l'integrazione continua quando torna, fa girare la prova su Linux appena c'è una macchina: non ferma l'unione del codice, ed è obbligatoria prima di ogni uso sul server (scelta del 13 novembre; lo spec della milestone 2, repo del codice).

## Contesto

- La corsia S serve le figure che usano più strumenti: un solo runner, al massimo 6 sessioni, costruito nella milestone 2 del PRD. In un giro, un pacchetto di scritture interne e un solo elemento esterno. Il ponte era un gancio che chiede al Cancello prima di ogni strumento ([ADR-0001](0001-motore-agent-sdk.md); [ADR-0021](0021-motore-a-due-corsie.md); [ricerca/45 §3.1 e §6.1](../../ricerca/45-architettura-v3.md)).
- Le fonti non dicevano che cos'è un giro, né da dove la sessione prende destinatari e fonti. Una regola c'era già: chi legge testo di terzi non propone nella stessa sessione ([ricerca/36 §5.1, punto 5](../../ricerca/36-architettura-v2.md); [ricerca/35, giudizio di sicurezza §8, punto 8](../../ricerca/35-giudizio-sicurezza.md)).
- Il 12 novembre l'SDK 0.3.322 è stato guidato contro un modello a copione, senza chiave e senza traffico verso servizi veri ([ricerca/50 §2 e §3](../../ricerca/50-agent-sdk-e-prova-a-copione.md)):
  - senza strumenti di serie la sessione non fa nulla da sé; su Windows Node rimette dieci variabili vere dell'utente, se non le impostiamo noi (E3, E10, E15);
  - per aspettare una persona funziona lo schema «in attesa»; il rinvio `defer` alla ripresa no (E7);
  - un giro biforcato lascia la base intatta, e dopo un crash il diario fa uscire l'effetto una volta sola. Senza biforcare, l'SDK inventa un risultato e una risposta (E11, E12, E13);
  - nessun freno ferma uno strumento già chiesto dal modello, salvo un gancio che nega; senza `onFailure: "block"` un gancio rotto lascia passare tutto (E16, E17);
  - la spesa passo per passo è giusta solo con gli eventi a flusso; `interrupt()` ferma in pochi millisecondi, `close()` lascia il processo vivo 7 secondi (E6, E16, E18);
  - il pacchetto pesa 386 MB, di cui 331 MB di eseguibile per sistema ([ricerca/50 §1.2 e §2](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- Quattro critici hanno letto la prima stesura del disegno, per sicurezza, fattibilità, perimetro e coerenza (documento di lavoro del 12 novembre, non pubblicato). Hanno trovato che:
  - «letto da uno strumento» non vuol dire «dato»: un indirizzo che una trascrizione ostile fa finire in un riassunto passerebbe, e lo scenario S9 della milestone 1 non reggerebbe in S;
  - il ponte vede la classe di una proposta solo nella risposta del Cancello: da solo non può fermare il secondo elemento esterno;
  - il diario per solo numero d'ordine regge con il copione, non con un modello vero che al giro rifatto chiede altro;
  - un giro che eredita dall'evento i ritentativi, la catena radice e l'origine rompe l'ordine dei giri, il tetto della sessione e il freno;
  - nei messaggi dell'SDK i token d'uscita sono un segnaposto ([ricerca/50 §3.2, «Spesa e tetti»](../../ricerca/50-agent-sdk-e-prova-a-copione.md));
  - la prova intera dentro la batteria aggiungerebbe circa 11 minuti e risultati che dipendono dai tempi.

## Decisione

- **Una sessione è una fila di giri, e ogni giro è un lavoro del motore.** La sessione è il lavoro di un agente S su una cosa sola. Il giro è un avvio dell'SDK, da un messaggio al risultato; fra un giro e l'altro il processo è chiuso. Ogni azione ha un numero d'ordine nel giro, e la chiave di una proposta è lavoro più numero d'ordine: lo spec della milestone 1 diceva «lavoro e giro» senza definire il giro, ed è una differenza dichiarata. Un giro parte sempre da un evento: un evento che la tabella manda a una sessione, un passaggio della bacheca ([ADR-0030](0030-bacheca-gruppi-specchi.md)), l'esito che la sessione aspetta, il messaggio di una persona.
- **La sessione ha una macchina a stati sua**: aperta, in attesa, chiusa, fallita, fermata. I giri di una sessione partono in ordine di nascita, uno alla volta. **Un giro non usa i ritentativi automatici degli eventi**: fallimento, stop, tetto, giri massimi e giro rifatto diverso portano l'evento a una persona, e la sessione riparte solo con «Continua». Catena radice e origine sono della sessione, con il tetto del profilo; solo il messaggio di una persona o «Continua» azzera il conto dei passaggi. Ogni profilo ha i suoi freni: passi per giro, giri per sessione, tetto del giro e della sessione.
- **Il runner è un compito dentro il motore**: 2 giri insieme di partenza, 6 al massimo. La chiusura ordinata aspetta i giri; una morte brusca chiude subito i processi figli e spegne il ponte, così dopo la morte nessuna chiamata arriva al Cancello.
- **La scatola è chiusa.** Nessuno strumento di serie, solo quelli del profilo, nessuna impostazione della macchina, un gancio che blocca anche quando si rompe. L'ambiente del processo figlio lo impostiamo tutto noi, con un elenco per Windows e uno per Linux. Cartella e configurazione sono per sessione, non per agente ([ricerca/50 §10, punto 10](../../ricerca/50-agent-sdk-e-prova-a-copione.md)): così le sessioni di clienti diversi non stanno nella stessa cartella. A ogni giro entrano le istruzioni dell'agente, le regole «Come lavoro» della persona e le regole fisse della corsia. **Il login di Claude di chi usa la macchina non entra mai**: è un criterio d'accettazione, con una prova che guarda l'ambiente del figlio.
- **Il ponte è lo strumento che propone, dentro il processo del runner, e il gancio nega soltanto.** Il Cancello decide dentro lo strumento, con la stessa rotta della corsia N. Una carta chiude il giro, e il suo esito fa partire il giro dopo. Il gancio è la seconda barriera. Cambia [ADR-0001](0001-motore-agent-sdk.md).
- **Le regole fisse del ponte** stanno nel nostro codice, e ognuna ha uno scenario che prova a romperla:
  - *i destinatari vengono dai dati, per riferimento.* Il modello indica un riferimento; il ponte lo traduce dai campi strutturati (partecipanti, contatto, persone). Un indirizzo che sta solo in un testo libero non vale mai. Anche la classe attesa e le fonti (cifre e date) le mette il ponte, dai dati;
  - *il testo che deriva da terzi obbliga a una carta.* È marcato quando viene da una trascrizione, da una mail o da un passaggio scritto da un modello; dal 13 novembre anche il titolo di un incontro e i nomi dei partecipanti esterni, che possono venire da un invito esterno. Se la sessione l'ha letto, le sue proposte esterne escono solo con una carta. Un evento con testo di terzi non va mai diretto a una sessione: il motore non parte se la tabella d'instradamento ce lo manda. Arriva a una sessione solo come campi estratti da una catena N, con un passaggio della bacheca;
  - *un solo elemento esterno per giro, con due barriere.* Il ponte rifiuta la seconda proposta «forse esterna» senza chiamare il Cancello. Il Cancello, con un limite fisso valido per ogni chiamante, fa nascere negata la seconda proposta esterna dello stesso giro. Dopo un esterno, una carta o una finestra, nessun altro effetto: il giro chiude. Una sola azione con effetto per risposta del modello;
  - *un effetto una volta sola, con il diario.* La riga si scrive prima dell'effetto. Un giro rifatto uguale riceve il risultato salvato; rifatto diverso, nessun effetto nuovo: la sessione si ferma e una persona vede che cosa era già uscito. Un giro morto si rifà da solo solo se non ha azioni esterne, al massimo due volte. Che cosa è uscito lo dicono il diario e il Cancello, non la conversazione salvata;
  - *i campi che il modello non scrive.* Colore (il più alto letto dalla sessione), persona, catena radice, passaggi, cliente e compito vengono dalla sessione. Per passare lavoro il modello sceglie solo l'agente, fra quelli ammessi, e il testo;
  - *le letture del solo cliente.* Gli strumenti leggono solo i dati del cliente del compito; una proposta verso un altro cliente è rifiutata;
  - *lo stop.* Ogni strumento con effetto lo legge prima di agire. Il runner lo controlla ogni 2 secondi, chiude il giro con `interrupt()` e poi i processi. Il lavoro resta fermo anche dopo lo sblocco.
- **Ogni giro biforca dal precedente**, e la base non si tocca. Un giro morto si rifà dalla stessa base, con il diario. Basi vecchie e rami morti si cancellano alla chiusura della sessione; il resto lo cancella un comando, a motore spento, lanciato da una persona o dal sistema operativo e mai da un agente, dopo un numero di giorni in configurazione (30, da confermare con Michele).
- **La spesa è a prenotazione.** Prima del giro il motore controlla i tetti e prenota il tetto del giro; il controllo somma spese e prenotazioni anche per la corsia N, ed è un cambio dichiarato. Durante il giro conta i token dagli eventi a flusso: oltre il tetto, strumento e gancio rifiutano ogni effetto e il giro si interrompe. `maxBudgetUsd` e `maxTurns` restano come rete. A fine giro la spesa vera prende il posto della prenotazione; un giro chiuso male lascia la prenotazione, o il conto del runner se è più alto.
- **La prova dell'SDK con il copione è un comando a parte** (`npm run prova-sdk`), con gli esperimenti da E1 a E24 e il suo rapporto, **da rifare a ogni versione** e, su Windows, prima di unire il codice delle sessioni. Su Linux si fa appena c'è una macchina, e sempre prima di ogni uso sul server. Nella batteria restano dieci scenari S brevi, da S11 a S20, e la batteria non cresce oltre il doppio di oggi.
- **La versione dell'SDK è fissata**, oggi la 0.3.322, ed entra nell'impronta dell'agente S. Una versione nuova entra quando passano la prova e i dieci scenari, e chi la unisce scrive la valutazione; senza valutazione le terne esterne tornano a L1 ([ADR-0020](0020-autonomia-a-livelli.md)). Fino alla milestone 3 del PRD le sessioni chiamano l'API direttamente, senza LiteLLM ([ADR-0004](0004-litellm-banca-token.md)).
- Il primo agente S è l'Agente brief: prima da un evento diretto, poi dalla bacheca e dall'agenda. Nella milestone 2 il ponte ha dieci strumenti: nove li usa lui, e `passa_lavoro` serve a passare lavoro sulla bacheca a un'altra sessione S; altri strumenti arrivano con l'agente che li chiede.

## Alternative considerate

### Alternativa: il ponte come gancio che chiede al Cancello prima di ogni strumento, come in ADR-0001

- **Pro**: un solo punto di controllo per tutti gli strumenti; è il disegno già scritto ([ADR-0001](0001-motore-agent-sdk.md); [ricerca/36 §5.1](../../ricerca/36-architettura-v2.md)).
- **Contro**: il gancio decide fuori dallo strumento. Per una carta dovrebbe rinviare lo strumento con `defer`, che alla ripresa è instabile; lo schema che regge è lo strumento che risponde «in carta», e poi il giro finisce ([ricerca/50 §3.2 e §9.1, E7 ed E7d](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **Perché no**: la garanzia resta la stessa, nessun effetto senza il Cancello. Lo chiama lo strumento; il gancio nega soltanto.

### Alternativa: un lavoro unico per sessione, con uno stato «in attesa»

- **Pro**: una riga per sessione; nessun legame da tenere fra giri ed eventi.
- **Contro**: un lavoro resterebbe aperto per ore o giorni, mentre aspetta una carta. Gli stati dei lavori della milestone 1 non hanno l'attesa, e la ripresa rimette in coda i lavori rimasti aperti. Una chiave stabile per ogni azione vuole un lavoro per giro.
- **Perché no**: il giro come lavoro riusa coda, ripresa, registro e tetti di oggi; l'attesa sta nella sessione.

### Alternativa: il runner in un processo a parte

- **Pro**: un guasto dell'SDK non tocca il motore; il runner potrebbe andare su un'altra macchina.
- **Contro**: un processo in più, con il suo token, la sua ripresa e il legame con il motore che [ADR-0021](0021-motore-a-due-corsie.md) ha tolto (possesso, battito e riserve fra runner). Il processo pesante, `claude.exe`, è già un figlio separato ([ricerca/50 §1.3](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **Perché no**: un compito dentro il motore usa la chiusura ordinata, lo stop e la ripresa che ci sono già.

### Alternativa: riprendere la sessione interrotta senza biforcare

- **Pro**: un file solo per sessione; lo spazio non cresce con il quadrato dei giri.
- **Contro**: dopo un crash l'SDK chiude da sé la chiamata rimasta aperta con «esito sconosciuto» e aggiunge una risposta inventata. La scelta di rifare l'effetto passa al modello, che non vede il diario ([ricerca/50 §3.2 e §6, punto 5](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **Perché no**: con la base intatta il giro si rifà da capo, con il diario (E11, E12).

### Alternativa: il diario per solo numero d'ordine

- **Pro**: semplice; con il copione basta (E12).
- **Contro**: un modello vero, al giro rifatto, può chiamare un altro strumento al posto n o cambiare gli argomenti. Riceverebbe l'esito di un'azione che non ha chiesto, e quella chiesta non partirebbe ([ricerca/50 §3.2](../../ricerca/50-agent-sdk-e-prova-a-copione.md)). Nella milestone 1, poi, la stessa chiave con un contenuto diverso è un errore.
- **Perché no**: il diario confronta strumento e argomenti; se cambiano, nessun effetto e una persona.

### Alternativa: gli indirizzi scritti dal modello, con un controllo «letto da uno strumento»

- **Pro**: il modello può scrivere a chiunque abbia incontrato nel compito; il ponte resta più semplice.
- **Contro**: riassunti, note del CRM e passaggi sono testo libero, scritto da un modello che ha letto testo di terzi. Un indirizzo messo lì da una trascrizione ostile passerebbe il controllo, e per il Cancello un contatto che ci ha scritto da poco può non dare una carta.
- **Perché no**: nella corsia N i destinatari vengono dai dati, ed è la difesa che regge ([ADR-0021](0021-motore-a-due-corsie.md)); i riferimenti la portano nella corsia S.

### Alternativa: la fila della spesa della corsia N intorno a tutto il giro

- **Pro**: nessuna prenotazione e nessun cambio alla corsia N; il tetto si controlla come oggi.
- **Contro**: la fila mette in ordine le spese dello stesso agente nel mese e della stessa catena radice. Tenuta per tutto il giro, terrebbe occupata una connessione al database per minuti e farebbe aspettare le altre sessioni dello stesso agente. E dentro il giro le chiamate al modello le fa `claude.exe`, non il nostro codice: la fila non le vedrebbe.
- **Perché no**: prenotazione prima, conto dagli eventi a flusso durante, spesa vera alla fine; la corsia N tiene la sua fila.

## Conseguenze

### Positive

- La corsia S ha le garanzie della N dove contano: destinatari e fonti dai dati, un effetto una volta sola, il Cancello che decide ([ADR-0021](0021-motore-a-due-corsie.md)).
- Ogni scelta poggia su un esperimento ripetibile, che si rilancia a ogni versione.
- Un crash non rifà un effetto e non perde un giro; uno stop non lascia processi accesi.

### Negative

- **Una sessione che ha letto testo derivato non manda mai verso l'esterno senza una persona**, anche quando la terna è a L3. Per gli agenti che leggono incontri, riassunti e passaggi ogni uscita esterna è una carta. Per gli incontri è una scelta prudente del 13 novembre: Alberto e Mattia la rivedono dopo V1, contando le carte nate solo per questo.
- Circa 390 MB di pacchetto, con un eseguibile per sistema, su ogni macchina e in ogni integrazione continua. Chi installa senza le dipendenze facoltative resta senza corsia S ([ricerca/50 §1.2](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- **Le prove senza chiave non dicono come sceglie il modello vero**: quali argomenti, quanti giri, che cosa chiede al giro rifatto, con quale spesa. Lo dice solo la prova dal vivo V1 ([ricerca/50 §8](../../ricerca/50-agent-sdk-e-prova-a-copione.md)).
- Il controllo dei tetti della corsia N cambia, e le sue prove si rifanno.
- Lo spazio su disco cresce con il quadrato dei giri, finché la sessione non chiude.

### Rischi

- **L'SDK cambia ogni pochi giorni** ([ricerca/50 §1.1](../../ricerca/50-agent-sdk-e-prova-a-copione.md)): versione fissata; la prova e i dieci scenari prima di ogni cambio.
- **La biforcazione non regge i blocchi di ragionamento firmati del modello vero** ([ricerca/50 §8](../../ricerca/50-agent-sdk-e-prova-a-copione.md)): si guarda in V1. Se non regge, tutto il peso va sul diario, e i giri rifatti diversi vanno a una persona.
- **Impostazioni gestite dal server** arrivano con una chiave d'organizzazione anche senza le impostazioni della macchina ([ricerca/50 §1.5](../../ricerca/50-agent-sdk-e-prova-a-copione.md)): si guarda in V1 se accendono strumenti o ganci.
- **Un testo ostile spinge il modello verso un indirizzo o un altro cliente**: riferimenti dai dati, letture del solo cliente, carta per il testo derivato.

## Fonti

- [ricerca/50, l'Agent SDK al 12 novembre e la prova a copione: In breve, §1, §2, §3 (E1-E18), §5, §6, §7, §8, §9.1 e §10](../../ricerca/50-agent-sdk-e-prova-a-copione.md)
- [ricerca/45, architettura v3, «Decisione del gruppo di progetto», §3.1 e §6.1](../../ricerca/45-architettura-v3.md)
- [ricerca/36, architettura v2, §5.1](../../ricerca/36-architettura-v2.md)
- [ricerca/35, giudizio di sicurezza, §8](../../ricerca/35-giudizio-sicurezza.md)
- [ADR-0001](0001-motore-agent-sdk.md), rivista da questa ADR; [ADR-0004](0004-litellm-banca-token.md); [ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md); [ADR-0030](0030-bacheca-gruppi-specchi.md)
- Senza collegamento: lo spec della milestone 1 e lo spec della milestone 2 (repo del codice); la prima stesura del disegno e le sue critiche (documento di lavoro del 12 novembre, non pubblicato)
