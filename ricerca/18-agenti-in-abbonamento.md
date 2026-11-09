# 18. La forza lavoro di agenti in abbonamento

**Per:** Michele Sanna e Alessandro Serratt (decisione di budget). **Preparato da:** Alberto Tuveri con un agente di ricerca. **Data di rilevazione:** 24 ottobre 2026.

**Domanda a cui risponde.** Quali agenti si possono comprare in abbonamento, al posto o accanto a ciò che ospitiamo sul server (HPE ProLiant con Quadro RTX 4000), per un'azienda di 4 persone tra UK e Italia, e quanto costano al mese.

**Come leggere le etichette.**
- **[verificato: Sx]** il fatto è scritto sulla pagina ufficiale del produttore o nel file locale indicato, letto il 24/10/2026 salvo diversa data.
- **[terzi: Sx]** voce di terzi (blog, stampa, comparatori), non controllata sulla pagina ufficiale.
- **[non verificato]** dato che non sono riuscito a controllare. **non trovato** dato che non esiste nelle fonti lette.
- **[ipotesi]** numero scelto da noi per fare il conto (volumi, tetti di spesa).

Le fonti S1-S30 sono elencate in fondo (§9). Tutti i prezzi sono in dollari USA, IVA esclusa, salvo dove indicato. Non ho fatto conversioni in euro o sterline.

**Nota sui rapporti precedenti.** Al momento della stesura in `C:/Users/alber/SerSan-AgentOS/ricerca/` non esistono ancora `10-hermes-agent.md`, `11-grokbot.md` e `12-altre-piattaforme.md`.

---

## 0. In breve

1. **Claude resta la base per le persone.** Il piano Team costa 25 $ (Standard) o 125 $ (Premium) a posto al mese con pagamento mensile, 20 $ o 100 $ con pagamento annuale; vale da 2 a 150 posti e include fino a 500 $ al mese di crediti API in comune. Di default i contenuti non vengono usati per l'addestramento [verificato: S1]. SerSan ha già il bundle con 5 account Team 5x, quindi per le persone il costo incrementale è zero.
2. **Claude Enterprise non fa per noi.** Costa 20 $ a posto con un minimo di 20 posti, più l'uso a tariffa API [verificato: S1]. I limiti di spesa per utente e i log di audit ci sono solo lì.
3. **Claude Tag è la "chat condivisa" già pronta (voce A7).** Mette @Claude nei canali Slack, in beta pubblica, sui piani Team ed Enterprise. Il lavoro nei canali si paga a consumo dal saldo dell'organizzazione, con un tetto di spesa mensile; chi lo usa nei canali non ha bisogno di un posto Claude [verificato: S5]. Ogni compito gira in una sandbox temporanea [verificato: S5].
4. **Claude Managed Agents sono agenti ospitati con sandbox, a consumo.** Costano 0,08 $ per ora di sessione attiva più i token; le ore in attesa non si pagano [verificato: S2]. Un agente acceso 24 ore su 24 costa al massimo 58,40 $ al mese di sola esecuzione (730 h × 0,08 $). Opus 5.5 costa 4 $ / 20 $ per milione di token, Sonnet 5.5 2 $ / 10 $, Haiku 5.5 0,10 $ / 0,50 $ [verificato: S2]. Si pagano con gli 800 $ al mese di crediti API che SerSan ha già.
5. **Due limiti di Claude oggi.** Le "routine" (ora "scheduled tasks") sono in anteprima, appartengono al singolo account e non si condividono; girano al massimo una volta l'ora e in automatico scrivono sui connettori [verificato: S3]. I nuovi Projects con coordinatore e thread **non sono offerti sui piani Team** [verificato: S4].
6. **OpenAI Dots esiste dal DevDay del 29/09/2026,** ma è un solo agente per persona, con il suo computer Linux nel cloud [verificato: S6]. In UK e UE si ha solo con ChatGPT Business Premium: il piano Pro è escluso in quelle regioni [verificato: S6]. Business Premium costa 125 $ al mese (100 $ con pagamento annuale), con un minimo di 2 posti [terzi: S8].
7. **Grok Bot è il prodotto più vicino all'organigramma di agenti.** Offre Bot con un nome, chat tra Bot (da 2 a 6), un Bot principale che smista il lavoro, Team Bots dentro Slack, un indirizzo email con un'approvazione per ogni invio e routine con webhook. Si paga con The X Subscription da 30 $ a posto [verificato: S9]. I computer stanno negli USA, l'utente non vede quale modello lavora e tutti i Bot di una persona condividono gli stessi accessi [verificato: S9].
8. **Hermes ospitato esiste: si chiama Hermes Cloud (Nous Portal).** I piani costano 20 $, 100 $ e 200 $ al mese in crediti, e l'istanza si paga a giorni. Tra le regioni ci sono **Londra, Francoforte, Parigi, Amsterdam e Stoccolma** [verificato: S10]. Un'app ufficiale per iOS non è uscita: è solo annunciata come "app mobile" con il round del 7/10 [terzi: S12, S27].
9. **Agenti personali dei video: in UK e in Italia quasi nessuno.** Muse di Meta è disponibile solo negli USA e, dal 23/10, in Giappone [verificato: S14; terzi: S15]. Per Hark Pro (20 $ e 100 $) non è confermata la disponibilità fuori dagli USA [terzi: S16]. Di Tab non ho trovato né prezzo né disponibilità. Lindy, Zapier Agents e Relevance AI si possono usare dall'UE e costano tra 20 $ e 350 $ al mese.
10. **Agente vocale "Andrea" (G5).** Con ElevenLabs Agents, che SerSan ha già, costa 0,08 $ al minuto oltre il pacchetto; il piano Pro (99 $) include 1.238 minuti [verificato: S20]. A parte si pagano l'LLM e la telefonia Twilio: una chiamata dall'area economica europea verso un cellulare italiano costa 0,0445 $ al minuto [verificato: S23]. Retell ha numeri italiani e britannici [verificato: S21].
11. **Tre combinazioni per 4 persone (§7).** Il costo incrementale stimato al mese è tra 310 $ e 440 $ con soli abbonamenti, tra 165 $ e 265 $ con la soluzione ibrida (consigliata) e tra 40 $ e 140 $ con quasi tutto in casa. Elettricità del server e tempo di sviluppo sono esclusi.

---

## 1. Che cosa cerchiamo di comprare

Le voci da A1 a I4 sono quelle di `00-visione-funzionalita.md` [verificato: S29]. In abbonamento ha senso comprare soprattutto cinque cose che il server da solo non dà, o dà con molto lavoro:

| Pezzo | Voci | Perché comprarlo invece di costruirlo |
|---|---|---|
| Chat condivisa dove agenti e persone lavorano insieme | A7, B1, G1, G9 | Va tenuta accesa e collegata a Slack; i prodotti pronti esistono |
| Computer o browser per agente, acceso a PC spento | A4, A5, D2 | Sandbox isolate e gestite; sul server vanno messe in sicurezza a mano |
| Routine e trigger (orari, webhook, eventi) | B1, C1, D2 | Pronti nei prodotti; sul server servono uno scheduler e un ingresso HTTPS |
| Telefono e voce | G5-G7 | Servono numeri italiani, operatore telefonico e bassa latenza: difficile in casa |
| Modelli di frontiera | tutte | Il Quadro RTX 4000 (8 GB) non fa girare modelli di quel livello |

---

## 2. Schede prodotto

### 2.1 Claude (Anthropic): Team, Enterprise, Claude Tag, scheduled tasks, Projects, Managed Agents

| Aspetto | Fatto | Fonte |
|---|---|---|
| Team, prezzo | Standard 25 $/mese (20 $ annuale); Premium 125 $/mese (100 $ annuale), 5 volte l'uso dello Standard; da 2 a 150 posti; tipi di posto mescolabili | [verificato: S1] |
| Team, cosa include | Claude Code e Cowork, Claude Design/Slides/Docs, integrazioni Microsoft 365, ricerca aziendale, fatturazione centrale, SSO, controlli admin sui connettori; **fino a 500 $/mese di crediti API in comune** | [verificato: S1] |
| Team, cosa manca | Log di audit, SCIM, ruoli, conservazione dei dati personalizzata, HIPAA | [verificato: S1] |
| Enterprise | 20 $ a posto con fatturazione annuale e **minimo 20 posti**, più uso a tariffa API; in più: limiti di spesa admin, ruoli, SCIM, audit, Compliance API, allowlist IP | [verificato: S1] |
| Addestramento | "No model training on your content by default" (Team ed Enterprise) | [verificato: S1] |
| DPA | Incluso nei Commercial Terms con le clausole contrattuali standard (SCC); per i clienti UK/SEE la controparte sarebbe Anthropic Ireland | [terzi: S26] |
| Dove stanno i dati | Negli USA; nessuna residenza UE o UK sul piano Team | [terzi: S26] |
| Residenza via API | Esistono solo `inference_geo: "global"` (predefinito) e `"us"`, che costa 1,1 volte; nessuna opzione UE nell'API di prima parte | [verificato: S2] |
| Claude Tag (Slack) | Beta pubblica; solo Team ed Enterprise; @Claude nei canali, nei thread e nei DM; checklist nel thread; memoria per canale; lavori programmati e "osservazione del canale"; connettori, plugin e skill configurati dall'admin per workspace o canale | [verificato: S5] |
| Claude Tag, costi | Nessun costo a posto: il lavoro nei canali e nei DM di gruppo si paga a consumo dal saldo dell'organizzazione, con tetto di spesa mensile; i DM 1:1 consumano il posto di chi scrive | [verificato: S5] |
| Claude Tag, storia | Lanciato il 23/06/2026; crediti promozionali di lancio (2.500 $ per Team con almeno 10 posti) validi fino al 1/09/2026, quindi scaduti | [terzi: S24] |
| Scheduled tasks (ex Routines) | Anteprima di ricerca; Pro, Max, Team, Enterprise; trigger a orario (**al massimo 1 volta l'ora**), API (`POST .../fire` con token), eventi GitHub; 100 esecuzioni pianificate l'ora per account; girano nel cloud di Anthropic; **appartengono al singolo account, non si condividono**; in modalità automatica usano i connettori **anche in scrittura** | [verificato: S3] |
| Scheduled tasks, costi | Consumano l'uso del posto; oltre il limite servono i crediti d'uso | [verificato: S3] |
| Projects (coordinatore + thread paralleli) | Beta pubblica su Pro e Max; **"Projects aren't offered on Team or Enterprise plans yet"**; un progetto appartiene a un solo utente e non si condivide | [verificato: S4] |
| Managed Agents | Agenti ospitati con sandbox, pagati a token + **0,08 $ per ora di sessione** in stato `running`; idle, rescheduling e terminated non si pagano; niente sconto batch; web search 10 $ ogni 1.000 ricerche | [verificato: S2] |
| Managed Agents, lancio | Beta pubblica dall'8/04/2026 | [terzi: S30] |
| Modelli e prezzi API (per milione di token, input/output) | Opus 5.5: 4 $ / 20 $; Sonnet 5.5: 2 $ / 10 $; Haiku 5.5: 0,10 $ / 0,50 $ (fino a 100k token di prompt); Fable 5.1: 10 $ / 50 $ | [verificato: S2] |
| Connettore Metricool già in uso | 4 tool di scrittura su "Needs approval"; regola SerSan: niente scritture su Metricool da Routines, task o loop | [verificato: S29, `05-marketing-e-post.md` §3.7] |
| Agenti con nome e agenti che si parlano | Claude Tag è un solo "@Claude"; nei Projects i thread sono coordinati da una conversazione, ma non sono su Team; Managed Agents: agenti definiti via API, nessuna "chat tra agenti" pronta trovata | [verificato: S4, S5]; il resto **non trovato** |
| Email e telefono propri | **non trovato** | |

### 2.2 OpenAI: ChatGPT Business ed Enterprise, Dots

| Aspetto | Fatto | Fonte |
|---|---|---|
| Business, prezzo | Standard 25 $/mese (20 $ annuale); Premium 125 $/mese (100 $ annuale), 5 volte l'uso e niente limite delle 5 ore; minimo 2 posti, tipi di posto mescolabili | [terzi: S8, con estratto della pagina d'aiuto OpenAI `help.openai.com/en/articles/8792828`, non aperta] |
| Dots, cos'è | Annunciato al DevDay del 29/09/2026: agente sempre acceso su **GPT-6 Astra**, con un computer Linux isolato nel cloud e Chrome per ogni utente; 4.000+ app tramite plugin (skill, MCP, estensioni, OAuth 2.1) | [verificato: S6] |
| Dots, quanti | **Uno per utente** al lancio; dentro un dot lavorano agenti in parallelo; "dot specialisti" con identità propria solo in anteprima enterprise | [verificato: S6] |
| Dots, piani | Il primo dot è incluso in Pro e Business Premium; **Pro non è disponibile in SEE, Svizzera e Regno Unito**; Business Premium copre tutte le regioni supportate | [verificato: S6]; conferme [terzi: S28] |
| Dots, Enterprise | Spento di default; l'admin accende "Use dots (Beta)", l'accesso al PC locale e le regole personalizzate; i dot possono entrare in Slack e Teams con identità propria | [verificato: S7] |
| Dots, routine e trigger | Promemoria e controlli ricorrenti con fuso orario; eventi da Gmail, Slack, PR di GitHub, eventi MCP dei plugin; **webhook generici non documentati**; il dot **non ha un indirizzo email suo** | [verificato: S6] |
| Dots, canali | App ChatGPT (web, desktop, mobile); lo si può chiamare a voce, ma **lui non può chiamare**; Slack e Teams; SMS solo in beta per Pro negli USA | [verificato: S6] |
| Dots, controlli | Quattro livelli di regole (agire, agire se pre-approvato, chiedere, passare la mano); auto-review da parte di un secondo modello; la pausa non ferma i task delegati e le esecuzioni pianificate | [verificato: S6] |
| Dove stanno i dati | Residenza in Europa (SEE + Svizzera) solo per i nuovi clienti Enterprise ed Edu e per l'API; **Business senza residenza UE** secondo la maggior parte delle fonti | [terzi: S25] |
| Workspace agents | Agenti condivisi e configurabili con Google Drive, Calendar, Slack e SharePoint, pianificabili; data di disponibilità generale incerta (21/05 o 06/07/2026) | [terzi: S25] |
| Addestramento e DPA per Business | [non verificato] | |
| API per Dots | **non trovato** (solo plugin e server MCP) | [verificato: S6] |
| Prime 48 ore | Demo dal vivo bloccata; permessi e messaggi persi | [terzi] |

### 2.3 Grok Bot (SpaceXAI, gestito da Cursor): The X Subscription e Team Bots

| Aspetto | Fatto | Fonte |
|---|---|---|
| Prezzo | Dal 12/10/2026 **The X Subscription**: Premium 30 $, Super 100 $, Ultra 200 $ al mese, con quota settimanale comune a Grok, Grok Bot e Cursor, poi crediti prepagati con tetto mensile; per i team **da 30 $ a posto** con SSO e fatturazione unica; Enterprise su trattativa | [verificato: S9, pagine lette il 14/10] |
| Bot con un nome | Nome, descrizione, avatar, conversazione continua, memoria e routine propri; skill, connettori, email e computer sono dell'account | [verificato: S9] |
| Agenti che si parlano | Messaggi diretti tra Bot, **chat di gruppo da 2 a 6 Bot**, menzioni, un "Main Bot" che smista; interruttore di team `Messaging Between Bots` | [verificato: S9] |
| Team Bots in Slack | Beta pubblica dal 28/09; ogni Team Bot è un'app Slack con nome e avatar; memoria di team e note per persona; fino a 25 segreti cifrati | [verificato: S9] |
| Computer | Una microVM Firecracker **per utente, negli USA**, condivisa da tutti i Bot dell'utente: i Bot non sono un confine di sicurezza | [verificato: S9] |
| Routine e webhook | Fino a 50 per Bot, almeno 5 minuti tra due giri; trigger da Slack, GitHub, Linear, Teams, Sentry, PagerDuty, email, **webhook**, X | [verificato: S9] |
| Email | Un indirizzo per utente su `mail.grokbot.com`; **ogni invio chiede approvazione**; massimo 50 destinatari; per i team va accesa dall'admin | [verificato: S9] |
| Integrazioni | Plugin OAuth (Gmail una casella alla volta, Notion, Slack, Shopify annunciato); server MCP propri `Remote HTTPS` | [verificato: S9] |
| Modelli | Il servizio sceglie il modello per ogni compito, anche di altri fornitori (Claude Opus 5.5 compreso); **l'utente non vede quale** | [verificato: S9] |
| UK e UE | Le app desktop e mobile ci sono (italiano compreso); il tag `@bot` su X non vale per account UE e UK; residenza dei dati fuori dagli USA solo con accordo scritto | [verificato: S9] |
| Termini | Il cliente risponde di ogni azione del Bot, anche di quelle avviate da solo; approvazioni e revisione sono "un aiuto" | [verificato: S9] |
| Affidabilità | Routine ferme per 2 h 37 il 13/10; incidente Slack del 1/10 nel racconto di un cliente | [verificato: S9] |
| Controlli che mancano ai team self-serve | Controlli di rete, registrazione delle azioni e audit sono solo Enterprise | [verificato: S9] |

### 2.4 Hermes Agent ospitato: Hermes Cloud (Nous Portal) e l'app iOS

| Aspetto | Fatto | Fonte |
|---|---|---|
| Esiste un Hermes ospitato? | Sì: **Hermes Cloud**, lanciato l'8/07/2026; istanza attiva in "due clic e 60 secondi" | [terzi: S11; annuncio Nous su X riportato in ricerca] |
| Piani Nous Portal | Free 0 $ (solo modelli gratuiti); Plus 20 $/mese con 22 $ di crediti; Super 100 $ con 110 $; Ultra 200 $ con 220 $; riporto massimo 10/50/100 $; 200+ modelli e uso dei tool | [verificato: S10] |
| Prezzo dell'istanza | A giorno, calcolato al secondo quando gira, solo storage quando è ferma; minimo 2 $ di crediti per partire; prezzi esatti solo dentro il Portal | [verificato: S10] |
| Taglie (terzi) | Medium (2 GB RAM, 4 vCPU, 10 sessioni) 0,56 $/giorno, circa 16,80 $/mese; Large (4 GB, 8 vCPU, 20 sessioni) 1,09 $/giorno, circa 32,70 $/mese; 0,03 $/giorno da ferma; inferenza e tool a parte | [terzi: S13] |
| Regioni | Amsterdam, Stoccolma, Mumbai, Parigi, Dallas, Francoforte, Los Angeles, **Londra**, Tokyo, Chicago, Singapore, San Jose, Sydney, Toronto; viene scelta la più vicina con disponibilità | [verificato: S10] |
| Isolamento | Ogni agente in un "hardened container" con sandbox isolate e workspace persistente (file, memoria, configurazione) | [verificato: S10] |
| Team | Agenti per persona o per progetto, controlli di accesso, fatturazione unica dall'organizzazione | [terzi: S11]; la pagina rimanda a "Business" ed "Enterprise" senza dettagli [verificato: S10] |
| Gestione via MCP | Istanze Hermes Cloud elencabili, avviabili e fermabili da un server MCP con OAuth | [verificato: guida nel clone `wd/guides/manage-hermes-cloud-with-mcp.md`] |
| Canali (Telegram, WhatsApp, Slack) su Cloud | **non trovato** per la versione ospitata; nella versione self-hosted c'è un gateway Telegram/WhatsApp | [verificato: clone del repository di Hermes] |
| Dati, DPA, addestramento | **non trovato** (la pagina rimanda a Termini e Privacy senza riassunto) | [verificato: S10] |
| App iOS | **Nessuna app ufficiale** al 20/10; l'app mobile è annunciata con il round di serie B da 90 M$ del 7/10 (valutazione 1,5 miliardi $), senza data; esistono client iOS non ufficiali (Hermex, ERMIS) | [terzi: S12, S27] |

### 2.5 Agenti personali citati nei video, e piattaforme di agenti

| Prodotto | Prezzo | UK / Italia | Cosa fa, in breve | Fonte |
|---|---|---|---|---|
| **Muse** (Meta) | Gratis per la maggior parte degli usi, con abbonamenti senza prezzo nella pagina; un comparatore indica "Power 20 $/mese" | **Solo USA** (e Giappone dal 23/10) | VM sicura con browser, modello Muse Spark, app e WhatsApp, approvazione prima di email e acquisti; i dati non vanno alla pubblicità; opt-out dall'addestramento | [verificato: S14]; [terzi: S15] |
| **Hark Pro** (Hark Labs) | Gratis con tetto, poi 20 $ e 100 $ al mese | Fuori dagli USA **non confermato** | Browser nel cloud per le faccende personali; lanciato il 6/10/2026; hardware nel 2027 | [terzi: S16] |
| **Tab** (Terrasoft, Inc.) | **non trovato** | **non trovato** | "Chiama, naviga e compra", via messaggi | [terzi: S15] |
| **Claude Duet** (Anthropic) | Citato con "Pro 20 $/mese" come app a sé | non trovato | Prodotto non verificato su pagine Anthropic | [terzi: S15] |
| **Gemini Spark** (Google) | Google AI Pro 19,99 $/mese | Paesi selezionati (USA, India, Australia, Canada) | | [terzi: S15] |
| **Lindy** | Team 29,99 $/mese per utente attivo con 3.000 crediti (piani fino a 9.999,50 $); ricariche 10 $ ogni 1.000 crediti; si ferma a crediti finiti; Enterprise su richiesta | Uso UE: GDPR dichiarato; dove stanno i dati: non indicato | Slack come collega, Gmail, 1.500+ integrazioni + MCP, scelta del modello da Team in su, approvazioni; "Phone calls" senza prezzo al minuto; SOC 2, nessun addestramento sui dati | [verificato: S17] |
| **Relevance AI** | Pro 29 $ (19 $ annuale) con 2.500 azioni; Team 349 $ (234 $ annuale) con 7.000 azioni; 80 $ ogni 1.000 azioni in più; secondo un'altra fonte la pagina pubblica mostra solo Enterprise | non trovato | "Forza lavoro" di agenti a consumo di azioni | [terzi: S18] |
| **Zapier Agents** | Zapier Pro 29,99 $/mese (750 task) o 19,99 $ annuale; Team 103,50 $/mese (69 $ annuale), 25 posti, SSO; Agents: 400 attività al mese gratis, 1.500 su Pro, "Pro da circa 33,33 $/mese (annuale)"; massimo 40 attività per esecuzione | non indicato | Ogni trigger, azione, ricerca web o messaggio via estensione Chrome vale 1 attività | [verificato: S19] |

### 2.6 Agenti vocali con numero italiano

| Prodotto | Prezzo | Numeri e telefonia | Modelli | Note | Fonte |
|---|---|---|---|---|---|
| **ElevenLabs Agents** (SerSan ha già ElevenLabs, piano non verificato) | Free 15 min; Starter 6 $ (75 min); Creator 22 $ (275 min); Pro 99 $ (1.238 min, 20 chiamate contemporanee); Scale 299 $ (3.738 min); Business 990 $ (12.375 min, 10 cloni vocali professionali); **0,08 $/min oltre il pacchetto**, 0,16 $ oltre la concorrenza; SMS 0,003 $ | Nessun costo telefonico ElevenLabs: si collega Twilio o un trunk SIP, che fattura a parte | LLM a consumo, dipende dal modello | DPA personalizzato e HIPAA solo Enterprise; residenza UE non indicata | [verificato: S20] |
| **Retell AI** | Infrastruttura voce 0,055 $/min + LLM (Claude 5.5 Sonnet 0,064 $/min, GPT 5.4 mini 0,024 $) + voce (0,015 $; ElevenLabs Flash 0,04 $) + telefonia 0,015 $/min; esempio della pagina: 0,11 $/min | **Italia e UK tra i paesi dei numeri (via Twilio)**; numero 2 $/mese; SIP proprio gratis | Scelta tra GPT, Claude e Gemini | API e webhook inclusi; chiamate in blocco +0,005 $ a chiamata; QA automatico 0,10 $/min dopo 100 min; 20 chiamate contemporanee gratis; DPA solo Enterprise; SOC 2 | [verificato: S21] |
| **Vapi** | 0,05 $/min di piattaforma, modello, voce e telefonia a parte; tutto compreso 0,14-0,33 $/min | non verificato | A scelta | | [terzi: S22] |
| **Bland AI** | 0,14 $/min tutto compreso (Start); 0,12 $/min + 299 $/mese (Build) | non verificato | | | [terzi: S22] |
| **Synthflow** | Secondo una fonte solo Enterprise, da 30.000 $/anno; fonti vecchie: 29 $/mese per 50 minuti | non verificato | | | [terzi: S22] |
| **Twilio Italia** (telefonia sotto ElevenLabs o Vapi) | Uscita verso fissi italiani 0,0168 $/min; verso cellulari italiani **0,0445 $/min dal SEE** (0,3473 $/min senza indicazione di origine); numero verde 27 $/mese; prezzo dei numeri locali solo nel CSV, non letto | Requisiti d'identità e d'indirizzo: non indicati nella pagina | | Dati di agosto 2026 | [verificato: S23] |

---

## 3. Confronto per caratteristica (piattaforme di agenti "da lavoro")

| | Claude (Team + Tag + Managed Agents) | ChatGPT Business Premium + Dots | Grok Bot (X Subscription) | Hermes Cloud | Lindy | Zapier Agents |
|---|---|---|---|---|---|---|
| **Prezzo** | 25-125 $ a posto; Tag a consumo; Managed Agents 0,08 $/h + token [S1, S2, S5] | 125 $ a posto, minimo 2 posti [S8 terzi] | da 30 $ a posto [S9] | 20-200 $ di crediti + istanza a giorni [S10] | 29,99 $ a utente [S17] | da 29,99 $ [S19] |
| **UK / UE** | Sì [S1] | Sì con Business Premium; no con Pro [S6] | App sì; computer negli USA [S9] | Sì, regioni a Londra e in UE [S10] | GDPR dichiarato [S17] | non indicato |
| **Piano team** | Team 2-150 posti [S1] | Business, minimo 2 posti [S8] | Team self-serve ed Enterprise [S9] | Org con fatturazione unica [S11 terzi] | Team con crediti in comune [S17] | Team, 25 posti [S19] |
| **Dove stanno i dati** | USA [S26 terzi] | USA per Business [S25 terzi] | USA [S9] | Regione scelta automaticamente [S10] | non indicato | non indicato |
| **DPA** | Nei Commercial Terms [S26 terzi] | non verificato | Trust di Cursor (non verificato) | non trovato | non indicato | non indicato |
| **Addestramento** | No di default [S1] | non verificato | Segue le impostazioni Cursor [S9] | non trovato | No [S17] | non indicato |
| **Agenti con nome** | Un "@Claude" in Slack; agenti API [S5] | 1 dot per utente [S6] | Sì, molti Bot [S9] | Sì, un agente per istanza [S10] | Sì, più agenti (non verificato) | Sì (non verificato) |
| **Agenti che si parlano** | non trovato su Team | Subagent dentro il dot [S6] | Sì, chat da 2 a 6 Bot [S9] | non trovato su Cloud | non indicato | non indicato |
| **Computer o browser** | Sandbox per sessione [S2, S5] | VM Linux + Chrome per utente [S6] | microVM per utente [S9] | Container per agente [S10] | non indicato | Browsing via estensione Chrome [S19] |
| **Routine e webhook** | Orario (al massimo ogni ora), API `/fire`, GitHub [S3]; Tag: lavori programmati [S5] | Orari ed eventi; webhook non documentati [S6] | Orari, eventi, webhook [S9] | non trovato | non indicato | Trigger Zapier [S19] |
| **Canali** | Slack (Tag), app [S5] | App, Slack, Teams, voce in entrata [S6] | App, Slack, email, X fuori UE [S9] | non trovato | Slack, email [S17] | estensione Chrome [S19] |
| **Integrazioni (Gmail, Calendar, HubSpot, Notion, LinkedIn, Metricool)** | Connettori MCP; Metricool già collegato [S29]; altri non verificati qui | 4.000+ app via plugin [S6] | Plugin OAuth: Gmail, Notion, Slack [S9] | "50+ connettori" [terzi] | 1.500+ integrazioni + MCP [S17] | Catalogo Zapier (non verificato) |
| **Modelli** | Claude, a scelta [S2] | GPT-6 Astra [S6] | Scelti dal servizio, invisibili [S9] | 200+ a scelta [S10] | Scelta da Team [S17] | non indicato |
| **API per SersanOutreach** | Managed Agents API; `/fire` dei task; connettori MCP remoti [S2, S3] | Solo plugin MCP con OAuth 2.1 [S6] | Webhook in entrata; MCP Remote HTTPS [S9] | MCP con OAuth per gestire le istanze | non indicato | Webhook Zapier (non verificato) |

**LinkedIn.** Nessuna piattaforma offre un'integrazione ufficiale per mandare messaggi LinkedIn. Grok Bot e Dots ci arrivano solo con il browser dell'agente: una guida del produttore di Grok Bot descrive richieste di collegamento LinkedIn [verificato: S9]. Per SerSan la strada LinkedIn resta SersanOutreach, con l'estensione Chrome e l'approvazione umana [verificato: S29, `01-sersanoutreach.md`].

---

## 4. Come si collegano a SersanOutreach

SersanOutreach espone 269 endpoint REST e due server MCP: `mcp_server/` in sola lettura (19 tool) e `mcp_operator/`, che scrive in modo controllato (14 operazioni, mai approvazione in blocco né invio). Ha anche un webhook pubblico `POST https://outreach.sersan.io/api/webhooks` [verificato: S29, `01-sersanoutreach.md` §5].

| Piattaforma | Come parla con SersanOutreach | Cosa serve |
|---|---|---|
| Claude Team / Claude Tag | `mcp_server` e `mcp_operator` aggiunti come connettori MCP remoti, a livello di organizzazione o di canale Slack | Esporli in HTTPS con autenticazione (oggi il server MCP installato non parte) [verificato: S29 riga 82] |
| Claude Managed Agents | Lo stesso MCP, oppure tool personalizzati che chiamano la REST API; SersanOutreach può aprire una sessione dell'agente via API | Chiave API (gli 800 $ di crediti) |
| Scheduled tasks | SersanOutreach chiama `POST /v1/claude_code/routines/<id>/fire` con un token (per esempio "nuova risposta calda") | Header beta `experimental-cc-routine-2026-04-01`; il testo arriva marcato come dato non fidato [verificato: S3] |
| Dots | Solo come plugin MCP con OAuth 2.1 | Server MCP pubblico con OAuth 2.1 [verificato: S6] |
| Grok Bot | Routine su webhook; server MCP `Remote HTTPS` nei Team Bots | Segreti del Bot (fino a 25) [verificato: S9] |
| Hermes Cloud | MCP o API dell'agente (Hermes è open source) | non verificato per la versione ospitata |
| Agenti vocali (Retell, ElevenLabs) | Il webhook del modulo lead chiama l'API della piattaforma vocale per la chiamata entro 90 secondi; l'esito torna via webhook a SersanOutreach | Retell: API e webhook inclusi [verificato: S21]; ElevenLabs: API [non verificato in questa sessione] |

---

## 5. Cosa comprare per quale voce (A1-I4)

"In casa" vuol dire sul server SerSan o con quello che abbiamo già: Claude Team, gli 800 $/mese di API, ElevenLabs, moda.app e i connettori.

| Voce | Bisogno | Da comprare (consigliato) | Prezzo | In casa | Nota |
|---|---|---|---|---|---|
| A1 | Registrare e trascrivere tutte le riunioni | Fireflies, come previsto nella visione | non verificato in questo rapporto | Whisper sul Quadro RTX 4000 | Avviso a chi partecipa |
| A2 | Second brain relazionale | Niente: Notion (già collegato) | prezzo Notion non verificato | — | |
| A3 | Database vettoriale | Niente | — | pgvector su Postgres nel server | Dati dei clienti in casa |
| A4 | Orchestratore | Claude Managed Agents per gli agenti che servono sempre accesi | 0,08 $/h + token [S2] | Hermes self-hosted o Claude Agent SDK sul server | Alternative a pagamento: Hermes Cloud (20 $ + ~17-33 $/mese), Grok Bot (30 $ a posto) |
| A5-A6 | Agenti di raccolta, pulizia e indicizzazione | Niente | — | Sul server, con Haiku 5.5 (0,10 $ / 0,50 $ per milione di token) | Lavori lunghi e ripetitivi: in casa costano meno |
| A7 | Chat condivisa tra agenti e persone | **Claude Tag in Slack** | a consumo, con tetto [S5] | Agenti del server come app Slack | Per molti agenti con un nome che si parlano, l'unico prodotto pronto è Grok Bot [S9] |
| B1 | Punti e next step nel canale del cliente | Claude Tag o Managed Agent attivato dal webhook di Fireflies | a consumo | Agente sul server | |
| B2 | Opportunità sul CRM | Niente | — | SersanOutreach (deals) | HubSpot non verificato |
| B3 | Mail di follow-up | Niente: bozza via connettore Gmail con approvazione | — | | Grok Bot chiede approvazione per ogni invio [S9] |
| B4 | To-do al team | Niente: Notion | — | | |
| B5 | Autonomia | Decisione interna | — | | Gli scheduled tasks scrivono sui connettori senza chiedere [S3] |
| C1 | Debrief del mattino | Scheduled task Claude (incluso nel posto) | 0 $ extra [S3] | Cron sul server | Massimo una volta l'ora, legato a un account |
| C2, C3, C5, C6 | Analisi di tutte le riunioni con le nostre regole | Fireflies + Claude Team | Fireflies non verificato | Trascrizioni nel server, regole in Notion | |
| C4 | Dettatura | non trovato prodotto dedicato in questa ricerca | — | Whisper locale | |
| D1 | Pipeline pesata | Niente | — | SersanOutreach + Claude Code | |
| D2 | Brief pre-meeting | Managed Agent con web search | 10 $ ogni 1.000 ricerche + token [S2] | Enrich di SersanOutreach (Perplexity) | |
| D3-D4 | Slide del brief | Niente: moda.app e Canva già presenti | — | | |
| D5 | Offerta automatica | Niente: Claude Team (Docs/Slides) | incluso [S1] | | |
| E3 | Banca dei token | Tetto di spesa Claude Tag [S5]; limiti per utente solo su Enterprise [S1] | — | Contatori in SersanOutreach o nel server | Su Team non ci sono limiti di spesa per persona |
| F1-F4 | Mappa dei processi da Google Workspace | **nessun prodotto trovato** in questa ricerca | — | Script sui metadati di Workspace | |
| G1-G4 | Analisi delle call di vendita, coaching | Fireflies + Claude; QA automatico Retell (0,10 $/min) | [S21] | Agente sul server | Valutare i lavoratori: verificare con un legale (Statuto dei lavoratori, AI Act) |
| G5 | "Andrea": richiamata entro 90 secondi | **ElevenLabs Agents** (già in abbonamento) + numero Twilio italiano; alternativa Retell | 0,08 $/min + LLM + 0,0445 $/min verso cellulari [S20, S23] | — | Va dichiarato che è un'AI; consenso scritto per clonare la voce |
| G6-G8 | Imparare dai rifiuti, risalire alle lead chiuse | Niente: trascrizioni + valutazioni | — | Server | |
| G9 | Organigramma di agenti | Niente | — | Registro degli agenti in Notion | Grok Bot ha questa forma pronta [S9] |
| H1-H7 | Formazione, ambassador, premio | Niente: i posti Claude ci sono già | — | | |
| I1-I4 | Policy, aree senza AI | Niente | — | | |

---

## 6. Prodotti da non comprare oggi, con il motivo

| Prodotto | Motivo | Fonte |
|---|---|---|
| Claude Enterprise | Minimo 20 posti a 20 $ più l'uso: per 4 persone pagheremmo 16 posti vuoti | [verificato: S1] |
| ChatGPT Pro con Dots | Non disponibile in UK e SEE | [verificato: S6] |
| Muse | Solo USA e Giappone | [verificato: S14; terzi: S15] |
| Hark Pro, Tab | Disponibilità fuori dagli USA non confermata o non trovata | [terzi: S15, S16] |
| Projects di Claude Code | Non offerti sui piani Team | [verificato: S4] |
| Synthflow | Secondo una fonte solo Enterprise da 30.000 $/anno | [terzi: S22] |

---

## 7. Tre combinazioni: costo mensile per 4 persone

**Ipotesi di volume per tutti e tre i conti** [ipotesi]:
- 4 persone;
- 300 chiamate ai lead al mese da 3 minuti, cioè 900 minuti di voce;
- 10 agenti di background, ciascuno attivo un'ora al giorno, cioè 300 ore di sessione al mese;
- token entro gli 800 $/mese di crediti API già disponibili;
- prezzi di listino con pagamento mensile.

**Formula generale:** `Costo = Σ (posti × prezzo del posto) + Σ (ore × 0,08 $) + token + minuti voce × tariffa + telefonia + numeri − ciò che SerSan paga già`.

**Esclusi da tutti i conti:** elettricità e connettività del server, Fireflies, Notion e Slack (prezzi non verificati qui), il costo attuale di Azure per SersanOutreach (in `01-sersanoutreach.md` risulta "non trovato") e il prezzo mensile del numero locale Twilio (presente solo nel CSV, non letto).

### 7.1 Solo abbonamenti (il server non fa da piattaforma per gli agenti)

| Voce | Formula | $/mese |
|---|---|---|
| Claude Team, 4 posti Premium | 4 × 125 | 500 |
| Claude Tag (chat condivisa in Slack) | tetto di spesa [ipotesi] | 150 |
| Scheduled tasks Claude (debrief, brief) | inclusi nell'uso del posto [S3] | 0 |
| Grok Bot, 4 posti The X Subscription Premium (agenti con nome, computer, email, Team Bots) | 4 × 30 | 120 |
| ElevenLabs Agents Pro | 99 (1.238 min ≥ 900) | 99 |
| Twilio, uscita verso cellulari italiani | 900 × 0,0445 | 40 |
| Zapier Pro (collegamenti), facoltativo | 29,99 | 30 |
| **Totale di listino** | | **≈ 909-939 $ + numero Twilio** |
| **Incrementale per SerSan** | Claude Team già nel bundle (0); ElevenLabs già in abbonamento (0-99) | **≈ 310-440 $** |

Variante con Dots al posto di Grok Bot: ChatGPT Business con 1 posto Premium e 1 Standard (minimo 2 posti) = 125 + 25 = **150 $** al mese, per un solo dot [S6, S8].

**Pro:** pronto in pochi giorni. **Contro:** i dati di agenti e clienti stanno in più cloud negli USA [S9, S26]; con Grok Bot non si vede quale modello lavora [S9]; SersanOutreach resta su Azure.

### 7.2 Ibrida (consigliata)

Persone su Claude Team; chat comune con Claude Tag; pochi agenti sempre accesi con Managed Agents; tutto il resto (SersanOutreach, orchestratore, database vettoriale, trascrizioni) sul server.

| Voce | Formula | $/mese |
|---|---|---|
| Claude Team, 4 posti Premium | 4 × 125 (già nel bundle) | 500 (incrementale 0) |
| Claude Tag | tetto di spesa [ipotesi] | 100 |
| Claude Managed Agents | 300 h × 0,08 | 24 |
| Token di agenti e server | entro gli 800 $ di crediti | 0 incrementale |
| Server: SersanOutreach + orchestratore + pgvector + Whisper | licenze 0; elettricità non stimata | 0 + elettricità |
| ElevenLabs Agents Pro + Twilio | 99 + 900 × 0,0445 | 139 (incrementale 40-139) |
| **Totale di listino** | | **≈ 763 $ + numero + elettricità** |
| **Incrementale per SerSan** | | **≈ 165-265 $ + numero + elettricità** (meno il costo Azure che si spegne) |

**Pro:** dati dei clienti e lavori lunghi in casa; si compra solo ciò che il server non sa fare bene (chat in Slack, sandbox, voce). **Contro:** l'orchestratore e i collegamenti vanno costruiti; Claude Tag è in beta [S5].

### 7.3 Quasi tutto in casa

| Voce | Formula | $/mese |
|---|---|---|
| Claude Team, 4 posti Premium (per le persone) | 4 × 125 (già nel bundle) | 500 (incrementale 0) |
| Agenti, chat tra agenti, routine | sul server, con i crediti API | 0 incrementale entro 800 $ |
| Voce: ElevenLabs + Twilio (o trunk SIP italiano, non verificato) | 99 + 40 | 139 (incrementale 40-139) |
| **Totale di listino** | | **≈ 639 $ + numero + elettricità** |
| **Incrementale per SerSan** | | **≈ 40-140 $ + numero + elettricità + tempo di sviluppo** |

**Pro:** costo minimo, massimo controllo sui dati. **Contro:** tutto il lavoro di costruzione, sicurezza e manutenzione è nostro: chat tra agenti, sandbox, routine, monitoraggio. La telefonia resta comunque un servizio esterno.

### 7.4 Quanto pesano i consumi (per tarare i tetti)

| Consumo | Conto | Fonte |
|---|---|---|
| Un Managed Agent sempre acceso | 730 h × 0,08 $ = 58,40 $/mese, token esclusi | [S2] |
| 800 $ di crediti in Sonnet 5.5 | per esempio 200 milioni di token in entrata (400 $) + 40 milioni in uscita (400 $) | [S2] |
| Una chiamata "Andrea" da 3 minuti oltre il pacchetto ElevenLabs | 3 × 0,08 + 3 × 0,0445 ≈ 0,37 $, LLM escluso | [S20, S23] |
| La stessa chiamata con Retell | circa 3 × 0,11 = 0,33 $ (esempio della pagina) + 3 × 0,015 di telefonia | [S21] |

---

## 8. Domande aperte

1. Cosa include esattamente il "Claude Team startup bundle" con 5 account Team 5x (durata, rinnovo)? E gli 800 $/mese di crediti API sono gli stessi "fino a 500 $ di crediti API in comune" del piano Team, oppure si sommano [S1]?
2. Il saldo d'uso di Claude Tag si può pagare con i crediti API o va finanziato a parte [S5]?
3. Quale piano ElevenLabs ha SerSan, e include gli Agents con i minuti necessari?
4. Quanto costa un numero locale o mobile italiano su Twilio, e quali documenti chiede l'operatore?
5. ChatGPT Business: uso dei dati per l'addestramento, DPA e residenza UE (le fonti di terzi non sono d'accordo) [S25].
6. Hermes Cloud: prezzi ufficiali delle taglie, DPA, canali disponibili nella versione ospitata, data dell'app iOS.
7. Slack: che piano ha SerSan? Claude Tag e Team Bots di Grok lo richiedono.
8. Agente vocale: verifica legale su dichiarazione AI, clonazione della voce di un collega e Registro delle opposizioni per le chiamate in uscita.
9. I rapporti 10, 11 e 12 (Hermes, Grokbot, altre piattaforme), quando esistono, vanno confrontati con questo per allineare i prezzi.

---

## 9. Fonti

Rilevate il 24/10/2026 salvo diversa indicazione.

| Id | Fonte | Tipo |
|---|---|---|
| S1 | https://claude.com/pricing | ufficiale |
| S2 | https://platform.claude.com/docs/en/about-claude/pricing (sezioni "Model pricing", "Data residency pricing", "Claude Managed Agents pricing") | ufficiale |
| S3 | https://code.claude.com/docs/en/routines ("Automate work with scheduled tasks") | ufficiale |
| S4 | https://code.claude.com/docs/en/claude-projects | ufficiale |
| S5 | https://claude.com/docs/claude-tag/overview | ufficiale |
| S6 | Fonti OpenAI lette via proxy il 1/10/2026: openai.com/index/introducing-dots, help.openai.com 20001529/20001530/20001554, learn.chatgpt.com/docs/dots | da fonti ufficiali |
| S7 | https://help.openai.com/en/articles/20001554-manage-dots-in-chatgpt-workspaces (letta via r.jina.ai, perché l'accesso diretto risponde 403) | ufficiale |
| S8 | Prezzi di ChatGPT Business: https://help.openai.com/en/articles/8792828-chatgpt-business-overview (solo estratto nei risultati di ricerca), https://appwrite.io/blog/post/chatgpt-business-premium-seats-pricing-and-whats-new, https://justinmckelvey.com/blog/chatgpt-business-pricing | terzi + estratto ufficiale |
| S9 | Pagine x.ai, docs e help di Cursor, forum Cursor del 12/10 (lette il 14-15/10/2026) | da fonti ufficiali |
| S10 | https://portal.nousresearch.com/cloud | ufficiale |
| S11 | https://lucaberton.com/blog/what-is-hermes-cloud-nous-portal/ (22/07/2026); post di Nous su X https://x.com/NousResearch/status/2074878754485043333 (solo estratto) | terzi |
| S12 | https://runtimewire.com/article/nous-research-90m-series-b-hermes-agent (7/10/2026) | terzi |
| S13 | https://openclawlaunch.com/guides/nous-portal, https://www.vantasoft.com/insights/hermes-agent-pricing, https://mausbot.com/blog/managed-hermes-agent-hosting (taglie dell'istanza) | terzi |
| S14 | https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/ (8/09, aggiornata il 30/09/2026) | ufficiale |
| S15 | https://ordalin.com/agents/personal (comparatore; Muse controllato il 24/10) | terzi |
| S16 | https://thenextweb.com/news/hark-pro-agent-hardware-europe, https://www.usecarly.com/blog/hark-ai/ | terzi |
| S17 | https://www.lindy.ai/pricing | ufficiale |
| S18 | https://www.getmacha.com/blog/relevance-ai-pricing-explained, https://automationatlas.io/answers/relevance-ai-pricing-explained-2026/ | terzi |
| S19 | https://zapier.com/pricing | ufficiale |
| S20 | https://elevenlabs.io/pricing/agents | ufficiale |
| S21 | https://www.retellai.com/pricing | ufficiale |
| S22 | https://stackbinary.io/insights/voice-ai-pricing-per-minute-2026, https://builts.ai/blog/vapi-vs-bland-ai-vs-retell-ai/, https://tested.media/retell-vs-vapi-vs-bland-vs-synthflow/ | terzi |
| S23 | https://www.twilio.com/en-us/voice/pricing/it (dati di agosto 2026) | ufficiale |
| S24 | https://www.techfinitive.com/introducing-slacks-newest-team-member-claude-tag/, https://www.cio.com/article/4189063/, https://www.eesel.ai/blog/claude-tag-pricing | terzi |
| S25 | https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt (solo estratto), https://www.spotdev.co.uk/blog/ai-data-residency-uk-chatgpt-claude-gemini-grok-muse, https://agent-works.ai/alternatives/chatgpt-team-alternatives-eu, https://www.waimakers.com/en/resources/ai-data-security/openai-eu | terzi + estratto ufficiale |
| S26 | https://compound.law/en-DE/tools/claude-team-gdpr/, https://www.heuking.de/en/news-events/newsletter-articles/detail/anthropic-claude-in-the-enterprise-data-protection-and-compliance-requirements-for-the-use-of-generative-ai.html | terzi |
| S27 | https://heraldapp.dev/best/hermes-agent-ios-apps, https://apps.apple.com/us/app/hermex/id6767006319 | terzi |
| S28 | https://www.tryagentsonic.com/articles/openai-dots-uk-eu-availability, https://www.remotehumans.ai/ai-tools/openai-dots-for-business | terzi |
| S29 | `C:/Users/alber/SerSan-AgentOS/ricerca/00-visione-funzionalita.md`, `01-sersanoutreach.md`, `05-marketing-e-post.md` | locale |
| S30 | https://www.verdent.ai/guides/claude-managed-agents-pricing, https://imisofts.com/blog/claude-managed-agents-pricing/ | terzi |
