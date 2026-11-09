# ADR-0002: Tutto self-hosted dentro il board di Michele, in cloud solo i servizi del board

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata; Michele l'ha già recepita ([domande per Michele, "Già recepito"](../../DOMANDE-PER-MICHELE.md))

**Chi decide**: Michele Sanna (CPTO), autore del board, che è vincolante ([ricerca/25, intestazione](../../ricerca/25-board-michele-e-delta.md)); ogni eccezione chiede il suo sì ([proposta, appendice A, J9](../../PRESENTAZIONE-CEO.md)) e, se costa, una decisione dei CEO ([proposta §14, decisioni 8-10 e 15](../../PRESENTAZIONE-CEO.md)).

## Contesto

La prima versione, del 24 ottobre, usava molti servizi in abbonamento: Slack, Notion, Recall.ai, ElevenLabs, Hermes Cloud, un password manager, i backup in cloud ([proposta §12.1](../../PRESENTAZIONE-CEO.md); [ricerca/36 §6](../../ricerca/36-architettura-v2.md)). Il 25 ottobre Michele ha condiviso il board, il disegno della sua infrastruttura: in cloud restano "solo i servizi verticali: tutto l'IaaS generico (Azure) esce", cioè escono i server generici in affitto ([board di Michele, Cloud & SaaS che restano](../../allegati/infra/SerSan%20Infra%20Board.md)); "tutto il resto dev'essere self hosted", cioè sui nostri server ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)). Il server è già comprato: un HPE DL380 Gen10 con 192 GB di RAM e una GPU, a Cagliari ([proposta §6.1 e §12.2](../../PRESENTAZIONE-CEO.md)).

## Decisione

Tutto il sistema gira sul nostro server, in reti separate, dentro il board ([proposta §5.1](../../PRESENTAZIONE-CEO.md)).

- **In cloud solo i servizi del board**: M365 con Teams ed Entra, l'identità di Microsoft; Claude Team; le API di Anthropic dietro LiteLLM; Jira, Instantly, GitHub, Supabase, Vercel, il DNS ([proposta §1 e §5.1](../../PRESENTAZIONE-CEO.md)). Dal 5 novembre c'è anche una piccola macchina Oracle a Milano per l'accesso da fuori, scelta da Michele ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md); [ADR-0018](0018-accesso-oracle-netbird-pangolin.md)).
- **Sul server**, con Proxmox, che fa girare le macchine virtuali, stanno i servizi del board e quelli degli agenti: motore, Cancello, bot, server MCP, voce di Andrea ([proposta §5.2 e §6.2](../../PRESENTAZIONE-CEO.md)).
- **Poche eccezioni, approvate una per una**: linea telefonica di Andrea, WhatsApp, Telegram, Slack per i clienti, invio della newsletter, alcuni strumenti commerciali ([proposta §5.1](../../PRESENTAZIONE-CEO.md)).
- **SersanOutreach** lascia Azure nella fase F2 del board; il suo database resta su Supabase ([proposta §7.2](../../PRESENTAZIONE-CEO.md)).
- **Tempi**: il sistema di agenti corre accanto alla roadmap di Michele, F0-F5; ogni fase parte quando la precedente è verificata ([proposta §11](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: i servizi in abbonamento della prima versione

- **Pro**: meno da costruire: 110-147 giorni di sviluppo per le fasi 0-5 ([proposta §15](../../PRESENTAZIONE-CEO.md)).
- **Contro**: circa 968 € al mese a regime, contro i circa 479-583 € di questa versione; audio delle call e voce di Andrea passavano da fornitori negli USA ([proposta §12.1 e §5.6](../../PRESENTAZIONE-CEO.md)).
- **Perché no**: sono fuori dal board, che è vincolante ([ricerca/25 §2](../../ricerca/25-board-michele-e-delta.md)).

### Alternativa: restare su Azure

- **Pro**: SersanOutreach gira già lì ([proposta §7.1](../../PRESENTAZIONE-CEO.md)).
- **Contro**: una sola macchina virtuale con 15,6 GB condivisi fra produzione, prove e monitoraggio, circa 150 € al mese, e i dati in due cloud ([proposta §7.2](../../PRESENTAZIONE-CEO.md)).
- **Perché no**: il board fa uscire Azure, e spegnerla fa risparmiare circa 150 € al mese ([proposta §12.1](../../PRESENTAZIONE-CEO.md)).

### Alternativa: tutto in casa, senza eccezioni

- **Pro**: nessuna uscita da mettere nella valutazione d'impatto e nel registro dei trattamenti ([ricerca/35, giudizio di sicurezza §5](../../ricerca/35-giudizio-sicurezza.md)).
- **Contro**: alcune funzioni non si possono tenere in casa: Andrea ha bisogno di un operatore telefonico ([ricerca/33 §1](../../ricerca/33-costi-v2.md)); Exchange Online, la posta di M365, non è fatto per la newsletter in massa ([ricerca/36 §4.1](../../ricerca/36-architettura-v2.md)); Apollo è una banca dati di contatti ([ricerca/25 §7, N08](../../ricerca/25-board-michele-e-delta.md)).
- **Perché no**: nessuna funzione si toglie; ciò che non può stare sul server diventa una necessità esterna con il suo costo ([ricerca/36, intestazione](../../ricerca/36-architettura-v2.md)).

## Conseguenze

### Positive

- Escono abbonamenti per circa 257 € al mese ([ricerca/33 §2.1](../../ricerca/33-costi-v2.md)). In più rispetto a oggi: circa 135 € al mese finché Azure resta accesa, da circa -15 a +20 € nella fase 2 con Azure spenta, da circa -1 a +70 € nelle fasi 3-4, da circa 46 a 168 € nelle fasi 5-6 con Andrea ([proposta §12.1](../../PRESENTAZIONE-CEO.md)).
- L'audio delle call resta in casa e si trascrive in casa ([proposta §5.6](../../PRESENTAZIONE-CEO.md)).

### Negative

- Chat, bot nelle call, voce di Andrea, newsletter, programmazione dei post, firma e fatture li costruiamo e gestiamo noi: per questo il totale sale a circa 249-332 giorni di sviluppo, più 29 di esercizio e patch ([proposta §15](../../PRESENTAZIONE-CEO.md)).
- 11-13 servizi e 3 reti nuove entrano nel perimetro di Cyber Essentials, la certificazione di sicurezza inglese, con le patch entro 14 giorni ([proposta §13](../../PRESENTAZIONE-CEO.md)).

### Rischi

- **Il tempo di chi amministra il server**: prima della fase F4 del board entrano solo i servizi del pilota, ognuno con un responsabile delle patch ([proposta §13 e appendice B](../../PRESENTAZIONE-CEO.md)).
- **Rete, corrente e backup**: una sola linea internet; batterie usate e senza garanzia nell'UPS, il gruppo di continuità; firewall fuori supporto; backup ancora da completare. Le risposte: linea di riserva prima della fase 5 (decisione 13), test dell'UPS all'arrivo, domanda scritta all'ente di Cyber Essentials sul firewall, e nessun dato dei clienti sul server prima della verifica della settimana 21 ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **Piano gratuito di Oracle**: Oracle si riprende le macchine che per 7 giorni restano sotto il 20% di CPU, rete e memoria ([ricerca/37 §3](../../ricerca/37-hardware-risposte-michele.md); [domande per Michele, n. 4](../../DOMANDE-PER-MICHELE.md)); un server a pagamento costerebbe 6,49 € al mese ([proposta §14, decisione 7](../../PRESENTAZIONE-CEO.md)).

## Fonti

- [Proposta per i CEO, §1, §5.1, §5.2, §5.6, §6.1, §6.2, §7.1, §7.2, §11, §12, §13, §14, §15, appendici A e B](../../PRESENTAZIONE-CEO.md)
- [Domande tecniche per Michele, "Già recepito" e n. 4](../../DOMANDE-PER-MICHELE.md)
- [ADR-0018, l'accesso da fuori](0018-accesso-oracle-netbird-pangolin.md)
- [Board dell'infrastruttura di Michele, Cloud & SaaS che restano](../../allegati/infra/SerSan%20Infra%20Board.md)
- [ricerca/25, il board di Michele e le correzioni, intestazione, §1, §2 e §7](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/33, costi v2, §1 e §2.1](../../ricerca/33-costi-v2.md)
- [ricerca/35, giudizio di sicurezza §5](../../ricerca/35-giudizio-sicurezza.md)
- [ricerca/36, architettura v2, intestazione, §4.1 e §6](../../ricerca/36-architettura-v2.md)
- [ricerca/37, le risposte di Michele sull'hardware, §2 e §3](../../ricerca/37-hardware-risposte-michele.md)
