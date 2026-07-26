# Build a mkdir CLI with quickli

This example shows a small `mkdir`-style program implemented with `quickli`.

Files in this example:

- `quickmkdir.py`: runnable example application
- `README.md`: guide and command overview

## Features

- one required directory argument
- one repeatable local option for additional paths
- local flags for `parents` and `exist-ok`
- one global verbose flag
- built-in directory path validation for creation targets

## Run the example

From the repository root:

```bash
PYTHONPATH=src python examples/simple/mkdir-cli/quickmkdir.py sandbox
PYTHONPATH=src python examples/simple/mkdir-cli/quickmkdir.py sandbox --parents --exist-ok
PYTHONPATH=src python examples/simple/mkdir-cli/quickmkdir.py --verbose sandbox --extra sandbox/logs --extra sandbox/data
```

## Notes

- `Argument("path", validators=[directory_path(exists=None)])` accepts missing paths but rejects existing files.
- `Option("extra", multiple=True, validators=[directory_path(exists=None)])` applies the same rule to extra directories.
- `--verbose` is global and can appear before or after the positional arguments.
- The handler can focus on `mkdir()` instead of checking whether an existing path is a file.
- The example uses a commandless application entrypoint instead of a named subcommand.