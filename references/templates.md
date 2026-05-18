# SDD Spec File Templates

These templates are used by the SDD skill to scaffold a new project's specification.
Fill in the `{{PLACEHOLDER}}` values during the interview phase.

---

## Template: requirements.md

```markdown
# requirements.md
> {{PROJECT_NAME}} — Version {{VERSION}} — {{DATE}}

## Overview
{{ONE_PARAGRAPH_DESCRIPTION}}

## Actors
{{#each ACTORS}}
- **{{name}}**: {{description}}
{{/each}}

## Functional Requirements

{{#each FEATURE_GROUPS}}
### {{group_name}}
{{#each requirements}}
- **REQ-{{id}}**: {{actor}} shall {{action}}.
  - _Acceptance_: {{acceptance_criterion}}
{{/each}}
{{/each}}

## Non-Functional Requirements
{{#each NFR}}
- **NFR-{{id}}**: {{description}}
  - _Measurement_: {{how_to_measure}}
{{/each}}

## Out of Scope ({{VERSION}})
{{#each OUT_OF_SCOPE}}
- {{item}}
{{/each}}

## Changelog
| Version | Date | Change |
|---|---|---|
| {{VERSION}} | {{DATE}} | Initial spec |
```

---

## Template: design.md

```markdown
# design.md
> {{PROJECT_NAME}} — Version {{VERSION}} — {{DATE}}

## Architecture Overview
{{ARCHITECTURE_DESCRIPTION}}

**Stack**: {{TECH_STACK}}
**Deployment**: {{DEPLOYMENT_TARGET}}

## System Diagram
```
{{ASCII_OR_MERMAID_DIAGRAM}}
```

## Data Models

{{#each MODELS}}
### {{model_name}}
| Field | Type | Constraints | Notes |
|---|---|---|---|
{{#each fields}}
| {{name}} | {{type}} | {{constraints}} | {{notes}} |
{{/each}}

**Relationships**: {{relationships}}
{{/each}}

## API / Interface Design

{{#if IS_REST_API}}
| Method | Path | Auth | REQ | Description |
|---|---|---|---|---|
{{#each endpoints}}
| {{method}} | {{path}} | {{auth}} | {{req_ref}} | {{description}} |
{{/each}}
{{/if}}

{{#if IS_EVENT_DRIVEN}}
### Events
| Event | Publisher | Subscribers | Payload |
|---|---|---|---|
{{#each events}}
| {{name}} | {{publisher}} | {{subscribers}} | {{payload}} |
{{/each}}
{{/if}}

## File Structure
```
{{PROJECT_ROOT}}/
{{FILE_TREE}}
```

## Security Design
{{SECURITY_NOTES}}

## Open Questions
{{#each OPEN_QUESTIONS}}
- [ ] {{question}}
{{/each}}

## Changelog
| Version | Date | Change |
|---|---|---|
| {{VERSION}} | {{DATE}} | Initial design |
```

---

## Template: tasks.md

```markdown
# tasks.md
> {{PROJECT_NAME}} — Version {{VERSION}} — {{DATE}}

## Legend
- [ ] Not started
- [~] In progress
- [x] Complete
- [!] Blocked — reason noted inline

---

{{#each PHASES}}
## Phase {{phase_number}}: {{phase_name}}
*Goal*: {{phase_goal}}

{{#each tasks}}
- [ ] **TASK-{{id}}** [{{req_refs}}]: {{description}}
  - _Refs rationale_: {{req_refs_rationale}}
  - _Output_: {{expected_output}}
  - _Verify_: {{verification_step}}
{{/each}}

{{/each}}

---

## Completed Tasks Archive
<!-- Move [x] tasks here at end of each sprint to keep active list clean -->
```

---

## The Universal AI Instruction Block

This block is injected into every AI agent config file. Edit the project-specific sections.

```
═══════════════════════════════════════════════════════════
SPEC DRIVEN DEVELOPMENT — PROJECT CONSTITUTION
Project: {{PROJECT_NAME}}
Version: {{SPEC_VERSION}}
═══════════════════════════════════════════════════════════

This project uses Spec Driven Development. All work is
governed by three source-of-truth files:

  requirements.md  — What the system must do
  design.md        — How the system is structured
  tasks.md         — The ordered implementation plan

MANDATORY BEFORE ANY ACTION:
  0. If CONTEXT.md exists, read it first — it has session state
  1. Read requirements.md in full
  2. Read design.md in full
  3. Read tasks.md — identify the next incomplete [ ] task

HARD CONSTRAINTS:
  ✗ Never implement requirements not in requirements.md
  ✗ Never alter the data model without updating design.md first
  ✗ Never create files not listed or implied in design.md
  ✗ Never mark a task [x] without verifying its acceptance criterion
  ✗ Never guess when a requirement is ambiguous — ask instead

AFTER COMPLETING A TASK:
  1. Run the verification step listed in tasks.md
  2. Mark the task [x] in tasks.md
  3. Report what was done and which REQ/NFR it satisfies

DIVERGENCE PROTOCOL:
  If implementation must deviate from design.md:
    → Stop immediately
    → Describe the conflict clearly
    → Wait for explicit user approval
    → Update design.md BEFORE writing code
═══════════════════════════════════════════════════════════
```

---

## Template: CONTEXT.md

```markdown
# CONTEXT.md
> {{PROJECT_NAME}} — Live session journal
> Last updated: {{DATE}} — Session {{SESSION_NUMBER}}

## ⚡ Resume from here

**Active task:** {{CURRENT_TASK_ID}} — {{CURRENT_TASK_DESCRIPTION}}
**Phase:** {{CURRENT_PHASE}}
**Status:** {{in progress | blocked | ready for next task}}
**Blocker (if any):** {{BLOCKER_DESCRIPTION or none}}

> On session start: read this file first, then requirements.md,
> design.md, and tasks.md. Do not ask what to work on — resume
> the active task above unless the user says otherwise.

---

## Session log

| # | Date | What was done | Files changed |
|---|---|---|---|
| {{SESSION_NUMBER}} | {{DATE}} | {{SUMMARY_ONE_LINE}} | {{FILES}} |

*(most recent first — add a row at the start of each session)*

---

## Key decisions

Decisions that are not obvious from the spec files alone.

| Decision | Rationale | Session |
|---|---|---|
| {{DECISION}} | {{WHY}} | {{SESSION_NUMBER}} |

---

## Open questions

Things still to be resolved. Move to design.md once decided.

{{#each OPEN_QUESTIONS}}
- [ ] {{question}}
{{/each}}

---

## Divergences from design.md

Any place where implementation differs from design.md, pending
a formal design.md update.

{{#each DIVERGENCES}}
- {{location}}: {{what differs}} — {{resolution_status}}
{{/each}}

---

## Changelog

| Session | Date | Summary |
|---|---|---|
| {{SESSION_NUMBER}} | {{DATE}} | Session opened |
```
