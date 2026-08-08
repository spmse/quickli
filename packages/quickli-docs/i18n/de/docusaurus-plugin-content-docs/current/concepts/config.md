---
sidebar_position: 7
description: Konfigurationsdatei-Unterstützung für quiCkLI-Anwendungen mit TOML.
keywords: [quickli, config, toml, konfiguration, schema, validieren]
---

# Konfigurationsdateien

quickli bietet native Unterstützung für TOML-Konfigurationsdateien über das Modul `config`.
Konfigurationsdateien liegen außerhalb der Befehlshierarchie und werden von der Anwendung
geladen, bevor Befehle ausgeführt werden.

```
Application
├── Command
│   ├── Argument
│   └── Option
└── Config   ← du bist hier (beim Start geladen, nicht Teil des Befehlsbaums)
```

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

## Tipps

:::tip[Config vs. Option für persistente Einstellungen]
Verwende eine **Konfigurationsdatei** für Einstellungen, die Nutzer einmal setzen und
zwischen Ausführungen beibehalten möchten — zum Beispiel einen Standard-Serverhost oder
eine API-Basis-URL. Verwende eine **Befehlsoption** für Einstellungen, die sich pro
Ausführung ändern, etwa das Ausgabeformat oder einen einmaligen Zielpfad.
:::

:::tip[Auto-Init beim ersten Start]
`add_auto_init_config` ist der empfohlene Weg, eine Konfigurationsdatei zu initialisieren.
Beim ersten Start schreibt es eine Datei mit allen Standardwerten, damit der Nutzer einen
konkreten Ausgangspunkt zum Bearbeiten hat. Bei jedem weiteren Start lädt und validiert es
die vorhandene Datei.
:::

## Wie geht es weiter?

- Siehe **[Application](./application.md)**, um zu erfahren, wie Config beim Start integriert wird.
- Siehe **[Parsers](./parsers.md)**, wenn du strukturierte Daten aus Befehlsargumenten statt aus
  einer persistenten Datei lesen möchtest.
