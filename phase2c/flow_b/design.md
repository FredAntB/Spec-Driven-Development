# design.md
> Supplier Invoice Reconciliation Service — Version v0-retrofit — 2026-05-18
>
> Retrofit design. Sections marked [TO VERIFY] reflect inferences from
> the operator's description rather than reads of the live code, and
> must be confirmed against the codebase before being treated as fact.

## Architecture Overview
A Node.js HTTP service deployed on Railway, receiving supplier PDF
invoice uploads at `POST /api/invoices`. Three internal modules form
the processing pipeline:

1. `pdf-parser` — wraps `pdf-parse`; turns the uploaded PDF into a
   structured list of invoice line items.
2. `matching-engine` — queries MongoDB for purchase orders and pairs
   each invoice line with at most one PO line.
3. `discrepancy-reporter` — formats the match output, flagging amount
   mismatches between invoice and PO lines.

There is no authentication layer today; the service is reachable only
from inside the internal network. The next phase adds an email
notifier and an approval endpoint, both of which will require auth
to be designed before they can ship.

**Stack**: Node.js, MongoDB, deployed on Railway. Framework, ODM,
test runner, and HTTP body parser are [TO VERIFY] — the operator
named the runtime and database only.

## System Diagram
```
[Internal uploader]
        │ multipart PDF
        ▼
┌────────────────────────────┐
│  POST /api/invoices route  │
└──────────────┬─────────────┘
               ▼
        ┌────────────┐      ┌──────────────────┐
        │ pdf-parser │ ───▶ │ matching-engine  │ ───┐
        └────────────┘      └──────────────────┘    │
                                    │               ▼
                                    │       ┌──────────────────┐
                                    ▼       │ MongoDB          │
                          ┌──────────────────────┐  - purchase_orders
                          │ discrepancy-reporter │  - invoices (?)
                          └──────────┬───────────┘
                                     ▼
                              HTTP response body
                              (email — next phase)
```

## Data Models

### Invoice
| Field | Type | Constraints | Notes |
|---|---|---|---|
| _id | ObjectId | PRIMARY KEY | MongoDB default |
| supplier_id | String | [TO VERIFY] | inferred from matching key; could be supplier name |
| invoice_number | String | [TO VERIFY] | extracted from PDF; uniqueness rule unknown |
| invoice_date | Date | [TO VERIFY] | extracted from PDF |
| currency | String | [TO VERIFY] | assumed single-currency per invoice |
| total_amount | Number | [TO VERIFY] | grand total parsed from PDF |
| lines | Array<InvoiceLine> | [TO VERIFY] | embedded line items |
| status | String | [TO VERIFY] | "matched" / "unmatched" / next phase: "approved" |
| created_at | Date | inferred | timestamp of upload |

### InvoiceLine (embedded)
| Field | Type | Constraints | Notes |
|---|---|---|---|
| description | String | [TO VERIFY] | line description from PDF |
| quantity | Number | [TO VERIFY] | quantity parsed from PDF |
| unit_price | Number | [TO VERIFY] | unit price parsed from PDF |
| line_total | Number | [TO VERIFY] | quantity × unit_price (or as printed) |
| matched_po_line_id | ObjectId | [TO VERIFY] | null if unmatched |
| discrepancy_amount | Number | [TO VERIFY] | null when matched and equal |

### PurchaseOrder
| Field | Type | Constraints | Notes |
|---|---|---|---|
| _id | ObjectId | PRIMARY KEY | — |
| po_number | String | [TO VERIFY] | matching key candidate |
| supplier_id | String | [TO VERIFY] | matching key candidate |
| status | String | [TO VERIFY] | "open" / "closed" |
| lines | Array<POLine> | [TO VERIFY] | embedded line items |

### POLine (embedded)
| Field | Type | Constraints | Notes |
|---|---|---|---|
| sku | String | [TO VERIFY] | possible alternate matching key |
| description | String | [TO VERIFY] | — |
| quantity | Number | [TO VERIFY] | — |
| unit_price | Number | [TO VERIFY] | — |
| line_total | Number | [TO VERIFY] | — |

### Discrepancy (next phase — REQ-005)
| Field | Type | Constraints | Notes |
|---|---|---|---|
| _id | ObjectId | PRIMARY KEY | — |
| invoice_id | ObjectId | NOT NULL | back-reference |
| line_index | Number | NOT NULL | index into invoices.lines |
| invoice_amount | Number | NOT NULL | snapshot at flag time |
| po_amount | Number | NOT NULL | snapshot at flag time |
| delta | Number | NOT NULL | invoice_amount − po_amount |
| notified_at | Date | NULL | set when REQ-005 email is sent |

## API / Interface Design

| Method | Path | Auth | REQ | Description |
|---|---|---|---|---|
| POST | /api/invoices | none (internal) | REQ-001, REQ-002, REQ-003, REQ-004 | Upload PDF; returns match/discrepancy result |
| GET | /api/invoices/:id | [TO VERIFY] | REQ-003 | Fetch a previously processed invoice (existence unconfirmed) |
| POST | /api/invoices/:id/approve | TBD (next phase) | REQ-006 | Manager approval on matched invoice |

## File Structure
```
supplier-invoice-reconciliation/
├── api/
│   └── invoices/             # POST /api/invoices route handler [TO VERIFY exact path]
├── modules/
│   ├── pdf-parser/           # wraps pdf-parse (REQ-002)
│   ├── matching-engine/      # MongoDB PO lookup + pairing (REQ-003)
│   └── discrepancy-reporter/ # mismatch formatter (REQ-004)
├── next-phase/               # to be added
│   ├── email-notifier/       # REQ-005
│   └── approval-workflow/    # REQ-006
├── package.json              # [TO VERIFY contents]
└── README.md                 # [TO VERIFY presence]
```

## Security Design
- Current: no authentication; the service is internal-network-only.
  This is acceptable in the v0-retrofit scope but must change before
  REQ-006 ships, because the approval endpoint introduces a privileged
  Manager action that cannot be left open.
- Next phase: introduce an auth boundary (mechanism [TO VERIFY] —
  likely a signed header from the internal SSO gateway, but not yet
  decided) before `/api/invoices/:id/approve`.
- Secrets (MongoDB URI, email transport credentials for REQ-005) come
  from Railway environment variables; none in the repo.

## Open Questions
- [ ] What is the exact matching key used by `matching-engine` — supplier
      + PO number, supplier + SKU, or a date-window heuristic? This
      determines whether REQ-003 fields are stable.
- [ ] Are processed invoices persisted in MongoDB today, or does the
      service return results without persistence? This blocks the
      design of REQ-005 (email needs a stable invoice reference).
- [ ] What tolerance, if any, applies when comparing invoice vs PO
      amounts? Is a $0.01 rounding delta a discrepancy?
- [ ] What is the intended auth mechanism for the next-phase Manager
      approval endpoint — internal SSO, signed token, or basic auth?
- [ ] Should REQ-005 emails be batched per invoice, batched per
      discrepancy line, or batched per day?

## Changelog
| Version | Date | Change |
|---|---|---|
| v0-retrofit | 2026-05-18 | Initial retrofit design |
