---
title: Comparing quickli, Click, and argparse
description: Compare Python CLI libraries and choose the right fit for your project.
keywords: [quickli, click, argparse, comparison, python, cli]
---

# Comparing quickli, Click, and argparse

`quickli`, [Click](https://click.palletsprojects.com/), and Python's built-in
[`argparse`](https://docs.python.org/3/library/argparse.html) help you build command-line
interfaces, but they make different trade-offs. `quickli` is a small, explicit framework;
Click is a feature-rich third-party library; and `argparse` is a parser included with Python.

## Feature comparison

| Feature | quickli | Click | argparse |
|---|---|---|---|
| Installation | Install the `quickli` package | Install the `click` package | Included in the Python standard library |
| Typical API | `Application`, `Command`, `Argument`, and `Option` resources | Decorators such as `@click.command()` and `@click.option()` | Build an `ArgumentParser`, add arguments, then parse |
| Multiple commands | Application command registry and nested subcommands | Commands and groups, including nested groups | Subparsers can dispatch to subcommands |
| Help | Generated application, command, and nested-command help; automatic `--help` and `-h` | Generated command help, with configurable help options | Generated parser help, normally available as `-h` and `--help` |
| Conversion and validation | Explicit converters and validators on argument and option resources | Parameter types, callbacks, and validation integrated with its parameter system | Types, actions, and custom validation in application code |
| Additional capabilities | Global options, shell-completion generation, configuration support, and an explicit plugin contract | Rich prompt, terminal, context, testing, and completion facilities | Flexible parsing primitives; higher-level behavior is generally assembled by the application |

`quickli` and Click both provide a framework for defining and composing commands. Their APIs
differ: quickli describes inputs with explicit resource objects, while Click's decorators
connect command parameters and options to the handler. For example:

```python
# quickli
@app.command(
    arguments=[Argument("name")],
    options=[Option("loud", is_flag=True)],
)
def greet(name: str, loud: bool = False) -> str:
    ...
```

```python
# Click
@click.command()
@click.argument("name")
@click.option("--loud", is_flag=True)
def greet(name: str, loud: bool) -> None:
    ...
```

With argparse, a similar command is assembled from parser calls:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--loud", action="store_true")
args = parser.parse_args()
```

The examples show the declaration style rather than complete applications. In particular,
`quickli.Application.main()` provides an executable shell, whereas `Application.run()` lets
the caller use the handler result directly.

## Which library should I choose?

- **Choose quickli** when you want a small framework with explicit command and input
  definitions, generated help, and a consistent structure for a growing CLI. It can also
  suit projects that want quickli's built-in configuration, completion, or plugin concepts.
- **Choose Click** when you need a mature, broad CLI toolkit, especially its richer terminal
  interactions, prompts, command contexts, testing support, and extensive ecosystem. It is
  a strong choice for polished, user-facing command-line applications.
- **Choose argparse** when your CLI is straightforward and you prefer a standard-library
  dependency with direct control over parser behavior. It is often a good fit for scripts,
  internal tools, and projects that do not need a separate CLI framework.

These libraries are not drop-in replacements for one another. Consider the complexity your
CLI needs today, the amount of framework behavior you want supplied, and your preference for
explicit resource declarations, decorators, or direct parser configuration.
