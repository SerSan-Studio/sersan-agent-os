# ADR-0004: LiteLLM come banca dei token e unico accesso ai modelli

**Data**: 2026-10-25 (registrata il 2026-11-09)

**Stato**: accettata; rivista il 2026-11-10 da [ADR-0020](0020-autonomia-a-livelli.md) e [ADR-0025](0025-un-modello-per-agente.md): tetti per classe al giorno e un modello per agente; rivista il 2026-11-11 da [ADR-0028](0028-instradamento-a-piu-motori.md): Jev passa da LiteLLM, la corsia T no

**Chi decide**: Michele Sanna (CPTO), perché LiteLLM è nel suo board, nella fase F4 ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)); i CEO per il tetto mensile delle API e il credito prepagato, se i crediti non bastano ([proposta §14, decisione 3](../../PRESENTAZIONE-CEO.md)).

## Contesto

Gli agenti ragionano con Claude via API: Haiku per i lavori semplici, Sonnet per quasi tutto, Opus per offerte e analisi ([proposta §5.1](../../PRESENTAZIONE-CEO.md)). L'idea chiede una banca dei token, cioè budget per persona e per agente con tetti che fermano davvero; i token sono le unità di testo con cui si pagano i modelli ([proposta §2.4](../../PRESENTAZIONE-CEO.md)). LiteLLM è un proxy, un servizio intermedio, che dà chiavi virtuali al posto di quella vera e mette budget su chiave, squadra e utente ([ricerca/26 §4.1 e §4.3](../../ricerca/26-claude-agent-sdk.md)). Il board di Michele mette le API di Anthropic "dietro LiteLLM", con i budget nella fase F4 ([ricerca/25 §1](../../ricerca/25-board-michele-e-delta.md)).

## Decisione

Ogni chiamata ai modelli passa da LiteLLM, sul nostro server ([proposta §5.1](../../PRESENTAZIONE-CEO.md)).

- **Chiavi**: una chiave virtuale per agente, mai la chiave di Anthropic; un team LiteLLM per squadra, un utente per persona ([ricerca/26 §4.1 e §4.3](../../ricerca/26-claude-agent-sdk.md); [proposta, appendice A, J2](../../PRESENTAZIONE-CEO.md)).
- **Tetti**: per agente, per catena di lavoro e per persona; avviso all'80%, stop al 100%, rendiconto mensile ([proposta §4.8](../../PRESENTAZIONE-CEO.md)). LiteLLM riserva il costo massimo prima della richiesta e la rifiuta se sfora il budget ([ricerca/26 §4.3](../../ricerca/26-claude-agent-sdk.md)).
- **Una sola uscita**: LiteLLM esce solo verso Anthropic ([proposta §13](../../PRESENTAZIONE-CEO.md)); gli agenti usano la chiave API, mai i posti di Claude Team ([ricerca/26 §5.2](../../ricerca/26-claude-agent-sdk.md)).
- **Conto vero**: ogni mese i conti di LiteLLM si confrontano con la Console di Anthropic, il pannello dell'account API con i consumi veri, perché i costi dell'SDK sono stime ([ricerca/26 §2 e §4.3](../../ricerca/26-claude-agent-sdk.md)).
- **Tempi**: chiave API limitata nel pilota, settimane 5-8; banca dei token alla fine della fase 2; budget per persona nella fase 4 ([proposta §11](../../PRESENTAZIONE-CEO.md)).

## Alternative considerate

### Alternativa: una chiave API diretta per ogni gruppo di agenti, con i limiti della Console

- **Pro**: costa 0 € e funziona prima che arrivi LiteLLM: è la strada del pilota ([ricerca/36 §4.5 e §12](../../ricerca/36-architettura-v2.md)).
- **Contro**: niente budget per persona ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)); in produzione moltiplica i segreti fuori da LiteLLM ([ricerca/35, giudizio di sicurezza §8](../../ricerca/35-giudizio-sicurezza.md)).
- **Perché no**: resta sul banco di prova e come uscita temporanea, se LiteLLM non regge ([ricerca/36 §12](../../ricerca/36-architettura-v2.md)).

### Alternativa: solo i tetti dell'Agent SDK

- **Pro**: sono già pronti: un tetto di turni e uno di dollari per ogni lavoro ([ricerca/26 §2](../../ricerca/26-claude-agent-sdk.md)).
- **Contro**: sono stime del client, non la fattura, e la spesa può superare il tetto con l'ultima risposta ([ricerca/26 §2](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: restano come secondo freno; il tetto per agente lo tiene LiteLLM ([ricerca/26 §2](../../ricerca/26-claude-agent-sdk.md)).

### Alternativa: posti Claude Team o gateway di Anthropic per gli agenti

- **Pro**: i cinque posti ci sono già, gratis il primo anno grazie al bundle startup ([proposta §1](../../PRESENTAZIONE-CEO.md)).
- **Contro**: per le regole di Anthropic chi costruisce servizi usa una chiave della Console, non i posti degli abbonamenti ([ricerca/26 §5.1](../../ricerca/26-claude-agent-sdk.md)); il gateway di Anthropic accetta solo un login dal browser, e un agente senza una persona davanti non si autentica ([ricerca/26 §4.4](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: i posti restano alle persone e il gateway non serve agli agenti: per loro resta LiteLLM, come nel board ([ricerca/26 §4.4 e §5.2](../../ricerca/26-claude-agent-sdk.md)).

## Conseguenze

### Positive

- Un solo punto dove si vedono e si fermano le spese, con tetti diversi per persona: più alto, per esempio, per l'ambassador interno ([proposta §2.4 e §10](../../PRESENTAZIONE-CEO.md)).
- Licenza a zero ([ricerca/33 §2.6](../../ricerca/33-costi-v2.md)); gli agenti non consumano i posti di Claude Team, quindi a fine bundle ne bastano meno premium ([proposta §14, decisione 16](../../PRESENTAZIONE-CEO.md)).

### Negative

- LiteLLM diventa un bene critico: custodisce la chiave di Anthropic e tutte le chiavi virtuali ([ricerca/36 §5.7](../../ricerca/36-architettura-v2.md)).
- Arriva con la fase F4 del board, o prima se Michele anticipa il posto per gli agenti ([proposta, appendice A, E3](../../PRESENTAZIONE-CEO.md)); fino ad allora il pilota usa una chiave API limitata, con il tetto di spesa nella Console ([proposta §11](../../PRESENTAZIONE-CEO.md); [ricerca/36 §7.1](../../ricerca/36-architettura-v2.md)).

### Rischi

- **Catena di fornitura**, cioè i pacchetti presi da fuori: a marzo 2026 sono circolate versioni compromesse di LiteLLM. Le difese: versione fissata, uscita solo verso Anthropic, pannello solo dalla rete di gestione, chiave principale con rotazione ([proposta §13](../../PRESENTAZIONE-CEO.md)).
- **Intestazioni di Anthropic**: LiteLLM deve inoltrare intatte `anthropic-beta` e `anthropic-version`, dove viaggiano le funzioni nuove; la correzione (PR #36736) era aperta al 25 ottobre. Prova nella fase 0 ([ricerca/26 §4.2](../../ricerca/26-claude-agent-sdk.md); [proposta §11](../../PRESENTAZIONE-CEO.md)).
- **Crediti finiti**: importo e scadenza dei crediti del bundle si verificano nella prima settimana; senza crediti le API costerebbero circa 196 € al mese (forbice 90-250), con un tetto a 250 € e un credito prepagato di 0-223 € ([proposta §1, §12.1 e §14, decisione 3](../../PRESENTAZIONE-CEO.md)).

## Revisione del 10 novembre 2026

- Ai budget di LiteLLM si aggiunge il **tetto per classe al giorno**, che conta il Cancello: per esempio 15 follow-up e 10 inviti per agente, al massimo 2 messaggi per destinatario ([ADR-0020](0020-autonomia-a-livelli.md); [ricerca/45 §2.7](../../ricerca/45-architettura-v3.md)).
- Ogni agente dichiara il suo modello: Claude via API, un modello open-weight sul nostro server o un modello open-weight di un fornitore. LiteLLM resta **l'unica porta** verso tutti, quindi non esce più solo verso Anthropic. I fornitori terzi ricevono solo dati verdi e gialli ([ADR-0025](0025-un-modello-per-agente.md)).
- LiteLLM entra davanti alle chiamate della corsia N già nella milestone 2, con un budget per catena ([ricerca/45 §12.2](../../ricerca/45-architettura-v3.md)).
- Sul banco di prova si usa una chiave per flusso con il limite della Console; se il limite per area di lavoro non c'è, il contatore sta nel Cancello ([ricerca/45 §2.7](../../ricerca/45-architettura-v3.md)).

## Revisione dell'11 novembre 2026

- LiteLLM resta l'unica porta verso i modelli delle corsie N e S e del decisore. Jev si chiama da LiteLLM con il passaggio `/typesafe` o con `/v1/systemone`, con una chiave virtuale e i modelli ammessi ([ricerca/49 §1.4](../../ricerca/49-instradamento-a-piu-motori.md)).
- **La corsia T non passa da LiteLLM**: le sessioni di Claude Code sui posti Team chiamano il modello dall'infrastruttura di Anthropic e consumano l'uso del posto, non la chiave API. Il loro conto lo tiene il motore, per posto: avvii, lavori aperti, consegne mancate ([ADR-0028](0028-instradamento-a-piu-motori.md)).
- Il piano Team include fino a 500 $ al mese di crediti API, validi per l'API e l'Agent SDK. Se il nostro piano ne ha diritto, l'organizzazione della Console collegata è quella della chiave dietro LiteLLM ([ricerca/49 §1.3](../../ricerca/49-instradamento-a-piu-motori.md)).

## Fonti

- [Proposta per i CEO, §1, §2.4, §4.8, §5.1, §10, §11, §12.1, §13, §14 e appendice A](../../PRESENTAZIONE-CEO.md)
- [ricerca/25, il board di Michele, §1](../../ricerca/25-board-michele-e-delta.md)
- [ricerca/26, Agent SDK, §2, §4.1-4.4, §5.1 e §5.2](../../ricerca/26-claude-agent-sdk.md)
- [ricerca/33, costi v2, §2.6](../../ricerca/33-costi-v2.md)
- [ricerca/35, giudizio di sicurezza §8](../../ricerca/35-giudizio-sicurezza.md)
- [ricerca/36, architettura v2, §4.5, §5.7, §7.1 e §12](../../ricerca/36-architettura-v2.md)
