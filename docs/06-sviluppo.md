# Sviluppo: fasi, verifiche, giorni e rischi

Questo file è per chi deve capire e costruire SerSan Agent OS, il sistema di 57 agenti AI in nove squadre che gira sul server di SerSan ([proposta §1](../PRESENTAZIONE-CEO.md)). Dice in che ordine si costruisce, come si verifica ogni passo, quanto lavoro serve, cosa può andare storto e cosa resta da decidere.

Cifre, fasi, decisioni e date sono quelle della proposta per i CEO, Alessandro Serratt e Michele Sanna: [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026. Se un numero qui non torna con la proposta, vale la proposta. Il piano tecnico di dettaglio è in [ricerca/36 §7](../ricerca/36-architettura-v2.md).

## In breve

- Sette fasi, dalla 0 alla 6, in circa 53 settimane ([proposta §11 e §15](../PRESENTAZIONE-CEO.md)).
- Oggi si impegnano solo le fasi 0 e 1, cioè le prime 8 settimane. Le altre si finanziano una per volta, sui risultati ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Due verifiche decidono se si va avanti: alla settimana 8 i CEO decidono se finanziare la fase 2; alla settimana 21 si decide se portare nella memoria i dati dei clienti ([proposta §1 e §11](../PRESENTAZIONE-CEO.md)).
- Nelle fasi 0 e 1 il lavoro lo portano avanti Alberto, Mattia e Michele. Ad Alessandro si chiedono l'assessment iniziale (la descrizione dei processi che fa ogni settimana), le sue regole di lavoro, il punto del venerdì su cosa si è automatizzato e le approvazioni dal telefono ([proposta §1 e §10](../PRESENTAZIONE-CEO.md)).
- I giorni di sviluppo sono solo nella sezione 5.

## Le parole del piano

- **Motore**: il nostro programma che fa girare gli agenti. Lo costruiamo con l'Agent SDK di Claude, cioè Claude Code, l'agente di Anthropic che lavora su file e comandi, usato come libreria. Ogni lavoro gira in un processo suo, cioè in un programma separato, con il profilo dell'agente, i suoi strumenti e un tetto di spesa ([proposta §5.1](../PRESENTAZIONE-CEO.md)).
- **Cancello**: l'unico programma che può mandare una mail, scrivere al cliente, toccare il CRM (l'archivio di contatti e trattative) o telefonare. Le azioni verso l'esterno le fa solo dopo il sì di una persona, una volta sola, o con una regola "Sempre"; fa eccezione "Andrea", l'agente vocale, che richiama senza carta solo chi lo ha chiesto (decisione 10). Le scritture interne, come meeting e trattative nel CRM o to-do in Jira (lo strumento per to-do e progetti), le fa secondo regole scritte, a nome della persona responsabile. In ogni caso registra tutto ([proposta §5.1 e §5.5](../PRESENTAZIONE-CEO.md)).
- **Carta**: la richiesta di approvazione che arriva nel canale Approvazioni di Teams, anche sul telefono, con il testo esatto dell'azione, un codice che vale una volta e una scadenza. Se nel frattempo il testo cambia, la carta non vale più ([proposta §4.11 e §5.4](../PRESENTAZIONE-CEO.md)).
- **Regola "Sempre"**: quando la stessa approvazione si ripete uguale per venti volte senza modifiche, una persona può trasformarla in una regola stretta su quell'agente, quel tipo di azione e quella destinazione, che scade dopo 30 giorni. Mai per offerte, primi contatti, pagamenti, cancellazioni, né per destinatari nuovi ([proposta §5.4](../PRESENTAZIONE-CEO.md)).
- **LiteLLM**: la porta da cui passano le chiamate degli agenti a Claude; dà a ogni agente, squadra e persona il suo budget ([proposta §5.1](../PRESENTAZIONE-CEO.md)).
- **Server MCP**: una presa standard a cui un agente si collega per usare uno strumento, per esempio la memoria, Jira o SersanOutreach, la nostra piattaforma outbound, cioè per i contatti commerciali in uscita su LinkedIn ed email, che diventa il CRM degli agenti ([proposta §1, §7.1 e §7.3](../PRESENTAZIONE-CEO.md)).
- **Bacheca**: il posto dove gli agenti si passano i compiti. Un freno nel codice impedisce le catene infinite: al massimo otto messaggi per conversazione, catene di tre passaggi, un tetto di spesa per catena ([proposta §4.11 e §5.3](../PRESENTAZIONE-CEO.md)).
- **Colori dei dati**: verde è il pubblico o l'interno non personale; giallo sono contatti di lavoro, campi del CRM e riassunti; rosso sono audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone e finanza. Il rosso resta sul server, oppure va all'API di Anthropic (l'accesso a Claude dai nostri programmi) dopo aver oscurato in locale i dati non necessari ([proposta §5.6](../PRESENTAZIONE-CEO.md)).
- **Claude Team e skill**: Claude Team è la finestra di lavoro di ognuno, con chat, skill e progetti per squadra; una skill è una procedura scritta che Claude segue per un lavoro che si ripete. Ogni processo che si ripete diventa una skill, ogni skill che funziona diventa un agente ([proposta §4.11 e §4.12](../PRESENTAZIONE-CEO.md)).
- **Buzz**: la chat open source di Block fatta per persone e agenti, in prova sul nostro server ([proposta §4.11](../PRESENTAZIONE-CEO.md)).
- **Board di Michele**: il disegno dell'infrastruttura del server, con reti, servizi e una roadmap in sei fasi, da F0 a F5 ([board di Michele](../allegati/infra/SerSan%20Infra%20Board.md)).

## 1. Come leggere il piano

**Settimane e giorni.** Le settimane sono il calendario delle fasi; la stima dei giorni di sviluppo è nella sezione 5 ([proposta §11](../PRESENTAZIONE-CEO.md)).

**Due cantieri.** L'infrastruttura la porta avanti Michele, con il suo board; sopra, noi costruiamo il sistema di agenti. Ogni fase parte quando la precedente è verificata, come nel board ([proposta §11](../PRESENTAZIONE-CEO.md)).

| Fase del board | Cosa porta | In corso durante le nostre fasi |
|---|---|---|
| F0 Arrivi | arrivo e montaggio dell'hardware, prova della RAM, export completo da Azure, il cloud di Microsoft dove oggi gira SersanOutreach | 0 |
| F1 Fondamenta | OPNsense, il software del firewall, con le reti separate; Proxmox, il sistema che fa girare le macchine virtuali sul server; l'accesso da fuori solo con identità verificata; il backup | 0 e 1 |
| F2 Via da Azure | i servizi, SersanOutreach compreso, passano da Azure al server; le macchine Azure si spengono | 1 e 2 |
| F3 Sicurezza | strumenti di sicurezza, inventario dei servizi, log e avvisi; documentazione per le norme ISO e per Cyber Essentials, la certificazione di sicurezza che chiede, fra l'altro, le patch critiche (gli aggiornamenti di sicurezza) entro 14 giorni e il secondo fattore di accesso (MFA) sui servizi cloud | 2 |
| F4 AI e bandi | la GPU per i modelli locali; la pipeline, cioè la catena di lavorazione, che rende ricercabili i documenti; i bandi con Firecrawl, che trasforma le pagine web in testo pulito, e n8n, che fa partire i lavori a orario e collega le applicazioni; LiteLLM con i budget | 2, 3 e 4 |
| F5 Laboratorio e dopo | le macchine di prova del laboratorio (Experimental 1 e 2) e gli ampliamenti dell'hardware | 4, 5 e 6 |

Fonti: [board di Michele, roadmap](../allegati/infra/SerSan%20Infra%20Board.md); la colonna di destra viene da [proposta §11](../PRESENTAZIONE-CEO.md); Azure da [proposta §7.1](../PRESENTAZIONE-CEO.md); Cyber Essentials da [ricerca/25 §7](../ricerca/25-board-michele-e-delta.md); n8n da [proposta §5.3](../PRESENTAZIONE-CEO.md).

**I tempi del board non sono ancora fissati.** In quante settimane si chiudono F0-F4 lo chiede la [domanda 1 per Michele](../DOMANDE-PER-MICHELE.md). Intanto il piano non si ferma: il pilota parte sul banco di prova ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)).

**Il banco di prova.** Il pilota non aspetta il board e non lo riordina. Nelle settimane 5-8 gira su una macchina di prova nella rete del laboratorio, con una chiave API limitata e un tetto di spesa, e salva solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata ([proposta §11](../PRESENTAZIONE-CEO.md)). Prima che la rete del laboratorio esista, il lavoro gira sulle macchine di sviluppo con dati di prova ([ricerca/36 §7.1](../ricerca/36-architettura-v2.md)). Se Michele anticipa il posto per gli agenti sul server (LiteLLM, il database, i segreti, n8n e due macchine virtuali, prima di F4), il passaggio sul server si anticipa ([proposta §11](../PRESENTAZIONE-CEO.md); [domanda 2 per Michele](../DOMANDE-PER-MICHELE.md)).

**Prima il funnel.** Il funnel è il percorso che porta un contatto (lead) a diventare cliente; oggi SersanOutreach ha 11 lead, 1 risposta e 0 meeting ([proposta §1](../PRESENTAZIONE-CEO.md)). Se alla settimana 8 l'email non è ancora attiva e i founder, Alessandro e Michele, non pubblicano dai loro profili LinkedIn, si fanno comunque le fasi 2 e 3, utili anche al funnel, e la fase 5 aspetta. "Andrea", l'agente vocale che richiama le lead che lo chiedono, e la pipeline pesata, cioè la probabilità di chiusura calcolata sullo storico, hanno senso solo con lead vere ([proposta §2.2, §8.1 e §11](../PRESENTAZIONE-CEO.md)).

**Dopo la fase 6** resta una manutenzione continua: aggiornamenti dell'Agent SDK, del Cancello e dei servizi, agenti nuovi ([proposta §11](../PRESENTAZIONE-CEO.md)).

## 2. Le regole che valgono in ogni fase

Ogni pezzo si costruisce dentro queste regole.

- **Gli agenti propongono, il codice esegue.** Nessun agente ha in mano un bottone che invia, pubblica, paga o cancella: passa sempre dal Cancello. La macchina degli agenti non ha accesso a internet e parla solo con LiteLLM, con i server MCP e con il Cancello ([proposta §5.4 e §9.2](../PRESENTAZIONE-CEO.md)).
- **Prima di ogni azione il motore chiede al Cancello**; se il Cancello non risponde in tempo, l'azione è bloccata ([proposta §5.3](../PRESENTAZIONE-CEO.md)).
- **Le routine nascono spente.** Ogni automazione parte in prova a secco: per una o due settimane mostra cosa avrebbe fatto, senza farlo ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Il testo di terzi non è mai un'istruzione.** Mail, trascrizioni, pagine web e risposte dei potenziali clienti entrano da una corsia senza strumenti. È la difesa contro le iniezioni di prompt, cioè le istruzioni nascoste in un testo per far agire un agente ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Tetti che fermano davvero.** Ogni agente e ogni catena di lavoro ha un budget: all'80% arriva un avviso, al 100% si ferma ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Tutto registrato e revocabile.** Registro delle azioni a sola aggiunta, segreti oscurati prima di qualsiasi log, stop di emergenza dal telefono ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Nessun bot nei canali condivisi con i clienti**: lì scrive solo il Cancello, dopo una carta ([proposta §4.11](../PRESENTAZIONE-CEO.md)).
- **Versioni fissate.** L'Agent SDK cambia quasi ogni giorno: si tiene una versione fissata e la si aggiorna ogni due settimane, dopo i dieci scenari di prova che motore e Cancello devono passare a ogni aggiornamento, entro i 14 giorni ([proposta §5.3 e §13](../PRESENTAZIONE-CEO.md)).
- **Ogni servizio nuovo** entra nel perimetro Cyber Essentials con un responsabile delle patch e un posto nell'inventario; prima della fase F4 del board entrano solo i servizi del pilota ([proposta §6.2 e §13](../PRESENTAZIONE-CEO.md)).

## 3. Il piano a fasi

| Fase | Settimane | Board in corso | Agenti al lavoro alla fine |
|---|---|---|---|
| 0. Valore subito e prove | 1-4 | F0-F1 | nessuno: si lavora con le skill di Claude Team |
| 1. Pilota su banco di prova | 5-8 | F1-F2 | 3 |
| 2. Pilota sul server e squadre che si parlano | 9-21 | F2-F4 | 14 |
| 3. Memoria, call, vendite preparate e canali | 22-35 | F4 | 32 |
| 4. Organizzazione, newsletter e Buzz | 36-40 | F4-F5 | 42 |
| 5. Vendite e voce | 41-48 | F5 | 46 |
| 6. Le altre automazioni | 49-53 | F5 | 57 |

Fonti: [proposta §4.12 e §11](../PRESENTAZIONE-CEO.md). Gli agenti di ogni fase sono quelli delle tabelle di [proposta §4](../PRESENTAZIONE-CEO.md), dove ogni agente ha la sua fase.

### Fase 0 · Valore subito e prove (settimane 1-4)

**Cosa si fa**

- Claude Team per tutti, con le skill, i template SerSan per offerte, slide e recap (i riassunti dopo le call) e un progetto per squadra. I cinque posti sono gratuiti per il primo anno grazie al bundle startup di Anthropic, che dà anche i crediti API ([proposta §1 e §11](../PRESENTAZIONE-CEO.md)).
- Le persone. Nella settimana 1 l'assessment: ognuno descrive quali processi fa ogni settimana e con quali strumenti. Nelle settimane 1-2 ognuno scrive in BookStack, il wiki sul nostro server dove stanno regole, processi e catalogo, come vuole riassunti, prossimi passi, report e orari di non disturbo: gli agenti leggono queste regole prima di ogni lavoro. Formazione documentata per tutti e quattro, come chiede l'AI Act, il regolamento europeo sull'intelligenza artificiale (art. 4) ([proposta §5.5 e §10](../PRESENTAZIONE-CEO.md)).
- L'email: decisione con il legale e casella attiva. Il parere legale unico consegna entro la settimana 3 i punti del pilota (email B2B, cioè tra aziende, verso l'Italia; registrazione delle call; trasferimenti di dati verso gli USA) e prima della fase 2 tutto il resto ([proposta §9.4 e §11](../PRESENTAZIONE-CEO.md)).
- SersanOutreach in sicurezza prima di collegare gli agenti: la decisione sulle regole dell'email (indirizzo e link di cancellazione nel footer, il piè di pagina della mail, oppure deroga registrata con parere legale), l'identità firmata dei chiamanti, il secondo fattore per i 7 account staff, una copia dei dati fuori dai suoi cloud con una prova di ripristino riuscita, gli avvisi che arrivano davvero a una persona ([proposta §7.4](../PRESENTAZIONE-CEO.md)).
- Il registro dei trattamenti e la valutazione d'impatto sulla protezione dei dati. Entro la settimana 3, con il parere, si decide quali dati arrivano a Claude Team; fino ad allora verde e giallo, e il rosso solo oscurato ([proposta §5.6 e §13](../PRESENTAZIONE-CEO.md)).
- Quattro prove tecniche: il bot di Teams, l'identità di chi approva, il blocco delle azioni, LiteLLM ([proposta §11](../PRESENTAZIONE-CEO.md)).
- La prima parte del motore ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Il marketing riparte: con Claude Team e la sessione presidiata di Alberto, cioè con una persona davanti allo schermo, si propone il calendario fino a Natale e si programmano, dopo il sì, i 22 testi dei post già pronti. I numeri del lunedì li compila una skill di Claude Team ([proposta §8.2 e §8.4](../PRESENTAZIONE-CEO.md)).
- Le verifiche della prima settimana, senza chiedere nulla ai CEO: cosa include il bundle startup (crediti mensili e scadenza), quale piano di Microsoft 365 (M365) e quale piano Jira abbiamo, quanto del kit commerciale paghiamo già. Si chiede anche ad Anthropic la conservazione zero dei dati delle API, che è gratuita ([proposta §14](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: tutti e quattro in Claude Team ogni giorno. Calendario dei post pieno fino a Natale. Prime offerte e slide con il nostro stile. Email decisa e casella attiva. SersanOutreach sicuro su identità e MFA ([proposta §11](../PRESENTAZIONE-CEO.md)).

### Fase 1 · Pilota su banco di prova (settimane 5-8)

**Cosa si fa**

- Il motore sul banco di prova, con il collegamento al Cancello, i dieci scenari di prova e il registro degli agenti: per ognuno nome, squadra, responsabile umano, modello, cosa può toccare, tetto di spesa e costo del mese ([proposta §4.12 e §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §7.3](../ricerca/36-architettura-v2.md)).
- Il Cancello versione 1, pronto alla fine della fase; le parti successive arrivano con le fasi che le usano ([proposta §5.4](../PRESENTAZIONE-CEO.md)).
- L'invio da Outlook attraverso Microsoft Graph, l'interfaccia con cui i programmi leggono e scrivono posta, calendario e trascrizioni di M365, solo verso il dominio del cliente ([proposta, appendice A, voce B3](../PRESENTAZIONE-CEO.md)).
- Le carte in Teams con l'identità di chi approva. Se il bot di Teams dà problemi, prima una registrazione Azure Bot gratuita, senza macchine accese, e in ultima istanza la pagina del Cancello con gli avvisi in Teams ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)).
- Le trascrizioni delle call Teams, che Microsoft scrive già, lette dal banco di prova ([proposta §6.4 e §11](../PRESENTAZIONE-CEO.md)).
- L'oscuramento locale dei dati non necessari, costruito e misurato in questa fase ([proposta §5.6](../PRESENTAZIONE-CEO.md)).
- Tre agenti: il Post-call (riassunto e bozza della mail di follow-up, quella che segue la call), l'Analista chiamate (riassunto secondo le regole di ciascuno, nel registro di tutti i meeting) e il Report del mattino (alle 7:00, per ciascuno, il debrief: cosa è successo ieri, scadenze, task, pipeline, cosa aspettano gli agenti da noi) ([proposta §4.2 e §4.8](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: dopo una call Teams il riassunto arriva nel canale interno e la bozza della mail arriva come carta sul telefono; dopo il sì parte una volta sola. Debrief alle 7:00 per tutti. Poi la verifica della settimana 8 (sezione 4) ([proposta §11](../PRESENTAZIONE-CEO.md)).

### Fase 2 · Pilota sul server e squadre che si parlano (settimane 9-21)

**Cosa si fa**

- Il motore passa sul server, con n8n per gli orari e LiteLLM per i budget ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Il Cancello aggiunge la chiave FIDO2, una chiave di sicurezza fisica che serve, oltre al sì, per offerte, contratti, fatture e primi contatti, e le regole "Sempre" che scadono ([proposta §5.4 e §11](../PRESENTAZIONE-CEO.md)).
- Nove bot di squadra in Teams, ognuno con il nome dei suoi agenti ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md)).
- Jira, BookStack e la memoria aperti agli agenti; BookStack chiede un database MariaDB da aggiungere al board ([proposta §11 e appendice A, voce A2](../PRESENTAZIONE-CEO.md)).
- SersanOutreach collegato: i suoi due server MCP, uno di lettura con 19 strumenti e uno operatore con 14 operazioni, raggiungibili dal motore con un accesso per squadra. Gli agenti leggono liberamente e scrivono solo attraverso il Cancello; per i clienti già attivi si aggiunge l'operazione che crea una trattativa. Invii in blocco, lanci e cancellazioni non esistono: restano a una persona ([proposta §7.3 e appendice A, voce B2](../PRESENTAZIONE-CEO.md)).
- La bacheca con il freno e il canale "Agenti" in Teams, dove tutti vedono il lavoro che gli agenti si passano ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md)).
- La richiesta a Meta per WhatsApp ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Lo stop di emergenza ferma anche gli invii di SersanOutreach: il kill switch, cioè l'interruttore che blocca tutti gli invii, e la pausa delle campagne di Instantly, il servizio delle sequenze email ([proposta §4.1 e §4.8](../PRESENTAZIONE-CEO.md)).
- I servizi nuovi (le macchine di motore, Cancello e server MCP, e MariaDB) entrano sul server in questa fase, sul posto per gli agenti oppure dopo F3, e vanno nell'inventario, ciascuno con un responsabile delle patch ([ricerca/36 §4.5](../ricerca/36-architettura-v2.md)).
- 11 agenti nuovi: Dettatura (Chiamate); Capo di gabinetto, Banca dei token, Registro e audit, Guardiano (Direzione); Agente task (Progetti); Editoriale, Ricerca concorrenza, Analista metriche, Pubblicatore (Marketing); Copywriter (Studio contenuti). Il Post-call aggiunge CRM e to-do in Jira ([proposta §4](../PRESENTAZIONE-CEO.md)).
- Nel frattempo il board, nella fase F2, sposta SersanOutreach da Azure al server; la macchina Azure si spegne solo dopo una settimana di funzionamento stabile ([proposta §7.2](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: CRM e to-do in Jira dopo ogni call. Gli agenti del marketing si passano il lavoro nel canale "Agenti" con il freno in azione. Organigramma con 14 agenti e i loro costi. Banca dei token in LiteLLM, cioè i budget di spesa per agente e per catena di lavoro; quelli per persona arrivano nella fase 4. Poi la verifica della settimana 21 (sezione 4) ([proposta §4.8 e §11](../PRESENTAZIONE-CEO.md)).

### Fase 3 · Memoria, call, vendite preparate e canali (settimane 22-35)

**Prima di partire**: altri 192 GB di RAM, perché con memoria e call il margine arriva a circa zero ([proposta §6.3](../PRESENTAZIONE-CEO.md)). Da qui conviene anche la seconda GPU, perché trascriviamo in casa le call dei clienti e le riunioni dal vivo ([proposta §6.4](../PRESENTAZIONE-CEO.md)).

**Cosa si fa**

- La ricerca nella memoria con i permessi di ciascuno, anche da Claude Team: chi chiede vede solo ciò che può vedere. La memoria che collega i momenti (trascrizioni, mail, documenti) è Qdrant, un database che cerca i testi anche per significato; gli embedding, cioè i testi tradotti in numeri per poterli cercare così, si calcolano sulla nostra GPU ([proposta §5.3, §5.5 e §11](../PRESENTAZIONE-CEO.md)).
- Il bot nelle call dei clienti: Vexa, sul nostro server, entra nelle call di Teams di altri, Meet e Zoom, dichiarandolo, e la trascrizione si fa in casa. Per le riunioni dal vivo la registrazione dal telefono e un vivavoce da sala ([proposta §4.2, §11, §14 decisione 14 e appendice A, voce J5](../PRESENTAZIONE-CEO.md)).
- Il Cancello versione 2 ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Telegram per gli avvisi, WhatsApp e Slack soprattutto per i clienti: stessi agenti, stesso codice. WhatsApp solo con l'API ufficiale di Meta e un numero dedicato, sempre dal Cancello. Su questi canali passano solo dati verdi, e le approvazioni restano in Teams ([proposta §2.1 e §4.11](../PRESENTAZIONE-CEO.md)).
- 18 agenti nuovi: Agente email, Agente LinkedIn, Sentinella segnali, Operatore outbound (Outbound); Agente chiamate, Agente agenda (Chiamate); Agente brief, Agente proposte, Analista vinto/perso, Agente intake (Vendite); Agente slide (Studio contenuti); Raccoglitore, Pulitore, Bibliotecario, Archivista, Sistemista (Memoria); Smistatore posta (Direzione); Agente bandi e finanziamenti (Amministrazione) ([proposta §4](../PRESENTAZIONE-CEO.md)).
- Su LinkedIn ogni messaggio passa dall'approvazione di una persona: gli agenti non usano l'autopilot dei messaggi, che scrive e approva da solo inviti e messaggi, né l'automazione del browser lato server ([proposta §7.1 e §7.4](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: brief, cioè la scheda che prepara l'incontro, pronto la sera prima di ogni incontro. Offerta in bozza entro un'ora. "Cosa ci siamo detti con X?" da Claude Team. Bandi ogni mattina. Posta smistata. Gli stessi agenti su Telegram, Slack e WhatsApp. 32 agenti al lavoro ([proposta §11](../PRESENTAZIONE-CEO.md)).

### Fase 4 · Organizzazione, newsletter e Buzz (settimane 36-40)

**Cosa si fa**

- Newsletter e programmazione dei post sul nostro server: listmonk per la newsletter, con l'invio attraverso un servizio di posta esterno, e Postiz per i post, al posto di Metricool, il servizio a pagamento che si usa finché Postiz non è pronto ([proposta §8.2, §11 e §14, decisioni 9 e 15](../PRESENTAZIONE-CEO.md)). Nessuno dei due è esposto su internet: si raggiungono solo da NetBird, la rete privata con cui si entra da fuori con identità verificata ([ricerca/36 §4.5](../ricerca/36-architettura-v2.md); [proposta §6.1](../PRESENTAZIONE-CEO.md)).
- La banca dei token per persona ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Le skill proposte dagli agenti: le scrivono in una cartella "proposte", un revisore le controlla ogni settimana e una persona le approva con una pull request, cioè una richiesta di modifica da rivedere e accettare ([proposta §11 e appendice A, voce A6](../PRESENTAZIONE-CEO.md)).
- Buzz sul banco di prova del laboratorio, collegato alla stessa bacheca di Teams ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md)).
- 10 agenti nuovi: Agente newsletter, Community manager (Marketing); Agente video, Agente grafiche (Studio contenuti); Project manager, Report cliente, Onboarding cliente, Sviluppatori (Progetti); Mappatore processi, Intervistatore (Direzione) ([proposta §4](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: prima newsletter dopo il sì. Risposte sulla pagina aziendale in carta. Mappa dei processi. Buzz come stanza degli agenti sul banco di prova: diventa quella ufficiale quando non perde più risposte e ha approvazioni funzionanti. 42 agenti ([proposta §11](../PRESENTAZIONE-CEO.md)).

### Fase 5 · Vendite e voce (settimane 41-48)

Parte solo con il parere legale e con lead reali ([proposta §11](../PRESENTAZIONE-CEO.md)).

**Prima di partire**: la seconda GPU, al più tardi all'inizio della fase, prima di spostare Andrea sulla GPU ([proposta §6.4](../PRESENTAZIONE-CEO.md)); la linea internet di riserva, consigliata prima della fase 5 ([proposta §14, decisione 13](../PRESENTAZIONE-CEO.md)); il consenso alla richiamata in ogni modulo: sito, campagne, eventi ([proposta, appendice A, voce G5](../PRESENTAZIONE-CEO.md)).

**Cosa si fa**

- "Andrea" con il centralino Asterisk e una linea telefonica italiana, prima sulla CPU e poi sulla seconda GPU. Pipecat regge la conversazione al telefono; Claude Haiku, il modello più leggero di Claude, ragiona; ascolto e voce girano in casa. La richiesta di richiamata arriva dal modulo del sito attraverso n8n ([proposta §5.1, §11 e appendice A, voce G5](../PRESENTAZIONE-CEO.md)). Andrea si dichiara AI dalla prima frase e richiama da solo soltanto chi lo ha chiesto nel modulo ([proposta §1 e §9.1](../PRESENTAZIONE-CEO.md)).
- Andrea parte con una voce sintetica. La versione con la voce clonata di un collega arriva dopo, sempre nella fase 5, solo con il suo contratto separato e revocabile e il via del parere legale ([proposta §14 decisione 10 e appendice A, lacune dichiarate](../PRESENTAZIONE-CEO.md)).
- La pipeline pesata e il portale clienti costruito sopra SersanOutreach. Finché le chiusure non sono 30-50, la pipeline usa pesi dichiarati da Alessandro ([proposta §4.3 e appendice A, voce D1 e lacune dichiarate](../PRESENTAZIONE-CEO.md)).
- 4 agenti nuovi: "Andrea", Coach vendite, Pipeline (Vendite) e Agente clienti simili (Outbound) ([proposta §4](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: una lead di prova viene richiamata entro 90 secondi e l'appuntamento è nel CRM. Chiamate in entrata con l'esito nel canale vendite. Coaching, cioè i consigli dopo ogni call di vendita, visibile solo a chi ha fatto la call. 46 agenti ([proposta §4.3 e §11](../PRESENTAZIONE-CEO.md)).

### Fase 6 · Le altre automazioni (settimane 49-53)

**Cosa si fa**

- Firma elettronica e fatturazione sul nostro server: DocuSeal per la firma; per le fatture lo strumento che usiamo già, se fa al caso, altrimenti uno sul nostro server ([proposta §11, §14 decisione 22 e appendice A, voci L1 e L2](../PRESENTAZIONE-CEO.md)).
- L'assistente personale per chi lo vuole: i dati di salute restano nell'account privato di chi lo sceglie e non entrano mai nella memoria aziendale ([proposta §4.8](../PRESENTAZIONE-CEO.md)).
- La prova di Paperclip, un piano di controllo open source fatto apposta per "aziende di agenti" ([proposta §4.12 e §11](../PRESENTAZIONE-CEO.md)).
- 11 agenti nuovi: Agente contratti (Vendite); Agente sito e SEO, Agente eventi e webinar (Marketing); Assistenza clienti, Agente rinnovi, Agente casi studio (Progetti); Allenatore AI, Assistente personale (Direzione); Agente fatture e incassi, Agente acquisti e abbonamenti, Controllo di gestione (Amministrazione) ([proposta §4](../PRESENTAZIONE-CEO.md)).

**Cosa si vede alla fine**: dal contratto all'incasso senza lavoro a mano. Ogni progetto chiuso diventa un caso studio. Tutti i 57 agenti nel registro ([proposta §11](../PRESENTAZIONE-CEO.md)).

## 4. Le verifiche delle settimane 8 e 21

### 4.1 Settimana 8: si finanzia la fase 2?

Alla settimana 8 i CEO decidono se finanziare la fase 2. Se ci si ferma, restano Claude Team usato bene da tutti, SersanOutreach sistemato, la decisione sull'email e il calendario dei post ([proposta §1](../PRESENTAZIONE-CEO.md)). La verifica ha due gruppi di criteri ([proposta §11](../PRESENTAZIONE-CEO.md)); i dettagli su come si misurano vengono da [ricerca/36 §7.4](../ricerca/36-architettura-v2.md).

**Criteri tecnici**, sul banco di prova:

1. Tre agenti lavorano una settimana senza scambiarsi le sessioni.
2. Nessun effetto esce senza una carta del Cancello, anche nei dieci scenari di prova, tra cui il Cancello che non risponde in tempo, la carta scaduta e il testo cambiato dopo la carta.
3. Una carta lasciata ferma la notte riprende il lavoro giusto al mattino.
4. L'approvazione arriva dal telefono con l'identità giusta, dalla carta in Teams o dalla pagina del Cancello.
5. La spesa resta nel tetto, e la stima di spesa dell'Agent SDK si discosta meno del 10% da quella della Console, il pannello di Anthropic dove si vede la spesa delle API.
6. Un aggiornamento dell'Agent SDK passa i dieci scenari ed è in uso entro 14 giorni dall'uscita.
7. Sul banco di prova non resta salvato nessun dato rosso.

**Criteri commerciali**:

1. Decisione sull'email presa e casella attiva.
2. Follow-up di tutte le call del periodo inviato entro 24 ore, dagli agenti sul banco di prova oppure con la skill del recap in Claude Team.
3. Carte decise entro 24 ore.
4. Almeno 8 post dei founder pubblicati nelle settimane 4-8.
5. Numeri del lunedì compilati ogni settimana.
6. Tutti e quattro usano Claude Team ogni giorno, come dicono le statistiche d'uso.
7. SersanOutreach sicuro su identità e MFA.

Da subito si misura anche quanto tempo passa oggi tra una lead e la prima risposta, per avere un punto di partenza ([proposta §11](../PRESENTAZIONE-CEO.md)).

### 4.2 Settimana 21: entrano i dati dei clienti?

Prima di passare alla memoria con i dati dei clienti servono ([proposta §11](../PRESENTAZIONE-CEO.md)):

1. gli stessi criteri tecnici della settimana 8, sul server, con i budget di LiteLLM al posto del tetto della Console ([ricerca/36 §7.5](../ricerca/36-architettura-v2.md));
2. la revisione esterna di Cancello, motore e bot fatta, con i rilievi gravi chiusi;
3. nessuna risposta del lavoro di una persona finita in un canale aperto a tutti;
4. tutti i servizi nuovi in inventario, con le patch entro 14 giorni;
5. il backup 3-2-1 in funzione, cioè tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio, con una prova di ripristino riuscita ([proposta §6.1](../PRESENTAZIONE-CEO.md));
6. la RAM misurata e la decisione d'acquisto presa.

Fino a questa verifica nessun dato dei clienti resta sul server ([proposta §13](../PRESENTAZIONE-CEO.md)).

### 4.3 Se una verifica non passa

- **Fallisce un criterio tecnico**: due settimane per correggere. Se il problema è di struttura, si prova Hermes Agent sullo stesso banco di prova, con gli stessi scenari, e si decide sui numeri ([proposta §11](../PRESENTAZIONE-CEO.md)). Hermes è un orchestratore open source, cioè un programma già pronto che coordina gli agenti, e lo abbiamo confrontato con il motore prima di scegliere. Cancello, memoria, server MCP, bot e skill restano uguali; Hermes diventa il nostro orchestratore solo se chiude i suoi problemi di sicurezza ([proposta §5.7](../PRESENTAZIONE-CEO.md)). I giorni di questa uscita sono nella sezione 5.
- **Falliscono i criteri commerciali**: vale "prima il funnel" (sezione 1): le fasi 2 e 3 vanno avanti, la fase 5 aspetta ([proposta §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §7.4](../ricerca/36-architettura-v2.md)).

## 5. La stima dei giorni di sviluppo

È l'unica stima dei giorni di lavoro di questo file. Viene da [proposta §15](../PRESENTAZIONE-CEO.md).

**Come si legge**

- I giorni sommano il lavoro di tutte le persone che sviluppano, in parallelo: per questo in una fase possono essere più dei giorni di calendario ([proposta §15](../PRESENTAZIONE-CEO.md)).
- Il valore più basso è la stima di base; il più alto comprende una riserva di circa un terzo ([proposta §15](../PRESENTAZIONE-CEO.md)).
- L'infrastruttura del board di Michele non è contata: la porta avanti lui ([proposta §15](../PRESENTAZIONE-CEO.md)). Non sono contate nemmeno la migrazione di SersanOutreach e le parti della fase F4 che il board fa già, come la base della ricerca nella memoria e la pipeline dei documenti: contiamo solo le nostre estensioni ([ricerca/36 §7.6](../ricerca/36-architettura-v2.md)).
- Sono contati l'installazione e l'esercizio dei servizi nuovi ([proposta §13](../PRESENTAZIONE-CEO.md)) e il contenuto di ogni agente: istruzioni, skill, schemi e prove ([ricerca/34-proposta-1 §4.3](../ricerca/34-proposta-1-agent-sdk.md)).
- "Esercizio e patch" sono i giorni per tenere in funzione e aggiornati i servizi nuovi (aggiornamenti, patch, scansioni), contati a parte: circa mezza giornata a settimana nelle fasi 2-4 e circa una nelle fasi 5-6, perché i servizi da seguire crescono ([ricerca/36 §4.5 e §7.6](../ricerca/36-architettura-v2.md)).

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

Fonte: [proposta §15](../PRESENTAZIONE-CEO.md).

**Note**

- **Oggi si chiedono le fasi 0 e 1**: 40,5-54 giorni di sviluppo in 8 settimane, come nella prima versione ([proposta §15](../PRESENTAZIONE-CEO.md)).
- **Calendario e capacità.** Le settimane sono calcolate sui giorni con la riserva più l'esercizio, con una capacità di circa 6,5 giorni di sviluppo a settimana per tutto il gruppo fino alla fase 3 e circa 7,5 dalla fase 4, da confermare. Se si consuma tutta la riserva, le fasi 0 e 1 finiscono a metà della settimana 9: la verifica resta alla settimana 8 e misura ciò che c'è ([ricerca/36 §7.1 e §7.2](../ricerca/36-architettura-v2.md)).
- **Con più capacità di sviluppo** dalla fase 2 il calendario scende da circa 53 a circa 42 settimane ([proposta §15](../PRESENTAZIONE-CEO.md)); il conto usa circa 9 giorni di sviluppo a settimana. Se Michele anticipa il posto per gli agenti, il passaggio sul server arriva qualche settimana prima, ma i giorni restano gli stessi ([ricerca/36 §7.7](../ricerca/36-architettura-v2.md)).
- **Perché il totale cresce rispetto alla prima versione** (110-147 giorni per le fasi 0-5): ora tutto è sul nostro server e nessuna funzione è tolta. Chat, bot nelle call, voce di Andrea, newsletter, programmazione dei post, firma elettronica e fatturazione li costruiamo e li gestiamo in casa invece di pagarli in abbonamento, e i giorni per le patch e l'esercizio sono contati ([proposta §15](../PRESENTAZIONE-CEO.md)).
- **La prova di Buzz** occupa circa 6 giorni nella fase 4 ([proposta §15](../PRESENTAZIONE-CEO.md)).
- **Se il motore non reggesse** alle verifiche, una prova di Hermes sullo stesso banco costa 6-8 giorni; usarlo al posto del motore costa 26-33 giorni con la riserva, mentre Cancello, memoria, bot e skill restano ([proposta §15](../PRESENTAZIONE-CEO.md)).
- **Dopo la fase 6** l'esercizio resta intorno a un giorno a settimana: aggiornamenti dell'Agent SDK, del Cancello e dei servizi, agenti nuovi ([proposta §15](../PRESENTAZIONE-CEO.md)).

## 6. I rischi principali e come li gestiamo

Sono i rischi della [proposta §13](../PRESENTAZIONE-CEO.md), divisi per tema.

### 6.1 Il codice che scriviamo

| Rischio | Come lo gestiamo |
|---|---|
| **Cancello, motore e bot sono codice scritto su misura** e nessuno lo ha ancora rivisto | Dieci scenari di prova a ogni aggiornamento; revisione esterna entro la settimana 21; Mattia sul codice dal primo giorno |
| **L'Agent SDK cambia quasi ogni giorno** | Versione fissata; aggiornamento ogni due settimane, dopo i dieci scenari, entro i 14 giorni |
| **Il motore non regge** | Verifiche alle settimane 8 e 21; Hermes come uscita già stimata, provato sullo stesso banco di prova |
| **LiteLLM custodisce tutte le chiavi**, e a marzo 2026 ne sono circolate versioni compromesse | Versione fissata e controllata; esce solo verso Anthropic; pannello raggiungibile solo dalla rete di gestione; chiave principale tra i segreti, con rotazione |
| **Il bot di Teams senza Azure** può dare errori di registrazione | Prova nella fase 0; registrazione Azure Bot gratuita, senza macchine accese; in ultima istanza la pagina del Cancello, con gli avvisi in Teams |
| **Iniezioni di prompt** da mail, trascrizioni e messaggi | Chi legge testo di terzi non ha strumenti che agiscono; nessuno strumento invia senza il Cancello |

### 6.2 Il server e la rete

| Rischio | Come lo gestiamo |
|---|---|
| **Il tempo di chi amministra il server**: il sistema aggiunge 11-13 servizi e 3 reti nuove al perimetro Cyber Essentials, con le patch entro 14 giorni | Prima della fase F4 entrano solo i servizi del pilota; ogni servizio ha un responsabile delle patch e un posto nell'inventario; installazione ed esercizio dei servizi nuovi sono nei giorni della sezione 5, mentre l'infrastruttura del board la porta avanti Michele e non è contata |
| **RAM finita** con tutte le funzioni | Misura con un tetto di sessioni; altri 192 GB prima della fase 3; leve per rimandare l'acquisto |
| **Una sola GPU fino all'arrivo della seconda**, prestata ogni tanto alla postazione di prova del laboratorio (Experimental-1) | I lavori della GPU aspettano in coda finché torna libera; seconda GPU da 16 GB dalla fase 3, al più tardi dalla fase 5; embedding e lavori a lotti, cioè fatti in blocco e non dal vivo, sulla CPU quando serve |
| **Una sola linea internet**: se cade la fibra, gli agenti si fermano, perché ragionano con Claude via internet, e Andrea non risponde | Nulla si perde: lavori e carte aspettano e ripartono quando la linea torna. Linea di riserva 4G/5G prima della fase 5 (decisione 13); l'accesso da fuori passa dalla macchina Oracle, la piccola macchina in cloud a Milano, e funziona anche sulla linea di riserva |
| **Mancanza di corrente**, con le batterie dell'UPS (il gruppo di continuità del rack) usate e senza garanzia | Dopo 3 minuti l'UPS spegne il server in modo pulito e tiene accesa la rete; al ritorno della corrente la rete riparte da sola, mentre il server va riacceso a distanza, a meno che Michele non lo imposti per ripartire da solo: fino ad allora gli agenti, e dalla fase 5 Andrea, restano fermi. Test di autonomia e di riaccensione all'arrivo dell'UPS, e batterie nuove se servono |
| **Backup non ancora completo**: la copia in sede va montata, quella a casa di Michele arriva a marzo 2027 | Nessun dato dei clienti resta sul server prima della verifica della settimana 21, che chiede il 3-2-1 con una prova di ripristino |
| **Il firewall Sophos è un modello fuori supporto**: Sophos non lo aggiorna più, e BIOS (il programma di base della macchina) e processore non ricevono più correzioni | Il software che ci gira, Proxmox e OPNsense, è aggiornato. Per Cyber Essentials si chiede prima per iscritto all'ente di certificazione se accetta questa configurazione; se non la accetta, OPNsense passa su un piccolo computer ancora supportato dal produttore (spesa da preventivare) |
| **Fine del supporto HPE**, il produttore del server, per lo chassis, cioè il telaio del server: ottobre 2029 secondo le fonti HPE consultate da Michele, da confermare con il numero di serie; le stime pubbliche partono da marzo 2028 | Macchine virtuali con backup: si spostano su un server nuovo senza rifare nulla; Michele prevede il secondo server a dicembre |
| **Tempi del board** non ancora fissati | Banco di prova nel laboratorio; il posto per gli agenti sul server come richiesta a Michele |

### 6.3 Dati, regole e canali

| Rischio | Come lo gestiamo |
|---|---|
| **Dati personali verso Claude Team**, che non ha un registro di audit | Decisione nel parere e nella valutazione d'impatto entro la settimana 3; il rosso arriva a Claude Team solo oscurato |
| **Registrazioni, "Andrea", coaching** e norme sul lavoro | Parere legale: i punti del pilota entro la settimana 3, il resto prima della fase 2; "Andrea" si dichiara sempre AI; coaching privato |
| **"Andrea" e la regola del piano marketing** che vieta voci sintetiche nelle call | Un'eccezione decisa dai CEO (decisione 10): solo richiamate chieste dalla lead, voce dichiarata, il brief resta letto da un founder |
| **Piattaforme di call che bloccano i bot** non registrati | Per le nostre call la trascrizione nativa di Teams; registrazione sul PC come riserva |
| **La voce italiana di Andrea** non abbastanza buona | Prova d'ascolto prima; voci migliori sulla seconda GPU; in ultima istanza una voce in cloud, come eccezione decisa dai CEO |
| **WhatsApp**: le soluzioni non ufficiali portano al blocco del numero | Solo l'API ufficiale di Meta, con un numero aziendale dedicato |
| **Buzz è giovane** | Resta sul banco di prova finché non perde più risposte e non ha approvazioni funzionanti; intanto la stanza degli agenti è il canale "Agenti" in Teams |

### 6.4 Il progetto

| Rischio | Come lo gestiamo |
|---|---|
| **Il funnel è vuoto**: 11 lead, 0 meeting, campagna ferma dal 9 settembre | Decisione sull'email e casella attiva nella fase 0; criteri commerciali alla settimana 8; "Andrea" solo con lead vere |
| **Calendario lungo**, circa un anno | Valore dalla prima settimana; fasi finanziate una per volta; con più capacità di sviluppo il calendario si accorcia (sezione 5) |
| **Troppi agenti per quattro persone** | Ogni agente ha un responsabile, un tetto e una riga nel registro; un agente che non serve si spegne dal registro |

**Le uscite.** Ogni pezzo sta dietro un'interfaccia: il motore parla con gli strumenti solo attraverso i server MCP, con i modelli solo attraverso LiteLLM, con l'esterno solo attraverso il Cancello. Se un pezzo non regge si cambia quel pezzo, e il resto rimane. La tabella delle uscite, pezzo per pezzo, è in [ricerca/36 §12](../ricerca/36-architettura-v2.md).

## 7. Le domande aperte

Le scelte tecniche sull'infrastruttura restano di Michele, e il documento per i CEO non le contiene. Le domande per lui sono in [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md), aggiornate l'8 novembre 2026 con le sue risposte sull'hardware e con la board del rack, cioè il piano di montaggio di server, firewall e UPS ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)). Sono 30, in sette gruppi:

| Gruppo | Domande | Di cosa parlano |
|---|---|---|
| Tempi e posto per gli agenti | 1-3 | settimane delle fasi F0-F4; posto per gli agenti prima di F4 o pilota su una macchina di prova del laboratorio; la rete in cui mettere il motore |
| Rete ed esposizione | 4-8 | la macchina Oracle a Milano e i limiti del piano gratuito; il bot di Teams; il punto d'ingresso pubblico della ricerca nella memoria per Claude Team; una regola del firewall per quella ricerca; il bypass delle porte del Sophos, che a firewall spento collegherebbe la fibra direttamente al server |
| Servizi nuovi e Cyber Essentials | 9-13 | i servizi nuovi e chi li aggiorna; i servizi esterni da ammettere; il sostituto di MinIO, l'archivio dei file previsto nel board e non più mantenuto; il firewall fuori supporto; versioni e abbonamenti di Proxmox |
| Backup | 14-16 | le regole del 3-2-1, lo spazio dei dischi, la designazione scritta per la copia fuori sede |
| Hardware | 17-24 | il riser, cioè il supporto per le schede aggiuntive, e la seconda GPU; il software sulla nuova GPU; l'uso della GPU da parte del laboratorio; UPS, autonomia e riaccensione; fine del supporto HPE; la linea di riserva |
| Dati e servizi del board | 25-27 | cos'è Sirius, la sorgente da cui parte la pipeline dei documenti nel board, e cosa fanno altri servizi già previsti; il database di SersanOutreach su Supabase, il database in cloud che il board tiene per il prodotto; i piani M365 e Jira e chi è amministratore globale di M365 |
| Per tutti e quattro | 28-30 | TypeScript come linguaggio del motore; chi fattura e con quale sistema; quali chat usano i clienti |

Fonti: [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md); Sirius da [ricerca/25 §7](../ricerca/25-board-michele-e-delta.md); Supabase da [proposta §7.2](../PRESENTAZIONE-CEO.md). In fondo al file ci sono anche note tecniche su RAM, GPU, firewall, fibra, UPS e Cyber Essentials, senza risposta richiesta.

**Le prime da chiudere**, perché servono prima del pilota delle settimane 5-8:

- 1 e 2: quando sono pronte le fasi del board e dove gira il pilota, sul posto per gli agenti o su una macchina di prova del laboratorio ([proposta §11](../PRESENTAZIONE-CEO.md));
- 5: il bot di Teams, che è una delle quattro prove della fase 0 ([proposta §11 e §13](../PRESENTAZIONE-CEO.md));
- 27: piani M365 e Jira e chi dà i consensi per Graph, con cui il pilota legge le trascrizioni e manda le mail ([proposta §11 e appendice A, voce B3](../PRESENTAZIONE-CEO.md));
- 28: il linguaggio del motore, perché la sua prima parte si scrive nella fase 0 ([proposta §11](../PRESENTAZIONE-CEO.md)).

**Le domande per Anthropic** ([ricerca/36 §13](../ricerca/36-architettura-v2.md)):

- se i crediti in comune del piano Team valgono anche per la chiave API dietro LiteLLM e se si sommano ai crediti del bundle;
- se il piano Team ha davvero i tetti di spesa per persona;
- la conservazione zero dei dati delle API, che si chiede subito ([proposta §14](../PRESENTAZIONE-CEO.md));
- se un giorno il sistema si offre ai clienti, come si applicano all'Agent SDK i termini sulla chiave di ogni utente finale.

## 8. Le spese e le decisioni chieste ai CEO

Il dettaglio è nella [proposta §12 e §14](../PRESENTAZIONE-CEO.md). Ai CEO si chiedono solo decisioni di budget, abbonamenti, acquisti e integrazioni; le scelte tecniche le abbiamo studiate noi, quelle sull'infrastruttura restano di Michele ([proposta §14](../PRESENTAZIONE-CEO.md)). Prezzi IVA esclusa, dove non è scritto altro ([proposta §12.1](../PRESENTAZIONE-CEO.md)).

### 8.1 Cosa si chiede oggi

1. Il via alle fasi 0 e 1, con la verifica alla settimana 8 su criteri tecnici e commerciali.
2. Nessun abbonamento nuovo oltre a quelli del board di Michele: Proxmox (20 € al mese), l'IP fisso (fino a 10 €), la macchina Oracle per l'accesso da fuori (0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento) e, se Michele li sceglie, gli abbonamenti Proxmox per firewall e backup (fino a circa 103 € al mese, decisione 17).
3. Il budget una tantum delle prime otto settimane: il parere legale unico (tetto 2.500 €, con due preventivi), il credito API se serve (circa 223 €), le spese del board che conviene fare subito (backup in sede, chiavi FIDO2, accessori). In tutto circa 2.900-3.890 €, più circa 140-550 € per le batterie nuove dell'UPS se il test di autonomia all'arrivo va male.

Fonte: [proposta §1](../PRESENTAZIONE-CEO.md).

### 8.2 Quanto si spende in più al mese, fase per fase

| Periodo | € al mese in più | Cosa comprende |
|---|---|---|
| Fasi 0-1 e inizio della fase 2, finché Azure resta accesa | ≈ 135 (circa 141 se servisse un server a pagamento per l'accesso) | Proxmox (20), IP fisso (fino a 10), corrente del rack (≈ 105), la macchina Oracle per l'accesso da fuori (0 € sul piano gratuito di Oracle; 6,49 € se servisse un server a pagamento) |
| Fase 2 (settimane 9-21), con Azure spenta | da ≈ -15 a ≈ +20 | Azure spenta fa risparmiare circa 150 €; Jira Standard, se serve |
| Fasi 3-4 (settimane 22-40) | da ≈ -1 a ≈ +70 | WhatsApp con numero dedicato, Slack, invio della newsletter, corrente della RAM in più |
| Fasi 5-6 (dalla settimana 41) | da ≈ 46 a ≈ 168 | Si aggiunge la linea telefonica italiana di "Andrea" (44-90 €) |

Fonte: [proposta §1 e §12.1](../PRESENTAZIONE-CEO.md).

Le API di Claude per gli agenti (stima 90-250 € al mese) dovrebbero stare dentro i crediti del bundle startup; se non bastano si pagano, con un tetto a 250 €. Claude Team è gratuito per il primo anno; alla scadenza si decide quanti posti tenere (fino a 447 € al mese) ([proposta §1](../PRESENTAZIONE-CEO.md)). Il listino a regime, nella fase 6, è di circa 479-583 € al mese ([proposta §12.1](../PRESENTAZIONE-CEO.md)). Il costo vero resta il tempo di sviluppo della sezione 5 ([proposta §1](../PRESENTAZIONE-CEO.md)).

### 8.3 Le decisioni e quando servono allo sviluppo

| # | Decisione | Quando serve | Costo |
|---|---|---|---|
| 1 | Avviare le fasi 0 e 1, con la verifica alla settimana 8 | oggi | le prime 8 settimane (giorni nella sezione 5); nessun abbonamento nuovo oltre a quelli del board |
| 2 | Parere legale unico (email, registrazioni, dati verso Claude Team, "Andrea", coaching, firma elettronica, dati negli USA, backup a casa di Michele) | subito: i punti del pilota entro la settimana 3, il resto prima della fase 2 | tetto 2.500 €, con due preventivi |
| 3 | Tetto mensile delle API se i crediti non bastano, e credito prepagato | dalla fase 0 | tetto 250 € al mese (stima 196 €); credito 0-223 € |
| 4 | Spese del board per backup, corrente e sicurezza: backup in sede; batterie nuove dell'UPS solo se il test all'arrivo va male; nodo per la copia fuori sede, che fa anche da firewall della rete dove sta; più avanti un Proxmox Backup Server (il server dei backup) più grande fuori sede; chiavi FIDO2; accessori | backup in sede, chiavi e accessori subito; batterie all'arrivo dell'UPS; nodo fuori sede entro marzo 2027; server dei backup più grande quando servirà più spazio | circa 165-500 €; circa 140-550 €; circa 240-250 €; circa 690-930 €; 232-464 €; fino a 200 € |
| 5 | Revisione esterna di sicurezza di Cancello, motore e bot, prima che i dati dei clienti restino sul server | entro la settimana 21 | indicativo 3.560-5.940 € (£3.000-5.000), con due preventivi |
| 6 | Jira Standard per 4 persone, se oggi siamo sul piano gratuito | dalla fase 2 | 28 € al mese |
| 7 | Macchina esterna per l'accesso da fuori (NetBird; Pangolin, che pubblica verso internet solo i punti d'ingresso necessari, come il bot di Teams e le pagine di firma; monitoraggio): Michele ha scelto Oracle Cloud a Milano | dalle fasi 0-1 | 0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento |
| 8 | Canali in più: Telegram, Slack, WhatsApp con numero dedicato | dalla fase 3 | Telegram 0 €; Slack 0 o 27 € al mese; WhatsApp circa 7-12 € al mese |
| 9 | Invio della newsletter con un servizio di posta esterno | dalla fase 4 | meno di 1 € al mese |
| 10 | Voce di "Andrea": eccezione alla regola delle voci sintetiche nelle call, con una linea telefonica italiana | dalla fase 5, solo per chi chiede di essere richiamato, con voce dichiarata, parere e lead vere | 44-90 € al mese; attivazione 7-14 € |
| 11 | RAM: altri 192 GB, 12 moduli uguali a quelli montati | prima della fase 3, o quando il margine scende sotto i 5 GB | circa 690-830 € |
| 12 | Seconda GPU RTX PRO 2000 Blackwell da 16 GB, con il riser secondario e la staffa se mancano | appena torna sotto i 1.000 € IVA inclusa, dalla fase 3; comunque entro l'inizio della fase 5 | circa 880-1.220 € |
| 13 | Linea internet di riserva: 4G/5G con una SIM dati aziendale; Starlink, internet via satellite, solo se in ufficio il segnale mobile è scarso | prima della fase 5 | 4G/5G: 77-200 € una tantum e 10-11 € al mese; Starlink: 349 € e 31 € al mese |
| 14 | Vivavoce da sala per le riunioni dal vivo | fase 3 | 100-250 € |
| 15 | Strumenti commerciali fuori dal board: Apollo (ricerca di contatti) e Higgsfield (video e immagini per i post) restano; Metricool finché Postiz non è pronto; Apify (segnali di assunzione) sostituito da Firecrawl; moda.app (slide) sostituito da Claude Team; Perplexity (arricchimento in SersanOutreach) da decidere con il prezzo; After Effects (grafica animata) resta com'è oggi, senza costi in più | Metricool fino alla fase 4 | fino a 188 € al mese; con il consiglio circa 146 € fino alla fase 4, poi circa 86 € |
| 16 | Posti Claude Team alla fine del bundle | alla scadenza del bundle | 447 € al mese con 5 premium; 357 con 4; 214 con 2 premium e 2 standard |
| 17 | Abbonamenti del board: Proxmox sul server; Proxmox sul firewall e sui due server dei backup, se Michele li sceglie; IP fisso | dalle fasi 0-1 | Proxmox sul server 20 € al mese; firewall circa 10 € al mese; 46,67 € al mese per ogni Proxmox Backup Server, circa 93 € per tutti e due; IP fisso fino a 10 € al mese |
| 18 | Teams nel piano M365, se oggi manca | subito, se manca: il bot di Teams è una delle prove della fase 0 | 6-14 € al mese |
| 19 | Premio mensile per chi costruisce con l'AI | fase 4 | 50-100 € al mese |
| 20 | Assistente personale: account Claude personale per chi lo vuole | fase 6 | 15-18 € al mese a persona |
| 21 | Firma elettronica qualificata, solo se il parere la chiede per certi contratti | dopo il parere, per la fase 6 | a preventivo |
| 22 | Strumento di fatturazione: quello che usiamo già, se fa al caso; altrimenti uno sul nostro server | fase 6 | 0 € o il canone dello strumento scelto |
| 23 | Un mese di prova di Grok Bot, uno degli agenti in abbonamento valutati nel primo giro, su soli dati pubblici | facoltativa | circa 54 € una volta |

Fonti: decisioni e costi da [proposta §14](../PRESENTAZIONE-CEO.md); i momenti da [proposta §1, §11, §12.2 e appendice A](../PRESENTAZIONE-CEO.md); Pangolin da [proposta §5.2](../PRESENTAZIONE-CEO.md); a cosa servono gli strumenti commerciali da [ricerca/25 §7](../ricerca/25-board-michele-e-delta.md); Grok Bot da [proposta, appendice B](../PRESENTAZIONE-CEO.md).

## 9. Rigenerare DOCX e PDF della proposta

La fonte è [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md); `PRESENTAZIONE-CEO.docx` e `PRESENTAZIONE-CEO.pdf` si generano da lì. Dopo ogni modifica al Markdown vanno rigenerati tutti e due, così i tre file dicono la stessa cosa.

**Cosa serve**

- Python 3 con la libreria python-docx, che [strumenti/md_to_docx.py](../strumenti/md_to_docx.py) usa per scrivere il DOCX: `python -m pip install python-docx`.
- LibreOffice, per passare dal DOCX al PDF.
- Solo per rifare il marchio: le librerie PyMuPDF, fontTools e Brotli, usate da [strumenti/marchio.py](../strumenti/marchio.py). Brotli serve a fontTools per leggere il font del logotipo, che è in formato WOFF2; senza, lo script si ferma con "No module named brotli": `python -m pip install pymupdf fonttools brotli`.

**I comandi**, dalla cartella principale della repo:

```
python -I -X utf8 strumenti/md_to_docx.py strumenti/modello-stile-sersan.docx PRESENTAZIONE-CEO.md PRESENTAZIONE-CEO.docx "SerSan Agent OS · Proposta di progetto · Documento interno" strumenti/brand/sersan-lockup.png
soffice --headless --convert-to pdf PRESENTAZIONE-CEO.docx
```

- Il primo comando prende il modello di stile `strumenti/modello-stile-sersan.docx`, ricavato dal DOCX del piano marketing, converte il Markdown e scrive il DOCX. Il testo tra virgolette sostituisce il piè di pagina del modello. Il lockup, cioè marchio e scritta SERSAN, va grande in copertina e piccolo nell'intestazione dalla seconda pagina; i titoli prendono il blu scuro del marchio ([strumenti/md_to_docx.py](../strumenti/md_to_docx.py)).
- `-I` fa girare Python isolato dall'ambiente dell'utente: ignora le variabili `PYTHON*` e i pacchetti installati con `pip install --user`, quindi python-docx va installato per l'interprete che usi. `-X utf8` fa usare a Python la codifica UTF-8 per file e terminale, così accenti e simboli come «·» restano giusti.
- Il secondo comando fa lavorare LibreOffice senza aprire finestre (`--headless`) e scrive `PRESENTAZIONE-CEO.pdf` nella cartella da cui lo lanci; con `--outdir <cartella>` lo scrive altrove. Su Windows, se `soffice` non è nel PATH, l'elenco delle cartelle in cui il sistema cerca i comandi, usa il percorso completo: `"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf PRESENTAZIONE-CEO.docx`.

**Il marchio.** `python -I -X utf8 strumenti/marchio.py` riscrive `strumenti/brand/sersan-lockup.svg` e `sersan-lockup.png` a partire da `favicon.svg` e dal font Sersan Display del logotipo, derivato da Jost con licenza SIL OFL (`strumenti/brand/LICENSE-Jost.txt`). Serve solo se cambia il marchio: il PNG è già nella repo ([strumenti/marchio.py](../strumenti/marchio.py)).

**Il Markdown che lo script capisce.** Lo script legge solo questo sottoinsieme ([strumenti/md_to_docx.py](../strumenti/md_to_docx.py)):

- in cima, le righe `% Titolo`, `% Sottotitolo` e `% Stato`, che diventano la copertina;
- titoli da `#` a `####`: ogni `#` apre una pagina nuova, e i titoli `#` e `##` formano l'indice;
- paragrafi; elenchi con `- `, anche rientrati di due spazi per il secondo livello; elenchi numerati con `1. `; note con `> `;
- blocchi di codice delimitati da tre apici inversi; tabelle con le colonne separate da `|`;
- grassetto con `**testo**`, codice con un apice inverso per lato, link con `[testo](url)`.

## Fonti di questo file

- [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026: §1, §2, §4-§15 e appendici A e B.
- [ricerca/36-architettura-v2.md](../ricerca/36-architettura-v2.md): §4.5, §7, §12 e §13.
- [ricerca/25-board-michele-e-delta.md](../ricerca/25-board-michele-e-delta.md): §7.
- [ricerca/34-proposta-1-agent-sdk.md](../ricerca/34-proposta-1-agent-sdk.md): §4.3.
- [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md).
- [Board di Michele](../allegati/infra/SerSan%20Infra%20Board.md) e [board del rack](../allegati/infra/Rack%20SerSan%2012U.md).
- [strumenti/md_to_docx.py](../strumenti/md_to_docx.py) e [strumenti/marchio.py](../strumenti/marchio.py).
