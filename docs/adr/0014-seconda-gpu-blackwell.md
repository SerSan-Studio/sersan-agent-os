# ADR-0014: Seconda GPU: RTX PRO 2000 Blackwell da 16 GB nel riser secondario

**Data**: proposta del 2026-11-08, da decidere (registrata il 2026-11-09)

**Stato**: proposta (decisione 12; modello scelto da Michele il 2026-11-07)

**Chi decide**: Alessandro e Michele approvano l'acquisto con la decisione 12; modello e montaggio sono scelte di Michele, a cui resta l'infrastruttura ([proposta §14](../../PRESENTAZIONE-CEO.md)).

## Contesto

Il server ha una sola GPU, una Quadro RTX 4000 da 8 GB, nel riser principale, cioè il supporto che ospita le schede aggiuntive: con il controller dei dischi quel riser è pieno ([proposta §6.1](../../PRESENTAZIONE-CEO.md)). La GPU calcola gli embedding, i vettori che rendono cercabile la memoria, fa girare il modello piccolo che prepara i documenti e trascrive le call; gli agenti ragionano con Claude via API e non la usano ([proposta §6.2](../../PRESENTAZIONE-CEO.md)). Nelle fasi 0-2 basta, perché le trascrizioni delle call in Teams arrivano già scritte da Microsoft. Dalla fase 3 (settimana 22) trascriviamo in casa anche le call dei clienti e la RTX 4000 è quasi piena; dalla fase 5 (settimana 41) la voce di Andrea, l'assistente AI che risponde e richiama al telefono, non può aspettare in coda. Intanto Michele presta ogni tanto la scheda alla postazione di prova del laboratorio, e i lavori della GPU aspettano ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).

## Decisione

- **Scheda**: NVIDIA RTX PRO 2000 Blackwell da 16 GB, scelta da Michele il 7 novembre ([ricerca/37 §1](../../ricerca/37-hardware-risposte-michele.md)). È la generazione successiva della RTX 2000 Ada che avevamo proposto: stessi 16 GB, 70 W presi dallo slot senza cavi di alimentazione, memoria più veloce. Ci stanno insieme trascrizione dal vivo, voce di Andrea e ricerca nella memoria, giorno e notte ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).
- **Montaggio**: slot 5 del riser secondario, con il kit HPE 870548-B21 che comprende la gabbia; la scheda occupa due slot e copre lo slot 4. Gli altri riser non accettano il suo connettore o costano di più ([ricerca/37 §4, Riser](../../ricerca/37-hardware-risposte-michele.md)). Il riser costa circa 75-160 € con IVA e spedizione, se manca; la versione PNY al dettaglio ha già la staffa ad altezza piena, con le altre la staffa costa circa 20 € ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).
- **Quando**: Michele la compra più avanti, quando il prezzo scende. La nostra proposta è comprarla appena torna sotto i 1.000 € IVA inclusa (circa 820 € esclusa), dalla fase 3, e comunque entro l'inizio della fase 5, anche se il prezzo non è sceso ([proposta §14, decisione 12](../../PRESENTAZIONE-CEO.md)).
- **Costo**: circa 880-1.220 € IVA esclusa, con riser e staffa se mancano ([proposta §12.2](../../PRESENTAZIONE-CEO.md)). Oggi in Italia la scheda costa circa 1.290-1.305 € IVA inclusa; la mediana dell'ultimo anno è intorno ai 985 € IVA inclusa ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: RTX 2000 Ada da 16 GB

- **Pro**: stessi 16 GB e 70 W, architettura matura per i programmi audio; a ottobre era la scheda che consigliavamo ([ricerca/32 §4.7](../../ricerca/32-hardware-e-upgrade.md)).
- **Contro**: memoria più lenta, 224 GB/s contro 288, e niente calcolo in FP4, cioè con numeri a 4 bit ([ricerca/32 §4.2](../../ricerca/32-hardware-e-upgrade.md)). Oggi in Italia costa circa 1.233 € IVA inclusa, e nelle offerte italiane lette il 7 novembre la Blackwell costa solo il 6% in più ([ricerca/37 §4, Seconda GPU](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: Michele ha scelto la Blackwell. La Ada torna interessante solo se scende sotto gli 800 € mentre la Blackwell resta sopra i 1.100 € ([ricerca/37 §4, Seconda GPU](../../ricerca/37-hardware-risposte-michele.md)).

### Alternativa: una scheda da 20-24 GB (RTX 4000 SFF Ada, RTX PRO 4000 Blackwell SFF, L4)

- **Pro**: oltre a trascrizione, voce e ricerca terrebbe sempre acceso anche un modello da 8 miliardi di parametri ([ricerca/32 §4.6](../../ricerca/32-hardware-e-upgrade.md)).
- **Contro**: costano da 2 a 4 volte una scheda da 16 GB; la L4 supera i 3.500 € ed è passiva, cioè raffreddata solo dall'aria del server, e non qualificata da HPE ([ricerca/32 §4.6 e §4.7](../../ricerca/32-hardware-e-upgrade.md)).
- **Perché no**: in casa girano solo modelli piccoli, perché gli agenti ragionano con Claude via API ([proposta §6.2](../../PRESENTAZIONE-CEO.md)); anche la GPU grande da circa 2.500 € della prima versione, pensata per i modelli locali, ha lasciato il posto a questa scheda ([proposta §12.2](../../PRESENTAZIONE-CEO.md)).

### Alternativa: restare con la sola RTX 4000

- **Pro**: nessuna spesa; nelle fasi 0-2 basta, e fino all'arrivo della seconda scheda fa tutto lei ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).
- **Contro**: dalla fase 3 è quasi piena, e quando va al laboratorio i lavori della GPU aspettano in coda ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **Perché no**: dalla fase 5 la voce di Andrea non può aspettare, e le voci migliori per Andrea girano sulla seconda GPU ([proposta §6.4 e §13](../../PRESENTAZIONE-CEO.md)).

## Conseguenze

### Positive

- Trascrizione dal vivo, voce di Andrea e ricerca nella memoria girano insieme sulla nuova scheda, giorno e notte ([proposta §6.4](../../PRESENTAZIONE-CEO.md)); la RTX 4000 resta per i lavori a lotti e per il laboratorio ([ricerca/32 §4.6](../../ricerca/32-hardware-e-upgrade.md)).
- A parte riser e staffa, se mancano, il server ha già quello che serve: seconda CPU, ventole e dissipatori adatti; a 70 W non serve un cavo di alimentazione ([ricerca/37 §4, Riser](../../ricerca/37-hardware-risposte-michele.md)). La corrente costa 3-8 € al mese ([proposta §12.1](../../PRESENTAZIONE-CEO.md)).

### Negative

- Spesa di circa 880-1.220 € IVA esclusa, con un prezzo oggi circa il 20% sopra quello di fine ottobre ([proposta §6.4 e §12.2](../../PRESENTAZIONE-CEO.md)).
- HPE non certifica due GPU di modelli diversi nello stesso server: la garanzia della scheda resta quella del venditore ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).
- Nel DL380 la scheda lavora in PCIe 3.0 x8, un collegamento più lento di quello che supporta: caricare un modello da 8-10 GB costa circa un secondo in più, con il modello già caricato non cambia nulla ([ricerca/37 §4, Seconda GPU](../../ricerca/37-hardware-risposte-michele.md)).

### Rischi

- CTranslate2 e faster-whisper, i motori della trascrizione, sulla Blackwell girano solo con la compilazione al volo; il servizio di trascrizione di Vexa, il bot che entra nelle call dei clienti, va ricostruito su CUDA 12.8 o successivo, la prima versione delle librerie di calcolo NVIDIA che supporta la Blackwell. Si prova tutto prima di spostare la trascrizione ([ricerca/37 §4, Seconda GPU](../../ricerca/37-hardware-risposte-michele.md); [DOMANDE-PER-MICHELE, domanda 18](../../DOMANDE-PER-MICHELE.md)).
- La staffa potrebbe non chiudere con il fermo della gabbia standard: in quel caso serve la gabbia HPE senza fermo P38515-B21, oggi poco disponibile ([ricerca/37 §4, Riser](../../ricerca/37-hardware-risposte-michele.md)).
- L'iLO, la console di gestione del server, non conosce la scheda: ventole e temperature vanno controllate prima e dopo il montaggio ([DOMANDE-PER-MICHELE, note](../../DOMANDE-PER-MICHELE.md)).

## Fonti

- [Proposta per i CEO, §6.1, §6.2, §6.4, §12.1, §12.2, §13 e §14 (decisione 12)](../../PRESENTAZIONE-CEO.md)
- [ricerca/32 §4: confronto tra le schede, prezzi e montaggio di ottobre](../../ricerca/32-hardware-e-upgrade.md)
- [ricerca/37 §1 e §4: risposte di Michele del 7 novembre, riser secondario, seconda GPU](../../ricerca/37-hardware-risposte-michele.md)
- [DOMANDE-PER-MICHELE: domande 17 e 18, note sulla GPU](../../DOMANDE-PER-MICHELE.md)
