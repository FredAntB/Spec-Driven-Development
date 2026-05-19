# tasks.md
> Supplier Invoice Reconciliation Service — Version v0-retrofit — 2026-05-18

## Legend
- [ ] Not started
- [~] In progress
- [x] Complete
- [!] Blocked — reason noted inline

---

## Phase 1: Spec Verification
*Goal*: Confirm that requirements.md and design.md actually match the
live codebase before any new feature work begins. Every [TO VERIFY]
marker in design.md and every entry in the Retrofit Assumptions
section of requirements.md must be resolved here. No production code
changes in this phase — only reading, measurement, and spec edits.

- [ ] **TASK-001** [REQ-001]: Verify the exact request shape of
      `POST /api/invoices` — multipart vs JSON, field name(s), content
      types accepted, and the response body shape.
  - _Refs rationale_: REQ-001 acceptance criterion depends on the real
    contract; the current text is inferred.
  - _Output_: Updated REQ-001 acceptance criterion and a note in
    design.md replacing the inferred upload assumption.
  - _Verify_: A sample `curl` matching the documented shape uploads a
    PDF successfully against the live service.

- [ ] **TASK-002** [REQ-002]: Verify that the `pdf-parser` module
      returns structured line items (description / quantity / unit
      price / line total) rather than raw text.
  - _Refs rationale_: REQ-002 assumes structured output; if the module
    returns text only, REQ-002 must be rewritten before downstream
    tasks proceed.
  - _Output_: Updated REQ-002 wording if needed and removal of the
    "[TO VERIFY]" markers on InvoiceLine fields in design.md.
  - _Verify_: Feed three real supplier PDFs through `pdf-parser` in a
    repl; confirm the returned shape matches the InvoiceLine table.

- [ ] **TASK-003** [REQ-003]: Read the `matching-engine` module and
      document the actual MongoDB query keys used to find purchase
      orders.
  - _Refs rationale_: The matching key (PO number vs SKU vs date
    window) drives both the PurchaseOrder schema and the open
    questions in design.md.
  - _Output_: Updated design.md PurchaseOrder + POLine tables with
    confirmed (not [TO VERIFY]) field types and a note recording the
    real matching key.
  - _Verify_: A test invoice + seeded PO produce the expected match
    using only the documented key.

- [ ] **TASK-004** [REQ-004]: Verify the discrepancy definition used
      by `discrepancy-reporter` — strict equality, tolerance, or
      quantity-aware? Confirm or amend REQ-004 accordingly.
  - _Refs rationale_: One of the open questions in design.md; affects
    whether REQ-005 emails will fire on rounding-only deltas.
  - _Output_: Updated REQ-004 acceptance criterion that names the
    actual tolerance rule, and removal of the matching open question
    from design.md.
  - _Verify_: Run the reporter against a fixture with a $0.01-only
    delta; documented behaviour matches observed behaviour.

- [ ] **TASK-005** [REQ-001..REQ-004]: Confirm whether processed
      invoices are persisted in MongoDB today or whether the service
      is purely request-scoped, and record the answer in design.md.
  - _Refs rationale_: REQ-005 (email) and REQ-006 (approval) both
    require a stable invoice reference; this is a blocker for Phase 2
    design.
  - _Output_: Updated design.md Invoice table — remove [TO VERIFY] on
    every field that is in fact persisted; add a note for any field
    that turns out not to exist.
  - _Verify_: A processed invoice is retrievable by id after the
    request completes, OR the spec records that it is not and Phase 2
    must add persistence first.

---

## Phase 2: Email Notification + Approval Workflow
*Goal*: Ship REQ-005 (discrepancy email) and REQ-006 (manager
approval) on top of the verified Phase-1 baseline.

- [ ] **TASK-006** [REQ-005]: Implement the email notifier module
      that sends one email per flagged invoice to a configured
      recipient list, triggered after the discrepancy reporter
      completes.
  - _Refs rationale_: REQ-005 acceptance criterion specifies one
    email per flagged invoice with the discrepancy summary in the body.
  - _Output_: `next-phase/email-notifier/` module, hooked into the
    request pipeline after `discrepancy-reporter`. Recipient list
    configured via environment variable.
  - _Verify_: Process a fixture invoice with one flagged line; capture
    the outbound email via a test SMTP sink and confirm exactly one
    message was sent containing the line description and the delta.

- [ ] **TASK-007** [REQ-005]: Persist a `Discrepancy` document per
      flagged line and set `notified_at` once the email is sent.
  - _Refs rationale_: Without persistence, re-runs would duplicate
    emails on the same flagged invoice.
  - _Output_: Discrepancy collection writes in `email-notifier` plus
    a guard that skips already-notified discrepancies.
  - _Verify_: Replay the same flagged invoice twice; the second pass
    sends zero emails and `notified_at` is unchanged.

- [ ] **TASK-008** [REQ-006]: Add an auth boundary covering the new
      approval endpoint, using the mechanism resolved by the
      design-question outcome from TASK-005.
  - _Refs rationale_: REQ-006 introduces a privileged Manager action
    that cannot ship while the service is fully open.
  - _Output_: Auth middleware applied to `POST
    /api/invoices/:id/approve`, rejecting unauthenticated requests
    with 401.
  - _Verify_: Hitting the approve endpoint without credentials returns
    401; hitting it with valid Manager credentials returns 200.

- [ ] **TASK-009** [REQ-006]: Implement the approval endpoint —
      flip a matched invoice's status to "approved" inside a single
      atomic operation and reject re-approval / mutation with 409.
  - _Refs rationale_: REQ-006 acceptance criterion specifies the
    `invoice_locked` error code on re-approval.
  - _Output_: `next-phase/approval-workflow/` module + route handler.
  - _Verify_: Approve a matched invoice → 200 and status "approved";
    second POST to the same endpoint → 409 with `error_code:
    "invoice_locked"`.

- [ ] **TASK-010** [REQ-005, REQ-006]: Add integration tests that
      cover the REQ-005 and REQ-006 acceptance criteria end-to-end
      using a MongoDB test container and the SMTP sink from TASK-006.
  - _Refs rationale_: Without these, the new requirements are
    unverified contracts.
  - _Output_: Integration test files under the project's existing test
    folder (path [TO VERIFY] from Phase-1 work).
  - _Verify_: `npm test` passes; each new test names the REQ it covers.

---

## Changelog
| Version | Date | Change |
|---|---|---|
| v0-retrofit | 2026-05-18 | Initial retrofit task list |

---

## Completed Tasks Archive
<!-- Move [x] tasks here at end of each sprint to keep active list clean -->
