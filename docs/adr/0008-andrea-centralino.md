# ADR-0008: "Andrea": centralino Asterisk e Pipecat con linea italiana, solo richiamate richieste

**Data**: da decidere con la decisione 10; proposta il 2026-10-25 (registrata il 2026-11-09)

**Stato**: proposta

**Chi decide**: i due CEO, Alessandro e Michele, con la decisione 10 ([proposta §14](../../PRESENTAZIONE-CEO.md)); Michele deve anche ammettere la rete separata VLAN 25 VOCE e l'operatore telefonico come servizio esterno ([domande per Michele, n. 9 e 10](../../DOMANDE-PER-MICHELE.md))

## Contesto

- La visione chiede "Andrea", un agente vocale che richiama entro 90 secondi, 24 ore su 24, chi lo chiede, risponde quando nessuno può, fissa l'appuntamento con uno di noi e impara dai rifiuti (voci G5, G6 e K10) ([proposta §4.3 e appendice A](../../PRESENTAZIONE-CEO.md)).
- La prima versione usava ElevenLabs e un numero Twilio, che non sono nel board di Michele ([ricerca/31 §0](../../ricerca/31-voce-andrea-self-hosted.md)).
- Un operatore telefonico serve comunque, e conviene italiano: gli operatori italiani bloccano le chiamate dall'estero che mostrano un numero italiano ([ricerca/31 §4.1](../../ricerca/31-voce-andrea-self-hosted.md)).
- Dal 2 agosto 2026 chi parla da solo con un esterno deve dire di essere un'AI; in Italia le chiamate automatizzate chiedono un consenso preventivo ([ricerca/16 §2](../../ricerca/16-gdpr-ai-act-e-regole.md)). Il piano marketing vieta le voci sintetiche nelle call: serve un'eccezione ([proposta §13](../../PRESENTAZIONE-CEO.md)).

## Decisione

- **Centralino**: Asterisk 22 LTS, la versione con supporto lungo, in una macchina sua nella VLAN 25 VOCE, con una linea italiana via internet (trunk SIP); l'operatore proposto è Messagenet ([proposta §5.2](../../PRESENTAZIONE-CEO.md), [ricerca/31 §1.1, §3 e §4.2](../../ricerca/31-voce-andrea-self-hosted.md)).
- **Conversazione**: Pipecat, una libreria open source per agenti vocali, con ascolto e voce in casa su modelli aperti, prima sulla CPU e poi sulla seconda GPU. Ragiona Claude Haiku attraverso LiteLLM, il servizio che tiene chiavi e budget ([ADR-0004](0004-litellm-banca-token.md)), con il ragionamento esteso spento: acceso, il primo token arriva dopo almeno 6,58 secondi. Verso Anthropic va solo il testo ([proposta §11 e appendice A, G5](../../PRESENTAZIONE-CEO.md), [ricerca/31, in breve](../../ricerca/31-voce-andrea-self-hosted.md)).
- **Solo chi lo chiede**: Andrea chiama solo chi nel modulo ha chiesto la richiamata di un assistente AI. Il Cancello, il nostro esecutore unico delle azioni esterne ([ADR-0003](0003-cancello-approvazioni.md)), salva il consenso e controlla orari, tetti, la lista di soppressione (l'elenco unico di chi ci ha detto no) e il Registro delle opposizioni (l'elenco pubblico di chi rifiuta le chiamate commerciali); senza consenso rifiuta. Queste telefonate partono senza carta, come eccezione da approvare con la decisione 10 ([proposta §5.1 e §9.1](../../PRESENTAZIONE-CEO.md), [ricerca/31 §9](../../ricerca/31-voce-andrea-self-hosted.md)).
- **Regole fisse**: la prima frase dice che è un'AI; Andrea fissa l'appuntamento e non vende; in entrata risponde quando nessuno di noi può, e l'esito va nel CRM e nel canale vendite ([proposta §4.3, §9.1, §9.3 e appendice A, K10](../../PRESENTAZIONE-CEO.md)).
- **Quando**: fase 5 (settimane 41-48), solo con il parere legale e lead vere; 44-90 € al mese più 7-14 € di attivazione. La voce clonata di un collega solo con un suo contratto separato e revocabile ([proposta §11 e §14](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: ElevenLabs e un numero Twilio, come nella prima versione

- **Pro**: voce pronta e curata, latenza già misurata, nessun lavoro di integrazione telefonica ([ricerca/31 §0](../../ricerca/31-voce-andrea-self-hosted.md)).
- **Contro**: circa 170 € al mese; ElevenLabs conserva i dati negli USA di serie ([ricerca/33 §2.3](../../ricerca/33-costi-v2.md), [ricerca/16 §5](../../ricerca/16-gdpr-ai-act-e-regole.md)).
- **Perché no**: la voce dei lead deve restare in casa; una voce in cloud resta l'ultima riserva, come eccezione ([proposta §5.6 e §13](../../PRESENTAZIONE-CEO.md)).

### Alternativa: LiveKit al posto di Pipecat e Asterisk

- **Pro**: licenza Apache-2.0 e telefonia SIP nativa ([ricerca/31 §2](../../ricerca/31-voce-andrea-self-hosted.md)).
- **Contro**: più pezzi da gestire e un IP pubblico con le porte SIP e audio aperte ([ricerca/31 §1.2 e §2](../../ricerca/31-voce-andrea-self-hosted.md)).
- **Perché no**: il board non apre porte; Pipecat è un solo processo, con la fine del turno in italiano e la voce locale già integrate ([ricerca/31 §2](../../ricerca/31-voce-andrea-self-hosted.md)).

## Conseguenze

### Positive

- L'audio dei lead resta in azienda, e Andrea costa 44-90 € al mese invece di circa 170 € ([proposta §12.1](../../PRESENTAZIONE-CEO.md), [ricerca/33 §2.3](../../ricerca/33-costi-v2.md)).

### Negative

- Una rete e due servizi in più da aggiornare entro 14 giorni ([ricerca/36 §4.5](../../ricerca/36-architettura-v2.md)).
- Più lento di una piattaforma in cloud: circa 1,3-2,0 secondi prima della risposta con la GPU, 1,6-2,5 sulla sola CPU, stima da misurare ([ricerca/31 §7.2](../../ricerca/31-voce-andrea-self-hosted.md)).
- Il pezzo che collega Pipecat ad Asterisk è della comunità e Pipecat non lo prova: va fissato o riscritto ([ricerca/31 §2 e §13](../../ricerca/31-voce-andrea-self-hosted.md)).

### Rischi

- Voce italiana non abbastanza buona: prova d'ascolto prima, voci migliori sulla seconda GPU ([proposta §13](../../PRESENTAZIONE-CEO.md), [ADR-0014](0014-seconda-gpu-blackwell.md)).
- Una sola linea internet: se cade la fibra Andrea non risponde; linea di riserva prima della fase 5 (decisione 13) ([proposta §13](../../PRESENTAZIONE-CEO.md), [ADR-0019](0019-linea-di-riserva.md)).
- L'offerta "illimitata" dell'operatore potrebbe non valere per un agente: allora si paga a consumo, verso i 90 € al mese ([ricerca/33 §2.3](../../ricerca/33-costi-v2.md)).
- Consenso nel modulo, Registro delle opposizioni e marcatura dell'audio sintetico vanno chiusi con il parere legale ([proposta §9.4](../../PRESENTAZIONE-CEO.md), [ricerca/31 §9](../../ricerca/31-voce-andrea-self-hosted.md)).

## Fonti

- [Proposta 2.1: §4.3, §5.1, §5.2, §5.6, §9.1, §9.3, §9.4, §11, §12.1, §13, §14, appendice A (G5, G6, K10)](../../PRESENTAZIONE-CEO.md)
- [ricerca/31: "Andrea" tutto in casa](../../ricerca/31-voce-andrea-self-hosted.md)
- [ricerca/16 §2 e §5: AI Act, consenso, dove stanno i dati](../../ricerca/16-gdpr-ai-act-e-regole.md)
- [ricerca/33 §2.3: costi di numero e chiamate](../../ricerca/33-costi-v2.md)
- [ricerca/36 §4.5: servizi nuovi e patch](../../ricerca/36-architettura-v2.md)
- [Domande per Michele, n. 9 e 10](../../DOMANDE-PER-MICHELE.md)
