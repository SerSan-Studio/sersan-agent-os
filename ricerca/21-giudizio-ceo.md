# 21 · Giudizio con la lente di Alessandro (CEO, vendite e marketing)

**Data:** 24/10/2026. **Criteri della lente:** valore per vendite e marketing, tempo al primo risultato visibile, costo mensile, semplicità per chi non è tecnico, rivendibilità alle PMI.

## 1. Punteggi (0-10, totale su 60)

| Proposta | Copertura | Tempo al valore | Costo | Affidabilità e manutenzione | Sicurezza e privacy | Indipendenza | **Totale** |
|---|---|---|---|---|---|---|---|
| **A Hermes + Cancello** | 8 | 5 | 7 | 5 | 7 | 8 | **40** |
| F Paperclip | 7 | 6 | 6 | 5 | 6 | 8 | **38** |
| G Ibrido | 8 | 5 | 5 | 3 | 6 | 7 | **34** |
| B buzz | 6 | 5 | 6 | 3 | 5 | 8 | **33** |
| E Claude-native | 7 | 3 | 4 | 4 | 8 | 5 | **31** |
| C Grok Bot | 6 | 8 | 4 | 5 | 3 | 2 | **28** |
| D OpenAI Dots | 5 | 6 | 3 | 4 | 4 | 3 | **25** |

Il costo include i giorni-persona di Alberto e Mattia, la spesa più grande.

## 2. Costi rifatti sulla stessa base

Esborso mensile «consigliato» con bundle e crediti validi, stack comune incluso (Workspace, Instantly, Apollo, Apify, Metricool, moda, Higgsfield, proxy) [verificato: 14 §11.1]:

| | Dichiarato (€) | Sulla stessa base (€) | Giorni-persona |
|---|---|---|---|
| B | 723 | ≈ 723 | 81 |
| E | 749 | ≈ 749 | 119 |
| A | 759 | ≈ 759 | 60, realistici ≈ 75 |
| F | 873 | ≈ 873 (≈ 780 senza HubSpot e Fireflies) | 68 + 2 al mese |
| G | 592 | ≈ 850-870 | 83 |
| C | 693 | ≈ 1.058 | 66 |
| D | ≈ 811 | ≈ 1.190, più crediti OpenAI di prezzo ignoto | 52 |

Finito il bundle, ogni proposta aggiunge 446,70 € di Claude Team [verificato: 14 §1.3].

## 3. Stime ottimistiche e affermazioni deboli

- **Tutte.** I conti presumono 60 call e 300 lead al mese. Oggi SersanOutreach ha 11 lead, 0 meeting, 0 vinti, readiness NOT READY, nessuna email live [verificato: 01 §0]; il calendario marketing non ha slot pronti [verificato: 05 §0]. Pipeline pesata, coaching e Andrea resteranno senza dati per mesi.
- **Self-hosted.** Fase 0 con nodi aperti: RAM sbilanciata, GPU non qualificata HPE, UPS da comprare, luogo del server ignoto [verificato: 15 §0].
- **Crediti.** Gli 800 $/mese non sono confermati [verificato: 14 §1.4].
- **A.** Il nucleo del Cancello vale 5 giorni-persona. E stima 9 per lo stesso nucleo, 4 per più proprietari, 2 per la porta dei modelli e 6 per le carte [verificato: 20-E §6]. Il primo rilascio di A slitta verosimilmente alla settimana 7-8 [non verificato].
- **D.** I Workspace Agents li ha verificati solo l'autore, via proxy; 12 §2 e 18 §2.2 li danno per non verificati, e il prezzo di Business Premium viene da terzi.
- **G.** Andrea è stimato a 250 minuti, gli altri a 1.000. La Sustainable Use License di n8n vieta la rivendita come servizio [verificato: 12 §0 punto 6].
- **C.** I dati «gialli» su Grok contraddicono la regola 7 di 16 §6: niente dati dei clienti su servizi in beta [verificato]. L'uscita in 10-15 giorni-persona è [non verificato].
- **E.** Al posto di Notion mette un vault Markdown in git: per due CEO non tecnici è un passo indietro.
- **F.** La storia di sicurezza (RCE senza autenticazione, IDOR fra aziende) l'ha letta l'autore su GitHub [non verificato qui]. L'adattatore Claude parte con `dangerouslySkipPermissions` a true e la telemetria è accesa di default.

## 4. Vincitore: A, Hermes con il Cancello

1. **Il racconto per vendere.** Hermes Agent è l'orchestratore scelto per la visione [verificato: 10 §1]. «L'orchestratore che usiamo noi, in casa vostra» è il messaggio più forte verso le PMI.
2. **Rivendibile.** Licenza MIT; Hermes è single-tenant, quindi un'istanza per cliente [non verificato: lettura mia di 10 §5]; versione ospitata con regione Londra, senza DPA trovato [verificato: 18 §2.4].
3. **Semplice per i CEO.** Solo Slack: DM e un canale di approvazioni con bottoni. Nessuna app nuova (B), nessuna console in più (F).
4. **Costo basso e uscita scritta.** Se Hermes delude a fine fase 1 si cambia orchestratore; Cancello, memoria e ingresso restano.

**F è seconda a due punti.** Organigramma e budget sono pronti, ma il progetto non ha un team dichiarato [non verificato: 12 §0] e nel 2026 ha avuto falle critiche, gravi per un'offerta a più clienti.

## 5. Innesti

1. **Marketing (05 §5).** Agenti editoriale, copy e metriche (Metricool in sola lettura) in fase 1, non 3-4: con il funnel vuoto sono il primo valore commerciale.
2. **Precondizione.** Chiudere le decisioni D0 sulla compliance email e una mailbox live in SersanOutreach [verificato: 01 §6].
3. **Da C.** I tre colori dei dati (verde, giallo, rosso): una regola che i CEO capiscono subito.
4. **Da F.** Organigramma con costo e tetto per agente visibile ai CEO dalla fase 1, non dalla 4.
5. **Da E.** Stima realistica del Cancello (circa 21 giorni-persona). Chiamate dirette alla Messages API per i lavori semplici, sessioni solo per brief e offerte.
6. **Da G.** Pilota sulla VM Azure se l'hardware tarda, riserva del 30 % sulle stime e Slack Connect per i canali dei clienti [non verificato].
7. **Da B.** Un canale `#ingresso` letto solo da agenti senza strumenti d'azione.
8. **Per la rivendita.** Niente n8n nel pacchetto.
9. **Prima demo senza nuovi fornitori.** Claude Tag in Slack, già nel piano Team, a consumo con tetto, per domande sui dati interni nelle settimane 1-2 [verificato: 18 §2.1].

## 6. Dissenso più forte

Il problema commerciale di SerSan oggi non è l'orchestrazione: il funnel non c'è. Ci sono 11 lead e 0 meeting, l'email è ferma per la compliance, i founder non hanno pubblicato post. Ogni proposta assorbe 52-119 giorni-persona dei due tecnici, cioè 3-6 mesi tolti a clienti paganti e funnel, e a bundle finito il conto sale di 450 € al mese. Tesi: per 8-12 settimane solo ciò che è già pagato (Claude Team, Claude Tag, MCP di SersanOutreach), sblocco di email e post, 30 esiti misurati; poi la piattaforma. A ne accoglie metà: fase 0-1 corta, decisione a fine fase 1, Andrea e pipeline pesata solo con dati veri.
