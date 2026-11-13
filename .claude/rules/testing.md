---
paths:
  - "tests/**/*.py"
  - "tests/**/*.json"
---

# Structure

- All tests should follow given-when-then pattern. divide them on sections where each starts with comment `#given`, `#when`, `#then`. Each section should contain only code related to that section. Avoid mixing code from different sections.

- In assert statements, the RHS is the expected value
- The only allowed comments are `# given`, `# when` and `# then`.
- Prefer pytest fixtures for setup and teardown. Avoid setup and teardown methods in test classes.
- Mark tests with the markers registered in `pyproject.toml`.
- In new test files, import the tested module as `from <path.to> import <module> as _<module>`.

# Stubs & Mocks
- Use pytest and pytest-mock. For mocking use `MockFixture`, and prefer `mocker.patch.object`.

# Parameters
- For multiple cases prefer parametrized tests, with `expected` as the final parameter.
