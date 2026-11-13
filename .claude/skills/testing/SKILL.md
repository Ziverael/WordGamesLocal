---
name: testing
description: Write, run and debug Python tests in this repo. Use when adding or changing tests, choosing a test level, or investigating pytest failures.
metadata:
  author: Ziverael
  version: 2.0
---

# Testing workflow

Test code conventions are in `.claude/rules/testing.md`. Read it before creating a test file. Commands, layout and project-specific testing notes are in the project's `CLAUDE.md`.

## 1. Choose test levels
Start at the lowest level that can prove the behaviour. Add a higher level only when the change crosses that boundary, and pass each level before starting the next.

| Change | Level | Marker |
|---|---|---|
| Atomic function | unit | `atomic` |
| `<domain>/controller.py` | unit with mocked external systems (filesystem, network, database) and mocked atomic functions, then component. Test that the atomic functions are called with the expected parameters and that their return values are handled properly | `controller` |
| User journey | e2e | `slow` |

- `unit/`: no external systems. Mock at the boundary and test one function or class.
- `component/`: real external systems of the project's test environment, but in isolation.
- `integration/`: real external systems of the project's test environment, without isolation.
- `e2e/`: the whole running system. If it is not set up, adding an e2e framework or driver needs approval first. Slow is acceptable. Flaky is a bug to fix, not to hide with retries or sleeps.

## 2. Reuse existing setup
Check `tests/conftest.py` and the level's `conftest.py` before adding a fixture. Prefer the fixtures and factories named in the "Testing notes" of `CLAUDE.md`.

## 3. Create cases
Create test for default case - especially if the function contains default arguments. Create most common case. Create edge cases, e.g. boundary conditions, empty input, first run case, error handling. Create malicious case, e.g. invalid argument types, tries of overflow or code injection. Create regression case, e.g. a test that reproduces a bug that was fixed.

## 4. Run
Use the test command from the "Commands" section of `CLAUDE.md`, in the environment it names. Run the targeted tests first, then the whole suite.

## 5. Done when
- A bug fix has a test that fails before the fix and passes after it.
- The targeted tests pass, then the full test and lint + check commands from `CLAUDE.md` pass.
- Never weaken, skip or delete a failing test to get a pass. Report it instead.
