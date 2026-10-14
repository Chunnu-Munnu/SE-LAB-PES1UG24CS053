# Lab 5 — Issue Table (`parking_lot_system.py`)

**Name:** AMOGH SHARMA  **SRN:** PES1UG24CS053
**Assigned repo:** [SETAPESU26/L5_51_parking_lot_system](https://github.com/SETAPESU26/L5_51_parking_lot_system)

Line numbers refer to the **original** file (see `Reports/Before/`). High and medium severity issues are listed first.

## Score summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.10 / 10 (36 messages) | **10.00 / 10** (0 messages) |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 10 issues | **0 issues** |

## Issues found and fixed

| # | Issue | Tool / Code | Severity | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|----------|------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B605 | High | Security | 64 | `os.system("echo ... " + filename)` runs a shell with the filename pasted in, so a name like `x.txt & del *` would run extra commands. | Removed the shell call and print the message with `print()`. |
| 2 | Weak MD5 hash | Bandit B324 | High | Security | 53 | MD5 is broken for collision resistance and should not be used to fingerprint plates. | Switched to `hashlib.sha256`. |
| 3 | Hardcoded secret printed to console | Manual review (CWE-798) | High | Security | 76, 85 | `gate_barrier_key = "BARRIER_GATE_SECRET_TOKEN_2026"` is committed in source and printed in plain text on every run. Bandit misses it because the variable name doesn't match its password regex. | Read the key from the `GATE_BARRIER_KEY` environment variable and only print whether it is configured. |
| 4 | Use of `eval()` | Bandit B307, Pylint W0123 | Medium | Security | 46–49 | `calculateParkingFee` evaluates a caller-supplied string, which allows arbitrary code execution. | Function now takes a numeric `surge_multiplier` and computes `rate * float(surge_multiplier)`. |
| 5 | Mutable default argument | Pylint W0102 | Medium | Bug | 15 | `entry_logs=[]` is created once and shared across every call, so logs leak between calls. | Default changed to `None`; a new list is created inside the function. |
| 6 | Try / except / pass with bare `except` | Bandit B110, Pylint W0702, Flake8 E722 | Low (Bandit) | Bug | 28–33 | `releaseSlot` silently swallows every exception (even typos), and the caller can't tell whether the release worked. | Look the slot up explicitly, print a message and return `False` for unknown slots, `True` on success. |
| 7 | Insecure random for ticket PIN | Bandit B311 | Low | Security | 57 | `random.randint` is a predictable PRNG; ticket PINs could be guessed. | Use `secrets.randbelow(9000) + 1000`. |
| 8 | `global` statement | Pylint W0603 | Warning | Design | 16 | `parkVehicle` rebinds the module-level `total_collections` through `global`. | Keep the running total in a module-level `ledger` dict that the function updates. |
| 9 | File opened without `with` / encoding | Pylint R1732, W1514 | Warning | Resource leak | 61–63 | The file handle is not closed if `write()` fails, and the encoding depends on the OS locale. | `with open(filename, "w", encoding="utf-8") as manifest:` |
| 10 | Parameter shadows a global | Pylint W0621 | Warning | Bug risk | 67 | `getAvailableSummary(parking_slots)` hides the module-level `parking_slots`. | Parameter renamed to `slots`. |
| 11 | Unused variables | Pylint W0612, Flake8 F841 | Warning | Code smell | 37, 47, 69 | `overtime_fee`, `base_rate` (only used inside the `eval` string) and loop variable `s` are never used. | Removed them; the loop iterates `slots.values()`. |
| 12 | Unused import | Pylint W0611, Flake8 F401 | Warning | Code smell | 4 | `math` is imported but never used. | Removed the import (`random` was also dropped when the PIN moved to `secrets`). |
| 13 | Comparison to `None` with `==` | Flake8 E711, Pylint C0121 | Convention | Style | 38 | `parking_slots.get(slot_id) == None` | `is None` |
| 14 | Simplifiable if / unnecessary else | Pylint R1703, R1705 | Refactor | Style | 40–43 | `if x: return True else: return False` | `return not slot["is_occupied"]` |
| 15 | Lines too long | Flake8 E501, Pylint C0301 | Convention | Style | 7, 8, 9, 23 | Lines of 82–131 characters (limit 79 for Flake8). | Wrapped the dict entries and the log message. |
| 16 | `%` string formatting | Pylint C0209 | Convention | Style | 23 | Old-style `%` formatting. | f-string. |
| 17 | camelCase function names | Pylint C0103 | Convention | Style | 15, 27, 36, 46, 52, 56, 60, 67 | `parkVehicle`, `releaseSlot`, … break PEP 8 naming. | Renamed to `park_vehicle`, `release_slot`, `check_slot_availability`, `calculate_parking_fee`, `generate_vehicle_hash`, `generate_ticket_pin`, `export_parking_manifest`, `get_available_summary`. |
| 18 | Constant naming | Pylint C0103 | Convention | Style | 12 | `total_collections` treated as a constant but mutated. | Replaced by the `ledger` dict (see #8). |
| 19 | Missing docstrings | Pylint C0114, C0116 | Convention | Documentation | 1, 15, 27, 36, 46, 52, 56, 60, 67, 75 | No module or function docstrings. | Added a module docstring and one per function. |
| 20 | Missing final newline | Flake8 W292, Pylint C0304 | Convention | Style | 88 | File ends without `\n`. | Added the newline. |

## Problems the tools did not flag

The assignment README warns that some problems only show up in the output. These were found by running the script and reading the code:

| # | Problem | Line(s) | What was wrong | Fix |
|---|---------|---------|----------------|-----|
| A | Output printed out of order | 64 | The `os.system` subprocess writes straight to the console while Python's own `print` output is still buffered, so "Parking manifest exported…" appeared as the **first** line of output. | Fixed by #1: the message now goes through `print()` and appears in order. |
| B | Secret token shown in output | 85 | `Barrier Key active: BARRIER_GATE_SECRET_TOKEN_2026` was printed on every run. | Fixed by #3. |
| C | Log line never shows the charge | 23 | The entry log said "with total charge calculated" but never included the amount, and `%d` would truncate fractional hours. | Log now reads e.g. `... for 3 hour(s), charge Rs 60.00`. |
| D | Zero or negative bookings accepted | 15–24 | `parkVehicle("P02", "X", -2)` succeeded and reduced `total_collections`. | `park_vehicle` rejects `hours_booked <= 0`. |
| E | Script runs on import | 88 | `main()` was called at module level, so importing the module ran the demo and wrote a file. | Wrapped in `if __name__ == "__main__":`. |
