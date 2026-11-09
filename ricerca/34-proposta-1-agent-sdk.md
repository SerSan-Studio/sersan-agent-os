# 34 · Proposta 1: il motore degli agenti sull'Agent SDK di Claude

**Data:** 25/10/2026. **Per:** Michele Sanna (CPTO), Alessandro Serratt (CEO), Mattia Scattu; preparata per Alberto Tuveri.
**Cosa propone:** un nostro servizio "motore agenti" costruito sull'Agent SDK di Claude, dentro il board dell'infrastruttura di Michele. Accanto al motore: n8n per orari, webhook e integrazioni; LiteLLM come banca dei token; il Cancello per approvazioni, invii una volta sola, registro e stop; PostgreSQL e Qdrant come memoria; BookStack per regole e processi; server MCP per gli strumenti; Microsoft Teams come chat di gruppo.
**Vincolo fisso:** il board di Michele (`allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`). In cloud restano solo M365/Entra ID, Claude Team, API Anthropic dietro LiteLLM, Cloudflare (DNS), GitHub, Supabase, Vercel, Jira, Instantly e uno spazio S3 facoltativo. Azure esce. Tutto il resto è self-hosted [verificato: board, righe 9-13 del testo completo; messaggio di Michele del 25/10/2026].
**Regola di Alberto:** nessuna funzione A1-L12 e nessuna integrazione si toglie o si rimanda a "forse" perché oggi manca un componente. Per ognuna scrivo chi la realizza e, se manca qualcosa, cosa serve: acquisto, abbonamento, servizio da installare, configurazione, giorni. Ciò che non può stare sul server è una necessità esterna con il suo costo.
**Fonti:** rapporti 25-33 di oggi, `PRESENTAZIONE-CEO.md`, `00-visione-funzionalita.md`, `01`, `22`; pagine web lette il 25/10/2026 (elenco nel §12). Context7 oggi ha la quota mensile esaurita: la documentazione dell'Agent SDK l'ho letta direttamente su code.claude.com.
**Etichette:** [verificato: fonte] = letto nella fonte indicata; [non verificato] = stima, proposta o dato di terzi non confermato. gp = giorni-persona. Prezzi IVA esclusa salvo dove scritto, rilevati il 25/10/2026 (quelli presi dalla presentazione sono del 24/10/2026). Cambio 1 $ = 0,8934 € [verificato: ricerca/14, ripreso in ricerca/22].

---

## In breve

Il motore è un servizio TypeScript sull'Agent SDK di Claude, in una macchina virtuale dedicata agli agenti. Fa girare un processo Claude per ogni lavoro, con il profilo dell'agente: regole, skill, strumenti ammessi, chiave di LiteLLM e tetti di spesa. Gli agenti non hanno strumenti che inviano. Per far uscire qualcosa chiamano `propose_action`: un hook dell'SDK ferma il turno, il Cancello crea una carta, una persona approva dal telefono in Teams, l'esecutore agisce una volta sola e la sessione riprende [verificato: ricerca/26 §2, hook `PreToolUse` con `defer`]. Quasi tutto il resto c'è già nel board: n8n, LiteLLM, PostgreSQL 16, Qdrant con l'MCP RAG, BookStack, Infisical, Firecrawl, l'osservabilità. Restano da scrivere sei pezzi nostri: il runner con il registro dei profili, il ponte verso il Cancello, la bacheca con il freno ai giri, la Porta chat per Teams (e per Telegram, WhatsApp e Slack con lo stesso codice), il Cancello stesso e alcuni server MCP.

Tutte le 90 voci della visione hanno un componente. Alcune richiedono qualcosa che oggi non c'è nel board: un operatore telefonico per "Andrea", un relay SMTP per la newsletter, Telegram, WhatsApp e Slack come canali esterni, alcuni strumenti commerciali in cloud, una seconda GPU da 16 GB e altri 192 GB di RAM per lo scenario completo. Il piano ha sei fasi in circa 43 settimane, con **218 gp di base e circa 290 gp con la riserva di un terzo**. Il server delle fasi F0-F3 è lavoro di Michele e non è contato. La spesa in più rispetto a oggi è di circa 135 € al mese finché Azure resta acceso, circa 14-31 € dopo lo spegnimento, circa 78-178 € a regime con Andrea, WhatsApp e Slack. Le API (circa 196 € al mese) restano dentro i crediti finché durano. Le una tantum della proposta sono circa 2.500-2.723 € subito (parere legale e credito API) e circa 931-1.572 € più avanti (RAM, staffa, vivavoce, numero); la seconda GPU (686-775 €) è una spesa del board che conviene anticipare. Se il motore non regge alla verifica della settimana 11, si prova Hermes sugli stessi pezzi: Cancello, LiteLLM, MCP e Porta restano [stima su ricerca/26, /27, /30, /31, /32, /33].

---

## 1. La proposta in una pagina

**Cosa costruiamo.** Un motore agenti nostro, piccolo, sopra l'Agent SDK di Claude in TypeScript. L'SDK dà il ciclo dell'agente, gli strumenti, le sessioni che si riprendono anche da PostgreSQL, i sottoagenti, gli hook, i permessi, i server MCP, le skill e l'output a schema [verificato: ricerca/26 §1-2]. Non dà orari, bacheca fra agenti, profili con nome nel tempo, chat di gruppo né memoria condivisa [verificato: ricerca/26 §8]. Questi li danno lo stack di Michele e i nostri sei pezzi.

**La regola che regge tutto.** Gli agenti preparano, una persona approva, un nostro programma esegue. Quel programma è il Cancello [verificato: ricerca/22 §1].

**Perché l'Agent SDK e non Hermes, nel quadro del board.**
- Il Cancello si aggancia in modo nativo: `PreToolUse` decide consenti, nega, chiedi o rimanda; con "rimanda" il processo si chiude e la sessione riparte quando la persona ha deciso [verificato: ricerca/26 §2, fonti D7-D9].
- Ogni server MCP riceve intestazioni HTTP scelte da noi per ogni sessione [verificato: https://code.claude.com/docs/en/agent-sdk/mcp, 25/10/2026]. Così l'MCP RAG può applicare i permessi della persona per cui l'agente lavora. Hermes invece passa solo un valore fisso o il nome del profilo [verificato: ricerca/27 "In breve"].
- Metà delle funzioni di Hermes nel board è doppia: orari e webhook (n8n), modelli e budget (LiteLLM), memoria (Qdrant e MCP RAG), chat web (Open WebUI) [verificato: ricerca/27 "In breve"].
- Hermes dalla v0.22 ha un solo gateway per tutti i profili, 273 problemi aperti sulla scheda #143547 (9 di sicurezza) e almeno 45 avvisi di sicurezza nel 2026 [verificato: ricerca/27 §1].
- Il costo di licenza è uguale (zero): cambia il lavoro. Hermes integrato costa 26-33 gp con la riserva più 1,5-2,5 gp al mese; il motore nostro circa 27 gp con la riserva [verificato: ricerca/33 §2.6, su stime di ricerca/26 e /27].

**Cosa non è.** Non è Claude Code in mano agli agenti senza freni: modalità `dontAsk` con un elenco chiuso di strumenti, regole deny che valgono anche in `bypassPermissions`, nessuno strumento che invia [verificato: ricerca/26 §2, fonte D6]. Non usa i posti Claude Team: gli agenti usano solo la chiave API dietro LiteLLM, come chiedono i termini di Anthropic [verificato: ricerca/26 §5].

---

## 2. Lo schema

```
PERSONE (4) ── Teams e Outlook (M365, Entra con MFA e chiave FIDO2), dal PC e dal telefono
            ── Claude Team: chat, Claude Code, connettore verso l'MCP RAG
            ── Telegram (solo avvisi) · WhatsApp (clienti) · Slack (se Michele lo ammette)
                 │ HTTPS firmato (bot Teams, webhook)          ▲ long polling (Telegram)
════ OPNsense · VLAN default-deny ════════════════════════════════════════════════════
20 EDGE    Traefik + Pangolin: /api/messages (Teams), webhook, MCP RAG con OAuth,
           pagine di firma, outreach.sersan.io
30 APPS    cancello-01: CANCELLO (carte, approvatori, esecutori, registro, ESTOP)
                        PORTA CHAT (Chat SDK + Teams SDK)
           mcp-01: MCP memoria, bacheca, BookStack, Jira, posta in lettura,
                   Firecrawl, SersanOutreach (lettura e operatore)
           n8n · LiteLLM · MCP RAG · BookStack · Open WebUI · SersanOutreach
           Postiz · listmonk · DocuSeal · andrea-01 (Pipecat, ascolto e voce)
32 AGENTI  agenti-01: MOTORE (runner, registro dei profili, 9 famiglie in container)
           uscita solo verso LiteLLM, mcp-01, MCP RAG e API del Cancello
40 DATA    PostgreSQL 16 · Qdrant · MariaDB (nuovo) · Infisical · Vaultwarden · MinIO
25 VOCE    voce-01: Asterisk 22 LTS (nuovo) ── trunk SIP dell'operatore italiano
35 MEET    meet-01: Vexa (nuovo), bot per le call dei clienti
80 AI      RTX 4000 di giorno: Qwen3-4B, embedding e reranker, Docling, trascrizione
           seconda GPU da 16 GB (consigliata prima di Andrea)
70 OBSRV   Prometheus · Grafana · Loki · Uptime Kuma · Wazuh · NetBox
90 LAB     Experimental-2: pilota Buzz, eventuale confronto con Hermes
═══════════════════════════════════════════════════════════════════════════════════════
CLOUD DEL BOARD   M365/Entra · Claude Team · API Anthropic (via LiteLLM) · Cloudflare DNS
                  · GitHub · Supabase · Vercel · Jira · Instantly · S3 facoltativo
ESTERNI DA AMMETTERE  operatore telefonico · Meta (WhatsApp) · Telegram · Slack · relay SMTP
                  · Apollo, Perplexity, Metricool, moda.app, Higgsfield (se restano)
```

Le VLAN 20, 30, 40, 70, 80 e 90 e i loro servizi sono quelli del board [verificato: board-vlan.txt]. Le VLAN 25, 32 e 35, le macchine `agenti-01`, `cancello-01`, `mcp-01`, `andrea-01`, `voce-01`, `meet-01` e i servizi Postiz, listmonk, DocuSeal e MariaDB sono proposte da far approvare a Michele [non verificato: proposta]. La VLAN 35 MEET viene da ricerca/30 §4.5, la VLAN voce da ricerca/31 §1.1.

---

## 3. Componenti e dove girano

### 3.1 Tabella dei componenti

"Stato" vuol dire: **board** = già previsto da Michele; **config** = nel board, da configurare per gli agenti; **nostro** = codice da scrivere; **nuovo** = servizio self-hosted da aggiungere al board; **esterno** = servizio fuori dal board, da ammettere come eccezione.

| Componente | Cosa fa | Stato | VLAN | Macchina | RAM | vCPU | GPU | Fonte |
|---|---|---|---|---|---|---|---|---|
| **Motore agenti** (runner, registro dei profili, 9 container di famiglia) | coda dei lavori, un processo SDK per lavoro, tetti, ripresa, `/stop` | nostro | 32 AGENTI (in alternativa 30 con il firewall di Proxmox) | VM `agenti-01` con Docker | 12 GB all'inizio (6 sessioni insieme), 16 GB con 8, 20 GB con 12-16 | 8-12 | no | 1 GiB, 1 CPU e 5 GiB di disco per sessione come partenza [verificato: ricerca/26 §3.3]; il resto [non verificato: stima] |
| **Cancello** | classi d'azione, carte, approvatori, esecutori, registro a catena, ESTOP | nostro | 30 APPS | VM `cancello-01` | 3-4 GB | 2-4 | no | [non verificato: stima, ricerca/32 §3.3 dà 1-2 GB al solo servizio] |
| **Porta chat** | bot Teams, poi Telegram, WhatsApp e Slack con lo stesso codice | nostro | 30 APPS | in `cancello-01` | 0,5-1 GB | 1 | no | [verificato: ricerca/28 §9 per la RAM stimata] |
| **Server MCP nostri o adottati** | memoria su Postgres, bacheca, BookStack, Jira, posta e calendario in lettura, Firecrawl, SersanOutreach | nostro e adottati | 30 APPS | VM `mcp-01` | 3-4 GB | 2-4 | no | [non verificato: stima] |
| n8n | orari, webhook firmati, ingressi, avvisi semplici | board | 30 | board | nei 69 GB dei servizi core | | no | [verificato: board-vlan.txt; board, tabella Capacità] |
| LiteLLM | porta dei modelli, chiavi virtuali, budget per agente, squadra e persona | board (fase F4) | 30 | board | nei 24 GB "AI, Firecrawl, Qdrant, LiteLLM" | | no | [verificato: board] |
| PostgreSQL 16 | coda, bacheca, sessioni, Cancello, memoria strutturata, LiteLLM, n8n | board | 40 DATA | board | +1-5 GB di crescita | | no | [verificato: board-vlan.txt] |
| Qdrant con BM25 | memoria vettoriale | board | 40 | board | nel board | | no | [verificato: board] |
| MCP RAG | ricerca con permessi per utente e registro delle query | board (F4), estensioni nostre | 30 | board | nel board | | no | [verificato: board, "Pipeline AI"] |
| Ollama Qwen3-4B, Infinity (embedding e reranker 0.6B), Docling | metadati, ricerca, documenti | board | 80 AI | LXC `ai-gpu-01` | nel board | | RTX 4000 di giorno | [verificato: board-vlan.txt] |
| Trascrizione (faster-whisper turbo, Parakeet v3, pyannote) | audio delle call e delle riunioni dal vivo | nuovo | 80 AI | LXC `ai-gpu-01` | +6-8 GB | 16 thread nei lotti su CPU | 2-4,5 GB di giorno; CPU la sera | [verificato: ricerca/30 §6 e §11.2] |
| Vexa 0.12.x | bot nelle call dei clienti (Teams di altri, Meet, Zoom web) | nuovo | 35 MEET | VM `meet-01` | 12 GB (3 bot) | 6-8 | usa la trascrizione in VLAN 80 | [verificato: ricerca/30 §4 e §11.2] |
| Asterisk 22 LTS | centralino di Andrea | nuovo | 25 VOCE | LXC `voce-01` | 1 GB | 1-2 | no | [verificato: ricerca/31 §1.1 e §8.2] |
| Pipecat con ascolto e voce (Parakeet int8, Pocket TTS) | conversazione di Andrea | nuovo | 30 | LXC `andrea-01` | 6-8 GB su CPU; 4 GB con la seconda GPU | circa 16 con 2 chiamate | seconda GPU nella fase 2 di Andrea | [verificato: ricerca/31 §8.2] |
| BookStack | regole "Come lavoro", processi, catalogo, manuale degli agenti | board, config | 30 | board | nel board | | no | [verificato: board-vlan.txt] |
| MariaDB per BookStack | database richiesto da BookStack | nuovo | 40 | container | 1 GB | 1 | no | BookStack chiede MySQL 8 o MariaDB 10.6 [verificato: ricerca/29 §3.1] |
| Infisical, Vaultwarden | segreti delle app e delle persone | board | 40 | board | | | no | [verificato: board-vlan.txt] |
| Firecrawl | pagine web in markdown per gli agenti | board | 30 | board | | | no | [verificato: board] |
| Postiz | programmazione dei post e metriche, al posto di Metricool | nuovo | 30 | container con Postgres e Redis | 2 GB | 1-2 | no | AGPL-3.0, LinkedIn, Instagram, YouTube e altri, API pubblica [verificato: github.com/gitroomhq/postiz-app, 25/10/2026]; RAM [non verificato] |
| listmonk | newsletter | nuovo | 30 | container, database su PostgreSQL | 0,5 GB | 1 | no | AGPL-3.0, API REST con token [verificato: github.com/knadh/listmonk; listmonk.app/docs/apis/apis, 25/10/2026]; RAM [non verificato] |
| DocuSeal | firma elettronica dei contratti | nuovo | 30, pagine di firma via Pangolin | container | 1 GB | 1 | no | AGPLv3, API e webhook, Docker, PostgreSQL o MySQL; versione 3.3.3 del 19/10/2026 [verificato: github.com/docusealco/docuseal e API releases, 25/10/2026]; RAM [non verificato] |
| Fatturazione | fatture, incassi, solleciti | nuovo, se Sirius non lo fa già | 30 | container | 1-2 GB | 1 | no | Invoice Ninja self-hosted sotto Elastic License 2.0 [non verificato: fonti terze, beancount.io 06/10/2026] |
| Open WebUI | chat sui modelli per tutti, con il budget di LiteLLM | board | 30 | board | | | no | [verificato: board-vlan.txt] |
| Buzz (pilota) | stanza degli agenti alla Buzz, via `claude-agent-acp` | nuovo, solo in LAB | 90 LAB | Experimental-2 | 4-8 GB dentro i 24 GB di Experimental | | no | [verificato: ricerca/28 §9; ricerca/17 citata lì] |
| Teams, Outlook, SharePoint, OneDrive | chat, posta, calendario, documenti | cloud del board | M365 | | | | | [verificato: board] |
| Jira | to-do e progetti | cloud del board | | | | | | [verificato: board] |
| Operatore telefonico (Messagenet) | numero italiano e trunk SIP di Andrea | esterno | | | | | | [verificato: ricerca/31 §4] |
| Relay SMTP (per esempio Amazon SES) | invio della newsletter | esterno | | | | | | Exchange Online non supporta l'invio in massa [verificato: avviso Microsoft MC787382 su mc.merill.net, letto tramite ricerca il 25/10/2026] |
| Telegram, WhatsApp Cloud API, Slack | canali in più verso gli stessi agenti | esterni | | | | | | [verificato: ricerca/28 §6] |

### 3.2 Bilancio della RAM

Il board lascia circa 53 GB liberi su 192 [verificato: board, tabella "Capacità"]. Proxmox limita la cache ZFS al 10 % della RAM con un tetto di 16 GiB: va fissato `zfs_arc_max` a 12 GiB per restare nei 16 GB che il board assegna a host e cache [verificato: ricerca/32 §3.2].

| GB nuovi | Fase B (pilota) | Fasi C-D | Fasi E-F (completo) | Fonte |
|---|---|---|---|---|
| Motore `agenti-01` | 12 | 16 | 20 | [non verificato: stima su 1 GiB per sessione, ricerca/26 §3.3] |
| Cancello e Porta `cancello-01` | 4 | 4 | 5 | [non verificato: stima] |
| Server MCP `mcp-01` | 3 | 4 | 4 | [non verificato: stima] |
| MariaDB | 1 | 1 | 1 | [non verificato: stima] |
| Crescita di PostgreSQL, Qdrant, Loki | 1 | 3 | 5 | [non verificato: ricerca/32 §3.3] |
| Trascrizione e lotti | 0 | 6 | 8 | [verificato: ricerca/30 §11.2, stima di quel rapporto] |
| Vexa `meet-01` | 0 | 12 | 12 | [verificato: ricerca/30 §11.2] |
| Postiz e listmonk | 0 | 2,5 | 2,5 | [non verificato: stima] |
| Andrea (Asterisk, Pipecat, ascolto, voce) | 0 | 0 | 8 su CPU, 4 con la seconda GPU | [verificato: ricerca/31 §8.2] |
| DocuSeal e fatturazione | 0 | 0 | 2,5 | [non verificato: stima] |
| SersanOutreach, worker in più | 0 | 1 | 2 | [verificato: ricerca/32 §3.3] |
| **Totale nuovo** | **21** | **49,5** | **66-70** | [non verificato: somma] |
| **Libera dopo** | **circa 32** | **circa 3** | **da -13 a -17** | [non verificato: calcolo su 53 GB] |

**Lettura.** Il pilota sta largo. Memoria e call arrivano al limite. Lo scenario completo non entra. Ricerca/32 arrivava alla stessa conclusione con meno servizi: da +7 a -11 GB [verificato: ricerca/32 §3.4].
**Proposta.** Comprare altri 192 GB (12 moduli da 16 GB, 384 GB in tutto) prima della fase C, quando entrano Vexa e la trascrizione. È l'unico passo bilanciato a banda piena: 816 € IVA esclusa in moduli da 2133 o £1.020 IVA esclusa (circa 1.218 €) in moduli da 2666 [verificato: ricerca/32 §2.4, configuratori del 25/10/2026]. Il ripiego è +64 GB (4 moduli, 272-512 €) con la banda al 69 % [verificato: ricerca/32 §2.4; Lenovo LP1089 citato lì].
**Leve per rimandare** [non verificato: proposte di ricerca/32 §3.4, più Vexa Lite, che è mia]: Experimental 1 e 2 accese solo quando servono (24 GB); tetto di 12 sessioni di agenti in parallelo; Andrea sulla seconda GPU invece che su CPU (-4 GB); Vexa Lite con una call alla volta (circa 4 GB invece di 12).

**Nota sui cento agenti (G9).** La RAM cresce con le sessioni attive insieme, non con i profili definiti. Cento profili con un tetto di 16 sessioni in parallelo stanno nei 20 GB del motore [verificato: ricerca/32 §3.3, deduzione di quel rapporto].

### 3.3 GPU: fasce orarie e seconda scheda

- **Il motore non usa la GPU.** Gli agenti ragionano con Claude via API. La GPU serve alla pipeline di Michele, alla trascrizione e alla voce di Andrea [verificato: board; ricerca/26 §4.5].
- **RTX 4000 di giorno.** Ollama Qwen3-4B, embedding e reranker, Docling: resta meno di 1 GB libero. La trascrizione dal vivo (circa 2,1 GB) entra solo se il reranker passa sulla CPU [verificato: ricerca/30 §6.1, stima di quel rapporto].
- **La sera** la scheda va a Experimental-1 [verificato: board, SerSan Infra Board.html riga 309 citata in ricerca/25]. Proposta: embedding e reranker su CPU (Qwen3-Embedding 0.6B gira su CPU [verificato: ricerca/13 riga 287, citata in ricerca/25 N06]); trascrizione a lotti su CPU con Parakeet in ONNX (36 volte il tempo reale su una CPU da scrivania [verificato: ricerca/30 §5.1]); bandi e prima indicizzazione nella fascia 01:00-07:00, se Michele restituisce la GPU all'AI di notte [non verificato: proposta, fasce da decidere con Michele].
- **Seconda GPU.** La "RTX A2000 con chip Ada da 6 GB GDDR7" non esiste [verificato: ricerca/25 H07; ricerca/32 §4.1]. Consiglio la **RTX 2000 Ada da 16 GB**, 70 W, 837-946 € IVA inclusa (686-775 € IVA esclusa) al 24-25/10/2026, nel riser secondario con una staffa ad altezza piena [verificato: ricerca/32 §4.3 e §4.7]. Ci stanno insieme Andrea, la trascrizione dal vivo e la pipeline RAG, 24 ore su 24 [non verificato: stima di ricerca/32 §4.6]. Il board la mette in F5; per Andrea e per le call della sera conviene averla prima della fase E [verificato: ricerca/32 §4.7 per la conseguenza].
- **Attenzione.** HPE scrive "Mixing of GPUs is not supported": due modelli diversi escono dalla configurazione supportata [verificato: ricerca/32 punto 4 dell'"In breve"].

### 3.4 Regole di rete da aggiungere

Tutte [non verificato: proposta da scrivere con Michele su OPNsense e nel firewall di Proxmox].

| Da | A | Cosa passa | Perché |
|---|---|---|---|
| `agenti-01` (32) | LiteLLM (30) | `/v1/messages` | modelli; nessun'altra uscita verso internet |
| `agenti-01` | `mcp-01`, MCP RAG, API del Cancello (30) | HTTP interno con token per famiglia | strumenti e `propose_action` |
| `agenti-01` | internet | niente | `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` e nessun WebFetch diretto: il web passa da Firecrawl [verificato: ricerca/26 §3.7] |
| LiteLLM | `api.anthropic.com` | 443 | unica uscita dei modelli [verificato: board, "API Anthropic dietro LiteLLM"] |
| `cancello-01` | Graph, login Microsoft, Bot Framework, Jira, SersanOutreach, Instantly, Telegram, Meta, Slack (se ammesso) | 443 | esecutori e Porta; i nomi esatti dei domini del bot si ricavano nello spike [verificato: ricerca/28 §2.2] |
| EDGE (20) | `cancello-01` | `/api/messages`, `/webhooks/whatsapp`, eventuali webhook Slack | messaggi dei canali; firmati dal mittente [verificato: ricerca/28 §2.2 e §6.2] |
| EDGE | MCP RAG | endpoint MCP con OAuth 2.1 verso Entra | connettore di Claude Team, che parte dai server di Anthropic [verificato: ricerca/29 §7.3] |
| MCP RAG (30) | Qdrant (40) | API di Qdrant | la regola non è scritta nel board [verificato: ricerca/29 §6.3] |
| `meet-01` (35) | internet | 443 e media UDP | i bot entrano nelle call; nessuna rotta verso DATA [verificato: ricerca/30 §4.5] |
| `voce-01` (25) | IP dell'operatore | SIP (meglio TLS 5061) e RTP | trunk di Andrea; sola registrazione o apertura limitata, decide Michele [verificato: ricerca/31 §1.2] |
| OBSRV (70) | tutte | lettura | come nel board [verificato: board-vlan.txt] |

**Esposizione pubblica.** Pangolin in modalità tunnel di solito vive su un VPS con 80 e 443 TCP e 51820 UDP raggiungibili; NetBird self-hosted chiede 80, 443 TCP e 3478 UDP [verificato: ricerca/25 N10]. Due strade: un VPS piccolo (Hetzner da 5,99 € al mese IVA esclusa per la linea "Cost-Optimized" [verificato: hetzner.com/cloud, 25/10/2026]) oppure l'IP fisso con porte aperte solo verso la VLAN EDGE. Decide Michele.

---

## 4. Cosa c'è già e cosa va costruito

### 4.1 Già nel board, usato così com'è

n8n, LiteLLM con budget, PostgreSQL 16, Qdrant con BM25, MCP RAG, mcp-enrich, mcp-memory, openoutreach (SersanOutreach), Firecrawl, bandi-watcher, BookStack, Open WebUI, Infisical, Vaultwarden, MinIO, Ollama con Qwen3-4B, Infinity, Docling, i runner GitHub, Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox, NetBird, Pangolin con Traefik, il PBS a casa, M365 con Teams, Jira, Instantly [verificato: board-vlan.txt; board].

### 4.2 Nel board, da configurare per gli agenti

| Servizio | Configurazione | Fonte |
|---|---|---|
| LiteLLM | una chiave virtuale per agente con tetto mensile, un team per squadra, un utente per persona; ID veri dei modelli (`claude-sonnet-5-5`); inoltro intatto di `anthropic-beta` e `anthropic-version`; test di accettazione | [verificato: ricerca/26 §4.2-4.3; PR #36736 di LiteLLM ancora aperta] |
| n8n | un flusso a orario per profilo che mette un lavoro in coda con una chiamata firmata; webhook del modulo del sito, di Instantly e dei trascritti; nessun flusso che scrive a clienti o prospect | [verificato: ricerca/26 §8; ricerca/25 C27] |
| BookStack | OIDC con Entra e gruppi; ruolo "Agente lettura" per famiglia; libri "Come lavoriamo", "Processi", "Catalogo", "Proposte degli agenti" | [verificato: ricerca/29 §3] |
| Jira | account di servizio per famiglia (5 inclusi), progetto modello per cliente, progetto "Interno"; Standard quando servono permessi diversi | [verificato: ricerca/29 §4] |
| M365 | app Entra per famiglia con `Sites.Selected` e RBAC di Exchange; accesso Graph alle trascrizioni e nomi dei parlanti; connettore M365 di Claude Team in sola lettura | [verificato: ricerca/29 §5; ricerca/30 §3.2] |
| MCP RAG | identità della persona da un token firmato dal runner; filtri su `acl`, `cliente`, `colore`; collezione `finanza` separata | [verificato: ricerca/29 §6.2 e §7.2, proposta di quel rapporto] |
| PostgreSQL 16 | database `motore`, `cancello`, `memoria`, `porta`; ruoli per famiglia con sicurezza per riga | [verificato: ricerca/29 §6.1] |
| OBSRV | OpenTelemetry dell'SDK verso Loki e Prometheus; cruscotti per agente; registro del Cancello in Loki e Wazuh | [verificato: ricerca/26 §2, osservabilità] |

### 4.3 Codice nostro da scrivere

| # | Pezzo | Contenuto | gp base | Fonte della stima |
|---|---|---|---|---|
| 1 | Runner delle sessioni | coda in PostgreSQL con `FOR UPDATE SKIP LOCKED`; un processo per lavoro; cartella, configurazione e chiave per famiglia; `maxTurns`, `maxBudgetUsd`, orologio esterno; `SessionStore` su PostgreSQL; risultato a schema; `/stop` | 3 | [verificato: ricerca/26 §10.2] |
| 2 | Registro dei profili | YAML in git con 57 profili; validazione; pagina BookStack e vista Grafana generate | 1,5 | idem |
| 3 | Ponte verso il Cancello | plugin "sersan-guardrail": hook `PreToolUse`, regole deny, modalità `dontAsk`, `propose_action` marcato `requiresUserInteraction`, `defer` e ripresa | 2 | idem |
| 4 | Bacheca e freno ai giri | tabelle `compiti` e `passaggi`; MCP con 5-6 strumenti; limiti per catena | 3 | idem |
| 5 | Orari, ingressi, LiteLLM, isolamento, osservabilità, collaudo | | 8 | idem (pezzi 5, 7-11) |
| 6 | Cancello | classi d'azione, approvatori, carte, outbox, registro a catena, ESTOP, esecutori (Graph, Jira, SersanOutreach, Instantly, BookStack, SharePoint) | 17,5 | ricerca/22 stimava 21 gp con la porta dei modelli (2) e le carte in Slack (4), che ora fanno LiteLLM e la Porta; più 2,5 gp di esecutori M365 [non verificato: ricalcolo mio su ricerca/22 §5 e ricerca/29 §10] |
| 7 | Porta chat | Chat SDK e Teams SDK, carte `Action.Execute` con `aadObjectId`, rotta pubblica; poi Telegram, WhatsApp, Slack | 8,5 + 0,75 + 4 + 1,5 | [verificato: ricerca/28 §9]; Slack [non verificato: stima mia] |
| 8 | Server MCP | memoria su Postgres (2,5), BookStack in sola lettura (0,75), Jira con `mcp-atlassian` (dentro 1,75), Firecrawl (0,5), SersanOutreach su HTTP con token per famiglia (2,5) | 6,25 + Jira | [verificato: ricerca/29 §10; ricerca/01 riga 315 per il trasporto HTTP che manca] |
| 9 | Ingressi della pipeline e MCP RAG | BookStack, Jira, SharePoint, Outlook, trascrizioni; identità per persona | 5,5 | [verificato: ricerca/29 §10] |
| 10 | Modulo riunioni | trascrizioni Teams, Vexa, lotti, telefono, aggancio al motore | 24,25 | [verificato: ricerca/30 §11.1, centro della forbice 22-29] |
| 11 | Andrea | Asterisk, Pipecat, ascolto e voce, controlli del Cancello, G6, seconda GPU | 28 | [verificato: ricerca/31 §11] |
| 12 | Strumenti nuovi | Postiz (2,5), listmonk con relay (2), DocuSeal (2,5), fatturazione (3), assistente personale (2) | 12 | [non verificato: stime mie] |
| 13 | Pipeline pesata e portale clienti | modulo statistico su SersanOutreach, cruscotto | 5 | [non verificato: stima mia] |
| 14 | Contenuto dei 57 agenti | prompt, `CLAUDE.md`, skill, schemi, prove: 0,5 gp per un agente semplice, 1 per uno medio, 2 per uno complesso | 67 | [non verificato: stima mia; ricerca/26 §10.2 lo lasciava fuori] |

### 4.4 Servizi self-hosted da aggiungere al board (con il sì di Michele)

MariaDB (per BookStack), Vexa in `meet-01`, il servizio di trascrizione nell'LXC GPU, Asterisk in `voce-01`, Pipecat in `andrea-01`, Postiz, listmonk, DocuSeal, lo strumento di fatturazione (se Sirius non lo è già), le tre VM `agenti-01`, `cancello-01`, `mcp-01`, il pilota Buzz in LAB. Ognuno entra nel perimetro Cyber Essentials: patch critiche entro 14 giorni, account non amministratori, software supportato [verificato: board, nota su Experimental; ricerca/25 N14].

### 4.5 Necessità esterne, con il costo

| Necessità | Per quale voce | Costo | Fonte |
|---|---|---|---|
| Operatore telefonico italiano (Messagenet SmartNumber PRO, 2 canali) | G5, K10 | 30,00 € al mese; a consumo 44-90 € al mese tutto compreso per 1.000 minuti | [verificato: messagenet.com, ricerca/31 §4 e ricerca/33 §2.3] |
| Relay SMTP per la newsletter (per esempio Amazon SES) | K9, L10 | 0,10 $ ogni 1.000 mail (circa 0,36 € al mese per 4.000 mail) | [verificato: aws.amazon.com/ses/pricing, 25/10/2026]; volume [non verificato] |
| WhatsApp Cloud API, numero dedicato e verifica Meta Business | J9, L5, L8, K5 | 1.000 messaggi di servizio gratis al mese per numero dal 01/10/2026; circa 7-12 € per 300 messaggi utility | [verificato: ricerca/28 §6.2]; stima [non verificato] |
| Telegram Bot API | J9 | 0 € | [verificato: ricerca/28 §6.1] |
| Slack (Free o Pro per 4 persone) | J9, B1 con clienti che usano Slack | 0 € o 27,00 € al mese | [verificato: ricerca/22 §9] |
| VPS per Pangolin e NetBird, se non si aprono porte | accesso pubblico di bot, webhook, MCP RAG, firme | da 5,99 € al mese | [verificato: hetzner.com/cloud, 25/10/2026] |
| Strumenti commerciali fuori dal board | D2, D4, J7, L8 | Apollo 43,78, Metricool 59,86 (sostituibile con Postiz), moda.app 26,80, Higgsfield 41,99, Apify 15,19 (sostituibile con Firecrawl): fino a 187,62 € al mese; Perplexity costo non trovato | [verificato: ricerca/33 §2.5, prezzi in parte non verificati in ricerca/14] |
| Prova di Grok Bot su soli dati pubblici | confronto di strumenti | circa 54 € una volta | [verificato: PRESENTAZIONE-CEO §14, decisione 17] |
| Firma qualificata, se il legale la chiede per certi contratti | L1 | da preventivare | [non verificato] |

---

## 5. Come lavorano insieme gli agenti

### 5.1 Un lavoro dall'inizio alla fine

1. **Ingresso.** Un lavoro nasce in tre modi: n8n a orario o su webhook firmato; una persona che scrive a un agente in Teams; un agente che passa un compito a un altro nella bacheca [non verificato: proposta su ricerca/26 §8].
2. **Coda.** Il lavoro entra nella tabella dei lavori in PostgreSQL con profilo, persona per cui si lavora, tetto in dollari e scadenza [non verificato: proposta].
3. **Sessione.** Il runner prende il lavoro e avvia un processo dell'SDK con il profilo: `CLAUDE.md` della squadra, skill ammesse, elenco chiuso di strumenti MCP, chiave LiteLLM dell'agente, `maxTurns` e `maxBudgetUsd`. Con `settingSources: []`, `CLAUDE_CONFIG_DIR` e `cwd` per famiglia un agente non legge le impostazioni di un altro [verificato: ricerca/26 §3.4].
4. **Contesto.** Prima di agire l'agente legge la pagina "Come lavoro" della persona in BookStack (per ID), i dati fissi dal MCP memoria e i passaggi utili dall'MCP RAG con i permessi della persona [verificato: ricerca/29 §2 e §7, proposta di quel rapporto].
5. **Testo di terzi.** Mail, trascrizioni, pagine web e messaggi dei clienti li legge una sessione senza strumenti d'azione, che restituisce solo campi a schema [verificato: ricerca/22 §2; ricerca/26 §2 per l'output a schema].
6. **Effetto.** Se serve far uscire qualcosa, l'agente chiama `propose_action(classe, destinazione, testo, motivo)`. L'hook del plugin chiede al Cancello: consenti (scrittura interna secondo regole), nega, oppure rimanda. Con "rimanda" il turno finisce con `tool_deferred`, il processo esce e la carta va in Teams [verificato: ricerca/26 §2, fonti D8-D9]. `defer` vale solo con una chiamata di strumento per turno: il plugin nega le chiamate parallele insieme a `propose_action` [verificato: ricerca/26 §2; regola di negazione: non verificato, proposta].
7. **Approvazione.** La persona preme "Approva" sul telefono. La Porta riceve l'azione con l'identità Entra (`aadObjectId`), il Cancello controlla che sia fra gli approvatori della classe, l'esecutore agisce una volta sola, la carta si aggiorna con nome e ora [verificato in parte: ricerca/28 §2.3, `aadObjectId` da confermare nello spike].
8. **Ripresa.** Il runner riprende la sessione dal `SessionStore` con l'esito, e l'agente chiude il lavoro o passa il compito [verificato: ricerca/26 §2].
9. **Conto.** LiteLLM conta e blocca oltre il budget; la stima dell'SDK va nel cruscotto e si confronta ogni mese con la Console [verificato: ricerca/26 §4.3 e §2, "Costi"].

**Due classi di lavoro.** Riassunti, estrazioni e classificazioni sono chiamate dirette ai modelli via LiteLLM, da n8n o dal runner, senza sessione. I lavori a più passi (recap, brief, offerte, deck, debrief) sono sessioni dell'SDK. `claude -p` serve per i lavori singoli lanciati dai runner GitHub [verificato: ricerca/22 §2; ricerca/26 §6].

### 5.2 Profili, famiglie e organigramma

Ogni agente è una riga del registro: nome, squadra, responsabile umano, modello, effort, prompt, skill, MCP ammessi, chiave LiteLLM, orari, tetti [verificato: ricerca/26 §10.2, pezzo 2]. I 57 profili girano in 9 container di famiglia, uno per squadra. Ogni famiglia ha la sua app Entra, il suo ruolo BookStack e PostgreSQL, il suo token MCP e il suo team in LiteLLM [non verificato: proposta].

| Squadra (agenti) | Responsabile | Modello prevalente | Strumenti principali | Chi approva le carte |
|---|---|---|---|---|
| Outbound (5) | Alessandro | Sonnet; Haiku per smistare | MCP SersanOutreach, mcp-enrich, Firecrawl, MCP RAG | Alessandro |
| Chiamate (5) | Alessandro | Sonnet | trascrizioni, calendario in lettura, MCP memoria | Alessandro |
| Vendite (8) | Alessandro | Sonnet; Opus per le offerte | MCP RAG, catalogo, SersanOutreach, SharePoint in lettura | Alessandro; Michele per offerte e affermazioni tecniche |
| Marketing (8) | Alberto | Sonnet; Haiku per le metriche | Firecrawl, Postiz, listmonk, BookStack | Alberto; il founder per i suoi post |
| Studio contenuti (4) | Alberto | Sonnet | template SerSan, skill per slide e documenti | Alberto |
| Progetti (8) | Michele, con Mattia | Sonnet | Jira, SharePoint, MCP RAG | Michele |
| Memoria (5) | Michele | Haiku e lavori deterministici | pipeline, OBSRV in lettura, NetBox | Michele |
| Direzione (10) | Alessandro e Michele | Sonnet; Opus per mappa dei processi | MCP memoria, Grafana, LiteLLM in lettura, posta in lettura | i CEO |
| Amministrazione (4) | Alessandro e Michele | Sonnet | Postgres finanza, MCP RAG `finanza`, fatturazione, DocuSeal | Alessandro o Michele |

Responsabili e approvatori per outbound, offerte e codice [verificato: PRESENTAZIONE-CEO §4.12; ricerca/22 §3]; il resto [non verificato: proposta]. Prezzi dei modelli al 25/10/2026 per milione di token: Opus 5.5 4 $ e 20 $, Sonnet 5.5 2 $ e 10 $, Haiku 5.5 da 0,10 $ e 0,50 $ [verificato: ricerca/26 §2].

**Classi d'azione nel Cancello** [verificato: PRESENTAZIONE-CEO §5.4 per le classi; approvatori per classe da ricerca/22 §3; il resto non verificato: proposta]:

| Classe | Esempi | Come passa |
|---|---|---|
| Lettura | cercare, leggere | consentita agli strumenti ammessi |
| Scrittura interna | to-do in Jira, meeting nel CRM, evento del debrief in Outlook | regola scritta, senza carta, a nome del responsabile; registro |
| Invio a cliente o prospect | follow-up, risposta, recap nel canale condiviso, WhatsApp | carta ad Alessandro; solo al dominio del cliente |
| Pubblicazione | post, newsletter, risposte ai commenti, pagine del sito | carta ad Alberto o al founder del profilo |
| Offerte, contratti, affermazioni tecniche | | carta a Michele |
| Fatture e solleciti | | carta ad Alessandro o Michele; pagamenti mai automatici |
| Codice e infrastruttura | modifiche alle skill, PR, patch | carta ad Alberto; patch del server a Michele |
| Cancellazione e credenziali | | sempre negate agli agenti |

**Regole "Sempre".** Dopo 20 approvazioni uguali senza modifiche, una persona può renderle automatiche per quell'agente, quel tipo di azione e quella destinazione; mai per offerte, primi contatti, pagamenti, cancellazioni [verificato: PRESENTAZIONE-CEO §5.4].

### 5.3 La bacheca e il freno ai giri

- **Bacheca.** Una tabella `compiti` e una `passaggi` in PostgreSQL, con un server MCP: crea, prendi, aggiorna, passa, chiudi, stato [verificato: ricerca/26 §8, proposta di quel rapporto].
- **Freno.** Al massimo 3 passaggi per catena, 8 messaggi per thread, un tetto in dollari per catena; oltre, la catena si ferma e arriva una carta a una persona [verificato: ricerca/22 §3 per i numeri].
- **Visibile a tutti (A7).** Ogni passaggio è rispecchiato nel canale Teams "Agenti" con il nome dell'agente in testa. Le persone intervengono con una @menzione [verificato: ricerca/28 §8.2, proposta di quel rapporto].
- **To-do delle persone.** I compiti per le persone vanno in Jira; un agente chiude da solo solo i compiti fra agenti, per quelli delle persone chiede il sì [verificato: ricerca/29 §4.2, proposta di quel rapporto].

### 5.4 La memoria: cosa legge un agente

| Casa | Cosa contiene | Come la legge l'agente | Fonte |
|---|---|---|---|
| BookStack | regole "Come lavoro", processi, catalogo, manuale | MCP BookStack in sola lettura | [verificato: ricerca/29 §2-3] |
| PostgreSQL `memoria` | persone, regole strutturate, registro degli agenti, obiettivi, catalogo con prezzi, meeting, decisioni, passaggi | MCP memoria, solo lettura | [verificato: ricerca/29 §6.1 e §7.1] |
| Qdrant con MCP RAG | trascrizioni, mail, documenti, Sirius, bandi, pagine BookStack, issue Jira | MCP RAG con i permessi della persona | [verificato: board; ricerca/29 §8.6] |
| Jira | to-do e progetti | MCP Jira | [verificato: ricerca/29 §4] |
| M365 | documenti, posta, calendario | MCP posta e calendario in lettura, solo per ID e sulle caselle in ambito | [verificato: ricerca/29 §5] |
| mcp-memory | appunti di lavoro del singolo agente | taccuino per famiglia, mai dati dei clienti | [verificato: ricerca/29 §7.1] |

**I numeri si calcolano, non si cercano.** Debrief e controllo di gestione leggono numeri calcolati dal codice su dati strutturati in PostgreSQL, non trovati con il RAG [verificato: ricerca/29 §8.5].

### 5.5 La chat di gruppo

- **Teams è la casa comune.** Un team "SerSan Agent OS" con un canale per squadra, "Approvazioni", "Agenti", "Ingresso", "Call di vendita", "Bandi" e un canale privato per cliente [verificato: ricerca/28 §8.1].
- **Bot.** Si parte con un bot "Agenti SerSan" che firma ogni messaggio con il nome dell'agente, più il Capo di gabinetto. Se le persone vogliono gli agenti come membri distinti, un bot per squadra (9) nella fase D [verificato: ricerca/28 §2.6, stima di quel rapporto].
- **Registrazione del bot.** "Teams-managed" senza sottoscrizione Azure; se dà errori 401, Azure Bot F0 (gratuito, nessuna risorsa che gira) oppure il piano B: carte su una pagina del Cancello dietro Pangolin con SSO Entra e avvisi in Teams [verificato: ricerca/28 §2.2].
- **Telegram** solo per avvisi senza contenuto, in long polling: nessuna porta aperta [verificato: ricerca/28 §6.1].
- **WhatsApp** soprattutto verso i clienti, sempre dal Cancello, con la Cloud API ufficiale [verificato: ricerca/28 §6.2].
- **Slack** con l'adattatore Slack dello stesso Chat SDK, che ha adattatori per Slack, Teams, Google Chat, Discord, Telegram, GitHub, Linear e WhatsApp, licenza MIT [verificato: github.com/vercel/chat, 25/10/2026]. Serve se Michele ammette Slack come eccezione, per esempio per i clienti che lavorano in Slack.
- **Buzz** come pilota della "stanza degli agenti" in LAB, via `claude-agent-acp`; la issue #7375 fa ancora perdere risposte senza errore [verificato: ricerca/26 §7.3].
- **Claude Tag in Teams** è solo in lista d'attesa [verificato: ricerca/28 §2.5].

### 5.6 Il percorso di un cliente sul motore

| Passo (PRESENTAZIONE-CEO §4.10) | Cosa succede nel motore |
|---|---|
| 1. La Sentinella trova un'azienda; l'Agente email prepara il primo messaggio | lavoro notturno da n8n; bozza in SersanOutreach via MCP; carta ad Alessandro |
| 2. Il prospect risponde; agenda, brief, concorrenza, slide | webhook di Instantly → SersanOutreach → n8n mette in coda; l'Agente email passa il compito al Brief nella bacheca; l'Agenda propone orari, l'invito parte dopo la carta |
| 3. La call | Teams nativo se è nostra; Vexa se è del cliente |
| 4. Dopo la call | "trascrizione pronta" → n8n → sessione post-call senza strumenti; recap nel canale interno; carte per mail e CRM; Proposte su Opus; task in Jira |
| 5. Marketing | obiezioni passate all'Editoriale nella bacheca; bozze via Postiz dopo la carta |
| 6. Firma e progetto | Contratti con DocuSeal dopo la carta di Michele; Project manager apre il progetto Jira |
| 7. Fatture e caso studio | Fatture e incassi, Casi studio, Rinnovi, Clienti simili; il giro riparte |

[non verificato: proposta costruita sui componenti dei §3-4]

---

## 6. Copertura voce per voce

"Cosa serve ancora" dice cosa manca oggi per avere la voce intera. Le fasi sono quelle del §7.

| Voce | Come la realizza la proposta 1 | Cosa serve ancora | Fase |
|---|---|---|---|
| J1 Un solo sistema multi-agente | un motore, una bacheca, una memoria, un Cancello, Teams | niente oltre al piano | B-F |
| J2 Squadre con compito e responsabile | registro dei profili con responsabile; un team LiteLLM per squadra | niente | B |
| J3 Outreach con agente email | Agente email su SersanOutreach via MCP e Instantly | email live: decisione di compliance D0 ancora aperta [verificato: ricerca/01 riga 17] | C |
| J4 Email → proposte → chiamate | bacheca e passaggi, visibili nel canale "Agenti" | niente | C |
| J5 Agente in ogni chiamata | trascrizione nativa di Teams per le nostre; Vexa per quelle dei clienti; telefono per le riunioni dal vivo | il bot entra solo se il cliente lo ammette (Teams "Unverified", Meet, Zoom OBF); riserva con registrazione sul PC [verificato: ricerca/30 "In breve"] | B (Teams), C |
| J6 Brief prima e dopo, slide per noi e per il cliente | Agente brief e Agente slide con template SerSan | niente; moda.app solo se ammesso (26,80 € al mese) | C |
| J7 Marketing con outreach e studio | squadre Marketing e Studio; Firecrawl; Postiz; HyperFrames in locale | Higgsfield in cloud: eccezione, 41,99 € al mese [non verificato: prezzo] | B-D |
| J8 Squadra progetti | Jira, Project manager, Agente task, Report, Onboarding, Sviluppatori | Jira Standard se servono permessi diversi (28,27 € al mese) | B, D |
| J9 Chat di gruppo come Buzz, con Slack, Telegram, WhatsApp | Teams con la Porta; Telegram, WhatsApp e Slack dallo stesso codice; Buzz in LAB | sì di Michele a Telegram, WhatsApp e Slack; verifica Meta Business; Slack 0-27 € al mese | B, D, E, F |
| A1 Tutte le riunioni registrate e trascritte | Teams via Graph, Vexa, telefono, trascrizione in casa, avviso in tre livelli | parere sull'art. 4 dello Statuto se ci sono dipendenti; DPIA [verificato: ricerca/30 §8] | B-C |
| A2 Memoria relazionale | BookStack per i testi, PostgreSQL per i dati, MCP memoria | MariaDB da aggiungere al board | B |
| A3 Memoria vettoriale | Qdrant con BM25 e reranker, MCP RAG, ingressi estesi | pipeline del board in F4 | C |
| A4 Orchestratore sul server | motore sull'Agent SDK in `agenti-01` | VLAN e RAM da confermare con Michele | A-B |
| A5 Agenti per ruolo | squadra Memoria più pipeline del board; squadre d'azione | niente | C |
| A6 Agenti che imparano | skill in git; un revisore settimanale propone modifiche come PR; una persona approva | niente | D |
| A7 Chat condivisa fra agenti | bacheca rispecchiata nel canale "Agenti"; intervento con @menzione | niente | C-D |
| B1 Punti nel canale del cliente | canale privato Teams subito; condiviso col cliente dopo la carta, o mail | canali condivisi con altre organizzazioni da provare [non verificato: ricerca/28 §2.5] | B, C |
| B2 Opportunità nel CRM | operazioni di SersanOutreach via Cancello; nuova operazione "crea deal" | MCP su HTTP con token (oggi solo stdio) [verificato: ricerca/01 riga 315] | B |
| B3 Mail di follow-up | bozza, carta, esecutore Outlook via Graph, solo al dominio del cliente | permesso di invio limitato con RBAC di Exchange | B |
| B4 To-do al team | Jira, scrittura interna del Cancello | niente | B |
| B5 Autonomia crescente | regole "Sempre" dopo 20 approvazioni | niente | D-F |
| C1 Debrief del mattino | n8n alle 7:00, chat 1:1 di Teams e mail, numeri da PostgreSQL | niente | B |
| C2 Agente anche al posto di chi manca | `recordAutomatically` sulle nostre riunioni; Vexa per le altre | provare se Teams registra senza nessuno di SerSan collegato [verificato: ricerca/30 §3.6] | C |
| C3 Analisi della call con Claude | sessione post-call senza strumenti, output a schema | niente | B |
| C4 Dettatura | dettatura delle app Claude; note vocali dal telefono trascritte in casa | niente | B, C |
| C5 Registro dei meeting e pipeline | tabella `meetings`, vista in Grafana | niente | B |
| C6 Regole di ciascuno lette prima di ogni lavoro | pagina BookStack "Come lavoro" letta per ID; `CLAUDE.md` della squadra | niente | B |
| D1 Pipeline pesata | probabilità per stadio dagli eventi di SersanOutreach, con intervallo | storico: oggi 0 vinti e 91 deal senza valore; pesi dichiarati fino a 30-50 chiusure [verificato: PRESENTAZIONE-CEO, appendice A] | E |
| D2 Brief dall'email della persona | SersanOutreach, mcp-enrich, Firecrawl, MCP RAG, posta | aperture delle mail solo con l'email live; Apollo e Perplexity come eccezioni (43,78 € al mese più Perplexity) | C |
| D3 Storico della relazione | MCP RAG con filtro cliente, tabella `meetings` | niente | C |
| D4 Slide automatiche | Agente slide con skill e template SerSan | moda.app solo se ammesso | C |
| D5 Offerta dal catalogo | Agente proposte su Opus, catalogo in BookStack e PostgreSQL, carta a Michele | niente | C |
| E1 Tempo per imparare | piano del §7 con riserva | niente | tutte |
| E2 Costruire ora | prezzi del §8 al 25/10/2026 | niente | tutte |
| E3 Banca dei token | LiteLLM per agente, squadra e persona; avviso all'80 % dal Cancello, stop al 100 % da LiteLLM | LiteLLM anticipato rispetto a F4 | B, D |
| E4 Formazione | un'ora documentata per i quattro (AI Act art. 4) | niente | A |
| F1 Metadati del lavoro | report e log di M365, aggregati, al massimo 21 giorni | quali API di M365 usare [non verificato: ricerca/29 §5.2] | D |
| F2 Interviste guidate | Intervistatore in chat 1:1 di Teams | niente | D |
| F3 Mappa dei processi | Mappatore, libro "Processi" in BookStack | niente | D |
| F4 Ore implicite e automazioni | analista mensile su Opus, ore in PostgreSQL | niente | D |
| F5 AI per tutti | Teams, Claude Team, Open WebUI con budget per persona | niente | A-B |
| G1 Call di vendita in un canale | canale Teams "Call di vendita" dal post-call | niente | C |
| G2 Fit score | qualificatore di SersanOutreach esteso alle call | volumi di call | E |
| G3 Valutazione della call | Coach vendite, nessuna stima delle emozioni (AI Act art. 5(1)(f)) | parere legale | E |
| G4 Report a chi ha fatto la call | chat 1:1 di Teams; al responsabile solo aggregati in Grafana | parere legale per andare oltre gli aggregati | E |
| G5 Andrea in 90 secondi, 24/7 | Asterisk, Pipecat, Haiku 5.5 col pensiero spento, ascolto e voce in casa; modulo del sito via n8n | operatore telefonico (eccezione); voce italiana da provare; parere legale; seconda GPU consigliata | E |
| G6 Impara dai rifiuti | analisi settimanale, nuove aperture via Cancello, test A/B | volumi | E |
| G7 Più conversione | tempo di richiamata e meeting nel debrief | niente | E |
| G8 Vinti e persi al marketing | Analista vinto/perso → Editoriale nella bacheca | chiusure: oggi 0 [verificato: ricerca/01] | C |
| G9 Agenti in organigramma fino a cento | registro dei profili, Grafana, pagina BookStack | RAM in più oltre le 16 sessioni insieme | B-F |
| G10 Superpotere | il risultato dell'insieme | niente | tutte |
| H1 Formarsi e sperimentare | due ore a settimana; Experimental-2 come sandbox; Open WebUI | niente | A-F |
| H2 Non delegabile | i CEO approvano dal telefono e leggono il debrief | niente | B |
| H3 Assessment | Intervistatore per ruolo | niente | D |
| H4 Ambassador | Mattia, con un tetto più alto in LiteLLM | niente | D |
| H5 Tutti costruiscono | ognuno possiede almeno un profilo nel registro | niente | D |
| H6 Premio mensile | classifica in Grafana dal registro | 50-100 € al mese [verificato: PRESENTAZIONE-CEO §14] | D |
| H7 Cambiare modo di lavorare | rituali di adozione (PRESENTAZIONE-CEO §10) | niente | tutte |
| I1 Il contesto fa la qualità | quattro case e una porta di ricerca | niente | B-C |
| I2 Oltre la versione base | skill, MCP e profili su misura | niente | B-F |
| I3 Aree dove l'AI non entra | classi negate nel Cancello; regole deny valide anche in `bypassPermissions` [verificato: ricerca/26 §2] | niente | B |
| I4 Marketing più creativo | Editoriale, Copywriter, Metriche, Pubblicatore | niente | B |
| K1 Debrief come primo appuntamento | evento Outlook creato dall'esecutore | niente | B |
| K2 "Ho trovato tre nuove call" | annuncio nella bacheca e nel canale "Agenti"; l'Agenda manda gli inviti dopo il sì | niente | C |
| K3 Posta smistata con risposte pronte | Smistatore su Graph con caselle limitate; invio dal Cancello | accordo di ciascuno sulla propria casella | C |
| K4 Chiedere cosa si è detto in una call | Claude Team con l'MCP RAG; Capo di gabinetto in Teams | regola sui dati rossi verso Claude Team (§9) | C |
| K5 Brief di intake e onboarding | Agente intake da modulo, posta, WhatsApp | niente | C |
| K6 Slide per il cliente con la storia della relazione | Brief, Slide, MCP RAG | niente | C |
| K7 Il nostro stile | template SerSan in SharePoint, skill di brand | template da preparare | C |
| K8 Portale clienti con Claude Code | SersanOutreach come portale, cruscotto della pipeline | niente | E |
| K9 Newsletter | Agente newsletter e listmonk | relay SMTP esterno (Exchange Online non è per l'invio in massa) | D |
| K10 Andrea anche in entrata | gruppo di squillo in Asterisk, poi Andrea; esito nel CRM e nel canale vendite | come G5 | E |
| K11 Perché si chiude e cercarne simili | Analista vinto/perso e Agente clienti simili | volumi | C, E |
| K12 Formazione continua dei commerciali | piano mensile del Coach | niente | E |
| K13 Mappa e assessment per i clienti | Mappatore e Intervistatore in un'istanza separata per cliente | istanza e dati separati da progettare [non verificato] | D-F |
| K14 Finanza e obiettivi nella memoria | tabella `obiettivi`; numeri di Sirius in PostgreSQL via n8n; documenti nel RAG | sapere cos'è Sirius [verificato: ricerca/29 §8] | C-F |
| K15 Acquisti automatizzati | Agente acquisti: fatture dei fornitori dalla posta, rinnovi; pagamenti sempre su carta | strumento di fatturazione | F |
| K16 Assistente personale | profilo privato per chi lo vuole, senza accesso alla memoria aziendale; i dati di salute restano nel suo account privato | consenso della persona | F |
| L1 Contratto con firma elettronica | Agente contratti e DocuSeal sul server | valore legale della firma semplice per UK e Italia nel parere; firma qualificata da fornitore esterno se serve | F |
| L2 Fatture, incassi, solleciti | Agente fatture; Sirius se è il gestionale, altrimenti Invoice Ninja | chi fattura e con quale sistema (UK, o SDI se c'è un soggetto italiano) [non verificato] | F |
| L3 Margini, cassa, obiettivi | Controllo di gestione su PostgreSQL e Grafana | dati strutturati di Sirius | F |
| L4 Bandi e finanziamenti | pipeline notturna del board più Agente bandi | niente | C |
| L5 Assistenza nella stanza del cliente | canale condiviso Teams, mail o WhatsApp; risposte su carta | come B1 e J9 | F |
| L6 Rinnovi e clienti a rischio | Agente rinnovi su call, report e Jira | niente | F |
| L7 Caso studio | Agente casi studio; testimonianza chiesta dopo la carta | niente | F |
| L8 Commenti e messaggi della pagina | Community manager con Postiz | accesso API alla pagina LinkedIn da verificare; Metricool come eccezione | D |
| L9 Sito, articoli e SEO | Agente sito con PR su GitHub; deploy su Vercel fatto da una persona | niente | F |
| L10 Webinar ed eventi | Agente eventi; webinar di Teams; inviti con listmonk; lead in SersanOutreach | licenza dei webinar di Teams da controllare [non verificato] | F |
| L11 Agente che sorveglia il server | Sistemista in sola lettura su Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox; patch come carte | stack OBSRV della fase F3 | C |
| L12 Allenatore | Allenatore AI dal registro d'uso, visibile solo all'interessato | niente | F |

### 6.1 Le lacune, e come si chiudono

| Lacuna | Cosa la chiude | Costo o lavoro |
|---|---|---|
| Nessuno storico di vendita (D1, G2, G6, G8, K11) | pesi dichiarati da Alessandro, poi calcolo vero dopo 30-50 chiusure | tempo, non soldi |
| Bot non ammessi nelle call dei clienti (J5, C2) | Teams nativo per le nostre; chiedere al cliente di ammettere "SerSan Verbale"; registrazione sul PC | 0 € |
| Voce di Andrea su CPU (G5, K10) | prova d'ascolto; seconda GPU da 16 GB; in ultima istanza un TTS in cloud come eccezione | 686-775 € IVA esclusa |
| Operatore telefonico fuori dal board (G5, K10) | aggiungerlo all'elenco dei servizi esterni | 44-90 € al mese |
| Canali esterni (J9) | eccezioni Telegram, WhatsApp, Slack | 0-39 € al mese |
| Newsletter (K9) | relay SMTP esterno | meno di 1 € al mese |
| Dati rossi verso Claude Team (K4, A3) | oscurare i blocchi rossi nell'MCP RAG, oppure darli solo agli agenti via API, dopo il parere | 0 €, lavoro dentro C.1 |
| Sirius sconosciuto (K14, L2, L3) | domanda a Michele | da capire |
| RAM e GPU per lo scenario completo | +192 GB prima della fase C; seconda GPU prima della fase E | §8.4 |
| Esposizione pubblica | VPS o porte verso EDGE | da 5,99 € al mese |
| Firma e fatture (L1, L2) | DocuSeal e strumento di fatturazione; parere legale | dentro il tetto del parere |
| MinIO archiviato dal 12/02/2026 [verificato: ricerca/25 N14] | Michele sceglie un sostituto (Garage o SeaweedFS) prima che ci vadano audio e file degli agenti | lavoro del board |

---

## 7. Piano per fasi

### 7.1 Ipotesi

- **Capacità** [non verificato: da confermare]: Alberto 4,5 gp a settimana, Mattia 1,5, Michele 0,5, cioè 6,5 gp a settimana nelle fasi A-C, mentre Michele porta avanti il board. Dalla fase D Michele dà 1 gp in più: 7,5 a settimana [verificato per i valori di partenza: ricerca/22 §5].
- **Il server non si conta.** Le fasi F0-F3 del board (montaggio, OPNsense e VLAN, Proxmox su ZFS, NetBird e Traefik, PBS, uscita da Azure con la migrazione di SersanOutreach, sicurezza) e la base della F4 (LXC GPU, pipeline Sirius → MCP, Firecrawl con n8n, LiteLLM con budget) sono lavoro di Michele [verificato: board, roadmap].
- **Tempi del board** [non verificato: ipotesi da sostituire con la stima di Michele]: F0-F1 nelle settimane 1-5, F2-F3 nelle settimane 6-14, F4 nelle settimane 15-18.
- **"Posto agenti" anticipato.** Il pilota sul server chiede LiteLLM, PostgreSQL 16, Infisical, n8n, le tre VM e la rotta pubblica del bot già nella fase F2 [verificato: ricerca/25 §6, strada (a)]. Se Michele non lo anticipa, il pilota gira su stage con una chiave diretta e un tetto basso nella Console [verificato: ricerca/26 §10.3].
- **Calendario.** Le settimane sono calcolate sui giorni con la riserva, come faceva la presentazione [verificato: PRESENTAZIONE-CEO §11 e §15].

### 7.2 Le fasi

| Fase | Settimane | Board in corso | Cosa si costruisce | gp base | gp con riserva | Cosa vedete alla fine |
|---|---|---|---|---|---|---|
| **A. Fondamenta del software e valore subito** | 1-5 | F0-F1 | nucleo del motore su sviluppo (runner, registro, ponte); prima parte del Cancello; spike del bot Teams e impostazioni Graph delle trascrizioni; debito di sicurezza di SersanOutreach; skill di marketing su Claude Team con dati verdi; modelli "Come lavoro", registro dei trattamenti, inizio DPIA, formazione | 25 | 33 | un agente di prova che propone una mail e si ferma su una carta premuta dal telefono; SersanOutreach verde su identità e MFA; post della settimana pronti |
| **B. Pilota: post-call, debrief, marketing in Teams** | 6-16 | F2-F3 e "posto agenti" | motore sul server; Cancello v1 con esecutori Outlook, Jira, SersanOutreach, pausa di Instantly; Porta Teams con le carte; trascrizioni Teams via Graph; Jira, BookStack, MCP memoria; SersanOutreach su HTTP; 14 agenti (Post-call, Analista chiamate, Dettatura, Report del mattino, Capo di gabinetto, Agente task, Guardiano, Registro, Banca dei token, Editoriale, Copywriter, Ricerca concorrenza, Analista metriche, Pubblicatore) | 51 | 68 | dopo una call Teams: recap, to-do in Jira, bozza in carta, invio dopo il sì; debrief alle 7:00; numeri del lunedì; organigramma con costi. **Verifica alla settimana 11** (§7.4) |
| **C. Memoria, call e vendite preparate** | 17-27 | F4 | ingressi della pipeline e MCP RAG per persona; Vexa, trascrizione in casa, telefono; bacheca e freno; Cancello v2; 18 agenti (Agente chiamate, Agenda, Brief, Proposte, Slide, Vinto/perso, Intake, Email, LinkedIn, Sentinella, Operatore outbound, Smistatore posta, Raccoglitore, Pulitore, Bibliotecario, Archivista, Sistemista, Bandi) | 55 | 73 | brief la sera prima; offerta in bozza entro un'ora; "cosa ci siamo detti con X?" da Claude Team; bot nelle call dei clienti; bandi ogni mattina; posta smistata |
| **D. Agenti che si parlano e organizzazione** | 28-31 | F4-F5 | specchio della bacheca in Teams e Jira; Telegram; listmonk e Postiz; banca dei token per persona; revisore delle skill; 10 agenti (Project manager, Report cliente, Onboarding, Sviluppatori, Newsletter, Community manager, Video, Grafiche, Mappatore processi, Intervistatore) | 20 | 26 | passaggi fra agenti visibili nel canale "Agenti" con il freno in azione; prima newsletter dopo il sì; mappa dei processi v0; circa 42 agenti accesi |
| **E. Vendite e voce** | 32-38 | F5 | Andrea su CPU, poi sulla seconda GPU; pipeline pesata e portale; WhatsApp per i clienti; 4 agenti (Andrea, Coach vendite, Pipeline, Clienti simili) | 40,5 | 54 | una lead di prova richiamata entro 90 secondi, con appuntamento nel CRM; coaching visibile solo al venditore |
| **F. Le altre automazioni e i canali in più** | 39-43 | F5 | DocuSeal, fatturazione, assistente personale, pilota Buzz in LAB, ponte Slack; 11 agenti (Contratti, Assistenza clienti, Rinnovi, Casi studio, Sito e SEO, Eventi e webinar, Fatture e incassi, Acquisti, Controllo di gestione, Allenatore AI, Assistente personale) | 26,5 | 35 | dal contratto all'incasso senza lavoro a mano; tutti i 57 agenti nel registro |
| **Totale** | **1-43** | | | **218** | **circa 290** | |

Tutte le cifre [non verificato: stime costruite sui rapporti 26-31 e sul §4.3]. Le settimane sono circa 43 perché ora facciamo in casa call, voce, chat e strumenti che prima erano abbonamenti. Se Mattia passa a 2,5 gp a settimana dalla fase B, il calendario scende di circa 5 settimane [non verificato: calcolo].

### 7.3 Dettaglio dei giorni

| Fase | Pezzo | gp base |
|---|---|---|
| A | Motore: runner, registro, ponte verso il Cancello, su sviluppo | 6,5 |
| A | Cancello, prima parte: classi, approvatori, registro a catena, outbox, ESTOP | 8 |
| A | Spike del bot Teams (1); impostazioni Teams e Graph per le trascrizioni (1, Michele) | 2 |
| A | Debito di sicurezza di SersanOutreach (Mattia) | 4 |
| A | Skill di marketing su Claude Team | 2 |
| A | Regole, registro dei trattamenti, DPIA, testi d'avviso, formazione | 2,5 |
| B | Motore: orari con n8n, LiteLLM, isolamento, osservabilità, collaudo, `SessionStore` | 8 |
| B | Cancello, seconda parte: esecutori Outlook, calendario, Jira, SersanOutreach, Instantly | 7 |
| B | Porta Teams con carte e rotta pubblica | 7,5 |
| B | Trascrizioni Teams da Graph e flag "avvisato" dell'Agenda | 4,5 |
| B | Jira (1,75), BookStack per gli agenti (2), MCP memoria (2,5) | 6,25 |
| B | SersanOutreach: MCP su HTTP con token, operazione "crea deal" | 3,5 |
| B | Contenuto di 14 agenti | 14,5 |
| C | Ingressi della pipeline, MCP RAG per persona, permessi Graph, organigramma | 7,25 |
| C | Modulo riunioni: Vexa, trascrizione, lotti, telefono, prove, esercizio | 19,75 |
| C | Bacheca e freno (3), MCP Firecrawl (0,5), Cancello v2 (2,5) | 6 |
| C | Contenuto di 18 agenti | 22 |
| D | Specchio della bacheca, Telegram, listmonk con relay, Postiz | 6,25 |
| D | Contenuto di 10 agenti, banca per persona, revisore delle skill | 13,5 |
| E | Andrea su CPU (24) e seconda GPU (4) | 28 |
| E | Pipeline pesata e portale clienti | 5 |
| E | WhatsApp per i clienti | 4 |
| E | Contenuto di 3 agenti (Coach, Pipeline, Clienti simili) | 3,5 |
| F | DocuSeal, fatturazione, assistente personale, Buzz in LAB, ponte Slack | 13 |
| F | Contenuto di 11 agenti | 13,5 |

[non verificato: stime; fonti dei singoli pezzi nel §4.3]

### 7.4 La verifica della settimana 11

Il motore va avanti se, dopo cinque settimane sul server [verificato: criteri tecnici da ricerca/26 §10.4; il resto non verificato: proposta]:
- tre profili girano una settimana senza sessioni scambiate;
- nessun effetto esce senza una carta del Cancello;
- una carta lasciata ferma una notte riprende la sessione giusta al mattino;
- la spesa resta nel tetto di LiteLLM e la stima dell'SDK differisce dalla Console meno del 10 %;
- un aggiornamento dell'SDK passa i 10 scenari di prova e arriva in produzione entro 14 giorni dall'uscita (Cyber Essentials);
- l'approvazione arriva dal telefono con l'identità Entra giusta.

Criteri commerciali, misurati insieme: follow-up di tutte le call entro 24 ore, carte decise entro 24 ore, post dei founder pubblicati, numeri del lunedì compilati [verificato: PRESENTAZIONE-CEO §11].

Se un criterio tecnico fallisce, si apre la via d'uscita del §10.

### 7.5 Cosa non è contato

Le fasi F0-F5 del board; la migrazione di SersanOutreach dentro "ci → apps → mesh" della F2; la costruzione dell'MCP RAG base e della pipeline Sirius → MCP della F4 (contiamo solo le nostre estensioni); la manutenzione dopo la fase F, stimata in 1-2 gp a settimana [verificato: board; PRESENTAZIONE-CEO §15 per la manutenzione].

---

## 8. Costi

### 8.1 Quanto spendiamo in più rispetto a oggi, fase per fase

Conto come la prima tabella della presentazione: costi nuovi, senza il kit commerciale, con le API dentro i crediti e Claude Team gratuito nel primo anno [verificato: metodo di ricerca/33 §3.1].

| Periodo | € al mese in più | Cosa comprende | Fonte |
|---|---|---|---|
| Fase A, Azure ancora acceso | circa 135 | Proxmox Community 20,00; IP fisso 10,00; corrente del server e del firewall a 400 W 105,27 | [verificato: ricerca/33 §3.1] |
| Fasi B-D, Azure spento in F2 | circa 14-31 | come sopra meno almeno 150 di Azure; più Jira Standard 28,27; VPS 0-6,49; corrente di 12 moduli RAM in più 6,39-10,22 (dalla fase C); relay SMTP circa 0,36 (dalla fase D) | [verificato: ricerca/33 §2.2; ricerca/32 §5.2; hetzner.com]; somma [non verificato] |
| Fase E, con Andrea e WhatsApp | circa 78-151 | più Andrea 44,24-90,43; WhatsApp 7-12; corrente della seconda GPU 6,39-17,89 | [verificato: ricerca/33 §2.3-2.4]; somma [non verificato] |
| Fase F, con Slack se ammesso | circa 78-178 | più Slack 0-27,00 | [verificato: ricerca/22 §9]; somma [non verificato] |
| Fine dell'anno gratuito di Claude Team | + 446,70 (5 premium); + 357,36 con 4 premium | invariato rispetto alle altre proposte | [verificato: ricerca/33 §2.2, claude.com/pricing/team] |
| Senza crediti API | + 195,65 (forbice 90-250) | sessioni e cache, come in ricerca/22 | [non verificato: stima di ricerca/22 §6] |
| Instantly, se oggi non è già pagato | + 69,33 | Hypergrowth annuale | [verificato: ricerca/33 §2.2] |
| Strumenti commerciali fuori dal board, se restano | + 0-187,62 | Apollo, Apify, Metricool, moda.app, Higgsfield | [verificato: ricerca/33 §2.5] |

### 8.2 Listino mensile a regime (fase F)

| Voce | € al mese | Fonte |
|---|---|---|
| Proxmox Community, 2 socket | 20,00 | [verificato: ricerca/33 §2.2, proxmox.com] |
| Jira Standard × 4 | 28,27 | [non verificato: ricerca/29 §4.1] |
| IP fisso | 0-10,00 | [non verificato: ricerca/33 §2.2] |
| VPS per Pangolin e NetBird, se serve | 0-6,49 | [verificato: hetzner.com/cloud] |
| Corrente del server (400 W) e del firewall | 105,27 | [non verificato: stima di ricerca/33 §2.4] |
| Corrente di RAM e seconda GPU | 12,78-28,11 | [non verificato: ricerca/32 §5.2] |
| API Anthropic | 195,65 | [non verificato: stima di ricerca/22 §6] |
| Andrea (operatore, Registro delle opposizioni, modelli) | 44,24-90,43 | [verificato: ricerca/33 §2.3] |
| WhatsApp verso i clienti | 7-12 | [non verificato: ricerca/28 §9] |
| Relay SMTP | circa 0,36 | [verificato: prezzo SES]; volume [non verificato] |
| Slack | 0-27,00 | [verificato: ricerca/22 §9] |
| Instantly | 69,33 | [verificato: ricerca/33 §2.2] |
| **Totale di listino** | **circa 483-593** | [non verificato: somma] |
| Strumenti commerciali fuori dal board, se restano | + 0-187,62 | [verificato: ricerca/33 §2.5] |
| Claude Team a fine bundle | + 446,70 | [verificato: ricerca/33 §2.2] |

Per confronto: lo scenario consigliato della presentazione valeva circa 968 € al mese; ricerca/33 lo porta a 518,95 € dentro il board [verificato: ricerca/33 §3.3]. La differenza con questa tabella sta in VPS, WhatsApp, Slack, relay, corrente di RAM e GPU.

**Motore SDK o Hermes: stesso costo mensile.** Licenza zero in entrambi i casi, si paga solo l'API [verificato: ricerca/33 §2.6].

### 8.3 Licenze dei componenti nuovi

| Componente | Licenza | Costo | Fonte |
|---|---|---|---|
| Agent SDK di Claude | Commercial Terms di Anthropic | 0 €, si paga l'API | [verificato: ricerca/26 §1.1] |
| Chat SDK (`chat`) | MIT | 0 € | [verificato: github.com/vercel/chat] |
| Postiz | AGPL-3.0 | 0 € self-hosted | [verificato: github.com/gitroomhq/postiz-app] |
| listmonk | AGPL-3.0 | 0 €; ultima stabile v6.2.0 del 26/06/2026, v7.0.0-beta.1 del 20/10/2026 | [verificato: API GitHub di knadh/listmonk, 25/10/2026] |
| DocuSeal | AGPLv3 con termini aggiuntivi | 0 € nella versione open source | [verificato: github.com/docusealco/docuseal] |
| Invoice Ninja | Elastic License 2.0 | 0 €; marchio rimosso a circa 40 $ l'anno | [non verificato: fonti terze] |
| Vexa | Apache-2.0 | 0 € | [verificato: ricerca/30 §4.1] |
| Pipecat | BSD-2 | 0 € | [verificato: ricerca/31 "Fatti"] |
| Asterisk 22 LTS | GPLv2 | 0 € | [non verificato] |
| Server MCP di Firecrawl | MIT, accetta un Firecrawl self-hosted con `FIRECRAWL_API_URL` | 0 € | [verificato: github.com/firecrawl/firecrawl-mcp-server, 25/10/2026] |

### 8.4 Una tantum

**Della proposta 1**

| Voce | Quando | € IVA esclusa | Fonte |
|---|---|---|---|
| Parere legale unico (call, Andrea, coaching, dati rossi verso Claude Team, firma, Statuto art. 4) | fase A | tetto 2.500 | [verificato: PRESENTAZIONE-CEO §14, decisione 10] |
| Credito API prepagato, se i crediti del bundle finiscono | fase A | 0-223 | [verificato: ricerca/33 §4.1] |
| RAM +192 GB (12 × 16 GB) | prima della fase C | 816-1.218 | [verificato: ricerca/32 §2.4] |
| Staffa ad altezza piena o riser per la seconda GPU | con la GPU | 8-90 (10-110 IVA inclusa) | [verificato: ricerca/32 §8] |
| Vivavoce da sala per le riunioni dal vivo | fase C | 100-250 | [non verificato: ricerca/30 §11.3] |
| Attivazione del numero di Andrea | fase E | 7-14 | [verificato: ricerca/33 §4.1] |
| **Totale della proposta** | | **3.431-4.295** | [non verificato: somma] |
| di cui chiesto subito | fase A | 2.500-2.723 | |

**Spese del board che la proposta usa** (non contate due volte, le scrivo perché i CEO le vedono insieme)

| Voce | Quando | € | Fonte |
|---|---|---|---|
| Seconda GPU RTX 2000 Ada 16 GB: il board la mette in F5, la proposta consiglia di anticiparla prima della fase E | F5 o prima | 686-775 IVA esclusa | [verificato: ricerca/32 §4.3; ricerca/33 §4.2] |
| PBS a casa (M920t, 2 dischi, 2 SSD per i metadati) | F1 | 640-1.180 IVA inclusa | [verificato: ricerca/32 §7] |
| Chiavi FIDO2, 2 a persona | F1 | 232-464 | [verificato: ricerca/33 §4.1] |
| Piccoli accessori | F0-F1 | 0-200 | [non verificato: ricerca/33 §4.1] |
| UPS rack 2U (Eaton 5PX 1500 G2 consigliato) | F5 | 937-1.144 | [verificato: ricerca/32 §6] |

**Chiesto oggi, proposta più board:** circa 3.257-4.354 € (parere legale, credito API, PBS a 525-967 € IVA esclusa, chiavi FIDO2, accessori) [non verificato: somma].

---

## 9. Rischi e mitigazioni

| Rischio | Mitigazione | Fonte |
|---|---|---|
| L'SDK esce quasi ogni giorno e cambia comportamenti (per esempio dalla 2.1.302 un'app senza modalità esplicita nega tutto) | versione fissata (oggi TS 0.3.310 con Claude Code 2.1.310); aggiornamento ogni due settimane dopo i 10 scenari; rientra nei 14 giorni di Cyber Essentials | [verificato: ricerca/26 §1.1 e §11] |
| LiteLLM non inoltra `anthropic-beta` (PR #36736 aperta) | test di accettazione a ogni aggiornamento; riserva: chiave diretta per famiglia con limiti nella Console | [verificato: ricerca/26 §4.2] |
| Il bot Teams-managed dà 401 | spike nella fase A; Azure Bot F0 come registro gratuito; piano B con la pagina del Cancello | [verificato: ricerca/28 §2.2] |
| Microsoft cambia la piattaforma (SDK archiviato, connettori spenti) | Chat SDK: cambiare canale vuol dire cambiare adattatore; Mattermost come piano B | [verificato: ricerca/28 §10] |
| Iniezioni da mail, trascrizioni, pagine e messaggi | nessuno strumento che invia; `dontAsk` con elenco chiuso; testo di terzi letto da sessioni senza strumenti; uscita su allowlist | [verificato: ricerca/26 §11] |
| Dati rossi verso Claude Team, che non ha la conservazione zero | filtro per colore nell'MCP RAG; decisione prima della fase C; richiesta di ZDR per l'API | [verificato: ricerca/25 N17; ricerca/29 §8.5] |
| RAM finita con tutte le funzioni | +192 GB prima della fase C; tetto alle sessioni; Experimental a richiesta | [verificato: ricerca/32 §3.4] |
| GPU piena di giorno e assente la sera | fasce orarie; CPU per embedding e lotti; seconda GPU da 16 GB | [verificato: ricerca/30 §6.2] |
| Più componenti da aggiornare entro 14 giorni (SDK, LiteLLM, Vexa, Postiz, listmonk, DocuSeal) | inventario in NetBox; finestra di aggiornamento ogni due settimane; il Sistemista apre le carte delle patch | [verificato: board per NetBox e regola dei 14 giorni]; metodo [non verificato] |
| Piattaforme di call che chiudono ai bot | Teams nativo per le nostre; riserva con registrazione sul PC | [verificato: ricerca/30 §12] |
| Voce italiana di Andrea o latenza non buone | prova d'ascolto prima; Haiku 4.5 come riserva (0,48 s al primo token); seconda GPU | [verificato: ricerca/31 §13] |
| Esposizione pubblica senza porte aperte | VPS o porte solo verso EDGE; verifica dei token firmati; CrowdSec | [verificato: ricerca/25 N10; ricerca/28 §10] |
| Codice nostro conosciuto da poche persone | Mattia lavora sul codice dal primo giorno; runbook; revisioni incrociate; TypeScript da confermare con Mattia | [verificato: ricerca/26 §11-12] |
| Giri fra agenti e spesa che scappa | freno nella bacheca; tetti in LiteLLM; `maxBudgetUsd`; ESTOP dal telefono | [verificato: ricerca/26 §4.3] |
| Calendario lungo (43 settimane) con tre persone a tempo parziale | valore per gradi (pilota alla fase B); priorità decise dai CEO a ogni fase | [non verificato: proposta] |
| Tempi del board non noti | "posto agenti" anticipato; pilota su stage con chiave limitata | [verificato: ricerca/26 §10.3] |
| Anthropic cambia termini o prezzi | chiave API; versioni fissate; memoria, bacheca e registro restano nostri | [verificato: ricerca/26 §11] |

---

## 10. Come si esce se qualcosa non regge

Ogni pezzo sta dietro un'interfaccia nostra: il motore parla con gli strumenti solo via MCP, con i modelli solo via LiteLLM, con l'esterno solo via Cancello. Cambiare un pezzo non tocca gli altri [non verificato: principio di progetto].

| Se non regge | Via d'uscita | Costo | Fonte |
|---|---|---|---|
| Il motore sull'SDK (verifica della settimana 11) | Hermes self-hosted, prima in Experimental-2 con 2-3 profili, poi al posto del runner; restano Cancello (via MCP `propose_action`), LiteLLM, server MCP, Porta e memoria; le skill hanno lo stesso formato | pilota 6-8 gp; integrazione 26-33 gp con la riserva | [verificato: ricerca/27 "In breve"; ricerca/22 §8 per il formato delle skill] |
| LiteLLM | chiave diretta per famiglia con limiti nella Console; i tetti del runner (`maxBudgetUsd`) restano | 0 € | [verificato: ricerca/26 §11] |
| Il bot Teams | Azure Bot F0; pagina del Cancello con avvisi via webhook di Workflows; Mattermost | 0 € o circa 35,74 € al mese per Mattermost Professional | [verificato: ricerca/28 §2.2, §4, §9] |
| Vexa | Attendee come piano B (con il limite sui tenant con MFA spenta); registrazione sul PC con Meetily | 2-3 gp di prova | [verificato: ricerca/30 §4.3 e §11.1] |
| La voce di Andrea in casa | voci sulla seconda GPU; in ultima istanza un servizio di voce in cloud, come eccezione | circa 88 € al mese per ElevenLabs Pro | [verificato: ricerca/31 §13; PRESENTAZIONE-CEO §12.1] |
| L'MCP di BookStack della comunità | MCP nostro con 6-8 strumenti | 1,5-2 gp | [verificato: ricerca/29 §3.2] |
| Postiz | Metricool come eccezione | 59,86 € al mese | [verificato: ricerca/33 §2.5] |
| DocuSeal | firma da un fornitore esterno, come eccezione | da preventivare | [non verificato] |
| Jira Free | Jira Standard | 28,27 € al mese | [non verificato: ricerca/29 §4.3] |
| Anthropic | chiamate semplici con la Messages API; Claude su Bedrock UE solo con il sì di Michele e se un cliente lo chiede | da preventivare | [verificato: ricerca/25 C24] |
| Tutto il sistema | ESTOP dal telefono: si ferma la coda, i budget di LiteLLM vanno a zero, SersanOutreach si ferma con il kill switch e la pausa di Instantly; il lavoro torna a mano, i dati restano in PostgreSQL, BookStack, Jira e M365 | 0 € | [verificato: ricerca/01 riga 288 per il kill switch] |

---

## 11. Domande aperte

**Per Michele**
1. Anticipi il "posto agenti" (LiteLLM, PostgreSQL 16, Infisical, n8n, le tre VM, la rotta pubblica del bot) alla fase F2?
2. Il motore va in una VLAN 32 AGENTI nuova, o nella 30 con il firewall di Proxmox per VM?
3. Pangolin e NetBird: VPS (da 5,99 € al mese) o IP fisso con porte verso EDGE?
4. Se il bot Teams-managed non funziona, ammetti un Azure Bot F0 (solo registro gratuito)?
5. Ammetti le nuove VLAN 25 VOCE e 35 MEET, e i servizi MariaDB, Vexa, trascrizione, Asterisk, Pipecat, Postiz, listmonk, DocuSeal e fatturazione?
6. Ammetti come esterni l'operatore telefonico, Meta per WhatsApp, Telegram, Slack, un relay SMTP e gli strumenti commerciali che restano?
7. RAM: compri altri 192 GB prima della fase C? Come sono fatti i 192 GB attuali?
8. Seconda GPU: RTX 2000 Ada 16 GB, anticipata prima della fase E? C'è posto nel riser secondario?
9. Fasce orarie della RTX 4000: a che ora va a Experimental-1 e quando torna all'AI?
10. Cos'è Sirius, e cosa sono mcp-enrich, mcp-memory e runner-dash?
11. Con cosa sostituisci MinIO?
12. Che stima in settimane dai alle fasi F0-F4?
13. Piano M365 e piano Jira di oggi?

**Per i CEO**
14. Confermate le classi di approvatori (§5.2)?
15. Confermate l'eccezione per la voce sintetica di Andrea, solo per chi chiede di essere richiamato?
16. Quali strumenti commerciali fuori dal board tenete (fino a 187,62 € al mese)?
17. I dati rossi che l'MCP RAG può dare a Claude Team: oscurati, oppure solo agli agenti via API?
18. Chi fattura (Sersan Limited nel Regno Unito o un soggetto italiano) e con quale sistema?

**Per Mattia**
19. TypeScript va bene come linguaggio del motore? Puoi dare 2,5 gp a settimana dalla fase B?

---

## 12. Fonti

**File del progetto** (letti il 25/10/2026)
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt` (board di Michele, vincolante)
- `PRESENTAZIONE-CEO.md` (§1, §4, §5, §10-15, appendice A)
- `ricerca/00-visione-funzionalita.md`, `01-sersanoutreach.md`, `22-architettura-scelta.md`
- `ricerca/25-board-michele-e-delta.md`, `26-claude-agent-sdk.md`, `27-hermes-self-hosted.md`, `28-chat-di-gruppo-self-hosted.md`, `29-conoscenza-task-e-documenti.md`, `30-call-e-trascrizione-self-hosted.md`, `31-voce-andrea-self-hosted.md`, `32-hardware-e-upgrade.md`, `33-costi-v2.md`

**Pagine web** (lette il 25/10/2026)
- Agent SDK, server MCP e intestazioni: https://code.claude.com/docs/en/agent-sdk/mcp
- Chat SDK: https://github.com/vercel/chat
- listmonk: https://github.com/knadh/listmonk ; https://api.github.com/repos/knadh/listmonk/releases ; https://listmonk.app/docs/apis/apis/
- DocuSeal: https://github.com/docusealco/docuseal ; https://api.github.com/repos/docusealco/docuseal/releases/latest
- Postiz: https://github.com/gitroomhq/postiz-app
- Server MCP di Firecrawl: https://github.com/firecrawl/firecrawl-mcp-server
- Amazon SES, prezzi: https://aws.amazon.com/ses/pricing/
- Hetzner Cloud, prezzi: https://www.hetzner.com/cloud/
- Exchange Online, limite sui destinatari esterni (MC787382, letto tramite ricerca): https://mc.merill.net/message/MC787382
- Invoice Ninja, licenza (fonte terza, letta tramite ricerca): https://beancount.io/blog/2026/10/06/self-hosted-invoicing-freelancers-invoice-ninja-crater-invoiceplane-guide
- Context7: libreria `/websites/code_claude_en_agent-sdk`, quota mensile esaurita il 25/10/2026

Le altre fonti web (Anthropic, LiteLLM, Microsoft, Qdrant, BookStack, Atlassian, Messagenet, NVIDIA, HPE, prezzi di GPU, RAM, UPS e PBS) sono elencate nei rapporti 25-33 da cui riprendo i fatti.
