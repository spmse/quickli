---
sidebar_position: 7
description: Native TOML-Konfigurationsdateiverwaltung, Validierung und Auto-Initialisierung in quiCkLI.
keywords: [quickli, config, toml, schema, ConfigField, ConfigSchema, add_auto_init_config, validate_config, generate_schema_json]
---

# Konfigurationsdateien

`quickli` bietet native TOML-Konfigurationsdateiverwaltung über sein `config`-Modul. Konfigurationsdateien liegen außerhalb des Befehls-Token-Streams und ermöglichen es Anwendungen, dauerhafte, schema-validierte Benutzereinstellungen beim Anwendungsstart zu laden.

```
Application
├── global_options
├── Command
└── Config   ← du bist hier (beim Start geladen, dauerhaft auf der Festplatte)
```

## Kernressourcen & API-Übersicht

| Ressource / Funktion | Beschreibung |
|---|---|
| `ConfigField` | Beschreibt einen erwarteten Schlüssel mit Typ, Standardwert, Erforderlich-Status, Validatoren und Beschreibung. |
| `ConfigSchema` | Container für eine Liste von `ConfigField`-Definitionen. |
| `Config` | Klasse zum Lesen (`load()`), Schreiben (`save()`) und Schema-Binden einer TOML-Datei an einem angegebenen `Path`. |
| `ConfigIssue` | Datenobjekt für Validierungsergebnisse (`severity`, `field`, `message`). |
| `add_auto_init_config` | Hilfsfunktion, die die TOML-Datei beim ersten Start mit Standardwerten anlegt und bei späteren Starts lädt. |
| `validate_config` | Validiert eine `Config`-Instanz ohne Ausnahmen auszulösen und gibt eine Liste von `ConfigIssue`-Befunden zurück. |
| `generate_schema_json` | Exportiert eine JSON-Schema-Wörterbuchdarstellung eines `ConfigSchema`. |

## Definieren eines Konfigurationsschemas

Ein `ConfigSchema` definiert die erwartete Struktur einer TOML-Datei:

```python
from quickli import ConfigField, ConfigSchema
from quickli import positive_number, number_range

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, default="127.0.0.1", description="Server-Bind-Host."),
        ConfigField("port", value_type=int, default=8080, validators=[number_range(1024, 65535)], description="Portnummer."),
        ConfigField("timeout", value_type=float, default=30.0, validators=[positive_number], description="Timeout in Sekunden."),
        ConfigField("debug", value_type=bool, default=False, description="Debug-Logging aktivieren."),
    ]
)
```

### ConfigField-Attribute

| Parameter | Typ | Standard | Beschreibung |
|---|---|---|---|
| `name` | `str` | Erforderlich | Feldname in der TOML-Datei. |
| `value_type` | `type` | `str` | Erwarteter Python-Typ (`str`, `int`, `float`, `bool`, `list`, `dict`). |
| `required` | `bool` | `False` | Bei `True` schlägt die Validierung fehl, wenn das Feld in der Datei fehlt und keinen Standardwert hat. |
| `default` | `Any` | `None` | Standardwert, der bei Auto-Initialisierung geschrieben oder als Ersatz verwendet wird. |
| `validators` | `list[Callable]` | `None` | Prüffunktionen, die auf den Feldwert angewendet werden. |
| `description` | `str \| None` | `None` | Beschreibung des Feldes. |

## Auto-Initialisierung und Laden (`add_auto_init_config`)

`add_auto_init_config` ist das empfohlene Muster für CLI-Anwendungen:

1. **Erster Start**: Existiert die Datei nicht, erstellt `add_auto_init_config` Ordner und Datei mit Standardwerten und gibt diese zurück.
2. **Spätere Starts**: Existiert die Datei, lädt und validiert `add_auto_init_config` die TOML-Datei.

```python
from pathlib import Path
from quickli import Application, Config, add_auto_init_config

config_path = Path.home() / ".config" / "myapp" / "config.toml"
config = Config(path=config_path, schema=schema)

config_data = add_auto_init_config(config)

app = Application(name="myapp")

@app.command(help_text="Server starten.")
def start() -> str:
    host = config_data.get("host", "127.0.0.1")
    port = config_data.get("port", 8080)
    return f"Server running on {host}:{port}"
```

:::info[Standardwerte bei Auto-Init]
Felder mit definierten `default`-Werten werden beim ersten Erstellen der Datei auf die Festplatte geschrieben.
:::

## Überprüfen von Validierungsergebnissen (`validate_config`)

Möchtest du Ergebnisse ohne Ausnahmen prüfen, rufe `validate_config(config)` auf:

```python
from quickli import validate_config

issues = validate_config(config)

for issue in issues:
    if issue.severity == "error":
        print(f"❌ [ERROR] Field '{issue.field}': {issue.message}")
    elif issue.severity == "warning":
        print(f"⚠️ [WARNING] Field '{issue.field}': {issue.message}")
```

`validate_config` unterscheidet:
- **`severity="error"`**: Fehlende erforderliche Felder, Typabweichungen oder Validierungsfehler.
- **`severity="warning"`**: Felder in der Datei, die nicht im `ConfigSchema` definiert sind.

## Exportieren von JSON-Schema (`generate_schema_json`)

`quickli` erlaubt den Export einer JSON-Schema-Darstellung aus einem `ConfigSchema`:

```python
from quickli import generate_schema_json, render_json

schema_dict = generate_schema_json(schema)
json_str = render_json(schema_dict)
print(json_str)
```

## Fehlerbehandlung & Ausnahmen

| Ausnahme | Ursache |
|---|---|
| `ConfigError` | Wird ausgelöst, wenn die Datei fehlt (bei direktem `load()`), unlesbar ist oder ungültige TOML-Syntax enthält. |
| `ConfigValidationError` | Wird ausgelöst, wenn die Schemavalidierung bei `config.load()` fehlschlägt. |

```python
from quickli import Config, ConfigError, ConfigValidationError

try:
    data = config.load()
except ConfigValidationError as e:
    print(f"Configuration invalid: {e}")
except ConfigError as e:
    print(f"Failed to read configuration file: {e}")
```

## Formatunterstützung & Serialisierung

- **Lesen**: Verwendet `tomllib` aus der Standardbibliothek (Python 3.11+).
- **Schreiben**: Unterstützt Skalare (`str`, `int`, `float`, `bool`), Listen und verschachtelte Tabellen auf einer Ebene (`dict`).
- `None`-Werte werden beim Schreiben übersprungen.

:::warning[Serialisierungsumfang]
Der integrierte TOML-Writer ist für skalare Felder und flache Tabellen ausgelegt. Für komplexe Strukturen verwende **[Parsers](./parsers.md)**.
:::

## Leitfaden: Config vs. Option

:::tip[Entscheidung zwischen Config und Option]
- Verwende **`Config`** für permanente Einstellungen, die Benutzer einmal festlegen (z. B. API-Keys oder Standard-Server-URLs).
- Verwende **[Option](./option.md)** für ausführungsspezifische Flags und Overrides (z. B. `--verbose` oder `--dry-run`).
:::

## Wie geht es weiter?

- Erfahre mehr über die Anwendungs-Integration in **[Application](./application.md)**.
- Überschreibe Konfigurationswerte dynamisch mit **[Option](./option.md)**.
- Verarbeite beliebige JSON-, YAML- oder TOML-Strings mit **[Parsers](./parsers.md)**.

