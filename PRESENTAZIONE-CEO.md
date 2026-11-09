% SerSan Agent OS
% Il secondo cervello di SerSan: quattro persone e una squadra di agenti
% Proposta di progetto per Alessandro Serratt e Michele Sanna · preparata da Alberto Tuveri · versione 2.1 · 8 novembre 2026 · documento interno

# 1. In breve

**Cosa proponiamo.** Costruire per SerSan un "secondo cervello" aziendale: SersanOutreach, marketing, contenuti, task, progetti e chiamate con i clienti diventano un solo sistema. Tutto quello che diciamo, scriviamo e decidiamo entra in una memoria aziendale, e 57 agenti AI, divisi in nove squadre, lavorano su quella memoria insieme a noi. Entrano in ogni call e la trascrivono, preparano brief e slide prima e dopo gli incontri, scrivono i follow-up, aggiornano il CRM, fissano gli appuntamenti, rispondono alla posta, propongono offerte e contratti, tengono il calendario dei post e la newsletter, richiamano le lead, preparano le fatture e ci mandano ogni mattina il punto della giornata. Gli agenti si parlano tra loro in una chat di gruppo che leggiamo anche noi: Teams, che abbiamo già con M365, con Telegram, Slack e WhatsApp collegati e Buzz in prova sul nostro server. Nessun agente manda niente a un cliente senza il sì di una persona o una regola "Sempre" che avete approvato voi. Fa eccezione "Andrea", che al telefono dice subito di essere un assistente AI e richiama da solo soltanto chi lo ha chiesto nel modulo (decisione 10).

**Come è fatto.** Tutto gira sul nostro server, dentro l'infrastruttura che Michele ha disegnato: in cloud restano solo i servizi del suo board, cioè M365, Claude Team, le API di Anthropic, Jira, Instantly, una piccola macchina Oracle a Milano per l'accesso da fuori e pochi altri. Fuori dal board restano poche eccezioni, da approvare una per una: la linea telefonica di Andrea, WhatsApp, Telegram, Slack per i clienti, l'invio della newsletter e alcuni strumenti commerciali (decisioni 8-10 e 15). Il motore degli agenti lo costruiamo noi con l'Agent SDK di Claude, la stessa tecnologia di Claude Code: è la strada che Michele preferisce ed è anche quella che ha vinto il confronto con Hermes (sezione 5.7). Gli agenti ragionano con Claude passando da LiteLLM, che tiene i budget. La memoria resta in casa. Tutto ciò che esce verso l'esterno passa da un nostro "Cancello" di approvazioni, che registra ogni azione. SersanOutreach si sposta da Azure al server e diventa il CRM degli agenti. Il piano marketing diventa il loro primo lavoro.

**Perché ora.**

- **È quello che vendiamo.** Le nostre linee 02 (Workflow Automation) e 03 (AI Features & Reliability) promettono ai clienti agenti che agiscono entro limiti decisi da loro. Costruirlo per noi è il caso studio più credibile che possiamo mostrare, e un'offerta che possiamo rivendere alle PMI del nostro ICP.
- **Abbiamo già quasi tutto.** Cinque posti Claude Team, i crediti API Anthropic, M365 con Teams, SersanOutreach con i suoi due server MCP già pensati per gli agenti, e un server già completo: 192 GB di RAM, 64 thread, dischi in mirror e una GPU, in un rack con firewall e UPS già comprati, dentro l'infrastruttura disegnata da Michele.
- **Il funnel ha bisogno di mani.** Oggi SersanOutreach ha 11 lead, 1 risposta e 0 meeting; il calendario marketing ha 96 slot, 3 pezzi pubblicati verificati al 13 ottobre e altri 5 programmati fino al 22 ottobre; il marketing operativo è senza titolare dal 30 settembre. Il sistema è l'addetto che manca, e non si stanca. Per questo partiamo da ciò che rende già con i numeri di oggi (Claude Team usato bene da tutti, post, follow-up delle call, decisione sull'email), mentre "Andrea" e la pipeline pesata aspettano che ci siano lead vere (sezione 11).

**Cosa costa.** Il dettaglio è nella sezione 12. Con tutto sul nostro server spendiamo meno di quanto previsto nella prima versione: escono Slack Pro come chat interna, Notion, Recall.ai, ElevenLabs, Hermes Cloud, il password manager e i backup in cloud; Slack resta solo per i clienti che lavorano lì. Quello che spendiamo **in più** rispetto a oggi:

| Periodo | € al mese in più | Cosa comprende |
|---|---|---|
| Fasi 0-1 e inizio della fase 2, finché Azure resta accesa | ≈ 135 (circa 141 se servisse un server a pagamento per l'accesso) | Abbonamento di Proxmox, il sistema che fa girare le macchine virtuali sul server (20), IP fisso (fino a 10), corrente del rack (≈ 105), la macchina Oracle per l'accesso da fuori (0 € sul piano gratuito di Oracle; 6,49 € se servisse un server a pagamento) |
| Fase 2 (settimane 9-21), con Azure spenta | da ≈ -15 a ≈ +20 | Azure spenta fa risparmiare circa 150 €; Jira Standard, se serve |
| Fasi 3-4 (settimane 22-40) | da ≈ -1 a ≈ +70 | WhatsApp con numero dedicato, Slack, invio della newsletter, corrente della RAM in più |
| Fasi 5-6 (dalla settimana 41) | da ≈ 46 a ≈ 168 | Si aggiunge la linea telefonica italiana di "Andrea" (44-90 €) |

- Le **API di Claude** per gli agenti (stima 90-250 € al mese) dovrebbero stare dentro i crediti del bundle startup, di cui verifichiamo importo e scadenza nella prima settimana; se non bastano le paghiamo noi, con un tetto a 250 €.
- **Claude Team** è gratuito per il primo anno grazie al bundle; alla scadenza decidiamo quanti posti tenere (fino a 447 € al mese). Gli agenti usano la chiave API, quindi potremo tenere meno posti premium.
- Gli **strumenti commerciali** che usiamo oggi e che il board di Michele non cita (Apollo, Metricool, Apify, moda.app, Higgsfield, Perplexity) li decidete voi caso per caso (decisione 15): una parte si sostituisce con strumenti sul nostro server.
- **Una tantum, oggi**: parere legale (tetto 2.500 €), il credito API se serve (circa 223 €) e le spese del board che conviene fare subito: il backup in sede, cioè case e dischi per la macchina che Michele monta con pezzi suoi (circa 165-500 €), chiavi di sicurezza FIDO2 (232-464 €), piccoli accessori (fino a 200 €). In tutto al massimo circa 3.890 €, più circa 140-550 € per le batterie nuove dell'UPS se il test di autonomia all'arrivo va male. Più avanti: la copia dei backup a casa di Michele (entro marzo 2027), RAM in più, la seconda GPU con il pezzo che serve a montarla, una linea internet di riserva e una revisione esterna di sicurezza (sezione 12.2). L'hardware principale è già comprato, compresi firewall e UPS da rack.
- **Il costo vero è il nostro tempo di sviluppo**: la stima in giorni, fase per fase, è nella sezione 15.

**Cosa vedete in 8 settimane.** Tutti e quattro lavoriamo ogni giorno in Claude Team, con le skill e i template SerSan per offerte, slide e recap. La decisione sull'email è presa e la casella è attiva. SersanOutreach è sicuro su identità e MFA. Il calendario dei post è pieno fino a Natale e i numeri del lunedì li compila una skill di Claude Team; dalla fase 2 lo fa l'Analista metriche. E il primo pezzo del sistema di agenti funziona: dopo ogni call in Teams il riassunto con i prossimi passi arriva nel canale interno e la bozza della mail di follow-up arriva sul telefono come carta, pronta da correggere e approvare; dopo il sì parte una volta sola. Ogni mattina alle 7:00 ognuno di noi riceve il suo debrief.

**Cosa vi chiediamo oggi.** Tre decisioni, più le altre della sezione 14:

1. Il via alle fasi 0 e 1, cioè le prime otto settimane, con una verifica alla settimana 8 su criteri tecnici e commerciali. Il lavoro lo portano avanti Alberto, Mattia e Michele; ad Alessandro chiediamo l'assessment iniziale, le sue regole di lavoro, il punto del venerdì e le approvazioni dal telefono. Alla settimana 8 decidete voi se finanziare la fase 2: se ci fermiamo, restano Claude Team usato bene da tutti, SersanOutreach sistemato, la decisione sull'email e il calendario dei post.
2. Nessun abbonamento nuovo oltre a quelli del board di Michele: Proxmox (20 € al mese), l'IP fisso (fino a 10 €), la macchina Oracle per l'accesso da fuori (0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento) e, se Michele li sceglie, gli abbonamenti Proxmox per firewall e backup (fino a circa 103 € al mese, decisione 17).
3. Il budget una tantum delle prime otto settimane: il parere legale unico (tetto 2.500 €, con due preventivi), da chiedere subito perché la parte sull'email serve già nella fase 0; il credito API se serve (circa 223 €); le spese del board che conviene fare subito (backup in sede, chiavi FIDO2, accessori). In tutto circa 2.900-3.890 €, contro i 5.016 € della prima versione, più circa 140-550 € per le batterie nuove dell'UPS se il test di autonomia all'arrivo va male.

# 2. L'idea

## 2.1 Un'azienda di quattro persone con una squadra di agenti

L'idea è semplice da dire: **tutto quello che facciamo per vendere, comunicare e consegnare diventa un solo sistema**, e una squadra di agenti AI lo fa girare insieme a noi. SersanOutreach, il marketing, la generazione dei contenuti, i task, i progetti e le chiamate con i clienti non sono più strumenti separati che qualcuno deve ricordarsi di aggiornare: sono collegati, e ogni pezzo è affidato a una squadra di agenti con un compito preciso e un responsabile umano.

Le squadre si parlano come farebbe un team di persone:

- la squadra **Outbound** ha un agente per le email, uno per LinkedIn e uno che sorveglia i segnali. Quando un prospect risponde, l'agente email passa il contatto all'agente dei **brief** e a quello delle **proposte**, che lavorano con quello delle **chiamate**;
- l'agente delle **chiamate** entra automaticamente in ogni call del calendario, dichiarandolo, e trascrive tutto; l'agente **agenda** fissa gli appuntamenti che emergono da call, mail e chat;
- l'agente dei **brief** prepara il brief prima della chiamata e quello dopo, con tutto il contesto della call, e chiede allo **Studio contenuti** le slide: per noi prima dell'incontro, per il cliente dopo;
- la squadra **Marketing** lavora con l'Outbound: ricerca la concorrenza, misura cosa funziona, trasforma le obiezioni sentite in call in contenuti, e chiede allo Studio video, slide e post;
- la squadra **Progetti** prende in carico il cliente quando firma: piano, task, avanzamento, report, assistenza, rinnovi e, a fine progetto, il caso studio per il Marketing;
- la squadra **Amministrazione** chiude il giro: fattura alla consegna, incassi, acquisti e abbonamenti, numeri confrontati con gli obiettivi, bandi e finanziamenti;
- dietro tutte, la squadra **Memoria** tiene il contesto e la squadra **Direzione** tiene le regole, la banca dei token, la posta in arrivo e il debrief di ogni mattina.

Tutto si vede in una **chat di gruppo**: la casa comune è **Teams**, che abbiamo già con M365. Ogni squadra ha il suo canale e un bot con il nome dei suoi agenti, e noi entriamo dal computer o dal telefono. Dalla fase 3 gli stessi agenti arrivano anche su **Telegram** (avvisi), **WhatsApp** e **Slack** (soprattutto per i clienti); le approvazioni restano in Teams, dove il Cancello riconosce chi preme; **Buzz**, la chat di Block fatta per persone e agenti, è in prova sul nostro server: quando supera le prove diventa la stanza degli agenti, che intanto è il canale "Agenti" di Teams.

## 2.2 Le funzioni che lo rendono un secondo cervello

1. **Contesto totale.** Ogni riunione, in call o dal vivo, viene registrata dichiarandolo e trascritta, e diventa memoria che gli agenti possono usare.
2. **Due memorie, sul nostro server.** Una relazionale (BookStack e PostgreSQL: processi, obiettivi, regole di lavoro di ciascuno, catalogo) e una vettoriale che collega i momenti (trascrizioni, mail, documenti).
3. **Un motore degli agenti sul nostro server**, costruito con l'Agent SDK di Claude, tra la memoria e i modelli, che coordina gli agenti.
4. **Il flusso commerciale senza mani.** Dopo una call: punti e prossimi passi nel canale del cliente, opportunità nel CRM, mail di follow-up, task al team.
5. **La giornata.** Debrief del mattino, anche come primo evento del calendario; un agente in ogni call anche al posto di chi manca; dettatura; riassunti scritti secondo le regole di ciascuno; domande libere alla memoria, come «cosa si è detto nella call di ieri con quel cliente?».
6. **La pipeline pesata** sullo storico reale, non a sensazione.
7. **Prima e dopo l'incontro.** Brief di intake per ogni nuova richiesta; brief prima e dopo la call; slide per noi e per il cliente, con la storia della relazione con noi; offerta commerciale costruita sul nostro catalogo e su ciò che il cliente ha detto; contratto dal nostro modello.
8. **La mappa dei processi**, con le ore che spendiamo e le automazioni da fare per prime; la stessa mappa, con l'assessment, diventa un servizio per i nostri clienti.
9. **Le vendite che si allenano.** Valutazione delle call di vendita con consigli a chi le ha fatte e un piano di allenamento ogni mese; un agente vocale, "Andrea", che richiama entro 90 secondi ogni lead che lo chiede, 24 ore su 24, risponde alle chiamate quando nessuno può, si dichiara AI e fissa l'appuntamento con uno di noi; dai clienti vinti, la ricerca di aziende simili.
10. **Gli agenti in organigramma**, ognuno con un responsabile e un costo, fino a cento.
11. **La governance.** Banca dei token, premio mensile a chi costruisce con l'AI, aree in cui l'AI per scelta non entra.
12. **Il marketing che non si ferma.** Calendario dei post, newsletter, sito, webinar ed eventi, risposte ai commenti sulla pagina aziendale; ciò che si sente in call diventa contenuto.
13. **La posta e l'agenda.** Un agente smista tutta la posta in arrivo e prepara le risposte; un altro fissa e sposta gli appuntamenti.
14. **Dalla firma all'incasso.** Contratto, apertura del progetto, fattura alla consegna, incassi e solleciti, rinnovi, caso studio.
15. **I numeri dell'azienda.** Dati finanziari e obiettivi nella memoria, accanto a processi e regole; ogni mese margini per cliente e per progetto, cassa e distanza dagli obiettivi; bandi e finanziamenti da non perdere.
16. **Un assistente personale, per chi lo vuole.** Calendario personale, viaggi, famiglia. I dati di salute restano nell'account privato di chi sceglie di usarli, mai nella memoria aziendale.

L'appendice A elenca ogni funzione con il componente che la realizza e la fase in cui arriva.

## 2.3 Perché è giusto per SerSan

Siamo quattro. Ogni ora spesa in follow-up, brief, proposte, post e report è un'ora tolta alla consegna o alla vendita, e non abbiamo nessuno a cui delegarla. Costruire adesso, mentre i token costano poco e mentre impariamo, è un vantaggio: chi impara a lavorare con gli agenti prima degli altri vende e consegna di più.

C'è poi un motivo commerciale. Il nostro profilo promette "agenti che agiscono, con i limiti che decidi tu", "testati su casi reali prima del rilascio", "monitorati su costo e qualità". Un sistema così, in uso ogni giorno da noi, è la prova migliore che sappiamo farlo. E diventa un'offerta: la stessa architettura, installata e gestita per una PMI, è un progetto di Workflow Automation con un canone di gestione.

## 2.4 Cosa cambia, in concreto

| Oggi | Con il sistema |
|---|---|
| Dopo una call: appunti, mail, CRM e to-do a mano, quando si trova il tempo | Entro pochi minuti: riassunto con i prossimi passi, opportunità aggiornata, bozza di follow-up pronta per il sì, to-do assegnati |
| Prima di un incontro: ricerca sul cliente fatta di corsa o non fatta | Brief completo e slide la sera prima, a partire dall'email della persona |
| Proposte scritte da zero, ogni volta | Bozza dal catalogo servizi, dalla trascrizione e dal brief, da rifinire e firmare |
| Pipeline "a sensazione", 91 deal senza un valore | Probabilità di chiusura pesata sullo storico, con intervallo dichiarato |
| Lead che aspettano ore | Richiamo entro 90 secondi, 24/7, con appuntamento fissato con uno di noi |
| Post prodotti a sprazzi, coda vuota dopo il 22 ottobre | Calendario pieno, bozze secondo le direttive, pubblicazione dopo il sì, numeri il lunedì |
| Conoscenza nelle teste e nelle chat | Memoria aziendale interrogabile da tutti, con le regole di lavoro di ciascuno |
| Appuntamenti fissati a colpi di mail; posta smaltita la sera | L'agente agenda propone gli orari e manda l'invito; la posta arriva smistata, con le risposte pronte per il sì |
| Fatture e solleciti quando qualcuno se ne ricorda | Fattura pronta alla consegna, solleciti dopo il sì, margini per cliente nel report del mese |
| Nessuna idea di quanto costa l'AI | Banca dei token: budget per persona e per agente, con tetti che fermano davvero |

# 3. Una giornata con il sistema

Per rendere l'idea, ecco un martedì qualunque a sistema avviato.

**7:00.** Alessandro apre Teams. Il debrief gli dice che ieri sono arrivate due risposte positive da SersanOutreach, che alle 11 ha una call con un prospect del settore energia e che il brief è pronto, che tre carte aspettano il suo sì e che la campagna email ha speso il 40% del tetto mensile. Michele riceve il suo: un'offerta da firmare, un'affermazione tecnica in un post da verificare, lo stato del server. Alberto e Mattia ricevono i loro. La posta della notte è già smistata: due risposte pronte da approvare, la fattura di un fornitore registrata, il resto archiviato.

**8:30.** Alessandro legge il brief del prospect: chi è l'azienda, cosa ha pubblicato negli ultimi mesi, chi sarà in call e che ruolo ha, lo storico dei contatti con noi (una mail aperta tre volte a settembre, un commento a un post di Michele), tre segnali e due possibili problemi da cui partire. In allegato le slide di presentazione con il nostro template.

**11:00-11:45.** La call. Il bot di registrazione entra, si presenta, e il prospect sa fin dall'invito che verrà registrata.

**11:55.** Nel canale interno del cliente compare il riassunto, scritto nel formato che Alessandro ha definito nelle sue regole: decisioni, prossimi passi con un nome e una data, rischi. In Jira ci sono i to-do. Nel CRM il meeting è registrato e il deal ha un valore stimato. Sul telefono di Alessandro arriva una carta: "Bozza di follow-up al cliente. Approva, modifica o rifiuta". Lui corregge una frase e approva. La mail parte.

**12:10.** Nella sala macchine, cioè il canale `#agenti` che chiunque può leggere, l'Agente proposte scrive: "Ho una bozza di proposta in due fasi per il cliente energia, la passo a Michele per la firma tecnica". La bozza è costruita sul nostro catalogo e su ciò che il cliente ha detto in call.

**12:20.** L'Agente agenda propone al prospect tre orari per la seconda call, presi dai calendari di Alessandro e Michele. L'invito parte dopo il sì e porta già l'avviso di registrazione.

**15:00.** L'Editoriale propone tre temi per i post di giovedì. Uno nasce da un'obiezione che il prospect ha fatto in call: "a volte la risposta onesta è costruire meno". Il Copywriter prepara le bozze in inglese e italiano, già controllate contro le regole di brand. Alessandro sceglie e approva.

**16:30.** Il progetto di un cliente chiude una milestone. L'Agente fatture prepara la fattura, l'Agente casi studio propone la bozza del caso studio e l'Agente rinnovi segnala che in call il cliente ha parlato di un secondo reparto: un'opportunità per la fase successiva. Tre carte per Michele.

**17:30.** Una lead compila il modulo sul sito e chiede di essere richiamata. Alle 17:31 "Andrea" la chiama, dice subito di essere un assistente virtuale di SerSan, capisce il problema, e fissa una call con Alessandro per giovedì. L'esito è già nel CRM e nel canale delle vendite. Alle 21:10 un'altra lead chiama il numero aziendale: risponde "Andrea" e fissa la call per venerdì.

**Venerdì.** Il report settimanale dice quante ore hanno lavorato gli agenti, quanto sono costati, quante carte abbiamo approvato senza modifiche. Le approvazioni che si ripetono identiche diventano candidate a una regola "Sempre": Alessandro ne attiva una, e da lunedì l'invito per la seconda call a chi ha già parlato con noi parte da solo.

# 4. Cosa costruiamo: nove squadre, quasi sessanta agenti

Il progetto copre ogni funzione dell'idea. Gli agenti sono divisi in nove squadre e **ogni squadra ha un responsabile umano**: un agente senza un responsabile è un agente senza controllo. La colonna "Fase" dice quando arriva (il piano è nella sezione 11).

## 4.1 Squadra Outbound (responsabile: Alessandro; tecnico: Alberto)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Agente email** | Gestisce le sequenze email su Instantly, legge le risposte, le classifica e propone la risposta da approvare. Quando un prospect è interessato passa il contatto all'agente brief e a quello delle proposte | 3 |
| **Agente LinkedIn** | Prepara inviti e messaggi su LinkedIn, sempre con l'approvazione di una persona, e segue le conversazioni | 3 |
| **Sentinella segnali** | Assunzioni, finanziamenti, cambi di ruolo, post pubblicati, commenti qualificati ai nostri post: propone il contatto giusto al momento giusto | 3 |
| **Operatore outbound** | Fa girare SersanOutreach: import, qualificazione, coda di approvazione, campagne | 3 |
| **Agente clienti simili** | Dai clienti vinti e da ciò che ha capito l'Analista vinto/perso cerca aziende simili e le passa all'Operatore: si replica ciò che funziona | 5 |

## 4.2 Squadra Chiamate (responsabile: Alessandro)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Agente chiamate** | Entra in ogni call del calendario, anche al posto di chi manca, dichiarandolo: nelle nostre call Teams prende la trascrizione di Microsoft; in quelle dei clienti (Teams di altri, Meet, Zoom) entra un bot sul nostro server e trascrive tutto in casa. Registra anche le riunioni dal vivo dal telefono | 3 (nella fase 1 le trascrizioni delle call Teams le legge già il Post-call) |
| **Analista chiamate** | Scrive il riassunto **secondo le regole di ciascuno**, lo mette nel registro di tutti i meeting, consultabile da tutti, e ne estrae la pipeline ("chi è caldo entro quando") | 1 |
| **Post-call** | Punti e prossimi passi nel canale del cliente, meeting e opportunità nel CRM, bozza di follow-up, task alla squadra Progetti | 1 (riassunto e bozza della mail), 2 (CRM e task in Jira) |
| **Agente agenda** | Fissa gli appuntamenti che emergono da call, mail e chat: quando il Raccoglitore trova nuove call da fissare, propone gli orari liberi di chi deve esserci, manda l'invito con l'avviso di registrazione dopo il sì, sposta e ricorda | 3 |
| **Dettatura** | Trascrive la voce in italiano e in inglese, dal telefono e dal PC | 2 |

## 4.3 Squadra Vendite (responsabile: Alessandro)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Agente brief** | **Prima della call**, dall'email della persona: azienda, dati pubblici, chi è in call, storico della relazione, ultime mail, post LinkedIn recenti (con una via consentita), segnali, concorrenti (dalla squadra Marketing), opportunità comuni. **Dopo la call**: brief con tutto il contesto, decisioni, obiezioni, prossimi passi. Chiede allo Studio le slide per noi e per il cliente, che raccontano anche la storia della relazione con noi | 3 |
| **Agente proposte** | Dopo l'incontro: catalogo SerSan più trascrizione più brief, una bozza di proposta a fasi con scope e prezzo da confermare; la firma tecnica è di Michele | 3 |
| **Pipeline** | Probabilità di chiusura pesata sullo storico di call e deal, con un intervallo onesto; un portale clienti costruito con Claude Code sopra SersanOutreach, con pipeline, pipeline pesata e storico di ogni cliente | 5 |
| **Coach vendite** | Dopo ogni call di vendita: fit del prospect, punti di forza, cosa migliorare, consigli pratici. Lo vede chi ha fatto la call; al responsabile vanno i dati aggregati. Ogni mese un piano di allenamento sui temi che tornano: la formazione dei commerciali diventa continua | 5 |
| **"Andrea"** | Richiama entro 90 secondi, 24/7, ogni nuova lead che nel modulo ha chiesto la richiamata di un assistente AI, si dichiara AI, qualifica e fissa l'appuntamento con uno di noi; risponde anche alle chiamate in entrata quando nessuno può; scrive l'esito di ogni telefonata nel canale delle vendite e nel CRM; impara dai rifiuti e prova aperture nuove | 5 |
| **Analista vinto/perso** | Perché un deal si chiude o si perde; manda il risultato al marketing, che migliora le campagne, e all'Agente clienti simili | 3 |
| **Agente intake** | Per ogni richiesta che arriva dal sito, dalla posta o da un contatto: chi è, cosa chiede, se rientra nel nostro cliente ideale, il brief di intake e il primo passo consigliato; prepara l'onboarding del potenziale cliente | 3 |
| **Agente contratti** | Dall'offerta approvata prepara il contratto sul nostro modello, lo manda in firma elettronica dopo il sì, ricorda le firme mancanti e, a firma avvenuta, avvisa il Project manager | 6 |

## 4.4 Squadra Marketing (responsabile: Alberto)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Editoriale** | Propone i temi dal piano marketing, dalle call, dalle obiezioni dei prospect e da ciò che ha funzionato nelle vendite | 2 |
| **Ricerca concorrenza** | Sorveglia siti, prezzi, annunci e contenuti dei concorrenti; manda un riepilogo settimanale e dà il contesto ai brief di vendita | 2 |
| **Analista metriche** | Il lunedì compila i dieci numeri del piano con i dati grezzi allegati; dice all'Outbound quali messaggi e temi funzionano | 2 |
| **Pubblicatore** | Prepara la lista da approvare (data, ora, rete, testo esatto, file); dopo il sì Alberto la programma su Postiz, sul nostro server (Metricool finché Postiz non è pronto), in una sessione presidiata, come chiedono le direttive; poi l'agente controlla che i post siano usciti e aggiorna calendario e registro | 2 |
| **Agente newsletter** | Prepara la newsletter dai post, dai casi studio e dalle novità e la manda dopo il sì; registra chi la apre, così il brief sa chi ci legge | 4 |
| **Community manager** | Legge commenti e messaggi della pagina aziendale e prepara le risposte da approvare; sui profili dei founder segnala soltanto, perché lì rispondono loro; passa all'Outbound chi può diventare cliente | 4 |
| **Agente sito e SEO** | Trasforma post e casi studio in articoli e pagine del sito, controlla SEO e velocità, propone le correzioni | 6 |
| **Agente eventi e webinar** | Organizza webinar ed eventi: inviti, iscrizioni, promemoria, follow-up dei partecipanti, che entrano in SersanOutreach come lead | 6 |

## 4.5 Squadra Studio contenuti (responsabile: Alberto)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Copywriter** | Post, caroselli, newsletter, testi delle campagne email, con la nostra voce e le regole di brand | 2 |
| **Agente slide** | Slide **per noi** (il brief prima dell'incontro) e **per il cliente** (recap dopo la call, proposta), deck e teardown con i nostri template | 3 |
| **Agente video** | Clip, reel, b-roll, motion graphics e varianti di formato, con Higgsfield, HyperFrames e After Effects | 4 |
| **Agente grafiche** | Immagini, caroselli e copertine con i nostri template | 4 |

## 4.6 Squadra Progetti (responsabile: Michele, con Mattia)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Project manager** | Apre il progetto quando il cliente firma: piano a fasi, milestone, responsabili, stato settimanale; segnala ritardi e rischi | 4 |
| **Agente task** | Crea i task dalle call, dalle chat e dalle mail, li assegna, ricorda le scadenze e chiude quelli già fatti | 2 |
| **Report cliente** | Report settimanale per il cliente con avanzamento e decisioni, da approvare prima dell'invio | 4 |
| **Onboarding cliente** | Dopo il kickoff: canale, cartelle, registro delle decisioni | 4 |
| **Sviluppatori** | Controllo qualità, analisi degli errori, pull request, documentazione, tutto in Claude Code e con revisione | 4 |
| **Assistenza clienti** | Legge le richieste dei clienti nella loro stanza e nella posta, prepara la risposta da approvare e apre i task | 6 |
| **Agente rinnovi** | Legge call, report e task dei clienti attivi: propone la fase successiva, segnala nuove opportunità e i clienti a rischio | 6 |
| **Agente casi studio** | A fine progetto scrive il caso studio con i numeri, chiede al cliente la testimonianza dopo il nostro sì e lo passa al Marketing | 6 |

## 4.7 Squadra Memoria (responsabile: Michele)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Raccoglitore** | Legge in continuo posta, calendario, documenti di M365, chat, BookStack, Jira, trascrizioni e CRM e li porta nella memoria | 3 |
| **Pulitore** | Deduplica, classifica, toglie i dati personali che non servono, separa il testo di terzi, che non è mai un'istruzione | 3 |
| **Bibliotecario** | Tiene la memoria: BookStack e PostgreSQL per ciò che è fisso, Qdrant per ciò che collega i momenti, con i modelli di embedding sulla nostra GPU. Risponde alle domande libere di tutti: «cosa si è detto con quel cliente?», «cosa gli abbiamo promesso?» | 3 |
| **Archivista** | Applica le scadenze di conservazione e tiene aggiornato il registro dei trattamenti | 3 |
| **Sistemista** | Sorveglia il server: salute delle macchine, backup, spazio, temperature, aggiornamenti dell'Agent SDK, dei servizi e dei modelli; avvisa Michele e prepara gli aggiornamenti da approvare | 3 |

## 4.8 Squadra Direzione (responsabili: Alessandro e Michele)

| Agente | Cosa fa | Fase |
|---|---|---|
| **Capo di gabinetto** | L'unico a cui scriviamo se non sappiamo a chi chiedere: capisce, smista alle squadre, riporta. Da computer e telefono | 2 |
| **Report del mattino** | Alle 7:00 per ciascuno: cosa è successo ieri, scadenze, task, pipeline, cosa aspettano gli agenti da noi | 1 |
| **Banca dei token** | Budget per agente, per catena di lavoro e per persona; avviso all'80%, stop al 100%; rendiconto mensile | 2 |
| **Registro e audit** | Ogni azione di ogni agente è tracciata: chi, cosa, perché, con quale approvazione | 2 |
| **Guardiano** | Blocca per default ciò che invia, pubblica, paga o cancella; chiede il sì sul telefono; stop di emergenza, che dalla fase 2 ferma anche gli invii di SersanOutreach (kill switch e pausa delle campagne Instantly) | 2 |
| **Mappatore processi** | Ricostruisce i processi dalle interviste e da ciò che ciascuno dichiara, e usa i metadati di M365 solo con l'accordo di ognuno (in quattro un dato aggregato resta riconoscibile). Restituisce la mappa con le ore implicite e le automazioni consigliate. Prima per noi, poi come servizio per i clienti (linea 04), insieme all'assessment | 4 |
| **Intervistatore** | Fa le interviste di assessment per ruolo, in chat | 4 |
| **Smistatore posta** | Legge tutta la posta in arrivo, non solo quella dell'outreach: smista, archivia, prepara le risposte da approvare, passa fatture e richieste alle squadre giuste | 3 |
| **Allenatore AI** | Un consiglio alla settimana a ciascuno su come usare meglio gli agenti, una guida per ogni agente nuovo, la formazione e la policy AI sempre aggiornate | 6 |
| **Assistente personale** (facoltativo) | Per chi lo vuole: calendario personale, preferenze di viaggio, famiglia. I dati di salute, se qualcuno vuole usarli, restano nel suo account privato e non entrano mai nella memoria aziendale | 6 |

## 4.9 Squadra Amministrazione (responsabili: Alessandro e Michele)

Chiude il giro che parte dall'outreach: dal contratto all'incasso. Si collega allo strumento di fatturazione e contabilità che usiamo (decisione 22 della sezione 14), e ogni fattura e ogni pagamento passano dal sì di una persona.

| Agente | Cosa fa | Fase |
|---|---|---|
| **Agente fatture e incassi** | Prepara la fattura quando una milestone è consegnata o quando il contratto lo prevede, la manda dopo il sì, segue gli incassi e prepara i solleciti | 6 |
| **Agente acquisti e abbonamenti** | Registra le fatture dei fornitori, tiene l'elenco di abbonamenti e rinnovi, segnala i posti che non usiamo e le scadenze in arrivo | 6 |
| **Controllo di gestione** | Porta nella memoria dati finanziari e obiettivi; ogni mese ricavi, costi, margine per cliente e per progetto, cassa e confronto con gli obiettivi | 6 |
| **Agente bandi e finanziamenti** | Cerca bandi, crediti d'imposta e finanziamenti per startup e AI, per noi e per i clienti; prepara scadenze, requisiti e documenti da raccogliere | 3 |

## 4.10 Come lavorano insieme: il percorso di un cliente

1. La **Sentinella segnali** trova un'azienda che assume uno sviluppatore e ha un progetto AI fermo. L'**Agente email** prepara il primo messaggio e Alessandro lo approva.
2. Il prospect risponde. L'Agente email lo scrive nella stanza dell'Outbound, l'**Agente agenda** fissa la call e l'Agente email passa il contatto all'**Agente brief**, che chiede alla **Ricerca concorrenza** il quadro del settore e all'**Agente slide** le slide per noi.
3. Il giorno della call l'**Agente chiamate** entra da solo, si presenta e trascrive.
4. Dieci minuti dopo la call: l'**Analista chiamate** scrive il riassunto, il **Post-call** aggiorna il CRM, l'Agente brief scrive il brief post-chiamata con tutto il contesto, l'Agente slide prepara il recap per il cliente, l'**Agente proposte** prepara la bozza dell'offerta per la firma di Michele, l'**Agente task** crea i task.
5. Le obiezioni sentite in call arrivano all'**Editoriale**, che le trasforma in un post; il **Copywriter** e l'**Agente video** lo producono; l'**Analista metriche** dice all'Agente email quali messaggi funzionano.
6. Michele approva l'offerta e l'**Agente contratti** manda il contratto in firma. Il cliente firma: il **Project manager** apre il progetto, l'**Onboarding** prepara canale e cartelle, il **Report cliente** parte dal primo venerdì, l'**Assistenza clienti** risponde alle domande nella stanza del cliente.
7. A ogni milestone consegnata l'**Agente fatture** prepara la fattura. A fine progetto l'**Agente casi studio** scrive il caso studio per il Marketing, l'**Agente rinnovi** propone la fase successiva e l'**Agente clienti simili** cerca aziende come questa: il giro riparte dal punto 1.

Ogni passaggio si vede nella chat di gruppo. Ogni cosa che esce verso il cliente passa da una carta e dal sì di una persona.

## 4.11 La chat di gruppo: Teams, Buzz, Slack, Telegram e WhatsApp

Tutti gli agenti e tutti noi stiamo in una chat di gruppo. La casa comune è **Microsoft Teams**, che abbiamo già con M365: un team "SerSan Agent OS" con un canale per squadra, "Approvazioni" per le carte, "Agenti", la sala macchine dove si passano il lavoro, "Ingresso", "Call di vendita", "Bandi" e un canale privato per ogni cliente. Ogni squadra ha un bot con il nome dei suoi agenti, e ogni messaggio è firmato dall'agente che lo scrive. Noi scriviamo al Capo di gabinetto o direttamente a un agente, dal computer o dal telefono.

- **Le carte** arrivano sul telefono dentro Teams: si approva con un tocco e il Cancello controlla chi ha premuto. Per offerte, contratti, fatture e primi contatti serve anche la chiave di sicurezza FIDO2.
- **Telegram** riceve gli avvisi; **WhatsApp** serve soprattutto verso i clienti, con l'API ufficiale di Meta e un numero dedicato, sempre dal Cancello; **Slack** si collega per i clienti che lavorano lì. Sono gli stessi agenti con lo stesso codice, e arrivano nella fase 3. Su questi canali passano solo dati verdi; per approvare anche da Telegram o WhatsApp serve legare quegli account all'identità Microsoft di ciascuno, e si può aggiungere in una fase successiva.
- **Buzz**, la chat open source di Block fatta per persone e agenti, gira sul banco di prova del nostro server come stanza degli agenti, collegata alla stessa bacheca di Teams. È ancora giovane: oggi perde alcune risposte senza segnalarlo e le sue approvazioni non sono pronte. Esce dal laboratorio quando questi problemi sono chiusi; se allora è più comoda di Teams, diventa la nostra casa comune.
- **Claude Team** resta la finestra di lavoro di ognuno: chat, skill, progetti per squadra e la ricerca nella memoria aziendale, con i propri permessi.

Un freno nel codice impedisce le catene infinite fra agenti: al massimo otto messaggi per thread, catene di tre passaggi, un tetto di spesa per catena. Nessun bot entra nei canali condivisi con i clienti: lì scrive solo il Cancello, dopo una carta.

## 4.12 L'organigramma

Ogni agente ha una riga nel registro: nome, squadra, responsabile umano, modello che usa, cosa può toccare, tetto di spesa, costo del mese. Il registro si vede come organigramma in una pagina di BookStack e in un cruscotto: Alessandro ha a riporto le squadre Outbound, Chiamate e Vendite; Michele la Memoria e i Progetti; Alberto il Marketing e lo Studio; la Direzione e l'Amministrazione sono di entrambi i CEO. Un agente nuovo nasce solo con un'approvazione, che porta con sé la sua riga nel registro dei trattamenti. Il disegno conta 57 agenti e cresce: ogni processo che si ripete diventa una skill, ogni skill che funziona diventa un agente. Cento agenti sono la traiettoria: gli agenti al lavoro sono 14 alla fine della fase 2, circa 32 alla fine della fase 3 e tutti e 57 alla fine della fase 6. Nella fase 6 proviamo anche Paperclip, un piano di controllo open source fatto apposta per "aziende di agenti".

# 5. Come è fatto

## 5.1 Le scelte in cinque frasi

1. **Tutto sul nostro server, dentro il board di Michele.** In cloud restano solo i servizi verticali del suo board: M365 con Teams, Claude Team, le API di Anthropic, Jira, Instantly, GitHub, Supabase, Vercel, il DNS e una piccola macchina Oracle a Milano per l'accesso da fuori. Il resto gira in casa, in reti separate; fuori dal board restano poche eccezioni da approvare una per una: la linea telefonica di Andrea, WhatsApp, Telegram, Slack per i clienti, l'invio della newsletter e alcuni strumenti commerciali (decisioni 8-10 e 15).
2. **Il motore lo costruiamo noi con l'Agent SDK di Claude.** È Claude Code usato come libreria: ogni lavoro gira in un processo suo, con il profilo dell'agente, i suoi strumenti e un tetto di spesa.
3. **Claude ragiona, LiteLLM tiene i conti.** Gli agenti usano Claude via chiave API (Haiku per i lavori semplici, Sonnet per quasi tutto, Opus per offerte e analisi) attraverso LiteLLM, che dà a ogni agente, squadra e persona il suo budget.
4. **Il Cancello agisce.** È l'unico programma che può mandare una mail, scrivere al cliente, toccare il CRM o telefonare. Le azioni verso l'esterno le fa solo dopo il sì di una persona, una volta sola, o con una regola "Sempre" (sezione 5.4); le telefonate di "Andrea" partono senza carta solo verso chi ha chiesto di essere richiamato (decisione 10); le scritture interne (meeting e deal nel CRM, to-do in Jira) le fa secondo regole scritte, a nome della persona responsabile. In entrambi i casi registra tutto.
5. **La chat di gruppo è la casa comune.** Teams per persone e agenti, con le approvazioni sul telefono; Telegram, Slack e WhatsApp collegati; Buzz in prova sul nostro server.

## 5.2 Lo schema

```
PERSONE (4)   Teams e Outlook (M365, accesso con MFA e chiave FIDO2), dal PC e dal telefono
              Claude Team: chat, skill, progetti per squadra, ricerca nella memoria
              Telegram (avvisi) · WhatsApp (clienti) · Slack (clienti) · Buzz (in prova)

===== SERVER DL380 · Proxmox · reti separate dietro OPNsense · accesso da NetBird =====
INGRESSO   Traefik, raggiunto da Pangolin sulla macchina Oracle: bot di Teams,
           webhook firmati, ricerca nella memoria per Claude Team, pagine di firma
APP        CANCELLO + PORTA CHAT (bot di Teams, Telegram, Slack, WhatsApp)
           server MCP: memoria, bacheca, BookStack, Jira, posta in lettura,
           SersanOutreach
           n8n (orari) · LiteLLM (budget) · BookStack · SersanOutreach
           Postiz · listmonk · DocuSeal · fatturazione · Andrea (Pipecat)
AGENTI     MOTORE (Agent SDK): un processo per lavoro, nessun accesso a internet
DATI       PostgreSQL 16 · Qdrant · Infisical · Vaultwarden · archivio dei file
VOCE       Asterisk: il centralino di Andrea, con una linea telefonica italiana
RIUNIONI   Vexa: il bot nelle call dei clienti (Teams di altri, Meet, Zoom)
AI         RTX 4000 + seconda GPU: embedding, ricerca, Qwen3-4B, trascrizione
MONITOR    Prometheus · Grafana · Loki · Uptime Kuma · Wazuh · NetBox
LAB        banco di prova degli agenti · Buzz · Paperclip
=======================================================================================
CLOUD DEL BOARD  M365 ed Entra · Claude Team · API Anthropic via LiteLLM · Jira
                 Instantly · GitHub · Supabase · Vercel · Cloudflare (DNS)
                 Oracle Cloud a Milano: NetBird, Pangolin, monitoraggio
ESTERNI          linea telefonica italiana · WhatsApp (Meta) · Telegram · Slack
                 invio della newsletter · strumenti commerciali che restano
BACKUP 3-2-1     Proxmox Backup Server in sede, ogni notte copia cifrata a casa
                 di Michele (Terra Noa) · S3 fuori sede facoltativo
```

## 5.3 Perché il motore sull'Agent SDK

- **Usa quello che Michele ha già.** Orari e integrazioni li fa n8n, i budget li tiene LiteLLM, la memoria sta in PostgreSQL, Qdrant e BookStack. Il motore non duplica nulla.
- **La persona arriva fino alla memoria.** Quando un agente lavora per Alessandro, la memoria gli mostra solo ciò che Alessandro può vedere. Così il coaching resta a chi ha fatto la call e i dati di ciascuno restano suoi.
- **Il Cancello si aggancia dentro il motore.** Prima di ogni azione il motore chiede al Cancello; se il Cancello non risponde in tempo, l'azione è bloccata.
- **È la tecnologia che già usiamo.** È la stessa di Claude Code, che Alberto usa ogni giorno: un pacchetto da aggiornare ogni due settimane, dopo dieci scenari di prova.
- **Cosa costa in più.** La bacheca fra agenti, i profili con nome e i bot per le chat li scriviamo noi, mentre Hermes li darebbe pronti. Sono giorni messi nel piano (sezione 15).

## 5.4 Il Cancello: l'autonomia senza perdere il controllo

L'obiettivo è che il post-call avvenga in modo autonomo. Ci arriviamo per gradi. La prima versione del Cancello è pronta alla fine della fase 1; le parti successive arrivano con le fasi che le usano. Funziona così:

1. Un agente **propone** un'azione ("manda questa mail a questo indirizzo").
2. Una regola la classifica: lettura, scrittura interna, invio, pubblicazione, pagamento, cancellazione, credenziali.
3. Le azioni delicate diventano una **carta** nel canale Approvazioni di Teams, con il testo esatto, un codice che vale una volta e una scadenza.
4. Dopo il sì di una persona, l'**esecutore** la compie una volta sola. Se nel frattempo il testo è cambiato, la carta non vale più. Per offerte, contratti, fatture e primi contatti serve anche la chiave FIDO2.
5. Tutto finisce nel **registro**, con chi ha chiesto, chi ha approvato e quanto è costato.

Quando la stessa approvazione si ripete uguale per venti volte senza modifiche, una persona può trasformarla in una regola "Sempre", stretta su quell'agente, quel tipo di azione e quella destinazione, che scade dopo 30 giorni. Mai per offerte, primi contatti, pagamenti, cancellazioni, né per destinatari nuovi.

Una protezione in più: la macchina degli agenti non ha accesso a internet e parla solo con LiteLLM, con i server MCP e con il Cancello. Un agente non ha una strada per mandare qualcosa fuori se non passando dal Cancello. Prima che i dati dei clienti restino sul server, una società esterna rivede Cancello, motore e bot (decisione 5).

## 5.5 La memoria

La memoria è divisa per tipo, e ogni tipo ha una sola fonte di verità:

| Dove | Cosa contiene |
|---|---|
| BookStack, sul server | le regole di lavoro di ciascuno ("Come lavoro"), i processi, il catalogo servizi, il manuale degli agenti |
| PostgreSQL, sul server | registro e organigramma degli agenti, obiettivi, prezzi, registro dei meeting, decisioni, passaggi fra agenti |
| Qdrant, sul server | ciò che "connette i momenti": trascrizioni, mail, documenti, Sirius, bandi, pagine di BookStack, issue di Jira |
| Jira | to-do e progetti |
| M365 | documenti, posta e calendario |

Gli embedding si calcolano sulla nostra GPU, quindi il contenuto non esce per essere indicizzato. Chiunque può chiedere, anche da Claude Team, "cosa ci siamo detti con X a settembre?" e ottenere la risposta con le fonti, vedendo solo ciò che può vedere. I numeri (pipeline, margini, budget) si calcolano dal codice sui dati, non si cercano nel testo.

## 5.6 I tre colori dei dati

Una regola semplice, scritta nel codice del Cancello, decide cosa può uscire dal server e verso chi:

| Colore | Cosa | Dove può andare |
|---|---|---|
| **Verde** | Pubblico o interno non personale | Qualunque fornitore ammesso, anche Claude Team |
| **Giallo** | Contatti di lavoro, campi del CRM, riassunti | Solo i fornitori del board, con contratto commerciale e DPA |
| **Rosso** | Audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone, finanza | Resta sul server, oppure va all'API Anthropic dopo aver oscurato in locale i dati non necessari |

Con tutto sul nostro server spariscono le due eccezioni della prima versione: l'audio delle call e la voce di Andrea non passano più da fornitori negli USA. L'audio resta in casa e si trascrive in casa. Claude Team riceve verde e giallo, e il rosso solo oscurato, finché il parere legale e la valutazione d'impatto non decidono diversamente, entro la settimana 3. L'oscuramento locale lo costruiamo e lo misuriamo nella fase 1.

## 5.7 Le alternative che abbiamo valutato

Michele ci ha chiesto di valutare se si può evitare Hermes usando l'Agent SDK di Claude, senza escluderlo a priori. Con il suo board abbiamo rifatto il confronto da capo: tre architetture, scritte da agenti AI separati dentro il suo board, valutate da quattro agenti giudici, ognuno con una lente: la visione di Alberto, la lente commerciale di Alessandro, quella tecnica di Michele, sicurezza e privacy. È un metodo per mettere alla prova la scelta prima di portarvela, non un verdetto: i punteggi e i dissensi dei giudici sono nell'appendice B. Punteggi su 240:

| Proposta | Visione | CEO | CPTO | Sicurezza | Totale | In una riga |
|---|---|---|---|---|---|---|
| **1. Motore sull'Agent SDK** | 43 | 42 | 44 | 42,5 | **171,5** | Scelta: tutte le 57 figure come agenti veri, senza doppioni con lo stack di Michele |
| 3. Claude Team al centro | 41 | 45 | 42 | 42 | 170 | La più rapida a dare valore, e la sua fase zero è entrata nel piano; da sola però trasforma molti agenti in strumenti da aprire a mano |
| 2. Hermes sul nostro server | 35 | 34 | 34 | 34 | 137 | Pronto con canali, profili e bacheca, ma con un punto unico che oggi ha 276 problemi aperti, 9 di sicurezza, e con funzioni doppie rispetto a n8n e LiteLLM |

**Hermes resta una porta aperta.** Se il motore non regge le verifiche delle settimane 8 e 21, proviamo Hermes sullo stesso banco di prova e decidiamo sui numeri: Cancello, memoria, server MCP, bot e skill restano uguali. Diventa il nostro orchestratore solo se chiude i suoi problemi di sicurezza. Il primo giro di confronto, con sette architetture, è nell'appendice B.

# 6. Il server

## 6.1 Cosa abbiamo

Il server è già completo e si monta secondo il board di Michele:

| Componente | Cosa c'è |
|---|---|
| Rack | 12U nell'ufficio di Cagliari: server, firewall e UPS; presto il backup in sede, più avanti il secondo server |
| Server | HPE ProLiant DL380 Gen10, due Intel Xeon Gold 5218 (64 thread in tutto) |
| Memoria | 192 GB DDR4 ECC: 12 moduli da 16 GB a 2133 MHz, uno per canale |
| Dischi | 2 SSD SAS da 800 GB in mirror per il sistema; 6 HDD SAS da 1,8 TB in tre mirror, circa 5,4 TB per i dati |
| GPU | NVIDIA Quadro RTX 4000 da 8 GB, nel riser principale, cioè il supporto che ospita le schede aggiuntive del server, che con il controller dei dischi è già pieno |
| Raffreddamento e corrente | ventole e dissipatori ad alte prestazioni, due alimentatori da 800 W Titanium |
| Rete | firewall Sophos SG 230 da rack, in arrivo, con Proxmox e OPNsense; fibra TIM a 2,5 Gbit, che sulle porte del firewall lavora a circa 1 Gbit; reti separate per ogni tipo di servizio; accesso da fuori solo da NetBird con identità verificata, attraverso la macchina Oracle; per ora nessuna linea di riserva |
| Backup | regola 3-2-1, cioè tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio: una copia in sede su un Proxmox Backup Server che Michele monta con pezzi suoi (mancano case e dischi), acceso di notte; ogni notte una copia cifrata va a casa di Michele, a Terra Noa, da marzo 2027 |
| Corrente | UPS da rack HPE R1500 G5 (1.550 VA, 1.100 W), in arrivo: se manca la corrente, dopo 3 minuti (come nella board di Michele) spegne il server in modo pulito e tiene accesa la rete fino a fine batteria; al ritorno della corrente la rete, se si era spenta, riparte da sola, mentre il server, com'è impostato oggi, va riacceso a distanza |

Il Sophos è un SG 230 rev. 2, un modello che Sophos non supporta più dal 30 giugno 2026. Michele non usa il software Sophos: ci mette Proxmox con OPNsense e i servizi di rete, tutti aggiornati dai loro progetti. Restano senza aggiornamenti il BIOS e il processore: per Cyber Essentials chiediamo prima all'ente di certificazione se accetta questa configurazione (sezione 13). Il Sophos fa anche da arbitro: quando arriva il secondo server, se uno dei due si ferma l'altro continua da solo.

Il supporto HPE per lo chassis dura fino a ottobre 2029 secondo le fonti ufficiali HPE consultate da Michele; le fonti pubbliche danno stime da marzo 2028 a ottobre 2029, quindi la data si conferma con il numero di serie del server. Il sistema gira comunque in macchine virtuali con backup: si sposta su un server nuovo senza rifare nulla. Michele prevede il secondo server già a dicembre, se c'è il budget (fino a 1.500 €): con il DL380 forma un cluster.

## 6.2 Cosa ci gira

Michele ha già previsto la maggior parte dei servizi: n8n, LiteLLM, PostgreSQL, Qdrant, BookStack, i segreti, il monitoraggio, la pipeline che rende ricercabili i documenti e i modelli locali sulla GPU. Il sistema di agenti aggiunge il motore, il Cancello con i bot della chat, i server MCP, il bot delle call, il centralino e la voce di Andrea, e qualche strumento per marketing e amministrazione: programmazione dei post, newsletter, firma elettronica, fatturazione. Ogni servizio nuovo entra nel perimetro Cyber Essentials con un responsabile delle patch, e prima della fase F4 del board entrano solo quelli del pilota.

La GPU fa i lavori che conviene tenere in casa: embedding e ricerca nella memoria, il modello piccolo che prepara i documenti, la trascrizione delle call e, con la seconda GPU, la voce di Andrea. Gli agenti ragionano con Claude via API: il motore non usa la GPU.

## 6.3 La RAM

Il board lascia circa 53 GB liberi. Il pilota ci sta largo; con memoria e call (fase 3) si arriva al limite; con tutte le funzioni (fasi 5-6) mancano circa 20 GB:

| | Fase 1 | Fase 2 | Fasi 3-4 | Fasi 5-6 |
|---|---|---|---|---|
| GB usati dal sistema di agenti | 8 | 25 | 53,5 | 70-74 |
| GB liberi con 192 GB | circa 45 | circa 28 | circa 0 | da -17 a -21 |
| GB liberi con 384 GB | | | circa 191 | circa 171-175 |

Per questo proponiamo di aggiungere altri 192 GB prima della fase 3 (settimana 22), o prima se il margine misurato scende sotto i 5 GB: 12 moduli da 16 GB uguali a quelli montati, uno in più per ogni canale. È l'unico passo che tiene la memoria bilanciata, e la velocità resta quella di oggi. Costa circa 690-830 € IVA esclusa (decisione 11).

## 6.4 La seconda GPU

Michele ha scelto la **RTX PRO 2000 Blackwell da 16 GB** e la compra più avanti, quando il prezzo scende. È la generazione successiva della RTX 2000 Ada che avevamo proposto: stessi 16 GB e 70 W senza cavi di alimentazione, memoria più veloce. Con 16 GB ci stanno insieme la trascrizione dal vivo, la voce di Andrea e la ricerca nella memoria, giorno e notte.

**Prezzo e montaggio.** In Italia oggi costa circa 1.290-1.305 € IVA inclusa (circa 1.060 € esclusa), circa il 20% in più di fine ottobre; la mediana dell'ultimo anno è intorno ai 985 € IVA inclusa (circa 810 € esclusa). Conviene comprarla quando torna sotto i 1.000 € IVA inclusa (circa 820 € esclusa); se all'inizio della fase 5 costa ancora di più, la compriamo lo stesso. Il riser principale del server è pieno: la scheda, che occupa due slot, va nel riser secondario, che costa circa 75-160 € con IVA e spedizione se non c'è già. La versione PNY venduta al dettaglio ha già la staffa ad altezza piena che serve; con le altre versioni la staffa costa circa 20 €.

**Quando comprarla.** Le trascrizioni delle nostre call in Teams arrivano già scritte da Microsoft, quindi le fasi 0-2 non ne hanno bisogno. Conviene dalla fase 3 (settimana 22), quando trascriviamo in casa le call dei clienti e le riunioni dal vivo e la RTX 4000 è quasi piena. Serve al più tardi all'inizio della fase 5 (settimana 41), prima di spostare Andrea sulla GPU, perché la voce al telefono non può aspettare. Fino ad allora fa tutto la RTX 4000; quando Michele la presta alla postazione di prova del laboratorio (Experimental-1), per poco tempo e solo ogni tanto, i lavori della GPU aspettano in coda finché torna libera. HPE non certifica due GPU di modelli diversi nello stesso server: la garanzia della scheda resta quella del venditore. Prima di spostare la trascrizione sulla nuova scheda proviamo che i programmi girano sulla sua architettura.

# 7. SersanOutreach dentro il sistema

## 7.1 Dove siamo

SersanOutreach è la nostra piattaforma outbound (LinkedIn ed email) con approvazione umana prima di ogni invio, tranne l'autopilot LinkedIn attivato a metà ottobre, che redige e approva da solo inviti e DM entro tetti giornalieri: 269 endpoint, 70 modelli di dati, 45 attività pianificate, quasi 11.000 test. Gira su una VM Azure condivisa con il database su Supabase. I numeri reali al 5 ottobre: 11 lead, 1 contattato, 1 risposta, 0 meeting, 91 deal aperti senza un valore. L'email via Instantly è pronta ma nessun dominio è attivo, perché una decisione di compliance è ancora aperta; su LinkedIn l'ultimo invio è manuale, del 25 settembre.

La macchina c'è, è grande e ben protetta, ma **gira a vuoto** perché mancano le decisioni e le mani che la usino ogni giorno. Gli agenti sono quelle mani.

## 7.2 Perché spostarlo sul nostro server

| | Oggi (Azure e Supabase) | Sul server SerSan |
|---|---|---|
| Applicazione | VM Azure con 15,6 GB condivisi tra produzione, stage e monitoraggio, stimata circa 150 € al mese | sul server, nella rete delle app, accanto alla memoria aziendale e al monitoraggio |
| Database | Supabase in Irlanda | resta su Supabase, che il board tiene in cloud come database del prodotto, salvo una scelta diversa di Michele |
| Agenti | prese MCP pronte ma non collegate | prese MCP raggiungibili dal motore, con un accesso per squadra |
| Dati | in due cloud | applicazione e memoria in casa, con il backup in sede e, da marzo 2027, una copia cifrata a casa di Michele |

La migrazione avviata il 16 ottobre cambia destinazione: invece di un nuovo assetto su Azure, il server, nella fase F2 del board di Michele ("via da Azure"). La VM Azure si spegne **solo dopo una settimana di funzionamento stabile**. Teniamo il dominio `outreach.sersan.io`, così l'estensione Chrome dei membri non va ricostruita.

## 7.3 Le prese per gli agenti sono già pronte

SersanOutreach è stato costruito pensando a Claude. Ha due server MCP, cioè due prese standard a cui un agente si collega:

- **lettura, 19 strumenti**: KPI, coda delle azioni, pipeline, funnel, risposte positive, azioni scadute, meeting, analisi dei deal persi, candidati alla riattivazione;
- **operatore, 14 operazioni**: importa lead, genera bozze (mai le approva), approva o rifiuta un messaggio solo se il testo è quello letto (questa operazione la chiama solo il Cancello, dopo il sì di una persona su una carta: gli agenti leggono liberamente e scrivono solo attraverso il Cancello), aggiorna un deal, registra un meeting o la prossima azione, mette in pausa una campagna. Non esistono invii in blocco, lanci o cancellazioni: restano a una persona. Per i clienti già attivi, che spesso non sono lead in SersanOutreach, aggiungiamo nella fase 2 l'operazione che crea un deal.

| Agente | Cosa fa dentro SersanOutreach |
|---|---|
| Post-call | Registra il meeting, aggiorna il deal con valore e prossima azione, apre i to-do |
| Pipeline | Legge eventi commerciali, deal e meeting e calcola la probabilità pesata |
| Agente brief | Parte dall'arricchimento già fatto e dallo storico delle conversazioni |
| Operatore outbound | Importa, fa generare le bozze, le porta in coda, legge le risposte |
| Sentinella segnali | Legge la casella dei segnali e propone i contatti |
| Agente email | Gestisce le sequenze, legge l'inbox, classifica e propone la risposta |
| Agente LinkedIn | Prepara inviti e messaggi da approvare e segue le conversazioni |
| Analista vinto/perso | Legge i motivi di chiusura e manda i risultati al marketing |
| "Andrea" | Riceve la lead dal sito o dalle campagne, se nel modulo ha dato il consenso alla richiamata; chiama, registra l'esito e il meeting |

## 7.4 Cosa va chiuso prima

Nella fase 0, prima di collegare gli agenti: la decisione di compliance sull'email (indirizzo e link di cancellazione nel footer, oppure deroga registrata con parere legale), l'identità firmata dei chiamanti, il secondo fattore per i 7 account staff, una copia dei dati di SersanOutreach fuori dai suoi cloud, per esempio sul backup in sede, con una prova di ripristino riuscita (la copia a casa di Michele, a Terra Noa, si aggiunge da marzo 2027), e gli alert che arrivano davvero a una persona. Sono le stesse cose che il report del mattino renderà visibili ogni giorno: la prima utilità degli agenti è non lasciare più ferme decisioni così.

**LinkedIn.** Gli agenti lavorano solo con l'approvazione umana di ogni messaggio: non usano l'autopilot dei DM né l'automazione del browser lato server. Se volete tenere l'autopilot acceso per le campagne di oggi, resta fuori dal perimetro degli agenti.

# 8. Il piano marketing e i post

## 8.1 Dove siamo

Il piano dei 90 giorni (175 pagine) e le direttive del 22 ottobre dicono con chiarezza cosa fare: il motore è **LinkedIn organico dai profili di Michele e Alessandro**, due post a settimana ciascuno, martedì e giovedì; la Pagina aziendale rilancia il mercoledì; Instagram un pezzo a settimana; YouTube con podcast e Shorts dalla quinta settimana; la newsletter di Michele se decidiamo sì il 23 novembre. Cinque pilastri di contenuto, dieci numeri da leggere ogni lunedì, un criterio di stop scritto prima di vedere i dati.

E dicono anche dove siamo: 96 slot in calendario, 22 testi pronti e approvati dal 6 ottobre, **tre pezzi pubblicati verificati al 13 ottobre** e altri cinque programmati fino al 22 ottobre, nessun post dei founder uscito, coda vuota dopo il 22 ottobre. Le direttive del 22 ottobre sono scritte esplicitamente "per un nuovo addetto ai contenuti". **Il sistema di agenti è quell'addetto.** Non sostituisce i founder davanti alla camera né il sì prima di ogni pubblicazione: fa tutto il resto, ogni settimana.

## 8.2 Gli agenti di Marketing e Studio, dentro le regole di casa

Le regole restano: niente esce senza un sì scritto; sulle piattaforme si scrive solo da una sessione presidiata; volti e voci solo dei founder con consenso; numeri solo dalla banca delle storie ("se un numero manca, togli la frase"); commenti su LinkedIn solo con regole approvate e tetti; inviti e messaggi solo da SersanOutreach.

| Agente | Ogni settimana | Strumenti |
|---|---|---|
| Editoriale | Temi per gli slot vuoti, con pilastro, voce, formato e la prova (storia o timecode di una registrazione) | Calendario, brief editoriale, banca storie, risposte e feedback da SersanOutreach |
| Ricerca concorrenza | Siti, prezzi, annunci e contenuti dei concorrenti; riepilogo settimanale; contesto per i brief di vendita | Firecrawl sul nostro server, ricerca web |
| Copywriter | Bozze EN e IT per LinkedIn, Instagram, YouTube, con il controllo automatico delle regole e una seconda lettura critica | Caption, plugin LinkedIn con il profilo di voce del founder |
| Visual e video | Scene, caroselli, teardown in PDF, thumbnail, b-roll, varianti di formato | HyperFrames in casa, Higgsfield, slide e design di Claude Team con i template SerSan |
| Pubblicatore | Bozze sullo scheduler con data, ora e testo esatto; dopo il sì Alberto le programma in una sessione presidiata e l'agente controlla che escano | Postiz sul nostro server; Metricool finché Postiz non è pronto |
| Analista metriche | I dieci numeri del lunedì con i dati grezzi allegati; quali formati vincono | Postiz in lettura, KPI di SersanOutreach |
| Newsletter | Una newsletter dai post e dai casi studio, mandata dopo il sì; chi la apre arriva nel brief | listmonk sul nostro server |
| Community manager | Risposte da approvare ai commenti e ai messaggi della pagina aziendale; sui profili dei founder segnala soltanto | Postiz, LinkedIn in lettura |

## 8.3 Il cerchio con le vendite

Marketing e Outbound lavorano come una squadra sola: i commenti qualificati sui post diventano contatti con un motivo per scrivere; le obiezioni nelle call diventano post e la serie "Prima di inviarci un brief"; i motivi per cui perdiamo un deal diventano teardown; le lead dal sito vengono richiamate e qualificate, e un founder risponde entro un giorno lavorativo come promettiamo.

## 8.4 Cosa sblocca subito

Nella fase 0, con Claude Team e la sessione presidiata di Alberto: calendario proposto fino a Natale e le 22 caption pronte programmate dopo il sì. Dalla fase 0 i numeri del lunedì li compila una skill di Claude Team; dalla fase 2 gli agenti tengono i registri e compilano i numeri con i dati grezzi; quelli dei profili dei founder arrivano quando i profili sono collegati. Restano a noi il provino di Alessandro, le registrazioni di voce, la pulizia del sito, il collegamento dei profili LinkedIn e le decisioni aperte del piano.

# 9. Controllo, sicurezza e regole

## 9.1 Le dieci regole del sistema

| # | Regola |
|---|---|
| 1 | Ogni agente che parla o scrive **da solo** a un esterno, come "Andrea", **si dichiara AI** dalla prima frase (AI Act, art. 50, in vigore dal 2 agosto 2026); mail, offerte e post che una persona rivede e approva escono a nome di quella persona |
| 2 | **Nessuna registrazione senza avviso**: nell'invito, a voce, con la possibilità di dire no |
| 3 | **Nessun giudizio sulle persone senza revisione umana**: il coaching va solo all'interessato, al responsabile vanno dati aggregati, nessuna emozione inferita |
| 4 | **Chiamate automatiche solo con consenso documentato** e numeri verificati sul Registro delle opposizioni |
| 5 | **Un "no" vale per tutti i canali e tutti gli agenti**: una sola lista di soppressione |
| 6 | **Nessuna voce o volto di una persona reale** senza un contratto separato, facoltativo e revocabile |
| 7 | **Minimizzazione prima del cloud**: si oscura ciò che non serve; solo fornitori con contratto commerciale e DPA |
| 8 | **Conservazione con scadenze automatiche**: audio fino a 30 giorni, trascrizioni e CRM 24 mesi dall'ultimo contatto, log degli agenti 90 giorni |
| 9 | **Registro dei trattamenti e valutazione d'impatto** aggiornati a ogni nuovo agente, compresi i brief pre-meeting, che sono profilazione |
| 10 | **Una persona nel giro per ogni azione esterna irreversibile**, e formazione AI documentata per tutti e quattro |

## 9.2 I cinque meccanismi di controllo

1. **Gli agenti propongono, il codice esegue.** Nessun agente ha in mano un bottone che invia, pubblica, paga o cancella: passa sempre dal Cancello. La macchina degli agenti raggiunge solo i servizi in lista, e nessun bot entra nei canali condivisi con i clienti.
2. **Le routine nascono spente.** Ogni automazione parte in prova a secco: per una o due settimane mostra cosa avrebbe fatto, senza farlo.
3. **Il testo di terzi non è mai un'istruzione.** Email, trascrizioni, pagine web e risposte dei prospect entrano da una corsia senza strumenti: gli agenti li leggono come dati, non come comandi. È la difesa contro le iniezioni di prompt, il rischio numero uno di qualunque agente che legge la posta.
4. **Tetti che fermano davvero.** Ogni agente e ogni catena di lavoro ha un budget; all'80% arriva un avviso, al 100% si ferma.
5. **Tutto è registrato e revocabile.** Registro delle azioni a sola aggiunta, segreti oscurati prima di qualsiasi log, stop di emergenza dal telefono.

## 9.3 Cosa resta umano, per scelta

Alcune cose le teniamo fuori dall'AI per scelta. Il nostro cuore è il giudizio: lo dice il nostro claim, "The intelligence is artificial. The judgement stays human". Restano a una persona, sempre:

- il **sì** a ogni messaggio verso un cliente o un prospect, a ogni pubblicazione, a ogni proposta, contratto e fattura, e a ogni prezzo, salvo le regole "Sempre" che decidete voi per messaggi ripetitivi a destinatari già noti (sezione 5.4) e le telefonate di "Andrea" a chi ha chiesto di essere richiamato (decisione 10);
- le **decisioni** di scope, di "non costruire", di accettare o rifiutare un cliente;
- la **valutazione delle persone**;
- la **relazione**: le call le facciamo noi, "Andrea" fissa l'appuntamento e non vende;
- **voce e volto** dei founder, i loro messaggi privati e i loro commenti;
- la **firma tecnica** di Michele sulle affermazioni tecniche.

## 9.4 Dove serve un parere legale

Nella fase 0 chiediamo un parere unico, in due consegne: entro la settimana 3 i punti che servono al pilota (email B2B verso l'Italia, registrazione delle call, trasferimenti verso gli USA), prima della fase 2 tutto il resto. I punti sono: come si applica il GDPR europeo a una Ltd con il team in Italia (ed eventuale rappresentante UE); l'inquadramento dei collaboratori in Italia (da cui dipendono le regole sul controllo a distanza); "Andrea" e il consenso nel modulo; un'eventuale voce clonata; il confine tra coaching e valutazione dei lavoratori; l'email B2B verso l'Italia (chiude la decisione aperta di SersanOutreach); i trasferimenti di dati verso gli USA; la registrazione delle call con clienti UK; i dati personali che possono arrivare a Claude Team; il valore legale della firma elettronica fatta in casa; la copia cifrata dei backup a casa di Michele, con la sua designazione per iscritto.

# 10. Persone e adozione

Un sistema così funziona solo se lo usiamo tutti, ogni giorno: comprare licenze non basta, serve cambiare il modo di lavorare, e non si può delegare. Il programma:

1. **Assessment (settimana 1).** Ognuno di noi descrive quali processi fa ogni settimana e con quali strumenti.
2. **Le regole di ciascuno (settimane 1-2).** Ogni persona scrive in BookStack come vuole i suoi riassunti, i prossimi passi, i report e gli orari di non disturbo. Gli agenti le leggono prima di ogni lavoro.
3. **Ambassador.** Alberto e Michele guidano la costruzione; Mattia diventa il secondo amministratore e l'ambassador interno, con un tetto di token più alto.
4. **Ognuno possiede almeno un agente** nel proprio ambito, con il Cancello e la banca dei token come limiti. Il venerdì, un breve punto su "cosa ho automatizzato questa settimana".
5. **Premio mensile** a chi ha costruito con l'AI la cosa che ha cambiato di più il nostro lavoro (proposta: un voucher di 50-100 €).
6. **Formazione** documentata per tutti e quattro (obbligo dell'AI Act, art. 4), aggiornata a ogni nuovo agente.
7. **Misura mensile**: tempo restituito, meeting fissati, proposte uscite, post pubblicati, costo per persona.

# 11. Il piano a fasi

Le settimane sono il calendario delle fasi; la stima dei giorni di sviluppo è nella sezione 15. Il piano corre accanto alla roadmap di Michele (F0-F5): l'infrastruttura la porta avanti lui, noi costruiamo sopra il sistema di agenti. Ogni fase parte quando la precedente è verificata, come nel suo board.

| Fase | Settimane | Board di Michele | Cosa si fa | Cosa vedete alla fine |
|---|---|---|---|---|
| **0. Valore subito e prove** | 1-4 | F0-F1 | Claude Team per tutti, con skill, template SerSan e progetti per squadra; decisione sull'email con il legale e casella attiva; sicurezza di SersanOutreach; registro dei trattamenti e valutazione d'impatto; quattro prove tecniche (bot di Teams, identità di chi approva, blocco delle azioni, LiteLLM); prima parte del motore | Tutti e quattro in Claude Team ogni giorno. Calendario dei post pieno fino a Natale. Prime offerte e slide con il nostro stile. Email decisa e casella attiva. SersanOutreach sicuro su identità e MFA |
| **1. Pilota su banco di prova** | 5-8 | F1-F2 | Motore su una macchina di prova nella rete del laboratorio; Cancello versione 1; invio da Outlook; carte in Teams con l'identità di chi approva; trascrizioni delle call Teams lette da Microsoft; oscuramento locale; Post-call, Analista chiamate e Report del mattino | Dopo una call Teams il riassunto arriva nel canale interno e la bozza della mail arriva come carta sul telefono; dopo il sì parte una volta sola. Debrief alle 7:00 per tutti. **Verifica della settimana 8** |
| **2. Pilota sul server e squadre che si parlano** | 9-21 | F2-F4 | Motore sul server con n8n e LiteLLM; Cancello con FIDO2 e regole "Sempre" che scadono; nove bot di squadra in Teams; Jira, BookStack e memoria per gli agenti; SersanOutreach collegato; bacheca con il freno e canale "Agenti"; richiesta a Meta per WhatsApp; 11 agenti nuovi | CRM e to-do in Jira dopo ogni call. Gli agenti del marketing si passano il lavoro nel canale "Agenti" con il freno in azione. Organigramma con 14 agenti e i loro costi. Banca dei token in LiteLLM. **Verifica della settimana 21** |
| **3. Memoria, call, vendite preparate e canali** | 22-35 | F4 | Ricerca nella memoria con i permessi di ciascuno, anche da Claude Team; bot nelle call dei clienti e trascrizione in casa; Cancello versione 2; Telegram, Slack e WhatsApp; 18 agenti nuovi | Brief la sera prima di ogni incontro. Offerta in bozza entro un'ora. "Cosa ci siamo detti con X?" da Claude Team. Bandi ogni mattina. Posta smistata. Gli stessi agenti su Telegram, Slack e WhatsApp. 32 agenti al lavoro |
| **4. Organizzazione, newsletter e Buzz** | 36-40 | F4-F5 | Newsletter e programmazione dei post sul nostro server; banca dei token per persona; skill proposte dagli agenti e approvate da una persona; Buzz sul banco di prova, collegato alla stessa bacheca; 10 agenti nuovi | Prima newsletter dopo il sì. Risposte sulla pagina aziendale in carta. Mappa dei processi. Buzz come stanza degli agenti sul banco di prova; diventa quella ufficiale quando non perde più risposte e ha approvazioni funzionanti. 42 agenti |
| **5. Vendite e voce** (solo con parere legale e lead reali) | 41-48 | F5 | "Andrea" con centralino e linea italiana, prima sulla CPU e poi sulla seconda GPU; pipeline pesata e portale clienti; Coach vendite, Pipeline, Clienti simili | Una lead di prova viene richiamata entro 90 secondi e l'appuntamento è nel CRM. Chiamate in entrata con l'esito nel canale vendite. Coaching visibile solo a chi ha fatto la call. 46 agenti |
| **6. Le altre automazioni** | 49-53 | F5 | Firma elettronica e fatturazione sul nostro server; assistente personale per chi lo vuole; prova di Paperclip; 11 agenti nuovi | Dal contratto all'incasso senza lavoro a mano. Ogni progetto chiuso diventa un caso studio. Tutti i 57 agenti nel registro |

**Oggi si impegnano solo le fasi 0 e 1, cioè le prime 8 settimane.** Le altre fasi si finanziano una per volta, sui risultati, e ogni funzione resta nel piano con la sua fase. Dopo la fase 6 resta una manutenzione continua: aggiornamenti dell'Agent SDK, del Cancello e dei servizi, agenti nuovi.

**Il banco di prova.** Il pilota non aspetta il board e non lo riordina. Nelle settimane 5-8 gira su una macchina di prova nella rete del laboratorio, con una chiave API limitata e un tetto di spesa, e salva solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata. Se Michele anticipa il posto per gli agenti sul server, il passaggio si anticipa.

**La verifica della settimana 8.** Due gruppi di criteri.

- **Tecnici**: tre agenti lavorano una settimana senza scambiarsi le sessioni; nessun effetto esce senza una carta del Cancello, anche nei dieci scenari di prova; una carta lasciata ferma la notte riprende il lavoro giusto al mattino; l'approvazione arriva dal telefono con l'identità giusta; la spesa resta nel tetto; un aggiornamento dell'Agent SDK passa i dieci scenari entro 14 giorni; sul banco di prova non resta salvato nessun dato rosso. Se un criterio fallisce, due settimane per correggere; se il problema è di struttura, proviamo Hermes sullo stesso banco con gli stessi scenari e decidiamo sui numeri.
- **Commerciali**: decisione sull'email presa e casella attiva; follow-up di tutte le call del periodo inviato entro 24 ore; carte decise entro 24 ore; almeno 8 post dei founder pubblicati nelle settimane 4-8; numeri del lunedì compilati ogni settimana; tutti e quattro usano Claude Team ogni giorno; SersanOutreach sicuro su identità e MFA. Da subito misuriamo anche quanto tempo passa oggi tra una lead e la prima risposta, per avere un punto di partenza.

**La verifica della settimana 21.** Prima di passare alla memoria con i dati dei clienti: gli stessi criteri tecnici, sul server; la revisione esterna di Cancello, motore e bot fatta, con i rilievi gravi chiusi; nessuna risposta del lavoro di una persona finita in un canale aperto a tutti; tutti i servizi nuovi in inventario, con le patch entro 14 giorni; il backup 3-2-1 in funzione, con una prova di ripristino riuscita; la RAM misurata e la decisione d'acquisto presa.

**Prima il funnel.** Se alla settimana 8 l'email non è ancora attiva e i founder non pubblicano, facciamo comunque le fasi 2 e 3, utili anche al funnel, e la fase 5 aspetta: "Andrea" e la pipeline pesata hanno senso solo con lead vere.

# 12. Quanto costa

## 12.1 Costi mensili

Prezzi IVA esclusa, rilevati il 24 e 25 ottobre 2026 e, per l'hardware e la linea di riserva, il 7 e l'8 novembre; cambio 1 $ = 0,8934 € e 1 £ = 1,1872 €. Con tutto sul nostro server escono Slack Pro, Claude in Slack, Notion, Hermes Cloud, Recall.ai, ElevenLabs, il password manager, i backup in cloud e Google Workspace, perché abbiamo M365. Quanto spendiamo in più rispetto a oggi:

| Periodo | € al mese in più | Cosa comprende |
|---|---|---|
| Fasi 0-1 e inizio della 2, finché Azure resta accesa | ≈ 135 (circa 141 con un server a pagamento per l'accesso) | Proxmox Community (20); IP fisso (fino a 10); corrente del rack, cioè server, firewall, UPS, rete e backup in sede, stimata con prudenza a 400 W (circa 105); macchina esterna per l'accesso (0 sul piano gratuito di Oracle; 6,49 con un server a pagamento) |
| Fase 2, con Azure spenta | da ≈ -15 a ≈ +20 | circa 150 € in meno di Azure; Jira Standard (0-28) |
| Fasi 3-4 | da ≈ -1 a ≈ +70 | corrente della RAM in più (6-10); WhatsApp (7-12); Slack (0-27); invio della newsletter (meno di 1) |
| Fasi 5-6, con Andrea | da ≈ 46 a ≈ 168 | linea italiana di Andrea (44-90); corrente della seconda GPU (3-8) |

Le API di Claude restano dentro i crediti finché bastano. Possono aggiungersi:

| Voce | € al mese |
|---|---|
| Fine dell'anno gratuito di Claude Team | 447 con 5 posti premium; 357 con 4; 214 con 2 premium e 2 standard |
| API di Claude senza crediti | circa 196 (forbice 90-250), con un tetto a 250 |
| Instantly, se oggi non è già pagato | 69 |
| Strumenti commerciali fuori dal board (Apollo, Metricool, Apify, moda.app, Higgsfield; Perplexity con il prezzo ancora da trovare) | fino a 188; con il consiglio della decisione 15 circa 146 fino alla fase 4, poi circa 86 |
| Teams, se manca dal piano M365 | 6-14 |
| Linea internet di riserva, se la aggiungiamo (decisione 13) | 10-11 con il 4G/5G; 31 con Starlink |
| Abbonamenti Proxmox per il firewall e per i due backup, se Michele li sceglie (decisione 17) | fino a circa 103 |
| Account Claude personale per l'assistente personale, facoltativo | 15-18 a persona |
| Premio mensile | 50-100 |

**Listino a regime**, nella fase 6: circa 479-583 € al mese, contro i circa 968 € della prima versione. Motore sull'Agent SDK o Hermes costano uguale: la licenza è zero in entrambi i casi e si paga solo l'API.

| Voce del listino | € al mese |
|---|---|
| Proxmox Community, 2 processori | 20 |
| Jira Standard per 4 persone (0 se basta il piano gratuito) | 28 |
| IP fisso | 0-10 |
| Macchina esterna per l'accesso (Oracle: 0; un server a pagamento: 6,49) | 0-6,49 |
| Corrente del rack | 105 |
| Corrente di RAM e seconda GPU | 9-18 |
| API di Claude, nei crediti finché durano | 196 |
| Andrea: linea italiana, Registro delle opposizioni, modelli | 44-90 |
| WhatsApp verso i clienti | 7-12 |
| Invio della newsletter | meno di 1 |
| Slack | 0-27 |
| Instantly | 69 |
| **Totale di listino** | **circa 479-583** |

## 12.2 Costi una tantum

| Voce | Quando | € IVA esclusa |
|---|---|---|
| Parere legale unico | fase 0, i punti del pilota entro la settimana 3 | tetto 2.500, con due preventivi |
| Credito API prepagato, se i crediti finiscono | fase 0 | 0-223 |
| Backup in sede: case e dischi per il Proxmox Backup Server che Michele monta con pezzi suoi (board) | subito: Michele sta già recuperando i pezzi | circa 165-500 |
| Chiavi di sicurezza FIDO2, due a persona (board) | subito, F1 del board | 232-464 |
| Piccoli accessori (board) | subito | 0-200 |
| Batterie nuove per l'UPS, solo se il test di autonomia all'arrivo va male: quelle montate sono usate e senza garanzia (board) | all'arrivo dell'UPS | circa 140 con batterie compatibili, fino a circa 550 con il kit originale HPE |
| **Oggi, in tutto** | | **circa 2.900-3.890** (prima erano fino a 5.016), più 140-550 se servono le batterie dell'UPS |
| Backup fuori sede a casa di Michele (Terra Noa): il piccolo nodo del board, che ospita la copia su un disco interno e fa anche da firewall della rete di Terra Noa (Starlink, sensori, telecamere) | entro marzo 2027 | circa 240-250 |
| Poi un Proxmox Backup Server più grande a Terra Noa, con i dischi (board) | quando servirà più spazio | circa 690-930 |
| Revisione esterna di sicurezza di Cancello, motore e bot | entro la settimana 21 | indicativo 3.560-5.940 (£3.000-5.000), con due preventivi |
| RAM: altri 192 GB, 12 moduli uguali a quelli montati | prima della fase 3, settimana 22 | circa 690-830 |
| Seconda GPU RTX PRO 2000 Blackwell da 16 GB, con il riser secondario e la staffa se mancano | quando il prezzo scende: conviene dalla fase 3, al più tardi all'inizio della fase 5 (sezione 6.4) | circa 880-1.220 |
| Linea internet di riserva (decisione 13) | consigliata prima della fase 5 | 4G/5G: 77-200, più 10-11 € al mese; Starlink: 349, più 31 € al mese |
| Vivavoce da sala per le riunioni dal vivo | fase 3 | 100-250 |
| Attivazione della linea di Andrea | fase 5 | 7-14 |

L'hardware principale è già comprato, compresi firewall e UPS da rack: Michele ha speso circa 2.975 € dei 3.200 € del budget del board (cifre del board, con l'IVA d'importazione), e per l'UPS ha preso un HPE R1500 G5 usato a 255 € invece dell'Eaton da 937-1.144 € IVA esclusa che avevamo messo in conto. Della prima versione non servono più gli accessori HPE, i dischi e la GPU grande da circa 2.500 € per i modelli locali: al suo posto c'è la seconda GPU da 16 GB della sezione 6.4.

Restano spese del board che non servono al sistema di agenti e si decidono a parte: il secondo server di Michele (fino a 1.500 €, circa 38 € al mese di corrente) e, se un giorno servirà più di 1 Gbit sul firewall, un modulo di rete più veloce (circa 420-500 €).

## 12.3 Cosa ci restituisce

Cosa il sistema ci toglie di mano:

| Attività | Oggi | Con il sistema |
|---|---|---|
| Follow-up, CRM e to-do dopo ogni call | a mano, quando si trova il tempo | revisione e sì |
| Brief prima degli incontri | ricerca fatta di corsa o non fatta | brief pronto da leggere |
| Proposte | scritte da zero | bozza da rifinire |
| Marketing: idee, bozze, calendario, numeri | senza un titolare dal 30 settembre | revisione e sì |
| Report, coordinamento, ricerca di informazioni | sparsi tra chat, mail e persone | debrief e domande alla memoria |
| Posta e appuntamenti | smaltiti a mano | posta smistata, risposte e inviti pronti per il sì |

È lavoro che oggi facciamo a mano quando c'è tempo, o che resta fermo, per una spesa in più che, spenta Azure, resta sotto i 170 € al mese finché valgono i crediti API e l'anno gratuito di Claude Team (dopo, fino a circa 615 € con cinque posti premium, più le API se i crediti finiscono), oltre al nostro tempo di sviluppo. Quanto ci restituisce davvero lo misuriamo dalla fase 1 con il registro degli agenti. Il valore più grande però non è il tempo: è richiamare una lead in 90 secondi invece che in ore, ed è avere una pipeline vera.

# 13. Rischi e come li gestiamo

| Rischio | Come lo gestiamo |
|---|---|
| **Il tempo di chi amministra il server**: il sistema aggiunge 11-13 servizi e 3 reti nuove al perimetro Cyber Essentials, con le patch entro 14 giorni | Prima della fase F4 entrano solo i servizi del pilota; ogni servizio ha un responsabile delle patch e un posto nell'inventario; installazione ed esercizio dei servizi nuovi sono nei giorni della sezione 15, mentre l'infrastruttura del board la porta avanti Michele e non è contata |
| **Cancello, motore e bot sono codice scritto su misura** e nessuno lo ha ancora rivisto | Dieci scenari di prova a ogni aggiornamento; revisione esterna entro la settimana 21; Mattia sul codice dal primo giorno |
| **L'Agent SDK cambia quasi ogni giorno** | Versione fissata; aggiornamento ogni due settimane, dopo i dieci scenari, entro i 14 giorni |
| **Il motore non regge** | Verifiche alle settimane 8 e 21; Hermes come uscita già stimata, provato sullo stesso banco di prova |
| **LiteLLM custodisce tutte le chiavi**, e a marzo 2026 ne sono circolate versioni compromesse | Versione fissata e controllata; esce solo verso Anthropic; pannello raggiungibile solo dalla rete di gestione; chiave principale tra i segreti, con rotazione |
| **Il bot di Teams senza Azure** può dare errori di registrazione | Prova nella fase 0; registrazione Azure Bot gratuita, senza macchine accese; in ultima istanza la pagina del Cancello, con gli avvisi in Teams |
| **Dati personali verso Claude Team**, che non ha un registro di audit | Decisione nel parere e nella valutazione d'impatto entro la settimana 3; il rosso arriva a Claude Team solo oscurato |
| **Iniezioni di prompt** da mail, trascrizioni e messaggi | Chi legge testo di terzi non ha strumenti che agiscono; nessuno strumento invia senza il Cancello |
| **RAM finita** con tutte le funzioni | Misura con un tetto di sessioni; altri 192 GB prima della fase 3; leve per rimandare l'acquisto |
| **Una sola GPU fino all'arrivo della seconda**, prestata ogni tanto alla postazione di prova del laboratorio (Experimental-1) | I lavori della GPU aspettano in coda finché torna libera; seconda GPU da 16 GB dalla fase 3, al più tardi dalla fase 5; embedding e lavori a lotti sulla CPU quando serve |
| **Piattaforme di call che bloccano i bot** non registrati | Per le nostre call la trascrizione nativa di Teams; registrazione sul PC come riserva |
| **La voce italiana di Andrea** non abbastanza buona | Prova d'ascolto prima; voci migliori sulla seconda GPU; in ultima istanza una voce in cloud, come eccezione decisa da voi |
| **Il funnel è vuoto**: 11 lead, 0 meeting, campagna ferma dal 9 settembre | Decisione sull'email e casella attiva nella fase 0; criteri commerciali alla settimana 8; "Andrea" solo con lead vere |
| **Calendario lungo**, circa un anno | Valore dalla prima settimana; fasi finanziate una per volta; con più capacità di sviluppo il calendario si accorcia (sezione 15) |
| **Tempi del board** non ancora fissati | Banco di prova nel laboratorio; il posto per gli agenti sul server come richiesta a Michele |
| **Registrazioni, "Andrea", coaching** e norme sul lavoro | Parere legale: i punti del pilota entro la settimana 3, il resto prima della fase 2; "Andrea" si dichiara sempre AI; coaching privato |
| **"Andrea" e la regola del piano marketing** che vieta voci sintetiche nelle call | Un'eccezione decisa da voi (decisione 10): solo richiamate chieste dalla lead, voce dichiarata, il brief resta letto da un founder |
| **Fine del supporto HPE** dello chassis (ottobre 2029 secondo le fonti HPE consultate da Michele, da confermare con il numero di serie; le stime pubbliche partono da marzo 2028) | Macchine virtuali con backup: si spostano su un server nuovo senza rifare nulla; Michele prevede il secondo server a dicembre |
| **Il firewall Sophos è un modello fuori supporto**: Sophos non lo aggiorna più, e BIOS e processore non ricevono più correzioni | Il software che ci gira, Proxmox e OPNsense, è aggiornato. Per Cyber Essentials chiediamo prima per iscritto all'ente di certificazione se accetta questa configurazione; se non la accetta, OPNsense passa su un piccolo computer ancora supportato dal produttore (spesa da preventivare) |
| **Una sola linea internet**: se cade la fibra, gli agenti si fermano, perché ragionano con Claude via internet, e Andrea non risponde | Nulla si perde: lavori e carte aspettano e ripartono quando la linea torna. Linea di riserva 4G/5G prima della fase 5 (decisione 13); l'accesso da fuori passa dalla macchina Oracle e funziona anche sulla linea di riserva |
| **Mancanza di corrente**, con le batterie dell'UPS usate e senza garanzia | Dopo 3 minuti l'UPS spegne il server in modo pulito e tiene accesa la rete; al ritorno della corrente la rete riparte da sola, mentre il server va riacceso a distanza, a meno che Michele non lo imposti per ripartire da solo: fino ad allora gli agenti, e dalla fase 5 Andrea, restano fermi. Test di autonomia e di riaccensione all'arrivo dell'UPS, e batterie nuove se servono |
| **Backup non ancora completo**: la copia in sede va montata, quella a casa di Michele arriva a marzo 2027 | Nessun dato dei clienti resta sul server prima della verifica della settimana 21, che chiede il 3-2-1 con una prova di ripristino |
| **Buzz è giovane** | Resta sul banco di prova finché non perde più risposte e non ha approvazioni funzionanti; intanto la stanza degli agenti è il canale "Agenti" in Teams |
| **WhatsApp**: le soluzioni non ufficiali portano al blocco del numero | Solo l'API ufficiale di Meta, con un numero aziendale dedicato |
| **Troppi agenti per quattro persone** | Ogni agente ha un responsabile, un tetto e una riga nel registro; un agente che non serve si spegne dal registro |

# 14. Le decisioni che vi chiediamo

Solo decisioni di budget, abbonamenti, acquisti e integrazioni. Le scelte tecniche le abbiamo studiate noi (sezioni 5 e 6); quelle sull'infrastruttura restano di Michele.

| # | Decisione | Consigliato | Costo |
|---|---|---|---|
| 1 | Avviare le fasi 0 e 1, con la verifica alla settimana 8 | Sì | Le prime 8 settimane; la stima in giorni è nella sezione 15; nessun abbonamento nuovo oltre a quelli del board |
| 2 | Parere legale unico (email, registrazioni, dati verso Claude Team, "Andrea", coaching, firma elettronica, dati negli USA, backup a casa di Michele) | Sì, subito: i punti del pilota entro la settimana 3, il resto prima della fase 2 | tetto 2.500 €, con due preventivi |
| 3 | Tetto mensile delle API se i crediti non bastano, e credito prepagato | Sì | tetto 250 € al mese (stima 196 €); credito 0-223 € |
| 4 | Spese del board per backup, corrente e sicurezza: backup in sede (case e dischi), subito; batterie nuove per l'UPS, solo se il test all'arrivo va male; nodo di Terra Noa, che ospita la copia fuori sede e fa anche da firewall della rete di Terra Noa, entro marzo 2027; più avanti, quando servirà più spazio, un Proxmox Backup Server più grande a Terra Noa, con i dischi; chiavi FIDO2; accessori | Sì | circa 165-500 €; circa 140-550 €; circa 240-250 €; circa 690-930 €; 232-464 €; fino a 200 € |
| 5 | Revisione esterna di sicurezza di Cancello, motore e bot, prima che i dati dei clienti restino sul server | Sì, con due preventivi | indicativo 3.560-5.940 € (£3.000-5.000), entro la settimana 21 |
| 6 | Jira Standard per 4 persone, se oggi siamo sul piano gratuito | Sì, dalla fase 2 | 28 € al mese |
| 7 | Macchina esterna per l'accesso da fuori (NetBird, Pangolin, monitoraggio): Michele ha scelto Oracle Cloud a Milano | Sì | 0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento |
| 8 | Canali in più: Telegram, Slack, WhatsApp con numero dedicato | Sì, dalla fase 3 | Telegram 0 €; Slack 0 o 27 € al mese; WhatsApp circa 7-12 € al mese |
| 9 | Invio della newsletter con un servizio di posta esterno | Sì, dalla fase 4 | meno di 1 € al mese |
| 10 | Voce di "Andrea": eccezione alla regola delle voci sintetiche nelle call, con una linea telefonica italiana | Sì, dalla fase 5, solo per chi chiede di essere richiamato, con voce dichiarata, parere e lead vere; la voce clonata di un collega solo con il suo contratto separato e revocabile | 44-90 € al mese; attivazione 7-14 € |
| 11 | RAM: altri 192 GB, 12 moduli uguali a quelli montati | Sì, prima della fase 3 o quando il margine scende sotto i 5 GB | circa 690-830 € |
| 12 | Seconda GPU RTX PRO 2000 Blackwell da 16 GB, con il riser secondario e la staffa se mancano | Sì: Michele la prende più avanti, aspettando che il prezzo scenda; noi proponiamo di comprarla appena torna sotto i 1.000 € IVA inclusa, dalla fase 3, e comunque entro l'inizio della fase 5, anche se il prezzo non è sceso (sezione 6.4) | circa 880-1.220 € |
| 13 | Linea internet di riserva | Sì, 4G/5G con una SIM dati aziendale, prima della fase 5; Starlink solo se in ufficio il segnale mobile è scarso. A chi intestare la SIM lo decidete voi: TIM chiede una partita IVA italiana e il contratto MultiBusiness, per Iliad il requisito non l'abbiamo verificato | 4G/5G: 77-200 € una tantum e 10-11 € al mese; Starlink: 349 € e 31 € al mese |
| 14 | Vivavoce da sala per le riunioni dal vivo | Sì, nella fase 3 | 100-250 € |
| 15 | Strumenti commerciali fuori dal board | Apollo e Higgsfield restano; Metricool finché Postiz non è pronto (fase 4); Apify sostituito da Firecrawl; moda.app sostituito da Claude Team; Perplexity da decidere con il prezzo; After Effects resta com'è oggi sul PC di Alberto, senza costi in più | fino a 188 € al mese; con il consiglio circa 146 € fino alla fase 4, poi circa 86 € |
| 16 | Posti Claude Team alla fine del bundle | Ridecidere alla scadenza: gli agenti usano la chiave API, quindi bastano meno posti premium | 447 € al mese con 5 premium; 357 con 4; 214 con 2 premium e 2 standard |
| 17 | Abbonamenti del board: Proxmox sul server; Proxmox sul firewall e sui due Proxmox Backup Server, in sede e a Terra Noa, se Michele li sceglie; IP fisso | Sì per Proxmox sul server e IP fisso; firewall e backup secondo la scelta di Michele | 20 € al mese; firewall circa 10 € al mese; 46,67 € al mese per ogni Proxmox Backup Server, circa 93 € per tutti e due; fino a 10 € al mese |
| 18 | Teams nel piano M365, se oggi manca | Sì, se manca | 6-14 € al mese |
| 19 | Premio mensile per chi costruisce con l'AI | Sì | 50-100 € al mese |
| 20 | Assistente personale: account Claude personale per chi lo vuole | Sì, facoltativo; decidere se lo paga l'azienda | 15-18 € al mese a persona |
| 21 | Firma elettronica qualificata, solo se il parere la chiede per certi contratti | Dopo il parere | a preventivo |
| 22 | Strumento di fatturazione | Quello che usiamo già, se fa al caso; altrimenti uno sul nostro server | 0 € o il canone dello strumento scelto |
| 23 | Un mese di prova di Grok Bot, su soli dati pubblici | Facoltativa | circa 54 € una volta |

**Cosa verifichiamo noi nella prima settimana**, senza chiedervi nulla: cosa include esattamente il bundle startup (crediti mensili e data di scadenza), quale piano M365 e quale piano Jira abbiamo oggi, quanto del kit commerciale paghiamo già. Chiediamo anche ad Anthropic la conservazione zero dei dati delle API, che è gratuita. Le domande tecniche per Michele sono in un file a parte, `DOMANDE-PER-MICHELE.md`.

# 15. La stima dei giorni di sviluppo

È l'unica stima dei giorni di lavoro del documento: i giorni di sviluppo che servono per costruire il sistema, fase per fase; le settimane delle altre sezioni sono il calendario. I giorni sommano il lavoro di tutte le persone che sviluppano, in parallelo: per questo in una fase possono essere più dei giorni di calendario. Nella tabella il valore più basso è la stima di base, il più alto comprende una riserva di circa un terzo. L'infrastruttura del board di Michele non è contata: la porta avanti lui.

| Fase | Settimane | Giorni di sviluppo | Esercizio e patch |
|---|---|---|---|
| 0. Valore subito e prove | 1-4 | 18-24 | 0 |
| 1. Pilota su banco di prova | 5-8 | 22,5-30 | 0 |
| 2. Pilota sul server e squadre che si parlano | 9-21 | 58,5-78 | 6,5 |
| 3. Memoria, call, vendite preparate e canali | 22-35 | 61,75-82 | 7 |
| 4. Organizzazione, newsletter e Buzz | 36-40 | 26,5-35 | 2,5 |
| 5. Vendite e voce | 41-48 | 38-51 | 8 |
| 6. Le altre automazioni | 49-53 | 24-32 | 5 |
| **Totale** | **1-53** | **circa 249-332** | **29** |

- **Oggi vi chiediamo le fasi 0 e 1**: 40,5-54 giorni di sviluppo in 8 settimane, come nella prima versione.
- **Perché il totale cresce rispetto alla prima versione** (110-147 giorni per le fasi 0-5): ora tutto è sul nostro server e nessuna funzione è tolta. Chat, bot nelle call, voce di Andrea, newsletter, programmazione dei post, firma elettronica e fatturazione li costruiamo e li gestiamo in casa invece di pagarli in abbonamento, e i giorni per le patch e l'esercizio sono contati.
- **La prova di Buzz** occupa circa 6 giorni nella fase 4.
- **Se il motore non reggesse** alle verifiche, una prova di Hermes sullo stesso banco costa 6-8 giorni; usarlo al posto del motore costa 26-33 giorni con la riserva, mentre Cancello, memoria, bot e skill restano.
- **Con più capacità di sviluppo** dalla fase 2 il calendario scende da circa 53 a circa 42 settimane.
- **Dopo la fase 6** l'esercizio resta intorno a un giorno a settimana: aggiornamenti dell'Agent SDK, del Cancello e dei servizi, agenti nuovi.

# Appendice A. Copertura completa della visione

Ogni funzione dell'idea, con il componente che la realizza e la fase. Le sigle corrispondono alla lista delle funzioni dell'idea. Le voci K sono dettagli dell'idea resi espliciti; le voci L sono automazioni in più che proponiamo noi.

| Voce | Funzione | Come la facciamo | Fase |
|---|---|---|---|
| J1 | Outreach, marketing, contenuti, task, progetti e chiamate in un solo sistema multi-agente | motore unico sull'Agent SDK, una bacheca, una memoria, un Cancello, Teams con la Porta | 2-6 |
| J2 | Ogni squadra di agenti ha il suo compito | registro dei profili con responsabile; un team LiteLLM e un bot Teams per squadra | 1-2 |
| J3 | Squadra outreach con un agente per le email | Agente email su SersanOutreach (MCP) e Instantly. Serve ancora: email attiva dopo la decisione con il legale | 0 (email), 3 (agente) |
| J4 | L'agente email parla con quello delle proposte, che parla con quello delle chiamate | bacheca con passaggi e freno, specchio nel canale "Agenti" | 2-3 |
| J5 | L'agente delle chiamate entra in automatico in ogni call e trascrive tutto | la trascrizione che Teams fa già per le nostre call; Vexa, un bot sul nostro server, per Teams di altri, Meet e Zoom; per le riunioni dal vivo la registrazione dal telefono, collegato al server in modo sicuro. Serve ancora: il cliente deve ammettere il bot; riserva con la registrazione sul PC; RAM per Vexa | 1 (Teams), 3 (Vexa) |
| J6 | Brief prima e dopo la call con tutto il contesto, slide per noi e per il cliente | Agente brief e Agente slide con i template SerSan; le stesse skill in Claude Team. Serve ancora: template SerSan da preparare | 0 (skill), 3 (agenti) |
| J7 | Il marketing collabora con l'outreach (ricerca concorrenza, metriche) e con la generazione di video, slide e contenuti | squadre Marketing e Studio sul motore; Firecrawl; Postiz; HyperFrames in locale; passaggi con l'Outbound in bacheca. Serve ancora: Higgsfield come eccezione per i video; Metricool finché Postiz non è pronto | 2-4 |
| J8 | Squadra progetti e task | Jira, Project manager, Agente task, Report cliente, Onboarding, Sviluppatori. Serve ancora: Jira Standard se servono permessi diversi | 2, 4 |
| J9 | Chat di gruppo come Buzz, collegata a Slack, Telegram e WhatsApp | Teams con la Porta e nove bot di squadra; Telegram, Slack e WhatsApp dallo stesso codice; Buzz nella sandbox di prova del laboratorio (Experimental-2), sulla stessa bacheca. Serve ancora: sì di Michele alle eccezioni; verifica Meta Business; la sandbox di prova (fase F5 del board) | 2, 3, 4 |
| A1 | Tutte le riunioni registrate e trascritte, dichiarandolo | Teams via Graph, Vexa, telefono, trascrizione in casa, avviso in tre livelli. Serve ancora: parere sull'art. 4 dello Statuto se ci sono dipendenti; DPIA | 1-3 |
| A2 | Second brain relazionale | BookStack per i testi, PostgreSQL per i dati, MCP memoria. Serve ancora: MariaDB da aggiungere al board | 2 |
| A3 | Database vettoriale che "connette i momenti" | Qdrant con BM25 e reranker, MCP RAG con l'identità della persona. Serve ancora: pipeline del board (fase F4) | 3 |
| A4 | Orchestratore sul nostro server | motore sull'Agent SDK, prima sul banco di prova poi sul server. Serve ancora: posto agenti o fine di F3 per passare sul server | 1-2 |
| A5 | Agenti divisi per ruolo: raccolta, pulizia, indicizzazione, azione | squadra Memoria più pipeline del board; squadre d'azione | 3 |
| A6 | Agenti che imparano da soli | skill in git; gli agenti scrivono proposte nella cartella "proposte"; revisore settimanale; una persona approva con una PR | 4 |
| A7 | Chat condivisa tra agenti | specchio della bacheca nel canale "Agenti", @menzioni; Buzz in pilota | 2 |
| B1 | Punti e prossimi passi nel canale del cliente | canale privato Teams subito; canale condiviso, mail, Slack o WhatsApp dopo la carta. Serve ancora: canali condivisi fra organizzazioni da provare | 1-3 |
| B2 | Opportunità creata nel CRM | esecutore del Cancello sull'MCP di SersanOutreach, operazione "crea deal". Serve ancora: presa MCP raggiungibile dal server, con un accesso per squadra | 2 |
| B3 | Mail di follow-up al cliente | bozza, carta, esecutore Outlook via Graph, solo al dominio del cliente. Serve ancora: permesso d'invio limitato alle caselle giuste | 1 |
| B4 | To-do al team | Jira, scrittura interna del Cancello | 2 |
| B5 | Tutto in autonomia | regole "Sempre" dopo 20 sì uguali, con scadenza di 30 giorni. Serve ancora: la vostra scelta di quali messaggi ai clienti possono diventare Sempre, dopo il parere legale | 2-6 |
| C1 | Debrief del mattino | Report del mattino alle 7:00 in Teams e per mail, numeri da PostgreSQL | 1 |
| C2 | Un agente in ogni call, anche al posto di chi manca | registrazione automatica delle nostre riunioni Teams; Vexa per le altre. Serve ancora: provare se Teams registra senza nessuno di SerSan collegato | 3 |
| C3 | Analisi della call con Claude | sessione post-call senza strumenti, uscita a schema | 1 |
| C4 | Dettatura | dettatura delle app Claude; Agente dettatura; note vocali dal telefono trascritte in casa | 0, 2, 3 |
| C5 | Registro di tutti i meeting dell'azienda e pipeline emersa | tabella dei meeting in PostgreSQL, vista in Grafana | 1-2 |
| C6 | Le regole di lavoro di ciascuno, lette dagli agenti | pagina "Come lavoro" in BookStack; istruzioni di squadra; istruzioni dei progetti Claude Team | 0, 2 |
| D1 | CRM fatto in casa con pipeline pesata | probabilità per stadio dagli eventi di SersanOutreach. Serve ancora: storico: oggi 0 vinti e 91 deal senza valore; pesi dichiarati fino a 30-50 chiusure | 5 |
| D2 | Brief pre-meeting dall'email della persona | SersanOutreach con il suo arricchimento dei contatti, Firecrawl, MCP RAG, posta; post LinkedIn con una via consentita (l'estensione di SersanOutreach nel browser di chi lavora, oppure un fornitore di dati come Apollo). Serve ancora: email attiva per le aperture; Apollo e Perplexity come eccezioni; la via per LinkedIn confermata dal parere legale | 3 |
| D3 | Storico della relazione | MCP RAG con filtro cliente, tabella dei meeting | 3 |
| D4 | Slide automatiche | skill delle slide in Claude Team; Agente slide sul motore. Serve ancora: template SerSan; moda.app solo se ammesso | 0, 3 |
| D5 | Offerta commerciale automatica | skill dell'offerta in Claude Team; Agente proposte su Opus con catalogo in BookStack e PostgreSQL; carta a Michele | 0, 3 |
| E1 | Mettere in conto il tempo per imparare e costruire | piano con una riserva di un terzo (sezione 15) ed esercizio dichiarato | tutte |
| E2 | Costruire ora, finché i token costano poco | Claude Team dalla settimana 1; prezzi rilevati il 24 e 25 ottobre 2026; versioni fissate | tutte |
| E3 | Policy AI e banca dei token | tetto di spesa sul banco di prova; LiteLLM per agente, squadra e persona; avviso all'80 % dal Cancello, stop al 100 %. Serve ancora: LiteLLM (fase F4 del board o posto agenti) | 1, 2, 4 |
| E4 | Imparare a usarla | formazione documentata per i quattro (AI Act art. 4) | 0 |
| F1 | Lettura dei metadati del lavoro (M365), con le tutele per le persone | report e registri di M365 aggregati, al massimo 21 giorni. Serve ancora: individuare le API di M365; accordo di ciascuno | 4 |
| F2 | Interviste guidate alle persone | Intervistatore in chat privata di Teams | 4 |
| F3 | Mappa dei processi aziendali | Mappatore processi, libro "Processi" in BookStack | 4 |
| F4 | Ore implicite per processo e classifica delle automazioni consigliate | analisi mensile su Opus, ore dei processi registrate in PostgreSQL | 4 |
| F5 | AI per tutti, non solo per i tecnici | Claude Team, Teams, Open WebUI (la chat con i modelli sul nostro server) con budget per persona | 0 |
| G1 | Call di vendita in un canale | canale Teams "Call di vendita" dal post-call | 3 |
| G2 | Fit score del prospect | qualificatore di SersanOutreach esteso alle call. Serve ancora: volumi di call | 5 |
| G3 | Valutazione della call e consigli | Coach vendite, senza stima delle emozioni, vietata dall'AI Act. Serve ancora: parere legale | 5 |
| G4 | Il report va a chi ha fatto la call (e al responsabile, in forma aggregata) | chat privata di Teams; al responsabile solo dati aggregati; i permessi della persona decidono chi vede. Serve ancora: parere legale per andare oltre gli aggregati | 5 |
| G5 | "Andrea" richiama in 90 secondi, 24/7 | Asterisk, Pipecat, Claude Haiku, ascolto e voce in casa; modulo del sito via n8n. Serve ancora: operatore telefonico italiano (eccezione); prova della voce italiana; parere legale; seconda GPU consigliata; linea internet di riserva consigliata prima della fase 5 (decisione 13); consenso alla richiamata in ogni modulo (sito, campagne, eventi); per la versione con la voce clonata di un collega, il suo contratto separato e revocabile | 5 |
| G6 | Impara dai rifiuti | analisi settimanale, nuove aperture via Cancello, test A/B. Serve ancora: volumi | 5 |
| G7 | Più conversione e risposte più veloci | tempo di richiamata e meeting nel debrief | 5 |
| G8 | Perché si chiude o si perde, passato al marketing | Analista vinto/perso → Editoriale nella bacheca. Serve ancora: chiusure: oggi 0 | 3 |
| G9 | 100+ agenti in organigramma | registro dei profili, Grafana, pagina BookStack, bot di squadra. Serve ancora: RAM oltre le 16 sessioni insieme | 2-6 |
| G10 | Un superpotere individuale, organizzativo e aziendale | il risultato dell'insieme | tutte |
| H1 | Formarsi e sperimentare | Claude Team, Open WebUI, la sandbox di prova del laboratorio (Experimental-2). Serve ancora: la sandbox di prova (fase F5 del board) | 0-6 |
| H2 | Non delegabile: tutti cambiano modo di lavorare, a partire dai CEO | i CEO approvano dal telefono e leggono il debrief ogni mattina | 1 |
| H3 | Assessment delle competenze | assessment iniziale in Claude Team; Intervistatore per ruolo | 0, 4 |
| H4 | Ambassador con più risorse | tetto di spesa più alto in LiteLLM | 4 |
| H5 | Tutti costruiscono qualcosa | ognuno possiede almeno un agente nel registro | 4 |
| H6 | Premio mensile a chi costruisce con l'AI la cosa che cambia di più il lavoro | classifica dal registro degli agenti. Serve ancora: il budget del premio (decisione 19) | 4 |
| H7 | Le licenze non bastano: serve cambiare il modo di lavorare | punto del venerdì, regole di ciascuno, misura mensile (sezione 10) | tutte |
| I1 | Il contesto fa la qualità | memoria divisa per tipo e una sola porta di ricerca | 2-3 |
| I2 | Non fermarsi alla versione base degli strumenti | skill, server MCP e profili su misura | 2-6 |
| I3 | Aree dove l'AI non entra | classi negate nel Cancello; regole di divieto che valgono sempre | 1 |
| I4 | Il marketing passa dal 70% ripetitivo al 70% creativo | Editoriale, Copywriter, Metriche, Pubblicatore | 2 |
| K1 | Il debrief di ieri e il piano di oggi come primo appuntamento del calendario | evento Outlook creato dall'esecutore | 2 |
| K2 | Un agente fissa gli appuntamenti che gli altri trovano («ho trovato tre nuove call») | annuncio nella bacheca e nel canale "Agenti"; l'Agenda manda gli inviti dopo il sì | 3 |
| K3 | Non rispondere più a mano alle mail | Smistatore posta su Graph con caselle limitate; invio dal Cancello. Serve ancora: accordo di ciascuno sulla propria casella | 3 |
| K4 | Chiedere alla memoria cosa si è detto in una call a cui non eravamo | Claude Team con l'MCP RAG; Capo di gabinetto in Teams. Serve ancora: regola sui dati rossi verso Claude Team (DPIA e parere) | 3 |
| K5 | Brief di intake e onboarding dei potenziali clienti | Agente intake da modulo, posta, WhatsApp | 3 |
| K6 | Slide per il cliente che raccontano la storia della relazione con noi | Brief, Slide, MCP RAG | 3 |
| K7 | Slide e documenti con il nostro stile, non con il formato standard che usano tutti | template SerSan in SharePoint; skill di brand in Claude Team e sul motore. Serve ancora: template da preparare | 0 |
| K8 | Un portale clienti costruito con Claude Code, con pipeline e pipeline pesata | SersanOutreach come portale, cruscotto della pipeline | 5 |
| K9 | Un agente che costruisce le newsletter | Agente newsletter e listmonk. Serve ancora: relay SMTP esterno | 4 |
| K10 | "Andrea" risponde anche alle chiamate e registra l'esito di ognuna | gruppo di squillo in Asterisk, poi Andrea; esito nel CRM e nel canale vendite. Serve ancora: come G5 | 5 |
| K11 | Capire perché una lead si chiude e replicarla su altri | Analista vinto/perso e Agente clienti simili. Serve ancora: volumi | 3, 5 |
| K12 | Formazione continua dei commerciali | piano mensile del Coach | 5 |
| K13 | Mappa dei processi e assessment usati anche per i clienti | Mappatore e Intervistatore in un'istanza separata per cliente. Serve ancora: istanza e dati separati da progettare | 4-6 |
| K14 | Dati finanziari e obiettivi nella memoria, usati per migliorare i processi | tabella degli obiettivi; numeri di Sirius in PostgreSQL via n8n; documenti nella memoria. Serve ancora: l'esportazione dei dati da Sirius (fiscale, clienti, documenti), prevista nella fase F4 del board | 3-6 |
| K15 | Gli acquisti automatizzati | Agente acquisti: fatture dei fornitori dalla posta, rinnovi; pagamenti sempre su carta. Serve ancora: strumento di fatturazione | 6 |
| K16 | Un assistente anche per la vita personale: calendario, viaggi, famiglia, salute | profilo privato senza memoria aziendale; dati di salute nell'account Claude personale. Serve ancora: consenso della persona | 6 |
| L1 | Contratto dall'offerta approvata, con firma elettronica | Agente contratti e DocuSeal. Serve ancora: valore legale della firma semplice nel parere; firma qualificata da fornitore esterno se serve | 6 |
| L2 | Fatture alla consegna, incassi e solleciti | Agente fatture sul sistema scelto con la decisione 22: Sirius, che ha già i dati fiscali e dei clienti, oppure Invoice Ninja sul nostro server. Serve ancora: chi fattura (UK, o SDI se c'è un soggetto italiano) e con quale sistema | 6 |
| L3 | Margini per cliente e per progetto, cassa, distanza dagli obiettivi | Controllo di gestione su PostgreSQL e Grafana. Serve ancora: i dati di Sirius esportati nella fase F4 del board | 6 |
| L4 | Bandi e finanziamenti per noi e per i clienti | pipeline bandi del board più Agente bandi | 3 |
| L5 | Assistenza ai clienti nella loro stanza | canale condiviso Teams, mail, WhatsApp o Slack; risposte su carta. Serve ancora: come B1 e J9 | 6 |
| L6 | Rinnovi, nuove fasi e clienti a rischio | Agente rinnovi su call, report e Jira | 6 |
| L7 | Ogni progetto chiuso diventa un caso studio | Agente casi studio; testimonianza chiesta dopo la carta | 6 |
| L8 | Commenti e messaggi della pagina aziendale | Community manager con Postiz. Serve ancora: accesso API alla pagina LinkedIn da verificare; Metricool come eccezione | 4 |
| L9 | Sito, articoli e SEO | Agente sito con PR su GitHub; deploy su Vercel fatto da una persona | 6 |
| L10 | Webinar ed eventi che portano lead | Agente eventi; webinar di Teams; inviti con listmonk; lead in SersanOutreach. Serve ancora: licenza dei webinar di Teams da controllare | 6 |
| L11 | Un agente che sorveglia il server | Sistemista in sola lettura sul monitoraggio del server e sull'inventario dei servizi (NetBox); patch come carte. Serve ancora: il monitoraggio del server (fase F3 del board) | 3 |
| L12 | Un allenatore che aiuta ciascuno a usare meglio gli agenti | Allenatore AI dal registro d'uso, visibile solo all'interessato | 6 |

**Lacune dichiarate.** La pipeline pesata (D1) oggi non ha storico su cui pesare: 0 deal vinti e 91 senza valore; finché le chiusure non sono 30-50 usa pesi dichiarati da Alessandro. Il brief (D2) parte con web, CRM e posta: le aperture delle mail arrivano quando l'email è attiva, e i post LinkedIn li leggiamo solo con mezzi consentiti. Il fit score (G2), il ciclo sui rifiuti (G6) e l'analisi vinto/perso (G8, oggi 0 deal chiusi) hanno bisogno di volumi che oggi non ci sono. "Andrea" parte con una voce sintetica. La versione fedele, con la voce clonata di un collega, la facciamo in casa con Qwen3-TTS sulla seconda GPU, nella fase 5, dopo la voce sintetica: servono il contratto separato e revocabile del collega e il via del parere legale. Il coaching (G4) al responsabile manda solo dati aggregati finché non abbiamo il parere legale. L'assistente personale (K16) tratta i dati di salute solo nell'account privato di chi lo sceglie: non entrano mai nella memoria aziendale né sul server.

# Appendice B. Le architetture e i giudizi

**Secondo giro, 25 ottobre, dentro il board di Michele.**

| Proposta | Lente visione | Lente commerciale | Lente tecnica | Lente sicurezza e privacy | Totale |
|---|---|---|---|---|---|
| 1. Motore sull'Agent SDK | 43 | 42 | 44 | 42,5 | **171,5** |
| 3. Claude Team al centro | 41 | 45 | 42 | 42 | 170 |
| 2. Hermes sul nostro server | 35 | 34 | 34 | 34 | 137 |

Ogni agente giudice ha dato da 0 a 10 punti su sei criteri: copertura della visione, tempo al valore, costo, affidabilità e manutenzione, sicurezza e privacy, aderenza al board di Michele. Il motore sull'Agent SDK vince in tre lenti su quattro. La lente commerciale preferisce di poco Claude Team al centro, perché dà valore prima: per questo la sua fase zero è entrata nel piano.

**I dissensi che abbiamo preso sul serio.**

- **Lente commerciale**: "il problema commerciale di oggi non è l'orchestratore, è il funnel vuoto". Da qui la decisione sull'email e la casella attiva nella fase 0, e i criteri commerciali alla settimana 8.
- **Lente tecnica**: "il collo di bottiglia non è il motore, è chi amministra il server". Da qui il tetto ai servizi prima della fase F4, un responsabile delle patch per ogni servizio e il pilota su un banco di prova che non riordina il board.
- **Lente sicurezza e privacy**: "la sicurezza della proposta scelta dipende da codice scritto su misura che nessuno ha ancora rivisto". Da qui la revisione esterna entro la settimana 21, le carte legate al testo e la chiave FIDO2 per le azioni più delicate.
- **Lente visione**: "una proposta che trasforma gli agenti in strumenti da aprire a mano tradisce l'idea". Da qui tutte le 57 figure come agenti veri, i nove bot di squadra e Buzz collegato alla stessa bacheca.

**Primo giro, 24 ottobre**, con le ipotesi di allora (Slack, Notion e diversi servizi in cloud): sette architetture valutate dagli stessi quattro tipi di giudici.

| Proposta | Lente visione | Lente commerciale | Lente tecnica | Lente privacy | Totale |
|---|---|---|---|---|---|
| A. Hermes + Cancello | 41 | 40 | 41 | 37 | **159** |
| F. Paperclip | 37 | 38 | 36 | 37,5 | 148,5 |
| G. Ibrido libero | 37 | 34 | 36 | 36,5 | 143,5 |
| B. buzz di Block | 36 | 33 | 35 | 36,5 | 140,5 |
| E. Claude-native | 34 | 31 | 37 | 38 | 140 |
| C. Grok Bot | 27 | 28 | 30 | 28 | 113 |
| D. OpenAI Dots | 26 | 25 | 27 | 27 | 105 |

Con il board di Michele il quadro è cambiato: tutto in casa, M365 al posto di Google e Slack, n8n e LiteLLM già previsti. La proposta Claude-native, allora seconda per la lente tecnica e prima per la privacy, è diventata il motore sull'Agent SDK.

**La critica finale.** Prima di consegnarvi il documento un agente critico ha controllato ogni voce della visione contro l'architettura scelta, e più giri di agenti revisori hanno ricontrollato numeri, coerenza e copertura, provando a smentire ogni rilievo prima di accettarlo.

# Appendice C. Il materiale di lavoro

Dietro questo documento c'è una cartella di lavoro interna: i rapporti di ricerca dei due giri, il board dell'infrastruttura di Michele e gli strumenti che producono questo PDF con il marchio SerSan. Quello che serve per decidere è qui. Le domande tecniche sull'infrastruttura sono in un file a parte per Michele, `DOMANDE-PER-MICHELE.md`.
