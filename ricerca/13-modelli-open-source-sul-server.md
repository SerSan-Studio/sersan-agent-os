# 13 · Modelli open source sul server SerSan: cosa gira davvero e a cosa serve

- **Data**: 2026-10-24. Prezzi e versioni sono stati rilevati oggi, salvo dove indicato.
- **Scopo**: dire ai CEO che cosa può girare **sul server appena comprato** (HPE ProLiant DL380 Gen10 presunto, NVIDIA Quadro RTX 4000 da 8 GB, 160 GB di DDR4-2133 ECC). Per ogni modello aperto: velocità, compiti del sistema multi-agente previsto dalla visione di Alberto e che cosa conviene lasciare a Claude (Opus, Sonnet, Haiku 5.5). In coda: se e come aggiornare la GPU.
- **Legenda**:
  - `[verificato: fonte]`: letto oggi su pagina ufficiale, scheda del modello, repository o file locale citato.
  - `[non verificato]`: stima mia, dato a memoria o voce di terzi (blog, tracker di prezzi, forum). Per le voci di terzi indico la fonte, ma chi fa il prodotto non le ha confermate.
  - «non trovato»: cercato senza risultato.
- **Cosa non ho fatto**: non ho modificato file dei repo, non ho avviato server o processi e non ho misurato nulla sul server, che da qui non si raggiunge. Tutte le velocità sul server sono **stime** ancorate a una misura pubblica della stessa scheda.

---

## 0. In breve

1. **La scheda compare nella classifica pubblica di llama.cpp.** Su un 7B in Q4_0 (Llama 2 7B, `llama-bench`, flash attention attiva) la Quadro RTX 4000 fa **67,6 token/s in scrittura e 1.663 token/s in lettura**. Sulla stessa prova una RTX 3090 fa 161,9 e una T4 44,0. `[verificato: github.com/ggml-org/llama.cpp/discussions/15013]`
2. **Che cosa sta negli 8 GB.** Ci stanno due configurazioni `[non verificato: stime della §3]`:
   - un modello **fino a 8-9B in Q4** con 8-16k token di contesto, a circa **45-50 token/s** stimati per un utente;
   - un **giudice 4B, Whisper turbo e un modello di embedding** accesi insieme.

   Un 12-14B entra solo spostando una parte dei pesi in RAM, e scende a circa **8-15 token/s** stimati.
3. **I 160 GB di RAM sono la sorpresa.** Bastano per i MoE grandi con gli esperti in RAM (Qwen3.6-35B-A3B, gpt-oss-120b), utili per i lavori notturni su dati sensibili, a circa **10-25 token/s** stimati. Il collo di bottiglia è la RAM: DDR4-2133 in 10 moduli, con canali non tutti pieni. Va misurata. `[non verificato: stima]`
4. **Turing è vecchia per l'ecosistema Python.** Non ha BF16 né FlashAttention 2, che richiede SM ≥ 8.0. vLLM la supporta (SM 7.5) ma con limiti seri, e **Gemma 4 su vLLM non parte su Turing** con nessun backend di attenzione. Qui lo stack giusto è **llama.cpp** (`llama-server` con CUDA), più faster-whisper per la voce. `[verificato: docs vLLM e issue #38918 via ricerca; classifica llama.cpp con colonna FA per la RTX 4000]`
5. **Il prezzo di Claude cambia il conto.** `[verificato: platform.claude.com/docs/en/about-claude/pricing]`
   - **Haiku 5.5**: 0,10 $ per milione di token in ingresso e 0,50 $ in uscita, per prompt fino a 100k token.
   - Sonnet 5.5: 2 $ e 10 $. Opus 5.5: 4 $ e 20 $. La Batch API toglie il 50 %.
   - Riassumere con Haiku 5.5 una call da 12k token costa circa **0,0017 $**.

   Il locale quindi **non si giustifica col risparmio** sui token. Si giustifica con la **privacy** (i dati dei clienti non escono), con gli **embedding** (che Anthropic non vende) e con l'audio.
6. **Voce: lo STT italiano in locale è maturo.** Ci sono Whisper large-v3-turbo, Parakeet TDT 0.6B v3 (25 lingue europee) e Qwen3-ASR (italiano, Apache-2.0). `[verificato: schede su Hugging Face e catalogo NVIDIA]`
7. **Il TTS italiano con clonazione e licenza commerciale esiste, ma nessuno di noi ne ha misurato la qualità in italiano.** `[verificato: GitHub resemble-ai/chatterbox, HF Qwen3-TTS]`
   - **Chatterbox Multilingual V3**: licenza MIT, filigrana Perth su ogni audio.
   - **Qwen3-TTS**: Apache-2.0. Il modello 1.7B ha WER italiano 0,948 e somiglianza del parlante 0,817.

   Per l'agente telefonico «Andrea» la scelta pratica oggi resta **ElevenLabs**, già in casa. Dal 2 agosto 2026 l'articolo 50 dell'AI Act chiede trasparenza sui contenuti sintetici. `[non verificato: commenti legali]`
8. **Embedding.** Nella tabella della sua scheda, **Qwen3-Embedding-0.6B** (Apache-2.0, 32k token) fa 64,33 su MMTEB. Batte bge-m3 (59,56) e multilingual-e5-large-instruct (63,22). Gira su GPU oppure su CPU. Come reranker c'è Qwen3-Reranker-0.6B. `[verificato: HF Qwen/Qwen3-Embedding-0.6B]`
9. **Giudici «System One».** `[verificato: README di CLM, serve_qwen3_8b.sh]`
   - Jev è un servizio cloud: i dati escono.
   - **CLM** (Apache-2.0) si appoggia a un encoder Qwen3-8B servito da vLLM, che in FP16 pesa circa 16 GB. Nella forma di riferimento **non entra negli 8 GB**.
   - Oggi il giudice locale sensato è un **Qwen3-4B che legge la probabilità del primo token**.
10. **Upgrade della GPU: non ora.** Se dopo 4-6 settimane di misure servirà più qualità in locale, le schede adatte a un 2U HPE sono quelle «da server» da 24 GB con un solo connettore di alimentazione. In entrambi i casi la RTX 4000 resta nel server per STT ed embedding.
    - **RTX A5000**: 230 W, 8-pin, 2 slot, 2.438 € nuova.
    - **RTX PRO 4000 Blackwell**: 140 W, 1 slot, 2.555 € oggi, minimo dell'ultimo anno 1.544 €.

    Le RTX 3090 e 4090 consumer sono sconsigliate nel DL380 per dimensioni, connettori e consumi (350-450 W). `[prezzi verificati: gpuprix.com/eu/workstation, pagina senza data letta il 2026-10-24; compatibilità: non verificato]`

---

## 1. Il server visto da un modello linguistico

| Componente | Dato | Che cosa conta per i modelli | Stato |
|---|---|---|---|
| GPU | NVIDIA Quadro RTX 4000, Turing TU104, 8 GB GDDR6 su bus a 256 bit (circa 416 GB/s), 2.304 CUDA core, 160 W, slot singolo | La velocità di scrittura di un LLM dipende dalla **banda di memoria**. La misura pubblica (67,6 t/s su 3,82 GB di pesi) dà una banda **effettiva** di circa 258 GB/s, il 62 % del valore teorico | specifiche: `[non verificato: dati del compito e scheda NVIDIA a memoria]`; misura: `[verificato: llama.cpp discussion 15013]` |
| Precisione | FP16 e INT8 sui tensor core. **Niente BF16 nativo, niente FP8 né FP4** | I modelli pubblicati in BF16 (Qwen3-ASR, Qwen3-TTS, l'encoder di CLM) vanno caricati in FP16 o FP32, oppure convertiti in GGUF. vLLM chiede `--dtype float16` | `[verificato: issue vLLM #1157 «Bfloat16 is only supported on GPUs with compute capability of at least 8.0»]` |
| Attenzione | FlashAttention 2 richiede SM ≥ 8.0. llama.cpp ha kernel FA propri che su Turing funzionano (+8 % in lettura sulla RTX 4000) | In Python (vLLM, transformers) l'attenzione veloce manca o è parziale; in llama.cpp no | `[verificato: issue vLLM #38918 e #29743 via ricerca; classifica llama.cpp: 1.662,8 t/s con FA contro 1.536,9 senza]` |
| CPU | Xeon Scalable, modello ignoto (1 o 2 socket da 8-20 core) | La DDR4-2133 fa pensare a Xeon di 1ª generazione o a moduli lenti. HPE elenca la RTX 4000 per il DL380 Gen10 **solo con Xeon Scalable di 2ª generazione**: è un vincolo del configuratore, non un limite fisico | `[non verificato: forum HPE che cita le QuickSpecs; la pagina risponde 403]` |
| RAM | 160 GB = 10 moduli da 16 GB DDR4-2133 ECC RDIMM | Circa 17 GB/s teorici per canale. Il DL380 Gen10 ha 6 canali per CPU, quindi 10 moduli su 2 socket lasciano canali vuoti o sbilanciati. Banda utile per llama.cpp stimata in **45-60 GB/s per socket** | `[non verificato: calcolo mio; il popolamento reale si legge con dmidecode]` |
| Bus | PCIe 3.0 (generazione Gen10) | Conta quando llama.cpp sposta pesi dalla RAM alla GPU per leggere prompt lunghi con gli esperti in RAM | `[non verificato]` |
| Dischi | SAS/SATA su controller Smart Array E208i-p | Caricare un modello da 5 GB richiede secondi, non minuti. Conviene tenere i modelli residenti | `[non verificato: stima]` |

Conseguenza pratica: **ogni processo che usa la GPU occupa anche il proprio contesto CUDA**, qualche centinaio di MB `[non verificato]`. Sono meglio pochi processi con più modelli o più slot che tanti processi piccoli.

---

## 2. I modelli candidati a ottobre 2026

### 2.1 Cosa esiste davvero (famiglie verificate oggi su Hugging Face)

| Famiglia | Taglie pubblicate | Data | Licenza | Stato |
|---|---|---|---|---|
| **Qwen3.5** | 0.8B, 2B, 4B, 9B, 27B, 35B-A3B (MoE), 122B-A10B, 397B-A17B | feb 2026 | Apache-2.0 | `[verificato: API HF Qwen; licenza: non verificato]` |
| **Qwen3.6** | 27B, 35B-A3B (anche in FP8) | apr 2026 | Apache-2.0 | `[verificato: API HF; licenza: non verificato, voci di terzi]` |
| **Qwen3.8** | 27B, Flash-Next, 2.4T-A95B | ago 2026 | non letta | `[verificato: API HF; licenza non trovata]` |
| Qwen3 (2025) | 4B, 4B-Instruct-2507, 8B, 14B, 30B-A3B | 2025 | Apache-2.0 | `[non verificato]` |
| **Gemma 4** | E2B, E4B, **12B** (mag 2026), 26B-A4B (MoE), 31B; versioni QAT Q4_0 in GGUF ufficiali | mar-giu 2026 | Apache-2.0 secondo fonti terze | `[verificato: API HF google; licenza: non verificato]` |
| Ministral 3 | 3B, 8B, 14B | dic 2025 | Apache-2.0 | `[non verificato]` |
| Granite 4.1 | 8B (e 30B) | apr 2026 | Apache-2.0 | `[non verificato]` |
| gpt-oss | 20b (21B, di cui 3,6B attivi), 120b | 2025 | Apache-2.0 | `[non verificato]` |
| SmolLM3 | 3B | 2025 | Apache-2.0; l'italiano è tra le 6 lingue native | `[non verificato]` |
| Phi-4, Phi-4-mini | 14B, 3,8B | 2025 | MIT; la scheda avverte che le lingue diverse dall'inglese vanno peggio | `[non verificato]`; **Phi-5: non trovato** |
| Mistral Small | 3.2 da 24B (2025); Small 4 è un MoE da 119B | 2025-26 | Apache-2.0 | `[non verificato]` |
| Llama 4 | Scout 109B-A17B, Maverick 400B | 2025 | Llama 4 Community License (restrittiva) | `[non verificato]` |
| DeepSeek R1 distillati | 7B, 14B (su base Qwen 2.5) | gen 2025 | MIT | `[non verificato]`; superati da Qwen3.5 e 3.6 |
| Nemotron 3 Nano | 4B | 2026 | solo inglese | `[non verificato]` |

### 2.2 Che cosa entra negli 8 GB

Le dimensioni dei file, dove indicate, le stimo a circa 0,6 GB per miliardo di parametri. «Entra» vuol dire che pesi, 8k token di cache e margine restano sotto i 7,5 GB.

| Modello | File Q4 | Entra in 8 GB? | Ruolo possibile | Nota su Turing e italiano |
|---|---|---|---|---|
| Qwen3.5-2B | — | sì | riserva del giudice | — |
| Ministral 3 3B | — | sì | giudice di riserva | — |
| **Qwen3-4B / 4B-Instruct-2507** | — | sì, con altri modelli accanto | **giudice e classificatore** | — |
| Qwen3.5-4B | — | sì | giudice | Architettura ibrida DeltaNet, quindi cache del contesto più piccola |
| Gemma 4 E4B | circa 3-5 GB | sì | giudice multimodale | — |
| **Qwen3.5-9B** | — | sì, quasi da solo | **estrazioni e riassunti in locale** | — |
| **Ministral 3 8B** | — | sì | estrazioni, risposte veloci | — |
| Granite 4.1-8B | — | sì | estrazioni | — |
| Gemma 4 12B | — | **no**, con una cache utile | — | solo con parte dei layer in RAM; su vLLM con Turing non parte `[verificato: issue vLLM #38918]` |
| Qwen3-14B, Phi-4, Ministral 3 14B | circa 8,5-9 GB | no: offload in RAM | qualità intermedia | `[non verificato: dimensioni stimate]` |
| gpt-oss-20b | circa 12 GB (MXFP4) | no: esperti in RAM | ragionamento a sforzo basso per i lavori in batch | — |
| Qwen3.6-35B-A3B, Qwen3.5-35B-A3B | circa 21-22 GB | no: esperti in RAM, attenzione su GPU | **qualità da 30B al costo di 3B attivi**, per i batch notturni | `[non verificato: dimensione stimata]` |
| Gemma 4 26B-A4B | circa 15-16 GB | no: esperti in RAM | come sopra | `[non verificato]` |
| Qwen3.6-27B, Qwen3.8-27B, Gemma 4 31B (densi) | circa 16-19 GB | no; con l'offload scrivono a 2-4 t/s | non adatti a questo server | `[non verificato: stima]` |
| gpt-oss-120b | circa 61-65 GB (MXFP4) | sì, **in RAM** (160 GB), con l'attenzione su GPU | il modello aperto più forte che il server può far girare, solo in batch | `[non verificato: stima]` |

### 2.3 Modello per compito

| Compito del sistema | In locale sulla RTX 4000 | Dove gira | In cloud | Consiglio |
|---|---|---|---|---|
| Classificare, instradare, giudicare intento e rischio (sì/no, scelta, punteggio) | Qwen3-4B o 4B-Instruct-2507 in Q4_K_M. Per ogni etichetta si legge la **probabilità del primo token** (`/completion` con `n_probs`), mai la confidenza che il modello dichiara. Per le classi stabili, SetFit su CPU | GPU | Haiku 5.5; Jev (TypeSafe) | locale per i flussi sensibili (email dei clienti, trascrizioni); Haiku 5.5 per il resto |
| Estrarre dati in JSON (da email a CRM, da trascrizione a prossimi passi) | Qwen3.5-9B, Ministral 3 8B o Granite 4.1-8B, con lo schema JSON imposto dalla **grammatica** di llama.cpp | GPU | Haiku 5.5 o Sonnet 5.5 | locale solo per i dati «solo locali» |
| Riassumere trascrizioni (30-60 minuti, cioè 8-20k token) | 8-9B con 16-32k di contesto e cache q8_0. Di notte, MoE 35B-A3B o gpt-oss-120b con gli esperti in RAM | GPU, poi GPU più RAM | Sonnet 5.5 per la qualità, Haiku 5.5 per il volume | Claude quando la trascrizione può uscire; locale quando no |
| Oscurare i dati personali prima di mandare testo a Claude | GLiNER multilingue per i dati personali, Microsoft Presidio, regole per codice fiscale, IBAN e partita IVA | CPU | — | sempre locale: serve proprio a questo `[non verificato: strumenti non riletti oggi]` |
| Embedding per il database vettoriale | Qwen3-Embedding-0.6B o bge-m3 | CPU o GPU | nessuno: Anthropic non vende embedding `[non verificato]` | **locale** |
| Riordinare i risultati di ricerca (rerank) | Qwen3-Reranker-0.6B o bge-reranker-v2-m3 | CPU o GPU | — | **locale** |
| Scrivere (follow-up, brief pre-meeting, offerte), usare strumenti in catena, orchestrare | no | — | Sonnet 5.5, Opus 5.5 | Claude |

### 2.4 I giudici «System One»: Jev, CLM, Kev

| Nome | Che cos'è | Licenza | Su questo server | Stato |
|---|---|---|---|---|
| **Jev** (TypeSafe) | API cloud che risponde a domande tipizzate (sì/no, scelta, punteggio) | servizio a pagamento | i dati escono verso un terzo; da valutare solo per dati non sensibili | `[non verificato]` |
| **CLM** (Contrastive-LM) | «System One» locale con la stessa API di Jev. È CLM-8B: una testa da 75 MB sopra gli embedding di **Qwen3-8B servito da vLLM** (`--runner pooling`, contesto 2048). Dichiara 58 ms su un esempio e «fino a 9 volte meno latenza» di Jev | Apache-2.0 | Qwen3-8B in FP16 pesa circa 16 GB: nella forma di riferimento **non entra negli 8 GB**. Due strade: provare l'encoder Qwen3-8B in GGUF Q8 o Q4 su llama.cpp con pooling «last» (la testa è addestrata su embedding a piena precisione, quindi lo scarto va misurato), oppure aspettare una GPU da 24 GB | `[verificato: README di CLM e serve_qwen3_8b.sh]`; adattamento a GGUF `[non verificato]` |
| **Kev** (jaredpalmer) | modelli locali simili a Jev, da 0,8B a 27B | Apache-2.0 | — | `[non verificato: repo non letto]` |

Valutazione per SerSan: con Haiku 5.5 a 0,10 $ per milione di token, un milione di giudizi da 600 token costa circa 60 $. CLM e Kev quindi **non servono per risparmiare**: servono solo se i giudizi riguardano dati che non devono uscire. Per quei dati si parte dal Qwen3-4B locale; CLM è il secondo esperimento.

---

## 3. Velocità realistiche sulla RTX 4000

### 3.1 L'àncora misurata

| Scheda (Turing, salvo dove indicato) | Lettura pp512 t/s (con FA) | Scrittura tg128 t/s (con FA) |
|---|---|---|
| RTX 2080 Ti | 3.107,6 | 109,2 |
| RTX 2070 SUPER | 2.293,3 | 87,7 |
| **Quadro RTX 4000** | **1.662,8** | **67,6** |
| RTX 2060 SUPER | 1.563,8 | 61,1 |
| Tesla T4 | 1.309,7 | 44,0 |
| RTX 3060 (Ampere) | 2.407,7 | 76,9 |
| RTX 3090 (Ampere) | 5.560,1 | 161,9 |
| RTX 4090 (Ada) | 14.770,6 | 189,0 |

Modello di prova: Llama 2 7B Q4_0, comando `llama-bench -ngl 99 -fa 0,1`; ogni riga ha una build diversa. `[verificato: github.com/ggml-org/llama.cpp/discussions/15013, letto il 2026-10-24]`

### 3.2 Stime per i casi del compito

Metodo: la velocità di scrittura è circa la banda effettiva divisa per i byte letti a ogni token. La banda effettiva della RTX 4000 è circa 258 GB/s (dalla riga sopra); quella utile della RAM la stimo in 45-60 GB/s per socket. Tutte le righe sono `[non verificato: stima mia]` e vanno rimisurate con `llama-bench`.

| Caso | Pesi letti per token | Scrittura stimata (1 utente) | Lettura del prompt stimata | Nota |
|---|---|---|---|---|
| 4B Q4_K_M tutto in VRAM | 2,5 GB | **80-100 t/s** | circa 3.000 t/s | un giudizio con il prefisso già in cache: circa 100-250 ms |
| 7-8B Q4 tutto in VRAM | 4,9-5,7 GB | **45-50 t/s** | circa 1.500 t/s | una trascrizione da 12k token si legge in circa 8 s |
| 14B Q4_K_M con circa 3 GB in RAM | 6 GB in VRAM e 3 GB in RAM | **8-15 t/s** | 300-800 t/s | la parte in RAM domina: 3 GB a 50 GB/s fanno 60 ms per token |
| MoE 30-35B-A3B con gli esperti in RAM (`--n-cpu-moe`) | circa 1,5 GB in RAM e 0,5-1 GB in VRAM | **12-25 t/s** | 250-500 t/s (i pesi passano per il PCIe 3.0) | voce di terzi: Qwen3.6-35B su RTX 3070 Ti da 8 GB passa da 8,7 a «40+» t/s con `-ncmoe`, probabilmente con DDR5 `[non verificato: medium.com/coding-nexus]` |
| gpt-oss-120b con gli esperti in RAM | circa 2,5-3 GB in RAM | **8-15 t/s** | 150-400 t/s | solo per i lavori notturni; con due socket (NUMA) va legato a un solo socket |
| Prova di confronto | — | — | — | solo CPU, Qwen3-30B-A3B Q4_K_M: circa 16,8 t/s su una scheda ARM non precisata `[non verificato: forum Radxa]` |

### 3.3 Quante richieste in parallelo

- llama-server serve più conversazioni insieme con gli **slot** (`-np N`) e il batching continuo. La scrittura è limitata dalla banda: con 4 slot la produzione **totale** sale a circa 2-2,5 volte quella di un utente solo, mentre ogni conversazione rallenta. Per un 8B: circa 25-30 t/s a testa, 100-120 t/s in tutto. `[non verificato: stima]`
- Il limite vero è la **cache del contesto**. Per Qwen3-4B e 8B (36 strati, 8 teste KV da 128) servono circa 147 KB per token in FP16 e circa 74 KB in q8_0. `[non verificato: calcolo mio sulle architetture]`
  - Con un 8B in VRAM restano circa 1,5-2 GB: **20-27k token in tutto**, per esempio 3 slot da 8k.
  - Con un 4B restano 4-4,5 GB: circa 55k token in q8_0, per esempio 6-8 slot.
  - I modelli ibridi Qwen3.5 (DeltaNet) e quelli a finestra scorrevole (Gemma 4) ne usano molto meno.
- Per il carico previsto dalla visione (post-call, brief, report) **la capacità non è il problema**: 10 riunioni al giorno da 12k token chiedono circa 25 s di GPU ciascuna con un 8B. Il problema è la **qualità** in italiano quando servono gli strumenti. `[non verificato: stima]`

---

## 4. Stack di servizio

| Motore | Su Turing (SM 7.5) | Pro | Contro | Verdetto |
|---|---|---|---|---|
| **llama.cpp `llama-server`** (CUDA) | sì, con una flash attention propria (misura sopra) | GGUF da 2 a 8 bit; offload per layer e per esperti (`--n-cpu-moe`); grammatica e schema JSON; endpoint compatibili OpenAI; embedding e rerank; slot paralleli; build fissabile | meno throughput di vLLM con decine di utenti; parser degli strumenti con bug noti su Qwen e Gemma (issue #20198, #20260, #27767, #29655) | **scelta principale** `[verificato: classifica llama.cpp; bug: non verificato]` |
| vLLM | supportato da SM 7.5, ma: **niente FlashAttention** (serve SM ≥ 8.0); FlashInfer funziona sulla T4 con limiti sulla dimensione delle teste; niente BF16; **Gemma 4 fallisce su RTX 2080 Ti con tutti i backend** (Turing ha 64 KB di memoria condivisa per SM); nessun backend Turing per Qwen3-VL | throughput alto con molti utenti; API di pooling (serve a CLM); Qwen3-ASR in streaming | 8 GB sono pochi per la sua cache a pagine; le quantizzazioni veloci (Marlin, FP8) sono pensate per Ampere e successive | **solo per esperimenti** (CLM, Qwen3-ASR) o su una futura GPU Ampere o più recente `[verificato: docs.vllm.ai pagina di installazione GPU, issue #38918, #29743, #1157 via ricerca; Marlin: non verificato]` |
| Ollama | sì (usa un motore derivato da llama.cpp) | installazione e cambio di modello con un comando | meno controllo su flag, versioni e grammatiche; un runtime in più da gestire | va bene per i prototipi, non come base `[non verificato]` |
| TGI (Hugging Face) | — | — | **in manutenzione dal dicembre 2025**: accettano solo correzioni minori; Hugging Face consiglia vLLM, SGLang e llama.cpp | escluso `[verificato: README ufficiale di TGI via ricerca; la data 11/12/2025 è una voce di terzi]` |
| SGLang | supporto Turing **non trovato** | throughput alto | stesso problema di vLLM con 8 GB | escluso per ora |

Contorno consigliato:
- un `llama-server` per ruolo (giudice, lavoro, embedding) con build **fissata**, mai aggiornata in automatico. In alternativa, un selettore che carica e scarica i modelli a richiesta, per esempio llama-swap `[non verificato]`;
- una **coda con priorità** davanti alla GPU (tempo reale prima del giorno, giorno prima della notte). I 25-100 agenti non devono mai chiamare la GPU direttamente.

---

## 5. Riconoscimento vocale italiano in locale

| Modello | Italiano | Licenza | VRAM e velocità | Su Turing | Stato |
|---|---|---|---|---|---|
| **Whisper large-v3-turbo** via faster-whisper (CTranslate2) | sì | MIT | turbo in int8 circa 1,5 GB, in fp16 circa 2,5 GB. 13 minuti di audio in circa 19 s su una GPU non nominata, cioè circa 40 volte il tempo reale | CTranslate2 richiede CUDA 12 e cuDNN 9; fp16 e int8 girano su Turing | VRAM e velocità: `[non verificato: blog di un venditore citato nella ricerca]`; requisiti: `[verificato: github.com/SYSTRAN/faster-whisper]` |
| Whisper large-v2 (prova ufficiale di riferimento) | sì | MIT | RTX 3070 Ti 8 GB, 13 minuti di audio: 59 s in int8 (2.926 MB); **16 s in int8 a lotti da 8 (4.500 MB)**; 17 s in fp16 a lotti (6.090 MB) | la RTX 4000 ha circa un terzo della potenza di calcolo della 3070 Ti: aspettarsi 2-3 volte più lento, cioè **un'ora di call in 2-5 minuti** a lotti | misura: `[verificato: README di faster-whisper v1.1.0]`; stima per Turing: `[non verificato]` |
| **Parakeet TDT 0.6B v3** (NVIDIA) | sì: 25 lingue europee, lingua riconosciuta da sola | CC-BY-4.0, uso commerciale ammesso | molto più veloce di Whisper; WER italiano su FLEURS del 3,00 % dichiarato da NVIDIA | NeMo in FP16 o FP32 | lingue e uso commerciale: `[verificato: catalogo NGC via ricerca]`; WER: `[non verificato]` |
| **Qwen3-ASR 1.7B e 0.6B** | sì | Apache-2.0 | WER su FLEURS (12 lingue, italiano compreso) 4,90 contro 5,27 di Whisper large-v3; su Common Voice 9,18 contro 10,77. Lo streaming funziona solo con vLLM | pesi in BF16, FlashAttention 2 consigliata: su Turing serve FP16, oppure la versione GGUF in llama-server | `[verificato: huggingface.co/Qwen/Qwen3-ASR-1.7B]`; GGUF: `[non verificato]` |
| Qwen3-ForcedAligner 0.6B | sì (11 lingue) | Apache-2.0 | tempi parola per parola, fino a 5 minuti di audio | come Qwen3-ASR | `[verificato: scheda di Qwen3-ASR]` |
| Nemotron 3.5 ASR streaming 0.6B | dichiarato «pronto» per l'italiano | OpenMDW-1.1 | WER su FLEURS 4,41 % a blocchi di 560 ms; la scheda elenca solo GPU NVIDIA su Linux | adatto proprio a questo server | `[non verificato]` |
| Canary-1b-v2 | 25 lingue europee | CC-BY-4.0 | — | — | `[non verificato]` |

**Chi parla (diarizzazione)**: `[non verificato: README di pyannote e note di terzi via ricerca, pagine non lette per intero]`
- pyannote **speaker-diarization-community-1**: CC-BY-4.0, scaricabile da Hugging Face solo dopo aver accettato i termini.
- Sul benchmark AMI impiega circa 31 s di calcolo per ora di audio, contro 14 s del modello a pagamento precision-2. Usa circa 1 GB di VRAM.
- **WhisperX** (BSD-2) lo usa come predefinito e mette insieme faster-whisper, allineamento delle parole e pyannote.
- L'alternativa NVIDIA è NeMo (Sortformer, MSDD) `[non verificato]`.

Nota di progetto: se SerSan adotta **Fireflies**, trascrizione e diarizzazione delle riunioni arrivano già fatte. Lo STT locale servirebbe allora all'audio che non deve uscire, alle chiamate dell'agente vocale e come riserva.

---

## 6. Sintesi vocale italiana in locale, e la clonazione

| Modello | Italiano | Clonazione | Licenza | Su Turing | Stato |
|---|---|---|---|---|---|
| **Chatterbox Multilingual V3** (Resemble AI) | sì (23+ lingue) | sì, da un clip breve (l'esempio usa 10 s) | **MIT**. Ogni audio porta la filigrana **Perth**, che lo script fornito rileva | 500M parametri, PyTorch | `[verificato: github.com/resemble-ai/chatterbox]`; qualità in italiano `[non verificato]` |
| **Qwen3-TTS 12Hz 0.6B e 1.7B** | sì (10 lingue) | sì, da «3 secondi» di audio | **Apache-2.0** | pesi in BF16, FlashAttention 2 consigliata: su Turing va provato in FP16 o FP32 | in italiano: WER 0,948 e somiglianza del parlante 0,817 per il 1.7B, 1,534 e 0,792 per lo 0.6B. Latenza della famiglia «fino a 97 ms» `[verificato: huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base]` |
| Kokoro 82M | 2 voci italiane di grado C | no | Apache-2.0 | gira anche su CPU | `[non verificato]` |
| Piper `it_IT-serena-high` | sì, voce femminile sintetica | no | modello MIT; il runtime `piper1-gpl` è GPL-3.0 e va tenuto in un processo separato | CPU | `[non verificato]` |
| XTTS-v2 (Coqui) | sì | sì | Coqui Public Model License, **non commerciale**. Coqui ha chiuso nel 2024 e nessuno vende più la licenza | — | `[non verificato: promptquorum.com]` |
| F5-TTS | parziale | sì | pesi CC-BY-NC-4.0 | — | `[non verificato: voce di terzi]` |
| Orpheus 3B | ci sono versioni multilingue di ricerca; italiano non confermato | sì | base Llama 3.2 | — | `[non verificato]` |
| Voxtral TTS (Mistral) | sì | — | pesi CC BY-NC: utilizzabile solo via API | — | `[non verificato]` |

**Consenso e regole sulla voce clonata** (l'agente «Andrea»):
- La voce di un collega è un **dato personale**. Per clonarla serve un **consenso scritto, specifico e revocabile** del collega, con l'elenco degli usi. `[non verificato: mia lettura del GDPR, non consultato oggi]`
- L'**AI Act, articolo 50**, si applica dal **2 agosto 2026**. `[non verificato: commenti di studi legali (Sidley, artificialintelligenceact.eu, Baker Botts); il testo del regolamento non l'ho letto]`
  - **50.1**: un sistema che parla con le persone deve dire di essere un'IA. È il caso del richiamo dei lead.
  - **50.2**: l'audio sintetico va marcato in modo leggibile da una macchina. Per i sistemi già sul mercato c'è tempo fino al 2 dicembre 2026.
  - **50.4**: l'audio che imita una persona reale va dichiarato come generato.
  - Il Digital Omnibus (Reg. UE 2026/1744) ha rinviato gli obblighi sui sistemi ad alto rischio, non l'articolo 50. Le sanzioni arrivano a 15 milioni di euro o al 3 % del fatturato.
- SerSan ha sede a Londra ma lavora con clienti e persone in Italia: se queste regole si applichino va chiesto a un legale.
- La filigrana Perth di Chatterbox aiuta a rispettare l'obbligo di marcatura `[non verificato]`.

**Perché «Andrea» resta su ElevenLabs per ora.** Un agente telefonico deve fare STT in streaming, LLM e TTS clonato insieme, in italiano e sotto il secondo. Negli 8 GB della scheda Turing ci starebbero al massimo un 4B, Parakeet e un TTS da 0,5-1,7B, senza nessuna misura di qualità in italiano. ElevenLabs è già pagata e copre clonazione, voce e agenti. `[non verificato: stima]`

---

## 7. Embedding e reranker multilingue

| Modello | Parametri | Licenza | MMTEB (media dei compiti) | Contesto | Dove gira | Stato |
|---|---|---|---|---|---|---|
| **Qwen3-Embedding-0.6B** | 0,6B | Apache-2.0 | **64,33** | 32k token; dimensione del vettore a scelta tra 32 e 1024 (MRL) | GPU o CPU | `[verificato: scheda HF]` |
| Qwen3-Embedding-4B e 8B | 4B e 8B | Apache-2.0 | 69,45 e 70,58 | 32k | il 4B in Q4 entra in GPU; l'8B no, se accanto c'è altro | `[verificato: scheda HF; i punteggi degli altri modelli vengono dalla classifica del 24 maggio 2025]` |
| multilingual-e5-large-instruct | 0,6B | MIT | 63,22 | 512 | CPU | `[verificato: tabella della scheda Qwen; licenza non verificata]` |
| **bge-m3** | 0,6B | MIT | 59,56 | 8k; un solo modello fa vettori densi, sparsi e multi-vettore | CPU o GPU | `[verificato: punteggio dalla scheda Qwen; licenza: voce di terzi]` |
| EmbeddingGemma-300m | 0,3B | Gemma Terms | — | — | CPU | `[non verificato]` |
| jina-embeddings-v3 e reranker v2 | — | CC-BY-NC (non commerciale) | — | — | — | `[non verificato]`; da escludere se confermato |
| **Qwen3-Reranker-0.6B, 4B e 8B** | 0,6-8B | Apache-2.0 | la scheda letta non riporta punteggi | 32k | lo 0.6B su CPU o GPU | `[verificato: tabella della serie nella scheda di Qwen3-Embedding]` |
| bge-reranker-v2-m3 | 0,6B | Apache-2.0 | — | 8k | CPU o GPU | `[non verificato]` |

Avvertenza: per la **ricerca** (RAG) nessuno di noi ha misure. Prima di scegliere: 50 domande italiane vere su trascrizioni ed email di SerSan, con recall@10 misurato con e senza reranker.

---

## 8. Budget della VRAM: cosa tenere acceso insieme

### Profilo A, «sempre acceso» (consigliato per partire)

| Servizio | VRAM | Fonte |
|---|---|---|
| Giudice Qwen3-4B Q4_K_M | da misurare | — |
| Embedding Qwen3-Embedding-0.6B | da misurare | — |
| STT faster-whisper large-v3-turbo int8 | circa 1,5 GB più il contesto CUDA | `[non verificato: voce di terzi]` |

La diarizzazione con pyannote si fa dopo lo STT o su CPU; il reranker sta su CPU.

### Profilo B, «LLM di lavoro» (una giornata con estrazioni in locale)

| Servizio | VRAM | Fonte |
|---|---|---|
| Ministral 3 8B o Qwen3.5-9B Q4_K_M, 16k token, cache q8_0 | da misurare | — |
| Giudice: lo stesso modello su uno slot dedicato, oppure Qwen3-4B su CPU | 0 | `[non verificato]` |
| Embedding, reranker, STT | su CPU o in coda | — |

### Profilo C, «notte» (lavori lunghi)

1. STT degli audio arretrati sulla GPU, a lotti (`batch_size` 8: per large-v2 in int8 il README ufficiale misura circa 4,5 GB).
2. Poi il MoE grande (Qwen3.6-35B-A3B o gpt-oss-120b): attenzione e cache sulla GPU, esperti nei 160 GB di RAM. Serve per riassunti e analisi su dati che non devono uscire.

### Cosa va sempre sulla CPU, con i 160 GB

- Embedding e reranker quando la GPU è occupata: bge-m3 e Qwen3-Embedding-0.6B girano bene su CPU.
- Classificatori SetFit, oscuramento dei dati personali (GLiNER, Presidio), Silero VAD, Smart Turn, Piper.
- Gli esperti dei MoE, cioè decine di GB.
- Il resto del server: Postgres con pgvector, SersanOutreach, l'orchestratore, i connettori.

La RAM è abbondante; a scarseggiare è la sua **banda**. `[non verificato]`

---

## 9. Aggiornare la GPU: opzioni compatibili con un DL380 Gen10

### Regole del telaio (da confermare sul server)

Fonte: risposte di dipendenti HPE nel forum community.hpe.com che citano le QuickSpecs a00008180enw. Oggi non ho potuto leggere le QuickSpecs (timeout) e il forum risponde 403. `[non verificato]`
- La Quadro RTX 4000 è tra le opzioni supportate dal DL380 Gen10.
- Richiede tre kit: **cavi di alimentazione P03849-B21**, **ventole ad alte prestazioni 867810-B21**, **dissipatore ad alte prestazioni 826706-B21**.
- Un kit di cavi alimenta fino a 3 schede a doppia larghezza o 6 a larghezza singola. Il server regge fino a 5 RTX 4000.
- Una scheda che non compare nelle QuickSpecs «potrebbe non funzionare in modo ottimale».

Le schede non HPE possono far girare le ventole al massimo tramite iLO `[non verificato]`. Secondo gli standard PCIe, il cavo già in casa (mini-8pin verso 6+8) porta al massimo 75 + 150 W dal connettore, più i 75 W dello slot `[non verificato: calcolo]`.

### Le schede candidate

| Scheda | VRAM, banda | Consumo, formato, alimentazione | Nel DL380 Gen10 | Prezzo rilevato | Scrittura 8B Q4 stimata | Che cosa sblocca |
|---|---|---|---|---|---|---|
| Quadro RTX 4000 (attuale) | 8 GB, 416 GB/s | 160 W, 1 slot, ventola, 8-pin | sì, nelle QuickSpecs | già comprata | **circa 50 t/s** (misura sul 7B: 67,6) | — |
| RTX A4000 | 16 GB, 448 GB/s | 140 W, 1 slot, turbina, 6-pin | probabile | **1.508 €** (Amazon FR) | circa 55 | 12-14B tutti in VRAM; un 8B e lo STT insieme |
| RTX A4500 | 20 GB, 640 GB/s | 200 W, 2 slot, 8-pin | probabile | **1.409 €** (Amazon FR) | circa 80 | 20-24B in Q4; il MoE 26B-A4B quasi tutto in VRAM |
| **RTX A5000** | 24 GB, 768 GB/s | 230 W, 2 slot, turbina, 8-pin | probabile: formato e connettore da server | **2.438 €** nuova (Amazon FR); usata 1.400-2.100 $ (annunci eBay USA) | circa 95 | 27B in Q4 o 35B-A3B quasi tutto in VRAM; l'encoder di CLM in FP16 (16 GB) più il giudice; STT e LLM medio insieme |
| RTX 4000 Ada | 20 GB, 360 GB/s | 130 W, 1 slot | probabile; connettore da verificare | **1.958 €** (Amazon IT) | circa 45 | come la A4500, ma scrive più lenta; ha FP8 |
| **RTX PRO 4000 Blackwell** | 24 GB GDDR7, 672 GB/s, 8.960 CUDA core | 140 W, 1 slot, ventola singola | probabile; connettore a 16 pin da verificare | **2.555 €** (MediaWorld IT, 22-24 ottobre); minimo dell'ultimo anno 1.544 €, mediana 2.326 € | circa 85 | come la A5000 con metà del consumo; FP8, FP4, BF16 e FlashAttention |
| NVIDIA L4 | 24 GB, 300 GB/s | 72 W, profilo basso, **passiva**, senza cavo | va bene col flusso d'aria di un server; supporto HPE sul Gen10 **non trovato** | 1.600-1.800 € (annunci eBay.de del 2025; prezzo del 2026 non trovato) | circa 38 | 24 GB con pochi watt, ma scrive più lenta della scheda attuale |
| RTX 3090 usata | 24 GB, 936 GB/s | 350 W, 2,5-3 slot, 2 connettori 8-pin o uno a 12 pin, sul bordo alto | **sconsigliata**: altezza e connettori non stanno in un 2U, e chiede più potenza di quella del cavo 6+8 | **843-1.392 €** usata (tracker europeo, cifre discordanti) | circa 125 (misura sul 7B: 161,9) | la più veloce per euro, ma non è una scheda da server |
| RTX 4090 | 24 GB, 1.008 GB/s | 450 W, 3 slot o più | no | non rilevato | circa 145 (misura sul 7B: 189,0) | — |

Fonti della tabella:
- prezzi delle schede professionali: `[verificato: gpuprix.com/eu/workstation, letto il 2026-10-24; un solo venditore per scheda, pagina senza data]`;
- minimo e mediana della PRO 4000: `[non verificato: gpuprix.com/eu/gpus/rtx-pro-4000-blackwell via ricerca, aggiornato il 22 ottobre]`;
- specifiche della PRO 4000: `[verificato: schede prodotto di Microless e Central Computer via ricerca]`;
- RTX 3090: `[non verificato: bestvaluegpu.com, gpudojo.com]`;
- A5000 usata: `[non verificato: annunci eBay, gpupoet.com di giugno 2026]`;
- L4: `[non verificato: annunci eBay.de]`;
- specifiche delle altre schede: `[non verificato: a memoria]`;
- velocità stimate in proporzione alla banda, partendo dalla misura della RTX 4000: `[non verificato: stima]`;
- misure sul 7B di 3090 e 4090: `[verificato: classifica llama.cpp]`.

Cosa **non** sblocca nemmeno una scheda da 24 GB: un 70B denso in Q4 pesa circa 40 GB e con l'offload sulla DDR4 scriverebbe a 2-3 t/s `[non verificato: stima]`. Servono 48 GB o due schede.

Configurazione consigliata **se** si compra: la nuova scheda da 24 GB per il LLM, e la RTX 4000 **lasciata nel server** per STT, embedding e giudice. Secondo cavo e secondo riser sono da verificare.

---

## 10. Raccomandazione

### Cosa fare in locale, subito, senza spendere

1. **Memoria aziendale.** Embedding (Qwen3-Embedding-0.6B o bge-m3) e reranker (Qwen3-Reranker-0.6B) per il database vettoriale su trascrizioni, email e documenti. Qui il locale vince su tutto: privacy, costo zero, e Anthropic non offre embedding.
2. **Pulizia dei dati prima del cloud.** Un giudice locale (Qwen3-4B, probabilità del primo token) classifica sensibilità e instradamento di ogni evento; su CPU si oscurano i dati personali. Così trascrizioni ed email dei clienti arrivano a Claude solo quando possono uscire, o dopo l'oscuramento.
3. **STT a lotti** (faster-whisper large-v3-turbo o Parakeet TDT v3, più pyannote) per l'audio che non deve finire in un servizio esterno. Prima va fatta una prova di WER su 10 chiamate vere di SerSan, accento sardo compreso.
4. **Un 8-9B per i dati «solo locali»** (estrazioni e riassunti), con una persona che rilegge.
5. **Lavori notturni** con un MoE grande in RAM, solo se le prove del punto 2 dicono che l'8-9B non basta.

### Cosa lasciare a Claude, e perché

| Modello | Prezzo per milione di token (ingresso / uscita) | Compiti | Perché |
|---|---|---|---|
| **Haiku 5.5** | 0,10 $ / 0,50 $ per prompt fino a 100k token (oltre: 0,50 / 2,50); lettura dalla cache 0,01 $ | il volume: riassunti, classificazioni ed estrazioni su dati non sensibili o già oscurati | costa meno della corrente che la GPU consumerebbe per lo stesso lavoro `[non verificato: stima dei consumi]`; qualità superiore a un 8B locale `[non verificato]` |
| **Sonnet 5.5** | 2 $ / 10 $; cache 0,10 $ | gli agenti che agiscono: dopo la call scrivono su Slack, aggiornano HubSpot, preparano la mail di follow-up e i to-do; brief pre-meeting; offerte; orchestrazione con strumenti | usare strumenti in catena in italiano è il punto debole dei modelli piccoli |
| **Opus 5.5** | 4 $ / 20 $; cache 0,20 $ | analisi delle call di vendita e coaching, mappa dei processi, pesatura della pipeline, il CRM fatto con Claude Code | ragionamenti lunghi, poche chiamate al giorno |
| Batch API | −50 % su ingresso e uscita | tutto ciò che può aspettare, come i report notturni | — |

Prezzi `[verificato: platform.claude.com/docs/en/about-claude/pricing, letto il 2026-10-24]`. Ai prezzi di Haiku 5.5, gli 800 $ al mese di crediti valgono circa 8 miliardi di token in ingresso: per un'azienda di 4 persone il budget non è un vincolo `[non verificato: calcolo]`.

### Upgrade

Non comprare ora. Per 4-6 settimane si misurano i profili A e B sui dati veri. Una scheda da 24 GB (RTX A5000 o RTX PRO 4000 Blackwell) si compra **solo se** succede una di queste due cose:
- il volume di dati «solo locali» è alto e l'8-9B non basta;
- si decide di portare l'agente vocale in casa.

Da evitare in questo telaio: RTX 3090, RTX 4090 e L4.

---

## 11. Prime prove quando il server è acceso (nessuna è stata eseguita)

| Prova | Comando o metodo | A che cosa serve |
|---|---|---|
| CPU e NUMA | `lscpu`, `numactl -H` | generazione dello Xeon (AVX-512, VNNI) e numero di socket |
| Moduli di RAM | `sudo dmidecode -t memory` | canali popolati e banda reale |
| GPU | `nvidia-smi -q` | modello esatto (versione HPE o no), driver, potenza massima, temperature |
| Banda della RAM | `llama-bench` con un modello solo su CPU | stimare offload e MoE |
| Velocità della GPU | `llama-bench -m <modello> -ngl 99 -fa 1` su 4B, 8B, 12B IQ4_XS e 35B-A3B con `--n-cpu-moe` | sostituire le stime della §3 con misure |
| Qualità in italiano | prompt italiani presi da casi veri di SerSan, per gli strumenti e per il giudice | confronto diretto con Haiku 5.5 |
| STT | 10 chiamate di SerSan: WER e tempo per ora di audio | scegliere tra Whisper turbo, Parakeet e Qwen3-ASR |
| Concorrenza | carico prolungato con 4 utenti | dimensionare slot e code |

---

## 12. Domande aperte

1. Che CPU c'è esattamente (Xeon Scalable di 1ª o di 2ª generazione), e come sono distribuiti i 10 moduli di RAM? Cambia la velocità di tutto ciò che sta in RAM.
2. Quali alimentatori, quale riser e quale kit di ventole ha il server? Da questo dipende se, e quale, seconda GPU può entrare.
3. SerSan userà Fireflies, o un servizio simile, per le riunioni? Se sì, lo STT locale scende di priorità.
4. Quali classi di dati **non** devono mai uscire (email dei clienti, trascrizioni, offerte)? Da questo dipende quanto lavoro tocca al modello locale.
5. Il collega che presta la voce ad «Andrea» firma un consenso? Come si dichiara l'IA a chi viene richiamato (AI Act, art. 50)? Serve un parere legale.
6. CLM vale la prova (encoder Qwen3-8B in GGUF), o basta il giudice Qwen3-4B?
7. Qwen3.8 (agosto 2026): non ho trovato né la licenza né le taglie piccole. Va ricontrollato prima della scelta.
8. Qual è il consumo reale del server sotto carico? Serve per confrontarlo col costo dei token di Haiku 5.5.

---

## 13. Fonti

Lette o interrogate il 2026-10-24.

- llama.cpp, classifica CUDA (Llama 2 7B Q4_0): https://github.com/ggml-org/llama.cpp/discussions/15013
- Hugging Face API, modelli Google (Gemma 4): https://huggingface.co/api/models?author=google&search=gemma-4
- Hugging Face API, modelli Qwen (Qwen3.5, 3.6, 3.8, ASR, TTS): https://huggingface.co/api/models?author=Qwen&sort=createdAt&direction=-1
- Qwen3-Embedding-0.6B: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- Qwen3-ASR-1.7B: https://huggingface.co/Qwen/Qwen3-ASR-1.7B
- Qwen3-TTS 1.7B Base: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base
- Chatterbox: https://github.com/resemble-ai/chatterbox
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- Parakeet TDT 0.6B (catalogo NGC, via ricerca): https://catalog.ngc.nvidia.com/orgs/nvidia/-/collections/parakeet-tdt-0.6b/
- vLLM, installazione su GPU: https://docs.vllm.ai/en/stable/getting_started/installation/gpu/
- vLLM, issue su Turing:
  - Gemma 4: https://github.com/vllm-project/vllm/issues/38918
  - Qwen3-VL: https://github.com/vllm-project/vllm/issues/29743
  - BF16: https://github.com/vllm-project/vllm/issues/1157
- TGI in manutenzione: https://raw.githubusercontent.com/huggingface/text-generation-inference/main/README.md ; per la data: https://www.spheron.network/blog/migrate-tgi-to-vllm-sglang-2026/ (terzi)
- Prezzi di Claude: https://platform.claude.com/docs/en/about-claude/pricing
- Prezzi delle GPU professionali in UE: https://gpuprix.com/eu/workstation ; https://gpuprix.com/eu/gpus/rtx-pro-4000-blackwell (via ricerca)
- RTX 3090 usata (terzi): https://bestvaluegpu.com/en-eu/history/new-and-used-rtx-3090-price-history-and-specs/ ; https://gpudojo.com/rtx-3090
- RTX A5000 usata (terzi): https://gpupoet.com/gpu/learn/price/june-2026/nvidia-rtx-a5000
- L4 (annunci): https://www.ebay.de/itm/146003500251 ; https://www.galaxus.de/en/s1/product/nvidia-l4-24-gb-graphics-card-49553719
- HPE DL380 Gen10 e GPU (forum, non leggibile direttamente):
  - https://community.hpe.com/t5/proliant-servers-ml-dl-sl/hp-dl380g10-nvidia-quadro-rtx4000/td-p/7162876
  - https://community.hpe.com/t5/proliant-servers-ml-dl-sl/rtx-3090-inside-a-dl380-gen10/td-p/7233995
  - QuickSpecs (timeout): https://www.hpe.com/psnow/doc/a00008180enw
- MoE con gli esperti in RAM (terzi):
  - https://medium.com/coding-nexus/one-flag-tripled-my-tokens-per-second-on-an-8gb-gpu-238f55d1e3bd
  - https://aiweekly.co/alerts/qwen3-moe-cpu-expert-offload-doubles-decode-speed-on-12gb-vram
  - https://forum.radxa.com/t/llama-cpp-benchmarks/27813
- pyannote e WhisperX (terzi): https://vexascribe.com/whisper-diarization ; https://cdn.jsdelivr.net/gh/pyannote/pyannote-audio@main/README.md
- TTS e licenze (terzi): https://www.promptquorum.com/power-local-llm/local-tts-voice-cloning-piper-coqui-xtts ; https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models
- AI Act, articolo 50 (terzi):
  - https://datamatters.sidley.com/2026/06/24/eu-ai-act-transparency-obligations-preparing-for-compliance-by-2-august-2026/
  - https://artificialintelligenceact.eu/transparency-rules-article-50/
  - https://www.bakerbotts.com/thought-leadership/publications/2026/september/eu-ai-act-article-50-transparency-obligations-go-live
- CLM (Contrastive-LM), `README.md` e `serve_qwen3_8b.sh`: https://github.com/Contrastive-LM/CLM
