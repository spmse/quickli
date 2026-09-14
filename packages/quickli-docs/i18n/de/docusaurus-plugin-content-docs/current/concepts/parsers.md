---
sidebar_position: 8
description: Hilfsfunktionen zur Serialisierung und Deserialisierung strukturierter Daten (JSON, YAML, TOML) in quiCkLI.
keywords: [quickli, parsers, json, yaml, toml, load_json, render_json, load_yaml, render_yaml, load_toml, render_toml]
---

# Parsers

`quickli.parsers` bietet Hilfsfunktionen zum Parsen und Rendern strukturierter Daten in den Formaten **JSON**, **YAML** und **TOML**. Parser sind zustandslose Hilfsfunktionen außerhalb der Befehlshierarchie — du kannst sie in **[Command](./command.md)**-Handlern, Konvertern für **[Argument](./argument.md#typ-konverter)** oder Datenverarbeitungspipelines aufrufen.

```
Application
└── Command
    └── handler()   ← Parser-Helfer in Handlern oder Konvertern aufrufen
        load_json / render_yaml / load_toml / …
```

## Öffentliche API-Referenz

Alle Parser-Helfer werden direkt aus dem Hauptpaket `quickli` re-exportiert:

| Funktion | Signatur | Beschreibung |
|---|---|---|
| `load_json` | `(text: str) -> Any` | Parst einen JSON-String in Python-Dictionaries/Listen. |
| `render_json` | `(value: Any) -> str` | Serialisiert Python-Datenstrukturen in einen formatierten JSON-String. |
| `load_yaml` | `(text: str) -> Any` | Parst einen YAML-String in Python-Dictionaries/Listen. |
| `render_yaml` | `(value: Any) -> str` | Serialisiert Python-Datenstrukturen in einen formatierten YAML-String. |
| `load_toml` | `(text: str) -> Any` | Parst einen TOML-String in Python-Dictionaries/Listen. |
| `render_toml` | `(value: Any) -> str` | Serialisiert Python-Datenstrukturen in einen formatierten TOML-String. |

:::info[Top-Level Modul-Export]
Du kannst alle Parser-Helfer direkt aus `quickli` importieren (z. B. `from quickli import load_json, render_yaml`).
:::

## Beispiel 1: Format-Konvertierungs-Befehl (YAML zu JSON)

Kombiniere `load_yaml` und `render_json`, um Konvertierungstools zu bauen:

```python
from pathlib import Path
from quickli import Application, Argument, load_yaml, render_json

app = Application(name="yaml2json")

@app.command(
    help_text="Eine YAML-Datei in formatiertes JSON umwandeln.",
    arguments=[Argument("path", converter=Path)],
)
def convert(path: Path) -> str:
    raw_yaml = path.read_text(encoding="utf-8")
    data = load_yaml(raw_yaml)
    return render_json(data)
```

## Beispiel 2: Argument-Konvertierung mit `load_json`

Verwende `load_json` als Konverter für `Argument` oder `Option`, um JSON-Strings auf der CLI zu parsen:

```python
from quickli import Application, Argument, load_json

app = Application(name="demo")

@app.command(
    help_text="JSON-Payload prüfen.",
    arguments=[
        Argument("payload", converter=load_json, help_text="Roher JSON-String."),
    ],
)
def inspect_payload(payload: dict) -> str:
    keys = ", ".join(payload.keys())
    return f"Payload contains {len(payload)} keys: {keys}"

print(app.run(["inspect-payload", '{"name": "Alice", "role": "admin"}']))
```

## Beispiel 3: Ausgaben basierend auf Optionen formatieren

Verwende Parser-Renderer, um Handler-Antworten dynamisch basierend auf einer `--format`-Option zu formatieren:

```python
from quickli import Application, Option
from quickli import render_json, render_yaml, render_toml

app = Application(name="demo")

@app.command(
    options=[
        Option("format", short_name="f", default="json", help_text="Ausgabeformat (json, yaml, toml)."),
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

## Leitfaden zur Formatauswahl

:::tip[Wahl des richtigen Formats]
- **JSON**: Optimal für Maschinen-zu-Maschinen-Kommunikation und API-Payloads.
- **YAML**: Optimal für menschlich lesbare Konfigurationen und Kubernetes-Manifeste.
- **TOML**: Optimal für menschlich bearbeitbare Anwendungskonfigurationsdateien.
:::

## Parsers vs. Konfigurationsmodul

:::note[Parsers vs. Config]
- Verwende **`parsers`**-Helfer für einmaliges Parsen oder Rendern beliebiger JSON/YAML/TOML-Strings oder Dateien innerhalb der Befehlslogik.
- Verwende **[Config](./config.md)**, wenn du eine dauerhafte, schema-validierte TOML-Konfigurationsdatei auf der Festplatte benötigst.
:::

## Wie geht es weiter?

- Erfahre mehr über Konverter in positionalen Eingaben in **[Argument](./argument.md)**.
- Erfahre mehr über CLI-Optionen in **[Option](./option.md)**.
- Siehe, wie dauerhafte TOML-Konfiguration funktioniert in **[Config](./config.md)**.

