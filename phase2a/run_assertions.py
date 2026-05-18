#!/usr/bin/env python3
"""Phase 2A Assertion Runner — SDD Skill v2.1b. 52 assertions."""

import re, sys, os

BASE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = open(os.path.join(BASE, "SKILL.md"), encoding="utf-8").read()
TMPL  = open(os.path.join(BASE, "references/templates.md"), encoding="utf-8").read()
CROSS = open(os.path.join(BASE, "references/capabilities-and-cross-ai.md"), encoding="utf-8").read()

results = []
def a(id, desc, passed, note=""): results.append((id, desc, passed, note))

# ── Extractors ───────────────────────────────────────────────────────────────

def section(text, heading):
    """Body of a ## heading until the next ## heading. Safe for SKILL.md."""
    m = re.search(rf"(?:^|\n)#+ {re.escape(heading)}[^\n]*\n", text)
    if not m: return ""
    start = m.end()
    stop = re.search(r"\n## ", text[start:])
    return text[start : start + stop.start()] if stop else text[start:]

def tmpl_section(heading):
    """
    Template section from templates.md — stops at next '## Template:' or
    '## The Universal' peer only, ignoring inner ## headings in code fences.
    """
    m = re.search(rf"(?:^|\n)## {re.escape(heading)}[^\n]*\n", TMPL)
    if not m: return ""
    start = m.end()
    stop = re.search(r'\n## Template:|\n## The Universal', TMPL[start:])
    return TMPL[start : start + stop.start()] if stop else TMPL[start:]

def cross_section(heading):
    """Section from cross-AI file (headings may be ## or ###)."""
    m = re.search(rf"(?:^|\n)#+ {re.escape(heading)}[^\n]*\n", CROSS)
    if not m: return ""
    start = m.end()
    stop = re.search(r"\n## ", CROSS[start:])
    return CROSS[start : start + stop.start()] if stop else CROSS[start:]

def desc_field(text):
    m = re.search(r"description: >\n  (.+?)(?=\n---)", text, re.DOTALL)
    return m.group(1).replace("\n  ", " ").strip() if m else ""

def claude_turns(ex): return re.findall(r'> Claude: "([^"]*)"', ex)

# ── Pre-extract ──────────────────────────────────────────────────────────────
desc      = desc_field(SKILL)
step1     = section(SKILL, "Step 1: Interview the User")
gate      = section(SKILL, "Generation Gate (enforced between Step 1 and Step 2)")
retrofit  = section(SKILL, "Workflow: Existing Project (Retrofit)")
mistakes  = section(SKILL, "Common Mistakes to Prevent")

partial_m = re.search(
    r"Example of partial-answer handling:(.*?)(?=\nExample of correct|\n###|\n##|\Z)",
    SKILL, re.DOTALL)
partial_ex = partial_m.group(1) if partial_m else ""

req_tmpl   = tmpl_section("Template: requirements.md")
des_tmpl   = tmpl_section("Template: design.md")
task_tmpl  = tmpl_section("Template: tasks.md")
uib_tmpl   = tmpl_section("The Universal AI Instruction Block")
uib_cross  = cross_section("The Universal Instruction Block (Template)")

# ════════════════════════════════════════════════════════════
# CATEGORY 1: TRIGGER
# ════════════════════════════════════════════════════════════
a("001","Description ≤ 1024 chars",               len(desc)<=1024,   f"{len(desc)} chars")
a("002","'requirements' in description",           "requirements"            in desc)
a("003","'cursorrules' in description",            "cursorrules"             in desc)
a("004","'CLAUDE.md' in description",              "CLAUDE.md"               in desc)
a("005","'SDD' in description",                    "SDD"                     in desc)
a("006","'document my system' in description",     "document my system"      in desc)
a("007","'no specs yet' in description",           "no specs yet"            in desc)
a("008","'I already have a codebase' in desc",     "I already have a codebase" in desc)
a("009","'describe my architecture' in desc",      "describe my architecture" in desc)

# ════════════════════════════════════════════════════════════
# CATEGORY 2: GATE
# ════════════════════════════════════════════════════════════
a("010","Generation Gate section exists",          "Generation Gate"         in SKILL)
a("011","Gate has exactly 4 □ items",              gate.count("□")==4,    f"found {gate.count('□')}")
a("012","'Only when all four' in gate",            "Only when all four"      in gate)
a("013","'product category' in gate",              "product category"        in gate)
a("014","'naming tools' in gate",                  "naming tools"            in gate)
a("015","'concrete deliverable name' in gate",     "concrete deliverable name" in gate)
a("016","Stack + deployment as separate gate items","tech stack" in gate.lower() and "deployment target" in gate.lower())
a("017","'stack ≠ deployment' in gate",            "stack ≠ deployment"      in gate)

# ════════════════════════════════════════════════════════════
# CATEGORY 3: INTERVIEW
# ════════════════════════════════════════════════════════════
a("018","'exactly ONE question' in Step 1",        "exactly ONE question"    in step1)
a("019","'2a' and '2b' in Step 1",                "2a" in step1 and "2b"   in step1)
a("020","Stack/deploy split rationale in Step 1",  "one does not imply the other" in step1 or "stack ≠ deployment" in step1)
a("021","Correct pacing example exists",           "Example of correct pacing" in SKILL)
a("022","Partial-answer example exists",           "Example of partial-answer handling" in SKILL)
a("023","'never bundle them' in partial example",  "never bundle them"       in partial_ex)
turns = claude_turns(partial_ex)
a("024","Partial example has ≥ 3 Claude turns",    len(turns)>=3,         f"found {len(turns)}")
bundled = any("database" in t.lower() and "deploy" in t.lower() for t in turns)
a("025","No Claude turn bundles database + deploy",not bundled,            f"turns={turns}")

# ════════════════════════════════════════════════════════════
# CATEGORY 4: RETROFIT
# ════════════════════════════════════════════════════════════
a("026","Retrofit workflow section exists",        "Workflow: Existing Project (Retrofit)" in SKILL)
nq = len(re.findall(r'^\d+\.', retrofit, re.MULTILINE))
a("027","Retrofit interview has ≥ 5 numbered Qs",  nq>=5,                 f"found {nq}")
a("028","'[TO VERIFY]' in retrofit",               "[TO VERIFY]"             in retrofit)
a("029","'v0-retrofit' in retrofit",               "v0-retrofit"             in retrofit)
a("030","Retrofit Gap Flagging section exists",    "Retrofit Gap Flagging"   in retrofit)
a("031","'code is the truth' in retrofit",         "code is the truth"       in retrofit)

# ════════════════════════════════════════════════════════════
# CATEGORY 5: TEMPLATE
# ════════════════════════════════════════════════════════════
a("032","'shall' in requirements template",        "shall"                   in req_tmpl)
a("033","'REQ-' in requirements template",         "REQ-"                    in req_tmpl)
a("034","'Out of Scope' in requirements template", "Out of Scope"            in req_tmpl)
a("035","'Open Questions' in design template",     "Open Questions"          in des_tmpl)
a("036","'Verify' in tasks template",              "Verify" in task_tmpl or "verification" in task_tmpl)
a("037","UIB present in templates.md",             "MANDATORY BEFORE ANY ACTION" in uib_tmpl)
a("038","'HARD CONSTRAINTS' in UIB (templates)",   "HARD CONSTRAINTS"        in uib_tmpl)
a("039","'DIVERGENCE PROTOCOL' in UIB (templates)","DIVERGENCE PROTOCOL"     in uib_tmpl)

# ════════════════════════════════════════════════════════════
# CATEGORY 6: ANTIPATTERN
# ════════════════════════════════════════════════════════════
a("040","'just start coding' in Common Mistakes",  "just start coding"       in mistakes.lower())
a("041","'Feature request with no spec context'",  "Feature request with no spec context" in mistakes)
a("042","'Generating config files before spec'",   "Generating config files before spec exists" in mistakes)
a("043","'fabricate' in Common Mistakes",          "fabricate"               in mistakes)
a("044","'Out of scope section missing'",          "Out of scope section missing" in mistakes)

# ════════════════════════════════════════════════════════════
# CATEGORY 7: CONSISTENCY
# ════════════════════════════════════════════════════════════
a("045","UIB section exists in cross-AI file",     "Universal Instruction Block" in CROSS)
a("046","'CLAUDE.md' in cross-AI file",            "CLAUDE.md"               in CROSS)
a("047","'.cursorrules' in cross-AI file",         ".cursorrules"            in CROSS)
a("048","'.windsurfrules' in cross-AI file",       ".windsurfrules"          in CROSS)
a("049","'copilot-instructions.md' in cross-AI",   "copilot-instructions.md" in CROSS)
a("050","'.aider.conf.yml' in cross-AI file",      ".aider.conf.yml"         in CROSS)
a("051","'MANDATORY BEFORE ANY ACTION' in cross-AI","MANDATORY BEFORE ANY ACTION" in CROSS)
core = ["MANDATORY BEFORE ANY ACTION","HARD CONSTRAINTS","DIVERGENCE PROTOCOL"]
missing = [p for p in core if p not in uib_tmpl or p not in uib_cross]
a("052","UIB core consistent across both ref files",not missing,
    f"missing: {missing}" if missing else "all 3 key sections present in both files")

# ════════════════════════════════════════════════════════════
# CATEGORY 8: CONTEXT — CONTEXT.md template and session management
# ════════════════════════════════════════════════════════════

CONTEXT_TMPL = tmpl_section("Template: CONTEXT.md") if "Template: CONTEXT.md" in TMPL else TMPL[TMPL.find("## Template: CONTEXT.md"):]

a("053","CONTEXT.md template present in templates.md",
    "Template: CONTEXT.md" in TMPL)
a("054","CONTEXT.md template has Resume block",
    "Resume from here" in CONTEXT_TMPL or "resume" in CONTEXT_TMPL.lower())
a("055","CONTEXT.md template has Session log section",
    "Session log" in CONTEXT_TMPL)
a("056","CONTEXT.md template has Key decisions section",
    "Key decisions" in CONTEXT_TMPL)
a("057","CONTEXT.md template has Open questions section",
    "Open questions" in CONTEXT_TMPL)
a("058","CONTEXT.md template has Divergences section",
    "Divergences" in CONTEXT_TMPL)
a("059","Session Management section exists in SKILL.md",
    "Session Management" in SKILL)
a("060","SKILL.md mentions CONTEXT.md update rules",
    "CONTEXT.md" in SKILL and "session log" in SKILL.lower())
a("061","UIB step 0 references CONTEXT.md in templates.md",
    "0. If CONTEXT.md" in TMPL or "0. If `CONTEXT.md`" in TMPL)
a("062","UIB step 0 references CONTEXT.md in cross-AI file",
    "0. If CONTEXT.md" in CROSS or "0. If `CONTEXT.md`" in CROSS)
a("063","CLAUDE.md startup order includes CONTEXT.md first",
    open(os.path.join(BASE, "CLAUDE.md"), encoding="utf-8").read().count("CONTEXT.md") >= 2)
a("064","SKILL.md quality checklist includes CONTEXT.md checks",
    "CONTEXT.md" in section(SKILL, "Output Quality Checklist"))



# ════════════════════════════════════════════════════════════
# REPORT
# ════════════════════════════════════════════════════════════
passed = [r for r in results if r[2]]
failed = [r for r in results if not r[2]]
cats = {
    "TRIGGER":     [r for r in results if int(r[0]) <=  9],
    "GATE":        [r for r in results if 10<=int(r[0])<=17],
    "INTERVIEW":   [r for r in results if 18<=int(r[0])<=25],
    "RETROFIT":    [r for r in results if 26<=int(r[0])<=31],
    "TEMPLATE":    [r for r in results if 32<=int(r[0])<=39],
    "ANTIPATTERN": [r for r in results if 40<=int(r[0])<=44],
    "CONSISTENCY": [r for r in results if 45<=int(r[0])<=52],
    "CONTEXT":     [r for r in results if 53<=int(r[0])<=64],
}
print(f"\n{'='*62}")
print(f"  SDD SKILL — PHASE 2A REPORT")
print(f"{'='*62}")
print(f"  Total: {len(results)}   Pass: {len(passed)}   Fail: {len(failed)}")
print(f"{'='*62}\n")
for cat, items in cats.items():
    cp = sum(1 for r in items if r[2])
    print(f"  [{cat}]  {cp}/{len(items)}")
    for id, desc, ok, note in items:
        ns = f"  ({note})" if note else ""
        print(f"    {'✓' if ok else '✗'} {id}: {desc}{ns}")
    print()
if failed:
    print(f"{'='*62}")
    print("  FAILURES")
    print(f"{'='*62}")
    for id,desc,ok,note in failed:
        print(f"\n  ✗ ASSERT-{id}: {desc}")
        if note: print(f"    → {note}")
    sys.exit(1)
else:
    print(f"{'='*62}")
    print("  ALL ASSERTIONS PASSED — Phase 2A complete")
    print(f"{'='*62}\n")
    sys.exit(0)
