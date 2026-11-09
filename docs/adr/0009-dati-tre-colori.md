# ADR-0009: Dati a tre colori e oscuramento locale prima del cloud

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata

**Chi decide**: Alberto e Michele, che guidano la costruzione ([proposta §10](../../PRESENTAZIONE-CEO.md)); quanto rosso può arrivare a Claude Team lo decidono il parere legale e la valutazione d'impatto, entro la settimana 3 ([proposta §5.6](../../PRESENTAZIONE-CEO.md))

## Contesto

- Gli agenti ragionano con Claude via API ([proposta §6.2](../../PRESENTAZIONE-CEO.md)). L'API di Anthropic non ha una regione in UE e conserva input e output per 30 giorni, oppure zero su accordo, che però non vale per Claude Team ([ricerca/16 §5](../../ricerca/16-gdpr-ai-act-e-regole.md)).
- Claude Team non ha un registro di audit ([proposta §13](../../PRESENTAZIONE-CEO.md)) né, sul piano Team, una conservazione personalizzata ([ricerca/36 §1.3](../../ricerca/36-architettura-v2.md)).
- La regola 7 del sistema chiede di oscurare ciò che non serve prima del cloud e di usare solo fornitori con contratto commerciale e DPA, il contratto sul trattamento dei dati ([proposta §9.1](../../PRESENTAZIONE-CEO.md)).
- Con trascrizioni e CRM sul nostro server SerSan ne è titolare, con tutta la responsabilità della sicurezza ([ricerca/16 §5](../../ricerca/16-gdpr-ai-act-e-regole.md)).

## Decisione

Ogni dato ha un colore. Una regola scritta nel codice del Cancello, il nostro esecutore unico delle azioni esterne ([ADR-0003](0003-cancello-approvazioni.md)), decide cosa può uscire dal server e verso chi ([proposta §5.6](../../PRESENTAZIONE-CEO.md)):

| Colore | Cosa | Dove può andare |
|---|---|---|
| **Verde** | pubblico o interno non personale | qualunque fornitore ammesso, anche Claude Team |
| **Giallo** | contatti di lavoro, campi del CRM, riassunti | solo i fornitori del board, con contratto commerciale e DPA |
| **Rosso** | audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone, finanza | resta sul server, oppure va all'API Anthropic dopo aver oscurato in locale i dati non necessari |

- **Oscuramento locale**: un filtro sul nostro server toglie i dati personali che non servono prima che il testo vada all'API. Lo costruiamo e lo misuriamo nella fase 1, su CPU, con una prova di qualità ([proposta §5.6](../../PRESENTAZIONE-CEO.md), [ricerca/36 §7.3](../../ricerca/36-architettura-v2.md)).
- **Claude Team** riceve verde e giallo, e il rosso solo oscurato, finché parere e valutazione d'impatto non decidono diversamente. La ricerca nella memoria gli passa il rosso solo oscurato e tiene la finanza in una raccolta separata ([proposta §5.6](../../PRESENTAZIONE-CEO.md), [ricerca/36 §5.5](../../ricerca/36-architettura-v2.md), [ADR-0005](0005-memoria-postgres-qdrant-bookstack.md)).
- **Sul banco di prova** si salvano solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata: le trascrizioni si leggono, si oscurano in memoria e si tiene solo il riassunto ([proposta §11](../../PRESENTAZIONE-CEO.md), [ricerca/36 §5.7](../../ricerca/36-architettura-v2.md)).
- **Telegram, WhatsApp e Slack** ricevono solo dati verdi ([proposta §4.11](../../PRESENTAZIONE-CEO.md)).
- In più chiediamo ad Anthropic la conservazione zero dei dati delle API, che è gratuita ([proposta §14](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: affidarsi solo ai contratti, senza oscuramento

- **Pro**: Anthropic tratta i dati per nostro conto, non li usa per l'addestramento e sull'API può non conservarli ([ricerca/16, sintesi punto 8](../../ricerca/16-gdpr-ai-act-e-regole.md)).
- **Contro**: nessuna regione in UE; niente conservazione zero per Claude Team; i contenuti segnalati possono restare fino a 2 anni ([ricerca/16, sintesi punto 8](../../ricerca/16-gdpr-ai-act-e-regole.md)).
- **Perché no**: la minimizzazione chiede di togliere prima ciò che non serve; il contratto resta, come aggiunta ([proposta §9.1 e §14](../../PRESENTAZIONE-CEO.md)).

### Alternativa: Claude su AWS Bedrock in UE per i dati rossi

- **Pro**: su Bedrock, il servizio di Amazon che offre anche i modelli Claude, il calcolo può restare in data center europei, e con lui i dati ([ricerca/16 §5](../../ricerca/16-gdpr-ai-act-e-regole.md)).
- **Contro**: AWS non è nel board, quindi è un cloud in più ([ricerca/25 §2, C24](../../ricerca/25-board-michele-e-delta.md)); i crediti valgono solo sull'API diretta di Anthropic ([ricerca/21, giudizio compliance §3](../../ricerca/21-giudizio-compliance.md)).
- **Perché no**: resta un'uscita, solo con il sì di Michele e se un cliente lo chiede ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)).

### Alternativa: il rosso anche a Claude Team, con l'accesso della persona

- **Pro**: era la strada della proposta che dava valore prima, con meno pezzi accesi ([ricerca/35, giudizio sicurezza, in breve](../../ricerca/35-giudizio-sicurezza.md)).
- **Contro**: il piano Team non ha registro di audit, conservazione personalizzata né Compliance API, l'interfaccia per i controlli di conformità ([ricerca/35, giudizio sicurezza §2](../../ricerca/35-giudizio-sicurezza.md)).
- **Perché no**: va contro la regola dei tre colori, che manda il rosso all'API solo dopo l'oscuramento ([ricerca/35, giudizio sicurezza §3.2](../../ricerca/35-giudizio-sicurezza.md)).

## Conseguenze

### Positive

- Una regola che i CEO capiscono e che il codice applica ([ricerca/22 §3](../../ricerca/22-architettura-scelta.md), [proposta §5.6](../../PRESENTAZIONE-CEO.md)).
- Gli embedding, i vettori che rendono il testo ricercabile, si calcolano sulla nostra GPU: il contenuto non esce per essere indicizzato ([proposta §5.5](../../PRESENTAZIONE-CEO.md)).

### Negative

- L'oscuramento è un pezzo in più da costruire e misurare nella fase 1, e fino al parere chi interroga la memoria da Claude Team vede il rosso solo oscurato ([proposta §5.6](../../PRESENTAZIONE-CEO.md)).

### Rischi

- Quanto bene funziona l'oscuramento va ancora misurato ([ricerca/16 §5](../../ricerca/16-gdpr-ai-act-e-regole.md)): per questo la verifica della settimana 8 chiede che sul banco di prova non resti salvato nessun dato rosso ([proposta §11](../../PRESENTAZIONE-CEO.md)).
- I dati personali verso Claude Team vanno decisi nel parere e nella valutazione d'impatto entro la settimana 3 ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- Le sessioni degli agenti restano su disco 30 giorni di serie: i lavori con dati rossi non le salvano, e una cancellazione chiesta da un interessato arriva fino ai backup ([ricerca/36 §5.7](../../ricerca/36-architettura-v2.md)).

## Fonti

- [Proposta 2.1: §4.11, §5.5, §5.6, §6.2, §9.1, §10, §11, §13, §14](../../PRESENTAZIONE-CEO.md)
- [ricerca/16: GDPR, AI Act e regole operative (sintesi punto 8, §5)](../../ricerca/16-gdpr-ai-act-e-regole.md)
- [ricerca/36 §1.3, §5.5, §5.7, §7.3, §12: architettura v2](../../ricerca/36-architettura-v2.md)
- [ricerca/35: giudizio di sicurezza e privacy](../../ricerca/35-giudizio-sicurezza.md)
- [ricerca/25 §2 (C24): Bedrock e il board](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/21: giudizio di compliance §3](../../ricerca/21-giudizio-compliance.md)
- [ricerca/22 §3: i tre colori nel primo giro](../../ricerca/22-architettura-scelta.md)
