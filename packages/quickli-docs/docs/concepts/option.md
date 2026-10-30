---
sidebar_position: 5
description: Option describes a named, order-independent input that modifies command or application behavior.
keywords: [quickli, option, flag, short alias, combined flags, repeatable, global options, local options, validators]
---

# Option

`Option` describes a named, order-independent input that modifies how a command or application behaves. Options can be **local** to a specific **[Command](./command.md)** or **global** across the entire **[Application](./application.md)**.

```
Application
├── global_options   ← available to every command (e.g. --verbose, --config)
└── Command
    └── Option       ← local option (you are here)
```

## Option Properties

When creating an `Option`, you can configure the following properties:

| Property | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | Required | Option name, accessed via CLI flags like `--output` and handler parameters like `output`. |
| `help_text` | `str` | `""` | Human-readable explanation rendered in help output. |
| `short_name` | `str \| None` | `None` | Single-character short alias (e.g., `"o"` for `-o`). |
| `required` | `bool` | `False` | Whether the option must be explicitly supplied by the caller. |
| `default` | `Any` | `None` | Default value if the option is omitted. (Default for `is_flag=True` is `False`). |
| `is_flag` | `bool` | `False` | When `True`, treats the option as a boolean toggle switch that takes no value argument. |
| `converter` | `Callable` | `str` | Transformation callable applied to supplied values before validation. |
| `validators` | `tuple[Validator, ...]` | `()` | Callables returning the validated value or raising `ValueError`. |
| `multiple` | `bool` | `False` | When `True`, allows the option to be repeated on the command line. |

Option destinations replace hyphens with underscores: `Option("dry-run", is_flag=True)`
passes `dry_run=True` to the handler. `metavar` belongs to `Argument`, not `Option`.

## Supported CLI Syntax Forms

`quickli` supports standard POSIX and GNU CLI option syntax out of the box:

- **Long option with space**: `--output out.json`
- **Long option with equal sign**: `--output=out.json`
- **Short option with space**: `-o out.json`
- **Combined short flags**: `-vxf` (equivalent to `-v -x -f` when all short options are boolean flags)

## Boolean Flags vs Value Options

### Value Option Example

```python
from quickli import Application, Option

app = Application(name="demo")

@app.command(
    options=[Option("output", short_name="o", default="out.txt")],
)
def export_data(output: str = "out.txt") -> str:
    return f"saving to {output}"

print(app.run(["export-data", "--output", "report.pdf"]))  # saving to report.pdf
print(app.run(["export-data", "-o", "report.pdf"]))        # saving to report.pdf
print(app.run(["export-data", "--output=report.pdf"]))    # saving to report.pdf
```

### Boolean Flag Example

```python
@app.command(
    options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable debug mode."),
    ],
)
def status(verbose: bool = False) -> str:
    return "Status: OK (debug enabled)" if verbose else "Status: OK"

print(app.run(["status"]))             # Status: OK
print(app.run(["status", "--verbose"])) # Status: OK (debug enabled)
print(app.run(["status", "-v"]))       # Status: OK (debug enabled)
```

:::info[Combined Short Flags]
When multiple single-character boolean flags are passed together (e.g., `-abc`), `quickli` splits them into individual flags (`-a`, `-b`, `-c`), provided all short options in the cluster are registered as flags (`is_flag=True`).
:::

## Repeatable Options (`multiple=True`)

`Option` supports two distinct types of repeatable behavior:

### 1. Repeatable Value Options (Lists)

When `multiple=True` on a value option (`is_flag=False`), repeated invocations accumulate converted values in a Python `list`:

```python
@app.command(
    options=[
        Option("tag", short_name="t", multiple=True, help_text="Add tag label."),
    ],
)
def tag_item(tag: list[str] | None = None) -> str:
    tags = tag or []
    return f"Applied tags: {', '.join(tags)}"

print(app.run(["tag-item", "--tag", "web", "-t", "v1.0", "--tag", "prod"]))
# Returns: Applied tags: web, v1.0, prod
```

### 2. Repeatable Flag Options (Occurrence Counts)

When `multiple=True` on a boolean flag (`is_flag=True`), repeated flags accumulate an integer occurrence count (e.g. `-v`, `-vv`, `-v -v -v`):

```python
@app.command(
    options=[
        Option("verbose", short_name="v", is_flag=True, multiple=True),
    ],
)
def run_job(verbose: int = 0) -> str:
    return f"Log verbosity level: {verbose}"

print(app.run(["run-job", "-v"]))     # Log verbosity level: 1
print(app.run(["run-job", "-vvv"]))   # Log verbosity level: 3
```

:::warning[Repeatable Flag Return Types]
A standard flag (`is_flag=True`, `multiple=False`) returns a `bool`. A repeatable flag (`is_flag=True`, `multiple=True`) returns an `int` representing the occurrence count. Make sure your handler function type hint matches the expected return type.
:::

:::note[Defaults and repeated values]
- A value option normally defaults to `None`; repeatable values default to a fresh `[]`.
- Repeatable values append to any configured list default, rather than replacing it.
- Supplied tokens are converted; defaults must already have the desired Python type.
- A non-repeatable option keeps its last supplied value.
- Flags take no value: `--verbose=false` is an error, not a way to turn a flag off.
:::

## Global and Local Options

Options can be registered as **local** options on a command or **global** options on the application:

```python
app = Application(
    name="demo",
    global_options=[
        Option("config", short_name="c", help_text="Path to config file."),
        Option("quiet", short_name="q", is_flag=True, help_text="Suppress output."),
    ],
)

@app.command(
    options=[
        Option("format", short_name="f", default="json", help_text="Local format option."),
    ],
)
def process(format: str = "json", config: str | None = None, quiet: bool = False) -> str:
    return f"format={format}, config={config}, quiet={quiet}"

# Global options can be placed BEFORE or AFTER the command name:
print(app.run(["--config", "settings.toml", "process", "-f", "yaml"]))
print(app.run(["process", "-f", "yaml", "--config", "settings.toml", "-q"]))
```

:::note[Global Option Placement]
`quickli` filters global options flexibly regardless of whether the user places them before the command name (`mycli -q process`) or after the command name (`mycli process -q`).
Every selected handler must accept all global option destinations or `**kwargs`.
Do not reuse a global destination on a local option.
:::

## Converters and Built-in Validators

Options support type conversion and validation in the same way as **[Argument](./argument.md)**:

```python
from pathlib import Path
from quickli import Application, Option
from quickli import file_path, positive_number

app = Application(name="demo")

@app.command(
    options=[
        Option(
            "file",
            short_name="f",
            converter=Path,
            validators=[file_path()],
            help_text="Input file path.",
        ),
        Option(
            "retries",
            short_name="r",
            converter=int,
            validators=[positive_number()],
            default=3,
            help_text="Retry count.",
        ),
    ],
)
def sync(file: Path | None = None, retries: int = 3) -> str:
    file_name = file.name if file else "none"
    return f"Syncing {file_name} with max {retries} retries"
```

## Where to Go Next

- Contrast options with positional input in **[Argument](./argument.md)**.
- See how options are attached to command handlers in **[Command](./command.md)**.
- Learn how application-wide global options are configured in **[Application](./application.md)**.
- Store persistent settings on disk instead of per-run options using **[Config](./config.md)**.
