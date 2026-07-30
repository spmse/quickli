# ADR 0002: Native TOML Configuration File Handling

## Status

Accepted

## Context

quickli is a minimal CLI framework.  As applications grow, they often need to
persist settings between runs rather than repeating the same options on every
invocation.  A native configuration mechanism keeps this pattern within the
framework and avoids forcing application authors to write boilerplate for every
project.

The design must stay dependency-free, work with Python 3.12 to 3.14, and fit
naturally alongside the existing `Argument`, `Option`, and `Validator` resources.

Key questions that shaped the decision:

1. Which file format should the config module support?
2. How should the module report validation problems?
3. How should first-run initialisation work?

## Decision

quickli implements a dedicated `config` module with the following resources:

- `ConfigField` — describes one expected key with a type, default, and validators.
- `ConfigSchema` — collects fields into a reusable contract.
- `Config` — manages loading and saving a single TOML file.
- `ConfigIssue` — a structured finding with a severity level.
- `add_auto_init_config` — creates a default file on first run; loads otherwise.
- `validate_config` — returns all issues without raising.

The module uses `tomllib` (stdlib, Python 3.11+) for reading and a minimal
built-in serialiser for writing.

## Options Considered

### Format: TOML

Benefits:

- TOML is the standard format for Python project configuration (`pyproject.toml`).
- `tomllib` ships with Python 3.11+ and requires no external dependency.
- TOML is human-readable and supports types (string, int, float, bool, list, table)
  natively, removing the need for string-to-type conversion.

Risks:

- Writing TOML requires a custom serialiser because `tomllib` is read-only.
- The custom serialiser is limited to one level of nesting.

### Format: JSON

Benefits:

- `json` is fully supported in the standard library for both reading and writing.
- Round-trip fidelity is trivial.

Risks:

- JSON lacks comments and is considered less ergonomic for hand-edited config files.
- Python projects do not conventionally use JSON for user-facing configuration.

### Format: INI / configparser

Benefits:

- `configparser` is stdlib and supports both reading and writing.
- Familiar format for many users.

Risks:

- Limited type support (everything is a string).
- No native support for nested structures.
- Less consistent with modern Python tooling.

### Validation: Raise on Load vs. Return Issues

Two approaches were considered:

**Option A: Raise `ConfigValidationError` on every problem found.**

Benefits:

- Fail-fast behaviour prevents partially-configured applications from starting.

Risks:

- Only the first error is reported, forcing multiple read-fix-run cycles.
- Unsuitable for diagnostic tools or config check commands that want a full list.

**Option B: Return a list of issues; raise only for hard errors.**

Benefits:

- `validate_config` returns the complete list of findings in one call.
- `Config.load()` still raises for blocking problems (missing required fields,
  type mismatches), preserving fail-fast behaviour for startup code.
- Application authors can decide how to present warnings and informational messages.

Decision: **Option B**.  `Config.load()` raises for hard errors, and `validate_config`
returns the complete list of issues without raising.

### First-Run Init: Separate Command vs. Integrated Helper

**Option A: Application authors write their own init logic.**

Benefits:

- Complete flexibility.

Risks:

- Boilerplate in every project that needs configuration.

**Option B: Provide `add_auto_init_config` as a reusable helper.**

Benefits:

- Reduces boilerplate.
- Behaviour is consistent across applications.
- Can be wired into startup code or a dedicated `config init` command.

Decision: **Option B**.  `add_auto_init_config` covers the common case and remains
small enough to understand at a glance.

## Consequences

Positive consequences:

- Applications can manage TOML config files without external dependencies.
- Validation is schema-driven and consistent with the existing `Validator` system.
- `validate_config` supports diagnostic and check-command use cases.
- `add_auto_init_config` removes boilerplate for the first-run creation pattern.

Tradeoffs:

- The built-in TOML writer is limited to one level of nested tables.
  Applications with deeply nested configuration must either flatten their schema
  or handle TOML writing themselves.
- Type checking for `bool` fields requires special-casing because `bool` is a
  subclass of `int` in Python.

Follow-up:

- A future release could add support for layered configuration
  (file + environment variables + CLI options).
- XDG base directory and platform-specific config paths could be offered as
  optional helpers.
