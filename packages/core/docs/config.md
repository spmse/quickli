# Configuration Files

quiCkLI provides native support for configuration files.  YAML is the recommended
and default format; JSON and TOML are also supported.  The configuration module lets
you define expected fields with types and defaults, load and save config files,
validate loaded values, generate a JSON Schema for editor support, and initialise
new files automatically on first run.

## Supported Formats

| Format | Extensions         | Recommendation                  |
| ------ | ------------------ | ------------------------------- |
| YAML   | `.yaml`, `.yml`    | **Recommended default**         |
| JSON   | `.json`            | Supported                       |
| TOML   | `.toml`            | Supported (legacy)              |

The format is inferred automatically from the file extension.  Use `.yaml` for new
projects.  You can override the format with the `format` parameter if needed.

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

config = Config(path=Path.home() / ".myapp" / "config.yaml", schema=schema)
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
| `Config`              | Manages loading, saving, and validating a config file               |
| `ConfigIssue`         | A single finding returned by `validate_config`                      |
| `add_auto_init_config`| Creates the file with defaults when absent; loads it when present   |
| `validate_config`     | Reports all issues in a loaded config as a structured list          |
| `generate_schema_json`| Generates a JSON Schema dict from a `ConfigSchema`                  |

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
| `name`       | `str`                     | —       | Key name as it appears in the config file          |
| `value_type` | `type`                    | `str`   | Expected Python type after parsing                 |
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

config = Config(path="app.yaml", schema=schema)
data = config.load()
print(data["host"])
```

`Config.load()` raises `ConfigError` when the file is missing or contains invalid
syntax.  When a schema is attached, it also raises `ConfigValidationError` for
missing required fields or type mismatches.

### Using a different format

Pass `format` explicitly to override the inferred format:

```python
config = Config(path="app.cfg", schema=schema, format="yaml")
```

## Saving a Config File

```python
config.save({"host": "example.com", "port": 9000})
```

`Config.save(data)` writes a config file at the configured path.  Parent directories
are created automatically.  `None` values are silently skipped.

### Supported value types

| Python type  | YAML              | JSON          | TOML                      |
| ------------ | ----------------- | ------------- | ------------------------- |
| `str`        | `host: example`   | `"example"`   | `host = "example"`        |
| `int`        | `port: 9000`      | `9000`        | `port = 9000`             |
| `float`      | `ratio: 1.5`      | `1.5`         | `ratio = 1.5`             |
| `bool`       | `debug: true`     | `true`        | `debug = true`            |
| `list`       | `- a\n- b`        | `["a","b"]`   | `tags = ["a", "b"]`       |
| `dict`       | nested mapping    | nested object | `[section]` table         |
| `None`       | skipped           | skipped       | skipped                   |

> **Note for TOML**: nested tables deeper than one level are not supported by the
> built-in writer.  Use YAML or JSON for deeply nested configuration.

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

config = Config(path=Path.home() / ".myapp" / "config.yaml", schema=schema)
data = add_auto_init_config(config)
# First run:  creates file with {"log_level": "info", "retries": 3}
# Later runs: loads the file and returns the stored values
```

Only fields with a non-`None` `default` are written to the new file.  Required
fields without defaults are intentionally excluded so users fill them in manually.

### Using `add_auto_init_config` in a command

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

CONFIG_PATH = Path.home() / ".myapp" / "config.yaml"


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

config = Config(path="app.yaml", schema=schema)
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

## Generating a JSON Schema

Use `generate_schema_json` to produce a JSON Schema document from a `ConfigSchema`.
This is useful for editor auto-completion, CI validation, or documentation tools.

```python
import json
from pathlib import Path

from quickli import ConfigField, ConfigSchema, generate_schema_json

schema = ConfigSchema(
    fields=[
        ConfigField(
            "host",
            value_type=str,
            required=True,
            help_text="Remote host to connect to.",
        ),
        ConfigField(
            "port",
            value_type=int,
            required=False,
            default=8080,
            help_text="TCP port number.",
        ),
    ]
)

schema_dict = generate_schema_json(schema, title="MyApp Configuration")
Path("schema.json").write_text(json.dumps(schema_dict, indent=2))
```

The generated `schema.json` looks like:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "MyApp Configuration",
  "properties": {
    "host": {
      "type": "string",
      "description": "Remote host to connect to."
    },
    "port": {
      "type": "integer",
      "description": "TCP port number.",
      "default": 8080
    }
  },
  "required": ["host"]
}
```

### `generate_schema_json` parameters

| Parameter     | Type           | Default | Description                                       |
| ------------- | -------------- | ------- | ------------------------------------------------- |
| `schema`      | `ConfigSchema` | —       | The schema to convert                             |
| `title`       | `str`          | `""`    | Optional title for the generated schema           |
| `description` | `str`          | `""`    | Optional description for the generated schema     |

### Type mapping

| Python type | JSON Schema type |
| ----------- | ---------------- |
| `str`       | `"string"`       |
| `int`       | `"integer"`      |
| `float`     | `"number"`       |
| `bool`      | `"boolean"`      |
| `list`      | `"array"`        |
| `dict`      | `"object"`       |

### Wiring into a command

You can expose schema generation as a CLI command:

```python
import json
from pathlib import Path
from quickli import Application, ConfigField, ConfigSchema, generate_schema_json

app = Application(name="myapp")

SCHEMA = ConfigSchema(
    fields=[
        ConfigField(
            "host", value_type=str, required=False, default="localhost", help_text="Remote host."
        ),
        ConfigField("port", value_type=int, required=False, default=8080, help_text="TCP port."),
    ]
)


@app.command(name="config-schema", help_text="Write configuration schema to schema.json.")
def config_schema() -> str:
    output = Path("schema.json")
    output.write_text(json.dumps(generate_schema_json(SCHEMA, title="myapp"), indent=2))
    return f"Schema written to {output}"
```

## Working with Nested Tables (YAML)

YAML handles nested structures naturally:

```yaml
# config.yaml
app_name: myapp
database:
  host: localhost
  port: 5432
```

```python
config = Config(path="config.yaml")
data = config.load()
print(data["database"]["host"])  # "localhost"
```

Saving nested dicts works in all formats:

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

## Error Handling

| Exception              | Raised when                                                        |
| ---------------------- | ------------------------------------------------------------------ |
| `ConfigError`          | File missing, unreadable, or contains invalid syntax               |
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

CONFIG_PATH = Path.home() / ".myapp" / "config.yaml"

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
