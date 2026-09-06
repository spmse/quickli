---
sidebar_position: 6
description: Modulare Plugin-Architektur zur Erweiterung von quiCkLI-Anwendungen mit wiederverwendbaren Befehlssätzen.
keywords: [quickli, plugin, erweiterung, register, load_plugin, PluginLoadError, modulare befehle]
---

# Plugin

Plugins bieten einen Erweiterungsmechanismus für `quickli`-Anwendungen, ohne den Anwendungscode im Kern zu verändern. Jedes Plugin kapselt eine Reihe von **[Command](./command.md)**-Handlern und -Ressourcen und registriert diese über einen strikten Vertrag bei einer **[Application](./application.md)**-Instanz.

Plugins befinden sich in der Architektur auf derselben Ebene wie reguläre Anwendungsbefehle:

```
Application
├── Command (direkt von der Anwendung registriert)
└── Plugin              ← du bist hier
    └── Command (von plugin.register() registriert)
```

## Der Plugin-Schnittstellenvertrag

Jedes Plugin muss `quickli.Plugin` unterklassen und drei erforderliche abstrakte Elemente implementieren:

| Element | Art | Beschreibung |
|---|---|---|
| `name` | `@property -> str` | Eindeutiger, nicht leerer String-Bezeichner für das Plugin (z. B. `"security-audit"`). |
| `description` | `@property -> str` | Kurze Beschreibung der vom Plugin bereitgestellten Funktionen. |
| `register(application)` | `method(Application) -> None` | Hook-Methode, in der das Plugin Befehle, Unterbefehle oder Ressourcen an der `Application` registriert. |

### Vollständiges Plugin-Beispiel

```python
import quickli

class DatabasePlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "database"

    @property
    def description(self) -> str:
        return "Bietet Datenbankmigrations- und Seeding-Befehle."

    def register(self, application: quickli.Application) -> None:
        @application.command(
            name="db-migrate",
            help_text="Datenbankschemamigrationen ausführen.",
        )
        def migrate() -> str:
            return "migrations applied"

        @application.command(
            name="db-seed",
            help_text="Datenbank mit Beispieldaten befüllen.",
        )
        def seed() -> str:
            return "database seeded"
```

## Laden von Plugins (`Application.load_plugin`)

Um ein Plugin zu registrieren, übergib eine Instanz deiner Plugin-Klasse an `Application.load_plugin()`:

```python
app = quickli.Application(name="mycli")

# Datenbank-Plugin laden:
app.load_plugin(DatabasePlugin())

# Vom Plugin bereitgestellte Befehle ausführen:
print(app.run(["db-migrate"]))  # migrations applied
print(app.run(["db-seed"]))     # database seeded
```

## Geladene Plugins anzeigen (`app.plugins`)

Du kannst alle geladenen Plugins über `app.plugins` abfragen:

```python
for plugin in app.plugins:
    print(f"Plugin: {plugin.name} — {plugin.description}")
```

## Fehlerbehandlung (`PluginLoadError`)

`quickli` erzwingt die Gültigkeit von Plugins und eindeutige Namen bei der Registrierung. Das Laden löst einen `PluginLoadError` aus, wenn:

1. **Leerer Name**: Die `name`-Property gibt einen leeren String zurück.
2. **Doppelter Name**: Ein Plugin mit demselben `name` ist bereits an der `Application` registriert.
3. **Registrierungsausnahme**: Die `register(application)`-Methode des Plugins löst eine unbehandelte Ausnahme aus.

```python
from quickli import Application, PluginLoadError

app = Application(name="demo")
db_plugin = DatabasePlugin()

app.load_plugin(db_plugin)

try:
    # Das zweimalige Laden desselben Plugins löst PluginLoadError aus:
    app.load_plugin(db_plugin)
except PluginLoadError as err:
    print(f"Failed to load plugin: {err}")
```

:::info[Eindeutigkeit von Plugins]
Jedes Plugin muss einen eindeutigen `name`-String zurückgeben, um Kollisionen zwischen Plugin-Paketen zu vermeiden.
:::

## Reglementierung & Einschränkungen

:::warning[Plugins können keine bestehenden Befehle überschreiben]
Ein Plugin kann keinen Befehl ersetzen, der bereits an der `Application` registriert wurde (weder von der Anwendung selbst noch von einem zuvor geladenen Plugin). Der Versuch, einen doppelten Befehlsnamen zu registrieren, löst einen `CommandRegistrationError` aus.
:::

:::tip[Modulare Anwendungsarchitektur]
Verwende Plugins, um große CLI-Anwendungen in unabhängige, wiederverwendbare Module aufzuteilen. So kann beispielsweise ein gemeinsames `auth`- oder `telemetry`-Plugin teamübergreifend verwendet werden.
:::

## Aktueller Status & Roadmap

- **Aktuell (Alpha)**: Explizite Plugin-Instanziierung und Laden über `app.load_plugin(PluginInstance())`.
- **Geplant (Zukunft)**: Automatische Plugin-Erkennung über Python-Paketeigenschaften (`importlib.metadata`).

## Wie geht es weiter?

- Erfahre mehr über Befehle in **[Command](./command.md)**.
- Erfahre, wie die Befehlsausführung funktioniert in **[Application](./application.md)**.
- Lade dauerhafte Konfigurationen in Plugins mit **[Config](./config.md)**.

