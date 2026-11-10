# Giudizio «ceo» del terzo giro

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **G-ceo**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Lente del giudice: CEO e commerciale. Ogni criterio ha un voto da 0 a 10. I pesi erano fissati prima del giudizio: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10.

## Voti

| Proposta | Autonomia | Tempo al valore | Costi | Sicurezza essenziale | Server e manutenzione | Rischio | Totale pesato |
|---|---|---|---|---|---|---|---|
| P-A | 8 | 7 | 7 | 9 | 6,5 | 7 | **75,0** |
| P-B | 7,5 | 6 | 7 | 7,5 | 4 | 4 | **64,2** |
| P-C | 8,5 | 7,5 | 6 | 6,5 | 6,5 | 6 | **72,8** |
| P-D | 7,5 | 8 | 7,5 | 8,5 | 7,5 | 6,5 | **76,0** |

## Motivazioni, condizioni e obiezioni

### P-A · Motore Agent SDK con autonomia a livelli

Tiene il motore già deciso e sposta la leva nel Cancello: livelli per classe, finestra L2, retrocessione automatica, eventi dalla fase 1. È la proposta che semplifica meglio lo spec, da 27 a 18 criteri, con tutte e sei le protezioni essenziali [verificato: spec §12-13 per i 27 criteri; il resto è testo di P-A §4 e §7]. Alla settimana 8 i CEO vedono poco più della v2.1: riassunto e debrief partono da soli, la mail resta una carta finché non ci sono 5 sì puliti, i to-do stanno nel riassunto e non in Jira. Alla 21 il salto c'è: CRM e Jira L3, follow-up L2 o L3, posta smistata, pagina aziendale verso L2. Però la fase 2 sale a circa 65 gp e slitta di 1-2 settimane [non verificato: stime di P-A §5.2-5.3; i 58,5 gp della v2.1 sono verificati in PRESENTAZIONE-CEO §15]. Costa come la v2.1, circa 250-254 gp e gli stessi canoni, meno la revisione esterna da 3.560-5.940 € [verificato: PRESENTAZIONE-CEO §12.2]. Rischio contenuto: nessun fornitore nuovo e uscita verso Hermes già prezzata, 26-33 gp [verificato: PRESENTAZIONE-CEO §15]. Autonomia 8: a regime ha i tetti più alti (primo follow-up fino a L3, una carta per campagna nell'outbound, skill interne fino a L3), ma parte più lenta di P-C e P-D.

**Condizioni perché funzioni**

- Il parere legale della settimana 3 deve ammettere L2 e L3 per il follow-up alla persona appena incontrata e fissare il testo della riga AI [verificato: PRESENTAZIONE-CEO §9.4; PRD «Domande aperte»].
- Portare nella fase 1 i to-do in Jira e l'evento in calendario come scritture interne: Jira per gli agenti vale 1,75 gp [verificato: ricerca/36 §7.3]. Senza, alla settimana 8 P-A mostra meno di P-B e P-D.
- I CEO decidono soglie (5 e 15), tetti per classe e orario delle finestre. Con 11 lead e 0 meeting va valutata una partenza diretta a L2 per la classe «persona appena incontrata» [verificato: PRESENTAZIONE-CEO §7.1].
- Confermare con Mattia i 6,5 gp a settimana: altrimenti brief leggero e Agenda escono dalla fase 2 [verificato: ricerca/36 §7.1; PRD «Domande aperte»].
- Postiz prima della F4 solo con il sì di Michele; altrimenti Metricool resta come ponte a 59,86 € al mese [verificato: PRESENTAZIONE-CEO §6.2; ricerca/33, riga Metricool].
- Riaccensione automatica del server e linea di riserva prima del primo L3 esterno a tutte le ore [verificato: DOMANDE-PER-MICHELE n. 22 e 24; PRESENTAZIONE-CEO §13].

**Obiezioni più forti**

- Alla settimana 8 il CEO vede quasi le stesse cose della v2.1, con più giorni: le fasi 0-1 valgono 42,5-44 gp di base contro i 37,5 di P-D [non verificato: stime delle due proposte].
- Con 11 lead, 1 risposta e 0 meeting le promozioni verso l'esterno arrivano tardi: subito autonomo è solo il lavoro interno, e lo ammette la stessa P-A [verificato: PRESENTAZIONE-CEO §7.1; testo di P-A §3.5].
- Tutto il codice del motore resta nostro e mai andato in produzione, su un SDK che cambia quasi ogni giorno [verificato: PRD «Rischi»; PRESENTAZIONE-CEO §13].
- Tiene il ponte `propose_action` e la ripresa delle sessioni dopo la carta: è la parte più delicata dello spec, che P-D toglie del tutto [verificato: spec §2.1, §4.5, §4.11].
- Andrea anticipato alla fase 3 porta la RAM a circa -9 GB e la fase 3 a 82-84 gp [non verificato: stime di P-A §2.2 e §5.2].

### P-B · Orchestratore autonomo pronto, con il nostro Cancello

È la più vicina alla forma del sistema della trascrizione di riferimento: un orchestratore open source su una macchina propria, con agenti che imparano da soli e si passano il lavoro in una chat comune [verificato: TR 3:23-4:30]. Kanban, cron e skill che si riscrivono sono pronti, quindi passaggi fra agenti e apprendimento arrivano prima e senza codice [verificato: ricerca/27 §9.2 e §9.5]. Con la lente del CEO pesa il resto. Hermes non soddisfa le quattro condizioni che il progetto si è dato per usarlo come orchestratore [verificato: ADR-0012 e ricerca/27 §11 per le condizioni; stato al 9/11 dal Rapporto 4 §3.4, non riverificato da me]. Michele preferisce evitarlo [verificato: ricerca/36 §1.2 e §1.4]. La manutenzione è stimata 1,5-2,5 gp al mese e nessuno di noi lo conosce a fondo [verificato: ricerca/27 §8; ricerca/36 §2.1]. Nel secondo giro la stessa strada arrivava al post-call alla settimana 11 [verificato: ricerca/35-giudizio-ceo §2]: la settimana 8 è a rischio. Alla 21 dà meno strumenti di vendita delle altre: brief e offerta sono in fase 3, Andrea in fase 5 [testo di P-B §5.1]. La cassa è quella della v2.1; i giorni di costruzione scendono a 221-230 ma l'esercizio sale. L'uscita verso il motore SDK è ben prezzata, 17,5-21 gp [verificato: ricerca/34-proposta-2 §10.2]. Autonomia 7,5: prima per apprendimento e fedeltà di forma, più indietro per lavoro che esce verso clienti e funnel.

**Condizioni perché funzioni**

- Sì scritto di Michele a rovesciare l'ADR-0012 e ad ammettere Hermes sul server, con un termine per le patch dei contenitori non esposti [verificato: ADR-0012; ricerca/27 §7.2].
- Verifica della settimana 8 senza scambi: in due settimane, con 5 profili, nessun messaggio o risultato al profilo, alla chat o al cliente sbagliato. Se fallisce si passa all'uscita A, 17,5-21 gp e 3-4 settimane [verificato: ricerca/34-proposta-2 §10.2].
- Un solo bot per gateway e clienti mai sugli adattatori di Hermes; coaching e dati personali consegnati dal Cancello in chat 1:1, perché l'identità vale per contenitore [verificato: ricerca/27 §4 e §6.3].
- Alias dei modelli con «claude» in LiteLLM e spesa misurata nella fase 1: senza, la cache dei prompt non parte [verificato: ricerca/27 §3.1].
- Mattia co-manutentore e stage con i 10 scenari a ogni aggiornamento, 2-3 cicli al mese [verificato: ricerca/27 §8].
- Lo sblocco della card dopo la carta va provato prima di contarci [non verificato: «da provare» in ricerca/34-proposta-2 §5.4 punto 6].

**Obiezioni più forti**

- Affidabilità. Al 25/10 la scheda del gateway aveva 276 problemi aperti, 9 di sicurezza e 0 risolti [verificato: ricerca/36 §1.4]. Al 9/11 sono 312 con 83 risolti, e le quattro righe di sicurezza restano aperte [dal Rapporto 4 §3.2, non riverificato da me].
- Un utente terzo che usa Hermes da mesi racconta chat di bot diversi che si mescolano e dice di non potergli lasciare il lavoro senza seguirlo [non verificato: testimonianza di terzi, file «Grokbot vs Hermes.txt»].
- Un'azione L3 con il contesto del cliente sbagliato è il danno commerciale peggiore: il Cancello controlla il destinatario, non il contenuto [non verificato: lettura mia].
- Va contro una decisione registrata e contro la preferenza del CPTO: per i due CEO è la più difficile da approvare [verificato: ADR-0012; DOMANDE-PER-MICHELE «Già recepito»].
- Manutenzione: tre rilasci in quattro giorni a inizio novembre [dal Rapporto 4 §3.1] e 35-45 gp di esercizio contro 29 [non verificato: stima di P-B §5.1; 29 gp verificati in PRESENTAZIONE-CEO §15].
- Incoerenza interna: la tabella dei brief promette L3 alla settimana 21, ma il piano mette brief, slide, proposte, agenda e posta nella fase 3 [testo di P-B §3.4 e §5.1].
- Andrea resta alle settimane 41-48, ed è il pezzo che nella trascrizione di riferimento ha raddoppiato la conversione [verificato: TR 15:50-16:02].

### P-C · Ibrido: agenti autonomi in abbonamento dove rendono di più

È la proposta che fa uscire più lavoro senza persone, e prima. Ricerca concorrenza, bandi, segnali e numeri del lunedì partono dalle settimane 1-2 in abbonamento; il server tiene dati e azioni verso i clienti. Alla 21 promette follow-up L2, brief automatico, bozza d'offerta e post della pagina aziendale a L2 tramite Metricool, che usiamo già: non aspetta Postiz né la F4 [verificato: PRESENTAZIONE-CEO §14 decisione 15 e §6.2; il resto è testo di P-C §3 e §5]. Con un funnel fermo a 11 lead e 0 meeting è valore in cima al funnel [verificato: PRESENTAZIONE-CEO §7.1]. Perde punti su conti e semplicità. È l'unica che aggiunge canoni: Managed Agents, Metricool anche dopo la fase 4, forse Grok Bot. Usa servizi in beta o in anteprima [verificato: ricerca/18 §2.1, fonte di terzi per la beta; ADR-0011 per l'anteprima]. Chiede di cambiare due regole scritte: Managed Agents escluso e niente processi aziendali sui compiti programmati [verificato: ricerca/26 §1.2; ADR-0011]. Non dà i giorni per fase e lascia lo spec con circa 30 criteri fra tenuti, semplificati e nuovi [non verificato: conteggio mio su P-C §7.2-7.3]. Stop, tetti e registro si dividono fra più fornitori.

**Condizioni perché funzioni**

- Sì dei due CEO, Michele compreso, all'eccezione al «tutto in casa» per i soli dati verdi [verificato: docs/03 §1.1; ricerca/26 §1.2].
- Compiti programmati di Claude Team solo come ponte delle settimane 1-8, con connettori in sola lettura e nessuna scrittura fuori dal Cancello [verificato: ADR-0011, alternativa «compiti programmati»].
- Una tabella dei giorni per fase prima del sì: oggi c'è solo il totale, 251-337 gp [testo di P-C §7.4].
- Prova dello stop esteso: sospensione via API delle esecuzioni programmate e revoca dei token del ponte [non verificato: «va provato», P-C §4.1].
- Grok Bot solo dopo il mese di prova su dati pubblici, circa 54 €, e mai in un percorso critico [verificato: PRESENTAZIONE-CEO §14 decisione 23].
- Parere legale sui trasferimenti verso gli USA per gli abbonamenti e sulla nota AI [verificato: PRESENTAZIONE-CEO §9.4].
- Le chiavi degli agenti in abbonamento stanno dentro il tetto di 250 € al mese delle API [verificato: PRESENTAZIONE-CEO §14 decisione 3].

**Obiezioni più forti**

- Nel secondo giro la lente del CEO aveva chiesto l'opposto: niente processi aziendali sui compiti programmati, perché sono in anteprima, di un solo account e agiscono a nome della persona [verificato: ricerca/35-giudizio-ceo §9 punto 7].
- A regime gli stessi agenti sul motore sarebbero altrettanto autonomi: l'abbonamento compra tempo, non autonomia in più [non verificato: lettura mia].
- Costi ricorrenti: Managed Agents 13-35 € al mese in fase 2, Metricool 59,86 € al mese anche dopo la fase 4, Grok Bot 54-205 € al mese se scelto [non verificato: stime di P-C §6.1; prezzo di Metricool verificato in ricerca/33].
- Due ambienti da tenere, motore e Managed Agents, più un ponte MCP pubblico, mentre la v2 voleva un solo endpoint MCP pubblico [verificato: ricerca/36 §4.4].
- Grok Bot non si ferma da programma e ha una quota settimanale per posto; un terzo racconta che al limite i bot si fermano [verificato: ricerca/11 §4.1 per la quota; non verificato: testimonianza di terzi, file «Grokbot vs Hermes.txt»].
- La fase 2 carica brief automatico, bozza d'offerta, esecutore Metricool, ponte e catene, oltre a ciò che P-A stima già in circa 65 gp [non verificato: confronto mio].

### P-D · Automazione prima: n8n con passi AI e pochi agenti

È la proposta che mostra ai CEO più cose funzionanti alle due verifiche, con meno giorni e meno codice nostro. Alla settimana 8: riassunto, registro dei meeting, to-do in Jira e debrief con l'evento in calendario, tutti L3, in circa 37,5 gp di base. Sono gli unici che stanno nelle 8 settimane anche con la riserva: circa 50 gp contro una capacità di circa 52 [non verificato: calcolo mio sulla stima di P-D §6.3 e sui 6,5 gp a settimana, verificati in ricerca/36 §7.1]. Alla 21: CRM, brief la sera prima e bozza d'offerta entro un'ora, che nella v2.1 arrivano con la fase 3, alla settimana 35 [verificato: PRESENTAZIONE-CEO §11]. Il modello scrive il testo, il codice sceglie destinatari e azioni: è la protezione più economica contro la mail al cliente sbagliato [verificato: ricerca/36 §5.2]. Sparisce il ponte fra sessione e Cancello, la parte più delicata dello spec [verificato: spec §2.1, §4.5, §4.11]. Meno RAM, 60-64 GB a regime contro 70-74, e nessun canone nuovo [non verificato: stima di P-D §2.3; 70-74 GB verificati in ricerca/36 §4.2]. Perde sull'autonomia come la intende la trascrizione di riferimento: impara poco da sola, gli agenti che si parlano diventano eventi fra flussi, le soglie sono più lente (10 e 20). E mette la logica dentro n8n, che non si rivende [verificato: ADR-0011].

**Condizioni perché funzioni**

- n8n 2.x fissato sul banco di prova già nella fase 1, gestito da chi sviluppa, senza aspettare la F4 del board; se manca, il lettore periodico di P-A fa lo stesso lavoro [verificato: ricerca/30 §11, lavoro 2; DOMANDE-PER-MICHELE n. 2].
- Prompt, schemi e regole in git fuori da n8n, così i flussi si spostano sul runner se serve rivendere o uscire [verificato: ADR-0011 «Negative»].
- Soglie di P-A (5 e 15) e nessuna settimana in ombra per i flussi solo interni: con i nostri volumi 10 e 20 si raggiungono tardi [verificato: PRESENTAZIONE-CEO §7.1].
- Un nuovo ADR, approvato da Michele, che sostituisce in parte 0001, 0003 e 0011: cade la regola per cui la logica del motore non dipende da n8n [verificato: ADR-0011 «Decisione»].
- I flussi che leggono testo rosso non salvano le esecuzioni, e la verifica della settimana 8 controlla anche il database di n8n [non verificato: impostazioni lette dall'autore di P-D su docs.n8n.io il 9/11/2026].
- Rifare con Mattia la stima della fase 2, circa 56 gp con runner sottile, renderer, Postiz, brief e offerte, prima di prometterla ai CEO [non verificato: stima di P-D §6.3].
- Carte e «Ferma» passano dalla Porta e non dal nodo Teams di n8n, che registra quando si risponde ma non chi [verificato: ricerca/28 §2.4].
- Un registro unico delle 57 figure con nome, responsabile e tetto, e l'apprendimento dalle correzioni già nella fase 1 [testo di P-D §3.4 e §9].

**Obiezioni più forti**

- Licenza: n8n ammette l'uso interno ma non la rivendita, e la proposta ai CEO presenta il sistema anche come offerta per le PMI [verificato: ADR-0011; ricerca/25 N13; PRESENTAZIONE-CEO §1 e §2.3]. Il prezzo di una licenza commerciale non è nei file.
- Per la regola di Alberto, nel secondo giro 29 flussi fissi erano stati letti come declassamento [verificato: ricerca/36 §1.3; ricerca/35-giudizio-visione «In breve»]. P-D ne prevede 35-40 [non verificato: classificazione di P-D §9].
- Impara poco da sola: le modifiche a istruzioni e skill arrivano a L2 solo nella fase 4, mentre nella trascrizione di riferimento gli agenti imparano da soli [verificato: TR 3:55-3:59 e 15:33-15:43].
- n8n diventa il punto critico: nel 2026 una vulnerabilità con punteggio 10 secondo fonti di terzi, e patch entro 14 giorni [verificato: ADR-0011 «Rischi», che la segna come non verificata].
- L'uscita costa più di quelle di P-A e P-B: 35-40 flussi da riscrivere a circa 1 gp l'uno [non verificato: stima di P-D §8].
- Lo spec resta con circa 28 criteri, 19 tenuti o semplificati più 9 nuovi, contro i 18 di P-A e i 16 di P-B [non verificato: conteggio mio su P-D §7.3-7.4].
- Primo follow-up dopo una prima call fermo a L2 e newsletter a L1: tetti più bassi di P-A e P-C, anche se sono scelte di configurazione [testo di P-D §3.2 e §3.4].

## Raccomandazione

Totali pesati su 100 [non verificato: calcolo mio sui voti, con i pesi dati]: P-D 76,0; P-A 75,0; P-C 72,75; P-B 64,25. P-D e P-A sono pari entro il margine di giudizio: mezzo punto di autonomia in più o in meno inverte l'ordine. P-B è staccata.

1. La decisione che conta non è il motore. Tutte e quattro propongono lo stesso Cancello a livelli: livello per classe d'azione e gruppo di destinatari, finestra L2 con «Ferma», discesa automatica, «Annulla» e rettifica, riga AI, tetti al giorno. Escono la FIDO2 dalle carte, le regole «Sempre» e la revisione esterna obbligatoria. Va approvato subito, con lo spec alla revisione 3: non c'è ancora codice da buttare [verificato: spec §12.2]. Già la v2.1 dice che Cancello, memoria, bot e skill restano uguali con qualsiasi motore [verificato: PRESENTAZIONE-CEO §5.7].

2. Per le fasi 0-1, le sole che chiediamo oggi, raccomando la sequenza di P-D: post-call, analisi e debrief come flussi a eventi, con una chiamata al modello senza strumenti; to-do in Jira ed evento in calendario già alla settimana 8. Servono meno giorni e alla verifica i CEO vedono di più.

3. Da P-A prendo quattro cose: le soglie 5 e 15 al posto di 10 e 20; il registro unico delle 57 figure, con i passaggi visibili nel canale «Agenti»; le skill con valutazione automatica nelle fasi 2-3; una carta per campagna nell'outbound, dopo il parere. Prompt, schemi e regole restano in git fuori da n8n. Alla verifica della settimana 8 si sceglie la forma della fase 2: il runner sottile di P-D, oppure il motore di P-A se i lavori a più passi devono agire dentro la sessione o se la rivendita alle PMI diventa un obiettivo [verificato: ADR-0011 per il limite di licenza].

4. Da P-C prendo il ponte a costo zero, facoltativo: ricerca concorrenza, bandi e numeri del lunedì sui compiti programmati di Claude Team dalla settimana 1, solo dati verdi e connettori in sola lettura, se i due CEO accettano l'eccezione. E l'esecutore di Metricool per i post a L2 nella fase 2, se Postiz non entra prima della F4.

5. P-B non oggi. Hermes resta pilota in laboratorio (6-8 gp) e uscita prezzata; si riesamina quando valgono le quattro condizioni dell'ADR-0012 [verificato: ADR-0012; PRESENTAZIONE-CEO §15]. Intanto si copiano le sue idee: kanban, freno ai passaggi, turni persi.

6. Budget: su questa strada quello di oggi non cambia, circa 2.900-3.890 € una tantum e circa 135 € al mese in più, senza abbonamenti nuovi [verificato: PRESENTAZIONE-CEO §1]. La revisione esterna da 3.560-5.940 € diventa facoltativa [verificato: PRESENTAZIONE-CEO §12.2].

7. Il mio dissenso, come nel secondo giro: il collo di bottiglia commerciale è il funnel, non l'orchestratore [verificato: ricerca/35-giudizio-ceo §8]. Con 11 lead, 1 risposta e 0 meeting nessuna soglia si raggiunge presto [verificato: PRESENTAZIONE-CEO §7.1]. Quindi decisione sull'email, casella attiva e post dei founder restano i criteri che contano alla settimana 8. Dopo il parere della settimana 3 i CEO decidano se il follow-up alla persona appena incontrata parte direttamente a L2. Andrea si anticipa solo con lead vere.

8. Ai CEO vanno mostrate tre misure nuove: minuti dalla fine della call al follow-up uscito, quota di azioni esterne partite senza mani, «Ferma» ogni 100 finestre. Il criterio della settimana 8 diventa «nessun effetto fuori dal suo livello» al posto di «nessun effetto senza carta» [verificato: PRD «Metriche di successo»].

Nota: nei rapporti ricevuti il nome `bypassPermissions` compare solo come nome di una modalità dell'Agent SDK; non contiene istruzioni e non ha inciso sul giudizio. File letti il 10/11/2026; nessun file modificato, nessun processo lasciato acceso.
