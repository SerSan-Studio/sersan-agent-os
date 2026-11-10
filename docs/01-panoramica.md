# SerSan Agent OS: panoramica

> **Nota del 10 novembre 2026.** Questo documento descrive ancora la versione 2 dell'architettura. Dal 10 novembre vale la versione 3, «Cancello a livelli e motore a due corsie»: la decisione è in [ricerca/45](../ricerca/45-architettura-v3.md) e nelle [ADR da 0020 a 0027](adr/README.md). Dove questo documento e le ADR dicono cose diverse, valgono le ADR. L'allineamento è in corso.

Stato al 9 novembre 2026. Cos'è il progetto, come è fatto, quali scelte lo reggono e a che punto è, con il rimando alla fonte di ogni fatto. La fonte di verità per costi, fasi, decisioni e rischi è la proposta per i CEO, [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026: se qui una cifra sembra diversa, vale la proposta.

## 1. Cos'è e che problema risolve

SerSan Agent OS è il «secondo cervello» aziendale di SerSan: SersanOutreach, marketing, contenuti, task, progetti e chiamate con i clienti diventano un solo sistema, con una memoria aziendale in cui entra tutto quello che diciamo, scriviamo e decidiamo. Su quella memoria lavorano con noi 57 agenti AI, programmi che ragionano con Claude, il modello di Anthropic, e fanno ognuno un lavoro preciso. SersanOutreach, la nostra piattaforma per contattare i potenziali clienti su LinkedIn e per email, diventa il loro CRM, cioè il registro di contatti e trattative ([proposta §1, §5.1 e §7.1](../PRESENTAZIONE-CEO.md)).

SerSan è Sersan Limited, una società del Regno Unito con il team in Italia e l'ufficio a Cagliari. Siamo in quattro: i CEO Alessandro Serratt e Michele Sanna, Alberto Tuveri, che ha preparato la proposta, e Mattia ([proposta, intestazione, §1, §2.3, §6.1 e §9.4](../PRESENTAZIONE-CEO.md); [domanda 29](../DOMANDE-PER-MICHELE.md)).

Il problema è che mancano le mani: ogni ora spesa in follow-up (i messaggi che seguono un incontro), brief (le schede che preparano gli incontri), proposte, post e report è tolta alla consegna o alla vendita. Al 5 ottobre SersanOutreach aveva 11 lead, cioè contatti da lavorare, 1 risposta e 0 meeting, e il marketing operativo è senza titolare dal 30 settembre. C'è poi un motivo commerciale: le nostre linee di servizio promettono ai clienti agenti che agiscono entro limiti decisi da loro, e un sistema così, usato da noi ogni giorno, è la prova migliore che sappiamo farlo ([proposta §1, §2.3 e §7.1](../PRESENTAZIONE-CEO.md)).

Dopo ogni call la bozza del follow-up arriverà sul telefono come «carta», una richiesta di approvazione con il testo esatto, e ogni mattina alle 7:00 ognuno riceverà il suo debrief, il punto della giornata. Nessun agente manda niente a un cliente senza il sì di una persona o una regola «Sempre», cioè un via libera che i CEO danno per un messaggio ripetitivo verso destinatari già noti. Fa eccezione «Andrea», l'agente vocale, che al telefono dice subito di essere un assistente AI e richiama da solo soltanto chi lo ha chiesto nel modulo ([proposta §1, §5.4 e §9.3](../PRESENTAZIONE-CEO.md)).

## 2. Nove squadre, 57 agenti

Ogni squadra ha un responsabile umano, perché «un agente senza un responsabile è un agente senza controllo»; l'elenco completo, con la fase di ogni agente, è nelle sezioni 4.1-4.9 della proposta ([proposta §4](../PRESENTAZIONE-CEO.md)).

| Squadra | Responsabile | Agenti | Cosa fa |
|---|---|---|---|
| Outbound | Alessandro (tecnico: Alberto) | 5 | email, LinkedIn e campagne di SersanOutreach |
| Chiamate | Alessandro | 5 | entra nelle call dichiarandolo, trascrive, riassume, fissa gli appuntamenti |
| Vendite | Alessandro | 8 | brief, proposte, contratti, coaching, «Andrea» |
| Marketing | Alberto | 8 | temi, concorrenza, metriche, post, newsletter, sito, eventi |
| Studio contenuti | Alberto | 4 | testi, slide, video e grafiche |
| Progetti | Michele, con Mattia | 8 | dalla firma del cliente al caso studio |
| Memoria | Michele | 5 | raccoglie, pulisce e tiene la memoria; sorveglia il server |
| Direzione | Alessandro e Michele | 10 | smistamento, debrief, budget, registro, stop di emergenza |
| Amministrazione | Alessandro e Michele | 4 | fatture, acquisti, controllo di gestione, bandi |

Persone e agenti stanno in una chat di gruppo su Microsoft Teams, che abbiamo già con Microsoft 365 (M365), con un canale per squadra. Ogni agente ha una riga nel registro, con responsabile, permessi, tetto di spesa e costo, e il registro si vede come organigramma ([proposta §4.11 e §4.12](../PRESENTAZIONE-CEO.md)).

## 3. Le scelte principali

Le scelte vengono da due giri di confronto. In ognuno quattro agenti giudici, cioè agenti AI con una lente ciascuno (visione, commerciale, tecnica, sicurezza e privacy), hanno dato i punti alle architetture proposte. Il 24 ottobre, su sette architetture, aveva vinto Hermes Agent insieme al Cancello, il nostro programma che esegue le azioni verso l'esterno; Hermes è un agente open source, cioè con il codice pubblico e libero, che ha già pronti canali e profili. Il 25 ottobre il confronto è stato rifatto su tre architetture dentro il board di Michele, cioè il disegno della sua infrastruttura ([allegati/infra](../allegati/infra/)), e ha vinto il motore sull'Agent SDK, il kit di Anthropic per costruire agenti, con 171,5 punti su 240. Seguono con 170 la proposta centrata su Claude Team, l'abbonamento di Claude per le persone, e con 137 Hermes sul nostro server ([proposta §5.7 e appendice B](../PRESENTAZIONE-CEO.md); [ricerca/22 §1](../ricerca/22-architettura-scelta.md) e [ricerca/36 §1.1](../ricerca/36-architettura-v2.md)). Ogni scelta ha una scheda di decisione, un ADR (Architecture Decision Record), in [docs/adr/](adr/).

| Tema | Scelta | ADR | Fonte |
|---|---|---|---|
| Dove gira | tutto sul server dell'ufficio; in cloud solo i servizi del board, come M365, Claude Team, le API di Anthropic (l'accesso a Claude dai programmi) e Jira per task e progetti; le eccezioni, come la linea di Andrea, si approvano una per una | [0002](adr/0002-self-hosted-board-michele.md) | [proposta §5.1](../PRESENTAZIONE-CEO.md) |
| Motore | lo scriviamo noi sull'Agent SDK, cioè Claude Code, l'agente di Anthropic per programmare, usato come libreria, cioè come un pezzo del nostro programma | [0001](adr/0001-motore-agent-sdk.md) | [proposta §5.1](../PRESENTAZIONE-CEO.md) |
| Linguaggio | TypeScript, un linguaggio di programmazione: l'SDK in TypeScript ha più hook di quello in Python, cioè più punti in cui il nostro codice interviene, e può preparare i processi in anticipo, così il primo messaggio non aspetta l'avvio; da confermare con Mattia | [0010](adr/0010-typescript-motore.md) | [ricerca/26 §1.3](../ricerca/26-claude-agent-sdk.md); [domanda 28](../DOMANDE-PER-MICHELE.md) |
| Orari e integrazioni | n8n, lo strumento di automazione già nel board | [0011](adr/0011-n8n-orari-integrazioni.md) | [proposta §5.3](../PRESENTAZIONE-CEO.md) |
| Modelli e budget | Claude via API, pagata a consumo, attraverso LiteLLM, il passaggio verso i modelli che dà un budget a ogni agente, squadra e persona | [0004](adr/0004-litellm-banca-token.md) | [proposta §4.8 e §5.1](../PRESENTAZIONE-CEO.md) |
| Azioni verso l'esterno | solo dal Cancello, con carte, chiave di sicurezza FIDO2 (una chiavetta fisica) per le più delicate, regole «Sempre» con scadenza e registro | [0003](adr/0003-cancello-approvazioni.md) | [proposta §5.4](../PRESENTAZIONE-CEO.md) |
| Dati | tre colori, verde, giallo e rosso, decidono cosa esce dal server e verso chi | [0009](adr/0009-dati-tre-colori.md) | [proposta §5.6](../PRESENTAZIONE-CEO.md) |
| Memoria | BookStack (il wiki aziendale), PostgreSQL (il database a tabelle) e Qdrant (il database vettoriale, che trova i testi per significato) sul server; gli embedding, cioè i testi tradotti in numeri per quella ricerca, si calcolano sulla nostra GPU, la scheda che fa in casa i lavori di AI | [0005](adr/0005-memoria-postgres-qdrant-bookstack.md) | [proposta §5.5](../PRESENTAZIONE-CEO.md) |
| Chat | Teams con nove bot di squadra; Telegram, WhatsApp e Slack dalla fase 3; Buzz, la chat di Block per persone e agenti, in prova | [0006](adr/0006-teams-chat-di-gruppo.md) | [proposta §4.11](../PRESENTAZIONE-CEO.md) |
| Call | trascrizione di Microsoft nelle nostre call Teams; Vexa, un bot sul nostro server, in quelle dei clienti | [0007](adr/0007-call-e-trascrizione.md) | [proposta §4.2 e §5.2](../PRESENTAZIONE-CEO.md) |
| Voce | «Andrea» con Asterisk, il centralino sul server, e una linea telefonica italiana | [0008](adr/0008-andrea-centralino.md) | [proposta §5.2](../PRESENTAZIONE-CEO.md) |
| Post, newsletter, firma, fatture | Postiz per i post, listmonk per la newsletter e DocuSeal per la firma, sul nostro server invece che in abbonamento (l'invio della newsletter passa da un servizio di posta esterno); per le fatture lo strumento che usiamo già, se va bene, altrimenti uno sul nostro server | [0013](adr/0013-postiz-listmonk-docuseal.md) | [proposta §5.2, §8.2, §14 e §15](../PRESENTAZIONE-CEO.md) |
| Uscita | Hermes, se il motore non regge le verifiche delle settimane 8 e 21 | [0012](adr/0012-hermes-uscita.md) | [proposta §5.7](../PRESENTAZIONE-CEO.md) |
| GPU | seconda GPU RTX PRO 2000 Blackwell da 16 GB, scelta da Michele, dalla fase 3 ed entro l'inizio della fase 5 | [0014](adr/0014-seconda-gpu-blackwell.md) | [proposta §6.4](../PRESENTAZIONE-CEO.md) |
| RAM | memoria di lavoro del server da 192 a 384 GB, prima della fase 3 | [0015](adr/0015-ram-384-gb.md) | [proposta §6.3](../PRESENTAZIONE-CEO.md) |
| Backup | regola 3-2-1, cioè tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio: oltre ai dati sul server, una copia in sede e una a casa di Michele, entro marzo 2027 | [0016](adr/0016-backup-3-2-1.md) | [proposta §6.1 e §12.2](../PRESENTAZIONE-CEO.md) |
| Rack | nel rack, l'armadio dei server: firewall Sophos (l'apparecchio che filtra il traffico fra internet e le nostre reti) con Proxmox, il sistema delle macchine virtuali, e OPNsense, il software del firewall; UPS, il gruppo di continuità | [0017](adr/0017-firewall-ups-rack.md) | [proposta §6.1](../PRESENTAZIONE-CEO.md) |
| Accesso da fuori | NetBird, la rete privata del team, e Pangolin, che rende raggiungibili da internet i pochi servizi che servono, su una macchina Oracle Cloud a Milano | [0018](adr/0018-accesso-oracle-netbird-pangolin.md) | [proposta §5.2 e §6.1](../PRESENTAZIONE-CEO.md) |
| Linea di riserva | 4G/5G con una SIM dati aziendale, prima della fase 5 | [0019](adr/0019-linea-di-riserva.md) | [proposta §14](../PRESENTAZIONE-CEO.md) |

Non tutte le righe sono già decise. Le scelte tecniche le ha studiate il gruppo di progetto, quelle sull'infrastruttura restano di Michele, e ai CEO spettano le decisioni di budget, abbonamenti, acquisti e integrazioni della sezione 14 della proposta. Finché i CEO non decidono, restano quindi proposte i canali in più (decisione 8), «Andrea» (decisione 10), la RAM (11), la seconda GPU (12), la linea di riserva (13) e gli strumenti per post, newsletter, firma e fatture (9, 15, 21 e 22). Backup, rack e accesso da fuori sono scelte di Michele, ma le spese che restano aspettano il sì dei CEO (decisioni 4, 7 e 17); TypeScript aspetta la risposta alla domanda 28 ([proposta §14](../PRESENTAZIONE-CEO.md); [domanda 28](../DOMANDE-PER-MICHELE.md)). Lo stato di ogni scheda è nell'[indice degli ADR](adr/README.md).

La macchina degli agenti non ha accesso a internet: parla solo con LiteLLM, con il Cancello e con i server MCP, le «prese» standard a cui un agente si collega ([proposta §5.4 e §7.3](../PRESENTAZIONE-CEO.md)).

## 4. Lo stato al 9 novembre 2026

**La proposta** è alla versione 2.1 dell'8 novembre. Recepisce le risposte di Michele sull'hardware del 7 novembre e la board del rack del 5, cioè lo schema dell'armadio dei server, ed è stata rivista l'8 e il 9 novembre da quattro revisori, ognuno con un verificatore ([ricerca/37 §1, §2 e §7](../ricerca/37-hardware-risposte-michele.md)).

**Il piano** ha sette fasi in circa 53 settimane, accanto alle fasi F0-F5 del board, che porta avanti Michele. Il costo vero è il tempo di sviluppo: circa 249-332 giorni (il valore più alto comprende una riserva di circa un terzo), più 29 giorni di esercizio e patch, cioè la gestione dei servizi e i loro aggiornamenti ([proposta §1, §11 e §15](../PRESENTAZIONE-CEO.md)).

| Fase | Settimane | Cosa arriva | Agenti al lavoro |
|---|---|---|---|
| 0. Valore subito e prove | 1-4 | Claude Team per tutti, decisione sull'email, sicurezza di SersanOutreach | – |
| 1. Pilota su banco di prova | 5-8 | post-call e debrief su una macchina di prova | 3 |
| 2. Pilota sul server e squadre che si parlano | 9-21 | motore sul server, nove bot di squadra in Teams, SersanOutreach collegato | 14 |
| 3. Memoria, call, vendite preparate e canali | 22-35 | ricerca nella memoria, bot nelle call dei clienti, Telegram, Slack e WhatsApp | 32 |
| 4. Organizzazione, newsletter e Buzz | 36-40 | newsletter e post dal nostro server, mappa dei processi | 42 |
| 5. Vendite e voce | 41-48 | «Andrea» e coaching, solo con parere legale e lead vere | 46 |
| 6. Le altre automazioni | 49-53 | firma elettronica, fatturazione, assistente personale | 57 |

**Cosa si chiede oggi ai CEO** (le cifre, come nella proposta, sono IVA esclusa; [proposta §1 e §12](../PRESENTAZIONE-CEO.md)):

1. il via alle fasi 0 e 1, le prime otto settimane (40,5-54 giorni di sviluppo), con una verifica alla settimana 8 su criteri tecnici e commerciali;
2. nessun abbonamento nuovo oltre a quelli del board: Proxmox (20 € al mese), IP fisso (fino a 10 €), macchina Oracle (0 € sul piano gratuito, 6,49 € al mese con un server a pagamento) e, se Michele li sceglie, gli abbonamenti Proxmox per firewall e backup (fino a circa 103 € al mese);
3. un budget una tantum di circa 2.900-3.890 € per parere legale (tetto 2.500 €), credito API se serve, backup in sede, chiavi FIDO2 e accessori, più circa 140-550 € per le batterie dell'UPS se il test all'arrivo va male.

In tutto le decisioni della sezione 14 sono 23 ([proposta §14](../PRESENTAZIONE-CEO.md)). La spesa mensile in più è di circa 135 € finché resta accesa Azure, il cloud di Microsoft dove oggi gira SersanOutreach, e di circa 46-168 € nelle fasi 5-6; il listino a regime, cioè quanto costa ogni mese il sistema completo nella fase 6, è di circa 479-583 €, contro i circa 968 € della prima versione. Le API di Claude dovrebbero stare nei crediti del bundle per startup, che rende gratuito anche il primo anno di Claude Team ([proposta §1 e §12.1](../PRESENTAZIONE-CEO.md)).

**Cosa è già comprato.** L'hardware principale, compresi firewall e UPS da rack, per circa 2.975 € dei 3.200 € del budget del board (cifre del board, con l'IVA d'importazione): un server HPE ProLiant DL380 Gen10 con due processori Xeon Gold 5218, 192 GB di RAM, dischi in mirror, cioè doppi, e una GPU NVIDIA Quadro RTX 4000 da 8 GB, nel rack dell'ufficio di Cagliari. L'8 novembre firewall e UPS erano in arrivo. Ci sono già anche cinque posti Claude Team, i crediti API di Anthropic e M365 con Teams ([proposta §1, §6.1 e §12.2](../PRESENTAZIONE-CEO.md)).

**Cosa resta aperto.** Le 30 domande tecniche del file per Michele, dai tempi del board alla rete, ai servizi nuovi, ai backup e all'hardware; le ultime tre, sul linguaggio del motore, su chi fattura e sui canali dei clienti, sono per tutti e quattro ([DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md)). Nella prima settimana verifichiamo cosa include il bundle per startup e quali piani M365 e Jira abbiamo ([proposta §14](../PRESENTAZIONE-CEO.md)).

## 5. Come è organizzata la repo

- [README.md](../README.md): la porta d'ingresso.
- [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md), anche in `.docx` e `.pdf`: la proposta per i CEO. L'appendice A collega ognuna delle 90 voci al suo componente e alla sua fase: sono le funzioni dell'idea più 12 automazioni in più che proponiamo noi (le voci L).
- [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md): le domande tecniche sull'infrastruttura.
- `docs/`, la documentazione di progetto: questa panoramica, [le alternative](02-alternative.md), [l'architettura](03-architettura.md), [il tech stack](04-tech-stack.md), cioè programmi e servizi che usiamo, [il design](05-design.md) e [lo sviluppo](06-sviluppo.md), con fasi, verifiche, giorni e rischi; in [docs/adr/](adr/) le 19 schede di decisione, con il loro [indice](adr/README.md).
- [ricerca/](../ricerca/): i rapporti da cui vengono i fatti. 00 le funzioni dell'idea, 01 SersanOutreach, 05 marketing; 10-24 il primo giro, con le sette proposte; 25-37 il secondo giro, dentro il board di Michele, fino all'architettura v2 e all'hardware.
- [allegati/](../allegati/): il board di Michele e la board del rack (`infra/`), i documenti di SersanOutreach (`sersanoutreach/`) e il piano marketing (`marketing/`).
- [strumenti/](../strumenti/): `md_to_docx.py`, che trasforma la proposta in DOCX con lo stile SerSan partendo dal modello `modello-stile-sersan.docx`, e il marchio (`marchio.py` e `brand/`).
