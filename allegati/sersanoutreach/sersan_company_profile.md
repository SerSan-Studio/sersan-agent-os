# SerSan — profilo azienda e ICP (fonte: sersan.io)

**Fonte**: <https://sersan.io> — rilevato il **2026-09-17**
**Stato**: fonte di verità per l'ICP, il posizionamento e le proof point di **SerSan che fa outbound su sé stessa**.
**Non** descrive il prodotto in questo repo (per quello vedi `README.md` e `CLAUDE.md`).

> Questo documento esiste perché per mesi l'unico posto in cui il repo scriveva *cosa vende SerSan* era
> `pilot_campaign_ui_setup_guide.md` del 2026-04-20, e diceva una cosa sbagliata:
> che SerSan vende la piattaforma di outbound a «team commerciali italiani». Non è così.
> SerSan è uno **studio di software su misura, automazione e AI**. La piattaforma di questo repo è uno
> strumento interno con cui SerSan fa il proprio outbound — non è l'offerta.

Quando cambia il sito, si aggiorna **questo file**, e da qui si propaga ai campi campagna.

---

## 1. Chi è SerSan

| | |
|---|---|
| **Cosa** | Studio di custom software, workflow automation e AI. Founder-led. |
| **Headline** | «We build the software your business is missing.» |
| **Sottotitolo** | «Custom software, automation & AI · For founders & SMEs · London» |
| **Promessa d'ingresso** | «From one manual workflow to a full production platform. You don't need a CTO to start.» |
| **Claim di posizionamento** | «The intelligence is artificial. The judgement stays human.» |
| **Differenziatore dichiarato** | «We tell you when AI isn't the answer.» / «We find what *should not* be built before code becomes debt.» |
| **Entità legale** | Sersan Limited — Co. No. 16878386 |
| **Sede** | 128 City Road, London EC1V 2NX, UK |
| **Contatto diretto** | `alex.s@sersan.dev` |
| **CTA primaria** | **«Send a project brief»** → <https://sersan.io/start> — risposta di un founder **entro 1 giorno lavorativo** |

### Numeri verificati

Tre soli numeri sono pubblicati, nel contatore dell'homepage:

- **14** named projects
- **4** built by SerSan
- **1** PhD, applied maths

> ⚠️ **Non ricavare questi numeri via scraping in markdown.** Il contatore animato dell'homepage duplica ogni
> cifra nel DOM: una conversione automatica li restituisce come `1414`, `44`, `11`, e la bio di Michele
> («8 years senior delivery») diventa `88 years combined`. Verificati sull'HTML grezzo il 2026-09-17.
> Un «88 anni di esperienza combinata» in una cold email è una proof point inventata.

---

## 2. Le quattro linee di servizio

Ordine e testi come sul sito. La colonna *Solves* è la più utile per l'outbound: è il dolore dichiarato,
scritto con le parole del cliente.

| # | Servizio | Il build tipico include | Solves (il dolore) |
|---|---|---|---|
| 01 | **Custom Software & Platforms**<br>`/services/engineering` | Tool interni e gestionali · portali clienti e web app · prodotti SaaS e piattaforme academy/LMS · integrazioni fra gli strumenti già in uso | «The tools you run on don't talk to each other.»<br>«You need software built properly, without hiring a team.» |
| 02 | **Workflow Automation**<br>`/services/automation` | Back-office ripetitivo · documenti letti, controllati e archiviati · lead/ordini/CRM tenuti in sync · niente perso: fallimenti mostrati e ritentati | «Your team retypes the same data every week.» |
| 03 | **AI Features & Reliability**<br>`/services/mlops` | Assistenti e copiloti sui propri contenuti · agenti che agiscono, con i limiti che decidi tu · testati su casi reali prima del rilascio · monitorati live su costo, qualità, accuratezza | «The AI demo impressed everyone, then stalled.» |
| 04 | **Technical Audits & Architecture**<br>`/services/architecture` | Audit di sistemi e processi · scelta build vs. buy vs. **don't-build** · dove l'AI ripaga davvero · architettura target, sequenziata e costata | «You know what's broken, not what to build first.»<br>«You need readiness before a board, customer, or regulator.» |

**Modello di ingaggio**: fixed scope, a fasi. «Days to weeks per workflow» per l'automazione. La continuazione
si guadagna con il valore dimostrato. Nessun prezzo pubblicato: si parte dal brief scritto.

### Il processo in 5 passi (utile come struttura di messaggio)

1. **Problem** — «It starts with one problem worth solving.» Si mappa quello che c'è davvero, non l'organigramma.
2. **Scope** — Costo, rischio, effort e risparmio reale, *prima* di scrivere codice. «Sometimes the honest answer is to build less, or nothing.»
3. **Build** — Tool interni, integrazioni, automazioni, web e mobile, e AI dove se lo merita.
4. **Proof** — «Working software is the only proof.» Monitoring, revisione umana e rollback dal giorno uno.
5. **Handover** — Il codice e il sistema sono del cliente, documentati, con training. E si resta raggiungibili.

### Il taglio su AI affidabile (linguaggio proprietario, buono per gli angle)

Il problema in tre parti — **No baseline** («A system you can't measure is a system you can't fix»),
**No trail** («every incident turns into archaeology»), **No boundaries** — e il rimedio in tre parti:
**eval baseline** (casi di test versionati), **trace propagation** («the answer is in the record… not Slack
archaeology»), **guardrail clamp**.

---

## 3. ICP

### 3.1 Chi

| Dimensione | Valore |
|---|---|
| **Tipo di azienda** | Founder, PMI, team in crescita. Da *un* workflow manuale a una piattaforma in produzione. |
| **Segnale chiave** | Non hanno un team di engineering interno — o ce l'hanno ma è saturo. «You don't need a CTO to start.» |
| **Ruoli** | Founder / CEO / owner; leader tecnici e di business che possono **definire il problema e autorizzare il lavoro**. Chi decide e chi sblocca. |
| **Geografia** | Base a Londra (UK). Consegna in inglese e italiano — il sito è bilingue EN/IT e la squadra è UK + Italia (Sardegna). |
| **Settori con referenze reali** | FinTech · Agritech / Rinnovabili · Real Estate · Industrial · Healthcare / MedTech · Public Sector · Aerospace · Energy · Greentech / Marine |

### 3.2 Griglia di qualificazione — dal sito, letterale

Questa è la sezione «We are honest about who we work with». Va usata **così com'è** come rubrica del
qualifier e come filtro pre-invio: è il criterio che l'azienda ha già scelto di rendere pubblico.

| # | ✅ Good fit | ✗ Not a fit |
|---|---|---|
| 01 | Qualcosa nel business costa tempo o denaro **oggi**. | Vogliono un chatbot-gadget per un comunicato stampa. |
| 02 | Sanno spiegare il workflow, anche senza la tecnologia. | Nessuno sa dire quale problema si stia risolvendo davvero. |
| 03 | Preferiscono risolvere un problema reale che comprare un'altra licenza. | Vogliono un prezzo fisso prima che il lavoro sia definito. |
| 04 | Vogliono una cosa fatta bene, regolamentati o no. | Vogliono saltare la compliance per uscire prima. |
| 05 | C'è qualcuno, tecnico o no, che può decidere e sbloccare. | Non decide nessuno, quindi non si firma niente. |
| 06 | Possono dare persone, dati o accessi per capire il problema. | Non danno gli accessi o il feedback che il lavoro richiede. |

**Come leggerla in outbound**: i «good fit» sono *trigger* da cercare nei segnali (un processo manuale citato,
uno stack frammentato, un progetto AI fermo dopo la demo, una scadenza di compliance). I «not a fit» sono
*motivi di scarto* — e sono anche il materiale migliore per la differenziazione, perché dire «non lo
costruiamo» è il posizionamento.

---

## 4. Case study e proof point

### 4.1 La distinzione che non va persa

Il sito separa nettamente due cose, e **l'outbound deve fare lo stesso**:

- **SerSan delivery / SerSan build** — lavoro consegnato *da SerSan come studio*. Qui si può dire «abbiamo costruito».
- **Prior experience** — lavoro fatto dai singoli (quasi sempre **Michele Sanna**) *prima* di SerSan, presso terzi.
  Qui si dice «il nostro CPTO ha costruito X in Revolut», **mai** «abbiamo lavorato con Revolut».

> Attribuire a SerSan un cliente tier-1 che è in realtà un impiego precedente di un fondatore è una proof point
> falsa: è il tipo di affermazione che brucia la credibilità nel primo reply e, in cold outreach su clienti
> regolamentati, è un rischio concreto. La regola vale nei prompt del copy agent, nei template e nei case study PDF.

### 4.2 Costruiti da SerSan

| Progetto | Settore | Cosa | Stack | Numeri / stato |
|---|---|---|---|---|
| **SphereNode** (`/case-studies/spherenode`) | FinTech · trading education | Ha collassato 8 SaaS (Circle, Teachable, Zoom, Intercom, HubSpot, Mailchimp, Stripe, Notion) in **un** prodotto verticale: Academy, Live Trading, AI Mentor RAG, Community, CRM, Pagamenti, Broadcast. Bilingue IT/EN. | TypeScript, React, Python, FastAPI, PostgreSQL, Supabase, Gemini RAG, Vimeo, Capacitor, PWA | Live in produzione · «8 → 1» tool · **32** capability RBAC granulari · una codebase, tre percorsi di installazione (PWA + iOS + Android) |
| **Quantex.live** (`/case-studies/quantex`) | FinTech · quant | Piattaforma di trading quantitativo AI-native: ingestione dati di mercato real-time, workflow di ricerca guidati da agenti LLM, motore di generazione segnali. | TypeScript, React, Node.js, Python, PostgreSQL, Redis, WebSockets, Vercel | V1 live · roadmap di build **14 settimane** su 5 fasi · V2 (layer AI) in sviluppo |
| **TerraNoa** (`/case-studies/terra-noa`) | Agritech · rinnovabili | Operazione integrata nel Sulcis Iglesiente: reti di sensori IoT, monitoraggio agrivoltaico, pipeline di manutenzione predittiva, telemetria da droni termografici e agricoli, integrazioni SCADA/OT. Michele è Presidente & CTO. | Databricks, PySpark, Delta Lake, Python, MLflow, Kafka, MQTT, Grafana, SCADA/OT | **13** linee di business su un'unica data backbone · ~**1,5 MWp** agrivoltaico pianificati · in implementazione |
| **DomusTua** (`/case-studies/domus-tua`) | Real Estate | Sito di brand con motion design e lead generation. | — | Consegnato |

### 4.3 Esperienza precedente (attribuita alle persone, non allo studio)

| Organizzazione | Settore | Contributo | Attribuzione corretta |
|---|---|---|---|
| **Revolut** | FinTech | Fraud detection · real-time inference | Michele Sanna, prima di SerSan |
| **J.P. Morgan** | FinTech · treasury | Credit risk · aerospace research | Michele Sanna, prima di SerSan |
| **Apple UK** (via Deloitte) | Retail operations | Time-series ML · supply chain | Michele Sanna, via Deloitte |
| **World Health Organization** | MedTech · oncologia | Computer vision · ricerca oncologica | Michele Sanna, research grant (freelance) |
| **Leonardo S.p.A.** | GEOINT | Cloud security · platform engineering | freelance |
| **Regione Sardegna** (via Accenture) | Settore pubblico · sanità | Identità digitale | via Accenture |
| **Tier-1 Pharmaceutical** (via Deloitte) | Life sciences | ML · trial operations | via Deloitte |
| **Salvatori** | Industrial | Computer vision · manutenzione predittiva · RL | CTO frazionale |
| **Rete RSSA italiana** | HealthTech · lungodegenza | Supporto alle decisioni cliniche | freelance |
| **Stealth Greentech** | Greentech · marine | Propulsione elettrica · IoT · manutenzione predittiva | co-founder & CTO |

Altri marchi citati nell'esperienza senior pre-SerSan: **Brevan Howard**, **Accenture**, **Deloitte**.

---

## 5. Il team (i mittenti)

| Persona | Ruolo | Titoli / note |
|---|---|---|
| **Alessandro Serratt** | CEO · Commercial Lead | USAAI Certified AI Consultant (CAIC) · doppio master: MBA + AI in Business. Possiede scoping, proposte, pricing, comunicazione col cliente. |
| **Michele Sanna** | CPTO · Technical Lead | PhD in Matematica Applicata, LSE · 8 anni di delivery senior in istituzioni tier-1 prima di SerSan (J.P. Morgan, Revolut, Deloitte, Brevan Howard, Accenture). |
| **Alberto Tuveri** | Software & AI Engineer · Creative Lead | BSc Informatica, Università di Camerino (2026) · tesi su architettura e sicurezza di sistemi agentici a livello OS (MCP, multi-agent, Zero-Trust) · front-end, WebGPU e motion; ha costruito sersan.io; direzione creativa e logo. |
| **Mattia Scattu** | Software Engineer | BSc Informatica, Università di Camerino · pubblicazione: *Knowledge Graphs as a Semantic Layer for Understanding Robotic Video* · ha consegnato un gestionale manutenzione/inventario per un operatore resort. |

Principio di ingaggio: **ogni progetto ha un owner commerciale e un owner tecnico, entrambi con nome e cognome**,
dalla proposta all'handover. «You work with the builders.»

---

## 6. Valori paste-ready per i campi campagna

Da incollare nel form campagna (`/campaigns/new/`) o nel wizard di onboarding (`/onboarding/`).
I nomi dei campi sono quelli del modello: vedi `backend/models/campaign.py`.

### `booking_link`

```
https://sersan.io/start
```

> ⚠️ **`https://cal.com/sersan/discovery` non esiste.** Era un placeholder entrato nella guida pilota del
> 2026-04-20 e mai sostituito. Sul sito **non c'è nessun link a calendario**: la CTA è il brief scritto su
> `/start`, con risposta di un founder entro 1 giorno lavorativo. Un link a calendario morto in una cold
> email è una conversione persa e un danno di reputazione.
> Fallback per contatto diretto: `alex.s@sersan.dev`.

### `icp_description`

```
Founder, PMI e team in crescita (indicativamente 10-200 dipendenti) senza un team di engineering interno,
o con un team saturo. Settori con referenze reali: FinTech, Agritech/rinnovabili, real estate, industriale,
healthcare/MedTech, settore pubblico, aerospace, energy, greentech. Decisore: founder/CEO/owner, oppure un
leader tecnico o di business che può definire il problema e autorizzare il lavoro.

Segnali di buon fit: un costo in tempo o denaro che si paga OGGI; uno stack frammentato in cui gli strumenti
non si parlano; dati ridigitati a mano ogni settimana; un progetto AI che ha impressionato in demo e poi si e'
fermato; una scadenza di compliance o una due diligence in arrivo; qualcuno dalla loro parte che puo' decidere
e sbloccare.

Segnali di scarto: vogliono un chatbot-vetrina per un comunicato; nessuno sa dire quale problema si stia
risolvendo; vogliono un prezzo fisso prima che il lavoro sia definito; vogliono saltare la compliance per
uscire prima; non decide nessuno; non danno accessi ne' feedback.
```

### `value_props`

```
- Si parte dal problema, non dalla tecnologia: mappiamo il processo reale, poi decidiamo cosa NON costruire.
  A volte la risposta onesta e' costruire meno, o niente.
- Scope fisso e a fasi: costo, rischio, effort e risparmio stimati PRIMA che qualcuno scriva codice.
  Da giorni-settimane per un singolo workflow fino a una piattaforma in produzione.
- Owner commerciale e owner tecnico con nome e cognome su ogni progetto, dalla proposta all'handover.
  Si lavora con chi costruisce.
- AI che regge i clienti veri: eval versionate prima del rilascio, tracciabilita' di cosa e' entrato/deciso/
  fatto/chi ha revisionato, guardrail e revisione umana sulle decisioni ad alto impatto, costo e qualita'
  monitorati in produzione.
- Il sistema resta tuo: codice nel tuo repository, documentazione, training del team, percorsi di rollback,
  e noi restiamo raggiungibili.
```

### `product_docs`

```
SerSan e' uno studio di custom software, automazione e AI con sede a Londra (Sersan Limited, 128 City Road,
London EC1V 2NX), founder-led. Costruiamo il software che manca all'azienda: dal singolo workflow manuale
fino alla piattaforma in produzione, per founder, PMI e team in crescita che non hanno un reparto di
engineering.

Quattro servizi. (1) Custom Software & Platforms: tool interni e gestionali, portali clienti, prodotti SaaS
e piattaforme academy/LMS, integrazioni fra gli strumenti gia' in uso. (2) Workflow Automation: back-office
ripetitivo, documenti letti/controllati/archiviati, lead-ordini-CRM tenuti in sync, con i fallimenti
mostrati e ritentati invece che persi. (3) AI Features & Reliability: assistenti e copiloti sui contenuti
del cliente, agenti che agiscono entro limiti definiti, testati su casi reali prima del rilascio e
monitorati live su costo, qualita' e accuratezza. (4) Technical Audits & Architecture: audit di sistemi e
processi, decisione build vs buy vs don't-build, dove l'AI ripaga davvero, architettura target sequenziata
e costata.

Come lavoriamo: problema -> scope (costo, rischio, effort, risparmio, prima del codice) -> build ->
proof (si misura se ha davvero fatto risparmiare tempo o denaro) -> handover (codice e sistema di
proprieta' del cliente, documentati, con training). Il claim: l'intelligenza e' artificiale, il giudizio
resta umano. E diciamo al cliente quando l'AI non e' la risposta.

Lavori consegnati da SerSan: SphereNode (FinTech/trading education, otto SaaS collassati in un prodotto
verticale, live, 32 capability RBAC); Quantex.live (FinTech quant, piattaforma AI-native con dati
real-time e agenti LLM, V1 live, roadmap 14 settimane); TerraNoa (agritech e rinnovabili, IoT e
manutenzione predittiva su Databricks, 13 linee di business su una sola data backbone, ~1,5 MWp
agrivoltaico pianificati); DomusTua (real estate, sito brand e lead generation).

Esperienza precedente dei fondatori, DA ATTRIBUIRE ALLE PERSONE E NON ALLO STUDIO: il CPTO Michele Sanna
(PhD in matematica applicata, LSE) ha lavorato su fraud detection real-time in Revolut, credit risk in
J.P. Morgan, time-series ML per Apple UK via Deloitte, e computer vision oncologica per la World Health
Organization. Non dire mai che SerSan ha avuto questi clienti.

Contatto: il punto di ingresso e' un brief scritto su https://sersan.io/start, letto e risposto da un
founder entro un giorno lavorativo. Nessun link a calendario.
```

### `campaign_objective`

```
Ottenere un brief scritto o una conversazione di scoping con il decisore, su UN problema concreto che oggi
costa tempo o denaro (un processo manuale, strumenti che non si parlano, un progetto AI fermo dopo la demo,
una scadenza di compliance). Non vendere un pacchetto: fare in modo che il prospect descriva il problema.
Prossimo passo proposto: rispondere a questa email descrivendo il problema, oppure inviare il brief su
https://sersan.io/start.
```

### Variante EN

Per campagne in inglese (`target_language: en`), gli stessi contenuti nella lingua del sito:

- **icp_description** — Founders, SMEs and growing teams (roughly 10-200 staff) with no in-house engineering team, or one that is already at capacity. Sectors with real references: FinTech, Agritech/renewables, real estate, industrial, healthcare/MedTech, public sector, aerospace, energy, greentech. Decision-maker: founder/CEO/owner, or a technical or business leader who can define the problem and authorise the work. Good fit: something in the business costs time or money today; the tools they run on don't talk to each other; the team retypes the same data every week; the AI demo impressed everyone, then stalled; readiness needed before a board, customer or regulator; someone on their side can decide and unblock. Not a fit: a chatbot gimmick for a press release; nobody can explain the problem; a fixed price demanded before the work is defined; skipping compliance to ship faster; nobody can sign off; no access or feedback.
- **campaign_objective** — Get a written brief or a scoping conversation with the decision-maker about one concrete problem that costs time or money today. Next step: reply describing the problem, or send a brief at https://sersan.io/start.
- **booking_link** — `https://sersan.io/start`

---

## 7. Regole per il copy (vincolanti)

1. **Mai attribuire a SerSan i clienti dell'esperienza precedente.** «Il nostro CPTO ha costruito la fraud
   detection real-time in Revolut» è vero; «abbiamo lavorato con Revolut» non lo è. Vedi §4.1.
2. **Solo i tre numeri pubblicati** (14 / 4 / 1) e le metriche dei case study in §4.2. Niente percentuali
   inventate. In particolare: la vecchia riga «abbiamo aiutato un'agenzia da 40 persone a tagliare del 60%
   il collo di bottiglia» era finta ed è stata rimossa da `scripts/so137_create_test_campaign.sh`.
3. **Nessun link a calendario.** La CTA è il brief su `/start` o una risposta all'email.
4. **Un problema per messaggio.** Il posizionamento è «si parte da un problema che vale la pena risolvere»:
   un'email che elenca quattro servizi lo contraddice.
5. **Il «don't-build» è un asset, non una scusa.** «A volte la risposta onesta è costruire meno, o niente»
   è il differenziatore più forte contro le software house e va usato.
6. **Nessuna promessa di prezzo fisso prima dello scope** — è letteralmente un «not a fit» dichiarato.

---

## 8. Dove questi valori vanno a finire

| Destinazione | Cosa | Come |
|---|---|---|
| Campagne in DB (`campaigns`) | `icp_description`, `value_props`, `product_docs`, `campaign_objective`, `booking_link` | Form UI `/campaigns/new/` o wizard `/onboarding/`. **Sono dati, non codice**: cambiarli in prod è un'azione da operatore. |
| Copy agent email | contesto campagna | `workers/email/copy_agent.py` legge i campi qui sopra dalla campagna |
| Copy agent LinkedIn | contesto campagna | `linkedin/agents/copy_agent.py` |
| Angle agent | contesto campagna | `backend/clients/claude_angle_agent.py` |
| Qualifier / feed ICP | griglia §3.2 | `ml/qualifier.py`, feed `/linkedin/feed/` |
| Guida pilota | valori d'esempio | `pilot_campaign_ui_setup_guide.md` |

**Le campagne già in produzione non vengono aggiornate da questo file.** Se una campagna live è stata
creata con il vecchio posizionamento, i suoi campi vanno corretti a mano dall'operatore con i valori di §6.
