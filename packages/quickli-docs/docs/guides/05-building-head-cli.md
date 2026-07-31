---
id: guide-head-cli
title: "Guide 5: File Head (quickhead)"
sidebar_position: 6
description: >
  Build a head-like file tool with quickli. Learn numeric conversion with converter=int
  and the positive_number validator to restrict option values.
keywords: [quickli, tutorial, head, file head, converter, positive_number, validator]
---

# Guide 5: File Head (quickhead)

This guide builds `quickhead`, a minimal `head`-like tool that prints the first (or last)
lines of a file. It introduces **numeric conversion** with `converter=int` and the built-in
`positive_number` validator.

You will learn how to:
- convert raw option strings to integers with **`converter=int`**
- validate converted values with **`positive_number()`**
- add a tail mode flag to reverse direction

## The full example

Save the following file as `quickhead.py`:

```python
from __future__ import annotations

from pathlib import Path
from sys import argv

from quickli import Application, Argument, Option, file_path, positive_number

app = Application(
    name="quickhead",
    description="A tiny head-like CLI built with quickli.",
)


@app.entrypoint(
    help_text=(
        "Display the first few lines of a file. If no value is given, the first 10 "
        "lines are displayed."
    ),
    arguments=[Argument("file", validators=[file_path()])],
    options=[
        Option(
            "lines",
            short_name="n",
            converter=int,
            validators=[positive_number()],
            help_text="Number of lines to display.",
        ),
        Option(
            "tailmode",
            short_name="t",
            is_flag=True,
            help_text="Display the last few lines instead of the first.",
        ),
    ],
)
def head(file: Path, lines: int = 10, tailmode: bool = False) -> str:
    content = file.read_text(encoding="utf-8").splitlines(keepends=True)
    if tailmode:
        return "".join(content[-lines:])
    return "".join(content[:lines])


if __name__ == "__main__":
    print(app.run(argv[1:]))
```

## Run it

```bash
# Print the first 10 lines (default)
python quickhead.py README.md

# Print the first 5 lines
python quickhead.py README.md --lines 5
python quickhead.py README.md -n 5

# Print the last 3 lines
python quickhead.py README.md -n 3 --tailmode
python quickhead.py README.md -n 3 -t
```

## Line-by-line explanation

### Numeric conversion

```python
Option(
    "lines",
    short_name="n",
    converter=int,
    validators=[positive_number()],
    help_text="Number of lines to display.",
),
```

The command line always delivers raw strings. `converter=int` tells quickli to call
`int()` on the value before passing it to the handler. If the conversion fails (for
example because the user passes `--lines abc`), quickli raises a clear error before the
handler runs.

You can use any callable as a converter — `int`, `float`, `Path`, or your own function.

### The `positive_number` validator

`positive_number()` runs after the converter, so it receives an `int`. It raises a
`ValueError` if the value is not positive (greater than zero). The handler can therefore
assume `lines >= 1`.

### Default value for a converted option

```python
def head(file: Path, lines: int = 10, tailmode: bool = False) -> str:
```

The default value for `lines` is `10`. When the option is absent, the handler receives
`10` directly — no conversion is needed for the default because quickli only runs the
converter for user-supplied values.

### Tail mode

```python
if tailmode:
    return "".join(content[-lines:])
return "".join(content[:lines])
```

Python's negative slice `content[-lines:]` returns the last `lines` elements. This is a
clean way to implement both head and tail in the same handler.

## What to try next

- Add a `--bytes` option that prints the first N bytes instead of lines.
- Read [Guide 6: Multi-Command CLI](./06-multi-command-kubectl.md) for named commands
  and global application options.
