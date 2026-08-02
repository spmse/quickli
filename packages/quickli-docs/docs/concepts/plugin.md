---
sidebar_position: 6
description: Plugins extend a quiCkLI application with reusable command sets.
keywords: [quickli, plugin, extension, register, load_plugin]
---

# Plugin

Plugins extend a `quickli` application without modifying the core package.
Each plugin registers its commands and resources against an `Application` instance through a
well-defined contract.

Plugins exist at the same level as regular commands in the hierarchy: they attach new
commands to an existing `Application` from the outside.

```
Application
├── Command (registered directly)
└── Plugin              ← you are here
    └── Command (registered by the plugin)
```

## Plugin contract

Every plugin must subclass `quickli.Plugin` and implement three members:

| Member | Kind | Required | Description |
|---|---|---|---|
| `name` | `str` property | yes | Unique, non-empty plugin identifier |
| `description` | `str` property | yes | Short description of what the plugin provides |
| `register(application)` | method | yes | Registers commands and resources against the app |

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

## Loading a plugin

Call `Application.load_plugin(plugin)` to load a plugin into your application.

```python
app = quickli.Application(name="demo")
app.load_plugin(VersionPlugin())
print(app.run(["version"]))  # 1.0.0
```

`load_plugin` validates the plugin name, prevents duplicate loading, and calls
`plugin.register(application)` to let the plugin register its commands.

## Inspecting loaded plugins

`Application.plugins` returns a copy of the loaded plugin list.

```python
for plugin in app.plugins:
    print(f"{plugin.name}: {plugin.description}")
```

## Error handling

`quickli.PluginLoadError` is raised when:

- the plugin name is empty,
- a plugin with the same name is already loaded,
- or the plugin's `register` method raises an exception.

```python
try:
    app.load_plugin(VersionPlugin())
except quickli.PluginLoadError as error:
    print(f"Failed to load plugin: {error}")
```

## Tips

:::tip When to use a plugin
Use a plugin when you want to package a reusable set of commands as a separate Python
module or package. For example, a shared `audit` plugin can be loaded into any team's
CLI without copying code. For small, app-specific commands, just use `@app.command`
directly.
:::

:::tip Plugins cannot override existing commands
A plugin cannot replace a command that has already been registered — either by the
application itself or by an earlier plugin. Design your plugins to add new commands
rather than replace existing ones.
:::

## Current status

The plugin system is implemented in the Alpha release with explicit loading through
`Application.load_plugin()`.
Automatic plugin discovery via Python package metadata (`importlib.metadata` entry points)
is planned for a future release.

## Reference

See the [plugin specification](https://github.com/spmse/quickli/blob/main/packages/core/specs/plugin.md)
and [ADR 0002](https://github.com/spmse/quickli/blob/main/packages/core/docs/adr/0002-plugin-api-design.md)
for the full design rationale.
