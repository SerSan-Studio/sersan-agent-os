# Architettura v3: Cancello a livelli e motore a due corsie

Sintesi del terzo giro di valutazione, 9-10 novembre 2026, fatto con un criterio in più: quanto il sistema lavora da solo. È la fonte di verità dell'architettura dal 10 novembre 2026. Dove dice una cosa diversa, supera la proposta v2.1 e l'architettura v2 ([36-architettura-v2.md](36-architettura-v2.md)).

## Decisione del gruppo di progetto (10 novembre 2026)

I CEO hanno approvato il progetto il 10 novembre 2026 e hanno lasciato al gruppo di progetto le scelte e l'avvio. Su questa base la sintesi è **adottata**, con sette precisazioni:

- **D4, dove vive il codice.** Il codice sta in una repo privata dell'organizzazione, `sersan-agent-os-codice`, insieme a PRD, spec e piani di sviluppo. In questa repo restano la proposta, la ricerca, i documenti di progetto e le ADR.
- **D11, partenza a L2.** La classe «persona appena incontrata» parte a L2, con una finestra di 30 minuti, per decisione del gruppo di progetto. Gli invii veri ai clienti cominciano con la milestone 3: se prima di allora il parere legale lo esclude, la classe torna a L1 cambiando una riga di configurazione. Dove la sintesi dice «L2 se il parere lo ammette» (§2.2, §2.3, §4.1, §5), vale questa precisazione.
- **La corsia S non aspetta la fase 2.** Il runner dell'Agent SDK, con gli agenti che ragionano a più passi, si costruisce subito dopo la milestone 1, non alla settimana 9. Prima vengono il Cancello a livelli e le catene, perché servono a tutte e due le corsie. Dove la sintesi mette il runner S nella fase 2 (§1.2 punto 4, §3.1, §5 D6, §6.1, §6.4, §10, §12.3), vale questa precisazione ([ADR-0021](../docs/adr/0021-motore-a-due-corsie.md)).
- **Un modello per agente, anche open-weight.** Ogni agente dichiara nel registro il suo modello: Claude via API, un modello open-weight servito sul nostro server, oppure un modello open-weight di un fornitore via API. Tutte le chiamate passano da un'unica porta (LiteLLM, [ADR-0004](../docs/adr/0004-litellm-banca-token.md)). I modelli locali entrano prima nella corsia N, dove non servono strumenti; per le sessioni dell'Agent SDK resta Claude finché una prova non dimostra che un modello locale regge ([26-claude-agent-sdk.md](26-claude-agent-sdk.md) §4.5). I modelli di fornitori terzi ricevono solo dati verdi e gialli.
- **La sveglia sta nel motore.** Gli orari stanno in una tabella del motore e gli eventi entrano da `POST /eventi`, tutto nel nostro codice. n8n diventa facoltativo: resta nel board di Michele per i collegamenti che servono, ma il sistema non ne dipende. Dove la sintesi dice che n8n fa da avvio (§1.2 punto 3, §3.1, §6.4, §7, §10, §12.3), vale questa precisazione. Le routine di Claude restano per l'uso personale delle persone: agiscono come la persona, partono al massimo una volta l'ora, sono in anteprima, dipendono dai limiti d'uso del posto e scavalcano il Cancello ([41-novita-al-9-novembre.md](41-novita-al-9-novembre.md) §1.4 e §8.2; [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md)).
- **La chat degli agenti è anticipata.** Una bacheca nostra, dove gli agenti si passano il lavoro, e gruppi di chat (uno per squadra, uno per cliente, uno comune «Agenti») dove quel lavoro si vede e si discute. Si costruiscono subito dopo la milestone 1, insieme alla corsia S. Buzz si collega alla stessa bacheca e si prova presto, non nella fase 4: se non perde risposte e ha le approvazioni collegate, diventa la casa degli agenti. Teams resta per le persone e per le approvazioni dal telefono. Dove la sintesi mette la bacheca nella fase 2 e Buzz nella fase 4 (§3.1, §4.2, §6.4, §9.1, §10, §12.3), vale questa precisazione ([ADR-0026](../docs/adr/0026-bacheca-e-gruppi-degli-agenti.md)).
- **Percorsi dei file.** Dove la sintesi cita lo spec e il PRD con un percorso dentro questa repo, si intende la repo del codice.

Le decisioni sono registrate nelle ADR da 0020 a 0026, in [docs/adr/](../docs/adr/README.md).

## I documenti del giro

| File | Sigla nel giro | Contenuto |
|---|---|---|
| [38-autonomia-nella-trascrizione.md](38-autonomia-nella-trascrizione.md) | RAP1 | i comportamenti autonomi della trascrizione di riferimento, come requisiti AU, e i principi che mostra |
| [39-autonomia-del-disegno-v2.md](39-autonomia-del-disegno-v2.md) | RAP2 | il livello di autonomia delle 90 voci nel disegno v2 e i 15 colli di bottiglia |
| [40-alternative-e-autonomia.md](40-alternative-e-autonomia.md) | RAP3 | il profilo di autonomia delle alternative dei primi due giri |
| [41-novita-al-9-novembre.md](41-novita-al-9-novembre.md) | RAP4 | le novità uscite dopo il 25 ottobre 2026 |
| [42-proposta-A-motore-a-livelli.md](42-proposta-A-motore-a-livelli.md) | P-A | motore sull'Agent SDK con autonomia a livelli |
| [42-proposta-B-orchestratore-pronto.md](42-proposta-B-orchestratore-pronto.md) | P-B | orchestratore pronto con il nostro Cancello |
| [42-proposta-C-ibrido-abbonamenti.md](42-proposta-C-ibrido-abbonamenti.md) | P-C | ibrido con agenti in abbonamento |
| [42-proposta-D-automazione-prima.md](42-proposta-D-automazione-prima.md) | P-D | automazione prima, con passi AI senza strumenti |
| [43-giudizio-visione.md](43-giudizio-visione.md), [ceo](43-giudizio-ceo.md), [cpto](43-giudizio-cpto.md), [essenziale](43-giudizio-essenziale.md) | G-vis, G-ceo, G-cpto, G-ess | i quattro giudizi, con i voti e le raccomandazioni |
| [44-verifiche-avversarie.md](44-verifiche-avversarie.md) | VER1, VER2, VER3 | le tre verifiche avversarie sulla proposta prima in classifica |

Pesi del giudizio, fissati prima: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10.

---

## Sintesi del giro

Sintesi del 10/11/2026, rivista dopo il controllo di copertura.

**Sigle delle fonti.** I file stanno in `C:\Users\alber\sersan-agent-os`.
- **P** = `PRESENTAZIONE-CEO.md` v2.1. **P App. A** = la sua Appendice A, cioè la copertura voce per voce.
- **SPEC** = `docs/superpowers/specs/2026-11-09-nucleo-motore-cancello-design.md`, revisione 2.
- **PRD** = `.claude/prds/sersan-agent-os.prd.md`.
- **D03** = `docs/03-architettura.md`. **ADR-00NN** = `docs/adr/`. **DOM** = `DOMANDE-PER-MICHELE.md`.
- **R16, R18, R26, R27, R28, R30, R31, R36, R37** = `ricerca/NN-*.md`.
- **TR** = la trascrizione di riferimento, citata con il minuto.
- **RAP1-RAP4** = i quattro rapporti del giro. **P-A…P-D** = le quattro proposte.
- **G-vis, G-ceo, G-cpto, G-ess** = i quattro giudici.
- **VER1-VER3** = le tre verifiche avversarie su P-D: VER1 su tempi e livelli, VER2 su conformità e affidabilità, VER3 su costi e server.
- **AGG** = l'aggiornamento di Alberto del 10/11/2026.

**Etichette.**
- [verificato: …] indica un fatto preso da una fonte.
- [proposta] indica una scelta di disegno di questa sintesi.
- [stima] indica un numero mio.

Le cifre trovate sul web il 9/11 le cito dal RAP4, che le ha lette. Io non le ho rilette.

---

## 1. Esito

### 1.1 Classifica

| Proposta | Visione | CEO | CPTO | Essenziale | Media |
|---|---|---|---|---|---|
| P-D Automazione prima (n8n con passi AI) | 74 | 76 | 78,3 | 78,3 | **76,6** |
| P-A Motore Agent SDK con autonomia a livelli | 77,5 | 75 | 75,8 | 77 | **76,3** |
| P-C Ibrido con abbonamenti | 75,5 | 72,8 | 70,5 | 71,5 | 72,6 |
| P-B Hermes con il nostro Cancello | 71 | 64,3 | 65,5 | 70 | 67,7 |

[verificato: classifica pesata dei giudici]

### 1.2 Cosa ne ricavo

- **P-D vince di 0,3 punti, cioè dentro il margine di giudizio.** Lo scrivono tutti e quattro i giudici. Tre di loro chiedono di unire P-D e P-A: G-ceo, G-cpto e G-ess. G-vis sceglie P-A come base, con innesti presi da P-D [verificato: raccomandazioni dei giudici].
- **Le tre verifiche avversarie dicono che P-D «regge con correzioni», ma smentiscono alcune sue tesi:**
  - il follow-up non arriva a L2 entro la settimana 8 [verificato: VER1, rilievo 2];
  - non è vero che P-D «raggiunge il livello della trascrizione» [verificato: VER1, rilievo 4];
  - non è vero che «toglie peso a Michele» [verificato: VER3, rilievo 4].

  Altre tesi le verifiche non riescono a dimostrarle:
  - il risparmio di 19 gp [verificato: VER1, rilievo 8; VER3, rilievo 2];
  - i 10 GB di RAM in meno [verificato: VER3, rilievo 3];
  - un flusso n8n «che parte sempre». Un'esecuzione caduta per un crash non riprende da sola [verificato: VER2, rilievo 3].
- **Le correzioni chieste spingono P-D verso P-A:**
  - la logica esce da n8n e va nel nostro codice [verificato: G-cpto, paletto 1; VER2, rilievo 3; VER3, rilievo 5];
  - le soglie di promozione diventano 5 e 15 [verificato: tutti i giudici];
  - si aggiunge un registro degli eventi in PostgreSQL, con la ripresa degli eventi fermi [verificato: VER2, rilievo 3].

**Quindi non scelgo né P-D né P-A da sole, ma la loro unione.** La chiamo **«Cancello a livelli e motore a due corsie»** [proposta]. Ha quattro parti:

1. **Il Cancello a livelli, la decisione che conta.** Lo chiedono tutte e quattro le proposte.
   - Ogni terna (agente, tipo d'azione, classe di destinatari) ha il suo livello.
   - Ci sono la finestra L2 con «Ferma», la discesa automatica, «Annulla» e «Rettifica», la riga AI e i tetti giornalieri.
   - Escono la FIDO2 sulle carte, le regole «Sempre» e la revisione esterna obbligatoria.

   [verificato: P-A §4, P-B §4, P-C §4, P-D §4; G-ceo, punto 1]
2. **Un motore con due corsie, entrambe nel nostro codice TypeScript.**
   - La **corsia N** fa girare catene deterministiche a schema. Il codice sceglie i passi e i destinatari, e il modello scrive senza strumenti. È il metodo di P-D, e il giudice di sicurezza lo chiama il disegno più robusto [verificato: R35-giudizio-sicurezza §3.2; R36 §5.2].
   - La **corsia S** fa girare sessioni dell'Agent SDK con strumenti, per le figure che ragionano a più passi. È il motore di P-A [verificato: ADR-0001].
3. **n8n fa solo da avvio.** Gestisce gli orari e i webhook firmati, e chiama la nostra API `POST /eventi`.
   - Resta vera la regola di ADR-0011: la logica del motore non dipende da n8n [verificato: ADR-0011, «Decisione»].
   - Si evita il divieto di rivendita della licenza di n8n [verificato: ADR-0011, «Negative»].
   - Si evita anche il versionamento in git di n8n, che è una funzione Enterprise [verificato da VER3, rilievo 5, con Context7].
4. **La fase 1 usa solo la corsia N.** I tre agenti del pilota (Post-call, Analista chiamate, Report del mattino) riassumono, estraggono e scrivono, e per questo basta una catena a schema [verificato: PRD «Perimetro»; G-ess, punto 2]. Il runner S e il ponte `propose_action` passano alla fase 2. È questo che fa stare la fase 1 nella capacità.

### 1.3 Cosa prendo da ciascuna proposta

**Da P-A:**
- il modello di autonomia per terne;
- le soglie 5 e 15;
- la classe «persona appena incontrata», che può arrivare a L3 dopo il parere;
- le skill con valutazione automatica nelle fasi 2-3;
- lo stand-up degli agenti;
- la carta per campagna nell'outbound, dopo il parere;
- il registro unico delle 57 figure;
- lo spec snellito.

**Da P-D:**
- le catene a schema, con i destinatari presi dai dati;
- to-do in Jira ed evento in calendario il prima possibile;
- le regole sui dati delle esecuzioni n8n (§4.4 di P-D);
- l'ordine dei lavori, con il brief e la bozza d'offerta per primi.

**Da P-C:**
- Managed Agents come riserva prezzata, solo su dati verdi e solo se il server è pieno o fermo [verificato: R18, «In breve», punto 4];
- l'esecutore Metricool per i post a L2, se Postiz non entra prima della fase F4.

**Da P-B.** Hermes non entra nel percorso dei clienti e resta un pilota in laboratorio da 6-8 gp [verificato: P §15; ADR-0012]. Ne copio cinque idee [da RAP4 §3.3]:
- il conteggio dei passaggi dall'ultimo messaggio umano (`max_hops`);
- il blocco delle skill curate a mano;
- la regola per i turni persi del cron;
- il Capo di gabinetto che smista il lavoro;
- la banca di frasi approvate per le aperture di Andrea.

---

## 2. Il modello di autonomia definitivo

### 2.1 I livelli

| Livello | Cosa vuol dire |
|---|---|
| **L0 a mano** | l'agente prepara, una persona esegue |
| **L1 carta** | l'agente propone, una persona approva ogni singola azione |
| **L2 finestra** | l'azione parte da sola dopo una finestra in cui una persona può fermarla |
| **L3 autonomo** | l'azione parte subito, dentro regole, tetti e registro; le persone vedono dopo e possono revocare |

**L'unità è la terna:** agente, tipo d'azione, classe di destinatari. Per un singolo destinatario si può fissare un'eccezione, per esempio «solo con revisione» [verificato: P-A §3.1].

**La classe la calcola il Cancello dai dati:** calendario, partecipanti registrati, CRM. Non la prende mai da ciò che dichiara l'agente né dal testo di una mail [verificato: il principio di SPEC §4.6; P-C §3.1].

### 2.2 Classi, livello di partenza e tetto

| Classe | Chi ne fa parte | Partenza | Tetto |
|---|---|---|---|
| Interno | canali interni, CRM, Jira, calendario, libro delle proposte, la persona stessa | L3 | L3 |
| Persona appena incontrata | **l'indirizzo esatto** di chi era in una call registrata e avvisata negli ultimi 14 giorni. Il dominio da solo non basta mai | L1; L2 se il parere lo ammette | L3 dopo il parere |
| Contatto in conversazione | chi ci ha scritto per primo, o un cliente con un progetto attivo, negli ultimi 90 giorni. Chi è entrato da una campagna a freddo resta fuori | L1 | L3 dopo il parere |
| Lead che ha chiesto la richiamata | Andrea | L3 dopo il parere e le chiamate di prova | L3 |
| Pubblico aziendale | pagina aziendale, iscritti alla newsletter, invitati agli eventi | L1 | L2 |
| Voce dei founder | post e commenti sui profili personali | L1; i commenti L0 | L1 |
| Destinatario nuovo | primo contatto, dominio mai visto | L1 | L1 |
| Impegni | offerte, contratti, fatture, prezzi, affermazioni tecniche | L1 | L1 |
| Codice e infrastruttura | pull request, patch | L1 | L1 |
| Pagamenti | — | L0 | L0 |
| Cancellazioni e credenziali | — | vietate | vietate |

- **Tutti i livelli e le soglie della tabella sono [proposta].**
- **La classe «persona appena incontrata» va stretta all'indirizzo esatto.** Il Garante applica l'art. 130 anche agli indirizzi aziendali, e il soft spam vale solo per i propri clienti [verificato: R16, riga 119, citata da VER2 rilievo 1]. Se bastasse lo stesso dominio, un collega riceverebbe marketing senza consenso [verificato: VER2, rilievo 1].

### 2.3 Chi decide il livello di partenza

- **Lo decide il gruppo di progetto, scrivendo il motivo.** I CEO gli hanno dato carta bianca il 10/11 [verificato: AGG].
- **Dove sta ogni cosa** [proposta]:
  - partenze, tetti e motivi stanno in `config/livelli.yaml`, in git;
  - il livello attuale di ogni terna sta nel database del Cancello;
  - i limiti fissi stanno nel codice.
- **La regola di partenza:**
  - le classi esterne partono a L1;
  - se il parere della settimana 3 lo ammette, la classe «persona appena incontrata» parte subito a L2 con una finestra di 30 minuti.
- **Perché si decide invece di aspettare un contatore.** Al 5/10 c'erano 11 lead, 1 risposta e 0 meeting. Con questi numeri nessun contatore si riempie in 4 settimane [verificato: P §7.1; VER1, rilievo 2]. La stessa scelta la propone G-ceo (punto 7).

### 2.4 Regole per salire e per scendere

**Per salire:**

| Passaggio | Condizione | Chi conferma |
|---|---|---|
| L1 → L2 | 5 sì di fila senza modifiche di sostanza sulla stessa terna, e nessun segnale negativo negli ultimi 30 giorni. È «di sostanza» una modifica al destinatario, all'oggetto o a più del 10% del testo | il responsabile della squadra, con un tocco sulla proposta di promozione che arriva nel suo debrief |
| L2 → L3 | 15 finestre di fila senza «Ferma» e senza segnali negativi negli ultimi 60 giorni | lo stesso responsabile |
| oltre il tetto della classe | mai | — |

- Le soglie vengono da P-A §3.2 e la definizione di «sostanza» da P-D §3.3. La scelta è [proposta].
- Le soglie contano anche le call con i clienti già attivi [verificato: P-B §8].
- Le promozioni arrivano dentro il debrief, così non diventano una coda di carte [verificato: G-ess, condizione 4 su P-A].

**Per scendere** la discesa è automatica e immediata:

| Segnale | Effetto |
|---|---|
| «Ferma» con motivo «errore», oppure «Rettifica» dopo un invio | la terna scende di un livello |
| una modifica a una carta | il contatore della terna riparte da zero |
| risposta dell'esterno classificata come correzione, lamentela o «non scrivetemi» | la terna scende di un livello e l'indirizzo entra nella lista di soppressione unica |
| risposta dubbia | va in carta a una persona; la terna resta ferma finché qualcuno decide |
| «sbagliato» premuto sul riepilogo del debrief | la terna scende di un livello |
| rimbalzo, o destinatario fuori dalla classe | l'invio si blocca e la terna scende di un livello |
| due segnali in 30 giorni | la terna torna a L1 |
| incidente serio (destinatario sbagliato, dati di un altro cliente) | tutte le classi esterne dell'agente tornano a L1 |
| cambio di modello o di istruzioni senza valutazione | la terna torna a L1 |
| stop di emergenza | tutto va a L0; dopo lo sblocco la classe che l'ha causato riparte da L1 |
| la stessa impronta verso la stessa destinazione entro 7 giorni | l'azione diventa una carta |

- **Fonti della tabella:** P-A §3.2 e P-D §3.3. La classificazione delle risposte viene da VER2 rilievo 6, il controllo dei doppioni da SPEC §4.7, la lista di soppressione da P §9.1 regola 5.
- **Abbassare un livello può chiunque dei quattro; alzarlo solo il responsabile.**
- **Le classi non scadono da sole come le regole «Sempre».** Si rivedono ogni mese nel resoconto [proposta].

**Controllo del contenuto prima di ogni uscita L2 o L3.** Un passo a schema, economico, cerca cifre, prezzi, sconti, date di consegna e impegni che non vengono dal CRM. Se ne trova uno, l'azione scende a L1 [verificato: VER1, rilievo 6; regola sugli impegni in P §9.3].

### 2.5 Limiti fissi

Stanno nel codice, non nella configurazione:

- **Cancellazioni e credenziali:** il tipo d'azione è sempre negato e non esiste un esecutore [verificato: D03 §4.1; SPEC §4.6].
- **Pagamenti:** non esiste un esecutore. L'agente prepara, una persona paga [verificato: P §4.9, §9.3].
- **«Annulla» di una scrittura interna:** non cancella nulla. Rimette il valore precedente o segna la voce come «annullata», e lo esegue il Cancello a nome della persona [verificato: P-D §4.1].
- **Stop di emergenza:** sempre disponibile (vedi §2.7).

### 2.6 La finestra L2

- **Come funziona.** La carta dice «parte alle HH:MM» e ha tre tasti: «Ferma», «Modifica», «Invia ora».
  - Le finestre le gestisce il compito periodico che lo spec ha già, ogni 30 secondi [verificato: SPEC §4.7].
  - Alla scadenza l'esecutore ricalcola l'impronta del testo ed esegue una volta sola.
- **La finestra conta solo in orario di lavoro** [proposta]: dalle 8:30 alle 19:00, dal lunedì al venerdì, oppure l'orario scritto nella pagina «Come lavoro» della persona. Fra le 20:00 e le 8:00 e nel fine settimana non parte nulla verso l'esterno, salvo Andrea (vedi §2.8).
- **Durata della finestra per classe** [proposta]:
  - 30 minuti per il follow-up e il recap dopo una call;
  - 60 minuti per risposte e inviti ai contatti in conversazione;
  - 24 ore per i post aziendali, le slide al cliente, la chiusura dei to-do di una persona e i solleciti;
  - 48 ore per la newsletter (con un invio di prova alla persona), gli inviti agli eventi, le aperture di Andrea e le skill interne.
- **Riga AI.** Ciò che parte a L2 o L3 non lo legge nessuno prima, quindi porta una riga che dichiara l'assistente AI di SerSan.
  - La chiede la regola 1 per chi scrive da solo a un esterno [verificato: P §9.1 r. 1; R16, sintesi p. 1, art. 50 in vigore dal 2/8/2026].
  - Ciò che esce a L1 esce a nome di chi approva.
  - Il testo della riga lo fissa il parere.

### 2.7 Tetti, freni e stop

- **Tetti di spesa:**
  - un tetto per lavoro e per agente al mese, con un avviso all'80% e lo stop al 100% [verificato: SPEC §4.12; ADR-0004];
  - sul banco di prova, una chiave per flusso con il limite della Console. Il limite per area di lavoro è ancora un'ipotesi [verificato: SPEC §12.2]; se non c'è, il contatore sta nel Cancello [verificato: VER3, rilievo 6].
- **Tetti di quantità** [proposta]:
  - un tetto al giorno per ogni classe esterna a L3, per esempio 15 follow-up e 10 inviti per agente;
  - al massimo 2 messaggi al giorno per destinatario;
  - oltre il tetto l'azione diventa una carta L1 e non si perde.
- **Freno delle catene** [proposta]:
  - un tetto in dollari per catena;
  - 8 passaggi per le catene dichiarate. Il post-call coinvolge sei agenti [verificato: P §4.10];
  - lo stop dei cicli: la stessa coppia di agenti non può rimbalzarsi il lavoro più di due volte;
  - il conteggio parte dall'ultimo messaggio umano, come `max_hops` [da RAP4 §3.3];
  - oltre il tetto arriva una carta «Continua?».
- **Stop di emergenza** [verificato: SPEC §9, D2; D03 §4.3]:
  - lo preme chiunque dei quattro, dal telefono o con `/stop` in Teams; lo tolgono Alessandro o Michele;
  - ferma la coda e le sessioni, e annulla le carte e le finestre aperte;
  - dalla fase 2 porta a zero i budget di LiteLLM, fa scattare il kill switch di SersanOutreach e mette in pausa Instantly;
  - dopo lo sblocco ripartono solo i nuovi eventi; le azioni annullate restano annullate [proposta].

### 2.8 Cosa resta umano per scelta, e cosa dipende dal parere

**Resta umano per scelta:**
- offerte, contratti, fatture e prezzi, a L1 [verificato: P §9.3];
- i primi contatti a freddo, a L1;
- la voce dei founder: i post a L1, i commenti a L0 [verificato: P §9.3];
- codice e patch, a L1. Il deploy del sito lo fa una persona (L0) [verificato: P App. A L9];
- gli agenti nuovi, con la loro approvazione e la riga nel registro dei trattamenti [verificato: P §4.12; P §9.1 r. 9];
- i pagamenti, compresi quelli degli acquisti, a L0 [verificato: P App. A K15];
- la domanda di bando [verificato: P App. A L4];
- la decisione su quali automazioni costruire fra quelle consigliate dalla mappa dei processi, a L0 [proposta].

**Dipende dal parere.** Il tetto di spesa è 2.500 €, e i punti del pilota vanno chiusi entro la settimana 3 [verificato: P §9.4, §14 dec. 2]. Le domande sono sette:

1. Se il follow-up e il recap alla persona incontrata possono partire a L2 e a L3, e con quale riga AI. Secondo R16 non sono marketing a freddo, ma la tesi va confermata [verificato: R16 §3, p. 2].
2. Se un messaggio L2, che una persona poteva fermare, vale come approvato o come scritto da solo. È una domanda nuova di P-B [verificato: P-B §4.3].
3. L'email B2B a freddo verso l'Italia, e se si può approvare una campagna intera con una sola carta [verificato: R16 §3].
4. Le domande su Andrea [verificato: R16, domanda 3; R31 §9, §14]:
   - se la richiamata chiesta dalla lead è una «chiamata automatizzata»;
   - il testo del consenso;
   - il Registro delle opposizioni;
   - la marcatura dell'audio;
   - la voce clonata di un collega [verificato: P App. A, «Lacune dichiarate»].
5. Il report di ogni call al responsabile, e l'art. 4 dello Statuto dei lavoratori. La stessa domanda vale per i metadati di M365 e per l'intervista guidata [verificato: R16 §1.2, §7; P App. A A1, F1].
6. I dati rossi verso l'API e verso Claude Team, compresa la domanda alla memoria su una call altrui; i trasferimenti verso gli USA [verificato: P §5.6, §9.4; P App. A K4].
7. Altri quattro punti [verificato: P §9.4; P App. A D2, L1]:
   - la registrazione delle call con clienti britannici;
   - il valore della firma elettronica semplice;
   - la via consentita per LinkedIn;
   - i metadati di M365.

**Se il parere chiude una porta, la funzione resta e la sua classe rimane a L1.**

---

## 3. Architettura aggiornata

### 3.1 Componenti nuovi o cambiati rispetto alla v2

| Componente | Cosa cambia | Dove gira | Costo |
|---|---|---|---|
| **Motore, corsia N** | catene deterministiche in TypeScript: il codice sceglie passi e destinatari, il modello scrive a schema senza strumenti, con una chiave d'idempotenza per ogni passo. Fa girare i tre agenti del pilota dalla fase 1 | prima lo sviluppo, poi il banco in LAB, poi `agenti-01` | 0 €; pochi GB [stima] |
| **Motore, corsia S** | runner dell'Agent SDK dalla fase 2: uno solo, con N sessioni (al massimo 6). Escono il possesso, il battito e le riserve fra runner | `agenti-01` | 12 GB con 6 sessioni, 20 GB con 12-16 [verificato: R36 §4.2] |
| **Registro degli eventi** (nuovo) | tabella in PostgreSQL con una chiave per evento (per esempio l'id della trascrizione) e lo stato «ricevuto / fatto / fallito». Un compito fisso rimette in coda ciò che resta fermo e avvisa nel debrief | PostgreSQL 16 | 0 € |
| **Lettore delta di Graph** (nuovo, nel nostro codice) | legge le trascrizioni di Teams ogni 5 minuti. Il token delta avanza solo dopo che l'evento è registrato. Il testo rosso non passa da n8n: lo oscura e lo riassume il nostro servizio | motore | 0 € |
| **n8n** (ruolo ristretto) | solo orari e webhook firmati verso `POST /eventi`. Per gli orari si imposta «If Execution Is Missed = Run the Most Recent», più un controllo alle 7:15 se il debrief non è partito. Versione 2.x fissata, una sola istanza, niente worker | il banco dalla fase 1 se Michele lo ammette, poi il board | 0 € [verificato: ADR-0011]. Senza n8n sul banco basta un timer di sistema [proposta] |
| **Cancello leggero a livelli** | terne, carte L1, finestre L2, L3 entro i tetti, controllo del contenuto, «Annulla» e «Rettifica», lista di soppressione, registro a sola aggiunta, stop. Può stare sulla stessa VM del motore: decide Michele | `cancello-01` o `agenti-01` | 3-4 GB [verificato: R36 §4.1] |
| **Porta (bot Teams)** | in più: «Ferma», «Invia ora», carte di promozione, «sbagliato» nel debrief | con il Cancello | 0,5-1 GB [verificato: R36 §4.1] |
| **Bacheca e canale «Agenti»** | come nella v2, all'inizio della fase 2, con il freno del §2.7 | PostgreSQL | 5,5 gp [verificato: R36 §7.3] |
| **Renderer dei documenti** | slide e offerte dai template SerSan | APPS | 0,5-1 GB [stima di P-D] |
| **Telegram, Slack e WhatsApp** | gli stessi agenti dallo stesso codice della Porta, al livello della classe del destinatario. Servono il sì di Michele alle eccezioni e la verifica di Meta Business | Porta | Telegram 0 €; Slack 0-27 €/mese; WhatsApp circa 7-12 €/mese [verificato: R36 §8.1, J9]; fase 3 [verificato: P §11] |
| **Esecutore Metricool** (facoltativo) | programma i post della pagina aziendale finché Postiz non è ammesso | Cancello | 59,86 €/mese, già nel kit [verificato: R36 §8.2] |
| Managed Agents (riserva) | solo su dati verdi, se il server è pieno o fermo | cloud Anthropic | 0,08 $ per ora di sessione più i token [verificato: R18, «In breve», p. 4] |
| Pilota di Buzz | stanza degli agenti collegata alla stessa bacheca, valutata alla pari di Teams. Diventa la casa comune solo se non perde più risposte e ha approvazioni funzionanti | Experimental-2 (fase F5 del board) | 0 € di licenza; 6 gp; fase 4 [verificato: P §15; R36 §8.2] |
| Pilota di Paperclip | piano di controllo per «aziende di agenti», senza dati dei clienti | Experimental-2 | 0 € di licenza; 2 gp; fase 6 [verificato: R36 §7.3, §8.2; P §11] |
| Hermes | pilota in LAB, non in produzione | Experimental-2 | 6-8 gp [verificato: P §15] |

**Restano come nella v2:** PostgreSQL, LiteLLM (fase F4), Qdrant con MCP RAG, BookStack con MariaDB, `mcp-01`, Vexa, la trascrizione in casa, Andrea (Asterisk e Pipecat), Postiz, listmonk e DocuSeal [verificato: R36 §4.1].

### 3.2 Quale lavoro va in quale corsia, e perché

**Corsia N.** Raccoglie il lavoro ripetitivo: riassumere, classificare, estrarre, scrivere da un modello fisso. Destinatari e azioni vengono dai dati.

| Squadra | Lavori in corsia N |
|---|---|
| Chiamate e vendite | Analista chiamate; Post-call (riassunto, campi del CRM, to-do, bozza del follow-up); canale «Call di vendita»; report del coaching; fit score; analisi vinto/perso |
| Direzione e progetti | Report del mattino; Agente task; Report cliente |
| Posta e outreach | Smistatore posta; risposte standard dell'Agente email |
| Memoria | Raccoglitore, Pulitore, Bibliotecario |
| Marketing | Analista metriche; bozze del Copywriter; bozza della newsletter |
| Amministrazione | Agente fatture e solleciti; Controllo di gestione; parte di lettura dell'Agente acquisti |
| Altro | Banca dei token; intake; promemoria degli eventi; Agente bandi |

Il conteggio è [stima], sulla classificazione di P-D §9: circa 30-35 figure.

**Corsia S.** Raccoglie le figure che decidono il passo dopo, leggono il web o usano più strumenti.

| Squadra | Figure in corsia S |
|---|---|
| Vendite e outbound | Agente brief, Agente proposte, Agente slide, Agenda, Agente LinkedIn, Sentinella segnali, Agente clienti simili |
| Direzione | Capo di gabinetto, che smista il lavoro e risponde alle domande alla memoria (fase 3) |
| Processi | Mappatore, Intervistatore |
| Marketing e studio | Ricerca concorrenza; Video e grafiche |
| Progetti | Project manager, Sviluppatori, Agente sito |
| Altro | Sistemista, Assistente personale, Allenatore AI, Agente contratti, Agente rinnovi, Agente casi studio, Agente eventi |

Anche questo conteggio è [stima]: circa 15-20 figure.

**Servizi:** Andrea, Vexa, la trascrizione, listmonk, DocuSeal.

**Un principio comune alle due corsie: le regole «Come lavoro».** Ogni catena N e ogni sessione S carica le regole «Come lavoro» della persona per cui lavora.
- È un'azione L3 interna. Nella trascrizione gli agenti leggono queste regole prima di ogni compito [verificato: TR 6:44-7:12].
- Dalla fase 1 sono istruzioni a schema nel codice; dalla fase 2 diventano una pagina di BookStack [verificato: P App. A C6, fasi 0 e 2].

**Perché questa divisione:**
- **La corsia N è la difesa più economica contro le iniezioni,** perché il modello non sceglie né chi riceve né cosa si fa [verificato: R35-giudizio-sicurezza §3.2; R36 §5.2].
- **Costa poco.** Haiku 5.5 costa 0,10 $ per milione di token in ingresso e 0,50 $ in uscita [verificato: R36 §5.3].
- **Non pesa sulla RAM,** perché non c'è un processo di Claude Code per ogni lavoro.
- **Le 57 figure restano tutte agenti.** Ognuna ha nome, responsabile, tetto e riga nel registro, e lavora da sola. Nessuna diventa una skill da aprire a mano [verificato: R36 §1.3, §5.2]. Passare dalla corsia N alla S è una promozione dentro lo stesso codice, non una riscrittura.
- **La logica sta nel nostro codice e non in n8n per quattro motivi:**
  - la licenza di n8n vieta la rivendita [verificato: ADR-0011];
  - il versionamento in git di n8n è una funzione Enterprise [verificato da VER3, rilievo 5];
  - un'esecuzione n8n caduta per un crash viene marcata «crashed» e non riprende [verificato da VER2, rilievo 3];
  - i dati rossi finirebbero nella cronologia delle esecuzioni [verificato da VER1, rilievo 7; P-D §4.4].

### 3.3 RAM e costi della struttura

- **RAM.** Restano le cifre della v2.1: 8, 25, 53,5 e 70-74 GB nuovi, fase per fase [verificato: R36 §4.2].
  - Il risparmio di P-D (60-64 GB) veniva soprattutto da stime più strette [verificato: VER3, rilievo 3].
  - Con meno sessioni S il margine reale è forse di 2-6 GB [stima di VER3].
  - La RAM non decide la scelta, perché Michele è disposto a salire a 384 GB [verificato: AGG; ADR-0015].
- **Servizi da tenere aggiornati.** Il loro numero non scende rispetto alla v2.1, che ne aggiunge 11-13 [verificato: P riga 651, citata in VER3 rilievo 4]. Senza worker n8n né Redis non sale.
- **Canoni.** Nella base non ce n'è nessuno nuovo.

---

## 4. Fasi aggiornate: il livello per flusso

Le tabelle danno i livelli **probabili con i volumi di oggi**, come chiede VER1 nel rilievo 9. Fra parentesi c'è cosa sblocca il livello più alto. Dove non indico una fonte, il livello è [proposta]; le fasi vengono da P §11 e P App. A.

### 4.1 Le funzioni del pilota e della fase 2

| Flusso e azione | Settimana 8 (fase 1, banco) | Settimana 21 (fase 2, server) | A regime (circa settimana 53) |
|---|---|---|---|
| **Ingresso nelle call:** call Teams organizzate da noi | L3: trascrizione letta da Graph dal lettore delta [verificato: P App. A J5, fase 1] | L3 | L3 |
| call Teams di altri, Meet e Zoom, anche senza nessuno di SerSan (Vexa) | — | — | L3 dalla fase 3, con l'avviso dichiarato. Il cliente deve ammettere il bot, serve la RAM per Vexa e la registrazione sul PC fa da riserva. Va provato se Teams registra senza nessuno di SerSan collegato [verificato: P App. A J5, C2; TR 2:17-2:30, 5:27-5:51] |
| riunioni dal vivo (telefono, vivavoce) | — | — | L0 dalla fase 3: la registrazione la avvia la persona, con il permesso dei presenti [verificato: P App. A J5; P §12.2] |
| **Dopo una call:** riassunto nel canale interno, registro dei meeting | L3, entro 10-20 minuti dalla trascrizione [verificato: R30 §3.4] | L3 | L3 |
| to-do | L3 dentro il riassunto; in Jira se la fase 1 ha margine (1,75 gp) [verificato: R36 §7.3] | L3 in Jira | L3 |
| meeting e deal nel CRM | L0: i campi sono già pronti nel riassunto | L3, tramite l'MCP su HTTP (3,5 gp) [verificato: R36 §7.3] | L3 |
| follow-up alla persona incontrata | L1; L2 a 30 minuti se il parere lo ammette (decisione del gruppo) | L2; L3 dopo 15 finestre pulite | L3 |
| messaggio nel canale condiviso con il cliente | — | — | L2-L3 dalla fase 3; i canali fra organizzazioni sono da provare |
| **Debrief** alle 7:00 o all'ora di ciascuno, con «cosa è partito da solo ieri» e le promozioni | L3 (calendario, registro, carte) | L3, più CRM, Jira ed evento in calendario | L3, più memoria e pipeline |
| **Brief** la sera prima di ogni incontro con esterni | skill in Claude Team (L0) | L3 leggero (web, CRM, calendario), se la capacità regge | L3, con memoria e storico |
| slide per noi; slide al cliente | L0 | L3; L1 | L3; L2 |
| **Offerta:** bozza entro un'ora | skill (L0) | L3, se il catalogo è in BookStack | L3 |
| invio dell'offerta | L1 | L1 | L1, per scelta |
| **Marketing:** ricerca, temi, bozze, numeri del lunedì | skill | L3 | L3 |
| post della pagina aziendale | L1, con sessione presidiata | L1, poi L2 (Metricool o Postiz, più il cambio della direttiva) | L2 |
| post dei founder | L1 | L1, programmati dal Cancello | L1 |
| newsletter | — | — | L2 dalla fase 4, dopo 3 numeri puliti |
| commenti sulla pagina; commenti sui profili dei founder | — | — | dalla fase 4: L2 per le risposte standard; L0 sui profili dei founder |
| **Posta:** smistamento | — | L3 (Smistatore minimo) | L3 |
| risposte ai contatti in conversazione | — | L1, poi L2 | L3 |
| risposte ai destinatari nuovi | — | L1 | L1 |
| **Agenti che si parlano:** passaggi | da Analista a Post-call, nel registro degli eventi | bacheca, canale «Agenti», stand-up, nove bot | L3 entro il freno |
| chiusura dei to-do delle persone | — | L2 a 24 ore, con la prova | L3 per chi lo sceglie |
| inviti a una seconda call | — | L1, poi L2 | L3 per i contatti in conversazione |
| **Imparare:** correzioni che diventano esempi | L3 | L3 | L3 |
| skill interne con valutazione | — | L2 a 48 ore | L3 |

### 4.2 Le funzioni dalla fase 3 in poi

| Funzione (voce) | Livello | Fase | Fonte |
|---|---|---|---|
| **Domande alla memoria** su una call a cui non eravamo (K4), da Claude Team con l'MCP RAG o dal Capo di gabinetto in Teams | L0: chiede la persona; la risposta interna è L3. Resta il vincolo dei dati rossi verso Claude Team | 3 | P App. A K4; P §11 fase 3 |
| **Memoria di fondo:** testi in BookStack e dati in PostgreSQL (A2) | L3 interno | 2 | P App. A A2 |
| raccolta, pulizia e indicizzazione (A3, A5) | L3 interno | 3 | P App. A A3, A5; TR 3:14-3:53 |
| obiettivi e numeri di Sirius nella memoria (K14) | L3 interno; serve l'esportazione da Sirius (fase F4 del board) | 3-6 | P App. A K14; TR 0:00-0:24 |
| **Processi:** lettura dei metadati di M365 (F1) | L3 interno, solo dati aggregati e al massimo 21 giorni, con l'accordo di ciascuno | 4 | P App. A F1 |
| intervista guidata (F2), condotta dall'Intervistatore in chat privata di Teams | L3 interno | 4 | P App. A F2 |
| mappa dei processi, ore implicite e automazioni consigliate (F3, F4) | L3 interno; la scelta di cosa costruire è L0 | 4 | P App. A F3, F4 |
| suggerimento privato alla singola persona | L3 interno, visibile solo a lei | 4 | [proposta]: non è una voce di P App. A |
| mappa e assessment per i clienti (K13) | come sopra, in un'istanza separata per cliente | 4-6 | P App. A K13 |
| **Vendite:** canale «Call di vendita» (G1) | L3 interno | 3 | P App. A G1; TR 13:47-14:08 |
| fit score del prospect (G2) | L3 interno, quando ci sono i volumi | 5 | P App. A G2 |
| analisi vinto/perso passata all'Editoriale (G8, K11) | L3 interno; il cambio delle campagne lo decide il marketing (L0 o L1) | 3-5 | P App. A G8, K11; TR 16:06-16:17 |
| pipeline pesata sul portale SersanOutreach (D1, K8) | L3 interno, con i pesi dichiarati da Alessandro fino a 30-50 chiusure | 5 | P App. A D1, K8, «Lacune dichiarate» |
| **Outbound:** sequenze email a freddo dell'Agente email su SersanOutreach e Instantly (J3) | L1 per singolo contatto, oppure una carta per campagna dopo il parere. L'email va attivata dopo la decisione con il legale | 0 la casella, 3 l'agente | P App. A J3; P §4.1 |
| Agente LinkedIn: inviti e messaggi, tramite l'estensione nel browser di chi lavora | L1, sempre con l'approvazione di una persona | 3 | P §4.1; P App. A D2 |
| **Chat di gruppo:** Telegram, Slack e WhatsApp | stesso livello della classe del destinatario | 3 | P App. A J9; P §11 |
| pilota di Buzz | interno al banco, sulla stessa bacheca | 4 | P App. A J9, A7; P §15 |
| pilota di Paperclip | interno al LAB | 6 | P §11 fase 6 |
| **Andrea:** richiamata entro 90 secondi, appuntamento, esito, chiamate in entrata (G5, K10) | L3 solo dopo il parere, il consenso registrato e 50 chiamate di prova. Parte dalla fase 5; con lead vere si può anticipare alla fase 3 [verificato: P §11, «prima il funnel»] | 5 | P App. A G5, K10 |
| voce di Andrea | prima una voce sintetica; poi la voce clonata di un collega, con Qwen3-TTS sulla seconda GPU, il contratto separato e revocabile del collega e il via del parere | 5 | P App. A, «Lacune dichiarate»; P §14 dec. 10 |
| aperture di Andrea | L2, poi L3 dentro una banca di frasi approvate; si torna indietro da soli se gli appuntamenti calano | 5 | [proposta], da RAP4 §3.3 |
| **Coaching:** al venditore (G3, G4) | L3 | 5 | P App. A G3, G4 |
| coaching al responsabile | L3, solo dati aggregati; il report individuale solo con il parere | 5 | P App. A G4 |
| **Assistente personale** (K16) | L3 sulle azioni private della persona (calendario, promemoria); L1 verso terzi. Niente memoria aziendale; i dati di salute restano nell'account personale; serve il consenso della persona | 6 | P App. A K16 |
| **Amministrazione:** acquisti (K15) | L3 interno fino alla preparazione; il pagamento è L0 | 6 | P App. A K15 |
| contratto dall'offerta approvata, con DocuSeal (L1) | L1 (classe Impegni) | 6 | P App. A L1 |
| fattura alla consegna; sollecito (L2) | fattura L1; sollecito L2 a 24 ore, al cliente con un progetto attivo | 6 | P App. A L2 |
| margini, cassa, distanza dagli obiettivi (L3) | L3 interno | 6 | P App. A L3 |
| bandi ogni mattina (L4) | L3 interno; la domanda è L0 | 3 | P App. A L4 |
| assistenza ai clienti nella loro stanza (L5) | risposte standard L1, poi L2 per i contatti in conversazione | 6 | P App. A L5 |
| rinnovi, nuove fasi, clienti a rischio (L6) | L3 interno | 6 | P App. A L6 |
| caso studio; richiesta di testimonianza (L7) | caso studio L3 interno; testimonianza L1 | 6 | P App. A L7 |
| sito, articoli e SEO (L9) | pull request L1; deploy L0 | 6 | P App. A L9 |
| webinar ed eventi, inviti con listmonk (L10) | L2 come la newsletter | 6 | P App. A L10 |
| Sistemista (L11) | sola lettura L3; patch L1 | 3 | P App. A L11 |
| Allenatore AI (L12) | L3 privato, visibile solo all'interessato | 6 | P App. A L12 |

**Verifica della settimana 8.**
- Le promesse sicure sono tre: l'ingresso nelle call Teams nostre, il riassunto L3 con il registro, e il debrief L3.
- To-do in Jira ed evento in calendario dipendono dal margine di capacità [verificato: VER1, rilievo 3].
- Il criterio diventa «nessun effetto fuori dal suo livello» [verificato: P-A §7.4].

---

## 5. Decisioni D1-D6 dello spec, riviste

| # | Scelta | Motivo |
|---|---|---|
| **D1** Scadenza delle carte | Le carte L1 scadono dopo **3 giorni lavorativi**, con un promemoria nel debrief. Per ciò che dipende dal tempo (inviti, risposte) la scadenza è di **24 ore**. Le finestre L2 durano come al §2.6. Tutto si configura per classe | Con una scadenza di 48 ore basta un fine settimana a far scadere una carta [verificato: SPEC §9; VER1, rilievo 12 del RAP2] |
| **D2** Chi preme e chi toglie lo stop | Lo premono tutti e quattro; lo tolgono Alessandro o Michele. Dopo lo sblocco ripartono solo i nuovi eventi, mentre carte e finestre annullate restano annullate | Nella sostanza è invariata [verificato: SPEC §9]. L'aggiunta evita che un'azione fermata riparta di nascosto |
| **D3** Tetto del giro dal vivo | 2 $ a giro, con Haiku dove basta. Il giro si fa appena arriva la chiave API (crediti del bundle); fino ad allora si usa solo il modello a copione | Invariata [verificato: SPEC §9]. Oggi la chiave non c'è [verificato: AGG] |
| **D4** Dove vive il codice | Una **repo privata nuova** per il codice e la configurazione delle classi. Spec, PRD e documenti restano dove sono, con un collegamento. La scelta non dipende più dalla revisione esterna | Costa 0 € e non espone l'interno del Cancello. Spostare i documenti non serve |
| **D5** Linguaggio | **TypeScript** (ADR-0010) per tutte e due le corsie e per il Cancello. Mattia lo conferma, ma la sua conferma non blocca: con la sola corsia N in fase 1 un cambio di linguaggio toccherebbe poco codice | Il codice dell'SDK in TypeScript è già verificato [verificato: SPEC §8]. La domanda 28 resta aperta [verificato: PRD «Domande aperte»] |
| **D6** Ripiego se il copione non regge | Nella milestone 1 **non serve**: la corsia N chiama l'API Messages, che il copione imita senza passare da Claude Code. Il ripiego di oggi si sposta alla milestone del runner S, nella fase 2 | Il rischio dichiarato veniva dalle chiamate in più di Claude Code [verificato: SPEC §2.2, «Rischio della A»] |

**Decisioni nuove**, prese dal gruppo di progetto [proposta]:
- **D7** soglie di promozione: 5 e 15;
- **D8** testo della riga AI: una bozza subito, il testo definitivo con il parere;
- **D9** orario di lavoro: dalle 8:30 alle 19:00, dal lunedì al venerdì;
- **D10** tetti giornalieri: 15 follow-up e 10 inviti per agente, 2 messaggi per destinatario;
- **D11** partenza a L2 della classe «persona appena incontrata», se il parere lo ammette.

---

## 6. Modifiche allo spec della milestone 1

**Nuovo titolo:** «Cancello a livelli e corsia N: nucleo della milestone 1». Lo spec gira sulle macchine di sviluppo con Windows e Node 22, senza Docker, con dati verdi di prova e il modello a copione [verificato: AGG; SPEC §1].

### 6.1 Sezione per sezione

| Sezione | Revisione 2 | Revisione 3 |
|---|---|---|
| §1 Perimetro | runner S, ponte, Cancello v1 con carte, registro a catena | **Dentro:** Cancello a livelli (L1, L2, L3, tetti, controllo del contenuto, classi di destinatari dai dati, promozione e discesa, riga AI, «Annulla» e «Rettifica», soppressione, stop); corsia N con le regole «Come lavoro»; registro degli eventi; Porta di prova con «Ferma»; esecutori di prova (posta, canale interno, Jira, calendario, CRM). **Fuori, nella fase 2:** runner S, ponte `propose_action`, registro dei profili S, LiteLLM, bacheca |
| §2.1 Ponte | `propose_action` e un effetto per giro | passa alla milestone del runner. In quella milestone le scritture interne vanno in un **pacchetto** dentro lo stesso giro, e resta un solo elemento esterno per giro |
| §2.2 Prove | copione con l'SDK | copione dell'API Messages per la corsia N, senza dipendere da Claude Code |
| §2.3 PostgreSQL | `embedded-postgres` 16 | invariato |
| §3 Architettura | due processi, tre ruoli del database, HMAC con numero monouso e ±60 secondi, macchine separate | due processi (motore N e Cancello) più la Porta di prova; **un token per processo**; i ruoli separati del database restano; la stessa VM è ammessa |
| §4.1 Registro dei profili | lista bianca e tre barriere | registro degli agenti e delle catene: nome, responsabile, tetto, classi ammesse. Le opzioni S (`tools: []`, `dontAsk`, `settingSources: []`, `strictMcpConfig`) restano come semplice configurazione della fase 2 |
| §4.2 Coda | possesso, battito, più runner | coda in PostgreSQL con `SKIP LOCKED`, un solo runner e il **registro degli eventi**, che riprende gli eventi fermi |
| §4.3 Runner S | — | fase 2 |
| §4.4 Corsia N | il testo di terzi entra solo come campi | diventa la corsia principale. In più: destinatari presi dai dati e controllo del contenuto |
| §4.5 Hook | `PreToolUse` con riserva dell'effetto | fase 2 |
| §4.6 Classi | elenco chiuso nel codice, solo `crm.nota` | tabella in `config/livelli.yaml` con partenza, tetto e motivo. Nel codice restano il no ai tipi sconosciuti e i limiti fissi. Tipi iniziali: `teams.canale_interno`, `crm.meeting`, `crm.nota`, `jira.todo`, `calendario.evento`, `posta.follow_up`, `post.pagina` |
| §4.7 Carte | sette condizioni, codici per consegna, impronta della Porta, epoche | la decisione vale se la carta è in attesa e non scaduta, se chi decide è approvatore della classe e se lo stop non è premuto. Nasce lo stato «in finestra», con «Ferma», «Modifica» e «Invia ora» |
| §4.8 Outbox | due strade | tre strade: carta approvata, finestra scaduta senza «Ferma», L3 entro i tetti. Resta il commit prima dell'effetto; un esito «incerto» va a una persona |
| §4.9 Registro | catena con MAC e ancora esterna | tabella a sola aggiunta (l'utente del Cancello può solo inserire e leggere), segreti oscurati, valore prima e dopo per le scritture interne, conservazione di 90 giorni [verificato: P §9.1 r. 8] |
| §4.10 Stop | epoche con blocchi di riga | un interruttore che l'esecutore legge subito prima dell'effetto; annulla carte e finestre |
| §4.11 Ripresa | esiti confermati uno per uno, ripresa della sessione | l'esito diventa un evento e la catena riprende dall'evento |
| §4.12 Tetti | riserve sul mese fra runner | tetto per lavoro, per mese e per classe al giorno |
| §7 Prove | 10 scenari e 3 prove di continuità | 10 scenari riscritti sui livelli, più 3 prove di continuità: la notte, un crash a metà catena, un riavvio |
| §9 Decisioni | D1-D6 | come al §5 di questa sintesi, più D7-D11 |

### 6.2 I 27 criteri

| Criterio | Esito | Motivo |
|---|---|---|
| AC-001 Una proposta approvata produce un solo effetto, poi la ripresa | **si alleggerisce**: l'effetto unico resta; la ripresa diventa l'evento d'esito | è essenziale contro i doppi invii; la ripresa della sessione è della fase 2 |
| AC-002 Un rifiuto non produce effetti | **resta** | essenziale |
| AC-003 Scrittura interna solo da elenco chiuso | **si alleggerisce**: il livello sta in configurazione, nel codice solo i divieti | collo di bottiglia 5 [verificato: RAP2] |
| AC-004 Cancello che non risponde → chiamata bloccata | **resta**, in forma semplice: nessun effetto e la catena ritenta con la stessa chiave | costa poco ed evita danni |
| AC-005 Un effetto per giro | **si alleggerisce** e passa alla milestone S: un pacchetto interno più un solo elemento esterno | collo di bottiglia 4 [verificato: RAP2] |
| AC-006 Tre barriere provate una per una | **si toglie** la prova separata; la configurazione resta nella fase 2 | è sicurezza oltre l'essenziale per un sistema chiuso |
| AC-007 Classi vietate anche saltando l'hook | **resta**: i limiti fissi valgono anche chiamando direttamente l'API del Cancello | limite fisso |
| AC-008 Una carta scaduta non si esegue | **resta**, con la finestra L2 come caso nuovo | essenziale |
| AC-009 Ciò che esce è ciò che la persona ha visto | **si alleggerisce**: l'esecutore ricalcola l'impronta; escono i codici per consegna, l'impronta della Porta e il controllo dei caratteri invisibili | resta la garanzia vera |
| AC-010 Due approvazioni, un solo effetto | **resta**, senza numeri monouso | niente doppie mail |
| AC-011 Solo chi è approvatore oggi | **si alleggerisce**: approvatore e sostituto per classe in configurazione | siamo in quattro |
| AC-012 Richieste firmate | **si toglie**: basta un token per processo | sistema chiuso, rete interna |
| AC-013 Il testo di terzi non porta ad azioni | **resta**: è il cuore della corsia N | essenziale contro le iniezioni |
| AC-014 Registro dei profili con lista bianca | **si alleggerisce** e passa alla milestone S | non serve alla corsia N |
| AC-015 Stop di emergenza; nulla riparte da solo | **resta**, semplificato, senza epoche | limite fisso |
| AC-016 Registro a catena | **si toglie**: basta una tabella a sola aggiunta | registro semplice |
| AC-017 Segreti fuori dai registri | **resta** | costa poco |
| AC-018 Carta ferma per la notte | **resta**, come «carta o finestra ferma per la notte: la catena riprende con l'esito giusto» | è un criterio della settimana 8 [verificato: PRD «Metriche»] |
| AC-019 Riavvio a metà giro | **resta**, con e senza carta, sul registro degli eventi | niente doppi effetti, niente lavori persi |
| AC-020 Tre agenti e tre runner | **si toglie** dalla milestone 1; nella milestone S diventa «tre agenti, un runner, nessuno scambio di sessioni» | il runner è uno solo |
| AC-021 Tetti con riserve fra runner | **si alleggerisce**: tetto per lavoro, per mese e per classe al giorno | i tetti sono essenziali |
| AC-022 La sessione vede solo ciò che le passiamo | **passa** alla milestone S, con una prova sola | — |
| AC-023 Batteria di prove con un comando, gratis | **resta**: obbligatoria su Windows, al banco anche su Linux | le prove sono l'unica revisione obbligatoria |
| AC-024 Giro dal vivo e aggiornamento dell'SDK | **si sposta**: il giro dal vivo quando c'è la chiave, la parte SDK alla milestone S | oggi manca la chiave |
| AC-025 Un'esecuzione incerta non si ripete | **resta** | niente doppie mail |
| AC-026 Una proposta ripetuta non crea una seconda carta | **resta** | idempotenza |
| AC-027 Niente carte orfane né esiti persi | **resta**, alleggerito, sul registro degli eventi | — |

**Bilancio:** 14 criteri restano, 9 si alleggeriscono o si spostano, 4 si tolgono (AC-006, AC-012, AC-016, AC-020).

### 6.3 Criteri nuovi per l'autonomia

[proposta, dai criteri di P-A §7.2, P-C §7.3, P-D §7.4 e delle verifiche]

1. **N1 Finestra L2.** Senza «Ferma» l'azione parte una volta sola alla scadenza, in orario di lavoro. Con «Ferma» non parte e la terna torna a L1. Con «Invia ora» parte subito.
2. **N2 L3 entro i tetti.** L'azione parte subito e lascia una riga nel registro. Oltre il tetto giornaliero diventa una carta L1.
3. **N3 Destinatari dai dati.** Un destinatario fuori dalla classe fa scendere l'azione a L1. Vale anche per un indirizzo dello stesso dominio che non era in call.
4. **N4 Controllo del contenuto.** Cifre, prezzi o date d'impegno che non vengono dal CRM fanno scendere l'azione a L1.
5. **N5 Promozione e discesa.** I contatori propongono la promozione, ma promuove solo il responsabile. Ogni segnale del §2.4 abbassa la terna da solo.
6. **N6 «Annulla» e «Rettifica».** Una scrittura interna si annulla senza cancellare nulla. La rettifica crea una carta L1 e abbassa la terna.
7. **N7 Riga AI.** C'è in ogni uscita L2 e L3, e non c'è in quelle L1.
8. **N8 Soppressione.** Un «no» blocca le azioni verso quel contatto su tutti i canali.
9. **N9 Un crash non perde la call.** Se il post-call cade a metà, l'evento resta «ricevuto» e viene ripreso senza doppi effetti.
10. **N10 Nessun dato rosso nei database,** compreso quello di n8n quando arriva. Il criterio vale dalla milestone 4.

### 6.4 Milestone del PRD

| # | Milestone | Risultato | Prima era |
|---|---|---|---|
| 1 | Cancello a livelli e corsia N | sulle macchine di sviluppo una catena a schema propone azioni; L1, L2 e L3 escono solo al loro livello; i 14 criteri tenuti e i criteri N1-N9 passano con un comando | nucleo motore e Cancello |
| 2 | Prove con Microsoft e LiteLLM | bot Teams senza Azure; identità di chi preme e «Ferma» sulla carta; LiteLLM. Se fallisce, il piano B è una pagina del Cancello con accesso Entra | uguale, più «Ferma» |
| 3 | Telefono e posta verso il cliente | Alessandro approva dal telefono o lascia passare una finestra; la mail parte una volta sola e solo all'indirizzo esatto | uguale, con L2 |
| 4 | Dalla call al riassunto | lettore delta, registro degli eventi, oscuramento; ingresso nelle call Teams nostre; riassunto L3 nel canale interno; nessun dato rosso salvato | uguale |
| 5 | Tre agenti al lavoro | debrief L3 alle 7:00 (con n8n o un timer); post-call L3 interno; follow-up L1, o L2 per decisione; to-do in Jira se c'è margine | uguale, con i livelli |
| 6 | Collaudo della settimana 8 | criteri misurati, più tre metriche: minuti fra la fine della call e il follow-up, quota di azioni L2-L3, «Ferma» ogni 100 finestre | uguale, con le metriche nuove |
| 7 (fase 2) | Runner S e ponte | brief, offerta e Capo di gabinetto in sessioni SDK; criteri AC-005, 014, 020, 022 e 024 | nuovo |
| 8 (fase 2) | Bacheca e promozioni | canale «Agenti», freno, stand-up, nove bot, contatori attivi | prima nel blocco della fase 2 |

**La metrica del PRD «Effetti usciti senza carta: 0» diventa «Effetti usciti fuori dal loro livello: 0»** [verificato: PRD «Metriche»; P-A §7.4].

---

## 7. ADR

### 7.1 ADR nuove

| ADR | Titolo | Decisione in una frase | Alternative scartate |
|---|---|---|---|
| **0020** | Autonomia a livelli per terna | Il Cancello dà a ogni terna un livello da L0 a L3, con un tetto per classe, la finestra L2, la promozione confermata dal responsabile e la discesa automatica | carta per ogni azione (v2); regole «Sempre» dopo 20 sì per destinazione; partenza a L3 senza parere |
| **0021** | Motore a due corsie | Le catene deterministiche (N) e le sessioni dell'Agent SDK (S) stanno nello stesso codice TypeScript; la fase 1 usa solo la corsia N | logica nei flussi n8n (P-D: licenza, git solo Enterprise, nessuna ripresa); tutto in sessioni SDK (P-A: RAM e rischio sul ponte); Hermes (P-B: ADR-0012 non soddisfatta) |
| **0022** | Registro degli eventi e ingressi | Ogni avvio passa da `POST /eventi` con una chiave per evento; n8n fa solo orari e webhook; il delta di Graph lo legge il nostro codice | n8n come esecutore dei flussi; lettura dentro n8n con il token che avanza prima della registrazione dell'evento |
| **0023** | Protezioni essenziali per un sistema chiuso | Restano limiti fissi, stop, tetti, registro a sola aggiunta, «Annulla» e «Rettifica» e la conformità minima; escono FIDO2 sulle carte, firme HMAC, registro a catena e revisione esterna obbligatoria | lo spec della revisione 2 così com'è |
| **0024** | Abbonamenti come riserva | Managed Agents solo su dati verdi e solo se il server è pieno o fermo; i compiti programmati di Claude Team solo per uso personale | P-C come base: aggiunge fornitori e uno stop che non ferma tutto |

### 7.2 ADR da rivedere

| ADR | Revisione |
|---|---|
| 0001 | il motore resta sull'Agent SDK, ma come corsia S dalla fase 2; rimanda ad ADR-0021 |
| 0003 | «carta per ogni azione esterna» e FIDO2 lasciano il posto ad ADR-0020; il Cancello resta l'unico esecutore; la VM separata non è più obbligatoria |
| 0004 | al budget di LiteLLM si aggiunge il tetto per classe al giorno |
| 0010 | TypeScript confermato anche per la corsia N e per il Cancello |
| 0011 | n8n fa solo da avvio; la sezione «Rischi» aggiunge le regole sui dati delle esecuzioni e sugli orari persi |
| 0012 | Hermes resta una via d'uscita e un pilota in LAB; le quattro condizioni restano |
| 0013 | Postiz prima della fase F4 solo con il sì di Michele; fino ad allora l'esecutore Metricool |
| 0019 | la linea di riserva va messa prima del primo L3 esterno fuori orario e prima di Andrea |

---

## 8. Modifiche ai documenti

**docs/02-alternative.md**
- Aggiungere il **§9 «Terzo giro, 9-10 novembre: autonomia»**, con il criterio nuovo, le quattro proposte, la classifica, le verifiche e l'unione scelta.
- Correggere l'«In breve»: il motore resta, ma ha due corsie.

**docs/03-architettura.md**
- **§1 Principi:** aggiungere «autonomia per classe dentro limiti fissi», «il codice sceglie i destinatari» e «ogni agente legge le regole "Come lavoro"».
- **§2-3:** inserire la corsia N e la corsia S, il registro degli eventi, il lettore delta e il ruolo ristretto di n8n.
- **§4 Percorso di un'azione:** riscrivere il §4.1 (classi con livello, tetti, finestra) e il §4.3 (stop che annulla le finestre).
- **§8 Sicurezza e conformità:** applicare ADR-0023 e aggiungere la riga AI.
- **§9:** aggiungere Managed Agents come riserva, e i piloti di Buzz e Paperclip con i loro gp.

**docs/05-design.md**
- **§5.5 Regole e carte:** passare ai livelli. Al posto della regola 10 vale «una persona per ogni impegno, ogni primo contatto e ogni destinatario nuovo» [verificato: P-D §4.3].
- **§5:** aggiungere lo stand-up degli agenti e il freno nuovo.
- **§6 Una giornata:** il debrief elenca ciò che è partito da solo e le promozioni.
- **§7-8:** aggiornare «cosa resta umano» con il §2.8 di questa sintesi, e riportare le tabelle del §4.2 per le funzioni dalla fase 3 in poi.
- **Canali condivisi con i clienti, Telegram, Slack e WhatsApp:** scrive solo il Cancello, al livello della classe [verificato: P §4.11].

**docs/06-sviluppo.md**
- **§3 Piano a fasi:** la fase 1 usa solo la corsia N; runner S e bacheca all'inizio della fase 2; brief e bozza d'offerta nella fase 2 se c'è capacità. Le altre funzioni restano nelle fasi del §4.2.
- **§4 Verifiche:** criterio «nessun effetto fuori dal suo livello» e le misure d'autonomia. La revisione esterna esce dalla verifica della settimana 21.
- **§5 Stima dei giorni:** usare le cifre del §9.3 di questa sintesi.
- **§8 Spese:** usare il §9 di questa sintesi.

**Fuori dai quattro documenti:** quando si rigenera PRESENTAZIONE-CEO vanno allineati il §5.4, la regola 10 del §9.1, il §11 e la decisione 5 del §14 [verificato: P-D §7.5].

---

## 9. Spese rispetto alla v2.1

I CEO hanno dato carta bianca: questo elenco serve solo da riferimento [verificato: AGG].

### 9.1 Una tantum

| Voce | Rispetto alla v2.1 | Motivo |
|---|---|---|
| Revisione esterna di Cancello, motore e bot | **da −3.560 a −5.940 €**: diventa facoltativa | sistema chiuso; restano le prove e la revisione di Mattia [verificato: P §12.2, dec. 5] |
| Chiavi FIDO2 (232-464 €) | **invariata**: le chiavi restano per l'accesso al board con NetBird | escono solo come secondo passo sulle carte [verificato: R30 §1; VER3] |
| Parere legale | invariato (tetto 2.500 €), con due domande in più | la riga AI; il valore di un messaggio L2 |
| Linea di riserva 4G/5G | invariata (77-200 €), ma **anticipata** a prima del primo L3 esterno fuori orario o di Andrea | continuità [verificato: ADR-0019] |
| RAM, seconda GPU, vivavoce, attivazione della linea di Andrea, backup, batterie dell'UPS | importi invariati; per i tempi vedi il §11 | [verificato: P §12.2] |
| Piloti in LAB | Hermes 6-8 gp, Buzz 6 gp, Paperclip 2 gp; nessun costo in euro | confronto sui numeri [verificato: P §15; R36 §8.2] |

**Oggi la spesa una tantum resta di circa 2.900-3.890 €** [verificato: P §1].

### 9.2 Mensili

| Voce | Rispetto alla v2.1 | Motivo |
|---|---|---|
| Base, per tutte le fasi | **invariata**: circa 135 €/mese nelle fasi 0-1, 479-583 €/mese a listino a regime | nessun canone nuovo [verificato: P §12.1] |
| Linea di riserva | +10-11 €/mese, **da prima** | continuità del lavoro L3 |
| Slack e WhatsApp | invariati: Slack 0-27 €/mese, WhatsApp circa 7-12 €/mese, dalla fase 3 | erano già nella copertura della v2.1 [verificato: R36 §8.1, J9] |
| Metricool | nulla in più finché fa da ponte; −59,86 €/mese quando entra Postiz | [verificato: R36 §8.2] |
| API di Claude | stima invariata, 90-250 €/mese con un tetto di 250 €, da misurare nella fase 1: più autonomia vuol dire più lavori | [verificato: P §1, §14 dec. 3] |
| Riserve facoltative | Managed Agents circa 4-35 €/mese, se usato [stima di P-C]; voce di Andrea in cloud circa 88 €/mese, se la voce in casa non passa | [verificato: R36 §12] |

### 9.3 Giorni di sviluppo

La v2.1 stima 22,5-30 gp per la fase 1, 40,5-54 gp per le fasi 0-1 e 249-332 gp per tutto il piano. In ogni fascia la cifra più alta comprende una riserva di circa un terzo [verificato: P §15]. Le cifre nuove della tabella sono [stima].

| Periodo | Base | Con la riserva | v2.1 (base / con riserva) |
|---|---|---|---|
| Fase 1 | circa 20-23 gp | circa 27-31 gp | 22,5 / 30 [verificato: P §15] |
| Fasi 0-1 | circa 38-41 gp | circa 45-55 gp | 40,5 / 54 [verificato: P §15] |
| Totale del piano | circa 247-250 gp | circa 329-333 gp | 249 / 332 [verificato: P §15] |

**Come si arriva alla fase 1.** Si parte dai 22,5 gp di base della v2.1 [verificato: P §15], poi:
- si toglie la parte S del motore sul banco: circa −5;
- si tolgono le difese oltre l'essenziale: −3,5;
- si aggiungono livelli, finestra, promozioni, «Annulla» e controllo del contenuto: da +4 a +6;
- si aggiunge il registro degli eventi: +1.

**Confronto con la v2.1.**
- Il conto della base scende di circa 1-2 gp. Con la riserva, nel caso peggiore, si supera di circa 1 gp il tetto della v2.1 (55 contro 54 per le fasi 0-1).
- La capacità delle fasi 0-1 è di circa 52 gp [verificato: R36 §7.1]. Già con la v2.1 la riserva sfora alla settimana 9 [verificato: R36 §7.2], e questo resta vero.
- Il risparmio di P-D non è dimostrato [verificato: VER1, rilievo 8].

**Il vantaggio sta nell'ordine dei lavori, non nel totale.** La stima va rifatta con Mattia, pezzo per pezzo.

---

## 10. Rischi residui

| Rischio | Cosa resta | Cosa lo contiene |
|---|---|---|
| Una mail sbagliata arriva a un cliente senza che nessuno l'abbia letta | a L2 e L3 nessuno legge prima | indirizzo esatto, controllo del contenuto, riga AI, tetti, discesa automatica, rettifica; la classe torna a L1 con un tocco, a 0 € |
| Volumi bassi | L2 e L3 verso l'esterno arrivano tardi; alla settimana 8 il valore è soprattutto interno | partenza a L2 per decisione, dopo il parere; «prima il funnel» [verificato: P §7.1, §11] |
| Il parere dice no | follow-up e recap restano a L1 | resta il tempo risparmiato sulle bozze |
| Una lamentela non viene riconosciuta | la terna resta alta | risposte dubbie in carta; «sbagliato» nel debrief; resoconto mensile |
| Codice nostro senza revisione esterna | bug nel Cancello | prove a ogni modifica, idempotenza, esito «incerto» a una persona, Mattia sul codice; revisione esterna se un cliente la chiede |
| Capacità della fase 1 | la settimana 8 slitta alla 9 o alla 10 | to-do in Jira ed evento in calendario solo se c'è margine; corsia S nella fase 2 |
| Porta senza Azure | niente «Ferma» dal telefono | prova subito (milestone 2); piano B con la pagina del Cancello [verificato: PRD «Rischi»] |
| n8n | orari persi, vulnerabilità, la versione 3.0 che cambia l'API [verificato da RAP4 §5] | solo ruolo di avvio, versione 2.x fissata, «Run the Most Recent», controllo delle 7:15; un timer di sistema come ripiego |
| L'Agent SDK cambia quasi ogni giorno | un aggiornamento rompe la corsia S | versione fissata, prove; la corsia N non dipende da Claude Code [verificato: P §13] |
| Vexa nelle call di altri | il cliente non ammette il bot | registrazione sul PC come riserva [verificato: P App. A J5] |
| Buzz giovane | perde risposte e le approvazioni non sono pronte | resta in LAB; nel frattempo la stanza degli agenti è il canale «Agenti» in Teams [verificato: P §13] |
| Continuità 24 ore su 24 | una sola linea, riaccensione a mano, una sola GPU | §11 |
| Dati rossi | trascrizioni nelle cronologie | il testo rosso non entra in n8n; criterio N10 |
| Rivendita alle PMI | nessun rischio, perché la logica non sta in n8n | ADR-0021 |
| Più eventi, più token | la spesa sale | tetti per lavoro, per agente e per classe; Haiku sulla corsia N |

---

## 11. Hardware consigliato a Michele

| Cosa | Quando | Costo | Cosa sblocca | Fonte |
|---|---|---|---|---|
| **Riaccensione automatica dopo un blackout** (impostazione del BIOS o dell'iLO) | subito, prima del primo lavoro L3 notturno sul banco | 0 € | debrief e catene ripartono senza nessuno in ufficio; oggi il server va riacceso a distanza | DOM n. 22; P §13 |
| **Test delle batterie dell'UPS** | all'arrivo | 140-550 €, se il test va male | lo spegnimento ordinato regge e nessuna catena si perde a metà | ADR-0017; P §12.2 |
| **Backup 3-2-1** (PBS in sede) | fase 2, prima dei dati dei clienti | 165-500 € subito; 240-250 € entro marzo 2027 | i dati dei clienti stanno sul server dopo la settimana 21, senza la revisione esterna come condizione | ADR-0016; P §11 |
| **Linea di riserva 4G/5G** | prima del primo L3 esterno fuori orario e prima di Andrea, cioè in pratica all'inizio della fase 3 | 77-200 €, più 10-11 €/mese | follow-up, richiamate e routine continuano anche se cade la fibra | ADR-0019; P §14 dec. 13 |
| **RAM: altri 192 GB, fino a 384** | all'inizio della fase 3, o prima se il margine misurato con 6 sessioni scende sotto i 5 GB | 690-830 €, più 6-10 €/mese di corrente | Vexa nelle call di altri, 12-16 sessioni S, Andrea su CPU anticipato, crescita verso cento agenti | ADR-0015; P §6.3; R36 §4.2 |
| **Seconda GPU da 16 GB** (RTX PRO 2000 Blackwell) | dalla fase 3, appena il prezzo scende; all'inizio della fase 3 se Andrea viene anticipato | 880-1.220 €, più 3-8 €/mese | trascrizione in casa senza code mentre la RTX 4000 è prestata; voce di Andrea migliore; voce clonata del collega con Qwen3-TTS (fase 5); niente attese serali | ADR-0014; P §6.4, §14 dec. 12; P App. A, «Lacune dichiarate» |
| **Vivavoce da sala** | fase 3 | 100-250 € | le riunioni dal vivo entrano nel post-call | P §12.2; P App. A J5 |
| **Secondo nodo** (in programma a dicembre) | a scelta di Michele | fino a 1.500 € | può ospitare Cancello e Porta separati dal motore, o fare da riserva fredda; la scelta è sua | R37 §2 |

**Per l'autonomia l'ordine consigliato è questo** [proposta]:
1. riaccensione automatica;
2. batterie dell'UPS;
3. backup;
4. linea di riserva;
5. RAM;
6. seconda GPU.

I primi quattro rendono affidabile il lavoro L3 quando non c'è nessuno; gli ultimi due ne allargano il volume.

---

## 12. Da dove parte lo sviluppo

### 12.1 Milestone 1: Cancello a livelli e corsia N, sulle macchine di sviluppo

L'ordine di lavoro è [proposta]:

1. **Mezza giornata per il modello a copione dell'API Messages,** verificando anche che `embedded-postgres` 16 parta su Windows.
2. **Schemi e ruoli del database:** eventi, coda, terne e livelli, carte e finestre, outbox, registro a sola aggiunta, soppressione, stato dello stop.
3. **Cancello:**
   - classi da `config/livelli.yaml`, con i limiti fissi nel codice;
   - carte L1, finestre L2 e L3 entro i tetti;
   - controllo del contenuto e classe calcolata dai dati;
   - outbox con un solo effetto ed esito «incerto»;
   - «Annulla» e «Rettifica»;
   - stop;
   - contatori di promozione e discesa.
4. **Corsia N:** la catena «post-call» su una trascrizione verde di prova, con le regole «Come lavoro» caricate. Escono il riassunto a L3 nel canale interno, i campi del CRM, i to-do e la bozza del follow-up a L1 o L2.
5. **Porta di prova da terminale:** mostra la carta o la finestra, ha i tasti «Approva», «No», «Ferma», «Invia ora» e «sbagliato», e preme lo stop.
6. **Esecutori di prova:** posta, canale interno, Jira, calendario e CRM scrivono in `uscita_di_prova`.
7. **Batteria di prova:** i 14 criteri tenuti più N1-N9, con un comando e gratis.

**Alla fine si vede funzionare:**
- da un comando che inietta «trascrizione pronta», il riassunto esce a L3;
- il follow-up arriva come carta L1. Dopo 5 sì puliti il sistema propone la promozione; dopo il tocco del responsabile, la mail successiva parte a L2 dopo 30 minuti in orario di lavoro;
- un «Ferma» blocca la finestra e riporta la terna a L1;
- una cifra inventata nel testo fa scendere l'azione a L1;
- un collega dello stesso dominio non riceve nulla;
- lo stop annulla tutto e niente riparte da solo;
- un crash a metà catena non perde la call e non manda due mail.

**Stima:** circa 8-10 gp [stima, vicina a P-D §7.5 e P-B §7].

### 12.2 Milestone 2: prove con Microsoft e LiteLLM, in parallelo

- Il bot Teams senza Azure nel nostro tenant: la carta e la finestra con «Ferma» sul telefono, e l'identità di chi preme (`aadObjectId`) [verificato: R28 §2.3].
- La pagina del Cancello con Entra come piano B.
- LiteLLM davanti alle chiamate della corsia N, con un budget per catena.
- La scelta fra piano A e piano B, prima di scrivere la Porta vera.

**Si vede funzionare:** una carta vera in Teams sul telefono di Alessandro, con un «Ferma» registrato a suo nome.

### 12.3 Milestone 3: telefono e posta verso il cliente

- La Porta vera sostituisce quella di prova senza cambiare l'API del Cancello [verificato: SPEC §11].
- Un esecutore Outlook invia solo all'indirizzo esatto del partecipante registrato.
- Le mail con esito incerto vengono riconciliate.
- Le uscite L2 portano la riga AI.

**Si vede funzionare:** Alessandro approva una bozza dal telefono, oppure la lascia passare dopo 30 minuti, e la mail parte una volta sola e solo a quell'indirizzo.

**Le milestone successive:**
- la 4 porta sul banco il lettore delta di Graph con l'ingresso nelle call Teams nostre, l'oscuramento e n8n o un timer;
- la 5 mette al lavoro i tre agenti, con il debrief delle 7:00;
- la 6 è il collaudo della settimana 8;
- con la fase 2 arrivano il runner S e la bacheca (§6.4). Le funzioni dalla fase 3 in poi seguono il §4.2.

---

**File controllati il 10/11/2026:**
- `C:\Users\alber\sersan-agent-os\PRESENTAZIONE-CEO.md`: §4.1, §11, §15 e l'Appendice A per intero, comprese le «Lacune dichiarate»
- `C:\Users\alber\sersan-agent-os\ricerca\36-architettura-v2.md`: §4.1, §7.2, §7.3, §8.1, §8.2, §12, per Buzz, Paperclip e i canali
- `C:\Users\alber\sersan-agent-os\docs\superpowers\specs\2026-11-09-nucleo-motore-cancello-design.md`: §1-3, §9, §12
- `C:\Users\alber\sersan-agent-os\.claude\prds\sersan-agent-os.prd.md`
- l'elenco di `C:\Users\alber\sersan-agent-os\docs\adr\`, con le ADR da 0014 a 0019 per i costi dell'hardware
- i titoli delle sezioni di `docs\02`, `docs\03`, `docs\05` e `docs\06`
- `C:\Users\alber\Desktop\tracrizione bot aziendali.txt`: ho controllato solo che esistano i minuti citati

Il resto viene dai rapporti, dalle proposte, dai giudizi e dalle verifiche del giro.

**Una nota.**
- Il «suggerimento privato alla singola persona» del §4.2 non è una voce dell'Appendice A di P: è una mia proposta.
