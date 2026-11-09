# 35 · Giudizio di sicurezza e privacy sulle tre proposte

**Data:** 25/10/2026. **Lente:** sicurezza e privacy. Guardo il perimetro Cyber Essentials, il GDPR, i dati che escono (solo verso Claude e i SaaS del board), le iniezioni di istruzioni, le approvazioni e il registro, la superficie d'attacco di ogni componente e le vulnerabilità note.
**Giudica:** `34-proposta-1-agent-sdk.md` (sdk), `34-proposta-2-hermes-self-hosted.md` (hermes), `34-proposta-3-claude-team-e-mcp.md` (teammcp).
**Vincoli:** il board di Michele è vincolante (`allegati/infra/`). Sopra tutto vale la regola di Alberto: nessuna funzione A1-L12 e nessuna integrazione si toglie o si declassa perché oggi manca un componente. Una proposta che declassa perde punti sulla visione.
**Fonti:** le tre proposte lette per intero; il board; `00-visione-funzionalita.md`; i rapporti 16, 25, 26, 27 e 29; le pagine web lette oggi, elencate in fondo. Context7 oggi risponde "Monthly quota reached" [verificato: risposta di Context7 del 25/10/2026]: la documentazione l'ho letta con WebFetch sulle pagine ufficiali.
**Etichette:** [verificato: fonte] = letto oggi nella fonte indicata; [non verificato] = stima, giudizio mio o fonte di terzi non confermata. gp = giorni-persona. Prezzi IVA esclusa, rilevati il 24-25/10/2026.

---

## In breve

**Vince la Proposta 1 (motore sull'Agent SDK), di mezzo punto sulla Proposta 3.** Per la mia lente la differenza vera sta nella sicurezza: 8 contro 6. La Proposta 1 mette il controllo degli effetti nel punto giusto: un hook del motore che nega per primo, un elenco chiuso di strumenti, nessuno strumento che invia, l'identità della persona passata all'MCP RAG, una sola rotta pubblica per il bot e una VLAN propria per gli agenti. La Proposta 3 dà valore prima e con meno pezzi accesi, ma porta più lavoro e più dati dentro Claude Team, che sul piano Team non ha log di audit, conservazione personalizzata né Compliance API [verificato: claude.com/pricing/team, 25/10/2026]. In più espone sei endpoint MCP su internet invece di uno. La Proposta 2 (Hermes) resta molto indietro: il gateway unico ha 276 problemi aperti, 9 di sicurezza e 0 risolti su `main` [verificato: API GitHub, issue #143547, aggiornata il 25/10/2026 alle 14:54 UTC], e l'identità verso l'MCP RAG vale per istanza, non per persona [verificato: docs MCP di Hermes].

Ho trovato anche due difetti tecnici nella Proposta 1 che vanno corretti prima della fase B (§8). Il primo: nella modalità `dontAsk` uno strumento MCP marcato `requiresUserInteraction` viene sempre negato, anche dopo un "allow" dell'hook [verificato: code.claude.com/docs/en/agent-sdk/permissions]. La combinazione scritta nella proposta quindi blocca anche le azioni approvate. Il secondo: un hook a comando che va in timeout su `PreToolUse` non blocca lo strumento, salvo `onFailure: "block"` [verificato: code.claude.com/docs/en/hooks]. Il guardrail va scritto come hook di callback del motore, che invece blocca allo scadere del tempo [verificato: idem].

---

## 1. Punteggi (0-10)

| Proposta | Visione | Tempo al valore | Costo | Affidabilità e manutenzione | Sicurezza e privacy | Aderenza al board | Totale |
|---|---|---|---|---|---|---|---|
| **1 · Agent SDK** | 9 | 6 | 5,5 | 6,5 | **8** | 7,5 | **42,5** |
| 3 · Claude Team e MCP | 7 | 8 | 7 | 6 | 6 | 8 | 42 |
| 2 · Hermes in casa | 8,5 | 6 | 6 | 4 | 4,5 | 5 | 34 |

[non verificato: giudizio mio, costruito sui fatti dei §2-§7]

Come ho dato i voti, in breve:
- **Visione.** La 1 dà un componente a tutte le 90 voci e scrive le lacune con il costo. La 2 fa lo stesso, ma con l'identità per istanza G4 ("il report va a chi ha fatto la call") non lo garantisce il sistema. La 3 copre tutto solo con le aggiunte A-G, e trasforma 10 delle 57 figure in "persona più skill in Claude Team" (tipo T): per la regola di Alberto è un declassamento degli agenti, quindi perde punti [non verificato: giudizio].
- **Tempo al valore.** Conto il valore lecito: sui dati dei clienti solo dopo Cancello, DPIA e registro. La 3 dà valore dalla prima settimana senza server. La 2 non può mettere dati rossi in Hermes finché non escono la v0.23 e le correzioni di sicurezza [verificato: proposta 2 §10.3, che cita ricerca/27 §11].
- **Costo.** Il mensile è quasi uguale nelle tre. Cambiano i gp (290, 227,5 e 254 con la riserva) e la RAM: la 1 e la 2 comprano +192 GB, la 3 forse no (ma vedi §7).
- **Affidabilità.** La 2 paga il ritmo di Hermes: 44 release dal 12/3 al 23/10/2026 e note incomplete per scelta [verificato: ricerca/27 §8]. La 3 dipende da funzioni in anteprima: i compiti programmati sono "in research preview" [verificato: code.claude.com/docs/en/routines].
- **Board.** La 3 è il disegno letterale del board ("Claude Team ragiona sul RAG via MCP"). La 1 segue la richiesta di Michele di valutare l'Agent SDK, ma aggiunge tre VLAN e anticipa RAM e GPU. La 2 porta Hermes, che Michele preferirebbe evitare [verificato: messaggio di Michele del 25/10/2026].

---

## 2. Cosa ho verificato oggi

| Affermazione delle proposte | Esito | Fonte |
|---|---|---|
| Hermes: gateway unico con 276 problemi aperti, 9 di sicurezza, 0 risolti su `main`, 39 in revisione in 14 PR (Proposta 2) | Confermato. La Proposta 1 scrive ancora 273: dato di ieri | [verificato: api.github.com/repos/NousResearch/hermes-agent/issues/143547, 25/10/2026] |
| Hermes: `identity_header` manda un valore fisso o il nome del profilo, "resolved once at connect time" | Confermato | [verificato: hermes-agent.nousresearch.com/docs/user-guide/features/mcp] |
| Hermes: `pre_tool_call` "fails closed" allo scadere del tempo | Confermato, con un punto aperto: "A hung callback is skipped for a 60s suppression window". La pagina non dice se in quei 60 secondi gli strumenti sono bloccati o passano | [verificato: hermes-agent.nousresearch.com/docs/user-guide/features/hooks] |
| Hermes in Buzz: il ponte risponde da solo `allow_once`; `approvals.mode: manual` non aiuta | Confermato | [verificato: hermes-agent.nousresearch.com/docs/user-guide/features/acp] |
| Agent SDK: intestazioni HTTP per server MCP decise da noi a ogni `query()` | Confermato: campo `headers`. L'SDK non fa il giro OAuth: il token lo passa la nostra app | [verificato: code.claude.com/docs/en/agent-sdk/mcp] |
| Agent SDK: le regole deny valgono anche in `bypassPermissions` | Confermato | [verificato: code.claude.com/docs/en/agent-sdk/permissions] |
| Agent SDK: `dontAsk` più `propose_action` con `requiresUserInteraction` | **Problema.** In `dontAsk` gli strumenti che chiedono interazione "are denied instead", anche se una regola o un hook li consente | [verificato: idem] |
| Hook `PreToolUse`: cosa succede in timeout | Un hook di callback dell'SDK in timeout blocca lo strumento. Un hook a comando, HTTP o MCP in timeout non lo blocca, salvo `onFailure: "block"` | [verificato: code.claude.com/docs/en/hooks] |
| `defer` e ripresa | Funziona solo con una chiamata di strumento per turno; alla ripresa l'hook viene richiamato; "`-p` resume doesn't restore the stored permission mode"; le sessioni restano su disco 30 giorni di default (`cleanupPeriodDays`) | [verificato: code.claude.com/docs/en/hooks] |
| Claude Team: niente log di audit, niente conservazione personalizzata, niente SCIM, niente Compliance API | Confermato. Il rapporto 16 (riga 158) diceva che l'amministratore imposta la conservazione: oggi la pagina la mette solo in Enterprise | [verificato: claude.com/pricing/team, 25/10/2026] |
| Connettori personalizzati: partono dal cloud di Anthropic; un server dietro firewall non si raggiunge | Confermato. La stessa pagina avverte che server malevoli possono iniettare istruzioni | [verificato: support.claude.com, articolo 11175166] |
| IP di uscita di Anthropic `160.79.104.0/21` | Confermato. Sono gli IP di tutto il servizio, quindi provano che la richiesta viene da Anthropic, non da SerSan | [verificato: platform.claude.com/docs/en/api/ip-addresses] |
| Compiti programmati di Claude Code: di una sola persona, "appears as you", non più di uno all'ora | Confermato. In più: girano in "auto mode" con un classificatore, e includono di default tutti i connettori, "including writes" | [verificato: code.claude.com/docs/en/routines] |
| LiteLLM: versioni compromesse su PyPI | Confermato: 1.82.7 e 1.82.8 del 24/03/2026, con furto di credenziali | [verificato: netspi.com, blog "LiteLLM Supply Chain Compromise"; fonte di terzi] |
| MinIO "archiviato dal 12/02/2026" | Quasi: dal 12/02/2026 "non più mantenuto", archiviato il 25/04/2026; immagini container ferme da ottobre 2025 | [non verificato: pinggy.io e blog.vonng.com, fonti di terzi] |
| VPS Hetzner "da 6,49 €" (Proposta 3) | La pagina oggi dice "€ 5.99 per month, excl. VAT" (linea Cost-Optimized). I 6,49 € includono forse l'indirizzo IPv4 | [verificato: hetzner.com/cloud, 25/10/2026]; IPv4 [non verificato] |

---

## 3. Le tre proposte con la lente della sicurezza

### 3.1 Proposta 1 · Agent SDK: 8 su 10

**Cosa regge.**
- Il controllo degli effetti è nel motore, non nel modello. L'ordine dei permessi parte dagli hook, poi le regole deny, che valgono anche in `bypassPermissions` [verificato: docs permissions]. Gli agenti non hanno strumenti che inviano [verificato: proposta 1 §1].
- Isolamento per famiglia: `settingSources: []`, `CLAUDE_CONFIG_DIR` e `cwd` separati, e in TypeScript l'opzione `env` sostituisce l'ambiente, quindi il processo non vede le chiavi del motore [verificato: ricerca/26 §3.4].
- Rete stretta: VLAN 32 nuova con uscita solo verso LiteLLM, MCP e Cancello; WebFetch spento, il web passa da Firecrawl; traffico non essenziale spento con `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` [verificato: proposta 1 §3.4; ricerca/26 §3.7].
- Testo di terzi (mail, trascrizioni, pagine, messaggi dei clienti) letto da una sessione senza strumenti d'azione, con uscita a schema [verificato: proposta 1 §5.1, punto 5]. È lo schema giusto contro le iniezioni.
- Identità della persona verso l'MCP RAG con un token firmato dal runner [verificato: proposta 1 §4.2]. Così i permessi per utente del board valgono anche per gli agenti.
- Un solo bot Teams per le carte (nove solo se lo chiedono le persone nella fase D) [verificato: proposta 1 §5.5].
- Verifica alla settimana 11 con criteri misurabili, compreso "nessun effetto esce senza una carta" e l'aggiornamento dell'SDK entro 14 giorni [verificato: proposta 1 §7.4].

**Cosa non regge ancora.**
- La combinazione `dontAsk` più `requiresUserInteraction` nega sempre `propose_action` (§2). Il difetto è sicuro, perché nega, ma rompe il flusso delle carte.
- Se il guardrail sta in un plugin con hook a comando, un timeout lascia passare lo strumento nel flusso normale (§2). La proposta non lo dice.
- Molto codice di sicurezza è nostro e nuovo: Cancello 17,5 gp, Porta 14,75 gp, runner, ponte e bacheca circa 9,5 gp, MCP e identità circa 11,75 gp [verificato: proposta 1 §4.3]. Nessuna revisione esterna è prevista né prezzata.
- Le trascrizioni delle sessioni stanno su disco in chiaro per 30 giorni di default e vengono copiate in PostgreSQL dal `SessionStore` [verificato: ricerca/26 §3.7; docs hooks]. La proposta 1 non lo tratta nel registro dei trattamenti.
- Le carte si approvano dal telefono con la sessione di Teams, senza un secondo fattore per le classi più rischiose (§8).
- Non cita l'incidente di LiteLLM di marzo 2026, che riguarda il pezzo che custodisce la chiave Anthropic (§6).

### 3.2 Proposta 3 · Claude Team e MCP: 6 su 10

**Cosa regge.**
- 29 dei 57 lavori sono chiamate a Claude con uscita a schema, senza strumenti [verificato: proposta 3 §5]. Contro le iniezioni è il disegno più robusto: un modello senza strumenti non può agire.
- Le persone arrivano ai connettori con OAuth di Entra, una per una; niente chiavi fisse sui dati gialli o rossi [verificato: proposta 3 §3.4].
- "Approvare non è uno strumento": il sì arriva solo dalla carta con l'identità Entra o dalla pagina del Cancello con FIDO2 [verificato: proposta 3 §4].
- Al massimo 6 sessioni del motore e 10 agenti con strumenti: meno processi che leggono testo di terzi [verificato: proposta 3 §3.3 e §5].

**Cosa non regge.**
- **Più superficie pubblica.** Sei endpoint MCP raggiungibili da internet (RAG, memoria, SersanOutreach, BookStack, Cancello, bacheca), più un "gateway OAuth" nostro davanti [verificato: proposta 3 §1 e §3.2]. Le altre due espongono solo l'MCP RAG, come chiede il board. Scrivere bene un server OAuth 2.1 non è banale [non verificato: giudizio]. La regola sugli IP di Anthropic non aiuta: quegli IP li usano tutti i clienti di Claude (§2).
- **Claude Team senza registro.** Sul piano Team mancano log di audit, conservazione personalizzata e Compliance API (§2). La proposta lo ammette e porta il registro nel Cancello e nei server MCP [verificato: proposta 3 §2]. Ma ciò che le persone fanno in Claude Team con il connettore M365 non passa da lì.
- **Dati rossi.** Nella tabella dei connettori il connettore Microsoft 365 ha "colore massimo: rosso, ma con l'accesso della persona" [verificato: proposta 3 §4]. Va contro la regola dei tre colori: il rosso resta sul server o va all'API dopo l'oscuramento [verificato: ricerca/29 §8.5, che cita PRESENTAZIONE-CEO §5.6].
- **Compiti programmati.** Girano nel cloud di Anthropic in "auto mode", con tutti i connettori inclusi di default, scritture comprese [verificato: code.claude.com/docs/en/routines]. La proposta dice che i connettori "leggono e propongono", ma il connettore ufficiale Atlassian (Jira) scrive. Una scrittura in Jira da un compito programmato salta il Cancello e il suo registro [non verificato: deduzione dai fatti sopra].
- **Nessuna DPIA nel piano.** P0 mette dati gialli (contatti dei lead) in Claude Team dalla prima settimana, ma né P0 né P1 contengono il registro dei trattamenti o la DPIA [verificato: ricerca nelle tre proposte; la Proposta 1 li ha nella fase A, la Proposta 2 in H0].
- K16 su un account Claude personale: tiene la salute fuori dall'azienda, ma è un piano consumer; va spento l'uso dei dati per l'addestramento [non verificato: impostazioni del piano consumer da rileggere].

### 3.3 Proposta 2 · Hermes in casa: 4,5 su 10

**Cosa regge.** Il contenimento è scritto bene: un container per confine di fiducia, un solo bot per istanza, terminale ed esecuzione di codice spenti, carte di business solo dal bot del Cancello, plugin `pre_tool_call` che blocca [verificato: proposta 2 §1 e §5.4]. Buzz resta in LAB senza dati dei clienti, proprio perché approva da solo [verificato: docs ACP di Hermes]. La verifica della settimana 11 controlla anche le chiamate verso Nous nel NetFlow [verificato: proposta 2 §10.3].

**Cosa non regge.**
- Hermes si definisce "a single-tenant personal agent" e scrive che l'unico confine contro un modello ostile è il sistema operativo [verificato: ricerca/27 §7.2, SECURITY.md].
- 9 problemi di sicurezza aperti nel gateway, fra cui segreti di un profilo usati da un altro (GW-41, KB-10) [verificato: ricerca/27 §6.2; issue #143547].
- Almeno 45 avvisi di sicurezza nel 2026 nel database di GitHub, 0 pubblicati dal repository [verificato: ricerca/27 §7.1]. Con la regola dei 14 giorni di Cyber Essentials questo vuol dire salti di versione frequenti e poco documentati.
- Identità per istanza: in `hermes-commerciale` scrivono tutti e quattro [verificato: proposta 2 §3.3]. Il Coach vendite sta lì, quindi il sistema non garantisce che il report di una call arrivi solo a chi l'ha fatta (G4). È un tema di riservatezza fra colleghi, con la L. 132/2025 e lo Statuto dei lavoratori da chiarire nel parere [non verificato: interpretazione].
- Sei bot Teams pubblici e il webhook di WhatsApp che entra direttamente in un'istanza con strumenti [verificato: proposta 2 §3.4]. Il testo dei clienti arriva a un agente che ha MCP in lettura e `propose_action`.
- L'"account ospite" Nous della v0.22.5 va escluso con il NetFlow: oggi non si sa se chiama fuori [verificato: ricerca/27 §2.1].
- Il punto dei "60 secondi" nel fail closed va provato (§2).
- Memoria interna di Hermes (`MEMORY.md`, `USER.md`) in sei volumi: il diritto alla cancellazione va onorato in sei posti in più [non verificato: deduzione da ricerca/27 §4].

---

## 4. Superficie d'attacco a confronto

| Voce | Proposta 1 | Proposta 2 | Proposta 3 |
|---|---|---|---|
| Endpoint pubblici dei bot | 1 (fino a 9 se si sceglie un bot per squadra) | 6 (5 istanze più il Cancello) | 1 |
| Endpoint MCP pubblici | 1 (MCP RAG, come nel board) | 1 (MCP RAG) | 6, più un gateway OAuth nostro |
| Webhook pubblici | WhatsApp nella Porta; n8n firmati; firma DocuSeal | WhatsApp dentro `hermes-commerciale`; n8n; DocuSeal | WhatsApp nella Porta; n8n; DocuSeal |
| Processi con strumenti che leggono testo di terzi | fino a 57 profili, con lo schema a due sessioni | 50 profili in 6 istanze | circa 10 agenti SDK, più le sessioni delle persone e i compiti programmati in Claude Team |
| Codice nuovo da aggiornare entro 14 giorni | SDK (quasi un rilascio al giorno) | Hermes (circa 1,5 release a settimana), più il plugin Python | SDK leggero, più funzioni Claude Team in anteprima |
| Registro di ciò che fa l'IA | Cancello, OpenTelemetry, Loki, Wazuh | Cancello, `/insights`, Loki | Cancello e MCP sì; Claude Team no |
| VLAN per gli agenti | 32 nuova (o 30 con firewall Proxmox) | 30, insieme a n8n e LiteLLM | 30 |

[verificato: §3 delle tre proposte; confronto non verificato]

Servizi nuovi uguali nelle tre, ognuno con le sue patch: Vexa, Asterisk, Pipecat, MariaDB, Postiz, listmonk, DocuSeal, strumento di fatturazione, Buzz in LAB [verificato: §3-4 delle tre proposte].

---

## 5. Dati che escono

Il board ammette fuori casa solo M365/Entra, Claude Team, API Anthropic dietro LiteLLM, Cloudflare, GitHub, Supabase, Vercel, Jira, Instantly e S3 facoltativo [verificato: board-testo-completo.txt, righe 13-33].

| Destinazione | Cosa riceve | Nel board? | Dove compare |
|---|---|---|---|
| API Anthropic via LiteLLM | prompt e contesto degli agenti; rosso solo oscurato | sì | 1, 2, 3 |
| Claude Team (chat, connettori, Cowork, compiti programmati nel cloud di Anthropic) | domande delle persone, risposte dell'MCP RAG, posta e documenti dal connettore M365 | sì, ma senza audit né conservazione personalizzata | 1 e 2 come finestra; 3 come centro del lavoro |
| Meta (WhatsApp Cloud API) | messaggi dei clienti | no, eccezione | 1, 2, 3 |
| Telegram | solo avvisi senza contenuto | no, eccezione | 1, 2, 3 |
| Slack | conversazioni con clienti che usano Slack | no, eccezione | 1, 2, 3 |
| Operatore telefonico (Messagenet) | voce e numeri dei lead | no, necessità esterna | 1, 2, 3 |
| Relay SMTP | indirizzi degli iscritti alla newsletter | no, necessità esterna | 1, 2, 3 |
| VPS per Pangolin | traffico verso bot, webhook e MCP | no, se scelto | 1, 2, 3 |
| Apollo, Metricool, moda.app, Higgsfield, Apify, Perplexity | contatti e contenuti | no, eccezioni | 1, 2, 3 |
| Nous | da escludere con il NetFlow | no | solo 2 |
| Account Claude personale | dati personali di chi lo sceglie | no | solo 3 (K16) |

[verificato: §2-§4 e §8 delle tre proposte; colonna "nel board" dal board]

Tutte e tre rispettano la regola di Alberto: scrivono le uscite come necessità o eccezioni con il loro costo, senza togliere funzioni [verificato: lettura delle tre proposte]. Ogni uscita fuori board va nella DPIA, nel registro dei trattamenti e nell'elenco dei sub-responsabili [non verificato: proposta mia, coerente con ricerca/16 riga 194].

---

## 6. Rischi comuni, che nessuna proposta chiude del tutto

1. **LiteLLM custodisce la chiave Anthropic e tutte le chiavi virtuali.** Le versioni 1.82.7 e 1.82.8 erano compromesse il 24/03/2026 [verificato: netspi.com, fonte di terzi]. Solo la Proposta 2 lo cita [verificato: proposta 2 §10.1]. Serve: immagine fissata per digest e controllata, uscita solo verso `api.anthropic.com`, pannello di amministrazione solo dalla VLAN MGMT, chiave principale in Infisical con rotazione [non verificato: proposta].
2. **n8n è nel board e riceve webhook da internet.** Nel 2026 ha avuto la CVE-2026-21858 (CVSS 10, esecuzione di codice senza login) e la CVE-2026-27493 sui nodi Form [non verificato: thehackernews.com e cyber.gov.au letti tramite ricerca, testo ufficiale di n8n non letto]. Rotte pubbliche solo per i webhook firmati, nessun Form pubblico, patch entro 14 giorni.
3. **Postiz custodisce i token delle pagine aziendali.** Nel 2026 ha avuto più CVE, fra cui una path traversal critica segnalata come sfruttata, corrette fino alla 2.21.8 [non verificato: NVD e OSV letti tramite ricerca]. Postiz mai pubblico: solo via NetBird.
4. **listmonk** ha avuto quattro CVE nel 2026, l'ultima (SQL injection) corretta nella 6.2.0 [non verificato: advisories.gitlab.com e opencve.io letti tramite ricerca]. La Proposta 1 cita la v6.2.0 come ultima stabile [verificato: proposta 1 §8.3].
5. **MinIO non è più mantenuto.** Va sostituito prima di salvarci audio e file degli agenti, come dicono tutte e tre [verificato: §6.1, §3.2, §3.2 delle tre proposte].
6. **I telefoni che approvano entrano nel perimetro Cyber Essentials**, anche se personali [verificato: ricerca/25 N03, da iasme.co.uk]. Nessuna proposta lo scrive nel piano: sistema supportato, blocco schermo, MFA, aggiornamenti.
7. **Le regole "Sempre".** Dopo 20 approvazioni uguali un'azione diventa automatica [verificato: proposta 1 §5.2, da PRESENTAZIONE-CEO §5.4]. Senza scadenza, il permesso resta anche se cambia il contesto. Servono una scadenza e una revisione mensile.
8. **Il VPS, se si sceglie.** Deve passare il TLS senza aprirlo (passthrough verso Traefik in casa), altrimenti vede in chiaro bot, webhook e MCP. È un sistema in più nel perimetro Cyber Essentials [non verificato: proposta].
9. **Lavoratori e registrazioni.** Debrief, metadati del lavoro (F1), coaching e registrazione delle call chiedono informativa, DPIA e parere sull'art. 4 dello Statuto; Andrea chiede il Registro delle opposizioni e la dichiarazione di essere un'IA [verificato: proposta 1 §6, voci A1, G3-G5]. Le tre proposte rimandano al parere legale con tetto 2.500 €.

---

## 7. Numeri che non tornano

| Dove | Cosa | Correzione |
|---|---|---|
| Proposta 1 §1 | "273 problemi aperti" su Hermes | oggi sono 276 [verificato: issue #143547] |
| Tutte e tre | "MinIO archiviato dal 12/02/2026" | non più mantenuto dal 12/02, archiviato il 25/04/2026 [non verificato: fonti di terzi] |
| Proposta 3 §3.3 | margine di RAM da +3 a +12 GB senza comprarne | il conto non mette Postiz, listmonk, DocuSeal e fatturazione (2,5-5 GB nelle altre proposte) e dà 6-8 GB a 6 sessioni, dove la Proposta 1 ne dà 12. Con le stesse voci il nuovo sale a circa 49,5-59 GB e il margine scende a circa -6/+3,5 GB [non verificato: ricalcolo mio] |
| Proposta 3 §10.2 | "RAM fino a 4 moduli, 0-400 €" | il rapporto 32 dà 272-512 € per 4 moduli, con la banda al 69 % [verificato: proposta 1 §3.2, che cita ricerca/32 §2.4] |
| Proposta 3 §10.2 | seconda GPU 686-893 €, UPS 1.011-1.060 € | nelle altre due: 686-775 € e 937-1.144 €. Stessi oggetti, fonti diverse [verificato: confronto fra le tre proposte] |
| Proposta 3 §10.1 | fine bundle "550,67-557,16 €" | include Andrea solo a consumo (103,97 €). Con il piano PRO il minimo è circa 504,48 €, coerente con i "58-110 € con Andrea" dell'In breve [non verificato: calcolo mio] |
| Proposte 1 e 2 | corrente della seconda GPU | 6,39-17,89 € nella 1, 2,55-7,66 € nella 2: stessa scheda, ipotesi diverse [verificato: proposta 1 §8.1; proposta 2 §9.1] |
| Proposta 3 §3.4 | VPS "da 6,49 € verificato su hetzner.com" | oggi la pagina dice 5,99 € [verificato: hetzner.com/cloud, 25/10/2026] |
| Proposta 2 In breve | "151 gp di base" | è il totale senza H6; il totale è 171 gp (227,5 con la riserva). Il contenuto degli agenti vale circa 0,6 gp l'uno, contro i 67 gp per 57 agenti della Proposta 1: probabile sottostima di 20-30 gp [non verificato: confronto mio] |
| Rapporto 16, riga 158 | "l'admin imposta la conservazione dell'organizzazione" su Claude Team | oggi la conservazione personalizzata è solo Enterprise [verificato: claude.com/pricing/team] |

Ho ricontato i totali principali e tornano: Proposta 1, una tantum 3.431-4.295 € e listino 483-593 €; Proposta 2, subito 3.114-4.354 € e integrazioni fino a circa 284 €; Proposta 3, 191 e 254 gp [non verificato: somme mie sulle tabelle delle proposte].

---

## 8. Il vincitore per la mia lente, e cosa va corretto

**Vince la Proposta 1.** È l'unica in cui il blocco degli effetti, l'identità per persona e la separazione di rete stanno in pezzi che controlliamo, con una superficie pubblica minima. Le correzioni che seguono vanno fatte prima che un dato di un cliente entri nel motore, cioè prima della fase B [non verificato: giudizio].

1. **Ponte verso il Cancello coerente.** Il guardrail diventa un hook di callback dell'SDK nel runner, che blocca allo scadere del tempo; se resta anche un plugin con hook a comando, ogni hook ha `onFailure: "block"` [verificato: docs hooks]. `propose_action` non può essere insieme in `dontAsk` e marcato `requiresUserInteraction`, perché viene sempre negato [verificato: docs permissions]. Strada più semplice: `propose_action` crea solo la carta e risponde "in attesa"; il Cancello riprende la sessione con l'esito come nuovo messaggio. Alla ripresa il runner ripassa la modalità, perché `--resume` non la ripristina [verificato: docs hooks]. Tutto questo entra nei 10 scenari di prova.
2. **Carte legate al contenuto e secondo fattore.** Ogni carta porta l'impronta del testo esatto, un codice monouso e una scadenza; l'esecutore ricalcola l'impronta prima di agire. Per offerte, contratti, fatture e solleciti, primi contatti, codice e infrastruttura serve un secondo passo con la chiave FIDO2 sulla pagina del Cancello, non solo il tocco in Teams [non verificato: proposta]. I telefoni che approvano entrano nel perimetro Cyber Essentials [verificato: ricerca/25 N03].
3. **Token della persona verso l'MCP RAG.** Firmato con una chiave in Infisical, vita breve, destinato solo all'MCP RAG. La persona è chi ha avviato il lavoro (l'`aadObjectId` dalla Porta o la persona che ha creato l'orario in n8n), mai un campo scritto dal modello. Il risultato va solo a chi può vedere quei dati: niente risposte di un lavoro di Alessandro in un canale aperto a tutti [non verificato: proposta].
4. **Claude Team e i dati rossi, decisi prima della fase B, non della C.** La proposta accende il connettore M365 di Claude Team in sola lettura (§4.2), ma quel connettore porta posta e documenti, cioè dati rossi, in un piano senza audit e senza conservazione personalizzata [verificato: claude.com/pricing/team; ricerca/29 §5.4]. Va scritto nella DPIA e nel parere; l'MCP RAG dà il rosso solo oscurato; l'accesso condizionale guarda gli IP di Anthropic [non verificato: proposta].
5. **Endpoint pubblici.** L'MCP RAG accetta solo token Entra del tenant SerSan con il giusto destinatario; la regola sugli IP di Anthropic è un filtro in più, non un'autenticazione [verificato: gli IP sono di tutto il servizio, platform.claude.com]. Con il VPS, TLS in passthrough [non verificato: proposta].
6. **LiteLLM come bene critico.** Aggiungere al §9 l'incidente del 24/03/2026 e le contromisure del §6 punto 1. La riserva "chiave diretta per famiglia" resta solo in stage: in produzione moltiplica i segreti fuori da LiteLLM [non verificato: proposta].
7. **Trascrizioni e diritto alla cancellazione.** `cleanupPeriodDays` basso, `persistSession: false` per i lavori con dati rossi, dataset ZFS cifrato, conservazione scritta nel registro dei trattamenti. La cancellazione su richiesta deve raggiungere PostgreSQL (`SessionStore`), Qdrant, Loki e i backup PBS [verificato per i 30 giorni: docs hooks; il resto: proposta].
8. **Meno sessioni con strumenti.** Prendere dalla Proposta 3 la divisione in tipi: per ogni profilo scrivere se legge testo di terzi e quali strumenti ha. Chi legge mail, WhatsApp, commenti o trascrizioni non ha `propose_action` nella stessa sessione [non verificato: proposta, coerente con proposta 1 §5.1 punto 5].
9. **Patch dei servizi aggiunti.** Postiz e listmonk mai pubblici; n8n pubblico solo sui webhook firmati; inventario in NetBox; scansione delle vulnerabilità con Wazuh su ogni VM e container [non verificato: proposta; CVE al §6].
10. **Regole "Sempre" con scadenza** (per esempio 30 giorni) e mai per destinatari o domini nuovi [non verificato: proposta].
11. **Revisione esterna.** Un controllo indipendente del Cancello, della Porta e del ponte prima dei dati dei clienti, da preventivare come necessità esterna [non verificato: costo da chiedere].
12. **Numeri da aggiornare:** 276 problemi di Hermes, date di MinIO, VPS a 5,99 € (§7).

---

## 9. Il mio dissenso più forte

Mezzo punto di vantaggio nasconde una scelta vera. La sicurezza della Proposta 1 è sulla carta: dipende da circa 50 gp di codice di sicurezza nostro (Cancello, Porta, ponte, runner, identità), scritto da due persone a tempo parziale, senza revisione esterna e con un SDK che esce quasi ogni giorno [verificato: proposta 1 §4.3; ricerca/26 §1.1]. Il primo controllo che ho fatto sulla documentazione ha già trovato due punti in cui il disegno non funziona come scritto (§2). La Proposta 3 mette la maggior parte del lavoro in chiamate senza strumenti e in un prodotto gestito: nella pratica le iniezioni hanno meno appigli. I suoi rischi sono di governo dei dati (Claude Team senza audit, rosso nel connettore M365, sei endpoint), e si chiudono con regole e configurazione più che con codice. Se SerSan non può pagare una revisione esterna e non regge il ritmo delle patch entro 14 giorni su SDK, LiteLLM, n8n, Vexa, Postiz, listmonk e DocuSeal, il vantaggio della Proposta 1 sparisce. Per questo consiglio la Proposta 1 come motore, ma con la fase P0 della Proposta 3 (Claude Team solo su dati verdi e gialli, con registro e DPIA già fatti) e con la sua divisione in tipi, così i processi con strumenti scendono da 57 a quelli che servono davvero [non verificato: giudizio].

---

## Fonti

**Pagine web lette il 25/10/2026**
- Claude Team, prezzi e funzioni: https://claude.com/pricing/team
- Connettori personalizzati con MCP remoti: https://support.claude.com/en/articles/11175166-about-custom-connectors-using-remote-mcp
- IP di Anthropic: https://platform.claude.com/docs/en/api/ip-addresses
- Compiti programmati di Claude Code: https://code.claude.com/docs/en/routines
- Agent SDK, MCP: https://code.claude.com/docs/en/agent-sdk/mcp
- Agent SDK, permessi: https://code.claude.com/docs/en/agent-sdk/permissions
- Hook di Claude Code (`defer`, timeout, `onFailure`): https://code.claude.com/docs/en/hooks
- Hermes, MCP: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- Hermes, hook: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- Hermes, ACP e Buzz: https://hermes-agent.nousresearch.com/docs/user-guide/features/acp
- Hermes, scheda del gateway unico: https://api.github.com/repos/NousResearch/hermes-agent/issues/143547
- Hetzner Cloud, prezzi: https://www.hetzner.com/cloud/

**Lette tramite ricerca web (fonti di terzi)**
- LiteLLM, incidente del 24/03/2026: https://www.netspi.com/blog/executive-blog/ai-ml-pentesting/litellm-supply-chain-compromise/
- MinIO non più mantenuto: https://pinggy.io/blog/minio_archived_self_hosted_s3_alternatives/ ; https://blog.vonng.com/en/db/minio-resurrect/
- n8n, CVE-2026-21858: https://thehackernews.com/2026/01/critical-n8n-vulnerability-cvss-100.html ; https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/critical-unauthenticated-remote-code-execution-vulnerability-in-n8n-workflow-automation-platform
- Postiz, CVE del 2026: https://nvd.nist.gov/vuln/detail/cve-2026-42556 ; https://osv.dev/vulnerability/CVE-2026-40487
- listmonk, CVE del 2026: https://advisories.gitlab.com/pkg/golang/github.com/knadh/listmonk/CVE-2026-21483/ ; https://app.opencve.io/cve/CVE-2026-62361

**File del progetto**
- `allegati/infra/SerSan Infra Board.md`, `board-testo-completo.txt`, `board-vlan.txt`
- `ricerca/00-visione-funzionalita.md`
- `ricerca/16-gdpr-ai-act-e-regole.md`, `ricerca/25-board-michele-e-delta.md`, `ricerca/26-claude-agent-sdk.md`, `ricerca/27-hermes-self-hosted.md`, `ricerca/29-conoscenza-task-e-documenti.md`
- `ricerca/34-proposta-1-agent-sdk.md`, `ricerca/34-proposta-2-hermes-self-hosted.md`, `ricerca/34-proposta-3-claude-team-e-mcp.md`

**Strumenti**
- Context7: quota mensile esaurita il 25/10/2026; documentazione letta con WebFetch.
