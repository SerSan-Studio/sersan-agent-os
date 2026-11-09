# 36 · Architettura v2: il motore degli agenti sull'Agent SDK, dentro il board di Michele

**Data:** 25/10/2026. **Per:** Alberto Tuveri. Serve a riscrivere la proposta per Alessandro Serratt (CEO) e Michele Sanna (CPTO), e come piano tecnico per Mattia Scattu.
**Cosa chiude:** la scelta dell'architettura dopo le tre proposte del 25/10 (`34-proposta-1-agent-sdk.md`, `34-proposta-2-hermes-self-hosted.md`, `34-proposta-3-claude-team-e-mcp.md`) e i quattro giudizi (`35-giudizio-visione.md`, `35-giudizio-ceo.md`, `35-giudizio-cpto.md`, `35-giudizio-sicurezza.md`).
**Vincolo fisso:** il board di Michele (`allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`). In cloud restano solo M365/Entra ID, Claude Team, l'API Anthropic dietro LiteLLM, Cloudflare (DNS), GitHub, Supabase, Vercel, Jira, Instantly e uno spazio S3 facoltativo. Azure esce. Tutto il resto è self-hosted [verificato: board-testo-completo.txt righe 12-33; messaggio di Michele del 25/10/2026].
**Regola di Alberto, sopra ogni altra:** nessuna funzione A1-L12 e nessuna integrazione si toglie, si rimanda a "forse" o si declassa perché oggi manca un componente. Per ognuna questo documento scrive il componente che la realizza e, se manca, cosa serve per averla: acquisto, abbonamento, servizio da installare, configurazione, giorni. Ciò che non può stare sul server è una necessità esterna con il suo costo, non una rinuncia.
**Fonti:** i rapporti 25-35, `PRESENTAZIONE-CEO.md`, `00-visione-funzionalita.md`, `01`, `22`; pagine web lette il 25/10/2026 (elenco nel §14). Context7 oggi risponde "Monthly quota reached": la documentazione l'ho letta sulle pagine ufficiali [verificato: risposta di Context7 del 25/10/2026].
**Etichette:** [verificato: fonte] = letto nella fonte indicata, o in un rapporto del progetto che lo ha verificato. [non verificato] = stima, calcolo, proposta o dato di terzi non confermato. gp = giorni-persona di sviluppo. Prezzi IVA esclusa salvo dove scritto, rilevati il 24 o il 25/10/2026. Cambi: 1 $ = 0,8934 € [verificato: ricerca/14 riga 7]; 1 £ = 1,1872 € [non verificato: cambio di ricerca/28 §2.1].

---

## In breve

**La scelta.** Il motore degli agenti è un servizio in TypeScript sull'Agent SDK di Claude. È la Proposta 1, la più votata: 171,5 punti, contro 170 della Proposta 3 e 137 della Proposta 2. Vince per tre lenti su quattro: visione, CPTO e sicurezza [verificato: 35-giudizio-*.md]. Ci innesto le idee migliori delle altre due. Dalla Proposta 3 prendo la fase zero su Claude Team, che dà valore dalla prima settimana senza server, e la divisione dei lavori in tipi, che riduce le sessioni con strumenti senza declassare nessun agente. Dalla Proposta 2 prendo il modello della bacheca di Hermes, le regole di Pangolin per percorso e per indirizzo e le uscite scritte come tabella.

**Hermes.** Si può evitare, come preferisce Michele. Il motivo non è il costo: la licenza è zero in entrambi i casi e si paga solo l'API [verificato: ricerca/33 §2.6]. Il motivo sono tre fatti di oggi. Il gateway unico di Hermes ha 276 problemi aperti, 9 di sicurezza e 0 risolti su `main` [verificato: api.github.com, issue #143547, aggiornata il 25/10/2026 alle 14:54 UTC]. Hermes passa all'MCP RAG solo un valore fisso o il nome del profilo, quindi i permessi valgono per istanza e non per persona [verificato: docs MCP di Hermes, controllate nei giudizi del 25/10/2026]. La sua bacheca funziona su un solo host [verificato: docs kanban di Hermes, giudizio visione §3.3]. Hermes resta un'uscita prezzata, con un pilota possibile in LAB.

**Cosa cambia rispetto alla Proposta 1**, con le correzioni dei giudici:
- valore dalla settimana 1 con Claude Team, decisione sull'email e mailbox live nelle prime quattro settimane;
- pilota su uno stage nella VLAN LAB con una chiave limitata, senza riordinare il board; il "posto agenti" anticipato resta una richiesta;
- post-call e debrief su stage già nelle settimane 5-8, verifica alla settimana 8 con criteri tecnici e commerciali;
- bacheca, freno ai giri e canale "Agenti" già nel pilota sul server; Telegram, Slack e WhatsApp nella fase 3; nove bot di squadra in Teams; Buzz con criteri per uscire dal LAB;
- ponte verso il Cancello corretto: due difetti del disegno sono verificati oggi sulla documentazione;
- carte legate al testo, secondo fattore con FIDO2 per le azioni più delicate, token della persona verso l'MCP RAG;
- servizi nuovi, patch e manutenzione messi in conto; corrente e VPS corretti.

**Numeri.** Sette fasi in circa 53 settimane. **249 gp di base, circa 332 con la riserva di un terzo**, più circa 29 gp di esercizio e patch dalla fase 2. L'infrastruttura delle fasi F0-F5 del board è lavoro di Michele e non è contata. Oggi si chiedono solo le fasi 0 e 1: 8 settimane, 40,5 gp di base, circa 54 con la riserva. In più rispetto a oggi si spendono circa 135 € al mese finché Azure resta acceso, da circa -15 a +20 € dopo lo spegnimento, circa 46-168 € a regime con Andrea e i canali. Il listino mensile a regime scende da circa 968 € a circa 479-583 €. Chiesto oggi una tantum: circa 3.257-4.354 €, comprese le spese del board che partono subito. Tutte le cifre sono stime [non verificato: calcoli dei §7 e §9].

**Cosa resta da sapere.** Cos'è Sirius, quale piano M365 e Jira ha SerSan, in quante settimane Michele chiude F0-F4, se anticipa il posto agenti, come sono fatti i 192 GB di RAM, quale seconda GPU compra, con cosa sostituisce MinIO (§13).

---

## 1. La scelta e perché

### 1.1 I punteggi dei giudici

| Lente | P1 Agent SDK | P3 Claude Team e MCP | P2 Hermes | Vince |
|---|---|---|---|---|
| Visione (Alberto) | 43 | 41 | 35 | P1 |
| CEO (Alessandro) | 42 | 45 | 34 | P3 |
| CPTO (Michele) | 44 | 42 | 34 | P1 |
| Sicurezza e privacy | 42,5 | 42 | 34 | P1 |
| **Totale** | **171,5** | **170** | **137** | **P1** |

[verificato: 35-giudizio-visione.md, 35-giudizio-ceo.md, 35-giudizio-cpto.md, 35-giudizio-sicurezza.md]

Lo scarto fra P1 e P3 è di un punto e mezzo. La scelta però non è un pareggio: P3 vince solo sul tempo al valore, e quel vantaggio lo prendo tutto con la sua fase zero (§1.5).

### 1.2 Perché il motore sull'Agent SDK

- **È l'unica che tiene intera l'idea.** Tutte le 57 figure sono agenti veri su un solo motore, con una bacheca, una memoria, un Cancello e una sola Porta verso Teams, Telegram, WhatsApp e Slack [verificato: giudizio visione §6].
- **La persona arriva fino alla memoria.** L'Agent SDK passa a ogni server MCP le intestazioni HTTP che decidiamo noi, a ogni `query()` [verificato: code.claude.com/docs/en/agent-sdk/mcp, controllato nei giudizi del 25/10/2026]. Così l'MCP RAG applica i permessi della persona per cui l'agente lavora, come chiede il board con "Permessi per utente" [verificato: board-testo-completo.txt riga 92].
- **Il Cancello si aggancia nel motore.** Un hook `PreToolUse` di callback decide prima di ogni strumento; se non risponde in tempo, lo strumento è bloccato [verificato: code.claude.com/docs/en/agent-sdk/hooks, 25/10/2026]. Le regole deny valgono anche in `bypassPermissions` [verificato: code.claude.com/docs/en/agent-sdk/permissions, 25/10/2026].
- **Segue il messaggio di Michele**: "Se possiamo evitare anche Hermès meglio, usiamo Agent SDK di Claude", senza escludere Hermes a priori [verificato: messaggio di Michele del 25/10/2026].
- **Usa quasi tutto ciò che il board ha già**: n8n, LiteLLM, PostgreSQL 16, Qdrant con l'MCP RAG, BookStack, Infisical, Firecrawl e lo stack OBSRV [verificato: board-vlan.txt].

### 1.3 Perché non la Proposta 3 come base

- **Declassa gli agenti.** Gli agenti con strumenti sono 9-10 su 57; dieci figure diventano skill che una persona apre in Claude Team e 29 diventano flussi fissi [verificato: 34-proposta-3 §5; giudizio visione §3.2]. Per la regola di Alberto è un declassamento.
- **Claude Team non dà squadre.** I compiti programmati appartengono a un solo account, agiscono "as you", non girano più di una volta l'ora e sono in anteprima di ricerca; i Projects non ci sono sul piano Team [verificato: code.claude.com/docs/en/routines e /claude-projects, controllati nei giudizi del 25/10/2026].
- **Più dati in un piano senza registro.** Il piano Team non ha log di audit, conservazione personalizzata né Compliance API [verificato: claude.com/pricing/team, giudizi del 25/10/2026].
- **Più superficie pubblica.** Sei endpoint MCP su internet invece di uno [verificato: 34-proposta-3 §3.2; giudizio sicurezza §4].
- **Cancello e motore nella stessa macchina**, accanto a un motore che legge testo di terzi [verificato: 34-proposta-3 §3.2; giudizio CPTO §4.5].

### 1.4 Perché non la Proposta 2

- Il gateway unico ha 276 problemi aperti: 140 rotti, 108 degradati, 9 di sicurezza, 0 risolti su `main`, 39 in revisione in 14 PR [verificato: api.github.com/repos/NousResearch/hermes-agent/issues/143547, 25/10/2026, 14:54 UTC].
- L'identità verso l'MCP RAG vale per istanza, non per persona [verificato: docs MCP di Hermes]. In `hermes-commerciale` scriverebbero tutti e quattro, quindi il sistema non garantisce che il coaching vada solo a chi ha fatto la call (G4) [verificato: giudizio sicurezza §3.3].
- La bacheca funziona su un solo host: le squadre starebbero in sei istanze, collegate da un MCP da scrivere [verificato: giudizio visione §3.3].
- In Buzz il ponte di Hermes approva da solo ogni permesso [verificato: docs ACP di Hermes, giudizi del 25/10/2026].
- Almeno 45 avvisi di sicurezza nel 2026, nessuno pubblicato dal repository; 44 release dal 12/03 al 23/10/2026 [verificato: ricerca/27 §7.1 e §8].
- Michele preferisce evitarlo [verificato: messaggio del 25/10/2026].

### 1.5 Cosa prendo dalle altre due

| Idea | Da | Dove entra |
|---|---|---|
| Claude Team per tutti dalla settimana 1: progetti per squadra, skill dell'organizzazione, connettori Atlassian e M365 in sola lettura | P3, fase P0 | Fase 0 (§7) |
| Divisione dei lavori in tipi (chiamata a schema senza strumenti, sessione con strumenti, servizio) | P3 §5 | §5.2, registro dei profili |
| Claude Team come "finestra" delle persone; memoria, bacheca e Cancello restano sul server | P3 §1 | §5.6 |
| Tetto iniziale di 6 sessioni e soglia di 5 GB per comprare RAM | P3 §3.3 | §4.2, decisione 11 |
| Corsia di revisione fra agenti, blocco "serve un umano" con sblocco dalla chat, stop dopo 2 fallimenti di fila, rifiuto dei cicli, dispatcher che riprende i compiti fermi | P2, kanban di Hermes | §5.4, fase 2 |
| Regole di Pangolin "Bypass Auth" solo per percorso e filtro sugli IP di Anthropic | P2 §3.4 | §4.4 |
| Limite "dati verdi e gialli finché F3 non è validata" | P2 §8 | §7.1 |
| Uscite scritte con "cosa si perde" e "cosa resta" | P2 §10.2 | §12 |
| Le quattro condizioni per riprendere Hermes come orchestratore | ricerca/27 §11, P2 | §2.4 |

[verificato: le proposte e i giudizi citati; la scelta di cosa prendere è mia]

### 1.6 Le correzioni dei giudici, una per una

| # | Correzione | Chi la chiede | Dove è applicata |
|---|---|---|---|
| 1 | Valore dalla settimana 1 con la fase P0 della P3 (circa 6,5 gp) | visione, CEO, CPTO, sicurezza | fase 0 |
| 2 | Decisione D0 sull'email con il legale, mailbox live e debito di sicurezza di SersanOutreach nelle prime quattro settimane | CEO | fase 0 |
| 3 | Debrief e post-call su stage con chiave diretta e tetto nella Console, nelle prime settimane | CEO (da ricerca/26 §10.3) | fase 1 |
| 4 | Verifica alla settimana 8, con criteri commerciali | CEO | §7.4 |
| 5 | Non riordinare il board: stage in LAB, solo dati verdi e gialli salvati finché F3 non è validata; il posto agenti è una richiesta | CPTO | §7.1, fasi 1-2 |
| 6 | Bacheca, freno e specchio nel canale "Agenti" già nel pilota | visione | fase 2 |
| 7 | Telegram e ponte Slack nella fase della memoria; richiesta a Meta già nel pilota | visione | fase 3 (WhatsApp compreso); richiesta Meta in fase 2 |
| 8 | Nove bot di squadra in Teams come consegna, non come opzione | visione | fase 2 |
| 9 | Buzz con criteri di uscita dal LAB e collegato alla stessa bacheca | visione | fase 4, §5.6 |
| 10 | A6: proposte di skill degli agenti in una cartella, approvate con una PR | visione | fase 4 |
| 11 | Ponte verso il Cancello: hook di callback; niente `dontAsk` insieme a `requiresUserInteraction`; ripresa che ripassa la modalità | sicurezza | §5.1, fase 1 |
| 12 | Carte legate al testo, codice monouso, scadenza; FIDO2 per le classi delicate; telefoni nel perimetro Cyber Essentials | sicurezza | §5.7, fase 2 |
| 13 | Token firmato della persona verso l'MCP RAG, mai scritto dal modello | sicurezza, CEO | §5.5, fase 3 |
| 14 | Dati rossi verso Claude Team decisi prima del pilota, nella DPIA e nel parere | sicurezza, CEO | fase 0 (entro la settimana 3) |
| 15 | MCP RAG pubblico: solo token Entra del tenant SerSan; filtro IP come aggiunta, non come autenticazione; TLS in passthrough sul VPS | sicurezza, CPTO | §4.4 |
| 16 | LiteLLM come bene critico, con l'incidente del 24/03/2026 | sicurezza | §5.7 |
| 17 | Conservazione delle trascrizioni e cancellazione fino ai backup | sicurezza | §5.7, fase 2 |
| 18 | Meno sessioni con strumenti, grazie ai tipi della P3 | sicurezza, CEO | §5.2 |
| 19 | Patch dei servizi aggiunti; Postiz e listmonk mai pubblici; n8n pubblico solo sui webhook firmati | sicurezza | §4.5 |
| 20 | Regole "Sempre" con scadenza e mai per destinatari nuovi | sicurezza | §5.8 |
| 21 | Revisione esterna di Cancello, Porta e ponte prima dei dati dei clienti | sicurezza | decisione 5 |
| 22 | Servizi nuovi e manutenzione messi in conto, con un responsabile delle patch per ognuno | CPTO | §4.5, §7 |
| 23 | RAM decisa sui numeri: lettura nell'iLO, misura con 6 sessioni, acquisto sotto i 5 GB liberi o prima di Vexa | CPTO, visione | §4.2, decisione 11 |
| 24 | Snellire senza perdere isolamento: `mcp-01` in un LXC, meno container di famiglia, Cancello sempre separato | CPTO | §4.1 |
| 25 | Spike delle quattro prove (bot senza Azure, `aadObjectId`, chiamate parallele, `anthropic-beta`) | CPTO | fase 0 |
| 26 | Fatturazione: prima capire Sirius | CPTO | §8, §13 |
| 27 | Numeri allineati: 276 problemi di Hermes; VPS 6,49 €; corrente GPU 2,55-7,66 € e RAM 6,39-10,22 €; gp non confrontabili fra le proposte | tutti | §2, §7.6, §9 |

---

## 2. Hermes contro Agent SDK: il confronto onesto

### 2.1 Fatto per fatto

| Criterio | Hermes self-hosted | Motore sull'Agent SDK | Fonte |
|---|---|---|---|
| Versione di oggi | v0.22.5 del 23/10/2026; v0.23 non ancora uscita | TypeScript 0.3.310 con Claude Code 2.1.310 | [verificato: API GitHub releases e registry.npmjs.org, 25/10/2026] |
| Ritmo dei rilasci | 44 release dal 12/03 al 23/10/2026, 8 a ottobre | 333 versioni TypeScript dal 27/09/2025, otto fra il 18 e il 23/10 | [verificato: ricerca/27 §8; ricerca/26 §1.1] |
| Pronto oggi | canali (Teams, Telegram, WhatsApp e più di 25 altri), profili con nome, bacheca, skill che crescono, cron | ciclo dell'agente, strumenti, hook, permessi, sessioni riprendibili anche da PostgreSQL, sottoagenti, MCP, skill; niente orari, bacheca, profili persistenti, chat di gruppo | [verificato: ricerca/27 §9.2; ricerca/26 §8] |
| Primo bot in Teams | in giorni | Porta da scrivere con Chat SDK e Teams SDK | [non verificato: stima di ricerca/27 §9.5; ricerca/28 §9] |
| Aggancio al Cancello | plugin `pre_tool_call` che blocca e, in timeout, "fails closed", con una finestra di 60 secondi da chiarire | hook `PreToolUse` di callback; in timeout la chiamata è bloccata; `deny` prevale su `defer`, `defer` su `ask` | [verificato: giudizio sicurezza §2; code.claude.com/docs/en/agent-sdk/hooks, 25/10/2026] |
| Identità verso l'MCP RAG | valore fisso o nome del profilo, "resolved once at connect time" | intestazioni per server a ogni `query()`: la persona arriva fino ai permessi | [verificato: docs MCP di Hermes; code.claude.com/docs/en/agent-sdk/mcp] |
| Bacheca | pronta, con dispatcher, revisione e blocco umano, ma su un solo host | da scrivere in PostgreSQL, circa 3 gp, più 1,5 gp per le idee di Hermes | [verificato: docs kanban di Hermes; stima: ricerca/26 §10.2] |
| Isolamento | un solo gateway per tutti i profili dalla v0.22.0; il gateway per profilo è "a temporary shim" | un processo per lavoro, cartella, configurazione e chiave per famiglia | [verificato: ricerca/27 §6.1; ricerca/26 §3.4] |
| Bug e sicurezza | 276 problemi aperti sul gateway, 9 di sicurezza, 0 risolti; almeno 45 avvisi nel 2026 | nessun bug noto di sessioni scambiate; due trappole di configurazione verificate oggi (§5.1) | [verificato: issue #143547; ricerca/27 §7.1; docs SDK] |
| Doppioni nel board | cron, webhook, budget, memoria, chat web, osservabilità, segreti | nessuno: n8n, LiteLLM e la memoria restano gli unici padroni del loro pezzo | [verificato: ricerca/27 §9.3] |
| Cache dei prompt via LiteLLM | parte solo se il nome del modello contiene "claude" (issue #17332) | ID veri dei modelli, inoltro di `anthropic-beta` da provare (PR #36736 di LiteLLM ancora aperta) | [verificato: ricerca/27 §3; api.github.com/repos/BerriAI/litellm/pulls/36736, 25/10/2026] |
| Giorni per il motore | 22,5 gp di base (20-25), 26-33 con la riserva | 21 gp di base, circa 27 con la riserva | [non verificato: stime di ricerca/27 §10 e ricerca/26 §10.2] |
| Manutenzione | 1,5-2,5 gp al mese, di più con più istanze | aggiornamento ogni due settimane dopo 10 scenari | [non verificato: stime degli stessi rapporti] |
| Licenza e canone | MIT, 0 € | Commercial Terms di Anthropic, 0 €; si paga l'API | [verificato: ricerca/33 §2.6] |
| Chiavi e termini | Claude via LiteLLM con la chiave API | solo chiave API; i posti Claude Team servono alle persone | [verificato: ricerca/26 §5] |
| Chi lo conosce | nessuno di noi a fondo | codice nostro, conosciuto da poche persone | [verificato: ricerca/26 §9] |

### 2.2 Dove Hermes è meglio, detto chiaramente

- È pronto: canali, profili, bacheca e skill che si migliorano funzionano senza scrivere codice [verificato: ricerca/27 §9.5].
- Ha una comunità enorme e un catalogo di plugin che cresce ogni settimana [verificato: ricerca/27 §9.5].
- Con il motore sull'SDK i bug di canali, bacheca e profili sono nostri. La Porta da sola vale circa 14,75 gp con Telegram, WhatsApp e Slack [non verificato: stima di 34-proposta-1 §4.3].
- Le sue idee migliori le prendo come modello per la bacheca (§5.4).

### 2.3 Dove l'Agent SDK è meglio

- La persona arriva fino ai permessi della memoria: è ciò che chiede il board e ciò che serve a G4, C6, K4 ed E3.
- Il Cancello si aggancia in modo nativo e blocca anche quando il nostro codice non risponde.
- Un pacchetto npm più il nostro codice da tenere nei 14 giorni di Cyber Essentials, invece di un gateway Python con release poco documentate [verificato: ricerca/26 §9; ricerca/25 N14].
- Nessun doppione con lo stack di Michele.

### 2.4 Il verdetto e come resta aperta la porta

**Verdetto:** motore sull'Agent SDK; Hermes non entra oggi nel percorso dei clienti [non verificato: giudizio, su fatti verificati sopra].

**La porta resta aperta in tre modi:**
1. **Pilota confinato** sullo stesso stage in LAB, o in Experimental-2 quando arriva con la fase F5 del board: due o tre profili, Telegram in polling, MCP in sola lettura, dati verdi; circa 6-8 gp [non verificato: stima di ricerca/27 §10].
2. **Hermes come orchestratore** solo se valgono insieme quattro condizioni: v0.23 uscita con note complete; righe di sicurezza MSG-43, GW-41, KB-10 e HR-6 chiuse su `main`; bug dei documenti su Teams (#113578) chiuso; un aggiornamento che passa i 10 scenari senza interventi a mano [verificato: ricerca/27 §11].
3. **Uscita prezzata:** se il motore non regge, Hermes prende il posto del runner. Restano Cancello, LiteLLM, server MCP, Porta, memoria e skill, che hanno lo stesso formato `SKILL.md`. Costo: 26-33 gp con la riserva [verificato: ricerca/27 §10; ricerca/22 §8 per il formato delle skill].

**I giorni non si confrontano a occhio.** La P1 stimava 67 gp per il contenuto dei 57 agenti (0,5-2 gp l'uno), la P2 circa 0,6 gp a profilo, la P3 circa 0,9. Con la stessa stima per agente la P2 arriverebbe a circa 200-210 gp, vicina alla P1. Il motore in sé costa quasi uguale: 22,5 gp Hermes, 21 gp SDK [verificato: giudizio visione §5 punto 2; giudizio CEO §3; ricerca/26 §10.2; ricerca/27 §10].

---

## 3. Lo schema

```
PERSONE (4): Teams e Outlook (M365, Entra con MFA e chiave FIDO2), dal PC e dal telefono
             Claude Team: chat, skill, progetti per squadra, connettore verso l'MCP RAG
             Telegram (avvisi) | WhatsApp (clienti) | Slack (se ammesso) | Buzz (pilota in LAB)
                |  HTTPS firmato (bot Teams, webhook)        ^  long polling (Telegram)
=========== OPNsense, VLAN default-deny ==================================================
20 EDGE   Traefik + Pangolin: /api/messages dei bot, webhook WhatsApp e n8n firmati,
          MCP RAG (OAuth Entra, filtro IP di Anthropic), pagine di firma DocuSeal
30 APPS   cancello-01 (VM): CANCELLO + PORTA CHAT (Chat SDK + Teams SDK)
          mcp-01 (LXC): MCP memoria, bacheca, BookStack, Jira, posta in lettura,
                        Firecrawl, SersanOutreach
          n8n | LiteLLM | MCP RAG | BookStack | Open WebUI | SersanOutreach
          Postiz e listmonk (mai pubblici) | DocuSeal | fatturazione | andrea-01 (Pipecat)
32 AGENTI agenti-01 (VM): MOTORE (runner, registro dei profili, container di famiglia)
          esce solo verso LiteLLM, mcp-01, MCP RAG e API del Cancello
40 DATA   PostgreSQL 16 | Qdrant | MariaDB (nuovo) | Infisical | Vaultwarden | S3 (al posto di MinIO)
25 VOCE   voce-01 (LXC): Asterisk 22 LTS <-> trunk SIP dell'operatore italiano
35 MEET   meet-01 (VM): Vexa, bot nelle call dei clienti
80 AI     ai-gpu-01 (LXC): Qwen3-4B, embedding e reranker, Docling, trascrizione
          RTX 4000 + seconda GPU da 16 GB (dalla fase 5)
70 OBSRV  Prometheus | Grafana | Loki | Uptime Kuma | Wazuh | NetBox
90 LAB    stage-agenti (VM): pilota delle fasi 1-2 | Experimental-2: Buzz, Paperclip, prova Hermes
==========================================================================================
CLOUD DEL BOARD   M365/Entra | Claude Team | API Anthropic via LiteLLM | Cloudflare DNS
                  GitHub | Supabase | Vercel | Jira | Instantly | S3 facoltativo
ESTERNI DA AMMETTERE  operatore telefonico | Meta (WhatsApp) | Telegram | Slack | relay SMTP
                  VPS per Pangolin (se scelto) | strumenti commerciali che restano
```

Le VLAN 20, 30, 40, 70, 80 e 90 e i loro servizi sono quelli del board [verificato: board-vlan.txt]. Le VLAN 25, 32 e 35, le macchine `agenti-01`, `cancello-01`, `mcp-01`, `stage-agenti`, `andrea-01`, `voce-01`, `meet-01` e i servizi MariaDB, Vexa, trascrizione, Asterisk, Pipecat, Postiz, listmonk, DocuSeal e fatturazione sono proposte da far approvare a Michele [non verificato: proposta]. La VLAN 32 può diventare la 30 con il firewall di Proxmox per VM, se Michele preferisce [non verificato: alternativa da decidere con lui].

---

## 4. Componenti e dove girano

### 4.1 Tabella dei componenti

"Stato": **board** = già previsto da Michele; **config** = nel board, da configurare per gli agenti; **nostro** = codice da scrivere; **nuovo** = servizio self-hosted da aggiungere al board; **esterno** = fuori dal board, da ammettere come eccezione.

| Componente | Cosa fa | Stato | VLAN e macchina | RAM | GPU | Fonte |
|---|---|---|---|---|---|---|
| **Motore agenti** | coda dei lavori, un processo SDK per lavoro, profili, tetti, ripresa, `/stop` | nostro | 32 AGENTI, VM `agenti-01` con Docker; container di famiglia, uniti dove permessi e segreti coincidono | 12 GB con 6 sessioni, 16 con 8-10, 20 con 12-16 | no | 1 GiB, 1 CPU e 5 GiB di disco per sessione come partenza [verificato: ricerca/26 §3.3]; il resto [non verificato: stima] |
| **Cancello** | classi d'azione, carte legate al testo, approvatori, esecutori, outbox, registro a catena, ESTOP, pagina con FIDO2 | nostro | 30 APPS, VM `cancello-01`, sempre separata dal motore | 3-4 GB | no | [non verificato: stima; separazione chiesta dal giudizio CPTO §7.7] |
| **Porta chat** | bot Teams e bot di squadra; poi Telegram, Slack e WhatsApp con lo stesso codice | nostro | 30 APPS, in `cancello-01` | 0,5-1 GB | no | [verificato: ricerca/28 §9 per la RAM stimata] |
| **Server MCP** | memoria su PostgreSQL, bacheca, BookStack in lettura, Jira, posta e calendario in lettura, Firecrawl, SersanOutreach | nostro e adottati | 30 APPS, LXC `mcp-01` | 3-4 GB | no | [non verificato: stima] |
| **Stage degli agenti** | pilota delle fasi 1-2, poi prove degli aggiornamenti dell'SDK | nuovo | 90 LAB, VM `stage-agenti`, con un suo PostgreSQL | 8 GB nel pilota, poi 4 | no | [non verificato: proposta; LAB "internet sì, nessun accesso a DATA", verificato: board-vlan.txt] |
| n8n | orari, webhook firmati, ingressi, avvisi | board, config | 30 APPS | nel board | no | [verificato: board-vlan.txt] |
| LiteLLM | porta dei modelli, chiavi virtuali, budget per agente, squadra e persona | board (fase F4), config | 30 APPS | nel board | no | [verificato: board, roadmap F4] |
| PostgreSQL 16 | coda, bacheca, sessioni, Cancello, memoria strutturata, LiteLLM, n8n | board, config | 40 DATA | +1-5 GB di crescita | no | [verificato: board-vlan.txt] |
| Qdrant con BM25 e MCP RAG | memoria vettoriale con permessi per persona e registro delle query | board (F4), estensioni nostre | 40 DATA e 30 APPS | nel board | no | [verificato: board righe 79-92] |
| Ollama Qwen3-4B, Infinity (embedding e reranker 0.6B), Docling | metadati, ricerca, documenti | board | 80 AI, LXC `ai-gpu-01` | nel board | RTX 4000 | [verificato: board-vlan.txt] |
| Trascrizione (faster-whisper turbo, Parakeet v3, pyannote) | audio di call e riunioni dal vivo | nuovo | 80 AI, LXC `ai-gpu-01` | +6-8 GB | 2-4,5 GB di giorno; CPU quando la GPU è altrove | [verificato: ricerca/30 §6 e §11.2] |
| Vexa 0.12.x | bot nelle call dei clienti (Teams di altri, Meet, Zoom web) | nuovo | 35 MEET, VM `meet-01` | 12 GB per 3 bot; circa 4 con Vexa Lite | usa la trascrizione in VLAN 80 | [verificato: ricerca/30 §4 e §11.2] |
| Asterisk 22 LTS | centralino di Andrea | nuovo | 25 VOCE, LXC `voce-01` | 1 GB | no | [verificato: ricerca/31 §1.1] |
| Pipecat con ascolto e voce (Parakeet int8, Pocket TTS) | conversazione di Andrea | nuovo | 30 APPS, LXC `andrea-01` | 6-8 GB su CPU; 4 GB con la seconda GPU | seconda GPU | [verificato: ricerca/31 §8.2] |
| BookStack | regole "Come lavoro", processi, catalogo, manuale degli agenti | board, config | 30 APPS | nel board | no | [verificato: board-vlan.txt] |
| MariaDB | database richiesto da BookStack | nuovo | 40 DATA, container | 1 GB | no | BookStack chiede MySQL 8 o MariaDB 10.6 [verificato: ricerca/29 §3.1] |
| Archivio S3 al posto di MinIO | audio, file degli agenti | board, da sostituire | 40 DATA | nel board | no | MinIO risulta `archived: true` [verificato: api.github.com/repos/minio/minio, giudizio CPTO]; date [non verificato: fonti terze] |
| Infisical, Vaultwarden | segreti delle app e delle persone | board | 40 DATA | nel board | no | [verificato: board-vlan.txt] |
| Firecrawl | pagine web in markdown per gli agenti | board | 30 APPS | nel board | no | [verificato: board] |
| Open WebUI | chat sui modelli per tutti, con il budget di LiteLLM | board | 30 APPS | nel board | no | [verificato: board-vlan.txt] |
| Postiz | programmazione dei post e metriche | nuovo, mai pubblico | 30 APPS, container | 2 GB | no | AGPL-3.0 [verificato: github.com/gitroomhq/postiz-app, in 34-proposta-1]; RAM [non verificato] |
| listmonk | newsletter | nuovo, mai pubblico | 30 APPS, container su PostgreSQL | 0,5 GB | no | AGPL-3.0, API REST [verificato: github.com/knadh/listmonk, in 34-proposta-1] |
| DocuSeal | firma elettronica | nuovo | 30 APPS; pagine di firma via Pangolin | 1 GB | no | AGPLv3, versione 3.3.3 del 19/10/2026 [verificato: 34-proposta-1 §3.1] |
| Fatturazione | fatture, incassi, solleciti | nuovo, se Sirius non lo fa già | 30 APPS, container | 1-2 GB | no | Invoice Ninja self-hosted sotto Elastic License 2.0 [non verificato: fonte terza] |
| Buzz | stanza degli agenti alla Buzz, via `claude-agent-acp` | nuovo, solo in LAB | 90 LAB, Experimental-2 | 4-8 GB nei 24 GB di Experimental | no | [verificato: ricerca/26 §7; ricerca/28 §9] |
| Paperclip | piano di controllo per "aziende di agenti", in prova | nuovo, solo in LAB | 90 LAB, Experimental-2 | dentro Experimental | no | [verificato: PRESENTAZIONE-CEO §4.12; 34-proposta-3 §9] |
| Teams, Outlook, SharePoint, OneDrive | chat, posta, calendario, documenti | cloud del board | M365 | | | [verificato: board] |
| Claude Team | finestra di lavoro delle persone | cloud del board | Anthropic | | | [verificato: board] |
| Jira | to-do e progetti | cloud del board | Atlassian | | | [verificato: board] |
| Operatore telefonico italiano (Messagenet) | numero e trunk SIP di Andrea | esterno | | | | [verificato: ricerca/31 §4] |
| Relay SMTP (per esempio Amazon SES) | invio della newsletter | esterno | | | | Exchange Online non è fatto per l'invio in massa [verificato: 34-proposta-1 §3.1, avviso MC787382] |
| Telegram, WhatsApp Cloud API, Slack | canali in più verso gli stessi agenti | esterni | | | | [verificato: ricerca/28 §6] |
| VPS per Pangolin e NetBird | endpoint pubblici senza porte aperte in casa | esterno, se scelto | | | | [verificato: ricerca/25 N10] |

### 4.2 La RAM, fase per fase

Il board lascia circa 53 GB liberi su 192 [verificato: board, tabella "Capacità"]. Proxmox limita la cache ZFS al 10 % della RAM con un tetto di 16 GiB: va fissato `zfs_arc_max` a 12 GiB per restare nei 16 GB che il board dà a host e cache [verificato: ricerca/32 §3.2].

| GB nuovi | Fase 1 (stage) | Fase 2 | Fasi 3-4 | Fasi 5-6 |
|---|---|---|---|---|
| `stage-agenti` | 8 | 4 | 4 | 4 |
| Motore `agenti-01` | 0 | 12 (6 sessioni) | 16 | 20 |
| Cancello e Porta `cancello-01` | 0 | 4 | 4 | 5 |
| Server MCP `mcp-01` | 0 | 3 | 4 | 4 |
| MariaDB | 0 | 1 | 1 | 1 |
| Crescita di PostgreSQL, Qdrant, Loki | 0 | 1 | 3 | 5 |
| Trascrizione e lotti | 0 | 0 | 6 | 8 |
| Vexa `meet-01` | 0 | 0 | 12 | 12 |
| Postiz e listmonk | 0 | 0 | 2,5 | 2,5 |
| Andrea | 0 | 0 | 0 | 8 su CPU, 4 con la seconda GPU |
| DocuSeal e fatturazione | 0 | 0 | 0 | 2,5 |
| SersanOutreach, worker in più | 0 | 0 | 1 | 2 |
| **Totale nuovo** | **8** | **25** | **53,5** | **70-74** |
| **Libera dopo, con 192 GB** | **circa 45** | **circa 28** | **circa -0,5** | **da -17 a -21** |
| **Libera dopo, con 384 GB** | | | **circa 191** | **circa 171-175** |

[non verificato: stime, costruite su 34-proposta-1 §3.2 e ricerca/32 §3.3, più lo stage]

**Lettura.** Il pilota sta largo. Memoria e call arrivano al limite. Lo scenario completo non entra. **Regola d'acquisto:** prima si legge nell'iLO come sono fatti i 192 GB; poi si misura con un tetto di 6 sessioni; si comprano altri 192 GB uguali a quelli montati quando il margine misurato scende sotto i 5 GB, e comunque prima di accendere Vexa all'inizio della fase 3 [verificato: regola del giudizio CPTO §7.6]. È l'unico passo bilanciato a banda piena: 816 € IVA esclusa con moduli da 2133, o £1.020 IVA esclusa (circa 1.218 €) con moduli da 2666 [verificato: ricerca/32 §2.4, configuratori del 25/10/2026]. Il ripiego da +64 GB costa 272-512 € ma porta la banda al 69 % [verificato: ricerca/32 §2.4].

**Leve per rimandare** [non verificato: proposte di ricerca/32 §3.4 e 34-proposta-1]: Experimental 1 e 2 accese solo quando servono (24 GB); tetto di 12 sessioni; Andrea sulla seconda GPU (-4 GB); Vexa Lite con una call alla volta (circa 4 GB invece di 12).

**Cento agenti (G9).** La RAM cresce con le sessioni attive insieme, non con i profili. Cento profili con un tetto di 16 sessioni stanno nei 20 GB del motore [verificato: ricerca/32 §3.3, deduzione di quel rapporto].

### 4.3 GPU e fasce orarie

- **Il motore non usa la GPU.** Gli agenti ragionano con Claude via API. La GPU serve alla pipeline del board, alla trascrizione e alla voce di Andrea [verificato: board; ricerca/26 §4.5].
- **RTX 4000 di giorno.** Con Qwen3-4B, embedding, reranker e Docling resta meno di 1 GB libero; la trascrizione dal vivo (circa 2,1 GB) entra solo se il reranker passa sulla CPU [verificato: ricerca/30 §6.1, stima di quel rapporto].
- **La sera** la scheda va a Experimental-1 [verificato: SerSan Infra Board.html riga 309, citata in ricerca/25]. Experimental 1 e 2 arrivano con la fase F5 del board [verificato: board, roadmap F5]: fino ad allora la RTX 4000 può restare all'AI anche la sera [non verificato: deduzione dalla roadmap].
- **Quando la GPU è altrove:** embedding e reranker su CPU, perché Qwen3-Embedding 0.6B gira su CPU [verificato: ricerca/25 N06]; trascrizione a lotti su CPU con Parakeet in ONNX, circa 36 volte il tempo reale [verificato: ricerca/30 §5.1]; bandi e prima indicizzazione nella fascia AI concordata con Michele [non verificato: fasce da decidere].
- **Seconda GPU.** La "RTX A2000 con chip Ada da 6 GB GDDR7" non esiste [verificato: ricerca/32 §4.1; ricerca/25 H07]. Consiglio la **RTX 2000 Ada da 16 GB**, 70 W, 837-946 € IVA inclusa (686-775 € IVA esclusa) al 24-25/10/2026, nel riser secondario con una staffa ad altezza piena [verificato: ricerca/32 §4.3 e §4.7]. Ci stanno insieme Andrea, la trascrizione dal vivo e la pipeline RAG, 24 ore su 24 [non verificato: stima di ricerca/32 §4.6]. Il board la mette nella fase F5, che coincide con la nostra fase 5: va montata prima di Andrea sulla GPU [non verificato: allineamento mio].
- **Attenzione:** HPE scrive "Mixing of GPUs is not supported"; due modelli diversi escono dalla configurazione supportata, ma la garanzia è di Bargain [verificato: ricerca/32 §4.4].

### 4.4 Rete ed esposizione pubblica

| Da | A | Cosa passa | Perché |
|---|---|---|---|
| `agenti-01` (32) | LiteLLM (30) | `/v1/messages` | modelli; nessun'altra uscita verso internet |
| `agenti-01` | `mcp-01`, MCP RAG, API del Cancello (30) | HTTP interno con token per famiglia | strumenti e `propose_action` |
| `agenti-01` | internet | niente | `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` e nessun WebFetch diretto; il web passa da Firecrawl [verificato: ricerca/26 §3.7] |
| LiteLLM | `api.anthropic.com` | 443 | unica uscita dei modelli [verificato: board, "API Anthropic dietro LiteLLM"] |
| `cancello-01` | Graph, login Microsoft, Bot Framework, Jira, SersanOutreach, Instantly, Telegram, Meta, Slack (se ammesso) | 443 | esecutori e Porta [verificato: ricerca/28 §2.2] |
| EDGE (20) | `cancello-01` | `/api/messages`, `/webhooks/whatsapp`, webhook Slack | messaggi dei canali, firmati dal mittente [verificato: ricerca/28 §2.2 e §6.2] |
| EDGE | MCP RAG | endpoint MCP con OAuth verso Entra | connettore di Claude Team, che parte dai server di Anthropic [verificato: support.claude.com 11175166, in ricerca/29 §7.3] |
| MCP RAG (30) | Qdrant (40) | API di Qdrant | regola da scrivere: oggi il board ha "AI → DATA solo Qdrant", non APPS → DATA [verificato: ricerca/29 §6.3] |
| `meet-01` (35) | internet | 443 e media UDP | i bot entrano nelle call; nessuna rotta verso DATA [verificato: ricerca/30 §4.5] |
| `voce-01` (25) | IP dell'operatore | SIP, meglio TLS 5061, e RTP | trunk di Andrea [verificato: ricerca/31 §1.2] |
| `stage-agenti` (90) | internet | 443 | API Anthropic con chiave limitata, Graph, bot; nessun accesso a DATA [verificato: board-vlan.txt per la regola LAB] |
| OBSRV (70) | tutte | lettura | come nel board [verificato: board-vlan.txt] |

[non verificato: regole proposte, da scrivere con Michele su OPNsense e nel firewall di Proxmox]

**Esposizione pubblica.**
- Pangolin in modalità tunnel di solito vive su un VPS con 80 e 443 TCP e 51820 UDP raggiungibili; NetBird self-hosted chiede 80, 443 TCP e 3478 UDP [verificato: ricerca/25 N10]. Le strade sono due: un VPS piccolo oppure l'IP fisso con porte aperte solo verso la VLAN EDGE. Decide Michele.
- **Prezzo del VPS:** la linea Hetzner Cost-Optimized parte da 5,99 € al mese ma oggi è segnata "Currently not available"; la Regular Performance parte da 6,49 € al mese IVA esclusa. Uso 6,49 € [verificato: hetzner.com/cloud, 25/10/2026].
- **Con il VPS**, il TLS passa senza essere aperto (passthrough verso Traefik in casa), così il VPS non vede in chiaro bot, webhook e MCP [non verificato: proposta del giudizio sicurezza §8].
- **Un solo endpoint MCP pubblico**, l'MCP RAG, come prevede il board [verificato: board, "endpoint MCP per Claude Team"]. Accetta solo token Entra del tenant SerSan con il giusto destinatario. La regola CIDR sugli IP di Anthropic `160.79.104.0/21` in Pangolin è un filtro in più, non un'autenticazione, perché quegli IP sono di tutto il servizio Anthropic [verificato: platform.claude.com/docs/en/api/ip-addresses; docs.pangolin.net/manage/access-control/rules, controllati nei giudizi del 25/10/2026].
- **Bot Teams:** un solo servizio Porta dietro una risorsa Pangolin con "Bypass Auth" solo sul percorso `/api/messages`; la verifica la fa il JWT del Bot Framework [verificato: docs Pangolin per le regole per percorso; ricerca/28 §2.2]. Le registrazioni sono dieci (Cancello più nove squadre); che tutte puntino allo stesso servizio va provato [non verificato].
- **Senza esporre nulla:** gli amministratori usano gli MCP da Claude Desktop attraverso la mesh di NetBird, come prevede il board [verificato: board, "In alternativa Claude Desktop via mesh"].

### 4.5 Il perimetro dei servizi nuovi e le patch

Il giudice CPTO ha ragione su un punto che pesa più della scelta del motore: ogni servizio nuovo entra nel perimetro Cyber Essentials, con patch critiche entro 14 giorni, account non amministratori e software supportato [verificato: board, nota su Experimental; ricerca/25 N14]. Per questo ogni servizio ha una fase d'ingresso, una regola di esposizione e un responsabile delle patch, e prima della fase F4 del board entrano solo i servizi del pilota.

| Servizio | Entra | Esposto su internet | Responsabile proposto delle patch | Nota |
|---|---|---|---|---|
| `stage-agenti` | fase 1 | no (solo uscita) | chi sviluppa il motore | chiave API diretta solo qui, con tetto nella Console |
| `agenti-01`, `cancello-01`, `mcp-01`, MariaDB | fase 2 (posto agenti o dopo F3) | solo la Porta, via Pangolin | motore e Cancello: chi sviluppa; sistema e MariaDB: amministratore del server | inventario in NetBox |
| Trascrizione, VLAN 35 e `meet-01` (Vexa) | fase 3 | no (Vexa esce, non riceve) | amministratore del server | Vexa è 0.12: versione fissata, prova a ogni salto |
| Postiz, listmonk | fase 4 | **mai**: solo via NetBird | amministratore del server | entrambi hanno avuto CVE nel 2026 [non verificato: NVD, OSV, GitLab letti tramite ricerca nel giudizio sicurezza §6] |
| Buzz, Paperclip | fase 4 e 6, solo in LAB | no | chi sviluppa | nessun dato dei clienti |
| VLAN 25, `voce-01`, `andrea-01` | fase 5 | solo il trunk SIP verso gli IP dell'operatore | amministratore del server | |
| DocuSeal, fatturazione | fase 6 | solo le pagine di firma | amministratore del server | |
| n8n (board) | già nel board | solo i webhook firmati, nessun Form pubblico | amministratore del server | CVE-2026-21858 con CVSS 10 nel 2026 [non verificato: fonti di terzi lette nel giudizio sicurezza §6] |

[non verificato: proposta; i nomi dei responsabili li fissa Michele]

Il lavoro per installare e collegare questi servizi è contato nelle fasi (circa 7,5 gp in tutto), e da fase 2 è contato anche l'esercizio: aggiornamenti, patch, scansioni con Wazuh (§7.2) [non verificato: stima].

---

## 5. Come lavora il sistema

### 5.1 Un lavoro dall'inizio alla fine, con il ponte corretto

1. **Ingresso.** Un lavoro nasce in tre modi: n8n a orario o su webhook firmato; una persona che scrive a un agente in Teams; un agente che passa un compito a un altro nella bacheca [non verificato: proposta su ricerca/26 §8].
2. **Coda.** Il lavoro entra nella tabella dei lavori in PostgreSQL con profilo, persona per cui si lavora, tetto in dollari e scadenza [non verificato: proposta].
3. **Sessione.** Il runner avvia un processo dell'SDK con il profilo: `CLAUDE.md` della squadra, skill ammesse, elenco chiuso di strumenti MCP in `allowedTools`, chiave LiteLLM, `maxTurns` e `maxBudgetUsd`. Con `settingSources: []`, `CLAUDE_CONFIG_DIR` e `cwd` per famiglia un agente non legge le impostazioni di un altro; in TypeScript l'opzione `env` sostituisce l'ambiente, quindi il processo non vede le chiavi del motore [verificato: ricerca/26 §3.4; giudizio sicurezza §3.1]. Modalità `dontAsk`: ciò che non è in elenco è negato [verificato: code.claude.com/docs/en/agent-sdk/permissions, 25/10/2026].
4. **Contesto.** L'agente legge la pagina "Come lavoro" della persona in BookStack, i dati fissi dal MCP memoria e i passaggi utili dall'MCP RAG, con il token della persona (§5.5) [verificato: ricerca/29 §2 e §7, proposta di quel rapporto].
5. **Testo di terzi.** Mail, trascrizioni, pagine web, commenti e messaggi dei clienti li legge una sessione senza strumenti d'azione, che restituisce solo campi a schema. Chi legge testo di terzi non ha `propose_action` nella stessa sessione [verificato: ricerca/22 §2; giudizio sicurezza §8 punto 8].
6. **Effetto (il ponte corretto).** Se serve far uscire qualcosa, l'agente chiama `propose_action(classe, destinazione, testo, motivo)`. Il controllo lo fa un **hook `PreToolUse` di callback nel runner**, non un hook a comando in un plugin:
   - se l'hook non risponde in tempo, la chiamata è bloccata [verificato: code.claude.com/docs/en/agent-sdk/hooks, 25/10/2026]; un hook a comando in timeout invece non blocca, salvo `onFailure: "block"` [verificato: giudizio sicurezza §2, da code.claude.com/docs/en/hooks];
   - `propose_action` **non** è marcato `requiresUserInteraction`: in `dontAsk` gli strumenti che chiedono interazione "are denied instead", anche se una regola li consente, e il flusso delle carte si romperebbe [verificato: code.claude.com/docs/en/agent-sdk/permissions, 25/10/2026];
   - l'hook nega le classi vietate, consente le scritture interne con regola e, per il resto, lascia passare `propose_action`, che crea solo la carta e risponde "in attesa, carta N"; l'agente chiude il turno e il runner segna il lavoro "in attesa" [non verificato: disegno proposto dal giudizio sicurezza §8 punto 1];
   - un effetto per turno: l'hook nega le altre chiamate di strumento nello stesso turno di `propose_action` [non verificato: regola da provare nello spike];
   - il `defer` nativo (il turno finisce con `stop_reason` "tool_deferred") resta l'alternativa, se lo spike lo dimostra più semplice [verificato: code.claude.com/docs/en/agent-sdk/hooks].
7. **Approvazione.** La carta arriva in Teams con il testo esatto, un'impronta del testo, un codice monouso e una scadenza. La persona preme "Approva" sul telefono; la Porta riceve l'azione con l'identità Entra (`aadObjectId`) e il Cancello controlla che sia fra gli approvatori della classe. Per offerte, contratti, fatture e solleciti, primi contatti, codice e infrastruttura serve un secondo passo con la chiave FIDO2 sulla pagina del Cancello [verificato in parte: ricerca/28 §2.3; `aadObjectId` da confermare nello spike; secondo fattore: proposta del giudizio sicurezza §8 punto 2].
8. **Esecuzione.** L'esecutore ricalcola l'impronta, agisce una volta sola (outbox) e aggiorna la carta con nome e ora [non verificato: proposta].
9. **Ripresa.** Il Cancello mette in coda la ripresa; il runner riprende la sessione dal `SessionStore` con l'esito come nuovo messaggio, ripassando modalità e opzioni, perché la ripresa non ripristina la modalità salvata [verificato: ricerca/26 §2 per il `SessionStore`; giudizio sicurezza §2 per la modalità].
10. **Conto.** LiteLLM conta e blocca oltre il budget; la stima dell'SDK va nel cruscotto e ogni mese si confronta con la Console [verificato: ricerca/26 §4.3; i costi dell'SDK sono stime del client, ricerca/26 "Fatti"].

### 5.2 Tre tipi di lavoro, nessun agente declassato

Ogni figura è un profilo del registro, con nome, squadra, responsabile, modello, tetto e costo del mese. Il **tipo** dice come lavora in quel momento, non quanto vale:
- **N, chiamata a schema:** riassumere, classificare, estrarre. Una chiamata via LiteLLM, senza strumenti, da n8n o dal runner. Contro le iniezioni è il disegno più robusto [verificato: giudizio sicurezza §3.2].
- **S, sessione con strumenti:** lavori a più passi (brief, offerte, deck, agenda, operatore). Una sessione SDK con il ponte verso il Cancello.
- **V, servizio:** un componente che fa il lavoro da sé (pipeline, Vexa, centralino, Cancello).

Le figure che la P3 metteva "in mano a una persona" (Copywriter, Agente video, Agente grafiche, Pubblicatore, Sviluppatori, Intervistatore, Assistente personale) restano **agenti del registro che ricevono lavoro dalla bacheca** con una sessione SDK. In più le loro skill sono anche in Claude Team, così una persona le può usare a mano [verificato: richiesta del giudizio CEO §9 punto 2; P3 §5 per l'elenco]. Per ogni profilo il registro scrive il tipo, se legge testo di terzi e quali strumenti ha [non verificato: proposta del giudizio sicurezza §8 punto 8].

### 5.3 Squadre, registro, organigramma e agenti con nome in Teams

| Squadra (agenti) | Responsabile | Modello prevalente | Strumenti principali | Chi approva le carte |
|---|---|---|---|---|
| Outbound (5) | Alessandro | Sonnet; Haiku per smistare | MCP SersanOutreach, mcp-enrich, Firecrawl, MCP RAG | Alessandro |
| Chiamate (5) | Alessandro | Sonnet | trascrizioni, calendario in lettura, MCP memoria | Alessandro |
| Vendite (8) | Alessandro | Sonnet; Opus per le offerte | MCP RAG, catalogo, SersanOutreach, SharePoint in lettura | Alessandro; Michele per offerte e affermazioni tecniche |
| Marketing (8) | Alberto | Sonnet; Haiku per le metriche | Firecrawl, Postiz, listmonk, BookStack | Alberto; il founder per i suoi post |
| Studio contenuti (4) | Alberto | Sonnet | template SerSan, skill per slide e documenti | Alberto |
| Progetti (8) | Michele, con Mattia | Sonnet | Jira, SharePoint, MCP RAG | Michele |
| Memoria (5) | Michele | Haiku e lavori deterministici | pipeline, OBSRV in lettura, NetBox | Michele |
| Direzione (10) | Alessandro e Michele | Sonnet; Opus per la mappa dei processi | MCP memoria, Grafana, LiteLLM in lettura, posta in lettura | i CEO |
| Amministrazione (4) | Alessandro e Michele | Sonnet | PostgreSQL finanza, MCP RAG `finanza`, fatturazione, DocuSeal | Alessandro o Michele |

[verificato: PRESENTAZIONE-CEO §4.12 e ricerca/22 §3 per responsabili e approvatori; il resto non verificato: proposta di 34-proposta-1 §5.2]. Prezzi dei modelli al 25/10/2026 per milione di token: Opus 5.5 4 $ e 20 $, Sonnet 5.5 2 $ e 10 $, Haiku 5.5 da 0,10 $ e 0,50 $ [verificato: ricerca/26 "Fatti"].

- **Registro dei profili** in git, con pagina BookStack e vista Grafana generate ogni notte. È l'organigramma (G9) [verificato: ricerca/26 §10.2 pezzo 2].
- **Agenti con nome in Teams:** nove bot, uno per squadra, firmano ogni messaggio con il nome dell'agente; il Capo di gabinetto risponde in chat 1:1. È una consegna della fase 2, circa 2 gp [verificato: ricerca/28 §2.6, "un bot per squadra"; gp non verificati].
- **Un agente nuovo** nasce solo con un'approvazione, che porta con sé la sua riga nel registro dei trattamenti [verificato: PRESENTAZIONE-CEO §4.12].

### 5.4 La bacheca e il freno ai giri

- **Bacheca.** Tabelle `compiti` e `passaggi` in PostgreSQL, con un server MCP: crea, prendi, aggiorna, passa, chiudi, stato [verificato: ricerca/26 §8].
- **Dal modello di Hermes:** corsia di revisione fra agenti prima della carta; blocco "serve un umano" con sblocco dalla chat; blocco automatico dopo 2 fallimenti di fila; rifiuto dei cicli di dipendenze; un dispatcher che riprende i compiti fermi [verificato: docs kanban di Hermes, giudizio visione §9].
- **Freno.** Al massimo 3 passaggi per catena, 8 messaggi per thread, un tetto in dollari per catena; oltre, la catena si ferma e arriva una carta a una persona [verificato: ricerca/22 §3 per i numeri].
- **Visibile a tutti (A7).** Ogni passaggio è rispecchiato nel canale Teams "Agenti" con il nome dell'agente in testa. Le persone intervengono con una @menzione [verificato: ricerca/28 §8.2, proposta di quel rapporto].
- **To-do delle persone** in Jira. Un agente chiude da solo solo i compiti fra agenti; per quelli delle persone chiede il sì [verificato: ricerca/29 §4.2].

### 5.5 La memoria e l'identità della persona

| Casa | Cosa contiene | Come la legge l'agente | Fonte |
|---|---|---|---|
| BookStack | regole "Come lavoro", processi, catalogo, manuale, cartella "proposte" di skill | MCP BookStack in sola lettura | [verificato: ricerca/29 §2-3] |
| PostgreSQL `memoria` | persone, regole strutturate, registro degli agenti, obiettivi, prezzi, meeting, decisioni, passaggi | MCP memoria, sola lettura | [verificato: ricerca/29 §6.1 e §7.1] |
| Qdrant con MCP RAG | trascrizioni, mail, documenti, Sirius, bandi, pagine BookStack, issue Jira | MCP RAG con i permessi della persona | [verificato: board; ricerca/29 §8.6] |
| Jira | to-do e progetti | MCP Jira | [verificato: ricerca/29 §4] |
| M365 | documenti, posta, calendario | MCP posta e calendario in lettura, solo sulle caselle in ambito | [verificato: ricerca/29 §5] |
| mcp-memory | appunti di lavoro del singolo agente | taccuino per famiglia, mai dati dei clienti | [verificato: ricerca/29 §7.1] |

- **Il token della persona.** Il runner firma un token con una chiave tenuta in Infisical, a vita breve, destinato solo all'MCP RAG. La persona è chi ha avviato il lavoro: l'`aadObjectId` dalla Porta, o chi ha creato l'orario in n8n. Mai un campo scritto dal modello. Il risultato va solo a chi può vedere quei dati: niente risposte di un lavoro di Alessandro in un canale aperto a tutti [non verificato: proposta del giudizio sicurezza §8 punto 3; il passaggio dell'intestazione è verificato: code.claude.com/docs/en/agent-sdk/mcp].
- **I permessi per documento** li applica l'MCP RAG con filtri sul payload: Qdrant ha chiavi per collezione, non per documento [verificato: ricerca/29, da qdrant.tech/documentation/security].
- **I numeri si calcolano, non si cercano.** Debrief e controllo di gestione leggono numeri calcolati dal codice su dati strutturati in PostgreSQL, non trovati con il RAG [verificato: ricerca/29 §8.5].
- **Dati rossi e Claude Team.** L'MCP RAG dà a Claude Team verde e giallo, e il rosso solo oscurato, finché parere e DPIA non decidono. La collezione `finanza` è separata e si toglie a Claude Team con una regola [verificato: regola dei tre colori, PRESENTAZIONE-CEO §5.6; proposta di ricerca/29 §6.2].

### 5.6 Chat di gruppo e canali

- **Teams è la casa comune.** Un team "SerSan Agent OS" con un canale per squadra, "Approvazioni", "Agenti", "Ingresso", "Call di vendita", "Bandi" e un canale privato per cliente [verificato: ricerca/28 §8.1].
- **Registrazione dei bot.** "Teams-managed", senza sottoscrizione Azure; se dà errori 401, un Azure Bot F0 gratuito (nessuna risorsa che gira) oppure il piano B: carte sulla pagina del Cancello dietro Pangolin con Entra e FIDO2, e avvisi in Teams [verificato: ricerca/28 §2.2; Q&A 5706215 e 5650695 per i 401].
- **Il nodo Teams di n8n** serve solo agli avvisi: su Teams registra solo l'ora della risposta, non chi approva [verificato: ricerca/28, documentazione di n8n].
- **Telegram** solo per avvisi senza contenuto, in long polling, senza porte aperte [verificato: ricerca/28 §6.1].
- **WhatsApp** soprattutto verso i clienti, sempre dal Cancello, con la Cloud API ufficiale e un numero dedicato. I modelli oltre le 24 ore li manda l'esecutore del Cancello. La verifica Meta Business si chiede nella fase 2 [verificato: ricerca/28 §6.2; giudizio visione §8 punto 2].
- **Slack** con l'adattatore dello stesso Chat SDK, per i clienti che lavorano in Slack [verificato: github.com/vercel/chat, licenza MIT, controllato nei giudizi del 25/10/2026].
- **Buzz** come stanza degli agenti in Experimental-2, via `claude-agent-acp`, collegata alla stessa bacheca. **Criteri per uscire dal LAB:** issue #7375 chiusa (oggi fa perdere risposte senza errore); nessuna approvazione automatica dei permessi; PR delle approvazioni (#8057, #7616) unite; un aggiornamento che passa i 10 scenari; patch nei 14 giorni. Finché non valgono, Buzz resta in LAB senza dati dei clienti [verificato: ricerca/26 §7.3 e ricerca/28 "Fatti" per le issue; criteri: proposta].
- **Claude Team è la finestra delle persone**: chat, skill, progetti per squadra, connettore verso l'MCP RAG. Nessun processo aziendale gira sui compiti programmati di Claude Team: tutto ciò che è a orario resta in n8n [verificato: richiesta del giudizio CEO §9 punto 7; code.claude.com/docs/en/routines].
- **Claude Tag in Teams** è solo in lista d'attesa, senza data [verificato: ricerca/28 §2.5].

### 5.7 Le regole di sicurezza che il disegno applica

- **Rete.** Agenti in una VLAN propria, senza internet; il web passa da Firecrawl; Cancello in una macchina separata; un solo endpoint MCP pubblico (§4.4).
- **LiteLLM è un bene critico**: custodisce la chiave Anthropic e tutte le chiavi virtuali. Le versioni 1.82.7 e 1.82.8 su PyPI erano compromesse il 24/03/2026 [non verificato: netspi.com, fonte di terzi letta nel giudizio sicurezza]. Quindi: immagine fissata per digest e controllata; uscita solo verso `api.anthropic.com`; pannello solo dalla VLAN MGMT; chiave principale in Infisical con rotazione; la chiave diretta per famiglia solo sullo stage [non verificato: proposta del giudizio sicurezza §8 punto 6].
- **Trascrizioni e cancellazione.** `cleanupPeriodDays` basso (di default le sessioni restano 30 giorni), `persistSession: false` per i lavori con dati rossi, dataset ZFS cifrato, conservazione scritta nel registro dei trattamenti. La cancellazione su richiesta raggiunge `SessionStore` in PostgreSQL, Qdrant, Loki e i backup del PBS [verificato per i 30 giorni: giudizio sicurezza §2; il resto: proposta].
- **Sullo stage, prima che F3 sia validata,** si salvano solo dati verdi e gialli. Le trascrizioni delle call si leggono da Graph, si oscurano in memoria con un filtro locale su CPU, vanno all'API e si conserva solo il riassunto [non verificato: proposta che applica la regola dei tre colori, PRESENTAZIONE-CEO §5.6, e il limite del giudizio CPTO §7.2].
- **Telefoni che approvano** dentro il perimetro Cyber Essentials, anche se personali: sistema supportato, blocco schermo, MFA, aggiornamenti [verificato: ricerca/25 N03, da iasme.co.uk].
- **Servizi aggiunti:** Postiz e listmonk mai pubblici; n8n pubblico solo sui webhook firmati; scansione delle vulnerabilità con Wazuh su ogni VM e container (§4.5).
- **Revisione esterna** di Cancello, Porta e ponte prima che i dati dei clienti restino salvati sul server (decisione 5).
- **Versioni fissate.** SDK oggi TypeScript 0.3.310 con Claude Code 2.1.310; aggiornamento ogni due settimane dopo i 10 scenari, dentro i 14 giorni [verificato: registry.npmjs.org, 25/10/2026; ricerca/26 §11].

### 5.8 Le classi d'azione nel Cancello

| Classe | Esempi | Come passa |
|---|---|---|
| Lettura | cercare, leggere | consentita agli strumenti ammessi |
| Scrittura interna | to-do in Jira, meeting nel CRM, evento del debrief in Outlook | regola scritta, senza carta, a nome del responsabile; registro |
| Invio a cliente o prospect | follow-up, risposta, recap nel canale condiviso, WhatsApp | carta ad Alessandro; solo al dominio del cliente; primo contatto con FIDO2 |
| Pubblicazione | post, newsletter, risposte ai commenti, pagine del sito | carta ad Alberto o al founder del profilo |
| Offerte, contratti, affermazioni tecniche | | carta a Michele, con FIDO2 |
| Fatture e solleciti | | carta ad Alessandro o Michele, con FIDO2; pagamenti mai automatici |
| Codice e infrastruttura | modifiche alle skill, PR, patch | carta ad Alberto, con FIDO2; patch del server a Michele |
| Cancellazione e credenziali | | sempre negate agli agenti |

[verificato: PRESENTAZIONE-CEO §5.4 per le classi; ricerca/22 §3 per gli approvatori; FIDO2: proposta del giudizio sicurezza]

**Regole "Sempre".** Dopo 20 approvazioni uguali senza modifiche, una persona può renderle automatiche per quell'agente, quel tipo d'azione e quella destinazione. Scadono dopo 30 giorni e si rivedono ogni mese. Mai per offerte, primi contatti, pagamenti, cancellazioni, né per destinatari o domini nuovi [verificato: PRESENTAZIONE-CEO §5.4; scadenza: proposta del giudizio sicurezza §8 punto 10].

---

## 6. Mappa prima → ora

"Prima" è la proposta del 24/10/2026 (`PRESENTAZIONE-CEO.md`, `ricerca/22`).

| Prima | Ora | Fonte |
|---|---|---|
| Hermes Agent come orchestratore | motore nostro sull'Agent SDK in `agenti-01`; Hermes come uscita prezzata | §1-2 |
| Hermes Cloud come palestra e riserva | nessuno; la riserva è il ripristino dal PBS a casa | [verificato: ricerca/25 C10] |
| Bacheca e cron di Hermes | bacheca in PostgreSQL con le idee di Hermes; orari in n8n | §5.4 |
| Slack Pro come chat di partenza | Teams (M365) con la Porta e nove bot di squadra; Slack solo come eccezione per i clienti | [verificato: ricerca/25 C01; ricerca/28] |
| Claude in Slack con tetto | Claude Team con il connettore MCP RAG | [verificato: ricerca/25 C01, C22] |
| Telegram e WhatsApp via Hermes | Telegram e WhatsApp dalla Porta (Chat SDK), stesso codice di Teams | §5.6 |
| Buzz in prova nella fase 2, forse chat principale | Buzz in Experimental-2 collegato alla bacheca, con criteri per uscire dal LAB | §5.6 |
| Notion per regole, processi, obiettivi, organigramma | BookStack per i testi, PostgreSQL per i dati, Jira per i task, Grafana per le viste | [verificato: ricerca/29] |
| Postgres 17 con pgvector | Qdrant con BM25 e reranker, PostgreSQL 16 per i dati | [verificato: ricerca/25 C11] |
| Porta dei modelli del Cancello, una chiave per famiglia | LiteLLM con chiavi virtuali e budget per agente, squadra e persona | [verificato: ricerca/25 C13] |
| Langfuse | OpenTelemetry verso Loki e Prometheus | [verificato: ricerca/25 C12] |
| Recall.ai per registrare le call | trascrizione nativa di Teams via Graph; Vexa per le call dei clienti; trascrizione in casa | [verificato: ricerca/30] |
| ElevenLabs e numero Twilio per Andrea | Asterisk, Pipecat, ascolto e voce con modelli aperti, operatore italiano Messagenet | [verificato: ricerca/31] |
| Google Workspace e Gmail | M365: Outlook ed Exchange via Graph | [verificato: ricerca/25 C03] |
| Cloudflare Tunnel | Pangolin e Traefik; Cloudflare solo DNS | [verificato: ricerca/25 C04] |
| WireGuard, Tailscale, VPS WireGuard | NetBird con SSO Entra e FIDO2 | [verificato: ricerca/25 C05] |
| 1Password | Vaultwarden e Infisical | [verificato: ricerca/25 C15] |
| Backup B2 in cloud | PBS su Lenovo M920t a casa; S3 fuori sede facoltativo | [verificato: ricerca/25 C16] |
| VM Azure | DL380 in casa; Azure spenta nella fase F2 del board | [verificato: board, roadmap F2] |
| Metricool per i post | Postiz in casa dalla fase 4; Metricool come eccezione fino ad allora | [verificato: ricerca/25 N08] |
| Apify per i segnali | Firecrawl del board | [verificato: ricerca/25 N08] |
| moda.app per le slide | Slides e Design di Claude Team e template SerSan; moda.app solo come eccezione | [verificato: 34-proposta-3 §8] |
| Strumento di newsletter da cercare | listmonk con un relay SMTP esterno | [verificato: 34-proposta-1 §4.5] |
| Firma elettronica da cercare | DocuSeal in casa; firma qualificata da fornitore esterno se serve | [verificato: 34-proposta-1 §3.1] |
| Fatturazione da cercare | Sirius se è il gestionale, altrimenti uno strumento in casa (Invoice Ninja, licenza da verificare) | [verificato: ricerca/29 §8] |
| Agenti tutti come profili Hermes | tre tipi di lavoro (schema, sessione, servizio), tutti nel registro | §5.2 |
| Organigramma in Notion | registro in git, Grafana, pagina BookStack | §5.3 |
| Pilota sul server nelle settimane 4-8 | pilota su stage in LAB nelle settimane 5-8; sul server quando il board lo consente | §7.1 |
| Verifica della settimana 8 su Hermes | verifica della settimana 8 sul motore e sul funnel | §7.4 |
| UPS 1.500 VA subito (1.163-1.293 €) | UPS attuale con NUT; UPS rack Eaton 5PX nella fase F5 | [verificato: ricerca/33 §4.3] |
| RAM da bilanciare (160 GB, 138 € in più) | 192 GB già presenti; +192 GB prima della fase 3 | §4.2 |
| GPU da sostituire (2.438-2.555 €) | seconda GPU RTX 2000 Ada da 16 GB (686-775 €) | §4.3 |
| Kit HPE, alimentatori e dischi (tetto 1.000 €) | già presenti; restano 0-200 € di accessori | [verificato: ricerca/33 §4.3] |

---

## 7. Piano per fasi

### 7.1 Ipotesi

- **Capacità del gruppo:** circa 6,5 gp a settimana fino alla fase 3, circa 7,5 dalla fase 4 [verificato: valori di partenza in ricerca/22 §5 e 34-proposta-1 §7.1; da confermare].
- **Riserva:** un terzo sui giorni di sviluppo, come la presentazione. Le settimane sono calcolate sui giorni con la riserva più l'esercizio [verificato: metodo di PRESENTAZIONE-CEO §11 e §15].
- **Il board non si conta due volte.** Le fasi F0-F5 di Michele (montaggio, OPNsense e VLAN, Proxmox, NetBird e Traefik, PBS, uscita da Azure con la migrazione di SersanOutreach, sicurezza, LXC GPU, pipeline Sirius → MCP, Firecrawl con n8n, LiteLLM con budget, lab, seconda GPU, UPS rack) non sono nei nostri gp [verificato: board, roadmap]. Contiamo solo le nostre estensioni e i servizi nuovi oltre il board.
- **Tempi del board,** da sostituire con la stima di Michele: F0-F1 nelle settimane 1-5, F2-F3 nelle 6-14, F4 nelle 15-18, F5 dalla 19 [non verificato: ipotesi di 34-proposta-1 §7.1].
- **Lo stage non riordina il board.** Il pilota delle fasi 1-2 gira su `stage-agenti` nella VLAN LAB, con una chiave API diretta e un tetto nella Console, salvando solo dati verdi e gialli finché F3 non è validata. Prima che la VLAN LAB esista, il lavoro gira sulle macchine di sviluppo con dati di prova [verificato: ricerca/26 §10.3; giudizio CPTO §7.2]. Il "posto agenti" anticipato (LiteLLM, PostgreSQL, Infisical, n8n, le VM in APPS) resta una richiesta a Michele: se arriva, il passaggio sul server si anticipa [verificato: ricerca/25 §6].
- **Ogni fase parte quando la precedente è verificata**, come nel board [verificato: board, "Ogni fase parte quando la precedente è validata"].

### 7.2 Le fasi

| Fase | Settimane | Board in corso | Cosa si costruisce | gp di base | gp con riserva | Esercizio (gp) | Cosa vedete alla fine |
|---|---|---|---|---|---|---|---|
| **0. Valore subito e prove** | 1-4 | F0-F1 | Claude Team per tutti; decisione D0 sull'email e mailbox live; debito di sicurezza di SersanOutreach; registro dei trattamenti e DPIA con la decisione sui dati rossi; spike delle quattro prove; prima parte del runner | 18 | 24 | 0 | Tutti e quattro in Claude Team ogni giorno; calendario dei post pieno fino a Natale; prime offerte e slide con il nostro stile; email decisa e mailbox live; SersanOutreach verde su identità e MFA |
| **1. Pilota su stage** | 5-8 | F1-F2 | motore su stage con il ponte corretto; Cancello parte 1; esecutore Outlook; Porta v1 con le carte; trascrizioni Teams da Graph; oscuramento locale; Post-call, Analista chiamate, Report del mattino | 22,5 | 30 | 0 | Dopo una call Teams il recap arriva nel canale interno e la bozza della mail arriva come carta sul telefono; dopo il sì parte una volta sola; debrief alle 7:00. **Verifica alla settimana 8** |
| **2. Pilota sul server e squadre che si parlano** | 9-21 | F2-F4 | motore sul server con n8n e LiteLLM; Cancello parte 2 con FIDO2; Porta completa e nove bot di squadra; Jira, BookStack, MCP memoria; SersanOutreach su HTTP; bacheca con freno e canale "Agenti"; 11 agenti | 58,5 | 78 | 6,5 | CRM e to-do in Jira dopo ogni call; gli agenti del marketing si passano il lavoro nel canale "Agenti" con il freno in azione; organigramma con 14 agenti e i loro costi; banca dei token in LiteLLM. **Verifica alla settimana 21** |
| **3. Memoria, call, vendite preparate e canali** | 22-35 | F4 | MCP RAG per persona con token firmato; ingressi della pipeline; Vexa e trascrizione in casa; Cancello v2; Telegram, Slack e WhatsApp; 18 agenti | 61,75 | 82 | 7 | Brief la sera prima; offerta in bozza entro un'ora; "cosa ci siamo detti con X?" da Claude Team con i permessi di chi chiede; bot nelle call dei clienti; bandi ogni mattina; posta smistata; gli stessi agenti su Telegram, Slack e WhatsApp; 32 agenti accesi |
| **4. Organizzazione, newsletter e Buzz** | 36-40 | F4-F5 | listmonk e Postiz; banca dei token per persona; proposte di skill con PR; Buzz in Experimental-2 sulla stessa bacheca; 10 agenti | 26,5 | 35 | 2,5 | Prima newsletter dopo il sì; risposte sulla pagina aziendale in carta; mappa dei processi v0; Buzz come stanza degli agenti in LAB; 42 agenti |
| **5. Vendite e voce** | 41-48 | F5 | Andrea su CPU, poi sulla seconda GPU; pipeline pesata e portale clienti; Coach, Pipeline, Clienti simili | 38 | 51 | 8 | Una lead di prova richiamata entro 90 secondi, appuntamento nel CRM; chiamate in entrata con esito nel canale vendite; coaching visibile solo al venditore; 46 agenti |
| **6. Le altre automazioni** | 49-53 | F5 | DocuSeal, fatturazione, assistente personale, pilota Paperclip; 11 agenti | 24 | 32 | 5 | Dal contratto all'incasso senza lavoro a mano; caso studio a fine progetto; tutti i 57 agenti nel registro |
| **Totale** | **1-53** | | | **249,25** | **circa 332** | **29** | |

[non verificato: stime costruite su 34-proposta-1 §4.3 e §7.3, sui rapporti 26-31 e sulle correzioni dei giudizi]

**Oggi si chiedono solo le fasi 0 e 1:** 8 settimane, 40,5 gp di base, circa 54 con la riserva. Con tutta la riserva consumata le due fasi finiscono a metà della settimana 9: la verifica resta alla settimana 8 e misura ciò che c'è [non verificato: calcolo, 54 gp a 6,5 gp a settimana]. Le altre fasi si finanziano una per volta sui risultati; ogni funzione resta nel piano con la sua fase.

**Prima il funnel.** Se alla settimana 8 l'email non è attiva e i founder non pubblicano, le fasi 2 e 3 vanno avanti perché servono anche al funnel, e la fase 5 aspetta: Andrea e la pipeline pesata hanno senso solo con lead vere [verificato: regola di PRESENTAZIONE-CEO §11].

### 7.3 Dettaglio dei giorni

| Fase | Pezzo | gp di base |
|---|---|---|
| 0 | Claude Team per tutti: SSO e controlli (0,5); connettori Atlassian e M365 in sola lettura, il secondo solo dopo la decisione sui dati rossi (1); un progetto condiviso per squadra (1); skill dell'organizzazione: voce del brand, template di slide e documenti, recap, brief, offerta dal catalogo, regole di brand (2,5); modello "Come lavoro" per i quattro (0,5); formazione AI Act art. 4 e assessment (1) | 6,5 |
| 0 | Decisione D0 sull'email con il legale; mailbox live (SPF, DKIM e DMARC su Cloudflare, riscaldamento, pausa e kill switch provati) | 1 |
| 0 | Debito di sicurezza di SersanOutreach: identità, MFA, backup fuori sede | 4 |
| 0 | Registro dei trattamenti, DPIA prima versione con la decisione sui dati rossi verso Claude Team, testi d'avviso | 2 |
| 0 | Spike: bot Teams senza Azure, `aadObjectId` nelle azioni delle carte, `propose_action` con chiamate parallele negate, inoltro di `anthropic-beta` in LiteLLM (2); impostazioni di Teams e Graph per le trascrizioni (1) | 3 |
| 0 | Motore: prima parte del runner, su sviluppo | 1,5 |
| 1 | Motore su stage: runner, registro dei profili con il tipo di lavoro, ponte corretto verso il Cancello, 10 scenari di prova | 5,5 |
| 1 | Cancello parte 1: classi d'azione, approvatori, carte legate al testo, registro a catena, outbox, ESTOP | 6 |
| 1 | Esecutore Outlook via Graph, solo al dominio del cliente | 1,5 |
| 1 | Porta v1: bot Teams con carte `Action.Execute` e identità Entra; piano B con la pagina del Cancello | 3,5 |
| 1 | Trascrizioni Teams lette da Graph sullo stage | 2,5 |
| 1 | Oscuramento locale v1 su CPU, con una prova di qualità | 1,5 |
| 1 | Contenuto di 3 agenti: Post-call, Analista chiamate, Report del mattino | 2 |
| 2 | Motore sul server: orari con n8n, LiteLLM, isolamento in VLAN, OpenTelemetry, `SessionStore` su PostgreSQL, collaudo | 8 |
| 2 | Cancello parte 2: esecutori di calendario, Jira, SersanOutreach e pausa di Instantly; secondo passo con FIDO2; regole "Sempre" con scadenza | 9,75 |
| 2 | Porta completa: rotta pubblica, thread = sessione, `/stop` e `/stato`, canali (5); nove bot di squadra (2) | 7 |
| 2 | Trascrizioni sul server: delta di Graph con n8n, flag "avvisato" dell'Agenda | 2 |
| 2 | Jira per gli agenti (1,75); BookStack con MariaDB (2); MCP memoria (2,5) | 6,25 |
| 2 | SersanOutreach: MCP su HTTP con token per famiglia, operazione "crea deal" | 3,5 |
| 2 | Bacheca e freno (3); idee della kanban di Hermes (1,5); specchio nel canale "Agenti" (1) | 5,5 |
| 2 | Servizi nuovi: VLAN 32, `agenti-01`, `cancello-01`, `mcp-01` in LXC, MariaDB, inventario in NetBox | 2,5 |
| 2 | Tipo di lavoro nel registro; regole di conservazione e cancellazione | 1,5 |
| 2 | Contenuto di 11 agenti: Dettatura, Capo di gabinetto, Agente task, Guardiano, Registro e audit, Banca dei token, Editoriale, Copywriter, Ricerca concorrenza, Analista metriche, Pubblicatore | 12,5 |
| 3 | Ingressi della pipeline (BookStack, Jira, SharePoint, Outlook, trascrizioni), MCP RAG per persona, permessi Graph, organigramma (7,25); token firmato della persona (1); MCP RAG pubblico con OAuth Entra e filtro IP (1) | 9,25 |
| 3 | Modulo riunioni: Vexa, trascrizione in casa, lotti, telefono, prove, esercizio | 19,75 |
| 3 | MCP Firecrawl (0,5); Cancello v2 (2,5) | 3 |
| 3 | Telegram (0,75); ponte Slack (1,5); WhatsApp per i clienti (4) | 6,25 |
| 3 | Servizi nuovi: VLAN 35, `meet-01`, servizio di trascrizione | 1,5 |
| 3 | Contenuto di 18 agenti: Agente chiamate, Agenda, Brief, Proposte, Slide, Vinto/perso, Intake, Email, LinkedIn, Sentinella, Operatore outbound, Smistatore posta, Raccoglitore, Pulitore, Bibliotecario, Archivista, Sistemista, Bandi | 22 |
| 4 | listmonk con relay SMTP e Postiz, mai pubblici | 4,5 |
| 4 | Contenuto di 10 agenti (Project manager, Report cliente, Onboarding, Sviluppatori, Newsletter, Community manager, Video, Grafiche, Mappatore processi, Intervistatore); banca dei token per persona; revisore delle skill | 13,5 |
| 4 | Proposte di skill degli agenti nella cartella "proposte", approvate con una PR | 1,5 |
| 4 | Buzz in Experimental-2 (4); collegamento alla bacheca e criteri di uscita (2) | 6 |
| 4 | Servizi nuovi: Postiz e listmonk | 1 |
| 5 | Andrea su CPU (24) e sulla seconda GPU (4) | 28 |
| 5 | Pipeline pesata e portale clienti | 5 |
| 5 | Contenuto di 3 agenti: Coach vendite, Pipeline, Clienti simili | 3,5 |
| 5 | Servizi nuovi: VLAN 25, `voce-01`, `andrea-01`, seconda GPU nell'LXC | 1,5 |
| 6 | DocuSeal (2,5); fatturazione (3, da confermare dopo aver capito Sirius); assistente personale (2) | 7,5 |
| 6 | Pilota Paperclip in Experimental-2 | 2 |
| 6 | Contenuto di 11 agenti: Contratti, Assistenza clienti, Rinnovi, Casi studio, Sito e SEO, Eventi e webinar, Fatture e incassi, Acquisti, Controllo di gestione, Allenatore AI, Assistente personale | 13,5 |
| 6 | Servizi nuovi: DocuSeal e fatturazione | 1 |

[non verificato: stime; la base è 34-proposta-1 §4.3 e §7.3; le aggiunte sono mie]

**Da 218 a 249,25 gp di base.** In più rispetto alla Proposta 1: fase zero su Claude Team (+4,5, al posto delle sole skill di marketing), mailbox live (+1), correzioni di sicurezza (+4,75), spike con quattro prove (+1), Porta v1 sullo stage (+1), oscuramento locale (+1,5), idee della kanban di Hermes (+1,5), bot di squadra (+2), Buzz collegato alla bacheca (+2), proposte di skill (+1,5), servizi nuovi (+7,5), tipi nel registro (+0,5), MCP RAG pubblico (+1), pilota Paperclip (+2); meno 0,5 sul registro dei trattamenti, perché la formazione passa nella fase zero [non verificato: somma, 31,25 gp]. Nessun pezzo della Proposta 1 è stato tolto.

### 7.4 La verifica della settimana 8

**Criteri tecnici, sullo stage** [verificato: base da ricerca/26 §10.4 e 34-proposta-1 §7.4; il resto non verificato: proposta]:
1. tre profili girano una settimana senza sessioni scambiate;
2. nessun effetto esce senza una carta del Cancello, anche nei 10 scenari (hook in timeout, chiamate parallele, carta scaduta, testo cambiato dopo la carta);
3. una carta lasciata ferma una notte riprende la sessione giusta al mattino;
4. l'approvazione arriva dal telefono con l'identità Entra giusta, dalla carta in Teams o dalla pagina del Cancello;
5. la spesa resta nel tetto della Console e la stima dell'SDK differisce dalla Console meno del 10 %;
6. un aggiornamento dell'SDK passa i 10 scenari ed è in uso entro 14 giorni dall'uscita;
7. sullo stage non resta salvato nessun dato rosso.

**Criteri commerciali** [verificato: base da PRESENTAZIONE-CEO §11 e giudizio CEO §8; il resto non verificato: proposta]:
1. decisione D0 sull'email presa con il legale e mailbox live, o una data scritta se il legale chiede più tempo;
2. follow-up di tutte le call del periodo inviato entro 24 ore: dagli agenti sullo stage, oppure con la skill del recap in Claude Team;
3. carte decise entro 24 ore;
4. almeno 8 post dei founder pubblicati nelle settimane 4-8;
5. numeri del lunedì compilati ogni settimana;
6. tutti e quattro usano Claude Team ogni giorno (statistiche d'uso);
7. SersanOutreach verde su identità e MFA.

Da subito si misura anche quanto passa oggi fra una lead e la prima risposta, come punto di partenza [verificato: PRESENTAZIONE-CEO §11].

**Se un criterio tecnico fallisce:** due settimane per correggere; se il problema è di struttura, si prova Hermes sullo stesso stage con gli stessi 10 scenari (6-8 gp) e si decide sui numeri (§12). **Se falliscono i criteri commerciali:** vale "prima il funnel" (§7.2).

### 7.5 La verifica della settimana 21

Il passaggio alla fase 3, con la memoria e i dati dei clienti su larga scala, richiede [non verificato: proposta]:
- gli stessi criteri tecnici della settimana 8, sul server e con i budget di LiteLLM al posto della Console;
- la revisione esterna di Cancello, Porta e ponte fatta, con i rilievi gravi chiusi;
- nessuna risposta di un lavoro di una persona finita in un canale aperto a tutti;
- tutti i servizi nuovi in NetBox, con le patch critiche applicate entro 14 giorni;
- la RAM misurata con 6 sessioni e la decisione d'acquisto presa (§4.2).

### 7.6 Cosa non è contato, e perché i gp non si confrontano

- **Non contato:** le fasi F0-F5 del board; la migrazione di SersanOutreach dentro "ci → apps → mesh"; l'MCP RAG di base e la pipeline Sirius → MCP della fase F4 (contiamo solo le nostre estensioni) [verificato: board].
- **Contato a parte:** l'esercizio, circa 0,5 gp a settimana nelle fasi 2-4 e circa 1 gp nelle fasi 5-6, perché i servizi da tenere aggiornati crescono [non verificato: stima].
- **Il confronto con le altre proposte non è alla pari.** I 67 gp per il contenuto dei 57 agenti sono una stima prudente che la P2 e la P3 non fanno (§2.4). I CEO non devono leggere 249 contro 171 come costo del motore.

### 7.7 Le leve sul calendario

- **Capacità.** Con circa 9 gp a settimana dalla fase 2 il calendario scende a circa 42 settimane [non verificato: calcolo].
- **Posto agenti anticipato da Michele.** Il passaggio sul server si anticipa di alcune settimane, ma i giorni restano gli stessi [non verificato: deduzione].
- **Tempi del board.** Se F4 arriva dopo la settimana 18, la fase 3 slitta di conseguenza; lo stage tiene vivo il pilota nel frattempo [non verificato: deduzione].

---

## 8. Copertura voce per voce

### 8.1 Le 90 voci della visione

"Cosa serve ancora" dice cosa manca oggi per avere la voce intera. "Costo" è la spesa in più per quella voce, oltre al lavoro del piano. Le fasi sono quelle del §7.

| Voce | Componente che la realizza | Cosa serve ancora | Costo | Fase |
|---|---|---|---|---|
| J1 Un solo sistema multi-agente | motore unico sull'Agent SDK, una bacheca, una memoria, un Cancello, Teams con la Porta | niente oltre al piano | dentro il piano | 2-6 |
| J2 Squadre con compito e responsabile | registro dei profili con responsabile; un team LiteLLM e un bot Teams per squadra | niente | 0 € | 1-2 |
| J3 Outreach con agente email | Agente email su SersanOutreach (MCP) e Instantly | email live dopo la decisione D0 con il legale | Instantly 69,33 €/mese, già nel board | 0 (email), 3 (agente) |
| J4 Email → proposte → chiamate | bacheca con passaggi e freno, specchio nel canale "Agenti" | niente | 0 € | 2-3 |
| J5 Agente in ogni chiamata | trascrizione nativa di Teams via Graph per le nostre call; Vexa per Teams di altri, Meet e Zoom; telefono via NetBird per il dal vivo | il cliente deve ammettere il bot; riserva con la registrazione sul PC; RAM per Vexa | 0 € di licenze; vivavoce 100-250 € una volta | 1 (Teams), 3 (Vexa) |
| J6 Brief prima e dopo, slide per noi e per il cliente | Agente brief e Agente slide con i template SerSan; le stesse skill in Claude Team | template SerSan da preparare | 0 €; 26,80 €/mese solo se resta moda.app | 0 (skill), 3 (agenti) |
| J7 Marketing con outreach e studio | squadre Marketing e Studio sul motore; Firecrawl; Postiz; HyperFrames in locale; passaggi con l'Outbound in bacheca | Higgsfield come eccezione per i video; Metricool finché Postiz non è pronto | Higgsfield 41,99 €/mese; Metricool 59,86 €/mese fino alla fase 4 | 2-4 |
| J8 Squadra progetti | Jira, Project manager, Agente task, Report cliente, Onboarding, Sviluppatori | Jira Standard se servono permessi diversi | 0-28,27 €/mese | 2, 4 |
| J9 Chat di gruppo come Buzz, con Slack, Telegram, WhatsApp | Teams con la Porta e nove bot di squadra; Telegram, Slack e WhatsApp dallo stesso codice; Buzz in Experimental-2 sulla stessa bacheca | sì di Michele alle eccezioni; verifica Meta Business; Experimental-2 (fase F5 del board) | Telegram 0 €; Slack 0-27 €/mese; WhatsApp circa 7-12 €/mese; Buzz 0 € | 2, 3, 4 |
| A1 Tutte le riunioni registrate e trascritte | Teams via Graph, Vexa, telefono, trascrizione in casa, avviso in tre livelli | parere sull'art. 4 dello Statuto se ci sono dipendenti; DPIA | dentro il parere legale | 1-3 |
| A2 Memoria relazionale | BookStack per i testi, PostgreSQL per i dati, MCP memoria | MariaDB da aggiungere al board | 0 € | 2 |
| A3 Memoria vettoriale | Qdrant con BM25 e reranker, MCP RAG con l'identità della persona | pipeline del board (fase F4) | 0 € | 3 |
| A4 Orchestratore sul server | motore sull'Agent SDK, prima su stage poi in `agenti-01` | posto agenti o fine di F3 per passare sul server | 0 € di licenza | 1-2 |
| A5 Agenti per ruolo | squadra Memoria più pipeline del board; squadre d'azione | niente | 0 € | 3 |
| A6 Agenti che imparano | skill in git; gli agenti scrivono proposte nella cartella "proposte"; revisore settimanale; una persona approva con una PR | niente | 0 € | 4 |
| A7 Chat condivisa fra agenti | specchio della bacheca nel canale "Agenti", @menzioni; Buzz in pilota | niente | 0 € | 2 |
| B1 Punti nel canale del cliente | canale privato Teams subito; canale condiviso, mail, Slack o WhatsApp dopo la carta | canali condivisi fra organizzazioni da provare | 0 € | 1-3 |
| B2 Opportunità nel CRM | esecutore del Cancello sull'MCP di SersanOutreach, operazione "crea deal" | MCP su HTTP con token (oggi solo stdio) | 0 € | 2 |
| B3 Mail di follow-up | bozza, carta, esecutore Outlook via Graph, solo al dominio del cliente | permesso d'invio limitato con RBAC di Exchange | 0 € | 1 |
| B4 To-do al team | Jira, scrittura interna del Cancello | niente | 0 € | 2 |
| B5 Autonomia crescente | regole "Sempre" dopo 20 sì uguali, con scadenza di 30 giorni | niente | 0 € | 2-6 |
| C1 Debrief del mattino | Report del mattino alle 7:00 in Teams e per mail, numeri da PostgreSQL | niente | 0 € | 1 |
| C2 Un agente anche al posto di chi manca | registrazione automatica delle nostre riunioni Teams; Vexa per le altre | provare se Teams registra senza nessuno di SerSan collegato | 0 € | 3 |
| C3 Analisi della call con Claude | sessione post-call senza strumenti, uscita a schema | niente | 0 € | 1 |
| C4 Dettatura | dettatura delle app Claude; Agente dettatura; note vocali dal telefono trascritte in casa | niente | 0 € | 0, 2, 3 |
| C5 Registro dei meeting e pipeline | tabella dei meeting in PostgreSQL, vista in Grafana | niente | 0 € | 1-2 |
| C6 Regole di ciascuno lette prima di ogni lavoro | pagina "Come lavoro" in BookStack letta per ID; `CLAUDE.md` di squadra; istruzioni dei progetti Claude Team | niente | 0 € | 0, 2 |
| D1 Pipeline pesata sullo storico | probabilità per stadio dagli eventi di SersanOutreach | storico: oggi 0 vinti e 91 deal senza valore; pesi dichiarati fino a 30-50 chiusure | 0 € | 5 |
| D2 Brief dall'email della persona | SersanOutreach, mcp-enrich, Firecrawl, MCP RAG, posta | email live per le aperture; Apollo e Perplexity come eccezioni | Apollo 43,78 €/mese; Perplexity prezzo da trovare | 3 |
| D3 Storico della relazione | MCP RAG con filtro cliente, tabella dei meeting | niente | 0 € | 3 |
| D4 Slide automatiche | skill delle slide in Claude Team; Agente slide sul motore | template SerSan; moda.app solo se ammesso | 0 € o 26,80 €/mese | 0, 3 |
| D5 Offerta dal catalogo | skill dell'offerta in Claude Team; Agente proposte su Opus con catalogo in BookStack e PostgreSQL; carta a Michele | niente | 0 € | 0, 3 |
| E1 Tempo per imparare | piano con riserva di un terzo ed esercizio dichiarato | niente | dentro il piano | tutte |
| E2 Costruire ora | Claude Team dalla settimana 1; prezzi del 24-25/10/2026; versioni fissate | niente | dentro il piano | tutte |
| E3 Banca dei token | tetto della Console sullo stage; LiteLLM per agente, squadra e persona; avviso all'80 % dal Cancello, stop al 100 % | LiteLLM (fase F4 del board o posto agenti) | 0 € | 1, 2, 4 |
| E4 Formazione | un'ora documentata per i quattro (AI Act art. 4) | niente | 0 € | 0 |
| F1 Metadati del lavoro | report e log di M365 aggregati, al massimo 21 giorni | individuare le API di M365; accordo di ciascuno | 0 € | 4 |
| F2 Interviste guidate | Intervistatore in chat 1:1 di Teams | niente | 0 € | 4 |
| F3 Mappa dei processi | Mappatore, libro "Processi" in BookStack | niente | 0 € | 4 |
| F4 Ore implicite e automazioni | analista mensile su Opus, ore in PostgreSQL | niente | 0 € | 4 |
| F5 AI per tutti | Claude Team, Teams, Open WebUI con budget per persona | niente | 0 € nel bundle | 0 |
| G1 Call di vendita in un canale | canale Teams "Call di vendita" dal post-call | niente | 0 € | 3 |
| G2 Fit score | qualificatore di SersanOutreach esteso alle call | volumi di call | 0 € | 5 |
| G3 Valutazione della call | Coach vendite, senza stima delle emozioni (AI Act art. 5(1)(f)) | parere legale | dentro il parere | 5 |
| G4 Report a chi ha fatto la call | chat 1:1 di Teams; al responsabile solo aggregati; il token della persona decide chi vede | parere per andare oltre gli aggregati | 0 € | 5 |
| G5 Andrea in 90 secondi, 24/7 | Asterisk, Pipecat, Haiku 5.5 col pensiero spento, ascolto e voce in casa; modulo del sito via n8n | operatore telefonico italiano (eccezione); prova della voce italiana; parere legale; seconda GPU consigliata | 44,24-90,43 €/mese; attivazione 7-14 €; GPU 686-775 € | 5 |
| G6 Impara dai rifiuti | analisi settimanale, nuove aperture via Cancello, test A/B | volumi | 0 € | 5 |
| G7 Più conversione | tempo di richiamata e meeting nel debrief | niente | 0 € | 5 |
| G8 Vinti e persi al marketing | Analista vinto/perso → Editoriale nella bacheca | chiusure: oggi 0 | 0 € | 3 |
| G9 Agenti in organigramma fino a cento | registro dei profili, Grafana, pagina BookStack, bot di squadra | RAM oltre le 16 sessioni insieme | RAM 816-1.218 € (decisione 11) | 2-6 |
| G10 Superpotere | il risultato dell'insieme | niente | dentro il piano | tutte |
| H1 Formarsi e sperimentare | due ore a settimana; Claude Team; Open WebUI; Experimental-2 come sandbox | Experimental-2 (fase F5 del board) | 0 € | 0-6 |
| H2 Non delegabile | i CEO approvano dal telefono e leggono il debrief | niente | 0 € | 1 |
| H3 Assessment | assessment iniziale in Claude Team; Intervistatore per ruolo | niente | 0 € | 0, 4 |
| H4 Ambassador | tetto più alto in LiteLLM | niente | 0 € | 4 |
| H5 Tutti costruiscono | ognuno possiede almeno un profilo nel registro | niente | 0 € | 4 |
| H6 Premio mensile | classifica in Grafana dal registro | budget del premio | 50-100 €/mese | 4 |
| H7 Cambiare modo di lavorare | rituali di adozione | niente | 0 € | tutte |
| I1 Il contesto fa la qualità | quattro case e una porta di ricerca | niente | 0 € | 2-3 |
| I2 Oltre la versione base | skill, MCP e profili su misura | niente | 0 € | 2-6 |
| I3 Aree dove l'AI non entra | classi negate nel Cancello; regole deny valide anche in `bypassPermissions` | niente | 0 € | 1 |
| I4 Marketing più creativo | Editoriale, Copywriter, Metriche, Pubblicatore | niente | 0 € | 2 |
| K1 Debrief come primo appuntamento | evento Outlook creato dall'esecutore | niente | 0 € | 2 |
| K2 "Ho trovato tre nuove call" | annuncio nella bacheca e nel canale "Agenti"; l'Agenda manda gli inviti dopo il sì | niente | 0 € | 3 |
| K3 Posta smistata con risposte pronte | Smistatore posta su Graph con caselle limitate; invio dal Cancello | accordo di ciascuno sulla propria casella | 0 € | 3 |
| K4 Chiedere cosa si è detto in una call | Claude Team con l'MCP RAG; Capo di gabinetto in Teams | regola sui dati rossi verso Claude Team (DPIA e parere) | 0 € | 3 |
| K5 Brief di intake e onboarding | Agente intake da modulo, posta, WhatsApp | niente | 0 € | 3 |
| K6 Slide con la storia della relazione | Brief, Slide, MCP RAG | niente | 0 € | 3 |
| K7 Il nostro stile | template SerSan in SharePoint; skill di brand in Claude Team e sul motore | template da preparare | 0 € | 0 |
| K8 Portale clienti con Claude Code | SersanOutreach come portale, cruscotto della pipeline | niente | 0 € | 5 |
| K9 Newsletter | Agente newsletter e listmonk | relay SMTP esterno | meno di 1 €/mese | 4 |
| K10 Andrea anche in entrata | gruppo di squillo in Asterisk, poi Andrea; esito nel CRM e nel canale vendite | come G5 | come G5 | 5 |
| K11 Perché si chiude e cercarne simili | Analista vinto/perso e Agente clienti simili | volumi | 0 € | 3, 5 |
| K12 Formazione continua dei commerciali | piano mensile del Coach | niente | 0 € | 5 |
| K13 Mappa e assessment per i clienti | Mappatore e Intervistatore in un'istanza separata per cliente | istanza e dati separati da progettare | lavoro da stimare quando c'è il primo cliente | 4-6 |
| K14 Finanza e obiettivi nella memoria | tabella degli obiettivi; numeri di Sirius in PostgreSQL via n8n; documenti nel RAG | sapere cos'è Sirius | 0 € | 3-6 |
| K15 Acquisti automatizzati | Agente acquisti: fatture dei fornitori dalla posta, rinnovi; pagamenti sempre su carta | strumento di fatturazione | vedi L2 | 6 |
| K16 Assistente personale | profilo privato senza memoria aziendale; dati di salute nell'account Claude personale | consenso della persona | 15,19-17,87 €/mese a persona, se lo paga l'azienda | 6 |
| L1 Contratto con firma elettronica | Agente contratti e DocuSeal | valore legale della firma semplice nel parere; firma qualificata da fornitore esterno se serve | 0 €; firma qualificata a preventivo | 6 |
| L2 Fatture, incassi, solleciti | Agente fatture; Sirius se è il gestionale, altrimenti Invoice Ninja in casa | chi fattura (UK, o SDI se c'è un soggetto italiano) e con quale sistema | 0 € o il canone dello strumento scelto | 6 |
| L3 Margini, cassa, obiettivi | Controllo di gestione su PostgreSQL e Grafana | dati strutturati di Sirius | 0 € | 6 |
| L4 Bandi e finanziamenti | pipeline bandi del board più Agente bandi | niente | 0 € | 3 |
| L5 Assistenza nella stanza del cliente | canale condiviso Teams, mail, WhatsApp o Slack; risposte su carta | come B1 e J9 | come J9 | 6 |
| L6 Rinnovi e clienti a rischio | Agente rinnovi su call, report e Jira | niente | 0 € | 6 |
| L7 Caso studio | Agente casi studio; testimonianza chiesta dopo la carta | niente | 0 € | 6 |
| L8 Commenti e messaggi della pagina | Community manager con Postiz | accesso API alla pagina LinkedIn da verificare; Metricool come eccezione | 0 € o 59,86 €/mese | 4 |
| L9 Sito, articoli e SEO | Agente sito con PR su GitHub; deploy su Vercel fatto da una persona | niente | 0 € | 6 |
| L10 Webinar ed eventi | Agente eventi; webinar di Teams; inviti con listmonk; lead in SersanOutreach | licenza dei webinar di Teams da controllare | 0 € se inclusi nel piano M365 | 6 |
| L11 Agente che sorveglia il server | Sistemista in sola lettura su OBSRV e NetBox; patch come carte | stack OBSRV (fase F3 del board) | 0 € | 3 |
| L12 Allenatore | Allenatore AI dal registro d'uso, visibile solo all'interessato | niente | 0 € | 6 |

[non verificato: tabella costruita su 34-proposta-1 §6, con le fasi e i costi di questo piano; i fatti di partenza sono nei rapporti 01, 25-33]

### 8.2 Le integrazioni, nessuna tolta

| Integrazione | Componente | Cosa serve | Costo | Fase |
|---|---|---|---|---|
| Teams (chat di gruppo e carte) | Porta chat con Chat SDK e Teams SDK; nove bot di squadra | registrazione "Teams-managed" o Azure Bot F0; app personalizzate ammesse nel tenant | 0 € se Teams è nel piano M365; altrimenti 5,72-14,29 €/mese | 1-2 |
| Buzz | Experimental-2, `claude-agent-acp` (Apache-2.0), collegato alla bacheca | Experimental-2 (F5 del board); criteri di uscita del §5.6 | 0 € di licenza; 6 gp | 4 |
| Slack | adattatore Slack del Chat SDK | eccezione da far approvare a Michele | 0 € (Free) o 27 €/mese (Pro per 4) | 3 |
| Telegram | Bot API in long polling, solo avvisi | eccezione | 0 € | 3 |
| WhatsApp | Cloud API ufficiale, numero dedicato, modelli inviati dal Cancello | eccezione; verifica Meta Business chiesta in fase 2 | circa 7-12 €/mese; 1.000 messaggi di servizio gratis al mese per numero | 3 |
| LinkedIn | Agente LinkedIn via SersanOutreach (estensione nel browser del membro, con approvazione); pagina aziendale via Postiz | accesso API alla pagina da verificare; Metricool come eccezione | 0 € o 59,86 €/mese | 3-4 |
| M365 (Outlook, SharePoint, OneDrive, Teams) | Graph con `Sites.Selected` e RBAC di Exchange; connettore M365 di Claude Team in sola lettura | consenso di un Global Administrator; decisione sui dati rossi | 0 € nel piano M365 | 0-3 |
| Jira | account di servizio per famiglia (5 inclusi); connettore Atlassian per le persone | piano attuale da conoscere | 0 € o 28,27 €/mese | 0, 2 |
| Instantly | resta come nel board; pausa delle campagne dall'ESTOP | niente | 69,33 €/mese se oggi non è pagato | 2 |
| SersanOutreach | MCP su HTTP con token per famiglia; esecutore del Cancello | decidere dove sta il database (Supabase o PostgreSQL 17 in casa) | 0 € | 2 |
| Claude Team | finestra delle persone; connettore MCP RAG | decisione sui dati rossi | 0 € nel bundle; 446,70 €/mese dopo, con 5 premium | 0 |
| API Anthropic | dietro LiteLLM; chiave diretta solo sullo stage | test di `anthropic-beta`; crediti da verificare | circa 195,65 €/mese stimati, nei crediti finché durano | 1 |
| Voce di Andrea | Asterisk, Pipecat, modelli aperti | operatore telefonico italiano (Messagenet), eccezione | 44,24-90,43 €/mese; 7-14 € di attivazione | 5 |
| Agente nelle call | Graph per le nostre call; Vexa per le altre | ammissione del bot da parte del cliente; RAM | 0 € di licenze | 1, 3 |
| Newsletter | listmonk | relay SMTP (per esempio Amazon SES, 0,10 $ ogni 1.000 mail) | meno di 1 €/mese | 4 |
| Firma elettronica | DocuSeal | parere sul valore legale; firma qualificata se serve | 0 €; qualificata a preventivo | 6 |
| Fatturazione | Sirius o Invoice Ninja in casa | sapere cos'è Sirius e chi fattura | 0 € o canone | 6 |
| Metricool / Postiz | Postiz in casa dalla fase 4 | eccezione per Metricool fino ad allora | 59,86 €/mese fino alla fase 4 | 0-4 |
| Apollo | arricchimento contatti | eccezione | 43,78 €/mese | 3 |
| Apify | sostituito da Firecrawl | copertura di Indeed da provare | 0 €; 15,19 €/mese se resta | 3 |
| Perplexity | arricchimento in SersanOutreach | eccezione finché Firecrawl non lo sostituisce | prezzo non trovato | 3 |
| moda.app | sostituito da Slides e Design di Claude Team | eccezione solo su dati verdi | 0 € o 26,80 €/mese | 0 |
| Higgsfield | video e immagini per i post | eccezione su contenuti pubblici | 41,99 €/mese | 2 |
| Grok Bot | prova di un mese su soli dati pubblici | eccezione cloud | circa 54 € una volta | 2 |
| Paperclip | pilota in Experimental-2 | nessun dato dei clienti | 0 € di licenza; 2 gp | 6 |
| Hermes | uscita prezzata; pilota possibile | §2.4 | 0 € di licenza; 6-8 gp per il pilota | se serve |
| GitHub e Vercel | runner in casa; deploy fatto da una persona | niente | 0 € nuovi | 6 |
| Supabase | database di SersanOutreach, come nel board | chiarire se "il prodotto" è SersanOutreach | costo di oggi, non nei file | 2 |

[verificato: prezzi da ricerca/28, /31, /33 e 34-proposta-1 §4.5, rilevati il 24-25/10/2026; il resto non verificato: proposta]

---

## 9. Costi

### 9.1 Quanto si spende in più rispetto a oggi

Stesso metodo della presentazione: costi nuovi, senza il kit commerciale, con le API dentro i crediti e Claude Team gratuito nel primo anno [verificato: metodo di ricerca/33 §3.1]. IVA esclusa, prezzi del 24-25/10/2026.

| Periodo | € al mese in più | Cosa comprende | Fonte |
|---|---|---|---|
| Fino allo spegnimento di Azure (fasi 0-1 e inizio della 2) | circa 135,27 | Proxmox Community 20,00; IP fisso 10,00; corrente del server e del firewall a 400 W 105,27 | [verificato: ricerca/33 §3.1] |
| Fase 2, Azure spenta | da circa -14,73 a +20,03 | come sopra meno circa 150 di Azure; più Jira Standard 0-28,27; più VPS 0-6,49 | [verificato: ricerca/33 §2.2; hetzner.com/cloud]; somma [non verificato] |
| Fasi 3-4 | da circa -0,98 a +69,61 | più corrente di 12 moduli RAM 6,39-10,22; WhatsApp 7-12; Slack 0-27; relay SMTP circa 0,36 | [non verificato: ricerca/32 §5.2; ricerca/28 §9]; somma [non verificato] |
| Fasi 5-6, con Andrea | da circa 45,81 a 167,70 | più Andrea 44,24-90,43; corrente della seconda GPU 2,55-7,66 | [verificato: ricerca/33 §2.3; corrente non verificata: ricerca/32 §5.2] |

La corrente della seconda GPU è 2,55-7,66 € al mese (10-30 W medi) e quella della RAM 6,39-10,22 € (25-40 W). La cifra 6,39-17,89 € della Proposta 1 era la somma delle due contata come sola GPU [verificato: ricerca/32 §5.2; giudizio CPTO §3.1].

**Voci da aggiungere se succedono:**

| Voce | € al mese | Fonte |
|---|---|---|
| Fine dell'anno gratuito di Claude Team | + 446,70 con 5 premium; 357,36 con 4; 214,42 con 2 premium e 2 standard | [verificato: prezzi su claude.com/pricing/team; calcolo di ricerca/33 §2.2] |
| Senza crediti API | + 195,65 (forbice 90-250) | [non verificato: stima di ricerca/22 §6] |
| Instantly, se oggi non è già pagato | + 69,33 | [verificato: ricerca/33 §2.2] |
| Strumenti commerciali fuori dal board, se restano | + 0-187,62 | [verificato: ricerca/33 §2.5, prezzi in parte non verificati] |
| Teams, se manca dal piano M365 | + 5,72-14,29 | [verificato: listino Microsoft in ricerca/33 §2.2; calcolo non verificato] |
| Account Claude personale per l'assistente personale | + 15,19-17,87 a persona | [verificato: claude.com/pricing, in 34-proposta-3 §8] |
| Premio mensile | + 50-100 | [verificato: PRESENTAZIONE-CEO §14] |

### 9.2 Listino mensile a regime (fase 6)

| Voce | € al mese | Fonte |
|---|---|---|
| Proxmox Community, 2 socket | 20,00 | [verificato: ricerca/33 §2.2] |
| Jira Standard × 4 (0 se il piano Free basta) | 28,27 | [non verificato: ricerca/29 §4.1] |
| IP fisso | 0-10,00 | [non verificato: ricerca/33 §2.2] |
| VPS per Pangolin e NetBird, se serve | 0-6,49 | [verificato: hetzner.com/cloud, 25/10/2026] |
| Corrente del server (400 W) e del firewall | 105,27 | [non verificato: stima di ricerca/33 §2.4] |
| Corrente di RAM e seconda GPU | 8,94-17,88 | [non verificato: ricerca/32 §5.2] |
| API Anthropic | 195,65 | [non verificato: stima di ricerca/22 §6] |
| Andrea (operatore, Registro delle opposizioni, modelli) | 44,24-90,43 | [verificato: ricerca/33 §2.3] |
| WhatsApp verso i clienti | 7-12 | [non verificato: ricerca/28 §9] |
| Relay SMTP | circa 0,36 | [verificato: prezzo SES in 34-proposta-1 §4.5]; volume [non verificato] |
| Slack | 0-27,00 | [verificato: ricerca/22 §9] |
| Instantly | 69,33 | [verificato: ricerca/33 §2.2] |
| **Totale di listino** | **circa 479-583** | [non verificato: somma] |

Per confronto: lo scenario consigliato della presentazione valeva circa 968 € al mese; il rapporto 33 lo porta a 518,95 € dentro il board, senza VPS, WhatsApp, Slack, relay e corrente di RAM e GPU [verificato: ricerca/33 §3.3]. **Motore SDK o Hermes: stesso costo mensile**, perché la licenza è zero in entrambi i casi [verificato: ricerca/33 §2.6].

### 9.3 Licenze dei componenti nuovi

| Componente | Licenza | Costo | Fonte |
|---|---|---|---|
| Agent SDK di Claude | Commercial Terms di Anthropic | 0 €, si paga l'API | [verificato: ricerca/26 §1.1] |
| Chat SDK (`chat`) | MIT | 0 € | [verificato: github.com/vercel/chat] |
| `claude-agent-acp` | Apache-2.0 | 0 € | [verificato: ricerca/26 "Fatti"] |
| Postiz, listmonk, DocuSeal | AGPL-3.0 (DocuSeal con termini aggiuntivi) | 0 € in casa | [verificato: 34-proposta-1 §8.3] |
| Invoice Ninja | Elastic License 2.0 | 0 €; marchio rimosso a circa 40 $ l'anno | [non verificato: fonte terza] |
| Vexa | Apache-2.0 | 0 € | [verificato: ricerca/30 §4.1] |
| Pipecat | BSD-2 | 0 € | [verificato: ricerca/31 "Fatti"] |
| Asterisk 22 LTS | GPLv2 | 0 € | [non verificato] |
| n8n | Sustainable Use License: uso interno sì, rivendita no | 0 € | [verificato: docs.n8n.io, in ricerca/25 C27] |
| Pangolin e NetBird (Community) | AGPL-3.0 | 0 € | [non verificato: ricerca/33 §2.7] |

### 9.4 Una tantum

**Della proposta**

| Voce | Quando | € IVA esclusa | Fonte |
|---|---|---|---|
| Parere legale unico (email, registrazioni, dati rossi verso Claude Team, Andrea e Registro delle opposizioni, coaching, art. 4 dello Statuto, firma) | fase 0; i punti del pilota entro la settimana 3 | tetto 2.500 | [verificato: PRESENTAZIONE-CEO §14, decisione 10] |
| Credito API prepagato, se i crediti finiscono | fase 0 | 0-223 | [verificato: ricerca/33 §4.1] |
| Revisione esterna di Cancello, Porta e ponte | preventivi in fase 1, lavoro entro la settimana 21 | indicativo £3.000-5.000, circa 3.560-5.940 | [non verificato: fonti di terzi lette tramite ricerca il 25/10/2026: thecyphere.com, jumpsec.com, cloudswitched.com; da confermare con due preventivi] |
| RAM +192 GB (12 × 16 GB) | prima della fase 3 (settimana 22), o sotto i 5 GB liberi | 816-1.218 | [verificato: ricerca/32 §2.4] |
| Staffa ad altezza piena o riser per la seconda GPU | con la GPU | 8-90 | [verificato: ricerca/32 §8] |
| Vivavoce da sala per le riunioni dal vivo | fase 3 | 100-250 | [non verificato: ricerca/30 §11.3] |
| Attivazione del numero di Andrea | fase 5 | 7-14 | [verificato: ricerca/33 §4.1] |
| **Totale senza la revisione esterna** | | **3.431-4.295** | [non verificato: somma] |
| **Totale con la revisione esterna** | | **circa 6.990-10.235** | [non verificato: somma] |

**Spese del board che il piano usa** (non contate due volte; le scrivo perché i CEO le vedono insieme)

| Voce | Quando | € | Fonte |
|---|---|---|---|
| PBS a casa (M920t, 2 dischi, 2 SSD per i metadati) | F1 del board | 640-1.180 IVA inclusa (circa 525-967 netti) | [non verificato: somma di ricerca/32 §7] |
| Chiavi FIDO2, 2 a persona | F1 | 232-464 | [verificato: ricerca/33 §4.1] |
| Piccoli accessori | F0-F1 | 0-200 | [non verificato: ricerca/33 §4.1] |
| Seconda GPU RTX 2000 Ada 16 GB | F5 del board, entro l'inizio della nostra fase 5 | 686-775 IVA esclusa (837-946 IVA inclusa) | [verificato: ricerca/32 §4.3] |
| UPS rack 2U (Eaton 5PX 1500 G2 consigliato) | F5 | 937-1.144 | [verificato: ricerca/32 §6] |
| Pagamento del server ("Pagare Bargain") | F0 | non nei file | [verificato: board, roadmap F0] |

**Chiesto oggi, piano più board:** circa 3.257-4.354 €: parere legale, credito API, PBS a 525-967 € netti, chiavi FIDO2, accessori [non verificato: somma]. Prima erano fino a 5.016 € [verificato: PRESENTAZIONE-CEO §1].

---

## 10. Le decisioni da chiedere ai CEO

Solo budget, abbonamenti, integrazioni e acquisti. Le scelte tecniche le decide Michele con noi (§13).

| # | Decisione | Consigliato | Costo | Quando |
|---|---|---|---|---|
| 1 | Avviare le fasi 0 e 1, con la verifica alla settimana 8 | Sì | 40,5 gp di base, circa 54 con la riserva; nessun abbonamento nuovo oltre a quelli del board | oggi |
| 2 | Parere legale unico | Sì, subito | tetto 2.500 € | settimane 1-3 |
| 3 | Tetto mensile delle API se i crediti non bastano, e credito prepagato | Sì | tetto 250 €/mese (stima 195,65 €); anticipo 0-223 € | dalla fase 0 |
| 4 | Spese del board che partono subito: PBS a casa, chiavi FIDO2, accessori | Sì | 640-1.180 € IVA inclusa; 232-464 €; 0-200 € | F1 del board |
| 5 | Revisione esterna di sicurezza di Cancello, Porta e ponte, prima che i dati dei clienti restino sul server | Sì, con due preventivi | indicativo £3.000-5.000 (circa 3.560-5.940 €) | entro la settimana 21 |
| 6 | Jira Standard per 4 persone, se oggi SerSan è su Free | Sì, dalla fase 2 | 28,27 €/mese | fase 2 |
| 7 | VPS per Pangolin e NetBird, se Michele lo preferisce alle porte aperte | Secondo la scelta di Michele | 6,49 €/mese | fase 2 |
| 8 | Canali in più come eccezioni: Telegram, Slack, WhatsApp con numero dedicato | Sì | Telegram 0 €; Slack 0 o 27 €/mese; WhatsApp circa 7-12 €/mese | fase 3 |
| 9 | Relay SMTP per la newsletter | Sì | meno di 1 €/mese | fase 4 |
| 10 | Voce di Andrea: eccezione alla regola delle voci sintetiche nelle call, con un operatore telefonico italiano | Sì, dalla fase 5, solo per chi chiede di essere richiamato, con voce dichiarata, parere e lead vere | 44,24-90,43 €/mese; attivazione 7-14 € | fase 5 |
| 11 | RAM +192 GB (12 × 16 GB) | Sì, prima della fase 3 o quando il margine misurato scende sotto i 5 GB | 816-1.218 € IVA esclusa | settimana 22 |
| 12 | Seconda GPU da 16 GB (consigliata RTX 2000 Ada) e staffa | Sì, nella fase F5 del board | 686-775 € + 8-90 € IVA esclusa | entro la settimana 41 |
| 13 | UPS rack (consigliato Eaton 5PX 1500 G2) | Sì, nella fase F5 del board | 937-1.144 € IVA esclusa | F5 del board |
| 14 | Vivavoce da sala per le riunioni dal vivo | Sì | 100-250 € | fase 3 |
| 15 | Strumenti commerciali fuori dal board | Apollo e Higgsfield come eccezioni; Metricool fino a Postiz (fase 4); Apify sostituito da Firecrawl; moda.app sostituito da Claude Team; Perplexity da decidere col prezzo | fino a 187,62 €/mese; con il consigliato circa 145,63 €/mese fino alla fase 4, poi circa 85,77 € | fase 0 |
| 16 | Posti Claude Team alla fine del bundle | Ridecidere alla scadenza; gli agenti usano la chiave API, quindi si possono tenere meno premium | 446,70 €/mese con 5 premium; 357,36 con 4; 214,42 con 2 premium e 2 standard | scadenza del bundle |
| 17 | Abbonamenti del board: Proxmox VE Community; PBS Community facoltativo; IP fisso | Sì per Proxmox e IP fisso | 20 €/mese; 46,67 €/mese; 0-10 €/mese | F1-F2 del board |
| 18 | Teams nel piano M365, se oggi manca | Sì, se manca | 5,72-14,29 €/mese | fase 0 |
| 19 | Premio mensile per chi costruisce con l'AI | Sì | 50-100 €/mese | fase 4 |
| 20 | Assistente personale: account Claude personale per chi lo vuole | Sì, facoltativo; decidere se lo paga l'azienda | 15,19-17,87 € al mese a persona | fase 6 |
| 21 | Firma qualificata, solo se il parere la chiede per certi contratti | Dopo il parere | a preventivo | fase 6 |
| 22 | Strumento di fatturazione | Sirius se è già lo strumento, altrimenti uno in casa | 0 € o il canone dello strumento scelto | fase 6 |
| 23 | Prova di Grok Bot per un mese, su soli dati pubblici | Facoltativa, come eccezione | circa 54 € una volta | dopo la fase 1 |

[verificato: importi dai §9 e dalle fonti citate lì; i consigli sono miei, non verificati]

---

## 11. Rischi e mitigazioni

| Rischio | Mitigazione | Fonte |
|---|---|---|
| Il collo di bottiglia è il tempo di chi amministra il server: 11-13 servizi nuovi e 3 VLAN nel perimetro Cyber Essentials | tetto ai servizi prima di F4 (§4.5); installazione ed esercizio contati; inventario in NetBox con un responsabile per ogni servizio | [verificato: giudizio CPTO §6] |
| Il codice di sicurezza è nostro (circa 50 gp fra Cancello, Porta, ponte, runner, identità) e nessuno lo ha rivisto | 10 scenari a ogni aggiornamento; revisione esterna entro la settimana 21; Mattia sul codice dal primo giorno | [verificato: giudizio sicurezza §9] |
| L'SDK esce quasi ogni giorno e cambia comportamenti | versione fissata; aggiornamento ogni due settimane dopo i 10 scenari, dentro i 14 giorni | [verificato: ricerca/26 §11; registry.npmjs.org] |
| Trappole di configurazione già trovate (`dontAsk` con `requiresUserInteraction`; hook a comando in timeout) | ponte con hook di callback e `propose_action` senza la marcatura (§5.1); prova negli scenari | [verificato: docs permissions e hooks, 25/10/2026] |
| LiteLLM non inoltra `anthropic-beta` (PR #36736 aperta) | test di accettazione a ogni aggiornamento; chiave diretta solo sullo stage | [verificato: API GitHub, 25/10/2026] |
| LiteLLM compromesso nella catena di fornitura (marzo 2026) | immagine per digest, uscita solo verso Anthropic, pannello da MGMT, chiave in Infisical con rotazione | [non verificato: netspi.com, fonte di terzi] |
| Il bot Teams-managed dà errori 401 | spike nella fase 0; Azure Bot F0 gratuito; piano B con la pagina del Cancello | [verificato: ricerca/28 §2.2] |
| Dati rossi verso Claude Team, senza log di audit né conservazione personalizzata | decisione nella DPIA e nel parere entro la settimana 3; MCP RAG dà il rosso solo oscurato; collezione `finanza` separata | [verificato: claude.com/pricing/team, giudizi] |
| Endpoint pubblici | un solo endpoint MCP; token Entra con destinatario; filtro IP come aggiunta; TLS in passthrough; CrowdSec | [verificato: giudizio sicurezza §8] |
| Iniezioni da mail, trascrizioni, pagine e messaggi | nessuno strumento che invia; testo di terzi letto da sessioni senza strumenti; uscita su allowlist | [verificato: ricerca/26 §11] |
| RAM finita con tutte le funzioni | misura con 6 sessioni; acquisto sotto i 5 GB o prima di Vexa; Vexa Lite e Experimental a richiesta come leve | [verificato: ricerca/32 §3.4; giudizio CPTO §7.6] |
| GPU piena di giorno e assente la sera dalla fase F5 | CPU per embedding e lotti; seconda GPU da 16 GB; due modelli diversi fuori dalla configurazione HPE | [verificato: ricerca/30 §6.2; ricerca/32 §4.4] |
| Piattaforme di call che chiudono ai bot non registrati | Teams nativo per le nostre call; riserva con la registrazione sul PC | [verificato: ricerca/30 "Fatti"] |
| Voce italiana di Andrea o latenza non buone | prova d'ascolto prima; Haiku 4.5 come riserva; seconda GPU; in ultima istanza una voce in cloud come eccezione | [verificato: ricerca/31 §13] |
| Funnel vuoto: 11 lead, 0 meeting, 0 vinti, campagna ferma dal 09/09/2026 | decisione D0 e mailbox live nella fase 0; criteri commerciali alla settimana 8; Andrea solo con lead vere | [verificato: ricerca/01 righe 15-18, giudizio CEO §8] |
| Calendario lungo (circa 53 settimane) | valore dalla settimana 1; fasi finanziate una per volta; leva della capacità (§7.7) | [non verificato: calcolo] |
| Tempi del board non noti | stage in LAB; posto agenti come richiesta | [verificato: ricerca/25 §6] |
| MinIO non più mantenuto | sostituto scelto da Michele prima di audio e file degli agenti | [verificato: API GitHub, `archived: true`] |
| CPU che Intel non aggiorna più dal 30/06/2025 | domanda a Michele per l'assessore Cyber Essentials; secondo nodo già in roadmap (2027-28) | [verificato: ricerca/32 §1; board, roadmap F5] |
| Anthropic cambia termini o prezzi | chiave API; versioni fissate; memoria, bacheca e registro restano in casa | [verificato: ricerca/26 §11] |

---

## 12. Le uscite, se qualcosa non regge

Ogni pezzo sta dietro un'interfaccia: il motore parla con gli strumenti solo via MCP, con i modelli solo via LiteLLM, con l'esterno solo via Cancello [non verificato: principio di progetto].

| Se non regge | Uscita | Cosa si perde | Cosa resta | Costo |
|---|---|---|---|---|
| Il motore sull'SDK (verifiche delle settimane 8 e 21) | Hermes self-hosted, prima in pilota con 2-3 profili, poi al posto del runner | il runner e il ponte via hook | Cancello (via MCP `propose_action`), LiteLLM, server MCP, Porta, memoria, skill nello stesso formato | pilota 6-8 gp; integrazione 26-33 gp con la riserva [verificato: ricerca/27 §10] |
| LiteLLM | chiave diretta per famiglia con limiti nella Console, solo finché si corregge | budget per persona | tetti del runner (`maxBudgetUsd`) | 0 € [verificato: ricerca/26 §11] |
| Il bot Teams | Azure Bot F0; pagina del Cancello con avvisi; Mattermost come piano B | carte dentro Teams | Cancello e approvazioni con Entra e FIDO2 | 0 € o circa 35,74 €/mese per Mattermost Professional [verificato: ricerca/28 §9] |
| Vexa | Attendee come piano B, escluso per Teams con login; registrazione sul PC | bot automatico nelle call di altri | trascrizione nativa delle nostre call | 2-3 gp di prova [verificato: ricerca/30 §4.3] |
| La voce di Andrea in casa | voci sulla seconda GPU; in ultima istanza un servizio di voce in cloud come eccezione | tutto in casa | Asterisk, Pipecat, operatore | circa 88 €/mese per ElevenLabs Pro [verificato: PRESENTAZIONE-CEO §12.1] |
| Postiz | Metricool come eccezione | programmazione in casa | Community manager e Pubblicatore | 59,86 €/mese [verificato: ricerca/33 §2.5] |
| DocuSeal | firma da un fornitore esterno | firma in casa | Agente contratti | a preventivo [non verificato] |
| L'MCP di BookStack della comunità | MCP nostro con 6-8 strumenti | niente | BookStack | 1,5-2 gp [verificato: ricerca/29 §3.2] |
| Buzz non supera i criteri | resta in LAB; la stanza degli agenti è il canale "Agenti" in Teams | Buzz come casa comune | bacheca, freno, specchio in Teams | 0 € |
| Anthropic | Claude su Bedrock UE solo con il sì di Michele e se un cliente lo chiede | | tutto il resto | a preventivo [verificato: ricerca/25 C24] |
| Tutto il sistema | ESTOP dal telefono: coda ferma, budget di LiteLLM a zero, kill switch di SersanOutreach e pausa di Instantly | gli automatismi | dati in PostgreSQL, BookStack, Jira e M365; il lavoro torna a mano | 0 € [verificato: ricerca/01 riga 288] |

---

## 13. Domande aperte

**Per Michele** (scelte tecniche)
1. In quante settimane chiudi F0-F4? Anticipi il "posto agenti" (LiteLLM, PostgreSQL 16, Infisical, n8n, le VM in APPS) o partiamo su stage in LAB?
2. Ci dai una VM `stage-agenti` nella VLAN LAB appena F1 è validata?
3. Motore in una VLAN 32 nuova, o nella 30 con il firewall di Proxmox per VM?
4. Pangolin e NetBird su un VPS (6,49 €/mese) o con l'IP fisso e porte verso EDGE?
5. Se il bot Teams-managed non funziona, ammetti un Azure Bot F0, solo come registro gratuito?
6. Ammetti le VLAN 25 VOCE e 35 MEET e i servizi MariaDB, Vexa, trascrizione, Asterisk, Pipecat, Postiz, listmonk, DocuSeal e fatturazione, con le fasi del §4.5? Chi patcha ognuno?
7. Ammetti come esterni l'operatore telefonico, Meta per WhatsApp, Telegram, Slack, un relay SMTP e gli strumenti commerciali che restano?
8. Come sono fatti i 192 GB (moduli, velocità, rank)? Quali riser e slot PCIe sono liberi?
9. Seconda GPU: RTX 2000 Ada 16 GB? Accetti di uscire dalla configurazione supportata da HPE, con la garanzia di Bargain?
10. Fasce orarie della RTX 4000 dalla fase F5: a che ora va a Experimental-1 e quando torna?
11. Cos'è Sirius, e cosa sono mcp-enrich, mcp-memory e runner-dash?
12. "Supabase, DB del prodotto" è SersanOutreach? Se il database viene in casa, su PostgreSQL 17 per evitare il ritorno di versione?
13. Con cosa sostituisci MinIO?
14. Piano M365 e piano Jira di oggi? Chi è Global Administrator?
15. Va bene per l'assessore Cyber Essentials una CPU che Intel non aggiorna più dal 30/06/2025?
16. Potenza e autonomia dell'UPS attuale; serve una linea internet di riserva?

**Per Anthropic**
17. I "fino a 500 $ al mese di crediti in comune" del piano Team valgono anche per la chiave API dietro LiteLLM? Si sommano ai crediti del bundle?
18. Sul piano Team ci sono davvero i tetti di spesa per persona?
19. Chiediamo subito la conservazione zero (ZDR) per l'API?
20. Se un giorno il sistema si offre ai clienti, come si applicano all'SDK i termini sulla chiave di ogni utente finale?

**Per il gruppo**
21. TypeScript va bene come linguaggio del motore anche per Mattia?
22. Chi fattura (Sersan Limited nel Regno Unito o un soggetto italiano) e con quale sistema?
23. I clienti usano Teams, Slack o WhatsApp? Per quali casi serve WhatsApp e chi approva i modelli di Meta?

---

## 14. Fonti

**File del progetto** (letti il 25/10/2026)
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt` (board di Michele, vincolante)
- `PRESENTAZIONE-CEO.md` (§1, §4, §5, §11-15)
- `ricerca/00-visione-funzionalita.md`, `01-sersanoutreach.md`, `22-architettura-scelta.md`
- `ricerca/25-board-michele-e-delta.md`, `26-claude-agent-sdk.md`, `27-hermes-self-hosted.md`, `28-chat-di-gruppo-self-hosted.md`, `29-conoscenza-task-e-documenti.md`, `30-call-e-trascrizione-self-hosted.md`, `31-voce-andrea-self-hosted.md`, `32-hardware-e-upgrade.md`, `33-costi-v2.md`
- `ricerca/34-proposta-1-agent-sdk.md`, `34-proposta-2-hermes-self-hosted.md`, `34-proposta-3-claude-team-e-mcp.md`
- `ricerca/35-giudizio-visione.md`, `35-giudizio-ceo.md`, `35-giudizio-cpto.md`, `35-giudizio-sicurezza.md`

**Pagine web lette oggi, 25/10/2026**
- Agent SDK, versione: https://registry.npmjs.org/@anthropic-ai/claude-agent-sdk/latest
- Agent SDK, permessi: https://code.claude.com/docs/en/agent-sdk/permissions
- Agent SDK, hook: https://code.claude.com/docs/en/agent-sdk/hooks
- Hermes, scheda del gateway unico: https://api.github.com/repos/NousResearch/hermes-agent/issues/143547
- Hermes, release: https://api.github.com/repos/NousResearch/hermes-agent/releases
- LiteLLM, PR #36736: https://api.github.com/repos/BerriAI/litellm/pulls/36736
- Hetzner Cloud, prezzi: https://www.hetzner.com/cloud/
- Prezzi dei test di sicurezza nel Regno Unito (fonti di terzi, lette tramite ricerca): https://thecyphere.com/blog/penetration-testing-cost/ ; https://www.jumpsec.com/guides/how-much-does-penetration-testing-cost-in-the-uk/ ; https://www.cloudswitched.com/blog/penetration-testing-cost-uk-2026
- Context7: quota mensile esaurita il 25/10/2026

**Pagine web lette dai giudizi e dai rapporti del 25/10/2026**, riprese qui: code.claude.com (agent-sdk/mcp, routines, claude-projects, hooks), claude.com/pricing/team, support.claude.com (articoli 11175166 e 12542951), platform.claude.com/docs/en/api/ip-addresses, docs.pangolin.net/manage/access-control/rules, github.com/vercel/chat, docs di Hermes (mcp, kanban, hooks, acp), api.github.com/repos/minio/minio, e le fonti su Microsoft, Qdrant, BookStack, Atlassian, Messagenet, NVIDIA, HPE, prezzi di GPU, RAM, UPS e PBS elencate nei rapporti 25-35.
