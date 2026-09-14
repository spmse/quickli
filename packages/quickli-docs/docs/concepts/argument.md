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
| `help_text` | `str \| None` | `None` | Description shown in command help output. |
| `required` | `bool` | `True` | Whether the positional argument must be provided. Automatically `False` if `default` is given. |
| `default` | `Any` | `None` | Fallback value used when an optional positional argument is omitted. |
| `converter` | `Callable \| None` | `None` | Transformation function applied to the raw string token before validation and execution. |
| `validators` | `list[Callable] \| None` | `None` | Callable checks executed against the converted value. |
| `metavar` | `str \| None` | `None` | Custom placeholder name displayed in generated usage lines and help listings. |

## Required vs Optional Arguments

Positional arguments are **required** by default. They become **optional** when a `default` value is provided:

```python
from quickli import Application, Argument

app = Application(name="demo")

@app.command(
    help_text="Greet a user with an optional fallback name.",
    arguments=[
        Argument("greeting", help_text="Greeting word."),
        Argument("name", default="World", help_text="Recipient name."),
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

- `file_path`: Validates that the path exists and is an existing file.
- `directory_path`: Validates that the path exists and is an existing directory.
- `positive_number`: Validates that a numeric value is strictly greater than 0.
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
        Argument("path", converter=Path, validators=[file_path], metavar="FILE"),
        Argument("threads", converter=int, validators=[number_range(1, 16)], metavar="N"),
    ],
)
def process(path: Path, threads: int) -> str:
    return f"Processing {path.name} with {threads} threads"

print(app.run(["process", "README.md", "4"]))
```

### Custom Validator Example

You can also provide custom validator callables that raise an error or return `False` when validation fails:

```python
def validate_even_number(val: int) -> bool:
    if val % 2 != 0:
        raise ValueError("Value must be an even integer")
    return True

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

