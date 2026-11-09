# Compliance email — decisioni che il codice non può prendere

**Per chi:** Alessandro Serratt (founder) + consulente legale qualificato.
**Cosa non è:** una consulenza legale, e nemmeno un'affermazione che SerSan sia
conforme a qualcosa. Questo documento è scritto da chi ha costruito il sistema e
descrive **cosa il sistema fa oggi** e **quali domande restano senza risposta**.
Nessuna riga di codice può rispondere alle domande qui sotto.
**Stato al 2026-08-31:** ADR-004 in vigore (quattro deroghe), ADR-020 proposto e
non approvato, ADR-030 proposto e non approvato.
**Aggiornamento 2026-08-31:** due affermazioni di ADR-030 che il codice non
implementava sono state chiuse (addendum in ADR-030): il token è ora obbligatorio
anche su `POST /api/unsubscribe`, e la riga di readiness `email_compliance`
interroga davvero il valutatore, quindi una deroga nominata non può più produrre
un verde. **Nessuna deroga è stata aperta, chiusa o modificata.** Le domande qui
sotto restano tutte senza risposta, e §D2.3 ne guadagna una nuova.

**Aggiornamento 2026-09-09.** Il campo che apre le deroghe è ora **validato**, e
la decisione ha una **storia**. Nessuna deroga è stata aperta, chiusa o
modificata; è cambiato ciò che conta come decisione. Vedi §D0, che è la sola
sezione con un'azione da fare **subito**.

**Aggiornamento 2026-10-04.** Una decisione è stata **presa**: approvare lo
step 1 autorizza anche gli step 2..N della sequenza Instantly (§D6,
ADR-033). Nessuna
deroga è stata aperta, chiusa o modificata.

---

## D0 — Le decisioni richieste ADESSO, dopo il 2026-09-09

Questa sezione esiste perché una modifica di codice ha reso **inefficace** una
deroga che era in vigore. Non è una richiesta di riesame teorico: finché non è
chiusa, una campagna di produzione **non invia**.

### D0.1 — `Ricerca Clienti` deroga sotto l'autorità `sad`

**Oggi (misurato in produzione il 2026-09-09).** La campagna
`Ricerca Clienti` — prospect commerciali, non canary — invia derogando
`physical_address` e `sender_country`, e il campo che autorizza quella deroga
contiene la stringa **`sad`**.

Il codice accettava qualunque stringa non vuota. Da questa PR una deroga deve
**nominare una decisione**: chi ha deciso, quando, e dove è minutata (una data,
un ADR, una SO, una PR). `sad` non lo è, quindi la deroga **non è più in
vigore** e i due requisiti tornano «non decisi».

**Conseguenza pratica, immediata.** La campagna smette di inviare: la send lane
**trattiene** i messaggi in `approved` (non li fallisce — sono recuperabili al
beat successivo appena la posizione è chiusa). Nessun dato è perso e nessun
messaggio parte per errore.

**Cosa serve decidere, e da chi.** Una delle due, e sono alternative:

| | Azione | Chi |
|---|---|---|
| **A** | Compilare `physical_address` e `sender_country` con i valori veri (l'entità di ADR-004 è `SERSAN Limited, 128 City Road, London EC1V 2NX, UK`) — la campagna torna conforme e la readiness email può diventare verde | founder |
| **B** | Registrare la deroga per esteso: **autorità** (la decisione founder del 2026-04-29 / ADR-004 §D1-D3), **giurisdizione** (quale regime si applica), **motivazione** (perché è accettabile e fino a quando) — la campagna invia, e la readiness email resta **rossa** di proposito | founder + consulente legale |

Entrambe si fanno dalla pagina della campagna, scheda **Compliance**. Nessuna
delle due è eseguibile dal codice: la prima chiede un indirizzo che nessuno ha
dichiarato, la seconda una decisione che nessuno ha minutato.

### D0.2 — Quale giurisdizione, per questa campagna

**Oggi.** Il campo `compliance_jurisdiction` esiste ed è **vuoto su ogni
campagna**. È NULL perché NULL è la verità: nessuno l'ha dichiarata. Popolarla
con un default (`IT`, «facciamo outbound italiano») fabbricherebbe una decisione
che nessuno ha preso.

**Cosa serve decidere.** L'entità che invia è inglese (`SERSAN Limited`,
Londra); i destinatari del pilot sono italiani. CAN-SPAM, GDPR/ePrivacy e PECR
non sono lo stesso regime e non impongono le stesse cose. **Quale si applica, e
per quali destinatari?** La risposta va scritta nel campo, in modo che la
prossima revisione sappia da dove ripartire.

### D0.3 — ADR-030 è ancora PROPOSTO

**Oggi.** Il meccanismo di ADR-030 è in codice e ora è anche validato; la
**policy** no. Un ADR proposto è una proposta, e la riga di readiness
`email_compliance_enforced` resta rossa finché resta tale — correttamente.

**Cosa serve decidere.** Approvare ADR-030, respingerlo, o emendarlo. È l'unica
delle tre azioni che chiude la riga senza chiudere ogni singola deroga.

---

## Come leggere questo documento

Il sistema sa dire una cosa sola: **se i campi che una persona qualificata ha
indicato come necessari sono stati compilati.** Che quelli siano i campi giusti,
per quelle giurisdizioni e per quei destinatari, è esattamente ciò che serve
decidere qui.

Ogni voce ha tre parti: **cosa fa il sistema oggi** (fatto verificabile),
**cosa serve decidere** (domanda), **cosa cambia in pratica** (conseguenza
operativa della risposta).

---

## D1 — Indirizzo postale fisico

**Oggi.** `campaigns.physical_address` esiste ed è validato al confine dell'API
(min 20 caratteri, almeno una cifra, almeno una virgola — euristica dichiarata
debole). Dal 2026-08-30 il gate di go-live e la send lane lo **richiedono**,
salvo deroga nominata. Con la deroga registrata l'indirizzo non viene reso e non
compare nell'email; senza indirizzo e senza deroga la campagna non parte.
L'entità legale `SERSAN Limited, 128 City Road, London EC1V 2NX, UK` è
identificata in ADR-004 e **non è attualmente valorizzata su nessuna campagna**.

**Da decidere.**
1. Quale entità legale invia, per ciascuna campagna? Coincide sempre con
   SERSAN Limited, o alcune campagne inviano per conto di un cliente — e in quel
   caso l'indirizzo da mostrare è quello del cliente o il nostro?
2. Se l'entità è UK e i destinatari sono IT/UE, quale indirizzo soddisfa
   l'obbligo applicabile — e quale obbligo è applicabile?
3. CAN-SPAM §5(a)(6) si attiva sui destinatari US. La deroga attuale è
   accettabile finché i destinatari sono solo IT/UE: **chi verifica che lo
   siano**, e con quale controllo? Oggi nessun controllo lega il paese del
   destinatario alla posizione dichiarata della campagna.

**Conseguenza.** Deroga confermata → `compliance_derogation_authority`
valorizzato, readiness email resta rossa, esposizione invariata e minutata.
Deroga chiusa → `physical_address` valorizzato, `{{physical_address}}` torna nel
template e compare in fondo a ogni email.

---

## D2 — Link di disiscrizione cliccabile

**Oggi.** Esistono **due** meccanismi, e nessuno dei due è linkato dalle email:

- `POST /api/unsubscribe` — pubblico, senza chiave API. Dal 2026-08-31 richiede
  un **token HMAC** per `(tenant_code, indirizzo)`; prima si fidava di
  `{email, tenant_code}`, cioè di due valori pubblici per costruzione — il
  `tenant_code` vive nella pagina del cliente, l'indirizzo è il dato che chiunque
  faccia outbound raccoglie. Rate limit 10/minuto.
- `GET/POST /leads/<uuid>/unsubscribe/` — pagina pubblica con token HMAC legato
  a `(lead_id, email)`. Dal 2026-08-30 il token è **obbligatorio** (prima un POST
  senza token saltava la verifica).

Entrambi scrivono una soppressione **durevole** a livello di identificatore, che
sopravvive alla cancellazione e al re-import del lead, e propagano l'opt-out a
Instantly tramite outbox con retry. La propagazione è **trasversale ai tenant**
di proposito: rimuove la persona da tutte le sue campagne Instantly, «perché un
opt-out riguarda la persona, non il tenant che ospitava la pagina».

**Da decidere.**
1. Il meccanismo testuale «Rispondi STOP» è sufficiente per i destinatari
   previsti, o serve un link cliccabile? (Nota di merito, non legale: rispondere
   richiede al destinatario di comporre un'email.)
2. Se serve il link: quale delle due strade? Entrambe adesso autenticano. La
   differenza è operativa: la pagina Django costruisce il token da sé, l'endpoint
   REST richiede che chi genera le email emetta un URL per destinatario con
   `unsubscribe_token.mint()`.
3. ⚠️ **Domanda ancora aperta, e non è chiusa da questo lavoro.**
   `GET /leads/<uuid>/unsubscribe/` mostra l'indirizzo email del lead a chiunque
   presenti l'UUID, **e gli consegna il token valido per disiscriverlo**. Il
   token protegge dal POST cieco, non da chi apre prima la pagina: il
   dispensatore e la serratura sono lo stesso endpoint pubblico. Oggi regge
   sull'entropia dell'UUIDv4 (indovinarlo non è una strategia), quindi non è
   sfruttabile per enumerazione — ma **un UUID che trapela** (un log, un export
   CSV, un referrer, un ticket di supporto) diventa sia una divulgazione di dato
   personale sia una soppressione permanente. Due domande distinte:
   a. la pagina deve confermare senza **rivelare** l'indirizzo (mostrarne una
      forma mascherata, `p***@example.com`)?
   b. il token deve essere **portato nell'URL** dall'email — cioè emesso a monte
      e non dispensato dalla pagina — così che aprire la pagina senza token non
      dia più niente da usare?
   Sono lavoro contenuto, ma cambiano il contratto del link che finirà nelle
   email: vanno decise **prima** di chiudere D2, non dopo.
4. `EMAIL_UNSUBSCRIBE_TOKENLESS_AUTHORITY` riapre il percorso senza token per non
   spegnere di soppiatto una pagina cliente già in produzione. **Esiste una
   pagina cliente che chiama questo endpoint?** Se no, la variabile non va mai
   valorizzata e questa riga si può cancellare. Se sì: chi la mantiene, e in
   quanto tempo può passare ai token?

**Conseguenza.** Deroga chiusa → serve una riga di footer con URL per-lead e la
decisione su quale endpoint resta pubblico.

---

## D3 — Informativa privacy linkata

**Oggi.** Nessun link. Non richiede sviluppo: serve il documento pubblicato a un
URL stabile, poi è una riga di footer.

**Da decidere.** Chi redige l'informativa, dove viene pubblicata, e se il
titolare del trattamento è SerSan o il cliente per cui la campagna invia.

---

## D4 — Meccanismo di opt-out e sua tempistica

**Oggi.** La frase «Rispondi STOP per disattivare sequenza email» è presente
**da ogni step, incluso il primo** (soglia riportata a 1 il 2026-08-20, ADR-020
§1 — prima gli step 1 e 2 uscivano senza alcun meccanismo). Le risposte in
entrata sono analizzate automaticamente da
`workers/email/_compliance.py::is_opt_out_reply`, che de-quota la storia citata
prima di cercare le parole chiave — necessario perché ogni nostra email contiene
la frase, e un client di posta la cita indietro anche in una risposta
entusiasta. Il parser sbaglia **di proposito verso il falso negativo**: perdere
un opt-out automatico (che l'operatore vede comunque in Unibox) costa meno che
disiscrivere un lead interessato.

**Da decidere.**
1. Il periodo di conservazione del meccanismo: per quanto tempo dopo l'ultimo
   invio un destinatario deve poter esercitare l'opt-out? La soppressione oggi è
   **permanente e senza scadenza**, il che è più conservativo di qualunque
   requisito noto — va confermato che sia la scelta voluta.
2. Un opt-out su un canale deve fermare anche l'altro? **Oggi sì** — la
   soppressione è per identificatore e `backend/services/inbound.py` ferma
   entrambi i canali. È una scelta di prodotto che vale la pena confermare,
   perché è più larga di quanto molte norme richiedano.

---

## D5 — Le decisioni che ADR-004 non ha mai posto

Sono nuove: nessun documento precedente le affronta, e il sistema fino al
2026-08-30 non aveva un posto in cui scriverle.

| Campo | Domanda | Perché non ha un default |
|---|---|---|
| `sender_country` | Da quale paese invia l'entità? | Decide quale regime si applica. Non è deducibile dall'IP di un worker né dal dominio della mailbox. |
| `recipient_type` | `b2b`, `b2c` o `mixed`? | B2B e B2C non hanno lo stesso regime in nessuna delle giurisdizioni rilevanti. «Probabilmente B2B» non è una dichiarazione, e una lista importata da CSV può contenere indirizzi personali. |
| `lawful_basis` | Legittimo interesse, consenso, contratto, non applicabile? | È la scelta di chi risponde del trattamento. Se è legittimo interesse serve il bilanciamento, e il bilanciamento è un documento che oggi non esiste. |
| `compliance_approved_by` / `_at` | Chi si assume la responsabilità della posizione, e quando? | I campi sopra descrivono una posizione; questo dice che qualcuno l'ha approvata. Senza, la posizione è di nessuno. |

---

## D6 — Gli step 2..N di Instantly: chi li approva — **DECISO 2026-10-04**

**Oggi.** SerSan pusha il lead nella campagna Instantly una volta sola, quando
lo step 1 è approvato, con le variabili dello step 1. Gli step 2..N li manda
Instantly da solo, dai template della sequenza sincronizzati da SerSan e con
quelle variabili. Nessuno step successivo ha una riga `approved` sua, e dal
2026-10-04 SerSan non bozza più quegli step (`sequence_advance.py` è rimossa):
le bozze che creava non cambiavano ciò che parte.

**Decisione** (ADR-033,
Alberto Tuveri insieme ad Alessandro Serratt, 2026-10-04). L'approvazione umana
dello step 1 autorizza anche gli step 2..N, così come la sequenza è
sincronizzata in quel momento. Un template cambiato dopo si rivede a livello di
sequenza.

**Conseguenza.** La decisione regge finché restano veri tre guardrail:
`stop_on_reply` acceso, il footer di opt-out su ogni step (soglia 1, §D4) e la
revisione della sequenza. Se uno di questi cade, o se cambia la soglia del
footer, la decisione va riaperta. La decisione non dice niente sulla
conformità degli step 2..N (ADR-033 §6): le domande 4 e 5 qui sotto valgono per
**ogni** step, non solo per il primo.

---

## Domande per il consulente legale

Poste come le porrebbe chi ha scritto il sistema, non come le porrebbe un
avvocato. Vanno riformulate da chi risponde.

1. **Perimetro.** Con entità UK e destinatari IT/UE, quali regimi si applicano
   simultaneamente al cold outbound B2B — GDPR, PECR, il recepimento italiano
   della ePrivacy, altro? Cambia se un destinatario è US?
2. **Base giuridica.** Il legittimo interesse regge per cold outbound B2B nelle
   giurisdizioni di cui sopra? Se sì, serve un bilanciamento documentato, e con
   quale contenuto minimo?
3. **Indirizzo postale.** Quale obbligo di indirizzo si applica a un'entità UK
   che scrive a destinatari IT/UE, indipendentemente da CAN-SPAM?
4. **Opt-out.** «Rispondi STOP» soddisfa il requisito di meccanismo di
   opposizione, o serve un meccanismo che non richieda di comporre un messaggio?
5. **Conservazione.** Per quanto deve restare esercitabile il meccanismo dopo
   l'ultimo contatto? La soppressione permanente crea di per sé un problema di
   minimizzazione (conserviamo indirizzi per non contattarli)?
6. **Titolarità.** Quando SerSan invia per conto di un cliente, chi è titolare e
   chi responsabile? Cambia l'entità da nominare nell'email?
7. **Esposizione pregressa.** Gli invii già effettuati sotto le deroghe ADR-004
   creano un'esposizione retroattiva che richiede un'azione, o la decisione
   riguarda solo gli invii futuri?
8. **Soppressioni scritte senza autenticazione.** Fino al 2026-08-31
   `POST /api/unsubscribe` accettava una disiscrizione da chiunque conoscesse un
   `tenant_code` e un indirizzo. Non risulta che sia stato sfruttato — e non
   risulta nemmeno il contrario, perché non c'era niente che distinguesse una
   richiesta legittima da una fabbricata. Due domande, la prima per il founder e
   la seconda per il legale:
   a. **(operativa, per Alex)** vale la pena passare al setaccio le soppressioni
      con `source='public_unsubscribe'` per capire se il volume e la
      distribuzione temporale sono compatibili con opt-out reali? È l'unica
      verifica possibile a posteriori, ed è una lettura, non una modifica.
   b. **(legale)** se una soppressione risultasse non richiesta
      dall'interessato, l'evento ha rilevanza di notifica — o è semplicemente un
      dato commerciale perso? La domanda non è oziosa: la soppressione è
      *conservativa* verso il destinatario (smette di ricevere email), quindi il
      danno cade su SerSan e sul cliente, non sulla persona.

---

## Cosa il sistema verifica adesso su una deroga (2026-09-09)

Tre condizioni, e **nessuna delle tre dice se la deroga sia lecita**. Quella
domanda è tutta in questo documento e la risponde una persona.

1. **L'autorità nomina una decisione** — almeno 20 caratteri, più di una parola,
   e un appiglio verificabile (una data, `ADR-nnn`, `SO-nnn`, `#nnn`). Serve
   perché un revisore abbia dove andare a controllare.
2. **La giurisdizione è dichiarata** — CAN-SPAM, GDPR/ePrivacy e PECR non sono
   lo stesso regime, e una deroga che non dice a quale si riferisce non si può
   nemmeno rivedere.
3. **La motivazione è scritta** — è il testo che si legge la volta dopo, quando
   la decisione va riesaminata.

Ogni cambiamento della posizione lascia una riga in
`campaign_compliance_decisions` (append-only, con prima/dopo e l'effetto sul
verdetto), leggibile da `GET /api/campaigns/{id}/compliance-history`. Una
decisione sostituita senza traccia di ciò che sostituiva non è una revisione.

⚠️ **Il canary resta esente**, e l'esenzione resta stretta: una campagna canary
può raggiungere solo gli indirizzi in `canary_recipients`, cioè caselle
dell'operatore, quindi non è email commerciale verso un prospect. L'esenzione
vale finché è l'allow-list a tenerla lontana dai prospect.

---

## Cosa NON è stato fatto, e perché

- **Nessuna deroga è stata revocata.** ADR-004 registra una decisione founder
  esplicita e minutata. Questo lavoro la rende rappresentabile, non la ribalta:
  con `compliance_derogation_authority` valorizzato le campagne inviano
  esattamente come prima.
- **Nessun valore è stato inventato.** La migration non fa backfill. Nessuna
  campagna ha ricevuto un `sender_country`, un `recipient_type` o una
  `lawful_basis` di default: sarebbero stati fabbricati da chi non ha
  l'autorità per deciderli.
- **Nessuna affermazione di conformità.** Il codice verifica la presenza di
  campi, non la loro sufficienza giuridica.
- **La readiness email resta rossa.** Anche con ogni deroga regolarmente
  registrata. È la descrizione onesta di «inviamo sotto un'esposizione
  accettata», e distinguerla da «siamo conformi» è il punto dell'intero lavoro.
