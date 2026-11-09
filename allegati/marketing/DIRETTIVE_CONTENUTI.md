% Direttive per generare contenuti
% Video, voce, immagini, slide e testi per i social: cosa si fa e come · versione del 22 ottobre 2026
% Da approvare

# 1. Come usare questo documento

Serve a chi produce i contenuti. Per programmare e pubblicare usa il documento «Gestione dei post».

## Le due strade

- **A mano**: nell'app o sul sito dello strumento, passo per passo.
- **Con Claude Code e il plugin `contenuti-sersan`** (Appendice A): scrivi in testa al messaggio l'etichetta `#Wnn` della scheda. Senza plugin l'etichetta non carica niente: incolla la riga «Con Claude Code» della scheda, con modello e parametri.

## Come si legge una scheda

Voci di una scheda, quando servono: Quando, Cosa serve, A mano, Con Claude Code, Ripiego, Regola, Controlli, Costo, Consegna.

## Stato e schermate diverse

- Prima di iniziare controlla lo stato attuale degli strumenti in `_docs/STATUS.md`.
- Schermata o tool diversi dalla scheda: a mano confronta con `_docs/STATUS.md`; con Claude Code rileggi il catalogo con `get_workflow_instructions` senza argomento. Se non torna, fermati e avvisa il responsabile del toolchain.

## Ruoli

| Ruolo | Cosa fa | Cosa non fa |
|---|---|---|
| Chi produce i contenuti | Genera, raccoglie il girato, scrive le bozze, tiene i registri, prepara le consegne | Non monta, non pubblica, non crea cloni di voce o volto al posto del founder |
| Chi monta | Composito, montaggio, reframe, sottotitoli, grafiche, musica, versioni, finali | Non cambia i testi approvati |
| Chi approva i testi | Approva per iscritto testi EN e IT | — |
| Chi firma la parte tecnica | Firma ogni affermazione tecnica stampata | — |
| Chi autorizza la pubblicazione | Dà il sì sulla lista di programmazione | — |
| Chi gestisce i post | Programma su Metricool dopo il sì | — |
| Il founder | Registra, approva volto, voce e propri testi, crea PVC e identità | — |
| L'amministratore degli strumenti | Posti, accessi, connettori, ricariche; ok al provino e agli strumenti fuori stack | — |
| Il responsabile del toolchain | Mantiene plugin e workflow, ripara le route bloccate | — |

## Glossario

- **Via B**: founder girato davvero; dopo si cambiano luogo, luce o vestiti.
- **Via A**: founder tutto generato da foto o da una cattura.
- **Provino**: prova di 10-30 s di un founder generato, giudicata alla cieca da chi lo conosce (§6).
- **PVC / IVC**: clone di voce ElevenLabs professionale (almeno 30 min di registrazione) e istantaneo (1-2 min, solo per prove).
- **Element, Soul ID**: identità del founder su Higgsfield. Le crea il founder con il suo posto nel workspace Team aziendale e ti passa l'ID. Mai identità create su account personali.
- **Ledger**: registro dei pezzi. **Registro del sì**: dove si scrive ogni approvazione prima di agire (§15).

# 2. Regole che valgono sempre

## Brand

- Nessuna etichetta «generato con AI» o «avatar», niente compliance né disclaimer. Lascia spenti gli interruttori AI delle piattaforme, anche se una skill dice il contrario.
- Non aggiungere C2PA. Non devi togliere i metadati; controllali con `exiftool` solo se serve.
- Niente prezzi.
- Ogni testo esce in EN e IT, con la CTA fissa (§11), e resta «BOZZA da approvare» fino al sì scritto.
- Parole vietate: compliant, compliance-ready, certified, conforme, certificato, «3am», «two people», «due persone», «SERSAN AI». Non citare licenze o contratti del team né i ruoli precedenti dei founder con i loro numeri.
- Frasi corte e concrete, tono sobrio, niente punti esclamativi né emoji, «AI» e mai «IA».

## Generazione

- Mai testo, lettere, numeri o marchio generati dentro immagini e video: li aggiunge l'impaginazione o chi monta, dai file ufficiali del marchio (§3).
- Volti e voci solo dei founder, con consenso scritto nel registro dei consensi (§15). Mai persone generate estranee (creator, clienti, testimonial, comparse).
- Voce del founder: voce vera, poi PVC nella stessa lingua, IVC solo per le prove. Posala sopra il video, con un solo passaggio di lip sync. Mai come traccia da far rigenerare al modello, mai `voice_change`, mai `create_voice` di Higgsfield, mai TTS come audio guida.
- Prima di modificare un video che non è dell'azienda, annota i diritti nel registro dei diritti (§15).
- Strumenti fuori stack (HeyGen, Runway, sync.so diretto, fal, BytePlus, Beeble, Luma): solo con l'ok dell'amministratore degli strumenti; annota ogni prova nel log delle prove esterne (§15).
- Prima di ogni serie fai una prova piccola e controllala (§13).
- Consegna materiale grezzo e livelli separati: composito e montaggio li fa chi monta (§14). Un tuo composito serve solo come anteprima interna.
- Non cancellare niente: scarti in `_scartati/` con il motivo (`_log/specs_tool.py mark`), prove superate in `_archivio/`.
- Usa solo il tuo accesso. Login e «Connect» li fa la persona a cui appartiene l'accesso; Claude non inserisce password.
- Niente esce senza un sì umano scritto nel registro del sì.

# 3. Postazione e accessi

## PC di chi produce i contenuti

1. Claude Code 2.1.273 o successivo: installalo da PowerShell, poi in un terminale nuovo controlla la versione e lancia `claude` con l'account claude.ai del tuo posto Team.

```
irm https://claude.ai/install.ps1 | iex
claude --version
claude
```

2. Node 22 o successivo, Python 3 con `pip install pillow`, ffmpeg nel PATH, Git per Windows (con Git Bash), GitHub CLI (`winget install GitHub.cli`), Google Chrome nel percorso standard (per `build.py`, §10).
3. Skill HyperFrames: `npx skills add heygen-com/hyperframes`. Imposta una volta le variabili, poi riapri il terminale:

```
setx HYPERFRAMES_SKIP_SKILLS 1
setx HYPERFRAMES_NO_TELEMETRY 1
```

4. Font del brand: installa tutti i `.ttf` di `kit/fonts/` dallo zip del kit (§10). File ufficiali del marchio: `kit/logo/`, nello stesso zip.
5. LibreOffice ed exiftool, se impagini il kit PPTX/PDF in locale (§10).
6. Al primo uso si scaricano Chrome (render), Parakeet (trascrizione) e il modello di scontorno: chiedi prima il sì all'amministratore degli strumenti.

After Effects, TX Library, Blender e Remotion stanno solo sul PC di chi monta.

## Accessi

| Strumento | Accesso | Collegamento |
|---|---|---|
| Claude | Il tuo posto Team | Connettori aggiunti dall'amministratore degli strumenti; ti autentichi tu |
| Higgsfield (sito higgsfield.ai) | Un posto nel workspace Team aziendale | Sul sito scegli il workspace aziendale prima di generare. Connettori `https://mcp.higgsfield.ai/mcp` e `https://bridge.higgsfield.ai/mcp`, poi `select_workspace` |
| ElevenLabs (app elevenlabs.io) | Un posto Full | Connettore `https://api.elevenlabs.io/v1/mcp` (OAuth) |
| moda | Il workspace aziendale | Connettore `https://agents.moda.app/mcp` |
| Metricool | Accesso aziendale dall'amministratore degli strumenti | Documento «Gestione dei post» |

## Cartella di lavoro condivisa

È il repository GitHub privato `SerSan-AI-Studio/SERSAN-marketing`: tutti i percorsi del documento partono dalla sua radice.

1. L'amministratore degli strumenti ti dà accesso all'organizzazione GitHub `SerSan-AI-Studio`.
2. Clona una volta, da Git Bash:

```
gh auth login
gh auth setup-git
git clone https://github.com/SerSan-AI-Studio/SERSAN-marketing.git
```

3. Prima di lavorare `git pull`; a fine lavoro `git add <file>`, `git commit -m "<cosa hai fatto>"`, `git push`. Mai `--force`: per un conflitto chiedi al responsabile del toolchain.
4. Nel repository solo file sotto i 50 MB. Girato, WAV e file più grandi vanno nella cartella di consegna di chi monta (§14).

| Cartella | Contenuto |
|---|---|
| `_docs/` | Documenti, `STATUS.md`, `ricette/` |
| `scripts/` | Copioni dei founder, battute approvate |
| `posts/carousels/v3_light/_template/` | Template dei caroselli |
| `posts/teardowns/out/kit/` | Kit PPTX/PDF, font e marchio |
| `_log/` | Log e script di QA |
| `_registri/` | Registri (§15) |
| `PUBBLICAZIONE/` | Finali, calendario, ledger, registro del sì |
| `_plugin/` | Plugin `contenuti-sersan` (Appendice A) |

`_ref/` (foto e voci dei founder), `_scartati/` e `_archivio/` non sono nel repository. `_ref/` è ristretto: ricevi solo gli ID (Element, Soul ID, voce condivisa). Le foto di riferimento le carica il founder negli Assets del workspace Higgsfield aziendale: a mano le scegli lì, con Claude Code usi i `media_id` che ti passa.

# 4. Prima di generare: scegliere la strada

## Le tre domande

1. **C'è un founder nell'immagine o nella voce?** No: §7, §9, §10. Sì: serve il consenso scritto.
2. **Girato o generato?** Preferisci la via B (§5). Podcast: registrato a due, poi cambio d'ambiente (B14). Via A (§6) solo dopo il sì sul provino. Da foto senza audio vero solo clip a bocca chiusa.
3. **Serve la sua voce?** Segui l'ordine della voce (§2, §8).

## Limiti di durata

Veo 8 s; Kling 3.0, FLUX Video Edit e Genjutsu Lite 15 s; Seedance 30 s; Genjutsu e Ad Multiplier: sorgenti da 4 a 30 s. Oltre il limite genera a spezzoni: li unisce chi monta.

## Tutte le combinazioni

«→» vuol dire: lo fa chi produce i contenuti e passa il risultato.

| Combinazione | Strada | Etichetta | Sezione | Chi |
|---|---|---|---|---|
| A1 Founder generato che parla | Avatars, dopo il provino, solo a mano | — | §6 | → chi monta |
| A3 Da foto a video parlato | Lip sync da foto, dopo il provino | `#W56`, `#W62` | §6 | → chi monta |
| A2 Persona inventata | Non si fa | — | §6 | — |
| A4 Founder narratore su un video esistente | Ripresa via B e scontorno | `#W49`, `#W59` | §6 | → chi monta |
| A5 Clip di ascolto | Seedance 2.5 da foto | `#W56` | §6 | → chi monta |
| B1, B10 Luogo con volto intatto, scontorno | Scontorno e fondale | `#W49`, `#W59`, `#W57` | §5 | → chi monta |
| B2, B6, B11 Luogo generativo, aggiungere, togliere | Ad Multiplier Edit | `#W71` | §5 | → chi monta |
| B3 Luce | Video Relight dal sito | — | §5 | → chi monta |
| B4, B5, B5-bis, B7, B8 Vestiti, oggetti, soggetto, gesti, stile | Genjutsu | `#W63` | §5 | → chi monta |
| B9 Nuove inquadrature del luogo | `/3d-jutsu`, solo con Claude Code | — | §5 | Chi produce i contenuti |
| B12 Reframe AI su richiesta di chi monta | `reframe` | `#W60` | §5 | → chi monta |
| B13 Upscale | Upscale Higgsfield | `#W58` | §5 | Chi produce i contenuti |
| B14 Podcast a due | Scontorno, fondale, audio pulito | `#W49`, `#W71` | §5 | → chi monta |
| B-roll, plate, loop, hook, video senza volto | Seedance, Kling, faceless | `#W56`, `#W68` | §7 | → chi monta |
| Logo, promo dal sito, versioni | HyperFrames | `#W36`, `#W39`, `#W55` | §7 | Chi monta |
| C1-C6 Voce, doppiaggio, lip sync, SRT, SFX | ElevenLabs, Higgsfield | `#W62`, `#W49` | §8 | → chi monta |
| Immagini, ritratti, copertine | Higgsfield Image | `#W57`, `#W78` | §9 | Chi produce i contenuti |
| Caroselli, slide, PDF | `build.py`, kit PPTX/PDF | `#W80`, `#W44` | §10 | → chi gestisce i post |
| Testi per i social | Bozze EN e IT | — | §11 | → chi approva i testi |

## Route bloccate

Se un workflow vuole After Effects o Blender in locale e all'avvio lo stato dice «NON installato», non ripiegare sul cloud: avvisa il responsabile del toolchain e usa logo `#W36`, scontorno `#W49`, grafiche `#W42`, togliere oggetti `#W71`.

# 5. Video con il founder girato davvero

## Ripresa comune

1. Fai registrare il founder secondo il suo copione: set, inquadratura, audio, vestiti, take e invio dei file sono lì. Non cambiarli.
   - `scripts/clips-alessandro/COPIONI_ALESSANDRO_2026-10-14.md`
   - `scripts/reels/COPIONI_MICHELE_2026-10-14.md`
   - `scripts/podcast/COPIONI_PODCAST_INSIEME_2026-10-14.md`
2. Alla prima sessione di ogni founder gira una clip di prova da 10 s e prova B2 e Object Swap sul luogo (B4 se cambiano i vestiti). Porta i risultati all'amministratore degli strumenti e scrivi lo strumento scelto nel registro del sì. Se nessuno tiene il volto identico, usa B1.
3. Metti i file ricevuti in `01_originali/` della cartella del pezzo, senza rinominarli (§14).
4. Estrai il segmento della battuta, senza toccare l'originale:

```
ffmpeg -ss <inizio> -t <durata> -i <originale> -c:v libx264 -crf 16 -c:a aac <ID>_seg.mp4
```

5. Controlla la durata con `ffprobe`: deve stare nel limite dello strumento (§4).

Regole per tutte le schede:
- Prova piccola a 480p o 720p (o con Lite) prima del finale a 1080p, cambiando una cosa alla volta.
- Con `generate_video` scrivi sempre `resolution` (il default è 720p). Con Seedance e Ad Multiplier anche `generate_audio:false`, con Kling `sound:"off"`. Genjutsu (`hf_mult_*`) ha solo `resolution`.
- Dopo ogni edit rimetti l'audio originale (Appendice B), salvo dove la scheda dice che lo fa il workflow.
- Salva ogni uscita in `02_editati/` (nomi: §14). Consegna: clip con l'audio rimesso, a chi monta, salvo dove la scheda dice altro.

## Schede

#### B1. Cambio di luogo con i pixel del volto intatti

- **Quando**: il volto deve restare quello girato, oppure la clip di prova ha bocciato B2.
- **Cosa serve**: take alla parete; immagine del luogo senza testo, con luce e punto di vista del take (§9).
- **A mano**:
  1. Se serve, fai l'upscale (B13).
  2. Fai lo scontorno (B10).
  3. Genera il fondale sul sito Higgsfield, Image (o Video per un fondale in movimento).
- **Con Claude Code**: `#W58` (upscale), `#W49` (scontorno gratis) o `#W59` (`remove_background`), `#W57` o `#W56` (fondale).
- **Controlli**: bordi di capelli e occhiali; luce del fondale coerente con quella sul founder.
- **Costo**: `#W49` gratis; `remove_background` senza preflight (§16).
- **Consegna**: livelli separati (matte, fondale, audio originale) a chi monta, che compone.

#### B2. Cambio di luogo con edit generativo (Ad Multiplier Edit)

- **Quando**: cambiare luogo o sfondo, anche insieme ai vestiti, tenendo recitazione, camera e audio.
- **Cosa serve**: un segmento di 4-30 s; immagine del luogo (`@Image1`); per i vestiti, un'immagine del capo.
- **A mano**: sito Higgsfield > Ads Studio > Ad Multiplier. Carica il video e le immagini, scrivi il prompt (Appendice B), genera. Poi rimetti l'audio originale.
- **Con Claude Code**: `#W71`: `model:"ad_multiplier"`, `mode:"video_edit"`, `generate_audio:false`, `duration` (durata del segmento con `ffprobe`, arrotondata per eccesso), `duration_policy:"strict"`, `aspect_ratio:"auto"`, `resolution` 720p o 1080p, `count:1`; prompt fino a 3.900 caratteri con `@Video1` e `@ImageN`. Il workflow rimette l'audio. Un output alla volta; se fallisce, riprova una volta sola.
- **Ripiego**: sito Higgsfield > Genjutsu > Object Swap, con l'immagine del luogo e il prompt dell'Appendice B.
- **Controlli**: identità del volto (i pixel si rigenerano); labiale con l'audio rimesso; mani; capelli. Con più segmenti dello stesso discorso, luogo e luce uguali in tutti.

#### B3. Cambio di luce

- **A mano**: sito Higgsfield > Video Relight.
- **Con Claude Code**: nessuna strada; solo a mano.
- **Ripiego**: grading, che fa chi monta.
- **Controlli**: pelle; sfarfallio.

#### B4. Cambio di vestiti

- **Cosa serve**: un segmento di 4-30 s; un'immagine per capo, frontale, con luce coerente.
- **A mano**:
  1. Apri higgsfield.ai/genjutsu (o Video > Genjutsu) > Object Swap.
  2. Carica un video e le immagini; scegli un preset o scrivi una descrizione breve.
  3. Per le bozze attiva Lite (elabora solo i primi 15 s e conserva l'audio).
  4. Scegli la risoluzione e genera.
- **Con Claude Code**: `#W63`, `generate_video` con `model:"hf_mult_replace_object"`, in `medias` un solo video (`role:"video"`) e le immagini (`role:"image"`), `resolution:"1080p"`. Genera una volta, poi `jobs_wait` con `timeout_seconds:15`. Lite solo a mano.
- **Ripiego**: Ad Multiplier Edit (B2) con il capo come `@ImageN`.
- **Controlli**: volto; labiale; audio presente.

#### B5. Sostituire un oggetto o un prodotto

- **Cosa serve**: segmento di 4-30 s; immagini dell'oggetto; diritti su ogni marchio che compare.
- **A mano**: come B4, con le immagini dell'oggetto.
- **Con Claude Code**: `#W63`, `hf_mult_replace_object`.
- **Controlli**: deriva dell'oggetto quando viene coperto o toccato.

#### B5-bis. Founder al posto del soggetto di un video esistente

- **Cosa serve**: video sorgente di 4-30 s con un soggetto chiaro, a figura intera, senza tagli; diritti annotati; foto del founder frontale, di tre quarti e a figura intera (§3); consenso.
- **A mano**: higgsfield.ai/genjutsu > Object Swap. Usa Motion Transfer solo se vuoi rifare anche luogo e look. Lite per le bozze. Nel prompt nomina chi sostituire (Appendice B).
- **Con Claude Code**: `#W63`, `hf_mult_replace_object` o `hf_mult_motion_control`.
- **Ripiego**: Ad Multiplier Edit (B2) con l'istruzione «replace» e la foto come `@ImageN`.
- **Regola**: provino obbligatorio (§6).
- **Controlli**: quelli del provino (§6); rotazioni rapide; mani. Il labiale resta quello della persona originale: per far parlare il founder fai dopo un solo lip sync (C4).

#### B6. Aggiungere il founder o un oggetto nella scena

- **Cosa serve**: take; riferimento del founder o dell'oggetto.
- **A mano**: sito Higgsfield > Ads Studio > Ad Multiplier, istruzione «add».
- **Con Claude Code**: `#W71`. Nel prompt scrivi posizione, scala, movimento e interazione; un `@ImageN` per ogni persona.
- **Controlli**: solo founder con consenso; nessuna persona in più.

#### B7. Motion transfer

- **Quando**: i gesti di un video guida su un founder ricavato da foto.
- **Cosa serve**: video guida di 4-30 s senza tagli, con un soggetto ben visibile, già nel formato finale; foto del founder con braccia e mani visibili.
- **A mano**: higgsfield.ai/genjutsu > Motion Transfer.
- **Con Claude Code**: `#W63`, `hf_mult_motion_control`. Non usare `motion_control` per un edit Genjutsu.
- **Regola**: provino obbligatorio (§6).
- **Controlli**: volto generato, fragile come nella via A; mani incrociate e oggetti davanti al corpo.

#### B8. Restyle di tutto il video

- **Quando**: solo se chi approva i testi o chi monta chiede uno stile su tutto il video.
- **Cosa serve**: video di 4-30 s; fino a 5 riferimenti facoltativi.
- **A mano**: sito Higgsfield > Genjutsu, scegli uno stile.
- **Con Claude Code**: `#W63`. Apri con `get_preset_instructions {preset:"/genjutsu"}`, sfoglia gli stili con `get_presets` (`source:"genjutsu"`, `category:"genjutsu-styles"`), leggi il prezzo con `get_presets` sul preset `genjutsu-style:<id>` con `initial_inputs:{video, references, resolution}`, genera con `execute_preset`.
- **Controlli**: palette e famiglie visive del brand (§9).
- **Costo**: `execute_preset` è senza preflight (§16).

#### B9. Nuove inquadrature dello stesso luogo

- **Cosa serve**: un'immagine del luogo senza testo.
- **A mano**: nessuna strada; solo con Claude Code.
- **Con Claude Code**: `get_preset_instructions` con `{preset:"/3d-jutsu"}`, poi «Reconstruct a location from an image»; gli angoli con `scene_builder_3d_generate_angles`.
- **Controlli**: lo stesso luogo in tutti gli angoli.
- **Consegna**: immagini da usare come fondali in B1, B2 o A5.

#### B10. Scontorno, matte o depth

- **A mano** (solo persone): fai prima l'upscale se serve (B13), poi da terminale:

```
npx hyperframes remove-background <in> -o <nome>.mov
```

- **Con Claude Code**: persone `#W49` (stessa via, gratis); oggetti o prodotti `#W59` (`remove_background`, `sam_3_video`, `depth_anything_video`).
- **Controlli**: bordi; sfarfallio.
- **Costo**: `#W59` senza preflight (§16).
- **Consegna**: ProRes 4444 `.mov` con alfa, a chi monta.

#### B11. Togliere oggetti, cavi o insegne

- **A mano**: sito Higgsfield > Ads Studio > Ad Multiplier, istruzione «remove».
- **Con Claude Code**: `#W71`.
- **Ripiego**: Smart Clean Up di Seedance dal sito Higgsfield.
- **Controlli**: i pixel si riscrivono, controlla il volto.

#### B12. Reframe AI da 16:9 a 9:16

- **Quando**: solo se chi monta chiede un reframe AI (di regola fa un crop non generativo con `#W37`).
- **A mano**: nessuna strada; solo con Claude Code.
- **Con Claude Code**: `#W60`, `reframe`, fino a 60 s e 1080p.
- **Controlli**: volto dentro la zona sicura.

#### B13. Upscale

- **Quando**: solo sugli asset scelti, prima dello scontorno.
- **A mano**: sito Higgsfield > Upscale.
- **Con Claude Code**: `#W58`, `upscale_video`.
- **Costo**: senza preflight (§16).
- **Consegna**: al passo successivo o a chi monta.

#### B14. Podcast registrato a due, con cambio d'ambiente

- **Cosa serve**: girato del set a due e WAV dei trasmettitori, secondo il copione del podcast (Ripresa comune).
- **A mano**:
  1. Video: scontorno del piano a due (B10); prova prima un segmento e controlla il bordo fra le due persone.
  2. Video: fondale dello studio (B1).
  3. Audio: Voice Isolator sui WAV, poi Scribe v2 con timestamp e diarizzazione (C5).
  4. Con Claude, sul trascritto, scegli battute e clip con inizio e fine; citazioni alla lettera.
  5. Tagli brevi già scelti (reel, trailer, 4-30 s): puoi usare B2.
  6. Clip di ascolto (A5) solo come riempitivo, senza cenni.
- **Con Claude Code**: `#W49` o `#W59` (matte), `#W57` o `#W56` (fondale), `#W71` (tagli brevi).
- **Controlli**: bordi fra le due persone; luce coerente; nomi e sigle nel trascritto.
- **Consegna**: matte, fondale, audio pulito, trascritto, SRT e lista delle battute scelte, a chi monta.

# 6. Video con il founder generato

## Provino

Obbligatorio prima di A1, A3, B5-bis e B7, per ogni founder e ogni strumento nuovo. Senza il sì dell'amministratore degli strumenti sul provino, usa la via B (§5).

1. Fai registrare al founder una battuta in IT e una in EN, due take per lingua, più 10 s di room tone e 10 s di sguardo muto in camera. Set e battuta: copioni in `scripts/`.
2. Genera 10-30 s con lo strumento candidato e la voce della serie. A1: app ElevenLabs > Avatars (ripiego HeyGen Avatar V, con l'ok dell'amministratore degli strumenti). A3: sito Higgsfield > Lipsync Studio (ripiego app ElevenLabs > Image & Video > OmniHuman 1.5, se approvato dall'amministratore degli strumenti).
3. Fai giudicare il risultato alla cieca, accanto a un take vero, da tre persone, almeno due che conoscono il founder. Passa se almeno 2 su 3 dicono «è lui».
4. Controlla: volto identico su tutti i fotogrammi (occhi, denti, barba), labiale su sigle, «gl», «sc» e doppie, bordi, voce.
5. Porta l'esito all'amministratore degli strumenti; scrivi il suo sì e lo strumento scelto nel registro del sì.

## Schede

#### A1. Founder che parla in camera, tutto generato

- **Quando**: solo dopo il sì sul provino.
- **Cosa serve**: identità Avatars creata dal founder da 3-5 foto e condivisa con te; audio vero o PVC approvato. Per HeyGen: cattura per Look da almeno 30 s (meglio 2 min), 16:9, 30 fps, treppiede, luce morbida, parete liscia, gesti piccoli e mai simbolici.
- **A mano**: lo strumento che ha passato il provino (registro del sì). ElevenLabs: app > Avatars, scegli l'identità, lo Style (abiti, sfondo, luce) e il PVC condiviso, genera. HeyGen: carica l'audio, bozza su Avatar IV, finale su Avatar V.
- **Con Claude Code**: nessuna strada; solo a mano.
- **Controlli**: clip di 60 s al massimo, frontali; labiale; somiglianza della voce; mani.

#### A2. Persona inventata

Non si fa (§2).

#### A3. Da foto a video parlato

- **Quando**: solo dopo il sì sul provino.
- **Cosa serve**: foto originale dagli Assets del workspace (§3): fotocamera posteriore, 1-2 m, bocca chiusa, sguardo in camera, mai selfie né foto da WhatsApp; audio vero o PVC approvato.
- **A mano**: lo strumento che ha passato il provino (registro del sì). Sito Higgsfield > Lipsync Studio (Kling Avatars 2.0): carica foto e audio, genera.
- **Con Claude Code**: fai prima una prova piccola.
  1. `#W56`: clip muta dalla foto, `seedance_2_5`, `mode:"omni_reference"`, `generate_audio:false`, `resolution:"1080p"`.
  2. `#W62`: un solo lip sync, `model:"sync_so"` con `input_video` e `input_audio`.
  - Mai la voce in `audio_references`.
- **Controlli**: il volto degrada dopo 10-15 s, quindi spezzoni brevi; mani; sfondo che «respira»; labiale sulle frasi difficili.

#### A4. Founder narratore sopra un video esistente

- **Cosa serve**: diritti sul video annotati nel registro dei diritti; un take via B del founder alla parete, con la voce vera (§5).
- **A mano**: scontorna il take (B10). Consegna take, matte e audio: chi monta compone il badge o il cutout.
- **Con Claude Code**: `#W49` o `#W59` per lo scontorno.
- **Regola**: per un founder non usare la modalità del workflow Narration che rigenera la voce.
- **Controlli**: bordi, luce coerente col video.

#### A5. Clip di ascolto (riempitivo del podcast)

- **Cosa serve**: 2 foto reali del founder (§3) e l'angolo del set.
- **A mano**: `_docs/ricette/RICETTA_clip_ascolto_podcast.md`: fotogramma di scena con `gpt_image_2`, pelle con `seedream_v5_pro` senza toccare il volto, poi sito Higgsfield > Video > Seedance 2.5 con fotogramma e foto reale.
- **Con Claude Code**: `#W56` con i parametri dell'Appendice B.
- **Regola**: chi ascolta resta fermo: togli i cenni dal prompt della ricetta.
- **Controlli**: volto fedele, bocca chiusa, mani, niente cifre o pseudo-lettere. Nella nota di consegna chiedi il crop 1,4-1,5x: l'inquadratura esce larga.

# 7. Video senza founder

Consegna sempre a chi monta (§14).

## B-roll, plate e loop

- **A mano**: sito Higgsfield > Video, Seedance 2.5 o Kling 3.0.
- **Con Claude Code**: `#W56`, `resolution` esplicita, `generate_audio:false`. Con Seedance fai la bozza con `draft:true` a 480p e il finale a 1080p con `draft_job_id` entro 7 giorni.
- **Loop**: Kling 3.0 pro con la stessa immagine come inizio e fine (Appendice B).
- **Controlli**: chiusura del loop con `_log/review_video.py`; palette (§9).

## Hook brevi da 3 s

1. Genera l'immagine di start (§9).
2. A mano: sito Higgsfield > Video > Kling 3.0 pro, image-to-video, 3 s, audio spento. Con Claude Code: `#W57` per l'immagine, poi `#W56` con i parametri «Hook da 3 s» dell'Appendice B. Mai text-to-video: esce slavato e fuori palette.
3. Aggiungi al prompt la frase «dark and low-key» dell'Appendice B.

## Explainer e video narrati senza volto

| Caso | Strada | Chi |
|---|---|---|
| Testo, numeri, grafici esatti | Claude Motion, solo a mano: nell'app Claude (web o desktop, posto Team) scrivi `/motion` e la descrizione, poi Export > MP4; non in Claude Code, dove `/motion` apre le gallerie Higgsfield | → chi monta |
| Video narrato faceless, su richiesta esplicita | `#W68` (cloud), solo con Claude Code | → chi monta |
| Explainer HTML | `#W38` (HyperFrames locale) | Chi monta |

- Testi e voce approvati prima. Voce: C1.
- Claude Motion: in una prova piccola controlla durata e formati 9:16 e 4:5 dell'MP4. È materiale (§14): il finale lo fa chi monta.

## Promo dal sito

La fa chi monta con `#W39`, solo dopo la conferma sul sito del §11, punto 4.

## Motion graphics e logo

Li fa chi monta, con `#W36`, dai file ufficiali del marchio (§3). Mai un logo generato.

## Varianti di uno stesso pezzo

- Lingue, copy e formati: chi monta, `#W55`.
- Varianti generate di uno spot da 4-30 s: sito Higgsfield > Ads Studio > Ad Multiplier, oppure `#W71` (`model:"ad_multiplier"`).

# 8. Audio e voce

Ordine della voce e divieti: §2. Impostazioni: Appendice B.

Consegna a chi monta (§14) un WAV 48 kHz per traccia, con nome `<ID>_<battuta>_<EN|IT>_vNN.wav`. Scarica il WAV (o l'MP3 a 192 kbps se il WAV manca) e convertilo:

```
ffmpeg -i <scaricato> -ar 48000 -c:a pcm_s24le <ID>_<battuta>_<EN|IT>_vNN.wav
```

#### C1. Voiceover senza founder

- **Cosa serve**: testo approvato, numeri e sigle per esteso; voci di brand (nome e `voice_id` EN e IT) dal decision log. Se mancano, le sceglie chi approva i testi fra libreria e Voice Design (Voices > My Voices > Add a new voice > Voice Design); annotale lì.
- **A mano**: app ElevenLabs > Text to Speech > modello `eleven_v4`, lingua, voce di brand. Un file per lingua.
- **Con Claude Code**: connettore ElevenLabs: `voice_id` da `creative_list_voices`, poi `creative_generate_speech` con `eleven_v4`, la lingua e `estimate_only:true`, poi con `generations_count:1`; nella risposta controlla il modello usato. Senza tool `creative_*`, lavora a mano.
- **Controlli**: ascolta in cuffia e dall'altoparlante del telefono.

#### C2. Voce del founder e PVC

Se manca la battuta registrata, usa il PVC del founder nella stessa lingua. L'IVC (1-2 min puliti, spunta di consenso) serve solo per le prove e non si pubblica.

**Registrazione per il PVC (il founder)**

- 45-60 min in IT e 30-45 min in EN, una lingua per sessione, stessa stanza e stesso microfono, tutto entro 48 h.
- Parlato naturale, un solo stile, pause fino a 1,5 s, niente riempitivi né musica.
- WAV 44,1 kHz/16 bit, da −23 a −18 dB RMS, picco −3 dB. Mai file passati da app di messaggistica.

**Creazione e condivisione (solo il founder, con il proprio accesso)**

1. Voices > + > Professional Voice Clone > carica i file.
2. Fai la verifica al microfono con la stessa attrezzatura; leggi ogni riga una volta.
3. Attendi l'addestramento (3-6 h, fino a 24).
4. My Voices > passa sul nome della voce > + accanto a «Eleven v4».
5. Tre puntini > Share Voice > aggiungi chi produce i contenuti.

Un clone per lingua. Nome: `<Ruolo>-<LINGUA>-v<n>`.

**Uso**

- **A mano**: Text to Speech con la voce condivisa, `eleven_v4`, lingua della voce.
- **Con Claude Code**: come C1, con il `voice_id` della voce condivisa.
- **Controlli**: ascolto alla cieca contro una registrazione vera non usata per il clone; velocità rispetto alla persona; sì scritto del founder.

#### C3. Doppiaggio IT-EN (solo ripiego)

Prima scelta: il founder registra il take EN. L'italiano dei founder non si doppia mai.

- **A mano**:
  1. App ElevenLabs > Dubbing > carica il video (sotto 1 GB) > lingua EN.
  2. Speaker similarity 7; abbassala se l'EN suona innaturale, alzala se non sembra lui.
  3. Genera, correggi trascrizione e traduzione, rigenera i segmenti.
  4. Scarica solo l'audio: il video del dubbing non si pubblica.
  5. Fai un solo lip sync (C4).
- **Con Claude Code**: `#W62` con `dubbing`, `target_language:"eng"`. È senza preflight: prova prima 10 s (Appendice B). Mai `voice_change` dopo.
- **Controlli**: sigle (SEO, API), numeri, «th», «w», «r».

#### C4. Lip sync su volto reale

- **Cosa serve**: girato con il volto visibile, audio pulito e approvato.
- **A mano**: sito Higgsfield > Lipsync Studio. Ripiego: app ElevenLabs > Image & Video > Sync 3, se l'amministratore degli strumenti l'ha approvato.
- **Con Claude Code**: `#W62` con `generate_video`, `model:"sync_so"`, `medias` con ruoli `input_video` e `input_audio`, `sync_mode`.
- **Regola**: un solo passaggio, dopo l'edit visivo (§12).
- **Controlli**: labiale su frasi difficili, denti, bordo della bocca.

#### C5. Pulizia, trascrizione e SRT

- **A mano**:
  1. App ElevenLabs > Voice Isolator > carica audio o video (fino a 500 MB e 1 h) > scarica.
  2. Speech to Text (Scribe v2) > attiva timestamp per parola e diarizzazione > aggiungi nomi e sigle come termini chiave > esporta SRT.
- **Con Claude Code**: via locale `#W49` (`npx hyperframes transcribe`; il modello si scarica solo con il sì, §3).
- **Controlli**: nomi, sigle e termini tecnici a mano; SRT EN e IT.

#### C6. Musica ed effetti

- **Musica**: la sceglie chi monta. Musica ElevenLabs solo se l'amministratore degli strumenti ha verificato la licenza e l'ha autorizzata.
- **SFX**, solo a mano: app ElevenLabs > Sound Effects > prompt breve in inglese, per esempio «Soft whoosh, then a low impact» > durata fino a 30 s, Loop se serve > scarica WAV 48 kHz. Un loop esce solo in MP3: convertilo con il comando sopra.
- **Mix e loudness**: chi monta (`#W90`).

## Quando usare l'audio di Higgsfield

- `sync_so` (C4) e `dubbing` come ripiego (C3), con `#W62`.
- `generate_audio` solo per un voiceover senza founder, se ElevenLabs non è disponibile. Indica sempre l'accento: il default è inglese americano.

# 9. Immagini e foto

Ogni immagine esce senza testo, lettere, numeri, marchio o esagoni. Annota ogni generazione nel log delle generazioni (§15).

| Lavoro | A mano | Con Claude Code |
|---|---|---|
| Key visual e fondali | Sito Higgsfield > Image, `nano_banana_pro` 2k (in 16:9 `seedream_v5_pro`) | `#W57` (`gpt_image_2_5`; alfa con `background:"transparent"`) |
| Ritratto del founder | Sito Higgsfield > Image, `gpt_image_2` con 2 foto reali, poi `seedream_v5_pro` per la pelle | `#W57` |
| Copertine e thumbnail | Fondo dal sito, titolo impaginato dopo | `#W78` |

- **Fondali**: soggetto nel 35-40% basso, 60-65% alto pulito.
- **Ritratti**: una foto reale del founder sempre fra i riferimenti (§3); consenso controllato; ogni ambiente nuovo approvato prima di animarlo. Soul ID (20-80 foto originali) lo crea il founder (§1).
- **Thumbnail**: titolo e grafica li mette chi monta o il template. Controlla che si legga a 320x180.
- **Famiglie visive**: particelle in murmurazione; costellazione di nodi.
- **Palette scura** (teardown): `#0B1422`, `#F4F6FA`, `#2280DC`, `#8A94A6`, accento raro `#3BE1FF`; Fraunces titoli, Switzer testo, JetBrains Mono numeri. **Palette chiara** (caroselli): `#F4F2ED`, `#07162C`, accento `#2553E8`; Switzer.
- **Ritocchi**: dopo un ritocco locale carica il PNG ritoccato (con Claude Code: `media_upload`) e usa il suo media id, mai il job o l'URL dell'originale.

# 10. Slide, caroselli e documenti PDF

## Caroselli con il template chiaro

Grafiche, PDF e sottotitoli impressi solo in EN; l'italiano va nella caption (§11).

1. Fai approvare i testi (§11): sì di chi approva i testi e, per le affermazioni tecniche, firma di chi firma la parte tecnica, nel registro del sì.
2. Copia i testi approvati in `data/<ID>_EN.json` del template (§3): `headline` e `sub` con gli a capo scelti, `*x*` per l'accento, `scene` col percorso dell'immagine.
3. Genera le scene: `seedream_v5_pro` 3:4 2k (il template ritaglia a 4:5), fascia alta vuota (45% copertina, 50% interni), nessun testo, logo, persona, mano o schermo. Prima una scena «ancora», approvata, poi le altre con quella come riferimento. Con Claude Code: `#W80`.
4. Bozza: apri il terminale in `posts/carousels/v3_light/_template/` e lancia `python build.py data/<ID>_EN.json` (riquadro BOZZA). Leggi gli avvisi in `out/<ID>_EN/qa.json`.
5. Fai confrontare i testi con la bozza resa da una seconda sessione Claude (§11).
6. Chiedi a chi approva i testi il sì sulla bozza resa e scrivilo nel registro del sì.
7. Finale: `python build.py data/<ID>_EN.json --final --out out/<ID>_EN_final` (la bozza resta in `out/<ID>_EN/`), poi la consegna qui sotto.

Serve internet per i font. Percorsi di output sotto i 250 caratteri. Il contatore «n/N» lo mette Instagram: non va nelle immagini. Con Claude Code chiedi di compilare il JSON e lanciare `build.py` (nessuna etichetta).

## Slide e PDF tecnici con il kit

1. Estrai `posts/teardowns/out/kit/sersan_td_kit_v3_1.zip`.
2. Bozza: `python kit/build_deck.py <contenuto>.json <cartella>`. Serve LibreOffice.
3. Finale, dopo il sì sui testi e la firma tecnica: stesso comando con `--final`, nella cartella di consegna.
4. Accetta solo se `_qa.json` ha `"pass": true`, `"warnings": []` e zero link.

Con Claude Code: `#W80` (nel sandbox, `sandbox_exec`). Regole: 10 tavole 1080x1350, CTA solo all'ultima; `sersan.io` come testo all'ultima tavola solo con la conferma sul sito del §11, punto 4.

## Consegna a chi gestisce i post

- Copia i finali in `PUBBLICAZIONE/`: le slide come `<SLOT_ID>_EN_<ratio>_01.png`, `_02` e così via; un PDF come `<SLOT_ID>_EN_<ratio>.pdf`. Lo `SLOT_ID` è nel calendario.
- Accanto metti `<SLOT_ID>_caption.md` (EN, `· · ·`, IT) e `<SLOT_ID>_alt.txt`.
- Scrivi `PRONTO` nella colonna `stato` del calendario.

## Altri strumenti

- **Claude Slides e Design**: deck e presentazioni dei founder, export PPTX o PDF.
- **Deck HTML navigabile**: `#W44`, solo con Claude Code.

## moda

Solo se l'amministratore degli strumenti lo autorizza come strumento principale. Niente video, niente founder, niente file con watermark.

1. Installa e accedi; `moda doctor` deve nominare il workspace aziendale.
2. Crea il canvas e metti la BOZZA su un livello separato.
3. Prima dei comandi a pagamento leggi `moda account costs`.
4. Esporta in PDF, o in PNG con `--format png`.

```
npm i -g @moda-design/moda
moda auth login
npx skills add moda-design/moda
moda doctor
moda canvas create --name "<ID>" --size 1080x1350 --category carousel
moda account costs
moda export "<canvas>" --format pdf --output <ID>.pdf
```

## Misure ed export

| Uscita | Formato |
|---|---|
| Carosello Instagram | PNG o JPEG 1080x1350 sRGB, al massimo 10 |
| Documento LinkedIn | Un PDF 1080x1350, pagine uguali, 8-15 pagine |
| Slide IG da un PDF | Pagine rese 1080x1350 |

Altre reti: documento «Gestione dei post».

## Alt text

Uno per slide, sotto i 100 caratteri, scritto guardando la slide finale: `F01: <titolo>. <descrizione>` per i caroselli, `S01: …` per i PDF. Su Instagram solo EN.

## Togliere la BOZZA e verificare

1. Togli solo il riquadro BOZZA (`--final`, o nascondi il livello in moda).
2. Confronta ogni finale con la bozza approvata: deve cambiare solo il riquadro BOZZA. Con Claude Code chiedi un diff pixel; a mano apri i due PNG uno sopra l'altro e alterna la visualizzazione.
3. Controlla copertina e ultima slide.
4. Nei PDF, titolo, oggetto e autore non devono contenere «draft» o «BOZZA». Correggili con exiftool scrivendo un file nuovo.

# 11. Testi per i social

## Struttura

1. In testa «BOZZA da approvare» (§2).
2. EN, poi la riga `· · ·`, poi IT, nello stesso post.
3. CTA una volta per lingua: «Send a project brief.» / «Inviaci un brief di progetto.»
4. «The link is in our profile.» / «Il link è nel profilo.» solo se l'amministratore degli strumenti conferma che la bio porta a `sersan.io/start` e che il sito non mostra datori di lavoro precedenti né certificazioni.

## Hashtag e link

- Instagram: al massimo 3 hashtag in tutto il post. Nessun link in caption.
- LinkedIn e YouTube: zero hashtag.
- Mai link nel primo commento.

## Controlli prima del sì

- Caratteri contati con `len()`.
- Zero «!», emoji, URL, @menzioni, «IA».
- Nessuna parola vietata (§2) né di disclosure: «AI-generated», «generated», «avatar», «synthetic», «generato», «generata».
- Marcatori tolti: `[CHECK …]`, `[NATIVE IT]`, `[DECISION …]`. Segnaposto sostituiti. Nessun rimando a pezzi che non esistono.

A mano rileggi con questa lista; con Claude Code chiedi questi controlli sul file.

## Approvazione e confronto con la bozza resa

1. Passa il testo a chi approva i testi e, se ha affermazioni tecniche, a chi firma la parte tecnica. Scrivi il sì nel registro del sì (§15).
2. Se il testo accompagna grafiche, apri una seconda sessione Claude, indipendente, e falle confrontare ogni testo con la bozza resa, prima del sì sulla bozza (§10). Se correggi un testo già approvato, chiedi di nuovo il sì.

## Limiti dei profili

LinkedIn: headline 220, About 2.600; Pagina: nome 100, tagline 120, About 2.000. Instagram: nome 30, bio 150.

## LinkedIn

Le bozze dei post LinkedIn si fanno con linkedin-skills: documento «Gestione dei post».

# 12. Come si usano gli strumenti insieme

| Lavoro | Strumento | Vedi |
|---|---|---|
| Testi, controlli, caroselli, slide | Claude Code | §10, §11 |
| Voce, pulizia, trascrizione, doppiaggio audio, SFX | ElevenLabs | §8 |
| Impaginazione, se autorizzata | moda | §10 |
| Immagini, edit video, lip sync | Higgsfield | §5-§9 |
| Scontorno e trascrizione locali | CLI HyperFrames | §5, §8 |
| Composito, montaggio, sottotitoli, grafiche, musica | Chi monta | §14 |

## Ordine di lavoro

1. Fai l'edit visivo sul take originale (§5).
2. Prepara l'audio con ElevenLabs (§8).
3. Se serve, fai un solo passaggio di lip sync. Mai due di fila.
4. Passa il pacchetto a chi monta (§14).

## Passaggio dei file

- Scarica ogni uscita nella cartella del pezzo (§14) prima del passo successivo.
- Per un file modificato in locale, carica quel file (§9, Ritocchi).

# 13. Controllo qualità

## Immagini e video generati

- Niente bande nere, cornici, riquadri, bordo da collage.
- Niente glifi, pseudo-lettere, cifre, forme da simbolo (stella, corona).
- Colori nella palette (§9): niente arancio, oro, grigio slavato, foschia.
- Mani e ginocchia giuste, volto fedele alla foto vera.
- Video: bocca chiusa a fine clip, sguardo in camera, loop che si chiude.

## Video modificati

- Fotogrammi a inizio, metà e fine: volto, labiale con l'audio rimesso, mani, capelli.
- Durata, proporzioni, risoluzione, fps e audio con `ffprobe`.

## Audio

- Velocità e somiglianza con la persona, ascolto alla cieca.
- In cuffia e dall'altoparlante del telefono; sigle, nomi e numeri.

## Strumenti

```
python _log/review_video.py out.jpg v1.mp4 v2.mp4
python _log/contact_sheet.py out.jpg img1.png img2.png
python _log/specs_tool.py mark <file relativo> scartato "<motivo>"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration -of json "<file>"
```

`mark` sposta lo scarto in `_scartati/` con il motivo, solo se il file è nel log delle generazioni.

# 14. Consegna al montaggio

## Cartella del pezzo

L'ID del pezzo è quello del copione o della colonna `pezzo` del calendario; se manca, chiedilo a chi monta prima di creare la cartella. Creala nella cartella di consegna che ti indica chi monta:

```
<AAAA-MM-GG>_<ID-PEZZO>/
  00_NOTA_CONSEGNA.md
  01_originali/   file del telefono e WAV, non rinominati
  02_editati/     originale + _<strumento>_vNN
  03_generati/
  04_audio/       WAV 48 kHz: voce, room tone, SFX
  05_testi/       righe approvate EN e IT, trascritto, .srt
  06_progetto/    sorgenti modificabili
  07_qa/          ffprobe.json, contact sheet, note
```

## Nota di consegna

In «BOZZA da approvare» finché i testi non sono approvati.

```
Pezzo (ID):
Formati e lingue:        9x16 / 4x5 / 16x9 · EN / IT
Origine:                 girato / generato / misto
Camera o modello, risoluzione, fps (ffprobe):
Take scelti (battuta → take):
Strumento usato per ogni take (negli editati l'audio è da sostituire con l'originale):
Via (A / B / nessuna), voce (vera / clone):
Testi approvati: file, righe, data, ruolo:
Secondi deboli (timecode):
Scartati e perché:
Musica e SFX: fonte e licenza:
Scadenza:
```

## Nomi e fps

- Originali: non rinominarli. Editati: originale + `_<strumento>_vNN`. Audio: §8.
- Render: `SERSAN_<ID>_<EN|IT>_<ratio>_vNN`. Finali in `PUBBLICAZIONE/`: `<SLOT_ID>_<EN|IT>_<ratio>`.
- Girato 25 fps, generato 24, cattura per l'avatar 30. Non convertire.

## Canale

Solo la cartella di consegna, mai WhatsApp o altre app di messaggistica (ricomprimono). Poi avvisa chi monta con un messaggio aziendale (Teams o email) con il percorso della cartella, senza allegati.

# 15. Registri

Se un file manca, crealo con queste colonne. Non cancellare righe: correggi con una nota datata. I percorsi in `_registri/` sono il default; l'amministratore degli strumenti può cambiarli.

| Registro | Dove | Chi scrive | Colonne principali |
|---|---|---|---|
| Log delle generazioni | `_log/generations.csv` | chi produce i contenuti | file, model, prompt, seed, credits, job_id, status |
| Log delle prove esterne | `_log/prove_esterne.csv` | chi produce i contenuti | data, strumento, input, output, persona, consenso, esito |
| Ledger | `PUBBLICAZIONE/ledger.csv` | chi produce i contenuti, chi gestisce i post | pezzo, canale, via, voce, esito, link, etichette automatiche |
| Claims register | `_registri/claims.csv` | chi firma la parte tecnica | claim, fonte, data, canali, stato |
| Registro dei consensi | `_ref/`; copia di sola lettura in `_registri/consensi_lettura.csv` | l'amministratore degli strumenti | persona, uso, strumento, ID, lingua, data, scadenza, revoca |
| Registro dei diritti | `_registri/diritti_video.csv` | chi produce i contenuti | video, proprietario, uso permesso, prova |
| Registro del sì | `PUBBLICAZIONE/registro_si.csv` | chi produce i contenuti o chi gestisce i post, dopo il sì | data, cosa, ruolo, canale, testo del sì, riferimento |
| Decision log | `_registri/decision_log.csv` | il ruolo che decide | data, decisione, alternativa scartata, fonte, responsabile, scadenza, revisione |
| Calendario | `PUBBLICAZIONE/calendario.csv` | chi gestisce i post | data, canale, formato, pezzo, stato, file |
| Numeri del lunedì | `PUBBLICAZIONE/numeri.csv` | chi gestisce i post | documento «Gestione dei post» |
| Battute approvate | `scripts/battute/BATTUTE_master.csv` | chi produce i contenuti | id, lang, text, status, approvato da, data |

- Prima di ogni pezzo con un founder controlla nella copia dei consensi persona, uso, strumento e scadenza.
- Log delle generazioni: con Claude Code chiedi di registrare ogni generazione (`_log/specs_tool.py add` prima, `done` a job finito); a mano aggiungi una riga in `_log/generations.csv` con file, model, prompt, credits, job_id (dall'URL del risultato) e status.

# 16. Costi e crediti

- Non c'è un tetto di spesa e non serve approvazione.
- Leggi comunque il costo prima di generare, per scoprire parametri sbagliati: a mano sul pulsante Generate; con Claude Code `get_cost:true` (Higgsfield) o `estimate_only:true` (ElevenLabs); in moda `moda account costs`.
- Senza preflight (costo non leggibile prima): `generate_*_batch`, `upscale_video`, `remove_background`, `execute_preset`, `dubbing`, `motion_control`. Ricontrolla i parametri prima di inviare; per un batch leggi il costo di un `generate_*` singolo.
- Non rilanciare per riprovare: guarda prima l'esito.
- Saldo con Claude Code: `select_workspace` sul workspace aziendale, poi `balance` e `transactions`.
- Crediti finiti: chiedi la ricarica all'amministratore degli strumenti. Mai un altro account.

# Appendice A. Con Claude Code: il plugin e le etichette

## Il plugin `contenuti-sersan`

Porta l'instradamento ai workflow con le etichette `#Wnn`, le regole di brand all'avvio e una conferma sulle scritture in Metricool.

1. Installalo dal terminale (PowerShell o Git Bash, non dentro Claude Code), dopo `gh auth setup-git` (§3); poi riavvia Claude Code:

```
claude plugin marketplace add SerSan-AI-Studio/SERSAN-marketing --sparse .claude-plugin _plugin
claude plugin install contenuti-sersan@sersan-marketing
```

2. Per aggiornarlo: `claude plugin marketplace update sersan-marketing`, poi riavvia Claude Code.
3. Se l'amministratore degli strumenti lo distribuisce dall'organizzazione Claude, con il login del tuo posto Team compare come `contenuti-sersan@synced`: salta il punto 1. Non compare se entri con `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper` o `--safe-mode`.
4. Se sul PC gli stessi hook sono già in `settings.json`, spegni il plugin, altrimenti partono due volte: `claude plugin disable contenuti-sersan@sersan-marketing` (o `@synced`).

## Etichette di chi produce i contenuti

| Etichetta | A cosa serve |
|---|---|
| `#W49` | Scontorno gratis delle persone, trascrizione locale |
| `#W56` | Video generato, loop, clip di ascolto, Seedance edit |
| `#W57` | Immagini e fondali |
| `#W58` `#W59` | Upscale; scontorno a crediti, anche di oggetti |
| `#W60` | Reframe AI, se lo chiede chi monta |
| `#W62` | Lip sync `sync_so`, prova di `dubbing` |
| `#W63` | Genjutsu: vestiti, oggetti, soggetto, moto, stili |
| `#W68` | Video faceless nel cloud |
| `#W71` | Ad Multiplier: luogo, add, remove, varianti |
| `#W78` `#W80` `#W44` | Fondi di copertine; scene senza testo e kit; deck HTML |

## Strumenti MCP

**Higgsfield**
- Prima: `get_workflow_instructions` senza argomento, `balance`, `models_explore {action:"get", model_id}`; prima di generare `get_cost:true`. Parametri di `generate_video`: nelle schede.
- In `medias` solo `media_id` confermati o `job_id` completati, mai URL. File locale: `media_upload`, poi `curl.exe -f -X PUT --upload-file "<file>" "<upload_url>"`, poi `media_confirm` dopo l'HTTP 200.
- Attesa: `jobs_wait {jobs:[{index, job_id}], timeout_seconds:15}`.

**ElevenLabs**: tool `creative_*` (C1).

**moda**: CLI e comandi in §10.

## CLI HyperFrames

```
npx hyperframes transcribe audio.mp3 --to srt -o subs.srt
npx hyperframes catalog --query "<parole>" --json
```

- Scontorno (B10) solo di persone, in `.mov`, mai `.webm`. Sull'italiano mai modelli `.en`.
- Se un comando non risponde come qui, avvisa il responsabile del toolchain.

## Avvisi del router

Se il router propone una strada diversa dalla scheda, vale la scheda. Il plugin avvisa su luce (B3), avatar da foto (A3), voce clonata (C2), traduzione del video (C3) e carosello (§10).

# Appendice B. Prompt e parametri pronti

## Modelli di prompt

**Genjutsu Object Swap, luogo** (a mano, higgsfield.ai/genjutsu):
```
Object swap: replace ONLY the background/location with the office in Reference Image 1. Keep the speaker exactly as filmed: same face, expression, lip movements, hands, wardrobe, framing, camera and timing. Match the lighting direction and color temperature of Reference Image 1 on the speaker. No new people, no text, no logos.
```

**Sostituzione del soggetto** (`hf_mult_replace_object`; in `<…>` il soggetto da sostituire):
```
Replace only <the man in the blue shirt> with the person in the reference images. Preserve the original background, other people, camera movement, timing, lighting direction, pose, and interaction.
```

**Ad Multiplier Edit** (un `@ImageN` per ogni persona). L'ultimo paragrafo è obbligatorio: non toglierlo.
```
Edit @Video1: move the scene to the location in @Image1. Keep the speaker from @Video1 unchanged: face, expression, lip movements, gestures, wardrobe, framing, camera, cuts and timing. Match the lighting of @Image1. No new people, no text, no logos.

Preserve every caption, subtitle, and other untargeted on-screen text element from @Video1 exactly as it appears, including its wording, styling, placement, animation, and timing. Text physically attached to a replaced target follows that replacement.
```

**Hook da 3 s**, frase da aggiungere al prompt:
```
The frame stays dark and low-key, deep navy (#0B1422) dominant from start to end; the haze stays subtle and never washes out the frame
```

**Video Seedance**: Subject, Action, Environment, Camera, Style, Constraints. Da 60 a 100 parole, un solo movimento di camera, solo frasi al positivo, niente testo, loghi o watermark.

## Parametri pronti

- **Loop**: `kling3_0`, `mode:"pro"`, `sound:"off"`, `duration:10`, `start_image` uguale a `end_image`.
- **Hook da 3 s**: immagine di start con `#W57`, poi `kling3_0`, `mode:"pro"`, `sound:"off"`, `duration:3`, immagine con `role:"start_image"`.
- **Clip di ascolto**: `seedance_2_5`, `mode:"omni_reference"`, `resolution:"1080p"`, `duration:10`, `aspect_ratio:"16:9"`, `generate_audio:false`; `image_references` = fotogramma di scena e foto reale, nessun altro.

## Impostazioni ElevenLabs

- Modello `eleven_v4`, `language_code` `it` o `en`.
- Stability 0,5; Similarity 0,75. Con un PVC, Clone Strength 0%, poi su a piccoli passi. Annota ogni cambio nella nota di consegna.
- Scrivi numeri e sigle per esteso. Pause con la punteggiatura, mai `<break>` su v4.

## ffmpeg

```
ffmpeg -i out.mp4 -i src.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -shortest fix.mp4
ffmpeg -i in.mp4 -t 10 -c copy test.mp4
```

Riga 1: rimette l'audio originale (`out.mp4` uscita dello strumento, `src.mp4` segmento originale). Riga 2: prova da 10 s.
