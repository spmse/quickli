---
sidebar_position: 7
---

# Konfigurationsdateien

quickli bietet native Unterstützung für TOML-Konfigurationsdateien über das Modul `config`.

## Ressourcen

- `ConfigField` — beschreibt einen erwarteten Schlüssel mit Typ, optionalem Standardwert und Validatoren.
- `ConfigSchema` — eine Sammlung von `ConfigField`-Objekten, die die erwartete Struktur definiert.
- `Config` — verwaltet das Lesen und Schreiben einer TOML-Datei an einem angegebenen Pfad.
- `ConfigIssue` — ein strukturiertes Ergebnis, das von `validate_config` zurückgegeben wird.
- `add_auto_init_config` — erstellt beim ersten Start eine Standarddatei und lädt sie bei späteren Starts.
- `validate_config` — gibt alle Probleme einer geladenen Konfiguration zurück, ohne eine Ausnahme auszulösen.

## Ein Schema definieren

```python
from quickli import ConfigField, ConfigSchema

schema = ConfigSchema(
    fields=[
        ConfigField("host", value_type=str, required=False, default="localhost"),
        ConfigField("port", value_type=int, required=False, default=8080),
    ]
)
```

## Laden und automatische Initialisierung

```python
from pathlib import Path
from quickli import Config, add_auto_init_config

config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
data = add_auto_init_config(config)
# First run:  writes defaults to file, returns {"host": "localhost", "port": 8080}
# Later runs: loads and validates the existing file
```

## Konfiguration validieren

```python
from quickli import validate_config

issues = validate_config(config)
for issue in issues:
    print(f"[{issue.severity.upper()}] {issue.field}: {issue.message}")
```

`validate_config` gibt Folgendes zurück:

- **Fehler** bei fehlenden erforderlichen Feldern, Typabweichungen und fehlgeschlagenen Validatoren.
- **Warnungen** bei Feldern, die in der Datei vorhanden, aber im Schema nicht definiert sind.

## Fehlerbehandlung

| Ausnahme | Wann sie ausgelöst wird |
| --- | --- |
| `ConfigError` | Datei fehlt, ist nicht lesbar oder enthält ungültige TOML-Syntax |
| `ConfigValidationError` | Erforderliches Feld fehlt oder Typ stimmt beim Aufruf von `load()` nicht |

Beide sind Unterklassen von `CLIError`.

## Formatunterstützung

- **Lesen**: verwendet `tomllib` aus der Python-Standardbibliothek (Python 3.11+).
- **Schreiben**: verwendet einen integrierten Serialisierer für Skalare und verschachtelte Tabellen auf einer Ebene.
- `None`-Werte werden beim Schreiben stillschweigend übersprungen.
