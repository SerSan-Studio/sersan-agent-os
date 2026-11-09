# 25 · Il board di Michele e le correzioni alla proposta

**Data:** 25/10/2026. **Per:** Alberto Tuveri, come base per la nuova versione di `PRESENTAZIONE-CEO.md`.
**Fonti principali:** il board dell'infrastruttura di Michele (`allegati/infra/`: `SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`, `SerSan Infra Board.html`), il suo messaggio ad Alberto del 25/10/2026, la proposta attuale (`PRESENTAZIONE-CEO.md`, salvata il 25/10/2026 alle 09:57), i rapporti 01, 13, 14, 15, 16 e 22, e ricerche web del 25/10/2026.
**Etichette:** [verificato: fonte] = letto nella fonte indicata; [non verificato] = stima, deduzione o voce di terzi non confermata. "Board" = il board di Michele, che è vincolante. "PCEO §x" = sezione x della proposta. Prezzi rilevati il 25/10/2026; IVA esclusa dove non è scritto altro.
**Come si usa:** ogni correzione ha un codice (C, H, S, N) per ritrovarla quando si riscrive la proposta. La regola guida è questa: nessuna funzione della visione si perde. Dove un servizio esce, il rapporto dice chi ne prende il posto, oppure lo segnala come eccezione da far decidere a Michele.

---

## In breve

Il board di Michele cambia la base della proposta in cinque punti. **Primo, il cloud si restringe:** restano solo M365 con Entra ID, Claude Team, l'API Anthropic dietro LiteLLM, Cloudflare per il DNS, GitHub, Supabase, Vercel, Jira, Instantly e uno spazio S3 fuori sede facoltativo; Azure esce, e "tutto il resto dev'essere self hosted". Quindi Slack, Notion, Google Workspace, Cloudflare Tunnel, Recall.ai, ElevenLabs con Twilio, Hermes Cloud, 1Password, Grok Bot, Telegram e WhatsApp escono dalla proposta oppure diventano eccezioni da far approvare a Michele. **Secondo, l'hardware è completo e più grande:** 192 GB di RAM, 2 CPU da 16 core, dischi, ventole, dissipatori e alimentatori sono già presenti; spariscono quasi tutte le spese una tantum della prima fase, mentre si aggiungono il Proxmox Backup Server a casa e, nella fase F5 del board, la seconda GPU e l'UPS da rack. **Terzo, la memoria cambia motore:** Qdrant con BM25 e reranker al posto di pgvector, PostgreSQL 16, BookStack e Jira al posto di Notion, e Claude Team che ragiona sui documenti tramite un MCP RAG con i permessi di chi chiede. **Quarto, l'orchestratore va rivalutato:** Michele preferisce l'Agent SDK di Claude a Hermes, e il board ha già LiteLLM, n8n e Open WebUI, che coprono una parte di ciò che Hermes dava. **Quinto, i tempi vanno allineati alla roadmap del board:** lo strato AI arriva nella fase F4, dopo rete, uscita da Azure e sicurezza, mentre la proposta mette il pilota degli agenti nelle settimane 4-8. In numeri, il listino mensile dello scenario consigliato scende da circa 968 € a 388-749 €, la spesa in più delle prime 8 settimane da circa 300 € a circa 102-125 €, e il budget una tantum chiesto oggi da 5.016 € a circa 3.010-3.530 € [stima, §5]. Restano da chiarire con Michele 21 punti (§7), raccolti in 18 domande (§8), tra cui la chat di gruppo, la voce di "Andrea", gli strumenti commerciali fuori dal board, il database di SersanOutreach, l'esposizione pubblica senza porte aperte, la GPU condivisa con i lavori notturni e il perimetro Cyber Essentials.

---

## 1. Cosa dice il board

| Area | Contenuto | Fonte |
|---|---|---|
| Cloud che restano | M365 / Entra ID (identità, MFA, posta); Claude Team ("ragiona sul RAG via MCP"); API Anthropic ("crediti · dietro LiteLLM"); Cloudflare (DNS); GitHub (repo, runner in casa); Supabase ("DB del prodotto"); Vercel (deploy clienti); Jira; Instantly (outreach); S3 fuori sede facoltativo (B2 o Hetzner). "Tutto l'IaaS generico (Azure) esce" | [verificato: SerSan Infra Board.md righe 9-13] |
| Regola generale | "Tutto il resto dev'essere self hosted"; valutare l'Agent SDK di Claude al posto di Hermes, senza escludere Hermes a priori | [verificato: messaggio di Michele, 25/10/2026] |
| Accesso | NetBird per team e admin (SSO Entra più chiave FIDO2, ACL per gruppo, funziona dietro il CGNAT di Starlink); Pangolin più Traefik per le app web dei clienti e per l'endpoint MCP di Claude Team, con autenticazione davanti; in alternativa Claude Desktop via mesh | [verificato: board righe 17-27] |
| Rete fisica | Rack VEVOR 12U in salotto; FTTH 2,5G con IP fisso da richiedere; router del provider in DMZ; OPNsense su Pentium 4417U con 4 porte (WAN, trunk VLAN 10-99, OOB per l'iLO, LAN ufficio); fa anche WireGuard/NetBird, Unbound, NTP, NUT, CrowdSec, NetFlow | [verificato: board righe 43-71] |
| Server | HPE DL380 Gen10, 2 Xeon Gold 5218 (64 thread), 192 GB ECC, rpool 2 SSD 800 GB in mirror, tank 3 mirror di HDD 1,8 TB (circa 5,4 TB), Quadro RTX 4000, TPM 2.0, Proxmox VE, default-deny fra VLAN con routing su OPNsense | [verificato: board riga 77] |
| Dettagli dal messaggio | 192 GB DDR4 RDIMM; SSD e HDD SAS; ventole e dissipatori ad alte prestazioni già presenti; doppio alimentatore 800 W Titanium; possibili upgrade: una seconda GPU "tipo RTX A2000" e qualche banco di RAM | [verificato: messaggio di Michele] |
| VLAN | OOB iLO; 10 MGMT; 20 EDGE (Traefik, Pangolin, NetBird); 30 APPS (n8n, mcp-enrich, mcp-memory, openoutreach, runner-dash, Homepage, LiteLLM, Open WebUI, MCP RAG, Firecrawl, bandi-watcher, draw.io, Excalidraw, BookStack; uscita su allowlist); 40 DATA (PostgreSQL 16, MinIO, Qdrant, Vaultwarden, Infisical; niente internet); 50 CICD (4 runner GitHub); 60 VAULT (MT bridge); 70 OBSRV (Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox); 80 AI (LXC con Ollama Qwen3-4B Q5_K_M, Infinity con embedding e reranker 0.6B, Docling, worker di indicizzazione); 90 LAB (Experimental-1 e 2); 99 PERSONAL; LAN ufficio | [verificato: board-vlan.txt] |
| GPU | "La RTX 4000 di giorno serve l'AI (VLAN 80), la sera passa a Experimental-1 con uno script; la A2000 futura resterà fissa sull'AI" | [verificato: SerSan Infra Board.html riga 309] |
| Pipeline AI | Export incrementale da Sirius (fiscale, clienti, documenti) → Docling → filtro (segreti scartati, PII marcate) → blocchi e metadati con Qwen3-4B → embedding Qwen3 0.6B in Qdrant più BM25 → reranker → MCP RAG (permessi per utente, log delle query) → Claude Team. "Password e chiavi non entrano mai nell'indice" | [verificato: board righe 79-109] |
| Bandi | Ogni notte: n8n cron → Firecrawl self-hosted → LLM 4B (riassunto, scadenza, punteggio) → RAG e DB → notifica in Teams o per mail | [verificato: board righe 111-133] |
| Backup | Sede 2 (casa, Starlink CGNAT): Proxmox Backup Server su Lenovo M920t da comprare, 2 HDD SATA in mirror, cifratura lato client, utente solo scrittura, acceso di notte da Home Assistant | [verificato: board righe 29-41] |
| Corrente | UPS attuale via USB al firewall con NUT, che spegne Proxmox in modo pulito; più avanti UPS rack 2U (APC SMT1500 o Eaton 5PX) | [verificato: board righe 69-71] |
| Roadmap | F0 Arrivi (pagare Bargain, export completo da Azure, montaggio, test RAM, firmware, TPM clear); F1 Fondamenta (OPNsense e VLAN, Proxmox su ZFS, NetBird e Traefik, PBS a casa); F2 Via da Azure (ci, apps, mesh; MT bridge; spegnere le VM Azure); F3 Sicurezza (Wazuh, NetBox, Authentik, CrowdSec, log e avvisi, documenti ISO e CE); F4 AI e bandi (LXC GPU, pipeline Sirius → MCP, Firecrawl e n8n, LiteLLM con budget); F5 Lab e dopo (Experimental 1 e 2, Minecraft, A2000, UPS rack, Nodo 2 nel 2027-28). "Ogni fase parte quando la precedente è validata" | [verificato: board righe 135-180] |
| RAM | Host e ZFS 16 GB; servizi core circa 69 GB; AI, Firecrawl, Qdrant, LiteLLM circa 24 GB; Experimental 24 GB; Minecraft 6 GB; libera circa 53 GB | [verificato: board righe 184-192] |
| Regole | Experimental dentro il perimetro Cyber Essentials (patch entro 14 giorni, account non admin, software supportato); default-deny ovunque; LAB e PERSONAL non vedono DATA; APPS → AI solo sulle API dei modelli; AI → DATA solo Qdrant; MGMT e OOB solo dal gruppo admin della mesh | [verificato: board righe 194-198] |

---

## 2. Componenti: cosa resta, cosa esce, cosa va deciso

| Cod. | Componente | Dove è nella proposta | Cosa dice il board | Esito | Cosa scrivere |
|---|---|---|---|---|---|
| C01 | **Slack Pro** e **Claude in Slack** | PCEO §1, 2.1, 3, 4.11, 5.1, 5.2, 8.4, 12.1, 14 n.4-5, App. A (J9, A7, B1, F5) | Non è tra i servizi che restano; per persone e notifiche c'è Teams dentro M365 | Esce | La porta per le persone è Teams (già dentro M365, piano da confermare) più Claude Team. Togliere 27,00 € e 44,67 € al mese. Claude in Slack non ha un sostituto diretto: le domande alla memoria passano da Claude Team con il connettore MCP RAG (C22) |
| C02 | **Notion Plus** | PCEO §2.2 n.2, 4.7, 4.12, 5.1, 5.5, 10, 12.1, 14 n.8, App. A (A2, B4, C5, C6, G9) | Non c'è; ci sono BookStack (APPS) e Jira (cloud) | Esce | Regole di lavoro, processi, catalogo e organigramma in BookStack; to-do e progetti in Jira; dati strutturati in PostgreSQL 16. Togliere 35,74 € al mese |
| C03 | **Google Workspace** e **Gmail** | PCEO §5.2 (esecutore Gmail), 12.1 (kit, 54,40 €), 14 (verifiche), App. A F1 | Identità, MFA e posta sono M365 / Entra ID | Esce | L'esecutore di posta e calendario usa Microsoft Graph (Outlook ed Exchange Online). La domanda "quale suite usiamo" è chiusa: M365. Togliere 54,40 € dal kit, se oggi non serve ad altro |
| C04 | **Cloudflare Tunnel** | PCEO §5.2 ("dietro firewall OPNsense e Cloudflare Tunnel"), 6.2 | Cloudflare resta solo per il DNS; l'esposizione passa da Pangolin più Traefik | Sostituito | Gli indirizzi pubblici (webhook di Instantly, `outreach.sersan.io` per l'estensione Chrome, endpoint MCP per Claude Team) passano da Pangolin e Traefik nella VLAN EDGE. Cloudflare resta fra i sub-responsabili solo come DNS |
| C05 | **WireGuard in OPNsense, Tailscale, VPS WireGuard** | PCEO §6.2 ("VPN per il team"); 22 §6 (Tailscale 28,59 € dietro CGNAT); 01 §3 (VPS WG) | Accesso solo da NetBird (SSO Entra più FIDO2), anche dietro CGNAT | Sostituito | L'accesso del team e degli admin passa da NetBird. Il VPS WireGuard esce con Azure (fase F2 "mesh"). Nessun costo Tailscale |
| C06 | **Recall.ai** | PCEO §5.6 (eccezione USA), 9.4, 12.1 (17,42 €), 13, 14 n.6 e verifiche, App. A (A1, C2) | Non c'è | Esce | Registrazione con Vexa sul server oppure con la trascrizione nativa di Teams letta via Graph (N05). Togliere 17,42 € al mese e l'eccezione "Recall negli USA" dai tre colori e dal parere legale |
| C07 | **Vexa** | PCEO §5.6 e 11 (prova nella fase 1) | Non c'è, ma è self-hosted (Apache-2.0) | Da prova a scelta principale, da far approvare | Vexa supporta Google Meet, Microsoft Teams e Zoom [verificato: github.com/Vexa-ai/vexa]. Va aggiunto alla VLAN APPS con la trascrizione sulla GPU (N05, N06) |
| C08 | **ElevenLabs** e **numero Twilio** | PCEO §1, 5.6, 9, 12.1 (170,28 €), 13, 14 n.9, App. A G5 | Non ci sono | Eccezione da decidere | "Andrea" resta nella visione (G5, K10). Due strade: eccezione approvata da Michele, oppure voce self-hosted rimandata alla seconda GPU (N07) |
| C09 | **Hermes Agent** | PCEO §1, 2.2 n.3, 5.1, 5.2, 5.3, 5.7, 11, 13, 15, App. A (A4, J4, J9), App. B | Non c'è; Michele preferisce valutare l'Agent SDK di Claude | Da rivalutare | "Orchestratore: Agent SDK di Claude o Hermes, scelta dopo un confronto con i componenti del board". Il confronto va rifatto (N01) |
| C10 | **Hermes Cloud** | PCEO §1, 5.2, 5.3, 5.6, 11 fase 0, 12.1 (18,67 €), 13, 14 n.7 | Non c'è | Esce | Niente palestra in cloud né riserva su Hermes Cloud. La riserva vera è il ripristino dal PBS a casa. Togliere 18,67 € (47 € nei mesi di prova) |
| C11 | **Postgres 17 con pgvector** | PCEO §2.2, 4.7, 5.2, 5.5, App. A A3; 22 §2 | PostgreSQL 16 in DATA; Qdrant più BM25 per i vettori; embedding e reranker Qwen3 0.6B su Infinity | Sostituito | "La memoria vettoriale è Qdrant, con ricerca ibrida (vettori più BM25) e un reranker, tutto sul server." Attenzione al database di SersanOutreach, oggi su Postgres 17.6 (N09) |
| C12 | **Langfuse** | 22 §2 (VM dati) | Non c'è | Esce o si chiede | Il conto delle chiamate lo fa LiteLLM; le tracce degli agenti vanno in Loki. Se serve Langfuse, va chiesto a Michele |
| C13 | **Porta dei modelli** del Cancello, una chiave per famiglia | PCEO §5.1, 9.2, 4.8 (banca dei token); 22 §2 | "API Anthropic dietro LiteLLM"; "LiteLLM con budget" in F4 | Sostituito in parte | LiteLLM dà chiavi virtuali con budget per chiave, utente e squadra, e respinge le richieste oltre il tetto [verificato: docs.litellm.ai/docs/proxy/users]. La banca dei token legge i conti di LiteLLM; il Cancello tiene approvazioni e audit |
| C14 | **Proxmox** | PCEO §6.2, 12.1 (20 €), 14 n.12 | Proxmox VE su ZFS, F1 | Resta | Il prezzo regge: 120 € l'anno per socket nel piano Community, quindi 240 € l'anno con 2 CPU [verificato: horizoniq.com, wz-it.com, fonti terze]. Abbonamento e data li decide Michele. Il PBS ha un abbonamento suo, facoltativo [non verificato: prezzo] |
| C15 | **Password manager** (1Password, 22,29 €) | PCEO §1 decisione 2, 12.1 | Vaultwarden (persone) e Infisical (segreti delle applicazioni) in DATA | Sostituito | Togliere 22,29 € al mese. Le chiavi API degli agenti stanno in Infisical, mai nei prompt né nei log |
| C16 | **Backup fuori sede** (B2, 3,10 €) | PCEO §1, 6.2, 11, 12.1 | PBS a casa su M920t; S3 fuori sede facoltativo | Sostituito | Backup quotidiani su PBS a casa, cifrati lato client, con utente solo scrittura. La copia S3 resta facoltativa. Aggiungere l'acquisto del PBS alle spese una tantum (§5.3) |
| C17 | **Telegram** | PCEO §1, 2.1, 4.11, 5.2, 12.1, 13, 14 n.18, App. A J9 | Non c'è | Eccezione da decidere | Il telefono si copre con Teams e con la pagina del Cancello. Telegram resta solo se Michele lo ammette (N04) |
| C18 | **WhatsApp** (API Meta) | Come C17 | Non c'è | Eccezione da decidere | Come C17 |
| C19 | **Buzz** | PCEO §1, 2.1, 4.11, 5.1, 5.2, 11, 13, 14 n.19 | Non c'è; sarebbe self-hosted | Da decidere | Compatibile con "self-hosted", ma pre-1.0: va pesato contro "software supportato" di Cyber Essentials (N14). La prova può stare nella VLAN LAB (Experimental-2) |
| C20 | **Paperclip** | PCEO §4.12, 11 fase 5 | Non c'è; sarebbe self-hosted | Da decidere | Prova solo nella VLAN LAB, senza dati dei clienti |
| C21 | **Grok Bot** | PCEO §5.7, 14 n.17 (prova da 54 €) | Non c'è; gira su computer negli USA | Eccezione da decidere | Togliere la decisione 17, oppure tenerla come eccezione approvata da Michele, solo su dati pubblici |
| C22 | **Claude Team** | PCEO §1, 5.2, 12, 14 n.13 | Resta e "ragiona sul RAG via MCP" | Resta, ruolo più grande | Claude Team diventa la porta principale verso la memoria: un connettore personalizzato (MCP remoto) verso l'MCP RAG, con i permessi di chi chiede. Il connettore parte dai server di Anthropic, quindi l'endpoint deve essere raggiungibile da internet (N10) [verificato: support.claude.com, articolo 11175166] |
| C23 | **API Anthropic** | PCEO §5.1, 12, 14 n.11 | Resta, dietro LiteLLM | Resta | Gli agenti usano solo la chiave API, mai l'accesso di Claude Team: l'Agent SDK lo chiede esplicitamente [verificato: code.claude.com/docs/en/agent-sdk/overview]. L'Agent SDK passa da LiteLLM con `ANTHROPIC_BASE_URL` [verificato: code.claude.com/docs/en/llm-gateway] |
| C24 | **Claude su AWS Bedrock in UE** | PCEO §13, 14 n.14 | AWS non c'è | Resta "su richiesta", con un sì di Michele | Aggiungere: "un nuovo cloud entra solo con l'approvazione di Michele". LiteLLM può indirizzare le chiamate anche verso Bedrock [non verificato: da provare] |
| C25 | **VM Azure** | PCEO §1, 5.2 (riserve), 7, 11, 12, 13 | Azure esce (F2: "spegnere le VM Azure", al plurale) | Esce prima | Togliere "Azure come riserva" e "se l'hardware tarda, la fase 1 parte sulla VM Azure". Il risparmio va ricalcolato su tutte le VM Azure, non su una sola da 150 € (N20) |
| C26 | **Supabase** | PCEO §7.1-7.2 ("In casa, latenza zero, stesso database per la memoria degli agenti") | Resta come "DB del prodotto" | Da chiarire | Se "il prodotto" è SersanOutreach, il database resta su Supabase in Irlanda e la riga della tabella 7.2 va riscritta (N09) |
| C27 | **n8n** | 22 §3 ("n8n non si prende") | C'è, in APPS, e fa girare i bandi | Resta | Correggere 22 e la proposta. L'uso interno è ammesso dalla licenza di n8n; non si rivende come servizio [verificato: docs.n8n.io, Sustainable Use License e FAQ]. Regola da aggiungere: n8n non manda nulla a clienti o prospect, perché quello passa solo dal Cancello |
| C28 | **Jira** | Assente | Resta in cloud | Entra | Agente task, Project manager, Report cliente e Onboarding lavorano su Jira |
| C29 | **BookStack, Open WebUI, Firecrawl, Docling, Ollama, Infinity, MCP RAG** | Assenti | Ci sono | Entrano | BookStack per la memoria relazionale; Open WebUI come chat interna sui modelli locali e su Claude con il budget di LiteLLM; Firecrawl per le ricerche web (al posto di Apify e in parte di Perplexity); Docling per PDF e scansioni |
| C30 | **Microsoft 365 e Teams** come casa comune | Assente (Teams solo come piattaforma di call) | M365 resta; le notifiche dei bandi vanno "in Teams o per mail" | Entra | Riscrivere la chat di gruppo (PCEO §4.11) attorno a Teams, salvo diversa scelta di Michele (N02) |
| C31 | **faster-whisper** (trascrizione locale) | PCEO §5.2, 6.1, App. A C4 | Non c'è sulla GPU | Da aggiungere o da spostare | Va chiesto a Michele dove gira: sulla RTX 4000 di giorno, su CPU, o sulla seconda GPU (N05, N06) |
| C32 | **Instantly** | PCEO §4.1, 7 | Resta | Resta | Nessuna modifica |
| C33 | **GitHub e runner** | PCEO §7 | Resta, 4 runner in CICD | Resta | Nessuna modifica, salvo il nome della VLAN |
| C34 | **Vercel** | Assente dalla proposta | Resta per i deploy dei clienti | Nessun impatto | Nessuna modifica; il deploy resta un'azione umana |
| C35 | **Apollo, Metricool, Apify, moda.app, Higgsfield, Perplexity, IPRoyal, Canva, After Effects** | PCEO §4.5, 8.2, 12.1, App. A D4; 01 §2 | Non ci sono | Eccezioni da decidere | Tabella N08 |
| C36 | **MinIO, Wazuh, NetBox, Authentik, CrowdSec, Uptime Kuma** | Assenti | Ci sono (F3 per la sicurezza) | Entrano | Il Sistemista legge OBSRV e NetBox; le approvazioni usano l'identità Entra (direttamente o via Authentik). MinIO ha un problema di supporto (N14) |
| C37 | **Sirius** | Assente | Prima sorgente della pipeline AI (fiscale, clienti, documenti) | Entra | Va spiegato cos'è e quali dati porta (N11) |

---

## 3. Hardware: prima e dopo

| Cod. | Voce | Proposta | Board e messaggio di Michele | Cosa scrivere |
|---|---|---|---|---|
| H01 | RAM | 160 GB, 10 moduli sbilanciati; 2 moduli in più a circa 138 € (PCEO §6.2, 12.3) | 192 GB DDR4 RDIMM ECC | "192 GB di RAM ECC." Con ogni probabilità sono 12 moduli da 16 GB, cioè i 10 comprati più 2 [non verificato: da confermare con Michele]; con 2 CPU, 12 moduli sono una configurazione bilanciata [verificato: 15 §0 punto 3]. Togliere i 138 €. Più RAM è un upgrade facoltativo: il prossimo passo bilanciato va controllato sulla tabella HPE; con 12 moduli in più, circa 828 € [stima: prezzo medio pagato, 690 € per 10 moduli, 15 §1] |
| H02 | CPU | Non indicata ("modello esatto da verificare", PCEO §14) | 2 Xeon Gold 5218 | "2 Xeon Gold 5218: 16 core e 32 thread ciascuna, 2,3 GHz, 125 W, 6 canali DDR4-2667" [verificato: scheda Intel e rivenditori, ricerca del 25/10/2026]. Togliere "modello esatto" dalle verifiche |
| H03 | Dischi | "2 dischi SSD con protezione da blackout" da comprare (PCEO §12.3) | rpool 2 SSD SAS 800 GB in mirror; tank 6 HDD SAS 1,8 TB in 3 mirror, circa 5,4 TB | Togliere i dischi dagli acquisti. Chiedere a Michele se database e Qdrant stanno sugli SSD (N16) |
| H04 | Ventole e dissipatori per la GPU | Kit HPE da comprare (PCEO §6.2, 12.3) | Ventole e dissipatori ad alte prestazioni già presenti | Togliere dagli acquisti |
| H05 | Alimentatori | "2 alimentatori da 800 W (se oggi sono da 500 W)" (PCEO §12.3) | Doppio 800 W Titanium già presente | Togliere dagli acquisti |
| H06 | GPU attuale | RTX 4000 per embedding, giudice, trascrizione e oscuramento, circa 6-6,5 GB su 8 (PCEO §6.1) | Di giorno all'AI (Ollama Qwen3-4B Q5_K_M, Infinity con embedding e reranker, Docling), la sera a Experimental-1 | Riscrivere i lavori della GPU con i modelli del board e la condivisione giorno e sera. La trascrizione non è nella lista (C31). Con Qwen3-4B in Q5, embedding e reranker in FP16 e Docling la scheda è già quasi piena: Whisper non entra insieme [non verificato: stima sulle misure di 13 §8] |
| H07 | Seconda GPU | "Non ora"; schede da 2.438-2.555 € (PCEO §6.2, 12.3, 14 n.3) | Seconda GPU "tipo RTX A2000" nella fase F5, fissa sull'AI | Diventa una decisione di budget della fase F5. Il modello va corretto: una "A2000 con chip Ada da 6 GB GDDR7" non esiste. La RTX A2000 (Ampere) ha 6 o 12 GB GDDR6 e 70 W; la versione Ada si chiama RTX 2000 Ada e ha 16 GB GDDR6, 70 W, PCIe 4.0 x8; la GDDR7 c'è sulla RTX PRO 2000 Blackwell, 16 GB, 70 W [verificato: gigazine.net, getdeploying.com, emarque.co]. Per tenere fissi modello 4B, embedding, reranker e Whisper servono almeno 12 GB [non verificato: stima] |
| H08 | UPS | UPS 1.500 VA "obbligatorio", 1.163-1.293 € subito (PCEO §1, 6.2, 12.3, 14 n.2) | UPS attuale via USB al firewall con NUT; UPS rack 2U più avanti (F5) | "Oggi c'è un UPS che spegne il server in modo pulito; l'UPS da rack arriva nella fase F5." Prezzo aggiornato del modello APC: 1.072-1.163 € IVA inclusa [verificato: eBay.de IT-Planet, Yeppon, 25/10/2026]. Chiedere potenza e autonomia dell'UPS attuale (N15) |
| H09 | Dove sta il server | "Un locale tecnico ventilato nella sede in Sardegna" (PCEO §6.2, 14 n.2b) | Rack VEVOR 12U in salotto | Togliere la decisione 2b: il posto l'ha scelto Michele. Tenere solo l'avvertenza su rumore e calore come rischio da misurare |
| H10 | Firewall e rete | Mini PC con OPNsense e VPN del team; tunnel Cloudflare (PCEO §6.2) | OPNsense con trunk VLAN, NetBird, Unbound, CrowdSec, NetFlow, NUT; FTTH 2,5G con IP fisso | Riscrivere con il board. Il costo dell'IP fisso va chiesto al provider (N20) |
| H11 | Hardware dei backup | PBS sul server con copia fuori sede (22 §2) | PBS su Lenovo M920t a casa, 2 HDD SATA in mirror | Nuova spesa una tantum: M920t ricondizionato 186-355 € [verificato: refurbed.it, pccomponentes.it, 25/10/2026] più 2 dischi SATA [non verificato: 100-250 €] |
| H12 | Fine del supporto HPE | 31/03/2028, "si sposta su un server nuovo" (PCEO §6.2, 13) | "Nodo 2 (2027-28)" nella fase F5 | Aggiungere che il secondo nodo è già in roadmap |
| H13 | Hardware "già comprato" | "L'hardware principale è già comprato" (PCEO §1); 1.241 € (PCEO §12.3) | F0: "Pagare Bargain" | Chiarire se il pagamento del server è ancora da fare e quanto vale. Se è da pagare, va nel quadro delle spese una tantum (N20) |
| H14 | Cavo GPU | Cavo non HPE da 10,80 € da controllare (15 §1) | Non citato | Tenere il controllo del cavo con il tester, oppure il cavo HPE |

---

## 4. Correzioni sezione per sezione

Le righe "nessuna modifica" sono omesse. Dove la correzione è già in §2 o §3, la riga rimanda al codice.

### 4.1 Sezione 1, In breve

| Cod. | Testo attuale | Board | Cosa scrivere |
|---|---|---|---|
| S1-01 | "Gli agenti si parlano tra loro in una chat di gruppo come Buzz, che leggiamo anche noi e che raggiungiamo da Slack, Telegram e WhatsApp" | Né Slack né Telegram né WhatsApp; Teams in M365 | "Gli agenti si passano il lavoro in stanze che tutti possono leggere, e noi li raggiungiamo da Teams, dal PC e dal telefono." La chat che ospita le stanze va decisa (N02) |
| S1-02 | "Usiamo Hermes Agent di Nous Research ... come orchestratore, installato sul server che abbiamo appena comprato" | C09 | "L'orchestratore gira sul nostro server. Michele preferisce l'Agent SDK di Claude; lo confrontiamo con Hermes sui componenti già previsti (LiteLLM, n8n, Jira, Teams) prima di scegliere." |
| S1-03 | "La memoria, le trascrizioni e il CRM restano in casa" | Supabase resta in cloud; Claude Team riceve i pezzi recuperati dall'MCP RAG | "Documenti, trascrizioni e indici restano sul server; a Claude arrivano solo i pezzi che servono a rispondere, con i permessi di chi chiede." Il CRM dipende da N09 |
| S1-04 | "...e ora un server con 160 GB di RAM e una GPU"; "ElevenLabs, moda.app" fra ciò che abbiamo | H01, H02, C08, C35 | "...e un server con 2 CPU da 16 core, 192 GB di RAM, circa 6,2 TB utili di dischi in mirror e una GPU" (800 GB di SSD più circa 5,4 TB di HDD [verificato: board]). ElevenLabs e moda.app solo se diventano eccezioni |
| S1-05 | Tabella "€ al mese in più": ≈ 300, 290, 140, 310 | §5.2 | Sostituire con la tabella di §5.2 |
| S1-06 | Elenco "Cosa costa": Claude in Slack, Hermes Cloud, Proxmox dalla fase 2, kit 311 € | C01, C10, C14, C03, C35 | Kit commerciale senza Google Workspace (circa 257 € al massimo), con gli strumenti fuori dal board segnati come eccezioni |
| S1-07 | "Una tantum: UPS (1.163-1.293 €), accessori HPE e due dischi (tetto proposto 1.000 €), deposito API (circa 223 €), parere legale (tetto 2.500 €)" | H01-H11 | "Una tantum: Proxmox Backup Server a casa (circa 290-610 €), qualche accessorio residuo (fino a 200 €), deposito API (circa 223 €), parere legale (tetto 2.500 €). UPS da rack e seconda GPU nella fase F5" [stima] |
| S1-08 | "Cosa vedete in 8 settimane": "i to-do sono in Notion", "anche su Telegram o WhatsApp", "SersanOutreach ... pronto a spostarsi sul server" | C02, C17, roadmap | To-do in Jira; debrief in Teams o per mail. Le 8 settimane vanno riallineate alle fasi F0-F4 (§6) |
| S1-09 | Decisione 1: "Il lavoro lo portano avanti Alberto, Mattia e Michele" | Michele cura l'infrastruttura | Aggiungere: "Michele guida le fasi F0-F3 del server; Alberto e Mattia costruiscono agenti e Cancello" |
| S1-10 | Decisione 2: "Slack Pro, Notion Plus, Claude in Slack con un tetto, registrazione delle call, Hermes Cloud come riserva, password manager e backup (circa 200 € al mese ... poi circa 170 €)" | C01, C02, C06, C10, C15, C16 | "Nessun abbonamento nuovo è necessario per la prima fase. Se Michele lo vuole, l'abbonamento Proxmox Community: 20 € al mese." |
| S1-11 | Decisione 3: "In tutto, al massimo 5.016 €" | §5.3 | "In tutto, circa 3.010-3.530 €" [stima] |

### 4.2 Sezione 2, L'idea

| Cod. | Testo attuale | Board | Cosa scrivere |
|---|---|---|---|
| S2-01 | 2.1: "La stessa chat è collegata a Slack, Telegram e WhatsApp" | C01, C17, C18 | "La stessa chat si raggiunge da Teams e dal telefono." Telegram e WhatsApp solo se approvati |
| S2-02 | 2.2 n.2: "Una relazionale (Notion: processi, obiettivi, regole...) e una vettoriale" | C02, C11 | "Una relazionale (BookStack e PostgreSQL: processi, obiettivi, regole di lavoro, catalogo) e una vettoriale (Qdrant) che collega trascrizioni, mail, documenti e l'archivio di Sirius" |
| S2-03 | 2.2 n.3: "Un orchestratore sul nostro server, Hermes Agent" | C09 | "Un orchestratore sul nostro server (Agent SDK di Claude o Hermes)" |
| S2-04 | 2.2 n.15: "bandi e finanziamenti da non perdere" | Pipeline bandi nella fase F4 | Aggiungere che la ricerca dei bandi arriva già con il server (F4), non nella fase 6 |
| S2-05 | 2.4, ultima riga: "Banca dei token: budget per persona e per agente, con tetti che fermano davvero" | LiteLLM con budget (F4) | Aggiungere "con i budget di LiteLLM" |

### 4.3 Sezione 3, Una giornata

| Cod. | Testo attuale | Cosa scrivere |
|---|---|---|
| S3-01 | "7:00. Alessandro apre Slack" | "Alessandro apre Teams" (o la chat scelta, N02) |
| S3-02 | "11:00-11:45. ... Il bot di registrazione entra" | Va bene con Vexa; con la trascrizione nativa di Teams non entra nessun bot, ma l'avviso resta (N05) |
| S3-03 | "11:55 ... In Notion ci sono i to-do ... Sul telefono di Alessandro arriva una carta" | "In Jira ci sono i to-do ... Sul telefono arriva un avviso in Teams e la carta si apre nella pagina del Cancello" (N03) |
| S3-04 | "12:10. Nella sala macchine, cioè il canale `#agenti`" | Nome della stanza nella chat scelta |
| S3-05 | "17:30 ... 'Andrea' la chiama" | Tenere solo se la voce passa come eccezione (N07); altrimenti spostare a "dopo la seconda GPU" |
| S3-06 | "Michele riceve il suo: ... lo stato del server" | "...lo stato del server da Grafana, Uptime Kuma e Wazuh, e le patch da applicare entro 14 giorni" |

### 4.4 Sezione 4, Squadre e agenti

| Cod. | Sezione e testo attuale | Board | Cosa scrivere |
|---|---|---|---|
| S4-01 | 4.2 Agente chiamate: "Entra automaticamente in ogni call del calendario (Meet, Teams, Zoom)" | C06, C07 | "Con Vexa sul server (Meet, Teams, Zoom); per le call in Teams in alternativa la trascrizione di Teams letta via Graph" (N05) |
| S4-02 | 4.2 Dettatura: "dal telefono e dal PC" | C31 | "Dettatura delle app Claude; note vocali trascritte sul server quando la GPU o la CPU lo permettono" |
| S4-03 | 4.3 Agente brief: dati pubblici, enrich | Firecrawl; mcp-enrich in APPS | "Dati pubblici con Firecrawl sul server e con l'arricchimento di SersanOutreach"; Apollo e Perplexity come eccezioni (N08) |
| S4-04 | 4.3 "Andrea" | C08 | Dipende da N07 |
| S4-05 | 4.3 Agente contratti: "lo manda in firma elettronica" | Firma elettronica fuori dal board | Segnare lo strumento di firma come eccezione da decidere nella fase 6, o un firmatario self-hosted [non verificato: da cercare] |
| S4-06 | 4.4 Pubblicatore e Analista metriche: "Metricool" | Fuori dal board | Eccezione, oppure Postiz self-hosted (AGPL-3.0, LinkedIn, Instagram, YouTube) [verificato: README di postiz-app; documentazione self-hosting] |
| S4-07 | 4.4 Agente newsletter: "la manda dopo il sì" | Nessuno strumento nel board | Strumento da scegliere fra un servizio approvato e uno self-hosted (N08) |
| S4-08 | 4.5 Agente video: "con Higgsfield, HyperFrames e After Effects" | Higgsfield fuori dal board | Higgsfield come eccezione su contenuti pubblici; HyperFrames gira in locale; After Effects è software desktop in abbonamento, dentro il perimetro Cyber Essentials come ogni software installato (N14) |
| S4-09 | 4.5 Agente slide | moda.app fuori dal board | "Slide con Claude e i nostri template"; moda.app solo come eccezione |
| S4-10 | 4.6 Project manager, Agente task, Report cliente, Onboarding | Jira | "Piano, task e stato in Jira" |
| S4-11 | 4.6 Onboarding cliente: "canale, cartelle, registro delle decisioni" | Teams, SharePoint, BookStack | "Canale in Teams, cartelle in SharePoint o sul server, registro delle decisioni in BookStack" |
| S4-12 | 4.7 Raccoglitore: "mail, calendario, Drive, chat, Notion, trascrizioni e CRM" | M365, Jira, BookStack, Sirius | "Posta, calendario e file di M365, Teams, BookStack, Jira, Sirius, trascrizioni e SersanOutreach" |
| S4-13 | 4.7 Bibliotecario: "Notion e il database di SersanOutreach ... Postgres con pgvector" | C02, C11 | "BookStack e PostgreSQL per la memoria relazionale; Qdrant con BM25 e reranker per quella vettoriale; risponde anche tramite Claude Team con l'MCP RAG" |
| S4-14 | 4.7 Sistemista: "aggiornamenti di Hermes e dei modelli" | OBSRV, NetBox, regola dei 14 giorni | "Legge Prometheus, Grafana, Loki, Uptime Kuma, Wazuh e NetBox; prepara le patch da applicare entro 14 giorni" |
| S4-15 | 4.7 Archivista | Loki, Wazuh, PBS | Aggiungere le scadenze di log e backup |
| S4-16 | 4.8 Banca dei token: "avviso all'80%, stop al 100%" | C13 | "Budget in LiteLLM per chiave, persona e squadra; l'avviso all'80% lo manda il Cancello" |
| S4-17 | 4.8 Guardiano: "Blocca per default ciò che invia, pubblica, paga o cancella" | n8n in APPS | Aggiungere: "Nessun flusso di n8n scrive a clienti o prospect" (C27) |
| S4-18 | 4.8 Mappatore processi: "metadati del Workspace" | M365 | "Metadati di Microsoft 365, solo con l'accordo di ognuno" |
| S4-19 | 4.8 Smistatore posta | M365 | "Legge la posta di Outlook tramite Microsoft Graph" |
| S4-20 | 4.9 intro: "Si collega allo strumento di fatturazione e contabilità che usiamo" | Fuori dal board | Chiarire se Sirius è il gestionale fiscale (N11) |
| S4-21 | 4.9 Agente bandi e finanziamenti, fase 6 | Pipeline bandi nella fase F4 | "Arriva con la fase F4 del server: n8n, Firecrawl e il modello locale cercano i bandi ogni notte e mandano i migliori in Teams o per mail; l'agente aggiunge requisiti e documenti" |
| S4-22 | 4.9 Controllo di gestione, fase 6 | Sirius nell'indice (F4) | "I dati fiscali di Sirius entrano nella memoria già nella fase F4; i report mensili restano nella fase 6" |
| S4-23 | 4.10 percorso del cliente, punti 2, 6 ("stanza dell'Outbound", "canale") | Teams | Nomi delle stanze nella chat scelta |
| S4-24 | 4.11 tutta la sezione (Buzz, Slack, Telegram, WhatsApp, percorso) | C01, C17-C19, C30 | Riscrivere: "Teams per le persone; stanze degli agenti nella chat scelta da Michele; carte nella pagina del Cancello; Telegram, WhatsApp e Buzz solo se approvati." Il freno ai giri resta |
| S4-25 | 4.12: "Il registro si vede in Notion come un organigramma"; "Nella fase 5 proviamo Paperclip" | C02, C20 | "Si vede in BookStack o in una dashboard di Grafana"; Paperclip in prova nella VLAN LAB |

### 4.5 Sezione 5, Come è fatto

| Cod. | Sezione e testo attuale | Cosa scrivere |
|---|---|---|
| S5-01 | 5.1 n.1: "Hermes Agent orchestra ... collegamento a Slack, Telegram e WhatsApp" | "L'orchestratore (Agent SDK o Hermes) gira in una macchina della VLAN APPS, con uscita solo verso i servizi in lista" |
| S5-02 | 5.1 n.2: "Gli agenti usano Claude via chiave API" | Aggiungere "attraverso LiteLLM, che conta e ferma la spesa" |
| S5-03 | 5.1 n.3: "le scritture interne (meeting e deal nel CRM, to-do in Notion)" | "to-do in Jira" |
| S5-04 | 5.1 n.4: "le regole e i processi in Notion" | "in BookStack" |
| S5-05 | 5.1 n.5: "Slack dal primo giorno, Buzz in prova dalla fase 2, Telegram e WhatsApp collegati" | "Teams per le persone, stanze degli agenti nella chat scelta, carte dal telefono" |
| S5-06 | 5.2 Lo schema (tutto) | Sostituire con lo schema proposto qui sotto |
| S5-07 | 5.3 Perché Hermes (tutta la sezione) | Riscrivere come "L'orchestratore: Agent SDK o Hermes". Fatti utili: l'Agent SDK offre subagenti, MCP, hook, permessi e sessioni, in Python e TypeScript, ed è regolato dai termini commerciali di Anthropic [verificato: code.claude.com/docs/en/agent-sdk/overview]. Hermes ha già un collegamento a Teams fra i suoi canali [verificato: 10 riga 95]. Il punto "Ha una versione ospitata, Hermes Cloud" va tolto |
| S5-08 | 5.4: "Le azioni delicate diventano una carta in `#approvazioni`" | "...una carta nella pagina del Cancello, aperta con l'identità Entra e la chiave FIDO2; l'avviso arriva in Teams" (N03). La frase "la macchina degli agenti può parlare in rete solo con i servizi in lista" coincide con la VLAN APPS ("uscita su allowlist") e resta |
| S5-09 | 5.5 La memoria a due database | Riscrivere con BookStack, PostgreSQL 16, Qdrant più BM25, reranker, MCP RAG e Claude Team; citare la regola del board "Password e chiavi non entrano mai nell'indice" |
| S5-10 | 5.6 Verde: "anche Claude in Slack e Hermes Cloud" | Togliere entrambi; il verde va a Claude Team, all'API e ai servizi approvati |
| S5-11 | 5.6 Rosso: "Resta sul server, oppure va all'API Anthropic dopo aver oscurato" | Aggiungere il nuovo flusso: l'MCP RAG passa a Claude Team pezzi di documenti dei clienti e dati fiscali di Sirius, con le PII solo marcate, non tolte [verificato: board, passo "Filtro"]. Claude Team non può avere la conservazione zero [verificato: 16 riga 158]. Serve una regola: quali pezzi rossi l'MCP RAG può restituire e a chi (N17) |
| S5-12 | 5.6 eccezioni: "Recall.ai ... negli USA"; "le chiamate di Andrea, che passano da ElevenLabs" | La prima esce (C06); la seconda resta solo se la voce diventa un'eccezione (C08) |
| S5-13 | 5.7 Alternative valutate e punteggi | Aggiungere: "I punteggi sono di prima del board di Michele. Con LiteLLM, n8n, Jira, Qdrant e l'MCP RAG già previsti, il costo di costruzione della proposta E (Claude-native) scende e il confronto va rifatto" [non verificato: da misurare] |

**Schema proposto per PCEO §5.2** (da rivedere con Michele):

```
PERSONE (4)  Teams e Outlook (M365; identità Entra con MFA e chiave FIDO2)
             Claude Team: chat, Claude Code, connettore MCP RAG sulla memoria
             Pagina del Cancello per le carte, dal PC e dal telefono
             Stanze degli agenti: nella chat scelta da Michele

==== SEDE 1 · rack in salotto · FTTH 2,5G · OPNsense, VLAN default-deny ====
EDGE  (20)  Traefik, Pangolin, NetBird: unico ingresso, sempre autenticato
APPS  (30)  ORCHESTRATORE (Agent SDK o Hermes) e CANCELLO: registro, regole,
            carte, audit, stop, freno ai giri; esecutori: posta e calendario
            via Graph, Teams, Jira, SersanOutreach, Instantly
            LiteLLM (porta dei modelli, banca dei token), n8n (routine),
            SersanOutreach e i suoi MCP, MCP RAG, Firecrawl, Vexa,
            Open WebUI, BookStack · uscita solo verso servizi in lista
DATA  (40)  PostgreSQL 16, Qdrant, Vaultwarden, Infisical · niente internet
AI    (80)  RTX 4000 di giorno: Qwen3-4B, embedding e reranker, Docling
            la sera la scheda va a Experimental-1; dalla F5 una seconda GPU
CICD  (50)  runner GitHub, staging su richiesta
OBSRV (70)  Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox
            (VAULT, LAB e PERSONAL non sono raggiungibili dagli agenti)
==============================================================================
SEDE 2 · casa   Proxmox Backup Server cifrato; S3 fuori sede facoltativo
IN CLOUD        M365 / Entra · Claude Team · API Anthropic via LiteLLM
                · Cloudflare DNS · GitHub · Supabase · Vercel · Jira · Instantly
DA DECIDERE     voce di "Andrea" · strumenti di marketing e lead fuori dal board
                · Telegram e WhatsApp · Buzz
```

### 4.6 Sezione 6, Il server

| Cod. | Testo attuale | Cosa scrivere |
|---|---|---|
| S6-01 | 6.1: "un HPE ProLiant DL380 Gen10, con 160 GB di RAM e una NVIDIA Quadro RTX 4000" | "Un HPE ProLiant DL380 Gen10 con 2 Xeon Gold 5218 (64 thread), 192 GB di RAM ECC, 2 SSD da 800 GB in mirror e 6 dischi da 1,8 TB in tre mirror (circa 5,4 TB), una Quadro RTX 4000 da 8 GB, doppio alimentatore da 800 W" (H01-H05) |
| S6-02 | 6.1: "SersanOutreach ..., Hermes, il Cancello, il database con la memoria, il monitoraggio, i backup" | Elenco dei servizi per VLAN, come nello schema. Aggiungere la tabella della RAM del board: circa 53 GB liberi, dove devono stare orchestratore e Cancello (N01) |
| S6-03 | 6.1: lavori della GPU (embedding, giudice, trascrizione, oscuramento); "circa 6-6,5 GB degli 8" | H06 e N06. Il "giudice veloce" è il Qwen3-4B del board; l'oscuramento è il passo "Filtro" della pipeline; la trascrizione va collocata |
| S6-04 | 6.1: "(Haiku 5.5 costa 0,10 $ per milione di token in ingresso)" | Resta, con la data di rilevazione |
| S6-05 | 6.2 "Dove": "Serve un locale tecnico ventilato; proponiamo la sede in Sardegna" | H09 |
| S6-06 | 6.2 "Corrente": "l'UPS è obbligatorio" | H08 |
| S6-07 | 6.2 "Memoria": "I 10 moduli comprati sono una configurazione sbilanciata" | H01 |
| S6-08 | 6.2 "GPU": "HPE chiede un kit di ventole e dissipatori ... va comprato dopo l'inventario" | H04: "Il server ha già ventole e dissipatori ad alte prestazioni" |
| S6-09 | 6.2 "Rete": "Il mini PC ... fa da firewall (OPNsense) e da VPN per il team. I servizi pubblici ... escono con un tunnel Cloudflare" | "OPNsense separa le VLAN e blocca tutto ciò che non è permesso. Il team entra da NetBird; i servizi pubblici passano da Pangolin e Traefik" (C04, C05, N10) |
| S6-10 | 6.2 "Software e backup": "backup quotidiani con una copia cifrata fuori sede" | "Proxmox su ZFS; backup su Proxmox Backup Server a casa, cifrati lato client, con un utente che può solo scrivere" (C16) |
| S6-11 | 6.2: supporto HPE fino al 31/03/2028 | H12 |
| S6-12 | 6.2: "L'aggiornamento della GPU non serve ora ... 2.400-2.600 €" | H07 |
| S6-13 | Nuovo paragrafo | Aggiungere la roadmap F0-F5 e la frase "ogni fase parte quando la precedente è validata" (§6) |
| S6-14 | Nuovo paragrafo | Aggiungere il perimetro Cyber Essentials e le sue regole (N14) |

### 4.7 Sezione 7, SersanOutreach

| Cod. | Testo attuale | Board | Cosa scrivere |
|---|---|---|---|
| S7-01 | 7.2, riga Memoria: "160 GB" | H01 | "192 GB" |
| S7-02 | 7.2, riga Database: "In casa, latenza zero, stesso database per la memoria degli agenti" | Supabase resta come "DB del prodotto" | Dipende da N09. Se resta su Supabase: "Il database resta su Supabase in Irlanda; sul server stanno l'applicazione e la memoria degli agenti." La memoria degli agenti sta comunque in PostgreSQL 16 e Qdrant sul server |
| S7-03 | 7.2, riga Costo: "VM Azure ... più VPS e Supabase → Corrente e backup" | Azure e VPS escono; Supabase forse resta | "Escono la VM Azure e il VPS WireGuard; Supabase resta se il database non si sposta" |
| S7-04 | 7.2, riga Dati: "In casa, con copia cifrata fuori sede" | PBS a casa | "Sul server, con copia cifrata nel PBS a casa" |
| S7-05 | 7.2 testo: "Lo spostamento è nella fase 2 ... La VM Azure si spegne solo dopo una settimana di funzionamento stabile" | F2 "Via da Azure: ci → apps → mesh" | "Lo spostamento segue la fase F2 del board: prima i runner, poi le applicazioni, poi la rete." La settimana di prova prima dello spegnimento resta |
| S7-06 | 7.2: "Teniamo il dominio `outreach.sersan.io`" | Pangolin e Traefik | Aggiungere "pubblicato da Pangolin e Traefik, con il DNS su Cloudflare" |
| S7-07 | 7.3: "due server MCP ... installati accanto a Hermes" (anche PCEO §11 fase 2) | APPS con mcp-enrich e mcp-memory | "installati nella VLAN APPS". Chiarire il rapporto fra i due MCP di SersanOutreach (lettura e operatore) e i servizi mcp-enrich e mcp-memory del board (N12) |
| S7-08 | 7.4: "il secondo fattore per i 7 account staff, il backup fuori sede e gli alert" | Entra MFA, PBS, OBSRV | Il secondo fattore resta (Cyber Essentials chiede MFA sui servizi esposti). Il backup fuori sede è il PBS; gli alert passano da Prometheus e Uptime Kuma |

### 4.8 Sezioni 8, 9 e 10

| Cod. | Testo attuale | Cosa scrivere |
|---|---|---|
| S8-01 | 8.2, Ricerca concorrenza: "Ricerca web, Perplexity" | "Firecrawl sul server e ricerca web di Claude"; Perplexity come eccezione (N08) |
| S8-02 | 8.2, Visual e video: "Higgsfield, moda.app, HyperFrames" | S4-08, S4-09 |
| S8-03 | 8.2, Pubblicatore, Analista metriche, Community manager: "Metricool" | S4-06 |
| S8-04 | 8.2, Newsletter: "Lo strumento di newsletter che sceglieremo" | Aggiungere "self-hosted o approvato da Michele" |
| S8-05 | 8.4: "Nella fase 0, con Claude in Slack e la sessione presidiata di Alberto" | "Con Claude Team e la sessione presidiata di Alberto" |
| S9-01 | 9.1 regola 7: "solo fornitori con contratto commerciale e DPA" | Aggiungere "e presenti nel board di Michele, o approvati da lui" |
| S9-02 | 9.1 regola 8: scadenze di conservazione | Aggiungere log in Loki e Wazuh e copie nel PBS |
| S9-03 | 9.2 n.1: "La macchina degli agenti raggiunge solo i servizi in lista" | Resta; coincide con la VLAN APPS |
| S9-04 | 9.2 n.5: "Registro delle azioni a sola aggiunta ... stop di emergenza dal telefono" | Aggiungere "il registro va anche in Loki e Wazuh"; lo stop dal telefono passa dalla pagina del Cancello |
| S9-05 | 9.4 Parere legale: "registrazione delle call, trasferimenti verso gli USA" | Togliere Recall.ai; aggiungere: i pezzi di documenti e dati fiscali che l'MCP RAG passa a Claude Team, la lettura delle trascrizioni di Teams, i metadati di M365, e la voce di "Andrea" solo se resta |
| S10-01 | 10 n.2: "Ogni persona scrive in Notion come vuole i suoi riassunti" | "in BookStack" |
| S10-02 | 10 n.3: "Mattia diventa il secondo amministratore" | "Mattia entra nel gruppo admin di NetBird come secondo amministratore, se Michele è d'accordo" |

### 4.9 Sezione 11, Il piano a fasi

| Cod. | Testo attuale | Cosa scrivere |
|---|---|---|
| S11-01 | Fase 0: "Server in sicurezza (inventario, memoria bilanciata, kit GPU, Proxmox, firewall, tunnel, backup fuori sede)" | "Fasi F0 e F1 del board, guidate da Michele: montaggio, test della RAM, firmware, OPNsense e VLAN, Proxmox su ZFS, NetBird e Traefik, PBS a casa" |
| S11-02 | Fase 0: "primi profili su Hermes Cloud con dati verdi" | Togliere; al suo posto "primi agenti su dati verdi con Claude Team e Claude Code, senza server" |
| S11-03 | Fase 0: "marketing con Claude in Slack" | "con Claude Team" |
| S11-04 | Fase 1: "Hermes sul server; Cancello v1; oscuramento locale; registrazione delle call e prova di Vexa; Telegram e WhatsApp; organigramma in Notion; ... ognuno con il suo bot Slack" | Riscrivere con i componenti del board. Il pilota sul server richiede almeno APPS, DATA, Infisical e LiteLLM, che il board mette fra F2 e F4: va deciso con Michele se anticiparli (§6) |
| S11-05 | Fase 2: "memoria vettoriale; ... Azure spenta" | La memoria vettoriale è il lavoro della fase F4 (pipeline Sirius → MCP); lo spegnimento di Azure è la fase F2 |
| S11-06 | Fase 3: "Un bot per agente in `#agenti`" | Nella chat scelta (N02) |
| S11-07 | Fase 5: "Pilota di Paperclip ...; Buzz esteso" | Nella VLAN LAB; Buzz solo se approvato |
| S11-08 | Fase 6: "Squadra Amministrazione (... bandi)" | Bandi già nella fase F4 (S4-21) |
| S11-09 | Verifica della settimana 8: "un aggiornamento di Hermes che passa i dieci scenari di prova"; "passiamo a un motore nostro ... (Agent SDK)" | Riscrivere sui criteri dell'orchestratore scelto. Aggiungere un criterio: ogni patch critica applicata entro 14 giorni anche con le versioni fissate (N14) |
| S11-10 | "Se l'hardware tarda, la fase 1 parte sulla VM Azure" | Togliere: l'hardware c'è e Azure esce. Al suo posto: "Finché il server non è pronto, gli agenti lavorano su dati verdi con Claude Team" |
| S11-11 | "Dopo la settimana 24 serve una manutenzione continua: aggiornamenti di Hermes, Cancello e server" | "...dell'orchestratore, del Cancello e del server, con la regola dei 14 giorni" |

### 4.10 Sezione 12, Quanto costa

| Cod. | Testo attuale | Cosa scrivere |
|---|---|---|
| S12-01 | 12.1 prima tabella (≈ 300, 290, 140, 310, + 447) | Tabella di §5.2 |
| S12-02 | 12.1 nota: "Telegram (gratis), WhatsApp ..., Buzz (0 €)" | Togliere o spostare fra le eccezioni |
| S12-03 | 12.1 riga "Nuovo per il progetto" ≈ 189 | 20,00-23,10 € (Proxmox e S3 facoltativo) [§5.1] |
| S12-04 | 12.1 riga "Server": "Corrente a 400 W (102,20)" | Resta come stima prudente; aggiungere il PBS di casa, acceso solo di notte [non verificato: pochi euro al mese] |
| S12-05 | 12.1 riga "Voce Andrea" | Segnare "solo se approvata come eccezione" |
| S12-06 | 12.1 riga "Kit commerciale": Google Workspace 54,40 e gli altri | Togliere Google Workspace; Instantly resta; gli altri come eccezioni (§5.1) |
| S12-07 | 12.1 "Totale di listino ≈ 968"; "Esborso nel primo anno ≈ 623 (a regime ≈ 1.265)" | 388-749 € di listino; 42-403 € di esborso nel primo anno [stima, §5.1] |
| S12-08 | 12.2 Tre scenari (301, 968, 2.250) | Da ricalcolare con le stesse regole; il minimo scende sotto i 301 € perché escono Notion, 1Password e il backup [non verificato: da rifare] |
| S12-09 | 12.3 Una tantum | Tabella di §5.3 |
| S12-10 | 12.4: "per 140-310 € al mese in più ... (dopo, fino a circa 760 €...)" | Ricalcolare con §5.2 |

### 4.11 Sezione 13, Rischi

| Cod. | Rischio attuale | Cosa scrivere |
|---|---|---|
| S13-01 | "Hermes è giovane e cambia ogni settimana" | Riscrivere sull'orchestratore scelto. Con le versioni fissate, ogni patch critica va comunque applicata entro 14 giorni (N14) |
| S13-02 | "Un solo server e un solo amministratore ... Azure accesa finché il server non è stabile, Hermes Cloud come riserva" | "UPS con spegnimento pulito, dischi in mirror, PBS a casa con ripristino provato, gruppo admin in NetBird con due persone, secondo nodo nel 2027-28" |
| S13-03 | "Dati fuori dall'UE: ... ElevenLabs e il bot di registrazione stanno negli USA" | Togliere il bot di registrazione (Vexa è in casa); ElevenLabs solo se resta; aggiungere Claude Team che riceve pezzi rossi dall'MCP RAG (N17) |
| S13-04 | "Buzz è giovane"; "WhatsApp" | Solo se restano |
| S13-05 | "Fine del supporto HPE" | Aggiungere "Nodo 2 già in roadmap" |
| S13-06 | Nuovo | **GPU condivisa**: la sera la RTX 4000 va a Experimental-1, ma bandi e indicizzazione girano di notte e Claude Team può interrogare la memoria a ogni ora (N06) |
| S13-07 | Nuovo | **Una sola linea internet**: senza linea di riserva si fermano webhook di Instantly, Pangolin e l'MCP per Claude Team (N15) |
| S13-08 | Nuovo | **Software senza supporto**: MinIO è archiviato e non riceve più patch regolari (N14) |
| S13-09 | Nuovo | **Server in salotto**: rumore e calore con la GPU e le ventole ad alte prestazioni [verificato: 15 §0 punto 5 per il rumore delle configurazioni con GPU] |
| S13-10 | Nuovo | **Esposizione pubblica**: Pangolin e NetBird hanno bisogno di porte raggiungibili da internet o di un VPS (N10) |
| S13-11 | Nuovo | **Flussi che aggirano il Cancello**: n8n e i connettori di Claude Team possono scrivere fuori; servono credenziali in sola lettura dove possibile (C27, N18) |

### 4.12 Sezione 14, Decisioni

| N. | Decisione attuale | Con il board | Cosa scrivere |
|---|---|---|---|
| 1 | Avviare le fasi 0 e 1 con verifica alla settimana 8 | Resta, con contenuto e tempi nuovi | Fasi allineate a F0-F4 (§6) |
| 2 | Completare il server e comprare l'UPS (UPS 1.163-1.293 €; accessori e dischi, tetto 1.000 €) | Hardware completo; UPS rack in F5 | "Comprare il PBS di casa (M920t e 2 dischi, circa 290-610 €) e gli accessori residui (fino a 200 €)" [stima] |
| 2b | Dove mettiamo il server | Deciso: rack in salotto | Togliere |
| 3 | Nessuna spesa per la GPU | Seconda GPU in F5 | "Seconda GPU nella fase F5: 500-830 € secondo il modello" (H07; RTX A2000 12 GB 499-569 € su eBay.de, RTX 2000 Ada 16 GB 648-770 € [verificato: eBay.de, hardwaredealz.com, Yeppon, 25/10/2026]; RTX PRO 2000 Blackwell circa 828 £ in offerta nel Regno Unito [verificato: shop.wearesync.co.uk]) |
| 4 | Slack Pro | Esce | Togliere |
| 5 | Claude in Slack | Esce | Togliere; al suo posto nessun costo: connettore MCP RAG e connettore Microsoft 365 di Claude Team [verificato: support.claude.com, articolo 12542951] |
| 6 | Bot di registrazione Recall.ai | Esce | "Registrazione sul server con Vexa, o trascrizione di Teams: 0 € di abbonamento" |
| 7 | Hermes Cloud | Esce | Togliere |
| 8 | Notion Plus | Esce | Togliere |
| 9 | Voce di "Andrea" | Fuori dal board | "Eccezione da approvare: ElevenLabs e numero italiano, circa 170 € al mese, oppure voce self-hosted dopo la seconda GPU" |
| 10 | Parere legale | Resta | Ambito aggiornato (S9-05) |
| 11 | Tetto API e deposito | Resta | "Tetto applicato da LiteLLM" |
| 12 | Proxmox dalla fase 2 | Resta | Decisione di Michele; 20 € al mese con 2 CPU |
| 13 | Posti Claude Team | Resta | Aggiungere che Claude Team diventa la porta verso la memoria, quindi conviene tenere i posti per tutti e quattro |
| 14 | Claude su server in Europa | AWS non c'è | "Solo se un cliente lo chiede e con il sì di Michele" |
| 15 | Premio mensile | Nessun impatto | Resta |
| 16 | Revisione di sicurezza esterna | Board F3: documenti ISO e CE | Collegarla alla documentazione ISO e Cyber Essentials della fase F3 |
| 17 | Prova di Grok Bot | Fuori dal board | Togliere, o eccezione su soli dati pubblici |
| 18 | Telegram e WhatsApp | Fuori dal board | Togliere, o eccezione |
| 19 | Buzz | Self-hosted, pre-1.0 | "Prova nella VLAN LAB, se Michele la ammette" |
| 20 | Fase 6 | Bandi in F4 | Togliere i bandi dalla fase 6; fatturazione e firma elettronica fuori dal board, da approvare |
| Verifiche | "il modello esatto del server"; "quale suite di posta"; "quanto costa oggi la VM Azure"; "DPA e sede di Recall.ai" | Chiuse o cambiate | Togliere le prime due; "quanto costano oggi tutte le VM Azure"; togliere Recall.ai; aggiungere "cos'è Sirius" e "costo dell'IP fisso" |

### 4.13 Sezione 15 e appendici

| Cod. | Testo attuale | Cosa scrivere |
|---|---|---|
| S15-01 | Fase 0: 15-20 giorni di sviluppo, con il server a carico di Alberto (22 §5) | Il server è lavoro di Michele nelle fasi F0-F1: separare i suoi giorni da quelli degli agenti |
| S15-02 | "Se alla settimana 8 cambiassimo orchestratore ... 10-15 giorni di base, più il rifacimento di bacheca, routine e collegamenti alle chat" | Rifare la stima: routine con n8n, bacheca in Jira o in PostgreSQL, chat con Teams, porta dei modelli con LiteLLM [non verificato: stima da rifare] |
| S15-03 | "La prova di Buzz occupa 4-6 giorni" | Solo se Buzz resta |
| A-01 | J4: "Passaggi fra agenti nella bacheca di Hermes" | "Passaggi fra agenti nella bacheca dell'orchestratore (o in Jira)" |
| A-02 | J9: "Slack dal primo giorno; Telegram e WhatsApp via Hermes; Buzz" | "Teams per le persone; chat degli agenti da decidere; Telegram e WhatsApp solo se approvati" |
| A-03 | A1: "Recall.ai con DPA verificato, o Vexa" | "Vexa sul server, o trascrizione di Teams" |
| A-04 | A2: "Notion: regole, processi, obiettivi, catalogo" | "BookStack e PostgreSQL" |
| A-05 | A3: "Postgres con pgvector, embedding sulla nostra GPU" | "Qdrant con BM25 e reranker, embedding sulla nostra GPU" |
| A-06 | A4: "Hermes sul server, versione fissata" | "Orchestratore sul server (Agent SDK o Hermes)" |
| A-07 | A7: "`#agenti` in Slack" | "Stanza degli agenti nella chat scelta" |
| A-08 | B1: "canale condiviso col cliente dopo il sì" | "canale condiviso in Teams dopo il sì" [non verificato: canali condivisi con organizzazioni esterne, da provare] |
| A-09 | B4, C5, C6: "Notion" | "Jira" (B4); "BookStack" (C5, C6) |
| A-10 | C4: "note vocali trascritte in casa" | Dipende da N05 |
| A-11 | D4: "moda.app o Claude" | "Claude con i nostri template; moda.app solo se approvato" |
| A-12 | E3: "Tetti per agente, catena e persona" | Aggiungere "in LiteLLM" |
| A-13 | F1-F2: "Metadati del Workspace" | "Metadati di Microsoft 365" |
| A-14 | F5: "Slack come porta unica, Claude Team per tutti" | "Teams e Claude Team per tutti; Open WebUI per i modelli locali" |
| A-15 | G5: "ElevenLabs e numero italiano" | Dipende da N07 |
| A-16 | G9: "Registro del Cancello esportato in Notion" | "in BookStack o Grafana" |
| A-17 | K1: "anche come evento in calendario" | "evento in Outlook" |
| A-18 | K4: "Bibliotecario e Capo di gabinetto, in chat e dal telefono" | "Claude Team con l'MCP RAG, il Bibliotecario e il Capo di gabinetto" |
| A-19 | K14, L3: fase 3-6 | "Dati fiscali di Sirius nella memoria dalla fase F4" |
| A-20 | L4: "Agente bandi e finanziamenti, fase 6" | "Fase F4 del board" |
| A-21 | L11: "Sistemista, fase 2" | "Sistemista sullo stack OBSRV, dopo la fase F3" |
| A-22 | Lacune dichiarate | Aggiungere: trascrizione e voce dipendono dalla GPU; gli strumenti fuori dal board sono eccezioni da decidere |
| B-01 | Appendice B, punteggi | Nota "punteggi di prima del board" (S5-13) |
| C-01 | Appendice C, cartella | Aggiungere `allegati/infra` (il board di Michele) e `ricerca/25` |
| L-01 | `LEGGIMI.md`: "ricerca/13 Modelli open source sul server (RTX 4000, 160 GB)" | "192 GB"; aggiungere `allegati/infra` e `ricerca/25` |
| R-01 | `ricerca/22-architettura-scelta.md` (schema §2, n8n §3, costi §6-7, rischi §8, decisioni §9) | Segnare in testa: "superato dal board di Michele per Slack, Notion, Cloudflare Tunnel, Recall.ai, Hermes Cloud, pgvector, Postgres 17, n8n, hardware e costi; vedi ricerca/25" |

---

## 5. Costi ricalcolati

Stime del 25/10/2026, IVA esclusa, cambio 1 $ = 0,8934 € come nella proposta. Le cifre di partenza vengono da PCEO §12 e da 14 §11.

### 5.1 Costi mensili dello scenario consigliato

| Voce | Proposta (€/mese) | Con il board (€/mese) | Nota |
|---|---|---|---|
| Slack Pro × 4 | 27,00 | 0 | Teams dentro M365 (C01) |
| Notion Plus × 4 | 35,74 | 0 | BookStack e Jira (C02); Jira è già nel board, costo attuale non trovato |
| Claude in Slack | 44,67 | 0 | C01 |
| Hermes Cloud | 18,67 | 0 | C10 |
| Proxmox Community, 2 socket | 20,00 | 20,00 | Decide Michele (C14) |
| Backup fuori sede | 3,10 | 0-3,10 | S3 facoltativo (C16) |
| Password manager | 22,29 | 0 | Vaultwarden e Infisical (C15) |
| Registrazione call | 17,42 | 0 | Vexa o Teams (C06) |
| **Nuovo per il progetto** | **≈ 189** | **≈ 20-23** | |
| API Claude (stima, coperte dai crediti) | ≈ 196 | ≈ 196 | Ora passano da LiteLLM. Una parte delle domande alla memoria passa da Claude Team, quindi la stima può scendere [non verificato] |
| Corrente del server (400 W) | 102,20 | 102,20 | Stima prudente invariata; il PBS di casa aggiunge pochi euro [non verificato] |
| Voce "Andrea" | 170,28 | 0 o 170,28 | Solo se diventa eccezione (C08) |
| Google Workspace | 54,40 | 0 | M365 (C03); M365 forse già pagato, da confermare. Se non lo è, Business Standard × 4 ≈ 48,52 € [non verificato: 14 riga 271] |
| Instantly | 69,33 | 69,33 | Resta (C32) |
| Apollo, Apify, Metricool, moda.app, Higgsfield | 187,62 | 0-187,62 | Eccezioni da decidere (N08) |
| **Totale di listino** | **≈ 968** | **≈ 388-749** | |
| **Esborso nel primo anno** (meno API coperte e 150 € di Azure) | **≈ 623** | **≈ 42-403** | Il risparmio di Azure va ricalcolato su tutte le VM (N20) |
| Claude Team alla fine del bundle | + 447 | + 447 | Invariato (C22) |

Conti: minimo 20,00 + 196 + 102,20 + 0 + 69,33 = 387,53 €; massimo 23,10 + 196 + 102,20 + 170,28 + 69,33 + 187,62 = 748,53 € [stima].

### 5.2 Quanto spendiamo in più rispetto a oggi

| Periodo | Proposta | Con il board | Cosa comprende |
|---|---|---|---|
| Fasi F0-F1 (prime settimane) | ≈ 300 | ≈ 102-125 | Corrente del server e, se scelto, Proxmox e S3; Azure ancora acceso |
| Dopo lo spegnimento di Azure (F2) | ≈ 140 | da circa -48 a -25 | Se Azure costa almeno 150 € al mese, dopo la fase F2 si spende meno di oggi [stima; costo reale di Azure non trovato] |
| Con la voce di "Andrea" | ≈ 310 | + 170, solo se approvata | C08 |
| Strumenti commerciali fuori dal board | Kit "serve comunque" | Solo la parte nuova, se approvata | N08 |
| Fine del bundle Claude Team | fino a + 447 | fino a + 447 | Invariato |

### 5.3 Costi una tantum

| Voce | Proposta | Con il board | Fonte |
|---|---|---|---|
| UPS 1.500 VA | 1.163-1.293 € subito | 0 ora; UPS rack 2U nella fase F5, 1.072-1.163 € IVA inclusa | [verificato: board; eBay.de IT-Planet e Yeppon, 25/10/2026] |
| Accessori HPE e dischi | tetto 1.000 € | 0-200 € (guide, cavo GPU, coperture, se mancano) | [non verificato: stima; ventole, dissipatori, alimentatori e dischi già presenti per il messaggio di Michele] |
| 2 moduli RAM | circa 138 € | 0 | H01 |
| Proxmox Backup Server a casa | non previsto | M920t 186-355 € più 2 HDD SATA 100-250 € | [verificato: refurbed.it, pccomponentes.it per l'M920t; dischi non verificato] |
| Deposito API | circa 223 € | circa 223 € | Invariato |
| Parere legale | tetto 2.500 € | tetto 2.500 € | Ambito aggiornato (S9-05) |
| Seconda GPU | 2.438-2.555 €, "non ora" | 500-830 € nella fase F5 | H07 |
| RAM in più | non prevista | circa 828 €, facoltativa | H01 [stima] |
| IP fisso e server da pagare a Bargain | non previsti | da chiedere | H13, N20 |
| **Chiesto oggi** | **al massimo 5.016 €** | **circa 3.009-3.528 €** | 223 + 2.500 + PBS (286-605) + accessori (0-200) [stima] |

---

## 6. Tempi: le fasi della proposta e la roadmap del board

Il board ordina il lavoro per fasi che partono "quando la precedente è validata", senza date. La proposta usa le settimane. Il punto critico: la proposta mette il pilota degli agenti sul server nelle settimane 4-8, mentre il board porta LXC GPU e LiteLLM con budget nella fase F4, dopo l'uscita da Azure (F2) e la sicurezza (F3).

| Proposta | Contenuto | Fase del board | Conflitto | Proposta di allineamento |
|---|---|---|---|---|
| Fase 0 (sett. 1-3) | Server in sicurezza, backup, chiavi API, Hermes Cloud, debito di SersanOutreach, registro dei trattamenti, marketing con Claude in Slack | F0 e F1 | Il server è di Michele; Hermes Cloud e Slack escono | Fase 0 = F0-F1 di Michele più il lavoro che non chiede il server: marketing con Claude Team, debito di sicurezza di SersanOutreach, registro dei trattamenti, regole personali in BookStack (appena c'è) |
| Fase 1 (sett. 4-8) | Orchestratore e Cancello sul server, post-call, debrief, oscuramento locale, registrazione | F2-F4 | Mancano ancora APPS con allowlist, LiteLLM con budget e GPU in LXC | Due strade da decidere con Michele: (a) anticipare in F1-F2 un "posto agenti" in APPS con LiteLLM, PostgreSQL e Infisical, senza GPU e senza dati rossi; (b) spostare il pilota dopo F3 e nel frattempo lavorare su dati verdi con Claude Team |
| Fase 2 (sett. 9-13) | SersanOutreach sul server, memoria vettoriale, Azure spenta | F2 (migrazione) e F4 (pipeline Sirius → MCP, Qdrant) | Ordine diverso: il board sposta prima e indicizza dopo | Seguire il board: migrazione in F2, memoria in F4 |
| Fasi 3-5 (sett. 14-24) | Chat fra agenti, organizzazione, vendite e voce, Paperclip, Buzz | Dopo F4; prove in F5 (LAB) | Nessuno, se le prove stanno in LAB | Paperclip e Buzz nella VLAN LAB |
| Fase 6 | Amministrazione, bandi, contratti | Bandi in F4 | I bandi arrivano prima | Togliere i bandi dalla fase 6 |
| Verifica sett. 8 | Criteri tecnici su Hermes | Nessuno | Dipende dall'orchestratore | Criteri riscritti dopo la scelta (N01), più la regola dei 14 giorni |

Serve da Michele una stima in settimane per F0-F4, così la proposta può tornare a un calendario.

---

## 7. Cose che il board non dice e che la proposta deve chiarire

| Cod. | Tema | Perché conta | Proposta da portare a Michele |
|---|---|---|---|
| N01 | **Orchestratore e Cancello: quale e dove** | Il board non cita né Hermes né l'Agent SDK né il Cancello | Agent SDK o Hermes in una macchina della VLAN APPS, con il Cancello accanto; RAM dentro i circa 53 GB liberi. L'Agent SDK usa solo la chiave API e passa da LiteLLM [verificato: code.claude.com]. Il confronto con Hermes va fatto in un rapporto a parte, con i componenti del board |
| N02 | **La chat di gruppo di persone e agenti** (J9, A7) | Slack esce; Teams c'è per le persone; Buzz, Telegram e WhatsApp non ci sono | Tre opzioni: Teams anche per gli agenti; una chat self-hosted per le stanze degli agenti (Buzz o un'altra); solo pagina del Cancello più avvisi in Teams. Hermes ha già un canale Teams [verificato: 10 riga 95]; con l'Agent SDK il collegamento va costruito. Un bot in Teams richiede una registrazione dell'app in Entra [non verificato: da controllare se serve anche una risorsa Azure Bot, visto che Azure esce] |
| N03 | **Le approvazioni dal telefono** | Le carte erano in Slack e Telegram | Pagina del Cancello raggiungibile da NetBird (o da Pangolin), con identità Entra e chiave FIDO2; avviso in Teams con il link. I telefoni che approvano entrano nel perimetro Cyber Essentials, anche se personali [verificato: iasme.co.uk, "Cyber Essentials myth busting": lo scope comprende anche i dispositivi BYOD, con le eccezioni dello schema] |
| N04 | **Telegram e WhatsApp** | La visione li chiede (J9) | Eccezione da decidere; il debrief e le carte funzionano anche con Teams sul telefono |
| N05 | **Registrazione e trascrizione delle call** | Recall.ai esce; Whisper non è nel board | Due strade: Vexa sul server (Apache-2.0; Meet, Teams, Zoom) [verificato: github.com/Vexa-ai/vexa]; per le call in Teams, la trascrizione nativa letta con Microsoft Graph, che chiede un permesso applicativo, una policy di accesso creata dall'admin e un'impostazione di Teams [verificato: learn.microsoft.com, calltranscript-get e onlinemeeting-list-transcripts; office365itpros.com]; secondo una fonte terza è un'API a consumo [verificato: docs.glean.com, fonte terza] |
| N06 | **GPU condivisa e lavori notturni** | La RTX 4000 la sera va a Experimental-1, ma i bandi girano "ogni notte" con il modello 4B, e Claude Team può interrogare la memoria a ogni ora (l'MCP RAG deve calcolare l'embedding della domanda) | Fasce orarie scritte; embedding e reranker anche su CPU quando la GPU è altrove (Qwen3-Embedding-0.6B gira su CPU [verificato: 13 riga 287]); bandi e indicizzazione nella fascia AI; con la seconda GPU il problema sparisce. Passare la scheda fra un LXC e una VM con uno script va provato [non verificato] |
| N07 | **La voce di "Andrea"** (G5, K10) | ElevenLabs e Twilio non sono nel board; il numero di telefono resta comunque un servizio esterno | Eccezione ElevenLabs più numero (circa 170 € al mese), oppure voce self-hosted (trascrizione, Claude, sintesi vocale) sulla seconda GPU nella fase F5 [non verificato: fattibilità e qualità in italiano da provare]. In ogni caso dalla fase 4 e con il parere legale |
| N08 | **Strumenti commerciali e di marketing fuori dal board** | Michele: "tutto il resto self-hosted" | Tabella qui sotto |
| N09 | **Database di SersanOutreach** | Il board tiene Supabase come "DB del prodotto" e ha PostgreSQL 16 in casa; oggi SersanOutreach usa Postgres 17.6 su Supabase [verificato: 01 riga 103] | Chiedere a Michele se "il prodotto" è SersanOutreach. Se il database viene in casa su PostgreSQL 16, il passaggio da 17.6 a 16 è un ritorno di versione: PostgreSQL non garantisce che un dump si carichi su una versione principale più vecchia [verificato: postgresql.org, pagina di pg_dump]. Meglio PostgreSQL 17 per SersanOutreach, oppure restare su Supabase |
| N10 | **Porte e indirizzi pubblici** | Il board dice "nessuna porta aperta" e "IP fisso da richiedere" | Pangolin in modalità tunnel di solito vive su un VPS con IP pubblico (80 e 443 TCP, 51820 UDP), e il lato di casa esce senza porte aperte [verificato: guide ramnode.com e computingforgeeks.com, fonti terze]. NetBird self-hosted chiede 80 e 443 TCP e 3478 UDP raggiungibili [verificato: documentazione NetBird, copia su mintlify.com]. Il connettore MCP di Claude Team arriva dagli indirizzi di Anthropic, quindi l'endpoint deve essere pubblico [verificato: support.claude.com, articolo 11175166]. Va deciso: VPS (un cloud in più, con un costo) oppure porte aperte solo verso la VLAN EDGE |
| N11 | **Sirius** | È la prima sorgente della pipeline (fiscale, clienti, documenti), ma la proposta non lo cita | Chiarire cos'è, chi lo usa, quali dati contiene, e se è lo strumento di fatturazione e contabilità della decisione 20. I dati fiscali sono rossi |
| N12 | **mcp-enrich, mcp-memory, runner-dash, Homepage** | Sono nel blueprint di Michele; la proposta parla di due MCP di SersanOutreach (lettura e operatore) | Chiarire cosa sono e se coincidono con i due MCP di SersanOutreach |
| N13 | **n8n** | La proposta (22 §3) diceva di non usarlo; il board lo usa | Tenerlo per routine interne e ingressi deterministici; mai invii a esterni; non entra in ciò che si rivende [verificato: docs.n8n.io] |
| N14 | **Cyber Essentials** | Il sistema di agenti sta nel perimetro | Da fine aprile 2026 (versione 3.3; 26 o 27 aprile secondo le fonti) le patch critiche o ad alto rischio non applicate entro 14 giorni e la MFA mancante sui servizi cloud fanno fallire la verifica [verificato: cobweb.com e wikipedia.org, fonti terze; la regola dei 14 giorni: iasme.co.uk, aggiornamento 2021]. Il software deve essere con licenza e supportato [verificato: iasme.co.uk]. Conseguenze: versioni fissate sì, ma patch critiche entro 14 giorni; Buzz pre-1.0 e Paperclip solo in LAB; MinIO è archiviato dal 12/02/2026 e non riceve patch regolari [verificato: infoq.com, itsfoss.com, vonng.com], quindi va chiesto a Michele se sostituirlo prima che ci finiscano file degli agenti |
| N15 | **Una sola linea e un solo UPS** | FTTH unica; UPS attuale di potenza non nota | Chiedere potenza e autonomia dell'UPS attuale e se serve una linea di riserva (per esempio 4G o 5G su OPNsense) [non verificato: proposta] |
| N16 | **Dove stanno i dati sui dischi** | 800 GB di SSD per sistemi e servizi; 5,4 TB su HDD | Chiedere se PostgreSQL e Qdrant stanno sugli SSD e quanto spazio prevede per trascrizioni e indici |
| N17 | **Claude Team e i dati rossi** | L'MCP RAG passa a Claude Team pezzi di documenti dei clienti e dati fiscali, con le PII marcate | Regola nel MCP RAG: quali colori può restituire e a chi; registro delle query già previsto dal board. Claude Team non ha la conservazione zero [verificato: 16 riga 158]. Punto da mettere nella DPIA e nel parere legale |
| N18 | **Connettore Microsoft 365 di Claude** | Claude può leggere Outlook, SharePoint, OneDrive e Teams, e con le scritture accese anche inviare mail [verificato: support.claude.com, articolo 12542951; claude.com/docs/connectors/microsoft/365] | Utile per le persone; le scritture vanno tenute spente, perché un invio deve passare dal Cancello |
| N19 | **Chi fa cosa** | La proposta (22 §5) dava il server ad Alberto | Michele guida F0-F3; Alberto e Mattia agenti e Cancello; Mattia nel gruppo admin se Michele è d'accordo |
| N20 | **Costi non noti** | Servono per il quadro dei costi | Costo di tutte le VM Azure e del VPS WireGuard; piano e costo di M365 (con o senza Teams); costo di Jira; IP fisso; eventuale VPS per Pangolin e NetBird; importo ancora da pagare a Bargain |
| N21 | **Open WebUI** | È nel board, la proposta non lo cita | "AI per tutti" (F5 della visione) anche sui modelli locali, con il budget di LiteLLM per persona. La licenza vieta di togliere il marchio Open WebUI sopra i 50 utenti, quindi non conta per l'uso interno ma conta per la rivendita [verificato: docs.openwebui.com/license] |

**N08 in dettaglio: strumenti fuori dal board**

| Strumento | A cosa serve oggi | Dati che tocca | Alternativa self-hosted | Proposta |
|---|---|---|---|---|
| Apollo (43,78 €) | Ricerca di contatti B2B | Gialli (contatti di lavoro) | Nessuna: è una banca dati di contatti | Eccezione, oppure si rinuncia e si usa l'arricchimento di SersanOutreach |
| Apify (15,19 €) | Segnali di assunzione da Indeed per SersanOutreach [verificato: 01 riga 97] | Pubblici | Firecrawl self-hosted, già nel board | Sostituire con Firecrawl [non verificato: copertura di Indeed da provare] |
| Perplexity (costo non trovato) | Arricchimento in SersanOutreach [verificato: 01 riga 96] | Pubblici | Firecrawl più ricerca web di Claude | Eccezione finché non è sostituito |
| Metricool (59,86 €) | Programmazione post e metriche | Pubblici e account social | Postiz (AGPL-3.0) [verificato: README postiz-app] | Da decidere; la programmazione resta in sessione presidiata come chiedono le direttive |
| moda.app (26,80 €) | Slide | Interni, a volte di clienti | Slide da Claude con i nostri template | Sostituire, o eccezione solo su dati verdi |
| Higgsfield (41,99 €) | Video e immagini per i post | Pubblici; volti dei founder | Nessuna di qualità sulla RTX 4000 [non verificato] | Eccezione su contenuti pubblici |
| ElevenLabs e Twilio (170,28 €) | Voce di "Andrea" | Rossi (audio di chiamate) | Da provare sulla seconda GPU | N07 |
| IPRoyal (proxy) | LinkedIn lato server | Gialli | Estensione nel browser dei membri, senza proxy [verificato: 01 riga 208] | Non serve |
| Canva (solo scenario completo) | Grafiche | Pubblici | Template interni | Togliere dallo scenario completo |
| After Effects | Motion graphics | Pubblici | HyperFrames in locale | Software desktop: resta, dentro Cyber Essentials |
| Strumento di newsletter | Newsletter (K9) | Gialli (iscritti) | Da cercare [non verificato] | Da decidere nella fase 3 |
| Firma elettronica e fatturazione | Fase 6 (L1, L2) | Rossi | Da cercare [non verificato] | Da decidere alla settimana 24 |

---

## 8. Domande aperte per Michele

1. L'orchestratore: confermi Agent SDK come prima scelta, con Hermes come alternativa da confrontare? Dove lo metti (VLAN APPS, VM o LXC) e quanta RAM gli dai?
2. La chat di gruppo: Teams anche per gli agenti, una chat self-hosted, o solo pagina del Cancello più avvisi in Teams? Telegram e WhatsApp sono ammessi?
3. Le approvazioni: va bene una pagina del Cancello raggiungibile da NetBird con Entra e FIDO2?
4. Le call: Vexa sul server, trascrizione di Teams via Graph, o tutte e due? Dove gira Whisper?
5. La GPU: quali sono le fasce orarie? I lavori notturni (bandi, indicizzazione) e le domande serali alla memoria possono usare la CPU?
6. La seconda GPU: il modello giusto è una RTX A2000 da 12 GB, una RTX 2000 Ada da 16 GB o una RTX PRO 2000 Blackwell da 16 GB? Entra nel riser del DL380 accanto alla RTX 4000?
7. "Supabase, DB del prodotto": il prodotto è SersanOutreach? Se il database viene in casa, su PostgreSQL 16 o 17?
8. Pangolin e NetBird: su un VPS (quale e quanto costa) o sul server con porte aperte verso EDGE? E l'endpoint MCP per Claude Team?
9. Cos'è Sirius, e cosa sono mcp-enrich, mcp-memory e runner-dash?
10. Quali strumenti fuori dal board ammetti come eccezione: Apollo, Perplexity, Metricool, moda.app, Higgsfield, ElevenLabs con numero, strumento di newsletter, firma elettronica, fatturazione?
11. Buzz e Paperclip possono essere provati nella VLAN LAB?
12. MinIO resta, nonostante sia archiviato? Con cosa lo sostituiresti?
13. UPS attuale: potenza, autonomia, e basta fino alla fase F5?
14. Serve una linea internet di riserva?
15. Che stima in settimane dai alle fasi F0-F4, e accetti di anticipare un "posto agenti" con LiteLLM prima di F4?
16. Abbonamenti Proxmox VE e PBS: li vuoi, e da quando?
17. Mattia può entrare nel gruppo admin di NetBird?
18. Costi da conoscere: tutte le VM Azure e il VPS WireGuard, piano M365 (con o senza Teams), Jira, IP fisso, importo da pagare a Bargain.

---

## 9. Fonti

**File del progetto (letti il 25/10/2026)**
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`, `SerSan Infra Board.html` (riga 309: la nota sulla GPU giorno e sera).
- Messaggio di Michele ad Alberto del 25/10/2026, riportato nel compito.
- `PRESENTAZIONE-CEO.md`, `LEGGIMI.md`, `ricerca/00-visione-funzionalita.md`, `ricerca/01-sersanoutreach.md`, `ricerca/10-hermes-agent.md`, `ricerca/13-modelli-open-source-sul-server.md`, `ricerca/14-costi-abbonamenti-e-api.md`, `ricerca/15-hardware-server-e-rete.md`, `ricerca/16-gdpr-ai-act-e-regole.md`, `ricerca/22-architettura-scelta.md`.

**Pagine web (rilevazione del 25/10/2026)**
- CPU: https://www.intel.com/content/www/us/en/products/sku/192444/intel-xeon-gold-6230-processor-27-5m-cache-2-10-ghz/specifications.html (pagina Intel con i dati della Gold 5218, URL anomalo); https://www.itcreations.com/product/111395
- GPU: https://www.gigazine.net/gsc_news/en/20240213-nvidia-rtx-2000-ada-generation ; https://getdeploying.com/gpus/nvidia-a2000-vs-nvidia-rtx-2000-ada ; https://emarque.co/products/nvidia-rtx-pro-2000-blackwell-professional-graphics-card ; https://shop.wearesync.co.uk/900-5g195-2551-000.html ; https://www.shi.com/Product/50567643 ; https://www.yeppon.it/products/pny-scheda-grafica-rtx-1286630 ; https://www.hardwaredealz.com/hardware/gpu/nvidia-rtx-2000-ada-generation/preisvergleich.33598 ; https://www.ebay.de/itm/389075110417
- Vexa: https://github.com/Vexa-ai/vexa ; https://newreleases.io/project/github/Vexa-ai/vexa/release/v0.6
- Pangolin: https://ramnode.com/guides/series/pangolin/introduction-architecture ; https://computingforgeeks.com/install-pangolin-self-hosted-reverse-proxy/
- NetBird: https://www.mintlify.com/netbirdio/netbird/deployment/self-hosted
- Claude, connettori: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp ; https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector ; https://www.claude.com/docs/connectors/microsoft/365
- Agent SDK e gateway: https://code.claude.com/docs/en/agent-sdk/overview ; https://code.claude.com/docs/en/llm-gateway
- LiteLLM: https://docs.litellm.ai/docs/proxy/users
- n8n: https://docs.n8n.io/sustainable-use-license/ ; https://docs.n8n.io/n8n-community-license/community-license/license-faq.md
- MinIO: https://infoq.com/news/2025/12/minio-s3-api-alternatives/ ; https://itsfoss.com/news/minio-moves-away-from-open-source/ ; https://blog.vonng.com/en/db/minio-resurrect/
- Cyber Essentials: https://cobweb.com/content-hub/blogs/cyber-essentials-changes-april-2026/ ; https://en.wikipedia.org/wiki/Cyber_Essentials ; https://iasme.co.uk/articles/changes-to-cyber-essentials-requirements-april-2021-update ; https://iasme.co.uk/articles/cyber-essentials-myth-busting
- Proxmox: https://www.horizoniq.com/blog/proxmox-subscription/ ; https://wz-it.com/en/knowledge/proxmox/how-much-does-proxmox-cost/
- Microsoft Graph, trascrizioni: https://learn.microsoft.com/en-us/graph/api/calltranscript-get?view=graph-rest-1.0 ; https://learn.microsoft.com/en-us/graph/api/onlinemeeting-list-transcripts ; https://office365itpros.com/2026/09/21/teams-meeting-graph-api/ ; https://docs.glean.com/connectors/native/teams/teams-transcripts
- Open WebUI: https://docs.openwebui.com/license/
- Postiz: https://cdn.jsdelivr.net/gh/gitroomhq/postiz-app@main/README.md ; https://www.mintlify.com/gitroomhq/postiz-app/self-hosting/overview
- PostgreSQL: https://www.postgresql.org/docs/current/app-pgdump.html
- PBS a casa: https://www.refurbed.it/en-it/p/lenovo-thinkcentre-m920t-tower ; https://www.pccomponentes.it/ssd-lenovo-thinkcentre-m920t-intel-core-i5-8500-8-gb-256-gb
- UPS: https://www.yeppon.it/collections/smart-ups-1500-apc ; https://www.ebay.de/p/133943213
