# Phase 2B — Behavioral Evaluation
# SDD Skill v2.1b
# Run via: "run phase2b eval" in the Code tab with this folder open

---

## Setup

Before running any test:
1. Confirm you have read `SKILL.md` in full this session
2. Confirm you have read `references/templates.md`
3. Acknowledge: "SKILL.md loaded. Beginning Phase 2B — 13 behavioral tests."

---

## Execution Protocol

For EACH test below, follow this exact sequence — no exceptions:

```
STEP 1  Read the prompt and category
STEP 2  Simulate the full response you would give a real user
        — write it completely before looking at the assertions
        — stay in character: you are Claude with SKILL.md as your only system context
        — do not add meta-commentary like "as per the skill..." in the response
STEP 3  Evaluate the simulated response against every PASS and FAIL condition
STEP 4  Record result: PASS (all P conditions met, zero F conditions triggered)
                       FAIL (any P condition missed OR any F condition triggered)
        Include which specific conditions passed/failed
STEP 5  Move to next test
```

After all 13 tests, write the final report to `phase2b/eval_report.md`.

---

## Tests

---

### TEST-01
**Prompt:** `"I want to start a new project"`
**Category:** Newbie trigger
**Expected path:** New project interview — Step 1, first question only

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response contains exactly one sentence ending in `?`
- P2: That question asks about what the project does, who uses it, or what problem it solves
- P3: Response does NOT open with a bullet list or numbered list
- P4: Response is ≤ 4 sentences total

FAIL conditions (ANY triggers FAIL):
- F1: Response contains a code block (``` present)
- F2: Response contains more than one `?`
- F3: Response asks about tech stack, deployment, or AI tools (too early — those are questions 2a, 2b, 3)
- F4: Response generates or previews any file content

---

### TEST-02
**Prompt:** `"how do I plan before I code"`
**Category:** Newbie trigger — Teaching Mode
**Expected path:** Teaching Mode explanation + offer to generate

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response mentions `requirements.md` (or requirements file)
- P2: Response mentions `design.md` (or design file)
- P3: Response mentions `tasks.md` (or tasks file)
- P4: Response ends with an offer to set up the files or start the process
- P5: Response does NOT immediately start the interview (no tech stack or AI tools questions)

FAIL conditions (ANY triggers FAIL):
- F1: Response generates any file content (code block with spec content)
- F2: Response asks for project details before explaining the concept
- F3: Response gives no actionable offer at the end (just explains and stops)

---

### TEST-03
**Prompt:** `"my AI keeps going off script, help"`
**Category:** Newbie trigger — problem diagnosis
**Expected path:** Explain spec drift → ask one follow-up

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response identifies the problem as spec drift, missing source of truth, or agent assumptions
- P2: Response mentions the three spec files (requirements, design, tasks) as the fix
- P3: Response ends with exactly one question (which project / which tool)
- P4: Response contains exactly one `?`

FAIL conditions (ANY triggers FAIL):
- F1: Response generates any file
- F2: Response asks two or more questions
- F3: Response gives no diagnosis — just offers to help without naming the root cause

---

### TEST-04
**Prompt:** `"I'm building a task management API in Node.js"`
**Category:** Spec generation — partial answer
**Expected path:** Acknowledge Node.js → ask for database only (next missing item)

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response acknowledges Node.js explicitly
- P2: Response asks about the **database** (the next missing part of 2a)
- P3: Response contains exactly one `?`
- P4: Response does NOT ask about deployment in the same message as database
- P5: Response does NOT ask about AI tools yet

FAIL conditions (ANY triggers FAIL):
- F1: Response generates requirements.md or any spec file
- F2: Response bundles database + deployment into one question
- F3: Response skips to asking about AI tools before stack is complete
- F4: Response contains a code block

---

### TEST-05
**Prompt:** `"set up cursor and claude code for my team project"`
**Category:** Spec generation — tools named, no project context
**Expected path:** Gate holds → ask what the project does (answer #1 missing)

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response does NOT generate any config file content
- P2: Response acknowledges Cursor and Claude Code were noted
- P3: Response asks what the project does (answer #1 required before any file generation)
- P4: Response contains exactly one `?`

FAIL conditions (ANY triggers FAIL):
- F1: Response contains `.cursorrules` file content
- F2: Response contains `CLAUDE.md` file content
- F3: Response generates any file before project description is given
- F4: Response contains `{{PROJECT_NAME}}` or any unfilled placeholder

---

### TEST-06
**Prompt:** `"create requirements for a SaaS dashboard"`
**Category:** Spec generation — product category, not project description
**Expected path:** Gate holds → interview before generation, no fabrication

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response does NOT generate a requirements.md
- P2: Response asks what the dashboard specifically does or who uses it
- P3: Response signals that "SaaS dashboard" is not enough information to proceed
- P4: Response contains exactly one `?`

FAIL conditions (ANY triggers FAIL):
- F1: Response contains `REQ-001` or any `REQ-xxx` identifiers
- F2: Response contains a markdown code block with requirement content
- F3: Response invents actors (Admin, User) without the user having named them
- F4: Response contains `shall` in a requirements context

---

### TEST-07
**Prompt:** `"make a cursorrules file for my project"`
**Category:** Cross-AI trigger — concrete deliverable, no project context
**Expected path:** Gate holds → ask for project context or check for existing spec

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response does NOT generate a `.cursorrules` file
- P2: Response either asks what the project does OR asks if a `requirements.md` already exists
- P3: Response explains why project context is needed first
- P4: Response contains at most two `?` (one compound check is acceptable here)

FAIL conditions (ANY triggers FAIL):
- F1: Response contains a code block with cursor rules content
- F2: Response contains the Universal Instruction Block text as a generated output
- F3: Response contains `{{PROJECT_NAME}}` or any unfilled placeholder
- F4: Response generates any file content

---

### TEST-08
**Prompt:** `"I use copilot and windsurf, how do I keep them consistent"`
**Category:** Cross-AI trigger — consistency question
**Expected path:** Explain Universal Instruction Block → offer to set up

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response explains the mechanism (Universal Instruction Block, shared mandate, or equivalent concept)
- P2: Response mentions `.github/copilot-instructions.md` or Copilot config
- P3: Response mentions `.windsurfrules` or Windsurf config
- P4: Response ends with an offer to set up OR an offer to explain further
- P5: Response does NOT generate config files before project context is given

FAIL conditions (ANY triggers FAIL):
- F1: Response generates `.github/copilot-instructions.md` content
- F2: Response generates `.windsurfrules` content
- F3: Response gives no explanation — just asks for project details immediately
- F4: Response contains unfilled `{{PLACEHOLDER}}` tokens

---

### TEST-09
**Prompt:** `"I already have a codebase, no specs yet"`
**Category:** Retrofit trigger
**Expected path:** Retrofit workflow → first retrofit interview question only

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response routes to retrofit mode (mentions reverse-engineering, discovering, or catching up)
- P2: Response asks what the system does **today** as the first question
- P3: Response frames the exercise as discovery (not design from scratch)
- P4: Response contains exactly one `?`

FAIL conditions (ANY triggers FAIL):
- F1: Response asks about tech stack as the first question (retrofit question 2, not 1)
- F2: Response asks about AI tools immediately
- F3: Response generates any file
- F4: Response treats this as a new project (asks "what do you want to build?" style)

---

### TEST-10
**Prompt:** `"help me document what my system already does"`
**Category:** Retrofit trigger — documentation phrasing
**Expected path:** Skill activates → retrofit workflow (NOT generic docs)

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response routes to SDD retrofit — mentions `requirements.md`, `design.md`, or `tasks.md` as outputs
- P2: Response asks what the system does today
- P3: Response frames output as spec files, not generic documentation (no mention of README, API docs, wiki)
- P4: Response contains exactly one `?`

FAIL conditions (ANY triggers FAIL):
- F1: Response asks "what format would you like?" (generic docs path)
- F2: Response mentions README, API documentation, or wiki as the output
- F3: Response does not mention spec files at all
- F4: Response generates any content

---

### TEST-11
**Prompt:** `"just start coding the login page"`
**Category:** Edge case — anti-pattern trigger
**Expected path:** Anti-pattern warning → spec first → check for existing spec

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response fires the anti-pattern warning (pushes back on coding without a spec)
- P2: Response gives a concrete reason (names real edge cases like OAuth, password reset, or session handling)
- P3: Response asks about existing spec OR asks what the login flow needs to handle
- P4: Response does NOT write any code

FAIL conditions (ANY triggers FAIL):
- F1: Response writes login page code (any code block with HTML, JS, or backend code)
- F2: Response fires no warning — just starts discussing implementation
- F3: Response is preachy (lectures more than one sentence on why specs matter)
- F4: Response asks two or more separate questions

---

### TEST-12
**Prompt:** `"add dark mode"`
**Category:** Edge case — feature request without spec context
**Expected path:** Spec presence check → ask if requirements.md exists

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response fires the spec presence check before any implementation
- P2: Response asks whether a `requirements.md` exists for this project
- P3: Response explains that dark mode needs to land in the spec before code
- P4: Response contains exactly one `?`

FAIL conditions (ANY triggers FAIL):
- F1: Response mentions `prefers-color-scheme` (CSS implementation detail)
- F2: Response mentions CSS variables in an implementation context
- F3: Response writes any CSS or code
- F4: Response assumes a spec exists and immediately adds dark mode as a REQ

---

### TEST-13
**Prompt:** `"update my tasks.md"`
**Category:** Edge case — existing project flow
**Expected path:** Ask which task completed → check design.md divergence

**Simulate response, then check:**

PASS conditions (ALL must be true):
- P1: Response asks which specific task was completed
- P2: Response asks or checks whether `design.md` needs updating (divergence check)
- P3: Response frames the design.md check as a precondition to closing the task
- P4: Response does NOT modify or generate tasks.md content without knowing which task

FAIL conditions (ANY triggers FAIL):
- F1: Response generates a new tasks.md or adds tasks without being asked
- F2: Response skips the design.md divergence check entirely
- F3: Response marks a task `[x]` without knowing which one
- F4: Response asks two separate questions before establishing which task is done

---

## Grading Rubric

```
PASS   — all P conditions met, zero F conditions triggered
WARN   — all P conditions met, but response quality is borderline
         (e.g. correct behavior but phrasing is awkward or incomplete)
FAIL   — any P condition missed OR any F condition triggered
```

A WARN does not count as a failure for the overall score but must be noted
with the specific concern so it can be addressed in skill iteration.

---

## Report Format

Write the report to `phase2b/eval_report.md` using this structure:

```markdown
# Phase 2B Behavioral Evaluation Report
Date: [date]
Skill version: v2.1b
Tester: Claude Code (Code tab, local session)

## Summary
Total: 13  Pass: X  Warn: X  Fail: X

## Results

| Test | Prompt (short) | Result | Notes |
|------|---------------|--------|-------|
| 01   | "start new project" | PASS | — |
...

## Failures and Warnings (detail)

### TEST-XX — [result]
Simulated response:
> [the response Claude gave]

Conditions failed:
- F1: [why it triggered]

Recommended fix: [what needs to change in SKILL.md]

## Phase 2B Conclusion
[PASSED / FAILED — and what to do next]
```

---

## Final instruction

After writing `phase2b/eval_report.md`, print a one-line summary to the chat:

```
Phase 2B complete: [X]/13 Pass, [X]/13 Warn, [X]/13 Fail — see phase2b/eval_report.md
```
