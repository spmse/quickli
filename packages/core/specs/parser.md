# Parser Specification

## Purpose

The parser resource provides minimal JSON and YAML loading/rendering helpers for applications
that need structured text input or output.

## Responsibilities

- Render Python data to JSON text.
- Render Python data to YAML text.
- Load JSON text into Python data.
- Load YAML text into Python data.
- Provide a single JSON-or-YAML entrypoint for each direction.

## Technical Notes

- Parsers are stored in `src/quickli/parsers`.
- The API entrypoints are `core_json_or_yaml_rendering(...)` and
  `core_json_or_yaml_loading(...)`.
- JSON behavior uses the Python standard library (`json`) with deterministic formatting for
  rendered output.
- YAML behavior is implemented in core without external dependencies.
- The YAML implementation is intentionally minimal and currently supports mappings, sequences,
  and scalar values.
- Unsupported format names raise `ValueError`.

## Future Extensions

- Extended YAML coverage for additional tags and advanced YAML syntax.
- Optional parser-specific error types.
