# Production Readiness — Authoritative Ledger

**This is the single source of truth for whether SerSanOutreach may go live.**
Every other readiness/audit/status/handoff document in this repo is historical
and has been marked as such (see [§ Superseded documents](#superseded-documents)).
If any of them disagree with this file, this file wins.

> **A generated report is not a launch approval.**
> The machine block below is regenerated from evidence and can be produced at any
> time — that only proves the *evaluator ran*. Readiness is the separate verdict
> `all_ready`, which is **fail-closed**: it is true only when *every* P0 row is
> `PASS`. A row whose evidence has not been collected is `UNKNOWN`, and `UNKNOWN`
> counts as **not ready**. Because the email and LinkedIn channel gates are
> themselves P0 rows, `all_ready` can never be true while either channel has an
> unresolved launch blocker.

## How to regenerate the machine-verifiable block

```bash
# Repo + GitHub governance only (what CI/a laptop can prove). Exits non-zero
# unless every P0 item passes.
python scripts/ops/readiness_eval.py

# Fold in the live runtime evidence for the real verdict. Run the read-only
# probe first, then pipe its log through the evaluator:
gh workflow run prod_launch_readiness.yml
gh run view --log <run-id> | \
  python scripts/ops/readiness_eval.py --runtime-signals - --no-github --migrations

# Rewrite the <!-- READINESS:BEGIN..END --> block in this file:
python scripts/ops/readiness_eval.py --write-ledger docs/PRODUCTION_READINESS.md

# JSON, for dashboards / CI assertions:
python scripts/ops/readiness_eval.py --format json
```

The evaluator (`scripts/ops/readiness_eval.py`) is **stdlib-only** so it runs on
the prod VM's system Python and in CI without extra deps. Its `evaluate()`
function is pure and is pinned by `tests/test_readiness_eval.py`. Signal
collection is best-effort: `gh`/`alembic` being unavailable yields `UNKNOWN`
(fail-closed), never a crash.

**Exit codes:** `0` = READY (every P0 `PASS`), `1` = NOT READY, `2` = usage
error. Pass `--report-only` to generate the report without asserting readiness.

---

## Baseline (repo state at time of writing — 2026-08-17)

> **Historical — do not read as current.** This section records the 2026-08-17
> starting point. The current state is the generated block below (bound to a
> commit) and `docs/growth_os_capability_map.md` (re-measured 2026-10-05: `main`
> = production = `672bf075`, 107 migrations, one head `3c5e7a9b1d2f`).

| Fact | Value | How to re-derive |
|---|---|---|
| Current `main` commit | `db4ff64` (merge of PR #195) | `git rev-parse origin/main` |
| Deployment commit | *runtime — not a repo artifact* | last successful `Deploy` run's `DEPLOY_SHA`, or `git rev-parse HEAD` in `/opt/apps/sersan-outreach/prod/repo` on the VM |
| Repo visibility | private | `gh api repos/SerSan-AI-Studio/SerSanOutreach --jq .visibility` |

### CI, migrations, containers, workers
- **CI:** `Tests` workflow (`.github/workflows/tests.yml`): `lint → test → integration-test`, plus a non-blocking `audit` (pip-audit). Latest run on `main` HEAD: **green**. `lint` also runs `scripts/gen_code_inventory.py --check`, which fails on duplicate/multiple Alembic heads.
- **Deploy gate:** `Deploy` (`.github/workflows/deploy.yml`) fires on `workflow_run: Tests completed` for `main` and pins `DEPLOY_SHA = workflow_run.head_sha`. ⚠️ Known gap documented in `tests.yml`: the deploy job gates on Tests *completion+conclusion*, not on the `test` job specifically (`needs: test` is not wired in `deploy.yml`). Tightening this belongs to **Prompt 3**.
- **Migrations:** Alembic is the single DDL owner (46 versions in `alembic/versions/`); Django models are `managed=False` (0 Django app migrations). Single-head is enforced in CI (`gen_code_inventory.py`) and re-checkable at runtime via `alembic heads` (`prod_ops.yml`).
- **Containers / workers:** compose source-of-truth is `docker-compose.prod.yml`; workers are `worker-linkedin` (must stay `--concurrency=1 --pool=solo`), `worker-email`, `worker-default`, `beat`. Monitoring stack (Prometheus/Grafana/Loki/Alertmanager) is a **separate** compose at `/opt/apps/sersan-outreach/grafana/` and is **not** in this repo.

### Email readiness (mailbox / domain / SPF / DKIM / DMARC / warmup / Instantly)
- Signals live on `backend/models/domain.py` (`spf_valid`, `dkim_valid`, `dmarc_valid`, `is_blacklisted`) and `backend/models/mailbox.py` (`instantly_warmup_status`, `instantly_warmup_score`, `is_active`). DNS-health lane: `workers/email/dns_health_monitor.py`; warmup mirror: `workers/email/warmup_monitor.py`.
- The **warm-sender gate** (`workers/email/_warm_sender.py`, `EMAIL_REQUIRE_WARM_SENDER=true`) is three-state and fail-closed only on a *registered, measured, cold* sender; a registered-sender ramp (`EMAIL_REQUIRE_REGISTERED_SENDER`) is in `observe`.
- Delivery is **delegated to Instantly** (`backend/clients/instantly.py`); no live SMTP/ACS path. A campaign with no `instantly_campaign_id` parks every message it owns in the HITL queue.
- **Live verdict:** `GET /api/system/readiness` → `email.ready` (`backend/routers/system.py`). This is `UNKNOWN` in the ledger until the runtime probe is ingested.
- ⚠️ **Compliance conflict — read before closing the email-compliance P0 row.** Physical-address enforcement was **removed** and is a **permanent** founder derogation under `docs/adr/ADR-004-pilot-compliance-derogations.md` (`DEROGA PERMANENTE`, 2026-04-29, reconfirmed 2026-07-28; extended beyond the pilot to all campaigns). Opt-out is a text string (`"Rispondi STOP…"`) applied only from step 3 (`OPT_OUT_STEP_THRESHOLD=3`); no clickable unsubscribe, no linked privacy policy. **Prompt 4 of the readiness pack explicitly reverses this ADR.** That is a founder + legal decision, not an engineering fix — the P0 row is owned by `founder+legal`, and eng should not silently re-enable enforcement without that sign-off and an ADR-004 update.

### LinkedIn readiness (account / CAPTCHA / proxy / egress / session)
- Signals on `backend/models/linkedin_profile.py`: `captcha_blocked_at`/`captcha_challenge_type`, encrypted `proxy_url` + `proxy_country/geo_source/geo_confirmed_at`, `active`, `cookie_data`, per-account limits (`connect_daily_limit` etc.), send window (`active_hours_start/end/days`).
- Gates: proxy required via `LINKEDIN_REQUIRE_PROXY` (`linkedin/proxy.py::has_usable_proxy`, currently default `false`), egress via `LINKEDIN_VERIFY_EGRESS` + `prod_egress_check.yml`, per-account budget `LINKEDIN_ACCOUNT_BUDGET_MODE=enforce` with warm-up ramp, send window `LINKEDIN_SEND_WINDOW_MODE=observe`.
- Per prior notes the account is **held pending a manual browser check** (App Challenge); standing founder constraint: *no profile bans*. Automation cannot send until a residential Italian proxy IP is set and `LINKEDIN_REQUIRE_PROXY=true`.
- **Live verdict:** `GET /api/system/readiness` → `linkedin.ready`. `UNKNOWN` until the probe is ingested.

### Backups / off-site / restore-test
- Scripts exist: `scripts/ops/db_backup.sh` (nightly `pg_dump`, 35-day retention, optional Azure off-site when `AZURE_BACKUP_STORAGE_ACCOUNT`/`AZURE_BACKUP_CONTAINER` set), `db_restore.sh` (restore-verification into a scratch DB by default), `install_backup_cron.sh`. Off-site design: `docs/backup_offsite_azure.md`.
- **Whether it actually runs, is recent, and uploads off-site is runtime-only** — and those are **three separate attested keys**, not one. `backup_freshness` (a dump ran), `backup_encryption` (it is not plaintext) and `backup_offsite` (it reached a remote store, which confirmed the blob) are collected independently and may never be derived from one another. Until 2026-08-25 the evaluator computed off-site protection as `backup_freshness AND restore_drill`, and reported a green P0 for a plaintext dump sitting on the same VM as the database. The probe's crontab/log scraping (`READINESS OFFSITE*`) can now only *refute* off-site protection, never establish it — a cron line that looks capable of an upload is not an upload. `UNKNOWN` until ingested. A passing restore test is a required part of this P0 item, and it records **which** copy it restored (`source=local|offsite`).

### Alert delivery
- Two paths: app-level KPI Slack push (`workers/kpi/alerts.py`, `SLACK_ALERT_WEBHOOK_URL`, silently inert if unset) and Prometheus→Alertmanager (Alertmanager config lives outside this repo). Alert rules: `infra/prometheus/rules/{sersan-alerts,email-pipeline-alerts}.yml`, firing-tested by `tests/test_alert_rules_can_fire.py`. Delivery state is `UNKNOWN` until the probe reports the env var / Alertmanager target.

### Security features & branch protection
- **All closed, measured 2026-08-25** (`gh api`, admin token): `main` **is** protected — required status checks `lint, audit, test, integration-test`, `strict: true`, code-owner review required; secret scanning, push protection and Dependabot security updates are all **enabled**; CODEOWNERS is present; workflow `uses:` are SHA-pinned.
- Two caveats that the row above does **not** cover, both deliberate and both worth knowing before reading a green ledger:
  - `enforce_admins: false` and `required_approving_review_count: 0`. Protection applies to non-admins (`enforcement_level: non_admins`); an admin merging with `--admin` bypasses it, which is how this repo's merge train is actually run.
  - GitHub Advanced Security is **off**, so CodeQL cannot upload and `codeql.yml` carries `continue-on-error`. The blocking static-analysis control is `sast_gate` (`lint` running `ruff check --config ruff-security.toml .`), which is required and green.
- ⚠️ This paragraph read "all open — `main` is not protected, secret scanning disabled" from the original 2026-04 audit until 2026-08-25, long after every one of those controls had been switched on. Nothing regenerates it, so it is hand-maintained: **re-measure before quoting it.** The generated block below is the one that is reproducible.

---

<!-- READINESS:BEGIN (generated by scripts/ops/readiness_eval.py — do not edit by hand) -->

**Evidence basis:** commit `99a0de4c8583` &nbsp;·&nbsp; runtime evidence collected `2026-08-20T09:23:00.648058Z`

| Launch decision | Verdict | P0 rows gating it |
|---|---|---|
| email pilot | **NOT READY** ❌ | 18 rows, 5 not yet PASS |
| LinkedIn pilot (manual) | **NOT READY** ❌ | 16 rows, 4 not yet PASS |
| LinkedIn pilot (automated) | **NOT READY** ❌ | 17 rows, 5 not yet PASS |
| COMBINED go-live | **NOT READY** ❌ | 21 rows, 8 not yet PASS |

> A generated report is **not** a launch approval. A verdict is true only when every P0 row gating it is PASS. UNKNOWN — evidence that could not be collected — is fail-closed and counts as not-ready; it is deliberately distinct from FAIL, because "nobody could read this" and "this is switched off" have different fixes. `▫️ NA` rows are informational and never gate.

### P0 — launch blockers
_12 pass · 4 fail · 4 unknown · 1 informational_

| | Item | Channel | Gates | Owner | Exit condition | Evidence | Recovery (when not PASS) |
|---|---|---|---|---|---|---|---|
| ✅ PASS | CI Tests green on main tip | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | GitHub Actions `Tests` workflow conclusion == success for current main HEAD | github.ci.main_tests=success | — |
| ✅ PASS | Database at exactly one migration head | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | `alembic heads` reports exactly 1 head (also gated by gen_code_inventory.py --check in CI) | 1 alembic head, 0 unapplied | — |
| ✅ PASS | main branch protection enforced | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | founder | GitHub branch protection present on main with required status checks (the review policy is reported in the verdict detail, not gated here) | main is protected | — |
| ✅ PASS | Secret scanning + push protection on | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | founder | Repo security_and_analysis: secret_scanning + push_protection == enabled | secret scanning + push protection enabled | — |
| ✅ PASS | Dependabot security updates on | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | founder | Repo security_and_analysis: dependabot_security_updates == enabled | github.dependabot=enabled | — |
| ✅ PASS | Blocking SAST gate (required check, green) | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | The job carrying `ruff check --config ruff-security.toml .` is BOTH a required status check on main AND green. Documented alternative to CodeQL (ruff-security.toml, tests/security/test_sast_gate_bites.py); it satisfies the security requirement only while both halves hold. | blocking SAST job is a required check and is green | — |
| ▫️ NA | CodeQL / GitHub Advanced Security | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | founder | INFORMATIONAL, never gating. CodeQL needs GHAS; this repo is private with GHAS off, so the analyses API answers 403 to every caller — unavailable, not failed. `sast_gate` is the control that gates. | CodeQL/GHAS is NOT ENABLED on this repository — unavailable, not failed. `sast_gate` is the gating control. | — |
| ✅ PASS | CODEOWNERS covers send/auth/migrations/deploy | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | CODEOWNERS file present at repo root or .github/ | CODEOWNERS present (reviewer routing for critical paths) | — |
| ✅ PASS | GitHub Actions pinned to immutable refs | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | Every `uses:` in .github/workflows pins a SHA or trusted immutable ref | repo.actions_pinned=pinned | — |
| ❔ UNKNOWN | Commercial email compliant by construction | email | email pilot | founder+legal | capability `email_compliance_enforced` (backend/services/email_compliance.py + workers/email/_compliance.py, exercised by executable tests naming evaluate_campaign_compliance / ensure_opt_out_footer / is_opt_out_reply) AND the LIVE `email_compliance` verdict clean. ⚠️ CONFLICT: closing this reverses ADR-004 (physical-address enforcement is a PERMANENT founder derogation, 2026-04-29/2026-07-28) — needs a founder + legal decision, not an eng fix. The row is red on the live derogation, never on a filename. | email_compliance_enforced: 186 test eseguibili in 12 file, e CI e' verde per il commit deployato — ma il verdetto di compliance VIVO non e' stato raccolto, quindi questa riga non afferma che le deroghe siano chiuse | Founder and counsel answer docs/compliance_decision_checklist.md and record it on the campaign; a named derogation keeps sending and leaves this row red by design (ADR-030). Engineering acts only if the capability tests fail. |
| ✅ PASS | Durable suppression / opt-out subsystem | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `suppression_durable`: backend/services/suppression.py present, and executable tests naming record_suppression / revoke_suppression / suppress_lead_if_listed exercise it (immutable suppression + retriable opt-out outbox + idempotent webhooks) | suppression_durable: 121 test eseguibili in 13 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Deterministic delivery / no duplicate sends | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `idempotent_send`: backend/services/delivery.py present, and executable tests naming claim_attempt / not_sendable_reason exercise it (transactional claim + idempotency key; two-worker + crash-after-side-effect cases) | idempotent_send: 168 test eseguibili in 13 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Instantly integration contract-verified | email | email pilot | eng | capability `instantly_contract`: backend/clients/instantly.py present, and executable tests naming InstantlyClient / InstantlyAPIError exercise it (captured-payload contract tests; webhook scoped to workspace/campaign/lead/message) | instantly_contract: 642 test eseguibili in 42 file, e CI e' verde per il commit deployato | — |
| ❌ FAIL | Email go-live gate passes (live) | email | email pilot | ops | /api/system/readiness reports email.ready == true on prod | email blockers: no active mailbox is registered — EMAIL_REQUIRE_WARM_SENDER is on but the gate fails open on senders it cannot match, so nothing is verifying warmup.…, Sending-domain DNS (SPF/DKIM/DMARC): UNKNOWN — No sending domain can be derived, because no active mailbox is registered. Fix: Register the sending m…, Email mailbox state: FAIL — No active mailbox is registered. The warm-sender gate matches senders by exact address and fails OPEN on senders it canno…, Instantly campaign mapping: FAIL — 1 of 1 ACTIVE email campaign(s) have no Instantly campaign id: 'SerSan Pilot 50'. Their approved messages are with… | Clear each email blocker on /internal-metrics/status/ — every one names its own fix — then re-run prod_launch_readiness.yml. |
| ❔ UNKNOWN | An email reply provably reaches us and stops both channels | email | email pilot | ops | `email_reply_ingestion` is PASS: the backend read one real `inbound_events` row for an OPERATOR-OWNED self-test conversation, saw the lead's journey change, saw the journey enrollments stopped, found nothing for that lead satisfying SENDABLE_MESSAGE_SQL on EITHER channel, confirmed the Unibox renders the reply to a person, and re-offered a duplicate of the same event and had it refused. `inbound_reply_sync.email` cannot stand in: it reports that SOME inbound event arrived recently, so it is green both when replies stop outreach and when nothing has ever exercised the path — and none of its branches says whether a reply STOPPED anything, showed itself in the Unibox, or survived a retry. | email_reply_ingestion: never observed — run prod_email_reply_selftest.yml | Run prod_email_reply_selftest.yml: prepare, reply from the operator-owned mailbox, verify (docs/email_reply_selftest.md). |
| ❌ FAIL | Production recovery readiness (encrypted + off-site + restored) | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | THREE separately attested facts, none inferred from another: `backup_encryption` (the artifact is not plaintext, and the receipt names WHICH key), `backup_offsite` (db_backup.sh read the blob back out of the remote store and recorded the receipt), and `restore_drill` — which must have restored the REMOTE object (`source=offsite`), not the local file. A local drill proves the dump is readable and leaves the credentials, the remote read permission and the decryption key untested, which is the whole of what a recovery depends on; an unrecorded provenance fails for the same reason. The drill must also have opened it with the key db_backup.sh encrypts with TODAY (`keyid=match`): a rotation to a public key whose private half nobody archived leaves every other signal green and no dump openable. A fresh local dump satisfies NONE of them: freshness is `backup_freshness`, which is a separate, non-gating row. | no verified off-site copy (l'ultimo upload off-site non è verificato (offsite=disabled)) | Founder provides the Azure storage account and credentials; operations then runs prod_dr.yml for an encrypted off-site backup and a restore drill FROM the remote object (docs/runbooks/dr_closure_sequence.md). |
| ❌ FAIL | Alert delivery PROVEN to reach a human | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | A drill the receiver acknowledged: one synthetic alert per critical category, injected through the real Alertmanager, with `alertmanager_notifications_failed_total` unchanged across the injection. Configuration does not close this row — neither a set the operator channel (it carries the KPI push, not Prometheus alerts) nor an Alertmanager whose config merely loads. The evidence expires in 24h, because a webhook can be revoked in an afternoon. | alert delivery never proven: no acknowledged Alertmanager drill. Run prod_alert_drill.yml -f send=true. | Founder names the destination (the Telegram chat_id); operations runs prod_alert_drill.yml and a person acknowledges it with prod_alert_ack.yml (docs/runbooks/alert_delivery_drill.md). |
| ✅ PASS | Global kill switch tested | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | capability `kill_switch` exercised by executable tests (pauses all prospect-facing sends without disabling review/recovery) | kill_switch: 359 test eseguibili in 20 file, e CI e' verde per il commit deployato | — |
| ❌ FAIL | LinkedIn account can act at all (live) | linkedin | LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | /api/system/readiness reports no LinkedIn blocker that a human operator cannot work around: a held CAPTCHA, no connected account, more than one active profile, an unreconciled delivery ledger or an engaged kill switch stop a hand-run pilot exactly as hard as an automated one. The saved session, the egress proxy and the send window do not — all three govern OUR browser, and in the manual pilot there is no browser of ours. | linkedin blockers: all connected LinkedIn accounts are CAPTCHA-blocked — clear the challenge to resume automation, CAPTCHA / authentication challenges: FAIL — 1 of 1 active account(s) are held on a security challenge (url-marker:/checkpoint/). A held account perfo… | Clear each LinkedIn blocker on /internal-metrics/status/ — connect an account, have the account holder clear a held challenge, reconcile delivery_unknown (docs/runbooks/unknown_delivery_reconciliation.md), release a stop only deliberately. |
| ❔ UNKNOWN | Unattended LinkedIn envelope engaged (live) | linkedin | LinkedIn pilot (automated) | ops | EVERY control in `LINKEDIN_AUTOMATION_CONTROLS` is separately PASS, each read from the evidence row that measures it: automation send mode declared by every process, at least one profile not locked to manual, LINKEDIN_SEND_WINDOW_MODE=enforce, LINKEDIN_ACCOUNT_BUDGET_MODE=enforce, a saved session, verified egress, no held account, and proven reply ingestion. A missing row is UNKNOWN, never PASS, and switching automation OFF closes none of them — a control does not become satisfied because the thing it protects was disabled. Gates the automated pilot only: the hand-run pilot is judged by `linkedin_ready`, where a human is the pacing and their own browser is the egress. | automation envelope not measured: send_mode, profile_lock, send_window, account_budget, session, proxy_egress, account_health, reply_ingestion | Automated pilot only: make each control the evidence lists PASS (docs/linkedin_automatic_acceptance.md); switching automation off closes none of them. |
| ❔ UNKNOWN | A LinkedIn reply provably reaches us and stops both channels | linkedin | LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | `linkedin_reply_ingestion` is PASS: the backend read one real `inbound_events` row for an OPERATOR-OWNED self-test conversation, saw the lead's journey change, saw the journey enrollments stopped, and found nothing for that lead satisfying SENDABLE_MESSAGE_SQL on EITHER channel — plus a duplicate of the same event re-offered and refused. Gates both LinkedIn pilots: the cohort is kept clean by a filter over `leads`, and that filter is worth nothing if replies never get in. `delivery_unknown.linkedin` cannot stand in — it reads zero both when replies arrive and when the inbound path is dead. | linkedin_reply_ingestion: never observed — run prod_linkedin_reply_selftest.yml | Run prod_linkedin_reply_selftest.yml: prepare, reply from the operator-owned profile, verify (docs/linkedin_reply_selftest.md). A hand-recorded reply proves the stop, not the automatic thread sync. |

### P1 — multichannel product
_7 pass · 1 fail · 0 unknown · 0 informational_

| | Item | Channel | Gates | Owner | Exit condition | Evidence | Recovery (when not PASS) |
|---|---|---|---|---|---|---|---|
| ✅ PASS | A backup ran recently | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | Freshness ONLY — reports that db_backup.sh produced an artifact inside its window. Deliberately non-gating and deliberately separate from `offsite_backup_restore`: this row is true of a plaintext file sitting on the same disk as the database. | a backup ran within the freshness window (LOCAL ONLY — no verified off-site copy) | — |
| ❌ FAIL | Backup artifact encrypted at rest | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | The last artifact was produced with age/openssl encryption, AND the private half that opens it is not configured on the backup host. Shown on its own row because a plaintext dump is a personal-data exposure on the VM even when it never leaves it; it also gates `offsite_backup_restore`, which will not pass on a plaintext upload. The custody half was added 2026-09-02: it used to be asserted by a constant string and measured by nobody, while the only way to make the unattended off-site drill pass was to put the private key in the VM's env file — which turned every row greener and the protection off. | the last backup artifact is PLAINTEXT — it contains every lead's personal data | Configure the age recipient (public key) on the VM and keep the private key OFF it, then run a backup (docs/runbooks/dr_closure_sequence.md). |
| ✅ PASS | First-class orgs + workspace isolation | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `workspace_isolation` exercised by executable tests (cross-tenant access denied for every endpoint/worker/job) | workspace_isolation: 141 test eseguibili in 19 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Unified journey / enrollment engine | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `journey_engine` exercised by executable tests (pure compute_next_action; safety precedence over any step; branch-loop guard) | journey_engine: 35 test eseguibili in 3 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Channel-specific contact-policy engine | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `contact_policy` exercised by executable tests (per-channel stop, frequency caps, quiet hours; no suppressed lead reopened) | contact_policy: 120 test eseguibili in 11 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | True multi-account LinkedIn scheduling | linkedin | LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `multi_account_linkedin` exercised by executable tests (per-account routing/locks; A's work never runs through B). Scheduling ACROSS accounts is built (2026-09-24): with several active profiles a scheduled lane run fans out into one run per account, pinned by a Celery header (tests/linkedin/test_each_profile_gets_its_own_run.py); outside a task the ambiguity still fails closed. This row is CODE evidence only — two accounts running live side by side is not proven by it. | multi_account_linkedin: 312 test eseguibili in 33 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Two-way Unibox operator inbox | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `two_way_unibox` exercised by executable tests (durable inbound; operator reply lane; replies don't resume sequences) | two_way_unibox: 358 test eseguibili in 33 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Real end-to-end provider verification | global | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | tests/test_e2e_provider.py present and green (sandbox/contract E2E; live canaries gated + allowlisted) | tests/test_e2e_provider.py: 11 executable test(s), and CI is green for the deployed commit (Prompt 16 sentinel) | — |

### P2 — scale / security / maturity
_4 pass · 1 fail · 0 unknown · 0 informational_

| | Item | Channel | Gates | Owner | Exit condition | Evidence | Recovery (when not PASS) |
|---|---|---|---|---|---|---|---|
| ✅ PASS | Production-grade background queue | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `queue_topology`: workers/queue/{topology,dead_letter,retry}.py present, and executable tests naming celery_task_routes / lane_for_task / REASON_ATTEMPTS_EXHAUSTED | queue_topology: 45 test eseguibili in 5 file, e CI e' verde per il commit deployato | — |
| ❌ FAIL | Hardened auth / authz / secrets | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `auth_hardening` (backend/auth.py + backend/services/rbac.py, exercised) AND all four contract clauses MEASURED satisfied — MFA, RBAC enforced on every declared action, signed scoped service identity, rotation runbook. Per-clause state and operator steps in docs/AUTH_HARDENING_CONTRACT.md; the verdict is re-measured from the tree. | il codice c'e' ed e' esercitato (auth_hardening: 131 test eseguibili in 18 file, e CI e' verde per il commit deployato), ma 2 delle 4 clausole del contratto NON sono soddisfatte: MFA per gli utenti privilegiati; identita' di servizio firmata e con scopi. Stato per clausola e passi operativi in docs/AUTH_HARDENING_CONTRACT.md | Close the clause the evidence names, in the order of docs/runbooks/auth_identity_rollout.md (keys → observe → preflight GO → enforce) and docs/AUTH_HARDENING_CONTRACT.md for MFA. |
| ✅ PASS | SLOs + end-to-end observability | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | ops | capability `slo_rules` exercised by executable tests (every SLI carries its own absent() guard, run on real series by promtool) AND a request-scoped correlation ID propagated across processes: held in a contextvar in-process, carried across the process boundary in the Celery message HEADERS (never the arguments), landed on the durable rows, and — the clause that keeps this honest — part of NO idempotency key, so adding the trace cannot cost de-duplication | slo_rules: 15 test eseguibili in 2 file, e CI e' verde per il commit deployato; correlation IDs propagated end-to-end (contextvar in-process, bound at HTTP ingress, 3/3 Celery signals, persisted on 3/3 tables, and in no idempotency key) | — |
| ✅ PASS | Event-sourced outcome analytics | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | capability `outcome_analytics` exercised by executable tests (metrics recomputable from immutable events) | outcome_analytics: 347 test eseguibili in 29 file, e CI e' verde per il commit deployato | — |
| ✅ PASS | Release process + doc-drift control | platform | email pilot, LinkedIn pilot (manual), LinkedIn pilot (automated) | eng | TWO halves, both required. (1) CHANGELOG.md carries a GENERATED block with at least one entry, every entry a real merge commit — a file that merely exists is not a release record. (2) `check_doc_drift.sh` is invoked by the required `lint` job, so the generated documents (inventory, changelog, ledger, launch checklist) cannot drift from their generators unnoticed. Presence is measured here; the entries being genuine is measured by the CI run, whose colour is attested separately against the deployed commit. | CHANGELOG.md: 549 generated entries; doc-drift guard wired into the required `lint` job, and CI is green for the deployed commit, so the entries were verified | — |

<!-- READINESS:END -->

---

## Superseded documents

These made readiness/status claims and are now **historical** — a banner has
been added to each pointing here. Do not cite them for go/no-go:

- `AUDIT_REPORT.md` (2026-04-16, webhook/HITL audit only)
- `PROJECT_STATUS_REPORT.md` (2026-04-16 snapshot)
- `docs/analysis/ANALISI_INDIPENDENTE_2026-07-17.md` (backend-only "production-ready" claim)
- `docs/readiness.md` (channel-readiness *how-to*; still useful as a description of the endpoint, not as a verdict)
- `docs/test_readiness_roadmap.md` (2026-04-17 planning doc)
- `HANDOVER.md` / `docs/handover_production_readiness.md` (already self-marked SUPERATO)

`docs/pilot_prelaunch_checklist.md` is **kept live** (referenced by
`backend/routers/system.py`) but now points here as the authoritative ledger.

## Ownership & exit conditions

Each row in the generated block carries an **owner**, the **prompt** that closes
it, and a **machine-verifiable exit condition**. Feature rows use a sentinel
(a named test file that must exist and be green); as each prompt in the
readiness pack lands its tests, its row flips from `FAIL` to `PASS`
automatically. Infra rows resolve against GitHub API / runtime-probe signals.
This is what keeps the ledger honest: it cannot be talked into `all_ready`, only
evidenced into it.
