# quiCkLI

[![CI](https://github.com/spmse/quickli/actions/workflows/ci.yml/badge.svg)](https://github.com/spmse/quickli/actions/workflows/ci.yml)
[![Coverage](https://github.com/spmse/quickli/actions/workflows/coverage.yml/badge.svg)](https://github.com/spmse/quickli/actions/workflows/coverage.yml)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)

quiCkLI is a minimal, educational Python framework for building command-line interfaces.
It keeps application structure, parsing, validation, configuration, plugins, and shell
completion explicit and readable.

The Python package and distribution name is `quickli`. The stylized project name is
`quiCkLI`.

## Current capabilities

- commandless applications with `@app.entrypoint(...)`
- named commands and subcommands for multi-command applications
- positional arguments, options, flags, repeatable values, and global options
- type conversion and validators for files, directories, positive numbers, and ranges
- generated help text with docstring fallback
- JSON, YAML, and TOML loading and rendering helpers
- configuration schemas, validation, and JSON Schema generation
- explicit plugin registration and loading
- Bash, PowerShell, and ZSH completion generation
- executable-shell output with structured quickli errors and JSON mode

The core API accepts explicit argument tokens through `Application.run()`. For executable
programs, `Application.main()` reads `sys.argv` by default, prints results, maps failures to
quickli errors, and returns process-friendly exit codes.

## Quick example

```python
from quickli import Application, Argument, Option

app = Application(name="hello", description="Greet a person.")


@app.entrypoint(
    help_text="Print a greeting.",
    arguments=[Argument("name")],
    options=[Option("uppercase", short_name="u", is_flag=True)],
)
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message


print(app.run(["Ada", "--uppercase"]))
```

For an executable shell:

```python
raise SystemExit(app.main())
```

## Repository layout

- [`packages/core`](packages/core): the Python package, tests, examples, specifications,
  and developer documentation
- [`packages/quickli-docs`](packages/quickli-docs): the Docusaurus documentation site
- [`.github`](.github): CI, coverage, release automation, and repository guidance

## Installation and development

For local development:

```bash
cd packages/core
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Run the core checks from `packages/core`:

```bash
python -m unittest discover -s tests -v
python -m ruff check .
python -m ruff format --check .
```

The repository requires Python 3.12, 3.13, or 3.14. The project uses the standard-library
`unittest` runner; Ruff, coverage, and build are development dependencies.

## Documentation

- [Documentation site](https://spmse.github.io/quickli/)
- [Documentation package](packages/quickli-docs/README.md)
- [Getting started guide](packages/quickli-docs/docs/getting-started.md)
- [Core concepts](packages/quickli-docs/docs/concepts/quickli-concepts.md)
- [Examples](packages/core/examples/README.md)
- [Specifications](packages/core/specs)
- [Architectural decisions](packages/core/docs/adr)

Start the documentation site from the repository root with:

```bash
pnpm install
pnpm --filter quickli-docs start
```

Build it with:

```bash
pnpm --filter quickli-docs build
```

The site currently supports English and German locales.

## Project status

quiCkLI is in alpha. The implementation, tests, specifications, and examples are being
developed together as an educational reference project. Release automation uses Release
Please; the core package is published to PyPI and the documentation site is deployed to
GitHub Pages.

## License

quiCkLI is licensed under the [MIT License](LICENSE).
