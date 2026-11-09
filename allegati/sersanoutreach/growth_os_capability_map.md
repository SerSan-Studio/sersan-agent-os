# SerSan internal Growth OS: capability map

Re-measured **2026-10-05** (Growth OS 18-prompt pack, Prompt 9) against `main` =
production = `672bf075` — the commit `/api/system/readiness/evidence` reports
as deployed, read at 15:57Z — and against the tree. Scope is SerSan's own
operation only: no white-label, billing, client self-service or reseller work.
**Re-measure before acting on any row**: open PRs land quickly, and the rows
name the ones that would change them. Rows 4, 6, 7 and 20 were updated when
#737 merged (`509b4da1`). Rows 1, 5, 13, 15, 16, 18, 20 and 24 were updated on
2026-10-08: PRs #738–#741 were closed unmerged and their content landed with
release #747 (merged 2026-10-06), so the gaps they named are closed on `main`.
The rest are as measured.

The previous version (2026-09-28, `ac3171c0`) was wrong on 13 of 25 rows:
Prompts 10, 12–23, 31 and 32 merged after it and nobody re-measured it.

Six states, never merged into one:

- **IMPLEMENTED**: code exists (backend, API, operator UI).
- **TESTED**: tests exercise it. *pure* means no database; *API/DB* means through the app against Postgres; *journey* means `tests/integration` or `scripts/e2e`.
- **MERGED / DEPLOYED**: on `main`, and running in production. Everything on `main` is deployed (`672bf075` when measured, `509b4da1` after #737).
- **CONFIGURED**: production data and settings make it able to run.
- **PROVEN LIVE**: a real run in production, with evidence.

Production volume on 2026-10-05: 11 leads in the funnel window, 1 contacted, 1
reply, 0 positive replies, 0 meetings, 0 won; 91 open deals, every one without a
value. Most rows below are therefore *implemented and tested* but **not proven
live**, because nothing has happened yet for them to measure.

| # | Capability | Implemented | Tested | Configured in prod | Proven live | Biggest gap |
|---|---|---|---|---|---|---|
| 1 | Acquire prospects (CSV email/LinkedIn, Sales Navigator, first-party inbound, vendor export) | CSV + LinkedIn CSV (UI), first-party inbound endpoint, Sales Navigator lane, vendor-export evaluation `/leads/vendor/` (P21); one registry `/growth/sources/` (P20) | API/DB | registry: CSV, LinkedIn CSV, first-party inbound **available**; Sales Navigator, post search, Ample **legacy**; Apollo, inbound webhook unavailable | CSV imports used; Sales Navigator discovery `warn` (never landed a lead) | deterministic routing of a first-party inbound person + `inbound_held` landed with release #747 (was #738); not yet exercised in prod |
| 2 | Enrich and understand | enrich_v2 lane + in-browser profile read | API/DB + journey | yes (Perplexity/Anthropic keys) | runs in prod; quality never benchmarked | one lead at a time on the LinkedIn queue |
| 3 | Evidence-backed angles | signals, observed/inferred taxonomy, angle agent, grounding + entailment guards | API/DB + journey | yes | not measured | paraphrased inference caught only by a planned LLM judge |
| 4 | Personalised generation (email + LinkedIn) | yes; real-draft corpus recorder (P10); email is drafted for step 1 only, Instantly sends steps 2..N (ADR-033, on `main` since #737) | API/DB + journey + offline judge | yes | drafts exist; the corpus has not been recorded from prod | copy benchmark on real drafts not run |
| 5 | Review before sending (HITL) | review queue + approval gate (LinkedIn) | API/DB, pure, Playwright | yes | used in prod | an approval is bound to the text that was read: the server compares the draft's fingerprint (`backend/routers/review.py`, release #747, was #741) |
| 6 | LinkedIn across employees | routing, isolation, per-account budget/window, extension 1.6.x, control desk; team page `/linkedin/team/` (on `main` since #737) | API/DB, JS harness, journey | 1 active profile, `linkedin_session`/egress n/a (member-browser transport); `linkedin_challenges` and `linkedin_profile_lock` **warn** | manual send + manual reply 2026-09-25; no automatic send observed | `linkedin_reply_ingestion` never collected; Michele not onboarded |
| 7 | Email through Instantly | mapping, push, senders, DNS/warm-up, go-live gate; staff email-infrastructure page and campaign/provider comparison (on `main` since #737) | API/DB + journey | campaigns mapped (`instantly_campaign_mapping` pass); `email_dns`, `email_mailbox_state`, `email_compliance` **fail** | `email_provider_canary` **never collected** | no sending domain or mailbox is live yet (`email_mailbox_state` **fail**): they are brought live from the email-infrastructure page |
| 8 | Ingest replies (Unibox) | webhook, inbound ledger, LinkedIn inbox sync, manual inbound, one conversation view | API/DB + journey | webhook secret configured; `inbound_reply_readable.email` pass | `email_reply_ingestion` and `linkedin_reply_ingestion` **never collected**; `inbound_reply_sync.email` unknown | the unmatched-event reconciliation queue is API-only |
| 9 | Stop irrelevant follow-ups | cross-channel stop, suppression, opt-out outbox | API/DB + journey | yes | manual LinkedIn reply stopped both channels (2026-09-25) | journey enrolment has no production entry point (not re-measured this pass) |
| 10 | Prioritise conversations | keyword classifier, uncertain-reply hold; queue items for unanswered replies | API/DB | yes | not measured | no ranking or filter inside the Unibox itself |
| 11 | Meetings | `meetings` entity booked/held/cancelled/no_show/rescheduled, moved only by a person (P13) | API/DB | yes | 0 meetings in prod | none in code; nothing to measure yet |
| 12 | Opportunities (deals) | owner, value (integer cents), currency, expected close, next action, detail page `/deals/<id>/`, `deal_activities` history (P12) | API/DB + page | deals created at import | 91 open deals, **all without a value**, so open pipeline is unknown, not zero | operators have not filled values; `highlights()` flags each |
| 13 | Proposals | a stage, recorded as `proposal_sent` when a deal ENTERS it | pure + DB | — | 0 | no proposal entity; the funnel says deals «passati a «Proposta»» (release #747, was #739), never that a proposal was sent |
| 14 | Won / lost | `close_reason` (vincolato), lost-deal section «Perché perdiamo» on `/growth/revenue/` | API/DB + page | — | 0 won, 0 lost | none in code |
| 15 | Revenue / contract value | `/growth/revenue/` (P16): by **id** never name, per currency never summed, NULL ≠ 0 (`unknown_value_deals`), test contacts excluded, **signed contract value** — no invoices or cash, which the system does not hold | API/DB + reconciliation | — | won 0; open 91 deals, value unknown on all 91 | values must be entered; the seeded reconciliation across ledger, revenue, funnel and partners is `tests/api/test_every_commercial_number_traces_to_its_step.py` (release #747) |
| 16 | Reactivation | eligibility decided at the click, deal locked (P18); page `/deals/reactivation/` | API/DB + page | — | 0 lost deals, so 0 candidates | one person's lost deals reopen one at a time (a per-person advisory lock, release #747, was #740); no scheduler (by design: a person clicks) |
| 17 | Channel/campaign/people performance | KPI daily, variants, trigger outcomes, dashboard; revenue by owner | DB + API | yes | dashboards render prod data | `workers/kpi/` still counts test contacts |
| 18 | What to do next (action queue) | `/growth/actions/` + agency view, P0–P3 rules, done/snooze/assign (P17) | API/DB + page | yes | renders on prod (read through MCP 2026-10-05) | `inbound_held` and the suppression filter on «unanswered» landed with release #747 (was #738), and so did words for every kind (was #740) |
| 19 | Executive view | `/growth/funnel/` from `commercial_events` (P15), inbound/outbound split, people behind each step | API/DB + page | yes | 11 leads → 1 contacted → 1 reply → 0 further | nothing to measure past the first reply |
| 20 | MCP growth operator | read server `mcp_server/` (19 tools, P31) + controlled-write server `mcp_operator/` (14 operations, P32), both in this repo | API/DB + unit | read server ran against prod from a checkout on 2026-10-05 (19 tools, all 200) | the **installed** read server fails to start (its config points at a deleted worktree); the write server is not installed | the servers sign who they act for on `main` since #737, while prod runs `AUTH_IDENTITY_MODE=observe`; the server-side approval fingerprint landed with release #747 (was #741) |
| 21 | Partner channel | partners, relationship report, owner/next action, deal attribution in the deal page (P23) | API/DB + page | — | no partner deals | none in code |
| 22 | Campaign blueprints | three SerSan blueprints → draft campaign + policy + steps, no Instantly until launch (P22) | API/DB + page | — | not used in prod | none in code |
| 23 | Copy QA | offline judge + promotion gate + real-draft corpus recorder (P10) | pure (CI gate) + DB | — | fixture corpus only | record a corpus from prod drafts |
| 24 | Commercial event history | eight event types (engaged … won/lost), each written by its proof, idempotent, no backfill (P14) | pure + DB | — | 0 events beyond `engaged` | retention: history leaves only with its deal — the trigger refuses UPDATE (except the actor set to NULL when that person is deleted), direct DELETE and TRUNCATE (migration `83eaad6fe360`), and every deleting route refuses while steps exist (release #747, was #739) |
| 25 | Test contacts out of metrics | excluded from funnel, revenue, lost deals, partners, reactivation, action queue | API/DB | yes | — | `workers/kpi/` daily KPIs still include them |

**Platform**

| Area | State in production (readiness evidence, 2026-10-05 15:57Z) |
|---|---|
| Release identity | `deployed_commit`, `migration_head`, `ci_result`, `canary_ladder` PASS for `672bf075` (the ladder is a **no-send** canary: it proves fixtures and refusals, never a delivery) |
| Backups | encryption PASS; restore drill PASS (local dump); off-site **FAIL** (no storage account); freshness **FAIL** |
| Alert delivery to a person | destination, routing and human receipt all **FAIL** |
| Repository governance | branch protection and SAST gate PASS; secret scanning, dependency scanning, code scanning **UNKNOWN** — unreadable without `GOVERNANCE_READ_TOKEN` (not set: 0 repository secrets), which is not evidence they are off |
| Auth hardening | `AUTH_IDENTITY_MODE=observe`, callers unsigned, MFA not enrolled — the staged rollout is a release-prompt item |
| Kill switches | none engaged (both channels can send) |

Never-collected required rows at 15:57Z: `email_provider_canary`,
`email_reply_ingestion`, `linkedin_reply_ingestion`. Until Prompt 9 the expiry
monitor and the launch evaluator called each of these **expired**; they are now
reported as **never observed** — the producer has to run once, there is nothing
to refresh.
