# ADR-0020: Autonomia a livelli per terna, decisa dal Cancello

**Data**: 2026-11-10

**Stato**: accettata

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Il livello di partenza di ogni classe lo fissa il gruppo di progetto, scrivendo il motivo; la promozione di una terna la conferma il responsabile della squadra ([ricerca/45 §2.3 e §2.4](../../ricerca/45-architettura-v3.md)).

## Contesto

- Nella v2 ogni azione esterna diventava una carta, cioè una richiesta di approvazione in Teams. Dopo 20 sì uguali una persona poteva creare una regola «Sempre» per una sola destinazione, che scadeva dopo 30 giorni ([ADR-0003](0003-cancello-approvazioni.md)).
- Il terzo giro ha misurato l'autonomia del disegno v2 e ha trovato 15 colli di bottiglia. Fra questi: la regola «Sempre» vale per una destinazione, mentre l'esempio della proposta parla di un gruppo di destinatari ([ricerca/39, «I 15 colli di bottiglia»](../../ricerca/39-autonomia-del-disegno-v2.md)).
- La trascrizione di riferimento mostra azioni verso l'esterno senza nessuno che approvi: il post-call che scrive al cliente e aggiorna il CRM, la richiamata delle lead entro 90 secondi, il coaching dopo ogni call ([ricerca/41 §8](../../ricerca/41-novita-al-9-novembre.md); [ricerca/38 §4](../../ricerca/38-autonomia-nella-trascrizione.md)).
- Nel giudizio del terzo giro l'autonomia pesava 35 punti su 100. Tutte e quattro le proposte chiedevano un Cancello a livelli ([ricerca/45, intestazione e §1.2](../../ricerca/45-architettura-v3.md)).
- I volumi di oggi sono bassi: al 5 ottobre c'erano 11 lead, 1 risposta e 0 meeting. Un contatore di approvazioni non si riempie in 4 settimane ([ricerca/45 §2.3](../../ricerca/45-architettura-v3.md); [ricerca/44, rilievo 2 di VER1](../../ricerca/44-verifiche-avversarie.md)).

## Decisione

**Quattro livelli** ([ricerca/45 §2.1](../../ricerca/45-architettura-v3.md)):

| Livello | Cosa vuol dire |
|---|---|
| L0 a mano | l'agente prepara, una persona esegue |
| L1 carta | l'agente propone, una persona approva ogni singola azione |
| L2 finestra | l'azione parte da sola dopo una finestra in cui una persona può fermarla |
| L3 autonomo | l'azione parte subito, dentro regole, tetti e registro; le persone vedono dopo e possono revocare |

- **L'unità è la terna**: agente, tipo d'azione, classe di destinatari. Per un singolo destinatario si può fissare un'eccezione, per esempio «solo con revisione» ([ricerca/45 §2.1](../../ricerca/45-architettura-v3.md)).
- **La classe la calcola il Cancello dai dati**: calendario, partecipanti registrati, CRM. Non la prende mai da ciò che dichiara l'agente né dal testo di una mail ([ricerca/45 §2.1](../../ricerca/45-architettura-v3.md)).
- **Ogni classe ha una partenza e un tetto.** Esempi: interno parte e resta a L3; contatto in conversazione parte a L1 e arriva a L3 dopo il parere; impegni (offerte, contratti, fatture, prezzi) e destinatari nuovi restano sempre a L1; pagamenti a L0; cancellazioni e credenziali sono vietate. La tabella completa sta in [ricerca/45 §2.2](../../ricerca/45-architettura-v3.md).
- **D11, persona appena incontrata.** È l'indirizzo esatto di chi era in una call registrata e avvisata negli ultimi 14 giorni; il dominio da solo non basta mai. Per decisione del gruppo di progetto parte a L2, con una finestra di 30 minuti. Gli invii veri ai clienti cominciano con la milestone di telefono e posta, la 4 del PRD (la 3 nel conto di ricerca/45): se prima di allora il parere legale lo esclude, la classe torna a L1 cambiando una riga di configurazione ([ricerca/45, «Decisione del gruppo di progetto», e §2.2](../../ricerca/45-architettura-v3.md)).
- **Dove sta ogni cosa**: partenze, tetti e motivi in `config/livelli.yaml`, in git nella repo del codice; il livello attuale di ogni terna nel database del Cancello; i limiti fissi nel codice ([ricerca/45 §2.3](../../ricerca/45-architettura-v3.md)).
- **Promozione**, sempre confermata dal responsabile con un tocco sulla proposta che arriva nel suo debrief ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)):
  - da L1 a L2 dopo 5 sì di fila senza modifiche di sostanza, e nessun segnale negativo negli ultimi 30 giorni. È di sostanza una modifica al destinatario, all'oggetto o a più del 10% del testo;
  - da L2 a L3 dopo 15 finestre di fila senza «Ferma» e senza segnali negativi negli ultimi 60 giorni;
  - mai oltre il tetto della classe.
- **Discesa automatica e immediata.** Un «Ferma» per errore, una «Rettifica», una lamentela, un «sbagliato» nel debrief o un rimbalzo fanno scendere la terna di un livello. Due segnali in 30 giorni la riportano a L1. Un cambio di modello o di istruzioni senza valutazione la riporta a L1. Lo stop di emergenza porta tutto a L0. Abbassare un livello può chiunque dei quattro; alzarlo solo il responsabile ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)).
- **Finestra L2.** La carta dice «parte alle HH:MM» e ha tre tasti: «Ferma», «Modifica», «Invia ora». La finestra conta solo in orario di lavoro, dalle 8:30 alle 19:00 dal lunedì al venerdì (D9). Dura 30 minuti per follow-up e recap, 60 per le risposte ai contatti in conversazione, 24 ore per post aziendali e solleciti, 48 ore per newsletter, inviti agli eventi e aperture di Andrea ([ricerca/45 §2.6](../../ricerca/45-architettura-v3.md)).
- **Riga AI.** Ciò che parte a L2 o a L3 porta una riga che dichiara l'assistente AI di SerSan; ciò che esce a L1 esce a nome di chi approva. Il testo definitivo lo fissa il parere (D8) ([ricerca/45 §2.6 e §5](../../ricerca/45-architettura-v3.md)).
- **Controllo del contenuto.** Prima di ogni uscita L2 o L3 un passo a schema cerca cifre, prezzi, sconti, date di consegna e impegni che non vengono dal CRM. Se ne trova uno, l'azione scende a L1 ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)).
- **Tetti giornalieri** (D10): 15 follow-up e 10 inviti al giorno per agente in ogni classe esterna a L3, e al massimo 2 messaggi al giorno per destinatario. Oltre il tetto l'azione diventa una carta L1 e non si perde ([ricerca/45 §2.7](../../ricerca/45-architettura-v3.md)).
- **Scadenza delle carte** (D1): 3 giorni lavorativi, 24 ore per ciò che dipende dal tempo ([ricerca/45 §5](../../ricerca/45-architettura-v3.md)).

## Alternative considerate

### Alternativa: una carta per ogni azione esterna, come nella v2

- **Pro**: nessun messaggio esce senza che una persona l'abbia letto ([ADR-0003](0003-cancello-approvazioni.md)).
- **Contro**: ogni follow-up aspetta una persona, anche di notte e nel fine settimana; il disegno resta lontano dalla trascrizione di riferimento ([ricerca/39, «I 15 colli di bottiglia»](../../ricerca/39-autonomia-del-disegno-v2.md)).
- **Perché no**: l'autonomia è il criterio con più peso del giro; con i livelli una classe torna a L1 con un tocco, a 0 € ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).

### Alternativa: regole «Sempre» dopo 20 sì per destinazione

- **Pro**: era già nella proposta v2.1, con la scadenza dopo 30 giorni ([ADR-0003](0003-cancello-approvazioni.md)).
- **Contro**: vale per una sola destinazione e con i volumi di oggi 20 sì non arrivano; non è definito cosa sia «uguale» né come si rinnovi la regola ([ricerca/39, «I 15 colli di bottiglia»](../../ricerca/39-autonomia-del-disegno-v2.md)).
- **Perché no**: la classe di destinatari calcolata dai dati copre lo stesso caso per un gruppo intero, con soglie più basse (5 e 15) che tutti i giudici hanno chiesto ([ricerca/45 §1.2](../../ricerca/45-architettura-v3.md)).

### Alternativa: partenza a L3 senza aspettare il parere

- **Pro**: è il livello della trascrizione di riferimento, subito ([ricerca/41 §8](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: il Garante applica l'art. 130 anche agli indirizzi aziendali, e il soft spam vale solo per i propri clienti ([ricerca/45 §2.2](../../ricerca/45-architettura-v3.md); [ricerca/16](../../ricerca/16-gdpr-ai-act-e-regole.md)).
- **Perché no**: le classi esterne arrivano a L3 solo dopo il parere e le finestre pulite; la partenza a L2 della persona appena incontrata è il passo più lungo che il gruppo di progetto si prende ([ricerca/45 §2.3](../../ricerca/45-architettura-v3.md)).

## Conseguenze

### Positive

- Il riassunto dopo la call, il debrief e le scritture interne partono a L3 dalla fase 1 ([ricerca/45 §4.1](../../ricerca/45-architettura-v3.md)).
- Le promozioni arrivano dentro il debrief, così non diventano una coda di carte ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)).
- Il criterio della settimana 8 diventa «nessun effetto fuori dal suo livello» ([ricerca/45 §6.4](../../ricerca/45-architettura-v3.md)).

### Negative

- A L2 e a L3 nessuno legge prima: una mail sbagliata può arrivare a un cliente ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).
- Il Cancello cresce: livelli, finestre, contatori, controllo del contenuto e «Annulla» valgono circa 4-6 giorni di sviluppo in più nella fase 1 ([ricerca/45 §9.3](../../ricerca/45-architettura-v3.md)).

### Rischi

- **Una lamentela non riconosciuta** lascia alta la terna: le risposte dubbie vanno in carta, c'è «sbagliato» nel debrief e le classi si rivedono ogni mese nel resoconto ([ricerca/45 §2.4 e §10](../../ricerca/45-architettura-v3.md)).
- **Il parere dice no**: follow-up e recap restano a L1, e resta il tempo risparmiato sulle bozze ([ricerca/45 §2.8 e §10](../../ricerca/45-architettura-v3.md)).
- **Volumi bassi**: alla settimana 8 il valore è soprattutto interno ([ricerca/45 §10](../../ricerca/45-architettura-v3.md)).

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §1.2, §2, §4.1, §5, §6.4, §9.3, §10](../../ricerca/45-architettura-v3.md)
- [ricerca/38, autonomia nella trascrizione, §4](../../ricerca/38-autonomia-nella-trascrizione.md)
- [ricerca/39, autonomia del disegno v2, «I 15 colli di bottiglia»](../../ricerca/39-autonomia-del-disegno-v2.md)
- [ricerca/41, novità al 9 novembre, §8](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/42, proposta A §3](../../ricerca/42-proposta-A-motore-a-livelli.md) e [proposta D §3.3](../../ricerca/42-proposta-D-automazione-prima.md)
- [ricerca/44, verifiche avversarie](../../ricerca/44-verifiche-avversarie.md)
- [ricerca/16, GDPR, AI Act e regole](../../ricerca/16-gdpr-ai-act-e-regole.md)
- [ADR-0003](0003-cancello-approvazioni.md), rivista da questa ADR
