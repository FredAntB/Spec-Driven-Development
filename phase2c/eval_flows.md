# Phase 2C — End-to-End Flow Evaluation
# SDD Skill v2.1b
# Tests generated file quality — not entry point behavior

---

## Setup

Before running any flow:
1. Confirm SKILL.md has been read in full this session
2. Confirm references/templates.md has been read in full
3. Create the output directories:
   - phase2c/flow_a/
   - phase2c/flow_b/
   - phase2c/flow_c/
   - phase2c/flow_c/.github/
4. Acknowledge: "Phase 2C ready. Running 3 end-to-end flows."

---

## Execution Protocol

For each flow:

```
STEP 1  Read the flow definition completely before starting
STEP 2  Play the SKILL role — respond exactly as the skill would to each
        user turn. Apply every rule in SKILL.md.
STEP 3  After each Claude turn, consume the next pre-scripted user answer
        and continue until the interview is complete
STEP 4  Generate the output files to disk in the correct flow directory
        — use Write tool for each file
        — files must be complete, not truncated or placeholder-filled
STEP 5  After writing all files for a flow, print:
        "Flow [A/B/C] complete — [N] files written to phase2c/flow_[a/b/c]/"
STEP 6  Move to next flow
```

After all 3 flows, run: `python3 phase2c/check_outputs.py`
Write the final report to `phase2c/eval_report_2c.md`

---

## Critical rules for file generation

- Every generated file must be complete — no "[content continues]" or truncation
- No {{PLACEHOLDER}} tokens anywhere in any generated file
- Project names, stack details, and actors must be filled from the interview answers
- The Universal Instruction Block must appear verbatim in every AI config file
  with the project name filled in — never generic or templated
- Write files using the Write tool, not as code blocks in chat

---

## Flow A — Greenfield Project, Full Spec Generation

**Scenario:** First-time SDD user, starting a new project from scratch.
**Output directory:** phase2c/flow_a/

### Pre-scripted conversation

---
**[User opens with:]**
"I want to set up spec driven development for a new project"

**[Claude responds as skill — conduct interview per SKILL.md Step 1 rules]**
*(one question at a time, conversationally)*

---
**[User answer 1 — what does it do:]**
"It's a time tracker for freelancers. They log hours against client projects,
set hourly rates, and generate invoices at the end of the month."

**[Claude asks next question — tech stack (2a)]**

---
**[User answer 2a — stack:]**
"Node.js, Express, PostgreSQL"

**[Claude asks next question — deployment (2b)]**

---
**[User answer 2b — deployment:]**
"Railway"

**[Claude asks next question — AI tools (3)]**

---
**[User answer 3 — AI tools:]**
"Claude Code and Cursor"

**[Claude confirms all answers and states it will now generate the spec files]**

---

### Files to generate for Flow A

Write all 5 files to phase2c/flow_a/ using the Write tool.

**1. requirements.md**
Generate a complete requirements.md for a freelance time tracker with:
- Actors: Freelancer (primary), Client (receives invoices only — no system access)
- At minimum 6 functional requirements (REQ-001 through REQ-006) covering:
  time entry creation, project management, rate setting, invoice generation,
  invoice export (PDF), and time entry editing
- At minimum 2 NFRs covering response time and data accuracy
- A concrete Out of Scope section (at minimum: team/multi-user support,
  payment processing, mobile app)
- Acceptance criteria for every REQ
- Changelog table (v1.0, today's date)

**2. design.md**
Generate a complete design.md covering:
- Architecture: REST API — Node.js + Express backend, PostgreSQL, Railway deployment
- Data models: TimeEntry, Project, Client, Invoice (each with typed fields + constraints)
- API endpoints mapped to REQ references
- File structure (at least 2 levels deep)
- Security design section (JWT auth)
- Open Questions section (at minimum 2 open questions about business rules)
- Changelog table

**3. tasks.md**
Generate a complete tasks.md with:
- At minimum 3 phases (Foundation, Core Features, Validation)
- Every task references at least one REQ or NFR
- Every task has a Verify step
- Tasks are atomic — no single task should span more than ~200 lines of new code
- Changelog table

**4. CLAUDE.md**
Generate CLAUDE.md containing:
- The Universal Instruction Block (from references/templates.md)
- Project name filled in: "Freelance Time Tracker"
- Spec version: v1.0
- Claude-specific additions (per SKILL.md Step 5)
- No {{PLACEHOLDER}} tokens anywhere

**5. .cursorrules**
Generate .cursorrules containing:
- The Universal Instruction Block — core text must be identical to CLAUDE.md
- Project name filled in: "Freelance Time Tracker"
- Cursor-specific additions (per capabilities-and-cross-ai.md)
- No {{PLACEHOLDER}} tokens anywhere

---

## Flow B — Retrofit, Existing Codebase

**Scenario:** Developer with an existing system, no specs yet.
**Output directory:** phase2c/flow_b/

### Pre-scripted conversation

---
**[User opens with:]**
"I already have a codebase, no specs yet"

**[Claude responds as skill — routes to retrofit workflow, asks first retrofit question]**

---
**[User answer 1 — what it does today:]**
"It processes supplier invoices. It reads PDF invoices, extracts line items,
matches them against purchase orders in our database, and flags discrepancies
where the invoice amount doesn't match the PO."

**[Claude asks next retrofit question — tech stack]**

---
**[User answer 2 — stack:]**
"Node.js, MongoDB, deployed on Railway"

**[Claude asks next question — AI tools]**

---
**[User answer 3 — AI tools:]**
"Just Claude Code for now"

**[Claude asks next question — key files / structure to share]**

---
**[User answer 4 — existing structure:]**
"I can describe it: there's a /api/invoices endpoint that accepts PDF uploads,
a pdf-parser module that uses pdf-parse, a matching-engine module that queries
MongoDB for POs, and a discrepancy-reporter that formats the mismatch output.
No authentication yet — it runs internal-only."

**[Claude asks next question — next planned phase of work]**

---
**[User answer 5 — next phase:]**
"We want to add email notifications when a discrepancy is flagged,
and eventually an approval workflow where a manager can sign off on matched invoices."

**[Claude confirms the retrofit scope and states it will generate the spec files]**

---

### Files to generate for Flow B

Write all 3 files to phase2c/flow_b/ using the Write tool.

**1. requirements.md** (retrofit version)
Generate a v0-retrofit requirements.md that:
- Version marker is "v0-retrofit" — explicitly stated in the file header
- Reverse-engineers current behavior into REQ-xxx statements using "shall" language
- Covers: PDF upload (REQ-001), line item extraction (REQ-002),
  PO matching (REQ-003), discrepancy flagging (REQ-004)
- Adds next-phase requirements: email notification (REQ-005),
  manager approval workflow (REQ-006)
- Has an Out of Scope section
- Has a Retrofit Assumptions section listing every inferred behavior
  that the user didn't explicitly confirm
- Acceptance criteria for every REQ

**2. design.md** (retrofit version)
Generate a design.md that:
- Reflects the described architecture (Node.js, MongoDB, Railway)
- Data models: Invoice, PurchaseOrder, Discrepancy (with typed fields)
- Fields that were NOT explicitly described by the user must be marked [TO VERIFY]
  Example: invoice.vendor_id (inferred from matching logic — mark [TO VERIFY])
- API endpoints section listing known routes
- Open Questions section — at minimum 3 questions about undescribed behavior
- No {{PLACEHOLDER}} tokens

**3. tasks.md** (retrofit version)
Generate a tasks.md that:
- Phase 1 is "Spec Verification" — tasks to confirm requirements.md matches live code
- Phase 2 covers the next planned work (email notifications + approval workflow)
- Does NOT create tasks for work already done (no "set up Node.js" or "create MongoDB schema")
- Every task references a REQ
- Every task has a Verify step

---

## Flow C — Cross-AI Configuration, 4 Tools

**Scenario:** Team lead setting up consistent AI configs across 4 different tools.
**Output directory:** phase2c/flow_c/ and phase2c/flow_c/.github/

### Pre-scripted conversation

---
**[User opens with:]**
"I use copilot and windsurf, how do I keep them consistent — I also use cursor and claude code"

**[Claude responds as skill — explains Universal Instruction Block mechanism,
offers to generate configs, asks what the project is]**

---
**[User answer 1 — what it does:]**
"It's a task board for engineering teams — kanban-style columns,
tasks linked to GitHub PRs, and a team velocity dashboard"

**[Claude asks about tech stack (2a)]**

---
**[User answer 2a — stack:]**
"React with Vite on the frontend, FastAPI on the backend, PostgreSQL"

**[Claude asks about deployment (2b)]**

---
**[User answer 2b — deployment:]**
"AWS — ECS for the backend, S3 + CloudFront for the frontend"

**[Claude confirms all 4 tools and states it will generate matching config files]**
*(AI tools answer was given in the opening message — do not re-ask)*

---

### Files to generate for Flow C

Write all 4 files using the Write tool. The Universal Instruction Block
core text MUST be identical across all 4 files.

**1. CLAUDE.md**
Contains:
- Universal Instruction Block with project name "Engineering Task Board"
- Spec version: v1.0
- Claude Code-specific additions

**2. .cursorrules**
Contains:
- Universal Instruction Block — core text byte-identical to CLAUDE.md
- Project name "Engineering Task Board"
- Cursor-specific additions

**3. .windsurfrules**
Contains:
- Universal Instruction Block — core text byte-identical to CLAUDE.md
- Project name "Engineering Task Board"
- Windsurf-specific additions

**4. .github/copilot-instructions.md**
Contains:
- Universal Instruction Block — core text byte-identical to CLAUDE.md
- Project name "Engineering Task Board"
- Copilot-specific additions

---

## After all 3 flows

Run the assertion checker:
```
python3 phase2c/check_outputs.py
```

Then write the report to phase2c/eval_report_2c.md using this structure:

```markdown
# Phase 2C Evaluation Report
Date: [date]
Skill version: v2.1b

## Summary
Total assertions: 47   Pass: X   Fail: X

## Flow A results — [PASS/FAIL]
[list any failed assertions with detail]

## Flow B results — [PASS/FAIL]
[list any failed assertions with detail]

## Flow C results — [PASS/FAIL]
[list any failed assertions with detail]

## Failures requiring SKILL.md changes
[for each failure: what broke, which rule was violated, recommended fix]

## Phase 2C Conclusion
[PASSED / FAILED — and what to do next]
```

Print one-line summary to chat:
```
Phase 2C complete: [X]/47 assertions pass — see phase2c/eval_report_2c.md
```
