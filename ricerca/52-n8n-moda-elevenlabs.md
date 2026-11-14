# 52. n8n, Moda ed ElevenLabs: tre strumenti che l'azienda ha già

- **Data**: 14 novembre 2026. Le pagine ufficiali citate sono state lette il 14 novembre 2026, salvo dove è scritta un'altra data. Quattro lettori hanno raccolto i fatti; le versioni e gli avvisi di sicurezza di n8n, che servono per l'installazione del 15 novembre, li ho ricontrollati sulle fonti lo stesso giorno.
- **Per chi**: Alberto, che ha dato la direttiva; Michele, che il 15 novembre installa n8n e a cui restano infrastruttura e fornitori; chi scriverà gli spec delle milestone con gli agenti dello Studio contenuti.
- **La direttiva di Alberto del 14 novembre 2026**, parola per parola: «non so se era gia contato all'inizio del brainstorming per sviluppare il primo piano o mi ero dimenticato, ma abbiamo anche N8N Comunity Edition (magari per le automazioni) ,Moda app e Eleven Labs (magari da collegare con gli agenti di makreting per il piano)  . é una variabile da tener conto come le altre . non agire come se fosse obbligatoria , ma giudicala come abbiamo fatto con tutto il resto delle nostre ricerche e alternative.»
- **Le precisazioni di Alberto dello stesso giorno**, parola per parola:
  1. «per ora n8n è inutilizzato , abbiamo l'abbonamento che non abbiamo ancora utilizzato. Moda app e ElevenLabs pure . quindi sono gratis nel senso che non ci sono costi per noi . Ce li hanno dati in regalo all'azienda.»
  2. «per n8n è installata da noi , la installa domani Michele.»
- **Domande a cui risponde**:
  1. I tre strumenti erano già stati contati nel progetto, e con quale esito?
  2. Che cosa sono oggi, con quali piani e quali prezzi di listino?
  3. Che cosa farebbero nel progetto, per quali agenti, e che cosa chiedono al disegno?
  4. Come stanno contro le alternative, con i sei criteri pesati del progetto?
  5. Che cosa succede al progetto se l'omaggio finisce?
  6. Che cosa conviene sapere il giorno in cui Michele installa n8n?
- **Cosa aggiorna**: [ADR-0011](../docs/adr/0011-n8n-orari-integrazioni.md) e [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md) su n8n; [ADR-0008](../docs/adr/0008-andrea-centralino.md) e [ricerca/31](31-voce-andrea-self-hosted.md) sulla voce di Andrea; [ADR-0002](../docs/adr/0002-self-hosted-board-michele.md) sulle eccezioni al board; [ADR-0009](../docs/adr/0009-dati-tre-colori.md) sul colore della voce; i fatti di [ricerca/41 §5](41-novita-al-9-novembre.md), di [ricerca/44](44-verifiche-avversarie.md) e di [docs/04-tech-stack.md](../docs/04-tech-stack.md) su n8n, di [ricerca/14 §2](14-costi-abbonamenti-e-api.md) e [ricerca/16 §5](16-gdpr-ai-act-e-regole.md) su ElevenLabs, di [ricerca/23](23-critica-completezza.md) su moda.app; la decisione 15 di [PRESENTAZIONE-CEO.md §14](../PRESENTAZIONE-CEO.md). Le revisioni proposte sono nel §7: nessuna ADR è stata modificata.
- **Legenda**:
  - `[verificato: fonte, data]`: letto sulla fonte indicata;
  - `[non verificato: motivo]`: stima, deduzione, o dato che la fonte primaria non conferma;
  - `[proposta]`: una scelta di disegno di questo rapporto;
  - `[calcolo]`: un conto fatto da me su dati citati.
- **Cosa non ho fatto**: niente installazioni, nessun account creato, nessun accesso a servizi, nessun acquisto, nessun connettore collegato né usato. Nella repo del codice ho solo letto; la correzione della direttiva D26 (§1.3) è entrata a parte, fatta da chi coordina.

### Parole usate spesso

- **Omaggio**: i tre strumenti che l'azienda ha ricevuto in regalo e dice di non avere ancora usato (per ElevenLabs vedi §1.4). Oggi non costano niente; durata e piano non si sanno.
- **A listino**: il prezzo pubblicato del piano, cioè quello che si pagherebbe senza l'omaggio.
- **Community Edition**: la versione gratuita di n8n da ospitare sul proprio server.
- **Flusso** (in inglese *workflow*) ed **esecuzione**: in n8n un flusso è una catena di passi, detti nodi; ogni volta che parte lascia un'esecuzione, con i dati che ha visto.
- **Webhook**: un indirizzo che un servizio chiama quando succede qualcosa.
- **Sintesi vocale** (*text to speech*): un testo che diventa voce.
- **Clonazione professionale** (*professional voice cloning*): la copia di una voce fatta da almeno 30 minuti di registrazione, con una verifica della persona.
- **Tela** (*canvas*) e **kit del marchio** (*brand kit*): in Moda, il foglio di lavoro modificabile e l'insieme di logo, colori, caratteri e immagini dell'azienda.
- **Crediti**: l'unità con cui ElevenLabs e Moda contano l'uso dentro un piano.
- **Chiave limitata**: una chiave API che vale solo per alcuni indirizzi del servizio e ha un tetto di spesa.

---

## In breve

1. **Tutti e tre erano già stati contati. Di nuovo ci sono tre cose: n8n è già disponibile, l'omaggio è confermato e ci sono due usi mai pesati.** n8n è nel board di Michele e nelle ADR 0011, 0021 e 0022: dal 10 novembre è facoltativo, perché la sveglia sta nel motore. ElevenLabs è stato valutato e scartato come voce di Andrea ([ADR-0008](../docs/adr/0008-andrea-centralino.md)); per gli agenti dello Studio non è mai stato pesato, anche se le direttive dei contenuti lo usano già. Moda (moda.app) non entra per la prima volta: il primo giro la dava «già presente» ([ricerca/18](18-agenti-in-abbonamento.md)), il secondo l'ha valutata, e la decisione 15 consiglia di sostituirla con Claude Team per le slide. Per ElevenLabs la disponibilità senza costi era già contata ([ricerca/14 §2.3](14-costi-abbonamenti-e-api.md); [ricerca/22](22-architettura-scelta.md)). È nuovo che n8n sia già disponibile, ed è nuova la conferma che l'azienda dispone dei tre strumenti senza costi, perché li ha ricevuti in omaggio, e che non li ha ancora usati. Su ElevenLabs la repo registra però due cloni della voce di un founder già fatti: l'account è già stato usato, anche se non dagli agenti (§1).
2. **n8n: entra come opzione, con condizioni.** Sta 2 punti sotto il codice del motore, 70 contro 72, dentro il margine, ma i due non si fanno concorrenza. Il motore resta la sveglia e l'unica strada verso fuori. n8n serve alle pipeline del board e alle automazioni interne che il Mappatore processi consiglia, purché chiamino `POST /eventi` con il loro token o scrivano solo su sistemi interni con credenziali ristrette. Activepieces, Windmill e Node-RED restano sotto di 13 punti o più (§3).
3. **Michele installa n8n il 15 novembre: la versione da prendere, al 14 novembre, è la 2.47.7.** È la stabile del 13 novembre e contiene le correzioni degli avvisi gravi che ho letto, fino a quelli del 13 novembre. La 2.48 e la 3.x sono ancora anteprime. Due cose contano più delle altre quel giorno. La prima: installare la sola immagine `n8nio/n8n:2.47.7` con PostgreSQL, e non il comando unico né la guida Docker Compose così come sono, perché aggiungono un contenitore privilegiato e partono con SQLite. La seconda: non impostare `NODES_EXCLUDE`, perché sulla 2.47.7 le esclusioni di serie bastano e un valore scritto male le toglie tutte senza avvisi. Poi: l'editor non va esposto su internet, e la chiave che cifra le credenziali la custodisce una persona. Il resto è nel §4.
4. **ElevenLabs per i contenuti dello Studio: entra come opzione, con condizioni.** Per voce, musica ed effetti dei contenuti pubblici prende 81 punti con l'omaggio, se l'omaggio copre l'API e un'area di lavoro a più posti [non verificato: domanda 7], altrimenti vale il totale a listino, 68; la prima alternativa, la sintesi vocale di OpenAI, ne prende 65. A listino lo scarto sta dentro il margine, e decide che nessuna alternativa dà voce, musica ed effetti insieme. Le condizioni: solo testi verdi, una chiave limitata di account di servizio tenuta dal motore, che chiede un'area di lavoro a più posti, nessuna cancellazione, ricarica automatica spenta, rinuncia all'addestramento impostata subito, uscita dal Cancello al livello del post, ogni file salvato nei nostri archivi, eccezione al board approvata con Michele. Due limiti in più. Per la musica i piani fino a Pro valgono solo per uso individuale: a un'azienda serve Scale, sotto i 10 dipendenti, o Business, sotto i 50. Per la regola dei colori la voce dei founder è un dato rosso finché il parere legale non decide. La proposta è che fino ad allora non si carichi su ElevenLabs, che gli agenti non la usino e che i due cloni già fatti restino fermi: lo decidono i founder (§5; §8, domanda 9).
5. **ElevenLabs per Andrea: non entra per ora.** La voce di chi chiama è un dato rosso e non esce dal server; gli agenti vocali di ElevenLabs la porterebbero negli USA. Resta la scelta di ADR-0008. Si precisa solo l'ultima riserva: se la voce italiana in casa non passa la prova d'ascolto, ElevenLabs può dare la sola voce di Andrea, con l'ascolto sempre in casa e un filtro locale che ferma i dati rossi nel testo delle risposte. Questa strada prende 66 punti con l'omaggio, con la stessa premessa non verificata del punto 4, contro i 68 della catena tutta in casa, dentro il margine, e 53 a listino: costa la linea e lo sviluppo come la catena in casa, chiede l'eccezione di Michele e, a listino, un piano a più posti per la chiave di account di servizio. Andrea arriva nella fase 5 (§5).
6. **Moda: entra come opzione, solo per le grafiche con dati verdi e finché dura l'omaggio.** Per caroselli, copertine e presentazioni pubbliche prende 73 punti contro i 72 della strada di Claude Team con i template SerSan: con l'omaggio è avanti di un punto, dentro il margine, e decide che Moda dà allo Studio un agente grafico con il kit del marchio, che l'altra strada non ha; a listino non conviene, e quando l'omaggio finisce lo Studio torna alla strada di Claude Team (punto 7). Le slide con dati gialli (brief, recap e proposte ai clienti) restano sulla strada della decisione 15: Moda è fuori dal board, conserva i dati negli USA e addestra i suoi modelli sui contenuti finché non si rinuncia con una mail (§6).
7. **L'omaggio conta nei costi e nel tempo, e non rende obbligatorio nessuno strumento.** Rifatti a listino, i confronti di n8n ed ElevenLabs danno lo stesso ordine: per i contenuti il vantaggio di ElevenLabs su OpenAI scende da 16 punti a 3, dentro il margine; per Andrea la catena in casa resta davanti, di 2 punti con l'omaggio e di 15 a listino. Moda invece scende da 73 a 66 e passa dietro la strada di Claude Team (72), fuori dal margine: a listino non conviene. Se l'omaggio finisce: n8n Community resta gratuito; ElevenLabs costa almeno 267,13 € al mese (Scale, il primo piano a più posti, che la chiave di account di servizio richiede; per la musica Scale vale solo sotto i 10 dipendenti, e fra 10 e 49 serve Business, 884,47 € al mese) o quanto si accorda con le vendite, oppure si passa all'alternativa; Moda a listino costerebbe 26,80 € al mese per posto, ma non conviene, e lo Studio torna alla strada di Claude Team. Ogni lavoro fatto si salva nei nostri file, così la fine dell'omaggio non fa perdere i file; se restino usabili a fini commerciali, i termini lo dicono solo per la musica di ElevenLabs, e per il resto va verificato (§3.5, §5.5, §6.5).
8. **Quattro fatti del 14 novembre 2026 correggono la repo.** La CVE-2026-21858 di n8n ora è verificata e non colpisce la 2.x. La pagina delle modifiche incompatibili della 3.0 non elenca cambi dell'API pubblica. ElevenLabs applica il suo DPA anche ai piani senza contratto su misura. Moda ha un DPA, aggiornato al 21 ottobre 2026, ma con l'addestramento acceso di serie (§1.4).
9. **Cinque ADR andrebbero riviste con una revisione datata**: 0002, 0008, 0009, 0011 e 0022. Il testo proposto è nel §7. Nella repo del codice la direttiva D26 diceva che Moda entrava nella valutazione per la prima volta: la correzione entra in D26 insieme a questo rapporto (§1.3).

---

## 1. La direttiva e la domanda: erano già stati contati?

La direttiva chiede due cose: se i tre strumenti erano già stati contati quando si è scritto il primo piano, e di giudicarli alla pari con le altre alternative, senza darli per obbligatori. Tutti e tre erano già stati contati, in modi diversi.

| Strumento | Già contato? | Dove | Che cosa si era deciso | Stato al 14 novembre |
|---|---|---|---|---|
| n8n | sì, dal 24 ottobre | [ADR-0011](../docs/adr/0011-n8n-orari-integrazioni.md), [ADR-0021](../docs/adr/0021-motore-a-due-corsie.md), [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md); ricerca/25, 42, 43, 44, 45 | prima orari e integrazioni; dal 10 novembre la sveglia nel motore e n8n facoltativo | vale ADR-0022; la domanda 33 a Michele è ancora aperta nel file, ma l'installazione del 15 novembre sembra darle risposta (§8) |
| ElevenLabs | sì, per Andrea | [ADR-0008](../docs/adr/0008-andrea-centralino.md); [ricerca/31](31-voce-andrea-self-hosted.md); [docs/02, §7.3](../docs/02-alternative.md) | scartato come voce di Andrea; una voce in cloud resta l'ultima riserva | vale ADR-0008; mai pesato per gli agenti dello Studio |
| Moda | sì, dal primo giro | [ricerca/25](25-board-michele-e-delta.md) (C35), [ricerca/33](33-costi-v2.md), [ricerca/36 §8.2](36-architettura-v2.md); decisione 15 | consiglio: sostituirla con Claude Team per le slide; eccezione solo su dati verdi | consiglio, non registrato come decisione |

### 1.1 n8n

- **Primo giro (24 ottobre)**: «n8n non si prende» ([ricerca/22](22-architettura-scelta.md)). La Community Edition era già descritta come gratuita, senza limite di esecuzioni ([ricerca/12](12-altre-piattaforme.md)).
- **Secondo giro (25 ottobre)**: il board di Michele ha n8n nella VLAN 30 APPS e lo usa per i bandi di ogni notte ([ricerca/25](25-board-michele-e-delta.md); [board di Michele](../allegati/infra/SerSan%20Infra%20Board.md)). Da lì [ADR-0011](../docs/adr/0011-n8n-orari-integrazioni.md): orari e integrazioni a n8n, con tre regole che restano. n8n non manda nulla a clienti o prospect; da internet si raggiungono solo i suoi webhook firmati; la logica del motore non dipende da lui.
- **Terzo giro (9-10 novembre)**: la proposta D metteva la logica dei flussi dentro n8n ed era prima in classifica ([ricerca/42, proposta D](42-proposta-D-automazione-prima.md)). È stata scartata per la licenza, per il versionamento in git che è una funzione Enterprise, per le esecuzioni cadute che non riprendono e per i dati rossi nella cronologia delle esecuzioni ([ADR-0021](../docs/adr/0021-motore-a-due-corsie.md); [ricerca/45 §3.2](45-architettura-v3.md)).
- **Dal 10 novembre**: la sveglia sta nel motore; n8n diventa facoltativo e, se un collegamento passa da lui, chiama `POST /eventi` e basta ([ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md)).
- **Che cosa non era scritto**: con che cosa si costruiscono le «automazioni consigliate» del Mappatore processi ([PRESENTAZIONE-CEO.md §4.8](../PRESENTAZIONE-CEO.md)). La direttiva dice «magari per le automazioni»: è questo il pezzo nuovo (§3.2).
- **Che cosa non si sapeva**: che fosse già disponibile all'azienda. L'ADR-0011 scriveva solo che n8n «arriva in casa con le fasi del board». Lo installa Michele il 15 novembre.

### 1.2 ElevenLabs

- **Primo giro**: Andrea era fatto con gli agenti vocali di ElevenLabs e un numero Twilio ([ricerca/22](22-architettura-scelta.md)), anche perché lo strumento era «già in casa» ([ricerca/20, proposta G](20-proposta-G-ibrido.md)). La disponibilità senza costi era già contata: [ricerca/14 §2.3](14-costi-abbonamenti-e-api.md) la registra, con piano, voci professionali e licenza della musica «da leggere», e [ricerca/22](22-architettura-scelta.md) ne tiene conto nei costi.
- **Secondo giro**: ElevenLabs e Twilio non sono nel board, e l'audio delle chiamate è un dato rosso ([ricerca/25](25-board-michele-e-delta.md)). [ricerca/31](31-voce-andrea-self-hosted.md) porta la voce in casa e [ADR-0008](../docs/adr/0008-andrea-centralino.md) lo decide: Asterisk, Pipecat, ascolto e voce in casa, Claude Haiku attraverso LiteLLM. Una voce in cloud resta l'ultima riserva, come eccezione.
- **Marketing**: le direttive dei contenuti del 22 ottobre usano già ElevenLabs per la voce fuori campo, clonazione della voce dei founder, effetti sonori e sottotitoli ([ricerca/05 §3.4](05-marketing-e-post.md); [DIRETTIVE_CONTENUTI.md](../allegati/marketing/DIRETTIVE_CONTENUTI.md)). Ma il disegno del progetto per l'Agente video nomina solo Higgsfield, HyperFrames e After Effects ([PRESENTAZIONE-CEO.md §4.5](../PRESENTAZIONE-CEO.md)). Per gli agenti dello Studio, quindi, ElevenLabs non è mai stato pesato.
- **Trascrizione**: [ADR-0007](../docs/adr/0007-call-e-trascrizione.md) fa la trascrizione delle call in casa; la trascrizione di ElevenLabs non è mai stata fra le alternative.

### 1.3 Moda

- **Primo giro**: moda.app compare come strumento «già presente» ([ricerca/18](18-agenti-in-abbonamento.md)), via MCP oppure con Claude Slides, per le slide automatiche (voce D4) ([ricerca/20, proposta G](20-proposta-G-ibrido.md); [ricerca/22](22-architettura-scelta.md)). Della sua offerta la repo dice che è «da verificare» ([ricerca/05 §4.5](05-marketing-e-post.md)).
- **Secondo giro**: moda.app è fuori dal board; le slide contengono dati interni e a volte dei clienti, quindi o si sostituisce o resta come eccezione solo su dati verdi ([ricerca/25](25-board-michele-e-delta.md), C35). [ricerca/23](23-critica-completezza.md) notava che riceverebbe dati gialli senza un DPA verificato. L'architettura v2 la sostituisce con Slides e Design di Claude Team e i template SerSan ([ricerca/36 §8.2](36-architettura-v2.md)).
- **Decisione 15**: il consiglio è «moda.app sostituito da Claude Team» ([PRESENTAZIONE-CEO.md §14](../PRESENTAZIONE-CEO.md)). [docs/04-tech-stack.md](../docs/04-tech-stack.md) lo scrive come già deciso; [docs/06-sviluppo.md](../docs/06-sviluppo.md) dice che la decisione la prende il gruppo con Michele, e non ne registra l'esito.
- **La frase corretta**: nella repo del codice la direttiva D26 diceva «Moda no: entra nella valutazione per la prima volta». Non era così: Moda è stata valutata nel secondo giro e ha un consiglio. La correzione entra in D26 insieme a questo rapporto.

### 1.4 Che cosa c'è di nuovo

- **L'omaggio, confermato per tutti e tre.** Per ElevenLabs la disponibilità senza costi era già contata (§1.2) e moda.app nel primo giro risultava già presente (§1.3). Di nuovo ci sono due cose: n8n è già disponibile, e l'azienda conferma di disporre dei tre strumenti senza costi, perché li ha ricevuti in omaggio, e di non averli ancora usati. Per il metodo questo conta nei costi e nel tempo al valore, non altrove (§2). La repo registra però due cloni della voce di un founder già fatti su ElevenLabs da audio compresso ([ricerca/05 §3.4](05-marketing-e-post.md)): l'account è già stato usato, anche se non dagli agenti. La rinuncia all'addestramento va quindi impostata subito, perché vale solo da quel momento (§5.1), e i due cloni rientrano nella domanda 9 [proposta].
- **Due usi mai pesati**: ElevenLabs per gli agenti dello Studio; Moda come strumento che un agente usa sul server senza una persona davanti, con una chiave API.
- **Fatti del 14 novembre 2026 che correggono la repo**:
  - la CVE-2026-21858 di n8n, che l'ADR-0011 dava «da fonti di terzi non verificate», è verificata: CVSS 10, del 7 gennaio 2026, versioni da 1.65.0 a 1.120.x; n8n scrive che la 2.x non è colpita [verificato: api.github.com/advisories?affects=n8n; blog.n8n.io/security-advisory-20260108, 14/11/2026];
  - [ricerca/44](44-verifiche-avversarie.md) dice che la 3.0 «cambia l'API», e [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md) lo ripete due volte, alle righe 14 e 35, fra i motivi contro n8n come sveglia; la stessa frase è in [docs/04-tech-stack.md](../docs/04-tech-stack.md), alle righe 192 e 340. La pagina ufficiale delle modifiche incompatibili della 3.0 non elenca cambi dell'API pubblica: cambiano l'installazione (solo Docker), alcuni nodi tolti e alcune impostazioni di sicurezza [verificato: docs.n8n.io/changelog/v30-breaking-changes.md, 14/11/2026];
  - [ricerca/16 §5](16-gdpr-ai-act-e-regole.md) dà il DPA di ElevenLabs «su richiesta (Enterprise)». Oggi i termini dicono che, per chi accetta per conto di un'azienda, il trattamento è regolato dal DPA anche sui piani senza contratto su misura [verificato: elevenlabs.io/terms-of-use; elevenlabs.io/dpa, 14/11/2026];
  - [ricerca/23](23-critica-completezza.md) dice che moda.app non ha un DPA verificato. Oggi il DPA c'è, fa parte dei termini ed è aggiornato al 21 ottobre 2026; ma l'addestramento sui contenuti è acceso finché il cliente non rinuncia [verificato: moda.app/dpa; moda.app/terms, 14/11/2026].
- **Prezzi**: quelli di Moda sono uguali al 24 ottobre ([ricerca/14 §6](14-costi-abbonamenti-e-api.md)). Quelli di ElevenLabs Pro (99 $ al mese) sono confermati, e i 1.238 minuti degli agenti, che ricerca/14 deduceva dall'ordine di una tabella, ora sono scritti sulla pagina dei prezzi degli agenti [verificato: elevenlabs.io/pricing/agents, 14/11/2026].

---

## 2. Come si giudica

- **Pesi**, gli stessi di [ricerca/45](45-architettura-v3.md) (riga 34, «Pesi del giudizio, fissati prima»): autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10. Li ho controllati nella repo e coincidono con quelli della direttiva sul metodo.
- **Voti da 0 a 10** per criterio, come nei quattro giudizi di [ricerca/43](43-giudizio-ceo.md) e in [ricerca/46 §5](46-obsidian-come-casa-dei-testi.md). Il totale è la somma di voto × peso, divisa per 10, quindi su 100.
- **Margine**: uno scarto fino a 3 punti sta dentro il margine di giudizio, come in ricerca/46, dove B è avanti di 3 punti ma «la differenza sta dentro l'incertezza dei voti». Dentro il margine si sceglie sulle condizioni e sui fatti, non sui totali, come in ricerca/45 e ricerca/46 [proposta].
- **L'omaggio** entra solo nei voti di costi e tempo al valore. Server e rischio si votano come se nessuno strumento fosse già installato o già in omaggio. Ogni confronto è rifatto anche a listino: se l'ordine cambia, lo scrivo.
- **Limiti fissi**: un'alternativa che viola un limite fisso del sistema è esclusa qualunque sia il totale. I limiti sono: agli agenti mai cancellazioni né credenziali; pagamenti mai automatici; stop di emergenza sempre; i dati rossi non escono dal server; ogni azione verso fuori passa dal Cancello al suo livello ([ricerca/45 §2.5](45-architettura-v3.md); [ADR-0009](../docs/adr/0009-dati-tre-colori.md); [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md)).
- **Abbonamenti**: se un pezzo non sta sul server, un abbonamento è ammesso con il suo costo ([ADR-0024](../docs/adr/0024-abbonamenti-come-riserva.md)). Uno strumento fuori dal board è un'eccezione, approvata una per una dal gruppo di progetto con Michele ([ADR-0002](../docs/adr/0002-self-hosted-board-michele.md)). Nel tempo al valore questo passaggio conta per ogni strumento fuori dal board, in omaggio o no [proposta].
- I voti sono un giudizio sui fatti raccolti [proposta].

---

## 3. n8n Community Edition

### 3.1 Che cos'è oggi

**Il prodotto.**
- n8n è un servizio di automazioni a flussi: editor visuale, orari, webhook, nodi per le applicazioni e nodi per agenti AI. Il catalogo dichiara «2,000+ integrations» [verificato: n8n.io/integrations, 14/11/2026].
- La Community Edition ha «almost the complete feature set of n8n» [verificato: docs.n8n.io/deploy/host-n8n/community-edition-features.md, 14/11/2026]. Le mancano:
  - variabili personalizzate, ambienti, segreti esterni, archivio esterno dei file;
  - flusso dei registri verso servizi esterni (i registri locali ci sono);
  - più istanze principali insieme (la modalità a code c'è);
  - progetti, accesso unico SSO (SAML e LDAP), condivisione di flussi e credenziali, controllo di versione con Git [verificato: stessa pagina].
- Senza condivisione, flussi e credenziali li vedono solo il proprietario dell'istanza e chi li ha creati: «Only the instance owner and the user who creates them can access workflows and credentials» [verificato: stessa pagina].
- Una chiave gratuita, che si riceve registrando la Community con una mail, sblocca cartelle, la copia nell'editor dei dati di un'esecuzione (*debug in editor*) e dati personalizzati delle esecuzioni [verificato: stessa pagina].
- Sui server propri i ruoli Admin e Chat user sono solo Enterprise [verificato: docs.n8n.io/administer/manage-users-and-access/understand-instance-roles.md, 14/11/2026]; nella Community restano quindi Owner e Member. Anche i ruoli personalizzati dell'istanza sono solo Enterprise [verificato: docs.n8n.io/administer/manage-users-and-access/set-permissions-and-roles-rbac/create-custom-roles/create-custom-instance-roles.md, 14/11/2026].

**Edizioni e listino.**

| Edizione | Dove gira | Prezzo di listino | Cosa aggiunge | Fonte |
|---|---|---|---|---|
| Community | sul nostro server | 0 € | — | [verificato: docs.n8n.io/deploy/host-n8n/community-edition-features.md, «Community edition: the free edition», 14/11/2026] |
| Starter, Pro | cloud di n8n | 20 € e 50 € al mese, con pagamento annuale | 2.500 e 10.000 esecuzioni | [verificato: n8n.io/pricing, 14/11/2026] |
| Business | solo sul nostro server | 667 € al mese, con pagamento annuale | 40.000 esecuzioni, 6 progetti condivisi, SSO e LDAP, ambienti, Git | [verificato: n8n.io/pricing/?selfHosted=true, 14/11/2026] |
| Enterprise | anche sul nostro server | su richiesta | segreti esterni, flusso dei registri, registri di controllo, oscuramento dei dati delle esecuzioni | [verificato: stessa pagina] |

**Versioni.**
- La stabile è la 2.47.7 del 13 novembre 2026; lo stesso giorno sono uscite la 2.48.4 e la 3.2.2, tutte e due segnate come anteprima, e la 1.123.96 della vecchia linea [verificato: api.github.com/repos/n8n-io/n8n/releases, 14/11/2026].
- Esce una versione minore quasi ogni settimana: «n8n releases a new minor version most weeks» [verificato: docs.n8n.io/changelog, 14/11/2026]. Le correzioni escono quasi ogni giorno: 2.47.4 l'11, 2.47.5 il 12, 2.47.6 e 2.47.7 il 13 novembre [verificato: api.github.com/repos/n8n-io/n8n/releases, 14/11/2026].
- La 3.0 è in anteprima dal 27 ottobre e la stabile è annunciata per inizio dicembre: «After the stable release, 2.x gets security and critical bug fixes for 12 months». Tutta la 3.0 vale anche per la Community [verificato: blog.n8n.io/introducing-n8n-v3, 14/11/2026].
- La 3.0 si installa solo con Docker, toglie alcuni nodi vecchi (Function, Cron, Interval, Read PDF e alcuni nodi LangChain) e la versione 1 del nodo AI Agent, e accende di serie la rotazione della chiave di cifratura. «Workflows that use a removed node fail when they run» [verificato: docs.n8n.io/changelog/v30-breaking-changes.md, 14/11/2026].

**Sicurezza.**
- Nel database degli avvisi di GitHub ci sono 24 avvisi critici su n8n pubblicati fra l'8 dicembre 2025 e il 14 maggio 2026; quasi tutti permettono di eseguire codice sul server, due hanno CVSS 10 [verificato: api.github.com/advisories?affects=n8n&severity=critical, 14/11/2026; il conteggio è dei lettori].
- Gli avvisi continuano. Il 28 ottobre 2026 ne sono usciti tre alti e nove moderati; il 13 novembre due alti e tre moderati [verificato: api.github.com/repos/n8n-io/n8n/security-advisories, 14/11/2026]. Per quello del 28 ottobre sui vecchi nodi Code basta un utente che può creare o modificare flussi, e le misure provvisorie «do not fully remediate the risk» [verificato: github.com/n8n-io/n8n/security/advisories/GHSA-9p7v-45m2-wxgj, 14/11/2026].
- Un avviso alto del 25 marzo 2026 riguarda proprio la Community: furto di credenziali attraverso la risoluzione per nome (CVE-2026-33663) [verificato: api.github.com/advisories?affects=n8n&severity=high, 14/11/2026].
- Dalla 2.0 i nodi Execute Command e Local File Trigger sono spenti di serie e il nodo Code non legge le variabili d'ambiente [verificato: docs.n8n.io/changelog/v20-breaking-changes.md, 14/11/2026].
- L'oscuramento dei dati delle esecuzioni è solo Enterprise: nella Community i dati delle esecuzioni restano leggibili [verificato: docs.n8n.io/deploy/host-n8n/configure-n8n/security/redact-execution-data.md, 14/11/2026].
- Un'attesa più lunga di 65 secondi nel nodo Wait salva nel database i dati dell'esecuzione [verificato: docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait.md, 14/11/2026].
- n8n non limita i dati che un nodo legge: un flusso grande può esaurire la memoria del server [verificato: docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/fix-memory-issues.md, 14/11/2026].

**Licenza.**
- Sustainable Use License: «You may use or modify the software only for your own internal business purposes or for non-commercial or personal use» [verificato: raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md, 14/11/2026].
- Le FAQ ufficiali ammettono di costruire automazioni per i clienti sulla propria istanza e di farsi pagare creazione e manutenzione: «The key condition is that n8n remains your internal tool, where clients receive outputs, not access». Vietano di ospitare n8n come servizio in cui i clienti costruiscono flussi e di offrirlo con un altro marchio [verificato: docs.n8n.io/n8n-community-license/community-license/license-faq.md, 14/11/2026].

**Per gli agenti e i collegamenti.**
- Nodi pronti per Microsoft Teams, Outlook, HubSpot, Postgres e Google Sheets. Il nodo Teams scrive i messaggi di chat come l'utente collegato: «The node sends and reads chat messages as the signed-in user» [verificato: docs.n8n.io, pagine dei nodi, 14/11/2026].
- Il nodo LinkedIn sa solo creare un post, come persona o come organizzazione [verificato: docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.linkedin.md, 14/11/2026].
- Il nodo Webhook ammette anche nessuna autenticazione, ha l'origine CORS «*» di serie e un elenco degli IP ammessi [verificato: docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook.md, 14/11/2026].
- Lo Schedule Trigger di serie scarta gli orari persi: «Don't Run Missed Executions (default)». Il recupero dell'ultimo orario perso va scelto nodo per nodo, sui nodi aggiunti dalla 2.36 in poi, e funziona solo con il pianificatore durevole (*durable scheduler*), acceso di serie dalla 2.45.0. Il fuso orario di serie sui server propri è `America/New_York`; la pagina del nodo lo scrive con lo spazio [verificato: docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger.md; timezone-and-localization.md, 14/11/2026].
- Il server MCP dell'istanza permette a un client di cercare, avviare e, dalla 2.13.0, creare e modificare flussi; «You can't restrict specific workflows to specific clients» [verificato: docs.n8n.io/connect/connect-to-n8n-mcp-server.md, 14/11/2026].
- L'approvazione di una persona sugli strumenti dell'agente si chiede da Teams, Outlook e altri canali; la pagina non dice se registra chi ha approvato [verificato: docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md, 14/11/2026]. L'ADR-0011 riporta che il nodo Teams registra solo l'ora.
- ElevenLabs entra in n8n con un nodo della comunità fatto da ElevenLabs e verificato da n8n [verificato: n8n.io/integrations/elevenlabs, 14/11/2026].

### 3.2 Che cosa farebbe nel progetto, e per quali agenti

| Agente o squadra | Che cosa farebbe con n8n | Che cosa dice oggi il disegno | Proposta |
|---|---|---|---|
| Agente bandi e finanziamenti (Amministrazione) | la pipeline notturna del board: orario, Firecrawl, modello locale da 4B, indice, avviso | è nel board di Michele, fase F4; l'agente aggiunge requisiti e documenti ([board](../allegati/infra/SerSan%20Infra%20Board.md)) | sì: n8n esegue la pipeline e chiama `POST /eventi` con «bandi pronti»; i bandi sono pubblici, quindi verdi |
| Mappatore processi (Direzione) | costruire le automazioni interne che consiglia | le consiglia; decidere quali costruire è L0; con che cosa non è scritto ([PRESENTAZIONE-CEO.md §4.8](../PRESENTAZIONE-CEO.md)) | sì, per le automazioni interne che leggono e chiamano `POST /eventi`, o scrivono solo su sistemi interni con credenziali ristrette; le costruisce una persona, non un agente |
| Guardiano e Porta (Direzione) | avvisi a senso unico in Teams | il nodo Teams serve solo agli avvisi, mai alle approvazioni ([ADR-0011](../docs/adr/0011-n8n-orari-integrazioni.md)) | solo per gli avvisi dei flussi di n8n; gli avvisi degli agenti li manda la Porta |
| Controllo di gestione (Amministrazione) | portare i numeri di Sirius in PostgreSQL | la proposta lo faceva «via n8n» (voce K14); oggi n8n chiama `POST /eventi` e basta | solo l'avviso «esportazione pronta»: i numeri sono finanza, quindi rossi, e non passano da n8n |
| Raccoglitore (Memoria) | leggere trascrizioni e file nuovi da Graph | li legge il lettore delta nel nostro codice ([ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md)) | no: testo rosso |
| Andrea, Agente intake, Agente email | modulo del sito, webhook di Instantly | arrivano direttamente su `POST /eventi` | no: un passaggio in più, senza vantaggio |
| Pubblicatore, Analista metriche, Community manager (Marketing) | pubblicare con i nodi LinkedIn e social, leggere le metriche | pubblica il Cancello, su Postiz o con l'esecutore Metricool ([ADR-0013](../docs/adr/0013-postiz-listmonk-docuseal.md)) | no: pubblicare da n8n salterebbe il Cancello; le metriche le legge già il motore |

Tutte le proposte della colonna di destra sono [proposta].

**Cosa ne ricavo** [non verificato: lettura nostra]. Per il sistema di agenti n8n non porta nulla di indispensabile: sveglia, eventi, catene e uscite stanno nel motore. Porta però un catalogo grande e un editor che una persona usa in pochi minuti, ed è proprio ciò che serve alle automazioni interne che non sono agenti: quelle del board e quelle che il Mappatore consiglia. Il valore sta lì, e lì valgono le regole già scritte.

### 3.3 Che cosa chiede al disegno

- **Corsia**: nessuna. n8n non è una corsia del motore: è un mittente di eventi come il modulo del sito, con il suo token su `POST /eventi` ([ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md)). L'evento entra nel registro e il motore sceglie la corsia [proposta].
- **Livello nel Cancello**: n8n non ha un livello, perché non fa azioni verso fuori. Ciò che un evento di n8n fa partire esce dal Cancello al livello della sua terna. Gli avvisi interni a senso unico non sono azioni verso fuori [proposta].
- **Colore dei dati**: verde e giallo; mai rosso, perché nella Community i dati delle esecuzioni restano leggibili (criterio N10 di [ricerca/45 §6.3](45-architettura-v3.md)). Per i dati rossi n8n porta al massimo l'avviso che un dato è pronto, mai il dato. I flussi con dati gialli non salvano le esecuzioni: è una regola nuova, più severa di quella di [ricerca/42, proposta D §4.4](42-proposta-D-automazione-prima.md), che lo chiede ai flussi che leggono testo rosso [proposta].
- **Credenziali**: le tiene una persona, il proprietario dell'istanza, e restano nel database di n8n cifrate con la chiave dell'istanza (§4). Nessun agente riceve la chiave dell'API di n8n né l'accesso al server MCP dell'istanza, che può creare e modificare flussi: un agente con quell'accesso potrebbe costruire un flusso che scrive fuori senza il Cancello [proposta].
- **Registro dei collegamenti**: ogni flusso attivo ha una riga in un file in git, con responsabile, innesco, colore dei dati, credenziali e sistemi toccati. La Community non ha il versionamento in git, quindi la riga va tenuta a mano [proposta].

### 3.4 Le alternative a confronto

Il ruolo confrontato: **le automazioni interne e i collegamenti che non sono agenti**. Voti da 0 a 10; totale su 100.

| Alternativa | Autonomia (35) | Tempo al valore (20) | Costi (15) | Sicurezza essenziale (10) | Server e manutenzione (10) | Rischio (10) | Totale |
|---|---|---|---|---|---|---|---|
| **A. n8n Community in casa** | 6: i flussi partono da soli e il catalogo è grande, ma ogni scrittura fuori salterebbe il Cancello, quindi può solo portare eventi, leggere o scrivere su sistemi interni | 10: lo installa Michele il 15 novembre; editor visuale e nodi pronti | 10: 0 € di licenza, anche a listino; costa solo il server | 4: 24 avvisi critici fra dicembre 2025 e maggio 2026, altri alti fino al 13/11; nella Community mancano SSO, obbligo di 2FA, oscuramento, registri di controllo | 4: un servizio nuovo, con PostgreSQL e rilasci settimanali | 6: licenza per uso interno; la 3.0 incompatibile da dicembre; il sistema non ne dipende | **70,0** |
| **B. Codice del motore** ([ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md)) | 8: tutto nel registro e sotto il Cancello, con livelli e stop; un collegamento nuovo lo può scrivere un agente di sviluppo in corsia T, come pull request | 4: ogni integrazione va scritta e provata | 8: nessuna licenza; costa lo sviluppo | 8: un solo ingresso con un token per mittente, nessun servizio in più | 8: nessun servizio nuovo, più codice da tenere | 8: nessuna dipendenza da terzi | **72,0** |
| **C. Activepieces** | 6: flussi, 280 e più «pieces» anche come server MCP, passi di approvazione; stesso limite del Cancello | 4: da installare, fuori dal board | 8: nucleo con licenza MIT; funzioni enterprise a pagamento, prezzo non verificato | 4: avvisi e controlli d'accesso non verificati | 4: un servizio nuovo | 6: la licenza MIT ammette la rivendita; maturità non verificata | **55,0** |
| **D. Windmill Community** | 6: flussi in codice, approvazioni con scadenza; permessi sulle approvazioni solo Cloud ed Enterprise | 4: da installare, fuori dal board, pensato per chi scrive codice | 8: gratuito fino a 50 utenti | 6: SSO fino a 10 utenti; avvisi non verificati | 4: un servizio nuovo | 6: licenza AGPLv3 | **57,0** |
| **E. Node-RED** | 4: flussi a eventi; funzioni per agenti e approvazioni non verificate | 4: da installare | 8: licenza Apache 2.0 | 4: non verificata | 4: un servizio nuovo | 6: progetto maturo della OpenJS Foundation | **48,0** |

Fonti dei voti: §3.1 per n8n; [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md) e [ricerca/49 §3](49-instradamento-a-piu-motori.md) per il motore e la corsia T; per C, D ed E [verificato: github.com/activepieces/activepieces; activepieces.com/docs/about/license; github.com/windmill-labs/windmill; windmill.dev/pricing; windmill.dev/docs/flows/flow_approval; github.com/node-red/node-red; nodered.org/about, 14/11/2026].

**Calcolo** [calcolo]: A = (6×35 + 10×20 + 10×15 + 4×10 + 4×10 + 6×10) / 10 = 70,0; B = (8×35 + 4×20 + 8×15 + 8×10 + 8×10 + 8×10) / 10 = 72,0; C = (6×35 + 4×20 + 8×15 + 4×10 + 4×10 + 6×10) / 10 = 55,0; D = (6×35 + 4×20 + 8×15 + 6×10 + 4×10 + 6×10) / 10 = 57,0; E = (4×35 + 4×20 + 8×15 + 4×10 + 4×10 + 6×10) / 10 = 48,0.

**Con e senza l'omaggio.** La Community è gratuita anche a listino: il totale di A non cambia. Se l'«abbonamento» di cui parla Alberto fosse una licenza a pagamento, cambierebbe la sicurezza: con Business (SSO, Git) il voto passerebbe a 6 e il totale a 72,0; con Enterprise (oscuramento, registri di controllo, segreti esterni) a 8 e il totale a 74,0 [calcolo]. Questi due totali valgono solo se la licenza è in omaggio. A listino Business costa 667 € al mese: con i costi a 4, come per ElevenLabs (§5.4.1), sarebbe A = (6×35 + 10×20 + 4×15 + 6×10 + 4×10 + 6×10) / 10 = 63,0, sotto la Community [calcolo]. Non è un dato: è la domanda 4 del §8.

**Cosa ne ricavo** [non verificato: lettura nostra]. A sta 2 punti sotto B, dentro il margine, e i due non sono in concorrenza: B fa ciò da cui gli agenti dipendono, A fa le automazioni interne che non sono agenti. Le altre tre restano indietro di 13 punti o più, anche votate tutte come servizi nuovi, al pari di n8n. Nessuna alternativa supera n8n fuori dal margine: il motore è avanti di 2 punti, dentro il margine.

### 3.5 Costi

- **Oggi**: 0 €. La Community è «the free edition» e non ha un prezzo di listino; si paga solo il server [verificato: docs.n8n.io/deploy/host-n8n/community-edition-features.md; n8n.io/pricing, 14/11/2026].
- **Accanto, il listino dei piani a pagamento**, se l'«abbonamento» fosse uno di questi: Business 667 € al mese con pagamento annuale; Enterprise su richiesta [verificato: n8n.io/pricing/?selfHosted=true, 14/11/2026].
- **Se l'omaggio finisce**: la Community resta gratuita, con la sua licenza. Se c'era una licenza a pagamento, l'istanza perde le funzioni in più e torna Community. Per questo le condizioni del §3.7 usano solo funzioni della Community: la fine dell'omaggio non tocca il progetto [proposta].
- **Costo nascosto**: le patch. Escono correzioni quasi ogni giorno e avvisi alti ogni mese, e la regola è «patch entro 14 giorni» con un responsabile ([ADR-0002](../docs/adr/0002-self-hosted-board-michele.md)).

### 3.6 Rischi

| Rischio | Cosa vuol dire | Come si contiene |
|---|---|---|
| Vulnerabilità frequenti | avvisi alti ogni mese, critici ogni mese fino a maggio 2026, spesso con esecuzione di codice sul server | versione fissata; controllo settimanale degli avvisi; patch entro 14 giorni; editor non esposto; pochi utenti, tutti fidati (§4) |
| Un flusso che scrive fuori | n8n può mandare mail o pubblicare senza il Cancello | nessun flusso verso clienti o prospect; credenziali in sola lettura dove si può; nessuna credenziale dei social in n8n [proposta] |
| Dati rossi nelle esecuzioni | nella Community i dati delle esecuzioni non si oscurano | niente rosso; i flussi con dati gialli non salvano le esecuzioni; la verifica di N10 controlla anche il database di n8n |
| Un agente che costruisce flussi | il server MCP dell'istanza crea e modifica flussi | server MCP dell'istanza e API pubblica spenti; nessuna chiave di n8n agli agenti [proposta] |
| Messaggi di Teams a nome di una persona | il nodo Teams scrive come l'utente collegato: con le credenziali di sola applicazione non crea messaggi né nei canali né nelle chat [verificato: pagina del nodo Microsoft Teams, «Service Principal credential support», 14/11/2026] | gli avvisi degli agenti li manda la Porta. Per gli avvisi a senso unico dei flussi di n8n c'è la notifica nel feed attività di una persona, che non è un messaggio e funziona con le credenziali di sola applicazione: chiede il permesso `TeamsActivity.Send` e una piccola app Teams di accompagnamento installata per chi riceve, e nessun utente con licenza [verificato: pagina del nodo Microsoft Teams, 14/11/2026]. Altrimenti un utente dedicato, con la sua licenza, non quello di una persona [proposta] |
| La 3.0 a dicembre | installazione solo con Docker, nodi tolti | restare sulla 2.x, che ha correzioni per 12 mesi; non usare da subito i nodi che la 3.0 toglie; il passaggio è una scelta a parte |
| La licenza | uso interno sì, rivendita no | n8n non entra in ciò che si rivende; per i servizi del Mappatore ai clienti, i clienti ricevono i risultati, non l'accesso |
| Dipendenza | un flusso fermo ferma una pipeline del board | il sistema di agenti non dipende da n8n ([ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md)) |

### 3.7 Giudizio

**Entra come opzione, con queste condizioni** [proposta]:
1. n8n resta facoltativo, come dice [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md): il sistema di agenti non dipende da lui per la sveglia, per gli eventi, per le catene né per le approvazioni.
2. Serve a tre cose: le pipeline del board, come i bandi della notte; le automazioni interne consigliate dal Mappatore e scelte da una persona; gli avvisi a senso unico dei suoi flussi.
3. Chiama `POST /eventi` con il suo token, oppure scrive solo su sistemi interni con credenziali ristrette. Non manda nulla a clienti o prospect e non pubblica.
4. Niente dati rossi; i flussi con dati gialli non salvano le esecuzioni.
5. Le credenziali le tiene una persona; nessun agente usa n8n, la sua API o il suo server MCP.
6. Versione 2.x fissata, una sola istanza, editor solo dalla rete privata, controlli del §4.
7. Ogni flusso attivo ha la sua riga nel registro dei collegamenti, in git.
8. Lo stop di emergenza ([ricerca/45 §2.7](45-architettura-v3.md)) vale anche per n8n: il motore rifiuta gli eventi con il token di n8n, e si fermano anche i flussi che scrivono su sistemi interni, per esempio spegnendo il servizio. Lo fa chi preme lo stop, con un comando sul server: con l'API pubblica e il server MCP spenti (§4, punto 4) il motore non comanda n8n.

Con il codice del motore sta dentro il margine: n8n è la scelta solo per i ruoli del punto 2; per tutto ciò da cui gli agenti dipendono, vince il motore.

---

## 4. Prima dell'installazione di n8n

Michele installa la Community Edition il 15 novembre 2026 sul server dell'azienda. Ecco che cosa conviene sapere quel giorno, punto per punto.

| # | Che cosa | Che cosa fare | Fonte |
|---|---|---|---|
| 1 | **Come installarlo** | Le prime due strade dell'elenco della documentazione, il comando unico di get.n8n.io (*one-line setup*) e la guida Docker Compose, installano anche i servizi di n8n Assistant. Fra questi c'è `sandbox-runner-1`, un contenitore privilegiato (`privileged: true`) con Docker dentro Docker: n8n dice di trattarlo «as equivalent to root on the host» e di tenerlo «on a dedicated machine or VM with nothing else on it». Tutte e due partono con SQLite, e la porta 5678 resta raggiungibile da fuori della macchina. Sul server dell'azienda conviene la sola immagine `n8nio/n8n:2.47.7` con PostgreSQL (punto 8), senza quei servizi, con la porta legata all'indirizzo locale o alla rete del proxy (punto 3). Chi usa lo stesso il comando unico fissa la versione con `--version 2.47.7` | [verificato: docs.n8n.io/deploy/host-n8n/install-options.md, one-line-setup.md, install-using-docker-compose.md e install-with-docker.md; raw.githubusercontent.com/n8n-io/n8n/master/docker/get-n8n-compose.yml; hub.docker.com, etichetta 2.47.7 dell'immagine n8nio/n8n, 14/11/2026]; la sola immagine con PostgreSQL e la porta legata [proposta] |
| 2 | **Versione** | Prendere la 2.47.7, la stabile del 13 novembre, con il numero esatto (immagine `n8nio/n8n:2.47.7`) e non con un'etichetta che si sposta. Non la 2.48.x né la 3.x, che sono anteprime; non la vecchia linea 1.x. La 2.47.7 contiene le correzioni dei tre avvisi alti del 28 ottobre (vecchi nodi Code, dalla 2.43.3; GraphicsMagick, dalla 2.46.1; isolamento delle espressioni dei flussi, GHSA-gx3v-3x3v-f8r5, che fa eseguire codice sul server a chi può creare o modificare flussi, dalla 2.46.1), dei nove moderati dello stesso giorno (dalla 2.46.1 al più tardi), dei due alti del 13 novembre (ruoli personalizzati, che nella Community non ci sono, dalla 2.47.6; accettazione degli inviti, dalla 2.14.0) e dei tre moderati del 13 novembre (credenziali degli inneschi, AWS Bedrock, nodi di integrazione: tutti dalla 2.47.6). Il giorno stesso, rileggere la pagina degli avvisi: se è uscita una 2.47.x più nuova con correzioni di sicurezza, prendere quella | [verificato: api.github.com/repos/n8n-io/n8n/releases; api.github.com/repos/n8n-io/n8n/security-advisories, GHSA-9p7v-45m2-wxgj, GHSA-f2cw-9483-7vcp, GHSA-gx3v-3x3v-f8r5, GHSA-q8rc-7m84-mfvj, GHSA-m7qq-gm3x-v79g, GHSA-h59h-rf6m-7jp5, GHSA-g333-hr44-g82p, GHSA-c772-hjfp-gfc2; per i ruoli personalizzati, create-custom-instance-roles.md, 14/11/2026] |
| 3 | **Che cosa non esporre** | Il processo n8n mai diretto su internet: «Don't expose the n8n process directly to the internet». La porta 5678 solo dietro il proxy; la porta 5679 del processo che smista i compiti (*task broker*) privata; PostgreSQL e Redis raggiungibili solo da n8n. Per il progetto: l'editor solo dalla rete privata NetBird, come Postiz e listmonk ([ADR-0013](../docs/adr/0013-postiz-listmonk-docuseal.md)); da fuori solo i webhook che servono, con un'intestazione o un JWT e l'elenco degli IP ammessi, perché di serie il nodo ammette nessuna autenticazione e CORS «*». Dietro il proxy si impostano `N8N_PROXY_HOPS=1` e `N8N_WEBHOOK_URL` con l'indirizzo pubblico dei webhook, e il proxy passa le intestazioni `X-Forwarded-For`, `X-Forwarded-Host` e `X-Forwarded-Proto`. Senza `N8N_PROXY_HOPS` n8n vede come chiamante il proxy, e l'elenco degli IP ammessi non distingue chi chiama | [verificato: docs.n8n.io/deploy/host-n8n/install-options/production-requirements.md; pagina del nodo Webhook; configure-webhook-urls-with-reverse-proxy.md, 14/11/2026]; editor sulla rete privata [proposta]; «senza `N8N_PROXY_HOPS`» [non verificato: deduzione] |
| 4 | **Funzioni da spegnere, protezioni da accendere** | API pubblica spenta se non serve, con `N8N_PUBLIC_API_DISABLED=true` («n8n recommends disabling it»); server MCP dell'istanza tolto con `N8N_DISABLED_MODULES=mcp`; raccolta dei dati anonimi d'uso spenta con `N8N_DIAGNOSTICS_ENABLED=false`. Nodi: sulla 2.47.7 non impostare `NODES_EXCLUDE`. Di serie la variabile esclude già Execute Command e Local File Trigger, e i vecchi nodi Function, Function Item e LangChain Code sono bloccati, perché `N8N_DEPRECATED_NODES_BLOCK` vale `true`: non va portato a `false`. Se la si imposta lo stesso, attenzione a due cose. La prima: `NODES_EXCLUDE` sostituisce l'elenco di serie e non vi si somma; se elenca solo i tre nodi vecchi, Execute Command e Local File Trigger si riaccendono. Il valore intero è `NODES_EXCLUDE='["n8n-nodes-base.executeCommand","n8n-nodes-base.localFileTrigger","n8n-nodes-base.function","n8n-nodes-base.functionItem","@n8n/n8n-nodes-langchain.code"]'`. La seconda: il valore deve arrivare a n8n come JSON puro. Gli apici singoli scritti qui valgono per la riga di comando; in un file compose si usa la forma a mappa, `NODES_EXCLUDE: '[…]'`, e non una voce di elenco con gli apici dopo l'uguale. Se il JSON non è valido, la 2.47.7 non avvisa e carica tutti i nodi. Dopo l'avvio, in ogni caso, nell'editor il nodo Execute Command non si deve trovare; se la variabile è impostata, `printenv NODES_EXCLUDE` nel contenitore deve stampare una riga che comincia con `[`. Nodo Code: il suo codice gira in un processo a parte (*task runner*). Di serie la modalità è interna (`N8N_RUNNERS_MODE` vale `internal`), che n8n sconsiglia in produzione: «Internal mode isn't recommended for production». Con credenziali vere serve la modalità esterna: `N8N_RUNNERS_MODE=external`, un segreto in `N8N_RUNNERS_AUTH_TOKEN` e, accanto all'immagine del punto 1, il contenitore `n8nio/runners` nella stessa versione di n8n. Protezione SSRF: di serie è spenta e si accende con `N8N_SSRF_PROTECTION_ENABLED=true`. Accesa, blocca le reti private (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16), l'indirizzo locale (127.0.0.0/8) e altri intervalli riservati: l'host di `POST /eventi` e i sistemi dei flussi ammessi vanno elencati in `N8N_SSRF_ALLOWED_HOSTNAMES` o `N8N_SSRF_ALLOWED_IP_RANGES`. Sulla 2.x l'elenco di serie non comprende 100.64.0.0/10, da cui NetBird di serie prende gli indirizzi: si aggiunge con `N8N_SSRF_BLOCKED_IP_RANGES=default,100.64.0.0/10`, come farà di serie la 3.0. Fra i nomi ammessi vanno solo nomi di zone interne, perché un nome ammesso salta il controllo sugli indirizzi | [verificato: docs.n8n.io/deploy/host-n8n/configure-n8n/security.md, disable-the-public-api.md, control-telemetry.md e enable-ssrf-protection.md; connect-to-n8n-mcp-server.md; variabili della protezione SSRF, ssrf-protection.md; GHSA-9p7v-45m2-wxgj; v20-breaking-changes.md e v30-breaking-changes.md; per `NODES_EXCLUDE`, nodes.md («To enable all nodes, specify `NODES_EXCLUDE: "[]"`», con l'elenco di serie dei due nodi), block-specific-nodes.md e il sorgente della 2.47.7 (nodes.config.ts e decorators.ts); per la forma nel file compose, prova di lettura delle due scritture in YAML; per il nodo Code, set-up-task-runners.md e task-runners.md; per NetBird, docs.netbird.io/manage/settings/networks, 14/11/2026]; non impostare `NODES_EXCLUDE`, controllo dopo l'avvio, MCP tolto, intervallo di NetBird ed elenco degli host [proposta] |
| 5 | **Dove stanno le credenziali, e chi le tiene** | n8n cifra le credenziali nel suo database con la chiave `N8N_ENCRYPTION_KEY`; se non la si dà, la crea al primo avvio nella cartella `~/.n8n`. Va data prima del primo avvio: n8n usa la chiave della variabile solo se non ne ha già salvata una. La guida di produzione dice di generarla (`openssl rand -hex 32`), custodirla e tenere la cartella dei dati su un volume persistente. Nella Community non ci sono i segreti esterni. Chi le tiene: Michele, come proprietario dell'istanza; la chiave nel gestore dei segreti e nel backup, separata dal backup del database, perché senza la chiave le credenziali salvate non si leggono («Without the encryption key […] a restored database or encrypted credential export can't be decrypted»); nessuna credenziale agli agenti; dove si può, credenziali in sola lettura; il token per `POST /eventi` è quello di n8n come mittente | [verificato: docs.n8n.io, set-a-custom-encryption-key.md, production-requirements.md, community-edition-features.md, keep-n8n-running/backup-and-restore.md, 14/11/2026]; chi le tiene [proposta] |
| 6 | **Accesso delle persone** | La 2FA è accesa di serie (`N8N_MFA_ENABLED` vale `true`), ma l'obbligo per tutti è solo Business o Enterprise: nella Community ognuno la attiva da sé, il proprietario per primo. Pochi utenti, tutti fidati: molti avvisi chiedono solo un utente che può modificare flussi | [verificato: user-management-and-2fa.md; manage-security-policies.md; GHSA-q8rc-7m84-mfvj, 14/11/2026] |
| 7 | **Memoria** | Per il solo n8n la documentazione non dà un minimo. Lo dà per l'installazione Docker Compose con i servizi di n8n Assistant (punto 1): 4 GB di RAM e 2 vCPU. L'altra cifra è un esempio basato sul cloud: memoria da 320 MB a 2 GB, database da 512 MB a 4 GB, circa 100 MB a riposo. Dato che n8n non limita i dati che un nodo legge, conviene un limite di memoria al contenitore | [verificato: docs.n8n.io, install-using-docker-compose.md, deploy-as-an-oem-integration/prerequisites.md e fix-memory-issues.md, 14/11/2026]; il limite [proposta] |
| 8 | **Database e sistema** | Linux a 64 bit; PostgreSQL in produzione, versioni 17 e 18 (elenco di luglio 2026), la 16 per compatibilità, in un intervallo che «shifts each year»; SQLite è il valore di serie ma non serve per più utenti. Il PostgreSQL del board è il 16 ([ricerca/25](25-board-michele-e-delta.md), VLAN 40 DATA): per n8n è solo la versione di compatibilità, quindi per n8n conviene un database 17 o 18; la scelta resta a Michele. Redis serve solo con la modalità a code: con una sola istanza non serve. Il database di n8n entra nel backup 3-2-1 ([ADR-0016](../docs/adr/0016-backup-3-2-1.md)), insieme alla cartella `.n8n`, che per n8n fa parte del backup completo | [verificato: production-requirements.md; choose-n8ns-database.md; backup-and-restore.md, 14/11/2026]; database 17 o 18 e backup [proposta] |
| 9 | **Esecuzioni e orari** | La pulizia delle esecuzioni è accesa di serie: dopo 336 ore o oltre 10.000 esecuzioni. Di serie n8n salva le esecuzioni riuscite, quelle fallite e quelle manuali: per i flussi con dati gialli vanno spente tutte e tre, dalle impostazioni di ogni flusso. Il fuso orario di serie è `America/New_York`: va impostato quello di Roma, con `GENERIC_TIMEZONE=Europe/Rome` e, con Docker, anche con `TZ=Europe/Rome`. Il pianificatore durevole è acceso di serie dalla 2.45.0, ma di serie lo Schedule Trigger scarta gli orari persi: se il server è spento all'ora fissata, il flusso salta. Ogni Schedule Trigger da recuperare, prima di tutto quello dei bandi della notte, va impostato, nella scheda Settings del nodo, alla voce «If Execution Is Missed», su «Run the Most Recent Missed Execution»; l'opzione c'è sui nodi aggiunti dalla 2.36 in poi | [verificato: manage-execution-data.md; executions.md; pagina dello Schedule Trigger; timezone-and-localization.md; install-with-docker.md, 14/11/2026]; quali flussi recuperare [proposta] |
| 10 | **Che cosa manca alla Community** | Variabili personalizzate, ambienti, segreti esterni, archivio esterno dei file, flusso dei registri verso fuori, più istanze principali, progetti, SSO, condivisione di flussi e credenziali, Git. In più, solo nei piani a pagamento: l'obbligo di 2FA e le politiche di sicurezza (Business ed Enterprise), l'oscuramento dei dati delle esecuzioni e i registri di controllo (Enterprise). La chiave gratuita della Community registrata dà cartelle, la copia nell'editor dei dati di un'esecuzione e dati personalizzati delle esecuzioni; registrarla vuol dire dare una mail a n8n, e lo decide una persona | [verificato: community-edition-features.md; manage-security-policies.md; redact-execution-data.md; n8n.io/pricing/?selfHosted=true, 14/11/2026] |

---

## 5. ElevenLabs

### 5.1 Che cos'è oggi

**Il prodotto.**
- È un servizio in cloud per la voce sintetica, venduto in tre linee: ElevenCreative per chi produce contenuti dall'interfaccia, ElevenAgents per gli agenti vocali, ElevenAPI per gli sviluppatori [verificato: elevenlabs.io/pricing, 14/11/2026].
- Il modello di sintesi più espressivo è eleven_v4, consigliato per i contenuti; parla più di 90 lingue, italiano compreso, fino a 10.000 caratteri per richiesta. Per il tempo reale c'è eleven_v4_turbo, con circa 100 ms di latenza mediana del modello, esclusa la rete. Tutti e due sono usciti il 28 settembre 2026 [verificato: elevenlabs.io/docs/overview/models; elevenlabs.io/blog/eleven-v4, 14/11/2026].
- Fa anche musica (music_v2_5), effetti sonori, doppiaggio, trascrizione (scribe_v3, del 10 novembre 2026) e, con modelli di altri fornitori, immagini e video [verificato: elevenlabs.io/docs/overview/models; elevenlabs.io/blog/scribe-v3; elevenlabs.io/docs/overview/capabilities/image-video, 14/11/2026].
- **Clonazione**: l'istantanea dà risultati con 1-3 minuti di audio; la professionale chiede almeno 30 minuti e una verifica letta a voce. «Even with their consent, you cannot clone someone else's voice»: la voce professionale di un founder la crea e la verifica il founder [verificato: elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning, 14/11/2026].
- **Telefono**: ElevenAgents si collega a Twilio o a un trunk SIP e passa la chiamata a una persona; gli IP fissi per le liste di permesso sono solo Enterprise [verificato: elevenlabs.io/docs/eleven-agents/overview; sip-trunking; transfer-to-human, 14/11/2026]. Dal 16 settembre 2026 c'è anche Reception, un centralino pronto; i numeri italiani arrivano dopo una richiesta regolatoria [verificato: elevenlabs.io/blog/reception; elevenlabs.io/docs/reception-ai/phone-numbers/international-numbers, 14/11/2026]. Con Speech Engine ElevenLabs fa ascolto, turni e voce, e la logica dell'agente resta sul nostro server [verificato: elevenlabs.io/docs/changelog/2026/5/25, 14/11/2026].

**Dati e conformità.**
- Di base i dati sono conservati negli USA; ambienti isolati in UE solo per i clienti Enterprise: «Data residency is an exclusive feature available to ElevenLabs' Enterprise customers» [verificato: elevenlabs.io/docs/overview/administration/data-residency, 14/11/2026].
- La modalità senza conservazione è solo per alcuni clienti Enterprise e non copre clonazione, doppiaggio e interfaccia web [verificato: elevenlabs.io/docs/eleven-api/resources/zero-retention-mode, 14/11/2026].
- Le conversazioni degli agenti si conservano per 2 anni di serie; il periodo si può ridurre, anche a zero [verificato: elevenlabs.io/docs/eleven-agents/customization/privacy/retention, 14/11/2026].
- Il DPA vale anche per chi accetta i termini per conto di un'azienda, senza contratto su misura; è aggiornato all'8 aprile 2026; i trasferimenti verso gli USA usano il Data Privacy Framework o le clausole contrattuali tipo [verificato: elevenlabs.io/dpa; elevenlabs.io/terms-of-use, 14/11/2026].
- ElevenLabs usa ingressi e uscite per addestrare i modelli, salvo opposizione dal menu «Data use»; l'opposizione vale solo da quel momento [verificato: elevenlabs.io/privacy-policy, 14/11/2026].
- Con il piano Free «you may only use the Services for non-commercial purposes» [verificato: elevenlabs.io/terms-of-use, 14/11/2026].
- Le regole d'uso vietano di clonare la voce di una persona viva senza consenso e chiedono di dire quando si parla con un'IA, se la legge lo richiede [verificato: elevenlabs.io/use-policy, 14/11/2026].
- Certificazioni rinnovate a ottobre 2026: ISO/IEC 27001, 27701, 42001, SOC 2 Type II, Cyber Essentials Plus e altre [verificato: elevenlabs.io/blog/certification-renewals, 14/11/2026].
- Gli obblighi di trasparenza del regolamento europeo sull'IA valgono dal 2 agosto 2026; nell'elenco dei firmatari del codice di buone pratiche, aggiornato al 24 settembre 2026, ElevenLabs non c'è [verificato: digital-strategy.ec.europa.eu, 14/11/2026].

**Per gli agenti.**
- SDK ufficiali con licenza MIT; il pacchetto Python è alla 2.78.0 del 12 novembre 2026 [verificato: pypi.org/project/elevenlabs, 14/11/2026].
- Il server MCP locale è archiviato dal 20 agosto 2026; quello ospitato si collega con OAuth, può cancellare agenti, e l'amministratore può spegnere singoli strumenti [verificato: github.com/elevenlabs/elevenlabs-mcp; elevenlabs.io/docs/eleven-agents/operate/hosted-mcp, 14/11/2026]. Per l'accesso la pagina descrive solo OAuth: una persona entra con il suo account ElevenLabs e «No API keys are copied into the client» [verificato: stessa pagina]. Quindi non serve a un programma che lavora senza una persona [non verificato: deduzione, la pagina non nomina altri accessi].
- Le chiavi API si limitano per indirizzo, con un tetto di crediti e un elenco di IP ammessi, che accetta solo indirizzi pubblici; per i sistemi automatici si consigliano gli account di servizio [verificato: elevenlabs.io/docs/overview/administration/workspaces/api-keys, 14/11/2026]. Gli account di servizio però ci sono solo per le aree di lavoro a più posti, e li gestisce solo l'amministratore: «Service Accounts are currently only available for multi-seat customers, and only Workspace admins can use this feature»; per averli si contattano le vendite. Una chiave personale richiede invece un posto Full [verificato: elevenlabs.io/docs/overview/administration/workspaces/service-accounts; pagina delle chiavi API, 14/11/2026]. A listino il primo piano a più posti è Scale, con 3 posti; Creator e Pro non indicano altri posti [verificato: elevenlabs.io/pricing, 14/11/2026].
- La ricarica automatica, se accesa, addebita la carta salvata quando il saldo scende sotto una soglia [verificato: elevenlabs.io/docs/overview/administration/pay-as-you-go, 14/11/2026].

### 5.2 Che cosa farebbe nel progetto, e per quali agenti

| Agente | Che cosa farebbe | Che cosa dice oggi il disegno | Proposta |
|---|---|---|---|
| Agente video (Studio contenuti, fase 4, corsia S) | voce fuori campo senza founder con eleven_v4; musica, effetti; la lettura di uno script con la voce di un founder solo dopo il parere legale (§5.3). Doppiaggio e sottotitoli no: chiedono di mandare l'audio registrato del video, che oggi è rosso ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)); i sottotitoli si fanno con la trascrizione in casa ([ADR-0007](../docs/adr/0007-call-e-trascrizione.md)) | nomina solo Higgsfield, HyperFrames e After Effects ([PRESENTAZIONE-CEO.md §4.5](../PRESENTAZIONE-CEO.md)); le direttive dei contenuti usano già ElevenLabs ([ricerca/05 §3.4](05-marketing-e-post.md)) | sì, come opzione (§5.7) |
| Copywriter ed Editoriale (Marketing) | trascrivere podcast e sessioni fonte | la trascrizione si fa in casa ([ADR-0007](../docs/adr/0007-call-e-trascrizione.md)) | no: per i testi pubblici la trascrizione in casa basta; per le call il dato è rosso |
| Andrea (Vendite, fase 5) | voce e agente telefonico | tutto in casa; ElevenLabs ultima riserva ([ADR-0008](../docs/adr/0008-andrea-centralino.md)) | non per ora; la riserva si precisa (§5.7) |

Le proposte della colonna di destra sono [proposta].

### 5.3 Che cosa chiede al disegno

- **Corsia**: S, dove lavora l'Agente video («Video e grafiche», [ricerca/45 §3.2](45-architettura-v3.md)). ElevenLabs è uno strumento del motore che l'agente chiama; la chiave la tiene lo strumento [proposta].
- **Livello nel Cancello**: produrre un file audio non è un'azione verso fuori. Pubblicarlo sì, al livello del post: pagina aziendale L1, poi L2 con la finestra di 24 ore; post dei founder sempre L1 ([ricerca/45 §4.1](45-architettura-v3.md); [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md)). Un contenuto con voce sintetica non va mai in messaggi diretti, commenti, outreach o call, come chiedono le regole del marketing ([ricerca/05 §5.6](05-marketing-e-post.md)); tutto ciò che esce a L2 o L3 porta la riga AI [proposta].
- **Colore dei dati**: solo verde, cioè gli script dei contenuti pubblici. ElevenLabs non è nel board, quindi il giallo non ci va senza un'eccezione ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)). Per la voce dei founder vale oggi la riga rossa di ADR-0009, che dice «audio» senza distinguere: le registrazioni e la voce clonata restano rosse: non si caricano su ElevenLabs e gli agenti non le usano, finché il parere legale non decide (domanda 16). I due cloni già fatti restano fermi (domanda 9). La proposta è nel §7.4 [proposta].
- **Credenziali che non vanno agli agenti**: una chiave di account di servizio, che chiede un'area di lavoro a più posti (§5.1), limitata agli indirizzi di sintesi, musica ed effetti, senza quelli che creano o cancellano voci e agenti; un tetto di crediti; l'elenco degli IP pubblici da cui esce il server; la chiave nel gestore dei segreti, letta solo dallo strumento. Il server MCP ospitato resta alle persone. La ricarica automatica resta spenta, perché i pagamenti non sono mai automatici [proposta].
- **Registro**: la riga dell'Agente video aggiunge il fornitore ElevenLabs con colore massimo verde; ElevenLabs entra nel registro dei trattamenti ([ricerca/45 §2](45-architettura-v3.md); [ADR-0025](../docs/adr/0025-un-modello-per-agente.md)) [proposta].

### 5.4 Le alternative a confronto

**5.4.1 Voce, musica ed effetti per i contenuti pubblici** (dati verdi). Voti da 0 a 10; totale su 100.

| Alternativa | Autonomia (35) | Tempo al valore (20) | Costi (15) | Sicurezza essenziale (10) | Server e manutenzione (10) | Rischio (10) | Totale |
|---|---|---|---|---|---|---|---|
| **A. ElevenLabs con l'omaggio** | 8: API e SDK, chiavi limitate, costo leggibile prima; voce, musica ed effetti in un servizio; la voce professionale la fa il founder | 8: già disponibile, nulla da installare, italiano in eleven_v4; fuori dal board, serve l'eccezione di Michele | 10: 0 € oggi | 6: dati negli USA; addestramento salvo rinuncia; DPA valido; certificazioni rinnovate a ottobre | 10: niente sul server | 6: prodotto che cambia ogni mese; contrasto aperto sulla riga AI | **81,0** |
| **B. Voce in casa sulla seconda GPU** (Qwen3-TTS, Chatterbox) | 6: dal motore senza chiavi esterne, ma solo voce: musica ed effetti restano da trovare | 2: serve la seconda GPU, non ancora comprata; la RTX 4000 è piena | 6: licenze aperte, ma la GPU va comprata | 10: niente esce dal server | 4: modelli da tenere e carico sulla GPU | 6: italiano da misurare; le misure pubblicate le dà un concorrente | **54,0** |
| **C. OpenAI, sintesi vocale** | 6: API semplice, solo voce | 6: account e chiave nuovi, fuori dal board | 8: 30 $ per milione di caratteri con tts-1-hd | 4: fornitore USA; DPA e conservazione non letti il 14 novembre 2026, quindi non verificata | 10: niente sul server | 6: italiano non verificato | **65,0** |
| **D. Amazon Polly** | 6: solo voce | 4: account AWS, fuori dal board; l'italiano non è scritto sulla pagina dei prezzi | 8: 30 $ per milione di caratteri con le voci Generative; quota gratuita il primo anno | 4: non verificata | 10: niente sul server | 6: italiano non verificato | **61,0** |

Fonti dei voti: §5.1 per ElevenLabs; [verificato: huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base; huggingface.co/ResembleAI/chatterbox; developers.openai.com/api/docs/pricing; aws.amazon.com/polly/pricing, 14/11/2026]; la seconda GPU e la RTX 4000 da [ricerca/48 §6.2](48-modelli-locali-e-gpu.md) e [ADR-0014](../docs/adr/0014-seconda-gpu-blackwell.md). Higgsfield, che il marketing usa già, non è nella tabella: i suoi strumenti vocali non li ho verificati il 14 novembre 2026, e le direttive vietano `voice_change` e `create_voice` sui founder ([ricerca/05 §3.4](05-marketing-e-post.md)).

**Calcolo** [calcolo]: A = (8×35 + 8×20 + 10×15 + 6×10 + 10×10 + 6×10) / 10 = 81,0; B = (6×35 + 2×20 + 6×15 + 10×10 + 4×10 + 6×10) / 10 = 54,0; C = (6×35 + 6×20 + 8×15 + 4×10 + 10×10 + 6×10) / 10 = 65,0; D = (6×35 + 4×20 + 8×15 + 4×10 + 10×10 + 6×10) / 10 = 61,0. Il totale di A con l'omaggio vale se l'omaggio copre l'API e un'area di lavoro a più posti, con gli account di servizio [non verificato: domanda 7]; altrimenti vale il totale a listino.

**A listino**: la chiave di account di servizio della condizione 2 (§5.7) chiede un'area di lavoro a più posti, quindi almeno Scale, 267,13 € al mese, oppure un accordo con le vendite (§5.1). I costi scendono a 4 e il tempo a 6, perché all'eccezione si aggiunge l'acquisto: A = (8×35 + 6×20 + 4×15 + 6×10 + 10×10 + 6×10) / 10 = 68,0 [calcolo]. ElevenLabs resta davanti anche senza l'omaggio, di 3 punti, dentro il margine: si sceglie sulle condizioni, e nessuna alternativa dà voce, musica ed effetti insieme. Il confronto poggia su due voti di OpenAI dati senza lettura: con sicurezza 6 e rischio 8 sarebbe C = (6×35 + 6×20 + 8×15 + 6×10 + 10×10 + 8×10) / 10 = 69,0, un punto sopra, sempre dentro il margine [calcolo]. Per la musica Scale vale solo sotto i 10 dipendenti (§5.5).

**5.4.2 La voce di Andrea** (dati gialli e rossi).

| Alternativa | Autonomia (35) | Tempo al valore (20) | Costi (15) | Sicurezza essenziale (10) | Server e manutenzione (10) | Rischio (10) | Totale |
|---|---|---|---|---|---|---|---|
| **A. Catena in casa di ADR-0008** (Asterisk, Pipecat, ascolto e voce in casa, Haiku via LiteLLM) | 8: sotto il Cancello, con il consenso controllato | 4: fase 5, tutto da costruire; voci migliori con la seconda GPU | 8: 44-90 € al mese, più lo sviluppo | 10: l'audio resta in casa | 4: una rete, Asterisk, Pipecat e modelli da aggiornare | 6: voce italiana da provare; il pezzo fra Pipecat e Asterisk è della comunità | **68,0** |
| **B. Ascolto in casa, voce di ElevenLabs** (al fornitore va solo il testo delle risposte) | 8: stessa catena e stesso Cancello | 4: serve comunque il centralino; si evita la prova della voce in casa, ma ElevenLabs è fuori dal board e serve l'eccezione di Michele | 8: la linea e lo sviluppo come A; ElevenLabs 0 € oggi; a listino 2, perché alla linea e allo sviluppo si aggiunge il piano a più posti: la chiave di account di servizio, come per i contenuti (§5.3), chiede almeno Scale, 267,13 € al mese | 6: il testo delle risposte va negli USA a un fornitore fuori dal board e può contenere dati rossi, quindi passa prima da un filtro locale; l'audio di chi chiama resta in casa | 6: un modello di voce in meno sulla GPU | 6: latenza su internet da misurare | **66,0** |
| **C. ElevenAgents con trunk SIP o Twilio** | 6: la logica gira sulla loro piattaforma, fuori dal nostro registro | 6: piattaforma pronta, passaggio a una persona; fuori dal board | 8: 0 € oggi se l'omaggio copre i minuti; a listino Pro 99 $ con 1.238 minuti, più modello e operatore | 2: audio e trascrizioni di chi chiama negli USA, 2 anni di serie | 10: niente sul server | 4: viola un limite fisso | **61,0, esclusa** |
| **D. Reception, centralino pronto** | 4: prodotto chiuso, integrazione con il Cancello non documentata | 6: pronto; numero italiano dopo la richiesta regolatoria; fuori dal board | 8: prova di 14 giorni, poi da 29 $ al mese | 2: come C, con registrazione di ogni chiamata | 10: niente sul server | 4: viola un limite fisso | **54,0, esclusa** |

Fonti: [ADR-0008](../docs/adr/0008-andrea-centralino.md) e [ricerca/31](31-voce-andrea-self-hosted.md) per A; §5.1 per B, C e D [verificato: elevenlabs.io/pricing/api; elevenlabs.io/pricing/agents; elevenlabs.io/docs/reception-ai/billing/plans-and-pricing, 14/11/2026]. Pipecat ha un servizio pronto per la voce di ElevenLabs [verificato: github.com/pipecat-ai/pipecat, README, 14/11/2026].

**Calcolo** [calcolo]: A = (8×35 + 4×20 + 8×15 + 10×10 + 4×10 + 6×10) / 10 = 68,0; B = (8×35 + 4×20 + 8×15 + 6×10 + 6×10 + 6×10) / 10 = 66,0; C = (6×35 + 6×20 + 8×15 + 2×10 + 10×10 + 4×10) / 10 = 61,0; D = (4×35 + 6×20 + 8×15 + 2×10 + 10×10 + 4×10) / 10 = 54,0. Anche il totale di B con l'omaggio vale se l'omaggio copre l'API e un'area di lavoro a più posti [non verificato: domanda 7]; altrimenti vale il totale a listino. A listino i costi di B scendono a 2, perché alla linea e allo sviluppo si aggiunge il piano a più posti, e il tempo a 2, perché all'eccezione si aggiunge l'acquisto, come nel §5.4.1: B = (8×35 + 2×20 + 2×15 + 6×10 + 6×10 + 6×10) / 10 = 53,0.

**Cosa ne ricavo** [non verificato: lettura nostra]. Per i contenuti ElevenLabs vince netto con l'omaggio e resta davanti a listino, di 3 punti, dentro il margine: nessuna alternativa dà voce, musica ed effetti insieme, e la voce in casa aspetta una GPU che non c'è. Per Andrea C e D sono escluse dal limite sui dati rossi, qualunque sia il totale. B sta dietro ad A: di 2 punti con l'omaggio, dentro il margine, e di 15 a listino, perché costa la linea e lo sviluppo come A e chiede l'eccezione di Michele e, a listino, un piano a più posti. Andrea arriva nella fase 5: oggi non c'è niente da scegliere. B conviene solo se la voce in casa non regge, e chiede un filtro locale che fermi il rosso nel testo delle risposte e un'eccezione di Michele.

### 5.5 Costi

- **Oggi**: 0 €, perché l'azienda dispone di ElevenLabs in omaggio. Quale piano copra l'omaggio non è confermato: la repo riporta una dotazione di 33 milioni di caratteri, con piano, voci professionali e licenza della musica «da leggere» ([ricerca/14](14-costi-abbonamenti-e-api.md)). È un dato da confermare (domanda 7).
- **Accanto, il listino** [verificato: elevenlabs.io/pricing, 14/11/2026; euro al cambio di riferimento BCE del 23/10/2026, 1 $ = 0,8934 €, lo stesso di [ricerca/14](14-costi-abbonamenti-e-api.md), calcolo]:

| Piano | Al mese | In euro | Crediti al mese | Voci professionali | Note |
|---|---|---|---|---|---|
| Free | 0 $ | 0 € | 10.000 | nessuna | solo uso non commerciale |
| Starter | 6 $ | 5,36 € | 30.000 | nessuna | licenza commerciale |
| Creator | 22 $ | 19,65 € | 121.000 | 1 | |
| Pro | 99 $ | 88,45 € | 600.000 | 1 | 1.238 minuti di agenti, 20 chiamate insieme |
| Scale | 299 $ | 267,13 € | 1.800.000 | 3 | 3 posti: il primo piano a più posti |
| Business | 990 $ | 884,47 € | 6.000.000 | 10 | 10 posti |
| Enterprise | su misura | — | su misura | — | residenza in UE, DPA e SLA su misura |

- Pagando l'anno si paga l'equivalente di 10 mesi; i crediti non usati passano al mese dopo per al massimo due mesi [verificato: elevenlabs.io/pricing, 14/11/2026].
- Per la musica i termini mettono un limite a parte: Free, Starter, Creator e Pro valgono solo per uso individuale («For Individual Use Only»); Scale vale per aziende con meno di 10 dipendenti, Business con meno di 50; oltre serve un contratto Enterprise Music [verificato: elevenlabs.io/music-terms, allegato A, aggiornato al 9 ottobre 2026, 14/11/2026].
- **Quanto serve allo Studio** [non verificato: stima, il volume non è misurato]: quattro video alla settimana con un minuto di voce ciascuno sono circa 16 minuti al mese, cioè circa 14.000 caratteri; con cinque minuti di musica (900 crediti al minuto) e venti effetti (200 crediti l'uno) [verificato per i crediti: elevenlabs.io/pricing, 14/11/2026] si arriva a circa 23.000 crediti. Starter basterebbe per i crediti, ma non ha voci professionali; Creator copre i crediti con margine. Per la musica però un'azienda non può usare i piani fino a Pro, e la chiave di account di servizio della condizione 2 (§5.7) chiede un'area di lavoro a più posti: a listino almeno Scale, che per la musica vale sotto i 10 dipendenti, oppure un accordo con le vendite (§5.1). Una dotazione da 33 milioni di caratteri vale 12 mesi [verificato: elevenlabs.io/pricing, 14/11/2026]. Se l'omaggio è quella dotazione, e i caratteri valgono come crediti, copre questo consumo con largo margine per tutti i 12 mesi [non verificato: domanda 7]; resta da sapere da quando contano i 12 mesi.
- **Se l'omaggio finisce**: o si paga il listino del primo piano a più posti, Scale a 267,13 € al mese (Business a 884,47 € se l'azienda usa la musica e ha da 10 a 49 dipendenti), o quanto si accorda con le vendite, o lo Studio passa alla sintesi di OpenAI a consumo, oppure alla voce in casa quando c'è la seconda GPU. Se il conto tornasse al piano Free, l'uso commerciale non sarebbe più ammesso: per questo ogni file prodotto si salva subito nei nostri archivi, con lo script e il piano con cui è stato fatto (condizione 8 del §5.7) [proposta]. Per la musica i termini lo dicono: chi ha un piano senza contratto Enterprise e lo declassa o lo chiude tiene la musica già fatta sotto il piano con cui è stata creata [verificato: elevenlabs.io/music-terms, §1.5, 14/11/2026]. Per voce ed effetti, se i file fatti durante l'omaggio restino usabili a fini commerciali dopo il passaggio al Free, i termini letti non lo dicono [non verificato].

### 5.6 Rischi

| Rischio | Cosa vuol dire | Come si contiene |
|---|---|---|
| L'omaggio finisce | il piano Free vieta l'uso commerciale | listino o alternativa scelti prima; file salvati nei nostri archivi (§5.5) |
| Addestramento sui contenuti | di serie ElevenLabs addestra su ingressi e uscite | rinuncia dal menu «Data use» impostata subito, perché sull'account ci sono già due cloni (§1.4): vale solo da quel momento |
| Voce dei founder | la voce professionale la crea solo la persona; è un dato personale | finché il parere legale non decide resta un dato rosso: non si carica su ElevenLabs e gli agenti non la usano, e i due cloni già fatti restano fermi (domanda 9); dopo, se il parere lo ammette, la crea il founder dal suo account, con consenso scritto, e gli agenti usano solo la voce già creata, per script approvati e con l'eccezione di Michele; mai in messaggi diretti, commenti, outreach o call |
| Cancellazioni | il server MCP ospitato e il nodo di n8n cancellano voci e agenti | chiave limitata agli indirizzi di sintesi, musica ed effetti; strumenti distruttivi spenti dall'amministratore |
| Pagamenti automatici | la ricarica automatica addebita la carta | ricarica spenta; tetto di crediti sulla chiave |
| Licenza della musica | Free, Starter, Creator e Pro valgono solo per uso individuale; Scale per aziende con meno di 10 dipendenti, Business con meno di 50; oltre serve un contratto Enterprise Music. Sui piani senza contratto su misura sono esclusi cinema, TV, radio e Studio Games, cioè i giochi venduti o monetizzati, non quelli indipendenti; Free e Starter non ammettono la distribuzione della musica in streaming [verificato: elevenlabs.io/music-terms, allegato A; elevenlabs.io/music, 14/11/2026] | musica solo con il piano verificato, come già chiedono le direttive dei contenuti, e solo se l'azienda rientra nel limite di dipendenti di quel piano |
| Riga AI | le direttive dei contenuti vietano le etichette; il Cancello mette la riga AI su ciò che esce a L2 o L3; la trasparenza vale dal 2 agosto 2026 | decide Alberto, con il parere (§8); fino ad allora vale la regola del Cancello |
| Prodotto che cambia | modelli ritirati a data fissa (Music v1 il 31 gennaio 2027) [verificato: elevenlabs.io/docs/overview/models, 14/11/2026], prezzi tagliati il 7 maggio 2026 [verificato: elevenlabs.io/blog/weve-lowered-api-agents-pricing-and-introduced-pay-as-you-go, 14/11/2026] | modello fissato nel registro; prezzi riletti prima di ogni acquisto |

### 5.7 Giudizio

**Per i contenuti dello Studio: entra come opzione, con queste condizioni** [proposta]:
1. Solo dati verdi: script di contenuti pubblici approvati.
2. Chiave di account di servizio limitata agli indirizzi di sintesi, musica ed effetti, con un tetto di crediti e gli IP pubblici da cui esce il server; la tiene lo strumento del motore, non l'agente. Gli account di servizio ci sono solo nelle aree di lavoro a più posti (§5.1).
3. Nessuna cancellazione e nessuna creazione di voci da parte degli agenti; finché il parere legale non decide, la voce dei founder non si carica su ElevenLabs e gli agenti non la usano; dopo, se il parere lo ammette, la crea solo il founder, e gli agenti la usano con l'eccezione di Michele (§7.4).
4. Ricarica automatica spenta; rinuncia all'addestramento impostata subito, perché sull'account ci sono già due cloni (§1.4).
5. Pubblicazione dal Cancello, al livello del post, con la riga AI dove esce a L2 o L3; mai voce sintetica in messaggi diretti, commenti, outreach o call.
6. Entra con l'Agente video, nella fase 4: prima di allora le persone possono usarlo a mano per i contenuti verdi, fuori dal sistema.
7. È un'eccezione al board, da approvare con Michele ([ADR-0002](../docs/adr/0002-self-hosted-board-michele.md)), e ha un responsabile.
8. Ogni file prodotto si salva nei nostri archivi, con lo script e il piano con cui è stato fatto (§5.5).

**Per Andrea: non entra per ora.** Resta [ADR-0008](../docs/adr/0008-andrea-centralino.md). L'ultima riserva si precisa così: solo la voce delle risposte di Andrea, con una chiave di account di servizio come nella condizione 2, con ascolto, trascrizione e registrazione sempre in casa, e solo se la voce italiana in casa non passa la prova d'ascolto. Il testo delle risposte può contenere dati rossi, perché può ripetere ciò che dice chi chiama: prima della sintesi esterna un filtro locale ferma o oscura il rosso, come fa ADR-0009 per l'API, oppure le risposte si prendono da un elenco chiuso di frasi. Il colore del testo delle risposte resta fra le domande del §8 [proposta].

**Per la trascrizione: non entra.** Resta [ADR-0007](../docs/adr/0007-call-e-trascrizione.md).

---

## 6. Moda

### 6.1 Che cos'è oggi

**Quale prodotto.** Moda è moda.app, il servizio che il connettore per Claude «Moda - Slides and Designs» porta con la dicitura «Made by Moda» e il bollino «Anthropic verified» [verificato: claude.com/connectors/moda, 14/11/2026]. La pubblica Nullframe, Inc., che opera con il nome Moda e ha sede a New York [verificato: moda.app/terms, 14/11/2026]. Gli omonimi, un'app Shopify per foto di moda e un'app per l'armadio personale, non fanno grafica per il marketing e li ho scartati [non verificato: le loro pagine non si sono lette il 14 novembre 2026].

**Il prodotto.**
- Un agente IA crea e modifica su una tela vettoriale slide, post social, caroselli, annunci, documenti, PDF, diagrammi, brevi video e siti; ogni elemento resta modificabile [verificato: moda.app; moda.app/llms.txt, 14/11/2026].
- Il kit del marchio si ricava dal sito dell'azienda [verificato: docs.moda.app/mcp/tools, 14/11/2026].
- Esporta in PDF, PowerPoint, PNG, JPG, MP4, GIF, WebP e Google Slides. Nel passaggio a PowerPoint caratteri ed effetti possono cambiare: «For the most faithful reproduction, use PDF export instead» [verificato: docs.moda.app/help/export/formats.md e troubleshooting.md, 14/11/2026].
- Importa PowerPoint, fino a 250 MB, e Google Slides, con «a best-effort conversion, not a pixel-perfect copy»; i PDF non si importano [verificato: docs.moda.app/help/getting-started/importing-files, 14/11/2026].
- All'agente si scrive nella propria lingua; l'italiano non è nominato [verificato: docs.moda.app/help/faq.md, 14/11/2026].
- È uscita al pubblico il 24 marzo 2026, con un finanziamento iniziale di 7,5 milioni di dollari [verificato: comunicato su markets.financialcontent.com, 14/11/2026].

**Dati e conformità.**
- Dati negli USA, su Google Cloud nella regione us-central1, in Iowa [verificato: moda.app/dpa, 14/11/2026].
- Il DPA fa parte dei termini, è aggiornato al 21 ottobre 2026 e usa le clausole contrattuali tipo per i trasferimenti dall'Europa [verificato: stessa pagina].
- Circa 30 sub-responsabili, quasi tutti negli USA: fra questi Anthropic, OpenAI, Google ed ElevenLabs per la voce [verificato: stessa pagina].
- «Unless Customer opts out, Moda may use Customer Data, Inputs, Outputs» per sviluppare i suoi modelli; la rinuncia si chiede con una mail e vale da quel momento [verificato: moda.app/terms, 14/11/2026].
- Il portale della sicurezza mostra SOC 2 Type 1 e Type 2 senza stato né date [verificato: trust.moda.app, 14/11/2026]. Le pagine non concordano su dove stia l'accesso unico SSO: la pagina della sicurezza dice Ultra, quella dei prezzi Enterprise [verificato: docs.moda.app/help/trust-security; moda.app/pricing, 14/11/2026].
- La responsabilità di Moda ha un tetto: il maggiore fra quanto pagato in 12 mesi e 1.000 dollari; i termini cambiano dal momento in cui sono pubblicati [verificato: moda.app/terms, 14/11/2026].

**Per gli agenti.**
- Il connettore remoto `https://agents.moda.app/mcp` accetta OAuth oppure una chiave API nell'intestazione di autorizzazione: lo può usare un motore sul server senza una persona davanti [verificato: docs.moda.app/agents/mcp-connector.md, 14/11/2026].
- Fra i suoi strumenti ci sono tre cancellazioni (`canvas_delete`, `brand_delete`, `drive_delete`) e la condivisione con un link (`canvas_share`); la pagina non parla di una conferma [verificato: stessa pagina; claude.com/connectors/moda, 14/11/2026]. Gli agenti di Moda pubblicano anche siti su `*.moda.page` [verificato: docs.moda.app/agents.md, 14/11/2026].
- Una chiave creata dalle impostazioni riceve di serie tutti i permessi tranne admin, e non c'è un permesso a parte per cancellare [verificato: docs.moda.app/api-reference/authentication, 14/11/2026].
- La CLI (`@moda-design/moda`) lavora senza browser con una chiave, non stampa mai le credenziali e, per ogni spesa in crediti, mostra la classe di costo prima e la ricevuta dopo [verificato: docs.moda.app/agents/cli-quickstart.md, 14/11/2026]. Ha licenza Apache-2.0 ed è alla versione 0.17.38 [verificato: registry.npmjs.org/@moda-design/moda; api.github.com/repos/moda-design/moda, 14/11/2026]. La sua repo su GitHub è nata il 10 agosto 2026 e si descrive «prototype» [verificato: api.github.com/repos/moda-design/moda, 14/11/2026].
- Limiti dell'API: 120 richieste al minuto per chiave, 25 esportazioni al minuto; lavori contemporanei 3 sul Free, 10 sul Pro, 15 sull'Ultra [verificato: docs.moda.app/api-reference/usage-limits, 14/11/2026].
- Su Claude Team il connettore lo aggiunge solo il proprietario dell'organizzazione [verificato: docs.moda.app/agents/mcp-connector.md, 14/11/2026].

### 6.2 Che cosa farebbe nel progetto, e per quali agenti

| Agente | Che cosa farebbe | Che cosa dice oggi il disegno | Proposta |
|---|---|---|---|
| Agente grafiche (Studio, fase 4) | caroselli 1080×1350, copertine, immagini con il kit del marchio | «con i nostri template» ([PRESENTAZIONE-CEO.md §4.5](../PRESENTAZIONE-CEO.md)); oggi il modello HTML; le direttive dei contenuti ammettono moda solo se autorizzata, senza video, senza founder, senza filigrana ([DIRETTIVE_CONTENUTI.md](../allegati/marketing/DIRETTIVE_CONTENUTI.md)) | sì, come opzione, dati verdi |
| Agente slide (Studio, fase 3) | presentazioni pubbliche (verdi); brief prima dell'incontro e slide al cliente (gialli) | decisione 15: Claude Team e template SerSan; «moda.app solo se ammesso» ([PRESENTAZIONE-CEO.md, appendice A, D4](../PRESENTAZIONE-CEO.md)) | verdi sì, come opzione; gialli no |
| Agente brief (Vendite) | chiede le slide allo Studio | profilo in corsia S nella milestone 2 del PRD | no: lavora su dati gialli |

Le proposte della colonna di destra sono [proposta].

### 6.3 Che cosa chiede al disegno

- **Corsia**: S, dove lavorano Agente slide e Agente grafiche ([ricerca/45 §3.2](45-architettura-v3.md); [ricerca/49 §2.6](49-instradamento-a-piu-motori.md)). Moda è uno strumento del motore, attraverso un nostro filtro sul connettore [proposta].
- **Livello nel Cancello**: produrre una tela non è un'azione verso fuori. Lo sono la condivisione con un link e la pubblicazione di un sito: per gli agenti non hanno un esecutore, e le fa una persona se servono. I file esportati escono dal Cancello al livello della loro terna: per esempio i post della pagina, L1 e poi L2 con la finestra di 24 ore ([ricerca/45 §2.6 e §4.1](45-architettura-v3.md)) [proposta].
- **Colore dei dati**: solo verde. Il giallo andrebbe solo a un fornitore del board con DPA ([ADR-0009](../docs/adr/0009-dati-tre-colori.md)): per Moda servirebbe un'eccezione di Michele, con il DPA letto e la rinuncia all'addestramento. Il rosso mai.
- **Credenziali che non vanno agli agenti**: una chiave di Moda nel gestore dei segreti, letta solo dallo strumento; un elenco degli strumenti ammessi nel nostro filtro, senza `canvas_delete`, `brand_delete`, `drive_delete`, `canvas_share` e la pubblicazione dei siti; il consumo in più spento, cioè con il tetto di spesa a zero, perché i pagamenti non sono mai automatici [proposta]. La pagina dei prezzi dice che il consumo oltre i crediti si addebita da solo e che si può fissare un tetto di spesa, non se il consumo in più si spegne o se il tetto può valere zero [non verificato]. Se non si può, lo strumento si ferma quando i crediti del piano finiscono e ogni acquisto di crediti lo approva una persona [proposta].
- **Uscita**: ogni tela finita si esporta in PDF o PNG nei nostri archivi, insieme al file modificabile quando serve, così il lavoro non resta solo da Moda [proposta].

### 6.4 Le alternative a confronto

Il ruolo confrontato: **slide e grafiche prodotte dagli agenti**. Voti da 0 a 10; totale su 100.

| Alternativa | Autonomia (35) | Tempo al valore (20) | Costi (15) | Sicurezza essenziale (10) | Server e manutenzione (10) | Rischio (10) | Totale |
|---|---|---|---|---|---|---|---|
| **A. Moda con l'omaggio** | 8: l'agente lavora sul server con una chiave; kit del marchio dal sito; tela modificabile; PDF, PPTX e PNG; ma cancellazioni e condivisione vanno filtrate da noi | 6: area di lavoro e connettore pronti; servono il filtro, la prova del PPTX con i nostri template e l'eccezione di Michele, perché è fuori dal board | 10: 0 € oggi | 4: dati negli USA con circa 30 sub-responsabili; addestramento acceso finché non si rinuncia; SOC 2 senza date; nessun permesso a parte per cancellare | 10: niente sul server | 4: prodotto uscito a marzo, CLI «prototype», server MCP già cambiato, documentazione discordante | **73,0** |
| **B. Claude Team e l'Agente slide sul motore** (consiglio della decisione 15) | 6: l'agente compone dai template SerSan; Claude Design e le skill di Claude Team servono le persone, non un agente sul server | 6: le skill ci sono; template e agente vanno fatti | 10: 0 € in più dentro Claude Team | 8: fornitore del board, termini commerciali, niente addestramento; giallo ammesso | 8: nessun servizio nuovo; template da tenere | 8: dentro il board | **72,0** |
| **C. Gamma, API e MCP** | 8: chiavi API su tutti i piani; presentazioni, documenti e post con il tema dell'azienda | 4: account nuovo, fuori dal board | 6: prezzi non verificati | 4: non verificata | 10: niente sul server | 4: non verificato | **63,0** |
| **D. Canva con il connettore** | 6: 17 strumenti; riempimento automatico dei modelli solo Enterprise, secondo una fonte di terzi | 4: fuori dal board, già tolto nel secondo giro | 6: prezzo non verificato | 4: non verificata | 10: niente sul server | 4: non verificato | **56,0** |
| **E. Figma con il server MCP** | 4: pensato per chi progetta; la scrittura chiede un posto Full | 4: fuori dal board; il posto Full va comprato | 6: 16 $ al mese il posto Full | 4: non verificata | 10: niente sul server | 4: non verificato | **49,0** |

Fonti dei voti: §6.1 per Moda; [PRESENTAZIONE-CEO.md §14](../PRESENTAZIONE-CEO.md), [docs/04-tech-stack.md](../docs/04-tech-stack.md) e [verificato: anthropic.com/news/claude-design-anthropic-labs, 14/11/2026] per B; [verificato: developers.gamma.app; claude.com/connectors/canva; docs.workato.com/en/mcp/prebuilt-mcps/canva-mcp-server.html; help.figma.com/hc/en-us/articles/32132100833559; figma.com/pricing, 14/11/2026] per C, D ed E. Le pagine dei prezzi di Canva e di Gamma hanno risposto con l'errore 403.

**Calcolo** [calcolo]: A = (8×35 + 6×20 + 10×15 + 4×10 + 10×10 + 4×10) / 10 = 73,0; B = (6×35 + 6×20 + 10×15 + 8×10 + 8×10 + 8×10) / 10 = 72,0; C = (8×35 + 4×20 + 6×15 + 4×10 + 10×10 + 4×10) / 10 = 63,0; D = (6×35 + 4×20 + 6×15 + 4×10 + 10×10 + 4×10) / 10 = 56,0; E = (4×35 + 4×20 + 6×15 + 4×10 + 10×10 + 4×10) / 10 = 49,0.

**A listino**: con un posto Pro a 26,80 € i costi scendono a 8 e il tempo a 4, perché all'eccezione si aggiunge l'acquisto: A = (8×35 + 4×20 + 8×15 + 4×10 + 10×10 + 4×10) / 10 = 66,0, sei punti sotto B, fuori dal margine [calcolo].

**Cosa ne ricavo** [non verificato: lettura nostra]. Con l'omaggio Moda è avanti di 1 punto, dentro il margine, e il vantaggio viene dall'autonomia e dall'omaggio; a listino B torna davanti di 6 punti, fuori dal margine, e Moda non conviene più. La scelta quindi si fa sulle condizioni, finché dura l'omaggio. Per i dati gialli decide la regola dei colori: Moda è fuori dal board e B no. Per i dati verdi Moda dà allo Studio un agente grafico che la strada di Claude Team non ha, con il kit del marchio pronto: lì ha senso tenerla come opzione.

### 6.5 Costi

- **Oggi**: 0 €, perché l'azienda dispone di Moda in omaggio. Piano e posti non si sanno (§8).
- **Accanto, il listino** [verificato: moda.app/pricing, 14/11/2026; euro al cambio di riferimento BCE del 23/10/2026, 1 $ = 0,8934 €, lo stesso di [ricerca/14](14-costi-abbonamenti-e-api.md), calcolo; la valuta non è scritta sulla pagina, il simbolo è il dollaro]:

| Piano | Per utente al mese | In euro | Crediti al mese per posto | Note |
|---|---|---|---|---|
| Free | 0 | 0 € | 500 | fino a 10 slide; file con il marchio moda.app; 3 lavori API |
| Pro | 30 $ | 26,80 € | 6.000, messi in comune | fino a 3 kit del marchio; senza marchio; 10 lavori API |
| Ultra | 100 $ | 89,34 € | 22.000 | kit illimitati; spazi condivisi; 15 lavori API |
| Enterprise | su misura | — | su misura | da 10 persone; SSO; SDK |

- Con il pagamento annuale si risparmia il 17%; i crediti non passano al mese dopo; sui piani a pagamento il consumo oltre i crediti si addebita da solo, a misura: «additional usage is automatically billed at a metered rate (you can set a maximum overage budget)». Se si possa spegnere, la pagina non lo dice [verificato: moda.app/pricing, 14/11/2026].
- **Se l'omaggio finisce**: il piano Free non serve per materiali da pubblicare, perché mette il marchio moda.app e si ferma a 10 slide. A listino Moda non conviene (§6.4): lo Studio torna alla strada di Claude Team con i template SerSan, che resta comunque quella dei dati gialli. Il listino, 26,80 € al mese per posto Pro, resta scritto accanto per chi volesse pagarlo lo stesso. Le esportazioni nei nostri archivi evitano di perdere il lavoro [proposta].

### 6.6 Rischi

| Rischio | Cosa vuol dire | Come si contiene |
|---|---|---|
| Cancellazioni e condivisione | il connettore cancella tele, kit e file, condivide con un link e pubblica siti; la chiave non le esclude | filtro nostro con l'elenco degli strumenti ammessi; condivisione e siti solo a una persona |
| Addestramento sui contenuti | acceso di serie | rinuncia per mail prima del primo uso; solo dati verdi |
| Prodotto giovane | CLI «prototype», server MCP cambiato in pochi mesi, documentazione discordante | versione della CLI fissata; esportazioni nei nostri archivi; la strada di Claude Team resta pronta |
| Fedeltà del PowerPoint | caratteri ed effetti possono cambiare | prova con i template SerSan; PDF per i materiali finali |
| Fine dell'omaggio | il Free mette il marchio e limita le slide; a listino Moda non conviene | ritorno alla strada di Claude Team (§6.4 e §6.5) |
| Termini | cambiano alla pubblicazione; responsabilità fino a 1.000 dollari | rilettura dei termini a ogni rinnovo; nessun dato che non sia verde |

### 6.7 Giudizio

**Entra come opzione, con queste condizioni** [proposta]:
1. Solo grafiche e presentazioni con dati verdi: caroselli, copertine, post e presentazioni pubbliche.
2. Le slide con dati gialli (brief prima dell'incontro, recap e proposte ai clienti) restano sulla strada della decisione 15: Claude Team per le persone e l'Agente slide sul motore con i template SerSan. Moda le riceve solo se Michele ammette un'eccezione, con il DPA letto e la rinuncia all'addestramento fatta.
3. Chiave nel gestore dei segreti, letta solo dallo strumento; filtro senza cancellazioni, senza condivisione con link e senza pubblicazione di siti.
4. Consumo in più spento, con il tetto di spesa a zero. Se Moda non lo permette [non verificato: §6.3], lo strumento si ferma quando i crediti del piano finiscono e ogni acquisto di crediti lo approva una persona.
5. Rinuncia all'addestramento chiesta per mail prima del primo uso.
6. Niente video e niente founder, come chiedono le direttive dei contenuti; il video resta a Higgsfield, HyperFrames e After Effects.
7. Ogni tela finita si esporta nei nostri archivi.
8. È un'eccezione al board, da approvare con Michele ([ADR-0002](../docs/adr/0002-self-hosted-board-michele.md)), e ha un responsabile.
9. Vale finché dura l'omaggio: a listino Moda sta 6 punti sotto la strada di Claude Team (§6.4), e lo Studio torna a quella.

---

## 7. Dove toccherebbe i documenti

Sono proposte: nessuna ADR è stata modificata. Ogni revisione va datata il giorno in cui il gruppo di progetto la accetta; qui porta la data del 14 novembre 2026.

### 7.1 ADR-0011, n8n per orari e integrazioni

Testo proposto, in fondo all'ADR:

> ## Revisione del 14 novembre 2026
>
> - La CVE-2026-21858 ora è verificata: CVSS 10, del 7 gennaio 2026, versioni da 1.65.0 a 1.120.x. La 2.x non è colpita (ricerca/52 §1.4).
> - Gli avvisi continuano: 24 critici fra dicembre 2025 e maggio 2026, altri alti fino al 13 novembre 2026. La patch entro 14 giorni resta, con un controllo settimanale degli avvisi (ricerca/52 §3.1).
> - La versione 2.x fissata è la 2.47.7 al 14 novembre 2026. La 3.0 stabile è annunciata per inizio dicembre; da allora la 2.x riceve correzioni di sicurezza per 12 mesi. Il passaggio alla 3.0 è una scelta a parte (ricerca/52 §4).
> - L'azienda dispone di n8n Community Edition; Michele la installa sul server il 15 novembre 2026. Nella Community mancano oscuramento dei dati delle esecuzioni, registri di controllo, segreti esterni, SSO e condivisione: per questo la regola «nessun dato rosso nelle esecuzioni» resta, e le credenziali di n8n le tiene una persona (ricerca/52 §3.1 e §4).

### 7.2 ADR-0022, eventi e sveglia nel motore

> ## Revisione del 14 novembre 2026
>
> - n8n resta facoltativo. Quando c'è, serve a tre cose: le pipeline del board, come i bandi della notte; le automazioni interne consigliate dal Mappatore processi, scelte da una persona e costruite da una persona; gli avvisi a senso unico dei suoi flussi. Chiama `POST /eventi` con il suo token, oppure scrive solo su sistemi interni con credenziali ristrette (ricerca/52 §3.7).
> - La pagina delle modifiche incompatibili della 3.0 non elenca cambi dell'API pubblica; cambiano installazione (solo Docker), nodi tolti e impostazioni di sicurezza (ricerca/52 §1.4).
> - Non serve alla sveglia, agli ingressi dall'esterno (il modulo del sito e Instantly chiamano direttamente `POST /eventi`), alle approvazioni, agli invii verso clienti e prospect. Per i dati rossi porta al massimo l'avviso che un dato è pronto, mai il dato.
> - Gli agenti non usano n8n: nessuna chiave della sua API e nessun accesso al server MCP dell'istanza, che può creare e modificare flussi.
> - Ogni flusso attivo ha una riga nel registro dei collegamenti, in git, con responsabile, innesco, colore dei dati e credenziali.
> - I flussi con dati gialli non salvano le esecuzioni.
> - Lo stop di emergenza vale anche per n8n: il motore rifiuta gli eventi con il suo token, e chi preme lo stop ferma il servizio con un comando sul server (ricerca/52 §3.7).

### 7.3 ADR-0008, Andrea

> ## Revisione del 14 novembre 2026
>
> - L'azienda dispone di ElevenLabs senza costi, perché l'ha ricevuto in omaggio. La scelta non cambia: la voce di chi chiama è un dato rosso e resta in casa; gli agenti vocali di ElevenLabs e Reception la porterebbero negli USA (ricerca/52 §5.4.2).
> - L'ultima riserva si precisa: se la voce italiana in casa non passa la prova d'ascolto, Andrea può usare la sola sintesi vocale di ElevenLabs per le sue risposte, con ascolto, trascrizione e registrazione sempre in casa. Al fornitore va solo il testo delle risposte, che può contenere dati rossi perché può ripetere ciò che dice chi chiama: prima della sintesi esterna un filtro locale ferma o oscura il rosso, come fa ADR-0009 per l'API, oppure le risposte si prendono da un elenco chiuso di frasi. Servono anche l'eccezione di Michele (ADR-0002) e una chiave di account di servizio come per i contenuti (ricerca/52 §5.7). Il colore del testo delle risposte lo dice il parere legale.
> - La voce clonata di un collega resta solo in casa finché il parere non decide (ricerca/52 §7.4). Su ElevenLabs la clonazione professionale la può fare solo la persona stessa.

### 7.4 ADR-0009, dati a tre colori

> ## Revisione del 14 novembre 2026
>
> - La riga rossa dice «audio» senza distinguere. Si precisa:
>   - l'audio delle call, dei lead e di chi chiama Andrea resta rosso;
>   - lo script di un contenuto pubblico approvato e la sua voce sintetica, se non è clonata da una persona, sono verdi;
>   - le registrazioni della voce di una persona fatte per clonarla, e la voce clonata, restano nella riga rossa «audio» finché parere legale e valutazione d'impatto non decidono diversamente, con la stessa prudenza che vale per Claude Team. Fino ad allora non si caricano su ElevenLabs e gli agenti non le usano; i cloni già fatti restano fermi (ricerca/52 §8, domanda 9). Se il parere lo ammette, le gestisce solo la persona dal suo account, con il suo consenso scritto, e la lettura di uno script approvato con la voce già creata da un founder può entrare nell'Agente video, con l'eccezione di Michele.
> - ElevenLabs e Moda non sono fornitori del board: ricevono solo verde, salvo un'eccezione di Michele con il DPA letto e la rinuncia all'addestramento fatta (ricerca/52 §5.3 e §6.3).

### 7.5 ADR-0002, tutto self-hosted dentro il board

> ## Revisione del 14 novembre 2026
>
> - Fra le eccezioni entrano, come opzione, due strumenti che l'azienda ha già in omaggio: ElevenLabs per voce, musica ed effetti dei contenuti pubblici, e Moda per le grafiche con dati verdi, finché dura l'omaggio (ricerca/52 §5.7 e §6.7).
> - Ogni eccezione ha: solo dati verdi, salvo l'eccezione sul colore di ADR-0009; una chiave letta solo dallo strumento del motore, limitata dove il fornitore lo permette (ElevenLabs) e dietro un nostro filtro dove no (Moda); ricarica automatica spenta; consumo in più spento o, se non si può, fermato dallo strumento a crediti finiti; rinuncia all'addestramento; ogni file salvato nei nostri archivi; un responsabile; il costo a listino scritto accanto per quando l'omaggio finisce (ElevenLabs almeno 267,13 € al mese con Scale, il primo piano a più posti che la chiave di account di servizio richiede, o quanto si accorda con le vendite; per la musica Scale vale sotto i 10 dipendenti, e fra 10 e 49 serve Business, 884,47 € al mese; Moda 26,80 € al mese per posto, ma a listino non conviene e lo Studio torna alla strada di Claude Team).
> - n8n Community Edition sta nel board e gira sul server: non è un'eccezione.

### 7.6 Altri documenti

- [docs/02-alternative.md](../docs/02-alternative.md): una sottosezione 10.5 sui tre strumenti, come le altre valutazioni dopo il terzo giro.
- [docs/04-tech-stack.md](../docs/04-tech-stack.md), riga della tabella su slide e documenti e nota sugli strumenti che escono: oggi danno la decisione 15 per presa. Andrebbe scritto: slide con dati gialli su Claude Team; Moda come opzione per le grafiche con dati verdi, finché dura l'omaggio. Nello stesso file, alle righe 192 e 340, la frase sulla 3.0 che cambia l'API va corretta come in ADR-0022 (§7.2).
- [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md), domanda 33: andrebbe aggiornata con l'installazione del 15 novembre e le domande del §8.
- Nella repo del codice, la direttiva D26: la frase «Moda no: entra nella valutazione per la prima volta» si corregge insieme a questo rapporto (§1.3).

---

## 8. Domande aperte per le persone

**Per tutti e tre** (Alberto):
1. Quanto dura l'omaggio di ciascuno, da quando conta e quale piano copre?
2. Chi tiene le credenziali di ciascun account, come proprietario e come amministratore? La proposta è una persona per strumento, con la 2FA, e nessun agente.
3. Quando l'omaggio di ElevenLabs finisce, si paga il listino o si passa all'alternativa? Per Moda il rapporto consiglia il ritorno alla strada di Claude Team (§6.4): si conferma? Lo decide il gruppo di progetto con Michele.

**n8n** (Michele):
4. Oltre alla Community Edition c'è una licenza o un piano registrato: Business, Enterprise, oppure la chiave gratuita della Community registrata? Alberto ha parlato di «abbonamento».
5. Su quale macchina e in quale rete gira (il board lo mette nella VLAN 30 APPS), chi è il proprietario dell'istanza, dove sta la chiave di cifratura e su quale PostgreSQL gira: il 16 del board, che per n8n è solo di compatibilità, o un 17 o 18 dedicato (§4, punto 8)?
6. Con quali flussi parte: i bandi della notte? Altri? È la domanda 33 di [DOMANDE-PER-MICHELE.md](../DOMANDE-PER-MICHELE.md), che oggi sembra avere risposta «sì».

**ElevenLabs** (Alberto):
7. Quale piano copre l'omaggio, quanti posti Full, quante voci professionali, quale licenza per la musica? Copre anche l'API e i minuti degli agenti, o solo ElevenCreative? Una dotazione da 33 milioni di caratteri vale 12 mesi (§5.5): l'omaggio è quella, e da quale data contano i 12 mesi? L'omaggio è un'area di lavoro a più posti, con gli account di servizio (§5.1)? Quanti dipendenti conta l'azienda per i termini della musica (§5.5)?
8. Chi amministra l'area di lavoro, e la rinuncia all'addestramento è impostata? Va impostata subito, perché sull'account ci sono già due cloni (§1.4).
9. Le voci dei founder: chi le registra, con quale consenso, e che cosa si fa dei cloni fatti finora con audio compresso ([ricerca/05 §3.4](05-marketing-e-post.md))? La proposta è che fino al parere restino fermi (§7.4): lo decidono i founder.

**Moda** (Alberto):
10. Quale piano e quanti posti; l'area di lavoro «sersan.dev» è quella dell'omaggio, e chi ne è proprietario?
11. La rinuncia all'addestramento è già stata chiesta per mail?
12. Le persone useranno Moda anche da Claude? Allora il proprietario dell'organizzazione Claude Team deve approvare il connettore.
13. Nel piano dell'omaggio il consumo oltre i crediti si addebita da solo? Si può spegnere, o portare il tetto di spesa a zero, e chi lo imposta (§6.3)?

**Decisioni**:
14. La decisione 15 va registrata come presa, con la precisazione di questo rapporto? Gruppo di progetto con Michele.
15. La riga AI: le direttive dei contenuti vietano le etichette, il Cancello mette la riga AI su ciò che esce a L2 o L3, la trasparenza vale dal 2 agosto 2026. Decide Alberto, con il parere.
16. Il colore della voce dei founder e dei cloni (§7.4) e quello del testo delle risposte di Andrea (§7.3): parere legale.
17. Le due eccezioni al board, ElevenLabs e Moda sui dati verdi, si approvano? Gruppo di progetto con Michele ([ADR-0002](../docs/adr/0002-self-hosted-board-michele.md)).

---

## 9. I buchi

Quello che le fonti non dicono, o dicono in modo diverso:
- **L'omaggio**: piano, durata e posti dei tre strumenti non sono confermati. Per ElevenLabs la repo riporta, da fonti di terzi, 33 milioni di caratteri per 12 mesi, con piano, voci professionali e licenza della musica «da leggere» ([ricerca/14](14-costi-abbonamenti-e-api.md)); la pagina dei prezzi conferma che una dotazione da 33 milioni di caratteri vale 12 mesi [verificato: elevenlabs.io/pricing, 14/11/2026], ma se l'omaggio sia quella, e da quando contino i 12 mesi, non si sa. Per Moda la repo dice che l'offerta è «da verificare» ([ricerca/05 §4.5](05-marketing-e-post.md)); di n8n non dice nulla.
- **n8n, modalità a code**: la pagina dei prezzi la mette fra le voci di Business, la pagina della Community la dà inclusa.
- **n8n, più istanze principali**: la pagina dei prezzi dice «Coming soon», la documentazione la dà già in Enterprise.
- **n8n, memoria**: nessun minimo ufficiale per il solo n8n; ci sono i 4 GB e 2 vCPU della guida Docker Compose con i servizi di n8n Assistant e l'esempio della pagina OEM.
- **n8n, approvazioni**: le pagine non dicono se le risposte da Teams e Outlook registrano chi ha approvato.
- **n8n, server MCP e agenti in anteprima**: le pagine dicono «all self-hosted plans» e non nominano la Community.
- **ElevenLabs, un abbonamento o tre**: la pagina dei prezzi parla di un unico monte crediti, quella dell'API dice che si paga in dollari e non in crediti.
- **ElevenLabs, server MCP senza persona**: la pagina documenta solo l'accesso OAuth di una persona, senza chiavi API nel client; un altro accesso non è nominato.
- **ElevenLabs, italiano**: nessuna misura indipendente; c'è solo la tabella di un concorrente, su un modello ElevenLabs non specificato.
- **ElevenLabs, file fatti durante l'omaggio**: per la musica la regola c'è, perché resta il piano con cui è stata creata (§1.5 dei termini della musica); per voce ed effetti, se restino usabili a fini commerciali dopo un ritorno al Free, i termini letti non lo dicono.
- **Moda, SSO**: Ultra per la pagina della sicurezza, Enterprise per quella dei prezzi.
- **Moda, cancellazioni**: se una tela cancellata si recupera, e per quanto; se il connettore chiede conferma.
- **Moda, chiavi con permessi limitati**: la pagina dell'autenticazione dice che una chiave creata dalle impostazioni riceve tutti i permessi tranne admin, senza poterli scegliere; la guida della CLI chiede invece, per i lavori automatici, una «scoped key» presa dalle impostazioni. Pesa sulla condizione 3 del §6.7 [verificato: docs.moda.app/api-reference/authentication; docs.moda.app/agents/cli-quickstart.md, 14/11/2026].
- **Moda, SOC 2**: solo i bollini, senza rapporto né date; cifratura a riposo non dichiarata.
- **Moda, italiano sulla tela**: caratteri e sillabazione non documentati.
- **Alternative**: prezzi di Canva e Gamma (errore 403); sicurezza di Activepieces, Windmill e Node-RED non letta; strumenti vocali di Higgsfield non verificati.

---

## Fonti

**Pagine ufficiali di n8n, lette il 14/11/2026**
- Edizioni, prezzi, licenza: https://docs.n8n.io/deploy/host-n8n/community-edition-features.md · https://n8n.io/pricing/ · https://n8n.io/pricing/?selfHosted=true · https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md · https://docs.n8n.io/n8n-community-license/community-license/license-faq.md
- Versioni: https://docs.n8n.io/changelog/readme.md · https://hub.docker.com/v2/repositories/n8nio/n8n/tags/2.47.7 · https://blog.n8n.io/introducing-n8n-v3 · https://docs.n8n.io/changelog/v30-breaking-changes.md · https://docs.n8n.io/changelog/v20-breaking-changes.md
- Installazione e sicurezza: https://docs.n8n.io/deploy/host-n8n/install-options/production-requirements.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/choose-n8ns-database.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/disable-the-public-api.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/enable-ssrf-protection.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/block-specific-nodes.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/nodes.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/ssrf-protection.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/timezone-and-localization.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/redact-execution-data.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/manage-security-policies.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/user-management-and-2fa.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/manage-execution-data.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/fix-memory-issues.md · https://docs.n8n.io/deploy/host-n8n/deploy-as-an-oem-integration/prerequisites.md · https://docs.n8n.io/administer/manage-users-and-access/understand-instance-roles.md · https://docs.n8n.io/administer/manage-users-and-access/set-permissions-and-roles-rbac/create-custom-roles/create-custom-instance-roles.md · https://docs.n8n.io/deploy/host-n8n/install-options.md · https://docs.n8n.io/deploy/host-n8n/install-options/one-line-setup.md · https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose.md · https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/task-runners.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/configure-webhook-urls-with-reverse-proxy.md · https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/control-telemetry.md · https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/backup-and-restore.md
- Nodi e agenti: https://n8n.io/integrations/ · https://n8n.io/integrations/elevenlabs/ · https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.microsoftteams.md · https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.microsoftoutlook.md · https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.hubspot.md · https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.linkedin.md · https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook.md · https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger.md · https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait.md · https://docs.n8n.io/connect/connect-to-n8n-mcp-server.md · https://docs.n8n.io/build/build-and-manage-agents.md · https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md · https://docs.n8n.io/api/
- Avvisi: https://blog.n8n.io/security-advisory-20260108

**GitHub, letto il 14/11/2026**
- https://api.github.com/repos/n8n-io/n8n/releases · https://api.github.com/repos/n8n-io/n8n/security-advisories · https://github.com/n8n-io/n8n/security/advisories?state=published · https://github.com/n8n-io/n8n/security/advisories/GHSA-9p7v-45m2-wxgj · https://github.com/n8n-io/n8n/security/advisories/GHSA-f2cw-9483-7vcp · https://github.com/n8n-io/n8n/security/advisories/GHSA-q8rc-7m84-mfvj · https://github.com/n8n-io/n8n/security/advisories/GHSA-h59h-rf6m-7jp5 · https://api.github.com/advisories?affects=n8n&ecosystem=npm&severity=critical&per_page=100 · https://api.github.com/advisories?affects=n8n&ecosystem=npm&severity=high&per_page=100 · https://raw.githubusercontent.com/n8n-io/n8n/n8n%402.47.7/packages/@n8n/config/src/configs/nodes.config.ts · https://raw.githubusercontent.com/n8n-io/n8n/n8n%402.47.7/packages/@n8n/config/src/decorators.ts · https://raw.githubusercontent.com/n8n-io/n8n/master/docker/get-n8n-compose.yml
- https://github.com/elevenlabs/elevenlabs-mcp · https://github.com/elevenlabs/elevenlabs-n8n · https://api.github.com/repos/moda-design/moda

**Pagine ufficiali di ElevenLabs, lette il 14/11/2026**
- Prezzi e termini: https://elevenlabs.io/pricing · https://elevenlabs.io/pricing/api · https://elevenlabs.io/pricing/agents · https://elevenlabs.io/terms-of-use · https://elevenlabs.io/music · https://elevenlabs.io/music-terms · https://elevenlabs.io/docs/overview/administration/pay-as-you-go · https://elevenlabs.io/blog/weve-lowered-api-agents-pricing-and-introduced-pay-as-you-go · https://elevenlabs.io/docs/reception-ai/billing/plans-and-pricing
- Modelli e prodotti: https://elevenlabs.io/docs/overview/models · https://elevenlabs.io/blog/eleven-v4 · https://elevenlabs.io/blog/scribe-v3 · https://elevenlabs.io/docs/overview/capabilities/image-video · https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning · https://elevenlabs.io/blog/reception · https://elevenlabs.io/docs/reception-ai/phone-numbers/international-numbers · https://elevenlabs.io/docs/changelog/2026/5/25
- Agenti e telefono: https://elevenlabs.io/docs/eleven-agents/overview · https://elevenlabs.io/docs/eleven-agents/customization/llm · https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking · https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/transfer-to-human · https://elevenlabs.io/docs/eleven-agents/operate/hosted-mcp · https://elevenlabs.io/docs/eleven-agents/workflows/post-call-webhooks · https://elevenlabs.io/docs/overview/administration/workspaces/api-keys · https://elevenlabs.io/docs/overview/administration/workspaces/service-accounts · https://elevenlabs.io/docs/help-center/technical/api-error-code-429
- Dati e conformità: https://elevenlabs.io/docs/overview/administration/data-residency · https://elevenlabs.io/docs/eleven-api/resources/zero-retention-mode · https://elevenlabs.io/docs/eleven-agents/customization/privacy/retention · https://elevenlabs.io/dpa · https://elevenlabs.io/privacy-policy · https://elevenlabs.io/use-policy · https://elevenlabs.io/safety · https://elevenlabs.io/blog/certification-renewals
- SDK: https://pypi.org/project/elevenlabs/

**Pagine ufficiali di Moda, lette il 14/11/2026**
- https://moda.app/ · https://moda.app/llms.txt · https://moda.app/pricing · https://moda.app/terms · https://moda.app/dpa · https://moda.app/privacy · https://moda.app/mcp · https://moda.app/blog/moda-vs-claude-design · https://trust.moda.app/
- https://docs.moda.app/agents.md · https://docs.moda.app/agents/mcp-connector.md · https://docs.moda.app/agents/cli-quickstart.md · https://docs.moda.app/mcp/overview · https://docs.moda.app/mcp/tools · https://docs.moda.app/api-reference/authentication · https://docs.moda.app/api-reference/usage-limits · https://docs.moda.app/help/faq.md · https://docs.moda.app/help/trust-security · https://docs.moda.app/help/export/formats.md · https://docs.moda.app/help/export/troubleshooting.md · https://docs.moda.app/help/getting-started/importing-files
- https://claude.com/connectors/moda · https://registry.npmjs.org/@moda-design/moda
- Comunicato del lancio: https://markets.financialcontent.com/pennwell.cabling/article/gnwcq-2026-3-24-moda-raises-75m-to-give-every-professional-a-design-agent

**Alternative, lette il 14/11/2026**
- Automazioni: https://github.com/activepieces/activepieces · https://www.activepieces.com/docs/about/license · https://github.com/windmill-labs/windmill · https://www.windmill.dev/pricing · https://www.windmill.dev/docs/flows/flow_approval · https://github.com/node-red/node-red · https://nodered.org/about/ · https://github.com/temporalio/temporal
- Voce: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base · https://huggingface.co/ResembleAI/chatterbox · https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md · https://huggingface.co/coqui/XTTS-v2 · https://github.com/pipecat-ai/pipecat · https://github.com/OHF-Voice/piper1-gpl · https://aws.amazon.com/polly/pricing/ · https://developers.openai.com/api/docs/pricing · https://developers.openai.com/api/docs/guides/realtime-sip · https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live · https://cloud.google.com/text-to-speech/pricing (non leggibile)
- Grafica: https://claude.com/connectors/canva · https://docs.workato.com/en/mcp/prebuilt-mcps/canva-mcp-server.html · https://help.figma.com/hc/en-us/articles/32132100833559 · https://www.figma.com/pricing/ · https://developers.gamma.app/ · https://developers.gamma.app/llms.txt · https://www.anthropic.com/news/claude-design-anthropic-labs

**NetBird, letta il 14/11/2026**
- https://docs.netbird.io/manage/settings/networks

**Commissione europea, letta il 14/11/2026**
- https://digital-strategy.ec.europa.eu/en/news/strong-backing-code-practice-transparency-AI-generated-content

**Documenti della repo**
- [ricerca/05, marketing e post, §2.9, §3.4, §4.5 e §5.6](05-marketing-e-post.md)
- [ricerca/12, altre piattaforme](12-altre-piattaforme.md) · [ricerca/14, costi, §2 e §6](14-costi-abbonamenti-e-api.md) · [ricerca/16, GDPR e AI Act, §5](16-gdpr-ai-act-e-regole.md) · [ricerca/18, agenti in abbonamento](18-agenti-in-abbonamento.md)
- [ricerca/20, proposta G](20-proposta-G-ibrido.md) · [ricerca/22, architettura del primo giro](22-architettura-scelta.md) · [ricerca/23, critica di completezza](23-critica-completezza.md) · [ricerca/25, il board di Michele](25-board-michele-e-delta.md)
- [ricerca/31, la voce di Andrea in casa](31-voce-andrea-self-hosted.md) · [ricerca/33, costi v2](33-costi-v2.md) · [ricerca/36, architettura v2, §8.2](36-architettura-v2.md)
- [ricerca/41, novità al 9 novembre, §5](41-novita-al-9-novembre.md) · [ricerca/42, proposta D, §4.4](42-proposta-D-automazione-prima.md) · [ricerca/43, i quattro giudizi](43-giudizio-ceo.md) · [ricerca/44, verifiche avversarie](44-verifiche-avversarie.md) · [ricerca/45, architettura v3, §2, §2.6, §3.2, §4.1 e §6.3](45-architettura-v3.md) · [ricerca/46, §5](46-obsidian-come-casa-dei-testi.md) · [ricerca/48, §6.2](48-modelli-locali-e-gpu.md) · [ricerca/49, §2.6 e §3](49-instradamento-a-piu-motori.md)
- [PRESENTAZIONE-CEO.md, §4.5, §4.8, §14 e appendice A](../PRESENTAZIONE-CEO.md) · [DOMANDE-PER-MICHELE.md, n. 33](../DOMANDE-PER-MICHELE.md) · [docs/02-alternative.md](../docs/02-alternative.md) · [docs/04-tech-stack.md](../docs/04-tech-stack.md) · [docs/06-sviluppo.md](../docs/06-sviluppo.md)
- [Board di Michele](../allegati/infra/SerSan%20Infra%20Board.md) · [Direttive dei contenuti](../allegati/marketing/DIRETTIVE_CONTENUTI.md)
- [ADR-0002](../docs/adr/0002-self-hosted-board-michele.md) · [ADR-0007](../docs/adr/0007-call-e-trascrizione.md) · [ADR-0008](../docs/adr/0008-andrea-centralino.md) · [ADR-0009](../docs/adr/0009-dati-tre-colori.md) · [ADR-0011](../docs/adr/0011-n8n-orari-integrazioni.md) · [ADR-0013](../docs/adr/0013-postiz-listmonk-docuseal.md) · [ADR-0014](../docs/adr/0014-seconda-gpu-blackwell.md) · [ADR-0016](../docs/adr/0016-backup-3-2-1.md) · [ADR-0020](../docs/adr/0020-autonomia-a-livelli.md) · [ADR-0021](../docs/adr/0021-motore-a-due-corsie.md) · [ADR-0022](../docs/adr/0022-eventi-e-sveglia-nel-motore.md) · [ADR-0024](../docs/adr/0024-abbonamenti-come-riserva.md) · [ADR-0025](../docs/adr/0025-un-modello-per-agente.md)

**La repo del codice**, letta il 14/11/2026: il PRD («Perimetro», «Milestone di consegna»); le direttive (D26); l'elenco delle attività; la cartella degli agenti e i file di configurazione delle squadre, degli orari e dei livelli; le righe degli spec della milestone 1 che nominano n8n.
