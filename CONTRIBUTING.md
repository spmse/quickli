# Contributing

## Goals

quickli is intentionally small, educational, and dependency-light. Contributions should
keep that direction intact.

## Before You Start

- Read [README.md](README.md) for the current scope.
- Read the relevant specification in `specs/` before changing a resource area.
- Read [docs/developer-guide.md](docs/developer-guide.md) for repository workflow rules.
- Review existing ADRs in `docs/adr/` when changing long-lived design decisions.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Quality Checks

Run these checks before opening a pull request.

```bash
python -m ruff check .
python -m ruff format --check .
PYTHONPATH=src python -m unittest discover -s tests -v
python -m build --sdist --wheel
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
- Update `docs/` pages when user-facing behavior changes.
- Update the relevant file in `specs/` when the technical contract changes.
- Add or update an ADR when the change affects future evolution.

## Pull Requests

When opening a pull request, include:

- what changed
- why it changed
- how it was validated
- any open risks or follow-up items

## Releases

Releases are created from Git tags. See [docs/github-publishing-guide.md](docs/github-publishing-guide.md)
for the maintainer workflow.