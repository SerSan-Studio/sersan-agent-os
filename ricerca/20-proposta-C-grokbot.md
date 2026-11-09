# 20 · Proposta C: Grok Bot in abbonamento come forza lavoro, il server come cassaforte

**Per:** Alessandro Serratt e Michele Sanna. **Da:** Alberto Tuveri, 24 ottobre 2026. Una delle sette proposte indipendenti.

**Etichette.** [verificato: fonte] = letto nella fonte; [non verificato] = stima o proposta mia. R00-R18 = i file `NN-*.md` di `C:/Users/alber/SerSan-AgentOS/ricerca/`. Prezzi IVA esclusa, 1 $ = 0,8934 € [verificato: R14].

---

## 1. L'architettura in una pagina

**In una riga: i Bot di Grok fanno il lavoro che si vede, il server custodisce i dati e fa il lavoro che non deve uscire.**

- **Un Main Bot per persona**: il capo di gabinetto con la stella. Riceve le richieste da telefono, desktop o Slack e le smista ai Bot specialisti [verificato: R11 §2.1].
- **I Bot aziendali sono Team Bots**: Post-call, Brief, Offerte, Coach, Editoriale, uno per ogni grande cliente. Alberto li configura una volta e li pubblica ai quattro; ognuno ha un'app Slack, memoria di team, fino a 25 segreti e server MCP propri [verificato: R11 §2.5].
- **Il server non ospita i Bot**, che girano solo nel cloud di Cursor, negli USA [verificato: R11 §6]. Ospita SersanOutreach, la memoria (Postgres con pgvector), trascrizione e oscuramento, le pipeline riservate con Claude API e un **gateway MCP** che decide che cosa i Bot leggono e scrivono.
- **Tre colori di dati** [non verificato: proposta]:
  - **verde** (pubblico, interno non personale): libero verso Grok;
  - **giallo** (contatti di lavoro, riassunti senza testo integrale, campi CRM): verso Grok solo dal gateway, dopo la DPIA;
  - **rosso** (audio, trascrizioni integrali, email intere, documenti dei clienti, valutazioni delle persone, finanza): server o Claude API con termini commerciali, **mai Grok**.

```
 4 PERSONE -- app Grok (telefono, desktop) -- Slack (#agenti, #cliente-x)
                          |
 +----------- GROK BOT (cloud Cursor, USA) -----------------+
 | 4 Main Bot, Team Bots, routine, webhook, browser cloud,  |
 | plugin: Calendar, Notion, Slack, Drive (Gmail dopo)      |
 +------^ MCP via HTTPS (verde, giallo) ----^ webhook ------+
        |                                   |
 +----- Cloudflare Tunnel ------------------+---------------+
 | SERVER SERSAN (DL380, Proxmox)                           |
 | gateway MCP: strumenti, colori, audit, limiti            |
 | SersanOutreach: CRM, outbound, coda di approvazione      |
 | dispatcher: eventi -> pipeline -> webhook ai Bot         |
 | Postgres + pgvector; GPU: STT, embedding, giudice        |
 +---^----------------^--------------------^----------------+
  Recall.ai          ElevenLabs + Twilio   Claude API
```

**Il giro di un evento.** Una call finita o una lead nuova arriva al dispatcher, che lancia la pipeline locale e chiama il webhook della routine del Team Bot; una routine parte al più ogni 5 minuti, quindi il dispatcher raggruppa («3 nuove call») [verificato: R11 §2.4]. Il Bot lavora con plugin e gateway, che registra ogni chiamata. Ogni uscita verso l'esterno è una bozza; la invia una persona.

---

## 2. Copertura della lista A1-I4

| # | Componente (fonte) | Stato |
|---|---|---|
| A1 | Bot Recall.ai nelle call, con avviso nell'invito; audio trascritto sul server (faster-whisper, pyannote); riunioni in presenza registrate dal telefono (R14 §4; R13 §5; R16 §1.1) | da costruire; Recall in abbonamento |
| A2 | Notion con processi, obiettivi, regole, calendari, letto dal plugin (R11 §2.4) | pronto |
| A3 | pgvector ed embedding Qwen3-Embedding-0.6B sulla GPU; `cerca_memoria` dal gateway (R11 §5; R13 §7) | da costruire |
| A4 | Main Bot che delega + dispatcher deterministico sul server (R11 §2.1) | in abbonamento + da costruire |
| A5 | Raccolta, pulizia, indicizzazione: worker sul server; azione: Bot Grok, circa 50 per account (R11 §2.1) | da costruire / in abbonamento |
| A6 | Memoria per Bot, skill che si correggono, «Teach a task» di 10 minuti (R11 §2.4) | in abbonamento |
| A7 | Gruppi da 2 a 6 Bot con passaggi leggibili; Team Bots in Slack; #agenti dove il server annuncia gli eventi (R11 §2.5) | da adattare |
| B1 | Recap post-call nel canale interno #cliente-x, dove risponde il Team Bot del cliente | da costruire |
| B2 | `record_meeting`, `update_deal`, `record_next_action` dal gateway; `create_deal` da aggiungere (R01 §5.2) | da adattare |
| B3 | Bozza di follow-up creata dal server in Gmail o Unibox; invio umano (R01 §5.5) | da adattare |
| B4 | To-do in un database Notion (R11 §2.4) | pronto |
| B5 | Scala di autonomia (§5); Grok non invia mai da solo all'esterno (R11 §7.4) | da costruire (regola) |
| C1 | Routine delle 5:30 del Main Bot: Calendar, Notion, `digest_ieri` (R11 §5) | in abbonamento |
| C2 | Recall.ai al posto di chi manca; Vexa in casa da provare (R12 §7) | in abbonamento |
| C3 | Claude Sonnet via API sul server, con le regole personali (R14 §1.5) | da costruire |
| C4 | Dettatura e chiamata vocale nell'app; Whisper locale per l'audio riservato | pronto |
| C5 | Registro aziendale delle riunioni (presenti, esito, pipeline emersa), `cerca_riunioni` (proposta) | da costruire |
| C6 | Pagina Notion «Come lavoro» per persona + Team Rules | da adattare |
| D1 | Deals e `commercial_events` di SersanOutreach + pesatura; oggi zero esiti, quindi pesi per fase (R01 §1.4) | da costruire |
| D2 | Team Bot Brief: web nel browser cloud + `brief_interno` (storico, aperture Instantly, enrich Perplexity); niente LinkedIn con login (R11 §5; R01 §5.5) | da adattare |
| D3 | Storia della relazione dentro `brief_interno` (R01 §5.5) | da adattare |
| D4 | Google Slides; moda.app via MCP da provare (R11 §5) | da adattare |
| D5 | Skill Offerta: catalogo Notion, riassunto giallo, brief; revisione umana (R11 §5) | da adattare |
| E1-E2 | Argomenti per i CEO; foglio settimanale delle ore risparmiate (R05 §5.8) | da costruire |
| E3 | Tetto mensile Grok, quota per posto, limiti per Bot nel gateway, chiave API per pipeline (R11 §4.1) | da adattare |
| E4 | Un'ora sull'AI Act + sessioni pratiche (R16 §4) | da costruire |
| F1 | Metadati della posta solo aggregati, al più 21 giorni; suite Google o Microsoft da confermare (R16 §1.2; R14 §5) | da costruire |
| F2 | Bot Intervistatore in chiamata vocale | in abbonamento |
| F3-F4 | Mappa dei processi, ore stimate, automazioni in ordine: Opus sul server, esito in Notion (R14 §1.5) | da costruire |
| F5 | App Grok sul telefono di tutti e quattro (R11 §1) | in abbonamento |
| G1 | Canale #call-vendita con riassunti gialli (proposta) | da costruire |
| G2 | Fit score dalla call + qualifier GP+BALD di SersanOutreach (R01 §1.1) | da adattare |
| G3 | Coaching con Opus sul server, report solo al venditore (R16 §1.2) | da costruire |
| G4 | Al responsabile solo aggregati, nessun voto alla persona (R16 §1.2) | da costruire |
| G5 | Andrea: ElevenLabs Agents + numero Twilio italiano, avviato dal server entro 90 s, si dichiara AI (R14 §3.4; R16 §2) | in abbonamento + da costruire |
| G6 | Analisi settimanale dei rifiuti; nuova apertura approvata da una persona (proposta) | da costruire |
| G7 | Cruscotto: tempo di richiamata, conversione per fonte (R01 §4.9) | da adattare |
| G8 | `lost_deal_analysis` al Team Bot Editoriale (R01 §5.1) | da adattare |
| G9 | Bot personali e Team Bots; organigramma in Notion con responsabile, budget, colore dei dati (R11 §2.1) | da adattare |
| H1 | Due ore a settimana di prove per 8 settimane, template condivisi (proposta) | da costruire |
| H2 | Ogni CEO usa il suo Main Bot dal primo giorno (proposta) | in abbonamento |
| H3 | Assessment con il Bot Intervistatore e un questionario (proposta) | da costruire |
| H4 | Alberto ambassador con posto Super o Ultra (R11 §4.1) | in abbonamento |
| H5 | «Share as template» solo per il team (R11 §2.1) | in abbonamento |
| H6 | Bacheca Notion; il Bot raccoglie le candidature, decidono i CEO (proposta) | da costruire |
| G10, H7, I1, I2 | Esiti e argomenti: piano a fasi (§6), CEO in prima persona (H2), contesto dal server (A1-A3) | — |
| I3 | Aree senza AI scritte: voce e volto dei founder, commenti e DM, lista dei 200 account, firma tecnica di Michele, prezzi e impegni, valutazione delle persone (R05 §5.8) | pronto |
| I4 | Team Bots Editoriale, Copy, Metriche; pubblicazione presidiata (R05 §5) | da adattare |

---

## 3. Che cosa gira sul server e che cosa in abbonamento

| Macchina Proxmox | Contenuto | vCPU | RAM | GPU, disco |
|---|---|---|---|---|
| `apps-prod` | SersanOutreach (8 servizi, 7,4 GiB di tetti misurati), Traefik, cloudflared, gateway, dispatcher | 8 | 32 GB | — |
| `data` | Postgres 17 + pgvector: CRM, riunioni, memoria, audit, contatori | 4 | 24 GB | 300 GB su mirror ZFS |
| `gpu` | llama.cpp: giudice Qwen3-4B, Qwen3-Embedding-0.6B; faster-whisper turbo int8 (circa 1,5 GB); pyannote e Presidio su CPU | 4 | 24 GB | RTX 4000 da 8 GB |
| `monitor`, `stage`, `pbs` | Grafana, Prometheus, Alertmanager; copia di prova; backup | 8 | 24 GB | dischi di backup separati |

Circa 104 GB su 128-160 [non verificato: dimensionamento da R15 §5.1, R13 §8, R01 §4.2]. L'audio, circa 30 ore al mese, si cancella entro 30 giorni.

**In abbonamento**: Grok Bot, che non si installa in casa [verificato: R11 §6]; Claude API per i dati rossi, perché la RTX 4000 regge modelli fino a 8-9B [verificato: R13 §0]; Recall.ai, 0,50 $ l'ora [verificato: R14 §4]; ElevenLabs e Twilio per voce e numero italiano [verificato: R13 §6]; Slack e Notion.

---

## 4. SersanOutreach e il marketing

- **SersanOutreach passa sul server** con la checklist di R01 §4.11. Il gateway espone ai Bot i 19 strumenti in lettura (`pipeline_overview`, `lost_deal_analysis`…) e una parte delle 14 operazioni (`record_meeting`, `record_next_action`, `update_deal`, `generate_drafts`) [verificato: R01 §5.1-5.2]. **`approve_message` resta umano.** Prima servono identità firmata in `enforce` (oggi `observe`), MFA dello staff e MCP via HTTPS con autenticazione [verificato: R01 §5.10, §6].
- **Eventi.** `positive_reply`, `meeting_booked` e `lost` arrivano al dispatcher: il Bot del titolare prepara la risposta in Unibox, Brief il dossier, Editoriale un tema.
- **Outbound invariato.** LinkedIn dall'estensione nel browser dei membri, email da Instantly, sempre con approvazione umana. **Nessun Bot Grok entra su LinkedIn**, nessuna tecnica anti-rilevamento [verificato: R11 §5; R18 §3].
- **Andrea non passa da Grok**, che non ha telefonia e distanzia le routine di 5 minuti [verificato: R11 §5]. Il modulo del sito chiama l'endpoint first-party di SersanOutreach e il dispatcher avvia la chiamata ElevenLabs entro 90 secondi [verificato: R01 §5.5]; l'esito torna nel CRM e in #call-vendita.
- **Marketing: tre Team Bots dentro le regole del 22/10** [verificato: R05 §5]. Editoriale porta temi da `reply_digest`, obiezioni e chiusure nel calendario Notion; Copy scrive bozze EN/IT con la skill di controllo; Metriche prepara il digest del lunedì in sola lettura. Si pubblica solo nella sessione presidiata con Metricool, dopo il sì scritto [verificato: R05 §5.4].

---

## 5. Controllo e sicurezza

**Autonomia a gradi** [non verificato: proposta]:
- **Livello 0 (fasi 0-2)**: tutto bozza; i Bot scrivono solo in canali interni, Notion e note CRM.
- **Livello 1**: un flusso senza correzioni per 30 giorni passa alle scritture interne automatiche.
- **Livello 2**: invii esterni automatici solo dentro i tetti del pilot di SersanOutreach, mai da Grok. I termini di Grok chiedono comunque revisione umana prima di comunicazioni esterne, transazioni, cancellazioni e impegni legali [verificato: R11 §7.4].

**Impostazioni del team Grok** [verificato: R11 §2.6]: Agent Email spenta; bozze accese; esecuzione sui PC locali su «Never»; Team Rules con le 10 regole di R16 §6; nessun «Always allow» sui plugin che scrivono. Gmail solo dopo 60 giorni e la DPIA: porterebbe l'intera casella negli USA.

**Iniezioni e confini:**
- Tutti i Bot di un utente condividono un computer cloud, quindi non sono un confine [verificato: R11 §2.3]: plugin minimi, nessun Bot di finanza su Grok. I Team Bots nei canali Slack girano su un computer separato.
- Il gateway consegna il testo esterno in campi delimitati, come dato; gli strumenti con effetti accettano solo identificativi stabili, mai nomi di canale (lezione dell'incidente Slack del 1/10).
- Le trascrizioni le legge sul server una sessione senza strumenti; a Grok arrivano campi strutturati.

**Audit.** Action Recording, audit log e OpenTelemetry sono solo Enterprise [verificato: R11 §2.6]. Noi teniamo un token del gateway per Bot e un registro append-only di ogni chiamata, con catena di hash copiata fuori sede. Buco residuo: ciò che un Bot fa nel browser cloud non lo vediamo.

**Budget.** Grok ha un tetto mensile sul saldo prepagato e una quota settimanale per posto, nessun budget per Bot [verificato: R11 §4.1, §5]. Aggiungiamo limiti giornalieri per token nel gateway e una chiave API per pipeline, con l'uso per chiave nella Console.

**GDPR.** DPA di Cursor (clausole UE, addendum UK) firmato prima dei dati gialli [non verificato: R11 §1, fonte terza]; DPIA prima della fase 2; lista di soppressione unica; audio al più 30 giorni [non verificato: R16 §6]. R16 sconsiglia dati di clienti su servizi in beta come Grok (§6, regola 7): qui vale per il rosso, non per il giallo. **Decidono i CEO**; la variante prudente pseudonimizza anche il giallo, e i Bot rendono meno.

**AI Act** [verificato: R16 §4]: Andrea si dichiara AI nella prima frase (art. 50, dal 2/8/2026); coaching solo all'interessato; nessuna emozione inferita dei colleghi; un'ora di alfabetizzazione documentata.

---

## 6. Piano a fasi

| Fase | Settimane | Lavoro | g-p | Cosa si vede alla fine |
|---|---|---|---|---|
| 0a Prova Grok | 1-2 | 4 posti, 4 Main Bot, 3 Team Bots su dati verdi, Team Rules, DPA, prova di 7 giorni sulla quota | 4 | ogni CEO riceve sul telefono il debrief delle 5:30 e chiede brief su aziende pubbliche |
| 0b Fondamenta | 1-3 | server secondo R15 §7, passi 1-9 | 6 | server in rack, UPS, backup provato |
| 1 CRM sotto i Bot | 3-5 | migrazione di SersanOutreach, identità in `enforce`, gateway con 12-15 strumenti, audit | 14 | in Slack «com'è la pipeline?» dà i numeri della dashboard; i next step finiscono nel CRM |
| 2 Memoria e post-call | 6-9 | Recall, STT locale, oscuramento, registro riunioni, pgvector, pipeline Claude, DPIA | 15 | entro 15 minuti dalla call: recap in #cliente-x, to-do, deal aggiornato, bozza pronta |
| 3 Vendite | 10-13 | Brief, Offerte, slide, fit score, coaching, Andrea con parere legale | 14 | brief il giorno prima; bozza d'offerta in un'ora; lead di prova richiamata in 90 s |
| 4 Organigramma | 14-18 | registro agenti, banca dei token, mappa dei processi, ciclo sui rifiuti, Bot marketing, premio, formazione | 13 | organigramma con più di 25 Bot, cruscotto dei costi, automazioni in ordine di valore |

Totale **66 giorni-persona** di Alberto e Mattia, più il tempo dei CEO [non verificato: stima]. Solo circa 12 sono configurazione di Grok: il resto vale anche senza Grok.

---

## 7. Costi mensili

**Formula.** Costo C = 0,8934 × (posti Grok × prezzo + tetto crediti Grok + ore Recall × 0,50 $ + minuti voce × 0,0445 $ + LLM voce) + numeri Twilio + Slack + Notion + ElevenLabs + backup + corrente + UPS/60 + API Claude − Claude Team finché vale il bundle.

| Voce (€/mese) | Minimo | Consigliato | Completo |
|---|---|---|---|
| Grok Bot (The X Subscription Teams) | 4 Premium, 120 $: 107,21 | 2 Super + 2 Premium + tetto 100 $, 360 $: 321,62 | 2 Ultra + 2 Super + tetto 200 $, 800 $: 714,72 |
| Recall.ai, solo registrazione | 30 h: 13,40 | 30 h: 13,40 | 80 h: 35,74 |
| Slack | Free: 0 | Pro × 4: 27,00 | Business+ × 4: 60,00 |
| Notion | Plus × 4: 35,74 | Plus × 4: 35,74 | Business × 4: 71,47 |
| ElevenLabs | 0 (senza Andrea) | Pro: 88,45 (0 col grant) | Scale: 267,13 |
| Twilio: numeri + minuti e LLM | 0 | 40,20 + 41,63 | 80,41 + 146,07 |
| Backup + corrente + UPS | 3,20 + 89,43 + 19,40 | 3,10 + 102,20 + 19,40 | 6,30 + 114,98 + 21,50 |
| API Claude (entro gli 800 $ di crediti) | 20,39 | 88,62 | 221,67 |
| **Totale architettura, di listino** | **288,77** | **781,36** | **1.739,99** |
| Esborso finché valgono bundle e crediti | 268,38 | 692,74 | 1.518,32 |
| Stack comune a tutte le proposte (Workspace, Instantly, Apollo, Apify, Metricool, moda, Higgsfield, Canva, 1Password, proxy) | 113,46 | 364,91 | 891,44 |
| **Tutto compreso** | **402,23** | **1.146,27** | **2.631,43** |

Fonti: R11 §4.1 per Grok; R14 §1.5, §2, §4, §5, §8, §11 per il resto.
- Finito il bundle: +446,70 € per 5 posti Claude Team premium, oppure +214,42 € per 2 premium e 2 standard se Grok diventa l'assistente quotidiano dei CEO.
- Spegnere la VM Azure fa risparmiare circa 150 € [non verificato: R14 §9].
- Rispetto allo scenario consigliato di R14 (941,70 €), C costa **circa 205 € al mese in più**: +321,62 di Grok, meno Fireflies, HubSpot e Notion Business.
- Il prezzo dei crediti Grok non è pubblicato [verificato: R11 §4.1].

---

## 8. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| Lock-in: conversazioni, memorie e skill non si esportano [verificato: R11 §7.1] | Fonte di verità sul server: skill in git come `SKILL.md`, regole in Notion. Uscita verso Claude Agent SDK o Hermes sullo stesso gateway in 10-15 g-p [non verificato] |
| Dati gialli negli USA; modello e sub-responsabili scelti dal fornitore [verificato: R11 §3, §7.2] | Colori dei dati, DPA, DPIA; Enterprise con residenza scritta se l'uso cresce |
| Quota non pubblicata [verificato: R11 §4.1]; nel forum c'è chi l'ha finita in un giorno [non verificato: R11 §4.3] | Prova di 7 giorni; posti Super a chi possiede le routine; tetto mensile; debrief di riserva sul server |
| Beta instabile: cinque incidenti dal 13 al 19/10 [verificato: R11 §7.3] | Nessun percorso critico su Grok: Andrea, webhook Instantly e coda di approvazione restano sul server |
| Termini: ogni azione è a carico del cliente [verificato: R11 §7.4] | Tutto bozza, Agent Email spenta, nessun «Always allow» |
| Accessi condivisi tra i Bot (incidente Slack del 1/10) [verificato: R11 §7.2] | Plugin minimi, destinazioni per identificativo, niente Bot di finanza |
| Piani cambiati tre volte in due mesi [verificato: R11 §7.1] | Pagamento mensile, revisione trimestrale |
| Approvazioni non presidiate che scadono in circa 10 minuti [verificato: R11 §2.6] | Il lavoro non presidiato produce solo bozze persistenti |
| Andrea: consenso, Registro delle opposizioni, numero italiano [verificato: R16 §2] | Voce sintetica non clonata, consenso nel modulo, parere legale prima della fase 3 |
| Storico commerciale vuoto: 11 lead, 0 vinti [verificato: R01 §1.4] | Pesi per fase dichiarati; pesatura sullo storico dopo 30 esiti |
| Un solo amministratore del server [verificato: R15 §6] | UPS, backup fuori sede, Mattia secondo amministratore |

---

## 9. Perché sceglierla, e perché no

**Perché sì:**
- È la strada più breve verso ciò che i CEO vedono ogni giorno: Bot con un nome, sul telefono e in Slack, con debrief e brief **in due settimane**, prima che il server sia pronto.
- Lascia al fornitore la parte più faticosa da tenere in casa: chat tra agenti, routine, browser isolati, app, approvazioni [verificato: R18 §1; R11 §9].
- Il lavoro sul server resta valido anche se un giorno si lascia Grok.
- Il servizio può usare Opus 5.5 senza costo in più per token [verificato: R11 §3].

**Perché no:**
- Il «cervello» (conversazioni, memoria dei Bot, decisioni) sta in un cloud USA chiuso, in beta, senza esportazione.
- Il modello non si sceglie e non si vede: la qualità dei singoli passaggi non si verifica.
- Costa circa 205 € al mese più del riferimento di R14, e i crediti Anthropic restano in parte inutilizzati.
- Senza Enterprise mancano audit e controlli di rete; li ricostruiamo solo per ciò che passa dal gateway.
- Copre la forma della visione di Alberto; i pezzi più preziosi (memoria, registro delle riunioni, pipeline pesata, Andrea) li costruiamo comunque noi.
