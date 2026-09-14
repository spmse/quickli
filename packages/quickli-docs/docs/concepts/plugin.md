---
sidebar_position: 6
description: Modular plugin architecture for extending quiCkLI applications with reusable command sets.
keywords: [quickli, plugin, extension, register, load_plugin, PluginLoadError, modular commands]
---

# Plugin

Plugins provide an extensibility mechanism for `quickli` applications without modifying core application code. Each plugin encapsulates a set of **[Command](./command.md)** handlers and resources, registering them against an **[Application](./application.md)** instance through a strict contract.

Plugins sit alongside regular application commands in the architecture:

```
Application
├── Command (registered directly by app)
└── Plugin              ← you are here
    └── Command (registered by plugin.register())
```

## The Plugin Interface Contract

Every plugin must subclass `quickli.Plugin` and implement three required abstract members:

| Member | Kind | Description |
|---|---|---|
| `name` | `@property -> str` | Unique, non-empty string identifier for the plugin (e.g. `"security-audit"`). |
| `description` | `@property -> str` | Short explanation of the functionality provided by the plugin. |
| `register(application)` | `method(Application) -> None` | Hook method where the plugin registers commands, subcommands, or resources onto the `Application`. |

### Complete Plugin Example

```python
import quickli

class DatabasePlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "database"

    @property
    def description(self) -> str:
        return "Provides database migration and seeding commands."

    def register(self, application: quickli.Application) -> None:
        @application.command(
            name="db-migrate",
            help_text="Run database schema migrations.",
        )
        def migrate() -> str:
            return "migrations applied"

        @application.command(
            name="db-seed",
            help_text="Seed database with sample data.",
        )
        def seed() -> str:
            return "database seeded"
```

## Loading Plugins (`Application.load_plugin`)

To register a plugin, pass an instance of your plugin class to `Application.load_plugin()`:

```python
app = quickli.Application(name="mycli")

# Load database plugin:
app.load_plugin(DatabasePlugin())

# Execute plugin-provided commands:
print(app.run(["db-migrate"]))  # migrations applied
print(app.run(["db-seed"]))     # database seeded
```

## Inspecting Loaded Plugins (`app.plugins`)

You can inspect all plugins currently loaded into an `Application` by accessing `app.plugins`, which returns a read-only snapshot list of loaded plugin instances:

```python
for plugin in app.plugins:
    print(f"Plugin: {plugin.name} — {plugin.description}")
```

## Error Handling (`PluginLoadError`)

`quickli` enforces plugin validity and unique names during registration. Loading a plugin raises `PluginLoadError` if:

1. **Empty Name**: The plugin `name` property returns an empty or whitespace string.
2. **Duplicate Name**: A plugin with the same `name` is already registered on the `Application`.
3. **Registration Exception**: The plugin's `register(application)` method raises an unhandled exception.

```python
from quickli import Application, PluginLoadError

app = Application(name="demo")
db_plugin = DatabasePlugin()

app.load_plugin(db_plugin)

try:
    # Attempting to load the same plugin twice raises PluginLoadError:
    app.load_plugin(db_plugin)
except PluginLoadError as err:
    print(f"Failed to load plugin: {err}")
```

:::info[Plugin Uniqueness]
Each plugin must return a unique `name` string to avoid collisions between third-party plugin packages.
:::

## Plugin Rules and Constraints

:::warning[Plugins Cannot Override Existing Commands]
A plugin cannot override or replace a command that has already been registered on the `Application` (either by the application itself or by a previously loaded plugin). Attempting to register a duplicate command name raises a `CommandRegistrationError`.
:::

:::tip[Modular Application Architecture]
Use plugins to break large CLI applications into independent, reusable modules. For example, a company can distribute a shared `auth` or `telemetry` plugin across multiple team repositories without duplicating command logic.
:::

## Current Status & Roadmap

- **Current (Alpha)**: Explicit plugin instantiation and loading via `app.load_plugin(PluginInstance())`.
- **Planned (Future)**: Automatic plugin discovery via Python package entry points (`importlib.metadata`).

## Where to Go Next

- Learn how commands registered by plugins work in **[Command](./command.md)**.
- See how application execution dispatches plugin commands in **[Application](./application.md)**.
- Load persistent configuration inside plugins using **[Config](./config.md)**.

