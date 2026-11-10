# P-A · Motore Agent SDK con autonomia a livelli

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **P-A**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Proposta di architettura per SerSan Agent OS, 9 novembre 2026.

**Fonti.** Ho letto tutti i file il 9/11/2026.
- **Documenti di progetto:**
  - **P** = `PRESENTAZIONE-CEO.md` v2.1;
  - **SPEC** = `docs/superpowers/specs/2026-11-09-nucleo-motore-cancello-design.md`, revisione 2;
  - **PRD** = `.claude/prds/sersan-agent-os.prd.md`;
  - **D03** = `docs/03-architettura.md`;
  - **DOM** = `DOMANDE-PER-MICHELE.md`;
  - **R05, R16, R18, R26, R28, R29, R30, R31, R36** = i rapporti con quel numero in `ricerca/`.
- **Trascrizioni:**
  - **TR** è la trascrizione di riferimento; la cito con il minuto.
  - **TT-A, TT-B e TT-C** sono le tre trascrizioni di terzi, nell'ordine `grokbot transcript.txt`, `claude and grokbot updates.txt` e `Grokbot vs Hermes.txt`. Sono dimostrazioni e opinioni di terzi, quindi tutto ciò che ne prendo è [non verificato].
- **Rapporti ricevuti:** RAP1-RAP4 sono i quattro rapporti del giro. I fatti web di RAP4 li ha letti il suo autore il 9/11 sulle URL che cita. Non li ho riletti, e li segno «da RAP4».
- **Cosa è mio:** livelli, soglie, finestre, tetti e giorni sono proposte o stime mie, segnate [non verificato: proposta] o [non verificato: stima].

---

## 1. L'idea in 5 righe

1. Teniamo il motore sull'Agent SDK e il Cancello come unico esecutore verso l'esterno, ma il Cancello diventa leggero. Invece di una carta per ogni azione, dà un livello (L0-L3) a ogni terna formata da agente, tipo d'azione e classe di destinatari.
2. Gli agenti partono da eventi già dalla fase 1: fine della call e orari, poi posta e modulo. Si passano il lavoro in una bacheca che si vede nel canale «Agenti», e in un giro fanno tutte le scritture interne che servono.
3. Una terna sale solo con prove pulite: 5 sì senza modifiche portano a L2, 15 finestre senza «Ferma» portano a L3. Serve un tocco del responsabile, e non si supera mai il tetto della classe. Al primo segnale negativo la terna scende da sola.
4. Restano solo le protezioni essenziali:
   - niente cancellazioni, credenziali o pagamenti in mano agli agenti;
   - stop di emergenza;
   - tetti di spesa;
   - registro semplice;
   - correzione degli errori;
   - conformità minima.
5. A regime il sistema lavora da solo come nella trascrizione di riferimento: dopo la call, al mattino, prima degli incontri, al telefono con le lead e nella bacheca. Restano a una persona offerte, contratti, fatture, primi contatti e la voce dei founder.

---

## 2. Componenti e dove girano

### 2.1 I componenti

| Componente | Cosa fa in P-A | Dove gira | Da quando | RAM | GPU | Fonte |
|---|---|---|---|---|---|---|
| **Motore** (runner) | coda in PostgreSQL, un processo SDK per ogni lavoro di tipo S, chiamate a schema per il tipo N, ripresa, tetti | fase 1: VM `stage-agenti` (LAB); dalla fase 2: `agenti-01` | fase 1 | stage 8 GB, compresi Cancello e PostgreSQL di prova. Poi 12 GB con 6 sessioni, 16 con 8-10, 20 con 12-16 | no | [verificato: R36 §4.1-4.2] |
| **Ingresso eventi** | sullo stage, un lettore periodico dentro il motore: trascrizioni Teams ogni 5 minuti, calendario, orari per persona. Dalla fase 2 lo sostituisce n8n, con webhook firmati e orari | stage, poi n8n del board | fase 1 | trascurabile | no | lettura a delta di Graph ogni 5-10 minuti, senza porte in ingresso [verificato: R30 §3.4]; n8n [verificato: D03 §3.2]; lettore nel motore [non verificato: proposta] |
| **Cancello leggero** | livelli per terna, carte L1, finestre L2, esecuzioni L3, outbox, registro, stop, tetti | fase 1 sullo stage; dalla fase 2 in `cancello-01` o nella VM del motore, come preferisce Michele | fase 1 | 3-4 GB | no | RAM [verificato: R36 §4.1]; stessa VM [non verificato: proposta] |
| **Porta Teams** | carte, pulsante «Ferma», carte di promozione; nove bot di squadra dalla fase 2 | con il Cancello | fase 1 | 0,5-1 GB | no | [verificato: R36 §4.1] |
| **Bacheca** | annunci, compiti e passaggi in PostgreSQL, rispecchiati nel canale «Agenti» | PostgreSQL 16 del board | minima nella fase 1, completa nella fase 2 | nel database | no | modello [verificato: R36 §5.4]; anticipo [non verificato: proposta] |
| PostgreSQL 16, n8n, LiteLLM, BookStack, Qdrant con MCP RAG, Infisical, Firecrawl, pipeline AI | come nella v2 | server, VLAN del board | LiteLLM con la fase F4 del board; nelle fasi 0-1 chiave diretta con tetto nella Console | nel board, più 1-5 GB di crescita del database | RTX 4000 per la pipeline | [verificato: R36 §4.1, §7.1] |
| Server MCP (memoria, bacheca, Jira, SersanOutreach, posta e calendario in lettura) | le prese degli agenti | `mcp-01` | fase 2 | 3-4 GB | no | [verificato: R36 §4.1] |
| Trascrizione delle call Teams | la fa Microsoft, Graph la consegna | M365 (cloud del board) | fase 1 | 0 | no | [verificato: P §6.4; R30 §3.1] |
| Vexa e trascrizione in casa | bot nelle call dei clienti | `meet-01`, `ai-gpu-01` | fase 3 | 12 GB (circa 4 con Vexa Lite), più 6-8 GB | 2-4,5 GB di giorno; CPU quando la GPU è altrove | [verificato: R36 §4.1] |
| Postiz | programma i post via API | server, mai pubblico | fase 2 se Michele lo ammette prima della F4; altrimenti Metricool come eccezione fino alla fase 4 | 2 GB | no | RAM [verificato: R36 §4.1]; prima della F4 entrano solo i servizi del pilota [verificato: P §6.2]; anticipo [non verificato: proposta] |
| listmonk con relay SMTP | newsletter | server più servizio esterno | fase 4 | 0,5 GB | no | [verificato: R36 §4.1] |
| **Andrea** (Asterisk e Pipecat) | richiama in 90 secondi e risponde alle chiamate in entrata | `voce-01`, `andrea-01` | su CPU dalla fase 3 se ci sono lead vere e il parere; altrimenti fase 5 | 1 GB più 6-8 GB su CPU; 4 GB con la seconda GPU | seconda GPU facoltativa, per una voce migliore | [verificato: R31 §8.2; R36 §4.1]; anticipo [non verificato: proposta] |
| Buzz, Paperclip, prova di Hermes | piloti in LAB | Experimental-2 | fasi 4 e 6 | 4-8 GB dentro Experimental | no | [verificato: R36 §4.1] |
| Cloud del board | M365 e Teams, Claude Team, API Anthropic, Jira, Instantly | cloud | subito | — | — | [verificato: P §5.1] |
| Esterni | operatore telefonico, Meta, Telegram, Slack, relay SMTP | esterni | fasi 3-5 | — | — | [verificato: P §5.1, §14] |

- Il motore non usa la GPU [verificato: P §6.2].
- I tipi di lavoro sono tre [verificato: R36 §5.2]. Per risparmiare RAM, P-A fa diventare tipo N tutto ciò che riassume, classifica o estrae: sono chiamate senza processo di Claude Code. Il tipo S resta ai lavori a più passi [non verificato: proposta].
- P-A non usa la modalità `auto` dell'SDK. È un classificatore in più, quindi un controllo in più. Costa token se LiteLLM non inoltra i campi giusti, e Anthropic la può spegnere dal suo lato [verificato da RAP4 §1.2-1.3]. Bastano `dontAsk` e un elenco chiuso di strumenti, che lo SPEC già usa [verificato: SPEC §4.3].

### 2.2 RAM e GPU per fase

Valori in GB.

| | Fase 1 | Fase 2 | Fasi 3-4 | Fasi 5-6 |
|---|---|---|---|---|
| v2.1, GB nuovi | 8 | 25 | 53,5 | 70-74 |
| P-A, GB nuovi | 8 | 25-27, con Postiz anticipato | 53,5; circa 62,5 se Andrea su CPU arriva nella fase 3 | 70-74 |
| P-A, liberi con 192 GB (53 liberi nel board) | circa 45 | circa 26-28 | circa 0; circa -9 con Andrea | da -17 a -21 |

[verificato per la v2.1: P §6.3; R36 §4.2. Righe P-A: non verificato, stima]

- **RAM.** I 192 GB in più restano da comprare prima della fase 3 (decisione 11, 690-830 €) [verificato: P §6.3, §14]. Se Andrea anticipa, all'inizio della fase 3 la RAM non ha margine. La leva è Vexa Lite, che usa circa 4 GB invece di 12 [verificato: R36 §4.2].
- **GPU.** La RTX 4000 resta alla pipeline. Quando Michele la presta a Experimental-1, i lavori della GPU aspettano in coda [verificato: P §6.4]. In P-A né il motore né Andrea su CPU dipendono dalla GPU, quindi il lavoro L3 continua anche la sera [verificato: R31 §8.2].

### 2.3 Abbonamenti e alternative, alla pari

| Opzione | Cosa aggiunge all'autonomia | Costo | Limite | Quando serve |
|---|---|---|---|---|
| Voce di Andrea in cloud | voce già pronta | circa 88 €/mese [verificato: R36 §12] | l'audio delle lead esce dall'azienda | solo se la voce in casa non passa la prova d'ascolto [verificato: P §13] |
| Managed Agents | cron al minuto, budget per sessione, webhook, multiagente [da RAP4 §2.2] | 0,08 $ per ora di sessione attiva più i token; al massimo 58,40 $/mese per un agente sempre acceso [verificato: R18 §0 p.4] | ciclo e trascrizioni da Anthropic negli USA, senza ZDR [da RAP4 §2.1] | lavori su soli dati verdi, se il server è pieno; il piano base non lo usa |
| Grok Bot | routine a orario o a intervallo, webhook che svegliano i bot, chat di gruppo e consegne visibili [non verificato: TT-A] | prova di un mese, circa 54 € [verificato: P §14, dec. 23] | computer solo negli USA; i controlli più forti sono solo sul piano Enterprise [da RAP4 §4]; un tetto d'uso settimanale che, raggiunto, ferma il lavoro [non verificato: TT-A, TT-C] | pilota su dati pubblici |
| Hermes in casa | stanze che smistano da sole, `max_hops`, cron, skill che si curano [da RAP4 §3.3] | licenza 0 €; pilota 6-8 gp; sostituzione del runner 26-33 gp [verificato: P §15] | 312 problemi aperti sul gateway, 228 senza correzione [da RAP4 §3.2]; chat che si mescolano fra bot nell'uso reale [non verificato: TT-C] | uscita, se il motore non regge |
| Paperclip | organigramma e budget degli agenti | licenza 0 €; pilota 2 gp [verificato: R36 §7.3] | è un piano di controllo, non un motore | pilota nella fase 6 |
| Buzz | stanza comune di persone e agenti | licenza 0 €; circa 6 gp [verificato: P §15] | approvazioni non collegate; nessun rilascio dopo il 9/10 [da RAP4 §7] | pilota nella fase 4 |
| Dots | un agente sempre acceso per persona | crediti di prezzo ignoto; nel Regno Unito solo con Business Premium [da RAP3 §1, sezione D] | dati nel cloud del fornitore | fuori dal piano |
| Linea internet di riserva | il lavoro L3 continua se cade la fibra | 77-200 € una tantum più 10-11 €/mese [verificato: P §14, dec. 13] | — | prima del primo L3 esterno 24 ore su 24 |

---

## 3. Il modello di autonomia

### 3.1 Livelli, terne e classi di destinatari

- **Cosa riceve il livello.** Il Cancello dà il livello a una **terna**: agente, tipo d'azione e classe di destinatari. Per un singolo destinatario si può aggiungere un'eccezione, per esempio un cliente che vuole «solo con revisione» e resta a L1 [non verificato: proposta].
- **Dove sta ogni cosa** [non verificato: proposta]:
  - il **tetto** di ogni classe sta in `config/livelli.yaml`, in git, e lo decidono i CEO;
  - il **livello attuale** sta nel database del Cancello;
  - i **limiti fissi** stanno nel codice.
- **Classi e livelli.** I limiti fissi sono quelli del compito. Il resto è [non verificato: proposta].

| Classe di destinatari | Esempi | Partenza | Tetto |
|---|---|---|---|
| Interno | canali interni, CRM, Jira, calendario, libro delle proposte in BookStack, la persona stessa | L3 | L3 |
| Contatto noto in conversazione | la persona appena incontrata in una call registrata e avvisata, nel dominio del cliente; chi ci ha scritto negli ultimi 30 giorni | L1 | L3, dopo il parere |
| Lead che ha chiesto la richiamata | Andrea | L3, con prove a vuoto prima delle lead vere | L3 |
| Pubblico aziendale | pagina aziendale, newsletter agli iscritti | L1 | L2 |
| Voce dei founder | post e commenti sui profili personali | L1 | L1 |
| Destinatario nuovo | primo contatto, dominio mai visto | L1 | L1 |
| Impegni | offerte, contratti, fatture, prezzi, affermazioni tecniche | L1 | L1 |
| Codice e infrastruttura | pull request, patch | L1 | L1; le skill interne seguono il §3.4, flusso 9 |
| Pagamenti | — | L0: l'agente prepara, una persona paga | L0 |
| Cancellazioni e credenziali | — | vietate | vietate |

### 3.2 Come si sale e come si scende

**Salire** [non verificato: proposta; soglie da tarare]:

| Passaggio | Condizione | Chi lo conferma |
|---|---|---|
| L1 → L2 | 5 sì di fila senza modifiche sulla stessa terna, e nessun segnale negativo negli ultimi 30 giorni | il responsabile della squadra, con un tocco sulla carta di promozione che prepara il Guardiano |
| L2 → L3 | 15 esecuzioni in L2 senza «Ferma» e senza segnali negativi negli ultimi 60 giorni | lo stesso responsabile |
| oltre il tetto della classe | mai | — |

**Scendere** è automatico e immediato [non verificato: proposta]:

| Segnale | Effetto |
|---|---|
| «Ferma» durante la finestra | la terna torna a L1 |
| modifica a una carta | il contatore riparte da zero |
| risposta del destinatario classificata come correzione, lamentela o «non scrivetemi» | la terna scende di un livello; l'indirizzo entra nella lista di soppressione unica [verificato: P §9.1, r. 5] |
| «sbagliato» premuto sul riepilogo del giorno | la terna scende di un livello |
| rimbalzo, o destinatario fuori dalla classe | l'invio si blocca e la terna scende di un livello |
| due segnali in 30 giorni | la terna torna a L1 |
| incidente serio (destinatario sbagliato, dato riservato uscito) | tutte le classi esterne dell'agente tornano a L1, con un avviso al responsabile |
| stop di emergenza | la classe che l'ha causato riparte da L1 |
| doppione: stessa impronta verso la stessa destinazione in 7 giorni | non parte da solo e diventa una carta; il controllo dei doppioni c'è già [verificato: SPEC §4.7] |

Chiunque dei quattro può abbassare un livello con un tocco. Per alzarlo serve il responsabile.

### 3.3 La finestra L2 e la trasparenza

- **Cosa c'è già.** Oggi il Cancello risponde in tre modi: carta, accettazione per regola, no [verificato: SPEC §4.5]. Un compito periodico, ogni 30 secondi, porta le carte scadute a «scaduta» [verificato: SPEC §4.7].
- **Cosa aggiunge P-A.** Lo stesso compito periodico gestisce anche le finestre [non verificato: proposta]:
  - nasce una carta «parte alle HH:MM», con il pulsante «Ferma»;
  - alla scadenza, se nessuno ha fermato, l'esecutore ricalcola l'impronta ed esegue una volta sola.
- **Orari.** La finestra conta solo nell'orario di lavoro scritto in «Come lavoro», di default 8:30-19:00 dal lunedì al venerdì. Un follow-up nato alle 18:50 parte alle 9:20 del giorno dopo [non verificato: proposta].
- **Durata della finestra per classe** [non verificato: proposta]:
  - 30 minuti per il follow-up dopo una call;
  - 60 minuti per le risposte e gli inviti a contatti noti;
  - 24 ore per i post sulla pagina aziendale, per la newsletter (con un invio di prova alla persona) e per la chiusura dei to-do di una persona;
  - 24-48 ore per le aperture di Andrea e per le skill interne.
- **Trasparenza.** Ciò che esce a L2 o a L3 non lo legge nessuno prima, quindi conta come scritto da un agente da solo. Porta una riga che dice che l'ha preparato e inviato l'assistente AI di SerSan per conto della persona. La regola 1 chiede di dichiararsi AI quando si scrive da soli a un esterno; ciò che una persona approva esce invece a suo nome [verificato: P §9.1, r. 1]. Il testo della riga lo fissa il parere [non verificato: proposta].
- **Limiti nel tempo.** Il riepilogo del giorno elenca tutto ciò che è partito a L2 e a L3.

### 3.4 I nove flussi

Come leggere la tabella:
- per ogni azione: livello di partenza con la fase, livello a regime e come si sale;
- le regole per salire e per scendere sono quelle del §3.2, salvo dove indico altro;
- livelli, fasi e soglie sono [non verificato: proposta]; le fonti dei fatti sono nelle note sotto la tabella.

| Flusso | Azione | Partenza | A regime | Come si sale |
|---|---|---|---|---|
| **1. Dopo una call** | evento «trascrizione pronta» → Analista chiamate (tipo N) → pacchetto del Post-call | L3, fase 1 | L3 | — |
| | riassunto e prossimi passi nel canale interno del cliente; registro dei meeting | L3, fase 1 | L3 | — |
| | meeting e deal nel CRM | L3, fase 2 | L3 | — |
| | to-do in Jira | L3, fase 2 | L3 | — |
| | mail di follow-up alla persona incontrata | L1, fase 1 | L3, se il parere lo consente | 5 sì → L2; 15 finestre → L3 |
| | messaggio nel canale condiviso con il cliente (Teams condiviso, Slack, WhatsApp) | L1, fase 3 | L3 | come la mail |
| **2. Debrief** | debrief all'ora che ognuno sceglie (di default le 7:00); dentro: cosa hanno fatto gli agenti da soli ieri e quali livelli sono cambiati | L3, fase 1 | L3 | — |
| | evento in calendario | L3, fase 2 | L3 | — |
| **3. Brief e slide** | brief la sera prima per ogni incontro in calendario con esterni (2 ore prima se l'incontro nasce in giornata) | versione leggera L3 a fine fase 2; completa nella fase 3 | L3 | — |
| | slide per noi | L3, fase 3 | L3 | — |
| | slide inviate al cliente | L1, fase 3 | L2 (tetto) | 5 sì → L2 |
| **4. Offerta** | bozza dal catalogo, dalla trascrizione e dal brief, entro un'ora | L3, fase 3; skill in Claude Team dalla fase 0 | L3 | — |
| | invio dell'offerta | L1: carta a Michele, senza FIDO2 | L1 (tetto) | non sale |
| **5. Marketing** | ricerca concorrenza, temi, bozze, numeri del lunedì | L3, fase 2 | L3 | — |
| | post sulla pagina aziendale, programmati da Postiz via API | L1, fase 2 | L2 (tetto) | 5 post approvati senza modifiche → L2 |
| | post sui profili dei founder | L1 | L1 (tetto) | non sale |
| | newsletter | L1, fase 4 | L2 (tetto) | 3 numeri approvati senza modifiche → L2 |
| | risposte ai commenti della pagina aziendale | L1, fase 4 | L2 (tetto) | 5 sì → L2 |
| | commenti sui profili dei founder | L0: l'agente segnala soltanto | L0 | non sale |
| **6. Andrea** | richiama entro 90 secondi chi ha dato il consenso nel modulo; appuntamento in calendario; conferma alla lead; esito nel CRM e nel canale vendite; chiamate in entrata | L3, con 50 chiamate di prova prima delle lead vere | L3 | nessuna finestra entra in 90 secondi |
| **7. Coaching** | report a chi ha fatto la call; piano mensile | L3, fase 3-5, con i volumi | L3 | — |
| | dati aggregati al responsabile | L3 | L3 | — |
| | report individuale al responsabile | bloccato finché c'è il parere | secondo il parere | dipende dal parere |
| **8. Agenti che si parlano** | annunci e passaggi in bacheca, rispecchiati nel canale «Agenti» | L3, fase 1 (minima) | L3, entro il tetto della catena | — |
| | chiusura dei compiti fra agenti | L3, fase 2 | L3 | — |
| | chiusura dei to-do di una persona, con la prova | L2, fase 2 | L3 per chi lo sceglie | 15 finestre pulite → L3 |
| | stand-up degli agenti ogni mattina, prima del debrief | L3, fase 2 | L3 | — |
| **9. Imparare** | analisi settimanale dei rifiuti di Andrea | L3 | L3 | — |
| | nuove aperture di Andrea | L2 (24 ore), poi prova A/B a L3 | L2 per l'apertura, L3 per l'A/B | — |
| | skill interne proposte dagli agenti, con una valutazione automatica | L2 (48 ore), fase 2-3 | L3 | 3 promozioni pulite → L3 |
| | skill che cambiano testi verso l'esterno | L1 | L1 (tetto) | non sale |

**Note sui flussi:**

- **Flusso 1.**
  - Nella trascrizione di riferimento, dopo la call partono da soli il riassunto nel canale del cliente, l'opportunità nel CRM, la mail di follow-up e i to-do, «in modo totalmente autonomo» [verificato: TR 4:42-5:07].
  - La mossa che sblocca il flusso è la classe «persona appena incontrata». Con la regola «Sempre» per destinazione, il primo follow-up restava su carta per sempre [verificato da RAP2, punto 2; regola in P §5.4]. R16 propone che il follow-up a un cliente con cui si è parlato non sia marketing a freddo, ma è una proposta da confermare con il parere [verificato: R16 §3, p. 2, segnata lì come proposta].
  - Il post-call non è istantaneo. La trascrizione arriva pochi minuti dopo la call, e con una lettura ogni 5-10 minuti servono circa 10-20 minuti; il tempo è da misurare [verificato: R30 §3.4].
  - La registrazione automatica di Teams probabilmente non parte se entra solo il cliente [verificato: R30 §3.6]. Nelle call dei clienti il bot va ammesso [verificato: R30 §4.4]. Senza trascrizione, l'agente chiede alla persona una nota vocale (L0).
- **Flusso 2.**
  - Nella trascrizione il debrief è alle 5:30 [verificato da RAP1: TR 5:12-5:25]. Nella v2.1 è alle 7:00 [verificato: P §4.8].
  - Nella fase 1 il debrief ha poca materia: gli agenti non leggono Jira, il CRM né la memoria [verificato: SPEC §1; PRD «Fuori»]. P-A ci aggiunge la lettura del calendario.
- **Flusso 3.** Così si chiude la lacuna AU-19, cioè il brief che parte da solo per ogni incontro in agenda [verificato da RAP1 §3]. I limiti restano:
  - il brief è profilazione e va nella DPIA [verificato: P §9.1, r. 9];
  - i post di LinkedIn si leggono solo con una via consentita;
  - le aperture delle mail si vedono solo con la casella attiva [verificato: P, appendice A, voce D2 e «Lacune dichiarate»].
- **Flusso 4.**
  - Il tetto L1 per le offerte è una scelta di business dei CEO, non sicurezza. Scope e prezzi restano umani [verificato: P §9.3].
  - Anche nella trascrizione il livello dell'offerta non è detto [verificato da RAP1, AU-21].
- **Flusso 5.**
  - Programmare i post da soli richiede di cambiare la regola di casa. Oggi su Metricool scrive solo una sessione presidiata, mai una routine [verificato: R05, regole di pubblicazione; P §8.2]. La regola è di Alberto, che è il responsabile del Marketing.
  - Per la newsletter la soglia è bassa perché esce una volta al mese: con 20 sì servirebbero quasi due anni [verificato da RAP2, voce K9].
  - L'accesso alle API della pagina LinkedIn è ancora da verificare [verificato: P, appendice A, voce L8].
- **Flusso 6.**
  - Nella trascrizione l'agente vocale richiama entro 90 secondi, 24 ore su 24, si dichiara AI e fissa l'incontro con una persona [verificato: TR 14:55-16:02].
  - Le regole sono quelle di R31 [verificato: R31 §9]:
    - consenso registrato nel modulo;
    - consultazione del Registro delle opposizioni;
    - frase d'apertura fissa che dichiara l'AI;
    - di notte richiama solo se la lead ha scelto «adesso».
  - Si scende così [non verificato: proposta]:
    - «non chiamatemi più» manda il numero nella lista di soppressione;
    - due lamentele in 30 giorni fanno tornare Andrea a L1, cioè propone l'orario e una persona richiama;
    - se l'API non risponde, Andrea si scusa e una persona richiama [verificato: R31 §7.2].
  - Su CPU la latenza è di 1,6-2,5 secondi [verificato: R31 §7.2]. La voce clonata di un collega si usa solo con un suo contratto separato e revocabile [verificato: P §14, dec. 10].
- **Flusso 7.**
  - Nella trascrizione il report va al venditore e al suo responsabile [verificato da RAP1: TR 14:36-14:50].
  - Da noi, al responsabile vanno solo dati aggregati finché non arriva il parere. Se i venditori sono dipendenti vale l'art. 4 dello Statuto dei lavoratori. Con la profilazione il sistema è ad alto rischio dal 2/12/2027, e stimare le emozioni è vietato [verificato: R16 §1.2, §4].
- **Flusso 8.**
  - Nella trascrizione gli agenti hanno una chat comune: un annuncio fa partire il lavoro di un altro agente, e si fanno notare i to-do già fatti [verificato: TR 3:59-4:30].
  - Nella v2 i to-do delle persone si chiudono solo con il sì del titolare [verificato: R29 §4.2; R36 §5.4].
  - Il freno della v2 ammette 3 passaggi per catena e 8 messaggi per thread [verificato: P §4.11]. Il percorso di un cliente dopo la call coinvolge sei agenti [verificato: P §4.10].
  - P-A propone tre tetti [non verificato: proposta]:
    - un tetto in dollari per catena;
    - 8 passaggi per le catene dichiarate;
    - lo stop dei cicli, cioè la stessa coppia di agenti che si rimbalza il lavoro più di due volte.
  - Il conteggio parte dall'ultimo messaggio umano, come fa `max_hops` nella v0.23 di Hermes [da RAP4 §3.3].
  - Si scende così [non verificato: proposta]: se il titolare riapre un to-do chiuso dall'agente, quella coppia di agente e persona torna a L1.
- **Flusso 9.**
  - Nella trascrizione l'agente vocale impara da solo dai rifiuti [verificato: TR 15:31-15:43].
  - La frase che dichiara l'AI resta fissa e la controlla un test [verificato: R31 §10]. Una variante d'apertura che fa peggio del controllo su un numero fissato di chiamate si spegne da sola [non verificato: proposta].
  - Le skill curate a mano si bloccano, come fa il «curator lock» di Hermes [da RAP4 §3.3]. Se una valutazione peggiora, la skill torna alla versione precedente e a L1 [non verificato: proposta].
  - Il ciclo dei rifiuti ha bisogno di volumi [verificato: P, appendice A, «Lacune dichiarate»].

### 3.5 Cosa P-A non promette

- **Promozioni lente.** Con 11 lead, 1 risposta e 0 meeting al 5/10 [verificato: P §7.1], i livelli L2 e L3 verso l'esterno arrivano tardi. Subito è autonomo solo il lavoro interno.
- **Post-call non istantaneo.** Servono minuti, non secondi (flusso 1).
- **Pubblicazione e outbound.** Su pagine, profili e campagne decidono le regole di casa e la legge. Per le email B2B verso l'Italia il Garante chiede il consenso anche per i contatti aziendali [verificato: R16, sintesi p. 7].
- **Segnali negativi.** Una lamentela scritta in modo ambiguo può sfuggire alla classificazione. Il riepilogo del giorno con il pulsante «sbagliato» serve proprio a coprire questo buco [non verificato: proposta].

---

## 4. Protezioni essenziali

### 4.1 Le sei protezioni

1. **Limiti fissi, scritti nel codice e non in configurazione.**
   - Cancellazioni e credenziali: il tipo d'azione è sempre negato e non esiste un esecutore [verificato: D03 §4.1; SPEC §4.6].
   - Pagamenti: non esiste un esecutore di pagamento. L'agente prepara, una persona paga [verificato: P §4.9].
   - Un'«annulla» chiesta da una persona la esegue il Cancello a nome di quella persona, mai un agente da solo [non verificato: proposta].
2. **Stop di emergenza.**
   - Lo preme dal telefono uno qualsiasi dei quattro; lo tolgono Alessandro o Michele [verificato: SPEC §9, D2].
   - Ferma la coda e le sessioni, e annulla carte e finestre aperte. Dalla fase 2 porta a zero i budget di LiteLLM, fa scattare il kill switch di SersanOutreach e mette in pausa Instantly [verificato: D03 §4.3].
   - Dopo lo sblocco ripartono i nuovi eventi; le azioni annullate no [non verificato: proposta].
3. **Tetti.**
   - Per lavoro (`maxBudgetUsd`, `maxTurns`) e per agente al mese, con avviso all'80% e stop al 100% [verificato: SPEC §4.12].
   - Per catena [verificato: P §4.11].
   - Nuovo: un tetto al giorno per ogni classe esterna a L3, per esempio 20 mail al giorno per agente [non verificato: proposta].
4. **Registro semplice.**
   - Una tabella a sola aggiunta: chi, cosa, quando, livello, esito, costo.
   - I permessi del database consentono solo di aggiungere e leggere; i segreti sono oscurati [verificato: SPEC §4.9 per i permessi e l'oscuramento].
   - Conservazione 90 giorni [verificato: P §9.1, r. 8].
   - Niente catena di impronte, MAC né ancora esterna [non verificato: proposta].
5. **Correzione degli errori.**
   - Il pulsante «Ferma» nella finestra.
   - «Annulla» per le scritture interne: riapre il to-do, rimette il campo del CRM com'era, toglie l'evento in calendario creato dall'agente, su richiesta di una persona.
   - «Rettifica» per un invio già partito: la bozza di correzione va su carta e la terna scende di livello.
   - Il riepilogo del giorno in ogni debrief.
   - Nuovi tentativi automatici quando l'errore prova che non è partito niente, cosa che lo SPEC fa già per gli esecutori [verificato: SPEC §4.8]. P-A li estende ai lavori falliti per un errore di rete prima di qualsiasi proposta. Il doppione lo blocca il controllo del §3.2 [non verificato: proposta].
6. **Conformità minima.**
   - Registro dei trattamenti e DPIA per registrazioni, agente vocale, analisi delle vendite e brief [verificato: P §9.1, r. 9; R16 §6, r. 9].
   - Avviso di registrazione [verificato: P §9.1, r. 2].
   - Conservazione con scadenze [verificato: P §9.1, r. 8].
   - Una sola lista di soppressione per tutti i canali [verificato: P §9.1, r. 5].
   - Riga AI sui testi a L2 e L3, e Andrea che si dichiara AI (AI Act art. 50, dal 2/8/2026) [verificato: R16 §2; P §9.1, r. 1].
   - Nessuna stima delle emozioni (art. 5(1)(f)) e formazione documentata dei quattro (art. 4) [verificato: R16 §4; P §10].
   - Email B2B secondo la regola italiana [verificato: R16 §3].
   - Consenso e Registro delle opposizioni per Andrea [verificato: R31 §9].
   - Nuovo agente solo con la sua riga nel registro dei trattamenti [verificato: P §4.12].
   - I tre colori dei dati e il limite «sullo stage solo verde e giallo finché la F3 non è validata» restano: sono regole del board di Michele [verificato: P §5.6, §11].

### 4.2 Cosa dipende dal parere legale

Il parere unico ha un tetto di 2.500 € [verificato: P §14, dec. 2]. Decide:
- se la mail di follow-up alla persona incontrata può salire a L2 e L3, e con quale testo per la riga AI;
- la base per le email B2B verso l'Italia, cioè se e come si fanno i primi contatti [verificato: R16 §7, p. 6];
- se i dati rossi, come le trascrizioni, possono andare all'API di Anthropic senza l'oscuramento locale [verificato: P §5.6, §9.4];
- Andrea: se la richiamata chiesta dalla lead è una «chiamata automatizzata», che testo deve avere il consenso, come si usa il Registro delle opposizioni, e se SerSan deve marcare l'audio sintetico [verificato: R31 §14, punti 7-8];
- il coaching individuale al responsabile e l'art. 4 dello Statuto [verificato: R16 §7, p. 2 e 5];
- la registrazione delle call con clienti nel Regno Unito, i trasferimenti verso gli USA e la firma elettronica [verificato: P §9.4].

P-A aggiunge tre domande: le prime due della lista, più i livelli nei canali condivisi con i clienti [non verificato: proposta].

### 4.3 Cosa toglie P-A rispetto alla v2.1

| Cosa si toglie | Dove sta oggi | Cosa resta al suo posto |
|---|---|---|
| Secondo passo con la chiave FIDO2 sulle carte | P §5.4; D03 §4.1 | identità di Teams sulla carta. Le chiavi FIDO2 restano al board per l'accesso, con NetBird ed Entra [verificato: R36 §6] |
| Regole «Sempre»: 20 sì, una sola destinazione, scadenza a 30 giorni | P §5.4; R36 §5.8 | livelli per classe, con promozione e retrocessione |
| Prova a secco di 1-2 settimane per ogni automazione | P §9.2 | la partenza a L1 |
| Firme HMAC con numero monouso fra i processi interni | SPEC §3 | un token per processo sulla rete interna |
| Codice monouso per ogni consegna e impronta calcolata dalla Porta | SPEC §4.7 | impronta ricalcolata dall'esecutore |
| Registro a catena con MAC e ancora esterna | SPEC §4.9 | tabella a sola aggiunta |
| Più runner, con possesso, battito e riserve sul tetto del mese | SPEC §4.2, §4.12 | un solo runner con N sessioni |
| Un solo effetto per giro, anche per le scritture interne | SPEC §2.1 | il pacchetto (§7) |
| Revisione esterna obbligatoria entro la settimana 21 (3.560-5.940 €) | P §12.2, dec. 5 | facoltativa, decisione dei CEO |
| VM del Cancello sempre separata | R36 §4.1 | scelta di Michele |

---

## 5. Fasi

### 5.1 Cosa è autonomo e quando

Tutte le righe sono [non verificato: proposta].

| Flusso | Settimana 8 (fine fase 1, stage) | Settimana 21 (fine fase 2, server) | A regime (settimana 53 circa) |
|---|---|---|---|
| Dopo una call | riassunto e registro L3 entro 10-20 minuti; mail L1, oppure L2 se la terna ha già 5 sì puliti; to-do elencati nel riassunto | riassunto, CRM e Jira L3; mail L2, o L3 dopo 15 finestre pulite e il parere | tutto a L3, compreso il canale condiviso dopo la promozione |
| Debrief | L3 all'ora di ciascuno | L3, più l'evento in calendario | L3 |
| Brief e slide | skill in Claude Team (L0) | brief leggero L3, se la capacità regge; altrimenti a inizio fase 3 | brief completo L3; slide al cliente fino a L2 |
| Offerta | skill (L0) | skill (L0) | bozza L3 entro un'ora; invio L1 |
| Marketing | skill, sessione presidiata | interno L3; pagina aziendale L1, poi L2 | pagina L2; founder L1; newsletter L2 |
| Posta in arrivo | — | smistamento L3; risposte a contatti noti L1, poi L2 | risposte a contatti noti L3; destinatari nuovi L1 |
| Andrea | — | — | L3, dalla fase 3 se ci sono lead vere e il parere |
| Coaching | — | — | L3 al venditore; aggregati al responsabile |
| Agenti che si parlano | bacheca minima: passaggio Analista → Post-call visibile in «Agenti» | bacheca completa, nove bot, stand-up; to-do delle persone L2 | uguale, fino a cento profili |
| Imparare | le correzioni alle carte diventano esempi | proposte di skill con valutazione automatica; skill interne L2 | skill interne L3; aperture di Andrea L2, poi A/B |

### 5.2 Cosa cambia rispetto alle fasi della v2.1

I giorni sono giorni-persona (gp) di base. Quelli della v2.1 sono [verificato: P §15; R36 §7.3]; le differenze sono [non verificato: stima].

| Fase | gp v2.1 | Cosa entra in P-A | Cosa esce o si alleggerisce | gp P-A |
|---|---|---|---|---|
| 0 | 18 | prova del delta di Graph su posta e trascrizioni (+0,5) | — | 18,5 |
| 1 | 22,5 | livelli, finestra, promozione e retrocessione (+2); pacchetto (+0,5); riga AI, tetti per classe e «annulla» (+1); eventi su stage: trascrizioni, calendario, orari (+1); bacheca minima con lo specchio in «Agenti» (+2, presi dalla fase 2) | pezzi di sicurezza del §4.3 (−3,5); oscuramento locale se il parere lo consente (−1,5) | 24-25,5 |
| 2 | 58,5 | posta come evento con uno Smistatore minimo (+3, dalla fase 3); Postiz e Pubblicatore via API (+2,5, dalla fase 4); proposte di skill con valutazione (+3); Agenda per contatti noti (+1,5, dalla fase 3); brief leggero (+1, dalla fase 3); stand-up degli agenti (+0,5) | FIDO2 sulle carte (−1,5); regole «Sempre» (−1,5); bacheca minima già fatta (−2) | circa 65 |
| 3 | 61,75 | carta per campagna in SersanOutreach, dopo il parere (+2-4); Andrea su CPU (+24, dalla fase 5) solo se ci sono lead e parere | Smistatore (−3), Agenda (−1,5), brief leggero (−1) | 58-60; 82-84 con Andrea |
| 4 | 26,5 | — | Postiz (−2,5), proposte di skill (−1,5) | 22,5 |
| 5 | 38 | — | Andrea (−24) se è anticipato | 38, oppure 14 |
| 6 | 24 | — | — | 24 |
| **Totale** | **249,25** | | | **circa 250-254** |

- **Fonti dei pezzi spostati:** le stime di carta per campagna (2-4 gp) e bacheca (5,5 gp) vengono da RAP2 §6 e §10; Postiz con listmonk 4,5 gp, proposte di skill 1,5, Andrea 24+4 [verificato: R36 §7.3].
- **Il totale resta quasi uguale.** Le semplificazioni pagano le aggiunte, e i pezzi che rendono possibile l'autonomia arrivano prima [non verificato: stima].

### 5.3 Effetto sul calendario

- **Capacità.** Con circa 6,5 gp a settimana fino alla fase 3 e 7,5 dalla fase 4 [verificato: R36 §7.1]:
  - la fase 2 si allunga di circa 1,3 settimane;
  - le fasi 3 e 4 si accorciano di altrettanto;
  - il totale resta circa 53 settimane, e 42 con 9 gp a settimana [verificato: P §15; per P-A: non verificato, calcolo mio].
- **Settimana 21.** Se la capacità resta a 6,5 gp, brief leggero e Agenda slittano di 1-2 settimane.
- **Settimana 8.** Come nella v2.1, con tutta la riserva la fase 1 sfora alla settimana 9 [verificato: R36 §7.2].
- **Cosa resta della v2.1:**
  - si chiedono oggi le sole fasi 0 e 1 [verificato: P §11];
  - ogni fase parte quando la precedente è verificata [verificato: P §11];
  - «prima il funnel» [verificato: P §11];
  - i dati dei clienti restano sul server solo dopo la verifica della settimana 21 [verificato: P §11, §13].

---

## 6. Costi

### 6.1 Una tantum

Importi IVA esclusa.

| Voce | v2.1 | P-A | Fonte |
|---|---|---|---|
| Parere legale unico | tetto 2.500 € | uguale, con tre domande in più | P §14, dec. 2 |
| Credito API, se servono | 0-223 € | uguale | P §12.2 |
| Spese del board da fare subito: backup in sede, chiavi FIDO2, accessori | 165-500 + 232-464 + 0-200 € | uguale; le chiavi FIDO2 servono all'accesso del board | P §12.2 |
| Batterie dell'UPS, se il test va male | 140-550 € | uguale | P §12.2 |
| Revisione esterna | 3.560-5.940 € | facoltativa; se la si fa, solo sulla parte esposta | P §12.2; [non verificato: proposta] |
| RAM, altri 192 GB | 690-830 € prima della fase 3 | uguale | P §12.2 |
| Seconda GPU | 880-1.220 € | uguale; non serve più ad Andrea per partire | P §12.2; R31 §8.2 |
| Linea internet di riserva 4G/5G | 77-200 € prima della fase 5 | uguale, ma prima del primo L3 esterno 24 ore su 24 | P §14, dec. 13 |
| Vivavoce da sala | 100-250 € | uguale | P §12.2 |
| Attivazione della linea di Andrea | 7-14 € | uguale, forse prima | P §12.2 |
| Riaccensione automatica del server | oggi va riacceso a distanza | 0 €; P-A la chiede come condizione per l'autonomia | DOM n. 22; P §13 |

**Chiesto oggi:** circa 2.900-3.890 €, come nella v2.1 [verificato: P §1]. **Dopo:** P-A risparmia fino a 3.560-5.940 € se la revisione esterna non si fa.

### 6.2 Mensili

Importi in euro al mese, IVA esclusa.

| Periodo | v2.1, in più rispetto a oggi | P-A | Fonte |
|---|---|---|---|
| Fasi 0-1 | circa 135 | uguale | P §12.1 |
| Fase 2 | da -15 a +20 | uguale; -59,86 se Postiz sostituisce Metricool già dalla fase 2; +10-11 se la linea di riserva arriva prima | P §12.1; R36 §8.2 |
| Fasi 3-4 | da -1 a +70 | uguale; +44-90 se Andrea parte nella fase 3 | P §12.1 |
| Fasi 5-6 | da 46 a 168 | uguale | P §12.1 |
| API di Claude | stima 196 (forbice 90-250), tetto 250 | uguale | P §12.1, §14 |
| Listino a regime | circa 479-583 | uguale, meno Metricool se esce prima | P §12.1 |

- **Gli eventi costano poco** [non verificato: calcolo mio, con i prezzi di R26 §2: Haiku 0,10/0,50 $ e Sonnet 2/10 $ per milione di token]:
  - classificare 50 mail al giorno con Haiku 5.5 costa meno di 1 $ al mese;
  - 100 post-call al mese con Sonnet 5.5 costano circa 7 $.
- **Abbonamenti facoltativi:** sono nel §2.3. Il piano base non ne aggiunge nessuno.

---

## 7. Cosa cambia nella milestone 1

Lo SPEC oggi:
- è una bozza in revisione 2, con 27 criteri;
- ha accolto i 15 rilievi della revisione avversaria, di cui 4 gravi [verificato: SPEC, intestazione, §12, §13];
- non ha ancora codice [verificato: SPEC §12.2], quindi si cambia senza perdere lavoro.

### 7.1 Sezione per sezione

| Sezione | Oggi | In P-A |
|---|---|---|
| §1 Perimetro | livelli e regole «Sempre» nella fase 2 | entrano nel nucleo: L1, L2 con finestra, L3 per regola, pacchetto, promozione, retrocessione, riga AI, tetti per classe, «annulla». Bacheca minima ed eventi vanno nelle milestone 4-5. FIDO2 esce |
| §2.1 Ponte | un effetto per giro, poi l'agente chiude | `propose_action` riceve un pacchetto: le scritture interne passano e il lavoro continua; gli elementi esterni producono una sola carta o finestra per giro |
| §3 Architettura | HMAC con numero monouso, margine di ±60 secondi; Cancello e motore su macchine separate | token per processo sulla rete interna; la stessa VM è ammessa. Restano i due utenti del database |
| §4.2 Coda | possesso, battito, più runner | un runner con N sessioni. Al riavvio il lavoro si riconcilia con la chiave della proposta; nuovi tentativi automatici se nessuna proposta è partita |
| §4.3 Runner | opzioni di isolamento | restano le stesse righe di configurazione (`tools: []`, `dontAsk`, `strictMcpConfig`, `settingSources: []`, `env` costruito da zero); via le verifiche dell'ambiente del processo |
| §4.4 Corsia N | testo di terzi solo come campi | resta: è ciò che rende sicuri gli eventi da posta |
| §4.6 Classi | elenco chiuso nel codice, solo `crm.nota` | politiche in configurazione, con un tetto per classe. Nel codice restano il no per ogni tipo sconosciuto e i limiti fissi |
| §4.7 Carte | sette condizioni, codici per consegna, impronta della Porta, epoca | la carta è valida se è in attesa, non è scaduta, chi decide è fra gli approvatori in configurazione e lo stop non è premuto. Nasce lo stato «in finestra», con «Ferma». La scadenza va per classe e in giorni lavorativi |
| §4.8 Outbox | due strade | tre strade: carta approvata, finestra scaduta senza «Ferma», regola L3 entro il tetto. Restano il commit prima dell'effetto e l'esito «incerta» che va a una persona |
| §4.9 Registro | catena, MAC, ancora | tabella a sola aggiunta con oscuramento |
| §4.10 Stop | epoche con blocchi di riga | un'unica riga di stato, letta dall'esecutore subito prima dell'effetto; carte e finestre annullate |
| §4.12 Tetti | riserve sul mese | tetto per lavoro e per mese, più un tetto giornaliero per classe |

### 7.2 I criteri: da 27 a 18

| Nuovo | Contenuto | Da |
|---|---|---|
| C1 | percorso L1: carta, sì o no, una sola esecuzione, ripresa; approvatori letti dalla configurazione | AC-001, 002, 011 |
| C2 | finestra L2: senza «Ferma» esegue una volta alla scadenza, nell'orario di lavoro; con «Ferma» niente effetto e la terna torna a L1. Una carta L1 scaduta non esegue | AC-008, nuovo |
| C3 | regola L3: esecuzione immediata entro il tetto giornaliero; una riga nel registro | AC-003, nuovo |
| C4 | pacchetto: più scritture interne nello stesso giro e un solo elemento esterno per giro | AC-003, 005 |
| C5 | promozione: dopo N sì puliti nasce la carta di promozione; il tocco cambia il livello, mai oltre il tetto | nuovo |
| C6 | retrocessione automatica per ogni segnale del §3.2, doppione compreso | nuovo |
| C7 | limiti fissi: cancellazioni, credenziali e pagamenti negati, anche chiamando direttamente l'API del Cancello | AC-007 |
| C8 | stop: coda ferma, carte e finestre annullate, nessun effetto dopo | AC-015, semplificato |
| C9 | una sola esecuzione anche con risposta persa, doppio clic, riavvio o Cancello che non risponde; esito incerto a una persona | AC-004, 010, 019, 025, 026 |
| C10 | ciò che esce è il testo della carta o della finestra: impronta ricalcolata all'esecuzione | AC-009, semplificato |
| C11 | testo di terzi solo come campi validati | AC-013 |
| C12 | solo gli strumenti del profilo, con un controllo della sessione | AC-006, 014, 022 |
| C13 | tetti per lavoro, per mese (avviso all'80%, stop al 100%) e per classe al giorno | AC-021, nuovo |
| C14 | ripresa dopo una notte o un riavvio, sul lavoro giusto, senza esiti persi | AC-018, 020, 027 |
| C15 | registro a sola aggiunta con i segreti oscurati | AC-016, 017 |
| C16 | riga AI presente in ogni testo esterno a L2 e L3 | nuovo |
| C17 | «annulla» delle scritture interne e rettifica dopo un invio | nuovo |
| C18 | prove con il modello a copione e giro dal vivo prima di ogni aggiornamento dell'SDK (importante, non obbligatorio) | AC-023, 024 |

- **Cosa esce del tutto:** AC-012 (richieste firmate) e la parte di AC-016 su catena, MAC e ancora.
- **Cosa resta dei 4 rilievi gravi della revisione avversaria** [verificato: SPEC §13], in forma più semplice:
  - i confini della strada senza carta, oggi garantiti dai tetti per classe e dai limiti fissi;
  - l'esecuzione una volta sola, garantita dall'outbox;
  - il legame fra ciò che si vede e ciò che esce, garantito dall'impronta;
  - l'idempotenza delle proposte.

### 7.3 Decisioni al gate

- **Restano:** D2, D3, D4, D5 e D6 [verificato: SPEC §9].
- **Cambia D1:** la scadenza va per classe e in giorni lavorativi, invece di 48 ore per tutte. Proposta: 3 giorni lavorativi per le bozze e 24 ore per ciò che dipende dal tempo [non verificato: proposta].
- **Nuove:**
  - D7, le soglie di promozione (5 e 15);
  - D8, il testo della riga AI, da fissare con il parere;
  - D9, l'orario di lavoro e la durata delle finestre;
  - D10, il tetto giornaliero per classe.

### 7.4 PRD

- **La metrica che cambia.** Oggi «Effetti usciti senza carta: 0» [verificato: PRD «Metriche»] misura solo che niente esca senza carta. Diventa «Effetti usciti fuori dal livello consentito: 0».
- **Metriche nuove:**
  - minuti fra la fine della call e il follow-up inviato;
  - quota di azioni esterne a L2 e L3;
  - «Ferma» ogni 100 finestre;
  - retrocessioni nel mese.

---

## 8. Rischi principali e strade d'uscita

| Rischio | Cosa fa P-A | Strada d'uscita | Costo dell'uscita |
|---|---|---|---|
| Una mail sbagliata arriva a un cliente senza che nessuno l'abbia letta | solo contatti noti; riga AI; tetti giornalieri; retrocessione al primo segnale; riepilogo del giorno; rettifica | abbassare il tetto della classe a L1 | 0 €, è configurazione |
| Pochi volumi: le promozioni non arrivano | soglie basse | i CEO, dopo il parere, fissano una partenza a L2 per una classe precisa | 0 € |
| Il parere dice no | i tetti seguono il parere | la classe resta L1: gli agenti preparano, una persona preme | 0 €; resta il tempo risparmiato sulle bozze |
| Istruzioni nascoste in mail e trascrizioni portano a un'azione autonoma | corsia N [verificato: SPEC §4.4]; destinatari nuovi mai sopra L1; doppioni su carta | portare a L1 le classi che partono da testo di terzi | 0 € |
| Meno difese di sicurezza | rete del board: VLAN, agenti senza internet [verificato: D03 §8.1]; token per processo; registro a sola aggiunta | rimettere firme e catena se i CEO lo chiedono | circa 2-4 gp [non verificato: stima] |
| L'Agent SDK cambia quasi ogni giorno | versione fissata e prove a ogni aggiornamento [verificato: P §13] | Hermes al posto del runner | 26-33 gp [verificato: P §15] |
| Continuità 24/7: una sola linea, riaccensione a mano, una GPU [verificato: P §13] | riaccensione automatica, nuovi tentativi, Andrea su CPU, finestre solo in orario | linea di riserva; voce di Andrea in cloud | 77-200 € più 10-11 €/mese; circa 88 €/mese |
| Capacità di sviluppo | le semplificazioni pagano le aggiunte | posta e Postiz alla fase 3 | 0 € |
| Postiz non ammesso prima della F4 | Metricool come eccezione | pubblicazione L1 con sessione presidiata, come oggi | 59,86 €/mese [verificato: R36 §8.2] |
| LiteLLM non inoltra gli header beta: la correzione è stata chiusa senza unione il 2/11 [da RAP4 §7] | prova a ogni aggiornamento | chiave diretta per famiglia con limiti nella Console [verificato: R36 §12] | 0 € |
| Più eventi, più token | tetti per lavoro, agente e classe; Haiku sul tipo N | meno eventi letti | 0 € |
| Motore in abbonamento come scorciatoia | fuori dal percorso dei clienti | pilota su dati pubblici | circa 54 € |

---

## 9. Funzioni: nessuna si toglie

### 9.1 Le 90 voci in P-A

Formato di ogni voce: agente · fase in P-A (fase v2.1) · livello a regime.
- Agenti e fasi v2.1 [verificato: P, appendice A, §4.1-4.9].
- Fasi P-A e livelli [non verificato: proposta].
- «=» vuol dire stessa fase della v2.1.

| Voce | Agente | Fase P-A (v2.1) | A regime |
|---|---|---|---|
| J1 | motore, bacheca, memoria, Cancello | 1-6 (2-6) | interno L3; esterno secondo la classe |
| J2 | registro dei profili, bot per squadra | 1-2 (=) | nuovo agente con approvazione e riga nel registro dei trattamenti |
| J3 | Agente email, Agente LinkedIn, Operatore outbound | 0 casella, 3 agenti (=) | risposte a contatti noti fino a L3; LinkedIn L1; primi contatti L1; campagne con una carta ciascuna |
| J4 | bacheca | 1-2 (2-3) | L3 entro il tetto della catena |
| J5 | Agente chiamate | 1 Teams, 3 Vexa (=) | L3 dove il bot è ammesso; dal vivo L0 |
| J6 | Agente brief, Agente slide | 0, 2 leggero, 3 (0, 3) | L3 per noi; al cliente fino a L2 |
| J7 | Editoriale, Ricerca concorrenza, Analista metriche, Copywriter, Pubblicatore; Video, Grafiche | 2; 4 (=) | interno L3; pagina L2; founder L1 |
| J8 | Agente task; Project manager, Report cliente, Onboarding, Sviluppatori | 2; 4 (=) | to-do L3; report al cliente fino a L2; pull request L1 |
| J9 | Porta e bot; Telegram, Slack, WhatsApp; Buzz | 1-2; 3; 4 (=) | interno L3; verso i clienti secondo la classe |
| A1 | Agente chiamate, Analista chiamate | 1-3 (=) | L3, con avviso |
| A2 | MCP memoria, BookStack | 2 (=) | lettura e libro delle proposte L3; libro «Processi» L2; «Come lavoro» lo cambia solo la persona |
| A3 | pipeline, Qdrant, MCP RAG | 3 (=) | L3 |
| A4 | motore | 1-2 (=) | L3, con eventi dalla fase 1 |
| A5 | Raccoglitore, Pulitore, Bibliotecario, Archivista | 3 (=) | L3; le scadenze di conservazione le esegue un lavoro fisso |
| A6 | revisore delle skill | 2-3 (4) | skill interne L3; skill su testi esterni L1 |
| A7 | bacheca, canale «Agenti» | 1 (2) | L3; to-do delle persone L2-L3 |
| B1 | Post-call | 1 interno, 3 canale condiviso (1-3) | L3 |
| B2 | Post-call | 2 (=) | L3 |
| B3 | Post-call | 1 (=) | L3 verso la persona incontrata, dopo il parere |
| B4 | Post-call, Agente task | 2 (=) | L3 |
| B5 | livelli | 1-6 (2-6) | per classe, fino al tetto |
| C1 | Report del mattino | 1 (=) | L3 |
| C2 | Agente chiamate, Vexa | 3 (=) | L3 nel tentativo |
| C3 | Analista chiamate (tipo N) | 1 (=) | L3 |
| C4 | Dettatura | 0, 2, 3 (=) | non è un'azione di agenti |
| C5 | Analista chiamate | 1 (1-2) | L3 |
| C6 | «Come lavoro» | 1 copia nel profilo, 2 BookStack (0, 2) | lettura L3 |
| D1 | Pipeline | 5 (=) | L3 con 30-50 chiusure |
| D2 | Agente brief | 2 leggero, 3 (3) | L3 |
| D3 | Agente brief, MCP RAG | 3 (=) | L3 |
| D4 | skill, Agente slide | 0, 3 (=) | per noi L3; al cliente fino a L2 |
| D5 | skill, Agente proposte | 0, 3 (=) | bozza L3; invio L1 |
| E1, E2, E4 | piano e formazione | tutte (=) | non sono azioni di agenti |
| E3 | Banca dei token, LiteLLM | 1, 2, 4 (=) | L3 |
| F1 | Mappatore processi | 4 (=) | L3 aggregato, con l'accordo di ciascuno |
| F2 | Intervistatore | 4 (=) | L3; l'intervista la conduce l'agente (lacuna AU-25 chiusa) |
| F3 | Mappatore processi | 4 (=) | analisi L3; libro «Processi» L2 |
| F4 | analisi mensile | 4 (=) | L3 |
| F5 | Claude Team, Open WebUI | 0 (=) | non è un'azione di agenti |
| G1 | Post-call | 2 (3) | L3 |
| G2 | qualificatore | 3-5 con i volumi (5) | L3 |
| G3, G4, K12 | Coach vendite | 3-5 (5) | L3 al venditore; aggregati al responsabile; individuale dopo il parere |
| G5, K10 | Andrea | 3 con lead e parere, altrimenti 5 (5) | L3 |
| G6 | Andrea | con G5 (5) | aperture L2, prova A/B L3 |
| G7 | Report del mattino | con G5 (5) | L3 |
| G8 | Analista vinto/perso | 3 (=) | L3 |
| G9 | registro | 2-6 (=) | nuovo agente con approvazione |
| G10, H1, H2, H4, H6, H7, I1, I2, I4 | persone, piano e qualità | come v2.1 | non sono azioni di agenti |
| H3 | Claude Team, Intervistatore | 0, 4 (=) | L3 |
| H5 | registro | 4 (=) | nuovo agente con approvazione |
| I3 | classi negate | 1 (=) | L0, per scelta |
| K1 | esecutore Outlook | 2 (=) | L3 |
| K2 | annunci in bacheca, Agente agenda | 2 (3) | contatti noti fino a L3; nuovi L1 |
| K3 | Smistatore posta | 2 (3) | smistamento L3; risposte a noti fino a L3; nuovi L1 |
| K4 | Claude Team con MCP RAG, Capo di gabinetto | 3 (=) | L3 |
| K5 | Agente intake | 3 (=) | brief L3; messaggi fino a L2 |
| K6 | Agente brief, Agente slide | 3 (=) | per noi L3; al cliente fino a L2 |
| K7 | template | 0 (=) | non è un'azione di agenti |
| K8 | SersanOutreach | 5 (=) | L3 |
| K9 | Agente newsletter | 4 (=) | L2 |
| K11 | Analista vinto/perso, Agente clienti simili | 3; 5 (=) | analisi L3; primo contatto L1 |
| K13 | Mappatore, Intervistatore | 4-6 (=) | L0 finché non c'è un'istanza per cliente |
| K14 | n8n da Sirius | 3-6 (=) | L3 |
| K15 | Agente acquisti | 6 (=) | registrazione delle fatture fornitori L3; pagamenti L0 |
| K16 | Assistente personale | 6 (=) | verso terzi fino a L2, se la persona lo sceglie; pagamenti mai |
| L1 | Agente contratti | 6 (=) | bozza L3; invio in firma L1 |
| L2 | Agente fatture e incassi | 6 (=) | fattura L1; solleciti a clienti noti fino a L2 |
| L3 | Controllo di gestione | 6 (=) | L3 |
| L4 | Agente bandi | 3 (=) | L3; la domanda la fa una persona |
| L5 | Assistenza clienti | 6 (=) | task L3; risposte ripetute a clienti noti fino a L3 |
| L6 | Agente rinnovi | 6 (=) | segnali L3; proposte L1 |
| L7 | Agente casi studio | 6 (=) | bozza L3; testimonianza L1; pubblicazione come J7 |
| L8 | Community manager | 4 (=) | pagina aziendale L2; profili dei founder: segnala soltanto |
| L9 | Agente sito e SEO | 6 (=) | pull request L1; pubblicazione fatta da una persona |
| L10 | Agente eventi e webinar | 6 (=) | iscrizioni L3; inviti L1; promemoria agli iscritti fino a L3 |
| L11 | Sistemista | 3 (=) | lettura L3; patch L1 a Michele |
| L12 | Allenatore AI | 6 (=) | L3, visibile solo all'interessato (lacuna AU-24 chiusa) |

### 9.2 Lacune della trascrizione che P-A chiude

[verificato da RAP1 §3; soluzioni: non verificato, proposta]

- **AU-09**, momenti di scambio fra agenti: lo stand-up degli agenti ogni mattina.
- **AU-19**, brief che parte da solo: un brief per ogni incontro in calendario.
- **AU-22**, risposte alla posta: livelli fino a L3 per i contatti noti.
- **AU-24**, suggerimenti alla singola persona: Allenatore AI e Mappatore, con l'accordo di ciascuno.
- **AU-25**, chi conduce l'intervista: la conduce l'agente.
- **AU-31**, voce registrata di un collega: già prevista, con un contratto separato [verificato: P, appendice A, voce G5].
- **I due processi rifatti con l'AI nella trascrizione**, eventi e formazione: per SerSan corrispondono a L10 (Agente eventi), L12 (Allenatore) ed E4 (formazione). Non si perde nulla.

### 9.3 Cosa manca e quanto costa

| Funzione | Cosa manca | Costo | Fonte |
|---|---|---|---|
| B3, J3, K3 | decisione sull'email, casella attiva, parere | parere, tetto 2.500 € | P §14 |
| B1, L5 | prova dei canali condivisi fra organizzazioni; Slack e WhatsApp come eccezioni | Slack 0-27 €/mese; WhatsApp 7-12 €/mese | P §12.1 |
| B2 | MCP di SersanOutreach su HTTP | 3,5 gp | R36 §7.3 |
| C2 | prova della registrazione automatica senza nessuno di SerSan in call | 0 € | R30 §3.6 |
| J5, A1, G9 | Vexa e RAM oltre le 16 sessioni | RAM 690-830 € | P §12.2 |
| A3, K4, E3 | pipeline e LiteLLM, che arrivano con la F4 del board | nel board | P, appendice A |
| J7, L8 | Postiz prima della F4 oppure Metricool; cambio della direttiva di pubblicazione; accesso API alla pagina LinkedIn | 59,86 €/mese per Metricool | R36 §8.2; P, appendice A |
| K9 | relay SMTP | meno di 1 €/mese | P §14, dec. 9 |
| G5, G6, K10 | operatore telefonico, prova della voce, parere, lead vere, consenso nei moduli; consigliate seconda GPU e linea di riserva | 44-90 €/mese più 7-14 €; GPU 880-1.220 €; linea 77-200 € più 10-11 €/mese | P §12, §14 |
| D1, G2, G6, G8, K11 | volumi di call e di chiusure | — | P, appendice A, «Lacune dichiarate» |
| G4 individuale | parere | dentro il tetto del parere | P §9.4 |
| D2 | casella attiva per le aperture; Apollo; via per LinkedIn confermata dal parere | Apollo 43,78 €/mese | R36 §8.2 |
| D4, K7 | template SerSan | lavoro interno | P, appendice A |
| F1, K3 | API di M365 da individuare; accordo di ciascuno sulla propria casella | — | P, appendice A |
| K13 | istanza separata per ogni cliente | da progettare | P, appendice A |
| K14, L3 | esportazione da Sirius, con la F4 del board | nel board | P, appendice A |
| K15, L2 | strumento di fatturazione (decisione 22) | 0 € o il canone dello strumento | P §14 |
| L1 | valore legale della firma; firma qualificata se serve | a preventivo | P §14, dec. 21 |
| L10 | licenza dei webinar di Teams | da controllare | P, appendice A |
| L11, J9, H1 | monitoraggio (F3) e sandbox (F5) del board | nel board | P, appendice A |
| A2 | MariaDB | 1 GB, già nel piano | R36 §4.2 |
| Pezzi propri di P-A | livelli, finestra, eventi in fase 1, valutazione delle skill, riga AI, «annulla» | compresi nel §5.2 | [non verificato: stima] |
