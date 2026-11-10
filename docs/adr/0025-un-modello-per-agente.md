# ADR-0025: Un modello per agente, anche open-weight, tutti dietro LiteLLM

**Data**: 2026-11-10

**Stato**: accettata; resta da chiudere con Michele il confronto fra la GPU da 16 GB e quella da 24 GB

**Chi decide**: il gruppo di progetto, con la carta bianca dei CEO del 10 novembre 2026 ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)). La scheda da comprare e il momento li decide il gruppo di progetto con Michele, a cui resta l'infrastruttura ([ADR-0014](0014-seconda-gpu-blackwell.md)).

## Contesto

- Nella v2 gli agenti ragionavano tutti con Claude via API: Haiku per i lavori semplici, Sonnet per quasi tutto, Opus per offerte e analisi. LiteLLM usciva solo verso Anthropic ([ADR-0004](0004-litellm-banca-token.md)).
- I modelli open-weight sono modelli con i pesi pubblici, che si possono far girare sul proprio server o comprare a consumo da un fornitore. Sul nostro server girano già modelli piccoli nella pipeline di Michele, come Qwen3-4B, gli embedding e il reranker ([ricerca/26 §4.5](../../ricerca/26-claude-agent-sdk.md); [ricerca/13](../../ricerca/13-modelli-open-source-sul-server.md)).
- LiteLLM può mandare anche l'Agent SDK verso altri modelli, ma Anthropic non lo supporta per Claude Code. Con gli 8 GB di VRAM della GPU di oggi nessun modello locale è adatto a usare strumenti in catena e a orchestrare ([ricerca/26 §4.5](../../ricerca/26-claude-agent-sdk.md)).
- La corsia N non dà strumenti al modello: gli chiede solo di scrivere campi a schema ([ADR-0021](0021-motore-a-due-corsie.md)).
- Michele è disposto ad aggiornare l'hardware: la RAM fino a 384 GB e la seconda GPU ([ricerca/45, «Decisione del gruppo di progetto», e §3.3](../../ricerca/45-architettura-v3.md); [ADR-0015](0015-ram-384-gb.md)).

## Decisione

- **Ogni agente dichiara nel registro il suo modello**, scelto fra tre tipi ([ricerca/45, «Decisione del gruppo di progetto»](../../ricerca/45-architettura-v3.md)):
  1. Claude via API;
  2. un modello open-weight servito sul nostro server;
  3. un modello open-weight di un fornitore, via API.
- **Un'unica porta**: tutte le chiamate passano da LiteLLM, con la chiave virtuale dell'agente e i suoi tetti ([ADR-0004](0004-litellm-banca-token.md)). Il motore non chiama mai un modello direttamente.
- **I modelli locali entrano prima nella corsia N**, dove non servono strumenti ([ADR-0021](0021-motore-a-due-corsie.md)).
- **Per le sessioni dell'Agent SDK resta Claude** finché una prova non dimostra che un modello locale regge: stessi scenari di prova, stesso Cancello, e un risultato misurato sugli strumenti in catena ([ricerca/26 §4.5](../../ricerca/26-claude-agent-sdk.md)).
- **I fornitori terzi ricevono solo dati verdi e gialli**, mai rossi ([ADR-0009](0009-dati-tre-colori.md)).
- **Cambiare il modello di un agente** è un cambio di configurazione in git: senza una valutazione, la terna dell'agente torna a L1 ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md); [ADR-0020](0020-autonomia-a-livelli.md)).

**Punto da chiudere con Michele: la seconda GPU, da 16 o da 24 GB.** Sono tutte e due schede della stessa classe da 70 W, senza cavo di alimentazione ([ricerca/32 §4.2](../../ricerca/32-hardware-e-upgrade.md)):

| | RTX PRO 2000 Blackwell | RTX PRO 4000 Blackwell SFF |
|---|---|---|
| Memoria | 16 GB GDDR7 ECC, 128 bit | 24 GB GDDR7 ECC, 192 bit |
| Banda | 288 GB/s | 432 GB/s |
| Formato | 2 slot, 2,7 × 6,6 pollici | 2 slot, mezza altezza |
| Cosa ci gira 24 ore su 24 | trascrizione dal vivo, voce di Andrea, ricerca nella memoria, il modello piccolo della pipeline | tutto questo, più un modello da 8 miliardi di parametri sempre acceso; un 14B accanto al piano audio |
| Velocità stimata su un 8B | circa 36 token/s | circa 54 token/s |
| Prezzo | circa 880-1.220 € IVA esclusa, con riser e staffa se mancano | listino SHI UE 3.032,85 €, senza data: **da verificare** |

Fonti della tabella: [ricerca/32 §4.2, §4.3 e §4.6](../../ricerca/32-hardware-e-upgrade.md) (velocità e piano dei modelli sono stime non verificate); [ADR-0014](0014-seconda-gpu-blackwell.md) per il prezzo della scheda da 16 GB.

- Con la scheda da 16 GB i modelli locali della corsia N restano piccoli, sulla RTX 4000 quando è libera.
- Con la scheda da 24 GB un modello da 8B sta sempre acceso accanto all'audio, e diventa un candidato per molte catene della corsia N [stima].
- Il montaggio nel riser secondario va verificato come per la scheda da 16 GB ([ADR-0014](0014-seconda-gpu-blackwell.md)).

## Alternative considerate

### Alternativa: solo Claude via API, come nella v2

- **Pro**: un solo fornitore, la qualità più alta sugli strumenti, nessun modello da servire ([ADR-0004](0004-litellm-banca-token.md)).
- **Contro**: ogni testo, anche il più ripetitivo, va fuori dal server e si paga a token; i dati rossi vanno oscurati prima ([ADR-0009](0009-dati-tre-colori.md)).
- **Perché no**: la corsia N rende possibile usare modelli più piccoli dove bastano; la scelta resta per agente.

### Alternativa: modelli locali anche nelle sessioni dell'Agent SDK, da subito

- **Pro**: meno spesa in token e nessun dato fuori dal server.
- **Contro**: Anthropic non supporta Claude Code verso altri modelli; con 8 GB nessun modello locale regge gli strumenti in catena ([ricerca/26 §4.5](../../ricerca/26-claude-agent-sdk.md)).
- **Perché no**: prima la prova, poi la scelta.

### Alternativa: ogni agente chiama il suo modello senza LiteLLM

- **Pro**: un passaggio in meno.
- **Contro**: niente budget per agente, segreti sparsi, nessun conto unico ([ADR-0004](0004-litellm-banca-token.md)).
- **Perché no**: la porta unica è la banca dei token.

## Conseguenze

### Positive

- Ogni agente usa il modello che basta al suo lavoro, e la spesa si vede tutta in LiteLLM.
- Un modello sul nostro server non manda testo fuori.

### Negative

- Più modelli da valutare e da tenere aggiornati; ogni cambio di modello passa da una valutazione.
- LiteLLM esce verso più destinazioni: Anthropic, il nostro server e i fornitori scelti ([ADR-0004](0004-litellm-banca-token.md)).
- La scheda da 24 GB costa, a listino, circa il triplo di quella da 16 GB ([ricerca/32 §4.3 e §4.6](../../ricerca/32-hardware-e-upgrade.md)).

### Rischi

- **Un modello locale sbaglia più di Claude** su un compito: la valutazione prima del cambio e la discesa automatica a L1 lo contengono ([ricerca/45 §2.4](../../ricerca/45-architettura-v3.md)).
- **Un fornitore terzo cambia termini o sede dei dati**: riceve solo dati verdi e gialli, e l'agente torna a un altro modello cambiando una riga.
- **Prezzo della scheda da 24 GB**: il listino trovato non ha data; va verificato prima della scelta ([ricerca/32 §4.3](../../ricerca/32-hardware-e-upgrade.md)).

## Fonti

- [ricerca/45, architettura v3: «Decisione del gruppo di progetto», §2.4, §3.3](../../ricerca/45-architettura-v3.md)
- [ricerca/26, Agent SDK, §4.5](../../ricerca/26-claude-agent-sdk.md)
- [ricerca/13, modelli open source sul server](../../ricerca/13-modelli-open-source-sul-server.md)
- [ricerca/32, hardware e upgrade, §4.2, §4.3 e §4.6](../../ricerca/32-hardware-e-upgrade.md)
- [ADR-0004](0004-litellm-banca-token.md), rivista da questa ADR; [ADR-0009](0009-dati-tre-colori.md); [ADR-0014](0014-seconda-gpu-blackwell.md), rivista da questa ADR; [ADR-0015](0015-ram-384-gb.md); [ADR-0020](0020-autonomia-a-livelli.md); [ADR-0021](0021-motore-a-due-corsie.md)
