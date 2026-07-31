# Plugin Specification

## Purpose

A plugin extends a `quickli` application without modifying the core package. Plugins
register commands, options, or other resources against an `Application` instance through
a stable, well-defined contract.

## Plugin Contract

Every plugin must subclass `quickli.Plugin` and implement the following abstract interface:

| Member | Kind | Required | Description |
|---|---|---|---|
| `name` | `str` property | yes | Unique, human-readable plugin identifier. Must not be empty. |
| `description` | `str` property | yes | Short description of what the plugin provides. |
| `register(application)` | method | yes | Registers commands and resources against the application. |

```python
import quickli


class MyPlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "my-plugin"

    @property
    def description(self) -> str:
        return "Demonstrates the minimal plugin contract."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Says hello.")
        def hello() -> str:
            return "hello from my-plugin"
```

## Loading Plugins

Use `Application.load_plugin(plugin)` to load a plugin instance into an application.

```python
app = quickli.Application(name="demo")
app.load_plugin(MyPlugin())
result = app.run(["hello"])
```

`load_plugin` performs the following steps in order:

1. Validates that the plugin `name` is not empty.
2. Validates that no plugin with the same `name` has already been loaded.
3. Calls `plugin.register(application)` to allow the plugin to register its resources.
4. Appends the plugin to the application's internal plugin list.

When step 3 raises any exception other than `PluginLoadError`, that exception is wrapped in
a `PluginLoadError` with an informative message. When `register` raises `PluginLoadError`
directly, it propagates unchanged.

## Inspecting Loaded Plugins

`Application.plugins` returns a copy of the loaded plugin list.

```python
for plugin in app.plugins:
    print(plugin.name, "-", plugin.description)
```

## Error Handling

| Situation | Exception raised |
|---|---|
| Plugin name is empty | `PluginLoadError` |
| Plugin with same name already loaded | `PluginLoadError` |
| `register` raises `PluginLoadError` | propagated unchanged |
| `register` raises any other exception | wrapped in `PluginLoadError` |

## Global Options and Plugins

When an application defines global options, plugin command handlers must declare the
corresponding parameters if they should receive those values:

```python
app = quickli.Application(
    name="demo",
    global_options=[quickli.Option("verbose", short_name="v", is_flag=True)],
)


class VerbosePlugin(quickli.Plugin):
    @property
    def name(self) -> str:
        return "verbose-plugin"

    @property
    def description(self) -> str:
        return "Plugin that respects the global verbose option."

    def register(self, application: quickli.Application) -> None:
        @application.command(help_text="Prints a message.")
        def hello(verbose: bool = False) -> str:
            msg = "hello"
            if verbose:
                msg = f"[verbose] {msg}"
            return msg
```

## Scope and Limitations

- Only explicit loading through `load_plugin` is supported in the current implementation.
- Discovery via Python package metadata (`importlib.metadata` entry points) is planned but
  not implemented.
- Plugins may not override commands registered by the application or by earlier plugins.
- The plugin contract is stable for the Alpha release. Breaking changes will be documented
  in the changelog.
