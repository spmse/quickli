# Agent Workflow

## Mission

Develop this repository as `quickli`, a minimal, educational, and extensible Python CLI
framework. Use `quickli` for code, imports, and packaging. Use `quiCkLI` as the stylized
project name in human-facing text where appropriate.

## Non-Negotiable Rules

- Use English for all repository-facing code comments, documentation, specifications, ADRs,
	and automation files.
- Do not proceed on silent assumptions.
- When an assumption is unavoidable, state it explicitly and include options, benefits, and
	risks.
- The user has final decision authority whenever something is unclear.
- Keep code PEP 8 compliant with a maximum line length of 100 characters.
- Prefer the Python standard library over external dependencies for simple problems.
- Keep tests compatible with Python 3.12, 3.13, and 3.14.
- Never remove tests without informing the user.
- Implement at most one feature in parallel.
- A task is complete only when implementation, tests, documentation, and user acceptance
	exist.

## Repository Facts

- License: MIT.
- Package and distribution name: `quickli`.
- Package source layout: `src/quickli`.
- Technical specifications live in `specs`.
- User and developer documentation live in `docs`.
- GitHub-specific automation and AI guidance live in `.github`.
- ADRs live in `docs/adr`.

## Required Working Style

- Read the relevant specification files before changing a resource area.
- Surface assumptions with options, potential value, and risks.
- Ask for user input instead of guessing when decisions are still open.
- Keep changes focused and implement only one feature at a time.
- Add or update unit tests for every functional change.
- Keep documentation consistent with the implementation.
- Prefer standard library solutions unless an external dependency is clearly justified.

## Delivery Checklist

- Implementation matches the approved scope.
- Unit tests cover the new or changed behavior.
- Existing tests remain intact unless the user explicitly approves a change.
- Documentation and specifications reflect the current behavior.
- Decisions, assumptions, and open questions are visible to the user.

## Definition of Done

- Functionality is implemented.
- Unit tests cover the behavior.
- Documentation is updated.
- Relevant specifications and ADR references are updated when design decisions change.
- The user has reviewed and accepted the result.

## Agents

All agents are expected to understand the current specifications, documentation, and
project rules before proposing or implementing changes.

Different agents may take the lead on different tasks based on the work required, but the
result must remain cohesive, minimal, educational, and accessible to developers with
different experience levels.

### Architect Agent

The architect agent owns high-level design decisions, project structure, and consistency
between implementation and specifications.

Responsibilities:
- define and refine core abstractions
- maintain technical specifications and ADRs
- keep complexity aligned with the project's educational goals

### Developer Agent

The developer agent implements approved functionality, writes or updates unit tests, and
keeps the codebase aligned with the specifications.

Responsibilities:
- implement the approved feature scope
- write or update unit tests
- update documentation alongside code changes
- prefer standard-library solutions unless a dependency is clearly justified

## QA Agent

The QA agent reviews changes for consistency, clarity, behavior, maintainability, and
alignment with the project's philosophy.

Responsibilities:
- identify behavioral regressions and edge cases
- check test coverage quality
- review documentation for consistency and clarity
- verify that accepted decisions are implemented faithfully

## User Agent

The user agent evaluates changes from a developer experience perspective, especially for
beginners and users who value low complexity.

Responsibilities:
- check whether examples and explanations are accessible
- highlight friction in the public API
- suggest future improvements without expanding the approved scope silently

## Collaboration

Agents collaborate by making design reasoning explicit, keeping the scope narrow, and
handing off work only when the current state is understandable and documented.

Expected collaboration pattern:
- read the relevant spec before editing a resource area
- confirm the user decision when a choice is open
- implement one feature at a time
- update tests and documentation in the same iteration
- surface risks instead of hiding them

### ADRs

Architectural Decision Records document significant design choices, their rationale, the
options considered, and their consequences.

ADR rules:
- store ADRs in `docs/adr`
- write them in clear English
- include context, decision, options, and consequences
- create one ADR per significant design decision
- reference ADRs from documentation or specifications where useful