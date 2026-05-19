# Phase 2C Kickoff

Paste the following into the Code tab to start the evaluation:

---

Read SKILL.md, references/templates.md, and references/capabilities-and-cross-ai.md
in full, then run the Phase 2C end-to-end flow evaluation exactly as defined in
phase2c/eval_flows.md.

Follow the execution protocol precisely:
- Create all output directories before starting:
  phase2c/flow_a/, phase2c/flow_b/, phase2c/flow_c/, phase2c/flow_c/.github/
- Run all 3 flows in sequence (A → B → C)
- Write every generated file to disk using the Write tool — no truncation
- After each flow, read one of its generated files back to confirm it exists
- After all flows complete, run the checker (see platform note below)
- Write the full report to phase2c/eval_report_2c.md using the Write tool
- After writing, read phase2c/eval_report_2c.md back and confirm it exists and is complete
- If the file is missing or truncated, write it again before continuing
- Print the one-line summary to chat when done

---

## Platform note — running check_outputs.py on Windows

The spec files contain UTF-8 box-drawing characters (═) that Windows'
default cp1252 codec rejects. Run the checker with:

  PYTHONUTF8=1 python phase2c/check_outputs.py

If `python` is not on PATH (Microsoft Store alias only), use the full path:

  PYTHONUTF8=1 "<AppData>\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_...\python3.12.exe" phase2c/check_outputs.py

On macOS/Linux the standard invocation works without the flag:

  python3 phase2c/check_outputs.py
