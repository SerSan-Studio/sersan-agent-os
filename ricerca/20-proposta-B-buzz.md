# 20 · Proposta B: buzz di Block come casa comune di persone e agenti

Data: 24/10/2026. Architetto B. Fonti abbreviate: `17§5` vuol dire `ricerca/17-buzz.md` §5, e così per gli altri numeri. Etichette: [verificato: fonte], [non verificato], [stima].

## 1. L'architettura in una pagina

**L'idea.** Un solo spazio di lavoro, buzz, sul nostro server. Le quattro persone e gli agenti stanno negli stessi canali. Ogni agente è un membro con nome, chiave propria, proprietario e memoria, e si delega con una @menzione. Gli umani leggono tutto [verificato: 17§0, §5]. buzz è la **stanza**, non il cervello. Il cervello di ogni agente è Claude Code con chiave API (oppure Hermes, Codex o un modello locale), collegato da `buzz-acp` [verificato: 17§5]. Quello che buzz non fa lo mettiamo noi accanto, in un servizio piccolo, `sersan-gate`: freno ai giri, approvazioni, isolamento, budget, email, CRM e memoria vettoriale.

```
 4 PERSONE: app buzz desktop/telefono, via VPN WireGuard     CLIENTI E LEAD
        │                                                   ▲ email, telefono, Slack
        ▼                                                   │ (solo dopo una carta)
┌───────────────────────── SERVER HPE · Proxmox VE 9 ──────────────────────────┐
│ VM buzz      relay Nostr · Postgres 17 · Redis 7 · MinIO · Caddy             │
│              #generale #squadra-* #cl-<cliente> #call-vendita #marketing     │
│              #ingresso (non fidato) #approvazioni #sala-macchine #premio     │
│                   ▲ wss, ruolo bot              ▲ workflow webhook interno   │
│ VM agenti    1 container per agente = buzz-acp + runtime                     │
│              Claude Code (chiave API) │ buzz-agent + llama.cpp │ Hermes      │
│                   │ solo MCP                                                 │
│ VM servizi   sersan-gate: carte, freno, budget, audit, esecutori             │
│              sersan-memoria: Postgres+pgvector │ ingresso: HMAC, anti-replay │
│ LXC gpu      Qwen3-4B giudice · Qwen3-Embedding-0.6B · faster-whisper        │
│ VM apps-prod SersanOutreach (8 servizi, MCP read 19 tool, operator 14 op)    │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ Cloudflare Tunnel: solo webhook e outreach.sersan.io
 ABBONAMENTI: API Anthropic · Claude Team · Recall.ai · Notion · ElevenLabs+Twilio
              Metricool · Instantly · Perplexity · Google Workspace
```

**Un flusso, dall'inizio alla fine (post-call).**
1. Il bot Recall.ai registra la call, che è stata dichiarata ai partecipanti.
2. La trascrizione arriva all'ingresso, che ne verifica firma o segreto. Un workflow `webhook` di buzz la posta in `#ingresso` e menziona @postcall.
3. @postcall legge le regole personali in Notion e la memoria, poi scrive punti e next step in `#cl-acme`.
4. Registra meeting e next action in SersanOutreach e crea i to-do in Notion.
5. Propone la mail di follow-up. La carta va in `#approvazioni`, un CEO reagisce ✅ e il gate invia con le credenziali dell'esecutore, non con quelle dell'agente.

**Cosa aggiungiamo a buzz e quanto costa farlo** (lacune da 17§8; le stime in giorni-persona sono mie):

| Aggiunta | Come | gg-p | €/mese |
|---|---|---|---|
| Freno ai giri fra agenti | patch nel nostro fork di `buzz-acp`: 8 risposte agente-agente per thread, azzerate da un umano; catene profonde al massimo 3; tetto in $ per thread; riga in `#sala-macchine` | 2-3 | 0 |
| Approvazioni verso l'esterno | `sersan-gate` fuori da buzz, perché `request_approval` fallisce [verificato: 17§5]; decide la reazione di una chiave umana autorizzata; avviso su Telegram | 5-6 | 0 |
| Isolamento | un container per agente con utente non privilegiato e segreti minimi; niente `--always-approve` | 2-3 | 0 |
| Cifratura | wss/TLS, relay raggiungibile solo in VPN, LUKS sui dischi, backup `age` fuori sede. I canali non sono cifrati end-to-end [verificato: 17§8 p.11] | 1 | 3-6 |
| Email e calendario | server MCP propri in lettura (con la chiave API i connettori di claude.ai si spengono); invio e inviti solo tramite esecutori del gate | 3 | 0 |
| CRM | MCP di SersanOutreach su HTTP con identità firmata in `enforce`; emettitore di webhook per gli eventi commerciali | 3-4 | 0 |
| Ingresso webhook | firma, anti-replay e rate limit, che il webhook di buzz non ha [verificato: 17§8 p.7] | 1 | 0 |
| Banca dei token | una chiave API per agente; lettura dei costi per turno (NIP-AM); `!shutdown` al 100 % | 1-2 | 0 |
| **Totale** | | **18-23** | **3-6** |

## 2. Copertura A1-I4

| # | Componente | Stato | Fonte |
|---|---|---|---|
| A1 | bot Recall.ai nelle call, avviso nell'invito; gli huddle buzz (solo inglese) restano spenti | in abbonamento | 14§4; 16§1 |
| A2 | Notion via MCP (processi, obiettivi, regole); canvas di canale come memoria della stanza | in abbonamento | 14§5; 17§5 |
| A3 | Postgres+pgvector, embedding locali sulla GPU, MCP `sersan-memoria` | da costruire | 13§7 |
| A4 | buzz è la stanza, Claude Code per agente è il cervello; Hermes via `hermes-acp` | da adattare | 17§5; 10§4.3 |
| A5 | persone e squadre buzz: raccolta, pulizia, indicizzazione, azione | da adattare | 17§5 |
| A6 | memoria per agente cifrata (core ≤ 64 KB) + skill in git; skill che si curano da sole con Hermes (fase 4) | da adattare | 17§5; 10§4.2 |
| A7 | canali, @menzioni, deleghe, trascrizione dal vivo del lavoro | pronto (freno da costruire) | 17§5 |
| B1 | `#cl-<cliente>` interno; al cliente va un'email approvata (Slack Connect solo nel completo) | da adattare | 17§6 |
| B2 | `record_meeting`, `update_deal` dell'operator SersanOutreach | da adattare | 01§5.2 |
| B3 | bozza → carta → esecutore Gmail/M365 | da costruire | — |
| B4 | Notion via MCP; action queue di SersanOutreach | pronto | 01§5.5 |
| B5 | gradi di autonomia per classe, decisi dai CEO | da costruire | 16§6 r.10 |
| C1 | workflow `schedule` (cron UTC) → @debrief; calendario via MCP | da adattare | 17§5 |
| C2 | bot Recall.ai | in abbonamento | 14§4 |
| C3 | @postcall su Sonnet 5.5 | pronto | 17§6 |
| C4 | dettatura del sistema operativo e dell'app Claude; Whisper locale per le note vocali | da adattare | 13§5 |
| C5 | tabella dei meeting in Postgres + ricerca buzz; pipeline emersa | da costruire | 17§6 |
| C6 | una pagina Notion per persona letta dalle skill | da adattare | 17§6 |
| D1 | pipeline pesata su `commercial_events` e deals di SersanOutreach | da costruire | 01§5.5 |
| D2 | @brief: enrich di SersanOutreach (Perplexity) + memoria + web search | da adattare | 01§2 |
| D3 | memoria vettoriale + `deal_activities` | da costruire | 01§5.5 |
| D4 | moda.app/Canva via MCP, link nel canale | da adattare | 05§5.3 |
| D5 | @offerte: catalogo Notion + trascrizione + brief → carta | da costruire | 14§1.5 |
| E1-E2 | argomenti per i CEO; costi al §7 | n.a. | 14§1.5 |
| E3 | chiave API per agente + tetti nel gate | da costruire | 17§8 p.5 |
| E4 | un'ora di formazione documentata (art. 4 AI Act) | da costruire (processo) | 16§4 |
| F1 | metadati Workspace solo aggregati, ≤ 21 giorni per persona | da costruire | 16§1.2 |
| F2 | interviste di @mappa in DM | da adattare | — |
| F3-F4 | mappa dei processi nel canvas di `#processi`; stima di ore e automazioni | da costruire | 14§1.5 |
| F5 | app tipo Slack per tutti, anche su telefono | pronto | 17§3 |
| G1 | `#call-vendita` con le trascrizioni | da adattare | 17§6 |
| G2 | fit score: il qualifier GP+BALD esteso alle call | da costruire | 01§1.1 |
| G3-G4 | coaching solo all'interessato, aggregati al responsabile | da costruire | 16§1.2 |
| G5 | "Andrea": ElevenLabs Agents + numero Twilio IT; consenso e RPO controllati dal gate | in abbonamento + da costruire | 14§3.4; 16§2 |
| G6-G7 | esiti delle chiamate → proposta di prompt con carta; KPI di richiamo | da costruire | — |
| G8 | @analista legge `lost_deal_analysis` e `review_feedback` → `#marketing` | da adattare | 01§5.1; 05§5.6 |
| G9 | catalogo `.agent.json` + organigramma in Notion: 100+ definizioni, 15-25 processi accesi | da adattare | 17§5 |
| G10, H1-H5, H7 | formazione e ambassador; canale `#laboratorio` | n.a. (processo) | 00 H |
| H6 | `#premio`, voto con le reazioni, conteggio di @segretario | da adattare | 17§6 |
| I1-I2 | il contesto è A1-A3 | n.a. | 00 I |
| I3 | canali con `respond_to: nobody`; elenco delle esclusioni in Notion | pronto | 17§6; 05§5 |
| I4 | agenti editoriale, copy e metriche; pubblicazione presidiata | da adattare | 05§5 |

## 3. Cosa gira sul server e cosa in abbonamento

Le misure partono da 8 moduli di RAM bilanciati (128 GB) [verificato: 15§2.2]. I numeri sono [stima], salvo SersanOutreach [verificato: 01§4.2].

| Macchina | Contenuto | vCPU | RAM | GPU | Disco |
|---|---|---|---|---|---|
| VM buzz | 5 container del compose, immagine fissata per digest | 4 | 8 GB | — | 100 GB |
| VM agenti | 10 agenti all'avvio, 25 a regime, parallelismo 1-2 (non 10) | 8 | 16→40 GB | — | 100 GB |
| VM servizi | gate, memoria, ingresso, Postgres+pgvector | 4 | 16 GB | — | 200 GB |
| LXC gpu | giudice, embedding, STT int8 ~1,5 GB | 4 | 16 GB | 8 GB, profilo "sempre acceso" [verificato: 13§8] | 50 GB |
| VM apps-prod/stage | SersanOutreach (tetti 7,4 GiB) | 12 | 36 GB | — | 200 GB |
| monitor, PBS | Prometheus/Grafana, backup | 4 | 12 GB | — | dischi propri |

Totale a regime: ~128 GB, cioè al limite. Comprare 2 moduli (138 €) e arrivare a 192 GB è la scelta prudente [verificato: 15§2.2]. Servono 2 SSD enterprise in mirror ZFS.

**In abbonamento, e perché.**
- Modelli di frontiera, perché 8 GB di VRAM non li reggono [verificato: 18§1; 13§2.2].
- Bot di riunione (Recall.ai), perché entrare in Meet, Zoom e Teams è difficile da fare in casa.
- Telefonia con numeri italiani (ElevenLabs+Twilio).
- Notion come base relazionale con MCP pronto.
- I servizi già integrati in SersanOutreach: Instantly (non ancora live), Perplexity, Apify [verificato: 01§2].

**Non in abbonamento:** chat (buzz sostituisce Slack), orchestrazione, vettoriale, embedding, giudice e STT per i dati che non devono uscire.

**Valutati e tenuti di riserva.**
- **Hermes Cloud**: ripiego se `hermes-acp` sul server resta fragile. Regione Londra, piano da 20 $ più un'istanza da circa 17-33 $ al mese [verificato: 18§2.4 per piani e regioni; taglie da terzi].
- **Grok Bot**: non entra in buzz e non gira sul server [verificato: 11§6].
- **Dots**: un solo agente per persona, con Business Premium a 125 $ [verificato: 18§2.2].

## 4. SersanOutreach e marketing

**SersanOutreach** passa sulla VM `apps-prod` seguendo la checklist di 01§4.11. Proposta per il database: Postgres locale, con backup fuori sede obbligatorio.
- **Dagli agenti a SersanOutreach.** I due server MCP passano da stdio a HTTP sulla rete interna, con una chiave per famiglia e `AUTH_IDENTITY_MODE=enforce` [verificato: 01§5.10]. Tutti gli agenti di vendita leggono i 19 tool. L'operator (14 operazioni, mai invio né approvazione in blocco) lo usano solo @postcall e @crm. `approve_message` non va a nessun agente: l'approvazione resta umana, nell'app o tramite una carta che porta il `fingerprint` [verificato: 01§5.2].
- **Da SersanOutreach agli agenti.** Un emettitore di webhook su `commercial_events` (`positive_reply`, `meeting_booked`, `lost`) chiama l'ingresso, che posta in `#vendite` e menziona l'agente giusto.
- **Lead dal modulo.** `inbound/first-party` → il gate controlla consenso e RPO → chiamata ElevenLabs entro 90 s → l'esito torna a SersanOutreach e in `#vendite`.
- **LinkedIn.** Resta nell'estensione di SersanOutreach, dentro l'envelope del pilot; le lane Playwright "stealth" restano spente e gli agenti buzz non toccano LinkedIn. Niente tecniche anti-rilevamento. Il modo `auto_linkedin` resta una decisione dei CEO [verificato: 01§6 r.2].

**Marketing.**
- Gli agenti @editoriale, @copy e @metriche lavorano in `#marketing` sui ruoli e sui sì già scritti nelle direttive del 22/10 [verificato: 05§5].
- Metricool in sola lettura per gli agenti. La pubblicazione resta una sessione presidiata, perché la regola di casa vieta che routine e loop scrivano su Metricool [verificato: 05§5.4]. Cambiarla è una decisione dei CEO, non di questa architettura.
- I post dei founder restano bozze nel loro DM.
- Il loop G8 porta ogni settimana obiezioni e motivi di perdita nel calendario editoriale.

## 5. Controllo e sicurezza

- **Approvazioni.** Una tabella delle classi nel codice del gate:

  | Classe | Regola |
  |---|---|
  | email o messaggi a terzi, pubblicazioni, chiamate | `ask` |
  | scritture interne (to-do, note di meeting) | `allow` |
  | cambio di stadio o valore di un deal | `ask` |
  | cancellazioni e pagamenti | `deny` |

  La carta mostra il testo esatto e l'impronta sha256. Vince la prima risposta e l'esecuzione è una sola, in transazione. Il gate ignora le reazioni delle chiavi con ruolo bot, perché il prompt di heartbeat invita gli agenti ad approvare [verificato: 17§8 p.2]. L'autonomia si guadagna per classe: dopo 30 giorni senza correzioni, i CEO possono passare una classe ad `allow`, mai un modello.
- **Iniezioni.** Email, trascrizioni e pagine web entrano solo in `#ingresso`. Lì le leggono agenti senza strumenti d'azione, che passano avanti solo campi strutturati. Un turno che ha letto testo non fidato rende `ask` ogni effetto. Ogni container monta solo i suoi MCP, con lo scope minimo.
- **Freno e stop.** Il freno è nel codice (§1). In più: `respond_to: allowlist`, un solo smistatore per canale, `!shutdown` e un ESTOP del gate che nega ogni effetto.
- **Audit.** Due catene di hash: quella di buzz e quella del gate. Ogni notte l'hash finale va copiato fuori dal server, perché la catena di buzz è "tamper-evident, not tamper-resistant" [verificato: 17§8 p.12].
- **Budget.** Tetto mensile per agente letto dagli eventi di costo: avviso all'80 %, stop al 100 %. Altri due tetti: per thread e per catena.
- **GDPR.**
  - SerSan diventa titolare dei dati sul server: cifratura, accessi nominativi, data breach in 72 ore [verificato: 16§5].
  - Conservazione: audio ≤ 30 giorni, trascrizioni 24 mesi, log degli agenti 90 giorni [verificato: 16§6 r.8].
  - DPIA per registrazioni, analisi vendite e "Andrea".
  - L'API Anthropic conserva 30 giorni, negli USA. I dati "solo locali" passano dal modello locale.
  - L'hosting di Block su buzz.xyz non si usa: i messaggi sarebbero leggibili da Block [verificato: 17§4].
  - A chi amministra il server va detto che può leggere i canali.
- **AI Act.** Ogni agente che scrive o parla a un esterno si dichiara AI (art. 50, dal 2/8/2026). Il coaching va solo all'interessato. Nessuna inferenza di emozioni. La valutazione del personale è ad alto rischio dal 2/12/2027 [verificato: 16§1-§4].

## 6. Piano a fasi

Il piano conta circa 1,2 persone a tempo pieno (Alberto, con Mattia a metà tempo) [stima].

| Fase | Settimane | gg-p | Cosa si vede alla fine |
|---|---|---|---|
| 0. Ferro e stanza | 1-2 | 8 | server in produzione (checklist 15§7), backup ripristinato una volta, buzz attivo per le 4 persone su PC e telefono |
| 1. Sala macchine e post-call | 3-5 | 16 | 4 agenti (@debrief, @postcall, @archivista, @smistatore), freno, gate con carte, Recall.ai. Dopo ogni call: recap nel canale cliente in pochi minuti, mail in approvazione, to-do in Notion. Debrief alle 7:00 nel DM di ciascuno |
| 2. Memoria e vendite | 6-9 | 22 | SersanOutreach sul server e collegato; pgvector; brief pre-meeting con slide; registro dei meeting; pipeline pesata v1; bozza d'offerta |
| 3. Marketing, coaching, voce | 10-14 | 20 | agenti marketing, loop G8, coaching conforme, "Andrea" dopo il parere legale, organigramma, banca dei token, `#premio` |
| 4. Scala | 15-20 | 15 | mappa dei processi aggregata, 25 agenti accesi, pilota Hermes per A6, primi gradi di autonomia |

Il **primo rilascio utile** è la fine della fase 1: **24 gg-p, 5 settimane**. Totale del programma: ~81 gg-p.

## 7. Costi mensili (EUR, IVA esclusa)

**Formula:**
`Fissi + Σ posti × prezzo + elettricità + UPS/60 + API (base del file 14 × k) + Recall.ai (ore × 0,65 $) + voce (minuti × 0,0445 $ + LLM) + proxy (GB × $/GB)`

- i dollari si convertono con 0,8934 [verificato: 14];
- k = 1,5 per i messaggi fra agenti nella stanza [stima];
- l'API resta coperta dai crediti (≤ 714,70 €) finché durano.

Gli importi vengono da 14§11 e 18§7. Differenze rispetto al file 14:
- Slack 0, perché buzz lo sostituisce (Slack Pro solo nel completo, come porta verso i clienti);
- Recall.ai al posto di Fireflies;
- il CRM è SersanOutreach (HubSpot facoltativo: +26,80 Starter, +160,81 Pro);
- Notion Plus nel minimo e nel consigliato;
- Proxmox Community a 10-20 €.

| Voce | Minimo | Consigliato | Completo |
|---|---|---|---|
| buzz, gate, memoria, giudice (self-host) | 0 | 0 | 0 |
| Notion | 35,74 (Plus) | 35,74 (Plus) | 71,47 (Business) |
| Slack | 0 | 0 | 27,00 (Pro) |
| Google Workspace | 27,20 | 54,40 | 54,40 |
| Instantly / Apollo / Apify | 33,59 | 128,30 | 486,28 |
| ElevenLabs + numeri Twilio | 0 | 128,65 | 347,54 |
| Metricool / moda / Higgsfield / Canva | 17,87 | 128,65 | 239,13 |
| 1Password, backup, Proxmox | 25,49 | 35,39 | 48,59 |
| Elettricità + UPS | 108,83 | 121,60 | 136,48 |
| **Fissi con il bundle Claude** | **248,72** | **632,73** | **1.410,89** |
| API Anthropic (base × 1,5) | 30,59 | 132,93 | 332,51 |
| Recall.ai (30 / 30 / 60 h) | 17,42 | 17,42 | 34,84 |
| Voce (minuti + LLM) | 0 | 41,63 | 146,07 |
| Proxy residenziali | 12,51 | 31,27 | 89,34 |
| **Totale** | **309,24** | **855,98** | **2.013,65** |
| **Esborso finché durano i crediti API** | **278,65** | **723,05** | **1.681,14** |
| **A regime (+446,70 di Claude Team)** | **755,94** | **1.302,68** | **2.460,35** |

Contro il consigliato del file 14 (780,20 + 161,50) il consigliato B costa circa 86 € in meno al mese. Spegnendo la VM Azure se ne risparmiano altri ~150 [non verificato: 14§9]. Una tantum: UPS da 1.163-1.293 €, più kit HPE e SSD non prezzati [14§11.3; 15§8]. Il file 15 stima la corrente a 28-70 €: il file 14 è più prudente e qui uso il suo valore.

## 8. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| buzz è pre-1.0, "Not finished", con release ogni 3-7 giorni [verificato: 17§2] | versioni fissate per digest, stage, prova di fumo prima di ogni aggiornamento |
| `buzz-acp` senza desktop su Linux non ha una guida passo per passo [non verificato: 17§7] | prova di 3 giorni all'inizio della fase 1; ripieghi: provider k3s, poi un ponte nostro sulla CLI `buzz` |
| prompt che non arrivano a `claude-agent-acp` (#7375); risposte doppie con Hermes (#7172) [verificato: 17§5] | istruzioni in `CLAUDE.md` nella cartella di lavoro [non verificato]; Hermes solo in fase 4 |
| notifiche push poco affidabili con il relay in casa; telefono con la stessa chiave del desktop [verificato: 17§2-§3] | carte anche su Telegram; telefono smarrito → rotazione della chiave |
| desktop Windows in alpha [verificato: 17§3] | agenti solo sul server, il PC fa da client |
| i clienti non entrano in buzz | B1 via email approvata o Slack Connect |
| doppia chat (WhatsApp, Teams) | i CEO decidono che buzz è la chat interna |
| Block cambia rotta | Apache-2.0, quindi fork possibile; dati nel nostro Postgres |
| 100 agenti sono 100 processi | definizioni nel catalogo, avvio su richiesta, 15-25 accesi |
| manutenzione affidata a una persona | runbook, Mattia secondo amministratore |
| giri e iniezioni | freno, corsie, tetti per chiave |

## 9. Perché sceglierla, e perché no

**Perché sì.**
- È l'unico prodotto self-hosted nato per "persone e agenti nella stessa stanza". Gli agenti sono membri veri, con nome, chiave, proprietario e memoria: è la forma di A7 e G9 senza doverla inventare.
- Licenza a 0 €, dati sul nostro server, app su desktop e telefono. Sostituisce Slack (27-60 € al mese).
- Accoglie qualunque cervello (Claude Code, Hermes, Codex, modelli locali), quindi il motore si cambia senza cambiare la stanza.
- Il primo valore arriva in 5 settimane.

**Perché no.**
- Ha sette mesi di vita. Le tre lacune bloccanti e le integrazioni le chiudiamo noi: 18-23 gg-p di codice nostro.
- Non ha integrazioni native.
- Push, mobile e Windows sono deboli.
- I clienti restano fuori.
- Il "cervello" (memoria, CRM pesato, voce, mappa dei processi) costa lo stesso lavoro in ogni proposta: buzz fa risparmiare solo sulla stanza.

Se i CEO vogliono maturità e clienti nello stesso canale, l'alternativa più sicura è Slack con Claude Tag o con il gateway di Hermes. Se vogliono la stanza propria e i dati in casa, B è la scelta coerente.
