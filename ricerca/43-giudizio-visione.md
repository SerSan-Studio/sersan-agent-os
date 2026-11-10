# Giudizio «visione» del terzo giro

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **G-vis**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Lente del giudice: visione e autonomia. Ogni criterio ha un voto da 0 a 10. I pesi erano fissati prima del giudizio: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10.

## Voti

| Proposta | Autonomia | Tempo al valore | Costi | Sicurezza essenziale | Server e manutenzione | Rischio | Totale pesato |
|---|---|---|---|---|---|---|---|
| P-A | 8 | 7 | 8 | 9 | 7 | 7,5 | **77,5** |
| P-B | 8,5 | 7 | 7,5 | 7 | 4,5 | 4,5 | **71,0** |
| P-C | 8 | 8,5 | 7 | 6,5 | 7 | 6,5 | **75,5** |
| P-D | 6,5 | 8 | 8,5 | 7 | 8 | 7,5 | **74,0** |

## Motivazioni, condizioni e obiezioni

### P-A · Motore Agent SDK con autonomia a livelli

Totale pesato 77,5 su 100 [non verificato: calcolo mio con i pesi fissati].
- Autonomia 8. Tiene l'idea intera: tutte le figure restano agenti veri su un solo motore, con bacheca e identità della persona [verificato: ricerca/36 §1.2 e §5.2]. Porta a L3 anche il primo follow-up alla persona appena incontrata, come nel post-call della trascrizione di riferimento [verificato: TR 4:42-5:07; il livello è una proposta di P-A §3.4]. La scala è corta: 5 sì per L2, 15 finestre per L3 [non verificato: soglie proposte]. Le skill interne salgono a L3 con una valutazione automatica. Resta sotto la trascrizione sulle aperture dell'agente vocale, ferme a L2 [verificato: TR 15:31-15:43], e parte piano: alla settimana 8 sono L3 solo riassunto, registro dei meeting e debrief [verificato: P-A §5.1].
- Sicurezza 9. Tiene le sei protezioni essenziali e toglie il resto: FIDO2 sulle carte, regole «Sempre», firme HMAC, codici per consegna, registro a catena, un solo effetto per giro [verificato: oggi in SPEC §2.1, §3, §4.7, §4.9 e in PRESENTAZIONE-CEO §5.4]. I criteri scendono da 27 a 18 [verificato: SPEC §12.4; P-A §7.2]. La finestra L2 riusa il compito periodico di 30 secondi che lo spec ha già [verificato: SPEC §4.7].
- Tempo al valore 7. La settimana 8 è la più povera delle quattro. Alla 21 ci sono CRM, Jira, posta smistata, bacheca completa e follow-up in L2 o L3, ma la fase 2 sale da 58,5 a circa 65 gp e P-A stessa mette in conto 1-2 settimane di ritardo [verificato: ricerca/36 §7.3; P-A §5.2-5.3].
- Costi 8. Come la v2.1, senza abbonamenti nuovi; la revisione esterna da 3.560-5.940 € diventa facoltativa [verificato: PRESENTAZIONE-CEO §12.1-12.2].
- Server 7. RAM come la v2.1: 8, 25, 53,5 e 70-74 GB, con l'acquisto prima della fase 3 [verificato: ricerca/36 §4.2]. Il codice è tutto nostro.
- Rischio 7,5. Dipende da un solo fornitore, l'API di Anthropic. L'uscita verso Hermes è prezzata: 26-33 gp [verificato: PRESENTAZIONE-CEO §15]. Oggi non c'è ancora codice [verificato: SPEC §12.2].

**Condizioni perché funzioni**

- Il parere legale ammette il follow-up in L2 e L3 verso chi ha partecipato alla call, con la riga che dichiara l'AI. Per ricerca/16 quel follow-up non è marketing a freddo, ma è una proposta da confermare [verificato: ricerca/16 §3, punto 2].
- I CEO fissano i tetti per classe dopo il parere, al posto della scelta sui messaggi «Sempre» [verificato: PRESENTAZIONE-CEO, appendice A, voce B5].
- Alberto cambia la regola di casa «su Metricool scrive solo una sessione presidiata» [verificato: ricerca/05 §5, regole 1 e 5; PRESENTAZIONE-CEO §8.2].
- Michele ammette Postiz prima della fase F4 del board, oppure resta Metricool, e imposta la riaccensione automatica del server [verificato: PRESENTAZIONE-CEO §6.2; DOMANDE-PER-MICHELE n. 22].
- Lo spec passa alla revisione 3 e nel PRD la metrica «effetti usciti senza carta: 0» diventa «effetti fuori dal livello consentito: 0» [verificato: PRD, «Metriche di successo»].
- To-do in Jira ed evento in calendario entrano come scritture L3 già nella fase 1, altrimenti la settimana 8 resta la più debole [non verificato: richiesta mia; oggi sono nella fase 2, verificato: ricerca/36 §7.3].
- Le soglie si tarano sui volumi veri: al 5 ottobre c'erano 11 lead e 0 meeting, e il PRD dà per probabile che le call siano poche [verificato: PRESENTAZIONE-CEO §7.1; PRD, «Rischi»].

**Obiezioni più forti**

- Alla settimana 8 mostra meno delle altre: tre agenti e nessuna scrittura in Jira o nel CRM [verificato: P-A §5.1].
- Le stime della fase 1 sono strette. P-A mette +2 gp per livelli, finestra, promozione e retrocessione; il Rapporto 2 stima 3-5 giorni la sola finestra e 2-4 giorni le classi [non verificato: sono due stime, nessuna misurata].
- Bacheca, profili con nome, bot e valutazione delle skill sono da scrivere: Hermes li darebbe pronti [verificato: PRESENTAZIONE-CEO §5.3].
- Sull'imparare da soli resta sotto la trascrizione: le skill passano da una valutazione ancora da costruire e le aperture di Andrea non superano L2 [verificato: P-A §3.4, flusso 9; TR 15:31-15:43].
- Con i volumi di oggi L3 verso l'esterno arriva dopo 20 follow-up puliti, cioè dopo mesi [non verificato: calcolo mio sulle soglie 5 e 15].

### P-B · Orchestratore autonomo pronto, con il nostro Cancello

Totale pesato 71,0 su 100 [non verificato: calcolo mio].
- Autonomia 8,5, la più alta sulla carta. È la più fedele all'idea: la lista delle funzioni nomina Hermes Agent come orchestratore sul nostro server [verificato: ricerca/00, voce A4]. È anche lo stesso orchestratore open source della trascrizione di riferimento, installato su una macchina propria, con agenti che imparano da soli [verificato: TR 3:23-3:59]. Profili, kanban con dispatcher e skill che l'agente scrive sono pronti [verificato: ricerca/27 §9.2; ricerca/34-proposta-2 §5.1]. Le skill interne sono L3 dalla fase 2 e le aperture di Andrea arrivano a L3 dentro una banca di frasi [non verificato: proposte di P-B §3.10]. Verso l'esterno però è la più prudente fra A, B e C: primo incontro L2, profili dei founder L0, pagina aziendale L2 solo dalla fase 4, Andrea nella fase 5 [verificato: P-B §3.2, §3.6, §3.7].
- Sicurezza 7. Tiene le sei protezioni e semplifica più di tutte: 16 criteri [verificato: P-B §7]. Ma i difetti aperti fra profili possono sfalsare tetti e registro per agente [verificato: ricerca/27 §6.2, righe GW-41 e KB-10]. E P-B non dice come evita che Hermes conservi testo rosso sul banco di prova [non verificato: assente in P-B; la proposta Hermes del secondo giro teneva i dati rossi fuori da Hermes, verificato: ricerca/34-proposta-2 §10.3].
- Tempo al valore 7. La settimana 8 è ricca: 5 profili, to-do in Jira, kanban, bot del Capo di gabinetto. Ma è appesa alla verifica: se fallisce, l'uscita costa 3-4 settimane [verificato: ricerca/34-proposta-2 §10.2].
- Costi 7,5. Licenza 0 € e mensili come la v2.1 [verificato: PRESENTAZIONE-CEO §12.1]; in più 1,5-2,5 gp al mese di manutenzione [verificato: ricerca/27 §8, stima di quel rapporto].
- Server 4,5. Tre contenitori più quello di prova, circa una release e mezza a settimana, nessuno di noi lo conosce a fondo [verificato: ricerca/27 §8; ricerca/36 §2.1]. Michele preferisce evitarlo [verificato: ricerca/36 §1.2].
- Rischio 4,5. Al 9/11 il gateway avrebbe 312 problemi, 83 risolti e 228 senza correzione [non verificato da me: letto su GitHub dal Rapporto 4 §3.2 e da P-B; in repo il dato è 276 aperti e 0 risolti al 25/10, verificato: ricerca/36 §1.4]. Due delle quattro condizioni dell'ADR-0012 non valgono e una non è provata [verificato: ADR-0012, «Decisione»; stato dal Rapporto 4 §3.4]. Un utente racconta chat che si mescolano fra bot [non verificato: testimonianza di terzi, trascrizione «Grokbot vs Hermes»].

**Condizioni perché funzioni**

- Alla verifica della settimana 8, con almeno 5 profili e due ingressi automatici, nessun risultato finisce al profilo o alla chat sbagliata e nessuna card sparisce [verificato: P-B §5.4, criterio 1].
- Alberto e Michele riscrivono l'ADR-0012, che oggi ammette Hermes come orchestratore solo a quattro condizioni; Michele accetta Hermes sul server e un termine di patch diverso per i contenitori non esposti [verificato: ADR-0012, «Decisione»; P-B §8].
- Lo sblocco della card quando arriva l'esito della carta funziona davvero: oggi è «da provare» [verificato: ricerca/34-proposta-2 §5.4, punto 6].
- Un solo bot per gateway, niente stanze di gruppo ospitate dal gateway, clienti mai sugli adattatori di Hermes [verificato: ricerca/27 §6.3].
- Prima del pilota si dimostra che Hermes non conserva testo rosso sul banco di prova [non verificato: richiesta mia; P-B non lo tratta].
- L'uscita verso il motore sull'Agent SDK resta pronta: 17,5-21 gp di base, 3-4 settimane [verificato: ricerca/34-proposta-2 §10.2].
- Mattia diventa co-manutentore di Hermes, perché oggi nessuno lo conosce a fondo [verificato: ricerca/36 §2.1].

**Obiezioni più forti**

- Mette nel percorso dei clienti un prodotto che la regola accettata del progetto oggi esclude [verificato: ADR-0012, «Decisione»].
- Un'azione L3 che parte con il contesto del profilo sbagliato non è autonomia: è controllo in più. P-B stessa rimanda l'autonomia verso i clienti a dopo la prova [verificato: P-B §1, riga 5].
- Toglie pezzi dell'idea: un solo bot al posto dei nove di squadra, stanze di gruppo spente, identità per contenitore e non per persona [verificato: P-B §2.3 e §5.3; ricerca/36 §1.4].
- Verso l'esterno è la più lenta: pagina aziendale in L2 solo dalla fase 4, Andrea nella fase 5, profili dei founder fermi a L0 [verificato: P-B §3.6-3.7].
- I giorni sono ottimistici. Nel secondo giro la proposta Hermes contava circa 0,6 gp a profilo contro 0,5-2 della v2 [verificato: ricerca/36 §2.4]. E l'elenco della settimana 21 conta già gli inviti dell'Agenda, che nella sua tabella arriva nella fase 3 [verificato: P-B §5.2 contro §9, voce K2].
- Raddoppia funzioni che il board ha già in n8n e LiteLLM [verificato: ricerca/27 §9.3].

### P-C · Ibrido: agenti autonomi in abbonamento dove rendono di più

Totale pesato 75,5 su 100 [non verificato: calcolo mio].
- Autonomia 8. È la più rapida a far uscire lavoro. Ricerca concorrenza, bandi e numeri del lunedì girano da soli dalle prime settimane con i compiti programmati di Cowork, che lavorano anche a computer spento [verificato: ricerca/34-proposta-3 §2], e poi con Managed Agents. Ha la scala più corta (5 e 10), il primo follow-up a L3 e i post aziendali a L3 dentro il calendario approvato [non verificato: proposte di P-C §3.1-3.2]. Impara meno di A e B: skill sul server in L2, aperture di Andrea ferme a L2. La bacheca arriva solo nella fase 2. Circa 12 agenti escono dal server, mentre l'idea e la trascrizione mettono l'orchestratore su una macchina propria [verificato: ricerca/00, voce A4; TR 3:34-3:39].
- Sicurezza 6,5. Le sei protezioni ci sono, ma con più pezzi: ponte con un token per fonte, stop da estendere e ancora da provare, registro degli agenti esterni affidato a uno strumento che l'agente deve chiamare [verificato: P-C §4.1]. Grok Bot non si comanda da programma [verificato: ricerca/11 §6]. Lo spec resta il più carico: 24 criteri tenuti o semplificati, più 6 nuovi [verificato: P-C §7.2-7.3; la somma è mia].
- Tempo al valore 8,5. La settimana 21 è la più ricca: brief automatico, bozza d'offerta, post in L2 da Metricool, che pubblica già sulla pagina LinkedIn [verificato: ricerca/33 §2.5].
- Costi 7. È la più cara al mese: Managed Agents a 0,08 $ per ora di sessione più i token [verificato: ricerca/18 §0, punto 4], Metricool che resta a 59,86 € [verificato: ricerca/36 §8.2], Grok Bot facoltativo.
- Server 7. Un po' meno RAM a regime [non verificato: stima di P-C §2.4]; un endpoint pubblico in più.
- Rischio 6,5. Il cuore è lo stesso di P-A. In più Managed Agents è in beta e senza conservazione zero [verificato: ricerca/12 §1], e i compiti programmati agiscono a nome di una persona [verificato: ADR-0011, «Alternative considerate»]. Tornare sul motore è facile.

**Condizioni perché funzioni**

- Alberto e i CEO accettano due eccezioni scritte: Managed Agents era escluso per la regola «tutto in casa», e i compiti programmati di Claude Team non potevano fare processi aziendali [verificato: ricerca/26 §1.2; ADR-0011, «Decisione»].
- Negli abbonamenti entrano solo dati verdi e solo connettori in sola lettura, perché i compiti programmati scrivono sui connettori senza chiedere [verificato: ricerca/05 §5, regola 5].
- L'oscuramento che toglie nomi e aziende dalle obiezioni funziona. Altrimenti il marketing in abbonamento lavora senza ciò che si sente in call [non verificato: dipendenza segnalata da me].
- Lo stop che revoca i token e sospende le esecuzioni programmate è provato prima del pilota: P-C lo dà come da provare [verificato: P-C §4.1, punto 2].
- Michele ammette il ponte MCP pubblico e Metricool resta come eccezione stabile [verificato: P-C §2.2; richiesta analoga in DOMANDE-PER-MICHELE n. 6].
- Il parere copre i trasferimenti verso gli USA anche per gli abbonamenti, e il DPA di Grok Bot va letto prima di usarlo [verificato: P-C §4.3, punto 6].

**Obiezioni più forti**

- Il guadagno è soprattutto di calendario. Le stesse squadre starebbero sul server con circa 4 GB [verificato: P-C §8, stima]. La regola di Alberto paga l'abbonamento quando un pezzo non sta sul server, e qui ci starebbe [verificato: testo del compito].
- Sposta fuori casa proprio una parte degli agenti, mentre l'idea e la trascrizione li vogliono su una macchina propria.
- Marketing e vendite si parlano attraverso un ponte che passa solo campi verdi: la collaborazione della voce J7 si assottiglia [non verificato: lettura mia di P-C §2.1].
- Più fornitori in beta da seguire, e uno stop che non ferma tutto.
- Sull'imparare da soli è sotto P-A e P-B.
- È la proposta che semplifica meno lo spec.

### P-D · Automazione prima: n8n con passi AI e pochi agenti

Totale pesato 74,0 su 100 [non verificato: calcolo mio].
- Autonomia 6,5. Automatizza molto e presto dentro l'azienda: alla settimana 8 sono L3 riassunto, registro, to-do in Jira, debrief ed evento in calendario [verificato: P-D §5.1]. Per la mia lente però è la più lontana dall'idea: 35-40 figure diventano flussi n8n e le sessioni con strumenti consegnano solo bozze [verificato: P-D §1 e §9]. Nel secondo giro una scelta simile fu scartata come declassamento degli agenti [verificato: ricerca/36 §1.3]. Qui i flussi partono da soli, e la trascrizione stessa indica catene da automatizzare [verificato: TR 13:11-13:20]. Ma nessun agente sceglie il passo dopo, scrive le proprie skill o parla con un altro, come fanno quelli della trascrizione [verificato: TR 3:53-4:30]. La scala è la più lenta: 10 carte di fila in 30 giorni, poi 20 invii, più l'avvio «in ombra»; il primo follow-up dopo una prima call resta a L2 e la newsletter a L1 [verificato: P-D §3.2-3.4]. Con 0 meeting al 5 ottobre le 10 carte in 30 giorni rischiano di non arrivare [verificato: PRESENTAZIONE-CEO §7.1 per il dato; il resto è un calcolo mio].
- Sicurezza 7. Ottiene molto con poco: il codice sceglie i destinatari e il modello scrive senza strumenti, il disegno che il giudice di sicurezza chiamò il più robusto [verificato: ricerca/35-giudizio-sicurezza §3.2]. Perde punti perché aggiunge prudenza che rallenta: avvio in ombra, soglie alte, tetto L2.
- Tempo al valore 8. È la consegna più credibile: nessun motore nella fase 1, e n8n è già nel board [verificato: P-D §7.1; ADR-0011, «Contesto»].
- Costi 8,5. Circa 230 gp contro 249, e fasi 0-1 a 37,5 gp [non verificato: stime di P-D §6.3; la base è verificata in ricerca/36 §7.2].
- Server 8. La RAM più bassa, 60-64 GB a regime [non verificato: stima di P-D §2.3].
- Rischio 7,5. Tecnica matura. Però la licenza di n8n vieta la rivendita [verificato: ADR-0011, «Conseguenze negative»], e il progetto vuole anche un'offerta da rivendere alle PMI [verificato: PRESENTAZIONE-CEO §1 e §2.3].

**Condizioni perché funzioni**

- Alberto decide in modo esplicito che la maggior parte delle figure sia un flusso e non un agente: nel secondo giro la sua regola diceva il contrario [verificato: ricerca/36 §1.3].
- Le soglie scendono verso quelle di P-A o di P-C, e il primo follow-up può salire a L3 dopo il parere [non verificato: richiesta mia].
- Michele mette n8n sul banco di prova già nella fase 1 [verificato: P-D §6.4].
- I flussi che leggono testo rosso non salvano le esecuzioni, e il testo rosso non attraversa un nodo Wait [verificato: P-D §4.4, da documentazione letta dal suo autore il 9/11].
- Ogni flusso ha un nome, un responsabile e prove su dati registrati, e si può trasformare in una sessione con strumenti [verificato: P-D §8].
- Carte e «Ferma» passano dalla Porta, perché il nodo Teams di n8n registra l'ora della risposta ma non chi risponde [verificato: ricerca/28 §2.4].

**Obiezioni più forti**

- È la meno fedele alla trascrizione: automazioni più che agenti che lavorano e imparano da soli.
- L'apprendimento è il più debole: esempi dalle correzioni, e modifiche alle istruzioni in L1 e poi in L2 [verificato: P-D §3.4, flusso 9].
- La scala è la più lenta. E il riassunto promette il livello della trascrizione, mentre il §3.5 ammette che il primo follow-up resta L2 [verificato: P-D §1, riga 5, contro §3.5].
- Cade la regola «la logica del motore non dipende da n8n» e si riscrivono tre ADR [verificato: ADR-0011, «Decisione»; P-D §7.5].
- n8n diventa il punto critico: licenza senza rivendita [verificato: ADR-0011, «Conseguenze negative»] e una vulnerabilità grave nel 2026 [non verificato: ADR-0011, «Rischi», fonti di terzi].
- 35-40 flussi visuali da tenere in ordine in quattro persone [non verificato: lettura mia del conteggio di P-D §9].

## Raccomandazione

Per la lente della visione scelgo P-A come base, con tre innesti presi dalle altre proposte.

Totali pesati su 100: P-A 77,5; P-C 75,5; P-D 74,0; P-B 71,0 [non verificato: calcolo mio con i pesi fissati]. Le distanze sono piccole, quindi contano le condizioni.

Cosa ho controllato. Il 10/11/2026 ho letto la trascrizione di riferimento per intero e, nella repo, la proposta v2.1, lo spec, il PRD, ricerca/00, 27, 34-proposta-2, 35-giudizio-visione, 36, gli ADR-0011 e 0012 e le domande per Michele. Ho letto anche la trascrizione di terzi «Grokbot vs Hermes». I fatti presi dal web il 9/11 non li ho riletti: li cito dal Rapporto 4. Non ho modificato file e non ho lasciato processi accesi.

Perché P-A. Le quattro proposte fanno la stessa mossa decisiva: un Cancello che dà un livello a ogni classe d'azione, con la finestra L2 e la discesa automatica. Cambia solo il motore. P-A tiene insieme tutto ciò che la mia lente chiede:
- agenti veri che si passano il lavoro;
- il post-call a L3 anche al primo follow-up, come nella trascrizione di riferimento [verificato: TR 4:42-5:07];
- la scala corta;
- lo spec più snello, da 27 a 18 criteri;
- nessun fornitore nuovo.

Il suo difetto è la settimana 8. Si corregge con innesti già scritti nelle altre proposte:
1. Da P-D: to-do in Jira ed evento in calendario come scritture L3 già nella fase 1; catene a schema senza strumenti per i passi più semplici, con i destinatari presi dai dati.
2. Da P-C: nelle settimane 1-8 le ricerche su dati verdi con i compiti programmati di Cowork in sola lettura, come ponte dichiarato; Metricool come esecutore dei post finché Postiz non è ammesso; le soglie 5 e 10. Managed Agents resta la leva da usare quando un pezzo non sta sul server, come chiede Alberto.
3. Da P-B: il Capo di gabinetto già nella fase 1, il modello della kanban, le skill legali bloccate, la banca di frasi che porta a L3 le aperture di Andrea, il conteggio delle call con i clienti già attivi per raggiungere le soglie.

Su Hermes. Sulla carta P-B è la più vicina all'idea e alla trascrizione, e le ho dato il voto di autonomia più alto. Oggi però un'azione L3 che parte con il contesto sbagliato toglie autonomia invece di darla, e due condizioni dell'ADR-0012 non valgono [verificato: ADR-0012, «Decisione»; stato dal Rapporto 4 §3.4, non riletto da me]. Propongo il pilota confinato in laboratorio, 6-8 gp [verificato: PRESENTAZIONE-CEO §15], con due misure: quante skill Hermes migliora da solo e quante volte sbaglia profilo. Se il pilota passa e le condizioni si chiudono, il confronto si rifà sui numeri.

Su P-D. Va presa come metodo, non come architettura: un flusso dove basta un flusso. Come base toglierebbe proprio gli agenti che lavorano e imparano da soli, cioè il cuore della richiesta di Alberto.

Tre decisioni servono con qualsiasi proposta:
- il parere legale sul follow-up che parte senza un sì esplicito;
- il cambio della regola della sessione presidiata, che spetta ad Alberto;
- la riscrittura dello spec alla revisione 3, con la metrica «effetti fuori dal livello consentito: 0» e le misure di autonomia: minuti fra fine call e follow-up, quota di azioni in L2 e L3, «Ferma» ogni 100 finestre.
