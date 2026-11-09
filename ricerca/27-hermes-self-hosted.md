# 27 · Hermes Agent tutto in casa, dentro il board di Michele

**Data:** 25/10/2026. **Per:** Alberto Tuveri, da girare a Michele Sanna.
**Cosa aggiorna:** il rapporto `10-hermes-agent.md` (24/10/2026) e la scelta di Hermes in `22-architettura-scelta.md`, alla luce del board dell'infrastruttura di Michele (`allegati/infra/`), che qui è vincolante.
**Etichette.** [verificato: fonte] = letto da me oggi sulla fonte indicata. [non verificato] = voce di terzi, riassunto di un motore di ricerca o stima mia, e lo dico. gp = giorni-persona. Tutte le rilevazioni web e GitHub sono del 25/10/2026, salvo dove scrivo un'altra data.

---

## In breve

Hermes Agent si può far girare tutto sul DL380, senza Hermes Cloud, senza Nous Portal e senza account Nous: l'immagine Docker è pubblica, la licenza è MIT e l'invio di metriche a Nous è spento di default [verificato: docs Docker; `config_defaults.py` su main]. Claude passa da LiteLLM con la chiave API, come un fornitore personalizzato in formato Anthropic; la cache dei prompt funziona solo se il nome del modello contiene "claude" [verificato: docs providers; issue #17332]. Il quadro però è cambiato dal 14 ottobre. La versione 0.22 ha messo tutti i profili in un solo gateway e ha ritirato l'opzione per tenerli separati. Oggi la scheda di tracciamento conta 273 problemi aperti, 9 di sicurezza e 48 proprio sui profili multipli; tra questi, i messaggi di un bot che finiscono nella chat di un altro bot [verificato: issue #143547, aggiornata il 25/10]. Nel 2026 il database di GitHub elenca almeno 45 avvisi di sicurezza su Hermes, uno critico e tre alti, mentre il repository non ne pubblica nessuno e le note di rilascio sono incomplete per scelta [verificato: GitHub Advisory Database; pagina Releases]. Con la regola di Cyber Essentials (patch entro 14 giorni) questo pesa: non si può restare fermi a lungo su una versione, e ogni salto di versione cambia molto. Nel board di Michele quasi metà delle funzioni di Hermes è doppia: le routine e i webhook li fa n8n, i modelli e i budget LiteLLM, la memoria Qdrant e l'MCP RAG, la chat web Open WebUI e Claude Team. Restano davvero suoi il gateway per Teams, Telegram e WhatsApp, i profili con skill che si migliorano, la bacheca dei compiti e la pipeline delle riunioni Teams. In più Hermes non sa passare all'MCP RAG l'identità della persona che scrive, solo un nome fisso o il nome del profilo: i "permessi per utente" del board valgono quindi per agente, non per persona [verificato: docs MCP]. Integrarlo bene in questo contesto costa circa 20-25 gp di base, 26-33 con la riserva del 30 %, più 1,5-2,5 gp al mese di manutenzione [stima]. Un motore nostro sull'Agent SDK, nello stesso contesto, sta nello stesso ordine di grandezza [stima]. La mia lettura: nel board di Michele Hermes non è necessario. Ha senso solo come pilota confinato (Telegram in polling, due o tre profili, sola lettura) oppure dopo che la v0.23 avrà chiuso i problemi di sicurezza del gateway unico.

---

## 1. Cosa è cambiato dal rapporto 10 (24/10 → 25/10)

| Fatto nel rapporto 10 | Stato oggi | Fonte |
|---|---|---|
| Ultima release v0.22.5 | Ancora v0.22.5, pubblicata il 23/10 alle 05:28 UTC; le note complete arriveranno con la v0.23.0, non ancora uscita | [verificato: GitHub API releases; pagina release v0.22.5] |
| 256.800 stelle, 58.403 commit | 256.899 stelle, 56.230 fork, 58.529 commit su `main`; ultimo push il 25/10 alle 06:57 UTC | [verificato: GitHub API e pagina del repository] |
| "5k+ issue e 5k+ PR aperte" | Il motore di ricerca di GitHub conta 17.066 issue aperte e 33.864 PR aperte; 2.420 commit nella settimana 18-24 ottobre | [verificato: GitHub search API]. Quante siano generate da bot di triage: [non verificato] |
| Bug #58032 (sessioni al profilo sbagliato) aperto | **Chiuso il 7/7/2026** con la PR #59325. Ma l'opzione che lo causava (`multiplex_profiles: false`) è stata **ritirata** | [verificato: issue #58032; docs multi-profile-gateways] |
| Bug #141623 (bot secondario non cancellabile) aperto | **Chiuso il 20/10/2026** | [verificato: GitHub API] |
| Bug #143150 (ripresa delle sessioni dopo la migrazione) aperto | Ancora aperto, aggiornato il 24/10 | [verificato: GitHub API] |
| Scheda #143547 sul gateway unico | Aperta: 273 problemi, 138 "rotti", 107 "degradati", 9 di sicurezza; al 24/10 nessuno risolto su `main`, 39 in revisione in 14 PR | [verificato: testo della issue #143547] |
| Più CVE nel 2026 | Almeno 45 avvisi nel GitHub Advisory Database dal 27/4 al 21/10/2026; 0 avvisi pubblicati nella pagina di sicurezza del repository | [verificato: github.com/advisories, pagine 1-2; github.com/NousResearch/hermes-agent/security/advisories] |
| Telemetria non trattata | "Shared metrics" verso `telemetry.nousresearch.com`, spente di default (`enabled: False`, `send: False`) | [verificato: `hermes_cli/config_defaults.py` e `hermes_cli/setup.py` su main] |
| Slack come chat | Nel board Slack e Notion non compaiono tra i servizi che restano; la chat aziendale è Teams (M365) | [verificato: board, sezione "Cloud & SaaS che restano"] |

---

## 2. Che cosa vuol dire "tutto in casa" nel board

### 2.1 Cosa si esclude

| Pezzo di Nous | Lo usiamo? | Perché | Fonte |
|---|---|---|---|
| Hermes Cloud | No | Istanza ospitata da Nous: è fuori dal perimetro del board | [verificato: board; rapporto 10 §8] |
| Nous Portal e "Tool Gateway" | No | Strumenti ospitati (ricerca, browser): li sostituiscono Firecrawl in casa e le chiavi nostre. Hermes accetta un Firecrawl self-hosted con `FIRECRAWL_API_URL` | [verificato: `website/docs/integrations/index.md` su main] |
| Hermes Relay | No | Connettore sperimentale che passa da un servizio esterno che tiene le credenziali | [verificato: docs messaging] |
| Hermes for Business | No | Tenant su infrastruttura Nous | [verificato: rapporto 10 §8] |
| Account Nous | Non serve | L'installazione documenta anche la via `hermes model` con fornitori propri | [verificato: docs installation] |
| Metriche condivise | Spente | Di default sono spente; l'endpoint non si può cambiare da variabile d'ambiente | [verificato: `config_defaults.py`, `shared_metrics_send_config.py` su main] |

Il codice resta MIT [verificato: rapporto 10 §2]. La v0.22.5 rifà il login Nous con un "account ospite" del piano gratuito [verificato: note v0.22.5]: va verificato sul posto che senza login non parta nessuna chiamata a Nous [non verificato]. La regola di rete che lo garantisce è l'allowlist in uscita della VLAN 30 (§2.3).

### 2.2 Dove gira

- **VLAN 30 APPS**, accanto a n8n, LiteLLM e Open WebUI, con "uscita su allowlist" [verificato: board-vlan.txt].
- **Contenitore Docker** `nousresearch/hermes-agent`, fissato per digest. Esistono tag `v0.22.5`, `stable` e `latest`; la documentazione dice che per un blocco esatto serve il digest [verificato: docs Docker; Docker Hub, 234 tag].
- Lo stato sta tutto in un volume (`/opt/data`: `.env`, `config.yaml`, sessioni, memorie, skill, log). Il volume va nel backup PBS [verificato: docs Docker].
- Il processo gira come utente `hermes` (UID 10000); il gateway rifiuta di partire come root [verificato: docs Docker].
- Regola da rispettare: mai due contenitori gateway sullo stesso volume [verificato: docs Docker].
- **Pilota possibile in Experimental-2** (VLAN 90 LAB: internet sì, nessun accesso a DATA) [verificato: board-vlan.txt]. È il posto giusto per provarlo con dati verdi senza toccare la memoria aziendale [stima].

### 2.3 Flussi di rete

| Flusso | Da → a | Porta e protocollo | Nota | Fonte |
|---|---|---|---|---|
| Modelli | Hermes (30) → LiteLLM (30) | HTTP interno, `/v1/messages` | Chiave virtuale LiteLLM per istanza | [verificato: docs providers; docs LiteLLM] |
| Memoria aziendale | Hermes (30) → MCP RAG (30) | HTTP MCP | Mai accesso diretto a Qdrant: la regola del board è "AI → DATA solo Qdrant" | [verificato: board] |
| Teams in ingresso | Bot Framework → Pangolin/Traefik (20) → Hermes (30) | HTTPS pubblico → HTTP `3978`, oppure `/p/<profilo>/api/messages` sull'ascoltatore condiviso `8642` | Teams rifiuta i certificati autofirmati; l'endpoint è autenticato dal JWT del Bot Framework | [verificato: docs teams; docs multi-profile-gateways] |
| WhatsApp in ingresso | Meta → Pangolin/Traefik (20) → Hermes (30) | HTTPS pubblico → `/whatsapp/webhook` | Firma con l'App Secret; senza, risponde 503 | [verificato: docs whatsapp-cloud] |
| Telegram | Hermes (30) → api.telegram.org | HTTPS in uscita (polling) | Nessuna porta in ingresso | [verificato: docs telegram] |
| n8n → Hermes | n8n (30) → Hermes (30) | API `8642` con chiave, oppure webhook `8644` con firma HMAC | | [verificato: docs Docker; docs webhooks] |
| Dashboard | NetBird admin → Hermes | `9119` | Autenticazione obbligatoria su ogni bind non locale | [verificato: docs Docker] |
| Uscite da permettere | Hermes → login.microsoftonline.com, servizi Bot Framework, graph.facebook.com, api.telegram.org | HTTPS | Nient'altro: niente PyPI, npm o GitHub in esercizio, perché gli aggiornamenti arrivano con l'immagine | [stima] |

**Attenzione al board.** Pangolin e Traefik mettono "autenticazione davanti" alle app [verificato: board]. I webhook di Teams e di WhatsApp non possono fare un login SSO: serve una regola che lasci passare solo quei percorsi, con la verifica affidata a JWT e firma. Che Pangolin lo permetta per percorso va verificato [non verificato].

### 2.4 Risorse

- Il board lascia circa 53 GB di RAM liberi [verificato: board, "Capacità"].
- L'esempio Docker ufficiale limita il contenitore a 4 GB e 2 CPU [verificato: docs Docker]. Con tre istanze separate (§6.3) servono circa 12-18 GB, browser spento [stima].
- La GPU non serve a Hermes [verificato: rapporto 10 §7]. Il Qwen3-4B del board non può fare da modello principale di un agente Hermes: Hermes vuole almeno 64.000 token di contesto per lavorare con gli strumenti e rifiuta l'avvio sotto quella soglia [verificato: docs providers]. Resta per i compiti brevi della pipeline [stima].

---

## 3. Claude via LiteLLM

### 3.1 Come si collega

- Hermes documenta LiteLLM come "OpenAI-compatible proxy", collegato come endpoint personalizzato [verificato: docs providers].
- Per restare nel formato Anthropic si usa un fornitore con nome nel blocco `providers:`, con `transport: anthropic_messages`, `api:` (indirizzo di LiteLLM), `key_env` o `key_cmd`, `default_model`, `models` e `context_length` [verificato: docs providers].
- `key_cmd` permette di leggere la chiave da un comando, per esempio dalla CLI di Infisical [verificato come esistenza della chiave: docs providers; l'uso con Infisical è una stima].
- LiteLLM espone `/v1/messages` nel formato nativo di Anthropic e lascia passare `cache_control`; la risposta riporta `cache_creation_input_tokens` e `cache_read_input_tokens` [verificato: docs.litellm.ai, native passthrough].
- **Cache dei prompt.** Hermes aggiunge i punti di cache sui gateway di terzi in `anthropic_messages` solo se il nome del modello contiene "claude" [verificato: issue #17332, che cita la PR #12846]. Quindi gli alias in LiteLLM devono contenere "claude" (per esempio `claude-sonnet-5-5`).
- Senza `transport` esplicito Hermes sceglie il formato OpenAI e la cache non parte; un articolo consiglia anche di togliere `/v1` dall'indirizzo [non verificato: blog di terzi su gitcode.csdn.net].
- **Rete di sicurezza in LiteLLM.** LiteLLM può aggiungere da solo i punti di cache per i modelli Claude: è spento di default, non raddoppia quelli già presenti e funziona sia su `/v1/messages` sia su `/chat/completions` [verificato: docs.litellm.ai, tutorial prompt caching]. Conviene accenderlo, per il bug KB-11 (§3.2).
- **Banca dei token.** Una chiave virtuale LiteLLM per istanza o per profilo, con budget: è la "LiteLLM con budget" della fase F4 del board [verificato: board, F4]. Ogni profilo Hermes ha il suo `.env`, quindi la sua chiave [verificato: docs profiles].
- Modelli già nel catalogo di Hermes dalla v0.22.0: Opus 5.5, Sonnet 5.5, Haiku 5.5 e Fable 5.1 [verificato: note v0.22.0].

### 3.2 Problemi noti su questa strada

| Problema | Effetto per noi | Stato | Fonte |
|---|---|---|---|
| #8465 "Proper Litellm support" | Il supporto LiteLLM è generico, non dedicato | Aperta dal 12/4/2026 | [verificato: GitHub API] |
| #133606: alias LiteLLM e lunghezza del contesto | Il valore `context_length` scritto a mano può essere ignorato | Aperta dal 6/10 | [verificato: GitHub API] |
| #133208 e #75479: sonde `/models` senza chiave | Errori 401 contro un LiteLLM con autenticazione | Aperte | [verificato: ricerca issue GitHub] |
| MP-19, MP-23, MP-25 nel gateway unico | Un fornitore personalizzato con nome "collassa" sul generico `custom`: turni falliti, ricaduta silenziosa o invio a un altro fornitore | In revisione nella PR #143593 | [verificato: commento della issue #143547] |
| KB-11 | I lavoratori della bacheca perdono il formato e l'indirizzo del fornitore | Aperto, riprodotto sulla v0.22.4 | [verificato: issue #143547; issue #141861] |
| 102 issue aperte che citano LiteLLM | Segnale di attrito, non di blocco | Aperte | [verificato: GitHub search API] |

**Rischio in comune con l'Agent SDK.** LiteLLM ha avuto due versioni compromesse su PyPI (1.82.7 e 1.82.8) a marzo 2026 [non verificato: riassunto di ricerca dell'avviso su docs.litellm.ai e di articoli di terzi]. Vale per entrambe le strade, perché LiteLLM è nel board comunque: versione fissata e immagine verificata.

### 3.3 Termini di Anthropic

- I piani Claude non si usano come motore di prodotti di terzi: per l'Agent SDK Anthropic scrive che non permette il login claude.ai "for their products, including agents built on the Claude Agent SDK" [verificato: code.claude.com/docs/en/agent-sdk/overview].
- Per Hermes il login OAuth Claude vale solo per Max con crediti extra [verificato: rapporto 10 §4.3].
- Quindi, con Hermes o con l'Agent SDK, gli agenti usano la chiave API dietro LiteLLM. I posti Claude Team restano alle persone [verificato: board, "Claude Team ragiona sul RAG via MCP"].

---

## 4. Convivenza con i servizi del board

| Servizio del board | Cosa fa Hermes di simile | Regola proposta | Fonte |
|---|---|---|---|
| **n8n** (cron, bandi, notifiche) | Cron in linguaggio naturale, webhook con firma HMAC (porta 8644, 30 richieste al minuto per rotta, corpo massimo 1 MB) | n8n tiene i lavori deterministici e le routine. Hermes fa solo i lavori a più passi. n8n chiama Hermes con l'API (`/v1/chat/completions`, `/v1/runs`) o con un webhook firmato; Hermes chiama n8n via webhook | [verificato: docs webhooks; rapporto 10 §4.2]; la divisione è una [stima] |
| **LiteLLM** | Rotazione delle chiavi, fornitore di riserva, modello per profilo | LiteLLM decide modelli, chiavi, budget e riserve. In Hermes niente `fallback_providers` | [verificato: rapporto 10 §4.3; board F4] |
| **Qdrant + MCP RAG** | Memoria interna piccola; un solo fornitore esterno alla volta (Mem0, Honcho, Hindsight e altri); Mem0 OSS può usare Qdrant | Nessun fornitore esterno in Hermes: una seconda memoria sarebbe un doppione. Hermes legge solo dall'MCP RAG | [verificato: docs memory-providers] |
| **Permessi per utente dell'MCP RAG** | `identity_header` manda un valore fisso o il nome del profilo, "resolved once at connect time" | L'MCP RAG vede l'agente, non la persona. Ogni istanza Hermes deve avere un'identità di servizio con i permessi minimi comuni a chi la usa | [verificato: docs MCP, "Per-user identity header"] |
| **mcp-memory, mcp-enrich, openoutreach** | Client MCP stdio e HTTP, OAuth 2.1, mTLS, filtri `tools.include` ed `exclude`, `trust: untrusted` chiede prima delle scritture | Solo gli strumenti in lettura nelle liste `include`; le scritture passano dal Cancello | [verificato: docs MCP] |
| **Firecrawl** in casa | `web_extract` con `FIRECRAWL_API_URL` | Hermes usa il Firecrawl del board, non strumenti ospitati | [verificato: docs integrations su main] |
| **Open WebUI** | API compatibile OpenAI; in Open WebUI compare un modello `hermes-agent` con una sola chiave condivisa | Va bene solo per chi ha gli stessi permessi: la chiave è unica | [verificato: docs.openwebui.com, pagina Hermes Agent] |
| **Infisical, Vaultwarden** | Segreti nel `.env` di ogni profilo | Le chiavi dei modelli con `key_cmd`; il resto nel `.env` del volume, mai leggibile da tutti | [verificato: docs providers; docs Docker] |
| **Prometheus, Grafana, Loki, Wazuh** | Esportatore OpenTelemetry, Langfuse, `/insights` | Tracce verso lo stack OBSRV; log del volume verso Loki e Wazuh | [verificato: rapporto 10 §4.2; `otlp_exporter.py` su main] |
| **Jira** | Bacheca kanban tra profili | Jira per le persone e i progetti; la bacheca di Hermes solo per i passaggi fra agenti, se Hermes resta | [stima] |
| **Experimental-2** (sandbox Linux con Docker) | Terminale in Docker | Nei profili aziendali il terminale e l'esecuzione di codice restano spenti. Il backend Docker richiederebbe il socket di Docker dentro il contenitore, cioè accesso da amministratore all'host | [stima] |
| **Claude Team** | Hermes può esporre le conversazioni come server MCP; dalla v0.22.5 è un plugin | Facoltativo | [verificato: note v0.22.5] |

---

## 5. I canali: Teams, Telegram, WhatsApp

| | Teams | Telegram | WhatsApp |
|---|---|---|---|
| Come arriva il messaggio | Webhook HTTPS pubblico su `/api/messages`, porta 3978, oppure `/p/<profilo>/api/messages` sull'ascoltatore condiviso | Polling in uscita; il webhook è facoltativo (porta 8443, segreto obbligatorio) | Solo con la Cloud API di Meta: webhook HTTPS pubblico. Il "bridge" Baileys usa un account personale e rischia il blocco del numero |
| Registrazione | CLI `@microsoft/teams.cli`: app Entra con client ID, segreto e tenant, "no Azure portal needed" | Un bot per profilo; lo stesso token non regge due polling | Account Meta Business, numero dedicato, token permanente di "System User" (gli altri scadono in 24 ore) |
| Chi può scrivere | `TEAMS_ALLOWED_USERS` con gli ID degli oggetti Entra | `TELEGRAM_ALLOWED_USERS`; senza lista, tutti negati | `WHATSAPP_CLOUD_ALLOWED_USERS`; senza lista, tutti negati |
| Gruppi | Nei canali risponde alle menzioni; con permessi RSC riceve tutto e serve `require_mention` | Privacy mode attiva di default; freno ai giri fra bot: pausa dopo 20 messaggi di bot in 5 minuti | Gruppi non supportati nella v1, solo chat dirette |
| Limiti noti | Un solo tenant; bug aperti: documenti non inviabili (#113578), risposte fuori dal thread (#97068), messaggi lunghi spezzati male (#124294); 40 issue aperte con "Teams" nel titolo | 673 issue aperte con l'etichetta Telegram | Fuori dalla finestra di 24 ore servono modelli approvati, e Hermes **non li invia**: un debrief programmato dopo 24 ore di silenzio fallisce (errore 131047). 192 issue aperte con l'etichetta WhatsApp |
| Adatto al board | Sì: M365 resta [verificato: board]. Serve però il percorso pubblico (§2.3) | Sì, è l'unico senza porte in ingresso. Non è nel board: va deciso | Sì per avvisi e approvazioni; no per routine lontane da un messaggio della persona |
| Fonti | [verificato: docs teams; GitHub API] | [verificato: docs telegram; GitHub search API] | [verificato: docs whatsapp-cloud; GitHub search API] |

**Riunioni Teams.** Hermes ha una pipeline che riceve gli eventi delle riunioni da Microsoft Graph, prende prima le trascrizioni e, se mancano, le registrazioni con trascrizione automatica, poi manda un riassunto a Teams, Notion o Linear [verificato: docs teams-meetings]. Servono un URL pubblico per i webhook di Graph e un lavoro programmato per rinnovare le sottoscrizioni, che Microsoft limita a 72 ore [verificato: docs teams-meetings]. La pagina non dice quali permessi Graph servono né se la funzione è sperimentale [verificato: docs teams-meetings]. È utile per A1 e J5 sulle riunioni Teams; lo stesso flusso si può costruire con n8n e Graph [stima].

**Slack.** Hermes si collegava a Slack senza URL pubblico [verificato: rapporto 10 §4.2]. Con Teams questo vantaggio sparisce: serve un ingresso pubblico, e il board non apre porte (§2.3).

---

## 6. Il bug noto: più profili sullo stesso gateway

### 6.1 Che cosa è cambiato con la v0.22.0

- Dal 14/10 "one backend and one gateway for every profile" [verificato: note v0.22.0].
- La PR #106742 ha spostato ogni conversazione locale (riga di comando, app, API, bot, cron, bacheca, chat di gruppo) in un unico processo gateway [verificato: issue #143547].
- `gateway.multiplex_profiles: false` "is retired": il gateway lo riscrive a `true`. Un gateway per profilo resta solo come "a temporary shim, not a supported topology" (`gateway.standalone: true`) o con `--force` [verificato: docs multi-profile-gateways].
- Il bug #58032 del rapporto 10 è chiuso [verificato: §1]. Ma la topologia che lo evitava non è più sostenuta.

### 6.2 I problemi aperti che contano per noi

Dalla scheda #143547 (273 problemi aperti, 206 confermati su `main`, 112 riprodotti dal vivo) [verificato: testo della issue]:

| Codice | Problema | Gravità per Nous | Stato |
|---|---|---|---|
| MSG-43 | Su un gateway con più bot Telegram, gli avanzamenti e gli avvisi di un profilo arrivano nella chat del bot di un altro profilo | sicurezza | Riprodotto dal vivo sulla v0.22.3 |
| GW-41 | Un turno può girare con la cartella di un profilo e i segreti o le regole del terminale di un altro | sicurezza | Lettura del codice, PR esterna da recuperare |
| KB-10 | Un compito della bacheca per un altro profilo può avviarne il gateway con i segreti del profilo che lo ha creato | sicurezza | Lettura del codice |
| HR-6 | In una chat di gruppo, un sottoagente di un altro profilo usa la modalità di approvazione del membro della stanza invece della propria | sicurezza | Riprodotto su `main` |
| (testo) | "Terminal commands can run with the environment and API keys of whichever client started the shared gateway" | tra i peggiori | Elencato tra i casi più gravi |
| GW-27 | Con WhatsApp (bridge) attivo ma non abbinato, il gateway esce all'avvio e blocca tutti i client | rotto | Riprodotto sulla v0.22.4 |
| GW-46 | Con i webhook Telegram su gateway condiviso, solo un bot ottiene la porta | rotto | Lettura del codice |
| Corsia 4 | 19 problemi in cui il codice legge l'ambiente del processo invece di quello del profilo servito | 8 rotti, 2 di sicurezza | Nessuno risolto al 24/10 |

Il criterio d'uscita del piano 22 era "zero conversazioni al profilo sbagliato" [verificato: 22 §5]. Con più bot sullo stesso gateway oggi non lo passerebbe: MSG-43 è proprio quel caso [stima basata su un fatto verificato].

### 6.3 Come si contiene, se si sceglie Hermes

1. **Un contenitore per ogni confine di fiducia**, ognuno con il proprio volume e un solo profilo, o pochi profili dello stesso livello. Esempio: commerciale, interno, direzione e amministrazione. La documentazione Docker prevede contenitori separati per "network segmentation" e per fissare versioni diverse [verificato: docs Docker]. In ogni contenitore il profilo di default è l'unico servito: niente gateway condiviso [stima].
2. **Un bot per contenitore** su Teams e su Telegram [stima].
3. **App desktop non usata**: 41 dei problemi aperti stanno nel desktop e nel terminale interattivo [verificato: issue #143547].
4. **Niente chat di gruppo ospitate dal gateway** finché i 20 problemi della corsia 2 non sono chiusi [verificato: issue #143547].
5. **Terminale ed esecuzione di codice spenti** nei profili aziendali [stima].

Questo contenimento ha un costo: tre istanze vuol dire tre volte aggiornamenti, chiavi, bot e prove [stima].

---

## 7. Vulnerabilità

### 7.1 I numeri del 2026

- Nel GitHub Advisory Database almeno **45 avvisi** su Hermes, dal 27/4 (CVE-2026-7112, 7113) al 21/10/2026 (CVE-2026-114463).
- Per gravità: 1 critico, 3 alti, 19 moderati, 21 bassi, 1 senza valutazione.
- Molti sono "unreviewed" e senza versione corretta indicata.

[verificato: github.com/advisories?query=hermes-agent, pagine 1 e 2]. Le issue aperte con l'etichetta `type/security` sono 547 [verificato: GitHub search API].

| CVE | Cosa | Gravità | Versioni | Fonte |
|---|---|---|---|---|
| CVE-2026-82021 | Il catalogo MCP incluso puntava a un ramo modificabile di un repository di terzi, non a un commit fisso: chi compromette quel repository arriva a ogni host che installa la voce | Critico, CVSS 4.0 9,0 | 0.18.2 fino a 0.19.0 esclusa | [verificato: GHSA-w9gw-vgmg-q67h] |
| CVE-2026-71963 | Esecuzione di comandi tramite un repository con `.git/config` preparato (`core.fsmonitor`); espone le chiavi dei fornitori | Alto, CVSS 4.0 8,6 | 0.18.2-0.21.0, corretto nel commit f6234d0 | [verificato: GHSA-cc88-9pxf-j2wv] |
| CVE-2026-53869 | DNS rebinding sugli endpoint WebSocket, aggira i controlli su Host e Origin | Alto | non indicate | [verificato: Advisory Database, pagina 2] |
| CVE-2026-114463 | Il webhook ricava la rotta autorizzata spezzando l'ID di sessione: con un nome di rotta contenente ":" si arriva a strumenti con più privilegi | n.d. | corretto nella v0.22.2 | [verificato: Advisory Database; dettaglio dal riassunto di ricerca, non verificato] |
| CVE-2026-14628 | Path traversal in `extract_media` del gateway | Moderato | fino a 2026.5.16 | [verificato: Advisory Database]; "senza autenticazione" [non verificato: SentinelOne] |
| CVE-2026-11461 | Un utente autenticato accede alle sessioni di altri | Basso | fino a 0.12.0 | [verificato: Advisory Database]; "il fornitore non ha risposto" [non verificato: riassunto di ricerca] |
| v0.21.6 (8/10) | Correzioni segnalate da Tenable: login della dashboard aggirabile con `X-Forwarded-For`, filtri git eseguiti da repository non fidati, allowlist della posta aggirabile | n.d. | corrette nella v0.21.6 | [verificato: pagina Releases] |

### 7.2 Perché pesa nel board

- Il board mette tutto il lavoro nel perimetro Cyber Essentials, con patch entro 14 giorni [verificato: board, "Capacità"].
- Da aprile 2026 le domande A6.4 e A6.5 di Cyber Essentials fanno fallire in automatico la verifica se gli aggiornamenti critici o ad alto rischio non sono installati entro 14 giorni [non verificato: riassunto di ricerca dell'avviso IASME; testo ufficiale non letto].
- Hermes non pubblica avvisi propri: la pagina di sicurezza del repository ne mostra 0 [verificato]. La sua politica dice che le scappatoie dalle euristiche interne "don't receive advisories" [verificato: SECURITY.md §3.2].
- Le note della v0.22.5 dicono "many changes are undocumented here on purpose" [verificato: rapporto 10 §3; pagina release].
- Risultato: capire quale versione chiude quale CVE richiede lavoro nostro, e spesso costringe a salire di versione minore, cioè ad accettare cambiamenti grandi come il gateway unico [stima].
- La politica resta chiara su un punto: "The only security boundary against an adversarial LLM is the operating system", e Hermes "is a single-tenant personal agent" [verificato: SECURITY.md su main].

---

## 8. Ritmo dei rilasci e peso della manutenzione

| Mese 2026 | Release | Fonte |
|---|---|---|
| marzo | 5 | [verificato: GitHub API releases] |
| aprile | 6 | idem |
| maggio | 5 | idem |
| giugno | 2 | idem |
| luglio | 5 | idem |
| agosto | 8 | idem |
| settembre | 5 | idem |
| ottobre (fino al 25) | 8 | idem |

- Sono 44 release dal 12/3 al 23/10/2026: circa una e mezza a settimana [verificato: GitHub API].
- Solo in ottobre: v0.21.6 (8/10), v0.21.7 (12/10), v0.22.0 (14/10), v0.22.1 (15/10), v0.22.2 (15/10), v0.22.3 e v0.22.4 (21/10), v0.22.5 (23/10) [verificato: GitHub API].
- La v0.22.1 era stata costruita dal commit sbagliato e conteneva lavoro non rilasciato sul gateway [verificato: note v0.22.2].
- Ad ogni avvio Docker le migrazioni dello schema di configurazione girano da sole, dopo una copia di `config.yaml` e `.env` [verificato: docs Docker].
- Prima di ogni release stabile escono candidate (`rc.2`, `rc.3` della v0.22.5 nella stessa notte) [verificato: Docker Hub].

**Stima della manutenzione con Hermes** [stima]:
- un ciclo di aggiornamento costa circa 0,5 gp: leggere le note, provare il digest in stage, i 10 scenari, promuovere e controllare;
- ne servono 2-3 al mese per stare dentro i 14 giorni;
- con lo smistamento dei bug e gli aggiramenti si arriva a **1,5-2,5 gp al mese**;
- con tre istanze (§6.3) il ciclo si ripete tre volte. La parte di prova si condivide, quindi la stima sale verso l'estremo alto.

**Per confronto.** Anche l'Agent SDK esce spesso: Python 12 release dal 30/9 al 24/10 (v0.2.163 → v0.2.174), TypeScript 12 release dal 14/10 al 23/10 (v0.3.299 → v0.3.310) [verificato: GitHub API]. Ma la sua superficie è una libreria: niente gateway, canali o bacheca da migrare. Il codice di quelle parti sarebbe nostro, e i suoi bug pure [stima].

---

## 9. Cosa porta in più rispetto a un motore su Agent SDK, e cosa duplica

### 9.1 Che cosa offre l'Agent SDK di suo

- Una libreria Python e TypeScript "that runs the Claude Code binary", con strumenti, hook, sottoagenti, MCP, permessi, sessioni riprendibili, skill, comandi, memoria e plugin [verificato: code.claude.com/docs/en/agent-sdk/overview].
- Uso regolato dai Commercial Terms di Anthropic [verificato: stessa pagina].
- Il passaggio da un gateway come LiteLLM è documentato da Anthropic con `ANTHROPIC_BASE_URL`. Anthropic però avverte che non mantiene i gateway di terzi e che il gateway va aggiornato insieme a Claude Code [verificato: code.claude.com/docs/en/llm-gateway].
- Per i canali esiste il Chat SDK di Vercel: libreria npm `chat` 4.43.0 del 19/10/2026, licenza MIT, con adattatori `@chat-adapter/teams`, `telegram`, `whatsapp` e stato su Postgres (`state-pg`) [verificato: registry.npmjs.org]. Che giri sul nostro server senza servizi Vercel: [non verificato].

### 9.2 Cosa porta in più Hermes

| Funzione pronta in Hermes | Nel motore su Agent SDK servirebbe | Ordine di grandezza per rifarla [stima] |
|---|---|---|
| Gateway con Teams, Telegram, WhatsApp Cloud e più di 25 altri canali [verificato: docs messaging], allowlist, abbinamento con codice, menzioni, freno ai giri fra bot | Adattatori del Chat SDK, stato in Postgres, allowlist e freno nostri | 4-6 gp, più la stessa preparazione di Entra e Meta |
| Profili con nome, `SOUL.md`, memoria, skill, cron e canali propri | Registro degli agenti (file o tabella) e cartelle di skill: l'Agent SDK le carica già da `.claude/` | 2-3 gp |
| Bacheca kanban fra profili con dispatcher e blocco "serve un umano" | Tabella in Postgres con un lavoratore, oppure Jira | 3-5 gp |
| Skill che l'agente scrive e migliora da solo (A6) | Un agente revisore che propone skill e una persona che approva | 1-2 gp |
| Ricerca a testo pieno nelle sessioni e compressione del contesto | Sessioni dell'SDK più ricerca in Postgres | 1-2 gp |
| Pipeline delle riunioni Teams | Flusso n8n con Microsoft Graph | 2-3 gp |
| Dashboard, app desktop, oltre 600 plugin in catalogo | Non necessari: Teams, Open WebUI e Grafana | 0 |

Le funzioni che l'Agent SDK ha già (sottoagenti, MCP, hook prima degli strumenti, permessi, sessioni) non costano niente da rifare [verificato: overview Agent SDK]. Anche Hermes ha un hook `pre_tool_call` che blocca e, se va in timeout, "fails closed" [verificato: docs hooks su main]. Il Cancello si aggancia nei due casi allo stesso modo.

### 9.3 Cosa duplica nel board

| Funzione di Hermes | Doppione nel board | Chi la tiene |
|---|---|---|
| Cron e routine | n8n | n8n |
| Webhook in ingresso | n8n | n8n |
| Rotazione chiavi, riserve, budget | LiteLLM | LiteLLM |
| Fornitori di memoria esterni | Qdrant, MCP RAG, mcp-memory, BookStack, PostgreSQL | Il board |
| Ricerca ed estrazione web | Firecrawl | Firecrawl, usato da chiunque |
| Chat web | Open WebUI e Claude Team | Open WebUI e Claude Team |
| Bacheca dei compiti | Jira (per le persone) | Jira; la bacheca Hermes solo fra agenti |
| Osservabilità | Prometheus, Grafana, Loki | Lo stack OBSRV |
| Sandbox | Experimental-2 | Experimental-2 |
| Segreti | Infisical, Vaultwarden | Infisical |

[verificato: componenti dal board-vlan.txt; funzioni di Hermes dal rapporto 10 e dalle docs citate]. La divisione dei ruoli è una [stima].

### 9.4 Dove l'Agent SDK va meglio in questo board

- **Identità della persona.** Il nostro codice può passare all'MCP RAG l'ID Entra di chi scrive in Teams, quindi i permessi per utente del board valgono davvero. Hermes manda solo un valore fisso o il nome del profilo [verificato: docs MCP; il resto è una stima].
- **Meno doppioni.** n8n, LiteLLM e la memoria restano gli unici padroni del loro pezzo [stima].
- **Gateway documentato da Anthropic** (`ANTHROPIC_BASE_URL`) [verificato: code.claude.com/docs/en/llm-gateway].
- **Un solo inquilino per processo.** Niente gateway condiviso fra profili con i bug di §6 [stima].

### 9.5 Dove Hermes va meglio

- È **pronto oggi**: canali, profili, bacheca, skill che crescono e cron funzionano senza scrivere codice [verificato: rapporto 10 §4].
- Ha una **comunità enorme** e un catalogo di plugin che cresce ogni settimana [verificato: GitHub; note v0.22.0].
- Il **tempo per il primo bot** in Teams o Telegram è di giorni, non di settimane [stima].

---

## 10. Stima dei giorni per integrarlo in questo contesto

**Prerequisiti dal board.** F1 (OPNsense e VLAN, Proxmox, NetBird e Traefik) e F4 (LiteLLM con budget, pipeline Sirius → MCP RAG) [verificato: board, roadmap]. Hermes entra dopo F4, oppure prima come pilota in Experimental-2 con dati verdi [stima].

| # | Lavoro | gp di base [stima] |
|---|---|---|
| 1 | Contenitore e rete: Docker nella VLAN 30, immagine fissata per digest, volume su ZFS, utente non root, allowlist in uscita su OPNsense, backup PBS del volume | 1,5 |
| 2 | LiteLLM: chiavi virtuali con budget per istanza, alias con "claude", `transport: anthropic_messages`, `context_length` esplicito, prova che la cache legga davvero, cache automatica di LiteLLM accesa | 1,5 |
| 3 | MCP: MCP RAG, mcp-memory, mcp-enrich e MCP di SersanOutreach; liste `include`; un'identità di servizio per istanza; prove dei confini dei permessi | 2 |
| 4 | n8n: API di Hermes con chiave, rotta webhook firmata, due flussi di prova nei due sensi | 1,5 |
| 5 | Teams: app Entra, percorso pubblico su Pangolin e Traefik senza SSO ma con JWT, menzioni e RSC, allowlist, prove in canale e in chat, aggiramento del bug dei documenti | 2,5 |
| 6 | Telegram in polling, un bot per istanza | 0,5 |
| 7 | WhatsApp Cloud API: account Meta Business, numero, token permanente, webhook, regole per la finestra di 24 ore | 2 |
| 8 | Aggancio al Cancello: hook `pre_tool_call` che blocca, strumento MCP `propose_action`, strumenti d'invio tolti | 2,5 |
| 9 | Isolamento: tre istanze separate con chiavi e bot distinti (§6.3) | 2 |
| 10 | Stage e aggiornamenti: 10 scenari di regressione, procedura di aggiornamento e di ritorno indietro, prova di una migrazione di configurazione | 2,5 |
| 11 | Osservabilità e conformità: OpenTelemetry verso Grafana e Loki, Wazuh, Uptime Kuma, schede per Cyber Essentials | 1,5 |
| 12 | Tre profili pilota con le loro skill: post-call su Teams, debrief del mattino, bandi | 2,5 |
| | **Totale** | **22,5 gp di base (forbice 20-25); 29 gp con la riserva del 30 % (forbice 26-33)** |

**Varianti** [stima]:
- **Senza WhatsApp:** 20,5 gp di base, circa 27 con la riserva.
- **Pilota confinato:** Experimental-2, Telegram in polling, 2 profili, MCP in sola lettura, niente Cancello e niente ingresso pubblico. Costa 6-8 gp.
- **Manutenzione dopo l'avvio:** 1,5-2,5 gp al mese (§8).
- **Tempi esterni** che non sono gp: la verifica di Meta Business e il consenso dell'amministratore M365 per i permessi Teams e Graph [non verificato: durata].

**Per confronto, il motore su Agent SDK nello stesso contesto**, come ordine di grandezza [stima, da confrontare con il rapporto dedicato]:
- nucleo (sessioni, registro degli agenti, hook verso il Cancello, LiteLLM via `ANTHROPIC_BASE_URL`): 6-8 gp;
- canali con il Chat SDK, inclusa la stessa preparazione di Entra e Meta: 6-9 gp;
- bacheca in Postgres o su Jira: 3-5 gp;
- routine via n8n: 0,5-1 gp;
- stage e prove: 2 gp;
- totale **17,5-25 gp di base**.

Le righe 1-4, 8, 11 e 12 della tabella Hermes servono in entrambi i casi. La differenza vera non sta nei giorni d'integrazione. Sta nel rischio e nella manutenzione: con Hermes dipendiamo dal ritmo e dai bug del suo gateway; con l'Agent SDK i bug di canali e bacheca sono nostri.

Rispetto al piano 22: lì l'uscita verso l'Agent SDK era stimata 10-15 gp, più il rifacimento di bacheca, routine e canali [verificato: 22 §1 punto 3; PRESENTAZIONE-CEO §15]. Nel board di Michele le routine le fa già n8n, e i canali con il Chat SDK costano meno di prima [stima].

---

## 11. Giudizio

**Si può evitare Hermes?** Sì. Nel board di Michele è sostituibile senza perdere funzioni della visione [stima]:
- n8n, LiteLLM, Qdrant con l'MCP RAG, Open WebUI e Claude Team coprono già metà di ciò che Hermes porta;
- per il resto (canali, profili, bacheca, skill che crescono) un motore sull'Agent SDK costa giorni simili;
- con l'Agent SDK l'identità della persona arriva fino ai permessi del RAG.

**Perché non lo metterei oggi nel percorso dei clienti** (fatti dei §6-8):
- il gateway unico ha problemi di sicurezza aperti proprio sui profili multipli, e la topologia che li evitava è ritirata;
- con la regola dei 14 giorni non si può restare fermi su una versione, e i salti di versione sono grandi e poco documentati;
- è un agente per un solo inquilino, mentre il board vuole permessi per persona.

**Quando Hermes ha senso** [stima]:
1. **Come pilota confinato** in Experimental-2: due o tre profili, Telegram in polling, MCP in sola lettura, dati verdi, 6-8 gp. Si misura se le skill che crescono e la bacheca valgono il costo.
2. **Come orchestratore**, solo se nelle due settimane di prova valgono quattro condizioni:
   - la v0.23 è uscita con note complete;
   - le righe di sicurezza della scheda #143547 (MSG-43, GW-41, KB-10, HR-6) risultano chiuse su `main`;
   - il bug dei documenti su Teams (#113578) è chiuso;
   - un aggiornamento passa i 10 scenari in stage senza interventi a mano.

Michele ha chiesto di valutare l'opzione Claude senza escludere Hermes a priori. Per questo propongo il motore sull'Agent SDK come base, con il Cancello agganciato agli hook. Hermes resta un'opzione da riprendere sui numeri del pilota.

---

## 12. Domande aperte

1. **Pangolin:** può esporre `/api/messages` di Teams e `/whatsapp/webhook` senza login SSO davanti, solo per quei percorsi? E dove gira il suo server pubblico, visto che il board non apre porte? [non verificato]
2. **Telegram e WhatsApp:** Michele li vuole? Il board cita solo Teams e la posta per le notifiche [verificato: board]; la visione chiede Telegram e WhatsApp (J9) [verificato: 00-visione].
3. **WhatsApp:** Sersan Limited può ottenere la verifica Meta Business e un numero dedicato? Hermes non invia i modelli approvati: i messaggi dopo 24 ore di silenzio vanno fatti da n8n o da codice nostro [verificato: docs whatsapp-cloud].
4. **Teams:** l'amministratore M365 concede i permessi RSC e quelli Graph per le trascrizioni? Servono licenze particolari per le trascrizioni? [non verificato]
5. **MCP RAG:** accetta identità di servizio per agente? Con quali permessi minimi? [non verificato]
6. **Cyber Essentials:** come documentiamo all'assessore i 14 giorni per un software che non pubblica avvisi propri? [non verificato]
7. **v0.23.0:** quando esce e quali righe della scheda #143547 chiude? Al 24/10 nessuna era risolta su `main` [verificato: issue #143547].
8. **Account ospite Nous** della v0.22.5: parte qualche chiamata verso Nous anche senza login? Da provare in Experimental-2 guardando il NetFlow di OPNsense [non verificato].
9. **Bacheca dei compiti fra agenti:** Jira (già pagato e nel board) o una tabella nostra? [stima: da decidere con Michele]

---

## Fonti

Tutte consultate il 25/10/2026, salvo diversa indicazione.

**Board di Michele (vincolante)**
- `C:/Users/alber/SerSan-AgentOS/allegati/infra/SerSan Infra Board.md`
- `C:/Users/alber/SerSan-AgentOS/allegati/infra/board-testo-completo.txt`
- `C:/Users/alber/SerSan-AgentOS/allegati/infra/board-vlan.txt`

**Rapporti del progetto**
- `ricerca/10-hermes-agent.md` (24/10/2026)
- `ricerca/22-architettura-scelta.md`
- `ricerca/00-visione-funzionalita.md`
- `PRESENTAZIONE-CEO.md` §5.3, §15

**Repository e rilasci di Hermes**
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/releases (anche via GitHub API)
- https://github.com/NousResearch/hermes-agent/releases/latest
- https://hub.docker.com/r/nousresearch/hermes-agent (tag via API)

**Issue di Hermes**
- https://github.com/NousResearch/hermes-agent/issues/143547 e commento 6365457002
- /issues/134889 ; /issues/106742 ; /issues/58032 ; /issues/141623 ; /issues/143150
- /issues/141861 ; /issues/17332 ; /issues/8465 ; /issues/133606 ; /issues/133208
- /issues/113578 ; /issues/97068 ; /issues/124294

**Sicurezza di Hermes**
- https://raw.githubusercontent.com/NousResearch/hermes-agent/main/SECURITY.md
- https://github.com/NousResearch/hermes-agent/security/advisories
- https://github.com/advisories?query=hermes-agent (pagine 1-2)
- https://github.com/advisories/GHSA-w9gw-vgmg-q67h
- https://github.com/advisories/GHSA-cc88-9pxf-j2wv
- https://www.sentinelone.com/vulnerability-database/cve-2026-14628/

**Codice di Hermes su main**
- `hermes_cli/config_defaults.py` (blocco `telemetry`)
- `hermes_cli/setup.py` (`setup_telemetry`)
- `hermes_cli/observability/shared_metrics_send_config.py`
- `website/docs/integrations/index.md` (Firecrawl self-hosted)

**Documentazione di Hermes**
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- .../docs/getting-started/installation
- .../docs/user-guide/docker
- .../docs/user-guide/messaging
- .../docs/user-guide/messaging/teams
- .../docs/user-guide/messaging/teams-meetings
- .../docs/user-guide/messaging/telegram
- .../docs/user-guide/messaging/whatsapp-cloud
- .../docs/user-guide/messaging/webhooks
- .../docs/user-guide/features/memory-providers
- .../docs/user-guide/features/mcp
- `website/docs/user-guide/multi-profile-gateways.md`, `profiles.md`, `features/hooks.md` su main

**Integrazioni**
- Open WebUI: https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent
- LiteLLM: https://docs.litellm.ai/docs/anthropic_unified/native_passthrough
- LiteLLM: https://docs.litellm.ai/docs/tutorials/prompt_caching
- LiteLLM: https://docs.litellm.ai/docs/proxy/customer_usage
- LiteLLM, incidente di marzo 2026: https://docs.litellm.ai/blog/security-update-march-2026 e https://www.netspi.com/blog/executive-blog/ai-ml-pentesting/litellm-supply-chain-compromise/ (letti tramite riassunto di ricerca)
- Blog sulla cache con LiteLLM: https://gitcode.csdn.net/69eef0d654b52172bc704006.html (terzi)

**Anthropic**
- https://code.claude.com/docs/en/agent-sdk/overview
- https://code.claude.com/docs/en/llm-gateway
- Release dell'Agent SDK via GitHub API: https://github.com/anthropics/claude-agent-sdk-python e https://github.com/anthropics/claude-agent-sdk-typescript

**Chat SDK**
- https://registry.npmjs.org/chat
- https://registry.npmjs.org/@chat-adapter/teams ; .../telegram ; .../whatsapp ; .../state-pg
- https://vercel.com/kb/guide/the-complete-guide-to-chat-sdk

**Cyber Essentials** (letti tramite riassunto di ricerca)
- https://iasme.co.uk/?p=27103
- https://www.techradar.com/pro/avoiding-the-auto-fail-under-cyber-essentials-new-rules
