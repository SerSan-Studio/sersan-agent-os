# 22 · L'architettura scelta per SerSan Agent OS

**Data:** 24/10/2026. **Per:** Alessandro Serratt e Michele Sanna, preparato per Alberto Tuveri.
**Fonti:** rapporti 00-01 e 05-18, proposte 20-A…G, giudizi 21 (visione, CEO, CPTO, compliance); tutti i file richiesti esistono.
**Etichette:** [verificato: 10 §5] = fatto letto nel file e nella sezione indicati; [non verificato] = stima, proposta o voce di terzi. Prezzi IVA esclusa, 1 $ = 0,8934 € [verificato: 14]. gp = giorni-persona.

---

## 1. La decisione in una pagina

**Cosa costruiamo.** Il secondo cervello aziendale della visione di Alberto, sul nostro server, con Hermes Agent come orchestratore: open source con licenza MIT [verificato: 10 §1]. Gli agenti lavorano con Claude via chiave API, leggono la memoria aziendale (Notion per le regole, un database in casa per call, mail e documenti) e parlano con noi in Slack. Tutto si regge su una regola: **gli agenti preparano, una persona approva, un nostro programma esegue**. Quel programma è il **Cancello**. È l'unico pezzo che può mandare una mail, scrivere al cliente, toccare il CRM o telefonare, e registra tutto.

**Perché questa.** Ha vinto in tre lenti su quattro (visione, CEO, CPTO) e nella somma. Nella somma delle quattro lenti, su 240 punti: A Hermes 159, F Paperclip 148,5, G ibrido 143,5, B buzz 140,5, E Claude-native 140, C Grok Bot 113, D Dots 105 [verificato: file 21; somma ricalcolata da me, perché i totali ricevuti chiamavano la stessa proposta in modi diversi]. I motivi:
- profili, bacheca dei compiti, cron e collegamento a Slack sono già fatti [verificato: 10 §4.1-4.2];
- dati e memoria restano sul nostro server;
- se Hermes delude si cambia solo l'orchestratore: Cancello, memoria e ingressi restano.

**Cosa cambia rispetto alla proposta A originale, dopo i giudizi.**
1. **Prima il funnel.** SersanOutreach ha 11 lead, 0 meeting e 0 vinti; l'email è ferma per la compliance; i founder non hanno pubblicato post [verificato: 01 §0, 05 §0]. Il valore arriva subito da ciò che è già pagato (Claude Team, Claude Tag, MCP di SersanOutreach) e dal marketing. Andrea e la pipeline pesata partono solo con dati veri.
2. **Tempi onesti.** Il Cancello vale circa 21 gp, non 5 [non verificato: stima di 20-E §6, confermata dal CPTO]. Su tutto il piano si aggiunge una riserva del 30 %. Il primo rilascio utile cade alla settimana 6-7.
3. **Decisione alla settimana 8, con criteri misurabili.** Basta che una conversazione finisca al profilo sbagliato (il bug noto di Hermes [verificato: 10 §6]) per passare a un motore nostro sull'Agent SDK di Claude: 10-15 gp [non verificato], senza buttare altro.
4. **Organigramma e banca dei token visibili ai CEO dalla fase 1.** Paperclip si prova solo oltre i 25 agenti.
5. **Tre colori dei dati** (verde, giallo, rosso) decidono che cosa può uscire dal server e verso chi.

**Cosa abbiamo scartato.**
- **Grok Bot**: computer negli USA, beta con cinque incidenti in una settimana, modello invisibile, nessuna esportazione [verificato: 11 §1, §7]; vietato per i dati dei lead (16 §6 regola 7).
- **OpenAI Dots**: un agente per persona, nel Regno Unito solo con Business Premium, crediti a prezzo ignoto, prodotto di un mese [verificato: 18 §2.2].
- **buzz** come chat di tutti: pre-1.0, approvazioni che falliscono, nessun freno ai giri [verificato: 17 §0]. Resta un pilota interno.
- **Paperclip** come base: governance senza cervello, sei advisory critici nel 2026 [non verificato: 20-F §5]. Resta l'innesto oltre i 25 agenti.
- **Claude-native puro (E)**: 119 gp, agenti che si parlano alla settimana 13. Resta l'uscita prezzata.
- **Ibrido (G)**: cinque componenti open source e otto servizi per un amministratore. Ne prendiamo le idee.

**Cosa chiediamo oggi.** Il via alle fasi 0-1 (8 settimane, circa 53 gp) e i piccoli abbonamenti del §9. Il resto si decide alla settimana 8, sui numeri.

---

## 2. Lo schema a blocchi

```
PERSONE (4) ── Slack Pro: DM, #approvazioni, #agenti, #ingresso, #call-vendita, #cliente-x (Slack Connect)
            ── Claude Team: chat, Claude Code, Claude Tag in Slack (solo dati verdi)
            ── Telegram: solo l'avviso «carta in attesa», mai il testo
                 ▲ Slack in Socket Mode: connessioni solo in uscita, nessuna porta aperta
═════════ SERVER DL380 · Proxmox VE 9 · dietro OPNsense e Cloudflare Tunnel ═════════
VM agenti  HERMES (versione fissata): profili con nome, bacheca, cron, un processo per card,
           browser spento, nessuno strumento che invia
           CANCELLO (TypeScript): registro degli agenti · policy · carte
           · outbox · audit a catena di hash · ESTOP · banca dei token · porta dei modelli
           (chiave, conteggio, tetto, colore dei dati) · freno ai giri · ESECUTORI, unici
           con effetti: Gmail, Slack, Notion, SersanOutreach, ElevenLabs
           CORSIA D'INGRESSO: webhook firmati → estrazione a schema senza strumenti
VM dati    Postgres 17 + pgvector: cervello (meeting, mail, documenti, eventi), Langfuse
VM gpu     RTX 4000 da 8 GB: embedding Qwen3-0.6B, giudice Qwen3-4B, faster-whisper
VM app     SersanOutreach (8 servizi), Traefik, cloudflared
VM stage   prove degli aggiornamenti; in fase 5 i piloti di Paperclip e buzz
VM monitor Prometheus, Grafana, Loki; Proxmox Backup Server con copia fuori sede
══════════════════════════════════════════════════════════════════════════════
IN ABBONAMENTO: API Anthropic (una chiave per famiglia di agenti) · Recall.ai · ElevenLabs
                + Twilio IT · Notion · Slack · Metricool · moda.app · gli strumenti di
                SersanOutreach (Instantly, Apollo, Apify, Perplexity)
RISERVE: Hermes Cloud (Londra, solo dati verdi) · VM Azure se l'hardware tarda
         · Claude su Bedrock UE se un cliente chiede la residenza dei dati in UE
```

**Come si parlano.**
- **Ingresso.** Recall.ai, il modulo del sito e Instantly chiamano webhook firmati via tunnel; la corsia d'ingresso verifica firma e anti-replay, poi un modello senza strumenti estrae i campi a schema JSON.
- **Due classi di lavoro.** Riassunti, estrazioni e classificazioni sono chiamate dirette alla Messages API; Hermes fa solo i lavori a più passi (recap, brief, offerte, deck).
- **Effetti.** Hermes chiama `propose_action`. Il Cancello risponde «consentito», «chiedi» o «negato». Se chiede, nasce una carta in `#approvazioni`. Dopo il sì di una persona autenticata l'esecutore agisce una volta sola.
- **Memoria e CRM.** Gli MCP di SersanOutreach girano come processi figli sullo stesso server: lettura libera per i profili commerciali, scritture solo tramite gli esecutori [verificato: 01 §5.1-5.2, §5.10].
- **Modelli.** Ogni chiamata passa dalla porta dei modelli, che aggiunge la chiave, conta e ferma al tetto. Che Hermes accetti un indirizzo Anthropic diverso va provato [non verificato]; in alternativa si usa una chiave per famiglia con limiti nella Console.

**I tre colori dei dati**, scritti nel codice del Cancello:
- **verde** (pubblico o interno non personale): va a qualunque fornitore ammesso, anche Claude Tag e Hermes Cloud;
- **giallo** (contatti di lavoro, campi del CRM, riassunti): solo verso fornitori con DPA e termini commerciali, mai verso servizi in beta o consumer;
- **rosso** (audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone, finanza): resta sul server, oppure va all'API Anthropic dopo l'oscuramento locale dei dati non necessari [verificato: 16 §6 regola 7; 13 §2.3].

---

## 3. Gli innesti presi dalle altre proposte

| Da | Innesto | Fase |
|---|---|---|
| E | Due classi di lavoro (Messages API e sessioni); porta dei modelli; approvatori per classe: Alessandro outbound e mail ai clienti, Michele offerte e affermazioni tecniche, Alberto infrastruttura e codice | 1 |
| E | Stima realistica del Cancello (≈21 gp) e conto API con sessioni e cache (≈195,65 € nel consigliato) | piano, §6 |
| B | Corsia `#ingresso`: chi legge testo di terzi non ha strumenti d'azione e passa avanti solo campi strutturati; approvazioni valide solo da un'identità umana, mai dalla chiave di un agente | 1 |
| B | Un bot Slack per agente con `allow_bots: "mentions"` [verificato: 10 §4.1]; freno: 8 messaggi per thread, catene di 3, tetto in $; buzz in pilota senza dati dei clienti | 3, 5 |
| F | Organigramma con responsabile, costo e tetto; ogni nuovo agente nasce da un'approvazione che porta la sua riga nel registro dei trattamenti e nella DPIA | 1, 3 |
| F | Coaching visibile solo all'interessato, con apertura d'emergenza registrata; Paperclip come piano di controllo oltre i 25 profili, con Hermes come adattatore e il Cancello come unico esecutore | 4, 5 |
| F | Bedrock UE per i dati rossi, se un cliente lo chiede; in alternativa la ZDR di Anthropic [verificato: 16 §5] | su richiesta |
| G | Riserva del 30 % sulle stime; pilota sulla VM Azure se l'hardware tarda; Slack Connect per il canale del cliente (su Pro: da verificare); un'istanza Hermes separata dove cambiano i permessi (finanza) | 0-3 |
| G | Hermes fuori dal percorso critico. **n8n non si prende**: lo stesso risultato lo dà la corsia d'ingresso, con un componente in meno e senza una licenza che vieta la rivendita [verificato: 12 §0 punto 6] | 1 |
| C | Tre colori dei dati come regola che i CEO capiscono, più severa di C: il giallo non va mai su servizi in beta | 1 |
| C, D | Valore nelle settimane 1-3 su dati verdi, con connettori in sola lettura (le routine scrivono senza chiedere [verificato: 18 §2.1]); Hermes Cloud come palestra | 0 |
| C, E, G | Riunioni fisiche registrate dal telefono, per chiudere A1 | 2 |
| D | Follow-up solo verso destinatari del dominio del cliente | 2 |
| A | Punto di decisione con criteri d'uscita dopo due settimane di prova | 1 |
| Tutte | Agenti editoriale, copy e metriche (Metricool in sola lettura) subito: con il funnel vuoto sono il primo valore [verificato: 05 §5] | 0-1 |
| Compliance | DPIA prima del primo post-call con un cliente; Cloudflare fra i sub-responsabili; prova di Vexa (Apache-2.0 [verificato: 12 §7]) | 0-2 |
| CEO | Precondizione D0 sull'email e mailbox live [verificato: 01 §6] | 0 |

---

## 4. Copertura A1-I4

| Voce | Componente | Fase |
|---|---|---|
| A1 Riunioni registrate e dichiarate | Recall.ai nelle call online, avviso nell'invito e a voce (il bot entra solo se l'evento è «avvisato»); riunioni fisiche dal telefono; trascrizione in casa; prova di Vexa | 1 online; 2 fisiche e Vexa |
| A2 Second brain relazionale | Notion Plus via MCP: regole, processi, obiettivi, catalogo | 1 |
| A3 Database vettoriale | pgvector; embedding e reranker Qwen3 0.6B sulla GPU; MCP «cervello» | 2 |
| A4 Orchestratore | Hermes fissato in VM; uscita prezzata verso l'Agent SDK | 1, decisione alla settimana 8 |
| A5 25 agenti per ruolo | Raccolta, pulizia e indicizzazione come lavori deterministici o su Haiku; azione su Sonnet e Opus | 1-3 |
| A6 Agenti che imparano | Skill `SKILL.md` scritte dall'agente; un revisore settimanale propone, una persona approva | 3 |
| A7 Chat condivisa | Bacheca di Hermes come registro; `#agenti` con un bot per agente; freno nel Cancello | 3 (`#ingresso` dalla 1) |
| B1 Recap nel canale del cliente | Canale interno subito; Slack Connect dopo la carta | 1 interno, 2 cliente |
| B2 Opportunità nel CRM | `record_meeting`, `update_deal` tramite l'esecutore | 2 |
| B3 Mail di follow-up | Bozza, poi carta ad Alessandro, poi l'esecutore Gmail invia (solo al dominio del cliente) | 1 bozza, 2 invio |
| B4 To-do | Notion, classe «scrittura interna» dai campi estratti | 1 |
| B5 Autonomia totale | Per gradi: tutto su carta; poi regole «Sempre» strette, create da una persona dopo 20 approvazioni senza modifiche; mai per offerte, primo contatto, pagamenti, cancellazioni | 5 |
| C1 Debrief del mattino | Cron per persona alle 7:00 in DM; numeri calcolati dal codice, frasi verificate | 1 |
| C2 Agente nelle call | Recall.ai al posto di chi manca | 1 |
| C3 Analisi con Claude | Estrazione a schema su Sonnet più profilo post-call | 1 |
| C4 Dettatura | Dettatura delle app Claude; note vocali Slack trascritte in casa | 0 app, 2 note |
| C5 Registro dei meeting | Tabella `meetings`: presenti, esito, pipeline emersa; vista in Notion | 2 |
| C6 Regole personali | Pagina Notion «Come lavoro», letta prima di ogni turno | 1 |
| D1 Pipeline pesata | Probabilità per stadio dagli eventi commerciali, con intervallo; pesi dichiarati fino a 30-50 chiusure | 4 |
| D2 Brief pre-meeting | Enrich di SersanOutreach, cervello, posta, ricerca web; arriva la sera prima | 2 |
| D3 Storico della relazione | Linea del tempo del cliente dentro il brief | 2 |
| D4 Slide del brief | moda.app via MCP o Claude Slides | 2 |
| D5 Offerta | Profilo su Opus: catalogo, trascrizione e brief, poi carta a Michele | 2 |
| E1-E2 Tempo e token | Argomenti dei §1 e §6 | — |
| E3 Banca dei token | Tetti per agente e per catena (avviso all'80 %, stop al 100 %); tetti per persona e report mensile | 1; 3 per persona |
| E4 Formazione | Un'ora documentata per i quattro (AI Act art. 4), aggiornata a ogni nuovo agente | 0 |
| F1 Metadati del Workspace | Job mensile solo su dati aggregati; dati individuali al massimo 21 giorni; suite di posta da confermare [verificato: 14 §5] | 3 |
| F2 Interviste | Profilo intervistatore in DM | 3 |
| F3-F4 Mappa e automazioni | Analista mensile su Opus: mappa, ore, costi, classifica | 3 |
| F5 AI per tutti | Slack come porta unica, Claude Team per tutti | 0 |
| G1 Canale call di vendita | `#call-vendita` alimentato dal post-call | 4 |
| G2 Fit score | Il qualificatore GP+BALD esteso alle call | 4 |
| G3-G4 Coaching | Report solo al venditore, aggregati al responsabile, niente emozioni; dopo il parere legale | 4 |
| G5 Andrea in 90 s | ElevenLabs Agents e numero Twilio italiano; il Cancello controlla consenso e Registro delle opposizioni; voce sintetica che si dichiara AI | 4 |
| G6 Impara dai rifiuti | Esiti analizzati ogni settimana; la nuova apertura parte con carta e prova A/B | 4 |
| G7 Risultati | Tempo di richiamata e meeting fissati nel debrief | 4 |
| G8 Perse al marketing | `lost_deal_analysis` e `review_feedback` passati all'agente editoriale | 2 |
| G9 100+ agenti in organigramma | Registro del Cancello esportato in Notion (responsabile, modello, tetto, costo); Paperclip in pilota oltre 25 | 1; 5 Paperclip |
| G10, H7 | Risultato dell'insieme; i rituali sotto | — |
| H1 Formarsi e sperimentare | Due ore a settimana di prova; template di agente | 0 |
| H2 Non delegabile | I CEO approvano le carte e leggono il debrief | 0-1 |
| H3 Assessment | Intervistatore per ruolo | 3 |
| H4 Ambassador | Mattia, con un tetto di token più alto | 3 |
| H5 Tutti costruiscono | Ognuno possiede almeno un agente | 3 |
| H6 Premio mensile | Classifica dal registro (agenti creati, ore stimate); decidono i CEO | 3 |
| I1-I2 Contesto | Coperti da A1-A3 | — |
| I3 Aree senza AI | Classi negate nel Cancello: voce e volto dei founder, loro DM e commenti, firma tecnica di Michele, lista dei 200 account, voti alle persone | 1 |
| I4 Marketing 70/30 | Editoriale, copy con lint e revisione avversaria, metriche; pubblica solo la sessione presidiata [verificato: 05 §5.4] | 0 via Claude Team, 1 profili |

**Lacune dichiarate.**
- D1 non ha storico: oggi ci sono 0 vinti e 91 deal senza valore [verificato: 01 §0].
- G5 nella versione fedele (la voce clonata di un collega) richiede un contratto separato e revocabile [verificato: 16 §6 regola 6].
- G4 al responsabile manda solo aggregati, finché non c'è il parere legale.

---

## 5. Piano a fasi

**Capacità assunta** [non verificato: da confermare]: Alberto 4,5 gp a settimana, Mattia 1,5, Michele 0,5, in tutto circa 6,5 gp a settimana. Le stime sono «base → con riserva del 30 %».

| Fase | Settimane | gp | Lavoro e chi lo fa | Dimostrazione che chiude la fase |
|---|---|---|---|---|
| **0 Fondamenta e valore subito** | 1-3 | 15 → 20 | **Alberto:** server secondo 15 §7 (inventario iLO, 8 moduli RAM bilanciati, kit GPU, Proxmox, ZFS, OPNsense, Tunnel, backup PBS e copia fuori sede); chiavi API per famiglia; profili e skill su Hermes Cloud con dati verdi. **Mattia:** debito di SersanOutreach (identità in `enforce`, MFA, backup fuori sede, alert provati fino a una persona) e runbook. **Michele:** registro dei trattamenti, inizio DPIA, verifica dei crediti nella Console. **Alessandro:** decisioni D0 sull'email con il legale, mailbox live, temi del marketing; usa Claude Tag ogni giorno | Ripristino di una VM dalla copia fuori sede davanti a Michele. SersanOutreach verde su identità, MFA e backup. Alessandro chiede a @Claude in Slack «cosa prepariamo questa settimana?» e ottiene risposta su dati verdi. Prima settimana di post pronta |
| **1 Pilota: post-call, debrief, marketing** | 4-8 | 25,5 → 33 | **Alberto e Mattia:** Hermes fissato; Cancello v1 (nucleo 9 gp, ruoli 2, porta dei modelli 2, carte in Slack 4); corsia d'ingresso e Recall.ai; post-call; debrief; profili editoriale, copy e metriche; organigramma v0 in Notion. **Michele:** guida le due settimane di misura (7-8). **Alessandro:** approva le carte | Dopo una call con un cliente attuale (avvisato): recap nel canale interno, to-do in Notion, bozza della mail in carta. Debrief alle 7:00 per tutti. Numeri del lunedì da Metricool. Organigramma con costo per agente. **Decisione alla settimana 8:** zero conversazioni al profilo sbagliato, zero effetti fuori dal Cancello, un aggiornamento di Hermes che passa 10 scenari su stage, spesa dentro il tetto, carte decise entro 24 ore. Se un criterio fallisce, si passa al motore sull'Agent SDK |
| **2 Memoria, brief, offerte, migrazione** | 9-13 | 24 → 31 | **Mattia e Alberto:** SersanOutreach sul server con la checklist di 01 §4.11; MCP collegati; cervello pgvector; brief e slide; offerte; Cancello v2 (invio Gmail limitato al dominio del cliente, Slack Connect, avvisi Telegram); riunioni fisiche; prova di Vexa. **Michele:** firma le offerte. **Alessandro:** porta la DPIA dei clienti al legale | Brief la sera prima di ogni incontro; bozza d'offerta entro un'ora dalla call; «cosa ci siamo detti con X?» ha risposta; follow-up inviato dopo il sì di Alessandro; Azure spenta |
| **3 Chat fra agenti e organizzazione** | 14-16 | 12 → 16 | **Alberto:** un bot Slack per agente con il freno; banca dei token per persona; approvazione `hire_agent` legata al registro. **Mattia:** intervistatore, mappa dei processi, ambassador. **CEO:** premio mensile | In `#agenti` il raccoglitore annuncia «3 nuove call» e l'agente degli appuntamenti le prende; il freno si vede in azione. Organigramma con 15-25 agenti e costi. Mappa dei processi v0 |
| **4 Vendite e voce** (si apre solo con parere legale e lead reali) | 17-20 | 15 → 20 | **Alberto:** Andrea (consenso e Registro delle opposizioni nel Cancello); fit score; coaching privato; ciclo sui rifiuti; pipeline pesata con intervallo. **Alessandro:** testo del consenso nel modulo; numero italiano | Una lead di prova lasciata nel modulo viene richiamata entro 90 s. Andrea si dichiara AI e fissa un meeting con un commerciale; l'esito arriva in SersanOutreach. Il coaching lo vede solo il venditore |
| **5 Scala e rivendibilità** | 21-24 | 10 → 13 | **Alberto:** Paperclip su stage (VPN, modalità autenticata, telemetria spenta) e pilota di buzz interno. **Michele:** prime regole «Sempre». | Organigramma oltre i 25 agenti con stop al 100 % dimostrato. Decisione scritta su Paperclip e buzz. Prima regola «Sempre» attiva |

**Totale:** 101,5 gp di base, circa 133 gp con la riserva, in 24 settimane. Oggi si impegnano solo le fasi 0-1: **53 gp in 8 settimane**.

**Gate commerciale** (dal dissenso CEO). Se alla settimana 8 l'email non è live e i founder non pubblicano, si fanno le fasi 2-3, utili anche al funnel, e la 4 aspetta. Se l'hardware tarda, la fase 1 parte sulla VM Azure [non verificato].

---

## 6. Costi mensili (tre scenari)

**Formula.** Costo = fissi di 14 §11.1 ± righe cambiate + API + ore di riunione × 0,65 $ + minuti di voce × 0,0445 $ + LLM della voce, tutto × 0,8934. Esborso = costo − API coperte dai crediti (fino a 714,70 €) − 150 € quando si spegne la VM Azure.
Le API usano la stima di 20-E §7 con sessioni e cache: Σ lavori × (input × prezzo + letture dalla cache × 0,05 × prezzo + scritture in cache × 1,25 × prezzo + output × prezzo) + ricerche × 0,01 $. Al posto di «14 × 1,5».

| € al mese | Minimo | Consigliato | Completo |
|---|---|---|---|
| Fissi di 14 con il bundle Claude Team | 248,70 | 780,20 | 1.652,60 |
| − Fireflies (al suo posto Recall.ai) | 0 | −67,90 | −67,90 |
| − HubSpot (il CRM è SersanOutreach) | 0 | −26,80 | −160,81 |
| − Notion Business → Plus | 0 | −35,73 | 0 |
| + Nous Portal Plus e Hermes Cloud [verificato: 18 §2.4] | 0 | +18,67 (istanza ferma) | +47,08 (istanza Large) |
| + Claude Tag, tetto [verificato: 18 §2.1] | 0 | +44,67 (50 $) | +89,34 (100 $) |
| + Proxmox Community, 2 socket [verificato: 15 §8] | 0 | +20,00 | +20,00 |
| **Fissi** | **248,70** | **733,11** | **1.580,31** |
| API Anthropic [non verificato: 20-E §7] | 54,70 | 195,65 | 486,90 |
| Recall.ai (30 / 30 / 100 ore) | 17,42 | 17,42 | 58,07 |
| Voce: minuti e LLM [14 §11.2] | 0 | 41,63 | 146,07 |
| Proxy residenziali (non servono con l'estensione [verificato: 01 §4.5]) | 0 | 0 | 0 |
| **Totale di listino** | **320,82** | **987,81** | **2.271,35** |
| **Esborso oggi**, con bundle e crediti | **266,12** | **792,16** | **1.784,45** |
| … dopo lo spegnimento di Azure [non verificato: 14 §9] | 116,12 | 642,16 | 1.634,45 |
| Senza crediti API (+ riga API) | 170,82 | 837,81 | 2.121,35 |
| Finito il bundle (+446,70 [verificato: 14 §1.3]) | 562,82 | 1.088,86 | 2.081,15 |

Note:
- Le ultime due righe partono da «dopo Azure»; l'ultima tiene i crediti. Senza bundle né crediti il consigliato costa 1.284,51 €.
- Fino alla fase 4 Andrea non c'è: il consigliato scende di 170,28 € (di 88,45 € in più se il grant ElevenLabs copre il piano Pro).
- Il consigliato presume 60 call e 300 lead al mese: con i volumi di oggi le API costano molto meno.
- I crediti da 800 $ al mese non sono confermati: forse 1.000 $ una tantum o 500 $ in comune, validi solo sull'API di prima parte [verificato: 14 §1.4].
- Dietro CGNAT si aggiunge Tailscale, 28,59 € [verificato: 15 §4.4].

---

## 7. Costi una tantum

| Voce | Importo | Fonte |
|---|---|---|
| Hardware già comprato: GPU 279, RAM 690, controller 52,70, cavo 10,80, rack 87,99, mini PC 121 | **1.241,49 €** (il prezzo del server non è nei file) | [verificato: 15 §1] |
| UPS 1.500 VA a onda sinusoidale (obbligatorio: 8,29 interruzioni l'anno nei piccoli comuni sardi) | 1.163-1.293 € | [non verificato: 14 §8; ARERA verificato: 15 §5.3] |
| 2 moduli RAM, solo con 2 CPU | ≈138 € | [non verificato: 15 §2.2] |
| Kit ventole, dissipatori e cavo GPU HPE, 2 alimentatori da 800 W, guide, 2 SSD con PLP e carrier | da verificare dopo l'inventario iLO | [verificato: 15 §7 passo 2] |
| Upgrade GPU (facoltativo, dopo 4-6 settimane di misure) | RTX PRO 4000 Blackwell 2.555 € (minimo annuo 1.544 €) o RTX A5000 2.438 € | [verificato: 13 §9] |
| Deposito API per il Tier 2 (oggi SersanOutreach è limitato dal Tier 1) | ≈250 $ ≈ 223 € | [verificato: 01 §2] |
| Numero di telefono italiano: attivazione e pratiche KYC (il canone è nei costi mensili) | da verificare | [verificato: 14 §3.1] |
| Dominio: sersan.io esiste già; un eventuale dominio per la posta degli agenti | da verificare | [verificato: 14 §8] |
| Consulenza legale: gli 8 punti di 16 §7 e le decisioni D0 sull'email | da verificare | — |
| Revisione di sicurezza esterna del Cancello, prima della rivendita | da verificare | dissenso di compliance |
| Licenza iLO Advanced (facoltativa) | da verificare | [verificato: 15 §2.6] |

---

## 8. Rischi residui e mitigazioni

| Rischio | Mitigazione |
|---|---|
| Hermes instabile: 5 patch in 10 giorni, oltre 5.000 issue, conversazioni al profilo sbagliato [verificato: 10 §3, §6] | Versione fissata, stage con 10 scenari, un processo per card, uscita alla settimana 8; le skill hanno il formato di Claude Code e restano valide [verificato: 10 §4.2] |
| Il Cancello è codice nostro, mai in produzione, di due persone | Test in CI su Linux, Mattia co-proprietario, revisioni incrociate, collaudo prima dei dati dei clienti, revisione esterna prima della rivendita |
| Funnel vuoto, nessun dato da pesare | Marketing dalla fase 0, precondizione D0, gate commerciale, fase 4 legata a lead reali |
| Un solo server e un solo amministratore; corrente e caldo in Sardegna [verificato: 15 §3.2, §5.3] | UPS, mirror ZFS, copia fuori sede, Mattia secondo amministratore, Azure accesa fino a una settimana stabile, Hermes Cloud come riserva fredda |
| Crediti API incerti; regole Anthropic cambiate due volte nel 2026 | Verifica nella Console; tetti nella porta dei modelli; uso automatico solo con chiave API; versioni fissate |
| Dati fuori UE: l'API Anthropic non ha una regione UE, Recall ed ElevenLabs stanno negli USA [verificato: 16 §5] | Tre colori; oscuramento locale; DPA; richiesta di ZDR; Bedrock UE su richiesta; prova di Vexa; Cloudflare fra i sub-responsabili |
| Iniezioni da mail e trascrizioni | Corsia d'ingresso senza strumenti; turno contaminato = carta; destinazioni per ID stabile |
| Registrazioni, Andrea, coaching; inquadramento di Alberto e Mattia «non trovato» [verificato: 16 §0]; art. 50 contro «mai etichette AI» [verificato: 05 §5] | Parere legale prima della fase 2; Andrea si dichiara sempre AI; coaching privato; informativa L. 132/2025 se ci sono dipendenti |
| Giri fra agenti e spesa che scappa | Freno nel codice, tetti per agente e per catena, `/stop` |
| Rivendita: Hermes è single-tenant [verificato: 10 §5] | Un'istanza per cliente; niente n8n nel pacchetto |
| Paperclip: advisory critici e default pericolosi [non verificato: 20-F §5] | Solo su stage, in VPN, modalità autenticata, telemetria spenta |
| GPU non qualificata HPE, RAM sbilanciata [verificato: 15 §0] | 8 moduli, kit HPE, firmware aggiornati, GPU nel monitoraggio |

---

## 9. Le decisioni di budget per i CEO

| # | Decisione | Consigliato | Costo |
|---|---|---|---|
| 1 | Avviare le fasi 0-1, con decisione alla settimana 8 | Sì | 53 gp interni in 8 settimane |
| 2 | Completare l'hardware e comprare l'UPS | Sì, con un tetto fissato dopo l'inventario iLO | UPS 1.163-1.293 €; kit da verificare |
| 3 | Upgrade della GPU | Non ora; si rivede dopo 4-6 settimane di misure | 2.438-2.555 € |
| 4 | Slack Pro per 4 persone | Sì | 27,00 €/mese |
| 5 | Claude Tag con tetto, solo dati verdi | Sì | 44,67 €/mese (50 $) |
| 6 | Bot di riunione | Recall.ai più prova di Vexa, non Fireflies (67,90 €) | ≈17,42 €/mese |
| 7 | Hermes Cloud come palestra per 2 mesi, poi riserva ferma | Sì | ≈18,67 €/mese (47 € con l'istanza accesa) |
| 8 | Notion | Plus × 4, non Business | 35,74 €/mese |
| 9 | Voce di Andrea | Solo dalla fase 4, con voce sintetica | ≈170 €/mese (88 € in meno se il grant copre il piano) |
| 10 | Parere legale unico (D0 email, registrazioni, Andrea, coaching, rappresentante UE) | Sì, prima della fase 2 | da verificare |
| 11 | Crediti API: tetto se non sono 800 $ al mese; deposito per il Tier 2 | Sì | tetto 250 €/mese (stima 195,65 €); deposito ≈223 € una tantum |
| 12 | Proxmox Community dalla fase 2 | Sì | 20 €/mese (10 € con una sola CPU) |
| 13 | Claude Team a fine bundle (data da verificare) | Ridecidere i posti alla scadenza | 446,70 €/mese con 5 premium; ≈214 € con 2 premium e 2 standard [non verificato] |
| 14 | Residenza UE dei dati rossi | Chiedere subito la ZDR (0 €); Bedrock UE solo se un cliente lo chiede | Bedrock da verificare |
| 15 | Premio mensile (H6) | Sì | voucher di 50-100 €/mese [non verificato: proposta] |
| 16 | Revisione di sicurezza esterna del Cancello | Sì, prima della rivendita (fase 5) | da verificare |
