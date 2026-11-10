# Giudizio «cpto» del terzo giro

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **G-cpto**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Lente del giudice: CPTO e tecnica. Ogni criterio ha un voto da 0 a 10. I pesi erano fissati prima del giudizio: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10.

## Voti

| Proposta | Autonomia | Tempo al valore | Costi | Sicurezza essenziale | Server e manutenzione | Rischio | Totale pesato |
|---|---|---|---|---|---|---|---|
| P-A | 8 | 7 | 7,5 | 9 | 6,5 | 7 | **75,8** |
| P-B | 7,5 | 7,5 | 6,5 | 6,5 | 4 | 4 | **65,5** |
| P-C | 8 | 7,5 | 6 | 7 | 5,5 | 6 | **70,5** |
| P-D | 7,5 | 8,5 | 8 | 8,5 | 8 | 6,5 | **78,2** |

## Motivazioni, condizioni e obiezioni

### P-A · Motore Agent SDK con autonomia a livelli

Tiene l'architettura che Michele ha già recepito (motore sull'Agent SDK, Cancello unico esecutore) [verificato: ADR-0001, stato; ADR-0003] e cambia solo la regola: un livello per terna al posto di una carta per azione. La finestra L2 riusa il compito periodico da 30 secondi che lo spec ha già [verificato: SPEC §4.7], quindi il passo tecnico è piccolo. A regime è la più vicina alla trascrizione di riferimento: follow-up L3 anche alla persona appena incontrata, skill interne L3, stand-up degli agenti [non verificato: proposta di P-A §3.4]. Dalla mia lente ha tre limiti. Il server pesa come nella v2.1: 8, 25-27, 53,5 e 70-74 GB nuovi, con margine zero dalla fase 3 [verificato per la v2.1: R36 §4.2; P §6.3]. Le fasi 0-1 salgono a 42,5-44 gp di base, circa 57-59 con la riserva, contro 52 di capacità in otto settimane [verificato: R36 §7.1-7.2 per capacità e base della v2.1; calcolo mio]. Alla settimana 8 non scrive ancora in Jira, nel CRM e in calendario [non verificato: P-A §5.1]. Totale pesato: 75,75 su 100 [calcolo mio].

**Condizioni perché funzioni**

- Michele conferma la revisione di ADR-0003: livelli al posto della carta per ogni azione, niente FIDO2 sulle carte, Cancello anche nella VM del motore. Oggi l'ADR dice che il Cancello resta sempre in una macchina separata [verificato: ADR-0003, alternativa «Cancello nella stessa macchina del motore»].
- I CEO fissano i tetti per classe dopo il parere legale, i cui punti del pilota arrivano entro la settimana 3 [verificato: P §9.4]. Senza parere il follow-up resta L1.
- La fase 1 va riportata dentro la capacità. Proposta mia: niente lettore periodico scritto nel motore, n8n sul banco di prova per orari e trascrizioni come in P-D, e bacheca minima solo se avanza tempo [non verificato: proposta mia; capacità verificata: R36 §7.1].
- I 192 GB in più vanno ordinati prima della fase 3 e il margine va misurato con 6 sessioni. Andrea su CPU nella fase 3 solo con Vexa Lite, perché il margine scende a circa -9 GB [verificato: R36 §4.2 per la regola e per Vexa Lite; -9 GB è una stima di P-A §2.2].
- Postiz prima della fase F4 solo con il sì di Michele: fino ad allora entrano solo i servizi del pilota [verificato: P §6.2]. Altrimenti resta Metricool.
- Batteria di prova automatica a ogni aggiornamento dell'SDK, in uso entro 14 giorni, e TypeScript confermato da Mattia [verificato: SPEC §7.6; DOM n. 28].
- Riaccensione automatica del server e linea di riserva prima del primo L3 verso l'esterno fuori orario [verificato: DOM n. 22; P §14, decisione 13].

**Obiezioni più forti**

- Non alleggerisce chi amministra il server. Restano 11-13 servizi e 3 reti nuove nel perimetro delle patch a 14 giorni [verificato: P §13; ADR-0002, «Negative»], e in più anticipa Postiz e forse Andrea [non verificato: P-A §2.1].
- L'autonomia è tutta codice nostro: motore, bacheca, Porta, nove bot. Lo conoscono due persone, e l'SDK conta 333 versioni TypeScript dal 27/09/2025 [verificato: ADR-0001, «Negative»].
- La fase 1 è la più carica delle quattro e alla settimana 8 dà meno lavoro interno delle altre: to-do solo dentro il riassunto, CRM e Jira nella fase 2 [non verificato: P-A §5.1, confronto mio con P-B §5.2 e P-D §5.1].
- Il lettore periodico dentro il motore dura una fase sola, poi lo sostituisce n8n. È lavoro da buttare e va contro la regola «il motore non duplica nulla» [verificato: ADR-0011, Decisione].
- Soglie di 5 e 15 con volumi quasi nulli: 11 lead, 1 risposta e 0 meeting al 5 ottobre [verificato: P §7.1]. Le promozioni si decidono su campioni molto piccoli, e non è scritto se contano le call interne.
- Il totale «quasi uguale» (250-254 gp) regge solo se le semplificazioni valgono davvero circa 5 gp nella fase 1. Lo spec non ha ancora codice, quindi non c'è un dato misurato [verificato: SPEC §12.2; stime di P-A §5.2 non verificate].

### P-B · Orchestratore autonomo pronto, con il nostro Cancello

Hermes dà pronti bacheca kanban, cron, profili e skill che l'agente scrive da solo [verificato: R27 §9.2; R34-2 §5.1]. È il disegno più vicino all'orchestratore che la trascrizione di riferimento descrive: open source, su una macchina propria, con agenti che imparano da soli [verificato: TR 3:25-3:59]. Alla settimana 8 porta già passaggi fra cinque profili e to-do in Jira [non verificato: P-B §5.2]. Dalla mia lente però è la più pesante da tenere in piedi. La repo mette quattro condizioni prima di usare Hermes come orchestratore, e Michele ha chiesto di evitarlo se possibile [verificato: ADR-0012, Decisione; ADR-0001, «Perché no»]. Al 9/11 la v0.23 è uscita, ma le righe di sicurezza MSG-43, GW-41, KB-10, HR-6 e il bug #113578 risultano ancora aperti [non verificato da me: letto il 9/11 da Rapporto 4 §3 e da P-B, due letture concordi]. La manutenzione stimata è 1,5-2,5 gp al mese [verificato: R27 §8, stima di quel rapporto]. L'identità verso la memoria vale per contenitore, non per persona [verificato: R27 §4]. La RAM non scende: 71-79 GB nuovi a regime contro 70-74 [non verificato: stima di P-B §2.4; v2.1 verificata: R36 §4.2]. Totale pesato: 65,5 su 100 [calcolo mio].

**Condizioni perché funzioni**

- Michele accetta di rovesciare ADR-0001 e ADR-0012 e di mettere un secondo ecosistema nel perimetro delle patch a 14 giorni, senza la deroga al termine che P-B gli chiede [verificato: ADR-0001; ADR-0012; la richiesta di deroga è in P-B §8].
- Prima di qualsiasi dato giallo dei clienti valgono tutte e quattro le condizioni di ADR-0012, non solo il criterio 1 di P-B: righe di sicurezza chiuse su main, #113578 chiuso, un aggiornamento che passa i dieci scenari senza interventi a mano [verificato: ADR-0012; R27 §11].
- La prova delle settimane 5-8 va fatta dietro LiteLLM, non solo con la chiave diretta: KB-11 e MP-19/23/25 colpiscono proprio i lavoratori della kanban e i fornitori con nome [verificato: R27 §3.2, stato al 25/10/2026].
- Lo sblocco della card quando arriva l'esito della carta va dimostrato: nella repo è ancora «da provare» [verificato: R34-2 §5.4, punto 6].
- Un responsabile delle patch nominato e 18-30 gp l'anno messi in conto solo per Hermes [calcolo mio su R27 §8].
- Cancello scritto senza dipendenze da Hermes, così l'uscita verso il motore SDK resta a 17,5-21 gp di base e 3-4 settimane [verificato: R34-2 §10.2, stima di quel rapporto].

**Obiezioni più forti**

- Il gateway condiviso. Al 25/10 la scheda contava 276 problemi aperti, 9 di sicurezza e 0 risolti [verificato: R36 §1.4]; al 9/11 sarebbero 312, con 228 senza correzione [non verificato da me: Rapporto 4 §3.2]. Un solo bot evita MSG-43, ma GW-41 e KB-10 riguardano segreti e cartelle scambiati fra profili dello stesso gateway [verificato: R27 §6.2]. Con tre contenitori i profili per gateway sono circa 18, 12 e 27 [calcolo mio sulle squadre di R36 §5.3]. Un riassunto con i dati di un altro cliente, a L3, è l'errore che non si ritira.
- KB-11 e MP-19/23/25 non compaiono fra i rischi di P-B, eppure stanno sul percorso che usa di più: la kanban dietro LiteLLM [verificato: R27 §3.2; assenza verificata nel testo di P-B §8].
- Patch a 14 giorni: 44 release dal 12/3 al 23/10 e almeno 45 avvisi di sicurezza nel 2026, con note di rilascio che dichiarano modifiche non documentate [verificato: R27 §7.1, §7.2, §8]. Chiedere un termine più lungo per i contenitori non esposti vuol dire chiedere a Michele di allentare Cyber Essentials.
- I 221-230 gp non si confrontano con gli altri piani. La stessa stima a 0,6 gp per profilo era già stata riportata a circa 200 gp per la Proposta 2 [verificato: R35-cpto §3.2; R36 §2.4]. E le fasi 0-1 costano più della v2.1: 43-45 gp di base, 57-60 con la riserva, su 52 di capacità [non verificato: P-B §6.4; capacità verificata: R36 §7.1].
- Con un solo bot spariscono i nove bot di squadra, e la chat fra agenti è uno specchio scritto da noi, perché le stanze di gruppo di Hermes non si usano [non verificato: P-B §5.3 e §3.9].
- Doppioni con il board su cron, webhook e budget [verificato: R27 §9.3]. Con l'identità per contenitore, il coaching «solo all'interessato» si regge su una consegna 1:1 del Cancello e non sui permessi della memoria [verificato: R27 §4; soluzione: P-B §3.8].
- Nessuno di noi conosce Hermes a fondo [verificato: R34-2 §10.1], e una testimonianza di terzi racconta chat di bot diversi che si mescolano nell'uso reale [non verificato: file «Grokbot vs Hermes.txt», fonte di terzi].

### P-C · Ibrido: agenti autonomi in abbonamento dove rendono di più

È la proposta che fa uscire lavoro autonomo prima: ricerca, bandi e bozze dalle settimane 1-2 sui compiti programmati di Claude Team, poi su Managed Agents. Ha anche la scala più corta verso L3: 5 sì, poi 10 esecuzioni [non verificato: P-C §3.1, §5.1]. Le squadre in abbonamento continuano a lavorare anche a server fermo. Dalla mia lente però compra poco. Gli abbonamenti tolgono al server circa 6 GB a regime (64-68 contro 70-74) e i 192 GB in più servono comunque prima della fase 3 [non verificato: stima di P-C §2.4; v2.1 verificata: R36 §4.2]. In cambio i runtime da tenere diventano tre o quattro, con stop, tetti e registro da ricucire fra loro. Va contro tre decisioni registrate: Managed Agents escluso, board vincolante, nessun processo aziendale sui compiti programmati [verificato: ADR-0001, alternativa «Managed Agents»; ADR-0002; ADR-0011, Decisione]. Costa di più ogni mese, e i giorni di sviluppo restano 251-337 [non verificato: P-C §6-7]. Totale pesato: 70,5 su 100 [calcolo mio].

**Condizioni perché funzioni**

- Sì scritto di Michele a un'eccezione ad ADR-0002 e ad ADR-0011, limitata ai dati verdi e ai connettori in sola lettura imposti dall'amministratore [verificato: ADR-0002, «Chi decide»; ADR-0011].
- Lo stop esteso va provato prima del primo agente in abbonamento: revoca dei token del ponte e sospensione via API delle esecuzioni programmate. P-C stessa scrive che va provato [non verificato: P-C §4.1, punto 2].
- Un solo runtime in abbonamento, Managed Agents. Grok Bot resta fuori dal percorso: non ha un'API pubblica per comandare i Bot, e registro delle azioni e audit sono solo Enterprise [verificato: R11, «API per integrare» e tabella dei controlli, righe 122 e 232].
- I compiti di Claude Team solo come ponte fino alla settimana 8, sull'account di una persona nominata: appartengono a un solo account, agiscono a suo nome e non girano più di una volta l'ora [verificato: ADR-0011, alternativa sui compiti programmati; R36 §1.3].
- Il parere legale copre anche Managed Agents: ciclo e sessioni stanno da Anthropic, e per questo il servizio era stato escluso [verificato: R26 §1.2]. Che manchi la conservazione zero e che la sede dei dati sia negli USA lo dice Rapporto 4 §2.1 [non verificato da me].
- Il ponte MCP pubblico entra solo dalla fase 2, con un responsabile delle patch e un token per fonte [non verificato: proposta mia su P-C §2.2].

**Obiezioni più forti**

- Non risolve il problema del server. Le squadre verdi sono lavori leggeri: spostarle fuori non evita né la RAM né la seconda GPU, che anzi diventa consigliata già all'inizio della fase 3 [non verificato: P-C §2.4].
- Più pezzi per quattro persone: due cicli di aggiornamento (SDK sul server e Managed Agents in beta), più contatori di spesa, un registro che dipende da uno strumento chiamato dall'agente [non verificato: P-C §4.1].
- Doppio trasloco: compiti di Claude Team nelle settimane 1-8, poi Managed Agents, poi il motore se serve l'uscita. Ogni passaggio è lavoro di configurazione che non resta [non verificato: lettura mia di P-C §5.2 e §8].
- Costa di più ogni mese senza togliere giorni: Managed Agents 13-35 €, Metricool 59,86 € anche dopo la fase 4, token 10-40 €, Grok Bot 54-205 € se scelto [non verificato: stime di P-C §6.1; verificati il prezzo di Metricool, R36 §8.2, e gli 0,08 $ per ora di sessione, R18 In breve punto 4].
- Lo spec non si alleggerisce: 24 criteri restano e ne entrano 6, due dei quali esistono solo per l'ibrido (ingresso esterno e stop esteso). Sono 30 contro i 27 di oggi [calcolo mio su P-C §7.2-7.3; 27 criteri verificati: SPEC §12.4].
- Un secondo endpoint MCP pubblico, mentre la v2 ne voleva uno solo: più regole da tenere su Pangolin [verificato: R36 §4.4].
- Tenere Metricool al posto di Postiz rovescia anche ADR-0013 [verificato: ADR-0013, Decisione].

### P-D · Automazione prima: n8n con passi AI e pochi agenti

È la più leggera per il server e per chi lo amministra. Stima 60-64 GB nuovi a regime contro 70-74, e circa 6 GB liberi nelle fasi 3-4 invece di zero, senza la VM e la VLAN del motore [non verificato: stime di P-D §2.3; v2.1 verificata: R36 §4.2]. Usa un pezzo che è già nel board di Michele e che fa girare i bandi [verificato: R25 §2, C27; R36 §4.1]. È l'unica le cui fasi 0-1 stanno nella capacità anche con la riserva: 37,5 gp di base, circa 50, su 52 [non verificato: stima di P-D §6.3; capacità verificata: R36 §7.1]. Alla settimana 8 ha più lavoro interno a L3 delle altre [non verificato: P-D §5.1]. Il modello scrive il testo ma non sceglie destinatari né azioni, e la chiamata a schema senza strumenti è il disegno più robusto contro le iniezioni [verificato: R36 §5.2]. La trappola dei dati rossi nelle esecuzioni di n8n è reale e la proposta la gestisce: di serie n8n salva tutte le esecuzioni e le cancella dopo 336 ore [verificato: documentazione di n8n letta con Context7 il 10/11/2026]. Limiti: scala più lenta, apprendimento più debole, e n8n come punto critico con una licenza che vieta la rivendita [verificato: ADR-0011, «Negative»]. Totale pesato: 78,25 su 100 [calcolo mio].

**Condizioni perché funzioni**

- Michele dice sì a n8n sul banco di prova nella fase 1 e a un nuovo ADR che sostituisce in parte ADR-0001, 0003 e 0011, oggi tutte accettate [verificato: stato delle tre ADR]. Finché la fase F4 non porta n8n e LiteLLM sul server, i flussi restano sul banco di prova con soli dati verdi e gialli [verificato: R36 §7.1].
- La logica resta fuori da n8n: prompt, schemi, classi e scelta dei destinatari stanno in file versionati e in un piccolo servizio TypeScript che i flussi chiamano. n8n fa solo avvii, attese e passaggi. Così resta vera la regola che tiene la logica indipendente da n8n, e l'uscita verso il runner costa poco [verificato: ADR-0011, Decisione; il resto è una proposta mia].
- Versione 2.x fissata, solo webhook firmati, nessun salvataggio delle esecuzioni nei flussi che leggono testo rosso, e controllo del database di n8n alla verifica della settimana 8 [verificato: variabili EXECUTIONS_DATA_SAVE_* e impostazione per flusso, documentazione di n8n letta con Context7 il 10/11/2026].
- Scala allineata a P-A: 5 sì per L2, 15 finestre per L3, niente settimana d'ombra per i flussi interni, e classe «persona appena incontrata» fino a L3 dopo il parere [non verificato: proposta mia].
- Bacheca in PostgreSQL come registro unico dei passaggi, con lo specchio nel canale «Agenti». Ogni flusso ha nome, responsabile e tetto nel registro degli agenti, come la v2 chiede per ogni tipo di lavoro [verificato: R36 §5.2, §5.4].
- Proposte di skill e di istruzioni con valutazione automatica già nelle fasi 2-3, non nella 4 [non verificato: proposta mia, presa da P-A §3.4].
- Carte e «Ferma» solo dalla Porta: su Teams il nodo di n8n registra quando si risponde, non chi [verificato: R28 §2.4; ADR-0003, alternativa «approvazioni con n8n»].
- Postiz nella fase 2 solo con il sì di Michele [verificato: P §6.2].
- Decisione scritta sulla rivendita: se il sistema si offre alle PMI, i flussi passano al runner o serve una licenza commerciale di n8n, il cui prezzo non è nei file [verificato: ADR-0011, «Negative»].

**Obiezioni più forti**

- Dipendenza da n8n. P-D stima 35-40 figure su 57 come flussi, e cade la regola che oggi tiene la logica fuori da n8n [verificato: ADR-0011, Decisione; il conteggio è una stima di P-D §9]. La licenza vieta la rivendita, mentre la proposta ai CEO presenta il sistema come offerta da rivendere alle PMI [verificato: ADR-0011; P §1]. L'uscita completa vale circa 1 gp a flusso [non verificato: stima di P-D §8].
- La lente visione aveva contato come declassamento anche i flussi fissi, non solo le skill: 39 figure su 57 nella Proposta 3 [verificato: R35-visione, In breve; ADR-0001]. P-D ricorda solo le 10 skill. Per gli agenti che si parlano e imparano da soli è la più lontana dalla trascrizione di riferimento [verificato: TR 3:53-4:30].
- Scala la più lenta delle quattro: ombra, 10 sì, 20 invii; newsletter L1 e primo follow-up L2 anche a regime [non verificato: P-D §3.2-3.4]. Con i volumi di oggi il follow-up alla settimana 8 resta L1 [volumi verificati: P §7.1].
- n8n diventa il punto critico: una vulnerabilità con CVSS 10 nel 2026 secondo fonti di terzi [non verificato: ADR-0011, «Rischi»] e una 3.0 con modifiche incompatibili [non verificato da me: Rapporto 4 §5]. I flussi in JSON si provano e si rivedono peggio del codice.
- La stima di circa 230 gp è ottimistica. Il contenuto dei 57 agenti vale 67 gp nella v2.1 e non cala solo perché diventa un flusso [verificato: R36 §2.4]; P-D stessa chiede di rifarla con Mattia.
- Parte del risparmio di RAM nella fase 2 è una stima più stretta, non architettura: 7 GB per 6 sessioni contro i 12 della v2.1, con lo stesso tetto [verificato: R36 §4.2; R26, 1 GiB per sessione come punto di partenza].
- Il limite di spesa per area di lavoro nella Console, su cui P-D appoggia i tetti del banco di prova, è ancora un'ipotesi da confermare [verificato: SPEC §12.2].

## Raccomandazione

Classifica sulla mia lente, con i pesi fissati (35, 20, 15, 10, 10, 10): P-D 78,25; P-A 75,75; P-C 70,5; P-B 65,5 [calcolo mio]. Il distacco fra le prime due è di 2,5 punti e dipende dal voto di autonomia: l'ordine si inverte solo se P-A sale di mezzo punto e insieme P-D scende di mezzo. Non lo leggo come una vittoria netta.

Raccomando P-D come base delle fasi 0-2, con il motore di P-A come binario di crescita e non come alternativa.

Perché P-D:
- È l'unica che toglie peso a Michele invece di aggiungerne: meno RAM, niente VM e VLAN del motore, un servizio che è già nel suo board. Il giudizio CPTO del 25/10 aveva indicato proprio lì il collo di bottiglia [verificato: R35-cpto §6].
- È l'unica che, per sua stima, sta nelle otto settimane anche con la riserva (circa 50 gp su 52) [non verificato: P-D §6.3; capacità verificata: R36 §7.1].
- L'autonomia che promette è la più facile da mantenere: un flusso avviato da un evento parte sempre, e il modello non sceglie i destinatari.
- Resta dentro la frase del board «il server cerca e prepara, Claude ragiona» [verificato: R35-cpto §4.6].

Cosa prendere dalle altre:
- Da P-A: la scala 5 e 15, la classe «persona appena incontrata» fino a L3 dopo il parere, le skill proposte dagli agenti con valutazione automatica, lo stand-up degli agenti e il runner sull'Agent SDK, che dalla fase 2 cresce per i profili a più passi. Così le 57 figure restano agenti del registro, e passare da flusso a sessione è una promozione, non una riscrittura.
- Da P-C: solo la riserva. Managed Agents su dati verdi resta un'uscita prezzata se il server è pieno o fermo, a 0,08 $ per ora di sessione attiva [verificato: R18, In breve punto 4]. Non come base, perché oggi toglie al server solo circa 6 GB.
- Da P-B: niente nel percorso dei clienti. Hermes resta il pilota in laboratorio da 6-8 gp, quando valgono le quattro condizioni [verificato: ADR-0012]. Ne copio le idee: conteggio dei passaggi dall'ultimo messaggio umano, blocco delle skill curate a mano, politica per i turni persi [non verificato da me: Rapporto 4 §3.3].

Tre paletti senza i quali non la raccomanderei:
1. La logica fuori da n8n, in file versionati e in un servizio TypeScript, per non perdere l'uscita e la rivendita [verificato: ADR-0011].
2. Bacheca e registro degli agenti in PostgreSQL, non nella cronologia di n8n.
3. Carte e «Ferma» solo dalla Porta, perché su Teams n8n non registra chi risponde [verificato: R28 §2.4].

Cosa cambia subito:
- Lo spec della milestone 1 passa alla revisione 3 come «Cancello a livelli e primi due flussi», senza runner. Non si perde lavoro, perché la repo contiene solo documenti [verificato: SPEC §12.2].
- A Michele vanno tre domande: n8n sul banco di prova, il nuovo ADR, Postiz prima della fase F4.

Valgono per tutte e quattro le proposte:
- I tetti L2 e L3 verso l'esterno li apre il parere legale, entro la settimana 3 [verificato: P §9.4].
- La RAM si compra quando il margine misurato scende sotto i 5 GB [verificato: R36 §4.2].
- Riaccensione automatica del server e linea di riserva vengono prima del primo L3 esterno fuori orario [verificato: DOM n. 22; P §14, decisione 13].
- Nessuna proposta aggiunge lavoro alla GPU. Sulla rete, P-D toglie la VLAN del motore e P-C aggiunge un endpoint pubblico [non verificato: P-D §2.2; P-C §2.2].

Non ho modificato file e non ho lasciato processi accesi.
