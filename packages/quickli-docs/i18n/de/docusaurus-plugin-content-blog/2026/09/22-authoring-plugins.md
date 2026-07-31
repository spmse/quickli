---
title: "Dein erstes quiCkLI-Plugin erstellen"
description: "Eine Schritt-für-Schritt-Anleitung zum Erstellen, Testen und Verteilen eines quiCkLI-Plugins."
slug: authoring-a-quickli-plugin
authors:
  - spmse
date: 2026-09-22
draft: true
tags: [general, plugins, tutorial, quickli]
keywords: [quickli, plugin erstellen, python paket, tutorial, pypi]
---

Dieser Beitrag führt dich durch den Aufbau eines kleinen, aber vollständigen
`quickli`-Plugins von Grund auf  -  einschließlich der Python-Paketstruktur, dem Schreiben
von Tests und den Schritten zur Verteilung.

{/* truncate */}

## Voraussetzungen

Stelle sicher, dass `quickli` installiert ist:

```bash
$ pip install quickli
```

## Was wir bauen werden

Wir erstellen ein Plugin namens `quickli-hello`, das jedem `quickli`-Application einen
`hello`-Befehl hinzufügt. Der Befehl akzeptiert ein optionales `--uppercase`-Flag und
ein optionales `name`-Argument.

```
demo hello Ada --uppercase
# HELLO ADA
```

## Projektstruktur

```
quickli-hello/
├── pyproject.toml
├── src/
│   └── quickli_hello/
│       └── __init__.py
└── tests/
    └── test_hello_plugin.py
```

## Schritt 1: Das Plugin-Paket erstellen

Erstelle `src/quickli_hello/__init__.py`:

```python
"""quickli-hello: fügt einer quickli-Anwendung einen hello-Befehl hinzu."""

from __future__ import annotations

import quickli


class HelloPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "quickli-hello"

    @property
    def description(self) -> str:
        return "Fügt einen hello-Befehl hinzu, der einen Benutzer mit Namen begrüßt."

    def register(self, application: quickli.Application) -> None:
        @application.command(
            help_text="Begrüßt einen Benutzer mit Namen.",
            arguments=[quickli.Argument("name", required=False, default="world")],
            options=[quickli.Option("uppercase", short_name="u", is_flag=True)],
        )
        def hello(name: str = "world", uppercase: bool = False) -> str:
            message = f"hello {name}"
            if uppercase:
                message = message.upper()
            return message
```

## Schritt 2: Eine pyproject.toml schreiben

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "quickli-hello"
version = "0.1.0"
description = "Ein quickli-Plugin, das einen hello-Befehl hinzufügt."
requires-python = ">=3.12"
dependencies = ["quickli>=0.1.1"]

[tool.setuptools]
package-dir = {"" = "src"}
```

## Schritt 3: Tests schreiben

```bash
$ PYTHONPATH=src python -m unittest discover -s tests -v
```

## Schritt 4: Das Plugin in einer Anwendung verwenden

```python
import quickli
from quickli_hello import HelloPlugin

app = quickli.Application(name="my-app", description="Meine CLI-Anwendung.")
app.load_plugin(HelloPlugin())

import sys
print(app.run(sys.argv[1:]))
```

## Referenz

- [Plugin-API-Übersicht](/blog/quickli-plugin-system)
- [Plugin-Konzeptdokumentation](/docs/concepts/plugin)
