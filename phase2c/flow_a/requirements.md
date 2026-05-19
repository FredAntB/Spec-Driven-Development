# requirements.md
> Freelance Time Tracker — Version v1.0 — 2026-05-18

## Overview
Freelance Time Tracker is a single-user web application that lets an
independent freelancer log billable hours against client projects, set
hourly rates per project, and produce monthly invoices as PDF documents
for delivery to clients. It is not a team product — one freelancer account
manages all of their own clients and projects.

## Actors
- **Freelancer**: The sole authenticated user. Creates projects, logs time,
  sets rates, and generates invoices. All system actions are performed by
  the Freelancer.
- **Client**: Receives invoices as PDF email attachments or downloads but
  has no login, no account, and no read or write access to the system.

## Functional Requirements

### Project & Client Management
- **REQ-001**: Freelancer shall create, rename, and archive client projects,
  each tied to a single client name and a default hourly rate.
  - _Acceptance_: Creating a project with name and rate persists it and it
    appears in the project list within 1 second of the response.

- **REQ-002**: Freelancer shall set or update the hourly rate on a project,
  with future time entries billed at the new rate and historical entries
  retaining their original rate.
  - _Acceptance_: After updating a rate from $80 → $100, a new time entry
    is billed at $100 while a pre-existing entry still shows $80 on the
    next invoice preview.

### Time Tracking
- **REQ-003**: Freelancer shall create a time entry against an existing
  project, specifying date, duration (minutes), and an optional description.
  - _Acceptance_: A POST with project_id, date, minutes, and description
    returns 201 with the new entry id and the entry is visible in the
    day's list.

- **REQ-004**: Freelancer shall edit or delete a time entry up until the
  point its containing invoice has been generated; entries on a generated
  invoice are immutable.
  - _Acceptance_: Editing an ungenerated entry succeeds with 200; editing
    an entry whose invoice has been generated returns 409 with an
    "invoice_locked" error code.

### Invoicing
- **REQ-005**: Freelancer shall generate a monthly invoice for a single
  client covering all unbilled time entries within a chosen month, with
  line items grouped by project and a calculated total.
  - _Acceptance_: Generating an invoice for client X for May 2026 produces
    one invoice record listing every unbilled entry in that month for that
    client, grouped by project, with subtotals and a grand total that
    matches the sum of (minutes/60 × rate) for each line.

- **REQ-006**: Freelancer shall export any generated invoice as a PDF
  containing the freelancer's business details, the client name, line
  items with rates and amounts, and the grand total.
  - _Acceptance_: Requesting PDF export of invoice 42 returns a
    Content-Type: application/pdf response whose rendered document
    contains the freelancer name, client name, every line item, and a
    total identical to the JSON invoice total.

## Non-Functional Requirements
- **NFR-001**: API responses for time entry create, list, and edit
  operations shall complete within 200 ms at p95 under a load of 50
  concurrent requests.
  - _Measurement_: k6 load test from a single Railway region produces a
    p95 latency ≤ 200 ms across a 5-minute run at 50 VUs.

- **NFR-002**: Invoice totals shall be financially accurate — line item
  amounts and grand totals must be exact to the cent with no
  floating-point drift across re-renders.
  - _Measurement_: A property-based test that generates 10 000 random
    invoices and recomputes totals from line items produces zero
    mismatches between stored total and recomputed total.

## Out of Scope (v1.0)
- Team or multi-user support (no shared accounts, no roles, no permissions)
- Payment processing or "pay this invoice" links (Stripe, PayPal, ACH)
- Native mobile applications (iOS, Android) — the v1.0 surface is web only
- Recurring or subscription billing
- Time tracking via timer/start-stop button (manual entry only in v1.0)
- Multi-currency support (single freelancer-chosen currency at signup)

## Changelog
| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-18 | Initial spec |
