# 30. L'agente che entra in ogni call, senza Recall.ai

Bot di riunione e trascrizione in casa per le funzioni J5, A1 e C2, e a valle per C3, C5, K4, B1-B4 e G1. Seconda stesura, con le fonti ricontrollate il 25/10/2026. Per Alberto, Michele, Mattia e Alessandro. Il vincolo fisso è il board dell'infrastruttura di Michele (`allegati/infra/`).

**Etichette.** [verificato: fonte] vuol dire letto nella fonte indicata. «Secondaria» vuol dire una fonte terza (rivista, blog, rivenditore). [non verificato] vuol dire stima, proposta o dato da provare. Prezzi in euro IVA inclusa, con la data in cui li abbiamo letti.

## In breve

Senza Recall.ai la cosa regge, ma non con un solo strumento. Le riunioni sono di quattro tipi e ognuno ha la sua strada.

1. **Riunioni Teams organizzate da SerSan: nessun bot.** Usiamo la trascrizione nativa di Teams, che resta in M365 (ammesso dal board), e la scarichiamo sul server con Microsoft Graph. Non servono Teams Premium né Copilot. Le API delle trascrizioni sono gratuite: Microsoft le ha tolte dal pagamento a consumo dal 25/08/2025 e non chiede più un abbonamento Azure [verificato: learn.microsoft.com, «Fetch Meeting Transcripts & Recordings», aggiornata il 30/09/2026, e «Metered APIs and services»]. Questo conta, perché Azure esce. Vanno accesi due interruttori che sono spenti di serie: l'accesso di Graph alle trascrizioni e i nomi di chi parla [verificato: learn.microsoft.com, «Manage transcript API access», 23/07/2026].
2. **Riunioni organizzate dai clienti (Teams di un altro tenant, Google Meet, Zoom): il bot self-hosted Vexa** (Apache-2.0, versione stabile 0.12.28 del 09/10/2026), in una VM isolata, con la trascrizione sul nostro server [verificato: API GitHub]. Piano B: Attendee (Elastic License 2.0). Attenzione: nel 2026 le tre piattaforme hanno chiuso le porte ai bot. Teams li manda in sala d'attesa con l'etichetta «Unverified» e l'amministratore del cliente può bloccarli del tutto. Meet mette gli ospiti «a rischio» in una coda rifiutata di serie. Zoom chiede alle app SDK un token legato a un utente già presente, e alcune riunioni rifiutano i browser automatici [verificato: mc.merill.net MC1251206; secondaria, office365itpros.com 24/08/2026, uctoday.com 25/03/2026; developers.zoom.us, FAQ OBF; note di rilascio Vexa 0.12.26]. Quindi il bot entra solo se il cliente lo ammette, e serve sempre una riserva: la registrazione sul PC di chi partecipa.
3. **Riunioni dal vivo: il telefono.** Registrazione con l'app di sistema, invio al server via NetBird con un Comando rapido (iPhone) o con «Condividi» (Android), poi trascrizione e riconoscimento dei parlanti a lotti.
4. **Trascrizione in italiano sul server.** Dal vivo: faster-whisper large-v3-turbo in int8, circa 2,1 GB di memoria GPU [verificato: Vexa, `deploy/transcription/.env.example`]. A lotti: NVIDIA Parakeet TDT 0.6B v3, errore sulle parole in italiano del 3,00 % su FLEURS, licenza CC-BY-4.0 [verificato: huggingface.co/nvidia/parakeet-tdt-0.6b-v3], oppure WhisperX. Per i parlanti: pyannote community-1 [verificato: huggingface.co/pyannote].

**La GPU.** La Quadro RTX 4000 da 8 GB è già quasi piena con il modello 4B, embedding, reranker e Docling, e la sera va a Experimental-1 [verificato: board]. La trascrizione dal vivo ci sta di giorno solo spostando il reranker sulla CPU. Per questo propongo tre modi: GPU di giorno, CPU la sera, e tutto sulla seconda GPU quando arriva. La CPU basta per i lotti: Parakeet in ONNX fa 36 volte il tempo reale su una CPU da scrivania [verificato: README onnx-asr]. La seconda GPU deve essere da **16 GB**: va divisa con la voce di Andrea (rapporto 31). La «A2000 con chip Ada da 6 GB GDDR7» del messaggio di Michele non esiste. Consiglio la RTX 2000 Ada 16 GB, 70 W, circa 650-920 € in negozi europei (rilevato il 25/10/2026) [verificato: secondaria, MediaMarkt BE, Datafox, OX.ee; 25 §H07].

**Stima: 22-29 giorni-persona**, di cui circa 13,5-16,5 di Mattia e 5,5-6,5 di Michele. Licenze software: 0 €. Recall.ai non serve più (circa 17 €/mese in meno con 30 ore di call [verificato: 22 §6]). La parte Teams si può fare subito, prima del server. Bot e trascrizione locale arrivano con la fase F4 del board (LXC GPU).

---

## 1. Cosa deve fare e con quali vincoli

**Le funzioni** [verificato: `00-visione-funzionalita.md`]:
- J5: l'agente delle chiamate entra da solo in ogni chiamata e trascrive tutto.
- A1: tutte le riunioni, in call o dal vivo, registrate dichiarandolo e trascritte.
- C2: un agente in ogni call, anche al posto di chi manca.
- A valle: C3 (analisi della call con Claude), C5 (registro dei meeting), K4 (chiedere alla memoria cosa si è detto), B1-B4 (flusso dopo la call), G1 (call di vendita in un canale).

**I vincoli del board** [verificato: `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`]:
- In cloud restano solo M365/Entra ID, Claude Team, API Anthropic dietro LiteLLM, Cloudflare, GitHub, Supabase, Vercel, Jira, Instantly e un S3 facoltativo. Azure esce. Tutto il resto è self-hosted.
- GPU Quadro RTX 4000 da 8 GB: di giorno all'AI (VLAN 80), la sera alla VM Experimental-1. La seconda GPU, nella fase F5, resterà fissa sull'AI.
- VLAN con default-deny. APPS esce su allowlist; AI esce solo per scaricare i modelli; DATA non esce.
- Accesso solo da NetBird (SSO Entra più chiave FIDO2) e da Pangolin con Traefik. Nessuna porta aperta.
- Perimetro Cyber Essentials: patch entro 14 giorni, account non amministratori, software supportato.
- RAM libera per crescere: circa 53 GB.

**I volumi.** Il piano precedente contava 30 ore di riunione al mese all'inizio e 100 a regime [verificato: 22 §6]. Con quattro persone, 100 ore sono circa 5 ore per giorno lavorativo. Di rado ci saranno più di due call insieme [non verificato: stima].

**Cosa cambia.** La presentazione usava Recall.ai nella fase 1 e una prova di Vexa [verificato: PRESENTAZIONE-CEO §6 e 22 §4]. Il rapporto 25 toglie Recall.ai [verificato: 25, C06]. Qui tutto passa in casa, tranne la trascrizione nativa di Teams, che resta in M365.

---

## 2. Le quattro situazioni da coprire

| Situazione | Chi organizza | Strada consigliata | Riserva |
|---|---|---|---|
| Call Teams creata da noi (interna o con clienti) | SerSan | Trascrizione nativa di Teams, scaricata con Graph | Registrazione sul PC di chi partecipa |
| Call Teams creata dal cliente | tenant del cliente | Bot Vexa come ospite | Registrazione sul PC |
| Google Meet o Zoom del cliente | cliente | Bot Vexa come ospite (Zoom dal client web) | Registrazione sul PC |
| Riunione dal vivo | chiunque | Telefono, poi invio al server | Portatile con vivavoce da sala |

Perché la prima riga non usa il bot. Nelle riunioni del nostro tenant Teams attribuisce ogni frase alla persona giusta, mostra da solo l'avviso di registrazione e non ha il problema dei bot «Unverified». Nelle riunioni degli altri invece non possiamo usarla: chi è di un'altra organizzazione, gli ospiti e gli anonimi non possono avviare la trascrizione [verificato: support.microsoft.com, «I can't transcribe a meeting in Microsoft Teams»].

---

## 3. La trascrizione nativa di Teams con Microsoft Graph

### 3.1 Licenze e costi

| Cosa | Serve? | Etichetta |
|---|---|---|
| Licenza M365 con Teams per chi organizza | Sì. Business Basic, Standard, Premium, E3 ed E5 includono la trascrizione | [verificato: secondaria, practical365.com, avviso MC260564]. Da controllare per i nostri quattro utenti con lo strumento di diagnostica delle trascrizioni nel centro di amministrazione M365 [verificato: learn.microsoft.com, «Manage transcription and captions»] |
| Teams Premium | No. Serve per traduzione dal vivo, riepilogo intelligente, modelli che impongono la registrazione, scelta di chi può registrare | [verificato: learn.microsoft.com, «Recording and transcription overview», aggiornata il 18/08/2026] |
| Microsoft 365 Copilot | No. Serve solo per il riepilogo intelligente e il dizionario personalizzato | [verificato: stessa pagina] |
| Costo delle API Graph | Zero. «Starting August 25, 2025, the Teams APIs are no longer metered» | [verificato: learn.microsoft.com, «Metered APIs and services in Microsoft Graph» e «Fetch Meeting Transcripts & Recordings»] |
| Abbonamento Azure | No. Serviva solo per le API a consumo | [verificato: stesse pagine] |

Nota: il rapporto 25 riportava, da una fonte terza, che le API erano a consumo [verificato: 25, N05, da docs.glean.com]. Le pagine Microsoft di oggi dicono il contrario. Vale Microsoft.

L'italiano («Italian (Italy)») è tra le lingue della trascrizione [verificato: learn.microsoft.com, «Manage transcription and captions»].

### 3.2 Impostazioni da accendere (Michele, circa 1 giorno)

1. **Accesso di Graph alle trascrizioni.** Spento di serie. Da spento, ogni richiesta risponde `403 GraphAccessToTranscriptsDisabled`, qualunque permesso abbia l'app [verificato: learn.microsoft.com, «Manage transcript API access» e «Get callTranscript»].
2. **Nomi di chi parla nelle trascrizioni via Graph.** Spento di serie. Da spento, il formato VTT con i nomi risponde `403 SpeakerAttributionNotAllowed` [verificato: stesse pagine]. Comando unico: `Set-CsTeamsMeetingConfiguration -EnableGraphTranscriptAccess true -EnableAttributedTranscripts true -Identity Global` [verificato: «Manage transcript API access»].
3. **Criterio di riunione**: trascrizione (`-AllowTranscription`) e registrazione accese per i quattro utenti [verificato: «Manage transcription and captions»].
4. **Link alla nostra informativa** al posto di quella standard, nell'avviso di registrazione [verificato: «Recording and transcription overview», voce «Privacy and security URL»].
5. **Scadenza** di registrazioni e trascrizioni in OneDrive allineata alla nostra regola: audio fino a 30 giorni [verificato: 16 regola 8; l'impostazione esiste, «Recording and transcription overview»].
6. **Chi ammette dalla sala d'attesa**: solo organizzatore e co-organizzatori. Così un ospite non può far entrare un bot di terzi [verificato: secondaria, office365itpros.com 24/08/2026, consiglio agli amministratori; proprietà `allowedLobbyAdmitters` in learn.microsoft.com, «onlineMeeting resource type»].
7. **Bot esterni nelle nostre riunioni.** Il criterio `ExternalBotAccessMode` ha tre valori: `AllowAllBots`, `RequireApprovalWhenDetected` (quello di serie) e `BlockDetectedBots` [verificato: secondaria, uctoday.com 30/06/2026; office365itpros.com 24/08/2026]. Da decidere cosa fare con i notetaker dei clienti (domanda aperta 7).
8. **Consenso esplicito** (facoltativo, §8): `-ExplicitRecordingConsent Enabled`. Non serve Premium [verificato: learn.microsoft.com, «Manage participant agreement for recording and transcription», 05/05/2026].

Attenzione: se chi organizza spegne Copilot nella riunione, si spengono anche registrazione e trascrizione [verificato: «Manage transcription and captions»].

### 3.3 L'app in Entra e i permessi

- Lettura: permesso applicativo `OnlineMeetingTranscript.Read.All` [verificato: learn.microsoft.com, «Get callTranscript», aggiornata l'01/10/2026].
- Call veloci senza calendario (ad hoc): `CallTranscripts.Read.All` [verificato: stessa pagina].
- Scrittura delle opzioni della riunione (§3.6): `OnlineMeetings.ReadWrite.All` [verificato: learn.microsoft.com, «Update onlineMeeting»].
- Per i permessi applicativi serve un **criterio di accesso applicativo** creato dall'amministratore e assegnato ai quattro utenti. Senza, il permesso da solo non basta [verificato: «Get callTranscript» e «Update onlineMeeting»].
- Il segreto dell'app va in Infisical (VLAN DATA), come gli altri [non verificato: proposta coerente con il board].

### 3.4 Come scaricare senza aprire porte

Due modi documentati:
- **Notifiche di cambiamento** su `users/{id}/onlineMeetings/getAllTranscripts`. Servono un URL pubblico HTTPS (quindi un endpoint dietro Pangolin) e un certificato per decifrare il contenuto [verificato: learn.microsoft.com, «teams-changenotifications-callrecording-and-calltranscript»].
- **Interrogazione periodica con delta** su `getAllTranscripts`: la prima volta tutto, poi solo le novità [verificato: learn.microsoft.com, «onlineMeeting: getAllTranscripts»].

Consiglio: **delta ogni 5-10 minuti da n8n**. Nessuna porta in ingresso, coerente con il board. La trascrizione arriva pochi minuti dopo la fine della call: per il recap basta [non verificato: tempo da misurare].

Il contenuto arriva in WebVTT con il nome di chi parla per ogni frase. Il formato docx è deprecato dal 31/05/2023 [verificato: «Get callTranscript»].

### 3.5 Limiti da conoscere

- Non funziona con le riunioni create via API senza un evento in calendario. Le riunioni vanno create come eventi [verificato: «Get callTranscript»].
- Una riunione online scade 60 giorni dopo l'inizio o la fine, se non viene aggiornata [verificato: «onlineMeeting resource type»]. Scarichiamo subito, quindi non pesa.
- Le trascrizioni stanno nel OneDrive di chi organizza [verificato: «Manage transcription and captions»]. È cloud M365, ammesso dal board.

### 3.6 Farla partire da sola, anche quando manca qualcuno (C2)

- L'opzione «Registra e trascrivi automaticamente» è disponibile anche senza Premium, ma è spenta di serie e va accesa riunione per riunione [verificato: «Recording and transcription overview»].
- La riunione online ha le proprietà `recordAutomatically` e `meetingSpokenLanguageTag` (per esempio `it-IT`), modificabili via Graph [verificato: «onlineMeeting resource type» e «Update onlineMeeting»]. L'agente agenda le accende sugli eventi nostri, solo se l'evento ha il flag «avvisato» (§8).
- **Punto da provare:** la registrazione automatica parte quando entra qualcuno della nostra organizzazione. Se entra solo il cliente, probabilmente non parte [verificato: secondaria, risposta su Microsoft Q&A e guida di Jiminny; non confermato da Microsoft]. Quindi C2 nelle nostre riunioni va provato con una call di test (§11, lavoro 10). Se non regge, la riserva è un collega di SerSan collegato anche solo con l'audio spento, oppure il bot Vexa sulla nostra riunione.

---

## 4. Bot open source self-hosted

### 4.1 Confronto

Dati letti il 25/10/2026 dall'API di GitHub e dalla documentazione dei progetti.

| Progetto | Licenza | Piattaforme | Trascrizione | Stato | A favore | Contro |
|---|---|---|---|---|---|---|
| **Vexa** | Apache-2.0 | Meet, Teams, Zoom «in produzione»; Jitsi da validare | faster-whisper nostro, API compatibile OpenAI | stabile 0.12.28 del 09/10/2026; 0.13.1 alpha del 07/09/2026 «non per la produzione»; 2.907 stelle; 722 segnalazioni aperte | trascrizione in casa già pronta, calendario, ingresso automatico, MCP, registrazioni su S3 nostro, cancellazione per riunione | in 0.12 non parla e non scrive in chat; rilasci quasi settimanali |
| **Attendee** | Elastic License 2.0 | Zoom, Meet, Teams | servizi esterni oppure «Custom Async» verso un nostro servizio, solo in self-host | 1.84.6 del 22/10/2026; 770 stelle | API ricca: chat, voce, calendario, webhook; flussi audio separati per persona su Meet e Zoom | Zoom con Meeting SDK e token OBF; in produzione Kubernetes, con la guida di installazione nel piano a pagamento; bot Teams con login solo con un tenant a parte e MFA spento |
| joinly | MIT | Meet, Zoom, Teams via browser | Whisper locale | 0.5.4 del 01/09/2026 | l'agente parla e agisce in riunione via MCP | il server MCP non ha autenticazione; non è una piattaforma di registrazione |
| screenappai/meeting-bot | MIT | Meet, Teams, Zoom | nessuna | 1.2.34 del 18/06/2026 | semplice | un lavoro alla volta |
| meetingbot/meetingbot | LGPL-3.0 | Meet, Teams, Zoom | da aggiungere | ultimo aggiornamento 09/04/2026; 298 stelle | API aperta | poco attivo |
| Meetily (senza bot) | MIT | qualsiasi, cattura l'audio del PC | Whisper o Parakeet in locale | 0.4.1 del 12/09/2026 | nessun bot da far entrare | macOS e Windows (Linux da sorgente); nessun riconoscimento dei parlanti nella versione gratuita |
| Bot media di Teams (Microsoft) | n.a. | solo Teams | nostra | n.a. | integrazione ufficiale | in produzione su Windows Server in Azure: Azure esce, quindi escluso |
| Recall.ai (riferimento) | servizio USA | tutte | inclusa | n.a. | maturo | escluso da questa richiesta |

Fonti della tabella: Vexa [verificato: API GitHub, README, `docs/api/meetings.mdx`]; Attendee [verificato: API GitHub, LICENSE, README, docs.attendee.dev «Transcription» e «Signed In Bots»]; joinly, screenappai e Meetily [verificato: API GitHub e README, prima stesura del 25/10/2026; Meetily riletto oggi]; meetingbot [verificato: API GitHub]; bot media di Teams [verificato: learn.microsoft.com, «Requirements and considerations for application-hosted media bots»].

### 4.2 Vexa nel dettaglio

**Come entra.** Ogni bot è un browser senza schermo che entra come un partecipante qualsiasi [verificato: Vexa, `docs/core/meetings.mdx`]. Zoom entra dal client web. Le riunioni Zoom che chiedono RTMS non sono supportate [verificato: note di rilascio 0.12.26].

**Calendario.** Vexa sa leggere un calendario ICS e mandare il bot circa 60 secondi prima dell'inizio [verificato: `docs/api/meetings.mdx`, `auto_join`]. Consiglio di non usarlo: l'indirizzo ICS è una credenziale e non porta il flag «avvisato». Meglio che n8n legga il calendario con Graph e chiami `POST /bots` solo per gli eventi avvisati [non verificato: proposta].

**Sala d'attesa.** Su Meet e Teams il bot aspetta che qualcuno lo ammetta. Il tempo massimo di attesa si regola nei parametri di uscita automatica [non verificato: letto nella guida di Vexa nella prima stesura, non riletto oggi].

**Trascrizione.** È un servizio a parte con faster-whisper e API compatibile OpenAI, da mettere dove c'è la GPU. Modello consigliato `large-v3-turbo` in int8: «~2.1 GB VRAM, >10x real-time» [verificato: `deploy/transcription/.env.example`]. Esiste una variante solo CPU, per la quale Vexa consiglia un modello più piccolo [verificato: `docs/deployment.mdx`]. Richieste insieme: 20 di serie su GPU (tarato su una RTX 4090), 2 su CPU, modificabile con `MAX_ACTIVE_REQUESTS` [verificato: stessa pagina]. Senza servizio di trascrizione i bot entrano e registrano, ma non producono testo [verificato: docs.vexa.ai, «deployment-lite»].

**Lingua.** Con `language: "it"` ogni pezzo è trascritto in italiano. Senza, la lingua si riconosce per ogni finestra e quelle incerte restano senza lingua [verificato: `docs/api/meetings.mdx`]. Per i clienti UK lo impostiamo a `en` dal calendario.

**Chi parla.** Vexa non tira a indovinare: quando non è sicuro lascia vuoto il nome, nel 4-7 % delle righe con voci sovrapposte [verificato: README]. Su Teams i nomi arrivano parola per parola dai dati di trasporto dalla 0.12.22; su Zoom per partecipante dalla 0.12.26 [verificato: note di rilascio].

**Cosa manca nella 0.12.** Far parlare il bot e cambiare la configurazione durante la call rispondono 404; l'invio di messaggi in chat non è implementato [verificato: README e `docs/api/meetings.mdx`]. Quindi il bot non può presentarsi da solo: l'avviso passa dal nome del bot, dall'invito e dalla voce di chi conduce (§8). La 0.13 alpha aggiunge chat sulle trascrizioni e MCP con autenticazione, ma non ha ancora cancellazione e conservazione: da non usare [verificato: note di rilascio 0.13.1].

**Dati.** Registrazioni solo audio su uno storage S3 nostro; nelle versioni Lite e Compose c'è versitygw, e Helm accetta un S3 esterno come MinIO [verificato: README e note di rilascio 0.12.28]. Cancellazione per riunione dalla 0.12.24 [verificato: note di rilascio]. Una scadenza automatica a 30 giorni la scriviamo noi [non verificato: proposta].

**Due modi di installarlo.**
- **Compose** (consigliato): un container per bot avviato dal runtime tramite il socket di Docker [verificato: `docs/deployment.mdx`]. Il socket dà poteri da amministratore sulla macchina: per questo va in una VM sua (§4.5). Ogni bot chiede 1 CPU e 2.048 MiB, e oltre quel tetto viene chiuso a metà riunione [verificato: `deploy/helm/charts/vexa/values.yaml`]. Requisiti: Ubuntu 24.04 e Docker 26 o successivo; l'immagine del bot è solo amd64 [verificato: README e `docs/deployment.mdx`].
- **Lite**: un solo container, bot come processi, nessun socket di Docker, più Postgres e storage [verificato: docs.vexa.ai, «deployment-lite»]. Però i bot dividono un solo schermo virtuale, «best for one browser session at a time» [verificato: stessa pagina]. Va bene per partire con una call alla volta; con due call insieme serve Compose.

**Integrazione.** Vexa espone una API REST e un endpoint MCP su `/mcp` [verificato: README]. Il modulo riunioni non dipende dalla scelta fra Agent SDK e Hermes (§9).

### 4.3 Attendee come piano B

Attendee vince su due punti: scrive in chat, quindi può presentarsi da solo, e può parlare [verificato: README e documentazione API]. Usa anche i sottotitoli della piattaforma su Zoom e Meet, gratis e a bassa latenza [verificato: docs.attendee.dev, «Transcription»]. Perde su tre punti:
- **Zoom.** Usa il Meeting SDK. Dal 02/03/2026 Zoom chiede il token OBF per entrare in riunioni di altri account, e il token si ottiene solo per un utente che ha autorizzato l'app ed è già nella riunione [verificato: developers.zoom.us, FAQ OBF]. Quindi niente «al posto di chi manca» sugli Zoom esterni. Da luglio 2026 Zoom rifiuta anche le eccezioni per gli ingressi anonimi dei bot [verificato: secondaria, devforum.zoom.us, «Anonymous Join Exception»].
- **Esercizio.** Django con Postgres e Redis; il modo Celery di serie «is not suitable for production»; in produzione Kubernetes, con le istruzioni nel piano a pagamento [verificato: README].
- **Teams con login.** Chiede un'organizzazione Office 365 separata con l'autenticazione a due fattori spenta [verificato: docs.attendee.dev, «Signed In Bots»]. Va contro le nostre regole (SSO Entra con FIDO2, Cyber Essentials): da non usare.

La licenza ELv2 vieta di offrire il software a terzi come servizio gestito [verificato: LICENSE]. L'uso interno va bene.

### 4.4 Cosa fanno le piattaforme contro i bot nel 2026

- **Teams.** Con l'avviso MC1251206 (pubblicato il 13/03/2026, aggiornato il 22/09/2026) Teams riconosce i bot esterni, li mostra in sala d'attesa e chiede all'organizzatore di ammetterli. È acceso di serie per tutti; la disponibilità generale si chiude entro fine ottobre 2026 [verificato: mc.merill.net, MC1251206]. Con MC1459141 del 21/08/2026 arriva il blocco totale (`BlockDetectedBots`), disponibile entro fine settembre 2026 [verificato: secondaria, office365itpros.com 24/08/2026; uctoday.com 30/06/2026]. Microsoft ha un programma di identificazione per i fornitori di bot (per esempio Recall.ai, Otter, Read AI): i loro bot entrano riconosciuti, gli altri finiscono fra le «minacce sospette» [verificato: secondaria, office365itpros.com 24/08/2026]. Il nostro bot self-hosted non sarà riconosciuto.
- **Zoom.** Token OBF obbligatorio per le app SDK dal 02/03/2026 [verificato: FAQ Zoom]. Il client web di Vexa non ha bisogno dell'SDK, ma alcune riunioni rifiutano i browser automatici e chiedono RTMS [verificato: note di rilascio Vexa 0.12.26].
- **Google Meet.** Dal 24/03/2026 la sala d'attesa ha due code. Gli ospiti «a rischio», bot compresi, vengono rifiutati di serie se l'organizzatore non interviene [verificato: secondaria, uctoday.com 25/03/2026; avviso di MiiTel sul «safeguarded guest admit flow»].

Conseguenza pratica: il bot funziona quando il cliente lo ammette. Chi conduce la call lo dice all'inizio («entra il nostro assistente SerSan Verbale, lo ammettete?»). Se il cliente blocca i bot, l'unica strada è la registrazione sul PC di chi partecipa, con lo stesso avviso.

### 4.5 Rete e sicurezza (proposta per Michele)

- **Una VM dedicata** `meet-01` (Ubuntu 24.04, Docker) in una VLAN sua, per esempio «35 · MEET». Il browser del bot esegue codice di Teams, Meet e Zoom e il runtime usa il socket di Docker: va isolato dal resto [non verificato: proposta].
- **In uscita**: 443 e i media. Teams: UDP 3478-3481 verso 52.112.0.0/14, 52.122.0.0/15 e 2603:1063::/38 [verificato: learn.microsoft.com, «Microsoft 365 URLs and IP address ranges», ID 11, letto tramite ricerca]. Meet: UDP 3478 e 19302-19309 [verificato: knowledge.workspace.google.com, «Prepare your network for Meet»]. Zoom: elenco sul sito di supporto di Zoom [non verificato: non letto]. Le pagine dei client caricano risorse da molti domini, quindi un'allowlist per dominio è fragile. Propongo uscita aperta su 443 solo da questa VLAN, senza rotte verso DATA [non verificato: proposta].
- **In ingresso**: solo da APPS (n8n) verso l'API di Vexa. Nessuna esposizione su Pangolin.
- **Verso DATA**: solo il bucket delle registrazioni su MinIO, oppure niente e un worker in APPS che preleva i file.
- **Testo di terzi**: le trascrizioni entrano dalla corsia senza strumenti già prevista, perché qualcuno in call può dire frasi che sembrano istruzioni [verificato: 22 §2; 26 §11].

---

## 5. Trascrizione locale in italiano

### 5.1 I modelli

| Modello | Licenza | Italiano | Cosa conta per noi | Etichetta |
|---|---|---|---|---|
| Whisper large-v3-turbo con faster-whisper | MIT | sì | modello dal vivo di Vexa; int8 circa 2,1 GB | [verificato: Vexa `.env.example`] |
| Whisper large-v2/v3 con faster-whisper | MIT | sì | misura ufficiale su RTX 3070 Ti 8 GB: int8 59 s con 2.926 MB; int8 a lotti da 8, 16 s con 4.500 MB; fp16 a lotti, 17 s con 6.090 MB | [verificato: README faster-whisper] |
| WhisperX | BSD-2 | sì, allineamento delle parole per `it` incluso | faster-whisper più allineamento più pyannote community-1; «<8GB gpu memory for large-v2»; chiede CUDA 12.8; ultima stabile 3.8.6 del 25/05/2026 | [verificato: README WhisperX; API GitHub] |
| **Parakeet TDT 0.6B v3** (NVIDIA) | CC-BY-4.0, uso commerciale ammesso | sì, 25 lingue europee | errore sulle parole: FLEURS 3,00 %, MLS 10,08 %, CoVoST 3,69 %; punteggiatura e maiuscole; tempi per parola; fino a 24 minuti in attenzione piena, 3 ore in attenzione locale; Turing non è fra le architetture elencate, ma la T4 (Turing) è fra le schede di prova | [verificato: huggingface.co/nvidia/parakeet-tdt-0.6b-v3] |
| Parakeet v3 con onnx-asr | MIT (libreria) | sì | 36 volte il tempo reale su CPU Ryzen 9800X3D; 57 su una T4 con CUDA; audio lungo con VAD | [verificato: README onnx-asr] |
| Canary-1b-v2 (NVIDIA) | CC-BY-4.0 | sì, anche traduzione da e verso l'inglese | circa 1 miliardo di parametri | [verificato: huggingface.co/nvidia/canary-1b-v2, prima stesura] |
| Nemotron 3.5 ASR streaming 0.6B | OpenMDW-1.1 | sì | streaming vero; FLEURS 4,41 % a blocchi di 560 ms; è il modello scelto per Andrea nella fase 2 | [verificato: 31 §5] |
| Qwen3-ASR 1.7B / 0.6B | Apache-2.0 | sì | streaming solo con vLLM | [verificato: 13 §5] |
| Voxtral Mini 4B Realtime (Mistral) | Apache-2.0 | sì | serve una GPU da almeno 16 GB da sola | [verificato: huggingface.co/mistralai, prima stesura] |

Nessuno di questi numeri è misurato su audio di SerSan. Serve la prova del §11 (lavoro 10), con accento sardo, inglese dei clienti UK e voci sovrapposte.

### 5.2 Chi parla

- **Nelle call online** il nome arriva dalla piattaforma. Teams lo scrive nel VTT [verificato: «Get callTranscript»]. Vexa usa gli eventi di chi parla [verificato: README Vexa]. Attendee ha flussi separati per persona su Meet e Zoom; su Teams il client web dà un solo flusso misto e si usano gli eventi [verificato: docs.attendee.dev, «Transcription»].
- **Nelle riunioni dal vivo** serve il riconoscimento dei parlanti. **pyannote speaker-diarization-community-1**: CC-BY-4.0; si scarica dopo aver accettato le condizioni su Hugging Face e poi funziona senza rete [verificato: huggingface.co/pyannote/speaker-diarization-community-1]. Errore su AMI: 17,0 % (microfoni personali) e 19,9 % (un solo microfono), contro 18,8 e 22,7 della 3.1; il modello a pagamento precision-2 fa 12,9 e 15,6 [verificato: stessa pagina]. Serve pyannote.audio 4.x [verificato: stessa pagina]. Sulla RTX 4000 un'ora di audio richiederà qualche minuto [non verificato: stima].
- La telemetria facoltativa di pyannote va spenta con `PYANNOTE_METRICS_ENABLED=0` [verificato: README pyannote, prima stesura]. In ogni caso la VLAN AI esce solo per scaricare modelli.
- Il nome vero si associa dopo. Chi carica la registrazione indica i presenti; un passaggio con Claude, o con il modello locale per i dati rossi, propone chi è «Parlante 1»; la persona conferma [non verificato: proposta].

### 5.3 Turing: cosa conta

- La RTX 4000 (Turing) non ha BF16 né FlashAttention 2 [verificato: 13 punto 4].
- CUDA 13 ha tolto Maxwell, Pascal e Volta: Turing è ora la generazione più vecchia supportata [verificato: docs.nvidia.com, CUDA Features Archive 13.3, prima stesura]. Va bene oggi, ma sarà la prossima a uscire.
- faster-whisper chiede CUDA 12 e cuDNN 9 [verificato: README faster-whisper]; WhisperX chiede CUDA 12.8 [verificato: README WhisperX].

### 5.4 Due passaggi

1. **Dal vivo**, durante la call: Vexa con large-v3-turbo int8. Serve al recap subito dopo e, in futuro, a un copilota in call.
2. **A lotti**, dopo la call e per tutte le riunioni dal vivo: Parakeet v3 (o WhisperX large-v3) più pyannote. Nelle call online, dove il nome arriva dalla piattaforma, il secondo passaggio si fa solo se la prova mostra che migliora davvero [non verificato: da misurare].

Poi il testo segue la pipeline del board: filtro dei segreti, blocchi e metadati con Qwen3-4B, embedding in Qdrant più BM25, reranker, MCP RAG verso Claude Team [verificato: board, «Pipeline AI»].

---

## 6. Memoria GPU

### 6.1 Quadro RTX 4000, 8 GB, com'è oggi

| Componente | Memoria GPU | Etichetta |
|---|---|---|
| Ollama, Qwen3-4B Q5_K_M (board) | circa 3,5-4,2 GB con il contesto | [non verificato: stima del 31 §8.1; servizio verificato nel board] |
| Infinity, embedding e reranker Qwen3 0.6B FP16 | circa 3 GB in tutto (circa 1,3-1,6 GB ciascuno) | [non verificato: stima del 31 §8.1] |
| Docling quando indicizza | a picchi | [non verificato] |
| **Libero** | **meno di 1 GB** | [non verificato: stima, coerente con 25 H06 e 31 §8.1] |
| faster-whisper large-v3-turbo int8, dal vivo | circa 2,1 GB | [verificato: Vexa `.env.example`] |
| faster-whisper large-v3 int8 a lotti da 8 | circa 4,5 GB (misura su large-v2, stessa taglia) | [verificato: README faster-whisper] |
| Parakeet v3 FP16 a blocchi | circa 2-3 GB | [non verificato: stima] |
| pyannote community-1 | circa 1-1,5 GB | [non verificato: stima] |

**Conclusione**: di giorno la trascrizione dal vivo entra solo se il reranker passa sulla CPU (si liberano circa 1,5 GB) e Docling lavora fuori dagli orari delle call. Il margine resta sotto 1 GB [non verificato: stima da misurare con `nvidia-smi` nella fase F4]. La sera la GPU non c'è.

### 6.2 Tre modi per il servizio di trascrizione

| Modo | Quando | Dal vivo | A lotti | Etichetta |
|---|---|---|---|---|
| **A, GPU di giorno** | fascia AI della RTX 4000 | turbo int8 sulla GPU, reranker sulla CPU | Parakeet o large-v3 quando Ollama ha scaricato il modello, altrimenti CPU | [non verificato: proposta] |
| **B, CPU** | la sera, con la GPU a Experimental-1, o se la GPU è piena | turbo int8 su CPU con al massimo 2 richieste insieme, oppure solo cattura (bot senza testo) | Parakeet int8 su CPU subito dopo la call | 2 richieste su CPU [verificato: Vexa `docs/deployment.mdx`]; velocità sugli Xeon [non verificato] |
| **C, seconda GPU** | dalla fase F5 | tutto sulla nuova scheda | tutto sulla nuova scheda | [non verificato: proposta] |

Lo script di Michele che passa la GPU a Experimental-1 deve prima fermare trascrizione, Ollama e Infinity, perché la scheda deve essere libera [non verificato: da provare con lo script]. Lo stesso script porta il servizio di trascrizione nel modo B.

**Quanto è lenta la CPU.** Parakeet v3 in ONNX fa 36 volte il tempo reale su una CPU da scrivania recente [verificato: README onnx-asr]. Gli Xeon Gold 5218 sono più lenti per core ma hanno 64 thread e le istruzioni AVX-512 [verificato: board per i thread; AVX-512 non verificato]. Stima: un'ora di audio in 3-6 minuti con 16 thread [non verificato: da misurare]. Per il recap dopo la call basta.

### 6.3 La seconda GPU, da dividere con Andrea

La seconda GPU, nella fase F5, «resterà fissa sull'AI» [verificato: board]. Non sarà solo nostra: il rapporto 31 la usa anche per la voce di Andrea nella fase 2 [verificato: 31 §8.3]. Ecco il conto insieme.

| Carico | Memoria | Etichetta |
|---|---|---|
| Andrea fase 2: Nemotron streaming più Qwen3-TTS 0.6B, una telefonata | circa 5 GB | [non verificato: stima del 31 §8.3] |
| Andrea con 2-3 telefonate o una voce più grande | circa 7-9 GB | [non verificato: stima del 31 §8.3] |
| Call, dal vivo: turbo int8 | circa 2,1 GB | [verificato: Vexa] |
| Call, a lotti: Parakeet più pyannote | circa 3-4,5 GB | [non verificato: stima] |
| Modello 4B, embedding e reranker (se passano qui la sera) | circa 6,5-7 GB | [non verificato: stima del 31 §8.1] |

| Combinazione | Totale | 6 GB | 12 GB | 16 GB |
|---|---|---|---|---|
| Solo audio delle call (dal vivo più lotti) | circa 5-6,6 GB | al limite | sì | sì |
| Audio delle call più Andrea (una telefonata) | circa 10-11,6 GB | no | al limite | sì |
| Audio delle call più Andrea (2-3 telefonate) | circa 12-15,6 GB | no | no | al limite: i lotti si accodano |
| Audio, Andrea e tutta la pipeline RAG insieme | circa 17-23 GB | no | no | no |

[non verificato: somme delle stime sopra]

**Come la dividerei.** Di giorno la RTX 4000 tiene la pipeline RAG, come nel board. La seconda GPU tiene Andrea e l'audio delle call, con i lotti in coda quando Andrea è occupato. La sera embedding e reranker passano sulla CPU (proposta già nel 25, N06) e la seconda GPU non cambia. Così nessuno resta senza GPU [non verificato: proposta].

**Un risparmio da provare.** Andrea nella fase 2 usa Nemotron o Parakeet. Se lo stesso server fa anche la trascrizione delle call, il modello si carica una volta sola. Vexa parla con un servizio compatibile OpenAI e dalla 0.12.26 accetta anche risposte di solo testo [verificato: note di rilascio 0.12.26]. Serve però un piccolo adattatore davanti a Parakeet [non verificato: da provare].

**Quale scheda.** Il messaggio di Michele parla di «RTX A2000 con chip Ada da 6 GB GDDR7»: questa scheda non esiste [verificato: 25 H07; 31 §8.3].

| Scheda | Memoria | Consumo | Prezzo (rilevato) | Etichetta |
|---|---|---|---|---|
| RTX A2000 (Ampere) | 6 o 12 GB GDDR6 | 70 W | 12 GB: 499-569 € su eBay.de (25/10/2026) | [verificato: 25 H07 e 31 §8.3] |
| **RTX 2000 Ada** | 16 GB GDDR6 ECC, 128 bit | 70 W, dallo slot | 712-916 € in negozi in Belgio ed Estonia; 648-770 € su comparatori tedeschi e italiani (25/10/2026); prezzo italiano corrente non trovato | [verificato: secondaria, MediaMarkt BE, Datafox, OX.ee; 25 §5 punto 3] |
| RTX PRO 2000 Blackwell | 16 GB GDDR7 ECC, PCIe 5.0 x8, profilo basso | 70 W | da 1.090 € su Amazon.it (gpuprix, 24/10/2026); 1.501 € da MediaWorld (25/10/2026) | [verificato: secondaria, gpuprix.com e mediaworld.it] |
| RTX 4000 SFF Ada | 20 GB GDDR6 ECC | 70 W | 1.320-2.457 € (minimo europeo 2.457 € al 24/09/2026) | [verificato: secondaria, gpuprix.com, hardwaredealz.com] |

Per l'audio consiglio la **RTX 2000 Ada da 16 GB**. Costa meno della Blackwell, ha BF16 e FlashAttention 2, e l'ecosistema la supporta da anni. Un segnale: Scriberr chiede un'immagine dedicata per le schede Blackwell, mentre da Pascal ad Ada basta quella standard [verificato: README Scriberr]. La 20 GB serve solo se si vuole tutto su una scheda 24 ore su 24, ma costa il doppio. Da controllare con Michele: riser e slot del DL380 Gen10 accanto alla RTX 4000, e se la scheda è a doppio slot [non verificato: QuickSpecs HPE non lette per queste schede].

---

## 7. Riunioni dal vivo dal telefono

| Modo | Come funziona | A favore | Contro | Etichetta |
|---|---|---|---|---|
| **App di sistema più invio** (consigliato) | iPhone: Memo vocali, poi un Comando rapido «Invia a SerSan» che manda il file all'endpoint interno. Android: registratore di sistema, poi «Condividi» verso lo stesso endpoint. Il telefono raggiunge il server con l'app NetBird | registra anche a schermo spento; nessuna app da costruire; l'audio va diretto sul server | un gesto in più alla fine | app NetBird per iOS e Android [verificato: docs.netbird.io]; il resto [non verificato: da provare] |
| Scriberr (self-hosted) | app web installabile con registratore integrato, cartella sorvegliata, Parakeet, Canary o Whisper, pyannote | potrebbe sostituire la pipeline a lotti e la pagina di caricamento | ultima versione 1.2.0 del 17/12/2025; accesso con JWT o chiavi API, nessun utente multiplo documentato: va messo dietro Pangolin con SSO; su iOS le registrazioni dentro un'app web sono da provare | [verificato: API GitHub, MIT, 3.114 stelle; README]; [non verificato: tenuta su iOS, segnalazioni sul forum Apple Developer, filo 797987] |
| Teams sul telefono | si apre una riunione Teams nella sala e la si trascrive | avviso e trascrizione automatici | tutto il parlato della sala finisce sotto un solo partecipante | [non verificato: comportamento da provare] |
| Portatile più vivavoce da sala | registrazione sul PC con un vivavoce USB | audio migliore, parlanti più facili da separare | un oggetto in più; circa 100-250 € | [non verificato: prezzo indicativo] |

**Flusso.** Il file arriva all'endpoint in APPS, finisce su MinIO, parte il lotto (Parakeet o WhisperX più pyannote). Chi ha registrato conferma i nomi dei parlanti da una pagina o da Teams. Poi il testo segue la pipeline del board.

**Avviso in sala.** Prima di premere il pulsante, una frase a voce (§8). Per le riunioni ricorrenti con un cliente, la nota anche nell'invito.

---

## 8. Avviso e consenso

Le regole generali sono già nel 16: legittimo interesse con avviso prima della registrazione, finalità e conservazione dichiarate, accesso limitato; il consenso dei dipendenti non è una base affidabile [verificato: 16 punto 6 e §1]. Regola 2: «nessuna registrazione senza avviso», e il bot entra solo se l'evento ha il flag «avvisato» [verificato: 16 §6]. DPIA obbligatoria per le registrazioni [verificato: 16 regola 9]. Resta il parere legale unico prima della fase 2 [verificato: 22 decisione 10]. Un provvedimento specifico del Garante sui bot di riunione non l'ho trovato; i commenti di settore rimandano a GDPR, Statuto dei lavoratori, AI Act e legge 132/2025 [verificato: secondaria, filodiritto.com e tomshw.it; ricerca del 25/10/2026].

**Tre livelli di avviso, sempre.**
1. **Nell'invito.** L'agente agenda aggiunge il testo e mette il flag «avvisato». Testo proposto [non verificato: proposta da far rivedere al legale]:
   > Per il verbale useremo un assistente AI di SerSan che registra e trascrive la riunione. Lo vedrete tra i partecipanti come «SerSan Verbale (AI, registra)». L'audio si cancella entro 30 giorni; la trascrizione serve solo per il verbale e il seguito del lavoro. Se preferite di no, rispondete a questa mail o ditelo all'inizio: lo togliamo subito. Informativa: [link].

   Per i clienti UK la stessa frase in inglese.
2. **Nella riunione.** Nelle nostre riunioni Teams l'avviso di registrazione compare a tutti, con il link alla nostra informativa (§3.2 punto 4). Con il bot, l'avviso è il suo nome, perché Vexa 0.12 non scrive in chat (§4.2).
3. **A voce**, da chi conduce: «Prima di iniziare: c'è il nostro assistente AI che registra e trascrive per il verbale. Va bene per tutti?». Se qualcuno dice no, si toglie il bot o si ferma la registrazione, e la riunione si segna «non registrata».

**Quando nessuno di SerSan è in call (C2).** Il bot entra solo se l'invito era avvisato. Nelle riunioni dei clienti è comunque l'organizzatore ad ammetterlo, vedendone il nome. Se non lo ammette, non si registra.

**Consenso esplicito di Teams** (facoltativo). Chiede a ciascuno Sì o No prima di parlare; chi dice No ha una vista di sola lettura; la scelta va nel report presenze e nei log di audit [verificato: learn.microsoft.com, «Manage participant agreement»]. Prova forte di trasparenza, ma all'inizio tutti sono muti finché non rispondono. Da provare prima con le riunioni interne.

**Riunioni interne e Statuto dei lavoratori.** Se in Italia ci sono dipendenti, gli strumenti da cui deriva un possibile controllo a distanza chiedono un accordo sindacale o l'autorizzazione dell'Ispettorato (art. 4 dello Statuto) [verificato: 16 punto 4 e §1]. Registrare tutte le riunioni interne può rientrarci. Se le quattro persone sono soci o amministratori e non dipendenti, l'art. 4 non si applica, ma GDPR e AI Act sì [verificato: 16 §3, domanda aperta]. Va chiarito prima di accendere la registrazione sulle riunioni interne (domanda aperta 10).

**Opposizione e cancellazione.** Un comando nella chat del team («cancella la registrazione di ...») avvia la cancellazione su Vexa, MinIO e OneDrive, con ricevuta [non verificato: da costruire].

**Conservazione.** Audio fino a 30 giorni, trascrizioni 24 mesi dall'ultimo contatto [verificato: 16 regola 8]. Vale per Vexa (lavoro notturno nostro), per MinIO (regola di scadenza del bucket) e per Teams (criterio di scadenza).

**AI Act.**
- È vietato usare sistemi AI per dedurre le emozioni delle persone sul posto di lavoro, dal 02/02/2025, salvo motivi medici o di sicurezza [verificato: art. 5(1)(f) del Regolamento (UE) 2024/1689, artificialintelligenceact.eu]. Quindi l'analisi delle call (C3, G3) non deve stimare emozioni o «umore» dei colleghi.
- Il bot che non parla non dialoga con le persone. Se in futuro parlerà o scriverà, dovrà dire di essere un'AI (art. 50) [verificato: 16 regola 1].
- La valutazione delle prestazioni dei venditori è ad alto rischio dal 02/12/2027 [verificato: 16 §3].

**Regno Unito.** Le regole specifiche sulla registrazione delle chiamate restano da verificare con il parere legale [non verificato: 16 domanda 8].

---

## 9. Come si collega al motore degli agenti

Il rapporto 26 consiglia di costruire il motore sull'Agent SDK di Claude in TypeScript e di non adottare Hermes [verificato: 26, «In breve»]. Il modulo riunioni non cambia con questa scelta: bot, trascrizione e archivio sono servizi a sé. Ecco l'aggancio [non verificato: proposta coerente con 26].

1. **Trascrizione pronta.** Il raccoglitore Teams, Vexa o il lotto scrivono la trascrizione in PostgreSQL e MinIO e segnano l'evento «trascrizione pronta».
2. **Lavoro in coda.** n8n vede l'evento e mette in coda un lavoro per il runner delle sessioni, come fa per orari e ingressi [verificato: 26, tabella dei pezzi, «Orari e ingressi»].
3. **Sessione «post-call» senza strumenti che inviano.** Legge la trascrizione come testo di terzi e restituisce un risultato a schema: recap, decisioni, prossimi passi, campi del CRM, bozza della mail [verificato: 26, output strutturato e difesa dalle iniezioni].
4. **Il Cancello.** La bozza della mail e gli aggiornamenti visibili al cliente diventano carte da approvare. Il recap interno va nel canale del cliente (B1-B4) [verificato: 26, «Approvazioni lunghe» e piano settimana 2].
5. **Memoria.** Il testo entra nella pipeline del board e diventa ricercabile da Claude Team tramite l'MCP RAG, con i permessi di chi chiede (K4) [verificato: board].

Due regole. L'endpoint MCP di Vexa non va dato agli agenti: solo l'agente agenda manda i bot, e solo per eventi avvisati. Le sessioni su trascrizioni sensibili non salvano la loro copia locale (`persistSession: false`) [verificato: 26 §3.7 e §11].

---

## 10. La raccomandazione

```
Calendario M365 --(Graph, n8n)--> Agente agenda: flag «avvisato», testo nell'invito
   |
   +-- riunione Teams nostra --> recordAutomatically + it-IT --> trascrizione Teams (OneDrive)
   |                                                                |  delta Graph ogni 5-10 min
   +-- riunione di altri --> Vexa (VM meet-01, VLAN MEET) --> audio su MinIO
   |      Teams, Meet, Zoom web     |  dal vivo: turbo int8 (GPU di giorno, CPU la sera)
   |                                +-- rifiutato? --> registrazione sul PC di chi partecipa
   +-- riunione dal vivo --> telefono --(NetBird)--> endpoint di caricamento --> MinIO
                                                              |
            Lotti: Parakeet v3 o WhisperX + pyannote <--------+
                              |
   Evento «trascrizione pronta» --> n8n --> sessione Agent SDK «post-call» senza strumenti
                              |                    |
   filtro segreti --> Qwen3-4B metadati --> Qdrant + BM25     carte al Cancello (mail, CRM)
                              |
                MCP RAG --> Claude Team (K4: «cosa si è detto?»)
```

**Le scelte.**
1. Trascrizione nativa di Teams per le riunioni nostre, scaricata con Graph in delta. Nessun bot, nessun costo.
2. Vexa stabile 0.12.x, versione fissata, per le riunioni degli altri. Compose in una VM dedicata; Lite solo per una prima prova. Non la 0.13 alpha.
3. Trascrizione in tre modi: GPU di giorno, CPU la sera, seconda GPU dalla F5.
4. Telefono con l'app di sistema e un Comando rapido o «Condividi», via NetBird. Scriberr da provare come alternativa già pronta.
5. Due passaggi: turbo dal vivo; Parakeet v3 (o WhisperX) più pyannote a lotti, dove la prova mostra un guadagno.
6. Riserva per i bot rifiutati: registrazione sul PC di chi partecipa, con lo stesso avviso (Meetily, poi caricamento dell'audio) [non verificato: esportazione dell'audio da Meetily da provare].
7. Attendee come piano B, solo se Vexa delude nella prova sul campo.
8. Seconda GPU da 16 GB (RTX 2000 Ada) nella fase F5, divisa con Andrea.

---

## 11. Giorni e risorse

### 11.1 Lavoro

Stime in giorni-persona [non verificato: stime di progetto].

| # | Lavoro | Chi | Giorni | Quando |
|---|---|---|---|---|
| 1 | Impostazioni Teams ed Entra: accesso Graph, nomi dei parlanti, link all'informativa, scadenza, chi ammette, criterio sui bot esterni, app e criterio di accesso applicativo | Michele | 1 | subito, senza server |
| 2 | Raccoglitore Teams: delta su `getAllTranscripts` per i 4 utenti, VTT su PostgreSQL e MinIO, legame con evento e cliente | Mattia | 2-3 | F2 (n8n in casa) |
| 3 | Agente agenda: flag «avvisato», testo nell'invito, `recordAutomatically` e `it-IT` sulle nostre riunioni, prenotazione del bot sulle altre | Mattia | 2 | F2-F4 |
| 4 | VM e VLAN meet: Docker, Vexa Compose, registrazioni su MinIO, regole OPNsense, controlli in Uptime Kuma | Michele | 2 | F4 |
| 5 | Servizio di trascrizione nell'LXC GPU, tre modi (GPU, CPU, passaggio serale) e script dei turni | Michele | 1-1,5 | F4 |
| 6 | Integrazione Vexa: invio del bot da n8n, stato, testo e audio nel nostro archivio, cancellazione a 30 giorni | Mattia | 3 | F4 |
| 7 | Pipeline a lotti: Parakeet v3 o WhisperX, pyannote, conferma dei nomi, ingresso nella pipeline del board (1-2 giorni se Scriberr passa la prova) | Mattia | 3-4 | F4 |
| 8 | Telefono: endpoint di caricamento, Comando rapido iOS, condivisione Android, guida di una pagina | Mattia, Michele | 2-3 | F4 |
| 9 | Aggancio al motore: evento «trascrizione pronta», lavoro in coda, schema del recap | Mattia | 1 | F4 |
| 10 | Prova di qualità: 10 call vere con consenso; errori sulle parole e sui parlanti per Teams nativo, turbo, large-v3, Parakeet, Canary; prova di C2 nelle nostre riunioni | Alberto, Mattia | 2-3 | F4, prima di accendere tutto |
| 11 | Prova sul campo dei bot: 15 riunioni (Teams di clienti, Meet, Zoom); ingressi riusciti, sala d'attesa, «Unverified» | Alberto, Alessandro | 1-2, diluiti | F4 |
| 12 | Informativa, testi d'avviso, DPIA; procedura art. 4 se servono | Alberto (più il legale) | 1-2 | prima del primo uso con un cliente |
| 13 | Esercizio: istruzioni operative, allarmi, aggiornamenti entro 14 giorni | Michele | 1, poi circa 0,5 al mese | dopo l'avvio |
| **Totale** | | | **22-29** | |

Per persona: Mattia circa 13,5-16,5; Michele circa 5,5-6,5 più l'esercizio; Alberto circa 2,5-4,5; Alessandro 0,5-1. Con Mattia a metà tempo su questo, sono circa 6-7 settimane di calendario dentro F2-F4 [non verificato: stima].

Il recap, il follow-up e il CRM dopo la call (B1-B4) sono lavoro del motore degli agenti e stanno nella stima del 26, non qui [verificato: 26, piano settimana 2].

In più, se servono: prova comparata con Attendee 2-3 giorni; montaggio della seconda GPU e passthrough 0,5-1 giorno.

### 11.2 Risorse sul server

| Risorsa | Dimensione | Dove | Etichetta |
|---|---|---|---|
| VM `meet-01` | 6-8 vCPU, 12 GB di RAM (3 bot da 2 GB più lo stack), 60-80 GB di disco | VLAN MEET | 1 CPU e 2 GB per bot [verificato: values.yaml]; il resto [non verificato: stima] |
| Servizio di trascrizione e lotti | 8 GB di RAM in più; 2-4,5 GB di memoria GPU nel modo A; 16 thread per i lotti nel modo B | VLAN AI | [non verificato: stima] |
| Modelli | circa 10 GB (turbo, large-v3, Parakeet, pyannote, allineamento) | rpool o tank | [non verificato: stima] |
| Audio | WAV 16 kHz mono circa 115 MB l'ora; con 100 ore al mese e 30 giorni di conservazione circa 12 GB | MinIO su tank | [non verificato: calcolo] |

RAM nuova in tutto circa 20 GB sui circa 53 GB liberi del board [verificato: board, tabella «Capacità»]. Con Andrea (6-8 GB nella fase 1 [verificato: 31 §8.2]) restano circa 25 GB liberi [non verificato: calcolo].

### 11.3 Costi

- Licenze software: 0 € (Apache-2.0, MIT, BSD-2, CC-BY-4.0; pyannote community-1 gratuito dopo l'accettazione delle condizioni) [verificato: pagine dei progetti].
- API Graph per le trascrizioni: 0 € [verificato: learn.microsoft.com, «Metered APIs and services»].
- M365: nessun costo in più se il piano attuale include Teams con la trascrizione [non verificato: piano di SerSan da confermare].
- Recall.ai non serve più: 17,42 €/mese in meno con 30 ore, 58,07 €/mese con 100 ore [verificato: 22 §6].
- Facoltativi: seconda GPU RTX 2000 Ada circa 650-920 € (rilevato il 25/10/2026) [verificato: secondaria, §6.3]; vivavoce da sala 100-250 € [non verificato].

---

## 12. Rischi e piano B

| Rischio | Effetto | Cosa facciamo |
|---|---|---|
| Le piattaforme chiudono ai bot (Teams «Unverified» e blocco, Zoom OBF e RTMS, coda «a rischio» su Meet) | il bot non entra nelle riunioni dei clienti | Teams nativo per le nostre; registrazione sul PC come riserva; chiedere al cliente di ammettere «SerSan Verbale» |
| Vexa è giovane e cambia ogni settimana | rotture dopo un aggiornamento | versione fissata; aggiornare dopo una prova; trascrizione, archivio e calendario restano nostri, quindi si cambia bot senza rifare il resto; piano B Attendee |
| GPU piena di giorno e assente la sera | niente trascrizione dal vivo | modi A e B (§6.2); seconda GPU in F5 |
| Seconda GPU contesa con Andrea | code sui lotti | priorità: Andrea, poi call dal vivo, poi lotti; RAG sulla CPU la sera |
| Qualità in italiano con accenti e voci sovrapposte | verbali sbagliati, nomi storpiati | prova del lavoro 10; elenco dei nomi di clienti e prodotti nel prompt iniziale di Whisper [non verificato: da provare]; vivavoce da sala dal vivo |
| C2 nelle nostre riunioni: la registrazione automatica non parte senza nessuno di SerSan | riunione persa | prova del lavoro 10; riserva con bot o con un collega collegato |
| Sicurezza della VM dei bot (browser con codice di terzi, socket di Docker) | via d'ingresso verso la rete interna | VLAN dedicata, nessuna rotta verso DATA, patch entro 14 giorni |
| Testo dei terzi come istruzioni | un agente agisce su una frase detta in call | corsia senza strumenti; ciò che esce passa dal Cancello [verificato: 22 §2; 26 §11] |
| Profili legali (UK, art. 4 dello Statuto, emozioni) | contestazioni | parere legale prima della fase 2; niente stima delle emozioni; avviso sempre |

---

## 13. Domande aperte

1. Quale piano M365 ha SerSan? Va controllato con lo strumento di diagnostica delle trascrizioni per i quattro utenti.
2. Quante call con i clienti organizziamo noi in Teams e quante le organizzano loro (Teams, Meet, Zoom)? Decide quanto lavoro fa il bot.
3. Qualcuno usa Zoom con i clienti? Se è raro, il caso Zoom si rimanda.
4. A che ora la GPU passa a Experimental-1? Ci sono call con clienti dopo quell'ora?
5. Quale seconda GPU intende Michele? Per l'audio e per Andrea serve una 16 GB (RTX 2000 Ada o RTX PRO 2000 Blackwell). Riser e slot del DL380 la accettano accanto alla RTX 4000?
6. Accendiamo il consenso esplicito di Teams nelle riunioni con i clienti, o basta l'avviso?
7. Nel nostro tenant, i notetaker dei clienti li lasciamo in sala d'attesa (di serie) o li blocchiamo?
8. Nome del bot e testo d'avviso in inglese per i clienti UK: li approva il parere legale insieme alle regole UK sulle registrazioni?
9. Dal vivo: chi registra, con quale telefono o microfono? Compriamo un vivavoce da sala?
10. Le quattro persone sono dipendenti, soci o amministratori? Da qui dipende se registrare le riunioni interne chiede la procedura dell'art. 4 dello Statuto.
11. Teniamo l'audio fino a 30 giorni dopo la trascrizione, come proposto nel 16, o lo cancelliamo subito?

---

## Fonti

Lette il 25/10/2026, salvo dove indicato.

**Progetto**
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt` (board di Michele)
- `ricerca/00-visione-funzionalita.md`, `13-modelli-open-source-sul-server.md`, `16-gdpr-ai-act-e-regole.md`, `22-architettura-scelta.md`, `25-board-michele-e-delta.md`, `26-claude-agent-sdk.md`, `31-voce-andrea-self-hosted.md`, `PRESENTAZIONE-CEO.md`

**Microsoft Teams e Graph**
- https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/meeting-transcripts/overview-transcripts
- https://learn.microsoft.com/en-us/graph/metered-api-list
- https://learn.microsoft.com/en-us/graph/api/calltranscript-get?view=graph-rest-1.0
- https://learn.microsoft.com/en-us/graph/api/onlinemeeting-getalltranscripts?view=graph-rest-1.0
- https://learn.microsoft.com/en-us/graph/api/resources/onlinemeeting?view=graph-rest-1.0
- https://learn.microsoft.com/en-us/graph/api/onlinemeeting-update?view=graph-rest-1.0
- https://learn.microsoft.com/en-us/graph/teams-changenotifications-callrecording-and-calltranscript
- https://learn.microsoft.com/en-us/microsoftteams/meeting-transcript-api-access
- https://learn.microsoft.com/en-us/microsoftteams/meeting-transcription-captions
- https://learn.microsoft.com/en-us/microsoftteams/recording-transcription-overview
- https://learn.microsoft.com/en-us/microsoftteams/participant-agreement-recording-transcription
- https://support.microsoft.com/office/i-can-t-transcribe-a-meeting-in-microsoft-teams-61f4c8e4-f2d1-4aeb-9b20-244c20fc3faa
- https://practical365.com/teams-automatic-transcription/ (licenze, MC260564)
- https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges (tramite ricerca)
- https://learn.microsoft.com/en-us/microsoftteams/platform/bots/calls-and-meetings/requirements-considerations-application-hosted-media-bots
- https://learn.microsoft.com/ja-jp/answers/questions/5669007/interview-recording-did-not-start-as-expected ; https://jiminny-inc.helpjuice.com/how-do-automatic-recordings-work-for-microsoft-teams-meetings

**Piattaforme e bot**
- https://mc.merill.net/message/MC1251206
- https://office365itpros.com/2026/08/24/teams-meeting-notetaking-bots/
- https://www.uctoday.com/unified-communications/microsoft-teams-to-block-external-bots-automatically-as-ai-notetaker-crackdown-hardens/
- https://www.uctoday.com/security-compliance-risk/google-meet-launches-update-to-better-screen-suspicious-bots/
- https://announce.miitel.com/en/google-meet-s-new-feature-may-cause-meeting-bots-to-appear-in-the-potential-risk-queue-4ztvjy
- https://knowledge.workspace.google.com/admin/meet/prepare-your-network-for-meet-meetings-and-live-streams
- https://developers.zoom.us/docs/meeting-sdk/obf-faq/ ; https://devforum.zoom.us/t/anonymous-join-exception/144677

**Bot di riunione**
- Vexa: https://github.com/Vexa-ai/vexa (README, API GitHub, releases) ; https://raw.githubusercontent.com/Vexa-ai/vexa/main/docs/docs/api/meetings.mdx ; https://raw.githubusercontent.com/Vexa-ai/vexa/main/docs/docs/deployment.mdx ; https://raw.githubusercontent.com/Vexa-ai/vexa/main/deploy/transcription/.env.example ; https://raw.githubusercontent.com/Vexa-ai/vexa/main/deploy/helm/charts/vexa/values.yaml ; https://docs.vexa.ai/deployment-lite.md
- Attendee: https://github.com/attendee-labs/attendee (README, LICENSE, API GitHub) ; https://docs.attendee.dev/guides/transcription/index.md ; https://docs.attendee.dev/guides/signedinbots/index.md
- joinly: https://github.com/joinly-ai/joinly ; meeting-bot: https://github.com/screenappai/meeting-bot ; meetingbot: https://github.com/meetingbot/meetingbot ; Meetily: https://github.com/Zackriya-Solutions/meetily

**Trascrizione e parlanti**
- https://github.com/SYSTRAN/faster-whisper ; https://github.com/m-bain/whisperX ; https://github.com/istupakov/onnx-asr
- https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 ; https://huggingface.co/nvidia/canary-1b-v2 ; https://docs.nvidia.com/nemo/speech/latest/asr/featured_models.html
- https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602
- https://huggingface.co/pyannote/speaker-diarization-community-1 ; https://github.com/pyannote/pyannote-audio
- https://github.com/rishikanthc/Scriberr
- https://docs.nvidia.com/cuda/archive/13.3.0/cuda-features-archive/index.html

**GPU e prezzi**
- https://www.mediamarkt.be/en/product/_pny-vcnrtx2000ada-sb-graphics-card-156848692.html ; https://pood.datafox.ee/en/videokaardid/pny-rtx2000-ada-nvidia-rtx-2000-ada-16-gb-gddr6 ; https://www.ox.ee/rus/product/2952401
- https://gpuprix.com/it/gpus/rtx-pro-2000-blackwell ; https://www.mediaworld.it/it/product/_nvidia-rtx-pro-2000-blackwell-16-gb-gddr7-scheda-grafica-16-gb-166218270.html
- https://gpuprix.com/eu/gpus/rtx-4000-sff-ada-generation ; https://www.hardwaredealz.com/hardware/gpu/nvidia-20gb-gddr6-4x-mdp/preisvergleich.25062

**Telefono, rete, regole**
- https://docs.netbird.io/get-started/install/mobile
- https://developer.apple.com/forums/thread/797987
- https://artificialintelligenceact.eu/article/5/
- https://www.filodiritto.com/ai-la-trascrizione-delle-videocall-rischi-legali-e-come-adottarla-correttamente ; https://www.tomshw.it/business/consenso-prima-delle-trascrizioni-ai-le-pmi-devono-fissare-una-regola-aziendale
