# 51. Un modello open-weight sul computer di sviluppo

- **Data**: 13 novembre 2026. Le pagine web e i file sono stati letti il 12 novembre 2026, salvo dove è scritta un'altra data. Lo stesso giorno un secondo lettore ha ricontrollato sulle fonti i 15 fatti principali: 14 confermati, uno corretto (lo spazio libero sul disco, che qui non riporto perché cambia).
- **Per chi**: chi scrive lo spec della milestone 2; Alberto, che decide se installare e scaricare.
- **Domande a cui risponde**:
  1. I programmi che servono un modello in locale (Ollama, llama.cpp, LM Studio) usano una scheda AMD Radeon RX 7800 XT da 16 GB su Windows 11?
  2. Quale dà al motore, sulla stessa chiamata compatibile con OpenAI, le tre cose che servono: l'uscita vincolata a uno schema, la probabilità dei token, le immagini?
  3. Quali modelli stanno in 16 GB, e con quale licenza?
  4. Che cosa si misura sul computer di sviluppo e che cosa solo sul server?
  5. Quale prima prova si propone, e che cosa deve fare una persona per avviarla?
- **Cosa aggiorna**:
  - [ricerca/48 §6.2](48-modelli-locali-e-gpu.md), che fa girare la prova dei modelli locali sulla RTX 4000 del server. Qui la prima parte della prova si sposta sul computer di sviluppo; velocità e memoria restano da misurare sul server.
  - [ricerca/48 §2c](48-modelli-locali-e-gpu.md) e [ricerca/13 §2.1](13-modelli-open-source-sul-server.md) su Ministral 3 8B, che lì era «non verificato»: licenza e italiano ora sono verificati (§5).
  - Le decisioni di partenza sono in [ADR-0025](../docs/adr/0025-un-modello-per-agente.md) (un modello per agente) e [ADR-0027](../docs/adr/0027-decisore.md) (il decisore).
- **Legenda**:
  - `[verificato: fonte, data]`: letto sulla fonte indicata, o letto sul computer con un comando di sola lettura;
  - `[non verificato: motivo]`: stima, calcolo, o dato che la fonte primaria non conferma;
  - `[proposta]`: una scelta di disegno di questo rapporto.
- **Cosa non ho fatto**: niente installazioni, nessun modello scaricato, nessun processo avviato. Sul computer ho usato solo comandi di sola lettura; nella repo del codice ho solo letto file. Nessuna velocità di questo rapporto è misurata sui modelli candidati.

### Parole usate spesso

- **Probabilità dei token** (in inglese *logprobs*): per ogni pezzo di parola (token) che il modello scrive, quanto era probabile e quali altri erano possibili. Serve al decisore per leggere quanto il modello è sicuro, invece di chiederglielo ([ricerca/47](47-modelli-system-one.md)).
- **Uscita vincolata a uno schema**: il programma obbliga il modello a scrivere un JSON che rispetta uno schema dato. Nell'API di OpenAI è `response_format` con `json_schema`.
- **API compatibile con OpenAI**: l'indirizzo `/v1/chat/completions`, che parla come l'API di OpenAI. Il nostro adattatore `compatibile_openai` usa questo.
- **Vulkan** e **ROCm**: due modi di far calcolare una scheda AMD. Vulkan è un'interfaccia grafica generale, che funziona su molte schede. ROCm è la piattaforma di calcolo di AMD; su Windows si chiama HIP SDK.
- **`llama-server`**: il server HTTP di llama.cpp.
- **GGUF, mmproj, quantizzazione**: come in [ricerca/48](48-modelli-locali-e-gpu.md). Q4_K_M e Q4_0 sono quantizzazioni a circa 4 bit.
- **Slot**: le richieste che il server tiene aperte insieme. Ognuna ha il suo contesto.
- **Ragionamento** (in inglese *thinking*): alcuni modelli scrivono prima un pensiero e poi la risposta. Il pensiero consuma token.
- **Lettura e scrittura**, in token al secondo: la lettura è il testo in ingresso che il modello elabora; la scrittura è la risposta che genera.

---

## In breve

1. **Tutti e tre i programmi usano la RX 7800 XT su Windows.** Ollama la elenca fra le schede ROCm e usa Vulkan come strada di riserva, accesa da sola. llama.cpp pubblica un pacchetto Vulkan e uno ROCm per Windows. LM Studio è già installato su questo computer, con i motori ROCm e Vulkan (§3).
2. **Ciò che distingue i tre è la probabilità dei token sulla chiamata che il motore usa già.** `llama-server` accetta `logprobs` e `response_format` con `json_schema` su `/v1/chat/completions`: l'ho letto nel codice. Ollama ha le probabilità solo sulla sua API; la pagina della sua API compatibile le segna come non supportate. LM Studio le documenta solo su `/v1/responses` (§4).
3. **La proposta per la prima prova è `llama-server` col pacchetto Vulkan, in ascolto su 127.0.0.1:8080** [proposta]. È l'indirizzo che il registro dei modelli dà già al fornitore `casa`. È lo stesso motore che [ricerca/13](13-modelli-open-source-sul-server.md) e [ricerca/48](48-modelli-locali-e-gpu.md) consigliano per il server. È uno zip, senza installazione, con la versione fissata (§8).
4. **Modelli: Qwen3.5-9B in Q4_K_M con il file della vista come primo** (5,68 GB più 918 MB), **Ministral 3 8B come secondo** (dichiara l'italiano), **Gemma 4 E4B come terzo** (piccolo, vede e ascolta) [proposta]. Tutti Apache-2.0. Insieme sono circa 18 GB da scaricare (§5).
5. **Su questa scheda un 7B in Q4_0 scrive a circa 125 token al secondo** (classifica Vulkan di llama.cpp). La RTX 4000 del server fa 67,6 sulla stessa prova. Le velocità non si trasferiscono al server; il JSON valido, le probabilità e la qualità dei campi sì, se il file del modello è lo stesso [non verificato: stima] (§6).
6. **Qwen3.5 «pensa» da solo, se non lo si spegne.** Il server va avviato con il ragionamento spento, altrimenti i token del pensiero consumano `max_tokens` [verificato: scheda di Qwen3.5-9B e opzione `--reasoning` di `llama-server`, 12/11/2026].
7. **Due cose del codice di oggi vanno decise nello spec.** `SERSAN_MODELLI_URL_BASE` manda tutti i fornitori allo stesso indirizzo, quindi non si possono avere insieme il copione per Claude e un modello vero in casa. Il fornitore `compatibile_openai` non chiede le probabilità dei token (§7).
8. **Sul computer di sviluppo vanno solo dati di prova.** Il colore massimo di `casa` è giallo, ma lì «casa» è il computer di Alberto, non il server (§2).
9. **Nessuna fonte citabile misura l'italiano di Qwen3.5-9B o di Gemma 4.** C'è solo MMMLU, che contiene l'italiano mescolato ad altre 13 lingue. La prova in italiano va fatta da noi (§5).

---

## 1. Il computer di sviluppo

| Parte | Cosa c'è | Stato |
|---|---|---|
| Processore | AMD Ryzen 7 7800X3D, con una grafica integrata che Windows vede come «AMD Radeon(TM) Graphics» | [verificato: comando di sola lettura sulle schede video, 12/11/2026] |
| Memoria | 31 GB di RAM | [verificato: stesso giorno] |
| Scheda dedicata | AMD Radeon RX 7800 XT, 16 GB (architettura RDNA3, sigla gfx1101) | [verificato: comando di sola lettura; sigla dalla pagina AMD, 12/11/2026] |
| Sistema | Windows 11 Pro, build 22631 (cioè 23H2) | [verificato: sistema della sessione, 12/11/2026] |

Tre cose contano per la prova:
- **Le schede video sono due.** Un programma che usa Vulkan può prendere la grafica integrata invece della RX 7800 XT. Va scelta a mano la scheda dedicata (§3, §8).
- **AMD dà la RX 7800 XT come supportata dall'HIP SDK 7.2.0 per Windows**, sia per l'esecuzione sia per lo sviluppo, solo su Windows 11. La versione convalidata è la 22H2; questo computer ha la 23H2 [verificato: rocm.docs.amd.com, pagina del 31/07/2026, letta il 12/11/2026].
- **Il driver della scheda** non l'ho confrontato con il requisito di Ollama, «AMD ROCm v7 / HIP7-capable» [non verificato: confronto non fatto].

**Già installato**: LM Studio, con i motori ROCm e Vulkan [verificato: comando di sola lettura, 12/11/2026].

---

## 2. Perché provare qui, e con quali dati

**Che cosa chiedono le fonti alla milestone 2**:
- Un agente della corsia N gira su un modello open-weight, servito sul nostro server o da un fornitore [verificato: PRD, «Milestone di consegna», 12/11/2026].
- La prova risponde alla domanda «regge i passi della corsia N, e quale scheda serve?» [verificato: PRD, «Domande aperte», 12/11/2026].
- Il cambio di modello di un agente è una riga del registro; senza valutazione la terna torna a L1 [verificato: [ADR-0025](../docs/adr/0025-un-modello-per-agente.md); spec della milestone 1 §11.2, 12/11/2026].
- I modelli locali entrano prima nella corsia N; le sessioni S restano su Claude finché una prova non dice altro [verificato: ADR-0025; PRD, «Perimetro», 12/11/2026].
- Le misure si fissano prima della prova; ogni risposta locale si confronta con Haiku 5.5 o Sonnet 5.5 sugli stessi casi verdi [verificato: [ricerca/48 §6.2](48-modelli-locali-e-gpu.md), dove è una proposta].
- I modelli che vedono e ascoltano arrivano nella milestone 2. Le capacità `immagini` e `audio` si dichiarano nel registro solo dopo la verifica sulla pagina ufficiale [verificato: spec della milestone 1 §4.8.3; registro dei modelli, 12/11/2026].
- Un dato rosso non esce dal server per «avere un modello che vede» [verificato: ADR-0025, aggiornamento del 10/11].
- Il decisore, con un modello in casa, deve leggere la probabilità dai token, non quella dichiarata dal modello [verificato: [ricerca/13 §2.3](13-modelli-open-source-sul-server.md); [ricerca/47, parte 1](47-modelli-system-one.md); PRD, «Domande aperte»].
- Per i criteri d'ingresso, il decisore in casa deve rispondere entro 200 ms, 95 volte su 100. La revisione dell'11/11 fa dei due criteri di sicurezza l'obiettivo delle soglie; gli altri, tempi compresi, si misurano e si registrano [verificato: [ADR-0027](../docs/adr/0027-decisore.md)].

**Dove le fonti fanno la prova**: nessuna fonte del progetto chiede di provare sul computer di sviluppo. Le fonti pensano alla RTX 4000 del server, che oggi ha meno di 1 GB libero [verificato: ricerca/48 §6.2]. Il computer con la RX 7800 XT è una strada nuova, utile finché il server non è pronto.

**Quali dati**: solo dati di prova. Nel registro il fornitore `casa` riceve al massimo il giallo («rosso solo dopo la milestone 5») [verificato: registro dei modelli e spec della milestone 1 §4.8.3, 12/11/2026]. Ma quel colore pensa al server: durante questa prova «casa» è il computer di Alberto.

---

## 3. I tre programmi a confronto

| | **Ollama** | **llama.cpp (`llama-server`)** | **LM Studio** |
|---|---|---|---|
| **RX 7800 XT su Windows** | nell'elenco delle schede ROCm per Windows, insieme a 7900 XTX, 7900 XT, 7900 GRE, 7700 XT, 7600 XT, 7600; chiede un driver «AMD ROCm v7 / HIP7-capable» | pacchetti Windows pronti per Vulkan e per ROCm 10.0 | i requisiti non parlano di AMD, Vulkan o ROCm; su questo computer ci sono i motori ROCm e Vulkan |
| **Vulkan** | acceso da solo «when the backend is installed»; si spegne con `OLLAMA_VULKAN=0`; `GGML_VK_VISIBLE_DEVICES` sceglie la scheda | pacchetto `llama-…-bin-win-vulkan-x64.zip` | il motore Vulkan installato è più vecchio di quello ROCm |
| **ROCm** | pacchetto a parte `ollama-windows-amd64-rocm.zip` | pacchetto `llama-…-bin-win-rocm-10.0-x64.zip`; su Windows con HIP `HSA_OVERRIDE_GFX_VERSION` non funziona | motore ROCm installato |
| **Come si installa** | installazione nella cartella dell'utente, senza diritti di amministratore; almeno 4 GB per il programma; Windows 10 22H2 o successivo | zip da scompattare, nessuna installazione | già installato; requisiti: AVX2, 16 GB di RAM e 4 GB di VRAM consigliati |
| **Versione** | stabile v0.40.16 del 9 novembre; anteprima v0.40.17 del 10 novembre | b12327 del 12 novembre, segnata «Pre-release»; quale tag recente non lo è va controllato | ultima per Windows 0.4.28; sul computer ce n'è una più vecchia |
| **Indirizzo** | `http://localhost:11434` | predefinito 127.0.0.1, porta **9931** (`LLAMA_ARG_PORT`); 8080 solo negli esempi Docker | porta 1234 negli esempi |
| **Licenza** | MIT | MIT | gratuito anche al lavoro dall'8 luglio 2025 |
| **Rischi** | cambia da solo con gli aggiornamenti | il multimodale è segnato «experimental»; Qwen3.5 su Vulkan ha segnalazioni aperte | una segnalazione: i motori ROCm di LM Studio 0.3.39 non caricavano i modelli su una RX 7800 XT |

Stato delle righe:
- Ollama [verificato: docs.ollama.com/gpu, docs.ollama.com/windows, github.com/ollama/ollama/releases, 12/11/2026; licenza da api.github.com/repos/ollama/ollama]. «Cambia da solo con gli aggiornamenti» [non verificato: non controllato].
- llama.cpp [verificato: github.com/ggml-org/llama.cpp/releases, README del server, docs/build.md, 12/11/2026]. Le dimensioni degli zip non sono scritte [non verificato]. Nell'esempio di compilazione HIP c'è gfx1100 (7900 XTX, XT, GRE); la RX 7800 XT è gfx1101 [verificato: docs/build.md].
- LM Studio [verificato: lmstudio.ai/docs/app/system-requirements, lmstudio.ai/download, lmstudio.ai/blog/free-for-work, 12/11/2026; motori dalla cartella del programma sul computer]. La porta predefinita [non verificato: le pagine lette mostrano solo esempi]. «Non è open source» [non verificato]. La segnalazione sui motori ROCm [non verificato: github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1395, letto solo il riassunto di una ricerca].
- Qwen3.5 su Vulkan: Qwen3.5 usa un'operazione nuova, GATED_DELTA_NET. Su Vulkan è entrata nella b8317; ci sono segnalazioni di lentezza su AMD (#20354) e di uscite rovinate su Android (#20603) [non verificato: letti solo i riassunti di una ricerca, non le pagine].
- Vulkan in Ollama: nella 0.12.11 arrivò come opzione da accendere (`OLLAMA_VULKAN=1`); oggi è acceso da solo [verificato: note della v0.12.11 e docs.ollama.com/gpu, 12/11/2026]. In quale versione è cambiato [non verificato: non trovato].
- Su questo computer, con la grafica integrata e la scheda dedicata: se Vulkan prende la integrata, Ollama chiede di impostare `GGML_VK_VISIBLE_DEVICES` sull'indice della scheda dedicata [verificato: docs.ollama.com/windows, 12/11/2026].

---

## 4. Le funzioni che servono al motore, e chi le ha

### 4.1 Che cosa manda oggi il motore

Nella repo del codice [verificato: registro dei modelli, adattatore `compatibile_openai`, cliente dei modelli e decisore su modello, letti il 12/11/2026]:
- Il fornitore `casa` è `compatibile_openai` su `http://127.0.0.1:8080/v1`, senza chiave, con `colore_massimo: giallo`.
- Nel registro c'è `qwen3-4b` su `casa`, con la sola capacità `testo`.
- L'adattatore chiama `<url_base>/chat/completions`. In `model` manda il nome del registro. Manda `response_format` con `json_schema` e `strict: true`, le immagini come `image_url` in base64, l'audio come `input_audio`. Rifiuta i `tool_calls`. **Non chiede le probabilità dei token.**
- `SERSAN_MODELLI_URL_BASE` sostituisce l'`url_base` di **tutti** i fornitori. Senza di lei, un agente attivo su `anthropic` senza chiave ferma il motore.
- Il decisore su modello chiede la probabilità dentro il JSON di risposta: è la probabilità **dichiarata**. Lo spec lo segna fra le cose aperte.
- Ogni chiamata ha un tetto di 60 secondi (spec della milestone 1 §4.8.1).

### 4.2 Chi dà che cosa sulla chiamata compatibile

| Funzione | `llama-server` | Ollama | LM Studio |
|---|---|---|---|
| **Schema JSON** su `/v1/chat/completions` | sì: accetta `json_object` e la forma di OpenAI `{"type":"json_schema","json_schema":{"name","strict","schema"}}` | `response_format` sì; la pagina sull'uscita a schema non nomina `json_schema` con `strict`; lo schema va nel campo `format` dell'API sua | sì, in `response_format.json_schema`; per i GGUF usa la grammatica di llama.cpp; avvisa che i modelli sotto 7B spesso non reggono l'uscita a schema |
| **Probabilità dei token** su `/v1/chat/completions` | sì: `logprobs: true` diventa `n_probs`, con `top_logprobs` a 20 se manca; rifiutate solo con strumenti più streaming | **no** secondo la pagina di oggi; sì su `/api/chat` (`logprobs`, `top_logprobs`) | non documentate: la pagina elenca 13 parametri, senza probabilità; `top_logprobs` solo su `/v1/responses`, dalla 0.3.39 |
| **Immagini** | `image_url` in base64, per URL o da file locale; serve `--mmproj`; il README chiama il multimodale «experimental» | sì, solo in base64, non per URL | `image_url` dalla 0.3.39 |
| **Audio** (`input_audio`) | il README parla di audio solo nel campo `multimodal_data` di `/completion` | non documentato sull'API compatibile | non letto |
| **Altro** | su `/completion`, `n_probs` dà le probabilità dei primi N token; `post_sampling_probs` le dà dopo il campionamento | non supportati `n`, `logit_bias`, `tool_choice` | `/v1/decisions`: «Answer typed questions with a decision model»; serve un modello di decisione caricato; la pagina non dice se dà probabilità |

Stato:
- `llama-server` [verificato: tools/server/README.md e tools/server/server-common.cpp, funzione `oaicompat_chat_params_parse`, 12/11/2026].
- Ollama [verificato: docs.ollama.com/api/openai-compatibility, docs.ollama.com/api/chat, docs.ollama.com/capabilities/structured-outputs, 12/11/2026]. `json_schema` con `strict` [non verificato: la pagina non lo nomina].
- LM Studio [verificato: lmstudio.ai/docs/developer/openai-compat e le pagine chat-completions, structured-output, decisions; changelog della 0.3.39, 12/11/2026].
- Le opzioni di `llama-server` che servono alla prova: `--reasoning on/off/auto` (predefinito auto), `--reasoning-budget` (predefinito -1), `--chat-template-kwargs`; `--jinja` acceso per default; `-c 0` prende il contesto dal modello; `-np -1` sceglie da solo il numero di slot; `--api-key` facoltativa; `--list-devices` e `--device` per scegliere la scheda [verificato: README del server, tabella delle opzioni, 12/11/2026].

**Cosa ne ricavo**: solo `llama-server` dà lo schema e le probabilità dei token sulla stessa chiamata che il motore usa già. Con Ollama le probabilità ci sono, ma su un'altra API. Con LM Studio, sulla chat non sono documentate.

**Un contrasto da tenere presente**: le note di Ollama 0.12.11 scrivono «Ollama's API and OpenAI-compatible API now support log probabilities»; la pagina di oggi dell'API compatibile le segna come non supportate [verificato: le due pagine, 12/11/2026]. Quale delle due vale oggi va provato.

---

## 5. I modelli candidati

| Modello | File Q4 | File della vista | Vede e ascolta | Licenza | Italiano | Stato |
|---|---|---|---|---|---|---|
| **Qwen3.5-9B** | Q4_K_M 5,68 GB (anche Q5_K_M 6,58; Q6_K 7,46; Q8_0 9,53) | F16 918 MB | immagini e video | Apache-2.0 | «201 languages and dialects», l'italiano non è nominato; MMMLU 81,2 | [verificato: huggingface.co/Qwen/Qwen3.5-9B e unsloth/Qwen3.5-9B-GGUF, 12/11/2026] |
| **Ministral 3 8B Instruct 2512** | Q4_K_M 5,2 GB (anche Q5_K_M 6,06; Q8_0 9,03), GGUF ufficiale di Mistral | 858 MB | sì, immagini | Apache-2.0 | **dichiarato**, fra 11 lingue | [verificato: huggingface.co/mistralai/Ministral-3-8B-Instruct-2512 e la versione GGUF, 12/11/2026] |
| **Gemma 4 E4B** | Q4_0 4,59 GB (ggml-org) | Q8_0 560 MB, oppure BF16 992 MB | immagini; audio fino a 30 s | Apache-2.0 | «35+ languages» per la famiglia, l'italiano non è nominato | [verificato: huggingface.co/ggml-org/gemma-4-E4B-it-GGUF; huggingface.co/google/gemma-4-12B-it per le lingue della famiglia; llama.cpp docs/multimodal.md, 12/11/2026] |
| Gemma 4 12B | Q4_0 ufficiale 6,98 GB | 0,18 GB | immagini, audio 30 s | Apache-2.0 | MMMLU 83,4 % | [verificato: huggingface.co/google/gemma-4-12B-it, 12/11/2026]; **non** è nell'elenco multimodale di llama.cpp |
| Qwen3-4B | — | — | no | Apache-2.0 | — | è il modello del board di Michele, in Ollama [verificato: [ricerca/33](33-costi-v2.md) e [ricerca/48 §2c](48-modelli-locali-e-gpu.md)]; il file GGUF ufficiale [non verificato] |

Note sui modelli:
- **Qwen3.5-9B pensa per default.** Si spegne con `chat_template_kwargs: {"enable_thinking": false}`; i comandi `/think` e `/nothink` non ci sono. Senza ragionamento la scheda consiglia temperatura 0,7 e top_p 0,8. Il contesto nativo è di 262.144 token [verificato: huggingface.co/Qwen/Qwen3.5-9B, 12/11/2026].
- **Qwen3.5-9B ha 32 strati**, di cui 8 di attenzione e 24 Gated DeltaNet: la cache del contesto è piccola [verificato: stessa pagina; [ricerca/13 §2.2](13-modelli-open-source-sul-server.md)]. Quanta memoria occupa a 32k token [non verificato: da misurare].
- **Gemma 4 E4B** è nell'elenco multimodale di llama.cpp sia fra i modelli che vedono sia fra quelli misti (vista e audio); Gemma 4 12B non c'è [verificato: docs/multimodal.md, 12/11/2026].
- **Ministral 3 8B** è risultato il migliore fra i modelli provati nell'articolo ITALIC del maggio 2026, con 87,4 % [non verificato: visto solo nel riassunto di una ricerca web].
- **Con Ollama** i nomi e le misure cambiano: `qwen3.5:9b` da 6,6 a 7,6 GB, `qwen3.5:4b` da 3,3 a 4,0 GB, `gemma4:e4b` da 6,6 a 9,5 GB, `gemma4:12b` da 7,7 a 8,0 GB; tutti «Text, Image». La pagina non scrive la licenza [verificato: ollama.com/library/qwen3.5 e ollama.com/library/gemma4, 12/11/2026].
- **Un modello che non sta nei 16 GB**: Qwen3.6-35B-A3B (IQ4_XS 17,7 GB). Si potrebbe provare solo con gli esperti nei 31 GB di RAM [non verificato: stima da [ricerca/48 §2h](48-modelli-locali-e-gpu.md)].

**L'italiano**:
- MMMLU contiene l'italiano (IT_IT) fra 14 lingue [verificato: huggingface.co/datasets/openai/MMMLU, 12/11/2026]. Il punteggio MMMLU quindi non misura l'italiano da solo.
- Nessuna classifica italiana ha Qwen3.5-9B o Gemma 4. Nelle ricerche EVALITA-LLM non mostra risultati per loro. Il confronto su EngGPT2 (arXiv 2605.07731) prova Gemma 3 12B e Qwen3-8B, non Qwen3.5 né Gemma 4 [verificato: arxiv.org/abs/2605.07731, 12/11/2026; [ricerca/48 §2c](48-modelli-locali-e-gpu.md)].

---

## 6. Velocità e memoria: che cosa si trasferisce al server

### 6.1 I numeri pubblici

| Scheda | Prova | Scrittura | Lettura | Stato |
|---|---|---|---|---|
| RX 7800 XT, Vulkan, senza flash attention | Llama 2 7B Q4_0 | 118,27 token/s | 2.017 token/s | [verificato: github.com/ggml-org/llama.cpp/discussions/10879, commit 4fdbc1e, data non scritta, letto il 12/11/2026] |
| RX 7800 XT, Vulkan, con flash attention | stessa | 124,86 token/s | 2.197 token/s | stessa fonte |
| Quadro RTX 4000 del server, CUDA | stessa | 67,6 token/s | 1.663 token/s | [verificato da [ricerca/13 §3.1](13-modelli-open-source-sul-server.md): classifica CUDA, discussion 15013, con un'altra versione di llama.cpp; nella 10879 la RTX 4000 non c'è] |

Che cosa se ne ricava, tutto [non verificato: stima]:
- Su un 7B la RX 7800 XT scrive circa 1,8 volte più veloce della RTX 4000 (calcolo sulle due righe).
- Qwen3.5-9B Q4_K_M dovrebbe scrivere a circa 70-85 token al secondo, Ministral 3 8B Q4_K_M a circa 80-90. È una proporzione sui byte letti per token, dalla riga della RX 7800 XT; non tiene conto delle operazioni DeltaNet su Vulkan.
- Pesi più vista di Qwen3.5-9B fanno 6,6 GB: nei 16 GB resta posto per un contesto di 32k e più slot.

Misure pubblicate di Qwen3.5-9B, Ministral 3 8B o Gemma 4 sulla RX 7800 XT non ne ho trovate (ricerca del 12/11/2026).

### 6.2 Che cosa vale anche per il server e che cosa no

Le due prove, qui e sul server, possono usare gli stessi file GGUF. Per questo [non verificato: stima]:

| Si trasferisce al server | Non si trasferisce |
|---|---|
| il collegamento: l'adattatore `compatibile_openai` resta lo stesso, cambia solo l'indirizzo | la velocità in token al secondo: altra scheda, altro motore di calcolo (Vulkan su AMD contro CUDA su NVIDIA) |
| la percentuale di JSON validi | la memoria occupata: la RTX 4000 ha 8 GB, oggi con meno di 1 GB libero |
| se le probabilità dei token arrivano | i tempi del decisore (l'obiettivo di 200 ms) |
| la qualità dei campi in italiano | i problemi propri di Qwen3.5 su Vulkan con AMD |

La memoria misurata qui serve comunque: dice se lo stesso modello, con 32k di contesto e due slot, può stare negli 8 GB della RTX 4000 [non verificato: stima].

### 6.3 I fatti del server da ricordare

- Il server ha una Quadro RTX 4000 (Turing, compute capability 7.5, 8 GB, niente BF16); sulla RTX 4000 lo stack giusto è llama.cpp [verificato da [ricerca/13 §0 e §4](13-modelli-open-source-sul-server.md) e [ricerca/48 §2](48-modelli-locali-e-gpu.md)].
- Sugli 8 GB della RTX 4000 il 9B con la vista è al limite; oggi la scheda ha meno di 1 GB libero [verificato da ricerca/48 §2c e §6.2].
- Il board di Michele fa già girare Ollama con Qwen3-4B [verificato da [ricerca/33](33-costi-v2.md)].
- Ollama chiede per NVIDIA una compute capability 5.0 o più e un driver 550 o più (570 per le 5.0-6.2) [verificato: docs.ollama.com/gpu, 12/11/2026].
- llama.cpp pubblica pacchetti Linux `ubuntu-cuda-12.8`, `ubuntu-cuda-13.5` e `ubuntu-vulkan` [verificato: release b12327, 12/11/2026]. Se CUDA 13.5 regge ancora Turing [non verificato: non controllato].
- La RTX PRO 2000 Blackwell chiede CUDA 12.8 o più; Ollama è compilato per Blackwell dalla 0.5.13 [verificato da ricerca/48 §2 e [ricerca/37](37-hardware-risposte-michele.md)].
- Sul server con Ollama cambierebbero porta (11434) e probabilità dei token, che su `/v1` mancano [non verificato: stima].

---

## 7. Che cosa va deciso nello spec

Per ogni punto le strade lette e la proposta. Le scelte restano allo spec.

1. **Dove gira la prima prova.**
   - A. Sul computer di sviluppo con la RX 7800 XT. Pro: c'è oggi, ha 16 GB, è veloce. Contro: non è il server; velocità e memoria non si trasferiscono.
   - B. Sulla RTX 4000 del server. Pro: è il posto vero. Contro: il server non è pronto e la scheda è piena.
   - C. Da un fornitore via API (`terzo-openweight`). Pro: nessun hardware. Contro: servono un account e una chiave; solo dati verdi e gialli.
   - **Proposta: A subito, per l'adattatore, il JSON, le probabilità e la qualità in italiano; poi B per velocità e memoria** [proposta].
2. **Quale programma.**
   - A. `llama-server` con Vulkan. Pro: probabilità e `json_schema` sulla stessa chiamata OpenAI; zip senza installazione; versione fissata; stesso motore consigliato per il server. Contro: la scheda si sceglie a mano; il multimodale è «experimental».
   - B. Ollama. Pro: un comando per scaricare e servire; il board lo usa già. Contro: su `/v1` le probabilità sono segnate come non supportate.
   - C. LM Studio. Pro: già installato. Contro: probabilità documentate solo su `/v1/responses`; il motore Vulkan installato è vecchio.
   - **Proposta: A.** LM Studio serve come controllo rapido, se Alberto vuole vedere un modello girare prima di scaricare llama.cpp [proposta].
3. **Vulkan o ROCm.**
   - Vulkan. Pro: per gli zip pronti non serve un SDK [non verificato]; è l'unica strada documentata da tutti e tre; ci sono misure pubbliche sulla RX 7800 XT. Contro: Qwen3.5 su Vulkan ha segnalazioni aperte su AMD [non verificato].
   - ROCm. Pro: supporto ufficiale AMD per la RX 7800 XT. Contro: lo zip di llama.cpp è per ROCm 10.0 e il driver va controllato; c'è la segnalazione su LM Studio con ROCm e RX 7800 XT.
   - **Proposta: Vulkan per la prima prova; ROCm solo se Qwen3.5 va male su Vulkan** [proposta].
4. **Quali modelli.**
   - Qwen3.5-9B: consigliato da ricerca/48 per il server, vede, ha punteggi di documento alti. Ma l'italiano non è dichiarato, pensa per default e usa operazioni nuove su Vulkan.
   - Ministral 3 8B: italiano dichiarato, GGUF ufficiale, architettura classica. In ricerca/48 non è fra i consigliati: lì è segnato «non riletti oggi».
   - Gemma 4 E4B: piccolo, vista e audio in llama.cpp; candidato per il decisore e per il modello piccolo. L'audio arriva solo a 30 secondi.
   - **Proposta: tutti e tre, in quest'ordine.** Qwen3.5-9B è il riferimento; Ministral la riserva per l'italiano; Gemma 4 E4B fa la prova del modello piccolo e del decisore con le probabilità. Qwen3-4B si aggiunge se la prova deve confrontare il modello che già gira nel board [proposta].
5. **Come il motore parla al modello vero mentre Claude resta a copione** (il copione, e come estenderlo per la corsia S, sono in [ricerca/50 §4.3](50-agent-sdk-e-prova-a-copione.md)).
   - A. Una variabile per fornitore, per esempio `SERSAN_MODELLI_URL_BASE_CASA`. Pro: cambio piccolo. Contro: una variabile in più.
   - B. Un comando di prova a parte, che usa il cliente dei modelli solo con agenti `casa`. Pro: non tocca il motore. Contro: non prova il giro intero.
   - **Proposta: A**, perché la prova deve passare dal runner vero, con colore, capacità e registro [proposta].
6. **Porta e nome del modello.**
   - Il registro ha già 8080; il predefinito di `llama-server` oggi è 9931. 8080 non è fra le porte che usa lo sviluppo (4100, 4200, 4300, 4310, 4900 e PostgreSQL; il copione è su 4900, spec della milestone 1 §4.8.3).
   - Il nome mandato in `model` è la chiave del registro: con `llama-server` basta `--alias`; con Ollama il nome ha i due punti (`qwen3.5:9b`).
   - **Proposta: 8080 e `--alias` uguale alla chiave del registro. Lo spec scrive che una porta occupata ferma la prova, non la sposta da sola** [proposta].
7. **Come il decisore legge la probabilità.**
   - A. Le probabilità sulla stessa chiamata a schema: si cerca, nell'elenco dei token, il token del valore della risposta. Pro: una chiamata. Contro: con lo schema i primi token sono `{"`; e non si sa se le probabilità sono prima o dopo il filtro della grammatica [non verificato: nessuna fonte lo dice].
   - B. Una chiamata senza schema, che chiede solo la prima parola; si leggono le probabilità di quelle opzioni, come in [ricerca/13 §2.3](13-modelli-open-source-sul-server.md). Pro: semplice da tarare. Contro: una chiamata per domanda.
   - **Proposta: B per la prova, A misurata accanto.** Il campo «probabilità» dentro il JSON resta per Claude [proposta].
   - Il 12 novembre la revisione di [ADR-0027](../docs/adr/0027-decisore.md) ha scelto B: un decisore in casa che legge la probabilità della prima parola. Nella milestone 2 la taratura riguarda il controllo del contenuto e le risposte degli esterni; Jev, con LiteLLM, entra nella milestone 3.
8. **Il ragionamento dei modelli.**
   - **Proposta: spento per la corsia N e per il decisore** (`--reasoning off`, oppure `chat_template_kwargs`). Pro: tempi prevedibili, `max_tokens` non consumati. Contro: forse meno qualità sui riassunti; si misura con e senza su 10 casi [proposta].
9. **Le soglie.** Le fissa lo spec prima della prova, come chiede [ricerca/48 §6.2](48-modelli-locali-e-gpu.md). Il §8.4 dice quali hanno già un valore nelle fonti.

---

## 8. La proposta per la prima prova

Tutto il paragrafo è [proposta]. Nessuno ha installato o scaricato niente: installare e scaricare lo decide Alberto.

### 8.1 Programma, modelli, porta

- **Programma**: `llama-server` di llama.cpp, pacchetto Vulkan per Windows, con la versione fissata.
- **Modelli**, in ordine: Qwen3.5-9B Q4_K_M con la vista F16; poi Ministral 3 8B Q4_K_M con la vista; poi Gemma 4 E4B Q4_0 con la vista Q8_0.
- **Indirizzo**: solo 127.0.0.1, porta 8080, come nel registro; `--alias` uguale alla chiave del registro.
- **Scheda**: la RX 7800 XT, scelta a mano dopo aver letto l'elenco delle schede.
- **Ragionamento**: spento.

### 8.2 I comandi

Li esegue una persona, in PowerShell. `$P` è la cartella della prova, che sceglie Alberto. Il tag `b12327` è un'anteprima: prima conviene prendere dalla pagina delle versioni l'ultimo tag che non lo è, e metterlo al suo posto.

```powershell
# 0. Cartella della prova e versione di llama.cpp (da scegliere)
$P   = "<cartella della prova>"
$TAG = "b12327"   # anteprima: sostituire con l'ultimo tag non in anteprima

# 1. Cartelle e programma (zip Vulkan, nessuna installazione)
New-Item -ItemType Directory -Force "$P\bin", "$P\modelli"
curl.exe -L -o "$P\llama-vulkan.zip" "https://github.com/ggml-org/llama.cpp/releases/download/$TAG/llama-$TAG-bin-win-vulkan-x64.zip"
Expand-Archive "$P\llama-vulkan.zip" -DestinationPath "$P\bin"

# 2. Quale scheda vede Vulkan (c'è anche la grafica integrata)
& "$P\bin\llama-server.exe" --list-devices

# 3. Modelli (circa 6,6 GB il primo)
curl.exe -L -o "$P\modelli\Qwen3.5-9B-Q4_K_M.gguf" https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/resolve/main/Qwen3.5-9B-Q4_K_M.gguf
curl.exe -L -o "$P\modelli\Qwen3.5-9B-mmproj-F16.gguf" https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/resolve/main/mmproj-F16.gguf
# poi, se serve:
curl.exe -L -o "$P\modelli\Ministral-3-8B-Q4_K_M.gguf" https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-GGUF/resolve/main/Ministral-3-8B-Instruct-2512-Q4_K_M.gguf
curl.exe -L -o "$P\modelli\Ministral-3-8B-mmproj.gguf" https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-GGUF/resolve/main/Ministral-3-8B-Instruct-2512-BF16-mmproj.gguf
curl.exe -L -o "$P\modelli\gemma-4-E4B-Q4_0.gguf" https://huggingface.co/ggml-org/gemma-4-E4B-it-GGUF/resolve/main/gemma-4-E4B-it-Q4_0.gguf
curl.exe -L -o "$P\modelli\gemma-4-E4B-mmproj-Q8_0.gguf" https://huggingface.co/ggml-org/gemma-4-E4B-it-GGUF/resolve/main/mmproj-gemma-4-E4B-it-Q8_0.gguf

# 4. Velocità, senza e con flash attention
& "$P\bin\llama-bench.exe" -m "$P\modelli\Qwen3.5-9B-Q4_K_M.gguf" -ngl 99 -fa 0,1

# 5. Server sulla porta del registro, solo su 127.0.0.1, ragionamento spento
#    (Vulkan0 va sostituito con il nome della scheda dedicata letto al passo 2)
& "$P\bin\llama-server.exe" -m "$P\modelli\Qwen3.5-9B-Q4_K_M.gguf" --mmproj "$P\modelli\Qwen3.5-9B-mmproj-F16.gguf" --host 127.0.0.1 --port 8080 --device Vulkan0 -ngl all -fa on -c 32768 -np 2 --reasoning off --alias qwen3.5-9b

# 6. Controllo, in un altro terminale
curl.exe http://127.0.0.1:8080/v1/models
```

Da sapere:
- Che `llama-bench` sia nello stesso zip [non verificato: da vedere dopo lo scompattamento].
- Gli indirizzi `resolve/main/...` seguono i nomi dei file letti il 12/11 sulle pagine dei repository; la forma dell'indirizzo è quella solita di Hugging Face [non verificato: da controllare al primo scaricamento].
- Il passo 6 con una richiesta vera (schema, `logprobs: true` e `top_logprobs: 5`) va scritto nello spec come piccolo script, per non dipendere dalle virgolette di PowerShell.

### 8.3 Spazio e tempo

**Spazio** [non verificato: stima sui file letti il 12/11/2026]:
- programma: da decine a poche centinaia di MB [non verificato: la pagina non scrive le dimensioni];
- Qwen3.5-9B con la vista: 6,6 GB; Ministral 3 8B con la vista: 6,1 GB; Gemma 4 E4B con la vista: 5,2 GB;
- in tutto circa 18 GB.

**Tempo** [non verificato: stima]:
- scaricare: circa 25 minuti a 100 Mbit/s, circa 3 minuti a 1 Gbit/s (la banda del computer non è nota);
- avvio e controlli: 15-30 minuti;
- velocità con `llama-bench`: 10 minuti per modello;
- prova di qualità: dipende dai casi pronti. Con 50 più 50 casi e tre modelli, mezza giornata di macchina, più il tempo di una persona per correggere.

### 8.4 Che cosa si misura, e con quali soglie

Le soglie le fissa lo spec **prima** della prova. Dove una fonte dà già un valore, lo riporto.

| N. | Misura | Come | Soglia |
|---|---|---|---|
| 1 | **Collegamento** | il fornitore `compatibile_openai` di oggi, senza modifiche, riceve da `llama-server` risposte che rispettano lo schema Zod, su un passo vero della corsia N | la fissa lo spec |
| 2 | **JSON valido** | percentuale di risposte che passano lo schema, su almeno 100 chiamate | la fissa lo spec |
| 3 | **Campi giusti in italiano** | post-call su 50 trascrizioni e smistamento su 50 mail, contro le risposte di una persona; con la chiave API anche contro Haiku 5.5 | per esempio 90 % dei campi giusti ([ricerca/48 §6.2](48-modelli-locali-e-gpu.md), dove è una proposta) |
| 4 | **Probabilità dei token** | arrivano sulla chiamata; per il decisore, calibrazione (ECE) e copertura su domande sì/no, con il metodo B del §7 punto 7 | la fissa lo spec |
| 5 | **Tempi** | lettura e scrittura in token al secondo (`llama-bench` e i tempi che `llama-server` restituisce); tempo di una chiamata del decisore | per il decisore in casa il criterio è 200 ms al 95° percentile, da misurare e registrare ([ADR-0027](../docs/adr/0027-decisore.md)); le altre le fissa lo spec |
| 6 | **Memoria** | VRAM usata con 32k di contesto e due slot, letta da Gestione attività; serve a capire se lo stesso modello sta negli 8 GB della RTX 4000 | la fissa lo spec |
| 7 | **Vista** | 10 immagini di prova (schermate e slide): il modello risponde, e la capacità `immagini` si può dichiarare nel registro | la fissa lo spec |
| 8 | **Ragionamento acceso o spento** | 10 casi con e 10 senza, per vedere quanto cambiano qualità e tempi | la fissa lo spec |
| 9 | **Stabilità di Qwen3.5 su Vulkan** | uscite rovinate su 100 chiamate | nessuna uscita rovinata; altrimenti si passa a Ministral o a ROCm |

---

## 9. Che cosa dipende da persone, chiavi o hardware

- **Installare e scaricare sul computer**: lo decide Alberto. Servono lo zip di llama.cpp e circa 18 GB di modelli.
- **Confronto con Haiku 5.5**: serve la chiave API di Anthropic, che oggi non c'è [verificato: PRD, «Domande aperte», bundle per startup, 12/11/2026]. Senza chiave il confronto si fa contro risposte scritte da una persona.
- **Dati di prova in italiano**: 50 trascrizioni e 50 mail, sintetiche oppure vere ma verdi, con i campi giusti scritti da una persona. Chi le scrive va deciso; le trascrizioni vere chiedono il consenso [verificato: [ricerca/48 §6.2](48-modelli-locali-e-gpu.md)].
- **Prova sul server**: il server non è pronto; la RTX 4000 è piena; la finestra va concordata con Michele [verificato: ricerca/48 §6.2; PRD, «Domande aperte»].
- **Seconda GPU**: la proposta della RTX PRO 2000 a Michele non è stata mandata; chi la manda lo decide Alberto [verificato: elenco delle attività nella repo del codice, 12/11/2026; [ADR-0025](../docs/adr/0025-un-modello-per-agente.md)].
- **Fornitore open-weight via API** (`terzo-openweight`): servono un account, una chiave e il sì di Michele sul fornitore per i dati gialli [verificato: [ADR-0027](../docs/adr/0027-decisore.md), «Chi decide»; ADR-0025].
- **Driver AMD per ROCm**: serve solo se Vulkan non basta; l'aggiornamento lo fa Alberto.

---

## 10. I buchi

Quello che le fonti non dicono, o dicono in modo diverso:
- **Probabilità dei token di Ollama sull'API compatibile**: le note della 0.12.11 dicono che ci sono; la pagina di oggi dice di no.
- **Porta di `llama-server`**: il registro e lo spec della milestone 1 presumono 8080; il README di oggi dice 9931.
- **Vulkan in Ollama**: nella 0.12.11 era da accendere, oggi è acceso da solo. La versione del cambio non l'ho trovata.
- **Qwen3.5 su Vulkan con AMD**: il supporto è entrato nella b8317, ma ci sono segnalazioni di lentezza e di uscite rovinate; non ho letto le segnalazioni intere.
- **Probabilità sotto una grammatica**: nessuna fonte dice se `llama-server` dà le probabilità prima o dopo il filtro dello schema.
- **`input_audio` su `/v1/chat/completions`**: il nostro adattatore lo usa; il README di `llama-server` parla di audio solo nel campo `multimodal_data` di `/completion`. Ollama non documenta l'audio sull'API compatibile.
- **Italiano**: nessuna misura citabile per Qwen3.5-9B e Gemma 4. Ministral 3 8B dichiara l'italiano; il risultato su ITALIC l'ho visto solo in un riassunto.
- **Velocità**: nessuno ha pubblicato misure di Qwen3.5-9B, Ministral 3 8B o Gemma 4 sulla RX 7800 XT; ci sono solo quelle su Llama 2 7B.
- **Dimensioni** degli zip di llama.cpp e del programma LM Studio: le pagine non le scrivono.
- **Versione stabile di llama.cpp**: la b12327 è un'anteprima; quale tag recente non lo è non l'ho controllato.
- **Driver AMD**: il driver del computer non l'ho confrontato con il requisito «ROCm v7 / HIP7».
- **CUDA 13.5 e Turing**: non ho verificato se i pacchetti CUDA 13.5 reggono ancora la RTX 4000.
- **LM Studio**: porta predefinita, ascolto solo su 127.0.0.1, autenticazione: le pagine lette non lo dicono. Le probabilità sulla chat non sono documentate. Se sia open source non l'ho verificato.
- **Ministral fra ricerca/13 e ricerca/48**: [ricerca/13 §2.1](13-modelli-open-source-sul-server.md) lo cita come non verificato; [ricerca/48 §2c](48-modelli-locali-e-gpu.md) scrive «non riletti oggi». Ora licenza e italiano sono verificati (§5).
- **Gemma 4 E4B e l'audio**: [ricerca/48 §2c](48-modelli-locali-e-gpu.md) dice che ascolta; la pagina di Ollama elenca per `gemma4:e4b` solo «Text, Image». L'elenco di llama.cpp lo dà con l'audio.
- **Qwen3-4B**: il file GGUF ufficiale non l'ho verificato.

---

## Fonti

**Pagine web, lette il 12/11/2026**
- Ollama: https://docs.ollama.com/gpu · https://docs.ollama.com/windows · https://docs.ollama.com/api/openai-compatibility · https://docs.ollama.com/api/chat · https://docs.ollama.com/capabilities/structured-outputs · https://github.com/ollama/ollama/releases · https://github.com/ollama/ollama/releases/tag/v0.12.11 · https://ollama.com/library/qwen3.5 · https://ollama.com/library/gemma4 · https://api.github.com/repos/ollama/ollama
- llama.cpp: https://github.com/ggml-org/llama.cpp/releases · https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md · https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/server/server-common.cpp · https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md · https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md · https://github.com/ggml-org/llama.cpp/discussions/10879 · https://api.github.com/repos/ggml-org/llama.cpp
- llama.cpp, Qwen3.5 su Vulkan (solo riassunti di una ricerca): https://github.com/ggml-org/llama.cpp/issues/20354 · https://github.com/ggml-org/llama.cpp/issues/20603 · https://github.com/ggml-org/llama.cpp/issues/19957 · https://newreleases.io/project/github/ggml-org/llama.cpp/release/b8317
- LM Studio: https://lmstudio.ai/docs/app/system-requirements · https://lmstudio.ai/docs/developer/openai-compat · https://lmstudio.ai/docs/developer/openai-compat/chat-completions · https://lmstudio.ai/docs/developer/openai-compat/structured-output · https://lmstudio.ai/docs/developer/openai-compat/decisions · https://lmstudio.ai/docs/developer/core/headless · https://lmstudio.ai/docs/developer/core/server · https://lmstudio.ai/changelog/lmstudio/lmstudio-v0.3.39 · https://lmstudio.ai/download · https://lmstudio.ai/blog/free-for-work · https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1395 (solo riassunto)
- AMD: https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html (pagina del 31/07/2026)
- Modelli: https://huggingface.co/Qwen/Qwen3.5-9B · https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/tree/main · https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512 · https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-GGUF/tree/main · https://huggingface.co/ggml-org/gemma-4-E4B-it-GGUF/tree/main · https://huggingface.co/google/gemma-4-12B-it · https://huggingface.co/datasets/openai/MMMLU · https://arxiv.org/abs/2605.07731 · https://arxiv.org/pdf/2605.07731 (solo riassunto, per ITALIC)

**Documenti della repo**
- [ricerca/13, modelli open source sul server, §0, §2, §3 e §4](13-modelli-open-source-sul-server.md)
- [ricerca/33, costi v2](33-costi-v2.md)
- [ricerca/37, hardware: risposte di Michele](37-hardware-risposte-michele.md)
- [ricerca/47, modelli System One, parte 1](47-modelli-system-one.md)
- [ricerca/48, modelli locali e GPU, §2, §4, §5 e §6](48-modelli-locali-e-gpu.md)
- [ricerca/50, l'Agent SDK e la prova a copione, §4.3](50-agent-sdk-e-prova-a-copione.md)
- [ADR-0025](../docs/adr/0025-un-modello-per-agente.md) · [ADR-0027](../docs/adr/0027-decisore.md) · [ADR-0028](../docs/adr/0028-instradamento-a-piu-motori.md)

**La repo del codice**, letta il 12/11/2026: il PRD («Perimetro», «Milestone di consegna», «Domande aperte», «Rischi»); lo spec della milestone 1 (§4.8.1, §4.8.2, §4.8.3, §11.2); il registro dei modelli; l'adattatore `compatibile_openai`; il cliente dei modelli; il decisore su modello; le direttive e l'elenco delle attività.

**Il computer di sviluppo**: comandi di sola lettura del 12/11/2026 sulle schede video, sui dischi, sui programmi installati e sui motori di LM Studio.
