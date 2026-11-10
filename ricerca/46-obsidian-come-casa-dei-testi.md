# Obsidian come casa dei testi: confronto con BookStack

> Terzo giro di valutazione (autonomia), 10 novembre 2026. Risponde alla domanda del 10/11: «valuta anche Obsidian, è già stato giudicato?». La risposta breve è no. Finora Obsidian era solo una riga «non verificato» in [ricerca/12](12-altre-piattaforme.md) (righe 174 e 186). Questo rapporto lo confronta con BookStack, la scelta di [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md).

**Metodo.**
- I fatti su Obsidian vengono da un rapporto di raccolta di questo giro. Ha letto la documentazione ufficiale e i repository GitHub il 10/11/2026. Riporto le fonti come le ha indicate.
- I fatti su BookStack vengono da [ricerca/29](29-conoscenza-task-e-documenti.md), rilevati il 25/10/2026. Oggi non li ho riletti sul web.
- I requisiti vengono dalla repo (ADR, ricerca/29, 36, 38, 45, docs/03, la proposta per i CEO).
- **Revisione scettica, 10/11/2026.** Un secondo lettore ha riletto sul web i fatti che reggono la raccomandazione (licenza, prezzi, Sync condiviso, Headless, CLI, Bases, roadmap, plugin, storia delle versioni, Obsidian Git, Quartz, API di BookStack). I fatti reggono, con tre aggiunte al §2. I voti invece no: la revisione ha corretto A, B e D (§5), aggiunto i casi non considerati (§4-bis) e cambiato la raccomandazione (§7). Le parti cambiate lo dicono.
- **Seconda revisione scettica, 10/11/2026.** Un terzo lettore ha riletto di nuovo sul web licenza, prezzi, Sync condiviso, storia delle versioni, Headless, CLI, Bases, roadmap, sicurezza dei plugin e di Sync, Quartz e tutta la pagina delle API di BookStack. I fatti su Obsidian reggono, con una correzione (Sync fonde le modifiche, §4-bis). Sull'API di BookStack due fatti nuovi pesano sull'autonomia di A: non ci sono endpoint per leggere o ripristinare le revisioni, e non c'è un controllo di versione sulle scritture. Il voto di autonomia di A torna a 6 e la raccomandazione cambia ancora (§5, §7). Le parti cambiate sono segnate «(rev. 2)».

Etichette:
- **[verificato: fonte, data]**: letto sulla fonte indicata.
- **[non verificato: motivo]**: dato di terzi, pagina non letta o prova non fatta.
- **[proposta]**: una mia indicazione, non un fatto.
- **[calcolo]**: conto fatto sui prezzi citati.

---

## In breve

1. **Obsidian non entra come casa dei testi.** Da solo non ha permessi, non ha SSO e per più persone richiede Sync, che è un cloud fuori dal board. Il suo punto forte è il formato: file Markdown con YAML [verificato: §2].
2. **Totali dopo la seconda revisione:** B (Markdown in git) 66,5 · C (misto) 66,0 · A (BookStack) 63,5 · D (Obsidian Sync) 61,0, su 100. La prima stesura dava B 76,0, D 69,5, C 66,0, A 63,5 e contava poco il lavoro non stimato di B. La prima revisione dava A 67,0, ma alzava l'autonomia di A senza sapere che l'API di BookStack non legge né ripristina le revisioni (§3 A, §5).
3. **Raccomandazione [proposta]:** B è avanti di 3 punti, ma la differenza sta dentro l'incertezza dei voti e il lavoro di B non è stimato. Oggi non serve scegliere: la milestone 1 non ha casa dei testi in nessuna delle due strade. L'ADR-0005 (BookStack) resta in vigore finché non si decide; niente ADR-0027 per ora. La scelta fra A e B si fa prima della fase 2, sulle prove del §9 e sulla stima di B.
4. **B passa** se la prova con i CEO riesce, se la stima del suo lavoro (sito con permessi per gruppo, MCP «testi», flusso Teams, hook di indicizzazione) resta nell'ordine di BookStack più MCP, cioè circa 2-4 gp [verificato: ricerca/29 righe 345-346; ricerca/36 righe 546 e 928], e se la cancellazione da git e dalle copie è provata. Altrimenti resta A.
5. **Obsidian non è la casa dei testi** in nessun caso: al massimo un editor facoltativo sul PC, sopra la cartella di B.

---

## 1. I requisiti

Sono le voci R-01…R-15 raccolte dalla repo. Qui le riassumo; le fonti sono indicate per voce.

| R | Cosa chiede | Fonte |
|---|---|---|
| R-01 | Contenuti: regole «Come lavoro» (una pagina per persona, modello fisso), processi, catalogo, manuale degli agenti, proposte degli agenti, skill (o loro copia), organigramma, «perché» degli obiettivi | [verificato: ADR-0005 «Decisione»; ricerca/29 §2 e §3.2; ricerca/36 §5.5; docs/03 §3.1] |
| R-02 | Chi scrive: «Come lavoro» solo la persona; processi proposti dal Mappatore e approvati da Michele; catalogo Michele; organigramma generato. Gli agenti non cambiano le pagine ufficiali, salvo dopo una carta, con `changelog` che cita agente e carta | [verificato: ricerca/29 §2 e §3.2; docs/05 riga 434] |
| R-03 | Chi legge: tutti gli agenti (catene N e sessioni S), le persone, Claude Team solo via MCP RAG | [verificato: ricerca/45 §3.2; docs/03 §5.1 e §5.4] |
| R-04 | Ogni lavoro carica prima le regole «Come lavoro» della persona, per ID stabile. Alcuni campi li legge il codice (per esempio l'orario per la finestra L2) | [verificato: ricerca/45 §2.6 e §3.2; ricerca/38 AU-17] |
| R-05 | Gli agenti non hanno internet: parlano con LiteLLM, i server MCP in VLAN 30 e il Cancello | [verificato: docs/03 §1.3 e §2.2] |
| R-06 | Scrittura degli agenti: libro delle proposte a L3; processi a L2 nella proposta P-A; ogni modifica ufficiale passa da una carta | [verificato: ricerca/45 §2.2; ricerca/42-A riga 540; ricerca/39 riga 108] |
| R-07 | Permessi per libro e per famiglia di agenti. Solo dati gialli e verdi; i rossi restano fuori. Bastano permessi semplici | [verificato: ricerca/29 §2 e §3.2; ricerca/45 §6.2; ADR-0023] |
| R-08 | Le persone lavorano da PC e telefono; da fuori si entra solo con NetBird. Due CEO non sono tecnici | [verificato: docs/03 §2.1; ricerca/21-giudizio-ceo riga 44] |
| R-09 | Login con Entra, MFA, FIDO2; chi scrive è riconoscibile per nome | [verificato: docs/03 §2.1 e §5.3] |
| R-10 | Tornare a una versione precedente; «annulla senza cancellare»; diritto alla cancellazione | [verificato: ricerca/29 §3.2; ricerca/45 §2.5; ADR-0005 «Rischi»] |
| R-11 | Ogni pagina entra in Qdrant con `fonte` e `acl`. Dal 10/11 gli eventi entrano da `POST /eventi` del motore | [verificato: ricerca/29 §3.2 e §8.6; ADR-0022] |
| R-12 | Ogni servizio va in VLAN DATA, nei backup PBS, nel monitoraggio, con un responsabile delle patch | [verificato: ricerca/29 §3.3; docs/03 §3.3] |
| R-13 | Self-hosted salvo i cloud del board; nessun ostacolo alla rivendita; un'istanza per cliente | [verificato: ADR-0005; ricerca/45 §4.2 e §10] |
| R-14 | Una cosa, un posto: ogni dato ha una sola fonte di verità | [verificato: ricerca/29 §2 e §11] |
| R-15 | Tempi: milestone 1 senza casa dei testi (regole a schema nel codice); BookStack previsto in fase 2 | [verificato: ricerca/45 §3.2 e §6; ricerca/36 riga 546] |

**Un fatto che pesa sul confronto.** Molti testi che leggono le macchine nascono già in Markdown e YAML in git: registro dei profili degli agenti, `config/livelli.yaml`, i `CLAUDE.md` di squadra, le skill, prompt e schemi delle catene [verificato: spec rev. 2 §4.1; ricerca/45 §2.3; docs/03 §3.1; ricerca/43-giudizio-ceo riga 92]. Con BookStack questi testi avrebbero una copia o una vista. Con una cartella Markdown starebbero tutti in un posto solo.

**Tre incoerenze già nella repo** che la scelta deve chiudere:
- quando si scrivono le regole: «settimane 1-2 in BookStack» (PRESENTAZIONE-CEO.md riga 529) contro «BookStack dalla fase 2» (ricerca/45 §3.2);
- dove sta il registro degli agenti: PostgreSQL (ADR-0005) contro file in git (docs/03 §3.1);
- dove stanno le proposte di skill: BookStack (ricerca/36 §5.5) contro git con una PR (docs/03 §3.1).

---

## 2. Cosa è Obsidian, in breve

- **Licenza.** L'app è gratuita anche per uso commerciale. La licenza commerciale (50 USD per utente all'anno) è facoltativa [verificato: obsidian.md/license e obsidian.md/pricing, 10/11/2026]. Il codice non è aperto; le note sono file Markdown in chiaro [verificato: obsidian.md/help/data-storage, 10/11/2026].
- **Dati.** Un vault è una cartella di file `.md`. Le proprietà sono YAML in testa al file. Obsidian vede da solo i cambiamenti fatti da altri programmi [verificato: data-storage e properties, 10/11/2026].
- **Tabelle.** Le Bases danno viste a tabella, lista, schede, kanban e mappa sulle proprietà dei file. Non sono un database relazionale [verificato: obsidian.md/help/bases e roadmap, 10/11/2026].
- **Più persone.** Solo Obsidian Sync ha vault condivisi: fino a 20 utenti, un abbonamento a testa, nessun ruolo, nessuna sola lettura, nessuna modifica in tempo reale. I dati stanno su DigitalOcean (si può scegliere Francoforte), cifrati end-to-end. Non esiste una versione self-hosted [verificato: obsidian.md/help/sync/collaborate, sync/security e teams/sync, 10/11/2026].
- **Sul server.** L'app non è fatta per girare senza schermo. La CLI ufficiale vuole l'app accesa. Obsidian Headless (`ob`) sincronizza con Sync senza app, ma è in beta e richiede l'abbonamento [verificato: obsidian.md/help/cli e sync/headless, 10/11/2026].
- **Per gli agenti.** Nessun server MCP ufficiale, e AI e MCP non sono in roadmap. Gli MCP della comunità leggono i file o passano dal plugin Local REST API, che gira dentro l'app accesa [verificato: obsidian.md/roadmap/; github.com/coddingtonbear/obsidian-local-rest-api; github.com/cyanheads/obsidian-mcp-server, 10/11/2026].
- **Plugin.** I plugin della comunità hanno pieno accesso a file, rete e sistema; Obsidian «cannot reliably restrict plugins» [verificato: obsidian.md/help/plugin-security, 10/11/2026].

**Aggiunte della revisione** [verificato: pagine indicate, 10/11/2026]:
- **Storia condivisa.** La storia delle versioni non dice chi ha fatto ogni modifica. Dice solo chi ha modificato il file per ultimo, e solo sul desktop. Le note restano 1 mese (Standard) o 12 mesi (Plus); gli allegati 2 settimane [obsidian.md/help/sync/version-history].
- **Headless.** I binari pronti sono per Windows e macOS; su Linux funziona senza l'addon e perde solo la data di creazione. La pagina avverte di non usare sullo stesso dispositivo sia la Sync dell'app sia Headless, perché crea conflitti [obsidian.md/help/sync/headless].
- **Roadmap.** «Obsidian for Work» (controllo di plugin e funzioni in azienda) è «Active»; «Multiplayer» (modifica insieme) è «Planned». Il prodotto per le aziende si sta muovendo, quindi D e i giudizi su Obsidian vanno riletti fra qualche mese [obsidian.md/roadmap/].
- **Quartz.** La pagina non parla di login né di pagine private. Il sito è unico per tutti: i permessi per gruppo vanno fatti nel proxy, per percorso, oppure con un sito per gruppo [non verificato: da progettare].

**Conclusione di fatto:** la parte forte di Obsidian è il formato, cioè file Markdown con YAML. Tutto il resto (sincronizzazione condivisa, CLI, API) è nel cloud del fornitore oppure richiede l'app accesa su un PC.

---

## 3. Le opzioni

### A. BookStack, come nell'ADR-0005

Un wiki web sul server, con MariaDB. Le persone scrivono nel browser. Gli agenti leggono con un MCP (di comunità o nostro) e scrivono nel libro delle proposte. Le pagine ufficiali cambiano dopo una carta, con il parametro `changelog`. Il webhook `page_update` porta le pagine in Qdrant [verificato: ricerca/29 §3.1-§3.4].

**Aggiunta della revisione.** L'API di BookStack accetta tag con nome e valore sulle pagine, per esempio `{"name": "Category", "value": "..."}`. Il `changelog` va da 1 a 180 caratteri. Quindi i campi fissi di «Come lavoro» (orario, non disturbare, tono) possono stare nei tag della pagina e il codice li legge dall'API, senza copia in PostgreSQL [proposta]. La modifica chiesta in Teams, con carta e `changelog`, funziona anche con BookStack: non è un vantaggio solo di B [proposta].

**Aggiunta della seconda revisione** [verificato: demo.bookstackapp.com/api/docs, letta per intero il 10/11/2026]:
- **Revisioni.** L'API non ha endpoint per leggere o ripristinare le revisioni di una pagina. Le pagine hanno solo elenco, creazione, lettura, modifica, cancellazione ed export. Il ripristino del cestino vale per gli elementi cancellati, non per le revisioni. La lettura di una pagina dà solo il numero di revisioni (`revision_count`).
- **Scritture vicine.** La documentazione non parla di controllo di versione sulle modifiche: niente ETag, niente rifiuto se la pagina è cambiata.
- **Tag.** Sono testo libero: chi modifica la pagina nel browser può cambiarli o cancellarli, e BookStack non controlla uno schema [deduzione dalla stessa pagina].
- **Cosa vuol dire per gli agenti.** Un agente non può «annullare» da solo una modifica: deve rimettere il testo vecchio, che il motore deve aver salvato prima (per esempio nella carta). Il ritorno a una revisione resta un'azione da interfaccia web, cioè di una persona [deduzione]. Il motore deve controllare lo schema dei tag a ogni lettura [proposta].

### B. Cartella Markdown in git sul server, fonte unica [proposta]

- **Dove.** Un repository git nudo (`testi.git`) sulla VLAN 30, raggiunto via SSH. Non serve un server git con interfaccia. Il motore ne tiene una copia di lavoro.
- **Come sono fatti i file.** Una cartella per tipo: `come-lavoro/`, `processi/`, `catalogo/`, `manuale/`, `proposte/`, `skill/`. Ogni file ha un'intestazione YAML con `id`, `colore`, `acl`, `proprietario` e i campi fissi: per «Come lavoro», per esempio, `orario`, `non_disturbare`, `tono`. Lo schema lo controlla il motore.
- **Agenti.** Leggono i file attraverso il motore o un piccolo MCP «testi» in sola lettura, che filtra per cartella e famiglia secondo `acl`. Scrivono solo in `proposte/`, a L3. Le modifiche ufficiali passano dalla carta. Dopo il sì il motore fa il commit con un'intestazione `Agente:` e `Carta:` [proposta].
- **Persone.**
  1. **Per cambiare:** lo chiedono in Teams («sposta il mio orario di non disturbo alle 18»). L'agente prepara la modifica, la persona conferma con una carta, il motore fa il commit a nome della persona.
  2. **Per leggere:** un sito statico di sola lettura generato dalla cartella, per esempio con Quartz, dietro un proxy con login Entra, raggiungibile da PC e telefono via NetBird. Quartz v5.1.0 gira in Docker e legge la sintassi di Obsidian [verificato: quartz.jzhao.xyz, 10/11/2026]. Il login davanti va progettato [non verificato].
  3. **Per chi è tecnico:** Obsidian sul PC, con il plugin Obsidian Git che fa commit e sync a intervalli [verificato: github.com/Vinzent03/obsidian-git, 10/11/2026].
- **Sincronizzazione scelta.** Git. Tra le strade in casa è l'unica che conserva autore e storia di ogni modifica. LiveSync salva i dati in CouchDB e non nei file del server, quindi gli agenti non li vedrebbero come file [verificato: github.com/vrtmrz/obsidian-livesync, 10/11/2026]. Un ponte da CouchDB ai file non l'ho verificato [non verificato]. Sul telefono git è debole: l'autore del plugin lo dice «highly unstable» [verificato: stessa pagina di Obsidian Git]. Per questo dal telefono si scrive tramite agente.
- **Ingresso in Qdrant.** Un hook `post-receive` del repository chiama `POST /eventi` con l'elenco dei file cambiati. La pipeline prende `acl` e `colore` dall'intestazione YAML [proposta].

### C. Misto: cartella Markdown per gli agenti, BookStack per il resto [proposta]

La cartella di B per i testi che gli agenti leggono e scrivono ogni giorno: «Come lavoro», processi, skill, manuale. BookStack per catalogo, «perché» degli obiettivi e testi lunghi delle persone. Variante: SharePoint al posto di BookStack per il resto. È già in M365 e toglie MariaDB, ma gli agenti lo leggerebbero via Graph attraverso un MCP [non verificato: non progettato].

### D. Cartella sul server più Obsidian Sync, come eccezione cloud [proposta]

Suggerita dai fatti: è l'unico modo per avere l'app Obsidian condivisa su PC e telefono (anche iOS) con storia e autore.
- Sul server, il client `ob` di Obsidian Headless tiene allineata la cartella con il vault condiviso. Gli agenti scrivono i file.
- Le persone usano l'app con un vault condiviso, cifrato end-to-end, regione Francoforte [verificato: obsidian.md/help/sync/headless, sync/collaborate e sync/security, 10/11/2026].
- Sulla cartella del server si possono tenere commit git locali per la storia con agente e carta. Che questo non crei una «doppia sincronizzazione» va provato [non verificato].
- Richiede un'eccezione al board, perché Obsidian Sync non è tra i cloud elencati [verificato: docs/03-architettura.md, riga 130].

---

## 4. Requisito per requisito

Legenda: ✔ soddisfa · ◐ in parte o con lavoro nostro · ✘ non soddisfa.

| R | A. BookStack | B. Markdown in git | C. Misto | D. Cartella + Obsidian Sync |
|---|---|---|---|---|
| R-01 contenuti | ✔ pagine, libri, tag. Registro e skill solo come copia | ✔ tutto, compresi registro, skill e configurazioni già in git | ◐ divisi in due posti | ✔ come B |
| R-02 chi scrive | ✔ ruoli per libro; `changelog` da API dalla v26.09 | ◐ chi scrive lo decide il motore (carta, commit); nessun blocco lato file | ◐ come B per la cartella, come A per il resto | ✘ nel vault condiviso tutti hanno i diritti del proprietario |
| R-03 chi legge | ✔ web e MCP | ✔ motore, MCP «testi», sito | ✔ | ✔ app e file |
| R-04 lettura per ID e campi a macchina | ◐ ID di pagina sì; i campi fissi possono stare nei tag nome-valore della pagina (revisione), senza schema controllato da BookStack (rev. 2), altrimenti vanno copiati in PostgreSQL come in ricerca/29 riga 169 | ✔ `id` e campi nell'YAML, letti dal codice senza copie | ✔ per le regole | ✔ come B |
| R-05 agenti senza internet | ✔ MCP in VLAN 30 | ✔ file locali | ✔ | ◐ gli agenti sì; il client `ob` deve uscire verso il cloud di Obsidian |
| R-06 scrittura degli agenti | ✔ libro proposte; ◐ MCP di comunità con 50 stelle, o nostro da 1,5-2 gp | ✔ scrittura di file più commit, senza API in mezzo | ✔ | ✔ come B |
| R-07 permessi | ✔ per ruolo, con override fino alla pagina | ◐ per cartella, solo nel nostro MCP e nel sito (il sito statico è unico: servono regole per percorso nel proxy); chi ha accesso SSH al repository, o una copia in Obsidian, vede tutto, storia compresa | ◐ | ✘ nessun permesso per persona o cartella |
| R-08 PC e telefono | ✔ web; ◐ telefono mai provato | ◐ PC sì; telefono solo in lettura dal sito o scrittura tramite agente in Teams | ◐ due strumenti diversi | ✔ app su PC, iOS e Android; ◐ sync in background sul telefono ancora «Active» in roadmap |
| R-09 Entra | ✔ OIDC e SAML, gruppi legati ai ruoli | ◐ Entra solo davanti al sito (proxy); le modifiche hanno il nome dato dal motore | ◐ | ✘ nessun SSO documentato |
| R-10 storia e correzione | ✔ revisioni, registro di audit, cestino per le persone; ✘ per gli agenti: l'API non legge né ripristina le revisioni (rev. 2) | ✔ storia completa con `git revert`; ✘ cancellare dati da git richiede di riscrivere la storia | ◐ | ◐ storia 1 o 12 mesi, autore dell'ultima modifica; allegati 2 settimane |
| R-11 ingresso in Qdrant | ✔ webhook più API | ✔ hook git verso `POST /eventi`; `acl` e `colore` dall'YAML | ◐ due ingressi | ◐ file watcher o commit locali; da provare |
| R-12 server | ◐ BookStack più MariaDB, un database in più | ✔ un repository git più un sito statico, nessun database | ✘ tutte e due le cose | ✔ un client e una cartella |
| R-13 self-hosted e licenza | ✔ MIT, già nel board | ✔ file nostri; Obsidian gratuito anche per uso commerciale, facoltativo | ✔ | ✘ Sync è cloud, fuori dal board; ◐ beta |
| R-14 una cosa, un posto | ◐ copie dei testi che nascono in git | ✔ | ✘ due case per i testi | ✔ |
| R-15 tempi | ◐ fase 2 | ✔ già dalla milestone 1 | ◐ | ◐ dopo l'eccezione |

---

## 4-bis. Casi che la prima stesura non considerava (revisione)

1. **Due agenti cambiano lo stesso file.**
   - B: in git vince chi fa il commit per primo; il secondo commit fallisce o crea un conflitto. Serve un solo scrittore (il motore) con una coda e un controllo di versione: la carta registra l'hash del file letto, e il commit si rifiuta se il file è cambiato nel frattempo [proposta].
   - A: la documentazione dell'API non prevede alcun controllo di versione sulle modifiche [verificato: demo.bookstackapp.com/api/docs, 10/11/2026], quindi l'ultima scrittura vince [deduzione]. Il motore può rileggere `revision_count` prima di scrivere, ma lettura e scrittura sono due chiamate separate: una modifica fatta nel browser fra le due va persa [deduzione].
   - Correzione della seconda revisione: il lavoro **non** è uguale. In git il rifiuto è garantito dallo strumento (un push che non parte dall'ultima versione viene rifiutato) [non verificato: comportamento standard di git, da provare con la prova 2 del §9]. In BookStack il controllo è solo nostro e lascia una finestra scoperta. Con un solo scrittore (il motore) il problema resta solo per le modifiche fatte a mano nel browser.
2. **Una persona modifica dal telefono mentre un agente scrive.**
   - A: la persona scrive nel browser, l'agente scrive via API dopo la carta. Rischio di sovrascrittura come al punto 1.
   - B: dal telefono si scrive solo tramite agente, quindi la modifica passa dalla stessa coda del motore e il conflitto non nasce. Chi usa Obsidian sul PC invece può andare in conflitto al pull.
   - D: se due persone modificano lo stesso file, Sync fonde le modifiche durante la sincronizzazione; non c'è modifica in tempo reale [verificato: obsidian.md/help/sync/collaborate, 10/11/2026]. La fusione è automatica: nessuno conferma il risultato, e una regola può uscire mescolata senza che la carta lo sappia [deduzione].
3. **Dati delicati copiati sui dispositivi.**
   - B con Obsidian: ogni PC tiene una copia intera del repository, con tutta la storia e tutte le cartelle. I permessi per cartella lì non valgono. Se un PC si perde, va cancellata la copia e, per i dati da togliere, riscritta la storia [deduzione].
   - D: ogni PC e telefono tiene il vault intero; il vault locale non è cifrato [verificato: obsidian.md/help/sync/security, 10/11/2026].
   - A: sui dispositivi non resta nulla, salvo la cache del browser.
   - Per questo nella revisione la sicurezza di B scende a 4 e quella di D a 3 (§5).
4. **Chi non ha Obsidian installato.** In B legge il sito e cambia le pagine solo chiedendo a un agente in Teams. Va bene per tre righe di «Come lavoro». Non va bene per testi lunghi come processi e catalogo, che Michele scrive e corregge [deduzione]. Per loro serve comunque un editor: Obsidian con git, oppure un editor web da aggiungere.
5. **L'ingresso nella porta di ricerca (MCP RAG).**
   - B: l'hook `post-receive` deve gestire anche file cancellati, rinominati e cambi di `acl`, che obbligano a rifare i permessi dei pezzi già in Qdrant. Il diritto alla cancellazione tocca tre posti: storia git, copie sui PC, Qdrant [proposta].
   - A: lo stesso lavoro con i webhook di BookStack (`page_update`, `page_delete`, permessi) [non verificato: elenco esatto degli eventi da rileggere].
   - Il lavoro è simile; in B pesa di più la cancellazione.

---

## 5. Voti

Pesi del terzo giro: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10. Il totale è la somma di voto × peso, diviso 10.

La prima revisione ha cambiato otto voti (uno di A, quattro di B, tre di D). Ogni cambio è segnato «(rev.)» con il voto della prima stesura fra parentesi. La seconda revisione ha cambiato un voto, segnato «(rev. 2)».

### A. BookStack — 63,5 (prima stesura 63,5; prima revisione 67,0)

| Criterio | Peso | Voto | Motivo |
|---|---|---|---|
| Autonomia | 35 | 6 (rev. 2: la prima revisione l'aveva alzato a 7) | Gli agenti passano da un'API e da un MCP da scegliere o scrivere. È vero che anche in B leggono attraverso il motore e che le pagine ufficiali aspettano la carta. Ma con BookStack gli agenti non possono leggere le versioni vecchie né tornare a una revisione: correggere da soli richiede che il motore salvi il testo vecchio. Le scritture non hanno controllo di versione e i tag non hanno schema (§3 A, §4-bis caso 1). In più skill e registro nascono in git. Due punti sotto B. |
| Tempo al valore | 20 | 5 | Arriva in fase 2, con circa 2 gp più 0,5-2 gp di MCP (ricerca/36 righe 546 e 928). |
| Costi | 15 | 7 | Licenza a 0 €, ma lavoro di posa più un database in più da tenere. |
| Sicurezza essenziale | 10 | 9 | Ruoli per libro, Entra, MFA, revisioni, registro di audit e cestino già pronti. |
| Server e manutenzione | 10 | 6 | Due servizi nuovi (BookStack e MariaDB) nei backup, nel monitoraggio e nelle patch. |
| Rischio | 10 | 7 | Prodotto maturo e nel board; restano i doppioni con git e il telefono mai provato. |

### B. Markdown in git, fonte unica — 66,5 (prima 76,0)

| Criterio | Peso | Voto | Motivo |
|---|---|---|---|
| Autonomia | 35 | 8 (rev., era 9) | Campi in YAML letti dal codice senza copie; skill, registro e testi in un solo posto; ogni modifica è un commit con agente e carta. Però gli agenti leggono e scrivono attraverso il motore o un MCP «testi» ancora da scrivere, e le modifiche ufficiali aspettano la carta come in A. |
| Tempo al valore | 20 | 6 (rev., era 7) | Le regole sono file già nella milestone 1, ma solo per il motore e con dati verdi. Per le persone il valore arriva solo con il sito con login e permessi per gruppo e con il flusso Teams, tutto da costruire e non stimato. |
| Costi | 15 | 7 (rev., era 9) | Nessuna licenza e nessun database. Ma sito, proxy con regole per percorso, MCP «testi», flusso Teams, controllo di versione nel motore e hook di indicizzazione sono codice nostro, non stimato: non si può dare un voto più alto di A, che ha una stima di circa 2-4 gp. |
| Sicurezza essenziale | 10 | 4 (rev., era 5) | Permessi solo per cartella e solo nel nostro codice; Entra solo davanti al sito; chi usa Obsidian ha sul PC tutto il repository con la storia (§4-bis, caso 3); la cancellazione in git è scomoda. |
| Server e manutenzione | 10 | 7 | Un repository nudo e un sito statico; niente database, ma un proxy con login da tenere. |
| Rischio | 10 | 5 | Il «passo indietro» per i CEO resta possibile; la mitigazione (scrittura via agente) va provata. |

### C. Misto — 66,0

| Criterio | Peso | Voto | Motivo |
|---|---|---|---|
| Autonomia | 35 | 8 | I testi degli agenti sono file; per il resto serve ancora l'MCP di BookStack. |
| Tempo al valore | 20 | 6 | Si costruiscono tutte e due le strade. |
| Costi | 15 | 6 | Si paga il lavoro di entrambe. |
| Sicurezza essenziale | 10 | 7 | BookStack copre bene la sua parte, la cartella resta debole come in B. |
| Server e manutenzione | 10 | 5 | Repository, sito, BookStack e MariaDB insieme. |
| Rischio | 10 | 5 | Le persone devono sapere dove sta cosa; si rompe «una cosa, un posto». |

### D. Cartella più Obsidian Sync — 61,0 (prima 69,5)

| Criterio | Peso | Voto | Motivo |
|---|---|---|---|
| Autonomia | 35 | 7 (rev., era 8) | Gli agenti scrivono file come in B, ma attraverso un client in beta che va tenuto allineato; la storia condivisa mostra solo chi ha modificato per ultimo; Sync fonde da solo due scritture vicine, senza conferma (§4-bis caso 2). |
| Tempo al valore | 20 | 6 (rev., era 8) | L'app è pronta su PC e telefono, ma prima serve l'eccezione al board, e Headless è in beta. |
| Costi | 15 | 7 | 192 USD all'anno per quattro persone con Sync a 4 USD al mese con pagamento annuale, più l'eventuale utenza per il server [calcolo su obsidian.md/pricing, riletto il 10/11/2026; quinta utenza non verificata]. |
| Sicurezza essenziale | 10 | 3 (rev., era 4) | Nessun permesso, nessuna sola lettura, nessun SSO; dati cifrati ma su cloud di terzi; il vault intero, non cifrato, sta su ogni PC e telefono. |
| Server e manutenzione | 10 | 8 | Solo un client e una cartella sul server. |
| Rischio | 10 | 3 | Fuori dal board; Headless in beta; prodotto che cambia in fretta (1.15.1 ha cambiato i vault condivisi). |

### Riepilogo

| Opzione | Totale su 100 |
|---|---|
| B. Markdown in git, fonte unica | 66,5 (prima 76,0) |
| C. Misto | 66,0 (invariato) |
| A. BookStack | 63,5 (prima revisione 67,0) |
| D. Cartella più Obsidian Sync | 61,0 (prima 69,5) |

I voti sono un giudizio sui fatti raccolti [proposta]. Calcolo: A = (6×35 + 5×20 + 7×15 + 9×10 + 6×10 + 7×10) / 10 = 63,5; B = (8×35 + 6×20 + 7×15 + 4×10 + 7×10 + 5×10) / 10 = 66,5; C = (8×35 + 6×20 + 6×15 + 7×10 + 5×10 + 5×10) / 10 = 66,0; D = (7×35 + 6×20 + 7×15 + 3×10 + 8×10 + 3×10) / 10 = 61,0 [calcolo]. B, C e A stanno in 3 punti. Il voto di costo di B (7) è dato su lavoro non stimato: se la stima uscisse alta e il voto scendesse a 5, B andrebbe a 63,5, pari con A. Per questo la scelta non si fa sui totali ma sulle prove del §9 e sulla stima del lavoro di B. Sulla sicurezza A vince netto (9 contro 4); sull'autonomia B vince di due punti.

---

## 6. Rischi

### A. BookStack
- **Doppioni.** Registro, skill e configurazioni nascono in git; BookStack ne terrebbe copie che possono divergere (R-14).
- **Campi a macchina.** L'orario per la finestra L2 può stare nei tag della pagina, ma i tag sono testo libero senza schema: una modifica nel browser può romperli, e il motore li deve controllare a ogni lettura. Altrimenti va copiato in PostgreSQL, quindi una seconda fonte [deduzione; aggiornato nella seconda revisione].
- **Correzione solo a mano.** L'API non legge né ripristina le revisioni [verificato: demo.bookstackapp.com/api/docs, 10/11/2026]. L'«annulla» di un agente funziona solo se il motore ha salvato il testo vecchio prima di scrivere [proposta].
- **MCP di comunità** con 50 stelle e nessuna data di rilascio visibile; altrimenti va scritto da noi [verificato: ricerca/29 §3.1].
- **Telefono** mai provato [non verificato].
- **Cancellazione su richiesta**: le revisioni conservano i testi vecchi; come cancellarle non è verificato [non verificato].

### B. Markdown in git
- **I due CEO.** Il giudice CEO ha già bocciato un «vault Markdown in git» come «passo indietro» [verificato: ricerca/21-giudizio-ceo riga 44]. La differenza qui è che i CEO non vedono git: scrivono in Teams e leggono un sito. Se la prova va male, B cade.
- **Permessi deboli.** I permessi esistono solo nel nostro MCP e nel sito. Chiunque abbia l'accesso SSH al repository vede tutto. Si mitiga con l'accesso al repository solo al motore e agli amministratori, e con un repository separato per i testi che non tutti devono vedere [proposta].
- **Cancellazione in git.** Togliere un dato personale dalla storia vuol dire riscriverla (per esempio con `git filter-repo`) e rifare le copie [non verificato: procedura da provare]. Si mitiga così: nei file solo dati gialli e verdi, mai rossi.
- **Conflitti** se una persona modifica con Obsidian mentre il motore fa un commit. Il plugin Obsidian Git risolve i conflitti nell'editor [verificato: github.com/Vinzent03/obsidian-git, 10/11/2026], ma resta lavoro per chi usa Obsidian.
- **Plugin della comunità** (Obsidian Git) con pieno accesso al PC [verificato: obsidian.md/help/plugin-security, 10/11/2026]. Si mitiga così: Obsidian è facoltativo e ha pochi plugin, scelti da Michele.
- **Link che cambiano** quando una nota cambia nome: non so se Obsidian li aggiorna [non verificato]. Il motore legge per `id`, non per nome del file, quindi il rischio per gli agenti è basso [proposta].

### C. Misto
- Due case per i testi: chi cerca qualcosa deve sapere dove guardare.
- Tutto il lavoro e la manutenzione di A più quelli di B.
- Le skill e i processi restano comunque nella cartella, quindi BookStack serve a poco.

### D. Cartella più Obsidian Sync
- **Board.** Serve un'eccezione di Michele per un cloud non elencato.
- **Nessun permesso.** Tutti gli utenti del vault condiviso hanno gli stessi diritti del proprietario [verificato: obsidian.md/help/sync/collaborate, 10/11/2026]. Un errore cancella o cambia le regole di altri; si recupera dalla storia.
- **Beta.** Obsidian Headless è in beta aperta; su Linux non conserva la data di creazione dei file [verificato: obsidian.md/help/sync/headless, 10/11/2026].
- **Dipendenza dal fornitore** per Sync e Headless. I file restano portabili.
- **Rivendita.** Ogni cliente dovrebbe avere i suoi abbonamenti Sync (K13) [deduzione].

---

## 7. Raccomandazione

**Raccomandazione dopo la seconda revisione [proposta]:**
1. **Obsidian non diventa la casa dei testi.** D (Obsidian Sync) chiede un'eccezione al board e non ha permessi né SSO. Resta solo, eventualmente, un editor facoltativo sul PC sopra la cartella di B.
2. **Oggi non si sceglie fra A e B.** B è avanti di 3 punti (66,5 contro 63,5) per l'autonomia: file con schema, storia leggibile e annullabile dagli agenti, rifiuto delle scritture vecchie garantito da git. A vince netto sulla sicurezza (9 contro 4), è pronto e ha una stima di lavoro. La differenza sta dentro l'incertezza, perché il lavoro di B non è stimato. La prima revisione dava A avanti perché credeva gli agenti capaci di correggere da soli anche in BookStack: non è così (§3 A).
3. **Scegliere ora non serve.** La milestone 1 non ha casa dei testi né con A né con B (ricerca/45 §3.2); BookStack arriva in fase 2. L'ADR-0005 resta in vigore finché non si decide. Niente ADR-0027 per ora.
4. **Si decide prima della fase 2**, con le prove del §9 fatte nella milestone 2. Si sceglie B se: la prova con i CEO va bene senza wiki; la stima di sito con permessi per gruppo, MCP «testi», flusso Teams e hook resta nell'ordine di BookStack più MCP (circa 2-4 gp); il modo di togliere un dato da git e dalle copie sui PC è provato. Se una delle tre cade, resta A.
5. **Valgono in tutti e due i casi:**
   - i campi fissi di «Come lavoro» letti dal codice senza copia in PostgreSQL (YAML in B, tag della pagina in A), con lo schema controllato dal motore;
   - la modifica chiesta a un agente in Teams, con carta (commit in B, `changelog` in A), per chi non vuole aprire un editor;
   - un solo scrittore per i testi ufficiali (il motore), che salva il testo letto prima di scrivere e rifiuta se è cambiato (§4-bis).
6. **La milestone 1 non cambia:** le regole restano a schema nel codice, come oggi. Nella spec si annota che lo schema va scritto in modo da diventare sia l'intestazione YAML di B sia i tag di A.

### Se B vince le prove: cosa cambierebbe nell'ADR-0005

Questa parte è il piano della prima stesura. Le revisioni lo tengono come piano per il caso in cui B passi le prove, non come decisione.
- Nella tabella «Decisione», la riga «BookStack» diventa «Cartella dei testi in git sul server (`testi.git`)», con lo stesso contenuto più registro degli agenti, skill e manuale.
- Il registro degli agenti sta nei file (oggi l'ADR-0005 dice PostgreSQL). Si chiude così l'incoerenza con docs/03 §3.1.
- Fra le «Negative» esce «MariaDB entra nel board».
- Entra un nuovo rischio: «permessi solo nel codice» e «cancellazione in git».
- Fra le «Alternative considerate» entrano BookStack (con il motivo dell'uscita) e Obsidian Sync (fuori dal board).
- Serve un nuovo ADR, il 0027 «Casa dei testi in Markdown e git», che sostituisce in parte l'ADR-0005. Non l'ho scritto: va deciso prima.

### Se B vince le prove: cosa cambierebbe nella milestone 1
- Le regole «Come lavoro», oggi istruzioni a schema nel codice, passano in `testi/come-lavoro/<id>.md`. L'intestazione YAML viene controllata dallo stesso schema che il motore usa già.
- Il motore le legge per `id` all'inizio di ogni catena N e sessione S. Funziona su Windows con Node 22, senza Docker, con soli dati verdi.
- Le altre parti della milestone 1 restano uguali.
- Si chiude l'incoerenza «settimane 1-2»: le regole si scrivono subito, nei file.

### Milestone 2 (prove con Teams e LiteLLM), in tutti e due i casi
- In più, una prova: «cambia la mia pagina Come lavoro» da Teams. L'agente propone la modifica, la persona conferma con la carta, il motore la applica (commit in B, API con `changelog` in A).
- È la prova decisiva per i CEO (§9, prova 1). Non aggiunge servizi.

### Se B vince le prove: fasi successive
- **Fase 2:** il sito di sola lettura con login Entra e l'MCP «testi» per le sessioni S, al posto di BookStack e del suo MCP.
- **Fase 3:** l'hook git verso `POST /eventi` per l'indicizzazione in Qdrant.
- **Fase 4:** processi e proposte di skill come PR nel repository, approvate con la carta. È già quello che dice docs/03 §3.1 per le skill.

---

## 8. Costi

| Voce | A. BookStack | B. Markdown in git | C. Misto | D. Obsidian Sync |
|---|---|---|---|---|
| Licenze | 0 € (MIT) | 0 €; licenza commerciale di Obsidian facoltativa, 50 USD per utente all'anno | 0 € | Sync 4 USD per utente al mese con pagamento annuale: 192 USD all'anno per quattro [calcolo]; utenza del server non verificata |
| Lavoro di posa | circa 2 gp BookStack con MariaDB, più 0,5-2 gp di MCP [verificato: ricerca/36 righe 546 e 928; ricerca/29 §3.3] | non stimato: repository, MCP «testi», sito con login, flusso Teams | somma di A e B | non stimato: client `ob`, vault condiviso |
| Servizi in più sul server | BookStack, MariaDB (circa 1 GB di RAM per MariaDB) | repository nudo, sito statico, proxy con login | tutti | client `ob` |

Non do giorni per B, C e D: non ci sono stime nella repo e non le invento. Vanno fatte nella revisione della spec, dopo le prove.

---

## 9. Cosa provare prima di decidere

1. **Prova con i CEO (decisiva).** Ognuno dei due CEO cambia tre cose della sua pagina «Come lavoro» chiedendolo all'agente in Teams. Poi le rilegge sul sito, dal telefono, via NetBird. Criterio: ce la fa da solo e non chiede di tornare a un wiki. Se fallisce: opzione A.
2. **Il motore legge e scrive.** Lettura per `id`, controllo dello schema YAML, commit con `Agente:` e `Carta:`, `git revert` di una modifica. Sulle macchine di sviluppo, nella milestone 1.
3. **Obsidian con git sul PC.** Obsidian Git contro il repository nudo via NetBird, con un commit del motore nello stesso momento. Si guarda come vengono risolti i conflitti.
4. **Sito con login.** Quartz in Docker dietro un proxy con login Entra; si prova da telefono.
5. **Cancellazione.** Si toglie una riga da tutta la storia di una copia del repository e si misura quanto costa.
6. **Per un confronto onesto con A.** BookStack dal telefono; un «annulla» fatto dal motore rimettendo il testo salvato nella carta, visto che l'API non ripristina le revisioni; una modifica nel browser fatta mentre il motore scrive, per misurare la finestra scoperta.
7. **Solo se si considera D.** Il client `ob` su Linux; se serve una quinta utenza per il server; commit git locali insieme a Sync senza corruzione.

---

## 10. Fonti

**Web, lette il 10/11/2026 dal rapporto di raccolta di questo giro:**
- https://obsidian.md/license · https://obsidian.md/pricing · https://obsidian.md/changelog/
- https://obsidian.md/help/data-storage · /help/properties · /help/attachments · /help/bases · /help/cli · /help/uri
- https://obsidian.md/help/sync/plans · /help/sync/collaborate · /help/sync/security · /help/sync/headless · /help/sync/version-history · /help/teams/sync · /help/sync-notes
- https://obsidian.md/help/publish/security · https://obsidian.md/help/plugin-security · https://obsidian.md/roadmap/ · https://obsidian.md/download
- https://github.com/vrtmrz/obsidian-livesync · https://github.com/Vinzent03/obsidian-git · https://github.com/coddingtonbear/obsidian-local-rest-api · https://github.com/cyanheads/obsidian-mcp-server
- https://forum.obsidian.md/t/running-obsidian-headlessly-on-ubuntu-for-ai-agent-workflows-xvfb-systemd-setup/112741
- https://quartz.jzhao.xyz/
- https://www.stitchflow.com/scim/obsidian (fonte di terzi, in parte incoerente)

**File della repo:**
- [ADR-0005](../docs/adr/0005-memoria-postgres-qdrant-bookstack.md), [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md), [ADR-0023](../docs/adr/0023-protezioni-essenziali.md)
- [ricerca/12](12-altre-piattaforme.md) righe 174 e 186; [ricerca/20-proposta-E](20-proposta-E-claude-native.md) righe 31 e 54; [ricerca/21-giudizio-ceo](21-giudizio-ceo.md) riga 44
- [ricerca/29](29-conoscenza-task-e-documenti.md) §2, §3, §6, §8.6, §10, §11; [ricerca/36](36-architettura-v2.md) §5.5, §7.3, righe 546, 552 e 928
- [ricerca/38](38-autonomia-nella-trascrizione.md); [ricerca/39](39-autonomia-del-disegno-v2.md) riga 108; [ricerca/42-A](42-proposta-A-motore-a-livelli.md) righe 540 e 556; [ricerca/43-giudizio-ceo](43-giudizio-ceo.md) riga 92
- [ricerca/45](45-architettura-v3.md) §2.2, §2.3, §2.5, §2.6, §3.2, §4.2, §6, §10, §12.2
- [docs/03-architettura.md](../docs/03-architettura.md) §1.3, §2.1, §2.2, §3.1, §3.3, §4.3, §5.1, §5.3, §5.4, riga 130
- [PRESENTAZIONE-CEO.md](../PRESENTAZIONE-CEO.md) righe 529, 747, 751, 763, 768, 775
- Spec del nucleo, rev. 2: `sersan-agent-os-codice/docs/superpowers/specs/2026-11-09-nucleo-motore-cancello-design.md` §4.1
