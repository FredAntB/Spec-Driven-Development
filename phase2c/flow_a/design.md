# design.md
> Freelance Time Tracker — Version v1.0 — 2026-05-18

## Architecture Overview
Freelance Time Tracker is a stateless Node.js REST API backed by a
managed PostgreSQL instance, deployed as a single web service on Railway.
The freelancer authenticates with email + password, receives a JWT, and
all subsequent API calls carry that token. PDF rendering is performed
synchronously on the API process using `pdfkit`; for v1.0 the throughput
target (NFR-001) is comfortably met by in-process rendering and no
worker queue is introduced.

**Stack**: Node.js 20 LTS, Express 4, PostgreSQL 16, `pg` (pg-pool),
`jsonwebtoken`, `bcrypt`, `pdfkit`, `zod` for input validation, Jest for tests.
**Deployment**: Railway — single web service + managed PostgreSQL add-on,
environment variables for `DATABASE_URL`, `JWT_SECRET`, `PORT`.

## System Diagram
```
[Freelancer browser]
        │  HTTPS + JWT
        ▼
┌──────────────────────┐        ┌──────────────────────┐
│  Express API (Node)  │ ─────▶ │  PostgreSQL (Railway)│
│  - routes/           │        │  - clients           │
│  - services/         │        │  - projects          │
│  - pdf renderer      │        │  - time_entries      │
└──────────────────────┘        │  - invoices          │
        │                       │  - invoice_lines     │
        ▼                       └──────────────────────┘
   PDF response
```

## Data Models

### Client
| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PRIMARY KEY | gen_random_uuid() |
| freelancer_id | UUID | NOT NULL, FK users(id) | scopes to owner |
| name | VARCHAR(120) | NOT NULL | display name on invoices |
| email | VARCHAR(255) | NULL | for future invoice email delivery |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | — |
| archived_at | TIMESTAMPTZ | NULL | soft-archive (REQ-001) |

**Relationships**: one Client has many Projects.

### Project
| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PRIMARY KEY | — |
| client_id | UUID | NOT NULL, FK clients(id) | — |
| name | VARCHAR(120) | NOT NULL | — |
| current_rate_cents | INTEGER | NOT NULL, CHECK (>= 0) | stored as cents to avoid float drift (NFR-002) |
| currency | CHAR(3) | NOT NULL DEFAULT 'USD' | single currency for v1.0 |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | — |
| archived_at | TIMESTAMPTZ | NULL | — |

**Relationships**: one Project has many TimeEntries; rate history is
captured per-TimeEntry via `rate_cents_snapshot` (REQ-002).

### TimeEntry
| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PRIMARY KEY | — |
| project_id | UUID | NOT NULL, FK projects(id) | — |
| entry_date | DATE | NOT NULL | local date the work was done |
| minutes | INTEGER | NOT NULL, CHECK (> 0 AND <= 1440) | per-day cap of 24h |
| description | TEXT | NULL | optional note (REQ-003) |
| rate_cents_snapshot | INTEGER | NOT NULL | rate at creation (REQ-002) |
| invoice_id | UUID | NULL, FK invoices(id) | NULL until billed (REQ-004) |
| created_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | — |
| updated_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | — |

**Relationships**: many TimeEntries belong to a Project; once
`invoice_id` is set, the row becomes immutable (enforced in service layer).

### Invoice
| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PRIMARY KEY | — |
| client_id | UUID | NOT NULL, FK clients(id) | — |
| period_start | DATE | NOT NULL | first day of billed month |
| period_end | DATE | NOT NULL | last day of billed month |
| total_cents | INTEGER | NOT NULL | denormalised sum of lines (REQ-005, NFR-002) |
| currency | CHAR(3) | NOT NULL | copied from project at generation |
| generated_at | TIMESTAMPTZ | NOT NULL DEFAULT now() | — |
| pdf_bytes | BYTEA | NULL | cached PDF for REQ-006; lazily populated |

**Relationships**: one Invoice has many InvoiceLines; each line is a
projection of the TimeEntries it billed.

### InvoiceLine
| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | UUID | PRIMARY KEY | — |
| invoice_id | UUID | NOT NULL, FK invoices(id) ON DELETE CASCADE | — |
| project_id | UUID | NOT NULL, FK projects(id) | grouping (REQ-005) |
| project_name_snapshot | VARCHAR(120) | NOT NULL | preserves history if renamed |
| minutes_total | INTEGER | NOT NULL | sum of entries grouped to this line |
| rate_cents_snapshot | INTEGER | NOT NULL | — |
| amount_cents | INTEGER | NOT NULL | round((minutes_total/60) * rate_cents_snapshot) |

**Relationships**: many InvoiceLines belong to one Invoice; the set of
TimeEntries billed to a line is recoverable via `time_entries.invoice_id
+ time_entries.project_id`.

## API / Interface Design

| Method | Path | Auth | REQ | Description |
|---|---|---|---|---|
| POST | /auth/login | none | — | Email + password → JWT |
| POST | /clients | JWT | REQ-001 | Create a client |
| GET | /clients | JWT | REQ-001 | List clients (excludes archived by default) |
| POST | /projects | JWT | REQ-001 | Create a project under a client with initial rate |
| PATCH | /projects/:id | JWT | REQ-001, REQ-002 | Rename or update rate |
| POST | /time-entries | JWT | REQ-003 | Create a time entry |
| GET | /time-entries | JWT | REQ-003 | List entries, filter by project / date range |
| PATCH | /time-entries/:id | JWT | REQ-004 | Edit an unbilled entry (409 if billed) |
| DELETE | /time-entries/:id | JWT | REQ-004 | Delete an unbilled entry (409 if billed) |
| POST | /invoices | JWT | REQ-005, NFR-002 | Generate an invoice for client + month |
| GET | /invoices/:id | JWT | REQ-005 | Get JSON view of an invoice + lines |
| GET | /invoices/:id/pdf | JWT | REQ-006 | Return invoice as application/pdf |

## File Structure
```
freelance-time-tracker/
├── src/
│   ├── app.js                # Express app wiring
│   ├── server.js             # entry point — listens on PORT
│   ├── db/
│   │   ├── pool.js           # pg-pool singleton (DATABASE_URL)
│   │   └── migrations/       # numbered SQL migrations
│   ├── middleware/
│   │   ├── auth.js           # JWT verification
│   │   └── errorHandler.js   # central error → JSON response
│   ├── routes/
│   │   ├── auth.routes.js
│   │   ├── clients.routes.js
│   │   ├── projects.routes.js
│   │   ├── timeEntries.routes.js
│   │   └── invoices.routes.js
│   ├── services/
│   │   ├── timeEntry.service.js
│   │   ├── invoice.service.js   # REQ-005 generation logic
│   │   └── pdf.renderer.js      # REQ-006 PDF assembly
│   └── lib/
│       └── money.js          # integer-cents math helpers (NFR-002)
├── tests/
│   ├── routes/
│   └── services/
├── package.json
├── railway.json              # Railway service config
└── README.md
```

## Security Design
- Authentication: email + password, bcrypt-hashed (12 rounds), short-lived
  JWT (1 hour) signed with `JWT_SECRET` from Railway env vars. No refresh
  tokens in v1.0 — the freelancer re-logs after expiry.
- Authorization: every authenticated route filters by `freelancer_id`
  resolved from the JWT subject. There is no admin role.
- Transport: Railway terminates TLS at the edge; the Node service trusts
  the proxy and rejects requests where `X-Forwarded-Proto` is not `https`
  in production.
- Input validation: every request body is parsed with a `zod` schema at
  the route boundary; validation errors return 400 with field-level
  messages.
- Secrets: `DATABASE_URL`, `JWT_SECRET` injected via Railway environment;
  no secrets in repo, `.env.example` only.

## Open Questions
- [ ] When the freelancer generates an invoice for a month that includes
      partially-billable entries spanning a month boundary, does the
      invoice include the whole entry or only the portion within
      `period_start..period_end`? (Current assumption: entry's
      `entry_date` is the sole determinant.)
- [ ] Should rate changes apply retroactively to *unbilled* entries on
      the same project, or only to entries created after the change?
      (Current implementation: only new entries; existing unbilled
      entries keep their snapshot rate.)
- [ ] What is the canonical tax handling for invoices — flat tax line,
      per-project tax, or no tax in v1.0? (No tax handling is currently
      designed; would alter Invoice + InvoiceLine schemas.)

## Changelog
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-18 | Initial design |
