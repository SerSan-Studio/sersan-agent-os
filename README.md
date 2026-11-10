# SerSan Agent OS

> **Aggiornamento del 10 novembre 2026.** I CEO hanno approvato il progetto e lo sviluppo è partito; il codice sta in una repo privata dell'organizzazione. Le decisioni nuove sono in [ricerca/45](ricerca/45-architettura-v3.md) e nelle [ADR da 0020 a 0027](docs/adr/README.md). Questo README e i documenti in `docs/` descrivono ancora la versione 2 e sono in corso di allineamento: dove dicono cose diverse dalle ADR, valgono le ADR.

Proposta e documentazione di progetto di SerSan Agent OS, il «secondo cervello» aziendale di SerSan: nove squadre di agenti AI, 57 in tutto, che lavorano con le persone su una memoria aziendale comune. Il motore lo scriviamo noi sull'Agent SDK di Claude e gira sul server dell'ufficio di Cagliari. Nessun agente manda qualcosa a un cliente senza il sì di una persona o una regola «Sempre» decisa dai CEO.

L'idea è di Alberto Tuveri. La proposta è per i CEO Alessandro Serratt e Michele Sanna ed è alla versione 2.1, dell'8 novembre 2026. Il codice del motore non c'è ancora: questa repo raccoglie la proposta, la ricerca da cui vengono i fatti e la documentazione di progetto.

## Da dove partire

1. [PRESENTAZIONE-CEO.pdf](PRESENTAZIONE-CEO.pdf), anche in [DOCX](PRESENTAZIONE-CEO.docx) e in [Markdown](PRESENTAZIONE-CEO.md): la proposta per i CEO. È la fonte di verità per costi, fasi, decisioni e rischi.
2. [docs/01-panoramica.md](docs/01-panoramica.md): il progetto in breve, con il rimando alla fonte di ogni fatto.
3. [docs/adr/](docs/adr/README.md): le 19 decisioni di architettura, ognuna con il suo stato.
4. [DOMANDE-PER-MICHELE.md](DOMANDE-PER-MICHELE.md): le 30 domande tecniche ancora aperte.

## Documentazione di progetto

| Documento | Contenuto |
|---|---|
| [Panoramica](docs/01-panoramica.md) | Cos'è il sistema, le nove squadre, le scelte principali, a che punto siamo |
| [Alternative](docs/02-alternative.md) | Le architetture confrontate nei due giri del 24 e 25 ottobre e perché ha vinto il motore sull'Agent SDK |
| [Architettura](docs/03-architettura.md) | Schema a livelli, componenti, percorso di un'azione, memoria, reti, infrastruttura, sicurezza |
| [Tech stack](docs/04-tech-stack.md) | Programmi e servizi per area, versioni, prove da fare prima di costruire |
| [Design](docs/05-design.md) | Le squadre e come lavorano insieme, approvazioni dal telefono, regole, cosa resta umano, design dei documenti |
| [Sviluppo](docs/06-sviluppo.md) | Le sette fasi, le verifiche delle settimane 8 e 21, i giorni di sviluppo, i rischi, le decisioni chieste ai CEO |
| [ADR](docs/adr/README.md) | Le schede di decisione, dal motore alla linea internet di riserva |

## Cosa c'è nella repo

| Cartella o file | Contenuto |
|---|---|
| [ricerca/](ricerca/) | I rapporti da cui vengono i fatti. 00 le funzioni dell'idea, voce per voce; 01 SersanOutreach; 05 il marketing. 10-24 il primo giro, con sette proposte di architettura e i giudizi; 25-37 il secondo giro, dentro il board di Michele, fino all'architettura v2 e alle risposte sull'hardware |
| [allegati/infra/](allegati/infra/) | Il board dell'infrastruttura di Michele e la board del rack |
| [allegati/sersanoutreach/](allegati/sersanoutreach/) | Copie di documenti di SersanOutreach: profilo aziendale, mappa delle capacità, architettura, prontezza, backup, compliance, server MCP. I rimandi ai file di quella repo sono testo, non link |
| [allegati/marketing/](allegati/marketing/) | Il piano marketing di 90 giorni, le direttive dei contenuti, la gestione dei post e il calendario |
| [strumenti/](strumenti/) | `md_to_docx.py`, che trasforma la proposta in DOCX con lo stile SerSan, il modello di stile e il marchio (`marchio.py` e `brand/`) |
| [LEGGIMI.md](LEGGIMI.md) | La guida della cartella di lavoro, con il cambio usato nei rapporti |

## Come sono scritti i documenti

- Ogni fatto porta la sua fonte. Nei rapporti di `ricerca/` c'è l'etichetta `[verificato: fonte]` o `[non verificato]`; nei documenti di `docs/` c'è il link alla sezione della proposta o al rapporto.
- I prezzi sono IVA esclusa, salvo dove è scritto. Il cambio usato è 1 $ = 0,8934 €.
- Se una cifra di `docs/` sembra diversa da quella della proposta, vale la proposta.

## Rigenerare DOCX e PDF della proposta

Dalla cartella principale della repo, con Python, la libreria python-docx e LibreOffice:

```
python -I -X utf8 strumenti/md_to_docx.py strumenti/modello-stile-sersan.docx PRESENTAZIONE-CEO.md PRESENTAZIONE-CEO.docx "SerSan Agent OS · Proposta di progetto · Documento interno" strumenti/brand/sersan-lockup.png
soffice --headless --convert-to pdf PRESENTAZIONE-CEO.docx
```

I dettagli, compreso come rifare il marchio, sono nella [sezione 9 di docs/06](docs/06-sviluppo.md#9-rigenerare-docx-e-pdf-della-proposta).
