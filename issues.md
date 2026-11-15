# Lab 5 – Issues found in `gym_system.py`

Student: Aarti Panchal (PES2UG24AM005) · Tools: Pylint, Bandit, Flake8
Scores: Pylint **6.60 → 10.00**, Bandit **1 High → 0**, Flake8 **10 → 0**
Reports: `before/` and `after/` folders.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| OS command injection (Bandit B605, **High**) | Security | 36 | `os.system("rm -f " + prefix + "*.json")` builds a shell command from a parameter; a prefix like `x; rm -rf ~` would execute arbitrary commands. | Removed the shell: use `glob.glob(prefix + "*.json")` and `os.remove()` on each match. (Commit 1) |
| Off-by-one capacity check | Bug (logic) | 11 | `len(roster) > capacity` lets one extra person in: Yoga (3 seats) held 4 members. Not flagged by any tool. | Changed to `>=`. Yoga now stops at 3 and HIIT at 2. |
| Mutable default argument (Pylint W0102) | Bug | 8 | `attendance_log=[]` is created once and shared by every call, so logs from unrelated calls pile up. | Default to `None`, create a fresh list inside the function. |
| Bare `except` (Flake8 E722 / Pylint W0702) | Bad practice | 21 | Swallows every error, including `KeyboardInterrupt` and real bugs, and hides the cause. | Catch only `(KeyError, ValueError)` (unknown class / member not booked). (Commit 2) |
| File handle never closed (Pylint R1732, W1514) | Resource leak | 32 | `open()` without `with` or `encoding`; if `json.dump` fails the file stays open and may not be flushed. | `with open(file, "w", encoding="utf-8") as handle:` |
| Negative capacity accepted | Bug (validation) | 49 | `set_capacity("Spin", -2)` is accepted silently, producing a class that can never be booked. | `set_capacity` raises `ValueError` for negative seats; `main` handles it. |
| Unvalidated user input | Bug / robustness | 52–53 | `int(n)` crashes with `ValueError` on `abc`, and a negative number silently books nobody. | New `read_guest_count()` validates input and falls back to the default of 1. |
| Mixed-type member IDs | Bug (data) | 47 | Member `55` is an int while others are strings like `"M1"`; rosters end up with mixed types. | Demo now uses `"55"`; IDs consistently strings. |
| Unconfigured class gets booked | Bug (logic) | 11, 48 | `Pilates` has no capacity (default 0) but `>` let one member in. Also an empty roster was created for rejected bookings. | `>=` rejects it; roster is only stored after a successful booking. |
| PEP 8 blank lines (Flake8 E302 ×9, E305) | Style | 8–58 | Two blank lines are required around top-level defs. | Added blank lines. (Commit 2) |
| `main()` runs on import | Design | 58 | Importing the module executes the whole demo and prompts for input. | Added `if __name__ == "__main__":` guard. |
| Naming `addMembers` (Pylint C0103) | Style | 27 | camelCase breaks snake_case convention. | Renamed `add_members`. |
| Missing docstrings (C0114, C0116 ×9) | Style | all | No module or function documentation. | Added docstrings. |
| f-string, `.items()` (C0209, C0206) | Style | 15, 39 | Old `%` formatting; dict indexed in a loop. | `f"{member_id} -> {class_name}"`; iterate `rosters.items()`. |
