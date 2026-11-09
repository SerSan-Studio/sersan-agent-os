# ADR-0006: Teams come chat di gruppo, Telegram, Slack e WhatsApp dallo stesso codice, Buzz in prova

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata per Teams e per Buzz in prova; proposta per i canali in più, che sono la decisione 8 ([proposta §14](../../PRESENTAZIONE-CEO.md))

**Chi decide**: i CEO per i canali in più e per Teams nel piano M365, se oggi manca (decisioni 8 e 18, [proposta §14](../../PRESENTAZIONE-CEO.md)); Michele Sanna (CPTO) per le eccezioni fuori dal board e la registrazione dei bot ([proposta, appendice A, J9](../../PRESENTAZIONE-CEO.md); [domande per Michele, n. 5 e 10](../../DOMANDE-PER-MICHELE.md)).

## Contesto

L'idea vuole una chat di gruppo "come Buzz", con persone e agenti nelle stesse stanze, collegata a Slack, Telegram e WhatsApp, e una stanza dove si vede come gli agenti si passano il lavoro ([proposta, appendice A, J9 e A7](../../PRESENTAZIONE-CEO.md)). La prima versione usava Slack Pro ([ricerca/36 §6](../../ricerca/36-architettura-v2.md)). Il board di Michele non ha Slack e tiene M365 con Teams, che SerSan paga già ([ricerca/28, In breve](../../ricerca/28-chat-di-gruppo-self-hosted.md)). Le carte del Cancello, cioè le richieste di approvazione, devono arrivare sul telefono con l'identità certa di chi approva ([ricerca/28 §1](../../ricerca/28-chat-di-gruppo-self-hosted.md)).

## Decisione

- **Teams è la casa comune**: un canale per squadra, più "Approvazioni", "Agenti", "Ingresso", "Call di vendita", "Bandi" e un canale privato per ogni cliente. Nei canali condivisi con i clienti scrive solo il Cancello ([proposta §2.1 e §4.11](../../PRESENTAZIONE-CEO.md)).
- **La Porta chat**, un nostro servizio scritto con il Chat SDK, una libreria con licenza MIT, e con il Teams SDK di Microsoft, porta in Teams le carte dalla fase 1 e nove bot, uno per squadra, dalla fase 2 ([proposta §4.11 e §11](../../PRESENTAZIONE-CEO.md); [ricerca/36 §8.2 e §9.3](../../ricerca/36-architettura-v2.md)).
- **Le carte** arrivano sul telefono come Adaptive Card, cioè messaggi con pulsanti, e Teams dice al bot chi ha premuto ([ricerca/28, In breve](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **I passaggi fra agenti** stanno nel motore, con il freno: otto messaggi per discussione (thread), catene di tre passaggi, un tetto di spesa per catena; il canale "Agenti" li rispecchia ([proposta §4.11](../../PRESENTAZIONE-CEO.md); [ricerca/28 §2.6](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Dalla fase 3 gli stessi agenti, con lo stesso codice,** arrivano su Telegram per gli avvisi e su WhatsApp e Slack, soprattutto per i clienti. Lì passano solo dati verdi, cioè pubblici o interni non personali; le approvazioni restano in Teams ([proposta §4.11, §5.6 e §11](../../PRESENTAZIONE-CEO.md)).
- **Buzz**, la chat open source di Block per persone e agenti, gira dalla fase 4 sul banco di prova, sulla stessa bacheca, con circa 6 giorni di lavoro. Esce dal banco di prova quando non perde più risposte e le sue approvazioni funzionano: allora diventa la stanza degli agenti e, se è più comoda di Teams, la casa comune ([proposta §2.1, §4.11, §11 e §15](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: Slack, come nella prima versione

- **Pro**: con il Socket Mode le connessioni sono solo in uscita, senza porte aperte ([ricerca/28 §1](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Contro**: non è nel board; Slack Pro e Claude in Slack costavano 71,67 € al mese ([ricerca/28 §9](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Perché no**: la chat interna è Teams; Slack resta solo per i clienti che lo usano ([proposta §1 e §12.1](../../PRESENTAZIONE-CEO.md)).

### Alternativa: Buzz come casa comune da subito

- **Pro**: è il modello dell'idea, con agenti membri veri, che hanno un nome e un proprietario ([ricerca/28 §3](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Contro**: al 25 ottobre la versione 0.5.28 non aveva approvazioni collegate né ponti verso Teams, Telegram o WhatsApp ([ricerca/28 §3](../../ricerca/28-chat-di-gruppo-self-hosted.md)); con Claude le risposte possono sparire senza errore ([ricerca/26 §7.3](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: resta nel laboratorio, senza dati dei clienti, finché non supera i criteri d'uscita ([ricerca/36 §5.6](../../ricerca/36-architettura-v2.md)).

### Alternativa: Mattermost o Matrix sul nostro server

- **Pro**: Mattermost è la chat self-hosted più matura; Matrix è federata e cifrata ([ricerca/28 §4 e §5](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Contro**: sarebbe una seconda chat accanto a Teams; Matrix chiede Kubernetes, un sistema complesso per gestire i container, e non ha pulsanti standard ([ricerca/28 §4 e §5](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Perché no**: Mattermost resta il piano B se un giorno si esce da Teams; Matrix non conviene per quattro persone ([ricerca/28, In breve](../../ricerca/28-chat-di-gruppo-self-hosted.md)).

## Conseguenze

### Positive

- Teams c'è già con M365: 0 € in più se è nel piano, altrimenti 6-14 € al mese ([proposta §14, decisione 18](../../PRESENTAZIONE-CEO.md)).
- Una sola identità per chat e approvazioni: Entra, l'identità di Microsoft, con il secondo fattore e la chiave FIDO2 ([ricerca/28 §2.6](../../ricerca/28-chat-di-gruppo-self-hosted.md)); cambiare canale vuol dire cambiare adattatore ([ricerca/28 §10](../../ricerca/28-chat-di-gruppo-self-hosted.md)).

### Negative

- Il bot riceve i messaggi da Microsoft su una rotta pubblica, unica e firmata, dietro Pangolin e Traefik, i servizi che fanno da porta d'ingresso al server ([ricerca/28 §1](../../ricerca/28-chat-di-gruppo-self-hosted.md)); Porta e bot li scriviamo e manteniamo noi ([proposta §5.3](../../PRESENTAZIONE-CEO.md)).
- I canali in più costano: Telegram 0 €, Slack 0 o 27 € al mese, WhatsApp circa 7-12 € al mese ([proposta §14, decisione 8](../../PRESENTAZIONE-CEO.md)).

### Rischi

- **Bot di Teams senza Azure**: può dare errori di registrazione; prova nella fase 0, poi una registrazione Azure Bot gratuita o, in ultima istanza, la pagina del Cancello ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **WhatsApp**: solo l'API ufficiale di Meta, perché le soluzioni non ufficiali portano al blocco del numero ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **Buzz è giovane**: finché resta sul banco di prova, la stanza degli agenti è il canale "Agenti" di Teams ([proposta §13](../../PRESENTAZIONE-CEO.md)).

## Fonti

- [Proposta per i CEO, §1, §2.1, §4.11, §5.3, §5.6, §11, §12.1, §13, §14, §15 e appendice A](../../PRESENTAZIONE-CEO.md)
- [ricerca/26, Agent SDK, §7.3](../../ricerca/26-claude-agent-sdk.md)
- [ricerca/28, chat di gruppo, In breve, §1, §2.6, §3, §4, §5, §9 e §10](../../ricerca/28-chat-di-gruppo-self-hosted.md)
- [ricerca/36, architettura v2, §5.6, §6, §8.2 e §9.3](../../ricerca/36-architettura-v2.md)
- [Domande tecniche per Michele, n. 5 e 10](../../DOMANDE-PER-MICHELE.md)
