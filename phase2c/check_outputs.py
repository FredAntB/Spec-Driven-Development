#!/usr/bin/env python3
"""
Phase 2C Assertion Runner — SDD Skill v2.1b
Checks generated file quality across 3 end-to-end flows.
Run AFTER Claude Code has completed all 3 flows.

Usage: python3 phase2c/check_outputs.py
"""

import re, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read(path):
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        return None
    return open(full, encoding="utf-8").read()

results = []
def a(flow, id, desc, passed, note=""):
    results.append((flow, id, desc, passed, note))

def has(text, *phrases):
    return all(p in text for p in phrases)

def req_ids(text):
    return re.findall(r'REQ-\d{3}', text)

def task_req_refs(text):
    """Count tasks that contain at least one REQ-xxx reference."""
    tasks = re.findall(r'- \[[ x~!]\].*', text)
    return sum(1 for t in tasks if re.search(r'REQ-\d{3}', t))

def verify_steps(text):
    return len(re.findall(r'[Vv]erify|[Vv]erification', text))

def placeholder_free(text):
    return '{{' not in text and '}}' not in text

def extract_uib_core(text):
    """
    Extract the Universal Instruction Block body.
    Returns the text between the first pair of border lines (═{10+}).
    Falls back to checking for the key mandate phrases directly.
    """
    m = re.search(r'═{10,}\n(.*?)═{10,}', text, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def uib_present(text):
    return "MANDATORY BEFORE ANY ACTION" in text

def uib_identical(texts):
    """
    Check that the UIB core sections are consistent across multiple files.
    Extracts the three mandatory phrases and checks all are present in each.
    Also checks that the full block (if extractable) is character-for-character
    identical across files that have it.
    """
    phrases = [
        "MANDATORY BEFORE ANY ACTION",
        "HARD CONSTRAINTS",
        "DIVERGENCE PROTOCOL"
    ]
    cores = []
    for text in texts:
        core = extract_uib_core(text)
        if core:
            cores.append(re.sub(r'\s+', ' ', core).strip())

    phrase_check = all(
        all(p in text for p in phrases)
        for text in texts
    )

    if len(cores) < 2:
        return phrase_check, "UIB border lines found in fewer than 2 files — checking phrases only"

    all_match = len(set(cores)) == 1
    return phrase_check and all_match, "" if (phrase_check and all_match) else f"UIB cores differ: {len(set(cores))} unique variants found"

# ════════════════════════════════════════════════════════════
# FLOW A — Greenfield: Freelance Time Tracker
# ════════════════════════════════════════════════════════════

req_a   = read("phase2c/flow_a/requirements.md")
des_a   = read("phase2c/flow_a/design.md")
task_a  = read("phase2c/flow_a/tasks.md")
claude_a= read("phase2c/flow_a/CLAUDE.md")
cursor_a= read("phase2c/flow_a/.cursorrules")

# File existence
a("A","A01","requirements.md exists",  req_a   is not None)
a("A","A02","design.md exists",        des_a   is not None)
a("A","A03","tasks.md exists",         task_a  is not None)
a("A","A04","CLAUDE.md exists",        claude_a is not None)
a("A","A05",".cursorrules exists",     cursor_a is not None)

if req_a:
    reqs = req_ids(req_a)
    a("A","A06","requirements.md uses 'shall' language",         "shall"       in req_a)
    a("A","A07","requirements.md has ≥ 6 REQ-xxx IDs",          len(reqs)>=6, f"found {len(reqs)}: {reqs}")
    a("A","A08","requirements.md has Out of Scope section",      "Out of Scope" in req_a)
    a("A","A09","requirements.md has acceptance criteria",       "Acceptance" in req_a or "acceptance" in req_a)
    a("A","A10","requirements.md has no {{placeholders}}",       placeholder_free(req_a))
    a("A","A11","requirements.md mentions Freelancer as actor",  "Freelancer"  in req_a or "freelancer" in req_a)

if des_a:
    a("A","A12","design.md has Open Questions section",          "Open Questions" in des_a)
    a("A","A13","design.md references REQ IDs in endpoints",     bool(re.search(r'REQ-\d{3}', des_a)))
    a("A","A14","design.md has no {{placeholders}}",             placeholder_free(des_a))
    a("A","A15","design.md mentions TimeEntry data model",       "TimeEntry" in des_a or "time_entry" in des_a or "time entry" in des_a.lower())

if task_a:
    linked = task_req_refs(task_a)
    total_tasks = len(re.findall(r'- \[[ x~!]\]', task_a))
    a("A","A16","tasks.md tasks have REQ references",            linked > 0, f"{linked}/{total_tasks} tasks reference a REQ")
    a("A","A17","tasks.md has Verify steps",                     verify_steps(task_a) >= 3, f"found {verify_steps(task_a)}")
    a("A","A18","tasks.md has no {{placeholders}}",              placeholder_free(task_a))

if claude_a:
    a("A","A19","CLAUDE.md has Universal Instruction Block",     uib_present(claude_a))
    a("A","A20","CLAUDE.md has no {{placeholders}}",             placeholder_free(claude_a))

if cursor_a and claude_a:
    consistent, note = uib_identical([claude_a, cursor_a])
    a("A","A20b","UIB consistent between CLAUDE.md and .cursorrules", consistent, note)

# ════════════════════════════════════════════════════════════
# FLOW B — Retrofit: Invoice Processor
# ════════════════════════════════════════════════════════════

req_b  = read("phase2c/flow_b/requirements.md")
des_b  = read("phase2c/flow_b/design.md")
task_b = read("phase2c/flow_b/tasks.md")

a("B","B01","requirements.md exists",  req_b  is not None)
a("B","B02","design.md exists",        des_b  is not None)
a("B","B03","tasks.md exists",         task_b is not None)

if req_b:
    reqs_b = req_ids(req_b)
    a("B","B04","requirements.md uses 'shall' language",             "shall"          in req_b)
    a("B","B05","requirements.md has ≥ 4 REQ-xxx IDs",              len(reqs_b)>=4,  f"found {len(reqs_b)}")
    a("B","B06","requirements.md has v0-retrofit version marker",    "v0-retrofit"    in req_b)
    a("B","B07","requirements.md has Out of Scope section",          "Out of Scope"   in req_b)
    a("B","B08","requirements.md has Retrofit Assumptions section",  "Assumption"     in req_b or "assumption" in req_b)
    a("B","B09","requirements.md has no {{placeholders}}",           placeholder_free(req_b))
    a("B","B10","requirements.md covers PDF invoice processing",
        "invoice" in req_b.lower() and ("pdf" in req_b.lower() or "PDF" in req_b))

if des_b:
    to_verify_count = des_b.count("[TO VERIFY]")
    a("B","B11","design.md has [TO VERIFY] markers",                 to_verify_count > 0, f"found {to_verify_count}")
    a("B","B12","design.md has Open Questions section",              "Open Questions" in des_b)
    a("B","B13","design.md has no {{placeholders}}",                 placeholder_free(des_b))

if task_b:
    first_phase = task_b[:task_b.find("\n## Phase 2") if "\n## Phase 2" in task_b else len(task_b)]
    has_verification_phase = (
        "spec verification" in task_b.lower() or
        "verify spec"       in task_b.lower() or
        "confirm spec"      in task_b.lower() or
        "validate spec"     in task_b.lower()
    )
    has_no_setup_tasks = not bool(re.search(
        r'set up node|create mongodb|initialize project|install express',
        task_b, re.IGNORECASE))
    a("B","B14","tasks.md Phase 1 is spec verification",             has_verification_phase)
    a("B","B15","tasks.md has no setup tasks for already-done work", has_no_setup_tasks)

# ════════════════════════════════════════════════════════════
# FLOW C — Cross-AI: Engineering Task Board (4 config files)
# ════════════════════════════════════════════════════════════

claude_c = read("phase2c/flow_c/CLAUDE.md")
cursor_c = read("phase2c/flow_c/.cursorrules")
wind_c   = read("phase2c/flow_c/.windsurfrules")
copilot_c= read("phase2c/flow_c/.github/copilot-instructions.md")

a("C","C01","CLAUDE.md exists",                        claude_c  is not None)
a("C","C02",".cursorrules exists",                     cursor_c  is not None)
a("C","C03",".windsurfrules exists",                   wind_c    is not None)
a("C","C04",".github/copilot-instructions.md exists",  copilot_c is not None)

config_files = [f for f in [claude_c, cursor_c, wind_c, copilot_c] if f is not None]

for i, (fname, content) in enumerate(zip(
    ["CLAUDE.md", ".cursorrules", ".windsurfrules", "copilot-instructions.md"],
    [claude_c, cursor_c, wind_c, copilot_c]
)):
    if content is not None:
        a("C", f"C{5+i:02d}", f"{fname} has Universal Instruction Block",
            uib_present(content))
        a("C", f"C{9+i:02d}", f"{fname} has no {{{{placeholders}}}}",
            placeholder_free(content))
        a("C", f"C{13+i:02d}", f"{fname} contains project name",
            "Engineering Task Board" in content or "task board" in content.lower())

if len(config_files) >= 2:
    consistent, note = uib_identical(config_files)
    a("C","C17",
        f"UIB core is consistent across all {len(config_files)} config files",
        consistent, note)

# ════════════════════════════════════════════════════════════
# REPORT
# ════════════════════════════════════════════════════════════

passed = [r for r in results if r[3]]
failed = [r for r in results if not r[3]]

flows = {"A": [], "B": [], "C": []}
for r in results:
    flows[r[0]].append(r)

flow_names = {
    "A": "Greenfield — Freelance Time Tracker",
    "B": "Retrofit — Invoice Processor",
    "C": "Cross-AI — Engineering Task Board",
}

print(f"\n{'='*64}")
print(f"  SDD SKILL — PHASE 2C REPORT")
print(f"{'='*64}")
print(f"  Total: {len(results)}   Pass: {len(passed)}   Fail: {len(failed)}")
print(f"{'='*64}\n")

for flow_key, items in flows.items():
    fp = sum(1 for r in items if r[3])
    print(f"  [FLOW {flow_key}] {flow_names[flow_key]}  {fp}/{len(items)}")
    for flow, id, desc, ok, note in items:
        ns = f"  ({note})" if note else ""
        print(f"    {'✓' if ok else '✗'} {id}: {desc}{ns}")
    print()

if failed:
    print(f"{'='*64}")
    print("  FAILURES — action required before v1.0 release")
    print(f"{'='*64}")
    for flow, id, desc, ok, note in failed:
        print(f"\n  ✗ Flow {flow} — {id}: {desc}")
        if note:
            print(f"    → {note}")
    sys.exit(1)
else:
    print(f"{'='*64}")
    print("  ALL ASSERTIONS PASSED — generation quality validated")
    print(f"{'='*64}\n")
    sys.exit(0)
