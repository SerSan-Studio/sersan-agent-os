# Domande tecniche per Michele

Per la proposta SerSan Agent OS (versione 2.1), costruita sul tuo board dell'infrastruttura e aggiornata l'8 novembre 2026 con le tue risposte sull'hardware e con la board del rack. Sono le scelte tecniche che restano tue; il documento per i CEO non le contiene. Il dettaglio è in `ricerca/36-architettura-v2.md`, `ricerca/25-board-michele-e-delta.md` e, per l'hardware, `ricerca/37-hardware-risposte-michele.md`.

**Già recepito:** l'hardware già completo (192 GB, 2 Gold 5218, dischi in mirror, ventole, dissipatori, alimentatori Titanium); il motore sull'Agent SDK di Claude al posto di Hermes, che resta come uscita; tutto self-hosted tranne i servizi del tuo board.

**Recepito l'8 novembre**, dalle tue risposte e dalla board del rack:

- RAM: 12 moduli da 16 GB 2Rx4 a 2133 MHz, uno per canale. Per arrivare a 384 GB proponiamo 12 moduli uguali, che restano a 2133.
- Riser principale pieno, con la RTX 4000 e il controller degli 8 dischi: la seconda GPU va nel riser secondario.
- Seconda GPU: RTX PRO 2000 Blackwell da 16 GB, più avanti, quando il prezzo scende. Nel documento la soglia la proponiamo noi (decisione 12): sotto i 1.000 € IVA inclusa; conviene dalla fase 3 (settimana 22), serve entro la fase 5 (settimana 41) per Andrea.
- Experimental-1: poco e solo ogni tanto; intanto i lavori della GPU aspettano in coda.
- UPS HPE R1500 G5 (1.550 VA, 1.100 W), con la scheda di rete Q1C17A e l'USB al Sophos per NUT: server giù dopo 3 minuti, rete accesa fino a fine batteria.
- Firewall: Sophos SG 230 rev. 2 con Proxmox, OPNsense in VM, NetBird, AdGuard e NUT; più avanti QDevice e Proxmox Datacenter Manager. Modulo FleXi solo se finiscono le porte; 10 Gbit diretti tra il DL380 e il nodo 2.
- Nessuna linea internet di riserva per ora; più avanti 4G/5G o Starlink.
- Backup 3-2-1: PBS in sede (scheda MSI H110, 2 × 500 GB in mirror, acceso di notte con Wake-on-LAN; mancano case e dischi) e copia ogni notte a Terra Noa da marzo 2027.
- Accesso da fuori: macchina Oracle Cloud a Milano con NetBird (gestione e relay), Pangolin, Uptime Kuma e ntfy.
- Secondo nodo a dicembre, se c'è il budget (fino a 1.500 €).

**Aggiunte l'11 novembre 2026:** le domande da 31 a 45, nate con l'architettura v3. Sono in fondo, prima delle note.

## Tempi e posto per gli agenti

1. In quante settimane pensi di chiudere F0-F4? Nel piano ho ipotizzato F0-F1 nelle settimane 1-5, F2-F3 nelle 6-14, F4 nelle 15-18, F5 dalla 19.
2. Puoi anticipare un "posto agenti" (LiteLLM, PostgreSQL 16, Infisical, n8n e due VM nella VLAN APPS) prima di F4, o partiamo con il pilota su una VM di prova nella VLAN LAB appena F1 è validata?
3. Nel trunk della board del rack ci sono anche le VLAN 35 e 85. La 35 è la MEET che avevamo proposto? La 85 è per gli agenti, senza internet, o per la voce? Se nessuna delle due, il motore lo mettiamo in una VLAN nuova (32 AGENTI) o nella 30 APPS con il firewall di Proxmox per VM?

## Rete ed esposizione

4. Macchina Oracle a Milano:
    - teniamo Pangolin in TLS passthrough verso Traefik, così il traffico dei clienti si apre solo in casa?
    - Il piano gratuito ha due limiti. Oracle si riprende le macchine che per 7 giorni restano sotto il 20% di CPU, rete e memoria, e NetBird, Pangolin e Uptime Kuma ci restano quasi sempre. E Milano ha una sola zona: se mancano macchine gratuite non c'è alternativa. Passiamo l'account a consumo (Pay As You Go)? Secondo un'email di Oracle del 2023 le risorse gratuite restano gratuite e non vengono più recuperate; la documentazione di oggi non lo dice.
    - Alla registrazione va scelta Milano come regione di casa, che poi non si cambia. Le macchine Ampere gratuite oggi hanno 2 core e 12 GB, non 4 e 24 come scrivono molte guide.
    - Con l'accesso da Oracle l'IP fisso serve ancora?
5. Il bot di Teams "Teams-managed" non chiede una sottoscrizione Azure, ma alcuni segnalano errori 401. Se non funziona, ammetti una registrazione Azure Bot F0 gratuita, senza risorse accese?
6. Ammetti l'endpoint pubblico dell'MCP RAG per Claude Team, pubblicato da Pangolin sulla macchina Oracle, con OAuth Entra e il filtro sugli IP di Anthropic (160.79.104.0/21)?
7. Oggi il board ha "AI → DATA solo Qdrant": serve anche la regola MCP RAG (APPS) → Qdrant (DATA).
8. Nella board la fibra entra in E0 e il trunk verso il DL380 esce da E1, cioè dalla stessa coppia con bypass LAN (E0/1). Se il bypass scatta, a Sophos spento o bloccato, la fibra resta collegata direttamente al trunk del server. Disattiviamo il bypass nel BIOS e lo proviamo a Sophos spento, oppure spostiamo la WAN su una porta senza bypass (E4 o E5)?

## Servizi nuovi e Cyber Essentials

9. Ammetti le VLAN 25 VOCE e 35 MEET e questi servizi, con le fasi del piano: MariaDB (per BookStack), Vexa, servizio di trascrizione, Asterisk, Pipecat, Postiz, listmonk, DocuSeal, fatturazione? Chi patcha ognuno?
10. Ammetti come esterni: un operatore telefonico italiano (Messagenet) per Andrea, Meta per WhatsApp, Telegram, Slack, un relay SMTP per la newsletter e gli strumenti commerciali che restano (Apollo, Higgsfield, Metricool fino a Postiz)?
11. MinIO è archiviato e non più mantenuto: con cosa lo sostituisci, per audio e file degli agenti?
12. Cyber Essentials v3.3 (questionario Danzell): il questionario chiede marca e modello del firewall, e il Sophos SG 230 è fuori supporto dal 30/06/2026 per tutte le revisioni; BIOS e processore non ricevono più correzioni (Intel ha chiuso gli aggiornamenti dell'i3-6100 il 30/09/2022, e lo stesso vale per il Pentium G4400 e l'i5-6500T, tutti Skylake). Chiediamo per iscritto all'ente di certificazione se accetta OPNsense aggiornato su questo hardware? Per la Gold 5218 il rischio è più basso: Intel ha chiuso il servizio generale il 30/06/2025, ma HPE aggiorna ancora la System ROM (3.70 di agosto 2026).
13. Proxmox VE 8 e PBS 3 sono a fine vita da agosto 2026: tutte le macchine vanno su PVE 9 e PBS 4. Per Cyber Essentials l'abbonamento non serve: basta che Proxmox dichiari la durata del supporto, che segue quella della Debian corrispondente, e all'assessore portiamo le due prove. Il repository senza abbonamento però è sconsigliato in produzione. Vuoi l'abbonamento Community anche sul Sophos (1 socket, circa 10 € al mese) e sui due PBS (46,67 € al mese ciascuno)? Nel documento per i CEO è la decisione 17.

## Backup

14. Cyber Essentials non chiede il backup (la v3.3 lo raccomanda soltanto); lo chiedono il GDPR (art. 32) e la ISO 27001 (A.8.13), con prove di ripristino. Proposta:
    - il PBS di Terra Noa tira i backup in pull dal PBS in sede, con un utente che in sede ha solo lettura, senza "remove vanished" e solo con gli snapshot cifrati;
    - il token del Proxmox verso il PBS in sede ha il solo ruolo DatastoreBackup: aggiunge backup ma non li cancella;
    - una sola chiave di cifratura, custodita fuori da casa tua;
    - verify ogni giorno, riverifica completa ogni mese, prova di ripristino ogni trimestre con verbale.

    Va bene?
15. Spazio: 2 × 500 GB in mirror bastano all'inizio, non per tutte le VM del server. Misuriamo l'occupato vero e passiamo a 2 × 4 TB (circa 340-360 € IVA esclusa) quando supera i 400 GB circa? Con il PBS acceso solo di notte, i job saltati perché la macchina era spenta ripartono da soli? La documentazione non lo dice. A Terra Noa la copia va sul disco interno dell'M920q: è l'NVMe da 256 GB, meno dei 500 GB del PBS in sede, o aggiungi un disco? Se serve, lo mettiamo nel costo del nodo.
16. La copia a casa tua: per il GDPR serve una tua designazione scritta come autorizzato e amministratore di sistema (provvedimento del Garante del 2008, con i log degli accessi per almeno sei mesi). L'abbiamo messa tra i punti del parere legale: ti va bene?

## Hardware

17. Riser: nella posizione secondaria c'è solo la copertura posteriore o già una gabbia? Se manca, il kit 870548-B21 comprende la gabbia 875056-001 e il riser 875058-001 (HPE PartSurfer). I prezzi vanno da circa 66 € su eBay.de (Tonitrus, gabbia da far confermare) a circa 145 € da ETB Technologies (con gabbia e un anno di garanzia); il sito di ETB non si legge in automatico, quindi il prezzo va ricontrollato a mano. La PRO 2000 va nello slot 5 (x16) e copre lo slot 4. La PNY retail VCNRTXPRO2000B-PB ha già la staffa ad altezza piena; se la staffa non chiude con il fermo della gabbia, HPE prevede la gabbia senza fermo P38515-B21.
18. Software sulla Blackwell:
    - driver Linux 580.76.05 o successivo con i moduli open, che vanno bene anche per la RTX 4000;
    - CTranslate2 e faster-whisper girano via JIT, senza codice nativo per sm_120: vanno provati, con la cache CUDA su un volume persistente;
    - l'immagine di trascrizione di Vexa parte da CUDA 12.3 e va ricostruita su 12.8 o successivo.

    Proviamo tutto prima di spostare la trascrizione?
19. Experimental-1: le finestre le teniamo fuori dall'orario delle call? Se una call cade lì, la trascrizione dal vivo aspetta in coda. E la VM resta spenta quando non ha la GPU, così la sua RAM resta libera?
20. UPS: con la seconda GPU e 384 GB il picco stimato del server è di 800-850 W, e con firewall e rete di 860-945 W. Regge, con 6-7 minuti di autonomia al picco. Con il nodo 2 sul gruppo 2, al picco i due server possono superare i 1.100 W: mettiamo un tetto di potenza dall'iLO o prendiamo un secondo UPS? Le batterie sono usate e senza garanzia. Se il test va male, il kit originale 796776-001 costa circa 520 € più IVA, sei batterie compatibili da 6 V 9 Ah (per esempio CSB HRL634WF2) circa 120 € più IVA. Il manuale HPE chiede batterie HPE e, per il cambio fatto da noi, di spegnere il carico e l'UPS.
21. Nel messaggio parlavi di circa 30 minuti di autonomia; la board del rack spegne il server dopo 3 minuti e tiene accesa la rete. Nel documento abbiamo messo i 3 minuti: è giusto? Con la tabella HPE, a 330 W l'UPS dà 23 minuti con batterie nuove.
22. Ritorno della corrente: la board mette il DL380 su Automatic Power-On "Restore Last Power State". Dopo lo spegnimento pulito comandato da NUT l'ultimo stato è "spento", quindi al ritorno della corrente il server resta spento, e la board dice di riaccenderlo con iLO o Wake-on-LAN. Lo lasciamo così, lo mettiamo su "Always Power On" o lo fa riaccendere il Sophos al ritorno della corrente? Durante il test di autonomia proviamo anche la riaccensione. Nel documento abbiamo scritto che oggi il server va riacceso a distanza.
23. Fine del supporto HPE del DL380: ottobre 2029 l'hai letto sul portale HPE con il numero di serie o nella comunicazione HPE a00139049? Le fonti pubbliche che abbiamo trovato danno solo stime di terzi, da marzo 2028 a ottobre 2029. Nel documento la data resta tua, da confermare con il numero di serie.
24. Linea di riserva, quando la aggiungi: 4G/5G con una SIM dati aziendale come seconda WAN di OPNsense in failover (Iliad Business 180 GB a 9,99 € più IVA, TIM Company Dati 100 GB a 10,99 € più IVA), con un router da circa 67 € più IVA (TP-Link Archer MR400, 4G) a circa 190 € più IVA (Teltonika RUT241); Starlink Business (31 € al mese e kit da 349 €, entrambi più IVA) solo se in ufficio il segnale mobile è scarso. TIM chiede una partita IVA italiana e il contratto MultiBusiness; per Iliad il requisito non l'abbiamo verificato. A chi intestarla lo decidete tu e Alessandro (decisione 13 del documento per i CEO): qui ti chiediamo operatore e router. Nel documento la consigliamo prima della fase 5, quando Andrea risponde al telefono: ti va bene?

## Dati e servizi del board

25. Cos'è Sirius? E cosa fanno oggi mcp-enrich, mcp-memory e runner-dash?
26. "Supabase, DB del prodotto" è il database di SersanOutreach? Se un giorno viene in casa, meglio PostgreSQL 17 per non tornare indietro di versione.
27. Quale piano M365 e quale piano Jira abbiamo oggi? Chi è Global Administrator per i consensi di Graph?

## Per tutti e quattro

28. TypeScript va bene come linguaggio del motore anche per Mattia?
29. Chi fattura (Sersan Limited nel Regno Unito o un soggetto italiano) e con quale sistema?
30. I clienti usano Teams, Slack o WhatsApp? Per quali casi serve WhatsApp e chi approva i modelli di Meta?

## Domande nate con l'architettura v3 (novembre 2026)

Il 10 novembre i CEO hanno approvato il progetto e l'architettura è passata alla versione 3: il Cancello a livelli e il motore a due corsie ([ricerca/45](ricerca/45-architettura-v3.md)). L'11 novembre si è aggiunto l'instradamento a più motori ([ADR-0028](docs/adr/0028-instradamento-a-piu-motori.md)). Le domande da 1 a 30 restano valide; dove una domanda nuova ne aggiorna una vecchia, lo dice. Nessuna di queste scelte ferma lo sviluppo in corso, che gira sulle macchine di sviluppo con dati di prova.

### Dove girano i processi

31. **Cancello, motore e Sala di controllo: una VM o due?** Nella versione 2 il Cancello aveva una macchina sua. Nella versione 3 la macchina separata non è più obbligatoria: i processi possono stare sulla stessa VM, e i ruoli separati del database restano ([ADR-0023](docs/adr/0023-protezioni-essenziali.md)). Quale delle due preferisci, e in quale VLAN (domanda 3)?
32. **L'ingresso degli eventi.** Il motore riceve tutto su un solo indirizzo, `POST /eventi`: lo chiamano la tabella degli orari, il lettore di Graph e i servizi esterni che ci servono, come il modulo del sito e Instantly, ognuno con il suo token ([ADR-0022](docs/adr/0022-eventi-e-sveglia-nel-motore.md)). Per i servizi esterni questo indirizzo va esposto dietro la porta d'ingresso del server. Lo pubblichi da Pangolin sulla macchina Oracle, come l'MCP RAG della domanda 6, o preferisci che il motore legga quei servizi a intervalli dall'interno, senza niente di esposto?
33. **n8n.** Orari ed eventi ora stanno nel motore, e il sistema di agenti non dipende più da n8n ([ADR-0022](docs/adr/0022-eventi-e-sveglia-nel-motore.md)). Lo tieni nel board per altri collegamenti? Sul banco di prova della fase 1 ne facciamo a meno, se sei d'accordo.
34. **Buzz sul banco di prova.** La prova di Buzz è anticipata: si fa con dati verdi appena c'è la bacheca degli agenti ([ADR-0026](docs/adr/0026-bacheca-e-gruppi-degli-agenti.md)). Lo ammetti, e su quale macchina?

### Fornitori e modelli

35. **TypeSafe (Jev) come fornitore per i dati gialli.** Jev è il modello che risponde alle domande chiuse del decisore. Ha un DPA con le clausole UE, ma è un servizio statunitense senza SLA, con la conservazione zero solo per i clienti enterprise ([ricerca/47 §5.3](ricerca/47-modelli-system-one.md)). Senza il tuo sì Jev decide solo sui testi verdi ([ADR-0027](docs/adr/0027-decisore.md)).
36. **OpenRouter per i modelli open-weight a consumo.** Solo dati verdi e gialli, con le opzioni `data_collection: deny` e `zdr: true` in ogni richiesta. La regione UE chiede il piano Business e non vale per tutti i modelli ([ricerca/48](ricerca/48-modelli-locali-e-gpu.md)). Lo ammetti?
37. **L'Auto Router di LiteLLM** è marcato «Add-on»: è gratuito o a pagamento ([ricerca/47 §5.3](ricerca/47-modelli-system-one.md))?
38. **Un decisore in casa.** Quanti core della CPU di `agenti-01` si possono dare a un modello piccolo, e quanta memoria resta libera di giorno nella RTX 4000 ([ricerca/47 §5.3](ricerca/47-modelli-system-one.md))?

### Sessioni di Claude Code sui posti Team (corsia T)

Per i lavori di sviluppo lunghi il motore può far partire una sessione di Claude Code sul posto Team della persona responsabile. Il lavoro torna come pull request in bozza, e il merge su `main` lo approva una persona ([ADR-0028](docs/adr/0028-instradamento-a-piu-motori.md); [ricerca/49 §9](ricerca/49-instradamento-a-piu-motori.md)).

39. **Quali repo entrano**, una per una. Su quelle repo servono queste regole di GitHub, senza eccezioni per gli amministratori: l'app di Claude solo lì; `main` solo con pull request e con l'approvazione di una persona diversa dall'ultima che ha fatto push; la regola di push sui workflow.
40. **Il runner sul nostro server.** All'inizio le sessioni girano sulle macchine di Anthropic, senza dati rossi. Un runner nostro lo vuoi? Su quale macchina e con quale rete in uscita? Si accende solo dopo la prova.
41. **La revisione delle pull request.** Automatica, con un workflow di GitHub e la chiave API, oppure solo da parte delle persone?

### Hardware: cosa cambia rispetto alle domande 17-24

42. **Seconda GPU, prima del previsto.** La proposta nuova è comprare la RTX PRO 2000 Blackwell da 16 GB per la milestone 2, anche a 1.100 € (prezzo di Amazon.it del 10 novembre), senza aspettare che scenda sotto i 1.000 €. Serve alla prova dei modelli locali: la RTX 4000 ha meno di 1 GB libero, e alcuni modelli da provare girano solo sulla Blackwell. La scheda da 24 GB della stessa classe costa più di tre volte tanto e non la proponiamo ([ADR-0014](docs/adr/0014-seconda-gpu-blackwell.md); [ricerca/48 §5](ricerca/48-modelli-locali-e-gpu.md)). Ti va bene? Questa domanda aggiorna il punto «Seconda GPU» in testa al file.
43. **RAM a 384 GB.** All'inizio della fase 3, o prima se il margine misurato con sei sessioni della corsia S scende sotto i 5 GB ([ADR-0015](docs/adr/0015-ram-384-gb.md)). Il margine lo misuriamo appena il runner della corsia S gira sul server. Va bene questa regola?
44. **Linea di riserva, prima.** La domanda 24 la consigliava prima della fase 5. Ora serve prima del primo lavoro che un agente fa da solo verso l'esterno fuori orario: senza fibra gli agenti si fermano, perché ragionano con Claude via internet ([ADR-0019](docs/adr/0019-linea-di-riserva.md)). Operatore e router restano scelte tue.
45. **Riaccensione dopo un blackout.** Con la sveglia dentro il motore, se il server resta spento il debrief delle 7:00 salta ([ADR-0022](docs/adr/0022-eventi-e-sveglia-nel-motore.md)). È un motivo in più per chiudere la domanda 22 con «Always Power On» o con la riaccensione dal Sophos.

## Note dalla ricerca, senza risposta richiesta

- **RAM**: servono moduli x4 come quelli montati (16 GB 2Rx4 PC4-2133P RDIMM). Con moduli x8 HPE spegne online spare, mirroring e Fast Fault Tolerance. Vanno negli slot 2, 4, 6, 7, 9 e 11 di ogni CPU. L'iLO può segnalare che non sono SmartMemory HPE, cosa normale con moduli Gen9. Dopo il montaggio, memtest86+ per 24 ore.
- **GPU**: nessuna Blackwell è qualificata HPE per il DL380 Gen10. Controlla in iLO ventole e temperatura prima e dopo, con iLO e Innovation Engine aggiornati e il profilo Optimal Cooling. La PRO 2000 sta sulla CPU 2: niente modelli divisi tra le due GPU, e i suoi servizi legati al nodo NUMA della CPU 2.
- **Sophos**:
  - OPNsense in VM con schede virtio su bridge. Nella 230 rev. 2 le porte stanno dietro uno switch PCIe, che può impedire il passthrough di una singola porta.
  - Alla VM almeno 8 GB, senza ballooning.
  - C'è un solo SSD: va salvata sul PBS la configurazione di OPNsense e del Proxmox del Sophos.
- **Fibra a 2,5 Gbit**: con E0 in rame da 1 Gbit si arriva a circa 940 Mbit/s, che per noi bastano. Il modulo FleXi 2×10GbE SFP+ (SGIZTCHF2, solo usato, circa 420 €) va solo a 1 o a 10 Gbit. Per i 2,5 Gbit servirebbe un SFP+ RJ45 con adattamento di velocità, da provare con l'ONT (Sophos ammette transceiver fino a 1 W), oppure un piccolo switch 2,5G con SFP+.
- **QDevice**: un container Debian con corosync-qnetd sul Proxmox del Sophos, fuori dal cluster, con la porta TCP 5403 aperta dai due nodi.
- **NUT**: la R1500 G5 non è nella lista di compatibilità di NUT. Via USB dovrebbe funzionare usbhid-ups con il sottodriver mge-hid, che riconosce gli UPS HP con ID 03f0 e prodotti 1fe5-1fe8: va controllato con lsusb. Via la scheda Q1C17A c'è snmp-ups, con le MIB da provare (cpqpower o ietf). Il modulo di gestione dell'UPS, l'iLO e la 561FLR-T non devono essere raggiungibili da internet.
- **Cyber Essentials**: i servizi cloud (M365, console e API di Anthropic, Oracle) sono sempre in ambito, con l'MFA obbligatoria. Anche il PBS a casa tua probabilmente rientra nell'ambito.
