# ADR-0010: TypeScript come linguaggio del motore

**Data**: da decidere con la domanda 28; proposta il 2026-10-25 (registrata il 2026-11-09)

**Stato**: proposta

**Chi decide**: tutti e quattro, con la risposta di Mattia, che lavora sul codice dal primo giorno ([domande, n. 28, per tutti e quattro](../../DOMANDE-PER-MICHELE.md), [proposta §13](../../PRESENTAZIONE-CEO.md))

## Contesto

- Il motore degli agenti lo costruiamo noi con l'Agent SDK di Claude, cioè Claude Code usato come libreria: ogni lavoro gira in un processo suo ([proposta §5.1](../../PRESENTAZIONE-CEO.md), [ADR-0001](0001-motore-agent-sdk.md)).
- L'SDK esiste in TypeScript e in Python; al 25/10/2026 erano alle versioni 0.3.310 e 0.2.174, ognuna con dentro il suo Claude Code ([ricerca/26 §1.1](../../ricerca/26-claude-agent-sdk.md)).
- Esce quasi ogni giorno: va fissato e aggiornato ogni due settimane, dopo dieci scenari di prova, entro i 14 giorni chiesti da Cyber Essentials, la certificazione di sicurezza britannica ([proposta §5.3 e §13](../../PRESENTAZIONE-CEO.md), [ricerca/26 §11](../../ricerca/26-claude-agent-sdk.md)).
- Il motore deve chiedere al Cancello prima di ogni azione e tenere separato un agente dall'altro ([proposta §5.3](../../PRESENTAZIONE-CEO.md), [ricerca/26 §3.4](../../ricerca/26-claude-agent-sdk.md)).

## Decisione

- Il motore è un servizio TypeScript su Node.js 18 o più, l'ambiente che fa girare il codice sul server: il runner, che avvia un processo per ogni lavoro, il registro dei profili, il ponte verso il Cancello e la bacheca fra agenti ([ricerca/26 §1.1 e §10.2](../../ricerca/26-claude-agent-sdk.md), [ricerca/36, in breve](../../ricerca/36-architettura-v2.md)).
- Perché TypeScript ([ricerca/26 §1.3, §3.4 e §7.2](../../ricerca/26-claude-agent-sdk.md)):
  - ha più hook, cioè le funzioni nostre che l'SDK chiama in punti fissi: in Python mancano, fra gli altri, `SessionStart`, `SessionEnd`, `StopFailure`, `PostCompact`, `PreModelSwitch`, `TaskCreated` e `TaskCompleted`;
  - preavvia i processi con `startup()` e `prewarm()`, così il primo messaggio non aspetta l'avvio a freddo;
  - l'opzione `env` sostituisce l'ambiente del processo: un agente vede solo le variabili che gli passiamo, mai le chiavi del motore;
  - l'adattatore `claude-agent-acp`, che porta gli agenti in Buzz (la chat di Block per persone e agenti, in prova), è costruito sull'SDK TypeScript.
- Anche la Porta chat, il servizio che porta gli agenti in Teams e negli altri canali, usa il Chat SDK, che dà Teams, Telegram e WhatsApp con un solo codice TypeScript ([ricerca/28 §2.2](../../ricerca/28-chat-di-gruppo-self-hosted.md), [ricerca/36 §4.1](../../ricerca/36-architettura-v2.md), [ADR-0006](0006-teams-chat-di-gruppo.md)).

## Alternative considerate

### Alternativa: l'SDK in Python

- **Pro**: con `ClaudeSDKClient` tiene aperta una conversazione ([ricerca/26 §1.3](../../ricerca/26-claude-agent-sdk.md)).
- **Contro**: meno hook, nessun preavvio dei processi, e `env` si aggiunge all'ambiente invece di sostituirlo ([ricerca/26 §1.3 e §3.4](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: hook e isolamento sono proprio ciò che serve al ponte verso il Cancello ([ricerca/36 §5.1](../../ricerca/36-architettura-v2.md)).

### Alternativa: Claude Code da riga di comando (`claude -p`), lanciato da n8n, senza un servizio nostro

- **Pro**: è lo stesso ciclo dell'SDK, utile per lavori singoli lanciati da n8n o dai runner di GitHub ([ricerca/26 §6](../../ricerca/26-claude-agent-sdk.md)).
- **Contro**: con decine di agenti, chat, approvazioni e sessioni riprese servono gli hook nel processo e il salvataggio delle sessioni, comodi solo con l'SDK; senza l'opzione `--bare` esegue gli hook e collega i server MCP (i servizi che danno strumenti agli agenti) trovati nella cartella, anche se nessuno l'ha mai dichiarata fidata ([ricerca/26 §6](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: resta per i lavori singoli e per le prove ([ricerca/26 §6](../../ricerca/26-claude-agent-sdk.md)).

## Conseguenze

### Positive

- Un solo linguaggio e un solo fornitore per il motore. La proposta con Hermes aveva due linguaggi, sei istanze e un gateway con 276 problemi aperti: per una squadra di quattro era il carico più pesante ([ricerca/35, giudizio CPTO §4.4](../../ricerca/35-giudizio-cpto.md)).
- Da aggiornare entro 14 giorni ci sono un pacchetto npm (il registro dei pacchetti JavaScript) e il nostro codice ([ricerca/36 §2.3](../../ricerca/36-architettura-v2.md)).

### Negative

- Mattia deve lavorare in TypeScript: è la domanda ancora aperta ([domande, n. 28](../../DOMANDE-PER-MICHELE.md)).
- "Andrea" usa Pipecat, un processo Python: nel sistema i linguaggi restano due, ma Andrea sta fuori dal motore e chiama l'API da solo ([ricerca/31 §2](../../ricerca/31-voce-andrea-self-hosted.md)).

### Rischi

- L'SDK TypeScript è ancora 0.3.x, con 333 versioni dal 27/9/2025, e cambia comportamenti: dalla versione 2.1.302 di Claude Code un'app senza modalità esplicita nega ogni strumento che non sia approvato da una regola o da una funzione nostra (hook o callback) ([ricerca/26 §1.1](../../ricerca/26-claude-agent-sdk.md)).
- Codice nostro conosciuto da poche persone: Mattia secondo manutentore dal primo giorno, una guida operativa e revisioni incrociate ([ricerca/26 §11](../../ricerca/26-claude-agent-sdk.md)).

## Fonti

- [Proposta 2.1: §5.1, §5.3, §13](../../PRESENTAZIONE-CEO.md)
- [ricerca/26: Claude Agent SDK, §1.1, §1.3, §3.4, §6, §7.2, §10.2, §11](../../ricerca/26-claude-agent-sdk.md)
- [ricerca/36: architettura v2, in breve, §2.3, §4.1, §5.1](../../ricerca/36-architettura-v2.md)
- [ricerca/28 §2.2: il Chat SDK per la Porta chat](../../ricerca/28-chat-di-gruppo-self-hosted.md)
- [ricerca/35: giudizio del CPTO §4.4](../../ricerca/35-giudizio-cpto.md)
- [ricerca/31 §2: Pipecat per "Andrea"](../../ricerca/31-voce-andrea-self-hosted.md)
- [Domande per Michele, n. 28](../../DOMANDE-PER-MICHELE.md)
