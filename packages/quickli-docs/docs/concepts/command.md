---
sidebar_position: 3
description: Command represents an executable operation and subcommand hierarchy in a quiCkLI CLI.
keywords: [quickli, command, subcommand, handler, authoring, registration, signature binding, docstrings]
---

# Command

`Command` represents an individual executable operation in a CLI application. Commands are registered with an **[Application](./application.md)** and own positional **[Argument](./argument.md)** definitions, named **[Option](./option.md)** definitions, and optional nested **[Subcommand](#nested-subcommands)** trees.

```
Application
└── Command   ← you are here
    ├── Argument
    ├── Option
    └── Subcommand
        ├── Argument
        └── Option
```

## Command Properties

A `Command` object contains the following explicit attributes:

| Property | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | Required | Public command invocation name (e.g., `"build"`). Normalized from function names if omitted. |
| `help_text` | `str \| None` | `None` | Human-readable help text. If `None`, falls back to the handler function's docstring. |
| `arguments` | `list[Argument]` | `[]` | Positional argument definitions. |
| `options` | `list[Option]` | `[]` | Named local option definitions. |
| `subcommands` | `list[Subcommand]` | `[]` | Nested subcommand definitions. |
| `handler` | `Callable` | Required | The Python function or callable executed when the command matches. |

## Ways to Author and Register Commands

`quickli` supports three explicit ways to define and register commands:

### 1. Decorator Authoring (`@app.command`)

The decorator pattern is the most concise way to define commands directly alongside handler functions:

```python
from quickli import Application, Argument, Option

app = Application(name="demo")

@app.command(
    name="deploy",
    help_text="Deploy an application target.",
    arguments=[Argument("target")],
    options=[Option("env", short_name="e", default="production")],
)
def deploy_app(target: str, env: str = "production") -> str:
    return f"Deploying {target} to {env}"

print(app.run(["deploy", "web-api", "-e", "staging"]))
```

### 2. Standalone Class Authoring (`Command` Instance)

You can instantiate `Command` objects directly for modular codebases where commands are defined across separate modules or packages:

```python
from quickli import Application, Command, Argument, Option

# Module: commands/build.py
def build_handler(target: str, release: bool = False) -> str:
    mode = "release" if release else "debug"
    return f"Building {target} ({mode})"

build_command = Command(
    name="build",
    help_text="Compile the source project.",
    arguments=[Argument("target")],
    options=[Option("release", is_flag=True)],
    handler=build_handler,
)

# Module: main.py
app = Application(name="demo")
app.register_command(build_command)

print(app.run(["build", "core", "--release"]))
```

### 3. Docstring Help Text Authoring

If `help_text` is omitted, `quickli` automatically uses the handler function's docstring for help generation:

```python
from quickli import Application

app = Application(name="demo")

@app.command()
def test() -> str:
    """Run all automated unit tests in the workspace."""
    return "tests passed"

print(app.run(["test", "--help"]))
```

:::tip[Docstrings Keep Code Self-Documenting]
Using docstrings for `help_text` eliminates duplication between code documentation and CLI help screens. The first paragraph of the docstring is rendered in command listings.
:::

## Command Name Normalization

When using `@app.command()` without an explicit `name` argument, `quickli` normalizes Python function names by converting underscores (`_`) into hyphens (`-`):

```python
@app.command()
def list_users() -> str:  # Registered as command name: "list-users"
    return "user listing"

print(app.run(["list-users"]))
```

:::note[Explicit Names Override Normalization]
If you pass `name="list_users"` explicitly to `@app.command()`, the exact string provided will be used as the CLI command name.
:::

## Parameter Binding & Validation

When a command executes, `quickli` parses input tokens into positional arguments and named options, then matches them against the handler function's parameter signature:

1. **Token Parsing**: Positional tokens fill **[Argument](./argument.md)** definitions in declaration order. Named tokens (`--flag` or `--option=value`) fill **[Option](./option.md)** definitions.
2. **Conversion & Validation**: Raw string tokens pass through converters (e.g. `int`, `Path`) and validators (e.g., `file_path`, `number_range`).
3. **Signature Binding**: Parsed values are bound to function parameters matching the argument/option names. Missing required arguments or unknown options raise a `CommandExecutionError`.

```python
from quickli import Application, Argument, Option

app = Application(name="demo")

@app.command(
    arguments=[Argument("count", converter=int)],
    options=[Option("label", default="item")],
)
def repeat(count: int, label: str = "item") -> str:
    return ", ".join([label] * count)

print(app.run(["repeat", "3", "--label", "hello"]))  # hello, hello, hello
```

:::info[Signature Parameter Matching]
Handler parameter names **must** match the defined `Argument` and `Option` resource names. If a parameter is missing or mismatched, `quickli` raises a registration error during setup.
:::

## Nested Subcommands

`Subcommand` inherits all capabilities of `Command` and enables nested command trees (e.g. `git remote add` or `kubectl config view`):

```python
from quickli import Application, Command, Subcommand, Argument, Option

app = Application(name="cloud")

@app.command(
    name="env",
    help_text="Manage cloud environments.",
    subcommands=[
        Subcommand(
            name="create",
            help_text="Create a new environment.",
            arguments=[Argument("env_name")],
            options=[Option("region", default="us-east-1")],
            handler=lambda env_name, region="us-east-1": f"Created {env_name} in {region}",
        ),
        Subcommand(
            name="delete",
            help_text="Delete an environment.",
            arguments=[Argument("env_name")],
            handler=lambda env_name: f"Deleted {env_name}",
        ),
    ],
)
def env_root() -> str:
    return "Use 'cloud env --help' to list subcommands."

print(app.run(["env", "create", "staging", "--region", "eu-central-1"]))
# Returns: Created staging in eu-central-1
```

:::tip[Subcommand Scope]
Subcommands inherit global options defined on the **[Application](./application.md)**, but local options belong specifically to the command or subcommand on which they are declared.
:::

## Where to Go Next

- Learn how positional input works in **[Argument](./argument.md)**.
- Learn about flags, repeatable values, and short aliases in **[Option](./option.md)**.
- Learn how global options and entrypoints are configured on **[Application](./application.md)**.
- Parse structured handler input/output using **[Parsers](./parsers.md)**.
- Package sets of commands into reusable modules using **[Plugin](./plugin.md)**.

