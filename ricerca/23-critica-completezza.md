# 23 · Critica di completezza dell'architettura scelta (22)

**Data:** 24/10/2026. **Letti:** 00, 22, 01, 05 (§0, §5, §6), 10-18; 20-E per le cifre citate da 22. Nessun file manca. **Etichette:** [verificato: file §]; [non verificato] = mia deduzione.

## 1. In breve

- Ogni voce A1-I4 ha una riga nel §4 di 22, ma circa venti sono coperte solo a parole: manca il pezzo che le fa funzionare o il dato su cui lavorano.
- Recall.ai, ElevenLabs e i bot Slack nei canali condivisi violano la regola dei tre colori, che regge la privacy di 22.
- La decisione della settimana 8 prova Hermes nella configurazione meno rischiosa e non misura risultati commerciali.
- I costi mescolano stack esistente e sistema nuovo, prendono le API da un'altra proposta e lasciano senza cifra le spese una tantum più grosse.
- Gli scarti di buzz e Grok Bot non poggiano sui fatti di SerSan.

## 2. Voci coperte solo a parole

| Voce | Problema | Fonte |
|---|---|---|
| A1, C2 | Recall.ai riceve l'audio (dato rosso) e nessun rapporto ne verifica sede o DPA. I 0,65 $/h includono la trascrizione di Recall: la «trascrizione in casa» non torna. Le riunioni fisiche «dal telefono» non hanno né app né flusso. | 14 §4; 16 §5 |
| A3 | 13 chiede 50 domande italiane con recall@10 prima di scegliere; la prova di fase 2 non ha soglia. | 13 §7 |
| A7, G9 | I bot Slack per agente arrivano in fase 3, dopo la decisione: la configurazione con i bug noti (più profili su un gateway) non viene provata. Alla settimana 16 gli agenti sono 15-25, non 100+. | 10 §6; 22 §5 |
| B2 | L'operator MCP non crea deal; la REST elencata ha solo lettura, PATCH e cambio di stadio. Un cliente attivo spesso non è un lead. | 01 §5.2, §5.5 |
| B3, C1, D2 | Esecutore Gmail, debrief «sul calendario», brief «la sera prima» e «chi è in call» danno per scontato Google, ma la suite di posta non è nota. | 14 §5 |
| C3, D5 | Le trascrizioni intere vanno a Sonnet e Opus, ma 22 le classifica rosse (fuori solo dopo l'oscuramento), e nessuna fase costruisce o misura l'oscuramento. | 13 §2.3; 16 §5 |
| D2-D3 | Manca metà delle fonti: aperture mail (nessuna mailbox live), newsletter (decisione al 23/11), post LinkedIn (nessuna via ufficiale), storico (11 lead). Il brief è profilazione da registrare. | 01 §0, §6; 05 §2.10; 16 §3 |
| D4 | moda.app riceve dati gialli senza un DPA verificato. Claude Slides è dei posti Team, non dell'API [non verificato]. | 16 §5-§6 |
| E3 | Dipende dalla porta dei modelli, cioè da un indirizzo base di Hermes non verificato; il ripiego (chiave per famiglia) non applica i colori. Su Team non ci sono tetti per persona. | 22 §2; 18 §5 |
| F1 | Con quattro persone un dato «aggregato» resta identificabile. Se ci sono dipendenti, servono le garanzie dell'art. 4 anche sotto i 21 giorni. | 16 §1.2 |
| D1, G2, G6-G8 | GP+BALD lavora sui profili e non ha esiti da cui imparare (0 vinti, 0 persi); l'A/B sui rifiuti non ha volumi e G7 non ha una base. In 24 settimane la pipeline pesata non arriva. | 01 §0, §1.1 |
| G5 | Le regole di casa vietano la voce sintetica in outreach e call, e il sito promette «a founder reads it». Senza un operatore autorizzato in Italia il CLI rischia il blocco. L'audio va a ElevenLabs, negli USA. | 05 §5.6, §5.8; 16 §2, §5 |

A6, C4 (note vocali) e G8 hanno una fase nel §4 ma nessun lavoro né prova nel piano. Coperte bene: A2, A4, A5, B4, B5, C6, E4, F5, H1-H5, I3, I4.

## 3. Promesse non sostenute ed etichette sbagliate

- **Uscita in 10-15 gp.** 20-E dà 4 gp al solo host dei lavori; routine, bacheca e bot andrebbero rifatti [verificato: 20-E §6]. Con l'uscita A arriva a circa 114 gp, contro i 119 di E [non verificato: mio calcolo].
- **Etichette.** 16 §5 non parla di Recall. Le taglie di Hermes Cloud (18,67 e 47,08 €) sono di terzi [verificato: 18 §2.4]. In 13 §2.3 l'oscuramento è [non verificato].
- **«Zero effetti fuori dal Cancello».** Per Hermes l'unico confine è il sistema operativo [verificato: 10 §5], e i suoi bot scrivono in Slack da soli: invitati per errore in un canale Slack Connect, parlano al cliente senza carta [non verificato]. Mancano un filtro in uscita sulla VM degli agenti e il divieto di bot nei canali condivisi.

## 4. Costi

- **API.** I 195,65 € vengono da 20-E §7, calcolati per un altro motore con 230 sessioni al mese [ipotesi]. 22 non dà sessioni né token: il conto non si rifà.
- **Perimetro.** I «fissi di 14» includono Instantly, Apollo, Apify, Higgsfield, Workspace e corrente. Manca la riga decisiva: quanto costa in più il sistema.
- **UPS.** È contato due volte: 19,40 € di ammortamento nei mensili e di nuovo negli una tantum.
- **Corrente.** 22 usa 102,20 € (400 W, 14 §11.1); 15 §3.1 stima 28-70 €. Scelta non spiegata.
- **Senza cifra.** Parere legale, kit HPE, alimentatori, SSD, climatizzazione del locale (15 §3.2) e revisione di sicurezza: le decisioni 2 e 10 chiedono un sì senza importo.
- **Persone.** I 133 gp non hanno valore in euro; dopo la settimana 24 manca la manutenzione (Hermes: 5 patch in 10 giorni [verificato: 10 §3]).
- **Riserva Azure.** Non dimensionata: 15,6 GiB già condivisi da prod, stage e monitoraggio, nessuna GPU [verificato: 01 §3.1].

## 5. Altre contraddizioni con i rapporti

- SersanOutreach entra com'è: `auto_linkedin` approva DM senza persona, `extension_voyager` è «non production-eligible» e acceso con l'override del rischio, lo stack usa Playwright stealth [verificato: 01 §1.1, §6 r.2]. Contraddice due principi di partenza.
- 05 dà la migrazione di SersanOutreach in corso su Azure [verificato: 05 §0, §7 d.7]; 22 la porta sul server senza chiarire.
- 22 tace la fine del supporto del DL380 Gen10, il 31/3/2028 secondo terzi [verificato: 15 §2.6], e il luogo del server, che decide GDPR e corrente [verificato: 16 §5].

## 6. Scarti

- **buzz.** I tre motivi sono lacune che 17 dice come colmare, e il Cancello di 22 toglie già alla chat approvazioni ed effetti [verificato: 17 §8]. Hermes ha difetti simili: approvazioni solo sulla shell, loop su Slack con `all` [verificato: 10 §4.1-§4.2]. I motivi veri per Slack (Slack Connect per B1, Claude Tag, buzz su Windows in alpha) 22 non li scrive.
- **Grok Bot.** I fatti valgono per i dati gialli e rossi. Per i verdi 11 propone un mese di prova a 120-150 $ e Alberto ha aperto all'abbonamento; 22 sceglie Hermes Cloud, con DPA «non trovato» [verificato: 11 §9; 18 §2.4].
- **G** è scartato per «cinque componenti e otto servizi», ma 22 ne usa di più [non verificato: mio conteggio].
- **Paperclip.** I sei advisory critici pesano, ma anche Hermes ha CVE 2026 sul webhook [non verificato: 10 §3], e 22 rifà nel Cancello organigramma e budget già pronti in Paperclip.

## 7. Domande di un CEO scettico

1. Quanto spendiamo in più al mese, e quanto valgono 53 gp tolti ai clienti?
2. Alla settimana 8 quale numero commerciale migliora?
3. Perché Hermes, se i bug colpiscono proprio i profili multipli?
4. Chi gestisce Hermes, Cancello e server senza Alberto?
5. Chi decide l'eccezione sulla voce sintetica per Andrea?
6. In quale paese e su che macchina staranno i dati nel 2028?

## 8. Correzioni minime prima di presentarlo

1. Riscrivere i tre colori sui flussi reali; mettere in fase 1 la prova dell'oscuramento.
2. Nelle settimane 7-8 provare almeno tre profili, ciascuno con il suo bot Slack, e aggiungere un criterio commerciale.
3. Riga del costo incrementale; API ricalcolate per Hermes; UPS contato una volta; tetti per legale e hardware.
4. Decisione dei CEO su `auto_linkedin` e stealth prima di collegare gli agenti.
5. Confermare la suite di posta e aggiungere la creazione del deal prima di B2, B3, C1 e D2.
6. Riscrivere gli scarti di buzz e Grok Bot sui fatti di SerSan, con la prova di Grok Bot sui dati verdi prezzata.
