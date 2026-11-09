# ADR-0007: Call: trascrizione di Teams per le nostre, Vexa e trascrizione in casa per le altre

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata

**Chi decide**: Alberto e Michele, che guidano la costruzione ([proposta §10](../../PRESENTAZIONE-CEO.md)); Michele deve ancora ammettere Vexa e la sua rete separata, la VLAN 35 MEET ([domande per Michele, n. 9](../../DOMANDE-PER-MICHELE.md))

## Contesto

- La visione chiede un agente che entri in ogni call, anche al posto di chi manca, e trascriva tutto dichiarandolo (voci J5, A1 e C2) ([proposta, appendice A](../../PRESENTAZIONE-CEO.md)).
- Il board di Michele, il disegno dell'infrastruttura, non ammette Recall.ai, il servizio USA della prima versione ([ricerca/25 §2, C06](../../ricerca/25-board-michele-e-delta.md)); audio e trascrizioni integrali sono dati rossi ([proposta §5.6](../../PRESENTAZIONE-CEO.md), [ADR-0009](0009-dati-tre-colori.md)).
- Nel 2026 Teams, Meet e Zoom hanno chiuso le porte ai bot non riconosciuti ([ricerca/30 §4.4](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- La GPU di oggi, una RTX 4000 da 8 GB, è quasi piena ([proposta §6.4](../../PRESENTAZIONE-CEO.md)).

## Decisione

1. **Call Teams organizzate da noi: nessun bot.** Teams trascrive già, con il nome di chi parla e l'avviso di registrazione. Il testo lo scarichiamo con Graph, l'API di Microsoft 365, ogni 5-10 minuti, gratis e senza aprire porte. Dalla fase 1 ([ricerca/30 §2 e §3](../../ricerca/30-call-e-trascrizione-self-hosted.md), [proposta, appendice A, J5](../../PRESENTAZIONE-CEO.md)).
2. **Call dei clienti (Teams di altri, Meet, Zoom): Vexa**, un bot open source che entra come un partecipante. Gira in una macchina sua nella VLAN 35 MEET, con la versione 0.12.x fissata. Dalla fase 3 ([proposta §5.2 e §11](../../PRESENTAZIONE-CEO.md), [ricerca/30 §4.5 e §10](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
3. **Riunioni dal vivo**: registrazione sul telefono, mandata al server attraverso NetBird, la rete privata del board ([ricerca/30 §7](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
4. **Trascrizione in casa con modelli aperti**: faster-whisper durante la call; dopo, a lotti, Parakeet v3 (o WhisperX) con pyannote, che separa chi parla ([ricerca/30 §5](../../ricerca/30-call-e-trascrizione-self-hosted.md)).

Sempre: avviso nell'invito, nella riunione e a voce; il bot lo manda solo l'Agente agenda, negli eventi segnati «avvisato»; audio fino a 30 giorni, trascrizioni 24 mesi dall'ultimo contatto ([proposta §9.1](../../PRESENTAZIONE-CEO.md), [ricerca/30 §8 e §9](../../ricerca/30-call-e-trascrizione-self-hosted.md)). Se il cliente non ammette il bot, si registra sul PC di chi partecipa ([proposta §13](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: Recall.ai, come nella prima versione

- **Pro**: è maturo, copre tutte le piattaforme e include la trascrizione ([ricerca/30 §4.1](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- **Contro**: è un servizio negli USA fuori dal board; costava circa 17 € al mese con 30 ore di call ([ricerca/30 §11.3](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- **Perché no**: l'audio è rosso e deve restare in casa ([proposta §5.6](../../PRESENTAZIONE-CEO.md)).

### Alternativa: Attendee al posto di Vexa

- **Pro**: scrive in chat e parla, quindi può presentarsi da solo ([ricerca/30 §4.3](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- **Contro**: su Zoom entra solo con il token di un utente già in riunione; in produzione chiede Kubernetes, un sistema complesso per gestire molti container; il suo bot Teams con login vuole l'autenticazione a due fattori spenta ([ricerca/30 §4.3](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- **Perché no**: resta il piano B, se Vexa delude sul campo ([ricerca/30 §10](../../ricerca/30-call-e-trascrizione-self-hosted.md)).

## Conseguenze

### Positive

- L'audio resta in casa; licenze e API delle trascrizioni costano 0 € ([proposta §5.6](../../PRESENTAZIONE-CEO.md), [ricerca/30 §11.3](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- La parte Teams serve già al pilota della fase 1 ([proposta §4.2](../../PRESENTAZIONE-CEO.md)).
- Bot, trascrizione e archivio sono servizi a sé: si può cambiare bot senza rifare il resto ([ricerca/30 §12](../../ricerca/30-call-e-trascrizione-self-hosted.md)).

### Negative

- Il bot entra solo se il cliente lo ammette, e Vexa 0.12 non scrive in chat: l'avviso passa dal suo nome, dall'invito e da chi conduce ([proposta, appendice A, J5](../../PRESENTAZIONE-CEO.md), [ricerca/30 §4.2](../../ricerca/30-call-e-trascrizione-self-hosted.md)).
- Due servizi in più da aggiornare entro 14 giorni; Vexa chiede circa 12 GB di RAM per tre bot ([ricerca/36 §4.1 e §4.5](../../ricerca/36-architettura-v2.md)), dentro la RAM in più della fase 3 ([ADR-0015](0015-ram-384-gb.md)).

### Rischi

- Le piattaforme bloccano i bot non registrati: la riserva è la registrazione sul PC ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- La GPU resta una sola fino alla seconda ([ADR-0014](0014-seconda-gpu-blackwell.md)), che conviene dalla fase 3 e serve al più tardi all'inizio della fase 5; quando la prende il laboratorio, i lavori aspettano in coda ([proposta §6.4](../../PRESENTAZIONE-CEO.md)). Sulla nuova scheda la trascrizione va provata prima ([domande per Michele, n. 18](../../DOMANDE-PER-MICHELE.md)).
- Nelle nostre call senza nessuno di SerSan collegato la registrazione automatica potrebbe non partire: va provato ([proposta, appendice A, C2](../../PRESENTAZIONE-CEO.md)).
- Registrare tocca GDPR, Statuto dei lavoratori e regole UK: servono parere legale e valutazione d'impatto ([proposta §9.4](../../PRESENTAZIONE-CEO.md), [ricerca/30 §8](../../ricerca/30-call-e-trascrizione-self-hosted.md)).

## Fonti

- [Proposta 2.1: §4.2, §5.2, §5.6, §6.4, §9.1, §9.4, §10, §11, §13, appendice A (J5, A1, C2)](../../PRESENTAZIONE-CEO.md)
- [ricerca/30: l'agente che entra in ogni call, senza Recall.ai](../../ricerca/30-call-e-trascrizione-self-hosted.md)
- [ricerca/25 §2 (C06): Recall.ai fuori dal board](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/36 §4.1 e §4.5: componenti, RAM e patch](../../ricerca/36-architettura-v2.md)
- [Domande per Michele, n. 9 e 18](../../DOMANDE-PER-MICHELE.md)
