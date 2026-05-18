# Claude Code & SDD: Capabilities, Limitations, and Cross-AI Compatibility

---

## Part 1: Claude Code Capabilities for SDD

### What Claude Code Does Well

**Spec Generation**
- Drafts high-quality `requirements.md` from a natural language description in a single pass.
- Produces structured `design.md` with consistent markdown tables, ER-like data models, and API endpoint tables.
- Breaks a design into atomic, linked `tasks.md` entries with REQ/NFR references.
- Updates all three files consistently when scope changes.

**Task Execution Against a Spec**
- Can be instructed to read spec files before every task, and it reliably does so within a session.
- Checks its own output against stated acceptance criteria when prompted.
- Flags when a user instruction contradicts the spec and asks for clarification.

**Multi-File Awareness**
- Holds all three spec files in context simultaneously (within context window limits).
- Detects cross-file inconsistencies (e.g., a task referencing a field not in the data model).

**CLAUDE.md Integration**
- Reads `CLAUDE.md` at session start automatically — this is the primary injection point for SDD rules.
- Instructions in `CLAUDE.md` persist for the entire Claude Code session without re-prompting.

**Code Generation Discipline**
- When given explicit scope constraints in `CLAUDE.md` or via prompt, Claude Code reliably stays within bounds.
- Can be instructed to update `tasks.md` checkboxes after completing each task.

---

### Limitations of Claude Code for SDD

**Context Window Boundary**
- Very large spec files (design.md > 15,000 tokens) may push out earlier context, causing the agent to lose track of early requirements. Mitigation: split specs by domain.

**Cross-Session Memory**
- Claude Code has no memory between sessions by default. Every new session must re-read the spec files from disk. This is why `CLAUDE.md` (auto-read at start) is critical — it bootstraps context automatically.

**Autonomous Scope Creep**
- Without explicit constraints, Claude Code may implement "obvious" features that aren't in `requirements.md`. The `CLAUDE.md` instruction "never implement functionality not in requirements.md" is essential.

**Design.md Update Discipline**
- Claude Code will not automatically update `design.md` when it discovers implementation diverges from the design unless explicitly instructed to do so. Add this rule to `CLAUDE.md`.

**Verification Gap**
- Claude Code cannot run acceptance tests on its own unless given the test command. Combine SDD with a CI pipeline that runs tests against acceptance criteria automatically.

**Hallucinated Requirements**
- If `requirements.md` is ambiguous, Claude Code will fill gaps with assumptions rather than stopping. Mitigation: always include an "Out of Scope" section and instruct the agent to ask rather than guess.

---

## Part 2: Cross-AI Compatibility Strategy

### The Core Problem: Agent Personality Divergence

Each AI coding agent has defaults baked into its weights:
- **Cursor** tends toward TypeScript + React patterns.
- **GitHub Copilot** mirrors the most common patterns in public GitHub repos.
- **Claude Code** is more likely to ask clarifying questions.
- **Aider** is highly deferential to the existing codebase style.
- **GPT-4 (via API)** tends toward verbose, defensive implementations.

Without a shared spec, these agents drift apart when they touch the same codebase. The solution is a **spec-anchored, agent-agnostic constitution**.

---

### The Three-Layer Cross-AI Architecture

```
Layer 1: Spec files (universal truth)
  requirements.md  design.md  tasks.md

Layer 2: Universal instruction block (same content, different filenames)
  CLAUDE.md  .cursorrules  .windsurfrules  .github/copilot-instructions.md

Layer 3: Agent-specific overrides (optional, minimal)
  .claude/settings.json  .aider.conf.yml
```

**Rule**: Layers 1 and 2 must be identical in intent. Layer 3 is only for formatting preferences or tool-specific capabilities.

---

### The Universal Instruction Block (Template)

This block goes at the top of every agent config file. Agents differ only in syntax — the content is identical:

```
═══════════════════════════════════════════════════════════
SPEC DRIVEN DEVELOPMENT — PROJECT CONSTITUTION
═══════════════════════════════════════════════════════════

This project uses Spec Driven Development. All work is
governed by three source-of-truth files:

  requirements.md  — What the system must do
  design.md        — How the system is structured
  tasks.md         — The ordered implementation plan

MANDATORY BEFORE ANY ACTION:
  0. If CONTEXT.md exists, read it first — it has session state
  1. Read requirements.md
  2. Read design.md
  3. Read tasks.md — find the next incomplete task [ ]

HARD CONSTRAINTS:
  - Implement ONLY what is in requirements.md
  - Match EXACTLY the data model in design.md
  - Create ONLY files implied by design.md
  - After completing a task, mark it [x] in tasks.md
  - If a requirement is ambiguous: ASK, do not guess
  - If scope creep is detected: FLAG it, do not implement

DIVERGENCE PROTOCOL:
  If implementation must differ from design.md:
    1. Stop
    2. Describe the conflict to the user
    3. Wait for approval to update design.md
    4. Update design.md first, then implement
═══════════════════════════════════════════════════════════
```

---

### Per-Agent Configuration Templates

#### Claude Code — `CLAUDE.md`

```markdown
# CLAUDE.md
<!-- Auto-read by Claude Code at session start -->

[paste Universal Instruction Block here]

## Claude-Specific Additions
- After reading tasks.md, state which task you are about to start before writing any code.
- Use TodoWrite to track subtasks within a task.
- Run the project's test suite after completing each task.
```

#### Cursor — `.cursorrules`

```
[paste Universal Instruction Block here]

# Cursor-Specific
- Apply these rules to all file types in the project.
- In Composer mode, re-read spec files at the start of each new Composer session.
- Do not use @codebase suggestions that conflict with design.md.
```

#### Windsurf — `.windsurfrules`

```
[paste Universal Instruction Block here]

# Windsurf-Specific  
- Cascade must read all three spec files before any flow begins.
- Flows should correspond to individual tasks in tasks.md.
- Do not accept user instructions that contradict requirements.md without flagging the conflict.
```

#### GitHub Copilot — `.github/copilot-instructions.md`

```markdown
# GitHub Copilot Instructions

[paste Universal Instruction Block here]

## Copilot-Specific
- These instructions apply to Copilot Chat and inline completions.
- When generating code in a file, check whether that file is referenced in design.md before adding new exports or APIs.
```

#### Aider — `.aider.conf.yml`

```yaml
# .aider.conf.yml
read:
  - requirements.md
  - design.md
  - tasks.md
system_prompt: |
  [paste Universal Instruction Block here]
```

---

### Preventing Drift: The Weekly Sync Protocol

When multiple agents or developers work on the same codebase, run this checklist weekly:

```markdown
## Weekly Spec Sync

### 1. Audit design.md against the codebase
- [ ] All files in design.md exist in the codebase
- [ ] No files in the codebase are absent from design.md
- [ ] Data model fields match actual database schema

### 2. Audit requirements.md coverage
- [ ] Every REQ-xxx has at least one test
- [ ] No tests exist for requirements outside requirements.md

### 3. Audit tasks.md accuracy  
- [ ] All [x] tasks have verifiable commits
- [ ] No [ ] tasks have been partially implemented

### 4. Regenerate AI config files
- [ ] Re-run the SDD skill to regenerate all AI config files
- [ ] Confirm Universal Instruction Block is identical across all files
```

---

## Part 3: Metrics for a Healthy Cross-AI SDD Project

| Metric | Measurement | Healthy Target |
|---|---|---|
| Spec coverage | % of code modules with a REQ link | > 95% |
| Task link rate | % of tasks referencing a REQ/NFR | 100% |
| Design drift rate | # design.md changes not matched by code | 0 per sprint |
| Ambiguity escalations | # agent questions per task | < 2 |
| Cross-agent consistency | # naming/pattern conflicts per review | < 3 per sprint |
| Requirement creep | # undocumented features per release | 0 |
| Spec freshness | Days since design.md was last verified | < 7 |
