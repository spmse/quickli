---
title: "Erste Schritte mit quiCkLI: Dateien lesen und Eingaben validieren"
description: >
  Lerne, wie du Dateipfade entgegennimmst, sie vor dem Ausführen deines Handlers
  validierst und globale Optionen verwendest. Wir bauen quickcat, einen minimalen
  Datei-Viewer.
slug: quickli-tutorial-02-file-tools
authors:
  - spmse
date: 2026-07-31
tags: [tutorial, quickli, python, cli, validators, file-path]
series:
  name: "Erste Schritte mit quiCkLI"
  position: 2
keywords: [quickli, python cli, validatoren, file_path, globale optionen, tutorial]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

In [Teil 1](/blog/quickli-tutorial-01-hello-world) hast du ein Begrüßungstool mit
einem einzigen Argument und einem Schalter gebaut. In diesem Artikel kommen zwei neue
Konzepte dazu: **Validatoren**, die ungültige Eingaben abfangen, bevor dein Handler
ausgeführt wird, und **globale Optionen**, die für jede Anweisung in einer Anwendung
gelten.

Das Beispiel ist `quickcat`, ein minimaler Datei-Viewer nach dem Vorbild des
Unix-`cat`-Befehls.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[0]} currentSlug="quickli-tutorial-02-file-tools" />

## Was du bauen wirst

```bash
$ python quickcat.py README.md
$ python quickcat.py README.md --number
$ python quickcat.py README.md -i CONTRIBUTING.md --verbose
```

## Neue Konzepte

| Konzept | Zweck |
|---|---|
| `file_path()` | Eingebauter Validator, der prüft, ob ein Pfad auf eine echte Datei zeigt |
| `global_options` | Optionen auf `Application`-Ebene, die für jeden Handler gelten |
| `multiple=True` | Dieselbe Option mehrfach übergeben und Werte in einer Liste sammeln |

## Globale Optionen

```python
app = Application(
    name="quickcat",
    description="Ein winziges cat-ähnliches CLI, gebaut mit quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Ausführliche Ausgabe aktivieren."),
    ],
)
```

Globale Optionen werden auf `Application`-Ebene definiert. Jeder Handler, der sie
verwenden möchte, muss den entsprechenden Parameter deklarieren.

## Der `file_path`-Validator

```python
Argument("path", help_text="Primärer Dateipfad.", validators=[file_path()]),
```bash

$ `file_path()` ist eine eingebaute Validator-Factory. Sie gibt ein Callable zurück, das
$ quickli nach dem Parsen, aber vor dem Aufruf deines Handlers ausführt. Wenn der Pfad
$ nicht existiert oder keine Datei ist, wird die Ausführung mit einer klaren Fehlermeldung
$ abgebrochen.

$ ## Wiederholbare Optionen

$ ```python
$ Option(
$     "include",
$     short_name="i",
$     multiple=True,
$     validators=[file_path()],
$     help_text="Zusätzliche Dateipfade, die nach der primären Datei ausgegeben werden.",
$ ),
```

`multiple=True` ermöglicht es, die Option mehrfach zu übergeben. Der Handler empfängt
`include` als `list[Path] | None`.

## Das vollständige Beispiel

```python
from __future__ import annotations

from pathlib import Path

from quickli import Application, Argument, Option, file_path


app = Application(
    name="quickcat",
    description="Ein winziges cat-ähnliches CLI, gebaut mit quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Ausführliche Ausgabe aktivieren."),
    ],
)


@app.entrypoint(
    help_text="Eine oder mehrere Textdateien auf stdout ausgeben.",
    arguments=[
        Argument("path", help_text="Primärer Dateipfad.", validators=[file_path()]),
    ],
    options=[
        Option("encoding", short_name="e", default="utf-8", help_text="Zeichenkodierung."),
        Option("number", short_name="n", help_text="Zeilennummern ausgeben.", is_flag=True),
        Option(
            "include",
            short_name="i",
            multiple=True,
            validators=[file_path()],
            help_text="Zusätzliche Dateipfade nach der primären Datei.",
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
    print(app.run())
```

## Was du gelernt hast

- `global_options` auf `Application` deklarieren Optionen, die für jeden Handler verfügbar sind.
- `file_path()` validiert, dass ein Wert auf eine vorhandene, lesbare Datei zeigt.
- `multiple=True` sammelt wiederholte Optionswerte in einer Liste.
- Validatoren laufen vor dem Handler und halten dessen Körper sauber.

## Weiter in dieser Reihe

Der abschließende Artikel baut eine kubectl-ähnliche Multi-Command-Anwendung mit
`@app.command`, eigenen Validator-Factories und `CommandExecutionError`.

📖 [Teil 3: Multi-Command-Anwendungen →](/blog/quickli-tutorial-03-multi-command-cli)
