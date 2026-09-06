---
sidebar_position: 8
description: Structured data serialization and deserialization helpers (JSON, YAML, TOML) in quiCkLI.
keywords: [quickli, parsers, json, yaml, toml, load_json, render_json, load_yaml, render_yaml, load_toml, render_toml]
---

# Parsers

`quickli.parsers` provides utility functions for parsing and rendering structured data in **JSON**, **YAML**, and **TOML** formats. Parsers are stateless utility functions that exist outside the command token hierarchy — you can invoke them inside **[Command](./command.md)** handlers, argument/option **[Argument](./argument.md#type-converters)** converters, or data processing pipelines.

```
Application
└── Command
    └── handler()   ← call parser helpers inside handlers or converters
        load_json / render_yaml / load_toml / …
```

## Public API Reference

All parser helpers are exported directly from top-level `quickli`:

| Function | Signature | Description |
|---|---|---|
| `load_json` | `(text: str) -> Any` | Parses a JSON string into Python dictionaries/lists. |
| `render_json` | `(value: Any) -> str` | Serializes Python data structures into a formatted JSON string. |
| `load_yaml` | `(text: str) -> Any` | Parses a YAML string into Python dictionaries/lists. |
| `render_yaml` | `(value: Any) -> str` | Serializes Python data structures into a formatted YAML string. |
| `load_toml` | `(text: str) -> Any` | Parses a TOML string into Python dictionaries/lists. |
| `render_toml` | `(value: Any) -> str` | Serializes Python data structures into a formatted TOML string. |

:::info[Top-Level Module Export]
You can import all parser helpers directly from `quickli` (e.g. `from quickli import load_json, render_yaml`). Importing from `quickli.parsers` is also supported.
:::

## Example 1: Format Conversion Command (YAML to JSON)

You can combine `load_yaml` and `render_json` to build format conversion tools:

```python
from pathlib import Path
from quickli import Application, Argument, load_yaml, render_json

app = Application(name="yaml2json")

@app.command(
    help_text="Convert a YAML file to formatted JSON.",
    arguments=[Argument("path", converter=Path)],
)
def convert(path: Path) -> str:
    raw_yaml = path.read_text(encoding="utf-8")
    data = load_yaml(raw_yaml)
    return render_json(data)

# Usage: yaml2json convert manifest.yaml
```

## Example 2: Argument Conversion with `load_json`

Use `load_json` as an `Argument` or `Option` converter to parse JSON strings passed on the CLI:

```python
from quickli import Application, Argument, load_json

app = Application(name="demo")

@app.command(
    help_text="Inspect JSON payload keys.",
    arguments=[
        Argument("payload", converter=load_json, help_text="Raw JSON string."),
    ],
)
def inspect_payload(payload: dict) -> str:
    keys = ", ".join(payload.keys())
    return f"Payload contains {len(payload)} keys: {keys}"

print(app.run(["inspect-payload", '{"name": "Alice", "role": "admin"}']))
# Returns: Payload contains 2 keys: name, role
```

## Example 3: Formatting Command Output Based on Option

Use parser renderers to format handler responses dynamically based on a user `--format` option:

```python
from quickli import Application, Option
from quickli import render_json, render_yaml, render_toml

app = Application(name="demo")

@app.command(
    options=[
        Option("format", short_name="f", default="json", help_text="Output format (json, yaml, toml)."),
    ],
)
def info(format: str = "json") -> str:
    data = {
        "app": "demo",
        "status": "healthy",
        "metrics": {"cpu": 12.5, "memory_mb": 256},
    }
    if format == "yaml":
        return render_yaml(data)
    elif format == "toml":
        return render_toml(data)
    return render_json(data)

print(app.run(["info", "-f", "yaml"]))
```

## Format Selection Guide

:::tip[Choosing the Right Format]
- **JSON**: Best for machine-to-machine interaction, API payloads, and automated script pipelines.
- **YAML**: Best for human-readable configurations and Kubernetes-style manifest files.
- **TOML**: Best for human-editable application configuration files and project settings.
:::

## Parsers vs Configuration Module

:::note[Parsers vs Config]
- Use **`parsers`** helpers for one-off parsing or rendering of arbitrary JSON/YAML/TOML strings or files inside command logic.
- Use **[Config](./config.md)** when you need a persistent, schema-validated TOML configuration file on disk with default fallback generation (`add_auto_init_config`).
:::

## Where to Go Next

- Learn how to integrate converters into positional input in **[Argument](./argument.md)**.
- Learn how to format CLI options in **[Option](./option.md)**.
- See how persistent TOML configuration works in **[Config](./config.md)**.

