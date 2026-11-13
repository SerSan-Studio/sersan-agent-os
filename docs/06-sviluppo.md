# Sviluppo: fasi, verifiche, giorni e rischi

> **Aggiornato l'11 novembre 2026 all'architettura v3**, «Cancello a livelli e motore a due corsie» ([ricerca/45](../ricerca/45-architettura-v3.md); [ADR da 0020 a 0028](adr/README.md)). Rispetto alla versione 2 sono cambiate tre cose:
> - ogni azione ha un livello di autonomia, da L0 a L3, e la verifica della settimana 8 chiede «nessun effetto fuori dal suo livello» invece di «nessun effetto senza una carta»; la revisione esterna esce dalla verifica della settimana 21 ([ADR-0020](adr/0020-autonomia-a-livelli.md); [ADR-0023](adr/0023-protezioni-essenziali.md));
> - il pilota usa solo la corsia N, le catene a schema; corsia S, bacheca e gruppi degli agenti e la prova di Buzz arrivano subito dopo la milestone 1, non nella fase 2 e nella fase 4 ([ADR-0021](adr/0021-motore-a-due-corsie.md); [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md));
> - entrano il «decisore», un modello per agente anche open-weight, il router a sei destinazioni con la corsia T sui posti Claude Team, e l'hardware si anticipa: la seconda GPU è proposta per la milestone 2, la linea di riserva va all'inizio della fase 3. Le stime dei giorni vanno rifatte ([ADR-0025](adr/0025-un-modello-per-agente.md); [ADR-0027](adr/0027-decisore.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ADR-0014](adr/0014-seconda-gpu-blackwell.md); [ADR-0019](adr/0019-linea-di-riserva.md)).
>
> **Il 12 novembre 2026** il gruppo di progetto ha fissato le scelte della milestone 2 ([ADR-0029](adr/0029-corsia-s-sessioni-a-giri.md); [ADR-0030](adr/0030-bacheca-gruppi-specchi.md)): il router entra nella milestone 2, la prova di Buzz aspetta il sì di Michele e una macchina Linux con Docker, i gruppi degli agenti si vedono nella Sala di controllo, la prova ombra del decisore si sposta alle milestone 5 e 6 ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ADR-0027](adr/0027-decisore.md)).

Questo file è per chi deve capire e costruire SerSan Agent OS, il sistema di 57 agenti AI in nove squadre che gira sul server di SerSan ([proposta §1](../PRESENTAZIONE-CEO.md)). Dice in che ordine si costruisce, come si verifica ogni passo, quanto lavoro serve, cosa può andare storto e cosa resta da decidere.

La proposta per i CEO, Alessandro Serratt e Michele Sanna, è [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026. Il 10 novembre 2026 i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)). La proposta resta com'è: fasi, settimane, costi e decisioni vengono ancora da lì. Dove la v3 la supera, la citazione della proposta resta come storia e accanto c'è la regola di oggi, con la sua fonte. Se due fonti dicono cose diverse, vale prima l'intestazione di [ricerca/45](../ricerca/45-architettura-v3.md), poi le ADR, poi il resto di ricerca/45, poi la proposta. Il piano tecnico della v2 è in [ricerca/36 §7](../ricerca/36-architettura-v2.md).

## In breve

- Sette fasi, dalla 0 alla 6, in circa 53 settimane ([proposta §11 e §15](../PRESENTAZIONE-CEO.md)).
- Lo sviluppo è partito il 10 novembre 2026 sulle macchine di sviluppo, con la milestone 1: il Cancello a livelli e la corsia N. Le sette milestone del PRD portano al collaudo della settimana 8 (la sezione qui sotto).
- Il pilota delle fasi 0 e 1 usa solo la corsia N. Corsia S, bacheca, gruppi degli agenti e prova di Buzz si costruiscono subito dopo la milestone 1 ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)). Dal 12 novembre la prova di Buzz aspetta il sì di Michele e una macchina Linux con Docker, e nella milestone 2 entra anche il router a più motori ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- Due verifiche restano: alla settimana 8 si misura il pilota sul banco di prova; alla settimana 21 si decide se portare nella memoria i dati dei clienti ([proposta §1 e §11](../PRESENTAZIONE-CEO.md)). Il criterio di base diventa «nessun effetto fuori dal suo livello» ([ricerca/45 §6.4](../ricerca/45-architettura-v3.md)).
- Nelle fasi 0 e 1 il lavoro lo portano avanti Alberto, Mattia e Michele. Ad Alessandro si chiedono l'assessment iniziale (la descrizione dei processi che fa ogni settimana), le sue regole di lavoro, il punto del venerdì su cosa si è automatizzato e le approvazioni dal telefono ([proposta §1 e §10](../PRESENTAZIONE-CEO.md)).
- I giorni di sviluppo sono solo nella sezione 5. La milestone 1 è cresciuta rispetto alla stima della v3: la stima va rifatta dopo i primi gruppi di compiti.

## Da dove parte lo sviluppo

**Dove sta il codice.** Il codice sta in una repo privata dell'organizzazione, «sersan-agent-os-codice», insieme a PRD, spec e piani di sviluppo. Il PRD è il documento che dice cosa deve fare il prodotto; lo spec dice come è fatto un pezzo. In questa repo restano la proposta, la ricerca, i documenti di progetto e le ADR ([ricerca/45, «Decisione del gruppo di progetto», D4](../ricerca/45-architettura-v3.md)).

**Tre parole per cominciare.**
- Il **Cancello a livelli** è l'unico programma che esegue le azioni degli agenti, e dà a ognuna un livello: da L0, una persona fa a mano, a L3, l'azione parte da sola dentro regole e tetti ([ADR-0020](adr/0020-autonomia-a-livelli.md)).
- La **corsia N** è il modo più semplice di far lavorare un agente: il codice sceglie i passi e i destinatari, e il modello scrive solo i campi di un modulo, senza strumenti ([ADR-0021](adr/0021-motore-a-due-corsie.md)).
- La **Sala di controllo** è la pagina web locale, usabile anche dal telefono sulla rete dell'ufficio, dove si vedono e si decidono carte, finestre, promozioni e stop di emergenza; prima che il bot di Teams sia pronto, si approva da lì ([architettura](03-architettura.md)).

**Le sette milestone del PRD.** Una milestone è un traguardo che si vede funzionare.

| # | Milestone | Cosa porta |
|---|---|---|
| 1 | Cancello a livelli e corsia N, con la Sala di controllo | sulle macchine di sviluppo una catena a schema propone azioni, e L1, L2 e L3 escono solo al loro livello |
| 2 | Corsia S, bacheca e gruppi degli agenti, prova di Buzz, primo modello open-weight; dal 12 novembre anche il router a più motori | gli agenti che ragionano a più passi; il posto dove gli agenti si passano il lavoro; la prima prova di un modello con i pesi pubblici; il router che sceglie dove va ogni lavoro, con la corsia T come destinazione di prova |
| 3 | Prove con Microsoft e LiteLLM | bot di Teams senza Azure, identità di chi approva, «Ferma» sulla carta, LiteLLM davanti alle catene |
| 4 | Telefono e posta | una bozza approvata dal telefono, o lasciata passare, parte una volta sola e solo all'indirizzo esatto |
| 5 | Dalla call al riassunto | lettura delle trascrizioni, oscuramento, riassunto L3 nel canale interno |
| 6 | Tre agenti sul banco | debrief alle 7:00, post-call, follow-up |
| 7 | Collaudo della settimana 8 | i criteri della sezione 4.1, misurati |

Il contenuto delle milestone viene da [ricerca/45 §6.4 e §12](../ricerca/45-architettura-v3.md). La numerazione del PRD sostituisce quella di ricerca/45, perché la corsia S è stata anticipata: la milestone 2 è nuova, e le altre scalano di un posto. Le ADR e le ricerche 46-49 contano ancora come ricerca/45: dove scrivono «milestone 2» per le prove con LiteLLM e Teams, qui è la milestone 3; dove scrivono «milestone 3» per telefono e posta, qui è la 4. Fanno eccezione la prova dei modelli locali e quella del decisore, con la seconda GPU che serve alla prima: qui stanno nella milestone 2, insieme al primo modello open-weight. La parte che passa da LiteLLM, come Jev, si chiude con le prove di LiteLLM della milestone 3. Dal 12 novembre fa eccezione anche il router: ADR-0028 lo mette nella sua milestone 2, cioè nella 3 del PRD, ma la revisione di quel giorno lo porta nella milestone 2 del PRD, perché LiteLLM serve solo a Jev. ADR-0029, ADR-0030 e le revisioni del 12 novembre contano come il PRD ([indice delle ADR](adr/README.md)).

**Lo stato della milestone 1.** È finita il 12 novembre 2026: il codice è unito nel ramo principale della repo, con oltre 900 prove automatiche, e l'ultimo giro di correzioni è del 13 novembre. Lo spec è alla revisione 3.3, con 49 criteri di accettazione. Il piano aveva 14 gruppi e 70 compiti. Restano a una persona tre verifiche: la lista di controllo della Sala, quella dal telefono e il giro dal vivo con la chiave API. Lo sviluppo è partito il 10 novembre 2026 sulle macchine di sviluppo, con dati di prova e un modello a copione, cioè un modello finto che dà risposte scritte prima, senza chiave API. Oltre a Cancello e corsia N, la milestone 1 comprende tre cose che la stima di [ricerca/45 §12.1](../ricerca/45-architettura-v3.md) non prevedeva:
- il **decisore**, un'interfaccia che fa domande chiuse a un modello e riceve una probabilità per ogni risposta ([ADR-0027](adr/0027-decisore.md));
- il **registro dei modelli**, un file che dice per ogni modello costi, capacità (testo, immagini, audio) e colori dei dati ammessi ([ADR-0025](adr/0025-un-modello-per-agente.md));
- i **testi letti da file**: le regole «Come lavoro» e gli altri testi stanno in file Markdown e YAML nella repo del codice, letti da un'interfaccia unica, finché non si sceglie la casa dei testi ([ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md)).

Per questo la stima dei giorni va rifatta (sezione 5).

## Le parole del piano

- **Motore**: il nostro programma che fa girare gli agenti, scritto in TypeScript ([ADR-0010](adr/0010-typescript-motore.md)). Ha due corsie nello stesso codice: la **corsia N**, catene a schema senza strumenti, e la **corsia S**, sessioni dell'Agent SDK di Claude, cioè Claude Code usato come libreria, per gli agenti che decidono il passo dopo o usano più strumenti. La corsia S ha un solo runner, il programma che fa girare le sessioni, con al massimo 6 sessioni insieme ([ADR-0021](adr/0021-motore-a-due-corsie.md)). Nella proposta il motore era solo la corsia S, con un processo per lavoro ([proposta §5.1](../PRESENTAZIONE-CEO.md)).
- **Sveglia e registro degli eventi**: gli orari stanno in una tabella del motore e gli eventi entrano da un solo ingresso, `POST /eventi`. Ogni evento ha una chiave e uno stato, così un crash non perde una call e non manda due mail ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)). Nella proposta la sveglia era n8n ([proposta §5.3](../PRESENTAZIONE-CEO.md)); oggi n8n è facoltativo.
- **Router e corsia T**: il router sceglie dove va ogni lavoro fra sei destinazioni: una regola nel codice, una catena N su un modello del nostro server, una catena N su Claude via API, una sessione S, la corsia T, una persona. La **corsia T** è una sessione di Claude Code su un posto Claude Team, avviata dal motore con un compito programmato, solo per lo sviluppo di progetti in codice e i lavori lunghi di quattro agenti; consegna una pull request, cioè una richiesta di modifica da rivedere e accettare ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- **Cancello**: l'unico programma che può mandare una mail, scrivere al cliente, toccare il CRM (l'archivio di contatti e trattative) o telefonare. Dà a ogni **terna**, cioè agente, tipo d'azione e classe del destinatario, un livello: **L0** una persona esegue, **L1** una persona approva con una carta, **L2** l'azione parte da sola dopo una finestra in cui si può fermare, **L3** parte subito, dentro regole, tetti e registro. La classe del destinatario la calcola il Cancello dai dati (calendario, partecipanti registrati, CRM), mai dal testo di una mail ([ADR-0020](adr/0020-autonomia-a-livelli.md)). Registra tutto ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- **Carta e finestra**: la carta è la richiesta di approvazione L1, con il testo esatto dell'azione e una scadenza di 3 giorni lavorativi, 24 ore per ciò che dipende dal tempo. La finestra L2 dice «parte alle HH:MM» e ha tre tasti: «Ferma», «Modifica», «Invia ora»; conta solo in orario di lavoro, dalle 8:30 alle 19:00 dal lunedì al venerdì ([ADR-0020](adr/0020-autonomia-a-livelli.md)). Arrivano in Teams, anche sul telefono, o nella Sala di controllo.
- **Promozione e discesa**: una terna sale da L1 a L2 dopo 5 sì di fila senza modifiche di sostanza, e da L2 a L3 dopo 15 finestre senza «Ferma»; la promozione la conferma il responsabile della squadra. Un segnale negativo la fa scendere da sola ([ADR-0020](adr/0020-autonomia-a-livelli.md)). Prende il posto delle regole "Sempre" della proposta, che si creavano dopo venti approvazioni uguali e valevano per una sola destinazione ([proposta §5.4](../PRESENTAZIONE-CEO.md)).
- **Decisore**: l'interfaccia del nostro codice che fa domande chiuse (sì o no, scelta, punteggio) e riceve una probabilità; sotto la soglia scritta in un file la risposta vale «dubbio». Una sua risposta può solo rendere il sistema più prudente. Il motore di partenza è Jev, un modello «System One» che risponde a domande chiuse invece di scrivere testo, sui testi verdi, e sui gialli quando Michele ammette il suo fornitore; per i testi rossi restano un modello in casa o le regole ([ADR-0027](adr/0027-decisore.md)). Jev entra nella milestone 3, con LiteLLM; fino ad allora il decisore gira sul copione, su un modello a schema e su un decisore in casa che legge la probabilità della prima parola ([ADR-0027, revisione del 12 novembre 2026](adr/0027-decisore.md)).
- **LiteLLM**: la porta da cui passano le chiamate degli agenti ai modelli; dà a ogni agente, squadra e persona il suo budget ([proposta §5.1](../PRESENTAZIONE-CEO.md)). Oggi la porta serve anche i modelli open-weight, cioè con i pesi pubblici, sul nostro server o da un fornitore, e Jev; la corsia T non passa da LiteLLM ([ADR-0004](adr/0004-litellm-banca-token.md); [ADR-0025](adr/0025-un-modello-per-agente.md)).
- **Server MCP**: una presa standard a cui un agente si collega per usare uno strumento, per esempio la memoria, Jira o SersanOutreach, la nostra piattaforma outbound, cioè per i contatti commerciali in uscita su LinkedIn ed email, che diventa il CRM degli agenti ([proposta §1, §7.1 e §7.3](../PRESENTAZIONE-CEO.md)).
- **Bacheca e gruppi degli agenti**: la bacheca è il posto, nel motore, dove gli agenti si passano i compiti; i gruppi di chat, uno per squadra, uno per cliente e uno comune «Agenti», mostrano quei passaggi alle persone. Un freno nel codice ferma le catene infinite: 8 passaggi per catena, conteggio dall'ultimo messaggio di una persona, al massimo due rimbalzi fra la stessa coppia di agenti, un tetto in dollari per catena, poi una carta «Continua?» ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)).
- **Colori dei dati**: verde è il pubblico o l'interno non personale; giallo sono contatti di lavoro, campi del CRM e riassunti; rosso sono audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone e finanza. Il rosso resta sul server, oppure va all'API di Anthropic (l'accesso a Claude dai nostri programmi) dopo aver oscurato in locale i dati non necessari ([proposta §5.6](../PRESENTAZIONE-CEO.md)). Verso la corsia T il rosso non va mai, neanche oscurato; i fornitori terzi di modelli ricevono solo verde e giallo ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ADR-0025](adr/0025-un-modello-per-agente.md)).
- **Claude Team e skill**: Claude Team è la finestra di lavoro di ognuno, con chat, skill e progetti per squadra; una skill è una procedura scritta che Claude segue per un lavoro che si ripete. Ogni processo che si ripete diventa una skill, ogni skill che funziona diventa un agente ([proposta §4.11 e §4.12](../PRESENTAZIONE-CEO.md)).
- **Buzz**: la chat open source di Block fatta per persone e agenti, in prova sul nostro server ([proposta §4.11](../PRESENTAZIONE-CEO.md)); si collega alla bacheca come specchio, e si prova quando Michele lo ammette e c'è una macchina Linux con Docker ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0030](adr/0030-bacheca-gruppi-specchi.md)).
- **Board di Michele**: il disegno dell'infrastruttura del server, con reti, servizi e una roadmap in sei fasi, da F0 a F5 ([board di Michele](../allegati/infra/SerSan%20Infra%20Board.md)).

## 1. Come leggere il piano

**Settimane, milestone e giorni.** Le settimane sono il calendario delle fasi della proposta; le milestone sono i traguardi del PRD dentro le fasi 0 e 1; la stima dei giorni di sviluppo è nella sezione 5 ([proposta §11](../PRESENTAZIONE-CEO.md)).

**Due cantieri.** L'infrastruttura la porta avanti Michele, con il suo board; sopra, noi costruiamo il sistema di agenti. Ogni fase parte quando la precedente è verificata, come nel board ([proposta §11](../PRESENTAZIONE-CEO.md)).

| Fase del board | Cosa porta | In corso durante le nostre fasi |
|---|---|---|
| F0 Arrivi | arrivo e montaggio dell'hardware, prova della RAM, export completo da Azure, il cloud di Microsoft dove oggi gira SersanOutreach | 0 |
| F1 Fondamenta | OPNsense, il software del firewall, con le reti separate; Proxmox, il sistema che fa girare le macchine virtuali sul server; l'accesso da fuori solo con identità verificata; il backup | 0 e 1 |
| F2 Via da Azure | i servizi, SersanOutreach compreso, passano da Azure al server; le macchine Azure si spengono | 1 e 2 |
| F3 Sicurezza | strumenti di sicurezza, inventario dei servizi, log e avvisi; documentazione per le norme ISO e per Cyber Essentials, la certificazione di sicurezza che chiede, fra l'altro, le patch critiche (gli aggiornamenti di sicurezza) entro 14 giorni e il secondo fattore di accesso (MFA) sui servizi cloud | 2 |
| F4 AI e bandi | la GPU per i modelli locali; la pipeline, cioè la catena di lavorazione, che rende ricercabili i documenti; i bandi con Firecrawl, che trasforma le pagine web in testo pulito, e n8n, che fa partire i lavori a orario e collega le applicazioni; LiteLLM con i budget | 2, 3 e 4 |
| F5 Laboratorio e dopo | le macchine di prova del laboratorio (Experimental 1 e 2) e gli ampliamenti dell'hardware | 4, 5 e 6 |

Fonti: [board di Michele, roadmap](../allegati/infra/SerSan%20Infra%20Board.md); la colonna di destra viene da [proposta §11](../PRESENTAZIONE-CEO.md); Azure da [proposta §7.1](../PRESENTAZIONE-CEO.md); Cyber Essentials da [ricerca/25 §7](../ricerca/25-board-michele-e-delta.md); n8n da [proposta §5.3](../PRESENTAZIONE-CEO.md). n8n resta nel board di Michele per i collegamenti che servono, ma il sistema di agenti non ne dipende: la sveglia sta nel motore ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).

**I tempi del board non sono ancora fissati.** In quante settimane si chiudono F0-F4 lo chiede la [domanda 1 per Michele](../DOMANDE-PER-MICHELE.md). Intanto il piano non si ferma: il pilota parte sul banco di prova ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)).

**Il banco di prova.** Il pilota non aspetta il board e non lo riordina. Nelle settimane 5-8 gira su una macchina di prova nella rete del laboratorio, con una chiave API limitata e un tetto di spesa, e salva solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata ([proposta §11](../PRESENTAZIONE-CEO.md)). Prima che la rete del laboratorio esista, il lavoro gira sulle macchine di sviluppo con dati di prova ([ricerca/36 §7.1](../ricerca/36-architettura-v2.md)): è lì che è partita la milestone 1, con Windows e Node 22, senza Docker ([ricerca/45 §6](../ricerca/45-architettura-v3.md)). Se Michele anticipa il posto per gli agenti sul server (nella proposta: LiteLLM, il database, i segreti, n8n e due macchine virtuali, prima di F4), il passaggio sul server si anticipa ([proposta §11](../PRESENTAZIONE-CEO.md); [domanda 2 per Michele](../DOMANDE-PER-MICHELE.md)). Oggi n8n non serve al banco: basta la tabella degli orari del motore ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).

**Prima il funnel.** Il funnel è il percorso che porta un contatto (lead) a diventare cliente; oggi SersanOutreach ha 11 lead, 1 risposta e 0 meeting ([proposta §1](../PRESENTAZIONE-CEO.md)). Se alla settimana 8 l'email non è ancora attiva e i founder, Alessandro e Michele, non pubblicano dai loro profili LinkedIn, si fanno comunque le fasi 2 e 3, utili anche al funnel, e la fase 5 aspetta. "Andrea", l'agente vocale che richiama le lead che lo chiedono, e la pipeline pesata, cioè la probabilità di chiusura calcolata sullo storico, hanno senso solo con lead vere ([proposta §2.2, §8.1 e §11](../PRESENTAZIONE-CEO.md)). Con questi volumi i livelli L2 e L3 verso l'esterno arrivano tardi, e alla settimana 8 il valore è soprattutto interno ([ricerca/45 §10](../ricerca/45-architettura-v3.md)).

**Dopo la fase 6** resta una manutenzione continua: aggiornamenti dell'Agent SDK, del Cancello e dei servizi, agenti nuovi ([proposta §11](../PRESENTAZIONE-CEO.md)).

## 2. Le regole che valgono in ogni fase

Ogni pezzo si costruisce dentro queste regole.

- **Gli agenti propongono, il codice esegue.** Nessun agente ha in mano un bottone che invia, pubblica, paga o cancella: ogni effetto verso l'esterno passa dal Cancello, qualunque sia la corsia. La macchina degli agenti non ha accesso a internet e parla solo con LiteLLM, con i server MCP e con il Cancello ([proposta §5.4 e §9.2](../PRESENTAZIONE-CEO.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)). La corsia T gira sulle macchine di Anthropic e consegna solo una pull request, che entra in `main` con il sì di una persona ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- **Ogni azione ha il suo livello.** Il livello di partenza di ogni classe lo fissa il gruppo di progetto, scrivendo il motivo, in un file in git; la promozione la conferma il responsabile; abbassare un livello può chiunque dei quattro ([ADR-0020](adr/0020-autonomia-a-livelli.md)).
- **Limiti fissi nel codice.** Cancellazioni e credenziali sono sempre negate; i pagamenti li fa una persona; offerte, contratti, fatture, prezzi e destinatari nuovi restano a L1 ([ADR-0020](adr/0020-autonomia-a-livelli.md); [ADR-0023](adr/0023-protezioni-essenziali.md)).
- **Il codice sceglie i destinatari, mai un modello.** Prima di ogni uscita L2 o L3 un controllo cerca cifre, prezzi, date e impegni che non vengono dal CRM; se ne trova uno, l'azione scende a L1 ([ADR-0020](adr/0020-autonomia-a-livelli.md)).
- **Un dubbio rende il sistema più prudente.** Una risposta del decisore può solo abbassare un livello, mandare una carta, colorare di rosso o passare a una corsia più capace; un dubbio non porta mai in corsia T ([ADR-0027](adr/0027-decisore.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- **Prima di ogni azione il motore chiede al Cancello**; se il Cancello non risponde in tempo, non succede nulla e la catena ritenta con la stessa chiave ([proposta §5.3](../PRESENTAZIONE-CEO.md); [ricerca/45 §6.2, AC-004](../ricerca/45-architettura-v3.md)).
- **Le automazioni nascono spente.** Ogni automazione parte in prova a secco: per una o due settimane mostra cosa avrebbe fatto, senza farlo ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Il testo di terzi non è mai un'istruzione.** Mail, trascrizioni, pagine web e risposte dei potenziali clienti entrano nella corsia N solo come campi, e il codice sceglie i destinatari. È la difesa contro le iniezioni di prompt, cioè le istruzioni nascoste in un testo per far agire un agente ([proposta §9.2](../PRESENTAZIONE-CEO.md); [ADR-0021](adr/0021-motore-a-due-corsie.md)).
- **Ogni agente legge le regole "Come lavoro"** della persona per cui lavora, in ogni catena e in ogni sessione ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md)).
- **Tetti che fermano davvero.** Ogni agente e ogni lavoro ha un budget: all'80% arriva un avviso, al 100% si ferma. In più ogni classe esterna a L3 ha un tetto al giorno, per esempio 15 follow-up e 10 inviti per agente e al massimo 2 messaggi per destinatario; oltre il tetto l'azione diventa una carta ([proposta §9.2](../PRESENTAZIONE-CEO.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)).
- **Tutto registrato e revocabile.** Registro delle azioni a sola aggiunta, segreti oscurati prima di qualsiasi log, «Annulla» delle scritture interne senza cancellare nulla, stop di emergenza dal telefono, da Teams o dalla Sala di controllo ([proposta §9.2](../PRESENTAZIONE-CEO.md); [ADR-0023](adr/0023-protezioni-essenziali.md)).
- **Riga AI.** Ciò che parte a L2 o L3 porta una riga che dichiara l'assistente AI di SerSan; il testo definitivo lo fissa il parere legale ([ADR-0020](adr/0020-autonomia-a-livelli.md)).
- **Nessun bot nei canali condivisi con i clienti**: lì scrive solo il Cancello, al livello della classe del destinatario ([proposta §4.11](../PRESENTAZIONE-CEO.md); [ADR-0006](adr/0006-teams-chat-di-gruppo.md)).
- **Versioni fissate.** L'Agent SDK cambia quasi ogni giorno: si tiene una versione fissata e la si aggiorna ogni due settimane, dopo i dieci scenari di prova, entro i 14 giorni ([proposta §5.3 e §13](../PRESENTAZIONE-CEO.md)). Riguarda la corsia S; la corsia N non dipende da Claude Code ([ricerca/45 §10](../ricerca/45-architettura-v3.md)). Anche Jev e ogni altro modello hanno la versione fissata, e cambiare modello senza una valutazione riporta la terna a L1 ([ADR-0027](adr/0027-decisore.md); [ADR-0025](adr/0025-un-modello-per-agente.md)).
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

Fonti: [proposta §4.12 e §11](../PRESENTAZIONE-CEO.md). Gli agenti di ogni fase sono quelli delle tabelle di [proposta §4](../PRESENTAZIONE-CEO.md), dove ogni agente ha la sua fase. Con la v3 cambia l'ordine di alcuni pezzi, non l'elenco delle funzioni:
- le sette milestone del PRD stanno dentro le fasi 0 e 1 e finiscono con il collaudo della settimana 8;
- i tre agenti del pilota girano solo nella corsia N ([ricerca/45 §1.2](../ricerca/45-architettura-v3.md));
- corsia S, bacheca, gruppi degli agenti e prova di Buzz si costruiscono nella milestone 2, subito dopo la milestone 1 ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)); dal 12 novembre con loro c'è il router, e la prova di Buzz aspetta il sì di Michele e una macchina Linux con Docker ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ADR-0030](adr/0030-bacheca-gruppi-specchi.md));
- brief e bozza d'offerta possono entrare nella fase 2, se c'è capacità ([ricerca/45 §4.1](../ricerca/45-architettura-v3.md));
- le altre funzioni restano nelle fasi di [ricerca/45 §4.2](../ricerca/45-architettura-v3.md), con il livello scritto in ogni fase qui sotto.

**I livelli di partenza** di ogni fase vengono da [ricerca/45 §4.1 e §4.2](../ricerca/45-architettura-v3.md). Sono i livelli probabili con i volumi di oggi; dove non c'è una fonte diversa sono una proposta del gruppo di progetto. Se il parere legale chiude una porta, la funzione resta e la sua classe rimane a L1 ([ricerca/45 §2.8](../ricerca/45-architettura-v3.md)).

### Fase 0 · Valore subito e prove (settimane 1-4)

**Cosa si fa**

- Claude Team per tutti, con le skill, i template SerSan per offerte, slide e recap (i riassunti dopo le call) e un progetto per squadra. I cinque posti sono gratuiti per il primo anno grazie al bundle startup di Anthropic, che dà anche i crediti API ([proposta §1 e §11](../PRESENTAZIONE-CEO.md)).
- Le persone. Nella settimana 1 l'assessment: ognuno descrive quali processi fa ogni settimana e con quali strumenti. Nelle settimane 1-2 ognuno scrive come vuole riassunti, prossimi passi, report e orari di non disturbo: gli agenti leggono queste regole prima di ogni lavoro. Formazione documentata per tutti e quattro, come chiede l'AI Act, il regolamento europeo sull'intelligenza artificiale (art. 4) ([proposta §5.5 e §10](../PRESENTAZIONE-CEO.md)). La proposta metteva queste regole in BookStack, il wiki sul nostro server; oggi stanno in file nella repo del codice, finché prima della fase 2 non si sceglie la casa dei testi ([ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md)).
- L'email: decisione con il legale e casella attiva. Il parere legale unico consegna entro la settimana 3 i punti del pilota (email B2B, cioè tra aziende, verso l'Italia; registrazione delle call; trasferimenti di dati verso gli USA) e prima della fase 2 tutto il resto ([proposta §9.4 e §11](../PRESENTAZIONE-CEO.md)). Al parere si aggiungono due domande: il testo della riga AI e se un messaggio partito a L2 vale come approvato ([ricerca/45 §2.8 e §9.1](../ricerca/45-architettura-v3.md)).
- SersanOutreach in sicurezza prima di collegare gli agenti: la decisione sulle regole dell'email (indirizzo e link di cancellazione nel footer, il piè di pagina della mail, oppure deroga registrata con parere legale), l'identità firmata dei chiamanti, il secondo fattore per i 7 account staff, una copia dei dati fuori dai suoi cloud con una prova di ripristino riuscita, gli avvisi che arrivano davvero a una persona ([proposta §7.4](../PRESENTAZIONE-CEO.md)).
- Il registro dei trattamenti e la valutazione d'impatto sulla protezione dei dati. Entro la settimana 3, con il parere, si decide quali dati arrivano a Claude Team; fino ad allora verde e giallo, e il rosso solo oscurato ([proposta §5.6 e §13](../PRESENTAZIONE-CEO.md)).
- Lo sviluppo, sulle macchine di sviluppo: la milestone 1 (Cancello a livelli, corsia N, decisore, registro dei modelli, testi da file, Sala di controllo), poi la milestone 2 (corsia S, bacheca e gruppi, prova di Buzz, primo modello open-weight e, dal 12 novembre, il router a più motori). La proposta chiamava questo lavoro «la prima parte del motore» ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Le quattro prove tecniche della proposta: il bot di Teams, l'identità di chi approva, il blocco delle azioni, LiteLLM ([proposta §11](../PRESENTAZIONE-CEO.md)). Oggi bot di Teams, identità e LiteLLM sono la milestone 3, con «Ferma» sulla carta; il blocco delle azioni da parte del Cancello si prova già con la batteria di prove della milestone 1 ([ricerca/45 §6.2 e §6.4](../ricerca/45-architettura-v3.md)). Il router, che sceglie fra le sei destinazioni, non aspetta LiteLLM: dal 12 novembre entra nella milestone 2, sul decisore che c'è, con la corsia T come destinazione di prova. La prova dal vivo della corsia T, con i passi di [ricerca/49 §7](../ricerca/49-instradamento-a-piu-motori.md), la fa Alberto dal suo account; solo dopo si scrive l'adattatore che la avvia davvero. Jev con LiteLLM resta nella milestone 3 ([ADR-0028, revisione del 12 novembre 2026](adr/0028-instradamento-a-piu-motori.md)). La corsia T sui progetti veri arriva solo dopo quella prova e la conferma scritta di Anthropic che l'uso rientra nei termini ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- Il marketing riparte: con Claude Team e la sessione presidiata di Alberto, cioè con una persona davanti allo schermo, si propone il calendario fino a Natale e si programmano, dopo il sì, i 22 testi dei post già pronti. I numeri del lunedì li compila una skill di Claude Team ([proposta §8.2 e §8.4](../PRESENTAZIONE-CEO.md)).
- Le verifiche della prima settimana, senza chiedere nulla ai CEO: cosa include il bundle startup (crediti mensili e scadenza), quale piano di Microsoft 365 (M365) e quale piano Jira abbiamo, quanto del kit commerciale paghiamo già. Si chiede anche ad Anthropic la conservazione zero dei dati delle API, che è gratuita ([proposta §14](../PRESENTAZIONE-CEO.md)). Si controlla anche se il nostro piano Team ha diritto ai crediti API inclusi, fino a 500 $ al mese ([ricerca/49 §1.3 e §9](../ricerca/49-instradamento-a-piu-motori.md)).
- La riaccensione automatica del server dopo un blackout, chiesta a Michele prima del primo lavoro L3 notturno sul banco: costa 0 € ([ricerca/45 §11](../ricerca/45-architettura-v3.md)).

**Livelli di partenza**: nessun agente del sistema lavora ancora per le persone. Brief, offerte, slide e marketing passano dalle skill di Claude Team, cioè a mano (L0); i post si pubblicano dopo il sì di una persona. Sulle macchine di sviluppo la milestone 1 prova L1, L2 e L3 su dati di prova ([ricerca/45 §4.1 e §12.1](../ricerca/45-architettura-v3.md)).

**Cosa si vede alla fine**: tutti e quattro in Claude Team ogni giorno. Calendario dei post pieno fino a Natale. Prime offerte e slide con il nostro stile. Email decisa e casella attiva. SersanOutreach sicuro su identità e MFA ([proposta §11](../PRESENTAZIONE-CEO.md)). Sulle macchine di sviluppo, da un comando che inietta «trascrizione pronta», il riassunto esce a L3, il follow-up arriva come carta o come finestra, un «Ferma» riporta la terna a L1 e lo stop annulla tutto ([ricerca/45 §12.1](../ricerca/45-architettura-v3.md)).

### Fase 1 · Pilota su banco di prova (settimane 5-8)

**Cosa si fa**

- Il motore sul banco di prova, con il Cancello a livelli, i dieci scenari di prova riscritti sui livelli e il registro degli agenti: per ognuno nome, squadra, responsabile umano, modello, corsie ammesse, cosa può toccare, tetto di spesa e costo del mese ([proposta §4.12 e §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §7.3](../ricerca/36-architettura-v2.md); [ricerca/45 §6.1](../ricerca/45-architettura-v3.md); [ADR-0025](adr/0025-un-modello-per-agente.md)).
- I tre agenti del pilota girano solo nella corsia N: riassumono, estraggono e scrivono, e per questo basta una catena a schema ([ricerca/45 §1.2](../ricerca/45-architettura-v3.md)). La proposta prevedeva qui il Cancello versione 1 con le carte ([proposta §5.4](../PRESENTAZIONE-CEO.md)); oggi è il Cancello a livelli della milestone 1.
- L'invio da Outlook attraverso Microsoft Graph, l'interfaccia con cui i programmi leggono e scrivono posta, calendario e trascrizioni di M365, solo all'indirizzo esatto del partecipante registrato (milestone 4) ([proposta, appendice A, voce B3](../PRESENTAZIONE-CEO.md); [ricerca/45 §12.3](../ricerca/45-architettura-v3.md)).
- Le carte e le finestre in Teams con l'identità di chi approva. Se il bot di Teams dà problemi, prima una registrazione Azure Bot gratuita, senza macchine accese, e in ultima istanza la pagina del Cancello con gli avvisi in Teams ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)). Intanto si usa la Sala di controllo.
- Le trascrizioni delle call Teams, che Microsoft scrive già, lette dal banco di prova: le legge ogni 5 minuti un lettore nel nostro codice, e un evento non si perde (milestone 5) ([proposta §6.4 e §11](../PRESENTAZIONE-CEO.md); [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).
- L'oscuramento locale dei dati non necessari, costruito e misurato in questa fase ([proposta §5.6](../PRESENTAZIONE-CEO.md)).
- Tre agenti (milestone 6): il Post-call (riassunto e bozza della mail di follow-up, quella che segue la call), l'Analista chiamate (riassunto secondo le regole di ciascuno, nel registro di tutti i meeting) e il Report del mattino (alle 7:00, per ciascuno, il debrief: cosa è successo ieri, cosa è partito da solo, scadenze, task, pipeline, cosa aspettano gli agenti da noi, e le proposte di promozione) ([proposta §4.2 e §4.8](../PRESENTAZIONE-CEO.md); [ricerca/45 §4.1](../ricerca/45-architettura-v3.md)).

**Livelli di partenza** ([ricerca/45 §4.1](../ricerca/45-architettura-v3.md)):
- ingresso nelle call Teams organizzate da noi: L3;
- riassunto nel canale interno e registro dei meeting: L3, entro 10-20 minuti dalla trascrizione;
- to-do: L3 dentro il riassunto; in Jira se la fase ha margine (1,75 giorni di sviluppo);
- meeting e trattative nel CRM: L0, con i campi già pronti nel riassunto;
- follow-up alla persona appena incontrata, cioè all'indirizzo esatto di chi era in una call registrata e avvisata negli ultimi 14 giorni: L2 con una finestra di 30 minuti, per decisione del gruppo di progetto. Se il parere lo esclude prima degli invii veri della milestone 4, la classe torna a L1 cambiando una riga di configurazione ([ricerca/45, «Decisione del gruppo di progetto», D11](../ricerca/45-architettura-v3.md));
- debrief alle 7:00: L3;
- brief, bozza d'offerta e marketing: skill in Claude Team (L0); invio dell'offerta L1; post della pagina aziendale e dei founder L1;
- passaggi fra agenti: dall'Analista al Post-call, nel registro degli eventi;
- correzioni che diventano esempi: L3.

**Cosa si vede alla fine**: dopo una call Teams il riassunto arriva nel canale interno e la bozza della mail arriva come finestra o come carta sul telefono; parte una volta sola e solo all'indirizzo esatto. Debrief alle 7:00 per tutti. Poi il collaudo della settimana 8 (milestone 7, sezione 4) ([proposta §11](../PRESENTAZIONE-CEO.md); [ricerca/45 §12](../ricerca/45-architettura-v3.md)).

### Fase 2 · Pilota sul server e squadre che si parlano (settimane 9-21)

**Cosa si fa**

- Il motore passa sul server con LiteLLM per i budget ([proposta §11](../PRESENTAZIONE-CEO.md)). La proposta metteva qui n8n per gli orari; oggi gli orari stanno nel motore e n8n è facoltativo ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).
- Il router, costruito nella milestone 2 e provato sul banco, sceglie la destinazione dei lavori anche sul server; con LiteLLM, dalla milestone 3, entra anche Jev. Le corsie ammesse da ogni agente restano scritte nel suo registro ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- La proposta faceva aggiungere qui al Cancello la chiave FIDO2, una chiave di sicurezza fisica, per offerte, contratti, fatture e primi contatti, e le regole "Sempre" ([proposta §5.4 e §11](../PRESENTAZIONE-CEO.md)). Oggi la FIDO2 non serve sulle carte, e resta per l'accesso al board con NetBird; al posto delle regole "Sempre" ci sono livelli e promozioni, già dalla milestone 1. In questa fase i contatori delle promozioni lavorano sui casi veri ([ADR-0023](adr/0023-protezioni-essenziali.md); [ADR-0020](adr/0020-autonomia-a-livelli.md); [ricerca/45 §6.4](../ricerca/45-architettura-v3.md)).
- Nove bot di squadra in Teams, ognuno con il nome dei suoi agenti, e lo stand-up degli agenti ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md); [ricerca/45 §4.1](../ricerca/45-architettura-v3.md)).
- Jira, la casa dei testi e la memoria aperti agli agenti ([proposta §11](../PRESENTAZIONE-CEO.md)). La casa dei testi si sceglie prima di questa fase fra BookStack, come nella proposta, e una cartella di file Markdown in git sul server ([ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md)). Con BookStack servono il database MariaDB da aggiungere al board, circa 2 giorni di posa e 0,5-2 di server MCP; per la cartella in git il lavoro non è ancora stimato e va stimato dopo le prove ([proposta, appendice A, voce A2](../PRESENTAZIONE-CEO.md); [ricerca/46 §7 e §8](../ricerca/46-obsidian-come-casa-dei-testi.md)).
- SersanOutreach collegato: i suoi due server MCP, uno di lettura con 19 strumenti e uno operatore con 14 operazioni, raggiungibili dal motore con un accesso per squadra. Gli agenti leggono liberamente e scrivono solo attraverso il Cancello; per i clienti già attivi si aggiunge l'operazione che crea una trattativa. Invii in blocco, lanci e cancellazioni non esistono: restano a una persona ([proposta §7.3 e appendice A, voce B2](../PRESENTAZIONE-CEO.md)).
- La bacheca con il freno, i gruppi degli agenti e lo stand-up ci sono già dalla milestone 2, con i gruppi visti nella Sala di controllo: in questa fase passano sul server e si collegano ai nove bot ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0030](adr/0030-bacheca-gruppi-specchi.md)). La proposta li metteva all'inizio di questa fase ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md)).
- La richiesta a Meta per WhatsApp ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Lo stop di emergenza ferma anche gli invii di SersanOutreach: il kill switch, cioè l'interruttore che blocca tutti gli invii, e la pausa delle campagne di Instantly, il servizio delle sequenze email ([proposta §4.1 e §4.8](../PRESENTAZIONE-CEO.md)). Porta anche a zero i budget di LiteLLM, annulla carte e finestre aperte e non fa partire nessun lavoro della corsia T ([ricerca/45 §2.7](../ricerca/45-architettura-v3.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- I servizi nuovi (le macchine di motore, Cancello e server MCP, e MariaDB se vince BookStack) entrano sul server in questa fase, sul posto per gli agenti oppure dopo F3, e vanno nell'inventario, ciascuno con un responsabile delle patch ([ricerca/36 §4.5](../ricerca/36-architettura-v2.md)). Il Cancello può stare sulla stessa macchina virtuale del motore: decide Michele ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- 11 agenti nuovi: Dettatura (Chiamate); Capo di gabinetto, Banca dei token, Registro e audit, Guardiano (Direzione); Agente task (Progetti); Editoriale, Ricerca concorrenza, Analista metriche, Pubblicatore (Marketing); Copywriter (Studio contenuti). Il Post-call aggiunge CRM e to-do in Jira ([proposta §4](../PRESENTAZIONE-CEO.md)). Il Capo di gabinetto gira nella corsia S ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md)).
- Brief e bozza d'offerta entrano in questa fase se c'è capacità: l'Agente brief e l'Agente proposte girano nella corsia S, che c'è già dalla milestone 2 ([ricerca/45 §3.2 e §4.1](../ricerca/45-architettura-v3.md)). Nella proposta arrivavano nella fase 3 ([proposta §4](../PRESENTAZIONE-CEO.md)).
- Nel frattempo il board, nella fase F2, sposta SersanOutreach da Azure al server; la macchina Azure si spegne solo dopo una settimana di funzionamento stabile ([proposta §7.2](../PRESENTAZIONE-CEO.md)).

**Livelli di partenza** ([ricerca/45 §4.1](../ricerca/45-architettura-v3.md)):
- riassunto, debrief, to-do in Jira, meeting e trattative nel CRM (con l'MCP su HTTP, 3,5 giorni di sviluppo) ed evento in calendario: L3;
- follow-up alla persona appena incontrata: L2, poi L3 dopo 15 finestre pulite;
- brief la sera prima di ogni incontro con esterni: L3 leggero (web, CRM, calendario), se la capacità regge;
- bozza d'offerta: L3, se il catalogo è nella casa dei testi; invio dell'offerta L1, per scelta;
- slide per noi L3; slide al cliente L1;
- marketing (ricerca, temi, bozze, numeri del lunedì): L3; post della pagina aziendale L1, poi L2 con Metricool o Postiz; post dei founder L1, programmati dal Cancello;
- smistamento della posta: L3; risposte ai contatti in conversazione L1, poi L2; risposte ai destinatari nuovi L1;
- passaggi fra agenti: L3 dentro il freno; chiusura dei to-do delle persone L2 a 24 ore; inviti a una seconda call L1, poi L2;
- skill interne con valutazione: L2 a 48 ore.

**Cosa si vede alla fine**: CRM e to-do in Jira dopo ogni call. Gli agenti del marketing si passano il lavoro nei gruppi, con il freno in azione. Organigramma con 14 agenti e i loro costi. Banca dei token in LiteLLM, cioè i budget di spesa per agente e per catena di lavoro; quelli per persona arrivano nella fase 4. Poi la verifica della settimana 21 (sezione 4) ([proposta §4.8 e §11](../PRESENTAZIONE-CEO.md)).

### Fase 3 · Memoria, call, vendite preparate e canali (settimane 22-35)

**Prima di partire** ([ricerca/45 §11](../ricerca/45-architettura-v3.md)):
- altri 192 GB di RAM, perché con memoria e call il margine arriva a circa zero ([proposta §6.3](../PRESENTAZIONE-CEO.md)); prima, se il margine misurato con 6 sessioni S scende sotto i 5 GB ([ADR-0015](adr/0015-ram-384-gb.md));
- la linea internet di riserva 4G/5G, prima del primo lavoro L3 verso l'esterno fuori orario e prima di Andrea: in pratica qui, non prima della fase 5 come nella proposta ([ADR-0019](adr/0019-linea-di-riserva.md));
- la seconda GPU: la proposta la consigliava da qui ([proposta §6.4](../PRESENTAZIONE-CEO.md)); oggi è proposta a Michele per la milestone 2 ([ADR-0014](adr/0014-seconda-gpu-blackwell.md)).

**Cosa si fa**

- La ricerca nella memoria con i permessi di ciascuno, anche da Claude Team: chi chiede vede solo ciò che può vedere. La memoria che collega i momenti (trascrizioni, mail, documenti) è Qdrant, un database che cerca i testi anche per significato; gli embedding, cioè i testi tradotti in numeri per poterli cercare così, si calcolano sulla nostra GPU ([proposta §5.3, §5.5 e §11](../PRESENTAZIONE-CEO.md)).
- Il bot nelle call dei clienti: Vexa, sul nostro server, entra nelle call di Teams di altri, Meet e Zoom, dichiarandolo, e la trascrizione si fa in casa. Per le riunioni dal vivo la registrazione dal telefono e un vivavoce da sala ([proposta §4.2, §11, §14 decisione 14 e appendice A, voce J5](../PRESENTAZIONE-CEO.md)).
- Il Cancello versione 2 ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Telegram per gli avvisi, WhatsApp e Slack soprattutto per i clienti: stessi agenti, stesso codice. WhatsApp solo con l'API ufficiale di Meta e un numero dedicato, sempre dal Cancello. Su questi canali passano solo dati verdi, e le approvazioni restano in Teams ([proposta §2.1 e §4.11](../PRESENTAZIONE-CEO.md)).
- 18 agenti nuovi: Agente email, Agente LinkedIn, Sentinella segnali, Operatore outbound (Outbound); Agente chiamate, Agente agenda (Chiamate); Agente brief, Agente proposte, Analista vinto/perso, Agente intake (Vendite); Agente slide (Studio contenuti); Raccoglitore, Pulitore, Bibliotecario, Archivista, Sistemista (Memoria); Smistatore posta (Direzione); Agente bandi e finanziamenti (Amministrazione) ([proposta §4](../PRESENTAZIONE-CEO.md)). Agente brief e Agente proposte possono essere già al lavoro dalla fase 2. Il Sistemista è uno dei quattro agenti che possono usare la corsia T, per le pull request di aggiornamento ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- Su LinkedIn ogni messaggio passa dall'approvazione di una persona: gli agenti non usano l'autopilot dei messaggi, che scrive e approva da solo inviti e messaggi, né l'automazione del browser lato server ([proposta §7.1 e §7.4](../PRESENTAZIONE-CEO.md)).

**Livelli di partenza** ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)):
- Vexa nelle call di altri: L3, con l'avviso dichiarato; riunioni dal vivo L0, perché la registrazione la avvia la persona con il permesso dei presenti;
- domande alla memoria su una call a cui non eravamo: le fa la persona (L0), la risposta interna è L3, con il vincolo dei dati rossi verso Claude Team; raccolta, pulizia e indicizzazione L3;
- canale «Call di vendita» e analisi vinto/perso: L3 interno; il cambio delle campagne lo decide il marketing;
- sequenze email a freddo: L1 per contatto, oppure una carta per campagna dopo il parere; Agente LinkedIn sempre L1;
- Telegram, Slack, WhatsApp e messaggi nel canale condiviso con il cliente: al livello della classe del destinatario, fino a L2-L3;
- bandi ogni mattina: L3 interno; la domanda di bando la fa una persona (L0);
- Sistemista: sola lettura L3; patch L1;
- Andrea si può anticipare a questa fase solo con lead vere (vedi la fase 5).

**Cosa si vede alla fine**: brief, cioè la scheda che prepara l'incontro, pronto la sera prima di ogni incontro. Offerta in bozza entro un'ora. "Cosa ci siamo detti con X?" da Claude Team. Bandi ogni mattina. Posta smistata. Gli stessi agenti su Telegram, Slack e WhatsApp. 32 agenti al lavoro ([proposta §11](../PRESENTAZIONE-CEO.md)).

### Fase 4 · Organizzazione, newsletter e Buzz (settimane 36-40)

**Cosa si fa**

- Newsletter e programmazione dei post sul nostro server: listmonk per la newsletter, con l'invio attraverso un servizio di posta esterno, e Postiz per i post, al posto di Metricool, il servizio a pagamento che si usa finché Postiz non è pronto ([proposta §8.2, §11 e §14, decisioni 9 e 15](../PRESENTAZIONE-CEO.md)). Nessuno dei due è esposto su internet: si raggiungono solo da NetBird, la rete privata con cui si entra da fuori con identità verificata ([ricerca/36 §4.5](../ricerca/36-architettura-v2.md); [proposta §6.1](../PRESENTAZIONE-CEO.md)). Postiz può entrare prima di F4 solo con il sì di Michele; fino ad allora i post della pagina aziendale li programma l'esecutore Metricool del Cancello ([ADR-0013](adr/0013-postiz-listmonk-docuseal.md)).
- La banca dei token per persona ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Le skill proposte dagli agenti: le scrivono in una cartella "proposte", un revisore le controlla ogni settimana e una persona le approva con una pull request ([proposta §11 e appendice A, voce A6](../PRESENTAZIONE-CEO.md)).
- Buzz: la proposta lo metteva qui, sul banco di prova del laboratorio ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md)). La v3 lo anticipava alla milestone 2, sulla stessa bacheca ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). Dal 12 novembre lo specchio verso Buzz si costruisce e si prova quando Michele lo ammette e c'è una macchina Linux con Docker; fino ad allora i gruppi degli agenti si vedono nella Sala di controllo. Se Buzz non perde risposte e ha le approvazioni collegate, i gruppi passano lì; se no restano nella Sala, o in Teams quando c'è il bot, e Buzz resta in prova ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md)).
- 10 agenti nuovi: Agente newsletter, Community manager (Marketing); Agente video, Agente grafiche (Studio contenuti); Project manager, Report cliente, Onboarding cliente, Sviluppatori (Progetti); Mappatore processi, Intervistatore (Direzione) ([proposta §4](../PRESENTAZIONE-CEO.md)). Gli Sviluppatori sono uno dei quattro agenti della corsia T: lo sviluppo di progetti in codice va lì, sui posti delle persone di Progetti, con la consegna come pull request ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §9](../ricerca/49-instradamento-a-piu-motori.md)).

**Livelli di partenza** ([ricerca/45 §2.6 e §4.2](../ricerca/45-architettura-v3.md)):
- newsletter: L2 dopo 3 numeri puliti, con una finestra di 48 ore e un invio di prova alla persona;
- commenti sulla pagina aziendale: L2 per le risposte standard; commenti sui profili dei founder L0;
- lettura dei metadati di M365: L3 interno, solo dati aggregati e al massimo 21 giorni, con l'accordo di ciascuno; intervista guidata L3 interno;
- mappa dei processi e automazioni consigliate: L3 interno; la scelta di cosa costruire la fa una persona (L0);
- lavori di sviluppo in corsia T: la pull request è la proposta, unirla in `main` è una carta L1.

**Cosa si vede alla fine**: prima newsletter dopo il sì. Risposte sulla pagina aziendale in finestra. Mappa dei processi. Buzz come casa degli agenti, se ha superato la prova. 42 agenti ([proposta §11](../PRESENTAZIONE-CEO.md); [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)).

### Fase 5 · Vendite e voce (settimane 41-48)

Parte solo con il parere legale e con lead reali ([proposta §11](../PRESENTAZIONE-CEO.md)). Con lead vere Andrea si può anticipare alla fase 3 ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)).

**Prima di partire**: la seconda GPU, al più tardi all'inizio della fase, prima di spostare Andrea sulla GPU ([proposta §6.4](../PRESENTAZIONE-CEO.md)); oggi è proposta per la milestone 2 ([ADR-0014](adr/0014-seconda-gpu-blackwell.md)). La linea internet di riserva, che la proposta consigliava prima di questa fase ([proposta §14, decisione 13](../PRESENTAZIONE-CEO.md)), oggi arriva all'inizio della fase 3 ([ADR-0019](adr/0019-linea-di-riserva.md)). Il consenso alla richiamata in ogni modulo: sito, campagne, eventi ([proposta, appendice A, voce G5](../PRESENTAZIONE-CEO.md)).

**Cosa si fa**

- "Andrea" con il centralino Asterisk e una linea telefonica italiana, prima sulla CPU e poi sulla seconda GPU. Pipecat regge la conversazione al telefono; Claude Haiku, il modello più leggero di Claude, ragiona; ascolto e voce girano in casa ([proposta §5.1, §11 e appendice A, voce G5](../PRESENTAZIONE-CEO.md)). La richiesta di richiamata arriva dal modulo del sito come evento su `POST /eventi`; la proposta la faceva passare da n8n ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md); [proposta, appendice A, voce G5](../PRESENTAZIONE-CEO.md)). Andrea si dichiara AI dalla prima frase e richiama da solo soltanto chi lo ha chiesto nel modulo ([proposta §1 e §9.1](../PRESENTAZIONE-CEO.md)).
- Andrea parte con una voce sintetica. La versione con la voce clonata di un collega arriva dopo, sempre nella fase 5, solo con il suo contratto separato e revocabile e il via del parere legale ([proposta §14 decisione 10 e appendice A, lacune dichiarate](../PRESENTAZIONE-CEO.md)).
- La pipeline pesata e il portale clienti costruito sopra SersanOutreach. Finché le chiusure non sono 30-50, la pipeline usa pesi dichiarati da Alessandro ([proposta §4.3 e appendice A, voce D1 e lacune dichiarate](../PRESENTAZIONE-CEO.md)). Il lavoro di codice sul portale può andare in corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- 4 agenti nuovi: "Andrea", Coach vendite, Pipeline (Vendite) e Agente clienti simili (Outbound) ([proposta §4](../PRESENTAZIONE-CEO.md)).

**Livelli di partenza** ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)):
- richiamata di Andrea: L3 solo dopo il parere, il consenso registrato e 50 chiamate di prova; fra le 20:00 e le 8:00 e nel fine settimana parte qualcosa verso l'esterno solo con Andrea ([ricerca/45 §2.6](../ricerca/45-architettura-v3.md));
- aperture di Andrea: L2, poi L3 dentro una banca di frasi approvate;
- coaching al venditore: L3; al responsabile L3 con soli dati aggregati, il report individuale solo con il parere;
- pipeline pesata e fit score del prospect: L3 interno.

**Cosa si vede alla fine**: una lead di prova viene richiamata entro 90 secondi e l'appuntamento è nel CRM. Chiamate in entrata con l'esito nel canale vendite. Coaching, cioè i consigli dopo ogni call di vendita, visibile solo a chi ha fatto la call. 46 agenti ([proposta §4.3 e §11](../PRESENTAZIONE-CEO.md)).

### Fase 6 · Le altre automazioni (settimane 49-53)

**Cosa si fa**

- Firma elettronica e fatturazione sul nostro server: DocuSeal per la firma; per le fatture lo strumento che usiamo già, se fa al caso, altrimenti uno sul nostro server ([proposta §11, §14 decisione 22 e appendice A, voci L1 e L2](../PRESENTAZIONE-CEO.md)).
- L'assistente personale per chi lo vuole: i dati di salute restano nell'account privato di chi lo sceglie e non entrano mai nella memoria aziendale ([proposta §4.8](../PRESENTAZIONE-CEO.md)).
- La prova di Paperclip, un piano di controllo open source fatto apposta per "aziende di agenti", in laboratorio e senza dati dei clienti, per circa 2 giorni di sviluppo ([proposta §4.12 e §11](../PRESENTAZIONE-CEO.md); [ricerca/45 §3.1](../ricerca/45-architettura-v3.md)).
- 11 agenti nuovi: Agente contratti (Vendite); Agente sito e SEO, Agente eventi e webinar (Marketing); Assistenza clienti, Agente rinnovi, Agente casi studio (Progetti); Allenatore AI, Assistente personale (Direzione); Agente fatture e incassi, Agente acquisti e abbonamenti, Controllo di gestione (Amministrazione) ([proposta §4](../PRESENTAZIONE-CEO.md)). L'Agente sito e SEO è il quarto agente della corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

**Livelli di partenza** ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)):
- contratto dall'offerta approvata, con DocuSeal: L1 (classe «Impegni»); fattura L1; sollecito L2 a 24 ore, al cliente con un progetto attivo;
- margini, cassa e distanza dagli obiettivi: L3 interno;
- assistenza ai clienti nella loro stanza: risposte standard L1, poi L2;
- rinnovi e clienti a rischio: L3 interno; caso studio L3 interno; richiesta di testimonianza L1;
- sito, articoli e SEO: pull request L1; il deploy lo fa una persona (L0);
- inviti a webinar ed eventi: L2, come la newsletter;
- acquisti: L3 interno fino alla preparazione; il pagamento è L0;
- assistente personale: L3 sulle azioni private della persona, L1 verso terzi; Allenatore AI L3, visibile solo all'interessato.

**Cosa si vede alla fine**: dal contratto all'incasso senza lavoro a mano. Ogni progetto chiuso diventa un caso studio. Tutti i 57 agenti nel registro ([proposta §11](../PRESENTAZIONE-CEO.md)).

## 4. Le verifiche delle settimane 8 e 21

### 4.1 Settimana 8: il pilota regge?

Nella proposta, alla settimana 8 i CEO decidevano se finanziare la fase 2; se ci si fermava, restavano Claude Team usato bene da tutti, SersanOutreach sistemato, la decisione sull'email e il calendario dei post ([proposta §1](../PRESENTAZIONE-CEO.md)). Dal 10 novembre il progetto è approvato e le scelte le prende il gruppo di progetto ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)): la verifica resta, ed è la milestone 7 del PRD, il collaudo. La verifica ha due gruppi di criteri ([proposta §11](../PRESENTAZIONE-CEO.md)); i dettagli su come si misurano vengono da [ricerca/36 §7.4](../ricerca/36-architettura-v2.md) e i cambi della v3 da [ricerca/45 §6.2-§6.4](../ricerca/45-architettura-v3.md).

**Criteri tecnici**, sul banco di prova:

1. **Nessun effetto esce fuori dal suo livello**: L1 solo dopo il sì, L2 solo a finestra scaduta senza «Ferma», L3 solo entro i tetti. Vale anche nei dieci scenari di prova, tra cui il Cancello che non risponde in tempo, la carta scaduta e il testo cambiato dopo la carta. Nella proposta il criterio era «nessun effetto senza una carta» ([ricerca/45 §6.4](../ricerca/45-architettura-v3.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)).
2. Una carta o una finestra lasciata ferma la notte riprende il lavoro con l'esito giusto al mattino; un crash a metà catena non perde la call e non manda due mail ([ricerca/45 §6.2, AC-018, e §6.3, N9](../ricerca/45-architettura-v3.md)).
3. L'approvazione e il «Ferma» arrivano dal telefono con l'identità giusta, dalla carta in Teams o dalla pagina del Cancello ([ricerca/45 §6.4](../ricerca/45-architettura-v3.md)).
4. La spesa resta nel tetto. Il confronto fra la stima di spesa dell'Agent SDK e la Console, il pannello di Anthropic dove si vede la spesa delle API, passa alla milestone della corsia S, perché il pilota non usa l'SDK ([ricerca/45 §6.2, AC-024](../ricerca/45-architettura-v3.md)).
5. Sul banco di prova non resta salvato nessun dato rosso.
6. I criteri della milestone 1, fra cui N1-N9 (finestra L2, L3 entro i tetti, destinatari dai dati, controllo del contenuto, promozione e discesa, «Annulla» e «Rettifica», riga AI, soppressione, crash), passano con un comando, gratis ([ricerca/45 §6.3 e §6.4](../ricerca/45-architettura-v3.md)).

Due criteri della proposta cambiano posto: «tre agenti lavorano una settimana senza scambiarsi le sessioni» e «un aggiornamento dell'Agent SDK passa i dieci scenari ed è in uso entro 14 giorni» passano alla milestone della corsia S, perché il pilota gira nella corsia N e la corsia S ha un solo runner ([ADR-0012](adr/0012-hermes-uscita.md); [ricerca/45 §6.2](../ricerca/45-architettura-v3.md)).

**Le misure d'autonomia**, nuove ([ricerca/45 §6.4](../ricerca/45-architettura-v3.md)):

- i minuti fra la fine della call e il follow-up;
- la quota di azioni partite a L2 o L3;
- i «Ferma» ogni 100 finestre.

Le promesse sicure della settimana 8 sono tre: l'ingresso nelle call Teams nostre, il riassunto L3 con il registro e il debrief L3. To-do in Jira ed evento in calendario dipendono dal margine di capacità ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)).

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

1. gli stessi criteri tecnici della settimana 8, sul server, con i budget di LiteLLM al posto del tetto della Console ([ricerca/36 §7.5](../ricerca/36-architettura-v2.md)), e le misure d'autonomia della sezione 4.1;
2. nessuna risposta del lavoro di una persona finita in un canale aperto a tutti;
3. tutti i servizi nuovi in inventario, con le patch entro 14 giorni;
4. il backup 3-2-1 in funzione, cioè tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio, con una prova di ripristino riuscita ([proposta §6.1](../PRESENTAZIONE-CEO.md));
5. la RAM misurata e la decisione d'acquisto presa.

**La revisione esterna esce dalla verifica.** La proposta chiedeva la revisione esterna di Cancello, motore e bot, con i rilievi gravi chiusi ([proposta §11](../PRESENTAZIONE-CEO.md)). Oggi è facoltativa: si fa se un cliente la chiede. Restano le prove a ogni modifica, che sono l'unica revisione obbligatoria, e la revisione di Mattia sul codice ([ADR-0023](adr/0023-protezioni-essenziali.md)). Con il backup in funzione i dati dei clienti stanno sul server dopo la settimana 21 senza la revisione esterna come condizione ([ricerca/45 §11](../ricerca/45-architettura-v3.md)).

Fino a questa verifica nessun dato dei clienti resta sul server ([proposta §13](../PRESENTAZIONE-CEO.md)).

### 4.3 Se una verifica non passa

- **Fallisce un criterio tecnico**: due settimane per correggere. Se il problema è di struttura, la proposta prevedeva di provare Hermes Agent sullo stesso banco di prova, con gli stessi scenari, e decidere sui numeri ([proposta §11](../PRESENTAZIONE-CEO.md)). Hermes è un orchestratore open source, cioè un programma già pronto che coordina gli agenti, e lo abbiamo confrontato con il motore prima di scegliere ([proposta §5.7](../PRESENTAZIONE-CEO.md)). Oggi Hermes resta una via d'uscita già prezzata e un pilota in laboratorio da 6-8 giorni di sviluppo, fuori dal percorso dei clienti. Le sue quattro condizioni non sono soddisfatte al 9 novembre ([ADR-0012](adr/0012-hermes-uscita.md)). Dentro la v3 c'è già un'uscita più vicina: se la corsia T non va, il lavoro ripiega sulla corsia S senza cambiare le catene ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). I giorni di queste uscite sono nella sezione 5.
- **Falliscono i criteri commerciali**: vale "prima il funnel" (sezione 1): le fasi 2 e 3 vanno avanti, la fase 5 aspetta ([proposta §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §7.4](../ricerca/36-architettura-v2.md)).
- **Il parere dice no** su follow-up e recap a L2: restano a L1, e resta il tempo risparmiato sulle bozze ([ricerca/45 §10](../ricerca/45-architettura-v3.md)).
- **Una prova della milestone 2 non passa** (sezione 4.4): il modello locale non entra per quel compito e l'agente resta su Claude; per il decisore, la domanda passa alle regole o a una carta ([ADR-0025](adr/0025-un-modello-per-agente.md); [ADR-0027](adr/0027-decisore.md)).

### 4.4 Le prove dei modelli, del decisore e della corsia T

Queste prove scelgono i modelli e le soglie. Le misure si fissano prima della prova.

**La prova dei modelli locali**, nella milestone 2, con il primo modello open-weight. Ogni risposta di un modello locale si confronta con Haiku 5.5 o Sonnet 5.5 sugli stessi casi verdi ([ricerca/48 §6.2](../ricerca/48-modelli-locali-e-gpu.md); [ADR-0025](adr/0025-un-modello-per-agente.md)):

| Prova | Cosa si misura | Soglia per passare |
|---|---|---|
| Trascrizione, su 10-20 call vere con consenso | errore sulle parole, tempo per ora di audio, memoria della GPU | da fissare con Alessandro [proposta] |
| Chi parla, su 5 riunioni dal vivo | errore nel riconoscere chi parla | da fissare con Alessandro [proposta] |
| Corsia N a schema, su 50 trascrizioni e 50 mail | moduli validi; campi giusti contro una persona; riassunti votati alla cieca contro Haiku 5.5 | per esempio il 90% dei campi giusti [proposta] |
| Lettura documenti, su 30 fatture e 20 documenti dei clienti | campi giusti (importo, data, partita IVA), tabelle | come sopra |
| Revisione visiva, su 20 slide e 10 grafiche con difetti inseriti apposta | difetti trovati, falsi allarmi | almeno quanto una persona sui difetti evidenti [proposta] |
| Strumenti in catena (esperimento), su 10 compiti della corsia S | compiti finiti senza errori, velocità | nessuna: decide solo se riparlarne |
| Velocità e memoria | prove di velocità e memoria con 4 utenti | sostituisce le stime |

Alcuni modelli da provare girano solo sulla seconda GPU: per questo si propone di comprarla per questa milestone ([ricerca/48 §6.2](../ricerca/48-modelli-locali-e-gpu.md); [ADR-0014](adr/0014-seconda-gpu-blackwell.md)).

**La prova del decisore**, nella milestone 2. ADR-0027 la prevedeva su circa 850 casi verdi in italiano, fra Haiku 5.5, Jev fissato e chiamato via LiteLLM, un modello piccolo sulla CPU e, se c'è la GPU, un modello da 4-9 miliardi di parametri, con dopo due settimane di prova ombra, in cui il decisore risponde accanto alla catena senza avere effetto ([ADR-0027](adr/0027-decisore.md)). Dal 12 novembre nella milestone 2 si tarano solo il controllo del contenuto e la lettura delle risposte degli esterni. I testi dei casi si possono generare con un modello; le etichette le mettono due persone, e lo strumento di taratura si scrive dopo i primi 100 casi. La prova confronta un decisore in casa, che legge la probabilità della prima parola, un modello piccolo sulla CPU e Haiku 5.5 quando c'è la chiave API. Jev entra nella milestone 3, con LiteLLM. La prova ombra si sposta a quando ci sono eventi veri, nelle milestone 5 e 6 ([ADR-0027, revisione del 12 novembre 2026](adr/0027-decisore.md); [ricerca/51](../ricerca/51-modelli-open-weight-sul-computer-di-sviluppo.md)). Le soglie scritte in ADR-0027 sono:

- trova almeno il 98% dei casi delle classi critiche («non scrivetemi», impegni, dati rossi);
- manda a una strada più economica al massimo il 2% dei casi difficili;
- non sta sotto Haiku 5.5 di più di 2 punti di accuratezza;
- ha un errore di calibrazione di 0,10 al massimo, cioè le sue probabilità dicono il vero: fra le risposte date con 0,8, circa 8 su 10 sono giuste;
- decide da solo almeno il 70% dei casi, con un errore reale del 2% al massimo;
- risponde entro 500 ms via API ed entro 200 ms in casa, 95 volte su 100.

Dall'11 novembre per Jev l'italiano non è un freno: i primi due criteri diventano l'obiettivo delle soglie, domanda per domanda, e gli altri si misurano e si registrano. Se per una domanda nessuna soglia li raggiunge, quella domanda la decidono le regole o una carta, e Jev resta per le altre ([ADR-0027, revisione dell'11 novembre](adr/0027-decisore.md); [ricerca/49 §1.4](../ricerca/49-instradamento-a-piu-motori.md)).

**Il router e la prova della corsia T**, nella milestone 2 dal 12 novembre; prima stavano con le prove di LiteLLM della milestone 3. Il router gira sul decisore che c'è, e la corsia T è una destinazione di prova che registra «partirebbe». La prova dal vivo della corsia T la fa Alberto dal suo account, passo per passo, su una repo di prova con dati verdi: passa se l'avvio parte e consegna una pull request in bozza. Solo dopo si scrive l'adattatore che avvia davvero la corsia T. Criteri nuovi: R1 un dubbio non porta mai in T; R2 un dato rosso o di colore ignoto non arriva mai a T; R3 un avvio T perso non si ripete da solo; R4 con lo stop attivo nessun avvio T parte ([ricerca/49 §7 e §8](../ricerca/49-instradamento-a-piu-motori.md); [ADR-0028, revisione del 12 novembre 2026](adr/0028-instradamento-a-piu-motori.md)).

**Con le prove di LiteLLM e Teams** (milestone 3):
- **la prova della casa dei testi** con i CEO: ognuno cambia tre cose della sua pagina «Come lavoro» chiedendolo all'agente in Teams. Se non ce la fa da solo, resta BookStack ([ricerca/46 §7 e §9](../ricerca/46-obsidian-come-casa-dei-testi.md)).

## 5. La stima dei giorni di sviluppo

È l'unica stima dei giorni di lavoro di questo file. La stima per fase viene da [proposta §15](../PRESENTAZIONE-CEO.md); quella della v3 da [ricerca/45 §9.3](../ricerca/45-architettura-v3.md).

**Come si legge**

- I giorni sommano il lavoro di tutte le persone che sviluppano, in parallelo: per questo in una fase possono essere più dei giorni di calendario ([proposta §15](../PRESENTAZIONE-CEO.md)).
- Il valore più basso è la stima di base; il più alto comprende una riserva di circa un terzo ([proposta §15](../PRESENTAZIONE-CEO.md)).
- L'infrastruttura del board di Michele non è contata: la porta avanti lui ([proposta §15](../PRESENTAZIONE-CEO.md)). Non sono contate nemmeno la migrazione di SersanOutreach e le parti della fase F4 che il board fa già, come la base della ricerca nella memoria e la pipeline dei documenti: contiamo solo le nostre estensioni ([ricerca/36 §7.6](../ricerca/36-architettura-v2.md)).
- Sono contati l'installazione e l'esercizio dei servizi nuovi ([proposta §13](../PRESENTAZIONE-CEO.md)) e il contenuto di ogni agente: istruzioni, skill, schemi e prove ([ricerca/34-proposta-1 §4.3](../ricerca/34-proposta-1-agent-sdk.md)).
- "Esercizio e patch" sono i giorni per tenere in funzione e aggiornati i servizi nuovi (aggiornamenti, patch, scansioni), contati a parte: circa mezza giornata a settimana nelle fasi 2-4 e circa una nelle fasi 5-6, perché i servizi da seguire crescono ([ricerca/36 §4.5 e §7.6](../ricerca/36-architettura-v2.md)).

**La stima della proposta, fase per fase.** La v3 non ha ristimato le fasi dalla 2 alla 6: per loro questa resta la stima di riferimento.

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

**La stima della v3.** Le cifre nuove sono [stima] di [ricerca/45 §9.3](../ricerca/45-architettura-v3.md):

| Periodo | Base | Con la riserva | Proposta (base / con riserva) |
|---|---|---|---|
| Fase 1 | circa 20-23 | circa 27-31 | 22,5 / 30 |
| Fasi 0-1 | circa 38-41 | circa 45-55 | 40,5 / 54 |
| Totale del piano | circa 247-250 | circa 329-333 | 249 / 332 |

Per la fase 1 la v3 parte dai 22,5 giorni di base della proposta, toglie la parte S del motore sul banco (circa 5) e le difese oltre l'essenziale (3,5), aggiunge livelli, finestra, promozioni, «Annulla» e controllo del contenuto (da 4 a 6) e il registro degli eventi (1). Con la riserva, nel caso peggiore, supera di circa 1 giorno il tetto della proposta per le fasi 0-1: 55 contro 54 ([ricerca/45 §9.3](../ricerca/45-architettura-v3.md)).

**Note**

- **La milestone 1 è cresciuta, e la stima va rifatta.** [ricerca/45 §12.1](../ricerca/45-architettura-v3.md) stimava la milestone 1 in circa 8-10 giorni [stima]. Il suo piano aveva 14 gruppi e 70 compiti, e la milestone è finita il 12 novembre 2026; comprendeva il decisore, il registro dei modelli e i testi letti da file, che quella stima non prevedeva ([ADR-0027](adr/0027-decisore.md)). Per il solo registro dei modelli [ricerca/48 §6.1](../ricerca/48-modelli-locali-e-gpu.md) stima circa 1-1,5 giorni [stima]; per il decisore e i testi da file non c'è una stima. Le stime dei giorni si fanno con Mattia quando serve una data, e non fermano il piano; qui non si scrive una cifra nuova ([ricerca/45 §9.3](../ricerca/45-architettura-v3.md)). Con la nuova stima va ricontrollata anche la data del collaudo della settimana 8.
- **Lavoro spostato prima, non tolto.** Corsia S, bacheca e gruppi (circa 5,5 giorni per bacheca e canale) e la prova di Buzz (circa 6 giorni) passano dalla fase 2 e dalla fase 4 alla milestone 2 ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ricerca/45 §3.1](../ricerca/45-architettura-v3.md)). Dal 12 novembre lo specchio verso Buzz si costruisce solo con il sì di Michele e una macchina Linux con Docker ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md)). Il vantaggio della v3 sta nell'ordine dei lavori, non nel totale ([ricerca/45 §9.3](../ricerca/45-architettura-v3.md)).
- **Lavoro nuovo, fuori dalle cifre di ricerca/45.** Router, adattatore della corsia T, lettore di GitHub e conto per posto: circa 4-6 giorni [stima di ricerca/49 §8]; la corsia T sui progetti veri: circa 3-4 giorni [stima di ricerca/49 §8] ([ricerca/49 §8](../ricerca/49-instradamento-a-piu-motori.md)).
- **Calendario e capacità.** Le settimane della proposta sono calcolate sui giorni con la riserva più l'esercizio, con una capacità di circa 6,5 giorni di sviluppo a settimana per tutto il gruppo fino alla fase 3 e circa 7,5 dalla fase 4, da confermare. La capacità delle fasi 0-1 è di circa 52 giorni; se si consuma tutta la riserva, le fasi 0 e 1 finiscono a metà della settimana 9, e con la v3 resta vero ([ricerca/36 §7.1 e §7.2](../ricerca/36-architettura-v2.md); [ricerca/45 §9.3](../ricerca/45-architettura-v3.md)). La settimana 8 può slittare alla 9 o alla 10: per questo to-do in Jira ed evento in calendario entrano nel pilota solo se c'è margine ([ricerca/45 §10](../ricerca/45-architettura-v3.md)).
- **Con più capacità di sviluppo** dalla fase 2 il calendario scende da circa 53 a circa 42 settimane ([proposta §15](../PRESENTAZIONE-CEO.md)); il conto usa circa 9 giorni di sviluppo a settimana. Se Michele anticipa il posto per gli agenti, il passaggio sul server arriva qualche settimana prima, ma i giorni restano gli stessi ([ricerca/36 §7.7](../ricerca/36-architettura-v2.md)).
- **Perché il totale della proposta cresce rispetto alla prima versione** (110-147 giorni per le fasi 0-5): tutto è sul nostro server e nessuna funzione è tolta. Chat, bot nelle call, voce di Andrea, newsletter, programmazione dei post, firma elettronica e fatturazione li costruiamo e li gestiamo in casa invece di pagarli in abbonamento, e i giorni per le patch e l'esercizio sono contati ([proposta §15](../PRESENTAZIONE-CEO.md)).
- **I piloti in laboratorio**: Hermes 6-8 giorni, Buzz 6, Paperclip 2, senza costi in euro ([ricerca/45 §9.1](../ricerca/45-architettura-v3.md)).
- **Se il motore non reggesse** alle verifiche, una prova di Hermes sullo stesso banco costa 6-8 giorni; usarlo al posto del motore costa 26-33 giorni con la riserva, mentre Cancello, memoria, bot e skill restano ([proposta §15](../PRESENTAZIONE-CEO.md)).
- **Dopo la fase 6** l'esercizio resta intorno a un giorno a settimana: aggiornamenti dell'Agent SDK, del Cancello e dei servizi, agenti nuovi ([proposta §15](../PRESENTAZIONE-CEO.md)).

## 6. I rischi principali e come li gestiamo

Sono i rischi della [proposta §13](../PRESENTAZIONE-CEO.md), divisi per tema, aggiornati con i rischi residui di [ricerca/45 §10](../ricerca/45-architettura-v3.md) e con le ADR.

### 6.1 Il codice che scriviamo

| Rischio | Come lo gestiamo |
|---|---|
| **Cancello, motore e bot sono codice scritto su misura** e nessuno lo ha ancora rivisto | Prove a ogni modifica, con un comando, gratis; idempotenza, cioè un passo ripetuto non fa un secondo effetto; esito «incerto» a una persona; Mattia sul codice dal primo giorno. La proposta chiedeva una revisione esterna entro la settimana 21: oggi è facoltativa, si fa se un cliente la chiede ([ADR-0023](adr/0023-protezioni-essenziali.md)) |
| **Una mail sbagliata arriva a un cliente senza che nessuno l'abbia letta**: a L2 e L3 nessuno legge prima | Indirizzo esatto, controllo del contenuto, riga AI, tetti giornalieri, discesa automatica, «Rettifica»; la classe torna a L1 con un tocco, a 0 € ([ricerca/45 §10](../ricerca/45-architettura-v3.md)) |
| **Una lamentela non viene riconosciuta** e la terna resta alta | Risposte dubbie in carta; «sbagliato» nel debrief; le classi si rivedono ogni mese nel resoconto ([ricerca/45 §10](../ricerca/45-architettura-v3.md)) |
| **Il decisore sbaglia** o una mail è scritta per ingannarlo | Non alza mai un livello e non sceglie destinatari; soglie alte e scritte in un file; un errore vale un dubbio; ogni domanda ha almeno due motori, e il ripiego sono le regole e una carta ([ADR-0027](adr/0027-decisore.md)) |
| **L'Agent SDK cambia quasi ogni giorno** | Versione fissata; aggiornamento ogni due settimane, dopo i dieci scenari, entro i 14 giorni. Tocca solo la corsia S: la corsia N non dipende da Claude Code ([ricerca/45 §10](../ricerca/45-architettura-v3.md)) |
| **Il motore non regge** | Verifiche alle settimane 8 e 21 e prove a ogni milestone; passare dalla corsia N alla S è una promozione nello stesso codice, non una riscrittura. Hermes resta un'uscita già prezzata e un pilota in laboratorio, fuori dal percorso dei clienti; le sue quattro condizioni non sono soddisfatte ([ADR-0012](adr/0012-hermes-uscita.md); [ADR-0021](adr/0021-motore-a-due-corsie.md)) |
| **La corsia T**: Anthropic legge l'uso dei posti in modo diverso dal nostro, la funzione è in anteprima, una sessione fa più del dovuto | Il motore non tocca mai il login dei posti; T solo per sviluppo e lavori lunghi, con un conto per posto; conferma scritta di Anthropic prima dei progetti veri; nessun connettore, rete limitata, `main` protetto, unione solo con revisione; adattatore separato e ripiego sulla corsia S ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)) |
| **LiteLLM custodisce tutte le chiavi**, e a marzo 2026 ne sono circolate versioni compromesse | Versione fissata e controllata; pannello raggiungibile solo dalla rete di gestione; chiave principale tra i segreti, con rotazione ([proposta §13](../PRESENTAZIONE-CEO.md)). La proposta lo faceva uscire solo verso Anthropic; oggi esce anche verso il nostro server e i fornitori scelti, che ricevono solo dati verdi e gialli ([ADR-0025](adr/0025-un-modello-per-agente.md)) |
| **La sveglia**: un orario perso o un evento fermo. La proposta usava n8n, che non recupera da solo un'esecuzione caduta | La sveglia sta nel motore: tabella degli orari in git, recupero dell'ultimo orario perso, controllo alle 7:15 se il debrief non è partito, registro degli eventi che rimette in coda ciò che resta fermo. n8n è facoltativo e, se c'è, non tiene dati rossi ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)) |
| **Il bot di Teams senza Azure** può dare errori di registrazione | Prova nella milestone 3; registrazione Azure Bot gratuita, senza macchine accese; in ultima istanza la pagina del Cancello, con gli avvisi in Teams; intanto la Sala di controllo ([proposta §13](../PRESENTAZIONE-CEO.md); [ricerca/45 §10](../ricerca/45-architettura-v3.md)) |
| **Iniezioni di prompt** da mail, trascrizioni e messaggi | Nella corsia N il testo di terzi entra solo come campi e il codice sceglie i destinatari; nessuno strumento invia senza il Cancello ([ADR-0021](adr/0021-motore-a-due-corsie.md)) |

### 6.2 Il server e la rete

| Rischio | Come lo gestiamo |
|---|---|
| **Il tempo di chi amministra il server**: il sistema aggiunge 11-13 servizi e 3 reti nuove al perimetro Cyber Essentials, con le patch entro 14 giorni | Prima della fase F4 entrano solo i servizi del pilota; ogni servizio ha un responsabile delle patch e un posto nell'inventario; installazione ed esercizio dei servizi nuovi sono nei giorni della sezione 5, mentre l'infrastruttura del board la porta avanti Michele e non è contata. Con la v3 il numero dei servizi non sale ([ricerca/45 §3.3](../ricerca/45-architettura-v3.md)) |
| **RAM finita** con tutte le funzioni | Misura con un tetto di sessioni; altri 192 GB all'inizio della fase 3, o prima se il margine misurato con 6 sessioni S scende sotto i 5 GB. La corsia S arriva subito dopo la milestone 1: il margine va misurato appena il runner gira sul server ([ADR-0015](adr/0015-ram-384-gb.md)) |
| **Una sola GPU fino all'arrivo della seconda**, prestata ogni tanto alla postazione di prova del laboratorio (Experimental-1); oggi ha meno di 1 GB libero | I lavori della GPU aspettano in coda finché torna libera; embedding e lavori a lotti, cioè fatti in blocco e non dal vivo, sulla CPU quando serve. La proposta consigliava la seconda GPU da 16 GB dalla fase 3; oggi è proposta a Michele per la milestone 2, perché serve alla prova dei modelli locali ([ADR-0014](adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md)) |
| **Una sola linea internet**: se cade la fibra, gli agenti si fermano, perché ragionano con Claude via internet, e Andrea non risponde. Con i livelli, follow-up e lavori a orario partono anche senza nessuno in ufficio | Nulla si perde: lavori, carte e finestre aspettano e ripartono quando la linea torna. La proposta metteva la linea di riserva 4G/5G prima della fase 5 (decisione 13); oggi va prima del primo lavoro L3 verso l'esterno fuori orario e prima di Andrea, in pratica all'inizio della fase 3. L'accesso da fuori passa dalla macchina Oracle, la piccola macchina in cloud a Milano, e funziona anche sulla linea di riserva ([ADR-0019](adr/0019-linea-di-riserva.md)) |
| **Mancanza di corrente**, con le batterie dell'UPS (il gruppo di continuità del rack) usate e senza garanzia | Dopo 3 minuti l'UPS spegne il server in modo pulito e tiene accesa la rete. Al ritorno della corrente la rete riparte da sola; per il server si chiede a Michele la riaccensione automatica, a 0 €, prima del primo lavoro L3 notturno sul banco: senza, il server va riacceso a distanza e il debrief salta. Test di autonomia e di riaccensione all'arrivo dell'UPS, e batterie nuove se servono ([proposta §13](../PRESENTAZIONE-CEO.md); [ricerca/45 §11](../ricerca/45-architettura-v3.md)) |
| **Backup non ancora completo**: la copia in sede va montata, quella a casa di Michele arriva a marzo 2027 | Nessun dato dei clienti resta sul server prima della verifica della settimana 21, che chiede il 3-2-1 con una prova di ripristino ([proposta §13](../PRESENTAZIONE-CEO.md)) |
| **Il firewall Sophos è un modello fuori supporto**: Sophos non lo aggiorna più, e BIOS (il programma di base della macchina) e processore non ricevono più correzioni | Il software che ci gira, Proxmox e OPNsense, è aggiornato. Per Cyber Essentials si chiede prima per iscritto all'ente di certificazione se accetta questa configurazione; se non la accetta, OPNsense passa su un piccolo computer ancora supportato dal produttore (spesa da preventivare) |
| **Fine del supporto HPE**, il produttore del server, per lo chassis, cioè il telaio del server: ottobre 2029 secondo le fonti HPE consultate da Michele, da confermare con il numero di serie; le stime pubbliche partono da marzo 2028 | Macchine virtuali con backup: si spostano su un server nuovo senza rifare nulla; Michele prevede il secondo server a dicembre |
| **Tempi del board** non ancora fissati | Sviluppo sulle macchine di sviluppo, poi banco di prova nel laboratorio; il posto per gli agenti sul server come richiesta a Michele |

### 6.3 Dati, regole e canali

| Rischio | Come lo gestiamo |
|---|---|
| **Dati personali verso Claude Team**, che non ha un registro di audit | Decisione nel parere e nella valutazione d'impatto entro la settimana 3; il rosso arriva a Claude Team solo oscurato, e alla corsia T mai ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)) |
| **Registrazioni, "Andrea", coaching, messaggi a L2** e norme sul lavoro | Parere legale: i punti del pilota entro la settimana 3, il resto prima della fase 2, con le due domande nuove su riga AI e messaggi L2; "Andrea" si dichiara sempre AI; coaching privato. Se il parere chiude una porta, la funzione resta a L1 ([ricerca/45 §2.8](../ricerca/45-architettura-v3.md)) |
| **"Andrea" e la regola del piano marketing** che vieta voci sintetiche nelle call | Un'eccezione che la proposta chiedeva ai CEO (decisione 10): solo richiamate chieste dalla lead, voce dichiarata, il brief resta letto da un founder. Oggi è accettata dal gruppo di progetto, e le chiamate vere aspettano il parere ([ADR-0008](adr/0008-andrea-centralino.md)) |
| **Piattaforme di call che bloccano i bot** non registrati | Per le nostre call la trascrizione nativa di Teams; registrazione sul PC come riserva |
| **La voce italiana di Andrea** non abbastanza buona | Prova d'ascolto prima; voci migliori sulla seconda GPU; in ultima istanza una voce in cloud, circa 88 € al mese, come eccezione che oggi decide il gruppo di progetto ([ricerca/45 §9.2](../ricerca/45-architettura-v3.md)) |
| **WhatsApp**: le soluzioni non ufficiali portano al blocco del numero | Solo l'API ufficiale di Meta, con un numero aziendale dedicato |
| **Buzz è giovane**: perde risposte e le approvazioni non sono collegate | Si prova quando Michele lo ammette e c'è una macchina Linux con Docker, con 200 messaggi in 5 giorni lavorativi, nessuno perso e nessuno doppio; diventa la casa degli agenti solo se non perde più risposte e ha approvazioni funzionanti; intanto i gruppi degli agenti si vedono nella Sala di controllo ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0030](adr/0030-bacheca-gruppi-specchi.md)) |
| **Dati di un cliente nel gruppo sbagliato** | Ogni gruppo per cliente vede solo i passaggi di quel cliente; un errore così è un incidente serio e riporta a L1 tutte le classi esterne dell'agente ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). Nella milestone 2 i gruppi si vedono solo nella Sala, e il gruppo per cliente controlla il cliente due volte sulla stessa riga; la rotta che dichiara l'incidente al Cancello arriva con gli specchi ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md)) |

### 6.4 Il progetto

| Rischio | Come lo gestiamo |
|---|---|
| **Il funnel è vuoto**: 11 lead, 0 meeting, campagna ferma dal 9 settembre. Con questi volumi L2 e L3 verso l'esterno arrivano tardi | Decisione sull'email e casella attiva nella fase 0; criteri commerciali alla settimana 8; follow-up a L2 per decisione del gruppo, invece di aspettare un contatore; "Andrea" solo con lead vere ([ricerca/45 §2.3 e §10](../ricerca/45-architettura-v3.md)) |
| **La milestone 1 è cresciuta**: decisore, registro dei modelli, testi da file, 70 compiti | La stima si rifà dopo i primi gruppi del piano; to-do in Jira ed evento in calendario solo se c'è margine (sezione 5) |
| **Calendario lungo**, circa un anno | Valore dalla prima settimana; con più capacità di sviluppo il calendario si accorcia (sezione 5) |
| **Troppi agenti per quattro persone** | Ogni agente ha un responsabile, un tetto e una riga nel registro; un agente che non serve si spegne dal registro |
| **Più eventi, più token**: con più autonomia la spesa sale | Tetti per lavoro, per agente e per classe; Haiku e i modelli più piccoli sulla corsia N ([ricerca/45 §10](../ricerca/45-architettura-v3.md)) |

**Le uscite.** Ogni pezzo sta dietro un'interfaccia: il motore parla con gli strumenti solo attraverso i server MCP, con i modelli solo attraverso LiteLLM, con l'esterno solo attraverso il Cancello. Fa eccezione la corsia T, che usa Claude Code sul posto della persona, fuori da LiteLLM, e ripiega sulla corsia S ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). Se un pezzo non regge si cambia quel pezzo, e il resto rimane. La tabella delle uscite, pezzo per pezzo, è in [ricerca/36 §12](../ricerca/36-architettura-v2.md).

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
- 5: il bot di Teams, che è la prova della milestone 3 ([proposta §11 e §13](../PRESENTAZIONE-CEO.md));
- 22 e 17-18: la riaccensione automatica del server, prima del primo lavoro L3 notturno sul banco, e la seconda GPU per la milestone 2, con il suo riser ([ricerca/45 §11](../ricerca/45-architettura-v3.md); [ADR-0014](adr/0014-seconda-gpu-blackwell.md));
- 27: piani M365 e Jira e chi dà i consensi per Graph, con cui il pilota legge le trascrizioni e manda le mail ([proposta §11 e appendice A, voce B3](../PRESENTAZIONE-CEO.md)).

La domanda 28 sul linguaggio resta aperta, ma non blocca più: TypeScript è accettato dal gruppo di progetto per le due corsie e il Cancello, e la conferma di Mattia non ferma il lavoro ([ADR-0010](adr/0010-typescript-motore.md); [ricerca/45 §5, D5](../ricerca/45-architettura-v3.md)).

**Le decisioni nuove che restano a Michele** ([ricerca/49 §9](../ricerca/49-instradamento-a-piu-motori.md); [ADR-0027](adr/0027-decisore.md)):

- se TypeSafe, il fornitore di Jev, può ricevere i dati gialli; senza il suo sì Jev decide solo sui testi verdi;
- le repo ammesse nella corsia T e le regole di GitHub;
- se e dove far girare sul nostro server le sessioni della corsia T.

**Le domande per Anthropic** ([ricerca/36 §13](../ricerca/36-architettura-v2.md); [ricerca/49 §1.3 e §9](../ricerca/49-instradamento-a-piu-motori.md)):

- se il nostro piano Team del bundle startup ha diritto ai crediti API inclusi, fino a 500 $ al mese, e se si sommano ai crediti del bundle; si controlla anche da «Organization settings > Billing»;
- per iscritto, se far partire i compiti programmati del Team da un nostro programma interno, per i lavori di sviluppo della persona del posto, rientra nell'uso previsto; prima della corsia T sui progetti veri;
- i tetti di spesa per persona del piano Team, che non sono offerti a ogni organizzazione;
- la conservazione zero dei dati delle API, che si chiede subito ([proposta §14](../PRESENTAZIONE-CEO.md));
- se un giorno il sistema si offre ai clienti, come si applicano all'Agent SDK i termini sulla chiave di ogni utente finale.

## 8. Le spese e le decisioni chieste ai CEO

Il dettaglio è nella [proposta §12 e §14](../PRESENTAZIONE-CEO.md). La proposta chiedeva ai CEO solo decisioni di budget, abbonamenti, acquisti e integrazioni; le scelte tecniche le abbiamo studiate noi, quelle sull'infrastruttura restano di Michele ([proposta §14](../PRESENTAZIONE-CEO.md)). Il 10 novembre 2026 i CEO hanno approvato il progetto e hanno lasciato le scelte al gruppo di progetto: da allora queste decisioni le prende il gruppo di progetto, con Michele per l'infrastruttura. L'elenco della v3 serve solo da riferimento ([ricerca/45, «Decisione del gruppo di progetto», e §9](../ricerca/45-architettura-v3.md)). Prezzi IVA esclusa, dove non è scritto altro ([proposta §12.1](../PRESENTAZIONE-CEO.md)).

### 8.1 Cosa si chiedeva, e cosa vale oggi

La proposta chiedeva tre cose ([proposta §1](../PRESENTAZIONE-CEO.md)):

1. Il via alle fasi 0 e 1, con la verifica alla settimana 8 su criteri tecnici e commerciali.
2. Nessun abbonamento nuovo oltre a quelli del board di Michele: Proxmox (20 € al mese), l'IP fisso (fino a 10 €), la macchina Oracle per l'accesso da fuori (0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento) e, se Michele li sceglie, gli abbonamenti Proxmox per firewall e backup (fino a circa 103 € al mese, decisione 17).
3. Il budget una tantum delle prime otto settimane: il parere legale unico (tetto 2.500 €, con due preventivi), il credito API se serve (circa 223 €), le spese del board che conviene fare subito (backup in sede, chiavi FIDO2, accessori). In tutto circa 2.900-3.890 €, più circa 140-550 € per le batterie nuove dell'UPS se il test di autonomia all'arrivo va male.

Il progetto è approvato e lo sviluppo è partito. Con la v3 la spesa una tantum di oggi resta di circa 2.900-3.890 € ([ricerca/45 §9.1](../ricerca/45-architettura-v3.md)). Le differenze ([ricerca/45 §9.1](../ricerca/45-architettura-v3.md)):
- la revisione esterna diventa facoltativa: da 3.560 a 5.940 € in meno;
- le chiavi FIDO2 restano, per l'accesso al board con NetBird, non più sulle carte;
- il parere legale resta con il tetto di 2.500 €, con due domande in più;
- la linea di riserva costa uguale, 77-200 €, ma si anticipa;
- la seconda GPU si propone per la milestone 2 ([ADR-0014](adr/0014-seconda-gpu-blackwell.md)): la sezione 8.4 dice quanto e quando.

### 8.2 Quanto si spende in più al mese, fase per fase

| Periodo | € al mese in più | Cosa comprende |
|---|---|---|
| Fasi 0-1 e inizio della fase 2, finché Azure resta accesa | ≈ 135 (circa 141 se servisse un server a pagamento per l'accesso) | Proxmox (20), IP fisso (fino a 10), corrente del rack (≈ 105), la macchina Oracle per l'accesso da fuori (0 € sul piano gratuito di Oracle; 6,49 € se servisse un server a pagamento) |
| Fase 2 (settimane 9-21), con Azure spenta | da ≈ -15 a ≈ +20 | Azure spenta fa risparmiare circa 150 €; Jira Standard, se serve |
| Fasi 3-4 (settimane 22-40) | da ≈ -1 a ≈ +70 | WhatsApp con numero dedicato, Slack, invio della newsletter, corrente della RAM in più |
| Fasi 5-6 (dalla settimana 41) | da ≈ 46 a ≈ 168 | Si aggiunge la linea telefonica italiana di "Andrea" (44-90 €) |

Fonte: [proposta §1 e §12.1](../PRESENTAZIONE-CEO.md).

**Cosa cambia con la v3** ([ricerca/45 §9.2](../ricerca/45-architettura-v3.md)):
- la base resta uguale: nessun canone nuovo, circa 135 € al mese nelle fasi 0-1 e 479-583 € al mese a listino a regime;
- la linea di riserva aggiunge 10-11 € al mese dall'inizio della fase 3, non dalla fase 5;
- Metricool, che fa da ponte per i post della pagina aziendale, non costa nulla in più; quando entra Postiz si risparmiano 59,86 € al mese;
- riserve facoltative: Managed Agents, il servizio in cui Anthropic fa girare gli agenti, circa 4-35 € al mese se usato, solo sui dati verdi e solo se il server è pieno o fermo; la voce di Andrea in cloud circa 88 € al mese, se la voce in casa non passa ([ADR-0024](adr/0024-abbonamenti-come-riserva.md));
- la corrente della seconda GPU, 3-8 € al mese, arriva prima se la scheda si compra per la milestone 2 ([ADR-0014](adr/0014-seconda-gpu-blackwell.md)).

**Modelli e posti.** Le API di Claude per gli agenti (stima 90-250 € al mese) dovrebbero stare dentro i crediti del bundle startup; se non bastano si pagano, con un tetto a 250 € ([proposta §1](../PRESENTAZIONE-CEO.md)). La stima resta, da misurare nella fase 1: più autonomia vuol dire più lavori ([ricerca/45 §9.2](../ricerca/45-architettura-v3.md)). In più:
- il piano Team include fino a 500 $ al mese di crediti API, che coprono l'API, l'Agent SDK e Managed Agents ma non Claude Code; se il nostro piano del bundle ne ha diritto va controllato ([ricerca/49 §1.3](../ricerca/49-instradamento-a-piu-motori.md));
- il decisore su Jev costa circa 0,05 $ ogni mille decisioni [stima di ricerca/49 §5];
- la corsia T non costa nulla in più finché basta l'uso del posto; oltre il limite costa come l'API. Quanto lavoro sta in un posto Anthropic non lo pubblica: lo misura la prova della corsia T ([ricerca/49 §1.5 e §5](../ricerca/49-instradamento-a-piu-motori.md)).

Claude Team è gratuito per il primo anno; alla scadenza si decide quanti posti tenere (fino a 447 € al mese) ([proposta §1](../PRESENTAZIONE-CEO.md)). Dall'11 novembre i posti servono anche la corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). Il listino a regime, nella fase 6, è di circa 479-583 € al mese ([proposta §12.1](../PRESENTAZIONE-CEO.md)). Il costo vero resta il tempo di sviluppo della sezione 5 ([proposta §1](../PRESENTAZIONE-CEO.md)).

### 8.3 Le decisioni e quando servono allo sviluppo

Sono le 23 decisioni che la proposta chiedeva ai CEO, con il momento e il costo della proposta. La colonna «Oggi» dice cosa vale dal 10 novembre, quando le decisioni sono passate al gruppo di progetto ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)).

| # | Decisione | Quando serve | Costo | Oggi |
|---|---|---|---|---|
| 1 | Avviare le fasi 0 e 1, con la verifica alla settimana 8 | oggi | le prime 8 settimane (giorni nella sezione 5); nessun abbonamento nuovo oltre a quelli del board | presa il 10 novembre con l'approvazione del progetto; lo sviluppo è partito lo stesso giorno |
| 2 | Parere legale unico (email, registrazioni, dati verso Claude Team, "Andrea", coaching, firma elettronica, dati negli USA, backup a casa di Michele) | subito: i punti del pilota entro la settimana 3, il resto prima della fase 2 | tetto 2.500 €, con due preventivi | uguale, con due domande in più: la riga AI e il valore di un messaggio L2 ([ricerca/45 §9.1](../ricerca/45-architettura-v3.md)) |
| 3 | Tetto mensile delle API se i crediti non bastano, e credito prepagato | dalla fase 0 | tetto 250 € al mese (stima 196 €); credito 0-223 € | uguale; da controllare i crediti API del piano Team ([ricerca/49 §1.3](../ricerca/49-instradamento-a-piu-motori.md)) |
| 4 | Spese del board per backup, corrente e sicurezza: backup in sede; batterie nuove dell'UPS solo se il test all'arrivo va male; nodo per la copia fuori sede, che fa anche da firewall della rete dove sta; più avanti un Proxmox Backup Server (il server dei backup) più grande fuori sede; chiavi FIDO2; accessori | backup in sede, chiavi e accessori subito; batterie all'arrivo dell'UPS; nodo fuori sede entro marzo 2027; server dei backup più grande quando servirà più spazio | circa 165-500 €; circa 140-550 €; circa 240-250 €; circa 690-930 €; 232-464 €; fino a 200 € | importi uguali; le chiavi FIDO2 servono all'accesso con NetBird, non alle carte ([ADR-0023](adr/0023-protezioni-essenziali.md)) |
| 5 | Revisione esterna di sicurezza di Cancello, motore e bot, prima che i dati dei clienti restino sul server | entro la settimana 21 | indicativo 3.560-5.940 € (£3.000-5.000), con due preventivi | facoltativa: si fa se un cliente la chiede ([ADR-0023](adr/0023-protezioni-essenziali.md)) |
| 6 | Jira Standard per 4 persone, se oggi siamo sul piano gratuito | dalla fase 2 | 28 € al mese | uguale |
| 7 | Macchina esterna per l'accesso da fuori (NetBird; Pangolin, che pubblica verso internet solo i punti d'ingresso necessari, come il bot di Teams e le pagine di firma; monitoraggio): Michele ha scelto Oracle Cloud a Milano | dalle fasi 0-1 | 0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento | uguale ([ADR-0018](adr/0018-accesso-oracle-netbird-pangolin.md)) |
| 8 | Canali in più: Telegram, Slack, WhatsApp con numero dedicato | dalla fase 3 | Telegram 0 €; Slack 0 o 27 € al mese; WhatsApp circa 7-12 € al mese | uguale; sui canali scrive il Cancello al livello della classe del destinatario ([ADR-0006](adr/0006-teams-chat-di-gruppo.md)) |
| 9 | Invio della newsletter con un servizio di posta esterno | dalla fase 4 | meno di 1 € al mese | la decide il gruppo di progetto con Michele; newsletter a L2 dopo 3 numeri puliti ([ADR-0013](adr/0013-postiz-listmonk-docuseal.md)) |
| 10 | Voce di "Andrea": eccezione alla regola delle voci sintetiche nelle call, con una linea telefonica italiana | dalla fase 5, solo per chi chiede di essere richiamato, con voce dichiarata, parere e lead vere | 44-90 € al mese; attivazione 7-14 € | accettata dal gruppo di progetto; le chiamate vere aspettano il parere ([ADR-0008](adr/0008-andrea-centralino.md)) |
| 11 | RAM: altri 192 GB, 12 moduli uguali a quelli montati | prima della fase 3, o quando il margine scende sotto i 5 GB | circa 690-830 € | accettata dal gruppo con Michele; all'inizio della fase 3, o prima se il margine con 6 sessioni S scende sotto i 5 GB ([ADR-0015](adr/0015-ram-384-gb.md)) |
| 12 | Seconda GPU RTX PRO 2000 Blackwell da 16 GB, con il riser secondario e la staffa se mancano | appena torna sotto i 1.000 € IVA inclusa, dalla fase 3; comunque entro l'inizio della fase 5 | circa 880-1.220 € | proposta a Michele per la milestone 2, anche a 1.100 € (sezione 8.4) ([ADR-0014](adr/0014-seconda-gpu-blackwell.md)) |
| 13 | Linea internet di riserva: 4G/5G con una SIM dati aziendale; Starlink, internet via satellite, solo se in ufficio il segnale mobile è scarso | prima della fase 5 | 4G/5G: 77-200 € una tantum e 10-11 € al mese; Starlink: 349 € e 31 € al mese | accettata dal gruppo di progetto e anticipata: prima del primo L3 esterno fuori orario e di Andrea, in pratica all'inizio della fase 3 ([ADR-0019](adr/0019-linea-di-riserva.md)) |
| 14 | Vivavoce da sala per le riunioni dal vivo | fase 3 | 100-250 € | uguale ([ricerca/45 §11](../ricerca/45-architettura-v3.md)) |
| 15 | Strumenti commerciali fuori dal board: Apollo (ricerca di contatti) e Higgsfield (video e immagini per i post) restano; Metricool finché Postiz non è pronto; Apify (segnali di assunzione) sostituito da Firecrawl; moda.app (slide) sostituito da Claude Team; Perplexity (arricchimento in SersanOutreach) da decidere con il prezzo; After Effects (grafica animata) resta com'è oggi, senza costi in più | Metricool fino alla fase 4 | fino a 188 € al mese; con il consiglio circa 146 € fino alla fase 4, poi circa 86 € | la decide il gruppo con Michele; Metricool programma i post della pagina aziendale a L2 finché Postiz non entra ([ADR-0013](adr/0013-postiz-listmonk-docuseal.md); [ADR-0024](adr/0024-abbonamenti-come-riserva.md)) |
| 16 | Posti Claude Team alla fine del bundle | alla scadenza del bundle | 447 € al mese con 5 premium; 357 con 4; 214 con 2 premium e 2 standard | i posti servono anche la corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)) |
| 17 | Abbonamenti del board: Proxmox sul server; Proxmox sul firewall e sui due server dei backup, se Michele li sceglie; IP fisso | dalle fasi 0-1 | Proxmox sul server 20 € al mese; firewall circa 10 € al mese; 46,67 € al mese per ogni Proxmox Backup Server, circa 93 € per tutti e due; IP fisso fino a 10 € al mese | uguale: scelte di Michele |
| 18 | Teams nel piano M365, se oggi manca | subito, se manca: il bot di Teams è una delle prove della fase 0 | 6-14 € al mese | uguale; il bot di Teams è la prova della milestone 3 |
| 19 | Premio mensile per chi costruisce con l'AI | fase 4 | 50-100 € al mese | uguale |
| 20 | Assistente personale: account Claude personale per chi lo vuole | fase 6 | 15-18 € al mese a persona | uguale |
| 21 | Firma elettronica qualificata, solo se il parere la chiede per certi contratti | dopo il parere, per la fase 6 | a preventivo | la decide il gruppo con Michele ([ADR-0013](adr/0013-postiz-listmonk-docuseal.md)) |
| 22 | Strumento di fatturazione: quello che usiamo già, se fa al caso; altrimenti uno sul nostro server | fase 6 | 0 € o il canone dello strumento scelto | la decide il gruppo con Michele ([ADR-0013](adr/0013-postiz-listmonk-docuseal.md)) |
| 23 | Un mese di prova di Grok Bot, uno degli agenti in abbonamento valutati nel primo giro, su soli dati pubblici | facoltativa | circa 54 € una volta | uguale |

Fonti: decisioni e costi da [proposta §14](../PRESENTAZIONE-CEO.md); i momenti da [proposta §1, §11, §12.2 e appendice A](../PRESENTAZIONE-CEO.md); Pangolin da [proposta §5.2](../PRESENTAZIONE-CEO.md); a cosa servono gli strumenti commerciali da [ricerca/25 §7](../ricerca/25-board-michele-e-delta.md); Grok Bot da [proposta, appendice B](../PRESENTAZIONE-CEO.md); la colonna «Oggi» dalle ADR citate e da [ricerca/45 §9](../ricerca/45-architettura-v3.md).

### 8.4 L'hardware, in ordine

È l'hardware che consigliamo a Michele, con il momento di oggi. L'ordine per l'autonomia è: riaccensione automatica, batterie dell'UPS, backup, linea di riserva, RAM, seconda GPU. I primi quattro rendono affidabile il lavoro L3 quando in ufficio non c'è nessuno; gli ultimi due ne allargano il volume ([ricerca/45 §11](../ricerca/45-architettura-v3.md)). La seconda GPU si anticipa per un altro motivo: serve alla prova dei modelli locali ([ADR-0014](adr/0014-seconda-gpu-blackwell.md)).

| Cosa | Quando | Costo | Cosa sblocca | Fonte |
|---|---|---|---|---|
| Riaccensione automatica dopo un blackout | subito, prima del primo lavoro L3 notturno sul banco | 0 € | debrief e catene ripartono senza nessuno in ufficio | [ricerca/45 §11](../ricerca/45-architettura-v3.md) |
| Test delle batterie dell'UPS | all'arrivo | 140-550 €, se il test va male | lo spegnimento ordinato regge e nessuna catena si perde a metà | [ricerca/45 §11](../ricerca/45-architettura-v3.md) |
| Backup 3-2-1, con il server dei backup in sede | fase 2, prima dei dati dei clienti | 165-500 € subito; 240-250 € entro marzo 2027 | i dati dei clienti sul server dopo la settimana 21 | [ricerca/45 §11](../ricerca/45-architettura-v3.md); [ADR-0016](adr/0016-backup-3-2-1.md) |
| Linea di riserva 4G/5G | prima del primo L3 esterno fuori orario e prima di Andrea, in pratica all'inizio della fase 3 | 77-200 €, più 10-11 € al mese | follow-up, richiamate e lavori a orario continuano anche se cade la fibra | [ADR-0019](adr/0019-linea-di-riserva.md) |
| RAM: altri 192 GB, fino a 384 | all'inizio della fase 3, o prima se il margine misurato con 6 sessioni S scende sotto i 5 GB | 690-830 €, più 6-10 € al mese di corrente | Vexa nelle call di altri, 12-16 sessioni S, crescita verso cento agenti | [ADR-0015](adr/0015-ram-384-gb.md); [ricerca/45 §11](../ricerca/45-architettura-v3.md) |
| Seconda GPU RTX PRO 2000 Blackwell da 16 GB | proposta per la milestone 2, senza aspettare che il prezzo scenda; serve il sì di Michele | 1.100 € su Amazon.it il 10 novembre, più il riser (75-160 €) se manca; 3-8 € al mese di corrente. La proposta stimava 880-1.220 € | prova dei modelli locali; trascrizione dal vivo, voce di Andrea, memoria e un modello piccolo insieme, giorno e notte | [ADR-0014, seconda revisione](adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md) |
| Vivavoce da sala | fase 3 | 100-250 € | le riunioni dal vivo entrano nel post-call | [ricerca/45 §11](../ricerca/45-architettura-v3.md) |
| Secondo nodo, in programma a dicembre | a scelta di Michele | fino a 1.500 € | può ospitare Cancello e Porta separati dal motore, o fare da riserva fredda | [ricerca/45 §11](../ricerca/45-architettura-v3.md) |

**Cosa non comprare ora.** Né la scheda da 24 GB a 70 W, che oggi costa circa 3.750-4.100 €, più di tre volte quella da 16 GB, né una scheda più grande con il cavo di alimentazione, che farebbe perdere al server la ridondanza degli alimentatori. Si riparla di una scheda più grande, o di un nodo pensato per la GPU, solo se la prova della milestone 2 chiede un modello più grande in casa ([ADR-0014, seconda revisione](adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md)).

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

- [ricerca/45-architettura-v3.md](../ricerca/45-architettura-v3.md): intestazione «Decisione del gruppo di progetto», §1-§6, §9, §10, §11 e §12.
- Le ADR in [docs/adr/](adr/README.md): da [0020](adr/0020-autonomia-a-livelli.md) a [0030](adr/0030-bacheca-gruppi-specchi.md), e le revisioni del 10 e dell'11 novembre di 0001, 0003, 0004, 0005, 0006, 0011, 0012, 0013, 0014, 0015 e 0019; le revisioni del 12 novembre di 0026, 0027 e 0028; inoltre 0008, 0010, 0016 e 0018.
- [ricerca/51-modelli-open-weight-sul-computer-di-sviluppo.md](../ricerca/51-modelli-open-weight-sul-computer-di-sviluppo.md), per il decisore in casa.
- [ricerca/46-obsidian-come-casa-dei-testi.md](../ricerca/46-obsidian-come-casa-dei-testi.md): §7, §8 e §9.
- [ricerca/48-modelli-locali-e-gpu.md](../ricerca/48-modelli-locali-e-gpu.md): §5.5, §6.1 e §6.2.
- [ricerca/49-instradamento-a-piu-motori.md](../ricerca/49-instradamento-a-piu-motori.md): §1.3, §1.4, §1.5, §5, §7, §8 e §9.
- [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026: §1, §2, §4-§15 e appendici A e B.
- [ricerca/36-architettura-v2.md](../ricerca/36-architettura-v2.md): §4.5, §7, §12 e §13.
- [ricerca/25-board-michele-e-delta.md](../ricerca/25-board-michele-e-delta.md): §7.
- [ricerca/34-proposta-1-agent-sdk.md](../ricerca/34-proposta-1-agent-sdk.md): §4.3.
- [Architettura](03-architettura.md), per la Sala di controllo.
- [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md).
- [Board di Michele](../allegati/infra/SerSan%20Infra%20Board.md) e [board del rack](../allegati/infra/Rack%20SerSan%2012U.md).
- [strumenti/md_to_docx.py](../strumenti/md_to_docx.py) e [strumenti/marchio.py](../strumenti/marchio.py).
- I fatti sullo sviluppo (repo privata, milestone del PRD, stato della milestone 1) vengono dalla repo privata del codice, che non è pubblica.
