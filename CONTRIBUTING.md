# Contributing

## Goals

quickli is intentionally small, educational, and dependency-light. Contributions should
keep that direction intact.

## Before You Start

- Read [README.md](README.md) for the current scope.
- Read the relevant specification in [`packages/core/specs/`](packages/core/specs).
- Read the [developer guide](packages/core/docs/developer-guide.md) for workflow rules.
- Review [ADRs](packages/core/docs/adr) when changing long-lived design decisions.

## Local Setup

```bash
cd packages/core
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Quality Checks

Run these checks from `packages/core` before opening a pull request.

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m build --sdist --wheel
```

Ruff checks Python source and stub files (`.py` and `.pyi`), including tests and executable
examples. Markdown documentation and its code blocks are not formatting inputs; for example,
`packages/core/README.md` is excluded from `python -m ruff format --check .`.

For documentation changes, use Node.js 24 and the pinned pnpm version. Run from the
repository root:

```bash
corepack pnpm install --frozen-lockfile
corepack pnpm --filter quickli-docs typecheck
corepack pnpm --filter quickli-docs build
```

## Contribution Rules

- Keep repository-facing content in English.
- Prefer the Python standard library over new dependencies for simple problems.
- Keep code compatible with Python 3.12, 3.13, and 3.14.
- Add or update tests for functional changes.
- Update documentation together with code changes.
- Surface assumptions explicitly instead of encoding them silently.
- Keep pull requests focused on one feature or fix at a time.

## Documentation Expectations

- Update [README.md](README.md) when the public feature set changes.
- Update `packages/core/docs/` and `packages/quickli-docs/docs/` when user-facing behavior changes.
- Update the relevant file in `packages/core/specs/` when the technical contract changes.
- Add or update an ADR when the change affects future evolution.

## Pull Requests

When opening a pull request, include:

- what changed
- why it changed
- how it was validated
- any open risks or follow-up items

## Releases

Release Please groups the independently versioned core library and documentation site into
one release pull request. Merging it creates draft component releases. The release workflow
then builds evidence, publishes the core distributions to PyPI when a core tag exists, publishes
the corresponding GitHub releases, and deploys documentation to GitHub Pages.
Track release-specific approval gates, validation evidence, and follow-up work in the release PR.

Use `feat(docs):` for new documentation content and `fix(docs):` for documentation corrections.
Release Please does not treat the bare `docs:` conventional-commit type as a release-triggering
change, so using it alone will not create a documentation release.

Maintain package-specific release notes in [packages/core/CHANGELOG.md](packages/core/CHANGELOG.md)
and [packages/quickli-docs/CHANGELOG.md](packages/quickli-docs/CHANGELOG.md).
