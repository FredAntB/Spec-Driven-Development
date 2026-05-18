# Spec Driven Development — From Newbie to Hero

> A progressive curriculum for developers who want to build software that actually matches what was intended.

---

## What Is Spec Driven Development?

Spec Driven Development (SDD) is a discipline where **written specifications precede all code**. Before a single line of implementation exists, the team agrees on:

1. **What** the system must do (`requirements.md`)
2. **How** the system will be structured (`design.md`)
3. **Which concrete steps** will build it (`tasks.md`)

AI agents, junior devs, and senior engineers all operate from the same shared truth. The spec is the source of authority — not the developer's memory, not a chat log, not a Jira ticket.

---

## Level 1 — Newbie: Understanding Why Specs Matter

### 1.1 The Cost of Specless Development

When teams skip specs:
- Requirements drift silently (the system does *something*, just not the right thing)
- AI agents hallucinate scope (they complete a task that wasn't asked)
- Rework costs 5–10× more than getting it right the first time
- Handoffs break because knowledge lives in one person's head

### 1.2 The Three Pillars of SDD

| File | Question It Answers | Who Reads It |
|---|---|---|
| `requirements.md` | *What* must this do? | Everyone |
| `design.md` | *How* will it be built? | Engineers, AI agents |
| `tasks.md` | *What are the atomic steps?* | Developer, AI agent executing work |

### 1.3 Your First Spec (Hands-On Exercise)

Pick any small project you've built before. Write 5 sentences for each pillar:

```markdown
# requirements.md (starter)
## Functional Requirements
- The system shall allow users to register with an email and password.
- The system shall send a confirmation email after registration.

## Non-Functional Requirements
- Registration must complete in under 2 seconds on a 4G connection.
```

**Lesson**: Even a rough spec forces clarity. You will immediately discover ambiguity you didn't know existed.

---

## Level 2 — Apprentice: Writing Your First Real Spec

### 2.1 `requirements.md` — The Contract

A good `requirements.md` answers these questions without ambiguity:

- **Actors**: Who uses this system? (User, Admin, External API)
- **Functional requirements**: What can each actor do? Use "shall" language.
- **Non-functional requirements**: Speed, scale, security, accessibility constraints.
- **Out of scope**: Explicitly list what this version does NOT do.
- **Acceptance criteria**: How do we know we're done?

```markdown
# requirements.md

## Overview
A task management API allowing teams to create, assign, and track tasks.

## Actors
- **User**: authenticated team member
- **Admin**: can manage users and delete any task

## Functional Requirements
### Tasks
- REQ-001: Users shall create tasks with a title, description, due date, and assignee.
- REQ-002: Users shall update only tasks they created or are assigned to.
- REQ-003: Admins shall delete any task regardless of ownership.

## Non-Functional Requirements
- NFR-001: All API responses shall return within 300ms at p95 under 1,000 concurrent users.
- NFR-002: All endpoints shall require JWT authentication.

## Out of Scope (v1)
- Real-time notifications
- Mobile application

## Acceptance Criteria
- All REQ-xxx items pass integration tests.
- Load test confirms NFR-001.
```

### 2.2 `design.md` — The Blueprint

The design translates requirements into technical decisions:

```markdown
# design.md

## Architecture
REST API, Node.js + Express, PostgreSQL, deployed on Railway.

## Data Models
### Task
| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| title | VARCHAR(255) | Required |
| description | TEXT | Optional |
| due_date | TIMESTAMPTZ | Required |
| creator_id | UUID FK | References users.id |
| assignee_id | UUID FK | References users.id, nullable |
| created_at | TIMESTAMPTZ | Auto |

## API Endpoints
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | /tasks | User | Create task (REQ-001) |
| PATCH | /tasks/:id | User/Admin | Update task (REQ-002) |
| DELETE | /tasks/:id | Admin | Delete task (REQ-003) |

## Security Design
- JWT validated via middleware on all routes.
- Row-level ownership check before PATCH (REQ-002).

## Open Questions
- [ ] Should soft-delete or hard-delete be used? (impacts audit trail)
```

### 2.3 `tasks.md` — The Execution Plan

Tasks are **atomic**, **ordered**, and **verifiable**:

```markdown
# tasks.md

## Phase 1: Foundation
- [ ] TASK-001: Initialize Node.js project with Express, configure ESLint + Prettier
- [ ] TASK-002: Set up PostgreSQL connection pool with pg-pool
- [ ] TASK-003: Write and run initial migration for `users` table
- [ ] TASK-004: Write and run migration for `tasks` table (design.md § Data Models)

## Phase 2: Auth Middleware
- [ ] TASK-005: Implement JWT validation middleware
- [ ] TASK-006: Write unit tests for middleware (valid token, expired, missing)

## Phase 3: Task Endpoints
- [ ] TASK-007: POST /tasks — implement + integration test (REQ-001)
- [ ] TASK-008: PATCH /tasks/:id — ownership check + test (REQ-002)
- [ ] TASK-009: DELETE /tasks/:id — admin-only + test (REQ-003)

## Phase 4: Validation
- [ ] TASK-010: Load test to confirm NFR-001 (p95 < 300ms @ 1k concurrent)
- [ ] TASK-011: Security review of JWT handling
```

**Key rule**: Every task links back to a REQ or NFR. If a task has no link, question whether it belongs in scope.

---

## Level 3 — Journeyman: SDD with AI Agents

### 3.1 Why AI Agents Drift Without Specs

AI agents are powerful but context-hungry. Without a spec:
- They invent requirements the user never stated
- They make architectural decisions that conflict with your existing system
- Different sessions produce incompatible implementations
- There is no objective way to evaluate if the agent succeeded

With a spec, you can tell an AI agent: *"Complete TASK-007. The full context is in requirements.md and design.md."* The agent has a bounded, verifiable job.

### 3.2 The AI-SDD Workflow

```
Human writes → requirements.md
                    ↓
Human + AI draft → design.md  (AI proposes, human approves)
                    ↓
AI generates → tasks.md       (from approved design)
                    ↓
AI executes → one task at a time, referencing spec files
                    ↓
Human reviews → each task output against acceptance criteria
```

### 3.3 Prompting AI Agents with Specs

**Bad prompt** (no spec context):
> "Build the task creation endpoint"

**Good prompt** (spec-grounded):
> "Complete TASK-007 from tasks.md. The endpoint must satisfy REQ-001 from requirements.md. The data model is defined in design.md § Data Models. Do not modify the database schema. Return only the implementation of POST /tasks and its integration test."

### 3.4 Keeping AI Agents Honest

Add a validation step at the end of every AI task:

```markdown
## After each task, verify:
- [ ] Does the output reference the correct REQ/NFR?
- [ ] Does it match the data model in design.md?
- [ ] Did any new files get created that aren't in the design?
- [ ] Did any existing files get modified outside the task's scope?
```

---

## Level 4 — Advanced: Cross-AI Compatibility

### 4.1 The Drift Problem

When different AI agents (Claude, Copilot, Cursor, Windsurf, GPT-4) work on the same codebase, they each have their own "personality":
- Different naming conventions
- Different error handling patterns
- Different assumptions about libraries

The spec files act as a **common constitution**. But agents also need to be instructed to read them.

### 4.2 AI Setting Files

Each major AI tool has a configuration file that pre-loads context:

| Tool | Config File | Location |
|---|---|---|
| Claude Code | `CLAUDE.md` | Project root |
| Cursor | `.cursorrules` | Project root |
| Windsurf | `.windsurfrules` | Project root |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/` |
| Aider | `.aider.conf.yml` | Project root |
| Continue | `.continue/config.json` | Project root |

### 4.3 The Universal Instruction Block

Every AI setting file should begin with a block that anchors the agent to the spec:

```
You are working on a project governed by Spec Driven Development.

BEFORE taking any action:
1. Read requirements.md to understand what the system must do.
2. Read design.md to understand how the system is structured.
3. Read tasks.md to find the current pending task.

CONSTRAINTS:
- Never implement functionality not present in requirements.md.
- Never change the data model without a corresponding update to design.md.
- Never create files not implied by design.md.
- Mark tasks complete in tasks.md after finishing them.
- If a requirement is ambiguous, ask for clarification instead of guessing.
```

---

## Level 5 — Hero: Governance, Reviews, and Scale

### 5.1 Spec Review Gates

Treat spec changes like code changes:

```
[New Feature Request]
       ↓
Update requirements.md → PR review
       ↓
Update design.md → Architecture review
       ↓
Update tasks.md → Sprint planning
       ↓
Implement (AI or human)
       ↓
Acceptance test against requirements.md criteria
```

### 5.2 Spec Versioning

```markdown
# requirements.md

## Changelog
| Version | Date | Change |
|---|---|---|
| 1.2 | 2025-06-01 | Added REQ-004: bulk task import |
| 1.1 | 2025-05-15 | Tightened NFR-001 from 500ms to 300ms |
| 1.0 | 2025-05-01 | Initial release |
```

### 5.3 When to Split the Spec

For large systems, split by domain:

```
specs/
├── auth/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── tasks-feature/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── notifications/  (future)
    └── requirements.md
```

### 5.4 Metrics for a Healthy Spec

- **Requirement coverage**: Every code module traces to at least one REQ.
- **Task completion rate**: Tasks completed ÷ tasks defined per sprint.
- **Spec drift rate**: How often code diverges from design.md (caught in review).
- **Ambiguity score**: Number of clarifying questions raised per spec review (lower is better).

### 5.5 The Hero Checklist

Before calling a feature "done":

```markdown
- [ ] All REQ-xxx items have passing tests
- [ ] All NFR-xxx items have been measured (not just assumed)
- [ ] design.md reflects the system as-built (updated if changed during implementation)
- [ ] tasks.md shows 100% completion for this phase
- [ ] No undocumented files or modules exist in the codebase
- [ ] Next phase's requirements.md draft has been started
```

---

## Quick Reference Card

```
Newbie    → Understand the three files. Write your first rough spec.
Apprentice → Write production-quality requirements, design, and tasks.
Journeyman → Integrate AI agents. Ground every prompt in the spec.
Advanced   → Cross-AI compatibility. Shared config files. Drift prevention.
Hero       → Governance, versioning, metrics, and spec-as-truth at scale.
```
