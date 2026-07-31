---
id: guide-mkdir-cli
title: "Guide 4: Directory Creator (quickmkdir)"
sidebar_position: 5
description: >
  Build a mkdir-like directory creator with quickli. Learn how to create multiple
  directories in one call using repeatable options and combine multiple path operations.
keywords: [quickli, tutorial, mkdir, directory creator, repeatable options, multiple paths]
---

# Guide 4: Directory Creator (quickmkdir)

This guide builds `quickmkdir`, a minimal `mkdir`-like tool that creates one or more
directories in a single call. It shows how to use a repeatable option to collect multiple
additional paths and how to combine them with the primary argument.

You will learn how to:
- accept a primary path argument alongside **extra paths** via a repeatable option
- validate paths that may not exist yet using `directory_path(exists=None)`
- use `--parents` and `--exist-ok` flags for `mkdir` behavior

## The full example

Save the following file as `quickmkdir.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, directory_path


app = Application(
    name="quickmkdir",
    description="A tiny mkdir-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Print created directories."),
    ],
)


@app.entrypoint(
    help_text="Create one or more directories.",
    arguments=[Argument("path", validators=[directory_path(exists=None)])],
    options=[
        Option(
            "extra",
            short_name="e",
            multiple=True,
            validators=[directory_path(exists=None)],
            help_text="Create additional directories in the same call.",
        ),
        Option("parents", short_name="p", is_flag=True, help_text="Create parent directories."),
        Option("exist-ok", is_flag=True, help_text="Ignore existing directories."),
    ],
)
def create(
    path: Path,
    extra: list[Path] | None = None,
    parents: bool = False,
    exist_ok: bool = False,
    verbose: bool = False,
) -> str:
    paths = [path, *(extra or [])]
    for item in paths:
        item.mkdir(parents=parents, exist_ok=exist_ok)

    if not verbose:
        return "created"

    return "\n".join(f"created: {item}" for item in paths)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

## Run it

```bash
# Create a single directory
python quickmkdir.py new-folder

# Create multiple directories
python quickmkdir.py dist -e logs -e tmp

# Create with parent directories
python quickmkdir.py a/b/c --parents

# Show what was created
python quickmkdir.py output --verbose

# Silently ignore already-existing directories
python quickmkdir.py output --exist-ok
```

## Line-by-line explanation

### Validating paths that may not exist

```python
Argument("path", validators=[directory_path(exists=None)])
```

`directory_path(exists=None)` skips the existence check. The validator only verifies that
the value is a syntactically valid path. This is the right choice here because we are
*creating* the directory — it must not already exist (unless `--exist-ok` is used).

### Collecting multiple paths

```python
Option(
    "extra",
    short_name="e",
    multiple=True,
    validators=[directory_path(exists=None)],
    help_text="Create additional directories in the same call.",
),
```

Passing `multiple=True` accumulates all `--extra` / `-e` values into a list. Each value
is individually validated by `directory_path(exists=None)`.

### Combining paths in the handler

```python
paths = [path, *(extra or [])]
for item in paths:
    item.mkdir(parents=parents, exist_ok=exist_ok)
```

The handler combines the primary path and the extra paths into one list, then creates
each directory. `extra or []` guards against `None` (when no `--extra` values are given).

### Option name with a hyphen

```python
Option("exist-ok", is_flag=True, help_text="Ignore existing directories."),
```

Options with hyphens in their names (`exist-ok`) are accessed in the handler as
underscored parameters (`exist_ok`). quickli converts hyphen-separated names to
underscore-separated parameter names automatically.

## What to try next

- Add a `--mode` option that accepts a Unix permission string (for example `755`) and
  passes it to `Path.mkdir`.
- Read [Guide 5: File Head](./05-building-head-cli.md) for numeric conversion and range
  validation.
