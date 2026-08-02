---
id: getting-started
title: Einstieg
sidebar_position: 2
description: quickli installieren und deine erste Kommandozeilenanwendung erstellen.
keywords: [quickli, installation, einstieg, python cli, erste anwendung]
---

import { AddToProject } from '@site/src/components/QuickliExamples';

# Einstieg

Dieser Leitfaden erstellt eine kleine Kommandozeilenanwendung mit einem Einstiegspunkt,
einem positionalen Argument und einem Schalter. quickli unterstützt Python 3.12, 3.13
und 3.14.

## quickli installieren

Für ein Projekt, das das veröffentlichte Paket verwendet, installiere quickli in einer
virtuellen Umgebung:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install quickli
```

Wenn du aus dem quickli-Repository arbeitest, installiere das Paket stattdessen im
editierbaren Modus:

```bash
python -m pip install -e packages/core
```

<AddToProject />

## Eine Anwendung erstellen

Speichere dieses Beispiel als `hello.py`:

```python
from __future__ import annotations

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
    print(app.run())
```

## Ausführen

Übergebe die Kommandozeilen-Token an die Anwendung:

```bash
python hello.py Ada
python hello.py Ada --uppercase
```

Der erste Befehl gibt `Hello, Ada!` aus; der zweite gibt `HELLO, ADA!` aus.

## Generierte Hilfe erkunden

Die Anwendung generiert Hilfe aus ihren registrierten Argumenten, Optionen und
Hilfs-Strings. Führe sie ohne Argumente aus, um den Hilfstext zu sehen:

```bash
python hello.py
```

`Application.run()` liest standardmäßig `sys.argv[1:]` und gibt das Handler-Ergebnis zurück.
Übergib eine explizite Liste zum Überschreiben: `app.run(["Ada", "--uppercase"])`.
Setze `auto_sys_argv=False` bei der Konstruktion, um das automatische Lesen zu deaktivieren.

## Wie es weitergeht

- Verwende `@app.command()`, um ein Multi-Command-CLI zu bauen.
- Verwende `converter=int` oder `converter=Path`, um Eingabewerte zu konvertieren.
- Füge Validatoren wie `file_path()` oder `number_range()` für geprüfte Eingaben hinzu.
- Lies die [Projektbeispiele](https://github.com/spmse/quickli/tree/main/packages/core/examples)
  für kleine, fokussierte Anwendungen.
