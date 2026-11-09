# ADR-0017: Rack: firewall Sophos SG 230 con Proxmox e OPNsense, UPS HPE R1500 G5 con spegnimento a livelli

**Data**: 2026-11-05 (registrata il 2026-11-09)

**Stato**: accettata (Michele, 2026-11-05)

**Chi decide**: Michele, che ha disegnato il rack e comprato i pezzi con il budget hardware del board; Alessandro e Michele approvano le batterie nuove dell'UPS, se servono (decisione 4), e l'eventuale abbonamento Proxmox sul firewall (decisione 17) ([proposta §14](../../PRESENTAZIONE-CEO.md)).

## Contesto

Il rack da 12 unità nell'ufficio di Cagliari ospita server, firewall e UPS ([proposta §6.1](../../PRESENTAZIONE-CEO.md)). Il board di ottobre metteva OPNsense, il firewall open source, su un mini PC a quattro porte, teneva l'UPS che c'era e prevedeva più avanti un UPS da rack, APC SMT1500 o Eaton 5PX ([SerSan Infra Board](../../allegati/infra/SerSan%20Infra%20Board.md)); a ottobre consigliavamo l'Eaton 5PX 1500 G2 ([ricerca/32 §6](../../ricerca/32-hardware-e-upgrade.md)). Con la seconda GPU e 384 GB di RAM il picco stimato di server, firewall e rete arriva a 860-945 W ([ricerca/37 §4, UPS](../../ricerca/37-hardware-risposte-michele.md)). La board del rack del 5 novembre fissa le due scelte dentro il budget hardware del board: circa 2.975 € spesi su 3.200 € ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md)).

## Decisione

- **Firewall**: un Sophos SG 230 rev. 2 da rack, pagato 217,80 €. Michele non usa il software Sophos: ci mette Proxmox, il sistema che fa girare le macchine virtuali, con OPNsense in una macchina virtuale e, in contenitori leggeri, NetBird, la rete privata per entrare da fuori, il filtro DNS, NUT (il programma che legge lo stato dell'UPS) e più avanti il QDevice, cioè il voto che fa da arbitro nel cluster a due server ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md); [proposta §6.1](../../PRESENTAZIONE-CEO.md)). Proxmox e OPNsense si aggiornano dai loro progetti. La fibra a 2,5 Gbit entra in una porta da 1 Gbit e rende circa 940 Mbit/s, che per noi bastano ([DOMANDE-PER-MICHELE, note](../../DOMANDE-PER-MICHELE.md)).
- **UPS**: un HPE R1500 G5 da rack usato, 1.550 VA e 1.100 W, pagato 255 € ([proposta §6.1 e §12.2](../../PRESENTAZIONE-CEO.md)). Le sei prese sono in tre gruppi: il primario per firewall, terminale della fibra, router e backup in sede; il gruppo 1 per i due alimentatori del server; il gruppo 2 per il secondo server. Il Sophos legge l'UPS via USB ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md)).
- **Spegnimento a livelli**: se manca la corrente, dopo 3 minuti il server si spegne in modo pulito e la rete resta accesa fino a fine batteria; al ritorno della corrente la rete, se si era spenta, riparte da sola, mentre il server, com'è impostato oggi, va riacceso a distanza ([proposta §6.1](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: OPNsense su un mini PC, come nel board di ottobre

- **Pro**: quattro porte da 2,5 Gbit, adatte alla fibra ([SerSan Infra Board](../../allegati/infra/SerSan%20Infra%20Board.md)); circa 12 W contro i 22-30 W stimati per il Sophos ([ricerca/37 §4, Firewall](../../ricerca/37-hardware-risposte-michele.md)).
- **Contro**: quattro porte in tutto. Nella board del rack il Sophos ne usa otto, sei in rame e due SFP, cioè prese per moduli di rete intercambiabili, per fibra, server, console del server, backup in sede, access point, UPS e secondo server ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: Michele ha scelto il Sophos da rack. Un piccolo computer ancora supportato dal produttore resta la strada se l'ente che certifica Cyber Essentials, lo standard di sicurezza britannico, non accetta il Sophos ([proposta §13](../../PRESENTAZIONE-CEO.md)).

### Alternativa: un UPS nuovo da rack (Eaton 5PX 1500 G2 o APC SMT1500)

- **Pro**: nuovi, con batterie nuove; l'Eaton ha 1.500 W e al picco con due GPU lavorerebbe al 53-57% ([ricerca/32 §6](../../ricerca/32-hardware-e-upgrade.md)).
- **Contro**: l'Eaton costa 937-1.144 € IVA esclusa; l'APC costa 1.011 € IVA esclusa e con 1.000 W al picco arriverebbe all'80-85% ([ricerca/32 §6](../../ricerca/32-hardware-e-upgrade.md)).
- **Perché no**: l'HPE usato a 255 € regge il picco stimato, 860-945 W, cioè il 78-86% dei suoi 1.100 W, con 6-7 minuti di autonomia; il risparmio è di circa 670-920 € ([ricerca/37 §4, UPS](../../ricerca/37-hardware-risposte-michele.md)).

## Conseguenze

### Positive

- Firewall e UPS sono già comprati con il budget del board, e l'UPS costa molto meno dell'Eaton messo in conto a ottobre ([proposta §12.2](../../PRESENTAZIONE-CEO.md)).
- Il server si spegne in modo pulito, e la rete resta accesa o, se si era spenta, riparte da sola: così il server si può riaccendere a distanza ([proposta §6.1](../../PRESENTAZIONE-CEO.md)).
- Quando arriva il secondo server il Sophos fa da arbitro: se uno dei due si ferma, l'altro continua da solo ([proposta §6.1](../../PRESENTAZIONE-CEO.md)).

### Negative

- Il Sophos SG 230 rev. 2 è fuori supporto dal 30 giugno 2026: BIOS e processore non ricevono più correzioni ([proposta §6.1](../../PRESENTAZIONE-CEO.md)).
- Le batterie dell'UPS sono usate e senza garanzia: se il test di autonomia all'arrivo va male servono circa 140-550 € ([proposta §12.2](../../PRESENTAZIONE-CEO.md)).
- Dopo un blackout, finché il server non viene riacceso, restano fermi gli agenti e, dalla fase 5, Andrea, l'assistente AI che parla al telefono, a meno che Michele non imposti il server per ripartire da solo ([proposta §13](../../PRESENTAZIONE-CEO.md); [DOMANDE-PER-MICHELE, domanda 22](../../DOMANDE-PER-MICHELE.md)).
- Con il secondo server sul gruppo 2, al picco i due server possono superare i 1.100 W: servirà un tetto di potenza o un secondo UPS ([DOMANDE-PER-MICHELE, domanda 20](../../DOMANDE-PER-MICHELE.md)).

### Rischi

- Cyber Essentials: prima chiediamo per iscritto all'ente di certificazione se accetta OPNsense aggiornato su questo hardware; se non lo accetta, OPNsense passa su un piccolo computer ancora supportato, con una spesa da preventivare ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- Nella board la fibra entra in E0 e il collegamento al server esce da E1, la stessa coppia di porte con bypass: se il bypass scatta a Sophos spento, la fibra resta collegata direttamente alla rete del server. Il bypass va disattivato nel BIOS e provato, oppure la fibra va su un'altra porta ([DOMANDE-PER-MICHELE, domanda 8](../../DOMANDE-PER-MICHELE.md)).
- I 3 minuti vengono dalla board; nel messaggio del 7 novembre Michele parla di circa 30 minuti di autonomia: va confermato quale valga ([DOMANDE-PER-MICHELE, domanda 21](../../DOMANDE-PER-MICHELE.md)).
- L'R1500 G5 non è nella lista di compatibilità di NUT: il collegamento USB va provato all'arrivo ([DOMANDE-PER-MICHELE, note](../../DOMANDE-PER-MICHELE.md)).

## Fonti

- [Proposta per i CEO, §6.1, §12.2, §13 e §14 (decisioni 4 e 17)](../../PRESENTAZIONE-CEO.md)
- [ricerca/37 §1, §2 e §4: risposte di Michele, board del rack, firewall, UPS](../../ricerca/37-hardware-risposte-michele.md)
- [ricerca/32 §6: UPS consigliato a ottobre](../../ricerca/32-hardware-e-upgrade.md)
- [Rack SerSan 12U: board del rack del 5 novembre](../../allegati/infra/Rack%20SerSan%2012U.md)
- [SerSan Infra Board: board di ottobre](../../allegati/infra/SerSan%20Infra%20Board.md)
- [DOMANDE-PER-MICHELE: domande 8, 12 e 20-22, note](../../DOMANDE-PER-MICHELE.md)
