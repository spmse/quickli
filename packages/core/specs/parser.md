# Parser Specification

## Purpose

The parser resource provides explicit JSON, YAML, and TOML loading/rendering helpers for
applications that need structured text input or output.

## Responsibilities

- Render Python data to JSON text.
- Render Python data to YAML text.
- Load JSON text into Python data.
- Load YAML text into Python data.
- Keep each parser function scoped to one data format.

## Technical Notes

- Parsers are stored in `src/quickli/parsers`.
- JSON uses `render_json(...)` and `load_json(...)`.
- YAML uses `render_yaml(...)` and `load_yaml(...)`.
- TOML uses `render_toml(...)` and `load_toml(...)`.
- JSON behavior uses the Python standard library (`json`) with deterministic formatting for
  rendered output.
- YAML behavior is implemented in core without external dependencies.
- TOML loading uses the Python standard library; the built-in renderer supports one level of
  tables.
- The YAML implementation is intentionally minimal and currently supports mappings, sequences,
  and scalar values.
- Each loader raises `ValueError` for invalid input. TOML rendering raises `TypeError` for
  unsupported values or tables deeper than one level.

## Future Extensions

- Extended YAML coverage for additional tags and advanced YAML syntax.
- Optional parser-specific error types.
