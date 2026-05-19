# requirements.md
> Supplier Invoice Reconciliation Service — Version v0-retrofit — 2026-05-18
>
> This is a retrofit specification: REQ-001..REQ-004 were reverse-engineered
> from the existing system as described by the operator. REQ-005..REQ-006
> describe the next planned phase of work. Every inferred behaviour is
> listed in the "Retrofit Assumptions" section and must be verified
> against the live code before it can be treated as fact.

## Overview
The system ingests supplier PDF invoices uploaded over an internal API,
extracts line items from each invoice, matches them against open
purchase orders held in MongoDB, and produces a report flagging any
discrepancy where invoice amounts do not match the corresponding PO.
The service is currently internal-only (no authentication). The next
phase adds email notification on flagged discrepancies and a manager
approval workflow for matched invoices.

## Actors
- **Operator**: Internal user (or upstream system) that uploads supplier
  PDF invoices to the service.
- **Manager** (next phase only): Internal user who reviews matched
  invoices and signs off via the approval workflow.
- **Notification recipient** (next phase only): Email address(es)
  receiving discrepancy alerts.

## Functional Requirements

### Current behaviour (reverse-engineered from live system)
- **REQ-001**: The service shall accept a PDF invoice upload at
  `POST /api/invoices` and store/process it as a new invoice record.
  - _Acceptance_: A multipart PDF upload returns a success response
    containing an invoice identifier, and the same identifier is
    retrievable via the matching/reporting path.

- **REQ-002**: The service shall extract line items (description,
  quantity, unit price, line total) from each uploaded PDF using the
  `pdf-parser` module (built on `pdf-parse`).
  - _Acceptance_: Given a known sample invoice PDF, the extracted
    line-item list contains the expected count of lines and the line
    totals sum to the PDF's printed grand total within ±$0.01.

- **REQ-003**: The matching engine shall query MongoDB for purchase
  orders that correspond to each extracted line item and produce a
  per-line match result.
  - _Acceptance_: For a test fixture with both matched and unmatched
    lines, the matching engine returns a result set in which every
    line is tagged either "matched" (with the PO reference) or
    "unmatched".

- **REQ-004**: The discrepancy reporter shall flag any line where the
  invoice line amount does not equal the matched PO line amount and
  produce a formatted mismatch output.
  - _Acceptance_: Given an invoice with one line at $120 and a PO line
    at $100, the reporter output lists that line with both amounts and
    a clearly marked discrepancy of $20.

### Next-phase behaviour (planned, not yet built)
- **REQ-005**: The service shall send an email notification to a
  configured recipient list whenever a discrepancy is flagged on an
  invoice.
  - _Acceptance_: Processing an invoice that triggers REQ-004 results
    in exactly one email being sent per flagged invoice to every
    configured recipient, with the discrepancy summary in the body.

- **REQ-006**: A Manager shall be able to review a matched (no-
  discrepancy) invoice and record an explicit approval, after which
  the invoice's status moves from "matched" to "approved" and is
  immutable.
  - _Acceptance_: A Manager-authenticated POST to an approval endpoint
    on a matched invoice flips the invoice status to "approved" and a
    subsequent attempt to re-approve or modify the invoice returns a
    409 with `error_code: "invoice_locked"`.

## Out of Scope (v0-retrofit)
- Public / external access — the service remains internal-only until
  authentication is added (likely in a later phase).
- OCR for image-only / scanned PDFs — current `pdf-parse` pipeline
  assumes text-extractable PDFs.
- Automatic PO creation when no PO is found — unmatched lines are
  reported, not auto-provisioned.
- Multi-currency reconciliation — current matching assumes a single
  shared currency between invoice and PO.
- A user-facing UI — interaction is API + email only in this phase.
- Payment execution (issuing payments to suppliers).

## Retrofit Assumptions
The following behaviours were inferred from the operator's description
and the named modules. Each must be confirmed against the live code
before being relied on:

- **REQ-001 assumption**: Upload is multipart with a single PDF part,
  not a JSON body with a base64 field. The endpoint name `/api/invoices`
  was confirmed; the exact body shape is inferred.
- **REQ-002 assumption**: The `pdf-parser` module currently extracts
  line items as structured rows (not just raw text). If it returns raw
  text only, REQ-002 must be rewritten to describe a downstream parsing
  step that is not yet in scope.
- **REQ-003 assumption**: PO lookup keys on a supplier identifier plus
  a PO reference number visible on the invoice. The matching key is not
  yet confirmed — it may instead key on SKU or supplier+date window.
- **REQ-003 assumption**: One invoice line corresponds to at most one PO
  line. Multi-line allocation (one invoice line covering multiple PO
  lines) was not described and is assumed out of scope.
- **REQ-004 assumption**: Discrepancy is defined strictly as numeric
  amount mismatch. Tolerance, rounding rules, and quantity-vs-unit-price
  attribution are not yet specified.
- **General assumption**: There is currently no persistence of the
  discrepancy report itself beyond returning it from the request — it
  may live only in the HTTP response. The next phase (REQ-005 email)
  may require persisting it.

## Changelog
| Version | Date | Change |
|---|---|---|
| v0-retrofit | 2026-05-18 | Initial retrofit + next-phase REQs |
