# Profilo di autonomia delle alternative studiate (primo e secondo giro)

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **RAP3**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

## Come leggere

- **Livelli.** Uso sempre i nomi del compito: L0 a mano, L1 carta, L2 finestra, L3 autonomo.
  - Alcune proposte usano sigle proprie: la E ha «L0, L1, L2», la C «Livello 0, 1, 2», i dots hanno quattro livelli e Paperclip usa Allowed, Ask first e Off. Le traduco nei livelli di Alberto [non verificato: mappatura mia].
- **«Pronta»** è ciò che la proposta mette in funzione al primo rilascio utile, con le regole con cui parte.
- **«Raggiungibile»** è ciò che la stessa proposta prevede a regime, con le sue regole. Non è ciò che il prodotto farebbe se togliessimo i guardrail.
- **Fonti.** Tutti i file stanno in `C:\Users\alber\sersan-agent-os`. Uso queste sigle:
  - **00, 10, 11, 12, 17, 18, 26, 27** sono `ricerca/NN-*.md`;
  - **20-A … 20-G** sono `ricerca/20-proposta-*.md`;
  - **21-visione, 21-ceo, 21-cpto, 21-compliance** e **35-visione, 35-ceo, 35-cpto, 35-sicurezza** sono i giudizi;
  - **22** è `ricerca/22-architettura-scelta.md`, **36** è `ricerca/36-architettura-v2.md`;
  - **34-1, 34-2, 34-3** sono le proposte del secondo giro;
  - **02-alt** è `docs/02-alternative.md`; **PRES** è `PRESENTAZIONE-CEO.md` (v2.1 dell'8/11/2026);
  - **TR** è la trascrizione di riferimento, con il minuto.
- **Date.** I rapporti del primo giro sono del 24/10/2026, quelli del secondo del 25/10/2026.
- **Costi.** Il primo giro dà il totale mensile di tutto lo stack. Il secondo dà soprattutto la spesa «in più rispetto a oggi». Le due serie non si confrontano riga per riga [verificato: 20-A §7; 34-1 §8.1, metodo].

## In breve

1. **La trascrizione di riferimento lavora quasi tutta a L3 autonomo.** Il post-call è completo e comprende la mail al cliente. L'agente vocale lavora 24 ore su 24 e impara dai rifiuti. Nel testo non compare nessun meccanismo di approvazione (§0).
2. **Ogni alternativa parte da L1 carta (o da L0 a mano) per ciò che esce.** Arriva a L3 autonomo solo con regole «Sempre», limitate per classe o per destinazione. Le eccezioni sono le scritture interne e la richiamata di Andrea a chi la chiede, già L3 autonomo nella maggior parte delle proposte.
3. **L2 finestra non c'è in nessuna alternativa.** In tutte, una carta che scade vale come «no».
4. **Le funzioni autonome già pronte sono più ricche in Grok Bot, Hermes, buzz e Paperclip.** Le proposte che li usano però le tengono strette (§1).
5. **Il secondo giro ha messo la capacità e il perimetro del server davanti all'autonomia** su cinque punti: i voti di costo e di aderenza al board, il tetto di sessioni, la voce legata alla GPU, l'esclusione dei motori in abbonamento e la continuità senza una riserva in cloud. L'ha difesa invece sull'ampiezza: tutte le 57 figure restano agenti veri (§3).

---

## 0. Il metro: la trascrizione di riferimento

L'imprenditore del video descrive questo sistema:

- **25 agenti** in background: chi raccoglie, chi pulisce, chi indicizza, chi agisce [verificato: TR, min. 3:41-3:55].
- **Agenti che si parlano.** Gli agenti «imparano e autoimparano» e si parlano in una chat condivisa [verificato: TR, min. 3:56-4:07].
  - Chi raccoglie annuncia tre nuove call e l'agente degli appuntamenti verifica cosa fissare [verificato: TR, min. 4:08-4:18].
  - Si aiutano a chiudere i to-do già fatti [verificato: TR, min. 4:22-4:31].
- **Post-call.** Dopo una call, un agente:
  - scrive punti e prossimi passi nel canale del cliente;
  - crea l'opportunità nel CRM;
  - manda la mail di follow-up al cliente;
  - assegna i to-do.

  Tutto «in modo totalmente autonomo» [verificato: TR, min. 4:42-5:07].
- **Debrief** come primo passo della giornata, alle 5:30 [verificato: TR, min. 5:14-5:27].
- **Brief e offerte** prima e dopo gli incontri, costruiti in automatico [verificato: TR, min. 7:44-9:06].
- **Coaching.** Dopo ogni call di vendita va al venditore e al suo responsabile, in modo «totalmente automatizzato» [verificato: TR, min. 14:38-14:52].
- **Agente vocale.**
  - Richiama la lead entro 90 secondi, si dichiara AI e fissa l'appuntamento con una persona [verificato: TR, min. 14:55-15:23].
  - Impara dai rifiuti e cambia l'apertura [verificato: TR, min. 15:34-15:44].
  - Lavora 24 ore su 24, 7 giorni su 7 [verificato: TR, min. 15:58-16:02].
- **Organizzazione.**
  - Oltre 100 agenti in organigramma [verificato: TR, min. 16:20-16:42].
  - Policy AI e banca dei token [verificato: TR, min. 10:49-10:56].
  - Aree in cui l'AI non entra per scelta [verificato: TR, min. 21:19-21:29].
- **Approvazioni.** Nel testo non si parla di approvazioni né di limiti [verificato: lettura integrale di TR]. Che non esistano non si può dedurre.
- **In livelli:** post-call intero L3 autonomo, voce 24/7 L3 autonomo, apprendimento dai rifiuti L3 autonomo [non verificato: mappatura mia].

---

## 1. Primo giro (24/10/2026): sette architetture

### A. Hermes con il Cancello: 159/240, prima

- **L'idea.** Hermes Agent (licenza MIT) orchestra profili con nome, una bacheca kanban, cron e canali. Il Cancello è l'unico che agisce verso l'esterno [verificato: 20-A §1].
- **Orari ed eventi.**
  - Debrief per persona alle 7:00 in DM, via cron [verificato: 20-A §2, voce C1].
  - Hermes ha di suo cron in linguaggio naturale, job senza modello e sorveglianze che svegliano il modello solo se qualcosa cambia [verificato: 10 §4.2].
  - I webhook firmati (fine call di Recall.ai, modulo del sito, Instantly) entrano dal tunnel. L'ingresso del Cancello apre una card per il profilo giusto [verificato: 20-A §1].
- **Passaggi e dialogo.**
  - La kanban è il registro dei passaggi. Slack `#agenti` fa da vetrina, con un freno a 8 messaggi consecutivi fra agenti per thread [verificato: 20-A §1, §5].
  - La «chat fra bot» di Hermes è un'interfaccia desktop: sul server la vetrina va costruita [verificato: 20-A §9; 10 §4.1].
- **Memoria e apprendimento.**
  - Memoria: Notion via MCP, pgvector con embedding locali. La memoria interna di Hermes è piccola (2.200 + 1.375 caratteri) [verificato: 20-A §2; 10 §4.2].
  - Skill: Hermes le scrive e le cura da solo, quindi la voce A6 è «pronta». Le scritture in memoria vanno in coda di approvazione [verificato: 20-A §2, A6].
  - Rifiuti di Andrea: analisi settimanale, nuova apertura accesa da una carta [verificato: 20-A §2, G6].
- **Approvazioni e limiti.**
  - Nessun profilo ha strumenti che inviano; si parte con tutto su carta [verificato: 20-A §1, §5].
  - Una regola «Sempre» nasce per classe e destinatario dopo 20 carte approvate senza modifiche. Mai per offerte, primo contatto, pagamenti e cancellazioni, che restano su carta [verificato: 20-A §5].
  - `/stop` in Slack ferma cron e kanban e fa rifiutare ogni effetto al Cancello [verificato: 20-A §5].
  - Il giudice di compliance nota che nel post-call Hermes scrive in Notion e nel CRM senza carta [verificato: 21-compliance §2].
  - Le approvazioni native di Hermes coprono solo la shell e scadono dopo 300 s [verificato: 20-A §5].
- **Canali, 24/7, voce.**
  - Slack in Socket Mode. Il gateway di Hermes ha 22 plugin di piattaforma [verificato: 20-A §1; 10 §4.2].
  - Gira come servizio sul server. Hermes Cloud (Londra) è la riserva fredda, solo per i profili senza dati dei clienti [verificato: 20-A §3].
  - Andrea usa ElevenLabs e un numero Twilio, fuori da Hermes, nelle settimane 9-12 dopo il parere legale [verificato: 20-A §2, §6]. Hermes da solo telefona solo in uscita, tramite terzi [verificato: 10 §5].
- **Pronto e da costruire.**
  - Pronte solo 4 voci (A4, A6, B4, C3) [non verificato: conteggio mio sulla tabella di 20-A §2].
  - 60 gp; primo rilascio alla settimana 5 con 18 gp [verificato: 20-A §6].
  - I giudici lo spostano alla settimana 7-8, con un Cancello da circa 21 gp [verificato: 21-ceo §3; 22 §1].
- **Server.** Circa 110 GB sui 128 di allora. La GPU fa solo lavori leggeri, perché Hermes chiede almeno 64.000 token di contesto [verificato: 20-A §3].
- **Costi.**
  - Listino 309 / 892 / 2.056 €/mese (minimo / consigliato / completo).
  - Uscita di cassa oggi 279 / 759 / 1.724 €.
  - A regime +446,70 € di Claude Team.
  - UPS 1.163-1.293 € una tantum [verificato: 20-A §7].
  - Abbonamenti: API Anthropic, Claude Team, Recall.ai, ElevenLabs con Twilio, Slack, Notion, Hermes Cloud come riserva [verificato: 20-A §3].
- **Sicurezza ancora aperta.**
  - Hermes si dichiara «single-tenant»; l'unico confine è il sistema operativo.
  - Contesti mescolati fra profili.
  - 5 patch in 10 giorni e oltre 5.000 issue aperte [verificato: 10 §3, §5, §6].
- **Punteggi ed esito.**
  - Voti: visione 41, CEO 40, CPTO 41, compliance 37 [verificato: 02-alt §2.1].
  - Vince il primo giro per equilibrio [verificato: 02-alt §2.2].
  - Nel piano scelto allora: chat fra agenti nelle settimane 14-16, Andrea nelle 17-20, prima regola «Sempre» nelle 21-24 [verificato: 22 §5].
  - Nel secondo giro lascia il posto all'Agent SDK [verificato: 36 §6].
- **Autonomia.**
  - Pronta: scritture interne e debrief L3 autonomo, uscite L1 carta, skill L3 autonomo (nativo).
  - Raggiungibile: uscite ripetitive L3 autonomo per classe e destinatario, Andrea L3 autonomo; le classi delicate restano L1 carta [non verificato: mappatura mia].

### B. buzz di Block: 140,5/240, quarta

- **L'idea.** buzz è la stanza comune: persone e agenti negli stessi canali. Ogni agente è un membro con nome, chiave, proprietario e memoria. Il cervello è Claude Code con la chiave API. Accanto c'è un nostro `sersan-gate` [verificato: 20-B §1].
- **Orari ed eventi.**
  - Workflow `schedule`, con cron in UTC o intervallo di almeno 60 s [verificato: 17 §5].
  - Workflow `webhook` senza firma del corpo né anti-replay: l'ingresso firmato lo scriviamo noi [verificato: 17 §5, §8].
  - SersanOutreach deve imparare a emettere webhook; oggi non lo fa [verificato: 20-B §4].
- **Passaggi e dialogo.**
  - Di serie: delega con @menzione, le persone leggono tutto, trascrizione del turno dal vivo [verificato: 17 §0, §5].
  - Manca il freno: gli autori hanno visto oltre 21 risposte in catena. La proposta lo aggiunge in un fork: 8 risposte per thread, catene di 3, tetto in dollari [verificato: 17 §5; 20-B §1].
- **Memoria e apprendimento.**
  - Memoria per agente, cifrata, con un nucleo fino a 64 KB. Nessuna memoria condivisa fra agenti [verificato: 17 §5].
  - Nessun auto-apprendimento di serie. Un agente può proporre un agente nuovo come bozza [verificato: 17 §5].
  - Nella proposta le skill stanno in git; quelle che si curano da sole arrivano con Hermes in fase 4. I rifiuti di Andrea diventano una proposta di prompt con carta [verificato: 20-B §2].
- **Approvazioni e limiti.**
  - Di serie le approvazioni non funzionano: un passo `request_approval` fa fallire il flusso, e i permessi partono in «bypass» [verificato: 17 §0, §5].
  - Nella proposta: email, pubblicazioni e chiamate passano su carta; le scritture interne passano senza; il cambio di stadio di un deal passa su carta; cancellazioni e pagamenti sono negati [verificato: 20-B §5].
  - Dopo 30 giorni senza correzioni, i CEO possono rendere automatica una classe intera, mai su decisione di un modello [verificato: 20-B §5].
  - Stop: `!shutdown` e un arresto d'emergenza nel gate [verificato: 20-B §5].
- **Canali, 24/7, voce.**
  - App buzz per computer e telefono, in VPN; le carte anche su Telegram; i clienti restano fuori [verificato: 20-B §1, §8].
  - Nessuna integrazione di serie con Slack o email [verificato: 17 §5].
  - Per lavorare 24/7 gli agenti devono girare sul server, ma il percorso passo per passo non è documentato [verificato: 17 §7].
  - Le chiamate di gruppo (huddle) hanno ascolto e voce solo in inglese [verificato: 17 §5]. Andrea usa ElevenLabs e Twilio, con consenso controllato dal gate, nelle settimane 10-14 [verificato: 20-B §2, §6].
- **Pronto e da costruire.**
  - Pronte A7 (senza freno), B4, C3, F5 e I3 [verificato: 20-B §2].
  - Le aggiunte nostre valgono 18-23 gp. Primo rilascio con 24 gp in 5 settimane, totale circa 81 gp [verificato: 20-B §1, §6].
- **Server.** Circa 128 GB a regime, al limite: si propone di salire a 192 GB. La GPU da 8 GB resta accesa per il giudice, gli embedding e la trascrizione [verificato: 20-B §3].
- **Costi.**
  - Totale 309 / 856 / 2.014 €/mese; esborso con i crediti 279 / 723 / 1.681 €; a regime 756 / 1.303 / 2.460 €.
  - Licenza 0 €; Slack non serve più.
  - UPS 1.163-1.293 € una tantum [verificato: 20-B §7].
- **Sicurezza ancora aperta.**
  - Versione prima della 1.0, che si dichiara «Not finished».
  - La chiave dell'agente sta nell'ambiente del processo.
  - Il telefono riceve la chiave privata del computer.
  - L'app per Windows è in alpha e scrive segreti in chiaro.
  - La catena d'audit segnala le modifiche ma non le impedisce [verificato: 17 §2, §8; 21-compliance §2].
- **Punteggi ed esito.**
  - Voti 36 / 33 / 35 / 36,5; è la più indipendente del giro [verificato: 02-alt §2.1-2.2].
  - Scartata come chat di tutti: approvazioni che falliscono, nessun freno ai giri [verificato: 22 §1].
  - Oggi è in prova come stanza degli agenti, nella fase 4 [verificato: 36 §5.6; PRES §11].
- **Autonomia.**
  - Pronta: interne L3 autonomo, uscite L1 carta. Senza il gate, buzz agisce a L3 autonomo e senza freni.
  - Raggiungibile: L3 autonomo per classi intere, Andrea L3 autonomo; cancellazioni e pagamenti negati [non verificato: mappatura mia].

### C. Grok Bot in abbonamento, il server come cassaforte: 113/240, sesta

- **L'idea.** I Bot di Grok, che girano nel cloud di Cursor negli USA, fanno il lavoro che si vede. Il server custodisce i dati. I dati sono divisi in tre colori [verificato: 20-C §1].
- **Orari ed eventi.**
  - Fino a 50 routine per Bot, con almeno 5 minuti fra due esecuzioni [verificato: 11 §2.4].
  - Le routine partono anche da Slack, GitHub, Linear, Teams, email del Bot, webhook e X [verificato: 11 §2.4].
  - Debrief alle 5:30 dal Bot principale [verificato: 20-C §2].
  - Un dispatcher sul server raggruppa gli eventi, per esempio «3 nuove call» [verificato: 20-C §1].
- **Passaggi e dialogo.**
  - Di serie: il Bot principale delega, chat di gruppo da 2 a 6 Bot, passaggi leggibili, Team Bots in Slack [verificato: 11 §2.1, §2.5].
  - È il prodotto più vicino a una «squadra di agenti con nome che si parlano» [verificato: 11 §9].
- **Memoria e apprendimento.**
  - Memoria per Bot e di team, nessun indice vettoriale, nessuna esportazione [verificato: 11 §2.2, §7.1].
  - Di serie: skill che si correggono e «Teach a task» da 10 minuti [verificato: 11 §2.4].
  - Imparare dai rifiuti non c'è nel prodotto [verificato: 11 §5]. Nella proposta, una persona approva la nuova apertura [verificato: 20-C §2].
- **Approvazioni e limiti.**
  - Di serie: «consenti una volta», «consenti sempre», «nega».
  - Nel lavoro non presidiato le approvazioni scadono in circa 10 minuti [verificato: 11 §2.6].
  - I termini mettono ogni azione a carico del cliente e chiedono la revisione di una persona prima delle comunicazioni esterne [verificato: 11 §7.4].
  - Nella proposta:
    - Livello 0: tutto resta bozza;
    - Livello 1: dopo 30 giorni senza correzioni le scritture interne diventano automatiche;
    - Livello 2: invii esterni automatici solo dentro i tetti del pilota di SersanOutreach, mai da Grok [verificato: 20-C §5].
  - Uno stop d'emergenza non è descritto [verificato: assente in 20-C].
- **Canali, 24/7, voce.**
  - App Grok sul telefono e sul computer, più Slack [verificato: 20-C §1].
  - I computer cloud sono sempre accesi, ma c'è una quota settimanale non pubblicata e la pagina di stato ha registrato cinque incidenti dal 13 al 19/10 [verificato: 11 §4.1, §7.3].
  - Grok non ha telefonia. Andrea parte dal server con ElevenLabs, nelle settimane 10-13 [verificato: 11 §5; 20-C §4, §6].
- **Pronto e da costruire.** Debrief e brief su dati pubblici in 2 settimane. Su 66 gp, solo circa 12 sono configurazione di Grok [verificato: 20-C §6].
- **Server.** Circa 104 GB [verificato: 20-C §3].
- **Costi.**
  - Posti Grok 107 / 322 / 715 €/mese; architettura 289 / 781 / 1.740 €; tutto compreso 402 / 1.146 / 2.631 € [verificato: 20-C §7].
  - Ricalcolata sulla stessa base delle altre, circa 1.058 € nello scenario consigliato [verificato: 21-ceo §2].
- **Sicurezza ancora aperta.**
  - Dati negli USA e modello invisibile.
  - Un solo computer condiviso da tutti i Bot di un utente.
  - Audit solo sul piano Enterprise [verificato: 11 §2.3, §2.6, §7].
  - Contrasta la regola 7 sui dati dei lead in servizi beta [verificato: 21-compliance §2].
- **Punteggi ed esito.**
  - Voti 27 / 28 / 30 / 28: la più veloce a dare valore, l'ultima per sicurezza e indipendenza [verificato: 02-alt §2.1-2.2].
  - Scartata [verificato: 22 §1]. Resta facoltativo un mese di prova su soli dati pubblici, circa 54 € [verificato: PRES §14, decisione 23].
- **Autonomia.**
  - Pronta: interne L3 autonomo, uscite L0 a mano (sono bozze che invia una persona).
  - Raggiungibile: uscite L3 autonomo solo tramite SersanOutreach; dai Bot restano L0 a mano [non verificato: mappatura mia].

### D. OpenAI Dots e Workspace Agents: 105/240, settima

- **L'idea.** Un dot per persona: un agente sempre acceso, con un computer Linux e Chrome nel cloud. I Workspace Agents condivisi fanno da organigramma. Il server tiene i dati dietro un gateway MCP [verificato: 20-D §1].
- **Orari ed eventi.**
  - Il dot ha promemoria e controlli ricorrenti. Reagisce a eventi da Gmail, Slack, GitHub e MCP; i webhook generici non sono documentati [verificato: 18 §2.2].
  - I Workspace Agents partono a orario, da Slack o da una chiamata API [verificato dall'autore di 20-D §1 via proxy; non confermato da 21-ceo §3].
- **Passaggi e dialogo.** Fra agenti non c'è un dialogo di serie: si passa da un relay sul server, con un tetto di turni [verificato: 20-D §2, §8].
- **Memoria e apprendimento.**
  - La memoria del dot non si vede e non si cancella in modo selettivo [verificato: 20-D §5; 21-compliance §2].
  - Il dot «impara dal feedback», con un meccanismo non spiegato [verificato: 20-D §2, A6].
- **Approvazioni e limiti.**
  - Di serie ci sono quattro livelli: agire, agire se pre-approvato, chiedere, passare la mano. In più c'è la revisione di un secondo modello [verificato: 18 §2.2].
  - Si parte con «chiedere» su ogni azione esterna [verificato: 20-D §5].
  - Un tipo di azione diventa «pre-approvato» dopo 20 approvazioni pulite e un sì scritto dei CEO [verificato: 20-D §5].
  - Pagamenti, LinkedIn, offerte e contratti restano «passare la mano» [verificato: 20-D §5].
  - La pausa del dot non ferma i compiti pianificati: lo stop è nostro [verificato: 18 §2.2; 20-D §5].
- **Canali, 24/7, voce.**
  - App ChatGPT, Slack e Teams; il dot è sempre acceso [verificato: 18 §2.2].
  - Il dot si può chiamare a voce ma non telefona. Andrea usa ElevenLabs e Twilio, nelle settimane 10-13 [verificato: 18 §2.2; 20-D §6].
- **Pronto e da costruire.** Valore in 2 settimane senza server (8 gp); totale circa 52 gp [verificato: 20-D §6].
- **Server.** Circa 82 GB [verificato: 20-D §3].
- **Costi.**
  - Circa 324 / 811 / 1.640 €/mese [verificato: 20-D §7].
  - Ricalcolata sulla stessa base, circa 1.190 € più crediti OpenAI di prezzo ignoto [verificato: 21-ceo §2].
- **Sicurezza ancora aperta.**
  - Prodotto uscito il 29/09; nelle prime 48 ore persi permessi e messaggi [non verificato: fonti terze, 20-D §8].
  - Nei test di OpenAI le violazioni salgono dall'8,6 % al 19,7 % passando da catene di 5 a catene di 10 compiti [verificato: 20-D §5].
- **Punteggi ed esito.** Voti 26 / 25 / 27 / 27. Scartata: un agente per persona, nel Regno Unito solo con Business Premium, crediti di prezzo ignoto [verificato: 02-alt §2.1; 22 §1].
- **Autonomia.**
  - Pronta: uscite L1 carta, dot sempre acceso.
  - Raggiungibile: L3 autonomo per tipo di azione pre-approvato; offerte, contratti, pagamenti e LinkedIn L0 a mano [non verificato: mappatura mia].

### E. Claude-native, con un demone nostro e l'Agent SDK: 140/240, quinta

- **L'idea.** Un demone nostro (`sersand`) decide chi può agire, chiede il sì, esegue, conta i token e traccia. Claude è la forza lavoro, sulla chiave API [verificato: 20-E §1].
- **Orari ed eventi.**
  - Report del mattino alle 05:30 su Slack e Telegram [verificato: 20-E §2].
  - Webhook firmati via tunnel per le call, il modulo e SersanOutreach [verificato: 20-E §1, §4].
- **Passaggi e dialogo.** `#agenti` e i passaggi con freno vanno costruiti: arrivano alla settimana 13 [verificato: 20-E §2, §9].
- **Memoria e apprendimento.**
  - Memoria: pgvector, un archivio di file Markdown in git, il CRM [verificato: 20-E §1].
  - Un agente revisore propone ogni settimana modifiche alle skill e una persona approva [verificato: 20-E §2, A6].
  - Rifiuti di Andrea: nuova apertura su carta, con prova A/B [verificato: 20-E §2, G6].
- **Approvazioni e limiti.**
  - Carta con impronta del testo, una sola esecuzione; il silenzio non vale come sì [verificato: 20-E §5].
  - I gradini della proposta:
    - «L0»: carta sempre;
    - «L1»: regola «Sempre» stretta (destinatario, modello di testo, tetto) dopo 20 approvazioni;
    - «L2»: controllo a campione.

    Mai per invii a freddo, offerte, cancellazioni, pagamenti. Andrea parte in «L1» solo per le lead che hanno dato consenso; `/stop` da Telegram o Slack [verificato: 20-E §5].
  - La «L1» di E corrisponde al mio L3 autonomo dentro una regola [non verificato: mappatura mia].
- **Canali, 24/7, voce.**
  - Slack e Telegram; il demone gira sul server; le pagine web non fidate si leggono con i Managed Agents, fuori dal server [verificato: 20-E §1, §3].
  - Andrea usa ElevenLabs e Twilio, nelle settimane 14-17 [verificato: 20-E §6].
- **Pronto e da costruire.**
  - 15-22 mila righe nuove, 119 gp in 20 settimane.
  - Primo rilascio alla settimana 8, debrief dalla settimana 5 [verificato: 20-E §1, §6].
- **Server.** 116 GB su 128, fino a 8 sessioni insieme [verificato: 20-E §3].
- **Costi.** Listino 298 / 966 / 2.358 €/mese; esborso con i crediti 243 / 749 / 1.807 € [verificato: 20-E §7].
- **Sicurezza ancora aperta.**
  - È codice nostro mai andato in produzione, senza revisione esterna.
  - Le carte su Telegram portano il testo delle mail [verificato: 21-compliance §2, §5].
- **Punteggi ed esito.**
  - Voti 34 / 31 / 37 / 38: prima per la privacy [verificato: 02-alt §2.1].
  - Allora resta l'uscita prezzata; con il board di Michele diventa il motore sull'Agent SDK [verificato: 22 §1; 02-alt §2.3].
- **Autonomia.**
  - Pronta: report e recap interno L3 autonomo, uscite L1 carta.
  - Raggiungibile: L3 autonomo stretto per destinatario, poi controllo a campione; Andrea L3 autonomo per chi ha dato consenso [non verificato: mappatura mia].

### F. Paperclip come piano di controllo: 148,5/240, seconda

- **L'idea.** Paperclip (licenza MIT):
  - mette gli agenti in organigramma;
  - assegna il lavoro come issue;
  - li sveglia;
  - conta la spesa e li ferma al tetto.

  Il lavoro lo fanno lavoratori collegati, per esempio Claude Code con la chiave API [verificato: 20-F §1].
- **Orari ed eventi.**
  - Routine cron e un battito periodico che sveglia gli agenti; debrief alle 5:30 [verificato: 20-F §1-2].
  - La scheda di stato non spende token se i fatti non cambiano [verificato: 20-F §2].
  - I webhook da SersanOutreach vanno scritti [verificato: 20-F §4].
- **Passaggi e dialogo.** Si delega creando un'issue, con costo e responsabile: una menzione da sola non assegna lavoro. In Slack c'è un bot per agente [verificato: 20-F §1-2].
- **Memoria e apprendimento.**
  - La memoria è fuori dal nucleo: Notion e pgvector [verificato: 20-F §1].
  - Skill Studio, con agenti che imparano e riflettono; ogni skill nuova passa da un'approvazione [verificato: 20-F §2, A6].
- **Approvazioni e limiti.**
  - Le impone il programma, non il prompt: Allowed, Ask first con gli argomenti firmati, Off [verificato: 20-F §1, §5].
  - Allowed: letture e scritture interne nel CRM. Ask first: aggiornamento dei deal. Off: approvare invii e scrivere su Metricool [verificato: 20-F §4].
  - Le regole «approva ancora uguale» arrivano dopo un periodo misurato. Mai per invii a lead nuovi, chiamate, pubblicazioni, cancellazioni, pagamenti [verificato: 20-F §5].
  - Le decisioni scadono dopo 7 giorni e la scadenza vale come no [verificato: 20-F §5].
  - Stop: pausa dell'azienda e kill switch di SersanOutreach [verificato: 20-F §5].
- **Canali, 24/7, voce.**
  - Slack, l'interfaccia web e il telefono; Hermes porta Telegram in fase 3 [verificato: 20-F §1].
  - Andrea non passa dal battito (un controllo ogni 30 s) ma dal webhook del modulo, nelle settimane 10-16 [verificato: 20-F §1, §6].
- **Pronto e da costruire.**
  - 10 voci pronte, 22 da adattare, 9 da costruire.
  - È pronta la governance, non il «cervello» né la voce [verificato: 20-F §2].
  - Primo rilascio 18 gp in circa 4 settimane, poi circa 2 gp al mese di manutenzione [verificato: 20-F §6].
- **Server.** Circa 106 GB, più 12-16 GB per il sistema; Paperclip non usa la GPU [verificato: 20-F §3].
- **Costi.** Circa 315 / 1.029 / 2.319 €/mese; esborso con i crediti circa 279 / 873 / 1.937 € [verificato: 20-F §7].
- **Sicurezza ancora aperta.**
  - 6 avvisi critici nel 2026, fra cui un'esecuzione di codice da remoto senza autenticazione e un agente che ha mandato email vere.
  - Default pericolosi (`dangerouslySkipPermissions`, telemetria accesa, filtro anti-iniezione in inglese).
  - Nessuna catena di hash nell'audit [verificato: 20-F §5; non riverificato dai giudici: 21-visione §3].
- **Punteggi ed esito.**
  - Voti 37 / 38 / 36 / 37,5 [verificato: 02-alt §2.1].
  - Governance senza cervello: resta un innesto [verificato: 22 §1]. Oggi è una prova nella fase 6 [verificato: PRES §11].
- **Autonomia.**
  - Pronta: interne, battito e routine L3 autonomo; uscite L1 carta; pubblicazioni L0 a mano.
  - Raggiungibile: uscite ripetitive L3 autonomo; lead nuovi, chiamate, pubblicazioni, cancellazioni e pagamenti fermi a L1 carta o L0 a mano; Andrea L3 autonomo [non verificato: mappatura mia].

### G. Ibrido libero: 143,5/240, terza

- **L'idea.** Il pezzo migliore per ogni livello:
  - Slack Pro con Claude Tag come casa comune;
  - Paperclip per il controllo;
  - n8n per i flussi fissi;
  - come lavoratori l'Agent SDK, i Managed Agents e un Hermes per persona;
  - Notion e pgvector per la memoria [verificato: 20-G §1].
- **Orari ed eventi.**
  - Routine alle 7:00 [verificato: 20-G §2].
  - I Managed Agents hanno esecuzioni pianificate con cron [verificato: 12 §1].
  - I webhook firmati in n8n aprono task in Paperclip [verificato: 20-G §1].
- **Passaggi e dialogo.**
  - Paperclip è il registro, `#agenti` la vetrina, il freno sta nel codice [verificato: 20-G §2, §5].
  - Claude Tag in Slack ha una modalità proattiva, pianifica i propri compiti e lavora «ore o giorni» [verificato: 12 §1].
- **Memoria e apprendimento.** Skill curate da Hermes e pull request settimanali sulle skill aziendali [verificato: 20-G §2, A6].
- **Approvazioni e limiti.**
  - Tre corsie di approvazione: SersanOutreach, Metricool, Paperclip.
  - «Sempre» per una classe intera dopo 30 giorni senza correzioni. Mai senza carta: prima offerta, invio a freddo, numero nuovo, cancellazioni.
  - `/stop` ferma tutto [verificato: 20-G §5].
- **Canali, 24/7, voce.**
  - Slack con Slack Connect per i clienti [verificato: 20-G §1].
  - Andrea con ElevenLabs e Twilio nelle settimane 13-16 [verificato: 20-G §6]. Consenso e richiamata in 90 s sono comunque codice da scrivere [verificato: 21-visione §3].
- **Pronto e da costruire.** 64 gp più il 30 % di riserva, circa 83; primo rilascio con circa 29 gp in 5 settimane [verificato: 20-G §6].
- **Server.** Circa 116 GB su 128 [verificato: 20-G §3].
- **Costi.**
  - Cassa oggi circa 239 / 592 / 1.622 €/mese [verificato: 20-G §7].
  - Ricalcolata sulla stessa base, circa 850-870 € nello scenario consigliato [verificato: 21-ceo §2].
- **Sicurezza ancora aperta.** Somma le superfici di cinque componenti; i Managed Agents sono fuori dalla conservazione zero; ci sono tre registri di approvazione [verificato: 21-compliance §2].
- **Punteggi ed esito.** Voti 37 / 34 / 36 / 36,5, la copertura più alta del giro [verificato: 02-alt §2.2]. Scartata: cinque componenti open source e otto servizi per un solo amministratore [verificato: 22 §1].
- **Autonomia.**
  - Pronta: debrief e Claude Tag L3 autonomo, recap e bozze L1 carta.
  - Raggiungibile: L3 autonomo per classi intere, Andrea L3 autonomo [non verificato: mappatura mia].

---

## 2. Secondo giro (25/10/2026): tre proposte dentro il board

### Proposta 1. Il motore sull'Agent SDK: 171,5/240, prima

- **L'idea.** Un servizio TypeScript fa girare un processo Claude per ogni lavoro, con il profilo dell'agente. Accanto: n8n, LiteLLM, Cancello, PostgreSQL, Qdrant, BookStack e Teams [verificato: 34-1 In breve].
- **Orari ed eventi.** n8n ha un flusso a orario per profilo e riceve i webhook firmati. Un lavoro può partire anche da Teams o da un passaggio in bacheca [verificato: 34-1 §5.1].
- **Passaggi e dialogo.**
  - Bacheca con freno: 3 passaggi per catena, 8 messaggi per thread, tetto in dollari. È visibile nel canale «Agenti».
  - In P1 la bacheca arriva nelle settimane 17-27 [verificato: 34-1 §5.3, §7.2].
- **Memoria e apprendimento.**
  - L'identità della persona arriva fino all'MCP RAG [verificato: 34-1 §1].
  - Un revisore settimanale propone pull request sulle skill. Le nuove aperture di Andrea passano dal Cancello, con prova A/B [verificato: 34-1 §6].
- **Approvazioni e limiti.**
  - Scritture interne senza carta.
  - Invii ai clienti, pubblicazioni, offerte e codice su carta.
  - Pagamenti mai automatici; cancellazioni e credenziali sempre negate.
  - «Sempre» per agente, azione e destinazione dopo 20 sì uguali.
  - Stop d'emergenza dal telefono [verificato: 34-1 §5.2, §10].
  - Il giudice di sicurezza ha trovato due difetti nel collegamento al Cancello, corretti nella v2 [verificato: 35-sicurezza In breve; 36 §5.1].
- **Canali, 24/7, voce.**
  - Teams con la «Porta» (il nostro bot); Telegram nelle settimane 28-31, WhatsApp nelle 32-38, Slack e Buzz nelle 39-43 [verificato: 35-visione §2].
  - La sera la GPU va a Experimental-1 [verificato: 34-1 §3.3].
  - Andrea in casa (Asterisk, Pipecat, su CPU, poi sulla seconda GPU) nelle settimane 32-38, per 28 gp [verificato: 34-1 §7.2-7.3].
- **Pronto e da costruire.**
  - L'SDK dà ciclo dell'agente, sessioni riprendibili, hook, permessi, MCP e skill. Non dà orari, bacheca, profili persistenti né chat di gruppo [verificato: 26 In breve].
  - 218 gp di base, circa 290 con la riserva; demo alla settimana 5, pilota alla 16 [verificato: 34-1 §7.2].
- **Server.**
  - RAM nuova 21 / 49,5 / 66-70 GB su 53 liberi: servono altri 192 GB prima della fase C.
  - Motore da 6 sessioni in 12 GB fino a 12-16 sessioni in 20 GB.
  - Seconda GPU da 16 GB prima della fase E [verificato: 34-1 §3.1-3.3].
- **Costi.**
  - In più rispetto a oggi: circa 135 €/mese con Azure accesa, 14-31 € dopo lo spegnimento, 78-178 € a regime.
  - Listino a regime 483-593 €, corretto dal CPTO a 479-583 €.
  - Una tantum della proposta 3.431-4.295 €.
  - Esterni: operatore telefonico, relay SMTP, WhatsApp, Slack, strumenti commerciali fino a 187,62 € [verificato: 34-1 §4.5, §8; 35-cpto §3.1].
- **Sicurezza ancora aperta.** Circa 50 gp di codice di sicurezza nostro, senza revisione esterna. LiteLLM ha avuto versioni compromesse il 24/03/2026, secondo una fonte terza [verificato: 35-sicurezza §3.1, §6, §9].
- **Punteggi ed esito.**
  - 43 / 42 / 44 / 42,5 = 171,5. Somme per criterio: copertura 36, tempo 23, costo 23,5, affidabilità 27,5, sicurezza 32, board 29,5 [verificato: 02-alt §4.3].
  - Diventa la v2 [verificato: 36 §1].
- **Autonomia.**
  - Pronta: interne L3 autonomo, uscite L1 carta.
  - Raggiungibile: «Sempre» L3 autonomo per destinazione; Andrea L3 autonomo solo per chi chiede la richiamata; skill L1 carta [non verificato: mappatura mia].

### Proposta 2. Hermes sul nostro server: 137/240, terza

- **L'idea.** Sei istanze di Hermes, una per confine di fiducia: 50 profili Hermes e 7 servizi, con il Cancello come unico esecutore [verificato: 34-2 In breve].
- **Orari ed eventi.** Gli orari li tiene n8n, che chiama l'API di Hermes. Il cron di Hermes non si usa per i processi aziendali, «per evitare doppioni» [verificato: 34-2 §1, §4].
- **Passaggi e dialogo.**
  - Dentro un'istanza c'è la kanban di Hermes:
    - un dispatcher ogni 60 s riprende i compiti fermi;
    - c'è una corsia di revisione e un blocco «serve un umano»;
    - dopo 2 fallimenti il compito si ferma da solo.
  - Fra istanze serve un nostro MCP «passaggi».
  - In `#agenti` compaiono solo i passaggi fra istanze, e le chat di gruppo di Hermes restano spente [verificato: 34-2 §5.1-5.2, §10.1].
- **Memoria e apprendimento.**
  - L'identità verso la memoria vale per istanza, non per persona [verificato: 34-2 §3.3].
  - Le skill le scrive Hermes; diventano attive dopo una pull request approvata [verificato: 34-2 §5.5].
- **Approvazioni e limiti.**
  - Un plugin blocca ogni strumento non ammesso e, se non risponde in tempo, nega.
  - Le carte di business arrivano solo dal bot del Cancello.
  - «Sempre» nelle settimane 31-34.
  - I dati rossi restano fuori da Hermes [verificato: 34-2 §5.4, §8.1, §10.3].
  - In Buzz, il ponte di Hermes approva da solo ogni permesso [verificato: 34-2 §5.3].
- **Canali, 24/7, voce.**
  - Un bot Teams per istanza; Telegram nelle settimane 21-23; WhatsApp nelle 24-30 (Hermes non manda i modelli oltre le 24 ore); Slack e Buzz nelle 31-34 [verificato: 34-2 §5.3, §8.1].
  - Andrea su CPU nelle settimane 24-30, poi sulla seconda GPU [verificato: 34-2 §8.1].
- **Pronto e da costruire.**
  - Profili, kanban, skill che crescono e canali sono pronti; il primo bot arriva «in giorni» [verificato: 34-2 In breve].
  - 171 gp di base (227,5 con la riserva), ma stimati a 0,6 gp per profilo: con il metro della P1 sarebbero circa 200 [verificato: 35-cpto §3.2].
- **Server.** RAM nuova 55-76 GB a regime, con l'acquisto prima delle settimane 24-30. Arriva prima che con l'SDK, perché ogni istanza ha il suo gateway [verificato: 34-2 §3.5].
- **Costi.** Listino circa 519 €/mese; eccezioni fino a circa 284 €; una tantum subito 3.114-4.354 € [verificato: 34-2 §9].
- **Sicurezza ancora aperta.**
  - Il gateway unico ha 276 problemi aperti, 9 di sicurezza, 0 risolti (25/10/2026, 14:54 UTC).
  - Almeno 45 avvisi di sicurezza nel 2026.
  - Manutenzione di 2-3 gp al mese [verificato: 35-cpto §2; 34-2 §8.2].
- **Punteggi ed esito.**
  - 35 / 34 / 34 / 34 = 137 [verificato: 02-alt §4.2].
  - Scartata per sicurezza, identità per istanza e bacheca su un solo host [verificato: 36 §1.4].
  - Resta un'uscita prezzata (26-33 gp) e una prova possibile in laboratorio (6-8 gp) [verificato: 36 §2.4].
- **Autonomia.**
  - Pronta: interne L3 autonomo con il dispatcher, uscite L1 carta.
  - Raggiungibile: «Sempre» L3 autonomo, Andrea L3 autonomo, skill L1 carta [non verificato: mappatura mia].

### Proposta 3. Claude Team al centro con i connettori MCP: 170/240, seconda

- **L'idea.** Le persone lavorano in Claude Team, collegato al server con connettori MCP. Dietro girano circa 30 lavori n8n. L'Agent SDK serve solo ai lavori a più passi [verificato: 34-3 In breve].
- **Orari ed eventi.**
  - Gli orari stanno in n8n.
  - I compiti programmati di Claude Team appartengono a una sola persona e agiscono a suo nome. Girano al massimo una volta l'ora e sono in anteprima.
  - Quelli di Cowork girano anche a computer spento [verificato: 34-3 §2].
- **I tipi di agente** [verificato: 34-3 §5]:
  - 10 di tipo «T»: una skill che apre una persona;
  - 29 di tipo «N»: un lavoro n8n a schema;
  - 9 di tipo «S»: una sessione dell'Agent SDK, al massimo 6 insieme;
  - 9 di tipo «V»: un servizio.
- **Passaggi e dialogo.** Da sola fa solo catene fisse. La bacheca e la chat di gruppo arrivano come aggiunte nelle settimane 23-28 [verificato: 34-3 §8-9].
- **Memoria e apprendimento.** Identità per persona via OAuth. L'apprendimento è solo «in parte»: il revisore delle skill arriva nelle settimane 23-28 [verificato: 34-3 §4, §7].
- **Approvazioni e limiti.**
  - «Approvare non è uno strumento»: il sì arriva solo da una persona.
  - Cancello v1 senza «Sempre». Le regole «Sempre» e lo **stop d'emergenza** arrivano solo nella parte 2, nelle settimane 23-28 [verificato: 34-3 §4, §9].
  - I compiti programmati includono di default i connettori in scrittura: una scrittura in Jira salterebbe il Cancello [verificato: 35-sicurezza §2, §3.2].
- **Canali, 24/7, voce.**
  - Claude Team su web, computer e telefono; Teams con carte e chat 1:1 dalla settimana 11; Telegram nelle settimane 23-28, WhatsApp nelle 29-36, Slack e Buzz nelle 37-42 [verificato: 34-3 §9].
  - Andrea nelle settimane 29-36 [verificato: 34-3 §9].
- **Pronto e da costruire.**
  - Da sola copre 59 voci per intero, 24 in parte e 7 no: J9, A7, G5, G6, K10, L1, L2. Con le aggiunte A-G le copre tutte.
  - 191 gp di base, 254 con la riserva [verificato: 34-3 §7, §9].
- **Server.**
  - Con il tetto di 6 sessioni: RAM nuova 41-50 GB e «la RAM in più non serve subito» [verificato: 34-3 §3.3].
  - I giudici ricalcolano il margine fra -6 e +9,5 GB [verificato: 35-ceo §6; 35-cpto §3.3; 35-sicurezza §7].
- **Costi.**
  - In più rispetto a oggi: da -15 a +20 €/mese dopo lo spegnimento di Azure, 58-110 € con Andrea, 551-557 € a fine bundle; listino circa 525 € [verificato: 34-3 §10].
  - Rende quasi obbligatori i 5 posti premium di Claude Team [verificato: 35-ceo §9].
- **Sicurezza ancora aperta.**
  - Sei endpoint MCP pubblici.
  - Claude Team senza log di audit né conservazione personalizzata.
  - Cancello e motore nella stessa macchina [verificato: 35-sicurezza §3.2].
- **Punteggi ed esito.**
  - 41 / 45 / 42 / 42 = 170. Prima su tempo al valore (34), costo (28) e aderenza al board (33); ultima sulla copertura (26) [verificato: 02-alt §4.3].
  - Scartata come base perché declassa gli agenti [verificato: 36 §1.3]. Il piano prende da lei la fase zero e il tetto di 6 sessioni [verificato: 36 §1.5].
- **Autonomia.**
  - Pronta: L0 a mano nelle settimane 1-4; dalla settimana 11 i lavori interni sono L3 autonomo e le uscite L1 carta.
  - Raggiungibile: 10 figure restano L0 a mano; «Sempre» L3 autonomo dalle settimane 23-28 [non verificato: mappatura mia].

### Per confronto: l'architettura v2 scelta

- **Fasi** [verificato: PRES §11]:
  - fase 0 (settimane 1-4): Claude Team per tutti;
  - fase 1 (settimane 5-8): carte sul telefono e debrief alle 7:00, con nessun dato rosso salvato sul banco di prova;
  - fase 2 (9-21): «Sempre» che scadono e FIDO2, bacheca con freno, nove bot di squadra;
  - fase 3 (22-35): Telegram, Slack e WhatsApp;
  - fase 4 (36-40): skill proposte dagli agenti;
  - fase 5 (41-48): Andrea.
- **Le regole «Sempre».** Valgono per agente, azione e destinazione, scadono dopo 30 giorni e non valgono mai per destinatari nuovi [verificato: 36 §5.8].
- **Andrea** richiama da solo solo chi lo chiede [verificato: PRES §1, decisione 10].
- **Tutte le 57 figure restano agenti** [verificato: 36 §5.2].

---

## 3. Dove il secondo giro ha messo la capacità del server davanti all'autonomia

In nessuno dei due giri l'autonomia era un criterio. Il sesto criterio è passato dall'«indipendenza» all'«aderenza al board di Michele» [verificato: 02-alt §1]. L'unica misura indiretta dell'autonomia è la copertura della visione.

1. **La lente del CPTO pesa RAM e GPU.** Dichiara di contare «il peso su RAM e GPU» [verificato: 35-cpto, intestazione].
   - La proposta meno autonoma (P3, copertura 26 su 40) chiude a 170, solo un punto e mezzo sotto la P1 (copertura 36).
   - La P3 recupera con tempo al valore 34, costo 28 e aderenza 33 [verificato: 02-alt §4.3].
2. **Il costo ha premiato la RAM risparmiata togliendo autonomia.**
   - Il giudice CEO scrive che la P3 risparmia 750-875 € «quasi solo perché non compra la RAM», e le dà 8 sul costo [verificato: 35-ceo §1, §4.2]. Visione e sicurezza le danno 7, il voto più alto della riga [verificato: 35-visione §1; 35-sicurezza §1].
   - Il CPTO scrive che quel risparmio «viene in buona parte dal declassamento»: 10 figure diventano skill aperte da una persona [verificato: 35-cpto §4.3]. In livelli, da L3 autonomo a L0 a mano [non verificato: mappatura mia].
3. **Chi chiedeva l'hardware che regge l'autonomia ha perso punti.**
   - La P1 perde sull'aderenza e sul costo perché chiede la RAM prima della fase C e la seconda GPU prima della fase E, «mentre il board la mette in F5» [verificato: 35-visione §3.1; 35-cpto §4.3, §4.6]. Il CPTO stesso nota che quegli upgrade li aveva proposti Michele: «cambia solo quando comprarli» [verificato: 35-cpto §4.6].
   - La P2 prende 5 sul costo anche perché «la RAM serve prima» [verificato: 35-cpto §4.3].
4. **La v2 ha preso la regola della RAM dalla P3.**
   - Si misura con 6 sessioni insieme; si comprano altri 192 GB solo sotto i 5 GB liberi o prima di Vexa [verificato: 36 §1.5, §4.2].
   - Nella fase 2 il motore ha 12 GB per 6 sessioni; 16 sessioni arrivano solo nelle fasi 5-6 [verificato: 36 §4.2].
   - La visione punta a cento agenti [verificato: 00, voce G9].
5. **La voce 24/7 è passata in casa e dietro la GPU.**
   - Con il board escono ElevenLabs e Twilio [verificato: PRES §1]. Andrea arriva nelle settimane 41-48, per 28 gp [verificato: 36 §7.2-7.3].
   - Nel primo giro, in abbonamento, Andrea stava fra le settimane 9 e 17 nelle sette proposte e nelle 17-20 nel piano scelto [verificato: 20-A … 20-G §6; 22 §5].
   - La seconda GPU serve «al più tardi all'inizio della fase 5» [verificato: PRES §6.4]. La voce in cloud resta solo come eccezione «in ultima istanza», circa 88 €/mese [verificato: 34-1 §10].
6. **La GPU condivisa toglie ore al lavoro continuo.**
   - La RTX 4000 di giorno è quasi piena; la sera va a Experimental-1 [verificato: 36 §4.3].
   - La v2.1 attenua: Michele la presta «per poco tempo e solo ogni tanto», e intanto i lavori della GPU aspettano in coda [verificato: PRES §6.4].
7. **I motori in abbonamento che davano autonomia e continuità sono usciti per il perimetro.**
   - I Managed Agents sono esclusi «contro la regola tutto in casa» [verificato: 26 §1.2]; Hermes Cloud è fuori perimetro [verificato: 34-2 §2]; Claude Tag esce insieme a Slack [verificato: 36 §6].
   - Nel primo giro Hermes Cloud era la riserva fredda [verificato: 22 §8]. Ora, se manca la corrente, l'UPS spegne il server dopo 3 minuti e agenti e Andrea restano fermi fino alla riaccensione [verificato: PRES §13].
8. **Il ritmo è quello del board.**
   - Ogni fase parte quando la precedente è validata.
   - Fino alla validazione della fase F3 (sicurezza) si salvano solo dati verdi e gialli.
   - Prima della F4 entrano solo i servizi del pilota [verificato: PRES §6.2, §11].

   Il motivo dichiarato è il carico di chi amministra il server [verificato: 35-cpto §6].

**Dove invece il secondo giro ha difeso l'autonomia.**
- Ha rifiutato di declassare gli agenti: tutte le 57 figure sono agenti che ricevono lavoro dalla bacheca [verificato: 36 §1.3, §5.2].
- Ha anticipato alla fase 2 la bacheca, il canale «Agenti» e i nove bot [verificato: 36 §1.6].

Ha protetto quindi l'ampiezza dell'autonomia, cioè chi è un agente. La capacità del server ha deciso quante sessioni girano insieme, quando arrivano e se lavorano di notte [non verificato: lettura mia]. La P2 è stata scartata soprattutto per sicurezza e identità, non per capacità [verificato: 36 §1.4].

---

## 4. Osservazioni trasversali (fatti, non verdetti)

- **L2 finestra non esiste in nessuna alternativa.**
  - Nella E «il silenzio non vale sì»; in Paperclip la scadenza vale come no; nella v2 la carta ha una scadenza [verificato: 20-E §5; 20-F §5; PRES §5.4].
  - In Grok le approvazioni non presidiate scadono in circa 10 minuti e la proposta C ripiega su bozze [verificato: 11 §2.6; 20-C §8].
  - L2 andrebbe progettato nel Cancello [non verificato: deduzione].
- **«Sempre» con ampiezze diverse.**
  - Per classe intera o per tipo di azione: B, G e D [verificato: 20-B §5; 20-G §5; 20-D §5].
  - Per destinazione: A, E, P1, P2, P3 e v2 (nella v2 anche con scadenza a 30 giorni) [verificato: 20-A §5; 20-E §5; 34-1 §5.2; 36 §5.8].
- **Il post-call della trascrizione è il pezzo più lontano.** Nella v2 la mail al cliente è L1 carta e diventa L3 autonomo solo per destinazione, dopo 20 sì uguali [verificato: 36 §5.8; PRES §9.3].
- **Imparare da soli resta L1 carta in ogni proposta.** Di serie si aggiornano da soli Hermes, Grok Bot e, in modo opaco, i dots [verificato: 10 §4.2; 11 §2.4; 20-D §2].
- **Stop d'emergenza.**
  - Presente in A, B, D, E, F, G, P1 e P2.
  - Assente nella C [verificato: 20-C].
  - Nella P3 arriva solo nelle settimane 23-28 [verificato: 34-3 §9].
  - Di serie, la pausa del dot non ferma i compiti pianificati [verificato: 18 §2.2].
- **Cancellazioni.**
  - Negate agli agenti in B, P1 e v2 [verificato: 20-B §5; 34-1 §5.2; 36 §5.8].
  - In A, F e G passano su carta, cosa che va contro il limite fisso [verificato: 20-A §5; 20-F §5; 20-G §5].
- **Leve già studiate per avere più autonomia con un abbonamento** (prezzi dai file):
  - voce di Andrea in cloud, circa 88 €/mese [verificato: 34-1 §10];
  - Managed Agent sempre acceso, al massimo 58,40 $/mese di sola esecuzione [verificato: 18 §0];
  - Hermes Cloud, Plus a 20 $/mese più l'istanza, a 0,56-1,09 $/giorno [non verificato: fonti terze, 18 §2.4];
  - Claude Tag, tetto di 44,67 €/mese (solo con Slack) [verificato: 22 §9];
  - prova di Grok Bot, circa 54 € [verificato: PRES §14];
  - linea internet di riserva, 77-200 € una tantum più 10-11 €/mese [verificato: PRES §14, decisione 13].

---

## 5. Tabella finale

| Alternativa (giro, punti) | Autonomia pronta (quando) | Autonomia raggiungibile (a regime) | Cosa la frena |
|---|---|---|---|
| **Trascrizione di riferimento** | In esercizio: post-call intero (mail al cliente compresa) L3 autonomo; voce 24/7 L3 autonomo | Impara dai rifiuti a L3 autonomo; oltre 100 agenti | Nessuna approvazione descritta [verificato: TR] |
| **A Hermes + Cancello** (1°, 159) | Settimana 5 dichiarata, 7-8 secondo i giudici: interne e debrief L3 autonomo; uscite L1 carta; skill L3 autonomo (di serie) | Uscite ripetitive L3 autonomo per classe e destinatario dopo 20 carte; classi delicate L1 carta; Andrea L3 autonomo (settimane 9-12) | Hermes «single-tenant», profili che si mescolano, ritmo dei rilasci |
| **B buzz** (1°, 140,5) | Settimana 5: interne L3 autonomo, uscite L1 carta; senza il gate, L3 autonomo senza freni | L3 autonomo per classi intere dopo 30 giorni; cancellazioni e pagamenti negati; Andrea L3 autonomo (settimane 10-14) | Approvazioni di serie rotte, nessun freno ai giri, versione prima della 1.0 |
| **C Grok Bot** (1°, 113) | 2 settimane, solo dati verdi: interne L3 autonomo, uscite L0 a mano | Uscite L3 autonomo solo via SersanOutreach; dai Bot L0 a mano; Andrea L3 autonomo dal server | Termini (revisione di una persona), dati negli USA, quota settimanale, beta |
| **D Dots** (1°, 105) | 2 settimane: uscite L1 carta; dot sempre acceso | L3 autonomo per tipo pre-approvato; offerte, contratti, pagamenti L0 a mano; Andrea L3 autonomo | Un dot per persona, dialogo fra agenti non nativo, pausa che non ferma i compiti |
| **E Claude-native** (1°, 140) | Settimana 8: report e recap interno L3 autonomo, uscite L1 carta | L3 autonomo stretto per destinatario, poi a campione; Andrea L3 autonomo; agenti che si parlano dalla settimana 13 | Tutto da scrivere (119 gp) |
| **F Paperclip** (1°, 148,5) | 4 settimane: interne, battito e routine L3 autonomo; uscite L1 carta; pubblicazioni L0 a mano | Uscite ripetitive L3 autonomo; lead nuovi, chiamate e pubblicazioni restano L1 carta o L0 a mano; Andrea L3 autonomo | Avvisi critici, default pericolosi, niente memoria |
| **G Ibrido** (1°, 143,5) | 5 settimane: debrief e Claude Tag L3 autonomo; recap L1 carta | L3 autonomo per classi intere; Andrea L3 autonomo (settimane 13-16) | Cinque componenti e otto servizi per un solo amministratore |
| **P1 Agent SDK** (2°, 171,5) | Settimana 16: interne L3 autonomo, uscite L1 carta | «Sempre» L3 autonomo per destinazione; Andrea L3 autonomo (settimane 32-38); skill L1 carta | Tutto il codice è nostro; RAM e GPU anticipate |
| **P2 Hermes in casa** (2°, 137) | Settimana 11: interne L3 autonomo con il dispatcher, uscite L1 carta, niente dati rossi | «Sempre» L3 autonomo (settimane 31-34); Andrea L3 autonomo (24-30); skill L1 carta | 276 problemi del gateway, identità per istanza |
| **P3 Claude Team + MCP** (2°, 170) | Settimane 1-4 L0 a mano; dalla 11 interne L3 autonomo, uscite L1 carta | 10 figure restano L0 a mano; «Sempre» L3 autonomo (settimane 23-28); Andrea (29-36); al massimo 6 sessioni | Agenti declassati, compiti che agiscono a nome della persona, stop tardivo |
| **v2 scelta** (dopo il 2° giro) | Settimana 8: interne L3 autonomo, uscite L1 carta | «Sempre» L3 autonomo per destinazione, 30 giorni; Andrea L3 autonomo solo su richiesta (settimane 41-48); skill L1 carta (36-40) | Si parte da 6 sessioni, serve la seconda GPU, si segue il ritmo del board |

Le colonne «pronta» e «raggiungibile» traducono le regole di ciascuna proposta nei livelli di Alberto [non verificato: mappatura mia]. Le settimane e le regole vengono dalle fonti citate nelle schede.
