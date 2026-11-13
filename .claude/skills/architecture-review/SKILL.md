---
name: architecture-review
description: Review a module, package or branch for design problems such as layering, coupling, security boundaries and efficiency. Use when asked for an architecture or design review, or before changing architectural boundaries.
argument-hint: "[path or branch]"
metadata:
  author: Ziverael
  version: 2.0
---

Review only. Do not edit code unless asked.

## Scope
Review `$ARGUMENTS`. If empty, review `git diff main...HEAD`. Read the changed code and its direct callers.

## Standards
Read `.claude/rules/python-development.md` and the "Architecture" section of the project's `CLAUDE.md`. Hold the code to both. If `CLAUDE.md` has no Architecture section, say so and review against the layering the code itself shows.

## Checks
1. **Layers:** dependencies flow only in the direction `CLAUDE.md` defines. Flag imports that point the wrong way, and business logic in the outermost layer (UI, views, CLI).
2. **Coupling:** prefer dependency injection when it improves testability, modularity or separation of responsibilities. Avoid unnecessary abstractions and DI frameworks. Keep function signatures focused and readable. When several parameters form one concept, consider a dataclass or Pydantic model, but not just to reduce argument count.
3. **Security:** for every trust boundary `CLAUDE.md` names, and any other place where outside data enters (files, network, user input), check who can reach it, input validation, resource limits, and that secrets do not leak into outputs.
4. **Efficiency:** blocking work on a thread or loop that must stay responsive, unbounded reads or result sets, repeated work inside loops that could be done once.
5. **Persistence:** changes to stored or exchanged data follow the versioning or migration policy in `CLAUDE.md`, and older data stays readable or is rejected with a clear error.
6. **Object-oriented code:** follow SOLID where classes are used.

## Report
List findings most severe first, each with `file:line`, the problem, what goes wrong concretely, and the smallest fix.
- Verify each finding in the code. If there are no real problems, say so.
- Skip what the project's linters and type checker already catch.
- If a fix changes architectural boundaries, give alternatives and trade-offs, and wait for approval (see `.claude/rules/engineering.md`).
