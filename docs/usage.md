# Usage

## Quick Start

```python
from pathlib import Path

from quickli import Application, Argument, Option, file_path, number_range

app = Application(
    name="demo",
    description="A tiny CLI application",
    global_options=[Option("verbose", short_name="v", is_flag=True)],
)


@app.entrypoint(
    help_text="Greets a user.",
    arguments=[Argument("name"), Argument("repetitions", converter=int)],
    options=[
        Option("config", short_name="c", converter=Path),
        Option("uppercase", short_name="u", is_flag=True),
        Option("tag", short_name="t", multiple=True),
        Option("limit", short_name="l", converter=int, validators=[number_range(min_value=1, max_value=10)]),
    ],
)
def greet(
    name: str,
    repetitions: int,
    config: Path | None = None,
    uppercase: bool = False,
    tag: list[str] | None = None,
    limit: int | None = None,
    verbose: bool = False,
) -> str:
    message = " ".join(f"hello {name}" for _ in range(repetitions))
    if uppercase:
        message = message.upper()
    if tag:
        message = f"{'/'.join(tag)}: {message}"
    if config is not None:
        message = f"{config}: {message}"
    if limit is not None:
        message = f"{message} (limit={limit})"
    if verbose:
        message = f"[verbose] {message}"
    return message


print(
    app.run(
        [
            "--verbose",
            "Ada",
            "2",
            "--config",
            "settings.toml",
            "--uppercase",
            "--tag",
            "demo",
            "--tag",
            "intro",
            "--limit",
            "5",
        ]
    )
)
```

## Current Behavior

- Applications can expose a root entrypoint without defining commands.
- Commands are regular Python callables when a multi-command CLI is needed.
- Command names default to the function name.
- Underscores in function names are normalized to hyphens.
- Positional arguments are defined with `Argument` resources and passed as strings.
- Arguments can convert raw strings through a `converter` callable such as `int` or `Path`.
- Arguments and options can validate converted values through `validators=[...]`.
- Named options are defined with `Option` resources and passed as keyword arguments.
- Options can convert raw strings through a `converter` callable.
- Options can be marked with `multiple=True` to collect repeated values.
- Applications can define global options that are parsed before or after the command name.
- Flags are modeled as boolean options.
- Calling `run([])` returns generated help text unless a root entrypoint is registered and can run directly.

## Resource Model

- `Application` owns the global CLI configuration and optional command registry.
- `Argument` describes positional input.
- `Option` describes named input.
- `converter` transforms raw CLI text before the handler is called.
- `validators` enforce domain-specific rules after conversion.

## Validation Layer

The validation layer runs after conversion and before the handler is called.

```python
from quickli import Application, Argument, file_path

app = Application(name="demo")


@app.entrypoint(arguments=[Argument("input", validators=[file_path()])])
def show(input: Path) -> str:
    return input.read_text(encoding="utf-8")
```

Built-in path validators:

- `file_path()` validates file paths and returns `Path` objects.
- `directory_path()` validates directory paths and returns `Path` objects.
- Both validators support `exists=True`, `exists=False`, or `exists=None`.

Built-in numeric validators:

- `positive_number()` accepts numeric values greater than zero.
- `number_range(min_value=..., max_value=...)` enforces inclusive ranges.

Validators also contribute metadata to generated help output when they expose descriptions.

See [docs/validation.md](docs/validation.md) for a detailed guide to built-in validators,
default validation, and custom validator patterns.

## Multi-Command Applications

Use `@app.command(...)` when the CLI needs named subcommands.

```python
from quickli import Application

app = Application(name="demo")


@app.command(name="version")
def version() -> str:
    return "0.1.0"


print(app.run(["version"]))
```

## Help Output

`render_help()` builds application help from the registered resources.

- Each command appears in the command summary.
- Each command gets a generated usage line.
- Global options and local options are rendered in separate help sections.
- Arguments and options are listed with their help text.
- Required, default, and flag metadata are shown in the generated output.
- Validator metadata such as expected file paths or numeric ranges is shown when available.

## Docstring Help

If no explicit `help_text` is passed, quickli falls back to the handler docstring.

```python
@app.entrypoint()
def greet() -> str:
    """Greets the current user."""
    return "hello"
```

The generated help output will use `Greets the current user.` as the help text.

## Commandless Apps

Use `@app.entrypoint(...)` when the CLI does not need subcommands.

- This matches common tools such as `cat`, `ls`, `mkdir`, or `head`.
- The entrypoint uses the same `Argument` and `Option` resources as commands.
- Global options still work with the root entrypoint.

## Scope of the Initial Scaffold

The current scaffold focuses on package structure, registration, argument and option
resources, execution, help output, tests, and documentation. Plugins and advanced parsing
remain planned work.

## Naming

- Use `quickli` as the Python package and distribution name.
- Use `quiCkLI` as the stylized project name in human-facing documentation.

## Examples

- See `examples/README.md` for the full examples index.
- See `examples/simple/cat-cli/README.md` for a step-by-step guide that builds a small `cat` command.
- See `examples/simple/ls-cli/README.md` for a directory-listing example.
- See `examples/simple/mkdir-cli/README.md` for a small directory-creation example.
- See `examples/simple/quickhead/README.md` for a validation-focused `head` example.
- See `examples/complex/pyk5l/README.md` for a multi-command kubectl-like example.
