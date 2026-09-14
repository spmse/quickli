---
sidebar_position: 7
description: Native TOML configuration file management, validation, and auto-initialization in quiCkLI.
keywords: [quickli, config, toml, schema, ConfigField, ConfigSchema, add_auto_init_config, validate_config, generate_schema_json]
---

# Configuration Files

`quickli` provides native TOML configuration file support through its `config` module. Configuration files exist outside the command token stream, enabling applications to load persistent, schema-validated user settings at startup before commands execute.

```
Application
├── global_options
├── Command
└── Config   ← you are here (loaded at startup, persistent on disk)
```

## Core Resources & API Summary

| Resource / Function | Description |
|---|---|
| `ConfigField` | Describes an expected configuration key, including its type, default, required status, validators, and description. |
| `ConfigSchema` | Container for a list of `ConfigField` definitions that form the application's configuration structure. |
| `Config` | Class managing TOML file reading (`load()`), writing (`save()`), and schema binding at a specified `Path`. |
| `ConfigIssue` | Data object holding validation findings (`severity`, `field`, `message`). |
| `add_auto_init_config` | Helper that auto-creates the TOML file with default values on first run, and loads/validates it on subsequent runs. |
| `validate_config` | Validates a `Config` instance without raising exceptions, returning a list of `ConfigIssue` findings. |
| `generate_schema_json` | Exports a dictionary JSON Schema representation of a `ConfigSchema`. |

## Defining a Configuration Schema

A `ConfigSchema` defines the expected structure of a TOML file:

```python
from quickli import ConfigField, ConfigSchema
from quickli import positive_number, number_range

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, default="127.0.0.1", description="Server bind host."),
        ConfigField("port", value_type=int, default=8080, validators=[number_range(1024, 65535)], description="Port number."),
        ConfigField("timeout", value_type=float, default=30.0, validators=[positive_number], description="Request timeout in seconds."),
        ConfigField("debug", value_type=bool, default=False, description="Enable debug logging."),
    ]
)
```

### ConfigField Attributes

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | Required | Field key name in the TOML file. |
| `value_type` | `type` | `str` | Expected Python type (`str`, `int`, `float`, `bool`, `list`, `dict`). |
| `required` | `bool` | `False` | When `True`, validation fails if the field is missing from the TOML file and has no default. |
| `default` | `Any` | `None` | Default value written during auto-initialization or used as fallback. |
| `validators` | `list[Callable]` | `None` | Callable checks executed against the field value. |
| `description` | `str \| None` | `None` | Field documentation string. |

## Auto-Initialization and Loading (`add_auto_init_config`)

`add_auto_init_config` is the recommended pattern for CLI applications. It ensures the user always has a valid configuration file on disk:

1. **First Run**: If the target TOML file does not exist, `add_auto_init_config` automatically creates parent directories, populates the file with default values, and returns the default data dictionary.
2. **Subsequent Runs**: If the file exists, `add_auto_init_config` loads the TOML file, validates it against the `ConfigSchema`, and returns the validated dictionary.

```python
from pathlib import Path
from quickli import Application, Config, add_auto_init_config

# Path: ~/.config/myapp/config.toml
config_path = Path.home() / ".config" / "myapp" / "config.toml"
config = Config(path=config_path, schema=schema)

# Load configuration with auto-init:
config_data = add_auto_init_config(config)

app = Application(name="myapp")

@app.command(help_text="Start server using loaded config.")
def start() -> str:
    host = config_data.get("host", "127.0.0.1")
    port = config_data.get("port", 8080)
    return f"Server running on {host}:{port}"
```

:::info[Auto-Init Default Values]
Fields marked with `default` values in the schema are written to disk when the configuration file is created for the first time.
:::

## Inspecting Validation Findings (`validate_config`)

If you want to inspect issues without raising exceptions, call `validate_config(config)`:

```python
from quickli import validate_config

issues = validate_config(config)

for issue in issues:
    if issue.severity == "error":
        print(f"❌ [ERROR] Field '{issue.field}': {issue.message}")
    elif issue.severity == "warning":
        print(f"⚠️ [WARNING] Field '{issue.field}': {issue.message}")
```

`validate_config` categorizes issues into:
- **`severity="error"`**: Missing required fields, type mismatches, or validator failures.
- **`severity="warning"`**: Fields present in the user's TOML file that are not defined in the `ConfigSchema`.

## Exporting JSON Schema (`generate_schema_json`)

`quickli` allows exporting a JSON Schema object from a `ConfigSchema` for documentation or integration with external editors:

```python
from quickli import generate_schema_json, render_json

schema_dict = generate_schema_json(schema)
json_str = render_json(schema_dict)
print(json_str)
```

## Error Handling & Exceptions

`quickli` provides dedicated exception types for configuration management, both inheriting from `CLIError`:

| Exception | Cause |
|---|---|
| `ConfigError` | Raised when the configuration file is missing (on direct `load()`), unreadable, or contains invalid TOML syntax. |
| `ConfigValidationError` | Raised when schema validation fails during `config.load()` (e.g. type mismatch or missing required field). |

```python
from quickli import Config, ConfigError, ConfigValidationError

try:
    data = config.load()
except ConfigValidationError as e:
    print(f"Configuration invalid: {e}")
except ConfigError as e:
    print(f"Failed to read configuration file: {e}")
```

## Format Support & Serialization

- **Reading**: Uses standard library `tomllib` (Python 3.11+).
- **Writing**: Built-in serialiser supports scalar types (`str`, `int`, `float`, `bool`), lists, and single-level nested tables (`dict`).
- `None` values are silently omitted during serialization.

:::warning[Serialization Scope]
The built-in TOML writer is designed for scalar fields and shallow dictionary tables. For complex multi-level structures, use **[Parsers](./parsers.md)**.
:::

## Config vs Option Guidelines

:::tip[Choosing Between Config and Option]
- Use **`Config`** for persistent settings that users configure once and expect to remain active across multiple CLI runs (e.g., API keys, server base URLs, or default preferences).
- Use **[Option](./option.md)** for per-invocation flags and overrides (e.g., `--verbose`, `--output=json`, or `--dry-run`).
:::

## Where to Go Next

- Learn how to initialize configuration in application startup scripts in **[Application](./application.md)**.
- Pass runtime option overrides over configuration defaults using **[Option](./option.md)**.
- Parse or format arbitrary TOML, JSON, or YAML strings using **[Parsers](./parsers.md)**.

