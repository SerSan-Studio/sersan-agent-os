# Backup & Disaster Recovery Strategy

**Data**: 2026-07-17 (riscritto)
**Stato**: PARZIALE — backup locali automatizzabili e verificabili; **copia off-site: codice pronto, infra da provisionare** (Azure Blob GRS + managed identity, decisione founder 2026-07-17 — vedi `backup_offsite_azure.md`)

> **Cosa è cambiato rispetto alla revisione 2026-04-17.** Il documento precedente era
> marcato ACTIVE e descriveva la produzione come *Azure PostgreSQL Flexible Server* con
> auto-backup, geo-ridondanza e point-in-time restore a 5 minuti. **Niente di tutto ciò
> è mai esistito.** Quelle risorse vivono solo nel path Terraform, che non ha remote
> state e non è mai stato applicato (vedi `infra/azure/main.tf:14-23`). La produzione è
> una VM singola che gira `docker-compose.prod.yml`, il cui servizio `db` è
> `postgres:15-alpine` su un volume docker locale.
>
> La conseguenza pratica: la procedura di restore documentata (*"Azure Portal >
> PostgreSQL > Point-in-time restore"*) puntava a una risorsa inesistente. Era il
> runbook che un operatore avrebbe aperto durante un incidente. Questo documento
> descrive ciò che esiste davvero.

---

## 1. Componenti da Proteggere

| Componente | Tipo | Criticità | Stato reale |
|---|---|---|---|
| PostgreSQL 15 (leads, campaigns, messages) | Dati applicativi | **CRITICA** | Dump locali; off-site Azure Blob GRS **cablato ma non ancora provisionato** (`backup_offsite_azure.md`) |
| Sessione LinkedIn (`linkedin_profiles.cookie_data`) | Dato nel DB, cifrato Fernet | ALTA | Nessun backup a sé: sta nel dump PostgreSQL, illeggibile senza `FIELD_ENCRYPTION_KEY`. Rigenerabile ri-autenticando |
| `.env` secrets | Configurazione | **CRITICA** | Fuori dal repo; copia nel password manager (da confermare) |
| Celery beat schedule | Stato runtime | BASSA | Rigenerato al restart, nessun backup necessario |

PostgreSQL è anche il **broker Celery** (kombu `sqla+`) e il result backend: non esiste
un Redis da cui ricostruire lo stato delle code. Perdere il DB significa perdere insieme
dati applicativi e coda di lavoro.

## 2. PostgreSQL — com'è davvero

### Produzione
- **Dove sta il database**: **Supabase** (AWS eu-west-1), raggiunto con `DB_DSN`
  (`scripts/ops/_db_target.sh`). Misurato il 2026-10-08: `Target: dsn
  …pooler.supabase.com`, Postgres 17.6. ⚠️ Fino al 2026-10-09 questa riga diceva
  «servizio `db` del compose, volume `pgdata_prod`»: era vero prima del
  trasferimento e non lo è più, e con lei era falsa la conclusione «perdere la VM
  porta via database e backup insieme».
- **Dump**: `scripts/ops/db_backup.sh` — `pg_dump | gzip -9`, cifrato con `age`,
  retention 35 giorni, con sanity check (`gunzip -t` + verifica header pg_dump) e
  rename atomico.
- **Destinazione locale**: `/opt/backups/sersan/prod/` sulla VM `vm-apps-01`
  (Azure): un'altra macchina e un altro provider rispetto al database, ma **un
  solo disco** — è la copia off-site (sotto) a togliere quel punto singolo.
- **Schedule**: `scripts/ops/install_backup_cron.sh --apply` (dump 03:00, verifica
  restore domenica 04:00). Controlla con `--status` se è installata.
- **Backup pre-deploy**: `scripts/ops/deploy_prod.sh:59-65`, best-effort — logga
  `WARN: backup failed, proceeding anyway` e **prosegue**. Non contarci come rete.

### Cosa la retention non cancella mai
Tre criteri, in ordine, e il terzo è quello che manca in quasi tutti gli script
di backup:

1. **L'età** (`RETENTION_DAYS`, default 35) decide *quali* file sono candidati.
2. **Il pavimento** (`BACKUP_MIN_KEEP`, default 3) decide *quanti* possono
   sparire: i più recenti restano anche se sono tutti oltre la soglia. Serve al
   caso in cui i backup si fermano per settimane e la prima notte buona
   cancellerebbe tutto lo storico.
3. **La prova** — dal 2026-09-02. L'artefatto che l'ultimo drill di restore ha
   davvero aperto (`${OPS_EVIDENCE_DIR}/restore_drill.json` → `dump_file`,
   `offsite_blob`) è escluso per nome, in aggiunta ai primi due.

Il terzo criterio esiste perché i primi due non si parlano con la cadenza del
drill. I backup sono notturni, il drill settimanale: il file provato è di norma
più vecchio dei tre tenuti dal pavimento, e finora lo salvava soltanto il fatto
che `RETENTION_DAYS=35` è più larga di sette giorni. Nessuno impone quella
relazione — abbassare `RETENTION_DAYS` per recuperare disco cancellava il solo
punto di ripristino mai dimostrato recuperabile, senza un errore.

Tre conseguenze operative:

- **Ricevuta illeggibile ⇒ nessuna cancellazione**, né locale né off-site. Un
  file che c'è e non si parsa è il caso in cui non si sa cosa si sta per
  cancellare; cancellare è irreversibile, non cancellare no. È lo stesso schema
  già applicato a un `RETENTION_DAYS` che non si capisce.
- **`python3` assente ⇒ nessuna cancellazione, e il messaggio nomina il binario.**
  Serve a leggere la ricevuta; senza, non si sa cosa proteggere. È un guasto
  diverso da una ricevuta corrotta — quella la ripara il prossimo drill, questo
  lo ripara `apt install python3` — e raccontarli con la stessa frase manda a
  leggere un file sano mentre la retention resta ferma ogni notte.
- **Ricevuta assente ⇒ retention normale.** Assente ≠ illeggibile: una VM appena
  installata non ha mai fatto un drill, e bloccarla riempirebbe il disco fino a
  fermare i backup. Non c'è niente da proteggere, quindi valgono età e pavimento.
- **Off-site, se il cutoff colpisse il blob provato, la retention off-site salta
  tutta.** `az storage blob delete-batch` non sa escludere un nome, quindi non si
  prova a escluderlo: si chiede prima chi cadrebbe e, se cade quello, non si
  cancella. Riparte da sola al primo drill su un blob più recente del cutoff.

Il difetto e i tre esiti sono inchiodati da
`tests/test_retention_spares_the_only_proven_recovery_point.py`, che esegue
`db_backup.sh` vero contro una directory temporanea.

### Il chiaro su disco: chi lo legge, e per quanto (dal 2026-10-08)
Misurato in prod il 2026-10-06: i dump erano `-rw-rw-r--` (leggibili da ogni
account della VM), la copia in chiaro di ogni notte restava accanto alla sua
gemella cifrata, e niente veniva più cancellato dal 2026-08-26 — la retention
generica gira **dopo** lo stadio off-site, che in prod esce 7 finché Azure non
c'è. Totale: 6,2 GB. La policy in `db_backup.sh` gira **prima** dell'off-site,
quindi vale anche oggi:

1. **Proprietario-solo, sempre.** Directory `0700`, ogni dump `0600`, compresi
   quelli già presenti; `umask 077` nello script, nel dump pre-deploy
   (`deploy_prod.sh`) e in quello pre-rollback (`rollback_prod.sh`).
2. **Il chiaro notturno se ne va quando la gemella cifrata esiste**, tranne il
   più recente finché `BACKUP_KEEP_LOCAL_PLAINTEXT=true` (il drill locale
   settimanale lo apre senza chiave privata). Mai un chiaro senza gemella: sarebbe
   l'unica copia di quella notte.
3. **Il dump pre-deploy / pre-rollback** è in chiaro per progetto (un rollback
   deve poterlo ripristinare senza la privata, che non sta sulla VM): resta
   `BACKUP_PLAINTEXT_KEEP_DAYS` giorni (default 7), poi se ne va.

**2 e 3 cancellano solo davanti a un sostituto VERIFICATO**: questo run ha
cifrato, *e* l'ultimo drill passato ha aperto un artefatto cifrato **con la
chiave con cui questo run cifra** (`restore_drill.json`: `status=ok` e
`decrypted_with` uguale al `CRYPTO_KEY_ID` del run — non il `key_id_match`
della ricevuta, che confrontava con la chiave corrente *al momento del drill* e
farebbe ereditare a una chiave ruotata la promozione di quella vecchia). Una
gemella cifrata che nessuno ha mai decifrato non è un sostituto: sulla VM la
privata non c'è, quindi solo un drill può dire che quel ciphertext si apre. Un
drill che ha aperto un dump in chiaro (`decrypted_with=none`, cioè l'ultimo di
prod, `source=local`) non prova niente, quindi anche il file che ha provato
resta. Senza prova la riga di log dice perché (`nessun-drill`,
`drill-non-su-cifrato-con-questa-chiave`, `ricevuta-illeggibile`,
`python3-assente`) e la ricevuta di backup porta `plaintext_removal` e
`plaintext_removed`.

**Conseguenza per prod**: oggi non viene rimosso niente (il drill è
`source=local`, chiave `unpaired`), e si stringono solo i permessi. Le
rimozioni partono dal primo `prod_dr.yml -f action=restore-offsite` riuscito
con la chiave corrente. `prod_dr.yml -f action=status` riporta, per tipo di
dump, numero, byte e permessi, senza aprire niente.
Test: `tests/test_plaintext_on_disk_is_owner_only_and_bounded.py`, che esegue
gli script veri e prende le ricevute dei drill da `db_restore.sh`, mai scritte
a mano.

### ⚠️ Il rischio aperto
Corretto il 2026-10-09. Il database non sta sulla VM (sopra), quindi perdere la
VM **non** perde dati: perde le copie. Il rischio vero è l'altro verso — perdere
il database (account o progetto Supabase, una migrazione distruttiva, una
cancellazione) quando l'unica copia indipendente è **un disco** della VM. I dump
lì sono cifrati e verificati, ma una copia sola su un disco solo non è una
strategia di recupero.

Lo chiude la copia off-site: Azure Blob GRS (`docs/backup_offsite_azure.md`, la
decisione del 2026-07-17) oppure, finché quell'account non è raggiungibile,
GitHub Releases (stesso documento, §«Provider alternativo»). Finché nessuna delle
due ha una ricevuta remota, la riga di recovery resta rossa.
> **La readiness non finge più il contrario.** Fino al 2026-08-25 il ledger di
> lancio riportava `Off-site backup + restore test proven — PASS` calcolandolo da
> «backup fresco AND restore riuscito», cioè da due proprietà di un file che non
> ha mai lasciato la macchina. Ora `backup_offsite` è una chiave separata che
> passa solo con una ricevuta del remoto, e finché l'infra non è provisionata la
> riga di recovery resta **rossa** — coerente con lo stato PARZIALE dichiarato
> qui sopra. Vedi `readiness.md`.

Il blocco di upload off-site in `db_backup.sh` **non è commentato**: è codice vivo, gated
sulla env var `AZURE_BACKUP_STORAGE_ACCOUNT`, che finché resta vuota lo fa uscire a log
con `Off-site upload SALTATO … backup SOLO LOCALE`. Non manca quindi del codice da
decommentare: manca lo storage account GRS e la managed identity sulla VM
(vedi `backup_offsite_azure.md`), più la env var nel file che
il cron sorgente. Attenzione a non leggere il verde di `[x] Copia off-site scritta` qui
sotto come "off-site attivo": significa scritta, non provisionata.

### Sviluppo (docker compose)
- **Dump**: `docker compose exec db pg_dump -U sersan sersan_outbound > backup_$(date +%Y%m%d).sql`
- **Restore**: `docker compose exec -T db psql -U sersan sersan_outbound < backup.sql`
- Consigliato prima di ogni migrazione Alembic.

## 3. Restore

`scripts/ops/db_restore.sh`. Il **default è non distruttivo**: ripristina in un database
usa-e-getta e verifica cosa è atterrato, senza toccare quello vivo.

```bash
# Verifica che l'ultimo backup sia ripristinabile (sicuro, non tocca il DB vivo)
./scripts/ops/db_restore.sh

# Verifica un dump specifico
./scripts/ops/db_restore.sh --file /opt/backups/sersan/prod/sersan_outbound_2026-07-16.sql.gz
```

Controlla: integrità del gzip, header pg_dump, restore senza errori (`ON_ERROR_STOP=1`),
presenza di `alembic_version`, numero di tabelle, conteggi delle tabelle core, e il delta
sui lead rispetto al DB vivo.

### Restore reale (DISTRUTTIVO)

```bash
./scripts/ops/db_restore.sh --target live --confirm
```

Senza `--confirm` rifiuta di partire. Fa un dump dello stato attuale prima di
sovrascrivere (`*_pre-restore_*.sql.gz`) e si ferma se quel dump fallisce.

Si rifiuta se gira un processo che invia, ripristina in una transazione sola e
lascia ogni invio fermo (`send_stop_switches`). Dopo — procedura completa in
`docs/runbooks/database_restore.md` §3:
1. `docker compose up -d backend frontend` — non i worker né beat
2. `docker exec <backend> alembic current` — deve mostrare la head riportata dallo script
3. Verificare `/health` e un conteggio lead; riconciliare ciò che è partito dopo il dump
4. Solo allora i worker, e lo stop si toglie da `/pilot/`

## 4. Sessione LinkedIn (cookie Playwright)
- **Dove sta davvero**: nel database, colonna `linkedin_profiles.cookie_data` — TEXT
  cifrato Fernet (`backend/models/linkedin_profile.py:47`; migrazione `9877116ae253`
  ha convertito la colonna da JSONB a TEXT cifrato). Il browser riceve lo
  `storage_state` dal DB all'avvio della sessione (`linkedin/browser/login.py:298-305`
  → `launch_browser(storage_state=...)`) e lo riscrive lì dopo il login
  (`linkedin/browser/login.py:265-267`). A parte, `_maybe_refresh_cookies`
  (`linkedin/browser/session.py:75-90`) rilegge la colonna solo per accorgersi che
  `li_at` è scaduto e forzare il re-login.
- **Il volume `playwright_profile` è vuoto per costruzione**: è montato solo in
  `docker-compose.dev.yml:131` e nessuna riga di codice ci scrive — niente
  `user_data_dir`, niente contesto persistente. Un `docker cp` da quella directory
  copia una cartella vuota, e in prod il volume non è nemmeno dichiarato. **Non è un
  asset da backuppare.**
- **Backup**: nessuno separato. La sessione è già dentro il dump del §2 — ma quel dump
  la restituisce leggibile **solo** insieme alla `FIELD_ENCRYPTION_KEY` corretta (§5).
- **Impatto perdita**: sessione LinkedIn da ri-autenticare a mano da `/linkedin/connect/`
  (estensione Chrome che cattura il cookie `li_at`, o email+password). Fastidio, non
  perdita di dati.

## 5. Secrets (.env)
- **Mai** nel repo (già in `.gitignore`)
- Copia cifrata nel password manager del team
- Rotazione webhook secret: `scripts/setup_instantly_webhook_secret.py`
- Recovery: rigenerare da `.env.example` + password manager
- **Nota**: `FIELD_ENCRYPTION_KEY` cifra a livello di campo le credenziali LinkedIn e la
  sessione del browser (`linkedin_profiles.cookie_data`).
  Perderla rende quei campi **irrecuperabili anche avendo un dump del DB.** Un backup
  del database senza quella chiave è parziale.

## 6. Stato dei lavori

- [x] Script di dump con retention e sanity check — `scripts/ops/db_backup.sh`
- [x] Script di restore + verifica non distruttiva — `scripts/ops/db_restore.sh`
- [x] Schedule versionata e installabile — `scripts/ops/install_backup_cron.sh`
- [x] **Copia off-site scritta** — upload su Azure Blob (GRS, managed identity,
      keyless) in `db_backup.sh:91`, con 3 retry ed exit≠0 se fallisce. PR #53.
      ⚠️ **È env-gated**: no-op finché `AZURE_BACKUP_STORAGE_ACCOUNT` non è
      impostata nel job cron sulla VM. Scritta ≠ attiva — vedi
      `docs/backup_offsite_azure.md` e la riga qui sotto.
- [ ] Eseguire `install_backup_cron.sh --apply` sulla VM prod e confermare con `--status`
- [ ] Primo restore verificato in produzione (`db_restore.sh`, modalità sicura)
- [ ] Confermare che `.env` e `FIELD_ENCRYPTION_KEY` siano nel password manager
- [ ] Decidere il destino del path Terraform: applicarlo con remote state, o rimuoverlo

> **Come si controllano le tre righe aperte senza SSH** (la VM è dietro
> WireGuard e questo client non è autorizzato): `gh workflow run
> prod_launch_readiness.yml`. Riporta lo `--status` del cron, i dump più
> recenti con data e dimensione, la coda del log di backup e se
> `AZURE_BACKUP_STORAGE_ACCOUNT` è impostata — tutto in sola lettura, senza
> stampare nessun valore segreto. Il runner self-hosted gira **sulla** VM, che
> è ciò che rende superflua la procedura `scp` documentata altrove.

**Su Terraform**: `backup_retention_days = 35` e `geo_redundant_backup_enabled = true`
sono configurati in `infra/modules/database/main.tf`, ma si applicano a un Flexible Server
che non esiste. Non contano come backup finché quel path non viene applicato davvero —
e oggi non può esserlo, perché il backend azurerm per il remote state è commentato.
