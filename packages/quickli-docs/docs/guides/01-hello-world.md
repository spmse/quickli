---
id: guide-hello-world
title: "Guide 1: Hello World"
sidebar_position: 2
description: >
  Build your first quickli application: a single entrypoint that greets a user by name
  with an optional uppercase flag. Covers Application, Argument, and Option.
keywords: [quickli, tutorial, hello world, entrypoint, argument, option, python, cli]
---

# Guide 1: Hello World

This guide creates the smallest useful `quickli` application: a greeting tool that
accepts a name and an optional flag to print the message in uppercase.

You will learn how to:
- create an `Application` with a description
- register an entrypoint using `@app.entrypoint`
- add a positional `Argument`
- add a boolean `Option` flag
- run the application from the command line

## The full example

Save the following file as `hello.py`:

```python
from __future__ import annotations

import sys

from quickli import Application, Argument, Option


app = Application(
    name="hello",
    description="Greet a person from the command line.",
)


@app.entrypoint(
    help_text="Print a greeting.",
    arguments=[Argument("name", help_text="Name to greet.")],
    options=[
        Option(
            "uppercase",
            short_name="u",
            is_flag=True,
            help_text="Print the greeting in uppercase.",
        ),
    ],
)
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message


if __name__ == "__main__":
    sys.exit(app.main())
```

## Run it

```bash
python hello.py Ada
# Hello, Ada!

python hello.py Ada --uppercase
# HELLO, ADA!

python hello.py Ada -u
# HELLO, ADA!
```

## Line-by-line explanation

### Imports

```python
from quickli import Application, Argument, Option
```

You only need to import the three classes you use. `quickli` keeps its public API small
and explicit.

### Creating the application

```python
app = Application(
    name="hello",
    description="Greet a person from the command line.",
)
```

`Application` is the root container. `name` is used in help output. `description` appears
below the usage line when you run the tool without arguments.

### Registering the entrypoint

```python
@app.entrypoint(
    help_text="Print a greeting.",
    arguments=[Argument("name", help_text="Name to greet.")],
    options=[
        Option(
            "uppercase",
            short_name="u",
            is_flag=True,
            help_text="Print the greeting in uppercase.",
        ),
    ],
)
def greet(name: str, uppercase: bool = False) -> str:
    ...
```

`@app.entrypoint` is used for commandless applications — the application has one purpose,
so there is no need for a command name.

- **`help_text`** appears in the generated usage output.
- **`arguments`** is a list of `Argument` instances in positional order.
- **`options`** is a list of `Option` instances.

### The `Argument` constructor

```python
Argument("name", help_text="Name to greet.")
```

`Argument` takes a positional name as its first argument. This name must match the
corresponding function parameter. By default, arguments are required. To make an argument
optional, pass `required=False` and provide a `default`.

### The `Option` constructor

```python
Option(
    "uppercase",
    short_name="u",
    is_flag=True,
    help_text="Print the greeting in uppercase.",
)
```

- **`"uppercase"`** becomes `--uppercase` on the command line.
- **`short_name="u"`** adds the `-u` short form.
- **`is_flag=True`** means the option is boolean: present → `True`, absent → `False`.
- The function parameter must match the option name with hyphens replaced by underscores
  (`uppercase` → `uppercase`).

### The handler function

```python
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message
```

The handler receives parsed values directly. `quickli` matches argument and option names
to parameter names. The default value for `uppercase` corresponds to the option being
absent.

The handler returns a string. `Application.main()` prints that return value for normal
successful runs.

### The entry point

```python
if __name__ == "__main__":
    sys.exit(app.main())
```

`Application.main()` is the simplest executable entry point. It reads `sys.argv[1:]`,
prints normal results, reports quickli runtime errors, and returns an exit code.

`Application.run(argv)` still accepts explicit tokens when you want that lower-level,
test-friendly boundary.

## Explore help output

Run without arguments to see the generated help:

```bash
python hello.py
```

quickli generates usage text from the registered arguments, options, and help strings.

## What to try next

- Add a second option (for example `--shout`) and change the message format.
- Make the `name` argument optional with `required=False` and `default="world"`.
- Read [Guide 2: File Viewer](./02-building-cat-cli.md) to learn about global options,
  multiple file arguments, and path validation.
