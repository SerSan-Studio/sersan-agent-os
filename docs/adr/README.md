# Architecture Decision Records

Ogni ADR (Architecture Decision Record) registra una decisione di architettura di SerSan Agent OS: contesto, scelta, alternative scartate e conseguenze, con i rimandi alle fonti.

| ADR | Titolo | Stato | Data |
|---|---|---|---|
| [ADR-0001](0001-motore-agent-sdk.md) | Motore degli agenti costruito sull'Agent SDK di Claude | accettata | 2026-10-25 |
| [ADR-0002](0002-self-hosted-board-michele.md) | Tutto self-hosted dentro il board di Michele, in cloud solo i servizi del board | accettata | 2026-10-25 |
| [ADR-0003](0003-cancello-approvazioni.md) | Il Cancello: unico esecutore delle azioni esterne, con carte di approvazione | accettata | 2026-10-25 |
| [ADR-0004](0004-litellm-banca-token.md) | LiteLLM come banca dei token e unico accesso ai modelli | accettata | 2026-10-25 |
| [ADR-0005](0005-memoria-postgres-qdrant-bookstack.md) | Memoria aziendale su PostgreSQL 16, Qdrant e BookStack, embedding in casa | accettata | 2026-10-25 |
| [ADR-0006](0006-teams-chat-di-gruppo.md) | Teams come chat di gruppo, Telegram, Slack e WhatsApp dallo stesso codice, Buzz in prova | accettata per Teams e Buzz in prova; i canali in più sono la decisione 8, proposta | 2026-10-25 |
| [ADR-0007](0007-call-e-trascrizione.md) | Call: trascrizione di Teams per le nostre, Vexa e trascrizione in casa per le altre | accettata | 2026-10-25 |
| [ADR-0008](0008-andrea-centralino.md) | "Andrea": centralino Asterisk e Pipecat con linea italiana, solo richiamate richieste | proposta (decisione 10) | da decidere |
| [ADR-0009](0009-dati-tre-colori.md) | Dati a tre colori e oscuramento locale prima del cloud | accettata | 2026-10-25 |
| [ADR-0010](0010-typescript-motore.md) | TypeScript come linguaggio del motore | proposta (domanda 28 per Mattia) | da decidere |
| [ADR-0011](0011-n8n-orari-integrazioni.md) | n8n per orari e integrazioni, il motore non lo duplica | accettata | 2026-10-25 |
| [ADR-0012](0012-hermes-uscita.md) | Hermes come uscita già prezzata, con le verifiche delle settimane 8 e 21 | accettata | 2026-10-25 |
| [ADR-0013](0013-postiz-listmonk-docuseal.md) | Postiz, listmonk e DocuSeal in casa per post, newsletter e firme | proposta (decisioni 9, 15, 21 e 22) | da decidere |
| [ADR-0014](0014-seconda-gpu-blackwell.md) | Seconda GPU: RTX PRO 2000 Blackwell da 16 GB nel riser secondario | proposta (decisione 12; modello scelto da Michele il 2026-11-07) | da decidere |
| [ADR-0015](0015-ram-384-gb.md) | RAM: altri 192 GB uguali a quelli montati | proposta (decisione 11) | da decidere |
| [ADR-0016](0016-backup-3-2-1.md) | Backup 3-2-1 con due Proxmox Backup Server, copia fuori sede in pull e cifrata | accettata (Michele); il pull aspetta il suo sì (domanda 14) | 2026-11-07 |
| [ADR-0017](0017-firewall-ups-rack.md) | Rack: firewall Sophos SG 230 con Proxmox e OPNsense, UPS HPE R1500 G5 con spegnimento a livelli | accettata (Michele) | 2026-11-05 |
| [ADR-0018](0018-accesso-oracle-netbird-pangolin.md) | Accesso da fuori attraverso una macchina Oracle a Milano, con NetBird e Pangolin | accettata (Michele) | 2026-11-05 |
| [ADR-0019](0019-linea-di-riserva.md) | Linea internet di riserva 4G/5G prima della fase 5 | proposta (decisione 13) | da decidere |
