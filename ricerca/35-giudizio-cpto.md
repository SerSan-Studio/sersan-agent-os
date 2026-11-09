# 35 · Giudizio del CPTO sulle tre proposte nel board di Michele

**Data:** 25/10/2026. **Lente:** quella di Michele Sanna, CPTO. Conta l'aderenza al suo board, che è vincolante. Contano il self-hosting, la manutenzione con un team di quattro persone, la maturità dei componenti e il peso su RAM e GPU. Conta la preferenza che Michele ha dichiarato per l'Agent SDK di Claude, senza escludere Hermes.
**Proposte giudicate:** `34-proposta-1-agent-sdk.md` (P1), `34-proposta-2-hermes-self-hosted.md` (P2), `34-proposta-3-claude-team-e-mcp.md` (P3), lette per intero.
**Altre fonti:** il board (`allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`), `00-visione-funzionalita.md`, `21-giudizio-cpto.md`, i rapporti 25, 26, 27, 32 e 33. Ho ricontrollato sul web i fatti che pesano di più (§2).
**Etichette:** [verificato: fonte] = letto oggi nella fonte indicata. [non verificato] = stima, calcolo o giudizio mio. gp = giorni-persona. Prezzi IVA esclusa salvo dove scritto, letti il 24-25/10/2026.
**Regola di Alberto applicata:** una proposta che declassa una funzione o un'integrazione perde punti sulla visione, e non la premio come più semplice per questo motivo.

---

## In breve

**Vince la Proposta 1 (motore sull'Agent SDK), con 44 punti su 60.** Segue la Proposta 3 con 42. La Proposta 2 si ferma a 34.

- **P1** è la risposta più diretta al messaggio di Michele: orchestratore sul server, Agent SDK, Hermes evitato ma tenuto come uscita prezzata. Ha la sicurezza migliore. Gli agenti stanno in una VLAN propria e il Cancello in una macchina separata. Ogni agente porta all'MCP RAG l'identità della persona per cui lavora, come chiede il board ("Permessi per utente"). Ha due difetti seri: dà valore tardi (pilota alla settimana 16) e ha un errore nei costi della corrente.
- **P3** è la più vicina alla filosofia del board ("il server cerca e prepara, Claude ragiona") ed è la più veloce a dare valore. In cambio declassa 10 agenti a "Claude Team usato da una persona". Mette il Cancello nella stessa macchina del motore che legge testo di terzi. Espone sei endpoint MCP su internet. Il suo bilancio della RAM non conta alcuni servizi.
- **P2** porta Hermes, che Michele preferisce evitare. Oggi la scheda #143547 del gateway unico ha 276 problemi aperti, 9 di sicurezza e 0 risolti su `main` [verificato: API GitHub, 25/10/2026 alle 14:54 UTC]. Hermes non sa passare all'MCP RAG l'identità della persona [verificato: docs MCP di Hermes]. Inoltre P2 allenta il cancello di sicurezza che il suo stesso rapporto di ricerca (27 §11) metteva prima di usare Hermes come orchestratore.

**Il mio dissenso più forte** (§6): il collo di bottiglia non è il motore, è Michele. Tutte e tre le proposte gli chiedono 2-3 VLAN nuove e 11-13 servizi nuovi da tenere patchati entro 14 giorni. Gli chiedono anche un "posto agenti" anticipato. Però contano Michele a 0,5 gp a settimana e non contano il lavoro d'infrastruttura.

---

## 1. Punteggi (0-10 per criterio, totale su 60)

| Proposta | Copertura della visione | Tempo al valore | Costo | Affidabilità e manutenzione | Sicurezza e privacy | Aderenza al board | **Totale** |
|---|---|---|---|---|---|---|---|
| **P1 Agent SDK** | 9 | 6 | 6 | 7 | 8 | 8 | **44** |
| P3 Claude Team e MCP | 7 | 8 | 6 | 7 | 6 | 8 | **42** |
| P2 Hermes self-hosted | 8 | 7 | 5 | 4 | 5 | 5 | **34** |

[non verificato: giudizio mio, motivato nei §3-4]

---

## 2. Cosa ho verificato oggi sul web

| Affermazione delle proposte | Esito | Fonte |
|---|---|---|
| Scheda #143547 di Hermes: 273 (P1) o 276 (P2) problemi aperti | **276** problemi aperti su `main`: 140 rotti, 108 degradati, 9 di sicurezza, 19 cosmetici. 0 risolti su `main`, 39 in revisione in 14 PR. Aggiornata il 25/10/2026 alle 14:54 UTC. Il dato di P1 è vecchio di qualche ora | [verificato: https://api.github.com/repos/NousResearch/hermes-agent/issues/143547] |
| Ultima release di Hermes v0.22.5 | sì, del 23/10/2026; prima la v0.22.4 e la v0.22.3, uscite entrambe il 21/10/2026 | [verificato: https://api.github.com/repos/NousResearch/hermes-agent/releases] |
| Agent SDK TS 0.3.310 con Claude Code 2.1.310 | sì: `"version":"0.3.310"`, `"claudeCodeVersion":"2.1.310"` | [verificato: https://registry.npmjs.org/@anthropic-ai/claude-agent-sdk/latest] |
| L'SDK passa intestazioni HTTP scelte da noi a ogni server MCP | sì: `headers` nella configurazione `mcpServers` passata a ogni `query()` | [verificato: https://code.claude.com/docs/en/agent-sdk/mcp] |
| `PreToolUse` con `defer` ferma il turno e lo fa riprendere | sì: il turno finisce con `stop_reason` "tool_deferred". `deny` prevale su `defer`, `defer` su `ask`. Se l'hook non risponde in tempo, la chiamata è bloccata | [verificato: https://code.claude.com/docs/en/agent-sdk/hooks] |
| Hermes manda all'MCP solo un valore fisso o il nome del profilo | sì: `value_from: static` oppure `value_from: profile`, "resolved once at connect time". Nessun modo per passare la persona che scrive | [verificato: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp] |
| Compiti programmati di Claude Code (ex routine): limiti | in anteprima di ricerca; su Pro, Max, Team ed Enterprise; le espressioni che girano più di una volta l'ora sono rifiutate; appartengono al singolo account, non si condividono, e ciò che fanno coi connettori "appears as you" | [verificato: https://code.claude.com/docs/en/routines] |
| Projects non disponibili sul piano Team | sì: "Projects aren't offered on Team or Enterprise plans yet" | [verificato: https://code.claude.com/docs/en/claude-projects] |
| Prezzi e limiti di Claude Team | posto standard 20 $ (25 $ mensile), premium 100 $ (125 $ mensile). "Up to $500 per month in pooled API credits". Log di audit e conservazione personalizzata solo su Enterprise. Controlli di spesa per utente "Yes" anche su Team | [verificato: https://claude.com/pricing/team, 25/10/2026] |
| PR #36736 di LiteLLM sull'header `anthropic-beta` ancora aperta | sì: aperta, non unita, aggiornata il 13/10/2026 | [verificato: https://api.github.com/repos/BerriAI/litellm/pulls/36736] |
| MinIO archiviato | sì: `archived: true` | [verificato: https://api.github.com/repos/minio/minio]; la data del 12/02/2026 [non verificato da me: ricerca/25 N14] |
| VPS Hetzner per Pangolin: 5,99 € (P1, P2) o 6,49 € (P3) | 5,99 €/mese IVA esclusa per la linea Cost-Optimized, segnata "Currently not available". 6,49 € per la linea Regular Performance. Il prezzo realistico oggi è quello di P3 | [verificato: https://www.hetzner.com/cloud/, 25/10/2026] |
| Chat SDK per la Porta chat | `vercel/chat`, licenza MIT, non archiviato, ultimo push il 23/10/2026, 2.421 stelle | [verificato: https://api.github.com/repos/vercel/chat] |
| Pangolin: aggiramento del login per percorso e filtri per IP | sì: azioni Bypass Auth, Block Access e Pass to Auth; corrispondenze per Path, IP e CIDR | [verificato: https://docs.pangolin.net/manage/access-control/rules] |

Context7 non l'ho usato. Le tre proposte dicono che oggi ha la quota esaurita, quindi ho letto le pagine ufficiali con WebFetch.

---

## 3. Numeri che non tornano

### 3.1 Proposta 1

1. **La corrente della RAM è contata due volte.** P1 mette "corrente della seconda GPU 6,39-17,89 €" nella fase E e "corrente di RAM e seconda GPU 12,78-28,11 €" nel listino. Il rapporto 32 dice altro: la GPU costa 2,55-7,66 €/mese e i 12 moduli di RAM 6,39-10,22 €/mese, a 0,35 €/kWh [verificato: ricerca/32 §5.2]. 6,39-17,89 è la somma di GPU e RAM. P1 però aggiunge la RAM già dalla fase C. L'errore nasce in ricerca/33 riga 214, che chiama "corrente della seconda GPU" la somma delle due [verificato: ricerca/33 riga 214]. Effetto corretto [non verificato: calcolo mio]:
   - fase E: circa **74-141 €** al mese, non 78-151;
   - fase F: circa 74-168 €, non 78-178;
   - listino a regime: circa **479-583 €**, non 483-593.
2. **Il VPS ha due prezzi.** Nei §3.4 e §4.5 vale 5,99 €, nei §8.1-8.2 vale 0-6,49 €. Oggi la linea da 5,99 € non è disponibile (§2): va usato 6,49 € ovunque.
3. **Problemi di Hermes:** 273 nel §1, oggi sono 276 (§2).
4. Il resto torna. Fasi: 25 + 51 + 55 + 20 + 40,5 + 26,5 = 218 gp; con la riserva 289, cioè circa 290. Una tantum: 3.431-4.295 €. Bilancio della RAM: 21, 49,5 e 66-70 GB nuovi su 53 liberi. Calendario: circa 6,5 gp a settimana fino alla fase C, 7,5 dopo [verificato: ricontati sulle tabelle di P1].

### 3.2 Proposta 2

1. **I 151 gp (171 con H6) non si confrontano con gli altri piani.** P2 stima 0,6 gp per profilo, circa 30 gp per i 50 profili. P1 stima 67 gp per il contenuto dei 57 agenti, cioè circa 1,2 gp l'uno [verificato: P2 §8.2; P1 §4.3]. Il motore in sé costa uguale: 22,5 gp per Hermes, 21 per l'SDK [verificato: ricerca/27 §10; ricerca/26 §10.2]. Con lo stesso metro di P1, P2 sale verso **200 gp di base** [non verificato: calcolo mio]. Il vantaggio di P2 sui giorni è quasi tutto nel metodo di stima.
2. **Manca la corrente della RAM.** P2 dice che i +192 GB servono prima di H4, ma nel mensile non mette 6,39-10,22 €/mese [verificato: P2 §3.5 e §9.1; ricerca/32 §5.2].
3. **La fase H6 è larga.** 26,5 gp con la riserva in 8 settimane, a 6,5 gp a settimana: la capacità sarebbe circa 52 gp. Il calendario di 42 settimane ha 3-4 settimane di aria [non verificato: calcolo mio].
4. **Il PBS ha due stime.** 382-967 € unisce la stima vecchia di ricerca/33 e quella nuova di ricerca/32 (circa 525-967 € netti) [verificato: ricerca/32 §7; ricerca/33 §4.1].
5. **P2 allenta il cancello di sicurezza.** Ricerca/27 §11 mette quattro condizioni prima di usare Hermes "come orchestratore": la v0.23 con note complete, le righe MSG-43, GW-41, KB-10 e HR-6 chiuse su `main`, il bug #113578 chiuso e 10 scenari passati [verificato: ricerca/27 §11]. P2 le chiede solo per i dati rossi. Lascia così entrare in Hermes i dati gialli dei clienti già in H2, con 9 problemi di sicurezza aperti [verificato: P2 §10.3].

### 3.3 Proposta 3

1. **Il bilancio della RAM non conta tutti i servizi.** La tabella del §3.3 non conta listmonk (0,5 GB), DocuSeal (1 GB) e la fatturazione (1-2 GB), che P3 stessa vuole in casa nel §8 E. Non conta nemmeno Postiz (2 GB), se si sceglie al posto di Metricool. Mancano 2,5-5,5 GB. Il margine scende da +3/+12 a circa **-2,5/+9,5 GB** [non verificato: calcolo mio con le stime di P1 §3.1]. La frase "la RAM in più non serve subito" regge solo al limite.
2. **La stima del PBS è superata.** P3 usa 382-730 € di ricerca/33. Ricerca/32 l'ha portata a 640-1.180 € IVA inclusa, cioè circa 525-967 € netti, perché i dischi sono raddoppiati di prezzo [verificato: ricerca/32 §7]. Il subtotale delle spese di subito passa da 3.114-4.117 € a circa **3.257-4.354 €**, come in P1 [non verificato: calcolo mio].
3. **L'UPS non è quello consigliato.** P3 scrive 1.011-1.060 € (APC). Ricerca/32 consiglia l'Eaton 5PX da 1.500 W a 937-1.144 €, perché l'APC da 1.000 W con due GPU lavora all'80-85 % al picco [verificato: ricerca/32 §6].
4. **Il calendario parte troppo basso.** P3 scrive "30-42 settimane" e dice di usare la riserva. Con 254 gp e 6,5-7,5 gp a settimana servono 34-39 settimane. Si arriva a 30 solo senza riserva [non verificato: calcolo mio].
5. **Una protezione è nel posto sbagliato.** P3 vuole proteggere i propri endpoint MCP con l'accesso condizionale di Entra sugli IP di Anthropic. L'accesso condizionale guarda però il login della persona in Entra, non le chiamate che i server di Anthropic fanno al nostro MCP con il token già emesso [non verificato: lettura mia]. Il filtro sugli IP va messo in Pangolin, con una regola CIDR [verificato: docs Pangolin, §2]. P2 lo fa così [verificato: P2 §3.4].

### 3.4 Comuni alle tre

- **Il "posto agenti" anticipato rompe la regola del board.** Il board dice "Ogni fase parte quando la precedente è validata" [verificato: board, Roadmap]. Tutte e tre chiedono LiteLLM, PostgreSQL e n8n in F2, cioè prima della sicurezza (F3) e prima di F4. Il rapporto 25 aveva già una seconda strada: pilota dopo F3 e, nel frattempo, dati verdi con Claude Team [verificato: ricerca/25 riga 444]. Solo P2 limita il pilota a dati verdi e gialli finché F3 non è validata.
- **Nessuna parla della CPU fuori supporto.** Intel non aggiorna più la Gold 5218 dal 30/06/2025. Per Cyber Essentials è un possibile rilievo [verificato: ricerca/32 §1 e §9]. È un tema del board, ma riguarda anche il "software supportato" dei servizi nuovi.
- **Solo P1 ricorda la regola di HPE sulle GPU.** HPE scrive "Mixing of GPUs is not supported", quindi la seconda GPU porta il server fuori dalla configurazione supportata [verificato: ricerca/32 §4.4]. La garanzia però è di Bargain, non un contratto HPE [verificato: ricerca/32 §4.4].

---

## 4. Il giudizio, criterio per criterio

### 4.1 Copertura della visione

- **P1: 9.** Tutte le 90 voci hanno un componente, una fase e "cosa serve ancora". I 57 agenti sono profili veri, che si passano il lavoro sulla bacheca. Gli strumenti esterni (operatore telefonico, relay SMTP, Telegram, WhatsApp, Slack, kit commerciale) sono scritti come necessità con il loro prezzo, non come rinunce [verificato: P1 §6 e §4.5].
- **P2: 8.** Anche qui c'è tutto, con componente e fase. Hermes porta pronti kanban, skill che migliorano e canali. Però i permessi della memoria valgono per istanza, non per persona [verificato: §2]. Così perdono qualità K4, C6 e i "permessi per utente" del board. WhatsApp oltre le 24 ore richiede comunque il Cancello o n8n [verificato: P2 §5.3].
- **P3: 7.** È onesta: da sola copre 59 voci, 24 in parte e 7 no; con le aggiunte A-G le copre tutte [verificato: ricontato sulla tabella del §7, 59 + 24 + 7 = 90]. Ma 10 agenti sono di tipo "T": Copywriter, Pubblicatore, Agente video, Agente grafiche, Sviluppatori, Intervistatore, Assistente personale e parti di altri [verificato: P3 §5]. Un agente "T" esiste solo quando una persona apre Claude Team. Non riceve passaggi dalla bacheca e non lavora da solo. Così J7 ("il marketing parla con la squadra di video, slide e contenuti") e G9 (agenti in organigramma) diventano lavoro di una persona aiutata da Claude. È un declassamento: per la regola di Alberto tolgo punti.

### 4.2 Tempo al valore

- **P3: 8.** Nella fase P0, dalla settimana 1, tutti e quattro lavorano in Claude Team con le skill dell'azienda, senza server. Il recap dopo le call arriva alla settimana 11 [verificato: P3 §9].
- **P2: 7.** Il pilota con 10 profili è pronto alla settimana 11. Gli adattatori di Hermes accorciano i canali [verificato: P2 §8.1]. Ma serve il "posto agenti" in F2, altrimenti tutto slitta di 4-7 settimane [verificato: P2 §8.1].
- **P1: 6.** Nella fase A ci sono già i post di marketing via Claude Team e la demo di una carta [verificato: P1 §7.2]. Il pilota vero (post-call, debrief, marketing in Teams) però finisce alla settimana 16, cinque settimane dopo le altre due.

### 4.3 Costo

Il mensile a regime è quasi uguale per tutte: circa 479-583 € (P1 corretto), 519 € (P2) e 525 € (P3). Lo stesso vale per i +446,70 € a fine bundle di Claude Team [verificato: P1 §8.2; P2 §9.2; P3 §10.1]. Contano quindi i giorni, la RAM e la manutenzione.
- **P1: 6.** È il piano con più giorni (218 gp, circa 290 con la riserva). Chiede +192 GB di RAM (816-1.218 €) prima della fase C e la seconda GPU prima della fase E. Ha l'errore sulla corrente (§3.1).
- **P3: 6.** Sulla carta è la più economica: niente RAM, GPU nella fase F5 come nel board. Ma il risparmio di RAM viene in buona parte dal declassamento del §4.1, che non premio. Il bilancio della RAM e la stima del PBS sono ottimisti (§3.3). Inoltre P3 lega il lavoro di ogni giorno ai posti premium: i compiti programmati consumano l'uso del posto, e oltre il limite servono crediti a consumo [verificato: §2, routines].
- **P2: 5.** I giorni sono sottostimati (§3.2). La manutenzione di Hermes costa 2-3 gp al mese con sei istanze [verificato: P2 §8.2]. La RAM serve prima, perché ogni istanza ha il suo gateway [verificato: P2 §3.5]. Le eccezioni arrivano fino a circa 284 € al mese [verificato: P2 §9.2].

### 4.4 Affidabilità e manutenzione

- **P1: 7.** Un solo linguaggio (TypeScript) e un solo fornitore per il motore. L'SDK esce quasi ogni giorno ed è ancora 0.3.x [verificato: §2], ma c'è una versione fissata e un collaudo ogni due settimane, dentro i 14 giorni di Cyber Essentials [verificato: P1 §9]. C'è parecchio codice nostro: runner, Cancello, Porta, server MCP, bacheca. Le macchine sono tre (`agenti-01`, `cancello-01`, `mcp-01`) e i container di famiglia nove. L'uscita verso Hermes è prezzata [verificato: P1 §10].
- **P3: 7.** Il motore è leggero (10 agenti, al massimo 6 sessioni), con una VM e un LXC. In più però c'è un secondo mondo da gestire: la configurazione di Claude Team, con funzioni in anteprima o in beta [verificato: §2]. C'è anche un gateway OAuth per sei server MCP pubblici [verificato: P3 §3.2 e §4]. Il codice nostro è quasi lo stesso di P1: Cancello, Porta, bacheca, MCP.
- **P2: 4.** I 276 problemi del gateway unico, 9 di sicurezza e 0 risolti, sono il punto debole [verificato: §2]. Si aggiungono 44 release dal 12/3 e almeno 45 avvisi di sicurezza nel 2026 [verificato: ricerca/27 righe 26 e 233]. Ci sono sei istanze e sei bot Teams. Ci sono problemi noti fra Hermes e LiteLLM (MP-19, MP-23, MP-25, KB-11) [verificato: ricerca/27 §3.2]. I linguaggi sono due: Python 3.14 per Hermes e TypeScript per il Cancello [verificato: P2 §10.1]. Per un team di quattro è il carico più pesante.

### 4.5 Sicurezza e privacy

- **P1: 8.**
  - Gli agenti stanno in una VLAN 32 nuova e possono uscire solo verso LiteLLM, i server MCP e l'API del Cancello [verificato: P1 §3.4].
  - Il Cancello sta in una VM separata, con i segreti degli esecutori.
  - Nessuno strumento manda nulla all'esterno; c'è la modalità `dontAsk` con un elenco chiuso di strumenti.
  - Ogni agente porta l'identità della persona all'MCP RAG [verificato: §2, intestazioni per server].
  - Pochi endpoint pubblici: il bot, i webhook e l'MCP RAG.
- **P3: 6.**
  - Claude Team riceve più dati che nelle altre proposte: memoria, CRM in lettura, BookStack. Il piano Team non ha log di audit né conservazione personalizzata [verificato: §2].
  - Gli endpoint MCP pubblici sono sei, "senza il login di Pangolin davanti" [verificato: P3 §3.2].
  - Il Cancello, la Porta e il motore che legge mail e trascrizioni stanno nella stessa VM `agenti-01` [verificato: P3 §1 e §3.2]. Un'iniezione riuscita nel motore arriva vicino ai segreti degli esecutori.
  - Di buono: l'identità di ogni persona arriva via OAuth e i dati rossi vanno oscurati.
- **P2: 5.**
  - Restano 9 problemi di sicurezza aperti nel gateway [verificato: §2].
  - I permessi valgono per istanza [verificato: §2].
  - Su Pangolin servono più rotte con "Bypass Auth", una per ogni bot.
  - L'account ospite Nous della v0.22.5 deve dimostrare di non chiamare nulla senza login [non verificato: P2 §2].
  - Il contenimento proposto è serio: istanze separate, plugin che blocca e "fails closed" allo scadere del tempo, carte solo dal Cancello [verificato: P2 §5.4]. Però si appoggia a un componente con difetti di sicurezza noti.

### 4.6 Aderenza al board

- **P1: 8.**
  - Usa quasi tutto lo stack di Michele: n8n, LiteLLM, PostgreSQL 16, Qdrant con MCP RAG, BookStack, Infisical, Firecrawl e OBSRV [verificato: P1 §4.1].
  - Segue la preferenza di Michele per l'SDK.
  - Chiede tre VLAN nuove (25, 32, 35), tre VM e la RAM prima della fase C. RAM e GPU sono upgrade che Michele stesso ha proposto; cambia solo quando comprarli.
  - Propone anche di accendere Experimental 1 e 2 solo quando servono: è una decisione che spetta a Michele.
- **P3: 8.**
  - È la più vicina alla frase del board "Il server cerca e prepara, Claude ragiona" [verificato: board, Pipeline AI].
  - Chiede due VLAN nuove e lascia la GPU nella fase F5.
  - Però toglie il login di Pangolin davanti alle rotte MCP, mentre il board scrive "con autenticazione davanti" [verificato: board, Accesso]. In più il risparmio di RAM regge solo al limite (§3.3).
- **P2: 5.**
  - Mette al centro Hermes, che Michele ha chiesto di evitare se possibile [verificato: messaggio di Michele del 25/10/2026].
  - Porta un secondo linguaggio e sei bot nel tenant.
  - Anticipa RAM e GPU già a H4. Il rapporto 27 concludeva che nel board Hermes "non è necessario" [verificato: ricerca/27 §11].

---

## 5. Il vincitore per la lente CPTO

**Proposta 1.** Le ragioni, in ordine di peso:
1. È l'architettura che Michele può difendere davanti a Cyber Essentials. Gli agenti sono isolati in una VLAN, i segreti degli esecutori stanno in un'altra macchina, gli endpoint pubblici sono pochi e i permessi valgono per persona fino al RAG.
2. Segue alla lettera il messaggio di Michele: self-hosted, Agent SDK, Hermes evitato ma pronto come piano B sugli stessi pezzi.
3. Copre la visione senza declassare agenti.

**Perché non P3**, che le sta a due punti. P3 ha la fase P0 migliore e la disciplina sulla RAM migliore, e vanno prese. Ma come architettura di base sposta in Claude Team una parte del lavoro degli agenti. Così perde l'autonomia di 10 figure e aumenta i dati che escono verso un servizio senza log di audit. In più mescola il Cancello e il motore nella stessa macchina.

**Perché non P2.** Oggi non metterei dati dei clienti in un gateway con 9 problemi di sicurezza aperti e 0 risolti. Hermes ha senso solo come pilota confinato in Experimental-2, con dati verdi, per 6-8 gp [verificato: ricerca/27 §10 e §11].

---

## 6. Il mio dissenso più forte

**Il collo di bottiglia non è il motore, è Michele.**
- **I servizi nuovi.** Contando le tabelle, P1 aggiunge al board 13 componenti nuovi e 3 VLAN, P2 13 componenti e 2 VLAN, P3 11-12 componenti e 2 VLAN [non verificato: conteggio mio]:
  - le VM degli agenti e del Cancello, il server MCP e MariaDB;
  - la trascrizione, Vexa, Asterisk e Pipecat;
  - Postiz, listmonk, DocuSeal, la fatturazione e Buzz.
- **Le patch.** Ognuno di questi entra nel perimetro Cyber Essentials: patch critiche entro 14 giorni, software supportato [verificato: board, nota su Experimental]. Diversi sono pre-1.0 o giovani: Vexa 0.12, Buzz, l'Agent SDK 0.3 [verificato: P1 §3.1; §2].
- **Il tempo di Michele.** Tutte e tre contano Michele a circa 0,5 gp a settimana sul progetto [verificato: P1 §7.1; P2 §8.1; P3 §9]. Gli chiedono anche di anticipare un "posto agenti" in F2, contro la regola "ogni fase parte quando la precedente è validata". Nessuna mette in conto i giorni di Michele per installare, mettere in rete e patchare questi servizi.

Il confronto fra SDK, Hermes e Claude Team pesa meno di questa domanda. Prima di scegliere il motore va fissato il perimetro dei servizi nuovi, con un responsabile per le patch di ognuno. Va fissato anche un tetto ai servizi che entrano prima della fase F4 del board.

Un secondo dissenso, più stretto. P2 applica il cancello di ricerca/27 §11 solo ai dati rossi. Quelle quattro condizioni valevano per Hermes come orchestratore in sé, e vanno rimesse così.

---

## 7. Cosa va corretto nella Proposta 1

1. **Dare valore prima.** Adottare la fase P0 di P3 dalla settimana 1: Claude Team per tutti e quattro, skill dell'azienda, Projects condivisi, connettori M365 in sola lettura e Jira. Poi portare il primo pilota (post-call e debrief) alla settimana 11, come P2 e P3, dividendo in due la fase B.
2. **Non riordinare il board di Michele.** La strada di partenza deve essere quella che non lo tocca: pilota su stage, nella VLAN LAB, con una chiave diretta e un tetto nella Console, solo dati verdi e gialli finché F3 non è validata [verificato: ricerca/26 §10.3; ricerca/25 riga 444]. Il "posto agenti" in F2 resta una richiesta, non un presupposto.
3. **Correggere la corrente.** GPU 2,55-7,66 €/mese, RAM 6,39-10,22 €/mese. Fase E circa 74-141 €, listino circa 479-583 € (§3.1).
4. **Usare un solo prezzo per il VPS:** 6,49 €/mese, perché la linea da 5,99 € oggi non è disponibile (§2).
5. **Mettere in conto l'infrastruttura nuova.** Una riga di gp per installare e collegare VLAN 25, 32 e 35, le tre VM e i servizi nuovi. Un inventario in NetBox con il responsabile delle patch di ognuno. Una stima di manutenzione dalla fase B, non solo dopo la fase F.
6. **Decidere la RAM sui numeri.** Prima si legge nell'iLO come sono fatti i 192 GB. Poi si misura con un tetto di 6 sessioni, come in P3. Si comprano +192 GB uguali a quelli montati quando il margine misurato scende sotto i 5 GB, o prima di Vexa [verificato: ricerca/32 §2.2-2.5; P3 §3.3 per la soglia].
7. **Snellire senza perdere isolamento.** `mcp-01` in un LXC; meno container di famiglia dove permessi e segreti coincidono. Il Cancello resta in una macchina sua.
8. **Chiudere l'MCP RAG su internet** con una risorsa Pangolin dedicata, una regola CIDR sugli IP di Anthropic (`160.79.104.0/21`) e il resto bloccato, più l'OAuth di Entra nel server [verificato: docs Pangolin; ricerca/29 §5.4 per gli IP; disegno non verificato].
9. **Provare nello spike della fase A quattro cose.** La registrazione del bot Teams senza Azure. L'`aadObjectId` nelle azioni delle carte. Il `defer` con le chiamate parallele negate dal plugin. L'inoltro di `anthropic-beta` in LiteLLM, con la PR #36736 ancora aperta (§2).
10. **Fatturazione.** Invoice Ninja ha una licenza non verificata. Prima di contare i 3 gp bisogna sapere cos'è Sirius e chi fattura.
11. **Aggiornare i dati su Hermes:** 276 problemi, non 273 (§2).

---

## 8. Cosa prendere dalle altre due

- **Da P3:**
  - la fase P0 senza server;
  - il tetto di 6 sessioni come punto di partenza e la soglia di 5 GB per comprare RAM;
  - le aggiunte A-G come lista di controllo, perché nulla della visione resti senza un componente.
- **Da P2:**
  - la regola CIDR in Pangolin per le rotte pubbliche;
  - il limite "dati verdi e gialli finché F3 non è validata";
  - le uscite prezzate scritte come tabella con "cosa si perde" e "cosa resta".
- **Da tutte e tre:** il pilota Buzz e un eventuale pilota Hermes restano in Experimental-2, senza dati dei clienti.

---

## 9. Domande per Michele che questo giudizio aggiunge

1. Quanti dei 11-13 servizi nuovi accetti prima di F4, e chi li patcha entro 14 giorni?
2. Preferisci il pilota su stage in LAB con chiave limitata (nessun riordino di F2-F4) o il "posto agenti" anticipato?
3. VLAN 32 dedicata agli agenti, o VLAN 30 con il firewall di Proxmox per VM?
4. Va bene una CPU che Intel non aggiorna più dal 30/06/2025, per l'assessor di Cyber Essentials [verificato: ricerca/32 §9]?
5. Seconda GPU: accetti di uscire dalla configurazione supportata da HPE, con la garanzia di Bargain [verificato: ricerca/32 §4.4]?

---

## Fonti

**File del progetto** (letti il 25/10/2026)
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`
- `ricerca/00-visione-funzionalita.md`, `ricerca/21-giudizio-cpto.md`
- `ricerca/34-proposta-1-agent-sdk.md`, `ricerca/34-proposta-2-hermes-self-hosted.md`, `ricerca/34-proposta-3-claude-team-e-mcp.md`
- `ricerca/25-board-michele-e-delta.md`, `ricerca/26-claude-agent-sdk.md`, `ricerca/27-hermes-self-hosted.md`, `ricerca/32-hardware-e-upgrade.md`, `ricerca/33-costi-v2.md`

**Pagine web** (lette il 25/10/2026)
- https://api.github.com/repos/NousResearch/hermes-agent/issues/143547
- https://api.github.com/repos/NousResearch/hermes-agent/releases
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://registry.npmjs.org/@anthropic-ai/claude-agent-sdk/latest
- https://code.claude.com/docs/en/agent-sdk/mcp
- https://code.claude.com/docs/en/agent-sdk/hooks
- https://code.claude.com/docs/en/routines
- https://code.claude.com/docs/en/claude-projects
- https://claude.com/pricing/team
- https://api.github.com/repos/BerriAI/litellm/pulls/36736
- https://api.github.com/repos/minio/minio
- https://www.hetzner.com/cloud/
- https://api.github.com/repos/vercel/chat
- https://docs.pangolin.net/manage/access-control/rules
