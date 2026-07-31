---
id: guide-head-cli
title: "Anleitung 5: Dateikopf (quickhead)"
sidebar_position: 6
description: >
  Erstelle mit quickli ein head-ähnliches Dateiprogramm. Lerne numerische Konvertierung
  mit converter=int und den positive_number-Validator zur Begrenzung von Optionswerten.
keywords: [quickli, tutorial, head, file head, converter, positive_number, validator]
---

# Anleitung 5: Dateikopf (quickhead)

Diese Anleitung erstellt `quickhead`, ein minimales `head`-ähnliches Werkzeug, das die
ersten oder letzten Zeilen einer Datei ausgibt. Du lernst die **numerische Konvertierung**
mit `converter=int` und den eingebauten `positive_number`-Validator kennen.

Du lernst:
- rohe Optionsstrings mit **`converter=int`** in Integer umzuwandeln
- konvertierte Werte mit **`positive_number()`** zu validieren
- ein Flag für den Tail-Modus hinzuzufügen

## Das vollständige Beispiel

Speichere die folgende Datei als `quickhead.py`:

```python
from __future__ import annotations

from pathlib import Path
from sys import argv

from quickli import Application, Argument, Option, file_path, positive_number

app = Application(
    name="quickhead",
    description="A tiny head-like CLI built with quickli.",
)


@app.entrypoint(
    help_text=(
        "Display the first few lines of a file. If no value is given, the first 10 "
        "lines are displayed."
    ),
    arguments=[Argument("file", validators=[file_path()])],
    options=[
        Option(
            "lines",
            short_name="n",
            converter=int,
            validators=[positive_number()],
            help_text="Number of lines to display.",
        ),
        Option(
            "tailmode",
            short_name="t",
            is_flag=True,
            help_text="Display the last few lines instead of the first.",
        ),
    ],
)
def head(file: Path, lines: int = 10, tailmode: bool = False) -> str:
    content = file.read_text(encoding="utf-8").splitlines(keepends=True)
    if tailmode:
        return "".join(content[-lines:])
    return "".join(content[:lines])


if __name__ == "__main__":
    print(app.run(argv[1:]))
```

## Ausführen

```bash
# Die ersten 10 Zeilen ausgeben (Standard)
python quickhead.py README.md

# Die ersten 5 Zeilen ausgeben
python quickhead.py README.md --lines 5
python quickhead.py README.md -n 5

# Die letzten 3 Zeilen ausgeben
python quickhead.py README.md -n 3 --tailmode
python quickhead.py README.md -n 3 -t
```

## Erklärung Zeile für Zeile

### Numerische Konvertierung

```python
Option(
    "lines",
    short_name="n",
    converter=int,
    validators=[positive_number()],
    help_text="Number of lines to display.",
),
```

Die Kommandozeile liefert immer rohe Strings. `converter=int` weist quickli an, vor der
Übergabe an den Handler `int()` auf den Wert anzuwenden. Schlägt die Konvertierung fehl,
etwa bei `--lines abc`, erzeugt quickli vor dem Handler-Aufruf eine klare Fehlermeldung.

Als Konverter kannst du jeden aufrufbaren Wert verwenden — `int`, `float`, `Path` oder
deine eigene Funktion.

### Der `positive_number`-Validator

`positive_number()` läuft nach dem Konverter und erhält daher einen `int`. Er löst einen
`ValueError` aus, wenn der Wert nicht positiv, also nicht größer als null, ist. Der
Handler kann deshalb von `lines >= 1` ausgehen.

### Standardwert für eine konvertierte Option

```python
def head(file: Path, lines: int = 10, tailmode: bool = False) -> str:
```

Der Standardwert für `lines` ist `10`. Wenn die Option fehlt, erhält der Handler direkt
`10`; für den Standardwert ist keine Konvertierung erforderlich, da quickli den Konverter
nur auf vom Benutzer gelieferte Werte anwendet.

### Tail-Modus

```python
if tailmode:
    return "".join(content[-lines:])
return "".join(content[:lines])
```

Der negative Python-Slice `content[-lines:]` gibt die letzten `lines` Elemente zurück.
So lassen sich Kopf und Ende derselben Datei sauber in einem Handler umsetzen.

## Was du als Nächstes ausprobieren kannst

- Füge eine Option `--bytes` hinzu, die die ersten N Bytes statt Zeilen ausgibt.
- Lies [Anleitung 6: CLI mit mehreren Befehlen](./06-multi-command-kubectl.md), um
  benannte Befehle und globale Anwendungsoptionen kennenzulernen.
