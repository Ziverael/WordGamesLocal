# Engineering conventions

## Role

- Start with the simplest architecture that satisfies the requirements. Consider established design patterns when they solve an identifiable problem. Avoid introducing abstractions, patterns, or layers without a concrete justification.

## Rules

- Avoid workarounds. When it is possible, follow enterprise standards. Also think about code efficiency and the security of the solution.
- Before implementing a change that introduces or significantly modifies architectural boundaries, design patterns, persistence strategies, or external integrations, present the proposed approach, alternatives, trade-offs, and risks. Wait for approval before proceeding.
- Project facts (stack, commands, layout, architecture, trust boundaries) are in the project's `CLAUDE.md`. Read them from there; do not assume them.
