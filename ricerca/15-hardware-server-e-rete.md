# 15. Server, rete e messa in produzione

- **Data di rilevazione**: 2026-10-24. Prezzi e versioni valgono a questa data.
- **Scopo**: valutare il server già comprato (presunto HPE ProLiant DL380 Gen10), il mini PC usato come firewall, e dire come metterli in produzione per il sistema multi-agente e per SersanOutreach. Sono fatti e scelte consigliate, senza domande ai CEO.
- **Legenda**: `[verificato: fonte]` = letto sulla fonte citata; `[voce di terzi: fonte]` = rivenditori, forum, articoli, non la pagina ufficiale del produttore; `[non verificato]` = deduzione o stima mia; `non trovato` = il dato non c'è nelle fonti consultate.
- **Fonte principale sul server**: HPE QuickSpecs «HPE ProLiant DL380 Gen10 Server», **Version 58 del 10-gen-2023** (91 pagine). I siti HPE (hpe.com, psnow) non hanno risposto il 2026-10-24 (timeout, DNS), e il forum HPE ha risposto 403. Ho quindi letto una copia integrale del PDF HPE ospitata da Bosch: https://assets.catalog.boschbuildingtechnologies.com/public/documents/QS_HPE_DL380G10_Special_enUS_42274285579.pdf. Il testo estratto è in `C:/Users/alber/AppData/Local/Temp/claude/C--Users-alber-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-09111ff7-b928-4377-9e53-68163227cdf4-abed6156-6df6-48ee-8417-c08b37213fdb-scratch-2026-10-24-761cec/e50fa6e2-0eec-433c-9aed-bd091fd494f8/scratchpad/qs/qs.txt` (il PDF è nella stessa cartella, `qs.pdf`).

---

## 0. In breve

1. **Il server va bene per il compito**: un DL380 Gen10 con 160 GB di RAM regge tutti i servizi di SersanOutreach (oggi 8 servizi con 7,4 GiB di tetti di memoria) più gli agenti, il monitoraggio e una GPU per modelli piccoli. Il limite vero non è la potenza: sono **rumore, calore, corrente e un solo punto di guasto** `[verificato per SersanOutreach: ricerca/01-sersanoutreach.md riga 20; il resto è non verificato]`.
2. **RAM**: HPE elenca per il Gen10 solo moduli SmartMemory DDR4-2666 e 2933, e scrive che «HPE DDR4 SmartMemory is required» per avere le prestazioni dichiarate. I moduli PC4-2133P comprati non sono in elenco: con ogni probabilità funzionano, ma a 2133 MT/s e senza supporto HPE `[verificato: QuickSpecs §Memory; il «funzionano» è non verificato]`.
3. **10 moduli sono una configurazione sbilanciata** secondo la tabella HPE (sia 10 su una CPU, sia 5+5 su due CPU). Le scelte bilanciate sono 8 moduli (128 GB) subito, oppure 12 moduli (192 GB) comprandone altri 2 `[verificato: QuickSpecs §Memory Population guidelines]`.
4. **GPU**: la Quadro RTX 4000 **non è nell'elenco degli acceleratori qualificati** HPE per il DL380 Gen10. Per qualunque GPU HPE richiede il **High Performance Fan Kit 867810-B21** e il **High Performance Heat Sink Kit 826706-B21**. La scheda (160 W, singolo slot) va nello slot 2 x16 del riser primario e ha bisogno del cavo di alimentazione supplementare `[verificato: QuickSpecs §Optional Features, §Accelerators; 160 W da Gigabyte]`.
5. **Rumore**: HPE dichiara 31-37 dBA nella posizione dell'astante, ma solo per le configurazioni standard. Con GPU, ventole ad alte prestazioni e componenti non HPE le ventole girano più forte. **Il server non va in un ufficio dove si lavora**: serve uno stanzino o un locale tecnico ventilato `[verificato per i dBA: QuickSpecs §Acoustic Noise; il resto è non verificato]`.
6. **Corrente**: stima 120-300 W medi, cioè 28-70 € al mese a 0,32 €/kWh. In Sardegna (comuni piccoli, E-Distribuzione, 2023) ogni utente in bassa tensione ha avuto in media **8,29 interruzioni** e 91,66 minuti persi l'anno: **l'UPS è obbligatorio** `[verificato per ARERA; stima per i consumi]`.
7. **Firewall**: il mini PC Pentium 4417U (2 core, 4 thread, 15 W) basta per OPNsense con NAT a 1 Gbit/s e per WireGuard del team. **Non basta** per fare IDS e VPN a 2,5 Gbit/s pieni, e l'ufficio non ne ha bisogno `[non verificato: stima su prove Thomas-Krenn di CPU simili]`.
8. **Esposizione su internet senza aprire porte**: **Cloudflare Tunnel** per gli indirizzi pubblici (webhook Instantly, `outreach.sersan.io` per l'estensione Chrome), perché il DNS è già su Cloudflare e Funnel di Tailscale accetta solo nomi `*.ts.net`. L'accesso del team va su **WireGuard in OPNsense** (gratis) o su **Tailscale Standard** a 8 $/utente/mese `[verificato: tailscale.com/pricing, docs Funnel; ricerca/01 riga 121]`.
9. **Sistema**: **Proxmox VE 9.x** (oggi 9.2, Debian 13) con una VM Ubuntu e Docker per le applicazioni, la GPU in una VM (passthrough) o in un container LXC, e i backup con Proxmox Backup Server più una copia fuori sede. Proxmox costa 0 € senza abbonamento, oppure 120 € l'anno per socket CPU con il repository enterprise `[verificato: proxmox.com pricing; comunicato 9.2 tramite ricerca]`.
10. **La checklist in 10 passi è al §7**. Il primo passo è identificare con l'iLO il modello esatto, le CPU, gli alimentatori e le ventole: da lì dipendono RAM, GPU e consumi.

---

## 1. Cosa è stato comprato e a cosa serve

| Componente | Prezzo pagato | A cosa serve | Giudizio |
|---|---|---|---|
| NVIDIA Quadro RTX 4000 8 GB GDDR6 (Turing), usata | 279 € | inferenza locale: trascrizione, embedding, modelli piccoli | adatta a modelli fino a circa 7-8 GB di VRAM; non qualificata HPE (§2.3) |
| 10 × 16 GB Samsung 2Rx4 PC4-2133P ECC RDIMM | 690 € | 160 GB di RAM | funziona con ogni probabilità, a 2133 MT/s; 10 moduli sono sbilanciati (§2.2) |
| HPE Smart Array E208i-p SR Gen10 (804394-B21) | 52,70 € | controller per i dischi SAS/SATA | va bene in modalità HBA per ZFS; non ha cache, quindi il RAID 5 hardware è lento in scrittura (§2.5) |
| Cavo di alimentazione GPU mini 8 pin → 6+8 pin «per HP DL380 G10» | 10,80 € | alimentazione supplementare della GPU | da controllare con il tester prima dell'uso, o da sostituire con il cavo HPE (§2.3) |
| Rack open frame 12U, 4 montanti, con ruote | 87,99 € | ospitare server, firewall, UPS | il formato a 4 montanti è giusto; vanno verificati la profondità utile e il tipo di fori (§3.3) |
| Cavi patch Cat6A 0,5 m | non indicato | collegamenti nel rack | adatti fino a 10 Gbit/s |
| Mini PC fanless Pentium 4417U, 4 × Intel i226-V 2,5G | 121 € | router e firewall | adeguato per l'ufficio (§4.1) |

Manca dalla lista: **UPS**, **dischi** (non indicati), **kit ventole e dissipatori HPE per la GPU** se il server non li ha già, **guide (rail kit)** se non sono incluse, ed eventualmente uno **switch gestito**. Un modo di fare a meno dello switch è al §4.2.

---

## 2. Il server: HPE ProLiant DL380 Gen10

### 2.1 Prima cosa: identificare il server

Il modello è presunto. Il cavo «per DL380 G10» e l'E208i-p «SR Gen10» sono coerenti con un Gen10, ma non lo provano: un Gen10 Plus usa memoria DDR4-3200 e cavi GPU diversi (8/12 pin) `[voce di terzi: listini dei kit P59212-B21 e P61423-B21 per Gen10 Plus]`. Dall'iLO (o dall'etichetta estraibile sul frontale) vanno letti:

| Dato | Perché conta | Dove si legge |
|---|---|---|
| Modello esatto e numero di serie | Gen10 o Gen10 Plus cambia RAM, cavi e firmware | etichetta estraibile «serial label pull tag» sul frontale `[verificato: QuickSpecs §Overview]`, iLO → Information |
| Numero e modello delle CPU | velocità della RAM, slot PCIe disponibili, consumi | iLO → System Information |
| Alimentatori (500 W o 800 W, uno o due) | margine per la GPU, ridondanza | iLO → Power |
| Tipo e numero di ventole (standard o high performance) | requisito HPE per la GPU | iLO → Fans |
| Gabbia dischi (8 SFF, 24 SFF, LFF) | quali dischi si possono montare | ispezione visiva |
| Scheda di rete FlexibleLOM (es. 4 × 1GbE) | collegamento al firewall | iLO → Network |
| Versioni firmware (System ROM, iLO, Innovation Engine) | i problemi di ventole risolti con gli aggiornamenti | iLO → Firmware |

**Con una sola CPU sono attivi solo i 3 slot del riser primario e solo 12 slot di memoria**: il riser secondario e quello terziario richiedono il processore 2 `[verificato: QuickSpecs §Secondary/Tertiary Riser, «Install DIMMs only if the corresponding processor is installed»]`.

### 2.2 Memoria

| Fatto | Etichetta |
|---|---|
| 24 slot, **12 per processore, 6 canali per processore, 2 DIMM per canale** | `[verificato: QuickSpecs §Memory]` |
| Tipi supportati: HPE DDR4 SmartMemory RDIMM o LRDIMM; non si mescolano RDIMM e LRDIMM | `[verificato: QuickSpecs §Memory]` |
| I kit HPE in elenco sono solo **DDR4-2666 e DDR4-2933**; nessun 2133 | `[verificato: QuickSpecs §Memory, elenco kit]` |
| «To realize the performance memory capabilities listed in this document, HPE DDR4 SmartMemory is required» | `[verificato: QuickSpecs §Memory]` |
| La velocità massima dipende da tipo di memoria, configurazione e processore; le CPU Bronze 32xx vanno comunque a 2133 MT/s | `[verificato: QuickSpecs §Memory Population, tabella processori]` |
| Moduli da 2133 in un Gen10: girano a 2133 MT/s (il minimo tra CPU e modulo) | `[non verificato: comportamento standard DDR4, non confermato da HPE]` |
| Un dipendente HPE sul forum scrive che i moduli non HPE possono generare errori | `[voce di terzi: community.hpe.com, citato nei risultati di ricerca, pagina non aperta (403)]` |
| Moduli Samsung 2Rx4 PC4-2133P da 16 GB sono tipici dei kit HPE **Gen9**; HPE non garantisce i moduli Gen9 nel Gen10 | `[non verificato]` |

**Popolazione.** La tabella HPE per 12 slot per CPU segna con l'asterisco «Unbalanced, not recommended» le configurazioni da **5, 7, 9, 10 e 11 moduli** per processore. Sono bilanciate quelle da 4, 6, 8 e 12 `[verificato: QuickSpecs §Memory Population guidelines]`. Con 2 CPU HPE chiede anche quantità pari e la stessa capacità sulle due CPU `[verificato: idem]`.

| CPU installate | Configurazione | RAM | Bilanciata secondo HPE | Nota |
|---|---|---|---|---|
| 1 | 10 moduli | 160 GB | **no** | funziona, prestazioni di memoria non uniformi `[non verificato]` |
| 1 | 6 moduli (1 per canale) | 96 GB | sì | massima banda per modulo |
| 1 | 8 moduli | 128 GB | sì | 2 moduli restano di scorta |
| 1 | 12 moduli (2 per canale) | 192 GB | sì | servono 2 moduli in più |
| 2 | 5 + 5 | 160 GB | **no** | un canale vuoto per CPU |
| 2 | 4 + 4 | 128 GB | sì | 2 moduli restano di scorta |
| 2 | 6 + 6 | 192 GB | sì | **la migliore**: tutti i 12 canali pieni; servono 2 moduli in più |

**Scelta consigliata**: partire con **8 moduli (128 GB)**, bilanciati, e tenere 2 moduli di scorta per i guasti. Se le CPU sono due, comprare **altri 2 moduli uguali** e arrivare a 6+6 (192 GB). Al prezzo pagato (690 € / 10 = 69 € a modulo) sono circa 138 € `[calcolo; prezzo di mercato non verificato]`. Negli slot vuoti vanno lasciati i «DIMM blank», perché HPE li richiede per il flusso d'aria in alcune configurazioni `[verificato: QuickSpecs, nota «Must install DDR4 DIMM blanks (P07818-B21) on all empty DIMM slots»]`.

**Banda**: 6 canali a 2133 MT/s fanno circa 102 GB/s teorici per socket, contro circa 141 GB/s a 2933 (−27 %) `[calcolo: canali × MT/s × 8 byte]`. Pesa solo sull'inferenza LLM su CPU. Gli agenti che chiamano le API Anthropic non se ne accorgono.

**Prova obbligatoria**: 24 ore di memtest86+ (incluso nell'ISO di Proxmox) prima di mettere dati veri, poi un controllo dell'IML (Integrated Management Log) dell'iLO per errori corretti ECC `[non verificato: procedura consigliata]`.

### 2.3 GPU: Quadro RTX 4000

**La scheda** `[voce di terzi: pagina prodotto Gigabyte, flopper.io, annunci]`:

| Dato | Valore |
|---|---|
| Memoria | 8 GB GDDR6, 256 bit, fino a 416 GB/s |
| Consumo massimo | 160 W (Gigabyte); 125 W di «total graphics power» secondo flopper.io, con la differenza attribuita alla porta VirtualLink USB-C |
| Formato | singolo slot, full height, raffreddamento attivo a turbina |
| Connettore | 1 × 8 pin PCIe (solo da un annuncio, non confermato dal produttore) |

**Cosa dice HPE per le GPU nel DL380 Gen10** `[verificato: QuickSpecs v58]`:

- Il riser primario standard ha lo **slot 2 PCIe 3.0 x16, full height, full length**; gli slot 1 e 3 sono x8 `[§Primary Riser]`. La RTX 4000 va nello slot 2.
- «High performance fan kits are required for rear drives, Graphics (GPU) card or NVMe configurations» `[§System Fans]`.
- **HPE DL38X Gen10 High Performance Temperature Fan Kit 867810-B21**: «also required to support GPUs configurations» `[§Optional Features]`.
- **HPE DL380 Gen10 High Performance Heat Sink Kit 826706-B21**: «Required for GPU installations». Le CPU sopra i 130 W lo hanno già di serie `[§Optional Features]`.
- I server 24 SFF e 12 LFF escono già con le 6 ventole high performance; quelli 8 SFF con 1 CPU di solito escono con 4 ventole standard `[§System Fans]`.
- L'elenco degli acceleratori qualificati comprende tra le altre T4, A2, A30, A40, A100, V100 e Radeon Instinct MI25. **Non c'è nessuna Quadro**: la RTX 4000 è una scheda non supportata da HPE `[§Accelerators; ricerca «Quadro» nel testo: 0 risultati]`.
- Per le GPU qualificate HPE fissa una **temperatura massima dell'aria in ingresso** per tipo di chassis: per la T4, per esempio, 35 °C sull'8 SFF, 30 °C o 20 °C su altri chassis `[§Accelerators, tabella]`. Per la RTX 4000 non c'è un valore, perché non è qualificata.
- Un «GPU enablement kit» come codice unico: **non trovato** nella QuickSpecs v58.

**Alimentazione della GPU.** Lo slot x16 dà al massimo 75 W (standard PCIe), quindi serve il cavo supplementare `[non verificato: dato dello standard PCIe, non dalla QuickSpecs]`. Il cavo HPE per i DL38X Gen10 è il kit **P03849-B21** (da 1 × 8 pin sulla scheda madre a 2 × 8 pin, 25 cm, ricambio P04670-001); un altro ricambio venduto come «8-pin GPU power cable» è il 869820-001 `[voce di terzi: listini Gekko Computer, Serverschmiede, Express Computer Systems]`. Il cavo comprato (mini 8 pin → 6+8) è di terze parti: i connettori di alimentazione delle schede madri server non sempre seguono la piedinatura PCIe standard, quindi **prima di accendere va controllato con un tester** che i 12 V e le masse arrivino sui pin giusti del connettore 8 pin PCIe. Altrimenti va comprato il P03849-B21 `[non verificato: precauzione]`.

**Ventole e rumore con una GPU non HPE.** L'iLO non legge la temperatura di una scheda non HPE. Diversi utenti segnalano ventole molto più veloci dopo aver montato GPU o controller di terze parti. Un tecnico HPE ha indicato come correzione l'aggiornamento di Innovation Engine (0.2.2.0 o successivo) e iLO (2.15 o successivo); altri consigliano «Optimal Cooling» nel BIOS (RBSU). Un utente ha forzato le ventole al 50 % via Redfish, avvertendo lui stesso di non farlo in produzione `[voce di terzi: thread community.hpe.com riassunti nei risultati di ricerca; pagine non aperte, 403]`. **Scelta consigliata**: firmware aggiornati, profilo «Optimal Cooling», ventole high performance come chiede HPE, e controllo della temperatura della GPU con `nvidia-smi` sotto carico. Niente forzature manuali delle ventole.

**Che cosa ci gira** (riferimento, non verdetto): con 8 GB entrano un modello di trascrizione, un modello di embedding e un LLM da 3-4 miliardi di parametri quantizzato.

### 2.4 Alimentatori

| Alimentatore HPE Flex Slot | Codice | Tensione | Nota |
|---|---|---|---|
| 500 W Platinum | 865408-B21 | 100-240 VAC | fino al 94 % di efficienza |
| 800 W Platinum | 865414-B21 | 100-240 VAC | fino al 94 % |
| 800 W Titanium | 865438-B21 | 200-240 VAC | fino al 96 % |
| 1600 W Platinum | 830272-B21 | 200-240 VAC | |

`[verificato: QuickSpecs §HPE Power Supplies e §Technical Specifications]`

- Le linee guida HPE del Gen9 ammettevano le GPU fino a 150 W con alimentatori da 800 W e chiedevano 1400 W per quelle più potenti `[voce di terzi: thread HPE community Gen9; non verificato per il Gen10]`.
- Stima del picco con 2 CPU da 125-150 W, GPU da 160 W, 10-12 moduli RAM, ventole high performance, dischi e controller: **circa 550-700 W** `[non verificato: stima mia]`. **Un alimentatore da 500 W non basta**. Con due alimentatori da 500 W la macchina funziona, ma oltre i 500 W di carico **la ridondanza si perde**.
- **Scelta consigliata**: **2 × 800 W Platinum (865414-B21)** in ridondanza 1+1. Va controllato il consumo reale dal contatore dell'iLO durante una prova sotto carico. HPE indica il suo **Power Advisor** per il dimensionamento `[verificato: QuickSpecs, «please use the HPE Power Advisor Tool»]`.

### 2.5 Controller E208i-p e dischi

| Fatto | Etichetta |
|---|---|
| E208i-p: 8 linee interne, **nessuna cache**, 12G SAS, scheda PCIe; in elenco tra gli «Essential RAID Controllers» del DL380 Gen10 | `[verificato: QuickSpecs §Storage Controllers]` |
| Non supportato sui modelli «DL380 Gen10 8SFF BC CTO» (P56969-B21, P56970-B21) | `[verificato: QuickSpecs]` |
| «Smart Array controllers only support Smart Carrier drives» | `[verificato: QuickSpecs]` |
| RAID 0, 1, 5, 10; 2 porte interne Mini-SAS x4; PCIe 3.0 x8; «Mixed Mode» (RAID e HBA insieme) | `[voce di terzi: CDW, HPE China product page, Express Computer Systems]` |
| Il server ha già il controller software S100i (SATA) per 12 dischi | `[verificato: QuickSpecs, «All models come with the S100i Smart Array Controller»]` |
| Gabbie possibili: 8, 16 o 24 SFF, 8 o 12 LFF, NVMe con gabbie e riser dedicati; **l'NVMe nei bay richiede anche il fan kit 867810-B21** | `[verificato: QuickSpecs §Optional Features]` |
| Il server alza le ventole quando non legge la temperatura di dischi o schede di terze parti | `[voce di terzi: industrialmonitordirect.com, blog non ufficiale]` |
| I cavi tra controller e backplane dipendono dalla gabbia installata | `[non verificato: codici non cercati]` |

**Scelta consigliata**:
- **Mai un disco solo.** Minimo **2 SSD SATA/SAS enterprise con protezione da perdita di alimentazione (PLP)** in mirror, per Proxmox e le VM.
- **L'E208i-p in modalità HBA** e il mirror fatto da **ZFS** in Proxmox, perché ZFS vuole vedere i dischi direttamente e l'E208i-p non ha cache da sfruttare. In alternativa RAID 1 sull'E208i-p e LVM-thin `[non verificato: prassi Proxmox]`.
- I dischi vanno montati nei **carrier HPE SmartCarrier** (anche usati), per non avere problemi di lettura delle temperature.
- Per un disco NVMe senza gabbia NVMe si può usare un adattatore PCIe M.2 in uno slot x8 libero. Con 1 CPU però gli slot sono 3: GPU nello slot 2, E208i-p e adattatore negli slot 1 e 3 `[non verificato: compatibilità di boot da NVMe su adattatore]`.

### 2.6 iLO 5: gestione da remoto

- Il server ha un chip iLO 5 e una porta iLO dedicata, e sul frontale una porta di servizio iLO `[verificato: QuickSpecs §Overview, §Server Management]`.
- La licenza **iLO Advanced** aggiunge «the full integrated remote console», i media virtuali da GUI e script e le funzioni avanzate di sicurezza e alimentazione `[verificato: QuickSpecs §HPE iLO Advanced]`. Senza licenza la console remota grafica è limitata `[non verificato: quanto]`. Prezzo della licenza: non cercato.
- **Regole**: la porta iLO va sulla rete di gestione (§4.2), mai su internet; la password di fabbrica (sull'etichetta) va cambiata subito; il firmware va aggiornato prima della messa in produzione `[non verificato: prassi]`.
- Gli aggiornamenti completi (Service Pack for ProLiant) potrebbero richiedere un contratto di assistenza HPE attivo: **non verificato**, non trovato nelle fonti.
- Fine vita: Park Place Technologies indica per il DL380 G10 la fine del servizio il **31-mar-2028** `[voce di terzi: parkplacetechnologies.com/eosl/hpe/proliant-dl380-g10]`. Le date ufficiali HPE: non trovate.

---

## 3. Consumo, calore, rumore, collocazione

### 3.1 Consumi e costo della corrente

| Fonte | Valore | Etichetta |
|---|---|---|
| SPECpower, DL380 Gen10, 2 × Xeon Platinum 8180, 96 GB, configurazione ottimizzata da HPE (2018) | 49,3 W in «active idle», circa 461 W a pieno carico | `[verificato: spec.org, risultato 2018-08-28, tramite ricerca]` |
| SPECpower, DL380 Gen10 Plus (2021) | 127-143 W in «active idle» | `[verificato: spec.org, tramite ricerca]` |
| Utenti in un forum (configurazione non precisata) | circa 85 W a riposo | `[voce di terzi: lemm.ee]` |
| **Stima per la nostra configurazione** (1-2 CPU, 10-12 moduli, GPU a riposo, ventole HP, 2-4 SSD) | **120-180 W a riposo, 350-550 W sotto carico** | `[non verificato: stima]` |
| Mini PC firewall | circa 10-15 W | `[non verificato: TDP CPU 15 W da technical.city e notebookcheck]` |

Costo, al prezzo indicativo di **0,32 €/kWh** tutto compreso. I comparatori riportano 0,332 €/kWh medi sul mercato libero (famiglie, imposte incluse) e ARERA 31,63 c€/kWh per la tutela del terzo trimestre 2026; un dato specifico per le PMI non è stato trovato `[voce di terzi: luce-gas.it, facile.it, risultati di ricerca 2026-10-24]`:

| Media 24/7 | kWh/anno | €/anno | €/mese |
|---|---|---|---|
| 120 W | 1.051 | 336 | 28 |
| 200 W | 1.752 | 561 | 47 |
| 300 W | 2.628 | 841 | 70 |
| mini PC 12 W | 105 | 34 | 3 |

`[calcolo]`. La misura vera si legge dal contatore dell'iLO dopo una settimana di lavoro normale.

### 3.2 Calore e temperatura

- Temperatura dell'aria in ingresso: **10-35 °C** standard. HPE avverte che le prestazioni possono calare **sopra i 30 °C** o con una ventola guasta. Umidità 8-90 % senza condensa `[verificato: QuickSpecs §Technical Specifications]`.
- Calore da smaltire: 200 W sono circa 680 BTU/h, 450 W circa 1.540 BTU/h `[calcolo: 1 W = 3,412 BTU/h]`.
- **D'estate in Sardegna** uno stanzino chiuso e non climatizzato supera facilmente i 30 °C `[non verificato]`. Con una GPU non qualificata conviene restare sotto i **25 °C in ingresso**: serve un locale climatizzato, oppure un ricambio d'aria forzato con l'uscita del calore verso l'esterno `[non verificato: inferenza dai limiti HPE per le GPU qualificate, 20-35 °C]`.

### 3.3 Rumore e collocazione

- HPE dichiara, a 23 °C e per le configurazioni standard: **LWAd 4,4-4,8 B** e **LpAm 31-37 dBA** nella posizione dell'astante, sia a riposo sia al lavoro, «Additional options may result in increased sound levels» `[verificato: QuickSpecs §Acoustic Noise]`.
- Valori in dB con GPU e ventole high performance: **non trovati**. Le testimonianze vanno da «abbastanza silenzioso quando non sta avviando» a ventole molto rumorose con schede non HPE `[voce di terzi: lemm.ee, community.hpe.com]`.
- **Scelta consigliata**: il server **non sta in un ufficio dove si lavora**. Va in uno stanzino o locale tecnico separato, ventilato o climatizzato, con la porta chiusa. All'avvio le ventole vanno al massimo per qualche decina di secondi `[non verificato]`.
- **Il rack 12U open frame a 4 montanti** è il formato giusto: un 2U da 15-25 kg su guide ha bisogno di 4 montanti. Peso del DL380 Gen10: **14,9-19,5 kg (SFF)**, **17,1-24,5 kg (LFF)**. Profondità: **67,94 cm (SFF)**, **73,02 cm (LFF)** `[verificato: QuickSpecs §System Unit]`. Da controllare sul rack comprato: profondità regolabile ad almeno 70-75 cm più lo spazio per i cavi, fori compatibili con le guide HPE «Easy Install» (quadri o tondi) e freni sulle ruote `[non verificato: la scheda del rack non è stata letta]`. Un open frame non riduce il rumore e non filtra la polvere: va bene solo in un locale tecnico.
- Ordine nel rack: **UPS in basso** (è il pezzo più pesante), server sopra, firewall e switch in alto. Il mini PC fanless non va messo nel flusso d'aria caldo che esce dal retro del server `[non verificato: prassi]`.

---

## 4. Rete

### 4.1 Il mini PC come firewall (OPNsense)

| Fatto | Etichetta |
|---|---|
| Pentium Gold 4417U: 2 core / 4 thread, 2,3 GHz fissi (nessun turbo), 14 nm, Kaby Lake Refresh, TDP 15 W | `[voce di terzi: technical.city, notebookcheck]` |
| Supporto AES-NI: **non confermato** dalle fonti trovate (ARK Intel non raggiunto) | `non trovato` |
| WireGuard su OPNsense 19.7: Core i5-6300U (2 core / 4 thread, simile al 4417U ma con turbo) **circa 720-810 Mbit/s**; Celeron J3160 circa 170 Mbit/s | `[verificato: thomas-krenn.com, wiki «OPNsense WireGuard Performance Tests»]` |
| N100 con 4 × i226-V: circa 1,1 Gbit/s in download e 770 Mbit/s in upload con WireGuard; il passaggio a FreeBSD 14 avrebbe raddoppiato le prestazioni | `[voce di terzi: forum.opnsense.org]` |
| Con alcuni firmware le i226-V hanno avuto cadute di collegamento | `[voce di terzi: computingforgeeks.com]` |

**Stima per il 4417U**: NAT e firewall senza IDS a 1 Gbit/s pieno; WireGuard tra 0,5 e 0,8 Gbit/s; con Suricata (IDS/IPS) attivo il throughput scende sensibilmente `[non verificato: inferenza dai dati sopra]`. WireGuard usa ChaCha20 e non ha bisogno di AES-NI; IPsec e OpenVPN invece ne approfittano `[non verificato]`. Le porte a 2,5G servono solo se la linea internet supera 1 Gbit/s. La scheda di rete del server, se è la FlexibleLOM 4 × 1GbE indicata nelle QuickSpecs, va comunque a 1 Gbit/s `[verificato: QuickSpecs, «Embedded 4 x 1GbE Network Adapter (if equipped)»]`.

**Scelta consigliata**: **OPNsense** (open source, gratuito, WireGuard incluso, plugin per l'UPS con NUT). Prima del ciclo di prova di 24 ore vanno aggiornati BIOS e firmware delle i226-V. La versione di OPNsense da installare è l'ultima stabile al momento dell'installazione (numero non verificato). Per pfSense i costi della versione Plus non sono stati verificati.

### 4.2 Segmentazione: porte dedicate al posto delle VLAN

Il mini PC ha 4 porte, quindi si può segmentare **senza comprare uno switch gestito**:

| Porta OPNsense | Rete | Cosa c'è | Regole |
|---|---|---|---|
| igc0 | **WAN** | modem/ONT del provider (meglio in bridge) | nessuna porta aperta in ingresso |
| igc1 | **LAN ufficio** | PC, Wi-Fi, stampanti | verso internet; verso i servizi del server solo sulle porte delle applicazioni |
| igc2 | **SERVER** | DL380 (una o più porte della FlexibleLOM; VLAN in trunk se servono più reti) | uscita verso internet limitata alle destinazioni necessarie; nessun accesso dalla LAN tranne quello previsto |
| igc3 | **GESTIONE** | iLO, interfaccia web di Proxmox, UPS di rete | raggiungibile solo dalla VPN degli amministratori |

`[non verificato: progetto consigliato]`. Se in futuro servono più dispositivi in una rete, si aggiunge uno switch gestito con le VLAN sulla porta interessata. Tra Proxmox (bridge VLAN-aware) e OPNsense si possono portare più VLAN su un solo cavo (es. «server-prod», «server-stage», «gpu») `[non verificato: configurazione standard]`.

**Una nota su SersanOutreach**: il worker LinkedIn usa Playwright; su Azure il traffico passa da IP e proxy cloud. Spostandolo in ufficio, le sessioni LinkedIn partiranno dall'IP pubblico dell'ufficio, a meno di non mantenere il proxy. Questo va deciso nel piano di migrazione `[non verificato: ricerca/01-sersanoutreach.md cita un proxy (IPRoyal) e un VPS WireGuard, ma non l'instradamento esatto]`.

### 4.3 Esporre i servizi su internet senza aprire porte

**Cosa deve essere pubblico** `[verificato: ricerca/01-sersanoutreach.md righe 14, 20, 121]`: `outreach.sersan.io` (l'estensione Chrome ha questo nome scritto nel manifest), i webhook di Instantly, e in futuro gli endpoint degli agenti (webhook di Fireflies, HubSpot, Slack, ecc.). Oggi l'ingresso è Traefik con Let's Encrypt su una VM Azure, il DNS è su Cloudflare, e gli strumenti interni sono raggiungibili solo via WireGuard.

**I webhook Instantly** si creano con un POST a `https://api.instantly.ai/api/v2/webhooks`; l'indirizzo va nel campo `target_hook_url`; un tipo di evento è `reply_received` `[verificato: developer.instantly.ai/guides/webhook-events, tramite ricerca]`. Il fatto che servano il piano Hypergrowth (97 $/mese) e che ci siano 3 tentativi in 30 secondi viene solo da pagine di terzi `[voce di terzi]`. Serve quindi un URL HTTPS pubblico e stabile.

| Opzione | Porte aperte | Dominio proprio (`outreach.sersan.io`) | Costo | Pro | Contro |
|---|---|---|---|---|---|
| **Cloudflare Tunnel** (`cloudflared` nel server) | nessuna, solo connessioni in uscita | **sì**, il DNS è già su Cloudflare | Zero Trust **gratis fino a 50 utenti**, poi 7 $/utente/mese; il connettore è incluso in tutti i piani | funziona anche dietro CGNAT o IP dinamico; si può mettere **Cloudflare Access** davanti alle pagine interne | Cloudflare termina il TLS e vede il traffico in chiaro (da citare nella valutazione GDPR); dipendenza da un fornitore |
| **Tailscale Funnel** | nessuna | **no**: solo nomi `*.ts.net`; porte 443, 8443, 10000; solo TLS | incluso in Tailscale (piano non verificato) | molto semplice | limiti di banda «non-configurable»; l'estensione Chrome andrebbe cambiata |
| **Reverse proxy Traefik/Caddy con porta 443 aperta** | 443 (e 80 per ACME) | sì | 0 € | come oggi su Azure, nessun intermediario | serve un IP pubblico statico, niente CGNAT; superficie d'attacco esposta; il firewall dell'ufficio diventa critico |
| **VPS ponte** (proxy pubblico più WireGuard verso l'ufficio) | nessuna in ufficio | sì | costo del VPS (non verificato) | il traffico non passa da Cloudflare | un server in più da mantenere |

`[verificato: docs Tailscale Funnel, tailscale.com/pricing; voce di terzi per i prezzi Cloudflare Zero Trust: zerotrustcost.com, cipherssecurity.com, zerometric.net; il resto non verificato]`

**Scelta consigliata**: **Cloudflare Tunnel** per tutto ciò che deve essere pubblico, con Traefik dentro il server che smista i nomi come oggi. Le pagine per il team (Grafana, pannelli degli agenti) vanno dietro **Cloudflare Access** (accesso con l'account Google Workspace o con un codice via email). I webhook restano pubblici ma con verifica della firma o di un segreto nell'applicazione. **Nessuna porta aperta** sul firewall dell'ufficio.

### 4.4 Accesso del team e degli amministratori

| Opzione | Costo | Nota |
|---|---|---|
| **WireGuard su OPNsense** | 0 € | SerSan lo usa già su Azure (allowlist `10.6.0.0/24`, `10.40.0.0/16`); per arrivare in ufficio serve un IP pubblico o una porta UDP aperta. Dietro CGNAT non funziona in ingresso `[verificato per l'uso attuale: ricerca/01 riga 121; il resto non verificato]` |
| **Tailscale Personal** | 0 €, fino a 6 utenti, dispositivi illimitati | che il piano sia ammesso per l'uso aziendale non è verificato `[verificato per i limiti: tailscale.com/pricing]` |
| **Tailscale Standard** | **8 $/utente/mese** (4 utenti = 32 $/mese) | sostituisce il vecchio piano Starter; funziona dietro CGNAT `[verificato: tailscale.com/pricing, 2026-10-24]` |
| **Cloudflare WARP / Access** | 0 € fino a 50 utenti | adatto alle applicazioni web; meno adatto a SSH e alla console di Proxmox `[voce di terzi]` |

**Scelta consigliata**: **WireGuard su OPNsense** se l'ufficio ha un IP pubblico (anche dinamico con DDNS). Se la linea è dietro CGNAT, **Tailscale Standard**, con un nodo nel server come subnet router verso la rete di gestione. L'interfaccia di Proxmox e l'iLO si raggiungono **solo** dalla VPN.

---

## 5. Sistema operativo, virtualizzazione, backup, UPS

### 5.1 Proxmox VE oppure Ubuntu con Docker

| | **Proxmox VE 9.x + VM/LXC** | **Ubuntu Server + Docker sul ferro** |
|---|---|---|
| Versione | PVE **9.2** (21-mag-2026, Debian 13.5, kernel 7.0); 9.0 di agosto 2025 `[verificato: comunicato proxmox.com e roadmap, tramite ricerca]` | Ubuntu LTS (versione non verificata) |
| Costo | 0 € con il repository no-subscription; **Community 120 €/socket/anno**, Basic 370 €, Standard 550 €, Premium 1.100 € (IVA esclusa) `[verificato: proxmox.com, pagina pricing]` | 0 € |
| Snapshot e ripristino | snapshot di VM intere, backup incrementali con PBS, ripristino di una VM in pochi minuti | solo backup dei volumi e della configurazione; un guasto del sistema vuol dire reinstallare |
| Separare prod, stage e agenti | VM diverse, risorse e reti separate | tutto nello stesso kernel e nello stesso Docker |
| GPU | passthrough a una VM, oppure driver sull'host e GPU condivisa con container LXC | diretta, con NVIDIA Container Toolkit: la via più semplice |
| ZFS | integrato, in mirror dall'installazione | possibile, ma a mano |
| Complessità | un livello in più da conoscere | minima |

**Rischio del passthrough su HPE.** Sui ProLiant più vecchi (ML350p, DL360 Gen9) Proxmox ha rifiutato il passthrough di alcune schede con l'errore «ineligible for IOMMU domain attach» (RMRR), legato al BIOS HPE. Per il Gen10 **non ho trovato prove né in un senso né nell'altro** `[voce di terzi: forum.proxmox.com]`. Se il passthrough fallisce, la soluzione di riserva è installare il driver NVIDIA sull'host Proxmox e dare la GPU a un **container LXC**, che non usa l'IOMMU `[non verificato: configurazione nota della community]`.

**Scelta consigliata: Proxmox VE 9.x** con:

| Macchina | Tipo | Contenuto | Risorse indicative |
|---|---|---|---|
| `apps-prod` | VM Ubuntu LTS | Docker Compose: SersanOutreach (8 servizi), Traefik, `cloudflared`, orchestratore degli agenti, code e cron | 8 vCPU, 32 GB |
| `apps-stage` | VM Ubuntu LTS | copia di prova | 4 vCPU, 12 GB |
| `gpu` | VM con passthrough (o LXC) | Ollama/llama.cpp, trascrizione, embedding | 4 vCPU, 16-24 GB, RTX 4000 |
| `data` | VM o LXC | Postgres con pgvector, se si decide di portare in casa il database o il vettoriale | 4 vCPU, 16-32 GB |
| `monitor` | LXC | Prometheus, Grafana, Loki, Alertmanager (oggi già usati) | 2 vCPU, 4-8 GB |
| `pbs` | VM, con dischi propri | Proxmox Backup Server, solo come primo livello | 2 vCPU, 4 GB |

`[non verificato: dimensionamento indicativo; SersanOutreach misura oggi 7,4 GiB di tetti di memoria, verificato in ricerca/01 riga 20]`. Con 128 GB restano più di 30 GB liberi.

**Database**: oggi SersanOutreach usa Supabase (Postgres 17.6, AWS eu-west-1, circa 35 ms a round trip da Azure) `[verificato: ricerca/01 riga 103]`. Se le applicazioni vanno in Sardegna e il database resta in Irlanda, la latenza va rimisurata (non trovata). È una scelta da fare nel piano di migrazione, non un vincolo dell'hardware.

### 5.2 Backup

- **Regola 3-2-1**: 3 copie, 2 supporti, 1 fuori sede `[non verificato: prassi]`.
- **Primo livello**: Proxmox Backup Server con backup incrementali e deduplicati delle VM, su **dischi diversi** da quelli delle VM. Meglio ancora su una macchina diversa, anche un vecchio PC `[non verificato: prassi]`. PBS 4.x è basato su Debian 13; la data dell'ultima versione stabile non è stata trovata `[voce di terzi]`.
- **Fuori sede**: sincronizzazione di PBS verso un PBS remoto, oppure **restic** (cifrato) verso uno storage a oggetti in cloud. Prezzi dei fornitori: non verificati.
- **Prova di ripristino** una volta al mese, scritta nel runbook. Oggi il backup di SersanOutreach sta su un solo disco della VM e la copia off-site su Azure non è attiva `[verificato: ricerca/01 riga 135]`: lo spostamento è l'occasione per correggere.

### 5.3 UPS e spegnimento ordinato

- Le interruzioni in Sardegna sono frequenti: nei comuni sotto i 5.000 abitanti serviti da E-Distribuzione, nel 2023, **91,66 minuti persi** per utente in bassa tensione per interruzioni lunghe senza preavviso e **8,29 interruzioni senza preavviso** (lunghe più brevi) per utente `[verificato: ARERA, «2023 ambiti territoriali bassa», riga Sardegna]`. Per una sede in città (media o alta concentrazione) i valori sono diversi e non li ho cercati. Anche un buco di un secondo spegne un server senza UPS.
- **Dimensionamento**: carico tipico 150-300 W, picco 550-700 W, più firewall e modem → **UPS da 1.500 VA / 1.000 W circa**, line-interactive o online, a **onda sinusoidale pura** (gli alimentatori Platinum con PFC attivo la preferiscono), formato rack 2U se possibile, con autonomia di 10-15 minuti al carico tipico. Modello e prezzo: non verificati.
- **Spegnimento ordinato con NUT**: l'UPS si collega in USB all'host Proxmox (server NUT). Dopo N minuti a batteria Proxmox spegne le VM in ordine (prima le applicazioni, poi il database, poi PBS) e infine sé stesso. OPNsense, con il plugin NUT come client, si spegne per ultimo. Nel BIOS va impostato «riaccendi al ritorno della corrente» `[non verificato: configurazione standard]`.
- Con due alimentatori, entrambi vanno sull'UPS, oppure uno sull'UPS e uno su un secondo UPS. Non uno sull'UPS e uno sulla rete: il primo buco farebbe cadere il carico tutto su un solo alimentatore e sull'UPS `[non verificato: prassi]`.

---

## 6. Rischi e contromisure

| Rischio | Probabilità | Impatto | Contromisura |
|---|---|---|---|
| Interruzioni di corrente (Sardegna: 8,29 l'anno per utente nei piccoli comuni, 2023) | alta | VM che si spengono di colpo, database corrotti | UPS con NUT (§5.3); ZFS; backup |
| Calore d'estate sopra i 30 °C in ingresso | media-alta | prestazioni ridotte, ventole al massimo, guasti | locale climatizzato o ventilato verso l'esterno; allarme dell'iLO sulla temperatura in ingresso |
| Un solo disco o un solo server | alta se non si interviene | perdita di dati, fermo di giorni | mirror ZFS; PBS più copia fuori sede; runbook di ripristino; per i servizi critici, possibilità di ripartire su una VM cloud dai backup |
| RAM non HPE e sbilanciata | media | messaggi di avviso nell'IML, prestazioni di memoria non uniformi | configurazione bilanciata (8 o 12 moduli); memtest di 24 h; 2 moduli di scorta |
| GPU non qualificata | media | ventole rumorose, temperature non viste dall'iLO, nessun supporto HPE | fan kit e dissipatori HP; firmware aggiornati; `nvidia-smi` nel monitoraggio |
| Cavo GPU di terze parti | bassa-media | danni a GPU o scheda madre | prova con il tester o cavo HPE P03849-B21 |
| Alimentatori sotto-dimensionati | media se sono da 500 W | spegnimenti sotto carico, nessuna ridondanza | 2 × 800 W; controllo dei consumi dall'iLO |
| Esposizione su internet | media | intrusioni | nessuna porta aperta; Cloudflare Tunnel e Access; iLO e Proxmox solo da VPN; aggiornamenti |
| Manutenzione affidata a una persona sola | alta | se Alberto non c'è, nessuno sa intervenire | runbook scritto; un secondo amministratore con accesso VPN e iLO; procedure provate |
| Ricambi e fine vita (EOSL secondo terzi: 31-mar-2028) | bassa-media | fermo in attesa dei pezzi | il mercato dell'usato DL380 Gen10 è ampio `[non verificato]`; a scorta un alimentatore, una ventola, un SSD e 2 moduli RAM |
| Linea internet unica | media | webhook persi e team senza accesso | i webhook di Instantly ritentano, ma per poco (secondo terzi); una linea di backup 4G/5G su OPNsense `[non verificato]` |
| Furto o danno fisico in ufficio | bassa | perdita dell'hardware e dei dati | locale chiuso a chiave; cifratura dei dischi (ZFS o LUKS) da valutare; copia fuori sede |

---

## 7. Checklist di messa in produzione in 10 passi

1. **Inventario e identificazione**: dall'iLO (porta dedicata, password di fabbrica cambiata subito) si leggono modello, CPU, alimentatori, ventole, gabbia dischi, FlexibleLOM e firmware. Si aggiornano System ROM, iLO 5 e Innovation Engine all'ultima versione disponibile.
2. **Hardware da completare**, in base al passo 1: fan kit 867810-B21 e dissipatori 826706-B21 se mancano; 2 alimentatori da 800 W; 2 SSD enterprise con PLP nei carrier SmartCarrier; il cavo GPU HPE P03849-B21, oppure la prova con il tester del cavo comprato; le guide del rack; 2 moduli RAM in più se le CPU sono due; l'UPS.
3. **Montaggio**: RAM in configurazione bilanciata (8 o 12 moduli, DIMM blank negli slot vuoti); GPU nello slot 2 del riser primario; E208i-p in uno slot x8 impostato in HBA; server nel rack su guide, UPS in basso, in un locale ventilato o climatizzato.
4. **Prove di 24-48 ore**: memtest86+ di 24 h; stress di CPU e GPU (`nvidia-smi` per le temperature) mentre si guardano ventole, temperatura in ingresso e consumo dall'iLO; controllo dell'IML. Si annotano i watt a riposo e sotto carico: sono i numeri veri per il costo della corrente.
5. **Firewall**: OPNsense sul mini PC, con BIOS e firmware aggiornati; quattro reti (WAN, LAN, SERVER, GESTIONE) come al §4.2; WireGuard (o Tailscale) per gli amministratori; NUT client; nessuna porta aperta verso l'interno.
6. **Proxmox VE 9.x**: installato su mirror ZFS dei 2 SSD; bridge VLAN-aware; interfaccia web raggiungibile solo dalla rete di gestione; repository impostato (no-subscription subito, Community a 120 €/socket/anno quando si va in produzione); NUT server collegato all'UPS, con la prova reale di un distacco della corrente.
7. **VM e GPU**: VM `apps-prod` e `apps-stage` con Ubuntu LTS e Docker; prova del passthrough della RTX 4000 alla VM `gpu`. Se compare l'errore RMRR, si passa al driver sull'host più LXC.
8. **Ingresso pubblico**: `cloudflared` nella VM delle applicazioni; in Cloudflare il nome `outreach.sersan.io` e i nomi dei webhook vanno sul tunnel; Cloudflare Access davanti alle pagine interne; i webhook di Instantly puntano al nuovo indirizzo e si prova un evento vero.
9. **Backup e monitoraggio**: PBS con piano giornaliero e conservazione dei backup; copia fuori sede (sync PBS o restic) e **prova di ripristino** di una VM intera; Prometheus, Grafana e Alertmanager (già in uso) estesi a host, iLO (Redfish o SNMP), UPS e GPU, con avvisi su Telegram come oggi.
10. **Passaggio in produzione e runbook**: migrazione di SersanOutreach da Azure con un periodo in parallelo; spegnimento della VM Azure solo dopo almeno una settimana stabile e un ripristino provato; runbook scritto (accessi, spegnimento e accensione, sostituzione di un disco, ripristino da backup, cosa fare se manca la corrente o la linea) e un secondo amministratore formato.

---

## 8. Costi aggiuntivi

| Voce | Tipo | Costo | Etichetta |
|---|---|---|---|
| Corrente del server | ricorrente | 28-70 €/mese (stima, a 0,32 €/kWh) | `[calcolo su stima]` |
| Corrente del mini PC | ricorrente | circa 3 €/mese | `[calcolo su stima]` |
| Proxmox VE Community | ricorrente, facoltativo | 120 €/socket/anno (240 € con 2 CPU), IVA esclusa | `[verificato: proxmox.com]` |
| Cloudflare Tunnel e Zero Trust | ricorrente | 0 € fino a 50 utenti | `[voce di terzi]` |
| Tailscale Standard (solo se serve) | ricorrente | 8 $/utente/mese, 32 $/mese per 4 persone | `[verificato: tailscale.com/pricing]` |
| 2 moduli RAM 16 GB (per arrivare a 12) | una tantum | circa 138 € al prezzo già pagato | `[calcolo]` |
| Fan kit 867810-B21, dissipatori 826706-B21, cavo P03849-B21, 2 alimentatori da 800 W, guide | una tantum, se mancano | non verificato | — |
| 2 SSD enterprise con PLP e carrier HPE | una tantum | non verificato | — |
| UPS 1.500 VA a onda sinusoidale | una tantum | non verificato | — |
| Licenza iLO Advanced (facoltativa) | una tantum | non verificato | — |
| Storage fuori sede per i backup | ricorrente | non verificato | — |

---

## 9. Verifiche tecniche ancora aperte

Sono verifiche di Alberto, non decisioni dei CEO:

- modello esatto, CPU, alimentatori, ventole, gabbia dischi e FlexibleLOM (passo 1);
- se la linea internet dell'ufficio ha un IP pubblico o è dietro CGNAT (decide tra WireGuard e Tailscale);
- dove si mette fisicamente il server e a che temperatura arriva quel locale d'estate;
- consumo reale dall'iLO dopo le prove;
- se il passthrough della GPU funziona sul Gen10 (rischio RMRR);
- se i moduli 2133 danno avvisi nell'IML;
- profondità e foratura del rack rispetto alle guide HPE.

---

## Fonti

Date di consultazione: tutte 2026-10-24.

**Ufficiali (produttore o ente)**
- HPE QuickSpecs DL380 Gen10, Version 58, 10-gen-2023, copia integrale ospitata da Bosch: https://assets.catalog.boschbuildingtechnologies.com/public/documents/QS_HPE_DL380G10_Special_enUS_42274285579.pdf. Indirizzo HPE originale, non raggiungibile oggi: https://www.hpe.com/psnow/doc/a00008180enw
- SPECpower_ssj2008, HPE ProLiant DL380 Gen10, 2018-08-28: https://www.spec.org/power_ssj2008/results/res2018q3/power_ssj2008-20180828-00850-power.html (letto tramite ricerca)
- Proxmox VE, prezzi degli abbonamenti: https://www.proxmox.com/en/products/proxmox-virtual-environment/pricing
- Proxmox VE 9.2, comunicato: https://proxmox.com/en/about/company-details/press-releases/proxmox-virtual-environment-9-2 (letto tramite ricerca); roadmap: https://pve.proxmox.com/wiki/Roadmap
- Tailscale, prezzi: https://tailscale.com/pricing; Funnel: https://tailscale.com/docs/features/tailscale-funnel
- Instantly, eventi webhook: https://developer.instantly.ai/guides/webhook-events (letto tramite ricerca)
- ARERA, continuità del servizio 2023, ambiti a bassa concentrazione: https://www.arera.it/fileadmin/allegati/dati/ele/2023_ambiti_territoriali_bassa_tab3_01.pdf
- Thomas-Krenn, OPNsense WireGuard Performance Tests: https://www.thomas-krenn.com/de/wiki/OPNsense_WireGuard_Performance_Tests

**Di terzi (rivenditori, forum, articoli)**
- Gigabyte, Quadro RTX 4000: https://www.gigabyte.com/ph/Professional-Graphics-Card/NVIDIA-QUADRO-RTX-4000-rev-10/sp; flopper.io: https://flopper.io/gpu/nvidia-quadro-rtx-4000-8gb
- Cavo GPU HPE P03849-B21: https://www.gekko-computer.de/en/p/HPE-DL38X-Gen10-2X-8-Pin-GPU-cable-kit-P03849-B21-NEW; https://www.serverschmiede.com/en/hp-25cm-dl380-gen10-gpu-power-cable-p04670-001-1x-8-pin-to-2x-8-pin-from-bundle-p03849-b21; 869820-001: https://expresscomputersystems.com/collections/hpe/products/869820-001
- E208i-p: https://cdw.com/product/hpe-smart-array-e208i-p-sr-gen10-storage-controller-raid-sata-6gb-s/4782873; https://www.hpe.com/cn/zh/product-catalog/compute/smart-array-controllers-and-smart-host-bus-adapters/pip.hpe-smart-array-e208i-p-sr-gen10-8-internal-lanes-no-cache-12g-sas-pcie-plug-in-controller.1010026918.html
- Ventole del DL380 Gen10 con schede aggiuntive: https://community.hpe.com/t5/proliant-servers-ml-dl-sl/high-fan-noise-dl380-gen10/td-p/7086328; https://community.hpe.com/t5/proliant-servers-ml-dl-sl/hp-dl380g10-nvidia-quadro-rtx4000/td-p/7162876 (403, solo estratti); https://industrialmonitordirect.com/blogs/knowledgebase/hp-dl380-gen10-nvme-ssd-fan-speed-compatibility-guide
- Consumi e rumore dagli utenti: https://lemm.ee/post/16004148
- Pentium 4417U: https://technical.city/en/cpu/Pentium-Gold-4417U; https://www.notebookcheck.net/Intel-Pentium-Gold-4417U-Processor-Kaby-Lake-Refresh-Benchmarks-and-Specs.433967.0.html
- WireGuard su N100 e i226-V: https://forum.opnsense.org/index.php?msg=197648; https://computingforgeeks.com/best-pfsense-opnsense-hardware/
- Cloudflare Zero Trust, prezzi: https://zerotrustcost.com/cloudflare-zero-trust-pricing; https://cipherssecurity.com/cloudflare-zero-trust-pricing-2026/; https://zerometric.net/research/cloudflare-zero-trust-free-plan-limits-2026/
- RMRR e passthrough su HPE: https://forum.proxmox.com/threads/pcie-pass-trough-in-a-hpe-ml350p-to-a-freenas-vm.70242/latest
- EOSL del DL380 G10: https://www.parkplacetechnologies.com/eosl/hpe/proliant-dl380-g10/
- Prezzo della corrente: https://luce-gas.it/guida/tariffe/kwh; https://www.facile.it/energia-luce-gas/tag/costo-kwh.html; https://www.pmi.it/economia/mercati/486775/prezzi-energia-2026-pun-psv-imprese.html

**Interne**
- `C:/Users/alber/SerSan-AgentOS/ricerca/01-sersanoutreach.md` (stack, ingresso, backup e database di SersanOutreach)
