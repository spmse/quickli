# Configuration File Specification

## Purpose

The configuration module provides native TOML configuration file handling for
quickli applications.  It lets application authors define expected fields with
types, defaults, and validators, then manage config files across application
runs.

## Responsibilities

- Describe the expected configuration structure through `ConfigField` and
  `ConfigSchema` resources.
- Load TOML configuration files and validate them against an optional schema.
- Save Python dicts to TOML files.
- Provide `add_auto_init_config` to create default config files on first run.
- Provide `validate_config` to report all issues in a loaded config without
  raising.
- Expose structured `ConfigIssue` objects with severity levels for diagnostic
  use cases.

## Technical Notes

- TOML is the only supported format.  The standard library `tomllib` module
  (Python 3.11+) handles reading.
- Writing uses a minimal built-in TOML serialiser that supports scalars and one
  level of nested tables.  Deep nesting raises `TypeError`.
- Boolean values are treated as a distinct type from integers in type checking
  because `bool` is a subclass of `int` in Python.  A `bool` value is not
  accepted when `value_type=int`, and an `int` value is not accepted when
  `value_type=bool`.
- `None` values are silently omitted from TOML output.
- `ConfigError` and `ConfigValidationError` are subclasses of `CLIError`.
- `Config.load()` raises `ConfigValidationError` for hard errors: missing
  required fields and type mismatches.
- `validate_config()` never raises.  It returns a `list[ConfigIssue]` that
  includes both errors and warnings (e.g. unrecognised fields).
- The resource must remain dependency-free beyond the standard library.
- The implementation is compatible with Python 3.12 to 3.14.

## Resources

### `ConfigField`

| Property     | Type                    | Description                                |
| ------------ | ----------------------- | ------------------------------------------ |
| `name`       | `str`                   | Field name in the TOML file                |
| `value_type` | `type`                  | Expected Python type                       |
| `required`   | `bool`                  | Whether absence is a hard error            |
| `default`    | `object`                | Default written on first-run init          |
| `help_text`  | `str`                   | Human-readable description                 |
| `validators` | `tuple[Validator, ...]` | Post-type-check constraints                |

Names are stripped at construction.  An empty name raises `ValueError`.

### `ConfigSchema`

| Property      | Type                     | Description                     |
| ------------- | ------------------------ | ------------------------------- |
| `fields`      | `tuple[ConfigField, ...]`| Ordered list of field contracts |
| `field_names` | `frozenset[str]`         | Set of all defined field names  |

Duplicate field names raise `ValueError` at construction.

`ConfigSchema.validate(data)` returns a `list[str]` of error messages.  It does
not raise.

### `Config`

| Property | Type              | Description                          |
| -------- | ----------------- | ------------------------------------ |
| `path`   | `Path`            | Resolved configuration file path     |
| `schema` | `ConfigSchema`    | Attached schema, or `None`           |
| `data`   | `dict[str,object]`| Copy of the currently loaded values  |

Methods:

| Method              | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `load()`            | Reads the file, validates against schema, returns data        |
| `save(data)`        | Serialises data and writes the file                           |

### `ConfigIssue`

| Attribute  | Type  | Description                                        |
| ---------- | ----- | -------------------------------------------------- |
| `field`    | `str` | Name of the affected key, or `""` for schema-level |
| `message`  | `str` | Human-readable description                         |
| `severity` | `str` | `"error"` or `"warning"`                           |

## Validation Contract

`validate_config(config)` produces issues in the following cases:

| Condition                                | Severity   |
| ---------------------------------------- | ---------- |
| Required field absent, no default        | `error`    |
| Field value has wrong type               | `error`    |
| Field value fails an attached validator  | `error`    |
| Key present but not in schema            | `warning`  |

An absent optional field with a default is not reported.

## Error Contract

| Exception              | Condition                                                    |
| ---------------------- | ------------------------------------------------------------ |
| `ConfigError`          | File missing, unreadable, or invalid TOML syntax             |
| `ConfigValidationError`| `load()` discovers required field missing or type mismatch   |

## TOML Serialisation Rules

- `bool` is serialised before `int` to prevent Python's `bool`/`int` overlap.
- `None` values are skipped.
- `dict` values become TOML table headers (`[section]`).
- Lists must contain only scalar values.
- Tables deeper than one level raise `TypeError`.
- Every output file ends with a trailing newline.

## Future Extensions

- Support TOML array-of-tables for list-of-sections configuration.
- Support configurable config file search paths (XDG, platform defaults).
- Provide a merge utility for layered configuration (file + env + CLI overrides).
- Expose schema-generated documentation for configuration reference pages.
