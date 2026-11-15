# Lab 5 – Reflection

**1. Which issues were the easiest and hardest to fix?**
Easiest were Flake8's formatting findings (blank lines) and Pylint's docstring/naming warnings, which are mechanical. The hardest was the security finding, because `os.system` had to be replaced with a different mechanism (`glob` + `os.remove`) while keeping the same behaviour. The off-by-one capacity bug was also tricky because no tool reported it. I only found it by running the program and noticing Yoga held 4 members with a limit of 3.

**2. Did the tools report any false positives, or miss anything?**
I saw no real false positives. Pylint's docstring warnings feel pedantic on a tiny script, but they are legitimate. The tools missed the logic bugs: the `>` vs `>=` check, negative capacity, mixed-type member IDs and the crash on non-numeric input. Static analysis finds patterns, not intent, so it cannot replace running the code and testing it.

**3. How would you integrate static analysis into a real workflow?**
Run Flake8 and Pylint in a pre-commit hook so style problems never reach the repo, and run all three tools in CI (for example GitHub Actions) on every pull request, failing the build on any Bandit High finding or a Pylint score below a set threshold. Bandit especially should be a hard gate, because security issues are costly to find later.

**4. What tangible improvements did you see?**
Pylint went from 6.60 to 10.00, Bandit from 1 High to 0 issues, and Flake8 from 10 findings to 0. The code is safer (no shell injection, no leaked file handles), more correct (capacity limits now respected, input validated), more readable (docstrings, snake_case, f-strings) and importable without side effects thanks to the `__main__` guard.
