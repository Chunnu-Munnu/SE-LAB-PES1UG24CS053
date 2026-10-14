# Lab 5 — Reflection

**Name:** AMOGH SHARMA  **SRN:** PES1UG24CS053
**File analysed:** `parking_lot_system.py` (L5_51 Parking Lot System)

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the Flake8 style issues: the unused `math` import, `== None` → `is None`, the missing final newline and the long lines. Each one points at an exact line and the fix is mechanical, with no effect on behaviour. Swapping MD5 for SHA-256 and `random.randint` for `secrets.randbelow` was just as quick.

The hardest was the `eval()` in `calculateParkingFee`. Deleting it was not enough, because the caller was passing a whole expression (`"base_rate * 1.50"`) as a string. I had to change the function's contract to accept a numeric surge multiplier and update the call site, while making sure the fee for P03 still came out as 45.0. Removing the `global` statement and the mutable default argument also took some thought, since both change how state moves through the program: the log list is now passed in from `main()` and the running total lives in a `ledger` dict. The hardcoded barrier key was tricky in a different way. Bandit did not report it at all, so I only found it by reading the code and the output.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Mostly the findings were real, but a few were debatable:

- **Pylint C0103 on `total_collections`** asked for an UPPER_CASE name because it is a module-level variable. It is not a constant, though; it is a running total that changes every time a car parks. Renaming it to `TOTAL_COLLECTIONS` would have silenced the warning and made the code more misleading. The real problem was the global mutable state, so I moved the total into a `ledger` dict instead of just renaming it.
- **Bandit B324 (MD5)** could be a false positive in a different program. If the hash were only used as a non-secret lookup key, `hashlib.md5(..., usedforsecurity=False)` would be acceptable. Here the plate hash is used as a fingerprint, so switching to SHA-256 was the safer choice.

I also saw the opposite problem: Bandit **missed** the hardcoded `BARRIER_GATE_SECRET_TOKEN_2026` because its B105 check matches variable names like `password` or `token`, and this one was called `gate_barrier_key`. A clean tool report doesn't mean the code is secure.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** a `pre-commit` hook that runs Flake8 and Bandit on staged files, plus editor integration (VS Code's Pylint/Flake8 extensions) so problems show up while typing instead of after the fact.
- **In CI:** a GitHub Actions job on every push and pull request that runs `pylint --fail-under=9.5`, `flake8` and `bandit -r . -ll` (fail on medium and high). A PR can't be merged while this check is red.
- **Shared config:** keep the rules in `setup.cfg` / `pyproject.toml` / `.bandit` in the repo so everyone runs the same checks, and only suppress a warning with an inline `# nosec` or `# pylint: disable=` plus a comment explaining why.
- **Gradual adoption on old code:** run the tools in report-only mode first, fix high-severity security findings immediately, then raise the Pylint threshold over time.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** the five Bandit findings (2 High, 1 Medium, 2 Low) went to zero. There is no more `eval`, no shell call built from a filename, no weak hash or predictable PIN, and the barrier key is no longer stored in source or printed.
- **Correctness:** the shared-list bug from `entry_logs=[]` is gone, unknown slots are reported instead of silently ignored, zero or negative bookings are rejected, and the manifest file is always closed. The output is also in the right order now; before, the `os.system` line printed first.
- **Readability:** Pylint went from **4.10/10 to 10.00/10**. Every function has a docstring and a snake_case name, `check_slot_availability` is two lines instead of six, and `get_available_summary` is a single `sum(...)`.
- **Maintainability:** the module can be imported without side effects thanks to the `__main__` guard, so the functions can be reused or unit-tested. Flake8 reports nothing, so future diffs won't be cluttered with style noise.
