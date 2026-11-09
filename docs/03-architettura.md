# Architettura di SerSan Agent OS

Architettura v2, allineata alla proposta per i CEO versione 2.1 dell'8 novembre 2026.

Questo documento spiega come è fatto SerSan Agent OS, il sistema di agenti AI di Sersan Limited che gira sul server aziendale. Copre i principi, lo schema a livelli, i componenti, il percorso di un'azione, la memoria, le reti, l'infrastruttura, la sicurezza e la conformità. È scritto per chi deve capire il progetto e per chi lo costruisce.

**Fonti principali**

- La [proposta per i CEO](../PRESENTAZIONE-CEO.md), versione 2.1 dell'8 novembre 2026. È la fonte di verità per costi, fasi, decisioni e rischi.
- L'[architettura v2](../ricerca/36-architettura-v2.md) del 25 ottobre 2026, con il dettaglio tecnico: VLAN (le reti separate del server), macchine, regole di rete, uscite.
- Le [risposte di Michele sull'hardware e la board del rack](../ricerca/37-hardware-risposte-michele.md), 8 novembre 2026.
- Il board di Michele Sanna, che vincola tutto il resto: il [board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md), l'[elenco delle VLAN](../allegati/infra/board-vlan.txt) e la [board del rack](../allegati/infra/Rack%20SerSan%2012U.md).
- Le [domande tecniche per Michele](../DOMANDE-PER-MICHELE.md), cioè le scelte sull'infrastruttura che restano sue.

**Come leggere**

- "Proposta" è `PRESENTAZIONE-CEO.md`. "Board" è l'infrastruttura disegnata da Michele.
- "Fase 0-6" sono le fasi del sistema di agenti; "F0-F5" sono le fasi del board. Le due roadmap corrono affiancate: l'infrastruttura la porta avanti Michele, il sistema di agenti si costruisce sopra ([proposta §11](../PRESENTAZIONE-CEO.md)).
- Le VLAN 25, 32 e 35 e le macchine con un nome come `agenti-01` sono proposte da far approvare a Michele ([ricerca/36 §3](../ricerca/36-architettura-v2.md)).
- I prezzi sono IVA esclusa ([proposta §12.1](../PRESENTAZIONE-CEO.md)). La stima dei giorni di sviluppo è solo nella [proposta §15](../PRESENTAZIONE-CEO.md).

---

## 1. I principi

### 1.1 Tutto in casa, dentro il board di Michele

Il sistema gira sul server di SerSan, dentro l'infrastruttura disegnata da Michele. In cloud restano solo i servizi verticali del board: Microsoft 365 con Teams, Claude Team, le API di Anthropic, Jira per to-do e progetti, Instantly per le campagne email, GitHub per il codice, Supabase per il database del prodotto, Vercel per i deploy, il DNS di Cloudflare e una piccola macchina Oracle a Milano per l'accesso da fuori. Il resto gira in casa, in reti separate. Fuori dal board restano poche eccezioni, da approvare una per una: la linea telefonica di Andrea, WhatsApp, Telegram, Slack per i clienti, l'invio della newsletter e alcuni strumenti commerciali (decisioni 8-10 e 15) ([proposta §5.1](../PRESENTAZIONE-CEO.md); [board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

Azure esce: SersanOutreach, la nostra piattaforma outbound per LinkedIn ed email che diventa il CRM degli agenti, passa sul server nella fase F2 del board, "via da Azure", e la macchina Azure si spegne solo dopo una settimana di funzionamento stabile ([proposta §7.1 e §7.2](../PRESENTAZIONE-CEO.md)).

### 1.2 Un processo per lavoro

Il motore degli agenti lo scriviamo noi con l'Agent SDK di Claude, cioè Claude Code usato come libreria. Ogni lavoro gira in un processo suo, con il profilo dell'agente, i suoi strumenti e un tetto di spesa ([proposta §5.1](../PRESENTAZIONE-CEO.md)). Il motore non duplica ciò che il board ha già: gli orari li fa n8n, il programma delle automazioni; i budget li tiene LiteLLM (paragrafo 1.4); la memoria sta in PostgreSQL, Qdrant e BookStack, cioè il database, la memoria che cerca per significato e la wiki con regole e processi ([proposta §5.3](../PRESENTAZIONE-CEO.md)).

### 1.3 Il Cancello: gli agenti propongono, il codice esegue

Il Cancello è l'unico programma che può mandare una mail, scrivere a un cliente, toccare il CRM o telefonare. Le azioni verso l'esterno le compie solo dopo il sì di una persona, una volta sola, oppure con una regola "Sempre" approvata. Le scritture interne (meeting e deal nel CRM, to-do in Jira) le fa secondo regole scritte, a nome della persona responsabile. In ogni caso registra tutto ([proposta §5.1](../PRESENTAZIONE-CEO.md)).

La macchina degli agenti non ha accesso a internet e parla solo con LiteLLM, con i server MCP e con il Cancello: un agente non ha una strada per mandare qualcosa fuori se non passando dal Cancello ([proposta §5.4](../PRESENTAZIONE-CEO.md)). MCP (Model Context Protocol) è la presa standard con cui un agente usa uno strumento ([proposta §7.3](../PRESENTAZIONE-CEO.md)).

### 1.4 Claude ragiona, LiteLLM tiene i conti

Gli agenti ragionano con Claude attraverso la chiave API: Haiku per i lavori semplici, Sonnet per quasi tutto, Opus per offerte e analisi. Ogni chiamata passa da LiteLLM, la porta verso i modelli prevista dal board, che custodisce le chiavi e dà a ogni agente, squadra e persona il suo budget ([proposta §5.1](../PRESENTAZIONE-CEO.md)). All'80% del budget arriva un avviso, al 100% il lavoro si ferma ([proposta §9.2](../PRESENTAZIONE-CEO.md)).

### 1.5 I dati hanno tre colori

Una regola semplice, scritta nel codice del Cancello, decide cosa può uscire dal server e verso chi ([proposta §5.6](../PRESENTAZIONE-CEO.md)).

| Colore | Cosa | Dove può andare |
|---|---|---|
| **Verde** | Pubblico o interno non personale | Qualunque fornitore ammesso, anche Claude Team |
| **Giallo** | Contatti di lavoro, campi del CRM, riassunti | Solo i fornitori del board, con contratto commerciale e DPA (l'accordo sul trattamento dei dati) |
| **Rosso** | Audio, trascrizioni integrali, mail intere, documenti dei clienti, giudizi sulle persone, finanza | Resta sul server, oppure va all'API di Anthropic dopo aver oscurato in locale i dati non necessari |

Con tutto sul server l'audio delle call e la voce di Andrea non passano più da fornitori negli USA: l'audio resta in casa e si trascrive in casa. Claude Team riceve verde e giallo, e il rosso solo oscurato, finché il parere legale e la valutazione d'impatto non decidono diversamente, entro la settimana 3 ([proposta §5.6](../PRESENTAZIONE-CEO.md)).

### 1.6 Ogni pezzo si può cambiare

Il motore parla con gli strumenti solo via MCP, con i modelli solo via LiteLLM e con l'esterno solo via Cancello ([ricerca/36 §12](../ricerca/36-architettura-v2.md)). Per questo Hermes, la piattaforma di agenti open source valutata come alternativa, resta un'uscita: se il motore non regge le verifiche delle settimane 8 e 21, si prova Hermes sullo stesso banco di prova e si decide sui numeri, mentre Cancello, memoria, server MCP, bot e skill restano uguali. Hermes diventa l'orchestratore solo se chiude i suoi problemi di sicurezza ([proposta §5.7](../PRESENTAZIONE-CEO.md)).

La chat di gruppo è la casa comune: Teams per persone e agenti, con le approvazioni sul telefono; Telegram, Slack e WhatsApp collegati; Buzz, la chat open source fatta per persone e agenti, in prova sul server ([proposta §4.11 e §5.1](../PRESENTAZIONE-CEO.md)).

---

## 2. Lo schema a livelli

Lo schema è quello della [proposta §5.2](../PRESENTAZIONE-CEO.md). Si legge dall'alto: le persone, poi il server con i suoi livelli, poi ciò che resta fuori dal server.

```
PERSONE (4)   Teams e Outlook (M365, accesso con MFA e chiave FIDO2), dal PC e dal telefono
              Claude Team: chat, skill, progetti per squadra, ricerca nella memoria
              Telegram (avvisi) · WhatsApp (clienti) · Slack (clienti) · Buzz (in prova)

===== SERVER DL380 · Proxmox · reti separate dietro OPNsense · accesso da NetBird =====
INGRESSO   Traefik, raggiunto da Pangolin sulla macchina Oracle: bot di Teams,
           webhook firmati, ricerca nella memoria per Claude Team, pagine di firma
APP        CANCELLO + PORTA CHAT (bot di Teams, Telegram, Slack, WhatsApp)
           server MCP: memoria, bacheca, BookStack, Jira, posta in lettura,
           SersanOutreach
           n8n (orari) · LiteLLM (budget) · BookStack · SersanOutreach
           Postiz · listmonk · DocuSeal · fatturazione · Andrea (Pipecat)
AGENTI     MOTORE (Agent SDK): un processo per lavoro, nessun accesso a internet
DATI       PostgreSQL 16 · Qdrant · Infisical · Vaultwarden · archivio dei file
VOCE       Asterisk: il centralino di Andrea, con una linea telefonica italiana
RIUNIONI   Vexa: il bot nelle call dei clienti (Teams di altri, Meet, Zoom)
AI         RTX 4000 + seconda GPU: embedding, ricerca, Qwen3-4B, trascrizione
MONITOR    Prometheus · Grafana · Loki · Uptime Kuma · Wazuh · NetBox
LAB        banco di prova degli agenti · Buzz · Paperclip
=======================================================================================
CLOUD DEL BOARD  M365 ed Entra · Claude Team · API Anthropic via LiteLLM · Jira
                 Instantly · GitHub · Supabase · Vercel · Cloudflare (DNS)
                 Oracle Cloud a Milano: NetBird, Pangolin, monitoraggio
ESTERNI          linea telefonica italiana · WhatsApp (Meta) · Telegram · Slack
                 invio della newsletter · strumenti commerciali che restano
BACKUP 3-2-1     Proxmox Backup Server in sede, ogni notte copia cifrata a casa
                 di Michele (Terra Noa) · S3 fuori sede facoltativo
```

### 2.1 I livelli, uno per uno

**Persone.** Sono quattro: Alessandro, Michele, Alberto e Mattia. Lavorano da Teams e Outlook, dal PC e dal telefono. L'accesso passa da Entra ID, l'identità di Microsoft, con MFA (un secondo fattore oltre alla password) e con la chiave FIDO2, una chiavetta fisica che conferma l'identità. Claude Team è la finestra di lavoro di ognuno: chat, skill, progetti per squadra e la ricerca nella memoria aziendale, con i propri permessi. Telegram riceve gli avvisi, WhatsApp e Slack servono soprattutto verso i clienti, Buzz è in prova ([proposta §3, §4.11 e §5.2](../PRESENTAZIONE-CEO.md)).

**Il server.** È un HPE ProLiant DL380 Gen10 con Proxmox, il sistema che fa girare le macchine virtuali (VM) e i container leggeri (LXC). I servizi stanno in reti separate, le VLAN (reti logiche distinte sullo stesso cablaggio), dietro OPNsense, il firewall open source. Da fuori si entra solo con NetBird, una rete privata cifrata che chiede un'identità verificata ([proposta §5.2 e §6.1](../PRESENTAZIONE-CEO.md)). Fra le VLAN tutto è vietato salvo ciò che è permesso, e il routing lo fa OPNsense ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

**Ingresso.** Traefik riceve le richieste HTTPS e le smista ai servizi interni. Da internet ci si arriva solo attraverso Pangolin, un tunnel che gira sulla macchina Oracle e pubblica pochi servizi senza aprire porte in ufficio. Passano di qui i messaggi dei bot di Teams, i webhook firmati (le chiamate che un servizio esterno fa quando succede qualcosa, firmate dal mittente), la ricerca nella memoria per Claude Team e le pagine di firma dei contratti ([proposta §5.2](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.4](../ricerca/36-architettura-v2.md)).

**App.** È il livello più affollato ([proposta §5.2](../PRESENTAZIONE-CEO.md)):

- il Cancello con la Porta chat, cioè i bot di Teams, Telegram, Slack e WhatsApp;
- i server MCP che danno agli agenti memoria, bacheca, BookStack, Jira, posta in lettura e SersanOutreach;
- n8n, che lancia i lavori a orario e riceve i webhook, e LiteLLM, che tiene i budget;
- BookStack, la wiki con regole e processi, e SersanOutreach, il CRM;
- i servizi per marketing, amministrazione e voce: Postiz per i post, listmonk per la newsletter, DocuSeal per la firma elettronica, la fatturazione e Pipecat, il programma che fa parlare Andrea.

**Agenti.** Il motore sull'Agent SDK: un processo per lavoro, nessun accesso a internet ([proposta §5.2](../PRESENTAZIONE-CEO.md)).

**Dati.** PostgreSQL 16 per i dati strutturati, Qdrant per la memoria vettoriale (il database che cerca per significato), Infisical per i segreti delle applicazioni, Vaultwarden per le password delle persone, e l'archivio dei file ([proposta §5.2](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1](../ricerca/36-architettura-v2.md)). Questa rete non ha internet ([elenco delle VLAN](../allegati/infra/board-vlan.txt)).

**Voce.** Asterisk, il centralino open source di Andrea, collegato a una linea telefonica italiana ([proposta §5.2](../PRESENTAZIONE-CEO.md)).

**Riunioni.** Vexa, il bot che entra nelle call dei clienti su Teams di altre aziende, Meet e Zoom. Le call di SerSan in Teams le trascrive già Microsoft, e il sistema legge quella trascrizione ([proposta §4.2 e §5.2](../PRESENTAZIONE-CEO.md)).

**AI.** La GPU Quadro RTX 4000 e, più avanti, una seconda GPU. Fanno i lavori che conviene tenere in casa: gli embedding (il testo trasformato in numeri per cercarlo per significato) e la ricerca nella memoria, il modello piccolo Qwen3-4B che prepara i documenti, la trascrizione delle call e, con la seconda GPU, la voce di Andrea. Gli agenti non usano la GPU: ragionano con Claude via API ([proposta §6.2](../PRESENTAZIONE-CEO.md)).

**Monitor.** Prometheus raccoglie le metriche, Grafana le mostra nei cruscotti, Loki tiene i log, Uptime Kuma controlla che i servizi rispondano, Wazuh cerca vulnerabilità e segnala allarmi di sicurezza, NetBox è l'inventario di indirizzi e apparati. Questa rete legge da tutte e non ha internet ([proposta §5.2](../PRESENTAZIONE-CEO.md); [elenco delle VLAN](../allegati/infra/board-vlan.txt)).

**Lab.** Il banco di prova degli agenti, dove gira il pilota, e i servizi in prova: Buzz e Paperclip ([proposta §5.2 e §11](../PRESENTAZIONE-CEO.md)).

**Cloud del board.** M365 con Entra, Claude Team, l'API di Anthropic (raggiunta solo attraverso LiteLLM), Jira, Instantly, GitHub, Supabase, Vercel, Cloudflare per il DNS, e la macchina Oracle Cloud a Milano per NetBird, Pangolin e il monitoraggio da fuori ([proposta §5.2](../PRESENTAZIONE-CEO.md)).

**Esterni.** I servizi fuori dal board, ognuno un'eccezione da approvare: la linea telefonica italiana di Andrea, WhatsApp di Meta, Telegram, Slack, l'invio della newsletter e gli strumenti commerciali che restano ([proposta §5.1 e §5.2](../PRESENTAZIONE-CEO.md)).

**Backup 3-2-1.** Tre copie dei dati su due supporti diversi, di cui una fuori dall'ufficio: un Proxmox Backup Server in sede e, ogni notte, una copia cifrata a casa di Michele, a Terra Noa. Uno spazio S3 fuori sede (un archivio di file in cloud) è facoltativo ([proposta §5.2 e §6.1](../PRESENTAZIONE-CEO.md)). Il dettaglio è nel paragrafo 7.6.

### 2.2 Dove sta ogni livello

| Livello | VLAN | Stato | Macchine e servizi |
|---|---|---|---|
| Ingresso | 20 EDGE | board | Traefik; Pangolin e la gestione di NetBird stanno sulla macchina Oracle |
| App | 30 APPS | board | `cancello-01` (VM: Cancello e Porta), `mcp-01` (LXC: server MCP), n8n, LiteLLM, MCP RAG, BookStack, Open WebUI, Firecrawl, SersanOutreach, Postiz, listmonk, DocuSeal, fatturazione, `andrea-01` (LXC: Pipecat) |
| Agenti | 32 AGENTI | proposta | `agenti-01` (VM con Docker: il motore). In alternativa resta nella 30, con il firewall di Proxmox per ogni VM |
| Dati | 40 DATA | board | PostgreSQL 16, Qdrant, MariaDB (nuova), Infisical, Vaultwarden, archivio S3 al posto di MinIO |
| Voce | 25 VOCE | proposta | `voce-01` (LXC: Asterisk) |
| Riunioni | 35 MEET | proposta | `meet-01` (VM: Vexa) |
| AI | 80 AI | board | `ai-gpu-01` (LXC): Qwen3-4B, embedding e reranker, Docling, trascrizione |
| Monitor | 70 OBSRV | board | Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox |
| Lab | 90 LAB | board | `stage-agenti` (VM, proposta: il banco di prova), Experimental-2 (la sandbox Linux del laboratorio) con Buzz e Paperclip |

Fonti: [ricerca/36 §3 e §4.1](../ricerca/36-architettura-v2.md); [elenco delle VLAN](../allegati/infra/board-vlan.txt); per la macchina Oracle, [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md).

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

| Componente | Ruolo | Dove gira | Quando |
|---|---|---|---|
| **Motore degli agenti** | Prende i lavori da una coda e avvia un processo dell'Agent SDK per ognuno, con il profilo dell'agente. Tiene i tetti, riprende i lavori in attesa, si ferma con `/stop` | `agenti-01`, VLAN 32 (proposta) | Prima parte nella fase 0; sul banco di prova nella fase 1; sul server nella fase 2 |
| **Cancello** | L'unico esecutore delle azioni esterne: classifica, crea le carte, controlla chi approva, esegue una volta sola, registra, ferma tutto con lo stop di emergenza | `cancello-01`, VLAN 30, sempre in una macchina separata dal motore | Versione 1 alla fine della fase 1; FIDO2 e regole "Sempre" nella fase 2; versione 2 nella fase 3 |
| **Porta chat** | I bot: uno per il Cancello e nove di squadra in Teams; poi Telegram, Slack e WhatsApp con lo stesso codice (Chat SDK e Teams SDK) | dentro `cancello-01` | Teams nelle fasi 1-2; gli altri canali nella fase 3 |
| **Server MCP** | Le prese degli agenti: memoria su PostgreSQL, bacheca, BookStack in lettura, Jira, posta e calendario in lettura, Firecrawl, SersanOutreach | `mcp-01`, VLAN 30 | Fasi 2-3 |
| **Bacheca** | Compiti e passaggi fra agenti, con il freno alle catene | tabelle in PostgreSQL, con un suo server MCP | Fase 2 |
| **Registro dei profili** | Una riga per agente: nome, squadra, responsabile, modello, cosa può toccare, tetto di spesa, costo del mese. È l'organigramma | file in git, con pagina in BookStack e vista in Grafana | Fasi 1-2 |
| **Banco di prova** | Il pilota della fase 1 (settimane 5-8), finché il motore non passa sul server nella fase 2; poi le prove di ogni aggiornamento dell'SDK. Ha un suo PostgreSQL e una chiave API limitata | `stage-agenti`, VLAN 90 LAB | Fase 1 |

Fonti: [proposta §4.12, §5.3, §5.4 e §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1, §5.3 e §7.3](../ricerca/36-architettura-v2.md).

**Il motore.** È un servizio in TypeScript, linguaggio da confermare anche per Mattia ([ricerca/36, In breve](../ricerca/36-architettura-v2.md); [domande per Michele, n. 28](../DOMANDE-PER-MICHELE.md)). Funziona così ([ricerca/36 §2.1, §4.1, §5.1, §5.7 e §6](../ricerca/36-architettura-v2.md)):

- un lavoro entra in una tabella di PostgreSQL con il profilo, la persona per cui si lavora, il tetto in dollari e la scadenza;
- il runner, la parte del motore che fa girare i lavori, avvia per ognuno un processo dell'SDK con il profilo: le istruzioni della squadra (`CLAUDE.md`), le skill ammesse, un elenco chiuso di strumenti MCP, la chiave di LiteLLM, il tetto di turni (`maxTurns`) e di spesa (`maxBudgetUsd`);
- la modalità è `dontAsk`: ciò che non è nell'elenco è negato, senza domande;
- ogni famiglia di agenti ha cartella, configurazione e chiave sue. Con `settingSources: []`, `CLAUDE_CONFIG_DIR` e `cwd` per famiglia un agente non legge le impostazioni di un altro; l'opzione `env` sostituisce l'ambiente, quindi il processo non vede le chiavi del motore;
- gli agenti con gli stessi permessi e gli stessi segreti condividono un container Docker ("container di famiglia");
- le sessioni si salvano in PostgreSQL attraverso il `SessionStore` dell'SDK, così un lavoro in attesa riparte dopo ore;
- metriche e log vanno a Prometheus e Loki con OpenTelemetry, lo standard aperto per la telemetria;
- il traffico non essenziale verso Anthropic è spento (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`) e non c'è WebFetch diretto: il web passa da Firecrawl.

Come punto di partenza ogni sessione ha 1 GiB di RAM, 1 CPU e 5 GiB di disco; il motore usa 12 GB con 6 sessioni insieme, 16 con 8-10 e 20 con 12-16 ([ricerca/36 §4.1](../ricerca/36-architettura-v2.md)). La versione dell'SDK è fissata e si aggiorna ogni due settimane, dopo dieci scenari di prova, entro 14 giorni dall'uscita ([proposta §13](../PRESENTAZIONE-CEO.md)). Al 25 ottobre 2026 era la 0.3.310 per TypeScript, con Claude Code 2.1.310 ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).

**Tre tipi di lavoro, nessun agente declassato.** Il tipo dice come un agente lavora in quel momento, non quanto vale ([ricerca/36 §5.2](../ricerca/36-architettura-v2.md)):

- **chiamata a schema**: riassumere, classificare, estrarre. Una sola chiamata via LiteLLM, senza strumenti, lanciata da n8n o dal runner. Contro le iniezioni di istruzioni nel testo è il disegno più robusto;
- **sessione con strumenti**: lavori a più passi, come brief, offerte, presentazioni, agenda. Una sessione dell'SDK con il collegamento al Cancello;
- **servizio**: un componente che fa il lavoro da sé, come la pipeline della memoria, Vexa, il centralino o il Cancello.

Tutte le 57 figure sono profili del registro. Anche quelle che una persona potrebbe usare a mano, come Copywriter, Agente video, Agente grafiche, Pubblicatore, Sviluppatori, Intervistatore e Assistente personale, restano agenti che ricevono lavoro dalla bacheca; in più le loro skill sono anche in Claude Team, così una persona le può usare a mano. Per ogni profilo il registro scrive il tipo di lavoro, se legge testo di terzi e quali strumenti ha ([ricerca/36 §5.2](../ricerca/36-architettura-v2.md)).

**La bacheca e il freno.** È il posto dove gli agenti si passano il lavoro ([ricerca/36 §5.4](../ricerca/36-architettura-v2.md)):

- due tabelle in PostgreSQL, `compiti` e `passaggi`, con un server MCP per creare, prendere, aggiornare, passare e chiudere un compito e leggerne lo stato;
- dal modello della bacheca di Hermes: una corsia di revisione fra agenti prima della carta; il blocco "serve un umano", che si sblocca dalla chat; il blocco automatico dopo due fallimenti di fila; il rifiuto dei cicli di dipendenze; un dispatcher che riprende i compiti fermi;
- il freno: al massimo tre passaggi per catena, otto messaggi per thread e un tetto di spesa per catena ([proposta §4.11](../PRESENTAZIONE-CEO.md)). Oltre, la catena si ferma e arriva una carta a una persona ([ricerca/36 §5.4](../ricerca/36-architettura-v2.md));
- ogni passaggio è rispecchiato nel canale Teams "Agenti", con il nome dell'agente in testa; le persone intervengono con una @menzione;
- i to-do delle persone stanno in Jira. Un agente chiude da solo solo i compiti fra agenti; per quelli delle persone chiede il sì.

**Il registro dei profili e le skill.** Il registro si vede come organigramma in una pagina di BookStack e in un cruscotto. Un agente nuovo nasce solo con un'approvazione, che porta con sé la sua riga nel registro dei trattamenti. Gli agenti al lavoro sono 14 alla fine della fase 2, circa 32 alla fine della fase 3 e tutti e 57 alla fine della fase 6 ([proposta §4.12](../PRESENTAZIONE-CEO.md)). La pagina BookStack e la vista Grafana si generano ogni notte dal registro in git ([ricerca/36 §5.3](../ricerca/36-architettura-v2.md)). Le skill stanno in git; dalla fase 4 gli agenti scrivono proposte di skill in una cartella "proposte", un revisore le guarda ogni settimana e una persona le approva con una pull request ([proposta, appendice A, voce A6](../PRESENTAZIONE-CEO.md)).

### 3.2 I servizi del board che il sistema usa

| Componente | Ruolo per gli agenti | Dove | Stato |
|---|---|---|---|
| **n8n** | Orari, webhook firmati, ingressi, avvisi. Pubblico solo sui webhook firmati, senza moduli pubblici | VLAN 30 | board |
| **LiteLLM** | Porta dei modelli: chiavi virtuali e budget per agente, squadra e persona. È l'unica uscita verso `api.anthropic.com` | VLAN 30; nel board arriva con la fase F4 | board |
| **PostgreSQL 16** | Coda dei lavori, bacheca, sessioni, Cancello, memoria strutturata, dati di LiteLLM e n8n | VLAN 40 | board |
| **Qdrant e MCP RAG** | Memoria vettoriale con ricerca per parole (BM25) e reranker (un modello che riordina i risultati). L'MCP RAG è il server che cerca nella memoria i passaggi utili e li passa al modello: applica i permessi della persona e registra le domande | VLAN 40 e 30 | board (fase F4), estensioni nostre |
| **Pipeline AI** | Ollama, il programma che fa girare i modelli locali, con Qwen3-4B per metadati e riassunti dei documenti; Infinity con embedding e reranker da 0.6B; Docling, che trasforma PDF e scansioni in testo | VLAN 80, `ai-gpu-01`, sulla RTX 4000 | board |
| **BookStack** | Regole "Come lavoro", processi, catalogo, manuale degli agenti | VLAN 30 | board |
| **Infisical e Vaultwarden** | Segreti delle applicazioni; password delle persone | VLAN 40 | board |
| **Archivio dei file** | Audio e file degli agenti. Il board prevedeva MinIO, che è archiviato e non più mantenuto: il sostituto lo sceglie Michele | VLAN 40 | board, da sostituire |
| **Firecrawl** | L'unica strada degli agenti verso il web: scarica le pagine e le trasforma in testo markdown | VLAN 30 | board |
| **Open WebUI** | La chat con i modelli per tutti, con il budget di LiteLLM | VLAN 30 | board |
| **Monitoraggio** | Prometheus, Grafana, Loki, Uptime Kuma, Wazuh, NetBox | VLAN 70 | board |
| **Traefik, Pangolin, NetBird** | Ingresso dei servizi pubblici e accesso da fuori | VLAN 20 e macchina Oracle | board |
| **SersanOutreach** | La piattaforma outbound, che diventa il CRM degli agenti. Due server MCP: lettura con 19 strumenti, operatore con 14 operazioni | VLAN 30, dalla fase F2 del board | board |

Fonti: [ricerca/36 §4.1, §4.5 e §5.7](../ricerca/36-architettura-v2.md); [proposta §7.2 e §7.3](../PRESENTAZIONE-CEO.md); [domande per Michele, n. 11](../DOMANDE-PER-MICHELE.md).

Su SersanOutreach due regole contano per l'architettura. L'operazione che approva un messaggio la chiama solo il Cancello, dopo il sì di una persona su una carta: gli agenti leggono liberamente e scrivono solo attraverso il Cancello. Non esistono invii in blocco, lanci o cancellazioni: restano a una persona ([proposta §7.3](../PRESENTAZIONE-CEO.md)). Il database resta su Supabase, che il board tiene in cloud, salvo una scelta diversa di Michele ([proposta §7.2](../PRESENTAZIONE-CEO.md)). Oggi i due server MCP parlano solo in locale (stdio): nella fase 2 vanno portati su HTTP, con un token per ogni famiglia di agenti ([ricerca/36 §7.3 e §8.1, voce B2](../ricerca/36-architettura-v2.md)).

### 3.3 I servizi nuovi da aggiungere al board

| Componente | Ruolo | Dove | Fase |
|---|---|---|---|
| **MariaDB** | Il database che BookStack richiede | VLAN 40, container | 2 |
| **Trascrizione** | Trascrive in casa l'audio delle call e delle riunioni dal vivo (faster-whisper, Parakeet, pyannote per riconoscere chi parla) | VLAN 80, `ai-gpu-01` | 3 |
| **Vexa** | Il bot che entra nelle call dei clienti (Teams di altri, Meet, Zoom) | `meet-01`, VLAN 35 | 3 |
| **Asterisk 22 LTS** | Il centralino di Andrea, collegato al trunk SIP dell'operatore italiano (la linea telefonica via internet) | `voce-01`, VLAN 25 | 5 |
| **Pipecat** | La conversazione di Andrea: ascolto, ragionamento con Claude Haiku, voce. Prima sulla CPU, poi sulla seconda GPU | `andrea-01`, VLAN 30 | 5 |
| **Postiz** | Programmazione dei post e metriche. Mai pubblico | VLAN 30, container | 4 |
| **listmonk** | Newsletter, con l'invio attraverso un relay SMTP esterno (un servizio che spedisce la posta in quantità). Mai pubblico | VLAN 30, container | 4 |
| **DocuSeal** | Firma elettronica; solo le pagine di firma escono via Pangolin | VLAN 30 | 6 |
| **Fatturazione** | Fatture, incassi e solleciti: Sirius, che ha già i dati fiscali e dei clienti, se fa al caso, oppure Invoice Ninja in casa (decisione 22) | VLAN 30, container | 6 |
| **Buzz** | Stanza degli agenti in prova, collegata alla stessa bacheca | Experimental-2, VLAN 90 | 4 |
| **Paperclip** | Piano di controllo open source per "aziende di agenti", in prova | Experimental-2, VLAN 90 | 6 |

Fonti: [ricerca/36 §4.1 e §4.5](../ricerca/36-architettura-v2.md); [proposta §11 e appendice A, voci G5, L1 e L2](../PRESENTAZIONE-CEO.md).

Ogni servizio nuovo entra nel perimetro Cyber Essentials (la certificazione britannica di sicurezza di base, paragrafo 8.2) con un responsabile delle patch e un posto nell'inventario. Prima della fase F4 del board entrano solo i servizi del pilota ([proposta §6.2 e §13](../PRESENTAZIONE-CEO.md)). Chi patcha cosa lo fissa Michele ([domande per Michele, n. 9](../DOMANDE-PER-MICHELE.md)).

### 3.4 Cloud del board ed esterni

| Servizio | Ruolo | Stato |
|---|---|---|
| **M365 ed Entra ID** | Identità, MFA, posta, calendario, documenti, Teams. Gli agenti ci arrivano con Graph, l'API di Microsoft 365, con permessi stretti: siti SharePoint scelti uno per uno e caselle limitate | cloud |
| **Claude Team** | La finestra di lavoro delle persone, con il connettore verso la memoria. Nessun processo aziendale gira sui compiti programmati di Claude Team: ciò che è a orario resta in n8n | cloud |
| **API di Anthropic** | Il ragionamento degli agenti, solo attraverso LiteLLM; la chiave diretta solo sul banco di prova | cloud |
| **Jira** | To-do e progetti | cloud |
| **Instantly** | Invio delle campagne email; lo stop di emergenza mette in pausa le campagne | cloud |
| **GitHub, Vercel** | Codice e runner in casa; i deploy del sito li fa una persona | cloud |
| **Supabase** | Il database di SersanOutreach | cloud |
| **Cloudflare** | Solo il DNS | cloud |
| **Macchina Oracle a Milano** | NetBird (gestione e relay), Pangolin, Uptime Kuma e ntfy (notifiche push) | cloud |
| **Operatore telefonico italiano** | Numero e trunk SIP di Andrea (proposto: Messagenet) | esterno |
| **WhatsApp, Telegram, Slack** | Canali in più verso gli stessi agenti | esterni |
| **Relay SMTP** | Invio della newsletter | esterno |
| **Strumenti commerciali** | Quelli che restano, decisi caso per caso (decisione 15) | esterni |

Fonti: [proposta §5.1, §5.2 e §14](../PRESENTAZIONE-CEO.md); [ricerca/36 §4.1, §5.6, §8.2 e §12](../ricerca/36-architettura-v2.md); [ricerca/37 §2](../ricerca/37-hardware-risposte-michele.md); [domande per Michele, n. 10](../DOMANDE-PER-MICHELE.md).

### 3.5 La chat di gruppo

- **Teams è la casa comune**: un team "SerSan Agent OS" con un canale per squadra, "Approvazioni" per le carte, "Agenti" (la sala macchine dove gli agenti si passano il lavoro), "Ingresso", "Call di vendita", "Bandi" e un canale privato per ogni cliente. Ogni squadra ha un bot con il nome dei suoi agenti e ogni messaggio è firmato dall'agente che lo scrive ([proposta §4.11](../PRESENTAZIONE-CEO.md)).
- **I bot sono dieci registrazioni**, il Cancello più nove squadre; che puntino tutte allo stesso servizio va provato ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)). La registrazione è "Teams-managed", senza sottoscrizione Azure. Se dà errori 401, si usa un Azure Bot F0 gratuito, senza risorse accese, oppure il piano B: le carte sulla pagina del Cancello dietro Pangolin, con Entra e FIDO2, e gli avvisi in Teams ([ricerca/36 §5.6](../ricerca/36-architettura-v2.md); [proposta §13](../PRESENTAZIONE-CEO.md)).
- **Il nodo Teams di n8n serve solo agli avvisi**: registra l'ora della risposta, non chi approva ([ricerca/36 §5.6](../ricerca/36-architettura-v2.md)).
- **Telegram** riceve gli avvisi; **WhatsApp** serve soprattutto verso i clienti, con l'API ufficiale di Meta e un numero dedicato, sempre dal Cancello; **Slack** si collega per i clienti che lavorano lì. Sono gli stessi agenti con lo stesso codice, dalla fase 3. Su questi canali passano solo dati verdi; per approvare anche da lì servirebbe legare quegli account all'identità Microsoft di ciascuno ([proposta §4.11](../PRESENTAZIONE-CEO.md)).
- **Buzz**, la chat open source di Block fatta per persone e agenti, gira sul banco di prova come stanza degli agenti, collegata alla stessa bacheca. Oggi perde alcune risposte senza segnalarlo e le sue approvazioni non sono pronte: esce dal laboratorio quando questi problemi sono chiusi ([proposta §4.11](../PRESENTAZIONE-CEO.md)). I criteri di uscita, con le issue da chiudere, sono in [ricerca/36 §5.6](../ricerca/36-architettura-v2.md).
- **Nessun bot entra nei canali condivisi con i clienti**: lì scrive solo il Cancello, dopo una carta ([proposta §4.11](../PRESENTAZIONE-CEO.md)).

---

## 4. Il percorso di un'azione

L'obiettivo è che il lavoro dopo una call avvenga in modo autonomo, e ci si arriva per gradi ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Il caso tipico: dopo una call in Teams il riassunto arriva nel canale interno e la bozza della mail di follow-up arriva sul telefono come carta; dopo il sì parte una volta sola ([proposta §1](../PRESENTAZIONE-CEO.md)). Il percorso, passo per passo:

1. **Nasce il lavoro.** In tre modi: n8n a orario o su un webhook firmato; una persona che scrive a un agente in Teams; un agente che passa un compito a un altro nella bacheca. Il lavoro entra nella coda con il profilo, la persona per cui si lavora, il tetto di spesa e la scadenza ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
2. **Parte la sessione.** Il runner avvia un processo dell'SDK con il profilo dell'agente. L'agente legge la pagina "Come lavoro" della persona in BookStack, i dati fissi dall'MCP della memoria e i passaggi utili dall'MCP RAG, con i permessi della persona ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
3. **Il testo di terzi resta un dato.** Mail, trascrizioni, pagine web e risposte dei prospect entrano da una corsia senza strumenti: una sessione che le legge restituisce solo campi a schema. Gli agenti li leggono come dati, non come comandi; è la difesa contro le iniezioni di prompt ([proposta §9.2](../PRESENTAZIONE-CEO.md)). Chi legge testo di terzi non può proporre azioni nella stessa sessione ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
4. **L'agente propone.** Se qualcosa deve uscire, l'agente propone un'azione, per esempio "manda questa mail a questo indirizzo", con il testo esatto e il motivo ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Prima di ogni strumento l'Agent SDK chiama una funzione del runner, l'hook `PreToolUse`, che chiede al Cancello; se il Cancello non risponde in tempo, l'azione è bloccata ([proposta §5.3](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.1](../ricerca/36-architettura-v2.md)). Si consente un solo effetto per turno: è una regola da provare nella fase 0 ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
5. **Il Cancello classifica.** Una regola mette l'azione in una classe: lettura, scrittura interna, invio, pubblicazione, pagamento, cancellazione, credenziali ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Cancellazioni e credenziali sono sempre negate agli agenti; le scritture interne passano secondo regole scritte, a nome del responsabile; le azioni delicate diventano una carta ([ricerca/36 §5.8](../ricerca/36-architettura-v2.md)).
6. **La carta.** Arriva nel canale "Approvazioni" di Teams, sul telefono, con il testo esatto, un codice che vale una volta e una scadenza ([proposta §5.4](../PRESENTAZIONE-CEO.md)). La persona approva, modifica o rifiuta con un tocco; il Cancello controlla chi ha premuto, con l'identità Microsoft, e che sia fra gli approvatori di quella classe ([proposta §4.11](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.1](../ricerca/36-architettura-v2.md)). Per offerte, contratti, fatture e primi contatti serve anche la chiave FIDO2, sulla pagina del Cancello ([proposta §5.4](../PRESENTAZIONE-CEO.md); [ricerca/35 §8](../ricerca/35-giudizio-sicurezza.md)). Intanto l'agente chiude il turno e il lavoro resta in attesa ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).
7. **L'esecuzione, una volta sola.** Dopo il sì l'esecutore del Cancello compie l'azione una volta sola. Se nel frattempo il testo è cambiato, la carta non vale più ([proposta §5.4](../PRESENTAZIONE-CEO.md)): ogni carta porta l'impronta del testo esatto, e l'esecutore la ricalcola prima di agire ([ricerca/35 §8](../ricerca/35-giudizio-sicurezza.md)). Gli esecutori sono stretti: la posta parte da Outlook via Graph solo verso il dominio del cliente ([ricerca/36 §8.1, voce B3](../ricerca/36-architettura-v2.md)).
8. **Il registro.** Tutto finisce nel registro: chi ha chiesto, chi ha approvato, quanto è costato ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Il registro delle azioni è a sola aggiunta e i segreti vengono oscurati prima di qualsiasi log ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
9. **La ripresa.** Il Cancello mette in coda la ripresa e il runner riprende la sessione con l'esito come nuovo messaggio, ripassando modalità e opzioni ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)). Una carta lasciata ferma la notte riprende il lavoro giusto al mattino: è uno dei criteri della verifica della settimana 8 ([proposta §11](../PRESENTAZIONE-CEO.md)).
10. **Il conto.** LiteLLM conta la spesa e blocca oltre il budget. La stima di costo dell'SDK va nel cruscotto e ogni mese si confronta con la Console di Anthropic ([ricerca/36 §5.1](../ricerca/36-architettura-v2.md)).

### 4.1 Le classi d'azione e chi approva

| Classe | Esempi | Come passa |
|---|---|---|
| Lettura | cercare, leggere | consentita agli strumenti ammessi del profilo |
| Scrittura interna | to-do in Jira, meeting nel CRM, evento del debrief in Outlook | regola scritta, senza carta, a nome del responsabile; registro |
| Invio a cliente o prospect | follow-up, risposta, recap nel canale condiviso, WhatsApp | carta ad Alessandro; solo al dominio del cliente; primo contatto con FIDO2 |
| Pubblicazione | post, newsletter, risposte ai commenti, pagine del sito | carta ad Alberto o al founder del profilo |
| Offerte, contratti, affermazioni tecniche | | carta a Michele, con FIDO2 |
| Fatture e solleciti | | carta ad Alessandro o Michele, con FIDO2; pagamenti mai automatici |
| Codice e infrastruttura | modifiche alle skill, pull request, patch | carta ad Alberto, con FIDO2; le patch del server a Michele |
| Cancellazione e credenziali | | sempre negate agli agenti |

Fonti: [proposta §5.4](../PRESENTAZIONE-CEO.md) per le classi; [ricerca/36 §5.8](../ricerca/36-architettura-v2.md) per esempi e approvatori. La proposta chiede la FIDO2 per offerte, contratti, fatture e primi contatti; il piano tecnico la estende a solleciti, codice e infrastruttura.

### 4.2 Le regole "Sempre"

Quando la stessa approvazione si ripete uguale venti volte senza modifiche, una persona può trasformarla in una regola "Sempre", stretta su quell'agente, quel tipo di azione e quella destinazione. La regola scade dopo 30 giorni. Mai per offerte, primi contatti, pagamenti, cancellazioni, né per destinatari nuovi ([proposta §5.4](../PRESENTAZIONE-CEO.md)). Le regole attive si rivedono ogni mese ([ricerca/36 §5.8](../ricerca/36-architettura-v2.md)). Quali messaggi ai clienti possono diventare "Sempre" lo decidono i CEO, dopo il parere legale ([proposta, appendice A, voce B5](../PRESENTAZIONE-CEO.md)).

### 4.3 Eccezioni e freni

- **Andrea** telefona senza carta solo a chi ha chiesto di essere richiamato nel modulo, e dice subito di essere un assistente AI (decisione 10) ([proposta §1 e §5.1](../PRESENTAZIONE-CEO.md)).
- **Le routine nascono spente**: ogni automazione parte in prova a secco e per una o due settimane mostra cosa avrebbe fatto, senza farlo ([proposta §9.2](../PRESENTAZIONE-CEO.md)).
- **Lo stop di emergenza** si preme dal telefono. Ferma la coda, porta a zero i budget di LiteLLM, fa scattare il kill switch di SersanOutreach e mette in pausa le campagne di Instantly. I dati restano in PostgreSQL, BookStack, Jira e M365, e il lavoro torna a mano ([proposta §4.8 e §9.2](../PRESENTAZIONE-CEO.md); [ricerca/36 §12](../ricerca/36-architettura-v2.md)).
- **Dieci scenari di prova** girano a ogni aggiornamento, per esempio: Cancello che non risponde in tempo, chiamate in parallelo, carta scaduta, testo cambiato dopo la carta. Nessun effetto deve uscire senza una carta del Cancello ([proposta §11 e §13](../PRESENTAZIONE-CEO.md); [ricerca/36 §7.4](../ricerca/36-architettura-v2.md)).

### 4.4 Come arriva, fase per fase

| Fase | Cosa si aggiunge al percorso |
|---|---|
| 0 | Quattro prove tecniche: bot di Teams, identità di chi approva, blocco delle azioni, LiteLLM; prima parte del motore |
| 1 | Motore sul banco di prova; Cancello versione 1; invio da Outlook; carte in Teams con l'identità di chi approva |
| 2 | Motore sul server con n8n e LiteLLM; Cancello con FIDO2 e regole "Sempre" che scadono; nove bot di squadra; SersanOutreach collegato; bacheca con il freno |
| 3 | Cancello versione 2; Telegram, Slack e WhatsApp |

Fonte: [proposta §11](../PRESENTAZIONE-CEO.md). Nella fase 2 arrivano anche gli esecutori di calendario, Jira, SersanOutreach e la pausa di Instantly ([ricerca/36 §7.3](../ricerca/36-architettura-v2.md)).

---

## 5. La memoria

### 5.1 Dove sta cosa

La memoria è divisa per tipo, e ogni tipo ha una sola fonte di verità ([proposta §5.5](../PRESENTAZIONE-CEO.md)).

| Dove | Cosa contiene | Come la legge un agente |
|---|---|---|
| BookStack, sul server | le regole di lavoro di ciascuno ("Come lavoro"), i processi, il catalogo servizi, il manuale degli agenti | MCP di BookStack, in sola lettura |
| PostgreSQL, sul server | registro e organigramma degli agenti, obiettivi, prezzi, registro dei meeting, decisioni, passaggi fra agenti | MCP della memoria, in sola lettura |
| Qdrant, sul server | ciò che "connette i momenti": trascrizioni, mail, documenti, Sirius, bandi, pagine di BookStack, issue di Jira | MCP RAG, con i permessi della persona |
| Jira | to-do e progetti | MCP di Jira |
| M365 | documenti, posta e calendario | MCP di posta e calendario in lettura, solo sulle caselle in ambito |

Fonti: [proposta §5.5](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.5](../ricerca/36-architettura-v2.md). Il piano tecnico propone anche un taccuino per ogni famiglia di agenti su mcp-memory, mai con dati dei clienti ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md)); cosa faccia oggi mcp-memory nel board è una domanda aperta ([domande per Michele, n. 25](../DOMANDE-PER-MICHELE.md)).

### 5.2 Come entra

La pipeline del board rende ricercabili i documenti. Il principio è "il server cerca e prepara, Claude ragiona", e password e chiavi non entrano mai nell'indice ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)):

1. **esportazione** incrementale da Sirius di dati fiscali, clienti e documenti;
2. **Docling** trasforma PDF, scansioni e tabelle in testo strutturato;
3. **filtro**: segreti e chiavi scartati, dati personali marcati;
4. **blocchi e metadati**: Qwen3-4B scrive cliente, anno, tipo e riassunto;
5. **embedding** con Qwen3-Embedding 0.6B verso Qdrant, insieme a BM25;
6. **reranker** Qwen3-Reranker 0.6B;
7. **MCP RAG**, con i permessi per utente e il registro delle domande, verso Claude Team.

Cosa sia esattamente Sirius è una domanda aperta per Michele ([domande per Michele, n. 25](../DOMANDE-PER-MICHELE.md)). Gli embedding si calcolano sulla GPU del server, quindi il contenuto non esce per essere indicizzato ([proposta §5.5](../PRESENTAZIONE-CEO.md)). Il board ha anche una pipeline dei bandi: n8n ogni notte, Firecrawl, un riassunto con il modello da 4B, indice e notifica in Teams o per mail ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)).

Dalla fase 3 la squadra Memoria tiene viva la memoria: il Raccoglitore porta dentro posta, calendario, documenti, chat, BookStack, Jira, trascrizioni e CRM; il Pulitore deduplica, classifica, toglie i dati personali che non servono e separa il testo di terzi; il Bibliotecario risponde alle domande libere; l'Archivista applica le scadenze di conservazione ([proposta §4.7](../PRESENTAZIONE-CEO.md)).

### 5.3 Chi vede cosa

- **La persona arriva fino alla memoria.** Quando un agente lavora per Alessandro, la memoria gli mostra solo ciò che Alessandro può vedere ([proposta §5.3](../PRESENTAZIONE-CEO.md)). L'Agent SDK passa a ogni server MCP le intestazioni HTTP decise da noi, a ogni chiamata ([ricerca/36 §1.2](../ricerca/36-architettura-v2.md)).
- **Il token della persona.** Il runner firma un token a vita breve, con una chiave tenuta in Infisical, valido solo per l'MCP RAG. La persona è chi ha avviato il lavoro: l'identità Microsoft che arriva dalla Porta, o chi ha creato l'orario in n8n. Non è mai un campo scritto dal modello. Il risultato va solo a chi può vedere quei dati: nessuna risposta del lavoro di una persona finisce in un canale aperto a tutti ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md); [ricerca/35 §8](../ricerca/35-giudizio-sicurezza.md)).
- **Permessi per documento.** Qdrant ha chiavi per collezione, non per documento: i permessi fini li applica l'MCP RAG con filtri sui metadati di ogni blocco ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md)).
- **I numeri si calcolano, non si cercano.** Pipeline, margini e budget si calcolano dal codice sui dati di PostgreSQL, non si cercano nel testo ([proposta §5.5](../PRESENTAZIONE-CEO.md)).

### 5.4 Cosa arriva a Claude Team

Chiunque può chiedere anche da Claude Team "cosa ci siamo detti con X a settembre?" e avere la risposta con le fonti, vedendo solo ciò che può vedere ([proposta §5.5](../PRESENTAZIONE-CEO.md)). L'MCP RAG dà a Claude Team verde e giallo, e il rosso solo oscurato, finché parere e valutazione d'impatto non decidono. La collezione `finanza` è separata e si toglie a Claude Team con una regola ([ricerca/36 §5.5](../ricerca/36-architettura-v2.md)). Pesa il fatto che Claude Team non tiene un registro delle attività che possiamo controllare ([proposta §13](../PRESENTAZIONE-CEO.md)).

### 5.5 Quanto si conserva

- Audio fino a 30 giorni; trascrizioni e CRM 24 mesi dall'ultimo contatto; log degli agenti 90 giorni ([proposta §9.1, regola 8](../PRESENTAZIONE-CEO.md)).
- Le sessioni dell'SDK di default restano 30 giorni: il periodo si abbassa, i lavori con dati rossi non salvano la sessione e i dati stanno su un dataset cifrato di ZFS, il file system dei dischi del server ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- Una cancellazione su richiesta deve raggiungere le sessioni in PostgreSQL, Qdrant, Loki e i backup ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- Sul banco di prova, finché la fase di sicurezza F3 del board non è validata, si salvano solo dati verdi e gialli. Le trascrizioni si leggono da Graph, si oscurano in memoria con un filtro locale, vanno all'API e si conserva solo il riassunto ([proposta §11](../PRESENTAZIONE-CEO.md); [ricerca/36 §5.7](../ricerca/36-architettura-v2.md)). L'oscuramento locale si costruisce e si misura nella fase 1 ([proposta §5.6](../PRESENTAZIONE-CEO.md)).

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
| 32 AGENTI | il motore, `agenti-01`; esce solo verso LiteLLM, `mcp-01`, MCP RAG e API del Cancello | no | fase 2 |
| 35 MEET | Vexa, `meet-01` | no: Vexa esce, non riceve | fase 3 |
| 25 VOCE | Asterisk, `voce-01` | solo il trunk SIP verso gli indirizzi dell'operatore | fase 5 |

Fonti: [ricerca/36 §3 e §4.5](../ricerca/36-architettura-v2.md). Il sistema aggiunge in tutto 11-13 servizi e 3 reti nuove al perimetro Cyber Essentials ([proposta §13](../PRESENTAZIONE-CEO.md)). La VLAN 32 può diventare la 30, con il firewall di Proxmox per ogni VM, se Michele preferisce ([ricerca/36 §3](../ricerca/36-architettura-v2.md)).

### 6.3 Chi parla con chi

| Da | Verso | Cosa passa |
|---|---|---|
| Motore (32) | LiteLLM (30) | solo le chiamate ai modelli (`/v1/messages`) |
| Motore | `mcp-01`, MCP RAG, API del Cancello (30) | HTTP interno con un token per famiglia di agenti |
| Motore | internet | niente |
| LiteLLM | `api.anthropic.com` | HTTPS: l'unica uscita dei modelli |
| `cancello-01` | Graph e login di Microsoft, Bot Framework, Jira, SersanOutreach, Instantly, Telegram, Meta, Slack | HTTPS: esecutori e Porta |
| EDGE (20) | `cancello-01` | messaggi dei bot e webhook firmati dal mittente |
| EDGE | MCP RAG | l'endpoint MCP per Claude Team, con OAuth di Entra (l'accesso delegato con l'identità Microsoft) |
| MCP RAG (30) | Qdrant (40) | regola nuova da scrivere: oggi il board ha solo "AI → DATA solo Qdrant" |
| `meet-01` (35) | internet | HTTPS e audio: i bot entrano nelle call; nessuna rotta verso DATA |
| `voce-01` (25) | indirizzi dell'operatore | SIP, meglio cifrato con TLS sulla porta 5061, e l'audio RTP |
| `stage-agenti` (90) | internet | HTTPS: API con chiave limitata, Graph, bot; nessun accesso a DATA |
| OBSRV (70) | tutte | sola lettura |

Fonti: [ricerca/36 §4.4](../ricerca/36-architettura-v2.md); [domande per Michele, n. 7](../DOMANDE-PER-MICHELE.md). Le regole vanno scritte con Michele su OPNsense e nel firewall di Proxmox ([ricerca/36 §4.4](../ricerca/36-architettura-v2.md)).

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

Le voci più pesanti sono il motore (fino a 20 GB), Vexa (12 GB per tre bot) e la trascrizione (6-8 GB) ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md)).

**La regola d'acquisto.** Si misura con un tetto iniziale di 6 sessioni. Si aggiungono altri 192 GB prima della fase 3 (settimana 22), o prima se il margine misurato scende sotto i 5 GB: 12 moduli da 16 GB uguali a quelli montati, uno in più per ogni canale. È l'unico passo che tiene la memoria bilanciata, e la velocità resta quella di oggi. Costa circa 690-830 € (decisione 11) ([proposta §6.3 e §13](../PRESENTAZIONE-CEO.md); per il tetto di 6 sessioni, [ricerca/36 §4.2](../ricerca/36-architettura-v2.md)).

**Leve per rimandare l'acquisto** ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md)): Experimental-1 e 2 accese solo quando servono (24 GB); un tetto di 12 sessioni; Andrea sulla seconda GPU (4 GB in meno); Vexa Lite con una call alla volta (circa 4 GB invece di 12).

**Cento agenti.** La RAM cresce con le sessioni attive insieme, non con il numero di profili: cento profili con un tetto di 16 sessioni stanno nei 20 GB del motore ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md)).

**Note per chi monta** ([ricerca/36 §4.2](../ricerca/36-architettura-v2.md); [domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)):

- la cache ZFS va fissata con `zfs_arc_max` a 12 GiB, per restare nei 16 GB che il board dà all'host e alla cache;
- servono moduli x4 come quelli montati (16 GB 2Rx4 PC4-2133P RDIMM): con moduli x8 HPE spegne online spare, mirroring e Fast Fault Tolerance;
- i nuovi moduli vanno negli slot 2, 4, 6, 7, 9 e 11 di ogni CPU; dopo il montaggio, memtest86+ per 24 ore. L'iLO può segnalare che non sono SmartMemory HPE, cosa normale con moduli Gen9.

### 7.4 Le GPU

**Oggi, la RTX 4000.** Di giorno, con Qwen3-4B, embedding, reranker e Docling, le resta meno di 1 GB libero; la trascrizione dal vivo (circa 2,1 GB) ci entra solo se il reranker passa sulla CPU ([ricerca/36 §4.3](../ricerca/36-architettura-v2.md)). Michele la presta ogni tanto, per poco tempo, alla postazione di prova del laboratorio (Experimental-1): intanto i lavori della GPU aspettano in coda finché torna libera ([proposta §6.4](../PRESENTAZIONE-CEO.md)). Embedding e lavori a lotti possono girare sulla CPU quando serve ([proposta §13](../PRESENTAZIONE-CEO.md)).

**La seconda GPU.** Michele ha scelto la **RTX PRO 2000 Blackwell da 16 GB**: 70 W senza cavi di alimentazione e memoria più veloce della generazione precedente. Con 16 GB ci stanno insieme la trascrizione dal vivo, la voce di Andrea e la ricerca nella memoria, giorno e notte ([proposta §6.4](../PRESENTAZIONE-CEO.md)).

- **Quando.** Conviene dalla fase 3 (settimana 22), quando si trascrivono in casa le call dei clienti e la RTX 4000 è quasi piena. Serve al più tardi all'inizio della fase 5 (settimana 41), prima di spostare Andrea sulla GPU. Fino ad allora fa tutto la RTX 4000 ([proposta §6.4](../PRESENTAZIONE-CEO.md)).
- **Prezzo.** In Italia oggi costa circa 1.290-1.305 € IVA inclusa (circa 1.060 € esclusa). Conviene comprarla quando torna sotto i 1.000 € IVA inclusa (circa 820 € esclusa); se all'inizio della fase 5 costa ancora di più, si compra lo stesso. Con riser e staffa la decisione 12 vale circa 880-1.220 € ([proposta §6.4 e §14](../PRESENTAZIONE-CEO.md)).
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

**L'UPS.** Un HPE R1500 G5 da rack (1.550 VA, 1.100 W), in arrivo. Se manca la corrente, dopo 3 minuti spegne il server in modo pulito e tiene accesa la rete fino a fine batteria. Al ritorno della corrente la rete, se si era spenta, riparte da sola; il server, com'è impostato oggi, va riacceso a distanza ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Come sono collegate le prese ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)):

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

**Una sola linea internet.** Se cade la fibra, gli agenti si fermano, perché ragionano con Claude via internet, e Andrea non risponde. Nulla si perde: lavori e carte aspettano e ripartono quando la linea torna. La linea di riserva 4G/5G è consigliata prima della fase 5 (decisione 13); l'accesso da fuori passa dalla macchina Oracle e funziona anche sulla linea di riserva ([proposta §13](../PRESENTAZIONE-CEO.md)). Costa 77-200 € una tantum e 10-11 € al mese; Starlink (349 € e 31 € al mese) solo se in ufficio il segnale mobile è scarso ([proposta §14](../PRESENTAZIONE-CEO.md)).

### 7.8 Il secondo server e la durata dell'hardware

Michele prevede il secondo server già a dicembre, se c'è il budget (fino a 1.500 €): con il DL380 forma un cluster ([proposta §6.1](../PRESENTAZIONE-CEO.md)). Si collega al DL380 con un cavo diretto a 10 Gbit ([board del rack](../allegati/infra/Rack%20SerSan%2012U.md)). È una spesa del board, decisa a parte ([proposta §12.2](../PRESENTAZIONE-CEO.md)).

Il supporto HPE per lo chassis dura fino a ottobre 2029 secondo le fonti ufficiali HPE consultate da Michele; le fonti pubbliche danno stime da marzo 2028 a ottobre 2029, quindi la data si conferma con il numero di serie. Il sistema gira comunque in macchine virtuali con backup: si sposta su un server nuovo senza rifare nulla ([proposta §6.1](../PRESENTAZIONE-CEO.md)).

---

## 8. Sicurezza e conformità

### 8.1 Le difese del disegno

I cinque meccanismi di controllo della proposta ([proposta §9.2](../PRESENTAZIONE-CEO.md)):

1. **Gli agenti propongono, il codice esegue.** Nessun agente ha in mano un bottone che invia, pubblica, paga o cancella: passa sempre dal Cancello. La macchina degli agenti raggiunge solo i servizi in lista, e nessun bot entra nei canali condivisi con i clienti.
2. **Le routine nascono spente.** Ogni automazione parte in prova a secco: per una o due settimane mostra cosa avrebbe fatto, senza farlo.
3. **Il testo di terzi non è mai un'istruzione.** Email, trascrizioni, pagine web e risposte dei prospect entrano da una corsia senza strumenti.
4. **Tetti che fermano davvero.** Ogni agente e ogni catena di lavoro ha un budget: avviso all'80%, stop al 100%.
5. **Tutto è registrato e revocabile.** Registro delle azioni a sola aggiunta, segreti oscurati prima di qualsiasi log, stop di emergenza dal telefono.

Il disegno aggiunge:

- **Reti strette**: agenti in una VLAN propria senza internet, web solo da Firecrawl, Cancello in una macchina separata, un solo endpoint MCP pubblico ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- **LiteLLM come bene critico.** Custodisce tutte le chiavi, e a marzo 2026 ne sono circolate versioni compromesse. Per questo: versione fissata e controllata, uscita solo verso Anthropic, pannello raggiungibile solo dalla rete di gestione, chiave principale fra i segreti, con rotazione ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **Versioni fissate** e aggiornamento dell'SDK ogni due settimane, dopo i dieci scenari, entro i 14 giorni ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **Revisione esterna.** Prima che i dati dei clienti restino sul server, una società esterna rivede Cancello, motore e bot, entro la settimana 21 (decisione 5) ([proposta §5.4 e §14](../PRESENTAZIONE-CEO.md)).
- **Banco di prova separato.** Nelle settimane 5-8 il pilota gira su una macchina di prova nella rete del laboratorio, con una chiave API limitata e un tetto di spesa, e salva solo dati verdi e gialli finché la fase di sicurezza del board (F3) non è validata ([proposta §11](../PRESENTAZIONE-CEO.md)).
- **La fase F3 del board** porta Wazuh, NetBox, Authentik (gestione delle identità), CrowdSec (blocco degli indirizzi che attaccano), log e avvisi, e la documentazione per ISO e Cyber Essentials ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)). Wazuh scansiona le vulnerabilità di ogni VM e container ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).

### 8.2 Cyber Essentials

Cyber Essentials è la certificazione britannica di sicurezza di base, con i requisiti dell'NCSC; il board la prevede, con la documentazione nella fase F3 ([board dell'infrastruttura](../allegati/infra/SerSan%20Infra%20Board.md)). I requisiti in vigore sono la versione 3.3, con il questionario Danzell ([domande per Michele, n. 12](../DOMANDE-PER-MICHELE.md)). I controlli sono cinque: firewall, configurazione sicura, aggiornamenti, controllo degli accessi e protezione dal malware. Per i server vuol dire: aggiornamenti critici o ad alto rischio entro 14 giorni, account separati per l'amministrazione, MFA dove disponibile ([ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)).

Cosa significa per l'architettura:

- **Il perimetro cresce.** Il sistema aggiunge 11-13 servizi e 3 reti nuove al perimetro, con le patch entro 14 giorni. Ogni servizio ha un responsabile delle patch e un posto nell'inventario; prima della fase F4 entrano solo i servizi del pilota ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **I telefoni che approvano** entrano nel perimetro, anche se personali: sistema supportato, blocco schermo, MFA, aggiornamenti ([ricerca/36 §5.7](../ricerca/36-architettura-v2.md)).
- **I servizi cloud** (M365, console e API di Anthropic, Oracle) sono sempre nel perimetro, con l'MFA obbligatoria. Anche il PBS a casa di Michele probabilmente rientra ([domande per Michele, note dalla ricerca](../DOMANDE-PER-MICHELE.md)).
- **Il firewall fuori supporto.** Sul Sophos il software (Proxmox e OPNsense) è aggiornato, ma BIOS e processore no. Si chiede prima per iscritto all'ente di certificazione se accetta questa configurazione; se non la accetta, OPNsense passa su un piccolo computer ancora supportato dal produttore, con una spesa da preventivare ([proposta §13](../PRESENTAZIONE-CEO.md)).
- **Il processore del server.** Per la Gold 5218 il rischio è più basso: Intel ha chiuso il servizio generale il 30/06/2025, ma HPE aggiorna ancora la System ROM, il firmware del server (3.70 di agosto 2026) ([domande per Michele, n. 12](../DOMANDE-PER-MICHELE.md)).
- **Le versioni di Proxmox.** Proxmox VE 8 (PVE, il sistema delle macchine virtuali) e PBS 3 sono a fine vita da agosto 2026: tutte le macchine vanno su PVE 9 e PBS 4. Il repository senza abbonamento è sconsigliato in produzione; gli abbonamenti per firewall e backup sono la decisione 17 ([domande per Michele, n. 13](../DOMANDE-PER-MICHELE.md); [proposta §14](../PRESENTAZIONE-CEO.md)).

### 8.3 GDPR e dati personali

Il GDPR è il regolamento europeo sulla protezione dei dati personali.

- **Minimizzazione prima del cloud**: si oscura ciò che non serve; solo fornitori con contratto commerciale e DPA ([proposta §9.1, regola 7](../PRESENTAZIONE-CEO.md)). I tre colori dei dati sono scritti nel codice del Cancello (paragrafo 1.5).
- **Registro dei trattamenti e valutazione d'impatto** (DPIA), aggiornati a ogni nuovo agente, compresi i brief prima degli incontri, che sono profilazione ([proposta §9.1, regola 9](../PRESENTAZIONE-CEO.md)). La prima versione si fa nella fase 0, con la decisione sui dati rossi verso Claude Team entro la settimana 3 ([proposta §11 e §13](../PRESENTAZIONE-CEO.md)).
- **Conservazione con scadenze automatiche** (paragrafo 5.5) ([proposta §9.1, regola 8](../PRESENTAZIONE-CEO.md)).
- **Trasferimenti negli USA**: con tutto sul server, l'audio delle call e la voce di Andrea non passano più da fornitori negli USA ([proposta §5.6](../PRESENTAZIONE-CEO.md)). Ad Anthropic si chiede la conservazione zero dei dati delle API, che è gratuita ([proposta §14](../PRESENTAZIONE-CEO.md)).
- **Backup.** Il GDPR (art. 32) chiede di saper ripristinare i dati in tempo e di provarlo con regolarità: da qui le prove di ripristino con verbale ([domande per Michele, n. 14](../DOMANDE-PER-MICHELE.md); [ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)). Per la copia a casa di Michele serve la sua designazione scritta come autorizzato e amministratore di sistema, con i log degli accessi per almeno sei mesi ([domande per Michele, n. 16](../DOMANDE-PER-MICHELE.md)). Con dati cifrati e chiave custodita altrove, il furto della macchina di norma non va notificato ([ricerca/37 §4, Backup 3-2-1](../ricerca/37-hardware-risposte-michele.md)).
- **Il parere legale**, in due consegne: entro la settimana 3 i punti del pilota (email B2B verso l'Italia, registrazione delle call, trasferimenti verso gli USA), prima della fase 2 il resto. Fra i punti: come si applica il GDPR europeo a una Ltd con il team in Italia, i dati personali che possono arrivare a Claude Team, il valore legale della firma elettronica fatta in casa e la copia cifrata dei backup a casa di Michele ([proposta §9.4](../PRESENTAZIONE-CEO.md)).

### 8.4 AI Act

- Ogni agente che parla o scrive da solo a un esterno, come Andrea, si dichiara AI dalla prima frase (art. 50, in vigore dal 2 agosto 2026) ([proposta §9.1, regola 1](../PRESENTAZIONE-CEO.md)).
- Formazione AI documentata per tutti e quattro (art. 4), aggiornata a ogni nuovo agente ([proposta §10](../PRESENTAZIONE-CEO.md)).
- Il Coach vendite non stima le emozioni, come chiede l'AI Act ([proposta, appendice A, voce G3](../PRESENTAZIONE-CEO.md)).

---

## 9. Se un pezzo non regge

| Se non regge | Uscita | Cosa resta |
|---|---|---|
| Il motore sull'Agent SDK, alle verifiche delle settimane 8 e 21 | Hermes sullo stesso banco di prova, con gli stessi scenari; poi al posto del motore, se i numeri lo dicono e se Hermes ha chiuso i suoi problemi di sicurezza | Cancello, LiteLLM, server MCP, Porta, memoria e skill nello stesso formato |
| LiteLLM | una chiave diretta per famiglia con limiti nella Console, solo finché si corregge | i tetti di spesa del runner |
| Il bot di Teams | Azure Bot F0 gratuito; la pagina del Cancello con gli avvisi in Teams | Cancello e approvazioni con Entra e FIDO2 |
| Vexa | Attendee come piano B (escluso per Teams con login); registrazione sul PC | la trascrizione nativa delle call in Teams |
| La voce di Andrea in casa | voci migliori sulla seconda GPU; in ultima istanza una voce in cloud, come eccezione decisa dai CEO | Asterisk, Pipecat, operatore |
| Postiz | Metricool come eccezione | Pubblicatore e Community manager |
| DocuSeal | firma da un fornitore esterno | Agente contratti |
| Buzz | resta in laboratorio; la stanza degli agenti è il canale "Agenti" di Teams | bacheca, freno, specchio in Teams |
| Tutto il sistema | stop di emergenza dal telefono | i dati in PostgreSQL, BookStack, Jira e M365; il lavoro torna a mano |

Fonti: [ricerca/36 §12](../ricerca/36-architettura-v2.md); [proposta §5.7 e §13](../PRESENTAZIONE-CEO.md). Il costo in giorni dell'uscita verso Hermes è nella [proposta §15](../PRESENTAZIONE-CEO.md).

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
