# 20 · Proposta G: ibrido libero, il pezzo migliore per ogni livello

**Per:** Alessandro Serratt e Michele Sanna. **Da:** Alberto Tuveri, architetto G di sette. **Data:** 24/10/2026.
**Fonti:** rapporti 00-18 di questa cartella, tutti presenti. **Etichette:** [verificato: n §x] = fatto del rapporto n, che cita la fonte primaria; [non verificato] = stima mia; gp = giorni-persona.

## 1. L'architettura in una pagina

Nessun prodotto copre da solo la visione di Alberto [verificato: 12 §0]. Per ogni livello si prende il pezzo più forte; i dati restano in due posti nostri, Postgres sul server e Notion, così ogni pezzo si può sostituire senza perdere la memoria.

```
PERSONE (4) ── Claude Team (chat, Claude Code, Cowork)
SLACK PRO, casa comune: #agenti #approvazioni #call-vendita
   #cliente-<x> (Slack Connect), DM del debrief, @Claude (Claude Tag)
      ▲ carte e recap       ▲ DM personali        ▲ avvisi
PAPERCLIP              HERMES ×4             n8n
organigramma, task,    assistente per        webhook firmati: Recall.ai,
budget, approvazioni,  persona (F3)          ElevenLabs, sito, NOTIFY
routine                                      di SersanOutreach → task
      │
LAVORATORI: Agent SDK in container, una chiave API per agente;
            Managed Agents per la ricerca web (sandbox fuori dal server)
      │ solo MCP con token per agente, nessuno strumento d'invio
SersanOutreach (CRM, HITL invii) · Postgres 17 + pgvector · Notion
GPU RTX 4000: embedding, giudice 4B, Whisper, oscuramento
Esterni: Metricool · moda.app · Andrea (ElevenLabs + Twilio)
```

| Livello | Scelta | Perché |
|---|---|---|
| Casa comune | Slack Pro + Claude Tag | Canali col cliente (B1; Slack Connect [non verificato]), app mature; Hermes, Paperclip e Claude Tag ci si collegano [verificato: 10 §4.2; 12 §3; 18 §2.1]. buzz oggi non ha approvazioni funzionanti, freno ai giri né ponte verso Slack [verificato: 17 §0] |
| Controllo | Paperclip (MIT) | Unico con organigramma, budget per agente con stop al 100 %, approvazioni imposte dal runtime, adattatori Claude Code e Hermes [verificato: 12 §3] |
| Flussi fissi | n8n Community | Maturo per webhook e catene deterministiche; uso interno ammesso [verificato: 12 §3] |
| Lavoratori | Agent SDK; Managed Agents; Hermes | Chiave API per l'uso automatico [verificato: 10 §1.5]; web non fidato fuori dal server [verificato: 12 §1]; Hermes è «single-tenant personal agent» e cura le proprie skill [verificato: 10 §1, §4.2] |
| Memoria | Notion + pgvector; Graphiti se serve | Relazionale più vettoriale, come chiede la visione [verificato: 00 A3]; embedding locali [verificato: 13 §7] |
| Riunioni | Recall.ai + Whisper locale | 0,65 $/h, nessun posto, testo subito sul server [verificato: 14 §4]; riserva Fireflies |
| Voce | ElevenLabs + Twilio IT | Già in casa; Hermes e Grok Bot telefonano solo tramite terzi [verificato: 10 §5; 11 §5] |
| Social | Metricool Advanced | MCP già attivo, revisione da Advanced [verificato: 05 §6]; Postiz chiede app LinkedIn e Meta approvate [non verificato: 05 §6] |
| CRM | SersanOutreach | Deal, meeting, eventi, HITL, due MCP [verificato: 01 §5]; HubSpot duplicherebbe |

Grok Bot e Dots restano fuori: computer negli USA, nessuna scelta del modello né dei crediti API, esportazione non documentata (Grok Bot); un agente per persona e niente Pro in UK/UE (Dots) [verificato: 11 §1; 18 §2.2]. Ripetono i posti Claude Team.

**Come si parlano: il post-call.** Recall.ai chiama il webhook firmato di n8n. n8n salva trascrizione e presenti in Postgres, calcola i vettori e apre un task in Paperclip. L'agente (Sonnet 5.5) legge le regole della persona in Notion, la trascrizione come dato non fidato e lo storico di SersanOutreach. Propone recap al cliente, deal aggiornato, bozza di mail, to-do. Paperclip le mette in `#approvazioni`; dopo il sì esegue il codice, non il modello.

## 2. Tabella di copertura

Stati: pronto, da adattare, da costruire, in abbonamento; n.a. = argomento.

| # | Componente | Stato | Fonte |
|---|---|---|---|
| A1 | Recall.ai online; riunioni fisiche registrate col telefono e Whisper; avviso nell'invito | in abbonamento + da adattare | 14 §4; 16 §1.1 |
| A2 | Notion via MCP | pronto | 18 §5 |
| A3 | pgvector, embedding e reranker locali | da costruire | 13 §7 |
| A4 | Paperclip + n8n, Claude via API | da adattare | 12 §3 |
| A5 | Raccolta e pulizia su Haiku o modelli locali, azione su Sonnet/Opus | da costruire | 13 §2.3 |
| A6 | Skill curate da Hermes; PR settimanali sulle skill aziendali | da adattare | 10 §4.2 |
| A7 | `#agenti` come vetrina, bacheca Paperclip come registro, freno nel codice | da adattare | 10 §9 |
| B1 | Recap nel canale Slack Connect del cliente, dopo la carta | da costruire | [non verificato] |
| B2 | `update_deal`, `record_meeting` di SersanOutreach | da adattare | 01 §5.2 |
| B3 | Bozza nella casella del titolare; ai lead nuovi scrive solo SersanOutreach | da costruire | 16 §3 |
| B4 | To-do in Notion | da adattare | 18 §5 |
| B5 | Autonomia per classe dopo 30 giorni senza correzioni | da costruire | 16 §6 |
| C1 | Routine alle 7:00, DM per persona | da costruire | 12 §3 |
| C2 | Bot Recall.ai sul calendario | in abbonamento | 14 §4 |
| C3 | Sonnet 5.5 con le regole della persona | pronto | 14 §1.5 |
| C4 | Dettatura delle app; note vocali Slack → Whisper | pronto + da adattare | 13 §5 |
| C5 | Tabella `meetings` con presenti, esito, pipeline | da costruire | 00 C5 |
| C6 | Pagina Notion «Come lavoro» letta per prima | da adattare | 00 C6 |
| D1 | Pesi per stadio, poi storico di `commercial_events` (oggi 0 vinti/persi) | da costruire | 01 §1.4 |
| D2 | Managed Agent con ricerca web + segnali e aperture da SersanOutreach | da costruire | 01 §5.5 |
| D3 | Ricerca su meeting, mail, deal | da costruire | 12 §6 |
| D4 | moda.app via MCP | in abbonamento | 14 §6 |
| D5 | Opus: catalogo + trascrizione + brief → bozza | da costruire | 14 §1.5 |
| E1-E2 | Fasi e costi (§6-7) | n.a. | — |
| E3 | Budget per agente, chiave per agente, tetto Claude Tag | pronto + da adattare | 12 §1, §3 |
| E4 | Formazione documentata | da costruire | 16 §4 |
| F1 | Job n8n sui log d'attività (suite non nota), solo aggregati, individuali ≤ 21 giorni | da costruire | 16 §1.2 |
| F2 | Intervista in DM | da costruire | — |
| F3-F4 | Mappa, ore, automazioni in classifica (Opus, mensile) | da costruire | 14 §1.5 |
| F5 | Slack e Claude Team per tutti | pronto | 18 §0 |
| G1 | `#call-vendita` dal post-call | da costruire | — |
| G2 | Qualifier GP+BALD esteso alle call | da adattare | 01 §1.1 |
| G3 | Coaching solo al venditore, senza emozioni | da costruire | 16 §1.2 |
| G4 | Al responsabile solo aggregati, fino al parere legale | da costruire (ridotto) | 16 §4 |
| G5 | ElevenLabs + Twilio IT + Haiku; voce sintetica dichiarata; consenso; RPO | in abbonamento | 16 §2 |
| G6 | Esiti valutati ogni settimana; aperture approvate | da costruire | — |
| G7 | Grafana: tempo di richiamo, meeting | da adattare | 01 §2 |
| G8 | `lost_deal_analysis` → agente editoriale | da adattare | 05 §5.6 |
| G9 | Organigramma Paperclip, copia in Notion | pronto | 12 §3 |
| G10, H7, I2 | Risultati, piano, contesto | n.a. | — |
| H1, H5 | `#ai-lab`, template di agente | pronto | — |
| H2, H4, I1 | CEO sulle carte da F1; Alberto ambassador | da costruire (processo) | — |
| H3 | Assessment guidato | da costruire | — |
| H6 | Classifica in `#ai-wins`; premio dei CEO | da costruire | — |
| I3 | Elenco in Notion + classi negate nel codice | da adattare | 05 §5.8 |
| I4 | Agenti marketing con sì umano | da costruire | 05 §5 |

## 3. Cosa gira sul server e cosa in abbonamento

| VM Proxmox | Contenuto | vCPU | RAM |
|---|---|---|---|
| apps-prod | SersanOutreach (tetti 7,4 GiB [verificato: 01 §4.2]), Traefik, cloudflared | 6 | 24 GB |
| agents | Paperclip, n8n, 10-15 lavoratori, 4 Hermes | 8 | 32 GB |
| data | Postgres 17 + pgvector | 4 | 24 GB |
| gpu | llama-server (giudice Qwen3-4B, embedding, reranker), faster-whisper | 4 | 16 GB |
| monitor, stage, pbs | Grafana, copia di prova, backup [verificato: 15 §5.1] | 8 | 20 GB |

- RAM: circa 116 GB su 128 bilanciati; con due CPU, 192 GB con 2 moduli in più (≈ 138 €) [verificato: 15 §2.2].
- GPU: giudice 4B, Whisper turbo ed embedding accesi insieme negli 8 GB [non verificato: 13 §0].
- Disco: 2 SSD con PLP in mirror ZFS, PBS su dischi propri, copia fuori sede; 400-600 GB il primo anno [non verificato].
- CPU: non è il limite, gli agenti aspettano l'API [verificato: 14 §9].

In abbonamento: Claude Team per le persone; crediti API per gli agenti; Claude Tag e Managed Agents a consumo con tetto [verificato: 18 §2.1]; Slack, Notion, Recall.ai, ElevenLabs con Twilio, Metricool e moda.app, dove comprare batte costruire: canali coi clienti, editor per le persone, bot nelle call, numeri italiani, API social approvate.

## 4. SersanOutreach e marketing

**Spostamento** secondo 01 §4.11, con due scelte:
- Cloudflare Tunnel, senza porte aperte; `outreach.sersan.io` resta, l'estensione non si ricostruisce [verificato: 15 §4.3; 01 §4.4].
- Database da Supabase al server: niente 35 ms a richiesta, tetto di 15 connessioni ed esposizione PostgREST; join diretti con la memoria [verificato: 01 §4.7, §6]. Il backup fuori sede `age` diventa obbligatorio [verificato: 01 §3.3]. La VM Azure si spegne dopo una settimana stabile.

**Aggancio.** Prima l'identità firmata in `enforce` e i due MCP in HTTP sulla rete interna, con un token per agente [verificato: 01 §5.10]. Gli agenti leggono con 19 tool e scrivono con 14 operazioni, senza invio né approvazione in blocco [verificato: 01 §5.2]. Gli eventi tornano con un `NOTIFY` su `commercial_events` letto da n8n (da costruire). Gli invii a lead nuovi restano nella coda HITL [verificato: 01 §5.4]; `auto_linkedin` è una scelta di rischio dei CEO [verificato: 01 §6].

**Marketing**, dentro le direttive del 22/10 [verificato: 05 §5]: agente editoriale (temi da call, risposte, deal persi), copy EN/IT con controllo delle regole, metriche (numeri del lunedì da Metricool e SersanOutreach), pubblicazione solo come bozze `draft:true` confermate da una persona [verificato: 05 §5.4]. I profili LinkedIn dei founder restano nativi.

## 5. Controllo e sicurezza

- **Approvazioni.** Nessun agente ha strumenti d'invio: propone, il codice esegue dopo il sì. Tre corsie: HITL di SersanOutreach (mail, LinkedIn), revisione di Metricool (post), carte di Paperclip in `#approvazioni` (resto). La carta mostra testo e destinatario, ricalcola l'impronta al sì e si consuma una volta.
- **Autonomia per gradi.** Bozza → esecuzione dopo carta → regola «Sempre» per una classe, scritta da una persona dopo 30 giorni senza correzioni. Mai senza carta: prima offerta, invio a freddo, numero nuovo, cancellazioni [verificato: 16 §6].
- **Iniezioni.** Mail, trascrizioni e web sono dati non fidati; chi li legge non ha strumenti con effetti; un turno che li contiene va in carta; agenti Slack con `allow_bots: "mentions"` [verificato: 10 §4.1].
- **Freno ai giri.** Nel codice.
- **Isolamento.** VM degli agenti separata dai dati; un container non privilegiato per agente; un Hermes per persona, perché in un canale «all callers are equally trusted» [verificato: 10 §5]; versioni fissate.
- **Audit e stop.** Eventi in sola aggiunta con catena di hash e ancora fuori sede; `/stop` ferma Paperclip, n8n e il kill switch di SersanOutreach [verificato: 01 §5.5].
- **Banca dei token.** Avviso all'80 %, stop al 100 % per agente; chiave per agente nella Console; report mensile.
- **GDPR.** DPA con Anthropic (nessuna regione UE, API conservate 30 giorni), ElevenLabs, Slack, Notion, Recall.ai; DPIA per registrazioni, vendite e voce; audio ≤ 30 giorni, trascrizioni 24 mesi; soppressione unica; oscuramento locale dei dati «solo locali» [verificato: 16 §5-6].
- **AI Act.** Andrea e gli agenti verso esterni si dichiarano AI (art. 50); coaching senza voto individuale, fuori dall'Allegato III 4(b) fino al parere legale; niente emozioni [verificato: 16 §4].

## 6. Piano a fasi

| Fase | Sett. | gp | Contenuto | Alla fine si vede |
|---|---|---|---|---|
| F0 Fondamenta | 1-2 | 8 | Checklist del server [15 §7], Tunnel, PBS fuori sede, Slack, chiavi per agente, registro trattamenti | Ripristino provato; canali Slack |
| F1 Primo valore | 3-5 | 14 | n8n, Recall.ai, pgvector, Paperclip in pilota con 3 agenti, regole Notion | Recap e bozze entro 10 minuti da ogni call; debrief alle 7 |
| F2 Vendite | 6-9 | 17 | SersanOutreach in casa, MCP HTTP, brief, slide, offerta, coaching | Brief prima di ogni meeting; VM Azure spenta |
| F3 Organigramma | 10-12 | 10 | Tutti gli agenti in Paperclip, freno, audit, Claude Tag, Hermes con Alberto | 12-15 agenti con budget; report token |
| F4 Estensioni | 13-16 | 15 | Andrea dopo il parere legale, mappa processi, marketing, G8 | Richiamata in 90 s; mappa in Notion |

Totale 64 gp più 30 % di riserva: circa 83. Primo rilascio utile (F0+F1): 22 gp più riserva, circa 29, cioè 5 settimane con Alberto a 4 giorni e Mattia a 1,5 [non verificato]. Se l'hardware tarda, F1 parte sulla VM Azure [non verificato].

## 7. Costi mensili (EUR, IVA esclusa)

**Formula:** fissi + (ore di bot × 0,65 $ + minuti voce × 0,0445 $ + ore Managed Agents × 0,08 $ + token) × 0,8934 − crediti API (fino a 714,70 €) − Claude Team del bundle (446,70 €). Prezzi da 14 §11 e 18 §7.
**Ipotesi:** minimo tutto in casa, senza voce; consigliato 60 call, Andrea a 250 minuti (oggi 11 lead [verificato: 01 §1.4]), 200 h di Managed Agents; completo 120 call, 3.000 minuti, 1.000 h, outbound pieno, GPU da 24 GB.

| Voce | Minimo | Consigliato | Completo |
|---|---|---|---|
| Claude Tag (tetto) | 0 | 89,34 | 134,01 |
| Slack | 0 | 27,00 | 60,00 |
| Notion × 4 | 35,74 | 35,74 | 71,47 |
| ElevenLabs (0 se il grant copre) | 0 | 19,65 | 267,13 |
| Numeri Twilio IT | 0 | 40,20 | 80,41 |
| Metricool | 17,87 | 59,86 | 59,86 |
| moda.app | 0 | 26,80 | 53,60 |
| Instantly + Apify | 33,59 | 84,52 | 415,70 |
| 1Password, backup, Proxmox | 25,49 | 45,39 | 48,59 |
| Corrente e UPS | 108,83 | 121,60 | 136,48 |
| GPU su 60 mesi | 0 | 0 | 42,58 |
| **Fissi** | **221,52** | **550,10** | **1.369,83** |
| API (coperte dai crediti) | 20,39 | 88,62 | 221,67 |
| Recall.ai | 17,42 | 17,42 | 34,84 |
| Managed Agents | 0 | 14,29 | 71,47 |
| Voce: minuti e LLM | 0 | 10,41 | 146,07 |
| **Cassa oggi** (bundle e crediti) | **≈ 239** | **≈ 592** | **≈ 1.622** |
| Senza crediti | ≈ 259 | ≈ 681 | ≈ 1.844 |
| Senza bundle né crediti | ≈ 706 | ≈ 1.128 | ≈ 2.291 |

Spegnere Azure toglie circa 150 € [non verificato: 14 §9]. Proxy a 0: con l'estensione non serve [verificato: 01 §4.5]. Esclusi suite di posta, Higgsfield, Canva, parere legale. Una tantum: UPS 1.163-1.293 €; GPU 2.555 € solo se le misure la chiedono [verificato: 13 §10].

## 8. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| Molti pezzi per una persona | Versioni fissate, prove di fumo, runbook, Mattia secondo amministratore, un'uscita per pezzo |
| Paperclip giovane, nessun team dichiarato [non verificato: 12 §3] | Pilota di 2 settimane; dati nel nostro Postgres; uscita n8n + tabella task |
| Hermes instabile, CVE [verificato: 10 §3] | Un'istanza per persona, nessun webhook esposto; uscita i posti Claude Team |
| Beta di Claude Tag e Managed Agents | Ruoli non critici, tetti |
| Crediti incerti [verificato: 14 §1.4] | Verifica in Console; costi con e senza crediti |
| Registrazioni, Andrea, vendite, Statuto art. 4 | Parere legale prima di F4; G4 ridotto |
| Un solo server, interruzioni in Sardegna [verificato: 15 §5.3] | UPS, mirror ZFS, PBS fuori sede, ripartenza in cloud |
| Pochi dati (11 lead, 0 vinti) | D1 e G2 partono da regole |
| Doppia chat | Slack unica chat interna; i CEO per primi |

## 9. Perché sceglierla, e perché no

**Sì.** Ogni livello ha il pezzo più forte e nessun fornitore tiene la memoria: CRM, trascrizioni e vettori stanno sul server, le regole in Notion. Usa ciò che SerSan paga già. Copre A1-I4 con limiti dichiarati (G4 ridotto, G5 dopo il legale, D1 senza storico). Primo valore in circa 5 settimane, a circa 590 € al mese finché valgono bundle e crediti.

**No.** È l'opzione con più integrazione: cinque componenti open source e otto servizi da sorvegliare e aggiornare. Dipende da Alberto, e Paperclip e Hermes sono giovani. Chi vuole un solo fornitore e un solo supporto troverà più semplice una soluzione tutta Claude, con meno controllo sui dati.
