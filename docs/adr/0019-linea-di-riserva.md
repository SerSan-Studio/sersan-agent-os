# ADR-0019: Linea internet di riserva 4G/5G, prima del primo lavoro L3 esterno fuori orario

**Data**: proposta del 2026-11-08 (registrata il 2026-11-09); accettata il 2026-11-10

**Stato**: accettata il 2026-11-10 dal gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026; operatore e router li sceglie Michele; la linea è anticipata a prima del primo L3 esterno fuori orario

**Chi decide**: Alessandro e Michele con la decisione 13, compreso a chi intestare la SIM; operatore e router li sceglie Michele ([proposta §14](../../PRESENTAZIONE-CEO.md); [DOMANDE-PER-MICHELE, domanda 24](../../DOMANDE-PER-MICHELE.md)).

## Contesto

L'ufficio ha una sola linea internet, la fibra TIM a 2,5 Gbit ([proposta §6.1](../../PRESENTAZIONE-CEO.md)). Il 7 novembre Michele ha deciso di non mettere per ora una linea di riserva e di aggiungere più avanti una 4G/5G o Starlink ([ricerca/37 §1](../../ricerca/37-hardware-risposte-michele.md)). Se cade la fibra gli agenti si fermano, perché ragionano con Claude via internet, e Andrea, l'assistente AI che parla al telefono con le lead, non risponde; nulla si perde, perché lavori e carte aspettano e ripartono quando la linea torna ([proposta §13](../../PRESENTAZIONE-CEO.md)). Dalla fase 5 (settimana 41) Andrea richiama al telefono le lead che lo chiedono ([proposta §11](../../PRESENTAZIONE-CEO.md)).

## Decisione

- **Prima della fase 5**, una linea 4G/5G con una SIM dati aziendale ([proposta §14, decisione 13](../../PRESENTAZIONE-CEO.md)), collegata a OPNsense, il firewall dell'ufficio, come seconda uscita: se la fibra cade, il firewall passa da solo sulla riserva (failover) ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Costo**: 77-200 € una tantum e 10-11 € al mese, IVA esclusa ([proposta §12.2](../../PRESENTAZIONE-CEO.md)). Per esempio Iliad Business Dati 180 a 9,99 € al mese o TIM Company Dati 100 GB a 10,99 €, con un router da circa 67 € (TP-Link Archer MR400) a circa 190 € (Teltonika RUT241), tutto IVA esclusa ([DOMANDE-PER-MICHELE, domanda 24](../../DOMANDE-PER-MICHELE.md)).
- L'operatore si sceglie misurando il segnale vicino al rack ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Regole d'uso** ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)): backup notturni e download grossi solo sulla fibra; Andrea si registra in uscita presso l'operatore telefonico, senza porte inoltrate; nessuna fiducia legata al solo indirizzo IP dell'ufficio, né in Entra, il sistema di accesso di Microsoft 365, né negli elenchi di indirizzi ammessi dei servizi esterni; una prova del passaggio di linea con una chiamata e una call Teams in corso.

## Alternative considerate

### Alternativa: nessuna linea di riserva

- **Pro**: nessuna spesa; è la scelta di Michele per ora ([ricerca/37 §1](../../ricerca/37-hardware-risposte-michele.md)).
- **Contro**: un guasto della fibra ferma gli agenti, Andrea e Teams in ufficio ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: dalla fase 5 Andrea risponde al telefono, e senza riserva un guasto della fibra lo ferma ([proposta §13](../../PRESENTAZIONE-CEO.md); [DOMANDE-PER-MICHELE, domanda 24](../../DOMANDE-PER-MICHELE.md)).

### Alternativa: Starlink Business

- **Pro**: non dipende dal segnale mobile; ha un indirizzo IP pubblico prenotato e un impegno di servizio al 99,9% ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Contro**: kit da 349 € e 31 € al mese per 50 GB, IVA esclusa ([proposta §12.2](../../PRESENTAZIONE-CEO.md)); oltre i 50 GB scende a 1 Mbit/s, salvo blocchi da 14 €; 75-100 W in più sull'UPS ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: costa di più; si prende solo se in ufficio il segnale mobile è scarso ([proposta §14, decisione 13](../../PRESENTAZIONE-CEO.md)).

### Alternativa: Starlink Residenziale o Standby

- **Pro**: il Residenziale costa 35 € al mese IVA inclusa, lo Standby circa 10 € al mese ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Contro**: il Residenziale è per uso domestico, sta dietro CGNAT, cioè un indirizzo condiviso che non accetta connessioni in entrata, e con il kit a noleggio non si mette in pausa; lo Standby va a 500 kbit/s e non è pensato per un uso costante ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: per l'ufficio di un'azienda Starlink indica il piano Business ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).

## Conseguenze

### Positive

- Se cade la fibra, la riserva tiene le connessioni in uscita: le API di Claude, Teams e la linea di Andrea, che si registra in uscita ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- L'accesso da fuori funziona anche sulla riserva, perché passa dalla macchina Oracle ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- Costa poco: 10-11 € al mese ([proposta §12.1](../../PRESENTAZIONE-CEO.md)).

### Negative

- Al passaggio da una linea all'altra le chiamate e le call Teams in corso cadono ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- I dati della SIM sono limitati: con quattro persone in video servono a stima circa 20 GB al giorno, quindi 180 GB coprono circa 8 giorni di uso pesante e 100 GB circa 4,6 ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).

### Rischi

- TIM chiede una partita IVA italiana e il contratto MultiBusiness, per Iliad il requisito non è verificato, e SerSan è una società inglese; senza partita IVA italiana restano le SIM per privati, intestate a una persona ([proposta §14, decisione 13](../../PRESENTAZIONE-CEO.md); [ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- Al passaggio sulla riserva le chiamate in entrata di Andrea si perdono finché il centralino non si registra di nuovo dalla nuova linea ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- Il segnale mobile vicino al rack non è ancora misurato ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).

## Revisione del 10 novembre 2026

- La spesa non aspetta più la decisione 13 dei CEO: il progetto è approvato. Tempi e acquisto li decide il gruppo di progetto con Michele ([ricerca/45](../../ricerca/45-architettura-v3.md), «Decisione del gruppo di progetto»).
- **La linea si anticipa**: va messa prima del primo lavoro L3 verso l'esterno fuori orario e prima di Andrea, cioè in pratica all'inizio della fase 3, non della fase 5 come diceva il titolo fino al 10 novembre ([ricerca/45 §9.1 e §11](../../ricerca/45-architettura-v3.md)).
- Il motivo è l'autonomia: con i livelli di [ADR-0020](0020-autonomia-a-livelli.md) follow-up, richiamate e lavori a orario partono senza nessuno in ufficio, e una caduta della fibra li fermerebbe.
- Nell'ordine consigliato a Michele per l'autonomia viene quarta: riaccensione automatica dopo un blackout, batterie dell'UPS, backup, linea di riserva ([ricerca/45 §11](../../ricerca/45-architettura-v3.md)).

## Fonti

- [Proposta per i CEO, §6.1, §11, §12.1, §12.2, §13 e §14 (decisione 13)](../../PRESENTAZIONE-CEO.md)
- [ricerca/37 §1, §3 e §4: risposta di Michele, costi e linea di riserva](../../ricerca/37-hardware-risposte-michele.md)
- [DOMANDE-PER-MICHELE: domanda 24](../../DOMANDE-PER-MICHELE.md)
