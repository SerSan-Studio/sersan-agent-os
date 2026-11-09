# 20 · Proposta D: la forza lavoro di agenti OpenAI (Dots e Workspace Agents), con il cervello in casa

**Data:** 24/10/2026. **Per:** Alessandro Serratt e Michele Sanna. **Angolo:** gli agenti OpenAI fanno il lavoro operativo. Il server SerSan tiene i dati, SersanOutreach, la memoria e la trascrizione. Claude resta per il codice e per i testi.

**Etichette.** `[verificato: fonte]` = letto in un rapporto di `ricerca/` (con il numero) o su una pagina ufficiale. `[non verificato]` = fonte terza, stima o ipotesi. Nessun file richiesto manca.

---

## 1. L'architettura in una pagina

- **Agenti OpenAI (cloud).**
  - Ogni posto ChatGPT Business Premium dà **un dot**: un agente sempre acceso su GPT-6 Astra, con un computer Linux e Chrome nel cloud, oltre 4.000 app via plugin (MCP con OAuth 2.1) e regole a quattro livelli [verificato: 18 §2.2].
  - Accanto ci sono i **Workspace Agents** di Business: agenti condivisi con nome e handle Slack. Partono a orario, da Slack o da una chiamata API (`202`) e usano MCP personalizzati. Le scritture sono su "Always ask" di default, con vincoli come "destinatari solo di questo dominio" [verificato: help.openai.com 20001143, via proxy, 24/10].
  - I dot sono gli assistenti delle persone; i Workspace Agents sono l'organigramma.
- **Server SerSan (Proxmox).** Ospita SersanOutreach, la memoria (Postgres e pgvector), la trascrizione su GPU, gli agenti di fondo e un **gateway MCP**. Il gateway è l'unica porta tra il cloud e i nostri dati: registra, chiede approvazioni e conta la spesa.
- **Claude.**
  - I posti Team servono alle persone per Claude Code e per i testi.
  - La chiave API (crediti da 800 $) fa girare gli agenti automatici sul server e lo strumento "redigi con Claude" che il gateway offre ai dot. Così l'uso automatico passa sempre dalla chiave API.

```
PERSONE (4): Claude Team (codice, testi) + ChatGPT Business (2 Premium, 2 Standard)
        |
SLACK: #sala-agenti  #cliente-<nome>  #call-vendita  #approvazioni
        ^  handle Slack degli agenti
CLOUD OPENAI (USA)
  dot personali: computer + Chrome, promemoria, regole a 4 livelli
  Workspace Agents: Post-call, Brief, Offerte, Pipeline, Editoriale, Metriche, Coach
        |  MCP remoto, OAuth 2.1          ^  trigger API
SERVER SERSAN, dietro Cloudflare Tunnel
  gateway "sersan-mcp": azioni negate per default, carte, audit, spesa, soppressione
  SersanOutreach (8 servizi, Postgres locale, MCP 19 letture + 14 operazioni)
  memoria: Postgres + pgvector (call, mail, documenti, meeting)
  GPU: Whisper/Parakeet, pyannote, embedding, giudice 4B per pseudonimizzare
  agenti di fondo (raccolta, pulizia, indici) con Claude API; scheduler eventi
ESTERNI: Recall.ai (bot riunioni), ElevenLabs + Twilio IT ("Andrea"),
         Notion (regole, processi), Metricool (solo sessione presidiata)
```

---

## 2. Tabella di copertura (A1-I4)

Fonti: numeri = rapporti in `ricerca/`; **WA** = help.openai.com 20001143; **RC** = help.openai.com 11481834 (rate card); **SP** = spotdev.co.uk [non verificato: terzi].

| Voce | Componente | Stato | Fonte |
|---|---|---|---|
| A1 Riunioni registrate e dichiarate | bot Recall.ai, STT sul server, avviso nell'invito | da adattare | 13 §5, 16 §1 |
| A2 Second brain relazionale | Notion (regole, processi) e Postgres (CRM) | da adattare | 01 §5.5 |
| A3 Database vettoriale | pgvector e Qwen3-Embedding, via gateway | da costruire | 13 §7 |
| A4 Orchestratore | dot e Workspace Agents; regia degli eventi sul server | in abbonamento | 18 §2.2, WA |
| A5 25 agenti per ruolo | fondo: worker con Haiku 5.5; azione: Workspace Agents | da costruire | 13 §10 |
| A6 Imparano | il dot "impara dal feedback" (meccanismo non spiegato); revisione mensile delle regole | da adattare | — |
| A7 Chat tra agenti | `#sala-agenti`; i messaggi tra agenti passano dal server | da adattare | WA; nativo: non trovato |
| B1 Recap nel canale cliente | trascrizione, poi trigger di "Post-call" | da adattare | WA |
| B2 Opportunità sul CRM | `update_deal`, `record_meeting` via gateway | da adattare | 01 §5.2 |
| B3 Mail di follow-up | bozza su Gmail; invio su "Always ask", solo al dominio del cliente | in abbonamento | WA |
| B4 To-do | `record_next_action` e Notion | da adattare | 01 §5.2 |
| B5 Autonomia totale | autonomia per gradi (§5) | da adattare | 16 §6 |
| C1 Debrief del mattino | promemoria ricorrente del dot | in abbonamento | 18 §2.2 |
| C2 Agente nelle call | bot Recall.ai (dot nelle riunioni: non trovato) | in abbonamento | 14 §4 |
| C3 Analisi con Claude | "analizza_call" del gateway, Sonnet 5.5 | da costruire | 13 §10 |
| C4 Dettatura | voce in ChatGPT e Claude; Whisper locale | pronto | 13 §5 |
| C5 Registro di tutti i meeting | tabella dei meeting con ricerca; "Pipeline" settimanale | da costruire | 01 §5.5 |
| C6 Regole personali | Notion e regole del dot | da adattare | 18 §2.2 |
| D1 Pipeline pesata | portale fatto con Claude Code; con 0 vinti per ora è descrittiva | da costruire | 01 §1.4 |
| D2 Brief pre-meeting | dot con browser, più CRM e aperture dal gateway; LinkedIn escluso | in abbonamento | 18 §3 |
| D3 Storico della relazione | query del gateway | da adattare | 01 §5.5 |
| D4 Slide | Pages di ChatGPT [non verificato: terzi], moda.app, Claude Slides | in abbonamento | 05 §5.8 |
| D5 Offerta | "Offerte" monta il materiale, Claude Opus scrive, una persona approva | da costruire | 13 §10 |
| E1 Curva di apprendimento | fasi 0-1 con i CEO | da adattare | — |
| E2 Costo dei token | §7 | pronto | 14 §1.5 |
| E3 Banca dei token | crediti OpenAI prepagati; contatori Claude nel gateway | da costruire | RC |
| E4 Formazione | un'ora documentata per agente nuovo | da adattare | 16 §4 |
| F1 Metadati del Workspace | aggregati; quelli individuali per non più di 21 giorni | da costruire | 16 §1.2 |
| F2 Interviste | "Intervistatore" nei DM di Slack | da adattare | WA |
| F3 Mappa dei processi | Opus su dati aggregati | da costruire | — |
| F4 Ore e automazioni | stesso agente | da costruire | — |
| F5 AI per tutti | ChatGPT e Claude per i quattro | pronto | 18 §2 |
| G1 Canale call di vendita | `#call-vendita` | da adattare | WA |
| G2 Fit score | qualificatore GP+BALD e lettura della call | da adattare | 01 §1.1 |
| G3 Coaching | report privato al solo interessato | da adattare | 16 §1.2 |
| G4 Report al responsabile | solo indicatori aggregati | da adattare | 16 §4 |
| G5 "Andrea" in 90 secondi | ElevenLabs e Twilio IT, attivati dal webhook (il dot non può chiamare) | in abbonamento | 14 §3.4, 18 §2.2 |
| G6 Imparare dai rifiuti | valutazione mensile; prompt approvato | da costruire | 16 §2 |
| G7 KPI | Grafana e funnel | da adattare | 01 §5.5 |
| G8 Lead chiusa → marketing | "Editoriale" legge `lost_deal_analysis` | da adattare | 05 §5.6 |
| G9 Organigramma | registro in Notion e handle Slack degli agenti | da adattare | WA |
| G10 Superpotere | effetto dell'insieme | pronto | — |
| H1 Formarsi e sperimentare | un dot per CEO | da adattare | — |
| H2 Non delegabile | i CEO usano il debrief ogni giorno | pronto | — |
| H3 Assessment | "Intervistatore" | da adattare | — |
| H4 Ambassador | posto Premium a chi è più avanti | pronto | — |
| H5 Tutti costruiscono | l'admin decide per ruolo chi costruisce | pronto | WA |
| H6 Premio mensile | Agent Analytics e voto | da adattare | WA |
| H7 Le licenze non bastano | rituali delle fasi | da adattare | — |
| I1-I2 Contesto | memoria in casa | da costruire | 13 §10 |
| I3 Aree senza AI | policy, con blocchi nelle regole e nel gateway | da adattare | 05 §5.8 |
| I4 Marketing 70/30 | Editoriale e Metriche in lettura | da adattare | 05 §5 |

---

## 3. Cosa gira sul server e cosa in abbonamento

**Sul server** (VM da 15 §5.1; somme mie, [non verificato: stima]):

| VM | vCPU / RAM | Contenuto |
|---|---|---|
| apps-prod | 8 / 32 GB | SersanOutreach (tetti 7,4 GiB [verificato: 01 §4.2]), cloudflared, gateway, scheduler, worker |
| data | 4 / 24 GB | Postgres 17 con pgvector |
| gpu | 4 / 16 GB + RTX 4000 | giudice 4B, embedding, Whisper turbo int8 (circa 1,5 GB) [verificato: 13 §8] |
| monitor, pbs | 4 / 10 GB | Prometheus, Grafana, backup |

In tutto sono circa 82 GB su 128-160. Il disco è un mirror ZFS di 2 SSD con PLP. 1-2 TB bastano: il dump di SersanOutreach pesa 6,2 GB [verificato: 01 §3.3] e l'audio si cancella entro 30 giorni.

**In casa** stanno dati dei clienti, trascrizioni ed embedding: Anthropic non vende embedding, e il lavoro di fondo con Haiku 5.5 costa 0,10 $ e 0,50 $ per milione di token [verificato: 13 §0].

**In abbonamento** stanno dot e Workspace Agents (computer isolati, browser, identità Slack, app, permessi), la telefonia e i modelli di frontiera: sul server andrebbero costruiti e messi in sicurezza a mano [verificato: 18 §1].

---

## 4. SersanOutreach e marketing

1. **Migrazione.** Si segue la checklist di 01 §4.11, con Postgres locale. `outreach.sersan.io` resta, dietro Cloudflare Tunnel, così l'estensione non va ricostruita [verificato: 01 §4.4; 15 §0].
2. **Gateway.** Gli MCP di oggi sono stdio: ChatGPT sul web richiede HTTPS e OAuth, che non esistono [verificato: 01 §5.1]. Il gateway li espone con OAuth 2.1, dopo aver portato a `enforce` l'identità firmata [verificato: 01 §6]. Approvazione in blocco, lancio e `send-control` non si espongono mai. Approvare non è inviare [verificato: 01 §5.2].
3. **Eventi.** Una risposta positiva arriva allo scheduler, che attiva "Follow-up". La bozza va in `#approvazioni`.
4. **LinkedIn.** Solo da SersanOutreach, con l'estensione e il sì umano [verificato: 18 §3]. Il Chrome dei dot non apre linkedin.com: c'è una regola di blocco e il controllo nell'audit. Che il blocco funzioni per dominio [non verificato].
5. **Marketing.**
   - "Editoriale" propone gli slot da obiezioni, rifiuti e temi delle call.
   - "Metriche" prepara i numeri del lunedì in sola lettura.
   - Copy e pubblicazione restano a Claude Code in sessione presidiata: nessuna routine scrive su Metricool [verificato: 05 §3.7, §5].

---

## 5. Controllo e sicurezza

- **Due barriere.**
  - **OpenAI.** Il dot ha quattro livelli (agire, agire se pre-approvato, chiedere, passare la mano), una revisione da un secondo modello e regole fisse su password e denaro. I Workspace Agents chiedono prima di ogni scrittura e accettano vincoli [verificato: WA].
  - **Il gateway.** Il cloud non lo aggira. Ogni azione è negata per default. Ogni carta mostra il contenuto esatto. L'approvazione si consuma prima dell'esecuzione ed è legata all'impronta del testo.
- **Autonomia per gradi** [non verificato: proposta].
  - Si parte con "chiedere" su ogni azione esterna.
  - Un tipo di azione passa a "pre-approvato" dopo 20 approvazioni pulite e un sì scritto dei CEO.
  - Pagamenti, LinkedIn, offerte e contratti restano a "passare la mano".
- **Iniezioni.** Nei test di OpenAI 16.600 email d'attacco hanno dato zero successi, ma restano "vulnerabilità note"; le violazioni salgono dall'8,6% al 19,7% da catene di 5 a 10 task. Contromisure: catene corte con contesto nuovo, mail e web trattati come dati, etichette MCP "sola lettura" e "distruttivo".
- **Arresto.** La pausa del dot non ferma i task pianificati [verificato: 18 §2.2]. Fermarli è compito nostro: revoca dei token del gateway, `send-control` di SersanOutreach, agenti spenti dall'admin. La procedura si prova ogni mese.
- **Audit.** Business non ha audit log né Compliance API [non verificato: SP]. L'audit sta quindi nel gateway, in append-only.
- **Budget.** I crediti OpenAI si comprano prima e fanno da tetto [verificato: RC]. Claude ha i contatori per agente, con un avviso all'80%.
- **GDPR.**
  - OpenAI Business firma il DPA con OpenAI OpCo LLC (USA), con SCC e Addendum UK.
  - Niente addestramento di default, nessuna residenza dei dati UE o UK, SOC 2 ma non ISO 27001 [non verificato: SP, 15/07/2026].
  - I dati dei lead non vanno nella memoria del dot, che non si cancella selettivamente. Al cloud arrivano estratti pseudonimizzati.
  - Servono una DPIA, la conservazione automatica e un'unica lista di soppressione [verificato: 16 §6].
- **AI Act.**
  - Ogni agente che scrive a un esterno si dichiara AI (art. 50).
  - Il coaching non dà voti e non legge le emozioni.
  - "Andrea" parte solo con consenso, controllo RPO e numero italiano [verificato: 16 §2, §4].

---

## 6. Piano a fasi

| Fase | Settimane | Giorni-persona | Cosa si vede alla fine |
|---|---|---|---|
| 0 Verifiche | 1 | 3 | conferma scritta di OpenAI sul dot in Business Premium UK; DPA; prezzo del credito; regole dei dot |
| 1 Valore subito | 1-2 | 5 | dot di Alessandro con debrief e brief; "Post-call", "Brief" e "Follow-up" in Slack su "Always ask"; Recall.ai con avviso |
| 2 Server e memoria | 3-6 | 20 | infrastruttura e backup (5); SersanOutreach migrato e Azure spento (7); pgvector e STT (3); gateway con audit (5) |
| 3 Commerciale e marketing | 7-9 | 12 | canale per cliente con recap, opportunità e to-do; offerta in bozza il giorno dopo; Editoriale e Metriche |
| 4 Voce, processi, organigramma | 10-13 | 12 | "Andrea" dopo il parere legale; mappa dei processi; organigramma; banca dei token |

Il primo rilascio utile sono le fasi 0 e 1: **8 giorni-persona in 2 settimane**, senza aspettare il server. Il totale è di circa 52 giorni-persona [non verificato: stima].

---

## 7. Costi mensili

**Formula.** Costo = Σ(posti ChatGPT × prezzo) + crediti OpenAI (tetto) + Slack + Notion + ore di riunione × 0,65 $ + voce (piano ElevenLabs + minuti × 0,0445 $ + numeri) + corrente + backup − VM Azure.

- I token Claude restano entro gli 800 $ di crediti: anche il carico completo vale circa 248 $ [verificato: 14 §1.5].
- Claude Team costa 0 finché c'è il bundle, 446,70 € a regime [verificato: 14 §11.1].
- Cambio 0,8934 €/$, IVA esclusa, pagamento mensile.

| Voce | Minimo | Consigliato | Completo | Fonte |
|---|---|---|---|---|
| ChatGPT Business | 1P+1S: 150 $ | 2P+2S: 300 $ | 4P: 500 $ | 18 §2.2 [non verificato: terzi] |
| Crediti OpenAI (tetto) | 50 $ | 150 $ | 400 $ | [non verificato: ipotesi] |
| Slack | 0 | 27,00 € | 60,00 € | 14 §11.1 |
| Notion | 35,74 € | 71,47 € | 71,47 € | 14 §11.1 |
| Recall.ai | 30 h: 19,50 $ | 60 h: 39 $ | 120 h: 78 $ | 14 §4 |
| Voce "Andrea" | 0 | 170,28 € | 493,61 € | 14 §11 |
| Corrente | 89,43 € | 102,20 € | 114,98 € | 14 §8.1 |
| Backup, Proxmox | 3,20 € | 3,10 € | 26,30 € | 14, 15 §8 |
| **Totale** | **≈ 324 €** | **≈ 811 €** | **≈ 1.640 €** | |
| Senza VM Azure (−150 €) | ≈ 174 € | ≈ 661 € | ≈ 1.490 € | 14 §9 [non verificato] |

**Il punto debole del conto.** Il prezzo del credito OpenAI non l'ho trovato. Il rate card dà 5-25 crediti per un'esecuzione tipica di un Workspace Agent [verificato: RC]. Con 1.500 esecuzioni al mese servono 7.500-37.500 crediti. Per questo il tetto è un limite di spesa, non una stima: si tara in fase 1, e se il conto sale il volume passa a Claude API.

---

## 8. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| Dots è nuovo (29/09); nelle prime 48 ore persi permessi e messaggi [non verificato: terzi] | un solo dot pilota; "chiedere" su ogni azione esterna |
| In UK il dot arriva solo con Business Premium; i Workspace Agents in UK non sono confermati | conferma scritta prima del canone annuale |
| Prezzo del credito ignoto | crediti prepagati; il volume passa a Claude API |
| Memoria del dot opaca, lock-in | la memoria vera è in casa; regole versionate in git |
| Dati negli USA, niente audit su Business | minimizzazione e audit nel gateway; Enterprise se un cliente lo chiede |
| Dialogo tra agenti non nativo, rischio di cicli | relay sul server con un tetto di turni |
| Due fornitori di AI | confini netti: OpenAI fa le operazioni, Claude codice e testi |
| Un solo amministratore | runbook e un secondo amministratore |

---

## 9. Perché sceglierla, e perché no

**Perché sì.**
- Dà valore in due settimane, senza server.
- Computer, browser, Slack, routine e permessi sono già fatti e testati.
- I CEO usano un'app e la voce.
- I dati restano in casa.
- Claude resta dove è più forte.

**Perché no.**
- Non è l'orchestratore open source previsto dalla visione di Alberto.
- Si pagano due fornitori.
- I dati operativi vanno negli USA.
- Il prezzo dei crediti è ignoto.
- Gli agenti non dialogano tra loro in modo nativo (Grok Bot sì).
- La memoria del dot è opaca.
- Il prodotto ha meno di un mese.
