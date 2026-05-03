# Build an ls CLI with quickli

This example shows a small `ls`-style program implemented with `quickli`.

Files in this example:

- `quickls.py`: runnable example application
- `README.md`: guide and command overview

## Features

- one optional directory argument
- one local flag for hidden files
- one repeatable local suffix filter
- one global verbose flag
- built-in directory path validation

## Run the example

From the repository root:

```bash
PYTHONPATH=src python examples/simple/ls-cli/quickls.py
PYTHONPATH=src python examples/simple/ls-cli/quickls.py docs --all
PYTHONPATH=src python examples/simple/ls-cli/quickls.py . --suffix .md --suffix .toml --verbose
```

## Notes

- `Argument("path", validators=[directory_path()])` validates the directory and returns `Path`.
- `Option("suffix", multiple=True)` collects multiple suffix filters.
- `--verbose` is global and can appear before or after the positional arguments.
- The handler can safely call `iterdir()` because validation already checked the path.
- The example uses a commandless application entrypoint instead of a named subcommand.