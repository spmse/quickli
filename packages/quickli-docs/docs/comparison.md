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

## A four-command `toolbox`

Consider a small `toolbox` application that combines file copying, directory creation, file
touching, and text output:

```text
toolbox cp SOURCE DESTINATION
toolbox mkdir PATH
toolbox touch PATH
toolbox echo TEXT
```

Assume the ordinary Python operation functions `copy_file(source, destination)`,
`make_directory(path)`, `touch_file(path)`, and `echo_text(text)` are defined in
`operations.py`. They perform the operation and return a message string. The examples focus on
how each library assembles and dispatches the same commands.

With quickli, register the functions with explicit argument resources. The application
provides command routing and executable help:

```python
from quickli import Application, Argument

from operations import copy_file, echo_text, make_directory, touch_file

app = Application(name="toolbox", description="File and text utilities.")

app.register(
    copy_file,
    name="cp",
    arguments=[Argument("source"), Argument("destination")],
)
app.register(
    make_directory,
    name="mkdir",
    arguments=[Argument("path")],
)
app.register(touch_file, name="touch", arguments=[Argument("path")])
app.register(echo_text, name="echo", arguments=[Argument("text")])

if __name__ == "__main__":
    raise SystemExit(app.main())
```

With Click, a group organizes the subcommands, and decorators declare each command's
parameters:

```python
import click

from operations import copy_file, echo_text, make_directory, touch_file

@click.group()
def toolbox():
    """File and text utilities."""

@toolbox.command()
@click.argument("source")
@click.argument("destination")
def cp(source, destination):
    click.echo(copy_file(source, destination))

@toolbox.command()
@click.argument("path")
def mkdir(path):
    click.echo(make_directory(path))

@toolbox.command()
@click.argument("path")
def touch(path):
    click.echo(touch_file(path))

@toolbox.command()
@click.argument("text")
def echo(text):
    click.echo(echo_text(text))

if __name__ == "__main__":
    toolbox()
```

With argparse, create a parser for each subcommand, then explicitly dispatch the parsed
arguments to the corresponding operation:

```python
import argparse

from operations import copy_file, echo_text, make_directory, touch_file

parser = argparse.ArgumentParser(prog="toolbox", description="File and text utilities.")
commands = parser.add_subparsers(dest="command", required=True)

cp_parser = commands.add_parser("cp", help="Copy a file.")
cp_parser.add_argument("source")
cp_parser.add_argument("destination")
cp_parser.set_defaults(
    run=lambda args: print(copy_file(args.source, args.destination))
)

mkdir_parser = commands.add_parser("mkdir", help="Create a directory.")
mkdir_parser.add_argument("path")
mkdir_parser.set_defaults(run=lambda args: print(make_directory(args.path)))

touch_parser = commands.add_parser("touch", help="Create a file or update its timestamp.")
touch_parser.add_argument("path")
touch_parser.set_defaults(run=lambda args: print(touch_file(args.path)))

echo_parser = commands.add_parser("echo", help="Write text.")
echo_parser.add_argument("text")
echo_parser.set_defaults(run=lambda args: print(echo_text(args.text)))

args = parser.parse_args()
args.run(args)
```

Each design supports this command tree and generated help, but the application structure
differs as it grows:

| Concern | quickli | Click | argparse |
|---|---|---|---|
| Add a command | Register a handler and its `Argument`/`Option` resources with the application | Add a decorated callback to the command group | Create a subparser, add its inputs, and set its dispatch handler |
| Dispatch | Handled by `Application.run()` or `Application.main()` | Handled by invoking the group | Application code calls the handler selected by the parser |
| Extend from another module | Register imported handlers or load a `Plugin` | Add or attach commands to a group | Add subparsers while assembling the parser, or factor parser setup into application code |

This larger example highlights the trade-off: quickli and Click provide application-level
command organization, while argparse gives the application direct control over how parsing
connects to its handlers.

The [complete runnable applications](https://github.com/spmse/quickli/tree/main/packages/core/examples/complex/toolbox)
share the same file operations. Their
[integration tests](https://github.com/spmse/quickli/blob/main/packages/core/tests/test_toolbox_examples.py)
exercise all four commands against temporary files and directories.

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
