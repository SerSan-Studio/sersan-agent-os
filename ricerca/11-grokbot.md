# 11. Grok Bot (SpaceXAI / Cursor): scheda allo stato del 24 ottobre 2026

Rapporto per il progetto SerSan Agent OS. Domanda: Grok Bot può fare da orchestratore e "squadra di agenti" per SerSan (4-5 persone), al posto o accanto a un sistema sul nostro server?

Nota sul nome: il prodotto si chiama **Grok Bot** (due parole). "Grokbot" o "Grockbot" sono le grafie dei video.

## Come leggere le etichette

- **[verificato: URL, 24/10]**: pagina ufficiale (documentazione `docs.x.ai/grok-bot`, aiuto e prezzi su `cursor.com`, termini, pagina di stato) aperta da me oggi, 24 ottobre 2026.
- **[verificato 14/10: fonte]**: pagina ufficiale riaperta il 14-15 ottobre 2026.
- **[terzi: fonte]**: stampa, blog, post. Sono voci di terzi, non conferme ufficiali.
- **[video V1/V2/V3]**: trascrizioni di tre video pubblici, non pubblicate in questa repo. V1 spiega 25 concetti di Grok Bot, V2 confronta Grok Bot e Hermes, V3 racconta le novità di Claude e di Grok Bot. Mostrano l'uso di una persona: sono testimonianze, non documentazione.
- **[non verificato]**: nessuna fonte affidabile lo conferma. **"non trovato"**: l'ho cercato e non c'è.

Il sito `x.ai` (changelog, Marketplace, post) risponde 403 agli strumenti automatici anche oggi: ciò che sta solo lì viene dalle verifiche del 14-15 ottobre o dalla stampa.

---

## 1. Scheda in breve

| Voce | Risposta | Fonte |
|---|---|---|
| Che cos'è | App chiusa (desktop macOS/Windows/Linux, iPhone/iPad, Android) con cui si tiene una squadra di agenti con nome e ruolo, i "Bot", che lavorano su un computer nel cloud con browser, file e terminale, usano i connettori e chiedono approvazioni | [verificato: https://docs.x.ai/grok-bot/faq, 24/10] |
| Chi lo fa | Marchio Grok di SpaceXAI (xAI è dentro SpaceX dal 2 febbraio 2026). Account, computer, fatturazione, termini e stato sono di Cursor (Anysphere), che SpaceX ha comprato ad agosto 2026 | [verificato 14/10]; termini su cursor.com [verificato: https://cursor.com/terms/grok-bot, 24/10] |
| Da quando | Beta dall'11 agosto 2026. Ultima versione stabile 0.75.5, del 23 ottobre 2026 | [verificato 14/10: InfoQ e Reworked]; [terzi: post di un dipendente Cursor su X, https://x.com/ericzakariasson/status/2113743401975963908] |
| Quanto costa | Incluso nei piani The X Subscription Premium (30 $), Super (100 $) e Ultra (200 $) al mese, anche come posti di team agli stessi prezzi. Oltre la quota settimanale si paga con crediti prepagati | [verificato: https://cursor.com/pricing e https://cursor.com/docs/account/teams/pricing, 24/10] |
| Costo stimato per 4-5 persone | Da 120-150 $ al mese (solo Premium) a circa 360-590 $ al mese (uso reale), IVA esclusa. Vedi §4 | stima mia [non verificato] sui prezzi verificati |
| Gira sul server SerSan? | **No.** Gira solo sui computer cloud di Cursor, negli Stati Uniti; niente installazione in casa né immagine propria. Il server può solo essere raggiunto dai Bot come strumento esterno (§6) | [verificato: https://docs.x.ai/grok-bot/security, 24/10] |
| Modelli | Li sceglie il servizio per ogni compito, anche di terzi (nominato Opus 5.5). L'utente non sceglie, non blocca e non vede quale modello ha risposto | [verificato: https://cursor.com/help/grok-bot/models, 24/10] |
| Dati | Archiviazione cloud obbligatoria; computer negli Stati Uniti; residenza dei dati solo con un impegno scritto tramite il commerciale; DPA di Cursor con clausole contrattuali standard UE e addendum UK | [verificato: docs.x.ai/grok-bot/security e /faq, 24/10]; [terzi: risultato di ricerca su https://www.cursor.com/terms/dpa, testo non aperto] |
| Copertura della visione di Alberto | Buona sulla forma (agenti con ruolo, delega, chat tra agenti, routine, Slack, Notion, approvazioni); scarsa sul cuore dati (database vettoriale, registro delle riunioni, CRM pesato) e nulla sull'agente vocale telefonico. Vedi §5 | analisi mia |
| Rischi principali | Lock-in totale (chiuso, cloud, nessun export documentato, nessuna scelta di modello), dati negli USA, computer condiviso tra tutti i Bot di un utente, quote settimanali, beta con incidenti frequenti, termini che mettono ogni azione a carico del cliente. Vedi §7 | §7 |

---

## 2. Che cos'è, funzione per funzione

### 2.1 Il Bot

| Funzione | Stato | Fonte |
|---|---|---|
| Bot con nome, etichetta (ruolo) e descrizione; avatar che mostra lo stato | c'è. Le pagine ufficiali divergono sul campo descrizione: l'aiuto di Cursor dice che le regole durature stanno ora nella memoria | [verificato 14/10: `docs.x.ai/grok-bot/bots`, `cursor.com/help/grok-bot/edit-bot`]; [video V1 §1-2] |
| Bot principale ("Main Bot", con la stella) che per prima cosa delega | c'è, dalla 0.66 | [verificato 14/10: changelog 0.66.0]; [video V3] |
| Quanti Bot per account | circa 50 secondo un post di settembre, "più di 50" secondo il changelog 0.31; la documentazione non dà un limite | [verificato 14/10]; limite attuale non trovato |
| Template condivisibili ("Share as template", link pubblico o solo team, Marketplace web con 90 template) | c'è. Il template porta istruzioni, memorie rilevanti, skill, routine e plugin, non computer, accessi e cronologia | [verificato 14/10: `docs.x.ai/grok-bot/bots`]; [video V1 §3] |
| Duplicare un Bot senza la cronologia | c'è | [verificato 14/10]; [video V1 §25] |

### 2.2 Memoria e contesto

| Funzione | Stato | Fonte |
|---|---|---|
| Memoria per Bot (preferenze, fatti, riassunti) | c'è; la documentazione avverte che non è una fonte autorevole | [verificato 14/10: `docs.x.ai/grok-bot/bots`] |
| Memoria globale comune a tutti i Bot | il video la mostra; la documentazione riaperta non la nomina | [video V1 §4]; [non verificato su pagina ufficiale] |
| Memoria di team e note private per persona (Team Bots) | c'è | [verificato: https://docs.x.ai/grok-bot/team-bots, 24/10] |
| Compattazione automatica della conversazione | automatica, non controllabile, non si sa quando avviene | [video V1 §5]; meccanismo non documentato |
| Pannello per modificare le memorie, esportazione della memoria | non trovato | [verificato 14/10] |

### 2.3 Il computer nel cloud

| Funzione | Stato | Fonte |
|---|---|---|
| Computer cloud persistente con browser, file (`/workspace`) e terminale | c'è | [verificato: https://docs.x.ai/grok-bot/computer-and-apps, 24/10] |
| **Un computer per Bot?** | **No: un computer per utente, condiviso da tutti i suoi Bot** (cookie, sessioni, file, credenziali della riga di comando). Ogni Bot ha solo un suo schermo. I video dicono "ogni Bot ha un computer": è impreciso | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §6] |
| Isolamento | microVM Firecracker per utente, separata a livello hardware dagli altri utenti; tra i Bot dello stesso utente nessun confine ("non usare Bot separati come confine di sicurezza") | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [verificato 14/10] |
| Disco da 126 GB | lo dice solo V2; la documentazione non indica la dimensione del disco | [video V2]; dimensione ufficiale non trovata |
| Browser con login salvati | c'è: si entra una volta e la sessione vale per tutti i Bot dell'utente; per password, 2FA, CAPTCHA e pagamenti l'utente prende il controllo | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §7, §21] |
| Vault di login, carte e contatti compilati dal Bot | nuovo nella 0.75.5 del 23 ottobre | [terzi: risultati di ricerca sul changelog ufficiale https://x.ai/changelog/bot e post X di eric zakariasson]; pagina non aperta (403) |
| File explorer condiviso | i file in `/workspace` sono visibili a ogni Bot; un'app "file explorer" dedicata non è descritta | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §8] |
| Terminale | c'è, sul computer cloud | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §9] |
| Accesso al PC locale dell'utente | c'è, se attivato: comandi e file con policy `Ask every time` (predefinita), `Always allow`, `Never allow`. Se l'app desktop debba restare aperta non è scritto | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §10, V2] |
| Indirizzi IP di uscita | statici, condivisi tra tutti i clienti; alcuni siti bloccano i datacenter | [verificato 14/10] |

### 2.4 Abilità

| Funzione | Stato | Fonte |
|---|---|---|
| Plugin con OAuth da "Connect apps", validi per tutto l'account; token tenuti dal backend di Cursor | c'è | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10] |
| Server MCP propri (`Remote HTTPS` o `Command`) | documentati per i Team Bots | [verificato: docs.x.ai/grok-bot/team-bots, 24/10] |
| Skill (libreria comune, richiamo con `/`) | c'è | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §12] |
| "Teach a task": registra fino a 10 minuti sul computer del Bot e ne ricava una skill in bozza; solo desktop, rilascio graduale | c'è | [verificato: docs.x.ai/grok-bot/faq, 24/10, per i 10 minuti]; [verificato 14/10] |
| Routine a orario e su evento (Slack, GitHub, Linear, Microsoft Teams, Sentry, PagerDuty, email del Bot, webhook, X); fino a 50 per Bot, almeno 5 minuti tra due esecuzioni, ultimi 20 esiti | c'è | [verificato 14/10]; [video V1 §14-15] |
| Webhook: ogni routine ha un indirizzo `POST` con chiave `Bearer`; 200 vuol dire "partita", non "finita" | c'è | [verificato 14/10: `cursor.com/help/grok-bot/routines`] |
| Indirizzo email proprio del Bot (`mail.grokbot.com`, uno per utente); ogni invio chiede approvazione | c'è | [verificato 14/10: `cursor.com/help/grok-bot/agent-email`] |
| App del telefono: calendario, promemoria, contatti, messaggi, posizione, casa domotica, con un "Allow" per app | in rilascio dal 22 ottobre 2026 su iOS e Android | [terzi: https://digitaltrends.com/phones/grok-bot-can-now-manage-your-calendar-reminders-and-more, 22/10] |
| Lavoro di codice | passa ai Cloud Agent di Cursor; V2 mostra un Bot di QA che lancia Cursor (prima con Claude Sonnet 4.5, poi con GPT 5.6 Sol) e torna con una PR | [verificato 14/10]; [video V2] |

**Plugin chiesti nel compito**

| Plugin | Esiste? | Fonte |
|---|---|---|
| Slack | sì (scrive come l'utente collegato; Team Bots come app Slack propria) | [verificato: docs.x.ai/grok-bot/team-bots, 24/10] |
| Gmail | sì, una casella alla volta | [verificato 14/10: `cursor.com/help/grok-bot/connect-plugins`] |
| Notion | sì (anche un secondo account); 43 template su 90 lo usano | [verificato 14/10] |
| HubSpot | compare tra le integrazioni di 4 template del Marketplace | [verificato 14/10: Marketplace x.ai non riaperto] |
| Google Docs, ClickUp | usati nel video | [video V1 §11] |
| Stripe, Sentry, GitHub, AWS, Cloudflare, 1Password, Apollo | mostrati nel video (Apollo con un errore) | [video V2]; 1Password solo su Mac [verificato 14/10: changelog 0.53] |
| Fireflies | **plugin non trovato**; V1 ha una skill privata "Fireflies ingest" | [video V1 §12] |
| Gong, Granola, Salesforce, Attio, Linear, Google Calendar/Drive/Sheets, Figma | nei template del Marketplace | [verificato 14/10] |
| Zoom | l'accesso dall'app desktop fallisce con l'errore 4700 | [verificato 14/10] |
| Totale catalogo | 220 plugin a metà agosto, secondo il Bot stesso a una giornalista | [terzi: Reworked, 12/08] |

### 2.5 Lavoro tra Bot

| Funzione | Stato | Fonte |
|---|---|---|
| Chat di gruppo da 2 a 6 Bot | c'è | [verificato 14/10: `docs.x.ai/grok-bot/chat-and-collaboration`]; [video V1 §16] |
| Menzioni `@`, `@everyone`, risposte in thread | c'è | stessa fonte; [video V1 §17, §19] |
| Passaggi di lavoro (messaggio asincrono da Bot a Bot), conversazione leggibile | c'è | stessa fonte; [video V1 §18] |
| Interruttore admin "Messaging Between Bots" | c'è (acceso per default) | [verificato 14/10] |
| Team Bot: un Bot configurato una volta e pubblicato al team; ogni collega ci parla in privato, nell'app o in Slack; OAuth con l'account di chi parla; fino a 25 segreti cifrati; routine personali; l'uso conta su chi parla | c'è | [verificato: docs.x.ai/grok-bot/team-bots, 24/10]; [video V3] |

### 2.6 Controllo

| Funzione | Stato | Fonte |
|---|---|---|
| Approvazioni `Allow once` / `Always allow` / `Deny`; bozze di email e Slack da inviare o scartare (spegnibili per Bot) | c'è | [verificato 14/10]; [video V1 §20] |
| Approvazioni nel lavoro non presidiato (routine, altri Bot) scadono dopo circa 10 minuti | c'è | [verificato 14/10: `docs.x.ai/grok-bot/approvals-security-and-privacy`] |
| Auto Review: modello revisore delle azioni rischiose; non guarda ogni effetto; imposizione e regole di team solo Enterprise | c'è | [verificato: docs.x.ai/grok-bot/security, 24/10] |
| Presa di controllo umana (password, 2FA, CAPTCHA, pagamenti) | c'è | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]; [video V1 §21] |
| Notifiche sul telefono per Bot | c'è | [verificato 14/10]; [video V1 §24] |
| Storico delle esecuzioni delle routine | ultimi 20 esiti; secondo V1 non si apre il dettaglio di un'esecuzione | [verificato 14/10]; [video V1 §23] |
| Log delle azioni ("Action Recording", 90 giorni), audit log, OpenTelemetry | solo Enterprise | [verificato: docs.x.ai/grok-bot/security, 24/10] |
| Log fatto dall'utente (ClickUp, Sheet, database) | consiglio del video, non una funzione | [video V1 §26] |

---

## 3. Modelli e annuncio di Musk

- **Il post.** Musk ha scritto su X il 7 ottobre 2026 che SpaceX userà "il miglior modello di back-end per ogni compito", nominando Claude Opus 5.5, Midjourney, Suno e "altre API di punta". [terzi: The Next Web, Ana Maria Constantin, 7/10, https://thenextweb.com/news/grok-bot-claude-opus-midjourney-suno-musk; TeslaNorth, https://teslanorth.com/2026/10/07/grok-bot-claude-opus-5-5-midjourney-suno/]. Il post originale su X non l'ho aperto. Alcune fonti lo datano alla sera del 6 ottobre (ora USA).
- **Che cosa dice la pagina ufficiale** [verificato: https://cursor.com/help/grok-bot/models, 24/10]:
  - per ogni compito Grok Bot usa il modello "più probabile a dare il risultato migliore", della casa o di un fornitore della lista dei sub-responsabili di Cursor;
  - nessun selettore di modello, né per utente né per richiesta; non si può bloccare un modello;
  - l'utente non vede quale modello ha risposto: l'uso compare come "uso di Grok Bot";
  - **l'instradamento verso Opus 5.5 non cambia il costo per token**; la quota si consuma secondo il tipo di lavoro e lo sforzo;
  - l'allowlist dei modelli del team in Cursor non vale per Grok Bot.
- **Che cosa vuol dire per i costi.** Non si paga di più quando il servizio sceglie Claude, ma non si può nemmeno chiedere Claude né prevedere il consumo. I crediti API Anthropic di SerSan (800 $ al mese) non si possono usare dentro Grok Bot: un'opzione "porta la tua chiave" non l'ho trovata. Un compito che il servizio manda ad Anthropic porta i dati a un sub-responsabile in più.
- **Il modello della casa.** V2 (più vecchio) dice "solo Grok 4.6"; V3 parla di Grok 4.7 come modello base, con i compiti difficili mandati a Opus 5.5 [video V2, V3]. Una versione ufficiale del modello di base non l'ho trovata.
- **Harness Cursor.** Il codice va ai Cloud Agent di Cursor [verificato 14/10]. Sui team, i modelli di terzi usati in Cursor si pagano a prezzo di listino API più 0,25 $ per milione di token ("Cursor Token Rate"); i modelli Cursor e Grok ne sono esenti [verificato: https://cursor.com/docs/account/teams/pricing, 24/10]. Se un Cloud Agent lanciato da un Bot paghi questa tariffa non è scritto [non verificato].

---

## 4. Piani e prezzi (rilevati il 24 ottobre 2026)

### 4.1 Piani in vigore: The X Subscription (dal 12 ottobre 2026)

| Piano | Prezzo al mese, tasse escluse | Grok Bot | Uso rispetto a Plus | Fonte |
|---|---|---|---|---|
| Free | 0 $ | no | limitato | [verificato: https://cursor.com/pricing, 24/10] |
| Plus | 8 $ (prezzo introduttivo) | no | base | idem |
| Premium | 30 $ | sì | 4x | idem |
| Super | 100 $ | sì | 15x | idem |
| Ultra | 200 $ | sì | 50x | idem |
| Teams | posti Premium 30 $, Super 100 $, Ultra 200 $ per utente; tipi di posto misti; Plus non c'è per i team | sì | come il piano individuale corrispondente | [verificato: https://cursor.com/docs/account/teams/pricing, 24/10] |
| Enterprise | su trattativa; quota "pooled"; controlli di accesso, rete e audit | sì | — | [verificato: https://cursor.com/pricing, 24/10] |

Regole d'uso [verificato: https://cursor.com/help/grok-bot/plans e /docs/account/teams/pricing, 24/10]:
- Una quota settimanale per posto, condivisa tra Grok Bot, Cursor e le app Grok; **i posti di un team non si dividono la quota** e l'uso non passa da un membro all'altro.
- Oltre la quota: crediti prepagati (`Auto Top-up`, tetto mensile in `grok.com/dashboard/billing`); nei team un saldo prepagato comune che solo gli admin ricaricano; l'uso si ferma quando finisce il saldo o si tocca il tetto mensile del team.
- L'ampiezza della quota in token non è pubblicata. Il prezzo dei crediti non è sulla pagina dei prezzi.
- Prova gratuita: un credito d'uso entro sette giorni, che non diventa un abbonamento.

### 4.2 Piani legacy (ancora validi per chi li ha)

Cursor Pro, Pro+ e Ultra (20, 60, 200 $), Cursor Teams Standard e Premium (40 e 120 $ a posto), SuperGrok, SuperGrok Plus e SuperGrok Heavy collegati a un account Cursor (30, 100, 300 $), X Premium+, Grok Business. Sui piani legacy, oltre la quota si paga "on-demand" a token, e il tetto mensile non ferma un lavoro già partito. SuperGrok Lite non include Grok Bot. [verificato: cursor.com/help/grok-bot/plans e /docs/account/teams/pricing, 24/10, per regole e prezzi Teams]; [verificato 14/10: per i prezzi SuperGrok, che vengono da x.ai]. I nomi "SuperGrok" e "SuperGrok Heavy" del compito sono quindi piani legacy: per un'azienda nuova la via è The X Subscription.

### 4.3 Costo stimato per SerSan (4-5 persone)

Stima mia [non verificato], su prezzi verificati. In dollari, IVA esclusa. Non include Claude Team, i crediti API Anthropic né gli altri abbonamenti che SerSan tiene comunque.

| Scenario | Composizione | Al mese |
|---|---|---|
| Prova | 4 o 5 posti Premium | 120-150 $ |
| Uso reale (2 persone che lo usano molto, con routine) | 2 Super + 2 o 3 Premium, più 100-300 $ di crediti come riserva | circa 360-590 $ |
| Squadra di agenti 24/7 (molte routine, chat di gruppo) | 4 o 5 Super, più crediti | 400-500 $ più crediti; con posti Ultra 800-1.000 $ |
| Controlli da impresa (log delle azioni, audit, rete, residenza scritta) | Enterprise | su trattativa, non pubblicato |

Perché la riserva di crediti: le chat di gruppo e le routine consumano più dei messaggi singoli [video V1 §22]; ogni risposta e ogni prova di routine conta [verificato 14/10]. Nel forum di Cursor alcuni utenti raccontano quote settimanali finite in un giorno, 27 $ spesi in dieci minuti dopo la quota, la settimana di Ultra finita in otto ore con 13 Bot [terzi: forum Cursor]. V2, su SuperGrok Heavy, era all'1% [video V2]. Le voci divergono: la quota reale va misurata con la prova gratuita.

---

## 5. Che cosa copre della visione di Alberto

Lista di controllo: `C:/Users/alber/SerSan-AgentOS/ricerca/00-visione-funzionalita.md`. Legenda: **Sì** = funzione del prodotto; **In parte** = si fa con plugin, skill o template, con limiti; **No** = non c'è.

| # | Voce della visione | Grok Bot | Perché |
|---|---|---|---|
| A1 | Tutte le riunioni registrate e trascritte | In parte | Nessun registratore di riunioni proprio verificato; il Bot "che entra in riunione al posto tuo" è solo dichiarato in un post [verificato 14/10]; plugin Gong e Granola; Fireflies solo come skill fatta dall'utente [video V1] |
| A2 | Notion come second brain relazionale | Sì | plugin Notion |
| A3 | Database vettoriale | No | Memoria per Bot e compattazione, nessun indice vettoriale. Si può raggiungere un database esterno (Supabase/pgvector sul server) con un server MCP, a nostra cura |
| A4 | Orchestratore | Sì, ma chiuso | Bot principale che delega; nessun accesso al codice né scelta del modello |
| A5 | Agenti divisi per ruolo (obiettivo: circa 25) | Sì | circa 50 o più Bot per account (limite non chiaro) |
| A6 | Agenti che imparano | In parte | memoria, skill che si correggono, "Teach a task"; nessun ciclo di valutazione |
| A7 | Chat condivisa tra agenti | In parte | gruppi da 2 a 6 Bot, menzioni, passaggi leggibili; non un canale unico con tutti gli agenti. I Team Bots stanno in Slack |
| B1-B4 | Post-call: punti su Slack, opportunità su HubSpot, mail di follow-up, to-do | In parte | Esiste il template "Call Follow-Ups" (Gong/Granola, HubSpot, Gmail, Slack, Notion) [verificato 14/10]; serve una fonte di trascrizioni collegata |
| B5 | Post-call totalmente autonomo, senza approvazione umana | In parte | Le bozze si possono spegnere per Bot, ma le approvazioni del lavoro non presidiato scadono in circa 10 minuti e i termini chiedono revisione umana sulle comunicazioni esterne |
| C1 | Debrief del mattino | Sì | routine a orario |
| C2 | Un agente dentro le call | No (solo dichiarato) | vedi A1 |
| C4 | Dettatura | Sì | dettatura e chiamata vocale con il proprio Bot |
| C5 | Registro di tutte le riunioni dell'azienda, pipeline emersa | In parte | memoria di team nei Team Bots; nessun registro interrogabile |
| C6 | Regole personali lette dagli agenti | Sì | memoria, skill, pagine Notion |
| D1 | Portale CRM fatto in casa, pipeline pesata sullo storico | No | Non è un CRM. I Cloud Agent possono scrivere codice, ma il portale vive altrove (SersanOutreach) |
| D2 | Brief pre-meeting da una email | In parte | ricerca web, plugin CRM e email; i post LinkedIn passano dal browser con login, e un'automazione su LinkedIn va contro i termini di LinkedIn (rischio a carico del cliente) [verificato 14/10]; aperture delle email solo se il sistema di invio è collegato |
| D4 | Slide del brief automatiche | In parte | Google Slides, pagine HTML; nessun collegamento a moda.app trovato |
| D5 | Offerta commerciale automatica | In parte | skill con catalogo e trascrizione |
| E3 | Policy dei token e "banca dei token" | In parte | quota per posto e tetto mensile del team; budget per Bot non trovato |
| F1-F4 | Mappa dei processi dai metadati di Google Workspace | No | nessuna funzione di analisi dei metadati; i plugin Google leggono i contenuti |
| G1-G4 | Analisi di ogni call di vendita, fit score, coaching al sales e al responsabile | In parte | template "Sales Call Coach" su Gong/Granola [verificato 14/10]. Valutare i venditori tocca le regole sul controllo dei lavoratori, con qualunque strumento |
| G5 | Agente vocale che richiama ogni lead entro 90 secondi, 24/7, con voce clonata | **No** | Niente telefonia propria: la chiamata vocale è solo tra l'utente e il suo Bot; un template fa telefonate in uscita con un servizio terzo, su richiesta [verificato 14/10]. Il richiamo in 90 secondi va costruito altrove (ElevenLabs più telefonia) |
| G6 | Impara dai rifiuti | No | |
| G9 | Agenti messi in organigramma | In parte | Bot per persona più Team Bots; nessuna vista a organigramma |
| H6, I3 | Premio mensile, aree senza AI | Fuori dallo strumento | scelte organizzative |

In sintesi: Grok Bot copre bene lo strato "colleghi AI con cui si parla" (A4-A7, C1, C4, C6, routine, Slack, telefono), cioè la parte che i CEO vedrebbero ogni giorno. Non copre lo strato dati che rende utile tutto il resto (A1, A3, C5, D1, F) né l'agente vocale (G5-G6), che restano da costruire comunque.

---

## 6. Può girare contro il server SerSan?

**Come piattaforma, no.** Grok Bot gira solo sui computer cloud di Cursor; installazione in casa, nel proprio perimetro o con un'immagine propria "non sono supportate oggi" [verificato: https://docs.x.ai/grok-bot/security, 24/10]. Il server HPE (RTX 4000, 160 GB di RAM) non può ospitare i Bot, la loro memoria o le loro conversazioni, e i modelli locali sulla GPU non possono essere usati da Grok Bot, che non permette di scegliere il modello.

**Come strumento, in parte.** Il server può essere raggiunto dai Bot in quattro modi:

| Via | Come | Limiti | Fonte |
|---|---|---|---|
| Server MCP remoto | Un server MCP sul nostro server (per esempio davanti a SersanOutreach e al database), esposto in HTTPS | Va pubblicato su internet (tunnel e autenticazione a nostra cura); i dati passano dal cloud USA | [verificato: docs.x.ai/grok-bot/team-bots, 24/10] |
| Webhook | Il server chiama l'indirizzo `POST` di una routine (per esempio "lead nuova") | Almeno 5 minuti tra due esecuzioni di una routine; 200 = partita, non finita | [verificato 14/10] |
| Esecuzione su un computer locale | L'app desktop esiste per Linux; i Bot eseguono comandi su un computer registrato, con approvazione | Che funzioni su un server senza schermo non è documentato [non verificato]; la documentazione parla di "Mac o Windows" | [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10] |
| Rete privata | Client Tailscale o Cloudflare Tunnel installato su ogni computer dei Bot con `Team Setup` | Solo Enterprise | [verificato 14/10] |

Con SersanOutreach sul server, Grok Bot potrebbe fare da "interfaccia di chat" verso i suoi dati attraverso un server MCP. Il cervello (conversazioni, memoria, decisioni) resterebbe comunque nel cloud di Cursor.

**API per integrare.** Un'API pubblica per comandare i Bot da un altro programma non l'ho trovata. Esistono i webhook in ingresso, i server MCP in uscita e, solo Enterprise, un'Admin API per gestire i computer [verificato 14/10].

---

## 7. Rischi

### 7.1 Lock-in

- Prodotto chiuso, solo cloud, nessuna scelta del modello [verificato: cursor.com/help/grok-bot/models e docs.x.ai/grok-bot/security, 24/10].
- **Esportazione dei dati: non trovata** per conversazioni, memorie e skill. Chiudendo l'account i dati vengono cancellati entro 30 giorni [verificato 14/10]. Solo Enterprise ha un'esportazione OpenTelemetry di prompt e risposte, su richiesta [verificato 14/10]. I template portano un Bot solo dentro un altro account Grok Bot.
- Il prodotto ha cambiato piani tre volte in due mesi (solo piani alti all'11 agosto, piani base dal 25-26 agosto, The X Subscription dal 12 ottobre) [verificato 14/10], e la società si è chiamata xAI, SpaceXAI e SpaceXSI [verificato 14/10; SpaceXSI solo da stampa].
- V2 lo dice "poco personalizzabile, prendi quello che c'è" [video V2]: è un'opinione, ma è coerente con l'assenza di codice sorgente.

### 7.2 Privacy e dati

- Computer negli Stati Uniti; il programma di residenza dei dati di Cursor non si applica a Grok Bot per default; un impegno scritto si chiede al commerciale [verificato: docs.x.ai/grok-bot/security, 24/10].
- Archiviazione cloud obbligatoria; non funziona con la vecchia Privacy Mode; la rinuncia all'addestramento segue le impostazioni dell'account Cursor [verificato: docs.x.ai/grok-bot/faq, 24/10].
- Nessun DLP integrato; c'è un gancio di inferenza in beta, solo Enterprise [verificato: docs.x.ai/grok-bot/security, 24/10]. Controlli di rete, log delle azioni e audit sono solo Enterprise.
- I fornitori di modelli sono quelli della lista dei sub-responsabili di Cursor, che cambia nel tempo [verificato: cursor.com/help/grok-bot/models, 24/10]; vi figurano SpaceXAI, Anthropic, OpenAI, Google, Meta e TypeSafe AI [verificato prima del 14/10, non ricontrollato].
- GDPR: la pagina di sicurezza non nomina il GDPR e rimanda al DPA [verificato: docs.x.ai/grok-bot/security, 24/10]. Il DPA di Cursor (aggiornato il 12 febbraio 2025) richiama le clausole contrattuali standard UE (decisione 2021/914, modulo 2) e l'addendum UK [terzi: sintesi di ricerca della pagina https://www.cursor.com/terms/dpa, testo completo non aperto]. Un'analisi legale GDPR di Grok Bot non l'ho trovata; una guida olandese conclude che a un'azienda europea servirebbero DPA e probabilmente una valutazione d'impatto [terzi: https://makeitmatter.studio/en/blog/grok-bot-explained-for-business].
- Disponibilità in Italia e nel Regno Unito: nessuna restrizione pubblicata [terzi: https://www.tryagentsonic.com/articles/grok-bot-availability-countries, 29/09]; l'app supporta l'italiano [verificato 14/10]. Unica esclusione documentata: il tag `@bot` su X non vale per gli account UE e UK [verificato 14/10: `docs.x.ai/grok-bot/tag-on-x`]. Le indagini del Garante irlandese riguardano X e Grok, non Grok Bot [terzi: TechRadar, PBS].
- Tutti i Bot di un utente condividono accessi, cookie e credenziali: un Bot "CFO" e un Bot che scrive su Slack vedono le stesse cose [verificato: docs.x.ai/grok-bot/computer-and-apps, 24/10]. Il 1° ottobre il Bot "CFO" personale di un CEO (Shane Mac, XMTP Labs) ha pubblicato saldi e spese in un canale Slack aziendale, secondo il suo racconto; le sue due versioni della causa non coincidono e manca una conferma indipendente [terzi: Business Insider e Hacker News].
- La scheda dell'App Store dichiara dati collegati all'utente usati anche per pubblicità e marketing dello sviluppatore [verificato 14/10].

### 7.3 Limiti e affidabilità

- Quota settimanale per posto, non condivisa; consumo non prevedibile perché il modello non si vede (§3, §4).
- Pagina di stato di ottobre [verificato: https://status.cursor.com/, 24/10]: 13/10 routine ferme 2 h 37 min; 14/10 degrado di 5 h 18 min con utenti che non raggiungevano il loro computer; 19/10 routine in ritardo per 1 h 6 min e degrado di 19 min; modelli Grok in errore il 15-16/10 (6 h 55 min) e non disponibili il 23-24/10 (41 min). Nessuna percentuale di disponibilità pubblicata.
- Approvazioni del lavoro non presidiato che scadono in circa 10 minuti; routine distanziate di almeno 5 minuti; gruppi di al più 6 Bot; un compito di uso del computer per Bot alla volta [verificato: docs.x.ai/grok-bot/faq, 24/10]; [verificato 14/10].
- Disco del computer da 126 GB secondo V2 [video V2]: per file video grandi serve uno storage esterno.

### 7.4 Contratto

I termini di Grok Bot (aggiornati il 12 ottobre 2026) mettono sul cliente ogni "azione agentica" autorizzata, configurata o permessa, anche quelle che il Bot avvia da solo; chiedono revisione umana prima di comunicazioni esterne, transazioni, cancellazioni, sistemi di produzione e impegni legali; le azioni sono fornite "così come sono" e il fornitore risponde solo per colpa grave o dolo; cancellare un Bot può non cancellare file, sessioni e credenziali condivisi [verificato: https://cursor.com/terms/grok-bot, 24/10]. La legge applicabile non è in quella pagina (rimanda al contratto generale).

---

## 8. Che cosa dicono i video e che cosa risulta oggi

| Affermazione | Video | Stato al 24/10 |
|---|---|---|
| Ogni Bot ha il suo computer | V1 §6 | Un computer per utente condiviso da tutti i Bot, uno schermo per Bot [verificato: docs.x.ai/grok-bot/computer-and-apps] |
| Abbonamento da 20, 100 o 200 $ | V1 §22 | Erano piani Cursor legacy; oggi Premium 30 $, Super 100 $, Ultra 200 $ [verificato: cursor.com/pricing] |
| Finita la quota "sei cotto", non puoi più usarlo | V2 | Si possono comprare crediti prepagati (anche V1 lo mostra) [verificato: cursor.com/help/grok-bot/plans] |
| Bloccato su Grok 4.6, niente Claude né GPT | V2 | Superato: dal 7 ottobre il servizio può usare modelli di terzi, Opus 5.5 compreso, ma l'utente non li sceglie [verificato: cursor.com/help/grok-bot/models] |
| Grok Bot non agisce sul mio computer | V2 (che però mostra un Bot che legge le credenziali AWS dal PC) | Può eseguire comandi sul PC con approvazione; non usa il browser locale già autenticato [verificato: docs.x.ai/grok-bot/computer-and-apps] |
| Disco da 126 GB | V2 | Non documentato |
| Nessun errore, il sistema più solido provato | V2 (opinione) | La pagina di stato registra cinque incidenti di Grok Bot dal 13 al 19 ottobre |
| Grok 4.7 di base, Opus 5.5 per i compiti difficili | V3 | Instradamento confermato in generale, versioni non documentate |
| Team Bot collegato a Slack, Bot principale con la stella | V3 | Confermati [verificato: docs.x.ai/grok-bot/team-bots]; [verificato 14/10] |
| Hermes più flessibile (modelli a scelta, gira sulle proprie macchine), ma più fragile | V2 | Fuori da questo rapporto: Hermes va valutato a parte, da capo, per SerSan |

---

## 9. Lettura per la decisione

Fatti che contano, senza verdetto:

1. Grok Bot è il prodotto più vicino, oggi, all'esperienza "squadra di agenti con nome che si parlano", ed è pronto subito, anche sul telefono e in Slack.
2. Non può stare sul server SerSan e non usa né i modelli locali né i crediti Anthropic; aggiunge una spesa di 120-590 $ al mese circa, che si somma a Claude Team.
3. Copre la parte visibile della visione di Alberto, non la parte dati (registro riunioni, database vettoriale, CRM pesato, mappa dei processi) né l'agente vocale che richiama le lead: quelle vanno costruite comunque, sul server o con altri servizi.
4. I dati di clienti e trascrizioni andrebbero negli Stati Uniti, su un prodotto in beta, senza esportazione documentata, con controlli da impresa solo su trattativa.
5. Un uso a basso rischio è possibile: una prova di un mese con 4-5 posti Premium (120-150 $), su dati non sensibili, per misurare la quota reale e la qualità dei passaggi tra Bot, da confrontare con le alternative (Hermes, sistema Claude-native sul server). Usarlo come base del sistema aziendale invece significa accettare il lock-in del §7.1.

## 10. Fonti

Ufficiali, aperte il 24 ottobre 2026:
- https://cursor.com/pricing
- https://cursor.com/docs/account/teams/pricing
- https://cursor.com/help/grok-bot/plans
- https://cursor.com/help/grok-bot/models
- https://cursor.com/terms/grok-bot (aggiornati il 12/10/2026)
- https://docs.x.ai/grok-bot/security
- https://docs.x.ai/grok-bot/faq
- https://docs.x.ai/grok-bot/computer-and-apps
- https://docs.x.ai/grok-bot/team-bots
- https://status.cursor.com/
- https://x.ai/changelog/bot (403: non letta)

Terzi (stampa e blog):
- The Next Web, 7/10/2026: https://thenextweb.com/news/grok-bot-claude-opus-midjourney-suno-musk
- TeslaNorth, 7/10/2026: https://teslanorth.com/2026/10/07/grok-bot-claude-opus-5-5-midjourney-suno/
- Digital Trends, 22/10/2026: https://digitaltrends.com/phones/grok-bot-can-now-manage-your-calendar-reminders-and-more
- Agent Sonic, 29/09/2026: https://www.tryagentsonic.com/articles/grok-bot-availability-countries
- Make It Matter: https://makeitmatter.studio/en/blog/grok-bot-explained-for-business
- Post X su 0.75.5: https://x.com/ericzakariasson/status/2113743401975963908
- DPA di Cursor (sintesi di ricerca): https://www.cursor.com/terms/dpa

Locali:
- trascrizione del video V1, non pubblicata in questa repo
- trascrizione del video V2, non pubblicata in questa repo
- trascrizione del video V3, non pubblicata in questa repo
- `C:/Users/alber/SerSan-AgentOS/ricerca/00-visione-funzionalita.md` (lista di controllo)
