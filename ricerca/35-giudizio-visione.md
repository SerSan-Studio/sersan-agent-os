# 35 · Giudizio delle tre proposte: la lente della visione

**Data:** 25/10/2026. **Per:** Alberto Tuveri.
**Lente:** quella di Alberto. Conta quanto ogni proposta realizza l'idea intera: le 90 voci A1-L12 di `00-visione-funzionalita.md`, le squadre di agenti che si parlano, la chat di gruppo "come Buzz" collegata a Slack, Telegram e WhatsApp. Più funzioni automatizzate è meglio. Una proposta che toglie o declassa funzioni o integrazioni perde punti sulla visione, anche se così diventa più semplice.
**Proposte giudicate, lette per intero:**
- P1 · `34-proposta-1-agent-sdk.md`: motore nostro sull'Agent SDK di Claude.
- P2 · `34-proposta-2-hermes-self-hosted.md`: Hermes Agent in sei istanze sul DL380.
- P3 · `34-proposta-3-claude-team-e-mcp.md`: Claude Team al centro, connettori MCP, n8n e un motore leggero.

**Vincolo:** il board di Michele (`allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`), letto per intero.
**Altre fonti:** `21-giudizio-visione.md`, `27-hermes-self-hosted.md` (§1, §5, §6), `28-chat-di-gruppo-self-hosted.md` (§1, §8, §9), `32` e `33` per i numeri; pagine ufficiali lette oggi (§4). Context7 oggi risponde "Monthly quota reached": la documentazione l'ho letta direttamente sulle pagine ufficiali [verificato: risposta di Context7 del 25/10/2026].
**Etichette:** [verificato: fonte] = controllato oggi sulla fonte indicata. [non verificato] = stima, calcolo o giudizio mio. gp = giorni-persona. Prezzi IVA esclusa, rilevati il 24-25/10/2026 come nelle proposte.

---

## In breve

**Per la lente della visione vince la P1, il motore sull'Agent SDK: 43 punti su 60.** La P3 segue con 41, la P2 chiude con 35 [non verificato: giudizio].

- La P1 è l'unica che porta tutte le 57 figure su un solo motore, con una sola bacheca, una sola memoria e una sola Porta per Teams, Telegram, WhatsApp e Slack. Ogni agente lavora con l'identità della persona per cui lavora. Tutte le 90 voci hanno un componente.
- La P2 ha pronte le funzioni più vicine all'idea (kanban, profili con persona, skill che crescono, canali). Ma nel board le spezza: sei istanze separate, chat di gruppo di Hermes spente, dati rossi fuori da Hermes, identità per istanza. E poggia su un gateway con 276 problemi aperti.
- La P3 dà valore prima di tutte, ma declassa: 39 delle 57 figure diventano flussi fissi o skill che una persona apre da sé. Le squadre che si parlano e la chat di gruppo arrivano solo alla settimana 23-28.

Il limite della P1 per questa lente: il cuore multi-canale arriva tardi. Telegram alla settimana 28-31, WhatsApp alla 32-38, Slack e Buzz alla 39-43. Va corretto (§8).

---

## 1. Punteggi (0-10, totale su 60)

| Proposta | Visione | Tempo al valore | Costo | Affidabilità e manutenzione | Sicurezza e privacy | Aderenza al board | **Totale** | Verdetto |
|---|---|---|---|---|---|---|---|---|
| **P1 Agent SDK** | **9** | 6 | 6 | 7 | 8 | 7 | **43** | vincitrice, con le correzioni del §8 |
| P3 Claude Team e MCP | 5 | **9** | **7** | 6 | 6 | **8** | 41 | ottima come fase zero, non come architettura |
| P2 Hermes | 8 | 7 | 6 | 4 | 5 | 5 | 35 | ricca sulla carta, fragile nel board |

[non verificato: giudizio mio, motivato nel §3]

---

## 2. Il cuore dell'idea: quando arriva e quanto è automatico

Settimane e fasi come le scrive ogni proposta. Tutte le stime di calendario sono [non verificato: piani delle proposte].

| Pezzo del cuore | P1 | P2 | P3 |
|---|---|---|---|
| Agenti che lavorano da soli con strumenti | 57 profili sul motore SDK [verificato: P1 §5.2] | 50 profili Hermes e 7 servizi [verificato: P2 §6, conteggio rifatto, torna] | 9 agenti SDK (10 con il deck), 29 lavori n8n a schema, 10 skill usate da una persona, 9 servizi [verificato: P3 §5] |
| Prima chat con gli agenti in Teams, carte sul telefono | fase B, sett. 6-16 | H1, sett. 5-11 | P1, sett. 5-11 (chat 1:1 e carte) |
| Squadre che si passano il lavoro (J4) | bacheca in C, sett. 17-27 | kanban dentro l'istanza da H1-H2; fra istanze in H3, sett. 21-23 | bacheca in P3, sett. 23-28 |
| Passaggi visibili a noi (A7) | tutti, nel canale "Agenti" (specchio in D, sett. 28-31) | solo quelli fra istanze finiscono in `#agenti` [verificato: P2 §5.2] | tutti, nel canale "Agenti", da P3 |
| Agenti come membri con nome in Teams | un bot che firma col nome dell'agente; 9 bot di squadra solo "se le persone vogliono" [verificato: P1 §5.5] | un bot per istanza (5 più il Cancello) [verificato: P2 §3.3] | un bot "Agenti SerSan" col nome dell'agente [verificato: P3 §8 B] |
| Telegram | D, sett. 28-31 | H3, sett. 21-23 | P3, sett. 23-28 |
| WhatsApp | E, sett. 32-38 | H4, sett. 24-30 | P4, sett. 29-36 |
| Slack | F, sett. 39-43 | H5, sett. 31-34 | P5, sett. 37-42 |
| Buzz (pilota in LAB) | F, sett. 39-43 | H5, sett. 31-34 | P5, sett. 37-42 |
| Identità della persona verso la memoria | per persona, anche per gli agenti | per istanza | per persona in Claude Team |
| Agenti che imparano (A6) | revisore settimanale che propone PR | Hermes scrive e cura le skill, poi PR | "in parte", revisore in P3 |
| Sessioni di agenti insieme | fino a 16 nei 20 GB del motore | 3-4 lavori per istanza | al massimo 6 |
| Copertura dichiarata delle 90 voci | 90 con componente | 90 con componente | da sola 59 sì, 24 in parte, 7 no; 90 con le aggiunte A-G |

**Lettura.** La P2 porta il cuore prima, la P1 lo porta più intero, la P3 lo porta più tardi e più povero [non verificato: giudizio].

---

## 3. Perché questi voti

### 3.1 P1, motore sull'Agent SDK: 43

**Visione 9.**
- Tutte le 90 voci hanno un componente e una fase. Le lacune sono scritte come necessità con costo: operatore telefonico, relay SMTP, eccezioni Telegram, WhatsApp e Slack, RAM e GPU [verificato: P1 §6 e §6.1; tabella ricontata, 90 righe].
- Un solo sistema: un motore, una bacheca con freno ai giri, una memoria, un Cancello. Nessuna barriera fra squadre [verificato: P1 §5.1-5.3].
- Una sola Porta per tutti i canali. Il Chat SDK ha adattatori per Slack, Teams, Google Chat, Discord, Telegram, GitHub, Linear e WhatsApp, licenza MIT [verificato: github.com/vercel/chat, 25/10/2026].
- Ogni server MCP riceve intestazioni HTTP nella configurazione passata a ogni `query()` [verificato: code.claude.com/docs/en/agent-sdk/mcp, 25/10/2026]. Così C6, K4 ed E3 valgono per persona anche quando lavora un agente.
- Perde un punto perché il multi-canale e Buzz arrivano nelle ultime 15 settimane, gli agenti come membri distinti di Teams restano un'opzione, e A6 è solo un revisore settimanale.

**Tempo al valore 6.** Fase A in 5 settimane: un agente di prova che si ferma su una carta e post di marketing su Claude Team. Il pilota vero è alla fine della fase B (sett. 16). Le squadre si parlano dalla fase C. Piano più lungo: 43 settimane, circa 290 gp con la riserva [verificato: P1 §7.2, somme rifatte: 218 di base, 289 con la riserva].

**Costo 6.** Mensile in linea con le altre: circa 14-31 € in più dopo lo spegnimento di Azure, listino a regime circa 483-593 € [verificato: P1 §8, somme rifatte, tornano]. Una tantum più alta e anticipata: +192 GB di RAM (816-1.218 €) già prima della fase C [verificato: P1 §8.4, da ricerca/32 §2.4]. Più giorni delle altre, ma 67 gp sono il contenuto dei 57 agenti, stimato in modo più prudente (§5).

**Affidabilità e manutenzione 7.** Motore piccolo, versione fissata, dieci scenari a ogni aggiornamento, verifica misurabile alla settimana 11, uscita verso Hermes già prezzata [verificato: P1 §7.4, §9, §10]. Rischi veri: l'SDK esce quasi ogni giorno, il codice nostro è conosciuto da poche persone, LiteLLM non inoltra ancora `anthropic-beta` (PR #36736 aperta) [verificato: P1 §9, da ricerca/26].

**Sicurezza e privacy 8.** Nessuno strumento che invia, `propose_action` con `defer` nativo, `dontAsk` con elenco chiuso, VLAN agenti senza internet, identità per persona [verificato: P1 §3.4 e §5.1, da ricerca/26]. Restano i dati rossi verso Claude Team (K4) e gli endpoint pubblici, come nelle altre.

**Aderenza al board 7.** Usa quasi tutto ciò che il board ha già. Chiede però tre VLAN nuove (25, 32, 35), tre VM, MariaDB, la RAM prima della fase C e la seconda GPU prima della fase E, mentre il board la mette in F5 [verificato: P1 §2 e §11; board, roadmap F5]. Risponde alla richiesta di Michele di valutare l'Agent SDK [verificato: messaggio di Michele nel compito].

### 3.2 P3, Claude Team e MCP: 41

**Visione 5.**
- Il conteggio "59 sì, 24 in parte, 7 no" torna sulla tabella [verificato: P3 §7, ricontato voce per voce]. Con le aggiunte A-G copre tutto, e non toglie nessuna voce.
- Ma declassa gli agenti. Solo 9-10 figure su 57 sono agenti con strumenti. Copywriter, Agente video, Agente grafiche, Pubblicatore, Sviluppatori, Intervistatore e Assistente personale diventano skill che una persona apre in Claude Team [verificato: P3 §5]. Non agiscono da soli.
- Claude Team non dà squadre: i compiti programmati appartengono al singolo account, non si condividono, agiscono "as you" e non girano più di una volta l'ora [verificato: code.claude.com/docs/en/routines, 25/10/2026]. I Projects con coordinatore "aren't offered on Team or Enterprise plans yet" [verificato: code.claude.com/docs/en/claude-projects, 25/10/2026].
- Tetto di 6 sessioni insieme. Squadre che si parlano e chat di gruppo solo dalla settimana 23-28.
- Il §11 scrive che "ci si può fermare dopo P2". Dopo P2 mancano J9, A7, Andrea, firma e fatture: è la rinuncia che la regola di Alberto vieta.

**Tempo al valore 9.** P0 dà valore dalla prima settimana, senza server. Recap dopo le call alla settimana 11 [verificato: P3 §9].

**Costo 7.** Usa ciò che si paga già. La RAM in più forse non serve (ma vedi §5, punto 7). 191 gp di base, 254 con la riserva [verificato: P3 §9, somme rifatte, tornano]. Listino circa 525,44 € al mese [verificato: P3 §10.1, 518,95 + 6,49]. A fine bundle i cinque posti premium (446,70 € al mese) diventano indispensabili, perché compiti e sessioni consumano l'uso dei posti [verificato: code.claude.com/docs/en/routines, "draw down subscription usage"].

**Affidabilità e manutenzione 6.** Meno pezzi sempre accesi. Ma i pezzi che fanno la differenza sono in anteprima: i compiti programmati sono "in research preview" [verificato: code.claude.com/docs/en/routines], gli ambienti self-hosted sono in beta [verificato: P3 §2].

**Sicurezza e privacy 6.** OAuth di Entra per persona sui connettori: bene. Ma il piano Team non ha log di audit né conservazione personalizzata, e più dati dell'azienda passano da Claude Team [verificato: P3 §2, da claude.com/pricing/team]. Endpoint MCP pubblici verso gli IP di Anthropic.

**Aderenza al board 8.** È il disegno del board: "Claude Team ragiona sul RAG via MCP" e "endpoint MCP per Claude Team" dietro Pangolin [verificato: board, sezioni Cloud e Accesso]. Restano Vexa, Asterisk, VLAN nuove ed eccezioni come nelle altre.

### 3.3 P2, Hermes in casa: 35

**Visione 8.**
- Ha pronte le funzioni più vicine all'idea: profili con persona, kanban con dispatcher, corsia di revisione e blocco "serve un umano", skill che l'agente scrive, canali [verificato: hermes-agent.nousresearch.com/docs/user-guide/features/kanban, 25/10/2026; P2 §4].
- Ma la kanban è "single-host by design" [verificato: stessa pagina]. Le squadre vivono in sei istanze e si parlano fra istanze solo con un MCP nostro.
- In `#agenti` finiscono solo i passaggi fra istanze [verificato: P2 §5.2]. Il giro email, agenda, brief, proposte sta tutto in `hermes-commerciale` e resta invisibile nel canale: A7 è a metà, ma la riga A7 non lo dice.
- La tabella dei rischi tiene spente le "chat di gruppo ospitate dal gateway" [verificato: P2 §10.1; ricerca/27 §6.3]. La riga J9 della copertura non lo dice.
- L'identità verso l'MCP RAG è un valore fisso o il nome del profilo, "resolved once at connect time" [verificato: hermes-agent.nousresearch.com/docs/user-guide/features/mcp, 25/10/2026].
- I dati rossi restano fuori da Hermes finché non escono la v0.23 e le correzioni di sicurezza [verificato: P2 §10.3]. Amministrazione e finanza lavorano col rosso oscurato.

**Tempo al valore 7.** Primi bot e kanban in H1 (sett. 5-11), squadre collegate in H3 (sett. 21-23), canali prima delle altre [verificato: P2 §8.1, somme rifatte: 151 e 201 per H0-H5, 171 e 227,5 con H6].

**Costo 6.** I 171 gp di base contano il contenuto dei profili a 0,6 gp l'uno. Con la stima della P1 il totale sale verso circa 200 gp [non verificato: mio calcolo, §5 punto 2]. Manutenzione di Hermes 2-3 gp al mese [verificato: P2 §8.2, stima di quel file]. RAM prima di H4.

**Affidabilità e manutenzione 4.** La scheda #143547 conta oggi 276 problemi aperti: 140 rotti, 108 degradati, 9 di sicurezza, 0 risolti su `main`, 39 in revisione in 14 PR [verificato: API GitHub, issue aggiornata il 25/10/2026 alle 14:54 UTC]. Almeno 45 avvisi di sicurezza nel 2026 [verificato: ricerca/27 §7.1]. Sei istanze da aggiornare entro 14 giorni.

**Sicurezza e privacy 5.** Il contenimento è serio: container per confine di fiducia, plugin che blocca in caso di errore, Cancello. Ma il gateway ha 9 problemi di sicurezza aperti, l'identità è per istanza, e in Buzz il ponte risponde da solo "allow_once" e "approvals.mode: manual does not help" [verificato: hermes-agent.nousresearch.com/docs/user-guide/features/acp, 25/10/2026].

**Aderenza al board 5.** Michele ha scritto che se si può evitare Hermes è meglio [verificato: messaggio di Michele nel compito]. Metà delle funzioni di Hermes è già nel board: n8n, LiteLLM, Qdrant, Open WebUI [verificato: ricerca/27, "In breve"]. Sei bot Teams nel tenant. RAM prima di H4.

---

## 4. Verifiche fatte oggi sulle affermazioni che pesano

| Affermazione | Dove | Esito | Fonte |
|---|---|---|---|
| Scheda #143547 di Hermes: 276 problemi, 9 di sicurezza, 0 risolti su `main` | P2 | confermata; la P1 scrive ancora 273 | [verificato: api.github.com/repos/NousResearch/hermes-agent/issues/143547, 25/10/2026] |
| L'Agent SDK passa intestazioni HTTP decise da noi a ogni server MCP | P1 | confermata: campo `headers` nella configurazione di `mcpServers` di ogni `query()` | [verificato: code.claude.com/docs/en/agent-sdk/mcp, 25/10/2026] |
| Hermes manda all'MCP solo un valore fisso o il nome del profilo | P1, P2 | confermata; la documentazione non prevede l'identità di chi scrive | [verificato: docs MCP di Hermes, 25/10/2026] |
| Kanban di Hermes su un solo host, con dispatcher, revisione, blocco | P2 | confermata; dispatcher ogni 60 secondi dentro il gateway | [verificato: docs kanban di Hermes, 25/10/2026] |
| In Buzz il ponte approva da solo i permessi di Hermes | P2 | confermata | [verificato: docs ACP di Hermes, 25/10/2026] |
| Buzz ha Hermes "come runtime predefinito" | P2 §5.3 | imprecisa: la pagina dice "preset runtime" | [verificato: docs ACP di Hermes, 25/10/2026] |
| Chat SDK con adattatori Teams, Telegram, WhatsApp, Slack, licenza MIT | P1, P3 | confermata | [verificato: github.com/vercel/chat, 25/10/2026] |
| Compiti programmati: per singolo account, non condivisi, "as you", non più di una volta l'ora, in anteprima | P3 | confermata | [verificato: code.claude.com/docs/en/routines, 25/10/2026] |
| Projects non offerti sul piano Team | P3 | confermata | [verificato: code.claude.com/docs/en/claude-projects, 25/10/2026] |
| Posti premium: 446,70 € al mese per 5, 357,36 per 4, 214,42 per 2 premium e 2 standard | P3 | i conti tornano con 100 $ e 20 $ a posto e 1 $ = 0,8934 € | [non verificato: mio ricalcolo sui prezzi citati in P3 §2] |
| Somme dei giorni e dei costi mensili | tutte | tornano, salvo arrotondamenti di 0,25 gp nella P1 (fase B 51,25 scritta 51; fase D 19,75 scritta 20) | [non verificato: mio ricalcolo] |

---

## 5. Numeri che non tornano

1. **Hermes, problemi aperti.** La P1 scrive 273 (dato del 24/10 in ricerca/27). Oggi sono 276, con 140 rotti e 108 degradati [verificato: API GitHub, 25/10/2026 14:54 UTC].
2. **Giorni non confrontabili.** La P1 conta 67 gp per il contenuto dei 57 agenti (0,5-2 gp l'uno). La P2 conta 0,6 gp a profilo, circa 28 gp in tutto. La P3 circa 1 gp ad agente. Con la stima della P1 la P2 salirebbe da 171 a circa 200 gp di base [non verificato: mio calcolo]. Il confronto 218, 171, 191 non dice quale motore costa meno.
3. **Corrente della seconda GPU.** La P1 usa 6,39-17,89 € al mese (25-70 W, ricerca/33). La P2 usa 2,55-7,66 € (10-30 W, ricerca/32). Stessa scheda, due cifre [verificato: ricerca/32 riga 348; ricerca/33 riga 119].
4. **Prezzi di GPU e UPS.** P1 e P2: GPU 686-775 € netti, UPS 937-1.144 €. P3: GPU 686-893 €, UPS 1.011-1.060 € [verificato: le tre proposte, §costi].
5. **VPS per Pangolin.** P1 e P2 scrivono "da 5,99 €"; P3 "da 6,49 €"; la P1 usa 6,49 nelle tabelle dei costi [verificato: le tre proposte].
6. **P3, fine del bundle.** La forbice 550,67-557,16 € usa per Andrea solo il piano a consumo (90,43 €). Con il piano PRO (44,24 €) il minimo è circa 504,48 € [non verificato: mio calcolo, 13,54 + 44,24 + 446,70].
7. **P3, margine di RAM.** Il conto "da +3 a +12 GB" non mette listmonk, DocuSeal, lo strumento di fatturazione ed eventualmente Postiz, che la P1 stima in circa 5 GB. Con quei servizi il margine scende a circa da -2 a +9 GB [non verificato: mio calcolo su P1 §3.2 e P3 §3.3]. "La RAM in più non serve" è quindi ottimistico.
8. **P2, costo mensile "≈14 €".** Non conta la corrente dei 12 moduli di RAM (6,39-10,22 €), che la stessa P2 chiede prima di H4, né il VPS. La P1 li conta. Non è sbagliato, ma non è confrontabile.

---

## 6. Vincitore per la lente della visione

**P1, il motore sull'Agent SDK.** È la sola delle tre che tiene insieme tutto ciò che Alberto mette al centro:
- un solo sistema multi-agente, senza muri fra squadre (J1, J4);
- tutti i 57 agenti come agenti veri, con strumenti e sessioni, e spazio per arrivare a cento (G9);
- la chat condivisa fra agenti leggibile da noi per intero (A7);
- una sola Porta verso Teams, Telegram, WhatsApp e Slack, più Buzz in pilota (J9);
- l'identità della persona fino alla memoria, anche quando lavora un agente (C6, K4, E3).

Vince di 2 punti sulla P3 e di 8 sulla P2 [non verificato: giudizio]. Vince solo se corregge i tempi del cuore multi-canale (§8).

---

## 7. Il mio dissenso più forte

**Contro la P3, e contro chi la sceglierebbe perché "più semplice".** Il suo "giudizio onesto" è giusto sul valore subito. Ma i conteggi la fanno sembrare più vicina all'idea di quanto sia. Chiamare "agente" una skill che una persona deve aprire, o un flusso n8n a schema, vuol dire contare come automatico ciò che non agisce da solo. Su 57 figure gli agenti veri sono 9-10. E la frase "ci si può fermare dopo P2 con il nucleo completo" è proprio la rinuncia che la regola di Alberto vieta: dopo P2 mancano la chat di gruppo, la stanza degli agenti, Andrea, la firma e le fatture. Il rischio concreto è fermarsi a un ottimo assistente per quattro persone, senza il sistema multi-agente.

**Contro il mio stesso giudizio del 24/10.** Nel rapporto 21 avevo dato vincente Hermes. Oggi cambio idea. Hermes porta pronte proprio le funzioni della visione, ma nel board di Michele le spezza: kanban su un solo host, chat di gruppo del gateway spente, identità per istanza, dati rossi esclusi, 276 problemi aperti sul gateway unico. Le sue funzioni migliori vanno prese come modello per la bacheca della P1 (§9), non come motore.

---

## 8. Cosa va corretto nella P1

1. **Anticipare le squadre che si parlano.** Bacheca e freno (3 gp) e specchio nel canale "Agenti" dalla fase C-D alla fase B, così il pilota mostra già J4 e A7.
2. **Anticipare i canali.** Telegram (0,75 gp) e il ponte Slack (1,5 gp) vanno in fase C, non in D e F. Lo stesso codice del Chat SDK lo permette. WhatsApp resta legato alla verifica Meta, ma la richiesta va fatta in fase B.
3. **Agenti come membri con nome.** I 9 bot di squadra in Teams (o un'identità per agente) diventano una consegna con giorni e fase, non un'opzione "se le persone vogliono".
4. **Buzz con un'uscita dal LAB.** Scrivere i criteri per portarlo fuori dal LAB (issue #7375 chiusa, nessuna approvazione automatica) e il lavoro per collegarlo alla stessa bacheca, con i giorni. Altrimenti "come Buzz" resta un pilota senza seguito.
5. **Agenti che imparano (A6).** Oltre al revisore settimanale, gli agenti scrivono le proposte di skill in una cartella "proposte", come fa Hermes, e una persona le approva con una PR. Con i giorni.
6. **Aggiornare Hermes.** 276 problemi, 140 rotti, 108 degradati, 9 di sicurezza, 0 risolti su `main` al 25/10/2026 alle 14:54 UTC.
7. **Allineare i numeri.** Corrente della seconda GPU (ricerca/32 o ricerca/33, con il motivo), prezzo del VPS (5,99 o 6,49 €).
8. **Dire che i giorni non sono confrontabili.** I 67 gp per il contenuto degli agenti sono una scelta prudente che le altre proposte non fanno. I CEO non devono leggere 218 contro 171 come costo del motore.
9. **RAM come decisione con data.** In fase C-D restano circa 3 GB. L'acquisto di +192 GB (816-1.218 € IVA esclusa, prezzi del 25/10/2026) va chiesto ai CEO con una data, prima della fase C.
10. **Valore subito più largo.** Portare dentro la fase A la P0 della P3: progetti condivisi per squadra e skill dell'organizzazione in Claude Team, con i giorni (circa 6,5 gp), non solo le skill di marketing (2 gp).

---

## 9. Cosa prendere dalle altre due

**Dalla P2 (Hermes), come modello per la bacheca della P1:**
- corsia di revisione fra agenti prima della carta del Cancello;
- blocco "serve un umano" con sblocco dalla chat;
- blocco automatico dopo 2 fallimenti di fila e rifiuto dei cicli di dipendenze;
- dispatcher che riprende i compiti fermi.
[verificato: docs kanban di Hermes, 25/10/2026]

**Dalla P2, per la rete:** le regole "Bypass Auth" di Pangolin solo per percorso e la regola CIDR sugli IP di Anthropic per l'MCP RAG [verificato: P2 §3.4, da docs.pangolin.net].

**Dalla P3:**
- la fase P0 su Claude Team, che dà valore senza server;
- l'idea di Claude Team come "finestra" delle persone, con la memoria e il Cancello sul server;
- i connettori MCP con OAuth di Entra per persona, che servono anche alla P1 per K4.
[verificato: P3 §1, §4, §9]
