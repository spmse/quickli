---
sidebar_position: 7
---

# Configuration Files

quickli provides native TOML configuration file support through the `config` module.

## Resources

- `ConfigField` — describes one expected key with a type, optional default, and validators.
- `ConfigSchema` — a collection of `ConfigField` objects that define the expected structure.
- `Config` — manages reading and writing a TOML file at a given path.
- `ConfigIssue` — a structured finding returned by `validate_config`.
- `add_auto_init_config` — creates a default file on first run; loads it on subsequent runs.
- `validate_config` — returns all issues in a loaded config without raising.

## Defining a schema

```python
from quickli import ConfigField, ConfigSchema

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, required=False, default="localhost"),
        ConfigField("port", value_type=int, required=False, default=8080),
    ]
)
```

## Loading and auto-initialising

```python
from pathlib import Path
from quickli import Config, add_auto_init_config

config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
data = add_auto_init_config(config)
# First run:  writes defaults to file, returns {"host": "localhost", "port": 8080}
# Later runs: loads and validates the existing file
```

## Validating configuration

```python
from quickli import validate_config

issues = validate_config(config)
for issue in issues:
    print(f"[{issue.severity.upper()}] {issue.field}: {issue.message}")
```

`validate_config` returns:

- **errors** for missing required fields, type mismatches, and validator failures.
- **warnings** for fields present in the file but not defined in the schema.

## Error handling

| Exception               | When raised                                          |
| ----------------------- | ---------------------------------------------------- |
| `ConfigError`           | File missing, unreadable, or invalid TOML syntax     |
| `ConfigValidationError` | Required field missing or type mismatch on `load()`  |

Both are subclasses of `CLIError`.

## Format support

- **Reading**: uses `tomllib` from the Python standard library (Python 3.11+).
- **Writing**: uses a built-in serialiser for scalars and one level of nested tables.
- `None` values are silently skipped when writing.
