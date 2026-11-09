# 21 · Giudizio di compliance sulle sette proposte

**Data:** 24/10/2026. **Lente:** privacy e sicurezza. **Fonti:** proposte 20-A…G e rapporti 00-18. Il tempo al valore conta il valore *lecito*: sui dati dei clienti solo dopo DPIA e gateway.

## 1. Punteggi (0-10)

| Proposta | Copertura | Tempo | Costo | Affidabilità | Sicurezza e privacy | Indipendenza | Totale |
|---|---|---|---|---|---|---|---|
| **E Claude-native** | 7,5 | 4 | 5,5 | 6,5 | 8 | 6,5 | **38,0** |
| F Paperclip | 8 | 5,5 | 6 | 5 | 5 | 8 | 37,5 |
| A Hermes | 8 | 5 | 6,5 | 5 | 5 | 7,5 | 37,0 |
| B buzz | 7,5 | 5 | 6,5 | 4 | 5,5 | 8 | 36,5 |
| G ibrido | 8,5 | 5 | 6,5 | 4 | 5 | 7,5 | 36,5 |
| C Grok Bot | 7 | 6,5 | 4,5 | 5 | 2,5 | 2,5 | 28,0 |
| D OpenAI | 6 | 5 | 4,5 | 5 | 3,5 | 3 | 27,0 |

## 2. Perché

**E vince, di mezzo punto.** È l'unica in cui i controlli che un cliente regolamentato chiede stanno in codice nostro e si possono mostrare: nessun agente con strumenti d'invio, carta con impronta ricalcolata e una sola esecuzione, corsie trusted/untrusted, utente Linux per lavoro, audit a catena di hash, `forget`, conservazione automatica, registro dei trattamenti legato al codice. Un solo fornitore di modelli, con DPA [verificato: 16 §5]. Limiti: 119 gg-p in 20 settimane. Difetti propri: le carte su Telegram portano il testo delle mail ai clienti; la porta dei modelli con `ANTHROPIC_BASE_URL` è [non verificato].

**F.** Approvazioni imposte dal runtime con argomenti firmati, issue private per il coaching, `hire_agent` come punto della DPIA. Ma il piano di controllo ha 6 advisory critici nel 2026 (RCE senza autenticazione, IDOR fra aziende, un agente che ha mandato email vere), default pericolosi (`dangerouslySkipPermissions`, telemetria accesa, filtro anti-iniezione in regex inglesi) e audit senza catena di hash [non verificato da me: 20-F §5 cita l'API GitHub]. I 18 gg-p del primo rilascio non contano l'indurimento che F stessa dichiara obbligatorio.

**A.** Il Cancello fuori da Hermes è giusto. Ma Hermes è "single-tenant", "all callers are equally trusted", e il solo confine è il sistema operativo [verificato: 10 §5]: non separa i permessi fra le quattro persone, quindi il coaching "solo al venditore" non lo garantisce il sistema. I contesti che si mescolano fra bot [verificato: 10 §6] sono un rischio di riservatezza fra clienti. Nel post-call Hermes scrive in Notion e nel CRM dopo aver letto la trascrizione, senza carta. Il Cancello in 5 giorni: E ne stima 9 per il solo nucleo [verificato: 20-E §6].

**B.** La migliore sulla località: anche la chat resta in casa. Ma buzz parte con permessi in `bypass`, chiave dell'agente nell'ambiente, approvazioni che falliscono, webhook senza firma, telefono con la chiave privata del desktop, client Windows alpha che scrive segreti in chiaro [verificato: 17 §0, §3, §5, §8].

**G.** Copre di più, ma somma le superfici di Paperclip, Hermes, n8n, Claude Tag e Managed Agents, questi fuori da ZDR [verificato: 12 §1]: la DPIA più difficile da spiegare, con tre registri di approvazione.

**C.** Contraddice la regola 7 di 16: "niente dati di clienti o lead su abbonamenti consumer o beta (es. Grok Bot)" [verificato: 16 §6]; i dati "gialli" sono dati di lead. Modello invisibile, un computer condiviso da tutti i Bot, audit solo Enterprise, nessuna esportazione, ogni azione a carico del cliente [verificato: 11 §3, §7]. DPA di Cursor non aperto [non verificato].

**D.** Nessuna residenza UE né audit log su Business [non verificato: fonti terze]. La memoria del dot non si cancella in modo selettivo: la cancellazione chiesta da un interessato non si onora. La fase 1 tratta dati dei clienti prima che il gateway esista. "I dati restano in casa" (§9) contraddice "i dati operativi vanno negli USA".

## 3. Buchi comuni, da chiudere prima di registrare un cliente

1. **Recall.ai e Fireflies** trattano l'audio grezzo, ma regione e DPA non sono verificati [verificato: 14 §4 solo prezzi; 16 §5]. Provare Vexa in casa [verificato: 12 §7].
2. **Cloudflare Tunnel** vede le trascrizioni in chiaro [verificato: 15 §4.3]: va fra i sub-responsabili.
3. **DPIA e test di bilanciamento** prima del post-call: nessun piano li mette in calendario.
4. **SersanOutreach** ha debiti propri: MFA con 0 iscritti, backup fuori sede assente, alert mai provati, `auto_linkedin` che approva DM senza persona, decisioni D0 sull'email aperte [verificato: 01 §6]. Agli agenti solo dopo `enforce`, MFA e un ripristino provato.
5. **Art. 50 contro la regola marketing "mai etichette AI"** [verificato: 05 §5]: nessuna proposta scioglie il conflitto. Andrea si dichiara sempre; per le bozze approvate e inviate da una persona serve il parere legale [non verificato: interpretazione].
6. **Lavoratori:** l'inquadramento di Alberto e Mattia è "non trovato" [verificato: 16 §0]; senza, debrief, mappa F1 e coaching restano senza l'informativa della L. 132/2025.
7. **API Anthropic senza regione UE** [verificato: 16 §5]: chiedere ZDR o usare Bedrock UE per i dati dei clienti, fuori dai crediti, che valgono solo sull'API di prima parte [verificato: 14 §1.4].

## 4. Cosa innestare in E

- Da **F**: Bedrock UE per i dati "rossi"; ogni agente nuovo nasce da un'approvazione con la sua riga nel registro e la DPIA; coaching visibile solo all'interessato, apertura d'emergenza registrata.
- Da **C**: i tre colori dei dati come policy del demone, più severa: il giallo mai su SaaS beta o consumer.
- Da **C** e **D**: nelle settimane 1-4 i CEO usano Claude Team su dati verdi, con connettori in sola lettura.
- Da **B**: si approva solo da un'identità umana autenticata; stanza `#ingresso` letta da agenti senza strumenti.
- Da **D**: destinatari solo del dominio del cliente.
- Da **A**: punto di decisione con criteri d'uscita dopo il pilota.
- Da **G**: 30 % di riserva sulle stime, registro dei trattamenti in fase 0.
- Correzione: su Telegram solo l'avviso "carta in attesa", mai il testo.

## 5. Dissenso più forte

La sicurezza di E è codice nostro mai andato in produzione, scritto da due persone, senza revisione esterna: un cliente regolamentato può fidarsi più di un prodotto usato da migliaia di aziende che di 15-22 mila righe nuove. E arriva tardi: gli agenti che si parlano alla settimana 13, contro le 4-5 di F e A. Se i CEO non lo usano presto (H2), il progetto si ferma prima che i controlli servano. Il Cancello si mette davanti a Paperclip o a Hermes comunque: F più il nucleo di E darebbe gli stessi controlli sugli effetti in circa metà del tempo.
