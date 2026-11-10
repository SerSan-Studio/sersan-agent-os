# Architecture Decision Records

Ogni ADR (Architecture Decision Record) registra una decisione di architettura di SerSan Agent OS: contesto, scelta, alternative scartate e conseguenze, con i rimandi alle fonti.

Il 10 novembre 2026 i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio. Le ADR da 0020 a 0026 registrano le decisioni del terzo giro ([ricerca/45](../../ricerca/45-architettura-v3.md)); le ADR che cambiano per effetto di quelle decisioni hanno in fondo una sezione «Revisione del 10 novembre 2026».

| ADR | Titolo | Stato | Data |
|---|---|---|---|
| [ADR-0001](0001-motore-agent-sdk.md) | Motore degli agenti costruito sull'Agent SDK di Claude | accettata; rivista da ADR-0021 (corsia S) | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0002](0002-self-hosted-board-michele.md) | Tutto self-hosted dentro il board di Michele, in cloud solo i servizi del board | accettata | 2026-10-25 |
| [ADR-0003](0003-cancello-approvazioni.md) | Il Cancello: unico esecutore delle azioni esterne, con carte di approvazione | accettata; rivista da ADR-0020 e ADR-0023 | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0004](0004-litellm-banca-token.md) | LiteLLM come banca dei token e unico accesso ai modelli | accettata; rivista da ADR-0020 e ADR-0025 | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0005](0005-memoria-postgres-qdrant-bookstack.md) | Memoria aziendale su PostgreSQL 16, Qdrant e BookStack, embedding in casa | accettata | 2026-10-25 |
| [ADR-0006](0006-teams-chat-di-gruppo.md) | Teams come chat di gruppo, Telegram, Slack e WhatsApp dallo stesso codice, Buzz in prova | accettata per Teams; Buzz e stanza degli agenti rivisti da ADR-0026; i canali in più sono la decisione 8, proposta | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0007](0007-call-e-trascrizione.md) | Call: trascrizione di Teams per le nostre, Vexa e trascrizione in casa per le altre | accettata | 2026-10-25 |
| [ADR-0008](0008-andrea-centralino.md) | "Andrea": centralino Asterisk e Pipecat con linea italiana, solo richiamate richieste | accettata dal gruppo di progetto; le chiamate vere aspettano il parere | 2026-11-10 |
| [ADR-0009](0009-dati-tre-colori.md) | Dati a tre colori e oscuramento locale prima del cloud | accettata | 2026-10-25 |
| [ADR-0010](0010-typescript-motore.md) | TypeScript come linguaggio del motore | accettata dal gruppo di progetto, per le due corsie e il Cancello | 2026-11-10 |
| [ADR-0011](0011-n8n-orari-integrazioni.md) | n8n per orari e integrazioni, il motore non lo duplica | accettata; rivista da ADR-0022 (sveglia nel motore, n8n facoltativo) | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0012](0012-hermes-uscita.md) | Hermes come uscita già prezzata, con le verifiche delle settimane 8 e 21 | accettata; rivista da ADR-0021 e ADR-0023 | 2026-10-25; rivista il 2026-11-10 |
| [ADR-0013](0013-postiz-listmonk-docuseal.md) | Postiz, listmonk e DocuSeal in casa per post, newsletter e firme | accettata dal gruppo di progetto; Michele ammette i servizi nuovi | 2026-11-10 |
| [ADR-0014](0014-seconda-gpu-blackwell.md) | Seconda GPU: RTX PRO 2000 Blackwell da 16 GB nel riser secondario | proposta, da chiudere con Michele: confronto con la scheda da 24 GB (ADR-0025) | 2026-11-08; rivista il 2026-11-10 |
| [ADR-0015](0015-ram-384-gb.md) | RAM: altri 192 GB uguali a quelli montati | accettata dal gruppo di progetto con Michele; il momento lo decidono insieme | 2026-11-10 |
| [ADR-0016](0016-backup-3-2-1.md) | Backup 3-2-1 con due Proxmox Backup Server, copia fuori sede in pull e cifrata | accettata (Michele); il pull aspetta il suo sì (domanda 14) | 2026-11-07 |
| [ADR-0017](0017-firewall-ups-rack.md) | Rack: firewall Sophos SG 230 con Proxmox e OPNsense, UPS HPE R1500 G5 con spegnimento a livelli | accettata (Michele) | 2026-11-05 |
| [ADR-0018](0018-accesso-oracle-netbird-pangolin.md) | Accesso da fuori attraverso una macchina Oracle a Milano, con NetBird e Pangolin | accettata (Michele) | 2026-11-05 |
| [ADR-0019](0019-linea-di-riserva.md) | Linea internet di riserva 4G/5G prima della fase 5 | accettata dal gruppo di progetto, anticipata a prima del primo L3 esterno fuori orario | 2026-11-10 |
| [ADR-0020](0020-autonomia-a-livelli.md) | Autonomia a livelli per terna, decisa dal Cancello | accettata | 2026-11-10 |
| [ADR-0021](0021-motore-a-due-corsie.md) | Motore a due corsie: catene a schema e sessioni dell'Agent SDK nello stesso codice | accettata | 2026-11-10 |
| [ADR-0022](0022-eventi-e-sveglia-nel-motore.md) | Eventi e sveglia nel motore; n8n facoltativo, routine di Claude solo per uso personale | accettata | 2026-11-10 |
| [ADR-0023](0023-protezioni-essenziali.md) | Protezioni essenziali per un sistema aziendale chiuso | accettata | 2026-11-10 |
| [ADR-0024](0024-abbonamenti-come-riserva.md) | Abbonamenti come riserva: Managed Agents sui dati verdi, compiti programmati di Claude Team per uso personale | accettata | 2026-11-10 |
| [ADR-0025](0025-un-modello-per-agente.md) | Un modello per agente, anche open-weight, tutti dietro LiteLLM | accettata; da chiudere con Michele il confronto fra GPU da 16 e da 24 GB | 2026-11-10 |
| [ADR-0026](0026-bacheca-e-gruppi-degli-agenti.md) | Bacheca e gruppi di chat degli agenti, anticipati; Buzz provato presto | accettata | 2026-11-10 |
