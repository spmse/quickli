# Build a head CLI with quickli

This example shows a small `head`-style program implemented with `quickli`.

Files in this example:

- `app.py`: runnable example application
- `README.md`: guide and validation notes

## Why this example matters

The example demonstrates the validation layer directly.

- `Argument("file", validators=[file_path()])` validates that the input exists.
- The validator also converts the value to `Path`.
- `Option("lines", validators=[positive_number()])` rejects zero and negative values.
- The handler can focus on reading lines instead of checking whether the file exists.

## Run the example

From the repository root:

```bash
PYTHONPATH=src python examples/simple/quickhead/app.py AGENTS.md
PYTHONPATH=src python examples/simple/quickhead/app.py AGENTS.md -n 5
PYTHONPATH=src python examples/simple/quickhead/app.py AGENTS.md -t -n 25
```

## Validation behavior

- Existing files are accepted.
- Missing files fail before the handler is called.
- Directories are rejected because the validator expects a file path.
- `--lines` must be a positive number.

## Help behavior

- Validator metadata appears in generated help output.
- The example can rely on generated help instead of manually documenting file and number constraints in the handler.