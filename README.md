# SerSan Agent OS

> **Aggiornato l'11 novembre 2026 all'architettura v3**, «Cancello a livelli e motore a due corsie» ([ricerca/45](ricerca/45-architettura-v3.md); [ADR da 0020 a 0028](docs/adr/README.md)). Cosa è cambiato:
> - il 10 novembre i CEO hanno approvato il progetto e hanno lasciato al gruppo di progetto le scelte e l'avvio; lo sviluppo è partito lo stesso giorno, e il codice sta in una repo privata dell'organizzazione;
> - ogni azione verso l'esterno ha un livello di autonomia, da L0 a L3, che le dà il Cancello; il motore ha due corsie e un router che sceglie dove far girare ogni lavoro, anche sui posti Claude Team per lo sviluppo in codice;
> - la ricerca arriva al rapporto 49 e le decisioni di architettura sono 28.
>
> **Il 12 novembre 2026** il gruppo di progetto ha fissato le scelte di disegno della milestone 2: la corsia S a giri e la bacheca con i gruppi degli agenti ([ADR-0029](docs/adr/0029-corsia-s-sessioni-a-giri.md); [ADR-0030](docs/adr/0030-bacheca-gruppi-specchi.md)), con le revisioni di cinque ADR; il router entra nella milestone 2. Da quel giorno la ricerca arriva al rapporto 51 e le decisioni di architettura sono 30.

Proposta e documentazione di progetto di SerSan Agent OS, il «secondo cervello» aziendale di SerSan: nove squadre di agenti AI, 57 in tutto, che lavorano con le persone su una memoria aziendale comune. Il motore lo scriviamo noi in TypeScript e gira sul server dell'ufficio di Cagliari. Ha due corsie: catene a schema, dove il codice sceglie passi e destinatari, e sessioni dell'Agent SDK di Claude per gli agenti che ragionano a più passi ([ADR-0021](docs/adr/0021-motore-a-due-corsie.md)). Ogni azione verso l'esterno passa dal Cancello, che le dà un livello: da «una persona approva ogni volta» a «parte da sola dentro regole e tetti» ([ADR-0020](docs/adr/0020-autonomia-a-livelli.md)).

L'idea è di Alberto Tuveri. La proposta, per i CEO Alessandro Serratt e Michele Sanna, è alla versione 2.1 dell'8 novembre 2026. I CEO hanno approvato il progetto il 10 novembre 2026 e lo sviluppo è partito lo stesso giorno, sulle macchine di sviluppo ([ricerca/45, «Decisione del gruppo di progetto»](ricerca/45-architettura-v3.md)). Il codice, con il PRD (il documento dei requisiti), gli spec e i piani di sviluppo, sta in una repo privata dell'organizzazione, `sersan-agent-os-codice`. Questa repo raccoglie la proposta, la ricerca da cui vengono i fatti, la documentazione di progetto e le ADR.

## Da dove partire

1. [docs/01-panoramica.md](docs/01-panoramica.md): il progetto in breve, a che punto siamo, con il rimando alla fonte di ogni fatto.
2. [ricerca/45](ricerca/45-architettura-v3.md): l'architettura v3, la fonte di verità dell'architettura dal 10 novembre 2026. Dove dice una cosa diversa, supera la proposta.
3. [docs/adr/](docs/adr/README.md): le 30 decisioni di architettura, ognuna con il suo stato.
4. [PRESENTAZIONE-CEO.pdf](PRESENTAZIONE-CEO.pdf), anche in [DOCX](PRESENTAZIONE-CEO.docx) e in [Markdown](PRESENTAZIONE-CEO.md): la proposta approvata dai CEO, versione 2.1. Resta la base per costi, fasi e rischi dove la v3 non la cambia.
5. [DOMANDE-PER-MICHELE.md](DOMANDE-PER-MICHELE.md): le 30 domande tecniche ancora aperte.

## Documentazione di progetto

| Documento | Contenuto |
|---|---|
| [Panoramica](docs/01-panoramica.md) | Cos'è il sistema, le nove squadre, le scelte principali, a che punto siamo |
| [Alternative](docs/02-alternative.md) | Le architetture confrontate nei tre giri, del 24 e 25 ottobre e del 9-10 novembre, e perché ha vinto l'unione «Cancello a livelli e motore a due corsie» |
| [Architettura](docs/03-architettura.md) | Schema a livelli, le due corsie del motore, componenti, percorso di un'azione, memoria, reti, infrastruttura, sicurezza |
| [Tech stack](docs/04-tech-stack.md) | Programmi, servizi e modelli per area, versioni, prove da fare prima di costruire |
| [Design](docs/05-design.md) | Le squadre e come si passano il lavoro, livelli e approvazioni dal telefono, regole, cosa resta umano, design dei documenti |
| [Sviluppo](docs/06-sviluppo.md) | Le sette fasi, le sette milestone del PRD, le verifiche delle settimane 8 e 21, i giorni di sviluppo, i rischi |
| [ADR](docs/adr/README.md) | Le schede di decisione, dal motore all'instradamento a più motori |

## Cosa c'è nella repo

| Cartella o file | Contenuto |
|---|---|
| [ricerca/](ricerca/) | I rapporti da cui vengono i fatti. 00 le funzioni dell'idea, voce per voce; 01 SersanOutreach; 05 il marketing. 10-24 il primo giro, con sette proposte di architettura e i giudizi; 25-37 il secondo giro, dentro il board di Michele, fino all'architettura v2 e alle risposte sull'hardware; 38-45 il terzo giro, sull'autonomia; 46-49 le valutazioni fatte dopo; 50-51 le prove per le scelte della milestone 2 (elenco sotto) |
| [allegati/infra/](allegati/infra/) | Il board dell'infrastruttura di Michele e la board del rack |
| [allegati/sersanoutreach/](allegati/sersanoutreach/) | Copie di documenti di SersanOutreach: profilo aziendale, mappa delle capacità, architettura, prontezza, backup, compliance, server MCP. I rimandi ai file di quella repo sono testo, non link |
| [allegati/marketing/](allegati/marketing/) | Il piano marketing di 90 giorni, le direttive dei contenuti, la gestione dei post e il calendario |
| [strumenti/](strumenti/) | `md_to_docx.py`, che trasforma la proposta in DOCX con lo stile SerSan, il modello di stile e il marchio (`marchio.py` e `brand/`) |
| [LEGGIMI.md](LEGGIMI.md) | La guida della cartella di lavoro, con il cambio usato nei rapporti |

**Il terzo giro e le valutazioni dopo**, dal 9 al 12 novembre 2026 ([ricerca/45, «I documenti del giro»](ricerca/45-architettura-v3.md)):

- [38](ricerca/38-autonomia-nella-trascrizione.md): i comportamenti autonomi della trascrizione di riferimento, scritti come requisiti.
- [39](ricerca/39-autonomia-del-disegno-v2.md): quanto lavora da solo il disegno v2, voce per voce, e i suoi 15 colli di bottiglia.
- [40](ricerca/40-alternative-e-autonomia.md): l'autonomia delle alternative dei primi due giri.
- [41](ricerca/41-novita-al-9-novembre.md): le novità uscite dopo il 25 ottobre 2026.
- 42: le quattro proposte del giro: [A, motore a livelli](ricerca/42-proposta-A-motore-a-livelli.md); [B, orchestratore pronto](ricerca/42-proposta-B-orchestratore-pronto.md); [C, ibrido con abbonamenti](ricerca/42-proposta-C-ibrido-abbonamenti.md); [D, automazione prima](ricerca/42-proposta-D-automazione-prima.md).
- 43: i quattro giudizi, con voti e raccomandazioni: [visione](ricerca/43-giudizio-visione.md), [CEO](ricerca/43-giudizio-ceo.md), [CPTO](ricerca/43-giudizio-cpto.md), [essenziale](ricerca/43-giudizio-essenziale.md).
- [44](ricerca/44-verifiche-avversarie.md): le tre verifiche avversarie sulla proposta prima in classifica.
- [45](ricerca/45-architettura-v3.md): la sintesi del giro e la decisione del gruppo di progetto: l'architettura v3.
- [46](ricerca/46-obsidian-come-casa-dei-testi.md): Obsidian e la «casa dei testi», cioè dove vivono i testi che gli agenti leggono e scrivono, a confronto con BookStack.
- [47](ricerca/47-modelli-system-one.md): i modelli «System One», che rispondono a domande chiuse con una probabilità, e il «decisore».
- [48](ricerca/48-modelli-locali-e-gpu.md): i modelli open-weight sul nostro server, la multimodalità e la seconda GPU.
- [49](ricerca/49-instradamento-a-piu-motori.md): l'instradamento a più motori e la corsia T sui posti Claude Team.
- [50](ricerca/50-agent-sdk-e-prova-a-copione.md): l'Agent SDK al 12 novembre e la sua prova con un modello a copione, senza chiave API.
- [51](ricerca/51-modelli-open-weight-sul-computer-di-sviluppo.md): i modelli open-weight sul computer di sviluppo e il decisore che legge la probabilità della prima parola.

## Come sono scritti i documenti

- Ogni fatto porta la sua fonte. Nei rapporti di `ricerca/` c'è l'etichetta `[verificato: fonte]` o `[non verificato]`; nei documenti di `docs/` c'è il link alla sezione della proposta, al rapporto o all'ADR.
- I prezzi sono IVA esclusa, salvo dove è scritto. Il cambio usato è 1 $ = 0,8934 €.
- Dove la v3 cambia la proposta valgono [ricerca/45](ricerca/45-architettura-v3.md) e le ADR; per il resto vale la proposta. I documenti di `docs/` citano la proposta come storia e accanto scrivono la regola di oggi.

## Rigenerare DOCX e PDF della proposta

Dalla cartella principale della repo, con Python, la libreria python-docx e LibreOffice:

```
python -I -X utf8 strumenti/md_to_docx.py strumenti/modello-stile-sersan.docx PRESENTAZIONE-CEO.md PRESENTAZIONE-CEO.docx "SerSan Agent OS · Proposta di progetto · Documento interno" strumenti/brand/sersan-lockup.png
soffice --headless --convert-to pdf PRESENTAZIONE-CEO.docx
```

I dettagli, compreso come rifare il marchio, sono nella [sezione 9 di docs/06](docs/06-sviluppo.md#9-rigenerare-docx-e-pdf-della-proposta).
