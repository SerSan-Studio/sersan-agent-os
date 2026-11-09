# 20 · Proposta A: Hermes Agent come orchestratore

**Data:** 24/10/2026. **Per:** Alessandro Serratt e Michele Sanna, preparata per Alberto Tuveri.
**Fonti:** i rapporti 00-18 di `ricerca/` (tutti presenti).
**Etichette:** **[v: 10§4]** = verificato nel rapporto di `ricerca/` indicato (numero e sezione); **[nv]** = non verificato: stima, proposta o voce di terzi. Cambio: 1 $ = 0,8934 € [v: 14].

---

## 1. L'architettura in una pagina

**L'idea.** Hermes ragiona e smista; un nostro servizio, il **Cancello**, agisce. Hermes Agent (Nous Research, MIT, v0.22.5) gira sul server con i pezzi che la visione chiede: profili con nome, bacheca kanban fra agenti, cron, gateway verso Slack [v: 10§4]. Claude via chiave API è il modello principale; la GPU fa i lavori leggeri. Ciò che esce verso clienti, lead o pubblico passa dal Cancello. I difetti noti di Hermes restano così fuori dal percorso dei clienti e dei soldi.

```
PERSONE: Slack (DM, #agenti, #approvazioni, canali cliente)
   ^ Socket Mode, solo in uscita
SERVER DL380 (Proxmox)
  VM agenti: Hermes fissato (profili, kanban, cron, un processo per card)
             MCP: Notion, cervello, SersanOutreach, Cancello
             runner codice: claude -p con chiave API e tetto in $
             CANCELLO: carte, esecutori, audit, ESTOP, budget, freno ai giri,
             ingresso webhook  <==  Cloudflare Tunnel  <==  Recall, form, Instantly
  VM dati:   Postgres 17 + pgvector (cervello, SersanOutreach)
  VM gpu:    llama.cpp (giudice Qwen3-4B, embedding), faster-whisper
  VM app:    SersanOutreach, Traefik, Langfuse;  backup PBS + copia fuori sede
IN USCITA: Anthropic API, ElevenLabs + Twilio (Andrea), Recall.ai, Notion,
           Gmail, Metricool in sola lettura.  RISERVA: Hermes Cloud (Londra)
```

**Un caso completo (B1-B4).** Recall.ai chiude la registrazione → webhook nel tunnel → l'ingresso verifica la firma e apre una card per il profilo `post-call` → Hermes (Sonnet 5.5) legge trascrizione, regole della persona in Notion e storico del cliente → scrive to-do in Notion e meeting in SersanOutreach → propone recap per il canale del cliente e mail di follow-up → carta in `#approvazioni` → chi segue il cliente preme Approva → il Cancello esegue una volta sola e registra.

**Quattro regole.**
1. Nessun profilo ha uno strumento che invia a terzi; in Hermes `send_message` già non è dato al modello [v: 10§4.2].
2. La bacheca kanban è il registro dei passaggi fra agenti; Slack ne è la vetrina.
3. Un processo per card e un solo bot "smistatore" in Slack: niente gateway unificato con 25 profili, dove stanno i bug aperti [v: 10§6].
4. Cancello, memoria e ingresso stanno fuori da Hermes: se Hermes delude, si cambia l'orchestratore e si tiene il resto.

**Codice e altri modelli.** Il profilo `sviluppo` lancia Claude Code (`claude -p`, chiave API, un worktree per lavoro, tetto in $); push e PR solo da carta. Il portale CRM lo scrivono Alberto e Mattia nelle sessioni interattive del piano Team. Altri modelli dove servono: Perplexity per la ricerca (già in SersanOutreach), ElevenLabs per la voce, un fornitore di riserva di Hermes solo per i profili senza dati dei clienti [v: 10§4.2; scelta: nv].

---

## 2. Copertura della visione (A1-I4)

Stato: **P** pronto · **A** da adattare · **C** da costruire · **S** in abbonamento · **—** scelta organizzativa.

|Voce|Componente|Stato|Fonte|
|---|---|---|---|
|A1 Riunioni registrate|Bot Recall.ai (Meet, Teams, Zoom) verso l'ingresso; avviso nell'invito e a voce|S+A|14§4, 16§1|
|A2 Second brain relazionale|Notion via MCP: regole, processi, obiettivi, clienti|A|12§6|
|A3 Database vettoriale|pgvector sul server, embedding Qwen3-Embedding-0.6B locale, MCP "cervello"|C|13§7|
|A4 Orchestratore|Hermes self-hosted, versione fissata|P|10§4|
|A5 25 agenti per ruolo|Profili di raccolta, pulizia, indicizzazione (cron senza modello o Haiku) e d'azione (Sonnet)|A|10§4.1-4.2|
|A6 Agenti che imparano|Skill scritte dall'agente; scritture in memoria in coda di approvazione|P|10§4.2|
|A7 Chat condivisa|Kanban come registro + specchio in `#agenti` con freno ai giri nel codice|A+C|10§4.1, 17§8|
|B1 Recap al cliente|Profilo post-call; Slack Connect o mail, solo da carta|C||
|B2 Opportunità nel CRM|`record_meeting`, `update_deal` di SersanOutreach via MCP|A|01§5.2|
|B3 Mail di follow-up|Bozza Gmail (skill email di Hermes), invio da carta|A||
|B4 To-do|Notion via MCP|P|10§9|
|B5 Autonomia totale|Per classe e per gradi (§5), mai al primo contatto|C|16§6|
|C1 Debrief del mattino|Cron per persona alle 7:00 in DM; numeri calcolati dal codice|A||
|C2 Agente nella call|Recall.ai; Hermes entra in Google Meet ma legge solo i sottotitoli|S||
|C3 Analisi con Claude|Profilo post-call su Sonnet 5.5|P|13§10|
|C4 Dettatura|faster-whisper sulla RTX 4000; note vocali in Slack|A|13§5|
|C5 Registro dei meeting|Tabella `meetings` nel cervello, vista in Notion, pipeline estratta|C|01§5.5|
|C6 Regole personali|Pagina Notion per persona, caricata dal provider di memoria prima di ogni turno|C|10§4.2|
|D1 Pipeline pesata|Portale in SersanOutreach con Claude Code; senza storico, pesi dichiarati|C|01§1.4|
|D2 Brief pre-meeting|Enrich di SersanOutreach (Perplexity, Voyager) + cervello + posta|A|01§2|
|D3 Storico relazione|Linea del tempo del cliente dal cervello|C|12§6|
|D4 Slide del brief|moda.app via MCP o Claude Slides|A|05§5.8|
|D5 Offerta|Profilo su Opus 5.5 con catalogo in Notion; invio da carta|C|14§1.5|
|E1-E2 Tempo e token|Argomenti in §6 e §9|—|00|
|E3 Banca dei token|Chiave API per famiglia di agenti, `/insights`, Langfuse, tetto per card, stop al 100 % nel Cancello|A|10§4.2|
|E4 Formazione|Alfabetizzazione documentata (AI Act art. 4)|—|16§4|
|F1 Metadati Workspace|Job notturno sui metadati, mai sui contenuti; dati individuali ≤ 21 giorni|C|16§1.2|
|F2 Interviste|Profilo intervistatore in DM|A|10§4.1|
|F3-F4 Mappa e automazioni|Profilo analista mensile su Opus, con ore e costo stimati|C|14§1.5|
|F5 AI per tutti|Slack come porta unica, un assistente per persona|A|10§4.2|
|G1 Canale call di vendita|`#call-vendita` alimentato dal post-call|A|10§4.1|
|G2 Fit score|Qualificatore GP+BALD di SersanOutreach esteso alle call|C|01§1.1|
|G3-G4 Coaching|Report solo al venditore; al responsabile numeri aggregati; nessuna emozione|C|16§1.2|
|G5 Andrea in 90 s|Ingresso → ElevenLabs Agents + numero Twilio italiano, senza Hermes nel percorso; si dichiara AI|S+C|14§3.4, 16§2|
|G6 Impara dai rifiuti|Esiti analizzati ogni settimana; nuova apertura proposta e accesa da carta|C||
|G7 Risultati|Tempo di richiamata e meeting fissati nel debrief|C|00 K|
|G8 Perse → marketing|`lost_deal_analysis`, `review_feedback` all'agente editoriale|A|05§5.6|
|G9 Organigramma di agenti|Database Notion generato dal registro dei profili: responsabile, modello, tetto, costo|C|18§5|
|G10, H1-H5, H7|Piano di formazione; ogni CEO con il proprio assistente; Mattia ambassador|—|00|
|H6 Premio mensile|Classifica dal registro (agenti creati, ore stimate)|C|00|
|I1-I2 Contesto|Coperti da A1-A3|—|00|
|I3 Aree senza AI|Policy letta dal Cancello: DM e commenti dei founder, firma tecnica di Michele|A|05§5.8|
|I4 Marketing 70/30|Agenti editoriale, copy e metriche di 05§5|A|05§5|

**Lacune vere.** D1 non ha storico (91 deal aperti senza valore, 0 vinti) [v: 01§0]; C2 dipende da un servizio esterno; G5 e G3-G4 aspettano un parere legale; F1 richiede che SerSan usi Google Workspace, oggi "non trovato" [v: 14§5].

---

## 3. Cosa gira sul server e cosa in abbonamento

|VM (Proxmox)|Contenuto|vCPU|RAM|Disco|
|---|---|---|---|---|
|agenti|Hermes in container, runner Claude Code, Cancello, Langfuse|8|24 GB|100 GB|
|dati|Postgres 17 + pgvector: cervello e SersanOutreach|4|24 GB|300 GB|
|gpu|llama.cpp: giudice Qwen3-4B, embedding; faster-whisper (~1,5 GB)|4|16 GB|50 GB|
|app|SersanOutreach (7,4 GiB di tetti misurati), Traefik, cloudflared|8|24 GB|100 GB|
|stage, monitor, pbs|prove degli aggiornamenti di Hermes, Prometheus/Grafana, backup|8|22 GB|dischi propri|

Totale circa 110 GB: sta nei 128 GB della configurazione bilanciata a 8 moduli [v: 15§2.2]. Dimensioni di dischi e vCPU [nv].

**Perché la GPU fa solo i lavori leggeri.** Hermes rifiuta i modelli con meno di 64k token di contesto per gli agenti con strumenti; la RTX 4000 non li regge a buona velocità [v: 10§4.3, §7]. I modelli locali fanno quindi i compiti ausiliari di Hermes (titoli, compressione, punteggi) e la pipeline del cervello: embedding (Anthropic non li vende), classificazione dei dati "solo locali", oscuramento prima del cloud, trascrizione [v: 13§0, §2.3].

**In abbonamento, e perché.** Claude API per i modelli di frontiera e Claude Team per le persone. ElevenLabs e Twilio, perché la telefonia vuole un operatore e un numero italiano. Recall.ai, perché i bot di riunione vivono nel cloud. Slack, Notion e Cloudflare Tunnel (0 €, nessuna porta aperta) [v: 15§4.3]. Hermes Cloud solo come riserva fredda, regione Londra; senza DPA trovato, ospita solo profili senza dati dei clienti [v: 18§2.4].

---

## 4. SersanOutreach e marketing

**Migrazione.** SersanOutreach passa nella VM `app` con la checklist di 01§4.11: stesso dominio `outreach.sersan.io` dietro Cloudflare Tunnel (l'estensione Chrome lo ha nel manifest), database in casa con backup `age` fuori sede, VM Azure spenta dopo una settimana stabile [v: 01§4.4, §4.7].

**Collegamento agli agenti.**
- I due server MCP di SersanOutreach sono stdio: sullo stesso server Hermes li lancia come processi figli, senza costruire HTTPS e OAuth [v: 01§5.1-5.2, §5.10]. Va riparata la configurazione rotta [v: 01§1.4].
- Lettura (19 tool) per tutti i profili commerciali. Scrittura solo `record_meeting`, `record_next_action`, `update_deal`, `generate_drafts`. `approve_message` e `import_leads` confermato sono bloccati da un hook: l'approvazione degli invii resta umana, con impronta, nell'interfaccia di SersanOutreach [v: 01§5.4; filtro: nv].
- Un utente "agenti" per famiglia e identità firmata in `enforce` (oggi `observe`) prima di dare scritture [v: 01§6].
- Il modulo lead del sito alimenta `/api/inbound/first-party/record` e, in parallelo, la chiamata di Andrea [v: 01§5.5].
- Hermes non tocca LinkedIn: browser spento (`--skip-browser`) e nessuna tecnica anti-rilevamento [v: 10§4.2].

**Marketing.** Gli agenti entrano nei ruoli di 05§5: editoriale (idee da call, `reply_digest`, motivi di perdita), copy con lint e revisione avversaria, metriche il lunedì da Metricool in sola lettura. Valgono le regole di casa: niente esce senza un sì nel registro; su Metricool scrive solo una sessione presidiata, mai cron o loop [v: 05§5]. Quindi Hermes prepara la lista da approvare e il copy; la pubblicazione resta la sessione presidiata di oggi. I profili LinkedIn dei founder restano manuali.

---

## 5. Controllo e sicurezza

**I difetti noti e come si colmano.**

|Difetto di Hermes|Rimedio|Da dove|
|---|---|---|
|Nel video V2 le chat di bot diversi si mescolano, il contesto si perde, l'installazione è faticosa; bug aperti sui profili multipli [v: 10§6]|Un processo per card, un solo bot Slack; versione fissata; ogni aggiornamento passa 10 scenari di prova nella VM `stage`||
|Approvazioni che scadono dopo 300 s e coprono solo la shell|Carte del Cancello||
|Mail, post e chiamate regolati da frasi nelle skill [v: 10§5]|Gli strumenti che inviano esistono solo nel Cancello; Hermes ha `propose_action`|open-dots|
|Giri infiniti fra agenti|Al massimo 8 messaggi consecutivi fra agenti per thread, azzerati da un messaggio umano|buzz [v: 17§8]|

**Autonomia per gradi.** Si parte con tutto su carta. Una regola "Sempre" nasce solo come riga confermata da una persona, per classe e destinatario, dopo 20 carte approvate senza modifiche. Le regole possono solo stringere. Mai "Sempre" per offerte, primo contatto, pagamenti e cancellazioni [soglia: nv]. Chi approva: il titolare del cliente per recap e mail; un CEO per le offerte; per i nuovi lead, la coda di SersanOutreach.

**Iniezioni.** Le sessioni nate da webhook partono con quattro strumenti.

**Confini.** Hermes stesso dichiara che il solo confine è il sistema operativo [v: 10§5]. Quindi: VM dedicata, container senza privilegi, terminale degli agenti in Docker, chiavi fuori dal sandbox con il proxy di Hermes, nessuna porta di Hermes su internet. I webhook passano dall'ingresso del Cancello, che verifica firma e anti-replay; dopo le CVE sui webhook del 2026 serve almeno la v0.22.2 [nv: 10§3].

**Audit, budget, stop.** Audit del Cancello a catena di hash. Stop al 100 % del tetto mensile per famiglia di agenti. `/stop` in Slack ferma i cron e la kanban (`hermes pause`) e fa rifiutare ogni effetto al Cancello [v: 10§4.2].

**GDPR e AI Act.**
- Se il server sta in Sardegna i dati restano in UE (luogo non confermato) [nv: 16§5]. Anthropic API: 30 giorni di conservazione, nessuna regione UE, DPA nei termini commerciali [v: 16§5].
- Audio ≤ 30 giorni, trascrizioni 24 mesi, log 90 giorni; registro dei trattamenti legato al codice da un test; DPIA per registrazioni, vendite e Andrea [v: 16§6].
- Art. 50: chi scrive o parla a un esterno si dichiara AI dal 2/8/2026. Valutare i venditori è alto rischio dal 2/12/2027; inferire emozioni è vietato. Statuto dei lavoratori art. 4 se ci sono dipendenti [v: 16§1.2, §4].
- Claude in automatico solo con chiave API, mai con il plugin che usa l'abbonamento [v: 10§6].

---

## 6. Piano a fasi

|Fase|Settimane|Giorni-persona|Cosa si vede alla fine|
|---|---|---|---|
|0. Fondamenta|1-2|6|Server nel rack con UPS, Proxmox, VPN, tunnel, ripristino di prova riuscito|
|1. Pilota: Hermes, Cancello, post-call, debrief|3-5|12|Dopo ogni call: recap in Slack, bozza di mail in carta, to-do in Notion, meeting in SersanOutreach; debrief alle 7:00|
|2. Memoria, brief, migrazione SersanOutreach|6-8|16|Brief la sera prima di ogni incontro; prima bozza d'offerta; Azure spenta|
|3. Vendite e voce (dopo il parere legale)|9-12|15|Lead richiamata in 90 s; coaching al singolo venditore; perdite al marketing|
|4. Organizzazione|13-16|11|25 profili in organigramma con costo; mappa dei processi; premio mensile; riserva Hermes Cloud provata|

**Totale 60 giorni-persona; primo rilascio utile alla settimana 5 con 18** [nv]. Fase 1 nel dettaglio: Hermes 2, Cancello 5, carte in Slack 1,5, flusso post-call 2, debrief 1, prove 0,5.

**Punto di decisione a fine fase 1.** Due settimane di misura. Se una sessione finisce al profilo sbagliato, o se un aggiornamento rompe il flusso, si sostituisce Hermes con un runner sull'Agent SDK di Claude. Cancello, cervello e ingresso restano; costo stimato 10-15 giorni-persona [nv].

---

## 7. Costi mensili (euro, IVA esclusa)

**Metodo.** Parto dalle tabelle 11.1-11.2 di 14 e cambio solo le righe toccate da questa architettura. Le API valgono 1,5 volte la stima di 14: Hermes ha un prompt di sistema con molti strumenti [nv].

**Formula:** costo = fissi di 14 ± righe cambiate + API (base × moltiplicatore × 1,5) + ore di riunione × 0,65 $ + minuti di voce × 0,0445 $ + LLM della voce + proxy. L'uscita di cassa è il costo meno le API, finché valgono gli 800 $ di crediti.

|Voce|Minimo|Consigliato|Completo|
|---|---|---|---|
|Fissi di 14 (Claude Team nel bundle)|248,70|780,20|1.652,60|
|− Fireflies, sostituito da Recall.ai|0|−67,90|−67,90|
|− CRM esterno (il CRM è SersanOutreach)|0|−26,80|−160,81|
|− Notion Business → Plus (l'AI la fa Claude)|0|−35,73|0|
|+ Nous Portal Plus e Hermes Cloud|0|+18,67|+47,08|
|**Fissi**|**248,70**|**668,44**|**1.470,97**|
|API Anthropic (14 × 1,5)|30,59|132,93|332,51|
|Recall.ai, 30 h × 0,65 $|17,42|17,42|17,42|
|Voce e proxy, come 14|12,51|72,90|235,41|
|**Totale di listino**|**309,22**|**891,69**|**2.056,31**|
|**Uscita di cassa oggi**|**278,63**|**758,76**|**1.723,80**|
|Dopo lo spegnimento della VM Azure (−150)|128,63|608,76|1.573,80|

- Hermes Cloud: Plus 20 $ al mese [v: 18§2.4]; istanza ferma 0,03 $/giorno; nel completo istanza Large accesa, 32,70 $ al mese [terzi: 18§2.4].
- Nel completo le API costano 372 $, dentro gli 800 $ di crediti, che vanno verificati nella Console [v: 14§1.4].
- A regime, senza bundle: +446,70 € di Claude Team, più le API se i crediti finiscono [v: 14§1.3].
- Una tantum: UPS 1.163-1.293 €; kit HPE e SSD non prezzati [v: 14§11.3, 15§8].

---

## 8. Rischi e mitigazioni

|Rischio|Prob.|Mitigazione|
|---|---|---|
|Hermes instabile: 5 patch in 10 giorni, 5.000+ issue aperte [v: 10§3]|alta|Versione fissata, VM `stage`, uscita prevista in §6|
|Contesti mescolati fra agenti|media|Un processo per card, prova di due settimane|
|Iniezione da email e trascrizioni|media|Effetti solo dal Cancello|
|Termini Anthropic|bassa|Chiave API per gli agenti; posti Team solo per le persone [v: 10§6]|
|Un solo amministratore|alta|Runbook, Mattia secondo amministratore [v: 15§6]|
|Corrente e guasti in Sardegna|alta|UPS, backup fuori sede, Azure accesa fino a una settimana stabile, riserva Hermes Cloud [v: 15§5.3]|
|Andrea, registrazioni, valutazione dei venditori|media|Parere legale prima della fase 3; voce sintetica non clonata salvo contratto [v: 16§7]|
|Spesa che scappa|bassa|Tetti per chiave e per card, freno ai giri|
|Nous sposta valore sui servizi a pagamento [v: 10§6]|media|Nucleo MIT, fork possibile|

---

## 9. Perché sceglierla, e perché no

**Perché sì.**
- Ha già i pezzi che la visione chiede: profili, kanban, cron e canali sono pronti, non da scrivere.
- Licenza MIT, dati sul nostro server, qualunque modello (Claude per pensare, la GPU per i lavori locali), una riserva ospitata a Londra.
- Rischio contenuto per costruzione: i pezzi che toccano clienti e soldi sono nostri e sopravvivono a un cambio di orchestratore.

**Perché no.**
- Hermes è il pezzo meno stabile, e l'autore del video V2 lo trova "buggy".
- Il valore protetto sta nel Cancello, che va costruito comunque.
- La "chat fra bot" visibile di Hermes è un'interfaccia desktop: sul server la vetrina in Slack è da costruire [v: 10§4.1].
- Chi vuole agenti sul telefono in pochi giorni li ha prima con Grok Bot, al prezzo di dati negli USA e nessuna scelta del modello [v: 11§1].
