# P-D · «Automazione prima»: n8n con passi AI e pochi agenti

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **P-D**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Proposta di architettura del 9/11/2026 per SerSan Agent OS, scritta per Alberto. Non ho modificato file e non ho lasciato processi accesi.

**Sigle delle fonti.** I file sono nella repo `C:\Users\alber\sersan-agent-os` e li ho letti il 9/11/2026.
- **P**: `PRESENTAZIONE-CEO.md` v2.1. **SPEC**: `docs/superpowers/specs/2026-11-09-nucleo-motore-cancello-design.md`. **PRD**: `.claude/prds/sersan-agent-os.prd.md`. **D03**, **D04**: `docs/03-architettura.md`, `docs/04-tech-stack.md`. **ADR-00NN**: `docs/adr/`. **DOM**: `DOMANDE-PER-MICHELE.md`.
- **R16, R26, R28, R29, R30, R31, R34-3, R35-vis, R35-cpto, R35-sic, R36, R37**: i rapporti con quel numero in `ricerca/`.
- **TR**: la trascrizione di riferimento, con il minuto. **T3**: le tre trascrizioni di terzi sul Desktop.
- **Rapp. 1-4**: i quattro rapporti del compito. Quando un fatto esterno viene da uno di loro scrivo «verificato dal Rapp. N».
- **n8n-docs**: tre pagine che ho letto io il 9/11/2026: `docs.n8n.io/hosting/scaling/execution-data/`, la pagina del nodo Wait e `docs.n8n.io/workflows/components/nodes/`.

**Etichette.** [proposta] indica una scelta di disegno mia. **gp** sono giorni-persona di sviluppo. I livelli sono L0 a mano, L1 carta, L2 finestra, L3 autonomo.

---

## 1. L'idea in 5 righe

1. I lavori ripetitivi diventano flussi n8n deterministici: dopo la call, debrief, brief, report, marketing e posta. Li avvia un evento o un orario. Il codice sceglie i passi e i destinatari; Claude, via LiteLLM, scrive i testi ed estrae i campi, senza strumenti.
2. Le sessioni con strumenti dell'Agent SDK restano per circa dieci figure che devono ragionare a più passi: brief, offerta, slide, agenda, Capo di gabinetto, mappa dei processi. Non agiscono: consegnano bozze e azioni proposte.
3. Il Cancello resta l'unico esecutore di ciò che esce e di ciò che si scrive. Decide per classe d'azione su quattro livelli invece di chiedere una carta per ogni azione; la finestra L2 è la novità.
4. L'autonomia sale classe per classe con dei contatori: 10 sì senza modifiche portano a L2, 20 invii non fermati portano a L3. Scende da sola al primo errore. Restano solo i limiti fissi, lo stop, i tetti, un registro semplice, la possibilità di annullare e la conformità minima.
5. Alla settimana 8, con circa gli stessi giorni della v2.1, sono già L3 il riassunto, il registro dei meeting, i to-do in Jira, il debrief e il suo evento in calendario; il follow-up può passare a L2. A regime P-D raggiunge il livello della trascrizione in tutto ciò che la trascrizione mostra, tranne offerte, contatti a freddo e pagamenti.

---

## 2. Componenti e dove girano

### 2.1 Lo schema

```
PERSONE (4)  Teams: carte, avvisi con "Ferma", canali, chat con gli agenti · Claude Team: finestra di lavoro
=========== SERVER DI MICHELE (DL380, Proxmox, VLAN del board) ===========
EVENTI E ORARI  n8n: webhook firmati, orari, delta di Graph, flussi con passi AI (tipo N)
RAGIONAMENTO    runner SDK sottile: ~10 profili S, sola lettura, uscita a schema
ESECUZIONE      CANCELLO a livelli (L0-L3, tetti, registro, annulla, stop) + PORTA (bot Teams)
                renderer dei documenti (slide e offerte dai template SerSan)
MEMORIA         PostgreSQL 16 (eventi, registro, meeting) · Qdrant + MCP RAG · BookStack
MODELLI         LiteLLM -> API Anthropic (budget per flusso, squadra, persona)
AI LOCALE       RTX 4000: pipeline del board · seconda GPU: trascrizione e voce
CALL E VOCE     Vexa (fase 3) · Asterisk + Pipecat per Andrea
LAB             banco di prova (n8n, PostgreSQL, Cancello, Porta) · Buzz · Paperclip
==========================================================================
CLOUD DEL BOARD M365 (Graph, Teams, Outlook) · Claude Team · API Anthropic · Jira · Instantly · Supabase
ESTERNI         operatore telefonico · relay SMTP · WhatsApp · Telegram · Slack
```

La regola è semplice: n8n legge e prepara, il runner ragiona, il Cancello scrive. n8n tiene solo credenziali di lettura [proposta, che applica ADR-0011, Conseguenze: «dove si può, usa credenziali in sola lettura»]. Come oggi, n8n non manda nulla a clienti o prospect [verificato: ADR-0011, Decisione].

### 2.2 Componenti

| Componente | Ruolo in P-D | Dove | RAM | GPU | Fonte |
|---|---|---|---|---|---|
| n8n, versione 2.x stabile fissata | orari; webhook firmati; lettura delle trascrizioni da Graph ogni 5-10 minuti; flussi; eventi fra flussi | VLAN 30 (board, fase F4); prima sul banco di prova | nel board; +2-3 GB per istanze o worker in più | no | n8n nel board e in F4 [verificato: R36 §4.1; D04, riga n8n]; delta ogni 5-10 minuti [verificato: R30 §3.4]; stabile 2.46.7, la 3.0 del 27/10 cambia l'API e le 3.x sono prerelease [verificato dal Rapp. 4 §5]; RAM in più [non verificato: stima mia] |
| Passi AI (tipo N) | riassumere, classificare, estrarre, scrivere bozze: una chiamata via LiteLLM, senza strumenti, con uscita a schema | dentro i flussi n8n | — | no | [verificato: R36 §5.2; SPEC §4.4] |
| Runner SDK sottile | circa 10 profili S. Usa gli MCP in sola lettura e Firecrawl. Non ha `propose_action` e non riprende dopo una carta. Il Capo di gabinetto riprende la sessione per thread | container in VLAN 30; se serve la VLAN 32 lo decide Michele | 6-8 GB con al massimo 6 sessioni | no | 1 GiB per sessione [verificato: R26, In breve p.3]; tetto di 6 sessioni [verificato: R36 §1.5]; la VLAN la decide Michele [verificato: R26 §3]; totale [non verificato: stima] |
| Cancello a livelli | associa le classi ai livelli; carte L1; finestre L2; esecuzione L3 dentro i tetti; limiti fissi; outbox; registro; annulla; stop; lista di soppressione | container suo, separato da n8n e dal runner | 2-3 GB con la Porta | no | [proposta]; nella v2 erano 3-4 GB [verificato: R36 §4.1] |
| Porta (bot Teams) | carte con l'identità di chi preme; avvisi L2 con «Ferma»; messaggi firmati con il nome dell'agente; `/stop`; chat 1:1 | con il Cancello | 0,5-1 GB | no | [verificato: R36 §4.1]. `Action.Execute` è verificato; l'arrivo dell'`aadObjectId` è da confermare [verificato: R28 §2.3] |
| Renderer dei documenti | slide e offerte con i template SerSan, a partire da contenuti a schema | VLAN 30 | 0,5-1 GB | no | [proposta; non verificato: stima] |
| Server MCP (`mcp-01`) | memoria, BookStack, Jira, posta in lettura, Firecrawl, SersanOutreach | VLAN 30 | 3-4 GB | no | [verificato: R36 §4.1-4.2] |
| PostgreSQL 16 | eventi, registro delle azioni, Cancello, meeting, n8n | VLAN 40 | +1-5 GB di crescita | no | [verificato: R36 §4.1] |
| LiteLLM | budget per flusso, squadra e persona; avviso all'80%, stop al 100% | VLAN 30 (board, F4) | nel board | no | [verificato: ADR-0004] |
| Qdrant con MCP RAG, BookStack, Firecrawl, pipeline AI | memoria e web | board | nel board; MariaDB 1 GB | RTX 4000 | [verificato: R36 §4.1] |
| Trascrizione in casa | call dei clienti e riunioni dal vivo | VLAN 80 | +6-8 GB | 2-4,5 GB di giorno | [verificato: R36 §4.1] |
| Vexa | bot nelle call dei clienti | `meet-01` | 12 GB; circa 4 con Vexa Lite | no | [verificato: R36 §4.1-4.2] |
| Asterisk e Pipecat (Andrea) | voce | VLAN 25 e 30 | 1 GB + 6-8 GB su CPU; 4 GB con la seconda GPU | seconda GPU | [verificato: R36 §4.1; R31 §8.2] |
| Postiz, listmonk | post e newsletter, mai pubblici | VLAN 30 | 2 + 0,5 GB | no | [verificato: R36 §4.1] |
| DocuSeal, fatturazione | firma e fatture | VLAN 30 | 1 + 1-2 GB | no | [verificato: R36 §4.1] |
| Banco di prova | n8n, PostgreSQL, Cancello e Porta del pilota | VLAN 90 LAB | 8 GB nel pilota, poi 4 | no | RAM [verificato: R36 §4.2]; n8n sul banco [proposta] |
| Cloud del board | M365 (Graph, Teams, Outlook), Claude Team, API Anthropic, Jira, Instantly, Supabase | cloud | — | — | [verificato: P §5.1] |
| Esterni | operatore telefonico, relay SMTP, WhatsApp, Telegram, Slack | — | — | — | [verificato: P §5.1, §14] |

### 2.3 La RAM, fase per fase

| GB nuovi | Fase 1 | Fase 2 | Fasi 3-4 | Fasi 5-6 |
|---|---|---|---|---|
| Banco di prova | 8 | 4 | 4 | 4 |
| Runner SDK sottile | 0 | 7 | 7 | 8 |
| n8n, istanze o worker in più | 0 | 2 | 3 | 3 |
| Cancello, Porta, renderer | 0 | 3,5 | 3,5 | 4 |
| Server MCP | 0 | 3 | 4 | 4 |
| MariaDB | 0 | 1 | 1 | 1 |
| Crescita di PostgreSQL, Qdrant e Loki | 0 | 1 | 3 | 5 |
| Postiz e listmonk | 0 | 2 | 2,5 | 2,5 |
| Trascrizione | 0 | 0 | 6 | 8 |
| Vexa | 0 | 0 | 12 | 12 |
| Worker in più di SersanOutreach | 0 | 0 | 1 | 2 |
| Andrea (CPU; con la seconda GPU) | 0 | 0 | 0, oppure 8 se anticipato | 8; 4 |
| DocuSeal e fatturazione | 0 | 0 | 0 | 2,5 |
| **Totale P-D** | **8** | **23,5** | **47 (55 con Andrea)** | **60-64** |
| Totale v2.1 | 8 | 25 | 53,5 | 70-74 |
| **Libera con 192 GB (53 liberi)** | **circa 45** | **circa 29** | **circa 6 (-2 con Andrea)** | **da -7 a -11** |

Le voci uguali alla v2.1 sono verificate in R36 §4.1-4.2. Runner, n8n e renderer sono stime mie [non verificato].

**Come si legge.**
- A regime P-D usa circa 10 GB meno della v2.1, soprattutto grazie al runner: 6-8 GB invece di 12-20.
- Con tutto acceso la RAM in più resta comunque probabile.
- La regola d'acquisto non cambia: si comprano altri 192 GB quando il margine misurato scende sotto i 5 GB [verificato: P §6.3; R36 §4.2].
- Le leve per rimandare l'acquisto restano tre:
  - Vexa Lite, che toglie circa 8 GB;
  - Experimental accese solo quando servono, 24 GB [verificato: R36 §4.2];
  - il secondo nodo che Michele prevede a dicembre, fino a 1.500 € [verificato: R37 §2]. Dove mettere i servizi lo decide lui.

### 2.4 GPU

- **P-D non aggiunge lavoro alla GPU.** I passi AI vanno a Claude via API. L'oscuramento locale gira sulla CPU, come nella v2.1 [verificato: R36 §7.3].
- **La RTX 4000.** Di giorno è quasi piena con la pipeline del board [verificato: R36 §4.3]. Michele la presta a Experimental-1 «al massimo qualche ora a settimana» [verificato: R37 §1].
- **Seconda GPU.** Vale la logica della v2.1: conviene dalla fase 3 e serve prima di portare Andrea sulla GPU [verificato: P §6.4]. Andrea può partire sulla CPU [verificato: R31, In breve].

### 2.5 Abbonamenti e alternative

**Il nucleo di P-D non richiede abbonamenti nuovi.** n8n in casa costa 0 € per l'uso interno [verificato: ADR-0011; R36 §9.3]. Se un pezzo non regge, Alberto ammette gli abbonamenti. Quelli già prezzati:
- voce in cloud per Andrea, circa 88 €/mese [verificato: R36 §12];
- Metricool, 59,86 €/mese, finché Postiz non è pronto [verificato: R36 §12];
- Managed Agents per un pilota su dati verdi: 0,08 $ per ora di sessione più i token. Dati negli USA, senza conservazione zero (ZDR) [verificato dal Rapp. 4 §2.1];
- un mese di prova di Grok Bot su dati pubblici, circa 54 € [verificato: P §14, decisione 23].

**Dove entrano le alternative, valutate alla pari.**
- **Hermes v0.23.** Ne copio le idee nel freno e negli eventi: `max_hops` di serie a 4, stanze che smistano da sole, cron nelle stanze [verificato dal Rapp. 4 §3.3]. Resta un'uscita per il runner: una prova costa 6-8 gp [verificato: P §15]. Le quattro condizioni per usarlo come orchestratore non sono ancora soddisfatte [verificato dal Rapp. 4 §3.4].
- **Grok Bot e Dots.** Hanno l'autonomia «pronta» più ampia: routine, webhook, chat di gruppo, passaggi e registro [T3, grokbot transcript, fonte di terzi]. Però stanno fuori dal server, con dati negli USA [verificato dal Rapp. 4 §4, §8.1]. Per Grok Bot conta anche il limite d'uso settimanale che ferma i bot [T3, «Grokbot vs Hermes», fonte di terzi]. Restano piloti facoltativi su dati pubblici.
- **Paperclip.** Resta la prova nella fase 6 come piano di controllo sopra il registro [verificato: P §4.12; Rapp. 4 §7].
- **Buzz.** Resta nel laboratorio [verificato: P §4.11; Rapp. 4 §7].
- **Claude-native.** P-D è un ibrido Claude-native: l'SDK per le sessioni S, Claude via API nei passi N.

---

## 3. Il modello di autonomia

### 3.1 Perché con P-D l'autonomia arriva prima

- **I limiti di oggi non stanno nel motore.** Nella v2.1 stanno quasi tutti nel Cancello, nelle regole di casa e nel calendario [verificato: Rapp. 2, In breve].
- **Il modello non sceglie né chi né cosa.** In un flusso deterministico il modello scrive il testo, ma destinatari e azioni li prende il codice dal calendario e dal CRM. Il giudice di sicurezza chiama la chiamata a schema senza strumenti «il disegno più robusto» contro le iniezioni [verificato: R35-sic §3.2]. Un'azione prevedibile può partire da sola con meno controlli [proposta]. I profili S che leggono il web o la posta consegnano solo documenti; le azioni che propongono passano da n8n, che prende il destinatario dai dati [proposta].
- **L2 non c'è in nessuna alternativa studiata** [verificato: Rapp. 3 §4]. P-D lo mette nel Cancello.
- **La trascrizione consiglia catene, non agenti.** Le automazioni che indica sono il deck da un modello unico, il follow-up della call, che «potrebbe essere totalmente automatizzato», e il brief di intake [verificato: TR min. 13:11-13:20].
- **Eventi e orari ci sono già nel pilota.** n8n li dà sul banco di prova. Nella milestone 1 della v2.1 i lavori partono da un comando dato a mano [verificato: SPEC §3; Rapp. 2, collo n. 7].

### 3.2 Come funziona la scala

**La regola parte dalla classe d'azione.** Una classe è un tipo d'azione per un gruppo di destinatari. Le regole «Sempre» della v2.1 erano strette su agente, azione e destinazione [proposta; v2.1: P §5.4].

**Destinatario noto.** È un indirizzo, o un dominio, con cui c'è stata una call registrata o uno scambio di mail nei due sensi negli ultimi 90 giorni, e che non è nella lista di soppressione [proposta].

**Il tetto per classe.** I tetti si fissano una volta, dopo il parere legale. Lo fanno i CEO, come oggi per i messaggi che possono diventare «Sempre» [verificato: P App. A, B5].

| Classe | Esempi | Tetto | Perché |
|---|---|---|---|
| Lettura e scrittura interna | to-do, CRM, calendario proprio, canali interni, registro | L3 | interna e annullabile |
| Messaggio a un destinatario noto | follow-up, recap, invito alla seconda call, risposta standard, promemoria, sollecito | L3 (i solleciti L2) | è il cuore della trascrizione [verificato: TR min. 4:42-5:07] |
| Primo messaggio dopo una prima call | primo follow-up a un prospect appena incontrato | L2 | ha appena parlato con noi; il parere decide |
| Primo contatto a freddo | email, LinkedIn | L1 | il Garante chiede il consenso [verificato: R16 §3]; su LinkedIn si approva ogni messaggio [verificato: P §7.4] |
| Pubblicazione | pagina aziendale; profili dei founder | L2; L1 | la voce dei founder resta umana per scelta [verificato: P §9.3] |
| Impegni | offerte, contratti, prezzi, fatture | L1 | impegno economico, scelta di casa [verificato: P §9.3] |
| Telefonata di Andrea | richiamata a chi l'ha chiesta nel modulo | L3 | nessuna finestra entra in 90 secondi [verificato dal Rapp. 4 §8.2] |
| Configurazione | istruzioni e skill dei flussi; strumenti, permessi, classi | L2 con valutazione; L1 | |
| Pagamenti | — | L0 | limite fisso |
| Cancellazioni, credenziali | — | vietate | limite fisso |

**Tetti di quantità e orari** [proposta]:
- ogni classe ha un massimo di azioni al giorno, ogni destinatario un massimo di messaggi al giorno, ogni catena un massimo di passaggi e di spesa;
- un'azione oltre il tetto scende a L1 e diventa una carta, quindi non si perde;
- dalle 20 alle 8 e nel fine settimana non parte nulla verso l'esterno. Fa eccezione Andrea: di notte richiama solo chi ha scelto «richiamatemi adesso» [non verificato: proposta di R31 §9].

**Ogni flusso nuovo parte «in ombra».** Per una settimana, o per 10 casi, prepara ciò che farebbe senza farlo. La prova si chiude al primo dei due traguardi, invece che dopo 1-2 settimane fisse [verificato: P §9.2 per la regola; il conteggio è una proposta del Rapp. 2, collo n. 15].

### 3.3 Le regole per salire e per scendere

| Passaggio | Quando | Chi decide |
|---|---|---|
| Ombra → L1 | dopo una settimana o 10 casi senza errori gravi | il responsabile della classe |
| L1 → L2 | 10 carte di fila approvate senza modifiche sostanziali in 30 giorni, e nessun reclamo. È sostanziale cambiare destinatario, oggetto o più del 10% del testo | il responsabile, entro il tetto della classe |
| L2 → L3 | 20 azioni di fila partite senza «Ferma» né rettifiche | il responsabile, solo per le classi ammesse a L3 |
| Giù di un livello, da solo | un «Ferma» con motivo «errore»; una rettifica dopo l'invio; un destinatario fuori dal gruppo | automatico |
| Di nuovo a L1, da solo | un reclamo o un'opposizione; un cambio di modello o di istruzioni non valutato; due tetti di spesa superati nel mese | automatico |
| Spento (L0), da solo | stop di emergenza; parere o norma che cambia; tre retrocessioni nello stesso mese | automatico; si riaccende a mano |

Le classi si rivedono ogni mese nel punto del venerdì. Non c'è la scadenza automatica a 30 giorni delle regole «Sempre» [proposta; v2.1: P §5.4, §10]. Le soglie sono una proposta mia [non verificato].

### 3.4 I nove flussi

**1. Dopo una call** (Teams dalla fase 1, call dei clienti con Vexa dalla fase 3)

| Azione | Partenza | A regime | Come si sale | Regole specifiche |
|---|---|---|---|---|
| Riassunto nel canale interno e registro dei meeting | L3, settimana 8 | L3 | — | se è scarso si corregge il prompt, non il livello |
| To-do al team in Jira | L3, settimana 8 | L3 | — | tre to-do chiusi come «sbagliato» in una settimana riportano il flusso a L1 |
| Meeting e opportunità nel CRM | L0 alla settimana 8 (i campi sono pronti nel riassunto); L3 quando c'è il connettore di SersanOutreach, nella fase 2 | L3 | arriva con il connettore | — |
| Mail di follow-up ai partecipanti | L1, settimana 8 | L3 per i clienti noti; L2 per il primo follow-up dopo una prima call | scala del §3.3, con finestra di 30 minuti in orario d'ufficio | solo ai partecipanti della call e al loro dominio; serve il parere; riga che dichiara l'AI a L2 e L3 |
| Punti nel canale del cliente | L1, fase 3 (canali condivisi, Slack, WhatsApp) | L3 per i clienti con un progetto attivo | come il follow-up | i canali condivisi fra organizzazioni vanno provati [verificato: P App. A, B1] |

**2. Debrief del mattino**

| Azione | Partenza | A regime | Note |
|---|---|---|---|
| Debrief alle 7:00 in Teams per ciascuno | L3, settimana 8 | L3 | si allarga con le fonti: calendario, registro dei meeting e Jira nella fase 1; CRM e pipeline nella 2; memoria nella 3 |
| Evento del debrief come primo appuntamento in calendario | L3, settimana 8 | L3 | — |
| «Cosa è partito da solo ieri», con le azioni fermate o corrette | L3, settimana 8 | L3 | è il controllo «dopo» |

**3. Brief prima di un incontro, con le slide**

| Azione | Partenza | A regime | Come si sale e regole |
|---|---|---|---|
| Brief la sera prima, per ogni incontro esterno in agenda | L3, fase 2 (web, CRM, calendario, registro); con tutta la memoria dalla fase 3 | L3 | è profilazione: serve la DPIA; LinkedIn solo per una via consentita [verificato: P §9.1 r.9; App. A, D2] |
| Slide per noi | L3, fase 2 | L3 | — |
| Deck al cliente | L1, fasi 2-3 | L2 per i clienti noti | 10 sì senza modifiche; numeri solo da dati verificati |

**4. Offerta dopo l'incontro**

| Azione | Partenza | A regime | Regole |
|---|---|---|---|
| Bozza dell'offerta entro un'ora, interna | L3, fase 2 | L3 | — |
| Invio dell'offerta | L1 (Michele o Alessandro, senza chiave FIDO2) | L1 | non sale: è un impegno di prezzo [verificato: P §9.3]. È una regola di casa che i CEO possono rivedere. Nella trascrizione il livello non è detto [verificato: Rapp. 1, AU-21] |

**5. Marketing**

| Azione | Partenza | A regime | Come si sale e regole |
|---|---|---|---|
| Ricerca concorrenza, temi, bozze, numeri del lunedì | L3, fase 2 | L3 | — |
| Post sulla pagina aziendale | L0 fino alla fase 2; poi L1 con Postiz, se Alberto cambia la regola della sessione presidiata [verificato: P §8.2] | L2 per i formati ricorrenti | 10 sì → L2 |
| Post sui profili dei founder | L1 | L1 | la voce dei founder resta umana [verificato: P §9.3] |
| Newsletter | L1, fase 4 | L1 | una al mese: salire non conviene. Solo iscritti con consenso; serve il relay SMTP |
| Risposte ai commenti della pagina | L1, fase 4 | L2 per ringraziamenti e domande standard | sui profili dei founder l'agente segnala soltanto (L0) |

**6. Andrea, la richiamata entro 90 secondi**

| Azione | Partenza | A regime | Regole |
|---|---|---|---|
| Richiamata, appuntamento con una persona, conferma via mail con un modello fisso, chiamate in entrata | L3 dal primo giorno dal vivo, dopo una settimana con lead di prova | L3 | Chiama solo chi ha chiesto la richiamata nel modulo. La prima frase, fissa, dichiara l'AI. Rispetta gli orari, fa al massimo 2 tentativi e ha un tetto di chiamate al giorno. Si spegne da sola dopo un reclamo [verificato per consenso e frase AI: R31 §9; il resto è una proposta] |

**7. Coaching delle vendite**

| Azione | Partenza | A regime | Regole |
|---|---|---|---|
| Report dopo ogni call di vendita e piano del mese, a chi ha fatto la call | L3, fase 3 | L3 | senza stimare emozioni, che è vietato [verificato: R16, sintesi 3] |
| Al responsabile | L3, solo dati aggregati | il report di ogni call solo se il parere lo consente | valutare il lavoro con profilazione è alto rischio dal 2/12/2027 [verificato: R16 §4]; in quattro un dato aggregato resta riconoscibile [verificato: P §4.8] |

**8. Agenti che si parlano e chiudono i to-do superati**

| Azione | Partenza | A regime | Come si sale e regole |
|---|---|---|---|
| Passaggi fra flussi («ho trovato tre nuove call»), con lo specchio nel canale «Agenti» | L3: base nella fase 1, completo nella 2 | L3 | freno a 4 passaggi per catena e tetto di spesa per catena; oltre, «serve un umano» in L1 |
| Inviti per le call trovate | L1, fase 2 | L3 per la seconda call con contatti noti; L2 per i nuovi che hanno chiesto la call | scala del §3.3; avviso di registrazione nell'invito |
| Stand-up degli agenti, ogni giorno | L3, fase 2 | L3 | copre i «momenti di scambio» della trascrizione [verificato: TR min. 4:20-4:30] |
| Chiusura dei to-do fra agenti | L3 | L3 | — |
| Chiusura dei to-do delle persone | L1: un tocco su «lo chiudo?» | L2: si chiude dopo 24 ore se il titolare non dice no e il registro ha una prova | 10 sì di fila del titolare; se il titolare riapre, torna a L1 [regola di oggi: verificato in R29 §4.2] |

**9. Apprendimento dai rifiuti e dagli esiti**

| Azione | Partenza | A regime | Regole |
|---|---|---|---|
| Imparare dalle correzioni alle bozze, che diventano esempi | L3, fasi 1-2 | L3 | interno |
| Nuove aperture di Andrea | L1: un founder approva | L2: partono dopo 48 ore senza «Ferma», con un controllo automatico della frase AI; il test A/B fra aperture approvate è L3 | servono volumi; con zero lead non c'è niente da imparare |
| Modifiche alle istruzioni e alle skill dei flussi | L1 | L2, con valutazione automatica su esempi fissi e ritorno alla versione precedente | i cambi a strumenti, permessi o classi restano L1 |

### 3.5 Confronto con la trascrizione di riferimento

**Dove P-D arriva allo stesso livello, L3:**
- il dopo-call interno e il follow-up ai clienti noti [verificato: TR min. 4:42-5:07];
- i passaggi fra agenti e gli appuntamenti a contatti noti [verificato: TR min. 4:03-4:18];
- la richiamata entro 90 secondi, 24 ore su 24 [verificato: TR min. 14:53-14:59, 15:58-16:02];
- il coaching a chi ha fatto la call [verificato: TR min. 14:36-14:43].

**Dove P-D fa più della trascrizione.** Nella trascrizione il debrief lo fa la persona [verificato: TR min. 5:14-5:23] e il brief parte quando qualcuno inserisce l'email [verificato: TR min. 7:51-7:55]. In P-D entrambi partono da soli, L3. Così si chiudono due lacune che il Rapp. 1 ha trovato: AU-19 e AU-09.

**Dove P-D resta sotto, e perché:**
- il primo follow-up dopo una prima call è L2, per prudenza e in attesa del parere;
- le aperture di Andrea sono L2, mentre nella trascrizione Andrea le cambia da solo [verificato: TR min. 15:34-15:44];
- il report di ogni call al responsabile dipende dal parere;
- offerte, contatti a freddo e profili dei founder restano L1. Nella trascrizione le offerte non hanno un livello [verificato: Rapp. 1, AU-21] e il freddo non c'è;
- pagamenti, cancellazioni e credenziali sono limiti fissi.

**Il controllo sta prima e dopo l'azione, come nella trascrizione** [verificato: Rapp. 1 §4, principio 17]. Prima ci sono classi, tetti e destinatari presi dai dati. Dopo ci sono il registro, il riepilogo nel debrief, l'annullo e la retrocessione.

---

## 4. Protezioni essenziali

### 4.1 Le sei protezioni

**1. Limiti fissi, scritti nel codice del Cancello e non in configurazione.**
- Cancellazioni e credenziali sono sempre negate, anche se la configurazione dice altro [verificato: D03 §4.1; SPEC §4.6].
- I pagamenti non salgono mai sopra L0: il sistema prepara, la persona paga dalla banca [proposta, coerente con P §9.3 e App. A, K15].
- L'annullo di una scrittura interna non cancella: rimette il valore di prima o segna «annullato» [proposta].

**2. Stop di emergenza.**
- Lo preme chiunque dei quattro con `/stop` in Teams; lo tolgono Alessandro o Michele [verificato: SPEC §9, D2].
- Il Cancello rifiuta tutto e annulla carte e finestre aperte. I flussi n8n leggono lo stato all'avvio e si fermano. Andrea passa le chiamate alle persone [proposta].
- Dalla fase 2 lo stop porta anche a zero i budget di LiteLLM, fa scattare il kill switch di SersanOutreach e mette in pausa Instantly [verificato: D03 §4.3].
- Nulla riparte da solo [verificato: SPEC §4.10].

**3. Tetti.**
- LiteLLM per flusso, squadra e persona, con avviso all'80% e stop al 100% [verificato: ADR-0004].
- Sul banco di prova si usa una chiave per flusso, con il limite di spesa della Console. I costi per chiave si leggono dall'API Usage and Cost, in beta dal 29/10 [verificato dal Rapp. 4 §2.3]. Che la Console permetta un limite per area di lavoro è ancora un'ipotesi da confermare [verificato: SPEC §12.2].
- Ci sono poi i tetti di quantità e il freno alle catene del §3.2 [proposta].

**4. Registro semplice.**
- Una tabella `azioni` in PostgreSQL. L'utente del Cancello può solo inserire e leggere.
- Per ogni azione registra chi l'ha proposta, cosa, a quale livello, chi ha deciso, l'esito e il costo. Per le scritture interne tiene anche il valore di prima e quello di dopo.
- A fianco ci sono lo storico delle esecuzioni di n8n e il riepilogo nel debrief [proposta].
- Conservazione: i log degli agenti 90 giorni; i testi inviati ai clienti come il CRM, 24 mesi [verificato: P §9.1 r.8].

**5. Correggere un errore.**
- La finestra L2 con «Ferma» e «Manda ora».
- «Annulla» per le scritture interne.
- «Rettifica» per un messaggio già partito: prepara la correzione come carta L1 e fa scendere la classe.
- Un invio dall'esito incerto non si ripete da solo [verificato: SPEC §4.8].
- Ogni passo di n8n ha una chiave d'idempotenza, così un ritentativo non produce un secondo effetto [proposta]. n8n ha «Retry On Fail» e «On Error» sui nodi [verificato: n8n-docs, impostazioni dei nodi].

**6. Conformità minima.**
- **Dichiarare l'AI.** Andrea lo fa dalla prima frase. Le mail L2 e L3 portano una riga del tipo «preparata con un assistente AI per conto di …». Le mail L1 escono a nome di chi approva [verificato: P §9.1 r.1; R16, sintesi 1 per l'art. 50 dal 2/8/2026; il testo della riga è una proposta].
- **Avviso di registrazione** nell'invito e a voce [verificato: P §9.1 r.2].
- **Una sola lista di soppressione** per tutti i canali, che il Cancello legge prima di ogni azione esterna [verificato: P §9.1 r.5].
- **Email B2B verso l'Italia.** Il Garante applica l'art. 130 anche ai contatti aziendali [verificato: R16 §3]. Il freddo resta in SersanOutreach, con approvazione di ogni messaggio. Che il follow-up a chi ha partecipato a una call non sia marketing a freddo [non verificato: proposta di R16 §3 p.2, da confermare nel parere].
- **Andrea.** Consenso nel modulo (art. 130 c.1) e controllo del Registro delle opposizioni ogni mese [verificato: R16, sintesi 1; R31 §9].
- **Registro dei trattamenti e DPIA** per registrazioni, analisi delle vendite, voce e brief [verificato: P §9.1 r.9].
- **Coaching** solo alla persona; al responsabile dati aggregati; niente emozioni [verificato: P §9.1 r.3].
- **Scadenze di conservazione** applicate da un lavoro fisso, mai da un agente [verificato: Rapp. 2, voce A5].
- **Dati rossi verso l'API** come deciderà il parere; fino ad allora si oscurano in locale [verificato: P §5.6].
- **Formazione AI documentata** (art. 4) [verificato: P §10].

### 4.2 Cosa dipende dal parere legale

Sono i punti già messi nel parere unico [verificato: P §9.4; R16 §7]:
- **Email B2B verso l'Italia.** Decide quali classi di mail possono salire a L2 o L3 e verso chi.
- **Registrazione delle call** e art. 4 dello Statuto dei lavoratori, se ci sono dipendenti. Decide su C2 e F1.
- **Andrea:** testo del consenso, art. 130, voce clonata con contratto separato.
- **Confine fra coaching e valutazione dei lavoratori.** Decide il report di ogni call al responsabile.
- **Trasferimenti verso gli USA.** Decidono i dati rossi verso l'API e verso Claude Team.
- **Registrazioni con clienti del Regno Unito.**
- **Valore della firma elettronica fatta in casa.**
- **Copia dei backup a casa di Michele.**
- **Nuovo per P-D:** il testo della riga AI nelle mail che partono da sole, e se basta.

### 4.3 Cosa non portiamo dalla v2.1

**Nel Cancello:**
- la chiave FIDO2 sulle carte. Le chiavi però restano, perché servono all'accesso NetBird del board [verificato: R30 §1];
- i codici monouso per ogni consegna, l'impronta calcolata dalla Porta e le sette condizioni della decisione;
- le firme HMAC con numero monouso fra servizi interni;
- il registro a catena con MAC e ancora esterna;
- le epoche dello stop;
- l'elenco chiuso nel codice delle scritture interne;
- le regole «Sempre» con 20 sì e scadenza a 30 giorni.

**Nelle prove:** le tre barriere sugli strumenti provate una per una e i dieci scenari a ogni aggiornamento dell'SDK, che diventano tre prove di base.

**Nelle condizioni:** la revisione esterna di sicurezza non è più una condizione; diventa facoltativa.

**Due regole di casa** che possono cambiare, se i CEO e Alberto lo decidono:
- la regola 10, «una persona nel giro per ogni azione esterna irreversibile» [verificato: P §9.1], diventa «una persona per ogni impegno e ogni primo contatto»;
- nei canali condivisi con i clienti oggi «scrive solo il Cancello, dopo una carta» [verificato: P §4.11]. Con P-D il Cancello resta l'unico che scrive, ma al livello della classe.

**Le regole del board restano di Michele:** VLAN, Cyber Essentials, «dati verdi e gialli finché F3 non è validata» [verificato: P §11].

### 4.4 Una trappola concreta di n8n: i dati delle esecuzioni

- **n8n salva i dati delle esecuzioni.** Le variabili `EXECUTIONS_DATA_SAVE_ON_SUCCESS`, `..._ON_ERROR`, `..._ON_PROGRESS` e `..._MANUAL_EXECUTIONS` decidono cosa tiene. La stessa scelta si può fare flusso per flusso. La pulizia è accesa di serie e cancella dopo 336 ore, cioè 14 giorni [verificato: n8n-docs, execution-data].
- **Il nodo Wait scrive nel database.** Se l'attesa supera i 65 secondi, salva i dati dell'esecuzione. Ha l'opzione «Limit Wait Time», che fa riprendere il flusso da solo alla scadenza [verificato: n8n-docs, nodo Wait].

Ne vengono tre regole [proposta]:
- i flussi che leggono testo rosso non salvano le esecuzioni, né riuscite né fallite;
- il testo rosso non attraversa mai un Wait: prima si riassume, poi si aspetta;
- la verifica della settimana 8 controlla il database di n8n.

Senza queste regole verrebbe meno «nessun dato rosso sul banco di prova» [verificato: PRD, Metriche].

---

## 5. Fasi

### 5.1 Alla settimana 8, fine della fase 1

Siamo sul banco di prova e si salvano solo dati verdi e gialli [verificato: P §11].

| Livello | Cosa |
|---|---|
| L3 | riassunto nel canale interno; registro dei meeting; to-do in Jira; debrief alle 7:00 con l'evento in calendario; riepilogo di ciò che è partito da solo; eventi di base fra i flussi nel canale «Agenti»; raccolta delle correzioni alle bozze |
| L2 | follow-up ai partecipanti della call, solo con 10 sì senza modifiche e il via del parere della settimana 3; altrimenti resta L1 |
| L1 | tutto il resto che esce |
| L0 | CRM (i campi sono pronti) finché non c'è il connettore; post (regola della sessione presidiata) |

**Confronto con la v2.1 alla settimana 8.** Lì sono L3 solo il riassunto interno e il debrief, che ha poco contesto. Il follow-up è L1 e nella fase 1 Jira, CRM e calendario non si scrivono [verificato: P §1, §11; Rapp. 2, voci C1 e B4].

### 5.2 Alla settimana 21, fine della fase 2

Siamo sul server, con n8n e LiteLLM.

| Livello | Cosa |
|---|---|
| L3 | CRM; brief la sera prima; bozza d'offerta entro un'ora; ricerca concorrenza, bozze e numeri del lunedì; smistamento della posta; stand-up degli agenti; to-do fra agenti; follow-up ai clienti con un progetto attivo, se la classe ha fatto i suoi 20 invii |
| L2 | primo follow-up dopo una call; recap e deck ai clienti noti; inviti alla seconda call; risposte standard a contatti noti; post della pagina aziendale nei formati ricorrenti; chiusura dei to-do delle persone con una prova |
| L1 | offerte, primi contatti, post dei founder, risposte non standard |

**Confronto con la v2.1 alla settimana 21.** Lì l'interno è L3, ma tutto ciò che esce è L1 e le regole «Sempre» sono quasi irraggiungibili [verificato: Rapp. 2, colli n. 1 e 2].

### 5.3 A regime, fasi 5-6

| Livello | Cosa |
|---|---|
| L3 | tutto l'interno; follow-up, recap, promemoria e inviti ai contatti noti; Andrea; coaching alla persona; test A/B; apprendimento dalle correzioni |
| L2 | primo follow-up dopo una prima call; pubblicazioni della pagina aziendale; nuove aperture di Andrea; istruzioni e skill che passano la valutazione; solleciti; risposte standard nella stanza del cliente |
| L1 | offerte, contratti, fatture, prezzi; contatti a freddo; post dei founder; newsletter; strumenti e permessi |
| L0 | pagamenti; commenti sui profili dei founder; ciò che il parere esclude |
| Vietate | cancellazioni, credenziali |

### 5.4 Cosa cambia rispetto alle fasi della v2.1

| Pezzo | v2.1 [verificato: P §11; R36 §7.3] | P-D |
|---|---|---|
| Eventi e orari | comando a mano nella milestone 1; n8n dalla fase 2 | n8n sul banco di prova dalla fase 1 |
| Motore SDK | prima parte nella fase 0, banco nella 1, server nella 2 | runner sottile dalla fase 2, solo per circa 10 profili S |
| Cancello | v1 nella fase 1; FIDO2 e «Sempre» nella 2; v2 nella 3 | livelli con finestra dalla fase 1; promozioni per classe dalla fase 2; niente FIDO2 |
| Jira e calendario come scritture | fase 2 | fase 1 |
| Bacheca e canale «Agenti» | fase 2 | base nella fase 1, completa nella 2 con lo stand-up degli agenti |
| Brief la sera prima, offerta entro un'ora | fase 3 | fase 2 |
| Postiz | fase 4 | fase 2 |
| Skill che imparano | fase 4, con pull request | dalle correzioni nella fase 2; con valutazioni e finestra nella 4 |
| Coaching | fase 5 | fase 3 |
| Andrea | fase 5 | costruito nella fase 3 se alla settimana 21 vale «prima il funnel», cioè lead vere e parere; altrimenti fase 5 [regola: verificato, P §11] |
| Revisione esterna | entro la settimana 21, condizione per i dati dei clienti | facoltativa. I dati dei clienti entrano in memoria con F3 validata e un ripristino del backup 3-2-1 riuscito [proposta] |

### 5.5 Le verifiche

**Settimana 8** [proposta, sulla base di P §11 e del PRD]:
- dopo ogni call Teams del periodo, riassunto e to-do entro 15 minuti da quando la trascrizione è disponibile;
- tutti i follow-up partiti entro 24 ore, misurando i minuti fra fine call e invio e la quota di quelli partiti senza nessun intervento;
- nessuna azione fuori dalla sua classe o dal suo tetto, nemmeno nelle prove: in particolare nessuna mail fuori dal dominio dei partecipanti e nessuna azione vietata;
- lo stop dal telefono ferma finestre e flussi entro un minuto, e nulla riparte da solo;
- il registro è completo, e un errore viene annullato o rettificato almeno una volta in prova;
- la spesa resta nel tetto;
- nessun dato rosso nei database, compreso quello di n8n;
- il debrief arriva ogni giorno lavorativo;
- i criteri commerciali restano quelli della v2.1 [verificato: P §11].

**Settimana 21.**
- Gli stessi criteri, sul server, con i budget di LiteLLM.
- Almeno tre classi a L2 o L3 senza retrocessioni nelle ultime quattro settimane.
- Backup 3-2-1 con un ripristino riuscito e RAM misurata, come nella v2.1 [verificato: P §11].
- La revisione esterna non è più un criterio.

---

## 6. Costi

### 6.1 Mensili, in più rispetto a oggi

| Periodo | v2.1 | P-D | Fonte |
|---|---|---|---|
| Fasi 0-1, con Azure accesa | circa 135 € | circa 135 € | [verificato: P §12.1] |
| Fase 2, con Azure spenta | da -15 a +20 € | uguale. In più si toglie Metricool (59,86 €) dalla fase 2 invece che dopo la fase 4. Metricool è nel kit commerciale, contato a parte | [verificato: P §12.1, §14 decisione 15; R36 §12]; anticipo [proposta] |
| Fasi 3-4 | da -1 a +70 € | uguale; +44-90 € se Andrea parte nella fase 3; +10-11 € della linea di riserva, da accendere prima di Andrea | [verificato: P §12.1, §14 decisione 13] |
| Fasi 5-6 | da 46 a 168 € | uguale | [verificato: P §12.1] |
| Listino a regime | circa 479-583 € | circa 479-583 € | [verificato: P §12.1] |

**API di Claude.** La stima resta 90-250 € al mese, con un tetto a 250 € [verificato: P §1].
- I passi N costano poco. Haiku 5.5 costa da 0,10 $ in ingresso e 0,50 $ in uscita per milione di token, Sonnet 5.5 2 $ e 10 $ [verificato: R36 §5.3].
- Un post-call con 20.000 token in ingresso e 1.000 in uscita su Sonnet costa circa 0,05 $ [non verificato: calcolo mio].
- Più autonomia vuol dire però più lavori al giorno, quindi il tetto resta.

**Claude Team a fine bundle.** Da 214 a 447 € al mese [verificato: P §12.1]. Gli automatismi non consumano i posti [verificato: ADR-0004].

**Abbonamenti facoltativi**, solo se un pezzo non regge (§2.5):
- voce in cloud, circa 88 € al mese;
- Metricool, 59,86 € al mese;
- utente di servizio M365 per n8n, 6,41 € al mese [non verificato: R33, riga 68]. Con la Porta non serve.

### 6.2 Una tantum

| Voce | v2.1 | P-D | Fonte |
|---|---|---|---|
| Oggi: parere (tetto 2.500), credito API (0-223), backup in sede (165-500), chiavi FIDO2 del board (232-464), accessori (0-200) | circa 2.900-3.890 € | uguale | [verificato: P §1, §12.2] |
| Revisione esterna di sicurezza | 3.560-5.940 €, condizione entro la settimana 21 | facoltativa: risparmio fino a 5.940 € | [verificato: P §12.2, decisione 5] |
| RAM, altri 192 GB | 690-830 € prima della fase 3 | 690-830 € quando il margine scende sotto i 5 GB: di solito nelle fasi 5-6, prima se Andrea parte nella fase 3 | [verificato: P §6.3]; momento [non verificato: stima del §2.3] |
| Seconda GPU con il riser | 880-1.220 € | uguale | [verificato: P §14, decisione 12] |
| Linea internet di riserva | 77-200 € più 10-11 € al mese | uguale, prima di Andrea | [verificato: P §14, decisione 13] |
| Vivavoce; attivazione del numero di Andrea; batterie dell'UPS se il test va male | 100-250; 7-14; 140-550 € | uguale | [verificato: P §12.2] |

### 6.3 Il tempo di sviluppo, che è il costo vero

| Fase | v2.1, gp di base [verificato: P §15; R36 §7.3] | P-D, gp di base [non verificato: stima mia] | Cosa cambia |
|---|---|---|---|
| 0 | 18 | 17,5 | la prova delle intestazioni in LiteLLM passa alla fase 2; n8n va sul banco |
| 1 | 22,5 | 20 | niente motore SDK; Cancello a livelli; Jira e calendario |
| 2 | 58,5 | circa 56 | runner sottile, renderer e Postiz; brief e offerte anticipati; Cancello più semplice |
| 3 | 61,75 | circa 55 (+28 se Andrea è anticipato) | coaching anticipato |
| 4 | 26,5 | circa 22 | Postiz già fatto |
| 5 | 38 | circa 37 (circa 9 se Andrea è anticipato) | — |
| 6 | 24 | circa 22 | — |
| **Totale** | **249,25** | **circa 230** | con la riserva circa 307 gp contro circa 332 |

**Come si legge.**
- Le fasi 0 e 1, che oggi si chiedono, valgono circa 37,5 gp, cioè circa 50 con la riserva, contro 40,5 e 54 della v2.1.
- P-D non accorcia molto il calendario. Call, voce, memoria, canali e contenuto degli agenti costano come prima. Cambia cosa è autonomo e quando.
- La stima va rifatta con Mattia.

### 6.4 Cosa cambia nelle decisioni dei CEO

- **Decisione 5:** la revisione esterna diventa facoltativa.
- **Nuova:** i tetti per classe dopo il parere, al posto dell'attuale «quali messaggi possono diventare Sempre» [verificato: P App. A, B5].
- **Andrea anticipato,** solo se vale «prima il funnel».
- **Per Michele:** n8n sul banco di prova; il Cancello in un container; la VLAN 32 non serve più.

---

## 7. Cosa cambia nella milestone 1 (lo spec)

### 7.1 Il nuovo perimetro

**Nome:** «Cancello a livelli e primi flussi n8n, su dati di prova». Come oggi gira sulle macchine di sviluppo, con dati verdi di prova [verificato: SPEC §1].

**Dentro:**
- il Cancello con classi e livelli in `config/classi.yaml`: L0-L3, tetti, orari, gruppi di destinatari, approvatori;
- i divieti fissi nel codice;
- carte L1 e finestre L2 decise dalla Porta di prova;
- L3 dentro i tetti;
- outbox con chiave d'idempotenza ed esito «incerta»;
- registro `azioni`, annullo, lista di soppressione, stop;
- esecutori di prova per posta, Jira, calendario e CRM;
- n8n 2.x fissato, con due flussi su dati registrati: post-call e debrief;
- le impostazioni di n8n per il testo rosso (§4.4);
- i contatori per le promozioni.

**Fuori:**
- runner SDK e LiteLLM, che vanno alla fase 2;
- Teams vero, alle milestone 2 e 3 del PRD;
- Graph vero, alle milestone 3 e 4.

### 7.2 Lo spec, parte per parte

| Parte dello spec | Oggi (revisione 2) | Con P-D |
|---|---|---|
| §2.1 Ponte | `propose_action`, un effetto per giro, ripresa della sessione con l'esito | tolto. n8n manda le azioni al Cancello con una chiave d'idempotenza; l'esito torna come evento |
| §2.2 Prove | modello a copione che imita l'API, più un giro dal vivo | dati e risposte registrati nei flussi; un giro dal vivo con tetto di 2 $ prima di chiudere |
| §2.3 PostgreSQL | `embedded-postgres` 16 | uguale |
| §3 Architettura | due processi, tre ruoli del database, firme HMAC con numero monouso | tre processi (n8n, Cancello, Porta di prova); un token per servizio sulla rete interna; sul registro il Cancello può solo inserire e leggere |
| §4.1 Registro dei profili | lista bianca, tre barriere | registro delle classi e dei flussi. I profili S arrivano nella fase 2 con `tools` ristretto, `dontAsk` e `settingSources: []` come semplice configurazione |
| §4.2-4.3 Coda e runner | possesso, battito, lock per profilo | tolti: la coda è quella di n8n |
| §4.4 Corsia N | una chiamata senza strumenti, campi validati | resta, dentro n8n. In più i destinatari vengono dai dati |
| §4.5 Hook | `PreToolUse` con riserva dell'effetto | tolto |
| §4.6 Classi | elenco chiuso nel codice, solo `crm.nota` | tabella in configurazione con i livelli; nel codice solo i divieti |
| §4.7 Carte | copia unica, impronta della Porta, codici per consegna, sette condizioni | testo salvato una volta con la sua impronta. La carta vale se è in attesa e non scaduta, se approva una persona della classe e se il testo è lo stesso. La finestra L2 usa il compito periodico di 30 secondi che lo spec ha già per le scadenze [verificato: SPEC §4.7] |
| §4.8 Outbox | due strade, trigger, esecutore che ricalcola tutto | tre strade: carta approvata, finestra scaduta, L3 nei tetti. Resta l'esito «incerta» senza nuovi tentativi |
| §4.9 Registro | catena con MAC e ancora esterna | tabella a sola aggiunta, con i segreti oscurati |
| §4.10 Stop | epoca, `FOR UPDATE` e `FOR SHARE` | un interruttore che l'esecutore legge prima di ogni effetto; annulla carte e finestre |
| §4.11-4.12 Ripresa e tetti | esiti confermati uno per uno; riserve sul mese | esiti come eventi con chiave unica; tetti di quantità; spesa con il limite della Console |

### 7.3 I 27 criteri

| Criteri | Con P-D |
|---|---|
| AC-001, AC-002, AC-008 | restano per le carte L1, senza la ripresa della sessione |
| AC-003 | cambia: scrittura interna per livello in configurazione, non da un elenco nel codice |
| AC-004 | si semplifica: con il Cancello che non risponde non c'è effetto; n8n ritenta con la stessa chiave |
| AC-005, AC-006, AC-014, AC-018, AC-020, AC-022 | tolti: riguardano solo le sessioni SDK |
| AC-007 | resta: sono i limiti fissi |
| AC-009 | si semplifica: resta l'impronta del testo; escono l'impronta calcolata dalla Porta e il controllo dei caratteri invisibili |
| AC-010, AC-025, AC-026 | restano: un solo effetto, l'incerto non si ripete, idempotenza |
| AC-011 | si semplifica: approva chi oggi è nella classe |
| AC-012 | si semplifica: un token per servizio |
| AC-013 | resta, nella forma n8n |
| AC-015 | si semplifica: niente epoche; «nulla riparte da solo» resta |
| AC-016 | tolto |
| AC-017 | resta, come «importante» |
| AC-019, AC-027 | si riducono a idempotenza ed esiti non persi |
| AC-021 | si semplifica: tetti di quantità e di spesa |
| AC-023 | cambia: batteria su dati registrati, gratis, con un comando |
| AC-024 | passa alla fase 2 per il runner, con tre scenari |

### 7.4 I criteri nuovi [proposta]

1. **L2:** senza «Ferma» l'azione parte alla scadenza; con «Ferma» non parte; con «Manda ora» parte subito.
2. **L3:** l'azione parte subito dentro i tetti; oltre il tetto scende a L1 come carta.
3. **Destinatari:** un destinatario fuori dal gruppo della classe fa scendere l'azione a L1.
4. **Soppressione:** un «no» blocca le azioni verso quel contatto su tutti i canali.
5. **Annulla:** una scrittura interna si annulla senza cancellare, e il registro lo mostra.
6. **Promozioni:** i contatori propongono la promozione; promuove solo il responsabile; la retrocessione è automatica.
7. **Riga AI:** è presente nelle azioni esterne L2 e L3.
8. **Testo rosso:** non resta nei database di n8n né del Cancello.
9. **Debrief:** arriva alle 7:00 su dati di prova.

### 7.5 Decisioni e giorni

**Decisioni del gate.**
- **D1:** la carta L1 scade dopo 3 giorni lavorativi, con un promemoria nel debrief. Oggi sono 48 ore, e un fine settimana basta a farla scadere [verificato: SPEC §9; Rapp. 2, collo n. 12].
- **D2, D3, D4:** restano uguali.
- **D5:** TypeScript per il Cancello; i flussi sono JSON di n8n, versionati in git.
- **D6:** tolta.

**Giorni.** Lo stesso lavoro, nella v2.1, vale circa 13 gp: prima parte del runner 1,5, motore sul banco 5,5, Cancello parte 1 6 [verificato: R36 §7.3; SPEC §11]. Con P-D sono circa 8-10 gp [non verificato: stima].

**Documenti da aggiornare.**
- Un nuovo ADR che sostituisce in parte:
  - ADR-0001, perché il motore non è più al centro;
  - ADR-0003, per la carta su ogni azione, la FIDO2, le regole «Sempre» e la VM separata;
  - ADR-0011, perché n8n porta anche la logica dei flussi, e la regola «la logica del motore non dipende da n8n» cade.
- PRD: perimetro, metriche d'autonomia, milestone.
- P: §5.4, §9.1 regola 10, §11.
- D03: §4.

---

## 8. Rischi principali e strade d'uscita

| Rischio | Come lo gestiamo | Strada d'uscita |
|---|---|---|
| Un messaggio sbagliato parte da solo verso un cliente | L2 prima di L3; solo destinatari noti; testo dal modello, destinatari dai dati; riga AI; retrocessione automatica; rettifica | la classe torna a L1 con un tocco, a costo zero |
| Il parere dice no a L2 e L3 per le mail verso l'Italia | quelle classi restano L1 dove il parere lo chiede | resta il guadagno sul lavoro interno e su Andrea, se è ammesso |
| n8n diventa il punto critico: nel 2026 una vulnerabilità con CVSS 10 [non verificato: fonti di terzi citate in ADR-0011]; la 3.0 cambia l'API [verificato dal Rapp. 4 §5] | versione 2.x fissata; da internet solo webhook firmati, nessun modulo pubblico; patch entro 14 giorni [verificato: ADR-0011]; flussi in git; prove su dati registrati | i flussi diventano lavori del runner SDK (circa 1 gp per un flusso semplice [non verificato]). Cancello, Porta e memoria restano |
| La licenza di n8n vieta la rivendita | il sistema interno non cambia | per offrirlo alle PMI i flussi passano al runner o a una licenza commerciale di n8n, con un prezzo che non è nei file [verificato per il divieto: ADR-0011] |
| La logica è sparsa in tanti flussi visuali | un flusso per agente, con nome e responsabile nel registro; sottoflussi comuni; test | — |
| I flussi a una chiamata non bastano per i casi nuovi | i casi che non rientrano vanno a una sessione S o a una persona («serve un umano») | — |
| n8n su Teams non registra chi approva [verificato: R28 §2.4] | carte e «Ferma» passano dalla Porta, con l'identità da provare | pagina del Cancello con Entra; oppure Wait di n8n con «Limit Wait Time», senza il nome di chi ferma |
| Il collo di bottiglia è Michele [verificato: R35-cpto §6] | P-D toglie la VM e la VLAN del motore ma aggiunge worker di n8n e il renderer: il conto dei servizi cambia poco | — |
| Andrea anticipato senza lead | regola «prima il funnel» alla settimana 21 | resta nella fase 5 |
| Una sola linea internet; server da riaccendere a mano dopo un blackout [verificato: P §13] | linea di riserva prima di Andrea; riaccensione automatica a scelta di Michele [verificato: DOM n. 22]; ritentativi di n8n | — |
| Iniezioni di istruzioni nel testo di terzi | passi AI senza strumenti; destinatari dai dati; tetti; L3 solo verso destinatari noti | una classe sospetta torna a L1 |
| Meno sicurezza, per scelta | registro, annulla, stop, tetti | revisione esterna se un cliente la chiede |
| Giudizio «meno agentico»: la lente visione ha penalizzato la P3 per questo [verificato: R35-vis §3.2] | nessuna figura diventa una skill da aprire a mano: tutte e 57 lavorano da sole come flussi, sessioni o servizi; P3 ne aveva 10 di tipo «skill aperta da una persona» [verificato: R34-3 §5] | qualsiasi flusso può diventare una sessione S |
| L'apprendimento non ha volumi su cui lavorare | si comincia dalle correzioni ai post-call | — |

---

## 9. Funzioni: nessuna si toglie

**Sigle della tabella.** N = flusso n8n con passi AI; S = sessione SDK; V = servizio.

**Fonti della tabella.** Componenti, cose che servono ancora e costi vengono da P App. A [verificato]. Apollo e Higgsfield da R34-3 §8 [verificato]. Livelli e fasi di P-D sono una proposta.

**Nessuna figura resta una skill da aprire a mano.** Stimo circa 35-40 N, 10-12 S e 7-9 V [non verificato: classificazione mia].

| Voci | Come in P-D | Livello a regime | Fase | Cosa serve ancora, e quanto costa |
|---|---|---|---|---|
| J1 | flussi, eventi, un Cancello, una memoria, la Porta | L3 interno | 1-6 | — |
| J2 | registro dei flussi e dei profili, con responsabile e tetti | un agente nuovo nasce con L1 | 1-2 | riga nel registro dei trattamenti |
| J3 | Agente email (N) | classificazione L3; risposte a contatti noti L2; primi contatti L1 | 2-3 | decisione D0 sull'email; parere |
| J4 | eventi fra flussi e sessioni | L3 | 2 | — |
| J5 | Teams via Graph; Vexa | L3 | 1; 3 | il cliente deve ammettere il bot; 12 GB per Vexa |
| J6 | brief e slide (S più renderer) | L3 per noi; L2 al cliente | 2-3 | template SerSan |
| J7 | Editoriale, concorrenza, metriche, Copywriter (N); video e grafiche (S) | L3 interno | 2-4 | Higgsfield 41,99 €/mese, come eccezione |
| J8 | Agente task (N); Project manager, Report cliente, Onboarding, Sviluppatori (S) | to-do L3; report L2; pull request L1 | 1; 4 | Jira Standard, 28 €/mese, se serve |
| J9 | Teams con la Porta e nove bot; Telegram, Slack, WhatsApp; Buzz nel laboratorio | L3 interno | 1-4 | WhatsApp 7-12 €/mese; Slack 0-27 €/mese; verifica Meta |
| A1 | Graph, Vexa, telefono, avviso | L3 | 1-3 | parere sull'art. 4 dello Statuto; DPIA |
| A2 | BookStack e PostgreSQL | lettura L3; pagine ufficiali L2 | 2 | MariaDB, 1 GB |
| A3 | Qdrant con MCP RAG | L3 | 3 | pipeline del board (F4) |
| A4 | n8n e runner sul server | — | 1 banco; 2 server | posto sul server (F4 o posto agenti) |
| A5 | Raccoglitore, Pulitore, Bibliotecario (N o V); Archivista come lavoro fisso | L3 | 3 | — |
| A6 | apprendimento dalle correzioni; istruzioni con valutazione | L3; L2 | 2; 4 | esempi fissi per ogni flusso |
| A7 | eventi, canale «Agenti», stand-up, chiusura dei to-do | L3; to-do delle persone L2 | 1-2 | — |
| B1 | recap nel canale del cliente | L3 per i clienti attivi | 3 | canali condivisi da provare |
| B2 | meeting e deal in SersanOutreach | L3 | 2 | SersanOutreach su HTTP con «crea deal», 3,5 gp |
| B3 | follow-up | L3 ai noti; L2 dopo la prima call | 1-2 | parere |
| B4 | to-do in Jira | L3 | 1 | — |
| B5 | scala L0-L3 per classe | — | 1-2 | tetti dei CEO dopo il parere |
| C1 | debrief alle 7:00 | L3 | 1 | — |
| C2 | registrazione automatica di Teams; Vexa | L3 | 3 | provare se Teams registra senza nessuno di SerSan |
| C3 | passo N | L3 | 1 | — |
| C4 | dettatura delle app Claude; note vocali trascritte in casa | — | 0; 3 | — |
| C5 | registro dei meeting in PostgreSQL | L3 | 1 | — |
| C6 | regole di ciascuno: file versionato, poi BookStack | lettura L3 | 1-2 | — |
| D1 | pipeline pesata calcolata dal codice | L3 | 5 | pesi dichiarati fino a 30-50 chiusure |
| D2 | brief dall'email (S) | L3 | 2-3 | via consentita per LinkedIn: estensione di SersanOutreach o Apollo, 43,78 €/mese; casella attiva per le aperture; DPIA |
| D3 | registro dei meeting, poi MCP RAG | L3 | 2-3 | — |
| D4 | slide (S più renderer) | L3 per noi; L2 al cliente | 2 | template |
| D5 | offerta (S su Opus) | bozza L3; invio L1 | 2 | — |
| E1, E2 | piano con riserva; prezzi rilevati | — | tutte | — |
| E3 | LiteLLM; sul banco una chiave per flusso | L3, con avviso e stop | 1-2 | LiteLLM dalla fase F4 |
| E4 | formazione documentata | — | 0 | — |
| F1 | metadati M365 aggregati, con l'accordo di ciascuno | L3 | 4 | API di M365 da individuare |
| F2 | Intervistatore in chat Teams (S) | L3 | 4 | — |
| F3 | mappa dei processi (S) | L3; libro «Processi» L2 | 4 | — |
| F4 | ore implicite (N) | L3 | 4 | — |
| F5 | Claude Team, Open WebUI | — | 0 | — |
| G1 | canale «Call di vendita» | L3 | 3 | — |
| G2 | fit score (N) | L3 | 5 | volumi di call |
| G3, G4 | valutazione e report alla persona; aggregati al responsabile | L3 | 3 | parere per andare oltre gli aggregati |
| G5, K10 | Andrea: richiamata, chiamate in entrata, esito | L3 | 3 se vale «prima il funnel», altrimenti 5 | 44-90 €/mese tra linea, Registro e modelli; 7-14 € di attivazione; parere; lead vere |
| G6 | aperture con finestra e test A/B | L2 | 3-5 | volumi |
| G7 | misure nel debrief | L3 | 3-5 | — |
| G8 | Analista vinto/perso (N) | L3 | 3 | chiusure: oggi 0 |
| G9 | registro: un flusso pesa poco sulla RAM | — | 2-6 | RAM oltre 6-8 sessioni S insieme |
| G10 | il risultato dell'insieme | — | tutte | — |
| H1-H7 | come nella v2.1. Con n8n tutti possono costruire flussi | — | 0-6 | premio 50-100 €/mese |
| I1-I4 | contesto in memoria; flussi e skill su misura; aree senza AI come classi L0 o vietate; marketing creativo | — | 1-6 | — |
| K1 | evento del debrief in calendario | L3 | 1 | — |
| K2 | «tre nuove call» passano all'Agenda | L3 ai noti; L2 ai nuovi | 2 | — |
| K3 | Smistatore posta (N) | smistamento L3; risposte standard L2-L3; le altre L1 | 2-3 | accordo di ciascuno sulla propria casella |
| K4 | Claude Team con MCP RAG; Capo di gabinetto | L3 | 3 | rosso oscurato fino al parere |
| K5 | Agente intake (N) | brief L3; onboarding L2 | 2-3 | — |
| K6 | slide con la storia della relazione | L3; L2 al cliente | 2-3 | — |
| K7 | template e renderer | — | 0-2 | template |
| K8 | portale su SersanOutreach | L3 | 5 | — |
| K9 | newsletter con listmonk | L1 | 4 | relay SMTP, meno di 1 €/mese |
| K11 | vinti e persi; clienti simili | analisi L3; primo contatto L1 | 3; 5 | volumi |
| K12 | piano mensile del Coach | L3 | 3 | — |
| K13 | mappa dei processi per i clienti | — | 4-6 | istanza separata, da progettare |
| K14 | numeri di Sirius in PostgreSQL via n8n | L3 | 3-6 | esportazione da Sirius (F4); capire cos'è Sirius |
| K15 | acquisti: fatture dei fornitori registrate | L3; pagamenti L0 | 6 | strumento di fatturazione |
| K16 | assistente personale | azioni verso terzi L1 | 6 | account Claude personale, 15-18 €/mese |
| L1 | contratti con DocuSeal | L1 | 6 | valore della firma nel parere |
| L2 | fatture e solleciti | fatture L1; solleciti L2 | 6 | decisione 22 |
| L3 | margini e cassa | L3 | 6 | dati di Sirius |
| L4 | bandi | L3 | 2-3 | pipeline del board |
| L5 | assistenza nella stanza del cliente | standard L2; le altre L1 | 6 | come B1 |
| L6 | rinnovi | segnali L3; proposte L1 | 6 | — |
| L7 | casi studio | bozza L3; testimonianza L1 | 6 | — |
| L8 | commenti della pagina aziendale | L2 per lo standard; profili dei founder L0 | 4 | accesso API alla pagina LinkedIn da verificare |
| L9 | sito e SEO | pull request L1; deploy a mano | 6 | — |
| L10 | webinar ed eventi | iscrizioni e promemoria L3; inviti L1 | 6 | licenza dei webinar di Teams da controllare |
| L11 | sorveglianza del server | lettura L3; patch L1 (Michele) | 3 | monitoraggio del board (F3) |
| L12 | Allenatore AI | L3 | 6 | — |

**In sintesi.** Tutte le 90 voci hanno un componente.

**Le necessità esterne sono le stesse della v2.1:**
- operatore telefonico, relay SMTP, WhatsApp, Slack;
- eccezioni del kit commerciale;
- RAM e seconda GPU.

**I prezzi sono quelli già verificati** [verificato: P §12, §14]. **Le tre differenze sono di calendario:** Postiz, brief e offerte arrivano prima; coaching prima; Andrea prima, se la condizione è vera.
