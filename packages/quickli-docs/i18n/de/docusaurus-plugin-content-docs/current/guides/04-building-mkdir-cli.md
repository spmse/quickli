---
id: guide-mkdir-cli
title: "Anleitung 4: Verzeichnisersteller (quickmkdir)"
sidebar_position: 5
description: >
  Erstelle mit quickli einen mkdir-ähnlichen Verzeichnisersteller. Lerne, wie du mit
  wiederholbaren Optionen mehrere Verzeichnisse in einem Aufruf erzeugst und mehrere
  Pfadoperationen kombinierst.
keywords: [quickli, tutorial, mkdir, directory creator, repeatable options, multiple paths]
---

# Anleitung 4: Verzeichnisersteller (quickmkdir)

Diese Anleitung erstellt `quickmkdir`, ein minimales `mkdir`-ähnliches Werkzeug, das
einen oder mehrere Verzeichnisse in einem Aufruf erzeugt. Du lernst, mit einer
wiederholbaren Option zusätzliche Pfade zu sammeln und sie mit dem primären Argument
zu kombinieren.

Du lernst:
- neben einem **primären Pfad** zusätzliche Pfade über eine wiederholbare Option zu akzeptieren
- Pfade, die noch nicht existieren, mit `directory_path(exists=None)` zu validieren
- für `mkdir`-Verhalten die Flags `--parents` und `--exist-ok` zu verwenden

## Das vollständige Beispiel

Speichere die folgende Datei als `quickmkdir.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, directory_path


app = Application(
    name="quickmkdir",
    description="A tiny mkdir-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Print created directories."),
    ],
)


@app.entrypoint(
    help_text="Create one or more directories.",
    arguments=[Argument("path", validators=[directory_path(exists=None)])],
    options=[
        Option(
            "extra",
            short_name="e",
            multiple=True,
            validators=[directory_path(exists=None)],
            help_text="Create additional directories in the same call.",
        ),
        Option("parents", short_name="p", is_flag=True, help_text="Create parent directories."),
        Option("exist-ok", is_flag=True, help_text="Ignore existing directories."),
    ],
)
def create(
    path: Path,
    extra: list[Path] | None = None,
    parents: bool = False,
    exist_ok: bool = False,
    verbose: bool = False,
) -> str:
    paths = [path, *(extra or [])]
    for item in paths:
        item.mkdir(parents=parents, exist_ok=exist_ok)

    if not verbose:
        return "created"

    return "\n".join(f"created: {item}" for item in paths)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

## Ausführen

```bash
# Ein einzelnes Verzeichnis erstellen
python quickmkdir.py new-folder

# Mehrere Verzeichnisse erstellen
python quickmkdir.py dist -e logs -e tmp

# Mit übergeordneten Verzeichnissen erstellen
python quickmkdir.py a/b/c --parents

# Erstellte Verzeichnisse anzeigen
python quickmkdir.py output --verbose

# Bereits vorhandene Verzeichnisse stillschweigend ignorieren
python quickmkdir.py output --exist-ok
```

## Erklärung Zeile für Zeile

### Pfade validieren, die noch nicht existieren dürfen

```python
Argument("path", validators=[directory_path(exists=None)])
```

`directory_path(exists=None)` überspringt die Existenzprüfung. Der Validator prüft nur,
ob der Wert ein syntaktisch gültiger Pfad ist. Das ist hier passend, weil wir das
Verzeichnis *erstellen* — es darf noch nicht existieren, außer `--exist-ok` wird verwendet.

### Mehrere Pfade sammeln

```python
Option(
    "extra",
    short_name="e",
    multiple=True,
    validators=[directory_path(exists=None)],
    help_text="Create additional directories in the same call.",
),
```

`multiple=True` sammelt alle Werte von `--extra` beziehungsweise `-e` in einer Liste.
Jeder Wert wird einzeln durch `directory_path(exists=None)` validiert.

### Pfade im Handler kombinieren

```python
paths = [path, *(extra or [])]
for item in paths:
    item.mkdir(parents=parents, exist_ok=exist_ok)
```

Der Handler kombiniert den primären Pfad und die zusätzlichen Pfade in einer Liste und
erstellt anschließend jedes Verzeichnis. `extra or []` schützt vor `None`, wenn keine
`--extra`-Werte angegeben wurden.

### Optionsname mit Bindestrich

```python
Option("exist-ok", is_flag=True, help_text="Ignore existing directories."),
```

Auf Optionen mit Bindestrichen (`exist-ok`) wird im Handler über Parameter mit
Unterstrichen (`exist_ok`) zugegriffen. quickli wandelt Namen mit Bindestrichen
automatisch in Namen mit Unterstrichen um.

## Was du als Nächstes ausprobieren kannst

- Füge eine Option `--mode` hinzu, die eine Unix-Berechtigungszeichenkette (zum Beispiel
  `755`) akzeptiert und an `Path.mkdir` übergibt.
- Lies [Anleitung 5: Dateikopf](./05-building-head-cli.md), um numerische Konvertierung
  und Bereichsvalidierung kennenzulernen.
