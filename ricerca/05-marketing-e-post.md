# 05. Marketing e post: piano, produzione, pubblicazione e dove entrano gli agenti

Rapporto di ricerca per la presentazione del sistema multi-agente SerSan. Stato dei fatti al 24/10/2026, letto dai file locali indicati (nessun file dei repo è stato modificato). Ogni fatto porta la fonte: `[verificato: percorso]` se letto in un file o nell'ambiente di questa sessione, `[non verificato]` se è una deduzione o un'informazione esterna ai file. Dove un dato manca, è scritto "non trovato".

Percorsi abbreviati: `MKT/` = `C:/Users/alber/Documents/SERSAN-marketing/`; `V2/` = `C:/Users/alber/Desktop/sersan-v2-main/marketing/`.

Revisione del 24/10 (secondo passaggio): i fatti sono stati ricontrollati sui file (calendario.csv, STATUS.md, INVENTARIO, DIRETTIVE, GESTIONE_POST, plugin, `_log/`, DOCX del piano estratto con Python); aggiunti il profilo del log delle generazioni (§3.6), le cartelle citate ma assenti (§3.9) e la corrispondenza con la lista di controllo della visione del file `00-visione-funzionalita.md` (§5.8).

---

## 0. Sintesi in una pagina

- **Il piano esiste in tre generazioni**: il vault del 25/08 (`V2/`, 168.000 parole, 24 ricerche, 626 fonti) [verificato: V2/README.md], la revisione del 26/09 per un team di quattro (`MKT/_docs/piano_originale/revised-plan.md`) e il PDF del 13/10 di 175 pagine (`MKT/_docs/SERSAN-Piano-marketing-90-giorni.pdf`) con Parte 1-3 e Appendici A-C [verificato: PDF p.1; STATUS.md, voce 13/10 sera]. Sopra il piano, dal 22/10, valgono **due direttive operative per ruolo**: `DIRETTIVE_CONTENUTI.md` (produrre) e `GESTIONE_POST.md` (programmare e pubblicare) [verificato: MKT/README.md punto 0].
- **Motore della domanda: LinkedIn organico dai profili personali di Michele e Alessandro**, 2+2 post a settimana (martedì e giovedì), 5 post su 6 senza link; Company Page come reshare del flagship il mercoledì; Instagram un asset a settimana (carosello il martedì, reel il giovedì o venerdì); YouTube dalla W5 per podcast e Shorts; newsletter di Michele solo se la decisione del 23/11 è sì; paid a zero per 90 giorni [verificato: revised-plan.md §5; PUBBLICAZIONE/README.md "Regole fisse"; GESTIONE_POST.md §4].
- **Attesa onesta dichiarata dal piano**: caso base **zero audit firmati entro Natale**; al 21/12 il successo è una pipeline di proposte aperte con almeno una SOW inviata [verificato: PDF p.2; revised-plan.md §2].
- **Calendario W01-W13: 96 slot**, nessuno PRONTO al 03/10 (DA APPROVARE 35, DA PRODURRE 34, BLOCCATO 23, DA MONTARE 4); lo stato nel CSV non è stato aggiornato dopo il 03/10 [verificato: PUBBLICAZIONE/CALENDARIO.md; calendario.csv].
- **Pubblicato davvero** (dati al 13/10): CR03 su Instagram e Facebook il 06/10 (reach 216, 312 visualizzazioni, 2 like, 1 condivisione), TD2 come carosello IG il 09/10 (reach 19), CR03 come PDF sulla Pagina LinkedIn il 13/10 (primo post della Pagina); altri 5 pezzi in coda Metricool fino al 22/10; **dopo il 22/10 la coda è vuota** [verificato: MKT/_docs/STATUS.md, voci 08/10, 13/10 e "Stato attuale 22/10"].
- **Come si pubblica oggi**: Alberto programma Pagina LinkedIn, Instagram e Facebook con Claude Code via il connettore MCP di Metricool (brand `sersan_ai`), dopo un sì registrato; i profili LinkedIn dei founder restano nativi (non collegati a Metricool); nessun post dei founder risulta pubblicato dai file [verificato: STATUS.md 06/10 e 08/10; PDF Appendice C1].
- **Cosa blocca**: pulizia D1 del sito non online (quindi niente link a sersan.io), nessuna registrazione dei founder (provino, voce, clip), crediti Higgsfield a 1,56 fino al rinnovo del 27/10, Matteo (marketing operativo) assente, SerSanOutreach fermo dal 16/10 per la migrazione su Azure, MCP locali di After Effects e Blender assenti [verificato: STATUS.md "Stato attuale degli strumenti (22/10/2026)"].
- **Automazione già prevista o pronta ma non attiva**: `_log/linkedin_commenti.py` (commenti e reazioni LinkedIn via Publora, 43 prove, dry-run a posto, manca l'account Publora), plugin Claude Code `contenuti-sersan` (245 prove, da verificare in sessione vera), tre task programmati di `linkedin-skills` (bozze del lunedì, commenti, pubblicazione), sette automazioni con API Claude stimate in STACK_STRUMENTI §5 [verificato: STATUS.md 22/10; GESTIONE_POST.md §9; STACK_STRUMENTI_2026-10-13.md §5].
- **Dove un sistema di agenti si inserisce senza violare le regole di casa**: a monte (idee, bozze, QA, impaginazione, calendario, metriche, segnali d'intento dal CRM e dall'outbound) e a valle della pubblicazione (numeri, ledger, criterio di stop, loop con SerSanOutreach). **Non** sulla pubblicazione senza sì umano, non sui commenti generati senza regole approvate dal titolare, mai sui DM fuori da SerSanOutreach [verificato: GESTIONE_POST.md §2, §9 "Cosa non si automatizza mai"; DIRETTIVE_CONTENUTI.md §2].

---

## 1. Fonti lette

| File | Data nel file | Cosa è |
|---|---|---|
| `MKT/README.md` | 22/10 | Ordine di lettura, struttura, regole non negoziabili, ID Higgsfield |
| `MKT/_docs/SERSAN-Piano-marketing-90-giorni.pdf` (+ .docx) | 26/09, agg. 13/10 | Piano dei 90 giorni, 175 pagine: Parte 1 sintesi, Parte 2 task per persona, Parte 3 video e pubblicità, App. A piano rivisto, App. B piani per persona, App. C strumenti |
| `MKT/_docs/piano_originale/revised-plan.md` | 26/09 | Sorgente markdown dell'Appendice A (tesi, decisioni D1-D14, canali, motore, outreach, numeri) |
| `MKT/_docs/DIRETTIVE_CONTENUTI.md` (+ docx, pdf) | 22/10 | Direttive per chi produce: ruoli, via A/B, schede B1-B14, A1-A5, C1-C6, immagini, caroselli, testi, QA, consegna, registri, plugin |
| `MKT/_docs/GESTIONE_POST.md` (+ docx, pdf) | 22/10 | Direttive per chi pubblica: approvazioni, accessi, settimana tipo, specifiche per rete, Metricool, LinkedIn automatizzato, SerSanOutreach, numeri |
| `MKT/_docs/STATUS.md` | 22/10 | Stato degli strumenti e registro storico (crediti, batch, decisioni, pubblicazioni) |
| `MKT/_docs/INVENTARIO_CONTENUTI.md` | 03/10 | 352 file media per tipo e stato |
| `MKT/_docs/RICERCA_VIDEO_FOUNDER_2026-10-13.md` (+ factcheck) | 13/10 | Via A (tutto generato) e via B (ibrida) per i video di Alessandro |
| `MKT/_docs/STACK_STRUMENTI_2026-10-13.md` (+ factcheck) | 13/10 | Strumenti dopo il premio Claude, matrice contenuto-strumento, automazioni, piano di adozione |
| `MKT/_docs/COPIONI_PUNTI_APERTI_2026-10-14.md` | 14/10 | Punti aperti prima di inviare i copioni ai founder |
| `MKT/_docs/DA_MONTARE.md`, `AE_PIANO_MONTAGGIO.md` | 03/10, agg. 13/10 | Coda di montaggio e template After Effects |
| `MKT/_docs/VOLTI_E_VOCE_FOUNDER.md` | 01/10, agg. 13/10 | Esito dei test su volti e voci |
| `MKT/PUBBLICAZIONE/CALENDARIO.md`, `calendario.csv`, `README.md`, `Wnn_*/SETTIMANA.md` | 03/10, agg. 13/10 | Calendario W01-W13, stati, regole fisse, decisioni aperte |
| `MKT/PUBBLICAZIONE/PRONTI_SUBITO/*` | 06-08/10 | Finali pronti, `POSTA_ORA.md`, `PIANO_AUTO.md`, `PIANO_IG_PAGINA_09-22-10.md`, `PROFILI_BIO.md` |
| `MKT/_plugin/contenuti-sersan/`, `MKT/.claude-plugin/marketplace.json` | 22/10 | Plugin Claude Code per chi produce e pubblica |
| `MKT/scripts/`, `MKT/posts/`, `MKT/_log/` | 30/09-22/10 | Brief editoriale, copioni, battute, caption, template, strumenti e log |
| `V2/README.md`, `V2/00-MASTER-PLAN.md`, `V2/01-strategy/content-pillars.md`, `V2/03-channels/linkedin.md`, `V2/06-automation/stack-and-rag.md`, `V2/07-measurement/measurement.md` | 24-25/08 | Vault del piano originale |
| `C:/Users/alber/Desktop/sersan-v2-main/PIANO.md` | 08/06 | Piano della Fase 2 del sito (WebGL): non riguarda il marketing, solo il sito come prova |
| `C:/Users/alber/Desktop/SERSAN-brand-film.aep` | 08/09 | Esiste: 253.124.407 byte; il piano AE dice di importarne solo l'outro `SRS Outro` [verificato: ls; AE_PIANO_MONTAGGIO.md §0.4] |
| `C:/Users/alber/SerSanOutreach/README.md`, `mcp_server/README.md` | – | Piattaforma outbound HITL, MCP `sersan-outreach` (sola lettura) e `sersan-operator` |

Conteggi delle cartelle media (solo elenco) [verificato: `find` del 24/10]: `posts/` 836 file (382 png, 242 html, 99 json, 8 pptx, 8 pdf), `images/` 110 (108 png), `video/` 128 (113 mp4, 14 wav), `audio/` 13 mp3, `_archivio/` 787, `_scartati/` 97, `_ref/` 85 (foto e voci dei founder, fuori dal repository). Sottocartelle: `posts/carousels` 698, `posts/teardowns` 136, `video/characters` 45, `video/loops` 34, `video/hooks` 21, `images/characters` 30, `images/backgrounds` 28, `images/key-visuals` 27, `audio/av03_takes` 13.

Repository Git: tre commit, tutti del 22/10 ("Base del repository", "Immagini e caroselli", "Video"); working tree pulito [verificato: `git log`, `git status`]. Nessun file del progetto porta una data successiva al 22/10: lo stato di questo rapporto si ferma lì.

---

## 2. Il piano marketing

### 2.1 Le tre generazioni e cosa vale oggi

| Versione | Dove | Cosa dice in più |
|---|---|---|
| Piano 2026 del 25/08 (due founder) | `V2/00-MASTER-PLAN.md` e 25 capitoli | Tesi "indipendenza proprietaria verificabile", 5 pilastri, LinkedIn come unico motore, newsletter entro il giorno 30, n8n + RAG su `marketing/` + pgvector, Attio come CRM, "zero automazione, zero pod, zero hashtag" su LinkedIn, compliance come gate [verificato: V2/README.md; V2/03-channels/linkedin.md §1; V2/06-automation/stack-and-rag.md §0] |
| Revisione del 26/09 (team di quattro) | `MKT/_docs/piano_originale/revised-plan.md`; Appendice A del PDF | Ruoli per persona, 21 canali con ore, decisioni D1-D14, SerSanOutreach al posto di n8n/Attio/Clay, avatar AI del team "sì, a condizione" (D14), numeri del lunedì rivisti [verificato: revised-plan.md §3, §5, §11] |
| PDF del 13/10 (175 pagine) | `MKT/_docs/SERSAN-Piano-marketing-90-giorni.pdf` | Aggiunge l'Appendice C: strumenti del premio Claude, via A e B con provino, voce, automazioni, gate 1-4 (19/10, 26/10, 02/11, 09/11) [verificato: PDF p.1-2, p.167-169] |
| Direttive del 22/10 | `MKT/_docs/DIRETTIVE_CONTENUTI.md`, `GESTIONE_POST.md` | "Dove i documenti del 13-14/10 dicono altro, valgono queste". Il piano grande non si aggiorna più [verificato: MKT/README.md punto 0; STATUS.md 22/10] |

Decisioni di Alberto registrate il 22/10 che cambiano il piano: budget senza limiti; account propri nei workspace aziendali; LinkedIn anche con commenti automatici; Metricool con l'accesso aziendale e il sì nel registro [verificato: STATUS.md, voce 22/10]. La regola del piano "niente strumenti terzi sui profili" è superata per le superfici aziendali dal 06/10 (Metricool) [verificato: STATUS.md 06/10; PDF p.167].

### 2.2 Tesi, posizionamento e obiettivi

- **Posizionamento** (regola 3 del brief): "SERSAN Limited, London. A founder-led software engineering and AI studio: custom software, automation, and AI where it earns its place." Tesi di marca "AI where it earns its place" / "L'AI dove se lo merita"; tagline solo come firma "The intelligence is artificial. The judgement stays human."; CTA fissa "Send a project brief." / "Inviaci un brief di progetto.", mai "Book a call" [verificato: MKT/scripts/_BRIEF.md §A regola 3, §B1].
- **Chi parla di cosa**: Alessandro (CEO) parla di esito per il cliente, scoping e rischio, mai presentato come ingegnere; Michele (tech lead) di sistemi, eval, automazione e readiness, firma ogni affermazione tecnica; Alberto (creative lead) di craft (Blender, AE, grading), senza numeri. Tono: 70% cosa guadagna il cliente, 20% come lavora SERSAN, 10% cosa rifiuta [verificato: _BRIEF.md §B1].
- **Obiettivi dichiarati**: il piano del 25/08 puntava a "risposte positive ICP / 200 contattati ≥4%", "costo per call qualificata < £450", "conversione audit → sprint ≥40%" [verificato: V2/00-MASTER-PLAN.md §8]. La revisione riduce le attese: con 100-150 touch in 90 giorni il caso base è 0 audit; attesi 2-5 risposte positive e 1-2 call qualificate da outbound; al giorno 90 conta la pipeline con almeno una SOW inviata [verificato: revised-plan.md §2; PDF p.2 "Attese oneste"].
- **Vincolo trasversale**: nessun contenuto e nessun messaggio outbound che porti traffico a sersan.io prima della pulizia D1 del sito (ruoli precedenti, loghi di terzi, numeri non verificati, token di telemetria). Al 22/10 la pulizia non è online [verificato: revised-plan.md §2; STATUS.md 22/10].

### 2.3 Canali

| Canale | Ruolo nel piano | Cadenza | Owner | Stato al 22/10 |
|---|---|---|---|---|
| LinkedIn, profili personali di Michele e Alessandro | Motore della domanda | 2 post a settimana ciascuno, mar e gio; 5 su 6 senza link; 15 min di commenti al giorno prima di postare; teardown PDF quindicinale (Michele) e video nativo quindicinale a settimane alterne | Founder pubblicano dal proprio account; Matteo prepara (assente), asset Alberto | Nessun post dei founder risulta pubblicato nei file; profili non collegati a Metricool [verificato: STATUS.md 08/10; CALENDARIO.md] |
| LinkedIn Company Page "SERSAN" | Credibilità: reshare riscritto del flagship il mercoledì, "Notify employees" una volta a settimana | 1 a settimana + documenti PDF | Matteo (assente); di fatto Alberto via Metricool | Primo post 13/10 (CR03 PDF); coda fino al 22/10 [verificato: STATUS.md 13/10] |
| LinkedIn, profilo di Alberto | Voce "craft" | Un post ogni due settimane dalla W5 (W05, W07, W09, W11), senza numeri | Alberto | DA PRODURRE [verificato: calendario.csv] |
| Instagram @sersan_ai (+ Pagina Facebook come asset Meta) | Prova visiva e pubblico craft; "pipeline attesa zero" | Un asset a settimana: carosello il martedì o reel del sito il giovedì; reel con founder il venerdì; mai due post feed lo stesso giorno | Matteo (assente); Alberto via Metricool | 1.121 follower al 13/10; CR03 e TD2 pubblicati; bio ancora "Scrivici PROCESSO in DM" verso la home [verificato: STATUS.md 13/10] |
| YouTube canale SERSAN | Minimo: Shorts dai master, podcast video dalla W5, CLIP-ALE-AUDIT 16:9 in W12 | Venerdì | Matteo (assente) | Canale "da preparare entro ven 16/10": esito non trovato |
| Newsletter LinkedIn di Michele | Bypassa il feed | Mensile, prima edizione 02/12 o 09/12 solo se D5/D-10 passa il 23/11 | Michele | BLOCCATO (D-10) [verificato: calendario.csv W10-NL-MIC-1] |
| Podcast video (D14) | Un episodio 16:9 da 25-35 min per fonte registrata, su YouTube (Spotify solo se confermato) | W5, W7, W9, W11, quinto in scorta | Founder, montaggio Alberto | Nessuna sessione registrata; tutti gli slot BLOCCATO [verificato: PDF p.5 "mar 13/10"; calendario.csv] |
| Articoli LinkedIn long-form | Due nei 90 giorni (TD1 in W7, TD3 in W11) dal profilo di Michele | – | Matteo adatta, Michele rivede | DA PRODURRE |
| Outreach umano e SerSanOutreach | Pipeline: binario LinkedIn manuale dal 07/10, SerSanOutreach dal 16/11 (email solo UK, inglese; LinkedIn solo manuale) | Rampa 1 → 10 → pilot 20 (30/11-11/12) | Alessandro approva, Matteo opera | SerSanOutreach fermo dal 16/10 (migrazione Azure) [verificato: STATUS.md 22/10; revised-plan.md §8] |
| Rete e referral Italia | 40% dell'acquisizione | – | Alessandro | non trovato nei file del marketing |
| SEO/AEO | Lento, difendibile; `robots.ts`, `sameAs`, `Content-Signal` | Una tantum (Michele) | Matteo, Michele | non trovato |
| Google Search, LinkedIn Ads, Meta Ads | Chiusi o spenti nei 90 giorni (LinkedIn Ads solo sopra 2.000 €/mese per 6 mesi; Meta spento) | – | – | Spenti [verificato: V2/00-MASTER-PLAN.md §4; revised-plan.md §5] |
| X, TikTok, Threads, Behance, Spotify | Parcheggiati o non aperti | – | – | Solo handle riservati [verificato: PUBBLICAZIONE/README.md "Canali e profili"] |

Fonte principale della tabella: `revised-plan.md` §5 e `PUBBLICAZIONE/README.md` "Canali e profili" e "Regole fisse di pubblicazione" [verificato].

### 2.4 Settimana tipo (per chi gestisce i post)

| Giorno | Cosa |
|---|---|
| Lunedì | Numeri della settimana prima (Metricool), orari, coda, bozze LinkedIn dei founder con linkedin-skills (task 08:00) |
| Martedì | Founder dal proprio profilo; Pagina LinkedIn 11:00; Instagram e Facebook 10:00 |
| Mercoledì | Gate: sì sulla settimana successiva; reshare della Pagina sul post del founder (+24 h, "Repost with your thoughts") |
| Giovedì | Come martedì |
| Venerdì | Instagram e Facebook 10:00 (reel con persona); YouTube |

Regole: un post al giorno per profilo; un reel con un founder sostituisce un suo post; almeno due settimane di pezzi PRONTI nel calendario; orari migliori da Metricool (`getBestTimeToPostByNetwork`) [verificato: GESTIONE_POST.md §4, §7].

### 2.5 Formati

Dal calendario (96 slot) [verificato: calendario.csv, conteggio del 24/10]: post di solo testo 23, post + Notify employees 9, reel avatar 4:5 8, reel avatar 9:16 8, carosello 8 frame 4:5 5, episodio podcast 16:9 5, PDF documento 10 tavole 4, post craft 3 (+1 con media Blender), Shorts 3, video 4:5 60-90 s 2, reel di cattura del sito 2 (+1), articolo LinkedIn 2, video tipografico 1, reel tipografico 1, newsletter 1, caption sostitutiva 1, reshare 1, video reale 4:5 con SRT 1.

Per canale: LinkedIn 59, Instagram 20, YouTube 13 (+1 condizionato a Spotify), newsletter 1, scorta 1, IG+LinkedIn 1. Per profilo: Michele 23 (+1), Alessandro 22, @sersan_ai 20, canale YouTube 15, Company Page 10, Alberto 4 [verificato: calendario.csv].

Specifiche per rete (misure, limiti) in `GESTIONE_POST.md` §5: LinkedIn immagine 1080x1350 o 1080x1080, testo 3.000; documento PDF 1080x1350 fino a 300 pagine e 100 MB; video 4:5 o 9:16, 3 s-15 min; Instagram 1080x1350 sRGB, fino a 10 slide, testo 2.200, max 3 hashtag; reel 1080x1920 H.264; YouTube 16:9, thumbnail 1280x720, almeno 3 capitoli, SRT EN e IT [verificato].

### 2.6 Pilastri di contenuto

Dal vault del 25/08, ripresi dal brief del 30/09 [verificato: V2/01-strategy/content-pillars.md §1; _BRIEF.md §A "Pillar P4 is renamed"]:

| Pilastro | Voce | Cadenza prevista | Formato | Esempi nel calendario |
|---|---|---|---|---|
| P1 Il Teardown | Michele | 1 ogni 2 settimane | PDF LinkedIn 10 tavole + reel + clip | TD1 "The eval set before the agent", TD2 "The forty-minute check", TD3 "Your AI vendor is one line in a Register of Information", TD4 "What we look at in the first two hours of an audit" |
| P2 Il Rifiuto | Alessandro | 1 a settimana, tetto 1 pezzo su 10 | Post corto + video 30-60 s | V02 "Six refusals" (tipografico) |
| P3 I Quattro Layer | entrambi | 1 al mese | Carosello, self-assessment, podcast | CR2 "Which layer are you on?" |
| P4 Readiness (ex "Compliance") | Michele | 1 ogni 2 settimane | Guida, checklist, post con date | CR4 "Readiness in practice", V19 spiegone DORA |
| P5 Il Lavoro | entrambi | 1 al mese | Case study, video, thread | V05 spores, V11 logo breakdown, CLIP-ALE-BRIEF, CLIP-ALE-AUDIT |

Serie nuove nei copioni del 14/10 senza slot in calendario: "Al bar" (BAR-1..5), "Prima di inviarci un brief" (FAQ-1..7), storie ST-1..8 di Alessandro e MST-1..5 di Michele [verificato: COPIONI_PUNTI_APERTI_2026-10-14.md punto 7].

### 2.7 Chi fa cosa

| Persona | Ruolo nel piano | Ore proposte | Nota |
|---|---|---|---|
| Alessandro | CEO, decide, vende, approva i testi non tecnici, si registra da solo (provino, voce, CL1, CL2, AV03), titolare di Claude Team (proposta) | 14 h in W1-W2, poi 12-15 h | [verificato: PDF p.6] |
| Michele | Tech lead: firma ogni claim tecnico e i teardown, infrastruttura di SerSanOutreach, zero outbound; AV02 via da decidere | circa 11 h/sett. | Freno: sopra il 60% di utilizzo fatturabile si rallenta [verificato: PDF p.6; revised-plan.md §11 n.5] |
| Alberto | Creative lead: AE, Higgsfield, cattura del sito, montaggio; dal 06/10 pubblica Page, IG e FB via Metricool; admin di Claude Team (proposta) | 14 h, tetto 15; con D14 circa 18 h | [verificato: PDF p.6] |
| Matteo | Marketing operativo e social: calendario, gate light, claims register, ledger, community, liste outbound, numeri del lunedì | 17-22,5 h/sett. | **Assente dal brief del 30/09**; D-14 (chi pubblica intanto) decisa di fatto: Alberto per le superfici aziendali; ledger, numeri e community senza owner [verificato: PDF p.6, p.9-10] |

Nota: il sito mostra Mattia Scattu come Software Engineer, non Matteo; la decisione su chi togliere o aggiungere era attesa entro il 09/10 e al 13/10 non è verificata [verificato: PDF p.9 "Da chiarire con il team"]. Nei file del marketing il quarto membro è sempre "Matteo".

Ruoli funzionali delle direttive del 22/10 (pensati per scaricare lavoro su un nuovo addetto): chi produce i contenuti, chi monta, chi approva i testi, chi firma la parte tecnica, chi autorizza la pubblicazione, chi gestisce i post, il founder, l'amministratore degli strumenti, il responsabile del toolchain [verificato: DIRETTIVE_CONTENUTI.md §1 "Ruoli"]. Il file `_docs/RUOLI.md` che dovrebbe dire chi ricopre ogni ruolo **non esiste** [verificato: ls di `_docs/`; GESTIONE_POST.md §1 lo cita "se manca, chiedilo all'amministratore"].

### 2.8 KPI

**I 10 numeri del lunedì** (riunione di 30 minuti a quattro) [verificato: PDF p.9; revised-plan.md §11]:

| # | Numero | Obiettivo o soglia | Attivo da |
|---|---|---|---|
| 1 | Risposte positive dei contatti ICP sul totale dei contattati | ≥4%; sotto il 2% si riscrive il messaggio (dopo ≥100 contattati) | W2 |
| 2 | Call di scoping prenotate | tetto di capacità 12-14 al mese | W2 |
| 3 | Proposte con SOW inviate, per canale d'origine | ≥1 SOW nei 90 giorni | W2 |
| 4 | Commenti qualificati sui post, da titoli ICP (non reazioni) | ledger | W3 |
| 5 | Utilizzo fatturabile di Michele | sopra il 60% si rallenta l'acquisizione | W1 |
| 6 | Salute del motore: fonte registrata sì/no, pezzi usciti sul piano, settimane di scorta | 2 settimane di scorta | W3 |
| 7 | Rischio aperto: ticket del sito aperti e gate saltati | zero gate saltati | W1 |
| 8 | Instagram: invii su reach e % di reach da non-follower | gate del giorno 90 | W3 |
| 9 | Visite al profilo da titoli ICP | – | W5 |
| 10 | Audit venduti, di cui da canale non-referral | cancello LEAN → STANDARD | W7 |

Regola dei formati vincenti (proposta): Instagram, reel 9:16 contro carosello sulla mediana di invii su reach (≥1,3x) e reach da non-follower, con almeno 3 uscite per formato; LinkedIn, un tema o formato è vincente con ≥2 commenti qualificati da titoli ICP in 2 uscite su 3 [verificato: revised-plan.md §11].

**Criterio di stop per i pezzi dei founder con AI** (via A o B): fermarsi se un cliente ideale, o tre persone in totale, mettono in dubbio l'autenticità, o se per due uscite di fila i commenti qualificati restano sotto la mediana dei post `reale` del founder nelle 4 settimane prima; non si cambia la soglia dopo aver visto i dati [verificato: GESTIONE_POST.md §11; revised-plan.md §11].

**Metriche leggibili da Metricool con Claude Code** (sola lettura, `getAnalyticsDataByMetrics`): Instagram IGPO14 reach, IGPO28 views, IGPO13 like, IGPO08 commenti, IGPO15 salvataggi, IGPO27 condivisioni, IGPO29 follow, IGPO12 interazioni; LinkedIn LIPO12 impressioni, LIPO13 reazioni, LIPO10 commenti, LIPO09 clic, LIPO18 condivisioni. Scritte nel "foglio dei numeri" `PUBBLICAZIONE/numeri.csv` (settimana, pezzo, rete, metrica, valore) e nel ledger [verificato: GESTIONE_POST.md §11]. Il file `numeri.csv` **non esiste ancora**, come `registro_si.csv`, `ledger.csv` e `_registri/` [verificato: STATUS.md 22/10; ls di `PUBBLICAZIONE/`].

Il vault del 25/08 avverte che l'attribuzione classica non funziona a questi volumi (GA4, Smart Bidding, MMM sotto soglia): "non modelliamo, contiamo", registro a mano con identità first-party [verificato: V2/07-measurement/measurement.md §1].

### 2.9 Regole di brand non negoziabili

Ogni testo in EN e poi IT nello stesso post (riga `· · ·` in mezzo, D-01 decisa il 06/10), "AI" mai "IA" (D-03), CTA una volta per lingua, zero punti esclamativi ed emoji, niente prezzi, niente numeri dei ruoli precedenti di Michele, mai "compliant", "certified", "3am", "two people", "SERSAN AI"; nessuna etichetta AI, disclaimer o C2PA; interruttori AI delle piattaforme spenti; hashtag al massimo 3 su Instagram e zero su LinkedIn e YouTube; nessun link su LinkedIn, nella caption Instagram e nel primo commento; mai testo, lettere o marchio generati dentro immagini e video; volti e voci solo dei founder con consenso scritto; niente esce senza un sì umano scritto nel registro del sì; testi "BOZZA da approvare" fino al sì [verificato: MKT/README.md "Regole non negoziabili"; GESTIONE_POST.md §2; DIRETTIVE_CONTENUTI.md §2].

Nota per la presentazione: la riga "niente etichette AI" delle direttive del 22/10 è in contrasto con il piano del 26/09 (D14: etichetta visibile per tutta la durata, riga in caption, toggle della piattaforma, C2PA) e con il vault del 25/08 ("un annuncio non etichettato o una voce sintetica non dichiarata costa più della campagna") [verificato: revised-plan.md §3 D14 regola 2 e §12 rischio 16; V2/README.md regola 4]. Le direttive vincono per ordine di lettura, ma è una scelta da tenere consapevole quando si progettano agenti che toccano i toggle delle piattaforme.

### 2.10 Decisioni aperte che pesano di più (al 22/10)

| ID | Decisione | Chi | Stato |
|---|---|---|---|
| D1 (sito) | Pulizia del sito: via ruoli precedenti, loghi di terzi, numeri, telemetria | Alberto esegue, Michele rivede, Alessandro firma | Non online; nuova data da fissare [verificato: STATUS.md 22/10] |
| D-14 | Chi pubblica, tiene ledger, numeri e community mentre Matteo è assente | Alessandro | Di fatto Alberto per le superfici aziendali; il resto senza owner [verificato: PDF p.9-10] |
| D-18 | Via A, B o entrambe per i video di Alessandro, decisa sul provino | Alberto | Provino non girato [verificato: STATUS.md 22/10] |
| D-04 | V11, V12, V13, V19: Michele reale o avatar | Michele + Alberto | Aperta; la voce di Michele non è registrata né clonata [verificato: CALENDARIO.md W05] |
| D-05 | Nome dello show del podcast | Alessandro | Aperta (scadeva 16/10) |
| D-10/D5 | Newsletter sì o no, nome, tema | Michele + Alessandro | 23/11 |
| Gate 1-4 degli strumenti | Grant ElevenLabs, moda, Metricool (19/10); voce e via (26/10); automazioni (02/11); intake (09/11) | Alberto | Esito del gate 1 del 19/10: **non trovato** nei file |
| Calendario editoriale | Notion (legge e scrive) o Google Drive (sola lettura), scelta entro il gate 1 | Alberto | Non trovato [verificato: PDF p.3, p.169] |

Elenco completo delle decisioni D-01..D-18 e D-C2..D-C7 in `PUBBLICAZIONE/README.md` "Decisioni aperte" e `_BRIEF.md` Appendix 1 [verificato].

---

## 3. Il flusso di produzione attuale

### 3.1 Testi

- **Brief editoriale** `scripts/_BRIEF.md` (15.697 parole, sezioni A-I: regole, posizionamento, podcast, reel, clip, teardown, caroselli, calendario H, banca asset I, decisioni) scritto da Alberto il 30/09; sovrascrive ogni documento del piano [verificato: _BRIEF.md §A; scripts/_INDEX.md].
- **Generazione**: un workflow Claude `sersan-content-drafts` (82 agenti, 0 errori) ha prodotto dal brief 19 deliverable (5 episodi podcast, reel AV02/AV03, clip di Alessandro, 4 teardown, 5 caroselli, caption W1-W12) con verifica avversariale a due lenti (brand e fatti, lingua parlata), correzione, lista battute e indice [verificato: STATUS.md "Testi: workflow completato"; _INDEX.md].
- **Battute**: `scripts/battute/BATTUTE_master.csv`, 348 battute EN e 348 IT (708 righe), unica fonte per generare; i file `*_battute.md` sono obsoleti [verificato: _INDEX.md; STATUS.md].
- **Marcatori aperti dopo la generazione**: circa 700 `[CHECK MICHELE]`, 227 `[NATIVE IT]`, 157 `[DECISION …]`, 49 `[CHECK ALBERTO]`, 10 battute bloccate da `[SHOW NAME]` [verificato: STATUS.md].
- **Copioni di registrazione per i founder** (14/10): Alessandro 49 pagine, Michele 45, podcast insieme 31 (DOCX, PDF, MD), generati con `assemble_copioni.py`, `assemble_michele_joint.py`, `build_copioni.py` in `_docs/lavoro_copioni_14-10/`; **non ancora inviati**, 8 decisioni da prendere prima [verificato: COPIONI_PUNTI_APERTI_2026-10-14.md].
- **Caption pronte**: `posts/captions/CAPTIONS_W01-W06.md` e `W07-W12.md`, copiate parola per parola in `PUBBLICAZIONE/Wnn_*/SETTIMANA.md`; `POSTA_ORA.md` elenca 22 post pubblicabili dopo l'ok (verifica avversaria) e 2 da non postare (CR05 racconta uno Sting A mai prodotto; W04-LI-MIC-2 rimanda a V12 non prodotto) [verificato: PUBBLICAZIONE/README.md; POSTA_ORA.md].
- **Approvazione**: Alberto riferisce che Alessandro e Michele hanno approvato tutti i testi il 06/10 [verificato: STATUS.md 06/10]. Il "registro del sì" previsto dalle direttive non esiste ancora come file.
- **Post LinkedIn dei founder, a regime**: bozze con il plugin `linkedin-skills` (sergebulaev): Story Bank e profilo di voce per founder (`_ref/<founder>/story-bank.md`, `voice-profile.md`, mai in repository), poi `linkedin-content-planner`, `linkedin-post-writer`, `linkedin-humanizer --mode audit`; task del lunedì 08:00 con `claude -p "Esegui l'attività 1 del §9…" --strict-mcp-config` (niente connettori, quindi nessuna scrittura su Metricool) [verificato: GESTIONE_POST.md §9]. Stato: plugin da installare, Story Bank da fare [verificato: STATUS.md 22/10].
- **Conversione documenti**: `_log/md_to_docx.py` produce i DOCX con lo stile del piano (ink #0B1422, blu #1668BA) [verificato: _log/md_to_docx.py].

### 3.2 Immagini, caroselli e PDF

- **Immagini generate su Higgsfield**: key visual e fondali con `nano_banana_pro` 2k (sito) o `gpt_image_2_5` (`#W57`); ritratti con `gpt_image_2` da 2 foto reali + `seedream_v5_pro` per la pelle; scene dei caroselli `seedream_v5_pro` 3:4 2k senza testo; thumbnail `#W78`. Palette scura (teardown) `#0B1422`, `#F4F6FA`, `#2280DC`, `#8A94A6`, accento raro `#3BE1FF`, font Fraunces, Switzer, JetBrains Mono; palette chiara (caroselli) `#F4F2ED`, `#07162C`, accento `#2553E8` [verificato: DIRETTIVE_CONTENUTI.md §9].
- **Caroselli Instagram**: template HTML "v3 chiara" `posts/carousels/v3_light/_template/` con `build.py data/<ID>_EN.json` (Chrome rende i font veri, scena come `<img>` sotto il testo; `--final` toglie il chip BOZZA; `qa.json` per frame; `_sheet.jpg` foglio provini). Misure prese dal carosello già pubblicato dal collega a settembre [verificato: build.py docstring e BASE]. La "route social Higgsfield" (`brand-asset-creation`, testo nei pixel) è stata provata su CR3: 0 slide su 8 passano la QA, 84,5 crediti; resta il gemello HTML a 0 crediti [verificato: STATUS.md 30/09 19:40].
- **Teardown PDF LinkedIn**: kit PPTX/PDF `posts/teardowns/out/kit/sersan_td_kit_v3_1.zip` con `kit/build_deck.py <contenuto>.json` (serve LibreOffice), 10 tavole 1080x1350, `_qa.json` con `pass: true`; font e marchio nel kit [verificato: DIRETTIVE_CONTENUTI.md §10; ls di `posts/teardowns/out/`].
- **moda.app**: workspace "sersan.dev", secondario finché l'amministratore degli strumenti non lo autorizza; via CLI impaginazione ed export senza crediti, niente video, niente founder [verificato: STATUS.md 22/10; DIRETTIVE §10].
- **Canva**: giudicato non necessario finché twin HTML e moda coprono gli stessi passaggi (bulk create solo Enterprise) [verificato: STACK_STRUMENTI §2 "Altri connettori"; PDF p.169]. Il connettore Canva in questa sessione richiede autenticazione [verificato: avviso di sessione].
- **Claude Slides e Design**: per deck e presentazioni dei founder, export PPTX o PDF; deck HTML con `#W44` [verificato: DIRETTIVE §10 "Altri strumenti"].

### 3.3 Video

- **Due vie per i founder**: via B (preferita) il founder si registra davanti a una parete, poi l'AI cambia solo luogo, luce o vestiti (Ad Multiplier Edit `#W71`, Genjutsu Object Swap `#W63`, scontorno + fondale `#W49`/`#W59`/`#W57`, Video Relight solo a mano); via A (tutto generato: ElevenLabs Avatars, HeyGen, Lipsync Studio) solo dopo il provino giudicato alla cieca da tre persone [verificato: DIRETTIVE §4-§6]. Le 14 clip AV03 generate il 30/09-01/10 (Seedance 2.5 con voce TTS) **non si pubblicano**: volto fedele, voce "per niente attendibile" perché guidata dal TTS [verificato: VOLTI_E_VOCE_FOUNDER.md §6].
- **Video senza founder**: b-roll, plate e loop con Seedance 2.5 o Kling 3.0 (`#W56`; loop Kling pro con `start_image = end_image`); hook da 3 s image-to-video; explainer con Claude Motion (solo app Claude, bozze) o `#W38` HyperFrames; faceless narrato `#W68`; promo dal sito `#W39`; logo e motion graphics `#W36` in HyperFrames; varianti lingue e formati `#W55` [verificato: DIRETTIVE §7; Appendice B].
- **After Effects 2026** (unica app Adobe sul PC di Alberto): master dei template di marca T03 hook, T04 sottotitoli EN/IT, T05 endframe, T06 Sting B, T07 titoli di capitolo, T10 transizioni, con controllo di lingua `IT` in Essential Graphics; progetto `ae/SERSAN-content-90d.aep` **da creare**; comp a 24 fps (girato reale a 25); render H.264, loudness con ffmpeg (-14 LUFS reel, -16 podcast) [verificato: AE_PIANO_MONTAGGIO.md §0-§4; DA_MONTARE.md §0]. Al 22/10 i server MCP locali di AE e Blender risultano assenti (CONNECTION_CLOSED) e i workflow che li richiedono sono bloccati [verificato: STATUS.md 22/10].
- **HyperFrames** (CLI locale, gratis): varianti, reel tipografici rapidi, scontorno delle persone (`npx hyperframes remove-background`), trascrizione (`npx hyperframes transcribe`) [verificato: DIRETTIVE §3, Appendice A "CLI HyperFrames"].
- **Blender**: Sting A (V03) e still per CR5, non prodotti [verificato: calendario.csv W05-LI-ALB-1, W12-IG-SER-1].
- **Brand film**: `C:/Users/alber/Desktop/SERSAN-brand-film.aep` (8/09, 253 MB) con 36 template a nomi duplicati; si importa solo l'outro [verificato: AE_PIANO_MONTAGGIO.md §0.4].
- **Limiti di durata degli strumenti**: Veo 8 s; Kling 3.0, FLUX Video Edit, Genjutsu Lite 15 s; Seedance 30 s; Genjutsu e Ad Multiplier sorgenti 4-30 s [verificato: DIRETTIVE §4].

### 3.4 Voce e audio

Ordine: voce vera registrata, poi clone professionale ElevenLabs (PVC, 45-60 min IT e 30-45 EN, un clone per lingua, condiviso dal founder), clone istantaneo solo per prove; un solo passaggio di lip sync (`sync_so` via `#W62`); mai `voice_change` o `create_voice` di Higgsfield sui founder; voiceover senza founder con `eleven_v4` (`creative_generate_speech`); pulizia e SRT con Voice Isolator e Scribe v2; SFX da ElevenLabs; musica la sceglie chi monta [verificato: DIRETTIVE §2, §8]. I cloni `Alessandro-EN` e `Alessandro-IT` esistenti vengono da audio WhatsApp compresso e sono solo riserva; la voce di Michele non è registrata [verificato: README.md "Aggiornamento 13/10"; CALENDARIO.md].

### 3.5 Il plugin Claude Code `contenuti-sersan`

- Marketplace `sersan-marketing` (`.claude-plugin/marketplace.json`), plugin v1.0.0 in `_plugin/contenuti-sersan/`, installazione `claude plugin marketplace add SerSan-AI-Studio/SERSAN-marketing --sparse .claude-plugin _plugin` [verificato: plugin.json; DIRETTIVE Appendice A].
- Tre hook: `SessionStart` (`session-start.js`: inietta `contesto-sessione.md`, regole di brand, ruoli, etichette, max 4.000 caratteri, solo dentro il repository), `UserPromptSubmit` (`router.js`: con `#Wnn` inietta il workflow, altrimenti suggerisce workflow e scheda da `routes.json` per parole chiave; `#raw` e `#nomotion` saltano), `PreToolUse` su `createScheduledPost|updateScheduledPost|createScheduledPostForReview|sendScheduledPostForReview` di qualsiasi MCP (`metricool-ask.js`: risponde `ask`, conferma umana obbligatoria) [verificato: hooks.json; file degli hook].
- Workflow inclusi (per chi produce; quelli di AE, Blender e TX Library restano sul PC di chi monta): W00, W03, W36-W49 (HyperFrames), W55, W56-W66 (Higgsfield generazione), W67-W82 (Higgsfield cloud, UGC, thumbnail, brand asset), W87, W88, W90 [verificato: `_plugin/contenuti-sersan/motion-design/INDEX.md`; elenco file].
- Stato: 245 prove e `claude plugin validate` a posto; da verificare in una sessione vera la conferma sulle scritture Metricool e i nomi dei tool [verificato: STATUS.md 22/10].

### 3.6 Strumenti in `_log/`

`prompts.py` registro dei prompt; `specs_tool.py add|done|mark` (specifiche per batch, download e log, scarti in `_scartati/`); `hf_archive.py manifest.json` download e log; `build_docs.py` rigenera le tabelle AUTO di `_docs/gen/*.md` e il riepilogo crediti in STATUS; `contact_sheet.py` e `review_video.py` fogli di revisione; `riordina.py` e `allinea_log.py` (riordino del 03/10); `linkedin_commenti.py` + `test_linkedin_commenti.py` (36 KB + 33 KB); `md_to_docx.py`; `generations.csv` 375 righe, 4.002,14 crediti registrati; `specs.json` 181 KB; `manifests/` per ogni job (121 file) [verificato: MKT/README.md "Strumenti"; ls e wc di `_log/`].

Profilo del log delle generazioni [verificato: `_log/generations.csv`, lettura con Python il 24/10]: colonne `timestamp_utc, file, model, params, prompt, seed, credits, job_id, uso_previsto, status, source_url`; **tutte le 375 righe portano la data 2026-09-30**, cioè l'unico giorno di generazione a crediti (il batch del bonus Credit Reset); dopo quella data le sessioni hanno lavorato a 0 crediti. Modelli più usati: `nano_banana_pro 2k` 76 righe (+18 in altre varianti), `seedream_v5_pro` 71 (+8 a 2k), `kling3_0 pro, sound off` 65 (+4), `gpt_image_2` 27 (+10 a 2k high), `minimax_h3 2K` 20 (+3), `seedance_2_5 omni_reference 1080p` 14, `seed_audio` 5, `soul_2 + soul_id` 3. È il dato da cui partire per stimare il consumo di un agente visual a regime: il piano stima 2.160-2.270 crediti al mese su 3.000 [verificato: STACK_STRUMENTI §2 "Higgsfield Ultra"].

### 3.7 Come si pubblica oggi

| Superficie | Come | Chi | Stato |
|---|---|---|---|
| Instagram @sersan_ai + Pagina Facebook | Metricool, brand `sersan_ai` (id 7273232), via connettore MCP da Claude Code: `createScheduledPost` con `info` JSON (testo EN `· · ·` IT, `media` URL pubblici caricati sullo storage Higgsfield con `media_upload` + PUT + `media_confirm`, `mediaAltText`, `instagramData.isAiGenerated:false`) | Alberto, dopo il sì | Attivo dal 06/10 [verificato: STATUS.md 06/10; GESTIONE_POST.md §8] |
| Pagina LinkedIn SERSAN (`urn:li:organization:110329207`) | Metricool, stesso brand; documenti PDF con `linkedinData.publishImagesAsPDF` | Alberto | Attivo dal 08/10; primo post 13/10 [verificato: STATUS.md 08/10, 13/10] |
| Profili LinkedIn di Michele, Alessandro, Alberto | Nativo, dal proprio account o scheduler di LinkedIn; a regime brand Metricool `founder_<nome>` con login del founder presente | Il founder | Non collegati; nessun post risultante [verificato: GESTIONE_POST.md §3; STATUS.md 08/10] |
| Commenti, risposte e reazioni LinkedIn | `_log/linkedin_commenti.py` via Publora (chiave in `~/.publora/publora.env`), con regole approvate dal titolare in `PUBBLICAZIONE/regole_commenti/<account>.md`, tetti 5+5 al giorno in rampa fino a 20, file di stop al primo errore | Task 09:30 lun-ven | Pronto, mai eseguito dal vero (manca Publora) [verificato: GESTIONE_POST.md §9; STATUS.md 22/10] |
| YouTube | Dal web di Metricool o YouTube Studio, AI toggle spento, SRT EN e IT | Matteo (assente) | Canale: esito non trovato |
| Inviti, DM, email outbound | SerSanOutreach (`https://outreach.sersan.io`), HITL, tetti 20 inviti/giorno, 40 DM, 30 follow-up | Alessandro approva | Fermo dal 16/10 [verificato: GESTIONE_POST.md §10; STATUS.md 22/10] |

Protezioni sulle scritture: Owner del Team mette su "Needs approval" i quattro tool Metricool nel connettore; l'hook PreToolUse del plugin chiede conferma; a ogni conferma si confrontano i parametri con la lista approvata; Metricool solo da sessione presidiata, "mai da Routines, task programmati o loop" [verificato: GESTIONE_POST.md §2, §8].

Riferimento alla scheda `C6` dell'Appendice C: "Routine e task programmati scrivono sui connettori senza chiedere: per regola Metricool e i connettori che scrivono restano fuori" [verificato: PDF p.168].

### 3.8 Dove si tiene il calendario

- Oggi: `PUBBLICAZIONE/calendario.csv` (UTF-8 BOM, 16 colonne: settimana, data_iso, giorno, slot_id, canale, profilo, formato, pezzo, stato, file_en, file_it, testo_en_fonte, testo_it_fonte, gate, blocchi, condizioni) e `CALENDARIO.md` con "Prossimi 10 giorni"; testi da incollare in `Wnn_*/SETTIMANA.md`; a regime si confronta con `getScheduledPosts` di Metricool [verificato: calendario.csv; GESTIONE_POST.md §4].
- Previsto: calendario editoriale su Notion (legge e scrive) o Google Drive, scelta di Alberto entro il gate 1 (19/10): **esito non trovato** [verificato: PDF p.3, p.169]. Il connettore Notion in questa sessione richiede autenticazione [verificato: avviso di sessione].
- Il vault del 25/08 proponeva Notion solo come "coda di approvazione umana", mai come fonte di verità [verificato: V2/06-automation/stack-and-rag.md §0].

### 3.9 Registri previsti (e non ancora creati)

Log delle generazioni (`_log/generations.csv`, esiste), log delle prove esterne, ledger (`PUBBLICAZIONE/ledger.csv`), claims register, registro dei consensi (`_ref/` + copia in `_registri/`), registro dei diritti, registro del sì (`PUBBLICAZIONE/registro_si.csv`), decision log, calendario, numeri del lunedì (`numeri.csv`), battute approvate (`BATTUTE_master.csv`, esiste), log LinkedIn (`_log/linkedin_azioni.csv`), registro del fermo (`_log/outreach_fermo.csv`) [verificato: DIRETTIVE §15; GESTIONE_POST.md §1]. Tutti quelli in `PUBBLICAZIONE/` e `_registri/` sono "da creare" [verificato: STATUS.md 22/10; ls].

Cartelle e file citati dai documenti ma assenti nel repository al 24/10 [verificato: `ls` di `_docs/` e `PUBBLICAZIONE/`]: `_docs/RUOLI.md` (chi ricopre ogni ruolo), `_docs/lavoro_direttive_21-10/` con `SINTESI_LETTURA.md` (la base di lettura delle direttive, citata in STATUS 22/10), `PUBBLICAZIONE/registro_si.csv`, `ledger.csv`, `numeri.csv`, `bozze_linkedin/`, `commenti_input/`, `commenti_pronti/`, `regole_commenti/`, `_registri/`, `ae/` (progetto After Effects). Un sistema di agenti che parte da queste direttive deve prima creare i registri, perché gli hook e lo script dei commenti li leggono come condizione per agire.

---

## 4. Cosa è fatto e cosa manca al 24/10/2026

### 4.1 Pubblicato (unici dati reali nei file)

| Data | Pezzo | Dove | Numeri | Fonte |
|---|---|---|---|---|
| 06/10 18:00 | CR03 "From brief to written verdict", carosello 8 slide EN, caption EN+IT | Instagram @sersan_ai + Facebook | reach 216, 312 visualizzazioni, 2 like, 1 condivisione (al 13/10) | [verificato: STATUS.md 06/10, 13/10] |
| 09/10 10:00 | TD2 "The forty-minute check", 10 slide scure | Instagram + Facebook | reach 19, 59 visualizzazioni, 3 like | [verificato: STATUS.md 13/10] |
| 13/10 11:00 | CR03 come documento PDF, primo post della Pagina | Pagina LinkedIn | non trovato | [verificato: STATUS.md 13/10] |
| 14/10, 16/10 | TD1 e TD3 caroselli | Instagram + Facebook | programmati il 08/10; esito e numeri **non trovati** | [verificato: PIANO_IG_PAGINA_09-22-10.md] |
| 15/10, 20/10, 22/10 | TD2, TD1, TD3 documenti PDF | Pagina LinkedIn | programmati; esito **non trovato** | idem |
| Settembre (prima del piano) | V01 reel del sito e un carosello del collega | Instagram | non nel progetto; comment-to-DM "Scrivici PROCESSO" ancora in bio al 13/10 | [verificato: CALENDARIO.md W01; STATUS.md 13/10] |

Lettura: i caroselli chiari (CR03) raggiungono molto più delle slide scure dei teardown (216 contro 19) [verificato: PDF p.167 C1]. Nessun post di testo dei founder risulta uscito, benché 22 testi siano pronti dal 06/10.

### 4.2 Pronto da pubblicare dopo il sì

In `PUBBLICAZIONE/PRONTI_SUBITO/` [verificato: ls]: CR03 EN e IT (8 PNG + PDF LinkedIn ciascuno), CR05 EN e IT (8 PNG + PDF), TD1, TD2, TD3 EN e IT (PDF finali, riquadro BOZZA tolto con diff pixel), slide IG di TD1-TD3 EN (10 PNG ciascuno), `POSTA_ORA.md` (22 post), `PIANO_AUTO.md` (23 post proposti, 07/10-04/11, mai attivato perché i profili dei founder non sono collegati), `PROFILI_BIO.md` (headline e About di Alessandro e Michele, tagline e About della Page, bio IG, EN e IT, da incollare a mano).

### 4.3 In bozza nel banco degli asset (stato al 03/10, unico inventario)

352 file media: 77 plate pronti (loop, hook, Sting B, DORA grid, set podcast, transizioni), 14 clip parlate AV03 (non pubblicabili), 2 clip di ascolto, 13 take audio, 136 immagini (19 pronte, 31 da approvare), 10 caroselli CR01-CR05 EN/IT (80 frame, chip BOZZA; CR1, CR2, CR4 con scene da rifare), 8 PDF + 8 PPTX dei teardown TD1-TD4 EN/IT [verificato: INVENTARIO_CONTENUTI.md §1]. Rough cut `video/reels_rough/` AV03-1 EN/IT v2 e AV03-3 EN v2: agli atti, non si pubblicano [verificato: CALENDARIO.md W06].

### 4.4 Manca o è bloccato

| Cosa manca | Cosa sblocca | Fonte |
|---|---|---|
| Pulizia D1 del sito (ruoli precedenti, "8 years senior delivery", "14 named projects", certificazione, fasce di budget su /start) | Link a sersan.io/start nei post, bio IG, About dei profili | STATUS.md 22/10; PDF p.3 |
| Provino di Alessandro (AV03-1-ALE-B03 IT ed EN) e D-18 | Via A/B, strumenti per sfondo e abiti, clip AV03, CL1, CL2 | README.md 13/10; DA_MONTARE.md §6 |
| Registrazione voce di Alessandro (PVC) e di Michele | Clip, podcast, trailer, episodi, AV02 | CALENDARIO.md; DA_MONTARE.md §5 |
| Sessione fonte registrata (nessuna al 13/10) | V11, V12, V13, V19, podcast E01-E05, Shorts | PDF p.5, p.64 |
| Crediti Higgsfield (1,56 fino al ~27/10; 3.000/mese Ultra) | Scene dei caroselli CR1, CR2, CR4; AV02 se generate (3.500-4.000 crediti) | STATUS.md; DA_MONTARE.md §5 |
| Montaggio in AE: progetto `ae/` da creare, template T03-T10, MCP locali assenti | V02 "Six refusals" (primo video, era previsto 08/10), hook 4:5, Sting B | DA_MONTARE.md §0; STATUS.md 22/10 |
| Collegamento dei profili LinkedIn dei founder (Metricool brand `founder_<nome>` o nativo) | 2+2 post a settimana, reshare della Page con menzione | GESTIONE_POST.md §3 |
| Account Publora, linkedin-skills installato, Story Bank e profilo di voce dei founder | Bozze automatiche del lunedì, commenti automatici | STATUS.md 22/10 |
| Workspace Team Higgsfield con posto per chi produce; posto Full ElevenLabs; utente Metricool proprio (piano Advanced per la revisione) | Lavoro di un nuovo addetto ai contenuti | STATUS.md 22/10 |
| Registri (`registro_si.csv`, `ledger.csv`, `numeri.csv`, `_registri/`) e `_docs/RUOLI.md` | Gate e numeri del lunedì | STATUS.md 22/10 |
| Owner di ledger, numeri del lunedì, community (D-14) | Riunione del lunedì, risposte entro un giorno | PDF p.9-10 |
| Nome dello show (D-05), canale YouTube, Spotify sì/no | Podcast | PUBBLICAZIONE/README.md |
| Copioni da inviare ai founder (8 punti aperti) | Sessioni di registrazione | COPIONI_PUNTI_APERTI |
| Slot vuoti dopo il 22/10 (Page) e il 16/10 (IG) | Continuità del feed | STATUS.md 22/10 |
| SerSanOutreach: migrazione Azure, prerequisiti legali (LIA, art. 14, List-Unsubscribe, blocco IT/DE), prime 100 righe della lista UK entro 06/11, primo invio 16/11 | Pipeline outbound | revised-plan.md §8; STATUS.md 22/10 |

### 4.5 Stato degli strumenti (22/10)

Higgsfield Ultra personale, 1,56 crediti; ElevenLabs grant aziendale (piano, slot PVC e licenza musica da leggere); moda secondario; Metricool brand `sersan_ai` con IG, FB, Page LinkedIn, accesso condiviso; LinkedIn automatizzato da installare; SerSanOutreach fermo dal 16/10; AE e Blender MCP assenti; repository GitHub privato dal 22/10; plugin pronto; sito non pulito; provino non girato [verificato: STATUS.md "Stato attuale degli strumenti (22/10/2026)"].

Premio Claude (stato al 13/10): Claude Team gratis 12 mesi fino a 5 posti Premium, crediti API mensili 100 $ per posto Premium con tetto 500 $ (maturazione sui posti gratuiti da verificare), 1.000 $ di API una tantum (scadenza 6 mesi o un anno), grant ElevenLabs 33M caratteri, offerta moda da verificare [verificato: STACK_STRUMENTI §2]. Il contesto di questo rapporto parla di "800 dollari al mese di crediti API": nei file del marketing la cifra non compare; da allineare [non verificato].

---

## 5. Dove un sistema di agenti può inserirsi

Premessa: le direttive del 22/10 definiscono già un sistema a ruoli con gate umani. Gli agenti si innestano **dentro quei ruoli**, non al posto dei sì. Vincoli che valgono per ogni agente [verificato: GESTIONE_POST.md §2, §8, §9; DIRETTIVE §2; STACK §4]:

1. Niente esce senza un sì umano scritto nel registro del sì; su Metricool scrive solo una sessione presidiata, mai Routines, task o loop; i quattro tool di scrittura restano su "Needs approval" più l'hook del plugin.
2. Volti e voci solo dei founder con consenso; mai testo o marchio generati nelle immagini; mai etichette AI (scelta del 22/10, vedi §2.9).
3. Commenti LinkedIn solo entro regole approvate dal titolare, con tetti e file di stop; inviti e DM solo da SerSanOutreach; mai comment-to-DM, mai post via Publora, mai reshare automatici, mai scraper senza ok scritto.
4. Numeri e fatti solo dalla Story Bank o dal claims register: "se un numero manca, togli la frase".
5. Routines e task desktop di Claude scrivono sui connettori senza chiedere: i connettori che scrivono restano fuori dagli agenti non presidiati.

### 5.1 Agente editoriale (idee dal CRM, dalle call e dai segnali)

| Voce | Contenuto |
|---|---|
| Input | Trascrizioni delle call di discovery e delle sessioni fonte (nel piano: Scribe v2 di ElevenLabs; il piano cita Granola "solo se i founder registrano le call" e Fireflies non compare) [verificato: STACK §2 "Altri connettori"]; `reply_digest` e `review_feedback` del MCP `sersan-outreach` (cosa scrivono i prospect, cosa rifiuta il revisore) [verificato: SerSanOutreach/mcp_server/README.md]; Story Bank dei founder; i 5 pilastri e il tetto "1 rifiuto su 10"; i commenti qualificati del ledger |
| Output | Proposte di tema per slot vuoti del calendario, con pilastro, voce, formato, evidenza (`evidence_paths` o riga della Story Bank), timecode se da una registrazione; "battute dal podcast" con timecode (automazione già stimata ~1,3 $/mese) [verificato: STACK §5] |
| Si innesta su | `calendario.csv` (stati), `scripts/_BRIEF.md` (regole e banca asset), `W2 content-atomise` del vault (una fonte → 8 post LinkedIn, 1 newsletter, 10 clip spec, cap a 8 post per episodio, claim nei primi 180 caratteri, chiudere con un'affermazione non con una CTA, scarto automatico dei post senza evidenza) [verificato: V2/06-automation/stack-and-rag.md §9 W2] |
| Gate umano | Alessandro sceglie i temi; Michele firma ogni claim tecnico |
| Rischio noto | "Fatti inventati" e "critico indulgente" (STACK §5); la lista dei 200 account e il tempo nei commenti e nei DM non si automatizzano mai [verificato: V2 stack-and-rag §9 "Cosa NON si automatizza"] |

### 5.2 Agente copy per piattaforma

| Voce | Contenuto |
|---|---|
| Input | Tema approvato, pilastro, voce, Story Bank, glossario B6 del brief, regole §2 e §11 delle direttive |
| Output | Bozza EN + `· · ·` + IT per LinkedIn (3.000), Instagram (2.200, alt text EN, max 3 hashtag), YouTube (titolo 100, descrizione 5.000 con capitoli), con contatore `len()`, "BOZZA da approvare" in testa, marcatori `[CHECK MICHELE]` dove serve |
| QA automatica (lint deterministico, già descritto nelle direttive) | zero `!`, emoji, URL, @menzioni, "IA", parole vietate, parole di disclosure ("AI-generated", "avatar", "synthetic", "generato"), CTA una volta per lingua, hashtag nei limiti, nessun rimando a pezzi assenti, marcatori tolti [verificato: GESTIONE_POST.md §6; DIRETTIVE §11] |
| QA avversaria | "Caption con QA avversaria: bozza Sonnet, critica Opus con regole in cache, 120 caption ~6,5 $/mese" e confronto testo-grafica da una seconda sessione indipendente [verificato: STACK §5; DIRETTIVE §11] |
| Si innesta su | `linkedin-skills` (planner, writer, humanizer con profilo di voce) per i post dei founder; `posts/captions/*.md` e `SETTIMANA.md` come destinazione; `BATTUTE_master.csv` per le battute parlate |
| Gate umano | Sì scritto di chi approva i testi e firma tecnica; il founder per il suo profilo |

### 5.3 Agente visual e video

| Voce | Contenuto |
|---|---|
| Input | Testo approvato, ID slot, pilastro, palette, banca asset (`_BRIEF.md` sezione I), registro dei consensi |
| Output | Scene senza testo (`#W57`, `#W80`), caroselli con `build.py` (JSON → PNG → `qa.json`), teardown con `kit/build_deck.py`, thumbnail (`#W78`), b-roll e loop (`#W56`), varianti (`#W55`), scontorni e SRT (`#W49`), pacchetto di consegna al montaggio (cartella `<data>_<ID>/00..07` e nota di consegna) [verificato: DIRETTIVE §9, §10, §14] |
| Si innesta su | Plugin `contenuti-sersan` (etichette `#Wnn`, router), `specs_tool.py add/done` per il log, `build_docs.py`, `review_video.py`/`contact_sheet.py`, catalogo HyperFrames (`npx hyperframes catalog`) |
| Limiti strutturali | Montaggio, composito e finali li fa "chi monta" su un PC con AE, Blender e TX Library: oggi quel PC è di Alberto e i server MCP locali sono assenti; la via A sui founder è "solo a mano" per A1 e B3; costi senza preflight (`upscale_video`, `remove_background`, `execute_preset`, `dubbing`) [verificato: DIRETTIVE §4 "Route bloccate", §6, §16] |
| Gate umano | Provino giudicato alla cieca; sì sulla bozza resa; QA §13 |

### 5.4 Agente di pubblicazione e programmazione

| Voce | Contenuto |
|---|---|
| Input | Lista da approvare (data, ora, rete, profilo, testo esatto, file, alt, primo commento, titolo documento) e la riga del registro del sì con l'id Metricool della bozza |
| Output | Bozze (`draft:true`) prima del sì; dopo la riga del sì, `createScheduledPost` o `createScheduledPostForReview` (Advanced); controllo con `getScheduledPosts`; riga nel ledger con `publicUrl`; aggiornamento di `calendario.csv` (stato PUBBLICATO) [verificato: GESTIONE_POST.md §7, §8] |
| Si innesta su | Connettore MCP Metricool (tutti i piani; revisione solo Advanced/Custom; Free 20 post al mese e niente LinkedIn) [verificato: STACK §2 "Metricool"]; hook `metricool-ask.js`; storage Higgsfield per gli URL pubblici dei media (il repository è privato) |
| Cosa resta a mano | Collegamento degli account e login dei founder, bio, nome e About, reshare della Page, checkpoint e CAPTCHA, storie con sticker, caroselli oltre 10, reel con audio fuori libreria, YouTube con AI toggle [verificato: GESTIONE_POST.md §5, §12] |
| Modalità ammessa | Sessione presidiata; l'agente prepara, un umano conferma ogni scrittura. Una Routine o un task non può pubblicare [verificato: GESTIONE_POST.md §2.5] |

### 5.5 Agente di analisi delle metriche

| Voce | Contenuto |
|---|---|
| Input | `getAnalyticsDataByMetrics` di Metricool (codici in §2.8), ledger, calendario, `_log/linkedin_azioni.csv`, `kpi_overview`/`growth_overview`/`campaign_scoreboard` del MCP `sersan-outreach` [verificato: SerSanOutreach/mcp_server/README.md] |
| Output | "Digest analytics: task Cowork il lunedì, Metricool in sola lettura, 0 $ API" con i grezzi allegati (regola: "numeri inventati: allegare i grezzi") [verificato: STACK §5]; `numeri.csv` compilato; lettura del criterio di stop per i pezzi founder-AI; verdetto formati vincenti (reel vs carosello, temi LinkedIn) secondo la regola fissata prima della misura; i 10 numeri del lunedì |
| Gate umano | Decide Alessandro; "campione piccolo: la lettura è direzionale, ma lo stop scatta alla lettera" [verificato: revised-plan.md §11] |
| Limite | Metricool non copre inbox, commenti, campagne Ads; i profili dei founder non sono collegati, quindi i loro numeri non arrivano finché non lo sono [verificato: STACK §2] |

### 5.6 Loop con l'outbound (post → lead → SerSanOutreach)

Cosa c'è già nei documenti e nel codice:

- **Dal post al lead**: i commenti qualificati "da titoli ICP" sono il numero 4 del lunedì; il venerdì "5-10 nomi nuovi con trigger documentato per l'outreach" [verificato: revised-plan.md §6 "Il flusso settimanale"]. Prima di commentare un post si controlla in `/leads/` di SerSanOutreach che l'autore non sia in una sequenza attiva [verificato: GESTIONE_POST.md §9 "Testi da commentare"].
- **Segnali d'intento** (W5 `intent-watch` del vault): Companies House, pagine `/careers`, feed di funding, stack detection; ≥2 segnali → watchlist, Slack solo a 3+; la lista dei 200 account resta a mano [verificato: V2 stack-and-rag §9 W5]. Nel piano del 26/09 il CRM Attio è sostituito da SerSanOutreach [verificato: revised-plan.md §3 D11].
- **Dal lead al messaggio**: SerSanOutreach genera l'icebreaker con Claude (step 1 su segnale Perplexity), HITL su ogni invio, Instantly per l'email; MCP `sersan-outreach` (sola lettura: KPI, varianti A/B, feedback del revisore, `reply_digest`) e `sersan-operator` (approva o rifiuta con `fingerprint`) [verificato: SerSanOutreach/README.md; mcp_server/README.md; GESTIONE_POST.md §10]. Gli step email "scritti dall'AI" restano spenti nel piano: solo template approvati da Alessandro [verificato: revised-plan.md §3 D11].
- **Dal lead al contenuto**: le risposte della Unibox e i motivi di rifiuto del revisore (`review_feedback`) sono materia per l'agente editoriale (obiezioni ricorrenti → FAQ "Prima di inviarci un brief", teardown).
- **Dal sito al CRM**: "Intake brief su sersan.io: Messages API + tool use, 0,09-0,13 $ a conversazione, si dichiara assistente virtuale; rischio prompt injection e promesse di prezzo" (gate 4, 09/11, solo con ok dei founder) [verificato: STACK §5, §6]. Il sito promette "a founder reads it" e risposta "within one business day": l'agente può qualificare, non rispondere al posto del founder [verificato: revised-plan.md §6 "Chi decide"].

Divieti espliciti del loop: nessun avatar o voce sintetica in DM, commenti, outreach o call; nessun invito o DM fuori da SerSanOutreach; i dati raccolti dalla vecchia automazione dei commenti non si riusano [verificato: revised-plan.md §3 D14 regola 4; GESTIONE_POST.md §9; COPIONI_PUNTI_APERTI "Ancora aperti dal 01/10"].

### 5.7 Dal vault: idee riusabili, non basi

- Il vault del 25/08 ha già scelto "corpus markdown versionato + retrieval agentico (grep) per gli umani e Claude Code; pgvector su Supabase solo per i chiamanti macchina; n8n come MCP Server Trigger così i workflow diventano tool di Claude Code; Notion come coda di approvazione" [verificato: V2/06-automation/stack-and-rag.md §0, §8]. È la stessa impostazione "secondo cervello" del contesto di questa presentazione, già argomentata per SerSan.

### 5.8 Corrispondenza con la lista di controllo della visione (file `00-visione-funzionalita.md`)

Le voci della visione di Alberto che toccano marketing e contenuti, e cosa esiste già in SerSan per coprirle [verificato: `C:/Users/alber/SerSan-AgentOS/ricerca/00-visione-funzionalita.md`; fonti SerSan come indicato]:

| Voce della visione | Cosa c'è già in SerSan | Agente di questo rapporto | Cosa manca |
|---|---|---|---|
| A1, C2, C5: ogni riunione trascritta e analizzata (Fireflies) | Il piano prevede Scribe v2 di ElevenLabs per podcast e sessioni fonte; Granola "solo se i founder registrano le call di discovery"; Fireflies non compare [verificato: STACK §2; DIRETTIVE §8 C5] | 5.1 editoriale (input) | Registrazione dichiarata delle call di vendita e di discovery; oggi nessuna sessione fonte registrata |
| A7: chat condivisa fra agenti | Nulla di equivalente; i canali umani sono Teams o email per la consegna al montaggio [verificato: DIRETTIVE §14 "Canale"] | Tutti | Canale comune leggibile dagli umani (il vault proponeva Slack `#inbound` per gli alert) [verificato: V2 stack-and-rag §9 W1] |
| B1-B4: post-call → Slack, CRM, mail di follow-up, to-do | SerSanOutreach ha deal, meeting, Unibox e `reply_digest`; nessun agente post-call [verificato: SerSanOutreach/mcp_server/README.md] | 5.6 loop outbound; 5.1 editoriale (obiezioni → temi) | Il collegamento call → CRM → contenuti; HITL su mail e to-do |
| C1: debrief del mattino | "Numeri del lunedì" e digest Cowork in sola lettura da Metricool, settimanale, non quotidiano [verificato: GESTIONE_POST.md §11; STACK §5] | 5.5 metriche | Un digest quotidiano che unisca Metricool, ledger, SerSanOutreach e calendario |
| D2, D4: brief pre-meeting e slide automatiche | Claude Slides e Design per i deck dei founder (dal Team, a richiesta); moda.app secondario [verificato: DIRETTIVE §10; STATUS 22/10] | 5.3 visual (deck) | Il brief pre-meeting non è nei file del marketing (è materia di SerSanOutreach e del CRM) |
| G2, G8: fit score e analisi delle lead chiuse, con i risultati passati al marketing | `review_feedback`, `kpi_overview`, `campaign_scoreboard` del MCP `sersan-outreach` [verificato: mcp_server/README.md] | 5.5 metriche; 5.6 loop | La regola scritta che porta i motivi di rifiuto e le obiezioni dentro il calendario editoriale |
| G5-G7: agente vocale che richiama le lead | Vietato dalle regole di casa per i founder: "mai in DM, commenti, outreach o call" un volto o una voce fatti con AI [verificato: revised-plan §3 D14 regola 4] | – | Decisione dei CEO: un agente vocale con voce dichiarata e non dei founder è fuori da ogni documento SerSan |
| E3: policy AI e banca dei token | Regola del 22/10 "budget senza limiti, non serve approvazione", ma costo letto prima di ogni generazione (`get_cost:true`, `estimate_only:true`) e nessun tetto sul MCP Higgsfield [verificato: DIRETTIVE §16; STACK §7] | 5.3 visual | Una policy per persona e per agente; un contatore comune dei crediti |
| H6: premio mensile a chi costruisce con l'AI | Non nei file | – | Decisione dei CEO |
| I3: aree dove l'AI non si usa di proposito | Già scritte: tempo nei commenti e nei DM, lista dei 200 account, voce vera dei founder, firma tecnica di Michele, sì umano su ogni uscita [verificato: V2 stack-and-rag §9; GESTIONE_POST.md §2, §9] | Vincolo per tutti | Da ribadire nel documento ai CEO come scelta, non come limite tecnico |
| I4: ribaltare il rapporto nel marketing, dove presentazioni, Excel e mail prendono gran parte del tempo | Il piano stima il tempo delle persone come 67% del costo del go-to-market (vault) e circa 195-226 h di Alberto in 12 settimane [verificato: V2/00-MASTER-PLAN.md §6; PDF p.6] | Tutti | Misura del tempo risparmiato: oggi non c'è un foglio delle ore effettive |

---

## 6. Strumenti e abbonamenti per pubblicare in automatico

Solo nomi e requisiti (i prezzi li valuta un altro agente). "Nei file" = citato nei documenti SerSan; altrimenti [non verificato] e da controllare sulle pagine ufficiali prima di decidere.

| Strumento | Cosa fa | Cosa richiede | Nei file |
|---|---|---|---|
| **Metricool** (in uso) | Programmazione e analytics di Instagram, Facebook, Pagina LinkedIn, YouTube e altri; MCP su tutti i piani; revisione a più occhi ("Send for review") solo su Advanced o Custom; Free: 20 post al mese e niente LinkedIn | Account aziendale; un utente per persona (Advanced); profili personali LinkedIn collegati con il login del founder; media come URL pubblici | [verificato: STACK §2; GESTIONE_POST.md §3, §7, §8] |
| **Buffer** (riserva) | Bozze e coda; MCP gratuito; senza analytics | Account | [verificato: STACK §2 "Alternativa: Buffer MCP"] |
| **Publora** | API di pubblicazione su LinkedIn usata da `linkedin-skills`; per SerSan solo commenti, risposte e reazioni (i post "mai via Publora") | Account aziendale, chiave API in `~/.publora/publora.env`, OAuth del titolare, `platform_id` | [verificato: GESTIONE_POST.md §3, §9] |
| **linkedin-skills** (plugin Claude Code, sergebulaev) | Story Bank, profilo di voce, planner, writer, humanizer, comment drafter, reply handler; tier 1 pubblica via Publora | Installazione da marketplace; niente `APIFY_TOKEN` né `PIXFARO_TOKEN`; non eseguire `test_detectors.py` | [verificato: GESTIONE_POST.md §9] |
| **SerSanOutreach** (interno) | Inviti, DM, follow-up, email via Instantly, HITL; MCP `sersan-outreach` e `sersan-operator` | Utente `operator`/`is_staff`, chiave `~/.sersan/api_key`, Chrome del titolare con estensione, Instantly | [verificato: GESTIONE_POST.md §10; SerSanOutreach/README.md] |
| **Instantly.ai** | Invio email, warmup, rotazione domini, webhook | Account, mailbox con SPF/DKIM/DMARC, DPA nel registro dei subprocessori | [verificato: SerSanOutreach/README.md; revised-plan.md §8] |
| **LinkedIn API** (Community Management / Marketing Developer Platform) | Pubblicazione su Page e profili via app approvata; LinkedIn "vuole l'intervento umano prima della pubblicazione automatica" | App LinkedIn, approvazione del programma partner, permessi `w_member_social`/`w_organization_social`, OAuth del membro o admin della Page | Avvertenza [verificato: STACK §7 fonte 40]; dettagli dei permessi [non verificato] |
| **Instagram Graph API / Content Publishing** | Pubblicazione di post, caroselli e reel su account Business/Creator; limite 100 post via API in 24 ore (caroselli: leggere `content_publishing_limit`) | Account Business o Creator collegato a una Pagina Facebook, app Meta con revisione, token di lunga durata | Limite [verificato: STACK §5 fonte 39]; requisiti dell'app [non verificato] |
| **YouTube Data API** | Upload, metadati, playlist, Shorts | Progetto Google Cloud, OAuth del canale, quota giornaliera, verifica dell'app per gli scope sensibili | [non verificato] |
| **Postiz** (self-host) | Scheduler open source multi-piattaforma, API, ospitabile sul server SerSan | Server (Docker, Postgres, Redis), app OAuth per ogni rete (LinkedIn, Meta, YouTube), dominio pubblico per i callback | [non verificato] |
| **Mixpost** (self-host, PHP/Laravel) | Scheduler self-host multi-piattaforma | Server, app OAuth per rete | [non verificato] |
| **Ayrshare / Late / SocialClaw** | API unificate di pubblicazione su più reti con una sola chiave (la skill `socialclaw` di questa sessione dichiara 13 piattaforme, X, LinkedIn, Instagram, Facebook Pages, TikTok, YouTube, Reddit, WordPress, Pinterest) | Account sul servizio, collegamento OAuth dei profili, chiave API; sono subprocessori di terzi da dichiarare | SocialClaw [verificato: elenco skill della sessione]; gli altri [non verificato] |
| **Rube MCP (Composio)** | Skill `linkedin-automation`, `youtube-automation`, `instagram`, `tiktok-automation` presenti in questa sessione: creano post, caricano video, leggono analytics via Composio | Account Composio e collegamento OAuth dei profili | [verificato: elenco skill della sessione; funzionamento non provato] |
| **Higgsfield TikTok** | Il connettore Higgsfield espone `tiktok_connect`, `tiktok_prepare_publish`, `tiktok_publish_status` | TikTok è parcheggiato nei 90 giorni | [verificato: elenco tool della sessione; PUBBLICAZIONE/README.md] |
| **n8n (self-host)** | Orchestrazione; nodo MCP Server Trigger per esporre i workflow come tool a Claude Code; nodi per LinkedIn, Meta, YouTube | VPS/server con Docker, Postgres, Caddy; licenza Community | [verificato: V2/06-automation/stack-and-rag.md §0, §7-§8] |
| **Claude Team: Routines e task desktop** | Routines (anteprima) richiedono un repo GitHub, girano al massimo ogni ora, usano tutti i connettori e scrivono senza chiedere; task desktop girano a PC acceso con MCP locali | Per regola SerSan: solo lettura, mai scritture su Metricool | [verificato: STACK §2 "Automazione", §4] |
| **Notion** o **Google Drive** | Calendario editoriale e coda di approvazione | Connettore d'organizzazione; Notion qui richiede autenticazione | [verificato: PDF p.169; avviso di sessione] |
| **ElevenLabs, Higgsfield, moda, HyperFrames, After Effects** | Produzione, non pubblicazione (vedi §3) | – | [verificato] |

Vincoli di policy che pesano su qualsiasi scelta: su LinkedIn "zero automazione" era la regola del 25/08 e il software di outreach dichiara di violare i termini di LinkedIn; il 22/10 Alberto ha ammesso i commenti automatici entro regole e tetti; i tool di terzi sui profili personali erano vietati dal piano del 26/09 ("nessuna credenziale condivisa, nessun tool di terzi sui profili personali") e oggi il brand Metricool `founder_<nome>` è previsto solo con il login del founder presente [verificato: V2/03-channels/linkedin.md §1; revised-plan.md §8 prerequisito 1; STATUS.md 22/10; GESTIONE_POST.md §3].

---

## 7. Domande aperte per i CEO

1. Chi tiene ledger, numeri del lunedì e community mentre Matteo è assente (D-14), e il nuovo "addetto ai contenuti" per cui sono state scritte le direttive del 22/10 è una persona o il sistema di agenti?
2. Si mantiene la regola "niente etichette AI" delle direttive del 22/10, in contrasto con il piano del 26/09 (D14) e con il vault del 25/08? Pesa su ogni agente che tocca i toggle delle piattaforme e sull'art. 50(4) citato dal piano.
3. I profili LinkedIn personali dei founder: nativi per sempre, Metricool con login del founder, o API ufficiale? Senza una risposta il motore 2+2 non parte e gli agenti di pubblicazione servono solo alle superfici aziendali.
4. Esito dei gate 1 (19/10) e 2 (26/10): grant ElevenLabs utilizzabile, piano Metricool, calendario su Notion o Drive, via A o B, voce master.
5. Data della pulizia D1 del sito: senza, nessun link e nessuna CTA "il link è nel profilo".
6. Crediti API Anthropic: 1.000 $ una tantum più crediti mensili (STACK) o "800 $ al mese" (contesto di questa presentazione)?
7. SerSanOutreach: la migrazione è su Azure (STATUS 22/10) mentre il contesto dice "verrà spostato sul server fisico": qual è la destinazione, e con quali prerequisiti legali chiusi (LIA, art. 14, opt-out EN, blocco IT/DE)?
8. Dove archiviare girato e registrazioni originali dei founder (oggi `_ref/` ha solo file WhatsApp) e come registrare le prove con strumenti fuori stack.
9. Il podcast: registrato insieme (copioni del 14/10) o battute alternate senza dialogo (brief regola 9)? Il brief va aggiornato prima di mandare i copioni.
10. Spotify, nome dello show, canale YouTube: decisioni scadute il 16/10 e il 23/10 senza esito nei file.

---

## 8. Allegati consigliati

- `C:/Users/alber/Documents/SERSAN-marketing/_docs/SERSAN-Piano-marketing-90-giorni.pdf` (piano, 175 pagine)
- `C:/Users/alber/Documents/SERSAN-marketing/_docs/DIRETTIVE_CONTENUTI.md` (direttive per chi produce)
- `C:/Users/alber/Documents/SERSAN-marketing/_docs/GESTIONE_POST.md` (direttive per chi pubblica)
- `C:/Users/alber/Documents/SERSAN-marketing/PUBBLICAZIONE/CALENDARIO.md` e `calendario.csv` (calendario W01-W13)
- Utili in più: `_docs/STATUS.md` (stato al 22/10), `_docs/STACK_STRUMENTI_2026-10-13.md` (strumenti e automazioni), `_docs/INVENTARIO_CONTENUTI.md` (banco asset), `PUBBLICAZIONE/PRONTI_SUBITO/POSTA_ORA.md` (22 post pronti), `scripts/_BRIEF.md` (brief editoriale), `_plugin/contenuti-sersan/hooks/contesto-sessione.md` (regole in 4.000 caratteri).
