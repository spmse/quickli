# Copilot Instructions

## Core Rules

- Use English for all generated documentation and repository-facing content.
- Do not proceed on silent assumptions. If an assumption is required, state it clearly.
- When assumptions exist, provide options, benefits, and risks.
- The user has final decision authority when something is unclear.
- A task is only complete when implementation, tests, documentation, and user acceptance exist.
- Prefer the Python standard library over external dependencies for simple problems.
- Keep code PEP 8 compliant with a maximum line length of 100 characters.
- Keep tests working on Python 3.12, 3.13, and 3.14.
- Never remove tests without informing the user.
- Implement at most one feature in parallel.

## Naming and License

- Use `quickli` as the Python package name, import path, and distribution name.
- Use `quiCkLI` as the stylized project name in prose when appropriate.
- The repository license is MIT.

## Repository Context

- The project is a minimal Python CLI development framework.
- The initial design centers on application, command, argument, option, and plugin concepts.
- Use the `src` layout with package code in `src/quickli`.
- Keep resource specifications in the `specs` directory.
- Keep ADRs in `docs/adr`.

## Documentation Rules

- Keep documentation consistent with the implementation.
- Update documentation for every functional change.
- Use the `docs` directory for user and developer documentation.
- Use the `.github` directory for GitHub-specific automation and AI guidance.
- Keep documentation clear and concise, avoiding unnecessary complexity.
- Documentation should always contain examples when describing usage or behavior.
- Documentation should be written for developers with varying experience levels,
  including beginners.

## Workflow Expectations

- Read the relevant specification before changing a resource area.
- Keep changes focused and aligned with a single approved feature.
- Add or update unit tests for every functional change.
- Update specifications when the technical design changes.
- Record significant design decisions as ADRs when the choice affects future evolution.
- Surface open questions early instead of encoding them silently in code.

## Quality Bar

- Prefer minimal interfaces and standard-library building blocks.
- Avoid speculative abstractions.
- Keep examples executable and accurate.
- Keep repository metadata aligned with the current release decisions.