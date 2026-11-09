# 35 · Giudizio con la lente del CEO (Alessandro, vendite)

**Data:** 25/10/2026. **Per:** Alessandro Serratt, con copia ad Alberto Tuveri e Michele Sanna.
**Cosa giudico:** le tre proposte del 25/10/2026: `34-proposta-1-agent-sdk.md` (P1), `34-proposta-2-hermes-self-hosted.md` (P2), `34-proposta-3-claude-team-e-mcp.md` (P3). Le ho lette per intero.
**La mia lente:** quanto presto arriva il primo valore commerciale, quanto costa, quanto tempo togliamo ai clienti, cosa vede Alessandro alla settimana 8.
**Vincoli:** il board di Michele è vincolante (`allegati/infra/`). Vale la regola di Alberto: nessuna funzione A1-L12 si toglie o si declassa perché oggi manca un componente. Chi declassa perde punti sulla visione.
**Etichette:** [verificato: fonte] = letto oggi nella fonte indicata; [non verificato] = stima, calcolo mio o giudizio. gp = giorni-persona. Prezzi IVA esclusa salvo dove scritto, rilevati il 24-25/10/2026.

---

## In breve

**Vince la Proposta 3** con la mia lente: 45 punti su 60, contro 42 della Proposta 1 e 34 della Proposta 2 [non verificato: giudizio].

- È l'unica che dà valore commerciale dalla prima settimana senza aspettare il server: 6,5 gp in quattro settimane, poi Claude Team usato ogni giorno da tutti e quattro [verificato: P3 §9].
- Alla fine copre le stesse 90 voci delle altre due, perché aggiunge bacheca, Porta chat, Vexa, Andrea e gli strumenti esterni con fase e costo [verificato: P3 §7-8].
- Ha un punto di arresto chiaro: dopo la fase P2 (settimana 22, 96,5 gp di base) il nucleo è completo e il resto si decide un pezzo alla volta [verificato: P3 §9 e §11].

**Va corretta** su cinque punti forti: conto della RAM troppo ottimista, alcuni agenti ridotti a skill usate da una persona, debito di sicurezza di SersanOutreach e decisione sull'email assenti dal piano, verifica alla settimana 11 invece che alla 8, dipendenza di costo dai posti premium di Claude Team (§9).

**Dalla Proposta 1** va preso il motore: identità della persona verso l'MCP RAG con le intestazioni HTTP dell'SDK, ponte verso il Cancello con `defer`, isolamento per famiglia. La Proposta 3 usa già un motore leggero sull'Agent SDK: basta adottare quei pezzi [verificato: P1 §1 e §4.3; P3 §1].

**Il mio dissenso più forte** riguarda tutte e tre: il problema commerciale di oggi è il funnel vuoto, non l'orchestrazione. Nessuna mette la decisione sull'email e la mailbox live come cancello delle prime quattro settimane, e tutte chiedono 42-43 settimane contro le 24 della presentazione (§8).

---

## 1. Punteggi (0-10 per criterio, totale su 60)

| Criterio | P1 Agent SDK | P2 Hermes | P3 Claude Team e MCP |
|---|---|---|---|
| Copertura della visione | 9 | 9 | 7 |
| Tempo al valore | 5 | 6 | 9 |
| Costo | 6 | 6 | 8 |
| Affidabilità e manutenzione | 7 | 4 | 6 |
| Sicurezza e privacy | 8 | 4 | 6 |
| Aderenza al board di Michele | 7 | 5 | 9 |
| **Totale** | **42** | **34** | **45** |

[non verificato: giudizio mio, motivato nei §2-7]

**Come leggo i criteri.**
- **Visione:** tutte e tre danno un componente a ogni voce A1-L12. La P3 perde due punti perché dieci agenti diventano skill di Claude Team usate da una persona (Copywriter, Agente video, Agente grafiche, Pubblicatore, Intervistatore e altri) e la tabella di copertura mette in testa la colonna "da sola" con 7 "No" [verificato: P3 §5 e §7]. Per J7 e G9 questo è un declassamento: un agente che non riceve lavoro dalla bacheca non è un agente in organigramma.
- **Tempo al valore:** conta cosa arriva ad Alessandro e quando (§2).
- **Costo:** mensile, una tantum e gp, sulla stessa base (§4).
- **Affidabilità e manutenzione:** pezzi sempre accesi, maturità dei componenti, gp al mese per restare nei 14 giorni di Cyber Essentials.
- **Sicurezza e privacy:** identità per persona, dove vanno i dati rossi, superfici pubbliche.
- **Aderenza al board:** quanto la proposta segue il disegno di Michele e il suo messaggio ("se possiamo evitare anche Hermes meglio, usiamo Agent SDK di Claude").

---

## 2. Cosa vede Alessandro alla settimana 8

| | P1 Agent SDK | P2 Hermes | P3 Claude Team e MCP |
|---|---|---|---|
| Settimane 1-4/5 | Skill di marketing in Claude Team (2 gp); un agente di prova che propone una mail e si ferma su una carta premuta dal telefono; SersanOutreach verde su identità e MFA [verificato: P1 §7.2-7.3] | Cancello che passa i test in CI; 10 profili scritti; Teams pronto per le trascrizioni; marketing con Claude Team [verificato: P2 §8.1] | Tutti e quattro in Claude Team ogni giorno; calendario dei post pieno fino a Natale; prime offerte e slide con il nostro stile; connettori M365 (sola lettura) e Jira [verificato: P3 §9] |
| Settimane 5/6-8 | Motore che passa sul server; Cancello, Porta e trascrizioni in costruzione [verificato: P1 §7.2] | Tre istanze Hermes in costruzione; primo bot in Teams "in giorni" [verificato: P2 "In breve"; stima di ricerca/27 §9.5] | Cancello v1, Porta chat v1, MCP memoria in costruzione [verificato: P3 §9] |
| Post-call automatico | a fine fase B (sett. 16), verifica alla sett. 11 | a fine H1 (sett. 11) | a fine P1 (sett. 11) |
| Dipende dai tempi del board? | sì, "posto agenti" anticipato in F2 | sì, "posto agenti" a fine F2, con un calendario del board più veloce degli altri | no per P0; sì da P1 |
| **Valore commerciale reale alla sett. 8** | **basso**: post e una demo | **medio-basso**: post e un bot di prova, solo dati verdi e gialli | **alto per il punto di partenza**: post, offerte, slide, domande su posta, calendario e trascrizioni delle nostre call Teams via connettore M365 |

[non verificato: lettura mia dei piani]

**Una nota per Alessandro.** La presentazione prometteva il post-call e la verifica alla settimana 8 [verificato: PRESENTAZIONE-CEO.md §11]. Oggi nessuna delle tre arriva al post-call automatico prima della settimana 11. Il motivo è che call, voce, chat e strumenti ora si fanno in casa, come chiede il board [verificato: P1 §7.2; P2 §8.1 "Perché più del piano precedente"].

---

## 3. Tempo tolto ai clienti

Alberto e Mattia sono anche le persone che servono ai clienti: i gp sono la spesa più grande.

| | P1 Agent SDK | P2 Hermes | P3 Claude Team e MCP |
|---|---|---|---|
| Prima fase (gp base / con riserva) | A: 25 / 33 | H0: 13,5 / 18 | P0: 6,5 / 8,5 |
| gp fino al primo post-call automatico | 76 / 101 (fine B) | 49 / 65 (fine H1) | 41 / 54,5 (fine P1) |
| Totale | 218 / circa 290, sett. 1-43 | 171 / 227,5, sett. 1-42 | 191 / 254, sett. 1-42 |
| Punto di arresto con nucleo completo | dopo C: 131 gp, sett. 27 | dopo H2: 92 gp, sett. 20 | dopo P2: 96,5 gp, sett. 22 |
| Manutenzione dichiarata | aggiornamento dell'SDK ogni due settimane; sistema 1-2 gp a settimana | Hermes 2-3 gp al mese, più il resto | come P1, ma il motore serve solo 10 agenti |

[verificato: tabelle dei piani P1 §7.2, P2 §8.1-8.2, P3 §9; somme parziali: calcolo mio, non verificato]

**Attenzione al confronto dei gp.** La P2 sembra la più leggera, ma solo perché stima il contenuto di ogni agente a 0,6 gp. La P1 lo stima a 0,5-2 gp (67 gp per 57 agenti), la P3 a circa 0,9 gp [verificato: P1 §4.3 riga 14; P2 §8.2; P3 §9]. Il motore in sé costa uguale: Hermes 22,5 gp di base, Agent SDK 21 [verificato: ricerca/27 §10; ricerca/26 §10.2]. Con la stessa stima per agente la P2 arriverebbe a circa 205-210 gp, vicina alla P1 [non verificato: calcolo mio].

---

## 4. Costi sulla stessa base

### 4.1 Al mese, in più rispetto a oggi

| Periodo | P1 | P2 | P3 |
|---|---|---|---|
| Azure ancora acceso | circa 135 € | circa 135 € | circa 135 € |
| Dopo Azure, agenti al lavoro | 14-31 € | circa 14 € | da -15 a +20 € |
| Con Andrea | 78-151 € (con WhatsApp e corrente della GPU) | circa 104 € (58 € con il piano PRO), più 2,55-7,66 € di GPU | 58-110 € |
| Listino a regime | 483-593 € | circa 519 €, più fino a 284 € di eccezioni | circa 525 € |
| Fine del bundle Claude Team | + 446,70 € | + 446,70 € | + 446,70 € |
| Senza crediti API | + 195,65 € | + 195,65 € | + 195,65 € |

[verificato: P1 §8.1-8.2; P2 §9.1-9.2; P3 §10.1; ho ricontrollato le somme dei listini, che tornano]

**Lettura.** A parità di voci i tre listini valgono circa 519-525 €. La P1 sembra più cara solo perché mette dentro WhatsApp, Slack, VPS, relay SMTP e la corrente di RAM e GPU, che le altre lasciano fra le eccezioni [non verificato: confronto mio]. Il costo vero che cambia è un altro: con la P3 Claude Team diventa lo strumento di ogni giorno e i 5 posti premium (446,70 € al mese) servono davvero. Con P1 e P2 si potrebbe scendere a meno posti premium, perché gli agenti usano la chiave API [verificato: P1 §8.1 "357,36 con 4 premium"; P3 §10.1 "214,42 con 2 premium e 2 standard"].

### 4.2 Una tantum

| | P1 | P2 | P3 |
|---|---|---|---|
| Subito (con le voci del board) | 3.257-4.354 € | 3.114-4.354 € | 3.114-4.117 € |
| Più avanti, sulla stessa base (GPU, UPS, RAM, staffa, numero, vivavoce) | 2.554-3.491 € | 2.554-3.491 € | 1.804-2.617 € |
| Altri 192 GB di RAM | sì, prima della fase C (sett. 17) | sì, prima di H4 (sett. 24) | no, salvo margine finito |

[verificato: P1 §8.4; P2 §9.3; P3 §10.2; righe "più avanti" ricalcolate da me sulle stesse voci, non verificato]

La P3 risparmia 750-875 € più avanti quasi solo perché non compra la RAM. Nel §6 spiego perché quel risparmio è incerto.

---

## 5. Affermazioni controllate oggi sul web

| Affermazione | Esito | Fonte |
|---|---|---|
| Claude Team: posto standard 20 $ (25 $ mensile), premium 100 $ (125 $ mensile), 5 volte l'uso | confermata | [verificato: claude.com/pricing/team, 25/10/2026] |
| Claude Team non ha log di audit né conservazione personalizzata | confermata | [verificato: idem] |
| Claude Team ha "Up to $500 per month in pooled API credits" | confermata; se valgano dietro LiteLLM resta da chiedere | [verificato: idem]; uso dietro LiteLLM [non verificato] |
| Tetti di spesa per persona su Team "contraddittori" (P3 §2) | la pagina elenca controlli per utente e organizzazione anche per Team; il comportamento reale va provato | [verificato: idem]; comportamento [non verificato] |
| Compiti programmati di Claude Code: anteprima di ricerca, di un solo account, agiscono "as you", non più di una volta l'ora | confermata | [verificato: code.claude.com/docs/en/routines, 25/10/2026] |
| Projects di Claude Code non offerti su Team | confermata: "Projects aren't offered on Team or Enterprise plans yet" | [verificato: code.claude.com/docs/en/claude-projects, 25/10/2026] |
| Agent SDK: intestazioni HTTP decise da noi per ogni server MCP (base dell'identità per persona della P1) | confermata: `headers` nella configurazione passata a ogni `query()` | [verificato: code.claude.com/docs/en/agent-sdk/mcp, 25/10/2026] |
| Hermes: ultima release v0.22.5 del 23/10/2026 | confermata | [verificato: API GitHub releases, 25/10/2026] |
| Hermes: scheda #143547 con 276 problemi aperti, 9 di sicurezza, 0 risolti su `main` | confermata, aggiornata il 25/10/2026 alle 14:54 UTC | [verificato: API GitHub issue #143547, 25/10/2026] |
| VPS Hetzner da 5,99 € al mese | confermata per la linea Cost-Optimized; la Regular Performance parte da 6,49 € | [verificato: hetzner.com/cloud, 25/10/2026] |
| Funnel di oggi: 11 lead, 1 contattato, 0 meeting, 0 vinti, 91 deal senza valore; email non live; readiness NOT READY | confermata (dati al 05/10/2026) | [verificato: ricerca/01 righe 15-18] |

Context7 non l'ho usato: le tre proposte riportano la quota mensile esaurita, e le pagine ufficiali le ho lette direttamente.

---

## 6. Numeri che non tornano

1. **RAM della P3.** Il conto (41-50 GB nuovi, margine da +3 a +12 GB) non contiene servizi che la stessa P3 mette nel piano: listmonk, DocuSeal, lo strumento di fatturazione e Postiz se sostituisce Metricool. La P1 li stima circa 5 GB [verificato: P3 §3.3; P1 §3.2]. Con quei 5 GB il margine scende a circa -2/+7 GB [non verificato: calcolo mio]. "La RAM in più non serve subito" va bene; "non serve" no.
2. **Calendario della P3.** "30-42 settimane": 30 settimane valgono i 191 gp di base senza riserva a 6,5 gp a settimana. Con la riserva e 7,5 gp a settimana sono circa 34 [non verificato: calcolo mio su P3 §9]. Scriverei 34-42.
3. **Ipotesi diverse sui tempi del board.** La P1 ipotizza F2-F3 nelle settimane 6-14 e F4 nelle 15-18; la P2 F2 nelle 5-7, F3 nelle 8-10, F4 nelle 11-14; la P3 non fissa date [verificato: P1 §7.1; P2 §8.1; P3 §9]. La P2 parte prima anche perché presume un board più veloce. La sua H2 (sett. 12-20) chiede F4 finita, che per la sua stessa ipotesi finisce alla settimana 14.
4. **Stima per agente.** 0,6 gp nella P2, circa 0,9 nella P3, 0,5-2 nella P1 (§3). Il confronto dei totali non è alla pari.
5. **Corrente della seconda GPU.** 6,39-17,89 € al mese nella P1 (25-70 W, da ricerca/33), 2,55-7,66 € nella P2 (10-30 W, da ricerca/32) [verificato: ricerca/33 riga 119; ricerca/32 riga 348]. Va scelta una sola ipotesi.
6. **UPS e GPU.** UPS 937-1.144 € in P1 e P2 (ricerca/32), 1.011-1.060 € in P3 (ricerca/33); GPU 686-775 € in P1 e P2, 686-893 € in P3, che come estremo alto usa il prezzo della RTX PRO 2000 Blackwell [verificato: ricerca/32 §6; ricerca/33 §4.2].
7. **RAM a pezzi.** La P3 mette "0-400 €" per 4 moduli in F5 (da ricerca/33); ricerca/32 dà 272-512 € e avverte che 4 moduli riducono la banda al 69 % [verificato: P3 §10.2; ricerca/33 riga 255; P1 §3.2 su ricerca/32 §2.4].
8. **PBS.** 525-967 € netti nella P1, 382-967 € nella P2 (mescola due fonti), 382-730 € nella P3 [verificato: P1 §8.4; P2 §9.3; P3 §10.2].
9. **Problemi di Hermes.** La P1 cita 273 problemi aperti, il numero del giorno prima; oggi sono 276 [verificato: P1 §1; API GitHub, 25/10/2026].
10. **Azure.** Il "-15 € al mese dopo Azure" di tutte e tre presume circa 150 € di Azure, un costo che non è nei file [verificato: P2 §9.1, che lo segnala].
11. **Crediti API.** Tutte e tre mettono le API nei crediti del bundle. Gli 800 $ al mese non erano confermati [verificato: ricerca/21-giudizio-ceo §3, su ricerca/14 §1.4]. Il rischio è + 195,65 € al mese per tutte.
12. **Tempo al valore della P1.** Il rapporto 26 prevede un debrief su stage alla settimana 1 e il post-call con la carta alla settimana 2, con una chiave diretta e un tetto nella Console [verificato: ricerca/26 §10.3]. La P1 non usa questa strada e mette 25 gp di fondamenta prima del pilota [verificato: P1 §7.2].
13. **"Hermes vince sul tempo al primo valore"** (P2 §11). Il pilota della P2 si misura alla settimana 11, come quello della P1, e il valore dalla prima settimana lo dà solo la P3 [verificato: P2 §8.1 e §10.3; P1 §7.4; P3 §9].

---

## 7. Perché questi punteggi

### P1 · Agent SDK (42)
- **Pro.** La base tecnica migliore: identità della persona fino all'MCP RAG, Cancello agganciato in modo nativo con `defer`, nessuno strumento che invia, uscita verso Hermes già prezzata [verificato: P1 §1, §5.1, §10; intestazioni MCP verificate oggi]. Copertura completa e onesta, con la stima più prudente degli agenti.
- **Contro per Alessandro.** 25 gp prima del pilota, post-call automatico a fine fase B (settimana 16), 218 gp di base. Chiede 192 GB di RAM prima della fase C e propone tre VLAN nuove (25, 32, 35) [verificato: P1 §2, §3.2, §7.2].

### P2 · Hermes (34)
- **Pro.** Canali, profili, kanban e skill che migliorano sono pronti; il primo bot arriva in giorni [verificato: P2 "In breve"; stima di ricerca/27 §9.5].
- **Contro.** Il gateway unico ha 276 problemi aperti, 9 di sicurezza, 0 risolti [verificato: API GitHub, 25/10/2026]. L'identità verso l'MCP RAG vale per istanza, non per persona [verificato: P2 §3.3]. In Buzz Hermes approva da solo ogni permesso [verificato: P2 §5.3]. Manutenzione 2-3 gp al mese con release poco documentate e la regola dei 14 giorni [verificato: P2 §8.2 e §10.1]. Va contro la preferenza scritta di Michele. I dati rossi restano fuori da Hermes finché non esce la v0.23 [verificato: P2 §10.3]. Per un CEO è il rischio più alto di perdere settimane in correzioni.

### P3 · Claude Team e MCP (45)
- **Pro.** Valore dalla prima settimana con ciò che SerSan paga già; la fase P0 non chiede nulla al server [verificato: P3 §9]. È il disegno del board: "Claude Team ragiona sul RAG via MCP" e "endpoint MCP per Claude Team" dietro Pangolin [verificato: board-testo-completo.txt righe 17-18 e 39-40]. Meno pezzi sempre accesi, motore Agent SDK solo per 10 agenti, punto di arresto dopo P2 [verificato: P3 §5 e §11].
- **Contro.** Dipende da funzioni in anteprima o in beta [verificato oggi: routines in "research preview"]. Porta pezzi di documenti a Claude Team, che non ha log di audit né conservazione personalizzata [verificato: claude.com/pricing/team]. Gli endpoint MCP devono essere raggiungibili dai server di Anthropic [verificato: P3 §3.4]. Alcuni agenti diventano skill usate a mano (§1). La RAM è contata stretta (§6).

---

## 8. Il mio dissenso più forte

**Il collo di bottiglia commerciale non è l'orchestratore.** Oggi SersanOutreach ha 11 lead, 0 meeting e 0 vinti; nessuna mailbox è live e la campagna è ferma dal 09/09/2026 per una deroga di compliance non valida [verificato: ricerca/01 righe 15-18]. Le tre proposte chiedono 191-290 gp e 42-43 settimane, contro le 24 settimane della presentazione [verificato: PRESENTAZIONE-CEO.md §11]. Nessuna mette fra i criteri delle prime quattro settimane la decisione D0 sull'email e una mailbox live. Solo la P1 mette in fase A il debito di sicurezza di SersanOutreach (4 gp di Mattia); la P3 no [verificato: P1 §7.3; P3 §9].

**Cosa chiederei ai CEO di approvare oggi.** Solo P0 e P1 della Proposta 3: 11 settimane, 41 gp di base (54,5 con la riserva) [verificato: P3 §9]. La fase P2 parte solo se alla verifica valgono anche tre criteri commerciali: email live dopo la decisione D0, almeno 8 post dei founder pubblicati, follow-up di tutte le call entro 24 ore [criteri: PRESENTAZIONE-CEO.md §11; il resto non verificato: proposta mia]. Andrea e la pipeline pesata partono solo con lead vere, come già scritto nella presentazione.

**Un secondo dissenso, verso chi premierà la P1 per completezza.** La copertura finale è la stessa nelle tre proposte: cambia l'ordine. La P1 spende 25 gp prima di dare un valore che Alessandro possa usare con un cliente [verificato: P1 §7.2-7.3]. Il motore della P1 è giusto; il suo calendario no.

---

## 9. Cosa va corretto nella Proposta 3

1. **RAM.** Rifare il conto con listmonk, DocuSeal, fatturazione e Postiz (circa 5 GB in più). Mettere in budget i 192 GB (816-1.218 €) come spesa prevista con una data di controllo, per esempio prima di P4, invece di "probabilmente evitabile" [verificato: P3 §3.3 e §10.2; P1 §3.2].
2. **Nessun agente declassato.** I dieci agenti "T" vanno scritti anche come profili del registro che ricevono lavoro dalla bacheca, con una sessione Agent SDK quando il lavoro arriva da un altro agente. Copywriter, Video, Grafiche e Pubblicatore devono poter "parlare" con Marketing e Outreach (J7) e stare in organigramma (G9). Nella tabella di copertura la prima colonna deve dire il componente previsto e la fase, non "No".
3. **Il funnel nelle prime quattro settimane.** Aggiungere alla P0 la decisione D0 sull'email con il legale e la mailbox live, e il debito di sicurezza di SersanOutreach (MFA, backup fuori sede), circa 4 gp come nella P1 [verificato: P1 §7.3; ricerca/01 riga 21].
4. **Verifica alla settimana 8, non 11.** Con criteri commerciali e tecnici, come prometteva la presentazione. Se il post-call automatico non è pronto, alla settimana 8 si misura il post-call fatto in Claude Team con il connettore M365 [verificato: PRESENTAZIONE-CEO.md §11; P3 §3.1 e §4].
5. **Identità per persona anche per gli agenti SDK.** Il motore deve passare all'MCP RAG un token firmato con la persona per cui lavora, come la P1 [verificato: intestazioni MCP dell'Agent SDK, code.claude.com, 25/10/2026; P1 §4.2].
6. **Costo strutturale di Claude Team.** Scrivere ai CEO che la P3 rende quasi obbligatori i 5 posti premium a fine bundle (446,70 € al mese) e mostrare lo scenario con 2 premium e 2 standard (214,42 €). Chiedere ad Anthropic il prezzo dei crediti d'uso oltre il limite e se i 500 $ in comune valgono dietro LiteLLM [verificato: P3 §10.1 e §12; claude.com/pricing/team].
7. **Niente processi aziendali sui compiti programmati di Claude Team.** Sono in anteprima, di un solo account e agiscono a nome della persona [verificato: code.claude.com/docs/en/routines, 25/10/2026]. Tutto ciò che è a orario resta in n8n; i compiti personali solo per uso individuale.
8. **Dati rossi prima di P2.** Il parere legale deve decidere cosa l'MCP RAG dà a Claude Team prima che entrino i documenti dei clienti; scrivere anche il costo di un eventuale passaggio a Enterprise se un cliente chiede i log di audit (prezzo da chiedere) [verificato: P3 §11].
9. **Numeri da allineare.** Calendario 34-42 settimane; VPS da 5,99 € (Cost-Optimized) o 6,49 € (Regular Performance) [verificato: hetzner.com/cloud, 25/10/2026]; RAM a 4 moduli 272-512 € con la banda al 69 %; una sola ipotesi per la corrente della seconda GPU.

## 10. Cosa prendere dalle altre due

- **Dalla P1:** il motore (runner, registro, ponte verso il Cancello con `defer`, isolamento per famiglia), la stima prudente per agente, la tabella delle classi d'azione, l'uscita verso Hermes già prezzata [verificato: P1 §4.3, §5.2, §10].
- **Dalla P1, rapporto 26:** un debrief e un post-call su stage con una chiave diretta e un tetto nella Console già nelle settimane 3-6, prima del "posto agenti" [verificato: ricerca/26 §10.3].
- **Dalla P2:** i criteri di uscita misurabili e le quattro condizioni per riprendere Hermes in futuro (v0.23, righe di sicurezza chiuse, bug dei documenti chiuso, 10 scenari) [verificato: P2 §10.3]. Hermes resta un pilota confinato in Experimental-2, 6-8 gp, solo se un giorno serve [verificato: ricerca/27 §11].

---

## Fonti

**File del progetto** (letti il 25/10/2026)
- `ricerca/34-proposta-1-agent-sdk.md`, `34-proposta-2-hermes-self-hosted.md`, `34-proposta-3-claude-team-e-mcp.md` (per intero)
- `allegati/infra/board-testo-completo.txt`, `board-vlan.txt`
- `ricerca/00-visione-funzionalita.md`, `01-sersanoutreach.md` (righe 15-21), `21-giudizio-ceo.md`, `26-claude-agent-sdk.md` (§10), `27-hermes-self-hosted.md` (§1, §10-11), `32-hardware-e-upgrade.md` e `33-costi-v2.md` (per i prezzi)
- `PRESENTAZIONE-CEO.md` (§11)

**Pagine web** (lette il 25/10/2026)
- https://claude.com/pricing/team
- https://code.claude.com/docs/en/routines
- https://code.claude.com/docs/en/claude-projects
- https://code.claude.com/docs/en/agent-sdk/mcp
- https://api.github.com/repos/NousResearch/hermes-agent/releases
- https://api.github.com/repos/NousResearch/hermes-agent/issues/143547
- https://www.hetzner.com/cloud/
