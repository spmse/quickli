---
sidebar_position: 6
description: Plugins erweitern eine quiCkLI-Anwendung mit wiederverwendbaren Befehlssets.
keywords: [quickli, plugin, erweiterung, register, load_plugin]
---

# Plugin

Plugins erweitern eine `quickli`-Anwendung, ohne das Kernpaket zu verändern.
Jedes Plugin registriert seine Befehle und Ressourcen anhand eines klar definierten Vertrags
bei einer `Application`-Instanz.

Plugins befinden sich in der Hierarchie auf derselben Ebene wie reguläre Befehle: Sie
hängen neue Befehle von außen an eine bestehende `Application` an.

```
Application
├── Command (direkt registriert)
└── Plugin              ← du bist hier
    └── Command (vom Plugin registriert)
```

## Plugin-Vertrag

Jedes Plugin muss `quickli.Plugin` unterklassen und drei Elemente implementieren:

| Element | Art | Erforderlich | Beschreibung |
|---|---|---|---|
| `name` | `str`-Property | ja | Eindeutiger, nicht leerer Plugin-Bezeichner |
| `description` | `str`-Property | ja | Kurze Beschreibung der bereitgestellten Funktionen |
| `register(application)` | Methode | ja | Registriert Befehle und Ressourcen bei der Anwendung |

```python
import quickli


class VersionPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "version-plugin"

    @property
    def description(self) -> str:
        return "Adds a version command."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Prints the application version.")
        def version() -> str:
            return "1.0.0"
```

## Ein Plugin laden

Rufe `Application.load_plugin(plugin)` auf, um ein Plugin in deine Anwendung zu laden.

```python
app = quickli.Application(name="demo")
app.load_plugin(VersionPlugin())
print(app.run(["version"]))  # 1.0.0
```

`load_plugin` validiert den Plugin-Namen, verhindert doppelte Ladevorgänge und ruft
`plugin.register(application)` auf, damit das Plugin seine Befehle registrieren kann.

## Geladene Plugins anzeigen

`Application.plugins` gibt eine Kopie der Liste geladener Plugins zurück.

```python
for plugin in app.plugins:
    print(f"{plugin.name}: {plugin.description}")
```

## Fehlerbehandlung

`quickli.PluginLoadError` wird ausgelöst, wenn:

- der Plugin-Name leer ist,
- bereits ein Plugin mit demselben Namen geladen wurde,
- oder die `register`-Methode des Plugins eine Ausnahme auslöst.

```python
try:
    app.load_plugin(VersionPlugin())
except quickli.PluginLoadError as error:
    print(f"Failed to load plugin: {error}")
```

## Tipps

:::tip[Wann ein Plugin verwenden]
Verwende ein Plugin, wenn du einen wiederverwendbaren Befehlssatz als separates Python-Modul
oder -Paket verpacken möchtest. Ein gemeinsames `audit`-Plugin kann z. B. in jede Team-CLI
geladen werden, ohne Code zu kopieren. Für kleine, anwendungsspezifische Befehle verwende
einfach direkt `@app.command`.
:::

:::warning[Plugins können keine bestehenden Befehle überschreiben]
Ein Plugin kann keinen Befehl ersetzen, der bereits registriert wurde — weder von der
Anwendung selbst noch von einem früheren Plugin. Entwirf deine Plugins so, dass sie neue
Befehle hinzufügen und keine bestehenden ersetzen.
:::

## Aktueller Status

Das Plugin-System ist im Alpha-Release mit explizitem Laden über
`Application.load_plugin()` implementiert.
Die automatische Plugin-Erkennung über Paketmetadaten (Entry Points von `importlib.metadata`)
ist für ein zukünftiges Release geplant.

## Referenz

Siehe die [Plugin-Spezifikation](https://github.com/spmse/quickli/blob/main/packages/core/specs/plugin.md)
und [ADR 0002](https://github.com/spmse/quickli/blob/main/packages/core/docs/adr/0002-plugin-api-design.md)
für die vollständige Begründung des Designs.
