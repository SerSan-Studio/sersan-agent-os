# ADR-0018: Accesso da fuori attraverso una macchina Oracle a Milano, con NetBird e Pangolin

**Data**: 2026-11-05 (registrata il 2026-11-09)

**Stato**: accettata (Michele, 2026-11-05)

**Chi decide**: Michele, che ha scelto la macchina; Alessandro e Michele approvano la spesa con la decisione 7 ([proposta §14](../../PRESENTAZIONE-CEO.md)).

## Contesto

Il board di Michele vuole un accesso "zero trust": nessuna porta aperta in ufficio, si entra solo con identità verificata ([SerSan Infra Board](../../allegati/infra/SerSan%20Infra%20Board.md)). Team e amministratori entrano con NetBird, una rete privata cifrata, usando il login di Entra, il sistema di identità di Microsoft 365, e una chiave FIDO2, cioè una chiavetta di sicurezza fisica; i servizi che altri devono raggiungere passano da Pangolin, che li pubblica attraverso un tunnel, e da Traefik, il proxy in casa che smista le richieste ai servizi ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)). Da fuori vanno raggiunti il bot di Teams, i webhook firmati (le chiamate automatiche di servizi come Instantly), le pagine di firma e la ricerca nella memoria per Claude Team, che arriva dai server di Anthropic ([proposta §5.2](../../PRESENTAZIONE-CEO.md); [ricerca/25 §7, N10](../../ricerca/25-board-michele-e-delta.md)). Il nodo pubblico di Pangolin e la gestione di NetBird hanno bisogno di porte raggiungibili da internet: o in ufficio, o su una macchina esterna ([ricerca/25 §7, N10](../../ricerca/25-board-michele-e-delta.md)).

## Decisione

- Una **macchina virtuale Oracle Cloud a Milano** ospita la gestione e il relay di NetBird, il nodo pubblico di Pangolin, Uptime Kuma, che controlla che i servizi rispondano, e ntfy per gli avvisi ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md)). Il relay fa passare il traffico, sempre cifrato, quando due macchine non riescono a collegarsi direttamente ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- In ufficio il connettore di Pangolin apre il tunnel verso Oracle solo con connessioni in uscita: nessuna porta aperta ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)). Da fuori si entra solo da NetBird, attraverso la macchina Oracle ([proposta §6.1](../../PRESENTAZIONE-CEO.md)).
- **Costo**: 0 € sul piano gratuito di Oracle; 6,49 € al mese se servisse un server a pagamento ([proposta §14, decisione 7](../../PRESENTAZIONE-CEO.md)).
- **Proposto a Michele** ([DOMANDE-PER-MICHELE, domande 4 e 6](../../DOMANDE-PER-MICHELE.md)): Pangolin in TLS passthrough, cioè il traffico cifrato attraversa la macchina Oracle senza essere aperto e si apre solo in casa; l'endpoint per Claude Team accetta solo i token Entra di SerSan, e il filtro sugli indirizzi IP di Anthropic è una protezione in più, non un'autenticazione ([ricerca/36 §4.4](../../ricerca/36-architettura-v2.md)).

## Alternative considerate

### Alternativa: IP fisso con porte aperte in ufficio verso la rete EDGE

- **Pro**: nessuna macchina esterna e nessun cloud in più; le porte si aprirebbero solo verso EDGE, la rete separata dei servizi esposti ([ricerca/25 §1 e §7, N10](../../ricerca/25-board-michele-e-delta.md); [ricerca/36 §4.4](../../ricerca/36-architettura-v2.md)).
- **Contro**: porte aperte in ufficio, contro il "nessuna porta aperta" del board; e se cade la fibra gli ingressi si fermano anche con una linea di riserva ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: Michele ha scelto la macchina esterna.

### Alternativa: un server a pagamento (VPS Hetzner)

- **Pro**: stesso disegno, su un server pagato che non rientra nelle regole delle macchine gratuite di Oracle ([ricerca/37 §3](../../ricerca/37-hardware-risposte-michele.md)).
- **Contro**: 6,49 € al mese IVA esclusa ([ricerca/36 §4.4](../../ricerca/36-architettura-v2.md)).
- **Perché no**: a Milano Oracle è gratuita; il server a pagamento resta il ripiego, già nei costi ([proposta §12.1](../../PRESENTAZIONE-CEO.md)).

### Alternativa: NetBird Cloud per la gestione di NetBird

- **Pro**: gratis fino a 5 utenti e 100 macchine, gestito fuori sede ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Contro**: va verificato se il piano gratuito accetta il login con Entra; il nodo pubblico di Pangolin andrebbe comunque ospitato da qualche parte ([ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- **Perché no**: Michele ha messo la gestione di NetBird sulla macchina Oracle, insieme a Pangolin e al monitoraggio ([ricerca/37 §2](../../ricerca/37-hardware-risposte-michele.md)).

## Conseguenze

### Positive

- Nessuna porta aperta in ufficio ([SerSan Infra Board](../../allegati/infra/SerSan%20Infra%20Board.md)).
- L'accesso da fuori funziona anche sulla linea di riserva, pure se quella sta dietro CGNAT, un indirizzo condiviso che non accetta connessioni in entrata, perché il nodo pubblico è fuori sede ([proposta §13](../../PRESENTAZIONE-CEO.md); [ricerca/37 §4, Linea di riserva](../../ricerca/37-hardware-risposte-michele.md)).
- Con un account che ha solo la regione di Milano, macchine e reti restano lì ([ricerca/37 §6, wan-oracle](../../ricerca/37-hardware-risposte-michele.md)).

### Negative

- Bot di Teams, webhook, ricerca nella memoria per Claude Team e accesso da fuori dipendono tutti da questa macchina ([proposta §5.2 e §6.1](../../PRESENTAZIONE-CEO.md)).
- È un servizio cloud in più nel perimetro Cyber Essentials, la certificazione di sicurezza britannica, dove i servizi cloud sono sempre in ambito e l'accesso con un secondo fattore (MFA) è obbligatorio ([DOMANDE-PER-MICHELE, note](../../DOMANDE-PER-MICHELE.md)).

### Rischi

- Oracle si riprende le macchine gratuite che per 7 giorni restano sotto il 20% di CPU, rete e memoria, e NetBird, Pangolin e Uptime Kuma ci restano quasi sempre. Passare l'account a consumo potrebbe evitarlo: lo diceva un'email di Oracle del 2023, la documentazione di oggi no ([DOMANDE-PER-MICHELE, domanda 4](../../DOMANDE-PER-MICHELE.md)).
- Milano ha una sola zona di disponibilità, cioè un solo gruppo di data center: se mancano macchine gratuite non c'è alternativa. La regione di casa si sceglie alla registrazione e non si cambia più ([DOMANDE-PER-MICHELE, domanda 4](../../DOMANDE-PER-MICHELE.md)), e non è confermato che con il piano gratuito si possa scegliere Milano ([ricerca/37 §6, wan-oracle](../../ricerca/37-hardware-risposte-michele.md)).
- Non è verificato che l'accordo di Oracle sul trattamento dei dati copra anche gli account gratuiti ([ricerca/37 §6, wan-oracle](../../ricerca/37-hardware-risposte-michele.md)).
- Resta da decidere se l'IP fisso serve ancora ([DOMANDE-PER-MICHELE, domanda 4](../../DOMANDE-PER-MICHELE.md)).

## Fonti

- [Proposta per i CEO, §5.2, §6.1, §12.1, §13 e §14 (decisione 7)](../../PRESENTAZIONE-CEO.md)
- [ricerca/37 §2, §3, §4 (linea di riserva) e §6 (verifica wan-oracle)](../../ricerca/37-hardware-risposte-michele.md)
- [ricerca/36 §4.4: rete ed esposizione pubblica](../../ricerca/36-architettura-v2.md)
- [ricerca/25 §1 e §7 (N10): il board e le porte pubbliche](../../ricerca/25-board-michele-e-delta.md)
- [SerSan Infra Board: accesso zero trust](../../allegati/infra/SerSan%20Infra%20Board.md)
- [Rack SerSan 12U: multi-sito Cagliari, Oracle e Terra Noa](../../allegati/infra/Rack%20SerSan%2012U.md)
- [DOMANDE-PER-MICHELE: domande 4 e 6, note](../../DOMANDE-PER-MICHELE.md)
