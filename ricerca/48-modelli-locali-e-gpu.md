# 48. Modelli locali, multimodalità e GPU

- **Data**: 10 novembre 2026. Prezzi, schede dei modelli e documentazione sono stati letti oggi, salvo dove è scritta un'altra data.
- **Per chi**: Alberto e Michele.
- **Domande**: le due di Alberto del 10 novembre.
  1. Mettere sul server Whisper e altri modelli piccoli per compiti specifici, collegati a LiteLLM, oppure a OpenRouter per quelli che non ospitiamo.
  2. Servono modelli multimodali locali, perché le squadre lavorano con slide, video e audio. Serve un modello multimodale come orchestratore?
- **Aggiorna** [13-modelli-open-source-sul-server.md](13-modelli-open-source-sul-server.md), che è del 24 ottobre e ragiona su una sola GPU da 8 GB. Le parti su voce e trascrizione restano in [30](30-call-e-trascrizione-self-hosted.md) e [31](31-voce-andrea-self-hosted.md); quelle su hardware e montaggio in [32](32-hardware-e-upgrade.md) e [37](37-hardware-risposte-michele.md).
- **Non tratta** i giudici «System One» (Jev, OpenJev): hanno un rapporto a parte: [47](47-modelli-system-one.md).
- **Legenda**:
  - `[verificato: fonte, data]`: letto sulla fonte indicata;
  - `[non verificato: motivo]`: stima, calcolo mio o dato che la fonte primaria non conferma.
- **Cosa non ho fatto**: niente installazioni, niente processi accesi, nessuna misura sul server. Tutte le memorie e le velocità sul server sono stime da misurare.

### Parole usate spesso

- **VRAM**: la memoria della scheda grafica (GPU). Un modello deve starci dentro per andare veloce.
- **Quantizzazione**: i pesi del modello salvati con meno bit (per esempio 4 invece di 16). Il modello occupa circa un quarto, e perde un po' di qualità.
- **GGUF**: il formato dei file quantizzati che usa llama.cpp. **mmproj** è il file GGUF in più che dà la vista (o l'udito) a un modello linguistico.
- **MoE** («mixture of experts»): un modello grande che per ogni parola usa solo una parte dei pesi. Per esempio «35B-A3B» vuol dire 35 miliardi di parametri, di cui 3 attivi.
- **Contesto e cache**: il testo che il modello tiene in memoria mentre lavora. Anche la cache occupa VRAM.
- **WER**: la percentuale di parole sbagliate in una trascrizione. Più bassa è, meglio è.
- **Diarizzazione**: capire chi parla e quando.
- **Embedding**: un vettore di numeri che rappresenta un testo (o un'immagine) e serve per cercare per significato. Il **reranker** riordina i risultati della ricerca.
- **OCR**: leggere il testo dentro un'immagine o un PDF scansionato.
- **VLM** («vision-language model»): un modello linguistico che guarda immagini. Un modello **omni** ascolta anche l'audio e guarda i video.
- **Corsia N e corsia S**: le due corsie del motore ([45 §3](45-architettura-v3.md)). La N fa catene a schema senza strumenti; la S fa sessioni dell'Agent SDK che usano strumenti.

---

## In breve

1. **Whisper e i modelli piccoli: sì, e quasi tutti stanno già dietro LiteLLM.** Trascrizione, embedding, reranker e modelli piccoli parlano tutti l'API di OpenAI; LiteLLM li vede come gli altri modelli [verificato: docs.litellm.ai, provider vLLM, 10/11/2026].
2. **OpenRouter solo per i dati verdi e gialli,** con `data_collection: deny` e `zdr: true` [verificato: openrouter.ai/docs, 10/11/2026]. La regione UE costa un piano Business e non vale per tutti i modelli.
3. **Multimodalità: serve, come occhi e orecchie. Come orchestratore no: i fatti confermano la posizione di partenza, ma per ragioni diverse dalla durata dell'audio.** Lo smistamento nel nostro motore lo fa già il codice, sui metadati; l'unico smistatore libero, il Capo di gabinetto, è Claude, che vede già immagini e PDF [verificato: 45 §3.2; platform.claude.com/docs vision, 10/11/2026]. Esistono modelli aperti che capiscono audio lunghi: Qwen3-Omni fino a 40 minuti, Voxtral Mini 3B fino a 40 minuti [verificato: rapporto tecnico di Qwen3-Omni e scheda di Voxtral, 10/11/2026]. Ma la trascrizione serve comunque, per la memoria, la ricerca e il registro; gli specialisti trascrivono meglio; capire il tono non serve ed è vietato per le emozioni dall'AI Act [verificato: docs/03-architettura.md, Coach vendite]. Gemma 4 ascolta solo 30 secondi; Qwen3-Omni chiede 18,6 GB di pesi anche in Q4 [verificato: schede dei modelli, 10/11/2026].
4. **Il modello che vede serve davvero in pochi casi:** rivedere slide, grafiche e video dello Studio, leggere scansioni, capire schermate. Per i dati rossi lo fa in casa un Qwen3.5-9B; per il resto Claude via API. Video e audio vanno prima spezzati in fotogrammi e testo. Le fatture passive in XML dello SDI, se fattura un soggetto italiano, non hanno bisogno né di OCR né di vista [stima].
5. **GPU: la RTX PRO 2000 Blackwell da 16 GB resta la scelta giusta.** Oggi costa 1.100 €, sopra la soglia di 1.000 € di ADR-0014. Con lei e la RTX 4000 stanno trascrizione, voce, memoria, un modello piccolo e uno da 9B che vede, ma il 9B sugli 8 GB è al limite. La scheda da 24 GB a 70 W costa più di tre volte e oggi è in preordine [verificato: prezzi del §5.3]. Visto che Michele è disposto ad aggiornare, conviene anticiparla alla milestone 2: costa circa 100 € più della soglia e sblocca le prove che la RTX 4000, già piena, non può fare [stima].
6. **Da costruire subito, senza hardware:** il registro dei modelli con capacità, fornitore e colori dei dati ammessi. Nella milestone 2 si provano i modelli locali in italiano, con misure fissate prima. La RAM a 384 GB non va anticipata per i modelli, salvo che la prova scelga un MoE in RAM [stima].

---

## 1. I compiti, squadra per squadra

Per ogni squadra: cosa entra e cosa esce che non è testo, e se basta trasformarlo in testo all'ingresso. Le squadre e gli agenti sono quelli di [PRESENTAZIONE-CEO.md §4](../PRESENTAZIONE-CEO.md). Le valutazioni della colonna «Cosa serve» sono [stima] mie.

Tre modi di trattare un ingresso non testuale:
- **T, in testo**: lo trasforma un modello specializzato (trascrizione, OCR, lettura del documento). Poi lavora un modello di solo testo.
- **D, descrizione**: un modello che vede scrive una descrizione o dei campi. Poi lavora un modello di solo testo.
- **V, vista al centro**: il modello che decide deve guardare l'immagine. La descrizione non basta.

| Squadra | Ingressi non testuali | Uscite non testuali | Cosa serve |
|---|---|---|---|
| **Outbound** | allegati delle risposte (PDF, immagini), immagini dei post LinkedIn, schermate di profili | nessuna | **T** per gli allegati; **D** per le immagini dei post, raro |
| **Chiamate** | audio delle call dei clienti (bot sul nostro server); registrazioni dal vivo dal telefono; dettatura; slide condivise in call. Le call Teams nostre arrivano già trascritte da Microsoft [verificato: PRESENTAZIONE-CEO §4.2] | nessuna | **T**: trascrizione più diarizzazione. Le slide condivise: fotogrammi chiave e **D**, solo se servono |
| **Vendite** | PDF e deck dei clienti per il brief e le proposte; pagine web; la voce del cliente al telefono con «Andrea»; contratti firmati (scansioni) | la voce di Andrea; offerte e contratti in PDF | **T** per documenti e contratti. Andrea: trascrizione in streaming e voce sintetica, cioè **T** in tempo reale ([31](31-voce-andrea-self-hosted.md)). Il Coach lavora sulla trascrizione con i tempi di chi parla: basta **T** |
| **Marketing** | siti, annunci e video dei concorrenti; schermate di cruscotti; immagini nei commenti | nessuna | **D** per annunci e immagini; **T** per i video (audio e fotogrammi). Le metriche vanno lette dalle API, non dalle schermate |
| **Studio contenuti** | brand, template, foto, video grezzi | **slide, grafiche, video, caroselli** | La produzione la fanno i nostri template e gli strumenti esterni (Higgsfield, HyperFrames, After Effects). **Rivedere** quello che esce è un caso **V**: va guardato |
| **Progetti** | documenti e specifiche del cliente; schermate di errori e di interfacce; allegati Jira | report in PDF | **T** per i documenti; **V** per il controllo qualità delle interfacce e per le schermate degli errori |
| **Memoria** | tutto quello che entra: PDF, PPTX, DOCX, scansioni, immagini nelle mail, registrazioni | nessuna | **T** con Docling e OCR. Le immagini dentro i documenti: una **D** all'ingresso, così diventano cercabili |
| **Direzione** | allegati della posta (fatture, immagini) per lo Smistatore; interviste in chat | nessuna | **T** per gli allegati; il resto è testo |
| **Amministrazione** | fatture scansionate o in PDF dei fornitori; estratti conto | fatture in PDF | **T** con OCR, oppure **V** diretto: un modello che vede legge la fattura e scrive i campi a schema. Sono dati rossi: in casa |

**Cosa ne ricavo** [stima]:
- La maggior parte del lavoro è **T**: trascrivere, leggere documenti, fare OCR. Lo fanno modelli specializzati e piccoli.
- La **D** serve a poche figure e quasi sempre all'ingresso, una volta sola: poi la descrizione va in memoria.
- La **V** serve in quattro casi: rivedere slide, grafiche e video dello Studio; leggere fatture e scansioni con impaginazione difficile; controllare interfacce e schermate; capire una slide condivisa in call quando il testo non basta.
- Nessuna squadra ha bisogno di un modello che ascolti l'audio «come suona». Tono ed emozione non sono nei requisiti delle nove squadre; anzi, il Coach vendite non deve stimare le emozioni, perché l'AI Act lo vieta [verificato: docs/03-architettura.md e docs/05-design.md, regola 3].
- Le fatture passive: se a fatturare è un soggetto italiano, arrivano dallo SDI in XML strutturato, senza OCR. Chi fattura è ancora una domanda aperta [verificato: ADR-0013, «Restano aperti»]. La **V** sulle fatture serve solo per scansioni e PDF esteri.

---

## 2. I candidati open-weight oggi, compito per compito

Le dimensioni dei file sono quelle dei repository su Hugging Face. La memoria «in uso» aggiunge contesto e cache: la stimo io e va misurata con `nvidia-smi`. «Senza quantizzazione» vuol dire BF16 o FP16, cioè circa 2 GB per miliardo di parametri [non verificato: regola di calcolo].

Un vincolo vale per tutto: la **Quadro RTX 4000 è Turing**. Non ha BF16 né FlashAttention 2, e in vLLM alcuni modelli recenti non partono (Gemma 4) [verificato: 13 §0 punto 4]. Sulla RTX 4000 lo stack giusto resta llama.cpp. La RTX PRO 2000 Blackwell chiede CUDA 12.8 o successivo e programmi compilati per la sua architettura [verificato: 37 §4, «Seconda GPU»].

### 2a. Trascrizione e riconoscimento di chi parla

| Modello | Licenza | Dimensione e memoria | Italiano | Maturità | Stato |
|---|---|---|---|---|---|
| **Whisper large-v3-turbo** con faster-whisper | MIT | int8 dal vivo circa 2,1 GB; large-v2 int8 a lotti da 8 circa 4,5 GB | sì | molto alta: è il modello dal vivo di Vexa | [verificato: 30 §5.1 e §6.1] |
| **Parakeet TDT 0.6B v3** (NVIDIA) | CC-BY-4.0, uso commerciale ammesso | 0,6 miliardi; circa 2-3 GB in FP16 [non verificato]; gira anche su CPU in int8 | sì, 25 lingue; WER FLEURS 3,00 % (media) | alta | [verificato: 30 §5.1] |
| **Nemotron Labs Unified ASR 0.6B** (NVIDIA, 21/08/2026) | OpenMDW 1.1, uso commerciale | 0,6 miliardi; un solo modello per lotti e streaming | sì: WER italiano 4,33 % a contesto pieno, 5,86 % in streaming a 0,56 s (media FLEURS, MCV, MLS) | nuovo; la scheda elenca Ampere, Blackwell, Hopper e Volta, **non Turing** | [verificato: huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b, 10/11/2026] |
| Nemotron 3.5 ASR streaming 0.6B | OpenMDW 1.1 | 0,6 miliardi | sì; FLEURS 4,41 % a 560 ms | scelto per Andrea nella fase 2 | [verificato: 31 §5] |
| Qwen3-ASR 1.7B e 0.6B | Apache-2.0 | 1,7 e 0,6 miliardi; dal 26/06/2026 anche in formato Transformers | sì | lo streaming solo con vLLM; llama.cpp lo elenca fra i modelli audio | [verificato: 13 §5; huggingface.co/api/models?author=Qwen; github.com/ggml-org/llama.cpp docs/multimodal.md, 10/11/2026] |
| Voxtral Mini 4B Realtime | Apache-2.0 | pesi da circa 9 GB: una scheda da 16 GB da sola | sì | buono ma pesante | [verificato: 31 §5] |
| Voxtral Mini 3B (2507) | Apache-2.0 | circa 9,5 GB in BF16 | sì, fra 8 lingue | trascrive fino a 30 minuti e **risponde a domande sull'audio** fino a 40 minuti; llama.cpp lo elenca fra i modelli audio | [verificato: huggingface.co/mistralai/Voxtral-Mini-3B-2507; llama.cpp docs/multimodal.md, 10/11/2026] |
| **pyannote community-1** (chi parla) | CC-BY-4.0, si scarica dopo aver accettato i termini | circa 1-1,5 GB [non verificato] | indipendente dalla lingua | alta; errore AMI 17,0 % | [verificato: 30 §5.2] |

**Consigliati**:
- **Whisper large-v3-turbo** per il dal vivo, già pronto in Vexa e in Pipecat.
- **Parakeet v3 più pyannote** per i lotti dopo la call. Gira anche su CPU, quindi non dipende dalla GPU la sera.
- Da provare nella milestone 2, solo sulla scheda Blackwell: **Nemotron Labs Unified 0.6B**, perché un solo modello farebbe lotti e streaming, anche per Andrea.
- Nessuno è stato misurato su audio di SerSan. Le WER pubblicate sono su audio pulito; il telefono a 8 kHz andrà peggio [verificato: 31 §5].

### 2b. Embedding e reranker

| Modello | Licenza | Dimensione | Note | Stato |
|---|---|---|---|---|
| **Qwen3-Embedding-0.6B** | Apache-2.0 | 0,6 miliardi; 32k token | MMTEB 64,33, meglio di bge-m3 (59,56) | [verificato: 13 §7] |
| **Qwen3-Reranker-0.6B** | Apache-2.0 | 0,6 miliardi | gira su GPU o CPU | [verificato: 13 §7] |
| Embedding e reranker insieme in FP16 (Infinity) | — | circa 3 GB | è la configurazione del board | [non verificato: 31 §8.1] |
| **Qwen3-VL-Embedding-2B** e Qwen3-VL-Reranker-2B | Apache-2.0 | 2 miliardi; vettori da 2048 | cercano anche **immagini, schermate e video**, oltre al testo; oltre 30 lingue | [verificato: huggingface.co/Qwen/Qwen3-VL-Embedding-2B, via ricerca, 10/11/2026] |

**Consigliati**: restano **Qwen3-Embedding-0.6B e Qwen3-Reranker-0.6B** per il testo. **Qwen3-VL-Embedding-2B** è un'aggiunta per più avanti: servirebbe a cercare «la slide con il grafico dei costi» guardando le slide, non solo il loro testo [stima].

### 2c. Modelli linguistici per la corsia N

Due livelli: **piccoli** (2-5 miliardi) per oscurare, classificare, smistare; **medi** (9-14 miliardi) per estrarre e riassumere a schema in italiano. Quasi tutti i nuovi modelli sono anche **VLM**: vedono le immagini. Il modello medio della corsia N e il modello che vede possono quindi essere **lo stesso modello** [verificato per Qwen3.5-9B e Gemma 4: schede dei modelli].

| Modello | Licenza | File Q4 | Senza quantizzazione | Vede? | Note | Stato |
|---|---|---|---|---|---|---|
| Qwen3-4B (2025) | Apache-2.0 | Q5_K_M circa 3,5-4,2 GB in uso | circa 8 GB | no | è il modello del board, in Ollama | [verificato: 30 §6.1; memoria non verificata] |
| **Gemma 4 E4B** | Apache-2.0 | 5,15 GB più 0,99 GB per la vista e l'udito | — | sì: immagini, audio fino a 30 s, video fino a 60 s a 1 fotogramma al secondo | Tau2 42,2 %; contesto 128k | [verificato: huggingface.co/google/gemma-4-E4B-it-qat-q4_0-gguf; ai.google.dev model card, 10/11/2026] |
| **Qwen3.5-9B** (febbraio 2026) | Apache-2.0 | Q4_K_M 5,68 GB più 0,92 GB per la vista | 17,9 GB | sì: immagini e video | 201 lingue; OCRBench 89,2; OmniDocBench 1.5 87,7; strumenti supportati | [verificato: huggingface.co/Qwen/Qwen3.5-9B e unsloth/Qwen3.5-9B-GGUF, 10/11/2026] |
| **Gemma 4 12B** (maggio 2026) | Apache-2.0 | Q4_0 ufficiale 6,98 GB più 0,18 GB | circa 24 GB [non verificato: calcolo] | sì: immagini, audio fino a 30 s, video fino a 60 s | MMMLU 83,4 %; Tau2 69,0 %; contesto 256k | [verificato: huggingface.co/google/gemma-4-12B-it e la versione GGUF, 10/11/2026] |
| Ministral 3 8B e 14B | Apache-2.0 | — | — | — | non riletti oggi | [non verificato: 13 §2.1] |

Note:
- **Italiano**: nessuna di queste schede riporta una prova solo in italiano. La classifica italiana EVALITA-LLM esiste, ma non ho trovato i risultati di Qwen3.5 o Gemma 4 [verificato: ricerca del 10/11/2026, risultati non trovati]. La qualità in italiano va misurata da noi.
- **Risposte a schema**: llama.cpp impone lo schema JSON con una grammatica, quindi un JSON valido è garantito anche con un modello piccolo [verificato: 13 §2.3]. Se i campi sono **giusti** lo dice solo la prova.
- **Su Turing**: Qwen3.5 ha una cache più piccola, grazie all'architettura ibrida [verificato: 13 §2.2]. In vLLM sulla RTX 4000 Gemma 4 non parte [verificato: 13 §0]. In llama.cpp l'elenco dei modelli multimodali cita Gemma 4 E2B, E4B, 26B-A4B e 31B per la vista, e solo E2B ed E4B per l'audio: **il 12B non c'è** [verificato: docs/multimodal.md, 10/11/2026]. Qwen3.5 non compare in quell'elenco, ma i suoi GGUF hanno il file della vista: il supporto va provato [non verificato].
- **Il 9B negli 8 GB è al limite**: 5,68 GB di pesi, 0,92 GB per la vista, poi la cache, il codificatore delle immagini durante il calcolo e circa 0,3-0,5 GB del driver [verificato per i file: unsloth/Qwen3.5-9B-GGUF; il resto non verificato]. Sulla Turing va usato il file della vista in F16 (918 MB), non quello in BF16 [stima: Turing non ha BF16, 13 §0]. Se non sta: Q4_K_S (5,39 GB) o IQ4_XS (5,17 GB), oppure la vista calcolata in CPU [non verificato: da misurare].

**Consigliati**:
- **Piccolo**: resta **Qwen3-4B** per oscurare, classificare e smistare, già nel board. **Gemma 4 E4B** è il candidato per sostituirlo, se serve anche vedere un'immagine piccola.
- **Medio**: **Qwen3.5-9B**, perché sta negli 8 GB della RTX 4000 (circa 6,6 GB di file più il contesto [non verificato]), vede, e ha i punteggi di documento più alti fra i medi letti. **Gemma 4 12B** è la seconda prova: ascolta anche brevi audio, ma con il contesto non sta negli 8 GB, e llama.cpp non lo elenca ancora fra i modelli multimodali [stima; elenco verificato il 10/11/2026].

### 2d. Modelli che vedono e modelli «omni»

| Modello | Licenza | Memoria | Cosa fa | Limiti | Stato |
|---|---|---|---|---|---|
| **Qwen3.5-9B** | Apache-2.0 | circa 6,6 GB di file in Q4 | immagini e video; MMMU 78,4; VideoMME 78,4 senza sottotitoli | niente audio | [verificato: scheda HF, 10/11/2026] |
| **Qwen3.6-27B** (aprile 2026) | Apache-2.0 | Q4_K_M 16,8 GB; IQ4_XS 15,4 GB; più 0,93 GB per la vista | immagini e video; MMMU 82,9; VideoMME 87,7 con sottotitoli | serve una scheda da 24 GB da sola | [verificato: huggingface.co/Qwen/Qwen3.6-27B e la versione GGUF di unsloth, 10/11/2026] |
| **Qwen3.6-35B-A3B** (aprile 2026) | Apache-2.0 | Q4_K_M 22,1 GB; IQ4_XS 17,7 GB; Q3_K_M 16,6 GB | immagini e video; MMMU 81,7; OmniDocBench 1.5 89,9 | MoE: gli «esperti» possono stare in RAM, a velocità più bassa | [verificato: huggingface.co/Qwen/Qwen3.6-35B-A3B e la versione GGUF di unsloth, 10/11/2026] |
| Qwen3.8-27B (agosto 2026) | Apache-2.0 | circa 28 miliardi | immagini e video | come la 3.6-27B | [verificato: huggingface.co/Qwen/Qwen3.8-27B, 10/11/2026] |
| Gemma 4 26B-A4B | Apache-2.0 | Q4_0 14,4 GB più 1,19 GB | immagini e video | niente audio | [verificato: GGUF ufficiale e model card, 10/11/2026] |
| **Gemma 4 12B** e E4B (omni piccoli) | Apache-2.0 | vedi §2c | immagini, **audio fino a 30 secondi**, video fino a 60 secondi | i limiti di durata | [verificato: model card, 10/11/2026] |
| **Qwen3-Omni-30B-A3B** | Apache-2.0 | in BF16 con Transformers almeno **68,7-78,9 GB** per 15 secondi di video; in GGUF Q4_K_M **18,6 GB** più 1,33 GB per vista e udito | ascolta audio fino a 40 minuti, guarda video, risponde anche a voce; italiano fra le lingue parlate | MoE: in llama.cpp gli esperti possono stare in RAM; la voce in uscita in llama.cpp non è documentata | [verificato: huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct; huggingface.co/ggml-org/Qwen3-Omni-30B-A3B-Instruct-GGUF; llama.cpp docs/multimodal.md; arxiv.org/abs/2509.17765 per i 40 minuti, 10/11/2026] |
| MiniCPM-o 4.5 | — | circa 19 GB in BF16, circa 11 GB in int4 secondo una copia della scheda | omni da 9 miliardi, video e audio in streaming | licenza non riletta | [non verificato: copie della scheda, non la scheda originale] |
| Qwen3.5-Omni (marzo 2026) | — | — | omni | fra i modelli pubblicati da Qwen su Hugging Face **non c'è** | [verificato: huggingface.co/api/models?author=Qwen, 10/11/2026] |

**Consigliati**:
- **In casa, subito provabile**: **Qwen3.5-9B** sulla RTX 4000.
- **In casa, se la prova lo chiede**: **Qwen3.6-35B-A3B** con gli esperti in RAM per i lavori notturni sui dati rossi, oppure **Qwen3.6-27B** su una scheda da 24 GB.
- **Omni**: nessuno da mettere in produzione. Gemma 4 E4B è utile per un audio breve, per esempio una nota vocale (il 12B non è ancora nell'elenco di llama.cpp). Qwen3-Omni non sta in VRAM su questo server; con llama.cpp e gli esperti in RAM si può provare, lento, come il MoE 35B-A3B [stima]. Resta un esperimento: non c'è un compito delle squadre che lo chieda (§1).

### 2e. Lettura dei documenti e OCR

| Strumento | Licenza | Dimensione | Cosa fa | Note | Stato |
|---|---|---|---|---|---|
| **Docling** | MIT (codice) | — | legge PDF, DOCX, **PPTX**, XLSX, HTML, immagini; anche audio e video con la trascrizione | è già nella pipeline di Michele | [verificato: github.com/docling-project/docling, 10/11/2026] |
| **granite-docling-258M** | Apache-2.0 | 0,26 miliardi | il VLM di Docling; scrive la struttura della pagina | inglese principale, **italiano non citato**; su schede senza BF16 (la T4, Turing come la nostra) va usato in FP32 | [verificato: huggingface.co/ibm-granite/granite-docling-258M, 10/11/2026] |
| **PaddleOCR-VL-1.5** (gennaio 2026) | Apache-2.0 | 0,9 miliardi | lettura del documento; OmniDocBench 1.5 **94,5** dichiarato | llama.cpp per la parte VLM dal 6/03/2026; esiste già la 1.6; italiano non citato | [verificato: huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5, 10/11/2026] |
| Qwen3.5-9B come lettore | Apache-2.0 | vedi §2c | legge l'immagine della pagina e scrive i campi a schema | OmniDocBench 1.5 87,7; OCRBench 89,2 | [verificato: scheda HF] |

Le cifre OmniDocBench delle schede non si confrontano tutte fra loro: Gemma riporta una distanza di modifica (più bassa è meglio), Qwen e Paddle un punteggio [verificato: le due schede].

**Consigliati**: **Docling** con il suo motore OCR per tutto quello che entra in memoria. **PaddleOCR-VL-1.5** come seconda prova per scansioni e tabelle difficili. Per le fatture dei fornitori, la prova confronta Docling più un modello di testo con **Qwen3.5-9B** che legge l'immagine e scrive i campi [stima].

### 2f. Voce sintetica

Niente di nuovo rispetto a [31 §6](31-voce-andrea-self-hosted.md):
- **Pocket TTS** (100 milioni di parametri, su CPU, voce italiana `giovanni`) per la fase 1 di Andrea;
- **Qwen3-TTS** (Apache-2.0; WER italiano 0,948 per il 1.7B) per la fase 2 sulla scheda Blackwell;
- **Chatterbox Multilingual** (MIT, con filigrana) come alternativa.

[verificato: 31 §6]. Nessuno ha misurato la qualità in italiano in casa [verificato: 31 §6.1].

### 2g. Generare immagini e video in casa

Non ha senso su questo server, per ora [stima]:
- **Video**: Wan 2.2 TI2V-5B (Apache-2.0) chiede almeno 24 GB per il 720p, e impiega circa 9 minuti per 5 secondi di video su una RTX 4090 [verificato: huggingface.co/Wan-AI/Wan2.2-TI2V-5B, via ricerca; tempi dal README citato da terzi]. Le nostre schede da 70 W sono molto più lente di una 4090 [stima].
- **Immagini**: Qwen-Image-2.1 (settembre 2026) ha 7 miliardi di parametri ed è sotto la «Qwen Research License», da rileggere per l'uso commerciale [verificato: huggingface.co/Qwen/Qwen-Image-2.1, 10/11/2026].
- Le grafiche e i video dello Studio non sono dati rossi. Lo Studio usa già Higgsfield, HyperFrames e After Effects [verificato: PRESENTAZIONE-CEO §4.5].

### 2h. Modelli locali che usano strumenti in catena (corsia S)

| Modello | Prove con strumenti dichiarate | Memoria | Stato |
|---|---|---|---|
| **Qwen3.6-35B-A3B** | TAU3-Bench 67,2; MCP-Atlas 62,8; MCPMark 37,0; Tool Decathlon 26,9 | IQ4_XS 17,7 GB; Q4_K_M 22,1 GB, più il contesto | [verificato: scheda HF e GGUF, 10/11/2026] |
| Gemma 4 26B-A4B | Tau2 68,2 % | 14,4 GB più 1,19 GB | [verificato: model card, 10/11/2026] |
| Gemma 4 12B | Tau2 69,0 % | circa 7,2 GB di file | [verificato: model card, 10/11/2026] |
| Qwen3.8-27B | ClawEval-MM 57,4 (strumenti con immagini) | circa 28 miliardi | [verificato: scheda HF, 10/11/2026] |

**Risposta**: **sulla carta sì**, Qwen3.6-35B-A3B. Sono prove dichiarate dal produttore. Non ho trovato un confronto con Claude 5.5 sulle stesse prove [non verificato]. Servono **circa 18-22 GB di pesi più il contesto**: oggi non sta in nessuna delle nostre schede. Ci sono due strade per provarlo:
- con gli esperti nella RAM, a circa 12-25 token al secondo stimati [non verificato: 13 §3.2];
- su una scheda da 24 GB, solo con la variante IQ4_XS.

Tecnicamente l'Agent SDK può parlare con un modello locale: llama.cpp ha un endpoint compatibile con l'API Messages di Anthropic da gennaio 2026 [verificato: huggingface.co/blog/ggml-org/anthropic-messages-api-in-llamacpp, 10/11/2026]. Però Anthropic non supporta Claude Code verso modelli non Claude [verificato: 26 §4.5]. Un utente riporta errori su `count_tokens` [non verificato: articolo di un utente]. Quindi la corsia S resta su Claude, come dice [45](45-architettura-v3.md). La prova in casa è un esperimento della milestone 2, non un piano.

---

## 3. Serve un orchestratore multimodale?

### 3.1 Le due strade a confronto

- **A. Un modello multimodale grande al centro**, che riceve tutto (audio, immagini, video, testo) e decide.
- **B. Uno smistatore piccolo sul testo e sui metadati**, più modelli specializzati che fanno da occhi e orecchie, e un modello che vede chiamato quando serve.

| Criterio | A, omni al centro | B, smistatore più specialisti | Fonte |
|---|---|---|---|
| **Qualità dell'ascolto** | Gemma 4 12B: WER FLEURS 6,9 % (media delle lingue); audio di 30 secondi al massimo. Qwen3-Omni e Voxtral Mini 3B capiscono fino a 40 minuti, ma una WER sull'italiano confrontabile non l'ho trovata | Parakeet v3: 3,00 % (media); Nemotron Unified: 4,33 % in italiano; nessun limite di durata a lotti | [verificato: schede dei modelli, 10/11/2026; confronto in italiano non verificato] |
| **Qualità della lettura dei documenti** | i VLM generalisti sono buoni (Qwen3.5-9B 87,7) | lo specialista da 0,9 miliardi dichiara 94,5 | [verificato: schede; metriche dichiarate dai produttori] |
| **Tempi** | il modello grande guarda tutto, anche quello che non serve | si trascrive una volta, poi si lavora sul testo; la vista solo dove serve | [stima] |
| **Memoria** | Qwen3-Omni: 69-79 GB in BF16 per 15 s di video; 18,6 GB più 1,33 GB in GGUF Q4_K_M | trascrizione 2-4,5 GB, lettura 1-2 GB, VLM medio 6,6-8 GB; si caricano a turno | [verificato per i file e per il BF16; il resto stima] |
| **Costo** | in VRAM servirebbe una scheda da 24 GB da sola, o più; con gli esperti in RAM gira lento sulle schede che abbiamo | entra nelle schede già scelte (§5) | [stima] |
| **Semplicità** | un solo modello; llama.cpp lo serve in GGUF, vLLM solo con un ramo dedicato | più servizi, ma ognuno con un'API standard dietro LiteLLM | [verificato: scheda di Qwen3-Omni e llama.cpp docs/multimodal.md; §4] |
| **Trascrizione per la memoria** | l'omni capisce l'audio, ma la trascrizione scritta serve comunque per la ricerca, il registro e le carte | la trascrizione è il prodotto principale | [stima] |
| **Sicurezza** | un modello che vede tutto e decide è più esposto a istruzioni nascoste in immagini e documenti | il codice sceglie passi e destinatari; il modello scrive a schema | [verificato: 45 §3.2, «La corsia N è la difesa più economica contro le iniezioni»] |

### 3.2 Verdetto

**I fatti confermano la posizione di partenza**, con due correzioni.

- **Lo smistamento non lo fa un modello.** Nella corsia N il codice sceglie passi e destinatari [verificato: 45 §3.1]. Cosa è l'ingresso (audio, PDF, immagine) e di che colore è lo dicono i metadati, non un modello. Un modello piccolo serve solo per classificare il testo, ed è già il Qwen3-4B. L'unico smistatore «libero» è il Capo di gabinetto, nella corsia S, su Claude [verificato: 45 §3.2]. Claude vede già immagini e PDF: l'orchestratore che Alberto cerca, in quella parte, è già multimodale; gli mancano solo audio e video diretti [verificato: platform.claude.com/docs vision, 10/11/2026].
- **Un omni al centro non porta niente che serva alle squadre.** Non è un limite di durata: Qwen3-Omni e Voxtral Mini 3B capiscono audio fino a 40 minuti [verificato: rapporto tecnico e scheda, 10/11/2026]. Il problema è un altro. La trascrizione scritta serve comunque, per la memoria e il registro; gli specialisti la fanno meglio e con meno memoria; il «come suona» non è richiesto e le emozioni sono vietate (§1). Qwen3-Omni in VRAM non sta, e Gemma 4 ascolta solo 30 secondi [verificato: schede].
- **Prima correzione: il modello che vede può essere lo stesso modello medio della corsia N.** Qwen3.5-9B e Gemma 4 sono già multimodali. Non serve un «modello della vista» separato da quello che estrae e riassume [verificato: schede; conseguenza stima].
- **Seconda correzione: la posizione sottovaluta un caso.** Quando il dato è rosso e la descrizione non basta (§3.3), il 9B in casa è l'unico modello che vede, e sugli 8 GB della RTX 4000 è al limite (§2c). Se la prova dice che il 9B sbaglia, non c'è un piano B in casa senza la scheda nuova o gli esperti in RAM. Questo è il vero rischio, non l'orchestratore [stima].
- **Dove la posizione rischia di sopravvalutare**: i casi **V** sui dati rossi sono pochi (scansioni, slide in call, interfacce dei clienti). Se la prova li conferma rari, il 9B che vede può restare spento e caricarsi a richiesta, invece di occupare la RTX 4000 tutto il giorno [stima].

### 3.3 Quando serve davvero un modello che vede al centro

| Caso | Perché la descrizione non basta | Chi lo fa meglio oggi |
|---|---|---|
| **Rivedere slide e grafiche dello Studio** (testo che esce dal riquadro, contrasto, logo, coerenza con il brand) | il difetto è visivo | **Claude via API** per il materiale pubblico e del marketing (verde): legge immagini fino a 2.576 px sul lato lungo sui modelli 4.7 e successivi, 600 immagini per richiesta [verificato: platform.claude.com/docs vision, 10/11/2026]. In casa Qwen3.5-9B, se la slide contiene dati di un cliente |
| **Rivedere un video prodotto** | ritmo, sottotitoli, inquadrature | **fotogrammi chiave più trascrizione**, poi Claude. La pagina della vista di Claude elenca solo formati di immagine, quindi niente video né audio diretti [verificato: platform.claude.com/docs vision]. In casa i VLM Qwen accettano video corti [verificato: schede] |
| **Fatture e scansioni con impaginazione difficile** (dati rossi) | tabelle, timbri, campi fuori posto | **in casa**: Docling e OCR, oppure Qwen3.5-9B che scrive i campi a schema. Da decidere con la prova. Le fatture XML dello SDI si leggono e basta (§1) |
| **Controllo qualità delle interfacce** (Progetti) | l'errore è dove sta un pulsante | Claude, che nella corsia S usa anche gli strumenti di navigazione [verificato: platform.claude.com/docs vision, sezione computer use]; in casa per i sistemi dei clienti |
| **Slide condivisa in una call** | il grafico non ha testo | fotogramma più Qwen3.5-9B in casa, perché è dato rosso |

Chi è più bravo fra Claude 5.5 e i Qwen sulle stesse immagini non l'ho trovato in una fonte [non verificato]. La regola pratica è quella dei colori dei dati: rosso in casa, verde e giallo dove la qualità è migliore. Per saperlo davvero si confronta nella prova della milestone 2 (§6).

---

## 4. Come si collegano

### 4.1 I servizi dietro LiteLLM

| Servizio | Motore | API che espone | Come lo vede LiteLLM | Stato |
|---|---|---|---|---|
| Modelli di testo e VLM in GGUF (Qwen3-4B, Qwen3.5-9B, Gemma 4) | **llama.cpp `llama-server`** sulla RTX 4000; Ollama per i prototipi | `/v1/chat/completions` con immagini; embedding e rerank; anche `/v1/messages` in formato Anthropic | modello `openai/…` con `api_base` del server locale | API multimodale compatibile OpenAI [verificato: llama.cpp docs/multimodal.md]; formato Anthropic [verificato: blog ggml-org]; configurazione LiteLLM [non verificato: da provare] |
| Modelli in formato Transformers sulla Blackwell (Qwen3-ASR, embedding, VLM) | **vLLM** 0.9 o successivo | `/v1/chat/completions`, `/v1/embeddings`, `/v1/audio/transcriptions`, video con `video_url` | prefisso `hosted_vllm/` più `api_base` | [verificato: docs.litellm.ai/docs/providers/vllm e docs.vllm.ai, 10/11/2026; versione minima: 37 §4] |
| Trascrizione con faster-whisper | **Speaches** (prima faster-whisper-server) | `/v1/audio/transcriptions`, anche in streaming | voce con `mode: audio_transcription` | API di Speaches [verificato: speaches-ai.github.io via ricerca]; `mode` [verificato: docs.litellm.ai audio_transcription]; il collegamento a un server locale non è documentato [non verificato] |
| Embedding e reranker | **Infinity**, come nel board | `/embeddings`, `/rerank` | modello di embedding | [verificato: board via 30 §6.1] |
| Claude | API Anthropic | `/v1/messages` | come oggi | [verificato: 26 §4] |

Note:
- Vexa e Pipecat vogliono un servizio di trascrizione compatibile con OpenAI [verificato: 30 §6.3]. Possono passare da LiteLLM, così trascrizioni e costi finiscono nello stesso registro [stima].
- La trascrizione dal vivo di Andrea **non** passa da LiteLLM: è un flusso continuo dentro Pipecat, sotto il secondo [verificato: 31 §7.2]. LiteLLM vede solo le richieste a Claude.
- Un processo per scheda e per ruolo, con versioni fissate e una coda con priorità, come in [13 §4](13-modelli-open-source-sul-server.md). Per caricare e scaricare i modelli a richiesta c'è llama-swap [non verificato: 13 §4].

### 4.2 Cosa passa da OpenRouter

- **Solo dati verdi e gialli**, come per tutti i fornitori terzi [verificato: 45, «Un modello per agente, anche open-weight»].
- In ogni richiesta: `provider: { "data_collection": "deny", "zdr": true }`. `deny` usa solo fornitori che non tengono i dati; `zdr` chiede quelli che non conservano prompt e risposte [verificato: openrouter.ai/docs, provider-selection e zdr, 10/11/2026]. Le stesse regole si fissano anche nelle impostazioni dell'account.
- **Regione UE**: `eu.openrouter.ai` tiene prompt e risposte in Europa, ma solo con i piani Business o Enterprise, e solo per i modelli abilitati. La Batch API ne è esclusa [verificato: openrouter.ai/docs in-region-routing e sovereign-ai, via ricerca, 10/11/2026]. Esempio: Qwen3.6-35B-A3B **non** è disponibile in regione UE [verificato: openrouter.ai/qwen/qwen3.6-35b-a3b, 10/11/2026].
- **Prezzi**: per Qwen3.6-35B-A3B si va da 0,012 $ a 0,25 $ per milione di token in ingresso e da 0,112 $ a 1,80 $ in uscita, secondo il fornitore [verificato: stessa pagina, 10/11/2026]. Haiku 5.5 costa 0,10 $ e 0,50 $ [verificato: 13 §0]. Il risparmio non è una ragione; OpenRouter serve solo per un modello che Claude non ha e che noi non ospitiamo [stima].
- **Cosa ci mandiamo**: poco. Per esempio un VLM grande per descrivere immagini pubbliche dei concorrenti, se la prova dice che il 9B in casa non basta [stima].

### 4.3 Il registro degli agenti dichiara le capacità dei modelli

LiteLLM ha già i campi giusti nel `model_info` di ogni modello: `supports_vision`, `supports_audio_input`, `supports_audio_output`, più `supports_function_calling` e `supports_response_schema`. Si leggono da `/model/info` [verificato: docs.litellm.ai, vision e audio, 10/11/2026]. Il nostro registro aggiunge quello che LiteLLM non sa: dove gira il modello e quali colori di dati può ricevere [proposta].

Esempio di voce del registro dei modelli [proposta]:

```yaml
modelli:
  - id: qwen35-9b-casa
    litellm: qwen35-9b            # nome del modello in LiteLLM
    fornitore: casa               # casa | anthropic | openrouter
    dove: rtx4000                 # scheda o servizio
    capacita: [testo, immagini, video_breve, schema_json]
    colori_ammessi: [rosso, giallo, verde]
    limiti: { contesto_token: 16384, lato_immagine_px: 1536 }
  - id: whisper-turbo-casa
    litellm: whisper-turbo
    fornitore: casa
    capacita: [audio_in_testo]
    colori_ammessi: [rosso, giallo, verde]
  - id: claude-sonnet
    litellm: claude-sonnet-5-5
    fornitore: anthropic
    capacita: [testo, immagini, pdf, strumenti, schema_json]
    colori_ammessi: [giallo, verde]   # il rosso solo dopo l'oscuramento
  - id: qwen36-35b-openrouter
    litellm: openrouter-qwen36-35b
    fornitore: openrouter
    capacita: [testo, immagini, strumenti]
    colori_ammessi: [verde]

agenti:
  - nome: Agente fatture e incassi
    modelli: [qwen35-9b-casa]     # in ordine di preferenza
```

**Come sceglie lo smistatore** [proposta], in codice, senza un modello:
1. Legge le parti dell'ingresso: testo, immagini, audio, video, PDF.
2. Calcola il colore dei dati (rosso, giallo, verde), come già fa il Cancello.
3. Fra i modelli dell'agente, in ordine, prende il primo che ha **tutte** le capacità richieste e ammette quel colore.
4. Se nessuno basta, trasforma l'ingresso: audio in testo con la trascrizione, PDF in testo con Docling, video in fotogrammi più trascrizione. Poi riprova.
5. Se ancora nessuno basta, si ferma e manda una carta al responsabile. Non manda mai un dato rosso fuori per «avere un modello che vede».
6. Ogni scelta va nel registro a sola aggiunta: modello, motivo, colore.

Le **capacità** stanno in un solo posto, il registro dei modelli. Il `model_info` di LiteLLM si genera da lì, così le due liste non si separano [proposta].

---

## 5. La GPU

### 5.1 Tre scenari di carico

Memoria in GB, stime da misurare con `nvidia-smi` [non verificato, salvo dove indicato].

| Servizio | Oggi | Con trascrizione, voce e modelli piccoli | Anche con un modello che vede e uno medio | Fonte |
|---|---|---|---|---|
| Qwen3-4B Q5_K_M con il contesto | 3,5-4,2 | 3,5-4,2 | 3,5-4,2 | 30 §6.1 |
| Embedding e reranker (Infinity) | circa 3 | circa 3 | circa 3 | 30 §6.1 |
| Docling e granite-docling, a picchi | 1-2 | 1-2 | 1-2 | [stima] |
| Whisper turbo int8 dal vivo | — | 2,1 | 2,1 | [verificato: 30 §6.1] |
| Parakeet v3 più pyannote a lotti | — | 3-4,5 (in coda) | 3-4,5 (in coda) | 30 §6.1 |
| Andrea: trascrizione in streaming più Qwen3-TTS 0.6B, una telefonata | — | circa 5 | circa 5 | 31 §8.3 |
| **Qwen3.5-9B Q4_K_M con la vista**, 16k di contesto: anche modello medio della corsia N | — | — | 7-8 (6,6 di file [verificato]) | [stima] |
| **Totale se tutto acceso** | **circa 7,5-9** | **circa 18-21** | **circa 25-29** | [stima] |
| **Totale senza i lotti in coda** | — | circa 14,6-16,3 | circa 21,6-24,3 | [stima] |

### 5.2 Come si dividono sulle schede

| Scenario | Solo RTX 4000 (8 GB) | RTX 4000 più 16 GB (RTX PRO 2000) | RTX 4000 più 24 GB |
|---|---|---|---|
| **Oggi** | sì, con meno di 1 GB libero [verificato: 30 §6.1] | sì, largo | sì, largo |
| **Trascrizione, voce, piccoli** | **no**: la trascrizione dal vivo entra solo spostando il reranker su CPU [verificato: 30 §6.1] | **sì**: Andrea, Whisper, embedding e 4B sulla 16 GB (13,6-14,3 GB [verificato: 32 §4.6, stima]); i lotti e Docling sulla RTX 4000 | sì, con margine |
| **Anche un 9B che vede** | — | **sì, al limite**: il 9B sulla RTX 4000 (7-8 GB su 8), lotti e Docling in coda o su CPU. Quando Michele presta la RTX 4000, il 9B si ferma: i lavori rossi aspettano, quelli verdi e gialli vanno a Claude | sì: il 9B sulla 24 GB insieme ai servizi (circa 21-22 GB), la RTX 4000 libera |
| **Anche un 27B o il MoE 35B-A3B** | no | no in VRAM; il MoE solo con gli esperti in RAM, di notte | solo il 27B in IQ4_XS o il MoE in IQ4_XS, **da soli** sulla scheda |

[stima, sulle cifre del §5.1]. Michele presta la RTX 4000 «poco, al massimo qualche ora a settimana» [verificato: 37 §1]: il limite dello scenario 3 con la 16 GB pesa poco.

### 5.3 Le schede che entrano davvero nel DL380 Gen10

**Dove**: il riser principale è pieno (RTX 4000 e controller dei dischi). La seconda scheda va nello slot 5 del riser secondario (connettore x16, collegamento PCIe 3.0 x8), con il kit 870548-B21 [verificato: 37 §1 e §4, «Riser»]. Il riser è PCIe 3.0: una scheda PCIe 5.0 x8 lavora a 3.0 x8. Per l'inferenza conta poco, perché i pesi si caricano una volta [non verificato: 37, deduzione]. HPE non qualifica nessuna Blackwell nel DL380 Gen10 e non supporta GPU di modelli diversi: le ventole vanno controllate con iLO dopo il montaggio [verificato: 37 §4, «Seconda GPU»].

**Classe da 70 W senza cavo** (alimentata dallo slot, due slot, mezza altezza, ventola propria):

| Scheda | Memoria e banda | 8B Q4 stimato | Prezzo di oggi | Stato |
|---|---|---|---|---|
| **RTX PRO 2000 Blackwell 16 GB** | 16 GB GDDR7, 288 GB/s | 36 token/s | **1.100 €** su Amazon.it (versione Lenovo); mediana 12 mesi 984 €; minimo 12 mesi 740 €; mediana 3 mesi 1.246 € | [verificato: gpuprix.com/italy, aggiornato il 9/11/2026, letto il 10/11/2026]; velocità [non verificato: 32 §4.6] |
| RTX 4000 SFF Ada 20 GB | 20 GB GDDR6, 280 GB/s | 35 token/s | 2.165 € su Amazon.de | [verificato: gpuprix.com/eu/workstation, pagina senza data, letta il 10/11/2026] |
| **RTX PRO 4000 Blackwell SFF 24 GB** | 24 GB GDDR7, 432 GB/s, 70 W | 54 token/s | **£3.139,49 IVA inclusa** da Scan UK, in preordine a 7-9 settimane (circa 3.750 € [non verificato: cambio di ottobre]); 4.088,95 € da LDLC Italia, versione OEM venduta solo dentro un sistema | [verificato: scan.co.uk e ldlc.com, 10/11/2026]; velocità [non verificato: 32 §4.6] |

Il prezzo della 24 GB nelle pagine lette va da circa 3,4 a 3,7 volte quello della 16 GB [non verificato: calcolo su 3.750-4.089 € contro 1.100 €]. Ottobre dava 3.032,85 € di listino SHI [verificato: 32 §4.3].

**Schede più grandi, con cavo** (oltre i 75 W dello slot):

| Scheda | Memoria | Consumo e cavo | Prezzo | Stato |
|---|---|---|---|---|
| RTX PRO 4000 Blackwell (non SFF) | 24 GB GDDR7 | 140 W, **1 slot**, connettore a 16 pin | 2.555 € da MediaWorld; 3.828,83 € IVA inclusa da Ibertronica | [verificato: gpuprix.com/italy, 9/11/2026; ibertronica.es, 10/11/2026] |
| RTX A5000 | 24 GB GDDR6, 768 GB/s | 230 W, 2 slot, 8 pin | 2.438 € su Amazon.fr | [verificato: gpuprix.com/eu/workstation, senza data, 10/11/2026]; specifiche [non verificato: 13 §9] |
| RTX PRO 4500 Blackwell | 32 GB, 896 GB/s | 200 W, 2 slot, lunghezza piena | 4.641 € da MediaWorld | [verificato: gpuprix.com/eu/workstation, 10/11/2026]; specifiche [verificato: datasheet PNY via ricerca] |

**Cosa serve per una scheda con cavo nel DL380** [verificato dove indicato]:
- **Il cavo**: i riser GPU hanno un connettore per il cavo di alimentazione della scheda [verificato: 37 riser-7]. Il codice del kit per il riser secondario va cercato: [non verificato]. Per il connettore a 16 pin serve un adattatore dai connettori HPE [non verificato].
- **Gli alimentatori**: il picco stimato in corrente continua con la RTX 4000 e una scheda da 70 W è già di 768-798 W, al limite di un solo alimentatore da 800 W [verificato: 37 ups-26, stima]. Una scheda da 140-230 W al posto di quella da 70 W porta il picco a circa 840-960 W: **un solo alimentatore non basta più** e si perde la ridondanza [non verificato: calcolo].
- **La soluzione HPE**: due alimentatori da 1600 W (830272-B21), perché HPE non ammette alimentatori diversi [verificato: 32 §5.4]. Un rivenditore belga lo elenca a 183,24 € IVA esclusa l'uno [non verificato: pagina non aperta]. In alternativa, un tetto di potenza con `nvidia-smi -pl` [verificato: 32 §5.4].
- **L'UPS** regge 1100 W; con la scheda da 70 W il picco totale è già stimato a 860-945 W [verificato: 37 ups-27, stima]. Una scheda da 230 W lo porta oltre i 1000 W [non verificato: calcolo].
- **Un'alternativa pulita**: **sostituire** la RTX 4000 (160 W) con una RTX PRO 4000 Blackwell da 140 W, 24 GB, 1 slot, nello stesso slot 2. Il consumo scende di 20 W e la memoria triplica. Serve l'adattatore a 16 pin [non verificato]. Costa 2.555 € [verificato: gpuprix, 9/11/2026], meno quello che si ricava dalla RTX 4000 usata (circa 350 € il prezzo più basso dell'usato su Amazon.nl [verificato: gpuprix.com/eu/workstation, senza data]).

### 5.4 La GPU grande nel secondo nodo di dicembre

Il nodo 2 arriva a dicembre, fino a 1.500 €, con circa 150 W previsti, sul gruppo 2 dell'UPS [verificato: 37 §2].

- **A favore**: niente limiti di riser, alimentatori HPE e flusso d'aria; ci stanno anche schede da tavolo; il DL380 non perde la ridondanza [stima].
- **Contro**:
  - Il budget non basta. Una scheda da 24 GB costa da sola più di 1.500 €: per esempio la RTX 3090 nuova parte da circa 1.990 € in Europa [verificato: gpuprix.com/eu, 16/09/2026, via ricerca]. Una Intel Arc Pro B60 da 24 GB costa 896 € [verificato: gpuprix.com/eu/workstation, senza data], ma lo stack software Intel è meno provato [non verificato].
  - L'UPS: una scheda da 300-350 W sul nodo 2, sommata al picco del DL380, supera i 1100 W [non verificato: calcolo].
  - I dati rossi viaggiano fra i due nodi sul collegamento a 10 Gbit: va bene, restano in sede [verificato: 37 §2 per il collegamento].
- **Quando ha senso**: solo se la prova della milestone 2 dice che per i dati rossi serve un 27B o il MoE in VRAM. Allora conviene un nodo pensato per la GPU, con il suo budget e il suo UPS, non dentro i 1.500 € [stima].

### 5.5 Raccomandazione per Michele

| Cosa | Quando | Costo | Cosa sblocca |
|---|---|---|---|
| **Nessun acquisto per la milestone 1** | ora | 0 € | il registro dei modelli e le prove con modelli finti (§6.1); sulla RTX 4000, in una finestra, le prime prove di 4B, Qwen3.5-9B con la vista, Gemma 4 E4B, Whisper; Parakeet su CPU |
| **RTX PRO 2000 Blackwell 16 GB**, come in [ADR-0014](../docs/adr/0014-seconda-gpu-blackwell.md) | ADR-0014 dice: quando torna sotto i 1.000 € IVA inclusa, dalla fase 3; prima se Andrea viene anticipato. **Proposta nuova**: comprarla per la milestone 2, anche a 1.100 €, perché Michele il 10/11 si è detto disposto ad aggiornare e la prova dei modelli locali ne ha bisogno (Nemotron Unified, vLLM, Qwen3-TTS, e una RTX 4000 libera per il 9B) [stima] | 1.100 € oggi più riser (75-160 €) se manca [verificato: 37 §3] | trascrizione dal vivo, voce di Andrea, memoria e 4B insieme, giorno e notte; la RTX 4000 resta al 9B che vede |
| **Non comprare ora la 24 GB da 70 W** | si rivede dopo la prova della milestone 2 | oggi circa 3.750-4.100 € | solo un modello medio in più sempre acceso; non vale più di tre volte il prezzo [stima] |
| **Scheda grande con cavo nel DL380** | sconsigliata | 2.438-4.641 € più alimentatori | la ridondanza degli alimentatori e il margine dell'UPS si perdono [stima] |
| **Sostituire la RTX 4000 con una 24 GB da 140 W** | solo se la prova chiede un 27B in casa e il nodo GPU non si fa | circa 2.200 € netti di differenza [non verificato: 2.555 € meno 350 €] | un 27B o il MoE in IQ4_XS in VRAM, senza toccare alimentatori e UPS |

**La RAM a 384 GB** ([ADR-0015](../docs/adr/0015-ram-384-gb.md)): **non va anticipata per i modelli**. Resta la regola di [45 §11](45-architettura-v3.md): all'inizio della fase 3, o prima se il margine misurato scende sotto i 5 GB [verificato: 45 §11]. C'è un'eccezione: se la prova sceglie il MoE 35B-A3B con gli esperti in RAM per i lavori notturni, servono circa 20 GB in più [verificato: 32 §3.3]. Con i 35 GB liberi dell'avvio della fase F4 ci stanno, ma il margine finisce [non verificato: 32 §3.4]. In quel caso conviene comprarla prima della fase 3. I prezzi della DDR4 non promettono di scendere [verificato: 32 §2.4].

---

## 6. Cosa costruire

### 6.1 Milestone 1: il registro dei modelli, senza hardware

- **Registro dei modelli** (§4.3): `config/modelli.yaml` con id, nome in LiteLLM, fornitore, scheda, capacità, colori ammessi e limiti. Ogni agente elenca i suoi modelli in ordine [proposta, in linea con [ADR-0025](../docs/adr/0025-un-modello-per-agente.md)].
- **Scelta del modello nel codice**: le parti dell'ingresso più il colore danno le capacità richieste; poi si prende il primo modello che le ha [proposta].
- **Trasformazioni come passi della catena N**: «audio in testo», «documento in testo», «video in fotogrammi più testo». Ognuna è un passo con la sua chiave d'idempotenza, come gli altri [proposta, coerente con 45 §3.1].
- **Prove, gratis, con modelli finti**:
  1. un ingresso con un'immagine va solo a un modello con `immagini`;
  2. un dato rosso non va mai a `openrouter` né ad `anthropic` senza oscuramento;
  3. senza un modello adatto si trasforma l'ingresso o esce una carta, mai un errore muto;
  4. il `model_info` di LiteLLM generato dal registro coincide con il registro.
- **Stima**: circa 1-1,5 gp dentro la milestone 1 [stima].

### 6.2 Milestone 2: la prova dei modelli locali

Va accanto alle prove con LiteLLM già previste da [45 §12.2](45-architettura-v3.md). Le misure si fissano **prima** della prova; ogni risposta locale si confronta con Haiku 5.5 o Sonnet 5.5 sugli stessi casi verdi [proposta].

| Prova | Modelli | Dati | Misura | Soglia per passare |
|---|---|---|---|---|
| Trascrizione | Whisper turbo, Parakeet v3 (CPU e GPU), Nemotron Unified (solo Blackwell) | 10-20 call vere con consenso, accento sardo, inglese dei clienti, telefono a 8 kHz | WER, tempo per ora di audio, VRAM | da fissare con Alessandro [proposta] |
| Chi parla | pyannote community-1 | 5 riunioni dal vivo | errore di diarizzazione | come sopra |
| Corsia N a schema | Qwen3-4B, Gemma 4 E4B, Qwen3.5-9B | 50 trascrizioni per il post-call; 50 mail per lo Smistatore | JSON valido; campi giusti contro una persona; riassunti votati alla cieca contro Haiku 5.5 | per esempio 90 % dei campi giusti [proposta] |
| Lettura documenti | Docling, PaddleOCR-VL-1.5, Qwen3.5-9B | 30 fatture di fornitori, 20 PDF e PPTX dei clienti | campi giusti (importo, data, partita IVA), tabelle | come sopra |
| Revisione visiva | Qwen3.5-9B in casa, Claude via API | 20 slide e 10 grafiche dello Studio con difetti inseriti apposta | difetti trovati, falsi allarmi | almeno quanto una persona su difetti evidenti [proposta] |
| Strumenti in catena (esperimento) | Qwen3.6-35B-A3B con gli esperti in RAM | 10 compiti della corsia S su dati di prova | compiti finiti senza errori, token al secondo | nessuna: decide solo se riparlarne |
| Velocità e memoria | tutti | — | `llama-bench`, `nvidia-smi`, carico con 4 utenti | sostituisce le stime del §5 |

La prova gira sulla RTX 4000. Attenzione: oggi la RTX 4000 ha meno di 1 GB libero con i servizi del board [verificato: 30 §6.1]. Per provare il 9B (7-8 GB) bisogna fermare 4B, embedding e reranker, o spostarli su CPU, in una finestra concordata con Michele; oppure avere già la Blackwell. Quello che chiede la Blackwell (Nemotron Unified, vLLM, Qwen3-TTS) si prova appena c'è la scheda [stima].

### 6.3 Più avanti

- **Con la RTX PRO 2000**: la trascrizione e Andrea si spostano sulla nuova scheda; si prova Qwen3-TTS per la voce, con la prova d'ascolto di [31 §6.1](31-voce-andrea-self-hosted.md).
- **Memoria che vede**: descrizioni delle immagini all'ingresso con il 9B; Qwen3-VL-Embedding-2B se la ricerca sulle slide lo chiede [stima].
- **Revisione automatica dello Studio**: una catena che esporta ogni slide in PNG, la fa guardare a Claude (verde) o al 9B (rosso) e scrive i difetti nella carta di approvazione [proposta].
- **Decisione sulla scheda da 24 GB o sul nodo GPU**: dopo la prova, con i numeri veri [stima].
- **Rileggere** fra tre mesi gli omni: Qwen3.5-Omni non ha pesi pubblici oggi; Gemma ha allungato la finestra audio? [stima].

---

## Fonti

File della repo (letti il 10/11/2026):
- [13-modelli-open-source-sul-server.md](13-modelli-open-source-sul-server.md), per intero
- [30-call-e-trascrizione-self-hosted.md](30-call-e-trascrizione-self-hosted.md) §5-6
- [31-voce-andrea-self-hosted.md](31-voce-andrea-self-hosted.md) §5-8
- [32-hardware-e-upgrade.md](32-hardware-e-upgrade.md) §2-5
- [37-hardware-risposte-michele.md](37-hardware-risposte-michele.md) §1-3 e §4 (riser, UPS, seconda GPU)
- [26-claude-agent-sdk.md](26-claude-agent-sdk.md) §4
- [45-architettura-v3.md](45-architettura-v3.md), decisione del 10/11, §3, §11, §12
- [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md) §4
- [docs/03-architettura.md](../docs/03-architettura.md) e [docs/05-design.md](../docs/05-design.md), regole sul Coach vendite e l'AI Act; [ADR-0013](../docs/adr/0013-postiz-listmonk-docuseal.md), chi fattura
- [ADR-0014](../docs/adr/0014-seconda-gpu-blackwell.md), [ADR-0015](../docs/adr/0015-ram-384-gb.md), [ADR-0025](../docs/adr/0025-un-modello-per-agente.md)

Pagine web, lette il 10/11/2026:
- Qwen3.5-9B: https://huggingface.co/Qwen/Qwen3.5-9B ; GGUF: https://huggingface.co/unsloth/Qwen3.5-9B-GGUF
- Qwen3.6-35B-A3B: https://huggingface.co/Qwen/Qwen3.6-35B-A3B ; GGUF: https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF
- Qwen3.6-27B: https://huggingface.co/Qwen/Qwen3.6-27B ; GGUF: https://huggingface.co/unsloth/Qwen3.6-27B-GGUF
- Qwen3.8-27B: https://huggingface.co/Qwen/Qwen3.8-27B
- Elenco dei modelli Qwen: https://huggingface.co/api/models?author=Qwen&sort=createdAt&direction=-1
- Qwen3-Omni-30B-A3B: https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct ; GGUF ufficiale: https://huggingface.co/ggml-org/Qwen3-Omni-30B-A3B-Instruct-GGUF ; rapporto tecnico (40 minuti di audio, via ricerca): https://arxiv.org/abs/2509.17765
- Voxtral Mini 3B: https://huggingface.co/mistralai/Voxtral-Mini-3B-2507
- Qwen3-VL-Embedding-2B (via ricerca): https://huggingface.co/Qwen/Qwen3-VL-Embedding-2B
- Qwen-Image-2.1: https://huggingface.co/Qwen/Qwen-Image-2.1
- Gemma 4, model card: https://ai.google.dev/gemma/docs/core/model_card_4
- Gemma 4 12B: https://huggingface.co/google/gemma-4-12B-it ; GGUF: https://huggingface.co/google/gemma-4-12B-it-qat-q4_0-gguf
- Gemma 4 E4B e 26B-A4B, GGUF: https://huggingface.co/google/gemma-4-E4B-it-qat-q4_0-gguf ; https://huggingface.co/google/gemma-4-26B-A4B-it-qat-q4_0-gguf
- Elenco dei modelli Gemma 4: https://huggingface.co/api/models?author=google&search=gemma-4
- MiniCPM-o 4.5 (copie della scheda, via ricerca): https://huggingface.co/openbmb/MiniCPM-o-4_5
- Nemotron Labs Unified ASR: https://huggingface.co/nvidia/nemotron-labs-unified-asr-0.6b
- Modelli Voxtral: https://huggingface.co/api/models?author=mistralai&search=voxtral
- granite-docling: https://huggingface.co/ibm-granite/granite-docling-258M
- PaddleOCR-VL-1.5: https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5
- Docling: https://github.com/docling-project/docling
- Wan 2.2 TI2V-5B (via ricerca): https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B
- llama.cpp, multimodale: https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md
- llama.cpp, API Messages: https://huggingface.co/blog/ggml-org/anthropic-messages-api-in-llamacpp
- vLLM, trascrizione: https://docs.vllm.ai/en/latest/examples/speech_to_text/openai/
- Speaches (via ricerca): https://speaches-ai.github.io/speaches
- LiteLLM: https://docs.litellm.ai/docs/completion/vision ; https://docs.litellm.ai/docs/completion/audio ; https://docs.litellm.ai/docs/audio_transcription ; https://docs.litellm.ai/docs/providers/vllm
- OpenRouter: https://openrouter.ai/docs/guides/routing/provider-selection ; https://openrouter.ai/docs/guides/features/zdr ; https://openrouter.ai/docs/guides/features/in-region-routing (via ricerca) ; https://openrouter.ai/qwen/qwen3.6-35b-a3b
- Claude, vista e PDF: https://platform.claude.com/docs/en/build-with-claude/vision ; https://platform.claude.com/docs/en/build-with-claude/pdf-support
- Prezzi delle GPU: https://gpuprix.com/eu/workstation ; https://gpuprix.com/italy/gpus/rtx-pro-2000-blackwell ; https://gpuprix.com/italy/gpus/rtx-pro-4000-blackwell ; https://www.scan.co.uk/products/pny-nvidia-rtx-pro-4000-sff-blackwell-pcie-50-24gb-gddr7-ecc-8960-cuda-cores-5th-gen-tensor-cores-re ; https://www.ldlc.com/it-it/scheda/PB00734966.html ; https://ibertronica.es/en/pny-rtx-pro-4000-blackwell-24gb-gddr7 ; RTX 3090 (via ricerca): https://gpuprix.com/eu/gpus/geforce-rtx-3090
- Specifiche RTX PRO 4500 Blackwell (via ricerca): https://www.pny.com/en-eu/File%20Library/Professional/DATASHEET/WORKSTATION/NVIDIA%20RTX%20PRO%20Blackwell/acmk0865_nvidia-rtx-pro-4500-blackwell-webonly.pdf
- Alimentatore HPE 1600 W (via ricerca, pagina non aperta): https://store.inetum.be/product/details/hewlett-packard-enterprise/servers/830272b21/1171UJ44?flang=en
- EVALITA-LLM (via ricerca): https://evalitahf-evalita-llm-leaderboard.hf.space
