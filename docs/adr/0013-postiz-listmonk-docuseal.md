# ADR-0013: Postiz, listmonk e DocuSeal in casa per post, newsletter e firme

**Data**: proposta il 2026-10-25 (registrata il 2026-11-09); accettata il 2026-11-10

**Stato**: accettata il 2026-11-10 dal gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026; Michele ammette i servizi nuovi

**Chi decide**: i due CEO, Alessandro e Michele, con le decisioni 9, 15, 21 e 22 ([proposta §14](../../PRESENTAZIONE-CEO.md)); Michele deve ammettere i servizi nuovi e il servizio esterno di invio della newsletter ([domande per Michele, n. 9 e 10](../../DOMANDE-PER-MICHELE.md))

## Contesto

- Gli agenti devono programmare i post, mandare la newsletter, mettere in firma i contratti e preparare le fatture (voci J7, K9, L1 e L2) ([proposta, appendice A](../../PRESENTAZIONE-CEO.md)).
- Oggi i post passano da Metricool, in cloud, 59,86 € al mese, che pubblica su Pagina LinkedIn, Instagram e Facebook ([ricerca/33 §2.5](../../ricerca/33-costi-v2.md)).
- Il board di Michele, il disegno dell'infrastruttura, tiene in cloud solo i suoi servizi: Metricool, newsletter, firma elettronica e fatturazione non ci sono ([ricerca/25 §7, N08](../../ricerca/25-board-michele-e-delta.md), [ADR-0002](0002-self-hosted-board-michele.md)).
- Le regole di casa: niente esce senza un sì scritto, e sulle piattaforme si scrive solo da una sessione presidiata ([proposta §8.2](../../PRESENTAZIONE-CEO.md)).

## Decisione

- **Post: Postiz**, open source (AGPL-3.0), sul nostro server dalla fase 4. Il Pubblicatore prepara la lista da approvare; dopo il sì Alberto programma i post su Postiz in una sessione presidiata, e l'agente controlla che escano. Fino ad allora resta Metricool (decisione 15) ([proposta §4.4 e §14](../../PRESENTAZIONE-CEO.md), [ricerca/36 §4.1](../../ricerca/36-architettura-v2.md)).
- **Newsletter: listmonk**, open source (AGPL-3.0), con API e database su PostgreSQL, dalla fase 4. L'invio passa da un servizio di posta esterno (relay SMTP, per esempio Amazon SES), per meno di 1 € al mese (decisione 9). L'Agente newsletter la manda dopo il sì e registra chi la apre ([proposta §4.4 e §14](../../PRESENTAZIONE-CEO.md), [ricerca/36 §4.1](../../ricerca/36-architettura-v2.md)).
- **Firme: DocuSeal**, open source (AGPL-3.0 con termini aggiuntivi), dalla fase 6. L'Agente contratti prepara il contratto dall'offerta approvata e, dopo il sì, lo manda in firma; una firma qualificata da un fornitore esterno solo se il parere legale la chiede (decisione 21) ([proposta §4.3, §11 e §14](../../PRESENTAZIONE-CEO.md), [ricerca/36 §9.3](../../ricerca/36-architettura-v2.md)).
- **Fatture**, nella fase 6: lo strumento che usiamo già, se fa al caso, altrimenti uno sul nostro server (decisione 22); le ipotesi sono Sirius, che ha già i dati fiscali e dei clienti, oppure Invoice Ninja sul nostro server ([proposta §14 e appendice A, L2](../../PRESENTAZIONE-CEO.md)).
- **Esposizione**: Postiz e listmonk mai raggiungibili da internet, solo dalla rete privata NetBird; di DocuSeal sono pubbliche solo le pagine di firma ([ricerca/36 §4.5](../../ricerca/36-architettura-v2.md)).
- Contratti e fatture passano da una carta del Cancello, il nostro esecutore unico delle azioni esterne, con la chiave di sicurezza FIDO2 ([proposta §4.11 e §5.4](../../PRESENTAZIONE-CEO.md), [ADR-0003](0003-cancello-approvazioni.md)).

## Alternative considerate

### Alternativa: restare su Metricool

- **Pro**: è già in uso e pubblica su Pagina LinkedIn, Instagram e Facebook ([ricerca/33 §2.5](../../ricerca/33-costi-v2.md)).
- **Contro**: 59,86 € al mese per un servizio in cloud fuori dal board ([ricerca/33 §2.5](../../ricerca/33-costi-v2.md)).
- **Perché no**: resta solo come ponte fino a Postiz; con il consiglio della decisione 15 gli strumenti fuori dal board scendono da circa 146 a circa 86 € al mese dopo la fase 4 ([proposta §14](../../PRESENTAZIONE-CEO.md)).

### Alternativa: mandare la newsletter da Exchange Online

- **Pro**: la posta di M365 l'abbiamo già ([proposta §1](../../PRESENTAZIONE-CEO.md)).
- **Contro**: Exchange Online non è fatto per l'invio in massa (avviso Microsoft MC787382) ([ricerca/34, proposta 1 §3.1](../../ricerca/34-proposta-1-agent-sdk.md)).
- **Perché no**: un servizio di invio esterno costa meno di 1 € al mese ([proposta §14](../../PRESENTAZIONE-CEO.md)).

### Alternativa: la firma da un fornitore esterno in cloud

- **Pro**: è l'uscita se DocuSeal non regge, e la strada per la firma qualificata se serve ([ricerca/36 §12](../../ricerca/36-architettura-v2.md), [proposta §14](../../PRESENTAZIONE-CEO.md)).
- **Contro**: un servizio in cloud in più, con un costo a preventivo ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)).
- **Perché no**: in casa la licenza costa 0 € ([ricerca/36 §9.3](../../ricerca/36-architettura-v2.md)) e i contratti, documenti dei clienti e quindi dati rossi, restano sul server ([proposta §5.6](../../PRESENTAZIONE-CEO.md)).

## Conseguenze

### Positive

- Metricool esce con la fase 4, e in casa le licenze costano 0 € ([proposta §14](../../PRESENTAZIONE-CEO.md), [ricerca/36 §9.3](../../ricerca/36-architettura-v2.md)).
- Chi apre la newsletter arriva nel brief prima delle call ([proposta §4.4](../../PRESENTAZIONE-CEO.md)).

### Negative

- Tre o quattro servizi in più da installare e aggiornare entro 14 giorni, ognuno con un responsabile delle patch ([proposta §6.2](../../PRESENTAZIONE-CEO.md), [ricerca/36 §4.5](../../ricerca/36-architettura-v2.md)), e circa 5 GB di RAM in più a regime ([ricerca/36 §4.2](../../ricerca/36-architettura-v2.md)).
- Nella versione gratuita di DocuSeal mancano promemoria automatici, ruoli e accesso unico (SSO): sono nella versione Pro a pagamento ([ricerca/34, proposta 3 §8](../../ricerca/34-proposta-3-claude-team-e-mcp.md)).

### Rischi

- Postiz e listmonk hanno avuto vulnerabilità nel 2026, secondo fonti non verificate: per questo non sono mai pubblici ([ricerca/36 §4.5](../../ricerca/36-architettura-v2.md)).
- L'accesso via API alla pagina LinkedIn è da verificare; se manca, Metricool resta come eccezione ([proposta, appendice A, L8](../../PRESENTAZIONE-CEO.md)).
- Restano aperti il valore legale della firma fatta in casa, chi fattura (la Ltd inglese, oppure un soggetto italiano con lo SDI, il sistema delle fatture elettroniche), cos'è Sirius e la licenza di Invoice Ninja ([proposta §9.4 e appendice A, L2](../../PRESENTAZIONE-CEO.md), [domande per Michele, n. 25 e 29](../../DOMANDE-PER-MICHELE.md), [ricerca/36 §9.3](../../ricerca/36-architettura-v2.md)).

## Revisione del 10 novembre 2026

- Le decisioni 9, 15, 21 e 22 non aspettano più i CEO: il progetto è approvato e le prende il gruppo di progetto con Michele ([ricerca/45](../../ricerca/45-architettura-v3.md), «Decisione del gruppo di progetto»).
- **Postiz** entra prima della fase F4 del board solo con il sì di Michele; fino ad allora i post della pagina aziendale li programma l'**esecutore Metricool** del Cancello ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md); [ADR-0024](0024-abbonamenti-come-riserva.md)).
- I post della pagina aziendale partono a L1 e passano a L2; quelli dei founder restano a L1 ([ricerca/45 §4.1](../../ricerca/45-architettura-v3.md); [ADR-0020](0020-autonomia-a-livelli.md)).
- La **newsletter** va a L2 dalla fase 4, dopo 3 numeri puliti, con un invio di prova alla persona e una finestra di 48 ore ([ricerca/45 §2.6 e §4.1](../../ricerca/45-architettura-v3.md)).
- Contratti e fatture restano a L1 nella classe «Impegni», ma senza la chiave FIDO2 sulla carta ([ADR-0020](0020-autonomia-a-livelli.md); [ADR-0023](0023-protezioni-essenziali.md)).

## Fonti

- [Proposta 2.1: §1, §4.3, §4.4, §4.11, §5.4, §5.6, §6.2, §8.2, §9.4, §11, §14, appendice A (J7, K9, L1, L2, L8)](../../PRESENTAZIONE-CEO.md)
- [ricerca/36: architettura v2, §4.1, §4.2, §4.5, §9.3, §12](../../ricerca/36-architettura-v2.md)
- [ricerca/33 §2.5: strumenti commerciali e di marketing](../../ricerca/33-costi-v2.md)
- [ricerca/25 §7 (N08): strumenti fuori dal board](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/34: proposta 1 §3.1](../../ricerca/34-proposta-1-agent-sdk.md) e [proposta 3 §8](../../ricerca/34-proposta-3-claude-team-e-mcp.md)
- [Domande per Michele, n. 9, 10, 25 e 29](../../DOMANDE-PER-MICHELE.md)
