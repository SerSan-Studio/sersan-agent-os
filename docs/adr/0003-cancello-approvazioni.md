# ADR-0003: Il Cancello: unico esecutore delle azioni esterne, con carte di approvazione

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata; rivista il 2026-11-10 da [ADR-0020](0020-autonomia-a-livelli.md) e [ADR-0023](0023-protezioni-essenziali.md): livelli al posto della carta per ogni azione

**Chi decide**: Michele Sanna (CPTO) con Alberto Tuveri per il disegno tecnico ([ricerca/36 §10](../../ricerca/36-architettura-v2.md)); i CEO per la revisione esterna di sicurezza ([proposta §14, decisione 5](../../PRESENTAZIONE-CEO.md)) e, dopo il parere legale, per i messaggi ai clienti che possono diventare regole "Sempre" ([proposta, appendice A, B5](../../PRESENTAZIONE-CEO.md)).

## Contesto

Gli agenti leggono posta, trascrizioni e pagine web, e preparano mail, post, offerte e fatture. Il rischio numero uno sono le iniezioni di prompt, cioè istruzioni nascoste nel testo di terzi ([proposta §9.2](../../PRESENTAZIONE-CEO.md)). Le regole del sistema vogliono una persona nel giro per ogni azione esterna irreversibile ([proposta §9.1](../../PRESENTAZIONE-CEO.md)). Già il primo giro, il 24 ottobre, si reggeva su una regola: gli agenti preparano, una persona approva, un nostro programma esegue ([ricerca/22 §1](../../ricerca/22-architettura-scelta.md)). L'obiettivo è arrivare per gradi a un dopo-call senza lavoro a mano: riassunto, CRM (l'archivio di contatti e trattative), follow-up e to-do ([proposta §2.4 e §5.4](../../PRESENTAZIONE-CEO.md)).

## Decisione

Il Cancello è l'unico programma che può mandare una mail, scrivere al cliente, toccare il CRM o telefonare ([proposta §5.1](../../PRESENTAZIONE-CEO.md)). Funziona così ([proposta §5.4](../../PRESENTAZIONE-CEO.md)):

1. Un agente **propone** un'azione e una regola la classifica: lettura, scrittura interna, invio, pubblicazione, pagamento, cancellazione, credenziali.
2. Le azioni delicate diventano una **carta** in Teams, con il testo esatto, un codice che vale una volta e una scadenza.
3. Dopo il sì di una persona, l'**esecutore** agisce una volta sola; se il testo è cambiato, la carta non vale più. Offerte, contratti, fatture e primi contatti chiedono anche la chiave di sicurezza fisica FIDO2.
4. Tutto finisce nel **registro**: chi ha chiesto, chi ha approvato, quanto è costato.

- **Chi approva** dipende dalla classe: per esempio Alessandro gli invii ai clienti, Michele offerte e contratti; cancellazioni e credenziali sono sempre negate agli agenti ([ricerca/36 §5.8](../../ricerca/36-architettura-v2.md)).
- **Regole "Sempre"**: dopo 20 approvazioni uguali, senza modifiche, una persona può rendere l'azione automatica per quell'agente, quel tipo di azione e quella destinazione. La regola scade dopo 30 giorni e non vale mai per offerte, primi contatti, pagamenti, cancellazioni o destinatari nuovi ([proposta §5.4](../../PRESENTAZIONE-CEO.md)).
- **Nessun'altra strada verso fuori**: gli agenti non hanno internet e il Cancello sta in una macchina sua ([proposta §5.4](../../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1](../../ricerca/36-architettura-v2.md)).
- **Tempi**: versione 1 alla fine della fase 1, FIDO2 e regole "Sempre" nella fase 2, versione 2 nella fase 3 ([proposta §5.4 e §11](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: approvazioni con n8n

- **Pro**: n8n, lo strumento di automazioni del board, ha un nodo Teams che manda un messaggio e aspetta la risposta ([ricerca/28 §2.4](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Contro**: su Teams registra quando si risponde, non chi ([ricerca/28 §2.4](../../ricerca/28-chat-di-gruppo-self-hosted.md)).
- **Perché no**: il Cancello deve sapere chi approva; n8n resta per orari e avvisi ([ricerca/25 §2, C27](../../ricerca/25-board-michele-e-delta.md)).

### Alternativa: azioni dai compiti programmati di Claude Team

- **Pro**: usa ciò che SerSan paga già ([ricerca/34, Proposta 3, In breve](../../ricerca/34-proposta-3-claude-team-e-mcp.md)).
- **Contro**: i compiti programmati includono di default tutti i connettori, scritture comprese, e così saltano il Cancello e il suo registro ([ricerca/35, giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)).
- **Perché no**: ciò che esce passa da un registro nostro; il connettore Microsoft 365 di Claude Team resta in sola lettura ([ricerca/29 §5.4](../../ricerca/29-conoscenza-task-e-documenti.md)).

### Alternativa: Cancello nella stessa macchina del motore

- **Pro**: una macchina virtuale in meno, come nella Proposta 3 ([ricerca/34, Proposta 3 §3.2](../../ricerca/34-proposta-3-claude-team-e-mcp.md)).
- **Contro**: un'iniezione riuscita nel motore arriva vicino ai segreti degli esecutori ([ricerca/35, giudizio CPTO §4.5](../../ricerca/35-giudizio-cpto.md)).
- **Perché no**: il Cancello resta sempre in una macchina separata ([ricerca/36 §4.1](../../ricerca/36-architettura-v2.md)).

## Conseguenze

### Positive

- Nessun agente ha in mano un bottone che invia, pubblica, paga o cancella ([proposta §9.2](../../PRESENTAZIONE-CEO.md)).
- Il Cancello non dipende dal motore: se Hermes ne prendesse il posto, resterebbe uguale ([proposta §5.7](../../PRESENTAZIONE-CEO.md)).

### Negative

- È codice nostro, da costruire per fasi e da mantenere ([proposta §5.4 e §15](../../PRESENTAZIONE-CEO.md)). In più chiede alle persone di decidere le carte in tempo: la verifica della settimana 8 le vuole decise entro 24 ore ([proposta §11](../../PRESENTAZIONE-CEO.md)).
- Servono due chiavi FIDO2 a persona, 232-464 € ([proposta §12.2](../../PRESENTAZIONE-CEO.md)); i telefoni che approvano entrano nel perimetro di Cyber Essentials, la certificazione di sicurezza inglese ([ricerca/36 §5.7](../../ricerca/36-architettura-v2.md)).

### Rischi

- **Codice su misura non ancora rivisto**: dieci scenari a ogni aggiornamento e revisione esterna di Cancello, motore e bot entro la settimana 21, circa 3.560-5.940 € ([proposta §13 e §14, decisione 5](../../PRESENTAZIONE-CEO.md)).
- **Bot di Teams senza Azure e identità di chi approva**: vanno provati nella fase 0; in ultima istanza si approva sulla pagina del Cancello ([proposta §11 e §13](../../PRESENTAZIONE-CEO.md); [ricerca/28 §2.3](../../ricerca/28-chat-di-gruppo-self-hosted.md)).

## Revisione del 10 novembre 2026

- Il Cancello resta **l'unico esecutore** delle azioni esterne, con la classificazione, l'esecuzione una volta sola e il registro.
- «Una carta per ogni azione esterna» lascia il posto ai **livelli da L0 a L3 per terna** (agente, tipo d'azione, classe di destinatari), con la finestra L2, la promozione confermata dal responsabile e la discesa automatica ([ADR-0020](0020-autonomia-a-livelli.md)).
- Escono le regole «Sempre» dopo 20 sì per destinazione: le sostituiscono le classi di destinatari calcolate dai dati ([ADR-0020](0020-autonomia-a-livelli.md)).
- Esce la chiave FIDO2 come secondo passo sulle carte; le chiavi restano per l'accesso al board con NetBird ([ADR-0023](0023-protezioni-essenziali.md)).
- La macchina separata per il Cancello non è più obbligatoria: può stare sulla stessa VM del motore, decide Michele ([ricerca/45 §3.1](../../ricerca/45-architettura-v3.md)).
- La revisione esterna diventa facoltativa: restano le prove a ogni modifica e la revisione di Mattia ([ADR-0023](0023-protezioni-essenziali.md)).
- Approvatore e sostituto per classe stanno nella configurazione ([ricerca/45 §6.2, AC-011](../../ricerca/45-architettura-v3.md)).

## Fonti

- [Proposta per i CEO, §2.4, §5.1, §5.4, §5.7, §9.1, §9.2, §11, §12.2, §13, §14, §15 e appendice A](../../PRESENTAZIONE-CEO.md)
- [ricerca/22, l'architettura del primo giro, §1](../../ricerca/22-architettura-scelta.md)
- [ricerca/25, il board di Michele, §2](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/28, chat di gruppo, §2.3 e §2.4](../../ricerca/28-chat-di-gruppo-self-hosted.md)
- [ricerca/29, conoscenza e documenti, §5.4](../../ricerca/29-conoscenza-task-e-documenti.md)
- [ricerca/34, Proposta 3, In breve e §3.2](../../ricerca/34-proposta-3-claude-team-e-mcp.md)
- [ricerca/35, giudizio CPTO §4.5](../../ricerca/35-giudizio-cpto.md) e [giudizio di sicurezza §2 e §3.2](../../ricerca/35-giudizio-sicurezza.md)
- [ricerca/36, architettura v2, §4.1, §5.7, §5.8 e §10](../../ricerca/36-architettura-v2.md)
