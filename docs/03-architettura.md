# Architettura di SerSan Agent OS

> **Aggiornato l'11 novembre 2026 all'architettura v3**, «Cancello a livelli e motore a due corsie» ([ricerca/45](../ricerca/45-architettura-v3.md); [ADR da 0020 a 0028](adr/README.md)). Rispetto alla versione 2 sono cambiate tre cose:
> - ogni azione ha un livello di autonomia, da L0 a L3, che il Cancello dà per agente, tipo d'azione e classe del destinatario. Non serve più una carta per ogni azione esterna ([ADR-0020](adr/0020-autonomia-a-livelli.md));
> - il motore ha due corsie nel nostro codice, catene a schema e sessioni dell'Agent SDK, con la sveglia, il registro degli eventi, il «decisore» e un router che sceglie fra sei destinazioni, compresa la corsia T sui posti Claude Team ([ADR-0021](adr/0021-motore-a-due-corsie.md); [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md); [ADR-0027](adr/0027-decisore.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md));
> - ogni agente dichiara il suo modello, anche open-weight, sempre dietro LiteLLM; bacheca e gruppi di chat degli agenti arrivano subito dopo la milestone 1; le protezioni scendono all'essenziale per un sistema chiuso ([ADR-0025](adr/0025-un-modello-per-agente.md); [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0023](adr/0023-protezioni-essenziali.md)).

Questo documento spiega come è fatto oggi SerSan Agent OS, il sistema di agenti AI di Sersan Limited che gira sul server aziendale. Copre i principi, lo schema a livelli, i componenti, il percorso di un'azione, la memoria, le reti, l'infrastruttura, la sicurezza e la conformità. È scritto per chi deve capire il progetto e per chi lo costruisce.

Il 10 novembre 2026 i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio. La proposta per i CEO resta la versione 2.1 dell'8 novembre 2026; dove la v3 la supera, qui la citazione della proposta resta come storia e accanto c'è la regola di oggi ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)).

**Fonti principali**

- La [decisione del gruppo di progetto e la sintesi del terzo giro](../ricerca/45-architettura-v3.md), 10 novembre 2026. È la fonte di verità dell'architettura: dove dice una cosa diversa, supera la proposta e l'architettura v2.
- Le [ADR](adr/README.md) da 0020 a 0028, e le sezioni di revisione del 10 e dell'11 novembre nelle altre ADR.
- Le ricerche del 10 e dell'11 novembre: la [casa dei testi](../ricerca/46-obsidian-come-casa-dei-testi.md) (46), i [modelli System One e il decisore](../ricerca/47-modelli-system-one.md) (47), i [modelli locali e la GPU](../ricerca/48-modelli-locali-e-gpu.md) (48), l'[instradamento a più motori](../ricerca/49-instradamento-a-piu-motori.md) (49).
- La [proposta per i CEO](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026, per costi, fasi e rischi che la v3 non cambia.
- L'[architettura v2](../ricerca/36-architettura-v2.md) del 25 ottobre 2026, con il dettaglio tecnico che la v3 tiene: VLAN (le reti separate del server), macchine, regole di rete, uscite.
- Le [risposte di Michele sull'hardware e la board del rack](../ricerca/37-hardware-risposte-michele.md), 8 novembre 2026.
- Il board di Michele Sanna, che vincola tutto il resto: il [board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md), l'[elenco delle VLAN](../allegati/infra/board-vlan.txt) e la [board del rack](../allegati/infra/Rack%20SerSan%2012U.md).
- Le [domande tecniche per Michele](../DOMANDE-PER-MICHELE.md), cioè le scelte sull'infrastruttura che restano sue.

**Come leggere**

- "Proposta" è `PRESENTAZIONE-CEO.md`. "Board" è l'infrastruttura disegnata da Michele.
- "Fase 0-6" sono le fasi del sistema di agenti; "F0-F5" sono le fasi del board. Le due roadmap corrono affiancate: l'infrastruttura la porta avanti Michele, il sistema di agenti si costruisce sopra ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Le "milestone" sono i passi dello sviluppo. Il codice, con PRD (il documento dei requisiti), spec e piani, sta in una repo privata dell'organizzazione, `sersan-agent-os-codice`. Le milestone del PRD sono sette e portano alla verifica della settimana 8, cioè alla fine della fase 1 (paragrafo 4.4). Questa numerazione sostituisce quella di [ricerca/45 §6.4 e §12](../ricerca/45-architettura-v3.md), perché la corsia S è stata anticipata. Le ADR e le ricerche scritte fino all'11 novembre contano ancora come ricerca/45, dove la milestone 2 era «prove con Microsoft e LiteLLM» e la 3 «telefono e posta»: per questo qui le milestone si chiamano anche per nome. Fanno eccezione la prova dei modelli locali e quella del decisore, con la seconda GPU che serve alla prima: il PRD le mette nella milestone 2, insieme al primo modello open-weight, come fa il [documento sullo sviluppo](06-sviluppo.md).
- Le VLAN 25, 32 e 35 e le macchine con un nome come `agenti-01` sono proposte da far approvare a Michele ([ricerca/36 §3](../ricerca/36-architettura-v2.md)).
- I prezzi sono IVA esclusa, salvo dove è scritto altro ([proposta §12.1](../PRESENTAZIONE-CEO.md)). La stima dei giorni di sviluppo è nella [proposta §15](../PRESENTAZIONE-CEO.md), rivista in [ricerca/45 §9.3](../ricerca/45-architettura-v3.md). Va rifatta: la milestone 1 comprende anche il decisore, il registro dei modelli e i testi letti da file, lavoro che la stima di [ricerca/45 §12.1](../ricerca/45-architettura-v3.md) non prevedeva ([ADR-0027](adr/0027-decisore.md); [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), revisione del 10 novembre).

---

## 1. I principi

### 1.1 Tutto in casa, dentro il board di Michele

Il sistema gira sul server di SerSan, dentro l'infrastruttura disegnata da Michele. In cloud restano solo i servizi verticali del board: Microsoft 365 con Teams, Claude Team, le API di Anthropic, Jira per to-do e progetti, Instantly per le campagne email, GitHub per il codice, Supabase per il database del prodotto, Vercel per i deploy, il DNS di Cloudflare e una piccola macchina Oracle a Milano per l'accesso da fuori. Il resto gira in casa, in reti separate. Fuori dal board restano poche eccezioni, da approvare una per una: la linea telefonica di Andrea, WhatsApp, Telegram, Slack per i clienti, l'invio della newsletter e alcuni strumenti commerciali (decisioni 8-10 e 15) ([proposta §5.1](../PRESENTAZIONE-CEO.md); [board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

Quando un pezzo non sta sul server, un abbonamento è ammesso. Managed Agents, il servizio in cui Anthropic fa girare gli agenti, è una riserva solo sui dati verdi, se il server è pieno o fermo ([ADR-0024](adr/0024-abbonamenti-come-riserva.md)). I posti Claude Team, oltre al lavoro delle persone, servono la corsia T per lo sviluppo di progetti in codice (paragrafo 3.1) ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

Azure esce: SersanOutreach, la nostra piattaforma outbound per LinkedIn ed email che diventa il CRM degli agenti, passa sul server nella fase F2 del board, "via da Azure", e la macchina Azure si spegne solo dopo una settimana di funzionamento stabile ([proposta §7.1 e §7.2](../PRESENTAZIONE-CEO.md)).

### 1.2 Un motore con due corsie, nel nostro codice

Il motore degli agenti lo scriviamo noi, in TypeScript ([ADR-0010](adr/0010-typescript-motore.md)). Ha due corsie, nello stesso codice ([ADR-0021](adr/0021-motore-a-due-corsie.md)):

- la **corsia N** fa girare catene a schema. Il codice sceglie i passi e i destinatari, presi dai dati; il modello scrive senza strumenti e restituisce campi a schema, cioè risposte con campi fissi, come un modulo. Raccoglie il lavoro ripetitivo: riassumere, classificare, estrarre, scrivere da un modello fisso;
- la **corsia S** fa girare sessioni dell'Agent SDK di Claude, cioè Claude Code usato come libreria, con gli strumenti. Serve alle figure che decidono il passo dopo, leggono il web o usano più sistemi. Ogni lavoro gira in un processo suo, con il profilo dell'agente e un tetto di spesa.

La milestone 1 usa solo la corsia N; la corsia S si costruisce subito dopo, senza aspettare la fase 2 ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md)). Un router nel motore sceglie dove fare ogni lavoro: una regola nel codice, una catena N su un modello in casa o su Claude, una sessione S, la corsia T sui posti Claude Team oppure una persona ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

Il motore non duplica ciò che il board ha già: i budget li tiene LiteLLM (paragrafo 1.4); la memoria sta in PostgreSQL, Qdrant e nella casa dei testi, cioè il database, la memoria che cerca per significato e il posto delle regole e dei processi ([proposta §5.3](../PRESENTAZIONE-CEO.md); [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md)). Gli orari invece stanno nel motore. La proposta li affidava a n8n, il programma delle automazioni del board ([proposta §5.3](../PRESENTAZIONE-CEO.md)); oggi la sveglia è una tabella degli orari nel motore, con un unico ingresso per gli eventi, `POST /eventi`. n8n diventa facoltativo: resta nel board per i collegamenti che servono, ma il sistema non ne dipende ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).

### 1.3 Il Cancello: gli agenti propongono, il codice esegue

Il Cancello è l'unico programma che può mandare una mail, scrivere a un cliente, toccare il CRM o telefonare. Nella proposta ogni azione verso l'esterno aspettava il sì di una persona, una volta sola, oppure una regola "Sempre" approvata ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Oggi il Cancello dà a ogni azione un livello di autonomia, da L0 a L3 ([ADR-0020](adr/0020-autonomia-a-livelli.md)):

- **L0 a mano**: l'agente prepara, una persona esegue;
- **L1 carta**: l'agente propone e una persona approva ogni singola azione su una carta, cioè una richiesta di approvazione con il testo esatto;
- **L2 finestra**: l'azione parte da sola dopo una finestra in cui una persona può fermarla;
- **L3 autonomo**: l'azione parte subito, dentro regole, tetti e registro; le persone vedono dopo e possono revocare.

In ogni caso il Cancello esegue una volta sola e registra tutto ([ADR-0023](adr/0023-protezioni-essenziali.md)).

La macchina degli agenti non ha accesso a internet e parla solo con LiteLLM, con i server MCP e con il Cancello: un agente non ha una strada per mandare qualcosa fuori se non passando dal Cancello ([proposta §5.4](../PRESENTAZIONE-CEO.md)). MCP (Model Context Protocol) è la presa standard con cui un agente usa uno strumento ([proposta §7.3](../PRESENTAZIONE-CEO.md)). Il Cancello può stare sulla stessa macchina virtuale del motore: lo decide Michele ([ADR-0023](adr/0023-protezioni-essenziali.md)).

Le persone approvano dal telefono, in Teams. La prima versione del posto dove si approva è la Sala di controllo della milestone 1: una pagina web locale, usabile anche dal telefono sulla rete dell'ufficio, dove si vedono e si decidono carte, finestre, promozioni, «sbagliato», «Annulla», «Rettifica», tetti e stop di emergenza. Fa da Porta di prova finché non c'è quella di Teams, e un comando da terminale fa le stesse cose.

### 1.4 Un modello per agente, LiteLLM tiene i conti

Nella proposta gli agenti ragionavano tutti con Claude via API: Haiku per i lavori semplici, Sonnet per quasi tutto, Opus per offerte e analisi ([proposta §5.1](../PRESENTAZIONE-CEO.md)). Oggi ogni agente dichiara nel registro il suo modello, fra tre tipi: Claude via API; un modello open-weight, cioè con i pesi pubblici, servito sul nostro server; un modello open-weight di un fornitore, via API. I modelli locali entrano prima nella corsia N, dove non servono strumenti. Nelle sessioni S resta Claude finché una prova non dimostra che un modello locale regge. I fornitori terzi ricevono solo dati verdi e gialli ([ADR-0025](adr/0025-un-modello-per-agente.md)).

Un registro dei modelli, il file `config/modelli.yaml`, dice per ogni modello il fornitore, i costi, le capacità (testo, immagini, audio) e i colori dei dati che può ricevere. La scelta la fa il codice: se il modello dell'agente non ha la capacità che serve, il lavoro si ferma e l'evento va a una persona. Un dato rosso non esce mai dal server per «avere un modello che vede» ([ADR-0025](adr/0025-un-modello-per-agente.md), aggiornamento del 10 novembre).

Ogni chiamata a un modello passa da LiteLLM, la porta verso i modelli prevista dal board, che custodisce le chiavi e dà a ogni agente, squadra e persona il suo budget ([proposta §5.1](../PRESENTAZIONE-CEO.md); [ADR-0004](adr/0004-litellm-banca-token.md)). Il motore non chiama mai un modello direttamente ([ADR-0025](adr/0025-un-modello-per-agente.md)). All'80% del budget arriva un avviso, al 100% il lavoro si ferma ([proposta §9.2](../PRESENTAZIONE-CEO.md)). Fa eccezione la corsia T: le sessioni sui posti Team consumano l'uso del posto e non passano da LiteLLM, e il loro conto lo tiene il motore, posto per posto ([ADR-0004](adr/0004-litellm-banca-token.md), revisione dell'11 novembre).

### 1.5 I dati hanno tre colori

Una regola semplice, scritta nel codice, decide cosa può uscire dal server e verso chi ([proposta §5.6](../PRESENTAZIONE-CEO.md)).

| Colore | Cosa | Dove può andare |
|---|---|---|
| **Verde** | Pubblico o interno non personale | Qualunque fornitore ammesso, anche Claude Team |
| **Giallo** | Contatti di lavoro, campi del CRM, riassunti | Solo i fornitori del board e quelli che Michele ammette, con contratto commerciale e DPA (l'accordo sul trattamento dei dati) |
| **Rosso** | Audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone, finanza | Resta sul server, oppure va all'API di Anthropic dopo aver oscurato in locale i dati non necessari |

Il colore si calcola prima di chiamare un modello; se non è noto vale rosso ([ADR-0027](adr/0027-decisore.md)). I fornitori di modelli open-weight ricevono al massimo verde e giallo ([ADR-0025](adr/0025-un-modello-per-agente.md)). Jev, il modello del decisore (paragrafo 1.10), riceve il verde, e il giallo solo quando Michele ammette il suo fornitore ([ADR-0027](adr/0027-decisore.md)). La corsia T non riceve mai il rosso, neanche oscurato ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

Con tutto sul server l'audio delle call e la voce di Andrea non passano più da fornitori negli USA: l'audio resta in casa e si trascrive in casa. Claude Team riceve verde e giallo, e il rosso solo oscurato, finché il parere legale e la valutazione d'impatto non decidono diversamente, entro la settimana 3 ([proposta §5.6](../PRESENTAZIONE-CEO.md)).

### 1.6 Ogni pezzo si può cambiare

Il motore parla con gli strumenti solo via MCP, con i modelli solo via LiteLLM e con l'esterno solo via Cancello ([ricerca/36 §12](../ricerca/36-architettura-v2.md)). Per questo Hermes, la piattaforma di agenti open source valutata come alternativa, resta un'uscita già prezzata e un pilota in laboratorio: se il motore non regge le verifiche delle settimane 8 e 21, si prova Hermes sullo stesso banco di prova e si decide sui numeri, mentre Cancello, memoria, server MCP, bot e skill restano uguali. Hermes diventa l'orchestratore solo se chiude i suoi problemi di sicurezza ([proposta §5.7](../PRESENTAZIONE-CEO.md); [ADR-0012](adr/0012-hermes-uscita.md)). Allo stesso modo un modello o un motore del decisore si cambia nella configurazione, senza toccare catene e Cancello ([ADR-0025](adr/0025-un-modello-per-agente.md); [ADR-0027](adr/0027-decisore.md)).

La chat ha due case. Le persone lavorano in Teams, con le approvazioni sul telefono. Gli agenti si passano il lavoro su una bacheca nostra, che si vede in gruppi di chat: uno per squadra, uno per cliente e uno comune, «Agenti». All'inizio i gruppi stanno in Teams; Buzz, la chat open source fatta per persone e agenti, si collega alla stessa bacheca e si prova subito dopo la milestone 1, non nella fase 4: se regge, diventa la casa degli agenti ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). Telegram, Slack e WhatsApp si collegano dalla fase 3 ([proposta §4.11 e §11](../PRESENTAZIONE-CEO.md)).

### 1.7 Autonomia per classe, dentro limiti fissi

L'autonomia si dà per terna: agente, tipo d'azione, classe del destinatario. Ogni classe ha un livello di partenza e un tetto che non si supera mai. Il livello sale con la promozione confermata dal responsabile della squadra e scende da solo al primo segnale negativo ([ADR-0020](adr/0020-autonomia-a-livelli.md)). Partenze, tetti e motivi stanno in un file di configurazione in git, `config/livelli.yaml`; il livello attuale di ogni terna sta nel database del Cancello (paragrafo 4.1).

Alcuni limiti invece sono fissi e stanno nel codice, non nella configurazione: gli agenti non cancellano e non toccano credenziali; i pagamenti non partono mai da soli, li fa una persona; un tipo d'azione sconosciuto è negato. Questi limiti valgono anche per chi chiama direttamente il Cancello ([ADR-0023](adr/0023-protezioni-essenziali.md)).

### 1.8 Il codice sceglie i destinatari, mai un modello

Nella corsia N i destinatari vengono dai dati: calendario, partecipanti registrati, CRM. La classe del destinatario la calcola il Cancello dagli stessi dati, mai da ciò che dichiara l'agente o dal testo di una mail ([ADR-0020](adr/0020-autonomia-a-livelli.md); [ADR-0021](adr/0021-motore-a-due-corsie.md)). È la difesa più economica contro le iniezioni di prompt, cioè le istruzioni nascoste nel testo di terzi, perché il modello non sceglie né chi riceve né cosa si fa ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md)).

Anche lo smistamento lo fa il codice, sui metadati. I modelli che vedono e ascoltano fanno da occhi e orecchie, non da orchestratore; l'unico smistatore libero è il Capo di gabinetto, nella corsia S, su Claude ([ADR-0025](adr/0025-un-modello-per-agente.md); [ricerca/48 §3.2](../ricerca/48-modelli-locali-e-gpu.md)).

### 1.9 Ogni agente legge le regole "Come lavoro"

Ogni catena N e ogni sessione S carica le regole "Come lavoro" della persona per cui lavora, cioè le regole di lavoro che ciascuno scrive per sé. È un'azione interna, a L3. Nella trascrizione di riferimento gli agenti leggono queste regole prima di ogni compito ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md); [ADR-0021](adr/0021-motore-a-due-corsie.md)).

Nella milestone 1 le regole stanno in file Markdown e YAML nella repo del codice, letti attraverso un'interfaccia unica. La loro casa definitiva si decide prima della fase 2 (paragrafo 5.1); cambiarla vuol dire cambiare l'interfaccia, non le catene ([ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), revisione del 10 novembre).

### 1.10 Un dubbio rende il sistema più prudente

Molte decisioni piccole le prende il «decisore»: un'interfaccia del nostro codice che fa a un modello domande chiuse (sì o no, una scelta, un punteggio) e riceve una probabilità per ogni risposta. Le soglie stanno in un file, `config/decisore.yaml`. Una risposta sotto la soglia vale «dubbio»; anche un errore, un ritardo o un tetto di spesa raggiunto valgono un dubbio ([ADR-0027](adr/0027-decisore.md)).

Un dubbio può solo rendere il sistema più prudente: una carta a una persona per quella volta, il colore rosso, una corsia più capace. Il decisore non sceglie mai un destinatario esterno e non alza mai un livello. Un dubbio non abbassa la terna: la terna scende solo per i segnali del paragrafo 4.2 ([ADR-0027](adr/0027-decisore.md)). E un dubbio non manda mai un lavoro nella corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

---

## 2. Lo schema a livelli

Lo schema è quello della [proposta §5.2](../PRESENTAZIONE-CEO.md), aggiornato alla v3. Si legge dall'alto: le persone, poi il server con i suoi livelli, poi ciò che resta fuori dal server.

```
PERSONE (4)   Teams e Outlook (M365, accesso con MFA e chiave FIDO2), dal PC e dal telefono
              Sala di controllo: carte, finestre, promozioni, tetti, stop
              Claude Team: chat, skill, progetti, ricerca nella memoria; corsia T per lo sviluppo
              Telegram (avvisi) · WhatsApp (clienti) · Slack (clienti) · Buzz (in prova)

===== SERVER DL380 · Proxmox · reti separate dietro OPNsense · accesso da NetBird =====
INGRESSO   Traefik, raggiunto da Pangolin sulla macchina Oracle: bot di Teams,
           webhook verso POST /eventi, ricerca nella memoria per Claude Team,
           pagine di firma
APP        CANCELLO A LIVELLI + PORTA CHAT (bot di Teams, Telegram, Slack, WhatsApp)
           server MCP: memoria, bacheca, testi, Jira, posta in lettura, SersanOutreach
           LiteLLM (porta dei modelli, budget) · n8n (facoltativo) · BookStack o testi in git
           SersanOutreach · Postiz · listmonk · DocuSeal · fatturazione · Andrea (Pipecat)
AGENTI     MOTORE: sveglia ed eventi · router · decisore · corsia N · corsia S
           nessun accesso a internet
DATI       PostgreSQL 16 · Qdrant · Infisical · Vaultwarden · archivio dei file
VOCE       Asterisk: il centralino di Andrea, con una linea telefonica italiana
RIUNIONI   Vexa: il bot nelle call dei clienti (Teams di altri, Meet, Zoom)
AI         RTX 4000 + seconda GPU: embedding, ricerca, trascrizione, modelli open-weight
MONITOR    Prometheus · Grafana · Loki · Uptime Kuma · Wazuh · NetBox
LAB        banco di prova degli agenti · Buzz · Paperclip · Hermes
=======================================================================================
CLOUD DEL BOARD  M365 ed Entra · Claude Team · API Anthropic via LiteLLM · Jira
                 Instantly · GitHub · Supabase · Vercel · Cloudflare (DNS)
                 Oracle Cloud a Milano: NetBird, Pangolin, monitoraggio
RISERVA          Managed Agents di Anthropic, solo su dati verdi
ESTERNI          linea telefonica italiana · WhatsApp (Meta) · Telegram · Slack
                 invio della newsletter · strumenti commerciali che restano
                 Jev (TypeSafe) via LiteLLM · fornitori di modelli open-weight, se servono
BACKUP 3-2-1     Proxmox Backup Server in sede, ogni notte copia cifrata a casa
                 di Michele (Terra Noa) · S3 fuori sede facoltativo
```

### 2.1 I livelli, uno per uno

**Persone.** Sono quattro: Alessandro, Michele, Alberto e Mattia. Lavorano da Teams e Outlook, dal PC e dal telefono. L'accesso passa da Entra ID, l'identità di Microsoft, con MFA (un secondo fattore oltre alla password) e con la chiave FIDO2, una chiavetta fisica che conferma l'identità. Claude Team è la finestra di lavoro di ognuno: chat, skill, progetti per squadra e la ricerca nella memoria aziendale, con i propri permessi. Telegram riceve gli avvisi, WhatsApp e Slack servono soprattutto verso i clienti, Buzz è in prova ([proposta §3, §4.11 e §5.2](../PRESENTAZIONE-CEO.md)). Dalla milestone 1 c'è anche la Sala di controllo, la pagina web dove si vedono e si decidono carte, finestre, promozioni e stop, anche dal telefono sulla rete dell'ufficio. Sui posti Claude Team di chi segue lo sviluppo gira la corsia T ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

**Il server.** È un HPE ProLiant DL380 Gen10 con Proxmox, il sistema che fa girare le macchine virtuali (VM) e i container leggeri (LXC). I servizi stanno in reti separate, le VLAN (reti logiche distinte sullo stesso cablaggio), dietro OPNsense, il firewall open source. Da fuori si entra solo con NetBird, una rete privata cifrata che chiede un'identità verificata ([proposta §5.2 e §6.1](../PRESENTAZIONE-CEO.md)). Fra le VLAN tutto è vietato salvo ciò che è permesso, e il routing lo fa OPNsense ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

**Ingresso.** Traefik riceve le richieste HTTPS e le smista ai servizi interni. Da internet ci si arriva solo attraverso Pangolin, un tunnel che gira sulla macchina Oracle e pubblica pochi servizi senza aprire porte in ufficio. Passano di qui i messaggi dei bot di Teams, i webhook (le chiamate che un servizio esterno fa quando succede qualcosa), la ricerca nella memoria per Claude Team e le pagine di firma dei contratti ([proposta §5.2](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.4](../ricerca/36-architettura-v2.md)). I webhook arrivano a `POST /eventi`, l'ingresso del motore, con un token per ogni mittente ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).

**App.** È il livello più affollato ([proposta §5.2](../PRESENTAZIONE-CEO.md)):

- il Cancello a livelli con la Porta chat, cioè i bot di Teams, Telegram, Slack e WhatsApp;
- i server MCP che danno agli agenti memoria, bacheca, testi, Jira, posta in lettura e SersanOutreach;
- LiteLLM, la porta di tutti i modelli, che tiene i budget; n8n, facoltativo, per i collegamenti del board che servono ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md));
- la casa dei testi con regole e processi, BookStack oppure una cartella di file Markdown in git, da decidere prima della fase 2 ([ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md)), e SersanOutreach, il CRM;
- i servizi per marketing, amministrazione e voce: Postiz per i post, listmonk per la newsletter, DocuSeal per la firma elettronica, la fatturazione e Pipecat, il programma che fa parlare Andrea.

**Agenti.** Il motore: la sveglia con il registro degli eventi, il router, il decisore, la corsia N e la corsia S. Nessun accesso a internet ([ADR-0021](adr/0021-motore-a-due-corsie.md); [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

**Dati.** PostgreSQL 16 per i dati strutturati, Qdrant per la memoria vettoriale (il database che cerca per significato), Infisical per i segreti delle applicazioni, Vaultwarden per le password delle persone, e l'archivio dei file ([proposta §5.2](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1](../ricerca/36-architettura-v2.md)). Questa rete non ha internet ([elenco delle VLAN](../allegati/infra/board-vlan.txt)).

**Voce.** Asterisk, il centralino open source di Andrea, collegato a una linea telefonica italiana ([proposta §5.2](../PRESENTAZIONE-CEO.md)).

**Riunioni.** Vexa, il bot che entra nelle call dei clienti su Teams di altre aziende, Meet e Zoom. Le call di SerSan in Teams le trascrive già Microsoft, e il sistema legge quella trascrizione ([proposta §4.2 e §5.2](../PRESENTAZIONE-CEO.md)).

**AI.** La GPU Quadro RTX 4000 e la seconda GPU. Fanno i lavori che conviene tenere in casa: gli embedding (il testo trasformato in numeri per cercarlo per significato) e la ricerca nella memoria, il modello piccolo Qwen3-4B che prepara i documenti, la trascrizione delle call e, con la seconda GPU, la voce di Andrea ([proposta §6.2](../PRESENTAZIONE-CEO.md)). La proposta diceva che gli agenti non usano la GPU. Oggi la GPU serve anche i modelli open-weight della corsia N e del decisore in casa, per esempio un modello da 9 miliardi di parametri che vede le immagini, per i dati rossi da guardare; la corsia S resta su Claude ([ADR-0025](adr/0025-un-modello-per-agente.md); [ricerca/48 §3.2](../ricerca/48-modelli-locali-e-gpu.md)). La seconda GPU è proposta a Michele per la milestone 2 (paragrafo 7.4).

**Monitor.** Prometheus raccoglie le metriche, Grafana le mostra nei cruscotti, Loki tiene i log, Uptime Kuma controlla che i servizi rispondano, Wazuh cerca vulnerabilità e segnala allarmi di sicurezza, NetBox è l'inventario di indirizzi e apparati. Questa rete legge da tutte e non ha internet ([proposta §5.2](../PRESENTAZIONE-CEO.md); [elenco delle VLAN](../allegati/infra/board-vlan.txt)).

**Lab.** Il banco di prova degli agenti, dove gira il pilota, e i servizi in prova: Buzz, provato subito dopo la milestone 1, Paperclip e Hermes ([proposta §5.2 e §11](../PRESENTAZIONE-CEO.md); [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ADR-0012](adr/0012-hermes-uscita.md)).

**Cloud del board.** M365 con Entra, Claude Team, l'API di Anthropic (raggiunta solo attraverso LiteLLM), Jira, Instantly, GitHub, Supabase, Vercel, Cloudflare per il DNS, e la macchina Oracle Cloud a Milano per NetBird, Pangolin e il monitoraggio da fuori ([proposta §5.2](../PRESENTAZIONE-CEO.md)).

**Riserva.** Managed Agents di Anthropic, solo sui dati verdi e solo se il server è pieno o fermo ([ADR-0024](adr/0024-abbonamenti-come-riserva.md)).

**Esterni.** I servizi fuori dal board, ognuno un'eccezione da approvare: la linea telefonica italiana di Andrea, WhatsApp di Meta, Telegram, Slack, l'invio della newsletter e gli strumenti commerciali che restano ([proposta §5.1 e §5.2](../PRESENTAZIONE-CEO.md)). Con la v3 si aggiungono Jev, il modello del decisore di TypeSafe, chiamato via LiteLLM, e i fornitori di modelli open-weight come OpenRouter, solo per un modello che Claude non ha e che noi non ospitiamo ([ADR-0027](adr/0027-decisore.md); [ADR-0025](adr/0025-un-modello-per-agente.md)).

**Backup 3-2-1.** Tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio: un Proxmox Backup Server in sede e, ogni notte, una copia cifrata a casa di Michele, a Terra Noa. Uno spazio S3 fuori sede (un archivio di file in cloud) è facoltativo ([proposta §5.2 e §6.1](../PRESENTAZIONE-CEO.md)). Il dettaglio è nel paragrafo 7.6.

### 2.2 Dove sta ogni livello

| Livello | VLAN | Stato | Macchine e servizi |
|---|---|---|---|
| Ingresso | 20 EDGE | board | Traefik; Pangolin e la gestione di NetBird stanno sulla macchina Oracle |
| App | 30 APPS | board | `cancello-01` (VM: Cancello e Porta; può stare su `agenti-01`, decide Michele), `mcp-01` (LXC: server MCP), n8n (facoltativo), LiteLLM, MCP RAG, BookStack, Open WebUI, Firecrawl, SersanOutreach, Postiz, listmonk, DocuSeal, fatturazione, `andrea-01` (LXC: Pipecat) |
| Agenti | 32 AGENTI | proposta | `agenti-01` (VM con Docker: il motore, con le corsie N e S). In alternativa resta nella 30, con il firewall di Proxmox per ogni VM |
| Dati | 40 DATA | board | PostgreSQL 16, Qdrant, MariaDB (nuova, se resta BookStack), Infisical, Vaultwarden, archivio S3 al posto di MinIO |
| Voce | 25 VOCE | proposta | `voce-01` (LXC: Asterisk) |
| Riunioni | 35 MEET | proposta | `meet-01` (VM: Vexa) |
| AI | 80 AI | board | `ai-gpu-01` (LXC): Qwen3-4B, embedding e reranker, Docling, trascrizione; i modelli open-weight da provare |
| Monitor | 70 OBSRV | board | Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox |
| Lab | 90 LAB | board | `stage-agenti` (VM, proposta: il banco di prova), Experimental-2 (la sandbox Linux del laboratorio) con Buzz, Paperclip e Hermes |

Fonti: [ricerca/36 §3 e §4.1](../ricerca/36-architettura-v2.md); [elenco delle VLAN](../allegati/infra/board-vlan.txt); per la macchina Oracle, [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md); per la v3, [ADR-0023](adr/0023-protezioni-essenziali.md), [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md), [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md) e [ricerca/48 §4.1](../ricerca/48-modelli-locali-e-gpu.md).

Nella board del rack il trunk verso il server porta anche le VLAN 35 e 85, che l'elenco delle VLAN del board non descrive. A Michele chiediamo se la 35 è la MEET proposta e a cosa serve la 85; se nessuna delle due è per gli agenti, il motore va in una VLAN 32 nuova o nella 30 ([domande per Michele, n. 3](../DOMANDE-PER-MICHELE.md)).

---

## 3. I componenti

Lo stato di ogni componente riprende, semplificata, la legenda del piano tecnico ([ricerca/36 §4.1](../ricerca/36-architettura-v2.md)):

- **nostro**: codice che scriviamo noi;
- **board**: già previsto da Michele, da configurare per gli agenti;
- **nuovo**: servizio open source da aggiungere al board;
- **cloud**: servizio del board che resta in cloud;
- **esterno**: fuori dal board, da ammettere come eccezione.

### 3.1 Il cuore, scritto da noi

Tutto il codice nostro sta nella repo privata `sersan-agent-os-codice` ([ADR-0021](adr/0021-motore-a-due-corsie.md)).

| Componente | Ruolo | Dove gira | Quando |
|---|---|---|---|
| **Motore, corsia N** | Catene a schema: il codice sceglie passi e destinatari, il modello scrive senza strumenti. Ogni passo ha una chiave d'idempotenza, così un passo ripetuto non produce un secondo effetto. Chiama i modelli senza passare da Claude Code | prima le macchine di sviluppo, poi il banco di prova, poi `agenti-01`, VLAN 32 (proposta) | Milestone 1; sul banco nella fase 1; sul server nella fase 2 |
| **Motore, corsia S** | Sessioni dell'Agent SDK con strumenti: un solo runner, con al massimo 6 sessioni insieme, e il ponte `propose_action` verso il Cancello | `agenti-01` | Subito dopo la milestone 1 (milestone 2) |
| **Sveglia e registro degli eventi** | La tabella degli orari e l'unico ingresso `POST /eventi`. Il registro tiene una chiave per evento e lo stato «ricevuto / fatto / fallito»; un compito fisso rimette in coda ciò che resta fermo | motore e PostgreSQL | Registro dalla milestone 1; orari con il debrief dei tre agenti (milestone 6) |
| **Lettore delta di Graph** | Legge le trascrizioni di Teams ogni 5 minuti. Il token delta, il segno di dove era arrivata la lettura, avanza solo dopo che l'evento è registrato | motore | Milestone 5, «dalla call al riassunto» |
| **Router** | Sceglie la destinazione di ogni lavoro fra sei, con regole fisse, decisore e la tabella `config/instradamento.yaml` | motore | Dopo la milestone 1, con le prove di LiteLLM |
| **Decisore** | Domande chiuse a un modello, probabilità in uscita, soglie in `config/decisore.yaml`; ogni chiamata lascia una riga | motore | Milestone 1, con un decisore a copione e uno su un modello a schema; la prova dei motori, Jev compreso, dopo |
| **Registro dei modelli** | `config/modelli.yaml`: fornitore, costi, capacità, colori ammessi. L'elenco dei modelli di LiteLLM si genera da qui | git | Milestone 1 |
| **Cancello a livelli** | L'unico esecutore delle azioni esterne: calcola la classe del destinatario, dà il livello alla terna, crea carte e finestre, controlla il contenuto, applica tetti e lista di soppressione, esegue una volta sola, registra, fa «Annulla» e «Rettifica», ferma tutto con lo stop di emergenza | `cancello-01`, VLAN 30, oppure la stessa VM del motore: decide Michele | Milestone 1; sul banco nella fase 1; sul server nella fase 2 |
| **Sala di controllo** | La pagina web locale, usabile anche dal telefono sulla rete dell'ufficio, che fa da Porta di prova: mostra e decide carte, finestre, promozioni, «sbagliato», «Annulla», «Rettifica», tetti e stop. Un comando da terminale fa le stesse cose | con il Cancello | Milestone 1 |
| **Porta chat** | I bot: uno per il Cancello e nove di squadra in Teams, con «Ferma», «Invia ora», promozioni e «sbagliato»; poi Telegram, Slack e WhatsApp con lo stesso codice (Chat SDK e Teams SDK) | con il Cancello | Teams con le prove di Microsoft (milestone 3) e il telefono (milestone 4); nove bot nella fase 2; gli altri canali nella fase 3 |
| **Adattatore della corsia T** | Avvia i compiti sui posti Team dall'outbox del Cancello, legge le consegne su GitHub, tiene il conto per posto | motore e Cancello | Prova dopo la milestone 1; lavori veri dopo la prova e la conferma scritta di Anthropic |
| **Server MCP** | Le prese degli agenti: memoria su PostgreSQL, bacheca, testi in lettura, Jira, posta e calendario in lettura, Firecrawl, SersanOutreach | `mcp-01`, VLAN 30 | Fasi 2-3 |
| **Bacheca e gruppi** | Compiti e passaggi fra agenti, con il freno; gruppi di chat per squadra, per cliente e «Agenti» | tabelle in PostgreSQL, con un suo server MCP | Subito dopo la milestone 1, con la corsia S |
| **Registro degli agenti** | Una riga per agente: nome, squadra, responsabile, modello, corsie ammesse, classi ammesse, cosa può toccare, tetto di spesa, costo del mese. È l'organigramma | file in git, con una pagina nella casa dei testi e una vista in Grafana | Milestone 1 per le catene; completo con la corsia S |
| **Banco di prova** | Il pilota della fase 1 (settimane 5-8), finché il motore non passa sul server nella fase 2; poi le prove di ogni aggiornamento. Ha un suo PostgreSQL e una chiave API limitata | `stage-agenti`, VLAN 90 LAB | Fase 1 |

Fonti: [proposta §4.12, §5.3, §5.4 e §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1, §5.3 e §7.3](../ricerca/36-architettura-v2.md); [ricerca/45 §3.1 e §6.1](../ricerca/45-architettura-v3.md); [ADR-0021](adr/0021-motore-a-due-corsie.md), [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md), [ADR-0023](adr/0023-protezioni-essenziali.md), [ADR-0025](adr/0025-un-modello-per-agente.md), [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md), [ADR-0027](adr/0027-decisore.md) e [ADR-0028](adr/0028-instradamento-a-piu-motori.md). Le milestone sono quelle del PRD; per il router e la corsia T l'ADR-0028 dice «milestone 2» e «milestone 3» con la numerazione di ricerca/45, cioè le prove con Microsoft e LiteLLM e il telefono con la posta.

**Il motore.** È un servizio in TypeScript, confermato per tutte e due le corsie e per il Cancello; la conferma di Mattia non blocca ([ADR-0010](adr/0010-typescript-motore.md), revisione del 10 novembre). Funziona così ([ricerca/36 §2.1, §4.1, §5.1, §5.7 e §6](../ricerca/36-architettura-v2.md); [ricerca/45 §6.1](../ricerca/45-architettura-v3.md)):

- un lavoro entra in una coda in PostgreSQL con il profilo, la persona per cui si lavora, il tetto in dollari e la scadenza. Lo prende un solo runner, la parte del motore che fa girare i lavori;
- nella corsia N il runner esegue la catena passo per passo. Il testo di terzi entra solo come campi, e il modello riceve solo ciò che il passo gli passa;
- nella corsia S il runner avvia per ogni lavoro un processo dell'SDK con il profilo: le istruzioni della squadra (`CLAUDE.md`), le skill ammesse, un elenco chiuso di strumenti MCP, la chiave di LiteLLM, il tetto di turni (`maxTurns`) e di spesa (`maxBudgetUsd`);
- nella corsia S la modalità è `dontAsk`: ciò che non è nell'elenco è negato, senza domande;
- ogni famiglia di agenti ha cartella, configurazione e chiave sue. Con `settingSources: []`, `CLAUDE_CONFIG_DIR` e `cwd` per famiglia un agente non legge le impostazioni di un altro; l'opzione `env` sostituisce l'ambiente, quindi il processo non vede le chiavi del motore;
- gli agenti con gli stessi permessi e gli stessi segreti condividono un container Docker ("container di famiglia");
- le sessioni S si salvano in PostgreSQL attraverso il `SessionStore` dell'SDK, così un lavoro in attesa riparte dopo ore;
- metriche e log vanno a Prometheus e Loki con OpenTelemetry, lo standard aperto per la telemetria;
- il traffico non essenziale verso Anthropic è spento (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`) e non c'è WebFetch diretto: il web passa da Firecrawl.

Le opzioni della corsia S sono semplice configurazione: la milestone 1 non le usa ([ricerca/45 §6.1](../ricerca/45-architettura-v3.md)). Come punto di partenza ogni sessione S ha 1 GiB di RAM, 1 CPU e 5 GiB di disco; il motore usa 12 GB con 6 sessioni insieme, 16 con 8-10 e 20 con 12-16 ([ricerca/36 §4.1](../ricerca/36-architettura-v2.md)). La corsia N non pesa sulla RAM, perché non c'è un processo di Claude Code per ogni lavoro ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md)). La versione dell'SDK è fissata e si aggiorna ogni due settimane, dopo dieci scenari di prova, entro 14 giorni dall'uscita ([proposta §13](../PRESENTAZIONE-CEO.md)). Al 25 ottobre 2026 era la 0.3.310 per TypeScript, con Claude Code 2.1.310 ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)). La corsia N non dipende dagli aggiornamenti dell'SDK ([ADR-0021](adr/0021-motore-a-due-corsie.md)).

**Le corsie, nessun agente declassato.** La corsia dice come un agente lavora in quel momento, non quanto vale ([ricerca/36 §5.2](../ricerca/36-architettura-v2.md); [ADR-0021](adr/0021-motore-a-due-corsie.md)):

- **corsia N, catena a schema**: riassumere, classificare, estrarre, scrivere da un modello fisso. Contro le iniezioni di istruzioni nel testo è il disegno più robusto. Costa poco: Haiku 5.5 costa 0,10 $ per milione di token in ingresso e 0,50 $ in uscita ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md)). Sono circa 30-35 figure [stima], fra cui Post-call, Analista chiamate, Report del mattino, Smistatore posta, la squadra Memoria, Analista metriche, fatture e solleciti, Agente bandi ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md));
- **corsia S, sessione con strumenti**: lavori a più passi, come brief, offerte, slide, il Capo di gabinetto, il Mappatore, il Project manager. Sono circa 15-20 figure [stima] ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md));
- **corsia T, sessione di Claude Code su un posto Claude Team**: solo lo sviluppo di progetti in codice e i lavori lunghi di quattro agenti, con la consegna come pull request ([ADR-0028](adr/0028-instradamento-a-piu-motori.md));
- **servizio**: un componente che fa il lavoro da sé, come la pipeline della memoria, Vexa, il centralino o il Cancello ([ricerca/36 §5.2](../ricerca/36-architettura-v2.md)).

Tutte le 57 figure sono profili del registro. Anche quelle che una persona potrebbe usare a mano, come Copywriter, Agente video, Agente grafiche, Pubblicatore, Sviluppatori, Intervistatore e Assistente personale, restano agenti che ricevono lavoro dalla bacheca; in più le loro skill sono anche in Claude Team, così una persona le può usare a mano. Per ogni profilo il registro scrive la corsia, se legge testo di terzi e quali strumenti ha ([ricerca/36 §5.2](../ricerca/36-architettura-v2.md)). Passare dalla corsia N alla S è una promozione dentro lo stesso codice, non una riscrittura ([ADR-0021](adr/0021-motore-a-due-corsie.md)).

**Il router e il decisore.** Per ogni lavoro il router sceglie la destinazione in tre passi ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §2](../ricerca/49-instradamento-a-piu-motori.md)):

1. **regole fisse nel codice**, senza modelli: stop di emergenza, tipo di evento già noto (per esempio la trascrizione pronta va alla catena «post-call»), corsie ammesse per l'agente, colore dei dati, capacità del modello, tetti di spesa, conto del posto per la corsia T, classi fisse del Cancello;
2. **il decisore**, solo per gli eventi a testo libero, con sei domande chiuse: che lavoro è, quanto è complesso, se servono strumenti, se tocca impegni, se è sviluppo o un lavoro lungo, se è urgente;
3. **una tabella** in git, `config/instradamento.yaml`, con le soglie di partenza.

Le destinazioni sono sei: una regola nel codice; una catena N su un modello open-weight sul nostro server; una catena N su Claude via API; una sessione S con la chiave API; la corsia T; una persona. Nel dubbio si sale di un gradino e non si scende mai: la scala è regola, catena in casa, catena su Claude, sessione S, persona; per il rosso è regola, catena in casa, persona ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). La catena in casa e quella su Claude sono la stessa catena: le distingue il modello dell'agente nel registro ([ADR-0025](adr/0025-un-modello-per-agente.md), revisione dell'11 novembre).

Il decisore serve anche fuori dal router: nel controllo del contenuto prima di un'uscita L2 o L3, nella lettura delle risposte degli esterni, con la domanda a parte «chiede di non essere più contattato?», e nel colore dei dati ([ADR-0027](adr/0027-decisore.md)). Il suo motore di partenza è Jev 1.14.0, un modello «System One» che non scrive testo ma restituisce probabilità, chiamato via LiteLLM con la versione fissata, sui testi verdi; sui gialli quando Michele ammette TypeSafe come fornitore. Per i testi rossi o di colore ignoto restano un modello in casa o le regole. L'italiano non è un freno: la prova in italiano serve a tarare le soglie, domanda per domanda ([ADR-0027](adr/0027-decisore.md) e [ADR-0028](adr/0028-instradamento-a-piu-motori.md), revisioni dell'11 novembre). Le soglie partono alte, fra 0,7 e 0,9, e sono una prima stima ([ADR-0027](adr/0027-decisore.md)). Jev costa 0,042 $ per milione di token in ingresso, con l'uscita gratuita: il guadagno non è il risparmio, sono le probabilità e le soglie scritte in un file ([ricerca/47, «In breve»](../ricerca/47-modelli-system-one.md)).

**La corsia T.** Serve lo sviluppo di progetti in codice e i lavori lunghi di quattro agenti: Sviluppatori, Agente sito e SEO, Pipeline per il portale clienti, Sistemista per le pull request di aggiornamento. Non serve il lavoro quotidiano dei 57 agenti ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). Come funziona:

- il motore avvia, sul posto Claude Team della persona responsabile, un compito programmato di Claude Code con il solo avvio via API. All'inizio gira sulle macchine di Anthropic; più avanti su un runner nostro, se Michele lo ammette;
- ogni persona crea il suo compito e il suo token dal suo account; il token sta nel gestore dei segreti. Il motore non tiene mai il login di nessuno: il token avvia un solo compito, non legge nulla e non chiama il modello. Il login dei posti è riservato all'uso di Claude Code da parte delle persone, e chi costruisce prodotti con l'Agent SDK deve usare la chiave API ([ricerca/49 §1.1 e §1.2](../ricerca/49-instradamento-a-piu-motori.md));
- il motore manda solo dati; il lavoro lo descrivono le istruzioni salvate dalla persona;
- la consegna è un branch (un ramo separato del codice) `claude/…` e una pull request in bozza, cioè una proposta di modifica. Unire in `main` è una carta L1, come vuole la classe «Codice e infrastruttura»;
- nessun connettore, rete «Limited», solo le repo di SerSan ammesse da Michele, `main` protetto senza eccezioni, nessuna modifica ai workflow di GitHub; solo dati verdi e gialli, mai rosso;
- l'avvio passa dall'outbox del Cancello, la tabella delle uscite, e non si ripete da solo;
- un programma non può sapere quanto uso resta su un posto Team. Il motore tiene un conto per posto: al massimo 2 lavori T aperti e 4 consegne al giorno per persona. Se la consegna manca alla scadenza, il lavoro torna in coda dopo 5 ore oppure, se è urgente, va in corsia S con un tetto di spesa. Questi numeri sono prime proposte ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §1.3 e §3.7](../ricerca/49-instradamento-a-piu-motori.md)).

La corsia T entra solo dopo la prova di [ricerca/49 §7](../ricerca/49-instradamento-a-piu-motori.md) e una conferma scritta di Anthropic che questo uso rientra in quello previsto ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)). Con la sola chiave API lo stesso lavoro costa circa 7 $ per mezza giornata di sviluppo con Sonnet 5.5 e circa 14 $ con Opus 5.5 [stima di ricerca/49 §1.5]; su un posto premium, cioè il posto Team con più uso, già pagato, non costa nulla in più finché basta l'uso del posto, ma toglie uso alla persona ([ricerca/49 §5](../ricerca/49-instradamento-a-piu-motori.md)).

**La bacheca, i gruppi e il freno.** È il posto dove gli agenti si passano il lavoro ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md); [ricerca/36 §5.4](../ricerca/36-architettura-v2.md)):

- tabelle in PostgreSQL, `compiti` e `passaggi`, con un server MCP per creare, prendere, aggiornare, passare e chiudere un compito e leggerne lo stato. Un agente che scrive sulla bacheca fa partire il lavoro di un altro attraverso il registro degli eventi;
- dal modello della bacheca di Hermes: una corsia di revisione fra agenti prima della carta; il blocco "serve un umano", che si sblocca dalla chat; il blocco automatico dopo due fallimenti di fila; il rifiuto dei cicli di dipendenze; un dispatcher che riprende i compiti fermi;
- i gruppi di chat mostrano la bacheca: uno per squadra, con gli agenti e le persone che la seguono; uno per cliente, interno, che non è il canale condiviso con il cliente; uno comune, «Agenti», con tutti i passaggi e lo stand-up degli agenti. Una persona scrive in un gruppo per correggere, fermare o rilanciare un passaggio;
- il freno. La proposta fissava tre passaggi per catena e otto messaggi per thread ([proposta §4.11](../PRESENTAZIONE-CEO.md)); oggi vale il freno di [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md): 8 passaggi per le catene dichiarate, la stessa coppia di agenti non si rimbalza il lavoro più di due volte, il conteggio parte dall'ultimo messaggio umano, un tetto in dollari per catena. Oltre il tetto arriva una carta «Continua?»;
- i passaggi fra agenti sono azioni interne a L3; ciò che esce verso l'esterno passa dal Cancello al livello della sua terna;
- i to-do delle persone stanno in Jira. La chiusura dei to-do di una persona parte a L2, con una finestra di 24 ore, dalla fase 2 ([ricerca/45 §2.6 e §4.1](../ricerca/45-architettura-v3.md)).

Fino a quando la bacheca non c'è, i passaggi del pilota, per esempio dall'Analista chiamate al Post-call, stanno nel registro degli eventi ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)).

**Il registro degli agenti e le skill.** Il registro si vede come organigramma in una pagina della casa dei testi e in un cruscotto. Un agente nuovo nasce solo con un'approvazione, che porta con sé la sua riga nel registro dei trattamenti. Gli agenti al lavoro sono 14 alla fine della fase 2, circa 32 alla fine della fase 3 e tutti e 57 alla fine della fase 6 ([proposta §4.12](../PRESENTAZIONE-CEO.md)). La pagina e la vista Grafana si generano ogni notte dal registro in git ([ricerca/36 §5.3](../ricerca/36-architettura-v2.md)). Oltre al modello, ogni agente dichiara le destinazioni che il router può usare per lui ([ADR-0025](adr/0025-un-modello-per-agente.md), revisione dell'11 novembre). Le skill stanno in git; dalla fase 4 gli agenti scrivono proposte di skill in una cartella "proposte", un revisore le guarda ogni settimana e una persona le approva con una pull request ([proposta, appendice A, voce A6](../PRESENTAZIONE-CEO.md)). Con la v3 le skill interne con valutazione partono a L2, con una finestra di 48 ore, dalla fase 2, e possono arrivare a L3 ([ricerca/45 §2.6 e §4.1](../ricerca/45-architettura-v3.md)).

### 3.2 I servizi del board che il sistema usa

| Componente | Ruolo per gli agenti | Dove | Stato |
|---|---|---|---|
| **n8n** | Facoltativo. Resta per i collegamenti del board che servono: se un collegamento passa da n8n, n8n chiama `POST /eventi` e basta, senza dati rossi nelle esecuzioni, con una versione 2.x fissata. Pubblico solo sui webhook firmati, senza moduli pubblici | VLAN 30 | board, facoltativo |
| **LiteLLM** | Porta di tutti i modelli: chiavi virtuali e budget per agente, squadra e persona. Esce verso l'API di Anthropic, verso i modelli sul nostro server, verso Jev e verso i fornitori ammessi. La corsia T non passa da qui | VLAN 30; nel board arriva con la fase F4 | board |
| **PostgreSQL 16** | Coda dei lavori, registro degli eventi, bacheca, sessioni S, Cancello con livelli, carte e registro, decisioni del decisore, memoria strutturata, dati di LiteLLM | VLAN 40 | board |
| **Qdrant e MCP RAG** | Memoria vettoriale con ricerca per parole (BM25) e reranker (un modello che riordina i risultati). L'MCP RAG è il server che cerca nella memoria i passaggi utili e li passa al modello: applica i permessi della persona e registra le domande | VLAN 40 e 30 | board (fase F4), estensioni nostre |
| **Pipeline AI** | Ollama, il programma che fa girare i modelli locali, con Qwen3-4B per metadati e riassunti dei documenti; Infinity con embedding e reranker da 0.6B; Docling, che trasforma PDF e scansioni in testo | VLAN 80, `ai-gpu-01`, sulla RTX 4000 | board |
| **BookStack** | Regole "Come lavoro", processi, catalogo, manuale degli agenti. Resta in vigore finché non si sceglie la casa dei testi, prima della fase 2 | VLAN 30 | board, da confermare |
| **Infisical e Vaultwarden** | Segreti delle applicazioni, compresi i token della corsia T; password delle persone | VLAN 40 | board |
| **Archivio dei file** | Audio e file degli agenti. Il board prevedeva MinIO, che è archiviato e non più mantenuto: il sostituto lo sceglie Michele | VLAN 40 | board, da sostituire |
| **Firecrawl** | L'unica strada degli agenti verso il web: scarica le pagine e le trasforma in testo markdown | VLAN 30 | board |
| **Open WebUI** | La chat con i modelli per tutti, con il budget di LiteLLM | VLAN 30 | board |
| **Monitoraggio** | Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox | VLAN 70 | board |
| **Traefik, Pangolin, NetBird** | Ingresso dei servizi pubblici e accesso da fuori | VLAN 20 e macchina Oracle | board |
| **SersanOutreach** | La piattaforma outbound, che diventa il CRM degli agenti. Due server MCP: lettura con 19 strumenti, operatore con 14 operazioni | VLAN 30, dalla fase F2 del board | board |

Fonti: [ricerca/36 §4.1, §4.5 e §5.7](../ricerca/36-architettura-v2.md); [proposta §7.2 e §7.3](../PRESENTAZIONE-CEO.md); [domande per Michele, n. 11](../DOMANDE-PER-MICHELE.md); per la v3, [ADR-0004](adr/0004-litellm-banca-token.md), [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), [ADR-0011](adr/0011-n8n-orari-integrazioni.md), [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md) e [ADR-0028](adr/0028-instradamento-a-piu-motori.md).

Su SersanOutreach due regole contano per l'architettura. L'operazione che approva un messaggio la chiama solo il Cancello: gli agenti leggono liberamente e scrivono solo attraverso il Cancello. Non esistono invii in blocco, lanci o cancellazioni: restano a una persona ([proposta §7.3](../PRESENTAZIONE-CEO.md)). Nella proposta l'operazione partiva dopo il sì di una persona su una carta; oggi parte al livello della terna, e per le campagne a freddo resta a L1 per singolo contatto, oppure una carta per campagna dopo il parere ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)). Il database resta su Supabase, che il board tiene in cloud, salvo una scelta diversa di Michele ([proposta §7.2](../PRESENTAZIONE-CEO.md)). Oggi i due server MCP parlano solo in locale (stdio): nella fase 2 vanno portati su HTTP, con un token per ogni famiglia di agenti ([ricerca/36 §7.3 e §8.1, voce B2](../ricerca/36-architettura-v2.md)).

### 3.3 I servizi nuovi da aggiungere al board

| Componente | Ruolo | Dove | Fase |
|---|---|---|---|
| **MariaDB** | Il database che BookStack richiede; serve solo se resta BookStack | VLAN 40, container | 2 |
| **Servizi dei modelli locali** | llama.cpp e vLLM per i modelli open-weight, Speaches per la trascrizione; tutti parlano l'API di OpenAI e stanno dietro LiteLLM | VLAN 80, `ai-gpu-01` | prova dopo la milestone 1 |
| **Trascrizione** | Trascrive in casa l'audio delle call e delle riunioni dal vivo (faster-whisper, Parakeet, pyannote per riconoscere chi parla) | VLAN 80, `ai-gpu-01` | 3 |
| **Vexa** | Il bot che entra nelle call dei clienti (Teams di altri, Meet, Zoom) | `meet-01`, VLAN 35 | 3 |
| **Asterisk 22 LTS** | Il centralino di Andrea, collegato al trunk SIP dell'operatore italiano (la linea telefonica via internet) | `voce-01`, VLAN 25 | 5 |
| **Pipecat** | La conversazione di Andrea: ascolto, ragionamento con Claude Haiku, voce. Prima sulla CPU, poi sulla seconda GPU | `andrea-01`, VLAN 30 | 5 |
| **Postiz** | Programmazione dei post e metriche. Mai pubblico. Prima della fase F4 del board entra solo con il sì di Michele; fino ad allora i post della pagina aziendale li programma l'esecutore Metricool del Cancello | VLAN 30, container | 4 |
| **listmonk** | Newsletter, con l'invio attraverso un relay SMTP esterno (un servizio che spedisce la posta in quantità). Mai pubblico | VLAN 30, container | 4 |
| **DocuSeal** | Firma elettronica; solo le pagine di firma escono via Pangolin | VLAN 30 | 6 |
| **Fatturazione** | Fatture, incassi e solleciti: Sirius, che ha già i dati fiscali e dei clienti, se fa al caso, oppure Invoice Ninja in casa (decisione 22) | VLAN 30, container | 6 |
| **Buzz** | Casa degli agenti in prova, collegata alla stessa bacheca, con dati verdi | Experimental-2, VLAN 90 | subito dopo la milestone 1 |
| **Paperclip** | Piano di controllo open source per "aziende di agenti", in prova, senza dati dei clienti | Experimental-2, VLAN 90 | 6 |

Fonti: [ricerca/36 §4.1 e §4.5](../ricerca/36-architettura-v2.md); [proposta §11 e appendice A, voci G5, L1 e L2](../PRESENTAZIONE-CEO.md); per la v3, [ricerca/48 §4.1](../ricerca/48-modelli-locali-e-gpu.md), [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), [ADR-0013](adr/0013-postiz-listmonk-docuseal.md), [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md) e [ricerca/45 §3.1](../ricerca/45-architettura-v3.md). Le decisioni 9, 15, 21 e 22 della proposta le prende oggi il gruppo di progetto con Michele ([ADR-0013](adr/0013-postiz-listmonk-docuseal.md)).

Ogni servizio nuovo entra nel perimetro Cyber Essentials (la certificazione britannica di sicurezza di base, paragrafo 8.2) con un responsabile delle patch e un posto nell'inventario. Prima della fase F4 del board entrano solo i servizi del pilota ([proposta §6.2 e §13](../PRESENTAZIONE-CEO.md)). Chi patcha cosa lo fissa Michele ([domande per Michele, n. 9](../DOMANDE-PER-MICHELE.md)).

### 3.4 Cloud del board ed esterni

| Servizio | Ruolo | Stato |
|---|---|---|
| **M365 ed Entra ID** | Identità, MFA, posta, calendario, documenti, Teams. Gli agenti ci arrivano con Graph, l'API di Microsoft 365, con permessi stretti: siti SharePoint scelti uno per uno e caselle limitate | cloud |
| **Claude Team** | La finestra di lavoro delle persone, con il connettore verso la memoria. I compiti programmati restano per l'uso personale, salvo la corsia T: lo sviluppo e i lavori lunghi di quattro agenti, avviati dal motore con il solo avvio via API. Nessun altro processo aziendale gira su Claude Team: ciò che è a orario sta nel motore | cloud |
| **API di Anthropic** | Il ragionamento delle corsie N e S, solo attraverso LiteLLM; la chiave diretta solo sul banco di prova. Il piano Team include fino a 500 $ al mese di crediti API, che coprono l'API e l'Agent SDK ma non Claude Code: se il nostro piano ne ha diritto va controllato | cloud |
| **Managed Agents** | Riserva solo sui dati verdi, se il server è pieno o fermo. Le azioni esterne passano comunque dal Cancello | cloud, riserva |
| **Jira** | To-do e progetti | cloud |
| **Instantly** | Invio delle campagne email; lo stop di emergenza mette in pausa le campagne | cloud |
| **GitHub, Vercel** | Codice, runner in casa e consegne della corsia T come pull request; i deploy del sito li fa una persona | cloud |
| **Supabase** | Il database di SersanOutreach | cloud |
| **Cloudflare** | Solo il DNS | cloud |
| **Macchina Oracle a Milano** | NetBird (gestione e relay), Pangolin, Uptime Kuma e ntfy (notifiche push) | cloud |
| **Operatore telefonico italiano** | Numero e trunk SIP di Andrea (proposto: Messagenet) | esterno |
| **WhatsApp, Telegram, Slack** | Canali in più verso gli stessi agenti | esterni |
| **Relay SMTP** | Invio della newsletter | esterno |
| **Strumenti commerciali** | Quelli che restano, decisi caso per caso (decisione 15) | esterni |
| **Metricool** | Programma i post della pagina aziendale finché Postiz non entra: 59,86 € al mese, già nel kit | esterno |
| **TypeSafe (Jev)** | Il motore di partenza del decisore, via LiteLLM. Servizio negli USA, senza SLA: riceve i testi verdi, e i gialli solo se Michele lo ammette | esterno |
| **Fornitori di modelli open-weight** | Per esempio OpenRouter, solo per un modello che Claude non ha e che noi non ospitiamo; solo dati verdi e gialli, con le opzioni che vietano di conservare i dati | esterno, se serve |

Fonti: [proposta §5.1, §5.2 e §14](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1, §5.6, §8.2 e §12](../ricerca/36-architettura-v2.md); [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md); [domande per Michele, n. 10](../DOMANDE-PER-MICHELE.md); per la v3, [ADR-0024](adr/0024-abbonamenti-come-riserva.md), [ADR-0025](adr/0025-un-modello-per-agente.md), [ADR-0027](adr/0027-decisore.md), [ADR-0028](adr/0028-instradamento-a-piu-motori.md), [ricerca/45 §3.1](../ricerca/45-architettura-v3.md), [ricerca/47 §1.2](../ricerca/47-modelli-system-one.md) e [ricerca/49 §1.3](../ricerca/49-instradamento-a-piu-motori.md).

### 3.5 La chat di gruppo

- **Teams è la casa delle persone**: un team "SerSan Agent OS" con un canale per squadra, "Approvazioni" per le carte, "Agenti" (la sala macchine dove gli agenti si passano il lavoro), "Ingresso", "Call di vendita", "Bandi" e un canale privato per ogni cliente. Ogni squadra ha un bot con il nome dei suoi agenti e ogni messaggio è firmato dall'agente che lo scrive ([proposta §4.11](../PRESENTAZIONE-CEO.md)). Le approvazioni dal telefono restano in Teams, con l'identità certa di chi preme ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)).
- **Le carte e le finestre.** Sul telefono arrivano la carta L1 con «Approva», «Modifica» e «No», e la finestra L2 con «Ferma», «Modifica» e «Invia ora»; nel debrief arrivano le proposte di promozione e il tasto «sbagliato» ([ricerca/45 §2.6 e §3.1](../ricerca/45-architettura-v3.md)). Prima che la Porta di Teams sia pronta, le stesse cose si fanno dalla Sala di controllo della milestone 1.
- **I gruppi degli agenti.** Oltre al canale "Agenti" ci sono un gruppo per squadra e un gruppo interno per cliente. Arrivano subito dopo la milestone 1, con la bacheca, e all'inizio stanno in Teams ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)).
- **I bot sono dieci registrazioni**, il Cancello più nove squadre; che puntino tutte allo stesso servizio va provato ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)). La registrazione è "Teams-managed", senza sottoscrizione Azure. Se dà errori 401, si usa un Azure Bot F0 gratuito, senza risorse accese, oppure il piano B: le carte sulla pagina del Cancello dietro Pangolin, con l'accesso Entra, e gli avvisi in Teams ([ricerca/36 §5.6](../ricerca/36-architettura-v2.md); [ricerca/45 §12.2](../ricerca/45-architettura-v3.md)).
- **Il nodo Teams di n8n serve solo agli avvisi**, quando n8n c'è: registra l'ora della risposta, non chi approva ([ricerca/36 §5.6](../ricerca/36-architettura-v2.md)).
- **Telegram** riceve gli avvisi; **WhatsApp** serve soprattutto verso i clienti, con l'API ufficiale di Meta e un numero dedicato, sempre dal Cancello; **Slack** si collega per i clienti che lavorano lì. Sono gli stessi agenti con lo stesso codice, dalla fase 3, al livello della classe del destinatario. Su questi canali passano solo dati verdi; per approvare anche da lì servirebbe legare quegli account all'identità Microsoft di ciascuno ([proposta §4.11](../PRESENTAZIONE-CEO.md); [ADR-0006](adr/0006-teams-chat-di-gruppo.md), revisione del 10 novembre).
- **Buzz**, la chat open source di Block fatta per persone e agenti, si collega alla stessa bacheca e si prova sul banco subito dopo la milestone 1, con dati verdi. La proposta lo metteva in prova dalla fase 4: oggi perde alcune risposte senza segnalarlo e le sue approvazioni non sono collegate ([proposta §4.11](../PRESENTAZIONE-CEO.md); [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). Se non perde risposte e ha le approvazioni collegate, diventa la casa degli agenti e i gruppi passano lì; se no, i gruppi restano in Teams ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)). I criteri di uscita, con le issue da chiudere, sono in [ricerca/36 §5.6](../ricerca/36-architettura-v2.md).
- **Nessun bot entra nei canali condivisi con i clienti**: lì scrive solo il Cancello, al livello della classe del destinatario ([proposta §4.11](../PRESENTAZIONE-CEO.md); [ADR-0006](adr/0006-teams-chat-di-gruppo.md), revisione del 10 novembre).

---

## 4. Il percorso di un'azione

L'obiettivo è che il lavoro dopo una call avvenga in modo autonomo, e ci si arriva per gradi ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Nella proposta il caso tipico era questo: dopo una call in Teams il riassunto arriva nel canale interno e la bozza della mail di follow-up arriva sul telefono come carta; dopo il sì parte una volta sola ([proposta §1](../PRESENTAZIONE-CEO.md)). Con la v3 il riassunto esce a L3 entro 10-20 minuti dalla trascrizione, e il follow-up alla persona appena incontrata parte a L2: la carta dice «parte alle HH:MM», e se nessuno preme «Ferma» entro 30 minuti in orario di lavoro la mail parte una volta sola ([ricerca/45 §4.1](../ricerca/45-architettura-v3.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)). Il percorso, passo per passo:

1. **Nasce il lavoro.** In quattro modi: un orario della tabella del motore; un evento su `POST /eventi`, per esempio dal lettore delle trascrizioni, dalla Porta o da un servizio esterno; una persona che scrive a un agente; un agente che passa un compito a un altro nella bacheca. Ogni evento entra nel registro degli eventi con una chiave, così lo stesso evento ricevuto due volte non fa partire due catene ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)). Il lavoro entra nella coda con il profilo, la persona per cui si lavora, il tetto di spesa e la scadenza ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
2. **Il router sceglie dove farlo.** Prima le regole fisse, poi il decisore per gli eventi a testo libero, poi la tabella: regola, catena N, sessione S, corsia T o persona (paragrafo 3.1) ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
3. **Parte la catena o la sessione.** L'agente legge le regole "Come lavoro" della persona, i dati fissi dall'MCP della memoria e i passaggi utili dall'MCP RAG, con i permessi della persona ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md); [ricerca/45 §3.2](../ricerca/45-architettura-v3.md)).
4. **Il testo di terzi resta un dato.** Mail, trascrizioni, pagine web e risposte dei prospect entrano da una corsia senza strumenti, che restituisce solo campi a schema. Gli agenti li leggono come dati, non come comandi; è la difesa contro le iniezioni di prompt ([proposta §9.2](../PRESENTAZIONE-CEO.md)). Nella corsia N il codice sceglie anche i destinatari ([ADR-0023](adr/0023-protezioni-essenziali.md)). Nella corsia S chi legge testo di terzi non può proporre azioni nella stessa sessione ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
5. **L'agente propone.** Se qualcosa deve uscire, l'agente propone un'azione, per esempio "manda questa mail a questo indirizzo", con il testo esatto e il motivo ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Nella corsia N la propone la catena, con il destinatario preso dai dati. Nella corsia S, prima di ogni strumento, l'Agent SDK chiama una funzione del runner, l'hook `PreToolUse`, che chiede al Cancello; se il Cancello non risponde in tempo, l'azione è bloccata ([proposta §5.3](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.1](../ricerca/36-architettura-v2.md)). In un giro della corsia S passano un pacchetto di scritture interne e un solo elemento esterno ([ADR-0001](adr/0001-motore-agent-sdk.md), revisione del 10 novembre).
6. **Il Cancello calcola classe e livello.** Dai dati calcola la classe del destinatario, poi guarda il livello della terna, i tetti del giorno e la lista di soppressione. Prima di un'uscita L2 o L3 controlla il contenuto: se trova cifre, prezzi, sconti, date o impegni che non vengono dal CRM, l'azione scende a L1 (paragrafo 4.1) ([ADR-0020](adr/0020-autonomia-a-livelli.md)).
7. **L'uscita al suo livello.** A L1 arriva una carta, con il testo esatto e una scadenza; a L2 una finestra con «Ferma», «Modifica» e «Invia ora»; a L3 l'azione parte subito; a L0 prepara l'agente ed esegue una persona ([ADR-0020](adr/0020-autonomia-a-livelli.md)). Il Cancello controlla chi ha premuto, con l'identità Microsoft, e che sia fra gli approvatori di quella classe ([proposta §4.11](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.1](../ricerca/36-architettura-v2.md)). Nella proposta offerte, contratti, fatture e primi contatti chiedevano anche la chiave FIDO2 sulla pagina del Cancello ([proposta §5.4](../PRESENTAZIONE-CEO.md)); oggi la FIDO2 sulle carte non c'è più ([ADR-0023](adr/0023-protezioni-essenziali.md)). Intanto il lavoro resta in attesa ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
8. **L'esecuzione, una volta sola.** Dopo il sì, alla fine della finestra o subito a L3, l'esecutore del Cancello compie l'azione una volta sola. Passa dall'outbox: si registra prima dell'effetto, e un esito «incerto» va a una persona invece di ripetersi ([ADR-0023](adr/0023-protezioni-essenziali.md)). Se nel frattempo il testo è cambiato, la carta non vale più ([proposta §5.4](../PRESENTAZIONE-CEO.md)): l'esecutore ricalcola l'impronta del testo esatto prima di agire ([ricerca/35 §8](../ricerca/35-giudizio-sicurezza.md); [ADR-0023](adr/0023-protezioni-essenziali.md)). Gli esecutori sono stretti: la posta parte da Outlook via Graph solo verso il dominio del cliente ([ricerca/36 §8.1, voce B3](../ricerca/36-architettura-v2.md)), e con la v3 solo all'indirizzo esatto del partecipante registrato ([ricerca/45 §12.3](../ricerca/45-architettura-v3.md)).
9. **Il registro.** Tutto finisce nel registro: chi ha chiesto, chi ha approvato o lasciato passare, a quale livello, quanto è costato ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Il registro delle azioni è a sola aggiunta, con il valore prima e dopo delle scritture interne, e i segreti vengono oscurati prima di qualsiasi log ([proposta §9.2](../PRESENTAZIONE-CEO.md); [ADR-0023](adr/0023-protezioni-essenziali.md)).
10. **La ripresa.** L'esito diventa un evento e la catena riprende da lì; una sessione S riprende con l'esito come nuovo messaggio ([ricerca/45 §6.1](../ricerca/45-architettura-v3.md); [ricerca/36 §5.1](../ricerca/36-architettura-v2.md)). Una carta o una finestra lasciata ferma la notte riprende il lavoro giusto al mattino: è uno dei criteri della verifica della settimana 8 ([proposta §11](../PRESENTAZIONE-CEO.md); [ricerca/45 §6.2](../ricerca/45-architettura-v3.md)).
11. **Il conto.** LiteLLM conta la spesa e blocca oltre il budget. La stima di costo dell'SDK va nel cruscotto e ogni mese si confronta con la Console di Anthropic ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).

### 4.1 Livelli, classi e chi approva

**La terna e la classe.** Ogni terna, cioè agente, tipo d'azione e classe del destinatario, ha il suo livello. Per un singolo destinatario si può fissare un'eccezione, per esempio «solo con revisione». La classe la calcola il Cancello dai dati: calendario, partecipanti registrati, CRM. Non la prende mai da ciò che dichiara l'agente né dal testo di una mail ([ADR-0020](adr/0020-autonomia-a-livelli.md)).

| Classe | Chi ne fa parte | Partenza | Tetto |
|---|---|---|---|
| Interno | canali interni, CRM, Jira, calendario, libro delle proposte, la persona stessa | L3 | L3 |
| Persona appena incontrata | l'indirizzo esatto di chi era in una call registrata e avvisata negli ultimi 14 giorni. Il dominio da solo non basta mai | L2, con una finestra di 30 minuti | L3 dopo il parere |
| Contatto in conversazione | chi ci ha scritto per primo, o un cliente con un progetto attivo, negli ultimi 90 giorni. Chi è entrato da una campagna a freddo resta fuori | L1 | L3 dopo il parere |
| Lead che ha chiesto la richiamata | Andrea | L3 dopo il parere e le chiamate di prova | L3 |
| Pubblico aziendale | pagina aziendale, iscritti alla newsletter, invitati agli eventi | L1 | L2 |
| Voce dei founder | post e commenti sui profili personali | L1; i commenti L0 | L1 |
| Destinatario nuovo | primo contatto, dominio mai visto | L1 | L1 |
| Impegni | offerte, contratti, fatture, prezzi, affermazioni tecniche | L1 | L1 |
| Codice e infrastruttura | pull request, patch | L1 | L1 |
| Pagamenti | — | L0 | L0 |
| Cancellazioni e credenziali | — | vietate | vietate |

Fonti: [ricerca/45 §2.2](../ricerca/45-architettura-v3.md) per la tabella; la partenza a L2 della persona appena incontrata è la decisione D11 del gruppo di progetto ([ricerca/45, «Decisione del gruppo di progetto»](../ricerca/45-architettura-v3.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)). Gli invii veri ai clienti cominciano con la milestone «telefono e posta», la 4 del PRD: se prima di allora il parere legale esclude la partenza a L2, la classe torna a L1 cambiando una riga di configurazione. La classe «persona appena incontrata» è stretta all'indirizzo esatto perché il Garante applica l'art. 130 anche agli indirizzi aziendali: se bastasse lo stesso dominio, un collega riceverebbe marketing senza consenso ([ricerca/45 §2.2](../ricerca/45-architettura-v3.md)).

**Chi approva.** Approvatore e sostituto per classe stanno nella configurazione ([ADR-0003](adr/0003-cancello-approvazioni.md), revisione del 10 novembre). Si parte dagli approvatori del piano tecnico: Alessandro per gli invii a clienti e prospect; Alberto o il founder del profilo per le pubblicazioni; Michele per offerte, contratti e affermazioni tecniche; Alessandro o Michele per fatture e solleciti; Alberto per il codice e Michele per le patch del server ([ricerca/36 §5.8](../ricerca/36-architettura-v2.md)). La pull request della corsia T arriva come carta L1 al responsabile dell'agente ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

**La finestra L2.** La carta dice «parte alle HH:MM» e ha tre tasti: «Ferma», «Modifica», «Invia ora». Alla scadenza l'esecutore ricalcola l'impronta del testo ed esegue una volta sola. La finestra conta solo in orario di lavoro, dalle 8:30 alle 19:00 dal lunedì al venerdì, oppure l'orario scritto nella pagina "Come lavoro" della persona; fra le 20:00 e le 8:00 e nel fine settimana non parte nulla verso l'esterno, salvo Andrea ([ricerca/45 §2.6](../ricerca/45-architettura-v3.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)). La durata cambia con il lavoro ([ADR-0020](adr/0020-autonomia-a-livelli.md)):

- 30 minuti per il follow-up e il recap dopo una call;
- 60 minuti per risposte e inviti ai contatti in conversazione;
- 24 ore per i post aziendali, le slide al cliente, la chiusura dei to-do di una persona e i solleciti;
- 48 ore per la newsletter, con un invio di prova alla persona, gli inviti agli eventi, le aperture di Andrea e le skill interne.

**La riga AI.** Ciò che parte a L2 o a L3 non lo legge nessuno prima, quindi porta una riga che dichiara l'assistente AI di SerSan. Ciò che esce a L1 esce a nome di chi approva. Il testo definitivo della riga lo fissa il parere legale (D8) ([ADR-0020](adr/0020-autonomia-a-livelli.md); [ricerca/45 §2.6](../ricerca/45-architettura-v3.md)).

**Il controllo del contenuto.** Prima di ogni uscita L2 o L3 un passo a schema cerca cifre, prezzi, sconti, date di consegna e impegni che non vengono dal CRM. Se ne trova uno, l'azione scende a L1 ([ADR-0020](adr/0020-autonomia-a-livelli.md)). Cifre e date le trova il codice; le domande di significato le fa il decisore ([ADR-0027](adr/0027-decisore.md)).

**I tetti giornalieri.** Al massimo 15 follow-up e 10 inviti al giorno per agente in ogni classe esterna a L3, e al massimo 2 messaggi al giorno per destinatario. Oltre il tetto l'azione diventa una carta L1 e non si perde (D10) ([ADR-0020](adr/0020-autonomia-a-livelli.md)).

**La lista di soppressione.** È unica: un «no» blocca le azioni verso quel contatto su tutti i canali ([ADR-0023](adr/0023-protezioni-essenziali.md)).

**«Annulla» e «Rettifica».** «Annulla» di una scrittura interna non cancella nulla: rimette il valore precedente o segna la voce come annullata, e lo esegue il Cancello a nome della persona. «Rettifica» dopo un invio crea una carta L1 e abbassa la terna ([ADR-0023](adr/0023-protezioni-essenziali.md); [ricerca/45 §2.5](../ricerca/45-architettura-v3.md)).

**Scadenza delle carte.** Le carte L1 scadono dopo 3 giorni lavorativi, con un promemoria nel debrief; per ciò che dipende dal tempo, come inviti e risposte, dopo 24 ore (D1) ([ADR-0020](adr/0020-autonomia-a-livelli.md)).

### 4.2 Le regole "Sempre", sostituite dalla promozione

Nella proposta, quando la stessa approvazione si ripeteva uguale venti volte senza modifiche, una persona poteva trasformarla in una regola "Sempre", stretta su quell'agente, quel tipo di azione e quella destinazione, con una scadenza di 30 giorni ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Oggi le regole "Sempre" non ci sono più: le sostituiscono le classi di destinatari calcolate dai dati, che valgono per un gruppo intero, e la promozione per terna ([ADR-0003](adr/0003-cancello-approvazioni.md), revisione del 10 novembre; [ADR-0020](adr/0020-autonomia-a-livelli.md)).

**Per salire** ([ADR-0020](adr/0020-autonomia-a-livelli.md); [ricerca/45 §2.4](../ricerca/45-architettura-v3.md)):

| Passaggio | Condizione | Chi conferma |
|---|---|---|
| L1 → L2 | 5 sì di fila senza modifiche di sostanza sulla stessa terna, e nessun segnale negativo negli ultimi 30 giorni. È «di sostanza» una modifica al destinatario, all'oggetto o a più del 10% del testo | il responsabile della squadra, con un tocco sulla proposta di promozione che arriva nel suo debrief |
| L2 → L3 | 15 finestre di fila senza «Ferma» e senza segnali negativi negli ultimi 60 giorni | lo stesso responsabile |
| oltre il tetto della classe | mai | — |

**Per scendere** la discesa è automatica e immediata ([ricerca/45 §2.4](../ricerca/45-architettura-v3.md)):

| Segnale | Effetto |
|---|---|
| «Ferma» con motivo «errore», oppure «Rettifica» dopo un invio | la terna scende di un livello |
| una modifica a una carta | il contatore della terna riparte da zero |
| risposta dell'esterno classificata come correzione, lamentela o «non scrivetemi» | la terna scende di un livello e l'indirizzo entra nella lista di soppressione unica |
| risposta dubbia | va in carta a una persona; la terna resta ferma finché qualcuno decide |
| «sbagliato» premuto sul riepilogo del debrief | la terna scende di un livello |
| rimbalzo, o destinatario fuori dalla classe | l'invio si blocca e la terna scende di un livello |
| due segnali in 30 giorni | la terna torna a L1 |
| incidente serio (destinatario sbagliato, dati di un altro cliente) | tutte le classi esterne dell'agente tornano a L1 |
| cambio di modello o di istruzioni senza valutazione | la terna torna a L1 |
| stop di emergenza | tutto va a L0; dopo lo sblocco la classe che l'ha causato riparte da L1 |
| la stessa impronta verso la stessa destinazione entro 7 giorni | l'azione diventa una carta |

Abbassare un livello può chiunque dei quattro; alzarlo solo il responsabile. Le classi non scadono da sole come le regole "Sempre": si rivedono ogni mese nel resoconto ([ricerca/45 §2.4](../ricerca/45-architettura-v3.md)). Quali messaggi ai clienti possono salire a L2 e a L3 dipende dal parere legale: se il parere chiude una porta, la funzione resta e la sua classe rimane a L1 ([ricerca/45 §2.8](../ricerca/45-architettura-v3.md)).

### 4.3 Eccezioni e freni

- **Limiti fissi.** Stanno nel codice: gli agenti non cancellano e non toccano credenziali, e per questi tipi d'azione non esiste un esecutore; i pagamenti non hanno un esecutore, l'agente prepara e una persona paga; un tipo d'azione sconosciuto è negato ([ADR-0023](adr/0023-protezioni-essenziali.md); [ricerca/45 §2.5](../ricerca/45-architettura-v3.md)).
- **Andrea** telefona senza carta solo a chi ha chiesto di essere richiamato nel modulo, e dice subito di essere un assistente AI (decisione 10) ([proposta §1 e §5.1](../PRESENTAZIONE-CEO.md)). Lavora a L3 solo dopo il parere legale, il consenso registrato e 50 chiamate di prova. Parte dalla fase 5; con lead vere si può anticipare alla fase 3. Le sue aperture partono a L2, con una finestra di 48 ore, poi passano a L3 dentro una banca di frasi approvate ([ADR-0008](adr/0008-andrea-centralino.md), revisione del 10 novembre).
- **Le automazioni nascono spente**: ogni automazione parte in prova a secco e per una o due settimane mostra cosa avrebbe fatto, senza farlo ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Lo stop di emergenza** lo preme chiunque dei quattro, dal telefono, con `/stop` in Teams o dalla Sala di controllo; lo tolgono Alessandro o Michele. Ferma la coda e le sessioni, e annulla le carte e le finestre aperte: tutto va a L0. Dalla fase 2 porta anche a zero i budget di LiteLLM, fa scattare il kill switch di SersanOutreach e mette in pausa le campagne di Instantly. Dopo lo sblocco ripartono solo i nuovi eventi: le azioni annullate restano annullate ([ADR-0023](adr/0023-protezioni-essenziali.md); [ricerca/45 §2.7](../ricerca/45-architettura-v3.md)). Con lo stop il motore non avvia nessun lavoro della corsia T, e Managed Agents, se è in uso come riserva, perde la chiave ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ADR-0024](adr/0024-abbonamenti-come-riserva.md)). I dati restano in PostgreSQL, nella casa dei testi, in Jira e in M365, e il lavoro torna a mano ([proposta §4.8 e §9.2](../PRESENTAZIONE-CEO.md); [ricerca/36 §12](../ricerca/36-architettura-v2.md)).
- **Dieci scenari di prova** girano a ogni aggiornamento, riscritti sui livelli, più tre prove di continuità: la notte, un crash a metà catena, un riavvio. Il criterio non è più «nessun effetto senza una carta», ma «nessun effetto fuori dal suo livello» ([proposta §11 e §13](../PRESENTAZIONE-CEO.md); [ricerca/45 §6.1 e §6.4](../ricerca/45-architettura-v3.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)). La batteria di prove gira con un comando, gratis, sulle macchine con Windows e al banco anche su Linux ([ADR-0023](adr/0023-protezioni-essenziali.md)).

### 4.4 Come arriva, passo per passo

Lo sviluppo è partito il 10 novembre 2026 sulle macchine di sviluppo, con dati di prova e un modello a copione, cioè un modello finto che dà risposte scritte prima, senza chiave API. Lo spec della milestone 1 è alla revisione 3.2, con 49 criteri di accettazione, e il suo piano ha 14 gruppi e 70 compiti.

| Passo | Cosa si aggiunge al percorso |
|---|---|
| Milestone 1 | Cancello a livelli e corsia N: L1, L2 e L3, tetti, controllo del contenuto, classi calcolate dai dati, promozione e discesa, riga AI, «Annulla» e «Rettifica», lista di soppressione, stop; la catena «post-call» con le regole "Come lavoro"; registro degli eventi; decisore a copione e su un modello a schema; registro dei modelli; testi letti da file; esecutori di prova; la Sala di controllo |
| Milestone 2 | Corsia S; bacheca e gruppi degli agenti; prova di Buzz; primo modello open-weight |
| Milestone 3 | Prove con Microsoft e LiteLLM: bot di Teams senza Azure, identità di chi preme e «Ferma» sulla carta, LiteLLM davanti alle catene con un budget per catena. Se il bot non va, il piano B è una pagina del Cancello con accesso Entra |
| Milestone 4 | Telefono e posta: Alessandro approva una bozza dal telefono o la lascia passare dopo 30 minuti, e la mail parte una volta sola e solo all'indirizzo esatto, con la riga AI |
| Milestone 5 | Dalla call al riassunto: lettore delta di Graph, oscuramento, ingresso nelle call Teams nostre, riassunto L3 nel canale interno, nessun dato rosso salvato |
| Milestone 6 | Tre agenti sul banco: debrief L3 alle 7:00 o all'ora di ciascuno, post-call L3 interno, follow-up a L2, o a L1 se il parere lo esclude; to-do in Jira se c'è margine |
| Milestone 7 | Collaudo della settimana 8: i criteri misurati, più tre metriche, cioè i minuti fra la fine della call e il follow-up, la quota di azioni L2-L3 e i «Ferma» ogni 100 finestre |
| Fase 2 | Motore e Cancello sul server, con LiteLLM; nove bot di squadra; SersanOutreach collegato; esecutori di calendario, Jira, SersanOutreach e pausa di Instantly |
| Fase 3 | Telegram, Slack e WhatsApp, al livello della classe del destinatario |

Le milestone sono quelle del PRD; il loro contenuto viene da [ricerca/45 §6.4 e §12](../ricerca/45-architettura-v3.md), con la numerazione nuova. Le fasi 2 e 3 vengono dalla [proposta §11](../PRESENTAZIONE-CEO.md) e da [ricerca/36 §7.3](../ricerca/36-architettura-v2.md). Nella proposta la fase 2 portava anche la FIDO2 e le regole "Sempre", e il motore usava n8n: oggi valgono [ADR-0023](adr/0023-protezioni-essenziali.md), [ADR-0020](adr/0020-autonomia-a-livelli.md) e [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md). Il router e la prova della corsia T vengono dopo la milestone 1, con le prove di LiteLLM; la corsia T sui progetti veri arriva solo dopo la prova e la conferma scritta di Anthropic ([ADR-0028](adr/0028-instradamento-a-piu-motori.md)).

---

## 5. La memoria

### 5.1 Dove sta cosa

La memoria è divisa per tipo, e ogni tipo ha una sola fonte di verità ([proposta §5.5](../PRESENTAZIONE-CEO.md)).

| Dove | Cosa contiene | Come la legge un agente |
|---|---|---|
| La casa dei testi, sul server: BookStack oppure una cartella di file Markdown in git | le regole di lavoro di ciascuno ("Come lavoro"), i processi, il catalogo servizi, il manuale degli agenti | MCP dei testi, in sola lettura |
| PostgreSQL, sul server | registro e organigramma degli agenti, obiettivi, prezzi, registro dei meeting, decisioni, passaggi fra agenti, registro degli eventi | MCP della memoria, in sola lettura |
| Qdrant, sul server | ciò che "connette i momenti": trascrizioni, mail, documenti, Sirius, bandi, pagine dei testi, issue di Jira | MCP RAG, con i permessi della persona |
| Jira | to-do e progetti | MCP di Jira |
| M365 | documenti, posta e calendario | MCP di posta e calendario in lettura, solo sulle caselle in ambito |

Fonti: [proposta §5.5](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.5](../ricerca/36-architettura-v2.md); [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), revisione del 10 novembre. Il piano tecnico propone anche un taccuino per ogni famiglia di agenti su mcp-memory, mai con dati dei clienti ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md)); cosa faccia oggi mcp-memory nel board è una domanda aperta ([domande per Michele, n. 25](../DOMANDE-PER-MICHELE.md)).

**La casa dei testi.** Resta aperta una domanda: dove vivono i testi che gli agenti leggono e scrivono, cioè playbook, verbali, "Come lavoro" e voce del brand. Le strade sono due: BookStack, la wiki prevista dal board, oppure una cartella di file Markdown in git sul server. Nei voti la cartella è avanti di 3 punti su 100 (66,5 contro 63,5), ma la differenza sta dentro l'incertezza e il suo lavoro non è stimato. La scelta si fa prima della fase 2, con le prove di [ricerca/46 §9](../ricerca/46-obsidian-come-casa-dei-testi.md): la prova decisiva è che ognuno dei due CEO cambi la sua pagina "Come lavoro" chiedendolo a un agente in Teams. Obsidian non è la casa dei testi: da solo non ha permessi né accesso unico, e per più persone chiede un servizio cloud fuori dal board; resta al massimo un editor facoltativo sul PC ([ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), revisione del 10 novembre; [ricerca/46, «In breve»](../ricerca/46-obsidian-come-casa-dei-testi.md)). BookStack costa circa 2 giorni di posa con MariaDB, più 0,5-2 giorni per il suo server MCP; per la cartella in git la stima va fatta ([ricerca/46 §8](../ricerca/46-obsidian-come-casa-dei-testi.md)).

### 5.2 Come entra

La pipeline del board rende ricercabili i documenti. Il principio è "il server cerca e prepara, Claude ragiona", e password e chiavi non entrano mai nell'indice ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)):

1. **esportazione** incrementale da Sirius di dati fiscali, clienti e documenti;
2. **Docling** trasforma PDF, scansioni e tabelle in testo strutturato;
3. **filtro**: segreti e chiavi scartati, dati personali marcati;
4. **blocchi e metadati**: Qwen3-4B scrive cliente, anno, tipo e riassunto;
5. **embedding** con Qwen3-Embedding 0.6B verso Qdrant, insieme a BM25;
6. **reranker** Qwen3-Reranker 0.6B;
7. **MCP RAG**, con i permessi per utente e il registro delle domande, verso Claude Team.

Cosa sia esattamente Sirius è una domanda aperta per Michele ([domande per Michele, n. 25](../DOMANDE-PER-MICHELE.md)). Gli embedding si calcolano sulla GPU del server, quindi il contenuto non esce per essere indicizzato ([proposta §5.5](../PRESENTAZIONE-CEO.md)). Il board ha anche una pipeline dei bandi: n8n ogni notte, Firecrawl, un riassunto con il modello da 4B, indice e notifica in Teams o per mail ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)). Nel sistema di agenti i bandi li cerca ogni mattina l'Agente bandi, a L3 interno, dalla fase 3; la domanda di bando resta a una persona ([ricerca/45 §4.2](../ricerca/45-architettura-v3.md)).

Dalla fase 3 la squadra Memoria tiene viva la memoria: il Raccoglitore porta dentro posta, calendario, documenti, chat, testi, Jira, trascrizioni e CRM; il Pulitore deduplica, classifica, toglie i dati personali che non servono e separa il testo di terzi; il Bibliotecario risponde alle domande libere; l'Archivista applica le scadenze di conservazione ([proposta §4.7](../PRESENTAZIONE-CEO.md)). Raccoglitore, Pulitore e Bibliotecario lavorano nella corsia N; sui testi rossi Raccoglitore e Pulitore usano un modello in casa ([ricerca/45 §3.2](../ricerca/45-architettura-v3.md); [ricerca/49 §2.6](../ricerca/49-instradamento-a-piu-motori.md)).

### 5.3 Chi vede cosa

- **La persona arriva fino alla memoria.** Quando un agente lavora per Alessandro, la memoria gli mostra solo ciò che Alessandro può vedere ([proposta §5.3](../PRESENTAZIONE-CEO.md)). L'Agent SDK passa a ogni server MCP le intestazioni HTTP decise da noi, a ogni chiamata ([ricerca/36 §1.2](../ricerca/36-architettura-v2.md)).
- **Il token della persona.** Il runner firma un token a vita breve, con una chiave tenuta in Infisical, valido solo per l'MCP RAG. La persona è chi ha avviato il lavoro: l'identità Microsoft che arriva dalla Porta, o chi ha creato l'orario nella tabella del motore. Non è mai un campo scritto dal modello. Il risultato va solo a chi può vedere quei dati: nessuna risposta del lavoro di una persona finisce in un canale aperto a tutti ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md); [ricerca/35 §8](../ricerca/35-giudizio-sicurezza.md)).
- **Permessi per documento.** Qdrant ha chiavi per collezione, non per documento: i permessi fini li applica l'MCP RAG con filtri sui metadati di ogni blocco ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md)).
- **I numeri si calcolano, non si cercano.** Pipeline, margini e budget si calcolano dal codice sui dati di PostgreSQL, non si cercano nel testo ([proposta §5.5](../PRESENTAZIONE-CEO.md)).

### 5.4 Cosa arriva a Claude Team

Chiunque può chiedere anche da Claude Team "cosa ci siamo detti con X a settembre?" e avere la risposta con le fonti, vedendo solo ciò che può vedere ([proposta §5.5](../PRESENTAZIONE-CEO.md)). L'MCP RAG dà a Claude Team verde e giallo, e il rosso solo oscurato, finché parere e valutazione d'impatto non decidono. La collezione `finanza` è separata e si toglie a Claude Team con una regola ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md)). Pesa il fatto che Claude Team non tiene un registro delle attività che possiamo controllare ([proposta §13](../PRESENTAZIONE-CEO.md)). La corsia T non riceve mai dati rossi, neanche oscurati, e lavora solo su repo senza dati personali: sul piano Team la conservazione è di 30 giorni, senza la conservazione zero ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §4](../ricerca/49-instradamento-a-piu-motori.md)).

### 5.5 Quanto si conserva

- Audio fino a 30 giorni; trascrizioni e CRM 24 mesi dall'ultimo contatto; log degli agenti 90 giorni ([proposta §9.1, regola 8](../PRESENTAZIONE-CEO.md)). Anche il registro a sola aggiunta del Cancello si conserva 90 giorni ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- Le sessioni dell'SDK di default restano 30 giorni: il periodo si abbassa, i lavori con dati rossi non salvano la sessione e i dati stanno su un dataset cifrato di ZFS, il file system dei dischi del server ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- Una cancellazione su richiesta deve raggiungere le sessioni in PostgreSQL, Qdrant, Loki e i backup ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- Sul banco di prova, finché la fase di sicurezza F3 del board non è validata, si salvano solo dati verdi e gialli. Le trascrizioni si leggono da Graph, si oscurano in memoria con un filtro locale, vanno all'API e si conserva solo il riassunto ([proposta §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.7](../ricerca/36-architettura-v2.md)). L'oscuramento locale si costruisce e si misura nella fase 1 ([proposta §5.6](../PRESENTAZIONE-CEO.md)). Il testo rosso non passa da n8n e nessun dato rosso resta nei database, compreso quello di n8n se c'è ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md); [ricerca/45 §6.3](../ricerca/45-architettura-v3.md)).

---

## 6. Le reti

### 6.1 Le VLAN del board

Una VLAN è una rete separata che condivide i cavi con le altre: OPNsense decide chi parla con chi. Le regole chiave del board sono: tutto vietato salvo ciò che è permesso; LAB e PERSONAL non vedono DATA; APPS raggiunge AI solo sulle API dei modelli; AI raggiunge DATA solo su Qdrant; MGMT e OOB sono raggiungibili solo dal gruppo degli amministratori della mesh NetBird ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

| VLAN | Rete | Regola d'uscita | Cosa c'è |
|---|---|---|---|
| OOB · iLO | 10.10.11.0/24 | porta fisica dedicata, nessun internet | la rete "fuori banda", solo per la gestione: iLO 5, la scheda di gestione remota del server, raggiungibile solo dalla mesh degli amministratori |
| 10 MGMT | 10.10.10.0/24 | solo aggiornamenti dal proxy | interfaccia di Proxmox, rete e firewall di Proxmox; nella board del rack anche il backup in sede |
| 20 EDGE | 10.10.20.0/24 | in ingresso solo dal tunnel | Traefik con un certificato TLS wildcard (valido per tutti i sottodomini); nell'elenco anche Pangolin e NetBird |
| 30 APPS | 10.10.30.0/24 | uscita solo verso destinazioni in lista | n8n, mcp-enrich, mcp-memory, openoutreach, runner-dash, Homepage, LiteLLM, Open WebUI, MCP RAG, Firecrawl, bandi-watcher, draw.io, Excalidraw, BookStack |
| 40 DATA | 10.10.40.0/24 | nessun internet | PostgreSQL 16, MinIO, Qdrant, Vaultwarden, Infisical |
| 50 CICD | 10.10.50.0/24 | uscita solo verso GitHub e i registry | 4 runner di GitHub, ambienti di staging su richiesta |
| 60 VAULT | 10.10.60.0/24 | isolata: esce solo verso i servizi esterni che le servono | un servizio Windows del board che il sistema di agenti non usa |
| 70 OBSRV | 10.10.70.0/24 | legge da tutte, nessun internet | Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox |
| 80 AI | 10.10.80.0/24 | uscita solo per scaricare i modelli | `ai-gpu-01` (LXC): Ollama con Qwen3-4B, Infinity con embedding e reranker, Docling, worker di indicizzazione |
| 90 LAB | 10.10.90.0/24 | internet sì, nessun accesso a DATA | Experimental-1 (postazione di prova con la RTX 4000), Experimental-2 (sandbox Linux con Docker) |
| 99 PERSONAL | 10.10.99.0/24 | solo internet, nessuna rotta verso le altre | fuori dal perimetro Cyber Essentials |
| LAN ufficio | 192.168.50.0/24 | internet; verso i server solo via mesh | PC, access point, stampante |

Fonti: [elenco delle VLAN](../allegati/infra/board-vlan.txt); [board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md); [board del rack](../allegati/infra/Rack%20SerSan%2012U.md). Nella board del rack, più recente, il Wi-Fi e le porte LAN del router TIM, che fa da access point, stanno sulla VLAN 99 senza etichetta ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)). Experimental-1 e 2 sono lavoro, quindi stanno nel perimetro Cyber Essentials ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

### 6.2 Le VLAN proposte per gli agenti

| VLAN | Cosa ospita | Esposta su internet | Entra |
|---|---|---|---|
| 32 AGENTI | il motore, `agenti-01`; esce solo verso LiteLLM, `mcp-01`, MCP RAG e API del Cancello; dall'ingresso riceve solo `POST /eventi`. Se Michele lo decide, ospita anche il Cancello | no | fase 2 |
| 35 MEET | Vexa, `meet-01` | no: Vexa esce, non riceve | fase 3 |
| 25 VOCE | Asterisk, `voce-01` | solo il trunk SIP verso gli indirizzi dell'operatore | fase 5 |

Fonti: [ricerca/36 §3 e §4.5](../ricerca/36-architettura-v2.md); per `POST /eventi` e il Cancello, [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md) e [ADR-0023](adr/0023-protezioni-essenziali.md). Il sistema aggiunge in tutto 11-13 servizi e 3 reti nuove al perimetro Cyber Essentials ([proposta §13](../PRESENTAZIONE-CEO.md)). La VLAN 32 può diventare la 30, con il firewall di Proxmox per ogni VM, se Michele preferisce ([ricerca/36 §3](../ricerca/36-architettura-v2.md)).

### 6.3 Chi parla con chi

| Da | Verso | Cosa passa |
|---|---|---|
| Motore (32) | LiteLLM (30) | solo le chiamate ai modelli e al decisore |
| Motore | `mcp-01`, MCP RAG, API del Cancello (30) | HTTP interno con un token per famiglia di agenti; fra motore, Cancello e Porta un token per processo |
| Motore | internet | niente |
| LiteLLM | `api.anthropic.com` | HTTPS: le chiamate a Claude delle corsie N e S |
| LiteLLM | `ai-gpu-01` (80) | le API dei modelli in casa; il board permette già APPS → AI solo sulle API dei modelli |
| LiteLLM | TypeSafe e fornitori di modelli ammessi | HTTPS: Jev e i modelli open-weight esterni, solo dati verdi e gialli |
| `cancello-01` | Graph e login di Microsoft, Bot Framework, Jira, SersanOutreach, Instantly, Telegram, Meta, Slack | HTTPS: esecutori e Porta |
| `cancello-01` | API dei compiti di Claude Code, GitHub | HTTPS: l'avvio dei lavori della corsia T e la lettura delle consegne |
| EDGE (20) | `cancello-01` | messaggi dei bot |
| EDGE | motore (`POST /eventi`) | webhook dei servizi esterni, con un token per mittente |
| EDGE | MCP RAG | l'endpoint MCP per Claude Team, con OAuth di Entra (l'accesso delegato con l'identità Microsoft) |
| MCP RAG (30) | Qdrant (40) | regola nuova da scrivere: oggi il board ha solo "AI → DATA solo Qdrant" |
| `meet-01` (35) | internet | HTTPS e audio: i bot entrano nelle call; nessuna rotta verso DATA |
| `voce-01` (25) | indirizzi dell'operatore | SIP, meglio cifrato con TLS sulla porta 5061, e l'audio RTP |
| `stage-agenti` (90) | internet | HTTPS: API con chiave limitata, Graph, bot; nessun accesso a DATA |
| OBSRV (70) | tutte | sola lettura |

Fonti: [ricerca/36 §4.4](../ricerca/36-architettura-v2.md); [domande per Michele, n. 7](../DOMANDE-PER-MICHELE.md); per la v3, [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md), [ADR-0023](adr/0023-protezioni-essenziali.md), [ADR-0025](adr/0025-un-modello-per-agente.md), [ADR-0028](adr/0028-instradamento-a-piu-motori.md) e il [board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md) per la regola APPS → AI. Le regole vanno scritte con Michele su OPNsense e nel firewall di Proxmox ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)). Due punti sono nuovi. `POST /eventi` va esposto dietro la porta d'ingresso, quindi il motore riceve dall'ingresso ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)). E secondo [ricerca/49 §3.4](../ricerca/49-instradamento-a-piu-motori.md) è il motore a leggere GitHub ogni 5 minuti, in sola lettura; qui la lettura sta sul Cancello, perché il motore non ha internet: dove farla lo decide Michele.

### 6.4 Il trunk del rack e le porte del firewall

Un trunk è un collegamento che porta più VLAN insieme: ogni pacchetto ha un'etichetta (tag) con il numero della sua VLAN. Nella board del rack il firewall Sophos collega tutto così ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md); [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)):

| Porta del firewall | Verso | Cosa passa |
|---|---|---|
| E0 | ONT della fibra TIM | la WAN, con PPPoE (il login verso l'operatore) sulla VLAN 835; OPNsense fa da router |
| E1 | DL380, porta LOM 1 (la prima porta di rete sulla scheda madre) | il trunk con le VLAN 10, 20, 30, 35, 40, 50, 60, 70, 80, 85 e 90, con etichetta |
| E2 | DL380, iLO | la rete OOB 10.10.11.0/24, senza internet |
| E3 | backup in sede | VLAN 10, backup e Wake-on-LAN (l'accensione a distanza dalla rete) |
| E4 | router TIM come access point | VLAN 99 senza etichetta: Wi-Fi e porte LAN |
| E5 | scheda di rete dell'UPS | pagina web, SNMP (il protocollo per leggere lo stato degli apparati) e gruppi di prese dell'UPS |
| E6-E7 | nodo 2, più avanti | trunk e scheda di gestione, con moduli SFP (porte per moduli di rete intercambiabili) |
| USB | UPS | NUT: il Sophos legge l'UPS e ordina gli spegnimenti |

Più avanti il DL380 e il nodo 2 si collegano direttamente a 10 Gbit, per il cluster, la migrazione e la replica ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)). Il server ha 4 porte da 1 Gbit sulla scheda madre, una scheda 561FLR-T con 2 porte da 10 Gbit in rame e l'iLO 5 ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)).

Un punto da chiudere prima di mettere in rete il Sophos: E0 ed E1 sono una coppia con bypass LAN. Se il bypass scatta, a Sophos spento o bloccato, la fibra resta collegata direttamente al trunk del server. Le strade sono disattivare il bypass nel BIOS e provarlo a Sophos spento, oppure spostare la WAN su una porta senza bypass ([domande per Michele, n. 8](../DOMANDE-PER-MICHELE.md)).

### 6.5 Cosa si vede da internet

- **Nessuna porta aperta in ufficio.** Si entra solo con identità verificata: NetBird per persone e amministratori, con SSO di Entra, chiave FIDO2 e regole per gruppo; Pangolin e Traefik per le pagine web e per l'endpoint MCP di Claude Team ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)). NetBird funziona anche dietro il CGNAT di Starlink (l'operatore condivide un indirizzo pubblico fra molti clienti, quindi da fuori non si entra direttamente) ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).
- **Un solo endpoint MCP pubblico**, l'MCP RAG per Claude Team. Accetta solo token Entra del tenant SerSan con il destinatario giusto; il filtro sugli indirizzi di Anthropic (160.79.104.0/21) è un controllo in più, non un'autenticazione, perché quegli indirizzi sono di tutto il servizio Anthropic ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md); [domande per Michele, n. 6](../DOMANDE-PER-MICHELE.md)).
- **Il bot di Teams** sta dietro una risorsa Pangolin che lascia passare senza login solo il percorso `/api/messages`; la verifica la fa il token firmato del Bot Framework ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)).
- **TLS in passthrough**: la proposta è che Pangolin sulla macchina Oracle passi il traffico cifrato senza aprirlo, così si apre solo in casa ([domande per Michele, n. 4](../DOMANDE-PER-MICHELE.md)).
- **Mai pubblici**: Postiz e listmonk, raggiungibili solo da NetBird. n8n è pubblico solo sui webhook firmati, senza moduli pubblici. DocuSeal espone solo le pagine di firma ([ricerca/36 §4.5](../ricerca/36-architettura-v2.md)).
- **Gli amministratori** usano gli MCP da Claude Desktop attraverso la mesh, senza esporre nulla ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).
- **Gli apparati di gestione** (il modulo di rete dell'UPS, l'iLO e la scheda 561FLR-T) non devono essere raggiungibili da internet ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)).

---

## 7. L'infrastruttura

### 7.1 Le sedi: Cagliari, Terra Noa, Milano

| Sede | Cosa c'è | Fonte |
|---|---|---|
| **Cagliari, ufficio** | Il rack da 12U con il server, il firewall e l'UPS; presto il backup in sede, più avanti il secondo server | [proposta §6.1](../PRESENTAZIONE-CEO.md) |
| **Terra Noa, casa di Michele** | Da marzo 2027 la copia cifrata dei backup, ogni notte, su un piccolo nodo del board che ospita la copia su un disco interno e fa anche da firewall della rete di Terra Noa. Più avanti un Proxmox Backup Server più grande | [proposta §6.1 e §12.2](../PRESENTAZIONE-CEO.md) |
| **Oracle Cloud, Milano** | Una macchina per l'accesso da fuori: NetBird (gestione e relay), Pangolin, Uptime Kuma e ntfy | [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md) |

**Due zone, non un cluster unico.** Un cluster Proxmox vuole una rete con pochi millisecondi di latenza e senza interruzioni. Starlink, che collega Terra Noa, ha 25-60 ms, sbalzi e brevi cadute: un cluster stirato fra le due sedi perderebbe spesso il quorum, cioè la maggioranza di voti che serve al cluster per restare attivo. Per questo c'è una zona per sito: il cluster "cagliari" in ufficio e un nodo singolo a Terra Noa. Proxmox Datacenter Manager, sul Sophos, le gestisce tutte da un'interfaccia e sposta le VM da una zona all'altra; il backup si sincronizza ogni notte da Cagliari a Terra Noa; NetBird collega tutto in una rete privata ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)). Terra Noa è collegata a internet con Starlink ([ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)).

### 7.2 Il server

| Componente | Cosa c'è |
|---|---|
| Server | HPE ProLiant DL380 Gen10, due Intel Xeon Gold 5218 (64 thread in tutto), nodo 1 di Proxmox |
| Memoria | 192 GB DDR4 ECC: 12 moduli da 16 GB a 2133 MHz, uno per canale |
| Dischi | 2 SSD SAS da 800 GB in mirror per il sistema; 6 HDD SAS da 1,8 TB in tre mirror, circa 5,4 TB per i dati. Un mirror tiene gli stessi dati su due dischi: se uno si rompe, l'altro continua |
| GPU | NVIDIA Quadro RTX 4000 da 8 GB, nel riser principale (il supporto che ospita le schede aggiuntive), che con il controller dei dischi è già pieno |
| Raffreddamento e corrente | Ventole e dissipatori ad alte prestazioni, due alimentatori da 800 W Titanium |

Fonti: [proposta §6.1](../PRESENTAZIONE-CEO.md); per il ruolo di nodo 1, [board del rack](../allegati/infra/Rack%20SerSan%2012U.md). Nel board i due gruppi di dischi si chiamano `rpool` (gli SSD) e `tank` (gli HDD), su ZFS, e il server ha un chip TPM 2.0, che custodisce le chiavi di cifratura ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

### 7.3 La RAM

Il board lascia circa 53 GB liberi. Il pilota ci sta largo; con memoria e call (fase 3) si arriva al limite; con tutte le funzioni (fasi 5-6) mancano circa 20 GB ([proposta §6.3](../PRESENTAZIONE-CEO.md)):

| | Fase 1 | Fase 2 | Fasi 3-4 | Fasi 5-6 |
|---|---|---|---|---|
| GB usati dal sistema di agenti | 8 | 25 | 53,5 | 70-74 |
| GB liberi con 192 GB | circa 45 | circa 28 | circa 0 | da -17 a -21 |
| GB liberi con 384 GB | | | circa 191 | circa 171-175 |

Le voci più pesanti sono il motore (fino a 20 GB), Vexa (12 GB per tre bot) e la trascrizione (6-8 GB) ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md)). Con la v3 queste cifre non cambiano: il peso del motore viene dalle sessioni della corsia S, mentre la corsia N pesa poco ([ricerca/45 §3.3](../ricerca/45-architettura-v3.md); [ADR-0015](adr/0015-ram-384-gb.md)).

**La regola d'acquisto.** Si misura con un tetto iniziale di 6 sessioni S. Si aggiungono altri 192 GB prima della fase 3 (settimana 22), o prima se il margine misurato scende sotto i 5 GB: 12 moduli da 16 GB uguali a quelli montati, uno in più per ogni canale. È l'unico passo che tiene la memoria bilanciata, e la velocità resta quella di oggi. Costa circa 690-830 € ([proposta §6.3 e §13](../PRESENTAZIONE-CEO.md); per il tetto di 6 sessioni, [ricerca/36 §4.2](../ricerca/36-architettura-v2.md)). Nella proposta era la decisione 11 dei CEO; dal 10 novembre tempi e acquisto li decidono il gruppo di progetto e Michele. Siccome la corsia S arriva subito dopo la milestone 1, il margine va misurato appena il runner gira sul server ([ADR-0015](adr/0015-ram-384-gb.md), revisione del 10 novembre). La RAM non va anticipata per i modelli locali, salvo un caso: se la prova sceglie un modello grande con una parte in RAM per i lavori notturni, servono circa 20 GB in più, e allora conviene comprarla prima della fase 3 ([ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md)).

**Leve per rimandare l'acquisto** ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md)): Experimental-1 e 2 accese solo quando servono (24 GB); un tetto di 12 sessioni; Andrea sulla seconda GPU (4 GB in meno); Vexa Lite con una call alla volta (circa 4 GB invece di 12).

**Cento agenti.** La RAM cresce con le sessioni attive insieme, non con il numero di profili: cento profili con un tetto di 16 sessioni stanno nei 20 GB del motore ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md)).

**Note per chi monta** ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md); [domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)):

- la cache ZFS va fissata con `zfs_arc_max` a 12 GiB, per restare nei 16 GB che il board dà all'host e alla cache;
- servono moduli x4 come quelli montati (16 GB 2Rx4 PC4-2133P RDIMM): con moduli x8 HPE spegne online spare, mirroring e Fast Fault Tolerance;
- i nuovi moduli vanno negli slot 2, 4, 6, 7, 9 e 11 di ogni CPU; dopo il montaggio, memtest86+ per 24 ore. L'iLO può segnalare che non sono SmartMemory HPE, cosa normale con moduli Gen9.

### 7.4 Le GPU

**Oggi, la RTX 4000.** Di giorno, con Qwen3-4B, embedding, reranker e Docling, le resta meno di 1 GB libero; la trascrizione dal vivo (circa 2,1 GB) ci entra solo se il reranker passa sulla CPU ([ricerca/36 §4.3](../ricerca/36-architettura-v2.md)). Michele la presta ogni tanto, per poco tempo, alla postazione di prova del laboratorio (Experimental-1): intanto i lavori della GPU aspettano in coda finché torna libera ([proposta §6.4](../PRESENTAZIONE-CEO.md)). Embedding e lavori a lotti possono girare sulla CPU quando serve ([proposta §13](../PRESENTAZIONE-CEO.md)).

**La seconda GPU.** Michele ha scelto la **RTX PRO 2000 Blackwell da 16 GB**: 70 W senza cavi di alimentazione e memoria più veloce della generazione precedente. Con 16 GB ci stanno insieme la trascrizione dal vivo, la voce di Andrea e la ricerca nella memoria, giorno e notte ([proposta §6.4](../PRESENTAZIONE-CEO.md)).

- **Quando.** La proposta la consigliava dalla fase 3 (settimana 22), quando si trascrivono in casa le call dei clienti e la RTX 4000 è quasi piena, e al più tardi all'inizio della fase 5 (settimana 41), prima di spostare Andrea sulla GPU ([proposta §6.4](../PRESENTAZIONE-CEO.md)). Oggi la proposta a Michele è comprarla per la milestone 2, quella del primo modello open-weight: la prova dei modelli locali ne ha bisogno, perché la RTX 4000 ha meno di 1 GB libero e alcuni modelli da provare girano solo sulla Blackwell. Serve il sì di Michele ([ADR-0014](adr/0014-seconda-gpu-blackwell.md), seconda revisione del 10 novembre; [ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md)).
- **Prezzo.** Alla data della proposta in Italia costava circa 1.290-1.305 € IVA inclusa (circa 1.060 € esclusa), e la proposta suggeriva di comprarla sotto i 1.000 € IVA inclusa (circa 820 € esclusa); con riser e staffa la decisione 12 valeva circa 880-1.220 € ([proposta §6.4 e §14](../PRESENTAZIONE-CEO.md)). Il 10 novembre il prezzo al pubblico era di 1.100 € su Amazon.it, con una mediana di 984 € negli ultimi 12 mesi: la proposta di oggi è comprarla anche a quel prezzo, senza aspettare la soglia ([ADR-0014](adr/0014-seconda-gpu-blackwell.md), seconda revisione del 10 novembre).
- **Cosa ci sta.** Con la scheda da 16 GB e la RTX 4000 girano insieme trascrizione, voce di Andrea, ricerca nella memoria, un modello piccolo e un modello da 9 miliardi di parametri che vede le immagini. Quest'ultimo sta sugli 8 GB della RTX 4000 al limite e va misurato [stima] ([ADR-0014](adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §5.2](../ricerca/48-modelli-locali-e-gpu.md)). I modelli sul server fanno da occhi e orecchie, non da orchestratore: un modello che ascolta e vede tutto al centro non porterebbe niente che serva alle squadre ([ricerca/48 §3](../ricerca/48-modelli-locali-e-gpu.md)).
- **Cosa non comprare ora.** Né la scheda da 24 GB a 70 W, che costa più di tre volte tanto (circa 3.750-4.100 €), né una scheda più grande con il cavo di alimentazione: con una scheda da 140-230 W un solo alimentatore non basta più e il server perde la ridondanza. Se la prova chiede un modello più grande in casa, si sostituisce la RTX 4000 o si fa un nodo pensato per la GPU, con il suo budget ([ADR-0014](adr/0014-seconda-gpu-blackwell.md), seconda revisione del 10 novembre).
- **Montaggio.** La scheda occupa due slot e va nel riser secondario, che costa circa 75-160 € con IVA e spedizione se non c'è già. La versione PNY venduta al dettaglio ha già la staffa ad altezza piena; con le altre la staffa costa circa 20 € ([proposta §6.4](../PRESENTAZIONE-CEO.md)). Va nello slot 5 (x16) e copre lo slot 4 ([domande per Michele, n. 17](../DOMANDE-PER-MICHELE.md)).
- **Supporto.** HPE non certifica due GPU di modelli diversi nello stesso server: la garanzia della scheda resta quella del venditore. Prima di spostare la trascrizione si prova che i programmi girano sulla nuova architettura ([proposta §6.4](../PRESENTAZIONE-CEO.md)).
- **Software.** Driver Linux 580.76.05 o successivo con i moduli open, valido anche per la RTX 4000; CTranslate2 e faster-whisper, i programmi della trascrizione, vanno provati, con la cache CUDA (la piattaforma di calcolo delle GPU NVIDIA) su un volume persistente; l'immagine di trascrizione di Vexa va ricostruita su CUDA 12.8 o successivo ([domande per Michele, n. 18](../DOMANDE-PER-MICHELE.md)). La scheda è collegata alla CPU 2: niente modelli divisi fra le due GPU, e i suoi servizi vanno legati alla CPU 2 e alla sua memoria (il nodo NUMA) ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)).

### 7.5 Rack, firewall, UPS e corrente

**Il rack.** È un VEVOR da 12U a quattro montanti, nell'ufficio di Cagliari ([ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)). Dal basso: l'UPS in U1, il DL380 in U2-3, il backup in sede in U4-5, il nodo 2 in U6-7 (più avanti), il Sophos in U8, montato girato con le porte verso il retro, e sul ripiano l'ONT e il router TIM ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)).

**Il firewall.** Un Sophos SG 230 rev. 2 da rack, in arrivo. Michele non usa il software Sophos: ci mette Proxmox con OPNsense e i servizi di rete, aggiornati dai loro progetti ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Il Proxmox del Sophos resta fuori dal cluster e fa girare OPNsense in una VM e, in container, NetBird, AdGuard con Unbound (il DNS con i filtri), NUT e più avanti il QDevice ([ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)). Il QDevice è il terzo voto per il quorum del cluster ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)): quando arriva il secondo server, se uno dei due si ferma l'altro continua da solo ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Note per chi lo configura ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)):

- OPNsense in VM con schede di rete virtuali (virtio) su bridge: le porte stanno dietro uno switch PCIe, che può impedire di passare alla VM una singola porta;
- alla VM almeno 8 GB, senza ballooning (Proxmox non deve toglierle RAM mentre gira);
- c'è un solo SSD: la configurazione di OPNsense e del Proxmox del Sophos va salvata sul backup;
- il QDevice è un container Debian con corosync-qnetd, con la porta TCP 5403 aperta dai due nodi.

Il Sophos SG 230 rev. 2 non è più supportato da Sophos dal 30 giugno 2026, e BIOS e processore non ricevono più correzioni: per Cyber Essentials si chiede prima all'ente di certificazione (paragrafo 8.2) ([proposta §6.1](../PRESENTAZIONE-CEO.md)).

**La fibra.** TIM a 2,5 Gbit, che sulle porte del firewall lavora a circa 1 Gbit ([proposta §6.1](../PRESENTAZIONE-CEO.md)); in pratica circa 940 Mbit/s, che bastano ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)). Se un giorno servirà di più, un modulo di rete più veloce costa circa 420-500 €, come spesa del board ([proposta §12.2](../PRESENTAZIONE-CEO.md)).

**L'UPS.** Un HPE R1500 G5 da rack (1.550 VA, 1.100 W), in arrivo. Se manca la corrente, dopo 3 minuti spegne il server in modo pulito e tiene accesa la rete fino a fine batteria. Al ritorno della corrente la rete, se si era spenta, riparte da sola; il server, com'è impostato oggi, va riacceso a distanza ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Con i lavori L3 di notte questo non basta: la riaccensione automatica dopo un blackout è il primo passo consigliato a Michele (paragrafo 7.9). Come sono collegate le prese ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)):

- **gruppo primario**, sempre acceso: il Sophos, la ciabatta con ONT e router TIM, il backup in sede;
- **gruppo 1**, staccato dopo lo spegnimento: i due alimentatori del DL380;
- **gruppo 2**: il nodo 2, più avanti;
- **gestione**: la scheda di rete dell'UPS sulla porta E5 e l'USB al Sophos per NUT (Network UPS Tools, il programma che legge l'UPS e ordina gli spegnimenti).

Le batterie montate sono usate e senza garanzia: all'arrivo si fa un test di autonomia, e se va male le batterie nuove costano circa 140-550 € ([proposta §12.2](../PRESENTAZIONE-CEO.md)). Con la seconda GPU e 384 GB il picco stimato è di 860-945 W fra server, firewall e rete: l'UPS regge, con 6-7 minuti di autonomia al picco. Con il nodo 2 i due server al picco possono superare i 1.100 W: a Michele chiediamo se mettere un tetto di potenza dall'iLO o prendere un secondo UPS ([domande per Michele, n. 20](../DOMANDE-PER-MICHELE.md)).

**La corrente.** La corrente del rack, cioè server, firewall, UPS, rete e backup in sede, è stimata con prudenza a 400 W, circa 105 € al mese ([proposta §12.1](../PRESENTAZIONE-CEO.md)). Il carico realistico di oggi è di 250-300 W, e quello vero si legge sul display dell'UPS o con un wattmetro ([ricerca/37 §3 e §4](../ricerca/37-hardware-risposte-michele.md)).

### 7.6 Il backup 3-2-1

La regola 3-2-1 chiede tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio ([proposta §6.1](../PRESENTAZIONE-CEO.md)).

| Copia | Dove | Stato |
|---|---|---|
| 1 | I dati sul DL380 | in casa |
| 2 | Un Proxmox Backup Server (PBS) in sede, nel rack, che Michele monta con pezzi suoi; acceso di notte con Wake-on-LAN | mancano case e dischi: circa 165-500 € |
| 3 | A Terra Noa, a casa di Michele: ogni notte una copia cifrata | entro marzo 2027: il nodo costa circa 240-250 €; più avanti un PBS più grande, circa 690-930 € |
| facoltativa | uno spazio S3 fuori sede | da decidere |

Fonti: [proposta §5.2, §6.1, §12.2 e §14, decisione 4](../PRESENTAZIONE-CEO.md); [board del rack](../allegati/infra/Rack%20SerSan%2012U.md). Il PBS in sede usa una scheda MSI H110M, un processore i3 o i5 e i 2 × 4 GB di RAM tolti dal Sophos, con 2 dischi da 500 GB in mirror ([ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md)).

**La proposta di disegno**, da confermare con Michele ([domande per Michele, n. 14](../DOMANDE-PER-MICHELE.md)):

- il PBS di Terra Noa tira i backup dal PBS in sede (pull), con un utente che in sede ha solo lettura, senza propagare le cancellazioni ("remove vanished" spento) e solo con gli snapshot cifrati;
- il token del Proxmox verso il PBS in sede ha il solo ruolo DatastoreBackup: aggiunge backup ma non li cancella;
- una sola chiave di cifratura, custodita fuori da casa di Michele;
- verifica ogni giorno, riverifica completa ogni mese, prova di ripristino ogni trimestre, con verbale.

Così chi prendesse il controllo dell'ufficio non avrebbe le credenziali per cancellare la copia di Terra Noa ([ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)).

**Spazio.** 2 × 500 GB in mirror bastano all'inizio, non per tutte le VM del server: si misura l'occupato vero e si passa a 2 × 4 TB quando supera circa 400 GB. A Terra Noa va chiarito se basta il disco interno del nodo o se serve un disco in più ([domande per Michele, n. 15](../DOMANDE-PER-MICHELE.md)).

**Due supporti.** Se i due PBS usano entrambi dischi rigidi, la regola è rispettata per numero di copie e per la copia fuori sede, ma non alla lettera per i due tipi di supporto: il secondo tipo lo darebbe un disco USB tenuto staccato o lo spazio S3 facoltativo ([ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)).

**I vincoli del piano.** Nella fase 0 una copia dei dati di SersanOutreach esce dai suoi cloud, per esempio sul backup in sede, con una prova di ripristino riuscita ([proposta §7.4](../PRESENTAZIONE-CEO.md)). Nessun dato dei clienti resta sul server prima della verifica della settimana 21, che chiede il 3-2-1 in funzione con una prova di ripristino ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)).

### 7.7 La macchina Oracle e la linea internet

**La macchina Oracle.** Michele ha scelto Oracle Cloud a Milano per NetBird, Pangolin e il monitoraggio da fuori. Costa 0 € sul piano gratuito di Oracle, 6,49 € al mese se servisse un server a pagamento (decisione 7) ([proposta §14](../PRESENTAZIONE-CEO.md)). Il piano gratuito ha due limiti: Oracle si riprende le macchine che per 7 giorni restano sotto il 20% di CPU, rete e memoria, e Milano ha una sola zona. Alla registrazione va scelta Milano come regione di casa, che poi non si cambia ([domande per Michele, n. 4](../DOMANDE-PER-MICHELE.md)).

**Una sola linea internet.** Se cade la fibra, gli agenti che ragionano con Claude via internet si fermano, e Andrea non risponde. Nulla si perde: lavori e carte aspettano e ripartono quando la linea torna. La proposta consigliava la linea di riserva 4G/5G prima della fase 5 (decisione 13); l'accesso da fuori passa dalla macchina Oracle e funziona anche sulla linea di riserva ([proposta §13](../PRESENTAZIONE-CEO.md)). Oggi la linea si anticipa: va messa prima del primo lavoro L3 verso l'esterno fuori orario e prima di Andrea, cioè in pratica all'inizio della fase 3. Con i livelli follow-up, richiamate e lavori a orario partono senza nessuno in ufficio, e una caduta della fibra li fermerebbe ([ADR-0019](adr/0019-linea-di-riserva.md), revisione del 10 novembre). Costa 77-200 € una tantum e 10-11 € al mese; Starlink (349 € e 31 € al mese) solo se in ufficio il segnale mobile è scarso ([proposta §14](../PRESENTAZIONE-CEO.md)).

### 7.8 Il secondo server e la durata dell'hardware

Michele prevede il secondo server già a dicembre, se c'è il budget (fino a 1.500 €): con il DL380 forma un cluster ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Si collega al DL380 con un cavo diretto a 10 Gbit ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)). È una spesa del board, decisa a parte ([proposta §12.2](../PRESENTAZIONE-CEO.md)).

Il supporto HPE per lo chassis dura fino a ottobre 2029 secondo le fonti ufficiali HPE consultate da Michele; le fonti pubbliche danno stime da marzo 2028 a ottobre 2029, quindi la data si conferma con il numero di serie. Il sistema gira comunque in macchine virtuali con backup: si sposta su un server nuovo senza rifare nulla ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Il secondo nodo può ospitare Cancello e Porta separati dal motore, o fare da riserva fredda: la scelta è di Michele ([ricerca/45 §11](../ricerca/45-architettura-v3.md)).

### 7.9 L'hardware per l'autonomia

Con i livelli molto lavoro parte quando in ufficio non c'è nessuno. Per questo [ricerca/45 §11](../ricerca/45-architettura-v3.md) consiglia a Michele un ordine preciso:

| Cosa | Quando | Costo | Cosa sblocca |
|---|---|---|---|
| Riaccensione automatica dopo un blackout (impostazione del BIOS o dell'iLO) | subito, prima del primo lavoro L3 notturno sul banco | 0 € | debrief e catene ripartono senza nessuno in ufficio |
| Test delle batterie dell'UPS | all'arrivo | 140-550 €, se il test va male | lo spegnimento ordinato regge e nessuna catena si perde a metà |
| Backup 3-2-1, con il PBS in sede | fase 2, prima dei dati dei clienti | 165-500 € subito; 240-250 € entro marzo 2027 | i dati dei clienti stanno sul server dopo la settimana 21 |
| Linea di riserva 4G/5G | prima del primo L3 esterno fuori orario e prima di Andrea | 77-200 €, più 10-11 € al mese | follow-up, richiamate e lavori a orario continuano anche se cade la fibra |
| RAM: altri 192 GB | all'inizio della fase 3, o prima se il margine scende sotto i 5 GB | 690-830 € | Vexa nelle call di altri, 12-16 sessioni S, crescita verso cento agenti |
| Seconda GPU da 16 GB | per la milestone 2 (paragrafo 7.4) | 1.100 €, prezzo al pubblico del 10 novembre, più il riser se manca (75-160 €) | prova dei modelli locali, trascrizione senza code, voce di Andrea |

I primi quattro rendono affidabile il lavoro L3 quando non c'è nessuno; gli ultimi due ne allargano il volume ([ricerca/45 §11](../ricerca/45-architettura-v3.md)). La seconda GPU nella tabella di ricerca/45 veniva dalla fase 3; con [ADR-0014](adr/0014-seconda-gpu-blackwell.md) e [ricerca/48 §5.5](../ricerca/48-modelli-locali-e-gpu.md) passa alla milestone 2.

---

## 8. Sicurezza e conformità

### 8.1 Le difese del disegno

I cinque meccanismi di controllo della proposta restano, adattati ai livelli ([proposta §9.2](../PRESENTAZIONE-CEO.md); [ADR-0023](adr/0023-protezioni-essenziali.md)):

1. **Gli agenti propongono, il codice esegue.** Nessun agente ha in mano un bottone che invia, pubblica, paga o cancella: passa sempre dal Cancello, al livello della sua terna. La macchina degli agenti raggiunge solo i servizi in lista, e nessun bot entra nei canali condivisi con i clienti.
2. **Le automazioni nascono spente.** Ogni automazione parte in prova a secco: per una o due settimane mostra cosa avrebbe fatto, senza farlo.
3. **Il testo di terzi non è mai un'istruzione.** Email, trascrizioni, pagine web e risposte dei prospect entrano da una corsia senza strumenti; nella corsia N entrano solo come campi, e i destinatari li sceglie il codice.
4. **Tetti che fermano davvero.** Ogni agente e ogni catena di lavoro ha un budget: avviso all'80%, stop al 100%. In più ci sono i tetti di quantità per classe al giorno e il freno delle catene.
5. **Tutto è registrato e revocabile.** Registro delle azioni a sola aggiunta, segreti oscurati prima di qualsiasi log, «Annulla» e «Rettifica», stop di emergenza dal telefono.

**Le protezioni essenziali.** SerSan Agent OS è un sistema aziendale chiuso: quattro persone, rete interna, accesso da fuori solo attraverso NetBird e Pangolin. I rischi veri sono il destinatario sbagliato e il doppio invio. Per questo la v3 tiene le protezioni che servono contro questi rischi e toglie quelle oltre l'essenziale ([ADR-0023](adr/0023-protezioni-essenziali.md)).

- **Restano**: i limiti fissi nel codice; il Cancello unico esecutore, con l'outbox (si registra prima dell'effetto, l'effetto esce una volta sola, un esito «incerto» va a una persona); lo stop di emergenza; i tetti; il registro a sola aggiunta, conservato 90 giorni; «Annulla» e «Rettifica»; un token per processo fra motore, Cancello e Porta, con i ruoli separati del database; la conformità minima, cioè riga AI, lista di soppressione unica, tre colori dei dati, riga nel registro dei trattamenti per ogni agente nuovo e parere legale con un tetto di 2.500 €; le prove a ogni modifica, con un comando e gratis, che sono l'unica revisione obbligatoria, più la revisione del codice di Mattia.
- **Escono**: la chiave FIDO2 come secondo passo sulle carte, che resta per l'accesso al board con NetBird; le firme HMAC fra i processi; il registro a catena; i codici per consegna e l'impronta della Porta, mentre resta l'impronta del testo ricalcolata dall'esecutore; la revisione esterna obbligatoria; la macchina separata obbligatoria per il Cancello.

Se un cliente o una certificazione chiedono di più, le difese tolte sono descritte nella revisione 2 dello spec e si possono rimettere ([ADR-0023](adr/0023-protezioni-essenziali.md)).

Il disegno aggiunge:

- **Reti strette**: agenti in una VLAN propria senza internet, web solo da Firecrawl, un solo endpoint MCP pubblico ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)). Il Cancello può stare nella stessa VM del motore, se Michele lo decide ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- **LiteLLM come bene critico.** Custodisce tutte le chiavi, e a marzo 2026 ne sono circolate versioni compromesse. Per questo: versione fissata e controllata, pannello raggiungibile solo dalla rete di gestione, chiave principale fra i segreti, con rotazione ([proposta §13](../PRESENTAZIONE-CEO.md)). La proposta voleva l'uscita solo verso Anthropic; oggi LiteLLM esce anche verso i modelli in casa, verso Jev e verso i fornitori ammessi, sempre con la regola dei colori ([ADR-0004](adr/0004-litellm-banca-token.md), revisioni del 10 e dell'11 novembre; [ADR-0025](adr/0025-un-modello-per-agente.md)).
- **Versioni fissate** e aggiornamento dell'SDK ogni due settimane, dopo i dieci scenari, entro i 14 giorni ([proposta §13](../PRESENTAZIONE-CEO.md)). Anche Jev e i modelli hanno la versione fissata: cambiarla è un cambio di modello, e senza una valutazione le terne che ne dipendono tornano a L1 ([ADR-0027](adr/0027-decisore.md)).
- **Il decisore non toglie prudenza.** Una sua risposta non alza mai un livello e non sceglie mai un destinatario esterno; una mail scritta per ingannarlo può al massimo mandare un'azione in carta ([ADR-0027](adr/0027-decisore.md)).
- **La corsia T sta in un recinto.** Sulle macchine di Anthropic i ganci del Cancello non entrano nella sessione; li sostituiscono i limiti di configurazione: nessun connettore, rete «Limited», solo repo ammesse, `main` protetto senza eccezioni, nessuna modifica ai workflow di GitHub, nessun segreto di produzione, regole di permesso nella repo. L'unico effetto possibile è una pull request, e nessun codice entra in `main` senza il sì di una persona ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §3.5](../ricerca/49-instradamento-a-piu-motori.md)).
- **Revisione esterna.** La proposta chiedeva che una società esterna rivedesse Cancello, motore e bot entro la settimana 21, prima che i dati dei clienti restassero sul server (decisione 5) ([proposta §5.4 e §14](../PRESENTAZIONE-CEO.md)). Oggi è facoltativa: si fa se un cliente la chiede. Si risparmiano da 3.560 a 5.940 € ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- **Banco di prova separato.** Nelle settimane 5-8 il pilota gira su una macchina di prova nella rete del laboratorio, con una chiave API limitata e un tetto di spesa, e salva solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata ([proposta §11](../PRESENTAZIONE-CEO.md)).
- **La fase F3 del board** porta Wazuh, NetBox, Authentik (gestione delle identità), CrowdSec (blocco degli indirizzi che attaccano), log e avvisi, e la documentazione per ISO e Cyber Essentials ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)). Wazuh scansiona le vulnerabilità di ogni VM e container ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).

### 8.2 Cyber Essentials

Cyber Essentials è la certificazione britannica di sicurezza di base, con i requisiti dell'NCSC; il board la prevede, con la documentazione nella fase F3 ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)). I requisiti in vigore sono la versione 3.3, con il questionario Danzell ([domande per Michele, n. 12](../DOMANDE-PER-MICHELE.md)). I controlli sono cinque: firewall, configurazione sicura, aggiornamenti, controllo degli accessi e protezione dal malware. Per i server vuol dire: aggiornamenti critici o ad alto rischio entro 14 giorni, account separati per l'amministrazione, MFA dove disponibile ([ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)).

Cosa significa per l'architettura:

- **Il perimetro cresce.** Il sistema aggiunge 11-13 servizi e 3 reti nuove al perimetro, con le patch entro 14 giorni. Ogni servizio ha un responsabile delle patch e un posto nell'inventario; prima della fase F4 entrano solo i servizi del pilota ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **I telefoni che approvano** entrano nel perimetro, anche se personali: sistema supportato, blocco schermo, MFA, aggiornamenti ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- **I servizi cloud** (M365, console e API di Anthropic, Oracle) sono sempre nel perimetro, con l'MFA obbligatoria. Anche il PBS a casa di Michele probabilmente rientra ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)).
- **Le chiavi FIDO2** restano per l'accesso al board con NetBird, anche se non servono più sulle carte ([ADR-0023](adr/0023-protezioni-essenziali.md)).
- **Il firewall fuori supporto.** Sul Sophos il software (Proxmox e OPNsense) è aggiornato, ma BIOS e processore no. Si chiede prima per iscritto all'ente di certificazione se accetta questa configurazione; se non la accetta, OPNsense passa su un piccolo computer ancora supportato dal produttore, con una spesa da preventivare ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **Il processore del server.** Per la Gold 5218 il rischio è più basso: Intel ha chiuso il servizio generale il 30/06/2025, ma HPE aggiorna ancora la System ROM, il firmware del server (3.70 di agosto 2026) ([domande per Michele, n. 12](../DOMANDE-PER-MICHELE.md)).
- **Le versioni di Proxmox.** Proxmox VE 8 (PVE, il sistema delle macchine virtuali) e PBS 3 sono a fine vita da agosto 2026: tutte le macchine vanno su PVE 9 e PBS 4. Il repository senza abbonamento è sconsigliato in produzione; gli abbonamenti per firewall e backup sono la decisione 17 ([domande per Michele, n. 13](../DOMANDE-PER-MICHELE.md); [proposta §14](../PRESENTAZIONE-CEO.md)).

### 8.3 GDPR e dati personali

Il GDPR è il regolamento europeo sulla protezione dei dati personali.

- **Minimizzazione prima del cloud**: si oscura ciò che non serve; solo fornitori con contratto commerciale e DPA ([proposta §9.1, regola 7](../PRESENTAZIONE-CEO.md)). I tre colori dei dati sono scritti nel codice, e il colore si calcola prima di chiamare un modello (paragrafo 1.5). I fornitori terzi di modelli ricevono solo dati verdi e gialli; Jev, servizio negli USA, riceve i gialli solo se Michele ammette il fornitore; la corsia T non riceve mai il rosso ([ADR-0025](adr/0025-un-modello-per-agente.md); [ADR-0027](adr/0027-decisore.md); [ADR-0028](adr/0028-instradamento-a-piu-motori.md)).
- **Lista di soppressione unica**: un «no» di un contatto blocca le azioni verso di lui su tutti i canali, e una risposta che chiede di non essere più contattati fa scendere la terna ([proposta §9.1, regola 5](../PRESENTAZIONE-CEO.md); [ADR-0023](adr/0023-protezioni-essenziali.md); [ADR-0020](adr/0020-autonomia-a-livelli.md)).
- **Destinatari stretti all'indirizzo esatto.** La classe «persona appena incontrata» vale solo per chi era nella call registrata e avvisata, mai per il dominio: il Garante applica l'art. 130 anche agli indirizzi aziendali ([ricerca/45 §2.2](../ricerca/45-architettura-v3.md)).
- **Registro dei trattamenti e valutazione d'impatto** (DPIA), aggiornati a ogni nuovo agente, compresi i brief prima degli incontri, che sono profilazione ([proposta §9.1, regola 9](../PRESENTAZIONE-CEO.md)). La prima versione si fa nella fase 0, con la decisione sui dati rossi verso Claude Team entro la settimana 3 ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)).
- **Conservazione con scadenze automatiche** (paragrafo 5.5) ([proposta §9.1, regola 8](../PRESENTAZIONE-CEO.md)).
- **Trasferimenti negli USA**: con tutto sul server, l'audio delle call e la voce di Andrea non passano più da fornitori negli USA ([proposta §5.6](../PRESENTAZIONE-CEO.md)). Ad Anthropic si chiede la conservazione zero dei dati delle API, che è gratuita ([proposta §14](../PRESENTAZIONE-CEO.md)).
- **Backup.** Il GDPR (art. 32) chiede di saper ripristinare i dati in tempo e di provarlo con regolarità: da qui le prove di ripristino con verbale ([domande per Michele, n. 14](../DOMANDE-PER-MICHELE.md); [ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)). Per la copia a casa di Michele serve la sua designazione scritta come autorizzato e amministratore di sistema, con i log degli accessi per almeno sei mesi ([domande per Michele, n. 16](../DOMANDE-PER-MICHELE.md)). Con dati cifrati e chiave custodita altrove, il furto della macchina di norma non va notificato ([ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)).
- **Il parere legale**, in due consegne: entro la settimana 3 i punti del pilota (email B2B verso l'Italia, registrazione delle call, trasferimenti verso gli USA), prima della fase 2 il resto. Fra i punti: come si applica il GDPR europeo a una Ltd con il team in Italia, i dati personali che possono arrivare a Claude Team, il valore legale della firma elettronica fatta in casa e la copia cifrata dei backup a casa di Michele ([proposta §9.4](../PRESENTAZIONE-CEO.md)). Con la v3 il tetto resta di 2.500 € e le domande crescono: se follow-up e recap alla persona incontrata possono partire a L2 e a L3, con quale riga AI, e se un messaggio L2, che una persona poteva fermare, vale come approvato o come scritto da solo ([ricerca/45 §2.8 e §9.1](../ricerca/45-architettura-v3.md)). Se il parere chiude una porta, la funzione resta e la sua classe rimane a L1 ([ricerca/45 §2.8](../ricerca/45-architettura-v3.md)).

### 8.4 AI Act

- Ogni agente che parla o scrive da solo a un esterno, come Andrea, si dichiara AI dalla prima frase (art. 50, in vigore dal 2 agosto 2026) ([proposta §9.1, regola 1](../PRESENTAZIONE-CEO.md)).
- **La riga AI.** Ciò che parte a L2 o a L3 non lo legge nessuno prima, quindi porta una riga che dichiara l'assistente AI di SerSan; ciò che esce a L1 esce a nome di chi approva. Una bozza del testo c'è subito, il testo definitivo lo fissa il parere (D8). La batteria di prove controlla che la riga ci sia in ogni uscita L2 e L3 e non in quelle L1 ([ADR-0020](adr/0020-autonomia-a-livelli.md); [ricerca/45 §5 e §6.3](../ricerca/45-architettura-v3.md)).
- Formazione AI documentata per tutti e quattro (art. 4), aggiornata a ogni nuovo agente ([proposta §10](../PRESENTAZIONE-CEO.md)).
- Il Coach vendite non stima le emozioni, come chiede l'AI Act ([proposta, appendice A, voce G3](../PRESENTAZIONE-CEO.md)).

---

## 9. Se un pezzo non regge

| Se non regge | Uscita | Cosa resta |
|---|---|---|
| Il motore sull'Agent SDK (corsia S), alle verifiche delle settimane 8 e 21 | Hermes sullo stesso banco di prova, con gli stessi scenari; poi al posto del motore, se i numeri lo dicono e se Hermes ha chiuso i suoi problemi di sicurezza. Il pilota di Hermes in laboratorio vale circa 6-8 giorni di sviluppo | Cancello, LiteLLM, server MCP, Porta, memoria e skill nello stesso formato; la corsia N, che non dipende da Claude Code |
| La corsia S piena (6 sessioni) o ferma | coda; poi Managed Agents di Anthropic, solo per gli agenti dichiarati verdi nel registro; poi una persona. Managed Agents costa 0,08 $ per ora di sessione più i token, circa 4-35 € al mese se usato [stima] | le azioni esterne passano comunque dal Cancello; ogni agente in riserva ha il suo tetto per sessione |
| La corsia T non disponibile (conto del posto pieno, avvio rifiutato, consegna mancata) | coda fino alla nuova finestra; se il lavoro è urgente, corsia S con un tetto di spesa per lavoro; poi una persona | le catene non cambiano: l'adattatore T è separato |
| Un modello in casa fermo (GPU piena, servizio giù) | coda per 30 minuti; poi Claude via API, se il colore lo ammette; per il rosso, una persona | il rosso non esce senza oscuramento |
| Il decisore (Jev fermo o in errore) | Haiku 5.5 a schema per verde e giallo, poi le regole, poi una carta | un errore vale un dubbio: il sistema diventa più prudente |
| LiteLLM | una chiave diretta per famiglia con limiti nella Console, solo finché si corregge; se il limite della Console non c'è, il contatore sta nel Cancello | i tetti di spesa del runner |
| Il bot di Teams | Azure Bot F0 gratuito; la pagina del Cancello con accesso Entra e gli avvisi in Teams; intanto la Sala di controllo | Cancello e approvazioni con l'identità di Entra |
| n8n | non serve: la sveglia sta nel motore | orari, eventi e registro degli eventi |
| Vexa | Attendee come piano B (escluso per Teams con login); registrazione sul PC | la trascrizione nativa delle call in Teams |
| La voce di Andrea in casa | voci migliori sulla seconda GPU; in ultima istanza una voce in cloud, circa 88 € al mese, come eccezione | Asterisk, Pipecat, operatore |
| Postiz | l'esecutore Metricool, 59,86 € al mese, già nel kit | Pubblicatore e Community manager |
| DocuSeal | firma da un fornitore esterno | Agente contratti |
| Buzz | si prova sulla stessa bacheca subito dopo la milestone 1, per circa 6 giorni di sviluppo; se non regge, i gruppi degli agenti restano in Teams | bacheca, freno, gruppi in Teams |
| Paperclip | pilota in laboratorio nella fase 6, per circa 2 giorni di sviluppo, senza dati dei clienti; se non serve, resta fuori | il registro degli agenti e la bacheca |
| La casa dei testi in git, se non passa le prove | resta BookStack | l'interfaccia unica dei testi: le catene non cambiano |
| Tutto il sistema | stop di emergenza dal telefono, da Teams o dalla Sala di controllo | i dati in PostgreSQL, nella casa dei testi, in Jira e in M365; il lavoro torna a mano |

Fonti: [ricerca/36 §12](../ricerca/36-architettura-v2.md); [proposta §5.7 e §13](../PRESENTAZIONE-CEO.md); per la v3, [ricerca/45 §2.7, §3.1, §9.1 e §9.2](../ricerca/45-architettura-v3.md), [ADR-0005](adr/0005-memoria-postgres-qdrant-bookstack.md), [ADR-0012](adr/0012-hermes-uscita.md), [ADR-0021](adr/0021-motore-a-due-corsie.md), [ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md), [ADR-0024](adr/0024-abbonamenti-come-riserva.md), [ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md), [ADR-0027](adr/0027-decisore.md), [ADR-0028](adr/0028-instradamento-a-piu-motori.md) e [ricerca/49 §2.7](../ricerca/49-instradamento-a-piu-motori.md). I giorni dei piloti vengono dalla [proposta §15](../PRESENTAZIONE-CEO.md), ripresi in ricerca/45 §9.1; nella stessa proposta §15 c'è il costo in giorni dell'uscita verso Hermes.

---

## 10. Punti aperti con Michele

Le scelte sull'infrastruttura restano di Michele. Quelle che toccano l'architettura sono nelle [domande per Michele](../DOMANDE-PER-MICHELE.md):

- **Tempi e posto per gli agenti** (n. 1-3): in quante settimane chiude F0-F4; se anticipa un "posto agenti" (LiteLLM, PostgreSQL 16, Infisical, n8n e due VM in APPS) o si parte con il pilota nella VLAN LAB; a cosa servono le VLAN 35 e 85 del trunk.
- **Rete ed esposizione** (n. 4-8): passthrough e piano della macchina Oracle, bot di Teams senza Azure, endpoint pubblico dell'MCP RAG, regola APPS → Qdrant, bypass di E0 ed E1.
- **Servizi nuovi e Cyber Essentials** (n. 9-13): VLAN 25 e 35 e i servizi nuovi con i responsabili delle patch; gli esterni da ammettere; il sostituto di MinIO; il firewall fuori supporto; le versioni e gli abbonamenti di Proxmox.
- **Backup** (n. 14-16): il disegno in pull, con permessi che aggiungono backup ma non li cancellano, e la chiave custodita fuori da casa di Michele; lo spazio dei dischi; la designazione di Michele per la copia a casa sua.
- **Hardware** (n. 17-24): riser e gabbia per la seconda GPU, software sulla Blackwell, finestre di Experimental-1, picco e autonomia dell'UPS, riaccensione del server al ritorno della corrente, data di fine supporto HPE, linea di riserva.
- **Dati e servizi del board** (n. 25-27): cos'è Sirius e cosa fanno oggi mcp-enrich, mcp-memory e runner-dash; il database di SersanOutreach; i piani di M365 e Jira.
- **Per tutti e quattro**, non solo per Michele (n. 28-30): TypeScript come linguaggio del motore anche per Mattia; chi fattura e con quale sistema; quali canali usano i clienti e chi approva i modelli di Meta per WhatsApp.

Con la v3 si aggiungono punti che le domande per Michele non hanno ancora:

- **Dove girano Cancello e motore**: nella stessa VM o in due, e se il secondo nodo ospita Cancello e Porta ([ADR-0023](adr/0023-protezioni-essenziali.md); [ricerca/45 §11](../ricerca/45-architettura-v3.md)).
- **L'ingresso del motore**: `POST /eventi` dietro la porta d'ingresso, con un token per mittente; n8n facoltativo nel board ([ADR-0022](adr/0022-eventi-e-sveglia-nel-motore.md)).
- **L'hardware per l'autonomia**: la riaccensione automatica dopo un blackout, subito; la linea di riserva anticipata all'inizio della fase 3; la seconda GPU per la milestone 2 (paragrafi 7.4 e 7.9) ([ADR-0019](adr/0019-linea-di-riserva.md); [ADR-0014](adr/0014-seconda-gpu-blackwell.md)).
- **I fornitori dei modelli**: TypeSafe per i testi gialli del decisore; OpenRouter, se serve, solo per verde e giallo ([ADR-0027](adr/0027-decisore.md); [ADR-0025](adr/0025-un-modello-per-agente.md)).
- **La corsia T**: le repo ammesse una per una, le regole di GitHub senza eccezioni, il runner nostro sul server, e da dove si leggono le consegne su GitHub (paragrafo 6.3) ([ADR-0028](adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §9](../ricerca/49-instradamento-a-piu-motori.md)).
- **Buzz sul banco**, con dati verdi, subito dopo la milestone 1 ([ADR-0026](adr/0026-bacheca-e-gruppi-degli-agenti.md)).

---

## Fonti

- [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md): proposta per i CEO, versione 2.1 dell'8 novembre 2026.
- [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md): domande tecniche per Michele, 8 novembre 2026.
- [ricerca/36-architettura-v2.md](../ricerca/36-architettura-v2.md): architettura v2, 25 ottobre 2026.
- [ricerca/37-hardware-risposte-michele.md](../ricerca/37-hardware-risposte-michele.md): hardware, risposte di Michele e board del rack, 8 novembre 2026.
- [ricerca/35-giudizio-sicurezza.md](../ricerca/35-giudizio-sicurezza.md): giudizio di sicurezza e privacy sulle tre proposte del secondo giro.
- [allegati/infra/SerSan Infra Board.md](../allegati/infra/SerSan%20Infra%20Board.md): board dell'infrastruttura di Michele.
- [allegati/infra/board-vlan.txt](../allegati/infra/board-vlan.txt): elenco delle VLAN del board.
- [allegati/infra/Rack SerSan 12U.md](../allegati/infra/Rack%20SerSan%2012U.md): board del rack, aggiornata al 5 novembre 2026.
- [ricerca/45-architettura-v3.md](../ricerca/45-architettura-v3.md): architettura v3 e decisione del gruppo di progetto, 10 novembre 2026.
- [ricerca/46-obsidian-come-casa-dei-testi.md](../ricerca/46-obsidian-come-casa-dei-testi.md): la casa dei testi, BookStack o Markdown in git, 10 novembre 2026.
- [ricerca/47-modelli-system-one.md](../ricerca/47-modelli-system-one.md): modelli System One e decisore, 10 novembre 2026.
- [ricerca/48-modelli-locali-e-gpu.md](../ricerca/48-modelli-locali-e-gpu.md): modelli locali, multimodalità e GPU, 10 novembre 2026.
- [ricerca/49-instradamento-a-piu-motori.md](../ricerca/49-instradamento-a-piu-motori.md): instradamento a più motori e corsia T, 11 novembre 2026.
- [docs/adr](adr/README.md): le decisioni di architettura, con le ADR da 0020 a 0028 e le revisioni del 10 e dell'11 novembre 2026.
