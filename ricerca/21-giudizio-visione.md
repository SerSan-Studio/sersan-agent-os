# 21 · Giudizio delle sette proposte: la lente della visione

**Data:** 24/10/2026. **Lente:** quella di Alberto: fedeltà completa alla visione (ogni voce A1-I4 fatta davvero), potenza, chat condivisa fra agenti e persone, crescita a 100 agenti; il budget per gli abbonamenti c'è. **Fonti:** rapporti 00-18 e proposte 20-A…G, tutti presenti. **Etichette:** [verificato: fonte], [non verificato].

## 1. Punteggi (0-10, totale su 60)

| Proposta | Copertura | Tempo | Costo | Affidabilità | Sicurezza | Indipendenza | Totale |
|---|---|---|---|---|---|---|---|
| **A Hermes** | 8 | 6 | 7 | 5 | 7 | 8 | **41** |
| F Paperclip | 8 | 6 | 6 | 4 | 5 | 8 | 37 |
| G Ibrido | 9 | 6 | 7 | 3 | 5 | 7 | 37 |
| B buzz | 7 | 5 | 7 | 3 | 6 | 8 | 36 |
| E Claude-native | 7 | 3 | 6 | 5 | 8 | 5 | 34 |
| C Grok Bot | 6 | 7 | 4 | 5 | 3 | 2 | 27 |
| D OpenAI Dots | 5 | 6 | 4 | 4 | 4 | 3 | 26 |

**Costo a parità di perimetro** (stack comune incluso, cassa con bundle e crediti, scenario consigliato): A 759 €, B 723 €, E 749 €, F 873 €, G circa 730 € (i 592 € dichiarati escludono Workspace, Apollo, Higgsfield, Canva), C circa 1.058 €, D circa 1.195 € (la sua tabella esclude Instantly, Apollo, Apify, Metricool, moda, 1Password, UPS) [non verificato: mia normalizzazione su 14§11]. Fra A, B, E, F e G il costo non decide.

## 2. Vincitore: A, Hermes orchestratore con il Cancello

- È lo stack della visione: orchestratore open source in casa, Claude via API, Notion, vettoriale, Slack, CRM. Profili, kanban, cron, delega e skill scritte dall'agente sono pronti [verificato: 10§4.1-4.2]: A4, A5, A6 e C1 sono funzioni, non promesse.
- Cancello, memoria e ingresso stanno fuori da Hermes: se delude si cambia l'orchestratore e si tiene il resto, con decisione a fine fase 1.
- MIT, dati in casa, qualunque modello, riserva ospitata a Londra [verificato: 18§2.4].
- Vince di poco, su sicurezza e indipendenza: F e G danno pronti organigramma e banca dei token.

## 3. Severità sulle stime

- **A.** Cancello in 6,5 gp [non verificato]; E stima lo stesso nucleo in 21 gp. Primo rilascio realistico: settimana 7-8, non 5. A1 dimentica le riunioni fisiche. Il bot smistatore unico toglie agli agenti l'identità visibile in Slack.
- **B.** `request_approval` fallisce, nessun freno, permessi in bypass [verificato: 17§0]; i prompt non arrivano a `claude-agent-acp` (#7375) [verificato: 17§5] e il rimedio è [non verificato]; `buzz-acp` senza desktop non ha guida [non verificato: 17§7].
- **C.** Cloud USA, nessuna esportazione, modello invisibile [verificato: 11§1, §7.1]; cinque incidenti dal 13 al 19/10 [verificato: 11§8]. Il debrief «in due settimane» usa solo dati verdi. I dati gialli su una beta contrastano la regola 7 [verificato: 16§6].
- **D.** Un dot per persona [verificato: 18§2.2]; Workspace Agents in UK non confermati; prezzo del credito OpenAI ignoto; nessun dialogo nativo fra agenti; prodotto con meno di un mese.
- **E.** 119 gp, chat fra agenti alla settimana 13, due terzi delle voci da scrivere.
- **F.** Bypass dei permessi di default, quattro regex inglesi contro le iniezioni, «A mention alone does not assign work»; sei advisory critici [riportato da F, non riverificato]. 18 gp con la messa in sicurezza: ottimistico.
- **G.** Cinque componenti open source e otto servizi per un amministratore; G5 «in abbonamento», ma consenso, RPO e richiamata in 90 s sono codice; costo sottostimato. La riserva del 30 % è la stima più onesta del lotto.
- **Tutte.** Gli 800 $/mese di crediti non sono confermati (forse 1.000 $ una tantum o 500 $ in comune) e il programma startup è chiuso [verificato: 14§1.4]. Le fasi 0 da 6-8 gp ignorano RAM sbilanciata, GPU non qualificata HPE, dischi e UPS da comprare [verificato: 15§0-§1].

## 4. Cosa innestare in A

1. **Da F e G: Paperclip come piano di controllo** oltre i 25 profili: organigramma con `reportsTo`, budget per agente con stop al 100 %, issue. Hermes vi gira come adattatore, il Cancello resta l'unico esecutore. Pilota in `stage` nella fase 4.
2. **Da B: agenti come membri con nome.** Dopo la prova di due settimane, un bot Slack per agente con `allow_bots: "mentions"` [verificato: 10§4.1] e il freno di B (8 messaggi per thread, catene di 3, tetto in $); buzz in pilota come stanza interna senza dati dei clienti.
3. **Da G:** n8n per gli ingressi deterministici, così Hermes esce dal percorso critico; Slack Connect per il canale del cliente (da verificare su Pro); 30 % di riserva; avvio sulla VM Azure se l'hardware tarda.
4. **Da E:** chiamate dirette alla Messages API per riassunti e classificazioni, sessioni solo per brief, offerte e deck; tetti per persona; approvatori per classe.
5. **Da C:** i tre colori dei dati nel Cancello, che decide cosa può uscire verso Hermes Cloud o un SaaS.
6. **Da C, E e G:** riunioni fisiche registrate dal telefono (A1).
7. **Da F:** coaching in issue privata (G3-G4); Claude su Bedrock UE come opzione [verificato: 16§5].
8. **Da D:** follow-up solo verso il dominio del cliente.

## 5. Lacune che nessuna proposta chiude

- **D1.** Zero vinti e 91 deal senza valore [verificato: 01§0]: la pipeline «pesata sullo storico» oggi è una tabella di pesi dichiarati.
- **F1.** La suite di posta in uso non è nota [verificato: 14§5].
- **G5.** La visione prevede la voce clonata di un collega; tutte propongono voce sintetica. La versione fedele chiede un contratto separato e revocabile [verificato: 16§6 regola 6] e una decisione dei CEO, perché i documenti di casa non prevedono un agente vocale [verificato: 05§5.8].
- **G4.** Al responsabile solo aggregati fino al parere legale [verificato: 16§4].

## 6. Dissenso più forte

Doveva vincere G, o F. Hermes si dichiara «a single-tenant personal agent», con bug aperti proprio sui profili multipli [verificato: 10§1, §6], e A lo riduce a smistatore con un solo bot Slack. Così A costruisce a mano i tre pezzi che la lente di Alberto mette al centro: chat visibile fra agenti e persone, organigramma, banca dei token per 100 agenti. Paperclip li dà pronti e ospita Hermes come adattatore; G tiene Hermes dove è forte, l'assistente personale che impara. A vince su sicurezza e indipendenza, i criteri che questa lente pesa meno. Senza l'innesto 1, A si ferma a 25 profili.
