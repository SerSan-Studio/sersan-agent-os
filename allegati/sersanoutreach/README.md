# SerSan Outbound Platform

> Self-hosted LinkedIn + Email outbound platform with Human-in-the-Loop (HITL) approval before every send.

---

## Overview

SerSan Outbound is a full-Python outbound sales platform forked from [OpenOutreach](https://github.com/eracle/OpenOutreach). It extends the LinkedIn automation engine with a complete Email pipeline, replacing N8N workflows with a unified Celery task architecture.

**Key principles:**
- **HITL invariant** — no message (LinkedIn or Email) is sent without human approval. For email, the approval of step 1 also authorizes steps 2..N, which Instantly sends from the synced sequence (ADR-033)
- **Self-hosted** — full data ownership, no vendor lock-in
- **Multi-channel** — LinkedIn + Email from a single platform
- **AI-powered** — Claude generates personalized icebreakers, GP Classifier + BALD active learning qualifies leads

---

## Architecture

```
Django Frontend (:8001)  ->  FastAPI Backend (:8000)  ->  PostgreSQL 15
                                                       ->  Celery Workers (linkedin + email queues)
                                                       ->  Celery Beat (scheduler)
```

| Component | Tech | Purpose |
|---|---|---|
| **Backend API** | FastAPI, SQLAlchemy 2.x async, Pydantic v2 | REST API (HITL review queue, auth; current endpoint/router counts in `docs/CODE_INVENTORY.md`) |
| **Frontend** | Django 5.2, Bootstrap 5, htmx | Dashboard, campaigns, leads, review queue, Unibox |
| **LinkedIn Worker** | Celery, Playwright stealth, Voyager API | Profile visits, connections, DMs, follow-ups |
| **Email Worker** | Celery, LangChain + Claude, Instantly API | Validation, enrichment, icebreaker generation, push to Instantly |
| **Instantly.ai** | Email delivery platform | Warmup, domain rotation, send, tracking (webhooks) |
| **ML Pipeline** | FastEmbed, scikit-learn, numpy | GP Regression + BALD active learning for lead qualification |
| **Database** | PostgreSQL 15, Alembic migrations | Single source of truth, Django `managed=False` |
| **Infrastructure** | Terraform (Azure + AWS), Docker Compose | Modular IaC, dev + prod compose files |

---

## Email Pipeline

```
Lead (raw) -> Ingest -> Validate (RFC+MX) -> Enrich (Perplexity)
  -> Copy Agent (icebreaker only, body from campaign template)
  -> HITL Review (card UI, approve/reject)
  -> Push to Instantly (API, custom variables: icebreaker + subject)
  -> Instantly sends (warmup, domain rotation, tracking)
  -> Webhooks (sent, opened, replied, bounced) -> SerSan DB
  -> Unibox (unified inbox for replies, reply via Instantly API)
```

**Sequence logic:**
- **Step 1**: AI icebreaker based on Perplexity signal (hiring, funding, etc.)
- **Step 2**: AI generates different angle on the *same* signal (auto, after delay_days)
- **Step 3-4**: Admin-configured templates (no AI)

> What Instantly actually sends at steps 2..N is each synced step template filled with the **step-1** variables (greeting, icebreaker, subject, opt-out footer). The step 2..4 drafts above are created in SerSan, but approving them does not change that text. The human approval of step 1 authorizes the whole sequence: see ADR-033.

---

## LinkedIn Pipeline

```
Search -> Enrich -> Qualify (GP + LLM) -> Visit -> Connect (HITL)
  -> Check Pending -> DM (HITL) -> Follow-up (HITL agent)
```

All send actions (connect, DM, follow-up) pass through HITL approval.

---

## Quick Start

### Prerequisites

- Docker Desktop
- Git

### 1. Clone & Configure

```bash
git clone git@github.com:SerSan-AI-Studio/SerSanOutreach.git
cd SerSanOutreach
cp .env.example .env
# Edit .env with your credentials (DB password, API keys, etc.)
```

### 2. Start Development Stack

```bash
make dev
# Or: docker compose -f docker-compose.dev.yml up --build
```

This starts 11 services: PostgreSQL, a one-shot migration service, FastAPI backend (:8000), Django frontend (:8001), tailwind-watcher, LinkedIn worker, Email worker, worker-default (kpi/default queue), Celery beat, Prometheus, and Grafana.

### 3. Access

- **Frontend**: http://localhost:8001 (login required)
- **API docs**: http://localhost:8000/docs
- **Admin**: http://localhost:8001/admin/

---

## Project Structure

```
backend/                  FastAPI backend
  models/                 SQLAlchemy models (schema source of truth)
  routers/                API endpoints (review, campaigns, leads, unibox, etc.)
  schemas/                Pydantic request/response DTOs
  auth.py                 X-API-Key authentication
  crypto.py               Fernet field-level encryption
  config.py               pydantic-settings configuration

frontend/                 Django frontend
  apps/                   dashboard, campaigns, leads, review, unibox, linkedin
  templates/              Bootstrap 5 templates
  api_client.py           httpx wrapper for Django -> FastAPI calls

workers/                  Celery task workers (task and beat counts: docs/CODE_INVENTORY.md)
  linkedin/               LinkedIn lane tasks + bootstrap + HITL helpers
  email/                  Email lane tasks (ingest, validate, enrich, copy, send to Instantly, ...)
  celery_app.py           Celery config with per-queue autodiscovery
  beat_schedule.py        The full Celery beat schedule

linkedin/                 OpenOutreach LinkedIn automation (browser, API, pipeline, agents, ML)
ml/                       Machine learning (GP Classifier, BALD, FastEmbed)
infra/                    Terraform modules (Azure + AWS)
alembic/                  Database migrations
compose/                  Dockerfiles (backend, frontend, worker-linkedin, worker-email)
```

---

## Key Features

| Feature | Description |
|---|---|
| **HITL Review Queue** | Card-based UI for approving/rejecting outreach messages with lead context |
| **Unibox** | Unified inbox for all email replies across mailboxes (Instantly-style) |
| **Warm-sender gate** | Warmup runs on Instantly; SerSan pushes no lead to a campaign whose senders are still cold (`workers/email/_warm_sender.py`). Instantly picks the sending mailbox and rotates domains — SerSan does not pin a lead to a mailbox, and the per-domain limit in the UI is indicative (no worker reads it) |
| **Icebreaker Generation** | AI generates 2-line personalized openers using Perplexity enrichment signals |
| **Sequences** | Email: approving step 1 approves the sequence, and Instantly sends steps 2..N from the synced templates (ADR-033). LinkedIn: follow-up DMs (steps 2-3) are drafted for HITL review (`workers/linkedin/sequence_advance_li.py`) |
| **Tenant Unsubscribe** | REST API for client-hosted unsubscribe pages (`POST /api/unsubscribe`) — requires a per-recipient HMAC token (`backend/services/unsubscribe_token.py`) |
| **Field Encryption** | Fernet AES-128 for SMTP passwords and LinkedIn credentials |
| **Non-root Containers** | All Docker containers run as non-root user |

---

## API Endpoints

All endpoints except `/health`, `/health/ready`, `/api/unsubscribe` and `/api/webhooks/*`
require the `X-API-Key` header. `/api/webhooks/*` (Instantly) authenticates with
`X-Webhook-Secret` instead (`backend/services/webhook_secret.py`).
`/api/unsubscribe` takes no API key but is **not** unauthenticated: it requires a per-recipient
HMAC token bound to `(tenant_code, address)` — see `backend/services/unsubscribe_token.py` and
ADR-030 §5. Without a valid token it answers `400`, indistinguishably from an unknown tenant or
an unknown address.

| Prefix | Endpoints | Purpose |
|---|---|---|
| `/api/review` | queue, stats, get, approve/reject | HITL review queue |
| `/api/campaigns` | CRUD | Campaign management |
| `/api/leads` | CRUD + search | Lead management |
| `/api/unibox` | threads, thread detail, reply | Unified inbox |
| `/api/mailboxes` | CRUD | Mailbox management |
| `/api/domains` | CRUD | Domain management |
| `/api/sequences` | email + linkedin steps | Sequence management |
| `/api/kpi` | daily, summary | KPI aggregates |
| `/api/campaigns/{id}/launch` | launch/pause | Instantly campaign control |
| `/api/campaigns/{id}/sync-instantly` | retry sync | Link campaign to Instantly |
| `/api/webhooks` | POST (X-Webhook-Secret) | Instantly event receiver |
| `/api/unsubscribe` | POST (public, HMAC token) | Tenant-based unsubscribe |

---

## Environment Variables

See `.env.example` for all required variables. Key ones:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL async connection |
| `CELERY_BROKER_URL` | Celery broker (PostgreSQL sqla transport) |
| `ANTHROPIC_API_KEY` | Claude API for icebreaker generation |
| `PERPLEXITY_API_KEY` | Perplexity Agent API for lead enrichment |
| `PERPLEXITY_AGENT_PRESET` | Perplexity Agent API preset (default `fast`) |
| `INSTANTLY_API_KEY` | Instantly.ai email delivery |
| `INSTANTLY_WEBHOOK_SECRET` | Shared-secret for X-Webhook-Secret header validation |
| `INSTANTLY_WEBHOOK_SECRET_PREVIOUS` + `..._PREVIOUS_EXPIRES_AT` | Previous secret, accepted until the configured expiry so a rotation loses no events (opt-outs included). See `docs/runbooks/instantly_webhook_secret_rotation.md` |
| `FIELD_ENCRYPTION_KEY` | Fernet key for encrypted DB fields |
| `INTERNAL_API_KEY` | Django -> FastAPI authentication |

---

## Makefile

```bash
make dev              # Start dev stack (docker compose up)
make down             # Stop services
make logs             # Tail logs
make test             # Run pytest
make lint             # ruff check
make prod             # Start production stack (gunicorn, no debug)
make build-all        # Build all production images
make health-check     # Verify service health
make migrate          # Run Alembic + Django migrations
make tf-plan TARGET=infra/azure   # Terraform plan
```

---

## Security

- Field-level encryption (Fernet AES-128) for stored credentials
- Timing-safe API key comparison (`hmac.compare_digest`)
- Django prod security: HSTS, SSL redirect, secure cookies
- Non-root Docker containers
- `.env` excluded from git and Docker builds
- Parameterized SQL queries (no injection)

---

## Compliance

- **CAN-SPAM**: List-Unsubscribe headers, compliance footer, public unsubscribe endpoint
- **GDPR**: Consent tracking fields, GDPR country-code awareness
- **Tenant isolation**: Unsubscribe API uses `tenant_code` per campaign

---

## License

Based on [OpenOutreach](https://github.com/eracle/OpenOutreach) (GPLv3).

---

Built by [SerSan AI Studio](https://github.com/SerSan-AI-Studio)
