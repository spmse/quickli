---
sidebar_position: 8
description: Helpers for parsing and rendering JSON, YAML, and TOML in quiCkLI CLIs.
keywords: [quickli, parsers, json, yaml, toml, load, render]
---

# Parsers

`quickli.parsers` provides explicit helpers for structured JSON, YAML, and TOML input and
output. Parsers are utility functions that sit outside the command hierarchy — you can call
them from any command handler that needs to read or produce structured data.

```
Application
└── Command
    └── handler()   ← call parser helpers from here
        load_yaml / render_json / …
```

## Public APIs

| Function | Description |
|---|---|
| `load_json(text)` | Parse a JSON string into a Python object |
| `render_json(value)` | Serialise a Python object to a JSON string |
| `load_yaml(text)` | Parse a YAML string into a Python object |
| `render_yaml(value)` | Serialise a Python object to a YAML string |
| `load_toml(text)` | Parse a TOML string into a Python object |
| `render_toml(value)` | Serialise a Python object to a TOML string |

## Convert between formats

```python
from quickli import load_yaml, render_json

data = load_yaml("kind: Pod\nmetadata:\n  name: web-preview\n")
print(render_json(data))
```

## Read structured input from an argument

```python
from pathlib import Path
from quickli import Application, Argument, load_json

app = Application(name="demo")


@app.command(
    help_text="Summarise a JSON file.",
    arguments=[Argument("path", converter=Path)],
)
def summarise(path: Path) -> str:
    data = load_json(path.read_text())
    return f"{len(data)} top-level keys"


print(app.run(["summarise", "data.json"]))
```

## Tips

:::tip[Which format to choose]
- Use **JSON** for machine-to-machine data and API responses.
- Use **YAML** for human-edited configuration and Kubernetes-style manifests.
- Use **TOML** for end-user configuration files (see [Configuration Files](./config.md)).

All three helpers are available from the top-level `quickli` import, so you do not need
to import `quickli.parsers` directly.
:::

:::tip[Parsers vs. Config]
`load_toml` / `render_toml` are useful for one-off parsing of TOML strings or files that
you manage yourself. For persistent application configuration with schema validation and
auto-initialisation, use the dedicated [Config](./config.md) resources instead.
:::

## Where to go next

- See **[Configuration Files](./config.md)** for persistent, schema-validated config.
- Go back to **[Command](./command.md)** to see how to wire parser helpers into a handler.
