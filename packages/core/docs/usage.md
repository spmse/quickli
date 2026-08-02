# Usage

## Quick Start

```python
from pathlib import Path

from quickli import Application, Argument, Option, Subcommand, file_path, number_range

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
        Option(
            "limit",
            short_name="l",
            converter=int,
            validators=[number_range(min_value=1, max_value=10)],
        ),
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

`Application.run()` is a library-core dispatcher. It receives explicit tokens,
dispatches the matching handler, and returns that handler's result.
By default, it does not read `sys.argv`, print the result, render process-level errors, or
select an exit code.
The caller decides how to adapt the returned value to an executable program.

When you want quickli to provide the executable shell, call `Application.main()` instead.
It reads `sys.argv[1:]` by default, prints results, returns an exit code, and converts
runtime failures into structured quickli errors.

```python
raise SystemExit(app.main())
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
- Commands can expose nested `Subcommand` resources.
- Calling `run([])` returns generated help text unless a root entrypoint is registered and
    can run directly.
- Calling `main()` runs an executable shell around `run()` and returns an integer exit code.
- User callback failures are wrapped in `UserCodeError` and keep the original exception as
  `original_error`.
- `main(output_format="json")` emits machine-readable success and error payloads.

## Executable Shell and Error Handling

Use `main()` when the application should own stdout, stderr, and process exit codes.

```python
from quickli import Application, CLIError

app = Application(
    name="demo",
    error_handler=lambda error: CLIError(f"custom: {error}"),
)


@app.command()
def explode() -> None:
    raise RuntimeError("boom")


raise SystemExit(app.main(output_format="json"))
```

In text mode, quickli prints the error message to stderr.
In JSON mode, quickli prints payloads such as:

```json
{"ok": false, "error": {"code": "user_code_error", "message": "..."}}
```

## Resource Model

- `Application` owns the global CLI configuration and optional command registry.
- `Argument` describes positional input.
- `Option` describes named input.
- `converter` transforms raw CLI text before the handler is called.
- `validators` enforce domain-specific rules after conversion.

## Validation Layer

The validation layer runs after conversion and before the handler is called.

```python
from pathlib import Path

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

See [validation.md](validation.md) for a detailed guide to built-in validators,
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

## Nested Subcommands

Use `Subcommand` resources when a command needs nested operations.

```python
from quickli import Application, Argument, Subcommand

app = Application(name="demo")


@app.command(
    name="env",
    subcommands=[
        Subcommand(
            name="create",
            help_text="Creates an environment.",
            arguments=[Argument("name")],
            handler=lambda name: f"created:{name}",
        )
    ],
)
def env() -> str:
    return "env"


print(app.run(["env", "create", "dev"]))
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

## Configuration Files

quickli includes native TOML configuration file support.

Define a schema, create a `Config` object, and call `add_auto_init_config` to
initialise the file on first run or load it on subsequent runs.

```python
from pathlib import Path

from quickli import (
    Config,
    ConfigField,
    ConfigSchema,
    add_auto_init_config,
    validate_config,
)

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, required=False, default="localhost"),
        ConfigField("port", value_type=int, required=False, default=8080),
    ]
)

config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
data = add_auto_init_config(config)

issues = validate_config(config)
for issue in issues:
    print(f"[{issue.severity.upper()}] {issue.field}: {issue.message}")
```

See [config.md](config.md) for the complete configuration file guide.

## Shell Completion

Enable shell completion by passing `shell_completion=True` to `Application`.
This registers a built-in `shell-completion` command that generates scripts for
**bash**, **zsh**, and **PowerShell**.

```python
app = Application(name="myapp", shell_completion=True)
```

Generate and install a bash script:

```bash
myapp shell-completion bash >> ~/.bash_completion
source ~/.bash_completion
```

Generate and install a zsh script:

```zsh
myapp shell-completion zsh >> ~/.zshrc
source ~/.zshrc
```

Generate and install a PowerShell script:

```powershell
myapp shell-completion powershell >> $PROFILE
. $PROFILE
```

See [shell-completion.md](shell-completion.md) for the full guide including standalone
generator functions and the `SUPPORTED_SHELLS` constant.

## Scope of the Initial Scaffold

The current scaffold focuses on package structure, registration, argument and option
resources, nested subcommands, conversion, validation, execution, help output, shell
completion, configuration files, and a rudimentary plugin loading system.
Plugin discovery via package metadata and a standard executable runtime remain planned
or out of scope.
Format-specific JSON, YAML, and TOML rendering/loading helpers are provided through
`quickli.parsers`.

## Format-specific Parser Helpers

Use `render_json(...)`, `render_yaml(...)`, `render_toml(...)` and their matching `load_*`
functions when a command
needs structured text output or input.

```python
from quickli import load_yaml, render_json

data = load_yaml("name: Ada\nroles:\n  - admin\n")
output = render_json(data)
```

Each parser function accepts one explicit format. Use the JSON, YAML, or TOML function that
matches the data you are reading or writing; there is no format-detecting parser entrypoint.

## Plugin System

Plugins extend an application without modifying the core package.  A plugin subclasses
`quickli.Plugin`, which defines a three-method contract: `name`, `description`, and
`register`.  Load a plugin by calling `Application.load_plugin(plugin)`.

```python
import quickli


class VersionPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "version-plugin"

    @property
    def description(self) -> str:
        return "Adds a version command."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Prints the application version.")
        def version() -> str:
            return "1.0.0"


app = quickli.Application(name="demo")
app.load_plugin(VersionPlugin())
print(app.run(["version"]))  # 1.0.0
```

`Application.plugins` returns a copy of the loaded plugins list.

`PluginLoadError` is raised when:
- the plugin name is empty,
- a plugin with the same name is already loaded,
- or the plugin's `register` method fails.

See `specs/plugin.md` for the full plugin contract.

## Naming

- Use `quickli` as the Python package and distribution name.
- Use `quiCkLI` as the stylized project name in human-facing documentation.

## Examples

- See `examples/README.md` for the full examples index.
- See `examples/simple/cat-cli/README.md` for a step-by-step guide that builds a small `cat`
    command.
- See `examples/simple/ls-cli/README.md` for a directory-listing example.
- See `examples/simple/mkdir-cli/README.md` for a small directory-creation example.
- See `examples/simple/quickhead/README.md` for a validation-focused `head` example.
- See `examples/complex/pyk5l/README.md` for a multi-command kubectl-like example.
