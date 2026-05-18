# Phase 2A — Assertion Spec
# SDD Skill: spec-driven-development
# Version under test: v2.1b

Each assertion is self-contained: prompt (if behavioral), target file, check method, and pass condition.
Categories: TRIGGER, GATE, INTERVIEW, RETROFIT, TEMPLATE, ANTIPATTERN, CONSISTENCY

---

## Category 1: TRIGGER — Description vocabulary and length

ASSERT-001
  File:   SKILL.md (description field)
  Check:  len(description) <= 1024
  Pass:   True

ASSERT-002
  File:   SKILL.md (description field)
  Check:  'requirements' in description
  Pass:   True

ASSERT-003
  File:   SKILL.md (description field)
  Check:  'cursorrules' in description
  Pass:   True

ASSERT-004
  File:   SKILL.md (description field)
  Check:  'CLAUDE.md' in description
  Pass:   True

ASSERT-005
  File:   SKILL.md (description field)
  Check:  'SDD' in description
  Pass:   True

ASSERT-006
  File:   SKILL.md (description field)
  Check:  'document my system' in description
  Pass:   True  [retrofit trigger — was silent fail in v1]

ASSERT-007
  File:   SKILL.md (description field)
  Check:  'no specs yet' in description
  Pass:   True  [retrofit trigger]

ASSERT-008
  File:   SKILL.md (description field)
  Check:  'I already have a codebase' in description
  Pass:   True  [retrofit trigger]

ASSERT-009
  File:   SKILL.md (description field)
  Check:  'describe my architecture' in description
  Pass:   True  [retrofit trigger]

---

## Category 2: GATE — Generation gate completeness

ASSERT-010
  File:   SKILL.md
  Check:  'Generation Gate' section exists
  Pass:   True

ASSERT-011
  File:   SKILL.md (gate section)
  Check:  count of '□' == 4
  Pass:   True  [four required answers, not three]

ASSERT-012
  File:   SKILL.md (gate section)
  Check:  'Only when all four' in gate section
  Pass:   True  [confirms three→four update applied]

ASSERT-013
  File:   SKILL.md (gate section)
  Check:  'product category' in gate section
  Pass:   True  [bypass pattern: "create requirements for a SaaS dashboard"]

ASSERT-014
  File:   SKILL.md (gate section)
  Check:  'naming tools' in gate section
  Pass:   True  [bypass pattern: "set up cursor and claude code"]

ASSERT-015
  File:   SKILL.md (gate section)
  Check:  'concrete deliverable name' in gate section
  Pass:   True  [bypass pattern: "make a cursorrules file"]

ASSERT-016
  File:   SKILL.md (gate section)
  Check:  'stack' and 'deployment' appear as separate gate items
  Pass:   True  [2a/2b split — was single item causing Warn on prompt 04]

ASSERT-017
  File:   SKILL.md (gate section)
  Check:  'stack ≠ deployment' OR 'both are required separately' in gate
  Pass:   True  [rationale for the split must be explicit]

---

## Category 3: INTERVIEW — Conversational rule and examples

ASSERT-018
  File:   SKILL.md (Step 1)
  Check:  'exactly ONE question' in Step 1
  Pass:   True  [conversational rule, non-negotiable]

ASSERT-019
  File:   SKILL.md (Step 1)
  Check:  '2a' and '2b' both in Step 1
  Pass:   True  [stack and deployment split in required answers list]

ASSERT-020
  File:   SKILL.md (Step 1)
  Check:  'one does not imply the other' OR 'stack ≠ deployment' in Step 1
  Pass:   True  [rationale for split must appear near the list]

ASSERT-021
  File:   SKILL.md (Step 1)
  Check:  'Example of correct pacing' section exists
  Pass:   True

ASSERT-022
  File:   SKILL.md (Step 1)
  Check:  'Example of partial-answer handling' section exists
  Pass:   True

ASSERT-023
  File:   SKILL.md (Step 1 — partial-answer example)
  Check:  'never bundle them' in partial-answer example
  Pass:   True  [explicit annotation that compound questions are forbidden]

ASSERT-024
  File:   SKILL.md (Step 1 — partial-answer example)
  Check:  partial-answer example contains >= 3 turn pairs (User/Claude alternations)
  Pass:   True  [must show sequential turns, not a compound question]

ASSERT-025
  File:   SKILL.md (Step 1 — partial-answer example)
  Check:  no single Claude turn in example contains both 'database' and 'deploy'
  Pass:   True  [the specific compound question that caused the last Warn — must be split]

---

## Category 4: RETROFIT — Retrofit workflow completeness

ASSERT-026
  File:   SKILL.md
  Check:  'Workflow: Existing Project (Retrofit)' section exists
  Pass:   True

ASSERT-027
  File:   SKILL.md (Retrofit section)
  Check:  retrofit interview contains >= 5 numbered questions
  Pass:   True  [full structured interview, not a one-liner]

ASSERT-028
  File:   SKILL.md (Retrofit section)
  Check:  '[TO VERIFY]' mentioned as marking convention
  Pass:   True  [unknown fields must be marked, not invented]

ASSERT-029
  File:   SKILL.md (Retrofit section)
  Check:  'v0-retrofit' in retrofit section
  Pass:   True  [version convention to distinguish from forward-looking specs]

ASSERT-030
  File:   SKILL.md (Retrofit section)
  Check:  'Retrofit Gap Flagging' section exists
  Pass:   True  [assumption log requirement]

ASSERT-031
  File:   SKILL.md (Retrofit section)
  Check:  'code is the truth' OR 'code as the truth' in retrofit section
  Pass:   True  [key mental model framing for retrofit]

---

## Category 5: TEMPLATE — Spec file template quality

ASSERT-032
  File:   references/templates.md
  Check:  'shall' in requirements.md template section
  Pass:   True  [REQ language convention]

ASSERT-033
  File:   references/templates.md
  Check:  'REQ-' in requirements.md template section
  Pass:   True  [requirement ID format]

ASSERT-034
  File:   references/templates.md
  Check:  'Out of Scope' in requirements.md template section
  Pass:   True  [required section]

ASSERT-035
  File:   references/templates.md
  Check:  'Open Questions' in design.md template section
  Pass:   True  [required section — unknown decisions must not be assumed]

ASSERT-036
  File:   references/templates.md
  Check:  'verification' OR 'Verify' in tasks.md template section
  Pass:   True  [every task needs a verification step]

ASSERT-037
  File:   references/templates.md
  Check:  Universal Instruction Block present (contains 'MANDATORY BEFORE ANY ACTION')
  Pass:   True

ASSERT-038
  File:   references/templates.md
  Check:  'HARD CONSTRAINTS' section in Universal Instruction Block
  Pass:   True

ASSERT-039
  File:   references/templates.md
  Check:  'DIVERGENCE PROTOCOL' section in Universal Instruction Block
  Pass:   True  [agents must stop and report if implementation diverges from design]

---

## Category 6: ANTIPATTERN — Common mistakes coverage

ASSERT-040
  File:   SKILL.md (Common Mistakes section)
  Check:  'just start coding' anti-pattern listed
  Pass:   True

ASSERT-041
  File:   SKILL.md (Common Mistakes section)
  Check:  'Feature request with no spec context' anti-pattern listed
  Pass:   True  [added in v2 — prompt 12 fix]

ASSERT-042
  File:   SKILL.md (Common Mistakes section)
  Check:  'Generating config files before spec exists' anti-pattern listed
  Pass:   True  [gate enforcement at the mistake level]

ASSERT-043
  File:   SKILL.md (Common Mistakes section)
  Check:  'invented content' OR 'fabricate' in Common Mistakes section
  Pass:   True  [no placeholder fabrication]

ASSERT-044
  File:   SKILL.md (Common Mistakes section)
  Check:  'Out of scope section missing' anti-pattern listed
  Pass:   True

---

## Category 7: CONSISTENCY — Cross-file integrity

ASSERT-045
  File:   references/capabilities-and-cross-ai.md
  Check:  'Universal Instruction Block' section exists
  Pass:   True

ASSERT-046
  File:   references/capabilities-and-cross-ai.md
  Check:  'CLAUDE.md' in agent config section
  Pass:   True

ASSERT-047
  File:   references/capabilities-and-cross-ai.md
  Check:  '.cursorrules' in agent config section
  Pass:   True

ASSERT-048
  File:   references/capabilities-and-cross-ai.md
  Check:  '.windsurfrules' in agent config section
  Pass:   True

ASSERT-049
  File:   references/capabilities-and-cross-ai.md
  Check:  'copilot-instructions.md' in agent config section
  Pass:   True

ASSERT-050
  File:   references/capabilities-and-cross-ai.md
  Check:  '.aider.conf.yml' in agent config section
  Pass:   True

ASSERT-051
  File:   references/capabilities-and-cross-ai.md
  Check:  'MANDATORY BEFORE ANY ACTION' in Universal Instruction Block
  Pass:   True  [block must be present in cross-AI reference, not just templates]

ASSERT-052
  File:   references/capabilities-and-cross-ai.md + references/templates.md
  Check:  Universal Instruction Block core text is identical in both files
  Method: Extract block from each file, strip whitespace, compare
  Pass:   True  [cross-file consistency — the whole point of the Universal block]

---

## Total: 52 assertions across 7 categories
## Mechanically checkable here: 52/52
## Requires live skill execution: 0 (all are static file checks)
