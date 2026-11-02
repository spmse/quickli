# Developer Guide

## Project Layout

- `src/quickli`: package source code.
- `tests`: unit tests.
- `specs`: technical resource specifications.
- `docs`: user and maintainer documentation.
- `examples`: runnable example applications with matching guides.
- `examples/simple`: focused single-purpose examples.
- `examples/complex`: larger multi-command examples.
- Repository-root `.github`: GitHub-specific automation and AI guidance.

The paths above, except `.github`, are relative to `packages/core`. The official
Docusaurus documentation lives in `packages/quickli-docs`.

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
- `Application` handles `--help`/`-h` before user callbacks. For example,
  `app.run(["deploy", "--help"])` returns help without required-input validation.
- `quickli.parsers` provides explicit JSON, YAML, and TOML rendering and loading helpers.
- `Config`, `ConfigField`, `ConfigSchema`, `add_auto_init_config`, `validate_config`,
  and `generate_schema_json` provide multi-format configuration file handling.
  YAML is the recommended default format; JSON and TOML are also supported.
- `Application(config=..., auto_init_config=True)` registers an opt-in `init` command.
  `app.init_config()` supports explicit initialization without automatic registration.

## Local Workflow

Run from `packages/core` after the [development install](installation.md):

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m build --sdist --wheel
```

Run examples manually when changing user-facing CLI behavior.

```bash
PYTHONPATH=src python examples/simple/quickhead/app.py docs/usage.md -n 5
PYTHONPATH=src python examples/simple/ls-cli/quickls.py . --suffix .md
PYTHONPATH=src python examples/complex/pyk5l/app.py get pods --verbose
```

## Runtime Boundary

- `Application.run()` remains the low-level dispatcher for explicit token lists.
- `Application.main()` is the standard executable runtime. It reads `sys.argv[1:]` by
  default, prints results, returns exit codes, and can emit JSON payloads for automation.
- Use the application-level `error_handler` callback when an integrating application needs a
  custom global error layer on top of quickli errors.

## Application Logging and Distribution

Use the standard-library `logging` module in application code. Create named loggers in
modules and configure handlers once in the executable entrypoint, keeping logs on stderr:

```python
import logging

logger = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger.info("Starting application")
    return app.main()
```

In this excerpt, `app` is your assembled `Application`. Do not configure logging during
library or plugin imports, log credentials, or print diagnostics into JSON result streams.
See the official [logging guide](https://spmse.github.io/quickli/docs/guides#logging-guide)
for a complete configurable example and repeatable verbosity flags.

The [packaging guide](https://spmse.github.io/quickli/docs/guides#packaging-guide)
covers console-script entry points, standalone executables, and non-root containers.

## Planned Work

- Release Please maintains independent releases for the core library and documentation site.
  Their version updates are grouped into one release pull request.
  See the [release checklist](open-source-release.md#release-preparation-checklist).

## Naming and License

- Use `quickli` for the Python package, imports, and distribution metadata.
- Use `quiCkLI` as the stylized project name in prose when that improves readability.
- The repository is licensed under the MIT License.

## Documentation Maintenance

- Keep [Current State and Agent Guide](current-state.md) aligned with implementation,
  tests, specifications, and documented limitations.

- Update `README.md` when the public feature set changes.
- Update `docs/usage.md` when the API shape or examples change.
- Update `docs/validation.md` when built-in validators or validation behavior change.
- Update the release documentation and workflow when release automation changes.
- Update `docs/config.md` when the config API, format support, or schema generation behavior changes.
- Update the relevant file in `specs/` when behavior changes.
- Add or update an ADR in `docs/adr` when a significant design decision affects future evolution.
- Keep example READMEs aligned with the runnable code in the same folder.
