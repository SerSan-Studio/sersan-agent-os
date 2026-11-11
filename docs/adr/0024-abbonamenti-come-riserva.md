# ADR-0024: Abbonamenti come riserva: Managed Agents sui dati verdi, compiti programmati di Claude Team per uso personale

**Data**: 2026-11-10

**Stato**: accettata; rivista il 2026-11-11 da [ADR-0028](0028-instradamento-a-piu-motori.md): i posti Team non sono più solo riserva, servono la corsia T

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). Michele dice quando il server è pieno o fermo.

## Contesto

- La regola di casa è tutto self-hosted dentro il board di Michele ([ADR-0002](0002-self-hosted-board-michele.md)). Quando un pezzo non sta sul server, un abbonamento è ammesso; fra le offerte di Claude ospitate il più autonomo è Managed Agents ([ricerca/41 §8.2, punto 6](../../ricerca/41-novita-al-9-novembre.md)).
- La proposta «ibrido con abbonamenti» (P-C) metteva al centro Claude Managed Agents, il servizio in cui Anthropic fa girare il ciclo dell'agente ([ricerca/42, proposta C §2](../../ricerca/42-proposta-C-ibrido-abbonamenti.md)). È arrivata terza, con 72,6 punti ([ricerca/45 §1.1](../../ricerca/45-architettura-v3.md)).
- Managed Agents ha le funzioni di autonomia più ricche fra le offerte ospitate di Anthropic: deployment programmati con cron al minuto, policy `auto`, tetto di spesa per sessione, webhook, multiagente. Costa i token a listino più 0,08 $ per ora di sessione attiva. Ma la sede dei dati è solo negli USA, non è idoneo a ZDR e le trascrizioni restano finché non le cancelliamo ([ricerca/41 §2.1 e §2.2](../../ricerca/41-novita-al-9-novembre.md)).
- I compiti programmati di Claude Team (le routine) appartengono a un singolo account, agiscono come la persona, partono al massimo una volta l'ora e includono i connettori, scritture comprese ([ricerca/41 §1.4](../../ricerca/41-novita-al-9-novembre.md); [ricerca/35, giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).

## Decisione

- **Managed Agents è una riserva prezzata**, non la base ([ricerca/45 §1.3 e §3.1](../../ricerca/45-architettura-v3.md); [ricerca/18, «In breve», punto 4](../../ricerca/18-agenti-in-abbonamento.md)):
  - si usa **solo su dati verdi**, cioè pubblici o interni non personali ([ADR-0009](0009-dati-tre-colori.md));
  - si usa **solo se il server è pieno o fermo**: per esempio un brief pre-meeting quando le sessioni S sono tutte occupate, o un lavoro di ricerca durante un fermo del server;
  - le azioni esterne passano comunque dal Cancello, attraverso un server MCP ([ricerca/41 §8.2, punto 6](../../ricerca/41-novita-al-9-novembre.md));
  - ogni agente in riserva ha il suo tetto di spesa per sessione e la sua riga nel registro; lo stop di emergenza ne revoca la chiave [proposta].
- **I compiti programmati di Claude Team restano per l'uso personale** delle persone, sui loro posti. Nessun processo aziendale ci gira sopra ([ricerca/45 §7.1](../../ricerca/45-architettura-v3.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).
- **Claude Team resta lo strumento delle persone**: chat, skill, progetti, e le domande alla memoria con l'MCP RAG, con il vincolo dei dati rossi ([ricerca/45 §4.2](../../ricerca/45-architettura-v3.md)).
- **L'esecutore Metricool** è l'altro abbonamento preso da P-C: programma i post della pagina aziendale a L2 finché Postiz non entra ([ricerca/45 §1.3](../../ricerca/45-architettura-v3.md); [ADR-0013](0013-postiz-listmonk-docuseal.md)).

## Alternative considerate

### Alternativa: P-C come base, con Managed Agents al centro

- **Pro**: autonomia pronta, poco codice nostro, runtime economico (0,08 $ l'ora) e sandbox anche in casa ([ricerca/41 §8.2, punto 6](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: aggiunge fornitori, porta ciclo e trascrizioni negli USA senza ZDR, e uno stop che non ferma tutto in un colpo ([ricerca/45 §7.1](../../ricerca/45-architettura-v3.md); [ricerca/43, giudizio CPTO](../../ricerca/43-giudizio-cpto.md)).
- **Perché no**: il motore sta sul server ([ADR-0021](0021-motore-a-due-corsie.md)); Managed Agents copre solo i buchi di capacità.

### Alternativa: nessuna riserva in cloud

- **Pro**: nessun dato esce dal server oltre alle chiamate ai modelli ([ADR-0002](0002-self-hosted-board-michele.md)).
- **Contro**: con il server pieno o fermo il lavoro si ferma; una sola linea e una sola GPU fino agli acquisti ([ricerca/45 §10 e §11](../../ricerca/45-architettura-v3.md)).
- **Perché no**: la riserva costa circa 4-35 € al mese se usata [stima di P-C], solo su dati verdi ([ricerca/45 §9.2](../../ricerca/45-architettura-v3.md)).

### Alternativa: i compiti programmati di Claude Team per i processi aziendali

- **Pro**: inclusi nei posti già pagati ([ricerca/41 §1.4](../../ricerca/41-novita-al-9-novembre.md)).
- **Contro**: agiscono come la persona, dipendono dai limiti d'uso del suo posto, sono in anteprima e scavalcano il Cancello ([ricerca/41 §1.4 e §8.2](../../ricerca/41-novita-al-9-novembre.md); [ricerca/35, giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)).
- **Perché no**: la sveglia aziendale sta nel motore ([ADR-0022](0022-eventi-e-sveglia-nel-motore.md)).

## Conseguenze

### Positive

- Un buco di capacità non ferma i lavori sui dati verdi.
- Nessun canone nuovo nella base: la riserva si paga solo se si usa ([ricerca/45 §9.2](../../ricerca/45-architettura-v3.md)).

### Negative

- Un fornitore in più da seguire, con un'API in beta (header `managed-agents-2026-04-01`) ([ricerca/41 §2.1](../../ricerca/41-novita-al-9-novembre.md)).
- Le figure che possono andare in riserva vanno preparate due volte: nel motore e in Managed Agents.

### Rischi

- **Un dato giallo o rosso finisce in riserva**: il motore decide la riserva solo per agenti dichiarati verdi nel registro [proposta].
- **Spesa**: tetto per sessione di Managed Agents più il tetto per agente ([ricerca/41 §2.2](../../ricerca/41-novita-al-9-novembre.md); [ADR-0004](0004-litellm-banca-token.md)).

## Revisione dell'11 novembre 2026

- Gli abbonamenti non sono più solo una riserva. I posti Claude Team servono la **corsia T**: un compito programmato con l'avvio via API, sul posto della persona responsabile, per lo sviluppo di progetti in codice e i lavori lunghi, con la consegna come pull request ([ADR-0028](0028-instradamento-a-piu-motori.md)).
- Cambia quindi la regola «i compiti programmati di Claude Team restano per l'uso personale»: valgono anche per i lavori di sviluppo assegnati dal motore alla persona del posto, senza connettori e con il solo avvio API ([ricerca/49 §3](../../ricerca/49-instradamento-a-piu-motori.md)). Gli avvii a orario e da GitHub restano ai compiti personali; la stessa revisione è in [ADR-0022](0022-eventi-e-sveglia-nel-motore.md).
- Le obiezioni di questa ADR ai compiti programmati restano vere e la corsia T le contiene: agiscono come la persona (la consegna è solo una pull request, unita con il sì di una persona), dipendono dai limiti del posto (conto per posto e ripiego su S), sono in anteprima (adattatore separato), includono i connettori (si tolgono tutti) e sulle macchine di Anthropic stanno fuori dai ganci del Cancello (nessun effetto esterno dentro T) ([ADR-0028](0028-instradamento-a-piu-motori.md)).
- Managed Agents resta la riserva sui dati verdi; i crediti API inclusi nel piano Team coprono anche Managed Agents ([ricerca/49 §1.3](../../ricerca/49-instradamento-a-piu-motori.md)).

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §1.1, §1.3, §3.1, §4.2, §7.1, §9.2, §10, §11](../../ricerca/45-architettura-v3.md)
- [ricerca/41, novità al 9 novembre, §1.4, §2.1, §2.2 e §8.2](../../ricerca/41-novita-al-9-novembre.md)
- [ricerca/42, proposta C](../../ricerca/42-proposta-C-ibrido-abbonamenti.md)
- [ricerca/43, giudizio CPTO](../../ricerca/43-giudizio-cpto.md)
- [ricerca/18, agenti in abbonamento, «In breve»](../../ricerca/18-agenti-in-abbonamento.md)
- [ricerca/35, giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)
- [ADR-0002](0002-self-hosted-board-michele.md); [ADR-0004](0004-litellm-banca-token.md); [ADR-0009](0009-dati-tre-colori.md); [ADR-0013](0013-postiz-listmonk-docuseal.md); [ADR-0021](0021-motore-a-due-corsie.md); [ADR-0022](0022-eventi-e-sveglia-nel-motore.md)
