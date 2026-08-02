---
sidebar_position: 4
description: Argument describes a required positional input value for a command.
keywords: [quickli, argument, positional, required, optional, converter, validator]
---

# Argument

`Argument` describes a positional input value for a command. Arguments belong to a command
(or subcommand) and are resolved in the order they are declared.

```
Application
└── Command
    └── Argument   ← you are here
```

## Core behavior

- Arguments are positional and ordered.
- They may be required or optional.
- An argument becomes optional when it has a default value.
- A converter can transform raw text before handler invocation.
- Validators can check converted values.

## Basic example

```python
from quickli import Application, Argument

app = Application(name="demo")


@app.command(
    help_text="Count characters in a word.",
    arguments=[Argument("word")],
)
def count(word: str) -> str:
    return str(len(word))


print(app.run(["count", "hello"]))  # 5
```

## Optional argument with a default

```python
from quickli import Application, Argument

app = Application(name="demo")


@app.command(
    help_text="Greet a user.",
    arguments=[Argument("name", default="World")],
)
def greet(name: str = "World") -> str:
    return f"Hello, {name}!"


print(app.run(["greet"]))          # Hello, World!
print(app.run(["greet", "Alice"]))  # Hello, Alice!
```

## Argument with a converter

Pass a `converter` callable to transform the raw string before the handler receives it.

```python
from quickli import Application, Argument

app = Application(name="demo")


@app.command(
    help_text="Double a number.",
    arguments=[Argument("value", converter=int)],
)
def double(value: int) -> str:
    return str(value * 2)


print(app.run(["double", "7"]))  # 14
```

## Typical usage

Use arguments for required command context, such as paths, identifiers, or target names:

- source file path
- resource name
- numeric input for an operation

If required arguments are missing, command execution fails with a deterministic error.

## Tips

:::tip Argument vs. Option
Use an `Argument` when the value is the *subject* of the command — the thing the command
acts on (a file path, a name, an ID). Use an `Option` when the value *modifies how* the
command behaves (a format, a verbosity level, a boolean flag).

```
# Argument: the file is what the command acts on
cat myfile.txt

# Option: the format modifies how the output looks
cat --format json myfile.txt
```
:::

:::tip Order matters
Arguments are matched positionally in the order they are declared. Place required
arguments before optional ones to keep the command signature predictable.
:::

## Where to go next

- Use **[Options](./option.md)** for named, order-independent input.
- Go back to **[Command](./command.md)** to see the full command structure.
