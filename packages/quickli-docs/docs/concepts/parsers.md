---
sidebar_position: 7
---

# Parsers

`quickli.parsers` provides explicit helpers for structured JSON, YAML, and TOML input and output.

## Public APIs

- `load_json(text)` and `render_json(value)`
- `load_yaml(text)` and `render_yaml(value)`
- `load_toml(text)` and `render_toml(value)`

## Example

```python
from quickli import load_yaml, render_json

data = load_yaml("kind: Pod\nmetadata:\n  name: web-preview\n")
print(render_json(data))
```
