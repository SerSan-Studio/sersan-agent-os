# Architecture Decision Records

Ogni ADR (Architecture Decision Record) registra una decisione di architettura di SerSan Agent OS: contesto, scelta, alternative scartate e conseguenze, con i rimandi alle fonti.

Il 10 novembre 2026 i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio. Le ADR da 0020 a 0026 registrano le decisioni del terzo giro ([ricerca/45](../../ricerca/45-architettura-v3.md)); le ADR che cambiano per effetto di quelle decisioni hanno in fondo una sezione «Revisione del 10 novembre 2026». L'ADR-0027 registra il «decisore», nato dalla valutazione dei modelli System One ([ricerca/47](../../ricerca/47-modelli-system-one.md)); le ricerche 46 e 48 aggiornano le ADR 0005, 0014 e 0025. L'11 novembre l'ADR-0028 registra l'instradamento a più motori, con la corsia T sui posti Claude Team ([ricerca/49](../../ricerca/49-instradamento-a-piu-motori.md)); le ADR 0001, 0004, 0022, 0024, 0025 e 0027 hanno in fondo una sezione «Revisione dell'11 novembre 2026».

| ADR | Titolo | Stato | Data |
|---|---|---|---|
| [ADR-0001](0001-motore-agent-sdk.md) | Motore degli agenti costruito sull'Agent SDK di Claude | accettata; rivista da ADR-0021 (corsia S) e da ADR-0028 (posti Team per la corsia T, il motore resta sulla chiave API) | 2026-10-25; rivista il 2026-11-10 e il 2026-11-11 |
| [ADR-0002](0002-self-hosted-board-michele.md) | Tutto self-hosted dentro il board di Michele, in cloud solo i servizi del board | accettata | 2026-10-25 |
| [ADR-0003](0003-cancello-approvazioni.md) | Il Cancello: unico esecutore delle azioni esterne, con carte di approvazione | accettata; rivista da ADR-0020 e ADR-0023 | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0004](0004-litellm-banca-token.md) | LiteLLM come banca dei token e unico accesso ai modelli | accettata; rivista da ADR-0020, ADR-0025 e ADR-0028 (Jev via LiteLLM, la corsia T fuori da LiteLLM) | 2026-10-25; rivista il 2026-11-10 e il 2026-11-11 |
| [ADR-0005](0005-memoria-postgres-qdrant-bookstack.md) | Memoria aziendale su PostgreSQL 16, Qdrant e BookStack, embedding in casa | accettata; la casa dei testi si decide prima della fase 2 (ricerca/46) | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0006](0006-teams-chat-di-gruppo.md) | Teams come chat di gruppo, Telegram, Slack e WhatsApp dallo stesso codice, Buzz in prova | accettata per Teams; Buzz e stanza degli agenti rivisti da ADR-0026; i canali in più sono la decisione 8, proposta | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0007](0007-call-e-trascrizione.md) | Call: trascrizione di Teams per le nostre, Vexa e trascrizione in casa per le altre | accettata | 2026-10-25 |
| [ADR-0008](0008-andrea-centralino.md) | "Andrea": centralino Asterisk e Pipecat con linea italiana, solo richiamate richieste | accettata dal gruppo di progetto; le chiamate vere aspettano il parere | 2026-11-10 |
| [ADR-0009](0009-dati-tre-colori.md) | Dati a tre colori e oscuramento locale prima del cloud | accettata | 2026-10-25 |
| [ADR-0010](0010-typescript-motore.md) | TypeScript come linguaggio del motore | accettata dal gruppo di progetto, per le due corsie e il Cancello | 2026-11-10 |
| [ADR-0011](0011-n8n-orari-integrazioni.md) | n8n per orari e integrazioni, il motore non lo duplica | accettata; rivista da ADR-0022 (sveglia nel motore, n8n facoltativo) | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0012](0012-hermes-uscita.md) | Hermes come uscita già prezzata, con le verifiche delle settimane 8 e 21 | accettata; rivista da ADR-0021 e ADR-0023 | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0013](0013-postiz-listmonk-docuseal.md) | Postiz, listmonk e DocuSeal in casa per post, newsletter e firme | accettata dal gruppo di progetto; Michele ammette i servizi nuovi | 2026-11-10 |
| [ADR-0014](0014-seconda-gpu-blackwell.md) | Seconda GPU: RTX PRO 2000 Blackwell da 16 GB nel riser secondario | proposta a Michele: la scheda da 16 GB, da comprare per la milestone 2 (ricerca/48) | 2026-11-08; rivista il 2026-11-10 |
| [ADR-0015](0015-ram-384-gb.md) | RAM: altri 192 GB uguali a quelli montati | accettata dal gruppo di progetto con Michele; il momento lo decidono insieme | 2026-11-10 |
| [ADR-0016](0016-backup-3-2-1.md) | Backup 3-2-1 con due Proxmox Backup Server, copia fuori sede in pull e cifrata | accettata (Michele); il pull aspetta il suo sì (domanda 14) | 2026-11-07 |
| [ADR-0017](0017-firewall-ups-rack.md) | Rack: firewall Sophos SG 230 con Proxmox e OPNsense, UPS HPE R1500 G5 con spegnimento a livelli | accettata (Michele) | 2026-11-05 |
| [ADR-0018](0018-accesso-oracle-netbird-pangolin.md) | Accesso da fuori attraverso una macchina Oracle a Milano, con NetBird e Pangolin | accettata (Michele) | 2026-11-05 |
| [ADR-0019](0019-linea-di-riserva.md) | Linea internet di riserva 4G/5G, prima del primo lavoro L3 esterno fuori orario | accettata dal gruppo di progetto | 2026-11-10 |
| [ADR-0020](0020-autonomia-a-livelli.md) | Autonomia a livelli per terna, decisa dal Cancello | accettata | 2026-11-10 |
| [ADR-0021](0021-motore-a-due-corsie.md) | Motore a due corsie: catene a schema e sessioni dell'Agent SDK nello stesso codice | accettata | 2026-11-10 |
| [ADR-0022](0022-eventi-e-sveglia-nel-motore.md) | Eventi e sveglia nel motore; n8n facoltativo, routine di Claude solo per uso personale | accettata; rivista da ADR-0028: il motore può avviare i compiti programmati della corsia T con il solo avvio API | 2026-11-10; rivista il 2026-11-11 |
| [ADR-0023](0023-protezioni-essenziali.md) | Protezioni essenziali per un sistema aziendale chiuso | accettata | 2026-11-10 |
| [ADR-0024](0024-abbonamenti-come-riserva.md) | Abbonamenti come riserva: Managed Agents sui dati verdi, compiti programmati di Claude Team per uso personale | accettata; rivista da ADR-0028: i posti Team non sono più solo riserva, servono la corsia T | 2026-11-10; rivista il 2026-11-11 |
| [ADR-0025](0025-un-modello-per-agente.md) | Un modello per agente, anche open-weight, tutti dietro LiteLLM | accettata; aggiornata dopo ricerca/47 e 48: registro dei modelli con capacità, proposta della GPU da 16 GB; rivista da ADR-0028: il registro serve anche a scegliere la destinazione | 2026-11-10; rivista il 2026-11-11 |
| [ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md) | Bacheca e gruppi di chat degli agenti, anticipati; Buzz provato presto | accettata | 2026-11-10 |
| [ADR-0027](0027-decisore.md) | Il «decisore»: domande tipizzate e soglie in un file, e un dubbio rende il sistema più prudente | accettata; i motori si scelgono con la prova della milestone 2; rivista da ADR-0028: l'italiano non è un freno, Jev motore di partenza sui testi verdi e gialli | 2026-11-10; rivista il 2026-11-11 |
| [ADR-0028](0028-instradamento-a-piu-motori.md) | Instradamento a più motori, con la corsia T sui posti Claude Team | accettata dal gruppo di progetto; la corsia T entra dopo la prova e la conferma di Anthropic | 2026-11-11 |

## Come si contano le milestone

Le milestone in vigore sono le sette del PRD, elencate in [docs/06-sviluppo.md](../06-sviluppo.md). [ricerca/45 §6.4](../../ricerca/45-architettura-v3.md) le contava in un altro modo, perché la corsia S non era ancora stata anticipata. Le ricerche restano come sono state scritte; questa tabella mette i due conti uno accanto all'altro.

| Nel PRD, in vigore | Cosa porta | In ricerca/45 §6.4 |
|---|---|---|
| 1 | Cancello a livelli e corsia N, con la Sala di controllo | 1 |
| 2 | Corsia S, bacheca e gruppi degli agenti, prova di Buzz, primo modello open-weight | 7 e 8, allora nella fase 2 |
| 3 | Prove con Microsoft e LiteLLM | 2 |
| 4 | Telefono e posta | 3 |
| 5 | Dalla call al riassunto | 4 |
| 6 | Tre agenti sul banco | 5 |
| 7 | Collaudo della settimana 8 | 6 |

Dove un'ADR o una ricerca usa il conto vecchio:

- **[ADR-0020](0020-autonomia-a-livelli.md)**: gli invii veri ai clienti cominciano con la milestone di telefono e posta, la 4 del PRD. Il testo riporta tutti e due i conti.
- **[ADR-0028](0028-instradamento-a-piu-motori.md)** e [ricerca/49 §8](../../ricerca/49-instradamento-a-piu-motori.md): «milestone 2», quella del router e dell'adattatore di prova della corsia T, è la 3 del PRD; «milestone 3», quella della corsia T sui progetti veri, è la 4. Se il router si possa anticipare alla milestone 2 del PRD si decide con lo spec di quella milestone: serve LiteLLM, perché Jev si chiama da lì.
- **[ricerca/46](../../ricerca/46-obsidian-come-casa-dei-testi.md)**: «milestone 2 (prove con Teams e LiteLLM)» è la 3 del PRD.

Dove il conto è già quello del PRD:

- **[ADR-0014](0014-seconda-gpu-blackwell.md), [ADR-0025](0025-un-modello-per-agente.md), [ADR-0027](0027-decisore.md), [ricerca/47](../../ricerca/47-modelli-system-one.md) e [ricerca/48](../../ricerca/48-modelli-locali-e-gpu.md)**: la «milestone 2» della prova dei modelli locali, della prova del decisore e della seconda GPU è la 2 del PRD, dove entra il primo modello open-weight. La parte che passa da LiteLLM, come Jev, si chiude con le prove di LiteLLM della milestone 3.
