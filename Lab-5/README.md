# Lab 5 — Static Code Analysis

**Name:** AMOGH SHARMA  **SRN:** PES1UG24CS053
**Assigned repo:** [SETAPESU26/L5_51_parking_lot_system](https://github.com/SETAPESU26/L5_51_parking_lot_system)

Pylint, Bandit and Flake8 were run on `parking_lot_system.py`, an automated parking lot and slot manager. Every issue they reported was fixed, plus a few logic problems the tools don't catch.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.10 / 10 | **10.00 / 10** |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | **0** |
| Flake8 | 10 issues | **0** |

## Contents

| Path | What it is |
|------|------------|
| `Code/parking_lot_system.py` | Cleaned script (the original is in the first Lab 5 commit) |
| `Reports/Before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` for the original script |
| `Reports/After/` | The same three reports for the fixed script (an empty `flake8_report.txt` means no issues) |
| `issues.md` | Issue table: issue, type, line(s), description, fix approach |
| `reflection.md` | Answers to the four reflection questions |
| `Documentation/PES1UG24CS053_Lab5_Report.pdf` | Full lab report (setup, results, issue table, reflection) |

## Commits

1. `Lab 5: add assigned parking_lot_system.py and baseline Pylint/Bandit/Flake8 reports`
2. `Lab 5: fix Bandit security issues (eval, MD5, random PIN, os.system, try/except/pass, hardcoded key)`
3. `Lab 5: fix Flake8 issues (unused import/variable, long lines, None comparison, final newline)`
4. `Lab 5: fix Pylint issues (10.00/10) and add issue table, reflection and report`

## Run it

```bash
pip install pylint bandit flake8
cd Lab-5/Code
python parking_lot_system.py
pylint parking_lot_system.py
bandit -r parking_lot_system.py
flake8 parking_lot_system.py
```

The barrier key is no longer stored in the source. Set the `GATE_BARRIER_KEY` environment variable if you want the script to report it as configured.
