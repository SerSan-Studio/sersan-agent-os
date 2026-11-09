# 28 · La chat di gruppo di persone e agenti, senza Slack e senza Azure

**Data di rilevazione:** 25/10/2026. **Per:** Michele Sanna (infrastruttura), Alessandro Serratt, Mattia Scattu; preparato per Alberto Tuveri.
**Oggetto:** la chat di gruppo dell'idea di Alberto (voci J9 e A7 di `ricerca/00-visione-funzionalita.md`): persone e agenti nelle stesse stanze, "come Buzz", raggiungibile anche da Telegram e WhatsApp, con le approvazioni dal telefono.
**Vincoli (board di Michele, vincolante):**
- in cloud restano solo M365/Entra ID (identità, MFA, posta, Teams), Claude Team, API Anthropic dietro LiteLLM, Cloudflare (DNS), GitHub, Supabase, Vercel, Jira, Instantly e un S3 fuori sede facoltativo;
- Azure esce: "tutto l'IaaS generico (Azure) esce";
- tutto il resto è self-hosted sul DL380, con VLAN default-deny su OPNsense;
- si entra solo da NetBird (SSO Entra più FIDO2) e da Pangolin più Traefik.

[verificato: `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`]. Slack non è nella lista, quindi esce.

**Legenda.**
- **[verificato: fonte]**: controllato oggi sulla fonte indicata. "Estratto" vuol dire che ho letto il passo tramite il motore di ricerca e non la pagina intera.
- **[non verificato]**: voce di terzi, pagina non raggiunta o deduzione mia.
- **[stima]**: un numero mio, con il ragionamento accanto.

Prezzi IVA esclusa, rilevati il 25/10/2026. Cambi: 1 $ = 0,8934 €, come nei rapporti precedenti [verificato: `ricerca/14`]; 1 £ = 1,1872 €, tasso della Bank of England del 19/10/2026 [verificato: tabella BoE su poundsterlinglive.com]. gp = giorni-persona.

---

## In breve

La chat di gruppo resta **Microsoft Teams**, che SerSan paga già con M365 e che il board tiene in cloud. Gli agenti entrano in Teams con un nostro bot, la **Porta chat**. Il bot gira sul server, nella VLAN 30 APPS, accanto al motore sull'Agent SDK di Claude e al Cancello.

**Le approvazioni** arrivano sul telefono come Adaptive Card con i pulsanti. Teams dice al bot chi ha premuto, con l'identità Entra protetta da MFA. Il Cancello accetta il sì solo dalle persone autorizzate per quella classe di azione.

**La registrazione del bot.** Il bot si registra come "Teams-managed" dal Developer Portal di Teams, senza sottoscrizione Azure: lo dice la documentazione di Microsoft. Alcuni utenti però segnalano problemi, quindi va provato in un giorno. Se la prova fallisce, ci sono due riserve:
- una registrazione Azure Bot gratuita: nessuna macchina virtuale, canale Teams senza limiti di messaggi;
- un piano B senza bot.

**Gli altri canali.**
- **Telegram** è facoltativo e porta solo avvisi senza contenuto. Usa la Bot API ufficiale in long polling, quindi nessuna porta aperta.
- **WhatsApp** entra più avanti e soprattutto per i clienti. Usa la Cloud API ufficiale di Meta, con i messaggi a pagamento.
- **Buzz** resta un pilota nella VLAN LAB.
- **Mattermost** è il piano B se un giorno si esce da Teams.
- **Matrix** non conviene per quattro persone.

**Costi e lavoro.**
- Costo fisso in più: **0 €** al mese.
- Rispetto al piano precedente si risparmiano Slack Pro (27,00 €) e Claude in Slack (44,67 €) [verificato: `ricerca/22` §9].
- Lavoro: **8-11 gp** per Teams più Telegram [stima, §9].

Punti chiave:
1. **Teams costa zero in più** se il piano M365 di SerSan lo include già. Da luglio 2026 i listini UK sono: Business Basic £5,40, Standard £10,80, Premium £16,90 per utente al mese, con impegno annuale [non verificato sulla pagina Microsoft: fonti di terzi, §2.1].
2. **Il bot non richiede Azure, sulla carta.** Microsoft scrive "No Azure subscription needed" per i bot Teams-managed e li dice adatti anche alla produzione, se non servono OAuth e SSO. Un moderatore di Microsoft Q&A scrive invece che serve una risorsa Azure Bot [verificato: §2.2]. Si decide con una prova di un giorno.
3. **Approvare dal telefono funziona.** L'app mobile di Teams mostra Adaptive Card fino alla versione 1.6. `Action.Execute` aggiorna la carta per tutti, per esempio con "approvato da… alle…" [verificato: Microsoft Learn, pagine aggiornate il 30/09 e il 13/10/2026].
4. **Il nodo Teams di n8n non basta per il Cancello.** Il suo "Send and Wait" su Teams usa pulsanti-link verso n8n. Registra quando si risponde, ma non chi: il "chi" c'è solo per Slack e Telegram [verificato: documentazione e changelog di n8n, versione 2.30 del 07/07/2026]. Va bene per gli avvisi, come i bandi; non per le approvazioni.
5. **Buzz, al 25/10, non è ancora una chat aziendale.** È in versione 0.5.28 del 09/10/2026. Le approvazioni sono ancora aperte (PR #8057 e #7616). Non ci sono connettori per Teams, Telegram o WhatsApp [verificato: API GitHub, 25/10].
6. **Telegram e WhatsApp hanno strade ufficiali.**
   - Telegram: Bot API 10.3, gratuita.
   - WhatsApp: Cloud API, a messaggio. Dal 01/10/2026 sono gratuiti 1.000 messaggi di servizio al mese per numero; oltre si paga [verificato: core.telegram.org; developers.facebook.com, 25/10].
   - I ponti non ufficiali per WhatsApp (mautrix, librerie "WhatsApp Web") rischiano il blocco del numero e non si usano.

---

## 1. Che cosa deve fare la chat, e che cosa cambia

| Richiesta | Da dove viene | Che cosa chiede alla chat |
|---|---|---|
| Chat di gruppo "come Buzz", collegabile a Slack, Telegram e WhatsApp | J9 [verificato: `ricerca/00`] | stanze per squadra, agenti come membri con un nome, accesso dal telefono, più canali verso gli stessi agenti |
| Chat condivisa fra agenti, leggibile da noi | A7 [verificato: `ricerca/00`] | vedere i passaggi di lavoro fra agenti e intervenire |
| Approvazioni su tutto ciò che esce (il Cancello) | `ricerca/22` §1-§2 [verificato] | pulsanti sul telefono, identità certa di chi approva, mai approvazioni concesse da un agente |
| Recap nel canale del cliente | B1 [verificato: `ricerca/00`] | un canale condiviso con persone esterne |
| Notifica dei bandi "Teams o mail" | board, pipeline bandi [verificato: board] | un messaggio al giorno in un canale |
| Slack esce, Azure esce, resto self-hosted | board di Michele [verificato] | niente Slack Pro, niente Claude in Slack, niente servizi Azure per far girare qualcosa |
| Michele preferisce valutare l'Agent SDK di Claude al posto di Hermes | messaggio di Michele [verificato: testo nel compito] | la chat non deve dipendere dal gateway di Hermes |

**Il cambio più grosso rispetto al piano precedente.** Il piano usava Slack in Socket Mode: connessioni solo in uscita, nessuna porta aperta [verificato: `ricerca/22` §2]. Un bot Teams invece riceve i messaggi su un indirizzo HTTPS pubblico, chiamato dai server di Microsoft [verificato: Microsoft Q&A, 13/01/2026, §2.2]. Serve quindi **una rotta pubblica** dietro Pangolin più Traefik. La rotta è unica, stretta e firmata da Microsoft.

---

## 2. Microsoft Teams

### 2.1 Licenze per una Ltd inglese nel 2026

| Piano Microsoft 365 (UK, con Teams) | Prima del 01/07/2026 | Dal 01/07/2026, al rinnovo | In € (1 £ = 1,1872 €) | Fonte |
|---|---|---|---|---|
| Business Basic | £4,60 | **£5,40** per utente al mese, annuale | 6,41 € | [non verificato sulla pagina Microsoft: nerdster.co.uk, aggiornato il 19/10/2026; amvia.co.uk] |
| Business Standard | £9,60 | **£10,80** | 12,82 € | idem |
| Business Premium | £16,90 | **£16,90** (invariato) | 20,06 € | idem |
| Fatturazione mensile | | £6,48 / £12,96 / £20,28 | | [non verificato: amvia.co.uk] |
| Listino USA | Basic 6 $, Standard 12,50 $, Premium 22 $ | Basic **7 $**, Standard **14 $**, Premium **22 $** | | [non verificato: office-watch.com, uctoday.com] |
| Piani senza Teams | esistono | una fonte indica £4,20 / £8,30 / £14,40 | | [non verificato: una sola fonte di terzi] |

**Lettura per SerSan.**
- Il board tiene "M365 / Entra ID" in cloud. SerSan ha già posta, identità e Teams, quindi la chat di gruppo **non aggiunge licenze** [stima].
- Il piano esatto di SerSan (Basic, Standard o Premium) e il numero di posti **non sono nei file**: è una domanda aperta.
- Teams Premium non serve per bot, carte e canali [stima].
- La pagina dei prezzi di Microsoft UK non ha risposto (timeout), quindi i prezzi vanno ricontrollati lì prima di metterli in un preventivo.

### 2.2 Il bot: registrazione, Azure sì o no, SDK

**Come arriva un messaggio al bot.** Il manifest dell'app Teams contiene solo l'ID dell'app, non l'indirizzo del bot. Teams inoltra i messaggi tramite il Bot Framework Service di Microsoft, che usa la registrazione del bot per trovare l'endpoint [verificato: risposta del moderatore su learn.microsoft.com/answers, domanda 5706215, 13/01/2026]. Quindi qualche registrazione presso Microsoft serve sempre. Il punto è **dove** sta.

| Strada | Serve una sottoscrizione Azure? | Costo | Limiti e stato | Fonte |
|---|---|---|---|---|
| **A. Teams-managed** (Developer Portal di Teams, o CLI del Teams SDK `teams app create` senza `--azure`) | **No**: "No Azure subscription needed", "Zero infrastructure to manage" | 0 € | niente gestione delle connessioni OAuth, niente SSO, controllo limitato sulla registrazione; "Works for production too, as long as you don't need OAuth/SSO"; si può migrare dopo verso Azure con `teams app bot migrate` senza cambiare ID e segreto | [verificato: microsoft.github.io/teams-sdk/cli/concepts/bot-locations, 25/10] |
| Segnali contrari su A | | | un moderatore di Microsoft Q&A scrive che non si può fare a meno della registrazione e che "per un bot Teams in produzione va usato Azure Bot Service"; un utente con un bot single-tenant creato solo nel Developer Portal ha avuto errori **401** sulle risposte e sui messaggi proattivi, e il 17/12/2025 scrive di averli risolti senza dire come | [verificato: Q&A 5706215 del 13/01/2026; Q&A 5650695 del 07/12/2025] |
| **B. Azure Bot, piano F0** | **Sì**: sottoscrizione, resource group, Azure CLI | **0 €**: Teams è un canale "standard" e i canali standard hanno "Unlimited messages" | dopo il 31/07/2025 non si creano più bot multi-tenant: solo single-tenant o identità gestita | [verificato: azure.microsoft.com/en-gb/pricing/details/bot-services, 25/10; learn.microsoft.com/azure/bot-service/abs-quickstart, estratto] |
| **C. Nessun bot** (piano B) | No | 0 €, oppure circa 6,41 € al mese per un utente di servizio Business Basic | i messaggi li posta n8n (nodo Teams) o un webhook di Workflows; l'approvazione si fa su una pagina del Cancello dietro Pangolin con SSO Entra | [stima: §2.4 e §2.5] |

**Che cosa vuol dire per "Azure esce".**
- La strada A non usa Azure.
- La strada B usa Azure solo come **registro gratuito**: nessuna VM, nessun database, nessun servizio che fa girare il nostro codice [stima]. I messaggi passano comunque dal Bot Framework Service di Microsoft anche con la strada A [verificato: Q&A 5706215].
- **Decide Michele** se una sottoscrizione con un solo oggetto gratuito rispetta il board.
- Se la sottoscrizione chiede un metodo di pagamento in archivio: [non verificato].

**SDK da usare.**

| Componente | Stato al 25/10/2026 | Fonte |
|---|---|---|
| Bot Framework SDK (il vecchio) | archiviato su GitHub; i ticket di supporto non sono più serviti dal 31/12/2025; i bot esistenti continuano a funzionare | [verificato: docs.azure.cn/en-us/bot-service/bot-service-overview, estratto] |
| **Teams SDK** di Microsoft | TypeScript, C# e Python; **Python in GA dal 01/05/2026** (pacchetto `microsoft-teams-apps`); OAuth, accesso tipizzato a Graph, plugin. La CLI è ancora "Preview" | [verificato: devblogs.microsoft.com, 01/05/2026; documentazione Teams SDK, estratto] |
| TeamsFx (il "Teams Toolkit" di prima) | deprecato da settembre 2025, supporto fino a settembre 2026 | [verificato: learn.microsoft.com/…/tool-sdk-overview, estratto] |
| **Chat SDK di Vercel** (`vercel/chat`) | licenza MIT; 2.421 stelle; ultimo push il 23/10/2026; adattatori `adapter-teams`, `adapter-telegram`, `adapter-whatsapp` e altri. L'adattatore Teams usa sotto il Teams SDK (`@microsoft/teams.apps`) e accetta `appType: "SingleTenant"`. Quello Telegram ha la modalità `polling`, quello WhatsApp usa la Cloud API ufficiale. Lo stato si può tenere in Postgres (`state-pg`) | [verificato: API GitHub e README dei pacchetti, 25/10] |

**Lettura.** Con l'Agent SDK al posto di Hermes manca il gateway già pronto. Hermes ha 22 plugin di piattaforma, Teams compreso [verificato: `ricerca/10` §4]. La Porta chat va quindi scritta, ma è piccola.
- Il **Chat SDK** dà Teams, Telegram e WhatsApp con un solo codice TypeScript. È la stessa lingua del Cancello [verificato: `ricerca/22` §2: "CANCELLO (TypeScript…)"].
- Il **Teams SDK** puro dà il controllo completo sulle carte.

Consiglio il Chat SDK per i messaggi e il Teams SDK per le carte di approvazione, nello stesso servizio [stima: l'adattatore espone il Teams SDK sottostante; da confermare nello spike].

**L'endpoint pubblico.**
- La rotta `/api/messages` va esposta da Traefik e Pangolin nella VLAN 20 EDGE, **senza** il login di Pangolin davanti. Il motivo: Microsoft la chiama con un token firmato (JWT), e il bot lo verifica [stima, da provare].
- Nessun'altra rotta della Porta va esposta.
- L'uscita dalla VLAN 30 APPS va aperta solo verso i domini Microsoft del bot: login e servizio dei messaggi. L'elenco preciso dei nomi è [non verificato]: si ricava nello spike.

### 2.3 Approvare dal telefono con le Adaptive Card

| Fatto | Fonte |
|---|---|
| L'app mobile di Teams supporta le Adaptive Card **fino alla versione 1.6**; oltre, la resa può essere incompleta | [verificato: learn.microsoft.com/…/cards-reference, ms.date 13/10/2026] |
| In Teams non c'è lo stile "positivo" o "distruttivo" dei pulsanti; `isEnabled` di `Action.Submit` non è supportato; niente caricamento di file dalle carte | [verificato: stessa pagina] |
| `Action.Execute` (Universal Actions) gestisce i pulsanti con il bot come unico backend, anche in Outlook. Permette viste per utente (il pulsante "Approva" solo a chi deve approvare) e carte che si aggiornano da sole dopo l'approvazione ("chi ha approvato e quando"). La pagina mostra esempi sia mobile sia desktop | [verificato: learn.microsoft.com/…/universal-actions-for-adaptive-cards/overview, ms.date 30/09/2026] |
| Il Teams SDK ha un gestore `card.action` e una guida con un server MCP che espone `request_approval` (manda una carta con Approva e Rifiuta) e `wait_for_approval` (aspetta la decisione) | [verificato: github.com/microsoft/teams-sdk, guida "mcp-server", 25/10] |
| Nelle attività che arrivano al bot c'è l'identità Entra di chi agisce (`aadObjectId` e nome) | [verificato in parte: risposta di un moderatore Microsoft sui bot single-tenant, techcommunity, estratto; da confermare nello spike] |

**Come lo usiamo.** Un agente non approva mai da solo. Il flusso:
1. L'agente chiama `propose_action` sul Cancello.
2. Il Cancello crea la carta; la Porta la manda nel canale `#approvazioni` o in DM all'approvatore.
3. La persona preme "Approva" sul telefono.
4. La Porta riceve l'azione con l'`aadObjectId` e la passa al Cancello. Il Cancello controlla che quell'identità sia fra gli approvatori della classe:
   - Alessandro per l'outbound e le mail ai clienti;
   - Michele per le offerte e le affermazioni tecniche;
   - Alberto per l'infrastruttura e il codice.

   [verificato: `ricerca/22` §3].
5. L'esecutore agisce una volta sola; la carta si aggiorna per tutti con nome e ora.

La guida MCP del Teams SDK è un buon modello di codice. Nel nostro caso però il "wait" lo fa il Cancello, non l'agente [stima].

**Sicurezza del telefono.** Chi approva lo fa con l'account Entra, quindi con MFA e con le regole di accesso condizionale del tenant [stima]. I telefoni che approvano probabilmente entrano nel perimetro Cyber Essentials, con patch e blocco schermo. Sul punto BYOD: [non verificato, da chiarire con chi certifica].

### 2.4 n8n: nodo Teams e "Send and Wait for Response"

| Fatto | Fonte |
|---|---|
| Operazioni: Channel (crea, elimina, leggi, aggiorna), Channel Message (crea, leggi, rispondi…), Chat Message (crea, leggi, **Send and Wait for Response**…), Task; nelle versioni recenti anche Chat, Chat Member, Online Meeting, Activity Notification | [verificato: docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.microsoftteams, 25/10] |
| Credenziali: Teams OAuth2 (predefinita), Microsoft OAuth2 (Graph) generica, oppure **Service Principal (App-Only)** "with no signed-in user", che però non supporta alcune operazioni. Con OAuth2 le operazioni girano "as the signed-in user" | [verificato: stessa pagina] |
| La credenziale nasce da una registrazione di app in Entra (redirect URI di n8n, client ID, segreto); l'amministratore potrebbe dover dare il consenso | [verificato: docs.n8n.io/integrations/builtin/credentials/microsoft, 25/10] |
| "Send and Wait": tipi Approval, Free Text, Custom Form; tempo massimo di attesa; il flusso riprende quando una persona risponde | [verificato: pagina del nodo Teams] |
| Dalla versione 2.30 (07/07/2026) ogni "Send and Wait", Teams compreso, registra `respondedAt`. **Chi ha risposto**, la lista di chi può approvare e il tocco dentro la chat ci sono **solo per Slack e Telegram** | [verificato: changelog di n8n, docs n8n via Context7] |
| Senza tocco dentro la chat il nodo manda **pulsanti-link** all'URL di ripresa di n8n (`$execution.resumeUrl`), unico per esecuzione | [verificato: documentazione del nodo Telegram e del nodo Wait] |

**Lettura.**
- Su Teams l'approvazione di n8n è un link: chi ce l'ha può aprirlo, e il telefono deve raggiungere n8n (via NetBird, oppure esponendo n8n) [stima].
- Non sapendo chi approva, **non va usata per il Cancello**.
- Va benissimo per gli avvisi del board: "Notifica · Teams o mail con i migliori del giorno" della pipeline dei bandi [verificato: board].
- Con OAuth2 delegato n8n posta **come una persona**, per esempio Alberto. Meglio un utente di servizio (una licenza Business Basic, circa 6,41 € al mese [stima]) oppure far postare la Porta chat.

### 2.5 Altri pezzi di Teams che contano

| Tema | Fatto | Fonte |
|---|---|---|
| Leggere tutto il canale | un bot riceve **tutti** i messaggi di un canale senza @menzione se dichiara il permesso RSC `ChannelMessage.Read.Group` e il proprietario acconsente | [verificato: learn.microsoft.com/…/channel-messages-with-rsc, estratto] |
| Webhook in entrata | i vecchi Office 365 Connectors sono stati **spenti fra il 18 e il 22/05/2026**; li sostituisce Workflows (Power Automate), che però non ha pulsanti interattivi per le MessageCard | [verificato: Message Center MC1181996 su mc.merill.net, estratto; office365itpros.com, 18/09/2026, estratto] |
| Claude dentro Teams | Claude Tag è nato in Slack e "is now coming to Microsoft Teams": lista d'attesa, **nessuna data** | [verificato: claude.com/form/claude-tag-teams-waitlist, 25/10] |
| Connettore M365 di Claude | per i piani Team ed Enterprise legge chat e canali di Teams da claude.ai, dopo l'attivazione dell'amministratore | [non verificato: articoli di terzi da ottobre 2025] |
| Clienti in Teams (B1) | canali condivisi con altre organizzazioni via B2B direct connect (vanno abilitati da entrambe le parti), oppure ospiti; i primi 50.000 utenti esterni attivi al mese sono gratuiti | [non verificato: Microsoft Q&A 2024 e blog di terzi; fonti in parte in contrasto sulle licenze degli ospiti] |
| Hermes con Teams | se Hermes resta, il suo gateway ha già un plugin Teams | [verificato: `ricerca/10` §4] |

### 2.6 Pro e contro di Teams

**Pro.**
- È già pagato.
- L'identità è la stessa di NetBird: Entra, MFA, FIDO2.
- Le app per telefono e computer sono mature, le notifiche arrivano.
- Ci sono carte con pulsanti e identità di chi approva.
- Si possono aprire canali con i clienti.
- Il tenant è già gestito da Michele.

**Contro.**
- Una rotta pubblica in più.
- Una piattaforma di sviluppo che Microsoft cambia spesso: SDK archiviato, connettori spenti, bot multi-tenant fermati [verificato: §2.2 e §2.5].
- Claude Tag non c'è ancora.
- Gli agenti in Teams sono app: un'app e una registrazione per bot. Con 57 agenti conviene **un bot per squadra** (9) o un solo bot che firma la carta con il nome dell'agente [stima].
- I bot non sono un buon canale per far parlare gli agenti fra loro. Lo scambio fra agenti va tenuto nel motore, e Teams lo mostra. Se un bot riceva i messaggi di un altro bot in un canale: [non verificato].

---

## 3. Buzz di Block self-hosted: stato al 25/10/2026

Il rapporto completo è `ricerca/17-buzz.md` del 24/10. Qui c'è solo ciò che è cambiato o che conta per la scelta della chat.

| Voce | Al 25/10/2026 | Fonte |
|---|---|---|
| Repo | 36.438 stelle, 4.822 fork, 3.675 fra issue e PR aperte, ultimo push il 25/10 alle 01:32 UTC, licenza Apache-2.0 | [verificato: api.github.com/repos/block/buzz, 25/10] |
| Ultima release desktop | v0.5.28 del 09/10/2026; nessuna release nelle ultime due settimane | [verificato: API releases, 25/10] |
| Approvazioni nei workflow | ancora **non collegate**: PR #8057 ("suspend request_approval steps and resume them exactly once") aperta, aggiornata il 15/10; PR #7616 (azioni di approvazione nel desktop) aperta | [verificato: API pulls, 25/10] |
| Freno ai giri fra agenti | assente nel codice al 24/10; la #8045 è un'issue aperta su un tema vicino (l'agente che continua ad ascoltare i thread che ha aperto) | [verificato: `ricerca/17` §5; API issues 8045, 25/10] |
| Collegamenti con Teams, Telegram, WhatsApp | **nessuno**. L'issue #4119 "Messaging connectors…" (Slack, Discord, Telegram, Teams) è aperta dal 01/08/2026 con 0 commenti; c'è una PR aperta per un ponte con Slack Connect (#2826), che ora non ci serve | [verificato: API issues e pulls, 25/10] |
| Agenti Claude | l'harness `buzz-acp` parla ACP con Goose, Codex e **Claude Code tramite `claude-agent-acp`** | [verificato: crates/buzz-acp/README.md, 25/10] |
| `claude-agent-acp` | adattatore ACP costruito sull'Agent SDK di Claude in TypeScript | [verificato: zed.dev/docs/ai/external-agents, estratto] |
| App per telefono | iOS e Android; le notifiche passano dal gateway push di Block. Nel repo esiste un crate `buzz-push-gateway`: se si possa ospitare in casa è [non verificato] | [verificato: `ricerca/17` §3; elenco dei crate via API, 25/10] |
| Windows | desktop in alpha, non firmato | [verificato: `ricerca/17` §3] |

**Lettura.** Buzz resta il modello dell'idea: agenti membri veri, con nome e proprietario. Oggi però non regge come chat di tutti, per quattro motivi:
- le approvazioni non funzionano;
- manca il freno ai giri;
- le notifiche dipendono da Block;
- non ha ponti verso Teams, Telegram e WhatsApp.

Ha un aggancio interessante con la scelta di Michele: Claude Code entra in Buzz tramite un adattatore fatto sull'Agent SDK. Va bene come **pilota della "stanza degli agenti"** nella VLAN 90 LAB, su Experimental-2 con Docker, senza dati di clienti, nella fase F5 del board [stima]. Il board dice che LAB non vede DATA [verificato].

---

## 4. Mattermost self-hosted

| Voce | Fatto | Fonte |
|---|---|---|
| Edizioni | Team Edition gratuita (meno di 250 utenti, **SSO rimosso**); **Entry** gratuita (funzioni di Enterprise Advanced con limiti, adatta a meno di 50 utenti); Professional, Enterprise, Enterprise Advanced a pagamento | [verificato: docs.mattermost.com/product-overview/editions-and-offerings, 25/10] |
| Limiti di Entry | cronologia dei canali limitata a **10.000 messaggi** in tutto (i più vecchi restano nel database ma non si vedono né si cercano); 250 domande all'agente AI al mese; chiamate di 40 minuti; **10.000 notifiche push al mese**; il sito dice che i limiti "will take effect in a future release"; solo supporto della community | [verificato: stessa pagina] |
| SSO con Entra ID | nelle funzioni di Professional (anche OpenID Connect, SAML, MFA, ospiti) | [verificato: stessa pagina] |
| Prezzi | il sito non mostra cifre ("Contact Sales"); licenze Professional ed Enterprise "sold as prepaid annual subscriptions" | [verificato: mattermost.com/pricing, 25/10] |
| Prezzo di Professional | 10 $ per utente al mese | [non verificato: TrustRadius, GetApp; una fonte cita un minimo di 11 utenti, non confermato] |
| Notifiche sul telefono | **TPNS gratuito solo per i clienti self-hosted "non commerciali"**, sconsigliato in produzione, senza SLA; HPNS (servizio ospitato da Mattermost) per Professional, Enterprise e Cloud; chi compila le proprie app deve ospitare il proprio push proxy | [verificato: docs.mattermost.com/…/push-notification-server-configuration-settings, 25/10] |
| Bot e pulsanti | account bot; pulsanti interattivi: il server manda un POST all'URL dell'integrazione con `user_id`, canale e post; la risposta può aggiornare il messaggio o mostrare un testo solo a chi ha premuto | [verificato: docs.mattermost.com/developers/integrate/plugins/interactive-messages, 25/10] |
| Pulsanti sul telefono | il changelog dell'app mobile dice che i pulsanti di bot, webhook e plugin funzionano anche su mobile, con lo stesso dialogo del web | [non verificato del tutto: estratto del changelog, versione non indicata] |
| AI | plugin Agents con modelli esterni o in casa, server MCP per sistemi interni; un server MCP ufficiale dalla v11.3 | [verificato: guida admin del plugin Agents, estratto; il server MCP ufficiale è non verificato, blog di terzi di gennaio 2026] |

**Lettura.**
- È la chat self-hosted più matura per un'azienda. I bot e i pulsanti sono semplici da scrivere.
- Per SerSan però ha due nodi:
  - per le notifiche affidabili sul telefono di un'azienda commerciale serve Professional, che usa comunque un servizio cloud di Mattermost, oppure app compilate da noi;
  - sarebbe **una seconda chat** accanto a Teams, che il team ha già.
- La Entry gratuita con 10.000 messaggi di cronologia si riempie presto in una chat con decine di agenti [stima].
- **Piano B** se un giorno si esce da M365 o da Teams.

---

## 5. Matrix con Element e i bridge

| Voce | Fatto | Fonte |
|---|---|---|
| ESS Community | Synapse, Matrix Authentication Service, Element Web, Element Call, Element Admin, Hookshot, PostgreSQL; chart Helm per Kubernetes (K3s suggerito); almeno 2 core e 2 GB; licenza AGPLv3; "We do not recommend using it commercially"; per comunità fino a 100 utenti | [verificato: github.com/element-hq/ess-helm, 25/10] |
| ESS Pro | per ambienti professionali: alta disponibilità, LDAP/SCIM, AuditBot, supporto. Prezzo non rilevato | [verificato: stessa pagina; prezzo non verificato] |
| Pulsanti per i bot | non c'è uno standard: la proposta MSC3006 ("bot interactions") definisce pulsanti che mandano un comando nella stanza; il suo stato di adozione in Element X è [non verificato]. Si approva con reazioni, risposte o sondaggi | [verificato: matrix.org, This Week in Matrix del 13/12/2024, estratto] |
| Ponte Telegram | mautrix-telegram riscritto in Go, release v26.04 di aprile 2026 | [verificato: mau.fi/blog/2026-04-mautrix-release, estratto] |
| Ponte WhatsApp | mautrix-whatsapp usa il protocollo di WhatsApp Web (multi-device), non l'API ufficiale. I suoi documenti dicono che il blocco è più probabile con attività sospette; per terzi viola i termini di WhatsApp | [verificato: documentazione di autenticazione di mautrix-whatsapp, estratto; violazione dei termini: non verificato, blog commerciale di luglio 2026] |
| Notifiche | le app Element dagli store usano i servizi push di Apple e Google tramite un gateway; dettagli per Element X [non verificato] | [non verificato: forum YunoHost] |

**Lettura.**
- È la scelta più sovrana: federata e cifrata.
- Ma richiede Kubernetes e non ha pulsanti standard.
- Il ponte WhatsApp non è ufficiale.
- Element sconsiglia la versione gratuita per uso commerciale.
- Per quattro persone che hanno già Teams è troppo lavoro per troppo poco. **Non consigliato** [stima].

---

## 6. Telegram e WhatsApp in modo ufficiale

### 6.1 Telegram: Bot API

| Fatto | Fonte |
|---|---|
| Ultima versione Bot API **10.3 del 24/08/2026** | [verificato: core.telegram.org/bots/api, 25/10] |
| Due modi per ricevere: `getUpdates` (long polling, **solo in uscita**) oppure webhook HTTPS sulle porte 443, 80, 88 o 8443; non insieme | [verificato: stessa pagina e core.telegram.org/bots/faq] |
| Webhook con certificato self-signed ammesso se si carica la chiave pubblica | [verificato: bots/faq] |
| Limiti: in una chat non più di un messaggio al secondo; nei gruppi 20 al minuto; in tutto circa 30 al secondo | [verificato: bots/faq] |
| Costo: "bots are able to message their users at no cost"; si pagano solo i broadcast oltre i 30 messaggi al secondo | [verificato: bots/faq] |
| n8n: "Send and Wait" su Telegram con tocco dentro la chat, registra chi ha risposto e limita chi può approvare; serve n8n raggiungibile in HTTPS pubblico su una porta ammessa; altrimenti torna ai pulsanti-link | [verificato: changelog e documentazione di n8n] |
| Chat SDK: adattatore Telegram con modalità `polling` e lista degli utenti ammessi (`allowedUserIds`) | [verificato: README di `adapter-telegram`, 25/10] |
| I bot non possono scrivere per primi a chi non li ha avviati; i messaggi con i bot non sono cifrati end-to-end e stanno sui server di Telegram | [non verificato] |

**Uso consigliato.**
- Solo **avvisi senza contenuto** ("c'è una carta in attesa, apri Teams") e, per chi lo vuole, il debrief in forma breve con soli dati verdi.
- Long polling dalla Porta: nessuna porta aperta. Basta aggiungere `api.telegram.org` all'allowlist d'uscita della VLAN APPS [stima].
- **Niente approvazioni del Cancello su Telegram**: l'identità è un ID Telegram, non Entra con MFA [stima].

### 6.2 WhatsApp: Cloud API di Meta

| Fatto | Fonte |
|---|---|
| Dal 01/07/2025 Meta fa pagare **a messaggio** consegnato, secondo categoria e paese del destinatario. I messaggi degli utenti verso l'azienda non si pagano | [verificato: developers.facebook.com/documentation/business-messaging/whatsapp/pricing, 25/10] |
| Categorie: template marketing, utility, authentication (inviabili sempre); service (solo come risposta entro 24 ore) | [verificato: stessa pagina] |
| **Dal 01/10/2026**: primi **1.000 messaggi di servizio al mese per numero** gratuiti, senza riporto; dal 1.001° si paga; anche le utility dentro la finestra di 24 ore diventano a pagamento; senza metodo di pagamento i messaggi oltre la soglia non partono | [verificato: stessa pagina] |
| L'Italia ha una tariffa propria nel listino (file CSV o PDF in euro); la tariffa marketing per l'Italia è salita dal 01/07/2026 | [verificato: stessa pagina; importi non letti] |
| Tariffa utility per l'Italia: circa 0,0248 € a messaggio (altre fonti 0,030-0,0375 $) | [non verificato: guide di terzi in contrasto fra loro] |
| Pulsanti di risposta: fino a **3** per messaggio; la scelta arriva al webhook `messages` | [verificato: developers.facebook.com/…/interactive-reply-buttons-messages, estratto] |
| Webhook: URL di callback HTTPS pubblico, token di verifica, firma con l'App Secret | [verificato: README di `adapter-whatsapp` del Chat SDK, 25/10] |
| n8n: nodo WhatsApp Business Cloud con "Send and Wait" | [verificato: docs n8n, canali di approvazione] |
| Regola di Meta sui chatbot AI generici: annunciata a ottobre 2025, sospesa in Italia dall'AGCM a dicembre 2025, contestata dalla Commissione europea a febbraio 2026; a marzo 2026 Meta ha detto che per 12 mesi li supporta in Europa. I bot di un'azienda per i propri clienti non erano toccati | [non verificato: TechCrunch del 24/12/2025, MediaNama di marzo 2026] |

**Uso consigliato.**
- WhatsApp serve soprattutto **verso i clienti**: assistenza (L5), messaggi della pagina (L8), intake (K5). Ogni messaggio in uscita passa dal Cancello.
- Per il team interno costa a messaggio e porta i dati da Meta. Il debrief su WhatsApp va fatto solo per chi lo chiede, con un template utility e soli dati verdi.
- **Niente approvazioni sul numero di telefono** [stima].
- Il webhook entra da Pangolin e Traefik nella VLAN EDGE, sulla rotta `/webhooks/whatsapp`.
- Servono anche: un numero dedicato, un portafoglio Meta Business, i template approvati e un DPA con Meta [stima].
- **Mai ponti non ufficiali** (mautrix-whatsapp, librerie "WhatsApp Web").

### 6.3 Da n8n o dal motore?

| Lavoro | Dove | Perché |
|---|---|---|
| Avviso giornaliero dei bandi in Teams | n8n (nodo Teams) o la Porta | è un messaggio senza decisioni [stima] |
| Approvazioni del Cancello | la Porta (Teams) | serve l'identità Entra di chi approva; n8n su Teams non la registra [verificato: §2.4] |
| Conversazioni con gli agenti (Teams, Telegram, WhatsApp) | la Porta, con il Chat SDK | un solo codice, un solo freno, un solo registro [stima] |
| Avvisi Telegram semplici | n8n o la Porta | entrambi vanno; il tocco in chat di n8n chiede un webhook pubblico, la Porta in polling no [verificato: §6.1] |

---

## 7. Confronto

| Criterio | **Teams + Porta** | Buzz | Mattermost | Matrix + Element | Telegram / WhatsApp |
|---|---|---|---|---|---|
| Già pagato o licenza | già in M365 (0 € in più) [stima] | Apache-2.0, 0 € | Professional circa 10 $/utente/mese [non verificato]; Entry gratis con limiti | AGPLv3, 0 €; Pro a preventivo | gratis / a messaggio |
| Rispetta "Azure esce" | sì con Teams-managed; con Azure Bot F0 solo un registro gratuito | sì | sì | sì | sì |
| Rispetta "resto self-hosted" | la Porta è in casa; la chat è nel cloud M365 ammesso dal board | sì; notifiche via Block | sì; notifiche via servizio Mattermost o app nostre | sì; notifiche via gateway Apple e Google | no: sono servizi cloud, usati solo come canali |
| Identità Entra e MFA | sì, nativa | no (chiavi Nostr) | solo da Professional | sì via OIDC (MAS) [non verificato per Entra] | no |
| App per telefono e notifiche | mature | iOS e Android giovani | mature, ma push di produzione a pagamento | mature | mature |
| Pulsanti per approvare dal telefono | sì (Adaptive Card 1.6) | approvazioni rotte | sì | nessuno standard | sì (inline keyboard; 3 pulsanti WhatsApp) |
| Chi ha premuto | sì, `aadObjectId` [da confermare nello spike] | n.d. | sì, `user_id` | sì, mittente della reazione | ID Telegram o numero |
| Agenti come membri | un'app per bot; meglio un bot per squadra | sì, nativo | account bot | utenti bot | un bot per numero o token |
| Ponti verso Telegram e WhatsApp | dalla Porta (Chat SDK) | nessuno | via plugin o Porta | mautrix (WhatsApp non ufficiale) | n.a. |
| Clienti esterni (B1) | canali condivisi o ospiti | inviti e chiavi | ospiti (Professional) | federazione | sì |
| Maturità | alta (piattaforma che cambia spesso) | pre-1.0 | alta | alta, ma pesante | alta |
| Lavoro per SerSan | 8-11 gp [stima, §9] | pilota 3-5 gp [stima] | 5-8 gp più gestione [stima] | 8-12 gp più Kubernetes [stima] | 0,5-1 gp Telegram; 3-5 gp WhatsApp [stima] |
| Verdetto | **chat di gruppo** | pilota in LAB (F5) | piano B | no | canali secondari |

---

## 8. Raccomandazione

### 8.1 Lo schema

```
PERSONE (4) ─ Microsoft Teams (M365, Entra + MFA), computer e telefono
              team "SerSan Agent OS": #approvazioni · #agenti · #ingresso · #call-vendita
              · #bandi · un canale per squadra · canali condivisi con i clienti (B1)
            ─ Telegram (facoltativo): solo "c'è una carta in attesa", mai il testo
            ─ WhatsApp (fase clienti): numero aziendale, Cloud API, tutto via Cancello
                │ HTTPS firmato da Microsoft (JWT)        ▲ long polling in uscita (Telegram)
══ OPNsense ══ VLAN 20 EDGE: Traefik + Pangolin, rotte pubbliche: /api/messages
              (poi /webhooks/whatsapp); nient'altro della Porta è esposto
VLAN 30 APPS  PORTA CHAT (TypeScript: Chat SDK + Teams SDK): Teams, Telegram, poi WhatsApp
              MOTORE (Agent SDK di Claude): squadre, sessioni, freno ai giri, scambi fra agenti
              CANCELLO: carte, approvatori per classe, registro, esecutori
              n8n: avvisi semplici (bandi), mai approvazioni del Cancello
              LiteLLM → API Anthropic
VLAN 40 DATA  PostgreSQL 16: stato della Porta, registro delle carte
VLAN 90 LAB   pilota Buzz su Experimental-2 (nessun dato di clienti)
```

Le VLAN e i servizi sono quelli del board [verificato: `board-vlan.txt`]. La posizione della Porta in APPS è una mia proposta [stima].

### 8.2 Come funziona, caso per caso

1. **Una persona chiede a un agente.** Alessandro scrive "@Outreach prepara il follow-up per X" nel canale della squadra. La Porta passa il messaggio al motore, che apre o riprende la sessione della squadra. La risposta arriva nel thread. Il testo che arriva dalla chat è trattato come input non fidato, come nella corsia `#ingresso` [verificato: `ricerca/22` §2].
2. **Un agente vuole far uscire qualcosa.** Il flusso del §2.3: carta, sì di una persona autorizzata dal telefono, esecutore una volta sola, carta aggiornata.
3. **La stanza degli agenti (A7).** Gli agenti si passano il lavoro nel motore, dove sta il freno ai giri. La Porta rispecchia i passaggi in `#agenti`, con il nome dell'agente in testa alla carta. Le persone leggono e intervengono con una @menzione. È la stessa idea di Buzz, con il freno e le approvazioni nostri [stima].
4. **Bandi.** n8n, ogni notte, posta i migliori del giorno in `#bandi`, come nel board [verificato: board].
5. **Clienti (B1).** Il recap va nel canale condiviso del cliente solo dopo la carta approvata. Se il cliente non usa Teams: ospite, mail o WhatsApp, sempre dal Cancello.
6. **Telegram e WhatsApp (J9).** Sono la stessa Porta e gli stessi agenti. Su questi canali arrivano solo dati verdi e avvisi; le decisioni restano in Teams.

### 8.3 In che ordine, sulla roadmap del board

| Fase del board | Lavoro sulla chat | gp [stima] |
|---|---|---|
| F1-F2 (fondamenta, via da Azure) | Team e canali in Teams; criteri per le app personalizzate nel tenant; **spike di un giorno**: bot Teams-managed con la CLI del Teams SDK, risposta, messaggio proattivo e carta premuta dal telefono attraverso Pangolin. Se dà 401: Azure Bot F0 oppure piano B (decide Michele) | 1 |
| F4 (AI + bandi) | Porta chat con Chat SDK e Teams SDK; carte del Cancello con `Action.Execute`, controllo dell'`aadObjectId`, scadenza e registro; avviso dei bandi; rotta `/api/messages` con allowlist d'uscita | 7-9 |
| F4-F5 | Avvisi Telegram in polling, per chi li vuole | 0,5-1 |
| Dopo il collaudo del Cancello con dati veri | WhatsApp per i clienti: Meta Business, numero, template, webhook, carte | 3-5, più l'attesa delle verifiche di Meta |
| F5 (lab) | Pilota Buzz in LAB con 3-5 agenti via `claude-agent-acp` | 3-5 |

### 8.4 Che cosa cambia rispetto a `ricerca/22` e alla presentazione

- **Slack Pro esce**: −27,00 € al mese. **Claude in Slack esce**: −44,67 € al mese, finché Claude Tag non arriva in Teams [verificato: `ricerca/22` §9; lista d'attesa §2.5].
- Le "carte in Slack" (4 gp nella fase 1 [verificato: `ricerca/22` §5]) diventano carte in Teams, con un costo simile [stima].
- "Un bot Slack per agente" diventa **un bot per squadra in Teams** [stima].
- Il Socket Mode senza porte diventa una rotta pubblica firmata (§1).
- Le frasi della presentazione su Slack come "chat di partenza" e su "Telegram e WhatsApp tramite Hermes" vanno aggiornate: Teams è la chat, Telegram e WhatsApp passano dalla Porta.
- Alessandro perde per ora "chiedere a @Claude in Slack". Al suo posto:
  - il connettore M365 di Claude Team, che legge Teams da claude.ai [non verificato];
  - il nostro bot, che risponde su dati verdi tramite il motore [stima].

---

## 9. Costi

**Mensili** (rilevati il 25/10/2026, IVA esclusa)

| Voce | € al mese | Fonte |
|---|---|---|
| Teams dentro il piano M365 attuale | **0** in più | [stima: piano attuale non nei file] |
| Registrazione del bot Teams-managed | 0 | [verificato: §2.2] |
| Riserva Azure Bot F0 | 0 (canale Teams senza limiti) | [verificato: §2.2] |
| Teams SDK, Chat SDK | 0 (open source, MIT) | [verificato: §2.2] |
| Utente di servizio per n8n (solo se si posta come utente) | 6,41 (Business Basic £5,40) | [non verificato sulla pagina Microsoft: §2.1] |
| Telegram Bot API | 0 | [verificato: §6.1] |
| WhatsApp verso i clienti (fase successiva) | a consumo: 1.000 messaggi di servizio gratis al mese; per esempio 300 template utility al mese costano circa 7-12 € | [stima su tariffe di terzi non verificate, §6.2] |
| Pilota Buzz | 0 di licenza | [verificato: `ricerca/17` §10] |
| **Totale fisso consigliato** | **0** (6,41 con l'utente di servizio) | |
| Risparmio sul piano precedente | **−71,67** (Slack Pro 27,00 più Claude in Slack 44,67) | [verificato: `ricerca/22` §9] |
| Alternativa Mattermost Professional, 4 utenti | circa 35,74 (4 × 10 $), forse di più se c'è un minimo di posti | [non verificato: §4] |
| Alternativa Matrix ESS Community | 0 di licenza, sconsigliata per uso commerciale | [verificato: §5] |

**Una tantum, in tempo** [stima]

| Lavoro | gp |
|---|---|
| Spike registrazione e prova dal telefono | 1 |
| Porta chat: messaggi, menzioni, thread, specchio di `#agenti`, stato in Postgres | 3-4 |
| Carte del Cancello in Teams | 3-4 |
| Rotta pubblica, allowlist d'uscita, avvisi del monitoraggio | 0,5-1 |
| Avvisi Telegram | 0,5-1 |
| **Totale Teams più Telegram** | **8-11** |
| WhatsApp clienti (dopo) | 3-5 |
| Pilota Buzz (F5) | 3-5 |

**Risorse sul server** [stima]: la Porta occupa 0,5-1 GB di RAM in APPS. Il board lascia circa 53 GB liberi [verificato: board]. Buzz in LAB chiede 4-8 GB [verificato: `ricerca/17` §7, stima di quel rapporto].

---

## 10. Rischi

| Rischio | Probabilità | Impatto | Mitigazione |
|---|---|---|---|
| Il bot Teams-managed non manda messaggi (401) | media [verificato: segnalazioni §2.2] | medio | spike nella fase F1-F2; riserva Azure Bot F0 (0 €) o piano B senza bot |
| Microsoft cambia ancora la piattaforma (SDK archiviato, connettori spenti, multi-tenant fermato) | alta [verificato: §2.2, §2.5] | medio | Teams SDK attuale, versioni fissate, una sola Porta da aggiornare |
| La rotta pubblica `/api/messages` attaccata | media | medio | verifica del JWT, limite di frequenza, CrowdSec, nessun'altra rotta esposta, log in Loki e Wazuh |
| Approvazione data dalla persona sbagliata o da un agente | bassa | alto | `aadObjectId` contro la lista per classe nel Cancello; carte con scadenza; mai approvazioni da identità di agenti [verificato: regola di `ricerca/22` §3] |
| Dati rossi nella chat cloud | media | alto | in Teams solo riassunti e campi; trascrizioni e mail intere restano sul server; tre colori del Cancello [verificato: `ricerca/22` §2] |
| Giri fra agenti che bruciano token | media | medio | freno nel motore, non nella chat; tetti per agente in LiteLLM |
| Iniezioni da messaggi della chat o di WhatsApp | media | alto | input non fidato; chi legge testo esterno non ha strumenti d'azione |
| WhatsApp: regole e prezzi di Meta che cambiano; numero bloccato con ponti non ufficiali | media | medio | solo Cloud API ufficiale; tetto di spesa; template approvati |
| Telegram fuori da Entra | certa | basso | solo avvisi verdi, nessuna approvazione |
| Telefoni personali nel perimetro Cyber Essentials | da chiarire | medio | patch entro 14 giorni, blocco schermo, eventuale accesso condizionale [non verificato] |
| Dipendenza da Microsoft per la chat | certa | medio | Porta con il Chat SDK (cambiare canale è cambiare adattatore); Mattermost come piano B |

---

## 11. Domande aperte

1. **Piano M365 di SerSan.** Quale piano ha (Basic, Standard, Premium), con quanti posti, e Teams è compreso? Chi è amministratore di Teams?
2. **Azure Bot.** Se il bot Teams-managed non funziona, Michele accetta una registrazione Azure Bot gratuita (F0, nessuna risorsa che gira) o preferisce il piano B senza bot?
3. **App personalizzate.** Il tenant permette di caricare app Teams personalizzate solo per l'organizzazione?
4. **Rotta pubblica.** Dove termina Pangolin: in casa con l'IP fisso da richiedere, o altrove? Quale nome DNS su Cloudflare per il bot?
5. **Clienti.** I clienti usano Teams (canali condivisi) o servono ospiti? Per quali casi vogliamo WhatsApp, e chi approva i template di Meta?
6. **Telegram.** Qualcuno lo vuole davvero? Se nessuno, si salta.
7. **Buzz.** Ora che Teams fa da finestra sulla stanza degli agenti, il pilota in LAB serve ancora o si rimanda?
8. **Approvatori.** Confermate le classi di `ricerca/22` §3: Alessandro outbound e mail ai clienti, Michele offerte e affermazioni tecniche, Alberto infrastruttura e codice?
9. **BYOD.** I telefoni personali che approvano entrano nel perimetro Cyber Essentials? Serve una regola di accesso condizionale per Teams sul telefono?

---

## Fonti

Locali:
- `C:\Users\alber\SerSan-AgentOS\allegati\infra\SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt` (board di Michele, vincolante)
- `C:\Users\alber\SerSan-AgentOS\ricerca\00-visione-funzionalita.md` (J9, A7, B1)
- `C:\Users\alber\SerSan-AgentOS\ricerca\10-hermes-agent.md` §4 (plugin di piattaforma)
- `C:\Users\alber\SerSan-AgentOS\ricerca\17-buzz.md` (rapporto su Buzz del 24/10)
- `C:\Users\alber\SerSan-AgentOS\ricerca\22-architettura-scelta.md` §2, §3, §5, §9
- `C:\Users\alber\SerSan-AgentOS\PRESENTAZIONE-CEO.md` §4.11 (testo da aggiornare)

Web, rilevato il 25/10/2026:
- Teams, bot e registrazione:
  - https://microsoft.github.io/teams-sdk/cli/concepts/bot-locations/
  - https://learn.microsoft.com/en-my/answers/questions/5706215/teams-bot-not-receiving-messages-when-using-a-self
  - https://learn.microsoft.com/en-nz/answers/questions/5650695/single-tenant-teams-bot-dev-portal-only-gets-401-u
  - https://learn.microsoft.com/azure/bot-service/abs-quickstart (estratto)
  - https://azure.microsoft.com/en-gb/pricing/details/bot-services/
  - https://docs.azure.cn/en-us/bot-service/bot-service-overview (estratto)
  - https://devblogs.microsoft.com/microsoft365dev/python-support-for-the-microsoft-teams-sdk-is-now-generally-available/
  - https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/build-and-test/tool-sdk-overview (estratto)
- Teams, carte e canali:
  - https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-reference
  - https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/universal-actions-for-adaptive-cards/overview
  - https://github.com/microsoft/teams-sdk (guide "executing-actions" e "mcp-server", via Context7)
  - https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc (estratto)
  - https://mc.merill.net/message/MC1181996 e https://office365itpros.com/2026/09/18/teams-workflows-updates/ (estratti)
  - https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/build-and-test/teams-developer-portal
- Claude in Teams:
  - https://claude.com/form/claude-tag-teams-waitlist
  - https://winbuzzer.com/2026/07/01/anthropic-eyes-claude-agent-for-microsoft-teams-xcxwbn/ (terzi)
- Licenze M365 (fonti di terzi):
  - https://nerdster.co.uk/insights/microsoft-365-price-changes-2026/
  - https://amvia.co.uk/blog/office-365-price
  - https://office-watch.com/2026/microsoft-365-business-price-increase-2026/
  - https://www.uctoday.com/unified-communications/microsoft-365-prices-rise-on-1-july-what-it-teams-need-to-do-before-the-deadline/
  - pagina Microsoft UK non raggiunta (timeout): https://www.microsoft.com/en-gb/microsoft-365/business/compare-all-microsoft-365-business-products
- Cambio sterlina:
  - https://www.poundsterlinglive.com/bank-of-england-spot/historical-spot-exchange-rates/gbp/GBP-to-EUR-2026
- n8n:
  - https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.microsoftteams/
  - https://docs.n8n.io/integrations/builtin/credentials/microsoft/
  - documentazione n8n-docs via Context7: changelog 2.30, nodo Wait, nodo Telegram, human-in-the-loop
- Chat SDK di Vercel:
  - https://github.com/vercel/chat e i README di `packages/adapter-teams`, `adapter-telegram`, `adapter-whatsapp`
- Buzz:
  - https://api.github.com/repos/block/buzz (repo, releases, pulls 8057 e 7616, issues 8045 e 4119, pulls 2826, contenuto di `crates`)
  - https://raw.githubusercontent.com/block/buzz/main/crates/buzz-acp/README.md
  - https://zed.dev/docs/ai/external-agents (estratto)
- Mattermost:
  - https://docs.mattermost.com/product-overview/editions-and-offerings.html
  - https://docs.mattermost.com/administration-guide/configure/push-notification-server-configuration-settings.html
  - https://mattermost.com/pricing/
  - https://docs.mattermost.com/developers/integrate/plugins/interactive-messages
  - https://docs.mattermost.com/product-overview/mobile-app-changelog (estratto)
  - https://docs.mattermost.com/configure/agents-admin-guide.html (estratto)
  - https://www.trustradius.com/products/mattermost/pricing (terzi)
- Matrix:
  - https://github.com/element-hq/ess-helm
  - https://matrix.org/blog/2024/12/13/this-week-in-matrix-2024-12-13/ (estratto)
  - https://mau.fi/blog/2026-04-mautrix-release/ (estratto)
  - https://git.sudo.is/matrix/mautrix-docs/src/branch/auth-page-link/bridges/go/whatsapp/authentication.md (estratto)
- Telegram:
  - https://core.telegram.org/bots/api
  - https://core.telegram.org/bots/faq
- WhatsApp:
  - https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
  - https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-reply-buttons-messages (estratto)
  - https://techcrunch.com/2025/12/24/italy-tells-meta-to-suspend-its-policy-that-bans-rival-ai-chatbots-from-whatsapp/ (terzi)
  - https://www.medianama.com/2026/03/223-meta-pauses-block-ai-chatbots-whatsapp/ (terzi)
  - https://sendapp.live/en/2025/08/04/how-much-does-whatsapp-business-api-cost-in-italy-complete-guide/ (terzi, tariffe italiane)
