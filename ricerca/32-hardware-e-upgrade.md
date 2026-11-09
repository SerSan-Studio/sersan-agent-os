# 32. Hardware reale del DL380 Gen10 e upgrade

- **Data di rilevazione**: 25 ottobre 2026. Prezzi e disponibilità valgono a questa data, salvo dove è scritta un'altra data.
- **Per chi**: Alberto e Michele. Serve come base per le domande di budget ai CEO.
- **Scopo**: rifare la parte hardware sulla configurazione reale di Michele. Memoria, seconda GPU, bilancio della RAM con i servizi del sistema di agenti, consumi e costo della corrente, UPS da rack, Proxmox Backup Server a casa.
- **Vincolo**: il board di Michele (`allegati/infra/`) è vincolante. Questo rapporto non lo cambia: dice cosa ci sta dentro, cosa manca e quanto costa.
- **Sostituisce** le parti hardware di `ricerca/15` (scritta per un server "presunto" da 160 GB) e aggiorna le voci hardware di `ricerca/25` e `ricerca/33`.
- **Legenda**: `[verificato: fonte]` = letto oggi sulla fonte indicata (pagina ufficiale, scheda tecnica, listino del venditore o file del progetto); `[non verificato]` = stima, calcolo o dato che la fonte primaria non conferma.
- **Cambio**: 1 € = 0,83728 £ e 1 € = 1,1193 $ (BCE, 23/10/2026), quindi 1 £ ≈ 1,194 € [verificato: ecb.europa.eu, tabella del 23/10/2026].
- **IVA**: per ogni prezzo è scritto se è inclusa o esclusa. I prezzi al dettaglio in Italia, Germania e Regno Unito di solito la includono (22 %, 19 %, 20 %).

---

## In breve

Il server di Michele è adatto al sistema di agenti e va bene subito, così com'è [non verificato: giudizio basato sul §3]. Le due CPU Xeon Gold 5218 hanno 6 canali di memoria ciascuna e leggono la RAM al massimo a 2666 MT/s [verificato: intel.com; HPE QuickSpecs]. I 192 GB sono con ogni probabilità 12 moduli da 16 GB, uno per canale: è la configurazione bilanciata migliore dopo quella piena [non verificato: da leggere nell'iLO; banda verificata su Lenovo LP1089]. La velocità reale dipende dai moduli: 2133 MT/s se sono i 10 moduli PC4-2133 già comprati più 2, 2666 MT/s se sono moduli da 2666 o più veloci [non verificato]. Il bilancio della RAM regge l'avvio della fase F4 con circa 35 GB liberi. Con tutte le funzioni accese (bot nelle call, "Andrea" al telefono, 12-16 sessioni di agenti insieme) il margine va da +7 a −11 GB, cioè finisce [non verificato: stima del §3]. L'unico passo che resta bilanciato e alla banda piena è passare a 24 moduli, cioè 384 GB: costano £1.020 IVA esclusa da Bargain Hardware (circa 1.218 €) in moduli da 2666, oppure 816 € IVA esclusa in moduli da 2133 su un rivenditore UE [verificato: configuratori del 25/10/2026]. Il passo da 4 moduli (256 GB) costa un terzo, ma la banda scende al 69 % [verificato: Lenovo LP1089]. La seconda GPU "RTX A2000 con chip Ada da 6 GB GDDR7" non esiste: le schede reali da 70 W senza cavo sono la RTX A2000 12 GB (Ampere), la RTX 2000 Ada 16 GB e la RTX PRO 2000 Blackwell 16 GB GDDR7 [verificato: datasheet NVIDIA e PNY]. Consiglio la **RTX 2000 Ada da 16 GB**, oggi a 837-946 € IVA inclusa [verificato: gpuprix e hardwaredealz]: ci stanno insieme Andrea, la trascrizione dal vivo, embedding, reranker e il modello da 4B, 24 ore su 24, mentre la RTX 4000 resta libera per Experimental-1 la sera [non verificato: stima di VRAM del §4.6]. Va nel riser secondario, con una staffa ad altezza piena. Consumo realistico: circa 300 W medi e 730-790 W di picco; a 0,35 €/kWh sono circa 77 € al mese [non verificato: stima del §5]. L'UPS rack consigliato è l'Eaton 5PX 1500 G2 da 1500 W. Il PBS a casa su Lenovo M920t con due dischi costa oggi 640-1.180 € IVA inclusa, perché i dischi sono raddoppiati di prezzo in un anno [verificato per i prezzi dei dischi: DriveVault su dati ComputerBase; somma non verificata].

**I punti per decidere**

1. **Memoria**: 6 canali per CPU, 2 moduli per canale, 24 slot; con la Gold 5218 HPE dà 2666 MT/s sia con 1 sia con 2 moduli per canale [verificato: HPE QuickSpecs DL380 Gen10 v58, tabella "Intel Xeon Gold 52xx"]. Le configurazioni a piena banda sono 6 o 12 moduli per CPU; 8 per CPU funzionano ma danno il 69 % della banda [verificato: Lenovo Press LP1089].
2. **Bilancio della RAM**: 192 GB bastano per F1-F4. Per lo scenario completo servono altri 192 GB (384 GB in tutto) oppure, come minimo, altri 64 GB a banda ridotta [non verificato: stima del §3].
3. **Seconda GPU**: RTX 2000 Ada 16 GB, 70 W, nel riser secondario. Alternativa più veloce ma oggi cara: RTX PRO 2000 Blackwell (1.090-1.425 € IVA inclusa). La L4 da 24 GB costa da 3.589 € ed esce dal budget [verificato: prezzi del §4.3].
4. **Correzione al rapporto 15**: la QuickSpecs HPE v58 **elenca** la Quadro RTX 4000 come modulo HPE R1F95C per il DL380 Gen10, con aria in ingresso fino a 35 °C sul telaio 8 SFF. Però HPE scrive anche "Mixing of GPUs is not supported": due GPU di modelli diversi escono comunque dalla configurazione supportata [verificato: QuickSpecs v58, tabella Accelerators e note].
5. **Corrente**: 250-350 W medi alla presa, 730-790 W di picco. A 0,30-0,40 €/kWh sono 55-102 € al mese; il valore centrale è circa 77 € [non verificato: stima del §5]. La seconda GPU aggiunge 2-10 € al mese, 12 moduli di RAM in più circa 6-10 €.
6. **UPS rack 2U**: Eaton 5PX 1500 G2 (1500 VA, 1500 W) o APC SMT1500RMI2UC (1500 VA, 1000 W). Con due GPU il picco del server arriva vicino ai 1000 W dell'APC: meglio l'Eaton, oppure l'APC con un tetto di potenza sulle GPU. Prezzi: 937-1.144 € IVA esclusa l'Eaton, 1.011 € IVA esclusa l'APC [verificato: listini del §6].
7. **PBS a casa**: M920t ricondizionato 186-360 € IVA inclusa, più 2 dischi da 4 TB (circa 390 €) o da 8 TB (circa 700 €), più due SSD piccoli per i metadati, che Proxmox raccomanda con i dischi meccanici [verificato: pbs.proxmox.com; prezzi del §7].
8. **Acquisti dal Regno Unito**: Bargain Hardware esclude la Sardegna dalla spedizione con dazi e IVA già pagati; per la Sardegna chiede di contattarli per un preventivo [verificato: Termini e condizioni di Bargain Hardware]. Se l'ordine del server ("Pagare Bargain", fase F0) è ancora aperto, conviene aggiungere lì la RAM.

---

## 1. La macchina reale

| Componente | Dato | Etichetta |
|---|---|---|
| Server | HPE ProLiant DL380 Gen10, 2U, Proxmox VE | [verificato: board di Michele] |
| CPU | 2 × Intel Xeon Gold 5218: 16 core e 32 thread ciascuna, 2,3 GHz (turbo 3,9 GHz), 22 MB di cache, 125 W, 2 UPI, 48 linee PCIe 3.0, memoria massima 1 TB per CPU | [verificato: intel.com, scheda Gold 5218; HPE QuickSpecs US v24] |
| Stato della CPU per Intel | "Discontinued", fine degli aggiornamenti di servizio il 30/06/2025 | [verificato: intel.com] |
| RAM | 192 GB DDR4 RDIMM ECC | [verificato: messaggio di Michele, board] |
| Dischi | rpool 2 × SSD SAS 800 GB in mirror; tank 3 mirror di HDD SAS 1,8 TB (6 dischi, circa 5,4 TB utili) | [verificato: board e messaggio di Michele] |
| Telaio | 8 dischi da 2,5" fanno pensare al telaio 8 SFF | [non verificato: da leggere sull'etichetta o nell'iLO] |
| Alimentatori | 2 × HPE 800 W Flex Slot Titanium (865438-B21): solo 200-240 V AC, efficienza fino al 96 % | [verificato: messaggio di Michele; HPE QuickSpecs v58] |
| Ventole e dissipatori | kit ad alte prestazioni già montati | [verificato: messaggio di Michele] |
| GPU | Quadro RTX 4000 8 GB: di giorno all'LXC AI, la sera alla VM Experimental-1 | [verificato: board] |
| Rete | 561FLR-T, porta 1 in trunk verso OPNsense; iLO sulla porta dedicata | [verificato: board] |
| Altro | TPM 2.0 | [verificato: board] |
| Garanzia | i server costruiti su ordine da Bargain Hardware hanno 3 anni di garanzia "return to base" del venditore | [verificato: bargainhardware.co.uk, pagina DL380 Gen10] |

Le linee PCIe sono 3.0. Una scheda PCIe 4.0 o 5.0 funziona, ma a velocità PCIe 3.0: con un collegamento x8 sono circa 7,9 GB/s. Conta quando si carica un modello nella memoria della GPU, non durante l'uso [non verificato: dato dello standard PCIe].

---

## 2. Memoria

### 2.1 Canali e velocità

| Fatto | Etichetta |
|---|---|
| 12 slot per CPU, 6 canali per CPU, 2 moduli per canale: 24 slot in tutto | [verificato: HPE QuickSpecs v58, §Memory] |
| Gold 5218: 6 canali, "DDR4-2667", 1 TB per CPU | [verificato: intel.com] |
| HPE, CPU Gold 52xx con moduli HPE SmartMemory: 2666 MT/s con 1 modulo per canale e anche con 2 | [verificato: QuickSpecs v58, tabella "HPE Server Memory speed: Intel Xeon Gold 52xx processors"] |
| "To realize the performance memory capabilities listed in this document, HPE DDR4 SmartMemory is required" | [verificato: QuickSpecs v58] |
| Con 2 CPU: quantità pari, stessa capacità sulle due CPU; non si mescolano RDIMM, LRDIMM e UDIMM | [verificato: QuickSpecs v58, "General Memory Population Rules"] |
| Moduli più veloci della CPU (2933, 3200) girano a 2666; moduli più lenti (2133) portano tutto a 2133 | [non verificato: comportamento standard DDR4, non scritto da HPE] |
| "System memory should be 2x GPU memory": con 8 + 16 GB di VRAM servono almeno 48 GB | [verificato: QuickSpecs v58, note sugli acceleratori] |

**Banda teorica per CPU**: 6 canali × 2666 MT/s × 8 byte = circa 128 GB/s; a 2133 MT/s circa 102 GB/s (−20 %). Con due CPU: circa 256 o 205 GB/s [non verificato: calcolo]. La banda pesa solo sui modelli linguistici fatti girare in CPU. Gli agenti che chiamano Claude via API non se ne accorgono [non verificato].

### 2.2 Come sono fatti, con ogni probabilità, i 192 GB

| Ipotesi | Composizione | Per CPU | Velocità | Probabilità | Come si riconosce |
|---|---|---|---|---|---|
| A | i 10 moduli Samsung 16 GB 2Rx4 PC4-2133P già comprati più 2 uguali | 6 moduli, 1 per canale | 2133 MT/s | alta | `ricerca/15` §1 elenca l'acquisto dei 10 moduli [verificato: 15 §1]; `ricerca/25` H01 fa la stessa ipotesi [verificato: 25] |
| B | 12 moduli da 16 GB 2666 o più veloci, presi nell'ordine Bargain | 6, 1 per canale | 2666 MT/s | media | la fase F0 del board dice "Pagare Bargain" e "Montaggio, test RAM" [verificato: board] |
| C | 24 moduli da 8 GB | 12, tutti gli slot | 2666 o 2133 | bassa | nessuno slot libero: per crescere si cambiano i moduli |
| D | 6 moduli da 32 GB | 3, metà canali vuoti | | bassa | banda al 51 % [verificato: Lenovo LP1089] |

`[non verificato: le probabilità sono una stima]`. Si verifica in un minuto: iLO → Memory Information, oppure `dmidecode -t memory` sull'host Proxmox (capacità, velocità configurata, rank e organizzazione x4 o x8 di ogni slot).

**Perché 6 moduli per CPU vanno bene.** Lenovo ha misurato con STREAM Triad la banda delle configurazioni da 1 a 12 moduli su Xeon Scalable di seconda generazione (la stessa famiglia della 5218). Le tre regole: tutti i canali usati con la stessa capacità e lo stesso numero di rank; i due controller di memoria di ogni CPU configurati allo stesso modo; le due CPU uguali [verificato: Lenovo Press LP1089].

| Moduli per CPU | Banda relativa misurata | HPE |
|---|---|---|
| 4 | 66 % | bilanciata |
| 6 | **95 %** | bilanciata |
| 8 | 69 % | bilanciata (nessun asterisco) |
| 9, 10, 11 | 18-69 % secondo la disposizione | "Unbalanced, not recommended" |
| 12 | **100 %** | bilanciata |

[verificato: Lenovo LP1089 per le percentuali; QuickSpecs v58 "Memory Population guidelines" per la colonna HPE]. Nota: HPE considera bilanciati anche 4 e 8 moduli per CPU, ma la misura Lenovo mostra che 8 moduli lasciano due canali vuoti e perdono un terzo della banda.

### 2.3 Espansioni che restano bilanciate (partendo da 12 moduli da 16 GB)

| Passo | RAM totale | Moduli per CPU | Banda relativa | Moduli da comprare | Bargain, 2666, IVA esclusa | Servermall, IVA esclusa |
|---|---|---|---|---|---|---|
| Oggi | 192 GB | 6 + 6 | 95 % | 0 | 0 | 0 |
| +64 GB | 256 GB | 8 + 8 | 69 % | 4 × 16 GB | £340 (≈ 406 €) | 272 € (2133) o 512 € (2666) |
| +96/160 GB | 288-352 GB | 9-11 per CPU | 18-69 % | 6-10 | sconsigliato | sconsigliato |
| **+192 GB** | **384 GB** | **12 + 12** | **100 %** | **12 × 16 GB** | **£1.020 (≈ 1.218 €)** | **816 € (2133) o 1.536 € (2666)** |
| +384 GB | 576 GB | 12 + 12 (un 16 e un 32 GB per canale) | 100 % se ogni canale è uguale | 12 × 32 GB | £2.760 (≈ 3.296 €) | 2.832 € (2666) |

[verificato: prezzi del §2.4; percentuali Lenovo LP1089; calcoli in euro non verificati]. Sull'ultima riga: HPE non scrive nella QuickSpecs se si possono mescolare capacità diverse nello stesso canale; un utente del forum HPE ha avuto un avviso di configurazione con 16 e 32 GB mescolati [verificato: community.hpe.com, citato nei risultati di ricerca]. Va evitata finché HPE non lo conferma.

**Regole pratiche per comprare** [non verificato: prassi]:
- comprare moduli uguali a quelli montati (stessa capacità, stessi rank, stessa organizzazione x4 o x8). Se i moduli attuali sono 2Rx4 PC4-2133, i nuovi da 2133 costano meno e non cambiano nulla; quelli da 2666 girerebbero comunque a 2133;
- l'organizzazione x4 serve anche per le correzioni di errore avanzate della piattaforma; con moduli x8 mescolati quella funzione può spegnersi;
- con 2 moduli per canale HPE dà ancora 2666 MT/s sulla Gold 52xx con moduli HPE; con moduli non HPE va verificato nell'IML dell'iLO dopo il montaggio;
- dopo il montaggio: 24 ore di memtest86+ e controllo dell'IML per errori corretti, come già previsto nella fase F0 del board.

### 2.4 Prezzi della RAM oggi, Regno Unito ed Europa

| Fonte e condizione | Modulo | Prezzo | Data | Etichetta |
|---|---|---|---|---|
| Bargain Hardware (UK), configuratore DL380 Gen10, rigenerato, garanzia 3 anni | 16 GB 2666 2Rx8 | £85 IVA esclusa (£102 inclusa) | 25/10/2026 | [verificato: bargainhardware.co.uk] |
| idem | 16 GB 2933 2Rx8 | £95 (£114) | 25/10/2026 | [verificato] |
| idem | 16 GB 3200 2Rx8 | £100 (£120) | 25/10/2026 | [verificato] |
| idem | 32 GB 2933 2Rx4 | £230 (£276) | 25/10/2026 | [verificato] |
| idem | 32 GB 3200 | £275 (£330) | 25/10/2026 | [verificato] |
| idem | 64 GB 2933 | £390 (£468) | 25/10/2026 | [verificato] |
| Servermall (UE, partita IVA lituana), configuratore in italiano, rigenerato, "non è un preventivo vincolante" | 16 GB 2133 | 68 € IVA esclusa | 25/10/2026 | [verificato: servermall.com/it] |
| idem | 16 GB 2400 / 2666 / 2933 | 81 / 128 / 135 € IVA esclusa | 25/10/2026 | [verificato] |
| idem | 32 GB 2133 / 2666 / 2933 | 162 / 236 / 283 € IVA esclusa | 25/10/2026 | [verificato] |
| datacenterdisk (USA), nuovo | Samsung 16 GB 2133 | 92,18 $ | aggiornato al 22/07/2026 | [verificato: datacenterdisk.com, via ricerca] |
| idem | Samsung 16 GB 2666 | 133,99-194,99 $ | 22/07/2026 | [verificato: idem] |
| Prezzo pagato per i 10 moduli 2133 (riferimento) | 16 GB 2133 | 69 € a modulo | prima del 24/10/2026 | [verificato: ricerca/15 §1] |

**Il mercato.** Bargain Hardware scrive che, secondo TrendForce, i prezzi a contratto della DRAM per server dovevano salire di circa il 90 % in un trimestre nel primo trimestre 2026, e che sul mercato spot la DDR4 ha avuto rincari oltre il 170 % [verificato: blog Bargain Hardware del 01/04/2026, che cita TrendForce e altre fonti]. Un tracker americano stima +60-80 % per la DDR4 ECC RDIMM tra inizio 2025 e il primo trimestre 2026 [verificato: datacenterdisk.com, via ricerca]. Aspettare non promette prezzi più bassi [non verificato].

**Spedizione in Sardegna.** Bargain Hardware ha un servizio con dazi e IVA d'importazione già pagati per l'Italia, ma "Italy (mainland only)": Sardegna e Sicilia sono escluse e vanno quotate a parte, con possibili spese doganali all'arrivo. Le aziende con partita IVA UE, scrive Bargain, devono usare la spedizione normale [verificato: Termini e condizioni di Bargain Hardware, sezione "EU Delivery with Duties & Taxes Included"]. Chi compra (Sersan Limited dal Regno Unito o un soggetto con partita IVA italiana) cambia il trattamento dell'IVA: da chiarire con il commercialista [non verificato].

**Ordine di grandezza dell'ordine Bargain.** Rifacendo la configurazione di Michele sul configuratore di oggi (telaio 8 SFF £180, 2 × Gold 5218 £40, 12 × 16 GB 2666 £1.020, 2 × SSD SAS 800 GB £160, 6 × HDD 1,8 TB £210, 8 carrier £56, 2 alimentatori Titanium £40, 561FLR-T £12, TPM £70, guide £40, controller E208i-a £43) si arriva a circa £1.870 IVA esclusa, circa 2.230 € [non verificato: ricostruzione dal configuratore del 25/10/2026; non è il preventivo di Michele; ventole e dissipatori non quotati].

### 2.5 Scelta consigliata sulla memoria

- **Subito**: nessun acquisto. Leggere nell'iLO la composizione reale dei 192 GB.
- **Se l'ordine Bargain non è ancora pagato** e i moduli sono da 2666: valutare di aggiungere 12 moduli nello stesso ordine (£1.020 IVA esclusa), perché Bargain applica prezzi di sistema e la spedizione è una sola [non verificato: convenienza da confermare con il preventivo].
- **Più avanti (prima di accendere bot delle call, Andrea e più sessioni di agenti)**: passare a 384 GB con 12 moduli uguali a quelli montati. Se i moduli sono 2133, la strada più economica è Servermall a 68 € l'uno (816 € IVA esclusa) [non verificato: prezzo non vincolante].
- **Da evitare**: 6, 8 o 10 moduli in più senza motivo. 4 moduli (256 GB) sono un ripiego accettabile per i servizi, non per i modelli in CPU [non verificato].

---

## 3. Bilancio della RAM con il sistema di agenti

### 3.1 Il bilancio del board

| Voce del board | GB | Etichetta |
|---|---|---|
| Host Proxmox e cache ZFS (ARC) | 16 | [verificato: board, tabella "Capacità"] |
| Servizi core (edge, apps, data, ci, vault, obsrv), compreso SersanOutreach (openoutreach in VLAN 30) | circa 69 | [verificato: board; board-vlan.txt, riga APPS] |
| AI, Firecrawl, Qdrant, LiteLLM | circa 24 | [verificato: board] |
| Experimental 1 e 2 | 24 | [verificato: board] |
| Minecraft | 6 | [verificato: board] |
| **Libera per crescere** | **circa 53** | [verificato: board] |

### 3.2 Una correzione sulla cache ZFS

Proxmox, per le installazioni nuove, limita l'ARC al 10 % della RAM con un tetto di 16 GiB, e indica come regola "2 GiB Base + 1 GiB/TiB-Storage" [verificato: pve.proxmox.com, wiki ZFS on Linux]. Con 192 GB l'ARC arriva quindi a 16 GiB da sola, più 2-4 GB dell'host: 18-20 GB, non 16. La regola chiede invece circa 8 GiB (2 + circa 0,7 TiB di rpool + circa 4,9 TiB di tank) [non verificato: calcolo]. **Proposta**: fissare `zfs_arc_max` a 12 GiB. Così host e ARC restano nei 16 GB del board.

### 3.3 I servizi del sistema di agenti che il board non conta

| Servizio | Avvio della fase F4 (GB) | Scenario completo (GB) | Etichetta |
|---|---|---|---|
| Correzione ARC, se non si fissa il tetto | 0 | 0-4 | [non verificato: §3.2] |
| Motore degli agenti (Agent SDK di Claude o Hermes): circa 1 GiB per sessione attiva, più coda e orchestrazione | 8-10 (8 sessioni) | 14-18 (12-16 sessioni) | 1 GiB per sessione come punto di partenza ufficiale [verificato: ricerca/26 §3.3, fonte D2]; numero di sessioni [non verificato] |
| Cancello: servizio delle approvazioni, worker e interfaccia (il database sta nel PostgreSQL del board) | 1 | 2 | [non verificato: stima] |
| Chat: Teams più il ponte "Porta" (Chat SDK) | 0,5-1 | 1; 2-4 se un giorno si passa a Mattermost | [non verificato: stima di ricerca/28] |
| Bot nelle call: VM meet-01 con Vexa, 3 bot | 0 | 12 | 2 GB per bot [verificato: values.yaml, citato in ricerca/30 §10.2]; totale [non verificato] |
| Trascrizione e lavori a lotti nell'LXC GPU | 4 | 8 | [non verificato: ricerca/30 §10.2] |
| Voce "Andrea" (Asterisk, Pipecat, STT, TTS) | 0 | 4-8 (8 se tutto su CPU, 4 con la seconda GPU) | [non verificato: ricerca/31] |
| SersanOutreach: worker in più con browser | 0 | 1-2 | 7,4 GiB di tetti già misurati e già nel board [verificato: ricerca/01 riga 20]; crescita [non verificato] |
| Crescita della memoria aziendale (Qdrant con trascrizioni e mail, PostgreSQL, Loki) | 2 | 4-6 | [non verificato] |
| **Totale nuovo** | **circa 16-18** | **circa 46-64** | [non verificato] |
| **RAM libera dopo** | **circa 35-37** | **da +7 a −11** | [non verificato] |
| Facoltativo: un modello MoE in RAM per lavori notturni su dati sensibili (Qwen3.6-35B-A3B o gpt-oss-120b) | | +20 / +65 | [non verificato: ricerca/13 §0] |

Nota su G9 ("agenti in organigramma, fino a cento"): la RAM cresce con le **sessioni attive insieme**, non con gli agenti definiti. Cento agenti con un tetto di 16 sessioni in parallelo stanno nei 14-18 GB della tabella. Senza tetto, ogni sessione in più costa circa 1 GiB [non verificato: deduzione dalla regola di ricerca/26].

### 3.4 Basta o no

- **Fasi F1-F4 (avvio)**: **basta**. Restano circa 35 GB liberi [non verificato].
- **Scenario completo** (bot nelle call, Andrea 24/7, 12-16 sessioni di agenti, crescita della memoria): **non basta** con margine. Proxmox può comprimere un po' la RAM con KSM e ballooning, ma con ZFS e VM Windows non conviene contarci [non verificato].
- **Quanta aggiungerne**: **+192 GB (12 × 16 GB, totale 384 GB)**. È l'unico passo bilanciato a piena banda, lascia circa 180-200 GB liberi (115-135 GB anche con il modello MoE più grande in RAM di notte) [non verificato: calcolo]. Il minimo che funziona è **+64 GB (4 × 16 GB, totale 256 GB)**, con la banda al 69 % [verificato: LP1089 per la banda].
- **Leve per rimandare l'acquisto** [non verificato: proposte]: tetto ARC a 12 GiB; Experimental 1 e 2 accese solo quando servono (24 GB); Andrea sulla seconda GPU invece che su CPU (−4 GB); tetto di 12 sessioni di agenti in parallelo.

---

## 4. Seconda GPU

### 4.1 Il modello giusto

Il messaggio di Michele parla di "una seconda GPU tipo una RTX A2000 con chip Ada da 6GB GDDR7". Una scheda così non esiste. Mescola tre prodotti:

| Pezzo del nome | Scheda reale | Etichetta |
|---|---|---|
| "RTX A2000", "6 GB" | RTX A2000 (Ampere), 6 GB o 12 GB GDDR6, 70 W | [verificato: datasheet NVIDIA RTX A2000; gpuprix.com, versione 6 GB in Germania] |
| "chip Ada" | RTX 2000 Ada Generation, 16 GB GDDR6, 70 W | [verificato: datasheet NVIDIA RTX 2000 Ada, copia HP] |
| "GDDR7" | RTX PRO 2000 Blackwell, 16 GB GDDR7, 70 W | [verificato: datasheet PNY RTX PRO 2000 Blackwell, maggio 2026] |
| "6 GB GDDR7" | esiste solo come GPU per portatili: RTX PRO 500 Blackwell, 6 GB GDDR7; non è una scheda PCIe | [verificato: notebookcheck.net, via ricerca] |

Con ogni probabilità Michele intende "una scheda della classe 2000 da 70 W, senza cavo di alimentazione". Le candidate vere sono la A2000 12 GB, la RTX 2000 Ada e la RTX PRO 2000 Blackwell [non verificato: interpretazione]. Le confronto qui sotto con la L4 e con le altre schede da 70-75 W senza alimentazione aggiuntiva.

### 4.2 Confronto tecnico

| Scheda | Architettura | Memoria | Banda | Bus | Consumo | Formato | Raffreddamento | Nella QuickSpecs HPE del DL380 Gen10 |
|---|---|---|---|---|---|---|---|---|
| Quadro RTX 4000 (già nel server) | Turing | 8 GB GDDR6 | 416 GB/s | PCIe 3.0 x16 | 160 W (125 W senza VirtualLink), cavo 8 pin | 1 slot, altezza piena | attivo | **sì**, modulo HPE R1F95C, 35 °C su 8 SFF |
| RTX A2000 12 GB | Ampere | 12 GB GDDR6 ECC, 192 bit | 288 GB/s | PCIe 4.0 x16 | 70 W | 2 slot, profilo basso, 2,7" × 6,6" | attivo | no |
| **RTX 2000 Ada** | Ada | **16 GB GDDR6 ECC**, 128 bit | 224 GB/s | PCIe 4.0 x8 | 70 W | 2 slot, profilo basso, 2,7" × 6,6" | attivo | no |
| RTX 2000E Ada | Ada | 16 GB GDDR6 ECC, 128 bit | 224 GB/s | PCIe 4.0 x8 | 50 W [non verificato] | **1 slot**, profilo basso | attivo, a turbina | no |
| RTX PRO 2000 Blackwell | Blackwell | 16 GB GDDR7 ECC, 128 bit | 288 GB/s | PCIe 5.0 x8 | 70 W | 2 slot, 2,7" × 6,6" | attivo | no |
| RTX 4000 SFF Ada | Ada | 20 GB GDDR6 ECC, 160 bit | 280 GB/s | PCIe 4.0 x16 | 70 W | 2 slot, 2,7" × 6,6" | attivo | no |
| RTX PRO 4000 Blackwell SFF | Blackwell | 24 GB GDDR7 ECC, 192 bit | 432 GB/s | PCIe 5.0 x8 | 70 W | 2 slot, mezza altezza | attivo | no |
| NVIDIA L4 | Ada | 24 GB GDDR6 ECC | 300 GB/s | PCIe 4.0 x16 | 72 W | 1 slot, profilo basso | **passivo** | no |
| NVIDIA T4 | Turing | 16 GB GDDR6 | 300-320 GB/s | PCIe 3.0 x16 | 70 W | 1 slot, profilo basso | **passivo** | **sì**, 35 °C su 8 SFF |
| NVIDIA A2 | Ampere | 16 GB GDDR6 | 200 GB/s | PCIe 4.0 x8 | 40-60 W | 1 slot, profilo basso | **passivo** | **sì**, solo con CPU di 2ª generazione, 30 °C su 8 SFF |

Fonti: datasheet NVIDIA RTX A2000, RTX 2000 Ada, RTX 4000 SFF Ada; datasheet PNY RTX PRO 2000 Blackwell e RTX PRO 4000 Blackwell SFF; pagina HPE e rivenditori per la L4; pagine NVIDIA di T4 e A2; SHI per la RTX 2000E Ada; HPE QuickSpecs v58 per l'ultima colonna [verificato, salvo dove indicato]. La banda della T4 è 300 GB/s nel vecchio datasheet e 320 GB/s nelle pagine nuove di NVIDIA [verificato: nvidia.com, via ricerca].

**Cosa cambia tra le architetture** [non verificato: sintesi]:
- **Turing** (RTX 4000, T4): niente BF16 e niente FlashAttention 2; lo stack giusto è llama.cpp [verificato: ricerca/13 §0 punto 4].
- **Ampere e Ada** (A2000, A2, 2000 Ada, L4): BF16 e FlashAttention 2; CTranslate2, PyTorch e NeMo le supportano da anni. Ada aggiunge FP8.
- **Blackwell** (PRO 2000, PRO 4000 SFF): FP4 e GDDR7. Servono CUDA 12.8 o successivo (che ha introdotto l'architettura SM 120) e librerie compilate per quella architettura [verificato: note di rilascio CUDA 12.8 via ricerca]. Per CTranslate2, il motore di faster-whisper, il supporto non l'ho trovato: va provato prima di comprare [non verificato].

### 4.3 Prezzi a oggi

| Scheda | Italia | Germania | Regno Unito | Usato | Etichetta |
|---|---|---|---|---|---|
| RTX A2000 12 GB | 383 € su Amazon.it, ma l'annuncio dice "8GB": non affidabile | 12 GB nuova non trovata; 6 GB nuova 587 € | **£455** nuova su Amazon UK (≈ 543 €); mediana 3 mesi £546 | eBay: 499-569 € (DE), £450 (UK), date non chiare | [verificato: gpuprix.com del 24/10/2026; eBay via ricerca, date non verificate] |
| **RTX 2000 Ada** | **837 €** su Amazon.it; mediana 12 mesi 738 € | **da 945,99 €** (10 negozi fino a 1.130,50 €) | £987 su Amazon UK (≈ 1.179 €); mediana 12 mesi £739 | non cercato | [verificato: gpuprix.com del 24/10/2026; hardwaredealz.com del 25/10/2026 ore 15:20] |
| RTX PRO 2000 Blackwell | 1.090 € su Amazon.it (versione Lenovo); mediana 12 mesi 971 € | da 1.425 € (NVIDIA), da 1.630,40 € (PNY) | £1.134 su Amazon UK (versione HP); Scan £1.658,48 (PNY OEM) | minimo degli ultimi 12 mesi 712-756 € | [verificato: gpuprix.com del 24/10/2026; hardwaredealz.com del 25/10/2026; scan.co.uk del 25/10/2026] |
| RTX 4000 SFF Ada | non cercato | 2.457 €, esaurita; mediana 12 mesi 1.489 € | non cercato | | [verificato: gpuprix.com del 23/10/2026] |
| RTX PRO 4000 Blackwell SFF | | listino SHI UE 3.032,85 € | listino SHI UK £3.692,34 | | [verificato: shi.com via ricerca; data non indicata] |
| NVIDIA L4 | | nuova da 3.589 € | | Dell usata 2.432,05 € (eBay.de) | [verificato: geizhals.de, dato del 07/10/2026; eBay via ricerca] |
| NVIDIA T4 | Servermall da 1.020 € IVA esclusa | | | eBay.de 564-590 €, date non chiare | [verificato: servermall.com del 25/10/2026; eBay via ricerca] |
| NVIDIA A2 | Servermall da 576 € IVA esclusa | listino SHI 1.783,52 € | | nuova sigillata 529 $ da venditore USA su eBay.de | [verificato: servermall.com del 25/10/2026; shi.com ed eBay via ricerca] |
| RTX 2000E Ada | | | | listino SHI 849-1.399 $ (due pagine in contrasto) | [verificato: shi.com via ricerca] |

I prezzi al dettaglio includono l'IVA del paese. La RTX PRO 2000 è salita molto nelle ultime settimane: oggi in Germania costa circa il 40 % più della sua mediana a 12 mesi [non verificato: calcolo su hardwaredealz e gpuprix].

### 4.4 Entra nel DL380 Gen10?

**Gli slot** [verificato: QuickSpecs v58, "Expansion Slots" e "Riser Information"]:
- riser primario standard (CPU 1): slot 1 PCIe 3.0 x8 altezza e lunghezza piena, slot 2 x16 altezza e lunghezza piena, slot 3 x8 altezza piena e mezza lunghezza;
- riser secondario (richiede la CPU 2, che c'è): il kit 870548-B21 ha la stessa disposizione, slot 4-6; esistono anche kit x16/x16 per una GPU a doppio slot (826694-B21, 826704-B21);
- riser terziario (CPU 2): due slot x8;
- "With the Standard Primary Riser the top x8 PCIe Slot connector will not be accessible with the installation of a doublewide GPU": una scheda a doppio slot copre lo slot accanto.

**Dove metterla** [non verificato: proposta da confermare con l'ispezione]:
- la RTX 4000 (1 slot) sta nello slot 2 del riser primario;
- **una scheda a 2 slot** (A2000, 2000 Ada, PRO 2000, 4000 SFF) va nello **slot 5 del riser secondario** (connettore x16, collegamento x8 o x16) e copre lo slot 4;
- **una scheda a 1 slot** (RTX 2000E Ada, T4, A2, L4) può andare anche nello slot libero del riser primario (x8), se il controller dei dischi non lo occupa.
- Se il riser secondario manca: il kit 870548-B21 usato costa 62-96 € IVA inclusa [verificato: Serverschmiede 96 € e annunci eBay.de, via ricerca]. Bargain vende il DL380 Gen10 8 SFF anche nella versione "6 PCIe Slots", cioè con due riser [verificato: configuratore Bargain del 25/10/2026].

**La staffa.** Gli slot del DL380 sono ad altezza piena. Le schede da 70 W della classe 2000 sono a profilo basso: la PNY RTX 2000 Ada -PB risulta venduta con la sola staffa a profilo basso [verificato: scheda di un rivenditore ungherese, via ricerca]. Serve una staffa ad altezza piena per 4 mini DisplayPort, da comprare a parte [non verificato: prezzo e disponibilità].

**Alimentazione.** A 70 W la scheda si alimenta dallo slot: niente cavo [verificato: datasheet "Total board power: 70 W"]. Gli alimentatori 2 × 800 W reggono il picco (§5.3).

**Raffreddamento** [verificato: QuickSpecs v58, note sugli acceleratori]:
- "Performance fans (867810-B21) are required for all GPU installations": ci sono già;
- "Performance Heatsinks (826706-B21) are required for Double Wide GPU installations": ci sono già;
- per le schede qualificate HPE fissa la temperatura massima dell'aria in ingresso: sul telaio 8 SFF 35 °C per RTX 4000 e T4, 30 °C per la A2.

Per le schede non qualificate l'iLO non legge la temperatura e regola le ventole senza quel dato [non verificato: comportamento riportato da utenti, ricerca/15 §2.3]. Per questo consiglio una scheda **con ventola propria** (A2000, 2000 Ada, PRO 2000) e non una passiva non qualificata come la L4: una passiva dipende tutta dal flusso d'aria del server, che l'iLO non sa di dover alzare [non verificato]. Il riser secondario sta dietro la CPU 2: l'aria arriva già scaldata. Nel salotto, d'estate, conviene tenere l'aria in ingresso sotto i 27 °C [non verificato: prudenza].

**Supporto HPE.** HPE scrive "Mixing of GPUs is not supported" [verificato: QuickSpecs v58]. Anche una T4 o una A2, che sono in elenco, accanto alla RTX 4000 escono dalla configurazione supportata. La garanzia del server però è quella di Bargain, non un contratto HPE [verificato: pagina Bargain]. In pratica la qualifica HPE conta come guida termica, non per l'assistenza [non verificato].

### 4.5 Driver e Proxmox

- Un solo driver NVIDIA sull'host serve entrambe le schede. I moduli del kernel open source di NVIDIA supportano solo Turing e successive; per Blackwell sono obbligatori [verificato: blog NVIDIA "NVIDIA Transitions Fully Towards Open-Source GPU Kernel Modules" e guida d'installazione dei driver]. La RTX 4000 è Turing: va bene con la stessa versione del driver.
- La seconda GPU resta sempre all'LXC `ai-gpu-01`. Lo script serale che passa la RTX 4000 a Experimental-1 deve staccare dal driver **solo** quella scheda (per indirizzo PCI) e non scaricare il modulo `nvidia`, che serve all'altra [non verificato: da provare con lo script di Michele].
- Ogni servizio va legato a una scheda con `CUDA_VISIBLE_DEVICES` o con l'assegnazione dei dispositivi nell'LXC [non verificato: prassi].

### 4.6 Cosa ci gira sopra

**Piano con una scheda da 16 GB fissa sull'AI, 24 ore su 24** [non verificato: stime da misurare con `nvidia-smi` nella fase F4]:

| Servizio | VRAM | Etichetta |
|---|---|---|
| "Andrea": STT in streaming e TTS Qwen3-TTS 0.6B, 1 chiamata | circa 5 GB | [non verificato: ricerca/31 §5] |
| Embedding e reranker Qwen3 0.6B FP16 (Infinity) | circa 3 GB | [non verificato: ricerca/31] |
| Trascrizione dal vivo: faster-whisper large-v3-turbo int8 | circa 2,1 GB | [verificato: Vexa `.env.example`, citato in ricerca/30 §6] |
| Qwen3-4B Q5_K_M con contesto (metadati della pipeline, bandi) | 3,5-4,2 GB | [non verificato: ricerca/31] |
| **Totale** | **circa 13,6-14,3 GB su 16** | [non verificato] |
| Lavori a lotti: Parakeet v3 e pyannote | 3-4,5 GB, in coda quando c'è spazio, o su CPU | [non verificato: ricerca/30 §6] |

Così la RTX 4000 non porta più servizi fissi. Di giorno resta per un modello da 8B (8 GB bastano per un 8B in Q4 con 8-16k token di contesto [non verificato: ricerca/13 §0]) o per i lotti; la sera va a Experimental-1 senza fermare nulla.

**Con le altre taglie** [non verificato]:
- **12 GB (A2000)**: ci stanno Andrea, embedding, reranker e Whisper (circa 10 GB), ma non il 4B, che resterebbe sulla RTX 4000 e la sera non ci sarebbe. È un compromesso.
- **20-24 GB (4000 SFF, PRO 4000 SFF, L4)**: tutto il piano sopra più un modello da 8B (5-7 GB) sempre acceso. Costano 2-4 volte una 16 GB.

**Modelli da 4 a 14 miliardi di parametri: velocità stimata per un utente** (token al secondo in scrittura con llama.cpp; stima = banda × 62 %, l'efficienza misurata sulla RTX 4000 nella classifica di llama.cpp, 67,6 token/s su 3,82 GB di pesi [verificato: github.com/ggml-org/llama.cpp/discussions/15013, via ricerca/13]; per la T4 uso la sua misura, 44 token/s sullo stesso test):

| Scheda | 4B Q5 (circa 3,3 GB) | 8B Q4_K_M (circa 5 GB) | 14B Q4_K_M (circa 9 GB) |
|---|---|---|---|
| Quadro RTX 4000 (8 GB) | 78 | 52 | non entra |
| RTX A2000 12 GB | 54 | 36 | 20, solo da sola |
| RTX 2000 Ada 16 GB | 42 | 28 | 15 |
| RTX PRO 2000 Blackwell 16 GB | 54 | 36 | 20 |
| RTX 4000 SFF Ada 20 GB | 53 | 35 | 19 |
| RTX PRO 4000 Blackwell SFF 24 GB | 81 | 54 | 30 |
| L4 24 GB | 56 | 37 | 21 |
| T4 16 GB | 51 | 34 | 19 |
| A2 16 GB | 38 | 25 | 14 |

[non verificato: stima; dimensioni dei pesi approssimate]. Due conclusioni. La RTX 4000 resta la scheda più veloce sui modelli piccoli: la seconda GPU porta **memoria e disponibilità 24/7**, non velocità. Un 14B gira su tutte le 16 GB, ma a 15-20 token/s e da solo; insieme al piano audio serve una 24 GB [non verificato].

### 4.7 Scelta consigliata sulla GPU

1. **RTX 2000 Ada 16 GB** (837-946 € IVA inclusa oggi): memoria giusta per il piano 24/7, architettura matura per l'audio, 70 W senza cavo, ventola propria. Nel riser secondario, slot 5, con staffa ad altezza piena [non verificato: scelta].
2. **RTX PRO 2000 Blackwell 16 GB**, se torna verso i 1.000 € e se faster-whisper e gli altri motori risultano compilati per Blackwell: +29 % di banda e FP4, stessi 70 W [non verificato].
3. **RTX 2000E Ada**, se lo spazio per una scheda a 2 slot non c'è: stessa memoria in un solo slot [non verificato: consumo e prezzo da confermare].
4. **Non consigliate**: A2000 12 GB (poca memoria per il piano completo, fuori produzione), L4 (oltre 3.500 € e passiva non qualificata), T4 e A2 (passive, lente o vecchie; la qualifica HPE non copre comunque due GPU diverse).

**Quando**: il board la mette nella fase F5. Se i bot delle call e Andrea devono funzionare anche la sera, quando la RTX 4000 è a Experimental-1, la seconda GPU serve già nella fase F4 [verificato: board per la fase F5 e per l'uso serale della RTX 4000; conseguenza non verificata]. È una decisione di budget.

---

## 5. Consumo elettrico e costo in Italia

### 5.1 I componenti

| Componente | Riposo (W) | Giorno tipico (W) | Picco (W) | Etichetta |
|---|---|---|---|---|
| 2 × Xeon Gold 5218 | 40-60 | 70-100 | 250 | TDP 125 W per CPU [verificato: intel.com]; resto [non verificato] |
| RAM 12 × 16 GB | 20-25 | 25-35 | 45-50 | [non verificato] |
| 6 HDD SAS 10k da 1,8 TB | 26-30 | 30-40 | 45 | per disco 4,4 W in attesa e 7,5 W tipici [verificato: scheda Seagate Exos 10E2400 di un rivenditore, via ricerca] |
| 2 SSD SAS 800 GB | 5-8 | 8-12 | 18 | [non verificato] |
| Quadro RTX 4000 | 9-12 | 15-40 | 125-160 | 9-12 W a riposo e 122 W misurati sotto carico [verificato: igorslab.de e servethehome.com, via ricerca]; 160 W [verificato: ricerca/15 §2.3] |
| Seconda GPU da 70 W | 6-10 | 15-35 | 70 | 70 W [verificato: datasheet]; riposo [non verificato] |
| 6 ventole ad alte prestazioni | 20-30 | 30-45 | 80-100 | [non verificato] |
| Scheda madre, iLO, 561FLR-T, controller, TPM | 35-45 | 40-50 | 55 | [non verificato] |
| **Somma** | **circa 160-220** | **circa 235-355** | **circa 690-750** | [non verificato] |
| **Alla presa** (perdite degli alimentatori Titanium) | **circa 170-240** | **circa 250-385** | **circa 730-790** | efficienza fino al 96 % [verificato: QuickSpecs v58]; il resto [non verificato] |

**Confronti pubblici.** SPECpower misura 49,3 W "active idle" su un DL380 Gen10 con 2 Xeon Platinum 8180, 96 GB e configurazione ridotta all'osso [verificato: spec.org, risultato del 28/08/2018]. Un fornitore di server dedicati dichiara per un DL380 Gen10 con 2 Gold 6144 e dischi LFF 96 W a riposo, 215 W medi e 487 W al massimo, senza GPU [verificato: voxility.com, via ricerca; dato del venditore]. I nostri 6 dischi a 10.000 giri, la rete a 10 Gbit e le due GPU spiegano la differenza [non verificato].

**Media sulle 24 ore** [non verificato]: notte circa 200 W, giorno circa 300 W, sera con Experimental-1 sotto carico circa 350-450 W. Media realistica **250-350 W, valore centrale 300 W**. La lettura vera arriva dal contatore dell'iLO dopo una settimana di lavoro.

### 5.2 Costo al mese e all'anno

| Media 24/7 | kWh al mese | 0,30 €/kWh | **0,35 €/kWh** | 0,40 €/kWh | 0,45 €/kWh |
|---|---|---|---|---|---|
| 250 W | 182,5 | 54,75 € | **63,87 €** | 73,00 € | 82,12 € |
| **300 W** | **219,0** | 65,70 € | **76,65 €** | 87,60 € | 98,55 € |
| 350 W | 255,5 | 76,65 € | **89,42 €** | 102,20 € | 114,98 € |
| All'anno, 300 W | 2.628 | 788 € | **920 €** | 1.051 € | 1.183 € |

[non verificato: calcolo con 730 ore al mese]. **Quanto pesano gli upgrade**: la seconda GPU aggiunge 10-30 W medi, cioè 2,55-7,66 € al mese a 0,35 €/kWh; 12 moduli di RAM in più 25-40 W, cioè 6,39-10,22 € al mese [non verificato]. D'estate, se il salotto è climatizzato, il condizionatore spende circa un terzo del calore del server in più [non verificato: stima con un rendimento del condizionatore di 3].

### 5.3 Il prezzo dell'energia

| Dato | Valore | Etichetta |
|---|---|---|
| PUN (prezzo all'ingrosso) del 23/10/2026 | 240,44 €/MWh, cioè 0,240 €/kWh; media di ottobre fino al 23 uguale | [verificato: comparasemplice.it, aggiornamento del 23/10/2026] |
| Offerte business a prezzo fisso, sola componente energia, IVA e oneri esclusi | 0,166-0,175 €/kWh (offerte Axpo valide da maggio e da agosto 2026) | [verificato: CTE Axpo "Scegli Sereno 2.0", via ricerca] |
| Prezzo usato nei rapporti precedenti | 0,35 €/kWh, forbice 0,30-0,40 | [verificato: ricerca/33 §2.4] |
| Prezzo tutto compreso per una piccola impresa in bassa tensione (energia, perdite, trasporto, oneri, accise) | 0,30-0,45 €/kWh IVA esclusa | [non verificato: stima; serve la bolletta della sede] |

Con il PUN di ottobre a 0,24 €/kWh, un contratto indicizzato arriva facilmente verso 0,35-0,40 €/kWh tutto compreso [non verificato: stima]. Per un'azienda l'IVA si recupera, quindi conta il prezzo IVA esclusa [non verificato: dipende dal regime fiscale di chi paga la bolletta]. Il rack è nel salotto della sede: se la fornitura è domestica, valgono prezzi e IVA diversi [verificato: board "Rack VEVOR 12U · salotto"; conseguenza non verificata].

### 5.4 Alimentatori e margine

- 2 × 800 W Titanium in ridondanza 1+1: se uno si guasta, l'altro deve reggere tutto. Il picco stimato di 690-750 W lato DC sta sotto gli 800 W, ma vicino [non verificato: §5.1].
- HPE, per le GPU qualificate, scrive "1x 1600W PS recommended, but this card will work with 1x800W PS (per GPU)" e rimanda al Power Advisor [verificato: QuickSpecs v58].
- "Mixing of 2 different power supplies is NOT allowed" [verificato: QuickSpecs v58]: i due alimentatori restano uguali.
- **Proposta**: tetto di potenza con `nvidia-smi -pl` sulla RTX 4000 (per esempio 100-110 W) e controllo del picco reale dall'iLO durante una prova di carico con CPU e due GPU al massimo [non verificato].
- Calore: 300 W sono circa 1.020 BTU/h, 790 W circa 2.700 BTU/h [non verificato: calcolo, 1 W = 3,412 BTU/h].

---

## 6. UPS rack 2U

**Dimensionamento** [non verificato]: picco del server 730-790 W più OPNsense (circa 15 W), router del provider e uno switch futuro: circa 800-850 W. Carico tipico circa 300-330 W.

| UPS | Potenza | Autonomia dichiarata | Prezzo | Etichetta |
|---|---|---|---|---|
| **Eaton 5PX 1500i RT2U G2** (5PX1500IRT2UG2) | 1500 VA / **1500 W**, line interactive, rack o torre | 14 min a metà carico (750 W), 5 min a pieno carico | 937,36 € IVA esclusa su it-partners.it (esaurito); 1.144,10 € IVA esclusa su dateks.lv; 1.192,80 € IVA tedesca inclusa (≈ 1.002 € netti) | [verificato: retailer via ricerca del 25/10/2026; ricerca/33 §4.2] |
| APC Smart-UPS SMT1500RMI2UC | 1500 VA / **1000 W**, line interactive, 2U, 4 prese C13 | circa 25 min a metà carico (500 W), circa 7 min a pieno carico | 1.011,42 € IVA esclusa (1.233,93 € inclusa) su it-partners.it; 1.162,99-1.292,99 € IVA inclusa su Yeppon | [verificato: ricerca/33 §4.2 del 24/10/2026; Yeppon via ricerca del 25/10/2026; autonomie da schede di rivenditori] |

- Con due GPU, al picco l'APC lavorerebbe all'80-85 %; l'Eaton al 53-57 % [non verificato: calcolo]. **Consiglio l'Eaton 5PX 1500 G2**, oppure l'APC con il tetto di potenza sulle GPU del §5.4.
- Al carico tipico di circa 300 W entrambi danno, a stima, 35-50 minuti; NUT spegne Proxmox dopo 5-10 minuti a batteria, quindi basta [non verificato: interpolazione].
- I due alimentatori del server vanno tutti e due sull'UPS (o su due UPS), mai uno sull'UPS e uno sulla rete [non verificato: prassi, già in ricerca/15 §5.3].
- Gli alimentatori Titanium accettano solo 200-240 V AC: l'uscita a 230 V dell'UPS va bene [verificato: QuickSpecs v58].
- L'UPS attuale, collegato in USB a OPNsense con NUT, va controllato: potenza e autonomia non sono note, e con la seconda GPU il picco sale [verificato: board; potenza dell'UPS non indicata].

---

## 7. Proxmox Backup Server a casa: Lenovo M920t con due dischi

### 7.1 Requisiti di PBS

| Requisito Proxmox | Etichetta |
|---|---|
| CPU moderna a 64 bit con almeno 4 core | [verificato: pbs.proxmox.com, "System Requirements"] |
| RAM: almeno 4 GiB per sistema, cache e servizi, più almeno 1 GiB per ogni TiB di spazio di backup | [verificato: idem] |
| Spazio di backup: dischi veloci con molte operazioni casuali; i migliori sono gli SSD enterprise | [verificato: idem] |
| Con dischi meccanici: "Using a metadata cache is highly recommended", per esempio un mirror ZFS "special device" | [verificato: idem] |
| Sistema: almeno 32 GiB, su ZFS ridondante o RAID con cache protetta | [verificato: idem] |

### 7.2 Il Lenovo M920t

| Dato | Valore | Etichetta |
|---|---|---|
| Vani | 2 da 3,5" (uno opzionale), 1 da 2,5" opzionale, 1 slot M.2 NVMe (PCIe 3.0) | [verificato: Lenovo PSREF ThinkCentre M920 Tower] |
| Memoria | fino a 64 GB DDR4-2666, 4 slot | [verificato: idem] |
| Dischi elencati | 3,5" fino a 2 TB ciascuno | [verificato: idem]; dischi più grandi di solito funzionano [non verificato] |
| Rete | 1 Gbit/s, Intel I219-LM, Wake-on-LAN | [verificato: idem] |
| Alimentatore | 180, 250 o 400 W | [verificato: idem] |
| Ricondizionato in Italia, i5-8500 | 185,99 € (8 GB, 256 GB SSD, refurbed.it, oggi esaurito); 279,99 € (32 GB, 240 GB SSD più 2 TB, Extremebit, esaurito); 349,68-359 € (32 GB, RigeneraTech); 355 € (8 GB, PcComponentes) | [verificato: ricerche del 25/10/2026; tutti IVA inclusa; disponibilità variabile] |

### 7.3 Dischi e configurazione

| Voce | Prezzo | Etichetta |
|---|---|---|
| Seagate IronWolf 4 TB | 195 € (era 94 € un anno prima) | [verificato: DriveVault del 17/09/2026, che cita il controllo prezzi di ComputerBase del 16/09/2026, Germania, IVA inclusa] |
| WD Red Plus 8 TB | 349 € (era 170 €) | [verificato: idem] |
| Disco enterprise rigenerato da 14 TB (Toshiba MG07ACA14TE, Bargain Hardware) | £235 IVA esclusa (£282 inclusa) | [verificato: bargainhardware.co.uk, 25/10/2026] |
| 2 SSD piccoli per sistema e metadati (M.2 NVMe più SATA da 2,5", 256-512 GB) | 60-120 € | [non verificato: stima] |

**Configurazione proposta** [non verificato]: due dischi da 3,5" in mirror ZFS per i backup; l'SSD M.2 e l'SSD da 2,5" in mirror, divisi in due partizioni: sistema di PBS e "special device" per i metadati. Se si perde lo special device si perde l'intero pool: per questo va in mirror. 16 GB di RAM bastano fino a circa 10 TiB di backup.

**Che taglia** [non verificato]: i dati da proteggere sono le VM su rpool (circa 0,7 TiB) e i dati su tank (fino a circa 4,9 TiB). Con la deduplica di PBS, 4 TB bastano all'inizio se i dati veri sono 1-2 TB; con tank piena servono 8 TB o più. Va deciso dopo aver letto quanto è davvero occupato.

**La rete di casa** [non verificato]: la casa è su Starlink dietro CGNAT e il PBS si raggiunge via NetBird [verificato: board]. Il primo backup completo di qualche TB su Starlink può richiedere giorni: conviene farlo in sede, collegando l'M920t alla rete dell'ufficio, e poi portarlo a casa per gli incrementali notturni.

**Costo totale del PBS**: M920t 186-360 € più dischi 390-700 € più SSD 60-120 €, cioè **circa 640-1.180 € IVA inclusa** [non verificato: somma]. È più di quanto stimato in ricerca/33 (circa 290-610 €), perché i dischi sono raddoppiati di prezzo [verificato: ricerca/33 §4; DriveVault]. Corrente: acceso circa 3 ore a notte a 30-35 W, circa 3 kWh al mese, meno di 1,5 € [non verificato].

---

## 8. Quadro delle spese hardware

| Voce | Fase | Basso | Alto | IVA | Etichetta |
|---|---|---|---|---|---|
| Lettura della RAM nell'iLO, prova di carico, tetto ARC | F0-F1 | 0 € | 0 € | | [non verificato] |
| PBS a casa: M920t, 2 HDD, 2 SSD | F1 | 640 € | 1.180 € | inclusa | [non verificato: §7] |
| Seconda GPU RTX 2000 Ada 16 GB | F4 o F5 | 837 € | 946 € | inclusa | [verificato: §4.3] |
| in alternativa RTX PRO 2000 Blackwell | F4 o F5 | 1.090 € | 1.425 € | inclusa | [verificato: §4.3] |
| Staffa ad altezza piena, riser secondario se manca | con la GPU | 10 € | 110 € | inclusa | [non verificato per la staffa; riser verificato §4.4] |
| RAM +192 GB (12 × 16 GB) | prima di bot e Andrea | 816 € (2133, UE) | 1.218 € (2666, Bargain) | esclusa | [verificato: §2.4; conversione non verificata] |
| in alternativa RAM +64 GB (4 × 16 GB) | | 272 € | 512 € | esclusa | [verificato: §2.4] |
| UPS rack 2U | F5 | 937 € | 1.144 € (Eaton) / 1.293 € IVA inclusa (APC) | vedi §6 | [verificato: §6] |
| Corrente in più per GPU e RAM | ogni mese | 9 € | 18 € | | [non verificato: §5.2] |

---

## 9. Rischi

| Rischio | Impatto | Contromisura |
|---|---|---|
| RAM finita con tutte le funzioni accese | VM che vanno in swap o non partono | RAM a 384 GB prima di bot e Andrea; tetto ARC; tetto alle sessioni di agenti [non verificato] |
| Moduli misti (velocità, rank, x4 e x8) nello stesso server | avvisi nell'IML, velocità più bassa | comprare moduli uguali a quelli montati; memtest e controllo dell'IML [non verificato] |
| Seconda GPU non qualificata e due GPU diverse | ventole rumorose o temperature non viste dall'iLO; nessun supporto HPE | scheda con ventola propria; `nvidia-smi` nel monitoraggio; aria in ingresso sotto 27 °C [non verificato] |
| Picco vicino agli 800 W di un alimentatore | spegnimento se un alimentatore si guasta sotto carico pieno | tetto di potenza sulla RTX 4000; prova di carico con lettura dall'iLO [non verificato] |
| Blackwell e librerie audio | faster-whisper o altri motori senza supporto per la nuova architettura | prova prima dell'acquisto, oppure RTX 2000 Ada [non verificato] |
| Rumore e calore nel salotto | disturbo, prestazioni ridotte d'estate | porta chiusa o locale separato; condizionatore; profilo ventole "Optimal Cooling" [non verificato] |
| CPU fuori dagli aggiornamenti Intel dal 30/06/2025 | possibile rilievo nel perimetro Cyber Essentials | chiedere all'assessor; controllare che HPE pubblichi ancora firmware per il Gen10 [verificato: data Intel; effetto su Cyber Essentials non verificato] |
| Prezzi di RAM e dischi in salita | budget superato | preventivi subito; acquisto nell'ordine Bargain se ancora aperto [verificato: tendenza del §2.4 e §7.3] |
| Spedizione dal Regno Unito in Sardegna | dogana e IVA all'arrivo, tempi | preventivo diretto di Bargain; chiarire chi compra [verificato: T&C Bargain] |

---

## 10. Domande aperte per Michele

1. Come sono fatti i 192 GB: quanti moduli, che velocità (2133 o 2666), rank e organizzazione (x4 o x8), moduli HPE o no?
2. L'ordine Bargain è ancora aperto? Quanto costa, chi compra (Sersan Limited o un soggetto italiano) e come arriva in Sardegna, che Bargain esclude dalla spedizione con dazi inclusi?
3. Quali riser ci sono (secondario 870548-B21?), quale controller dei dischi (E208i-p in uno slot o E208i-a) e quali slot sono liberi?
4. Quale seconda GPU intendevi: A2000 12 GB, RTX 2000 Ada 16 GB o RTX PRO 2000 Blackwell 16 GB? E la vuoi nella fase F5 o già in F4, per avere audio e Andrea anche la sera?
5. UPS attuale: potenza in VA e W e autonomia. Regge un picco di circa 800 W con due GPU?
6. Che contratto elettrico ha la sede (business o domestico) e quanto costa il kWh tutto compreso?
7. Che temperatura raggiunge il salotto d'estate, e il rumore delle ventole è accettabile lì?
8. Quanti TB sono davvero occupati su rpool e tank? Serve per scegliere dischi da 4 o 8 TB per il PBS.
9. Per Cyber Essentials va bene una CPU che Intel non aggiorna più dal 30/06/2025? HPE pubblica ancora firmware per il DL380 Gen10?
10. Vogliamo far girare di notte un modello grande in RAM sui dati sensibili? Se sì, i 384 GB servono comunque.

---

## Fonti

Date di consultazione: tutte il 25/10/2026, salvo dove indicato.

**Ufficiali (produttore, ente, documentazione)**
- HPE QuickSpecs ProLiant DL380 Gen10, Version 58 del 10/01/2023, copia integrale: https://assets.catalog.boschbuildingtechnologies.com/public/documents/QS_HPE_DL380G10_Special_enUS_42274285579.pdf (memoria, riser, acceleratori, alimentatori). Copia locale del testo letta oggi: scratchpad `qs/qs.txt`
- HPE QuickSpecs ProLiant DL380 Gen10, versione US 24 del 01/07/2019 (tabella dei processori, Gold 5218): copia locale `qs2/qs-us.txt`
- Intel, Xeon Gold 5218: https://www.intel.com/content/www/us/en/products/sku/192444/intel-xeon-gold-6230-processor-27-5m-cache-2-10-ghz/specifications.html (l'indirizzo cita la 6230 ma la pagina è della 5218)
- Lenovo Press LP1089, "Balanced Memory Configurations with Second-Generation Intel Xeon Scalable Processors": https://lenovopress.lenovo.com/lp1089.pdf
- Proxmox VE, ZFS on Linux (limite ARC): https://pve.proxmox.com/wiki/ZFS_on_Linux
- Proxmox Backup Server, requisiti di sistema: https://pbs.proxmox.com/docs/installation.html
- Lenovo PSREF ThinkCentre M920 Tower: https://psref.lenovo.com/syspool/Sys/PDF/ThinkCentre/ThinkCentre_M920_Tower/ThinkCentre_M920_Tower_Spec.html
- Datasheet PNY RTX PRO 2000 Blackwell (maggio 2026): https://www.pny.com/File%20Library/Company/Support/Product%20Brochures/NVIDIA%20RTX/English/NVIDIA-RTX-PRO-2000-Blackwell-Datasheet.pdf
- Datasheet PNY RTX PRO 4000 Blackwell SFF Edition: https://www.pny.com/file%20library/company/support/product%20brochures/nvidia%20rtx/english/nvidia-rtx-pro-4000-blackwell-sff-edition-datasheet.pdf
- Datasheet NVIDIA RTX 2000 Ada (copia HP): https://valuehub.hp.com/static/nvidia/docs/NVIDIA%20RTX%202000%20Ada%20Generation%20Datasheet.pdf
- Datasheet NVIDIA RTX 4000 SFF Ada: https://www.nvidia.com/content/dam/en-zz/Solutions/products/workstations/nvidia-rtx-4000-sff-datasheet.pdf
- Datasheet NVIDIA RTX A2000 (via ricerca): https://www.nvidia.com/content/dam/en-zz/pt_br/Solutions/design-visualization/rtx-a2000/nvidia-rtx-a2000-datasheet-pt-br.pdf ; Lenovo Press LP1919: https://lenovopress.lenovo.com/LP1919
- NVIDIA A2 e T4 (via ricerca): https://www.nvidia.com/en-us/data-center/products/a2/ ; https://nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-t4/t4-tensor-core-datasheet.pdf
- NVIDIA L4 su HPE (via ricerca): https://www.hpe.com/us/en/product-catalog/options/pip.specifications.nvidia-accelerators.1014731952.html
- NVIDIA, moduli kernel open source: https://developer.nvidia.com/blog/nvidia-transitions-fully-towards-open-source-gpu-kernel-modules/ ; https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html
- CUDA 12.8, nuove architetture (via ricerca): https://docs.nvidia.com/cuda/archive/12.8.0/cuda-features-archive/index.html
- SPECpower DL380 Gen10, 28/08/2018: https://www.spec.org/power_ssj2008/results/res2018q3/power_ssj2008-20180828-00850.html
- BCE, tassi di riferimento del 23/10/2026: https://www.ecb.europa.eu/stats/exchange/eurofxref/shared/pdf/2026/10/20261023.pdf

**Venditori e listini**
- Bargain Hardware, configuratore DL380 Gen10: https://www.bargainhardware.co.uk/hp-proliant-dl380-g10-2u-rack-server-configure-to-order ; Termini e condizioni: https://www.bargainhardware.co.uk/terms-conditions/ ; blog del 01/04/2026: https://www.bargainhardware.co.uk/blog/blog/why-is-ram-so-expensive-in-2026-an-update-for-enterprise-it-buyers
- Servermall, configuratore Dell R740 (prezzi di RAM e GPU): https://servermall.com/it/config/dell-r740-16-2-5-5185/
- datacenterdisk (RAM, luglio 2026, via ricerca): https://datacenterdisk.com/drives/samsung-16gb-ddr4-2133-bzw5 ; https://datacenterdisk.com/server-ram/ddr4
- gpuprix (24/10/2026): https://gpuprix.com/it/gpus/rtx-a2000 ; https://gpuprix.com/italy/gpus/rtx-2000-ada-generation ; https://gpuprix.com/italy/gpus/rtx-pro-2000-blackwell ; https://gpuprix.com/germany/gpus/rtx-a2000 ; https://gpuprix.com/germany/gpus/rtx-2000-ada-generation ; https://gpuprix.com/germany/gpus/rtx-pro-2000-blackwell ; https://gpuprix.com/germany/gpus/rtx-4000-sff-ada-generation ; https://gpuprix.com/uk/gpus/rtx-a2000 ; https://gpuprix.com/uk/gpus/rtx-2000-ada-generation ; https://gpuprix.com/uk/gpus/rtx-pro-2000-blackwell
- hardwaredealz (25/10/2026 ore 15:20): https://www.hardwaredealz.com/hardware/gpu/nvidia-rtx-2000-ada-generation/preisvergleich.33598 ; https://www.hardwaredealz.com/hardware/gpu/nvidia-rtx-pro-2000-blackwell-16gb/pny-16gb-gddr7-4x-mdp/preisvergleich.30571 ; https://www.hardwaredealz.com/hardware/gpu/nvidia-rtx-pro-2000-blackwell-16gb/nvidia-16gb-gddr7-4x-mdp-retail/preisvergleich.30565
- Scan, PNY RTX PRO 2000 Blackwell OEM: https://www.scan.co.uk/products/pny-nvidia-rtx-pro-2000-blackwell-oem
- geizhals, NVIDIA L4 (via ricerca): https://geizhals.de/fujitsu-s26361-f3166-r523-a1712951.html ; https://geizhals.de/nvidia-l4-900-2g193-0000-001-a3464751.html
- SHI (via ricerca): https://www.shi.com/product/48300464/NVIDIA-RTX-2000E-Ada-Generation ; https://eu.shi.com/product/49992647/NVIDIA-RTX-PRO-4000-Blackwell ; https://www.de.shi.com/product/44505100/NVIDIA-A2-GPU-computing-processor
- Riser 870548-B21 (via ricerca): https://serverschmiede.com/en/hp-primary-secondary-2nd-riser-pcie-x8-x16-x8-2nd-gpu-ready-incl-cage-dl560-dl380-gen10-870548-b21
- Staffa della RTX 2000 Ada (via ricerca): https://www.hrp.hu/pny-nvidia-rtx-2000-ada-16gb-128bit-2816-cuda-pcie-4-0-x8-4xmdp-1-4a-3ev-vcnrtx2000ada-pb
- UPS (via ricerca): https://it-partners.it/en/products/eaton-5px1500irt2ug2-gruppo-di-continuita-ups-a-linea-interattiva-1500-kva-1500-w-8-presa-e-ac-5px1500irt2ug2 ; https://www.dateks.lv/en/cenas/ups/761823-eaton-5px1500irt2ug2-1500va-1500w-iec-2u ; https://shop.winpro.com.sg/products/eaton-5px1500irt2ug2-line-interactive-ups-9210-63060 ; https://www.yeppon.it/collections/smart-ups-1500-apc ; https://happyware.com/uk-en/apc-smt1500rmi2uc
- M920t (via ricerca): https://www.refurbed.it/en-it/p/lenovo-thinkcentre-m920t-tower ; https://extremebit.it/core-i5-8a-generazione/5520-lenovo-thinkcentre-m920t-tower-pc-computer-intel-i5-8500-ram-32gb-hdd-2tb-ssd-240gb-freedos-ricondizionato-grado-a-8052275528415.html ; https://www.rigeneratech.it/pc-intel-core-i5/4369-pc-intel-core-i5-pc-tower-ricondizionato-lenovo-thinkcentre-m920t-i5-8500-ram-32gb-ssd-256gb-hdd-2tb-windows-11-pro-office.html ; https://www.pccomponentes.it/ssd-lenovo-thinkcentre-m920t-intel-core-i5-8500-8-gb-256-gb
- Dischi: https://www.drivevault.io/blog/when-will-hard-drive-prices-come-down.html (17/09/2026)

**Misure e dati di terzi**
- Consumo della Quadro RTX 4000 (via ricerca): https://servethehome.com/nvidia-quadro-rtx-4000-review-a-versatile-ai-and-professional-gpu/7 ; https://www.igorslab.de/en/nvidia-quadro-rtx-4000-im-test-guenstiger-profi-abger-with-surprise-performance-igorslab/9/
- Dischi Exos 10E2400 (via ricerca): https://www.alza.cz/EN/seagate-exos-10e2400-1-8tb-fastformat-sas-d5855800.htm
- DL380 Gen10 con 2 Gold 6144 (via ricerca): https://voxility.com/dedicated-server/prices/DL380+Gen10+(2xGold+6144)+8-LFF+%2B+2-NVMe
- RTX PRO 500 Blackwell per portatili (via ricerca): https://www.notebookcheck.net/Nvidia-RTX-PRO-500-Blackwell-Generation-Laptop-Benchmarks-and-Specs.997332.0.html
- Forum HPE, capacità miste (via ricerca): https://community.hpe.com/t5/proliant-servers-ml-dl-sl/maximum-ram-support-hpe-proliant-dl380-gen10/m-p/7220436/highlight/true
- PUN del 23/10/2026: https://www.comparasemplice.it/informazioni/news/pun-aggiornamento-del-23-10-2026
- Offerte business Axpo (via ricerca): https://www.axpo.com/content/dam/axpo19/italy/cte-offerte-business/Scegli%20Sereno%202.0_2608.pdf

**Interne**
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt` (vincolanti)
- `ricerca/01-sersanoutreach.md` (tetti di memoria di SersanOutreach)
- `ricerca/13-modelli-open-source-sul-server.md` (velocità della RTX 4000, Turing, modelli MoE in RAM)
- `ricerca/15-hardware-server-e-rete.md` (moduli 2133 comprati, cavo GPU, collocazione)
- `ricerca/25-board-michele-e-delta.md` (voci H01-H13)
- `ricerca/26-claude-agent-sdk.md` (RAM per sessione)
- `ricerca/28-chat-di-gruppo-self-hosted.md`, `ricerca/30-call-e-trascrizione-self-hosted.md`, `ricerca/31-voce-andrea-self-hosted.md` (RAM e VRAM dei servizi)
- `ricerca/33-costi-v2.md` (prezzi di UPS e M920t del 24/10/2026, prezzo dell'energia)
