---
sidebar_position: 3
description: Command represents one executable action in a quiCkLI CLI.
keywords: [quickli, command, subcommand, handler, registration]
---

# Command

`Command` represents one executable operation in a CLI. Commands live directly inside an
`Application` and are the main way to expose named actions to the user.

```
Application
└── Command   ← you are here
    ├── Argument
    ├── Option
    └── Subcommand
        ├── Argument
        └── Option
```

`Subcommand` inherits from `Command` and is used for nested command trees. It behaves
identically to a `Command` but is attached under a parent command rather than directly
under the `Application`.

## What a command contains

- a public command name
- help text (explicit or derived from a docstring)
- positional argument definitions
- named option definitions
- optional nested subcommand definitions
- one handler callable

## Responsibilities

A command parses tokens that belong to it, validates the parsed values against resource
definitions, binds values to the handler signature, and executes the handler.

## Naming behavior

Commands are registered under unique names. Function names are normalized by replacing
underscores with hyphens when a name is not explicitly provided.

## Basic command example

```python
from quickli import Application, Argument, Option

app = Application(name="demo")


@app.command(
    help_text="Greet someone.",
    arguments=[Argument("name")],
    options=[Option("shout", is_flag=True)],
)
def greet(name: str, shout: bool = False) -> str:
    msg = f"Hello, {name}!"
    return msg.upper() if shout else msg


print(app.run(["greet", "Alice"]))           # Hello, Alice!
print(app.run(["greet", "Alice", "--shout"]))  # HELLO, ALICE!
```

## Nested subcommands example

Use `Subcommand` when a command naturally groups further actions, such as `env create`
and `env delete`.

```python
from quickli import Application, Argument, Subcommand

app = Application(name="demo")


@app.command(
    name="env",
    subcommands=[
        Subcommand(
            name="create",
            arguments=[Argument("name")],
            handler=lambda name: f"created:{name}",
        )
    ],
)
def env() -> str:
    return "env"


print(app.run(["env", "create", "dev"]))
```

## Tips

:::tip[Command vs. Subcommand]
Use a top-level `@app.command` for actions that are independent of each other, such as
`build` and `clean`. Use a `Subcommand` when actions logically share a namespace, such as
`env create`, `env list`, and `env delete`.
:::

:::tip[Help text from docstrings]
If you do not pass `help_text`, `quickli` automatically uses the function's docstring.
This keeps your handler code self-documenting.

```python
@app.command()
def build() -> str:
    """Build the project and produce a release artefact."""
    return "building…"
```
:::

## Where to go next

- Add **[Arguments](./argument.md)** to accept positional input.
- Add **[Options](./option.md)** to accept named flags and values.
- Go back to **[Application](./application.md)** to understand how commands are dispatched.
