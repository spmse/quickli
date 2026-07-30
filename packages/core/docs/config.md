# Configuration Files

quickli provides native support for TOML configuration files.  The configuration
module lets you define expected fields with types and defaults, load and save config
files, validate loaded values, and initialise new files automatically on first run.

## Quick Start

```python
from pathlib import Path

from quickli import (
    Config,
    ConfigField,
    ConfigSchema,
    add_auto_init_config,
    validate_config,
)

schema = ConfigSchema(
    fields=[
        ConfigField(
            "log_level",
            value_type=str,
            required=False,
            default="info",
            help_text="Logging verbosity level.",
        ),
        ConfigField(
            "retries",
            value_type=int,
            required=False,
            default=3,
            help_text="Number of retry attempts.",
        ),
        ConfigField("host", value_type=str, required=True, help_text="Remote host to connect to."),
    ]
)

config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
data = add_auto_init_config(config)

print(data["host"])
```

`add_auto_init_config` creates the file with defaults on first run, or loads it when
the file already exists.

## Resource Model

| Resource              | Purpose                                                             |
| --------------------- | ------------------------------------------------------------------- |
| `ConfigField`         | Describes one expected field: name, type, default, validators       |
| `ConfigSchema`        | A collection of `ConfigField` objects for a complete configuration  |
| `Config`              | Manages loading, saving, and validating a TOML file                 |
| `ConfigIssue`         | A single finding returned by `validate_config`                      |
| `add_auto_init_config`| Creates the file with defaults when absent; loads it when present   |
| `validate_config`     | Reports all issues in a loaded config as a structured list          |

## Defining a Schema

Use `ConfigField` to describe each key the application needs.

```python
from quickli import ConfigField, ConfigSchema, positive_number

schema = ConfigSchema(
    fields=[
        ConfigField(
            "workers",
            value_type=int,
            required=False,
            default=4,
            help_text="Number of parallel workers.",
            validators=[positive_number()],
        ),
        ConfigField(
            "output_dir",
            value_type=str,
            required=True,
            help_text="Directory for output files.",
        ),
    ]
)
```

### `ConfigField` parameters

| Parameter    | Type                      | Default | Description                                        |
| ------------ | ------------------------- | ------- | -------------------------------------------------- |
| `name`       | `str`                     | —       | Key name as it appears in the TOML file            |
| `value_type` | `type`                    | `str`   | Expected Python type after TOML parsing            |
| `required`   | `bool`                    | `True`  | Whether the key must be present                    |
| `default`    | `object`                  | `None`  | Written when the file is first created             |
| `help_text`  | `str`                     | `""`    | Description for documentation or help output       |
| `validators` | `tuple[Validator, ...]`   | `()`    | Optional validators run during validation          |

Supported `value_type` values: `str`, `int`, `float`, `bool`, `list`, `dict`.
Booleans are treated as a distinct type and are never accepted as integers.

### `ConfigSchema` rules

- Field names must be unique.  Duplicate names raise `ValueError` at construction.
- All validators from `quickli.validators` are compatible with `ConfigField.validators`.
- A `ConfigSchema` is optional. `Config` works without one for schema-free use cases.

## Loading a Config File

```python
from quickli import Config, ConfigSchema, ConfigField

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str),
        ConfigField("port", value_type=int),
    ]
)

config = Config(path="app.toml", schema=schema)
data = config.load()
print(data["host"])
```

`Config.load()` raises `ConfigError` when the file is missing or contains invalid
TOML syntax.  When a schema is attached, it also raises `ConfigValidationError` for
missing required fields or type mismatches.

## Saving a Config File

```python
config.save({"host": "example.com", "port": 9000})
```

`Config.save(data)` writes a TOML file at the configured path.  Parent directories
are created automatically.

### Supported value types in `save`

| Python type  | TOML representation             |
| ------------ | ------------------------------- |
| `str`        | Quoted string: `"hello"`        |
| `int`        | Integer: `42`                   |
| `float`      | Float: `3.14`                   |
| `bool`       | `true` or `false`               |
| `list`       | Inline array: `[1, 2, 3]`       |
| `dict`       | Table section: `[section]`      |
| `None`       | Silently skipped                |

Nested tables deeper than one level are not supported by the built-in TOML writer.
Use a flat structure or one level of sections for configuration files.

## Auto-Initialise on First Run

`add_auto_init_config` handles two scenarios transparently:

- **File absent**: creates the file with default values from the schema.
- **File present**: loads and validates the file.

```python
from pathlib import Path
from quickli import Config, ConfigField, ConfigSchema, add_auto_init_config

schema = ConfigSchema(
    fields=[
        ConfigField("log_level", value_type=str, required=False, default="info"),
        ConfigField("retries", value_type=int, required=False, default=3),
    ]
)

config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
data = add_auto_init_config(config)
# First run:  creates file with {"log_level": "info", "retries": 3}
# Later runs: loads the file and returns the stored values
```

Only fields with a non-`None` `default` are written to the new file.  Required
fields without defaults are intentionally excluded so users fill them in manually.

### Using `add_auto_init_config` in a command

You can wire `add_auto_init_config` into a dedicated `config init` command:

```python
from pathlib import Path
from quickli import Application, Config, ConfigField, ConfigSchema, add_auto_init_config

app = Application(name="myapp")

SCHEMA = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, required=False, default="localhost"),
        ConfigField("port", value_type=int, required=False, default=8080),
    ]
)

CONFIG_PATH = Path.home() / ".myapp" / "config.toml"


@app.command(name="config-init", help_text="Create a default configuration file.")
def config_init() -> str:
    config = Config(path=CONFIG_PATH, schema=SCHEMA)
    data = add_auto_init_config(config)
    return f"Configuration ready at {CONFIG_PATH}: {data}"
```

## Validating Configuration

`validate_config` inspects the currently loaded data and returns all issues.  Unlike
`Config.load()`, it never raises—it always returns the complete list so callers can
decide how to report or handle each finding.

```python
from quickli import Config, ConfigField, ConfigSchema, validate_config

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, required=True),
        ConfigField("port", value_type=int, required=True),
    ]
)

config = Config(path="app.toml", schema=schema)
config.load()

issues = validate_config(config)
for issue in issues:
    print(f"[{issue.severity.upper()}] {issue.field}: {issue.message}")
```

### Issue severities

| Severity  | Meaning                                                                 |
| --------- | ----------------------------------------------------------------------- |
| `error`   | Blocking problem: missing required field, wrong type, validator failure |
| `warning` | Non-critical concern: field not defined in the schema (possible typo)   |

`validate_config` returns an empty list when no schema is attached to `config`.

### `ConfigIssue` fields

| Attribute  | Type  | Description                                                  |
| ---------- | ----- | ------------------------------------------------------------ |
| `field`    | `str` | Name of the affected configuration key                       |
| `message`  | `str` | Human-readable description of the problem                    |
| `severity` | `str` | `"error"` or `"warning"`                                     |

## Attaching Validators to Fields

Any callable from `quickli.validators` works as a `ConfigField` validator.

```python
from quickli import ConfigField, number_range, positive_number

ConfigField("workers", value_type=int, validators=[positive_number()])
ConfigField("timeout", value_type=int, validators=[number_range(min_value=1, max_value=300)])
```

Custom validators follow the same contract as CLI validators: raise `ValueError` with
a user-facing message when the value is invalid.

```python
def non_empty_string(value: str) -> str:
    if not value.strip():
        raise ValueError("value must not be blank")
    return value


ConfigField("name", value_type=str, validators=[non_empty_string])
```

## Working with Nested Tables

Save and load nested TOML tables by using a dict value:

```python
config.save(
    {
        "app_name": "myapp",
        "database": {
            "host": "localhost",
            "port": 5432,
        },
    }
)
```

The resulting TOML file:

```toml
app_name = "myapp"

[database]
host = "localhost"
port = 5432
```

Loading nested tables works transparently; the value arrives as a Python `dict`.

## Error Handling

| Exception              | Raised when                                                        |
| ---------------------- | ------------------------------------------------------------------ |
| `ConfigError`          | File missing, unreadable, or contains invalid TOML syntax          |
| `ConfigValidationError`| Required field missing or type mismatch detected during `load`     |

Both exceptions are subclasses of `CLIError`.

```python
from quickli import ConfigError, ConfigValidationError

try:
    data = config.load()
except ConfigValidationError as exc:
    print(f"Fix your config file: {exc}")
except ConfigError as exc:
    print(f"Could not read config file: {exc}")
```

## Full Example

```python
from pathlib import Path

from quickli import (
    Application,
    Config,
    ConfigField,
    ConfigSchema,
    add_auto_init_config,
    number_range,
    positive_number,
    validate_config,
)

SCHEMA = ConfigSchema(
    fields=[
        ConfigField(
            "host",
            value_type=str,
            required=False,
            default="localhost",
            help_text="Remote host.",
        ),
        ConfigField(
            "port",
            value_type=int,
            required=False,
            default=8080,
            help_text="Remote port.",
            validators=[number_range(min_value=1, max_value=65535)],
        ),
        ConfigField(
            "workers",
            value_type=int,
            required=False,
            default=4,
            help_text="Worker count.",
            validators=[positive_number()],
        ),
    ]
)

CONFIG_PATH = Path.home() / ".myapp" / "config.toml"

app = Application(name="myapp", description="An example multi-command app.")


@app.command(name="start", help_text="Start the application.")
def start() -> str:
    config = Config(path=CONFIG_PATH, schema=SCHEMA)
    data = add_auto_init_config(config)

    issues = validate_config(config)
    warnings = [i for i in issues if i.severity == "warning"]
    for w in warnings:
        print(f"[WARNING] {w.field}: {w.message}")

    return f"Starting on {data['host']}:{data['port']} with {data['workers']} workers"


print(app.run(["start"]))
```

## Related

- [Validation](validation.md) for a guide to the built-in validators.
- [Developer Guide](developer-guide.md) for project development rules.
