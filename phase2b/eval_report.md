# Phase 2B Behavioral Evaluation Report
Date: 2026-05-18
Skill version: v1.0
Tester: Claude Code (Code tab, local session)

## Summary
Total: 15  Pass: 15  Warn: 0  Fail: 0

## Results

| Test | Prompt (short) | Result | Notes |
|------|---------------|--------|-------|
| 01   | "start new project" | PASS | Single conversational question about project purpose; no bullets, no other questions. |
| 02   | "how do I plan before I code" | PASS | Explains the three spec files and ends with an offer to set them up. |
| 03   | "my AI keeps going off script" | PASS | Names spec drift, prescribes the three files, one follow-up question. |
| 04   | "task management API in Node.js" | PASS | Acknowledges Node.js, asks only about database next. |
| 05   | "set up cursor and claude code" | PASS | Gate holds — names noted, asks project purpose first. |
| 06   | "requirements for a SaaS dashboard" | PASS | Refuses to fabricate from a product category, asks for specifics. |
| 07   | "make a cursorrules file" | PASS | Doesn't generate, asks if specs already exist. |
| 08   | "copilot + windsurf consistency" | PASS | Explains Universal Instruction Block, names both config files, offers setup. |
| 09   | "I already have a codebase" | PASS | Routes to retrofit, asks what the system does today. |
| 10   | "document what my system does" | PASS | Routes to SDD retrofit (not README/wiki), asks what system does today. |
| 11   | "just start coding the login page" | PASS | Anti-pattern push-back with concrete edge cases (OAuth, reset, session). |
| 12   | "add dark mode" | PASS | Spec presence check before any CSS or implementation. |
| 13   | "update my tasks.md" | PASS | Asks which task first; flags divergence check as next step, doesn't bundle. |
| 14   | "continue where we left off" | PASS | Announces Session 4, names TASK-007 / POST /tasks from fixture. |
| 15   | "what are we working on?" | PASS | Acknowledges missing CONTEXT.md, offers to create it. |

## Simulated responses (for the record)

### TEST-01
> Happy to help you spec it out. What does the project do — who are its users and what's the core job it performs?

### TEST-02
> Spec Driven Development is the answer most teams reach for. You write three short files first: `requirements.md` (what the system must do, with concrete acceptance criteria), `design.md` (how it's structured — data models, endpoints, file tree), and `tasks.md` (the ordered, atomic build steps that each reference a requirement). Together they give you (and any AI agent) a single source of truth so work doesn't drift.
>
> Want me to walk you through setting these up for a real project? I can interview you in a few quick questions and generate the files.

### TEST-03
> What you're hitting is spec drift — the agent has no single source of truth, so it makes assumptions and invents requirements that weren't part of the plan. The fix is to give it three short files to anchor on: `requirements.md` (what to build), `design.md` (how it's structured), and `tasks.md` (the ordered steps), and have the agent read them before every action. Which project is this happening on?

### TEST-04
> Good start — Node.js noted. What database are you planning to use?

### TEST-05
> Cursor and Claude Code noted — I'll set both up so they stay in sync. Before I generate any config, I need a bit of project context so the files aren't generic. What does the project do — who uses it and what's the core job?

### TEST-06
> "SaaS dashboard" is a category, not a project — if I drafted requirements from that alone I'd be inventing features that may not match what you're actually building. What does this dashboard specifically do, and who uses it?

### TEST-07
> A `.cursorrules` file is only useful if it points Cursor at a real spec — otherwise it's just boilerplate that doesn't constrain anything. Before I generate one, do you already have a `requirements.md` and `design.md` for this project, or should we create those first?

### TEST-08
> The trick is a Universal Instruction Block — one identical chunk of rules (which spec files to read, what's off-limits, when to stop and ask) that you drop into every agent's config. For your stack that means `.github/copilot-instructions.md` for Copilot and `.windsurfrules` for Windsurf, each carrying the same block plus a couple of agent-specific lines. The block anchors them both to the same `requirements.md`, `design.md`, and `tasks.md`, so they can't drift away from each other.
>
> Want me to set this up for your project? I'd need a quick read on what you're building and the stack first.

### TEST-09
> Got it — we'll retrofit the specs by reverse-engineering them from what's already built rather than designing from scratch. The goal is to capture truth from the live system, not invent new requirements. To start, what does the system do today — describe it as if you were explaining it to a new teammate?

### TEST-10
> Happy to — and the most useful form is a Spec Driven Development retrofit: `requirements.md` (what the system does today), `design.md` (how it's actually structured), and `tasks.md` (the next phase of work). That way the documentation is enforceable by your AI agents, not just a static write-up. To start the discovery, what does the system do today?

### TEST-11
> Hold on — login pages look small but they hide branching paths (OAuth vs. password, reset flows, session vs. JWT, lockouts) that bite later if they aren't decided up front. Do you already have a `requirements.md` for this project, or should we sketch what the login flow needs to handle first?

### TEST-12
> Before I add dark mode, this needs a home in the spec — otherwise it lands as drive-by code and the next feature contradicts it. Do you have a `requirements.md` for this project so I can add a REQ for the theming behavior and update `design.md` before touching code?

### TEST-13
> Two-step close: first I need the specific task. Which one did you finish — TASK-id or a brief description? Once you tell me, I'll check whether `design.md` needs updating before I mark it `[x]`.

### TEST-14
> Session 4 resuming. Last session (3) closed out TASK-005 (JWT middleware) and TASK-006 (its unit tests). Active task is TASK-007 — implementing the POST /tasks endpoint, Phase 2 (Core endpoints), in progress with no blocker. Ready to pick up there, or do you want to start something different?

### TEST-15
> I don't see a `CONTEXT.md` in this project, so I don't have session state to resume from. What's the active task, or want me to create a `CONTEXT.md` so the next session can pick up automatically?

## Failures and Warnings (detail)

None — all 15 tests passed with zero failed P conditions and zero triggered F conditions.

## Phase 2B Conclusion

PASSED — 15/15. The skill's behavioral guardrails held across newbie triggers, the generation gate, cross-AI requests, retrofit routing, anti-pattern push-back, the two-step task-close protocol, and both CONTEXT.md states (present + absent). No SKILL.md changes recommended from this run; proceed to the next phase of evaluation or release.
