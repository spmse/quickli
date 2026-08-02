---
title: "Getting Started with quiCkLI: Reading Files and Validating Input"
description: >
  Learn how to accept file paths, validate them before your handler runs, and use global
  options that apply to every command in your application. We build quickcat, a minimal
  cat-like file viewer.
slug: quickli-tutorial-02-file-tools
authors:
  - spmse
date: 2026-07-31
tags: [tutorial, quickli, python, cli, validators, file-path]
series:
  name: "Getting Started with quiCkLI"
  position: 2
keywords: [quickli, python cli, validators, file_path, global options, tutorial]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

In [Part 1](/blog/quickli-tutorial-01-hello-world) you built a greeting tool with a
single argument and a flag. In this article you will add two new ideas:
**validators** that reject invalid input before your handler runs, and **global options**
that apply to every command in an application.

The example is `quickcat`, a minimal file viewer modeled after the Unix `cat` command.

:::note

`Application.run()` reads `sys.argv[1:]` by default. Pass an explicit list to override,
or set `auto_sys_argv=False` to disable automatic reading.

:::

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[0]} currentSlug="quickli-tutorial-02-file-tools" />

## What you will build

```bash
$ python quickcat.py README.md
$ python quickcat.py README.md --number
$ python quickcat.py README.md -i CONTRIBUTING.md --verbose
```

## New concepts

| Concept | Purpose |
|---|---|
| `file_path()` | Built-in validator that checks whether a path points to a real file |
| `global_options` | Options that appear on `Application` and apply to every handler |
| `multiple=True` | Accept the same option more than once and collect values into a list |

## Global options

```python
app = Application(
    name="quickcat",
    description="A tiny cat-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
)
```

Global options live on `Application`, not on an individual command. They can appear before
or after the command name on the command line, and every handler that wants them declares
the matching parameter.

## The `file_path` validator

```python
Argument("path", help_text="Primary file path.", validators=[file_path()]),
```

`file_path()` is a built-in validator factory. It returns a callable that quickli runs
after parsing but before calling your handler. If the path does not exist or is not a
file, execution stops with a clear error message  -  your handler never sees an invalid
value.

You can pass multiple validators in the list; they run left to right.

## Repeatable options

```python
Option(
    "include",
    short_name="i",
    multiple=True,
    validators=[file_path()],
    help_text="Additional file paths to print after the primary file.",
),
```

`multiple=True` lets users pass the option more than once:

```bash
$ python quickcat.py main.py -i utils.py -i helpers.py
```

The handler receives `include` as `list[Path] | None`. When absent, it is `None`.

## The full example

```python
from __future__ import annotations

from pathlib import Path

from quickli import Application, Argument, Option, file_path


app = Application(
    name="quickcat",
    description="A tiny cat-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
)


@app.entrypoint(
    help_text="Print one or more text files to stdout.",
    arguments=[
        Argument("path", help_text="Primary file path.", validators=[file_path()]),
    ],
    options=[
        Option("encoding", short_name="e", default="utf-8", help_text="Text encoding."),
        Option("number", short_name="n", help_text="Print line numbers.", is_flag=True),
        Option(
            "include",
            short_name="i",
            multiple=True,
            validators=[file_path()],
            help_text="Additional file paths to print after the primary file.",
        ),
    ],
)
def show(
    path: Path,
    encoding: str = "utf-8",
    number: bool = False,
    include: list[Path] | None = None,
    verbose: bool = False,
) -> str:
    input_paths = [path, *(include or [])]
    rendered_chunks: list[str] = []

    for input_path in input_paths:
        text = input_path.read_text(encoding=encoding)
        lines = text.splitlines()

        if number:
            lines = [f"{index:>4}  {line}" for index, line in enumerate(lines, start=1)]

        if verbose:
            rendered_chunks.append(f"==> {input_path} <==")
        rendered_chunks.append("\n".join(lines))

    return "\n".join(chunk for chunk in rendered_chunks if chunk)


if __name__ == "__main__":
    print(app.run())
```

## What you learned

- `global_options` on `Application` declare options available to every handler.
- `file_path()` validates that a value is an existing, readable file.
- `multiple=True` accumulates repeated option values into a list.
- Validators run before the handler, keeping the handler body clean.

## Next in this series

The final article builds a kubectl-like multi-command application with `@app.command`,
custom validator factories, and `CommandExecutionError`.

📖 [Part 3: Multi-Command Applications →](/blog/quickli-tutorial-03-multi-command-cli)
