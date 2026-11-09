# 16 — GDPR, AI Act e regole operative per il sistema di agenti SerSan

**Data di rilevazione:** 2026-10-24. **Per chi:** documento ai CEO (Alessandro Serratt, Michele Sanna).
**Cosa c'è qui:** le regole da rispettare, in pratica, per il sistema multi-agente descritto in `00-visione-funzionalita.md`. SerSan è una UK Ltd, ha il team in Italia e clienti sia UK che italiani.
**Avvertenza:** questa è una mappa operativa. Non sostituisce un parere legale. I punti che lo richiedono sono elencati al §7.

**Legenda.**
- `[verificato: ufficiale — URL]`: letto su una pagina dell'autorità o del fornitore (Garante, EDPB, ICO, Commissione UE, AGCOM, Anthropic, ElevenLabs, xAI).
- `[verificato: secondaria — URL]`: riportato da studi legali o testate, senza la pagina ufficiale.
- `[non verificato]`: deduzione o proposta di questo rapporto.
- `non trovato`: il dato non è emerso dalle ricerche.

---

## Sintesi per decidere (10 punti)

1. **L'agente vocale «Andrea» è il pezzo più rischioso.** Valgono tre regole insieme:
   - dal **2 agosto 2026** deve dire di essere un'AI al primo contatto (AI Act art. 50, che l'Omnibus non ha rinviato) `[verificato: ufficiale — ai-act-service-desk art. 50; secondaria — Gibson Dunn 27/5/2026]`;
   - in Italia le chiamate automatizzate senza operatore richiedono il **consenso preventivo** (Codice privacy art. 130 c.1) `[verificato: secondaria — registrodelleopposizioni.it; ufficiale per i c.2/c.4 — Garante]`;
   - la voce clonata di un collega è un «deepfake» audio da dichiarare (art. 50(4)), e il consenso di un dipendente è debole per definizione (EDPB 05/2020) `[verificato: ufficiale — art. 50; EDPB]`.
2. **Prefissi 0843/0844: non sono obbligatori.** Li hanno introdotti la L. 5/2018 e la delibera AGCOM **156/18/CIR** del 2018, non una delibera del 2024-2025. In alternativa basta un numero in chiaro e richiamabile. La delibera **21/26/CIR** (14/4/2026) non ha reso obbligatoria una numerazione dedicata, ma obbliga i fornitori a bloccare le chiamate con un CLI non attribuito `[verificato: secondaria — Agenda Digitale 7/5/2026; registrodelleopposizioni.it]`.
3. **L'analisi «performance del sales» è il secondo punto critico.**
   - Valutare il rendimento dei lavoratori con l'AI è un caso dell'**Allegato III punto 4(b)** dell'AI Act. Se c'è profilazione, è **sempre alto rischio** (art. 6(3)) `[verificato: ufficiale — art. 6, Allegato III]`. Gli obblighi per l'alto rischio scattano il **2 dicembre 2027** dopo l'Omnibus (Reg. UE 2026/1744) `[verificato: secondaria — Gibson Dunn, Orrick, ActuIA]`.
   - **Inferire le emozioni** dei colleghi è già **vietato** dal 2 febbraio 2025 (art. 5(1)(f)) `[verificato: ufficiale — art. 5]`.
4. **Se i colleghi in Italia sono dipendenti, si applica lo Statuto dei lavoratori art. 4.** Gli strumenti che permettono un controllo a distanza richiedono un accordo sindacale o l'autorizzazione dell'Ispettorato. Il Garante fissa un tetto orientativo di **21 giorni** per i metadati della posta `[verificato: ufficiale — Garante doc. 6/6/2024, provv. 29/4/2025 e 14/7/2026]`. La «mappa dei processi dai metadati di Google Workspace» va quindi fatta su dati **aggregati**.
5. **La L. 132/2025 (in vigore dal 10/10/2025) art. 11** obbliga a informare i lavoratori quando l'AI serve a controllo o monitoraggio (rinvio al d.lgs. 152/1997 art. 1-bis) `[verificato: secondaria — gdpr.it, Wikilabour]`.
6. **La registrazione delle riunioni regge sul legittimo interesse, a condizioni precise:** avviso prima della registrazione, finalità e conservazione dichiarate, accesso limitato. Il consenso dei dipendenti non è una base affidabile (EDPB 05/2020) `[verificato: ufficiale — EDPB; secondaria — Agenda Digitale, iusprivacy]`.
7. **Email B2B: UK e Italia divergono.**
   - UK (PECR): le email a società non richiedono consenso, quelle a ditte individuali sì `[verificato: ufficiale — ICO]`.
   - Italia: il Garante applica l'art. 130 (consenso) anche ai contatti aziendali; i dati pubblici o presi da LinkedIn non sono liberi per il marketing (provv. 12/2/2026) `[verificato: ufficiale — Garante]`.

   Gli agenti non cambiano la regola, ma moltiplicano i contatti: serve un'unica lista di soppressione per tutti i canali.
8. **Anthropic:**
   - i dati commerciali (API, Team) non vengono usati per l'addestramento, salvo opt-in; Anthropic è responsabile del trattamento (processor) `[verificato: ufficiale — privacy.claude.com]`;
   - l'API conserva input e output **30 giorni**, oppure **ZDR** su accordo (non vale per l'interfaccia Team). I contenuti segnalati possono restare fino a 2 anni `[verificato: ufficiale]`;
   - **non c'è una regione UE**: `inference_geo` ammette solo `global` e `us`, la workspace geo solo `us` `[verificato: ufficiale — platform.claude.com data-residency]`.
9. **ElevenLabs** conserva in USA di default; la residenza UE è **solo Enterprise** e il trattamento fuori regione resta possibile `[verificato: ufficiale]`. **Grok Bot (xAI)** è in **beta** dall'11/8/2026, solo su abbonamenti SuperGrok/Cursor; Enterprise è in lista d'attesa e la regione non è indicata `[verificato: ufficiale — x.ai]`. Non è adatto oggi ai dati di clienti e lead `[non verificato: valutazione]`.
10. **Mettere trascrizioni e CRM sul server in ufficio** fa di SerSan il titolare con l'intera responsabilità della sicurezza (art. 32): cifratura, backup cifrato fuori sede, accessi nominativi, log e procedura di data breach a 72 ore. Lo schema di backup `age` di SersanOutreach si riusa `[verificato: 01-sersanoutreach.md §3]`.

---

## 0. Quali regole valgono per SerSan

| Regime | Quando si applica a SerSan | Stato |
|---|---|---|
| **UK GDPR + DPA 2018 + PECR** (e Data (Use and Access) Act 2025) | sempre: SerSan è una UK Ltd; PECR per email, SMS e chiamate verso UK | ICO: guida B2B «under review» per le modifiche del DUAA 2025 `[verificato: ufficiale — ico.org.uk B2B]`; definizione di direct marketing del DPA portata in PECR dal 20/8/2025 `[verificato: secondaria — sintesi di ricerca su ico.org.uk]` |
| **GDPR UE + Codice privacy IT** | per i dati di persone in Italia (lead, clienti, team). Due strade: (a) il team in Sardegna è uno «stabilimento» (art. 3(1)); (b) art. 3(2), offerta di servizi in UE, che richiede un **rappresentante UE (art. 27)** | da decidere con un legale (§7). Il Garante ha sanzionato Character.AI anche per il **ritardo nella nomina del rappresentante UE** (comunicato 9/7/2026, 158.000 €) `[verificato: ufficiale — garanteprivacy.it docweb 10269594]` |
| **Trasferimenti UE→UK** | dati dei lead italiani gestiti dalla Ltd | adeguatezza UK **rinnovata il 19/12/2025 fino al 27/12/2031** `[verificato: secondaria — Hunton, Freeths, The Register]` |
| **Statuto dei lavoratori art. 4, L. 132/2025 art. 11, d.lgs. 152/1997 art. 1-bis** | solo se in Italia ci sono **lavoratori subordinati** (o parasubordinati, per l'informativa) | inquadramento di Alberto e Mattia: `non trovato` |
| **AI Act (Reg. UE 2024/1689, modificato dal 2026/1744)** | per sistemi usati in UE o il cui output è usato in UE (art. 2) | art. 2 non riletto in questa sessione `[non verificato]`; versione consolidata EUR-Lex del 27/7/2026 `[verificato: ufficiale — ai-act-service-desk]` |
| **Telemarketing IT** (art. 130 Codice, DPR 26/2022 RPO, L. 5/2018, delibere AGCOM) | chiamate verso numeri italiani | §2 |

---

## 1. Registrazione e trascrizione di riunioni e call di vendita

### 1.1 Persone esterne (clienti, lead)

| Tema | Regola pratica | Fonte |
|---|---|---|
| Base giuridica | legittimo interesse (verbalizzazione, follow-up, CRM), con test di bilanciamento scritto; il consenso serve solo se la registrazione non è necessaria | Agenda Digitale «Videocall e privacy» `[verificato: secondaria]`; ICO B2B (test in tre parti) `[verificato: ufficiale]` |
| Informativa | nell'invito (link alla privacy) + annuncio a voce all'avvio + possibilità di chiedere di non registrare; il bot Fireflies visibile come partecipante | prassi degli enti (informativa prima dell'avvio) `[verificato: secondaria — comune.vicenza.it, ss.camcom.it]`; dettaglio Fireflies `non trovato` (non cercato) |
| Diritto di opposizione | il marketing diretto ha un'opposizione **assoluta** (UK e UE): chi dice no esce da tutti gli agenti | ICO B2B `[verificato: ufficiale]` |
| Conservazione | proposta: audio cancellato dopo la trascrizione (≤ 30 giorni); trascrizione e riassunto 24 mesi dall'ultimo contatto; poi cancellazione automatica | `[non verificato: proposta]` |
| Regno Unito | registrare le chiamate a fini aziendali richiede una base UK GDPR e un'informativa; le regole specifiche (Lawful Business Practice Regulations) non sono state verificate | `[non verificato]` |

### 1.2 Colleghi: la «performance del sales» e il coaching

| Rischio | Cosa dice la regola | Fonte |
|---|---|---|
| Controllo a distanza | in Italia, gli strumenti da cui deriva la possibilità di controllo a distanza richiedono **accordo sindacale o autorizzazione dell'Ispettorato** (con 4 persone senza RSA si passa dall'Ispettorato) | Garante, documento di indirizzo metadati 6/6/2024 (doc. 10026277) e provv. 29/4/2025 (10134221) `[verificato: ufficiale]`; «senza RSA → Ispettorato» `[non verificato: lettura dell'art. 4]` |
| Metadati (Google Workspace) | conservare i metadati della posta oltre **21 giorni** (indicazione orientativa) può costituire controllo indiretto; per finalità del comma 1 servono le garanzie sindacali anche entro 21 giorni | Garante 6/6/2024; provv. 14/7/2026 Comune di Chivasso (10286374) `[verificato: ufficiale]` |
| Informativa AI | il datore informa i lavoratori sull'uso di sistemi di AI per controllo o monitoraggio (L. 132/2025 art. 11, rinvio all'art. 1-bis d.lgs. 152/1997); in vigore dal 10/10/2025 | gdpr.it, Wikilabour `[verificato: secondaria]` |
| Consenso del dipendente | quasi mai libero nel rapporto di lavoro | EDPB Guidelines 05/2020 sul consenso `[verificato: ufficiale — edpb.europa.eu]` |
| Punteggi sulle persone | precedenti Foodinho: 2,6 M€ (2021) e 5 M€ (2024). Il Garante ha chiesto intervento umano, diritto di contestare, verifica periodica dell'accuratezza, niente discriminazioni e rispetto dell'art. 4 | garanteprivacy.it doc. 9677377, 10074840 `[verificato: ufficiale]` |
| AI Act | valutare prestazioni e comportamento dei lavoratori = Allegato III 4(b); con profilazione è sempre alto rischio (art. 6(3)); dal **2/12/2027** | ai-act-service-desk art. 6, Allegato III `[verificato: ufficiale]`; data `[verificato: secondaria]` |
| Emozioni | **vietato** inferire le emozioni sul luogo di lavoro (art. 5(1)(f)), salvo motivi medici o di sicurezza | ai-act-service-desk art. 5 `[verificato: ufficiale]` |

**Come progettarlo** `[non verificato: proposta]`:
- il report di coaching va **solo al sales interessato**;
- al responsabile vanno **indicatori aggregati** sulla call o sulla pipeline (fit score del cliente, obiezioni ricorrenti), non un voto alla persona;
- nessun uso dei report per promozioni, compensi o sanzioni;
- nessun tono, stress o «sentiment» del collega.

Se invece i due CEO vogliono la valutazione del personale (il punto G4 della visione), serve trattarla da sistema ad alto rischio a partire da dicembre 2027 e, in Italia, seguire la procedura dell'art. 4. **Domanda aperta:** se i «sales» sono i soci e amministratori, e non dipendenti, l'art. 4 non si applica, ma GDPR e AI Act sì.

---

## 2. Agente vocale «Andrea» che richiama i lead

| Obbligo | Dettaglio | Fonte |
|---|---|---|
| **Dichiararsi AI** | art. 50(1): le persone devono sapere che interagiscono con un'AI; art. 50(5): informazione chiara **al più tardi alla prima interazione**; in vigore dal **2/8/2026**, non rinviato dall'Omnibus | ai-act-service-desk art. 50 (consolidato 27/7/2026) `[verificato: ufficiale]`; date `[verificato: secondaria — Gibson Dunn 27/5/2026]`; linee guida della Commissione sull'art. 50 del 20/7/2026 `[verificato: secondaria — gtlaw, nicfab]` |
| Voce clonata | contenuto audio che imita una persona reale: obbligo di disclosure come deepfake (art. 50(4)); per l'audio si citano avvisi sonori | art. 50(4) `[verificato: ufficiale]`; definizione di deepfake (art. 3) non riletta `[non verificato]` |
| **Consenso per chiamate automatizzate (IT)** | art. 130 c.1 Codice privacy: chiamate senza operatore solo con consenso preventivo; il RPO si applica anche ai sistemi automatizzati | registrodelleopposizioni.it (DPR 26/2022) `[verificato: secondaria]`; testo art. 130 c.1 su Normattiva non letto `[non verificato]` |
| **RPO** | dal 2022 copre tutti i numeri, cellulari compresi; l'iscrizione annulla i consensi precedenti; consultazione **mensile e prima di ogni campagna**; efficace in 15 giorni | registrodelleopposizioni.it, DPR 26/2022 `[verificato: secondaria/ufficiale RPO]` |
| **Numero chiamante** | numero **in chiaro e richiamabile** oppure prefissi **0844** (commerciali) / **0843** (statistiche), da L. 5/2018 e delibera **156/18/CIR**. I prefissi non sono obbligatori e risultano inutilizzati | registrodelleopposizioni.it `[verificato]`; studiocataldi, Agenda Digitale 7/5/2026 `[verificato: secondaria]` |
| CLI e spoofing | delibera **21/26/CIR** (adottata il 14/4/2026, pubblicata il 29/4/2026): il fornitore deve impedire chiamate con CLI non attribuito. Piattaforma anti-spoofing per le chiamate dall'estero da **novembre 2025** (delibera 106/25/CONS) | Agenda Digitale 7/5/2026 `[verificato: secondaria]`. **Conseguenza:** un numero italiano presentato da un operatore UK rischia il blocco; serve una numerazione italiana assegnata da un operatore autorizzato `[non verificato]` |
| **UK** | chiamate automatizzate: consenso **specifico** per le chiamate automatiche, anche se il numero non è nel TPS/CTPS; chiamate live: screening TPS + CTPS | ICO B2B `[verificato: ufficiale]`; un agente conversazionale AI equiparato a «automated call» `[non verificato: parere]` |
| Base per richiamare un lead che ha compilato un modulo | il lead chiede di essere ricontattato, quindi misure precontrattuali. Resta prudente raccogliere nel modulo un consenso esplicito alla «richiamata da un assistente AI», con traccia (ora, IP, testo) | `[non verificato: proposta]` |
| Sanzioni recenti | TIM 9,5 M€ per telemarketing (luglio 2026); oltre 37.000 segnalazioni nei primi 7 mesi del 2026 | riportato da un risultato di ricerca sul sito del Garante, pagina non aperta `[non verificato]` |

### Clonare la voce di un collega

- **Consenso:** nel rapporto di lavoro il consenso non è libero, salvo che il rifiuto non abbia conseguenze (EDPB 05/2020) `[verificato: ufficiale]`.
- **Contratto proposto** `[non verificato: proposta]`: un accordo separato di licenza d'uso della voce, facoltativo, revocabile, con un compenso e con usi elencati (solo «Andrea», solo richiamate dei lead). Prevede la cancellazione del modello vocale a fine rapporto o a richiesta.
- **Reato:** la L. 132/2025 ha introdotto l'**art. 612-quater c.p.** (diffusione illecita di contenuti generati o alterati con AI che inducono in errore e causano un danno ingiusto, fino a 5 anni) `[verificato: secondaria — iusletter, truescreen]`.
- **Fornitore:** ElevenLabs richiede la verifica del consenso per la clonazione `[verificato: ufficiale, pagina marketing, senza dettaglio]`.
- **Alternativa più semplice:** una voce sintetica non riconducibile a una persona reale, con il nome dell'assistente.

---

## 3. Email e LinkedIn outbound: cosa cambia con gli agenti

SersanOutreach copre già il flusso con approvazione umana. Le decisioni di compliance D0 sono aperte (giurisdizione, indirizzo fisico, deroga ADR-004) `[verificato: 01-sersanoutreach.md riga 323]`.

| | UK (PECR + UK GDPR) | Italia (GDPR + Codice art. 130) |
|---|---|---|
| Email a società | consenso **non** richiesto; mittente identificato e opt-out funzionante `[verificato: ufficiale — ICO]` | il Garante richiede il consenso (art. 130 c.2) anche per indirizzi aziendali di persone; eccezione soft spam (c.4) solo per i propri clienti `[verificato: ufficiale — Garante doc. 2542348, 10271850]` |
| Ditte individuali | come persone fisiche: consenso o soft opt-in `[verificato: ufficiale]` | come persone fisiche `[non verificato]` |
| Dati da LinkedIn o dal web | legittimo interesse con test e informativa `[verificato: ufficiale]` | vincolo di finalità: dati raccolti per uno scopo non si riusano per il marketing; caso Lex Iuris, ammonimento del 12/2/2026 `[verificato: ufficiale — Garante doc. 10225019]` |

**Cosa cambia con gli agenti** `[non verificato: proposta]`:
1. Una sola lista di soppressione per email, LinkedIn, voce e follow-up post-call: un «no» su un canale ferma tutti gli agenti.
2. L'agente post-call che manda la mail di follow-up a un **cliente con cui si è parlato** non fa marketing a freddo; i messaggi a lead nuovi restano nella lane di SersanOutreach con approvazione umana.
3. L'informativa art. 14 va data al primo contatto (entro un mese) e deve dire che c'è un'AI.
4. Il brief pre-meeting (aperture email, post LinkedIn, «segnali strategici») è profilazione B2B: va nel registro con la sua fonte e la conservazione. Il tracciamento delle aperture verso destinatari italiani è da valutare con il legale.

---

## 4. AI Act: classificazione e scadenze

| Componente | Ruolo SerSan | Classificazione proposta | Obblighi |
|---|---|---|---|
| Orchestratore, agenti di back-office (debrief, CRM, offerte, mappa processi aggregata) | fornitore (sistema costruito in casa, messo in servizio per uso proprio) + deployer | rischio minimo `[non verificato]` | art. 4 alfabetizzazione |
| Chat o agenti che scrivono a esterni | fornitore + deployer | trasparenza (art. 50(1)) | dichiararsi AI dal 2/8/2026 |
| «Andrea» con voce clonata | fornitore + deployer | trasparenza (art. 50(1) e 50(4)) | dichiararsi AI e dichiarare l'audio sintetico |
| Analisi delle call: fit score del **cliente** | deployer | non è nell'Allegato III `[non verificato]` | trasparenza verso il cliente (registrazione e AI) |
| Analisi delle call: **valutazione del sales** | fornitore + deployer | **alto rischio** (Allegato III 4(b) + profilazione, art. 6(3)) `[verificato: ufficiale]` | dal **2/12/2027**: gestione del rischio, dati, log, supervisione umana, informazione ai lavoratori (art. 26) `[art. 26 non riletto: non verificato]` |
| Inferenza di emozioni dei colleghi | — | **vietata** dal 2/2/2025 (art. 5(1)(f)) `[verificato: ufficiale]` | non costruirla |

**Scadenze:**
- **2/2/2025:** divieti (art. 5) e alfabetizzazione (art. 4) in vigore. L'Omnibus ha ammorbidito l'art. 4: da «garantire un livello sufficiente» a «adottare misure per sostenerne lo sviluppo» `[verificato: secondaria — Gibson Dunn, ISMS Lite]`.
- **27/7/2026:** l'Omnibus (Reg. UE 2026/1744) è in vigore. Il Parlamento lo ha approvato il 16/6/2026 e il Consiglio il 29/6/2026 `[verificato: secondaria — Orrick 07/2026, aiacto, ActuIA]`.
- **2/8/2026:** trasparenza (art. 50) in vigore.
- **2/12/2026:** fine della tolleranza per la marcatura art. 50(2), solo per i sistemi già sul mercato prima del 2/8/2026 `[verificato: secondaria]`. Riguarda i fornitori di modelli generativi più che SerSan `[non verificato]`.
- **2/12/2027:** obblighi per gli alti rischi dell'Allegato III. **2/8/2028:** obblighi per i sistemi dell'Allegato I `[verificato: secondaria]`.

**Alfabetizzazione in pratica** `[non verificato: proposta]`: un'ora di formazione documentata per i 4 sull'uso degli agenti, sui limiti, sui dati che non vanno nel cloud e su quando fermarli. Va aggiornata a ogni nuovo agente.

---

## 5. Dove stanno i dati

| Servizio | Dove | Conservazione e addestramento | Contratto | Fonte |
|---|---|---|---|---|
| **Anthropic API** (crediti da 800 $/mese) | inferenza `global` (default) o `us` (prezzo 1,1×, modelli 4.6+); workspace geo **solo `us`**; **nessuna regione UE** | input/output cancellati entro **30 giorni**; ZDR per organizzazione su accordo (solo API ed endpoint idonei); contenuti segnalati fino a 2 anni, punteggi di sicurezza fino a 7 anni; feedback 5 anni; i Covered Models richiedono 30 giorni (dal 9/6/2026) | termini commerciali: cliente titolare, Anthropic responsabile; nessun addestramento salvo opt-in (feedback, Development Partner Program) | platform.claude.com data-residency e api-and-data-retention; privacy.claude.com 7996866 (aggiornata 1/7/2026), 7996868, 9267385 `[verificato: ufficiale]` |
| **Claude Team** (5 account) | come sopra (USA) | le chat restano finché le si cancella; l'admin imposta la conservazione dell'organizzazione; **non idoneo a ZDR** | termini commerciali + DPA; nessun addestramento di default | privacy.claude.com; support.claude.com `[verificato: ufficiale]`; testo del DPA `non trovato` |
| Rotte UE per Claude | Amazon Bedrock (profili di inferenza UE) o Google Vertex (multi-regione UE) | secondo il cloud provider | contratto con AWS o Google | platform.claude.com `[verificato: ufficiale]`, costi `non trovato` |
| **ElevenLabs** | USA di default; ambienti isolati **UE**, India, Singapore **solo Enterprise**; il trattamento può avvenire fuori regione (affiliate, sub-responsabili, moderazione, LLM custom, webhook) | Zero Retention Mode opzionale, separato, modelli limitati | DPA su richiesta (Enterprise) | elevenlabs.io/docs data-residency `[verificato: ufficiale]`; prezzo Enterprise `non trovato` |
| **Grok Bot (xAI)** | «computer nel cloud», regione non indicata | conservazione e addestramento: non indicati nella pagina di lancio | beta dall'11/8/2026 per SuperGrok/SuperGrok Plus/Heavy e Cursor; Enterprise in lista d'attesa; nel footer ci sono Enterprise Terms e DPA (non letti) | x.ai/news/introducing-grok-bot `[verificato: ufficiale]`; prezzi discordanti (120-300 $/mese) `[verificato: secondaria]` |
| **Hermes Agent** (self-hosted) | sul server SerSan; i dati escono solo verso il provider del modello scelto (Anthropic, OpenRouter, Nous Portal…) | memoria su volume locale | licenza MIT; nessuna certificazione (SOC 2/ISO) | vellum, opentechhub, dev.co `[verificato: secondaria]`; telemetria «assente» da una sola fonte `[non verificato]` |
| Fireflies (visione) | `non trovato` (non cercato) | `non trovato` | `non trovato` | da verificare prima dell'uso |

**Trasferimenti:** USA per Anthropic, ElevenLabs default e xAI. La base (Data Privacy Framework, SCC o IDTA UK) va letta nei DPA dei fornitori. Lo stato DPF di Anthropic è `non trovato`.

### Server in ufficio (HPE DL380 + firewall i226-V)

Cosa cambia `[non verificato: proposta, salvo dove indicato]`:
- **SerSan è titolare** delle trascrizioni e del CRM (non più un SaaS responsabile). Si riducono i trasferimenti extra-UE, ma tutta la sicurezza (art. 32) e la notifica del data breach entro 72 ore restano in casa.
- **Misure minime:**
  - cifratura del disco (i dischi del Smart Array E208i-p vanno cifrati a livello di OS);
  - backup cifrato **fuori sede** con chiave fuori dall'host: lo schema `age` + retention di SersanOutreach si riusa `[verificato: 01-sersanoutreach.md §3]`;
  - accessi nominativi con MFA, solo via WireGuard;
  - log degli accessi ai dati;
  - separazione tra i dati dei clienti e i dati interni;
  - UPS e rack chiuso a chiave;
  - restore provato a intervalli fissi.
- **Il paese del server conta:** se l'ufficio è in Sardegna, i dati stanno in UE e la Ltd vi accede dal Regno Unito, coperta dall'adeguatezza. L'ubicazione è `non trovata`.
- **Redazione prima del cloud:** il modello locale sulla Quadro RTX 4000 (8 GB) può fare la pseudonimizzazione dei nomi e dei numeri prima di mandare il testo a Claude. La fattibilità va misurata.

---

## 6. Le 10 regole operative da mettere nel documento

| # | Regola | Perché | Come si controlla |
|---|---|---|---|
| 1 | **Ogni agente che parla o scrive a un esterno si dichiara AI** nella prima frase o nel primo messaggio; «Andrea» dice di essere un assistente virtuale con voce sintetica | AI Act art. 50(1), (4), (5) dal 2/8/2026 | test automatico sul prompt di apertura; campione di registrazioni ogni mese |
| 2 | **Nessuna registrazione senza avviso**: avviso nell'invito + annuncio a voce + possibilità di dire no | GDPR artt. 6, 13; trasparenza | il bot di registrazione entra solo se l'evento ha il flag «avvisato» |
| 3 | **Nessun giudizio sulle persone senza revisione umana**: il coaching va solo all'interessato, al responsabile vanno dati aggregati, nessuna emozione inferita sui colleghi, nessuna decisione di lavoro presa dall'AI | Allegato III 4(b), art. 5(1)(f), art. 22 GDPR, Statuto art. 4, precedenti Foodinho | revisione degli output dell'agente di analisi; nessun campo «voto al sales» nel CRM |
| 4 | **Chiamate automatiche solo con consenso documentato**; numeri IT verificati sul RPO ogni mese e prima di ogni campagna; UK su TPS/CTPS; numero in chiaro e richiamabile assegnato da un operatore italiano | art. 130 c.1, DPR 26/2022, L. 5/2018, delibere AGCOM 156/18/CIR e 21/26/CIR; PECR | l'agente vocale rifiuta un lead senza consenso registrato o con controllo RPO più vecchio di 30 giorni |
| 5 | **Un «no» vale per tutti i canali e tutti gli agenti**: una sola lista di soppressione condivisa | opposizione assoluta al marketing (UK e UE) | ogni agente con canale esterno legge la lista prima di agire |
| 6 | **Nessuna voce o volto di una persona reale senza contratto separato**, facoltativo, revocabile e compensato; il clone si cancella a fine rapporto | EDPB 05/2020; art. 612-quater c.p.; diritto alla voce | registro dei modelli vocali con il riferimento del contratto |
| 7 | **Minimizzazione prima del cloud**: pseudonimizzare i dati personali non necessari; mai dati sanitari o giudiziari nel cloud; solo fornitori con termini commerciali + DPA (Anthropic API/Team, ElevenLabs con DPA); niente dati di clienti o lead su abbonamenti consumer o beta (es. Grok Bot) | art. 5(1)(c), 28, 44 GDPR | elenco dei fornitori ammessi nel codice dell'orchestratore; blocco delle chiamate verso endpoint non in lista |
| 8 | **Conservazione con scadenze automatiche** (proposta): audio ≤ 30 giorni; trascrizioni e CRM 24 mesi dall'ultimo contatto; lead mai convertiti 12 mesi; log degli agenti 90 giorni; metadati individuali di Workspace ≤ 21 giorni, poi solo aggregati | art. 5(1)(e) GDPR; Garante 6/6/2024 sui metadati | job notturno di cancellazione con ricevuta |
| 9 | **Registro dei trattamenti e DPIA aggiornati a ogni nuovo agente**; DPIA obbligatoria per registrazioni, analisi delle vendite e agente vocale | art. 30 e 35 GDPR; Garante su Character.AI (DPIA in ritardo) | test che fallisce se un agente nuovo non ha la sua riga nel registro |
| 10 | **Umano nel giro per ogni azione esterna irreversibile** (prima offerta, invio a freddo, chiamata a un numero nuovo, modifica visibile al cliente) + **formazione AI documentata** per tutti e quattro | art. 4 AI Act; prudenza commerciale; coerente con la lane di approvazione di SersanOutreach | log di audit per agente; registro delle formazioni |

---

## 7. Dove serve un parere legale

1. **Applicazione del GDPR UE alla Ltd:** il team in Sardegna è uno stabilimento (art. 3(1))? Se no, serve il **rappresentante UE (art. 27)**? Quale autorità è capofila?
2. **Inquadramento dei collaboratori in Italia** (dipendenti, parasubordinati, P.IVA, soci): da questo dipendono l'art. 4 dello Statuto, la procedura presso l'Ispettorato e l'informativa ex art. 1-bis.
3. **«Andrea»:** è un «sistema automatizzato di chiamata» per l'art. 130 c.1 (IT) e per PECR reg. 19 (UK)? Qual è la base per richiamare chi ha compilato un modulo? Che testo deve avere il consenso nel form?
4. **Contratto per la voce clonata** di un dipendente: validità, revoca, uso dopo la cessazione, art. 612-quater.
5. **Analisi delle vendite:** dove passa il confine tra coaching (fuori dall'Allegato III) e valutazione dei lavoratori (alto rischio dal 2/12/2027)? Obblighi del deployer (art. 26).
6. **Email B2B verso l'Italia:** consenso (linea del Garante) o legittimo interesse? Chiude le D0 aperte di SersanOutreach.
7. **Trasferimenti verso gli USA** (Anthropic, ElevenLabs, xAI): base giuridica nei DPA; serve l'IDTA o l'Addendum UK per la Ltd.
8. **Registrazione delle chiamate con clienti UK:** Lawful Business Practice Regulations e aggiornamenti del DUAA 2025.

---

## 8. Fonti

| Fonte | Tipo | Data |
|---|---|---|
| https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50 | ufficiale (Commissione UE, testo consolidato) | consolidato al 27/7/2026, letto il 24/10/2026 |
| https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6 | ufficiale | idem |
| https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3 | ufficiale | idem |
| https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5 | ufficiale | idem |
| https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ | secondaria | 27/5/2026 |
| https://www.orrick.com/en/Insights/2026/07/EU-AI-Act-Update-Digital-Omnibus-Finalizes-8-Compliance-Changes | secondaria | 07/2026 |
| https://www.actuia.com/en/news/ai-act-obligations-in-force-and-delays-under-omnibus-2026-1744/ | secondaria | 2026 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10026277 | ufficiale (metadati, 21 giorni) | 6/6/2024 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10286374 | ufficiale | 14/7/2026 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10134221 | ufficiale | 29/4/2025 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10269594 | ufficiale (Character.AI) | 9/7/2026 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9677377 e /10074840 | ufficiale (Foodinho) | 2021, 22/11/2024 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/2542348 | ufficiale (linee guida spam) | 4/7/2013 |
| https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10225019 | ufficiale (Lex Iuris) | 12/2/2026 |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10271850 | ufficiale | 28/5/2026 |
| https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf | ufficiale EDPB | 4/5/2020 (v1.1) |
| https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/ | ufficiale ICO | letta il 24/10/2026 (data della pagina non indicata) |
| https://registrodelleopposizioni.it/conosci-i-tuoi-diritti/ ; DPR 26/2022 (PDF sul sito RPO) | ufficiale RPO | 2022-2023 |
| https://www.agendadigitale.eu/infrastrutture/chiamate-da-numeri-falsi-nuove-regole-agcom-ecco-cosa-cambia/ | secondaria (delibera AGCOM 21/26/CIR) | 7/5/2026 |
| https://archivio.studiocataldi.it/articoli/news/32483-telemarketing-ecco-i-prefissi-per-identificare-i-call-center.asp | secondaria (delibera 156/18/CIR) | 2018 |
| https://www.gdpr.it/entrata-in-vigore-la-legge-132-2025-sullintelligenza-artificiale-nuovi-obblighi-per-i-datori-di-lavoro/ ; https://www.wikilabour.it/segnalazioni/rapporto-di-lavoro/impiego-dellintelligenza-artificiale-nel-mondo-del-lavoro/ | secondaria (L. 132/2025) | 2025 |
| https://iusletter.com/dalla-redazione/intelligenza-artificiale/deepfake-dimensione-fenomenologica-e-quadro-giuridico-applicabile/ | secondaria (art. 612-quater) | 22/5/2026 |
| https://platform.claude.com/docs/en/manage-claude/data-residency | ufficiale Anthropic | letta il 24/10/2026 |
| https://platform.claude.com/docs/en/manage-claude/api-and-data-retention | ufficiale Anthropic | letta il 24/10/2026 |
| https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data | ufficiale Anthropic | aggiornata il 1/7/2026 |
| https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training ; .../9267385-does-anthropic-act-as-a-data-processor-or-controller | ufficiale Anthropic | lette tramite ricerca il 24/10/2026 |
| https://elevenlabs.io/docs/overview/administration/data-residency | ufficiale ElevenLabs | letta il 24/10/2026 |
| https://x.ai/news/introducing-grok-bot | ufficiale xAI | 11/8/2026 |
| https://www.hunton.com/privacy-and-cybersecurity-law-blog/european-commission-renews-uk-data-adequacy-decisions | secondaria (adeguatezza UK) | 12/2025 |
| https://www.vellum.ai/blog/official-hermes-agent-breakdown ; https://www.opentechhub.io/hermes-agent/ | secondaria (Hermes Agent) | 2026 |
| `C:/Users/alber/SerSan-AgentOS/ricerca/01-sersanoutreach.md`, `00-visione-funzionalita.md` | locale | 24/10/2026 |
