# tasks.md
> Freelance Time Tracker — Version v1.0 — 2026-05-18

## Legend
- [ ] Not started
- [~] In progress
- [x] Complete
- [!] Blocked — reason noted inline

---

## Phase 1: Foundation
*Goal*: Stand up an empty but deployable Express + PostgreSQL service on
Railway with authentication wired in, so every later task lands on a
working baseline.

- [ ] **TASK-001** [REQ-001, REQ-003]: Initialize Node.js project, add
      Express, pg, jsonwebtoken, bcrypt, zod, pdfkit, jest as dependencies.
  - _Refs rationale_: Foundation for every later REQ; pinning deps now
    prevents drift later.
  - _Output_: `package.json`, `package-lock.json`, `src/server.js`
    listening on `process.env.PORT`.
  - _Verify_: `npm install && node src/server.js` boots; curl to `/health`
    returns `200 {"ok":true}`.

- [ ] **TASK-002** [REQ-001, REQ-003, REQ-005]: Create initial PostgreSQL
      migration with `clients`, `projects`, `time_entries`, `invoices`,
      `invoice_lines` tables matching design.md data models exactly.
  - _Refs rationale_: All persistence requirements depend on this schema.
  - _Output_: `src/db/migrations/001_init.sql` plus a `npm run migrate`
    script that applies pending migrations.
  - _Verify_: Run `npm run migrate` against a fresh PostgreSQL; `\d` on
    each table shows the column types and constraints from design.md.

- [ ] **TASK-003** [REQ-001..REQ-006]: Configure Railway deployment —
      `railway.json`, environment variables (`DATABASE_URL`, `JWT_SECRET`,
      `PORT`), and `npm start` script.
  - _Refs rationale_: Deployment target was confirmed as Railway in the
    interview; failing to wire this early blocks every smoke test.
  - _Output_: `railway.json`, `.env.example`, README deploy section.
  - _Verify_: `railway up` from a clean clone reaches a public URL and
    `/health` responds 200.

- [ ] **TASK-004** [REQ-001..REQ-006]: Implement JWT auth middleware
      (`src/middleware/auth.js`) plus `POST /auth/login` returning a
      1-hour JWT signed with `JWT_SECRET`.
  - _Refs rationale_: Every protected endpoint depends on this; design.md
    Security Design section mandates JWT.
  - _Output_: `src/middleware/auth.js`, `src/routes/auth.routes.js`,
    bcrypt password verification.
  - _Verify_: Login with valid creds returns 200 + JWT; login with bad
    creds returns 401; a protected route called without `Authorization`
    returns 401.

---

## Phase 2: Core Features
*Goal*: Implement the freelancer-facing capabilities — projects, time
entries, invoice generation, and PDF export.

- [ ] **TASK-005** [REQ-001, REQ-002]: Implement client and project CRUD
      routes (`POST/GET /clients`, `POST/PATCH /projects`).
  - _Refs rationale_: REQ-001 (create/archive projects), REQ-002 (update
    rate without rewriting history).
  - _Output_: `src/routes/clients.routes.js`,
    `src/routes/projects.routes.js`, `src/services/project.service.js`.
  - _Verify_: Create a client + project, then PATCH rate from $80 → $100;
    historical project read still records the rate change at the right
    timestamp.

- [ ] **TASK-006** [REQ-003, NFR-001]: Implement time entry create + list
      routes (`POST /time-entries`, `GET /time-entries`).
  - _Refs rationale_: REQ-003 defines the create contract; NFR-001 sets
    the latency target for these endpoints.
  - _Output_: `src/routes/timeEntries.routes.js`,
    `src/services/timeEntry.service.js` with zod request schemas.
  - _Verify_: POST returns 201 with the new id; GET filtered by
    project_id + date range returns only matching entries.

- [ ] **TASK-007** [REQ-004]: Implement edit + delete on time entries
      with the "billed entries are immutable" rule.
  - _Refs rationale_: REQ-004 specifies the 409 `invoice_locked` response.
  - _Output_: `PATCH /time-entries/:id`, `DELETE /time-entries/:id`,
    service-layer guard checking `invoice_id IS NULL`.
  - _Verify_: PATCH on an unbilled entry returns 200; PATCH on a billed
    entry returns 409 with `error_code: "invoice_locked"`.

- [ ] **TASK-008** [REQ-005, NFR-002]: Implement invoice generation
      (`POST /invoices`) — gather unbilled entries for client + month,
      group by project, compute totals in integer cents, persist
      invoice + invoice_lines, and stamp `invoice_id` on the included
      time entries inside one transaction.
  - _Refs rationale_: REQ-005 defines grouping; NFR-002 demands
    cent-accurate totals — implementation must stay in integers.
  - _Output_: `src/services/invoice.service.js`, `src/lib/money.js`.
  - _Verify_: Generate an invoice over a seeded month; recomputed total
    from `invoice_lines.amount_cents` equals `invoices.total_cents`
    exactly, and previously unbilled `time_entries.invoice_id` is now set.

- [ ] **TASK-009** [REQ-006]: Implement PDF export
      (`GET /invoices/:id/pdf`) using `pdfkit`, rendering freelancer
      details, client name, line items, and grand total.
  - _Refs rationale_: REQ-006 specifies the PDF content and Content-Type.
  - _Output_: `src/services/pdf.renderer.js`, route handler returning
    `Content-Type: application/pdf`.
  - _Verify_: Request returns a PDF whose extracted text (via `pdfreader`
    in tests) contains the freelancer name, client name, every line item
    description, and the grand total.

---

## Phase 3: Validation
*Goal*: Prove the system meets its acceptance and non-functional
criteria before declaring v1.0 ready.

- [ ] **TASK-010** [REQ-001..REQ-006]: Write Jest integration tests
      that exercise the acceptance criterion for each REQ-001..REQ-006
      end-to-end against a test database.
  - _Refs rationale_: The acceptance criteria in requirements.md are the
    contract — without tests, they're aspirations.
  - _Output_: `tests/routes/*.test.js`, one describe-block per REQ.
  - _Verify_: `npm test` passes; every REQ-xxx appears in at least one
    test name or comment.

- [ ] **TASK-011** [NFR-001]: Write a k6 load script that hits time
      entry create/list/edit at 50 VUs for 5 minutes.
  - _Refs rationale_: NFR-001 sets a p95 ≤ 200 ms target; this is how
    we verify it.
  - _Output_: `tests/load/timeEntries.k6.js`, README instructions.
  - _Verify_: Run against a Railway-deployed staging environment; k6
    summary reports `http_req_duration p(95) < 200`.

- [ ] **TASK-012** [NFR-002]: Write a property-based test (fast-check)
      generating 10 000 random invoices and asserting recomputed total
      equals stored total for every one.
  - _Refs rationale_: NFR-002 measurement is exactly this property test.
  - _Output_: `tests/services/invoiceTotal.property.test.js`.
  - _Verify_: `npm test -- invoiceTotal.property` reports 10 000 runs,
    0 shrinks, 0 failures.

---

## Changelog
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-18 | Initial task list |

---

## Completed Tasks Archive
<!-- Move [x] tasks here at end of each sprint to keep active list clean -->
