# ADR-0027: Il «decisore»: domande tipizzate e soglie in un file, e un dubbio rende il sistema più prudente

**Data**: 2026-11-10

**Stato**: accettata; i motori dietro l'interfaccia si scelgono con la prova della milestone 2

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Se un fornitore esterno di decisioni può ricevere i dati gialli lo decide Michele ([ricerca/47 §5.3](../../ricerca/47-modelli-system-one.md)).

## Contesto

- Prima e dopo il lavoro degli agenti il sistema prende molte decisioni piccole: a chi tocca un evento, se un testo prende un impegno, che cosa ha risposto un esterno, di che colore è un dato ([ricerca/47, Parte 2](../../ricerca/47-modelli-system-one.md)).
- Nell'architettura v3 queste decisioni erano passi a schema dentro le catene: il controllo del contenuto prima di un'uscita L2 o L3 e la lettura delle risposte degli esterni ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)). Le soglie stavano nei testi delle istruzioni e nessuna risposta portava una probabilità.
- Il 10 novembre Alberto ha chiesto di valutare i modelli «System One», come Jev e OpenJev, messi a monte dei modelli pesanti. Un System One non scrive testo: riceve uno stato e domande tipizzate (sì o no, scelta, punteggio) e restituisce una probabilità per ogni opzione ([ricerca/47 §1.1](../../ricerca/47-modelli-system-one.md)).
- Jev è proprietario, è uscito il 15 settembre 2026, non ha SLA e non dichiara le lingue che regge. Il produttore scrive che un testo ostile nello stato può spostare le risposte e che il modello preferisce la prima opzione dell'elenco ([ricerca/47 §1.2](../../ricerca/47-modelli-system-one.md)).
- OpenJev è un server aperto che parla la stessa API. Il suo modello principale chiede una GPU da almeno 24 GB; i modelli piccoli che serve girano su CPU. Nessuno misura l'italiano ([ricerca/47 §1.3 e §1.4](../../ricerca/47-modelli-system-one.md)).
- Per SerSan il guadagno non è il risparmio, che vale poche decine di dollari al mese [stima]. Il guadagno è avere probabilità e soglie scritte in un file, per far scendere i livelli, smistare gli eventi e capire il colore dei dati ([ricerca/47, «In breve» e §3.3](../../ricerca/47-modelli-system-one.md)).

## Decisione

- **Un'interfaccia unica nel nostro codice, il «decisore».** Riceve uno stato e domande tipizzate. Per ogni domanda restituisce la risposta e una probabilità fra 0 e 1 ([ricerca/47, «Il decisore: un'interfaccia unica»](../../ricerca/47-modelli-system-one.md)).
- **Le soglie stanno in `config/decisore.yaml`**, in git come `config/livelli.yaml`, per uso e per domanda. Una risposta sotto la soglia vale «dubbio». Nella milestone 1 le domande sono scritte nel codice; ricerca/47 propone di portare nel file anche quelle, e si decide con la prova della milestone 2.
- **Una risposta del decisore può solo rendere il sistema più prudente**: scendere di livello, mandare una carta a una persona, colorare di rosso, passare a una corsia più capace. Il decisore non sceglie mai un destinatario esterno e non alza mai un livello ([ricerca/47, Parte 2](../../ricerca/47-modelli-system-one.md)).
- **Un dubbio non abbassa la terna.** L'azione va in carta per quella volta. La terna scende solo per i segnali di [ADR-0020](0020-autonomia-a-livelli.md).
- **Un errore vale un dubbio.** Un timeout, un errore del fornitore, una risposta non valida o un tetto di spesa raggiunto danno «dubbio» su tutte le domande, con il motivo nel registro.
- **Il colore si controlla prima di chiamare un motore.** Se il colore non è noto vale rosso, e un testo rosso non va a un motore esterno. Il decisore del colore gira in casa; se in casa non c'è, restano le regole in codice e il rosso per default ([ricerca/47, Parte 2, punto d](../../ricerca/47-modelli-system-one.md); [ADR-0009](0009-dati-tre-colori.md)).
- **Dove si usa**:
  1. lo smistamento degli eventi a testo libero fra una regola, una catena della corsia N, una sessione della corsia S e una persona;
  2. il controllo del contenuto prima di un'uscita L2 o L3: cifre e date le trova il codice, al decisore restano le domande di significato;
  3. la lettura delle risposte degli esterni, con una domanda a parte: «chiede di non essere più contattato?»;
  4. il colore dei dati.
- **I motori dietro l'interfaccia si cambiano senza toccare catene e Cancello**: un decisore a copione per le prove, le regole in codice come primo filtro, Claude Haiku a schema, un System One, cioè Jev o un modello sul nostro server. Tutte le chiamate passano da LiteLLM, con la versione sempre fissata ([ADR-0004](0004-litellm-banca-token.md); [ADR-0025](0025-un-modello-per-agente.md)).
- **Ogni chiamata si registra**: uso, domande, risposte prima della soglia, probabilità, soglie applicate e spesa. Dalla milestone 2 si aggiunge la correzione della persona, quando arriva. Il registro serve a tarare le soglie e a misurare ogni mese la calibrazione, cioè se fra le risposte date con probabilità 0,8 circa l'80% è giusto.
- **Milestone 1**: l'interfaccia, il decisore a copione, il decisore su un modello a schema, le soglie in configurazione, lo smistamento e il controllo del contenuto che lo usano. Senza hardware nuovo.
- **Milestone 2**: la prova in italiano su circa 850 casi verdi fra Haiku 5.5, Jev fissato via LiteLLM, un modello piccolo su CPU e, se c'è la GPU, un modello da 4-9 miliardi di parametri. Poi due settimane di prova ombra, in cui il decisore risponde accanto alla catena senza avere effetto ([ricerca/47, Parte 4 e §5.2](../../ricerca/47-modelli-system-one.md)).
- **Un motore entra per un quesito** solo se, sulla metà dei casi messa da parte ([ricerca/47 §4.4](../../ricerca/47-modelli-system-one.md)):
  - trova almeno il 98% dei casi delle classi critiche («non scrivetemi», impegni, rosso), cioè non sbaglia nessuno dei 150 casi veri di ogni classe;
  - manda a una strada più economica al massimo il 2% dei casi difficili;
  - non sta sotto Haiku 5.5 di più di 2 punti di accuratezza;
  - ha un errore di calibrazione (ECE) di 0,10 al massimo;
  - decide da solo almeno il 70% dei casi, con un errore reale del 2% al massimo;
  - risponde entro 500 ms via API ed entro 200 ms in casa, 95 volte su 100.

## Alternative considerate

### Alternativa: Jev chiamato direttamente, come smistatore unico a monte

- **Pro**: risponde in 70-500 ms dichiarati e costa 0,042 $ per milione di token in ingresso, con l'uscita gratuita ([ricerca/47 §1.1 e «In breve»](../../ricerca/47-modelli-system-one.md)).
- **Contro**: è proprietario e giovane, senza SLA; non dichiara l'italiano; riceverebbe anche testi di cui non si conosce ancora il colore; un testo ostile può spostare le sue risposte ([ricerca/47 §1.2](../../ricerca/47-modelli-system-one.md)).
- **Perché no**: entra solo come uno dei motori dietro l'interfaccia, sui dati verdi, e sui gialli se Michele ammette il fornitore; e solo dopo la prova.

### Alternativa: nessun decisore, ogni catena tiene il suo passo a schema

- **Pro**: niente da costruire; è il disegno di [ricerca/45 §2.4](../../ricerca/45-architettura-v3.md).
- **Contro**: soglie sparse nelle istruzioni, nessuna probabilità, nessun registro con cui tararle.
- **Perché no**: la spesa di modello è la stessa, ma senza misura non si può dire quando un livello può salire.

### Alternativa: solo regole in codice

- **Pro**: gratuite, prevedibili, sempre in casa.
- **Contro**: trovano cifre, IBAN, rimbalzi e «fuori ufficio», ma non il significato di una frase come «non vorrei più ricevere i vostri messaggi» ([ricerca/47 §4.1](../../ricerca/47-modelli-system-one.md)).
- **Perché no**: restano come primo filtro e come ripiego. Il sistema deve funzionare anche con le sole regole, con più carte per le persone.

### Alternativa: un modello grande o multimodale che smista tutto

- **Pro**: un solo punto che vede testo, immagini e audio.
- **Contro**: un modello che vede tutto e decide è più esposto alle istruzioni nascoste nei documenti; in casa non sta nelle schede che abbiamo ([ricerca/48 §3.1](../../ricerca/48-modelli-locali-e-gpu.md)).
- **Perché no**: lo smistamento lo fa il codice sui metadati, e l'unico smistatore libero resta il Capo di gabinetto su Claude ([ricerca/48 §3.2](../../ricerca/48-modelli-locali-e-gpu.md)).

## Conseguenze

### Positive

- Le soglie si leggono e si cambiano in un file, con la storia in git.
- Ogni decisione lascia una riga con la sua probabilità: si può misurare quanto sbaglia e dove.
- Cambiare motore non tocca le catene né il Cancello.

### Negative

- È lavoro in più nella milestone 1, che la stima di [ricerca/45 §12.1](../../ricerca/45-architettura-v3.md) non prevedeva.
- Prima di alcune uscite c'è una chiamata in più a un modello.
- Con Claude la probabilità è quella che il modello dichiara, poco affidabile finché non è tarata sui nostri casi ([ricerca/13 §2.3](../../ricerca/13-modelli-open-source-sul-server.md)). Per questo le soglie partono alte, fra 0,7 e 0,9, e sono una prima stima.

### Rischi

- **Un caso difficile trattato come facile**: le soglie sono asimmetriche; con la fiducia bassa si sale di gradino e non si scende mai; nel debrief resta il tasto «sbagliato» ([ricerca/47 §5.4](../../ricerca/47-modelli-system-one.md)).
- **Una mail scritta per ingannare il decisore**: il decisore non alza mai un livello e non sceglie destinatari; la prova ha 20 casi ostili ([ricerca/47 §4.1](../../ricerca/47-modelli-system-one.md)).
- **Un prodotto giovane cambia le risposte fra una versione e l'altra**: la versione è sempre fissata; cambiarla è un cambio di modello, e senza una valutazione le terne che dipendono da quel quesito tornano a L1 ([ricerca/47 §5.4](../../ricerca/47-modelli-system-one.md); [ADR-0020](0020-autonomia-a-livelli.md)).
- **Il fornitore è fermo o cambia prezzo**: ogni quesito ha almeno due motori; il ripiego sono le regole e una carta a una persona.
- **L'italiano non è dichiarato da nessun fornitore**: la prova è tutta in italiano, e un motore entra solo se supera le soglie scritte sopra.

## Fonti

- [ricerca/47, modelli System One a monte degli agenti: Parte 1 (i fatti), Parte 2 (dove entra e l'interfaccia), Parte 4 (piano di prova), Parte 5 (raccomandazione e rischi)](../../ricerca/47-modelli-system-one.md)
- [ricerca/48, modelli locali, multimodalità e GPU, §3](../../ricerca/48-modelli-locali-e-gpu.md)
- [ricerca/45, architettura v3, §2.4 e §12.1](../../ricerca/45-architettura-v3.md)
- [ricerca/13, modelli open source sul server, §2.3](../../ricerca/13-modelli-open-source-sul-server.md)
- [ADR-0004](0004-litellm-banca-token.md); [ADR-0009](0009-dati-tre-colori.md); [ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md); [ADR-0025](0025-un-modello-per-agente.md)
