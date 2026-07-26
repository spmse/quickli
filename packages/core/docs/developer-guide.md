# Developer Guide

## Project Layout

- `src/quickli`: package source code.
- `tests`: unit tests.
- `specs`: technical resource specifications.
- `docs`: user and maintainer documentation.
- `examples`: runnable example applications with matching guides.
- `examples/simple`: focused single-purpose examples.
- `examples/complex`: larger multi-command examples.
- `.github`: GitHub-specific automation and AI guidance.

## Development Rules

- Keep project-facing documentation in English.
- Prefer the Python standard library over external dependencies for simple problems.
- Keep generated code functional and covered by dedicated unit tests.
- Keep line length at or below 100 characters.
- Work on one feature at a time.

## Current API Shape

- `Application` supports both commandless entrypoints and named commands.
- `Argument` and `Option` support conversion and validation.
- Global options may be parsed before or after the command name.
- Help text may come from explicit `help_text` values or handler docstrings.

## Local Workflow

```bash
python -m ruff check .
python -m ruff format --check .
PYTHONPATH=src python -m unittest discover -s tests -v
python -m build --sdist --wheel
```

Run examples manually when changing user-facing CLI behavior.

```bash
PYTHONPATH=src python examples/simple/quickhead/app.py AGENTS.md -n 5
PYTHONPATH=src python examples/simple/ls-cli/quickls.py . --suffix .md
PYTHONPATH=src python examples/complex/pyk5l/app.py get-pods --verbose
```

## Open Decisions

- Plugin and option APIs should be designed from a written proposal before implementation.

## Naming and License

- Use `quickli` for the Python package, imports, and distribution metadata.
- Use `quiCkLI` as the stylized project name in prose when that improves readability.
- The repository is licensed under the MIT License.

## Documentation Maintenance

- Update `README.md` when the public feature set changes.
- Update `docs/usage.md` when the API shape or examples change.
- Update `docs/validation.md` when built-in validators or validation behavior change.
- Update `docs/github-publishing-guide.md` when release automation changes.
- Update the relevant file in `specs/` when behavior changes.
- Add or update an ADR in `docs/adr` when a significant design decision affects future evolution.
- Keep example READMEs aligned with the runnable code in the same folder.
