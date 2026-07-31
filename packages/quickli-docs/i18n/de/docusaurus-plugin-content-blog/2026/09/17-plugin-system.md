---
title: "Das quiCkLI-Plugin-System"
description: "Eine Einführung in die quiCkLI-Plugin-API und den Vertrag, den jeder Plugin-Autor implementieren muss."
slug: quickli-plugin-system
authors:
  - spmse
date: 2026-09-17
draft: true
tags: [general, plugins, api, quickli]
keywords: [quickli, plugin system, api, python cli, erweiterbar]
---

`quickli` enthält jetzt ein rudimentäres Plugin-System, mit dem du jede Anwendung
erweitern kannst, ohne das Kernpaket zu berühren. Dieser Beitrag führt durch die
Plugin-API, den Vertrag, den du implementieren musst, und wie der Lademechanismus
funktioniert.

{/* truncate */}

## Warum ein Plugin-System?

Ein CLI-Framework, das nur durch Bearbeiten des Quellcodes erweitert werden kann, ist ein
geschlossenes System. Plugins machen es möglich, wiederverwendbare Befehle als
unabhängige Python-Pakete zu verteilen, die jede `quickli`-Anwendung zur Laufzeit laden
kann.

## Der Plugin-Vertrag

Jedes Plugin muss `quickli.Plugin` ableiten und genau drei Member implementieren.

```python
import quickli


class VersionPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "version-plugin"

    @property
    def description(self) -> str:
        return "Fügt der Anwendung einen Version-Befehl hinzu."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Gibt die Anwendungsversion aus.")
        def version() -> str:
            return "1.0.0"
```

## Ein Plugin laden

Rufe `Application.load_plugin(plugin)` auf, um ein Plugin zu laden.

```python
app = quickli.Application(name="demo")
app.load_plugin(VersionPlugin())
print(app.run(["version"]))  # 1.0.0
```

## Fehlerbehandlung

`quickli.PluginLoadError` ist der einzige Ausnahmetyp, der bei allen Ladefehlern
ausgelöst wird.

| Situation | Verhalten |
|---|---|
| Plugin-Name ist leer | `PluginLoadError` vor dem Aufruf von `register` |
| Plugin mit gleichem Namen bereits geladen | `PluginLoadError` |
| `register` löst `PluginLoadError` aus | unverändert weitergegeben |
| `register` löst eine andere Ausnahme aus | in `PluginLoadError` eingebettet |

## Referenz

- [Plugin-Konzeptdokumentation](/docs/concepts/plugin)
- [Plugin-Spezifikation auf GitHub](https://github.com/spmse/quickli/blob/main/packages/core/specs/plugin.md)
