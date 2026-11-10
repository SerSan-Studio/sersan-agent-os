# Requisiti di autonomia dalla trascrizione di riferimento (AU)

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **RAP1**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

**Fonti.**
- **TR** è la trascrizione di riferimento, `C:\Users\alber\Desktop\tracrizione bot aziendali.txt`. L'ho letta per intero il 9/11/2026, da 0:00 a 23:19. I minuti citati sono quelli segnati nel file.
- **VF** è `C:\Users\alber\sersan-agent-os\ricerca\00-visione-funzionalita.md`, letto per intero (voci J1-J9 e A1-L12).
- I limiti fissi del progetto vengono da `C:\Users\alber\sersan-agent-os\docs\03-architettura.md`.



**Come leggere.**
- Il livello indicato è quello descritto nella TR, non quello scelto dal progetto.
- **«L3 int.»** indica un'azione che parte da sola e resta dentro l'azienda (raccolta, analisi, report al team): le persone la vedono dopo.
- **«L0»** indica che l'agente prepara e poi una persona usa il risultato o agisce.
- **«n.d.»** significa che la TR non lo dice.
- Persone e aziende del video non sono nominate. Gli strumenti sono descritti per la funzione che svolgono. «L'imprenditore» è sempre l'imprenditore del video.

## 1. Elenco AU

### Memoria, agenti di fondo, chat fra agenti

**AU-01 — I dati aziendali migliorano i processi di continuo.**
- **Cosa:** l'AI usa i dati delle call, i processi del team, i dati finanziari, gli obiettivi, i calendari e le agende per «migliorare continuamente i processi» e velocizzare il lavoro delle persone.
- **Parte da:** lavoro continuo, frequenza n.d.
- **Agisce:** «le AI» del sistema, senza altri dettagli.
- **Persona:** n.d.
- **Esterno:** n.d.
- **Impara:** sì; il metodo non è descritto.
- **Livello:** n.d.

[verificato: TR 0:00-0:24, voce fuori campo]

**AU-02 — Assistente per la vita personale e familiare.**
- **Cosa:** lo stesso sistema gestisce il calendario e la dieta dell'imprenditore e dei figli, insieme alla moglie. Raccoglie i dati dello smartwatch e del materasso intelligente. Nella stessa memoria ci sono esami del sangue, visite mediche, preferenze di viaggio, famiglia e cibo.
- **Parte da:** i dati dei dispositivi, in modo continuo.
- **Agisce:** il sistema personale. La memoria è una sola, per la vita personale e per l'azienda.
- **Persona:** n.d.
- **Esterno:** nessun effetto verso i clienti.
- **Impara:** n.d.
- **Livello:** n.d. La raccolta dai dispositivi è automatica.

[verificato: TR 0:24-0:31; 2:42-2:45; 3:00-3:12]

**AU-03 — Un agente entra nelle call e le trascrive.**
- **Cosa:** tutte le riunioni vengono registrate, dichiarandolo. Nelle call online un agente si collega da solo e tiene la trascrizione. Negli incontri dal vivo l'imprenditore chiede il permesso e registra con il telefono. Il motivo dato è che il contesto è la cosa più importante.
- **Parte da:** ogni call.
- **Agisce:** l'agente di registrazione.
- **Persona:** dichiara la registrazione; dal vivo la avvia lei.
- **Esterno:** l'agente è presente nelle call, anche in quelle con i clienti.
- **Impara:** n.d.
- **Livello:** L3 nelle call online, L0 dal vivo.

[verificato: TR 2:17-2:30]

**AU-04 — L'agente partecipa alle call al posto di chi manca, in tutta l'azienda.**
- **Cosa:** lo strumento registra, riassume e analizza le conversazioni dell'imprenditore e del resto dell'azienda: incontri con i clienti, one-to-one, riunioni sulla pipeline. In una call a cui lui non ha partecipato, «c'era un mio agente all'interno della call».
- **Parte da:** ogni call in agenda, anche quando il titolare è assente.
- **Agisce:** l'agente di registrazione.
- **Persona:** nessuno durante la call; si legge dopo.
- **Esterno:** l'agente è presente nella call con clienti o colleghi.
- **Impara:** n.d.
- **Livello:** L3.

[verificato: TR 5:27-5:51]

**AU-05 — Agenti di fondo: raccolta, pulizia, indicizzazione.**
- **Cosa:** l'orchestratore è open source, installato su una macchina propria, e sta fra la memoria e modelli di più fornitori. Ci girano 25 agenti. Alcuni lavorano in sottofondo: uno raccoglie le informazioni, uno le pulisce, uno costruisce la parte vettoriale dei database. Altri svolgono le attività vere e proprie. Le memorie sono due: una relazionale per le informazioni fisse, una vettoriale che collega i momenti.
- **Parte da:** lavoro di sottofondo, frequenza n.d.
- **Agisce:** gli agenti di fondo.
- **Persona:** nessuno.
- **Esterno:** nessuno.
- **Impara:** vedi AU-06.
- **Livello:** L3 int.

[verificato: TR 3:14-3:53]

**AU-06 — Gli agenti imparano da soli.**
- **Cosa:** gli agenti «imparano e autoimparano» che cosa si può costruire.
- **Parte da:** n.d.
- **Agisce:** gli agenti dell'orchestratore.
- **Persona:** n.d.
- **Esterno:** nessun effetto diretto.
- **Impara:** sì, da soli; il meccanismo non è descritto.
- **Livello:** L3 int.

[verificato: TR 3:53-3:59]

**AU-07 — Chat comune fra gli agenti, dove il lavoro passa dall'uno all'altro.**
- **Cosa:** gli agenti hanno una chat condivisa in cui si parlano. Il messaggio di un agente fa partire il lavoro di un altro. Per esempio, chi raccoglie scrive «ho trovato tre nuove call» e l'agente degli appuntamenti va a vedere se ce ne sono da fissare.
- **Parte da:** un evento annunciato da un altro agente.
- **Agisce:** gli agenti.
- **Persona:** nessuno. [non verificato: la TR non dice se le persone leggono la chat]
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L3 int.

[verificato: TR 3:59-4:18]

**AU-08 — Un agente fissa gli appuntamenti che gli altri agenti trovano.**
- **Cosa:** quando viene annunciato che ci sono nuove call, l'agente incaricato degli appuntamenti controlla se ce ne sono da fissare.
- **Parte da:** il messaggio dell'agente di raccolta nella chat comune.
- **Agisce:** l'agente degli appuntamenti.
- **Persona:** nessuna persona nominata.
- **Esterno:** appuntamenti in calendario. [non verificato: la TR non dice se gli inviti partono verso persone esterne né se qualcuno li conferma]
- **Impara:** n.d.
- **Livello:** L3, per come è descritto.

[verificato: TR 4:08-4:18]

**AU-09 — Momenti di scambio fra agenti; i to-do superati vengono chiusi.**
- **Cosa:** come in un team di persone, gli agenti hanno «momenti di scambio comune» in cui si aiutano. Uno fa notare all'altro che certi to-do sono già fatti e gli dice di chiuderli.
- **Parte da:** i momenti di scambio, che sono ricorrenti; frequenza n.d.
- **Agisce:** gli agenti.
- **Persona:** nessuno.
- **Esterno:** nessuno; toccano solo liste di to-do.
- **Impara:** gli agenti si correggono a vicenda.
- **Livello:** L3 int.

[verificato: TR 4:18-4:29]

### Dopo la call: un solo agente, un solo flusso

Queste voci valgono per AU-10, AU-11, AU-12 e AU-13:
- **Parte da:** la fine della call, quando la trascrizione è pronta.
- **Agisce:** un solo agente.
- **Persona:** nessuno; vede dopo. Prima l'imprenditore doveva ricordarsi tutto o farlo fare a qualcuno del team.
- **Impara:** n.d.
- **Livello:** L3. Il flusso «avviene in modo totalmente autonomo».

[verificato: TR 4:30-5:07]

**AU-10 — Punti principali e prossimi passi nel canale del cliente.**
- **Esterno:** un messaggio nel canale chat dedicato al cliente. [non verificato: la TR non dice se il cliente legge quel canale]

[verificato: TR 4:40-4:51]

**AU-11 — Opportunità creata nel CRM.**
- **Esterno:** scrittura nel CRM.

[verificato: TR 4:51-4:54]

**AU-12 — Mail di follow-up al cliente appena incontrato, con i punti principali.**
- **Esterno:** email al cliente.
- **Nota:** il verbo usato è «fa una mail». L'autonomia totale però è dichiarata per tutto il flusso, e l'imprenditore dice che i follow-up non li fa più lui.

[verificato: TR 4:54-4:58; 9:45-9:49]

**AU-13 — To-do per l'imprenditore e per il team.**
- **Esterno:** nessuno.

[verificato: TR 4:58-5:03]

### La giornata e le call

**AU-14 — Debrief del mattino alle 5:30.**
- **Cosa:** si ripassa cosa è successo ieri e quali prossimi passi servono per pianificare la giornata. È il primo passo del giorno.
- **Parte da:** un orario fisso, le 5:30, segnato in calendario.
- **Agisce:** la persona. [non verificato: la TR non dice se un agente prepara il debrief]
- **Persona:** lo fa lei.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L0.

[verificato: TR 2:02-2:09; 5:12-5:25]

**AU-15 — Analisi di una call su richiesta.**
- **Cosa:** l'imprenditore porta in un modello linguistico la registrazione di una call, anche di una a cui non ha partecipato. Chiede cosa si è discusso e quali sono i prossimi passi.
- **Parte da:** la richiesta della persona.
- **Agisce:** il modello.
- **Persona:** chiede, poi decide e agisce.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L0.

[verificato: TR 5:51-6:00]

**AU-16 — Registro dei meeting di tutta l'azienda, con la pipeline.**
- **Cosa:** lo strumento delle call, insieme al modello, fa un'analisi strutturata di ogni meeting e li tiene tutti in un registro. Ciascuno vede anche i meeting degli altri. In automatico il sistema dice chi c'era e chi no, cosa è successo, quale pipeline è emersa e chi è «caldo» entro una certa data.
- **Parte da:** ogni call registrata.
- **Agisce:** lo strumento delle call con il modello.
- **Persona:** vede dopo.
- **Esterno:** nessuno.
- **Impara:** n.d. Tutto viene dalla trascrizione.
- **Livello:** L3 int.

[verificato: TR 6:07-6:44]

**AU-17 — Le regole di lavoro vengono lette prima di ogni compito.**
- **Cosa:** i riassunti standard degli strumenti di registrazione sono di bassa qualità. Per questo l'imprenditore ha scritto una volta come vuole i prossimi passi, i report e il suo modo di lavorare. Quando l'agente fa una ricerca, va a cercarsi queste regole da solo.
- **Parte da:** ogni richiesta o ricerca.
- **Agisce:** l'agente.
- **Persona:** scrive le regole una volta.
- **Esterno:** nessuno.
- **Impara:** n.d. Le regole le scrive la persona.
- **Livello:** L3 int.

[verificato: TR 6:44-7:12]

### Vendite: pipeline, brief, slide, offerta, posta

**AU-18 — Pipeline pesata sullo storico.**
- **Cosa:** un portale clienti, costruito in casa con uno strumento di sviluppo AI, prende i dati dal CRM e da tutte le call. Costruisce la pipeline e la percentuale pesata. Stima dallo storico dei clienti quanto è probabile chiudere ogni progetto, invece di andare a sensazione.
- **Parte da:** i dati del CRM e delle call. [non verificato: la TR non dice ogni quanto si aggiorna]
- **Agisce:** il portale.
- **Persona:** vede dopo.
- **Esterno:** nessuno; legge soltanto il CRM.
- **Impara:** usa tutto lo storico; non è detto se si ricalibra da solo.
- **Livello:** L3 int.

[verificato: TR 7:13-7:42]

**AU-19 — Brief prima di ogni incontro.**
- **Cosa:** partendo dall'email della persona da incontrare, il brief raccoglie da solo:
  - chi è oggi la sua azienda: operazioni societarie, dati economici pubblicati, sede;
  - chi partecipa alla call;
  - tutto ciò che si sa della persona, nei dati aziendali e in quelli personali dell'imprenditore: da quando è nel CRM, l'ultima mail, le aperture di mail e newsletter, i post sul social professionale;
  - lo storico della relazione;
  - i segnali strategici, i temi da trattare e le opportunità comuni.
- **Parte da:** la persona inserisce l'email. La voce fuori campo dice che l'imprenditore «in automatico si prepara» per tutti gli incontri.
- **Agisce:** lo strumento dei brief, costruito in casa.
- **Persona:** inserisce l'email e usa il brief nell'incontro.
- **Esterno:** nessuno; fa solo letture.
- **Impara:** n.d.
- **Livello:** L0.

[verificato: TR 7:42-8:44]

**AU-20 — Slide automatiche sulla storia della relazione.**
- **Cosa:** le slide per l'incontro raccontano la relazione con il cliente: da quanti anni dura e quante persone del cliente hanno partecipato. Sono «totalmente automatizzate».
- **Parte da:** la preparazione dell'incontro.
- **Agisce:** lo strumento dei brief.
- **Persona:** le presenta al cliente.
- **Esterno:** arrivano al cliente attraverso la persona.
- **Impara:** n.d.
- **Livello:** L0.

[verificato: TR 8:36-8:55]

**AU-21 — Offerta commerciale dopo l'incontro.**
- **Cosa:** «la stessa cosa avviene dopo l'incontro». Si costruisce un'offerta su misura mettendo insieme il catalogo, quanto detto nell'incontro e quanto si sa dell'azienda.
- **Parte da:** la fine dell'incontro.
- **Agisce:** lo stesso sistema. [non verificato: la TR dice «andiamo a costruire» e non chiarisce quanto fa l'agente]
- **Persona:** n.d. chi la rivede e chi la invia.
- **Esterno:** l'offerta va al cliente. [non verificato: l'invio non è descritto]
- **Impara:** n.d.
- **Livello:** n.d., almeno L0.

[verificato: TR 8:55-9:05]

**AU-22 — Follow-up e mail non più scritti a mano.**
- **Cosa:** l'imprenditore ha 8-10 meeting al giorno. Non fa più lui i follow-up e non risponde lui alle mail.
- **Parte da:** le mail in arrivo e i meeting.
- **Agisce:** n.d.
- **Persona:** n.d. La frase dice solo che non lo fa lui.
- **Esterno:** mail verso clienti, partner e team.
- **Impara:** n.d.
- **Livello:** n.d. Per il follow-up dopo la call vale AU-12, che è L3.

[verificato: TR 9:41-9:52]

### Processi

Contesto: un ingegnere AI dell'azienda mostra il sistema che traccia i processi per renderli più efficienti. L'azienda lo usa per sé e per i clienti. [verificato: TR 11:49-12:04]

**AU-23 — Lettura dei metadati della suite d'ufficio.**
- **Cosa:** il sistema mappa i dati d'uso di posta, calendario, archivio file e fogli di calcolo. Per privacy non entra nel contenuto dei singoli file: legge solo i metadati d'uso.
- **Parte da:** l'avvio della mappatura. [non verificato: non è detto se la mappatura è continua o fatta una volta sola]
- **Agisce:** il sistema di mappatura.
- **Persona:** nessuno.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L3 int.

[verificato: TR 12:04-12:16]

**AU-24 — Osservazioni alla persona su come usa gli strumenti.**
- **Cosa:** il sistema dice alla persona, per esempio, che apre sei file sette volte al giorno. Le chiede se ha senso tenere i dati sempre in quel foglio di calcolo.
- **Parte da:** i risultati della mappatura.
- **Agisce:** il sistema.
- **Persona:** riceve il suggerimento e decide.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L0.

[verificato: TR 12:17-12:23]

**AU-25 — Intervista guidata.**
- **Cosa:** dopo la mappatura parte una breve intervista per capire il lavoro giorno per giorno. Comincia da come la persona descrive il suo ruolo.
- **Parte da:** la fine della mappatura.
- **Agisce:** dal contesto sembra il sistema. [non verificato: la TR non dice esplicitamente chi fa le domande]
- **Persona:** risponde.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L3 int., se l'intervista la conduce il sistema.

[verificato: TR 12:25-12:36]

**AU-26 — Mappa dei processi, ore nascoste e automazioni consigliate.**
- **Cosa:** il sistema restituisce tre cose:
  - la mappa dei processi. Esempio B2B: acquisizione lead, call col prospect, mail di follow-up, proposta, kickoff, presentazione, tracciamento dell'esito;
  - la stima di volumi e ore: circa sei proposte a settimana, tre-quattro ore ciascuna, circa 18 ore di costo implicito;
  - le automazioni consigliate: deck da un modello unico, follow-up della call totalmente automatizzabile, brief di intake.
- **Parte da:** mappatura e intervista.
- **Agisce:** il sistema.
- **Persona:** decide quali automazioni fare.
- **Esterno:** nessun effetto diretto. Per i clienti diventa un servizio.
- **Impara:** indica da solo dove conviene automatizzare.
- **Livello:** L0.

[verificato: TR 12:36-13:20]

### Vendite che si allenano e agente vocale

Contesto: secondo la voce fuori campo, tutto l'inserimento dei potenziali clienti è stato «automatizzato e migliorato». [verificato: TR 13:39-13:46]

**AU-27 — Ogni call di vendita trascritta in un canale comune.**
- **Cosa:** soprattutto nella vendita dei corsi B2C, tutte le call vengono trascritte in un canale chat dove ci sono tutte le persone. Si vede chi è il venditore e chi il cliente.
- **Parte da:** ogni call di vendita.
- **Agisce:** il sistema delle call.
- **Persona:** vede dopo.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L3 int.

[verificato: TR 13:47-14:01]

**AU-28 — Fit score del prospect.**
- **Cosa:** il sistema valuta in automatico quanto il prospect è adatto al corso. Esempio: 10 su 100, quindi probabilmente non è il cliente migliore.
- **Parte da:** ogni call.
- **Agisce:** il sistema.
- **Persona:** vede dopo.
- **Esterno:** nessuno.
- **Impara:** n.d.
- **Livello:** L3 int.

[verificato: TR 14:01-14:08]

**AU-29 — Valutazione della call e consigli di coaching.**
- **Cosa:** il sistema giudica la prestazione del venditore (per esempio: call insufficiente, nessun tentativo di discovery). Indica punti di forza, cose da migliorare e consigli di coaching, anche a chi ha lavorato bene.
- **Parte da:** ogni call.
- **Agisce:** il sistema.
- **Persona:** vede dopo.
- **Esterno:** nessuno.
- **Impara:** fa migliorare le persone, non sé stesso.
- **Livello:** L3 int.

[verificato: TR 14:08-14:36]

**AU-30 — Dopo ogni call il report va al venditore e al suo responsabile.**
- **Cosa:** dopo ogni conversazione di vendita il report arriva al venditore e al suo responsabile. Nella TR è descritta come «formazione alla rete vendita totalmente automatizzato». I commerciali hanno un sistema di formazione continua.
- **Parte da:** la fine di ogni call di vendita.
- **Agisce:** il sistema.
- **Persona:** venditore e responsabile vedono dopo.
- **Esterno:** nessuno.
- **Impara:** fa migliorare i commerciali di continuo.
- **Livello:** L3 int.

[verificato: TR 14:36-14:50; 16:02-16:06]

**AU-31 — L'agente vocale richiama ogni lead entro 90 secondi, a qualsiasi ora.**
- **Cosa:** quando qualcuno lascia un contatto, entro 90 secondi lo chiama un agente vocale. L'agente dichiara di essere un'AI e parla con la voce registrata di un collega. Lavora 24 ore su 24, 7 giorni su 7, tutto l'anno. Prima la richiamata arrivava dopo 2 ore. Secondo la TR, il tasso di conversione dei commerciali è raddoppiato.
- **Parte da:** un contatto lasciato.
- **Agisce:** l'agente vocale.
- **Persona:** nessuno durante la chiamata.
- **Esterno:** telefonata al potenziale cliente.
- **Impara:** vedi AU-33.
- **Livello:** L3.

[verificato: TR 14:50-15:07; 15:50-16:02]

**AU-32 — L'agente vocale fissa l'incontro con un commerciale e registra l'esito.**
- **Cosa:** a fine chiamata l'agente riporta da solo com'è andata. Per esempio: ha fissato un incontro con un commerciale reale, una persona fisica. Oppure annota che la persona ha rifiutato la consulenza gratuita.
- **Parte da:** la fine della chiamata.
- **Agisce:** l'agente vocale.
- **Persona:** il commerciale prende l'incontro; gli altri vedono l'esito dopo.
- **Esterno:** appuntamento con il potenziale cliente.
- **Impara:** vedi AU-33.
- **Livello:** L3.

[verificato: TR 15:07-15:27]

**AU-33 — L'agente vocale impara dai rifiuti.**
- **Cosa:** quando la persona rifiuta, l'agente cerca da solo il perché. Cerca anche come cambiare l'apertura e la conversazione, per migliorare di continuo. Il team lo testa di continuo.
- **Parte da:** ogni rifiuto.
- **Agisce:** l'agente vocale.
- **Persona:** il team fa i test. [non verificato: la TR non dice se una persona controlla la nuova apertura prima che venga usata]
- **Esterno:** cambiano le chiamate future.
- **Impara:** sì, dall'esito delle chiamate.
- **Livello:** L3, per come è descritto.

[verificato: TR 15:31-15:43]

**AU-34 — L'agente vocale risponde alle chiamate.**
- **Cosa:** nell'organigramma l'agente vocale è quello «che risponde alle chiamate».
- **Parte da:** una chiamata. [non verificato: la TR non dice se si tratta solo di chiamate in entrata]
- **Agisce:** l'agente vocale.
- **Persona:** nessuno durante la chiamata.
- **Esterno:** telefono.
- **Impara:** vedi AU-33.
- **Livello:** L3, per come è descritto.

[verificato: TR 16:37-16:40]

**AU-35 — I contatti chiusi vengono analizzati e l'analisi va al marketing.**
- **Cosa:** un sistema analizza tutti i dati sul perché un contatto si è chiuso e cerca come ripetere quel risultato su altri. L'analisi va direttamente al marketing, che la usa per migliorare le campagne.
- **Parte da:** i contatti chiusi.
- **Agisce:** il sistema di analisi.
- **Persona:** il marketing riceve l'analisi e cambia le campagne.
- **Esterno:** nessun effetto diretto.
- **Impara:** sì, a livello di azienda.
- **Livello:** L3 int. per l'analisi e la consegna; L0 per le campagne.

[verificato: TR 16:06-16:17]

### Altri agenti e automazioni

**AU-36 — Agente delle newsletter.**
- **Cosa:** nell'organigramma c'è l'agente «che costruisce le newsletter».
- **Parte da:** n.d.
- **Agisce:** l'agente.
- **Persona:** c'è un responsabile in organigramma; il suo ruolo è n.d.
- **Esterno:** newsletter agli iscritti. [non verificato: la TR non dice se l'agente le invia]
- **Impara:** n.d.
- **Livello:** n.d.

[verificato: TR 16:30-16:38]

**AU-37 — Acquisti automatizzati.**
- **Cosa:** chi lavora in finanza ha automatizzato i processi di acquisto. È uno degli esempi citati per il premio mensile a chi costruisce qualcosa con l'AI.
- **Parte da, agisce, persona, esterno:** n.d. [non verificato: la TR non dice fin dove arriva l'automazione, né se tocca ordini o pagamenti]
- **Impara:** n.d.
- **Livello:** n.d.

[verificato: TR 18:36-18:50]

**Sintesi dei livelli.** Gli AU sono 37:
- **25 sono L3.** 15 restano dentro l'azienda. 10 hanno effetti all'esterno: AU-03, 04, 08, 10, 11, 12, 31, 32, 33 e 34.
- **6 sono L0:** AU-14, 15, 19, 20, 24 e 26.
- **6 hanno il livello non detto:** AU-01, 02, 21, 22, 36 e 37.
- **Nessuno è L1 o L2.** La TR non descrive mai un'approvazione prima di un'azione, né una finestra di tempo per fermarla. [verificato: TR letta per intero]

### Cose della TR che non sono comportamenti autonomi

- **Dettatura al posto della tastiera** → C4. [verificato: TR 6:02-6:07]
- **Tempo e costi:**
  - servono «qualche centinaio» di ore per imparare → E1 [verificato: TR 9:28-10:00];
  - conviene costruire ora, finché i token costano poco → E2 [verificato: TR 10:23-10:37];
  - policy AI e banca dei token, citate dalla voce fuori campo → E3 [verificato: TR 10:37-10:54];
  - bisogna formarsi → E4, H1 [verificato: TR 10:54-11:00; 16:54-17:14].
- **AI per tutti, non solo per i tecnici** → F5. [verificato: TR 13:20-13:33]
- **Agenti in organigramma:** sono più di 100, e una persona può avere cinque riporti umani e 25 agenti. La TR lo chiama un superpotere per la persona e per l'azienda → G9, G10. [verificato: TR 16:17-16:48]
- **Adozione:** sperimentare; il cambiamento non si può delegare; valutazione delle competenze per reparto; ambassador con più risorse; esempio dall'alto e prove dal basso; premio mensile; le licenze da sole non bastano → H1-H7. La TR non dice che la valutazione delle competenze sia automatica. [verificato: TR 17:14-19:03]
- **Qualità:** il contesto fa la qualità; non bisogna fermarsi alle slide nel formato standard che usano tutti → I1, I2, K7. [verificato: TR 19:39-20:03]
- **Limiti:** ci sono aree in cui l'azienda ha deciso di non usare l'AI. Il marketing oggi è al 70% lavoro ripetitivo, e l'obiettivo è ribaltare la proporzione → I3, I4. [verificato: TR 21:14-22:04]
- **Processo degli eventi e processo della formazione rifatti dai dipendenti con l'AI.** La TR non dice cosa fanno né se partono da soli. Nessuna voce di VF li copre in modo specifico (vedi §3). [verificato: TR 18:50-18:58]

## 2. Tabella AU → voci di VF

[verificato: VF, tutte le sezioni J, A-I, K, L]

| AU | Livello nella TR | Voci VF | Copertura | Nota |
|---|---|---|---|---|
| AU-01 | n.d. | K14, A2 | piena | — |
| AU-02 | n.d. | K16 | parziale, per scelta | VF lo rende facoltativo e tiene i dati di salute fuori dalla memoria aziendale; nella TR la memoria personale e quella aziendale sono la stessa |
| AU-03 | L3 online, L0 dal vivo | A1, J5, C2 | piena | — |
| AU-04 | L3 | C2, J5, A1 | piena | — |
| AU-05 | L3 int. | A5, A3, A4 | piena | — |
| AU-06 | L3 int. | A6 | piena | — |
| AU-07 | L3 int. | A7, J4 | piena | A7 aggiunge che la chat è leggibile dalle persone |
| AU-08 | L3 | K2 | piena | — |
| AU-09 | L3 int. | A7 | parziale | A7 chiude i to-do già fatti, ma non prevede momenti di scambio ricorrenti fra agenti |
| AU-10 | L3 | B1, B5, J9 | piena come traguardo | in VF il flusso senza mani arriva alla fine di un percorso (B5); nella TR è già attivo |
| AU-11 | L3 | B2, B5 | piena come traguardo | come AU-10 |
| AU-12 | L3 | B3, B5 | piena come traguardo | come AU-10; è l'unica mail al cliente che la TR descrive come autonoma |
| AU-13 | L3 int. | B4, B5, J8 | piena come traguardo | come AU-10 |
| AU-14 | L0 | C1, K1 | piena | VF lo estende a ogni persona |
| AU-15 | L0 | C3, K4 | piena | — |
| AU-16 | L3 int. | C5, C3, K4, A1 | piena | — |
| AU-17 | L3 int. | C6, A2, I2 | piena | — |
| AU-18 | L3 int. | D1, K8 | piena | — |
| AU-19 | L0 | D2, D3, J6 | parziale | D2 parte dall'email; nessuna voce dice che il brief parte da solo per ogni incontro in agenda, né che usa anche dati personali |
| AU-20 | L0 | D4, K6, J6, K7 | piena | — |
| AU-21 | n.d. | D5, J6 | piena sulla funzione | né la TR né VF dicono il livello |
| AU-22 | n.d. | K3, B3 | parziale | K3 parla di «risposte pronte», cioè di preparazione; la TR dice solo che non risponde più lui |
| AU-23 | L3 int. | F1, K13 | piena | — |
| AU-24 | L0 | F1, F4 | parziale | nessuna voce copre i suggerimenti alla singola persona su come usa gli strumenti |
| AU-25 | L3 int. | F2, K13 | parziale | F2 non dice se l'intervista la conduce un agente |
| AU-26 | L0 | F3, F4, K13 | piena | le automazioni consigliate nell'esempio corrispondono a D4/K7, B3 e K5 |
| AU-27 | L3 int. | G1, J9 | piena | — |
| AU-28 | L3 int. | G2 | piena | — |
| AU-29 | L3 int. | G3, K12 | piena | — |
| AU-30 | L3 int. | G4, K12 | parziale, per scelta | G4 manda al responsabile solo il dato aggregato; nella TR il responsabile riceve il report di ogni call |
| AU-31 | L3 | G5, G7, K5 | piena, manca un dettaglio | G5 non dice che la voce è quella registrata di un collega |
| AU-32 | L3 | G5, K10 | piena | — |
| AU-33 | L3 | G6, A6 | piena | né la TR né VF dicono se la nuova apertura passa prima da una persona |
| AU-34 | L3 | K10 | piena | — |
| AU-35 | L3 int. (campagne L0) | G8, K11, J7 | piena | — |
| AU-36 | n.d. | K9 | piena sulla funzione | livello non detto |
| AU-37 | n.d. | K15 | piena sulla funzione | livello non detto; con i limiti fissi del progetto si ferma prima del pagamento |

## 3. AU che nessuna voce copre

- **Nessun AU resta senza voce.** Ogni comportamento autonomo della TR ha almeno una voce in VF.
- **8 AU sono coperti solo in parte:**
  - AU-02 e AU-30, per scelta del progetto: i dati personali restano separati e al responsabile arriva solo il dato aggregato;
  - AU-09: mancano i momenti di scambio ricorrenti fra agenti;
  - AU-19: manca il brief che parte da solo per ogni incontro in agenda;
  - AU-22: non è chiaro il livello delle risposte alle mail;
  - AU-24: mancano i suggerimenti alla singola persona;
  - AU-25: non è detto che l'intervista la conduca un agente;
  - AU-31: manca la voce registrata di un collega.
- **4 AU sono coperti come traguardo:** AU-10, 11, 12 e 13. Nella TR il flusso dopo la call è già L3; in VF ci si arriva alla fine del percorso (B5).
- **Due funzioni non hanno una voce e non sono descritte come autonome:** il processo degli eventi e quello della formazione, rifatti con l'AI [verificato: TR 18:50-18:58]. Le segnalo perché nessuna funzione vada persa. La voce L10 riguarda gli eventi che portano contatti, non il processo interno degli eventi. [verificato: VF §L]
- **Alcune voci di VF non hanno un AU:**
  - J1-J3, C4, E1-E4, F5, G9, G10, H1-H7 e I1-I4 vengono da principi o pratiche della TR, non da comportamenti autonomi;
  - L1-L12 sono automazioni in più, proposte dallo studio del 25 ottobre, e non compaiono nella TR. [verificato: VF intestazione; TR letta per intero]

## 4. Principi di autonomia che la TR mostra

1. **Il contesto è il carburante.** Tutto viene registrato e trascritto, dichiarandolo. Più contesto hanno gli agenti, più possono dare consigli o «lavorare al posto nostro». [verificato: TR 2:17-2:58; 19:46-19:55] → A1, I1
2. **Due memorie e un orchestratore proprio.** Un database relazionale per le informazioni fisse e uno vettoriale che collega i momenti. Sopra c'è un orchestratore open source installato su una macchina propria, fra la memoria e modelli di più fornitori. [verificato: TR 3:00-3:39] → A2, A3, A4
3. **Un agente per ogni compito.** L'imprenditore ha 25 agenti, l'azienda più di 100. Alcuni lavorano sempre in sottofondo (raccolta, pulizia, indicizzazione), altri agiscono. [verificato: TR 3:39-3:53; 16:17-16:37] → A5, J3
4. **Gli agenti si parlano in una chat comune.** Il lavoro passa da un agente all'altro con un messaggio, senza che una persona lo smisti. [verificato: TR 3:59-4:18] → A7, J4, K2
5. **Gli agenti si correggono a vicenda.** Nei momenti di scambio comune si aiutano e chiudono i to-do superati, come un team di persone. [verificato: TR 4:18-4:29] → A7
6. **Il lavoro ripetitivo va da solo, anche verso il cliente.** Dopo ogni call, canale del cliente, CRM, mail di follow-up e to-do partono senza intervento. L'imprenditore non fa più i follow-up e non risponde più alle mail a mano. [verificato: TR 4:40-5:07; 9:41-9:52] → B1-B5, K3
7. **Velocità e continuità.** Il contatto viene richiamato in 90 secondi invece che in 2 ore, a qualsiasi ora e in qualsiasi giorno. Secondo la TR, la conversione dei commerciali è raddoppiata. [verificato: TR 14:53-14:57; 15:50-16:02] → G5, G7
8. **Gli agenti imparano dall'esito.** Imparano da soli. L'agente vocale cambia l'apertura dopo i rifiuti. I contatti chiusi insegnano qualcosa al marketing. I dati aziendali servono a migliorare i processi. [verificato: TR 0:15-0:24; 3:53-3:59; 15:31-15:43; 16:06-16:17] → A6, G6, G8, K11, K14
9. **Il sistema dice cosa automatizzare dopo.** La mappa dei processi stima le ore nascoste e consiglia le automazioni da fare. [verificato: TR 12:36-13:20] → F3, F4
10. **Le regole si scrivono una volta e si leggono ogni volta.** La persona fissa come vuole i risultati. Gli agenti cercano da soli queste regole prima di lavorare. [verificato: TR 6:59-7:12] → C6
11. **Dentro l'azienda tutto è visibile.** Le call di vendita finiscono in un canale dove ci sono tutti. Il registro dei meeting mostra a ciascuno anche quelli degli altri. Dopo ogni call il report va al venditore e al responsabile. [verificato: TR 6:13-6:30; 13:53-14:01; 14:36-14:43] → C5, G1, G4
12. **Trasparenza verso l'esterno e privacy.** La registrazione è dichiarata e, dal vivo, avviene solo con il permesso. L'agente vocale dice di essere un'AI. La mappatura legge i metadati, non il contenuto dei file. [verificato: TR 2:17-2:27; 14:57-15:01; 12:10-12:16] → A1, G5, F1
13. **Ogni agente ha un responsabile umano.** Gli agenti stanno in organigramma: una persona può avere cinque riporti umani e 25 agenti. [verificato: TR 16:22-16:37] → G9, J2
14. **La relazione con il cliente resta umana, per scelta.** L'agente vocale passa la persona a un commerciale reale. Brief e slide preparano chi incontra il cliente. Ci sono aree in cui l'azienda ha deciso di non usare l'AI. Nel marketing l'AI si prende il lavoro ripetitivo e lascia alle persone quello creativo. [verificato: TR 8:36-8:44; 15:07-15:14; 21:14-22:04] → I3, I4
15. **Banca dei token e policy AI.** Ognuno sa quanti token può usare. Conviene costruire ora, finché costano poco. [verificato: TR 10:23-10:54, in parte voce fuori campo] → E2, E3
16. **L'autonomia cresce dal basso.** Tutti sperimentano e costruiscono. Ogni mese un premio va a chi ha costruito con l'AI la cosa che ha cambiato di più l'azienda, per esempio gli acquisti automatizzati. [verificato: TR 18:27-18:58] → H5, H6, K15
17. **Il controllo sta prima e dopo l'azione, non durante.** La TR non descrive mai un'approvazione prima di un'azione, né una finestra per fermarla, neanche per la mail al cliente. Il controllo sta prima: regole scritte, registrazioni dichiarate, aree escluse. E sta dopo: canali, registri, report, organigramma, test continui sull'agente vocale. [verificato: TR letta per intero; 5:03-5:07; 6:59-7:12; 15:31-15:34; 16:22-16:37]
18. **Quello che la TR non dice.** La TR non parla di cancellazioni, credenziali, pagamenti, stop di emergenza, tetti per singolo agente, registro delle azioni, revoca o gestione degli errori [verificato: TR letta per intero]. Nel progetto questi limiti restano fissi:
    - cancellazioni e credenziali sempre negate agli agenti, pagamenti mai automatici [verificato: docs/03-architettura.md §4 e §4.1];
    - stop di emergenza dal telefono [verificato: docs/03-architettura.md §4.3].

    Per AU-37 questo significa che l'automazione degli acquisti si ferma prima del pagamento.
