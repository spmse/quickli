# ADR 0002: Plugin API Design

## Status

Accepted

## Context

Issue [#22](https://github.com/spmse/quickli/issues/22) requested a rudimentary plugin
loading mechanism, an official plugin API contract, and documentation covering both the
plugin system and how to author plugins.

The project needed to decide:

- How plugins are discovered and loaded.
- What contract plugin authors must implement.
- How errors in plugin loading are reported.
- How the plugin system relates to the existing `Application`, `Command`, `Argument`, and
  `Option` abstractions.

## Decision

### Plugin contract

Every plugin must subclass `quickli.Plugin`, an abstract base class that requires three
members:

| Member | Kind | Description |
|---|---|---|
| `name` | `str` property | Unique, non-empty plugin identifier |
| `description` | `str` property | Short description of what the plugin provides |
| `register(application)` | method | Registers commands and resources against the app |

Using an abstract base class (rather than a protocol or duck-typed interface) was chosen
because it produces clear `TypeError` messages when a plugin author forgets to implement
a required method, and it keeps the contract explicit and inspectable.

### Loading mechanism

`Application.load_plugin(plugin)` is the sole public entry point for loading a plugin.
It validates the plugin name, prevents duplicate loading, calls `plugin.register(self)`,
and appends the plugin to an internal list.

Discovery via Python package metadata (`importlib.metadata` entry points) was considered
but deferred.  Automatic discovery adds complexity and security considerations that are
out of scope for the Alpha milestone.

### Error handling

A new `PluginLoadError(CLIError)` exception was introduced.  Any exception raised during
`register` is wrapped in `PluginLoadError` to give callers a single exception type to
catch at the plugin-loading boundary.  If `register` raises `PluginLoadError` directly,
it propagates unchanged so that plugin authors can signal intentional failures with a
precise message.

### Placement of plugin state

Loaded plugins are tracked in `Application._plugins` (a `list[Plugin]`).
`Application.plugins` returns a copy to prevent external mutation.

## Options Considered

| Option | Summary | Rejected because |
|---|---|---|
| Protocol-based contract | Use `typing.Protocol` instead of ABC | Less helpful error messages for missing methods |
| Entry point discovery | Auto-discover plugins via `importlib.metadata` | Adds security and dependency complexity; deferred |
| Plugin manager class | Separate `PluginManager` object | Unnecessary indirection for a minimal framework |
| Decorator registration | `@app.plugin` decorator | Less readable for multi-command plugins |

## Consequences

- Plugin authors must subclass `quickli.Plugin` and implement `name`, `description`, and
  `register`.
- Applications load plugins explicitly; there is no automatic discovery in Alpha.
- `PluginLoadError` joins the exception hierarchy under `CLIError`.
- `Application.plugins` exposes the loaded plugin list as a read-only copy.
- Entry point discovery remains a documented follow-up item.
- The `plugin_loading` capability moves from `not_implemented` to `implemented` in the
  feature summary.
