# 31 · "Andrea" tutto in casa: l'agente vocale self-hosted (G5, G6, K10)

Rapporto del 25 ottobre 2026 per Alberto, Michele e Mattia. Sostituisce, per la sola voce di "Andrea", la parte ElevenLabs + Twilio descritta in `22-architettura-scelta.md`, in `PRESENTAZIONE-CEO.md` e la riga Twilio di `33-costi-v2.md`.

Legenda delle etichette:
- `[verificato: fonte]`: letto oggi su una pagina ufficiale, su un file del progetto o su una fonte secondaria indicata.
- `[non verificato]`: stima, deduzione o proposta di questo rapporto, oppure dato non confermato dalla fonte primaria.
- `non trovato`: il dato non è emerso dalle ricerche.

Prezzi rilevati il 25/10/2026, IVA esclusa salvo dove scritto. Cambio 1 $ = 0,8934 € `[verificato: LEGGIMI.md]`. Corrente a 0,35 €/kWh, come in `33-costi-v2.md` `[non verificato: ipotesi di 33-costi-v2 §2.4]`.

---

## In breve

"Andrea" si può fare tutto sul server di Michele, senza ElevenLabs e senza Twilio. La proposta è: **Asterisk 22 LTS** come centralino, **Pipecat** come motore della conversazione, un **numero italiano di Messagenet** come trunk SIP (30 € al mese, 2 linee), riconoscimento e sintesi vocale **con modelli a pesi aperti e licenza commerciale** in casa, e **Claude Haiku 5.5 via API**, dietro LiteLLM, **con il pensiero spento**. L'audio dei lead non esce più dall'azienda: verso Anthropic va solo il testo. Si parte **solo su CPU**, perché la RTX 4000 è piena e la sera va alla VM Experimental-1; la seconda GPU migliora voce e velocità ma non è necessaria per partire. Costo: **circa 47 € al mese** (contro circa 170 € della via ElevenLabs e circa 82 € della via Twilio), più **circa 24 giorni-persona** di lavoro. Le regole non cambiano: Andrea si dichiara AI nella prima frase, chiama solo chi ha dato il consenso nel modulo, e il Cancello blocca tutto il resto `[non verificato: proposta di questo rapporto; i singoli fatti sono nelle sezioni con le loro etichette]`.

Sei punti per decidere:

1. **La GPU attuale non basta per Andrea, e la sera non c'è.** La Quadro RTX 4000 da 8 GB porta già Qwen3-4B, embedding, reranker e Docling, e la sera passa a Experimental-1 `[verificato: board di Michele]`. Andrea deve rispondere 24 ore su 24 (G5, K10). Quindi la **fase 1 gira su CPU**: Pocket TTS di Kyutai (italiano, voce `giovanni`, pesi CC-BY-4.0, circa 200 ms al primo audio su CPU) e Parakeet TDT v3 in int8 per l'ascolto `[verificato: huggingface.co/kyutai/pocket-tts; huggingface.co/nvidia/parakeet-tdt-0.6b-v3]`. La qualità della voce italiana va ascoltata prima di decidere `[non verificato]`.
2. **Il pensiero di Claude va spento, o Andrea tace per secondi.** Haiku 5.5 ha il pensiero acceso di serie; misurato con il pensiero a effort "low", il primo token arriva dopo **6,58 secondi** `[verificato: artificialanalysis.ai/providers/anthropic]`. Haiku 5.5 accetta `thinking: {type: "disabled"}` a effort "high" o inferiore `[verificato: platform.claude.com, pagina Thinking]`. Il tempo al primo token senza pensiero non è ancora misurato da nessuno: `non trovato`. Riserva: Haiku 4.5, 0,48 s misurati, 10 volte più caro ma sempre pochi euro al mese `[verificato: artificialanalysis.ai; platform.claude.com pricing]`.
3. **Latenza realistica: 1,3-2,0 secondi** con GPU e **1,6-2,5 secondi** solo su CPU, dalla fine della frase del cliente al primo suono di Andrea `[non verificato: stima per fasi, §7]`. Più lenta di una piattaforma in cloud, ma accettabile per richiamare un lead se Andrea usa frasi brevi e un "certo, un attimo" pre-registrato.
4. **La seconda GPU cambia la qualità, non la fattibilità.** Una "A2000 Ada da 6 GB GDDR7" non esiste. Esistono RTX A2000 (Ampere, 6 o 12 GB GDDR6), RTX 2000 Ada (16 GB GDDR6) e RTX PRO 2000 Blackwell (16 GB GDDR7), tutte a 70 W; a 70 W ci sono anche RTX 4000 SFF Ada (20 GB) e RTX PRO 4000 Blackwell SFF (24 GB) `[verificato: computerbase.de, cgchannel.com, emarque.co, hardwaredealz.com]`. Consiglio una **16 GB** (circa 770-1.500 € oggi in Italia): ci stanno Andrea e tutta la pipeline RAG, e la RTX 4000 resta libera per Experimental-1 `[non verificato: stima]`.
5. **Il Registro delle opposizioni non blocca la richiamata in 90 secondi.** Il consenso dato **dopo** l'iscrizione al Registro resta valido `[verificato: secondaria, agendadigitale.eu 1/4/2022, su L. 5/2018 art. 1 c.6]`. Il lead che compila il modulo dà un consenso nuovo, quindi Andrea può chiamarlo subito; il Registro si consulta comunque ogni mese e prima di ogni campagna, e l'esito vale 15 giorni `[verificato: secondaria, fiscoetasse.com e smartworld.it; interpretazione per Andrea non verificata, va al legale]`.
6. **Dichiararsi AI è obbligatorio da agosto e non è stato rinviato.** L'art. 50(1) dell'AI Act si applica dal 2/8/2026; il Digital Omnibus non lo ha spostato. Il periodo di grazia per la marcatura dell'audio (art. 50(2)) vale fino al 2/12/2026 solo per i sistemi già sul mercato prima del 2/8/2026, quindi non per Andrea `[verificato: secondaria, labs.cloudsecurityalliance.org 21/9/2026]`.

Manca al board una voce: **un operatore telefonico è inevitabile**. Va aggiunto all'elenco dei servizi esterni che restano, accanto a M365, Claude Team e gli altri `[non verificato: proposta]`.

---

## 0. Cosa chiede la visione e cosa cambia

| Voce | Testo della visione | Fonte |
|---|---|---|
| G5 | Agente vocale "Andrea": richiama ogni lead entro 90 secondi, 24/7, si dichiara AI e fissa l'appuntamento con una persona | `[verificato: 00-visione-funzionalita.md riga 89]` |
| G6 | L'agente vocale impara dai rifiuti e cambia l'apertura | `[verificato: idem, riga 90]` |
| K10 | "Andrea" risponde anche alle chiamate in entrata e registra l'esito di ogni telefonata | `[verificato: idem, riga 130]` |

**Prima:** ElevenLabs Agents, numero mobile italiano Twilio, consenso e Registro controllati dal Cancello, circa 170 € al mese dalla fase 4 `[verificato: PRESENTAZIONE-CEO.md righe 553 e 719]`. Dopo il board di Michele, `33-costi-v2.md` aveva già tolto ElevenLabs e lasciato numero e chiamate Twilio per circa 82 € al mese `[verificato: 33-costi-v2.md riga 61]`.

**Ora:** Michele chiede che tutto ciò che non è nell'elenco del board sia self-hosted. In cloud restano solo M365/Entra ID, Claude Team, API Anthropic dietro LiteLLM, Cloudflare, GitHub, Supabase, Vercel, Jira, Instantly e S3 fuori sede facoltativo `[verificato: allegati/infra/board-testo-completo.txt]`. ElevenLabs e Twilio non ci sono. Il cervello di Andrea (API Anthropic) è già nell'elenco.

**Cosa si perde rispetto a ElevenLabs:** voce pronta e curata, latenza già misurata dal fornitore, nessun lavoro di integrazione telefonica. **Cosa si guadagna:** l'audio dei lead resta in casa, nessun canone a minuto per la voce, controllo completo del flusso `[non verificato: valutazione]`.

**Una regola interna da ricordare:** il piano marketing vieta voci sintetiche nelle call; per Andrea la presentazione chiede ai CEO un'eccezione, "solo per richiamare chi lo ha chiesto, con voce sintetica dichiarata" `[verificato: PRESENTAZIONE-CEO.md riga 637]`. Con la voce in casa l'eccezione resta necessaria.

---

## 1. Architettura proposta

```
Modulo del sito (consenso "richiamata da assistente AI", testo, ora, IP)
   -> SersanOutreach / n8n (VLAN 30)
   -> Cancello: consenso registrato? lista di soppressione? orario? tetto chiamate?
   -> Asterisk 22 LTS (nuova VLAN "voce"): chiamata in uscita sul trunk Messagenet
        <-> chan_websocket (audio slin16 + comandi JSON)
   -> agente Pipecat (VLAN 30, APPS)
        Silero VAD + Smart Turn v3.2 (CPU)
        STT in casa (CPU in fase 1, GPU in fase 2 in VLAN 80)
        Claude Haiku 5.5 via LiteLLM, pensiero spento (solo testo verso Anthropic)
        TTS in casa (CPU in fase 1, GPU in fase 2)
   -> esito: CRM SersanOutreach + canale vendite + calendario M365
   -> registrazione cifrata in MinIO (VLAN 40), cancellata dopo la trascrizione
```

Tutto il flusso è una proposta `[non verificato]`. Le componenti e i loro fatti sono nelle sezioni che seguono.

### 1.1 Dove mettere i pezzi nelle VLAN del board

| Pezzo | VLAN proposta | Regole da aggiungere su OPNsense | Fonte o stato |
|---|---|---|---|
| Asterisk | nuova VLAN "voce" (per esempio 25), oppure EDGE (20) | uscita solo verso gli IP dell'operatore (SIP 5060 o 5061 TLS, RTP); da Asterisk verso l'agente Pipecat solo sulla porta WebSocket | EDGE accetta in ingresso solo dal tunnel `[verificato: board-vlan.txt]`; VLAN nuova `[non verificato: proposta]` |
| Agente Pipecat | 30 · APPS | verso LiteLLM (stessa VLAN) e verso le API dei modelli in VLAN 80 | "APPS → AI solo sulle API dei modelli" è già nel board `[verificato: board]` |
| STT e TTS (fase 2) | 80 · AI, nello stesso LXC GPU o in uno nuovo | nessuna nuova uscita | `[non verificato: proposta]` |
| Registrazioni e trascrizioni | 40 · DATA (MinIO, PostgreSQL 16) | APPS → DATA come gli altri servizi | `[non verificato: proposta]` |
| Monitoraggio | 70 · OBSRV | latenza e chiamate su Prometheus e Grafana; log SIP su Loki e Wazuh | `[non verificato: proposta]` |
| Telefoni delle persone (K10) | LAN ufficio o mesh NetBird | softphone SIP verso Asterisk solo attraverso la mesh | `[non verificato: proposta]` |

### 1.2 Il nodo "nessuna porta aperta"

Il board dice "zero-trust, nessuna porta aperta" e l'IP fisso è ancora da richiedere `[verificato: board]`. Il SIP ha due strade:

- **Strada A, solo registrazione:** Asterisk si registra presso l'operatore e tiene aperta la connessione dall'interno. Con le opzioni NAT di PJSIP (`rtp_symmetric`, `force_rport`, `rewrite_contact`) di solito l'audio passa senza aprire porte. Rischio: audio a senso unico con alcuni operatori `[non verificato: prassi comune, da provare]`.
- **Strada B, apertura limitata:** inoltro di SIP (meglio TLS 5061) e della gamma RTP solo dagli IP dell'operatore, con CrowdSec e Wazuh davanti. Più affidabile, ma è una porta aperta, anche se su lista bianca `[non verificato: proposta]`.

Decide Michele. LiveKit SIP, l'alternativa ad Asterisk, chiede in ogni caso un IP pubblico, la porta SIP 5060 e la gamma RTP 10000-20000 aperte, e la rete host di Docker `[verificato: github.com/livekit/sip]`.

---

## 2. Framework: Pipecat o LiveKit Agents

| Criterio | Pipecat | LiveKit Agents |
|---|---|---|
| Licenza | BSD-2-Clause `[verificato: github.com/pipecat-ai/pipecat]` | Apache-2.0 per il codice e per il server SIP `[verificato: github.com/livekit/sip]`; il turn detector locale ha la "LiveKit Model License" `[verificato: docs.livekit.io turn-detector]` |
| Versione al 25/10/2026 | 1.14.0 del 24 ottobre `[verificato: github.com/pipecat-ai/pipecat/releases, anno dedotto]` | livekit-agents 1.8.9 del 24 ottobre `[verificato: github.com/livekit/agents/releases, anno dedotto]` |
| Pezzi da installare | un processo Python per l'agente | server LiveKit + servizio SIP + Redis + agente `[verificato: github.com/livekit/sip]` |
| Telefonia | serializzatori per i provider cloud; per Asterisk il pacchetto comunitario `pipecat-asterisk`, "community-maintained", che Pipecat "does not test or officially support", provato con Pipecat 1.1.0 e Python 3.12+, da usare con `FastAPIWebsocketTransport`; audio `slin` `[verificato: docs.pipecat.ai, serializzatore Asterisk]` | SIP nativo con chiamate in entrata, in uscita e DTMF; la registrazione presso l'operatore non è citata `[verificato: github.com/livekit/sip]` |
| Fine del turno in italiano | Smart Turn v3.2, BSD-2, 23 lingue con l'italiano, 8 MB in versione CPU, circa 65 ms su un'istanza cloud standard `[verificato: github.com/pipecat-ai/smart-turn]` | `v1-mini` gira in locale su CPU, gratis; `v1` completo gira su LiveKit Inference e oltre una soglia si paga; italiano fra le 14 lingue `[verificato: docs.livekit.io turn-detector]` |
| STT e TTS locali già pronti | Whisper (faster-whisper) con `hotwords` (1.9.0) e `initial_prompt` (1.11.0); Pocket TTS locale su CPU (1.7.0) con `Language.IT`; Kokoro; servizi NVIDIA `[verificato: release notes Pipecat; docs.pipecat.ai Pocket TTS via ricerca]` | soprattutto plugin verso servizi cloud; per i modelli locali serve un server compatibile `[non verificato]` |
| Note su Claude | dalla 1.10.0 `AnthropicLLMService` passa `temperature`, `top_k` e `top_p` tramite `extra_body` `[verificato: release notes Pipecat]` | dalla 1.8.9 la scelta forzata di uno strumento ricade su "auto" per diversi modelli Claude recenti `[verificato: release notes LiveKit]` |
| Adatto a 1-3 chiamate insieme | sì | sì, ma con più infrastruttura |

**Scelta consigliata: Pipecat** `[non verificato: valutazione]`. Motivi: un solo processo, licenza BSD, Smart Turn libero in italiano, Pocket TTS e Whisper già integrati, e Asterisk davanti risolve la registrazione SIP. Il serializzatore Asterisk è comunitario: si fissa la versione e, se serve, lo si riscrive (1-2 giorni, conteggiati in §11) `[non verificato: stima]`.

**Attenzione ai parametri di campionamento.** Con la versione API `2026-10-21`, mandare `temperature`, `top_p` o `top_k` dà errore 400 su tutti i modelli, anche con i valori di default `[verificato: secondaria, platform.claude.com/docs/en/api/migration-2026-10-21 via ricerca]`. Pipecat e LiteLLM vanno configurati per non mandarli, oppure si resta sulla versione `2023-06-01` `[non verificato: comportamento delle due librerie da provare]`.

**Hermes o Claude Agent SDK non servono nel ciclo della telefonata.** La conversazione in tempo reale chiama direttamente l'API Messages in streaming. Gli agenti dell'Agent OS (con Agent SDK o Hermes, secondo la scelta generale di `26-claude-agent-sdk.md` e `27-hermes-self-hosted.md`) lavorano prima e dopo la chiamata: brief del lead, scrittura nel CRM, riassunto, analisi dei rifiuti per G6 `[non verificato: proposta]`.

---

## 3. Centralino: Asterisk o FreeSWITCH

| Criterio | Asterisk | FreeSWITCH |
|---|---|---|
| Versioni | 22 LTS: rilasciata il 16/10/2024, solo correzioni di sicurezza dal 16/10/2028, fine vita 16/10/2029. 24 LTS: data prevista 15/10/2026, ma al 25/10/2026 la pagina la segna ancora "Pre-release" `[verificato: docs.asterisk.org Asterisk-Versions]` | progetto open source 1.11.2 (data esatta `non trovato`); edizione a pagamento "FreeSWITCH Advantage" 20.26.1 del 29/1/2026 `[verificato: secondaria, newreleases.io e developer.signalwire.com via ricerca]` |
| Audio verso l'agente | `chan_websocket` nativo dalle versioni 22.6.0 e 23.0.0; formato JSON preferito dalla 22.8.0. Comandi per svuotare la coda audio (interruzioni), `HANGUP`, `ANSWER`; eventi `MEDIA_START`, `DTMF_END`, controllo di flusso `MEDIA_XOFF`/`MEDIA_XON`; coda di circa 1.000 frame (circa 20 s); messaggi fino a 65.500 byte; uscita verso un server remoto con `Dial(WebSocket/...)`. La pagina scrive il comando di svuotamento sia `FLUSH_MEDIA` sia `MEDIA_FLUSH` `[verificato: docs.asterisk.org WebSocket]` | modulo di terzi `mod_audio_stream`: edizione comunitaria a senso unico; l'edizione commerciale parla di un limite di 10 canali gratuiti `[verificato: README di mod_audio_stream, letto nella rilevazione precedente di oggi; termini da confermare]` |
| Licenza | GPL-2.0 `[non verificato in questa sessione]` | MPL-1.1 `[verificato: pkgs.alpinelinux.org]`; i pacchetti binari ufficiali chiedono un token personale di un account SignalWire gratuito, il codice su GitHub no `[verificato: secondaria, signalwire.com FAQ via ricerca]` |
| Integrazione con Pipecat | `pipecat-asterisk` (comunitario) `[verificato: docs.pipecat.ai]` | nessun serializzatore trovato `[verificato: ricerca senza risultati]` |

**Scelta consigliata: Asterisk 22 LTS subito, passaggio a 24 LTS quando esce la finale** `[non verificato: proposta]`. Asterisk fa anche il resto del centralino per K10: gruppo di squillo verso le persone, segreteria, orari, registrazione.

Cyber Essentials: Asterisk parla con l'operatore, quindi entra nel perimetro con patch entro 14 giorni `[verificato: board, regola del perimetro]`. Le versioni LTS hanno 4 anni di supporto pieno e uno di sole correzioni di sicurezza `[verificato: docs.asterisk.org]`.

---

## 4. Trunk SIP e numero italiano (prezzi al 25/10/2026)

### 4.1 Perché un operatore italiano

La delibera AGCOM **106/25/CONS** (maggio 2025) obbliga gli operatori a bloccare le chiamate dall'estero che mostrano un numero italiano: dal 19/8/2025 i fissi, dal **19/11/2025 i mobili**, salvo chi è davvero in roaming `[verificato: secondaria, lentepubblica.it, corrierecomunicazioni.it, agendadigitale.eu via ricerca]`. La delibera **21/26/CIR** (14/4/2026) obbliga i fornitori a impedire chiamate con un numero non attribuito `[verificato: 16-gdpr-ai-act-e-regole.md riga 98]`. **Conseguenza:** un trunk estero che presenta un numero italiano rischia il blocco. Conviene un operatore italiano che origina le chiamate in Italia `[non verificato: deduzione]`.

### 4.2 Offerte trovate

| Operatore | Offerta | Prezzo | Note | Fonte |
|---|---|---|---|---|
| **Messagenet** (italiano) | SmartNumber PRO Base | 15 €/mese | 1 canale; fissi illimitati e 1.000 minuti verso mobili | `[verificato: messagenet.com/voip, IVA esclusa]` |
| Messagenet | **SmartNumber PRO Intermedio** | **30 €/mese** | 2 canali; fissi e mobili italiani illimitati "a condizioni di uso lecito e corretto"; attivazione non indicata ("Subito attivo!") | `[verificato: idem]` |
| Messagenet | SmartNumber PRO Avanzato | 45 €/mese | 3 canali | `[verificato: idem]` |
| Messagenet | SmartNumber a consumo | 36,60 €/anno + 8,54 € di attivazione, IVA inclusa | 1 canale; Asterisk e FreePBX fra i centralini compatibili | `[verificato: idem]` |
| Messagenet | tariffe a consumo | fisso 0,0189 €/min, mobile 0,0944 €/min, IVA inclusa, "effettivi secondi di conversazione", senza scatto | | `[verificato: messagenet.com/tariffe]` |
| VoipVoice (italiano, solo business) | voce per aziende e rivenditori | prezzi non pubblici | numero di prova gratuito | `[verificato: voipvoice.it, rilevazione precedente di oggi]` |
| Zadarma (estero) | numero geografico 070, 079, 0789 | 6 €/mese (3 € pagando l'anno), attivazione 0 € | serve un indirizzo nella stessa regione del numero e un documento; numeri mobili italiani non in listino | `[verificato: zadarma.com/it/tariffs/numbers/italy, IVA esclusa]`; rischio blocco anti-spoofing `[non verificato]` |
| Twilio (USA) | numero mobile IT | 45 $/mese | SIP trunking verso mobili IT: 0,3433 $/min, 0,0405 $/min se l'origine è nello SEE; "Pricing current as of August 2026" | `[verificato: twilio.com/en-us/sip-trunking/pricing/it]`; servizio cloud USA fuori dal board |

**Scelta consigliata: Messagenet SmartNumber PRO Intermedio** (2 canali, 30 €/mese): una chiamata in uscita e una in entrata insieme `[non verificato: proposta]`. Tre verifiche prima di firmare:
1. se l'uso "illimitato" ammette le chiamate fatte da un agente automatico. Le condizioni d'uso non sono state lette `non trovato`; nel mercato italiano i contratti "illimitati" di solito escludono i call center e l'uso automatico `[verificato: secondaria, condizioni Fastweb e delibere Co.re.com via ricerca]`. Se non è ammesso, si passa al consumo, circa 76 €/mese per 1.000 minuti (§12) `[non verificato: calcolo]`;
2. chi firma il contratto e con quale indirizzo: Sersan Limited è inglese, il team è in Sardegna. Per Zadarma serve un indirizzo nella stessa regione del numero; per Messagenet il requisito non è indicato sulla pagina `[verificato per Zadarma; non trovato per Messagenet]`;
3. se l'operatore accetta SIP su TLS e SRTP `non trovato`.

Il numero deve essere **in chiaro e richiamabile**; i prefissi 0843 e 0844 non sono obbligatori `[verificato: 16-gdpr-ai-act-e-regole.md riga 21]`.

---

## 5. Riconoscimento vocale (STT) in italiano, in streaming

| Modello | Licenza | Italiano | Streaming | Hardware | Integrazione con Pipecat | Fonte |
|---|---|---|---|---|---|---|
| **Nemotron 3.5 ASR streaming 0.6B** (NVIDIA) | OpenMDW-1.1, "ready for commercial use" | sì, livello "Transcription-ready". WER FLEURS: 5,23% a 80 ms, 4,85% a 160 ms, 4,83% a 320 ms, **4,41% a 560 ms**, 4,25% a 1,12 s | **sì, nativo** | GPU Turing, Volta, Ampere, Lovelace, Hopper, Blackwell; anche CPU con NeMo-Speech.cpp (GGUF), velocità non pubblicata | da scrivere: NeMo 26.06, Transformers 5.13+ o NeMo-Speech.cpp dietro un piccolo server | `[verificato: huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b]` |
| **Parakeet TDT 0.6B v3** (NVIDIA) | CC-BY-4.0, uso commerciale ammesso | sì. WER: FLEURS 3,00%, MLS 10,08%, CoVoST 3,69% | a blocchi (script con blocchi da 2 s) | GPU Ampere, Blackwell, Hopper, Volta (Turing non elencata); CPU in int8 ONNX, almeno 2 GB di RAM | a segmenti dopo il VAD, servizio da scrivere | `[verificato: huggingface.co/nvidia/parakeet-tdt-0.6b-v3]`; versione int8 per sherpa-onnx (codificatore circa 622 MB) e fattore di tempo reale su CPU 0,04-0,13 in prove della comunità `[verificato: secondaria, huggingface.co via ricerca, non su Xeon]` |
| Whisper large-v3-turbo (faster-whisper) | MIT | sì | no: Pipecat lo usa a segmenti dopo il VAD | GPU; su CPU lento per il tempo reale | **già integrato** (`hotwords`, `initial_prompt` per nomi e gergo) | `[verificato: release notes Pipecat 1.9.0 e 1.11.0]`; prestazioni `[non verificato]` |
| Vosk italiano 0.22 | Apache-2.0 | sì. WER: 8,10% Common Voice, 15,68% MLS (modello grande da 1,2 GB) | **sì, su CPU** | CPU | da scrivere | `[verificato: alphacephei.com/vosk/models]` |
| Qwen3-ASR 0.6B e 1.7B | Apache-2.0 | sì (30 lingue) | solo con vLLM | BF16; su Turing vLLM ha limiti seri | da scrivere | `[verificato: 13-modelli-open-source-sul-server.md §1]` |
| Voxtral Mini 4B Realtime 2602 (Mistral) | Apache-2.0 | sì (13 lingue) | sì, ritardo da 80 a 1.200 ms, 480 ms consigliati | pesi da circa 9 GB: solo su una scheda da 16 GB, da solo | da scrivere | `[verificato: rilevazione precedente di oggi su mistral.ai e recipes.vllm.ai]` |

**Scelta consigliata** `[non verificato: proposta]`:
- **Fase 1 (CPU):** Parakeet TDT v3 int8 a segmenti, subito dopo che Smart Turn dice "ha finito". Da provare in parallelo Nemotron con NeMo-Speech.cpp su CPU: se regge il tempo reale su 4-8 thread dello Xeon, dà lo streaming vero già in fase 1. Vosk resta la riserva in streaming su CPU, meno preciso.
- **Fase 2 (GPU):** Nemotron 3.5 ASR streaming a 560 ms, che dà i parziali mentre il cliente parla.
- **Prima di scegliere:** prova di WER su 20 telefonate vere registrate con consenso, accento sardo compreso, già chiesta in `13-modelli §8` `[verificato: 13-modelli-open-source-sul-server.md]`. L'audio telefonico arriva a 8 kHz (G.711) e le WER pubblicate sono su audio pulito: aspettarsi numeri peggiori `[non verificato]`.

---

## 6. Sintesi vocale (TTS) in italiano: modelli e licenze

| Modello | Licenza dei pesi | Italiano | Latenza e hardware | Integrazione Pipecat | Uso commerciale per Andrea | Fonte |
|---|---|---|---|---|---|---|
| **Pocket TTS** (Kyutai) | pesi **CC-BY-4.0**, codice MIT; per scaricare si accettano le condizioni su Hugging Face; vietato clonare voci "without explicit and lawful consent" | sì: voce predefinita **`giovanni`**, più la variante `italian_24l`, "higher quality but slower" | 100M parametri, **pensato per la CPU**, circa 200 ms al primo audio; circa 6 volte il tempo reale su un MacBook Air M4, circa 2,3-2,5 volte su una VM x86 | **già integrato** (`PocketTTSService`, `Language.IT`; la lingua si sceglie all'avvio, la voce si cambia a caldo) | **sì**, con attribuzione. Le voci di esempio hanno licenze proprie: Expresso ed EARS sono **non commerciali**, VCTK è CC-BY, le donazioni sono CC0. La licenza di `giovanni` non è nella pagina delle voci `non trovato`; il file di esempio si chiama `common_voice_it_...`, quindi probabilmente viene da Common Voice (CC0) `[non verificato]` | `[verificato: huggingface.co/kyutai/pocket-tts; github.com/kyutai-labs/pocket-tts; huggingface.co/kyutai/tts-voices; docs.pipecat.ai via ricerca]` |
| **Qwen3-TTS** 0.6B e 1.7B (Alibaba) | **Apache-2.0** | sì (10 lingue). WER italiano: 0,948 per 1.7B Base, 1,534 per 0.6B Base (ElevenLabs 1,743 nella stessa tabella) | streaming, "fino a 97 ms" dichiarati; pesi BF16 ed esempi con FlashAttention 2, che su Turing mancano; varianti Base (clonazione da 3 s), CustomVoice e **VoiceDesign** (voce da una descrizione, solo 1.7B) | da scrivere | **sì** | `[verificato: huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base]` |
| **Magpie TTS Multilingual 357M** (NVIDIA) | NVIDIA Open Model License, "ready for commercial use" | sì (12 lingue, versione v2607 del 21/7/2026) | primo audio 79 ms su A100 con 1 flusso (container NIM); GPU elencate: Ampere, Ada, Hopper; Turing e Blackwell non elencate | servizio NVIDIA di Pipecat via gRPC, oppure server da scrivere `[non verificato]` | **sì**. I container NIM in produzione possono chiedere una licenza NVIDIA AI Enterprise `[non verificato]`: meglio il checkpoint aperto con NeMo | `[verificato: huggingface.co/nvidia/magpie_tts_multilingual_357m; huggingface.co/blog/nvidia/magpie-tts-multilingual-voice-agents, 10/8/2026]` |
| **Fun-CosyVoice 3 0.5B** (2512) | **Apache-2.0** | sì (9 lingue comuni) | "bi-streaming", latenza "fino a 150 ms" dichiarata; GPU | da scrivere | **sì** | `[verificato: rilevazione precedente di oggi su huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512]` |
| **Chatterbox Multilingual V3** (Resemble AI) | **MIT** | sì (23+ lingue) | 500M; CUDA, CPU o MPS; il repository non cita un'API di streaming | da scrivere | **sì**. Ogni audio porta la filigrana **Perth**, utile per la marcatura (§9) | `[verificato: github.com/resemble-ai/chatterbox]` |
| Kokoro 82M | Apache-2.0 | 2 voci, `if_sara` e `im_nicola`, voto complessivo **C**, con 10-100 minuti di addestramento | gira su CPU | **già integrato** | sì; i fonemi italiani passano da espeak-ng (GPL-3.0), che non pesa per un uso interno non distribuito `[non verificato]` | `[verificato: huggingface.co/hexgrad/Kokoro-82M VOICES.md]` |
| Piper | modelli MIT; runtime `piper1-gpl` GPL-3.0 | voci `paola` (dataset senza licenza dichiarata), `riccardo` x_low (M-AILABS, "See URL"), `serena` (dataset sintetico CC-BY-4.0) | CPU | **già integrato** | solo come riserva: la licenza dei dati di `paola` e `riccardo` non è chiara | `[verificato: huggingface.co/rhasspy/piper-voices]` |
| Orpheus 3B es_it | etichetta Apache-2.0, ma deriva da Llama-3.2-3B-Instruct; "Beta Release" di ricerca | sì (spagnolo e italiano) | 3B: troppo pesante insieme al resto | da scrivere | **sconsigliato**. La licenza Llama 3.2 permette l'uso commerciale ma chiede "Built with Llama" e il nome "Llama" all'inizio dei modelli derivati distribuiti; l'etichetta Apache non la toglie; modello beta | `[verificato: huggingface.co/canopylabs/3b-es_it-ft-research_release; huggingface.co/meta-llama/Llama-3.2-3B-Instruct LICENSE]` |
| XTTS-v2 (Coqui) | Coqui Public Model License | sì (17 lingue) | GPU | sì (servizio esistente) | **no**: licenza solo non commerciale, anche per l'audio generato; Coqui ha chiuso tra fine 2023 e inizio 2024 e nessuno vende più la licenza commerciale | licenza e lingue `[verificato: huggingface.co/coqui/XTTS-v2]`; chiusura `[verificato: secondaria, vari siti via ricerca]` |
| F5-TTS | codice MIT, pesi **CC-BY-NC** "due to the training data Emilia" | modelli ufficiali senza italiano dichiarato | GPU | da scrivere | **no** | `[verificato: github.com/SWivid/F5-TTS]` |
| Voxtral TTS (Mistral) | pesi CC BY-NC | sì | GPU, oppure API a pagamento | no | **no** in casa | `[verificato: secondaria, kdnuggets.com e neelshah18.com via ricerca]` |

### 6.1 La voce di Andrea

- **Niente voce di un collega.** Clonare la voce di una persona reale crea obblighi in più e richiede un contratto separato e revocabile; il progetto parte con una voce sintetica dichiarata `[verificato: PRESENTAZIONE-CEO.md riga 758]`.
- **Come avere una voce italiana con diritti puliti** `[non verificato: proposta, da provare]`:
  1. fase 1: provare la voce `giovanni` di Pocket TTS, dopo aver chiarito la sua licenza con Kyutai;
  2. creare una voce con Qwen3-TTS **VoiceDesign** da una descrizione ("voce maschile italiana, 35 anni, calda, ritmo calmo"), registrare 10-20 secondi e usarli come riferimento per Pocket TTS (fase 1) o per Qwen3-TTS Base (fase 2). Pocket TTS vieta la clonazione senza consenso: una voce disegnata non appartiene a nessuno, ma va annotato nel registro dei trattamenti;
  3. in alternativa, un doppiatore con un contratto di licenza d'uso della voce;
  4. riserva a costo zero: Kokoro `im_nicola` (voto C).
- **Prova d'ascolto:** 10 frasi tipiche di Andrea, 3-4 modelli, voti di 5 persone fuori dal progetto. Nessuno ha ancora misurato la qualità italiana di questi modelli in casa `[verificato: 13-modelli-open-source-sul-server.md §1]`.

---

## 7. Latenza realistica con Claude via API

### 7.1 Il modello

- **Claude Haiku 5.5** (`claude-haiku-5-5`, uscito il 7/10/2026): 0,10 $ per milione di token in ingresso e 0,50 $ in uscita fino a 100.000 token di prompt; lettura dalla cache 0,01 $; il più veloce della gamma attuale ("Fastest") `[verificato: platform.claude.com pricing e models overview; data: artificialanalysis.ai]`.
- **Il pensiero è acceso di serie** ed effort di default "medium". Haiku 5.5 accetta `thinking: {type: "disabled"}` solo a effort "high" o inferiore; con il pensiero spento e l'output JSON il modello può saltare una chiamata a uno strumento che gli serve `[verificato: platform.claude.com, pagine Thinking e Models overview]`.
- **Misure con il pensiero acceso** (Artificial Analysis): primo token dopo 6,58 s a effort "low", 7,71 s a "medium"; poi 172-178 token al secondo `[verificato: artificialanalysis.ai/providers/anthropic]`. Per la voce è inaccettabile: il pensiero va spento.
- **Senza pensiero** il dato è `non trovato`. Riferimenti: Haiku 4.5 senza ragionamento **0,48 s**, 83 token al secondo; Sonnet 5 senza ragionamento **0,79 s** `[verificato: artificialanalysis.ai/providers/anthropic]`.
- **Riserva:** Haiku 4.5 resta disponibile come modello legacy, pensiero spento di serie, 1 $ e 5 $ per milione di token `[verificato: platform.claude.com pricing e pagina Thinking]`. Se Haiku 5.5 senza pensiero risultasse lento, si usa Haiku 4.5 per circa 17 € in più al mese (§12) `[non verificato: calcolo]`.
- Con la versione API `2026-10-21` niente `temperature`, `top_p`, `top_k` (§2) `[verificato: secondaria, guida di migrazione via ricerca]`.
- Nessuna regione UE: `inference_geo: "us"` costa 1,1 volte, "global" è il default `[verificato: platform.claude.com pricing]`.

### 7.2 Bilancio della latenza, dalla fine della frase del cliente al primo suono di Andrea

| Fase | Fase 1, solo CPU | Fase 2, con GPU | Base della stima |
|---|---|---|---|
| Rete telefonica e Asterisk, buffer anti-jitter | 0,15-0,25 s | 0,15-0,25 s | `[non verificato: valori tipici VoIP]` |
| VAD (silenzio di 0,2 s) + Smart Turn | 0,25-0,35 s | 0,25-0,30 s | Smart Turn circa 65 ms `[verificato: github smart-turn]` |
| STT finale | 0,2-0,4 s (Parakeet a segmenti su CPU) | 0,05-0,2 s (parziali in streaming) | fattore 0,04-0,13 su CPU in prove della comunità `[verificato: secondaria]`; resto `[non verificato: stima]` |
| Claude Haiku 5.5 senza pensiero, primo token, con andata e ritorno verso gli USA e LiteLLM | 0,5-0,8 s | 0,5-0,8 s | Haiku 4.5: 0,48 s `[verificato: artificialanalysis.ai]`; resto `[non verificato]` |
| TTS, primo pezzo di audio | 0,2-0,4 s (Pocket TTS) | 0,1-0,3 s (Qwen3-TTS, Magpie o CosyVoice 3) | 200 ms Pocket `[verificato: HF]`; 97, 79 e 150 ms dichiarati su GPU da data center `[verificato: HF e blog NVIDIA]` |
| **Totale** | **circa 1,6-2,5 s** (vedi nota) | **circa 1,3-2,0 s** | `[non verificato: somma delle stime]` |

Nota: la somma minima della fase 1 è 1,3 s, ma su CPU i tempi si allungano quando due chiamate sono attive insieme; per prudenza la forchetta parte da 1,6 s `[non verificato]`.

**Come renderla accettabile** `[non verificato: proposte]`:
- frasi brevi (una o due per turno) e testo mandato al TTS frase per frase;
- un "Certo, un attimo" pre-sintetizzato quando serve uno strumento (calendario, CRM);
- prompt di sistema in cache e orari liberi del calendario letti **prima** di comporre il numero;
- interruzione immediata svuotando la coda audio di Asterisk quando il cliente riprende a parlare `[verificato: comando in docs.asterisk.org WebSocket]`;
- misura vera di p50 e p95 su 50 chiamate di prova prima di andare dai lead.

**Se l'API Anthropic non risponde:** Andrea si scusa, dice che una persona richiamerà, e il Cancello mette la richiamata nel canale vendite. Un modello locale da 4B non è adatto a una conversazione di vendita `[non verificato: valutazione]`.

---

## 8. Memoria GPU e CPU necessaria; cosa cambia con la seconda GPU

### 8.1 Oggi la RTX 4000 non ha spazio per Andrea

| Servizio già previsto sulla RTX 4000 (8 GB) | Memoria stimata | Fonte |
|---|---|---|
| Ollama, Qwen3-4B Q5_K_M | circa 3,5-4,2 GB con il contesto | `[non verificato: stima]`; servizio `[verificato: board-vlan.txt]` |
| Infinity, embedding + reranker Qwen3 0.6B FP16 | circa 3 GB | `[non verificato: stima]`; servizio `[verificato: board]` |
| Docling (quando indicizza) | a picchi | `[non verificato]` |
| **Libero per Andrea** | **meno di 1 GB** | `[non verificato: stima]` |

In più la scheda "di giorno all'AI, la sera alla VM Experimental-1" `[verificato: 25-board-michele-e-delta.md riga 27, dal board]`. Un agente che deve rispondere 24/7 non può dipendere da lei.

### 8.2 Fase 1: Andrea solo su CPU

| Componente | CPU | RAM | Fonte |
|---|---|---|---|
| Asterisk (LXC) | 1-2 vCPU | 1 GB | `[non verificato: stima]` |
| Agente Pipecat + Silero VAD + Smart Turn | 2 vCPU | 1-2 GB | `[non verificato: stima]` |
| STT Parakeet int8 | 4 vCPU per chiamata | circa 1-2 GB | `[non verificato: stima]`; almeno 2 GB per caricarlo `[verificato: HF Parakeet]` |
| TTS Pocket TTS | 2-4 vCPU per chiamata | circa 1 GB | 6 volte il tempo reale su un M4 `[verificato: HF]`; sullo Xeon Gold 5218 `[non verificato]` |
| **Totale per 2 chiamate insieme** | **circa 16 vCPU su 64** | **circa 6-8 GB su circa 53 liberi** | RAM libera `[verificato: board, tabella Capacità]`; resto `[non verificato]` |

La RAM in più di cui parla Michele non serve ad Andrea: bastano i circa 53 GB già liberi `[non verificato: deduzione dalla tabella]`.

### 8.3 Fase 2: la seconda GPU

Il board prevede la seconda GPU nella fase F5, "fissa sull'AI" `[verificato: board, roadmap F5; 25-board-michele-e-delta.md riga 27]`. Michele scrive "RTX A2000 con chip Ada da 6GB GDDR7": quella scheda non esiste `[verificato: le schede reali sono nella tabella]`. Le schede da 70 W, alimentate dallo slot:

| Scheda | Architettura | Memoria | Prezzo rilevato | Fonte |
|---|---|---|---|---|
| RTX A2000 | Ampere (2021) | 6 o 12 GB GDDR6 | 12 GB: 499-569 € su eBay.de | specifiche `[verificato: 30-call-e-trascrizione-self-hosted.md, da TechPowerUp e Gigabyte]`; prezzi `[verificato: 25-board-michele-e-delta.md riga 325]` |
| RTX 2000 Ada | Ada Lovelace (2024) | 16 GB GDDR6 | 769,99 € (PNY, Yeppon); 1.071,47 € (Dell, IT-Partners) | specifiche `[verificato: computerbase.de]`; prezzi `[verificato: secondaria, ricerca, date delle pagine non indicate]` |
| RTX PRO 2000 Blackwell | Blackwell (2025) | 16 GB GDDR7 ECC | 1.090 € il più basso in Italia (24/10/2026), minimo a 12 mesi 740 €, mediana 971 €; 1.501 € su MediaWorld | specifiche `[verificato: cgchannel.com, emarque.co]`; prezzi `[verificato: gpuprix.com/italy, MediaWorld via ricerca]` |
| RTX 4000 SFF Ada | Ada Lovelace | 20 GB GDDR6 ECC | circa 1.320-2.100 € IVA inclusa; mediana europea a 12 mesi 1.760 € (24/9/2026) | `[verificato: secondaria, hardwaredealz.com, jacob.de, gpuprix.com via ricerca]` |
| RTX PRO 4000 Blackwell SFF | Blackwell | 24 GB GDDR7 ECC | circa 2.140-2.160 € (Germania) | `[verificato: secondaria, hardwaredealz.com via ricerca]` |

Cosa ci sta in ciascuna (stime in FP16 o BF16 con il contesto CUDA) `[non verificato: stime]`:

| Combinazione | Memoria | 6 GB | 12 GB | 16 GB | 20-24 GB |
|---|---|---|---|---|---|
| Nemotron ASR + Magpie TTS o Qwen3-TTS 0.6B, 1 chiamata | circa 4-5 GB | al limite | sì | sì | sì |
| Nemotron + Qwen3-TTS 1.7B o Chatterbox, 2-3 chiamate | circa 7-9 GB | no | sì | sì | sì |
| Andrea + tutta la pipeline RAG (Qwen3-4B, embedding, reranker) | circa 12-14 GB | no | no | **sì** | sì, con margine |
| Voxtral Mini 4B Realtime da solo | oltre 9 GB | no | stretto | sì, ma senza altro | sì |

**Cosa cambia davvero con la seconda GPU** `[non verificato: valutazione]`:
1. **Voce migliore:** Qwen3-TTS, Magpie, CosyVoice 3 o Chatterbox al posto di Pocket TTS. Ampere, Ada e Blackwell hanno BF16 e FlashAttention 2, che su Turing mancano `[verificato: 13-modelli-open-source-sul-server.md §1]`. Magpie elenca Ampere e Ada ma non Blackwell né Turing `[verificato: HF Magpie]`.
2. **Ascolto in streaming:** Nemotron dà le parole mentre il cliente parla; si guadagnano circa 0,2-0,3 s.
3. **Più chiamate insieme** senza togliere CPU agli altri servizi.
4. **Con 16 GB o più** tutta l'AI (Andrea + RAG) sta sulla nuova scheda 24/7, e la RTX 4000 può andare a Experimental-1 anche di giorno. Con 6 GB la scheda serve solo ad Andrea.

**Consiglio:** una 16 GB al posto della A2000 da 6 GB; RTX 2000 Ada se si cerca il prezzo, RTX PRO 2000 Blackwell se si vuole GDDR7 ed ECC `[non verificato: valutazione]`. Da verificare con Michele: spazio nei riser del DL380 Gen10 (sono schede a basso profilo ma a doppio slot) `[verificato: cgchannel.com per la PRO 2000]`, driver NVIDIA nell'host Proxmox che reggano insieme Turing e Blackwell, e passaggio della scheda nell'LXC `[non verificato]`.

---

## 9. Regole: dichiararsi AI, consenso, Registro delle opposizioni

Le regole sono già in `16-gdpr-ai-act-e-regole.md`. Qui c'è come le applica Andrea self-hosted, con gli aggiornamenti di oggi.

| Regola | Cosa fa Andrea o il Cancello | Fonte |
|---|---|---|
| **Dichiararsi AI** dalla prima interazione (AI Act art. 50(1), dal 2/8/2026, non rinviato dal Digital Omnibus) | Prima frase fissa, non modificabile da G6: "Buongiorno, sono Andrea, l'assistente virtuale di SerSan. Sono un'intelligenza artificiale e la chiamata è registrata." Test automatico sul prompt di apertura e campione mensile delle registrazioni | data e mancato rinvio `[verificato: secondaria, labs.cloudsecurityalliance.org 21/9/2026]`; regola `[verificato: 16-gdpr §6]`; testo della frase `[non verificato: proposta]` |
| **Stato del Digital Omnibus** | Accordo provvisorio a maggio 2026; ha spostato le scadenze dei sistemi ad alto rischio, non l'art. 50. Una fonte dà l'entrata in vigore al 27/7/2026 | accordo `[verificato: secondaria, CSA]`; entrata in vigore `[verificato: secondaria, usercentrics.com via ricerca, da confermare sulla Gazzetta UE]` |
| **Marcatura dell'audio sintetico** (art. 50(2)) | Costruendo Andrea in casa, SerSan potrebbe esserne il "fornitore" e dover marcare l'audio in modo leggibile da una macchina. Il periodo di grazia fino al 2/12/2026 vale solo per i sistemi sul mercato prima del 2/8/2026: Andrea parte dopo, quindi niente grazia. Il Codice di condotta finale del 10/6/2026 chiede "at least two layers of machine-readable marking" (metadati, filigrane o altro) ed è volontario. Chatterbox ha già la filigrana Perth; al telefono (G.711, 8 kHz) una filigrana può non sopravvivere. Proposta: metadati e filigrana sulle registrazioni conservate, più la dichiarazione a voce | grazia `[verificato: secondaria, CSA]`; Codice `[verificato: secondaria, jonesday.com]`; ruolo di fornitore e tenuta della filigrana `[non verificato: domanda per il legale]` |
| **Consenso alle chiamate automatizzate** (Codice privacy art. 130 c.1) | Andrea chiama solo chi ha spuntato nel modulo "richiamata da un assistente AI"; il Cancello salva testo, ora e IP del consenso e rifiuta un lead senza consenso registrato | `[verificato: 16-gdpr-ai-act-e-regole.md riga 19]`; controllo nel Cancello `[non verificato: proposta]` |
| **Registro delle opposizioni** | Il consenso dato dopo l'iscrizione resta valido: il lead del modulo si può chiamare subito. Il Registro si consulta ogni mese e prima di ogni campagna; l'esito vale **15 giorni** per il telefono; le liste tornano entro 24 ore con, per ogni numero, l'eventuale data di annullamento dei consensi. La regola 4 di `16-gdpr` parla di 30 giorni: va corretta a 15 | consenso successivo `[verificato: secondaria, agendadigitale.eu 1/4/2022]`; obblighi, 15 giorni e 24 ore `[verificato: secondaria, fiscoetasse.com e smartworld.it via ricerca, articoli del 2022]`; applicazione ad Andrea `[non verificato: domanda per il legale]` |
| Costo del Registro | Prima fascia: 10.000 numeri a 92 € l'anno IVA esclusa (tariffa 2024). Per il 2026 il nuovo decreto (DM 22/12/2025) era in attesa di registrazione e valevano le tariffe del DM 20/12/2024 prorogate | 2024 `[verificato: mise.gov.it, DM tariffe 2024, via ricerca]`; 2026 `[verificato: avviso MIMIT del 23/12/2025, via ricerca]`; importo 2026 `non trovato` |
| **Un "no" ferma tutti i canali** | "Non chiamatemi più" riconosciuto in chiamata: Andrea conferma, chiude, e il numero entra nella lista di soppressione condivisa con email e LinkedIn | `[verificato: 16-gdpr §6 regola 5]`; riconoscimento in chiamata `[non verificato: proposta]` |
| **Numero in chiaro e richiamabile** | Numero geografico o mobile dell'operatore italiano; chi richiama trova una persona o Andrea (K10) | `[verificato: 16-gdpr-ai-act-e-regole.md riga 97]` |
| **Registrazione** | Informativa a voce all'inizio; audio cifrato in MinIO, cancellato dopo la trascrizione (al massimo 30 giorni); trascrizione e riassunto 24 mesi dall'ultimo contatto | `[verificato: 16-gdpr §1.1, proposta già scritta]` |
| **Persona disponibile** | Andrea offre sempre di farsi richiamare da una persona; non vende, fissa l'appuntamento | `[verificato: PRESENTAZIONE-CEO.md riga 489]` |
| **DPIA** | Obbligatoria per l'agente vocale, prima del primo lead vero | `[verificato: 16-gdpr §6 regola 9]` |
| **Regno Unito** | Fuori dal primo rilascio: le chiamate automatiche verso il Regno Unito chiedono un consenso specifico (PECR) | `[verificato: 16-gdpr §2]` |
| **Orari** | G5 chiede 24/7. Proposta: di notte Andrea richiama solo se il lead ha scelto "richiamatemi adesso"; altrimenti alle 9 del mattino | `[non verificato: proposta]` |

Vantaggio per la privacy del self-hosting: la voce dei lead non va più negli USA (ElevenLabs conserva in USA di default) `[verificato: 16-gdpr §0]`. Il testo della conversazione va comunque ad Anthropic, senza regione UE `[verificato: 16-gdpr §0; platform.claude.com pricing]`. Proposta: niente dati sensibili nel prompt, numero di telefono pseudonimizzato, richiesta ad Anthropic della conservazione zero già prevista `[non verificato: proposta; conservazione zero in PRESENTAZIONE-CEO.md riga 650]`.

---

## 10. G6 e K10 nel dettaglio

**K10, chiamate in entrata** `[non verificato: proposta]`:
1. Il numero aziendale suona sulle persone (softphone SIP collegati via NetBird) per 20 secondi in orario d'ufficio.
2. Se nessuno risponde, o fuori orario, risponde Andrea con la stessa frase di apertura.
3. Andrea capisce il motivo, fissa la call sul calendario M365 o prende un messaggio.
4. A fine chiamata il riassunto e l'esito (appuntamento, da richiamare, non interessato, opposizione) vanno nel CRM SersanOutreach e nel canale vendite. Il Cancello approva solo ciò che esce verso il cliente, per esempio la mail di conferma.

**G6, imparare dai rifiuti** `[non verificato: proposta]`:
1. Ogni settimana un agente legge le trascrizioni con esito "rifiuto" e raggruppa le obiezioni.
2. Propone due aperture alternative. La frase di dichiarazione AI resta fissa e un test lo controlla.
3. Le nuove aperture passano dal Cancello: un founder approva.
4. Andrea alterna le aperture approvate (test A/B) e il cruscotto mostra il tasso di appuntamenti per apertura.
5. Le trascrizioni sono fatte in casa, quindi l'analisi non manda audio fuori; costo con Sonnet 5.5 sotto 1 € al mese (§12).

---

## 11. Stima dei giorni di lavoro

| Attività | Chi | Giorni-persona | Base |
|---|---|---|---|
| Contratto con l'operatore, numero, Asterisk 22 LTS in LXC, trunk, regole OPNsense, TLS e SRTP se disponibili | Michele | 3-4 | `[non verificato: stima]` |
| Agente Pipecat: chan_websocket, serializzatore (fissato o riscritto), VAD, Smart Turn, Claude via LiteLLM con pensiero spento e senza parametri di campionamento | Mattia | 4-5 | `[non verificato: stima]` |
| STT: integrazione di 2 candidati (Parakeet e Nemotron su CPU) e prova di WER su 20 telefonate vere | Mattia, Alberto | 3-4 | `[non verificato: stima]` |
| TTS e voce di Andrea: licenza di `giovanni`, VoiceDesign o doppiatore, prova d'ascolto con 5 persone | Alberto | 2-3 | `[non verificato: stima]` |
| Cancello: consenso registrato, lista di soppressione, Registro ogni mese, orari, tetti; esito nel CRM e nel canale; calendario M365 | Alberto, Mattia | 4-5 | `[non verificato: stima]` |
| K10: gruppo di squillo, fuori orario, segreteria | Michele | 1-2 | `[non verificato: stima]` |
| G6: analisi dei rifiuti, aperture nel Cancello, test A/B | Alberto | 2-3 | `[non verificato: stima]` |
| Prove finali: latenza p50 e p95 su 50 chiamate, interruzioni, DTMF, API ferma, due chiamate insieme; DPIA e registro dei trattamenti | tutti | 3-4 | `[non verificato: stima]` |
| **Totale fase 1 (CPU)** | | **circa 22-30, in media 24** | `[non verificato: stima]` |
| Fase 2: montaggio della GPU, passaggio nell'LXC, Nemotron e nuovo TTS, nuova misura di latenza | Michele, Mattia | 3-5 in più | `[non verificato: stima]` |

Su calendario sono circa **5-6 settimane** con tre persone a tempo parziale `[non verificato: stima]`. Nel piano attuale Andrea arriva nella fase 4 (settimane 17-20), solo con parere legale e lead veri `[verificato: PRESENTAZIONE-CEO.md riga 519]`; lato server serve LiteLLM acceso, cioè la fase F4 del board `[verificato: board, roadmap F4]`.

---

## 12. Costi mensili

Ipotesi come in `14-costi §3.4`: 300 lead al mese, circa 1.000 minuti, 90% verso mobili `[verificato: 14-costi-abbonamenti-e-api.md §3.4]`.

| Voce | Fase 1, PRO Intermedio | Fase 1, a consumo | Fase 2 (con GPU) | Base |
|---|---|---|---|---|
| Operatore e numero | 30,00 € (2 canali, illimitato "con uso lecito e corretto") | 2 numeri SmartNumber 5,00 € + 900 min × 0,0774 € + 100 min × 0,0155 € = **76,19 €** | come la fase 1 scelta | prezzi `[verificato: messagenet.com, IVA del 22% scorporata]`; calcolo `[non verificato]` |
| Registro delle opposizioni | 7,67 € (92 € l'anno) | 7,67 € | 7,67 € | `[verificato: tariffa 2024 prorogata]`; importo 2026 `non trovato` |
| Claude in chiamata (Haiku 5.5, 18.000 token in e 600 out al minuto) | ≈ 1,88 € (2,10 $) | ≈ 1,88 € | ≈ 1,88 € | stessa ipotesi di `14-costi §3.4` `[verificato]`; prezzi `[verificato: platform.claude.com]` |
| Claude dopo la chiamata: 333 riassunti (5.000 token in, 300 out) e 4 analisi G6 con Sonnet 5.5 | ≈ 4,40 € (4,93 $) | ≈ 4,40 € | ≈ 4,40 € | prezzi `[verificato: platform.claude.com]`; volumi `[non verificato: stima]` |
| Corrente in più | ≈ 2,60 € (10 W medi) | ≈ 2,60 € | ≈ 9,00 € (più la GPU a 25 W medi) | `[non verificato: ipotesi a 0,35 €/kWh]` |
| **Totale al mese** | **≈ 47 €** | **≈ 93 €** | **≈ 53-99 €** | `[non verificato: somma]` |
| Una tantum | attivazione non indicata | 7,00 € per numero (8,54 € IVA inclusa) | scheda da 16 GB: circa 770-1.500 € | `[verificato: messagenet.com; prezzi GPU in §8.3]` |

Se Haiku 5.5 senza pensiero fosse troppo lento e si usasse Haiku 4.5, la riga "Claude in chiamata" passa da 1,88 € a circa 18,76 € (21,00 $) `[non verificato: calcolo con i prezzi di platform.claude.com]`.

**Confronto** `[non verificato: confronto]`:
- via ElevenLabs: circa 170 € al mese (88,45 € Pro, 40,20 € numero, 41,63 € chiamate e modello) `[verificato: PRESENTAZIONE-CEO.md riga 553]`;
- via Twilio con voce locale: circa 82 € al mese, con il rischio della tariffa SIP verso i mobili a 0,3433 $ al minuto `[verificato: 33-costi-v2.md righe 61 e 75]`;
- via Messagenet e voce in casa: circa 47 € al mese, 93 € se l'illimitato non vale per un agente.

Il risparmio è di circa 75-120 € al mese rispetto a ElevenLabs, contro circa 24 giorni-persona di lavoro e una scheda per la fase 2. La ragione forte per farlo in casa non è il prezzo: è che la voce dei lead resta in azienda, come chiede Michele `[non verificato: valutazione]`.

---

## 13. Rischi e come ridurli

| Rischio | Cosa fare | Stato |
|---|---|---|
| Voce italiana di Pocket TTS non abbastanza naturale | prova d'ascolto prima di tutto; in riserva aspettare la GPU (Qwen3-TTS, Magpie, CosyVoice 3); in ultima istanza chiedere ai CEO un'eccezione per un TTS in cloud | `[non verificato]` |
| Licenza della voce `giovanni` non chiara | chiedere a Kyutai; altrimenti voce disegnata con VoiceDesign o doppiatore | `non trovato` |
| STT sbaglia nomi e accento sardo | `hotwords` e `initial_prompt` con i nomi SerSan (se Whisper); prova di WER su chiamate vere | `[verificato: opzioni nelle release notes Pipecat]` |
| Haiku 5.5 lento anche senza pensiero, o salta strumenti | misura il primo giorno; riserva Haiku 4.5; strumenti semplici e senza output JSON in chiamata | `[verificato: avvertenza in platform.claude.com Thinking]`; latenza `non trovato` |
| Parametri di campionamento rifiutati (errore 400) | configurare Pipecat e LiteLLM per non mandarli | `[verificato: guida di migrazione 2026-10-21 via ricerca]` |
| Latenza sopra i 2 secondi | misurare p50 e p95; frasi corte; dati pre-caricati; GPU in fase 2 | `[non verificato]` |
| Serializzatore Asterisk comunitario si rompe con un aggiornamento | fissare le versioni; riscriverlo in casa (è piccolo) | `[verificato: è comunitario e non testato da Pipecat]` |
| Audio a senso unico per il NAT | provare le due strade di §1.2 prima di firmare con l'operatore | `[non verificato]` |
| "Illimitato" dell'operatore non valido per un agente | leggere le condizioni; piano a consumo | `[non verificato]` |
| Chiamate bloccate per il numero chiamante | operatore italiano che origina in Italia | `[non verificato: deduzione da 106/25/CONS]` |
| API Anthropic lenta o ferma | messaggio di scuse e richiamata umana nel canale | `[non verificato]` |
| Marcatura dell'audio richiesta da subito | metadati e filigrana sulle registrazioni; parere legale sul ruolo di fornitore | `[non verificato]` |

---

## 14. Domande aperte

1. **Michele:** per il SIP preferisci la sola registrazione o un'apertura limitata agli IP dell'operatore? In quale VLAN mettiamo Asterisk?
2. **Michele:** quale seconda GPU esattamente? La "A2000 Ada da 6 GB GDDR7" non esiste: A2000 12 GB, RTX 2000 Ada 16 GB, RTX PRO 2000 Blackwell 16 GB, oppure una SFF da 20-24 GB? Entra nei riser del DL380 Gen10 accanto alla RTX 4000?
3. **Michele:** possiamo aggiungere al board l'operatore telefonico fra i servizi esterni che restano?
4. **Alessandro e Michele:** chi firma il contratto con l'operatore (Sersan Limited o una persona in Italia) e con quale indirizzo in Sardegna?
5. **Messagenet:** il traffico illimitato di SmartNumber PRO vale per chiamate fatte da un agente automatico? Supporta TLS e SRTP?
6. **Kyutai:** con quale licenza è rilasciata la voce italiana `giovanni` di Pocket TTS?
7. **Legale:** il consenso dato nel modulo pochi secondi prima basta anche se il numero è iscritto al Registro delle opposizioni, e serve comunque abbonarsi al Registro se Andrea chiama solo chi ha dato il consenso? La richiamata chiesta dal lead è "chiamata automatizzata" per l'art. 130 c.1?
8. **Legale:** facendo Andrea in casa, SerSan è "fornitore" ai sensi dell'art. 50(2) e deve marcare l'audio sintetico anche al telefono?
9. **Alberto:** voce `giovanni`, voce disegnata con VoiceDesign o doppiatore con contratto?
10. **Alessandro:** Andrea richiama anche di notte, o solo se il lead sceglie "adesso"? Su chi squilla prima il numero aziendale, e per quanti secondi?
11. **Tutti:** il canale vendite resta Slack o passa a Teams, visto che M365 resta?

---

## Fonti

Progetto:
- `C:\Users\alber\SerSan-AgentOS\ricerca\00-visione-funzionalita.md` (G5, G6, K10)
- `C:\Users\alber\SerSan-AgentOS\allegati\infra\SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`
- `C:\Users\alber\SerSan-AgentOS\PRESENTAZIONE-CEO.md` (righe 489, 519, 553, 637, 650, 719, 758)
- `C:\Users\alber\SerSan-AgentOS\ricerca\13-modelli-open-source-sul-server.md` §1 e §8; `14-costi-abbonamenti-e-api.md` §3.4; `16-gdpr-ai-act-e-regole.md` §0, §1, §2, §6; `22-architettura-scelta.md`; `25-board-michele-e-delta.md`; `26-claude-agent-sdk.md`; `27-hermes-self-hosted.md`; `30-call-e-trascrizione-self-hosted.md`; `33-costi-v2.md`

Framework e centralino (lette il 25/10/2026):
- https://github.com/pipecat-ai/pipecat e https://github.com/pipecat-ai/pipecat/releases
- https://docs.pipecat.ai/api-reference/server/services/serializers/asterisk
- https://docs.pipecat.ai/api-reference/server/services/tts/pocket-tts (via ricerca)
- https://github.com/pipecat-ai/smart-turn
- https://github.com/livekit/agents/releases ; https://github.com/livekit/sip ; https://docs.livekit.io/agents/logic/turns/turn-detector/
- https://docs.asterisk.org/About-the-Project/Asterisk-Versions/ ; https://docs.asterisk.org/Configuration/Channel-Drivers/WebSocket/
- https://pkgs.alpinelinux.org/package/v3.24/main/x86_64/freeswitch ; https://newreleases.io/project/github/signalwire/freeswitch/release/v1.11.2 ; https://signalwire.com/faqs/how-do-i-get-a-freeswitch-token (via ricerca)

Operatori e regole telefoniche:
- https://www.messagenet.com/voip/ ; https://www.messagenet.com/tariffe/
- https://zadarma.com/it/tariffs/numbers/italy/
- https://www.twilio.com/en-us/sip-trunking/pricing/it
- https://lentepubblica.it/cittadini-e-imprese/telefonate-moleste-da-call-center-scatta-oggi-il-primo-stop-per-i-numeri-italiani-falsi/ ; https://corrierecomunicazioni.it/telco/telemarketing-selvaggio-da-oggi-stop-alle-chiamate-moleste-dallestero-ecco-cosa-succede ; https://www.agendadigitale.eu/infrastrutture/telemarketing-da-agosto-il-super-filtro-dei-numeri-fasulli-ecco-come/ (via ricerca)
- https://www.agendadigitale.eu/sicurezza/privacy/registro-opposizioni-come-cambia-il-telemarketing-e-i-nodi-aperti/
- https://www.fiscoetasse.com/normativa-prassi/13127-come-bloccare-le-chiamate-indesiderate-in-arrivo-il-nuovo-registro-delle-opposizioni.html ; https://www.smartworld.it/guide/registro-opposizioni-blocco-chiamate-indesiderate-come-iscriversi.html (via ricerca)
- https://www.mise.gov.it/images/stories/normativa/4.1_RPO_DM_Tariffe2024_v0.6_22.12.2023_FIRM.pdf ; https://www.mimit.gov.it/images/stories/normativa/AVVISO_del_23_dicembre_2025_Registro_Pubblico_delle_Opposizioni_Costi_e_tariffe.pdf (via ricerca)
- https://www.fastweb.it/adsl-aziende/dettagli/traffico-incluso/?ofr=1 (esempio di clausola "uso lecito e corretto", via ricerca)

AI Act:
- https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article50-watermarking-deadline/ (21/9/2026)
- https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/ (via ricerca)
- https://www.jonesday.com/en/insights/2026/06/european-commission-publishes-final-code-of-practice-on-marking-and-labelling-aigenerated-content

Modelli vocali:
- https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b
- https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 ; https://huggingface.co/istupakov/parakeet-tdt-0.6b-v3-onnx ; https://huggingface.co/OpenASR/parakeet-tdt-0.6b-v3 (via ricerca)
- https://alphacephei.com/vosk/models
- https://huggingface.co/kyutai/pocket-tts ; https://github.com/kyutai-labs/pocket-tts ; https://huggingface.co/kyutai/tts-voices
- https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base
- https://huggingface.co/nvidia/magpie_tts_multilingual_357m ; https://huggingface.co/blog/nvidia/magpie-tts-multilingual-voice-agents
- https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512
- https://github.com/resemble-ai/chatterbox
- https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- https://huggingface.co/rhasspy/piper-voices
- https://huggingface.co/canopylabs/3b-es_it-ft-research_release ; https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct/blob/main/LICENSE.txt
- https://huggingface.co/coqui/XTTS-v2 ; https://github.com/SWivid/F5-TTS
- https://www.kdnuggets.com/open-weight-text-to-speach-with-voxtral-tts ; https://neelshah18.com/blog/mistral-voxtral-tts-open-weight-speech-model/ (via ricerca)

Claude:
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://platform.claude.com/docs/en/build-with-claude/thinking
- https://platform.claude.com/docs/en/api/migration-2026-10-21 (via ricerca)
- https://artificialanalysis.ai/providers/anthropic ; https://artificialanalysis.ai/models/claude-haiku-5-5

GPU:
- https://www.computerbase.de/2024-02/rtx-2000-ada-generation-gpu-nvidias-kleinste-workstation-grafikkarte-mit-16-gb-bei-70-watt/ ; https://www.cgchannel.com/?p=169367 ; https://emarque.co/products/nvidia-rtx-pro-2000-blackwell-professional-graphics-card (rilevazione precedente di oggi)
- https://gpuprix.com/italy/gpus/rtx-pro-2000-blackwell ; https://www.mediaworld.it/it/product/_nvidia-rtx-pro-2000-blackwell-16-gb-gddr7-scheda-grafica-16-gb-166218270.html
- https://www.yeppon.it/products/pny-scheda-grafica-rtx-1286630 ; https://www.it-partners.it/apps/aeo/ai/md/default/products/dell-nvidia-rtx-2000-ada-16gb-gddr6-dell-m7x81.md (via ricerca)
- https://www.hardwaredealz.com/hardware/gpu/nvidia-20gb-gddr6-4x-mdp/preisvergleich.25062 ; https://gpuprix.com/eu/gpus/rtx-4000-sff-ada-generation ; https://www.jacob.de/produkte/pny-vcnrtx4000adalp-pb-grafikkarte-vcnrtx4000adalp-pb-artnr-8312099.html (via ricerca)
- https://www.hardwaredealz.com/hardware/gpu/nvidia-rtx-pro-4000-blackwell-sff-edition-24gb/pny-24gb-gddr7-4x-mdp/preisvergleich.30573 (via ricerca)
