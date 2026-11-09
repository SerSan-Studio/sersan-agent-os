# 34 · Proposta 2: Hermes Agent tutto in casa, dentro il board di Michele

**Data:** 25/10/2026. **Per:** Alberto Tuveri, da portare a Michele Sanna (CPTO). Le parti di budget servono anche ad Alessandro Serratt (CEO).
**Cosa è:** la proposta completa con Hermes Agent come orchestratore sul DL380. Niente Hermes Cloud, niente Nous Portal, niente account Nous. Claude passa da LiteLLM con la chiave API. Il Cancello approva ed esegue tutto ciò che esce. Il motore sull'Agent SDK di Claude è descritto nel rapporto 26: qui scrivo la Proposta 2 per intero, come se fosse la scelta, con i suoi limiti e le sue uscite.
**Vincolo:** il board di Michele (`allegati/infra/`) è vincolante. Dove serve qualcosa che il board non ha, lo scrivo come componente da aggiungere o come necessità esterna con il suo costo, mai come rinuncia (regola di Alberto del 25/10/2026).
**Fonti:** i rapporti 25-33 del 25/10/2026, i rapporti 10 e 22, `PRESENTAZIONE-CEO.md`, `00-visione-funzionalita.md`, la documentazione ufficiale di Hermes riletta oggi, le API di GitHub. Context7 oggi ha esaurito la quota mensile: la documentazione l'ho letta con WebFetch sulle pagine ufficiali [verificato: risposta di Context7 del 25/10/2026].

**Etichette.**
- [verificato: fonte] = letto oggi nella fonte indicata (pagina ufficiale, file del progetto, API di GitHub). "Via ricerca" vuol dire letto in un risultato di ricerca e non sulla pagina intera.
- [non verificato] = stima, calcolo, proposta di progetto o voce di terzi.
- gp = giorni-persona di sviluppo. "Base" è la stima senza riserva; "con riserva" aggiunge circa un terzo.

**Prezzi.** IVA esclusa salvo dove è scritto, rilevati il 24-25/10/2026. Cambio 1 $ = 0,8934 €, come nei rapporti 14, 22 e 33 [verificato: ricerca/33, "Come leggere"].

**Fasi.** Per non confonderle con le fasi del board (F0-F5), le fasi di questa proposta si chiamano H0-H6.

---

## In breve

**Cosa proponiamo.** Hermes Agent gira sul DL380 in **sei istanze Docker separate**, una per confine di fiducia: commerciale, marketing, progetti, direzione, amministrazione e una per l'assistente personale di chi lo vuole. Stanno in una VM della VLAN 30 APPS, con l'immagine fissata per digest, un volume per istanza e l'uscita su allowlist [proposta; fatti sui container: verificato, docs Docker di Hermes]. Dei 57 agenti, **50 sono profili Hermes** e **7 sono codice o servizi** che il board ha già o che costruiamo (Cancello, LiteLLM, n8n, pipeline di indicizzazione, trascrizione) [non verificato: proposta, §6]. Claude ragiona via LiteLLM con una chiave virtuale per profilo e un budget per squadra e per persona. Il **Cancello** è l'unico pezzo che manda mail, scrive al cliente, tocca il CRM, pubblica o telefona; ha un suo bot Teams per le carte di approvazione, con l'identità Entra di chi preme. La memoria è quella del board: BookStack, PostgreSQL 16, Qdrant con BM25 e reranker dietro l'MCP RAG.

**Perché Hermes.** Porta pronti i pezzi che la visione chiede e che con l'Agent SDK vanno scritti: profili con nome, persona e skill proprie; una bacheca kanban fra profili con dispatcher, corsia di revisione e blocco "serve un umano"; skill che l'agente scrive e migliora; canali Teams, Telegram, WhatsApp e Slack; un preset per entrare in Buzz [verificato: docs Hermes kanban, teams, acp; ricerca/10 §4]. Il primo bot che risponde in Teams o Telegram arriva in giorni, non in settimane [non verificato: stima di ricerca/27 §9.5].

**Cosa pesa contro, ad oggi.**
- Il gateway unico per tutti i profili ha **276 problemi aperti, 9 di sicurezza, 0 risolti su `main`** (39 in revisione in 14 PR) [verificato: issue #143547 via API GitHub, aggiornata il 25/10/2026 alle 14:54 UTC]. Uno di questi porta gli avvisi di un bot nella chat di un altro bot [verificato: ricerca/27 §6.2].
- Nel 2026 il GitHub Advisory Database conta **almeno 45 avvisi** su Hermes, uno critico; la pagina di sicurezza del repository ne pubblica 0 [verificato: ricerca/27 §7]. L'ultima release è ancora la **v0.22.5 del 23/10/2026**; la v0.23 con le note complete non è uscita [verificato: API GitHub releases, 25/10/2026].
- Hermes non passa all'MCP RAG l'identità della persona che scrive: solo un valore fisso o il nome del profilo, "resolved once at connect time" [verificato: docs MCP di Hermes]. I permessi per persona del board valgono quindi per istanza, non per persona.
- Su WhatsApp Hermes non manda i modelli approvati da Meta [verificato: ricerca/27 §5]. In Buzz l'adattatore approva da solo ogni richiesta di permesso di Hermes [verificato: docs ACP di Hermes].

**Come lo conteniamo.** Istanze separate, un bot per istanza, terminale ed esecuzione di codice spenti, nessuno strumento che invia, un plugin `pre_tool_call` che blocca e "fails closed" allo scadere del tempo [verificato: docs hooks di Hermes], le approvazioni di business solo nel Cancello, una verifica con criteri misurabili alla fine della fase H1 e un'uscita già prezzata verso l'Agent SDK.

**Tempi.** Sette fasi in 42 settimane di calendario. Le fasi H0-H5 (34 settimane) valgono **151 gp di base, circa 201 con la riserva**; la fase H6, le altre automazioni, **20 gp di base, circa 26,5 con la riserva** [non verificato: stime, §8]. L'infrastruttura F0-F4 del board la porta avanti Michele e non è contata qui.

**Costi.** Hermes costa 0 € di licenza (MIT) [verificato: ricerca/27 §2.1]. In più rispetto a oggi, senza il kit commerciale: circa **135 €/mese** con Azure ancora accesa, circa **15 € in meno di oggi** dopo lo spegnimento di Azure, circa **14 €** con gli agenti al lavoro, circa **104 €** con "Andrea" (58 € con il piano PRO dell'operatore). Il listino mensile dello scenario consigliato è circa **519 €**; le integrazioni fuori dal board, se approvate come eccezioni, aggiungono fino a circa **284 €** [non verificato: calcoli su ricerca/33, §9]. Una tantum: circa **3.114-4.354 € subito**; più avanti circa **1.631-2.009 €** (seconda GPU, staffa, UPS) oppure **2.447-3.227 €** con 192 GB di RAM in più [non verificato: calcoli su ricerca/32 e 33, §9.3].

**Copertura.** Tutte le 90 voci A1-L12 hanno un componente e una fase. Dove manca un pezzo (seconda GPU, operatore telefonico, relay SMTP, firma elettronica, strumento di fatturazione, API di LinkedIn, eccezioni di Michele), il §7 dice cosa serve e quanto costa.

---

## 1. La proposta in dieci punti

1. **Hermes orchestra, in sei istanze.** Un container per confine di fiducia, ognuno con il suo volume `/opt/data`, il suo profilo principale e il suo bot. La documentazione di Hermes prevede container separati per "network segmentation" e conformità, e avverte di non far girare mai due gateway sullo stesso volume [verificato: docs Docker di Hermes, 25/10/2026].
2. **Claude ragiona, LiteLLM conta.** Fornitore con nome in `transport: anthropic_messages`, alias uguali agli ID veri (`claude-sonnet-5-5`), così la cache dei prompt di Hermes parte [verificato: ricerca/27 §3.1]. Una chiave virtuale per profilo, un team per squadra, un utente per persona [non verificato: proposta su docs LiteLLM, ricerca/26 §4.3].
3. **Il Cancello agisce.** Gli agenti hanno un solo strumento di scrittura, `propose_action`, verso il Cancello. Il Cancello classifica, crea la carta, la manda sul telefono, esegue una volta sola dopo il sì e registra tutto [non verificato: proposta, come ricerca/22 §2].
4. **Le carte arrivano dal bot del Cancello, non da Hermes.** Le carte di Hermes su Teams hanno quattro pulsanti, fra cui "Always Allow", e servono ai comandi pericolosi [verificato: docs Teams di Hermes]. Per le azioni di business non le usiamo: il Cancello ha un suo bot con Adaptive Card e controlla l'`aadObjectId` di chi preme [non verificato: proposta di ricerca/28 §2.3].
5. **n8n tiene gli orari, Hermes i lavori a più passi.** Il debrief alle 7:00, i bandi notturni, il download delle trascrizioni di Teams sono flussi n8n che chiamano l'API di Hermes (`/v1/runs`) o un suo webhook firmato [verificato: ricerca/27 §4; divisione: proposta].
6. **La memoria è quella del board.** BookStack per i testi, PostgreSQL per i dati, Jira per i task, M365 per documenti e posta, Qdrant dietro l'MCP RAG per la ricerca [verificato: ricerca/29 "In breve"]. Nessun fornitore di memoria esterno dentro Hermes [proposta di ricerca/27 §4].
7. **Dentro un'istanza gli agenti si passano il lavoro sulla kanban di Hermes; fra istanze, su un MCP "passaggi" nostro in PostgreSQL**, perché la kanban è "single-host by design" e vive in un SQLite per istanza [verificato: docs kanban di Hermes].
8. **Le persone parlano con gli agenti in Teams.** Telegram per gli avvisi, WhatsApp per i clienti, Slack solo se Michele lo ammette come eccezione, Buzz in prova nella VLAN LAB.
9. **Le call e Andrea sono servizi a parte.** Trascrizione nativa di Teams via Graph e bot Vexa per le call degli altri (rapporto 30); Asterisk, Pipecat e un operatore italiano per Andrea (rapporto 31). Hermes lavora prima e dopo.
10. **Verifica alla settimana 11.** Se un criterio fallisce, si passa al motore sull'Agent SDK senza buttare il resto (§10.2).

---

## 2. Il perimetro: cosa resta in cloud e cosa serve da fuori

| Gruppo | Voce | Ruolo nella Proposta 2 | Fonte |
|---|---|---|---|
| Cloud del board | M365 / Entra ID | identità, MFA, posta, calendario, SharePoint, Teams | [verificato: board-testo-completo.txt] |
| | Claude Team | chat delle persone, Claude Code, connettore MCP RAG con i permessi di chi chiede | [verificato: board] |
| | API Anthropic dietro LiteLLM | motore di tutti i profili Hermes | [verificato: board] |
| | Cloudflare (DNS), GitHub (runner in casa), Supabase, Vercel, Jira, Instantly, S3 facoltativo | come nel board | [verificato: board] |
| Necessità esterne che il board non elenca | Operatore telefonico italiano (Messagenet) | numero e chiamate di Andrea; un trunk estero con numero italiano rischia il blocco (delibera AGCOM 106/25/CONS) | [verificato: ricerca/31 §4.1, fonti secondarie] |
| | Relay SMTP per la newsletter | M365 non è fatto per gli invii di massa; serve un servizio di invio da scegliere | [non verificato: da scegliere e prezzare] |
| | VPS per Pangolin e NetBird, se Michele non apre porte | Pangolin in tunnel di solito sta su un VPS con 80/443 TCP e 51820 UDP | [verificato: ricerca/25 N10, guide di terzi]; Hetzner "Cost-Optimized" da 5,99 €/mese IVA esclusa, disponibilità incerta [verificato: hetzner.com/cloud, 25/10/2026] |
| | Meta (WhatsApp Cloud API) | canale verso i clienti, a messaggio | [verificato: ricerca/28 §6.2] |
| | Telegram Bot API | avvisi, gratuita | [verificato: ricerca/28 §6.1] |
| Eccezioni da far approvare a Michele | Slack, Apollo, Perplexity, Metricool, moda.app, Higgsfield | integrazioni che la visione usa e che il board non elenca (§9.2) | [verificato: ricerca/25 N08; ricerca/33 §2.5] |
| Esce | Hermes Cloud, Nous Portal, Hermes Relay, Hermes for Business | fuori dal perimetro | [verificato: ricerca/27 §2.1] |

**Telemetria di Hermes.** Le metriche condivise verso Nous sono spente di default [verificato: ricerca/27, `config_defaults.py` su main]. La v0.22.5 ha introdotto un "account ospite" Nous: che senza login non parta nessuna chiamata va provato con il NetFlow di OPNsense [non verificato: ricerca/27 §2.1].

---

## 3. Componenti e dove girano

### 3.1 Lo schema

```
PERSONE (4)  Teams (M365, Entra + MFA + FIDO2): un bot per istanza Hermes, un canale per squadra,
             #agenti (specchio dei passaggi), #approvazioni (bot del Cancello), canali dei clienti
             Claude Team: chat, Claude Code, connettore MCP RAG (OAuth Entra, permessi per persona)
             Telegram (facoltativo): solo avvisi verdi · WhatsApp Cloud API: clienti, tutto via Cancello
             Slack (solo se approvato come eccezione): Socket Mode, nessuna porta in ingresso
      | HTTPS firmato (JWT Microsoft, firma Meta)            ^ polling in uscita (Telegram, Slack)
== OPNsense, default-deny ======================================================================
EDGE  (20)  Traefik + Pangolin: rotte pubbliche strette, "Bypass Auth" solo per percorso:
            /api/messages dei bot, /webhooks/whatsapp, MCP RAG (OAuth + IP di Anthropic),
            firma dei clienti (DocuSeal), webhook di Instantly verso n8n
APPS  (30)  VM agenti-01 (Docker): 6 istanze HERMES fissate per digest, un volume ciascuna
              commerciale · marketing · progetti · direzione · amministrazione · personale
              terminale e codice spenti · nessuno strumento che invia · plugin pre_tool_call
            VM cancello-01: CANCELLO (carte, approvatori, esecutori, audit, stop, freno ai giri)
              + bot Teams delle carte + MCP "passaggi" fra istanze + pagina web di riserva
            LXC mcp-01 (nuovo): MCP memoria su Postgres, MCP BookStack, MCP Firecrawl, MCP Jira
            Dal board: LiteLLM · n8n · MCP RAG · mcp-memory · mcp-enrich · openoutreach
              · Firecrawl · BookStack · Open WebUI · bandi-watcher
            Nuovi: Pipecat (Andrea) · endpoint audio dal telefono · DocuSeal · listmonk · Postiz
VOCE  (25, nuova)  Asterisk 22 LTS <-> trunk Messagenet
MEET  (35, nuova)  VM meet-01: Vexa, bot nelle call organizzate dai clienti
DATA  (40)  PostgreSQL 16 (Cancello, passaggi, memoria, LiteLLM, n8n) · Qdrant · MinIO o sostituto
            · Vaultwarden · Infisical · MariaDB per BookStack (nuovo)
AI    (80)  RTX 4000 di giorno: Qwen3-4B, embedding, reranker, Docling, trascrizione dal vivo
            la sera: CPU · con la seconda GPU da 16 GB: Andrea, trascrizione e RAG 24 ore su 24
CICD  (50)  runner GitHub: agenti Sviluppatori (Claude Code) · stage delle istanze Hermes
OBSRV (70)  Prometheus · Grafana (organigramma e costi) · Loki · Uptime Kuma · Wazuh · NetBox
LAB   (90)  Experimental-2: pilota Buzz con Hermes via ACP, pilota Paperclip, nessun dato dei clienti
================================================================================================
IN CLOUD (board)   M365/Entra · Claude Team · API Anthropic via LiteLLM · Cloudflare · GitHub
                   · Supabase · Vercel · Jira · Instantly · S3 facoltativo
NECESSITÀ ESTERNE  operatore telefonico italiano · relay SMTP · eventuale VPS · eccezioni (§9.2)
```

Le VLAN 10-99 e i servizi "dal board" sono quelli di `board-vlan.txt` [verificato]. Le VLAN 25 VOCE e 35 MEET sono proposte dei rapporti 31 e 30 [non verificato: proposte]. Il resto dello schema è la mia proposta [non verificato].

### 3.2 Tabella dei componenti

| Componente | Nel board? | VLAN | Macchina | RAM | GPU | Chi lo installa | Etichetta |
|---|---|---|---|---|---|---|---|
| Hermes Agent, 3 istanze nel pilota, 6 a regime | no | 30 | VM `agenti-01` con Docker, 8-16 vCPU | 6-12 GB nel pilota; 19-32 GB a regime con i lavoratori della kanban | no | Alberto, Mattia | limite d'esempio 4 GB e 2 CPU per container, minimo 1 GB e 1 CPU, consigliati 2-4 GB [verificato: docs Docker di Hermes]; somme [non verificato: stima] |
| Cancello: servizio TypeScript, worker, bot Teams delle carte, MCP "passaggi", pagina web | no | 30 | VM `cancello-01` | 2-3 GB | no | Alberto, Mattia | TypeScript [verificato: ricerca/22 §2]; RAM [non verificato: ricerca/32 §3.3] |
| MCP nuovi: memoria su Postgres, BookStack, Firecrawl, Jira | no | 30 | LXC `mcp-01` | 0,5-1 GB | no | Mattia | [non verificato: proposta di ricerca/29 §7] |
| LiteLLM con budget | sì | 30 | del board | nei 24 GB del board | no | Michele (F4), noi la configurazione | [verificato: board] |
| n8n | sì | 30 | del board | nei 69 GB del board | no | Michele | [verificato: board-vlan.txt] |
| MCP RAG, mcp-memory, mcp-enrich, openoutreach | sì | 30 | del board | idem | no | Michele, Mattia | [verificato: board-vlan.txt] |
| BookStack | sì | 30 | del board | idem | no | Michele | [verificato: board-vlan.txt]; chiede MySQL 8 o MariaDB 10.6, non elencati nel board [verificato: ricerca/29 §3.1] |
| PostgreSQL 16, Qdrant, Infisical, Vaultwarden | sì | 40 | del board | idem | no | Michele | [verificato: board-vlan.txt] |
| MinIO | sì, ma archiviato | 40 | del board | idem | no | Michele | archiviato dal 12/02/2026 [verificato: ricerca/25 N14]; sostituto (Garage, SeaweedFS) [non verificato: ricerca/33 §2.7] |
| Pipeline AI (Docling, filtro, Qwen3-4B, embedding, reranker) | sì | 80 | LXC `ai-gpu-01` | nei 24 GB del board | RTX 4000 di giorno | Michele (F4) | [verificato: board] |
| Trascrizione (faster-whisper, Parakeet, pyannote) | no | 80 | LXC `ai-gpu-01` | 4-8 GB | 2,1-4,5 GB di giorno; CPU la sera | Michele, Mattia | [verificato: ricerca/30 §6; RAM non verificato] |
| Vexa, bot nelle call | no | 35 nuova | VM `meet-01` | 12 GB con 3 bot | no (usa la trascrizione) | Michele | 1 CPU e 2 GB per bot [verificato: ricerca/30 §4.2]; totale [non verificato] |
| Andrea: Asterisk, Pipecat, STT e TTS | no | 25 nuova e 30 | LXC | 6-8 GB su CPU | seconda GPU nella fase 2 di Andrea | Michele, Mattia | [non verificato: ricerca/31 §8.2] |
| DocuSeal, firma elettronica | no | 30 | container | circa 1 GB | no | Michele | AGPL-3.0, 18.788 stelle, attivo il 19/10/2026 [verificato: API GitHub, 25/10/2026]; RAM [non verificato] |
| listmonk, newsletter | no | 30 | container | circa 0,5 GB | no | Mattia | AGPL-3.0, 23.961 stelle, attivo il 24/10/2026 [verificato: API GitHub, 25/10/2026]; RAM [non verificato] |
| Postiz, programmazione dei post (alternativa a Metricool) | no | 30 | container | 1-2 GB | no | Mattia | AGPL-3.0, 37.763 stelle, attivo il 24/10/2026 [verificato: API GitHub, 25/10/2026]; RAM [non verificato] |
| Buzz, pilota | no | 90 LAB | Experimental-2 | 4-8 GB | no | Alberto | [verificato: ricerca/28 §9 per la RAM, stima di quel rapporto] |
| Teams, Jira, M365 | cloud | | | | | Michele (impostazioni) | [verificato: board] |

### 3.3 Le sei istanze Hermes

| Istanza | Profili (§6) | Chi può scrivere al bot (`TEAMS_ALLOWED_USERS`) | Identità verso l'MCP RAG | Canali | Dati massimi |
|---|---|---|---|---|---|
| `hermes-commerciale` | 16: Outbound, Chiamate, Vendite | tutti e quattro | servizio "commerciale": clienti e lead, niente finanza | bot Teams "Agenti Commerciali"; WhatsApp Cloud API (intake e clienti); Telegram avvisi | giallo; rosso solo oscurato |
| `hermes-marketing` | 12: Marketing e Studio contenuti | tutti e quattro | servizio "marketing": pubblico e interno non personale | bot "Agenti Marketing"; Telegram avvisi | verde e giallo |
| `hermes-progetti` | 8: Progetti | tutti e quattro | servizio "progetti": clienti attivi | bot "Agenti Progetti" | giallo; rosso solo oscurato |
| `hermes-direzione` | 9: Memoria e Direzione | tutti e quattro | servizio "direzione": tutto tranne finanza | bot "Capo di gabinetto"; Telegram avvisi | giallo; rosso solo oscurato |
| `hermes-amministrazione` | 4: Amministrazione | Alessandro e Michele | servizio "finanza": collezione Qdrant separata | bot "Agenti Amministrazione" | rosso solo oscurato |
| `hermes-personale` | 1 per persona che lo chiede (K16) | solo quella persona | nessuna memoria aziendale | chat 1:1 di Teams; Telegram se la persona vuole | personale; salute mai |

Fatti che reggono la tabella:
- `TEAMS_ALLOWED_USERS` prende gli ID degli oggetti Entra; i messaggi di chi non è in lista sono "silently dropped" [verificato: docs Teams di Hermes].
- L'`identity_header` di Hermes manda un valore fisso o il nome del profilo [verificato: docs MCP di Hermes]: per questo l'identità verso l'MCP RAG è una per istanza.
- La collezione `finanza` separata in Qdrant è la proposta di ricerca/29 §6.2 [non verificato: proposta]; Qdrant ha chiavi JWT per collezione [verificato: ricerca/29 §6.2].
- Hermes si definisce "a single-tenant personal agent" [verificato: ricerca/27 §7.2, SECURITY.md]: è il modello giusto per l'assistente personale (K16) e per questo l'istanza personale è separata [non verificato: lettura mia].
- Il raggruppamento per confine di fiducia è la mia proposta, che estende le tre istanze di ricerca/27 §6.3 [non verificato].

**Dentro ogni istanza** il profilo principale è l'unico con un bot. Gli altri profili ricevono lavoro dalla kanban o per delega, non da un bot proprio. Così il gateway unico serve un solo bot per istanza e i problemi della scheda #143547 sui bot multipli (MSG-43, GW-46) non si presentano [non verificato: proposta; i problemi sono verificati in ricerca/27 §6.2].

### 3.4 Rete: flussi e rotte pubbliche

| Flusso | Da → a | Regola | Etichetta |
|---|---|---|---|
| Modelli | istanze Hermes (30) → LiteLLM (30) → api.anthropic.com | chiave virtuale per profilo; uscita di LiteLLM solo verso Anthropic | [verificato: ricerca/27 §2.3; board "API Anthropic dietro LiteLLM"] |
| Memoria | Hermes (30) → MCP RAG (30) → Qdrant (40) | mai accesso diretto a Qdrant; la regola APPS → DATA per MCP RAG va scritta | [verificato: ricerca/29 §6.3, il board non la elenca] |
| Azioni | Hermes (30) → Cancello (30) → servizi esterni | solo `propose_action`; gli esecutori e i loro segreti stanno nella VM del Cancello | [non verificato: proposta] |
| Orari e ingressi | n8n (30) → Hermes `8642` (API) o `8644` (webhook HMAC) | 30 richieste al minuto per rotta, corpo fino a 1 MB | [verificato: ricerca/27 §4] |
| Teams in ingresso | Microsoft → Pangolin/Traefik (20) → Hermes `3978` o `/p/<profilo>/api/messages` | regola Pangolin "Bypass Auth" solo sul percorso del bot; verifica affidata al JWT del Bot Framework | percorsi e porta [verificato: docs Teams di Hermes]; "Bypass Auth" per percorso con jolly `*` [verificato: docs.pangolin.net/manage/access-control/rules] |
| WhatsApp | Meta → Pangolin (20) → `hermes-commerciale` `/whatsapp/webhook` | firma con l'App Secret | [verificato: ricerca/27 §2.3] |
| MCP RAG per Claude Team | server di Anthropic → Pangolin (20) → MCP RAG (30) | OAuth 2.1 con Entra nell'MCP RAG; regola CIDR sugli IP di Anthropic `160.79.104.0/21` | connettori dai server di Anthropic [verificato: ricerca/29 §7.3]; IP [verificato: ricerca/29 §5.4]; regole CIDR in Pangolin [verificato: docs Pangolin] |
| Telegram, Slack | Hermes → api.telegram.org, Slack (Socket Mode) | solo in uscita | [verificato: ricerca/27 §5; ricerca/10 §4.2] |
| Uscite di Hermes | solo LiteLLM, MCP interni, login.microsoftonline.com e servizi del Bot Framework, graph.facebook.com, api.telegram.org | niente PyPI, npm o GitHub in esercizio | [non verificato: stima di ricerca/27 §2.3] |
| Dashboard di Hermes | gruppo admin di NetBird → `9119` | autenticazione obbligatoria | [verificato: ricerca/27 §2.3] |

**Il punto aperto.** Pangolin in tunnel di solito vive su un VPS con IP pubblico; NetBird self-hosted chiede 80/443 TCP e 3478 UDP raggiungibili [verificato: ricerca/25 N10]. Il board dice "nessuna porta aperta" e "IP fisso da richiedere" [verificato: board]. Due strade, da far scegliere a Michele: un VPS (circa 6 €/mese, §2) o porte aperte solo verso la VLAN EDGE con l'IP fisso.

### 3.5 RAM e GPU

**RAM.** Il board lascia circa 53 GB liberi [verificato: board, "Capacità"]. Proxmox limita la cache ZFS al 10 % della RAM con un tetto di 16 GiB, quindi conviene fissarla a 12 GiB per restare nei 16 GB del board [verificato: ricerca/32 §3.2].

| Voce nuova | Pilota (H1-H2) | Regime (da H4) | Etichetta |
|---|---|---|---|
| Hermes: 3 istanze nel pilota, 6 a regime, più i lavoratori della kanban | 6-12 GB | 19-32 GB | [non verificato: stima su 2-4 GB per container dalla docs Docker e su un tetto di 3-4 lavori per istanza] |
| Cancello, bot delle carte, MCP passaggi | 1,5-2 GB | 2-3 GB | [non verificato] |
| MCP nuovi | 0,5-1 GB | 1 GB | [non verificato] |
| Trascrizione e lotti | 4 GB | 8 GB | [non verificato: ricerca/30 §11.2] |
| Vexa | 0-4 GB (versione Lite, una call) | 12 GB (3 bot) | [verificato: 2 GB per bot, ricerca/30; totale non verificato] |
| Andrea su CPU | 0 | 6-8 GB | [non verificato: ricerca/31 §8.2] |
| DocuSeal, listmonk, Postiz | 0 | 2-4 GB | [non verificato] |
| SersanOutreach in crescita, memoria aziendale in crescita | 2 GB | 5-8 GB | [non verificato: ricerca/32 §3.3] |
| **Totale nuovo** | **circa 14-25 GB** | **circa 55-76 GB** | [non verificato] |
| **Margine sui 53 GB liberi** | **circa +28/+39 GB** | **da circa -2 a -23 GB** | [non verificato] |

Conclusione: la RAM di oggi basta fino alla fase H3. **Prima della fase H4** (Andrea e i bot delle call a pieno) servono **192 GB in più** (12 moduli da 16 GB, 384 GB in tutto, unica espansione bilanciata a piena banda) [verificato: ricerca/32 §2.3 per la banda; conclusione non verificata]. Con Hermes il bisogno arriva un po' prima che con l'Agent SDK, perché ogni istanza ha il suo gateway e il suo dispatcher [non verificato: confronto con ricerca/32 §3.3, motore 14-18 GB a regime].

**GPU.** Hermes non usa la GPU [verificato: ricerca/10 §7]. Il Qwen3-4B del board non può fare da modello di un profilo Hermes, perché Hermes chiede almeno 64.000 token di contesto per lavorare con gli strumenti [verificato: ricerca/27 §2.4]. La RTX 4000 fa il lavoro del board di giorno; la trascrizione dal vivo ci entra solo spostando il reranker sulla CPU; la sera la scheda va a Experimental-1 e si lavora su CPU [verificato: board; ricerca/30 §6]. La seconda GPU consigliata è una **RTX 2000 Ada da 16 GB** (837-946 € IVA inclusa al 24-25/10/2026): ci stanno Andrea, la trascrizione dal vivo, embedding, reranker e il modello da 4B, 24 ore su 24 [verificato: prezzi in ricerca/32 §4.3; carico non verificato, §4.6]. La "RTX A2000 con chip Ada da 6 GB GDDR7" del messaggio di Michele non esiste [verificato: ricerca/32 §4.1]. Il board la mette nella fase F5; per avere Andrea con la voce migliore e la trascrizione anche la sera serve già nella fase H4 [non verificato: conseguenza, ricerca/32 §4.7]. È una decisione di budget.

---

## 4. Cosa c'è già nel board e cosa va costruito

| Funzione | Già nel board | Cosa aggiunge Hermes pronto | Cosa costruiamo noi | Etichetta |
|---|---|---|---|---|
| Orari e routine | n8n | cron in linguaggio naturale (non usato per i processi aziendali, per evitare doppioni) | flussi n8n che chiamano Hermes | [verificato: board; ricerca/27 §4]; divisione [proposta] |
| Modelli, chiavi, budget | LiteLLM con budget (F4) | modello per profilo, per card, per sottoagente | chiavi per profilo, alias con "claude", cache automatica accesa | [verificato: ricerca/27 §3.1] |
| Memoria aziendale | Qdrant, BookStack, PostgreSQL 16, MCP RAG, mcp-memory | memoria piccola per profilo (`MEMORY.md` e `USER.md`), ricerca nelle sessioni | MCP memoria su Postgres, MCP BookStack, ingressi della pipeline | [verificato: ricerca/10 §4.2; ricerca/29 §7] |
| Profili con nome | nessuno | profili con `SOUL.md`, skill, memoria, canali | registro dei profili in git e nel Cancello | [verificato: ricerca/10 §4.1] |
| Passaggi fra agenti | nessuno | kanban con dispatcher, revisione, blocco "serve un umano" (dentro un'istanza) | MCP "passaggi" fra istanze, freno ai giri, specchio in `#agenti` | [verificato: docs kanban di Hermes] |
| Canali | Teams (M365) | adattatori Teams, Telegram, WhatsApp Cloud, Slack, oltre 25 canali | registrazioni, rotte pubbliche, regole di uscita | [verificato: ricerca/27 §5] |
| Approvazioni | nessuna | carte per i comandi pericolosi; hook `pre_tool_call` con `block`, `approve`, `modify` | il Cancello con il suo bot, le classi di approvatori, gli esecutori | [verificato: docs hooks e Teams di Hermes] |
| Web | Firecrawl | `web_extract` con `FIRECRAWL_API_URL` | niente | [verificato: ricerca/27 §4] |
| Chat web interna | Open WebUI, Claude Team | API compatibile OpenAI di Hermes; in Open WebUI una sola chiave condivisa | niente (Open WebUI resta sui modelli via LiteLLM) | [verificato: ricerca/27 §4] |
| Osservabilità | Prometheus, Grafana, Loki, Wazuh | esportatore OpenTelemetry, `/insights` | cruscotti per istanza e per agente | [verificato: ricerca/27 §4] |
| Segreti | Infisical, Vaultwarden | `key_cmd` per leggere la chiave da un comando | collegamento a Infisical | [verificato: ricerca/27 §3.1; uso con Infisical non verificato] |
| Call | Teams in M365 | pipeline riunioni Teams via Graph (chiede URL pubblico e rinnovo ogni 72 ore) | raccoglitore n8n in delta (senza porte), Vexa, lotti, telefono | [verificato: ricerca/27 §5; ricerca/30 §3.4] |
| Voce | nessuna | skill solo in uscita verso servizi cloud, niente chiamate in arrivo | Andrea con Asterisk e Pipecat | [verificato: ricerca/10 §4.2; ricerca/31] |
| Firma, newsletter, fatture | nessuna | nessuna | DocuSeal, listmonk e relay SMTP, esecutore verso lo strumento contabile | [non verificato: proposta, §7] |

---

## 5. Come lavorano insieme gli agenti

### 5.1 Dentro un'istanza

- **Profili.** Ogni agente è un profilo con nome, persona, modello, skill e strumenti propri [verificato: ricerca/10 §4.1]. Il modello lo sceglie LiteLLM dalla chiave: Haiku 5.5 per raccolta e smistamento, Sonnet 5.5 per quasi tutto, Opus 5.5 per offerte e analisi [prezzi verificati: ricerca/26 §2, 25/10/2026; scelta: proposta].
- **Kanban.** I compiti sono righe di un SQLite per istanza, visibili a tutti i profili di quella istanza, "profile-agnostic on purpose". Il dispatcher gira nel gateway ogni 60 secondi, riprende i compiti bloccati e lancia il profilo assegnato [verificato: docs kanban di Hermes].
- **Revisione.** `kanban_request_review` porta la card in revisione; un revisore chiude o chiede modifiche [verificato: idem]. La usiamo per i testi che passano da un agente all'altro prima della carta del Cancello [proposta].
- **Serve un umano.** Un profilo blocca la card con `kanban_block` e un motivo; una persona la sblocca dalla chat con `/kanban unblock`, anche mentre l'agente lavora [verificato: idem]. Su Teams il comando va provato: la pagina cita Telegram e Discord [non verificato].
- **Freni interni.** Tetti di lavori in corso per istanza e per profilo; dopo 2 fallimenti di fila la card si blocca da sola; cicli di dipendenze rifiutati; budget di giri per lavoratore [verificato: idem].
- **Delega.** `delegate_task` crea sottoagenti con contesto vuoto e schema d'uscita [verificato: ricerca/10 §4.1]. Profondità 1 per partire [proposta].

### 5.2 Fra istanze: l'MCP "passaggi"

La kanban è "single-host by design": condividerla vorrebbe dire montare lo stesso `kanban.db` in più istanze, con nomi di profilo che si scontrano [verificato: docs kanban di Hermes]. Quindi fra istanze il lavoro passa da un piccolo server MCP nostro, nella VM del Cancello [non verificato: proposta]:

1. Il profilo che passa il lavoro chiama `passa(squadra_destinataria, compito, dati_a_schema, catena_id)`.
2. L'MCP scrive la riga nella tabella `passaggi` in PostgreSQL e applica il **freno ai giri**: al massimo 3 passaggi per catena, 8 messaggi per thread, un tetto in dollari per catena [freno: ricerca/22 §3; numeri non verificati].
3. L'MCP chiama il webhook firmato dell'istanza di destinazione, che apre una card per il profilo giusto [webhook HMAC verificato: ricerca/27 §4].
4. n8n rispecchia il passaggio nel canale Teams `#agenti` con un webhook di Workflows, a senso unico, con il nome dell'agente in testa [webhook di Workflows: ricerca/29 §5.3, non verificato; specchio: proposta].
5. Le persone leggono `#agenti` e intervengono con una @menzione al bot dell'istanza.

Una cautela: il CVE-2026-114463 riguardava proprio i nomi delle rotte dei webhook con ":"; è corretto nella v0.22.2 [verificato: ricerca/27 §7.1]. Le rotte si chiamano senza ":".

### 5.3 Con le persone

| Canale | Come entra | Cosa ci passa | Etichetta |
|---|---|---|---|
| **Teams** | un bot per istanza (adattatore Hermes); registrazione con `@microsoft/teams.cli`, "no Azure portal needed"; se dà errori, Azure Bot F0 gratuito o pagina del Cancello | conversazioni con gli agenti, debrief, riassunti (al massimo gialli) | [verificato: docs Teams di Hermes; ricerca/28 §2.2] |
| **Telegram** | polling in uscita, un bot per istanza (lo stesso token non regge due polling) | solo avvisi verdi ("c'è una carta in attesa") e debrief breve per chi lo vuole | [verificato: ricerca/27 §5; docs multi-profile-gateways] |
| **WhatsApp** | Cloud API di Meta, webhook dietro Pangolin, solo chat dirette | clienti: intake, assistenza, messaggi della pagina; ogni invio passa dal Cancello | [verificato: ricerca/27 §5; ricerca/28 §6.2] |
| **Slack** (eccezione) | Socket Mode, senza URL pubblico | stanze per chi lavora con clienti su Slack (Slack Connect) | [verificato: ricerca/10 §4.2] |
| **Buzz** (pilota in LAB) | Buzz ha Hermes come runtime predefinito via ACP | stanza degli agenti di prova, senza dati dei clienti | [verificato: docs ACP di Hermes] |
| **Claude Team** | connettore MCP RAG e connettore M365 in sola lettura | domande libere alla memoria con i permessi della persona | [verificato: ricerca/29 §5.4 e §7.3] |

**Due regole su WhatsApp e Buzz.**
- Fuori dalla finestra di 24 ore WhatsApp vuole un modello approvato, e Hermes non lo manda [verificato: ricerca/27 §5]. Quei messaggi li manda l'esecutore del Cancello (o n8n con il nodo WhatsApp Business Cloud), sempre dopo una carta [proposta; nodo n8n verificato in ricerca/28 §6.2].
- In Buzz il ponte risponde da solo "allow_once" a ogni richiesta di permesso di Hermes, e `approvals.mode: manual` non aiuta; la documentazione dice di togliere `terminal` e `code_execution` e di tenere l'accesso "Owner only" [verificato: docs ACP di Hermes]. Nel pilota valgono quindi solo i blocchi del plugin `pre_tool_call` e del Cancello [proposta].

### 5.4 Le approvazioni: il Cancello e il telefono

1. Un profilo prepara un'azione e chiama `propose_action` (MCP del Cancello).
2. Il plugin `sersan-guardrail` (Python, `pre_tool_call`) controlla ogni chiamata di strumento: tutto ciò che non è nell'elenco del profilo riceve `block`. Il plugin non usa la direttiva `approve` per le azioni di business. Se il plugin non risponde entro il tempo (30 secondi di default, al massimo 600), lo strumento è bloccato: "fails closed" [verificato: docs hooks di Hermes; elenco e regola: proposta].
3. Il Cancello classifica l'azione (lettura, scrittura interna, invio, pubblicazione, pagamento, cancellazione, credenziali) e crea la carta [classi: verificato, PRESENTAZIONE-CEO §5.4].
4. Il bot del Cancello manda la Adaptive Card in `#approvazioni` o in chat a chi deve approvare. L'app mobile di Teams regge le carte fino alla versione 1.6; `Action.Execute` aggiorna la carta per tutti con nome e ora [verificato: ricerca/28 §2.3].
5. Il Cancello accetta il sì solo se l'`aadObjectId` è fra gli approvatori della classe: Alessandro per outbound e mail ai clienti, Michele per offerte e affermazioni tecniche, Alberto per infrastruttura e codice [classi: verificato, ricerca/22 §3; presenza dell'`aadObjectId` nelle azioni delle carte: da confermare nello spike, ricerca/28 §2.3].
6. Durante l'attesa la card della kanban resta bloccata con `kanban_block`; alla decisione il Cancello la sblocca con un commento tramite il webhook dell'istanza [non verificato: da provare].
7. Dopo il sì l'esecutore agisce una volta sola; se il testo è cambiato, la carta non vale più; tutto va nel registro e in Loki e Wazuh [regola: PRESENTAZIONE-CEO §5.4; log: proposta].

**Riserva senza bot.** Se il bot del Cancello non funziona senza Azure, Michele sceglie fra Azure Bot F0 (0 €, Teams è un canale "standard" con messaggi illimitati) e una pagina del Cancello dietro Pangolin con SSO Entra e FIDO2 [verificato: ricerca/28 §2.2].

**Una regola in più per SersanOutreach.** SersanOutreach ha dal 14-15/10/2026 i modi `auto_blank_invites` e `auto_linkedin`, un autopilota che redige e approva inviti entro i tetti giornalieri [verificato: ricerca/01 riga 45]. Restano spenti finché il Cancello non ne prende il controllo, oppure diventano una regola "Sempre" del Cancello [non verificato: proposta].

### 5.5 La memoria

- Hermes non ha un fornitore di memoria esterno: la memoria aziendale è una sola, quella del board [proposta di ricerca/27 §4].
- Ogni istanza legge: MCP RAG (ricerca ibrida e reranker), MCP memoria su Postgres (regole, obiettivi, catalogo, meeting, decisioni), MCP BookStack in sola lettura (pagine "Come lavoro" per ID stabile), mcp-memory come taccuino per famiglia di agenti [verificato: ricerca/29 §2 e §7; elenco degli strumenti: proposta].
- Con `tools.include` ogni profilo vede solo gli strumenti in lettura che gli servono [verificato: docs MCP di Hermes].
- I blocchi rossi arrivano agli agenti già oscurati dall'MCP RAG, perché poi vanno all'API Anthropic: è la regola dei tre colori [verificato: PRESENTAZIONE-CEO §5.6]. Il filtro del board marca le PII ma non le toglie [verificato: board]: l'oscuramento va costruito e misurato (fase H2).
- Le regole personali (C6) si leggono prima di ogni lavoro per una persona; il `SOUL.md` del profilo tiene solo le regole della squadra [proposta].
- Le skill (A6): Hermes scrive e cura le proprie skill [verificato: ricerca/10 §4.2]. Le modifiche finiscono in una cartella "proposte"; una pull request nel repository delle skill e il sì di una persona le rendono attive [proposta].

### 5.6 Modelli e banca dei token

- LiteLLM applica budget per chiave, team e utente e rifiuta le richieste oltre il tetto; serve PostgreSQL [verificato: ricerca/26 §4.3].
- Una chiave per profilo, un team per squadra, un utente per persona; Hermes `/insights` come controllo incrociato; il conto vero dalla Console ogni mese [proposta; `/insights` verificato in ricerca/10 §4.2].
- Problemi noti sulla strada Hermes-LiteLLM: sonde `/models` senza chiave (401), `context_length` ignorato con gli alias, fornitore con nome che "collassa" sul generico nel gateway unico (MP-19, MP-23, MP-25), lavoratori della kanban che perdono il formato del fornitore (KB-11) [verificato: ricerca/27 §3.2]. Contromisure: ID veri come nomi, `context_length` esplicito, cache automatica di LiteLLM accesa (spenta di default), prova di accettazione prima di ogni aggiornamento [verificato per la cache di LiteLLM: ricerca/27 §3.1; il resto: proposta].

### 5.7 Il percorso di un cliente, con le istanze

1. **Sentinella segnali** (commerciale) trova un'azienda che assume; **Agente email** prepara il primo messaggio; carta ad Alessandro; il Cancello lo invia con Instantly.
2. Il prospect risponde. **Agente email** apre una card per **Agente agenda** e **Agente brief** sulla kanban della stessa istanza. **Agente brief** chiede con `passa` a **Ricerca concorrenza** (marketing) il quadro del settore e ad **Agente slide** (marketing) le slide per noi.
3. **Agente agenda** propone gli orari presi da Outlook via Graph; carta; l'invito parte con il testo di avviso e il flag "avvisato".
4. La call: se è una riunione Teams nostra, la trascrizione nativa arriva via Graph a n8n; se è del cliente, entra Vexa come "SerSan Verbale (AI, registra)" [ricerca/30 §8].
5. n8n apre il lavoro **Post-call**: **Analista chiamate** scrive il riassunto secondo le regole della persona; **Post-call** prepara CRM, to-do e bozza della mail; **Agente proposte** (Opus) prepara l'offerta; **Agente slide** il recap per il cliente; tutto ciò che esce diventa una carta.
6. Le obiezioni passano con `passa` a **Editoriale** (marketing).
7. Michele approva l'offerta; **Agente contratti** prepara il contratto e il Cancello lo manda in firma con DocuSeal; a firma avvenuta, `passa` a **Project manager** (progetti).
8. A ogni milestone **Agente fatture** (amministrazione) prepara la fattura; a fine progetto **Agente casi studio** (progetti) passa il caso al marketing e **Agente clienti simili** (commerciale) ne cerca altri.

Ogni passaggio fra istanze compare in `#agenti`; ogni cosa che esce passa da una carta [proposta, sul percorso di PRESENTAZIONE-CEO §4.10].

---

## 6. I 57 agenti: istanza, tipo, modello, fase

Tipo: **H** = profilo Hermes; **S** = servizio o codice (n8n, pipeline, Cancello, LiteLLM, trascrizione). Modello: H5 = Haiku 5.5, S5 = Sonnet 5.5, O5 = Opus 5.5. Tutta la tabella è una proposta [non verificato]; elenco e compiti degli agenti vengono da PRESENTAZIONE-CEO §4 [verificato].

| # | Squadra | Agente | Tipo | Istanza o servizio | Modello | Fase |
|---|---|---|---|---|---|---|
| 1 | Outbound | Agente email | H | commerciale | S5 | H2 |
| 2 | Outbound | Agente LinkedIn | H | commerciale (invio dall'estensione di SersanOutreach) | S5 | H2 |
| 3 | Outbound | Sentinella segnali | H | commerciale (Firecrawl, mcp-enrich) | H5 | H2 |
| 4 | Outbound | Operatore outbound | H | commerciale (MCP di SersanOutreach) | S5 | H2 |
| 5 | Outbound | Agente clienti simili | H | commerciale | S5 | H4 |
| 6 | Chiamate | Agente chiamate | S | n8n, Graph, Vexa | nessuno | H1 (Teams), H2 (Vexa) |
| 7 | Chiamate | Analista chiamate | H | commerciale | S5 | H1 |
| 8 | Chiamate | Post-call | H | commerciale | S5 | H1 |
| 9 | Chiamate | Agente agenda | H | commerciale (Graph via Cancello) | H5 | H2 |
| 10 | Chiamate | Dettatura | S | servizio di trascrizione; app Claude | nessuno | H2 |
| 11 | Vendite | Agente brief | H | commerciale | S5 | H2 |
| 12 | Vendite | Agente proposte | H | commerciale | O5 | H2 |
| 13 | Vendite | Pipeline | H + S | commerciale; calcolo in Postgres | S5 | H4 |
| 14 | Vendite | Coach vendite | H | commerciale | S5 | H4 |
| 15 | Vendite | "Andrea" | S + H | Pipecat e Asterisk; profilo commerciale prima e dopo | H5 in chiamata | H4 |
| 16 | Vendite | Analista vinto/perso | H | commerciale | S5 | H2 |
| 17 | Vendite | Agente intake | H | commerciale (anche WhatsApp) | S5 | H2 |
| 18 | Vendite | Agente contratti | H | commerciale (DocuSeal via Cancello) | S5 | H6 |
| 19 | Marketing | Editoriale | H | marketing | S5 | H1 |
| 20 | Marketing | Ricerca concorrenza | H | marketing (Firecrawl) | S5 | H1 |
| 21 | Marketing | Analista metriche | H | marketing | H5 | H1 |
| 22 | Marketing | Pubblicatore | H | marketing (Metricool o Postiz, sessione presidiata) | H5 | H1 |
| 23 | Marketing | Agente newsletter | H | marketing (listmonk via Cancello) | S5 | H3 |
| 24 | Marketing | Community manager | H | marketing | S5 | H3 |
| 25 | Marketing | Agente sito e SEO | H | marketing (pull request su GitHub) | S5 | H6 |
| 26 | Marketing | Agente eventi e webinar | H | marketing | S5 | H6 |
| 27 | Studio | Copywriter | H | marketing | S5 | H1 |
| 28 | Studio | Agente slide | H | marketing | S5 | H2 |
| 29 | Studio | Agente video | H | marketing (HyperFrames; Higgsfield se approvato) | S5 | H2 |
| 30 | Studio | Agente grafiche | H | marketing | S5 | H2 |
| 31 | Progetti | Project manager | H | progetti (Jira) | S5 | H3 |
| 32 | Progetti | Agente task | H | progetti (Jira) | H5 | H1 |
| 33 | Progetti | Report cliente | H | progetti | S5 | H3 |
| 34 | Progetti | Onboarding cliente | H | progetti (Teams, SharePoint, BookStack via Cancello) | S5 | H3 |
| 35 | Progetti | Sviluppatori | H + S | progetti; Claude Code sui runner della VLAN 50 | S5, O5 | H3 |
| 36 | Progetti | Assistenza clienti | H | progetti | S5 | H6 |
| 37 | Progetti | Agente rinnovi | H | progetti | S5 | H6 |
| 38 | Progetti | Agente casi studio | H | progetti | S5 | H6 |
| 39 | Memoria | Raccoglitore | S | n8n e pipeline del board | H5 per i metadati | H1-H2 |
| 40 | Memoria | Pulitore | S | filtro del board e oscuramento nell'MCP RAG | nessuno | H2 |
| 41 | Memoria | Bibliotecario | H | direzione (MCP RAG) | S5 | H2 |
| 42 | Memoria | Archivista | H | direzione | H5 | H2 |
| 43 | Memoria | Sistemista | H | direzione (Grafana e Prometheus in lettura) | H5 | H2 |
| 44 | Direzione | Capo di gabinetto | H | direzione | S5 | H1 |
| 45 | Direzione | Report del mattino | H | direzione (avviato da n8n alle 7:00) | S5 | H1 |
| 46 | Direzione | Banca dei token | S | LiteLLM e Cancello | nessuno | H1 |
| 47 | Direzione | Registro e audit | S | Cancello, Loki, Wazuh | nessuno | H1 |
| 48 | Direzione | Guardiano | S | Cancello e plugin `pre_tool_call` | nessuno | H1 |
| 49 | Direzione | Mappatore processi | H | direzione | O5 | H3 |
| 50 | Direzione | Intervistatore | H | direzione | S5 | H3 |
| 51 | Direzione | Smistatore posta | H | direzione (Outlook in sola lettura) | H5 | H2 |
| 52 | Direzione | Allenatore AI | H | direzione | S5 | H6 |
| 53 | Direzione | Assistente personale | H | istanza personale | S5 | H6 |
| 54 | Amministrazione | Agente fatture e incassi | H | amministrazione | S5 | H6 |
| 55 | Amministrazione | Agente acquisti e abbonamenti | H | amministrazione | H5 | H6 |
| 56 | Amministrazione | Controllo di gestione | H | amministrazione (numeri da Postgres) | O5 | H6 |
| 57 | Amministrazione | Agente bandi e finanziamenti | H | amministrazione, sopra la pipeline bandi del board | S5 | H2 |

Conteggio: 50 profili Hermes (16 commerciale, 12 marketing, 8 progetti, 9 direzione, 4 amministrazione, 1 personale) e 7 servizi [non verificato: conteggio sulla tabella]. Cento agenti restano la traiettoria (G9): la RAM cresce con i lavori in corso insieme, non con i profili definiti [verificato: ricerca/32 §3.3, nota su G9].

---

## 7. Copertura voce per voce (A1-L12)

Tutte le righe sono proposte di progetto [non verificato: proposta]. I fatti che le reggono sono nei §2-6 con le loro etichette. "Lacuna e cosa serve" dice cosa manca oggi per avere la funzione, mai che la funzione si toglie.

### 7.1 J. Il cuore dell'idea

| Voce | Come la realizza la Proposta 2 | Fase | Lacuna e cosa serve |
|---|---|---|---|
| J1 Un solo sistema multi-agente | 6 istanze Hermes, una memoria comune, un Cancello, l'MCP passaggi | H1-H3 | nessuna |
| J2 Squadre con compito e responsabile | squadre del §6, responsabile umano nel registro del Cancello e nella persona del profilo | H1 | nessuna |
| J3 Outreach con agenti specializzati | 5 profili Outbound in `hermes-commerciale` | H2 | nessuna |
| J4 Email → proposte → chiamate | kanban della stessa istanza; delega | H2 | nessuna |
| J5 Agente in ogni call | trascrizione nativa di Teams via Graph (nostre), Vexa (dei clienti), telefono (dal vivo) | H1-H2 | i bot non registrati entrano solo se il cliente li ammette; riserva: registrazione sul PC [ricerca/30 §4.4] |
| J6 Brief prima e dopo con slide per noi e per il cliente | Agente brief e Agente slide (passaggio fra istanze) con i template SerSan | H2 | moda.app solo come eccezione (26,80 €/mese) |
| J7 Marketing con outreach e studio | passaggi fra `marketing` e `commerciale`; Ricerca concorrenza e Analista metriche | H1-H2 | nessuna |
| J8 Squadra progetti | `hermes-progetti` con Jira | H1-H3 | Jira Standard (28,27 €/mese) per i permessi degli account di servizio |
| J9 Chat di gruppo come Buzz, con Slack, Telegram, WhatsApp | Teams (stanze, agenti con nome, telefono), Telegram, WhatsApp; Buzz pilota in LAB; Slack via Hermes | H1-H5 | Telegram, WhatsApp e Slack sono eccezioni da far approvare; Slack Pro 27 €/mese; WhatsApp a messaggio; Buzz pre-1.0 resta pilota |

### 7.2 A. Memoria e orchestrazione

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| A1 Tutte le riunioni registrate e trascritte | Teams nativo, Vexa, telefono via NetBird; lotti Parakeet o WhisperX con pyannote | H1-H2 | GPU piena di giorno, assente la sera: CPU o seconda GPU (837-946 € IVA inclusa) |
| A2 Memoria relazionale | BookStack (testi), PostgreSQL (dati), Jira (task), M365 (documenti) | H2 | MariaDB per BookStack da aggiungere al board |
| A3 Memoria vettoriale | Qdrant con BM25 e reranker dietro l'MCP RAG; ingressi da Sirius, BookStack, Jira, SharePoint, Outlook, trascrizioni | H2 | sapere cos'è Sirius; regola APPS → DATA per l'MCP RAG |
| A4 Orchestratore sul server | Hermes self-hosted, 6 istanze | H1 | verifica alla settimana 11 (§10.3) |
| A5 Agenti per ruolo | raccolta e pulizia come servizi; indicizzazione nella pipeline; azione nei profili | H1-H3 | nessuna |
| A6 Agenti che imparano | skill scritte e curate da Hermes, attive dopo la revisione di una persona | H3 | nessuna |
| A7 Chat condivisa fra agenti | kanban per istanza, MCP passaggi fra istanze, specchio in `#agenti` | H3 | la kanban non attraversa le istanze: serve l'MCP passaggi (3 gp) |

### 7.3 B. Dopo una call

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| B1 Punti nel canale del cliente | canale privato Teams per cliente; con il cliente canale condiviso o mail, dopo la carta | H1 interno, H2 cliente | canale condiviso con altre organizzazioni da provare [ricerca/28 §2.5] |
| B2 Opportunità nel CRM | esecutore del Cancello verso SersanOutreach | H2 | la nuova operazione che crea un deal [PRESENTAZIONE-CEO §11] |
| B3 Mail di follow-up | bozza, carta, esecutore Outlook via Graph, solo al dominio del cliente | H1 bozza, H2 invio | nessuna |
| B4 To-do al team | Jira, scrittura interna del Cancello | H1 | nessuna |
| B5 Autonomia crescente | regole "Sempre" del Cancello dopo 20 approvazioni uguali | H5 | nessuna |

### 7.4 C. La giornata

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| C1 Debrief del mattino | n8n alle 7:00 → Report del mattino; numeri calcolati da Postgres; chat Teams e mail | H1 | nessuna |
| C2 Agente in ogni call, anche per chi manca | `recordAutomatically` sulle nostre riunioni; Vexa sulle altre | H1-H2 | va provato se la registrazione automatica parte senza nessuno di SerSan [ricerca/30 §3.6] |
| C3 Analisi della call | Analista chiamate a schema; niente stima delle emozioni | H1 | nessuna |
| C4 Dettatura | dettatura delle app Claude; note vocali via NetBird o OneDrive trascritte sul server | H2 | GPU o CPU per la trascrizione |
| C5 Registro dei meeting | tabella `meetings` in Postgres, vista in Grafana | H2 | nessuna |
| C6 Regole di ciascuno | pagina BookStack "Come lavoro" letta per ID prima di ogni lavoro | H1 | nessuna |

### 7.5 D. Vendite

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| D1 Pipeline pesata | calcolo in Postgres dagli eventi di SersanOutreach, con intervallo | H4 | storico: oggi 0 vinti; pesi dichiarati fino a 30-50 chiusure [ricerca/22 §4] |
| D2 Brief dall'email della persona | Agente brief con mcp-enrich, MCP RAG, posta, Firecrawl | H2 | post LinkedIn solo con mezzi consentiti; Apollo come eccezione (43,78 €/mese) |
| D3 Storico della relazione | linea del tempo dall'MCP RAG con filtro `cliente` | H2 | nessuna |
| D4 Slide automatiche | Agente slide con i template SerSan | H2 | moda.app solo come eccezione |
| D5 Offerta dal catalogo | Agente proposte su Opus; catalogo in BookStack e Postgres; firma di Michele | H2 | nessuna |

### 7.6 E. Tempo, token e policy

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| E1 Tempo per imparare | §8 | n.a. | nessuna |
| E2 Costruire ora | §9 | n.a. | nessuna |
| E3 Banca dei token | LiteLLM per chiave, squadra e persona; avvisi del Cancello all'80 %, stop al 100 % | H1, H3 per persona | nessuna |
| E4 Formazione | un'ora documentata per i quattro, aggiornata a ogni agente nuovo | H0 | nessuna |

### 7.7 F. Processi

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| F1 Metadati del lavoro | report e log di M365, aggregati, con il consenso di ognuno | H3 | quali API di M365 usare è da verificare [ricerca/29 §5.2] |
| F2 Interviste | Intervistatore in chat 1:1 di Teams | H3 | nessuna |
| F3 Mappa dei processi | Mappatore su Opus; pagine BookStack | H3 | nessuna |
| F4 Ore e automazioni consigliate | Mappatore con ore e costi in Postgres | H3 | nessuna |
| F5 AI per tutti | Teams e Claude Team per tutti; Open WebUI per i modelli locali | H0-H1 | nessuna |

### 7.8 G. Vendite che si allenano e organigramma

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| G1 Call di vendita in un canale | canale Teams "Call di vendita" | H4 | nessuna |
| G2 Fit score | qualificatore di SersanOutreach esteso alle call | H4 | volumi |
| G3 Valutazione e consigli | Coach vendite | H4 | parere legale; niente emozioni (AI Act art. 5) |
| G4 Report a chi ha fatto la call | chat 1:1; al responsabile solo aggregati | H4 | parere legale |
| G5 Andrea in 90 secondi, 24/7 | Asterisk, Pipecat, Haiku 5.5 col pensiero spento, Pocket TTS su CPU | H4 | operatore italiano (30 €/mese PRO o circa 76 € a consumo); voce migliore con la seconda GPU; parere legale; eccezione alla regola del piano marketing sulle voci sintetiche |
| G6 Impara dai rifiuti | analisi settimanale delle trascrizioni, nuove aperture approvate, prova A/B | H4 | nessuna |
| G7 Più conversione | tempi di richiamata e meeting nel debrief | H4 | nessuna |
| G8 Vinti e persi al marketing | Analista vinto/perso → Editoriale | H2 | volumi |
| G9 Agenti in organigramma fino a cento | registro nel Cancello; Grafana; pagina BookStack rigenerata | H1-H3 | RAM in più a regime (§3.5) |
| G10 Superpotere | risultato dell'insieme | n.a. | nessuna |

### 7.9 H. Adozione

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| H1 Formarsi e sperimentare | due ore a settimana, template di profilo Hermes | H0 | nessuna |
| H2 Non delegabile | i CEO approvano le carte e leggono il debrief | H1 | nessuna |
| H3 Assessment | Intervistatore | H3 | nessuna |
| H4 Ambassador | Mattia con un tetto di token più alto in LiteLLM | H3 | nessuna |
| H5 Tutti costruiscono | ognuno possiede almeno un profilo | H3 | nessuna |
| H6 Premio mensile | classifica in Grafana dal registro | H3 | voucher 50-100 €/mese |
| H7 Cambiare modo di lavorare | i rituali sopra | n.a. | nessuna |

### 7.10 I. Qualità e limiti

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| I1-I2 Il contesto fa la qualità | quattro case e una porta di ricerca | H2 | nessuna |
| I3 Aree senza AI | classi negate nel Cancello e blocchi del plugin `pre_tool_call` | H1 | nessuna |
| I4 Marketing più creativo | squadra Marketing | H1 | nessuna |

### 7.11 K. Dettagli resi espliciti

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| K1 Debrief come primo appuntamento | evento in Outlook creato dall'esecutore | H1 | nessuna |
| K2 Un agente fissa le call trovate dagli altri | passaggio verso Agente agenda; annuncio in `#agenti` | H2-H3 | nessuna |
| K3 Posta smistata con risposte pronte | Smistatore posta su caselle limitate con il RBAC di Exchange | H2 | consenso di ciascuno |
| K4 Cosa si è detto in una call | Claude Team con l'MCP RAG; Bibliotecario e Capo di gabinetto in Teams | H2 | regola sui dati rossi verso Claude Team [ricerca/29 §8.5] |
| K5 Intake e onboarding dei prospect | Agente intake, anche su WhatsApp | H2 | WhatsApp come eccezione |
| K6 Slide con la storia della relazione | Agente brief e Agente slide | H2 | nessuna |
| K7 Nostro stile | template SerSan in SharePoint | H1 | nessuna |
| K8 Portale clienti con Claude Code | SersanOutreach come portale, cruscotto della pipeline | H4 | nessuna |
| K9 Newsletter | Agente newsletter con listmonk; invio dopo il sì | H3 | relay SMTP esterno da scegliere e prezzare |
| K10 Andrea in entrata ed esito | gruppo di squillo in Asterisk, poi Andrea; esito nel CRM | H4 | operatore italiano |
| K11 Perché si chiude e lead simili | Analista vinto/perso e Agente clienti simili | H2-H4 | volumi |
| K12 Formazione dei commerciali | Coach vendite, piano mensile | H4 | parere legale |
| K13 Mappa e assessment per i clienti | Mappatore e Intervistatore, poi offerta | H3-H5 | nessuna |
| K14 Finanza e obiettivi nella memoria | numeri di Sirius in Postgres via n8n; testi in Qdrant `finanza` | H2-H6 | sapere cos'è Sirius e cosa esporta |
| K15 Acquisti automatizzati | Agente acquisti e abbonamenti | H6 | nessuna |
| K16 Assistente personale | istanza Hermes personale, Graph delegato al solo calendario della persona, salute mai | H6 | consenso della persona |

### 7.12 L. Automazioni in più

| Voce | Come | Fase | Lacuna e cosa serve |
|---|---|---|---|
| L1 Contratto con firma elettronica | Agente contratti; DocuSeal self-hosted; link di firma dietro Pangolin | H6 | valore legale della firma semplice in Italia e UK da chiarire nel parere legale [non verificato] |
| L2 Fatture, incassi, solleciti | esecutore verso lo strumento contabile in uso | H6 | quale strumento usa Sersan Limited (forse Sirius); in mancanza, uno self-hosted come Invoice Ninja, licenza da verificare (GitHub la indica come "Other") [verificato: API GitHub, 25/10/2026] |
| L3 Margini, cassa, obiettivi | Controllo di gestione su Postgres | H6 | export strutturato di Sirius |
| L4 Bandi | pipeline bandi del board più Agente bandi | H2 | nessuna |
| L5 Assistenza nella stanza del cliente | Assistenza clienti su Teams, mail o WhatsApp | H6 | nessuna |
| L6 Rinnovi e clienti a rischio | Agente rinnovi | H6 | nessuna |
| L7 Casi studio | Agente casi studio | H6 | nessuna |
| L8 Commenti della pagina aziendale | Community manager; risposte dopo la carta | H3 | lettura dei commenti: API di LinkedIn con accesso approvato o strumento di terzi (Metricool) [non verificato] |
| L9 Sito e SEO | pull request sul repository del sito; deploy dopo il sì | H6 | nessuna |
| L10 Webinar ed eventi | Agente eventi; webinar in Teams | H6 | funzioni webinar del piano M365 di SerSan da verificare [non verificato] |
| L11 Agente che sorveglia il server | Sistemista sullo stack OBSRV, in sola lettura | H2 | regola APPS → OBSRV in lettura da scrivere |
| L12 Allenatore AI | profilo in direzione | H6 | nessuna |

### 7.13 Le lacune, in una tabella

| Lacuna | Cosa serve | Costo | Etichetta |
|---|---|---|---|
| GPU piena di giorno, assente la sera | seconda GPU RTX 2000 Ada 16 GB | 837-946 € IVA inclusa | [verificato: ricerca/32 §4.3] |
| RAM a regime | +192 GB (12 × 16 GB) | 816 € (2133, UE) - 1.218 € (2666, Bargain), IVA esclusa | [verificato: ricerca/32 §2.4] |
| Numero e chiamate di Andrea | operatore italiano | 44-90 €/mese | [non verificato: calcolo di ricerca/33 §2.3] |
| Invio della newsletter | relay SMTP | da preventivare | [non verificato] |
| Esposizione senza porte aperte | VPS o porte verso EDGE | circa 6 €/mese per un VPS | [verificato: hetzner.com, 25/10/2026] |
| Chat con Slack | eccezione di Michele | 27 €/mese Slack Pro × 4 | [verificato: PRESENTAZIONE-CEO §12.1, 24/10/2026] |
| Strumenti commerciali | eccezioni di Michele | fino a 187,62 €/mese | [verificato: ricerca/33 §2.5] |
| Firma elettronica valida | parere legale; DocuSeal o servizio in cloud | 0 € di licenza con DocuSeal | [non verificato] |
| Fatturazione | sapere lo strumento in uso | da chiarire | [non verificato] |
| Identità della persona verso l'MCP RAG | identità per istanza più allowlist; domande personali via Claude Team | 0 € | [verificato: docs MCP di Hermes] |
| WhatsApp oltre 24 ore | modelli inviati dall'esecutore del Cancello o da n8n | a messaggio | [verificato: ricerca/27 §5] |
| Sirius sconosciuto | domande a Michele | n.a. | [verificato: ricerca/29 §8.1] |

---

## 8. Piano per fasi

### 8.1 Le fasi

**Capacità ipotizzata:** circa 6,5 gp a settimana fra Alberto, Mattia e Michele [non verificato: ipotesi di ricerca/22 §5]. **Non contate:** le fasi F0-F4 del board (OPNsense e VLAN, Proxmox, NetBird, Traefik, Pangolin, PBS, uscita da Azure, sicurezza, LXC GPU, pipeline Sirius → MCP, Firecrawl e n8n per i bandi, installazione di LiteLLM), che porta avanti Michele [verificato: board, roadmap]. **Calendario:** il board non ha date; ipotizzo F0-F1 nelle settimane 1-4, F2 nelle 5-7, F3 nelle 8-10, F4 nelle 11-14 [non verificato: ipotesi da far confermare a Michele].

| Fase | Settimane | Prerequisito del board | Cosa si fa | gp base | gp con riserva | Cosa si vede alla fine |
|---|---|---|---|---|---|---|
| **H0 Preparazione e valore subito** | 1-4 | nessuno (in parallelo a F0-F1) | nucleo del Cancello in CI (registro, regole, classi, outbox, audit, stop); registro dei profili e repository delle skill in git; plugin `sersan-guardrail` scritto e provato in locale; impostazioni Teams per le trascrizioni (accesso Graph, nomi dei parlanti, criteri); informativa e DPIA; marketing con Claude Team | 13,5 | 18 | Cancello che passa i test; 10 profili scritti; Teams pronto per le trascrizioni |
| **H1 Posto agenti e pilota** | 5-11 | F2 (apps in casa) più un "posto agenti" anticipato: VM agenti, LiteLLM minimo, PostgreSQL, Infisical; solo dati verdi e gialli finché F3 non è validata | 3 istanze Hermes (commerciale, marketing, direzione) fissate per digest; LiteLLM; Teams per istanza; aggancio al Cancello; bot delle carte con lo spike di un giorno; raccoglitore delle trascrizioni Teams in n8n; esecutori Outlook e calendario; 10 profili: post-call, analista chiamate, debrief, capo di gabinetto, editoriale, copywriter, ricerca concorrenza, analista metriche, pubblicatore, agente task (Jira); stage con 10 scenari | 35,5 | 47 | dopo una call Teams: riassunto, to-do in Jira, bozza della mail in carta sul telefono; debrief alle 7:00; numeri del lunedì; **verifica della settimana 11** (§10.3) |
| **H2 Memoria, call e vendite** | 12-20 | F3 validata (dati rossi), F4 (LXC GPU, pipeline, LiteLLM con budget) | MCP RAG con le identità di istanza; MCP memoria e BookStack; ingressi della pipeline; oscuramento dei blocchi rossi; Vexa, trascrizione nei tre modi, lotti, telefono; prova di qualità; outbound con SersanOutreach; brief, slide, proposte, agenda, intake, smistatore, bibliotecario, archivista, sistemista, bandi; esecutori del CRM e stop di Instantly; istanza progetti | 43 | 57 | brief la sera prima; bozza d'offerta entro un'ora; la memoria risponde ad almeno 8 su 10 di 50 domande; bot nelle call dei clienti che li ammettono |
| **H3 Squadre collegate e organizzazione** | 21-23 | nessuno nuovo | MCP passaggi fra istanze con freno e specchio in `#agenti`; 6 istanze; banca dei token per persona; organigramma in Grafana; skill che migliorano con revisione; project manager, report cliente, onboarding, sviluppatori, mappatore, intervistatore, newsletter (listmonk), community manager; avvisi Telegram | 14,5 | 19,5 | gli agenti si passano il lavoro fra squadre sotto i nostri occhi; organigramma con i costi |
| **H4 Vendite e voce** | 24-30 | RAM +192 GB; parere legale; lead vere | Andrea su CPU (Asterisk, Pipecat, operatore, consenso e Registro nel Cancello); fit score, coach, pipeline pesata, clienti simili; WhatsApp per i clienti con i modelli via Cancello | 33 | 44 | una lead di prova richiamata entro 90 secondi, appuntamento nel CRM |
| **H5 Lab, scala e seconda GPU** | 31-34 | F5 (Experimental, seconda GPU, UPS rack) | seconda GPU e Andrea fase 2; trascrizione 24 ore su 24; pilota Buzz con Hermes via ACP in LAB; pilota Paperclip in LAB; prime regole "Sempre"; Slack se approvato | 11,5 | 15,5 | voce migliore; decisione scritta su Buzz e Paperclip; prima regola "Sempre" |
| **H6 Le altre automazioni** | 35-42 | nessuno nuovo | amministrazione (fatture, acquisti, controllo di gestione); contratti con DocuSeal; assistenza clienti, rinnovi, casi studio; sito e SEO; eventi; allenatore AI; assistente personale | 20 | 26,5 | dal contratto all'incasso senza lavoro a mano; organigramma verso i sessanta agenti |
| **Totale H0-H5** | **1-34** | | | **151** | **201** | |
| **Totale con H6** | **1-42** | | | **171** | **227,5** | |

Tutte le cifre in gp: [non verificato: stime costruite sui rapporti 26, 27, 28, 29, 30 e 31, dettaglio in §8.2].

**Perché più del piano precedente.** La presentazione stimava 110-147 gp per le fasi 0-5 [verificato: PRESENTAZIONE-CEO §15]. Qui entrano in casa pezzi che prima erano abbonamenti: le call senza Recall.ai (22-29 gp), Andrea senza ElevenLabs (circa 24 gp), le carte su Teams con un bot nostro, i connettori della memoria al posto di Notion [verificato: ricerca/30 §11, ricerca/31 §11, ricerca/28 §9, ricerca/29 §10].

**Il conflitto con il board.** Il board porta LiteLLM e la GPU nella fase F4 [verificato: board]. Senza il "posto agenti" anticipato, H1 aspetta F4 e tutto slitta di circa 4-7 settimane [non verificato: stima sulle ipotesi di calendario]. È la prima domanda per Michele (§12).

### 8.2 Da dove vengono i giorni

| Pacchetto | gp base | Fase | Fonte della stima |
|---|---|---|---|
| Nucleo del Cancello | 9 | H0 | [non verificato: ricerca/22 §5] |
| Registro dei profili, skill, plugin `pre_tool_call` | 2,5 | H0 | [non verificato: stima mia] |
| Impostazioni Teams per le trascrizioni; informativa e DPIA | 2 | H0 | [non verificato: ricerca/30 §11, lavori 1 e 12] |
| Integrazione Hermes: container e rete 1,5; LiteLLM 1,5; MCP 1; n8n 1,5; Teams 2,5; aggancio al Cancello 2,5; stage e aggiornamenti 2,5; osservabilità 1,5 | 14,5 | H1 | [non verificato: ricerca/27 §10, righe 1-5, 8, 10, 11] |
| Cancello v1: approvatori 2; porta dei modelli 1; bot delle carte 3,5; spike 1 | 7,5 | H1 | [non verificato: ricerca/22 §5; ricerca/28 §9] |
| Raccoglitore Teams e aggancio al post-call | 3,5 | H1 | [non verificato: ricerca/30 §11, lavori 2 e 9] |
| 10 profili pilota (0,6 gp l'uno) e Jira | 7,5 | H1 | [non verificato: stima mia; Jira da ricerca/29 §10] |
| Esecutori Outlook e calendario via Graph | 2,5 | H1 | [non verificato: ricerca/29 §10] |
| MCP RAG con identità di istanza e prove dei confini | 2 | H2 | [non verificato: ricerca/27 §10, riga 3] |
| MCP memoria, MCP BookStack, ingressi della pipeline | 7,25 | H2 | [non verificato: ricerca/29 §10] |
| Modulo call: agenda, VM meet, trascrizione, Vexa, lotti, telefono, prove, esercizio | 19 | H2 | [non verificato: ricerca/30 §11] |
| 17 profili (0,6 gp l'uno) | 10 | H2 | [non verificato: stima mia] |
| Esecutori del CRM e stop di Instantly | 2 | H2 | [non verificato: stima mia] |
| Oscuramento dei blocchi rossi con prova di qualità; agente bandi | 2,5 | H2 | [non verificato: stima mia] |
| MCP passaggi, freno e specchio | 3 | H3 | [non verificato: come la bacheca di ricerca/26 §10.2] |
| Da 3 a 6 istanze | 1,5 | H3 | [non verificato: ricerca/27 §10, riga 9, estesa] |
| Banca dei token per persona, organigramma, skill con revisione, Telegram | 3,5 | H3 | [non verificato: stima mia] |
| 8 profili e listmonk | 6,5 | H3 | [non verificato: stima mia] |
| Andrea fase 1 | 24 | H4 | [non verificato: ricerca/31 §11] |
| Coach, fit score, pipeline pesata, clienti simili | 5,5 | H4 | [non verificato: stima mia] |
| WhatsApp con Hermes e modelli via Cancello | 3,5 | H4 | [non verificato: ricerca/27 §10, riga 7, più 1,5] |
| Seconda GPU e Andrea fase 2 | 4,5 | H5 | [non verificato: ricerca/31 §11; ricerca/30 §11.1] |
| Pilota Buzz con Hermes | 4 | H5 | [non verificato: ricerca/28 §9] |
| Pilota Paperclip; regole "Sempre" | 3 | H5 | [non verificato: stima mia] |
| Amministrazione, contratti, assistenza, rinnovi, casi studio, sito, eventi, allenatore, assistente personale | 20 | H6 | [non verificato: stima mia, in linea con i 20-26 gp di PRESENTAZIONE-CEO §15] |

**Manutenzione dopo l'avvio.** Hermes: 1,5-2,5 gp al mese per stare nei 14 giorni di Cyber Essentials, verso l'estremo alto con più istanze [non verificato: ricerca/27 §8]. Con sei istanze sulla stessa immagine la prova si fa una volta; stimo 2-3 gp al mese [non verificato]. Modulo call: circa 0,5 gp al mese [non verificato: ricerca/30 §11.1]. Il resto del sistema: 1-2 giorni a settimana, come nel piano precedente [verificato: PRESENTAZIONE-CEO §15].

---

## 9. Costi

### 9.1 Quanto spendiamo in più rispetto a oggi

Stesso metodo di PRESENTAZIONE-CEO §12.1 e di ricerca/33 §3.1: costi nuovi, senza il kit commerciale, API dentro i crediti, Claude Team gratuito nel primo anno. Hermes non aggiunge canoni: licenza MIT, nessun servizio Nous [verificato: ricerca/27 §2.1; ricerca/33 §2.6].

| Periodo | € al mese in più | Cosa comprende | Etichetta |
|---|---|---|---|
| H0, F0-F1, Azure accesa | ≈ 135,27 | Proxmox Community 20,00 + IP fisso 10,00 + corrente 105,27 | [non verificato: ricerca/33 §3.1] |
| Dopo lo spegnimento di Azure (F2) | ≈ -14,73 | meno circa 150 € di Azure | [non verificato: idem; costo reale di Azure non nei file] |
| H1-H3, agenti al lavoro | ≈ 13,54 | più Jira Standard 28,27 | [non verificato: idem] |
| H4, con Andrea | ≈ 103,97 (≈ 57,78 con il piano PRO) | più 90,43 a consumo (44,24 con il PRO) | [non verificato: idem] |
| H5, seconda GPU accesa | + 2,55-7,66 | 10-30 W medi a 0,35 €/kWh | [non verificato: ricerca/32 §5.2] |
| Fine dell'anno gratuito di Claude Team | + 446,70 (5 premium) | invariato rispetto alle altre proposte | [verificato: ricerca/33 §2.2, claude.com/pricing/team del 25/10/2026] |
| Senza crediti API | + 195,65 | stima per un motore con sessioni e cache | [non verificato: ricerca/22 §6] |
| Instantly, se non è già pagato | + 69,33 | Hypergrowth annuale | [verificato: ricerca/33 §2.2, instantly.ai del 25/10/2026] |

**Una nota sui token.** La stima API (195,65 €/mese nel consigliato) vale per Hermes come per l'Agent SDK [verificato: ricerca/33 §2.6]. Hermes però mette nel prompt memoria, indice delle skill e schemi degli strumenti; con la cache attiva il peso scende. Se gli alias in LiteLLM non contengono "claude", la cache non parte e il conto sale [verificato per la cache: ricerca/27 §3.1; effetto sul conto non verificato]. Va misurato nella fase H1.

### 9.2 Listino mensile e integrazioni da tenere

| Voce | € al mese | Etichetta |
|---|---|---|
| **Listino consigliato** (nuovo 58,27; API 195,65; corrente e firewall 105,27; Andrea 90,43; Instantly 69,33) | **518,95** | [non verificato: ricerca/33 §3.2] |
| Slack Pro × 4, se approvato (J9) | + 27,00 | [verificato: PRESENTAZIONE-CEO §12.1, prezzo del 24/10/2026] |
| Claude in Slack con tetto, solo con Slack | + 44,67 | [verificato: idem] |
| WhatsApp verso i clienti, circa 300 messaggi utility | + 7-12 | [non verificato: ricerca/28 §9] |
| Apollo | + 43,78 | [verificato: ricerca/33 §2.5, prezzi del 24/10/2026] |
| Metricool (0 se si sceglie Postiz in casa) | + 59,86 | [verificato: idem] |
| moda.app (0 se bastano Claude e i template) | + 26,80 | [verificato: idem] |
| Higgsfield | + 41,99 | [verificato: idem] |
| Apify (0 con Firecrawl in casa) | + 15,19 | [verificato: idem] |
| Perplexity | costo non trovato | [verificato: ricerca/25 N08] |
| VPS per Pangolin e NetBird, se scelto | + 5,99 | [verificato: hetzner.com/cloud, 25/10/2026] |
| Utente di servizio M365, se serve | + 6,41 | [non verificato: ricerca/28 §9] |
| Relay SMTP per la newsletter | da preventivare | [non verificato] |
| **Tutte le integrazioni fuori board** | **fino a circa + 284** | [non verificato: somma delle righe con un prezzo, WhatsApp a 12 €] |

### 9.3 Una tantum

**Subito (H0, fasi F0-F1 del board)**

| Voce | Importo IVA esclusa | Etichetta |
|---|---|---|
| PBS a casa: M920t, 2 HDD, SSD per i metadati | 382-967 € | 382-730 € [non verificato: ricerca/33 §4.1]; fino a 640-1.180 € IVA inclusa (circa 525-967 € netti) con dischi da 8 TB e SSD dei metadati [non verificato: ricerca/32 §7, conversione mia] |
| Chiavi FIDO2, 8 chiavi | 232-464 € | [verificato: ricerca/33 §4.1, yubico.com del 25/10/2026] |
| Parere legale unico | tetto 2.500 € | [verificato: PRESENTAZIONE-CEO §14] |
| Piccoli accessori | 0-200 € | [non verificato: ricerca/25 §5.3] |
| Credito API prepagato, se servono | 0-223 € | [verificato: ricerca/33 §4.1] |
| **Subtotale** | **≈ 3.114-4.354 €** | [non verificato: somma] |

Hermes non ha costi una tantum. Il pagamento del server ("Pagare Bargain") non è nei file [verificato: board, F0].

**Più avanti (H4-H5)**

| Voce | Importo | Etichetta |
|---|---|---|
| Seconda GPU RTX 2000 Ada 16 GB | 686-775 € netti (837-946 € IVA inclusa) | [verificato: ricerca/32 §4.3; netti: calcolo mio] |
| Staffa ad altezza piena; riser secondario se manca | circa 8-90 € netti | [non verificato: ricerca/32 §8] |
| UPS rack Eaton 5PX 1500 G2 | 937-1.144 € | [verificato: ricerca/32 §6] |
| **Subtotale senza RAM** | **≈ 1.631-2.009 €** | [non verificato: somma] |
| RAM +192 GB, prima di H4 | 816-1.218 € | [verificato: ricerca/32 §2.4] |
| **Subtotale con RAM** | **≈ 2.447-3.227 €** | [non verificato: somma] |
| Attivazione del numero di Andrea | 7-14 € | [verificato: ricerca/33 §4.1] |
| Vivavoce da sala per le riunioni dal vivo (facoltativo) | 100-250 € | [non verificato: ricerca/30 §7] |

---

## 10. Rischi e come si esce

### 10.1 Rischi

| Rischio | Effetto | Come lo gestiamo | Etichetta |
|---|---|---|---|
| Gateway unico: 276 problemi aperti, 9 di sicurezza, 0 risolti su `main` | conversazioni o avvisi al profilo sbagliato, segreti di un profilo usati da un altro | un'istanza per confine di fiducia; un solo bot per istanza; niente app desktop; niente chat di gruppo ospitate dal gateway; criteri della verifica | [verificato: issue #143547, 25/10/2026]; contromisure [proposta, ricerca/27 §6.3] |
| `gateway.standalone` è uno "shim" temporaneo e la topologia per profilo è ritirata | separare i profili dentro un'istanza non è più sostenuto | separazione per container, che la documentazione ammette per segmentazione e conformità | [verificato: docs multi-profile-gateways e Docker di Hermes] |
| Patch entro 14 giorni con release frequenti e poco documentate (44 release dal 12/3, 8 in ottobre; almeno 45 avvisi nel 2026) | rischio di fallire Cyber Essentials o di rompere qualcosa a ogni salto | 2-3 cicli al mese su stage con 10 scenari; immagine per digest; se una patch critica non esce in tempo, si spengono le rotte pubbliche dell'istanza esposta | [verificato: ricerca/27 §7-8]; procedura [proposta] |
| Catena di fornitura (catalogo MCP di Hermes su ramo modificabile, CVE-2026-82021; versioni compromesse di LiteLLM a marzo 2026) | codice estraneo sul server | niente catalogo MCP di Hermes: solo i nostri MCP fissati per commit; LiteLLM fissato e verificato | [verificato: ricerca/27 §7.1]; LiteLLM [non verificato: ricerca/27 §3.2] |
| Identità della persona non passa all'MCP RAG | chi parla con un'istanza vede ciò che vede l'istanza | identità minima per istanza; `TEAMS_ALLOWED_USERS`; domande personali via Claude Team, che passa la persona | [verificato: docs MCP e Teams di Hermes] |
| Carte di Hermes con "Always Allow" | un tocco rende permanente un permesso | le azioni di business non passano dal gate di Hermes; terminale spento | [verificato: docs Teams di Hermes] |
| Buzz approva da solo le richieste di Hermes | esecuzione senza persona | pilota solo in LAB, senza dati dei clienti, terminale e codice tolti, accesso "Owner only" | [verificato: docs ACP di Hermes] |
| Problemi Hermes-LiteLLM (sonde 401, alias, MP-19/23/25, KB-11) | turni falliti o cache spenta | prova di accettazione; cache automatica di LiteLLM accesa; riserva solo in stage con chiave diretta limitata | [verificato: ricerca/27 §3.2] |
| Bug Teams di Hermes: documenti non inviabili (#113578), risposte fuori thread (#97068) | file e thread scomodi | i file li condivide l'esecutore del Cancello con un link SharePoint | [verificato: ricerca/27 §5]; contromisura [proposta] |
| Kanban su un solo host | niente passaggi diretti fra istanze | MCP passaggi in Postgres | [verificato: docs kanban di Hermes] |
| Chiamate verso Nous con l'account ospite | dati fuori perimetro | allowlist d'uscita e controllo del NetFlow | [non verificato: da misurare] |
| RAM a regime | VM che non partono | RAM +192 GB prima di H4; tetto ARC a 12 GiB; tetti di lavori per istanza | [non verificato: §3.5] |
| GPU la sera | niente trascrizione dal vivo e voce più povera | CPU la sera; seconda GPU in H4 | [verificato: board; ricerca/30 §6] |
| Esposizione pubblica senza porte aperte | bot, WhatsApp e MCP RAG non raggiungibili | VPS o porte verso EDGE, decide Michele; "Bypass Auth" solo per percorso | [verificato: docs Pangolin; ricerca/25 N10] |
| Due linguaggi (Hermes in Python, Cancello in TypeScript) | più cose da sapere per due persone | il plugin Python è piccolo e chiama l'API HTTP del Cancello | [verificato: Python 3.14 per Hermes, ricerca/10 §2; TypeScript per il Cancello, ricerca/22 §2] |
| Nessuno di noi conosce Hermes a fondo | errori di configurazione | pilota con 3 istanze, runbook, Mattia co-manutentore | [verificato: ricerca/26 §9] |
| Funnel vuoto | poco valore da misurare | marketing dalla fase H0; Andrea solo con lead vere | [verificato: ricerca/22 §1] |
| Modi automatici di SersanOutreach | inviti che non passano dal Cancello | spenti, o regola "Sempre" del Cancello | [verificato: ricerca/01 riga 45] |

### 10.2 Le uscite, se qualcosa non regge

| Uscita | Quando | Cosa si perde | Cosa resta | Costo |
|---|---|---|---|---|
| **A. Motore sull'Agent SDK al posto di Hermes** | un criterio della verifica fallisce, o un avviso critico resta senza patch oltre i 14 giorni | configurazione delle istanze, plugin Python, uso della kanban e degli adattatori di Hermes | Cancello e suo bot, LiteLLM, n8n, MCP, memoria, skill (stesso formato `SKILL.md` di Claude Code), modulo call, Andrea, registro dei profili | 17,5-21 gp di base (circa 23-28 con riserva), 3-4 settimane [non verificato: ricerca/26 §10.2 meno i pezzi già fatti] |
| **B. Hermes solo per i canali** | i profili reggono male, ma Telegram, WhatsApp e Slack servono | orchestrazione in Hermes | Hermes come porta dei canali verso un runner sull'SDK | circa 12-15 gp di base [non verificato: stima] |
| **C. Hermes solo come pilota confinato** | i problemi di sicurezza del gateway restano aperti | Hermes nel percorso dei clienti | tutto il resto, Hermes in Experimental-2 con dati verdi | pilota 6-8 gp [non verificato: ricerca/27 §10] |
| Bot Teams senza Azure non funziona | spike di H1 | n.a. | Azure Bot F0 a 0 € o pagina del Cancello | 0 € [verificato: ricerca/28 §2.2] |
| Vexa non regge | prova sul campo di H2 | n.a. | Attendee come piano B (non per Teams con login), registrazione sul PC | 2-3 gp [non verificato: ricerca/30 §11.1] |
| Voce italiana su CPU non basta | prova d'ascolto di H4 | n.a. | seconda GPU; in ultima istanza un TTS in cloud come eccezione | [non verificato: ricerca/31 §13] |
| "Illimitato" dell'operatore non vale per un agente | prima di firmare | n.a. | piano a consumo | circa 90 €/mese invece di 44 [non verificato: ricerca/33 §2.3] |
| MinIO non più mantenuto | prima che ci vadano file degli agenti | n.a. | Garage o SeaweedFS | 0 € di licenza [non verificato: ricerca/33 §2.7] |
| MCP di BookStack di comunità | se la revisione del codice non convince | n.a. | un MCP nostro con 6-8 strumenti | 1,5-2 gp [non verificato: ricerca/29 §3.2] |

### 10.3 La verifica della settimana 11 (fine di H1)

Hermes resta l'orchestratore e si passa a H2 (con i dati dei clienti) solo se, in due settimane di misura [non verificato: criteri proposti, sul modello di ricerca/22 §5 e ricerca/26 §10.4]:
1. zero conversazioni o avvisi finiti al profilo o al bot sbagliato, con almeno 3 istanze e 10 profili attivi;
2. zero effetti usciti senza una carta del Cancello;
3. una carta lasciata in attesa per una notte sblocca la card giusta al mattino;
4. un aggiornamento di Hermes passa i 10 scenari su stage senza interventi a mano, entro 14 giorni dalla release;
5. la cache dei prompt legge davvero (letture in cache sopra zero in LiteLLM) e la spesa sta nel tetto; `/insights`, LiteLLM e Console differiscono meno del 10 %;
6. nessuna chiamata verso domini Nous nel NetFlow;
7. le carte sono decise entro 24 ore (criterio commerciale, che dipende da noi).

Per mettere dati rossi in Hermes, in più, le quattro condizioni di ricerca/27 §11: v0.23 uscita con note complete; righe di sicurezza MSG-43, GW-41, KB-10 e HR-6 chiuse su `main`; bug #113578 chiuso; un aggiornamento che passa i 10 scenari [verificato: ricerca/27 §11]. Se non valgono, i dati rossi restano agli agenti che non girano in Hermes (post-call a schema senza strumenti, chiamato da n8n) finché non valgono [non verificato: proposta].

---

## 11. Hermes o Agent SDK in questo board

| Criterio | Proposta 2 (Hermes) | Motore sull'Agent SDK (ricerca/26) | Etichetta |
|---|---|---|---|
| Profili, kanban, skill che crescono | pronti | da scrivere (circa 4,5 gp) | [verificato: ricerca/26 "In breve"] |
| Canali | Teams, Telegram, WhatsApp, Slack pronti | Chat SDK da integrare | [verificato: ricerca/27 §9.2] |
| Aggancio al Cancello | plugin `pre_tool_call` con `block`, fail closed | hook `PreToolUse` con `defer` nativo | [verificato: docs hooks di Hermes; ricerca/26 §2] |
| Identità della persona verso l'MCP RAG | per istanza | per persona | [verificato: ricerca/27 §9.4] |
| Isolamento | un container per confine di fiducia | cartella, configurazione e chiave per agente | [verificato: ricerca/26 §3.4; docs Docker di Hermes] |
| Bug aperti noti | 276 nel gateway unico, 9 di sicurezza | nessun bug noto di sessioni scambiate | [verificato: issue #143547; ricerca/26 §9] |
| Avvisi di sicurezza | almeno 45 nel 2026, nessuno pubblicato dal repository | pacchetto npm che esce quasi ogni giorno | [verificato: ricerca/27 §7; ricerca/26 §1.1] |
| Giorni del motore | 22,5 gp di base (forbice 20-25) | 21 gp di base | [non verificato: ricerca/27 §10; ricerca/26 §10.2] |
| Manutenzione | 1,5-2,5 gp al mese, di più con più istanze | aggiornamento ogni due settimane | [non verificato: idem] |
| Licenza e canone | MIT, 0 € | Commercial Terms, 0 € | [verificato: ricerca/33 §2.6] |

**Lettura.** La Proposta 2 vince sul tempo al primo valore e sulla ricchezza dei canali; perde sull'identità per persona, sulla sicurezza del gateway e sulla manutenzione [non verificato: giudizio]. Il resto del sistema (Cancello, memoria, call, Andrea, n8n, LiteLLM) è lo stesso nelle due proposte, quindi l'uscita A del §10.2 costa solo il motore.

---

## 12. Domande aperte

**Per Michele**
1. Accetti un "posto agenti" anticipato alla fine di F2 (VM agenti con Docker, LiteLLM minimo, PostgreSQL, Infisical), con soli dati verdi e gialli fino alla validazione di F3? Senza, H1 aspetta F4.
2. Le istanze Hermes nella VLAN 30 APPS o in una VLAN dedicata agli agenti? Con quanta RAM per la VM `agenti-01`?
3. Che stima in settimane dai alle fasi F0-F4?
4. Pangolin e NetBird su un VPS (circa 6 €/mese) o porte aperte solo verso EDGE con l'IP fisso? Ammetti le regole "Bypass Auth" per percorso su `/api/messages`, `/webhooks/whatsapp` e sul link di firma, e la regola CIDR sugli IP di Anthropic per l'MCP RAG?
5. Il bot "Teams-managed" senza Azure, oppure Azure Bot F0 gratuito, oppure la pagina del Cancello? Sei bot Teams (cinque istanze più il Cancello) vanno bene nel tenant?
6. Quali eccezioni ammetti: Slack, Telegram, WhatsApp, Apollo, Perplexity, Metricool o Postiz, moda.app, Higgsfield, relay SMTP, operatore telefonico?
7. Seconda GPU già in H4 (RTX 2000 Ada 16 GB) invece che in F5? RAM +192 GB prima di H4?
8. Che cos'è Sirius, cosa esporta e chi vede i suoi dati? Cosa sono mcp-memory, mcp-enrich e runner-dash?
9. MariaDB per BookStack nella VLAN DATA, e un sostituto di MinIO?
10. Regole da scrivere: APPS → DATA per l'MCP RAG verso Qdrant; APPS → OBSRV in lettura per il Sistemista.

**Per Alessandro**
11. Su quale piano sono oggi M365 (con o senza Teams, funzioni webinar) e Jira (Free o Standard)?
12. Quale strumento di fatturazione e contabilità usa Sersan Limited? Serve una firma elettronica qualificata o basta quella semplice con DocuSeal?
13. Andrea: chi firma con l'operatore, e Andrea richiama anche di notte?

**Da misurare nelle prove**
14. L'`aadObjectId` arriva nelle azioni delle carte del bot del Cancello?
15. `/kanban unblock` funziona anche da Teams, non solo da Telegram e Discord?
16. Senza login l'account ospite di Hermes chiama domini Nous?
17. Con alias "claude" la cache si legge davvero attraverso LiteLLM, e quanto costa un profilo Hermes al giorno rispetto alla stima?

---

## Fonti

Lette il 25/10/2026, salvo dove indicato.

**Board di Michele (vincolante)**
- `C:\Users\alber\SerSan-AgentOS\allegati\infra\SerSan Infra Board.md`
- `C:\Users\alber\SerSan-AgentOS\allegati\infra\board-testo-completo.txt`
- `C:\Users\alber\SerSan-AgentOS\allegati\infra\board-vlan.txt`

**Rapporti del progetto**
- `ricerca/00-visione-funzionalita.md` (voci A1-L12)
- `ricerca/01-sersanoutreach.md` (riga 45, modi automatici)
- `ricerca/10-hermes-agent.md` (24/10/2026, con la nota del 25/10)
- `ricerca/22-architettura-scelta.md`
- `ricerca/25-board-michele-e-delta.md`
- `ricerca/26-claude-agent-sdk.md`
- `ricerca/27-hermes-self-hosted.md`
- `ricerca/28-chat-di-gruppo-self-hosted.md`
- `ricerca/29-conoscenza-task-e-documenti.md`
- `ricerca/30-call-e-trascrizione-self-hosted.md`
- `ricerca/31-voce-andrea-self-hosted.md`
- `ricerca/32-hardware-e-upgrade.md`
- `ricerca/33-costi-v2.md`
- `PRESENTAZIONE-CEO.md` (§4, §5.4, §5.6, §11, §12, §14, §15, appendice A)

**Documentazione di Hermes Agent (pagine ufficiali)**
- https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks (`pre_tool_call`, timeout, fail closed)
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams (registrazione, `/api/messages`, porta 3978, allowlist, carte)
- https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways (gateway unico, `standalone`, `/p/<profilo>/`)
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban (SQLite per istanza, dispatcher, blocchi, revisione)
- https://hermes-agent.nousresearch.com/docs/user-guide/docker (container separati, digest, `/opt/data`, risorse, UID)
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp (`identity_header`, filtri, OAuth)
- https://hermes-agent.nousresearch.com/docs/user-guide/features/acp (Buzz come host ACP, approvazioni automatiche)

**GitHub (API)**
- https://api.github.com/repos/NousResearch/hermes-agent/releases (ultima v0.22.5 del 23/10/2026)
- https://api.github.com/repos/NousResearch/hermes-agent/issues/143547 (276 problemi, 9 di sicurezza, 0 risolti su main)
- https://api.github.com/repos/docusealco/docuseal
- https://api.github.com/repos/knadh/listmonk
- https://api.github.com/repos/gitroomhq/postiz-app
- https://api.github.com/repos/invoiceninja/invoiceninja

**Altre pagine**
- https://docs.pangolin.net/manage/access-control/rules (Bypass Auth, Block, Pass to Auth; percorsi, IP, CIDR)
- https://www.hetzner.com/cloud/ (piano Cost-Optimized da 5,99 €/mese IVA esclusa)
- Ricerca web del 25/10/2026 su Hermes, Buzz e ACP: https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/acp

**Strumenti**
- Context7: quota mensile esaurita il 25/10/2026; documentazione letta con WebFetch sulle pagine ufficiali.
