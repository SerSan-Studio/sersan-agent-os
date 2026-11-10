# Proposta P-B: orchestratore autonomo pronto, con il nostro Cancello

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **P-B**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

**Sigle delle fonti.**
- Tutti i file sono nella repo `C:\Users\alber\sersan-agent-os` e li ho letti il 9/11/2026:
  - **P** = `PRESENTAZIONE-CEO.md` v2.1;
  - **SPEC** = `docs/superpowers/specs/2026-11-09-nucleo-motore-cancello-design.md`;
  - **PRD** = `.claude/prds/sersan-agent-os.prd.md`;
  - **D03** = `docs/03-architettura.md`; **DOM** = `DOMANDE-PER-MICHELE.md`; **ADR-00xx** = `docs/adr/`;
  - **R10, R16, R18, R20A, R27, R30, R31, R34-1, R34-2, R35V, R36** = i file di `ricerca/` con quel numero.
- **TR** è la trascrizione di riferimento, con il minuto. **T1, T2, T3** sono le trascrizioni di terzi `Grokbot vs Hermes.txt`, `grokbot transcript.txt` e `claude and grokbot updates.txt`.
- Il 9/11/2026 ho fatto alcuni controlli sul web, in sola lettura:
  - **GH-REL**: i rilasci di Hermes su api.github.com;
  - **GH-143547** e **GH-113578**: le due issue di Hermes, sulla stessa API;
  - **N8N**: la pagina del nodo Wait su docs.n8n.io.
- Cito i quattro rapporti di questo giro come «Rapporto N».
- Non ho modificato file della repo e non è rimasto acceso nessun processo.

---

## 1. L'idea in 5 righe

1. Gli agenti girano su Hermes Agent, sul server di Michele. Hermes ha licenza MIT e costa 0 €. Dà già pronti profili con nome, cron, kanban con dispatcher, delega, skill che l'agente scrive da solo e canali [verificato: R27 §2.1, §9.2]. È lo stesso orchestratore open source usato nella trascrizione di riferimento [verificato: TR 3:34-3:59].
2. Il Cancello resta l'unico pezzo che agisce verso l'esterno. Non chiede più una carta per ogni azione: dà a ogni classe d'azione un livello, da L0 a mano a L3 autonomo, con la finestra L2 e il tasto «Annulla» [non verificato: proposta].
3. Una classe sale di livello quando lo dicono i numeri: carte approvate senza modifiche, finestre passate senza «Ferma». Scende da sola al primo errore [non verificato: proposta].
4. Restano solo le protezioni essenziali: limiti fissi, stop, tetti di spesa, registro semplice, correzione degli errori, conformità minima [verificato: indicazione di Alberto del 9/11/2026, nel compito].
5. Il limite, detto chiaro: sul gateway di Hermes sono risolti 83 problemi su 312. Fra quelli aperti c'è quello degli avvisi che finiscono nella chat di un altro bot. Per questo l'autonomia verso i clienti parte solo dopo la prova delle settimane 5-8 [verificato: GH-143547, aggiornata il 9/11/2026].

---

## 2. Componenti e dove girano

### 2.1 I pezzi

| Componente | Cosa fa in P-B | Dove gira | RAM | GPU | Fonte |
|---|---|---|---|---|---|
| Hermes, 3 contenitori aziendali | commerciale (Outbound, Chiamate, Vendite); marketing e studio; direzione, progetti, memoria e amministrazione. Profili, kanban, cron, delega, skill. Niente terminale, niente esecuzione di codice, niente strumenti che inviano | server, VM `agenti-01`, Docker con immagine fissata per digest | 8-12 GB in fase 2; 14-18 GB a regime | no | Hermes non usa la GPU [verificato: R10 §7]; 2-4 GB consigliati per contenitore [verificato: docs Docker in R34-2 §3.2]; totali [non verificato: stima mia su R34-2 §3.5] |
| Un solo bot Teams di Hermes | il «Capo di gabinetto»: si parla con lui e lui passa il lavoro | contenitore direzione; ingresso `/api/messages` via Pangolin | nel contenitore | no | adattatore Teams senza portale Azure [verificato: R27 §5]; regola Pangolin per percorso [verificato: R36 §4.4] |
| Hermes personali (fase 6) | assistente personale (K16), uno per chi lo vuole | stessa VM | 4-8 GB in tutto | no | [non verificato: stima] |
| Hermes di prova | ogni aggiornamento passa i 10 scenari prima dell'uso | VLAN 90 LAB | 8 GB nel pilota, insieme a Cancello e PostgreSQL; poi 4 | no | stage in LAB [verificato: R36 §4.1, §7.1] |
| Cancello | classi e livelli, finestra L2, «Annulla», esecutori, registro, stop, tetti; bot Teams delle carte; avvisi e «Ferma» su Telegram; servizio «passa» fra contenitori | VM `cancello-01` | 3-4 GB | no | [verificato: R36 §4.1, stima di quel rapporto] |
| n8n | ingressi: trascrizioni Teams da Graph ogni 5-10 minuti, calendario, modulo del sito, webhook, messaggi dei clienti; orari critici come il debrief | board | nel board | no | [verificato: R30 §3.4; R36 §4.1] |
| LiteLLM | chiavi per profilo, squadra e persona, budget, cache | board, fase F4 | nel board | no | [verificato: R27 §3.1; R36 §4.1] |
| Memoria | PostgreSQL 16, Qdrant con MCP RAG, BookStack con MariaDB, server MCP di lettura | board e LXC `mcp-01` | MariaDB 1 GB; `mcp-01` 3-4 GB | embedding sulla RTX 4000 | [verificato: R36 §4.1] |
| Call | trascrizione nativa di Teams via Graph; Vexa per le call dei clienti; trascrizione in casa | M365; VM `meet-01`; LXC `ai-gpu-01` | Vexa 12 GB con 3 bot; trascrizione 6-8 GB | 2-4,5 GB di giorno | [verificato: R30 §3, §6; R36 §4.1] |
| Andrea | Asterisk, Pipecat, operatore telefonico italiano | `voce-01`, `andrea-01` | 1 GB + 6-8 GB su CPU; 4 GB con la seconda GPU | seconda GPU | [verificato: R31 «In breve», §8; R36 §4.1] |
| Postiz, listmonk, DocuSeal, fatturazione | come nella v2.1 | contenitori | 2,5 + 2,5 GB | no | [verificato: R36 §4.2] |
| Buzz, Paperclip | prove in laboratorio | Experimental-2 | 4-8 GB | no | [verificato: R36 §4.1] |
| Cloud del board | M365 ed Entra (Teams, Outlook), Claude Team, API Anthropic, Jira, Instantly, DNS, macchina Oracle | cloud | | | [verificato: P §5.1] |
| Esterni da ammettere | operatore telefonico, WhatsApp, Telegram, Slack, relay SMTP | cloud | | | [verificato: P §5.1] |
| Abbonamenti facoltativi | Hermes Cloud per la continuità su dati verdi; voce in cloud per anticipare Andrea; linea di riserva | cloud | | | §6.3 |

### 2.2 Cosa dà pronto Hermes e cosa scriviamo noi

**Pronto, lo usiamo così com'è:**
- profili con nome, `SOUL.md`, memoria, skill e canali propri [verificato: R10 §4.1];
- kanban [verificato: docs kanban in R34-2 §5.1]:
  - un dispatcher che passa ogni 60 secondi e una corsia di revisione;
  - il blocco «serve un umano» e lo stop dopo 2 fallimenti di fila;
  - il rifiuto dei cicli di dipendenze e i tetti sui lavori in corso;
  - nella v0.23 i lavoratori della kanban «are usable again» [verificato: GH-REL v0.23.0];
- cron in linguaggio naturale. Si può fermare un lavoro in corso e decidere, per ogni lavoro, cosa fare dei turni persi (`--catch-up on|off`) [verificato: GH-REL v0.23.0];
- skill che l'agente scrive e cura da solo [verificato: R10 §4.2]. Con `hermes curator lock` una skill curata a mano non si può più riscrivere, nemmeno in modalità YOLO [verificato: GH-REL v0.23.0];
- delega a sottoagenti, con uno schema per la risposta [verificato: R10 §4.1];
- API `/v1/runs` e webhook firmati HMAC, così n8n e il Cancello possono far partire Hermes [verificato: R27 §4];
- tetti di spesa per gli strumenti a pagamento, validi anche in YOLO [verificato: GH-REL v0.23.0];
- `hermes pause`, che ferma cron e kanban [verificato: R10 §4.2].

**Da scrivere:**
- il Cancello con i livelli e i suoi esecutori, più il bot delle carte;
- il servizio «passa», che porta il lavoro da un contenitore all'altro;
- gli MCP di lettura: memoria, BookStack, Jira, SersanOutreach, posta e calendario;
- i flussi n8n degli ingressi;
- lo sblocco della card quando arriva l'esito della carta [non verificato: da provare, come scrive R34-2 §5.4 punto 6].

### 2.3 Perché tre contenitori e un solo bot

- **La kanban non attraversa i contenitori.** Vive in un SQLite per istanza ed è «single-host by design» [verificato: R34-2 §5.2]. I passaggi più frequenti (mail → agenda → brief → proposte, e il post-call) restano quindi nello stesso contenitore, dove la kanban fa tutto da sola.
- **Un bot per gateway.** Quando un gateway serve più bot, gli avvisi di un profilo arrivano nella chat di un altro (MSG-43, ancora aperto) [verificato: GH-143547]. Con un bot solo il problema non si presenta. Un utente che usa Hermes da mesi racconta chat di bot diversi che si mescolano [verificato: T1].
- **Meno profili per gateway.** La scheda dei problemi segnala installazioni con molti profili che si bloccano o ripartono [verificato: GH-143547, sezione «Several profiles»]. Tre contenitori dividono il carico.
- **Si parla con il Capo di gabinetto, che smista il lavoro.** È lo stesso schema usato dalle persone delle trascrizioni di terzi [verificato: T1, T2].
- **I clienti non parlano mai con Hermes.** WhatsApp, Slack e i canali condivisi passano dal Cancello in uscita e da n8n in entrata [non verificato: proposta; la regola «lì scrive solo il Cancello» è verificata in P §4.11].
- **Fra contenitori il lavoro passa con «passa».** È un piccolo servizio del Cancello che apre la card nell'altro contenitore via webhook [non verificato: proposta sul modello dell'MCP «passaggi», R34-2 §5.2, 3 gp].
- Nella fase 1 basta un contenitore con 5 profili. Si divide in tre nella fase 2 [non verificato: proposta].

### 2.4 RAM e GPU, fase per fase

Il board lascia circa 53 GB liberi [verificato: R36 §4.2]. La tabella conta i GB nuovi [non verificato: stima mia sul modello di R36 §4.2 e R34-2 §3.5].

| GB nuovi | Fase 1 (stage) | Fase 2 | Fasi 3-4 | Fasi 5-6 |
|---|---|---|---|---|
| Stage (Hermes, Cancello, PostgreSQL) | 8 | 4 | 4 | 4 |
| Hermes, contenitori aziendali | 0 | 8-12 | 12-16 | 14-18 |
| Hermes personali | 0 | 0 | 0 | 4-8 |
| Cancello e bot delle carte | 0 | 3 | 3 | 4 |
| `mcp-01`, MariaDB, crescita dei database | 0 | 5 | 8 | 10 |
| Trascrizione e Vexa | 0 | 0 | 18 | 20 |
| Postiz, listmonk e SersanOutreach | 0 | 0 | 3,5 | 4,5 |
| Andrea su CPU, DocuSeal e fatturazione | 0 | 0 | 0 | 10,5 |
| **Totale nuovo** | **8** | **20-24** | **48,5-52,5** | **71-79** |
| **Liberi con 192 GB** | **circa 45** | **circa 29-33** | **circa 0,5-4,5** | **da -18 a -26** |

**Come si legge.**
- Con P-B la RAM si comporta come nella v2.1: i 192 GB in più servono prima della fase 3 (decisione 11, 690-830 €) [verificato: P §6.3, §14].
- In P-B il limite non è un tetto di sessioni: la kanban limita i lavori in corso per contenitore e per profilo [verificato: R34-2 §5.1]. Si parte con 3-4 lavori per contenitore, come nella P2, e si misura [verificato: R35V §2; numeri di partenza: proposta].
- La GPU non cambia rispetto alla v2.1:
  - il Qwen3-4B non può fare da modello di un profilo Hermes, perché Hermes vuole almeno 64.000 token di contesto [verificato: R27 §2.4];
  - di giorno la RTX 4000 lavora per la pipeline [verificato: P §6.4];
  - la seconda GPU da 16 GB serve dalla fase 3, al più tardi dalla fase 5 (decisione 12, 880-1.220 €) [verificato: P §6.4, §14].

### 2.5 La variante in abbonamento

- **Hermes Cloud** [verificato: R18 §2.4]:
  - ha la regione di Londra;
  - il piano Plus costa 20 $ al mese, con 22 $ di crediti;
  - l'istanza si paga a giorni: secondo una fonte terza 0,56 $ per la Medium e 1,09 $ per la Large;
  - un DPA e i canali disponibili nella versione ospitata non sono stati trovati.
- Dalla v0.23 gli agenti di Hermes Cloud li aggiorna Hermes Cloud stesso [verificato: GH-REL v0.23.0].
- **Hermes for Business** gira su un tenant dell'infrastruttura di Nous, con un «Team Gateway» per Slack, Telegram, Discord e WhatsApp. I prezzi non sono pubblicati [verificato: R10 §8].
- **Lettura.**
  - Senza DPA, Hermes Cloud non può trattare dati di clienti o lead, perché si ammettono solo fornitori con DPA [verificato: R16 §6 regola 7].
  - Oggi serve solo per tenere vive le routine su dati verdi quando il server è fermo, a circa 33-47 € al mese per istanza [non verificato: prezzi di terzi, cambio di R36].
  - Se Nous offrisse un DPA e Teams, il cloud toglierebbe la manutenzione di Hermes (1,5-2,5 gp al mese) e 14-18 GB di RAM [non verificato: deduzione].

---

## 3. Il modello di autonomia

### 3.1 Le regole comuni

L'unità è la **classe d'azione per un gruppo di destinatari**, per esempio «mail a un cliente con una call registrata negli ultimi 14 giorni». La classe la decide il Cancello dal tipo d'azione e dal destinatario, non da quello che dichiara l'agente [verificato: principio di SPEC §4.6].

| Passaggio | Regola [non verificato: soglie proposte] |
|---|---|
| L1 → L2 | 5 carte di fila approvate senza modifiche, oppure 10 in 30 giorni con al massimo una modifica. Il Cancello propone il passaggio e il responsabile della classe conferma con un tocco |
| L2 → L3 | 20 azioni partite a fine finestra senza «Ferma» e senza correzioni, in almeno 2 settimane. Vale solo per le classi che i CEO, dopo il parere, mettono nell'elenco «può arrivare a L3» |
| Giù di un livello, da solo | una correzione segnalata (tasto «Era sbagliato», reclamo, mail rimbalzata); due «Ferma» in 7 giorni; due «Annulla» in 7 giorni |
| Subito a L1 | un destinatario o un cliente sbagliato; un testo con i dati di un altro cliente |
| Un agente a L0 | ha raggiunto il tetto di spesa: resta fermo fino al mese dopo o finché una persona alza il tetto |
| Tutto a L0 | stop di emergenza; niente riparte da solo |
| A mano | chiunque dei quattro abbassa una classe con un tocco; alzarla spetta al responsabile |

Oggi la regola «Sempre» chiede 20 sì uguali per agente, azione e destinazione, scade dopo 30 giorni e non vale mai per destinatari nuovi [verificato: P §5.4]. Con 11 lead, 1 risposta e 0 meeting al 5/10 [verificato: P §7.1] quella soglia non si raggiunge [verificato: Rapporto 2, collo 2].

**Altre regole comuni** [non verificato: proposte, salvo dove indicato]:
- **Finestra L2.** La carta dice «parte alle HH:MM» e offre tre tasti: «Ferma», «Modifica», «Invia ora». Durate:
  - 30 minuti per follow-up e recap;
  - 2 ore per inviti e risposte;
  - 24 ore per post e documenti al cliente;
  - 48 ore per newsletter e nuove aperture di Andrea.
- **Ore d'invio.** Le azioni L2 e L3 verso l'esterno partono fra le 8 e le 20, dal lunedì al venerdì. Una finestra che scade fuori orario parte alle 8.
- **Destinatari.** In L2 e L3 sono ammessi solo indirizzi già presenti fra i partecipanti della call o nel CRM per quel cliente, e solo nel dominio del cliente. La regola «solo verso il dominio del cliente» c'è già [verificato: D03 §4 punto 7].
- **Dichiarazione AI.** Un messaggio che parte in L2 o L3 lo dice, per esempio «preparato e inviato dall'assistente AI di SerSan per conto di …». L'obbligo per chi scrive da solo a un esterno è verificato [P §9.1 regola 1; R16 §6 regola 1]; il testo è una proposta.
- **Testi con impegni.** Se il testo contiene prezzi, sconti, date di consegna o impegni, il Cancello lo tratta come un'offerta, quindi L1.
- **Routine nuove.** Partono a L1, con le carte visibili, invece che «a secco» per una o due settimane come oggi [regola attuale verificata: P §9.2].

### 3.2 Dopo una call

Nel video i quattro passi avvengono «in modo totalmente autonomo» [verificato: TR 4:47-5:07]. Da noi la card del Post-call la apre n8n, che legge le trascrizioni Teams da Graph ogni 5-10 minuti senza aprire porte [verificato: R30 §3.4]. Per le call organizzate dai clienti entra Vexa, dalla fase 3 [verificato: R36 §7.2].

| Passo | Sett. 8 | Sett. 21 | A regime | Si sale | Si scende |
|---|---|---|---|---|---|
| Riassunto e prossimi passi nel canale interno e nel registro dei meeting | L3 | L3 | L3 | interno, L3 da subito | una correzione si sistema; il livello resta |
| Punti nel canale del cliente (canale condiviso o Slack Connect) | L1 | L2, 30 minuti | L3 per i clienti con relazione attiva; L2 al primo incontro | regole comuni | regole comuni |
| Meeting e opportunità nel CRM | L3 per la nota, se SersanOutreach espone l'operazione; altrimenti dalla fase 2 | L3 | L3 | interno, con «Annulla» per 7 giorni | due «Annulla» in 7 giorni: L2 |
| Mail di follow-up | L1, con la classe L2 pronta da accendere | L2, 30 minuti | L3 per i clienti con relazione attiva; L2 al primo incontro | regole comuni | regole comuni, più rimbalzo o risposta negativa |
| To-do al team in Jira | L3, con «Annulla» | L3 | L3 | interno | due «Annulla» in 7 giorni: L2 |

- Le soglie e i livelli della tabella sono una proposta [non verificato].
- Alla settimana 8 la L2 dipende dal numero di call e dal parere legale, che arriva entro la settimana 3 [verificato: P §9.4].
- L'operazione «crea deal» con l'MCP su HTTP vale 3,5 gp ed è nella fase 2 [verificato: R36 §7.3].
- I canali condivisi con altre organizzazioni vanno provati [verificato: R34-2 §7.3, voce B1].

### 3.3 Debrief del mattino

- **Livello:** L3 alla settimana 8, alla 21 e a regime.
- **Quando parte:** lo avvia n8n alle 7:00 [verificato: P §1], oppure all'ora che ciascuno scrive nelle sue regole; nel video è alle 5:30 [verificato: TR 5:12-5:25].
- **Cosa contiene** [non verificato: proposta]:
  - alla settimana 8: calendario, call di ieri, carte in attesa, to-do creati;
  - alla settimana 21: in più CRM, Jira e numeri;
  - a regime: in più memoria, pipeline ed esiti di Andrea.
  - I numeri si calcolano dal codice, non si cercano nel testo [verificato: R36 §5.5].
- **Rispetto alla v2.1:** nella fase 1 della v2.1 gli agenti non leggono calendario, Jira né CRM [verificato: SPEC §1; PRD «Fuori»]. In P-B è n8n a passare i dati del calendario al debrief già dalla fase 1 [non verificato: proposta].
- **Evento «Debrief» come primo appuntamento in calendario (K1):** L3 dalla fase 2.
- **Se il debrief non arriva**, n8n manda un avviso [non verificato: proposta].

### 3.4 Brief prima di un incontro, con le slide

| Passo | Sett. 8 | Sett. 21 | A regime | Si sale / si scende |
|---|---|---|---|---|
| Brief per ogni incontro esterno in agenda: la sera prima alle 18, oppure 2 ore prima se l'incontro è fissato in giornata | L0, con la skill in Claude Team | L3 su dati pubblici, CRM e posta | L3 con memoria e storico | interno |
| Slide per noi | L0 | L3 | L3 | interno |
| Slide o documento da mandare al cliente prima dell'incontro | L0 | L1 | L2, 24 ore, per i clienti con relazione attiva | regole comuni |
| Presentazione in call | L0 | L0 | L0: la fa la persona | — |

- Nel video il brief parte quando una persona inserisce l'email [verificato: TR 7:42-8:44].
- In P-B n8n legge il calendario ogni sera e apre una card per ogni incontro esterno. Così si chiude il punto AU-19 del Rapporto 1 [non verificato: proposta].
- Il brief è profilazione, quindi va nella DPIA [verificato: P §9.1 regola 9].

### 3.5 Offerta dopo l'incontro

| Passo | Sett. 8 | Sett. 21 | A regime |
|---|---|---|---|
| Bozza dal catalogo entro un'ora dalla call (Agente proposte, con Opus) | L0, skill in Claude Team | non ancora: l'agente arriva in fase 3 | L3 |
| Invio al cliente | L1 | L1 | L1 a Michele per prezzi e perimetro nuovi; L2 di 24 ore solo per i rinnovi a listino sotto una soglia decisa dai CEO |

- **Si sale** solo per i rinnovi a listino, e solo con la decisione dei CEO. **Si scende** al primo reclamo: i rinnovi tornano a L1 [non verificato: proposta].
- La firma tecnica di Michele resta umana [verificato: P §9.3].
- Il video non dice a che livello va l'offerta [verificato: Rapporto 1, AU-21].

### 3.6 Marketing

| Passo | Sett. 8 | Sett. 21 | A regime | Si sale / si scende |
|---|---|---|---|---|
| Ricerca concorrenza, ogni settimana | L0 (skill) | L3 | L3 | interno |
| Temi, bozze, caroselli, numeri del lunedì | L0 (skill) | L3 | L3 | interno |
| Post sulla pagina aziendale | L0, sessione presidiata | L1 | L2 di 24 ore con Postiz, dalla fase 4 | regole comuni; serve cambiare la direttiva «solo da sessione presidiata» |
| Post sui profili dei founder | L0 | L0 | L0, per scelta | — |
| Newsletter | non ancora | non ancora | L1 per ogni numero; L2 di 48 ore quando il testo viene solo da post già pubblicati | regole comuni |
| Risposte ai commenti della pagina | non ancora | non ancora | L1; L2 per le risposte standard | regole comuni |

Le regole di casa sono verificate [P §8.2, §9.3], così come Postiz nella fase 4 [P §11]. I livelli sono una proposta [non verificato].

### 3.7 Andrea, richiamata entro 90 secondi

Nel video Andrea chiama entro 90 secondi, dice di essere un'AI e fissa l'incontro con un commerciale [verificato: TR 14:53-15:12].

| Passo | Partenza (fase 5, sett. 41-48) | A regime |
|---|---|---|
| Richiamata entro 90 secondi a chi ha dato il consenso nel modulo | L3 | L3; di notte solo se il lead ha scelto «richiamatemi adesso» |
| Appuntamento nel calendario di un commerciale e conferma al lead con un modello fisso | L3 | L3 |
| Esito nel CRM e nel canale vendite | L3 | L3 |
| Chiamate in entrata fuori orario | L3 | L3 |
| Lead senza consenso | L0: lo richiama una persona | L0 |

- **Si sale:** non per gradi, perché in 90 secondi non c'è spazio per una finestra. Andrea parte a L3 solo con il parere, il consenso registrato e una prova con una lead finta [verificato: decisione 10 e fase 5, P §1 e §11; R31 §9].
- **Si scende:**
  - chi dice «non chiamatemi più» entra nella lista di soppressione di tutti i canali [verificato: P §9.1 regola 5];
  - due reclami in un mese, o una chiamata senza la frase AI, sospendono Andrea (L0) fino alla revisione [non verificato: proposta].
- La voce di un collega si usa solo con un contratto separato e revocabile [verificato: P §9.1 regola 6, §14 decisione 10].

### 3.8 Coaching delle vendite

| Passo | Partenza (fase 5) | A regime |
|---|---|---|
| Report a chi ha fatto la call, dopo ogni call di vendita | L3 | L3 |
| Al responsabile | dati aggregati, L3 ogni settimana | il report di ogni call, come nel video, solo se il parere lo consente |

- Niente stima delle emozioni, vietata dal 2/2/2025, e niente voto nel CRM [verificato: R16 §4 e §6 regola 3].
- Se ci sono dipendenti valgono l'art. 4 dello Statuto e, con la profilazione, l'alto rischio dal 2/12/2027 [verificato: R16 «Sintesi», punti 3-4].
- In Hermes l'identità verso la memoria vale per contenitore [verificato: R27 §4]. Per questo il report non va nella memoria comune: il Cancello lo consegna solo nella chat 1:1 [non verificato: proposta].

### 3.9 Agenti che si parlano e chiudono i to-do superati

Nel video gli agenti hanno una chat condivisa, si passano il lavoro e chiudono i to-do già fatti [verificato: TR 4:02-4:18; Rapporto 1, AU-09].

| Passo | Sett. 8 | Sett. 21 | A regime | Si sale / si scende |
|---|---|---|---|---|
| Passaggi fra agenti dello stesso contenitore (kanban) | L3 fra i 5 profili | L3 | L3 | — |
| Passaggi fra squadre («passa») | non ancora | L3 | L3 | — |
| Specchio dei passaggi nel canale «Agenti» di Teams | L3 | L3 | L3 | — |
| Chiusura delle card degli agenti già superate | L3 | L3 | L3 | — |
| Chiusura dei to-do delle persone in Jira che risultano fatti | non ancora | L2: avviso al titolare, chiusura dopo 24 ore se non dice no | L3 con «Riapri», quando la prova è nel registro (meeting tenuto, mail partita) | un to-do riaperto riporta la classe a L2 |
| «Momento di scambio» del venerdì: ogni squadra rilegge le card aperte | non ancora | L3 | L3 | — |

- **Freno.** Il freno della v2.1 (3 passaggi per catena, 8 messaggi per thread) [verificato: P §4.11] fermerebbe la catena del post-call [verificato: Rapporto 2, collo 6]. In P-B restano i freni della kanban [verificato: R34-2 §5.1] più un tetto in dollari per catena. Oltre il tetto arriva una carta «Continua?» (L1) [non verificato: proposta].
- **Le stanze di gruppo di Hermes non fanno da registro.** Hanno `max_hops` uguale a 4 [verificato: GH-REL v0.23.0], ma 28 problemi aperti [verificato: GH-143547].

### 3.10 Apprendimento dai rifiuti

| Passo | Sett. 8 | Sett. 21 | A regime | Si sale / si scende |
|---|---|---|---|---|
| Skill interne (riassunti, ricerche, formati) che Hermes riscrive | non ancora | L3, con la versione in git e un riepilogo ogni settimana nel canale «Agenti» | L3 | una correzione riporta la versione precedente |
| Skill che cambiano testi verso i clienti | non ancora | L2, 24 ore | L2; L3 dopo 3 cicli senza «Ferma» | regole comuni |
| Skill bloccate: dichiarazione AI, testi legali, regole sui dati | L0 per gli agenti | L0 | L0, con `curator lock` | — |
| Nuove aperture di Andrea, ricavate dai rifiuti | non ancora | non ancora | L2 di 48 ore con prova A/B; poi L3 dentro una banca di frasi approvata | si torna da soli alla versione precedente se il tasso di appuntamenti scende, per esempio del 20% su 30 chiamate |
| Vinti e persi, analisi al marketing | non ancora | L3 | L3 | — |

- Nel video l'agente vocale impara da solo [verificato: TR 15:34-15:43]. Nella v2.1 ogni apertura e ogni skill nuova passa da una carta [verificato: Rapporto 2, voci A6 e G6].
- I livelli e le soglie di questa tabella sono una proposta [non verificato].

### 3.11 Quanto ci avvicina alla trascrizione

| Nella trascrizione | P-B a regime |
|---|---|
| Post-call: i quattro passi L3 | CRM e to-do L3; canale del cliente e mail L3 per i clienti con relazione attiva, L2 di 30 minuti al primo incontro |
| Debrief fatto dalla persona (L0) | L3, preparato |
| Brief che parte dall'email inserita a mano | L3 per ogni incontro in agenda |
| Andrea L3, impara da solo | L3 solo per chi ha dato il consenso; aperture L2, poi L3 dentro una banca di frasi |
| Offerta: livello non detto | L1 |
| Agenti che si parlano e si correggono | L3 |

Restano più bassi per scelta o per legge:
- le offerte con prezzi nuovi;
- i post dei founder;
- i primi contatti a freddo (decide il parere sull'email);
- i pagamenti, mai automatici.

---

## 4. Protezioni essenziali

### 4.1 Le sei protezioni che restano

1. **Limiti fissi.**
   - Cancellazioni e credenziali sono classi negate nel codice del Cancello, non configurabili [verificato: SPEC §4.6].
   - I profili Hermes non hanno terminale, esecuzione di codice né strumenti che inviano [verificato: R34-2 §3.2; `send_message` non è dato al modello, R10 §4.2].
   - Nessun esecutore di pagamento esiste: l'agente prepara, una persona paga (L0) [verificato: P §9.3].
2. **Stop di emergenza.**
   - Si preme da un tasto in Teams, con `/stop` al Capo di gabinetto o da Telegram.
   - Il Cancello nega tutto e annulla carte e finestre aperte. Hermes va in pausa con `hermes pause` [verificato: R10 §4.2] e gli ingressi n8n si fermano.
   - Riparte solo con Alessandro o Michele, e niente riparte da solo [verificato: principio in SPEC §4.10, decisione D2].
3. **Tetti di spesa.**
   - Budget in LiteLLM per profilo, squadra e persona, con avviso all'80% e stop al 100% [verificato: P §9.2; R27 §3.1].
   - Un tetto in dollari per catena di lavoro [non verificato: proposta].
   - I tetti degli strumenti a pagamento di Hermes [verificato: GH-REL v0.23.0].
   - Prima della fase F4 basta una chiave con limite nella Console [verificato: P §11].
4. **Registro semplice.**
   - È una tabella a sola aggiunta: chi ha chiesto, agente, classe, livello, destinatario, testo, chi ha approvato oppure «finestra scaduta» o «autonomo», esito, costo.
   - I segreti vengono oscurati.
   - Il registro si vede in Grafana e in un riepilogo settimanale [non verificato: proposta].
   - Si conserva 90 giorni [verificato: P §9.1 regola 8].
5. **Correzione degli errori** [non verificato: proposta]:
   - la finestra L2;
   - «Annulla» per 7 giorni sulle scritture interne;
   - «Era sbagliato», che fa preparare all'agente una correzione e abbassa la classe;
   - «una volta sola» per ogni azione; una mail dall'esito incerto non si rimanda da sola [principio verificato: SPEC §4.8].
6. **Conformità minima:**
   - dichiarazione AI nei messaggi L2 e L3 e nelle telefonate di Andrea;
   - avviso di registrazione;
   - consenso e Registro delle opposizioni per Andrea;
   - una sola lista di soppressione;
   - regole sull'email B2B;
   - registro dei trattamenti e DPIA per registrazioni, Andrea e analisi delle vendite;
   - scadenze di conservazione;
   - DPA e richiesta di conservazione zero ad Anthropic;
   - formazione prevista dall'art. 4 dell'AI Act.

   [verificato: P §9.1 regole 1-9, §14; R16 §6]

### 4.2 Cosa si toglie rispetto al disegno attuale

| Oggi | In P-B | Fonte di oggi |
|---|---|---|
| Chiave FIDO2 come secondo passo sulle carte | tolta; le chiavi restano per l'accesso a M365, come spesa del board | P §5.4; D03 §4.1 |
| Codice monouso per ogni consegna e impronta calcolata dalla Porta | l'esecutore invia il testo salvato, che non si può più cambiare | SPEC §4.7 |
| Richieste HMAC con numero monouso | un token per servizio nella rete interna | SPEC §3 |
| Registro a catena con MAC e ancora esterna | tabella a sola aggiunta | SPEC §4.9 |
| Un solo effetto per giro | più scritture interne in una sola proposta | SPEC §2.1 |
| Elenco chiuso nel codice delle scritture interne | configurazione con i livelli | SPEC §4.6 |
| «Sempre» con 20 sì per destinazione e scadenza a 30 giorni | regole di promozione per classe (§3.1) | P §5.4 |
| Sei istanze Hermes, una per confine di fiducia | tre contenitori, divisi per affidabilità | R34-2 §3.3 |
| Revisione esterna come condizione per i dati dei clienti (3.560-5.940 €) | facoltativa | P §14, decisione 5 |
| Plugin `pre_tool_call` come difesa principale | non serve: gli agenti non hanno strumenti che inviano. Inoltre nella v0.23 un gateway senza nessuno davanti salta un hook di shell non approvato | R34-2 §5.4; GH-REL v0.23.0 |
| Corsia separata per il testo di terzi come cancello | resta solo come buona pratica nello smistamento della posta | SPEC §4.4 |

Le regole del board di Michele non sono controlli del progetto e restano: VLAN, patch entro 14 giorni, dati rossi salvati solo dopo F3, backup 3-2-1 [verificato: R36 §4.5, §7.1; P §11]. A Michele chiediamo dove si possono allentare.

### 4.3 Cosa dipende dal parere legale

Il parere costa al massimo 2.500 €; i punti del pilota arrivano entro la settimana 3 [verificato: P §9.4, §14].

| Tema | Effetto sui livelli | Fonte |
|---|---|---|
| Email B2B verso l'Italia: il Garante chiede il consenso anche per i contatti aziendali | i primi contatti restano a L1 o fermi | R16 §3 |
| Follow-up e recap a un cliente già incontrato: secondo R16 non è marketing a freddo | decide se B1 e B3 possono arrivare a L3 | R16 §3 punto 2 (proposta di quel rapporto) |
| Se un messaggio L2, che una persona poteva fermare, vale come approvato | decide se in L2 serve la dichiarazione AI | domanda nuova [non verificato] |
| Registrazione delle call; art. 4 dello Statuto se ci sono dipendenti | J5, A1, C2 | P §9.4; R16 §1 |
| Confine fra coaching e valutazione dei lavoratori | G3, G4, K12 | R16 §4, §7 |
| Andrea: consenso nel modulo (art. 130), voce, Registro delle opposizioni | G5, G6, K10 | R16 §2; R31 §9 |
| Dati verso gli USA e Claude Team | dati rossi, K4 | P §5.6, §9.4 |
| Firma elettronica, via per LinkedIn, metadati di M365 | L1, L8, D2, F1 | P §9.4; R16 «Sintesi» punto 4 |
| Hermes Cloud, se lo si usa | senza DPA solo dati verdi | R18 §2.4 |

Se il parere chiude una porta, la funzione resta e la sua classe rimane a L1.

---

## 5. Fasi

### 5.1 Il piano

| Fase | Settimane | Board | Cosa si costruisce | gp di base [non verificato: stima mia su R36 §7.3 e R34-2 §8.2] |
|---|---|---|---|---|
| 0 | 1-4 | F0-F1 | come nella v2.1: Claude Team, email, SersanOutreach, registro dei trattamenti e DPIA. In più: prova di Hermes sulla macchina di sviluppo con il modello a copione; prima parte del Cancello semplice | circa 19 |
| 1 | 5-8 | F1-F2 | stage in LAB: un contenitore Hermes con 5 profili (Post-call, Analista chiamate, Report del mattino, Capo di gabinetto, Agente task) e il bot Teams; Cancello v1 con livelli, finestra e «Annulla»; carte in Teams; esecutori per Outlook, canale interno e Jira; trascrizioni da Graph | circa 24-26 |
| 2 | 9-21 | F2-F4 | Hermes sul server con LiteLLM; tre contenitori, «passa», specchio «Agenti»; regole di promozione; esecutori per calendario, SersanOutreach (nota e deal) e pausa di Instantly; Telegram per avvisi, «Ferma» e approvazioni; BookStack, MCP memoria, Jira; 11 agenti | circa 38-42 |
| 3 | 22-35 | F4 | memoria con i dati dei clienti; Vexa e trascrizione in casa; brief, slide, proposte, agenda, posta; WhatsApp e Slack tramite Cancello e n8n; linea di riserva; 18 agenti | circa 55-57 |
| 4 | 36-40 | F4-F5 | Postiz e listmonk; skill verso i clienti in L2; Buzz in LAB con Hermes; 10 agenti | circa 23-24 |
| 5 | 41-48 | F5 | Andrea in casa (oppure prima, in cloud, se ci sono lead); coach, pipeline, clienti simili | circa 38 |
| 6 | 49-53 | F5 | DocuSeal, fatturazione, assistenti personali in Hermes, Paperclip in LAB; 11 agenti | circa 24 |
| **Totale** | **1-53** | | | **circa 221-230**; circa 295-307 con la riserva di un terzo; più circa 35-45 gp di esercizio |

Per confronto, la v2.1 vale 249,25 gp di base e 29 gp di esercizio [verificato: R36 §7.2]. P-B costruisce un po' meno e mantiene di più, perché Hermes chiede 1,5-2,5 gp al mese [verificato: R27 §8, stima]. Il calendario resta di circa 50-53 settimane: il guadagno è che l'autonomia arriva prima [non verificato: deduzione].

### 5.2 Cosa è autonomo a che punto

[non verificato: proposta]

- **Settimana 8** (stage, dati verdi e gialli):
  - L3: riassunto interno dopo la call, registro dei meeting, to-do in Jira con «Annulla», debrief, passaggi fra i 5 profili;
  - L2: classe pronta per il follow-up ai clienti con call registrata, da accendere con le prime approvazioni senza modifiche;
  - L1: tutto il resto verso l'esterno.
- **Settimana 21** (server, 14 agenti):
  - L3: CRM (meeting e deal), calendario, passaggi fra squadre, ricerche e bozze del marketing, chiusura delle card degli agenti, skill interne;
  - L2: follow-up e recap ai clienti noti, chiusura dei to-do delle persone, inviti per la seconda call a contatti noti;
  - L1: primi contatti, offerte, LinkedIn, post.
- **A regime:**
  - L3: post-call completo per i clienti con relazione attiva, brief, Andrea, coaching a chi ha fatto la call, apprendimento interno;
  - L2: primo incontro, newsletter, post della pagina aziendale, aperture di Andrea finché non entrano nella banca di frasi;
  - L1: offerte con prezzi nuovi, contratti, fatture, primi contatti a freddo, codice, agenti nuovi;
  - L0: pagamenti, cancellazioni, credenziali, profili dei founder.

### 5.3 Cosa cambia rispetto alla v2.1

- **Motore.** Hermes al posto del runner sull'Agent SDK. L'ADR-0012 si rovescia: il motore sull'SDK diventa l'uscita.
- **Ingressi.** Eventi e orari dalla fase 1. Oggi, nella milestone 1, i lavori partono da un comando dato a mano [verificato: SPEC §3, §5].
- **Passaggi fra agenti.** Dalla fase 1, con la kanban pronta. La bacheca da scrivere arriva nella fase 2 [verificato: P §11].
- **Livelli.** L2 e L3 con «Annulla» dalla fase 1. Oggi non c'è una L2 [verificato: SPEC §4.5].
- **Esecutori interni.** Jira e canale interno dalla fase 1 invece che dalla 2 [verificato: PRD «Fuori»]. Telegram dalla fase 2 invece che dalla 3 [verificato: P §11].
- **Regole.** Regole di promozione al posto delle «Sempre».
- **Continuità.** Linea di riserva nella fase 3 invece che prima della fase 5 [verificato: P §14, decisione 13].
- **Controlli tolti.** Niente FIDO2 sulle carte, niente revisione esterna obbligatoria.
- **Bot.** Un solo bot Hermes. I nove bot di squadra diventano messaggi firmati con il nome dell'agente nei canali di squadra; tornano quando MSG-43 sarà chiuso [non verificato: proposta].

### 5.4 Le verifiche delle settimane 8 e 21

Criteri tecnici [non verificato: proposta, sul modello di P §11 e R34-2 §10.3]:
1. In due settimane, con almeno 5 profili e due ingressi automatici, nessun messaggio o risultato finisce al profilo, alla chat o al cliente sbagliato, e nessuna card sparisce.
2. Nessuna azione è uscita a un livello più alto di quello della sua classe; i 10 scenari passano.
3. Ogni «Ferma» ha fermato davvero; nessuna azione L2 è partita prima del tempo.
4. «Annulla» riporta lo stato di prima.
5. La spesa resta nel tetto, con al massimo il 10% di scarto fra Hermes, LiteLLM e Console.
6. Un aggiornamento di Hermes passa i 10 scenari sullo stage nel termine di Michele.
7. Sullo stage non resta salvato nessun dato rosso.

Ai criteri commerciali della v2.1 [verificato: P §11] si aggiungono due misure: il tempo mediano fra la fine della call e il follow-up uscito, e la quota di passi del post-call fatti senza mani.

Se il criterio 1 fallisce, ci sono due settimane per correggere. Se il problema è di struttura, si passa all'uscita A (§8). Alla settimana 21 valgono gli stessi criteri sul server, più il backup 3-2-1 e la decisione sulla RAM [verificato: P §11].

---

## 6. Costi

### 6.1 Al mese, in più rispetto a oggi

La licenza di Hermes costa 0 €. La v2.1 scrive già che Hermes e l'SDK costano uguale [verificato: R27 §2.1; P §12.1]. Le cifre sono quindi quelle della v2.1:

| Periodo | € al mese in più |
|---|---|
| Fasi 0-1, con Azure ancora acceso | circa 135 |
| Fase 2, con Azure spento | da circa -15 a +20 |
| Fasi 3-4 | da circa -1 a +70, più 10-11 della linea di riserva anticipata |
| Fasi 5-6 | da circa 46 a 168 |
| Listino a regime | circa 479-583 |

[verificato: P §12.1, salvo la linea anticipata, che è una proposta]

- **API.** La stima è di circa 196 € al mese (forbice 90-250), con un tetto a 250 [verificato: P §12.1, §14 decisione 3].
- **Più autonomia vuol dire più lavori automatici**, quindi la spesa va misurata nella fase 1.
- **Cache.** Funziona solo se il nome del modello in LiteLLM contiene «claude» [verificato: R27 §3.1]. Nella v0.23 i cron condividono la chiave della cache e le esecuzioni singole mandano circa 1.570 token in meno [verificato: GH-REL v0.23.0].

### 6.2 Una tantum

- **Oggi:** come nella v2.1, circa 2.900-3.890 €, più 140-550 € per le batterie dell'UPS se servono [verificato: P §1, §12.2].
- **Più avanti:**

| Voce | € | Fonte |
|---|---|---|
| RAM | 690-830 | [verificato: P §12.2] |
| Seconda GPU | 880-1.220 | [verificato: P §12.2] |
| Linea di riserva | 77-200 | [verificato: P §12.2] |
| Vivavoce da sala | 100-250 | [verificato: P §12.2] |
| Attivazione della linea di Andrea | 7-14 | [verificato: P §12.2] |
| Backup del board | secondo il board | [verificato: P §12.2] |
| Revisione esterna | 3.560-5.940 € non più obbligatori in P-B | [verificato per l'importo: P §12.2] |

### 6.3 Abbonamenti facoltativi per avere più autonomia

| Abbonamento | A cosa serve | Costo | Fonte |
|---|---|---|---|
| Linea internet di riserva 4G/5G | gli agenti e Andrea non si fermano se cade la fibra | 10-11 € al mese, più 77-200 € una volta | [verificato: P §14, decisione 13] |
| Hermes Cloud | routine su dati verdi anche a server spento | circa 33-47 € al mese per istanza | [non verificato: prezzi di terzi, R18 §2.4] |
| Voce in cloud per anticipare Andrea | Andrea dalla fase 3, se ci sono lead | circa 170 € al mese con ElevenLabs; la voce dei lead andrebbe negli USA | [verificato: R31 §12; R16 «Sintesi» punto 9] |
| Prova di Grok Bot su dati pubblici | confronto alla pari sulle routine di marketing | circa 54 € una volta | [verificato: P §14, decisione 23] |

Hermes sa importare gli utenti di Grok Bot con `hermes migrate` [verificato: GH-REL v0.22.6].

### 6.4 Giorni di sviluppo

| | v2.1 | P-B |
|---|---|---|
| Fasi 0-1 | 40,5 gp di base, circa 54 con la riserva [verificato: R36 §7.2] | circa 43-45 di base, circa 57-60 con la riserva [non verificato: stima] |
| Totale | 249,25 di base [verificato: R36 §7.2] | circa 221-230 di base [non verificato: stima] |
| Esercizio | 29 [verificato: R36 §7.2] | circa 35-45 [non verificato: stima] |

Le fasi 0-1 di P-B costano qualche giorno in più perché anticipano esecutori e livelli. Con 6,5 gp a settimana [verificato: R36 §7.1] la base ci sta, la riserva in parte no.

---

## 7. Cosa cambia, in concreto, nella milestone 1

**Resta uguale** [verificato: SPEC §1, §2.2, §7.5]:
- il Cancello unico esecutore;
- le macchine di sviluppo con dati di prova verdi;
- la Porta di prova da terminale;
- il modello a copione.

Il modello a copione si usa anche con Hermes. Basta un fornitore con nome in `anthropic_messages` che punta al servizio di prova, con `context_length` di almeno 64.000 [verificato: R27 §2.4, §3.1].

**Si sostituisce:**
- coda dei lavori, runner dell'SDK, hook `PreToolUse` e ripresa delle sessioni (§4.2, §4.3, §4.5, §4.11) lasciano il posto a:
  - kanban e cron di Hermes;
  - un MCP `sersan` con `propose_action`;
  - una card che si blocca in attesa e che il Cancello sblocca con l'esito via webhook [non verificato: da provare].
- In L3 e L2 l'agente non aspetta: riceve «eseguita» oppure «parte alle HH:MM».

**Si semplifica:** come nella tabella del §4.2.
- Le condizioni per una decisione valida passano da sette a quattro: carta in attesa, carta non scaduta, approvatore della classe, stop non premuto.

**Si aggiunge:**
- livelli per classe e gruppo di destinatari;
- timer della finestra con «Ferma», «Modifica» e «Invia ora»;
- «Annulla»;
- discesa automatica dei livelli;
- ore d'invio.

**I criteri passano da 27 a 16:**

| Criteri | Cosa ne fa P-B |
|---|---|
| AC-001, 002, 003, 007, 008, 011, 015, 017, 025 | restano, adattati |
| AC-010 e 026 | diventano un criterio solo |
| AC-021 | diventa: con la chiave al limite, il lavoro si ferma senza effetti |
| AC-018, 020, 024, 027 | diventano un criterio solo su Hermes: tre profili e ingressi in parallelo senza scambi; una card in attesa per una notte riparte con l'esito giusto; un aggiornamento di Hermes passa i 10 scenari |
| AC-004, 005, 006, 009, 012, 013, 014, 016, 019, 022, 023 | tolti |
| Nuovi | L2 eseguita una volta a scadenza; «Ferma» e «Modifica»; «Annulla»; discesa dei livelli |

**Decisioni D1-D6:**
- D1 diventa scadenza per classe più durata delle finestre L2.
- D2, D3 e D4 restano come sono.
- D5: il Cancello resta in TypeScript; con Hermes non scriviamo codice Python, solo configurazione.
- D6 vale anche per Hermes.

**ADR e PRD:**
- un ADR nuovo prende il posto di ADR-0001;
- l'ADR-0012 si rovescia;
- ADR-0003 e ADR-0010 si correggono.
- Nel PRD la metrica «effetti usciti senza carta: 0» diventa «effetti usciti sopra il livello della loro classe: 0». Si aggiungono le misure di autonomia del §5.4.

**Giorni:** circa 9-10 gp, contro circa 13 della milestone sull'SDK [non verificato: stima mia; mappatura dei pezzi in SPEC §11 e gp in R36 §7.3].

---

## 8. Rischi principali e strade d'uscita

| Rischio | Effetto | Come lo gestiamo |
|---|---|---|
| Affidabilità di Hermes: 312 problemi, 83 risolti al 9/11; MSG-43, GW-41, KB-10 e HR-6 ancora aperti [verificato: GH-143547]; una persona racconta chat che si mescolano [verificato: T1] | un'azione L3 con il contesto sbagliato | un bot per gateway; clienti mai sugli adattatori di Hermes; destinatari controllati dal Cancello; L3 verso l'esterno solo dopo le verifiche |
| Ritmo dei rilasci: v0.22.6, v0.22.7 e v0.23.0 in quattro giorni (2-5/11); note delle patch «undocumented here on purpose» [verificato: GH-REL] | 1,5-2,5 gp al mese; patch entro 14 giorni per il board | digest fissato, stage, 10 scenari; chiedere a Michele un termine diverso per i contenitori non esposti |
| Identità per contenitore, non per persona [verificato: R27 §4] | chi parla col bot vede ciò che vede il contenitore | in quattro, in un sistema chiuso, è accettabile; coaching e dati personali consegnati 1:1; domande personali via Claude Team |
| Errore autonomo verso un cliente | una mail partita non si ritira | finestra L2, testi con impegni sempre L1, dichiarazione AI, discesa automatica, correzione |
| Parere restrittivo | alcune classi restano a L1 | le funzioni restano; si decide classe per classe |
| Pochi volumi [verificato: P §7.1] | le soglie si raggiungono tardi | contano anche le call con i clienti già attivi |
| Bug noti di Hermes: Teams non manda documenti (#113578, aperto [verificato: GH-113578]); WhatsApp non manda i modelli [verificato: R27 §5] | file e messaggi oltre le 24 ore | li manda l'esecutore del Cancello |
| Una sola linea, server da riaccendere a distanza [verificato: P §13; DOM 22] | niente lavoro 24/7 | linea di riserva nella fase 3; riaccensione automatica decisa da Michele; politica dei turni persi del cron |
| Nessuno conosce Hermes a fondo [verificato: R34-2 §10.1] | errori di configurazione | pilota con un contenitore; Mattia co-manutentore |

**Strade d'uscita:**

| Uscita | Quando | Cosa resta | Costo |
|---|---|---|---|
| **A.** Il motore sull'Agent SDK della v2.1 prende il posto di Hermes | fallisce il criterio 1 della verifica | Cancello con i livelli, esecutori, skill nello stesso formato `SKILL.md`, memoria, call, Andrea | 17,5-21 gp di base, 3-4 settimane [verificato: R34-2 §10.2] |
| **B.** Hermes solo per i canali o per il marketing su dati verdi | i profili reggono male | tutto il resto | 12-15 gp [verificato: R34-2 §10.2] |
| **C.** Hermes solo come pilota in LAB | i problemi restano aperti | tutto il resto | 6-8 gp [verificato: R27 §10] |
| **D.** Hermes Cloud | arriva un DPA da Nous | Hermes senza manutenzione nostra | abbonamento, §6.3 |
| **E.** Ogni classe torna a L1 con un tocco | serve fermare l'autonomia senza cambiare architettura | il sistema funziona come la v2.1 | 0 |

---

## 9. Funzioni: nessuna si toglie

Tutte le righe sono una proposta [non verificato]. I costi vengono dalle fonti indicate.

| Voce | Componente in P-B e fase | Livello a regime | Cosa manca e quanto costa |
|---|---|---|---|
| J1 Un solo sistema | Hermes, Cancello, memoria; fasi 1-6 | interno L3, esterno per classe | nulla |
| J2 Squadre con responsabile | profili Hermes e registro nel Cancello; fasi 1-2 | agente nuovo L1 | riga nel registro dei trattamenti [P §4.12] |
| J3 Outreach con agente email | profili Outbound; fase 3 | primi contatti L1; risposte a contatti noti L2-L3; LinkedIn L1; invii in blocco L0 | parere sull'email [P §14, decisione 2] |
| J4 Email → proposte → chiamate | kanban del contenitore commerciale; fase 3 | L3 | nulla |
| J5 Agente in ogni call | Teams nativo, Vexa, telefono; fasi 1-3 | L3 sulle nostre call; il cliente deve ammettere il bot | Vexa, 12 GB; vivavoce 100-250 € [P §12.2] |
| J6 Brief e slide | Agente brief e Agente slide; fasi 2-3 | L3 interno; L2 al cliente | template SerSan; DPIA |
| J7 Marketing | squadre Marketing e Studio; fasi 2-4 | L3 interno; pagina L2; founder L0 | Postiz in fase 4, Metricool come ponte (59,86 €/mese) [R34-2 §9.2] |
| J8 Progetti | Jira; fasi 1-4 | to-do L3; report al cliente L2; PR L1 | Jira Standard 28 €/mese [P §14] |
| J9 Chat di gruppo | Teams (bot Hermes), Telegram, WhatsApp e Slack tramite Cancello, Buzz in LAB; fasi 1-4 | come per classe | WhatsApp 7-12 €/mese; Slack 0-27 €/mese [P §14] |
| A1 Riunioni registrate | come J5; fasi 1-3 | L3 | parere, DPIA |
| A2 Memoria relazionale | BookStack e PostgreSQL; fase 2 | lettura L3; pagine ufficiali L2 | MariaDB, 1 GB |
| A3 Memoria vettoriale | Qdrant con MCP RAG; fase 3 | L3 | dati dei clienti dopo la settimana 21 |
| A4 Orchestratore sul server | Hermes self-hosted; fasi 1-2 | — | posto agenti o stage [DOM 2] |
| A5 Agenti per ruolo | raccolta, pulizia, indicizzazione; fase 3 | L3 | le scadenze le applica un lavoro fisso, non un agente |
| A6 Agenti che imparano | skill curate da Hermes, con lock; fase 2 | interne L3; verso i clienti L2; legali L0 | nulla |
| A7 Chat fra agenti | kanban, «passa», specchio «Agenti», scambio del venerdì; fasi 1-2 | L3 | servizio «passa», 3 gp |
| B1 Punti nel canale del cliente | Post-call e Cancello; fasi 1-2 | L3 clienti noti; L2 primo incontro | prova dei canali condivisi |
| B2 Opportunità nel CRM | esecutore SersanOutreach; fase 2 | L3 | «crea deal», 3,5 gp [R36 §7.3] |
| B3 Mail di follow-up | Post-call ed esecutore Outlook; fase 1 | L3 clienti noti; L2 primo incontro | parere |
| B4 To-do al team | esecutore Jira; fase 1 | L3 con «Annulla» | 1,75 gp |
| B5 Autonomia crescente | regole di promozione; fase 2 | — | circa 1,5 gp |
| C1 Debrief | n8n e Report del mattino; fase 1 | L3 | nulla |
| C2 Agente anche per chi manca | `recordAutomatically` e Vexa; fasi 1-3 | L3 nel tentativo | da provare [R30 §3.6] |
| C3, C5 Analisi e registro dei meeting | Analista chiamate; fasi 1-2 | L3 | nulla |
| C4 Dettatura | app Claude e trascrizione | non si applica | nulla |
| C6 Regole di ciascuno | pagine «Come lavoro»; fase 2 | lettura L3; modifiche le fa la persona | nulla |
| D1 Pipeline pesata | Pipeline; fase 5 | L3 | storico di 30-50 chiusure |
| D2, D3 Brief e storico | Agente brief; fase 3 | L3 | Apollo 43,78 €/mese; parere su LinkedIn |
| D4 Slide | Agente slide; fase 3 | L3; L2 al cliente | template |
| D5 Offerta | Agente proposte; fase 3 | bozza L3; invio L1 | nulla |
| E1, E2 Tempo e token; E4 Formazione | piano e formazione | non si applica | E4 è un obbligo (art. 4 AI Act) |
| E3 Banca dei token | LiteLLM e tetti di Hermes; fasi 1-2 | L3 | nulla |
| F1 Metadati del lavoro | Mappatore, solo dati aggregati; fase 4 | L3 | parere; API di M365 da scegliere |
| F2 Interviste | l'Intervistatore conduce l'intervista; fase 4 | L3 | nulla |
| F3, F4 Mappa e ore | Mappatore; fase 4 | analisi L3; consigli alla persona L0 | nulla |
| F5 AI per tutti | Claude Team e bot Hermes; fase 0 | — | nulla |
| G1, G2 Canale delle call e fit score | Post-call e qualificatore; fasi 3-5 | L3 | volumi di call |
| G3, G4, K12 Coaching | Coach vendite; fase 5 | L3 a chi ha fatto la call; aggregati al responsabile | parere |
| G5, K10 Andrea | Asterisk e Pipecat; fase 5 | L3 | operatore 44-90 €/mese; seconda GPU; linea di riserva [P §14] |
| G6 Andrea impara | aperture e A/B; fase 5 | L2, poi L3 nella banca di frasi | nulla |
| G7, G8 Risultati; vinti e persi | debrief e Analista vinto/perso; fasi 3-5 | L3 | volumi |
| G9 Fino a cento agenti | registro e contenitori; fasi 2-6 | agente nuovo L1 | RAM come al §2.4 |
| G10 Superpotere | è il risultato dell'insieme | non si applica | nulla |
| H1-H7 Adozione | piano delle persone; H5: routine e skill create in chat con Hermes; fasi 0-6 | non si applica | premio 50-100 €/mese [P §14] |
| I1-I2 Contesto e qualità | coperti da A1-A3 | non si applica | nulla |
| I3 Aree senza AI | classi L0 nel Cancello; fase 1 | L0 | nulla |
| I4 Marketing più creativo | come J7 | come J7 | come J7 |
| K1 Debrief in calendario | esecutore Outlook; fase 2 | L3 | nulla |
| K2 «Tre nuove call» | Raccoglitore e Agenda; fase 3 | annuncio L3; inviti L2, poi L3 per contatti noti | nulla |
| K3 Posta | Smistatore posta; fase 3 | smistamento L3; risposte L1, poi L2-L3 per contatti noti | accordo di ciascuno sulla propria casella |
| K4 Cosa si è detto in una call | Claude Team con MCP RAG; fase 3 | L3 | parere sui dati rossi |
| K5 Intake e onboarding | Agente intake; fase 3 | brief L3; messaggi L2 | nulla |
| K6, K7 Slide e nostro stile | Agente slide e template; fasi 0-3 | L3; L2 al cliente | template |
| K8 Portale clienti | SersanOutreach; fase 5 | L3 | nulla |
| K9 Newsletter | listmonk; fase 4 | L1, poi L2 | relay SMTP, meno di 1 €/mese [P §14] |
| K11 Perché si chiude | Analista vinto/perso; fasi 3-5 | analisi L3; primi contatti L1 | volumi |
| K13 Mappa per i clienti | Mappatore e Intervistatore | L0 | va progettata un'istanza separata per cliente [non verificato: giorni non stimati] |
| K14 Finanza nella memoria | n8n da Sirius; fasi 3-6 | L3 | sapere cos'è Sirius [DOM 25] |
| K15 Acquisti | Agente acquisti; fase 6 | registrazione L3; pagamenti L0 | nulla |
| K16 Assistente personale | Hermes personale; fase 6 | verso terzi L1, poi L2; salute mai nella memoria aziendale | account personale 15-18 €/mese [P §14] |
| L1 Contratti | DocuSeal; fase 6 | bozza L3; invio L1 | parere sulla firma |
| L2 Fatture e solleciti | Agente fatture; fase 6 | invio L1; primi solleciti L2 su decisione dei CEO | strumento di fatturazione [P §14, decisione 22] |
| L3, L12 Margini e Allenatore | fase 6 | L3 | export di Sirius |
| L4 Bandi | pipeline del board; fase 3 | L3; la domanda la fa una persona (L0) | nulla |
| L5 Assistenza clienti | fase 6 | risposte L1, poi L2-L3 sulle domande ricorrenti | prova dei canali condivisi |
| L6 Rinnovi | fase 6 | segnali L3; proposte L1, rinnovi a listino L2 | decisione dei CEO |
| L7 Casi studio | fase 6 | bozza L3; testimonianza L2 | nulla |
| L8 Commenti della pagina | Community manager; fase 4 | L1, poi L2; founder L0 | accesso API alla pagina LinkedIn |
| L9 Sito e SEO | fase 6 | PR L1 | nulla |
| L10 Webinar ed eventi | fase 6 | iscrizioni e promemoria L3; inviti L2 | licenza webinar di Teams |
| L11 Sorveglianza del server | Sistemista; fase 3 | lettura L3; patch L1 | nulla |

Le voci sono 90, tutte presenti. Due processi della trascrizione non hanno una voce: gli eventi e la formazione, rifatti con l'AI [verificato: Rapporto 1 §3]. Restano coperti da H5, con routine e skill create in chat, e in parte da L10.
