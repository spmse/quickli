---
sidebar_position: 3
---

# Command

`Command` represents one executable operation in a CLI.
`Subcommand` inherits from `Command` and is used for nested command trees.

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

## Nested subcommands example

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
