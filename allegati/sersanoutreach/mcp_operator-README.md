# `sersan-operator` MCP server — the Growth Operator's controlled changes

Growth OS Prompt 32. The read-only questions live in `mcp_server`
(`sersan-outreach`); this is the second server, the one that can change data —
so an assistant can prepare and manage growth work in a conversation while
everything irreversible stays behind the controls the app already has.

The two servers are separate on purpose. The read-only server's guarantee is
structural: its client cannot issue a write (`tests/mcp/test_the_mcp_server_can_only_read.py`).
Putting writes in the same package would turn that into a promise.

## The fourteen operations

| Operation | The route it calls (the app's own button) | What it cannot do |
| --- | --- | --- |
| `create_campaign_draft_from_blueprint` | `POST /api/campaigns/from-blueprint` | create anything but a DRAFT: nothing on Instantly, autopilot off |
| `import_leads` | `POST /api/leads/bulk-import` | write without `confirm=true` — without it, it only previews |
| `generate_drafts` | email: `POST /admin/sync/run-pipeline/start`, then `GET /admin/sync/run-pipeline/status` (the page's own pair; the synchronous route is not allowed) · LinkedIn: `POST /api/leads/{id}/linkedin/generate-dm` | approve: drafts wait as `pending_review`; at most 3 people per call. Per person it says `done` only when a draft exists (read back from the review queue / the route's `generated`), else `no_draft` with the reason, `already_pending`, `running` (still going on the server: do not start it again) or `unknown` / `not_sent` (the batch stops there) |
| `list_review_queue` | `GET /api/review/queue` | — (a read; each draft carries its `fingerprint`) |
| `approve_message` | `PATCH /api/review/{id}` `{"status": "approved", "expected_fingerprint": <the listed fingerprint>, "review_note": "via assistant (mcp-operator)"}` | approve a text the operator did not read (the server compares the `fingerprint` on the row it locks and answers 409 `draft_changed` if the text differs), edit it, or send it |
| `reject_message` | `PATCH /api/review/{id}` `{"status": "rejected", "rejection_reason", "review_note": "via assistant (mcp-operator)[: note]"}` | reject without one of the nine reasons |
| `assign_owner` | `PATCH /api/deals/{id}` | assign someone outside the campaign's workspace (the backend refuses) |
| `update_deal` | `PATCH /api/deals/{id}` | parse the amount itself — the backend's one parser does |
| `record_next_action` | `PATCH /api/deals/{id}` | — |
| `record_meeting` | `POST /api/deals/{id}/meetings`, `…/{meeting}/answer`, `…/reschedule` | record a meeting as held before its time |
| `change_deal_stage` | `POST /api/deals/{id}/stage` | skip the stage rules |
| `assign_partner` | `POST /api/deals/{id}/partner` | attribute by name — only by the partner's id |
| `reactivate_deal` | `POST /api/reactivation/deals/{id}/reactivate` | reopen a deal the backend's recheck refuses (it says why) |
| `pause_campaign` | `POST /api/campaigns/{id}/pause` | — (it says when Instantly did not confirm) |

There is **no** launch, bulk approval, send-control, deletion, suppression
change, mailbox or domain operation, and the client could not make one if
asked: every request is matched against `MUTATIONS` / `READS` in
`client.py` before it leaves, redirects are not followed, and only
`client.py` speaks HTTP (`tests/mcp_operator/test_the_operator_changes_only_what_it_may.py`).

## Why the controls hold

* **A change needs a person.** The server refuses to start without
  `SERSAN_USER_ID`; every request carries it, so the backend scopes the change to
  that operator's campaigns, checks their workspace role (a viewer cannot
  approve, an operator cannot create or pause a campaign) and records them as
  the actor. There is no agency-wide write.
* **Approving is not sending.** An approved message still waits for the send
  lane, which checks go-live readiness, the pilot envelope, the send mode,
  suppression, reply state and caps. `approve_message` answers with the
  campaign's go-live gate so the conversation says what is still missing.
* **An unknown outcome is never retried.** A request that left without an
  answer, or a 5xx, is `OutcomeUnknown`: check the page.
* **Every answer carries `performed`** — method, route, parameters, body,
  status, and as whom — next to what the API answered.
* **An answer never contradicts what was committed.** If the approval landed and
  the follow-up read of the go-live gate failed, the answer is the approval plus
  a note (not an error that makes the operator try again); a draft batch that
  stops keeps the results it already had.
* **What the trail says.** The actor of every change is the operator in
  `SERSAN_USER_ID` (`reviewer_id`, `deal_activities.actor_user_id`, …). A review
  decision made here is marked in the row's own `review_note` — `via assistant
  (mcp-operator)`, the field the backend already keeps for how a decision was
  taken (`autopilot`, `bulk approval`). A pause leaves a `security_audit_log`
  row (`privileged_operation`, who and, when the request is signed, `via
  mcp-operator`). The signed client is only known to the backend with a signed
  token: until the key is deployed the backend cannot tell an assistant request
  from the operator's own, and the conversation's `performed` echo is the trace.

The definition of done is a test on a real database:
`tests/api/test_the_growth_operator_acts_only_through_the_controls.py`.

## Configure

The same variables as `sersan-outreach`, with `SERSAN_USER_ID` **required** and
`SERSAN_MCP_ALLOW_UNSCOPED` ignored:

```bash
claude mcp add sersan-operator \
  --scope user \
  --env SERSAN_API_BASE_URL=https://outreach.sersan.io \
  --env SERSAN_USER_ID=<your Django user id> \
  --env SERSAN_API_KEY_FILE=/Users/alex/.sersan/api_key \
  --env PYTHONPATH=/Users/alex/sersanoutreach/SerSanOutreach \
  -- ~/.venvs/sersan-mcp/bin/python -m mcp_operator
```

The client asks before every call of a tool that is not read-only, and marks
`approve_message`, `reject_message` and `change_deal_stage` as destructive.
Keep it that way: auto-approving this server's tools removes the human the
design relies on.

**Signed identity (since 2026-10-03).** Every request carries a fresh
`X-Caller-Token`: subject `user:<SERSAN_USER_ID>` — the operator every change is
recorded against — client `mcp-operator`, scopes `read`+`write` and nothing more
(no admin, ops or manual send; never staff). Its key is this client's own
(`AUTH_IDENTITY_KEYS__CLIENT_MCP_OPERATOR`), in its own `kid:secret` file,
`~/.sersan/identity_keys.mcp-operator` by default (`chmod 600`;
`SERSAN_IDENTITY_KEYS_FILE` for another path) — never the read server's file,
which it refuses. The installation can pin the client to
named operators (`AUTH_IDENTITY_CLIENT_SUBJECTS__MCP_OPERATOR`). Without a key the
requests leave unsigned, as the startup line says, and `enforce` refuses them.
See `docs/runbooks/auth_identity_rollout.md` §6.
