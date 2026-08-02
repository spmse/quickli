---
id: guide-hello-world
title: "Anleitung 1: Hello World"
sidebar_position: 2
description: >
  Erstelle deine erste quickli-Anwendung: einen Einstiegspunkt, der eine Person anhand
  ihres Namens begrüßt und ein optionales Großschreibungs-Flag unterstützt. Behandelt
  Application, Argument und Option.
keywords: [quickli, tutorial, hello world, entrypoint, argument, option, python, cli]
---

# Anleitung 1: Hello World

Diese Anleitung erstellt die kleinste nützliche `quickli`-Anwendung: ein Begrüßungs-
werkzeug, das einen Namen und ein optionales Flag für Großbuchstaben akzeptiert.

Du lernst:
- eine `Application` mit einer Beschreibung zu erstellen
- mit `@app.entrypoint` einen Einstiegspunkt zu registrieren
- ein Positions-`Argument` hinzuzufügen
- ein boolesches `Option`-Flag hinzuzufügen
- die Anwendung über die Kommandozeile auszuführen

## Das vollständige Beispiel

Speichere die folgende Datei als `hello.py`:

```python
from __future__ import annotations

from quickli import Application, Argument, Option


app = Application(
    name="hello",
    description="Greet a person from the command line.",
)


@app.entrypoint(
    help_text="Print a greeting.",
    arguments=[Argument("name", help_text="Name to greet.")],
    options=[
        Option(
            "uppercase",
            short_name="u",
            is_flag=True,
            help_text="Print the greeting in uppercase.",
        ),
    ],
)
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message


if __name__ == "__main__":
    print(app.run())
```

## Ausführen

```bash
python hello.py Ada
# Hello, Ada!

python hello.py Ada --uppercase
# HELLO, ADA!

python hello.py Ada -u
# HELLO, ADA!
```

## Erklärung Zeile für Zeile

### Imports

```python
from quickli import Application, Argument, Option
```

Du musst nur die drei verwendeten Klassen importieren. `quickli` hält seine öffentliche
API klein und ausdrücklich.

### Die Anwendung erstellen

```python
app = Application(
    name="hello",
    description="Greet a person from the command line.",
)
```

`Application` ist der zentrale Container. `name` wird in der Hilfe verwendet.
`description` erscheint unter der Nutzungszeile, wenn du das Werkzeug ohne Argumente
startest.

### Den Einstiegspunkt registrieren

```python
@app.entrypoint(
    help_text="Print a greeting.",
    arguments=[Argument("name", help_text="Name to greet.")],
    options=[
        Option(
            "uppercase",
            short_name="u",
            is_flag=True,
            help_text="Print the greeting in uppercase.",
        ),
    ],
)
def greet(name: str, uppercase: bool = False) -> str:
    ...
```

`@app.entrypoint` ist für Anwendungen ohne Befehl gedacht. Die Anwendung hat einen
einzigen Zweck, daher ist kein Befehlsname nötig.

- **`help_text`** erscheint in der erzeugten Nutzungsausgabe.
- **`arguments`** ist eine Liste von `Argument`-Instanzen in Positionsreihenfolge.
- **`options`** ist eine Liste von `Option`-Instanzen.

### Der Konstruktor von `Argument`

```python
Argument("name", help_text="Name to greet.")
```

`Argument` erwartet als erstes Argument einen Positionsnamen. Dieser Name muss zum
entsprechenden Funktionsparameter passen. Argumente sind standardmäßig erforderlich.
Für ein optionales Argument übergibst du `required=False` und einen `default`.

### Der Konstruktor von `Option`

```python
Option(
    "uppercase",
    short_name="u",
    is_flag=True,
    help_text="Print the greeting in uppercase.",
)
```

- **`"uppercase"`** wird in der Kommandozeile zu `--uppercase`.
- **`short_name="u"`** ergänzt die Kurzform `-u`.
- **`is_flag=True`** bedeutet, dass die Option boolesch ist: vorhanden → `True`, nicht vorhanden → `False`.
- Der Funktionsparameter muss zum Optionsnamen passen, wobei Bindestriche durch Unterstriche ersetzt werden.

### Die Handler-Funktion

```python
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message
```

Der Handler erhält die geparsten Werte direkt. `quickli` ordnet Argument- und
Optionsnamen den Parameternamen zu. Der Standardwert für `uppercase` entspricht der
Abwesenheit der Option.

Der Handler gibt einen String zurück. `quickli` gibt nichts aus; diese Verantwortung
bleibt beim ausführbaren Einstiegspunkt.

### Der Einstiegspunkt

```python
if __name__ == "__main__":
    print(app.run())
```

`Application.run()` liest standardmäßig `sys.argv[1:]`, dispatcht den passenden Handler
und gibt das Ergebnis zurück. Übergib eine explizite Liste zum Überschreiben:
`app.run(["Ada", "--uppercase"])`. Setze `auto_sys_argv=False` bei der Konstruktion,
um das automatische Lesen zu deaktivieren.

## Die Hilfeausgabe erkunden

Starte das Programm ohne Argumente:

```bash
python hello.py
```

quickli erzeugt den Nutzungstext aus den registrierten Argumenten, Optionen und
Hilfetexten.

## Was du als Nächstes ausprobieren kannst

- Füge eine zweite Option hinzu, etwa `--shout`, und ändere das Nachrichtenformat.
- Mache das Argument `name` mit `required=False` und `default="world"` optional.
- Lies [Anleitung 2: Dateibetrachter](./02-building-cat-cli.md), um globale Optionen,
  mehrere Dateiargumente und Pfadvalidierung kennenzulernen.
