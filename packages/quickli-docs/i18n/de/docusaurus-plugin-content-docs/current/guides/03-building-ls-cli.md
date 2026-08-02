---
id: guide-ls-cli
title: "Anleitung 3: Verzeichnisauflistung (quickls)"
sidebar_position: 4
description: >
  Erstelle mit quickli ein Werkzeug zur Verzeichnisauflistung. Lerne optionale Argumente
  mit Standardwerten, den directory_path-Validator und die Filterung nach Endungen kennen.
keywords: [quickli, tutorial, ls, directory listing, optional argument, directory_path]
---

# Anleitung 3: Verzeichnisauflistung (quickls)

Diese Anleitung erstellt `quickls`, ein minimales `ls`-ähnliches Werkzeug, das den Inhalt
eines Verzeichnisses auflistet. Sie zeigt, wie ein Argument durch einen Standardwert
**optional** wird und wie der `directory_path`-Validator eingesetzt wird.

Du lernst:
- ein `Argument` mit `required=False` und einem `default` optional zu machen
- den eingebauten **`directory_path`-Validator** zu verwenden
- Ergebnisse mit einer wiederholbaren Suffix-Option zu filtern

## Das vollständige Beispiel

Speichere die folgende Datei als `quickls.py`:

```python
from __future__ import annotations

from pathlib import Path

from quickli import Application, Argument, Option, directory_path


app = Application(
    name="quickls",
    description="A tiny ls-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Show the scanned directory."),
    ],
)


@app.entrypoint(
    help_text="List files in a directory.",
    arguments=[
        Argument(
            "path",
            required=False,
            default=Path("."),
            validators=[directory_path()],
        )
    ],
    options=[
        Option("all", short_name="a", is_flag=True, help_text="Include hidden files."),
        Option(
            "suffix",
            short_name="s",
            multiple=True,
            help_text="Filter by one or more suffixes.",
        ),
    ],
)
def list_directory(
    path: Path = Path("."),
    all: bool = False,
    suffix: list[str] | None = None,
    verbose: bool = False,
) -> str:
    items = sorted(path.iterdir(), key=lambda item: item.name)
    if not all:
        items = [item for item in items if not item.name.startswith(".")]
    if suffix:
        items = [item for item in items if any(item.name.endswith(value) for value in suffix)]

    lines: list[str] = []
    if verbose:
        lines.append(f"Listing: {path}")
    lines.extend(item.name for item in items)
    return "\n".join(lines)


if __name__ == "__main__":
    print(app.run())
```

## Ausführen

```bash
# Aktuelles Verzeichnis auflisten
python quickls.py

# Ein bestimmtes Verzeichnis auflisten
python quickls.py /tmp

# Versteckte Dateien anzeigen
python quickls.py --all

# Nach Suffix filtern
python quickls.py --suffix .py

# Mehrere Suffixe
python quickls.py --suffix .py -s .md

# Verzeichnispfad in der Ausgabe anzeigen
python quickls.py --verbose
```

## Erklärung Zeile für Zeile

### Optionales Argument mit Standardwert

```python
Argument(
    "path",
    required=False,
    default=Path("."),
    validators=[directory_path()],
)
```

- `required=False` macht das Argument optional.
- `default=Path(".")` liefert den Wert, wenn das Argument weggelassen wird.
- Der Validator wird auch auf den aufgelösten Standardwert angewendet. So kannst du
  sicher sein, dass der Pfad unabhängig von der Eingabe gültig ist.

### Der `directory_path`-Validator

`directory_path()` prüft, ob der Wert auf ein vorhandenes Verzeichnis zeigt. Wie
`file_path()` erzeugt er eine klare Fehlermeldung, bevor der Handler aufgerufen wird,
wenn der Pfad nicht existiert oder kein Verzeichnis ist.

### Nach Suffix filtern

```python
Option(
    "suffix",
    short_name="s",
    multiple=True,
    help_text="Filter by one or more suffixes.",
),
```

Die Option `suffix` kann mehrfach übergeben werden. Der Handler verwendet `any()`, um
Elemente zu behalten, die mindestens einem der angegebenen Suffixe entsprechen:

```python
if suffix:
    items = [item for item in items if any(item.name.endswith(value) for value in suffix)]
```

Dieses Muster ist nützlich, wenn du eine variable Liste von Filterwerten aus der
Kommandozeile akzeptieren möchtest.

## Was du als Nächstes ausprobieren kannst

- Füge ein Flag `--long` hinzu, das Dateigröße und Änderungszeit neben dem Namen ausgibt.
- Lies [Anleitung 4: Verzeichnisersteller](./04-building-mkdir-cli.md), um weitere Muster
  für wiederholbare Optionen kennenzulernen.
