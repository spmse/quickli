---
sidebar_position: 7
---

# Parser

`quickli.parsers` bietet klar abgegrenzte Funktionen für strukturierte JSON-, YAML- und TOML-Ein- und -Ausgabe.

## Öffentliche APIs

- `load_json(text)` und `render_json(value)`
- `load_yaml(text)` und `render_yaml(value)`
- `load_toml(text)` und `render_toml(value)`

## Beispiel

```python
from quickli import load_yaml, render_json

data = load_yaml("kind: Pod\nmetadata:\n  name: web-preview\n")
print(render_json(data))
```
