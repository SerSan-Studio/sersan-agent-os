# `sersan-outreach` MCP server

Read-only access to the platform's KPIs and human-review feedback, from Claude
(and, with the extra step at the bottom, from ChatGPT). It answers strategic
questions — *is the funnel improving, which variant actually wins, what does the
reviewer keep rejecting* — rather than exposing endpoints.

It cannot send, approve, launch, pause or edit anything. See
`client.py` for why that is structural and not a promise.

## Tools

| Tool | Answers |
| --- | --- |
| `kpi_overview(days, channel)` | Funnel totals for a window vs the window before it, with staleness and truncation warnings |
| `variant_leaderboard(channel, min_sample)` | A/B variants by reply rate, with 95% intervals and an explicit verdict on whether the top two separate |
| `review_feedback(days, channel)` | Approve/reject counts, rejection reasons, edit distance, broken down by prompt version and campaign |
| `reply_digest(channel, limit)` | Recent conversations with what the prospect actually wrote — read from `/api/unibox/conversations/{lead}` (`inbound_events`, the rows the Unibox shows), never from `outreach_messages.reply_body`, which nothing writes |
| `campaign_scoreboard(days, channel)` | Every campaign side by side over one window |

### The Growth Operator (Growth OS Prompt 31)

The changes — drafts, approvals, deals — are a second server, `sersan-operator`
(`mcp_operator/README.md`); this one stays read-only.

Fourteen more tools answer the questions of SerSan's internal Growth OS — and
answer them with **the number the app's page shows**: each one reads the route
that page reads, with the same parameters, and passes the numbers through
(`mcp_server/growth.py`). The definition of done — *«How is outbound doing this
month?» gets the dashboard's numbers* — is a test on a real database,
`tests/api/test_the_growth_operator_says_what_the_dashboard_says.py`.

| Tool | Answers | Reads (the page) |
| --- | --- | --- |
| `growth_overview(period, start, end)` | The window's funnel (inbound/outbound), value won, open pipeline, win rate, cycle, and what stands open now | `/api/growth/ceo-funnel`, `/revenue`, `/summary`, `/action-queue` (`/growth/funnel/`, `/growth/revenue/`) |
| `action_queue(priority, owner_user_id, unowned, kind)` | What to do now, P0–P3, one item at a time | `/api/growth/action-queue` (`/growth/actions/`) |
| `pipeline_overview()` | Deals by stage: count, value per currency, unpriced, flags, the largest | `/api/deals/`, `/api/growth/revenue` (`/deals/`) |
| `campaign_performance(period)` | Each campaign's funnel and money, side by side | `/api/growth/ceo-funnel` per campaign, `/revenue` |
| `funnel_breakdown(period, filters…)` | Each step, conversion, who skipped a step, and the filter choices | `/api/growth/ceo-funnel` (`/growth/funnel/`) |
| `revenue_attribution(period, dimension)` | Value by campaign, channel, source, owner, partner, inbound/outbound. An `end` alone is «everything up to that day» (as on the page), not 30 days | `/api/growth/revenue` (`/growth/revenue/`) |
| `positive_replies(period)` | Who replied positively, and who still waits for our answer | `/api/growth/ceo-funnel/members` (`/growth/funnel/people/`), `/action-queue` |
| `overdue_actions(owner_user_id)` | The queue items past due, most late first | `/api/growth/action-queue` |
| `meeting_summary(period, days_ahead)` | Booked/held in the window, the ones coming, the ones to record | `/api/growth/meetings`, `/summary`, `/ceo-funnel` (`/growth/`) |
| `lost_deal_analysis(period)` | Why we lose, with the value lost per currency (an `end` alone is «everything up to that day») | `/api/growth/lost-deals` (`/growth/revenue/`) |
| `reactivation_candidates()` | Lost deals worth reopening for a new reason | `/api/reactivation/candidates` (`/deals/reactivation/`) |
| `partner_performance(partner_id)` | Each partner as a relationship, and what it brought — **agency view** | `/api/partners/` (`/partners/`) |
| `linkedin_readiness()` | The operator's account; in the agency view every profile with its readiness state, the histogram of states, and which ones are blocked (`/pilot/` shows the same roster) | `/api/linkedin/account-status`, `/profiles/overview` |
| `mailbox_readiness()` | Mailboxes, the warm-sender gate's verdict, blocked campaigns — **agency view** | `/api/mailboxes/`, `/action-queue` (`/mailboxes/`) |

Every answer is one JSON object (structured output, with its schema) in the
same envelope: `as_of`, `window` (inclusive UTC dates, or `all_time`), `scope`
(one operator's campaigns, or the agency view), `test_contacts` (excluded unless
asked), `sources` (the routes and parameters read), `open_in_app` (the pages
with the same numbers) and `conventions`: **`null` is unknown, never zero**;
money is integer cents **per currency**, never summed across currencies, with a
`*_display` beside it and the deals without an amount counted apart; ids are
canonical; time is UTC. Nothing is recomputed that a page shows, and nothing
writes. `SERSAN_APP_BASE_URL` sets where the page links point when the pages are
not on the API's host (a dev stack: `http://localhost:8001`).

**Signed identity (since 2026-10-03).** Every request carries a fresh
`X-Caller-Token`: subject `user:<SERSAN_USER_ID>` (or `system:mcp` in the agency
view), client `mcp-read`, scopes `read` (agency view: `read`+`admin`). The backend
refuses every writing method from this client whatever the scopes. The key is
this client's own (`AUTH_IDENTITY_KEYS__CLIENT_MCP_READ` on the backend), in
`~/.sersan/identity_keys.mcp-read` (`kid:secret`, `chmod 600`;
`SERSAN_IDENTITY_KEYS_FILE` for another path). Never the operator server's file:
each server signs with the first line of its own, and pointed at the other
server's default file it refuses to start. Without a key the server sends
unsigned requests and says so on startup — the backend refuses those once
`AUTH_IDENTITY_MODE=enforce`. Keys, rotation, revocation and pinning to named
operators: `docs/runbooks/auth_identity_rollout.md` §6.

## Install

The protocol SDK is not a platform dependency — this runs on the operator's
machine, not in any image. Use a venv of its own, installed from `uv.lock` (the
`mcp` extra), so the SDK version on your machine is the one the repository
tested rather than whatever was newest the day you installed it:

```bash
cd /path/to/SerSanOutreach
UV_PROJECT_ENVIRONMENT=~/.venvs/sersan-mcp uv sync --frozen --python 3.12 \
  --extra mcp --no-install-project --no-default-groups
```

Re-run it after a `git pull` that changes `uv.lock`. Both servers (`mcp_server`
and `mcp_operator`) use this one venv. Check what it holds against the lock:

```bash
~/.venvs/sersan-mcp/bin/python scripts/ops/lock_conformance.py --lock uv.lock
```

## Configure

| Variable | Meaning |
| --- | --- |
| `SERSAN_API_BASE_URL` | `https://outreach.sersan.io`, or `http://localhost:8000` against the dev stack |
| `SERSAN_API_KEY_FILE` | Path to a file containing the key and nothing else, `chmod 600`. Default `~/.sersan/api_key` |
| `SERSAN_API_KEY` | The key inline. Wins over the file — fine for a dev stack, wrong for production |
| `SERSAN_USER_ID` | Django user id. Every call carries it as `X-User-Id`, so answers cover that operator's campaigns |
| `SERSAN_MCP_ALLOW_UNSCOPED` | `1` to omit `X-User-Id` and read **every tenant**. The tools label the answer when you do |
| `SERSAN_MCP_TIMEOUT` | Seconds per request, default 60 — `/api/kpi/summary` was measured at 28.7s |

The key is a file path and not a value because `claude mcp add --env
SERSAN_API_KEY=…` writes what you give it into `~/.claude.json`, which is a
settings file: readable by default, copied between machines, pasted into bug
reports. This key is accepted on every router of the API, including
`/campaigns/{id}/launch` and `/review/bulk-approve`.

```bash
mkdir -p ~/.sersan && chmod 700 ~/.sersan
# then write the key with no shell history and no echo:
read -rs "k?INTERNAL_API_KEY: " && printf %s "$k" > ~/.sersan/api_key && chmod 600 ~/.sersan/api_key && unset k
```

## Claude Code

```bash
claude mcp add sersan-outreach \
  --scope user \
  --env SERSAN_API_BASE_URL=https://outreach.sersan.io \
  --env SERSAN_USER_ID=1 \
  --env PYTHONPATH=/Users/alex/sersanoutreach/SerSanOutreach \
  -- ~/.venvs/sersan-mcp/bin/python -m mcp_server
```

`PYTHONPATH` points at the repository root: the package is not installed into
the venv, it is imported from the checkout, so a `git pull` updates the tools.

## Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sersan-outreach": {
      "command": "/Users/alex/.venvs/sersan-mcp/bin/python",
      "args": ["-m", "mcp_server"],
      "env": {
        "PYTHONPATH": "/Users/alex/sersanoutreach/SerSanOutreach",
        "SERSAN_API_BASE_URL": "https://outreach.sersan.io",
        "SERSAN_USER_ID": "1"
      }
    }
  }
}
```

Restart Claude Desktop; the server announces itself on stderr with the base URL
and the scope it will read, which is the fastest way to catch a wrong `SERSAN_USER_ID`.

## Checking it works

```bash
SERSAN_API_BASE_URL=https://outreach.sersan.io SERSAN_USER_ID=1 PYTHONPATH="$PWD" ~/.venvs/sersan-mcp/bin/python -m mcp_server
```

A misconfigured environment exits 2 naming the missing variable instead of
starting and failing on every question.

Two failures worth recognising rather than debugging:

* **`has no /api/review/feedback (answered 422)`** — the backend you are pointed
  at predates that endpoint, so `/api/review/{message_id}` matched first and
  tried to read "feedback" as a UUID. The other four tools work meanwhile.
* **`timed out after 60s`** — `/api/kpi/summary` counts leads and messages across
  the whole scope. `kpi_overview` already degrades: it prints the funnel and says
  the backlog block is missing rather than printing zeros.

## ChatGPT — the desktop app runs this locally

The ChatGPT macOS app ships a Codex CLI inside it and reads
`~/.codex/config.toml`, where `[mcp_servers.*]` entries are ordinary local stdio
servers — the app registers its own `node_repl` and `cua_repl` the same way. So
no hosting and no OAuth are needed for that surface:

```bash
/Applications/ChatGPT.app/Contents/Resources/codex mcp add sersan-outreach \
  --env SERSAN_API_BASE_URL=https://outreach.sersan.io \
  --env SERSAN_MCP_ALLOW_UNSCOPED=1 \
  --env SERSAN_API_KEY_FILE=/Users/alex/.sersan/api_key \
  --env PYTHONPATH=/Users/alex/sersanoutreach/SerSanOutreach \
  -- /Users/alex/.venvs/sersan-mcp/bin/python -m mcp_server
```

`codex mcp list` shows it; `codex mcp remove sersan-outreach` undoes it. The
tools appear in the app's Codex sessions. The app owns that file and rewrites
it on update, so keep a copy of the command — not of the file.

## What ChatGPT on the web, and claude.ai, would still need

Those are hosted and cannot launch a local process, so stdio is out. The tool
module is transport-agnostic — `MCPServer.run(transport="streamable-http")` is
the one-line part — but the rest is not code this repo can decide:

1. **Somewhere to run it** with a public HTTPS name. Not inside the backend
   image: `mcp` 2.x requires starlette 1.6 and this repo pins `fastapi<0.142`,
   whose starlette floor is far below that. It is a separate service.
2. **An OAuth authorization server.** A hosted connector has no safe place for
   `SERSAN_API_KEY`: the key grants writes across every tenant, and a connector
   config is not a secret store. The remote server must authenticate the *user*
   and derive `X-User-Id` from that, keeping the API key server-side.
   django-oauth-toolkit covers the parts ChatGPT needs — Dynamic Client
   Registration (`DCR_ENABLED`), Client ID Metadata Documents (`CIMD_ENABLED`),
   PKCE by default, RFC 8414 metadata — so the existing Django login and its
   staff TOTP can be the identity.
3. **ChatGPT web also needs Developer mode** turned on (Settings → Security and
   login). It does *not* need a `search`/`fetch` pair: that is only for deep
   research and company knowledge. Write actions there are confirmed per call
   unless a tool declares `readOnlyHint`, which every tool here does.

Do not use the "No authentication" option those connector dialogs offer. With
this key behind the server, the URL would be the only thing protecting every
client's pipeline.
