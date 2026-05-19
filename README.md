# spec-driven-development

> A Claude skill that writes your specs before you write your code —
> and keeps every AI coding tool on the same page.

[![Version](https://img.shields.io/badge/version-1.0--beta-blue)](https://github.com/FredAntB/spec-driven-development/releases/tag/v1.0-beta)
[![CI](https://github.com/FredAntB/spec-driven-development/actions/workflows/ci.yml/badge.svg)](https://github.com/FredAntB/spec-driven-development/actions/workflows/ci.yml)
[![Phase 2A](https://img.shields.io/badge/static%20assertions-64%2F64-brightgreen)](phase2a/assertions.md)
[![Phase 2B](https://img.shields.io/badge/behavioral%20tests-13%2F13-brightgreen)](phase2b/eval_session.md)
[![Phase 2C](https://img.shields.io/badge/generation%20quality-53%2F53-brightgreen)](phase2c/eval_flows.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## The problem this solves

You open Claude Code and ask it to build a feature. An hour later it's
done something technically impressive that isn't quite what you wanted.
You ask Cursor to fix it. It contradicts what Claude Code did. You ask
Copilot to clean up. It invents a third interpretation.

The root cause is always the same: your AI agents have no shared source
of truth. They fill every gap with their own assumptions.

This skill fixes that by creating three files before any code is written:

| File | Answers |
|---|---|
| `requirements.md` | What the system must do |
| `design.md` | How it will be built |
| `tasks.md` | What to build next, in order |

Every AI tool reads from these files before touching code. Drift stops.

---

## Quick start

Install the skill, then start a conversation with any of these:

```
"I want to start a new project"
"my AI keeps going off script, help"
"I already have a codebase, no specs yet"
"set up cursor and claude code for my team project"
```

Claude will ask a few short questions and generate your spec files.
No configuration needed.

---

## Installation

### Claude.ai / Claude desktop app (Chat tab)

1. Download [`spec-driven-development-v1.0.skill`](releases/latest)
2. In Claude settings → Skills → Install from file

Or via CLI:
```bash
claude plugin install FredAntB/spec-driven-development
```

### Claude Code (Code tab)

```bash
git clone https://github.com/FredAntB/spec-driven-development
```

Open the folder in the Code tab. The `CLAUDE.md` file is auto-read
at session start and bootstraps the skill.

**Windows note:** Git must be installed for the Code tab to work
with local folders. Download from [git-scm.com](https://git-scm.com).

---

## What you get

### For a new project (greenfield)

Claude interviews you in 4 short questions — one at a time,
conversationally — then generates:

```
your-project/
├── requirements.md      ← what the system must do
├── design.md            ← how it will be built
├── tasks.md             ← atomic ordered implementation steps
└── CLAUDE.md            ← Claude Code reads this automatically
```

**requirements.md** uses `shall` language and REQ-xxx IDs so every
requirement is traceable:

```markdown
## Functional Requirements

### Tasks
- **REQ-001**: Users shall create tasks with a title, description,
  due date, and assignee.
  - _Acceptance_: POST /tasks returns 201 with the created task object

- **REQ-002**: Users shall update only tasks they created or are
  assigned to.
  - _Acceptance_: PATCH /tasks/:id returns 403 for unauthorized users
```

**tasks.md** links every task back to its requirement inline:

```markdown
## Phase 2: Core endpoints

- [ ] **TASK-007** [REQ-001]: Implement POST /tasks with validation
  - _Output_: Route handler + request schema validation
  - _Verify_: POST /tasks returns 201 with all fields present
```

### For an existing codebase (retrofit)

Same result, reverse-engineered from what you describe:

```
your-project/
├── requirements.md      ← v0-retrofit: discovered from existing code
├── design.md            ← with [TO VERIFY] on every inferred field
└── tasks.md             ← Phase 1 is spec verification, not new code
```

### For cross-AI teams

Generates identical instruction blocks across every tool your team uses:

```
your-project/
├── CLAUDE.md                           ← Claude Code
├── .cursorrules                        ← Cursor
├── .windsurfrules                      ← Windsurf
├── .github/copilot-instructions.md    ← GitHub Copilot
└── .aider.conf.yml                     ← Aider
```

Each file contains the same Universal Instruction Block — agents read
the same mandate, cite the same spec files, follow the same divergence
protocol. The only differences are tool-specific additions.

---

## Supported AI tools

| Tool | Config file | Status |
|---|---|---|
| Claude Code | `CLAUDE.md` | ✓ Tested |
| Cursor | `.cursorrules` | ✓ Tested |
| Windsurf | `.windsurfrules` | ✓ Tested |
| GitHub Copilot | `.github/copilot-instructions.md` | ✓ Tested |
| Aider | `.aider.conf.yml` | ✓ Generated |

---

## The Universal Instruction Block

Every AI config file contains this block, with only the project name
and spec version filled in:

```
═══════════════════════════════════════════════════════════
SPEC DRIVEN DEVELOPMENT — PROJECT CONSTITUTION
Project: Your Project Name
Version: 1.0
═══════════════════════════════════════════════════════════

This project uses Spec Driven Development. All work is
governed by three source-of-truth files:

  requirements.md  — What the system must do
  design.md        — How the system is structured
  tasks.md         — The ordered implementation plan

MANDATORY BEFORE ANY ACTION:
  1. Read requirements.md in full
  2. Read design.md in full
  3. Read tasks.md — identify the next incomplete [ ] task

HARD CONSTRAINTS:
  ✗ Never implement requirements not in requirements.md
  ✗ Never alter the data model without updating design.md first
  ✗ Never create files not listed or implied in design.md
  ✗ Never mark a task [x] without verifying its acceptance criterion
  ✗ Never guess when a requirement is ambiguous — ask instead

DIVERGENCE PROTOCOL:
  If implementation must deviate from design.md:
    → Stop immediately
    → Describe the conflict clearly
    → Wait for explicit user approval
    → Update design.md BEFORE writing code
═══════════════════════════════════════════════════════════
```

---

## Test suite & CI

This skill ships with a complete, runnable test suite — 130 assertions
across three phases. A GitHub Actions workflow runs the automatable
checks on every push and pull request.

### GitHub Actions workflow (`.github/workflows/ci.yml`)

Four jobs run on every push to `main`/`master` and on every PR:

| Job | What it does | Required to pass? |
|---|---|---|
| `phase2a` | Runs 64 static assertions via Python | Yes — hard gate |
| `phase2c` | Runs 53 generation quality checks against committed fixtures | Yes if fixtures present |
| `phase2b-notice` | Prints instructions for running behavioral tests manually | Informational only |
| `all-checks` | Aggregates results — reference this in branch protection rules | Yes |

**Branch protection setup** — in your repo settings, add `all-checks`
as the single required status check. This means one rule covers all
automated phases now and any you add later.

### Running locally

```bash
# Phase 2A — static assertions (64 checks)
python3 phase2a/run_assertions.py

# Windows — if python3 not on PATH or encoding errors occur
PYTHONUTF8=1 python phase2a/run_assertions.py

# Phase 2C — generation quality (53 checks, requires fixture files)
python3 phase2c/check_outputs.py
```

Or paste the KICKOFF.md for each phase into the Claude Code tab
for a zero-setup run from any machine.

### Running in Claude Code (Code tab)

| Phase | Paste this | Output |
|---|---|---|
| 2A | `phase2a/KICKOFF.md` | Runs script, explains any failures |
| 2B | `phase2b/KICKOFF.md` | 13 behavioral tests → `eval_report.md` |
| 2C | `phase2c/KICKOFF.md` | 3 flows → files → `eval_report_2c.md` |

### Phase 2C fixtures

Phase 2C requires Claude Code to generate real spec files, which are
then committed to the repo as fixtures that CI checks on every push.

To regenerate fixtures after a significant skill change:
1. Open the repo folder in the Code tab
2. Paste `phase2c/KICKOFF.md`
3. Commit the files Claude Code writes to `phase2c/flow_a/`,
   `phase2c/flow_b/`, and `phase2c/flow_c/`

CI will automatically pick up the new fixtures on the next push.

### Current test results

| Phase | Type | Assertions | CI |
|---|---|---|---|
| 2A | Static file checks | 64 / 64 ✓ | Automated |
| 2B | Behavioral (live session) | 13 / 13 ✓ | Manual |
| 2C | Generation quality | 53 / 53 ✓ | Automated (fixtures required) |

---

## Trigger phrases

The skill activates on a wide vocabulary. A sample:

**Starting a project:**
`"I want to start a new project"` · `"help me plan before I code"` ·
`"set up SDD for my project"` · `"I need a spec"`

**AI tool setup:**
`"set up cursor and claude code"` · `"make a cursorrules file"` ·
`"my AI keeps going off script"` · `"keep my agents consistent"`

**Existing codebase:**
`"I already have a codebase, no specs yet"` ·
`"help me document what my system does"` ·
`"describe my architecture"` · `"add specs to existing project"`

**Feature requests:**
`"add dark mode"` → triggers spec presence check before any code
`"just start coding"` → triggers anti-pattern warning

---

## Anti-patterns the skill prevents

| Anti-pattern | What the skill does |
|---|---|
| "just start coding" | Pushes back with concrete reasons, asks for spec |
| Feature request without spec context | Checks for requirements.md before proceeding |
| Generating config files before spec exists | Hard gate — interview required first |
| AI guessing at ambiguous requirements | Asks for clarification, never fabricates |
| Out of scope missing from requirements | Flags it and asks what won't be in v1 |

---

## Community beta — we need testers

This skill is in **public beta**. It has passed 118 automated
assertions and 3 end-to-end generation flows, but it has not yet
been tested by strangers using natural language.

We need 5 testers matching these profiles:

- A complete beginner starting their first real project
- A solo developer with an active side project (greenfield or partial)
- A team lead whose team uses multiple AI tools
- A developer with an existing codebase and no written specs
- A developer who actively uses 3+ AI coding tools simultaneously

**To volunteer:** Open an issue titled `[Beta] I'd like to test`
and describe which profile fits you best.

All you need to do is use the skill naturally for your real work
and file issues when something doesn't work. That's it.

---

## Contributing

1. Fork the repo
2. Make your change to `SKILL.md` or the reference files
3. Run the Phase 2A assertion suite: `python3 phase2a/run_assertions.py`
4. If assertions fail, fix them before filing a PR
5. If your change adds new behavior, add a corresponding assertion

New assertions go in `phase2a/assertions.md` (human-readable spec)
and `phase2a/run_assertions.py` (machine-executable check).

---

## Skill structure

```
spec-driven-development/
├── SKILL.md                                  ← the skill (install this)
├── CLAUDE.md                                 ← Code tab bootstrap
├── references/
│   ├── sdd-curriculum.md                     ← newbie-to-hero teaching guide
│   ├── capabilities-and-cross-ai.md          ← Claude Code + cross-AI strategy
│   └── templates.md                          ← spec file + UIB templates
├── phase2a/
│   ├── assertions.md                         ← human-readable test spec
│   └── run_assertions.py                     ← static assertion runner
├── phase2b/
│   ├── eval_session.md                       ← behavioral test definitions
│   └── KICKOFF.md                            ← Code tab eval kickoff
├── phase2c/
│   ├── eval_flows.md                         ← end-to-end flow definitions
│   ├── check_outputs.py                      ← generation quality checker
│   └── KICKOFF.md                            ← Code tab eval kickoff
└── beta/
    ├── BETA_PLAN.md                          ← 5-person beta plan
    ├── TESTER_BRIEF.md                       ← tester onboarding guide
    └── ISSUE_TEMPLATES.md                    ← feedback issue templates
```

---

## License

MIT — use freely, attribution appreciated.

---

## Acknowledgements

Built and tested using the Claude skill framework. Test suite
methodology adapted from the skill-creator eval harness. All
118 assertions were written before the corresponding fixes —
test-first, always.
