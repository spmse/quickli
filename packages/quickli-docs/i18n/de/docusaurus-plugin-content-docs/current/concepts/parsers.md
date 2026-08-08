---
sidebar_position: 8
description: Helfer zum Parsen und Rendern von JSON, YAML und TOML in quiCkLI-CLIs.
keywords: [quickli, parser, json, yaml, toml, laden, rendern]
---

# Parser

`quickli.parsers` bietet klar abgegrenzte Funktionen für strukturierte JSON-, YAML- und
TOML-Ein- und -Ausgabe. Parser sind Hilfsfunktionen außerhalb der Befehlshierarchie — du
kannst sie aus jedem Command-Handler aufrufen, der strukturierte Daten lesen oder erzeugen
muss.

```
Application
└── Command
    └── handler()   ← Parser-Helfer hier aufrufen
        load_yaml / render_json / …
```

## Öffentliche APIs

| Funktion | Beschreibung |
|---|---|
| `load_json(text)` | Einen JSON-String in ein Python-Objekt parsen |
| `render_json(value)` | Ein Python-Objekt in einen JSON-String serialisieren |
| `load_yaml(text)` | Einen YAML-String in ein Python-Objekt parsen |
| `render_yaml(value)` | Ein Python-Objekt in einen YAML-String serialisieren |
| `load_toml(text)` | Einen TOML-String in ein Python-Objekt parsen |
| `render_toml(value)` | Ein Python-Objekt in einen TOML-String serialisieren |

## Zwischen Formaten konvertieren

```python
from quickli import load_yaml, render_json

data = load_yaml("kind: Pod\nmetadata:\n  name: web-preview\n")
print(render_json(data))
```

## Strukturierte Eingabe aus einem Argument lesen

```python
from pathlib import Path
from quickli import Application, Argument, load_json

app = Application(name="demo")


@app.command(
    help_text="Eine JSON-Datei zusammenfassen.",
    arguments=[Argument("path", converter=Path)],
)
def summarise(path: Path) -> str:
    data = load_json(path.read_text())
    return f"{len(data)} Schlüssel auf oberster Ebene"


print(app.run(["summarise", "data.json"]))
```

## Tipps

:::tip[Welches Format wählen]
- Verwende **JSON** für maschinelle Kommunikation und API-Antworten.
- Verwende **YAML** für manuell bearbeitete Konfigurationen und Kubernetes-ähnliche Manifeste.
- Verwende **TOML** für endnutzerorientierte Konfigurationsdateien (siehe [Konfigurationsdateien](./config.md)).

Alle drei Helfer sind über den Top-Level-Import `quickli` verfügbar, du musst
`quickli.parsers` nicht direkt importieren.
:::

:::tip[Parser vs. Config]
`load_toml` / `render_toml` sind nützlich für einmaliges Parsen von TOML-Strings oder
Dateien, die du selbst verwaltest. Für persistente Anwendungskonfiguration mit
Schema-Validierung und Auto-Initialisierung verwende stattdessen die dedizierten
[Config](./config.md)-Ressourcen.
:::

## Wie geht es weiter?

- Siehe **[Konfigurationsdateien](./config.md)** für persistente, schema-validierte Konfiguration.
- Geh zurück zu **[Command](./command.md)**, um zu sehen, wie Parser-Helfer in einen Handler eingebunden werden.
