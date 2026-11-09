# 33 · Costi v2: il progetto nel perimetro del board di Michele

Rilevazione del **25/10/2026**, seconda stesura della giornata. Aggiorna i costi di `ricerca/14`, di `ricerca/22` §6-7 e della `PRESENTAZIONE-CEO.md` §12 dopo il board dell'infrastruttura di Michele, che è vincolante. È allineato ai rapporti di oggi sul board (25), sul motore (26, 27), sulla chat (28), sulla conoscenza (29), sulle call (30) e sulla voce di "Andrea" (31).

## In breve

Il board di Michele toglie quasi tutti gli abbonamenti nuovi del progetto. Slack, Notion, Claude in Slack, Hermes Cloud, Recall.ai, ElevenLabs, il password manager e il backup in cloud spariscono: valevano circa **257 € al mese**, e le stesse funzioni girano sul server o dentro M365. Esce anche Google Workspace (54 €), perché posta e identità stanno su M365. Restano o si aggiungono poche voci: Proxmox (20 €), Jira Standard se oggi SerSan usa il piano Free (28 €), l'IP fisso (fino a 10 €), la corrente del server (circa 105 € a 400 W), il numero e le chiamate di "Andrea" con un operatore italiano (44-90 € invece di circa 170 €) e Instantly (69 €), l'unico strumento commerciale che il board tiene. Nello scenario consigliato il listino mensile scende da circa **968 €** a circa **519 €**. La spesa in più rispetto a oggi, contata come nella presentazione (senza il kit commerciale), scende da circa 300 € a circa **135 €** nelle prime fasi; dopo lo spegnimento di Azure diventa circa **15 € in meno di oggi**; con gli agenti e Andrea è circa **104 €** (prima circa 310 €); alla fine dell'anno gratuito di Claude Team sale a circa **551 €** (prima circa 757 €); senza crediti API arriva a circa 746 €. Instantly aggiunge 69 € a ogni riga, se oggi non è già pagato. Apollo, Apify, Metricool, moda.app e Higgsfield (188 € al mese in `ricerca/14`) non sono nel board: se restano, sono eccezioni da far approvare a Michele. Sul piano dei costi Hermes e l'Agent SDK di Claude si equivalgono: zero licenza, si paga solo l'API. Le spese una tantum sono circa **3.100-4.100 € subito** (backup a casa, chiavi FIDO2, parere legale, piccoli accessori, eventuale credito API), contro i 5.016 € chiesti prima, e circa **1.700-2.350 € più avanti** nella fase F5 (seconda GPU da 16 GB, UPS rack, RAM facoltativa). Le voci più incerte sono la corrente vera del server, l'uso "illimitato" delle chiamate per un agente automatico, i crediti API, il piano M365 di SerSan e il futuro di MinIO. Ogni cifra di questo paragrafo ha fonte ed etichetta nelle sezioni 2-4 [non verificato: calcoli riassunti].

## Come leggere questo documento

- **Prezzi IVA esclusa**, salvo dove è scritto. Dove un negozio mostra solo prezzi con IVA, divido per 1,22 (IVA italiana) o per 1,19 (IVA tedesca) e lo scrivo.
- **Cambio**: 1 USD = 0,8934 EUR, come in `ricerca/14` (riferimento BCE del 23/10/2026) [verificato: ricerca/14, riga 7]. Per le sterline uso 1 GBP = 1,1872 EUR, come `ricerca/28` [non verificato: cambio di ricerca/28 §2.1].
- **Date**: le pagine web le ho lette il **25/10/2026**, salvo dove indico un'altra data. I prezzi presi da `ricerca/14` e dalla presentazione sono del **24/10/2026**.
- **Etichette**:
  - **[verificato: fonte]**: ho letto il dato sulla pagina o nel file citato.
  - **[non verificato]**: il dato viene da risultati di ricerca, rivenditori, forum o da una mia stima. Va confermato prima di spendere.
- **Somme e conversioni**: sono calcoli miei sulle voci delle tabelle. Valgono quanto le voci da cui partono.
- **Il board è vincolante**: dove un rapporto precedente dice altro, vale il board [verificato: allegati/infra/SerSan Infra Board.md].

---

## 1. Cosa cambia nel perimetro

- **Restano in cloud**: M365 / Entra ID (identità, MFA, posta), Claude Team (ragiona sul RAG via MCP), API Anthropic (crediti, dietro LiteLLM), Cloudflare (DNS), GitHub (runner in casa), Supabase (DB del prodotto), Vercel (deploy clienti), Jira, Instantly (outreach), S3 fuori sede facoltativo (B2 o Hetzner) [verificato: allegati/infra/board-testo-completo.txt, sezione "Cloud & SaaS che restano"].
- **Esce**: tutto Azure. La fase F2 si chiama "Via da Azure" e chiude con "Spegnere le VM Azure" [verificato: idem, roadmap F2].
- **Va sul server**: n8n, mcp-enrich, mcp-memory, openoutreach, LiteLLM, Open WebUI, MCP RAG, Firecrawl, bandi-watcher, BookStack, PostgreSQL 16, MinIO, Qdrant, Vaultwarden, Infisical, runner GitHub, Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox, Ollama con Qwen3-4B, Infinity con embedding e reranker, Docling [verificato: allegati/infra/board-vlan.txt].
- **Hardware già preso**: HPE DL380 Gen10, 2 Xeon Gold 5218, 192 GB ECC, 2 SSD da 800 GB in mirror, 6 HDD SAS da 1,8 TB in 3 mirror (circa 5,4 TB), Quadro RTX 4000, ventole e dissipatori performance, 2 alimentatori da 800 W Titanium [verificato: board e messaggio di Michele del 25/10/2026].
- **Backup**: Proxmox Backup Server su un Lenovo M920t da comprare, a casa, con 2 HDD SATA in mirror [verificato: board, sezione "Sede 2 · casa"].
- **Motore degli agenti**: Michele chiede di valutare l'Agent SDK di Claude al posto di Hermes. Per i costi la scelta conta poco (§2.6).
- **Telefono di Andrea**: il board non elenca un operatore telefonico. Per Andrea serve per forza [verificato: ricerca/31, "In breve"].

---

## 2. Costi mensili

### 2.1 Cosa sparisce

Le cifre "prima" sono quelle dello scenario consigliato della presentazione, prezzi del 24/10/2026 [verificato: PRESENTAZIONE-CEO.md §12.1].

| Voce | € al mese prima | € al mese ora | Cosa la sostituisce | Fonte del "prima" |
|---|---|---|---|---|
| Slack Pro × 4 | 27,00 | 0 | Teams di M365, con un bot per gli agenti e le carte di approvazione [verificato: ricerca/28, "In breve"] | [verificato: ricerca/14 §5, https://slack.com/pricing] |
| Notion Plus × 4 | 35,74 | 0 | BookStack per i testi, PostgreSQL per i dati, Jira per i task [verificato: ricerca/29, "In breve"] | [verificato: PRESENTAZIONE-CEO.md §12.1; prezzo di origine non verificato in ricerca/14 §5] |
| Claude in Slack, con tetto | 44,67 | 0 | Claude Team con il connettore MCP RAG [verificato: ricerca/25, C01] | [verificato: ricerca/22 §6] |
| Hermes Cloud di riserva | 18,67 | 0 | Motore sul server (Agent SDK o Hermes self-hosted) | [verificato: ricerca/22 §6] |
| Recall.ai, 30 ore di call | 17,42 | 0 | Trascrizione nativa di Teams via Graph, bot Vexa self-hosted per le call esterne, trascrizione sulla GPU [verificato: ricerca/30, "In breve"] | [verificato: ricerca/22 §6] |
| ElevenLabs Pro per Andrea | 88,45 | 0 | Voce e ascolto con modelli aperti sul server [verificato: ricerca/31, "In breve"] | [verificato: PRESENTAZIONE-CEO.md §12.1] |
| Password manager (1Password Teams Starter) | 22,29 | 0 | Vaultwarden e Infisical sul server (VLAN 40) [verificato: board-vlan.txt] | [verificato: PRESENTAZIONE-CEO.md §12.1; prezzo di origine non verificato in ricerca/14 §6] |
| Backup in cloud (B2, 0,5 TB) | 3,10 | 0 | PBS a casa; S3 fuori sede solo se si vuole (§2.2) | [verificato: PRESENTAZIONE-CEO.md §12.1] |
| **Totale abbonamenti che spariscono** | **257,34** | **0** | | [non verificato: calcolo] |
| Google Workspace (era nel kit commerciale) | 54,40 | 0 | M365, già nel board per posta e identità [verificato: ricerca/25, C03] | [verificato: PRESENTAZIONE-CEO.md §12.1] |
| VM Azure (oggi accese) | risparmio di circa 150 | risparmio di almeno 150 | Escono tutte in F2. Il costo reale non è nei file | [non verificato: ricerca/14 §9, stima su una Standard_D4s_v5 in West Europe] |

### 2.2 Cosa resta o si aggiunge

| Voce | € al mese | Dettaglio | Etichetta |
|---|---|---|---|
| **API Anthropic** | ≈ 195,65 (forbice 90-250) | Stima per un motore con sessioni e cache. Coperta dai crediti finché durano (800 $ al mese, cioè 714,70 €, da confermare). Una parte delle domande alla memoria passa da Claude Team, quindi la stima può scendere | stima: [non verificato: ricerca/22 §6]; crediti: [non verificato: ricerca/14 §1.4]; Claude Team: [non verificato: ricerca/25 §5.1] |
| **Claude Team** | 0 nel primo anno; 446,70 a regime con 5 posti premium | Premium 100 $ a posto al mese con fatturazione annuale, 125 $ mensile; standard 20 $ / 25 $; da 2 a 150 posti. Con 4 premium: 357,36 €. Con 2 premium e 2 standard: 214,42 €. La pagina promette anche "Up to $500 per month in pooled API credits", con una nota non leggibile | prezzi: [verificato: https://claude.com/pricing/team, 25/10/2026]; anno gratis: [non verificato: ricerca/14 §1.4] |
| **Proxmox VE Community, 2 socket** | 20,00 | 120 € l'anno per socket, prezzi netti. La pagina mette Community sotto "For non-production use" e consiglia Basic, Standard o Premium per la produzione. Basic costa 370 € per socket, cioè 61,67 € al mese | [verificato: https://www.proxmox.com/en/products/proxmox-virtual-environment/pricing, 25/10/2026] |
| Proxmox Backup Server a casa | 0 (consigliato) | Senza abbonamento si usa il repository no-subscription. La documentazione scrive "It is not recommended to use it on production servers". Con Community: 560 € l'anno, cioè 46,67 € al mese | [verificato: https://www.proxmox.com/en/products/proxmox-backup-server/pricing; https://pbs.proxmox.com/docs/installation.html, 25/10/2026] |
| **Jira Standard × 4** | 28,27 (0 se il piano Free basta o se è già pagato) | Free fino a 10 utenti. Standard 7,91 $ a utente. `ricerca/29` consiglia Standard quando entrano gli account di servizio degli agenti con permessi diversi | prezzo: [non verificato: resolution.de e altri, risultati di ricerca del 25/10/2026]; consiglio: [verificato: ricerca/29 §4.3] |
| **IP fisso sulla linea FTTH** | 0-10 (uso 10 per prudenza) | Il board dice "IP fisso da richiedere". Alcune offerte business lo includono, altre lo vendono a 5-10 € al mese più IVA. L'operatore della linea non è nei file | richiesta: [verificato: board, "Rete fisica"]; prezzo: [non verificato: https://offerta-internet.it/partita-iva, letto tramite ricerca] |
| **Corrente del server e del firewall** | 105,27 prudente (79,72 al valore centrale) | Server a 400 W medi (102,20 €) più firewall a 12 W (3,07 €), a 0,35 €/kWh. Dettagli in §2.4 | [non verificato: stima] |
| **Numero e chiamate per Andrea** (dalla fase in cui parte) | 90,43 prudente; 44,24 se l'uso "illimitato" vale anche per un agente | Operatore italiano Messagenet, registro delle opposizioni, Claude per la chiamata e i riassunti. Dettagli in §2.3 | [non verificato: calcolo su prezzi verificati in §2.3] |
| **Instantly Hypergrowth, annuale** | 69,33 | 77,6 $ al mese con fatturazione annuale; 97 $ mensile (86,66 €) | [verificato: https://instantly.ai/pricing, 25/10/2026] |
| Teams, se non è già nel piano M365 | 0 se incluso; 5,72-14,29 se manca | Listino mondiale in dollari dal 01/11/2025: Business Basic 6,00 $ con Teams e 4,40 $ senza; Standard 12,50 $ e 9,29 $; Premium 22,00 $ e 18,79 $; Teams Essentials 4,00 $. Passare a un piano con Teams costa 1,60-3,21 $ a utente; Teams Essentials per 4 persone 14,29 € | listino: [verificato: https://www.microsoft.com/en-us/licensing/news/microsoft365-teams-2025, 25/10/2026]; calcolo: [non verificato] |
| Utente di servizio M365 per n8n (facoltativo) | 0; 6,41 se serve | Business Basic UK £5,40 secondo `ricerca/28`. Le fonti UK di oggi danno £5,33-5,60 dal 01/07/2026 | [non verificato: ricerca/28 §9; wavenet.co.uk e priority-it.co.uk letti tramite ricerca] |
| Registrazione del bot Teams | 0 | Bot "Teams-managed" senza sottoscrizione Azure; riserva Azure Bot F0 gratuita | [verificato: ricerca/28 §9] |
| S3 fuori sede (facoltativo) | 0; 6,21-6,49 per 1 TB | Backblaze B2: 6,95 $ per TB al mese (6,21 €), uscita gratis fino a 3 volte i dati salvati, chiamate API di classe A, B e C gratis. Hetzner Object Storage: 6,49 € al mese con 1 TB di spazio e 1 TB di traffico. Hetzner Storage Box 1 TB: 3,20 €, ma senza S3 (va bene per restic e Borg) | [verificato: https://www.backblaze.com/cloud-storage/pricing; https://www.hetzner.com/storage/object-storage/; https://www.hetzner.com/storage/storage-box/, 25/10/2026] |
| Corrente del Lenovo M920t a casa | meno di 1 | Acceso di notte da Home Assistant, circa 2 ore a 30 W | [non verificato: stima] |
| Telegram (facoltativo) e WhatsApp (più avanti) | 0; WhatsApp circa 7-12 per 300 messaggi utility | Non sono nel board: sarebbero eccezioni. Telegram Bot API gratuita. WhatsApp Cloud API: 1.000 messaggi di servizio gratis al mese per numero dal 01/10/2026 | [verificato: ricerca/28 §6 e §9; stima WhatsApp non verificata] |

### 2.3 Andrea: numero e chiamate

- **Cosa resta fuori per forza**: il numero di telefono e il trasporto delle chiamate. Voce, ascolto e logica possono girare sul server [verificato: ricerca/31, "In breve"].
- **Perché un operatore italiano**: dal 19/11/2025 gli operatori italiani bloccano le chiamate dall'estero che mostrano un numero italiano, salvo il roaming vero (delibera AGCOM 106/25/CONS). Un trunk estero con un numero italiano rischia il blocco [verificato: ricerca/31 §4.1, su fonti secondarie; la conseguenza è non verificata].
- **Messagenet, prezzi del 25/10/2026**:
  - SmartNumber PRO per 2-4 colleghi: **30 € al mese IVA esclusa**, 2 canali, fissi e mobili illimitati "a condizioni di uso lecito e corretto". Con 1 canale: 15 € (fissi illimitati, 1.000 minuti verso mobili). Con 3 canali: 45 € [verificato: https://www.messagenet.com/voip/].
  - SmartNumber a consumo: 36,60 € l'anno IVA inclusa (2,50 € al mese netti), attivazione 8,54 € IVA inclusa (7,00 € netti) [verificato: idem].
  - Tariffe a consumo: mobili 0,0944 €/min e fissi 0,0189 €/min, "Prezzi IVA 22% inclusa", al secondo, senza scatto. Al netto: 0,0774 € e 0,0155 € [verificato: https://www.messagenet.com/tariffe/; netto: non verificato, calcolo].
- **Calcolo per 1.000 minuti al mese** (90 % verso mobili, 2 numeri), stessa ipotesi di `ricerca/14` §3.4 e `ricerca/31` §12:

| Voce | A consumo (prudente) | PRO 2 canali (se l'illimitato vale per un agente) | Etichetta |
|---|---|---|---|
| Operatore e numeri | 76,19 (2 numeri 5,00 + 900 min × 0,0774 + 100 min × 0,0155) | 30,00 | [non verificato: calcolo su prezzi verificati] |
| Registro pubblico delle opposizioni | 7,67 (92 € l'anno) | 7,67 | importo: [non verificato: ricerca/31 §12, tariffa 2024]; nel 2026 valgono le tariffe del DM 20/12/2024 prorogate [verificato: avviso MIMIT del 23/12/2025, https://www.mimit.gov.it/images/stories/normativa/AVVISO_del_23_dicembre_2025_Registro_Pubblico_delle_Opposizioni_Costi_e_tariffe.pdf] |
| Claude Haiku 5.5 in chiamata | 1,88 (2,10 $) | 1,88 | [verificato: ricerca/14 §3.4] |
| Claude Sonnet 5.5 per riassunti e analisi | 4,69 (5,25 $) | 4,69 | [non verificato: stima di ricerca/31 §12] |
| **Totale** | **90,43** | **44,24** | [non verificato: calcolo] |

- **Prima** la voce valeva circa 170,28 € al mese: ElevenLabs Pro 88,45, numero Twilio 40,20, chiamate e modello 41,63 [verificato: PRESENTAZIONE-CEO.md §12.1].
- **Twilio per confronto** (prezzi "current as of August 2026"):
  - Programmable Voice verso mobili italiani: 0,0445 $ con origine nello Spazio economico europeo, 0,3473 $ con l'origine di default [verificato: https://www.twilio.com/en-us/voice/pricing/it].
  - SIP trunking verso mobili italiani: 0,0405 $ con origine SEE, 0,0436 $ da USA o Canada, 0,3433 $ di default; numero mobile italiano 45 $ al mese [verificato: https://www.twilio.com/en-us/sip-trunking/pricing/it].
  - Con la tariffa SEE, 1.000 minuti costano circa 36-40 €; con quella di default circa 307-310 € [non verificato: calcolo]. Twilio è un servizio USA fuori dal board, e resta il rischio di blocco del numero chiamante [non verificato: ricerca/31 §4.1].
- **Corrente**: Andrea su CPU aggiunge 2-3 € al mese [non verificato: ricerca/31 §12]. È già dentro la stima prudente del server a 400 W.
- **Due verifiche prima di firmare**: se l'uso "illimitato" ammette le chiamate fatte da un agente automatico; e chi firma, visto che Sersan Limited è inglese e il team è in Sardegna [verificato: ricerca/31 §4.2].

### 2.4 Corrente

| Dato | Valore | Etichetta |
|---|---|---|
| Indice Selectra di ottobre 2026 (all'ingrosso più perdite, spread, oneri e trasporto variabili, IVA) | media mensile 0,384 €/kWh al 21/10/2026; 0,421 €/kWh il 21/10. La pagina non dice l'aliquota IVA né se vale per famiglie o imprese | [verificato: https://selectra.net/energia/attualita/mercato/pun-psv-21-ottobre-2026] |
| Lo stesso valore senza IVA | circa 0,349 €/kWh con IVA al 10 %; circa 0,315 €/kWh con IVA al 22 % | [non verificato: calcolo] |
| Prezzo usato in questo rapporto | **0,35 €/kWh**, forbice 0,30-0,40 | [non verificato: ipotesi, come ricerca/14 §8.1] |
| DL380 Gen10 con 2 Xeon Platinum 8180, SPECpower 2018 | 49,3 W in "active idle", circa 461 W a pieno carico | [verificato: ricerca/15 §3, da spec.org] |
| Quadro RTX 4000 | fino a 160 W | [verificato: ricerca/15 §2.3] |
| Seconda GPU da 70 W (A2000, RTX 2000 Ada, RTX PRO 2000) | 70 W | [verificato: pagine gpuprix citate in §4.2, 25/10/2026] |
| **Stima per la configurazione del board** (2 CPU, 12 moduli RAM, 6 HDD SAS, 2 SSD, GPU di giorno all'AI e di sera alla VM Experimental-1, ventole performance) | **200-400 W medi, valore centrale 300 W** | [non verificato: stima] |

| Media 24/7 | kWh al mese (× 730 h) | a 0,30 €/kWh | **a 0,35 €/kWh** | a 0,40 €/kWh |
|---|---|---|---|---|
| 200 W | 146,0 | 43,80 | **51,10** | 58,40 |
| 300 W | 219,0 | 65,70 | **76,65** | 87,60 |
| 400 W | 292,0 | 87,60 | **102,20** | 116,80 |
| 450 W | 328,5 | 98,55 | **114,98** | 131,40 |
| Firewall OPNsense, 12 W | 8,8 | 2,63 | **3,07** | 3,50 |
| Seconda GPU in F5, 25-70 W medi | 18,3-51,1 | 5,48-15,33 | **6,39-17,89** | 7,30-20,44 |

Tutte le cifre della tabella: [non verificato: calcolo sulle ipotesi sopra].

- Nei totali uso **400 W** (102,20 €), lo stesso valore della presentazione, così i numeri si confrontano. Ci aggiungo il firewall (3,07 €).
- Una parte del consumo serve ai laboratori (Experimental-1 e 2) e alla VLAN personale, non agli agenti [verificato: board, tabella "RAM · 192GB"]. Chi paga quella parte è una scelta interna.
- Il numero vero si legge dall'iLO dopo le prove di carico [verificato: ricerca/15 §7, passo 4].
- Il rack sta in un "salotto" [verificato: board, sezione "Rete fisica"]. Se il contratto della luce è domestico, il prezzo ha l'IVA al 10 % e l'IVA non si recupera [non verificato].

### 2.5 Strumenti commerciali e di marketing

Il board cita solo **Instantly**. Gli altri strumenti del kit commerciale non compaiono [verificato: board, "Cloud & SaaS che restano"]. Ecco cosa risulta da `ricerca/14` (prezzi del 24/10/2026).

| Strumento | Cosa risulta da ricerca/14 | € al mese nel consigliato di prima | Nel board | Cosa c'è sul server al suo posto |
|---|---|---|---|---|
| **Instantly** | Growth 47 $ mensile, 37,60 $ annuale; Hypergrowth 97 $ / 77,60 $; Light Speed 358 $ / 286,30 $. Oggi confermati sulla pagina ufficiale. La pagina ha però delle incongruenze: una scheda "Hypergrowth" mostra 358 $, e il limite di Hypergrowth è 125.000 mail in una tabella e 100.000 in un'altra | 69,33 | **sì** | resta |
| Apollo | Basic 49 $ a posto annuale (59-65 $ mensile); Professional 79 $ / 99 $; Organization 119 $ con almeno 3 posti [non verificato in ricerca/14 §6] | 43,78 | no | mcp-enrich, copertura da verificare [non verificato] |
| Apify | Free 0 $; Starter 19 $ / 17 $; Scale 199 $ / 179 $; Business 999 $ / 899 $ [verificato in ricerca/14 §6: https://apify.com/pricing] | 15,19 | no | Firecrawl self-hosted [verificato: board-vlan.txt] |
| Metricool | Starter 25 $ / 20 $; Advanced 67 $, da cui parte l'approvazione [non verificato in ricerca/14 §7]. Oggi pubblica Pagina LinkedIn, Instagram e Facebook [verificato: ricerca/05] | 59,86 | no | nessuno nel board |
| moda.app | Free 0 $; Pro 30 $ a utente; Ultra 100 $ a utente [verificato in ricerca/14 §6: https://moda.app/pricing] | 26,80 | no | nessuno nel board |
| Higgsfield | Fonti in contrasto: Plus 59 $ / 47 $, Ultra 129 $ / 99 $, oppure Basic 9 $, Pro 29 $, Max 79 $ [non verificato in ricerca/14 §6]. Alberto usa un Ultra personale [verificato: ricerca/05] | 41,99 | no | nessuno nel board |
| Google Workspace | Business Starter 6,80 €; Business Standard 13,60 € a utente [non verificato in ricerca/14 §5] | 54,40 | no: posta e identità sono su M365 | M365 |

- Prezzi di Instantly: [verificato: https://instantly.ai/pricing, 25/10/2026]. Il costo che SerSan paga oggi per Instantly non è nei file [verificato: ricerca/01 §3.4].
- **Se il board si applica alla lettera**, il kit costa 69,33 € al mese invece di 311,35 € [non verificato: calcolo].
- **Se Apollo, Apify, Metricool, moda.app e Higgsfield restano**, si aggiungono 187,62 € al mese [non verificato: calcolo]. Sono servizi in cloud: tenerli richiede un'eccezione al "tutto self-hosted" di Michele, da decidere con lui e con Alessandro.
- **Google Workspace** sembra non servire più, perché il board mette posta e identità su M365 [verificato: ricerca/25, C03]. Va confermato che SerSan non paghi entrambe le suite.

### 2.6 Hermes o Agent SDK: cosa cambia nei costi

- **Agent SDK**: libreria senza canone; si paga l'uso dell'API. Gli agenti usano la chiave API, mai i posti di Claude Team [verificato: ricerca/26, "In breve" punto 5 e §5]. Quindi la riga API serve in ogni caso.
- **Hermes self-hosted**: licenza MIT, gira sul DL380 senza Hermes Cloud, senza Nous Portal e senza account Nous [verificato: ricerca/27, "In breve"]. Hermes Cloud esce comunque con il perimetro del board.
- **La stima API vale per entrambi**: è stata fatta per un motore con sessioni e cache [verificato: ricerca/22 §6, formula].
- **La differenza è di lavoro, non di canone**: Hermes chiede 26-33 gp di integrazione più 1,5-2,5 gp al mese di manutenzione; il motore sull'SDK circa 27 gp con la riserva [non verificato: stime di ricerca/27 §10 e ricerca/26 "In breve"].
- **LiteLLM**: budget per chiave, squadra, utente e cliente, con PostgreSQL [verificato: ricerca/26 §4.3]. Nessun costo di licenza nei totali.
- **Limiti Anthropic**: il livello Start ha un tetto di spesa di 500 $ al mese, Build 1.000 $, Scale 200.000 $. I livelli salgono in automatico con lo storico d'uso, oppure su richiesta dalla Console; la pagina non chiede depositi [verificato: https://platform.claude.com/docs/en/api/rate-limits, 25/10/2026]. Il consigliato (circa 219 $) sta sotto il tetto Start; il completo (circa 545 $) richiede il livello Build [non verificato: calcolo].

### 2.7 Licenze dei componenti self-hosted

- Nei totali conto **0 €** per i componenti open source del board [non verificato: non ho controllato tutte le licenze].
- **NetBird**: il server self-hosted è AGPL-3.0 dalla versione 0.53.0 (agosto 2025), senza limiti di utenti nella Community Edition. La licenza commerciale serve per alta affidabilità, SCIM e log dei flussi: circa 2.000 € l'anno fino a 50 utenti, a luglio 2026 [non verificato: wz-it.com e docs.netbird.io/selfhosted/enterprise, letti tramite ricerca]. Il piano cloud Free costa 0 € fino a 5 utenti [verificato: https://netbird.io/pricing]. Per 4 persone basta la Community Edition [non verificato].
- **Pangolin**: la Community Edition è AGPL-3.0 e gratuita. L'Enterprise Edition è gratuita sotto i 100.000 $ di fatturato lordo annuo, con una chiave di licenza [non verificato: docs.pangolin.net/self-host/enterprise-edition, letto tramite ricerca]. La pagina prezzi mostra solo i piani cloud: Basic gratis, Team 4 $ e Business 9 $ a utente [verificato: https://pangolin.net/pricing].
- **MinIO**: più fonti dicono che la Community Edition è in sola manutenzione da dicembre 2025, senza immagini Docker né binari da ottobre 2025, e che il repository non è più mantenuto dal 2026. Il prodotto a pagamento, AIStor, parte da cifre a cinque zeri l'anno [non verificato: linuxiac.com, itsfoss.com, blog.elest.io, letti tramite ricerca]. Con la regola Cyber Essentials del "software supportato" MinIO va probabilmente sostituito con un'alternativa gratuita (per esempio Garage o SeaweedFS). Costo di licenza atteso: 0 € [non verificato].
- **Open WebUI**: dalla v0.6.6 la licenza chiede di lasciare visibile il marchio, salvo installazioni fino a 50 utenti in 30 giorni [non verificato: docs.openwebui.com/license, letto tramite ricerca]. Nessun costo.
- **n8n**: è sotto Sustainable Use License, che di norma ammette l'uso interno gratuito [non verificato: pagina della licenza non trovata il 25/10/2026]. Va controllato prima della produzione.

### 2.8 Servizi in cloud che restano e sono già in uso

M365 / Entra ID, Cloudflare, GitHub, Supabase, Vercel e Jira restano [verificato: board]. Sono costi dell'azienda di oggi, non nuovi per il progetto, e i loro importi non sono nei file [verificato: ricerca/14 §12]. Faccio due eccezioni: Jira Standard, che può servire per gli agenti (§2.2), e Teams, solo se oggi manca dal piano M365. I runner GitHub in casa possono ridurre i minuti di Actions a pagamento [non verificato].

---

## 3. Totali mensili

### 3.1 Quanto spendiamo in più rispetto a oggi, fase per fase

Conto come la prima tabella della presentazione (§12.1): costi nuovi, **senza il kit commerciale**, con le API dentro i crediti e Claude Team gratuito nel primo anno. Le fasi sono quelle del board.

| Periodo | € al mese in più | Cosa comprende | Prima (PCEO §12.1) |
|---|---|---|---|
| F0-F1, Azure ancora accesa | **≈ 135,27** | Proxmox 20,00 + IP fisso 10,00 + corrente 105,27 | ≈ 300 (settimane 1-8) |
| F2-F3, Azure spenta | **≈ −14,73** | come sopra, meno circa 150 di Azure: si spende meno di oggi | ≈ 140 (settimane 14-16) |
| F4, agenti al lavoro | **≈ 13,54** | più Jira Standard 28,27 | |
| Con Andrea | **≈ 103,97** (≈ 57,78 con il piano PRO) | più 90,43 (o 44,24) | ≈ 310 (dalla settimana 17) |
| Fine dell'anno gratuito di Claude Team | **≈ 550,67** | più 446,70 (5 premium); ≈ 461,33 con 4 premium; ≈ 318,39 con 2 premium e 2 standard | fino a ≈ 757 |
| Anche senza crediti API | **≈ 746,32** | più 195,65 di API | |
| Instantly, se oggi non è già pagato | **+ 69,33** a ogni riga | | il kit era fuori da questa tabella |

Tutte le cifre: [non verificato: calcolo sulle voci di §2]. Il riferimento "prima": [verificato: PRESENTAZIONE-CEO.md §12.1].

### 3.2 I tre scenari

Gli scenari sono gli stessi della presentazione: minimo (niente voce, piani gratuiti), consigliato (60 call e 300 lead al mese), completo (volumi pieni, 3.000 minuti di voce) [verificato: PRESENTAZIONE-CEO.md §12.2].

| € al mese | Minimo | Consigliato | Completo |
|---|---|---|---|
| Nuovo per il progetto | 0 (Proxmox senza abbonamento, Jira Free, IP già incluso) | 58,27 (Proxmox Community 20,00; Jira Standard 28,27; IP fisso 10,00) | 180,27 (Proxmox Basic 61,67; PBS Community 46,67; Jira Standard 28,27; Teams Essentials 14,29; utente di servizio 6,41; S3 2 TB su Hetzner 12,96; IP fisso 10,00) |
| API Anthropic | 54,70 | 195,65 | 486,90 |
| Server: corrente e firewall | 79,72 (300 W) | 105,27 (400 W) | 118,05 (450 W) |
| Andrea | 0 | 90,43 (1.000 minuti a consumo) | 267,11 (3.000 minuti a consumo, Sonnet con cache) |
| Strumenti commerciali del board (Instantly) | 33,59 (Growth) | 69,33 (Hypergrowth) | 255,78 (Light Speed) |
| **Totale di listino** | **168,01** | **518,95** | **1.308,11** |
| Esborso con bundle e crediti, Azure accesa | 113,31 | 323,30 | 821,21 |
| **Esborso dopo lo spegnimento di Azure** | **−36,69** | **173,30** | **671,21** |
| Finito l'anno gratuito di Claude Team, crediti ancora attivi | 410,01 | 620,00 | 1.117,91 |
| Senza bundle né crediti API | 464,71 | 815,65 | 1.604,81 |
| *Prima (PCEO §12.2): totale di listino* | *301* | *968* | *2.250* |
| *Prima: esborso dopo lo spegnimento di Azure* | *97* | *623* | *1.613* |
| *Prima: senza bundle né crediti* | *598* | *1.265* | *2.547* |

- Tutte le cifre nuove: [non verificato: calcolo]. Le API del minimo e del completo vengono da [non verificato: ricerca/22 §6]. Le cifre "prima": [verificato: PRESENTAZIONE-CEO.md §12.2].
- Andrea nel completo: 2 numeri 5,00 + 2.700 min × 0,0774 + 300 min × 0,0155 = 218,57; più registro 7,67, modello in chiamata 26,80 (30 $, come ricerca/14 §11.2) e riassunti 14,07. Con il piano PRO a 3 canali scenderebbe a circa 93,54 € [non verificato: calcolo].
- Nel minimo l'esborso è negativo: spegnere Azure fa risparmiare più di quanto costa il progetto.
- **Variante strumenti commerciali**: se restano Apollo, Apify, Metricool, moda.app e Higgsfield, il consigliato sale di 187,62 €: listino 706,57 €, esborso dopo Azure 360,92 €, a regime 1.003,27 € [non verificato: calcolo].
- **Andrea con il piano PRO a 2 canali**: il consigliato scende di 46,19 €, a 472,76 € di listino [non verificato: calcolo].
- **Voci facoltative fuori dal consigliato**: S3 fuori sede (6,21-6,49 € per TB), Teams se manca (5,72-14,29 €), utente di servizio M365 (6,41 €), PBS Community (46,67 €), Proxmox Basic invece di Community (+41,67 €), corrente della seconda GPU in F5 (6,39-17,89 €), WhatsApp più avanti (circa 7-12 €).
- **Voci invariate, fuori dai totali come prima**: il premio mensile per chi costruisce con l'AI (50-100 €), la revisione di sicurezza esterna nella fase 5 e gli strumenti della fase 6, a preventivo [verificato: PRESENTAZIONE-CEO.md §14, decisioni 15, 16 e 20].

### 3.3 Il ponte dalla proposta precedente (consigliato)

| Gruppo | Prima | Ora | Differenza |
|---|---|---|---|
| Nuovo per il progetto | 188,89 | 58,27 | −130,62 (escono 8 abbonamenti; entrano Jira Standard e IP fisso) |
| API Anthropic | 195,65 | 195,65 | 0 |
| Server | 102,20 | 105,27 | +3,07 (ora conto anche il firewall) |
| Andrea | 170,28 | 90,43 | −79,85 (escono ElevenLabs e Twilio; entra un operatore italiano) |
| Kit commerciale | 311,35 | 69,33 | −242,02 (Google Workspace −54,40; strumenti non citati −187,62) |
| **Totale** | **968,37** | **518,95** | **−449,42** |

Fonte del "prima": [verificato: PRESENTAZIONE-CEO.md §12.1 e ricerca/22 §6]; il resto: [non verificato: calcolo].

---

## 4. Costi una tantum

### 4.1 Subito (fasi F0-F1)

| Voce | Importo IVA esclusa | Dettaglio | Etichetta |
|---|---|---|---|
| Lenovo M920t ricondizionato | 152-294 € (186-359 € con IVA) | i5-8500: da 8 GB e 256 GB SSD (refurbed.it, 185,99 €) fino a 32 GB con un HDD da 2 TB (eBay, 359 €) | [non verificato: refurbed.it, pccomponentes.it, ebay.de/itm/226965262318, prezzi letti tramite ricerca il 25/10/2026; la pagina refurbed.it oggi dà il modello esaurito] |
| 2 HDD SATA da 4 TB in mirror per il PBS | 230-436 € (115-218 € l'uno) | WD Red Plus 4 TB: un negozio tedesco lo mostra a 258,90 € con IVA (217,56 € netti); i dischi sono saliti di prezzo nel 2026. Lenovo indica per i vani da 3,5" dischi "up to 2TB each": dischi più grandi di solito funzionano, ma sono fuori elenco | prezzi: [non verificato: coolblue.de e techradar.com, letti tramite ricerca]; limite Lenovo: [verificato: https://psref.lenovo.com/syspool/Sys/PDF/ThinkCentre/ThinkCentre_M920_Tower/ThinkCentre_M920_Tower_Spec.html] |
| **Backup a casa, totale** | **382-730 €** | La misura dei dischi dipende da quanti dati vanno salvati: è una domanda aperta | [non verificato: calcolo] |
| Chiavi FIDO2 per NetBird ed Entra (2 a persona, 8 chiavi) | 232-464 € (232 € con Security Key NFC, 464 € con YubiKey 5 NFC) | 35,38 € e 70,76 € l'una con IVA sullo store italiano di Yubico, cioè 29,00 € e 58,00 € netti. Voce che nasce dal board | prezzi: [verificato: https://www.yubico.com/it/store/, 25/10/2026]; richiesta: [verificato: board, "NetBird mesh"] |
| Piccoli accessori (guide, coperture degli slot, cavi), se mancano | 0-200 € | Michele dice che ventole, dissipatori e alimentatori ci sono già | [non verificato: stima di ricerca/25 §5.3] |
| Parere legale unico | tetto 2.500 € | Invariato. L'elenco dei temi cambia: esce Recall.ai; entrano i documenti e i dati fiscali che l'MCP RAG passa a Claude Team, la lettura delle trascrizioni di Teams, i metadati di M365, la voce di Andrea e il registro delle opposizioni che risponde entro 24 ore | tetto: [verificato: PRESENTAZIONE-CEO.md §14, decisione 10]; temi: [verificato: ricerca/25, S9-05; ricerca/31, "In breve" punto 5] |
| Credito API prepagato, se i crediti del bundle finiscono | 0-223 € | Non è un deposito per salire di livello: la pagina dei limiti di oggi non ne parla. È un anticipo sull'uso del mese. I 250 $ di prima venivano da un sistema di livelli più vecchio | [verificato: https://platform.claude.com/docs/en/api/rate-limits; ricerca/01 §3.4] |
| Attivazione del numero di Andrea | 7-14 € | Quando parte Andrea | [verificato: https://www.messagenet.com/voip/, 8,54 € con IVA a numero] |
| Pagamento del server ("Pagare Bargain" in F0) | non nei file | | [verificato: board, roadmap F0] |
| **Subtotale subito** | **≈ 3.114-4.117 €**, più il server | Prima: fino a 5.016 € (UPS 1.293, accessori 1.000, deposito 223, legale 2.500) | ora: [non verificato: calcolo]; prima: [verificato: ricerca/25 §5.3 e PRESENTAZIONE-CEO.md §12.3] |

### 4.2 Più avanti (fase F5)

| Voce | Importo IVA esclusa | Dettaglio | Etichetta |
|---|---|---|---|
| **Seconda GPU, fissa sull'AI** | **686-893 €** (consigliata da 16 GB); 496 € per la A2000 da 6 GB | La "A2000 con chip Ada da 6 GB GDDR7" del messaggio di Michele non esiste. RTX A2000 6 GB GDDR6, 70 W: 605 € con IVA (≈ 496 € netti). RTX 2000 Ada 16 GB GDDR6, 70 W: 837 € (≈ 686 €). RTX PRO 2000 Blackwell 16 GB GDDR7, 70 W: 1.090 € (≈ 893 €). I rapporti 30 e 31 consigliano 16 GB: ci stanno Andrea e tutta la pipeline RAG, e la RTX 4000 resta libera per Experimental-1 | prezzi minimi in Italia aggiornati al 24/10/2026, letti il 25/10/2026: [verificato: https://gpuprix.com/italy/gpus/rtx-a2000-6gb, https://gpuprix.com/italy/gpus/rtx-2000-ada-generation, https://gpuprix.com/italy/gpus/rtx-pro-2000-blackwell]; IVA inclusa nei prezzi: [non verificato]; consiglio: [verificato: ricerca/30 e ricerca/31 §8.3] |
| **UPS rack 2U** (APC SMT1500 o Eaton 5PX) | **1.011-1.060 €** | Eaton 5PX1500IRT2UG2: 1.212,17 € con IVA tedesca (≈ 1.018,63 € netti), in magazzino. APC SMT1500RMI2UC: 1.011,42 € IVA esclusa su it-partners; 1.292,99 € con IVA su Yeppon (≈ 1.059,83 € netti) | Eaton: [verificato: https://www.office-partner.de/eaton-5px-1500i-rt2u-g2-n2000000709, 25/10/2026]; APC: [non verificato: it-partners.it e yeppon.it letti tramite ricerca] |
| RAM in più (facoltativa) | 0; +4 moduli ≈ 160-400 €; +12 moduli ≈ 480-1.200 € | Con 2 CPU le configurazioni bilanciate sono 6+6, 8+8 e 12+12 moduli. Se i 192 GB sono 12 moduli da 16 GB, +4 moduli portano a 256 GB e +12 a 384 GB. Moduli usati da 16 GB: circa 40-100 € netti l'uno; un modulo HPE nuovo costa circa 357 €. Il board lascia già circa 53 GB liberi | bilanciamento: [verificato: ricerca/15 §2.2]; 53 GB liberi: [verificato: board]; prezzi: [non verificato: amcompute.com, ebay.de, store.inetum.be letti tramite ricerca]; composizione dei 192 GB: [non verificato] |
| **Subtotale più avanti** | **≈ 1.697-2.353 €** (GPU da 16 GB, UPS, fino a 4 moduli RAM) | Con la A2000 da 6 GB e senza RAM: circa 1.507 €. Con 12 moduli RAM: fino a circa 3.153 € | [non verificato: calcolo] |

**Totale una tantum**: circa **4.811-6.470 €**, più il pagamento del server [non verificato: calcolo]. In più, già speso prima del board: 1.241,49 € di hardware (GPU, RAM, controller, cavo, rack, mini PC) [verificato: ricerca/22 §7].

### 4.3 Cosa esce dalle una tantum della proposta precedente

| Voce di prima | Importo di prima | Perché esce | Etichetta |
|---|---|---|---|
| Kit ventole e dissipatori HPE, cavo GPU, 2 alimentatori da 800 W, dischi | tetto 1.000 € | Ci sono già; resta solo una piccola riserva per accessori (§4.1) | [verificato: messaggio di Michele del 25/10/2026] |
| 2 moduli RAM per bilanciare | ≈ 138 € | I 192 GB ci sono già | [verificato: idem] |
| Aggiornamento GPU | 2.438-2.555 € | Sostituito da una seconda GPU più piccola in F5 | [verificato: board, roadmap F5] |
| UPS 1.500 VA "obbligatorio subito" | 1.163-1.293 € | C'è già un UPS collegato al firewall con NUT; quello rack arriva in F5 | [verificato: board, "UPS attuale → NUT"] |
| Prova di Grok Bot per un mese | ≈ 54 € | È un servizio in cloud, fuori dal perimetro | [verificato: PRESENTAZIONE-CEO.md §14, decisione 17] |

**Correzione sull'UPS**: i 1.163-1.293 € dei rapporti precedenti erano con ogni probabilità prezzi **con IVA**. Yeppon mostra 1.292,99 € come prezzo pieno, e lo stesso modello costa 1.011,42 € IVA esclusa su un altro negozio [non verificato: stesse fonti di §4.2].

### 4.4 Voci del board che non sono del progetto agenti

Le scrivo perché i CEO le vedranno nel board, ma non entrano nei totali.

| Voce | Costo | Etichetta |
|---|---|---|
| Certificazione Cyber Essentials (il board lavora "dentro il perimetro") | £320-450 più IVA l'anno, cioè circa 380-534 € l'anno; Plus circa £1.350-1.500 | [non verificato: Wikipedia e forensiccontrol.com letti tramite ricerca; cambio di ricerca/28] |
| Licenze Windows per Experimental-1 e per il bridge MT (VLAN 60) | non nei file | [verificato: board-vlan.txt elenca le due macchine Windows] |
| Minecraft (VLAN 99, fuori perimetro) e server di casa i7 6700K | 0 € di licenza; quota di corrente | [verificato: board, "Minecraft fuori perimetro" e "Sede 2 · casa"] |
| Nodo 2 (2027-2028) | non nei file | [verificato: board, roadmap F5] |

---

## 5. Cosa può spostare i numeri

| Rischio | Effetto | Come lo chiudiamo |
|---|---|---|
| Corrente vera del server | 44-117 € al mese tra 200 e 400 W e tra 0,30 e 0,40 €/kWh | Misura dall'iLO dopo le prove di carico |
| L'uso "illimitato" di Messagenet non vale per un agente | Andrea passa da 44,24 € a 90,43 € al mese (a 1.000 minuti) | Leggere le condizioni d'uso o chiedere a Messagenet prima di firmare |
| Operatore estero per Andrea | blocco delle chiamate con numero italiano; con Twilio a tariffa di default circa 307-310 € per 1.000 minuti | Operatore italiano (§2.3) |
| Crediti API non confermati (800 $ al mese, 1.000 $ una tantum o 500 $ in comune) | fino a 195,65 € al mese in più nel consigliato | Verifica nella Claude Console |
| Piano M365 senza Teams | 5,72-14,29 € al mese in più | Controllo nel centro di amministrazione M365 |
| Jira già a pagamento, oppure Free sufficiente | −28,27 € al mese | Chiedere a Michele il piano di oggi |
| Strumenti commerciali non citati dal board | +187,62 € al mese se restano | Decisione con Michele e Alessandro |
| MinIO non più mantenuto | lavoro per sostituirlo; licenza a pagamento se si resta su MinIO | Scelta di Michele (Garage, SeaweedFS o altro) |
| Abbonamento Proxmox per la produzione | da 20,00 € (Community) a 61,67 € (Basic), più 46,67 € per il PBS | Scelta di Michele |
| Prezzi di RAM e dischi in salita nel 2026 | le forbici di §4 possono allargarsi | Preventivi prima dell'ordine |
| Qualità della voce locale in italiano | se non basta, torna un servizio in cloud | Prova su CPU prima della fase di Andrea |

---

## 6. Cosa cambia rispetto alla prima stesura di oggi

- **Andrea**: ora usa un operatore italiano, come `ricerca/31`, per la regola AGCOM contro i numeri italiani chiamati dall'estero. La voce vale 44-90 € invece di 82 € con Twilio.
- **Twilio SIP trunking**: la tariffa verso i mobili italiani con origine SEE è 0,0405 $, non 0,3433 $. Quest'ultima è la tariffa di default [verificato: https://www.twilio.com/en-us/sip-trunking/pricing/it].
- **Jira Standard e IP fisso** entrano nel consigliato con valori prudenti (§2.2).
- **Le fasi** si confrontano con la presentazione senza il kit commerciale, come nella sua prima tabella (§3.1). Instantly è una riga a parte.
- **MinIO, NetBird e Pangolin**: aggiunte le note sulle licenze (§2.7).
- **Dischi del PBS**: forbice più alta, per i prezzi saliti nel 2026 (§4.1).

---

## 7. Domande aperte

1. Quale piano M365 ha SerSan, con quanti posti, e include Teams? Sersan Limited compra M365 nel Regno Unito o in Italia?
2. Jira oggi è Free o Standard? Gli account di servizio degli agenti richiedono Standard?
3. Quale seconda GPU intende Michele: A2000 6 GB, RTX 2000 Ada 16 GB o RTX PRO 2000 Blackwell 16 GB GDDR7?
4. Come sono composti i 192 GB (12 moduli da 16 GB?), e a che velocità girano?
5. Quanto costa e quando si paga il server ("Pagare Bargain")?
6. Chi è l'operatore della linea FTTH, e quanto costa l'IP fisso?
7. Il contratto della luce del locale con il rack è aziendale o domestico? Chi paga la corrente del PBS a casa?
8. Quali strumenti commerciali restano: Apollo, Apify, Metricool, moda.app, Higgsfield? SerSan paga oggi anche Google Workspace?
9. Instantly è già pagato oggi, e con quale piano?
10. Crediti API e anno gratuito di Claude Team: importo e scadenza nella Claude Console. I "fino a 500 $ al mese di crediti pooled" del piano Team si sommano?
11. Messagenet ammette le chiamate fatte da un agente dentro l'offerta "illimitata"? Chi firma il contratto per Sersan Limited?
12. Quanti dati vanno salvati nel PBS a casa, e quindi quanto grandi devono essere i due dischi? Serve davvero anche l'S3 fuori sede?
13. Con MinIO non più mantenuto, quale archivio S3 usiamo sul server?
14. Lo SKU e il costo reale delle VM Azure di oggi: quante sono e quanto costano?

---

## Fonti

**Pagine ufficiali lette il 25/10/2026**

- Proxmox VE, prezzi: https://www.proxmox.com/en/products/proxmox-virtual-environment/pricing
- Proxmox Backup Server, prezzi: https://www.proxmox.com/en/products/proxmox-backup-server/pricing
- Proxmox Backup Server, repository: https://pbs.proxmox.com/docs/installation.html
- Claude Team, prezzi: https://claude.com/pricing/team
- Anthropic, limiti e livelli: https://platform.claude.com/docs/en/api/rate-limits
- Instantly: https://instantly.ai/pricing
- Twilio Voice Italia: https://www.twilio.com/en-us/voice/pricing/it
- Twilio SIP trunking Italia: https://www.twilio.com/en-us/sip-trunking/pricing/it
- Messagenet, offerte VoIP: https://www.messagenet.com/voip/
- Messagenet, tariffe: https://www.messagenet.com/tariffe/
- MIMIT, avviso del 23/12/2025 sulle tariffe del Registro delle opposizioni: https://www.mimit.gov.it/images/stories/normativa/AVVISO_del_23_dicembre_2025_Registro_Pubblico_delle_Opposizioni_Costi_e_tariffe.pdf
- Microsoft, piani con e senza Teams (dal 01/11/2025): https://www.microsoft.com/en-us/licensing/news/microsoft365-teams-2025
- Backblaze B2: https://www.backblaze.com/cloud-storage/pricing
- Hetzner Object Storage: https://www.hetzner.com/storage/object-storage/
- Hetzner Storage Box: https://www.hetzner.com/storage/storage-box/
- Yubico store Italia: https://www.yubico.com/it/store/
- Lenovo PSREF, ThinkCentre M920 Tower: https://psref.lenovo.com/syspool/Sys/PDF/ThinkCentre/ThinkCentre_M920_Tower/ThinkCentre_M920_Tower_Spec.html
- NetBird, prezzi: https://netbird.io/pricing
- Pangolin, prezzi: https://pangolin.net/pricing
- Selectra, prezzi dell'energia del 21/10/2026: https://selectra.net/energia/attualita/mercato/pun-psv-21-ottobre-2026

**Negozi e tracker di prezzi letti il 25/10/2026**

- gpuprix, RTX A2000 6 GB: https://gpuprix.com/italy/gpus/rtx-a2000-6gb
- gpuprix, RTX 2000 Ada: https://gpuprix.com/italy/gpus/rtx-2000-ada-generation
- gpuprix, RTX PRO 2000 Blackwell: https://gpuprix.com/italy/gpus/rtx-pro-2000-blackwell
- Office-Partner, Eaton 5PX 1500i RT2U G2: https://www.office-partner.de/eaton-5px-1500i-rt2u-g2-n2000000709

**Fonti terze, lette tramite risultati di ricerca il 25/10/2026** (tutte [non verificato])

- it-partners, APC SMT1500RMI2UC: https://it-partners.it/en/products/apc-smt1500rmi2uc-gruppo-di-continuita-ups-a-linea-interattiva-1-5-kva-1000-w-4-presa-e-ac-smt1500rmi2uc
- Yeppon, APC Smart-UPS 1500: https://www.yeppon.it/collections/smart-ups-1500va-lcd
- Refurbed, Lenovo M920t: https://www.refurbed.it/en-it/p/lenovo-thinkcentre-m920t-tower
- PcComponentes, Lenovo M920t: https://www.pccomponentes.it/ssd-lenovo-thinkcentre-m920t-intel-core-i5-8500-8-gb-256-gb
- eBay, Lenovo M920t: https://www.ebay.de/itm/226965262318
- Coolblue, WD Red Plus 4 TB: https://www.coolblue.de/produkt/920990/wd-red-plus-wd40efpx-4-tb.html
- TechRadar, prezzi dei dischi in salita: https://techradar.com/pro/wd-red-plus-4tb-internal-nas-hdd-review
- amcompute, RAM DDR4 RDIMM usata: https://www.amcompute.com/appraisals/ddr4-16gb-rdimm
- eBay, Samsung 16 GB PC4-2133P: https://www.ebay.de/p/10061718399
- Inetum, HPE P00920-B21: https://store.inetum.be/product/details/hewlett-packard-enterprise/motherboard-memory-processor/p00920b21/1171XG70?flang=en
- Offerta-internet, IP statico per partita IVA: https://offerta-internet.it/partita-iva
- resolution.de, prezzi Jira 2026: https://www.resolution.de/post/jira-pricing-plans/
- Wavenet, prezzi M365 UK da luglio 2026: https://www.wavenet.co.uk/blog/microsoft-365-price-increase-july-2026
- Priority IT, prezzi M365 UK da luglio 2026: https://priority-it.co.uk/2026/05/what-the-microsoft-365-price-increases-in-july-2026-mean-for-you/
- wz-it, licenza self-hosted di NetBird: https://wz-it.com/en/blog/netbird-self-hosting-license-commercial-starter/
- Pangolin, edizioni: https://docs.pangolin.net/self-host/enterprise-edition
- Linuxiac, MinIO senza sviluppo attivo: https://linuxiac.com/minio-ends-active-development/
- It's FOSS, MinIO: https://itsfoss.com/news/minio-moves-away-from-open-source/
- Elestio, MinIO in manutenzione: https://blog.elest.io/minio-is-in-maintenance-mode-your-guide-to-s3-compatible-storage-alternatives/
- Open WebUI, licenza: https://docs.openwebui.com/license/
- Wikipedia, Cyber Essentials: https://en.wikipedia.org/wiki/Cyber_Essentials
- Forensic Control, prezzi Cyber Essentials: https://forensiccontrol.com/guides/how-much-does-cyber-essentials-cost/

**File locali**

- `C:/Users/alber/SerSan-AgentOS/allegati/infra/SerSan Infra Board.md`
- `C:/Users/alber/SerSan-AgentOS/allegati/infra/board-testo-completo.txt`
- `C:/Users/alber/SerSan-AgentOS/allegati/infra/board-vlan.txt`
- `C:/Users/alber/SerSan-AgentOS/PRESENTAZIONE-CEO.md` (§12, §14)
- `C:/Users/alber/SerSan-AgentOS/ricerca/01-sersanoutreach.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/05-marketing-e-post.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/14-costi-abbonamenti-e-api.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/15-hardware-server-e-rete.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/22-architettura-scelta.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/25-board-michele-e-delta.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/26-claude-agent-sdk.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/27-hermes-self-hosted.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/28-chat-di-gruppo-self-hosted.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/29-conoscenza-task-e-documenti.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/30-call-e-trascrizione-self-hosted.md`
- `C:/Users/alber/SerSan-AgentOS/ricerca/31-voce-andrea-self-hosted.md`
