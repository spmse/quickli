---
title: "Getting Started with quiCkLI: Your First Command-Line Application"
description: >
  Build your first Python command-line application with quiCkLI in under five minutes.
  This tutorial covers Application, Argument, and Option  -  the three primitives you need
  to know to get started.
slug: quickli-tutorial-01-hello-world
authors:
  - spmse
date: 2026-08-04
draft: true
tags: [tutorial, getting-started, quickli, python, cli]
series:
  name: "Getting Started with quiCkLI"
  position: 1
keywords: [quickli, python cli, command-line framework, tutorial, beginner]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

If you have ever wanted to build a small Python command-line tool but found larger
frameworks overwhelming, `quiCkLI` was designed for you. It is a minimal framework
that keeps the essentials visible so you can learn  -  and build  -  without unnecessary
complexity.

In this first article of the *Getting Started with quiCkLI* series you will build a
greeting tool with exactly three concepts: `Application`, `Argument`, and `Option`.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[0]} currentSlug="quickli-tutorial-01-hello-world" />

## What you will build

```bash
$ python hello.py Ada
$ Hello, Ada!

$ python hello.py Ada --uppercase
$ HELLO, ADA!
```

A single file. No configuration. Under thirty lines of Python.

:::tip

`Application.run()` returns the handler result. A real executable wrapper still needs to
print that result and decide how to map errors to exit codes.

:::

## Prerequisites

Install quickli in a virtual environment:

```bash
$ python -m venv .venv
$ source .venv/bin/activate   # Windows: .venv\Scripts\activate
$ pip install quickli
```

You need Python 3.12 or later.

## Step 1: Create the application

```python
from quickli import Application

app = Application(
    name="hello",
    description="Greet a person from the command line.",
)
```

`Application` is the root container. It owns command registration and dispatch. You give
it a name (used in help output) and a short description.

## Step 2: Register a handler

```python
from quickli import Application, Argument, Option

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
```

`@app.entrypoint` registers a function as the single handler for this application.

- `Argument("name")` declares a required positional value. quickli passes it directly to
  the `name` parameter of your function.
- `Option("uppercase", is_flag=True)` declares a boolean flag. Present → `True`,
  absent → `False`.

## Step 3: Run the application

```python
import sys

if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

`Application.run(argv)` accepts a list of tokens and returns the handler result. You
decide what to do with it  -  in this case, you print it.

## The full file

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
    print(app.run(sys.argv[1:]))
```

## Try it

```bash
$ python hello.py Ada           # Hello, Ada!
$ python hello.py Ada -u        # HELLO, ADA!
$ python hello.py               # (help output)
```

## What you learned

- `Application` owns registration and dispatch.
- `@app.entrypoint` registers a single handler for the whole application.
- `Argument` describes positional, required input.
- `Option` with `is_flag=True` adds a boolean switch.
- `Application.run(argv)` returns the result  -  you control output.

## Next in this series

The next article adds **file input**, **validation**, and **global options** by building a
small file viewer inspired by the Unix `cat` command.

📖 [Part 2: Reading Files  -  the quickcat tool →](/blog/quickli-tutorial-02-file-tools)
