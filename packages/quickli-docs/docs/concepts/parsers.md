---
sidebar_position: 7
---

# Parsers

`quickli.parsers` provides dependency-light helpers for structured JSON/YAML input and output.

## Public APIs

- `core_json_or_yaml_loading(text, format_name=None)`
- `core_json_or_yaml_rendering(value, format_name="json")`

## Example

```python
from quickli import core_json_or_yaml_loading, core_json_or_yaml_rendering

data = core_json_or_yaml_loading("kind: Pod\nmetadata:\n  name: web-preview\n")
print(core_json_or_yaml_rendering(data, format_name="json"))
```

When `format_name` is omitted during loading, quickli detects JSON payloads that begin with
`{` or `[` and otherwise parses as YAML.
