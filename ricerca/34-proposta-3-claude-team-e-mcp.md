# 34 · Proposta 3: Claude Team al centro, con i connettori MCP verso il server

**Data:** 25/10/2026. **Per:** Alessandro Serratt e Michele Sanna, preparata per Alberto Tuveri; la parte tecnica vale anche per Mattia Scattu.
**Vincolo fisso:** il board dell'infrastruttura di Michele (`allegati/infra/`). In cloud restano solo M365/Entra ID, Claude Team, API Anthropic dietro LiteLLM, Cloudflare (DNS), GitHub, Supabase, Vercel, Jira, Instantly e uno spazio S3 facoltativo. Azure esce. Tutto il resto è self-hosted sul DL380 [verificato: `SerSan Infra Board.md` righe 9-13; messaggio di Michele del 25/10/2026].
**Regola di Alberto:** nessuna funzione della lista A1-L12 si toglie, si rimanda a "forse" o si declassa. Dove manca un componente, il documento scrive cosa serve per averlo: acquisto, abbonamento, servizio da installare, configurazione, giorni.
**Letti:** `00-visione-funzionalita.md`, `PRESENTAZIONE-CEO.md`, il board completo, i rapporti 22 e 25-33, e le pagine ufficiali di Anthropic e degli altri fornitori lette oggi.
**Etichette.** [verificato: fonte] = letto oggi nella fonte indicata, o nel rapporto del progetto citato. [non verificato] = stima, proposta o dato da confermare. gp = giorni-persona di sviluppo. Prezzi IVA esclusa salvo dove è scritto, rilevati il 24 o il 25/10/2026; cambio 1 $ = 0,8934 € [verificato: ricerca/14, riga 7].

---

## In breve

**L'idea.** Le quattro persone lavorano in **Claude Team**, che SerSan ha già. Dentro Claude Team trovano la memoria e gli strumenti dell'azienda attraverso alcuni **connettori MCP** verso il server: la memoria ricercabile (MCP RAG), la memoria con i dati fissi (regole, obiettivi, catalogo, meeting), SersanOutreach in lettura, Jira, BookStack e il **Cancello**. Dietro le quinte girano pochi **lavori programmati in n8n**, che chiamano Claude con la chiave API passando da LiteLLM. L'**Agent SDK di Claude** entra solo dove serve un agente vero, cioè un lavoro a più passi con strumenti: il brief, l'offerta, l'agenda, l'operatore outbound e pochi altri. Ciò che esce verso un cliente passa sempre dal Cancello, con la carta di approvazione sul telefono in Teams.

**Quanto copre da sola.** Contando le 90 voci della lista, la Proposta 3 nella sua forma "pura" (Claude Team, connettori, lavori n8n, Cancello, pochi agenti Agent SDK) copre **59 voci per intero, 24 in parte e 7 no** (§7). Le parti che non copre da sola sono quelle che l'idea mette al centro: le **squadre di agenti che si passano il lavoro** in una stanza leggibile da noi, la **chat di gruppo** di persone e agenti, l'agente che **entra nelle call degli altri**, la voce di **"Andrea"** e alcuni strumenti esterni (firma elettronica, fatturazione, newsletter). Claude Team oggi non li dà: i compiti programmati appartengono al singolo account e non si condividono, i Projects con un coordinatore non ci sono sul piano Team, e Claude in Teams è solo in lista d'attesa [verificato: §2]. Per coprire tutto servono sette aggiunte (§8), tutte dentro il board o scritte come necessità esterne con il loro costo.

**Tempi e lavoro.** Sei fasi, da P0 a P5. Si parte subito, senza server: nelle prime quattro settimane Claude Team lavora già per il marketing, le offerte e le slide, sui soli dati verdi e gialli. Il lavoro di sviluppo è di **circa 191 gp di base e 254 gp con una riserva di un terzo**, in **30-42 settimane** con la capacità di oggi. L'infrastruttura F0-F3 la porta avanti Michele con il suo board e qui non è contata [non verificato: stima, §9].

**Costi.** Rispetto a oggi: circa **135 € al mese in più** finché Azure resta acceso; da circa **−15 a +20 €** dopo lo spegnimento di Azure; circa **58-110 €** con Andrea; circa **551-557 €** quando finisce l'anno gratuito di Claude Team. Una tantum: circa **3.114-4.117 € subito** e **1.697-2.353 € nella fase F5** del board. Le eccezioni fuori dal board (Metricool, Apollo, Slack, WhatsApp e le altre) sono a parte, ognuna con il suo prezzo [non verificato: calcoli su ricerca/33, §10].

**Il giudizio onesto.** È la proposta che dà valore prima e con meno pezzi sempre accesi, perché usa ciò che SerSan paga già. Non è però una scorciatoia per l'idea intera: per far parlare le squadre fra loro e avere la chat di gruppo servono la stessa bacheca, lo stesso Cancello e la stessa "Porta chat" in Teams delle proposte centrate sul motore. In più dipende da funzioni di Claude Team ancora in anteprima o in beta, e porta a Claude Team pezzi di documenti dell'azienda: i dati rossi vanno decisi con il parere legale (§11).

---

## 1. L'architettura in una pagina

```
PERSONE (4)
  Claude Team (web, desktop, telefono): chat, Projects condivisi per squadra,
  skill dell'organizzazione, Cowork, Claude Code, compiti programmati personali
     |  connettori ufficiali: Microsoft 365 (sola lettura), Atlassian/Jira
     |  connettori nostri (MCP remoti con OAuth Entra), via Pangolin + Traefik:
     |    MCP RAG . MCP memoria . SersanOutreach lettura . BookStack . Cancello . bacheca
  Teams (M365): debrief, carte di approvazione, canali per squadra e per cliente,
     |  stanza "Agenti" (dalla fase P3) tramite il nostro bot "Porta chat"
     v
==================== DL380 . Proxmox VE . VLAN default-deny su OPNsense ====================
VLAN 20 EDGE   Traefik + Pangolin: rotte /mcp/* con OAuth dei server, /api/messages del bot
VLAN 30 APPS   n8n: orari, webhook, circa 30 lavori programmati
               LiteLLM: una chiave per agente, un team per squadra, un utente per persona
               VM agenti-01: CANCELLO (carte, regole, esecutori, audit, stop)
                             PORTA CHAT (bot Teams; Telegram, WhatsApp, Slack come eccezioni)
                             MOTORE LEGGERO su Agent SDK (circa 10 agenti veri, max 6 sessioni)
               LXC mcp-01: MCP memoria, gateway OAuth, SersanOutreach MCP, BookStack MCP,
                           Cancello MCP, bacheca MCP
               MCP RAG, mcp-memory, BookStack, openoutreach, Firecrawl, bandi-watcher (board)
VLAN 40 DATA   PostgreSQL 16 (memoria, cancello, bacheca, litellm, n8n, sessioni) . Qdrant
               archivio S3 (MinIO o sostituto) . Infisical . Vaultwarden . MariaDB per BookStack
VLAN 80 AI     LXC GPU: Qwen3-4B, embedding e reranker, Docling (board) + trascrizione
VLAN MEET      VM meet-01: Vexa, bot nelle call degli altri (dalla fase P2)
VLAN VOCE      Asterisk per "Andrea" (dalla fase P4); agente Pipecat in APPS
VLAN 50 CICD   runner GitHub (board) + runner self-hosted di Claude Code (facoltativo, beta)
VLAN 70 OBSRV  Prometheus, Loki, Grafana (organigramma, banca dei token), Wazuh
VLAN 90 LAB    pilota Buzz (e Paperclip) su Experimental-2, senza dati dei clienti
==========================================================================================
FUORI, come necessità esterne con costo: operatore telefonico italiano (Andrea), relay SMTP
per la newsletter, eventuale VPS per Pangolin, eccezioni del kit commerciale (§8 E)
```

[verificato: board per i servizi che esistono già; il resto è una proposta, non verificato]

Le quattro regole del disegno:

1. **Le persone lavorano in Claude Team, gli automatismi con la chiave API.** I posti Claude Team servono all'uso ordinario delle app di Anthropic. Chi costruisce servizi, anche con l'Agent SDK, usa la chiave della Console [verificato: ricerca/26 §5.1, da code.claude.com/docs/en/legal-and-compliance]. Quindi i lavori di n8n e gli agenti del motore passano da LiteLLM con la chiave API; le persone usano i loro posti.
2. **I connettori leggono e propongono, non agiscono.** I connettori nostri espongono solo strumenti di lettura e lo strumento "proponi un'azione" del Cancello. Il connettore Microsoft 365 resta in sola lettura. Un invio, una pubblicazione, un pagamento o una cancellazione passano dal Cancello e dal sì di una persona [non verificato: proposta coerente con PRESENTAZIONE-CEO.md §5.4].
3. **L'Agent SDK solo dove serve.** Riassumere, classificare ed estrarre a schema sono chiamate semplici a Claude, lanciate da n8n. Una sessione Agent SDK si apre solo per i lavori a più passi con strumenti [non verificato: proposta, sul modello di ricerca/20-E §1].
4. **La memoria e le regole stanno in casa.** Claude Team è una finestra, non un deposito: memoria, registro, bacheca e Cancello restano sul server. Se un giorno Claude Team cambia, si cambia la finestra [non verificato: proposta].

---

## 2. Cosa sa fare Claude Team oggi, e cosa no

Pagine lette il 25/10/2026.

| Tema | Fatto | Fonte |
|---|---|---|
| Prezzo | Posto standard 20 $ al mese con fatturazione annuale (25 $ mensile); posto premium 100 $ (125 $ mensile), con 5 volte l'uso dello standard; da 2 a 150 posti | [verificato: claude.com/pricing/team] |
| Cosa include | Claude Code e Cowork; Design, Slides e Docs; integrazione Microsoft 365 e Outlook; ricerca aziendale; Projects con condivisione; connettori, skill, memoria, ricerca web; SSO; controlli dell'amministratore sui connettori remoti e locali; skill distribuite a tutta l'organizzazione; statistiche d'uso e istruzioni dell'organizzazione | [verificato: claude.com/pricing/team] |
| Crediti | "Up to $500 per month in pooled API credits" | [verificato: claude.com/pricing/team]; se valgono anche per la chiave API dietro LiteLLM [non verificato] |
| Dati | "No model training on your content by default" | [verificato: claude.com/pricing/team] |
| Cosa manca rispetto a Enterprise | log di audit, SCIM, Compliance API, conservazione dei dati personalizzata, ruoli, HIPAA | [verificato: claude.com/pricing/team] |
| Tetti di spesa per persona | La pagina si contraddice: nella tabella di confronto "User and organizational level spend controls" è "Yes" anche per Team, mentre fra le voci di Enterprise c'è "Admins set user and org spend limits" | [verificato: claude.com/pricing/team]; il comportamento reale [non verificato] |
| Connettori personalizzati (MCP remoti) | Ci sono sul piano Team. Solo gli Owner li aggiungono; poi ogni persona si collega da sola, di solito con OAuth. Con una credenziale fissa, tutti condividono gli stessi accessi | [verificato: support.claude.com, articolo 11175166] |
| Da dove partono | Dai server di Anthropic, per tutti i client. Un server in una rete privata o dietro VPN non si raggiunge, salvo aprire agli IP di Anthropic | [verificato: support.claude.com, articolo 11175166] |
| Compiti programmati in Cowork | Su tutti i piani a pagamento, Team compreso. Girano in remoto anche a computer spento. Frequenza oraria, giornaliera, settimanale o manuale. Usano connettori, skill e plugin | [verificato: support.claude.com, articolo 13854387, aggiornato il 24/10/2026] |
| Compiti programmati di Claude Code | In anteprima di ricerca. Su Pro, Max, Team ed Enterprise. Partono a orario (non più di una volta l'ora), con una chiamata API (`/fire` con token) o da un evento GitHub. **Appartengono al singolo account e non si condividono.** Consumano l'uso del posto. Ciò che fanno attraverso i connettori "appears as you". Gli Owner li possono spegnere per tutti | [verificato: code.claude.com/docs/en/routines] |
| Ambienti self-hosted | In beta pubblica su Team ed Enterprise, spenti di default. Le sessioni cloud di Claude Code e i compiti programmati girano su un nostro "runner", che fa solo connessioni in uscita verso `api.anthropic.com`. Raggiungono i servizi interni senza esporli. Consumano l'uso dei posti. Non funzionano con la conservazione zero (ZDR). La conversazione va comunque ad Anthropic | [verificato: code.claude.com/docs/en/self-hosted-environments] |
| Projects con coordinatore e thread paralleli | "Projects aren't offered on Team or Enterprise plans yet" | [verificato: code.claude.com/docs/en/claude-projects] |
| Claude dentro Teams (Claude Tag) | Solo lista d'attesa, senza data; Claude Tag oggi vive in Slack | [verificato: ricerca/28 §2.5, da claude.com/form/claude-tag-teams-waitlist] |
| Connettore Microsoft 365 | Legge SharePoint, OneDrive, Outlook, chat e canali di Teams, calendari, trascrizioni e registrazioni delle riunioni, con l'accesso delegato della persona. Scrittura spenta di default. Serve il consenso di un Global Administrator | [verificato: ricerca/29 §5.4, da support.claude.com, articolo 12542951] |

**Cosa vuol dire per l'idea.**
- Claude Team è un ottimo posto di lavoro per **ogni singola persona**: chat, slide, documenti, codice, skill dell'azienda, domande alla memoria anche dal telefono.
- Non è una **squadra di agenti**: non ci sono agenti con un nome che vivono nel tempo, non c'è una bacheca fra agenti, i compiti programmati sono di una persona e agiscono a suo nome. Non c'è nemmeno una chat di gruppo con gli agenti dentro Teams [verificato: righe sopra].
- Non ha **log di audit** sul piano Team [verificato: claude.com/pricing/team]. Il registro di ciò che succede lo tengono il Cancello e i server MCP, con il registro delle query del board [verificato: board, "MCP RAG · Permessi per utente · log delle query"].

---

## 3. Componenti e dove girano

### 3.1 In cloud (tutto già nel board)

| Componente | Ruolo nella Proposta 3 | Nel board | Da fare |
|---|---|---|---|
| **Claude Team**, 5 posti premium nel bundle | La porta di lavoro delle persone: Projects condivisi per squadra, skill dell'organizzazione, connettori, Cowork, Claude Code | sì, "ragiona sul RAG via MCP" [verificato: board] | configurazione, skill, connettori (fase P0) |
| **M365 / Entra ID** | Identità, MFA, posta, calendario, SharePoint, Teams; trascrizioni delle nostre riunioni via Graph | sì [verificato: board] | registrazioni delle app, permessi minimi, impostazioni delle trascrizioni |
| **API Anthropic** dietro LiteLLM | Lavori di n8n, agenti del motore, voce di Andrea | sì [verificato: board] | chiavi virtuali e budget in LiteLLM |
| **Jira** | To-do e progetti; connettore Atlassian per le persone; account di servizio per gli agenti | sì [verificato: board] | modello di progetto, account di servizio |
| **Instantly**, **GitHub**, **Supabase**, **Vercel**, **Cloudflare** | Come nel board | sì [verificato: board] | nessuna modifica |

### 3.2 Sul DL380

| Componente | VLAN | Macchina | RAM | GPU | Nel board? | Da costruire |
|---|---|---|---|---|---|---|
| Traefik + Pangolin | 20 EDGE | come da board | board | no | sì | rotte `/mcp/*` senza il login di Pangolin davanti (l'OAuth lo fanno i server MCP) e `/api/messages` del bot Teams [non verificato: da provare] |
| n8n | 30 APPS | come da board | board | no | sì | circa 30 flussi (§5) |
| LiteLLM | 30 APPS | come da board | board | no | sì, in F4 | chiavi, team, budget, prova degli header `anthropic-beta` [verificato: ricerca/26 §4.2] |
| MCP RAG | 30 APPS | come da board | board | no | sì | filtri per colore e per persona, oscuramento delle PII marcate, OAuth con Entra |
| mcp-memory | 30 APPS | come da board | board | no | sì | resta un taccuino per famiglia di agenti [verificato: ricerca/29 §7.1] |
| BookStack | 30 APPS | come da board | board | no | sì | modelli di pagina, ruoli, OIDC con Entra |
| **VM agenti-01**: Cancello, Porta chat, motore leggero su Agent SDK | 30 APPS | VM con Docker | 8-12 GB | no | **no** | sì (§8, §9) |
| **LXC mcp-01**: MCP memoria su Postgres, gateway OAuth, SersanOutreach MCP in HTTP, BookStack MCP, Cancello MCP, bacheca MCP | 30 APPS | LXC | 2 GB | no | in parte (mcp-enrich, mcp-memory) | sì |
| PostgreSQL 16 | 40 DATA | come da board | board | no | sì | schemi `memoria`, `cancello`, `bacheca`; database di LiteLLM e n8n |
| Qdrant | 40 DATA | come da board | board | no | sì | collezioni `conoscenza` e `finanza` separate [verificato: proposta di ricerca/29 §6.2] |
| MariaDB per BookStack | 40 DATA | LXC | 1 GB | no | **no** | BookStack non supporta PostgreSQL [verificato: ricerca/29 §3.1] |
| Archivio S3 (audio, file) | 40 DATA | come da board | board | no | sì (MinIO) | MinIO è archiviato dal 12/02/2026 [verificato: ricerca/25 N14]: sostituto da scegliere con Michele |
| LXC GPU: Qwen3-4B, embedding, reranker, Docling | 80 AI | come da board | board | RTX 4000 di giorno | sì | nessuno |
| Servizio di trascrizione | 80 AI | stesso LXC | 4-8 GB | 2-4,5 GB di giorno, CPU la sera | **no** | sì [verificato: ricerca/30 §6.2] |
| VM meet-01 con Vexa | VLAN MEET nuova | VM | 12 GB | no | **no** | sì [verificato: ricerca/30 §11.2] |
| Asterisk per Andrea | VLAN VOCE nuova | LXC | 1 GB | no | **no** | sì [verificato: ricerca/31 §1.1] |
| Agente Pipecat per Andrea | 30 APPS | container | 1-2 GB, più 4-6 GB di STT e TTS su CPU | seconda GPU in F5, facoltativa | **no** | sì [verificato: ricerca/31 §8.2] |
| Runner self-hosted di Claude Code | 50 CICD | container, uno per persona | 1-2 GB ciascuno [non verificato] | no | **no** | facoltativo, beta (§3.4) |
| Grafana, Loki, Prometheus, Wazuh | 70 OBSRV | come da board | board | no | sì | cruscotti: organigramma, banca dei token, costi per agente |
| Buzz (e Paperclip) | 90 LAB | Experimental-2 | dentro i 24 GB del board | no | LAB sì, Buzz no | pilota senza dati dei clienti |

### 3.3 Bilancio di RAM e GPU

**RAM.** Il board lascia circa 53 GB liberi [verificato: board, tabella "Capacità"]. Il rapporto 32 stima 16-18 GB nuovi all'avvio di F4 e 46-64 GB con tutto acceso, con 12-16 sessioni di agenti insieme [verificato: ricerca/32 §3.3]. La Proposta 3 tiene **al massimo 6 sessioni del motore** insieme, perché il lavoro delle persone gira sui posti Claude Team nel cloud di Anthropic. Conto per lo scenario completo, con le voci del rapporto 32:

| Voce | GB |
|---|---|
| Motore leggero (al massimo 6 sessioni, più coda) | 6-8 |
| Cancello | 2 |
| Porta chat | 1 |
| LXC mcp-01 e MariaDB | 3 |
| Bot nelle call (VM meet-01) | 12 |
| Trascrizione e lotti | 8 |
| Andrea su CPU (4 con la seconda GPU) | 4-8 |
| SersanOutreach, worker in più | 1-2 |
| Crescita della memoria aziendale | 4-6 |
| **Totale nuovo** | **41-50** |
| **Margine sui 53 GB liberi** | **da +3 a +12** |

[non verificato: somma di stime]. Due condizioni: fissare la cache ZFS a 12 GiB, come propone il rapporto 32 [verificato: ricerca/32 §3.2], e accendere il runner self-hosted di Claude Code solo se il margine lo consente (4-8 GB in più) [non verificato]. Con queste due regole **la RAM in più non serve subito**. Se il margine scende sotto i 5 GB misurati, il passo giusto è quello del rapporto 32: 384 GB, 816 € IVA esclusa con moduli 2133 o £1.020 con moduli 2666 [verificato: ricerca/32 §2.3].

**GPU.** La Proposta 3 non aggiunge carichi rispetto ai rapporti 30 e 31. Di giorno la RTX 4000 tiene la pipeline del board; la trascrizione dal vivo ci entra solo spostando il reranker sulla CPU; la sera la scheda va a Experimental-1 e la trascrizione passa sulla CPU [verificato: ricerca/30 §6]. Le domande serali di Claude Team alla memoria calcolano l'embedding della domanda sulla CPU [verificato: ricerca/25 N06]. La seconda GPU consigliata è la **RTX 2000 Ada da 16 GB**, nella fase F5 del board; la "A2000 Ada da 6 GB GDDR7" non esiste [verificato: ricerca/32 §4].

### 3.4 Rete e accessi

- **Connettori di Claude Team.** Partono dai server di Anthropic, quindi gli endpoint MCP devono essere raggiungibili da internet [verificato: support.claude.com 11175166]. La strada del board è Pangolin con Traefik [verificato: board, "Accesso"]. Se Pangolin chiede un suo login davanti, Anthropic non lo supera: i server MCP fanno da sé l'OAuth con Entra, e Pangolin lascia passare solo quelle rotte [non verificato: da provare, come scrive ricerca/29 §7.3]. L'accesso condizionale di Entra può guardare le richieste dagli IP di Anthropic, `160.79.104.0/21` [verificato: ricerca/29 §5.4].
- **Una persona, un'identità.** Con l'OAuth di Entra ogni persona arriva all'MCP RAG con il suo nome. Una credenziale fissa darebbe a tutti gli stessi accessi [verificato: support.claude.com 11175166]. Quindi niente chiavi fisse sui connettori che toccano dati gialli o rossi [non verificato: proposta].
- **Dove vive Pangolin.** Pangolin in modalità tunnel di solito sta su un VPS con IP pubblico, oppure servono porte aperte verso la VLAN EDGE con l'IP fisso [verificato: ricerca/25 N10]. Un VPS piccolo parte da **6,49 € al mese** IVA esclusa su Hetzner [verificato: hetzner.com/cloud, 25/10/2026]. Decide Michele.
- **Senza esporre nulla.** Michele e Alberto possono usare i server MCP da Claude Desktop attraverso la mesh di NetBird, come prevede il board [verificato: board, "In alternativa Claude Desktop via mesh"]. I server MCP locali di Claude Desktop però non arrivano in Cowork né in claude.ai [verificato: support.claude.com 11175166]. Dal telefono serve la rotta pubblica.
- **Runner self-hosted di Claude Code (facoltativo).** Le sessioni cloud di Claude Code e i compiti programmati delle persone possono girare su un runner nostro, solo in uscita verso `api.anthropic.com`, e raggiungere i server MCP interni senza esporli [verificato: code.claude.com/docs/en/self-hosted-environments]. Proposta: un runner per persona nella VLAN 50 CICD, accanto ai runner GitHub, con regole esplicite verso le sole porte MCP in APPS [non verificato: proposta]. Limiti: è in beta, ogni runner serve un solo proprietario alla volta, e non funziona se l'organizzazione attiva la conservazione zero [verificato: idem].
- **Bot Teams.** Riceve i messaggi su `/api/messages`, chiamato dai server di Microsoft con un token firmato [verificato: ricerca/28 §2.2]. Registrazione "Teams-managed" senza Azure da provare in un giorno; riserva Azure Bot F0 gratuita o pagina del Cancello [verificato: ricerca/28 "In breve"].

---

## 4. I connettori per le persone

| Connettore | Strumenti | Chi lo usa | Colore massimo | Autenticazione | Fase |
|---|---|---|---|---|---|
| **MCP RAG** (board) | `cerca`, `apri`, `fonti` con fonte, data e link | tutti | giallo; rosso solo oscurato, finché il parere legale non decide (§11) | OAuth Entra, filtri per persona | P2 |
| **MCP memoria** (nuovo, su Postgres) | `regole_di`, `obiettivi`, `catalogo`, `meeting`, `decisioni`, `agente` | tutti | giallo; obiettivi finanziari solo ai CEO | OAuth Entra | P1 |
| **SersanOutreach lettura** | i 19 strumenti in lettura già scritti (KPI, coda, pipeline, funnel, risposte, deal persi) | Alessandro, Alberto | giallo | oggi è solo stdio: servono un host HTTPS e un server OAuth, che non esistono [verificato: ricerca/01 §5.1] | P1 |
| **Jira** | connettore Atlassian ufficiale (Rovo MCP, OAuth 2.1) | tutti | giallo | account della persona [verificato: ricerca/29 §4.1] | P0 |
| **BookStack** | lettura di libri e pagine; le modifiche passano dal Cancello | tutti | giallo | OAuth Entra o token per persona | P2 |
| **Cancello** (nuovo) | `carte_in_attesa`, `stato_carta`, `proponi_azione`; **nessuno strumento che approva** | tutti | come l'azione | OAuth Entra | P1 |
| **Bacheca** (nuovo) | `affida_lavoro` a una squadra, `stato_lavoro`, `passaggi_di_oggi` | tutti | giallo | OAuth Entra | P3 |
| **Microsoft 365** (ufficiale) | lettura di posta, calendario, file, chat, trascrizioni | tutti | rosso, ma con l'accesso della persona | delegato; scrittura spenta [verificato: ricerca/29 §5.4] | P0 |
| **Metricool** (eccezione) | già in uso, scritture su "Needs approval" | Alberto | verde | account Metricool [verificato: ricerca/18, riga 72] | P0, se Michele lo ammette |

Tre regole valgono per tutti i connettori [non verificato: proposte]:
- **Approvare non è uno strumento.** Il sì arriva solo dalla carta in Teams, che porta l'identità Entra di chi preme, oppure dalla pagina del Cancello con Entra e chiave FIDO2. Un modello non può approvare nulla, nemmeno se una mail o una trascrizione glielo chiede.
- **I compiti programmati personali leggono e propongono.** Ciò che un compito programmato fa con i connettori appare a nome della persona [verificato: code.claude.com/docs/en/routines]. Per questo i connettori nostri non hanno strumenti che scrivono fuori dal Cancello.
- **Ogni query è registrata.** I server MCP scrivono in Loki chi ha chiesto cosa e quali blocchi sono usciti, come chiede il board per l'MCP RAG [verificato: board].

---

## 5. Gli agenti in background: quattro tipi

Le 57 figure delle nove squadre della presentazione restano tutte [verificato: PRESENTAZIONE-CEO.md §4]. Cambia il modo in cui ognuna lavora. Quattro tipi:

- **T. Claude Team**: una skill e un progetto condiviso in Claude Team, usati da una persona. L'agente è Claude con le regole della squadra.
- **N. Lavoro n8n**: un orario o un evento, una chiamata a Claude via LiteLLM con uscita a schema, una carta se qualcosa esce.
- **S. Agente Agent SDK**: un lavoro a più passi con strumenti, lanciato da n8n o dalla bacheca, con il ponte verso il Cancello.
- **V. Servizio**: un componente che fa il lavoro da sé (pipeline, bot, centralino, Cancello).

| Squadra | Agente | Tipo | Fase |
|---|---|---|---|
| Outbound | Agente email | N (risposte di Instantly, classificazione, bozza, carta) | P2 |
| Outbound | Agente LinkedIn | N (coda di SersanOutreach, bozze da approvare) | P2 |
| Outbound | Sentinella segnali | N (notte: Firecrawl, segnali di SersanOutreach, punteggio) | P2 |
| Outbound | Operatore outbound | S (MCP operatore di SersanOutreach, scritture solo via Cancello) | P2 |
| Outbound | Agente clienti simili | S (ricerca a più passi) | P4 |
| Chiamate | Agente chiamate | V (trascrizione di Teams via Graph; Vexa per le call degli altri) | P1 e P2 |
| Chiamate | Analista chiamate | N (riassunto secondo le regole di ciascuno, registro dei meeting) | P1 |
| Chiamate | Post-call | N (estrazione a schema, recap, CRM, bozza della mail in carta) | P1 |
| Chiamate | Agente agenda | S (calendari M365, proposta di orari, invito dopo il sì) | P2 |
| Chiamate | Dettatura | T (dettatura delle app Claude) più V (note vocali trascritte in casa) | P0 e P2 |
| Vendite | Agente brief | S (sera prima) più T (su richiesta) | P2 |
| Vendite | Agente proposte | S (bozza su Opus) più T (Michele rifinisce) | P2 |
| Vendite | Pipeline | N (probabilità calcolate dal codice, testo da Claude) | P4 |
| Vendite | Coach vendite | N (solo alla persona; aggregati al responsabile) | P4 |
| Vendite | "Andrea" | V (Asterisk, Pipecat, Haiku 5.5 via LiteLLM) | P4 |
| Vendite | Analista vinto/perso | N | P2 |
| Vendite | Agente intake | N (modulo, posta, brief di intake, carta) | P2 |
| Vendite | Agente contratti | N (modello, firma elettronica dopo il sì) | P5 |
| Marketing | Editoriale | T più N (temi settimanali) | P0 e P2 |
| Marketing | Ricerca concorrenza | N (settimanale, Firecrawl) | P2 |
| Marketing | Analista metriche | N (lunedì: Metricool, KPI di SersanOutreach) | P2 |
| Marketing | Pubblicatore | T (sessione presidiata di Alberto, come chiedono le direttive) | P0 |
| Marketing | Agente newsletter | N (con lo strumento di newsletter) | P3 |
| Marketing | Community manager | N (commenti della pagina aziendale, risposte in carta) | P3 |
| Marketing | Agente sito e SEO | S (Claude Code su un runner, pull request; il deploy resta umano) | P5 |
| Marketing | Agente eventi e webinar | N | P5 |
| Studio | Copywriter | T (skill con la voce del brand) | P0 |
| Studio | Agente slide | T (Slides e Design di Claude Team) più S (deck automatico per il brief) | P0 e P2 |
| Studio | Agente video | T (con Higgsfield, HyperFrames, After Effects) | P0 |
| Studio | Agente grafiche | T | P0 |
| Progetti | Project manager | S (Jira, stato settimanale, rischi) | P3 |
| Progetti | Agente task | N (to-do in Jira via Cancello) | P1 |
| Progetti | Report cliente | N (venerdì, carta) | P3 |
| Progetti | Onboarding cliente | N (canale Teams, cartella SharePoint, progetto Jira dopo la carta) | P3 |
| Progetti | Sviluppatori | T (Claude Code; compiti programmati con eventi GitHub) | P0 |
| Progetti | Assistenza clienti | N (stanza del cliente e posta, risposta in carta) | P5 |
| Progetti | Agente rinnovi | N (mensile) | P5 |
| Progetti | Agente casi studio | N (a fine progetto) | P5 |
| Memoria | Raccoglitore | V (pipeline del board più ingressi n8n) | P1 e P2 |
| Memoria | Pulitore | V (filtro del board, modello locale) | P2 |
| Memoria | Bibliotecario | V (MCP RAG) più T (le domande da Claude Team) | P2 |
| Memoria | Archivista | N (scadenze di conservazione) | P2 |
| Memoria | Sistemista | N (avvisi di Prometheus, riassunto, Teams) | P2 |
| Direzione | Capo di gabinetto | S (smista sulla bacheca) più T (progetto condiviso in Claude Team) | P0 e P3 |
| Direzione | Report del mattino | N (alle 7:00, numeri da Postgres) | P1 |
| Direzione | Banca dei token | V (LiteLLM più statistiche di Claude Team) | P1 e P3 |
| Direzione | Registro e audit | V (Cancello, Loki) | P1 |
| Direzione | Guardiano | V (Cancello) | P1 |
| Direzione | Mappatore processi | S (interviste e dati dichiarati, una volta al mese) | P3 |
| Direzione | Intervistatore | T (progetto "Intervista" in Claude Team) | P0 e P3 |
| Direzione | Smistatore posta | N (delta di Graph, classificazione, bozze in carta) | P2 |
| Direzione | Allenatore AI | N (settimanale) | P5 |
| Direzione | Assistente personale | T (account Claude personale di chi lo vuole) | P5 |
| Amministrazione | Fatture e incassi | N (con lo strumento di fatturazione) | P5 |
| Amministrazione | Acquisti e abbonamenti | N | P5 |
| Amministrazione | Controllo di gestione | N (numeri da Postgres, export di Sirius) | P5 |
| Amministrazione | Bandi e finanziamenti | V (pipeline bandi del board) più N (profili dei clienti) | P2 |

[non verificato: classificazione proposta]

**In numeri**, guardando il tipo scritto per primo: 10 agenti di tipo T, 29 lavori N, 9 agenti S, 9 servizi V. Contando anche le figure miste, il motore Agent SDK serve a 10 agenti veri (i 9 di tipo S più il deck automatico dell'Agente slide), non a 57. Il registro dei profili li conta tutti e 57, con nome, squadra, responsabile, tipo, modello, tetto di spesa e costo del mese [non verificato: proposta].

---

## 6. Come lavorano insieme

### 6.1 Le tre strade

1. **Persona, Claude, connettori.** Alessandro chiede in Claude Team: "cosa abbiamo promesso a questo cliente?". Claude legge MCP RAG, MCP memoria e SersanOutreach, con i permessi di Alessandro, e risponde con le fonti. Se serve agire, Claude chiama `proponi_azione` sul Cancello; la carta arriva in Teams; Alessandro approva dal telefono; l'esecutore agisce una volta sola.
2. **Persona, bacheca, agenti.** Dalla fase P3 il Capo di gabinetto è un progetto condiviso in Claude Team con il connettore bacheca. Una persona scrive "prepara l'offerta per il cliente X entro domani". Claude chiama `affida_lavoro`; il lavoro entra nella coda; il motore apre una sessione dell'Agente proposte; il risultato torna nel thread di Teams e, se esce dall'azienda, come carta.
3. **Evento, n8n, agenti.** Una trascrizione pronta, una risposta di Instantly, un modulo del sito o un orario fanno partire un lavoro n8n o una sessione del motore. Il lavoro scrive un **passaggio** nella bacheca per l'agente successivo. La bacheca applica il freno: al massimo 3 passaggi per catena, 8 messaggi per thread e un tetto in dollari per catena [non verificato: valori di ricerca/22 §3, da tarare].

[non verificato: tutte proposte]

### 6.2 Il percorso di un cliente con la Proposta 3

1. La **Sentinella** (lavoro notturno) trova un'azienda che assume uno sviluppatore. Scrive un passaggio per l'**Agente email**, che prepara il primo messaggio in SersanOutreach. Alessandro lo approva.
2. Il prospect risponde. L'Agente email classifica la risposta e passa il contatto all'**Agente agenda** e all'**Agente brief**. L'agenda propone tre orari dai calendari M365; l'invito parte dopo il sì, con l'avviso di registrazione.
3. La sera prima, l'Agente brief (sessione Agent SDK) legge SersanOutreach, la memoria e il web via Firecrawl, chiede alla skill delle slide il deck per noi e lo mette nella cartella del cliente. Alessandro lo legge sul telefono, o lo apre in Claude Team e fa domande.
4. La call è in Teams, organizzata da noi: nessun bot. La trascrizione di Teams arriva sul server con Graph; n8n fa partire **Analista chiamate** e **Post-call**. Dieci minuti dopo: recap nel canale del cliente, meeting e deal in SersanOutreach, to-do in Jira, bozza della mail in carta.
5. L'**Agente proposte** prepara la bozza su Opus; Michele la rifinisce in Claude Team con il catalogo e la firma tecnica.
6. Le obiezioni sentite in call finiscono nella bacheca del Marketing. Alberto, nel progetto Marketing di Claude Team, chiede al Copywriter i post della settimana.
7. Dopo la firma, il **Project manager** apre il progetto in Jira, l'**Onboarding** prepara canale e cartella dopo la carta, e il giro continua fino alla fattura e al caso studio.

Ogni passaggio fra agenti è una riga della bacheca e un messaggio nel canale Teams "Agenti", firmato con il nome dell'agente [non verificato: proposta; il bot che posta nei canali è necessario perché Graph non lo permette a un'app, verificato in ricerca/29 §5.3].

---

## 7. Copertura voce per voce

**Come leggere la tabella.** "Da sola" giudica la Proposta 3 pura: Claude Team con i connettori, i lavori n8n via LiteLLM, il Cancello con le carte in Teams e i pochi agenti Agent SDK. "Sì" vuol dire che la voce è coperta per intero con questi pezzi. "In parte" vuol dire che serve un'aggiunta, oppure che mancano dati che oggi non ci sono. "No" vuol dire che senza un'aggiunta la voce non si fa. Le aggiunte A-G sono descritte nel §8. Tutta la tabella è una valutazione [non verificato], costruita sui fatti dei §2-§6.

| Voce | Come la fa la Proposta 3 | Da sola | Cosa serve aggiungere | Fase |
|---|---|---|---|---|
| J1 Un solo sistema multi-agente collegato | Memoria comune (MCP RAG, Postgres, BookStack), Cancello unico, catene n8n | In parte | A: bacheca dei passaggi, registro delle squadre | P1-P3 |
| J2 Ogni squadra ha compito e responsabile | Registro dei profili in git; un team LiteLLM e un progetto Claude Team per squadra | Sì | | P2 |
| J3 Outreach con agenti specializzati | Agente email, LinkedIn, Sentinella (N), Operatore (S) | Sì | | P2 |
| J4 Email parla con proposte, che parla con chiamate | Catene fisse in n8n | In parte | A: passaggi liberi fra agenti nella bacheca, con il freno | P3 |
| J5 L'agente entra in ogni call e trascrive | Nostre riunioni Teams: trascrizione nativa via Graph | In parte | C: Vexa per Teams di altri, Meet e Zoom; telefono per il dal vivo | P1-P2 |
| J6 Brief prima e dopo, slide per noi e per il cliente | Agente brief (S) con skill delle slide; Slides e Design di Claude Team | Sì | | P2 |
| J7 Marketing con outreach e con lo Studio | Progetti Marketing e Studio in Claude Team, lavori N su Firecrawl e KPI | In parte | E: Metricool, Higgsfield e gli altri strumenti come eccezioni, oppure i sostituti | P0-P2 |
| J8 Squadra progetti e task | Jira con account di servizio; Project manager (S); lavori N | Sì | | P1-P3 |
| J9 Chat di gruppo come Buzz, con Slack, Telegram, WhatsApp | Claude Team non è una chat di gruppo con agenti; Claude in Teams è in lista d'attesa | No | B: Porta chat in Teams; Telegram, WhatsApp e Slack come eccezioni; pilota Buzz in LAB | P3-P5 |
| A1 Tutte le riunioni registrate e trascritte | Teams via Graph, con avviso | In parte | C: Vexa, trascrizione in casa, telefono via NetBird | P1-P2 |
| A2 Memoria relazionale | BookStack per i testi, Postgres per i dati, MCP memoria | Sì | | P1-P2 |
| A3 Memoria vettoriale | Qdrant con BM25 e reranker, MCP RAG (board) | Sì | | P2 |
| A4 Orchestratore sul nostro server | n8n più motore leggero su Agent SDK, sul DL380; Hermes non serve | Sì | | P1-P2 |
| A5 Agenti per raccolta, pulizia, indicizzazione, azione | Pipeline del board più ingressi n8n; agenti N e S | Sì | | P2 |
| A6 Agenti che migliorano le skill | Skill in git, distribuite a Claude Team e all'SDK | In parte | A: agente revisore che propone modifiche, sì di una persona | P3 |
| A7 Chat fra agenti leggibile da noi | | No | A + B: bacheca mostrata nel canale Teams "Agenti" | P3 |
| B1 Punti e prossimi passi nel canale del cliente | Recap del Post-call postato dal bot nel canale Teams del cliente | Sì | canale condiviso con il cliente da provare | P1 |
| B2 Opportunità nel CRM | Esecutore del Cancello sull'MCP operatore di SersanOutreach | Sì | | P1-P2 |
| B3 Mail di follow-up | Bozza, carta, invio con Outlook via Graph | Sì | | P1 |
| B4 To-do al team | Jira, scrittura interna del Cancello | Sì | | P1 |
| B5 Autonomia crescente | Cancello v1 senza regole "Sempre" | In parte | Cancello parte 2: regole "Sempre" dopo 20 sì senza modifiche | P3 |
| C1 Debrief del mattino | Lavoro N alle 7:00, numeri da Postgres, chat 1:1 di Teams e mail | Sì | | P1 |
| C2 Un agente in ogni call, anche al posto di chi manca | Registrazione automatica delle nostre riunioni Teams (da provare senza nessuno di SerSan) | In parte | C: Vexa per le call degli altri | P1-P2 |
| C3 Analisi strutturata della call | Estrazione a schema via LiteLLM; analisi libera in Claude Team | Sì | | P1 |
| C4 Dettatura | Dettatura delle app Claude | Sì | C per le note vocali trascritte in casa | P0-P2 |
| C5 Registro di tutti i meeting | Tabella `meetings` in Postgres, Grafana, MCP memoria | Sì | | P1 |
| C6 Regole di lavoro lette dagli agenti | Pagina "Come lavoro" in BookStack; istruzioni dei progetti Claude Team | Sì | | P0-P2 |
| D1 Pipeline pesata sullo storico | Probabilità calcolate dal codice sugli eventi di SersanOutreach | In parte | dati: oggi 0 deal vinti; pesi dichiarati finché le chiusure non sono 30-50 | P4 |
| D2 Brief dall'email della persona | Agente brief (S) e progetto Vendite in Claude Team | Sì | aperture delle mail quando l'email è attiva | P2 |
| D3 Storico della relazione nel brief | MCP RAG con filtro cliente | Sì | | P2 |
| D4 Slide automatiche | Slides e Design di Claude Team, skill con il nostro template | Sì | | P0 |
| D5 Offerta dal catalogo | Agente proposte su Opus, catalogo in BookStack e Postgres | Sì | | P2 |
| E1 Tempo per imparare e costruire | Piano a fasi con giorni dichiarati (§9) | Sì | | P0 |
| E2 Costruire ora | Valore da subito con Claude Team | Sì | | P0 |
| E3 Policy AI e banca dei token | LiteLLM con budget per agente, squadra e persona (stop vero) | In parte | F: per i posti Claude Team solo statistiche d'uso; tetti per persona da verificare (§2) | P1-P3 |
| E4 Formazione | Programma su Claude Team per tutti e quattro | Sì | | P0 |
| F1 Metadati del lavoro, con tutele | Report e log di M365 al posto di Google Workspace, solo aggregati | In parte | scelta delle API di M365 da fare [non verificato] | P3 |
| F2 Interviste guidate | Progetto "Intervista" in Claude Team | Sì | | P0-P3 |
| F3 Mappa dei processi | Mappatore (S), mappa in BookStack | Sì | | P3 |
| F4 Ore per processo e automazioni consigliate | Ore in Postgres, classifica mensile | Sì | | P3 |
| F5 AI per tutti | Claude Team per tutti; Open WebUI del board sui modelli locali | Sì | | P0 |
| G1 Ogni call di vendita in un canale | Canale Teams "Call di vendita", postato dal bot | Sì | | P1 |
| G2 Fit score del prospect | Qualificatore di SersanOutreach esteso alle call | In parte | dati di chiusura che oggi mancano | P4 |
| G3 Valutazione della call e consigli | Lavoro N dopo ogni call di vendita, senza stima delle emozioni | Sì | parere legale | P4 |
| G4 Report a chi ha fatto la call | Chat 1:1 di Teams; aggregati al responsabile | Sì | | P4 |
| G5 Andrea richiama in 90 secondi, 24/7 | | No | D: Asterisk, Pipecat, operatore italiano, voce in casa | P4 |
| G6 Andrea impara dai rifiuti | | No | D: analisi settimanale, aperture nuove in carta, prova A/B | P4 |
| G7 Più conversione, risposte più veloci | Tempi di risposta nel debrief | In parte | D per la richiamata in 90 secondi | P4 |
| G8 Vinti e persi al marketing | Analista vinto/perso (N) | Sì | servono deal chiusi | P2 |
| G9 Agenti in organigramma, fino a cento | Registro dei profili | In parte | F: organigramma in Grafana e BookStack; cento agenti = più profili, non più RAM, con il tetto di 6 sessioni | P3 |
| G10 Superpotere individuale e aziendale | Claude Team per la persona; memoria e Cancello per l'azienda | In parte | A + B per la parte di squadra | P3 |
| H1 Formarsi e sperimentare | Claude Team, skill, Cowork | Sì | | P0 |
| H2 Non delegabile, a partire dai CEO | Carte e Claude Team ogni giorno per i CEO | Sì | | P0 |
| H3 Assessment delle competenze | Progetto in Claude Team | Sì | | P0 |
| H4 Ambassador con più risorse | Posto premium e budget LiteLLM più alto per Mattia | Sì | | P0 |
| H5 Tutti costruiscono qualcosa | Skill, progetti e compiti programmati personali in Claude Team | Sì | | P0 |
| H6 Premio mensile | Classifica da registro e statistiche d'uso | Sì | | P1 |
| H7 Cambiare il modo di lavorare | Programma di adozione | Sì | | P0 |
| I1 Il contesto fa la qualità | MCP RAG e regole personali | Sì | | P2 |
| I2 Oltre la versione base | Skill, connettori, istruzioni dell'organizzazione | Sì | | P0 |
| I3 Aree in cui l'AI non entra | Classi negate nel Cancello; strumenti di scrittura spenti nei connettori | Sì | | P1 |
| I4 Marketing dal ripetitivo al creativo | Progetti Marketing e Studio in Claude Team | Sì | | P0 |
| K1 Debrief come primo appuntamento | Evento in Outlook creato dall'esecutore | Sì | | P1 |
| K2 Un agente fissa gli appuntamenti che gli altri trovano | Agente agenda (S) | In parte | A: gli annunci "ho trovato tre nuove call" passano dalla bacheca | P2-P3 |
| K3 Posta smistata con risposte pronte | Smistatore posta (N): delta di Graph, caselle limitate, bozze in carta | Sì | | P2 |
| K4 Chiedere cosa si è detto in una call | MCP RAG da Claude Team; connettore M365 per le call Teams | Sì | | P2 |
| K5 Brief di intake e onboarding dei potenziali clienti | Agente intake (N) | Sì | | P2 |
| K6 Slide che raccontano la relazione | Brief più skill delle slide | Sì | | P2 |
| K7 Slide e documenti con il nostro stile | Skill dell'organizzazione con i template SerSan | Sì | | P0 |
| K8 Portale clienti con Claude Code | Claude Code delle persone su SersanOutreach | Sì | | P4 |
| K9 Agente che costruisce la newsletter | Agente newsletter (N) | In parte | E: strumento di newsletter (Listmonk in casa) e un relay SMTP | P3 |
| K10 Andrea risponde anche in entrata | | No | D: gruppo di squillo, risposta fuori orario, esito nel CRM | P4 |
| K11 Perché una lead si chiude, e altre simili | Vinto/perso (N) e clienti simili (S) | Sì | servono deal chiusi | P2-P4 |
| K12 Formazione continua dei commerciali | Coach vendite, piano mensile | Sì | | P4 |
| K13 Mappa e assessment anche per i clienti | Mappatore e Intervistatore riusati per la linea 04 | Sì | | P3-P5 |
| K14 Dati finanziari e obiettivi nella memoria | Obiettivi in Postgres | In parte | export strutturato di Sirius verso Postgres; decisione sui dati rossi | P2-P5 |
| K15 Acquisti automatizzati | Registro delle fatture dei fornitori e dei rinnovi | In parte | E: strumento di contabilità; il pagamento resta umano | P5 |
| K16 Assistente personale, salute fuori dall'azienda | | In parte | E: account Claude personale per chi lo vuole, fuori dall'organizzazione | P5 |
| L1 Contratto con firma elettronica | | No | E: firma elettronica (DocuSeal in casa o un servizio esterno) | P5 |
| L2 Fatture, incassi, solleciti | | No | E: strumento di fatturazione (Sirius o altro) collegato al Cancello | P5 |
| L3 Margini, cassa, distanza dagli obiettivi | Numeri calcolati in Postgres | In parte | export strutturato di Sirius | P5 |
| L4 Bandi per noi e per i clienti | Pipeline bandi del board, notifica in Teams | Sì | | P2 |
| L5 Assistenza nella stanza del cliente | Lavoro N sulla posta e sul canale del cliente, risposta in carta | In parte | canale condiviso di Teams con il cliente da provare | P5 |
| L6 Rinnovi e clienti a rischio | Agente rinnovi (N) | Sì | | P5 |
| L7 Caso studio da ogni progetto | Agente casi studio (N) | Sì | | P5 |
| L8 Risposte sulla pagina aziendale | Community manager (N) | In parte | E: lettura dei commenti con Metricool (eccezione) o con l'API di LinkedIn | P3 |
| L9 Sito, articoli e SEO | Claude Code con pull request; deploy umano su Vercel | Sì | | P5 |
| L10 Webinar ed eventi | Inviti e iscrizioni in SersanOutreach | In parte | webinar di Teams, se il piano M365 li include [non verificato] | P5 |
| L11 Agente che sorveglia il server | Sistemista (N) su OBSRV | Sì | | P2 |
| L12 Allenatore per usare meglio gli agenti | Allenatore AI (N) su registro e statistiche d'uso | Sì | | P5 |

**Riepilogo.** Su 90 voci: **59 Sì, 24 In parte, 7 No**. Le 7 voci "No" sono J9, A7, G5, G6, K10, L1 e L2. Delle 24 "In parte", D1 e G2 aspettano dati di vendita che oggi non ci sono; K14 e L3 aspettano l'export strutturato di Sirius; le altre 20 aspettano un'aggiunta del §8. Con le aggiunte A-G **tutte le 90 voci sono coperte** [non verificato: valutazione; conteggio fatto sulla tabella].

---

## 8. Cosa serve aggiungere per coprire tutto

| Aggiunta | Cosa copre | Componenti | Dove gira | Costo al mese | gp di base | Fase |
|---|---|---|---|---|---|---|
| **A. Bacheca e squadre che si parlano** | J1, J4, A6, A7, K2, G10 | Tabelle `compiti` e `passaggi` in Postgres; MCP bacheca (crea, prendi, aggiorna, passa, chiudi); freno ai giri; vista nel canale Teams "Agenti" e specchio facoltativo in Jira; Capo di gabinetto in Claude Team con il connettore bacheca; agente revisore delle skill | VM agenti-01, Postgres | 0 € | 6 | P3 |
| **B. Chat di gruppo** | J9, A7 | **Porta chat**: Chat SDK di Vercel (MIT) con gli adattatori Teams, Telegram, WhatsApp e Slack, più il Teams SDK per le carte [verificato: ricerca/28 §2.2]. Un bot "Agenti SerSan" con il nome dell'agente in ogni messaggio; thread = sessione; comandi `/stop` e `/stato` | VM agenti-01 | Teams 0 € se è nel piano M365 [non verificato]. **Telegram**: 0 €, eccezione da approvare [verificato: ricerca/28]. **WhatsApp Cloud API**: circa 7-12 € per 300 messaggi, 1.000 di servizio gratis al mese per numero, numero dedicato e verifica Meta, eccezione [verificato: ricerca/28 §6; stima in ricerca/33]. **Slack**: workspace Free 0 € o Pro 27,00 € per 4 persone (prezzo del 24/10/2026), eccezione [verificato: ricerca/33 §2.1]. **Buzz**: 0 € di licenza, pilota in LAB | 4 (Porta v2) + 1,5 (Telegram) + 2,5 (WhatsApp) + 1,5 (Slack) + 4 (Buzz) = 13,5 | P3-P5 |
| **C. Agente nelle call** | J5, A1, C2, C4 (note vocali) | Vexa 0.12.x in una VM e VLAN dedicate; servizio di trascrizione (faster-whisper turbo dal vivo, Parakeet v3 o WhisperX con pyannote a lotti); telefono via NetBird; riserva con la registrazione sul PC [verificato: ricerca/30 §10] | VLAN MEET, VLAN 80 | 0 € di licenze; facoltativo un vivavoce da sala 100-250 € una volta [non verificato: ricerca/30] | 19 (più 3,5 di impostazioni Teams e raccoglitore, già in P1) | P1-P2 |
| **D. Voce di "Andrea"** | G5, G6, G7, K10 | Asterisk 22 LTS, Pipecat, Parakeet e Pocket TTS su CPU, Claude Haiku 5.5 via LiteLLM con il pensiero spento, operatore italiano Messagenet; voce migliore con la seconda GPU [verificato: ricerca/31 "In breve"] | VLAN VOCE, 30 APPS, 80 AI | 44,24-90,43 € (operatore, Registro delle opposizioni, Claude) [non verificato: calcolo di ricerca/33 §2.3]. **Operatore telefonico: necessità esterna da aggiungere al board** | 24 + 4 per la GPU | P4 |
| **E. Strumenti esterni e sostituti** | J7, K9, K15, K16, L1, L2, L8, L10 | Vedi tabella sotto | | Vedi tabella sotto | compresi nelle fasi | P0-P5 |
| **F. Organigramma e banca dei token completi** | E3, G9 | Registro in Postgres, cruscotti in Grafana, pagina BookStack rigenerata ogni notte; budget LiteLLM per persona; lettura mensile delle statistiche d'uso di Claude Team | VLAN 70, 30 | 0 € | 2,5 | P3 |
| **G. Runner self-hosted di Claude Code** (facoltativo) | rende più sicuri H5, K8, L9 e i compiti programmati delle persone | Un runner per persona, solo in uscita verso Anthropic | VLAN 50 CICD | 0 € di licenza; consuma l'uso dei posti [verificato: code.claude.com/docs/en/self-hosted-environments] | 2, da aggiungere a P2 solo se scelto (fuori dal totale del §9) | P2 |

**E in dettaglio: strumenti fuori dal board.** Ognuno è scritto come necessità, con il suo costo. Decide Michele se ammetterlo come eccezione; i sostituti in casa sono indicati dove esistono.

| Strumento | A cosa serve | Costo al mese | Sostituto in casa | Etichetta |
|---|---|---|---|---|
| Metricool | Programmazione dei post e metriche; connettore già in uso in Claude | 59,86 € | Postiz (AGPL-3.0) | prezzo [verificato: PRESENTAZIONE-CEO.md §12.1, 24/10/2026]; Postiz [verificato: ricerca/25 N08] |
| Apollo | Ricerca di contatti B2B | 43,78 € | nessuno; arricchimento di SersanOutreach | [verificato: ricerca/25 N08] |
| Apify | Segnali di assunzione | 15,19 € | Firecrawl del board | [verificato: ricerca/25 N08]; copertura di Indeed [non verificato] |
| moda.app | Slide | 26,80 € | Slides e Design di Claude Team, già inclusi | [verificato: claude.com/pricing/team] |
| Higgsfield | Video e immagini per i post | 41,99 € | nessuno di qualità sulla RTX 4000 | [verificato: ricerca/25 N08] |
| Newsletter (K9) | Invio e aperture | Listmonk: 0 € di licenza (AGPL v3, usa PostgreSQL) più un relay SMTP esterno, prezzo da scegliere | Listmonk sul server, in APPS | Listmonk [verificato: github.com/knadh/listmonk, 25/10/2026]; relay [non verificato] |
| Firma elettronica (L1) | Contratti in firma dopo il sì | DocuSeal in casa: 0 € (AGPLv3 con condizioni aggiuntive; API e webhook; promemoria automatici, ruoli e SSO solo nella versione Pro a pagamento) | DocuSeal in APPS, con PostgreSQL | [verificato: github.com/docusealco/docuseal, 25/10/2026]; prezzo della Pro e valore legale della firma [non verificato] |
| Fatturazione (L2) | Fatture, incassi, solleciti | da conoscere | forse Sirius | [non verificato: domanda aperta a Michele] |
| Account Claude personale (K16) | Assistente personale con i dati di salute fuori dall'azienda | Claude Pro 17 $ al mese con fatturazione annuale (15,19 €), 20 $ mensile (17,87 €), a persona, per chi lo vuole | nessuno | [verificato: claude.com/pricing, 25/10/2026] |
| Operatore telefonico (D) | Numero e chiamate di Andrea | 30,00-76,19 € | non esiste in casa | [verificato: ricerca/31 §12] |
| VPS per Pangolin | Endpoint pubblici senza porte aperte in casa | da 6,49 € | porte aperte verso EDGE con l'IP fisso | [verificato: hetzner.com/cloud, 25/10/2026; ricerca/25 N10] |

---

## 9. Piano per fasi

**Capacità assunta.** Alberto circa 4,5 gp a settimana, Mattia 1,5-2,5, Michele circa 0,5 sul progetto oltre al board: **6,5-7,5 gp a settimana** [non verificato: ipotesi di ricerca/22 §5 e ricerca/30 §11.1, da confermare]. Le settimane sotto usano il valore più prudente, con la riserva.

**Cosa non contiamo.** Le fasi F0-F3 del board (arrivi, fondamenta, uscita da Azure, sicurezza) e i pezzi F4 del board (LXC GPU, pipeline Sirius verso MCP, Firecrawl con n8n, LiteLLM con budget) li porta avanti Michele [verificato: board, roadmap]. Qui contiamo solo il lavoro in più. Il board non ha date: le settimane delle fasi P1-P2 dipendono da quando Michele chiude F2 e F4 [verificato: ricerca/25 §6].

| Fase | Settimane | Dipende dal board | Cosa si fa | gp base | gp con riserva | Cosa vedete alla fine |
|---|---|---|---|---|---|---|
| **P0 · Claude Team subito** | 1-4 | nulla: in parallelo a F0-F1 | SSO con Entra e controlli dell'amministratore (0,5); connettori Microsoft 365 in sola lettura, Atlassian, Metricool se ammesso (1); un progetto condiviso per squadra con le istruzioni (1); skill dell'organizzazione: voce del brand in italiano e inglese, template di slide e documenti, formato del recap e del brief, offerta dal catalogo, controllo delle regole di brand (2,5); modello "Come lavoro" e prima versione per quattro (0,5); formazione e assessment (1). Solo dati verdi e gialli | 6,5 | 8,5 | Tutti e quattro lavorano in Claude Team ogni giorno. Calendario dei post pieno fino a Natale. Prime offerte e slide con il nostro stile |
| **P1 · Prese MCP, Cancello e primi lavori** | 5-11 | Postgres 16, n8n, rotta Pangolin e LiteLLM in un "posto agenti" anticipato in F2; altrimenti la fase parte dopo F3 | Cancello v1: regole, carte, esecutori Outlook e Jira, audit (10); Porta chat v1: bot Teams con carte Action.Execute e chat 1:1 (4); LiteLLM: chiavi, team, budget, prova degli header (1); MCP memoria (2,5); OAuth con Entra davanti ai server MCP e prova dai server di Anthropic (2,5); SersanOutreach in HTTP con OAuth come connettore (2,5); registrazioni Graph, Sites.Selected, RBAC di Exchange (2,5); Jira per gli agenti (1,5); impostazioni delle trascrizioni Teams e raccoglitore via Graph (3,5); debrief, Analista chiamate, Post-call, Agente task, registro dei meeting (4,5) | 34,5 | 46 | Dopo ogni call Teams: recap nel canale del cliente, to-do in Jira, bozza della mail in carta sul telefono. Debrief alle 7:00. Claude Team legge CRM e regole. **Verifica di fine P1** |
| **P2 · Memoria e agenti veri** | 12-22 | F4 del board: LXC GPU, pipeline, Firecrawl, LiteLLM | Motore leggero su Agent SDK: runner, profili, ponte verso il Cancello, isolamento, osservabilità, collaudo (13); MCP RAG con filtri per colore e per persona (2,5); ingressi della pipeline da BookStack, Jira, SharePoint, Outlook e trascrizioni (4); BookStack con MariaDB e MCP in lettura (2); aggiunta C, agente nelle call (19); contenuto e flussi di 16 agenti: brief, proposte, agenda, operatore, email, LinkedIn, sentinella, smistatore posta, intake, vinto/perso, concorrenza, metriche, editoriale, archivista, sistemista, bandi (15) | 55,5 | 74 | Brief la sera prima. Offerta in bozza entro un'ora. Posta smistata. Bot nelle call dei clienti. Claude Team risponde bene ad almeno 8 domande su 10, su 50 domande in italiano preparate da noi |
| **P3 · Squadre che si parlano e chat di gruppo** | 23-28 | nessuna nuova | Aggiunta A, bacheca (4) e revisore delle skill (2); aggiunta B, Porta chat v2 (4) e Telegram (1,5); aggiunta F, organigramma (1) e banca dei token (1,5); Cancello parte 2: regole "Sempre", freno per catena, stop di emergenza, pausa delle campagne (6); agenti: project manager, report cliente, onboarding, newsletter con Listmonk, community manager, capo di gabinetto, mappatore, intervistatore (7,5) | 27,5 | 36,5 | Gli agenti si passano il lavoro nel canale "Agenti". Il Capo di gabinetto smista da Claude Team e da Teams. Organigramma con i 57 agenti e i loro costi |
| **P4 · Vendite e voce** | 29-36 | F5 per la seconda GPU, facoltativa | Aggiunta D, Andrea su CPU (24) e con la seconda GPU (4); pipeline pesata e portale clienti con Claude Code (4); coach, fit score, clienti simili (3); WhatsApp (2,5). Solo con il parere legale e lead vere | 37,5 | 50 | Una lead di prova richiamata entro 90 secondi, appuntamento nel CRM. Esiti di Andrea nel canale vendite |
| **P5 · Le altre automazioni** | 37-42 | nessuna | Amministrazione: fatture, acquisti, controllo di gestione, bandi per i clienti (8); contratti con firma elettronica (3); assistenza, rinnovi, casi studio (4); sito e SEO (2,5); eventi e webinar (2,5); allenatore AI e assistente personale (2); pilota Buzz in LAB (4); Slack come eccezione (1,5); pilota Paperclip in LAB (2) | 29,5 | 39 | Dal contratto all'incasso senza lavoro a mano. Ogni progetto chiuso diventa un caso studio |
| **Totale** | **1-42** | | | **191** | **254** | |

[non verificato: tutte le stime; i giorni di C e D vengono da ricerca/30 §11 e ricerca/31 §11, quelli del motore da ricerca/26 §10.2 senza la chat, quelli della conoscenza da ricerca/29 §10 senza il bot]

**Il calendario in breve.** 30-42 settimane per tutto, a seconda della capacità reale. Il nucleo della proposta (P0-P2) è pronto alla settimana 22, con circa 96,5 gp di base. La fase P0 dà valore dalla prima settimana e non chiede nulla al server.

**Verifica alla fine di P1 (settimana 11).** La fase P2 parte se [non verificato: proposta]:
- tutti e quattro usano Claude Team ogni giorno (statistiche d'uso);
- i connettori MCP rispondono dai server di Anthropic, con l'identità di ciascuno e il registro delle query;
- il recap arriva entro 15 minuti per tutte le call Teams del periodo;
- nessun effetto è uscito senza una carta del Cancello;
- ogni carta porta l'identità Entra di chi l'ha approvata;
- la spesa è rimasta nei tetti di LiteLLM.

Se un criterio fallisce, vale il piano B del §11 per quel pezzo, senza buttare il resto.

---

## 10. Costi

### 10.1 Al mese, in più rispetto a oggi

Stesso metodo della presentazione e del rapporto 33: costi nuovi, senza il kit commerciale, con le API dentro i crediti finché durano e Claude Team gratuito nel primo anno. Prezzi IVA esclusa del 24-25/10/2026.

| Periodo | € al mese in più | Cosa comprende |
|---|---|---|
| P0-P1, Azure ancora acceso | **≈ 135,27** | Proxmox 20,00, IP fisso 10,00, corrente del server e del firewall 105,27 [non verificato: ricerca/33 §3.1] |
| Dopo lo spegnimento di Azure (F2) | **≈ −14,73** | come sopra, meno circa 150 € di Azure [non verificato: ricerca/33] |
| P1-P3 con gli agenti | **≈ 13,54-20,03** | più Jira Standard 28,27 se il piano Free non basta; più 6,49 se Pangolin va su un VPS |
| P4 con Andrea | **≈ 57,78-110,46** | più 44,24-90,43 per Andrea |
| Fine dell'anno gratuito di Claude Team | **≈ 550,67-557,16** | più 446,70 con 5 posti premium (100 $ a posto); 357,36 con 4 premium; 214,42 con 2 premium e 2 standard [verificato per i prezzi: claude.com/pricing/team; calcolo non verificato] |
| Anche senza crediti API | **≈ 746,32-752,81** | più 195,65 di API stimate [non verificato: ricerca/22 §6] |
| Instantly, se oggi non è pagato | **+ 69,33** a ogni riga | [verificato: ricerca/33 §2.2] |

**Listino mensile dello scenario consigliato:** circa **525,44 €** (518,95 € del rapporto 33 più il VPS), contro i 968 € della presentazione [non verificato: calcolo].

**Due differenze della Proposta 3 sui costi.**
- **Le API possono scendere.** Molto lavoro delle persone gira sui posti Claude Team, già pagati; i lavori n8n usano soprattutto chiamate semplici. La stima di 195,65 € resta come tetto prudente [non verificato: ricerca/25 §5.1].
- **I posti contano di più.** Claude Team diventa lo strumento di ogni giorno: alla fine del bundle conviene tenere i 5 posti premium, perché i compiti programmati e le sessioni cloud consumano l'uso del posto [verificato: code.claude.com/docs/en/routines]. Oltre il limite servono i crediti d'uso a consumo, che l'amministratore accende per l'organizzazione [verificato: idem]; il prezzo a consumo [non verificato].

**Eccezioni facoltative, fuori dai totali:** kit commerciale fuori dal board fino a 187,62 € (Metricool, Apollo, Apify, moda.app, Higgsfield); Slack 0-27,00 €; WhatsApp circa 7-12 €; Teams se manca dal piano M365 5,72-14,29 €; utente di servizio M365 6,41 €; account Claude personale per l'assistente personale 15,19-17,87 € a persona; relay SMTP della newsletter, prezzo da scegliere [verificato per i prezzi: ricerca/33 §2.2 e §2.5, claude.com/pricing; relay non verificato].

### 10.2 Una tantum

| Quando | Voce | Importo IVA esclusa | Etichetta |
|---|---|---|---|
| Subito | PBS a casa (Lenovo M920t e 2 dischi) | 382-730 € | [non verificato: ricerca/33 §4.1] |
| Subito | Chiavi FIDO2, 8 chiavi | 232-464 € | [verificato: ricerca/33 §4.1, store Yubico] |
| Subito | Parere legale unico, con i temi nuovi (dati di Claude Team, trascrizioni, Andrea) | tetto 2.500 € | [verificato: PRESENTAZIONE-CEO.md §14] |
| Subito | Piccoli accessori, se mancano | 0-200 € | [non verificato] |
| Subito | Credito API prepagato, se i crediti finiscono | 0-223 € | [verificato: ricerca/33 §4.1] |
| **Subtotale subito** | | **≈ 3.114-4.117 €** | [non verificato: calcolo] |
| Fase P4 | Attivazione del numero di Andrea | 7-14 € | [verificato: ricerca/33] |
| Fase P2, facoltativo | Vivavoce da sala per le riunioni dal vivo | 100-250 € | [non verificato: ricerca/30] |
| F5 del board | Seconda GPU RTX 2000 Ada 16 GB | 686-893 € | [verificato: ricerca/33 §4.2] |
| F5 del board | UPS rack 2U | 1.011-1.060 € | [verificato: ricerca/33 §4.2] |
| F5 del board | RAM, fino a 4 moduli | 0-400 € | [non verificato] |
| **Subtotale F5** | | **≈ 1.697-2.353 €** | [non verificato: calcolo] |
| Solo se il margine di RAM finisce | 12 moduli, 384 GB | 816 € (Servermall, moduli 2133) o £1.020 (Bargain, moduli 2666) | [verificato: ricerca/32 §2.3]; probabilmente evitabile con il tetto di 6 sessioni (§3.3) |

Il pagamento del server a Bargain non è nei file [verificato: ricerca/33 §4.1].

---

## 11. Rischi e come si esce

| Rischio | Effetto | Cosa facciamo | Come si esce se non regge |
|---|---|---|---|
| **Funzioni di Claude Team in anteprima o in beta** (compiti programmati, ambienti self-hosted, Cowork sul web) [verificato: §2] | Cambiano o spariscono | Le funzioni che contano stanno sul server: memoria, Cancello, bacheca, lavori n8n. Claude Team è la finestra | Si passa alla finestra di riserva: Teams con la Porta chat per parlare con gli agenti, Open WebUI del board per la chat sui modelli, Claude Desktop via mesh. È lo stesso server delle proposte centrate sul motore |
| **Dati rossi a Claude Team** (documenti dei clienti, dati fiscali). Team non ha conservazione personalizzata né ZDR [verificato: claude.com/pricing/team; ricerca/25 N17] | Rischio GDPR e contrattuale | MCP RAG dà a Claude Team solo verde e giallo, e il rosso oscurato, finché il parere legale non decide; il rosso intero va solo agli agenti sul server via API, dopo l'oscuramento locale [verificato: regola dei tre colori, PRESENTAZIONE-CEO.md §5.6] | Collezione `finanza` separata in Qdrant: si toglie dall'accesso di Claude Team con una regola, senza rifare nulla |
| **Endpoint pubblici per i connettori** [verificato: support.claude.com 11175166] | Una porta in più verso internet | OAuth con Entra sui server MCP, accesso condizionale sugli IP di Anthropic, rotte strette in Pangolin, registro delle query | Claude Desktop via NetBird e runner self-hosted per le sessioni Code: niente MCP dal telefono, ma nessuna rotta pubblica |
| **I compiti programmati agiscono a nome della persona** [verificato: code.claude.com/docs/en/routines] | Una scrittura fuori dal Cancello | Connettori nostri senza strumenti di scrittura; M365 in sola lettura; gli Owner possono spegnere i compiti programmati per tutti [verificato: idem] | Spegnerli e lasciare gli automatismi a n8n |
| **Team senza log di audit e senza ruoli** [verificato: claude.com/pricing/team] | Non si vede in Claude Team chi ha fatto cosa | L'audit sta nel Cancello e nei registri dei server MCP in Loki | Passaggio a Enterprise, con preventivo [non verificato: prezzo] |
| **Limiti d'uso dei posti** | Le persone si fermano a metà giornata | Posti premium (5 volte lo standard); lavori pesanti sugli agenti via API; crediti d'uso a consumo con un tetto [verificato: claude.com/pricing/team; code.claude.com/docs/en/routines] | Spostare i lavori ripetitivi da Claude Team a n8n |
| **Bot Teams senza Azure** [verificato: ricerca/28 §2.2] | Le carte non arrivano | Prova di un giorno nella fase P1 | Azure Bot F0 gratuito (decide Michele) oppure la pagina del Cancello dietro Pangolin con Entra e FIDO2, con l'avviso in Teams |
| **Il board non ha date; LiteLLM arriva in F4** [verificato: ricerca/25 §6] | La fase P1 slitta | Chiedere a Michele un "posto agenti" anticipato in F2 | P0 continua su Claude Team; su stage si parte con una chiave diretta con tetto nella Console [verificato: ricerca/26 §10.3] |
| **LiteLLM non inoltra un header `anthropic-beta`** [verificato: ricerca/26 §4.2] | Una funzione dell'SDK si rompe | Prova di accettazione a ogni aggiornamento | Chiave diretta per famiglia di agenti, con tetti nella Console |
| **Agent SDK con rilasci quasi quotidiani** [verificato: ricerca/26 §1.1] | Comportamenti che cambiano | Versione fissata, aggiornamento ogni due settimane dopo 10 scenari, dentro la regola dei 14 giorni di Cyber Essentials | Il motore serve solo 10 agenti: si possono riportare per un periodo su lavori n8n più semplici |
| **Iniezioni di istruzioni** da mail, trascrizioni, pagine web, anche lette in Claude Team | Un'azione voluta da un estraneo | Nessuno strumento che invia; approvare non è uno strumento; testo di terzi letto senza strumenti [verificato: ricerca/26 §11] | Spegnere i connettori di scrittura e lasciare solo la lettura |
| **Squadre e chat costano quasi come nelle altre proposte** | Il vantaggio della Proposta 3 si riduce nelle fasi P3-P5 | Dichiararlo ai CEO: il guadagno sta nel valore subito e nei pezzi sempre accesi, non nel totale dei giorni | Le fasi P3-P5 sono le stesse del motore: si passa senza buttare nulla |
| **Hermes** | Michele chiede di confrontarlo [verificato: messaggio del 25/10] | Non serve in questa proposta | Pilota confinato in Experimental-2, 6-8 gp, se un giorno serve [verificato: ricerca/27 "In breve"] |
| **MinIO non più mantenuto** [verificato: ricerca/25 N14] | Fuori dalla regola del software supportato | Sostituto da scegliere con Michele prima di salvare l'audio | Garage o SeaweedFS [non verificato] |
| **RAM** | Margine stretto con tutto acceso | Tetto di 6 sessioni, cache ZFS a 12 GiB, runner Claude Code solo se c'è margine | 384 GB (§10.2) |
| **Tempo tolto ai clienti** | 191 gp di base sono molti | Fasi brevi con una verifica; P0 dà valore senza server | Ci si può fermare dopo P2 con il nucleo completo e decidere le aggiunte una per volta |

---

## 12. Domande aperte

**Per Michele**
1. Anticipi in F2 un "posto agenti" in APPS (PostgreSQL 16, n8n, LiteLLM, Infisical, rotta Pangolin per gli MCP)?
2. Pangolin su un VPS (da 6,49 € al mese) o in casa con porte aperte verso EDGE? Accetti le rotte `/mcp/*` raggiungibili dagli IP di Anthropic, con OAuth di Entra sui server?
3. Bot Teams "Teams-managed", Azure Bot F0 gratuito o pagina del Cancello?
4. Possiamo provare il runner self-hosted di Claude Code (beta) nella VLAN 50, con regole verso le sole porte MCP?
5. Che cosa sono Sirius, mcp-memory e mcp-enrich? Sirius è lo strumento di fatturazione (L2)?
6. Quali eccezioni ammetti: Metricool, Apollo, Higgsfield, Telegram, WhatsApp, Slack, l'operatore telefonico per Andrea, un relay SMTP per la newsletter?
7. Con cosa sostituisci MinIO?
8. Quali fasce orarie per la GPU, e quale seconda GPU da 16 GB?
9. Su quale piano sono oggi Jira e M365? Teams e i webinar sono inclusi? Chi è Global Administrator?

**Per Alessandro e i CEO** (solo budget)
10. A fine bundle teniamo 5 posti premium (446,70 € al mese) o un mix?
11. Dopo il parere legale: quali dati rossi può vedere Claude Team?

**Per Anthropic**
12. I 500 $ di crediti API in comune del piano Team valgono anche per la chiave API dietro LiteLLM? E gli 800 $ al mese del bundle si sommano?
13. Sul piano Team ci sono davvero i tetti di spesa per persona? La pagina dei prezzi si contraddice.
14. Chiediamo la conservazione zero per l'API, sapendo che esclude gli ambienti self-hosted di Claude Code?

---

## 13. Fonti

**Pagine lette il 25/10/2026**
- Claude Team, prezzi e funzioni: https://claude.com/pricing/team
- Claude, prezzi dei piani individuali: https://claude.com/pricing
- Connettori personalizzati con MCP remoti: https://support.claude.com/en/articles/11175166-about-custom-connectors-using-remote-mcp
- Compiti programmati in Cowork: https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- Compiti programmati di Claude Code: https://code.claude.com/docs/en/routines
- Ambienti self-hosted di Claude Code: https://code.claude.com/docs/en/self-hosted-environments
- Projects di Claude Code: https://code.claude.com/docs/en/claude-projects
- Hetzner Cloud, prezzi: https://www.hetzner.com/cloud/
- Listmonk: https://github.com/knadh/listmonk
- DocuSeal: https://github.com/docusealco/docuseal

**File del progetto**
- Board di Michele: `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`
- `ricerca/00-visione-funzionalita.md` (voci A1-L12)
- `PRESENTAZIONE-CEO.md` (§4 squadre e agenti, §5 Cancello e colori, §12 costi, §14 decisioni)
- `ricerca/01-sersanoutreach.md` (§5.1-5.2, server MCP)
- `ricerca/14`, `ricerca/18` (Claude Team, compiti programmati, Metricool), `ricerca/20-proposta-E-claude-native.md`, `ricerca/22-architettura-scelta.md`
- `ricerca/25-board-michele-e-delta.md`, `ricerca/26-claude-agent-sdk.md`, `ricerca/27-hermes-self-hosted.md`, `ricerca/28-chat-di-gruppo-self-hosted.md`, `ricerca/29-conoscenza-task-e-documenti.md`, `ricerca/30-call-e-trascrizione-self-hosted.md`, `ricerca/31-voce-andrea-self-hosted.md`, `ricerca/32-hardware-e-upgrade.md`, `ricerca/33-costi-v2.md`
