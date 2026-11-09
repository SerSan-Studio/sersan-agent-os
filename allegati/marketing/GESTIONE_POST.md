% Gestione dei post
% Metricool, LinkedIn automatizzato e SerSanOutreach: dalla bozza approvata ai numeri · versione del 22 ottobre 2026
% Da approvare

# 1. Come usare questo documento

Per chi gestisce i post e chi approva. Per produrre i contenuti: «Direttive per generare contenuti» (`_docs/DIRETTIVE_CONTENUTI.md`).

Due strade: **A mano** nell'app o sul sito; **Con Claude Code** con i tool MCP indicati e il plugin `contenuti-sersan`.

Percorsi relativi alla radice del repository condiviso `SerSan-AI-Studio/SERSAN-marketing`: clone, `git pull` prima di lavorare, commit e push dopo, come nel §3 delle Direttive. `_ref/` non è nel repository. Controlla lo stato attuale degli strumenti in `_docs/STATUS.md`.

## Ruoli

Chi ricopre ogni ruolo è in `_docs/RUOLI.md`; se manca, chiedilo all'amministratore degli strumenti.

- **Chi gestisce i post**: lista, programmazione, controlli, registri, numeri.
- **Chi approva i testi**, **chi firma la parte tecnica**, **chi autorizza la pubblicazione**, **il founder**: i sì del §2.
- **Il titolare dell'account LinkedIn**: collega l'account, approva le regole dei commenti e il pilota, risolve i checkpoint.
- **Operatore e staff di SerSanOutreach**: l'operatore approva inviti e DM; lo staff gestisce pilota, stop e rientro.
- **L'amministratore degli strumenti** (accessi, chiavi, autorizzazioni); **il responsabile del toolchain** (plugin, hook, script).

## Glossario

- **Registro del sì**: dove scrivi ogni approvazione prima di agire.
- **Ledger**: una riga per pezzo; `via` vale `reale`, `A` o `B` (Direttive).
- **Lista da approvare**: i post esatti di un periodo (§6).
- **Sessione presidiata**: Claude Code aperto da te, con te al PC.
- **Brand Metricool**: gruppo di account con un solo account LinkedIn.
- **Tier di linkedin-skills**: 0 bozze; 1 Publora (qui solo commenti, risposte, reazioni).
- **Pilota**: configurazione degli invii automatici di SerSanOutreach (`/pilot/`).

## Registri

Se un file manca, crealo con queste colonne; non cancellare righe.

| Registro | File | Colonne |
|---|---|---|
| Registro del sì | `PUBBLICAZIONE/registro_si.csv` | data, cosa, ruolo, canale, testo del sì, riferimento |
| Ledger | `PUBBLICAZIONE/ledger.csv` | pezzo, canale, via, voce, esito, link, etichette automatiche |
| Foglio dei numeri | `PUBBLICAZIONE/numeri.csv` | settimana, pezzo, rete, metrica, valore |
| Log LinkedIn | `_log/linkedin_azioni.csv` | data e ora, account, URL, tipo, testo, esito |
| Registro del fermo | `_log/outreach_fermo.csv` | data e ora, account, profilo, canale, evento, classificazione, link |

# 2. Regole che valgono sempre

1. Due livelli di approvazione:
   - contenuto: sì ai testi EN e IT di chi approva i testi, o del founder per il suo profilo; firma tecnica su affermazioni e PDF tecnici;
   - programmazione: sì di chi autorizza la pubblicazione sulla lista esatta (§6).
2. Senza la riga del sì nel registro non programmi niente. Fino al sì il testo resta «BOZZA da approvare».
3. Brand:
   - EN, riga `· · ·`, IT, nello stesso post; CTA una volta per lingua: «Send a project brief.» / «Inviaci un brief di progetto.»;
   - niente prezzi, punti esclamativi, emoji; «AI», mai «IA»;
   - vietati: compliant, compliance-ready, certified, conforme, certificato, «3am», «two people», «due persone», «SERSAN AI», numeri dei ruoli precedenti dei founder;
   - hashtag: al massimo 3 su Instagram, zero su LinkedIn e YouTube; nessun link su LinkedIn, nella caption Instagram e nel primo commento;
   - nessuna etichetta AI, disclaimer o C2PA aggiunto; interruttori AI spenti (§7), anche se una skill dice il contrario; non serve togliere i metadati.
4. Usa solo il tuo accesso. Login e «Connect» li fa il titolare; Claude non inserisce password.
5. Metricool solo da una sessione presidiata: prima del sì solo bozze, dopo la riga del sì la programmazione. Mai da Routines, task programmati o loop.
6. Su LinkedIn l'automazione resta entro le regole approvate dal titolare (§9).

# 3. Accessi e account

## Metricool

- Entra con l'accesso aziendale che ti dà l'amministratore degli strumenti.
- Brand `sersan_ai`: Instagram, Pagina Facebook, Pagina LinkedIn (la collega un Super Admin della Pagina).
- Profilo di un founder: crea il brand `founder_<nome>` e apri il collegamento di LinkedIn, profilo personale; il founder, presente, fa il login e concede l'accesso, senza ricevere l'accesso a Metricool. Controlla con il §7, passo 1.

## Publora

- L'amministratore degli strumenti apre un account Publora aziendale; la chiave API sta solo in `~/.publora/publora.env`, sul PC che pubblica.
- Il titolare collega il suo profilo dal pannello di Publora con OAuth, facendo lui il login. Il platform_id (`linkedin-...`) è nel pannello o in `GET /platform-connections`: scrivilo nelle regole (§9).

## SerSanOutreach

- Chiedi allo staff un utente su `https://outreach.sersan.io`: `operator` per approvare; `is_staff` solo per cockpit e `/pilot/`.
- **Con Claude Code**: lo staff ti dà la tua chiave (`~/.sersan/api_key`, mai quella dell'agenzia) e i comandi per installare `sersan-outreach` e `sersan-operator`.
- L'account che invia lo collega il titolare in `/linkedin/connect/`, dal suo Chrome con l'estensione.

## Controllo iniziale

A ogni nuovo accesso e cambio di piano controlla:
1. Metricool, Plan and Billing: con Advanced o Custom usa la revisione (§7, passo 7) e un utente per persona; con Starter saltala. Two-factor authentication attiva (Account settings > Access), login con email aziendale.
2. Pagina LinkedIn «SERSAN», tagline e About approvati; bio Instagram approvata.

# 4. Settimana tipo e calendario

Ora italiana.

| Giorno | Cosa |
|---|---|
| Lunedì | Numeri (§11), orari, coda, bozze LinkedIn (§9) |
| Martedì | Founder dal suo profilo; Pagina LinkedIn 11:00; Instagram e Facebook 10:00 |
| Mercoledì | Sì sulla settimana successiva; reshare della Pagina |
| Giovedì | Come martedì |
| Venerdì | Instagram e Facebook 10:00 (reel con persona); YouTube |

- Un post al giorno per profilo, anche nel feed Instagram; un reel con un founder sostituisce un suo post.
- Tieni almeno due settimane di pezzi PRONTI nel calendario.
- Reshare, solo a mano, con il testo riscritto approvato nella lista come post a sé: a +24 h, dalla Pagina, sul post del founder, «Repost» > «Repost with your thoughts»; «Notify employees» una volta a settimana.
- Calendario (`PUBBLICAZIONE/calendario.csv`): aggiorna `stato` (DA PRODURRE, DA MONTARE, DA APPROVARE, PRONTO, BLOCCATO, TAGLIATO, PUBBLICATO); se sposti una data, sposta i post che la citano. **Con Claude Code** confrontalo con `getScheduledPosts`.

# 5. Specifiche per rete

| Rete e formato | Misura | Limiti |
|---|---|---|
| LinkedIn immagine | 1080x1350 o 1080x1080 | testo 3.000 caratteri |
| LinkedIn documento | PDF 1080x1350, pagine uguali | 300 pagine, 100 MB; titolo; niente alt |
| LinkedIn video | 4:5 o 9:16, MP4 | 3 s-15 min; SRT EN e IT da desktop |
| Instagram post, carosello | 1080x1350 sRGB, JPEG o PNG 8 MB | 10 slide EN via Metricool; alt EN |
| Instagram reel, storie | 1080x1920; reel H.264, 23-60 fps | copertina 9:16; storie 3-60 s |
| YouTube | 16:9; thumbnail 1280x720 | titolo 100, descrizione 5.000 |

- **Instagram**: testo 2.200; alt e primo commento solo nel feed. A mano: storie con link, menzioni o sticker; caroselli oltre 10; reel con audio fuori dalla libreria di Metricool.
- **Facebook**: stesso post e formati di Instagram; reel 3-90 s (più lunghi a mano).
- **YouTube**: almeno 3 capitoli, il primo a 00:00, ognuno di almeno 10 s; SRT EN e IT come file. Shorts 9:16 fino a 3 min (60 s con musica non dell'Audio Library), con «Related video».
- **TikTok, X, Threads**: non collegarli senza l'ok dell'amministratore degli strumenti.

# 6. Dalla bozza alla lista da approvare

## Cosa contiene

Solo pezzi PRONTI, con i finali in `PUBBLICAZIONE/` (`<SLOT_ID>_<EN|IT>_<ratio>.<ext>`; slide `<SLOT_ID>_EN_<ratio>_01.png`). Per ogni post: data e ora, rete e profilo, testo esatto con caratteri e limite, file, alt text, primo commento, titolo del documento LinkedIn.

## Controlli sui testi

- Testo identico all'approvato e sotto il limite: **A mano** con il contatore dell'editor di Metricool; **Con Claude Code** con `len()`.
- Zero punti esclamativi, emoji, URL, @menzioni, «IA», parole vietate (§2) e di disclosure: «AI-generated», «generated», «avatar», «synthetic», «generato», «generata».
- CTA una volta per lingua; hashtag nei limiti; nessun rimando a pezzi assenti o successivi; tolti `[CHECK …]`, `[NATIVE IT]`, `[DECISION …]` e i segnaposto.
- **Con Claude Code**: confronta testi e finali da una seconda sessione.

## Chiedere e registrare il sì

1. Entro il mercoledì della settimana prima manda la lista per iscritto a chi autorizza la pubblicazione; per una settimana intera basta un messaggio.
2. Nel registro del sì scrivi una riga per post: in `cosa` pezzo, rete e profilo, data e ora; in `riferimento` l'id Metricool della bozza. Senza ruolo, data o canale vale non approvato.
3. Se dopo il sì cambi testo, data, ora o file, chiedi un nuovo sì.

# 7. Metricool passo per passo

| Passo | A mano (app.metricool.com) | Con Claude Code (§8) |
|---|---|---|
| 1. Reti collegate | Planning: icone delle reti del brand | `getBrandSettings` |
| 2. Orario | Planning > «Best times», per rete | `getBestTimeToPostByNetwork` |
| 3. Nuovo post | Planning: crea un post, scegli le reti, incolla il testo | `createScheduledPost` |
| 4. Media | Da `PUBBLICAZIONE/`, Google Drive o Dropbox | URL pubblici in `media` |
| 5. Alt text, primo commento | Alt per immagine; commento vuoto | `mediaAltText`, `firstCommentText:""` |
| 6. Documento LinkedIn | Icona documento > PDF, con il titolo | PNG in `media`, `linkedinData` |
| 7. Revisione (Advanced, Custom) | «Send for review», revisori, criterio | `createScheduledPostForReview` |
| 8. Bozza o programmazione | «Save as draft» prima del sì; «Schedule» dopo | `draft:true` prima; `draft:false`, `autoPublish:true` dopo |
| 9. Controllo | Calendario: data, ora, rete, testo; filtro «Error» | `getScheduledPosts` |
| 10. Dopo l'uscita | Copertina, slide, testo, accenti; difetti: §13 | `PUBLISHED`, `publicUrl` |
| 11. Registrazione | Ledger: «Esito: PUBBLICATO il <data>, link <url>» | Claude scrive la riga |

Revisione:
- Revisore: chi autorizza la pubblicazione (utente del brand o esterno via email); criterio «One approval is enough» o «Everyone must approve», mai «Auto-approve if no one rejects».
- Mandalo in revisione almeno 24 h prima: se all'ora di uscita non è approvato, attende 3 ore, poi non esce.
- Ogni modifica azzera la revisione; un rifiuto blocca il post. Correggi da Review requests > Rejected > View configuration > Notes e rimandalo.

## Interruttori AI spenti

- Instagram: editor del post > Instagram Presets > «AI-generated content» spento.
- YouTube: programma dal web e lascia spento «AI generated or altered content» (`youtubeData.isAiGeneratedContent` false o assente); in YouTube Studio, Attributes > «AI use» = No.
- LinkedIn: non usare l'opzione «self-attest».

## Errori frequenti

- Post di un profilo LinkedIn non uscito: profilo non collegato; fai sempre il passo 1.
- Accenti storti nel terminale: il file è giusto; passa a Metricool i caratteri veri (–, ·, è).

# 8. Metricool con Claude Code

## Quando

Solo da una sessione presidiata; programmi solo dopo il sì (§2). Autentica il connettore con il tuo accesso (Customize > Connectors > Metricool) e caricane i tool con ToolSearch («Metricool»).

## Strumenti

Tool: quelli del §7 e di «Protezioni sulle scritture»; id del brand (`blogId`, `brandId`) da `getBrandSettings`. Carosello Instagram più Facebook (`info` è una stringa JSON):

```
blogId: "<id del brand>"
date:   "2026-11-03T10:00:00+01:00"
info:
{
  "autoPublish": true,
  "draft": false,
  "providers": [{"network": "instagram"}, {"network": "facebook"}],
  "publicationDate": {"dateTime": "2026-11-03T10:00:00", "timezone": "Europe/Madrid"},
  "text": "<testo EN>\n\n· · ·\n\n<testo IT>",
  "media": ["https://<url>/<SLOT_ID>_EN_<ratio>_01.png", "..."],
  "mediaAltText": ["F01: <titolo>. <descrizione>", "..."],
  "firstCommentText": "", "shortener": false, "smartLinkData": {"ids": []}, "descendants": [], "hasNotReadNotes": false,
  "instagramData": {"type": "POST", "isAiGenerated": false},
  "facebookData": {"type": "POST"}
}
```

- `date`: +02:00 con l'ora legale, +01:00 con l'ora solare. `publicationDate.timezone` resta `Europe/Madrid`: stessa ora di Roma.
- Documento sulla Pagina LinkedIn: `providers` linkedin, `mediaAltText: []`, `"linkedinData": {"documentTitle": "<titolo>", "publishImagesAsPDF": true, "previewIncluded": true, "type": "post"}`. Per un PDF diretto fai prima una prova piccola.
- Media: URL pubblici diretti, non link al repository (è privato): con il tuo accesso Higgsfield `media_upload`, PUT con curl sull'URL ricevuto, `media_confirm`, poi apri gli URL restituiti. Ripiego: media a mano in Planning.
- Dopo ogni scrittura fai il §7, passo 9.

## Protezioni sulle scritture

1. L'amministratore degli strumenti, Owner del Team, in Organization settings > Connectors > Metricool mette su «Needs approval» `createScheduledPost`, `updateScheduledPost`, `createScheduledPostForReview`, `sendScheduledPostForReview`.
2. Non spegnere l'hook PreToolUse di `contenuti-sersan`, che chiede conferma sugli stessi tool.
3. A ogni conferma confronta i parametri con la lista approvata; se non coincidono, rifiuta.

## Prova con un post a data lontana

La prima volta e a ogni cambio di piano o di plugin, con il sì dell'amministratore degli strumenti e i permessi abituali:
1. Chiedi a Claude un post «TEST» fra tre mesi, `draft:true` (con Advanced o Custom anche in revisione). Devono comparire la richiesta del connettore e la conferma dell'hook; se una manca, fermati e avvisa il responsabile del toolchain.
2. In Planning il post deve risultare bozza. Annota l'esito nel registro del sì, cancella il post e verifica con `getScheduledPosts`.

# 9. LinkedIn automatizzato con linkedin-skills

Il plugin linkedin-skills scrive piano, bozze, commenti e risposte; con Publora pubblica commenti, risposte e reazioni. I post escono da Metricool. Solo con Claude Code, salvo i passi a mano.

## Installazione

1. In Claude Code: `/plugin marketplace add sergebulaev/linkedin-skills`, poi `/plugin install linkedin-skills@linkedin-skills` (su Windows il plugin, non il clone). Annota la versione; prima di aggiornare leggi le note di release.
2. Nessuna chiave nel plugin, niente `APIFY_TOKEN`, `PIXFARO_TOKEN`, `LINKEDIN_SKILLS_CUSTOM_POSTER`. Non eseguire `test_detectors.py`, che manda il testo a terzi.

## Passo zero: Story Bank e profilo di voce

Per ogni founder, prima delle bozze automatiche:
1. Esegui con il founder `linkedin-interviewer --mode bank` (20-40 minuti).
2. Esegui `linkedin-humanizer --mode profile` con 3-6 suoi post veri.
3. Nel profilo («Hard rules», «Links and CTA») metti le regole del §2, senza pause `..` né frasi in minuscolo; nella Story Bank («Off limits») clienti e progetti da non nominare.
4. Salva `_ref/<founder>/story-bank.md` e `_ref/<founder>/voice-profile.md` con `filled: yes`, mai in un repository.

Numeri e fatti solo dalla Story Bank: se un numero manca, togli la frase.

## Task programmati

Girano sul PC acceso di chi gestisce i post, con il suo posto Claude:
1. Bozze, lunedì 08:00: per ogni founder `linkedin-content-planner` e `linkedin-post-writer` sui suoi slot della settimana dopo, con `_ref/<founder>/`, poi `linkedin-humanizer --mode audit`; solo file «BOZZA da approvare» in `PUBBLICAZIONE/bozze_linkedin/`.
2. Testi dei commenti, lun-ven 09:00: per ogni file di `PUBBLICAZIONE/commenti_input/` non ancora in `PUBBLICAZIONE/commenti_pronti/`, con le regole del suo account, `linkedin-comment-drafter` o `linkedin-reply-handler`, poi `linkedin-humanizer --mode strict`; testo in `commenti_pronti/`, stesso nome.
3. Pubblicazione dei commenti, lun-ven 09:30.

Righe (`--strict-mcp-config` esclude i connettori e quindi ogni scrittura su Metricool):

```
claude -p "Esegui l'attività 1 del §9 di _docs/GESTIONE_POST.md." <opzioni>
claude -p "Esegui l'attività 2 del §9 di _docs/GESTIONE_POST.md." <opzioni>
python -I -X utf8 _log/linkedin_commenti.py
<opzioni> = --strict-mcp-config --permission-mode acceptEdits --permission-prompts none
```

**A mano**: Utilità di pianificazione di Windows > «Crea attività di base» > nome, frequenza, ora > «Avvia un programma»: «Programma o script» la prima parola, «Aggiungi argomenti» il resto, «Inizia da» la radice del repository. **Con Claude Code**: `schtasks /Create` con gli stessi valori.

Fai prima una prova piccola: lancia la riga 1 dalla radice e controlla `bozze_linkedin/`; in `claude --strict-mcp-config`, `/mcp` non deve mostrare server.

## Pubblicazione dei post

Ogni founder: 2 post a settimana, martedì e giovedì; le altre bozze restano in `bozze_linkedin/`. Dopo il sì programma la Pagina dal brand aziendale, ogni founder dal suo (§7).

## Commenti, risposte e reazioni automatici

### Regole approvate

Il titolare le approva per iscritto in `PUBBLICAZIONE/regole_commenti/<account>.md`, una volta e a ogni cambio (un account nuovo sì, un post nuovo no), con una riga nel registro del sì con riferimento `regole_commenti/<account>.md`; senza, non parte niente.

```
Account: <profilo LinkedIn>, platform_id <linkedin-...>
Temi ammessi: ...
Tono: ...
Account da commentare: <elenco>
Tetti al giorno: commenti 5, risposte 5; una reazione per commento
Orari: 09:30-17:30, lunedì-venerdì
Approvato da: <titolare>, il <data>
```

### Ritmo e limiti

- Tetti del modello per la prima settimana, dimezzati sull'account che invia da SerSanOutreach; poi, dopo ogni settimana senza segnali di limitazione e con un nuovo sì del titolare, +3 commenti al giorno, fino a 20.
- Mai 15 o più commenti in 90 secondi, né gli stessi account allo stesso minuto ogni giorno.
- Commenti di 200-350 caratteri, risposte di 150-300, una alla volta; oltre 10 nello stesso thread, distribuiscile nel tempo.

### Testi da commentare

Solo a mano, ogni mattina prima delle 09:00, per ogni post nuovo degli account in elenco:
1. Controlla in `/leads/` di SerSanOutreach che l'autore non sia in una sequenza attiva; se lo è, saltalo.
2. Crea `PUBBLICAZIONE/commenti_input/<data>_<account>_<n>.txt`: prima riga l'URL del post o del commento a cui rispondere, poi il testo copiato da LinkedIn.

Niente lettura automatica; Apify solo con l'autorizzazione scritta dell'amministratore degli strumenti, sugli URL approvati.

### Pubblicazione dei commenti

`_log/linkedin_commenti.py` pubblica i testi di `commenti_pronti/` che passano i controlli del §6, entro regole, tetti e orari: prima la reazione, poi il commento o la risposta. Scrive ogni azione nel log LinkedIn e sposta i file usciti in `PUBBLICAZIONE/commenti_pubblicati/`. Al primo errore (429, rifiuto, checkpoint, avviso) si ferma senza riprovare e crea `_log/linkedin_STOP_<account>.txt`, che blocca l'account.

1. L'amministratore degli strumenti salva `PUBLORA_API_KEY` e `LINKEDIN_PLATFORM_ID` in `~/.publora/publora.env` sul PC che pubblica, mai nel repository.
2. Lo script trova linkedin-skills fra i plugin di Claude Code; se non lo trova, imposta `LINKEDIN_SKILLS_DIR` sulla cartella del plugin.
3. Prova prima con `--dry-run` (controlli e anteprima, nessuna scrittura), poi con `--no-wait` (una sola pubblicazione, senza pause): un commento e una reazione veri su un post del titolare. Controlla su LinkedIn account, testo e reazione, poi il log; se qualcosa non va, non attivare l'attività 3.
4. Codici di uscita: 0 tutto bene; 1 configurazione mancante o non valida, o un altro giro in corso; 2 account fermato.
5. Non aprire il log e il registro del sì con Excel: li risalva in un formato che lo script rifiuta.

Finché l'attività 3 non è attiva, il titolare incolla su LinkedIn i testi di `commenti_pronti/`.

### Controllo e ripartenza

Ogni mattina guarda in `_log/`: se c'è un file `linkedin_STOP_`, avvisa per iscritto il titolare e l'amministratore degli strumenti; cancellalo solo dopo il sì del titolare nel registro del sì e riparti dai tetti iniziali.

## Cosa non si automatizza mai

- Inviti e DM fuori da SerSanOutreach.
- Comment-to-DM.
- Post via Publora.
- Reshare.
- Scraper (Apify o altri), salvo l'ok esplicito dell'amministratore degli strumenti.

# 10. SerSanOutreach

## Cosa fa

Inviti senza nota, DM, follow-up, lettura della posta LinkedIn; le risposte dalla Unibox le manda una persona. Non pubblica né commenta.

## Modi di approvazione

- In automatico: `manual_all` niente; `manual_linkedin` solo email; `auto_blank_invites` inviti senza nota; `auto_linkedin` anche DM, con `autopilot_enabled`, `autopilot_dm_enabled` e il sì scritto del titolare sul pilota (modelli e tetti) nel registro del sì. Senza, `manual_all`. Lo imposta lo staff in `/pilot/`.
- **A mano**: l'operatore apre `/review/?channel=linkedin` e accetta, o rifiuta con un motivo.
- **Con Claude Code**: `sersan-outreach` (lettura) e `sersan-operator` (approva o rifiuta con il `fingerprint`), con la tua chiave (§3).

## Tetti per account

- Al giorno 20 inviti (100 a settimana), 40 DM, 30 follow-up; in rampa ogni tetto giornaliero scende a 5 più 2 per giorno attivo negli ultimi 30. Si possono solo abbassare (titolare in `/linkedin/settings/`, staff in `/linkedin/team/`).
- Finestra 09:00-18:00 lun-ven; contatori azzerati a mezzanotte UTC. Dopo l'avviso del limite settimanale, niente inviti a mano per 7 giorni.

## Convivenza

- LinkedIn conta anche commenti e azioni a mano, che i contatori non vedono (da qui i tetti dimezzati del §9).
- Niente inviti o DM a mano ai lead delle campagne; se succede, registralo nel cockpit.
- Il Chrome del titolare con l'estensione serve solo a SerSanOutreach; non chiuderne la sessione LinkedIn.
- Checkpoint o CAPTCHA: ferma tutto sull'account, commenti compresi (file di stop); lo risolve a mano il titolare, dallo stesso paese.

## Quando è fermo

È fermo se `https://outreach.sersan.io` non si apre o «Connect» mostra l'account OFFLINE.
1. Avvisa l'amministratore degli strumenti e lo staff.
2. Crea `_log/linkedin_STOP_<account>.txt` per l'account che invia.
3. Nel registro del fermo annota inizio, fine e ogni risposta, contatto a mano o richiesta di non essere contattati, senza il testo.

Niente outreach manuale di massa né campagne Instantly; non scollegare l'estensione. Una campagna attiva la mette in pausa lo staff.

## Rientro dopo un fermo

Dettagli in `docs/runbooks/emergency_shutdown.md` §4 del repository di SerSanOutreach.
1. Lo staff rimette su server e deploy approvato, con gli stop accesi e `PILOT_MODE=enforce` nel `.env`; **con Claude Code** o da terminale, `gh workflow run` di `prod_linkedin_status.yml` (log «[Pilot] envelope engaged»), `prod_launch_readiness.yml`, `prod_dr.yml -f action=backup`.
2. **A mano**: il titolare controlla in «Connect» estensione, account e «invia». Lo staff riporta il registro del fermo dalla Unibox («Registralo qui») entro 14 giorni da ogni risposta e controlla: posta sincronizzata (`/linkedin/team/`); «Sends we cannot confirm» a zero (`/pilot/`), messaggi superati rifiutati; in Instantly niente partito, webhook «SerSan dashboard sync» attivo.
3. Con un sì esplicito: modo del pilota, campagne, per ultimo lo stop LinkedIn; rampa bassa, tetti invariati. Poi togli il file di stop dei commenti.

# 11. Dopo la pubblicazione

## Il giorno dell'uscita

Fai il §7, passi 10 e 11, e dedica 15 minuti ai commenti: su Instagram, Facebook e Pagina LinkedIn rispondi a mano dall'app o dall'Inbox di Metricool, in giornata. Profili dei founder: §9 e §10.

## Numeri del lunedì

- **A mano**: Analytics di ogni brand in Metricool, settimana precedente.
- **Con Claude Code**, sola lettura: `getAnalyticsDataByMetrics` (`brandId`, `from`, `to`, `metrics`); codici con `getAnalyticsAvailableMetrics` (`network`, `connector:"posts"`).

```
IG: IGPO14 reach, IGPO28 views, IGPO13 like, IGPO08 commenti, IGPO15 salvataggi,
IGPO27 condivisioni, IGPO29 follow, IGPO12 interazioni
LinkedIn: LIPO12 impressioni, LIPO13 reazioni, LIPO10 commenti, LIPO09 clic,
LIPO18 condivisioni
```

Scrivi i numeri nel foglio dei numeri e, per ogni pezzo, nel ledger.

## Criterio di stop

Ogni lunedì, per i pezzi dei founder con `via` A o B. Commento qualificato: scritto da una persona esterna al team con un ruolo da cliente ideale (i ruoli li indica chi autorizza la pubblicazione).
- Fermati se un cliente ideale, o tre persone in totale, mettono in dubbio l'autenticità, o se per due uscite di fila i commenti qualificati restano sotto la mediana dei post `reale` del founder nelle 4 settimane prima.
- Se scatta: niente pezzi nuovi con AI, coda ferma anche su Metricool; avvisa chi autorizza la pubblicazione. Non cambiare la soglia dopo aver visto i dati.

## Etichette automatiche

Se una piattaforma mette da sola «AI info», «Altered or synthetic content» o l'icona C2PA, non contestarla e non ripubblicare: annotala nel ledger e avvisa l'amministratore degli strumenti.

# 12. Cose da fare a mano

- Collegamento degli account, checkpoint e CAPTCHA: il titolare.
- Bio di Instagram; nome, tagline e About della Pagina LinkedIn.
- Reshare della Pagina (§4) e testi da commentare (§9).

# 13. Problemi frequenti

| Problema | Cosa fai |
|---|---|
| Connettore assente | Sessione nuova, poi ToolSearch |
| Caption con «il link è nel profilo» | Controlla che la bio porti a `sersan.io/start` |
| Finale fuori specifica o difettoso | Non correggerlo né programmarlo: a chi monta con la nota del difetto; stato DA MONTARE |
| Uscito con errore nel testo o difetto | Instagram e Facebook: archivialo; LinkedIn: eliminalo. Avvisa chi approva i testi o chi monta; annota nel ledger |
