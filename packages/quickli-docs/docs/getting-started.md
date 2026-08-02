---
id: getting-started
title: Getting Started
sidebar_position: 2
description: Install quickli and build your first command-line application.
---

import { AddToProject } from '@site/src/components/QuickliExamples';

# Getting Started

This guide creates a small command-line application with one entrypoint, one positional
argument, and one flag. quickli supports Python 3.12, 3.13, and 3.14.

## Install quickli

For a project using the released package, install quickli in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install quickli
```

When working from the quickli repository, install the package in editable mode instead:

```bash
python -m pip install -e packages/core
```

<AddToProject />

## Create an application

Save this example as `hello.py`:

```python
from __future__ import annotations

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
    print(app.run())
```

## Run it

Pass the command-line tokens to the application:

```bash
python hello.py Ada
python hello.py Ada --uppercase
```

The first command prints `Hello, Ada!`; the second prints `HELLO, ADA!`.

## Explore generated help

The application generates help from its registered arguments and options. Run it without
arguments to see the usage text:

```bash
python hello.py
```

`Application.run()` reads `sys.argv[1:]` by default and returns the handler result. Pass
an explicit list to override: `app.run(["Ada", "--uppercase"])`. Set
`auto_sys_argv=False` at construction to disable automatic reading entirely.

## Where to go next

- Use `@app.command()` to build a multi-command CLI.
- Use `converter=int` or `converter=Path` to convert input values.
- Add validators such as `file_path()` or `number_range()` for checked input.
- Read the [project examples](https://github.com/spmse/quickli/tree/main/packages/core/examples)
  for small, focused applications.