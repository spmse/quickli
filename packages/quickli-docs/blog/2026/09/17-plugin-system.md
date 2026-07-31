---
title: "Introducing the quiCkLI Plugin System"
description: "A walkthrough of the quiCkLI plugin API and the contract every plugin author must implement."
slug: quickli-plugin-system
authors:
  - spmse
date: 2026-09-17
draft: true
tags: [general, plugins, api, quickli]
---

`quickli` now ships with a rudimentary plugin system that lets you extend any application
without touching the core package. This post walks through the plugin API, the contract
you must implement, and how the loading mechanism works.

{/* truncate */}

## Why a plugin system?

A CLI framework that can only be extended by editing source code is a closed system.
Plugins make it possible to distribute reusable commands as independent Python packages
that any `quickli` application can load at runtime.

The Alpha release ships a minimal, explicit loading API. Automatic discovery via Python
package metadata entry points is planned but kept out of scope until the contract is
proven stable.

## The Plugin contract

Every plugin must subclass `quickli.Plugin` and implement exactly three members.

```python
import quickli


class VersionPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "version-plugin"

    @property
    def description(self) -> str:
        return "Adds a version command to the application."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Prints the application version.")
        def version() -> str:
            return "1.0.0"
```

### `name`

A unique, non-empty string that identifies this plugin. The name appears in error messages
and in `Application.plugins`.

### `description`

A short human-readable description of what the plugin provides. Used in help output and
diagnostic messages.

### `register(application)`

The entry point called once when the plugin is loaded. Add commands, register options, or
perform any other setup here. Raise `quickli.PluginLoadError` to signal an unrecoverable
failure.

## Loading a plugin

Call `Application.load_plugin(plugin)` to load a plugin.

```python
app = quickli.Application(name="demo")
app.load_plugin(VersionPlugin())
print(app.run(["version"]))  # 1.0.0
```

`load_plugin` performs these steps:

1. Validates that the plugin `name` is not empty.
2. Validates that no plugin with the same `name` is already loaded.
3. Calls `plugin.register(application)`.
4. Appends the plugin to the internal plugin list.

## Inspecting loaded plugins

`Application.plugins` returns a copy of the currently loaded plugin list.

```python
for plugin in app.plugins:
    print(f"{plugin.name}: {plugin.description}")
```

## Error handling

`quickli.PluginLoadError` is the single exception type raised for all loading failures.

| Situation | Behavior |
|---|---|
| Plugin name is empty | `PluginLoadError` raised before `register` is called |
| Plugin with same name is already loaded | `PluginLoadError` raised |
| `register` raises `PluginLoadError` | propagated unchanged |
| `register` raises any other exception | wrapped in `PluginLoadError` |

```python
try:
    app.load_plugin(VersionPlugin())
except quickli.PluginLoadError as error:
    print(f"Plugin load failed: {error}")
```

## Global options and plugins

When an application defines global options, a plugin command handler must declare the
corresponding parameters to receive those values.

```python
app = quickli.Application(
    name="demo",
    global_options=[quickli.Option("verbose", short_name="v", is_flag=True)],
)


class InfoPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "info-plugin"

    @property
    def description(self) -> str:
        return "Prints application information."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Shows info.")
        def info(verbose: bool = False) -> str:
            if verbose:
                return "[verbose] demo 1.0.0 (Python 3.12)"
            return "demo 1.0.0"


app.load_plugin(InfoPlugin())
print(app.run(["--verbose", "info"]))  # [verbose] demo 1.0.0 (Python 3.12)
```

## What is not yet supported

- **Automatic discovery** via `importlib.metadata` entry points is planned but not
  implemented. For now, plugins must be loaded explicitly with `load_plugin`.
- **Nested subcommands inside plugins** are not supported in the current command model.
- **Plugin ordering guarantees** beyond the order in which `load_plugin` is called are
  not defined.

## Reference

- [Plugin concept documentation](/docs/concepts/plugin)
- [Plugin specification on GitHub](https://github.com/spmse/quickli/blob/main/packages/core/specs/plugin.md)
- [ADR 0002: Plugin API Design](https://github.com/spmse/quickli/blob/main/packages/core/docs/adr/0002-plugin-api-design.md)
