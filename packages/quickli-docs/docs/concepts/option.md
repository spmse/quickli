---
sidebar_position: 5
description: Option describes a named, order-independent input that modifies command behavior.
keywords: [quickli, option, flag, named, global, local, repeatable]
---

# Option

`Option` describes a named input that modifies command behavior. Options belong to a
command (local options) or to the `Application` itself (global options).

```
Application
├── global options   ← available to every command
└── Command
    └── Option       ← you are here (local option)
```

## Supported forms

- long form: `--output value`
- long assignment form: `--output=value`
- short form: `-o value`

## Core capabilities

- default values
- required options
- boolean flags (`is_flag=True`)
- conversion callables for non-flag values
- validators for converted values
- repeatable values (`multiple=True`)

Repeatable non-flag options accumulate values in a list. Repeatable flags accumulate
occurrence counts.

## Local and global options

Options can be defined on commands (local) or at the application level (global).
Global options may appear before or after the command name.

## Basic option example

```python
from quickli import Application, Argument, Option

app = Application(name="demo")


@app.command(
    help_text="Write text to a file.",
    arguments=[Argument("text")],
    options=[Option("output", short_name="o", default="out.txt")],
)
def write(text: str, output: str = "out.txt") -> str:
    return f"writing '{text}' to {output}"


print(app.run(["write", "hello"]))                     # writing 'hello' to out.txt
print(app.run(["write", "hello", "--output", "a.txt"]))  # writing 'hello' to a.txt
```

## Boolean flag example

```python
from quickli import Application, Option

app = Application(name="demo")


@app.command(
    help_text="Print version information.",
    options=[Option("verbose", short_name="v", is_flag=True)],
)
def version(verbose: bool = False) -> str:
    if verbose:
        return "demo version 1.0.0 (debug build)"
    return "demo 1.0.0"


print(app.run(["version"]))            # demo 1.0.0
print(app.run(["version", "--verbose"]))  # demo version 1.0.0 (debug build)
print(app.run(["version", "-v"]))        # demo version 1.0.0 (debug build)
```

## Repeatable option example

```python
from quickli import Application, Option

app = Application(name="demo")


@app.command(
    help_text="Tag a resource.",
    options=[Option("tag", short_name="t", multiple=True)],
)
def tag_resource(tag: list[str] | None = None) -> str:
    labels = tag or []
    return f"tags: {', '.join(labels)}"


print(app.run(["tag-resource", "--tag", "a", "--tag", "b"]))  # tags: a, b
```

## Global option example

```python
from quickli import Application, Option

app = Application(
    name="demo",
    global_options=[Option("verbose", short_name="v", is_flag=True)],
)


@app.command(help_text="Build the project.")
def build(verbose: bool = False) -> str:
    return f"building… (verbose={verbose})"


print(app.run(["--verbose", "build"]))  # building… (verbose=True)
print(app.run(["build", "--verbose"]))  # building… (verbose=True)
```

## Tips

:::tip Argument vs. Option
Use an `Argument` for the primary subject of the command (what it acts on). Use an
`Option` for anything that *changes how* the command behaves — output format, verbosity,
a toggle, or a secondary target.
:::

:::tip Local vs. global options
Define an option as **local** when it only makes sense for one command (like `--output`
for a write command). Define it as **global** when it should apply to every command in
the application (like `--verbose` or `--config`).
:::

:::tip Flags for on/off switches
Use `is_flag=True` when the option represents a boolean toggle that does not take a
value. The presence of the flag sets it to `True`; its absence leaves it as `False`.
:::

## Where to go next

- Use **[Arguments](./argument.md)** for positional, ordered input.
- Go back to **[Command](./command.md)** to see how options and arguments fit together.
- See **[Application](./application.md)** for how global options are declared.
