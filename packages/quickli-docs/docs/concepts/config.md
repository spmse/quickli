---
sidebar_position: 7
description: Configuration file support for quiCkLI applications using TOML.
keywords: [quickli, config, toml, configuration, schema, validate]
---

# Configuration Files

`quickli` provides native TOML configuration file support through the `config` module.
Configuration files sit outside the command hierarchy and are loaded by the application
before commands run.

```
Application
├── Command
│   ├── Argument
│   └── Option
└── Config   ← you are here (loaded at startup, not part of the command tree)
```

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

## Tips

:::tip[Config vs. Option for persistent settings]
Use a **config file** for settings that users set once and expect to persist between
runs — for example, a default server host or an API base URL. Use a **command option**
for settings that change on a per-invocation basis, such as the output format or a
one-off target path.
:::

:::tip[Auto-init on first run]
`add_auto_init_config` is the recommended way to initialise a config file. It writes a
file with all default values on the first run so the user has a concrete starting point
to edit. On every subsequent run it loads and validates the existing file.
:::

## Where to go next

- See **[Application](./application.md)** for how to integrate config loading at startup.
- See **[Parsers](./parsers.md)** if you need to parse structured data from command arguments
  rather than from a persistent file.
