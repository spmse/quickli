---
id: guide-ls-cli
title: "Guide 3: Directory Listing (quickls)"
sidebar_position: 4
description: >
  Build a directory listing tool with quickli. Learn optional arguments with defaults,
  the directory_path validator, and suffix filtering.
keywords: [quickli, tutorial, ls, directory listing, optional argument, directory_path]
---

# Guide 3: Directory Listing (quickls)

This guide builds `quickls`, a minimal `ls`-like tool that lists the contents of a
directory. It shows how to make an argument **optional** by providing a default value and
how to use the `directory_path` validator.

You will learn how to:
- make an `Argument` optional with `required=False` and a `default`
- use the built-in **`directory_path` validator**
- filter results with a repeatable suffix option

## The full example

Save the following file as `quickls.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, directory_path


app = Application(
    name="quickls",
    description="A tiny ls-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Show the scanned directory."),
    ],
)


@app.entrypoint(
    help_text="List files in a directory.",
    arguments=[
        Argument(
            "path",
            required=False,
            default=Path("."),
            validators=[directory_path()],
        )
    ],
    options=[
        Option("all", short_name="a", is_flag=True, help_text="Include hidden files."),
        Option(
            "suffix",
            short_name="s",
            multiple=True,
            help_text="Filter by one or more suffixes.",
        ),
    ],
)
def list_directory(
    path: Path = Path("."),
    all: bool = False,
    suffix: list[str] | None = None,
    verbose: bool = False,
) -> str:
    items = sorted(path.iterdir(), key=lambda item: item.name)
    if not all:
        items = [item for item in items if not item.name.startswith(".")]
    if suffix:
        items = [item for item in items if any(item.name.endswith(value) for value in suffix)]

    lines: list[str] = []
    if verbose:
        lines.append(f"Listing: {path}")
    lines.extend(item.name for item in items)
    return "\n".join(lines)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

## Run it

```bash
# List the current directory
python quickls.py

# List a specific directory
python quickls.py /tmp

# Show hidden files
python quickls.py --all

# Filter by suffix
python quickls.py --suffix .py

# Multiple suffixes
python quickls.py --suffix .py -s .md

# Show the directory path in output
python quickls.py --verbose
```

## Line-by-line explanation

### Optional argument with a default

```python
Argument(
    "path",
    required=False,
    default=Path("."),
    validators=[directory_path()],
)
```

- `required=False` makes the argument optional.
- `default=Path(".")` provides the value used when the argument is omitted.
- The validator still runs against the default value when it is resolved, so you can be
  confident the path is valid regardless of whether the user provides it.

### The `directory_path` validator

`directory_path()` checks whether the value points to an existing directory. Like
`file_path()`, it raises a clear error before the handler is called when the path does
not exist or is not a directory.

### Suffix filtering

```python
Option(
    "suffix",
    short_name="s",
    multiple=True,
    help_text="Filter by one or more suffixes.",
),
```

The `suffix` option can be passed multiple times. The handler uses `any()` to keep items
that match at least one of the given suffixes:

```python
if suffix:
    items = [item for item in items if any(item.name.endswith(value) for value in suffix)]
```

This pattern is useful whenever you want to accept a variable-length list of filter values
from the command line.

## What to try next

- Add a `--long` flag that prints file size and modification time alongside the name.
- Read [Guide 4: Directory Creator](./04-building-mkdir-cli.md) for more repeatable option
  patterns.
