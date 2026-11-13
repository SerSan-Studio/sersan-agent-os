# Le alternative valutate

> **Aggiornato l'11 novembre 2026 all'architettura v3**, «Cancello a livelli e motore a due corsie» ([ricerca/45](../ricerca/45-architettura-v3.md); [ADR da 0020 a 0028](adr/README.md)). Cosa è cambiato in questo documento:
> - c'è un terzo giro di confronto, del 9 e 10 novembre, fatto con l'autonomia come criterio più pesante (§9);
> - ci sono le valutazioni fatte dopo quel giro: casa dei testi, «decisore», modelli locali e GPU, e l'11 novembre l'instradamento a più motori (§10);
> - i paragrafi dall'1 all'8 restano come storia dei primi due giri; dove il terzo giro li ha superati, una nota lo dice e rimanda all'ADR giusta.

Questo documento racconta come siamo arrivati alle scelte di SerSan Agent OS: quali architetture abbiamo confrontato, con quali punteggi, perché una strada ha vinto e cosa resta delle altre. Poi riprende, una per una, le alternative decise lungo il progetto, ognuna con i suoi pro, i suoi contro e l'esito. Serve a chi deve capire il progetto e a chi lo costruisce: per non rifare confronti già fatti e per sapere quali strade restano aperte.

Per i primi due giri la fonte di verità per cifre, fasi, decisioni e rischi è la [proposta per i CEO, versione 2.1 dell'8 novembre 2026](../PRESENTAZIONE-CEO.md), che qui chiamiamo "proposta". Il 10 novembre 2026 i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio. Da quel giorno l'architettura è la versione 3: dove la proposta e la v3 dicono cose diverse, valgono [ricerca/45](../ricerca/45-architettura-v3.md) e le [ADR](adr/README.md). I prezzi sono IVA esclusa salvo dove è scritto, come nella [proposta §12.1](../PRESENTAZIONE-CEO.md).

## In breve

- **Primo giro, 24 ottobre 2026.** Sette architetture, con le ipotesi di allora: Slack come chat, Notion come memoria scritta e diversi servizi in cloud. Vince Hermes Agent, un orchestratore open source (il programma che coordina gli agenti), insieme al Cancello: 159 punti su 240 ([proposta, appendice B](../PRESENTAZIONE-CEO.md)). Il Cancello è l'unico programma che può mandare una mail, scrivere a un cliente, toccare il CRM o telefonare: le azioni verso l'esterno le fa solo dopo il sì di una persona su una carta di approvazione, o con una regola "Sempre", e registra tutto ([proposta §5.1, §5.4](../PRESENTAZIONE-CEO.md)). *Superato dal terzo giro: il Cancello resta l'unico esecutore, ma ogni azione ha un livello di autonomia da L0 a L3 invece della carta fissa; vedi §9 e [ADR-0020](adr/0020-autonomia-a-livelli.md).*
- **Il board di Michele cambia la base.** Il 25 ottobre il disegno dell'infrastruttura di Michele tiene in cloud pochi servizi e porta tutto il resto sul nostro server ([ricerca/25, In breve](../ricerca/25-board-michele-e-delta.md)). Michele chiede anche di valutare se si può evitare Hermes usando l'Agent SDK di Claude, cioè Claude Code usato come libreria dentro un nostro programma, senza escludere Hermes a priori ([proposta §5.1, §5.7](../PRESENTAZIONE-CEO.md)).
- **Secondo giro, 25 ottobre 2026.** Tre proposte dentro il board. Vince il motore sull'Agent SDK con 171,5 punti, davanti a Claude Team al centro (170) e a Hermes sul nostro server (137). Di Claude Team al centro è entrata nel piano la fase zero ([proposta §5.7](../PRESENTAZIONE-CEO.md)).
- **Hermes resta una porta aperta.** Se il motore non regge alle verifiche delle settimane 8 e 21, si prova Hermes sullo stesso banco di prova e si decide sui numeri ([proposta §5.7](../PRESENTAZIONE-CEO.md)). Dopo il terzo giro Hermes è anche un pilota in laboratorio, e i criteri delle due verifiche sono cambiati ([ADR-0012, revisione del 10 novembre](adr/0012-hermes-uscita.md)).
- **Terzo giro, 9-10 novembre 2026: autonomia.** Il confronto si rifà con un criterio nuovo, quanto il sistema lavora da solo, che pesa 35 punti su 100 ([ricerca/45, «I documenti del giro»](../ricerca/45-architettura-v3.md)). Quattro proposte nuove; le prime due finiscono a 0,3 punti l'una dall'altra, 76,6 e 76,3 su 100 ([ricerca/45 §1.1](../ricerca/45-architettura-v3.md)). Vince la loro unione, «Cancello a livelli e motore a due corsie» (§9):
  - **il motore resta nostro, ma ha due corsie**: la corsia N fa catene fisse in cui il codice sceglie passi e destinatari e il modello scrive senza strumenti; la corsia S fa sessioni dell'Agent SDK per le figure che ragionano a più passi ([ADR-0021](adr/0021-motore-a-due-corsie.md));
  - **l'autonomia è per livelli**: il Cancello dà a ogni combinazione di agente, tipo d'azione e classe di destinatari un livello da L0 (a mano) a L3 (autonomo), che sale con le prove pulite e scende da solo al primo errore ([ADR-0020](adr/0020-autonomia-a-livelli.md));
  - **n8n è facoltativo**: orari ed eventi stanno nel motore, e il sistema di agenti non dipende da n8n ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md));
  - **restano le protezioni essenziali** di un sistema aziendale chiuso; la revisione esterna del codice diventa facoltativa ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- **Dopo il terzo giro, 10 e 11 novembre.** La casa dei testi si sceglie prima della fase 2; nasce il «decisore»; ogni agente può avere il suo modello, anche open-weight; la seconda GPU si propone per la milestone 2; l'11 novembre un router nel motore sceglie fra sei destinazioni, compresa la corsia T sui posti Claude Team (§10).
- **Sei scelte puntuali**, prese lungo il progetto e spiegate nella sezione 7:

| Tema | Scelta | Le altre strade |
|---|---|---|
| Chat di gruppo (§7.1) | Microsoft Teams per persone e agenti ([proposta §4.11](../PRESENTAZIONE-CEO.md)) | Slack solo per i clienti, dalla fase 3; Buzz in prova nel laboratorio, nella fase 4 ([proposta §4.11, §11](../PRESENTAZIONE-CEO.md)) |
| Trascrizione delle call (§7.2) | La trascrizione di Teams per le nostre call, dalla fase 1; un bot sul nostro server e la trascrizione in casa per le call dei clienti, dalla fase 3 ([proposta, appendice A, J5](../PRESENTAZIONE-CEO.md)) | Recall.ai in cloud, scelto nel primo giro: esce ([proposta §1](../PRESENTAZIONE-CEO.md)); Fireflies era già scartato ([ricerca/22 §9](../ricerca/22-architettura-scelta.md)) |
| Voce di Andrea (§7.3) | Voce e conversazione sul nostro server, con una linea telefonica italiana, dalla fase 5 ([proposta §11](../PRESENTAZIONE-CEO.md)) | ElevenLabs con un numero Twilio, in cloud: esce ([proposta §1](../PRESENTAZIONE-CEO.md)); in ultima istanza resta una voce in cloud, come eccezione decisa dai CEO ([proposta §13](../PRESENTAZIONE-CEO.md)) |
| Seconda GPU (§7.4) | RTX PRO 2000 Blackwell da 16 GB, scelta da Michele ([proposta §6.4](../PRESENTAZIONE-CEO.md)) | RTX 2000 Ada (la nostra proposta di ottobre), RTX A2000, L4 ([ricerca/32 §4.7](../ricerca/32-hardware-e-upgrade.md)) |
| UPS (§7.5) | HPE R1500 G5 usato, 255 €, già comprato ([proposta §12.2](../PRESENTAZIONE-CEO.md)) | Eaton 5PX nuovo, 937-1.144 € ([proposta §12.2](../PRESENTAZIONE-CEO.md)) |
| Accesso da fuori (§7.6) | Una macchina Oracle Cloud a Milano, sul piano gratuito ([proposta §14, decisione 7](../PRESENTAZIONE-CEO.md)) | Un server virtuale in affitto a 6,49 € al mese, come riserva; l'IP fisso con porte aperte ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)) |

*Superato in parte dal terzo giro, vedi §9 e §10.* Tre righe della tabella hanno oggi tempi o regole diversi:
- **la voce di Andrea** non aspetta più una decisione dei CEO: Andrea è accettato dal gruppo di progetto, parte dalla fase 5 o dalla 3 con lead vere, e lavora a L3 solo dopo il parere legale, il consenso registrato e 50 chiamate di prova ([ADR-0008, revisione del 10 novembre](adr/0008-andrea-centralino.md));
- **Buzz** non aspetta la fase 4: si collega alla bacheca degli agenti e si prova subito dopo la milestone 1, sul banco di prova e con dati verdi ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). Dal 12 novembre la prova aspetta il sì di Michele e una macchina Linux con Docker ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md));
- **la seconda GPU** resta la RTX PRO 2000 Blackwell da 16 GB, ma la proposta a Michele è comprarla per la milestone 2, anche a 1.100 €, senza aspettare che scenda sotto i 1.000 € ([ADR-0014, seconda revisione del 10 novembre](adr/0014-seconda-gpu-blackwell.md)).

## 1. Come leggere i confronti

- **Chi scrive e chi giudica.** Nel secondo giro le tre architetture sono state scritte da agenti AI separati, dentro il board di Michele, e valutate da quattro agenti giudici, ognuno con una lente ([proposta §5.7](../PRESENTAZIONE-CEO.md)). Il primo giro, prima del board, aveva seguito lo stesso metodo: sette proposte indipendenti, valutate dagli stessi quattro tipi di giudici ([proposta, appendice B](../PRESENTAZIONE-CEO.md); [ricerca/20-C, intestazione](../ricerca/20-proposta-C-grokbot.md)).
- **Le quattro lenti.** La visione di Alberto, cioè quanto si realizza l'idea intera; la lente commerciale di Alessandro; quella tecnica di Michele; sicurezza e privacy ([proposta §5.7](../PRESENTAZIONE-CEO.md)). Sono agenti che ragionano con quella lente, non le persone.
- **I criteri.** Ogni giudice dà da 0 a 10 punti su sei criteri: copertura della visione, tempo al valore, costo, affidabilità e manutenzione, sicurezza e privacy, aderenza al board di Michele. Un giudice dà al massimo 60 punti, i quattro insieme 240 ([proposta, appendice B](../PRESENTAZIONE-CEO.md)). Nel primo giro, prima del board, il sesto criterio era l'indipendenza: per esempio una licenza aperta e la libertà di scegliere il modello ([ricerca/21 CPTO §1, §2](../ricerca/21-giudizio-cpto.md)).
- **Un metodo, non un verdetto.** "È un metodo per mettere alla prova la scelta prima di portarvela, non un verdetto" ([proposta §5.7](../PRESENTAZIONE-CEO.md)).
- **I giorni non si confrontano a occhio.** Ogni proposta contava in modo diverso il lavoro sul contenuto dei singoli agenti ([ricerca/36 §2.4](../ricerca/36-architettura-v2.md)). La stima che vale è quella della [proposta §15](../PRESENTAZIONE-CEO.md). *Superato dal terzo giro: con le due corsie e la corsia S anticipata la stima va rifatta con Mattia, pezzo per pezzo; vedi §9.9 e [ADR-0021](adr/0021-motore-a-due-corsie.md).*
- **Il terzo giro ha un metro diverso.** I voti sono pesati e il totale è su 100, non su 240; lo spiega il §9.2.

## 2. Primo giro, 24 ottobre: sette architetture

Le ipotesi di allora erano diverse da oggi: Slack come chat di tutti, Notion come memoria scritta e diversi servizi in cloud, fra cui Recall.ai per registrare le call ed ElevenLabs per la voce di Andrea, l'agente vocale che richiama le lead ([ricerca/22 §2](../ricerca/22-architettura-scelta.md); [proposta, appendice B](../PRESENTAZIONE-CEO.md)).

### 2.1 I punteggi

| Proposta | Visione | Commerciale | Tecnica | Privacy | Totale su 240 |
|---|---|---|---|---|---|
| A. Hermes con il Cancello | 41 | 40 | 41 | 37 | **159** |
| F. Paperclip | 37 | 38 | 36 | 37,5 | 148,5 |
| G. Ibrido libero | 37 | 34 | 36 | 36,5 | 143,5 |
| B. buzz di Block | 36 | 33 | 35 | 36,5 | 140,5 |
| E. Claude-native | 34 | 31 | 37 | 38 | 140 |
| C. Grok Bot | 27 | 28 | 30 | 28 | 113 |
| D. OpenAI Dots | 26 | 25 | 27 | 27 | 105 |

Fonte: [proposta, appendice B](../PRESENTAZIONE-CEO.md). I quattro giudizi completi: [visione](../ricerca/21-giudizio-visione.md), [commerciale](../ricerca/21-giudizio-ceo.md), [tecnica](../ricerca/21-giudizio-cpto.md), [privacy](../ricerca/21-giudizio-compliance.md).

### 2.2 Dove si sono separate

La tabella somma i voti dei quattro giudici per ogni criterio, quindi ogni casella vale al massimo 40. I voti vengono dalle tabelle dei quattro giudizi del 24 ottobre ([visione §1](../ricerca/21-giudizio-visione.md), [commerciale §1](../ricerca/21-giudizio-ceo.md), [tecnica §1](../ricerca/21-giudizio-cpto.md), [privacy §1](../ricerca/21-giudizio-compliance.md)); in grassetto il migliore di ogni colonna.

| Proposta | Copertura della visione | Tempo al valore | Costo | Affidabilità e manutenzione | Sicurezza e privacy | Indipendenza |
|---|---|---|---|---|---|---|
| A. Hermes con il Cancello | 32 | 22 | **27,5** | 20 | 26 | 31,5 |
| F. Paperclip | 31 | 23,5 | 24 | 18 | 21 | 31 |
| G. Ibrido libero | **34,5** | 22 | 24,5 | 13 | 21 | 28,5 |
| B. buzz di Block | 27,5 | 20 | 25,5 | 13 | 22,5 | **32** |
| E. Claude-native | 29,5 | 14 | 20,5 | **21,5** | **32** | 22,5 |
| C. Grok Bot | 26 | **29,5** | 17,5 | 19 | 11,5 | 9,5 |
| D. OpenAI Dots | 21 | 24 | 15,5 | 17 | 15,5 | 12 |

- **A ha vinto per equilibrio.** Era prima solo nel costo, ma seconda in copertura, affidabilità, sicurezza e indipendenza.
- **La Claude-native (E)** era la più sicura e la più affidabile, ma la più lenta a dare valore.
- **Grok Bot (C)** era la più veloce a dare valore, ma l'ultima per sicurezza e indipendenza.
- **L'ibrido (G)** copriva più di tutte sulla carta, ma era fra le meno affidabili.

### 2.3 Le sette architetture, una per una

#### A. Hermes con il Cancello: 159 punti, prima

- **L'idea.** Hermes Agent, open source di Nous Research con licenza MIT (una licenza che permette anche l'uso commerciale), ragiona e smista il lavoro fra profili con nome, con una bacheca dei compiti, routine e il collegamento a Slack. Il Cancello, un nostro servizio, è l'unico che agisce verso l'esterno ([ricerca/20-A §1](../ricerca/20-proposta-A-hermes.md); [ricerca/22 §1](../ricerca/22-architettura-scelta.md)).
- **A favore.** I pezzi che l'idea chiede sono già pronti; dati e memoria restano sul server; se Hermes delude si cambia solo l'orchestratore, mentre Cancello, memoria e ingressi restano ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)).
- **Contro.** Hermes si dichiara "a single-tenant personal agent": è pensato per un solo utente, chi può scrivergli ha la stessa fiducia, e permessi diversi per persona chiedono istanze separate ([ricerca/10 §5](../ricerca/10-hermes-agent.md)). Con più profili sullo stesso gateway, il processo che collega i profili ai canali di chat, erano segnalate conversazioni finite al profilo sbagliato ([ricerca/10 §6](../ricerca/10-hermes-agent.md)). In dieci giorni erano uscite cinque patch, e le issue aperte, cioè le segnalazioni sul repository, erano più di 5.000 ([ricerca/10 §1](../ricerca/10-hermes-agent.md)).
- **Esito.** Vince il primo giro, con una decisione alla settimana 8: se anche una sola conversazione finisce al profilo sbagliato, si passa a un motore nostro sull'Agent SDK ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)).

#### F. Paperclip: 148,5 punti, seconda

- **L'idea.** Paperclip, open source con licenza MIT, fa da piano di controllo degli agenti: organigramma, budget per agente con stop al 100 %, approvazioni imposte dal programma e non dal prompt, routine e adattatori per Claude Code, Codex e Hermes ([ricerca/12 §0](../ricerca/12-altre-piattaforme.md)). Nella proposta il lavoro lo fanno lavoratori collegati, come Claude Code con la chiave API ([ricerca/20-F §1](../ricerca/20-proposta-F-paperclip.md)).
- **A favore.** La governance che serve per arrivare a cento agenti è già pronta, mentre con Hermes organigramma e banca dei token andrebbero costruiti a mano ([ricerca/21 visione §6](../ricerca/21-giudizio-visione.md); [ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)).
- **Contro.** Sei avvisi di sicurezza critici nel 2026, fra cui un'esecuzione di codice da remoto senza autenticazione e un agente che ha ereditato l'accesso a Gmail e ha mandato email vere ([ricerca/20-F §5](../ricerca/20-proposta-F-paperclip.md); [ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)). È governance senza cervello: memoria e lavoro degli agenti restano da costruire ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)).
- **Esito.** Allora restava un innesto da provare oltre i 25 agenti ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)). Oggi è una prova nella fase 6, sul banco di prova del laboratorio ([proposta §4.12, §5.2, §11](../PRESENTAZIONE-CEO.md)).

#### G. Ibrido libero: 143,5 punti, terza

- **L'idea.** Per ogni livello il pezzo più forte: Slack Pro con Claude Tag (Claude che risponde dentro la chat) come casa comune; Paperclip per il controllo; n8n, uno strumento di automazioni a orario e via webhook, per i flussi fissi; come lavoratori l'Agent SDK, i Managed Agents (agenti ospitati da Anthropic) e Hermes; come memoria Notion e un database vettoriale, cioè un database che cerca per significato ([ricerca/20-G §1](../ricerca/20-proposta-G-ibrido.md)).
- **A favore.** La copertura più alta sulla carta e una riserva del 30 % sulle stime, "la stima più onesta del lotto" ([ricerca/21 visione §3](../ricerca/21-giudizio-visione.md)).
- **Contro.** Somma i rischi di Paperclip, Hermes e n8n: cinque componenti open source e otto servizi per un solo amministratore ([ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)). Il costo dichiarato era sottostimato, e la licenza di n8n vieta di rivenderlo come servizio ([ricerca/21 CEO §2, §3](../ricerca/21-giudizio-ceo.md)). La valutazione d'impatto sulla privacy sarebbe stata la più difficile da spiegare, con tre registri di approvazione ([ricerca/21 compliance §2](../ricerca/21-giudizio-compliance.md)).
- **Esito.** Se ne prendono le idee ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)). n8n allora restava fuori; oggi c'è, perché è nel board di Michele, per routine e integrazioni interne e mai per invii a clienti ([ricerca/25 §2, C27](../ricerca/25-board-michele-e-delta.md)). *Superato dal terzo giro: orari ed eventi stanno nel motore e n8n è facoltativo; vedi §9 e [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md).*

#### B. buzz di Block: 140,5 punti, quarta

- **L'idea.** Un solo spazio di lavoro sul nostro server, buzz, dove persone e agenti stanno negli stessi canali e ogni agente è un membro con nome, che si delega il lavoro con una menzione. Buzz è la stanza, non il cervello: il cervello di ogni agente è Claude Code con la chiave API ([ricerca/20-B §1](../ricerca/20-proposta-B-buzz.md)).
- **A favore.** Anche la chat resta in casa ([ricerca/21 compliance §2](../ricerca/21-giudizio-compliance.md)); gli agenti sono membri veri; la più indipendente del lotto (tabella del §2.2).
- **Contro.** È un prodotto prima della versione 1.0, con le approvazioni nei flussi di lavoro che falliscono e senza un freno ai giri, cioè un limite nel codice ai messaggi a catena fra agenti ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)). Se buzz si ferma, si ferma la chat di tutto il team ([ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)).
- **Esito.** Scartata come chat di tutti; resta un pilota interno ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)). Oggi è in prova come stanza degli agenti (§7.1). *Superato in parte dal terzo giro: la prova è anticipata a subito dopo la milestone 1; vedi §9 e [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md). Dal 12 novembre la prova aspetta il sì di Michele e una macchina Linux con Docker ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md)).*

#### E. Claude-native: 140 punti, quinta

- **L'idea.** Un servizio nostro, piccolo, decide chi può agire, chiede il sì, esegue, conta i token e traccia. Claude è la forza lavoro sulla chiave API: chiamate dirette per riassumere e classificare, sessioni dell'Agent SDK per i lavori a più passi. Le persone restano sui posti Claude Team ([ricerca/20-E §1](../ricerca/20-proposta-E-claude-native.md)).
- **A favore.** Per il giudice tecnico è la più solida su sicurezza e osservabilità ([ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)). Per il giudice della privacy è l'unica in cui i controlli che un cliente regolamentato chiede stanno in codice nostro e si possono mostrare, con un solo fornitore di modelli ([ricerca/21 compliance §2](../ricerca/21-giudizio-compliance.md)).
- **Contro.** È la più lenta: molto codice da scrivere e la chat fra agenti solo alla settimana 13 ([ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)). Al posto di Notion metteva un archivio di file Markdown in git, un passo indietro per due CEO non tecnici ([ricerca/21 CEO §3](../ricerca/21-giudizio-ceo.md)). La sua sicurezza sarebbe stata codice nostro mai andato in produzione, senza revisione esterna ([ricerca/21 compliance §5](../ricerca/21-giudizio-compliance.md)).
- **Esito.** Prima per la lente privacy e seconda per la lente tecnica; allora restava l'uscita prezzata ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)). Con il board di Michele è diventata il motore sull'Agent SDK ([proposta, appendice B](../PRESENTAZIONE-CEO.md)).

#### C. Grok Bot: 113 punti, sesta

- **L'idea.** I Bot di Grok, in abbonamento, fanno il lavoro che si vede; il server custodisce i dati e fa il lavoro che non deve uscire ([ricerca/20-C §1](../ricerca/20-proposta-C-grokbot.md)).
- **A favore.** La più veloce a dare valore: gli agenti sono un servizio già pronto, senza nulla da installare in casa ([ricerca/11 §1](../ricerca/11-grokbot.md)).
- **Contro.** I Bot girano solo sui computer cloud di Cursor, negli Stati Uniti, e il modello lo sceglie il servizio senza che l'utente lo veda ([ricerca/11 §1](../ricerca/11-grokbot.md)). Dal 13 al 19 ottobre la pagina di stato registrava cinque incidenti ([ricerca/11 §8](../ricerca/11-grokbot.md)). Le nostre regole operative vietano dati di clienti o lead su abbonamenti consumer o in beta ([ricerca/16 §6, regola 7](../ricerca/16-gdpr-ai-act-e-regole.md)). Sulla stessa base di costo delle altre arrivava a circa 1.058 € al mese ([ricerca/21 CEO §2](../ricerca/21-giudizio-ceo.md)).
- **Esito.** Scartata ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)). Resta facoltativo un mese di prova su soli dati pubblici, circa 54 € una volta ([proposta §14, decisione 23](../PRESENTAZIONE-CEO.md)).

#### D. OpenAI Dots: 105 punti, settima

- **L'idea.** Gli agenti di OpenAI, Dots e Workspace Agents, fanno il lavoro operativo nel cloud; il server tiene dati, SersanOutreach (la nostra piattaforma outbound), memoria e trascrizione; Claude resta per il codice e i testi ([ricerca/20-D §1](../ricerca/20-proposta-D-openai-dots.md)).
- **A favore.** Agenti condivisi con un nome e un proprio utente in Slack, con le scritture che di default chiedono sempre conferma ([ricerca/20-D §1](../ricerca/20-proposta-D-openai-dots.md)).
- **Contro.** Workspace Agents non confermati nel Regno Unito e prezzo dei crediti OpenAI ignoto ([ricerca/21 visione §3](../ricerca/21-giudizio-visione.md)). La proposta scriveva insieme "i dati restano in casa" e "i dati operativi vanno negli USA" ([ricerca/21 CPTO §3](../ricerca/21-giudizio-cpto.md)). Costava circa 1.190 € al mese, più i crediti OpenAI ([ricerca/21 CEO §2](../ricerca/21-giudizio-ceo.md)).
- **Esito.** Scartata ([ricerca/22 §1](../ricerca/22-architettura-scelta.md)).

### 2.4 Cosa è uscito dal primo giro

A vince in tre lenti su quattro, visione, commerciale e tecnica, e nella somma. La lente privacy preferiva la Claude-native, di mezzo punto su Paperclip e di un punto su A ([ricerca/22 §1](../ricerca/22-architettura-scelta.md); [proposta, appendice B](../PRESENTAZIONE-CEO.md)). Il piano di allora prese dalle altre proposte e dai giudici alcune correzioni che sono ancora nel progetto ([ricerca/22 §1, §3](../ricerca/22-architettura-scelta.md)):

- **prima il funnel**, il percorso che porta da un contatto a un cliente: valore subito da ciò che è già pagato, come Claude Team e i server MCP di SersanOutreach (MCP è lo standard con cui un agente si collega a uno strumento), e dal marketing; Andrea e la pipeline pesata, cioè la probabilità di chiusura calcolata sullo storico, solo con dati veri;
- **una decisione alla settimana 8**, con criteri misurabili;
- **organigramma e banca dei token**, cioè i budget per agente e per persona, visibili ai CEO dalla fase 1 (da Paperclip);
- **i tre colori dei dati**, verde, giallo e rosso, scritti nel Cancello per decidere cosa può uscire dal server e verso chi (da Grok Bot);
- **chi legge testo di terzi non ha strumenti d'azione** (da buzz);
- **le riunioni dal vivo registrate dal telefono** (da Grok Bot, Claude-native e ibrido);
- **il follow-up solo verso il dominio del cliente** (da Dots);
- **una riserva sulle stime** (dall'ibrido).

Oggi le ritroviamo nella proposta: i tre colori al §5.6, la corsia senza strumenti per il testo di terzi al §9.2, il follow-up verso il dominio del cliente e le riunioni dal telefono nell'appendice A (voci B3 e J5), la riserva di circa un terzo al §15 ([proposta](../PRESENTAZIONE-CEO.md)).

### 2.5 I dissensi del primo giro

Ogni giudice ha scritto anche il suo dissenso più forte:

- **Visione.** Doveva vincere l'ibrido, o Paperclip. Con Hermes si costruiscono a mano proprio i pezzi che l'idea mette al centro, cioè la chat visibile fra agenti e persone, l'organigramma e la banca dei token per cento agenti, che Paperclip dà pronti ([ricerca/21 visione §6](../ricerca/21-giudizio-visione.md)).
- **Commerciale.** Il problema di SerSan non è l'orchestrazione, è il funnel: 11 lead, 0 meeting, l'email ferma per la compliance, nessun post dei founder. Prima 8-12 settimane con ciò che è già pagato, poi la piattaforma ([ricerca/21 CEO §6](../ricerca/21-giudizio-ceo.md)).
- **Tecnica.** Una volta costruito il Cancello, Hermes aggiunge poco e porta un progetto enorme da seguire per anni: circa 58.000 commit, più di 5.000 issue aperte, note di rilascio incomplete per scelta. Se anche un solo contesto finisce al profilo sbagliato, la scelta giusta è la Claude-native ([ricerca/21 CPTO §6](../ricerca/21-giudizio-cpto.md)).
- **Privacy.** La sicurezza della Claude-native è codice nostro mai andato in produzione, scritto da due persone senza revisione esterna, e arriva tardi ([ricerca/21 compliance §5](../ricerca/21-giudizio-compliance.md)).

Tre di questi temi sono tornati nel secondo giro e hanno cambiato il piano: il funnel prima di tutto, il motore sull'Agent SDK al posto di Hermes e la revisione esterna del codice di sicurezza (§4.4).

## 3. Cosa ha cambiato il board di Michele

Il board è il disegno dell'infrastruttura del server fatto da Michele, ed è vincolante per il progetto ([board di Michele](../allegati/infra/SerSan%20Infra%20Board.md); [ricerca/25, intestazione](../ricerca/25-board-michele-e-delta.md)). Rispetto al primo giro cambia la base in cinque punti ([ricerca/25, In breve](../ricerca/25-board-michele-e-delta.md)):

1. **Il cloud si restringe.** Restano M365 con Entra ID (l'identità aziendale di Microsoft), Claude Team, l'API di Anthropic dietro LiteLLM, Cloudflare per il DNS, GitHub, Supabase, Vercel, Jira, Instantly e uno spazio S3 facoltativo. Azure esce, e "tutto il resto dev'essere self hosted", cioè installato sul nostro server. Slack, Notion, Google Workspace, Recall.ai, ElevenLabs con Twilio, Hermes Cloud e altri servizi escono o diventano eccezioni da far approvare a Michele.
2. **L'hardware è completo e più grande del previsto.**
3. **La memoria cambia motore**: Qdrant per la ricerca, PostgreSQL 16, BookStack e Jira al posto di Notion, e Claude Team che interroga i documenti con i permessi di chi chiede.
4. **L'orchestratore va rivalutato**: Michele preferisce l'Agent SDK, e il board ha già LiteLLM (il proxy che passa le chiamate ai modelli e tiene i budget), n8n e Open WebUI (una chat web sui modelli), che coprono una parte di ciò che dava Hermes.
5. **I tempi si allineano alla roadmap del board**: lo strato AI arriva nella sua fase F4.

"Con il board di Michele il quadro è cambiato: tutto in casa, M365 al posto di Google e Slack, n8n e LiteLLM già previsti" ([proposta, appendice B](../PRESENTAZIONE-CEO.md)). Per questo il confronto sull'orchestratore è stato rifatto da capo.

## 4. Secondo giro, 25 ottobre: tre proposte dentro il board

### 4.1 Le tre proposte

#### Proposta 1. Il motore sull'Agent SDK

- **Cosa propone.** Un servizio nostro in TypeScript sull'Agent SDK, in una macchina dedicata agli agenti. Per ogni lavoro fa girare un processo Claude con il profilo dell'agente: regole, skill (le procedure scritte che l'agente sa usare), strumenti ammessi, chiave di LiteLLM e tetti di spesa. Accanto: n8n per orari e webhook, LiteLLM come banca dei token, il Cancello, PostgreSQL e Qdrant come memoria, BookStack per regole e processi, i server MCP e Teams come chat. Restano da scrivere sei pezzi nostri: il runner, cioè il programma che lancia i lavori, con il registro dei profili; il ponte verso il Cancello; la bacheca dei compiti fra agenti con il freno ai giri; la "Porta chat", il nostro bot che collega gli agenti a Teams (e, con lo stesso codice, a Telegram, WhatsApp e Slack); il Cancello stesso e alcuni server MCP ([ricerca/34-1, In breve](../ricerca/34-proposta-1-agent-sdk.md)).
- **Punto forte.** È l'unica che porta tutte le 57 figure su un solo motore, con una sola bacheca, una sola memoria e una sola Porta, e ogni agente lavora con l'identità della persona per cui lavora ([ricerca/35 visione, In breve](../ricerca/35-giudizio-visione.md)).
- **Punto debole.** Dà valore tardi, con il pilota alla settimana 16 ([ricerca/35 CPTO, In breve](../ricerca/35-giudizio-cpto.md)), e la sua sicurezza dipende da codice nostro scritto da due persone a tempo parziale, senza revisione esterna ([ricerca/35 sicurezza §9](../ricerca/35-giudizio-sicurezza.md)).

#### Proposta 2. Hermes sul nostro server

- **Cosa propone.** Hermes in sei istanze separate sul server, una per confine di fiducia: commerciale, marketing, progetti, direzione, amministrazione e assistente personale. Dei 57 agenti, 50 sono profili Hermes e 7 sono codice o servizi. Claude passa da LiteLLM; il Cancello ha un suo bot Teams per le carte di approvazione ([ricerca/34-2, In breve](../ricerca/34-proposta-2-hermes-self-hosted.md)).
- **Punto forte.** Porta pronti i pezzi che con l'Agent SDK vanno scritti: profili con nome, persona e skill proprie; una bacheca fra profili con dispatcher, corsia di revisione e blocco "serve un umano"; skill che l'agente scrive e migliora; i canali Teams, Telegram, WhatsApp e Slack. Il primo bot che risponde in Teams arriva in giorni ([ricerca/34-2, In breve](../ricerca/34-proposta-2-hermes-self-hosted.md)).
- **Punto debole.** Il gateway unico di Hermes ha 276 problemi aperti, 9 di sicurezza e 0 risolti; nel 2026 il database degli avvisi di sicurezza di GitHub conta almeno 45 avvisi su Hermes; Hermes passa alla memoria solo un valore fisso o il nome del profilo, quindi i permessi valgono per istanza e non per persona ([ricerca/34-2, In breve](../ricerca/34-proposta-2-hermes-self-hosted.md); [ricerca/36 §1.4](../ricerca/36-architettura-v2.md)).

#### Proposta 3. Claude Team al centro

- **Cosa propone.** Le quattro persone lavorano in Claude Team, l'abbonamento a Claude che SerSan ha già, e da lì usano memoria e strumenti dell'azienda attraverso connettori MCP verso il server. Dietro le quinte girano lavori programmati in n8n. L'Agent SDK entra solo dove serve un agente vero: brief, offerta, agenda, operatore outbound e pochi altri. Ciò che esce passa dal Cancello ([ricerca/34-3, In breve](../ricerca/34-proposta-3-claude-team-e-mcp.md)).
- **Punto forte.** Dà valore dalla prima settimana senza aspettare il server, con meno pezzi sempre accesi, perché usa ciò che SerSan paga già ([ricerca/34-3, In breve](../ricerca/34-proposta-3-claude-team-e-mcp.md)).
- **Punto debole.** Da sola copre per intero 59 voci della visione su 90 ([ricerca/34-3, In breve](../ricerca/34-proposta-3-claude-team-e-mcp.md)). Gli agenti con strumenti sono 9-10 su 57: dieci figure diventano skill che una persona apre in Claude Team e 29 diventano flussi fissi. I compiti programmati di Claude Team appartengono a un solo account, e il piano Team non ha log di audit, conservazione personalizzata né Compliance API. Espone sei endpoint MCP su internet invece di uno, e mette Cancello e motore nella stessa macchina ([ricerca/36 §1.3](../ricerca/36-architettura-v2.md)).

### 4.2 I punteggi

| Proposta | Visione | Commerciale | Tecnica | Sicurezza e privacy | Totale su 240 |
|---|---|---|---|---|---|
| 1. Motore sull'Agent SDK | 43 | 42 | 44 | 42,5 | **171,5** |
| 3. Claude Team al centro | 41 | 45 | 42 | 42 | 170 |
| 2. Hermes sul nostro server | 35 | 34 | 34 | 34 | 137 |

Fonte: [proposta §5.7 e appendice B](../PRESENTAZIONE-CEO.md). I quattro giudizi completi: [visione](../ricerca/35-giudizio-visione.md), [commerciale](../ricerca/35-giudizio-ceo.md), [tecnica](../ricerca/35-giudizio-cpto.md), [sicurezza](../ricerca/35-giudizio-sicurezza.md). Il motore vince in tre lenti su quattro; la lente commerciale preferisce di poco Claude Team al centro, perché dà valore prima ([proposta, appendice B](../PRESENTAZIONE-CEO.md)).

### 4.3 Dove si sono separate

Somma dei quattro giudici per ogni criterio, su 40, dalle tabelle dei giudizi del 25 ottobre ([visione §1](../ricerca/35-giudizio-visione.md), [commerciale §1](../ricerca/35-giudizio-ceo.md), [tecnica §1](../ricerca/35-giudizio-cpto.md), [sicurezza §1](../ricerca/35-giudizio-sicurezza.md)); in grassetto il migliore di ogni riga.

| Criterio | 1. Motore sull'Agent SDK | 3. Claude Team al centro | 2. Hermes sul nostro server |
|---|---|---|---|
| Copertura della visione | **36** | 26 | 33,5 |
| Tempo al valore | 23 | **34** | 26 |
| Costo | 23,5 | **28** | 23 |
| Affidabilità e manutenzione | **27,5** | 25 | 16 |
| Sicurezza e privacy | **32** | 24 | 18,5 |
| Aderenza al board di Michele | 29,5 | **33** | 20 |
| **Totale** | **171,5** | 170 | 137 |

- Il motore è avanti su copertura della visione, affidabilità e sicurezza: tutti e quattro i giudici gli danno 9 su 10 per la copertura e 8 su 10 per la sicurezza.
- Claude Team al centro è avanti su tempo al valore, costo e aderenza al board. Il suo vantaggio più largo è il tempo al valore, ed è proprio quello che il piano ha preso con la sua fase zero ([ricerca/36 §1.1](../ricerca/36-architettura-v2.md)).
- Hermes è ultimo su affidabilità, sicurezza e aderenza al board, e di mezzo punto anche sul costo; per l'affidabilità tutti e quattro i giudici gli danno 4 su 10.

### 4.4 I dissensi presi sul serio

Dalla [proposta, appendice B](../PRESENTAZIONE-CEO.md):

- **Lente commerciale**: "il problema commerciale di oggi non è l'orchestratore, è il funnel vuoto". Da qui la decisione sull'email e la casella attiva nella fase 0, e i criteri commerciali alla verifica della settimana 8.
- **Lente tecnica**: "il collo di bottiglia non è il motore, è chi amministra il server". Da qui il tetto ai servizi nuovi prima della fase F4 del board, un responsabile delle patch per ogni servizio e il pilota su un banco di prova che non riordina il board.
- **Lente sicurezza e privacy**: "la sicurezza della proposta scelta dipende da codice scritto su misura che nessuno ha ancora rivisto". Da qui la revisione esterna entro la settimana 21, le carte legate al testo e la chiave FIDO2, una chiave di sicurezza fisica, per le azioni più delicate. *Superato dal terzo giro: la revisione esterna diventa facoltativa e la FIDO2 esce dalle carte, mentre resta per l'accesso al board; vedi §9 e [ADR-0023](adr/0023-protezioni-essenziali.md).*
- **Lente visione**: "una proposta che trasforma gli agenti in strumenti da aprire a mano tradisce l'idea". Da qui tutte le 57 figure come agenti veri, i nove bot di squadra e Buzz collegato alla stessa bacheca.

### 4.5 Cosa è entrato nel piano dalle altre due

Dalla **Proposta 3, Claude Team al centro** ([ricerca/36 §1.5](../ricerca/36-architettura-v2.md)):

- Claude Team per tutti dalla prima settimana, con progetti per squadra, skill dell'organizzazione e connettori di Jira e M365 in sola lettura: è la fase 0;
- la divisione dei lavori in tipi (chiamata a schema senza strumenti, sessione con strumenti, servizio), che riduce le sessioni con strumenti senza togliere a nessuna figura il suo agente;
- Claude Team come finestra delle persone, con memoria, bacheca e Cancello che restano sul server;
- un tetto iniziale di 6 sessioni insieme e la soglia dei 5 GB liberi per comprare la RAM.

Dalla **Proposta 2, Hermes sul nostro server** ([ricerca/36 §1.5](../ricerca/36-architettura-v2.md)):

- il modello della bacheca dei compiti fra agenti (§6);
- le regole di Pangolin che aprono senza login solo il percorso del bot di Teams, e il filtro sugli indirizzi di Anthropic davanti all'endpoint della memoria, come controllo in più e non come autenticazione ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md));
- il limite per cui il banco di prova salva solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata ([proposta §11](../PRESENTAZIONE-CEO.md));
- le uscite scritte con "cosa si perde" e "cosa resta" ([ricerca/36 §12](../ricerca/36-architettura-v2.md)).

## 5. Perché ha vinto il motore sull'Agent SDK

- **Vince in tre lenti su quattro**: visione, tecnica, sicurezza e privacy. La lente commerciale preferisce di poco Claude Team al centro, perché dà valore prima: per questo la sua fase zero è entrata nel piano ([proposta, appendice B](../PRESENTAZIONE-CEO.md)).
- **Tiene intera l'idea.** Tutte le 57 figure sono agenti veri su un solo motore, con una bacheca, una memoria, un Cancello e una sola Porta verso Teams, Telegram, WhatsApp e Slack ([ricerca/36 §1.2](../ricerca/36-architettura-v2.md)).
- **La persona arriva fino alla memoria.** L'Agent SDK passa a ogni server MCP le intestazioni HTTP, cioè i dati che accompagnano ogni richiesta, che decidiamo noi a ogni chiamata: così, quando un agente lavora per Alessandro, la memoria gli mostra solo ciò che Alessandro può vedere, come chiede il board con i "permessi per utente". Il coaching resta a chi ha fatto la call e i dati di ciascuno restano suoi ([proposta §5.3](../PRESENTAZIONE-CEO.md); [ricerca/36 §1.2](../ricerca/36-architettura-v2.md)). Hermes passa solo un valore fisso o il nome del profilo ([ricerca/36 §2.1](../ricerca/36-architettura-v2.md)).
- **Il Cancello si aggancia dentro il motore.** Prima di ogni azione il motore chiede al Cancello con un hook, un controllo che l'SDK chiama prima di ogni strumento; se il Cancello non risponde in tempo, l'azione è bloccata ([proposta §5.3](../PRESENTAZIONE-CEO.md); [ricerca/36 §1.2](../ricerca/36-architettura-v2.md)). *Superato il 12 novembre per la strada, non per la garanzia: a chiamare il Cancello è lo strumento che propone, `proponi_azione`, dentro il processo del runner, e il gancio prima degli strumenti nega soltanto ([ADR-0001, revisione del 12 novembre 2026](adr/0001-motore-agent-sdk.md); [ADR-0029](adr/0029-corsia-s-sessioni-a-giri.md)).*
- **Usa quello che Michele ha già.** Orari e integrazioni li fa n8n, i budget li tiene LiteLLM, la memoria sta in PostgreSQL, Qdrant e BookStack: il motore non duplica nulla ([proposta §5.3](../PRESENTAZIONE-CEO.md)). Con Hermes sarebbero doppi routine, webhook, budget, memoria, chat web, osservabilità e segreti ([ricerca/36 §2.1](../ricerca/36-architettura-v2.md)). *Superato dal terzo giro per gli orari: la sveglia sta nel motore e n8n è facoltativo ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)); la casa dei testi, BookStack o file Markdown in git, si sceglie prima della fase 2 ([ADR-0005, revisione del 10 novembre](adr/0005-memoria-postgres-qdrant-bookstack.md)). Vedi §9 e §10.*
- **Segue la richiesta di Michele**, che preferisce questa strada a Hermes ([proposta §1, §5.7](../PRESENTAZIONE-CEO.md)).
- **Costa uguale di licenza**: zero in entrambi i casi; si paga solo l'API ([proposta §12.1](../PRESENTAZIONE-CEO.md)).
- **Il prezzo della scelta.** La bacheca fra agenti, i profili con nome e i bot per le chat li scriviamo noi, mentre Hermes li darebbe pronti: sono giorni messi nel piano ([proposta §5.3](../PRESENTAZIONE-CEO.md)). E i bug di canali, bacheca e profili diventano nostri ([ricerca/36 §2.2](../ricerca/36-architettura-v2.md)).

**Hermes e motore sull'Agent SDK, fatto per fatto**, al 25 ottobre 2026 ([ricerca/36 §2.1](../ricerca/36-architettura-v2.md)):

| Criterio | Hermes sul nostro server | Motore sull'Agent SDK |
|---|---|---|
| Versione | v0.22.5 del 23/10/2026; la v0.23 non ancora uscita | TypeScript 0.3.310 con Claude Code 2.1.310 |
| Ritmo dei rilasci | 44 release dal 12/03 al 23/10/2026 | 333 versioni TypeScript dal 27/09/2025 |
| Pronto oggi | canali (Teams, Telegram, WhatsApp e più di 25 altri), profili con nome, bacheca, skill che crescono, routine | ciclo dell'agente, strumenti, hook, permessi, sessioni riprendibili, sottoagenti, MCP, skill; niente orari, bacheca, profili persistenti né chat di gruppo |
| Primo bot in Teams | in giorni | la Porta è da scrivere |
| Aggancio al Cancello | un plugin che blocca e, se va in timeout, chiude per sicurezza, con una finestra di 60 secondi da chiarire | un hook dentro il motore: in timeout la chiamata è bloccata |
| Identità verso la memoria | un valore fisso o il nome del profilo | intestazioni scelte da noi a ogni chiamata: la persona arriva ai permessi |
| Bacheca | pronta, ma su un solo host | da scrivere in PostgreSQL |
| Isolamento | un solo gateway per tutti i profili dalla v0.22.0 | un processo per lavoro, con cartella, configurazione e chiave per famiglia |
| Problemi noti | 276 problemi aperti sul gateway, 9 di sicurezza, 0 risolti; almeno 45 avvisi di sicurezza nel 2026 | nessun bug noto di sessioni scambiate; due trappole di configurazione, verificate e corrette nel disegno ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)) |
| Doppioni con il board | routine, webhook, budget, memoria, chat web, osservabilità, segreti | nessuno |
| Giorni per integrare il motore (stime) | 22,5 di base, 26-33 con la riserva | 21 di base, circa 27 con la riserva |
| Manutenzione | 1,5-2,5 giorni al mese | un aggiornamento ogni due settimane, dopo 10 scenari di prova |
| Licenza | MIT, 0 € | termini commerciali di Anthropic, 0 €; si paga l'API |

## 6. Cosa resta di Hermes

- **Una porta aperta, con i numeri.** Se il motore non regge alle verifiche delle settimane 8 e 21, proviamo Hermes sullo stesso banco di prova, con gli stessi scenari, e decidiamo sui numeri ([proposta §5.7, §11](../PRESENTAZIONE-CEO.md)). *Superato in parte dal terzo giro: Hermes resta via d'uscita già prezzata e diventa anche un pilota in laboratorio da 6-8 giorni di sviluppo; alla settimana 8 il criterio «nessun effetto senza una carta» diventa «nessun effetto fuori dal suo livello», e alla 21 la revisione esterna esce dai criteri. Vedi §9 e [ADR-0012, revisione del 10 novembre](adr/0012-hermes-uscita.md).*
- **Quanto costa cambiare.** Una prova di Hermes costa 6-8 giorni; usarlo al posto del motore 26-33 giorni con la riserva. Cancello, memoria, server MCP, bot e skill restano uguali ([proposta §5.7, §15](../PRESENTAZIONE-CEO.md)); le skill hanno lo stesso formato `SKILL.md` nei due casi ([ricerca/36 §2.4](../ricerca/36-architettura-v2.md)).
- **Come sarebbe la prova.** Due o tre profili sul banco di prova del laboratorio, Telegram in polling (il bot va a prendere i messaggi, senza aprire porte), strumenti MCP in sola lettura, solo dati verdi ([ricerca/36 §2.4](../ricerca/36-architettura-v2.md)).
- **Quando diventa l'orchestratore.** Solo se chiude i suoi problemi di sicurezza ([proposta §5.7](../PRESENTAZIONE-CEO.md)). In concreto, quattro condizioni insieme: la versione 0.23 uscita con le note complete; chiuse sul ramo principale le righe di sicurezza MSG-43, GW-41, KB-10 e HR-6 della scheda #143547, la segnalazione su GitHub che raccoglie i problemi del gateway unico ([ricerca/10 §6](../ricerca/10-hermes-agent.md)); chiuso il bug dei documenti su Teams (#113578); un aggiornamento che passa i 10 scenari senza interventi a mano ([ricerca/36 §2.4](../ricerca/36-architettura-v2.md); [ricerca/27 §11](../ricerca/27-hermes-self-hosted.md)).
- **Le sue idee migliori sono già nel piano.** La nostra bacheca prende da quella di Hermes la corsia di revisione fra agenti, il blocco "serve un umano" con sblocco dalla chat, lo stop dopo due fallimenti di fila, il rifiuto dei cicli e il dispatcher che riprende i compiti fermi ([ricerca/36 §1.5](../ricerca/36-architettura-v2.md)). E, come in Hermes, gli agenti propongono skill nuove in una cartella "proposte", che una persona approva con una PR, cioè una modifica proposta al codice ([proposta, appendice A, A6](../PRESENTAZIONE-CEO.md); [ricerca/35 visione §8](../ricerca/35-giudizio-visione.md)).
- **Dove resta migliore, detto chiaramente.** È pronto oggi, ha una comunità enorme e un catalogo di plugin che cresce ogni settimana ([ricerca/36 §2.2](../ricerca/36-architettura-v2.md)).

## 7. Le alternative decise lungo il progetto

### 7.1 La chat di gruppo: Teams, Slack, Buzz

Cosa deve fare la chat: stanze per squadra con gli agenti come membri con un nome, accesso dal telefono, la chat fra agenti leggibile da noi, approvazioni con l'identità certa di chi approva, canali con i clienti ([ricerca/28 §1](../ricerca/28-chat-di-gruppo-self-hosted.md)).

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| **Microsoft Teams**, con la nostra "Porta chat", il bot che collega gli agenti | Già pagato con M365: 0 € in più se il piano lo include. La stessa identità dell'accesso da fuori: Entra con MFA e chiave FIDO2. App mature per computer e telefono. Carte con pulsanti (Adaptive Card) che dicono al bot chi ha premuto. Canali con i clienti. Il tenant lo gestisce già Michele ([ricerca/28 §2.6](../ricerca/28-chat-di-gruppo-self-hosted.md)) | Una rotta pubblica in più, perché il bot riceve i messaggi da Microsoft su un indirizzo HTTPS ([ricerca/28 §1](../ricerca/28-chat-di-gruppo-self-hosted.md)). Una piattaforma che Microsoft cambia spesso; Claude Tag non c'è ancora; ogni bot è un'app, quindi conviene un bot per squadra ([ricerca/28 §2.6](../ricerca/28-chat-di-gruppo-self-hosted.md)). La registrazione del bot senza Azure può dare errori ([proposta §13](../PRESENTAZIONE-CEO.md)) | **Casa comune.** Un team "SerSan Agent OS" con un canale per squadra, "Approvazioni", "Agenti", "Ingresso", "Call di vendita", "Bandi" e un canale privato per cliente; un bot per ognuna delle nove squadre; le carte sul telefono ([proposta §4.11](../PRESENTAZIONE-CEO.md)). Se la registrazione non funziona: un Azure Bot gratuito senza macchine accese, o la pagina del Cancello con gli avvisi in Teams ([proposta §13](../PRESENTAZIONE-CEO.md)). Se Teams manca dal piano M365: 6-14 € al mese ([proposta §14, decisione 18](../PRESENTAZIONE-CEO.md)) |
| **Slack** | Nel primo giro era la casa comune: con il Socket Mode apre solo connessioni in uscita, senza porte aperte; Slack Connect per i canali dei clienti; Claude Tag dentro Slack ([ricerca/22 §2](../ricerca/22-architettura-scelta.md)). Hermes, Paperclip e Claude Tag ci si collegano già ([ricerca/20-G §1](../ricerca/20-proposta-G-ibrido.md)) | Non è fra i servizi che il board tiene in cloud ([ricerca/25 §2, C01](../ricerca/25-board-michele-e-delta.md)). Costava 27 € al mese di Slack Pro più 44,67 € di Claude in Slack ([ricerca/28 §8.4](../ricerca/28-chat-di-gruppo-self-hosted.md)), per una seconda chat accanto a Teams | **Esce come chat interna**, insieme a Claude in Slack ([proposta §12.1](../PRESENTAZIONE-CEO.md)). Resta per i clienti che lavorano lì, dalla fase 3, con lo stesso codice degli altri canali: 0 o 27 € al mese ([proposta §4.11; §14, decisione 8](../PRESENTAZIONE-CEO.md)) |
| **Buzz** di Block, la chat open source fatta per persone e agenti | Il modello dell'idea: agenti membri veri, con nome e proprietario. Licenza Apache-2.0, si installa in casa. Claude Code ci entra con un adattatore costruito sull'Agent SDK ([ricerca/28 §3](../ricerca/28-chat-di-gruppo-self-hosted.md)) | Al 25 ottobre era alla versione 0.5.28, prima della 1.0; approvazioni non ancora collegate; nessun ponte verso Teams, Telegram o WhatsApp ([ricerca/28 §3](../ricerca/28-chat-di-gruppo-self-hosted.md)). Perde alcune risposte senza segnalarlo ([proposta §4.11](../PRESENTAZIONE-CEO.md)). Cyber Essentials, la certificazione di sicurezza britannica che il board segue, chiede software supportato ([ricerca/25 §2, C19](../ricerca/25-board-michele-e-delta.md)) | **In prova** nella sandbox del laboratorio (Experimental-2) come stanza degli agenti, collegata alla stessa bacheca, nella fase 4: circa 6 giorni ([proposta §11, §15; appendice A, J9](../PRESENTAZIONE-CEO.md)). Esce dal laboratorio quando non perde più risposte e ha approvazioni funzionanti; se allora è più comoda di Teams, diventa la casa comune. Intanto la stanza degli agenti è il canale "Agenti" di Teams ([proposta §4.11, §13](../PRESENTAZIONE-CEO.md)). *Superato dal terzo giro: Buzz si prova subito dopo la milestone 1, collegato alla bacheca; se regge diventa la casa degli agenti, mentre Teams resta per le persone e per le approvazioni. Fino ad allora gli agenti hanno gruppi di chat in Teams: uno per squadra, uno per cliente e uno comune, «Agenti». Vedi §9 e [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md). Rivisto il 12 novembre: i gruppi stanno nella Sala di controllo finché non c'è il bot di Teams o Buzz, e Buzz si prova quando Michele lo ammette e c'è una macchina Linux con Docker ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md))* |

- **Gli altri canali.** Dalla fase 3 gli stessi agenti arrivano su Telegram, per gli avvisi, e su WhatsApp e Slack, soprattutto per i clienti; le approvazioni restano in Teams, dove il Cancello riconosce chi preme ([proposta §2.1, §4.11](../PRESENTAZIONE-CEO.md)). WhatsApp solo con l'API ufficiale di Meta e un numero dedicato, perché le soluzioni non ufficiali portano al blocco del numero ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **Le altre chat valutate.** Mattermost, la chat self-hosted più matura, resta il piano B se un giorno si esce da Teams: per notifiche affidabili sul telefono servirebbe il piano a pagamento, e sarebbe una seconda chat accanto a Teams. Matrix con Element è scartata: chiede Kubernetes, non ha pulsanti standard per approvare e verso WhatsApp ha solo un ponte non ufficiale ([ricerca/28 §4, §5, §7](../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Quando Buzz esce dal laboratorio**: la issue #7375 chiusa, nessuna approvazione automatica dei permessi, le PR delle approvazioni (#8057 e #7616) unite, un aggiornamento che passa i 10 scenari di prova, le patch entro 14 giorni ([ricerca/36 §5.6](../ricerca/36-architettura-v2.md)).

### 7.2 La trascrizione delle call: servizi in cloud, Vexa e trascrizione in casa

L'agente delle chiamate entra in ogni call, dichiarandolo, e la trascrive ([proposta §4.2](../PRESENTAZIONE-CEO.md)). L'audio e le trascrizioni integrali sono dati rossi, il più delicato dei tre colori: restano sul server, oppure vanno all'API di Anthropic dopo aver oscurato in locale i dati non necessari ([proposta §5.6](../PRESENTAZIONE-CEO.md)). Le riunioni sono di quattro tipi, e ognuno ha la sua strada: call Teams nostre, call Teams di altri, Meet e Zoom dei clienti, riunioni dal vivo ([ricerca/30 §2](../ricerca/30-call-e-trascrizione-self-hosted.md)).

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| **Servizi in cloud**: Recall.ai, un bot di registrazione a 0,65 $ l'ora, o Fireflies | Maturi, entrano in tutte le piattaforme, trascrizione inclusa ([ricerca/30 §4.1](../ricerca/30-call-e-trascrizione-self-hosted.md)). Recall costava circa 17,42 € al mese con 30 ore di call ([ricerca/22 §6](../ricerca/22-architettura-scelta.md)) | L'audio, dato rosso, esce dal server: Recall.ai è un servizio negli USA ([ricerca/30 §4.1](../ricerca/30-call-e-trascrizione-self-hosted.md); [proposta §5.6](../PRESENTAZIONE-CEO.md)), e di Recall.ai e Fireflies nessuno aveva verificato la regione dei dati e il DPA, l'accordo sul trattamento dei dati ([ricerca/21 compliance §3](../ricerca/21-giudizio-compliance.md); [ricerca/23 §2](../ricerca/23-critica-completezza.md)). Non sono nel board ([ricerca/25 §2, C06](../ricerca/25-board-michele-e-delta.md)). Fireflies costava 67,90 € al mese ([ricerca/22 §9](../ricerca/22-architettura-scelta.md)) | **Escono.** Fireflies era già scartato nel primo giro, a favore di Recall.ai ([ricerca/22 §9](../ricerca/22-architettura-scelta.md)); Recall.ai esce con il board ([proposta §1](../PRESENTAZIONE-CEO.md)): l'audio resta in casa e si trascrive in casa ([proposta §5.6](../PRESENTAZIONE-CEO.md)) |
| **Trascrizione nativa di Teams**, scaricata sul server con Microsoft Graph, l'API di M365 | Nessun bot: la trascrizione resta in M365, che il board ammette. Teams attribuisce ogni frase alla persona giusta e mostra da solo l'avviso di registrazione. Le API delle trascrizioni sono gratuite dal 25 agosto 2025 e non chiedono Azure ([ricerca/30, In breve; §2; §3.1](../ricerca/30-call-e-trascrizione-self-hosted.md)) | Vale solo per le riunioni organizzate nel nostro Teams. Vanno accese due impostazioni spente di serie: l'accesso di Graph alle trascrizioni e i nomi di chi parla ([ricerca/30, In breve](../ricerca/30-call-e-trascrizione-self-hosted.md)). Va provato se registra anche senza nessuno di SerSan collegato ([proposta, appendice A, C2](../PRESENTAZIONE-CEO.md)) | **Scelta per le nostre call Teams**, dalla fase 1 ([proposta §11; appendice A, J5](../PRESENTAZIONE-CEO.md)) |
| **Vexa**, un bot open source sul nostro server che entra nella call come un partecipante | Licenza Apache-2.0; Meet, Teams e Zoom; trascrizione in casa già pronta, calendario, cancellazione per riunione ([ricerca/30 §4.1](../ricerca/30-call-e-trascrizione-self-hosted.md)) | La versione stabile 0.12 non parla e non scrive in chat, quindi non si presenta da sola; esce una versione quasi ogni settimana ([ricerca/30 §4.1, §4.2](../ricerca/30-call-e-trascrizione-self-hosted.md)). Nel 2026 Teams, Meet e Zoom hanno chiuso le porte ai bot: il bot entra solo se il cliente lo ammette ([ricerca/30, In breve](../ricerca/30-call-e-trascrizione-self-hosted.md)) | **Scelta per le call dei clienti**, cioè Teams di altri, Meet e Zoom, dalla fase 3. Riserva: la registrazione sul PC di chi partecipa ([proposta §4.2, §13; appendice A, J5](../PRESENTAZIONE-CEO.md)). Piano B: Attendee, un altro bot da installare sul server, solo se Vexa delude nella prova sul campo ([ricerca/30 §10](../ricerca/30-call-e-trascrizione-self-hosted.md)) |
| **Trascrizione in casa**, sulla nostra GPU o sulla CPU | L'audio non esce dal server ([proposta §5.6](../PRESENTAZIONE-CEO.md)); licenze a 0 € ([ricerca/30 §11.3](../ricerca/30-call-e-trascrizione-self-hosted.md)) | La RTX 4000 di oggi è già quasi piena ([ricerca/30, In breve](../ricerca/30-call-e-trascrizione-self-hosted.md)), e ogni tanto Michele la presta al laboratorio ([proposta §6.4](../PRESENTAZIONE-CEO.md)) | **Scelta.** Dal vivo faster-whisper; a lotti Parakeet o WhisperX, con pyannote per riconoscere chi parla ([ricerca/30 §10](../ricerca/30-call-e-trascrizione-self-hosted.md)). Prima sulla RTX 4000, poi sulla seconda GPU, che conviene dalla fase 3 ([proposta §6.4](../PRESENTAZIONE-CEO.md)). *Superato in parte dopo il terzo giro: la seconda GPU si propone per la milestone 2; vedi §10.3 e [ADR-0014](adr/0014-seconda-gpu-blackwell.md)* |

- **Riunioni dal vivo.** Si registrano dal telefono, che manda l'audio al server in modo sicuro; poi trascrizione e riconoscimento di chi parla a lotti ([ricerca/30, In breve](../ricerca/30-call-e-trascrizione-self-hosted.md); [proposta, appendice A, J5](../PRESENTAZIONE-CEO.md)). Per le riunioni in sala, un vivavoce da 100-250 € nella fase 3 ([proposta §14, decisione 14](../PRESENTAZIONE-CEO.md)).
- **Perché non il bot ufficiale di Microsoft.** In produzione gira su Windows Server in Azure, e Azure esce ([ricerca/30 §4.1](../ricerca/30-call-e-trascrizione-self-hosted.md)).

### 7.3 La voce di Andrea: in cloud o in casa

"Andrea" richiama entro 90 secondi ogni nuova lead che nel modulo ha chiesto la richiamata di un assistente AI, risponde alle chiamate in entrata quando nessuno può, si dichiara AI dalla prima frase e fissa l'appuntamento con uno di noi ([proposta §4.3, §9.1](../PRESENTAZIONE-CEO.md)).

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| **In cloud**: ElevenLabs Agents con un numero mobile italiano di Twilio, il piano della prima versione | Voce pronta e curata, latenza già misurata dal fornitore, nessun lavoro di integrazione telefonica ([ricerca/31 §0](../ricerca/31-voce-andrea-self-hosted.md)) | L'audio delle chiamate passa da fornitori negli USA ([proposta §5.6](../PRESENTAZIONE-CEO.md)); fuori dal board ([ricerca/25 §2, C08](../ricerca/25-board-michele-e-delta.md)); circa 170 € al mese ([ricerca/22 §9](../ricerca/22-architettura-scelta.md)) | **Esce** ([proposta §1](../PRESENTAZIONE-CEO.md)). Resta l'ultima istanza: se la voce italiana in casa non è abbastanza buona, una voce in cloud come eccezione decisa dai CEO ([proposta §13](../PRESENTAZIONE-CEO.md)) |
| **Via di mezzo**: voce in casa, numero e chiamate su Twilio | Circa 82 € al mese, meno della via ElevenLabs ([ricerca/31 §12](../ricerca/31-voce-andrea-self-hosted.md)) | Twilio è un servizio USA fuori dal board, con il rischio di pagare 0,3433 $ al minuto verso i cellulari italiani ([ricerca/31 §4.2, §12](../ricerca/31-voce-andrea-self-hosted.md)); con le regole AGCOM, chi chiama dall'estero mostrando un numero italiano rischia il blocco ([ricerca/31 §4.1](../ricerca/31-voce-andrea-self-hosted.md)) | Scartata |
| **In casa**: Asterisk, un centralino open source; Pipecat, una libreria per le conversazioni vocali in tempo reale; la linea di un operatore telefonico italiano; ascolto e voce con modelli sul nostro server; Claude Haiku via LiteLLM ([proposta, appendice A, G5](../PRESENTAZIONE-CEO.md); [ricerca/31, In breve](../ricerca/31-voce-andrea-self-hosted.md)) | L'audio dei lead resta in azienda: verso Anthropic va solo il testo. Nessun canone a minuto per la voce ([ricerca/31, In breve; §0](../ricerca/31-voce-andrea-self-hosted.md)) | La RTX 4000 non ha spazio per Andrea, quindi si parte sulla CPU; latenza stimata di 1,3-2,0 secondi con la GPU e di 1,6-2,5 sulla sola CPU ([ricerca/31, In breve](../ricerca/31-voce-andrea-self-hosted.md)). La voce italiana va provata con un test d'ascolto ([proposta §13](../PRESENTAZIONE-CEO.md)). L'operatore telefonico resta comunque un servizio esterno da approvare ([proposta, appendice A, G5](../PRESENTAZIONE-CEO.md)) | **Scelta**, dalla fase 5: prima sulla CPU, poi sulla seconda GPU. Linea italiana, Registro delle opposizioni e modelli: 44-90 € al mese, attivazione 7-14 € ([proposta §11, §12.1; §14, decisione 10](../PRESENTAZIONE-CEO.md)) |

- **L'operatore.** La ricerca propone Messagenet, operatore italiano, da verificare sull'uso da parte di un agente automatico ([ricerca/31 §4.2](../ricerca/31-voce-andrea-self-hosted.md); [domande per Michele, n. 10](../DOMANDE-PER-MICHELE.md)).
- **La voce clonata di un collega.** Si fa solo in casa, con Qwen3-TTS sulla seconda GPU, nella fase 5 e dopo la voce sintetica, con il contratto separato e revocabile del collega e il via del parere legale ([proposta, appendice A, lacune dichiarate](../PRESENTAZIONE-CEO.md)).
- **Un'eccezione di regola.** Il piano marketing vieta voci sintetiche nelle call: per Andrea serve un'eccezione decisa dai CEO, solo per le richiamate chieste dalla lead e con voce dichiarata ([proposta §13; §14, decisione 10](../PRESENTAZIONE-CEO.md)). *Superato dal terzo giro: il progetto è approvato e Andrea è accettato dal gruppo di progetto, che decide tempi e acquisti con Michele. Andrea lavora a L3 solo dopo il parere legale, il consenso registrato e 50 chiamate di prova; parte dalla fase 5, e con lead vere si può anticipare alla fase 3 ([ADR-0008, revisione del 10 novembre](adr/0008-andrea-centralino.md)).*

### 7.4 La seconda GPU: A2000, RTX 2000 Ada, RTX PRO 2000 Blackwell, L4

Perché serve: la Quadro RTX 4000 da 8 GB fa oggi tutto il lavoro della GPU, e quando Michele la presta al laboratorio i lavori aspettano in coda. La seconda scheda deve tenere insieme, giorno e notte, la trascrizione dal vivo, la voce di Andrea e la ricerca nella memoria ([proposta §6.4](../PRESENTAZIONE-CEO.md)). Porta memoria e disponibilità continua, non velocità: sui modelli piccoli la RTX 4000 resta la più veloce ([ricerca/32 §4.6](../ricerca/32-hardware-e-upgrade.md)). Il messaggio di Michele parlava di una seconda GPU "tipo una RTX A2000 con chip Ada da 6GB GDDR7": una scheda così non esiste, perché il nome mescola tre prodotti diversi ([ricerca/32 §4.1](../ricerca/32-hardware-e-upgrade.md); [ricerca/25 §3, H07](../ricerca/25-board-michele-e-delta.md)).

| Scheda | Pro | Contro | Esito |
|---|---|---|---|
| **RTX A2000 12 GB** | 70 W, senza cavo di alimentazione; la più economica, circa £455 nuova nel Regno Unito, IVA britannica inclusa ([ricerca/32 §4.2, §4.3](../ricerca/32-hardware-e-upgrade.md)) | Con 12 GB ci stanno Andrea, la ricerca nella memoria e la trascrizione, ma non il modello piccolo da 4 miliardi di parametri che prepara i documenti; fuori produzione ([ricerca/32 §4.6, §4.7](../ricerca/32-hardware-e-upgrade.md)) | Scartata |
| **RTX 2000 Ada 16 GB** | 16 GB, 70 W senza cavo, ventola propria, architettura matura per l'audio ([ricerca/32 §4.7](../ricerca/32-hardware-e-upgrade.md)) | 837-946 € IVA inclusa a fine ottobre ([ricerca/32 §4.7](../ricerca/32-hardware-e-upgrade.md)); il 7 novembre, nelle offerte italiane, la Blackwell costava solo il 6 % in più ([ricerca/37 §4, seconda GPU](../ricerca/37-hardware-risposte-michele.md)) | Era la nostra proposta di ottobre; superata dalla scelta di Michele ([proposta §6.4](../PRESENTAZIONE-CEO.md)) |
| **RTX PRO 2000 Blackwell 16 GB** | La generazione successiva della 2000 Ada: stessi 16 GB e 70 W senza cavi, memoria più veloce ([proposta §6.4](../PRESENTAZIONE-CEO.md)), 288 GB/s contro 224 ([ricerca/32 §4.2](../ricerca/32-hardware-e-upgrade.md)) | In Italia circa 1.290-1.305 € IVA inclusa, il 20 % in più di fine ottobre; la mediana dell'ultimo anno è intorno ai 985 € IVA inclusa. Il riser principale, il supporto che ospita le schede aggiuntive, è pieno: la scheda va nel riser secondario, che costa circa 75-160 €, IVA e spedizione comprese, se manca. HPE non certifica due GPU di modelli diversi nello stesso server, e i programmi vanno provati sulla nuova architettura prima di spostarci la trascrizione ([proposta §6.4](../PRESENTAZIONE-CEO.md)) | **Scelta da Michele**, da comprare quando il prezzo scende. Noi proponiamo sotto i 1.000 € IVA inclusa (circa 820 € esclusa): conviene dalla fase 3 e serve al più tardi all'inizio della fase 5, prima di spostare Andrea sulla GPU. Circa 880-1.220 € con riser e staffa ([proposta §6.4; §14, decisione 12](../PRESENTAZIONE-CEO.md)). *Superato dopo il terzo giro: la scheda resta questa, ma la proposta a Michele è comprarla per la milestone 2, anche a 1.100 € più il riser se manca (75-160 €), perché la prova dei modelli locali ne ha bisogno ([ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md)); vedi §10.3 e [ADR-0014, seconda revisione del 10 novembre](adr/0014-seconda-gpu-blackwell.md)* |
| **NVIDIA L4 24 GB** | 24 GB: ci starebbe anche un modello da 8 miliardi di parametri sempre acceso ([ricerca/32 §4.6](../ricerca/32-hardware-e-upgrade.md)) | Oltre 3.500 € nuova, IVA inclusa. Raffreddamento passivo e scheda non qualificata HPE: dipende tutta dall'aria del server, che il controller di gestione (iLO) non sa di dover aumentare ([ricerca/32 §4.3, §4.4, §4.7](../ricerca/32-hardware-e-upgrade.md)) | Scartata |

Scartate anche la T4 e la A2, passive e più lente o più vecchie ([ricerca/32 §4.7](../ricerca/32-hardware-e-upgrade.md)).

### 7.5 L'UPS: Eaton 5PX, APC o HPE R1500 G5

L'UPS, il gruppo di continuità, tiene accese le macchine quando manca la corrente. Il board prevedeva più avanti un UPS da rack, APC SMT1500 o Eaton 5PX ([board di Michele](../allegati/infra/SerSan%20Infra%20Board.md)); a ottobre abbiamo messo in conto l'Eaton ([ricerca/32 §6](../ricerca/32-hardware-e-upgrade.md)).

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| **Eaton 5PX 1500i RT2U G2**, nuovo | 1.500 VA e 1.500 W; con due GPU, al picco lavorerebbe al 53-57 % della sua potenza ([ricerca/32 §6](../ricerca/32-hardware-e-upgrade.md)) | 937-1.144 € IVA esclusa ([proposta §12.2](../PRESENTAZIONE-CEO.md)) | Messo in conto a ottobre, **non comprato** ([proposta §12.2](../PRESENTAZIONE-CEO.md)) |
| **APC Smart-UPS SMT1500RMI2UC**, nuovo | Da rack, circa 25 minuti di autonomia a metà carico ([ricerca/32 §6](../ricerca/32-hardware-e-upgrade.md)) | 1.000 W: al picco con due GPU lavorerebbe all'80-85 %; circa 1.011 € IVA esclusa ([ricerca/32 §6](../ricerca/32-hardware-e-upgrade.md)) | Scartato |
| **HPE R1500 G5**, usato | 1.550 VA e 1.100 W, da rack, con la scheda di rete e il collegamento USB al firewall per NUT, il programma che legge lo stato dell'UPS e spegne le macchine. Dopo 3 minuti senza corrente spegne il server in modo pulito e tiene accesa la rete fino a fine batteria ([proposta §6.1](../PRESENTAZIONE-CEO.md); [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)). Costa 255 € ([proposta §12.2](../PRESENTAZIONE-CEO.md)). Con le batterie nuove, a circa 330 W dà 23 minuti ([domande per Michele, n. 21](../DOMANDE-PER-MICHELE.md)) | Batterie usate e senza garanzia: se il test di autonomia all'arrivo va male, 140-550 € di batterie nuove ([proposta §1, §12.2](../PRESENTAZIONE-CEO.md)). Con la seconda GPU e 384 GB di RAM il picco stimato è di 860-945 W: regge, con 6-7 minuti di autonomia; con il secondo server, al picco si possono superare i 1.100 W ([domande per Michele, n. 20](../DOMANDE-PER-MICHELE.md)). Al ritorno della corrente il server, com'è impostato oggi, va riacceso a distanza ([proposta §6.1](../PRESENTAZIONE-CEO.md)) | **Comprato da Michele**, in arrivo ([proposta §6.1, §12.2](../PRESENTAZIONE-CEO.md)). All'arrivo: test di autonomia e di riaccensione, e batterie nuove se servono ([proposta §13](../PRESENTAZIONE-CEO.md)). Per il secondo server serviranno un tetto di potenza o un secondo UPS: è una domanda aperta per Michele ([domande per Michele, n. 20](../DOMANDE-PER-MICHELE.md)) |

### 7.6 L'accesso da fuori: VPS, IP fisso con porte aperte, macchina Oracle

Il board vuole "zero-trust, nessuna porta aperta": si entra solo con identità verificata, attraverso NetBird, una rete privata con accesso Entra e chiave FIDO2 per il team e gli amministratori, e attraverso Pangolin con Traefik, che pubblicano le app web per i clienti e l'endpoint MCP per Claude Team ([board di Michele](../allegati/infra/SerSan%20Infra%20Board.md)). Però Pangolin, in modalità tunnel, di solito vive su un server con un indirizzo pubblico; NetBird installato da noi chiede alcune porte raggiungibili; e il connettore di Claude Team parte dai server di Anthropic, quindi l'endpoint deve essere raggiungibile da internet ([ricerca/25 §7, N10](../ricerca/25-board-michele-e-delta.md)).

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| **VPS**, un server virtuale in affitto, con Pangolin e NetBird | In casa nessuna porta aperta: il lato di casa esce soltanto ([ricerca/25 §7, N10](../ricerca/25-board-michele-e-delta.md)). Con il TLS in passthrough, cioè il traffico cifrato che passa senza essere aperto, il VPS non vede in chiaro bot, webhook e MCP ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)) | Un cloud in più, con un costo: 6,49 € al mese, perché l'offerta da 5,99 € non era disponibile ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)) | Era una delle due strade di ottobre. Resta la riserva a pagamento, 6,49 € al mese ([proposta §14, decisione 7](../PRESENTAZIONE-CEO.md)) |
| **IP fisso con porte aperte** solo verso la rete EDGE del board, quella dei servizi esposti | Nessun servizio esterno in più ([ricerca/25 §7, N10](../ricerca/25-board-michele-e-delta.md)) | Va contro la regola del board "nessuna porta aperta" ([board di Michele](../allegati/infra/SerSan%20Infra%20Board.md)) | Scartato: era l'altra strada di ottobre ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)) |
| **Macchina Oracle Cloud a Milano**, sul piano gratuito Always Free, con NetBird, Pangolin e il monitoraggio (Uptime Kuma e ntfy) | 0 € sul piano gratuito: due piccole macchine AMD da 1 GB oppure una Ampere con 2 core e 12 GB, e 10 TB al mese di traffico in uscita ([ricerca/37 §3](../ricerca/37-hardware-risposte-michele.md)). Con Milano come unica regione, i dati restano lì ([ricerca/37 §6, gruppo wan-oracle](../ricerca/37-hardware-risposte-michele.md)). L'accesso funziona anche sulla linea di riserva ([proposta §13](../PRESENTAZIONE-CEO.md)) | Oracle si riprende le macchine gratuite che per 7 giorni restano sotto il 20 % di CPU, rete e memoria; Milano ha una sola zona di disponibilità; la regione di casa si sceglie alla registrazione e poi non si cambia ([ricerca/37 §3](../ricerca/37-hardware-risposte-michele.md); [domande per Michele, n. 4](../DOMANDE-PER-MICHELE.md)). Come ogni servizio cloud è nel perimetro di Cyber Essentials, con l'MFA obbligatoria ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)) | **Scelta da Michele** ([board del rack, versione HTML](../allegati/infra/Rack%20SerSan%2012U.html); [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)), nei costi dalle fasi 0-1: 0 € sul piano gratuito, 6,49 € al mese se servisse un server a pagamento ([proposta §1; §14, decisione 7](../PRESENTAZIONE-CEO.md)) |

- **Cosa resta da decidere con Michele**: se passare l'account Oracle a consumo, perché non si riprenda le macchine; se tenere Pangolin in TLS passthrough verso Traefik; se l'IP fisso serve ancora ([domande per Michele, n. 4](../DOMANDE-PER-MICHELE.md)). Nella proposta l'IP fisso resta nei costi, fino a 10 € al mese ([proposta §1; §14, decisione 17](../PRESENTAZIONE-CEO.md)).
- **Senza esporre nulla.** Gli amministratori possono usare i server MCP anche da Claude Desktop attraverso NetBird, come prevede il board ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)).

## 8. Le altre sostituzioni del secondo giro

Con il board di Michele altri pezzi del primo giro hanno cambiato strada. Nessuna funzione si perde: dove un servizio esce, qualcuno ne prende il posto ([ricerca/25, intestazione e §2](../ricerca/25-board-michele-e-delta.md)).

| Nel primo giro | Dopo il board di Michele | Fonte |
|---|---|---|
| Notion per regole, processi e to-do | BookStack, un wiki sul server, per regole, processi e catalogo; Jira per to-do e progetti; PostgreSQL 16 per i dati. *Superato in parte dopo il terzo giro: la casa dei testi, BookStack o una cartella di file Markdown in git, si sceglie prima della fase 2; vedi §10.1* | [ricerca/25 §2, C02](../ricerca/25-board-michele-e-delta.md); [ADR-0005, revisione del 10 novembre](adr/0005-memoria-postgres-qdrant-bookstack.md) |
| Google Workspace e Gmail | M365: posta e calendario con Microsoft Graph | [ricerca/25 §2, C03](../ricerca/25-board-michele-e-delta.md) |
| Cloudflare Tunnel per esporre i servizi | Pangolin e Traefik; Cloudflare solo per il DNS | [ricerca/25 §2, C04](../ricerca/25-board-michele-e-delta.md) |
| WireGuard, Tailscale o un VPS WireGuard per entrare da fuori | NetBird, con Entra e chiave FIDO2 | [ricerca/25 §2, C05](../ricerca/25-board-michele-e-delta.md) |
| Postgres 17 con pgvector per la memoria vettoriale | Qdrant con ricerca ibrida e reranker (un modello che riordina i risultati), tutto sul server | [ricerca/25 §2, C11](../ricerca/25-board-michele-e-delta.md) |
| Claude in Slack per le domande sui dati | Claude Team con il connettore verso la memoria, con i permessi di chi chiede | [ricerca/25 §2, C01 e C22](../ricerca/25-board-michele-e-delta.md) |
| Hermes Cloud come palestra e riserva | Niente: la riserva vera è il ripristino dal backup | [ricerca/25 §2, C10](../ricerca/25-board-michele-e-delta.md) |
| Password manager in cloud | Vaultwarden per le persone, Infisical per i segreti delle applicazioni | [ricerca/25 §2, C15](../ricerca/25-board-michele-e-delta.md) |
| Backup in cloud | Proxmox Backup Server in sede e, da marzo 2027, una copia cifrata fuori sede | [ricerca/25 §2, C16](../ricerca/25-board-michele-e-delta.md); [proposta §6.1](../PRESENTAZIONE-CEO.md) |
| n8n escluso | n8n per routine e integrazioni interne, mai per invii a clienti o prospect. *Superato dal terzo giro: la sveglia sta nel motore e n8n è facoltativo; vedi §9* | [ricerca/25 §2, C27](../ricerca/25-board-michele-e-delta.md); [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md) |
| La VM Azure come riserva | Esce con Azure | [ricerca/25 §2, C25](../ricerca/25-board-michele-e-delta.md) |

## 9. Terzo giro, 9-10 novembre: autonomia

### 9.1 Perché si è rifatta la valutazione

- **La domanda è cambiata.** I primi due giri chiedevano quale orchestratore usare. Il terzo chiede quanto il sistema lavora da solo ([ricerca/45, intestazione](../ricerca/45-architettura-v3.md)). Alberto vuole agenti che lavorano e imparano da soli, come quelli della trascrizione di riferimento ([ricerca/43, giudizio visione, «Raccomandazione»](../ricerca/43-giudizio-visione.md)). E vuole solo le protezioni essenziali ([ricerca/42, proposta B §1](../ricerca/42-proposta-B-orchestratore-pronto.md)), perché SerSan Agent OS è un sistema aziendale chiuso: quattro persone, rete interna, accesso da fuori solo attraverso NetBird e Pangolin ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- **I livelli di autonomia.** Il giro misura ogni azione su quattro livelli ([ADR-0020](adr/0020-autonomia-a-livelli.md)):
  - **L0 a mano**: l'agente prepara, una persona esegue;
  - **L1 carta**: l'agente propone, una persona approva ogni singola azione;
  - **L2 finestra**: l'azione parte da sola dopo un tempo in cui una persona può fermarla;
  - **L3 autonomo**: l'azione parte subito, dentro regole, tetti e registro; le persone vedono dopo e possono revocare.
- **Cosa hanno trovato i quattro rapporti di partenza.**
  - **La trascrizione di riferimento lavora quasi tutta a L3.** Il post-call è completo e comprende la mail al cliente; l'agente vocale lavora giorno e notte e impara dai rifiuti; nel testo non compare nessuna approvazione ([ricerca/40, «In breve»](../ricerca/40-alternative-e-autonomia.md)). I comportamenti autonomi del video sono elencati come requisiti in [ricerca/38](../ricerca/38-autonomia-nella-trascrizione.md).
  - **Il disegno v2 era molto più prudente.** Nelle fasi 0-1 tutto ciò che esce è L1 e i lavori partono da un comando dato a mano. Nessuna voce arriva a L2, perché il Cancello non ha la finestra. I colli di bottiglia sono 15 ([ricerca/39, «In breve»](../ricerca/39-autonomia-del-disegno-v2.md)).
  - **I limiti stanno quasi tutti nel Cancello**, nelle regole di casa e nel calendario, non nel motore: cambiare orchestratore non li toglie ([ricerca/39, «In breve»](../ricerca/39-autonomia-del-disegno-v2.md)).
  - **Nessuna alternativa dei primi due giri aveva la finestra L2.** Ognuna partiva da L1 per ciò che esce, e il secondo giro aveva messo la capacità del server davanti all'autonomia ([ricerca/40, «In breve»](../ricerca/40-alternative-e-autonomia.md)).
  - **Le novità uscite dopo il 25 ottobre**, per l'Agent SDK, Managed Agents, Hermes, n8n e Buzz, sono raccolte in [ricerca/41](../ricerca/41-novita-al-9-novembre.md).

### 9.2 Il criterio nuovo e i pesi

- **Sei criteri con pesi fissati prima del giudizio**: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10 ([ricerca/45, «I documenti del giro»](../ricerca/45-architettura-v3.md)).
- **Come si conta.** Ogni giudice dà da 0 a 10 punti per criterio; ogni voto conta secondo il peso del suo criterio, e il totale pesato è su 100. La classifica è la media dei quattro totali ([ricerca/43, giudizio visione, «Voti»](../ricerca/43-giudizio-visione.md); [ricerca/45 §1.1](../ricerca/45-architettura-v3.md)).
- **Quattro giudici, ognuno con una lente**: visione e autonomia; CEO e commerciale; CPTO e tecnica; protezioni essenziali e affidabilità ([visione](../ricerca/43-giudizio-visione.md), [CEO](../ricerca/43-giudizio-ceo.md), [CPTO](../ricerca/43-giudizio-cpto.md), [essenziale](../ricerca/43-giudizio-essenziale.md)).

### 9.3 Le quattro proposte

| Proposta | L'idea | Fonte |
|---|---|---|
| **P-A. Motore sull'Agent SDK con autonomia a livelli** | Il motore resta sull'Agent SDK e il Cancello resta l'unico esecutore, ma diventa leggero: invece di una carta per ogni azione dà un livello a ogni terna, cioè agente, tipo d'azione e classe di destinatari. Una terna sale con 5 sì puliti a L2 e con 15 finestre senza «Ferma» a L3; scende da sola al primo segnale negativo. Gli agenti partono da eventi già dalla fase 1 e si passano il lavoro in una bacheca | [ricerca/42, proposta A §1](../ricerca/42-proposta-A-motore-a-livelli.md) |
| **P-B. Orchestratore pronto con il nostro Cancello** | Gli agenti girano su Hermes, sul server di Michele, con profili, orari, bacheca e skill che l'agente scrive da solo già pronti. Il Cancello dà un livello a ogni classe d'azione. Il limite, detto dalla proposta stessa: sul gateway di Hermes erano risolti 83 problemi su 312, quindi l'autonomia verso i clienti parte solo dopo la prova delle settimane 5-8 | [ricerca/42, proposta B §1](../ricerca/42-proposta-B-orchestratore-pronto.md) |
| **P-C. Ibrido con agenti in abbonamento** | Sul server restano i dati dei clienti, le azioni verso i clienti e il Cancello. Le squadre che usano solo dati verdi (ricerca, bandi, segnali pubblici, piano editoriale, testi, grafiche, video, metriche e SEO, cioè il posizionamento sui motori di ricerca) girano in abbonamento: prima su Claude Team, poi su Claude Managed Agents, il servizio in cui Anthropic fa girare gli agenti | [ricerca/42, proposta C §1](../ricerca/42-proposta-C-ibrido-abbonamenti.md) |
| **P-D. Automazione prima** | I lavori ripetitivi diventano flussi n8n fissi, avviati da un evento o da un orario: il codice sceglie i passi e i destinatari, Claude scrive i testi senza strumenti. Le sessioni dell'Agent SDK restano per circa dieci figure che ragionano a più passi e consegnano solo bozze. Una classe sale a L2 dopo 10 sì e a L3 dopo 20 invii non fermati | [ricerca/42, proposta D §1](../ricerca/42-proposta-D-automazione-prima.md) |

Tutte e quattro chiedono lo stesso Cancello a livelli, con la finestra L2 e la discesa automatica: cambia solo il motore ([ricerca/43, giudizio visione, «Raccomandazione»](../ricerca/43-giudizio-visione.md); [ricerca/43, giudizio CEO, «Raccomandazione», punto 1](../ricerca/43-giudizio-ceo.md)).

### 9.4 I quattro giudizi

Il voto sull'autonomia, da 0 a 10, dice già molto: in ogni lente P-D ha il voto più basso, o pari al più basso. Recupera su tempo al valore, costi e server.

| Giudice | P-A | P-B | P-C | P-D |
|---|---|---|---|---|
| Visione | 8 | **8,5** | 8 | 6,5 |
| CEO | 8 | 7,5 | **8,5** | 7,5 |
| CPTO | **8** | 7,5 | **8** | 7,5 |
| Essenziale | 8 | **8,5** | 7,5 | 7 |

Fonte: le tabelle «Voti» dei quattro giudizi ([visione](../ricerca/43-giudizio-visione.md), [CEO](../ricerca/43-giudizio-ceo.md), [CPTO](../ricerca/43-giudizio-cpto.md), [essenziale](../ricerca/43-giudizio-essenziale.md)); in grassetto il voto più alto di ogni riga.

- **Visione.** Sceglie P-A come base: agenti veri che si passano il lavoro, il post-call fino a L3 anche per il primo follow-up, nessun fornitore nuovo. Il suo difetto è la settimana 8, la più povera delle quattro. Lo corregge con innesti dalle altre: to-do in Jira ed evento in calendario e catene a schema da P-D; le ricerche su dati verdi come ponte e Metricool da P-C; il Capo di gabinetto e la bacheca da P-B ([ricerca/43, giudizio visione, «Raccomandazione»](../ricerca/43-giudizio-visione.md)).
- **CEO.** P-D e P-A sono pari entro il margine di giudizio. La decisione che conta è il Cancello a livelli, da approvare subito; per le fasi 0-1 consiglia l'ordine dei lavori di P-D, con le soglie di P-A. Resta il suo dissenso del secondo giro: il collo di bottiglia commerciale è il funnel, non l'orchestratore ([ricerca/43, giudizio CEO, «Raccomandazione»](../ricerca/43-giudizio-ceo.md)).
- **CPTO.** Raccomanda P-D come base delle fasi 0-2, con il motore di P-A come binario di crescita, a tre condizioni: la logica fuori da n8n, in un servizio TypeScript; bacheca e registro degli agenti in PostgreSQL; carte e «Ferma» solo dalla Porta, il nostro bot di Teams ([ricerca/43, giudizio CPTO, «Raccomandazione»](../ricerca/43-giudizio-cpto.md)).
- **Essenziale.** Raccomanda l'unione di P-D e P-A: per eseguire si parte da P-D, il modello di autonomia viene da P-A. Hermes resta un pilota in laboratorio; gli abbonamenti solo dove un pezzo non regge in casa ([ricerca/43, giudizio essenziale, «Raccomandazione»](../ricerca/43-giudizio-essenziale.md)).

### 9.5 La classifica

| Proposta | Visione | CEO | CPTO | Essenziale | Media su 100 |
|---|---|---|---|---|---|
| P-D. Automazione prima | 74 | 76 | 78,3 | 78,3 | **76,6** |
| P-A. Motore sull'Agent SDK con autonomia a livelli | 77,5 | 75 | 75,8 | 77 | **76,3** |
| P-C. Ibrido con abbonamenti | 75,5 | 72,8 | 70,5 | 71,5 | 72,6 |
| P-B. Hermes con il nostro Cancello | 71 | 64,3 | 65,5 | 70 | 67,7 |

Fonte: [ricerca/45 §1.1](../ricerca/45-architettura-v3.md). Alcuni giudizi scrivono i totali con due decimali, per esempio 78,25; la tabella li arrotonda come ricerca/45.

- **P-D vince di 0,3 punti, cioè dentro il margine di giudizio**: lo scrivono tutti e quattro i giudici. Tre di loro (CEO, CPTO ed essenziale) chiedono di unire P-D e P-A; il giudice della visione sceglie P-A con innesti da P-D ([ricerca/45 §1.2](../ricerca/45-architettura-v3.md)).
- **P-B è ultima.** Le quattro condizioni che il progetto si è dato per usare Hermes come orchestratore non sono soddisfatte ([ADR-0021](adr/0021-motore-a-due-corsie.md); [ADR-0012](adr/0012-hermes-uscita.md)).

### 9.6 Le tre verifiche avversarie

Tre scettici hanno provato a confutare la prima in classifica, P-D: il primo su tempi e livelli, il secondo su conformità e affidabilità, il terzo su costi, server e manutenzione. Il verdetto di tutti e tre è lo stesso: **regge con correzioni** ([ricerca/44](../ricerca/44-verifiche-avversarie.md)).

- **Tesi smentite** ([ricerca/44](../ricerca/44-verifiche-avversarie.md): VER1 rilievi 2 e 4, VER2 rilievo 1, VER3 rilievo 4):
  - alla settimana 8 il follow-up ai partecipanti della call non arriva a L2: con 11 lead, 1 risposta e 0 meeting al 5 ottobre, 10 sì puliti non stanno in quattro settimane;
  - P-D non raggiunge il livello della trascrizione: lo smentisce la proposta stessa, che tiene il primo follow-up a L2 e la newsletter a L1;
  - una classe di destinatari definita dal dominio non è lecita: il Garante applica le regole sul consenso anche agli indirizzi aziendali, quindi conta solo l'indirizzo esatto di chi era nella call;
  - P-D non toglie peso a Michele: porta i servizi da tenere aggiornati a circa 15-17, contro gli 11-13 della v2.1.
- **Tesi non dimostrate** ([ricerca/44](../ricerca/44-verifiche-avversarie.md): VER1 rilievi 6 e 8, VER2 rilievo 3, VER3 rilievi 2 e 3):
  - il risparmio di circa 19 giorni di sviluppo: il vantaggio vero di P-D sta nell'ordine dei lavori, non nel totale;
  - i 10 GB di RAM in meno: la forbice realistica è di 2-6 GB;
  - il flusso n8n «che parte sempre»: un'esecuzione caduta per un crash viene marcata «crashed» e non riprende da sola;
  - un'uscita L2 o L3 sicura perché il codice sceglie i destinatari: il disegno protegge chi riceve, non che cosa riceve, e manca un controllo del contenuto prima dell'invio.
- **Le correzioni chieste spingono P-D verso P-A** ([ricerca/45 §1.2](../ricerca/45-architettura-v3.md)): la logica esce da n8n e va nel nostro codice; le soglie di promozione diventano 5 e 15; si aggiunge un registro degli eventi in PostgreSQL, che rimette in coda gli eventi fermi. Altre correzioni entrano nel Cancello: l'indirizzo esatto, il controllo del contenuto prima di ogni uscita L2 o L3 e la classificazione delle risposte degli esterni ([ricerca/44](../ricerca/44-verifiche-avversarie.md): VER1 rilievo 6, VER2 rilievi 1 e 6).
- **Molti rilievi valgono anche per P-A**, a partire dai volumi bassi: verso l'esterno, alla settimana 8, l'autonomia reale è L1 per qualsiasi proposta ([ricerca/44, VER2 rilievo 5](../ricerca/44-verifiche-avversarie.md)).

### 9.7 L'unione scelta: «Cancello a livelli e motore a due corsie»

Non vince né P-D né P-A da sola, ma la loro unione ([ricerca/45 §1.2](../ricerca/45-architettura-v3.md)). Le sue parti, come valgono oggi:

1. **Il Cancello a livelli, la decisione che conta.** Ogni terna ha il suo livello, con la finestra L2 e il tasto «Ferma», la discesa automatica, «Annulla» e «Rettifica», la riga che dichiara l'assistente AI e i tetti giornalieri. Escono la chiave FIDO2 sulle carte, le regole «Sempre» e la revisione esterna obbligatoria ([ricerca/45 §1.2](../ricerca/45-architettura-v3.md); [ADR-0020](adr/0020-autonomia-a-livelli.md); [ADR-0023](adr/0023-protezioni-essenziali.md)).
2. **Un motore con due corsie, tutte e due nel nostro codice TypeScript.** La corsia N fa girare catene a schema: il codice sceglie passi e destinatari, il modello scrive senza strumenti. È il metodo di P-D, e il giudice di sicurezza del secondo giro lo chiama il disegno più robusto contro le istruzioni nascoste nel testo di terzi. La corsia S fa girare le sessioni dell'Agent SDK con strumenti, per le figure che ragionano a più passi: è il motore di P-A ([ADR-0021](adr/0021-motore-a-due-corsie.md)).
3. **Orari ed eventi stanno nel motore.** La sintesi faceva di n8n l'avvio dei lavori; la decisione del gruppo di progetto ha portato anche gli orari nel nostro codice, e n8n è facoltativo ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md); [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).
4. **La milestone 1 usa solo la corsia N.** I tre agenti del pilota (Post-call, Analista chiamate, Report del mattino) riassumono, estraggono e scrivono, e per questo basta una catena a schema. La sintesi metteva la corsia S nella fase 2; la decisione del gruppo di progetto la costruisce subito dopo la milestone 1 ([ricerca/45 §1.2 e «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md); [ADR-0021](adr/0021-motore-a-due-corsie.md)).

**Cosa entra da ciascuna proposta** ([ricerca/45 §1.3](../ricerca/45-architettura-v3.md)):

- **da P-A**: il modello di autonomia per terne; le soglie 5 e 15; la classe «persona appena incontrata», che può arrivare a L3 dopo il parere legale; le skill con valutazione automatica nelle fasi 2-3; lo stand-up degli agenti; una carta per campagna nell'outbound, dopo il parere; il registro unico delle 57 figure;
- **da P-D**: le catene a schema, con i destinatari presi dai dati; to-do in Jira ed evento in calendario il prima possibile; le regole sui dati delle esecuzioni di n8n, dove n8n c'è; l'ordine dei lavori, con il brief e la bozza d'offerta per primi;
- **da P-C**: Managed Agents come riserva prezzata, solo su dati verdi e solo se il server è pieno o fermo ([ADR-0024](adr/0024-abbonamenti-come-riserva.md)); l'esecutore Metricool per i post a L2, se Postiz non entra prima;
- **da P-B**: Hermes non entra nel percorso dei clienti e resta un pilota in laboratorio da 6-8 giorni di sviluppo. Se ne copiano cinque idee: il conteggio dei passaggi dall'ultimo messaggio umano, il blocco delle skill curate a mano, la regola per i turni persi, il Capo di gabinetto che smista il lavoro, la banca di frasi approvate per le aperture di Andrea ([ADR-0012, revisione del 10 novembre](adr/0012-hermes-uscita.md)).

### 9.8 Le sette precisazioni del gruppo di progetto

Il 10 novembre i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio. Il gruppo ha adottato la sintesi con sette precisazioni, che valgono sopra le parti della sintesi che nominano ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)):

1. **Dove vive il codice.** In una repo privata dell'organizzazione, `sersan-agent-os-codice`, con PRD, spec e piani di sviluppo. In questa repo restano la proposta, la ricerca, i documenti di progetto e le ADR.
2. **La persona appena incontrata parte a L2.** È l'indirizzo esatto di chi era in una call registrata e avvisata negli ultimi 14 giorni. Parte con una finestra di 30 minuti, per decisione del gruppo di progetto. Gli invii veri ai clienti cominciano con la milestone di telefono e posta: se prima di allora il parere legale lo esclude, la classe torna a L1 cambiando una riga di configurazione ([ADR-0020](adr/0020-autonomia-a-livelli.md)).
3. **La corsia S non aspetta la fase 2.** Si costruisce subito dopo la milestone 1; prima vengono il Cancello a livelli e le catene, perché servono a tutte e due le corsie ([ADR-0021](adr/0021-motore-a-due-corsie.md)). Per questo il piano di sviluppo di oggi ha una numerazione nuova delle milestone, che sostituisce quella di [ricerca/45 §6.4 e §12](../ricerca/45-architettura-v3.md): la corsia S, con la bacheca, i gruppi degli agenti, la prova di Buzz e il primo modello open-weight, è la milestone 2; telefono e posta diventano la milestone 4.
4. **Un modello per agente, anche open-weight.** Ogni agente dichiara nel registro il suo modello: Claude via API, un modello open-weight sul nostro server o un modello open-weight di un fornitore via API. Tutte le chiamate passano da LiteLLM. I modelli locali entrano prima nella corsia N; nelle sessioni dell'Agent SDK resta Claude finché una prova non dimostra che un modello locale regge. I fornitori terzi ricevono solo dati verdi e gialli ([ADR-0025](adr/0025-un-modello-per-agente.md)).
5. **La sveglia sta nel motore.** Gli orari stanno in una tabella del motore e gli eventi entrano da un unico ingresso, `POST /eventi`. n8n resta nel board di Michele per i collegamenti che servono, ma il sistema non ne dipende. Le routine di Claude, cioè i compiti programmati sui posti, restano per l'uso personale delle persone. Dall'11 novembre c'è un'eccezione: il motore può avviare un compito programmato sul posto della persona responsabile, per la corsia T del §10.4 ([ADR-0022 e la sua revisione dell'11 novembre](adr/0022-eventi-e-sveglia-nel-motore.md)).
6. **La chat degli agenti è anticipata.** Una bacheca nostra, dove gli agenti si passano il lavoro, e gruppi di chat dove quel lavoro si vede: uno per squadra, uno per cliente, uno comune «Agenti». Si costruiscono insieme alla corsia S. Buzz si collega alla stessa bacheca e si prova presto: se non perde risposte e ha le approvazioni collegate, diventa la casa degli agenti. Teams resta per le persone e per le approvazioni dal telefono ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). *Rivisto il 12 novembre: i gruppi stanno nella Sala di controllo finché non c'è il bot di Teams o Buzz, i passaggi fra agenti non sono azioni del Cancello, e Buzz si prova quando Michele lo ammette e c'è una macchina Linux con Docker ([ADR-0030](adr/0030-bacheca-gruppi-specchi.md)).*
7. **Percorsi dei file.** Dove la sintesi cita lo spec e il PRD con un percorso dentro questa repo, si intende la repo del codice.

La milestone 1 è in costruzione dal 10 novembre 2026 sulle macchine di sviluppo, con dati di prova e un modello a copione, senza chiave API.

### 9.9 Cosa è cambiato rispetto al secondo giro

| Tema | Secondo giro, 25 ottobre | Terzo giro, 9-10 novembre, con le decisioni dopo |
|---|---|---|
| La domanda | quale orchestratore, dentro il board di Michele (§3) | quanto il sistema lavora da solo ([ricerca/45, intestazione](../ricerca/45-architettura-v3.md)) |
| Criteri e pesi | sei criteri con lo stesso peso, fra cui copertura della visione e aderenza al board; totale su 240 (§1) | sei criteri pesati: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10; media su 100 (§9.2) |
| Giudici | visione, commerciale, tecnica, sicurezza e privacy (§1) | visione, CEO, CPTO, protezioni essenziali; più tre verifiche avversarie sulla prima in classifica (§9.4, §9.6) |
| Esito | motore sull'Agent SDK, 171,5 punti (§4.2) | unione di P-D (76,6) e P-A (76,3): «Cancello a livelli e motore a due corsie» (§9.5, §9.7) |
| Motore | ogni agente è una sessione dell'Agent SDK ([ADR-0001](adr/0001-motore-agent-sdk.md)) | due corsie nello stesso codice, N e S ([ADR-0021](adr/0021-motore-a-due-corsie.md)); dall'11 novembre un router con sei destinazioni, compresa la corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)) |
| Azioni verso l'esterno | una carta per ogni azione; regole «Sempre» dopo 20 sì per una sola destinazione ([ADR-0003](adr/0003-cancello-approvazioni.md)) | livelli da L0 a L3 per terna, finestra L2, soglie 5 e 15, discesa automatica ([ADR-0020](adr/0020-autonomia-a-livelli.md)) |
| Protezioni | anche FIDO2 sulle carte, firme fra i processi, registro a catena, revisione esterna entro la settimana 21 ([ADR-0023, «Contesto»](adr/0023-protezioni-essenziali.md)) | le protezioni essenziali; la revisione esterna diventa facoltativa ([ADR-0023](adr/0023-protezioni-essenziali.md)) |
| Orari ed eventi | n8n ([ADR-0011](adr/0011-n8n-orari-integrazioni.md)) | nel motore, con un registro degli eventi; n8n facoltativo ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)) |
| Chat fra agenti | bacheca e canale «Agenti» all'inizio della fase 2, Buzz dalla fase 4 ([ADR-0026, «Contesto»](adr/0026-bacheca-e-gruppi-degli-agenti.md)) | bacheca e gruppi di chat subito dopo la milestone 1, Buzz provato presto ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)) |
| Hermes | via d'uscita già prezzata ([ADR-0012](adr/0012-hermes-uscita.md)) | via d'uscita e pilota in laboratorio da 6-8 giorni di sviluppo, con cinque idee copiate ([ADR-0012, revisione](adr/0012-hermes-uscita.md)) |
| Modelli | Claude via API per tutti gli agenti ([ADR-0025, «Contesto»](adr/0025-un-modello-per-agente.md)) | un modello per agente, anche open-weight, tutti dietro LiteLLM ([ADR-0025](adr/0025-un-modello-per-agente.md)) |
| Abbonamenti | Claude Team per le persone; gli agenti mai sui posti Team ([ADR-0028, «Contesto»](adr/0028-instradamento-a-piu-motori.md)) | Managed Agents come riserva sui dati verdi ([ADR-0024](adr/0024-abbonamenti-come-riserva.md)); dall'11 novembre i posti Team servono la corsia T, mentre il motore non usa mai il loro login ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)) |
| Spese | quelle della proposta v2.1 ([proposta §12](../PRESENTAZIONE-CEO.md)) | nessun canone nuovo nella base; la spesa una tantum resta di circa 2.900-3.890 €, e la revisione esterna da 3.560-5.940 € diventa facoltativa ([ricerca/45 §9.1 e §9.2](../ricerca/45-architettura-v3.md)) |
| Giorni di sviluppo | la stima della [proposta §15](../PRESENTAZIONE-CEO.md) | da rifare con Mattia, pezzo per pezzo ([ricerca/45 §9.3](../ricerca/45-architettura-v3.md)): la corsia S è anticipata, e la milestone 1 comprende anche il «decisore», il registro dei modelli e i testi letti da file, lavoro che la stima di [ricerca/45 §12.1](../ricerca/45-architettura-v3.md) non prevedeva ([ADR-0027](adr/0027-decisore.md)) |

## 10. Valutazioni del 10 novembre dopo il terzo giro

Il 10 novembre, subito dopo il terzo giro, Alberto ha fatto tre domande. Ognuna ha avuto un rapporto e una decisione registrata. L'11 novembre se n'è aggiunta una quarta, sull'instradamento (§10.4).

### 10.1 Obsidian e la casa dei testi

- **La domanda.** Alberto ha chiesto: «valuta anche Obsidian, è già stato giudicato?». Obsidian è un editor di note in file Markdown; la domanda è se possa essere la casa dei testi che gli agenti leggono e scrivono: playbook, verbali, regole «Come lavoro» e voce del brand ([ricerca/46, intestazione](../ricerca/46-obsidian-come-casa-dei-testi.md); [ADR-0005, revisione del 10 novembre](adr/0005-memoria-postgres-qdrant-bookstack.md)).
- **L'esito.** Obsidian non è la casa dei testi: da solo non ha permessi né accesso unico, e per più persone chiede Sync, un cloud fuori dal board. Resta al massimo un editor facoltativo sul PC. La partita vera è fra BookStack e una cartella di file Markdown in git: nei voti la cartella è avanti, 66,5 contro 63,5 su 100, ma la differenza sta dentro l'incertezza dei voti e il suo lavoro non è stimato ([ricerca/46, «In breve»](../ricerca/46-obsidian-come-casa-dei-testi.md)).
- **Dove sta la decisione.** [ADR-0005, revisione del 10 novembre](adr/0005-memoria-postgres-qdrant-bookstack.md): BookStack resta in vigore e la scelta si fa prima della fase 2, con le prove di [ricerca/46 §9](../ricerca/46-obsidian-come-casa-dei-testi.md). Intanto, nella milestone 1, i testi stanno in file Markdown e YAML nella repo del codice, letti da un'interfaccia unica.

### 10.2 I modelli System One e il «decisore»

- **La domanda.** Valutare i modelli «System One», come Jev e OpenJev, messi a monte dei modelli pesanti. Un System One non scrive testo: riceve uno stato e domande chiuse (sì o no, scelta, punteggio) e restituisce una probabilità per ogni risposta ([ricerca/47, intestazione e «In breve»](../ricerca/47-modelli-system-one.md)).
- **L'esito.** Il guadagno non è il risparmio, che vale poche decine di dollari al mese [stima]: è avere probabilità e soglie scritte in un file. Nasce il «decisore», un'interfaccia unica nel nostro codice, con le soglie in `config/decisore.yaml`. Serve a smistare gli eventi, a controllare il contenuto prima di un'uscita L2 o L3, a leggere le risposte degli esterni e a capire il colore dei dati. Una sua risposta può solo rendere il sistema più prudente: non sceglie mai un destinatario e non alza mai un livello. Nella milestone 1 c'è l'interfaccia, con un decisore a copione e uno su un modello a schema; nella milestone 2 la prova in italiano su circa 850 casi ([ADR-0027](adr/0027-decisore.md)).
- **L'11 novembre**, per decisione di Alberto, l'italiano non è più un freno: Jev, fissato alla versione 1.14.0 e chiamato via LiteLLM, è il motore di partenza del decisore sui testi verdi, e su quelli gialli quando Michele ammette il fornitore. Per i testi rossi o di colore ignoto restano un modello in casa o le regole. La prova in italiano serve a tarare le soglie ([ADR-0027, revisione dell'11 novembre](adr/0027-decisore.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- **Il 12 novembre**, con le scelte della milestone 2, Jev entra nella milestone 3 con LiteLLM; fino ad allora il decisore gira sul copione, su un modello a schema e su un decisore in casa che legge la probabilità della prima parola ([ricerca/51](../ricerca/51-modelli-open-weight-sul-computer-di-sviluppo.md)). Nella milestone 2 si tarano solo il controllo del contenuto e le risposte degli esterni; le due settimane di prova ombra si spostano a quando ci sono eventi veri, nelle milestone 5 e 6 ([ADR-0027, revisione del 12 novembre](adr/0027-decisore.md)).
- **Dove sta la decisione.** [ADR-0027](adr/0027-decisore.md).

### 10.3 Modelli locali, multimodalità e GPU

- **Le domande.** Mettere sul server Whisper e altri modelli piccoli, collegati a LiteLLM, oppure usare OpenRouter per quelli che non ospitiamo. E se serve un modello multimodale, cioè che vede immagini e ascolta audio, anche come orchestratore ([ricerca/48, intestazione](../ricerca/48-modelli-locali-e-gpu.md)).
- **L'esito.**
  - Whisper e i modelli piccoli sì, dietro LiteLLM come gli altri; OpenRouter solo per i dati verdi e gialli, e solo per un modello che Claude non ha e che noi non ospitiamo ([ADR-0025, aggiornamento del 10 novembre](adr/0025-un-modello-per-agente.md)).
  - I modelli multimodali servono come occhi e orecchie, non come orchestratore: lo smistamento lo fa il codice, e l'unico smistatore libero, il Capo di gabinetto, è Claude, che vede già immagini e PDF. Per i dati rossi da guardare, come scansioni e slide condivise in una call, lavora in casa un modello da 9 miliardi di parametri ([ADR-0025, aggiornamento del 10 novembre](adr/0025-un-modello-per-agente.md)).
  - Nasce il registro dei modelli, `config/modelli.yaml`, con fornitore, costi, capacità e colori dei dati ammessi per ogni modello ([ADR-0025, aggiornamento del 10 novembre](adr/0025-un-modello-per-agente.md)).
  - La seconda GPU resta la RTX PRO 2000 Blackwell da 16 GB, da comprare per la milestone 2 anche a 1.100 €, più il riser se manca (75-160 €): la prova dei modelli locali ne ha bisogno, perché la RTX 4000 è già piena. La scheda da 24 GB a 70 W costa più di tre volte, circa 3.750-4.100 €, e non si compra ora ([ADR-0014, seconda revisione del 10 novembre](adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md)).
- **Dove sta la decisione.** [ADR-0025](adr/0025-un-modello-per-agente.md) per i modelli e [ADR-0014](adr/0014-seconda-gpu-blackwell.md) per la GPU, che resta una proposta a Michele.

### 10.4 L'11 novembre: instradamento a più motori

- **La domanda.** Alberto ha dato tre direttive: per i modelli System One l'italiano non è un problema; serve un instradamento che colleghi Jev, i modelli open-weight sul server e le sessioni di Claude Team; per i compiti costosi, come lo sviluppo di progetti in codice, il sistema deve saper avviare sessioni di Claude Code sui posti Team ([ricerca/49, intestazione](../ricerca/49-instradamento-a-piu-motori.md)).
- **L'esito.**
  - Un router nel motore sceglie la destinazione di ogni lavoro fra sei: una regola nel codice; una catena N su un modello open-weight sul nostro server; una catena N su Claude via API; una sessione S con la chiave API; la **corsia T**, cioè una sessione di Claude Code su un posto Claude Team; una persona ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
  - La corsia T parte solo con il meccanismo che Anthropic offre per questo, il compito programmato con avvio via API, sul posto della persona responsabile. Consegna solo una pull request in bozza, che entra nel codice con il sì di una persona; non ha connettori e non riceve mai dati rossi. Serve lo sviluppo di progetti in codice e i lavori lunghi di quattro agenti: Sviluppatori, Agente sito e SEO, Pipeline per il portale clienti, Sistemista ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
  - La regola «mai i posti di Claude Team» oggi vale per il motore: il motore non usa mai il login di un posto, perché i termini di Anthropic lo riservano all'uso normale di Claude Code ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
  - **Costi.** Il router e l'adattatore di prova della corsia T valgono circa 4-6 giorni di sviluppo in più [stima di ricerca/49]. Lo sviluppo pesante pagato a token costerebbe circa 7-14 $ per mezza giornata [stima di ricerca/49], mentre la corsia T usa i posti già pagati ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). Il piano Team include fino a 500 $ al mese di crediti API, che coprono l'API e l'Agent SDK ma non Claude Code; se ne ha diritto anche il nostro piano va controllato ([ricerca/49, «In breve»](../ricerca/49-instradamento-a-piu-motori.md)).
  - **Il 12 novembre** il router entra nella milestone 2 del PRD, sul decisore che c'è, con la corsia T come destinazione di prova. La prova dal vivo dei passi di ricerca/49 §7 la fa Alberto dal suo account; l'adattatore che avvia davvero la corsia T si scrive dopo. Jev con LiteLLM resta nella milestone 3 ([ADR-0028, revisione del 12 novembre](adr/0028-instradamento-a-piu-motori.md)).
- **Dove sta la decisione.** [ADR-0028](adr/0028-instradamento-a-piu-motori.md), accettata dal gruppo di progetto. La corsia T entra solo dopo la prova di [ricerca/49 §7](../ricerca/49-instradamento-a-piu-motori.md) e la conferma scritta di Anthropic.

## Dove approfondire

- **La scelta e i numeri**: [proposta §5.3, §5.7 e appendice B](../PRESENTAZIONE-CEO.md).
- **Primo giro**: le sette proposte, [A](../ricerca/20-proposta-A-hermes.md), [B](../ricerca/20-proposta-B-buzz.md), [C](../ricerca/20-proposta-C-grokbot.md), [D](../ricerca/20-proposta-D-openai-dots.md), [E](../ricerca/20-proposta-E-claude-native.md), [F](../ricerca/20-proposta-F-paperclip.md) e [G](../ricerca/20-proposta-G-ibrido.md); i quattro giudizi, [visione](../ricerca/21-giudizio-visione.md), [commerciale](../ricerca/21-giudizio-ceo.md), [tecnica](../ricerca/21-giudizio-cpto.md) e [privacy](../ricerca/21-giudizio-compliance.md); la scelta di allora in [ricerca/22](../ricerca/22-architettura-scelta.md); la critica di completezza in [ricerca/23](../ricerca/23-critica-completezza.md).
- **Il board di Michele**: [il board](../allegati/infra/SerSan%20Infra%20Board.md), [la board del rack](../allegati/infra/Rack%20SerSan%2012U.md) e il confronto con la proposta in [ricerca/25](../ricerca/25-board-michele-e-delta.md).
- **Agent SDK e Hermes dentro il board**: [ricerca/26](../ricerca/26-claude-agent-sdk.md) e [ricerca/27](../ricerca/27-hermes-self-hosted.md).
- **Secondo giro**: le tre proposte, [1](../ricerca/34-proposta-1-agent-sdk.md), [2](../ricerca/34-proposta-2-hermes-self-hosted.md) e [3](../ricerca/34-proposta-3-claude-team-e-mcp.md); i quattro giudizi, [visione](../ricerca/35-giudizio-visione.md), [commerciale](../ricerca/35-giudizio-ceo.md), [tecnica](../ricerca/35-giudizio-cpto.md) e [sicurezza](../ricerca/35-giudizio-sicurezza.md); l'architettura scelta in [ricerca/36](../ricerca/36-architettura-v2.md).
- **Terzo giro**: i quattro rapporti di partenza, [ricerca/38](../ricerca/38-autonomia-nella-trascrizione.md), [39](../ricerca/39-autonomia-del-disegno-v2.md), [40](../ricerca/40-alternative-e-autonomia.md) e [41](../ricerca/41-novita-al-9-novembre.md); le quattro proposte, [A](../ricerca/42-proposta-A-motore-a-livelli.md), [B](../ricerca/42-proposta-B-orchestratore-pronto.md), [C](../ricerca/42-proposta-C-ibrido-abbonamenti.md) e [D](../ricerca/42-proposta-D-automazione-prima.md); i quattro giudizi, [visione](../ricerca/43-giudizio-visione.md), [CEO](../ricerca/43-giudizio-ceo.md), [CPTO](../ricerca/43-giudizio-cpto.md) ed [essenziale](../ricerca/43-giudizio-essenziale.md); le [verifiche avversarie](../ricerca/44-verifiche-avversarie.md); l'architettura v3 in [ricerca/45](../ricerca/45-architettura-v3.md); le decisioni nelle [ADR da 0020 a 0026](adr/README.md).
- **Dopo il terzo giro**: la casa dei testi in [ricerca/46](../ricerca/46-obsidian-come-casa-dei-testi.md), il «decisore» in [ricerca/47](../ricerca/47-modelli-system-one.md), modelli locali e GPU in [ricerca/48](../ricerca/48-modelli-locali-e-gpu.md), l'instradamento a più motori in [ricerca/49](../ricerca/49-instradamento-a-piu-motori.md); le decisioni in [ADR-0027](adr/0027-decisore.md), [ADR-0028](adr/0028-instradamento-a-piu-motori.md) e nelle revisioni di [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), [ADR-0014](adr/0014-seconda-gpu-blackwell.md) e [ADR-0025](adr/0025-un-modello-per-agente.md).
- **Le scelte della milestone 2, 12 novembre**: l'Agent SDK con la prova a copione in [ricerca/50](../ricerca/50-agent-sdk-e-prova-a-copione.md), i modelli open-weight sul computer di sviluppo in [ricerca/51](../ricerca/51-modelli-open-weight-sul-computer-di-sviluppo.md); le decisioni in [ADR-0029](adr/0029-corsia-s-sessioni-a-giri.md), [ADR-0030](adr/0030-bacheca-gruppi-specchi.md) e nelle revisioni del 12 novembre di [ADR-0001](adr/0001-motore-agent-sdk.md), [ADR-0021](adr/0021-motore-a-due-corsie.md), [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md), [ADR-0027](adr/0027-decisore.md) e [ADR-0028](adr/0028-instradamento-a-piu-motori.md).
- **Le scelte puntuali**: la chat in [ricerca/28](../ricerca/28-chat-di-gruppo-self-hosted.md), le call in [ricerca/30](../ricerca/30-call-e-trascrizione-self-hosted.md), la voce di Andrea in [ricerca/31](../ricerca/31-voce-andrea-self-hosted.md), l'hardware in [ricerca/32](../ricerca/32-hardware-e-upgrade.md) e [ricerca/37](../ricerca/37-hardware-risposte-michele.md), le domande tecniche aperte in [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md).
