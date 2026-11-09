# 21 · Giudizio del CPTO sulle sette proposte

**Data:** 24/10/2026. **Lente:** quella di Michele Sanna, CPTO: affidabilità, manutenzione con 2-3 ingegneri, codice nuovo, dipendenze fragili, osservabilità, cambi dei fornitori, uso del server comprato. **Fonti:** proposte 20-A…G e rapporti 00-18. Le stime senza fonte sono [non verificato] e le correggo al ribasso.

## 1. Punteggi (0-10 per criterio, totale su 60)

| Proposta | Copertura A1-I4 | Tempo al valore | Costo | Affidabilità e manutenzione | Sicurezza e privacy | Indipendenza | Totale |
|---|---|---|---|---|---|---|---|
| **A Hermes + Cancello** | 8 | 6 | 7 | 5 | 7 | 8 | **41** |
| E Claude-native | 8 | 4 | 5 | 6 | 8 | 6 | 37 |
| F Paperclip | 8 | 6 | 6 | 4 | 5 | 7 | 36 |
| G Ibrido | 9 | 6 | 6 | 3 | 5 | 7 | 36 |
| B buzz | 7 | 5 | 6 | 3 | 6 | 8 | 35 |
| C Grok Bot | 7 | 8 | 5 | 4 | 3 | 3 | 30 |
| D OpenAI Dots | 5 | 7 | 4 | 4 | 4 | 3 | 27 |

## 2. Vincitore: A, con correzioni

**Perché vince.**
- **Il percorso critico è codice nostro e piccolo.** Cancello, memoria e ingresso stanno fuori da Hermes, che non ha strumenti d'invio [verificato: 10 §4.2]. Se Hermes delude si cambia l'orchestratore e si tiene il resto. È l'unica proposta con un punto di decisione datato e un'uscita prezzata (runner Agent SDK, 10-15 gg-p [non verificato]).
- **Meno codice d'impianto.** Profili, kanban, cron, Slack in Socket Mode, client MCP e skill esistono già [verificato: 10 §4.1-4.2]. Gli MCP di SersanOutreach girano come processi figli stdio sullo stesso server: niente involucro HTTP + OAuth, che le altre proposte devono scrivere [verificato: 01 §5.1, §5.10].
- **Indipendenza.** MIT, qualunque modello, riserva ospitata a Londra [verificato: 10 §1; 18 §2.4].
- **Server usato bene.** La GPU fa embedding, trascrizione e giudice [verificato: 13 §8]; i modelli di frontiera passano dall'API, perché Hermes vuole almeno 64k di contesto [verificato: 10 §4.3].

**Cosa non credo della proposta A.**
- **Il Cancello in 5 gg-p è ottimistico.** Vanno scritti ruoli per approvatore, carte in Slack, esecutori per Gmail, Slack e SersanOutreach: E stima 9 + 4 + 6 gg-p. La fase 1 vale circa 20 gg-p, non 12; primo rilascio alla settimana 6-7 [non verificato: stima mia].
- **Hermes è il pezzo meno stabile.** Ha avuto 5 patch in 10 giorni e ha oltre 5.000 issue aperte. Ha bug con più profili sullo stesso gateway (sessioni al profilo sbagliato) e più CVE nel 2026 [verificato: 10 §3, §6]. È "single-tenant": niente permessi diversi per persona [verificato: 10 §5].

## 3. Perché non le altre

- **E** è la più solida su sicurezza e osservabilità, e la più onesta. Chiede però 15-22 mila righe nuove e 119 gg-p a due persone che portano già SersanOutreach, oggi NOT READY su tutti e quattro i verdetti [verificato: 01 §0]. La chat fra agenti arriva alla settimana 13.
- **F** dà pronta la governance (organigramma, budget con stop, approvazioni con argomenti firmati). In cambio porta 488.000 righe che non leggeremo e 6 advisory critici nel 2026, tra cui una RCE senza autenticazione e un agente che ha mandato email vere. Ha default pericolosi e rilasci con breaking change [verificato: 20-F §5, §8]. Il cervello resta da costruire.
- **G** copre di più sulla carta, ma somma i rischi di Paperclip, Hermes e n8n: cinque componenti open source e otto servizi per una persona. Non cita gli advisory di Paperclip.
- **B** sostituisce Slack con un prodotto pre-1.0: se buzz si ferma, si ferma la chat del team. Le lacune bloccanti si chiudono con un fork di `buzz-acp` da mantenere. L'avvio senza desktop su Linux non è documentato [verificato: 17 §0, §7].
- **C** porta dati "gialli" negli USA su una beta chiusa, senza audit fuori da Enterprise. Il modello è invisibile e la quota non è pubblicata; i piani sono cambiati tre volte in due mesi [verificato: 11 §4, §7]. Restringe ai dati rossi la regola 7 di 16, che non lo dice.
- **D** poggia su Dots (uscito il 29/09) e su Workspace Agents non confermati in UK. Il prezzo dei crediti è ignoto e la pausa non ferma i task pianificati [verificato: 18 §2.2]. Scrive insieme "i dati restano in casa" e "i dati operativi vanno negli USA".

## 4. Cosa innestare in A

1. **Da E, due classi di lavoro.** Riassunti, estrazioni e classificazioni vanno con chiamate dirette alla Messages API con JSON a schema, fuori da Hermes; Hermes fa solo i lavori a più passi. Cala la superficie esposta e l'uscita verso l'Agent SDK resta in esercizio.
2. **Da E, porta dei modelli e conto API realistico.** Un proxy aggiunge la chiave, conta e ferma per agente. Le API si stimano con sessioni e cache (195 € nel consigliato), non con 14 × 1,5. Va provato che Hermes accetti un indirizzo Anthropic diverso [non verificato].
3. **Da E, ruoli per classe di carta.** Alessandro approva outbound e mail ai clienti, Michele offerte e affermazioni tecniche, Alberto infrastruttura e codice.
4. **Da G, istanze Hermes separate dove i permessi cambiano**, per esempio la finanza [verificato: 10 §5].
5. **Da B, la corsia d'ingresso.** Chi legge mail e trascrizioni non ha strumenti d'azione e passa avanti solo campi strutturati.
6. **Da C e D, valore nelle prime due settimane.** Mentre si monta il server, i profili girano su Hermes Cloud (Londra) con dati pubblici o interni non personali [verificato: 18 §2.4]. Il DPA non è stato trovato: niente dati di clienti.
7. **Da F, la via UE.** I profili con dati dei clienti possono usare Claude via Bedrock con inferenza UE, se il costo regge [verificato: 16 §5; costo non trovato].
8. **Da G, una riserva del 30 % su tutte le stime.**

## 5. Condizioni prima di collegare gli agenti

- **Debito di SersanOutreach** [verificato: 01 §6]: identità firmata in `enforce`, MFA (oggi 0 iscritti su 7 account staff), backup fuori sede, alert provati fino a una persona. Senza questi, gli agenti scrivono in un CRM che non sappiamo ripristinare.
- **Crediti API.** Va letto nella Console se sono 800 $ al mese, 1.000 $ una tantum o 500 $ in comune [verificato: 14 §1.4].
- **Volume.** Oggi ci sono 11 lead, 0 meeting e 0 vinti [verificato: 01 §0]. Pipeline pesata, coaching e "Andrea" aspettano dati da pesare; prima vengono post-call, debrief, brief e memoria.

## 6. Dissenso più forte

Una volta costruito il Cancello, Hermes aggiunge poco. In cambio porta un runtime Python 3.14 con 58.000 commit, 5.000 issue aperte e note di rilascio incomplete "on purpose", da seguire per anni con due ingegneri [verificato: 10 §3]. Corrette le stime di A, la distanza da E scende a 30-40 gg-p di impianto: Slack, cron, registro degli agenti [non verificato: stima mia]. E dà un solo linguaggio, un solo fornitore di modelli, osservabilità completa e nessuna dipendenza giovane. Se nella prova di due settimane anche un solo contesto finisce al profilo sbagliato, la scelta giusta è E. Conviene saperlo prima di scrivere skill e profili legati a Hermes.
