---
sidebar_position: 7
description: YAML, JSON, and TOML configuration, custom schemas, and initialization in quiCkLI.
keywords: [quickli, config, toml, schema, ConfigField, ConfigSchema, add_auto_init_config, validate_config, generate_schema_json]
---

# Configuration Files

`quickli` manages persistent YAML, JSON, and TOML settings through `Config`. YAML is the
default for unknown extensions. A `ConfigSchema` describes your application's keys;
it is independent of CLI arguments and options.

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
| `Config` | Manages YAML, JSON, or TOML reading (`load()`), writing (`save()`), and schema binding. |
| `ConfigIssue` | Data object holding validation findings (`severity`, `field`, `message`). |
| `add_auto_init_config` | Creates defaults when the file is absent; otherwise loads and validates it. |
| `validate_config` | Validates a `Config` instance without raising exceptions, returning a list of `ConfigIssue` findings. |
| `generate_schema_json` | Exports a dictionary JSON Schema representation of a `ConfigSchema`. |

## Defining a Configuration Schema

A `ConfigSchema` defines top-level keys and their Python types:

```python
from quickli import ConfigField, ConfigSchema
from quickli import positive_number, number_range

schema = ConfigSchema(
    fields=[
        ConfigField("host", default="127.0.0.1", help_text="Server bind host."),
        ConfigField(
            "port", value_type=int, default=8080,
            validators=[number_range(1024, 65535)], help_text="Port number.",
        ),
        ConfigField(
            "timeout", value_type=float, default=30.0,
            validators=[positive_number()], help_text="Request timeout in seconds.",
        ),
        ConfigField("debug", value_type=bool, default=False, help_text="Enable debug logging."),
    ]
)
```

### ConfigField Attributes

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | Required | Top-level field key in the file. |
| `value_type` | `type` | `str` | Expected Python type (`str`, `int`, `float`, `bool`, `list`, `dict`). |
| `required` | `bool` | `True` | Missing keys fail validation unless a non-`None` default exists. |
| `default` | `object` | `None` | Value written during initialization, not merged during loading. |
| `validators` | `tuple[Validator, ...]` | `()` | Checks executed against present, correctly typed values. |
| `help_text` | `str` | `""` | Field documentation included in generated JSON Schema. |

:::important[Defaults are not a merge policy]
`load()` returns only the keys present in the file. For example, use
`data.get("port", 8080)` for an explicit fallback. Initialization writes non-`None`
defaults but leaves required fields without defaults for the user to fill in.
`save()` does not validate the schema; `load()` does.
:::

## Application initialization: automatic command or explicit routine

Pass one `Config` object to the application. It carries the path, schema, and format together:

```python
from pathlib import Path
from quickli import Application, Config, ConfigField, ConfigSchema, Option

schema = ConfigSchema(fields=[
    ConfigField("host", default="localhost"),
    ConfigField("port", value_type=int, default=8080),
    ConfigField(
        "service", value_type=dict,
        default={"labels": ["development"], "enabled": True},
    ),
])
config = Config(Path.home() / ".mytool" / "settings.json", schema=schema)
app = Application("mytool", config=config, auto_init_config=True)

@app.command(options=[Option("port", converter=int)])
def serve(port: int | None = None) -> str:
    data = config.load()
    effective_port = port if port is not None else data.get("port", 8080)
    return f"{data['host']}:{effective_port}"

if __name__ == "__main__":
    raise SystemExit(app.main())
```

1. Save the example as `mytool.py`.
2. Run `python mytool.py init` to create the custom structure.
3. Edit the JSON file, then run `python mytool.py serve`.
4. Run `python mytool.py serve --port 9000` for an explicit, per-invocation override.

The generated JSON includes nested values:

```json
{
  "host": "localhost",
  "port": 8080,
  "service": {"labels": ["development"], "enabled": true}
}
```

For YAML, use `settings.yaml` or `Config("settings.conf", schema=schema, format="yaml")`:

```yaml
host: localhost
port: 8080
service:
  labels:
    - development
  enabled: true
```

:::note[Initialization is opt-in]
`auto_init_config=True` registers an `init` command; it does not create files during
construction, help rendering, or other commands. It requires `config=...` and reserves
the command name `init`. Re-running it loads the existing file without overwriting it.
Invalid existing files raise an error instead of being reset.
:::

When automatic command registration is disabled (the default), call the same routine explicitly:

```python
manual_app = Application("mytool", config=config)
data = manual_app.init_config()
```

You may call this from startup code or a custom `config-init` handler. Without an attached
configuration, `init_config()` raises `ConfigError`. No global configuration singleton or
automatic file/environment/CLI precedence is introduced.

:::tip[Nested validation]
`ConfigField("service", value_type=dict)` checks the outer type, not nested keys.
Use a custom validator that raises `ValueError` to check inner structure. JSON Schema
export describes top-level types and defaults, not arbitrary validator constraints.
:::

## Auto-Initialization and Loading (`add_auto_init_config`)

Use the standalone helper when you do not want configuration attached to `Application`:

1. **First run**: Create parent directories, write fields with defaults, and return them.
2. **Subsequent runs**: Load and validate the existing file, preserving user changes.

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

`validate_config(config)` inspects the data already held in memory; it does not read the file.
If `load()` reports schema errors, the parsed data remains available for diagnostics:

```python
from quickli import ConfigValidationError, validate_config

try:
    config.load()
except ConfigValidationError:
    pass

issues = validate_config(config)

for issue in issues:
    if issue.severity == "error":
        print(f"❌ [ERROR] Field '{issue.field}': {issue.message}")
    elif issue.severity == "warning":
        print(f"⚠️ [WARNING] Field '{issue.field}': {issue.message}")
```

`validate_config` categorizes issues into:
- **`severity="error"`**: Missing required fields, type mismatches, or validator failures.
- **`severity="warning"`**: Top-level keys not defined in the `ConfigSchema`.

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
| `ConfigError` | Missing/unreadable file, invalid encoding or syntax, invalid document shape, or write failure. |
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

- **YAML** (`.yaml`, `.yml`): PyYAML safe loading and dumping; nested mappings and lists.
- **JSON** (`.json`): Standard-library `json`; nested objects and arrays.
- **TOML** (`.toml`): Standard-library `tomllib` reading and a shallow built-in writer.
- Explicit `format="yaml"`, `"json"`, or `"toml"` overrides the extension; other formats
  raise `ValueError`.
- Configuration roots must be mappings with string keys, not lists or scalars. Empty/null
  YAML documents load as `{}`; JSON `null` is not a configuration object.
- Top-level `None` values are omitted when writing. Nested nulls are retained by JSON/YAML.
- Files use UTF-8. Quote YAML strings such as `"on"` or date-like values when they must
  remain strings; PyYAML applies YAML scalar conversion.

:::warning[Serialization Scope]
The built-in TOML writer supports scalar values, scalar lists, and one table level.
Use YAML or JSON for deeply nested configuration.
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
