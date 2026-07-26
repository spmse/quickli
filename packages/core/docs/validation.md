# Validation

quickli validates CLI input after conversion and before the handler is called.

This keeps handlers focused on application behavior instead of repetitive checks such as
"does this file exist?" or "is this number positive?".

## Validation Flow

The input pipeline is:

1. quickli reads raw command-line text.
2. A `converter` transforms the raw value when one is configured.
3. Each validator checks the converted value.
4. quickli passes the validated value to the handler.

That order matters.

- Use converters for shape changes such as `str -> int` or `str -> Path`.
- Use validators for business or domain rules such as "must be positive" or
  "must point to an existing file".

## Attach Validators To Arguments

```python
from pathlib import Path

from quickli import Application, Argument, file_path

app = Application(name="reader")


@app.entrypoint(arguments=[Argument("source", converter=Path, validators=[file_path()])])
def read(source: Path) -> str:
    return source.read_text(encoding="utf-8")
```

You can also omit the explicit `Path` converter because `file_path()` already returns a
`Path` object.

```python
from pathlib import Path

from quickli import Application, Argument, file_path

app = Application(name="reader")


@app.entrypoint(arguments=[Argument("source", validators=[file_path()])])
def read(source: Path) -> str:
    return source.read_text(encoding="utf-8")
```

## Attach Validators To Options

```python
from quickli import Application, Option, positive_number

app = Application(name="head")


@app.entrypoint(options=[Option("lines", short_name="n", converter=int,
                               validators=[positive_number()], default=10)])
def show(lines: int) -> str:
    return f"showing {lines} lines"
```

This pattern is useful for optional numeric parameters, file destinations, and output
format switches that accept restricted values.

## Built-In Validators

quickli currently ships with four built-in validators.

### `file_path()`

Use `file_path()` when the input must refer to a file path.

```python
from quickli import Argument, file_path

Argument("source", validators=[file_path()])
```

Behavior:

- returns a `Path` object
- rejects non-file paths
- can require an existing path, a missing path, or skip the existence check

Configuration:

```python
file_path()
file_path(exists=True)
file_path(exists=False)
file_path(exists=None)
```

Use cases:

- `exists=True`: input file that must already exist
- `exists=False`: output file path that must not exist yet
- `exists=None`: file-shaped path without an existence requirement

### `directory_path()`

Use `directory_path()` when the input must refer to a directory path.

```python
from quickli import Argument, directory_path

Argument("target", validators=[directory_path()])
```

Behavior:

- returns a `Path` object
- rejects non-directory paths
- supports the same `exists=True`, `exists=False`, and `exists=None` options

Typical use cases:

- reading an existing directory
- validating a directory creation target
- accepting a directory-shaped path before later creation

### `positive_number()`

Use `positive_number()` when a numeric value must be greater than zero.

```python
from quickli import Option, positive_number

Option("count", short_name="n", converter=int, validators=[positive_number()])
```

This works with converted integers and floats.

### `number_range(min_value=..., max_value=...)`

Use `number_range(...)` when a numeric value must stay inside an inclusive range.

```python
from quickli import Option, number_range

Option(
    "limit",
    short_name="l",
    converter=int,
    validators=[number_range(min_value=1, max_value=100)],
)
```

You may provide only one boundary.

```python
number_range(min_value=1)
number_range(max_value=100)
```

## Defaults Are Also Validated

quickli validates default values too.

That means a misconfigured option default fails early instead of silently introducing an
invalid state.

```python
Option("lines", short_name="n", converter=int, validators=[positive_number()], default=10)
```

If the default were `0`, quickli would reject it because it does not satisfy the validator.

## Validators In Generated Help

Validators can contribute metadata to generated help text.

For example, a file validator can communicate that an argument expects a file path, and a
numeric range validator can expose the accepted bounds.

This makes the CLI more self-descriptive without extra manual help text.

## Reusable Custom Validators

For application-specific rules, use a small callable that raises `ValueError` when the
value is invalid.

```python
def non_empty_slug(value: str) -> str:
    if not value or " " in value:
        raise ValueError("slug must not be empty or contain spaces")
    return value
```

Then attach it like any other validator.

```python
from quickli import Argument

Argument("slug", validators=[non_empty_slug])
```

Practical guidance:

- keep validators small and focused
- raise `ValueError` with a clear user-facing message
- prefer validators over manual checks inside the handler when the rule belongs to input
  validation

## When To Use Conversion Versus Validation

Use conversion when the CLI value must become another Python type.

- `int`
- `float`
- `Path`

Use validation when the type is already correct but the value must satisfy extra rules.

- positive integer
- existing file
- directory path that must not exist yet
- range-limited numeric option

Combine both when needed.

```python
Option(
    "lines",
    short_name="n",
    converter=int,
    validators=[number_range(min_value=1, max_value=200)],
)
```

## Related Examples

- `examples/simple/cat-cli` uses `file_path()` for file input.
- `examples/simple/ls-cli` uses `directory_path()` for directory input.
- `examples/simple/mkdir-cli` uses `directory_path(exists=None)` for a directory creation target.
- `examples/simple/quickhead` uses `file_path()` and `positive_number()` together.
- `examples/complex/pyk5l` combines `file_path()` and `positive_number()` in a multi-command app.