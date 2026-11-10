# Verifiche avversarie del terzo giro

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Tre scettici hanno provato a confutare la proposta prima in classifica, P-D. Negli altri documenti del giro sono citati come **VER1**, **VER2** e **VER3**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

## VER1 · tempi e livelli: l'autonomia promessa contro quella reale

**Verdetto:** regge con correzioni.

### VER1, rilievo 1

**Tesi:** Le fasi 0-1 di P-D stanno nelle 8 settimane anche con la riserva: 17,5 + 20 = 37,5 gp di base, circa 50 con la riserva, su una capacità di circa 52 (P-D §6.3; giudici CEO e CPTO).

**Esito:** non dimostrata.

**Prove:** P-D non scompone i 20 gp della fase 1 (P-D.md: unica riga «niente motore SDK; Cancello a livelli; Jira e calendario»). Ricostruzione dalla tabella dei pezzi della v2.1 [verificato: R36 §7.3]. La fase 1 vale 22,5 gp. Togliendo il motore sul banco (5,5) restano circa 17 gp: Cancello parte 1 6, Outlook 1,5, Porta v1 3,5, trascrizioni da Graph 2,5, oscuramento locale 1,5, contenuto dei 3 agenti 2. P-D aggiunge nella stessa fase:
- finestra L2, 3-5 gg [non verificato: stima di R2 §3, punto 3];
- classi a livelli, 2-4 gg [non verificato: stima di R2 punto 1];
- esecutore Jira 1,75 [verificato: R36 §7.3];
- esecutore calendario, che nella v2.1 sta dentro i 9,75 gp della parte 2 del Cancello [verificato: R36 §7.3];
- installazione e flussi di n8n sul banco, contatori delle promozioni, annullo, lista di soppressione, base della bacheca e specchio nel canale «Agenti» (la bacheca completa vale 5,5 gp [verificato: R36 §7.3]).
Tolta anche la sicurezza «in eccesso» (P-A la stima −3,5 gp), la fase 1 arriva a circa 23-27 gp. Le fasi 0-1 diventano circa 41-45 gp di base e 54-60 con la riserva, contro 52 di capacità (6,5 gp × 8 settimane [verificato: R36 §7.1, «da confermare»; PRD «Domande aperte»]). Il giudice essenziale aveva già scritto «ottimisti di 2-3 gp». Il calcolo è mio [non verificato].

**Correzione:** Chiedere a P-D la tabella dei pezzi della fase 1 come quella di R36 §7.3, rifatta con Mattia. Spostare Jira, calendario e bacheca base all'inizio della fase 2, oppure dichiarare la settimana 9-10 come data realistica. Lo stesso difetto vale, ancora più forte, per P-A: 42,5-44 gp di base.

### VER1, rilievo 2

**Tesi:** Alla settimana 8 il follow-up ai partecipanti della call può già essere L2 (P-D §1 riga 5; §5.1).

**Esito:** falsa.

**Prove:** Le condizioni le pone P-D stessa: ogni flusso nuovo parte «in ombra» per una settimana o 10 casi; poi servono 10 carte di fila approvate senza modifiche in 30 giorni; poi il via del parere (§3.2-3.3, §5.1). La fase 1 copre le settimane 5-8 [verificato: P §11]. I volumi al 5/10 erano 11 lead, 1 risposta e 0 meeting [verificato: P §7.1]. Il PRD dà per «alta» la probabilità di poche call [verificato: PRD «Rischi»]. Le call interne non producono follow-up verso clienti. Il flusso vero, con Teams e Graph veri, nelle milestone del PRD arriva solo con le milestone 3-5 [verificato: PRD, «Milestone di consegna»], cioè a ridosso della settimana 8. In più la registrazione automatica probabilmente non parte se entra solo il cliente [verificato: R30 §3.6]. A conti fatti, 10 sì puliti dopo l'ombra non stanno in 4 settimane.

**Correzione:** Scrivere che alla settimana 8 il follow-up è L1, e solo L1. La partenza diretta a L2 della classe «persona appena incontrata» deve diventare una decisione esplicita del gruppo di progetto dopo il parere (ora la può prendere, per l'aggiornamento del 10/11), invece di un contatore che non si riempie. Vale anche per P-A: 5 sì in 4 settimane sono comunque improbabili.

### VER1, rilievo 3

**Tesi:** Alla settimana 8 sono L3 riassunto, registro dei meeting, to-do in Jira, debrief ed evento del debrief in calendario (P-D §5.1). Per i giudici è il quadro più concreto.

**Esito:** non dimostrata.

**Prove:** - Riassunto e registro: plausibili, ma dipendono da cose ancora aperte. Il bot Teams senza Azure e l'identità sulle carte sono una prova della milestone 2 [verificato: PRD «Domande aperte»]. Le trascrizioni integrali sono dati rossi [verificato: P §5.6 tabella; D03]. Sul banco si salvano solo verde e giallo [verificato: P §11]. Il rosso va all'API solo oscurato in locale finché il parere non decide [verificato: PRD «Domande aperte»].
- To-do in Jira: nella v2.1 «Jira aperto agli agenti» è fuori dal perimetro delle fasi 0-1 [verificato: PRD «Fuori»]. Il piano Jira di SerSan non è noto [verificato: R36 §1, «Cosa resta da sapere»].
- Evento in calendario: richiede un esecutore di scrittura su Graph, che nella v2.1 sta nella parte 2 del Cancello [verificato: R36 §7.3]. L'MCP prevede posta e calendario solo in lettura [verificato: R36 §4.1].
- La milestone 1 di P-D esclude Teams e Graph veri (P-D §7.1).
Quindi le tre scritture L3 in più rispetto alla v2.1 dipendono da lavoro non contato (vedi il primo rilievo).

**Correzione:** Dividere la promessa della settimana 8 in due:
- certo: riassunto L3 nel canale interno e debrief L3;
- condizionato: to-do in Jira ed evento in calendario a L3, se la fase 1 ha margine.
Il criterio di verifica va legato ai pezzi realmente contati.

### VER1, rilievo 4

**Tesi:** «A regime P-D raggiunge il livello della trascrizione in tutto ciò che la trascrizione mostra, tranne offerte, contatti a freddo e pagamenti» (P-D §1, riga 5).

**Esito:** falsa.

**Prove:** Lo smentisce il §3.5 della stessa P-D, che elenca altri punti sotto la trascrizione:
- primo follow-up dopo una prima call fermo a L2;
- aperture di Andrea a L2, mentre nella trascrizione l'agente le cambia da solo [verificato: TR 15:31-15:44];
- report al responsabile solo con il parere;
- profili dei founder a L1.
In più: newsletter L1 a regime (§3.4, flusso 5) e modifiche a istruzioni e skill a L2 solo dalla fase 4. Gli agenti che imparano e si parlano da soli nella trascrizione [verificato: TR 3:53-4:30] in P-D diventano eventi fra flussi. Lo avevano già notato i giudici visione e CPTO.

**Correzione:** Riscrivere la riga 5 con l'elenco vero dei punti sotto la trascrizione. Alzare i tetti dove è solo prudenza: primo follow-up a L3 dopo il parere, newsletter a L2 con 3 numeri approvati come in P-A, skill interne con valutazione dalle fasi 2-3.

### VER1, rilievo 5

**Tesi:** Alla settimana 21 sono L3 i follow-up ai clienti con un progetto attivo e almeno tre classi sono a L2 o L3 (P-D §5.2, §5.5).

**Esito:** non dimostrata.

**Prove:** La scala di P-D chiede, per arrivare a L3: ombra, poi 10 sì di fila senza modifiche sostanziali (destinatario, oggetto o più del 10% del testo) in 30 giorni, poi 20 invii di fila senza «Ferma» né rettifiche. Sono almeno 30 follow-up puliti consecutivi sulla stessa classe (P-D §3.3). Un solo «Ferma» con motivo errore fa scendere la classe. Con i volumi del 5/10 [verificato: P §7.1] 30 follow-up in 13 settimane richiedono più di 2 call con clienti a settimana, tutte pulite. Il calcolo è mio [non verificato]. Le classi che salgono davvero entro la settimana 21 sono quelle interne, che partono già da L3.

**Correzione:** Adottare le soglie 5 e 15 di P-A e contare per classe di destinatari, non per singolo flusso. Togliere l'ombra per i flussi solo interni. Fissare per decisione, dopo il parere, il livello di partenza delle classi a basso rischio. Il criterio «tre classi a L2 o L3» va riscritto escludendo quelle nate L3.

### VER1, rilievo 6

**Tesi:** Il modello scrive solo il testo, mentre destinatari e azioni li sceglie il codice: per questo un'azione prevedibile può partire da sola con meno controlli (P-D §3.1).

**Esito:** non dimostrata.

**Prove:** Il disegno protegge chi riceve, non che cosa riceve. Che la chiamata a schema senza strumenti sia il disegno più robusto contro le iniezioni è verificato [R35-sic §3.2; R36 §5.2]. Ma un follow-up L3 scritto dal modello può contenere un prezzo, una data o un impegno tecnico, e gli impegni sono una classe con tetto L1 [verificato: P §9.3; P-D §3.2]. P-D non prevede nessun controllo del contenuto prima di un'uscita L2 o L3. La retrocessione scatta dopo l'invio (§3.3). Lo stesso limite vale per P-A, che però ha un elemento esterno per giro e un riepilogo con il tasto «sbagliato».

**Correzione:** Prima di ogni uscita L2 o L3, aggiungere al passo AI un controllo a schema economico: niente cifre, prezzi o date d'impegno fuori dai dati del CRM. Se il controllo trova qualcosa, l'azione scende a L1. Costa poco e serve a P-D come a P-A.

### VER1, rilievo 7

**Tesi:** Con le regole su EXECUTIONS_DATA_SAVE_* e «niente rosso attraverso un Wait», su n8n non resta nessun dato rosso, e la verifica può controllarlo (P-D §4.4).

**Esito:** non dimostrata.

**Prove:** Le variabili e la pulizia dopo 336 ore le ha lette su docs.n8n.io l'autore di P-D il 9/11 e il giudice CPTO con Context7 il 10/11; io non le ho rilette. Senza salvataggio delle esecuzioni, però, un post-call fallito non si può indagare, e questo indebolisce la protezione «correggere un errore» (lo nota anche il giudice essenziale). Se la trascrizione VTT scaricata da Graph venga trattata come dato binario, e dove n8n la scriva, non è coperto da nessun file letto [non verificato]. La regola del banco resta «nessun dato rosso salvato» [verificato: P §11; PRD «Metriche»].

**Correzione:** Nei flussi n8n la trascrizione intera non deve entrare. Un piccolo servizio TypeScript la scarica, la oscura e la riassume, e passa a n8n solo campi gialli. Era già la richiesta del CPTO sulla logica fuori da n8n, e rende vera anche la regola di ADR-0011 «la logica non dipende da n8n» [verificato: ADR-0011, Decisione]. Il registro degli errori del flusso conserva solo i campi gialli.

### VER1, rilievo 8

**Tesi:** Il totale di circa 230 gp (contro 249,25) e la fase 2 di circa 56 gp, con runner, renderer, Postiz, brief e offerte anticipati, sono credibili (P-D §6.3).

**Esito:** non dimostrata.

**Prove:** Nella v2.1 il contenuto degli agenti vale 67 gp, e trasformare una figura in un flusso non lo riduce [verificato: R36 §2.4 e §7.6; obiezione del giudice CPTO]. P-D anticipa nella fase 2 lavori che nella v2.1 stanno altrove:
- brief e proposte, dentro i 22 gp per 18 agenti della fase 3;
- Postiz con listmonk, 4,5 gp della fase 4;
- la parte serena di runner e renderer.
Toglie solo il motore (8) e FIDO2 e regole «Sempre» (circa 3) [verificato per i pezzi della v2.1: R36 §7.3]. Il saldo è mio [non verificato] e porta la fase 2 sopra i 58,5 gp, non sotto. P-D stessa chiede di rifare la stima con Mattia.

**Correzione:** Non presentare il risparmio di 19 gp come argomento: va contato come uguale alla v2.1 finché non c'è una stima pezzo per pezzo. Il vantaggio reale di P-D è nell'ordine dei lavori, non nel totale.

### VER1, rilievo 9

**Tesi:** Quali flussi restano davvero a L1 o L0 nelle date promesse.

**Esito:** vera.

**Prove:** Elenco realistico [non verificato: lettura mia delle condizioni di P-D, dei volumi in P §7.1 e del perimetro del PRD]:
- Settimana 8:
  - L1: follow-up ai clienti, e ogni altra uscita;
  - L0: CRM (lo dice P-D) e post (regola della sessione presidiata [verificato: P §8.2]);
  - condizionati: to-do in Jira ed evento in calendario.
- Settimana 21:
  - verso l'esterno quasi tutto a L1: primo follow-up, recap e deck ai clienti, inviti alla seconda call, risposte standard;
  - L2 possibile solo se il gruppo di progetto fissa per decisione la partenza a L2 dopo il parere;
  - post della pagina aziendale: L1 se Michele non ammette Postiz prima della F4 [verificato: P §6.2];
  - Andrea: assente.
- A regime: L1 per decisione su newsletter, founder, offerte e freddo; L0 sui commenti dei founder.
Le classi che contano per la trascrizione arrivano a L3 solo se i volumi crescono.

**Correzione:** Nel documento per il gruppo di progetto mettere una tabella a tre colonne: livello promesso, livello probabile con i volumi di oggi, decisione che sblocca la differenza. Lo stesso va fatto per P-A.

### VER1, rilievo 10

**Tesi:** Un difetto comune a P-D e P-A: l'autonomia verso l'esterno dipende da due prove ancora aperte, non dal motore.

**Esito:** vera.

**Prove:** Il bot Teams senza Azure, con l'identità di chi preme, è la prova della milestone 2 [verificato: PRD «Domande aperte»; R28 §2.3, aadObjectId da confermare]. Il «Ferma» delle finestre L2 e lo stop dal telefono passano tutti dalla Porta (P-D §2.2, §4.1). Il piano B, la pagina del Cancello, va scritto [verificato: R36 §7.3, Porta v1 con piano B]. Il nodo Teams di n8n non registra chi risponde [verificato: ADR-0011, «Negative»]. Il parere (entro la settimana 3 [verificato: PRD]) decide se il Post-call può leggere le trascrizioni e se possono partire invii veri.

**Correzione:** Fare subito la prova della Porta e del parere, prima di scrivere finestre e promozioni. Se la Porta fallisce, le finestre L2 si appoggiano alla pagina del Cancello con l'accesso Entra. Tenere pronto anche il piano «nessuna L2 esterna», in cui tutto il valore della settimana 8 resta interno.

## VER2 · conformità e affidabilità essenziali

**Verdetto:** regge con correzioni.

### VER2, rilievo 1

**Tesi:** «Destinatario noto» (un indirizzo o un dominio con call registrata o mail nei due sensi negli ultimi 90 giorni) è una classe che può salire lecitamente a L3 per follow-up, recap, inviti alla seconda call, promemoria e solleciti (P-D §3.2, flusso 1: «solo ai partecipanti della call e al loro dominio»).

**Esito:** falsa.

**Prove:** Il Garante applica l'art. 130 c.2 (consenso) anche agli indirizzi aziendali di persone; il soft spam (c.4) vale solo per i propri clienti [verificato: ricerca/16-gdpr-ai-act-e-regole.md, tabella UK/Italia, riga 119]. R16 esenta dal «freddo» solo la mail post-call al cliente con cui si è parlato, e la segna come proposta [verificato: ricerca/16 riga 125]. Se il criterio è il dominio, un collega del partecipante che non ha mai parlato con noi diventa «noto», e la mail che riceve è marketing senza consenso. Lo stesso vale per un prospect che ha risposto una volta a una campagna fredda: rispondere non vuol dire acconsentire al marketing [non verificato: lettura mia della linea del Garante]. Il difetto vale in parte anche per P-A, che mette nella classe «chi ci ha scritto negli ultimi 30 giorni» [testo di P-A §3.1].

**Correzione:** La classe vale solo per l'indirizzo esatto di chi era nella call registrata e avvisata, o di chi ci ha scritto per primo. Il dominio da solo non basta mai. Chi è entrato nel giro da una campagna fredda resta L1 finché non è cliente o non ha dato il consenso. Il parere della settimana 3 decide se e fin dove la classe sale oltre L1.

### VER2, rilievo 2

**Tesi:** Il primo follow-up dopo una call e le mail L2/L3 sono conformi all'AI Act art. 50 grazie alla riga che dichiara l'AI, mentre le mail L1 escono a nome di chi approva.

**Esito:** vera.

**Prove:** L'art. 50(1) e (5) è in vigore dal 2/8/2026: l'informazione va data al più tardi alla prima interazione [verificato: ricerca/16 righe 18 e 93]. La regola 1 della v2.1 fa uscire a nome della persona ciò che la persona approva [verificato: PRESENTAZIONE-CEO §9.1]. Il testo della riga è ancora da fissare: P-D lo mette fra le domande del parere (§4.2).

**Correzione:** Nessuna sul principio. Il testo della riga si fissa con il parere, e un test automatico ne controlla la presenza (criterio 7 di P-D §7.4). Vale uguale per P-A.

### VER2, rilievo 3

**Tesi:** «Un flusso avviato da un evento parte sempre» e il lavoro autonomo non si perde: ritentativi di n8n, chiavi d'idempotenza, esito «incerta» (P-D §4.1 punto 5; giudizio CPTO).

**Esito:** non dimostrata.

**Prove:** La documentazione di n8n dice che un'esecuzione interrotta da un crash, un riavvio o un OOM viene marcata «crashed». Il recupero all'avvio (startup-recovery) la segnala, ma non la riprende [verificato: docs n8n, trace-executions-with-opentelemetry, letta con Context7 il 10/11/2026]. «Retry On Fail» ritenta un nodo dentro la stessa esecuzione, non un'esecuzione caduta. In più P-D spegne il salvataggio delle esecuzioni proprio per i flussi con testo rosso (§4.4), cioè post-call e posta: quando falliscono non resta niente da rilanciare né da esaminare [non verificato: deduzione mia; che il riavvio a mano usi i dati salvati non l'ho riletto]. Se il lettore delta di Graph avanza il suo token prima che il flusso finisca, la trascrizione salta in silenzio [non verificato: dipende da come si scrive il flusso]. Il server dopo un blackout va riacceso a mano [verificato: PRESENTAZIONE-CEO §13; DOMANDE n. 22]. Il difetto vale anche per P-A, che però tiene una coda in PostgreSQL con ripresa (SPEC §4.2) e un criterio di ripresa (C14).

**Correzione:** Una tabella «eventi» in PostgreSQL, fuori da n8n, con stato «ricevuto / fatto / fallito» e chiave per evento (per esempio l'id della trascrizione). Il token delta avanza solo dopo che l'evento è registrato lì. Un compito fisso rimette in coda gli eventi rimasti «ricevuto» da più di N minuti e avvisa nel debrief chi è caduto due volte. Il riavvio parte dall'evento, non dall'esecuzione di n8n, quindi il testo rosso resta fuori dallo storico. Si aggiunge un criterio: «un crash a metà del post-call non perde la call».

### VER2, rilievo 4

**Tesi:** Il debrief alle 7:00 arriva ogni giorno lavorativo a L3 (P-D §3.4 flusso 2; verifica della settimana 8, §5.5).

**Esito:** non dimostrata.

**Prove:** Di serie lo Schedule Trigger di n8n non esegue le esecuzioni perse quando l'istanza era giù («Don't Run Missed Executions»). Il recupero c'è solo se lo si imposta, con lo scheduler durevole: predefinito dalla 2.45.0, opzioni dalla 2.36 [verificato: docs n8n, nodo Schedule Trigger, Context7 10/11/2026]. P-D fissa la 2.46.7, quindi l'opzione c'è, ma non la imposta. Senza riaccensione automatica, un blackout notturno salta il debrief senza che nessuno lo sappia.

**Correzione:** Su ogni orario «If Execution Is Missed = Run the Most Recent Missed Execution». Riaccensione automatica del server (DOMANDE n. 22). Un controllo che, se il debrief non è partito entro le 7:15, avvisa in Teams. Vale anche per P-A, con il suo lettore periodico.

### VER2, rilievo 5

**Tesi:** Alla settimana 8 il follow-up può già passare a L2 (10 sì senza modifiche in 30 giorni, più il via del parere) e la scala dà autonomia vera verso i clienti (P-D §1 riga 5, §5.1).

**Esito:** non dimostrata.

**Prove:** Al 5/10 c'erano 11 lead, 1 risposta e 0 meeting [verificato: PRESENTAZIONE-CEO §7.1]. Dieci call esterne con follow-up approvato senza modifiche in 30 giorni non sono in vista. La fase «in ombra» e i 20 invii per L3 allungano ancora i tempi (P-D §3.2-3.3). Il parere è previsto entro la settimana 3 [verificato: P §9.4], ma il suo esito sull'art. 130 è aperto [verificato: ricerca/16, domanda 6]. Le tesi «stesso livello della trascrizione» (§1) e «primo follow-up L2» (§3.5) si contraddicono, come notano già i giudici.

**Correzione:** Soglie 5 e 15 come in P-A. Nessuna ombra per i flussi solo interni. Le soglie contano anche le call con clienti già attivi. Ai CEO e ad Alberto si dice chiaramente che verso l'esterno, alla settimana 8, l'autonomia reale è L1. P-A ha lo stesso limite dei volumi, solo con soglie più basse.

### VER2, rilievo 6

**Tesi:** Le protezioni essenziali bastano e la retrocessione automatica corregge gli errori: un «Ferma» con motivo, una rettifica, un reclamo o un'opposizione riportano la classe a L1 (P-D §3.3).

**Esito:** non dimostrata.

**Prove:** P-D non dice chi riconosce un reclamo o un «non scrivetemi» nelle risposte, né con quale classificatore. Se un reclamo non viene riconosciuto, la classe resta L3 e la lista di soppressione non si aggiorna. P-A ammette lo stesso buco e lo copre con il tasto «sbagliato» sul riepilogo del giorno [testo di P-A §3.5]. La lista unica di soppressione è obbligatoria [verificato: P §9.1 r.5; ricerca/16 riga 124]. Il resto delle protezioni c'è e non va oltre l'essenziale: limiti fissi nel codice, stop, tetti, registro a sola aggiunta, annulla e rettifica, outbox con «incerta» [verificato: P-D §4.1; SPEC §4.8].

**Correzione:** Ogni risposta di un esterno a un messaggio L2 o L3 passa da un passo N che la classifica (correzione, lamentela, opposizione, altro). Nel dubbio la risposta va in carta a una persona e la classe resta ferma finché qualcuno non decide. Il tasto «sbagliato» va nel debrief, preso da P-A.

### VER2, rilievo 7

**Tesi:** Nessun dato rosso resta sul banco di prova anche con n8n, grazie alle tre regole del §4.4 (niente salvataggio delle esecuzioni, nessun Wait con testo rosso, controllo del database).

**Esito:** vera.

**Prove:** Le variabili EXECUTIONS_DATA_SAVE_* e la scelta per singolo flusso esistono. La pulizia di serie cancella dopo 336 ore. Il nodo Wait salva l'esecuzione sopra i 65 secondi [verificato: P-D §4.4 sulle pagine di docs.n8n.io; confermato dal giudice CPTO con Context7 il 10/11]. Le trascrizioni integrali sono rosse e sul banco si salvano solo dati verdi e gialli [verificato: PRESENTAZIONE-CEO, tabella dei colori e §11 «Il banco di prova»].

**Correzione:** Resta in piedi, ma va unita al registro eventi fuori da n8n (rilievo 3). Senza quel registro, togliere lo storico rende inaffidabile il recupero dei flussi rossi. Fino al parere, il testo rosso verso l'API passa dall'oscuramento locale, come P-D già dice.

### VER2, rilievo 8

**Tesi:** Registrazione delle call e post-call autonomo sono leciti e affidabili dalla fase 1, con l'avviso nell'invito e a voce (P-D §4.1 punto 6; flusso 1).

**Esito:** vera.

**Prove:** La registrazione regge sul legittimo interesse se ci sono avviso preventivo, finalità e conservazione dichiarate, e accesso limitato [verificato: ricerca/16 righe 27 e 61]. Il limite pratico è che nelle call organizzate dai clienti la registrazione di Teams probabilmente non parte e il bot va ammesso [verificato: ricerca/30 §3.6 e §4.4, citati nella v2.1 e in P-A]. P-D lo rimanda a Vexa nella fase 3, quindi dichiara la lacuna.

**Correzione:** Test di bilanciamento scritto e informativa nell'invito prima della prima call registrata. Quando la trascrizione non c'è, l'agente chiede una nota vocale (L0), come in P-A. Le call con clienti nel Regno Unito restano nel parere.

### VER2, rilievo 9

**Tesi:** Andrea a L3 (richiamata entro 90 secondi) è lecito con il consenso nel modulo e la frase fissa che dichiara l'AI.

**Esito:** non dimostrata.

**Prove:** Le chiamate senza operatore richiedono il consenso preventivo (art. 130 c.1) e il controllo del Registro delle opposizioni. Se la richiamata chiesta dalla lead sia una «chiamata automatizzata» è una domanda ancora aperta del parere [verificato: ricerca/16 righe 19, 95, 191 e domanda 3]. P-D lega il via al parere e alle lead vere [testo di P-D §5.4], ma nella tabella del flusso 6 scrive «L3 dal primo giorno dal vivo» senza questa condizione.

**Correzione:** Nel flusso 6 scrivere esplicitamente: L3 solo dopo il parere, con il testo del consenso che il parere approva, il controllo RPO non più vecchio di 30 giorni e il rifiuto automatico delle lead senza consenso registrato. Vale uguale per P-A.

## VER3 · costi, server e manutenzione

**Verdetto:** regge con correzioni.

### VER3, rilievo 1

**Tesi:** I costi mensili e una tantum di P-D sono quelli della v2.1, già verificati (circa 135 €/mese nelle fasi 0-1; 479-583 € a regime; RAM 690-830 €; seconda GPU 880-1.220 €; linea di riserva 77-200 € più 10-11 €/mese; revisione esterna facoltativa, fino a 5.940 € risparmiati)

**Esito:** vera.

**Prove:** Le cifre coincidono con PRESENTAZIONE-CEO §6.3 riga 399, §12.2 righe 622-623 e §14 decisioni 5, 11, 12 e 13 (righe 687-695). Il prezzo della RAM è confermato anche in ricerca/37 righe 72 e 409 (ram-24, forbice 690-830 €). R36 §4.2 dava ancora 816-1.218 €: è un valore superato dalla v2.1, non un errore di P-D. I 6,41 € dell'utente di servizio sono segnati correttamente come non verificati (ricerca/33 riga 68; ricerca/28 riga 79). Il risparmio sulla revisione esterna non distingue P-D: vale allo stesso modo per P-A (P-A §6.1).

**Correzione:** Nessuna sulle cifre. Va però detto che il vantaggio di costo in euro rispetto a P-A è nullo: le due proposte hanno gli stessi canoni e la stessa revisione facoltativa. Il punto in più ai «costi» che i giudici danno a P-D viene solo dai giorni-persona (vedi il rilievo sui 230 gp).

### VER3, rilievo 2

**Tesi:** Il totale scende a circa 230 gp contro 249,25, e le fasi 0-1 a 37,5 gp (circa 50 con la riserva, sotto i 52 di capacità)

**Esito:** non dimostrata.

**Prove:** La riserva è calcolata bene: 230 × 4/3 ≈ 307. Il taglio di circa 19 gp però non è spiegato voce per voce. Nella tabella di P-D §6.3 la fase 5 scende da 38 a circa 37 e la fase 6 da 24 a circa 22, con la colonna «Cosa cambia» vuota («—»). Il contenuto dei 57 agenti vale circa 67 gp in R36 §7.3 (righe 541, 551, 557, 559, 565, 569) e non cala solo perché un agente diventa un flusso; anche il giudice CPTO lo segnala. Per la fase 1 (20 gp) ho rifatto il conto su R36 §7.3: 22,5 meno il motore (5,5) fa 17; più l'esecutore Jira (1,75, R36 riga 546), il calendario, l'installazione di n8n sul banco, livelli, finestra, annulla e soppressione (+2-3,5 secondo P-A §5.2), meno 3,5 di semplificazioni. Si arriva a circa 20,5-22 gp. Il Rapporto 2 stima la sola finestra in 3-5 giorni. Il renderer dei documenti è un servizio nuovo senza giorni in nessun file. Infine n8n sul banco dalla fase 1 porta esercizio già nella fase 1, dove la v2.1 ne conta 0 (R36 §7.2 riga 511).

**Correzione:** Scrivere una tabella dei gp voce per voce, come R36 §7.3, con il renderer, l'installazione e l'esercizio di n8n sul banco, e i pezzi di Cancello e Porta per L2. Fino ad allora conviene usare 240-250 gp e, per le fasi 0-1, circa 39-41 gp di base (52-55 con la riserva): la stessa fascia di rischio di sforare la settimana 8 che ha la v2.1. Mattia rifà la stima, come chiede P-D stessa.

### VER3, rilievo 3

**Tesi:** A regime P-D usa circa 10 GB meno della v2.1 (60-64 contro 70-74 GB) e nelle fasi 3-4 lascia circa 6 GB liberi invece di zero

**Esito:** non dimostrata.

**Prove:** I conti tornano: 53 - 47 = 6 e 53 - 60/64 = da -7 a -11. Il risparmio però nasce quasi tutto da stime più strette, non dall'architettura. (1) Runner: 7 GB per 6 sessioni contro i 12 di R36 §4.2 riga 258. R26 riga 126 dà 1 GiB a sessione come punto di partenza e scrive che «la memoria cresce con la durata della sessione»: 7 GB lasciano circa 1 GB per sistema operativo e container. (2) Cancello, Porta e renderer stanno in 3,5 GB, mentre R36 dà 4 GB a Cancello e Porta da soli (riga 259; Cancello 3-4 GB alla riga 218): il renderer (0,5-1 GB secondo P-D) è entrato senza farli crescere. (3) n8n con worker in più (+2-3 GB) richiede Redis: la documentazione di n8n sulla modalità a code scrive che servono Redis e il database e che SQLite non è supportato (letta con Context7 il 10/11/2026). Nella repo Redis non compare fra i servizi del board né nelle tabelle di P-D. (4) Postiz anticipato alla fase 2 è contato a 2 GB, ma ha bisogno di Postgres e Redis (ricerca/05 riga 432; 34-proposta-1 riga 99).

**Correzione:** Rifare la tabella di P-D §2.3 con il runner a 10-12 GB e Cancello più Porta a 4 GB, più il renderer e Redis (oppure scrivere che n8n gira senza worker in più). La forbice realistica è di 2-6 GB in meno della v2.1, non 10. La regola d'acquisto resta quella di oggi: si misura con 6 sessioni e si compra sotto i 5 GB di margine (R36 §4.2). Con Michele disposto a salire a 384 GB (aggiornamento del 10/11) la RAM non decide fra P-D e P-A.

### VER3, rilievo 4

**Tesi:** P-D toglie peso a Michele: meno servizi, niente VM né VLAN del motore, e n8n è già nel board

**Esito:** falsa.

**Prove:** Oggi la v2.1 aggiunge 11-13 servizi e 3 reti nuove al perimetro con le patch entro 14 giorni (PRESENTAZIONE-CEO riga 651; R36 §4.5). P-D toglie una sola rete, la VLAN 32 (resta il dubbio, vedi sotto). Contando la sua tabella §2.2, aggiunge invece più servizi da tenere aggiornati entro 14 giorni:
- una seconda istanza di n8n sul banco di prova dalla fase 1, che non è quella del board;
- worker di n8n e Redis;
- un renderer dei documenti;
- Postiz, con il suo Redis, già nella fase 2;
- il runner, il Cancello e la Porta in container separati;
- mcp-01, MariaDB, trascrizione, Vexa, Asterisk, Pipecat, listmonk, DocuSeal e fatturazione.
In tutto sono circa 15-17 servizi, contro 11-13. Lo ammette P-D stessa al §8: «il conto dei servizi cambia poco». C'è anche una contraddizione interna sulla rete: al §2.2 scrive che la VLAN 32 «se serve lo decide Michele», al §6.4 che «non serve più». Infine Postiz prima della fase F4 urta la regola di P §6.2, riga 385: prima della F4 entrano solo i servizi del pilota.

**Correzione:** Togliere l'affermazione e scrivere il perimetro vero: un elenco dei servizi con fase d'ingresso e responsabile delle patch, come R36 §4.5, compresi n8n sul banco, Redis, il renderer e Postiz. Chiedere a Michele in modo esplicito Postiz e n8n prima della F4. Anche P-A anticipa Postiz e ha lo stesso problema (P-A §2.1).

### VER3, rilievo 5

**Tesi:** n8n costa 0 € e il nucleo di P-D non chiede abbonamenti; la dipendenza dal fornitore è gestibile con i flussi in JSON versionati in git

**Esito:** non dimostrata.

**Prove:** Che l'uso interno costi 0 € è vero: la Sustainable Use License ammette l'uso interno (ADR-0011 riga 32; R36 riga 820). Ma la stessa licenza vieta la rivendita (ADR-0011 riga 55), e PRESENTAZIONE-CEO §1 e §2.3 presenta il sistema anche come offerta per le PMI. L'integrazione git nativa di n8n («Version control using Git», ambienti) è una funzione del piano Enterprise: la documentazione lo scrive in chiaro, letta con Context7 il 10/11/2026. Senza licenza i flussi si portano in git solo con un'esportazione via CLI o API scritta da noi. In più P-D mette 35-40 figure dentro n8n, il cui responsabile delle patch è l'amministratore del server (R36 §4.5, riga 330). Ogni aggiornamento di sicurezza del board tocca quindi la logica aziendale. La versione 3.0 cambia l'API e la richiesta di fissare la 2.x viene dal Rapporto 4, che non ho riletto. La regola «la logica del motore non dipende da n8n» cade (ADR-0011 riga 23).

**Correzione:** (1) Esportazione automatica dei flussi in git con uno script nostro (n8n export:workflow o API pubblica), contata nei gp, oppure il prezzo della licenza Enterprise, che non è nei file. (2) Prompt, schemi e scelta dei destinatari in un servizio TypeScript fuori da n8n, come chiede il giudice CPTO, così che uscirne costi poco. (3) Una regola scritta su chi aggiorna n8n e su come si provano i flussi prima di ogni patch entro i 14 giorni. (4) La decisione sulla rivendita va presa ora.

### VER3, rilievo 6

**Tesi:** I tetti di spesa sul banco di prova si reggono sul limite per chiave della Console di Anthropic, finché LiteLLM non arriva con la F4

**Esito:** non dimostrata.

**Prove:** Lo SPEC elenca fra le ipotesi da verificare «La Console permette un limite di spesa per area di lavoro» (SPEC riga 664). P-D lo ammette al §4.1, punto 3. Oggi poi lo sviluppo non ha una chiave API e le prove usano un modello a copione (aggiornamento del 10/11). LiteLLM arriva con la fase F4 del board (R36 §7.1).

**Correzione:** Tenere questa ipotesi fra le verifiche della fase 0. Se il limite per area di lavoro non c'è, aggiungere un contatore di spesa nel Cancello o nel servizio TypeScript. Il difetto vale identico anche per P-A (P-A §2.1: «chiave diretta con tetto nella Console»).

### VER3, rilievo 7

**Tesi:** Il risparmio di P-D sui mensili include Metricool tolto già dalla fase 2 (-59,86 €), grazie a Postiz anticipato

**Esito:** non dimostrata.

**Prove:** La decisione 15 tiene Metricool «finché Postiz non è pronto (fase 4)» (PRESENTAZIONE-CEO riga 697). Postiz prima della F4 dipende dal sì di Michele (P §6.2 riga 385). Postiz serve anche al cambio della regola della sessione presidiata (P riga 168). Secondo ricerca/05 riga 432 chiede inoltre un dominio pubblico per i callback OAuth: va chiarito con il «mai pubblico» di R36 §4.5. La cifra di 59,86 € è giusta (R36 §8.2), ma il kit commerciale è contato a parte e P-D stessa non la mette nel totale.

**Correzione:** Presentarlo come risparmio condizionato a tre sì: Michele, Alberto e la prova dei callback OAuth senza esposizione. Altrimenti Metricool resta fino alla fase 4. Vale anche per P-A, che fa lo stesso anticipo.

### VER3, rilievo 8

**Tesi:** P-D non aggiunge lavoro alla GPU e non dipende dalla seconda GPU per partire

**Esito:** vera.

**Prove:** I passi AI vanno a Claude via API. La RTX 4000 è quasi piena di giorno (R36 §4.3) e viene prestata a Experimental solo «qualche ora a settimana» (ricerca/37 riga 20). La seconda GPU serve dalla fase 3 e prima di Andrea sulla GPU (P §6.4). Il secondo nodo di dicembre, fino a 1.500 €, è citato bene (ricerca/37 riga 53).

**Correzione:** Nessuna. Su questo P-D e P-A sono pari: neanche il motore di P-A usa la GPU (P §6.2).

### VER3, rilievo 9

**Tesi:** Dipendenza dai fornitori: P-D è più sicura di P-A perché toglie il ponte con l'Agent SDK nella fase 1

**Esito:** non dimostrata.

**Prove:** P-D sposta la dipendenza, non la riduce. Toglie l'SDK dalla fase 1 (rilasci quasi quotidiani: ADR-0001 conta 333 versioni TypeScript) ma lo rimette dalla fase 2 con il runner sottile. In più aggiunge n8n come secondo cuore, con la licenza e la funzione git Enterprise viste sopra, la 3.0 in arrivo e una vulnerabilità con CVSS 10 nel 2026 (ADR-0011 riga 61, segnata come non verificata). Entrambe le proposte restano legate all'API di Anthropic. L'uscita di P-D costa circa 1 gp per ognuno dei 35-40 flussi, una stima propria (P-D §8). L'uscita di P-A verso Hermes costa 26-33 gp (P §15).

**Correzione:** Nella valutazione del rischio contare due fornitori critici, Anthropic e n8n, con una versione fissata e la prova dei flussi registrati a ogni aggiornamento. Il conto di uscita va messo accanto a quello di P-A: con 35-40 flussi a 1 gp l'uno, l'uscita di P-D (35-40 gp) costa più di quella di P-A.
