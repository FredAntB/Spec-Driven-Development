# CLAUDE.md
<!-- Auto-read by Claude Code at session start -->

═══════════════════════════════════════════════════════════
SPEC DRIVEN DEVELOPMENT — PROJECT CONSTITUTION
Project: Freelance Time Tracker
Version: v1.0

This project uses Spec Driven Development. All work is
governed by three source-of-truth files:

  requirements.md  — What the system must do
  design.md        — How the system is structured
  tasks.md         — The ordered implementation plan

MANDATORY BEFORE ANY ACTION:
  0. If CONTEXT.md exists, read it first — it has session state
  1. Read requirements.md in full
  2. Read design.md in full
  3. Read tasks.md — find the next incomplete [ ] task

HARD CONSTRAINTS:
  - Implement ONLY what is in requirements.md
  - Match EXACTLY the data model in design.md
  - Create ONLY files listed or implied by design.md
  - Never mark a task [x] without verifying its acceptance criterion
  - If a requirement is ambiguous: ASK, do not guess
  - If scope creep is detected: FLAG it, do not implement

AFTER COMPLETING A TASK:
  1. Run the verification step listed in tasks.md
  2. Mark the task [x] in tasks.md
  3. Report what was done and which REQ/NFR it satisfies

DIVERGENCE PROTOCOL:
  If implementation must deviate from design.md:
    1. Stop immediately
    2. Describe the conflict to the user
    3. Wait for explicit approval to update design.md
    4. Update design.md FIRST, then implement
═══════════════════════════════════════════════════════════

## Claude-Specific Additions
- After reading tasks.md, state which task you are about to start before writing any code.
- Use TodoWrite to track subtasks within a larger task.
- Run `npm test` after completing each task and report the result.
