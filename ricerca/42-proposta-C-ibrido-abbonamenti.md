# P-C · Ibrido: agenti autonomi in abbonamento dove rendono di più

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **P-C**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Proposta d'architettura del 9/11/2026, per il confronto fra le alternative.

**Come leggere**
- **Livelli.** L0 a mano, L1 carta, L2 finestra, L3 autonomo, con il significato fissato nel compito.
- **Sigle delle fonti** (file letti tutti il 9/11/2026):
  - P = `PRESENTAZIONE-CEO.md`, la proposta v2.1;
  - SPEC = la spec della milestone 1, revisione 2;
  - PRD = `.claude/prds/sersan-agent-os.prd.md`;
  - D03 = `docs/03-architettura.md`; ADR-00NN = `docs/adr/`; DOM = `DOMANDE-PER-MICHELE.md`;
  - R00…R37 = `ricerca/NN-*.md`; R20C e R20G sono le proposte C e G del primo giro, R34-3 la proposta 3 del secondo;
  - TR = la trascrizione di riferimento, con il minuto;
  - T1, T2 e T3 = le trascrizioni di terzi sul Desktop («grokbot transcript», «Grokbot vs Hermes», «claude and grokbot updates»). Sono testimonianze, non documentazione;
  - RAP1-RAP4 = i quattro rapporti di questo giro. I fatti che si trovano solo nel RAP4 vengono da pagine web lette da quel rapporto il 9/11: li cito con l'indirizzo, ma non li ho ricontrollati io.
- **Etichette.**
  - [verificato: …] e [non verificato: …];
  - [proposta]: una scelta di disegno mia;
  - [stima]: un numero mio, non verificato.

---

## 1. L'idea in 5 righe

1. Sul server restano i dati dei clienti, le azioni verso i clienti e il Cancello, che resta l'unico esecutore. Ci stanno post-call, CRM, posta, offerte, Andrea, coaching e memoria.
2. In abbonamento girano le squadre che usano solo dati verdi: ricerca, bandi, segnali pubblici, editoriale, copy, grafiche, video, metriche e SEO. Partono subito su Claude Team e passano a Claude Managed Agents dalla fase 1. Grok Bot è lo studio facoltativo di Alberto, dopo il mese di prova.
3. Il Cancello non chiede più una carta per ogni azione: ogni classe d'azione ha il suo livello.
   - L3 per il lavoro interno.
   - L2, e poi L3, per i messaggi a destinatari noti.
   - L1 solo per offerte, prezzi, contratti, fatture e primi contatti.
4. Restano le protezioni essenziali: limiti fissi, stop, tetti, registro semplice, annulla e correggi, conformità minima. Escono la FIDO2 sulle carte, la revisione esterna e le firme crittografiche fra i nostri processi.
5. I tempi:
   - alla settimana 8 riassunti, debrief e ricerca vanno senza mani;
   - alla 21 follow-up e post aziendali partono dopo la finestra;
   - a regime il post-call è come nella trascrizione di riferimento, ma offerte e contratti li firma ancora una persona.

[proposta: tutte e cinque le righe]

---

## 2. Componenti e dove girano

### 2.1 La regola che decide il posto

- **Il posto lo decide il colore dei dati**, come nella v2.1 [verificato: P §5.6]:
  - **verde**, pubblico o interno non personale: va a qualunque fornitore ammesso;
  - **giallo**, contatti di lavoro, campi del CRM, riassunti: va solo a fornitori con contratto e DPA;
  - **rosso**, audio, trascrizioni, mail intere, documenti dei clienti, giudizi sulle persone, finanza: resta sul server, oppure va all'API di Anthropic dopo l'oscuramento locale.
- **P-C aggiunge una sola regola.** Una squadra va in abbonamento solo se tutto ciò che legge e scrive è verde. Il server le passa solo campi verdi, per esempio le obiezioni sentite in call senza nomi né aziende [proposta].
- **Le squadre in abbonamento non hanno credenziali di account aziendali.** Ci raggiungono con un token stretto, che imposta una persona. Il token apre solo le letture verdi e la proposta d'azione al Cancello, e lo stop lo revoca [proposta].
- **È un cambio di regola rispetto alla v2.** Lì Managed Agents era escluso «contro la regola tutto in casa», e i compiti programmati di Claude Team non potevano fare processi aziendali [verificato: R26 §1.2; ADR-0011]. P-C li ammette solo per il verde. Il motivo è la nuova richiesta di Alberto: scegliere anche in base all'autonomia, ammettendo l'abbonamento [proposta].

### 2.2 Tabella dei componenti

**Sul server, dentro il board di Michele**

| Componente | Cosa fa in P-C | Dove | RAM | GPU | Fonte |
|---|---|---|---|---|---|
| Motore sull'Agent SDK | agenti con dati gialli e rossi: Outbound, Chiamate, Vendite, Progetti, Memoria, Direzione, Amministrazione | stage in LAB nelle fasi 1-2, poi VM `agenti-01` | 12 GB con 6 sessioni; a regime 16 GB invece di 20, perché circa 12 agenti stanno in abbonamento | no | RAM per sessioni [verificato: R36 §4.1]; riduzione [stima] |
| Cancello e Porta Teams | livelli L0-L3, finestra con «Ferma», tetti, registro, annulla, stop, carte in Teams | VM `cancello-01` | 3-4 GB + 0,5-1 GB | no | [verificato: R36 §4.1] |
| Server MCP e ponte per gli abbonamenti | letture e bacheca; alle fonti esterne solo letture verdi e `propose_action` | LXC `mcp-01`; endpoint pubblico via Pangolin dalla fase 2 | 3-4 GB, +0,5 per il ponte | no | MCP [verificato: R36 §4.1]; Pangolin sulla macchina Oracle [verificato: D03 §3.4]; ponte [proposta, stima] |
| n8n, LiteLLM, PostgreSQL, Qdrant, BookStack con MariaDB, Infisical | come nella v2 | board | come nella v2 | RTX 4000 per embedding e ricerca | [verificato: R36 §4.1] |
| Trascrizione e Vexa | come nella v2, dalla fase 3 | VLAN 80 e 35 | 6-8 GB; Vexa 12 GB (circa 4 con Vexa Lite) | 2-4,5 GB di giorno | [verificato: R36 §4.1] |
| Andrea (Asterisk, Pipecat, Haiku via LiteLLM) | come nella v2, ma pronta una fase prima se ci sono lead e parere | VLAN 25 e APPS | 1 GB + 6-8 GB su CPU; 4 GB con la seconda GPU | parte su CPU; seconda GPU consigliata | [verificato: R31 In breve, §8; R36 §4.1] |
| listmonk con relay SMTP | invio della newsletter; la lista degli iscritti è gialla e resta qui | APPS | 0,5 GB | no | [verificato: R36 §4.1] |
| DocuSeal, fatturazione | come nella v2, fase 6 | APPS | 2,5 GB | no | [verificato: R36 §4.2] |
| Postiz | non si installa: lo sostituisce Metricool | — | −2 GB | — | 2 GB [verificato: R36 §4.1]; scelta [proposta] |

**Cloud del board, invariato:** M365 e Teams, Claude Team, API Anthropic dietro LiteLLM, Jira, Instantly [verificato: P §5.1].

**Abbonamenti di P-C**

| Servizio | Ruolo | Dati | Costo | Fonte |
|---|---|---|---|---|
| Compiti programmati di Cowork (Claude Team) | squadre in abbonamento delle settimane 1-8: ricerca concorrenza, bandi, bozze del calendario, numeri del lunedì | solo verdi; connettori in sola lettura | 0 € in più: sono nel bundle | girano a computer spento, con skill e connettori [verificato: R34-3 §2]; i connettori lasciati in scrittura saltano il Cancello [verificato: ADR-0003]; l'amministratore controlla i connettori [verificato: R34-3 §2] |
| Claude Managed Agents | base delle squadre in abbonamento dalla fase 1: sessioni a orario, sandbox nel cloud di Anthropic, ricerca web, MCP verso il nostro ponte | solo verdi | 0,08 $ per ora di sessione attiva, più i token sulla chiave API, più 10 $ ogni 1.000 ricerche | prezzi [verificato: R18 §2.1]; cron, sandbox anche in casa, niente ZDR, beta [verificato: R12 §1]; tetto per sessione e politica `auto` [verificato dal RAP4 §2.2: platform.claude.com, release notes, 9/11] |
| Grok Bot (facoltativo) | studio di Alberto per grafiche, video e ricerca: bot con nome, chat di gruppo, routine, browser nel cloud, «Teach a task» | solo verdi; nessun login ad account aziendali che pubblicano o pagano | mese di prova circa 54 €, poi 30-100 $ a posto | [verificato: P §14 decisione 23; R11 §2 e §4.1] |
| Metricool | il Cancello ci programma i post della pagina aziendale e dei profili collegati | testi dei post, verdi | 59,86 €/mese | prezzo [verificato: R36 §8.2]; pubblica già pagina LinkedIn, Instagram e Facebook [verificato: R33 §2.5] |
| Higgsfield | video e immagini | verdi | 41,99 €/mese, già nella decisione 15 | [verificato: R36 §8.2] |
| Operatore telefonico, relay SMTP, WhatsApp, Telegram, Slack | come nella v2 | — | come nella v2 | [verificato: P §12.1] |

**Valutati alla pari e lasciati fuori dalla base**
- **Copilot Studio.**
  - A favore: ha trigger autonomi sugli eventi di M365 e tiene i dati nella geografia britannica.
  - Contro: gira con le credenziali di chi crea l'agente, e ogni evento si paga in crediti [verificato dal RAP4 §6: learn.microsoft.com, authoring-triggers-about e requirements-messages-management, 9/11].
  - Per quattro persone non fa nulla che Managed Agents e n8n non facciano già [proposta].
- **OpenAI Dots.**
  - Dà un solo dot per persona; nel Regno Unito solo con Business Premium, a 125 $ a posto e minimo 2 posti.
  - Non ha webhook generici [verificato: R18 §2.2].
- **Claude Tag.** Funziona solo in Slack; per Teams c'è solo una lista d'attesa [verificato: R28 §2.5; R34-3 §2].
- **Hermes Cloud.** Resta una variante del runtime in abbonamento: ha la regione di Londra e skill che si curano da sole [verificato: R18 §2.4]. Non lo prendo come base per due motivi:
  - i prezzi delle istanze vengono in parte da terzi [verificato: R18 §2.4];
  - le conversazioni dei profili si mescolano [verificato: RAP3 §1, da R10; T2, testimonianza].
- **Hermes sul server, Buzz e Paperclip.** Restano come nella v2.1: uscita prezzata e prove in LAB [verificato: P §5.7, §4.11, §4.12].

### 2.3 Perché Managed Agents come base e Grok Bot solo come studio

| Criterio | Managed Agents | Grok Bot | Cowork (Claude Team) |
|---|---|---|---|
| Autonomia pronta | sessioni a orario, sandbox, MCP [verificato: R12 §1]; più agenti, obiettivi e tetto per sessione [RAP4 §2.2] | routine a orario, su eventi e webhook; un bot principale che delega; chat da 2 a 6 bot; skill che si correggono [verificato: R11 §2.4-2.5] | compiti orari, giornalieri o settimanali a computer spento [verificato: R34-3 §2] |
| Semplicità | API e configurazione nostra | app pronta [verificato: R11 §1] | già in uso dalla fase 0 |
| Tempo al valore | 1-2 settimane [stima] | debrief e brief su dati pubblici in 2 settimane [verificato: R20C §6] | giorni [stima] |
| Costo | 0,08 $/h più token, sulla chiave API [verificato: R18 §2.1] | 30-100 $ a posto più crediti; la quota settimanale non è pubblicata [verificato: R11 §4.1] | 0 € nel bundle |
| Collegamento con Cancello e Teams | lo comandiamo noi via API e MCP; gli esiti arrivano in Teams dalla Porta | MCP remoto solo per i Team Bots, nessuna API per comandare i bot, Team Bots solo in Slack [verificato: R11 §2.5, §6] | connettori MCP; agisce a nome della persona [verificato: R34-3 §2] |
| Dati | USA, niente ZDR [verificato: R12 §1]; termini commerciali di Anthropic [verificato: R16 §5] | USA, modello invisibile, audit solo Enterprise; i termini chiedono una revisione umana prima delle comunicazioni esterne [verificato: R11 §1, §2.6, §7.4] | USA; il piano Team non ha log di audit [verificato: R36 §1.3] |
| Ruolo in P-C | base dalla fase 1 | studio facoltativo dopo la prova | ponte nelle settimane 1-8 e strumento personale |

### 2.4 RAM e GPU fase per fase

| GB nuovi sul server | Fase 1 | Fase 2 | Fase 3 | Fase 4 | Fasi 5-6 |
|---|---|---|---|---|---|
| v2.1 | 8 | 25 | 53,5 (fasi 3-4 insieme) | | 70-74 |
| P-C | 8 | circa 25,5 | circa 51,5 | circa 59,5 se Andrea parte su CPU | circa 64-68 |
| P-C, liberi con 192 GB (oggi ne restano 53) | circa 45 | circa 27,5 | circa 1,5 | circa −6,5 | da circa −11 a −15 |
| P-C, liberi con 384 GB | | | circa 193 | circa 185 | circa 177-181 |

[verificato: v2.1 da R36 §4.2 e P §6.3; P-C: stima mia, con −2 GB di Postiz, −4 GB del motore a regime, +0,5 GB del ponte e +8 GB di Andrea su CPU nella fase 4]

**Lettura**
- **RAM.** I 192 GB in più (690-830 €) servono comunque prima della fase 3, come nella decisione 11 [verificato: P §6.3, §14].
- **GPU.** Le squadre in abbonamento non usano la nostra GPU.
  - La seconda GPU (880-1.220 €) conviene già all'inizio della fase 3, come dice la v2.1 [verificato: P §6.4, §12.2].
  - Con Andrea in fase 4 diventa la scelta consigliata, non un'opzione [proposta].

---

## 3. Il modello di autonomia

### 3.1 La scala comune

**I gruppi di destinatari** [proposta]
- **Interno.** Persone di SerSan, canali interni, CRM, Jira, calendario.
- **Noto.** Chi ha partecipato a una call registrata con noi negli ultimi 30 giorni, o ha uno scambio nel CRM negli ultimi 90.
- **Nuovo.** Tutti gli altri.

Le destinazioni ammesse si calcolano dai dati. Non si prendono mai dal testo di una mail in arrivo: è anche la difesa più economica contro le iniezioni di prompt [proposta].

**Come si sale** [proposta]
- **Da L1 a L2:** dopo 5 carte di fila approvate senza modifiche di sostanza, nella stessa classe e nello stesso gruppo.
- **Da L2 a L3:** dopo 10 esecuzioni di fila senza «Ferma», senza correzioni e senza reclami.
- **Chi conferma la salita:** il responsabile della classe, con un tocco.
  - Alessandro per i clienti, Alberto per le pubblicazioni, Michele per offerte e affermazioni tecniche [verificato: P §4.12; D03 §4.1].
- **Le soglie a confronto.** Le regole «Sempre» della v2 chiedono 20 sì per una sola destinazione e scadono dopo 30 giorni [verificato: P §5.4; R36 §5.8].
  - Con i numeri di oggi non si raggiungono [verificato: RAP2, collo di bottiglia 2].
  - Al 5/10 c'erano 11 lead, 1 risposta e 0 meeting [verificato: P §7.1]. Anche le soglie di P-C chiederanno quindi settimane o mesi [stima].

**Come si scende**, in automatico [proposta]
- Un «Ferma», un rifiuto, una correzione dopo l'invio, un reclamo o un rimbalzo: la classe scende di un livello per quel gruppo.
- Due episodi in 30 giorni: la classe torna a L1.
- Un'azione oltre il tetto diventa una carta.
- Lo stop di emergenza porta tutto a L0.

**I tetti** [proposta]
- **Mai sopra L1:** offerte, prezzi, contratti, fatture e solleciti, primi contatti a freddo, risposte a destinatari nuovi.
- **Mai:** cancellazioni, credenziali e pagamenti. Sono i limiti fissi.
- **Finestre:** 30-60 minuti per i messaggi dopo una call; 24 ore per post e newsletter.
- **Tetti di partenza:**
  - 15 follow-up e 10 inviti al giorno;
  - 3 post aziendali al giorno, una newsletter al mese;
  - le chiamate di Andrea, nei limiti delle linee che abbiamo.

**Scadenze e trasparenza** [proposta]
- **Nessuna scadenza automatica dei livelli.** Ogni mese il resoconto elenca le classi attive con i loro numeri, e un tocco abbassa una classe.
- **Nota AI.** Un messaggio L2 o L3 verso un esterno porta una riga che dice che l'ha preparato l'assistente AI, finché il parere non dice altro.
  - La regola 1 chiede di dichiararsi AI a chi scrive «da solo» [verificato: P §9.1]. Che valga anche per L2 è una mia proposta.

### 3.2 I nove flussi

**1. Dopo una call: riassunto, canale del cliente, CRM, mail di follow-up, to-do**
- **Dove gira:** sul server, perché la trascrizione è rossa [verificato: P §5.6].
- **Riassunto nel canale interno del cliente:**
  - L3 dalla settimana 8, a regime L3;
  - la v2.1 lo prevede già [verificato: P §1], ma nello SPEC manca ancora il tipo d'azione [verificato: SPEC §4.6].
- **CRM, meeting e prossima azione:**
  - L3 dalla settimana 8, se anticipiamo l'MCP di SersanOutreach su HTTP, che costa 3,5 gp ed è oggi nella fase 2 [verificato: R36 §7.3];
  - senza l'anticipo, alla settimana 8 il meeting va nel registro in PostgreSQL;
  - «crea deal» è L3 dalla fase 2 [verificato: P §7.3].
- **To-do:** L3 come lista dentro il riassunto dalla settimana 8; in Jira dalla fase 2 [verificato: R36 §7.3].
- **Mail di follow-up:**
  - **Partenza:** L1 alla settimana 8, se il parere della settimana 3 ammette invii veri [verificato: PRD, «Domande aperte»].
  - **Poi:** L2, con una finestra di 30-60 minuti.
  - **A regime:** L3 verso i partecipanti esterni della call registrata, anche per il primo follow-up [proposta].
  - **Si scende** con una correzione, un reclamo, o un destinatario che non era nella call.
- **Canale condiviso con il cliente** (Teams condiviso, Slack, WhatsApp):
  - stessa classe della mail; L1 dalla fase 3, quando arrivano i canali [verificato: P §11];
  - a regime L2-L3.

**2. Debrief del mattino**
- **Dove gira:** sul server.
- **Livello:** L3 dalla settimana 8, con un orario sul banco di prova. Oggi non è scritto come parta il debrief nella fase 1 [verificato: RAP2, collo 7; SPEC §3].
- **Cosa contiene:**
  - il calendario in lettura, il registro dei meeting e le carte in attesa;
  - i risultati delle squadre in abbonamento [proposta].
- **Dalla fase 2:** anche come evento nel calendario, in L3 [verificato: P, appendice A, K1].
- **Discesa:** non si applica, perché è interno; chi non lo vuole lo spegne.

**3. Brief prima di un incontro, con slide**
- **Dove gira:**
  - CRM e memoria sul server, perché sono gialli;
  - la ricerca pubblica su azienda e settore, che è verde, la fa un agente in abbonamento con la ricerca web e la passa al server [proposta].
- **Partenza:** L0 nella fase 0, con la skill di Claude Team [verificato: P, appendice A, J6 e D4].
- **Dalla fase 2:** L3 automatico per ogni incontro con esterni in calendario, 18 ore prima.
  - Copre AU-19, che oggi è coperto solo in parte [verificato: RAP1 §3].
  - Le slide per noi sono L3.
- **Slide per il cliente:** L1, poi L2 come allegato del recap.
- **Limiti che restano:**
  - i post LinkedIn si leggono solo con una via consentita;
  - le aperture delle mail arrivano solo con la casella attiva [verificato: P, appendice A, D2].

**4. Offerta dopo l'incontro**
- **Dove gira:** sul server, con il catalogo, la trascrizione e Opus.
- **Bozza:** L0 con la skill nella fase 0; L3 entro un'ora dalla fase 2, se il catalogo è già in BookStack [proposta].
- **Invio:** L1 sempre, con la firma tecnica di Michele ma senza FIDO2.
  - Scope e prezzi restano umani [verificato: P §9.3].
  - La trascrizione di riferimento non dice a che livello parte l'offerta [verificato: RAP1, AU-21].

**5. Marketing: post, newsletter, ricerca concorrenza**
- **Ricerca concorrenza:** in abbonamento.
  - L3 dalla settimana 1-2 con Cowork, poi su Managed Agents.
  - Un riepilogo ogni settimana nel canale Marketing.
- **Editoriale e Copywriter:** in abbonamento.
  - Le bozze sono L3.
  - Le obiezioni arrivano dal server già senza nomi.
- **Post sulla pagina aziendale:**
  - **Settimana 8:** L1, con la programmazione ancora a mano, come chiede la regola della sessione presidiata [verificato: P §8.2].
  - **Dalla fase 2:** L2 con 24 ore di finestra; il post lo programma il Cancello su Metricool.
  - **A regime:** L3 per i post dentro il calendario del mese, che si approva una volta in L1, e per i rilanci [proposta].
  - Serve cambiare la regola della sessione presidiata: decide Alberto.
- **Post dei founder:**
  - L1 sempre, perché la voce dei founder resta umana per scelta [verificato: P §9.3];
  - dopo il sì li programma il Cancello, quindi sparisce il passo L0.
- **Newsletter:**
  - la bozza è L3, in abbonamento; l'invio parte da listmonk sul server;
  - la prima uscita è L1, nella fase 3 invece che nella 4;
  - dopo 3 uscite senza modifiche di sostanza passa a L2, con 24 ore di finestra. Con 20 sì per ogni regola servirebbero quasi due anni [verificato: RAP2, voce K9].
- **Si scende** con un post corretto o rimosso, un reclamo o un errore di brand: la classe torna a L1.

**6. Andrea, la richiamata entro 90 secondi**
- **Dove gira:** sul server, perché voce e numero del lead sono dati personali.
- **Livello:** L3 per sua natura, perché in 90 secondi non entra nessuna finestra.
- **Regole** [verificato: P §9.1, regole 1 e 4; R31 §9]:
  - chiama solo chi ha dato il consenso nel modulo;
  - si dichiara AI;
  - si controlla ogni mese il Registro delle opposizioni.
- **Come sale:**
  1. prova a secco sui nostri numeri;
  2. L3 in orario d'ufficio;
  3. poi giorno e notte. Di notte richiama solo chi ha scelto «adesso» [verificato: R31 §9, proposta di quel rapporto].
- **Quando:** pronta nella fase 4 se ci sono lead vere e il parere; altrimenti resta nella fase 5. Vale la regola «prima il funnel» [verificato: P §11].
- **Chiamate in entrata:** L3 dopo 20 secondi di squillo sulle persone [verificato: R31 §10, proposta].
- **Si scende** a richiamata umana (L0) per un reclamo, un consenso mancante, un «no» non registrato o una latenza oltre la soglia.

**7. Coaching delle vendite**
- **Dove gira:** sul server, perché contiene giudizi sulle persone.
- **Livello:** L3 verso chi ha fatto la call, dalla fase 3, per chi lo sceglie (oggi vende Alessandro) [proposta]. Nella v2.1 era nella fase 5 [verificato: P §4.3].
- **Al responsabile:** solo dati aggregati, e nessuna emozione stimata [verificato: P §9.1 r3; R16 §1.2].
- **Non sale oltre:** nella trascrizione di riferimento il report va anche al responsabile [verificato: RAP1, AU-30]. Dipende dal parere.

**8. Agenti che si parlano e chiudono i to-do superati**
- **Dove gira:** la bacheca sta sul server; gli agenti in abbonamento ci entrano dal ponte, solo con compiti verdi.
- **Dalla fase 2:**
  - I passaggi fra agenti sono L3, nel canale «Agenti».
  - Il freno guarda i giri a vuoto e la spesa della catena, non più tre passaggi fissi.
  - Le catene note si approvano una volta, con un loro tetto. Per esempio il post-call, che coinvolge sei agenti [verificato: P §4.10, §4.11; proposta].
- **Chiusura dei to-do:**
  - fra agenti: L3;
  - delle persone: L2, con un «lo chiudo domani se non dici no» invece del sì esplicito della v2 [verificato: R36 §5.4; proposta].
- **Riunione settimanale degli agenti**, che copre AU-09 [proposta]:
  - il Capo di gabinetto passa la bacheca;
  - chiude i compiti superati fra agenti;
  - propone le chiusure alle persone.

**9. Apprendimento dai rifiuti**
- **Andrea (G6):**
  - ogni settimana analizza i rifiuti, e due aperture nuove entrano nel test A/B in L2, con 24 ore di finestra al founder;
  - la frase che dichiara l'AI resta bloccata [verificato: R31 §9-10];
  - se gli appuntamenti calano o arriva un reclamo, torna da sola all'apertura precedente;
  - a regime resta L2 [proposta].
- **Skill degli agenti sul server (A6):**
  - oggi passano da una pull request con FIDO2, cioè L1 [verificato: R36 §5.8; P, appendice A, A6];
  - in P-C le propongono gli agenti e si uniscono da sole dopo 24 ore se passano le prove d'esempio, cioè L2 [proposta].
- **Squadre in abbonamento:** L3 sulle proprie skill e memorie, perché producono solo bozze interne.
- **Si scende:** se una prova d'esempio fallisce, la skill torna indietro da sola.

### 3.3 Confronto con la trascrizione di riferimento

| Flusso | Trascrizione di riferimento | P-C a regime | Perché la differenza |
|---|---|---|---|
| Post-call | L3, «in modo totalmente autonomo» [verificato: TR 4:42-5:07] | L3 per l'interno e per il follow-up ai partecipanti; L2-L3 per il canale condiviso | finestra solo all'inizio; nota AI |
| Debrief | L0, lo fa la persona [verificato: RAP1, AU-14] | L3 | oltre la trascrizione |
| Brief | L0, parte dall'email inserita [verificato: RAP1, AU-19] | L3 automatico | oltre la trascrizione |
| Offerta | livello non detto [verificato: RAP1, AU-21] | bozza L3, invio L1 | prezzi e impegni restano umani |
| Andrea | L3 su ogni lead, 24 ore su 24 [verificato: TR 14:53-16:02] | L3 su chi ha dato il consenso | consenso alle chiamate automatiche [verificato: R16 §2] |
| Coaching | L3 al venditore e al responsabile [verificato: RAP1, AU-30] | L3 alla persona, aggregati al responsabile | parere legale |
| Agenti che si parlano | L3 [verificato: RAP1, AU-07 e AU-09] | L3 fra agenti, L2 sui to-do delle persone | |
| Rifiuti | L3 [verificato: RAP1, AU-33] | L2 | uno sguardo a settimana costa poco, mentre al telefono si rischia la reputazione [proposta] |

---

## 4. Le protezioni essenziali

### 4.1 Le sei protezioni

**1. Limiti fissi**
- Il Cancello nega sempre cancellazioni, credenziali e pagamenti [verificato: SPEC §4.6; D03 §4.1].
- Le squadre in abbonamento non hanno né credenziali né carte di pagamento.
- Grok Bot ha da poco un deposito di carte e login: non lo usiamo [verificato: R11 §2.3, voce di terzi].

**2. Stop di emergenza**
- Un pulsante in Teams, più un avviso con ntfy.
- Ferma la coda e gli esecutori, porta a zero LiteLLM, fa scattare il kill switch di SersanOutreach e mette in pausa Instantly [verificato: D03 §4.3].
- In P-C fa anche due cose in più [proposta]:
  - revoca i token del ponte;
  - sospende via API i deployment programmati di Managed Agents. Questo va provato.
- Grok Bot non si comanda da programma [verificato: R11 §6]: le sue routine si spengono dall'app. Il token revocato gli toglie comunque l'accesso a dati e Cancello.

**3. Tetti**
- LiteLLM per agente, squadra e persona [verificato: P §5.1].
- Una chiave API per ogni agente in abbonamento, con il suo rendiconto [verificato dal RAP4 §2.3: Usage and Cost Analytics API, 29/10].
- Il tetto per sessione di Managed Agents [RAP4 §2.2].
- Il tetto mensile del saldo di Grok Bot [verificato: R11 §4.1].
- Tetti giornalieri per classe d'azione nel Cancello [proposta].

**4. Registro semplice**
- Una sola tabella a sola aggiunta: chi, cosa, livello, destinazione, chi ha approvato o fermato, costo ed esito.
- Si conserva 90 giorni [verificato: P §9.1 r8].
- Il resoconto arriva ogni sera e dentro il debrief.
- Gli agenti in abbonamento registrano ogni loro giro con uno strumento del ponte. Il prodotto da solo non basta:
  - Grok Bot tiene solo gli ultimi 20 esiti;
  - il registro delle sue azioni è solo per il piano Enterprise [verificato: R11 §2.6];
  - anche T1 consiglia di farsi un registro proprio [testimonianza].

**5. Correzione degli errori**
- Per le scritture interne c'è «annulla»: il Cancello salva l'operazione inversa e la esegue quando una persona preme.
- Per gli invii c'è «correggi»: una bozza di correzione in L1, e la classe scende di un livello.
- Un'esecuzione incerta va a una persona e non si ripete da sola [verificato: SPEC §4.8].
- Nessun doppio invio, grazie alla chiave d'idempotenza [verificato: SPEC §4.5].

**6. Conformità minima**
- **Dati e regole sui clienti**
  - colori dei dati, con solo il verde verso gli abbonamenti nuovi [verificato: P §5.6];
  - dichiarazione AI per Andrea e per chi scrive da solo (art. 50, dal 2/8/2026) [verificato: R16, sintesi p. 1];
  - avviso di registrazione [verificato: P §9.1 r2];
  - consenso per le chiamate automatiche e Registro delle opposizioni [verificato: R16 §2];
  - una sola lista di soppressione [verificato: R16 §6 r5];
  - nessun primo contatto a freddo verso l'Italia senza consenso, salvo parere diverso [verificato: R16 §3];
  - niente stima delle emozioni [verificato: R16 §4].
- **Obblighi dell'azienda**
  - registro dei trattamenti e DPIA [verificato: R16 §6 r9]. Si aggiornano a ogni nuovo trattamento invece che a ogni nuovo agente [proposta, da confermare nel parere];
  - scadenze di conservazione [verificato: P §9.1 r8];
  - formazione AI documentata [verificato: P §10];
  - backup 3-2-1 prima che i dati dei clienti restino sul server. È sicurezza del trattamento (art. 32), non un cancello in più [verificato: P §13; DOM n. 14].

### 4.2 Cosa si toglie rispetto alla v2.1 e allo SPEC

**Escono**
- **FIDO2.** Esce come secondo passo delle carte [verificato: P §5.4]. Le chiavi restano solo se Michele le vuole per l'accesso al board con NetBird ed Entra [verificato: R36 §6; P §12.2].
- **Revisione esterna di Cancello, motore e bot.** Costava 3.560-5.940 € ed era un criterio della settimana 21 [verificato: P §11, §14 decisione 5]. Al suo posto: la revisione di Mattia più un agente critico [proposta].
- **Le difese dello SPEC** [verificato: SPEC §3, §4.7, §4.9]:
  - le firme HMAC con ora e numero monouso fra i nostri processi;
  - il registro a catena con MAC e ancora esterna;
  - l'impronta calcolata dalla Porta e i codici per ogni consegna;
  - le tre barriere sugli strumenti provate una per una.
- **I vincoli sul giro.** «Un solo effetto per giro» e l'elenco chiuso nel codice [verificato: SPEC §2.1, §4.6].
- **Le regole «Sempre».** Con 20 sì, scadenza a 30 giorni e revisione mensile [verificato: R36 §5.8].

**Cambiano**
- La scadenza unica delle carte a 48 ore [verificato: SPEC §9, D1] diventa una scadenza per classe.
- La prova a secco di 1-2 settimane [verificato: P §9.2] dura fino a 10 casi di fila senza errori [proposta].

**Restano**, perché costano poco ed evitano danni veri [verificato: SPEC §4.4, §4.5, §4.9]:
- l'idempotenza;
- i segreti oscurati nei registri;
- il blocco se il Cancello non risponde;
- la chiave degli agenti che non può approvare;
- la lettura separata della posta che arriva da sconosciuti.

### 4.3 Cosa dipende dal parere legale

Il parere ha un tetto di 2.500 € [verificato: P §14, decisione 2].

1. **Follow-up in L2 e L3 senza un sì esplicito.** Bisogna capire se basta la nota AI. Secondo R16 un follow-up a un cliente appena incontrato non è marketing a freddo [verificato: R16 §3, proposta di quel rapporto]. Se il parere dice no, il follow-up resta L1.
2. **Email B2B a freddo verso l'Italia.** Il Garante chiede il consenso [verificato: R16 §3]. Da qui dipende se l'Outbound può approvare una campagna intera invece di ogni messaggio.
3. **Andrea:**
   - il testo del consenso;
   - l'art. 130 e il Registro delle opposizioni;
   - la marcatura dell'audio [verificato: R31 §9, §14].
4. **Coaching:** il confine fra coaching e valutazione dei lavoratori, e quando si applica l'art. 4 dello Statuto [verificato: R16 §1.2, §7].
5. **Registrazione delle call con clienti italiani e britannici** [verificato: P §9.4].
6. **Trasferimenti verso gli USA per gli abbonamenti:**
   - Anthropic, e Cursor per Grok Bot;
   - il DPA di Cursor non l'abbiamo letto [verificato: R11 §7.2; R16 §5].
7. **Dati rossi verso Claude Team, e l'eventuale rappresentante nell'UE** [verificato: P §5.6; R16 §0].
8. **Nota AI sui post in L2 e L3** [proposta: domanda nuova].

---

## 5. Le fasi

### 5.1 Cosa è autonomo e quando

| Pezzo | Settimana 8 | Settimana 21 | A regime |
|---|---|---|---|
| Riassunto post-call nel canale interno | L3 | L3 | L3 |
| CRM: meeting e prossima azione | L3 se anticipiamo l'MCP su HTTP; altrimenti registro in PostgreSQL | L3, anche «crea deal» | L3 |
| To-do | L3, nel riassunto | L3, in Jira | L3 |
| Mail di follow-up | L1, con il passaggio a L2 pronto | L2 con 30-60 minuti di finestra; L3 per chi ha già superato le soglie | L3 ai partecipanti della call |
| Debrief | L3, con il calendario | L3, più l'evento in calendario | L3 |
| Brief e slide per noi | L0 con la skill; ricerca pubblica L3 in abbonamento | L3 automatico per ogni incontro esterno | L3, con la memoria |
| Offerta | L0 con la skill | bozza L3, invio L1 | bozza L3, invio L1 |
| Ricerca concorrenza, bandi, segnali d'azienda | L3, in abbonamento | L3 | L3 |
| Post della pagina aziendale | L1, programmati a mano | L2 con 24 ore di finestra, dal Cancello | L3 dentro il calendario approvato |
| Post dei founder | L1, programmati a mano | L1, programmati in automatico | L1 |
| Newsletter | — | — (prima uscita nella fase 3) | L2 |
| Agenti che si parlano | — | L3 fra agenti, L2 sui to-do delle persone | idem, più la riunione settimanale |
| Andrea | — | — | L3 su chi lo chiede (fase 4 o 5) |
| Coaching | — | — | L3 alla persona, dalla fase 3 |
| Apprendimento | skill in abbonamento L3 | skill sul server L2 | aperture di Andrea L2 |

[proposta]

**Agenti al lavoro** [stima, sulla base di P §4.12]
- Settimana 8: circa 6-7, cioè 3 sul server e 3-4 in abbonamento.
- Settimana 21: circa 18-19, contro i 14 della v2.1.
- A regime: 57, di cui circa 12 in abbonamento.

### 5.2 Cosa cambia rispetto alle fasi della v2.1

- **Fase 0:**
  - le squadre in abbonamento partono su Cowork, con i connettori in sola lettura;
  - la prova di Grok Bot si fa qui, mentre la v2 la metteva dopo la fase 1 [verificato: R36 §10, decisione 23];
  - lo SPEC passa alla revisione 3, semplificata.
- **Fase 1:**
  - il Cancello v1 ha livelli, finestra, tetti, resoconto e «annulla»;
  - sul banco di prova arrivano gli orari: il debrief e la lettura delle trascrizioni ogni 5-10 minuti;
  - due agenti partono su Managed Agents. Il banco di prova apre le loro sessioni e ritira i risultati, quindi non serve nessuna porta aperta: lo stage esce solo verso internet [verificato: R36 §4.4; proposta];
  - il CRM arriva qui se anticipiamo i 3,5 gp.
- **Fase 2:**
  - L2 per follow-up, inviti e post;
  - l'esecutore di Metricool e il ponte MCP pubblico;
  - la bacheca con le catene approvate;
  - Editoriale, Copywriter, Ricerca concorrenza e Metriche girano in abbonamento e non sul motore;
  - Bandi e Sentinella arrivano dalla fase 3, solo con segnali sulle aziende;
  - grafiche e video arrivano dalla fase 4;
  - dal Cancello parte 2 escono FIDO2 e le regole «Sempre».
- **Fase 3:**
  - il brief automatico;
  - la newsletter, che arriva dalla fase 4;
  - il coaching per chi lo sceglie;
  - le risposte L2 della posta ai contatti noti.
- **Fase 4:**
  - Andrea arriva dalla fase 5, se ci sono lead e parere. I suoi 28 gp si spostano, non si aggiungono [verificato: R36 §7.3];
  - Postiz non si installa.
- **Fasi 5-6:** come nella v2.1.
- **Verifiche:**
  - alla settimana 8 il criterio diventa «nessun effetto fuori dal suo livello», invece di «nessun effetto senza carta» [verificato: P §11];
  - alla settimana 21 sparisce la revisione esterna, e restano il backup 3-2-1 e la RAM misurata.

---

## 6. Costi

### 6.1 Mensili, in più rispetto a oggi

Stesso metodo della v2.1: senza strumenti commerciali, con le API dentro i crediti e Claude Team nel bundle [verificato: P §12.1].

| Periodo | v2.1 (€/mese) | P-C (€/mese) | Cosa cambia |
|---|---|---|---|
| Fasi 0-1 | circa 135 (141) | circa 139-150 | Managed Agents dalla fase 1: circa 4-9 € fra ore di sessione e ricerche [stima su R18 §2.1] |
| Fase 2 | da −15 a +20 | da circa −2 a +55 | Managed Agents: circa 13-35 €, con 120-300 ore e 500-1.500 ricerche [stima] |
| Fasi 3-4 | da −1 a +70 | da circa +12 a +105; fino a circa +206 con Andrea in fase 4 | Andrea 44-90 € [verificato: P §12.1]; linea di riserva 10-11 € anticipata [verificato: P §14, decisione 13] |
| Fasi 5-6 | da 46 a 168 | da circa 59 a 203 | Managed Agents |

**Voci che si aggiungono** [stima, sui prezzi di R11 §4.1 e P §12.1]
- **Grok Bot**, facoltativo dalla fase 2: circa 54-205 €/mese. Si va da due posti Premium a un Super più un Premium con 100 $ di crediti.
- **Metricool** resta anche dopo la fase 4. Gli strumenti commerciali costano quindi circa 146 € invece di 86 €, cioè +59,86 €/mese.
- **Token delle squadre in abbonamento:** in gran parte si spostano dal motore. Ne stimo circa 10-40 €/mese in più, sulla stessa chiave e sotto lo stesso tetto di 250 € [stima].

### 6.2 Una tantum

| Voce | v2.1 | P-C | Fonte |
|---|---|---|---|
| Oggi: parere, credito API, backup in sede, accessori | 2.900-3.890 €, con la FIDO2 | circa 2.720-3.480 €, con la prova di Grok Bot (54 €); +232-464 € se Michele tiene le chiavi FIDO2 per l'accesso | [verificato: P §1, §12.2; calcolo mio] |
| Revisione esterna | 3.560-5.940 € | 0 € | [verificato: P §12.2] |
| RAM, 192 GB in più | 690-830 €, prima della fase 3 | uguale | [verificato: P §12.2] |
| Seconda GPU | 880-1.220 €, dalla fase 3 e al più tardi dalla 5 | 880-1.220 €, all'inizio della fase 3 | [verificato: P §6.4] |
| Linea di riserva | 77-200 €, prima della fase 5 | 77-200 €, prima che Andrea vada in produzione | [verificato: P §14] |
| Vivavoce, attivazione della linea di Andrea, voci del board | invariati | invariati | [verificato: P §12.2] |

**Saldo:** circa 3.500-6.350 € in meno di una tantum [stima].

---

## 7. Cosa cambia nella milestone 1 (lo SPEC)

### 7.1 Perimetro

- **Tipi d'azione nuovi, ognuno con il suo livello in configurazione** [proposta]:
  - `teams.canale_interno` (L3);
  - `crm.meeting` (L3);
  - `calendario.evento_interno` (L3);
  - `posta.follow_up` (L1, poi L2 e L3);
  - `post.pagina` (L1, poi L2).
- **I livelli stanno in un file di configurazione** e non più in un elenco chiuso nel codice.
- **Più scritture interne in un solo giro.** Resta un solo effetto esterno in attesa per lavoro.
- **Un ingresso per le fonti esterne:** proposte con un token per fonte, e solo i tipi ammessi per quella fonte.
- **Le letture in sola lettura sono ammesse da subito.**

### 7.2 I 27 criteri

| Criterio | In P-C | Perché |
|---|---|---|
| AC-001, AC-002 | restano | sono il percorso base |
| AC-003 (scritture interne da elenco chiuso, con trigger) | si semplifica: livelli in configurazione, più scritture per giro, niente trigger | collo di bottiglia 5 [verificato: RAP2] |
| AC-004 (Cancello che non risponde) | resta, con una variante sola | fermarsi quando il Cancello tace costa poco |
| AC-005 (un effetto per giro) | si semplifica: più effetti interni, un effetto esterno in attesa | collo di bottiglia 4 [verificato: RAP2] |
| AC-006 (tre barriere provate una per una) | **si toglie** la prova separata; la configurazione resta | sicurezza oltre il necessario |
| AC-007 (classi vietate) | resta | sono i limiti fissi |
| AC-008 (carta scaduta) | cambia: scadenza per classe; in L2 allo scadere della finestra l'azione parte | finestra |
| AC-009 (cinque varianti sull'impronta) | si semplifica: il testo non cambia dopo la carta; una modifica crea una nuova versione | resta la garanzia che esce ciò che si è visto |
| AC-010 (due approvazioni, un effetto) | resta, senza i numeri monouso | niente doppie mail |
| AC-011 (approvatori di oggi) | si semplifica: approvatore e sostituto per classe; fermano tutti e quattro | siamo in quattro |
| AC-012 (firme HMAC, numeri monouso) | **si toglie**: un token per chiamante; la chiave del motore non può decidere | sistema chiuso |
| AC-013 (testo di terzi) | si semplifica: corsia separata solo per posta e moduli da sconosciuti; per L2-L3 valgono le destinazioni ammesse | difesa economica |
| AC-014 (sola lista bianca `propose_action`) | si semplifica: schema validato, letture ammesse | gli agenti devono leggere |
| AC-015 (stop con epoche) | si semplifica: un solo interruttore; alla ripresa una persona sceglie «riprendi» o «annulla» | lo stop resta essenziale |
| AC-016 (catena con MAC e ancora) | **si toglie**: tabella a sola aggiunta e resoconto | registro semplice |
| AC-017 (segreti nei registri) | resta | costa poco |
| AC-018 (carta ferma la notte) | resta, senza il confronto dell'ambiente del processo | criterio della settimana 8 |
| AC-019 (riavvio a metà giro) | resta, con due varianti: con carta e senza carta | niente doppi effetti |
| AC-020 (tre agenti e tre runner) | si semplifica: tre agenti e un runner; più runner dalla fase 2 | |
| AC-021 (tetti con riserve fra runner) | si semplifica: tetto per lavoro e per mese, avviso all'80%, stop al 100% | i tetti sono essenziali |
| AC-022 (la sessione vede solo ciò che passiamo) | si semplifica: la configurazione resta, con una prova sola | |
| AC-023 (batteria su Windows e Linux con registro delle connessioni) | si semplifica: un comando, una piattaforma | |
| AC-024 (giro dal vivo e aggiornamento dell'SDK) | resta | l'SDK cambia spesso |
| AC-025, AC-026 | restano | niente doppie mail |
| AC-027 (carte orfane, esiti persi) | si semplifica | |

**Bilancio:** 11 criteri restano, 13 si semplificano, 3 si tolgono [proposta].

### 7.3 Criteri nuovi

[proposta]

1. **N1, livelli e tetti.** Ogni tipo d'azione ha il suo livello per gruppo di destinatari. Oltre il tetto l'azione diventa una carta. Fuori dalle destinazioni ammesse va in L1.
2. **N2, finestra L2.** La carta mostra l'ora di partenza e il pulsante «Ferma». Se nessuno ferma, l'azione parte una volta sola. Un «Ferma» in tempo non produce effetti.
3. **N3, discesa automatica.** Un «Ferma», un rifiuto o una correzione abbassano la classe di un livello. Il cambio compare nel resoconto.
4. **N4, resoconto e annulla.** Ogni azione L2 o L3 compare nel resoconto. «Annulla» esegue l'operazione inversa salvata. «Correggi» prepara una bozza in L1.
5. **N5, ingresso esterno.** Una fonte con il suo token propone solo i tipi che le sono ammessi, e non riceve mai dati rossi.
6. **N6, stop esteso.** Lo stop revoca i token delle fonti esterne e sospende le loro esecuzioni programmate.

### 7.4 Decisioni, PRD e giorni

**Decisioni dello SPEC** [verificato: SPEC §9 per quelle di oggi; proposta per le modifiche]
- D1: le carte L1 scadono dopo 72 ore; le finestre durano 30-60 minuti per i messaggi dopo una call e 24 ore per post e newsletter.
- D2: invariata.
- D4: la repository privata resta consigliata, ma non è più legata alla revisione esterna.
- D3, D5 e D6: invariate.

**PRD e verifica della settimana 8** [verificato: PRD «Metriche di successo»; P §11]
- La metrica «effetti usciti senza carta: 0» diventa «effetti fuori dal loro livello: 0».
- Si aggiungono tre misure [proposta]:
  - la quota di azioni partite senza intervento;
  - i minuti dalla fine della call al follow-up partito;
  - i «Ferma» e le correzioni per classe.

**Giorni di sviluppo** [stima]
- **Milestone 1:**
  - si risparmiano circa 3,5-5,5 gp di irrobustimento;
  - si aggiungono circa 4,5-6,5 gp per livelli, finestra, resoconto, annulla, destinazioni, ingresso esterno e stop;
  - la milestone resta circa della stessa misura, ±1-2 gp.
- **Sul piano intero:**
  - le semplificazioni liberano circa 6-9 gp;
  - le aggiunte ne chiedono circa 8-13;
  - il totale passa da 249-332 gp a circa 251-337 [stima su P §15].

---

## 8. Rischi principali e strade d'uscita

| Rischio | Mitigazione | Strada d'uscita |
|---|---|---|
| Una mail sbagliata arriva a un cliente in L2 o L3 | destinazioni ammesse, tetti, nota AI, finestra, discesa automatica, «correggi» | la classe torna a L1, cambiando solo la configurazione |
| Il parere chiede un sì esplicito sui follow-up | resta L1 per i follow-up; interno e pagina aziendale restano autonomi | si perde la parte più vicina alla trascrizione di riferimento |
| Volumi bassi: le soglie non si raggiungono | soglie regolabili; vale «prima il funnel» [verificato: P §11] | L2 manuale, deciso dal responsabile |
| Managed Agents: beta, dati negli USA, niente ZDR [verificato: R12 §1] | solo dati verdi; tetti per chiave | le stesse skill sul motore: il formato è comune a più di 70 piattaforme [verificato dal RAP4 §7: anthropic.com/news, 9/11]. Costa circa 4 GB e qualche gp [stima]. In alternativa Hermes Cloud |
| Grok Bot: modello invisibile, quota settimanale, incidenti, termini [verificato: R11 §3, §4.1, §7.3, §7.4] | resta facoltativo, solo dati verdi, mai un percorso critico | si lascia dopo la prova; le skill stanno in git [verificato: R20C §8] |
| Dati gialli finiscono negli abbonamenti, incollati da qualcuno | il ponte dà solo campi verdi; nessun connettore di posta o CRM negli abbonamenti; formazione | revoca del token |
| Bug del Cancello, più semplice e senza revisione esterna | idempotenza, esiti incerti a una persona, prove funzionali, revisione di Mattia | si riattiva una revisione esterna se servono dati dei clienti su larga scala |
| Il bot di Teams senza Azure dà errori, e mancano «Ferma» e carte | pagina del Cancello e avvisi ntfy [verificato: P §13] | Azure Bot F0 gratuito [verificato: R36 §5.6] |
| Linea internet o corrente ferme [verificato: P §13] | le squadre in abbonamento continuano a lavorare; linea di riserva prima di Andrea | riaccensione automatica: decide Michele [verificato: DOM n. 22] |
| Più fornitori da tenere d'occhio | in abbonamento solo due fornitori e solo dati verdi; meno servizi sul server, senza Postiz | tutto torna sul motore |

---

## 9. Funzioni: nessuna si toglie

**Voci che cambiano posto, livello o componente**

| Voce | In P-C | Cosa serve ancora | Costo |
|---|---|---|---|
| J1 | server e squadre in abbonamento sulla stessa bacheca | ponte MCP pubblico | 1-2 gp [stima]; 0 €, Pangolin è già nel board |
| J3, K11 | L1 per messaggio; oppure L1 per campagna e invii L3 entro i tetti, solo verso società britanniche o contatti con consenso | operazione «approva campagna»; parere | 2-4 gp [verificato: RAP2, collo 10] |
| J6, D2-D4, K6 | brief e slide per noi in L3; ricerca pubblica in abbonamento | lettura del calendario; orario 18 ore prima | circa 1 gp [stima]; ricerche a 10 $ ogni 1.000 [verificato: R18 §2.1] |
| J7, I4, K7 | marketing e studio in abbonamento; il Cancello pubblica | esecutore Metricool; nuova regola sulla sessione presidiata | 1-1,5 gp [stima]; 59,86 €/mese; Grok Bot 54-205 €/mese se lo scegliamo |
| A6 | skill sul server L2; in abbonamento L3 | esempi di prova per ogni skill | 1-2 gp [stima] |
| A7, e AU-09 | bacheca più riunione settimanale degli agenti | catene approvate con un loro tetto | circa 1 gp [stima] |
| B1-B5 | Cancello a livelli | livelli, finestra, resoconto, annulla | 3-5 gp, al posto di FIDO2 e «Sempre» [stima] |
| C1, K1 | debrief L3 dalla settimana 8 | orario sul banco di prova | 0,5-1 gp [stima] |
| E3 | anche le chiavi delle squadre in abbonamento | rendiconto per chiave [RAP4 §2.3] | 0,5 gp [stima] |
| G3, G4, K12 | coaching dalla fase 3 per chi lo sceglie | parere | circa 1,5 gp, spostati [stima] |
| G5, K10 | Andrea una fase prima, se ci sono lead e parere | seconda GPU, linea di riserva, operatore | 880-1.220 €; 77-200 € più 10-11 €/mese; 44-90 €/mese [verificato: P §12] |
| G6 | aperture nuove in L2, con ritorno automatico | test A/B | 0,5-1 gp oltre ai 2-3 già previsti [verificato: R31 §11; stima] |
| G9 | l'organigramma registra anche fornitore e posto di ogni agente | una colonna in più nel registro | 0,5 gp [stima] |
| K3 (e AU-22) | risposte L2 ai contatti noti | corsia separata per i mittenti sconosciuti | come nella v2.1 |
| K9 | newsletter L2 dalla fase 3 | relay SMTP | meno di 1 €/mese [verificato: P §12.1] |
| K16 | account Claude personale; per chi lo vuole, Grok Bot con le app del telefono [verificato: R11 §2.4, voce di terzi] | consenso | 15-18 € a persona [verificato: P §12.1] oppure 30 $ |
| L4 | bandi in abbonamento dalla fase 0-1 | — | dentro Cowork o Managed Agents |
| L8 | L2 per le risposte brevi sulla pagina aziendale; sui profili dei founder l'agente segnala soltanto | accesso alla pagina tramite Metricool | dentro Metricool |

**AU coperti solo in parte nel RAP1** [verificato: RAP1 §3]

P-C li copre così:
- **AU-09:** con la riunione settimanale degli agenti.
- **AU-19:** con il brief automatico per ogni incontro.
- **AU-22:** con le risposte L2 della posta.
- **AU-24:** con i consigli personali dell'Allenatore AI (L12) e del Mappatore (F1).
- **AU-25:** l'intervista la conduce l'agente Intervistatore (F2).
- **AU-31:** con la voce clonata su Qwen3-TTS sulla seconda GPU, con contratto separato e parere [verificato: P, appendice A, «Lacune dichiarate»].
- **Processo degli eventi e processo della formazione** [verificato: TR 18:50-18:58]: li coprono L10, E4, H1 e L12.
- **AU-02 e AU-30:** restano separati per scelta, come nella v2.1.

**Tutte le altre voci** restano con il componente e la fase dell'appendice A della v2.1 [verificato: P, appendice A]:

J2, J4, J5, J8, J9, A1-A5, C2-C6, D1, D5, E1, E2, E4, F1-F5, G1, G2, G7, G8, G10, H1-H7, I1-I3, K2, K4, K5, K8, K13-K15, L1-L3, L5-L7, L9-L12.

Hanno i livelli della scala del §3.1. Le uniche differenze sono due:
- FIDO2 tolta da L1 e L2;
- pagamenti mai automatici.

---
