# Lab 6 — Code and Branch Coverage Analysis

**Name:** AMOGH SHARMA  **SRN:** PES1UG24CS053
**Assigned repo:** [SETAPESU26/L6_L7_51_self_storage](https://github.com/SETAPESU26/L6_L7_51_self_storage) — `self_storage.py`, which works out storage rent by unit size, months, climate control and membership, checks access rules and reports payment status.

The starter test file covered 32% of the code (38% with branches). Two new test files were added: one for line coverage and one for branch coverage.

| Run | Test file | Tests | Line coverage | Branch coverage |
|-----|-----------|-------|---------------|-----------------|
| Starter | `test_self_storage.py` | 2 | 32% | 6 branches partly covered (38% combined) |
| Code coverage | `CodeCoverageTest_self_storage.py` | 14 | **92%** (3 lines missed: 22, 40, 45) | 90% combined, 3 branches partly covered |
| Branch coverage | `BranchCoverageTest_self_storage.py` | 42 | **100%** | **100%** (26/26 branches) |

## Contents

| Path | What it is |
|------|------------|
| `self_storage.py` | Module under test, unchanged |
| `test_self_storage.py` | Original starter tests, unchanged |
| `CodeCoverageTest_self_storage.py` | Tests that reach at least 90% line coverage |
| `BranchCoverageTest_self_storage.py` | Tests that drive every `if` / `elif` to both outcomes, including each side of `is_member and unit_size != "large"` and the boundaries (`months` 0, `extra` 6 vs 7, `hour` 5/6/22/23, visitors 2/3/4/5, and every payment cutoff) |
| `Screenshots/code_coverage.png` | Terminal output for the code coverage run |
| `Screenshots/branch_coverage.png` | Terminal output for the branch coverage run |

## Run it

```bash
pip install coverage pytest
cd Lab-6

# code (line) coverage
coverage run -m pytest CodeCoverageTest_self_storage.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_self_storage.py
coverage report -m
```

## Commits

1. `Lab 6: add code coverage tests (92% line coverage)`
2. `Lab 6: add branch coverage tests (100% branch coverage) and README`
