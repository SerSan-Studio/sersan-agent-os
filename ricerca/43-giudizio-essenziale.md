# Giudizio «essenziale» del terzo giro

> Terzo giro di valutazione (autonomia), 9-10 novembre 2026. Negli altri documenti del giro questo file è citato come **G-ess**. La decisione e l'indice del giro sono in [45-architettura-v3.md](45-architettura-v3.md).

Lente del giudice: protezioni essenziali e affidabilità. Ogni criterio ha un voto da 0 a 10. I pesi erano fissati prima del giudizio: autonomia 35, tempo al valore 20, costi 15, sicurezza essenziale 10, server e manutenzione 10, rischio 10.

## Voti

| Proposta | Autonomia | Tempo al valore | Costi | Sicurezza essenziale | Server e manutenzione | Rischio | Totale pesato |
|---|---|---|---|---|---|---|---|
| P-A | 8 | 7 | 8 | 8,5 | 7 | 7,5 | **77,0** |
| P-B | 8,5 | 7 | 7,5 | 5,5 | 5 | 4,5 | **70,0** |
| P-C | 7,5 | 7,5 | 6,5 | 6,5 | 7,5 | 6,5 | **71,5** |
| P-D | 7 | 8,5 | 8,5 | 9 | 8 | 7 | **78,2** |

## Motivazioni, condizioni e obiezioni

### P-A · Motore Agent SDK con autonomia a livelli

Ha i tetti più alti verso l'esterno e la scala più corta: 5 sì portano a L2, 15 finestre a L3, e il primo follow-up alla persona appena incontrata può arrivare a L3, come nella trascrizione di riferimento [verificato: P-A §3.1-3.2; TR 4:42-5:07]. Le sei protezioni essenziali ci sono tutte. Lo spec scende da 27 a 18 criteri: escono FIDO2 sulle carte, firme con numero monouso, registro a catena e revisione esterna obbligatoria; restano l'esecuzione una volta sola e l'esito incerto a una persona [verificato: P-A §4.3, §7.1-7.2; SPEC §4.7-4.9]. Perde sul tempo: alla settimana 8 i to-do restano nel riassunto e il CRM non c'è; la fase 1 sale da 22,5 a 24-25,5 gp, e già la v2.1 con la riserva finisce a metà della settimana 9 [verificato: P-A §5.1-5.2; R36 §7.2]. Motore, bacheca e lettore degli eventi sono codice nostro ancora da scrivere, quindi l'affidabilità del lavoro autonomo è da dimostrare [verificato: SPEC §12.2; non verificato: giudizio mio]. L'uscita verso Hermes ha già un prezzo, 26-33 gp [verificato: P §15].

**Condizioni perché funzioni**

- Parere legale entro la settimana 3 sul follow-up a L2 e L3 e sul testo della riga AI; se dice no, la classe resta a L1 [verificato: P §9.4; R16 §3, proposta di quel rapporto].
- Portare nella fase 1 l'esecutore Jira (1,75 gp), oppure accettare che alla settimana 8 i to-do restino nel riassunto [verificato: R36 §7.3].
- Tenere un solo elemento esterno per giro, la corsia senza strumenti per il testo di terzi, il tetto giornaliero per classe e il riepilogo del giorno con il tasto «sbagliato»: sono le difese che reggono L3 [verificato: P-A §3.2, §4.1, §7.1; SPEC §4.4].
- Proporre le promozioni dentro il debrief, così il tocco del responsabile non diventa una coda [non verificato: proposta mia].
- Due sì di Michele: Postiz prima della F4 (altrimenti Metricool) e riaccensione automatica del server prima del primo L3 esterno 24 ore su 24 [verificato: P §6.2, §13; DOM n. 22; P-A §2.1].
- Versione dell'SDK fissata e prove prima di ogni aggiornamento [verificato: P §13].

**Obiezioni più forti**

- Alla settimana 8 dà meno delle altre tre: sono L3 solo riassunto, registro e debrief [verificato: P-A §5.1].
- Scrive un lettore degli eventi dentro il motore che n8n sostituisce nella fase 2: circa 1 gp a perdere [verificato: P-A §2.1, §5.2].
- Il motore resta codice su misura, conosciuto da poche persone, su un SDK che cambia quasi ogni giorno [verificato: P §13; R36 §2.1].
- Con 11 lead, 1 risposta e 0 meeting al 5/10, anche le soglie basse arrivano tardi: subito è autonomo solo il lavoro interno [verificato: P §7.1; P-A §3.5].
- Il server non si alleggerisce: 70-74 GB a regime, e con Andrea nella fase 3 il margine scende a circa -9 GB [verificato: P-A §2.2, stima di P-A; R36 §4.2].
- Una lamentela scritta in modo ambiguo può sfuggire: la retrocessione automatica non è garantita [verificato: P-A §3.5].

### P-B · Orchestratore autonomo pronto, con il nostro Cancello

È la più fedele alla trascrizione di riferimento: un orchestratore open source su macchina propria, con bacheca, cron e skill che l'agente scrive da solo, pronti senza scrivere codice [verificato: TR 3:23-3:59; R27 §9.2, §9.5]. Le protezioni essenziali stanno nel Cancello e lo spec scende a 16 criteri, senza sicurezza in eccesso [verificato: P-B §4.1-4.2, §7]. Il voto basso viene dall'affidabilità del lavoro autonomo. Delle quattro condizioni che l'ADR-0012 chiede per usare Hermes come orchestratore, oggi ne vale una; la scheda del gateway conta 312 problemi, 228 senza correzione [verificato: ADR-0012; R27 §11; non verificato da me: stato al 9/11, dal Rapporto 4 §3.2-3.4 e dal controllo di P-B]. Un utente racconta chat di bot diversi che si mescolano più volte [non verificato: testimonianza di terzi, «Grokbot vs Hermes»]. Rifare sull'SDK ciò che Hermes dà pronto vale circa 10-16 gp una volta; tenere aggiornato Hermes ne chiede 1,5-2,5 al mese [verificato: R27 §9.2 e §8, stime di quel rapporto; somma mia].

**Condizioni perché funzioni**

- Superare il criterio 1 della verifica: due settimane con almeno 5 profili e due ingressi automatici, senza messaggi, risultati o card finiti al posto sbagliato. Se fallisce, si passa al motore sull'SDK: 17,5-21 gp, 3-4 settimane [verificato: P-B §5.4; R34-2 §10.2].
- Provare prima dello sviluppo lo sblocco della card quando arriva l'esito della carta: regge tutto il percorso L1 e oggi non è verificato [verificato: R34-2 §5.4 punto 6; P-B §2.2].
- Tenere le trascrizioni fuori dalle sessioni di Hermes sullo stage, con un riassunto a schema fatto prima, finché vale «solo verde e giallo» [verificato: R34-2 §10.3; R27 §2.2; P §11].
- Avere n8n sullo stage già nella fase 1, o usare il cron di Hermes come ripiego: il board porta n8n più avanti [verificato: ADR-0011 «Rischi»; non verificato: P-B non lo dice].
- Il sì di Michele, che preferisce evitare Hermes e deve reggere le patch entro 14 giorni con rilasci frequenti e note incomplete [verificato: R36 §1.2; DOM «Già recepito»; R27 §7.2, §8].
- Controllare nel traffico che non partano chiamate verso il fornitore di Hermes [verificato: R27 §2.1, dove è segnato come non verificato].

**Obiezioni più forti**

- Un solo bot per gateway toglie MSG-43, ma più profili nello stesso gateway lasciano aperti GW-41 e KB-10: un turno può girare con la cartella o i segreti di un altro profilo [verificato: R27 §6.2; R34-2 §3.3].
- Il guasto tipico è un testo con il contesto sbagliato che parte a L3. La regola «subito a L1» scatta dopo, quando il messaggio è già uscito [verificato: P-B §3.1, §8].
- Rovescia ADR-0001 e ADR-0012 senza che le condizioni scritte lì siano cambiate [verificato: ADR-0012; P-B §7].
- Nel board Hermes duplica n8n e LiteLLM su orari, webhook e budget [verificato: R27 §9.3].
- È la proposta che pesa di più su server e persone: 71-79 GB a regime, tre contenitori più lo stage, due linguaggi, nessuno che conosca Hermes a fondo [verificato: P-B §2.4, stima di P-B; R34-2 §10.1].
- Andrea resta alle settimane 41-48 e il primo follow-up a un cliente nuovo resta a L2 [verificato: P-B §3.2, §3.7].
- L'identità vale per contenitore, non per persona: coaching e dati personali reggono solo su una consegna 1:1 fatta dal Cancello [verificato: R27 §4; P-B §3.8].

### P-C · Ibrido: agenti autonomi in abbonamento dove rendono di più

Dà autonomia prima di tutte sul lavoro a dati verdi: ricerca, bandi, bozze e numeri del lunedì partono da soli dalle settimane 1-2, con i compiti programmati già nel bundle [verificato: P-C §5.1; R34-3 §2]. Il nucleo sul server è quello di P-A, con una scala corta (5 e 10). Con la mia lente perde per tre motivi. Apre un sistema che doveva restare chiuso: un ponte pubblico e agenti nel cloud di terzi, che obbligano ad aggiungere due criteri di sicurezza nuovi [verificato: P-C §2.2, §7.3]. Lo stop e il registro sono deboli proprio lì: Grok Bot non si comanda da programma e tiene solo gli ultimi 20 esiti; la sospensione di Managed Agents va ancora provata [verificato: R11 §2.6, §6; P-C §4.1]. Costa di più ogni mese e lascia lo spec quasi intero: restano 24 criteri su 27, più 6 nuovi [verificato: P-C §6.1, §7.2-7.3].

**Condizioni perché funzioni**

- Una decisione di Michele e dei CEO che ammetta Managed Agents e i compiti programmati per i soli dati verdi: oggi sono esclusi [verificato: R26 §1.2; ADR-0011].
- Provare che lo stop revoca i token del ponte e sospende le esecuzioni programmate; i compiti programmati li spegne il proprietario dell'organizzazione [verificato: P-C §4.1; R34-3 §11].
- Connettori in sola lettura e nessun connettore di posta o CRM negli abbonamenti: una scrittura salterebbe il Cancello [verificato: ADR-0011].
- Mettere nel parere i trasferimenti verso gli USA per i due fornitori nuovi; il testo del DPA di Grok Bot non è stato aperto [verificato: P-C §4.3 punto 6; R11 §1].
- Tenere Grok Bot fuori dalla base: la quota settimanale non è pubblicata e, quando finisce, i bot si fermano [verificato: R11 §4.1; non verificato: testimonianza di terzi, «Grokbot vs Hermes»].
- Anticipare i 3,5 gp dell'MCP di SersanOutreach solo se la fase 1 ha margine [verificato: R36 §7.3].

**Obiezioni più forti**

- Il server regge da solo tutti gli agenti: la differenza è di circa 6 GB a regime. L'abbonamento non serve per capacità [verificato: P-C §2.4, stima di P-C; P §6.3].
- Lo stesso anticipo sul lavoro verde si ottiene con n8n sullo stage, senza fornitori nuovi [non verificato: confronto mio con P-D §5.1].
- Tre ambienti per gli agenti (motore, Managed Agents, compiti programmati), più Grok Bot se scelto: più posti dove un lavoro può fermarsi, per quattro persone [verificato: P-C §2.2].
- Managed Agents è in beta, con dati negli USA e senza conservazione zero; i compiti programmati sono in anteprima e agiscono a nome di una persona [verificato: R12 §1; ADR-0011; non verificato da me: Rapporto 4 §2.1].
- Costa di più ogni mese: Managed Agents 13-35 € nella fase 2, Metricool 59,86 € per sempre, Grok Bot 54-205 € se scelto; a fine bundle i compiti programmati consumano l'uso dei posti [verificato: P-C §6.1, stime di P-C; R36 §12; R34-3 §10.1].
- Il colore verde dipende dalle persone: basta un dato incollato a mano per portare un contatto fuori dal server [verificato: P-C §8].

### P-D · Automazione prima: n8n con passi AI e pochi agenti

È la più affidabile per costruzione: il codice sceglie passi e destinatari, il modello scrive senza strumenti e ogni passo ha la sua chiave d'idempotenza. Il giudice di sicurezza del secondo giro chiamava la chiamata a schema senza strumenti il disegno più robusto contro le iniezioni [verificato: R35-sic §3.2; P-D §2.1, §4.1]. Le protezioni essenziali ci sono tutte e non frenano il lavoro interno. Alla settimana 8 dà il quadro più concreto, perché nella fase 1 non c'è un motore da scrivere: riassunto, registro, to-do in Jira, debrief ed evento in calendario a L3 [verificato: P-D §5.1, §5.4]. I 20 gp della fase 1 mi sembrano ottimisti di 2-3 gp: restano comunque vicini ai 22,5 della v2.1 [non verificato: conto mio su R36 §7.3]. Usa meno RAM, 60-64 GB a regime contro 70-74 [verificato: P-D §2.3, stima di P-D; P §6.3]. Perde sull'autonomia: impara meno delle altre, ha la scala più lenta (ombra, poi 10 sì e 20 invii) e tiene il primo follow-up a L2 [verificato: P-D §3.2-3.4].

**Condizioni perché funzioni**

- Prendere da P-A la scala (5 sì per L2, 15 finestre per L3), il tetto L3 per il primo follow-up dopo il parere e le skill con valutazione automatica già dalle fasi 2-3 [verificato: P-A §3.1-3.2, §3.4 flusso 9].
- Michele ammette n8n sullo stage nella fase 1: nel board n8n arriva più avanti [verificato: P-D §6.4; ADR-0011 «Rischi»].
- I flussi che leggono testo rosso non salvano le esecuzioni e non attraversano un Wait; la verifica della settimana 8 controlla anche il database di n8n [verificato: P-D §4.4, §5.5].
- Carte e «Ferma» passano dalla Porta, non dal nodo Teams di n8n, che registra quando si risponde ma non chi [verificato: R28 §2.4; ADR-0011 «Negative»].
- Un flusso per figura, con nome e responsabile nel registro, e i flussi in git: è ciò che evita il declassamento e tiene gestibili 35-40 flussi [verificato: R36 §5.2; P-D §8].
- Tenere pronto dalla fase 2 il runner sottile, per i casi che non entrano in un flusso [verificato: P-D §2.2, §8].
- Decidere ora se il sistema si rivenderà: la licenza di n8n lo vieta, mentre il PRD dice che non è un prodotto da vendere [verificato: ADR-0011 «Negative»; P §2.3; PRD «Utenti»].

**Obiezioni più forti**

- È la meno fedele al meccanismo della trascrizione di riferimento: lì gli agenti imparano da soli e si parlano in una chat; qui 35-40 figure sono flussi fissi [verificato: TR 3:55-4:30; P-D §9; non verificato: conteggio di P-D].
- Nel secondo giro i flussi fissi contavano come declassamento [verificato: R36 §1.3; R35-vis riga 22].
- Con i volumi di oggi, 10 sì senza modifiche in 30 giorni non arrivano [verificato: P §7.1; non verificato: calcolo mio].
- Fa cadere la regola per cui la logica non dipende da n8n; uscirne costa circa 1 gp a flusso [verificato: ADR-0011 «Decisione»; non verificato: stima di P-D §8].
- Senza lo storico delle esecuzioni, un post-call fallito si indaga peggio [non verificato: deduzione mia da P-D §4.4].
- n8n diventa il punto critico: una vulnerabilità grave nel 2026 e una versione 3.0 che cambia l'API [non verificato: fonti di terzi in ADR-0011; Rapporto 4 §5].
- Lo spec si accorcia meno che in P-A e P-B: restano 19 criteri su 27, più 9 nuovi [verificato: P-D §7.3-7.4; conto mio].

## Raccomandazione

Con i pesi fissati i totali su 100 sono: P-D 78,25; P-A 77,0; P-C 71,5; P-B 70,0 [non verificato: calcolo mio sui voti sopra]. P-D e P-A sono a poco più di un punto: raccomando la loro unione, non una delle due da sola.

1. Il Cancello a livelli va fatto comunque. Tutte e quattro le proposte lo chiedono: livello per classe d'azione, finestra L2 con «Ferma», annulla e rettifica, riga AI, retrocessione automatica, niente FIDO2 sulle carte, revisione esterna facoltativa [verificato: P-A §4, P-B §4, P-C §4, P-D §4].
2. Per eseguire parto da P-D. Nelle fasi 0-1 i tre agenti del pilota riassumono, estraggono e scrivono: bastano flussi n8n con passi AI senza strumenti. Il runner sottile sull'SDK arriva nella fase 2, per le figure che ragionano a più passi [verificato: PRD «Perimetro»; R36 §5.2; P-D §2.2].
3. Da P-A prendo il modello di autonomia: soglie 5 e 15, primo follow-up fino a L3 dopo il parere, skill interne con valutazione dalle fasi 2-3, stand-up degli agenti. Così si chiude il punto debole di P-D.
4. Hermes resta un pilota in laboratorio su dati verdi (6-8 gp), per misurare le skill che si curano da sole e la bacheca. Diventa orchestratore quando valgono le quattro condizioni dell'ADR-0012: oggi ne vale una [verificato: ADR-0012; R27 §10-11; non verificato da me: stato al 9/11, Rapporto 4 §3.4].
5. Abbonamenti solo dove un pezzo non regge in casa: voce in cloud per Andrea (circa 88 €/mese) e linea di riserva (10-11 €/mese) [verificato: R36 §12; P §14]. I compiti programmati di Claude Team restano per l'uso personale [verificato: ADR-0011].

Cosa si semplifica nello spec della milestone 1 [verificato: SPEC §12.4]. Escono: firme con numero monouso (AC-012); registro a catena con MAC e ancora (AC-016); tre barriere provate una per una (AC-006); codici per consegna e impronta calcolata dalla Porta (parte di AC-001, AC-009 e AC-010); epoche dello stop (parte di AC-015); più runner con possesso e riserve sul tetto del mese (AC-020, parte di AC-021). Restano, perché costano poco ed evitano danni veri: limiti fissi nel codice (AC-007); una sola esecuzione ed esito incerto a una persona (AC-010, AC-025, AC-026); stop dopo il quale nulla riparte da solo (AC-015); segreti oscurati (AC-017); testo di terzi solo come campi (AC-013); tetti per lavoro e per mese. Si aggiungono: finestra L2, L3 dentro i tetti, retrocessione automatica, annulla e rettifica, riga AI, destinatari presi dai dati.

Avvertenze. Giorni, RAM e livelli delle quattro proposte sono stime dei loro autori [non verificato]. I numeri di Hermes al 9/11 non li ho ricontrollati sul web. Non ho modificato file né lasciato processi accesi.

File controllati: C:\Users\alber\sersan-agent-os\PRESENTAZIONE-CEO.md (P); C:\Users\alber\sersan-agent-os\docs\superpowers\specs\2026-11-09-nucleo-motore-cancello-design.md (SPEC); C:\Users\alber\sersan-agent-os\.claude\prds\sersan-agent-os.prd.md (PRD); C:\Users\alber\sersan-agent-os\docs\adr\0011-n8n-orari-integrazioni.md e C:\Users\alber\sersan-agent-os\docs\adr\0012-hermes-uscita.md (ADR); C:\Users\alber\sersan-agent-os\DOMANDE-PER-MICHELE.md (DOM); in C:\Users\alber\sersan-agent-os\ricerca\ i rapporti 10, 11, 12, 16, 18, 26, 27, 28, 30, 31, 34-proposta-2, 34-proposta-3, 35-giudizio-sicurezza (R35-sic), 35-giudizio-visione (R35-vis) e 36; C:\Users\alber\Desktop\tracrizione bot aziendali.txt (TR); le tre trascrizioni di terzi C:\Users\alber\Desktop\Grokbot vs Hermes.txt, C:\Users\alber\Desktop\grokbot transcript.txt e C:\Users\alber\Desktop\claude and grokbot updates.txt.
