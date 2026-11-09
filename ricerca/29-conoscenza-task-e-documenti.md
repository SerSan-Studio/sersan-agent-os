# 29 · Conoscenza, task e documenti senza Notion

**Data:** 25/10/2026. **Per:** Michele Sanna e Alessandro Serratt, preparato per Alberto Tuveri.
**Vincolo:** il board dell'infrastruttura di Michele è vincolante (`allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`). Notion e Slack non sono nella lista dei servizi cloud che restano. Michele ha scritto ad Alberto: «Tutto il resto dev'essere self hosted».
**Letti:** 00, 22, PRESENTAZIONE-CEO.md (sezioni 4, 5, 12, 14, appendice A), 01, il board completo. Ricerca web e documentazione ufficiale del 25/10/2026.
**Etichette:** [verificato: fonte] = fatto letto nella fonte indicata il 25/10/2026; [non verificato] = stima, proposta mia o voce di terzi. Prezzi IVA esclusa, cambio 1 $ = 0,8934 € [verificato: 22, intestazione]. gp = giorni-persona.

---

## In breve

Notion e Slack escono dal progetto. Al loro posto non mettiamo un solo strumento, ma quattro case che il board prevede già, ognuna con un compito preciso. **BookStack**, sul server, tiene i testi che le persone scrivono e leggono: le regole di lavoro di ciascuno, i processi, il catalogo, il manuale degli agenti. **PostgreSQL 16**, sul server, tiene i dati con numeri e campi fissi: il registro e l'organigramma degli agenti, gli obiettivi, i prezzi del catalogo, il registro dei meeting. **Jira**, in cloud, tiene to-do e progetti. **Microsoft 365** tiene documenti, posta, calendario e chat: SharePoint, OneDrive, Outlook e Teams. Sopra le quattro case c'è una sola porta di ricerca, **MCP RAG**: indicizza in Qdrant ciò che serve e risponde sia a Claude Team sia agli agenti sul server, con i permessi di chi chiede. **Teams** prende il posto di Slack come chat di persone e agenti. **mcp-memory** resta un taccuino per i singoli agenti, non la memoria aziendale. **Sirius** compare solo nel board: nessun file del progetto lo descrive e la ricerca web non trova un gestionale italiano con quel nome. Dal board sappiamo che contiene dati fiscali, clienti e documenti, esportati in modo incrementale verso la pipeline di ricerca. Va chiesto a Michele che cosa sia. BookStack è adatto agli agenti per leggere e scrivere testi (API completa, permessi per ruolo e per libro, accesso con Entra), ma non sostituisce le tabelle vive di Notion: quelle vanno in Postgres e si guardano in Grafana. Il costo mensile scende di circa 107 € (Notion Plus, Slack Pro e Claude in Slack); entra Jira, gratis fino a 10 utenti se il piano Free basta.

Le cinque cose da decidere:
1. BookStack per i testi, Postgres per i dati, Jira per i task, SharePoint per i documenti: una cosa, un posto.
2. Teams come chat di persone e agenti, con un bot per le carte di approvazione.
3. Una sola pipeline di indicizzazione, quella del board, estesa da Sirius alle altre fonti.
4. Che cosa fa Claude Team con i dati rossi che MCP RAG gli restituisce (§8.5).
5. Jira Free o Standard (§4.3).

---

## 1. Cosa cambia rispetto alla proposta

| Funzione | Prima (22 e presentazione) | Ora | Fonte del cambio |
|---|---|---|---|
| Memoria relazionale | Notion Plus via MCP | BookStack per i testi, PostgreSQL 16 per i dati | Notion non è nel board; BookStack e PostgreSQL 16 sì [verificato: board-vlan.txt, VLAN 30 e 40] |
| Memoria vettoriale | Postgres 17 con pgvector | Qdrant con BM25, embedding e reranker Qwen3 0.6B, MCP RAG | [verificato: SerSan Infra Board.md, «Pipeline AI»] |
| To-do e progetti | Notion | Jira in cloud | [verificato: SerSan Infra Board.md, «Cloud & SaaS che restano»] |
| Documenti | suite da confermare (Google o Microsoft) | SharePoint e OneDrive | [verificato: board, «M365 / Entra ID»; PRESENTAZIONE-CEO.md §14, verifiche della prima settimana] |
| Posta e calendario | esecutore Gmail | Outlook e calendario di Exchange via Microsoft Graph | [verificato: board, «identità, MFA, posta»] |
| Chat | Slack Pro, Claude in Slack, `#approvazioni`, `#agenti` | Teams | Slack non è nel board; Teams sì [verificato: board-testo-completo.txt, «Cloud»] |
| Banca dei token | porta dei modelli nel Cancello | LiteLLM con budget, più i tetti del Cancello | [verificato: board, «API Anthropic · crediti · dietro LiteLLM»] |
| Organigramma | registro del Cancello esportato in Notion | registro in Postgres, vista in Grafana, pagina BookStack rigenerata | proposta mia [non verificato] |
| Accesso da fuori | Cloudflare Tunnel | NetBird (SSO Entra e FIDO2) e Pangolin con Traefik | [verificato: board, «Accesso»] |

Il Cancello resta com'era: gli agenti preparano, una persona approva, un nostro programma esegue [verificato: 22 §1]. Cambiano solo i suoi esecutori: prima Gmail, Slack e Notion; ora Outlook e calendario via Graph, Teams, Jira, BookStack e SharePoint.

---

## 2. Una cosa, un posto: la mappa della conoscenza

Regola di base: ogni informazione ha **una sola fonte di verità**. Qdrant è una copia indicizzata e si ricostruisce dalle fonti. Il colore è quello della regola dei tre colori [verificato: PRESENTAZIONE-CEO.md §5.6].

| Informazione | Fonte di verità | Chi scrive | Come la leggono gli agenti | Come la vedono le persone | Colore |
|---|---|---|---|---|---|
| Regole di lavoro di ciascuno (C6) | BookStack, libro «Come lavoriamo», una pagina per persona con un modello fisso | la persona | MCP BookStack in lettura, prima di ogni lavoro | BookStack | giallo |
| Processi (F3) | BookStack, libro «Processi»; ore e costi per processo in Postgres | Mappatore processi propone, Michele approva | MCP BookStack e MCP memoria | BookStack, Grafana | giallo |
| Obiettivi (A2, K14) | Postgres, tabella `obiettivi` (valore, scadenza, responsabile); il perché in una pagina BookStack | i CEO | MCP memoria | Grafana | rosso se finanziari |
| Catalogo servizi (D5) | BookStack, libro «Catalogo», per i testi; Postgres per codice, prezzo base e giorni tipici | Michele | MCP BookStack e MCP memoria | BookStack | giallo |
| Registro e organigramma degli agenti (G9) | Postgres, tabella del Cancello; costi da LiteLLM | il Cancello, dopo l'approvazione di un nuovo agente | MCP memoria | Grafana; pagina BookStack rigenerata ogni notte | verde |
| Skill degli agenti (A6) | repo GitHub delle skill, con revisione; copia leggibile in BookStack | l'agente propone, una persona approva la modifica | file del repo | BookStack | verde |
| To-do e progetti (B4, J8) | Jira | persone e agenti (account di servizio) | API di Jira, n8n | Jira, web e app | giallo |
| Registro dei meeting (C5) | Postgres, tabella `meetings` | agente post-call | MCP memoria | Grafana | giallo |
| Documenti di lavoro e dei clienti | SharePoint (un sito per cliente) e OneDrive | persone; agenti solo dopo una carta | Graph con permesso sui soli siti scelti; testo indicizzato in Qdrant | SharePoint, Teams | rosso |
| Posta e calendario | Exchange Online | persone; agenti tramite gli esecutori | Graph su caselle limitate | Outlook | rosso |
| Chat persone-agenti | Teams | tutti | bot del sistema | Teams | giallo |
| Conoscenza ricercabile (A3) | Qdrant, copia delle fonti | pipeline | MCP RAG | Claude Team via MCP RAG | come la fonte |
| Appunti di lavoro di un agente | mcp-memory | l'agente | mcp-memory | nessuna vista | verde |
| Dati fiscali, clienti e documenti di Sirius | Sirius | da chiarire | MCP RAG per i testi; Postgres per i numeri (da prevedere) | da chiarire | rosso |

Tutte le righe sono una proposta mia [non verificato], costruita sui componenti del board.

---

## 3. BookStack: è adatto agli agenti?

### 3.1 Fatti

- **Licenza e costo.** MIT, gratuito, sorgente su Codeberg [verificato: https://www.bookstackapp.com/].
- **Versione.** L'ultima è la v26.09 del 24/09/2026. Porta le preferenze di layout per utente, la ricerca dentro un libro o un capitolo via API e il parametro `changelog` sulle pagine create o modificate via API. Ora richiede un `APP_KEY` esplicito [verificato: https://www.bookstackapp.com/blog/bookstack-release-v26-09/].
- **API.** Token nell'intestazione `Authorization: Token <id>:<segreto>`. L'utente deve avere il permesso «Access System API». Limite predefinito di 180 richieste al minuto per utente, modificabile. Gruppi di endpoint: pagine, capitoli, libri, scaffali, allegati, registro di audit, commenti, permessi sui contenuti, immagini, import, cestino, ruoli, ricerca, tag, utenti. Le pagine si creano anche in Markdown [verificato: https://demo.bookstackapp.com/api/docs].
- **Permessi.** Un utente può avere più ruoli, e i permessi si sommano. Ogni scaffale, libro, capitolo o pagina può sovrascrivere i permessi per ruolo. Libri e capitoli passano le regole ai figli. Vale la regola più specifica; a parità, vince il permesso concesso [verificato: https://www.bookstackapp.com/docs/user/roles-and-permissions/].
- **Accesso con Entra.** BookStack supporta OIDC, SAML2 e LDAP, e la MFA per ruolo [verificato: https://www.bookstackapp.com/]. Con OIDC può legare i gruppi ai ruoli, confrontando i nomi o gli ID esterni scritti nel ruolo [verificato: https://bookstackapp.com/docs/admin/oidc-auth, letto tramite la ricerca]. Entra di solito manda gli ID dei gruppi, non i nomi: vanno scritti nel campo degli ID esterni [non verificato: deduzione].
- **Webhook.** Dalla v21.12 BookStack manda un POST JSON per gli eventi del registro di audit, per esempio `page_update` [verificato: https://www.bookstackapp.com/blog/bookstack-release-v21-12/, letto tramite la ricerca].
- **Database.** Serve MySQL 8.0 o MariaDB 10.6 o successivi. PostgreSQL non è documentato fra i supportati [verificato: https://www.bookstackapp.com/docs/admin/installation/].
- **Server MCP.** Ne esistono di comunità. Il più completo, `ttpears/bookstack-mcp`, è MIT, ha 21 strumenti in lettura e 22 in scrittura, con la scrittura spenta per default. Funziona in stdio o in HTTP, accetta i token di BookStack e descrive anche l'accesso OAuth con Entra per un connettore remoto di Claude. Ha 50 stelle [verificato: https://github.com/ttpears/bookstack-mcp].

### 3.2 Come lo usano gli agenti

- **Lettura.** Ogni famiglia di agenti ha un utente BookStack con un ruolo «Agente lettura», che vede solo i libri che le servono. Per esempio, gli agenti commerciali vedono «Come lavoriamo» e «Catalogo», non i processi interni di amministrazione [non verificato: proposta].
- **Regole personali (C6).** Prima di ogni lavoro per una persona, l'agente legge la sua pagina «Come lavoro» per ID stabile, non per titolo. Il modello di pagina ha sezioni fisse: formato dei riassunti, prossimi passi, orari di non disturbo, tono, cose da non fare mai [non verificato: proposta].
- **Scrittura.** Gli agenti non modificano le pagine ufficiali. Scrivono in un libro «Proposte degli agenti», oppure propongono la modifica al Cancello, che la applica dopo il sì con un `changelog` che cita l'agente e la carta. Le revisioni di BookStack permettono di tornare indietro [non verificato: proposta; il parametro `changelog` è verificato sopra].
- **Ricerca.** La ricerca di BookStack è per parole. Per le domande libere, ogni pagina va anche in Qdrant: il webhook `page_update` chiama n8n, n8n prende il Markdown dall'API e lo passa alla pipeline [non verificato: proposta].
- **MCP.** Due strade: adottare `ttpears/bookstack-mcp` in sola lettura, con versione fissata e codice riletto; oppure scrivere il nostro con 6-8 strumenti (cerca, leggi pagina, leggi libro, elenca, proponi modifica). Il secondo costa di più ma lo controlliamo noi [non verificato: proposta].

### 3.3 Limiti

- **Niente database alla Notion.** BookStack ha pagine, tabelle dentro le pagine e tag, non viste filtrabili su campi. Organigramma, obiettivi e registro dei meeting vanno quindi in Postgres e si guardano in Grafana, che il board ha già [verificato: board-vlan.txt, VLAN 70]. Se qualcuno vuole tabelle modificabili a mano, NocoDB su Postgres è un'opzione, ma dal 9/1/2026 ha una licenza «Sustainable Use» che vieta di offrirlo come servizio a pagamento [verificato: https://nocodb.com/docs/self-hosting/license, letto tramite la ricerca]. Non lo consiglio ora.
- **Un database in più.** MariaDB non è nel board. Va aggiunto nella VLAN DATA, nel backup e nel monitoraggio [non verificato: proposta].
- **MCP di comunità piccolo.** 50 stelle, nessuna data di rilascio visibile [verificato: GitHub, sopra]. Va trattato come codice nostro: versione fissata e revisione.

### 3.4 Giudizio

Adatto, per i testi. API completa, permessi fini per ruolo e per libro, accesso con Entra, webhook, licenza MIT. Non adatto come base dati: per quello c'è Postgres [non verificato: giudizio mio].

---

## 4. Jira in cloud

### 4.1 Fatti

- **Piani.** Free fino a 10 utenti; Standard a 7,91 $ per utente al mese [non verificato: risultato di ricerca che cita https://www.atlassian.com/software/jira/pricing.jsp, pagina non aperta, rilevato il 25/10/2026]. Per quattro persone, Standard costa 31,64 $, cioè circa 28,27 € al mese [non verificato: calcolo mio].
- **Free contro Standard.** Free ha 2 GB e limiti su permessi, ruoli e sicurezza delle issue; i ruoli di progetto e il registro di audit partono da Standard [verificato: https://confluence.atlassian.com/sneaky/servicedeskcloud/jira-cloud-plans-1097175872.html, pagina Atlassian non datata].
- **Account di servizio.** Sono account non legati a una persona, per integrazioni e automazioni. Con accesso a Jira **non contano nel limite di utenti**. Cinque sono inclusi; Atlassian Guard Standard arriva a 250. Usano token API o credenziali OAuth 2.0 e ricevono ruoli e gruppi come un utente [verificato: https://support.atlassian.com/user-management/docs/understand-service-accounts/]. Che i cinque gratuiti valgano anche sul piano Free non è chiaro dalla pagina [non verificato].
- **Token.** I token creati dopo il 15/12/2024 scadono entro un anno [non verificato: https://titanapps.io/blog/jira-api-token-how-to-create-manage-and-secure-your-authentication, fonte di terzi]. Gli account di servizio usano token con ambiti che chiamano Jira dall'indirizzo `api.atlassian.com/ex/jira/<cloudId>/` [non verificato: risposte della community Atlassian].
- **Limiti di traffico.** Dal 2 marzo 2026 valgono limiti a punti per le app Forge, Connect e OAuth; il traffico con token API resta solo sotto i limiti a raffica [verificato: https://developer.atlassian.com/cloud/jira/platform/rate-limiting, letto tramite la ricerca].
- **n8n.** Il nodo Jira Software crea, aggiorna, cerca, commenta e cambia stato alle issue; c'è anche il Jira Trigger; il nodo si può usare come strumento di un agente AI [verificato: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.jira].
- **MCP.** Il server MCP remoto di Atlassian (Rovo MCP) è GA e accetta OAuth 2.1 o token API; le azioni hanno i permessi del titolare del token [verificato: https://github.com/atlassian/atlassian-mcp-server, letto tramite la ricerca]. L'accesso con token API va acceso dall'amministratore dell'organizzazione [non verificato: post della community del 15/5/2026]. In alternativa, `sooperset/mcp-atlassian` è un server MCP da ospitare in casa, MIT, 98 strumenti, con Jira Cloud supportato [verificato: https://github.com/sooperset/mcp-atlassian].

### 4.2 Come lo usano gli agenti

- **Progetti.** Un progetto Jira per ogni progetto cliente, da un modello (fasi, milestone, report del venerdì). Un progetto «Interno» per i to-do di SerSan [non verificato: proposta].
- **Identità.** Un account di servizio per famiglia di agenti (Progetti, Vendite, Direzione), non uno per agente: cinque bastano per partire. Ogni issue creata da un agente porta l'etichetta `da-agente` e il link alla fonte sul server, per esempio l'ID della call [non verificato: proposta].
- **To-do dopo la call (B4).** Il post-call estrae i to-do a schema; il Cancello li crea in Jira come «scrittura interna», a nome del responsabile della call, secondo le regole già previste [verificato: PRESENTAZIONE-CEO.md §5.1, «le scritture interne ... le fa secondo regole scritte»].
- **Chiudere i to-do fatti (A7).** I to-do creati dagli agenti per altri agenti si chiudono da soli. Per quelli delle persone l'agente scrive un commento («mi sembra fatto: lo chiudo?») e chiude solo dopo il sì del titolare [non verificato: proposta].
- **Via di accesso.** Per gli agenti sul server: il nostro MCP o n8n, con il token dell'account di servizio preso da Infisical. Per le persone in Claude Team: il connettore Atlassian, con il loro account [non verificato: proposta].
- **Colore.** Jira è in cloud: dentro le issue vanno riassunti e link, mai trascrizioni, mail intere o dati finanziari [non verificato: proposta coerente con PRESENTAZIONE-CEO.md §5.6].

### 4.3 Free o Standard

Con quattro persone il piano Free basta per il numero di utenti. Il limite vero sono i permessi: senza ruoli di progetto, un account di servizio degli agenti commerciali vedrebbe anche i progetti dei clienti e quelli interni. Proposta: si parte con Free, se SerSan non ha già un piano; si passa a Standard (circa 28 € al mese) quando entrano gli account di servizio con permessi diversi, cioè dalla fase 1 [non verificato: proposta]. Prima va chiesto a Michele su quale piano è oggi Jira.

---

## 5. Microsoft 365: documenti, posta, calendario e chat

### 5.1 SharePoint e OneDrive

- **Struttura.** Un sito SharePoint «Clienti» con una raccolta per cliente (offerte, contratti, consegne, verbali), un sito «SerSan interno» con i modelli SerSan (K7), OneDrive per i file personali [non verificato: proposta].
- **Permessi degli agenti.** Il permesso Graph `Sites.Selected` dà accesso a nessun sito finché un amministratore non concede il singolo sito, con ruolo read, write, manage o fullcontrol. È GA e vale anche per le API REST di SharePoint [verificato: https://devblogs.microsoft.com/microsoft365dev/controlling-app-access-on-specific-SharePoint-site-collections/, letto tramite la ricerca].
- **Attenzione alla ricerca.** Secondo una risposta della community del gennaio 2026, la ricerca di Graph ignora la restrizione di `Sites.Selected` [non verificato: Microsoft Q&A]. Quindi agli agenti non diamo la ricerca di Graph: leggono solo per ID, e le domande libere passano da Qdrant.
- **Indicizzazione.** Graph ha la «delta query» per file (`driveItem`), elementi di lista, messaggi, eventi, messaggi di chat e trascrizioni delle riunioni (`callTranscript`). Restituisce solo ciò che è cambiato dall'ultima volta [verificato: https://learn.microsoft.com/en-us/graph/delta-query-overview]. Un flusso n8n, ogni ora, porta i file nuovi o cambiati dei siti scelti alla pipeline [non verificato: proposta].

### 5.2 Outlook e calendario

- **Caselle limitate.** Il «RBAC per le applicazioni» di Exchange Online sostituisce le vecchie Application Access Policies. Lega un permesso a un ambito di caselle: l'app vede solo quelle. Serve il ruolo di Exchange Administrator; un cmdlet permette di provare l'effetto prima [verificato: https://learn.microsoft.com/graph/auth-limit-mailbox-access].
- **Uso.** Lo Smistatore posta (K3) legge solo le caselle in ambito, con l'accordo di ciascuno. Le bozze stanno in una casella condivisa degli agenti. L'invio lo fa solo l'esecutore del Cancello, dopo il sì, come prima con Gmail. Il report del mattino come primo appuntamento (K1) è un evento creato dall'esecutore nel calendario della persona [non verificato: proposta].
- **Metadati (F1).** Al posto dei metadati di Google Workspace si usano report e log di Microsoft 365, con le stesse tutele: dati aggregati e al massimo 21 giorni per i metadati della posta [verificato per i 21 giorni: 16, tabella dei metadati; non verificato quali API di Microsoft usare].

### 5.3 Teams al posto di Slack

- **Perché Teams.** È già nel board e già pagato con M365. Il board lo usa anche per le notifiche dei bandi («Teams o mail») [verificato: SerSan Infra Board.md, «Bandi»].
- **Stanze.** Un team «SerSan» con un canale per squadra (Outbound, Chiamate, Vendite, Marketing, Studio, Progetti, Amministrazione), un canale «Approvazioni» per le carte, un canale «Agenti» come sala macchine, un canale privato per ogni cliente [non verificato: proposta, ricalcata su PRESENTAZIONE-CEO.md §4.11].
- **Bot.** Graph non permette a un'app di scrivere nei canali a proprio nome, se non per le migrazioni: per scrivere serve un bot del Bot Framework installato nel team [verificato: https://learn.microsoft.com/graph/api/channel-post-messages, letto tramite la ricerca]. Registrare il bot senza una sottoscrizione Azure è possibile dal Developer Portal di Teams, ma le fonti sono in disaccordo [non verificato]. Il bot deve ricevere chiamate dal Bot Framework: serve un indirizzo pubblico, che passa da Pangolin e Traefik [non verificato: deduzione dal board, «Pangolin + Traefik»].
- **Un bot o tanti.** Slack prevedeva un bot per agente [verificato: 22 §3]. In Teams ogni bot è un'app da registrare e installare. Proposta: un bot «Agenti SerSan» per carte, debrief e chat 1:1, con il nome dell'agente in testa a ogni messaggio; bot separati solo per il Capo di gabinetto e pochi altri [non verificato: proposta].
- **Notifiche semplici.** I vecchi connettori di Office 365 in Teams sono stati spenti fra il 18 e il 22 maggio 2026; al loro posto ci sono i webhook di Workflows [non verificato: copia del Message Center MC1181996, https://mc.merill.net/message/MC1181996]. Per avvisi a senso unico (bandi, server, budget) basta un webhook di Workflows, senza bot [non verificato: proposta].
- **Trascrizioni.** Per le call fatte in Teams, Graph espone le trascrizioni con la delta query (`callTranscript`) [verificato: delta-query-overview, sopra]. È una possibile alternativa al bot di registrazione per A1, da provare con i permessi giusti [non verificato].
- **Telegram, WhatsApp e Buzz.** Restano come nella presentazione; il loro collegamento dipende dall'orchestratore (Agent SDK o Hermes), trattato a parte [non verificato].

### 5.4 Il connettore Microsoft 365 di Claude Team

- Cerca e legge SharePoint, OneDrive, Outlook (anche le caselle condivise che la persona vede), chat e canali di Teams, calendari, trascrizioni e registrazioni delle riunioni [verificato: https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector].
- L'accesso è delegato: Claude vede solo ciò che vede la persona. La lettura è attiva per default; la scrittura (mail, eventi, file, messaggi Teams) va accesa a parte, e per Teams ogni strumento di invio si può mettere su «Ask» o «Blocked» [verificato: idem].
- Serve il consenso una tantum di un Global Administrator di Entra, e un tenant con un piano Microsoft Business. La ricerca su SharePoint copre tutto il tenant, senza limite per sito. L'accesso condizionale può valutare le richieste che partono dagli IP di Anthropic, `160.79.104.0/21` [verificato: idem].
- Proposta: acceso per tutti in sola lettura. La scrittura resta spenta: ciò che esce passa dal Cancello [non verificato: proposta].

### 5.5 Un'identità per famiglia di agenti

Ogni famiglia di agenti ha una sua registrazione di app in Entra, con permessi minimi: `Sites.Selected` sui soli siti utili, RBAC di Exchange sulle sole caselle utili, nessun permesso «.All» se non serve. Microsoft vende anche Agent 365, con un'identità Entra per agente; è GA dal 1/5/2026 e costerebbe 15 $ per utente al mese [non verificato: https://www.licensingschool.co.uk/licensing-blog/2026/03/23/agent-365-ga-announcement/]. Per quattro persone non serve ora [non verificato: giudizio mio].

---

## 6. PostgreSQL e Qdrant: la memoria degli agenti

### 6.1 PostgreSQL

- **Versione.** Il board prevede PostgreSQL 16 [verificato: board-vlan.txt, VLAN 40]. La 16 è supportata fino al 9/11/2028; la 17 fino all'8/11/2029; la 18 fino al 14/11/2030 [verificato: https://www.postgresql.org/support/versioning/]. Proposta: valutare la 17 o la 18 all'installazione, per non migrare fra due anni [non verificato: proposta].
- **Schema `memoria`.** Tabelle: `persone`, `regole` (copia strutturata delle pagine BookStack, per leggere in fretta i campi fissi), `registro_agenti`, `obiettivi`, `catalogo`, `processi`, `meetings`, `decisioni`, `passaggi` (i lavori che un agente passa a un altro), `eventi` [non verificato: proposta]. Nello stesso server girano anche i database di LiteLLM e di n8n.
- **Permessi.** Ogni famiglia di agenti ha un ruolo Postgres. La sicurezza per riga (RLS) applica le policy riga per riga; se una tabella ha la RLS attiva e nessuna policy, non si vede niente. Superutenti e ruoli con `BYPASSRLS` la saltano; il proprietario della tabella anche, salvo `FORCE ROW LEVEL SECURITY` [verificato: https://www.postgresql.org/docs/16/ddl-rowsecurity.html].
- **Banca dei token (E3).** LiteLLM mette tetti per chiave, per utente e per team, con azzeramento periodico (`budget_duration`); senza database i budget non valgono [verificato: https://docs.litellm.ai/docs/proxy/users]. Proposta: una chiave per agente, un team per squadra, un utente per persona. Il registro in Postgres guarda le spese di LiteLLM per l'organigramma con i costi [non verificato: proposta].
- **Niente pgvector.** I vettori stanno in Qdrant, come dice il board. In Postgres restano i dati con campi fissi.

### 6.2 Qdrant

- **Permessi per collezione.** Dalla v1.9.0 Qdrant accetta chiavi JWT con accesso in lettura (`r`) o lettura e scrittura (`rw`) per singola collezione. Si accende con `api_key` e `jwt_rbac: true`. Il claim `value_exists` revoca un token cambiando un valore nel database, senza ruotare la chiave [verificato: https://qdrant.tech/documentation/security/].
- **Permessi per documento.** Qdrant non li fa da solo: li deve applicare MCP RAG, con un filtro sul campo `acl` di ogni blocco (gruppi Entra o famiglia di agenti), più `cliente`, `colore` e `fonte` [non verificato: proposta; il board chiede «permessi per utente» a MCP RAG].
- **Ricerca ibrida.** Il tutorial ufficiale combina vettori densi e BM25 sparso, con l'IDF calcolato da Qdrant e la fusione dei risultati nel database [verificato: https://qdrant.tech/documentation/tutorials-basics/cloud-inference-hybrid-search/, letto tramite la ricerca]. Che il BM25 si calcoli anche lato server dalla v1.15.2 lo dice solo una fonte di terzi [non verificato].
- **Collezioni.** Proposta: una collezione `conoscenza` per tutto il generale e una `finanza` separata per i dati fiscali di Sirius. Così un errore nei filtri di MCP RAG non porta la finanza a un agente il cui token non ha accesso a `finanza` [non verificato: proposta].

### 6.3 Il firewall decide il flusso

Il board dice: «APPS → AI solo sulle API dei modelli · AI → DATA solo Qdrant» [verificato: SerSan Infra Board.md, «Regole chiave del firewall»]. Conseguenze:
- il lavoratore di indicizzazione nella VLAN AI scrive solo in Qdrant, quindi tutti i metadati utili alla ricerca stanno nel payload dei blocchi;
- i dati strutturati (numeri di Sirius, registro dei meeting, obiettivi) arrivano in Postgres da n8n, nella VLAN APPS, non dalla VLAN AI;
- MCP RAG, nella VLAN APPS, legge Qdrant nella VLAN DATA: la regola che lo permette va scritta in modo esplicito [non verificato: il board non la elenca].

---

## 7. mcp-memory e MCP RAG

### 7.1 mcp-memory

- **Cosa sappiamo.** È nella VLAN APPS del board [verificato: board-vlan.txt]. Non è nel repo di SersanOutreach e nessun file del progetto lo descrive [verificato: ricerca nei file del 25/10/2026].
- **Le due implementazioni più probabili.** Il server di riferimento «Knowledge Graph Memory» salva entità, relazioni e osservazioni in un file JSONL, non ha utenti né permessi e coordina solo le scritture con un file di lock [verificato: https://github.com/modelcontextprotocol/servers/tree/main/src/memory]. `mcp-memory-service` è Apache-2.0, con ricerca semantica su SQLite-vec e versione 10.x [non verificato: elenchi di glama.ai e mdskills.ai].
- **Proposta.** In entrambi i casi mcp-memory resta un taccuino: un'istanza o un file per famiglia di agenti, con appunti di lavoro, mai dati dei clienti né dati rossi. La memoria aziendale sta in Postgres, BookStack e Qdrant, dietro MCP RAG e un piccolo MCP «memoria» su Postgres [non verificato: proposta].
- **MCP memoria su Postgres.** Strumenti in lettura: `regole_di(persona)`, `obiettivi()`, `catalogo(voce)`, `agente(nome)`, `meeting(cliente, periodo)`, `decisioni(cliente)`. Nessuno strumento in scrittura: le scritture passano dal Cancello [non verificato: proposta].

### 7.2 MCP RAG: una porta sola

- **Cosa fa.** Il board lo mette in fondo alla pipeline, con permessi per utente e registro delle query, verso Claude Team [verificato: SerSan Infra Board.md, «Pipeline AI»].
- **Strumenti proposti.** `cerca(domanda, filtri)` restituisce passaggi riordinati dal reranker, ognuno con fonte, data e link (SharePoint, BookStack, Jira o Sirius); `apri(id)` dà il blocco intero; `fonti(cliente)` elenca i documenti di un cliente [non verificato: proposta].
- **Chi chiede.** Una persona da Claude Team, autenticata con Entra; oppure un agente sul server, con il suo token. MCP RAG trasforma l'identità in filtri sul payload [non verificato: proposta].
- **Registro.** Ogni query va in Loki con chi, cosa, quali blocchi sono usciti [non verificato: proposta; Loki è nel board].

### 7.3 Come si collegano Claude Team e gli agenti sul server

- **Claude Team.** I connettori personalizzati partono dai server di Anthropic, non dal computer della persona. Un server dietro VPN o firewall non si raggiunge, salvo aprire agli IP di Anthropic. Solo gli Owner aggiungono un connettore; poi ogni persona si collega da sola, e Claude vede solo ciò che quella persona può vedere [verificato: https://support.claude.com/en/articles/11175166-about-custom-connectors-using-remote-mcp, letto tramite la ricerca]. È quello che il board prevede con Pangolin e Traefik [verificato: board, «Accesso»]. Il punto delicato: se Pangolin chiede un suo login davanti, il server di Anthropic non lo supera. MCP RAG deve fare da sé l'OAuth 2.1 con Entra, e Pangolin deve lasciar passare quel percorso [non verificato: da provare].
- **Agenti sul server con l'Agent SDK.** L'SDK collega server MCP in stdio, HTTP o dentro il processo. Gli strumenti si chiamano `mcp__<server>__<strumento>` e si autorizzano uno per uno con `allowedTools`. Per i server HTTP il token va nell'intestazione `Authorization`. L'SDK non fa il giro OAuth interattivo [verificato: https://code.claude.com/docs/en/agent-sdk/mcp]. Quindi ogni famiglia di agenti ha un token statico, conservato in Infisical, e una lista di strumenti permessi [non verificato: proposta].
- **Claude Desktop via mesh.** Il board prevede questa alternativa [verificato: board, «Pangolin + Traefik»]. Utile per Michele e Alberto, che possono usare MCP RAG senza esporlo [non verificato: proposta].

---

## 8. Sirius

### 8.1 Cosa sappiamo

- Compare solo nel board: «Sirius → conoscenza ricercabile → Claude Team», con il primo passo «Export: Fiscale, clienti, documenti da Sirius · incrementale». La pipeline sta nella fase F4, «AI + bandi» [verificato: SerSan Infra Board.md].
- Nessun altro file del progetto lo nomina, e nemmeno il repo di SersanOutreach [verificato: ricerca nei file del 25/10/2026].
- La ricerca web non trova un gestionale o un archivio italiano chiamato «Sirius»: escono un POS per l'ospitalità (Siriusware), una software house di Quarrata senza prodotti noti e una startup moldava di contabilità [verificato: ricerca web del 25/10/2026; nessun risultato pertinente].

### 8.2 Ipotesi

1. È lo strumento che oggi tiene contabilità, dati fiscali, anagrafiche dei clienti e documenti. Lo fa pensare la parola «Fiscale», e la presentazione elenca fra le verifiche della prima settimana «quale strumento di fatturazione e contabilità usiamo oggi» [verificato per la frase: PRESENTAZIONE-CEO.md §14; l'ipotesi non è verificata].
2. È il nome di un server o di un archivio esistente, da esportare durante l'uscita da Azure (F0 «Export completo da Azure», F2 «Via da Azure») [verificato per le fasi: board; l'ipotesi non è verificata].

Da chiedere a Michele: che cos'è, dove sta, che formati esporta (PDF, XML delle fatture, CSV), se ha API o solo export, di chi sono i dati (di SerSan o anche dei clienti dei clienti) e chi oggi può vederli.

### 8.3 Come la pipeline serve gli agenti

| Passo del board | Cosa fa [verificato: SerSan Infra Board.md, «Pipeline AI»] | Cosa ne ricavano gli agenti [non verificato: proposta] |
|---|---|---|
| Export | fiscale, clienti, documenti da Sirius, incrementale | solo i dati nuovi o cambiati; i numeri strutturati vanno anche in Postgres via n8n |
| Docling | PDF, scansioni, tabelle diventano testo strutturato | anche le scansioni diventano ricercabili |
| Filtro | segreti e chiavi scartati, PII marcate | le PII marcate permettono a MCP RAG di oscurarle per chi non deve vederle |
| Blocchi e metadati | Qwen3-4B Q5 aggiunge cliente, anno, tipo, riassunto | filtri precisi: «fatture del cliente X del 2025» |
| Embedding | Qwen3-Embedding 0.6B FP16, Qdrant e BM25 | ricerca per significato e per parole esatte (numeri di fattura, codici) |
| Reranker | Qwen3-Reranker 0.6B | meno passaggi, più pertinenti: meno token spesi |
| MCP RAG | permessi per utente, registro delle query, verso Claude Team | la stessa porta serve gli agenti sul server |

Il principio del board è «il server cerca e prepara, Claude ragiona» e «password e chiavi non entrano mai nell'indice» [verificato: SerSan Infra Board.md].

### 8.4 Chi la usa

| Agente o funzione | Cosa chiede | Fonte giusta [non verificato: proposta] |
|---|---|---|
| Controllo di gestione (L3, K14) | margini per cliente e per progetto, cassa, distanza dagli obiettivi | numeri da Postgres; documenti da MCP RAG per spiegare gli scostamenti |
| Agente fatture e incassi (L2) | storico fatture, scadenze, solleciti già fatti | numeri da Postgres; testi da MCP RAG |
| Agente acquisti e abbonamenti (K15) | fatture dei fornitori, rinnovi | MCP RAG con filtro `tipo` |
| Agente bandi (L4) | requisiti, fatturato, dati aziendali per la candidatura | MCP RAG; i bandi stessi arrivano dalla pipeline Firecrawl del board |
| Agente brief e Agente rinnovi (D2, D3, L6) | storico della relazione, offerte e contratti passati | MCP RAG con filtro `cliente` |
| Agente proposte e Agente contratti (D5, L1) | offerte e contratti simili come modello | MCP RAG e catalogo in Postgres |
| Bibliotecario e Capo di gabinetto (K4) | domande libere | MCP RAG |
| Persone in Claude Team | domande libere con le fonti | MCP RAG, con i loro permessi |

### 8.5 Due avvertenze

- **I numeri non si cercano, si calcolano.** Il RAG trova passaggi; non somma il fatturato. Il debrief e il controllo di gestione devono leggere numeri calcolati dal codice su dati strutturati, come già previsto per il debrief [verificato: 22 §4, C1, «numeri calcolati dal codice»]. Quindi l'export di Sirius deve dare anche righe strutturate (per esempio data, cliente, importo) che n8n carica in Postgres [non verificato: proposta].
- **I dati rossi e Claude Team.** La regola dei tre colori dice: finanza e documenti dei clienti sono rossi; restano sul server, oppure vanno all'API Anthropic dopo l'oscuramento locale [verificato: PRESENTAZIONE-CEO.md §5.6]. Il board invece fa ragionare Claude Team sui dati di Sirius, e il filtro marca le PII senza toglierle [verificato: board]. Claude Team non è l'API. Tre strade: MCP RAG oscura i blocchi rossi prima di darli a Claude Team; oppure si aggiorna la regola, dopo aver riletto i termini di Claude Team con il legale; oppure i blocchi rossi vanno solo agli agenti sul server, via LiteLLM e API [non verificato: proposta]. Va deciso prima della fase F4.

### 8.6 Una pipeline, più sorgenti

La pipeline del board è il pezzo giusto per tutta la memoria vettoriale, non solo per Sirius. Proposta: lo stesso percorso (Docling, filtro, metadati, embedding, reranker) con più ingressi, ognuno con il suo campo `fonte` [non verificato: proposta]:

| Fonte | Come arriva | Quando |
|---|---|---|
| Sirius | export incrementale | come da board |
| BookStack | webhook `page_update`, poi API in Markdown | a ogni modifica |
| Jira | Jira Trigger di n8n | a ogni modifica |
| SharePoint e OneDrive | delta query di Graph, sui soli siti scelti | ogni ora |
| Outlook | delta query, sulle sole caselle in ambito e con l'accordo di ciascuno | ogni ora |
| Trascrizioni delle call | dal bot di registrazione o da `callTranscript` di Teams | dopo ogni call |
| Bandi | pipeline Firecrawl del board | ogni notte |

La GPU è condivisa: la RTX 4000 serve la VLAN AI e la VM Experimental-1 nella VLAN LAB [verificato: board-vlan.txt]. La prima indicizzazione dell'archivio va pianificata nelle ore in cui la GPU è assegnata all'AI; la seconda GPU prevista in F5 toglie il problema [non verificato: deduzione].

---

## 9. Dove va ogni funzione che usava Notion o Slack

«Prima» riassume 22 §4 e PRESENTAZIONE-CEO.md, appendice A e sezioni 4-5 [verificato]. «Ora» è la mia proposta sul board [non verificato].

| Voce | Prima | Ora |
|---|---|---|
| J4 Passaggi fra agenti | bacheca di Hermes e chat di gruppo (Slack) | tabella `passaggi` in Postgres, visibile nel canale Teams «Agenti»; i to-do visibili alle persone in Jira |
| J7, I4 Marketing in fase 0 | Claude in Slack | app di Claude Team, senza Slack |
| J8 Squadra progetti | task in Notion | Jira, un progetto per cliente da modello; canale Teams e cartella SharePoint creati dall'Onboarding tramite gli esecutori |
| J9 Chat di gruppo | Slack dal primo giorno, Telegram e WhatsApp, Buzz in prova | Teams dal primo giorno; Telegram, WhatsApp e Buzz come prima |
| A2 Memoria relazionale | Notion: regole, processi, obiettivi, catalogo | BookStack per i testi, Postgres per i dati, MCP memoria per gli agenti |
| A3 Memoria vettoriale | pgvector | Qdrant e BM25 con MCP RAG, pipeline del board estesa |
| A5 Raccoglitore | legge mail, calendario, Drive, chat, Notion | legge Outlook, calendario, SharePoint, OneDrive, Teams, BookStack, Jira, Sirius tramite la pipeline |
| A7 Chat fra agenti | `#agenti` in Slack, un bot per agente | canale Teams «Agenti»; un bot con il nome dell'agente nel messaggio; freno ai giri nel Cancello |
| B1 Recap nel canale del cliente | canale Slack interno, poi Slack Connect | canale privato Teams per cliente; con il cliente un canale condiviso di Teams o la mail, dopo la carta (il canale condiviso con esterni va provato) |
| B3 Mail di follow-up | carta in `#approvazioni`, esecutore Gmail | carta nel canale Teams «Approvazioni» o in chat 1:1, esecutore Outlook via Graph |
| B4 To-do al team | Notion | Jira, scrittura interna del Cancello |
| B5 Autonomia crescente | regole «Sempre» sulle carte Slack | stesse regole, sulle carte Teams |
| C1 Debrief del mattino | DM Slack alle 7:00 | chat 1:1 di Teams e mail; numeri da Postgres |
| C4 Dettatura | note vocali Slack trascritte in casa | dettatura delle app Claude; note vocali in una cartella OneDrive, trascritte sul server |
| C5 Registro dei meeting | tabella `meetings`, vista in Notion | tabella `meetings` in Postgres, vista in Grafana |
| C6 Regole personali | pagina Notion «Come lavoro» | pagina BookStack «Come lavoro», letta per ID prima di ogni lavoro |
| D5 Offerta dal catalogo | catalogo in Notion | testi in BookStack, prezzi in Postgres, offerta in SharePoint |
| E3 Banca dei token | porta dei modelli; report e organigramma in Notion | budget in LiteLLM, tetti nel Cancello, vista in Grafana |
| F1 Metadati del lavoro | Google Workspace | report e log di Microsoft 365, con le stesse tutele |
| F2 Interviste | DM Slack | chat 1:1 di Teams con il bot |
| F5 AI per tutti | Slack come porta unica, Claude Team per tutti | Teams come porta unica, Claude Team per tutti |
| G1 Call di vendita in un canale | `#call-vendita` | canale Teams «Call di vendita» |
| G4 Report a chi ha fatto la call | messaggio privato | chat 1:1 di Teams; al responsabile solo aggregati |
| G9 Organigramma | registro esportato in Notion | registro in Postgres; Grafana e pagina BookStack rigenerata ogni notte |
| H2 I CEO approvano | carte in Slack | carte in Teams, anche dal telefono |
| H6 Premio mensile | classifica dal registro | classifica in Grafana dal registro |
| I1, I2 Il contesto fa la qualità | due memorie (Notion e vettoriale) | quattro case e una porta di ricerca |
| K1 Debrief come primo appuntamento | evento in calendario | evento in Outlook creato dall'esecutore |
| K2 «Ho trovato tre nuove call» | annuncio in `#agenti` | annuncio nel canale Teams «Agenti»; inviti in Outlook dopo il sì |
| K3 Posta smistata | Gmail | Outlook, caselle limitate con il RBAC di Exchange |
| K4 Chiedere cosa si è detto | Bibliotecario in chat | MCP RAG da Claude Team e Capo di gabinetto in Teams |
| K14, L3 Finanza e obiettivi | obiettivi in Notion | Postgres e dati strutturati di Sirius |
| L4 Bandi | agente in fase 6 | pipeline del board (n8n, Firecrawl, LLM 4B, RAG e DB, notifica Teams o mail) |
| L5 Assistenza nella stanza del cliente | canale condiviso Slack | canale condiviso Teams o mail, dopo la carta |
| L11 Sistemista | avvisi a Michele | Prometheus, Grafana, Loki, Uptime Kuma, Wazuh; avvisi via webhook di Workflows in Teams |

Le voci che non usavano né Notion né Slack non cambiano per effetto di questo rapporto.

---

## 10. Costi e lavoro

**Costi mensili** (prezzi rilevati il 24/10/2026 per le voci della presentazione, il 25/10/2026 per Jira):

| Voce | € al mese | Fonte |
|---|---|---|
| Escono Notion Plus × 4 | −35,74 | [verificato: PRESENTAZIONE-CEO.md §12.1] |
| Esce Slack Pro × 4 | −27,00 | [verificato: idem] |
| Esce Claude in Slack con tetto | −44,67 | [verificato: idem] |
| **Totale che esce** | **−107,41** | calcolo mio |
| Entra Jira Free | 0 | [non verificato: prezzo citato in §4.1] |
| oppure Jira Standard × 4 | +28,27 | [non verificato: calcolo mio] |
| BookStack, MariaDB, Qdrant, Postgres | 0 di licenza | [verificato: BookStack MIT; gli altri sono nel board] |

Nella presentazione il kit commerciale conta anche Google Workspace a 54,40 € al mese [verificato: PRESENTAZIONE-CEO.md §12.1]. Se la suite è M365, quella riga va sostituita con il costo di M365 già pagato [non verificato: piano M365 da confermare].

**Lavoro** [non verificato: stima mia, base e con riserva del 30 %]:

| Pezzo | gp |
|---|---|
| BookStack con MariaDB, OIDC con Entra e gruppi, modelli di pagina, ruoli degli agenti | 1-1,5 → 1,3-2 |
| MCP BookStack: adozione in sola lettura e revisione (oppure il nostro: 1,5-2) | 0,5-1 → 0,7-1,3 |
| MCP memoria su Postgres: schema, RLS, 6-8 strumenti | 2-3 → 2,6-3,9 |
| Jira: account di servizio, modello di progetto, flussi n8n | 1,5-2 → 2-2,6 |
| Graph: registrazioni, `Sites.Selected`, RBAC di Exchange, esecutori Outlook e calendario | 2-3 → 2,6-3,9 |
| Bot Teams con carte e chat 1:1, registrazione, indirizzo dietro Pangolin | 4-6 → 5,2-7,8 |
| Ingressi della pipeline: BookStack, Jira, SharePoint, Outlook, trascrizioni | 3-5 → 3,9-6,5 |
| Organigramma in Grafana e pagina BookStack generata | 0,5-1 → 0,7-1,3 |
| **Totale** | **14,5-22,5 → 19-29** |

Buona parte sostituisce lavoro già previsto per Notion, Slack e Gmail: per esempio le carte in Slack valevano 4 gp [verificato: 22 §5, fase 1]. Il lavoro in più netto è di circa 6-9 gp, soprattutto per il bot Teams e per gli ingressi della pipeline [non verificato: stima mia].

---

## 11. Rischi

| Rischio | Mitigazione [non verificato: proposte] |
|---|---|
| Bot Teams più complessi dei bot Slack; serve un indirizzo pubblico | un solo bot all'inizio; indirizzo dietro Pangolin con verifica dei token del Bot Framework; notifiche semplici con i webhook di Workflows |
| Jira Free senza ruoli di progetto: un account di servizio vede tutto | Standard dalla fase 1, o progetti separati per sito |
| Dati rossi verso Claude Team tramite MCP RAG | decisione del §8.5 prima della fase F4 |
| La ricerca di Graph ignora `Sites.Selected` | agli agenti niente ricerca di Graph; solo letture per ID e Qdrant |
| MCP di BookStack di comunità, piccolo | versione fissata, sola lettura, revisione; oppure il nostro |
| mcp-memory senza permessi | solo taccuino per famiglia di agenti, mai dati dei clienti |
| MariaDB fuori dal board | aggiungerlo nella VLAN DATA, nel backup PBS e nel monitoraggio |
| Doppioni fra BookStack e Postgres | una fonte di verità per ogni informazione (§2); le copie si rigenerano |
| Sirius sconosciuto | domande a Michele (§12) prima di progettare l'export |

---

## 12. Domande aperte per Michele

1. Che cos'è Sirius, dove sta, che formati esporta, se ha API, di chi sono i dati e chi li vede oggi?
2. mcp-memory è il server di riferimento a grafo, `mcp-memory-service` o un altro? Chi lo usa oggi?
3. Su quale piano è Jira oggi? Lo usate già per i progetti dei clienti?
4. Quale piano M365 ha SerSan (Basic, Standard, Premium)? Chi è Global Administrator per i consensi?
5. Si può esporre un indirizzo per il bot Teams dietro Pangolin, accanto all'endpoint MCP?
6. MCP RAG nella VLAN APPS può leggere Qdrant nella VLAN DATA? La regola va scritta.
7. Per i dati rossi che MCP RAG passa a Claude Team, quale delle tre strade del §8.5?
8. PostgreSQL 16 come nel board, o 17-18 all'installazione?
9. Teams diventa la chat di gruppo, o si preferisce una chat interamente in casa (componente nuovo, fuori dal board)?

---

## Fonti

**File del progetto** (letti il 25/10/2026):
- `C:\Users\alber\SerSan-AgentOS\allegati\infra\SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`
- `C:\Users\alber\SerSan-AgentOS\ricerca\00-visione-funzionalita.md`
- `C:\Users\alber\SerSan-AgentOS\ricerca\22-architettura-scelta.md`
- `C:\Users\alber\SerSan-AgentOS\PRESENTAZIONE-CEO.md`
- `C:\Users\alber\SerSan-AgentOS\ricerca\01-sersanoutreach.md`, `16-gdpr-ai-act-e-regole.md`, `18-agenti-in-abbonamento.md`
- `C:\Users\alber\SerSan-AgentOS\allegati\sersanoutreach\sersan_company_profile.md`

**Web e documentazione** (rilevati il 25/10/2026):
- BookStack: https://www.bookstackapp.com/ · https://www.bookstackapp.com/blog/bookstack-release-v26-09/ · https://demo.bookstackapp.com/api/docs · https://www.bookstackapp.com/docs/user/roles-and-permissions/ · https://www.bookstackapp.com/docs/admin/installation/ · https://bookstackapp.com/docs/admin/oidc-auth · https://www.bookstackapp.com/blog/bookstack-release-v21-12/ · https://github.com/ttpears/bookstack-mcp
- NocoDB: https://nocodb.com/docs/self-hosting/license
- Jira e Atlassian: https://www.atlassian.com/software/jira/pricing.jsp · https://confluence.atlassian.com/sneaky/servicedeskcloud/jira-cloud-plans-1097175872.html · https://support.atlassian.com/user-management/docs/understand-service-accounts/ · https://developer.atlassian.com/cloud/jira/platform/rate-limiting · https://github.com/atlassian/atlassian-mcp-server · https://github.com/sooperset/mcp-atlassian · https://titanapps.io/blog/jira-api-token-how-to-create-manage-and-secure-your-authentication
- n8n: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.jira · https://docs.n8n.io/integrations/builtin/credentials/jira
- Microsoft: https://devblogs.microsoft.com/microsoft365dev/controlling-app-access-on-specific-SharePoint-site-collections/ · https://learn.microsoft.com/graph/auth-limit-mailbox-access · https://learn.microsoft.com/en-us/graph/delta-query-overview · https://learn.microsoft.com/graph/api/channel-post-messages · https://mc.merill.net/message/MC1181996 · https://www.licensingschool.co.uk/licensing-blog/2026/03/23/agent-365-ga-announcement/
- Claude: https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector · https://support.claude.com/en/articles/11175166-about-custom-connectors-using-remote-mcp · https://code.claude.com/docs/en/agent-sdk/mcp
- PostgreSQL: https://www.postgresql.org/support/versioning/ · https://www.postgresql.org/docs/16/ddl-rowsecurity.html
- Qdrant: https://qdrant.tech/documentation/security/ · https://qdrant.tech/documentation/tutorials-basics/cloud-inference-hybrid-search/
- LiteLLM: https://docs.litellm.ai/docs/proxy/users
- MCP memory: https://github.com/modelcontextprotocol/servers/tree/main/src/memory · https://glama.ai/mcp/servers/@doobidoo/mcp-memory-service
- Ricerche su «Sirius» senza risultati pertinenti: https://www.capterra.it/software/77989/sirius-e · https://atoka.io/public/it/azienda/sirius-technology-srl/7e3d960d9d84 · https://accesso.com/?p=6555
