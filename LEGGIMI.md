# SerSan Agent OS · cartella del progetto

Proposta di un sistema multi-agente aziendale per SerSan: un "secondo cervello" con nove squadre di agenti, idea di Alberto Tuveri. Preparata da Alberto il 24 ottobre 2026, aggiornata il 25, per Alessandro Serratt e Michele Sanna.

## Da dove partire

1. `PRESENTAZIONE-CEO.pdf` (anche `.docx` e `.md`): il documento da presentare. Inizia con una pagina di sintesi e chiude con le decisioni di budget (sezione 14) e la stima dei giorni di sviluppo (sezione 15).
2. `ricerca/36-architettura-v2.md`: l'architettura scelta il 25 ottobre sul board di Michele (motore sull'Agent SDK di Claude, tutto self-hosted), con il piano e i costi in dettaglio tecnico.
3. `DOMANDE-PER-MICHELE.md`: le domande tecniche sull'infrastruttura, da mandare a Michele.
4. `ricerca/00-visione-funzionalita.md`: la lista completa delle funzioni, voce per voce (A1-L12).

## Cartelle

| Cartella | Contenuto |
|---|---|
| `ricerca/00` | L'idea di Alberto, funzione per funzione (A1-L12) |
| `ricerca/01` | SersanOutreach: stato reale, costi, migrazione sul server, prese per gli agenti |
| `ricerca/05` | Piano marketing e post: dove entrano gli agenti |
| `ricerca/10` | Hermes Agent (Nous Research) al 24/10/2026 |
| `ricerca/11` | Grok Bot (SpaceXAI / Cursor) |
| `ricerca/12` | Altre piattaforme: Anthropic, OpenAI, open source, SaaS, memoria, riunioni, voce |
| `ricerca/13` | Modelli open source sul server (RTX 4000, 160 GB) |
| `ricerca/14` | Listino di costi, abbonamenti e API, con tre scenari |
| `ricerca/15` | Server, rete e messa in produzione (checklist in 10 passi) |
| `ricerca/16` | GDPR, AI Act e regole operative |
| `ricerca/17` | buzz di Block |
| `ricerca/18` | Agenti in abbonamento (Claude, Dots, Grok Bot, Hermes Cloud, voce) |
| `ricerca/20` | Le sette proposte di architettura (A-G) |
| `ricerca/21` | I quattro giudizi (visione, CEO, CPTO, privacy) |
| `ricerca/22` | L'architettura scelta |
| `ricerca/23` | La critica di completezza, recepita nella presentazione |
| `ricerca/24` | I 45 rilievi della revisione finale (numeri, lettura da CEO, copertura), recepiti |
| `ricerca/25` | Secondo giro: la proposta confrontata riga per riga con il board di Michele |
| `ricerca/26-27` | Claude Agent SDK; Hermes Agent tutto sul nostro server |
| `ricerca/28-31` | Chat di gruppo (Teams, Buzz, Slack, Telegram, WhatsApp); conoscenza e task senza Notion; call e trascrizione in casa; voce di Andrea in casa |
| `ricerca/32-33` | Hardware reale, RAM e seconda GPU; costi della versione 2 |
| `ricerca/34-35` | Le tre proposte del secondo giro e i quattro giudizi |
| `ricerca/36` | L'architettura scelta nella versione 2 |
| `ricerca/37` | Le risposte di Michele sull'hardware del 7 novembre e la revisione della versione 2.1 |
| `allegati/infra` | Il board dell'infrastruttura di Michele (HTML, Markdown, testo e VLAN) |
| `allegati/sersanoutreach` | Profilo aziendale, mappa delle capacità, architettura, prontezza, backup, compliance, server MCP |
| `allegati/marketing` | Piano 90 giorni, direttive contenuti, gestione post, calendario |
| `strumenti` | `md_to_docx.py` (Markdown in DOCX con lo stile SerSan), il modello di stile, `marchio.py` e la cartella `brand`: marchio, font Sersan Display del logotipo (licenza OFL) e lockup per copertina e intestazione |

## Rigenerare il documento

```
cd C:\Users\alber\SerSan-AgentOS
python -I -X utf8 strumenti\marchio.py
python -I -X utf8 strumenti\md_to_docx.py strumenti\modello-stile-sersan.docx PRESENTAZIONE-CEO.md PRESENTAZIONE-CEO.docx "SerSan Agent OS · Proposta di progetto · Documento interno" strumenti\brand\sersan-lockup.png
"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf PRESENTAZIONE-CEO.docx
```

## Come sono stati fatti i rapporti

Rilevazioni del 24/10/2026 con agenti di ricerca: lettura dei repo locali (SersanOutreach, SERSAN-marketing) e ricerca web sulle pagine ufficiali. Ogni fatto porta l'etichetta [verificato: fonte] o [non verificato]. Prezzi IVA esclusa, cambio 1 $ = 0,8934 €.