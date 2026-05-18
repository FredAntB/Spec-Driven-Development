# Community Beta Plan — spec-driven-development v1.0
# Target: 5 testers, 2-week window, structured feedback

---

## Objective

Validate the skill against real users who did not design it, using
natural language and real projects — not curated test prompts.

Controlled testing (Phases 2A/2B/2C) confirmed the skill works
correctly for anticipated inputs. Beta confirms it works for
unanticipated ones.

---

## Tester Profiles

Five profiles selected to cover every distinct usage path in the skill.
Each tester is assigned one primary scenario. They should not be told
what the "right" experience looks like — natural, uncoached usage is
the signal.

---

### Tester 1 — The Complete Beginner
**Profile:** Developer with 0–2 years experience. Has heard of
"writing specs" but never done it. No existing SDD knowledge.
Uses Claude.ai casually. No Claude Code.

**Assigned scenario:**
Start a new personal project from scratch using the skill.
The project can be anything real they want to build.

**What we're watching:**
- Does the skill trigger from their natural phrasing?
- Does the interview feel like a conversation or a form?
- Can they understand the three output files without explanation?
- Does the generated requirements.md make sense to them?

**Success condition:** Tester completes a full spec (all 3 files)
for their project without abandoning the process or asking for
help outside the skill.

---

### Tester 2 — The Solo Developer
**Profile:** 3–7 years experience. Writes code daily. Has thought
about specs but skips them under deadline pressure. Uses Claude Code
or Cursor as their primary AI tool.

**Assigned scenario:**
Use the skill to set up SDD on a real side project they're currently
building. They likely have some code already (partial retrofit).

**What we're watching:**
- Does the retrofit vs greenfield routing work for "I have some code"?
- Do the AI config files (CLAUDE.md / .cursorrules) actually work
  in their Claude Code or Cursor session after being generated?
- Does the tasks.md format match how they naturally think about work?

**Success condition:** Tester generates a working CLAUDE.md or
.cursorrules and successfully uses it in their AI tool session,
with the agent reading the spec before each change.

---

### Tester 3 — The Team Lead
**Profile:** 5–12 years experience. Leads a team of 2–5 devs.
Different team members use different AI tools (mixture of Copilot,
Cursor, Claude Code). Frustrated by inconsistent AI outputs across
the team.

**Assigned scenario:**
Use the skill to create a shared SDD constitution for their team's
current active project. Must generate config files for at least
2 different AI tools used by different team members.

**What we're watching:**
- Does the cross-AI config generation work for a real team scenario?
- Do different team members' AI tools actually produce more consistent
  outputs after installing the config files?
- Is the Universal Instruction Block phrasing clear enough that a
  team member can explain it to a colleague without reading the skill?

**Success condition:** At least 2 AI tools are configured and at
least one team member not involved in the setup can use their tool
with the spec files without additional instruction.

---

### Tester 4 — The Existing Codebase Owner
**Profile:** Any experience level. Has a codebase of 3+ months with
no written specs. The code is the truth and they need to catch the
docs up to it.

**Assigned scenario:**
Use the skill to retrofit their existing codebase into SDD.
They must end up with a requirements.md and design.md that
accurately reflect what the system actually does today.

**What we're watching:**
- Does "help me document what my system does" trigger the skill?
- Does the [TO VERIFY] convention make sense and get used correctly?
- Is the Retrofit Gap Flagging useful or annoying?
- Does the v0-retrofit version marker cause any confusion?

**Success condition:** Tester can share the generated retrofit spec
with a colleague who wasn't in the conversation, and that colleague
agrees it accurately describes the existing system.

---

### Tester 5 — The Cross-AI Power User
**Profile:** Experienced developer who deliberately uses multiple AI
tools for different tasks (e.g., Cursor for implementation, Copilot
for quick completions, Claude Code for architecture). Currently
experiencing agent drift.

**Assigned scenario:**
Use the skill to set up SDD across all their AI tools simultaneously
on an active project. Then run all configured tools against the same
task and compare outputs.

**What we're watching:**
- Do all 3–4 generated config files work correctly in their
  respective tools without modification?
- Do the agents actually behave more consistently when given the
  same spec files vs without?
- Are there any tool-specific quirks the skill's config additions
  don't account for?

**Success condition:** Tester reports that agents from at least
2 different tools produce outputs that don't contradict each other
when working from the same spec.

---

## Timeline

```
Day 0    Publish to GitHub as v1.0-beta. Recruit 5 testers.
         Post to: Dev.to, Hacker News (Show HN), X/Twitter,
                  Claude Discord, cursor.directory forums.

Day 1–3  Onboarding. Each tester receives:
         - Link to the GitHub repo
         - Their tester brief (scenario + what to watch for)
         - Link to the feedback issue template
         - One rule: use natural language, don't try to trigger
           the skill with "correct" phrasing

Day 4–7  Active testing window (first half).
         Watch GitHub Issues for friction reports.
         Do NOT help testers — let them struggle naturally.
         That struggle IS the data.

Day 8    Optional mid-point check-in (async, not a call).
         Ask one question only:
         "What's the most confusing thing so far, in one sentence?"

Day 9–13 Active testing window (second half).
         Testers complete their scenario and file final feedback.

Day 14   Beta closes. Triage all issues.
         Categorize into: trigger miss / interview friction /
         output quality / cross-AI / retrofit / other.
         Prioritize fixes by frequency × severity.

Day 15+  Action fixes. Cut v1.1.
```

---

## Feedback Collection

Testers file GitHub Issues using the feedback template.
No forms, no surveys — Issues keep feedback public and searchable.

Three issue types:

**Bug** — skill did something wrong
Label: `beta-bug`
Template: What I said → What happened → What I expected

**Miss** — skill didn't trigger when it should have
Label: `beta-miss`
Template: Exact phrase I used → What the skill did instead

**Friction** — skill worked but felt wrong
Label: `beta-friction`
Template: Which step → What felt off → What would have been better

---

## Success Criteria

Beta passes if:

| Criterion | Target |
|---|---|
| Testers completing their scenario | 4/5 |
| Critical output failures (wrong files generated) | 0 |
| Trigger miss rate on natural phrasings | < 20% |
| Cross-AI config files working without modification | ≥ 3/5 tools tested |
| Average tester satisfaction (1–5 self-reported) | ≥ 4.0 |

Beta fails if:
- 2 or more testers abandon their scenario
- Any critical file generation error (placeholder in output, wrong workflow triggered)
- Cross-AI UIB inconsistency discovered in the wild

---

## What Happens After Beta

**If beta passes:** Cut v1.1 with all fixes applied. Submit to
SkillsMP, SkillHub, and claudeskills.info. Tag v1.0-beta as
superseded. Announce on the same channels used for recruitment.

**If beta fails:** Triage all issues. Identify root cause(s).
Apply fixes. Rerun Phase 1 test suite (13 prompts) plus any new
assertions derived from beta failures. Cut v1.1-beta and run a
second, smaller beta (2–3 testers) focused on the failure areas.
