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
| `help_text` | `str` | `""` | Description; application registration falls back to the handler docstring. |
| `arguments` | `tuple[Argument, ...]` | `()` | Ordered positional argument definitions. |
| `options` | `tuple[Option, ...]` | `()` | Named local option definitions. |
| `subcommands` | `tuple[Subcommand, ...]` | `()` | Nested subcommand definitions. |
| `handler` | `Callable` | Required | The Python function or callable executed when the command matches. |

## Ways to Author and Register Commands

Use decorators for nearby handlers and `app.register()` for imported handlers. A standalone
`Command` can also execute tokens directly. Docstrings supply help, not registration.

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

### 2. Registering Handlers from Other Modules

Keep domain logic independent of the application, then register it where the app is assembled:

```python
from quickli import Application, Argument, Option

# Module: commands/build.py
def build_handler(target: str, release: bool = False) -> str:
    mode = "release" if release else "debug"
    return f"Building {target} ({mode})"

app = Application(name="demo")
app.register(
    build_handler,
    name="build",
    help_text="Compile the source project.",
    arguments=[Argument("target")],
    options=[Option("release", is_flag=True)],
)

print(app.run(["build", "core", "--release"]))
```

In a multi-file project, put `build_handler` in `commands/build.py` and import it into your
application module. Register once during assembly, not inside another handler.
There is no `app.register_command()` method.

For lower-level use without an application registry:

```python
from quickli import Argument, Command

command = Command("echo", handler=lambda text: text, arguments=[Argument("text")])
assert command.execute(["hello"]) == "hello"
print(command.render_help("demo"))
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

print(app.commands["test"].render_help(app.name))
```

:::tip[Docstrings Keep Code Self-Documenting]
Application registration uses the handler's cleaned docstring when `help_text` is empty.
Keep it concise: the full text is used, not just its first paragraph.
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
Explicit names are normalized too: `name="list_users"` registers `list-users`.
Names must remain unique after normalization; duplicates raise `CommandRegistrationError`.
:::

## Parameter Binding & Validation

When a command executes, `quickli` parses input tokens into positional arguments and named options, then matches them against the handler function's parameter signature:

1. **Token Parsing**: Positional tokens fill **[Argument](./argument.md)** definitions in declaration order. Named tokens (`--flag` or `--option=value`) fill **[Option](./option.md)** definitions.
2. **Conversion & Validation**: Raw string tokens pass through converters (e.g. `int`, `Path`) and validators (e.g., `file_path`, `number_range`).
3. **Signature binding**: Arguments are passed positionally in declaration order. Options
   are passed as keywords, replacing hyphens with underscores in destination names.
   Missing required input, unknown options, or incompatible signatures raise
   `CommandExecutionError` during execution.

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
Type annotations document intent; they do not enable conversion. Declare `converter=int`
explicitly. Handler positional parameter order must match arguments; option destination
names must be accepted as keywords. Signature mismatches fail at execution, not registration.
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
    return app.commands["env"].render_help(app.name)

print(app.run(["env", "create", "staging", "--region", "eu-central-1"]))
# Returns: Created staging in eu-central-1
```

:::tip[Subcommand Scope]
Selected subcommands receive application-global options, but not their parent's local
options. Their handlers must accept global keyword destinations, explicitly or through
`**kwargs`. Declare local options on the selected subcommand; they do not apply to siblings.
:::

## Where to Go Next

- Learn how positional input works in **[Argument](./argument.md)**.
- Learn about flags, repeatable values, and short aliases in **[Option](./option.md)**.
- Learn how global options and entrypoints are configured on **[Application](./application.md)**.
- Parse structured handler input/output using **[Parsers](./parsers.md)**.
- Package sets of commands into reusable modules using **[Plugin](./plugin.md)**.
