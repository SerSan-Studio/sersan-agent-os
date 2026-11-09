# 20 · Proposta F: Paperclip come piano di controllo dell'azienda di agenti

**Data:** 24/10/2026. **Per:** Alessandro Serratt, Michele Sanna. **Angolo:** una delle sette architetture a confronto.

**Etichette.** [verificato: fonte] letto oggi o in un rapporto già verificato; [non verificato] stima o voce di terzi. Sigle delle fonti: **[P-rel]** note di rilascio v2026.1023.0; **[P-gh]** API GitHub del repo e dei suoi advisory, 24/10; **[01]…[18]** i rapporti in `ricerca/`.

---

## 1. L'architettura in una pagina

Paperclip (MIT, Node 24 + Postgres) fa da "direzione del personale" degli agenti: li mette in organigramma, assegna il lavoro come issue, li sveglia, conta la spesa, li ferma al tetto e chiede l'ok umano. Non esegue: il lavoro lo fanno lavoratori collegati da adattatori (Claude Code con chiave API, script, Hermes, webhook).

```
 PERSONE: Slack · web di Paperclip · telefono        ESTERNI: call, email, modulo del sito
 Board = Alessandro, Michele · Operatore = Alberto            │
        │ approvano, leggono, assegnano                         │ webhook (Cloudflare Tunnel)
┌───────▼──────────────────── SERVER DL380 · Proxmox ──────────▼──────────────────────┐
│ VM agents   PAPERCLIP (versione fissata): organigramma · obiettivi · issue ·        │
│             budget con stop · approvazioni · gateway strumenti Allowed/Ask/Off ·    │
│             routine cron/webhook · battito · registro attività · inbox attenzione   │
│               ├─ claude_local: Claude Code + chiave API, in sandbox bubblewrap      │
│               ├─ process/http: raccolta, pulizia, indicizzazione (niente LLM)       │
│               ├─ hermes (fase 3): agenti di fondo, gateway Telegram                 │
│               └─ webhook: SersanOutreach, ElevenLabs                                │
│ VM data     Postgres 17: db paperclip · db memoria + pgvector · db outreach         │
│ VM gpu      RTX 4000: embedding, giudice/redazione Qwen3-4B, Whisper                │
│ VM apps     SersanOutreach: CRM, coda HITL degli invii, MCP read/operator           │
└───────────────────────────────┬─────────────────────────────────────────────────────┘
                                ▼ API in uscita
 IN ABBONAMENTO: Anthropic API · Slack Pro · Fireflies o Recall.ai · ElevenLabs + Twilio ·
                 Notion · Metricool · moda.app · Instantly/Perplexity/Apify (già di SersanOutreach)
```

Cinque scelte che reggono il disegno:
1. **Il cervello è nostro.** La memoria (Notion più Postgres con pgvector) vive fuori, via MCP: per Paperclip è un "Anti-goal for core".
2. **Gli agenti si parlano attraverso il lavoro.** Si delega creando un'issue, con costo e responsabile; "A mention alone does not assign work or wake another agent". Slack è la vetrina, la bacheca il registro. buzz [17] resterebbe un'alternativa per la stanza interna, ma oggi non ha freno ai giri né approvazioni collegate: qui il freno sta nella bacheca.
3. **Ogni azione verso l'esterno parte in "Ask first"**, con gli argomenti esatti firmati: se cambiano dopo l'ok, il gateway rifiuta.
4. **Gli invii a lead nuovi restano in SersanOutreach**, che ha già l'approvazione umana sul testo [verificato: 01 §5.4].
5. **"Andrea" non passa dal battito di Paperclip** (tick di 30 s): la chiamata parte dal webhook del modulo, l'esito torna in Paperclip.

---

## 2. Tabella di copertura

Stati: **P** pronto · **A** da adattare · **C** da costruire · **S** in abbonamento · **Pr** processo interno.

| Voce | Componente | Stato | Fonte |
|---|---|---|---|
| A1 | Fireflies (consigliato; connettore Paperclip già presente) o bot Recall.ai (minimo), avviso nell'invito | S | [14 §4], [16 §1] |
| A2 | Notion per regole, processi e obiettivi + tabelle Postgres `memoria` (persone, aziende, riunioni), sincronizzate di notte | A | [12 §6] |
| A3 | pgvector + Qwen3-Embedding-0.6B sulla GPU + MCP `sersan-memoria` | C | [13 §7] |
| A4 | Paperclip più lavoratori Claude e Hermes | P | — |
| A5 | Reparto Memoria (raccolta, pulizia, indice) su adattatore `process`; reparti Commerciale, Marketing, Operazioni | A | — |
| A6 | Skill Studio (skill versionate, test, ripristino), agenti `learning` e `reflection-coach`; ogni nuova skill passa da approvazione | A | — |
| A7 | Thread delle issue + un bot Slack per agente con "Require at-mention" | P | [P-rel] |
| B1 | Agente post-call; canale Slack Connect per cliente, messaggio in Ask first | A | [P-rel]; Slack Connect su Pro [non verificato] |
| B2 | `record_meeting`, `update_deal`, `record_next_action` di `mcp_operator` | A | [01 §5.2] |
| B3 | Bozza Gmail (scope readonly + compose), invio umano | A | — (connettore Gmail in Developer Preview) |
| B4 | Issue di Paperclip assegnate alle persone (organigramma misto) | P | — |
| B5 | Autonomia per gradi: bozza → Ask first → regola revocabile "approva ancora uguale" | A | — |
| C1 | Routine delle 5:30 per persona; la status card non spende token se i fatti non cambiano | A | — |
| C2 | Bot Fireflies o Recall.ai | S | [14 §4] |
| C3 | Agente post-call su Sonnet 5.5 | A | [14 §1.5] |
| C4 | Dettatura delle app Claude dei posti Team | S | [non verificato] |
| C5 | Tabella `riunioni` + ricerca aziendale di Paperclip + estrazione "chi è caldo" | C | — |
| C6 | Pagine Notion "Come lavoro" diventano istruzioni dell'agente primario di ognuno | A | [P-rel] |
| D1 | Status card su `commercial_events` e deal; con 0 vinti e 0 persi si parte da stime a priori | C | [01 §1.4] |
| D2 | Agente `briefs` + ricerca web + enrich Perplexity + `reply_digest`; aperture mail dai webhook Instantly | A | [01 §5] |
| D3 | `commercial_events` + memoria | C | [01 §5.5] |
| D4 | moda.app o Canva via MCP | A | [14 §6] |
| D5 | Agente offerte (Opus) con il catalogo come skill, revisione obbligatoria | A | — |
| E1-E2 | Piano a fasi (§6) | Pr | — |
| E3 | Budget per azienda, agente e progetto (80 %, stop al 100 %), tetti giornalieri, registro costi esatto; una chiave API per reparto con limite in Console | P | [P-rel] |
| E4 | Alfabetizzazione AI Act art. 4 | Pr | [16 §4] |
| F1 | Script su metadati aggregati, mai individuali oltre 21 giorni | C | [16 §1.2] |
| F2 | Routine "intervista" | A | — |
| F3-F4 | Agente analista (Opus): mappa, ore stimate, automazioni in classifica | C | — |
| F5 | Un agente primario per persona | P | [P-rel] |
| G1 | Canale `#call-vendita` + un'issue per call | A | — |
| G2 | Fit score dalla trascrizione, che estende GP+BALD | C | [01 §1.2] |
| G3 | Agente coach; report come **issue privata** | A | [P-rel] |
| G4 | Al sales l'issue privata; al responsabile solo aggregati; nessuna emozione | A | [16 §1.2] |
| G5 | ElevenLabs Agents + numero Twilio IT, avviati dal webhook del modulo | S + C | [14 §3.4], [16 §2] |
| G6 | Routine settimanale che propone il nuovo attacco; la modifica del prompt va in Ask first | C | — |
| G7 | Status card dei KPI | A | — |
| G8 | `lost_deal_analysis` → issue al Marketing | A | [01 §5.1] |
| G9 | Organigramma con `reportsTo`, esportabile in SVG, squadre dal catalogo | P | — |
| G10, H1, H7, I1, I2 | Adozione e contesto (I2 = A1-A3) | Pr | — |
| H2 | I CEO nel Board: approvano strategie, assunzioni di agenti, budget | P | — |
| H3 | Routine di intervista per reparto | A | — |
| H4 | Ruolo "ambassador" con budget più alto | P | — |
| H5 | Ognuno crea agenti in un proprio progetto privato, entro il budget | P | [P-rel] |
| H6 | Routine mensile che elenca i candidati dall'attività; decide il Board | A | — |
| I3 | Gateway "Off" + elenco nelle istruzioni aziendali + progetti senza agenti | P | — |
| I4 | Squadra `content-machine` del catalogo adattata ai 5 ruoli di [05] | A | [05 §5] |

**Conteggio:** 10 P, 22 A, 9 C (più metà di G5), 4 S, 8 Pr. Paperclip copre la **governance**: organigramma, budget, approvazioni, routine, to-do. Non copre il **cervello** (A2-A3, C5, D1, D3, F) né la voce, che vanno costruiti.

---

## 3. Cosa gira sul server e cosa in abbonamento

| VM (Proxmox, [15 §5.1]) | Contenuto | vCPU | RAM | Disco |
|---|---|---|---|---|
| agents | Paperclip + lavoratori Claude Code (al massimo 10 run insieme) + Hermes in fase 3 | 8 | 24 GB | 150 GB |
| data | Postgres 17 con pgvector: tre database, ruoli separati | 4 | 24 GB | 300 GB |
| gpu | llama-server (Qwen3-4B, embedding 0.6B), faster-whisper | 4 | 16 GB | 60 GB |
| apps-prod | SersanOutreach (8 servizi, tetti misurati 7,4 GiB), Traefik, cloudflared | 6 | 20 GB | 100 GB |
| apps-stage | prova degli aggiornamenti di Paperclip e di SersanOutreach | 4 | 12 GB | 80 GB |
| monitor, pbs | Prometheus, Grafana, Loki; backup | 4 | 10 GB | dischi propri |

Totale: circa 106 GB più 12-16 GB per host e ZFS. Sta nei 128 GB bilanciati; con 192 GB c'è spazio per più run in parallelo [non verificato: stima; una sessione Claude Code pesa 0,5-1 GB, da 17 §7]. A Paperclip la GPU non serve. Il log di ogni run ha un tetto di 4 MB: con una ritenzione di 90 giorni restano pochi GB.

**Sul server** (costo basso, dati in casa, modello a scelta): piano di controllo, memoria, embedding, redazione dei dati personali, trascrizione di riserva, SersanOutreach. **In abbonamento**, perché in casa non si fa bene: modelli di frontiera (non entrano in 8 GB), bot nelle call, telefonia italiana, canale umano (Slack), pagine scritte a mano (Notion). Paperclip Cloud non serve ed è solo in lista d'attesa [verificato: README].

---

## 4. Come si collegano SersanOutreach e il marketing

**SersanOutreach** si sposta su `apps-prod` con i 10 passi di [01 §4.11]. Lo stesso dominio evita di ricostruire l'estensione. Il database va in `data`, così la latenza scende dai 35 ms di oggi a quasi zero [verificato: 01 §4.7]. Tre collegamenti:
1. **MCP.** `mcp_server` (19 strumenti) e `mcp_operator` (14 operazioni) oggi parlano solo su stdio: serve un involucro HTTP autenticato dentro la rete del server [verificato: 01 §5.10], registrato in Paperclip come "MCP remoto". Allowed: letture, `record_meeting`, `record_next_action`, `generate_drafts` (non approva mai). Ask first: `update_deal`, `change_deal_stage`. Off: `approve_message`, che resta a una persona nell'app.
2. **Webhook.** Per risposta positiva, meeting fissato e modulo inbound servono webhook da SersanOutreach verso le routine di Paperclip: oggi esistono solo notifiche Telegram, quindi vanno scritti [verificato: 01 §5.6]. Il modulo inbound chiama anche ElevenLabs.
3. **Identità.** Una famiglia `X-Caller-Token` dedicata a Paperclip, con `AUTH_IDENTITY_MODE=enforce` prima di collegare: oggi è in `observe` [verificato: 01 §6].

Valgono sempre: una sola lista di soppressione, letta da ogni agente con un canale esterno; LinkedIn solo dal browser del membro, senza tecniche anti-rilevamento.

**Marketing.** La squadra `content-machine` del catalogo si adatta ai ruoli di [05 §5]: editoriale, copy, visual, analisi, pubblicazione. Le regole di casa vietano le scritture su Metricool da routine, task e loop [verificato: 05 §5]. Quindi in Paperclip i 4 strumenti di scrittura di Metricool partono **Off**: gli agenti consegnano pacchetti pronti (testo, file, alt, orario) come allegati dell'issue, e li pubblica la sessione presidiata di Alberto.

Il loop G8 porta obiezioni e motivi delle chiusure perse nel calendario editoriale; il digest del lunedì unisce Metricool (in lettura) e i KPI di SersanOutreach.

**Decisione per i CEO:** accettare "Ask first" con argomenti firmati come equivalente della sessione presidiata. È un cambio di regola di casa.

---

## 5. Controllo e sicurezza

**Approvazioni.** Tre meccanismi imposti dal runtime, non dal prompt: stadi di revisione sulle issue, approvazioni del Board (nuovi agenti, strategie, budget), gateway degli strumenti. I CEO approvano offerte, messaggi ai clienti, budget e nuovi agenti; Alberto connettori e configurazione; ogni sales i propri follow-up. Le regole "approva ancora uguale" arrivano solo dopo un periodo misurato, mai per invii a lead nuovi, chiamate, pubblicazioni, cancellazioni o pagamenti. Le decisioni scadono dopo 7 giorni di default: per noi una scadenza vale come no, e si richiede.

**Due difetti di partenza**: l'adattatore Claude parte con `dangerouslySkipPermissions: true` e il filtro anti-iniezione sono quattro regex in inglese. Correzioni: sandbox bubblewrap con rete in allowlist (spenta di default); utente Linux separato per i lavoratori; nessuno strumento d'invio nelle sessioni; preset `low_trust_review` per chi legge email e trascrizioni, da cui non risale prosa verso contesti più fidati; scanner in italiano come filtro MCP.

**Storia di sicurezza** [verificato: P-gh]: 12 advisory, 6 critici, tra cui RCE senza autenticazione (aprile 2026), RCE via DNS rebinding sulle istanze locali (luglio 2026), IDOR sulle chiavi tra aziende, un agente Codex che ha ereditato Gmail e mandato email vere. Contromisure: modalità `authenticated` + `private`, mai `local_trusted`; interfaccia solo da VPN o Cloudflare Access; VM dedicata senza altri segreti; telemetria spenta (è accesa di default); iscrizione agli advisory.

**Audit.** Ci sono `activity_log`, `tool_call_events` (in sola aggiunta per costruzione delle route) e il registro delle letture dei segreti, ma nessuna catena di hash. Va aggiunto un export notturno firmato con hash, fuori dal server (1-2 giorni).

**Budget.** I tetti di Paperclip guardano la spesa registrata, quindi un run in corso può sforare; dalla v2026.1023.0 un uso senza prezzo vale come tetto raggiunto [verificato: P-rel]. Secondo argine: limiti per chiave API nella Console Anthropic. Emergenza: pausa dell'azienda in Paperclip e kill switch degli invii in SersanOutreach.

**GDPR** [16]: i dati stanno in Postgres sul server, in UE se l'ufficio è in Sardegna (ubicazione non nei file); l'API Anthropic conserva 30 giorni, in USA o `global`. Via UE: la release del 23/10 instrada Claude su Amazon Bedrock [verificato: P-rel], che ha profili di inferenza UE [verificato: 16 §5]. L'approvazione `hire_agent` è il punto in cui ogni nuovo agente porta la sua riga del registro e la DPIA. Un lavoro notturno cancella alle scadenze (audio 30 giorni, log 90).

**AI Act:** chi scrive o parla a esterni si dichiara AI (art. 50, dal 2/8/2026). Il coaching sta in issue private, che admin e owner aprono solo in "break glass" con riga d'audit [verificato: P-rel]: non diventa così la valutazione dei lavoratori dell'Allegato III, alto rischio dal 2/12/2027 [verificato: 16 §4].

---

## 6. Piano a fasi

| Fase | Settimane | gg-persona | Lavoro | Cosa si vede alla fine |
|---|---|---|---|---|
| 0 Fondamenta | 1-2 | 6 | Server secondo [15 §7]; VM `agents` e `data`; Paperclip v2026.1023.0 in Docker su Postgres esterno; accessi, telemetria spenta, staging | I CEO entrano in Paperclip, vedono l'organigramma con 3 agenti e budget a zero |
| 1 Post-call e debrief | 3-4 | 12 | Webhook Fireflies o Recall → routine → agente post-call; MCP HTTP di SersanOutreach; schema minimo `riunioni`; bot Slack; budget e Ask first | Dieci minuti dopo una call: riepilogo in Slack, deal aggiornato, bozza di mail, to-do assegnati. Alle 5:30 il debrief |
| 2 Memoria e vendite | 5-9 | 25 | pgvector, sincronizzazione Notion, MCP memoria; brief, offerte, slide; coach privato; card della pipeline; migrazione di SersanOutreach; bozze del marketing | Brief da una email in 5 minuti; bozza d'offerta dopo la call; "cosa ci siamo detti con X" |
| 3 Voce, processi, autonomia | 10-16 | 25 | "Andrea" dopo il parere legale; ciclo che impara dai rifiuti; mappa dei processi aggregata; budget per persona; premio; prime regole di fiducia; Hermes per 2-3 agenti di fondo | Lead richiamata in 90 secondi; mappa dei processi; 25 agenti in organigramma |
| 4 Regime | continuo | 2 al mese | Aggiornamento mensile passato da staging, revisione dei budget, nuovi agenti del team | Verso 50-100 righe in organigramma, molte senza LLM |

**Primo rilascio utile:** fasi 0 e 1, 18 giorni-persona, circa 4 settimane. **Totale fino alla fase 3:** 68 giorni-persona [non verificato: stima].

---

## 7. Costi mensili (EUR, IVA esclusa)

**Formula:** `Costo = Fissi[14 §11.1] + Variabili[14 §11.2] + Δ_F`. La differenza propria di questa architettura è:

`Δ_F = Paperclip (0, MIT) + Proxmox Community + run × 0,05 $ × 0,8934 + Tailscale (solo nel completo)`

| Voce | Minimo | Consigliato | Completo |
|---|---|---|---|
| Fissi con il bundle Claude [14] | 248,70 | 780,20 | 1.652,60 |
| Variabili, API comprese [14] | 50,30 | 161,50 | 457,10 |
| Proxmox Community, 2 socket [15 §8] | 0 | 20,00 | 20,00 |
| Sovraccosto dei run di coordinamento [stima] | 16,08 (360 run) | 67,01 (1.500 run) | 160,81 (3.600 run) |
| Tailscale, 4 utenti se c'è CGNAT [15 §4.4] | 0 | 0 | 28,59 |
| **Totale con il bundle** | **≈ 315** | **≈ 1.029** | **≈ 2.319** |
| A regime, senza bundle (+446,70) | ≈ 762 | ≈ 1.475 | ≈ 2.766 |
| Esborso mentre durano gli 800 $ di crediti (meno la riga API) | ≈ 279 | ≈ 873 | ≈ 1.937 |
| VM Azure spenta [non verificato] | −150 | −150 | −150 |

**Ipotesi dei run** [stima]: 6, 25 e 40 agenti con LLM, da 2 a 3 run al giorno ciascuno. Ogni run costa in media 0,05 $, tra Sonnet e Haiku a cache fredda. L'uso API resta sotto i crediti: circa 156 € nel consigliato e 382 € nel completo, contro 714,70 € [verificato: 14 §1.5]. Hermes Cloud (20 $ di crediti + 17-33 $ di istanza) [non verificato: 18 §2.4] e Claude Tag restano fuori: sono riserve. Una tantum: UPS da 1.163-1.293 € e i kit del server [14 §11.3].

---

## 8. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| Progetto giovane: nato il 2/3/2026; l'ultima release porta 200 commit e breaking change (permessi degli Operator, budget sugli usi senza prezzo) [verificato: P-gh, P-rel] | Versione fissata, staging, aggiornamento mensile dopo le note |
| Dipendenza da una persona: il primo contributore ha 3.426 commit, il secondo 835 [verificato: P-gh] | MIT con fork possibile; la nostra logica sta in skill, MCP e Postgres; esportazione dell'azienda |
| Superficie d'attacco (§5) | Rete chiusa, VM dedicata, advisory monitorati |
| 488.000 righe di server che non possiamo leggere | Usarlo come scatola nera via API; niente fork salvo emergenze |
| Memoria e voce assenti | Costruite fuori: sono il grosso delle fasi 2 e 3 |
| Con la chiave API i connettori di claude.ai non ci sono | Connettori come MCP diretti in Paperclip; per Notion, Canva e moda va verificato che il server MCP ospitato esista |
| Iniezioni da email e trascrizioni | Preset low-trust, campi strutturati, scanner italiano |
| Pipeline senza storico (0 vinti) | Probabilità a priori dichiarate tali fino a 20-30 esiti |
| Termini Anthropic | Chiave API per ogni lavoratore automatico; i posti Team solo per le persone [verificato: 10 §6] |
| Un'interfaccia in più | Il team resta in Slack; Paperclip lo aprono i CEO per approvare, Alberto per operare |

---

## 9. Perché sceglierla, e perché no

**Perché sì.**
- Organigramma (G9), banca dei token (E3), approvazioni (B5, H2), routine (C1) e to-do (B4) sono **pronti dal primo giorno**: le parti di governance che altrove si scrivono a mano.
- **Nessun vincolo di modello.** Oggi Claude via API; domani Hermes, Codex, un modello locale o OpenAI Dot (in prova [verificato: P-rel]), con lo stesso organigramma. Claude via Bedrock UE apre la residenza dei dati.
- Le issue private si adattano al coaching conforme.
- La comunità è grande: 106.904 stelle, 17.756 fork [verificato: P-gh].
- I dati stanno sul nostro server.

**Perché no.**
- Copre la **governance**, non il **cervello**. Memoria, registro delle riunioni, pipeline pesata, mappa dei processi e voce, cioè metà del valore della visione di Alberto, si costruiscono comunque.
- È un software di 8 mesi, con 6 advisory critici nel 2026 e rilasci ogni 1-2 settimane, l'ultimo con breaking change.
- I suoi default (bypass dei permessi, telemetria, filtro anti-iniezione in inglese) vanno chiusi da noi.
- Costa circa 2 giorni al mese di manutenzione, a carico di Alberto.

Per un primo risultato senza dipendere da un progetto giovane conviene un'architettura più sottile; per arrivare davvero a decine di agenti con contabilità e controllo pronti, questa.
