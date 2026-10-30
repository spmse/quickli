---
sidebar_position: 4
description: Argument describes a required or optional positional input value for a command.
keywords: [quickli, argument, positional, required, optional, converter, validators, metavar, file_path, number_range]
---

# Argument

`Argument` describes a positional input value for a **[Command](./command.md)** or **[Subcommand](./command.md#nested-subcommands)**. Arguments are matched in the fixed order they are declared in the command definition.

```
Application
└── Command
    └── Argument   ← you are here
```

## Argument Properties

When defining an `Argument`, you can configure several properties:

| Property | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | Required | Internal parameter name bound to the handler function signature. |
| `help_text` | `str` | `""` | Description shown in command help output. |
| `required` | `bool` | `True` | Whether the positional argument must be provided. Set `False` explicitly to allow omission. |
| `default` | `Any` | `None` | Fallback value used when an optional positional argument is omitted. |
| `converter` | `Callable` | `str` | Transformation function applied to the raw string token before validation and execution. |
| `validators` | `tuple[Validator, ...]` | `()` | Callables that return the validated value or raise `ValueError`. |
| `metavar` | `str \| None` | `None` | Custom placeholder name displayed in generated usage lines and help listings. |

## Required vs Optional Arguments

Positional arguments are required by default, even if a default is supplied. Set
`required=False` to make one optional; the resource default supplies the omitted value:

```python
from quickli import Application, Argument

app = Application(name="demo")

@app.command(
    help_text="Greet a user with an optional fallback name.",
    arguments=[
        Argument("greeting", help_text="Greeting word."),
        Argument("name", required=False, default="World", help_text="Recipient name."),
    ],
)
def greet(greeting: str, name: str = "World") -> str:
    return f"{greeting}, {name}!"

print(app.run(["greet", "Hello"]))          # Hello, World!
print(app.run(["greet", "Hello", "Alice"]))  # Hello, Alice!
```

:::warning[Positional Argument Ordering]
Arguments are matched sequentially from left to right. Place all required positional arguments *before* any optional positional arguments to ensure deterministic CLI token parsing.
:::

## Type Converters

By default, argument tokens are passed to handlers as raw strings. Pass a `converter` callable (such as `int`, `float`, `Path`, or a custom function) to transform the token automatically:

```python
from pathlib import Path
from quickli import Application, Argument

app = Application(name="demo")

@app.command(
    help_text="Calculate line count for a given file.",
    arguments=[
        Argument("file", converter=Path, help_text="Target file path."),
    ],
)
def count_lines(file: Path) -> str:
    lines = len(file.read_text().splitlines())
    return f"{file.name} has {lines} lines"
```

## Built-in and Custom Validators

`quickli` exports several built-in validator functions that run after type conversion:

- `file_path()`: Creates a validator for an existing file.
- `directory_path()`: Creates a validator for an existing directory.
- `positive_number()`: Creates a validator requiring a numeric value greater than zero.
- `number_range(min_val, max_val)`: Validates that a numeric value lies within `[min_val, max_val]`.

### Example with Built-in Validators

```python
from pathlib import Path
from quickli import Application, Argument
from quickli import file_path, number_range

app = Application(name="demo")

@app.command(
    help_text="Process a target file with a specific thread count.",
    arguments=[
        Argument("path", converter=Path, validators=[file_path()], metavar="FILE"),
        Argument("threads", converter=int, validators=[number_range(1, 16)], metavar="N"),
    ],
)
def process(path: Path, threads: int) -> str:
    return f"Processing {path.name} with {threads} threads"

print(app.run(["process", "README.md", "4"]))
```

### Custom Validator Example

Custom validators must return the value to pass to the next validator or handler,
or raise `ValueError` on failure. Returning `False` replaces the value; it does not reject it:

```python
def validate_even_number(val: int) -> int:
    if val % 2 != 0:
        raise ValueError("Value must be an even integer")
    return val

@app.command(
    arguments=[Argument("amount", converter=int, validators=[validate_even_number])],
)
def split(amount: int) -> str:
    return f"Half is {amount // 2}"
```

:::info[Validator Metadata in Help Text]
Built-in validators enrich command help output automatically by describing expected constraints (e.g. `[1..16]`) alongside the argument description.
:::

## Custom Metavar Formatting

Use `metavar` to customize how the positional argument appears in generated usage strings and help screens:

```python
@app.command(
    arguments=[Argument("target_url", metavar="URL")],
)
def fetch(target_url: str) -> str:
    return f"fetching {target_url}"
```

Generated usage line:
`Usage: demo fetch URL`

## Values that look like options

Use the `--` separator to stop option parsing when a positional value begins with `-`:

```python
from quickli import Application, Argument

app = Application("demo")
app.register(lambda text: text, name="echo", arguments=[Argument("text")])
assert app.run(["echo", "--", "--not-an-option"]) == "--not-an-option"
```

Defaults should already have the desired Python type. Conversion applies to supplied
tokens, not omitted defaults. For example, use `default=4`, not `default="4"`, with
`converter=int`.

## Argument vs Option Guidelines

:::tip[Choosing Between Argument and Option]
- Use an **`Argument`** for the primary **subject** or target of the operation — the core entity the command acts upon (e.g. a source file path, a user ID, or a project name).
- Use an **`Option`** for settings or flags that **modify how** the operation executes (e.g. output format, verbosity level, dry-run toggle, or timeout).

```bash
# Argument: 'main.py' is the subject being executed
quickpython run main.py

# Option: '--debug' and '--output' modify how the execution behaves
quickpython run main.py --debug --output=json
```
:::

## Where to Go Next

- Learn about named inputs and flags in **[Option](./option.md)**.
- See how arguments attach to commands in **[Command](./command.md)**.
- Use **[Parsers](./parsers.md)** inside converters to parse complex string input like JSON or YAML.
