# Quanto è autonomo il disegno attuale: le 90 voci e i 15 colli di bottiglia

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **RAP2**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

## In breve

- **Dentro il sistema gli agenti fanno da soli; tutto ciò che esce passa da una carta.** A regime, secondo la mia classificazione:
  - 34 voci sono L3 piene: lavoro interno, controlli automatici e «Andrea»;
  - 21 voci sono L3 nel lavoro interno, ma hanno un passo L1 verso l'esterno;
  - 13 voci restano L1;
  - 7 voci hanno un passo L0 che non si toglie;
  - 15 voci non sono azioni di agenti.

  Nessuna voce arriva a L2, perché il Cancello non ha la finestra [non verificato: conteggio mio sulla tabella; che manchi la finestra è verificato: SPEC §4.5, AC-001].
- **Confronto con la trascrizione di riferimento.**
  - Nel video, dopo una call partono da soli quattro passi: riassunto nel canale del cliente, opportunità nel CRM, mail di follow-up e to-do. L'imprenditore dice che tutto avviene «in modo totalmente autonomo» [verificato: TR 4:40-5:07].
  - Nel nostro disegno CRM e to-do sono L3 dalla fase 2. Il canale del cliente e la mail restano L1. Per un cliente nuovo restano L1 anche a regime, perché le regole «Sempre» escludono i destinatari nuovi [verificato: P §5.4, App. A B1-B4].
  - Vale lo stesso per gli inviti, le risposte alla posta, le skill che imparano e le aperture di «Andrea».
  - «Andrea» invece è L3 come nel video, ma chiama solo chi ha chiesto di essere richiamato [verificato: P §14 decisione 10; TR 14:53-15:09].
- **Nelle fasi 0-1, le uniche che chiediamo oggi:**
  - tutto ciò che esce è L1;
  - i lavori partono da un comando dato a mano;
  - gli agenti non leggono Jira, il CRM né la memoria [verificato: SPEC §1, §3; PRD «Perimetro» e «Fuori»].

  Le metriche del PRD controllano che niente esca senza carta. Non misurano quanto lavoro esce senza una persona [verificato: PRD «Metriche di successo»].
- **Quasi tutti i limiti stanno nel Cancello, nelle regole di casa e nel calendario, non nell'Agent SDK.** Cambiare orchestratore non li toglie: Cancello, memoria, server MCP, bot e skill restano gli stessi con qualsiasi motore [verificato: P §5.7; D03 §1.6]. Per scegliere l'architettura in base all'autonomia conta soprattutto come si ridisegna il Cancello.
- **I limiti fissi sono già nel disegno**: cancellazioni e credenziali mai agli agenti, pagamenti mai automatici, stop di emergenza. Non li conto fra i colli di bottiglia [verificato: D03 §4.1, §4.3; SPEC §4.10].

## Come leggere la tabella

- **Livelli**:
  - L0 a mano: l'agente prepara, una persona esegue;
  - L1 carta: una persona approva ogni singola azione;
  - L2 finestra: l'azione parte da sola dopo un tempo in cui una persona può fermarla;
  - L3 autonomo: l'azione parte subito, dentro regole, tetti e registro.

  «Fine fase» vuol dire alla fine della fase in cui la voce è completa. «A regime» vuol dire dopo la fase 6, con le regole «Sempre» attive. «n.a.» indica una voce che non è un'azione di agenti.
- **Natura del limite**:
  - [T] tecnico o di costruzione;
  - [P] prudenza o regola di casa;
  - [L] legale: un obbligo, oppure un parere ancora atteso;
  - [E] esterno: piattaforme e fornitori;
  - [V] mancano oggi i volumi o i dati;
  - [F] la voce arriva in una fase tarda.
- **Sigle delle fonti** (tutti i file letti il 9/11/2026):
  - P = PRESENTAZIONE-CEO.md v2.1;
  - D03 = docs/03-architettura.md; D05 = docs/05-design.md;
  - R10, R16, R28, R29, R30, R31, R36 = i rapporti con quel numero in ricerca/;
  - SPEC = docs/superpowers/specs/2026-11-09-nucleo-motore-cancello-design.md;
  - PRD = .claude/prds/sersan-agent-os.prd.md;
  - DOM = DOMANDE-PER-MICHELE.md;
  - TR = la trascrizione di riferimento, con il minuto.
- **Fase e agenti di ogni voce** vengono da P, appendice A e §4.1-4.9 [verificato].
- **I livelli sono una mia lettura** delle regole citate, non un dato scritto nei documenti [non verificato: classificazione mia].

**Regole comuni.** Nella tabella le richiamo con la lettera.

- **(a) Carta.**
  - Passano solo con una carta: invii a clienti e prospect, pubblicazioni, offerte, contratti, fatture e codice.
  - Senza carta passano solo le letture, le scritture interne previste da una regola, le regole «Sempre» e le telefonate di «Andrea» a chi le ha chieste.
  - [verificato: D03 §4.1; D05 §5.5]
- **(b) Regole «Sempre».**
  - Esistono solo dalla fase 2 e nascono dopo 20 sì uguali.
  - Valgono per un agente, un tipo d'azione e una destinazione, e scadono dopo 30 giorni.
  - Non valgono mai per offerte, primi contatti, pagamenti, cancellazioni, destinatari o domini nuovi.
  - [verificato: P §5.4; R36 §5.8]
- **(c) Bacheca e freno.** La bacheca arriva nella fase 2. Il freno ammette al massimo 3 passaggi per catena e 8 messaggi per thread; oltre, arriva una carta [verificato: P §4.11, §11; R36 §5.4].
- **(d) Un solo effetto per giro.** Le scritture interne sono un elenco chiuso scritto nel codice; nella milestone 1 c'è solo `crm.nota` [verificato: SPEC §2.1, §4.5, §4.6].
- **(e) Avvio dei lavori.** Nella milestone 1 i lavori partono da un comando dato a mano. Orari e webhook arrivano con n8n sul server, nella fase 2 [verificato: SPEC §3, §5; ADR-0011; D03 §4.4].
- **(f) Strumenti di lettura.**
  - Nella milestone 1 gli agenti non leggono niente.
  - SersanOutreach, Jira, BookStack e memoria si aprono agli agenti nella fase 2; la ricerca nella memoria (MCP RAG) nella fase 3.
  - I dati dei clienti entrano in memoria solo dopo la settimana 21.
  - [verificato: SPEC §1, §4.5; PRD «Fuori»; P §11]
- **(g) Dichiarazione AI.** Un agente che scrive o parla da solo a un esterno deve dire di essere un'AI (AI Act, art. 50). Ciò che una persona approva esce a nome di quella persona [verificato: P §9.1 regola 1].
- **(h) Canali condivisi con i clienti.** Lì non entra nessun bot: scrive solo il Cancello, dopo una carta [verificato: P §4.11].

## Tabella delle 90 voci

| Voce | Agente · fase | Fine fase | A regime | Cosa lo limita | Fonti |
|---|---|---|---|---|---|
| J1 Un solo sistema | tutti; motore, bacheca, memoria e Cancello · 2-6 | L3 dentro, L1 fuori | uguale; fuori L3 solo con «Sempre» | (a)(b)(c) [P]; tutti i 57 agenti solo alla fine della fase 6 [F] | [verificato: P §4.12, §11] |
| J2 Squadre con responsabile | registro dei profili, un bot per squadra · 1-2 | L1: un agente nuovo nasce solo con un'approvazione | L1 | approvazione e riga nel registro dei trattamenti per ogni agente [P][L: art. 30 e 35 GDPR] | [verificato: P §4.12, §9.1 r.9; R16 §6 r.9] |
| J3 Outreach con agente email | Agente email, Agente LinkedIn, Operatore outbound · 0 casella, 3 agenti | L1 per risposte e messaggi LinkedIn; L1 con FIDO2 per i primi contatti; L0 per lanci e invii in blocco | L1; L3 con «Sempre» solo per risposte ripetute a contatti noti; primi contatti, LinkedIn e lanci restano L1 o L0 | (a)(b)(g) [P]; lanci, invii in blocco e autopilot LinkedIn esclusi per gli agenti [P]; per l'email B2B verso l'Italia il Garante chiede il consenso, decisione D0 aperta [L] | [verificato: P §4.1, §7.1, §7.3, §7.4; R16 sintesi p.7] |
| J4 Email → proposte → chiamate | bacheca · 2-3 | L3 nei passaggi, entro il freno | L3 entro il freno; oltre tre passaggi, carta | (c) [P]; bacheca solo dalla fase 2 [F] | [verificato: P §4.11; R36 §5.4] |
| J5 Agente in ogni chiamata | Agente chiamate · 1 Teams, 3 Vexa | Fase 1: L3 nella lettura; la trascrizione si accende a mano (L0) finché non arrivano il flag «avvisato» e la registrazione automatica [non verificato: deduzione] | call Teams nostre: L3; call dei clienti: il cliente deve ammettere il bot (L0 dalla sua parte); riunioni dal vivo: L0 dal telefono | trascrizione automatica spenta di serie; sala d'attesa di Teams, Meet che rifiuta i bot, Zoom con token OBF [E]; Vexa 0.12 non parla né scrive in chat, quindi l'avviso lo dà chi conduce [E]; avviso di registrazione obbligatorio [L]; RAM per Vexa [T] | [verificato: R30 §3.6, §4.2, §4.4; R36 §7.3] |
| J6 Brief prima e dopo, slide | Agente brief, Agente slide · 0 skill, 3 agenti | Fase 0: L0, una persona usa la skill; fase 3: L3 per brief e slide interne, L1 per le slide al cliente | uguale | (a)(e)(f): il brief «la sera prima» ha bisogno del calendario e della memoria [T][F]; template SerSan da preparare [T]; il brief è profilazione, va nella DPIA [L] | [verificato: P §4.3, App. A J6; R16 §3 p.4] |
| J7 Marketing con outreach e studio | Editoriale, Ricerca concorrenza, Analista metriche, Copywriter, Pubblicatore · 2; Video, Grafiche · 4 | L3 per temi, ricerche, numeri e bozze; pubblicazione: carta (L1), poi Alberto programma il post in una sessione presidiata (L0) | uguale: l'ultimo passo resta L0 | regola di casa delle direttive marketing [P]; Postiz solo dalla fase 4 [F]; Higgsfield come eccezione [E] | [verificato: P §4.4, §8.2] |
| J8 Squadra progetti | Agente task · 2; Project manager, Report cliente, Onboarding, Sviluppatori · 4 | Fase 2: L3 per creare i to-do in Jira; L1 per chiudere quelli delle persone | L3 per to-do e progetti; L1 per report al cliente, to-do altrui e pull request (classe codice, con FIDO2) | (a)(d) [P][T]; i to-do delle persone si chiudono solo con il sì del titolare [P] | [verificato: P §4.6; R36 §5.4, §5.8; R29 §4.2] |
| J9 Chat di gruppo e canali | Porta chat; Buzz in laboratorio · 2, 3, 4 | L3 per i messaggi interni; L1 verso i clienti su WhatsApp e Slack; si approva solo in Teams | uguale; Buzz resta in laboratorio finché perde risposte | (a)(h) [P]; per approvare da Telegram o WhatsApp bisogna legare l'identità Microsoft, rinviato a «una fase successiva» [T]; Buzz giovane, verifica Meta Business [E] | [verificato: P §4.11; D05 §5.4; R36 §5.6] |
| A1 Riunioni registrate | Agente chiamate, Analista chiamate · 1-3 | come J5 | come J5 | come J5; parere sull'art. 4 dello Statuto dei lavoratori se ci sono dipendenti; DPIA [L] | [verificato: P App. A A1; R16 §1] |
| A2 Memoria relazionale | MCP memoria, BookStack · 2 | L3 in lettura; L1 per cambiare le pagine ufficiali | uguale | (a)(f) [P]; gli agenti scrivono solo in un libro di proposte o passano dal Cancello [P]; MariaDB da aggiungere [T] | [verificato: R29 §3.2; P App. A A2] |
| A3 Memoria vettoriale | pipeline del board, Qdrant, MCP RAG · 3 | L3 (servizio) | L3 | pipeline del board nella fase F4 [T][F]; dati dei clienti dopo la settimana 21 [P]; dati rossi verso Claude Team solo oscurati fino a parere e DPIA [L] | [verificato: P App. A A3, §5.6, §11] |
| A4 Orchestratore sul server | motore · 1-2 | L3 nell'esecuzione, ma nella milestone 1 i lavori partono a mano | L3, con n8n per orari e webhook | (e) [T]; per passare sul server serve il posto agenti o la fine della fase F3 [T][F] | [verificato: SPEC §3, §5; DOM n. 2] |
| A5 Agenti per ruolo | Raccoglitore, Pulitore, Bibliotecario, Archivista · 3 | L3 per raccolta, pulizia e indicizzazione | L3 | le cancellazioni sono sempre negate agli agenti: le scadenze le applica solo un lavoro fisso [P]; chi esegua la cancellazione non è scritto [non verificato: assente nei file] | [verificato: P §4.7; D03 §4.1; R16 §6 r.8] |
| A6 Agenti che imparano | revisore delle skill · 4 | L1: proposta in cartella, revisore settimanale, pull request approvata da una persona con FIDO2 | L1 | prudenza [P]; fase 4 [F]; nel video gli agenti imparano da soli | [verificato: P App. A A6; R36 §5.8; TR 3:55] |
| A7 Chat fra agenti | canale «Agenti» · 2 | L3 per i passaggi e i compiti fra agenti; L1 per chiudere i to-do delle persone | uguale | (c) [P]; nel video gli agenti chiudono da soli i to-do già fatti | [verificato: R36 §5.4; R29 §4.2; TR 4:27-4:29] |
| B1 Punti nel canale del cliente | Post-call · 1-3 | L3 nel canale interno privato; L1 verso il canale del cliente | L1 verso il cliente: canale condiviso, mail, Slack, WhatsApp | (a)(h) [P]; nella milestone 1 il messaggio nel canale interno non è ancora fra le scritture ammesse per regola [T]; canali condivisi fra organizzazioni da provare [E] | [verificato: P App. A B1; SPEC §4.6] |
| B2 Opportunità nel CRM | Post-call, operazione «crea deal» · 2 | L3 (scrittura interna) | L3 | (d) [T]; l'MCP di SersanOutreach oggi funziona solo in locale, va portato su HTTP [T] | [verificato: P §7.3; R36 §8.1] |
| B3 Mail di follow-up | Post-call · 1 | L1: carta ad Alessandro; Outlook manda solo al dominio del cliente | L1 per il primo follow-up a un cliente nuovo, anche a regime; L3 con «Sempre» solo per clienti già noti | (a)(b)(g) [P]; il parere entro la settimana 3 dice se possono partire invii veri [L]; permesso d'invio limitato in Exchange [T] | [verificato: P §5.4, App. A B3; PRD «Domande aperte»; R36 §8.1; TR 5:05-5:07] |
| B4 To-do al team | Post-call, Agente task · 2 | L3 (Jira, per regola) | L3 | (d) [T]; nella fase 1 gli agenti non hanno Jira: i to-do li scrive una persona (L0) [F] | [verificato: P §4.2; PRD «Fuori»] |
| B5 Autonomia crescente | regole «Sempre» · 2-6 | L1: prima della fase 2 le regole non esistono | L3 solo per messaggi ripetuti a destinatari noti; mai per clienti nuovi, offerte o primi contatti | (b) [P]; quali messaggi possono diventare «Sempre» lo decidono i CEO dopo il parere [L] | [verificato: P §5.4, App. A B5] |
| C1 Debrief del mattino | Report del mattino · 1 | L3 a orario, ma con poco contesto: nella fase 1 gli agenti non leggono Jira, CRM, calendario né memoria | L3 | (e): come parta alle 7:00 sul banco di prova non è scritto [T][non verificato]; (f) [T]; la mail del debrief alla persona stessa non ha ancora un tipo d'azione per regola [T][non verificato: deduzione da SPEC §4.6] | [verificato: P §4.8, App. A C1; PRD] |
| C2 Agente anche al posto di chi manca | Agente chiamate, Vexa · 3 | L3 nel tentativo; L0 di fatto se nessuno di SerSan è collegato o il cliente non ammette il bot | uguale | la registrazione automatica di Teams forse non parte senza un utente interno, va provata [E]; piattaforme che bloccano i bot [E] | [verificato: R30 §3.6, §4.4] |
| C3 Analisi della call | Analista chiamate, lettura senza strumenti · 1 | L3 | L3 | dati rossi oscurati in locale prima dell'API; sul banco di prova si conserva solo il riassunto [L][P] | [verificato: P §5.6; D03 §5.5] |
| C4 Dettatura | Dettatura · 0, 2, 3 | n.a.: parte quando la persona la usa | n.a. | — | [verificato: P App. A C4] |
| C5 Registro dei meeting | Analista chiamate · 1-2 | L3 | L3 | sul banco di prova solo dati verdi e gialli [P] | [verificato: P §11] |
| C6 Regole di ciascuno | pagina «Come lavoro» · 0, 2 | L3 in lettura, dalla fase 2 | uguale; se un agente propone una modifica, passa da una carta | (f) [F]; pagine ufficiali solo dopo il sì [P] | [verificato: P §10; R29 §3.2] |
| D1 Pipeline pesata | Pipeline · 5 | L3 nel calcolo, con pesi dichiarati da Alessandro (L0) | L3 quando ci sono 30-50 chiusure | oggi 0 deal vinti e 91 senza valore [V]; fase 5 [F] | [verificato: P App. A D1, «Lacune dichiarate»] |
| D2 Brief dall'email | Agente brief · 3 | L3 | L3 | la via per LinkedIn va confermata dal parere; le aperture delle mail arrivano solo con la casella attiva [L][V]; Apollo e Perplexity come eccezioni [E]; DPIA [L] | [verificato: P App. A D2] |
| D3 Storico della relazione | Agente brief, MCP RAG · 3 | L3 | L3 | (f) [F][P] | [verificato: P App. A D3] |
| D4 Slide automatiche | skill · 0; Agente slide · 3 | fase 0: L0; fase 3: L3 per noi, L1 al cliente | uguale | template da preparare [T]; (a) [P] | [verificato: P App. A D4] |
| D5 Offerta automatica | skill · 0; Agente proposte · 3 | fase 0: L0; fase 3: L3 la bozza, L1 con FIDO2 l'invio, firma tecnica di Michele | L1 sempre | (a)(b): un'offerta non diventa mai «Sempre»; scope e prezzi restano umani [P] | [verificato: P §4.3, §5.4, §9.3] |
| E1, E2 Tempo e token | piano · tutte | n.a. | n.a. | — | [verificato: P App. A] |
| E3 Banca dei token | Banca dei token, LiteLLM · 1, 2, 4 | L3: avviso all'80 % e stop al 100 % automatici | L3, anche per persona dalla fase 4 | LiteLLM nella fase F4 del board o con il posto agenti [T][F] | [verificato: P App. A E3; SPEC §4.12] |
| E4 Formazione | persone · 0 | n.a. (obbligo dell'art. 4 dell'AI Act) | n.a. | [L] | [verificato: P §10] |
| F1 Metadati del lavoro | Mappatore processi · 4 | L3 sull'analisi aggregata, dopo l'accordo di ciascuno | uguale | al massimo 21 giorni e solo aggregati; art. 4 dello Statuto se ci sono dipendenti [L]; API di M365 da individuare [T] | [verificato: P App. A F1; R16 §1.2] |
| F2 Interviste | Intervistatore · 4 | L3 | L3 | fase 4 [F] | [verificato: P App. A F2] |
| F3 Mappa dei processi | Mappatore · 4 | L3 per l'analisi; L1 per scrivere nel libro ufficiale «Processi» | uguale | pagine ufficiali solo dopo il sì [P] | [verificato: R29 §3.2] |
| F4 Ore implicite | analisi mensile · 4 | L3 | L3 | fase 4 [F] | [verificato: P App. A F4] |
| F5 AI per tutti | Claude Team, Open WebUI · 0 | n.a. | n.a. | — | [verificato: P App. A F5] |
| G1 Call di vendita in un canale | Post-call · 3 | L3 | L3 | fase 3 [F] | [verificato: P App. A G1] |
| G2 Fit score | qualificatore · 5 | L3 | L3 | mancano i volumi di call [V] | [verificato: P App. A G2] |
| G3 Valutazione della call | Coach vendite · 5 | L3 verso chi ha fatto la call | L3 | parere atteso; con profilazione la valutazione dei lavoratori è ad alto rischio dal 2/12/2027; stima delle emozioni vietata [L] | [verificato: R16 §1.2, §4] |
| G4 Report del coaching | Coach vendite · 5 | L3 a chi ha fatto la call; al responsabile solo dati aggregati | uguale, finché il parere non dice altro | scelta legale in attesa [L]; nel video il report va anche al responsabile | [verificato: P App. A G4; TR 14:40] |
| G5 Andrea in 90 secondi | «Andrea» · 5 | L3, provato con una lead di prova | L3: l'unico contatto esterno senza carta | solo chi ha chiesto la richiamata nel modulo; si dichiara AI; Registro delle opposizioni [L]; una sola linea internet, server da riaccendere a distanza, GPU [T]; servono parere e lead vere [L][V]; la mail di conferma al lead passa dal Cancello, ma non è scritto se con una carta [non verificato] | [verificato: P §4.3, §13; R31 §9, §10] |
| G6 Andrea impara dai rifiuti | «Andrea» · 5 | L1: un founder approva ogni nuova apertura; poi il test A/B gira da solo | uguale | prudenza [P]; volumi [V]; nel video Andrea cambia l'apertura da solo | [verificato: R31 §10; TR 15:34-15:43] |
| G7 Più conversione | Report del mattino · 5 | L3 | L3 | — | [verificato: P App. A G7] |
| G8 Vinti e persi al marketing | Analista vinto/perso · 3 | L3 | L3 | oggi 0 chiusure [V] | [verificato: P App. A G8] |
| G9 Fino a cento agenti | registro · 2-6 | L1 per ogni agente nuovo | L1 | RAM oltre 16 sessioni insieme [T]; approvazione e registro dei trattamenti [P][L] | [verificato: P §4.12, App. A G9; TR 16:23] |
| G10 Superpotere | — | n.a. | n.a. | — | [verificato: P App. A] |
| H1 Formarsi e sperimentare | Claude Team, sandbox · 0-6 | n.a. | n.a. | sandbox nella fase F5 del board [T] | [verificato: P App. A H1] |
| H2 Non delegabile | CEO dal telefono · 1 | n.a.: la voce stessa chiede il sì umano | n.a. | — | [verificato: P App. A H2] |
| H3 Assessment | Claude Team · 0; Intervistatore · 4 | fase 0: L0; fase 4: L3 | L3 | — | [verificato: P App. A H3] |
| H4 Ambassador | tetto in LiteLLM · 4 | n.a. (configurazione) | n.a. | — | [verificato: P App. A H4] |
| H5 Tutti costruiscono | registro · 4 | L1 | L1 | come G9 | [verificato: P App. A H5] |
| H6 Premio mensile | classifica dal registro · 4 | n.a.: classifica L3, premio deciso dalle persone | n.a. | budget del premio [P] | [verificato: P App. A H6] |
| H7, I1, I2 | adozione e qualità | n.a. | n.a. | — | [verificato: P App. A] |
| I3 Aree senza AI | classi negate nel Cancello · 1 | n.a.: L0 per scelta | n.a. | [P] | [verificato: P §9.3] |
| I4 Marketing più creativo | come J7 · 2 | come J7 | come J7 | come J7 | [verificato: P App. A I4] |
| K1 Debrief nel calendario | esecutore Outlook · 2 | L3 (scrittura interna) | L3 | (d): il tipo va aggiunto all'elenco chiuso [T] | [verificato: D03 §4.1; R36 §7.3] |
| K2 «Ho trovato tre nuove call» | Raccoglitore, Agente agenda · 3 | L3 per l'annuncio; L1 per ogni invito | L1 per i destinatari nuovi; L3 con «Sempre» per la seconda call a contatti noti | (a)(b)(c) [P]; Raccoglitore e Agenda solo dalla fase 3 [F]; nel video l'agente degli appuntamenti agisce da solo | [verificato: P §3, App. A K2; TR 4:08-4:18] |
| K3 Posta senza rispondere a mano | Smistatore posta · 3 | L3 per smistare; L1 per ogni risposta | L1; L3 con «Sempre» solo per destinatari noti | (a)(b)(g) [P]; serve l'accordo di ciascuno sulla propria casella [P][L]; chi legge la mail non può proporre azioni: la risposta nasce in un secondo lavoro che vede solo i campi estratti [T]; archiviare non è ancora un tipo per regola [non verificato] | [verificato: P §4.8, App. A K3; SPEC §4.4; TR 9:47] |
| K4 Cosa si è detto in una call | Claude Team con MCP RAG, Capo di gabinetto · 3 | L3 | L3 | dati rossi verso Claude Team solo oscurati fino a DPIA e parere [L]; dati dei clienti dopo la settimana 21 [P] | [verificato: P App. A K4, §5.6] |
| K5 Intake e onboarding | Agente intake · 3 | L3 per il brief di intake; L1 per i messaggi di onboarding | uguale | (a)(b) [P] | [verificato: P §4.3] |
| K6 Slide con la storia della relazione | Brief, Slide · 3 | L3 per noi; L1 al cliente | uguale | (a) [P] | [verificato: P App. A K6] |
| K7 Il nostro stile | template e skill · 0 | n.a. (template da preparare) | n.a. | [T] | [verificato: P App. A K7] |
| K8 Portale clienti | SersanOutreach · 5 | L3 | L3 | fase 5 [F] | [verificato: P App. A K8] |
| K9 Newsletter | Agente newsletter · 4 | L1 | L1: con una newsletter al mese, 20 invii uguali chiedono quasi due anni [non verificato: calcolo] | relay SMTP esterno [E]; regola di casa: niente esce senza un sì scritto [P] | [verificato: P §8.2] |
| K10 Andrea in entrata | «Andrea» · 5 | L3 | L3 | come G5 | [verificato: R31 §10] |
| K11 Perché si chiude, aziende simili | Analista vinto/perso · 3; Agente clienti simili · 5 | L3 per l'analisi e il passaggio all'Operatore; L1 con FIDO2 per il primo contatto | uguale | volumi [V]; un primo contatto non diventa mai «Sempre» [P] | [verificato: P §4.1] |
| K12 Formazione dei commerciali | Coach vendite · 5 | L3 | L3 | il confine fra coaching e valutazione dei lavoratori va chiarito nel parere [L] | [verificato: P §9.4] |
| K13 Mappa per i clienti | Mappatore, Intervistatore · 4-6 | L0: l'istanza separata per ogni cliente non è ancora progettata | L0 | [T] | [verificato: P App. A K13] |
| K14 Finanza nella memoria | n8n da Sirius · 3-6 | L3 (flusso fisso) | L3 | esportazione da Sirius nella fase F4; cosa sia Sirius è ancora una domanda aperta [T] | [verificato: P App. A K14; DOM n. 25] |
| K15 Acquisti | Agente acquisti · 6 | L3 per registrare le fatture dei fornitori (tipo da aggiungere); pagamenti mai automatici | uguale | pagamenti: limite fisso [P]; strumento di fatturazione, decisione 22 [T] | [verificato: P §4.9, App. A K15] |
| K16 Assistente personale | Assistente personale · 6 | L1 per ogni azione verso terzi; pagamenti mai | uguale | consenso della persona; dati di salute fuori dalla memoria aziendale [L]; quali azioni personali passino per regola non è scritto [non verificato] | [verificato: P App. A K16] |
| L1 Contratto con firma | Agente contratti, DocuSeal · 6 | L3 per la bozza e l'avviso al Project manager; L1 con FIDO2 per l'invio in firma | L1 | (a)(b) [P]; valore legale della firma semplice nel parere [L] | [verificato: P §4.3; D03 §4.1] |
| L2 Fatture e solleciti | Agente fatture · 6 | L1 con FIDO2 | L1 | chi fattura e con quale sistema, decisione 22 [L][T] | [verificato: D03 §4.1] |
| L3 Margini e cassa | Controllo di gestione · 6 | L3 | L3 | dati di Sirius dalla fase F4 [T] | [verificato: P App. A L3] |
| L4 Bandi | pipeline del board, Agente bandi · 3 | L3 per ricerca e avviso; la domanda di bando la fa una persona | uguale | — | [verificato: P §4.9] |
| L5 Assistenza nella stanza del cliente | Assistenza clienti · 6 | L3 per i task; L1 per ogni risposta | L1; L3 con «Sempre» solo per risposte ripetute a clienti noti | (a)(b)(h) [P]; canali condivisi da provare [E]; lettura del testo esterno come in K3 [T] | [verificato: P §4.6] |
| L6 Rinnovi | Agente rinnovi · 6 | L3 per i segnali; L1 per le proposte | uguale | le proposte sono offerte, quindi mai «Sempre» [P] | [verificato: P §4.6] |
| L7 Casi studio | Agente casi studio · 6 | L3 per la bozza; L1 per chiedere la testimonianza; pubblicazione come J7 | uguale | (a); sessione presidiata [P] | [verificato: P App. A L7] |
| L8 Commenti della pagina | Community manager · 4 | L1 sulla pagina aziendale; L0 sui profili dei founder, dove l'agente segnala soltanto | uguale | la voce dei founder resta umana per scelta [P]; accesso API alla pagina LinkedIn da verificare [E] | [verificato: P §4.4, §9.3] |
| L9 Sito e SEO | Agente sito · 6 | L1 per la pull request (con FIDO2); L0 per la pubblicazione su Vercel | uguale | la pubblicazione la fa una persona [P] | [verificato: P App. A L9] |
| L10 Webinar ed eventi | Agente eventi · 6 | L3 per iscrizioni e lead; L1 per inviti e follow-up | L1; L3 con «Sempre» per i promemoria agli iscritti | (a)(b) [P]; licenza dei webinar di Teams da controllare [E] | [verificato: P §4.4] |
| L11 Sorveglianza del server | Sistemista · 3 | L3 in sola lettura; L1 con FIDO2 per le patch, che approva Michele | uguale | monitoraggio nella fase F3 del board [T] | [verificato: P App. A L11; D03 §4.1] |
| L12 Allenatore | Allenatore AI · 6 | L3 | L3 | fase 6 [F] | [verificato: P App. A L12] |

## I 15 colli di bottiglia dell'autonomia

1. **Una carta per ogni invio verso l'esterno.**
   - **Causa**: ogni invio, pubblicazione, offerta, contratto e fattura passa solo con una carta. Nella milestone 1 il tipo `posta.invia` passa sempre da una carta [verificato: D03 §4.1; SPEC §4.6]. Nei canali condivisi con i clienti scrive solo il Cancello, dopo una carta [verificato: P §4.11].
   - **Natura: scelta di prudenza, non obbligo di legge.**
     - La regola 10 chiede una persona in ogni azione esterna irreversibile. R16 la motiva con la prudenza commerciale e con l'art. 4 dell'AI Act, che riguarda la formazione [verificato: P §9.1 r.10; R16 §6 r.10].
     - R16 mette il lavoro interno degli agenti a rischio minimo [verificato: R16 §4, dove la classificazione è segnata come non verificata].
     - Nei file letti nessuna norma chiede il sì di una persona per un follow-up a un cliente già incontrato [non verificato: è un'assenza nei file, non un parere].
     - Resta un vincolo legale indiretto: una mail che parte da sola deve dire che l'ha scritta un'AI (art. 50) [verificato: P §9.1 r.1].
   - **Voci colpite**: B1, B3, J3, J6, J8, K2, K3, K5, K6, K9, L1, L2, L5-L8, L10.
   - **Per toglierlo**:
     - una classe a basso rischio che passa a L2 o L3, per esempio il follow-up entro 24 ore a un dominio con una call registrata, con l'avviso AI nel testo;
     - costo: circa 2-4 giorni nel Cancello e nella Porta, più le nuove prove [non verificato: stima mia; per confronto, la parte 2 del Cancello vale 9,75 giorni, R36 §7.3];
     - serve una decisione dei CEO dopo il parere, che cambi le regole 1 e 10 e il §9.3 [verificato: P App. A B5];
     - rischio: una mail sbagliata arriva a un cliente senza che nessuno l'abbia letta.

2. **Regole «Sempre» quasi irraggiungibili.**
   - **Causa**: una regola nasce dopo 20 sì uguali per lo stesso agente, tipo d'azione e destinazione. Scade dopo 30 giorni, si rivede ogni mese, non vale mai per destinatari o domini nuovi ed esiste solo dalla fase 2 [verificato: P §5.4; R36 §5.8; PRD «Fuori»].
   - **Con i numeri di oggi non si raggiunge.** Al 5 ottobre c'erano 11 lead, 1 risposta e 0 meeting [verificato: P §7.1]. Venti sì per la stessa destinazione in 30 giorni non arrivano [non verificato: calcolo]. Il primo follow-up va sempre a un destinatario nuovo, quindi resta su carta per sempre [non verificato: mia lettura della regola].
   - **La proposta è incoerente**: l'esempio del §3 attiva una regola per «chi ha già parlato con noi», cioè per un gruppo di destinatari, non per una destinazione [verificato: P §3, §5.4]. Non è definito se «uguale» si riferisca al testo o al tipo, né come si rinnovi la regola [non verificato: non scritto nei file].
   - **Natura**: prudenza. La scadenza viene dal giudizio di sicurezza; quali messaggi possano diventare «Sempre» lo decidono i CEO dopo il parere [verificato: R36 §5.8; P App. A B5].
   - **Per toglierlo**:
     - una regola per gruppo di destinatari, per esempio «call negli ultimi 14 giorni»;
     - una soglia più bassa, per esempio 5 sì senza modifiche, e il rinnovo automatico se nel mese non ci sono revoche;
     - costo: circa 1,5-3 giorni [non verificato: stima mia];
     - serve la decisione dei CEO.

3. **Il Cancello non ha il livello L2.**
   - **Causa**: il Cancello risponde a una proposta in tre soli modi: carta, accettazione per regola, no [verificato: SPEC §4.5]. Il criterio AC-001 vieta qualsiasi effetto prima del sì [verificato: SPEC §12.4].
   - **Natura**: scelta di disegno, cioè di prudenza; non dipende dall'Agent SDK e resterebbe anche con Hermes [verificato: P §5.7].
   - **Voci colpite**: quelle del punto 1, più G6, A6 e le patch del Sistemista.
   - **Per toglierlo**:
     - una carta con il timer, che mostra l'ora di partenza e un pulsante «Ferma»; il Cancello ricalcola l'impronta del testo alla scadenza e lo stop di emergenza annulla le finestre aperte;
     - costo: circa 3-5 giorni [non verificato: stima mia];
     - vanno riscritti AC-001 e le prove sulla scadenza e sullo stop, e la revisione esterna si allarga (3.560-5.940 €) [verificato: P §14 decisione 5];
     - il silenzio che vale come sì va bene per i follow-up, non per offerte, contratti e pagamenti.

4. **Un solo effetto per giro, e il lavoro si chiude dopo una scrittura interna.**
   - **Causa**:
     - dopo `propose_action` l'agente deve chiudere il turno; lo spec sceglie una regola più stretta delle fonti, che parlavano di un effetto per turno [verificato: SPEC §2.1, §4.5; R36 §5.1 p.6];
     - anche una scrittura interna consuma l'effetto del giro, e senza carta il giro si chiude con il lavoro «fatto» [verificato: SPEC §4.3, AC-003];
     - quindi un post-call che deve registrare il meeting, creare il deal, aprire i to-do e scrivere nel canale ha bisogno di un lavoro nuovo per ogni effetto [non verificato: mia deduzione dallo spec];
     - chi legge testo esterno non può proporre azioni: ogni risposta a una mail chiede due lavori in fila [verificato: SPEC §4.4].
   - **Natura**: scelta tecnica di sicurezza [verificato: SPEC §2.1, §13].
   - **Per toglierlo**:
     - un «pacchetto» di scritture interne in una sola proposta, e la ripresa del lavoro anche dopo una scrittura per regola;
     - costo: circa 2-3 giorni, più la revisione di AC-003 e AC-005 [non verificato: stima mia];
     - la lettura separata del testo esterno va tenuta: si può solo concatenare in automatico i due lavori.

5. **Le scritture interne sono un elenco chiuso nel codice del Cancello.**
   - **Causa**: nella milestone 1 passa per regola solo `crm.nota`, e il file di configurazione non può allargare l'elenco [verificato: SPEC §4.6]. Mancano ancora i tipi per:
     - il riassunto nel canale interno e la mail del debrief alla persona;
     - l'evento nel calendario e i to-do in Jira;
     - il deal su SersanOutreach;
     - l'archiviazione della posta;
     - le proposte in BookStack.

     [non verificato: elenco ricavato dalle voci B1, C1, K1, B4, B2, K3 e A2 confrontate con SPEC §4.6]
   - **Natura**: prudenza tecnica, nata dalla revisione avversaria (rilievo grave 1) [verificato: SPEC §13].
   - **Per toglierlo**:
     - circa 0,5-1 giorno per ogni tipo nuovo [non verificato: stima mia];
     - gli esecutori di calendario, Jira e SersanOutreach sono già nei 9,75 giorni della fase 2 [verificato: R36 §7.3];
     - in alternativa, un elenco firmato fuori dal codice, con una revisione a ogni modifica.

6. **Bacheca solo dalla fase 2 e freno a tre passaggi.**
   - **Causa**: prima della fase 2 gli agenti non si passano il lavoro. Dopo, il freno ferma una catena oltre 3 passaggi o 8 messaggi e manda una carta [verificato: P §4.11, §11; R36 §5.4]. Dopo una call il percorso di un cliente coinvolge sei agenti: Analista, Post-call, Brief, Slide, Proposte e Task [verificato: P §4.10]. Se contano come una catena sola, il freno la ferma [non verificato: la bacheca non ha ancora uno spec].
   - **Natura**: prudenza contro i giri infiniti e la spesa; i numeri del freno vengono dal primo giro di proposte [verificato: R36 §5.4].
   - **Per toglierlo**:
     - anticipare bacheca e freno (5,5 giorni) alla fase 1 [verificato: R36 §7.3];
     - catene approvate in anticipo, con un tetto di spesa loro: circa 1-2 giorni [non verificato: stima mia].

7. **Niente eventi nella fase 1.**
   - **Causa**:
     - nella milestone 1 i lavori partono da un comando dato a mano;
     - n8n e la lettura periodica delle trascrizioni da Graph arrivano nella fase 2;
     - il Raccoglitore, che trova le nuove call, arriva nella fase 3.

     [verificato: SPEC §3, §5; ADR-0011; R36 §7.3; P §4.7]

     Non è scritto come partano sul banco di prova il Post-call a fine call e il debrief delle 7:00 [non verificato: assente in SPEC, PRD e R36 §7.3].
   - **Natura**: limite tecnico e di calendario, legato al posto agenti nel board [verificato: DOM n. 2].
   - **Per toglierlo**:
     - una lettura delle trascrizioni ogni 5-10 minuti e un orario per il debrief sul banco di prova, con n8n o un orario di sistema (cron): circa 1-2 giorni [non verificato: stima mia; il metodo è in R30 §3.4];
     - le notifiche di Graph al posto della lettura periodica chiedono un indirizzo pubblico [verificato: R30 §3.4];
     - i compiti programmati di Claude Team sono esclusi, perché scavalcano il Cancello [verificato: ADR-0011].

8. **Gli agenti leggono poco, e i dati dei clienti arrivano tardi.**
   - **Causa**: nella fase 1 gli agenti non leggono niente. Jira, CRM, BookStack e memoria arrivano nella fase 2, la ricerca nella memoria nella fase 3, i dati dei clienti dopo la settimana 21 [verificato: SPEC §1, §4.5; PRD «Fuori»; P §11].
   - **Natura**: in parte tecnica, cioè l'ordine di costruzione. In parte prudenza: la revisione esterna e il backup vengono prima dei dati dei clienti. In parte legale: il rosso va a Claude Team solo oscurato [verificato: P §5.6, §14].
   - **Per toglierlo**:
     - anticipare le letture su dati verdi e gialli: Jira 1,75 giorni, MCP memoria 2,5, SersanOutreach su HTTP 3,5 [verificato: R36 §7.3];
     - per anticipare i dati dei clienti, anticipare la revisione esterna e il backup 3-2-1 [verificato: P §14 decisioni 4-5].

9. **Gli agenti imparano e crescono solo con un'approvazione.**
   - **Causa**:
     - una skill nuova passa da una pull request approvata con FIDO2;
     - un founder approva ogni nuova apertura di «Andrea»;
     - un agente nuovo nasce solo con un'approvazione.

     [verificato: P App. A A6, §4.12; R31 §10; R36 §5.8] Nel video gli agenti imparano da soli [verificato: TR 3:55, 15:34-15:43].
   - **Natura**: prudenza contro le iniezioni di istruzioni e il codice non rivisto. Per gli agenti nuovi c'è anche un obbligo legale: registro dei trattamenti e DPIA (art. 30 e 35) [verificato: P §9.1 r.9; R16 §6].
   - **Per toglierlo**:
     - skill in prova con valutazioni automatiche e promozione con la finestra: circa 3-5 giorni [non verificato: stima mia];
     - per G6, aperture con la finestra dentro la frase fissa che dichiara l'AI: circa 0,5-1 giorno oltre ai 2-3 già stimati [verificato: R31 §11 per i 2-3 giorni; il resto è una stima];
     - Hermes scrive e cura da solo le proprie skill [verificato: R10 §4.2]. Il suo gateway però aveva 276 problemi aperti, di cui 9 di sicurezza, al 25/10/2026 [verificato: R36 «In breve»].

10. **L'outbound non può diventare autonomo.**
    - **Causa**:
      - lanci, invii in blocco e cancellazioni restano a una persona;
      - su LinkedIn ogni messaggio va approvato;
      - i primi contatti chiedono la FIDO2 e non diventano mai «Sempre»;
      - l'autopilot LinkedIn che SersanOutreach ha già, entro tetti giornalieri, resta fuori dal perimetro degli agenti.

      [verificato: P §7.1, §7.3, §7.4, §5.4]
    - **Natura**: legale per l'email verso l'Italia, dove il Garante chiede il consenso anche per i contatti aziendali [verificato: R16 sintesi p.7, §3]. Prudenza per LinkedIn e per i primi contatti. Il rischio di blocco dell'account LinkedIn non è nei file letti [non verificato].
    - **Per toglierlo**:
      - una carta per campagna invece che per messaggio, con nuove operazioni in SersanOutreach e nel Cancello: circa 2-4 giorni [non verificato: stima mia];
      - prima serve il parere sull'email B2B verso l'Italia (decisione 2, tetto 2.500 €) [verificato: P §14].

11. **La pubblicazione resta a mano.**
    - **Causa**: dopo il sì, Alberto programma i post in una sessione presidiata. Sui profili dei founder l'agente segnala soltanto. Postiz arriva nella fase 4 [verificato: P §4.4, §8.2, §9.3, §11].
    - **Natura**: regola di casa delle direttive marketing, cioè prudenza, non legge [verificato: P §8.2].
    - **Per toglierlo**:
      - un collegamento del Cancello verso Postiz per la pagina aziendale (carta, poi «Sempre»): circa 1-2 giorni [non verificato: stima mia];
      - anticipare Postiz (4,5 giorni insieme a listmonk) [verificato: R36 §7.3] e cambiare la direttiva;
      - verificare l'accesso API alla pagina LinkedIn [verificato: P App. A L8].

12. **Le carte rallentano: FIDO2, solo Teams, scadenza a 48 ore.**
    - **Causa**:
      - offerte, contratti, fatture e primi contatti chiedono la chiave FIDO2; il disegno tecnico la estende a solleciti, codice e infrastruttura [verificato: P §5.4; D03 §4.1];
      - si approva solo in Teams [verificato: P §4.11];
      - lo spec propone carte che scadono dopo 48 ore, quindi un fine settimana basta a farle scadere [verificato: SPEC §9 D1].
    - **Natura**: prudenza di sicurezza, più un limite tecnico: l'identità di chi approva arriva solo da Entra.
    - **Per toglierlo**:
      - FIDO2 solo dove la chiede la proposta: 0 giorni;
      - una scadenza diversa per ogni classe, con la configurazione;
      - approvazioni da Telegram con l'identità collegata: circa 1-2 giorni [non verificato: stime mie];
      - promemoria delle carte con ntfy, già sulla macchina Oracle [verificato: D03 §3.4].

13. **Il sistema non regge da solo le 24 ore.**
    - **Causa**:
      - con una sola linea internet gli agenti si fermano;
      - dopo un blackout il server va riacceso a distanza;
      - l'unica GPU viene prestata al laboratorio;
      - oltre 16 sessioni insieme serve altra RAM.

      [verificato: P §13, §6.3; DOM n. 22] Un lavoro interrotto finisce «fallito» e non riparte da solo; un'esecuzione incerta va a una persona [verificato: SPEC §4.2, §4.8]. P scrive che dopo un guasto della linea i lavori «ripartono», ma lo spec non prevede nuovi tentativi [verificato: P §13; non verificato: assente nello spec].
    - **Natura**: tecnica e d'infrastruttura. Il rifiuto di ritentare è prudenza, contro i doppi effetti.
    - **Per toglierlo**:
      - linea di riserva: 77-200 € una tantum e 10-11 € al mese (decisione 13);
      - riaccensione automatica del server: scelta di Michele, 0 € (domanda 22);
      - seconda GPU: 880-1.220 € (decisione 12); RAM: 690-830 € (decisione 11) [verificato: P §14; DOM n. 22, 24];
      - nuovi tentativi automatici per i lavori falliti per un errore di rete: circa 1 giorno [non verificato: stima mia].

14. **Scelte legali in attesa.**
    - **Causa**: sono ancora aperti
      - l'email B2B verso l'Italia;
      - la registrazione delle call e l'art. 4 dello Statuto dei lavoratori;
      - i dati rossi verso Claude Team;
      - il consenso per «Andrea»;
      - il confine fra coaching e valutazione dei lavoratori;
      - la via per LinkedIn e la firma elettronica;
      - i metadati di M365.

      [verificato: P §9.4; R16 §7]
    - **Natura**: legale. Alcuni obblighi sono già certi: dichiarare l'AI (art. 50), non stimare le emozioni (art. 5(1)(f)), avere il consenso per le chiamate automatizzate (art. 130) [verificato: R16 sintesi, §2, §4].
    - **Per toglierlo**: il parere unico (decisione 2, tetto 2.500 €) e la DPIA [verificato: P §9.4, §14]. Il codice non toglie questo limite: può solo prepararsi alle risposte.

15. **Gli agenti chiave arrivano tardi e partono spenti.**
    - **Causa**:
      - gli agenti al lavoro sono 3 a fine fase 1, 14 a fine fase 2, circa 32 a fine fase 3, e tutti e 57 solo alla settimana 53;
      - Agenda, Smistatore posta, Agente email e Brief arrivano nella fase 3; contratti, fatture e assistenza nella fase 6;
      - ogni automazione parte in prova per 1-2 settimane.

      [verificato: P §4.12, §11, §9.2]
    - **Natura**: scelta di piano, legata alla capacità di circa 6,5 giorni di sviluppo a settimana, più prudenza [verificato: R36 §7.1].
    - **Per toglierlo**:
      - con circa 9 giorni di sviluppo a settimana dalla fase 2 il calendario scende da circa 53 a circa 42 settimane [verificato: P §15];
      - portare nelle fasi 1-2 ciò che rende possibile l'autonomia, cioè eventi, letture, bacheca, «Sempre» e finestra, prima di aggiungere agenti [non verificato: proposta mia];
      - chiudere la prova quando l'automazione ha fatto un certo numero di casi senza errori, invece che dopo un tempo fisso [non verificato: proposta mia].
