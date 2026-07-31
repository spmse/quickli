---
title: "Erste Schritte mit quiCkLI: Deine erste Kommandozeilenanwendung"
description: >
  Erstelle deine erste Python-Kommandozeilenanwendung mit quiCkLI in unter fünf Minuten.
  Dieses Tutorial behandelt Application, Argument und Option – die drei Grundbausteine,
  die du zum Einstieg brauchst.
slug: quickli-tutorial-01-hello-world
authors:
  - name: quiCkLI contributors
    url: https://github.com/spmse/quickli
date: 2025-08-01
draft: true
tags: [tutorial, einstieg, quickli, python, cli]
series:
  name: "Erste Schritte mit quiCkLI"
  position: 1
keywords: [quickli, python cli, kommandozeilen-framework, tutorial, anfänger]
---

Wenn du schon immer ein kleines Python-Kommandozeilentool erstellen wolltest, aber
größere Frameworks überwältigend fandest, wurde `quiCkLI` für dich entwickelt. Es ist ein
minimales Framework, das die Grundbausteine sichtbar lässt – damit du lernen und bauen
kannst, ohne unnötige Komplexität.

Im ersten Artikel der Reihe *Erste Schritte mit quiCkLI* wirst du ein Begrüßungstool
mit genau drei Konzepten erstellen: `Application`, `Argument` und `Option`.

<!-- truncate -->

## Was du bauen wirst

```
python hello.py Ada
Hello, Ada!

python hello.py Ada --uppercase
HELLO, ADA!
```

Eine einzige Datei. Keine Konfiguration. Unter dreißig Zeilen Python.

## Voraussetzungen

Installiere quickli in einer virtuellen Umgebung:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install quickli
```

Du benötigst Python 3.12 oder neuer.

## Schritt 1: Die Anwendung erstellen

```python
from quickli import Application

app = Application(
    name="hello",
    description="Grüße eine Person von der Kommandozeile.",
)
```

`Application` ist der Wurzel-Container. Er verwaltet Registrierung und Dispatch. Du
gibst ihm einen Namen (für die Hilfsausgabe) und eine kurze Beschreibung.

## Schritt 2: Einen Handler registrieren

```python
from quickli import Application, Argument, Option

@app.entrypoint(
    help_text="Einen Gruß ausgeben.",
    arguments=[Argument("name", help_text="Name, der gegrüßt werden soll.")],
    options=[
        Option(
            "uppercase",
            short_name="u",
            is_flag=True,
            help_text="Den Gruß in Großbuchstaben ausgeben.",
        ),
    ],
)
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message
```

`@app.entrypoint` registriert eine Funktion als einzelnen Handler für diese Anwendung.

- `Argument("name")` deklariert einen erforderlichen Positionswert.
- `Option("uppercase", is_flag=True)` deklariert einen booleschen Schalter.

## Schritt 3: Die Anwendung ausführen

```python
import sys

if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

`Application.run(argv)` nimmt eine Liste von Token entgegen und gibt das Handler-Ergebnis
zurück. Du entscheidest, was damit zu tun ist.

## Die vollständige Datei

```python
from __future__ import annotations

import sys

from quickli import Application, Argument, Option


app = Application(
    name="hello",
    description="Grüße eine Person von der Kommandozeile.",
)


@app.entrypoint(
    help_text="Einen Gruß ausgeben.",
    arguments=[Argument("name", help_text="Name, der gegrüßt werden soll.")],
    options=[
        Option(
            "uppercase",
            short_name="u",
            is_flag=True,
            help_text="Den Gruß in Großbuchstaben ausgeben.",
        ),
    ],
)
def greet(name: str, uppercase: bool = False) -> str:
    message = f"Hello, {name}!"
    return message.upper() if uppercase else message


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
```

## Probiere es aus

```bash
python hello.py Ada           # Hello, Ada!
python hello.py Ada -u        # HELLO, ADA!
python hello.py               # (Hilfsausgabe)
```

## Was du gelernt hast

- `Application` verwaltet Registrierung und Dispatch.
- `@app.entrypoint` registriert einen einzelnen Handler für die gesamte Anwendung.
- `Argument` beschreibt positionalen, erforderlichen Input.
- `Option` mit `is_flag=True` fügt einen booleschen Schalter hinzu.
- `Application.run(argv)` gibt das Ergebnis zurück – du steuerst die Ausgabe.

## Weiter in dieser Reihe

Der nächste Artikel fügt **Datei-Input**, **Validierung** und **globale Optionen** hinzu,
indem er einen kleinen Datei-Viewer nach dem Vorbild des Unix-`cat`-Befehls baut.

📖 [Teil 2: Dateien lesen – das quickcat-Tool →](/de/blog/quickli-tutorial-02-file-tools)
