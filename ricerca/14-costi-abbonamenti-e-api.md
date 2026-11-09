# 14 · Costi: abbonamenti, API e infrastruttura

Listino rilevato il **24/10/2026** per il sistema multi-agente di SerSan.

## Come leggere questo documento

- **Cambio**: 1 EUR = 1,1193 USD, tasso di riferimento BCE del 23/10/2026. Quindi 1 USD = 0,8934 EUR. Ogni cifra in dollari è convertita con questo fattore [non verificato su pagina: la ricerca cita il valore pubblicato da https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html].
- **IVA**: tutti i prezzi sono **IVA esclusa**, salvo dove è scritto diversamente.
- **Etichette**:
  - **[verificato: URL]**: ho letto il dato sulla pagina ufficiale il 24/10/2026.
  - **[non verificato: fonte]**: il dato viene da articoli, comparatori o snippet di ricerca. Va confermato prima di firmare.
  - **[stima]**: è un mio calcolo, con le ipotesi scritte accanto.
- **Budget di ricerca**: ho fatto 20 ricerche e letto 15 pagine. Le voci non coperte sono marcate «non trovato».

---

## Sintesi per i CEO

1. **Le API di Claude costano poco per questo carico.** Il carico tipo richiesto (60 call, 20 brief, 20 offerte, 300 lead, 3.000 mail, 30 post) costa circa **23 $ al mese, cioè circa 20 €** [stima, §1.5]. Moltiplicato per 10 per i loop agentici, resta sotto i 250 $. Gli 800 $ al mese di crediti API bastano con molto margine.
2. **I listini attuali di Anthropic** [verificato: https://platform.claude.com/docs/en/about-claude/pricing]:

   | Modello | Input ($/Mtoken) | Output ($/Mtoken) |
   |---|---|---|
   | Opus 5.5 | 4 | 20 |
   | Sonnet 5.5 | 2 | 10 |
   | Haiku 5.5 (prompt fino a 100k token) | 0,10 | 0,50 |

   La Batch API dimezza il costo. Sui modelli 5.5 la lettura da cache costa il 5% dell'input.
3. **Claude Team premium costa 100 $ a posto al mese con fatturazione annuale (125 $ mensile)** [verificato: https://claude.com/pricing/team].
   - Cinque posti a listino costano circa **447 € al mese** (fatturazione annuale).
   - È un costo che **arriva quando finisce il bundle startup**. La data di scadenza del bundle di SerSan non è nei file.
   - Il programma startup di Anthropic risulta **chiuso alle nuove domande** [verificato: https://claude.com/programs/startups].
4. **Il costo più grande, dopo Claude Team, è il pacchetto di vendita e outbound**: Instantly, Apollo, HubSpot ed ElevenLabs. Il server in sé non è la voce più cara.
5. **L'agente vocale «Andrea»**, con 300 lead al mese e circa 1.000 minuti, costa circa **170 € al mese** [stima, §3.4]:
   - ElevenLabs Pro: 99 $ al mese, include circa 1.238 minuti di Agents (il numero è dedotto dall'ordine della tabella);
   - chiamate Twilio verso i cellulari italiani: 0,0445 $ al minuto;
   - numero mobile italiano: 45 $ al mese.
6. **La corrente del server costa quanto la VM Azure.** Con 350-450 W accesi 24 ore su 24, il consumo è di **255-330 kWh al mese**. A 0,30-0,40 €/kWh, il costo è di **77-131 € al mese** [stima]. Una VM Azure D4s_v5 in West Europe costa circa **150 € al mese** [non verificato: comparatori].
   - Il risparmio, quindi, **non sta nella bolletta**. Sta nella capacità: 160 GB di RAM e una GPU, che su Azure costerebbero molto di più.
7. **I totali del mio scenario «consigliato»**:
   - costi fissi: circa **780 € al mese** finché vale il bundle Claude Team; circa **1.227 € al mese** a regime;
   - costi variabili: circa **160 € al mese**;
   - spegnendo la VM Azure si recuperano circa **150 € al mese**.

   Le tabelle complete sono in §11.

---

## 1. Anthropic

### 1.1 Prezzi API per milione di token (USD)

Fonte di tutta la tabella: [verificato: https://platform.claude.com/docs/en/about-claude/pricing].

| Modello | Input | Scrittura cache 5 min | Scrittura cache 1 h | Lettura cache | Output | Batch input | Batch output |
|---|---|---|---|---|---|---|---|
| **Claude Opus 5.5** | 4,00 | 5,00 | 8,00 | 0,20 | 20,00 | 2,00 | 10,00 |
| **Claude Sonnet 5.5** | 2,00 | 2,50 | 4,00 | 0,10 | 10,00 | 1,00 | 5,00 |
| **Claude Haiku 5.5** (prompt ≤ 100k token) | 0,10 | 0,125 | 0,20 | 0,01 | 0,50 | 0,05 | 0,25 |
| Claude Haiku 5.5 (prompt > 100k token) | 0,50 | 0,625 | 1,00 | 0,05 | 2,50 | 0,25 | 1,25 |
| Per confronto: Sonnet 4.6 | 3,00 | 3,75 | 6,00 | 0,30 | 15,00 | 1,50 | 7,50 |
| Per confronto: Fable 5.1 / Mythos 5.1 | 10,00 | 12,50 | 20,00 | 0,25 | 50,00 | 5,00 | 25,00 |

**Regole che cambiano il conto** [verificato: stessa pagina]:

- **Cache**:
  - la scrittura in cache costa 1,25 volte l'input se dura 5 minuti, 2 volte se dura 1 ora;
  - la lettura costa 0,05 volte l'input su Opus 5.5 e Sonnet 5.5, 0,1 volte sugli altri modelli.
- **Batch API**: sconto del 50% su input e output.
- **Contesto lungo**:
  - dai modelli 4.6 in poi il contesto da 1M token ha il prezzo standard;
  - fa eccezione Haiku 5.5, che sopra i 100k token di prompt paga la tariffa più alta su tutta la richiesta.
- **Residenza dei dati**: `inference_geo: "us"` moltiplica ogni voce per 1,1. Il default `global` usa il prezzo standard.
- **Fast mode**: su Opus 5.5 costa 8 $ in input e 40 $ in output. Non si combina con la Batch API.
- **Tokenizzatore**: dai modelli 4.7 in poi lo stesso testo produce circa il 30% di token in più rispetto ai modelli precedenti.

### 1.2 Strumenti lato server e Managed Agents (USD)

Fonte: [verificato: https://platform.claude.com/docs/en/about-claude/pricing].

| Voce | Prezzo |
|---|---|
| Web search | **10 $ ogni 1.000 ricerche**, più i token dei risultati |
| Web fetch | nessun costo aggiuntivo oltre ai token |
| Code execution | gratis se usata insieme a web search o web fetch. Senza di loro: **1.550 ore gratis al mese** per organizzazione, poi 0,05 $ all'ora per container, con un minimo di 5 minuti |
| Claude Managed Agents | token a listino più **0,08 $ per ora di sessione**, contata solo nello stato `running`. Niente sconto batch |

### 1.3 Abbonamenti Claude per il team

| Piano | Prezzo | Cosa include | Fonte |
|---|---|---|---|
| **Team, posto standard** | 20 $/posto/mese annuale, 25 $ mensile | «più uso di Pro»; da 2 a 150 posti; i tipi di posto si possono combinare | [verificato: https://claude.com/pricing/team] |
| **Team, posto premium** | **100 $/posto/mese annuale, 125 $ mensile** | 5 volte l'uso del posto standard. Accesso a Fable pari al «50% of weekly limits» | [verificato: idem] |
| Team, cosa c'è nel piano | — | Claude Code incluso (la pagina non dice su quali posti); Projects e condivisione dei progetti; connettori, con controlli admin per connettori remoti e locali; SSO e verifica del dominio; extra usage; nessun addestramento sui contenuti per default. **«Up to $500 per month in pooled API credits†»**: la nota † non era leggibile, quindi le condizioni non sono note | [verificato: idem] |
| Enterprise | 20 $/posto/mese annuale, **minimo 20 posti**; l'uso si paga a parte a tariffe API | tutto Team più SCIM, audit log, Compliance API, retention personalizzata, ruoli, offerta pronta per HIPAA | [verificato: https://claude.com/pricing] |
| Pro | 17 $/mese annuale (200 $ anticipati), 20 $ mensile | Claude Code, Projects | [verificato: idem] |
| Max | da 100 $/mese (5x) | 5x o 20x l'uso di Pro | [verificato: idem] |

**Calcolo per SerSan** [stima]:

- Cinque posti premium costano 500 $ al mese con fatturazione annuale (circa **446,70 €**) oppure 625 $ al mese con fatturazione mensile (circa **558,40 €**).
- Enterprise ha un minimo di 400 $ al mese più l'uso a consumo. Per 4 persone non conviene.

### 1.4 Il «bundle startup»

- **Stato del programma**: la pagina ufficiale dice «Our current cohort is now full, and we're not accepting new applications right now» [verificato: https://claude.com/programs/startups].
  - Offre crediti di partner «worth up to $45,000» (la Claude Startup Stack).
  - Per i founder finanziati da un VC partner, fino a 100.000 $ di crediti API aggiuntivi, da richiedere tramite il VC.
  - I crediti valgono solo sull'API di prima parte, cioè la Claude Console, e non su AWS, Google o Azure.
  - La pagina **non** riporta né i posti Team gratuiti né l'importo dei crediti API.
- **Cosa dicono le fonti terze sul lancio del 06/10/2026** [non verificato: https://tech-ish.com/2026/10/07/claude-startups-free-team-year-and-api-credits/, https://cloudinsight.cc/en/blog/claude-for-startups-guide, https://www.androidheadlines.com/2026/10/anthropic-expands-claude-startups-program.html]:
  - Claude Team gratis per **un anno**, fino a **5 posti premium**, solo per organizzazioni nuove su Team;
  - **1.000 $** di crediti API che scadono 6 mesi dopo l'assegnazione;
  - tra le offerte dei partner, ElevenLabs con 12 mesi gratis e 33 milioni di caratteri;
  - domande in pausa o chiuse dal 13/10/2026.
- **Cosa risulta a SerSan**: 5 account Team 5x e **800 $ al mese** di crediti API (dal contesto di Alberto).
  - L'importo non coincide con i 1.000 $ una tantum riportati dalle fonti terze.
  - Potrebbe sommarsi ai «fino a 500 $ al mese di crediti pooled» del piano Team.
  - **Da verificare nella Claude Console**: importo, scadenza dei crediti e data di fine dell'anno gratuito di Team.

### 1.5 Stima del carico di lavoro tipo (prezzi USD di §1.1)

**Formula**: costo = Σ (richieste × (token di input × prezzo input + token di output × prezzo output) / 1.000.000) + strumenti.

| # | Lavoro | Modello | Ipotesi per singola unità | Calcolo | USD al mese |
|---|---|---|---|---|---|
| 1 | 60 call trascritte e analizzate (30 min ciascuna) | Sonnet 5.5 | 6.000 in, 1.500 out (dato del compito) | 60 × (6.000 × 2 + 1.500 × 10) / 10⁶ = 60 × 0,027 | **1,62** |
| 2 | 20 brief pre-meeting | Sonnet 5.5 + web search | 40.000 in, 3.000 out, 10 ricerche [stima] | 20 × (0,08 + 0,03 + 10 × 0,01) | **4,20** |
| 3 | 20 offerte commerciali | Opus 5.5 | 30.000 in (template, trascrizione, listino), 5.000 out [stima] | 20 × (30.000 × 4 + 5.000 × 20) / 10⁶ = 20 × 0,22 | **4,40** |
| 4 | 300 lead arricchiti e qualificati | Sonnet 5.5 + Perplexity Agent API | 8.000 in, 1.000 out, 3 `web_search` Perplexity a 0,0025 $ [stima] | 300 × 0,026 + 900 × 0,0025 | **10,05** (7,80 Claude + 2,25 ricerche; esclusi i token Perplexity, prezzo non trovato) |
| 5 | Agente di posta: 100 mail al giorno, quindi 3.000 al mese | Haiku 5.5 | 2.000 in, 300 out [stima] | 3.000 × (2.000 × 0,10 + 300 × 0,50) / 10⁶ = 3.000 × 0,00035 | **1,05** |
| 6 | 30 post al mese | Sonnet 5.5 | 15.000 in (voce di marca, story bank), 2.000 out [stima] | 30 × (0,03 + 0,02) | **1,50** |
| | **Totale base** | | | | **22,82 $ ≈ 20,39 €** |

**Varianti** [stima]:

- **Batch API** su call, lead e post (lavori che possono aspettare): il totale scende a circa 17,4 $.
- **Lead su Haiku 5.5** invece che su Sonnet: la riga 4 passa da 7,80 $ a 0,39 $ di token Claude.
- **Offerte su Sonnet 5.5** invece che su Opus: la riga 3 passa da 4,40 $ a 2,20 $.
- **Carico reale, consigliato**: il totale base va moltiplicato per 4 per tenere conto di loop di strumenti, contesto ripetuto, retry e orchestratore. A questo si aggiungono:
  - debrief del mattino: 30 × (50.000 in + 2.000 out) su Sonnet, pari a 3,60 $;
  - coaching delle call su Opus: 60 × (8.000 in + 2.000 out), pari a 4,32 $.

  Il totale è **99,20 $ ≈ 88,60 €**.
- **Carico reale, completo**: base × 10, più debrief e coaching, più la mappa mensile dei processi (5 Mtoken in + 0,2 Mtoken out su Sonnet, pari a 12 $). Il totale è **248,12 $ ≈ 221,70 €**.
- In tutti e tre i casi il carico resta **sotto gli 800 $ al mese** di crediti, che valgono 714,70 €. Finché durano i crediti, l'esborso effettivo per le API è 0.

---

## 2. ElevenLabs

### 2.1 Piani

Fonte dei piani: [verificato: https://elevenlabs.io/pricing]. Minuti di Agents e concorrenza: [verificato: https://elevenlabs.io/pricing/api].

| Piano | Mensile | Annuale (equivalente al mese) | Crediti al mese | Minuti TTS circa | Voci PVC | Posti | Minuti Agents inclusi* | Chiamate concorrenti* |
|---|---|---|---|---|---|---|---|---|
| Free | 0 $ | — | 10k | ~10 | 0 | — | 15 | 4 |
| Starter | 6 $ (la scheda mostra 1 $ in promozione) | 5 $ | 30k | ~30 | 0 (IVC sì) | — | 75 | 6 |
| Creator | 22 $ (la scheda mostra 11 $ in promozione) | 18,33 $ | 121k | ~121 | 1 | — | 275 | 10 |
| **Pro** | **99 $** | 82,50 $ | 600k | ~600 | 1 | — | **1.238** | 20 |
| **Scale** | **299 $** | 249,17 $ | 1,8M | ~1.800 | 3 | 3 | **3.738** | 30 |
| **Business** | **990 $** | 825 $ | 6M | ~6.000 | 10 | 10 | **12.375** | 40 |
| Enterprise | su misura | su misura | su misura | — | su misura | su misura | — | — |

\* La pagina API non etichetta ogni riga col nome del piano. L'abbinamento piano-minuti è **dedotto dall'ordine delle righe**: va confermato con ElevenLabs.

### 2.2 Prezzi a consumo

Fonte: [verificato: https://elevenlabs.io/pricing/api].

| Voce | Prezzo |
|---|---|
| **Agents / Conversational AI** | **0,08 $ al minuto** oltre i minuti inclusi; **0,16 $** al minuto oltre il limite di concorrenza |
| LLM ospitato da ElevenLabs | «0,08 $ + uso LLM». Realtime v1 Mini: 0,20 $ in e 6,00 $ out per Mtoken. Realtime v1 Max: 1,80 $ in e 9,00 $ out per Mtoken |
| TTS | Multilingual v2 e v3: 0,08 $ ogni 1.000 caratteri. Flash/Turbo: 0,04 $ ogni 1.000 caratteri |
| Speech to Text | Scribe v2: 0,22 $ all'ora. Scribe v2 Realtime: 0,39 $ all'ora |
| Telefonia | non indicata sulla pagina |

### 2.3 Clonazione della voce e situazione di SerSan

- **Clonazione professionale (PVC)**: non c'è un prezzo a parte. È inclusa da Creator in su: 1 voce su Creator e Pro, 3 su Scale, 10 su Business [verificato: https://elevenlabs.io/pricing].
- **Consenso del collega**: le regole di ElevenLabs sulla verifica della voce di un'altra persona non sono state verificate in questa ricerca [non verificato].
- **Grant aziendale**: SerSan ha già un grant ElevenLabs. Piano, slot PVC e licenza musica sono ancora «da leggere» [verificato: `C:/Users/alber/SerSan-AgentOS/ricerca/05-marketing-e-post.md`, riga 315, che cita STATUS.md del 22/10].

---

## 3. Telefonia per l'agente vocale in Italia

### 3.1 Twilio

| Voce | Prezzo USD | Fonte |
|---|---|---|
| Chiamata in uscita verso cellulare italiano, da origine SEE | **0,0445 $/min** | [verificato: https://www.twilio.com/en-us/voice/pricing/it, prezzi «as of August 2026»] |
| Chiamata in uscita verso cellulare italiano, da USA o Canada | 0,0476 $/min | [verificato: idem] |
| Chiamata in uscita verso cellulare italiano, tariffa di default | 0,3473 $/min | [verificato: idem] |
| Chiamata in uscita verso fisso italiano | 0,0168 $/min | [verificato: idem] |
| Numero verde italiano | 27 $/mese, più 0,4614 $/min in entrata | [verificato: idem] |
| **Numero mobile italiano** | **45 $/mese** | [non verificato: snippet di ricerca della pagina ufficiale https://www.twilio.com/en-us/sip-trunking/pricing/it. Un CSV Twilio senza data riporta 30 $] |
| Numero geografico italiano | **non trovato** | — |
| Requisiti KYC per i numeri italiani | **non trovati** sulla pagina dei prezzi. Di solito serve un «regulatory bundle» con indirizzo e documenti | [non verificato] |

### 3.2 Telnyx e Vonage

- **Telnyx**: la pagina per l'Italia non riporta tariffe italiane [verificato: https://telnyx.com/pricing/call-control/it]. Mostra solo prezzi generici:
  - Voice API 0,002 $/min, più SIP trunking «from 0,0032 $/min»;
  - numeri «1,00 $/number/mo», senza dire se il prezzo vale per l'Italia.
  - Prezzo del numero italiano, tariffe verso i mobili italiani e KYC: **non trovati**. Telnyx rimanda al listino SIP scaricabile o all'endpoint `GET /v2/public/pricing`.
- **Vonage**: **non trovato** (non cercato per limiti di budget).

### 3.3 Piattaforme «tutto compreso»

Tutti i dati di questa tabella vengono da comparatori e blog, spesso affiliati [non verificato: https://www.retellai.com/blog/vapi-vs-bland, https://ainora.lt/blog/ai-voice-agent-cost-per-minute-2026, https://texttolab.com/blog/voice-agent-pricing].

| Piattaforma | Modello di prezzo | Costo al minuto |
|---|---|---|
| Vapi | 0,05 $/min di orchestrazione, componenti a costo | circa 0,07-0,15 $/min tutto compreso |
| Retell AI | ogni componente a consumo | 0,07-0,31 $/min; il suo stimatore dà circa 0,115 $/min |
| Bland AI | Start 0,14 $/min, nessun canone; Build 0,12 $/min + 299 $/mese; Scale 0,11 $/min + 499 $/mese | telefonia spesso a parte |

### 3.4 Stima per «Andrea» [stima]

**Ipotesi**: 300 lead al mese, circa 3 minuti a chiamata, più i tentativi a vuoto, per circa **1.000 minuti al mese**.

| Componente | Calcolo | USD al mese |
|---|---|---|
| ElevenLabs Pro | 99 $, include circa 1.238 minuti | 99,00 |
| Minuti oltre l'incluso | nessuno | 0 |
| LLM: Claude Haiku 5.5 come LLM personalizzato | circa 18.000 token in e 600 token out al minuto: 1.000 min × (18.000 × 0,10 + 600 × 0,50) / 10⁶ | ≈ 2,10 |
| Twilio, chiamate verso cellulari italiani | 1.000 × 0,0445 | 44,50 |
| Twilio, numero mobile italiano | | 45,00 |
| **Totale** | | **≈ 190,60 $ ≈ 170 €** |

**Alternative**:

- Con Retell a circa 0,115 $/min: circa 115 $, più il numero.
- Con Bland Start: circa 140 $, più la telefonia.

---

## 4. Trascrizione delle riunioni

| Prodotto | Free | Piano intermedio | Piano team/business | Fonte |
|---|---|---|---|---|
| **Fireflies** | sì | Pro 10 $/posto annuale, 18 $ mensile | **Business 19 $/posto annuale, 29 $ mensile**; Enterprise 39 $ | prezzi: [non verificato: https://www.techrepublic.com/article/news-best-ai-meeting-note-takers-2026/, https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter]. Sulla pagina ufficiale la tabella dei prezzi non era leggibile; risulta solo che le integrazioni CRM partono da Pro, che Business ha limiti API pooled per il team e registrazione video, e che il prezzo è per posto [verificato: https://fireflies.ai/pricing] |
| **Fathom** | sì | Premium 16 $/utente annuale, 20 $ mensile | Team 15 $ / 19 $ (minimo 2 utenti); Business 25 $ / 34 $ | [non verificato: stesse fonti terze] |
| **Otter** | sì | Pro 8,33 $ annuale, 16,99 $ mensile | Business 19,99 $ / 30 $ | [non verificato: idem] |
| **Granola** | Basic gratis, storico limitato | — | Business 14 $/utente; Enterprise 35 $ | [non verificato: idem] |
| **tl;dv** | gratis, registrazioni cancellate dopo 3 mesi | prezzi a pagamento **non trovati** | — | [non verificato] |
| **Recall.ai (API)** | primi 5 h gratis (PAYG) | **0,50 $ all'ora di registrazione**, più 0,15 $ all'ora di trascrizione | archivio gratis 7 giorni, poi 0,05 $ all'ora di registrazione (tenuta 30 giorni); bot a 4 core +0,10 $/h, bot GPU +1 $/h; startup 0,25 $/h per le prime 10.000 h, su domanda; Launch/Enterprise su misura | [verificato: https://www.recall.ai/pricing] |

**Per 60 call da 30 minuti, cioè 30 ore al mese** [stima]:

- **Recall.ai**: 30 × (0,50 + 0,15) = **19,50 $ ≈ 17,40 €** al mese. È la via per un «secondo cervello» costruito in casa.
- **Fireflies Business con 4 posti**: 76 $ ≈ **67,90 €** al mese. È la soluzione già pronta, senza nulla da costruire in casa.
- **Trascrizione locale**: con Recall.ai solo come bot, si può trascrivere sulla GPU del server. I costi non sono verificati qui.

---

## 5. CRM e strumenti di lavoro

| Prodotto | Piani e prezzi per posto o utente al mese | Fonte |
|---|---|---|
| **HubSpot Sales Hub** | Free 0. Starter circa 15 $ annuale o 20 $ mensile (le fonti variano da 7 a 20 $). **Professional 90 $ annuale, 100 $ mensile, più 1.500 $ di onboarding una tantum**. Enterprise 150 $ più 3.500 $ di onboarding | [non verificato: https://www.sybill.ai/blogs/hubspot-sales-hub-pricing, https://blog.hubspot.com/sales/hubspot-sales-hub-pricing] |
| **Pipedrive** | Lite 14 $, Growth 39 $, Premium 59 $, Ultimate 79 $ (annuale). Lite mensile 24 $. Nessun piano gratuito | [non verificato: https://www.sparrowcrm.com/blogs/pipedrive-pricing] |
| **Attio** | Free fino a 3 posti. Plus 29-35 $, Pro 69-79 $ (annuale; le fonti non concordano). AI ed enrichment a crediti | [non verificato: https://www.stacksync.com/blog/attio-crm-2025-review-features-pros-cons-pricing] |
| **Twenty** | open source, self-host a costo zero. Cloud 9 $/posto | [non verificato: https://moderninbound.com/blog/twenty-crm-vs-attio] |
| **Notion** | Plus 10 $ annuale, 12 $ mensile. **Business 20 $ annuale, 24 $ mensile**, con Notion AI, Agent, Custom Agents e AI Meeting Notes; su Free e Plus l'AI è solo in prova. Gli agenti possono consumare crediti (10 $ ogni 1.000, una sola fonte) | [non verificato: https://www.rock.so/blog/notion-pricing, https://coworker.ai/blog/notion-ai-pricing] |
| **Slack** (prezzi in EUR) | Free: storico di 90 giorni. **Pro 6,75 € annuale, 8,25 € mensile**. **Business+ 15 € annuale, 18 € mensile**. Enterprise+ 45 € | [verificato: https://slack.com/pricing] |
| **Google Workspace** (Italia, EUR, IVA esclusa) | Business Starter 6,80 € annuale, 8,10 € flessibile. Business Standard 13,60 € / 16,20 € (altre fonti: 5,75-6,90 € e 11,50-13,80 €) | [non verificato: https://bulltech.it/blog/microsoft-365-vs-google-workspace] |
| **Microsoft 365 Business** (Italia, EUR, IVA esclusa) | Basic 6,07 € annuale, 7,28 € mensile. Standard 12,13 € / 14,56 €. Premium 19,06 € / 22,87 €. La fonte dice di averli letti su microsoft.com/it-it il 05/08/2026 | [non verificato: https://synsphere.it/notizie/microsoft-365-prezzi-2026-cosa-cambia-pmi/] |

Quale suite di posta usi oggi SerSan (Google o Microsoft): **non trovato**.

---

## 6. Strumenti già in uso o citati

| Prodotto | Piani e prezzi | Fonte |
|---|---|---|
| **Instantly**, invio | Growth 47 $ mensile, 37,60 $ annuale (5.000 email, 1.000 contatti). Hypergrowth 97 $ / 77,60 $ (100-125k email). Light Speed 358 $ / 286,30 $ (500k email, 100k contatti) | [non verificato: https://www.usecarly.com/blog/instantly-review/, https://www.saleshandy.com/blog/instantly-pricing/] |
| **Instantly Leads**, crediti | Growth Credits 47 $ (1.500-2.000 crediti). Supersonic 97 $ (5.000-7.500). Hyper 197 $ (da 10.000). Bundle Starter 94 $, Scale 194 $, Agency 555 $. CRM a parte: 47 $ o 97 $. I crediti scadono dopo 2 mesi sui piani mensili | [non verificato: idem] |
| **Perplexity API** | Search API 5 $ ogni 1.000 richieste (Fast 1 $). Agent API: `web_search` 0,0025 $ a chiamata (Fast 0,001 $); `fetch_url` 0,0005 $; `people_search` e `finance_search` 0,005 $; `sandbox` 0,03 $ a sessione. Token ai prezzi del modello scelto: tier `flex` a 0,5x, `priority` a 2x. **Prezzi per token di Sonar e Sonar Pro: non trovati** sulle pagine ufficiali attuali, che rimandano alle pagine dei modelli dell'Orchestrator e dell'Agent API | [verificato: https://docs.perplexity.ai/getting-started/pricing e https://docs.perplexity.ai/guides/pricing] |
| **Apify** | Free 0 $ (5 $ di uso incluso). Starter 19 $ mensile, 17 $ annuale. Scale 199 $ / 179 $. Business 999 $ / 899 $. Compute unit 0,20 $, 0,16 $ e 0,13 $ secondo il piano. Proxy residenziale 8 $, 7,5 $ e 7 $ al GB. L'uso prepagato non si accumula da un mese all'altro | [verificato: https://apify.com/pricing] |
| **Apollo** | Basic 49 $/posto annuale (59-65 $ mensile). Professional 79 $ / 99 $. Organization 119 $ annuale, minimo 3 posti | [non verificato: https://emelia.io/hub/apollo-io-pricing-guide, https://www.saleshandy.com/blog/apolloio-pricing/] |
| **Proxy residenziali** | Bright Data PAYG circa 4-8,40 $/GB. Decodo (ex Smartproxy) 3,75 $/GB a 3 GB (11,25 $/mese), 2,75 $/GB a 100 GB, PAYG 4-8,50 $. IPRoyal 7-7,35 $/GB PAYG su piccoli volumi, 1,75 $/GB solo da 10 TB, traffico senza scadenza | [non verificato: https://proxyfacts.com/blog/bright-data-pricing, https://proxyfacts.com/blog/decodo-review, https://use-apify.com/blog/iproyal-pricing-plans-2026] |
| **moda.app** | Free 0 $ (fino a 10 membri, 500 crediti a posto, watermark). **Pro 30 $/utente/mese** (6.000 crediti a posto, pooled; MCP fino a 10 task concorrenti). **Ultra 100 $/utente/mese** (22.000 crediti). Enterprise su misura (10+ persone, SSO). Annuale «Save 17%». I crediti non si accumulano | [verificato: https://moda.app/pricing] |
| **Higgsfield** | Le fonti si contraddicono. Prima versione: Starter 19 $, Plus 59 $ (47 $ annuale), Ultra 129 $ (99 $ annuale). Seconda versione: Basic 9 $, Pro 29 $, Max 79 $. Business da circa 65 $/posto. Oggi Alberto usa un Ultra personale | prezzi: [non verificato: https://www.krea.ai/blog/higgsfield-pricing-explained-2026-unlimited-credits-and-real-monthly-costs, https://www.pixara.ai/blogs/higgsfield-ai-pricing]. Ultra personale: [verificato: 05-marketing-e-post.md riga 315] |
| **Canva** | Teams (ora Business) circa 250 $/persona/anno, cioè circa 20,83 $ al mese. Guide più vecchie indicano 10 $/mese con un minimo di 3 posti | [non verificato: https://saasswapper.com/canva-pricing.html] |
| **1Password** | Teams Starter Pack 24,95 $/mese fino a 10 utenti. Business 8,99 $/utente/mese (8 dollari prima del ritocco di marzo 2026) | [non verificato: la ricerca cita la pagina ufficiale https://1password.com/pricing/business, che non ho aperto] |

Costi attuali di Instantly, Perplexity, Apify, IPRoyal e Supabase per SersanOutreach: **non trovati** nel repository [verificato: `C:/Users/alber/SerSan-AgentOS/ricerca/01-sersanoutreach.md` §3.4].

---

## 7. Pubblicazione social

| Prodotto | Prezzi | Fonte |
|---|---|---|
| **Buffer** | Free: 3 canali, 1 posto. Essentials 6 $/canale mensile, 5 $ annuale. Team 12 $ / 10 $ per canale, membri illimitati e approvazioni | [non verificato: https://omidsaffari.com/blog/buffer-review, https://hashtagtools.io/blog/buffer-vs-hootsuite-social-media-scheduler-2026] |
| **Metricool** (in uso) | Starter 25 $ mensile, 20 $ annuale. **Advanced 67 $**: l'approvazione (revisione) parte da qui; non è chiaro se il prezzo sia mensile o annuale. Fascia completa: da 0 a 159 $ annuale, fino a 210 $ mensile | [non verificato: https://outfeed.ai/blog/metricool-vs-hootsuite/, https://checkthat.ai/brands/metricool/pricing]. Uso attuale e necessità della revisione: [verificato: 05-marketing-e-post.md §§ Metricool] |
| **Hootsuite** | Standard 99 $/utente (annuale), Professional 199 $, Advanced 399 $ | [non verificato: idem] |
| **Postiz** | open source, self-host gratuito | [non verificato: non trovato in questa ricerca] |

**Requisiti delle API** (non coperti da questa ricerca) [non verificato]:

- **LinkedIn**: la pubblicazione sulla Pagina aziendale passa per un'app con accesso alla Community Management API, che richiede la revisione di LinkedIn.
- **Instagram**: serve un account Business o Creator collegato a una Pagina Facebook, più un'app Meta con permessi approvati.
- **YouTube**: la Data API ha una quota giornaliera, e un upload consuma molte unità.

Oggi SerSan pubblica Pagina LinkedIn, Instagram e Facebook tramite Metricool, quindi questi requisiti sono già coperti da Metricool [verificato: 05-marketing-e-post.md].

---

## 8. Infrastruttura

| Voce | Prezzo | Fonte |
|---|---|---|
| **Cloudflare Zero Trust** | **gratis fino a 50 utenti**. Pay-as-you-go 7 $/utente/mese. Il 51° utente viene bloccato, non addebitato in automatico | [non verificato: https://costbench.com/software/business-vpn/cloudflare-zero-trust/, https://zerometric.net/research/cloudflare-zero-trust-free-plan-limits-2026/] |
| **Tailscale** | Personal gratis, ma per uso non commerciale (3 o 6 utenti secondo la fonte). Starter/Standard 6-8 $/utente. Premium 18 $/utente annuale, 20 $ mensile | [non verificato: https://www.vendr.com/marketplace/tailscale, https://costbench.com/compare/tailscale-vs-cloudflare-zero-trust/] |
| WireGuard self-host | 0 €: è già usato da SersanOutreach | [verificato: 01-sersanoutreach.md riga 14] |
| **Dominio** | sersan.io esiste già, con il sottodominio outreach.sersan.io. Costo annuo **non trovato** | [verificato: 01-sersanoutreach.md riga 98] |
| **Certificato TLS** | 0 € con Let's Encrypt o con il TLS di Cloudflare | [non verificato] |
| **Backup off-site per 500 GB** | Backblaze B2 6,95 $/TB/mese, cioè circa 3,48 $ per 0,5 TB; senza costi API dal 01/05/2026. Hetzner Storage Box BX11 da 1 TB: **3,20 €/mese** IVA esclusa (5 TB 10,90 €). Azure Blob Hot LRS circa 0,0184-0,0196 $/GB, cioè 9,20-9,80 $ per 500 GB; la variante GRS non è verificata | B2: [non verificato: la ricerca cita https://www.backblaze.com/cloud-storage/pricing]. Hetzner: [non verificato: la ricerca cita la documentazione Hetzner]. Azure: [non verificato: https://www.azure-calc.co.uk/guides/azure-blob-storage-pricing-uk/] |
| **UPS 1500 VA** | APC Smart-UPS 1500 rack 2U (SMT1500RMI2UC) a **1.163-1.293 €** su Yeppon.it (due prezzi per la stessa scheda). Esistono modelli line-interactive più economici, prezzo non verificato | [non verificato: https://www.yeppon.it/collections/smart-ups-1500va-lcd] |

### 8.1 Elettricità in Italia

**Prezzi trovati**:

- **PUN di ottobre 2026** (all'ingrosso, senza oneri, trasporto e imposte): le fonti danno circa **0,21-0,24 €/kWh**. Una riporta una media di ottobre di 223,51 €/MWh; un'altra un parziale di 212,20 €/MWh al 24/10 [non verificato: https://www.finanza.com/finanza-personale/mercati/prezzo-pun-energia-ottobre, https://tariffe.segugio.it/guide-e-strumenti/domande-frequenti/pun-luce-oggi-qual-e-il-valore.aspx].
- **Clienti vulnerabili in maggior tutela** (famiglie, non PMI): riferimento ARERA dal 01/10/2026 di 43,43 centesimi/kWh, imposte incluse [non verificato: https://www.finanza.com/finanza/dati-macroeconomici/prezzi-energia-arera-ottobre-2026].
- **Prezzo medio «tutto compreso» per una PMI a ottobre 2026: non trovato.**

**Ipotesi di lavoro** [stima]: tra **0,30 e 0,40 €/kWh** tutto compreso, IVA esclusa, cioè il PUN più circa 0,08-0,16 € di oneri, trasporto, accise e margine. Il valore centrale è 0,35 €/kWh.

| Assorbimento medio 24/7 | kWh al mese (× 730 h) | a 0,30 €/kWh | **a 0,35 €/kWh** | a 0,40 €/kWh |
|---|---|---|---|---|
| 350 W | 255,5 | 76,65 € | **89,43 €** | 102,20 € |
| 400 W | 292,0 | 87,60 € | **102,20 €** | 116,80 € |
| 450 W | 328,5 | 98,55 € | **114,98 €** | 131,40 € |

Il mini PC che fa da router consuma probabilmente 10-15 W, cioè circa 3-5 € al mese [non verificato].

Dove sarà fisicamente il server (Sardegna, Londra o altrove): **non trovato**. Se fosse nel Regno Unito, la tabella non vale.

---

## 9. Confronto con la VM Azure attuale

| Voce | Valore | Fonte |
|---|---|---|
| VM attuale `vm-apps-01` | 15,6 GiB di RAM. SKU, vCPU, disco e costo: **non trovati** nel repository | [verificato: 01-sersanoutreach.md righe 118 e 141] |
| Standard_D4s_v5 (4 vCPU, 16 GiB), West Europe, Linux, pay-as-you-go | **0,230 $/h, cioè 167,90 $ al mese (730 h), circa 150 €** | [non verificato: https://www.azurespeed.com/AzureVmPricing/Standard_D4s_v5, https://cloudprice.net/vm/Standard_D4s_v5] |
| Standard_D4as_v5 (AMD), West Europe | 0,208 $/h, cioè 151,84 $ al mese, circa 135,70 € | [non verificato: idem] |
| B4ms, West Europe | **non trovato** | — |
| Esclusi dal prezzo | disco gestito, IP pubblico, traffico, backup, Azure Monitor (stimato 40-60 $/mese nel disegno Container Apps, mai attivato) | [verificato: 01-sersanoutreach.md riga 141] |

**Lettura** [stima]:

- Una VM da 16 GB costa circa **150 € al mese** più gli accessori. Il server fisico, solo di corrente, costa **77-131 € al mese**.
- Il server offre però **160 GB di RAM e una GPU da 8 GB**. Una capacità simile su Azure costerebbe molte volte di più; il prezzo di una VM GPU equivalente non è stato cercato.
- Il guadagno vero sta nello spazio per far girare tutto in casa: agenti, database vettoriale, trascrizione locale e SersanOutreach. Sul solo canone mensile il guadagno è piccolo.

---

## 10. Grokbot e Hermes

Li trattano altri rapporti. Non ho cercato il loro costo totale, quindi qui risulta **non trovato**.

---

## 11. Tabelle finali

### Ipotesi dei tre scenari

- **Minimo**: si usa ciò che SerSan ha già, piani gratuiti e self-host. Niente agente vocale. Recall.ai al posto di Fireflies.
- **Consigliato**:
  - il nucleo di strumenti già pronti: trascrizione con Fireflies, CRM leggero, Notion Business, Slack Pro;
  - agente vocale su circa 1.000 minuti al mese;
  - outbound medio.
- **Completo**: tutte le funzioni a volume pieno, HubSpot Professional, outbound Light Speed, voce su 3.000 minuti al mese.
- **Unità**: euro al mese, IVA esclusa, cambio 0,8934. «4 posti» significa le 4 persone del team.

### 11.1 Costi fissi mensili (EUR)

| Voce | Minimo | Consigliato | Completo | Note |
|---|---|---|---|---|
| Claude Team, 5 posti premium | 0 | 0 | 0 | coperti dal bundle; **446,70 a regime** (500 $ con fatturazione annuale) |
| Trascrizione riunioni | 0 (Recall.ai a consumo, vedi 11.2) | 67,90 (Fireflies Business × 4) | 67,90 | Fireflies [non verificato] |
| CRM | 0 (HubSpot Free o Twenty self-host) | 26,80 (HubSpot Starter × 2) | 160,81 (HubSpot Pro × 2) | Pro richiede anche 1.340 € una tantum |
| Notion | 35,74 (Plus × 4) | 71,47 (Business × 4) | 71,47 | Business include Notion AI |
| Slack | 0 (Free) | 27,00 (Pro × 4) | 60,00 (Business+ × 4) | [verificato] |
| Google Workspace | 27,20 (Starter × 4) | 54,40 (Standard × 4) | 54,40 | forse già pagato: non trovato |
| Instantly (annuale) | 33,59 (Growth) | 69,33 (Hypergrowth) | 255,78 (Light Speed) | |
| Apollo (1 posto, annuale) | 0 | 43,78 (Basic) | 70,58 (Professional) | |
| Apify | 0 (Free) | 15,19 (Starter, annuale) | 159,92 (Scale, annuale) | [verificato] |
| ElevenLabs | 0 (grant) | 88,45 (Pro) | 267,13 (Scale) | 0 se il grant copre il piano |
| Numeri Twilio IT | 0 | 40,20 (1 numero mobile) | 80,41 (2 numeri) | |
| Metricool | 17,87 (Starter) | 59,86 (Advanced) | 59,86 | oppure Postiz a 0 |
| moda.app | 0 (Free) | 26,80 (Pro × 1) | 53,60 (Pro × 2) | [verificato] |
| Higgsfield aziendale | 0 | 41,99 (Plus, annuale) | 88,45 (Ultra, annuale) | prezzi incerti |
| Canva | 0 | 0 | 37,22 (Business × 2) | |
| 1Password Teams Starter | 22,29 | 22,29 | 22,29 | |
| Cloudflare Tunnel e Zero Trust | 0 | 0 | 0 | fino a 50 utenti |
| Backup off-site | 3,20 (Hetzner 1 TB) | 3,10 (B2, 0,5 TB) | 6,30 (entrambi) | |
| Elettricità a 0,35 €/kWh | 89,43 (350 W) | 102,20 (400 W) | 114,98 (450 W) | [stima], range ±15% |
| UPS ammortizzato in 60 mesi | 19,40 | 19,40 | 21,50 | 1.163-1.293 € una tantum |
| **Totale fisso con il bundle Claude** | **≈ 248,70** | **≈ 780,20** | **≈ 1.652,60** | |
| **Totale fisso a regime, senza bundle** | **≈ 695,40** | **≈ 1.226,90** | **≈ 2.099,30** | + 446,70 di Claude Team |
| Risparmio se si spegne la VM Azure | −150 | −150 | −150 | D4s_v5 West Europe [non verificato]; SKU reale non trovato |

### 11.2 Costi variabili mensili (EUR) [stima]

| Voce | Minimo | Consigliato | Completo | Formula |
|---|---|---|---|---|
| API Anthropic | 20,39 (carico base) | 88,62 (base × 4 + debrief + coaching) | 221,67 (base × 10 + extra + mappa processi) | §1.5. **Coperte dagli 800 $/mese di crediti finché durano** |
| Bot di registrazione | 17,42 (Recall.ai: 30 h × 0,65 $) | 0 (dentro Fireflies) | 0 | |
| Agente vocale: telefonia e LLM | 0 | 41,63 (1.000 min × 0,0445 $ + 2,10 $ di LLM) | 146,07 (3.000 min × 0,0445 $ + 30 $ di LLM Sonnet con cache) | i minuti ElevenLabs sono dentro il piano |
| Proxy residenziali | 12,51 (2 GB × 7 $) | 31,27 (5 GB × 7 $) | 89,34 (20 GB × 5 $) | i GB al mese sono ipotesi |
| Ricerca web (Perplexity e Claude) | dentro la riga API | dentro la riga API | dentro la riga API | |
| **Totale variabile** | **≈ 50,30** | **≈ 161,50** | **≈ 457,10** | |
| di cui pagato in contanti mentre durano i crediti API | ≈ 29,90 | ≈ 72,90 | ≈ 235,40 | il totale meno la riga API |

Voce **opzionale, esclusa dai totali**: se gli agenti girano come Claude Managed Agents invece che sul server, si aggiungono 0,08 $ per ora di sessione. Con 200 ore al mese sono circa 14,30 €, con 1.000 ore circa 71,50 €.

### 11.3 Costi una tantum (EUR)

| Voce | Importo | Fonte |
|---|---|---|
| UPS APC Smart-UPS 1500 VA rack | 1.163-1.293 | [non verificato: Yeppon] |
| Onboarding di HubSpot Professional (solo scenario completo) | circa 1.340 (1.500 $) | [non verificato] |
| Server, mini PC, rack e cavi | già acquistati | dal contesto |

---

## 12. Cosa non ho trovato e domande aperte

- **Pagine ufficiali senza prezzo leggibile**: Fireflies e Telnyx per l'Italia.
- **Prezzi non verificati su pagina ufficiale**:
  - HubSpot, Pipedrive, Attio, Notion, Google Workspace, Microsoft 365;
  - Instantly, Apollo, Higgsfield, Canva, Metricool, Buffer, Hootsuite;
  - Cloudflare, Tailscale, Azure.
- **Prezzi non trovati per niente**:
  - numero geografico italiano su Twilio; KYC per i numeri italiani; Vonage;
  - prezzo per token di Perplexity Sonar;
  - piani a pagamento di tl;dv;
  - VM B4ms; prezzo PMI dell'elettricità «tutto compreso»;
  - costo del dominio sersan.io; Postiz; requisiti delle API social;
  - Grokbot e Hermes.
- **Bundle startup**:
  - 800 $ al mese di crediti contro i 1.000 $ una tantum riportati dalle fonti terze, contro i «fino a 500 $ al mese di crediti pooled» della pagina Team;
  - data di fine dell'anno gratuito di Team;
  - da leggere nella Claude Console.
- **Grant ElevenLabs**: quale piano copre e quanti minuti di Agents include.
- **Dove sarà il server** (Italia o Regno Unito) e con quale contratto elettrico.
- **Quale suite di posta** usa SerSan e se Notion e Slack sono già pagati.
- **SKU e costo reale della VM Azure `vm-apps-01`**, del VPS WireGuard e del piano Supabase.

---

## Fonti (rilevazione del 24/10/2026)

**Pagine ufficiali lette**:

- https://platform.claude.com/docs/en/about-claude/pricing
- https://claude.com/pricing
- https://claude.com/pricing/team
- https://claude.com/programs/startups
- https://elevenlabs.io/pricing
- https://elevenlabs.io/pricing/api
- https://www.twilio.com/en-us/voice/pricing/it
- https://telnyx.com/pricing/call-control/it
- https://docs.perplexity.ai/getting-started/pricing
- https://docs.perplexity.ai/guides/pricing
- https://fireflies.ai/pricing
- https://slack.com/pricing
- https://www.recall.ai/pricing
- https://moda.app/pricing
- https://apify.com/pricing

**Fonti terze**: sono citate riga per riga accanto al dato.

**File locali**:

- `C:/Users/alber/SerSan-AgentOS/ricerca/01-sersanoutreach.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/05-marketing-e-post.md`
