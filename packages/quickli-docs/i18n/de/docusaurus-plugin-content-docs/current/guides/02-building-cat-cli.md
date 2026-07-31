---
id: guide-cat-cli
title: "Anleitung 2: Dateibetrachter (quickcat)"
sidebar_position: 3
description: >
  Erstelle mit quickli einen cat-ähnlichen Dateibetrachter. Lerne globale Optionen,
  mehrere Dateiargumente, den file_path-Validator und wiederholbare Optionen kennen.
keywords: [quickli, tutorial, cat, file viewer, global options, validators, repeatable options]
---

# Anleitung 2: Dateibetrachter (quickcat)

Diese Anleitung erstellt `quickcat`, ein minimales `cat`-ähnliches Werkzeug, das eine
oder mehrere Dateien nach stdout ausgibt. Du lernst globale Optionen, den eingebauten
`file_path`-Validator und wiederholbare Optionen kennen.

Du lernst:
- **globale Optionen** auf der `Application` zu definieren
- den eingebauten **`file_path`-Validator** zu verwenden
- **wiederholbare Optionen** mit `multiple=True` zu akzeptieren
- mehrere Eingabepfade im Handler zu kombinieren

## Das vollständige Beispiel

Speichere die folgende Datei als `quickcat.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, file_path


app = Application(
    name="quickcat",
    description="A tiny cat-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
)


@app.entrypoint(
    help_text="Print one or more text files to stdout.",
    arguments=[
        Argument("path", help_text="Primary file path.", validators=[file_path()]),
    ],
    options=[
        Option("encoding", short_name="e", default="utf-8", help_text="Text encoding."),
        Option("number", short_name="n", help_text="Print line numbers.", is_flag=True),
        Option(
            "include",
            short_name="i",
            multiple=True,
            validators=[file_path()],
            help_text="Additional file paths to print after the primary file.",
        ),
    ],
)
def show(
    path: Path,
    encoding: str = "utf-8",
    number: bool = False,
    include: list[Path] | None = None,
    verbose: bool = False,
) -> str:
    input_paths = [path, *(include or [])]
    rendered_chunks: list[str] = []

    for input_path in input_paths:
        text = input_path.read_text(encoding=encoding)
        lines = text.splitlines()

        if number:
            lines = [f"{index:>4}  {line}" for index, line in enumerate(lines, start=1)]

        if verbose:
            rendered_chunks.append(f"==> {input_path} <==")
        rendered_chunks.append("\n".join(lines))

    return "\n".join(chunk for chunk in rendered_chunks if chunk)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

## Ausführen

```bash
# Eine Datei ausgeben
python quickcat.py README.md

# Mit Zeilennummern ausgeben
python quickcat.py README.md --number

# Mehrere Dateien ausgeben (verbose zeigt Dateinamen)
python quickcat.py README.md -i CONTRIBUTING.md --verbose

# Textkodierung ändern
python quickcat.py data.txt --encoding latin-1
```

## Erklärung Zeile für Zeile

### Globale Optionen

```python
app = Application(
    name="quickcat",
    description="A tiny cat-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
)
```

Globale Optionen werden auf der Ebene der `Application` definiert. Sie können auf der
Kommandozeile vor oder nach dem Befehlsnamen stehen. Jeder Handler, der eine globale
Option verwenden möchte, muss den passenden Parameter deklarieren.

### Der `file_path`-Validator

```python
Argument("path", help_text="Primary file path.", validators=[file_path()]),
```

`file_path()` gibt eine Validator-Funktion zurück, die prüft, ob der Wert auf eine
existierende und lesbare Datei zeigt. Existiert der Pfad nicht, schlägt der Befehl mit
einer klaren Fehlermeldung fehl, bevor der Handler aufgerufen wird.

Validatoren werden nach der Konvertierung aufgerufen. Der Handler erhält daher ein
`Path`-Objekt und keinen rohen String.

### Wiederholbare Optionen

```python
Option(
    "include",
    short_name="i",
    multiple=True,
    validators=[file_path()],
    help_text="Additional file paths to print after the primary file.",
),
```

`multiple=True` weist quickli an, jedes Vorkommen von `--include` in einer Liste zu
sammeln. Du kannst die Option mehrmals übergeben:

```bash
python quickcat.py main.py -i utils.py -i helpers.py
```

Der Handler erhält `include` als `list[Path] | None`. Wird die Option gar nicht
übergeben, ist `include` gleich `None`.

### Automatische Typannotation

Die Handler-Signatur verwendet `Path` als Typ für `path`:

```python
def show(
    path: Path,
    encoding: str = "utf-8",
    number: bool = False,
    include: list[Path] | None = None,
    verbose: bool = False,
) -> str:
```

quickli verwendet Typannotationen zusammen mit registrierten Konvertern und Validatoren,
um dem Handler bereits verwendbare Werte zu übergeben.

### Die Ausgabe erstellen

```python
input_paths = [path, *(include or [])]
rendered_chunks: list[str] = []

for input_path in input_paths:
    text = input_path.read_text(encoding=encoding)
    lines = text.splitlines()

    if number:
        lines = [f"{index:>4}  {line}" for index, line in enumerate(lines, start=1)]

    if verbose:
        rendered_chunks.append(f"==> {input_path} <==")
    rendered_chunks.append("\n".join(lines))

return "\n".join(chunk for chunk in rendered_chunks if chunk)
```

Der Handler sammelt für jede Datei einen Abschnitt und verbindet sie am Ende. Leere
Strings, die von leeren Dateien erzeugt werden, werden herausgefiltert.

## Was du als Nächstes ausprobieren kannst

- Füge mit `converter=int` eine Option `--max-lines` hinzu, um die Ausgabelänge zu begrenzen.
- Lies [Anleitung 3: Verzeichnisauflistung](./03-building-ls-cli.md), um optionale
  Argumente und Verzeichnisvalidierung kennenzulernen.
