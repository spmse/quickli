---
id: guide-cat-cli
title: "Guide 2: File Viewer (quickcat)"
sidebar_position: 3
description: >
  Build a cat-like file viewer with quickli. Learn global options, multiple file arguments,
  the file_path validator, and repeatable options.
keywords: [quickli, tutorial, cat, file viewer, global options, validators, repeatable options]
---

# Guide 2: File Viewer (quickcat)

This guide builds `quickcat`, a minimal `cat`-like tool that prints one or more files to
standard output. It introduces global options, the built-in `file_path` validator, and
repeatable options.

You will learn how to:
- define **global options** on the `Application`
- use the built-in **`file_path` validator**
- accept **repeatable options** with `multiple=True`
- combine multiple input paths in the handler

## The full example

Save the following file as `quickcat.py`:

```python
from __future__ import annotations

import sys
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
    print(app.run(sys.argv[1:]))
```

## Run it

```bash
# Print a single file
python quickcat.py README.md

# Print with line numbers
python quickcat.py README.md --number

# Print multiple files (verbose shows filenames)
python quickcat.py README.md -i CONTRIBUTING.md --verbose

# Change text encoding
python quickcat.py data.txt --encoding latin-1
```

## Line-by-line explanation

### Global options

```python
app = Application(
    name="quickcat",
    description="A tiny cat-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
)
```

Global options are defined at the `Application` level. They can appear **before or after**
the command name on the command line. Every handler that wants to use a global option must
declare the matching parameter.

### The `file_path` validator

```python
Argument("path", help_text="Primary file path.", validators=[file_path()]),
```

`file_path()` returns a validator function that checks whether the given value points to
an existing, readable file. If the path does not exist, the command fails with a clear
error message before the handler is called.

Validators are called after conversion, so the handler receives a `Path` object, not a
raw string.

### Repeatable options

```python
Option(
    "include",
    short_name="i",
    multiple=True,
    validators=[file_path()],
    help_text="Additional file paths to print after the primary file.",
),
```

`multiple=True` tells quickli to accumulate every occurrence of `--include` into a list.
You can pass the option several times:

```bash
python quickcat.py main.py -i utils.py -i helpers.py
```

The handler receives `include` as `list[Path] | None`. When the option is not passed at
all, `include` is `None`.

### Automatic type annotation

The handler signature uses `Path` as the type for `path`:

```python
def show(
    path: Path,
    encoding: str = "utf-8",
    number: bool = False,
    include: list[Path] | None = None,
    verbose: bool = False,
) -> str:
```

quickli uses the type annotations together with the registered converters and validators
to pass ready-to-use values to the handler.

### Building the output

```python
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
```

The handler collects chunks for each file and joins them at the end. Empty strings
(produced by empty files) are filtered out.

## What to try next

- Add a `--max-lines` option using `converter=int` to limit output length.
- Read [Guide 3: Directory Listing](./03-building-ls-cli.md) for optional arguments and
  directory validation.
