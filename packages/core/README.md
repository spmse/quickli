# quiCkLI

quiCkLI is a minimal, educational Python framework for building command-line interfaces.
The package and import name is `quickli`. It supports Python 3.12, 3.13, and 3.14.

The project is in alpha. Select and test a released version before depending on its APIs.
The online documentation follows the source checkout and may describe unreleased additions.

## Installation

Install the published package in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install quickli
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Your first command-line application

Save this example as `hello.py`:

```python
from quickli import Application, Argument, Option

app = Application("hello", description="Greet a person.")


@app.entrypoint(
    arguments=[Argument("name", help_text="Person to greet.")],
    options=[Option("uppercase", short_name="u", is_flag=True)],
)
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message


if __name__ == "__main__":
    raise SystemExit(app.main())
```

Run the application:

```bash
python hello.py Ada
python hello.py Ada -u
python hello.py --help
```

The first two calls print `Hello, Ada!` and `HELLO, ADA!`. The help request prints usage
without calling the handler. `Application.main()` prints results, reports errors to stderr,
and returns a process exit code. For library use and tests, `app.run(["Ada"])` returns
the handler result without printing it.

## Named commands

Use `@app.command()` for a CLI with several operations:

```python
from quickli import Application, Argument, Option

app = Application("tasks")


@app.command(
    arguments=[Argument("target")],
    options=[Option("retries", converter=int, default=3)],
)
def deploy(target: str, retries: int = 3) -> str:
    """Deploy a target with a configurable retry count."""
    return f"Deploying {target} with {retries} retries"


if __name__ == "__main__":
    raise SystemExit(app.main())
```

Save it as `tasks.py`, then run `python tasks.py deploy staging --retries 5`.
Use `python tasks.py deploy -h` for command help. Nested subcommands support help too.
Explicit options claiming a help alias retain their behavior; set `auto_help=False` on
the application to disable automatic help.

## Configuration

Define your own schema and choose YAML, JSON, or TOML:

```python
from quickli import Application, Config, ConfigField, ConfigSchema

schema = ConfigSchema(fields=[
    ConfigField("host", default="localhost"),
    ConfigField("port", value_type=int, default=8080),
])
config = Config("settings.json", schema=schema)
app = Application("service", config=config, auto_init_config=True)

data = app.run(["init"])
print(data["host"])
```

The opt-in `init` command creates a missing configuration from schema defaults. If a file
already exists, initialization loads and validates it rather than resetting it.
Construction does not write files. When the automatic command is disabled, use
`app.init_config()` explicitly.

Loading does not merge missing defaults into existing files. Required fields without
defaults are left out of new templates and must be filled in before loading. JSON/YAML
configuration roots must be mappings with string keys. YAML files use PyYAML safe loading
and serialization; the separate `quickli.parsers` YAML string helpers support a smaller subset.

## Features

- Single-action entrypoints, named commands, and nested subcommands.
- Positional arguments, local/global options, boolean flags, and repeatable options.
- Explicit converters and validators for checked input.
- Automatic `--help` and `-h` with generated usage and docstring descriptions.
- JSON/YAML/TOML configuration, validation, initialization, and JSON Schema export.
- Explicit plugin loading and Bash, Zsh, and PowerShell completion generation.
- Structured errors, exit codes, and optional JSON output through `Application.main()`.

## Documentation and examples

- [Getting started](https://spmse.github.io/quickli/docs/getting-started)
- [Application concepts](https://spmse.github.io/quickli/docs/concepts/application)
- [Configuration](https://spmse.github.io/quickli/docs/concepts/config)
- [Logging integration](https://spmse.github.io/quickli/docs/guides#logging-guide)
- [Packaging, executable binaries, and containers](https://spmse.github.io/quickli/docs/guides#packaging-guide)
- [Source and runnable examples](https://github.com/spmse/quickli)
- [Issues](https://github.com/spmse/quickli/issues)
- [Releases](https://github.com/spmse/quickli/releases)

## License

MIT License. The distribution includes the full license text in `LICENSE`.
