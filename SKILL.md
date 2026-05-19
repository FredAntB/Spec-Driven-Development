---
name: spec-driven-development
version: 1.0.0
description: >
  Use this skill to scaffold Spec Driven Development: requirements.md, design.md, tasks.md, and cross-compatible AI config files (CLAUDE.md, .cursorrules, .windsurfrules, .github/copilot-instructions.md). Triggers: 'requirements', 'spec', 'design doc', 'tasks', 'CLAUDE.md', 'cursorrules', 'SDD', 'spec driven', 'AI configuration', 'cross-AI', 'multi-agent', 'agent setup'. Also trigger for: 'set up my AI tools', 'keep agents consistent', 'stop AI going off-script', 'plan before coding', 'structure project for AI'. Retrofit triggers: 'document my system', 'document my codebase', 'describe my architecture', 'write up what we built', 'add specs to existing project', 'no specs yet', 'help me document', 'I already have a codebase'. Use whenever a user wants to start a project, configure coding agents, create spec docs, or prevent AI agents from drifting, hallucinating scope, or producing inconsistent implementations.
---

# Spec Driven Development Skill

This skill guides the user through creating a complete Spec Driven Development environment:
- `requirements.md` — what the system must do
- `design.md` — how it will be built
- `tasks.md` — atomic, ordered implementation steps
- AI agent configuration files for Claude Code, Cursor, Windsurf, GitHub Copilot, and Aider

**Reference files** (read when needed):
- `references/sdd-curriculum.md` — full teaching curriculum, newbie to hero
- `references/capabilities-and-cross-ai.md` — Claude Code capabilities, limitations, cross-AI strategy
- `references/templates.md` — all spec file and AI config templates

---

## When to Read Reference Files

| Situation | Read |
|---|---|
| User is new to SDD and needs explanation | `sdd-curriculum.md` Levels 1–3 |
| User asks about Claude Code + SDD specifics | `capabilities-and-cross-ai.md` Part 1 |
| User wants cross-AI config files | `capabilities-and-cross-ai.md` Part 2–3 |
| You need template content to generate files | `templates.md` |

---

## Workflow: First Run (New Project)

### Step 1: Interview the User

**Conversational rule (non-negotiable):** Ask exactly ONE question, wait for the answer, then ask the next. Never present questions as a numbered list or bullet list — that feels like a form, not a conversation. A newbie who sees three bullets may answer only the first or feel overwhelmed.

**The four required answers before any file is generated:**
1. What the project does and who uses it
2a. Tech stack (language, framework, database)
2b. Deployment target (Railway, Fly.io, AWS, Vercel, etc. — offer to suggest if unknown)
3. Which AI coding tools they use (Claude Code, Cursor, Windsurf, Copilot, Aider, other)

Stack and deployment are separate required answers because one does not imply the other. "Node.js" tells you nothing about deployment. "Railway" tells you nothing about the language. Both must be known independently before generation proceeds.

**If the user's opening message already answers some but not all of these**, acknowledge what you know and ask only for what's missing — still one question at a time.

**Optional follow-ups** (ask only when the user's answer raises real ambiguity):
- "Are there performance, security, or accessibility constraints?"
- "What is explicitly out of scope for this first version?"

Example of correct pacing:
> User: "I want to start a new project"
> Claude: "Happy to help you spec it out. What does the project do — who are its users and what's the core job it performs?"
> User: "It's a task manager for small dev teams"
> Claude: "Got it. What's your tech stack — language, framework, database?"
> User: "Node.js, Express, PostgreSQL"
> Claude: "And where are you planning to deploy? (Railway, Fly.io, AWS — or I can suggest one)"
> User: "Railway"
> Claude: "Last thing — which AI coding tools do you use? (Claude Code, Cursor, Copilot, Windsurf, something else?)"

Example of partial-answer handling:
> User: "I'm building a task management API in Node.js"
> Claude: "Good start — Node.js noted. What database are you planning to use?"
> User: "PostgreSQL"
> Claude: "And where are you deploying? (Railway, Fly.io, AWS — or I can suggest one)"
> User: "Railway"
> Claude: "Last thing — which AI coding tools do you use?"
> *(stack partially given — ask for each missing part one at a time, never bundle them)*

### Generation Gate (enforced between Step 1 and Step 2)

**HARD RULE: No file of any kind may be generated until all four interview answers are in hand.**

This gate applies to every output path — `requirements.md`, `design.md`, `tasks.md`, `.cursorrules`, `CLAUDE.md`, and all other config files. There are no exceptions, including when:
- The user says "create requirements for X" (X is a product category, not a full description)
- The user says "make a cursorrules file" (a concrete deliverable name is not permission to skip the interview)
- The user says "set up Cursor and Claude Code" (naming tools is not the same as providing project context)
- The user gives a partial stack answer like "Node.js" (stack ≠ deployment — both are required separately)
- The user provides some but not all of the four required answers (ask for the rest one at a time)

If any answer is missing, ask for it conversationally before proceeding. Do not generate placeholder files with `{{UNFILLED}}` tokens. Do not generate plausible-sounding fake requirements from a product category alone.

**Gate check before generating any file:**
```
□ Do I know what the project does and who uses it?    → if not, ask first
□ Do I know the tech stack (language/framework/db)?   → if not, ask first
□ Do I know the deployment target?                    → if not, ask first
□ Do I know which AI tools the user uses?             → if not, ask first
Only when all four are ✓ → proceed to Step 2
```

---

### Step 2: Generate `requirements.md`

Read `references/templates.md` for the template. Fill in all `{{PLACEHOLDERS}}`.

**Quality rules for requirements.md:**
- Every functional requirement uses "shall" language (REQ-xxx: Actor shall verb object)
- Every requirement has a concrete acceptance criterion
- NFRs have a measurable metric (not "fast" — use "< 200ms at p95")
- Out of scope section is non-empty (if user didn't provide it, infer likely assumptions)
- Requirement IDs are sequential starting at REQ-001

**Output:** Create `requirements.md` in the project root (or ask for path if ambiguous).

---

### Step 3: Generate `design.md`

Read `references/templates.md` for the template.

**Quality rules for design.md:**
- Every REQ-xxx must map to at least one data model field, endpoint, or component
- Data model fields have explicit types and constraints (not just "string" — use VARCHAR(255) or TEXT with reasoning)
- API endpoints reference the REQ they satisfy
- File structure section shows at minimum the top 2 levels of the project tree
- Open Questions section captures anything the user hasn't decided yet — do not guess, ask

**Output:** Create `design.md` in the project root.

---

### Step 4: Generate `tasks.md`

Read `references/templates.md` for the template.

**Quality rules for tasks.md:**
- Tasks are ordered: infrastructure → data layer → business logic → API layer → tests → validation
- Every task references at least one REQ or NFR **inline on the checkbox line** using the format `**TASK-{{id}}** [REQ-xxx, NFR-xxx]` — not only on a separate `_Refs_:` line. This makes references machine-checkable by static tools and CI scripts.
- Every task has an explicit verification step (a test command, a manual check, a metric measurement)
- Tasks are atomic — one task should not produce more than ~200 lines of new code
- Phase goals are stated in plain English

**Output:** Create `tasks.md` in the project root.

---

### Step 5: Generate AI Agent Configuration Files

Ask the user which agents they use (if not already answered in the interview).

For each selected agent, generate the appropriate config file. Read `references/capabilities-and-cross-ai.md` Part 2 for the per-agent templates.

**Always generate:**
- `CLAUDE.md` (for Claude Code) — even if user didn't ask, this is the baseline

**Generate based on user's tools:**
| Tool | File | Location |
|---|---|---|
| Cursor | `.cursorrules` | Project root |
| Windsurf | `.windsurfrules` | Project root |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/` directory |
| Aider | `.aider.conf.yml` | Project root |

**Quality rules for AI config files:**
- The Universal Instruction Block is IDENTICAL in content across all files (same constraints, same protocol) — only the agent-specific additions differ
- The block references the actual spec file names (`requirements.md`, `design.md`, `tasks.md`)
- Agent-specific additions are minimal — no more than 5 lines of agent-specific rules
- Config files include the project name and spec version in the header

**Output:** Create all requested config files in their correct locations.

---

## Workflow: Existing Project (Retrofit)

Triggered by: "I already have a codebase, no specs yet", "document what my system does", "describe my architecture", "help me document", "write up what we built", "add specs to my project", or any similar phrase implying an existing system without written specs.

### Retrofit Interview (ask one question at a time, conversationally)

The retrofit interview is different from the new project interview — you are discovering truth from existing code, not designing from scratch. Ask these in order:

1. "What does the system do today — describe it as if explaining to a new teammate?"
2. "What's the tech stack? (language, framework, database, deployment)"
3. "Which AI tools do you use on this project?"
4. "Are there parts of the codebase you'd like to share so I can read the actual structure? (key files, folder tree, or a README)"
5. "What's the next feature or phase of work you're planning? (This determines what tasks.md covers)"

Question 4 is important — retrofitting from code is more accurate than retrofitting from memory. Offer to read files if they can share them.

### Retrofit Generation Process

**Step 1 — Reverse-engineer `requirements.md`**
- Ask "What does this system do today?" and turn the description into REQ-xxx statements
- Use past tense internally to distinguish discovered requirements from new ones
- Flag every behavior you infer that the user didn't explicitly confirm: "I'm inferring REQ-004 from what you described — does the system actually enforce this?"
- Add an Out of Scope section based on what's absent from their description
- Mark the version as `v0-retrofit` to distinguish it from a forward-looking spec

**Step 2 — Reverse-engineer `design.md`**
- If files were shared, read the actual folder structure and data models
- If no files were shared, produce a design.md skeleton and mark every section with `[TO VERIFY]`
- Never invent a data model — if you don't know the schema, list the entities and mark fields as `[unknown]`
- Capture the real endpoints or interfaces if available, otherwise list them as open questions

**Step 3 — Generate `tasks.md` for the NEXT phase only**
- Do not create tasks for work already done — that history is in git, not tasks.md
- The first phase should be "Spec Verification": tasks to confirm that requirements.md and design.md actually match the live codebase
- The second phase covers the next feature or planned work the user described in question 5

**Step 4 — Generate AI config files as normal**
- Apply the same generation gate: all three interview answers required first
- The Universal Instruction Block must reference the real spec files by name

### Retrofit Gap Flagging

After generating each file, explicitly list every assumption made:
> "I made the following assumptions — please verify each one:
> - REQ-003: I assumed authentication uses JWT because you mentioned tokens, but I didn't see the auth code
> - design.md § Data Models: The `users` table fields are marked [TO VERIFY] — share the schema migration or model file to confirm"

This is the most important difference between retrofit and new-project workflows. In a new project, the spec is the truth. In a retrofit, the code is the truth and the spec must be verified against it.

---


## Workflow: Updating Specs (Change Request)

When the user wants to add a feature or change existing behavior:

### Spec Presence Check (run before anything else)

When a feature request arrives without explicit spec context in the conversation, do not implement it. Instead, check:

> "Before I add dark mode — do you have a `requirements.md` for this project? If so, I'll check whether it's in scope and add it properly. If not, let's create one first so this change has a home."

A feature request without spec context is one of three situations:
- **Specs exist, in scope** → update requirements.md first, then design.md, then tasks.md, then implement
- **Specs exist, out of scope** → flag the conflict, ask whether to expand scope formally before touching code
- **No specs exist** → route to the Retrofit workflow, build the spec, then handle the feature

Never implement a feature request by jumping straight to code, even if the request seems small. "Add dark mode" or "add a search bar" always has spec implications.

### Change Request Process (when specs are confirmed to exist)

1. Identify which spec file(s) are affected
2. Propose the minimal change to `requirements.md` first (new REQ-xxx or modified acceptance criterion)
3. Show impact on `design.md` (new model fields, endpoints, components, or files)
4. Add new tasks to `tasks.md` in a new phase
5. Remind the user to regenerate AI config files if the project name or version changed

**Never update `design.md` before `requirements.md` is updated first.** The requirement is the authority.

### Task closing protocol ("update my tasks.md")

When a user asks to mark a task done, close it or update tasks.md,
follow this exact two-step sequence — never bundle both steps into
one message:

**Step 1 — Identify the task first:**
Ask which task was completed. Wait for the answer.
> "Which task did you just finish? Give me the TASK-id or a brief description."

**Step 2 — Divergence check after identification:**
Only once the specific task is named, ask whether design.md needs updating.
> "Before I mark TASK-007 `[x]` — did the implementation match `design.md`
> exactly, or did anything diverge? If anything drifted, we update
> design.md first, then close the task."

**Why the order matters:** The divergence question only makes sense in
the context of a specific task. Asking both at once forces the user to
hold two things in mind before answering either. Always identify first,
then check divergence.

---


## Session Management — CONTEXT.md

### The problem this solves

A project's three spec files answer *what to build* and *how to build it*.
They do not answer *where we are right now*. When a user starts a new chat
session — because the context window filled, because they want an isolated
session for a new task, or because a day passed — Claude has no way to know
which task is active, what decisions were made mid-session, or why the code
looks the way it does.

`CONTEXT.md` is the session journal. It bridges instances.

### What CONTEXT.md contains

- **Resume block** — the single most important section: active task ID,
  current phase, status, and any blocker. Claude reads this first and
  resumes without asking.
- **Session log** — one row per session: date, one-line summary, files changed.
  Never transcripts — always summaries.
- **Key decisions** — decisions that aren't obvious from the spec files
  (why JWT over sessions, why PostgreSQL over MongoDB, why soft-delete).
- **Open questions** — unresolved items that haven't made it into design.md yet.
- **Divergences** — places where implementation differs from design.md pending
  a formal update.

### When to create CONTEXT.md

Generate CONTEXT.md as part of the initial spec setup (Step 2–4) or when
a user first asks to resume work in a new session on an existing project.

The file starts minimal — just the resume block and an empty session log.
It grows through use.

### Rules for updating CONTEXT.md

**At the end of any session where work was done:**
1. Add a row to the session log (date, one-line summary, files changed)
2. Update the resume block with the next active task
3. Move any resolved open questions to design.md
4. Record any divergences from design.md that are pending update

**At the start of any session:**
1. Read CONTEXT.md first — before requirements.md, design.md, or tasks.md
2. Announce: "Session [N] resuming. Last worked on: [task]. Picking up at: [task]."
3. If CONTEXT.md does not exist yet, offer to create it

**Never:**
- Record conversation transcripts in CONTEXT.md — only outcomes
- Let the session log grow beyond the last 10 sessions without archiving
  older entries to a `CONTEXT_ARCHIVE.md`
- Update the session log mid-session — only at natural stopping points

### When CONTEXT.md is present — modified startup behavior

When a user starts a session on a project that already has CONTEXT.md,
Claude's opening move changes:

**Without CONTEXT.md:**
> "What are we working on today?"

**With CONTEXT.md:**
> "Session 4 resuming. Last session we completed TASK-005 and TASK-006
> (JWT middleware). Active task is TASK-007 — POST /tasks implementation.
> Ready to continue, or do you want to start something different?"

This is the entire value of CONTEXT.md: the user says nothing and work
continues exactly where it left off.

### Output quality check for CONTEXT.md

Before presenting a generated or updated CONTEXT.md:
- [ ] Resume block has a specific task ID — not "continue development"
- [ ] Session log row added for the current session
- [ ] No conversation transcripts — only outcomes
- [ ] Open questions are questions, not tasks (tasks go in tasks.md)
- [ ] No {{PLACEHOLDER}} tokens remain

---

## Output Quality Checklist

Before presenting any generated file to the user, verify:

**CONTEXT.md** (when generated or updated)
- [ ] Resume block has a specific task ID and status
- [ ] Session log has a row for the current session
- [ ] No conversation transcripts — summaries only
- [ ] Open questions are actual questions, not tasks
- [ ] No `{{PLACEHOLDER}}` tokens


- [ ] All functional requirements use "shall" language
- [ ] All REQ-xxx IDs are unique and sequential
- [ ] Every requirement has an acceptance criterion
- [ ] NFRs have measurable targets
- [ ] Out of scope section is present

**design.md**
- [ ] Every REQ maps to a design element
- [ ] Data model has typed fields with constraints
- [ ] Endpoints reference REQs
- [ ] File structure is present
- [ ] Open questions are captured, not assumed

**tasks.md**
- [ ] Tasks are ordered logically
- [ ] Every task has a REQ/NFR reference
- [ ] Every task has a verification step
- [ ] No single task is too large (> 200 lines of new code is a smell)

**AI config files**
- [ ] Universal Instruction Block is present and complete
- [ ] Content is consistent across all generated config files
- [ ] Agent-specific additions are minimal and non-contradictory
- [ ] Files are in the correct locations

---

## Metrics: Evaluating SDD Health

Read `references/capabilities-and-cross-ai.md` Part 3 for the full metrics table.

Quick summary:

| Signal | Green | Yellow | Red |
|---|---|---|---|
| Spec coverage | > 95% code has REQ link | 80–95% | < 80% |
| Task link rate | 100% tasks have REQ ref | 90–99% | < 90% |
| Ambiguity escalations | < 2 per task | 2–5 | > 5 |
| Design drift rate | 0 per sprint | 1–2 | > 2 |
| Requirement creep | 0 undocumented features | — | Any |

---

## Teaching Mode

If the user is new to SDD, offer to explain concepts using `references/sdd-curriculum.md`:

- **"What is SDD?"** → Summarize sdd-curriculum.md introduction + Level 1
- **"How do I write requirements?"** → Walk through Level 2.1
- **"How do I use AI with specs?"** → Summarize Level 3
- **"How do I set up multiple AI tools?"** → Level 4 + capabilities-and-cross-ai.md Part 2

Always offer to generate the actual files after explaining — teaching and doing go together.

---

## Common Mistakes to Prevent

Actively flag these anti-patterns if you see them in user inputs:

| Anti-pattern | What to say |
|---|---|
| "Just start coding and we'll spec later" | "Let's take 10 minutes to write requirements.md first — it will save hours of rework." |
| Requirements with no acceptance criteria | "How will we know this requirement is satisfied? Let's add a concrete test." |
| Tasks that span multiple days | "This task is very large. Let's break it into smaller atomic steps." |
| Design decisions before requirements | "Let's lock requirements first so the design has a foundation." |
| AI config files that differ from each other | "I'll make sure all your AI agents get the same instruction block." |
| Out of scope section missing | "What won't this version do? Stating it prevents scope creep." |
| Feature request with no spec context | "Before I add that — do you have a requirements.md? I want to make sure this lands in the right place." |
| Generating config files before spec exists | Never produce CLAUDE.md, .cursorrules, or similar until requirements.md is at least drafted. |
| Filling placeholders with invented content | If interview answers are missing, ask — never fabricate plausible requirements from a product category. |
