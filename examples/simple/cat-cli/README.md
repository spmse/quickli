# Build a cat CLI with quickli

This example packages both the guide and the runnable source code in the same directory.

Files in this example:

- `quickcat.py`: runnable example application
- `README.md`: explanation of the resource setup and example commands

## Goal

The example demonstrates:

- one global flag option
- one required file path argument
- local options for encoding and line numbering
- one repeatable local option for extra file paths
- built-in file path validation

## Run the example

From the repository root:

```bash
PYTHONPATH=src python examples/simple/cat-cli/quickcat.py README.md
PYTHONPATH=src python examples/simple/cat-cli/quickcat.py --verbose README.md --number
PYTHONPATH=src python examples/simple/cat-cli/quickcat.py README.md --include docs/usage.md
```

## Code Layout

See `quickcat.py` in the same folder for the runnable implementation.

The example uses:

- a commandless application through `@app.entrypoint(...)`
- a global `--verbose` flag
- one required validated file argument
- one repeatable validated file option
- local options for encoding and numbering

## Resource mapping

- `Application` owns the root entrypoint and the global `--verbose` option.
- `Argument("path", validators=[file_path()])` models the required input file.
- `Option("include", validators=[file_path()], multiple=True)` validates extra input files.
- Local `Option` resources model `--encoding`, `--number`, and repeatable `--include`.

## Notes about the parser

- Global options are parsed before or after the root-level arguments.
- Local options are parsed on the application entrypoint.
- Repeatable non-flag options return lists.
- Repeatable flags return integer counts.

## Validation notes

- The example does not manually check `Path.exists()`.
- `file_path()` performs the existence and file-type check before the handler runs.
- The handler receives ready-to-use `Path` objects.