---
sidebar_position: 1
description: Comprehensive overview of quiCkLI's core concepts and how they relate to each other.
keywords: [quickli, concepts, application, command, argument, option, config, parsers, plugin, hierarchy]
---

# quiCkLI Concepts

`quickli` is built from a small set of explicit, modular concepts. Each concept represents a focused building block in your CLI architecture, ensuring clarity, testability, and extensibility without speculative abstractions.

```
Application
├── global_options           ← application-wide flags/values
├── Command "build"
│   ├── Argument "target"    ← positional required input
│   └── Option "--output"    ← named local flag or setting
├── Command "env"
│   └── Subcommand "create"  ← nested action under parent command
├── Plugin "metrics"
│   └── Command "stats"      ← external commands attached via plugin contract
├── Config                   ← persistent TOML config loaded at application startup
└── Parsers                  ← format helpers (JSON, YAML, TOML) used inside handlers
```

## Core Concept Hierarchy

Every `quickli` CLI has a single **[Application](./application.md)** instance at its root. 

- **[Application](./application.md)** owns the command registry, handles global options, dispatches command tokens, and manages the execution lifecycle (`run()` vs `main()`).
- **[Command](./command.md)** wraps an individual CLI operation. Commands define positional **[Argument](./argument.md)** resources and named **[Option](./option.md)** resources, and can contain nested **[Subcommand](./command.md#nested-subcommands)** trees.
- **[Argument](./argument.md)** represents required or optional positional input passed to a command in a fixed order.
- **[Option](./option.md)** represents named, order-independent input (such as `--verbose` or `--output=file.txt`). Options can be **local** to a command or **global** across the application.
- **[Config](./config.md)** manages persistent TOML settings on disk, using a `ConfigSchema` to validate user configuration on startup.
- **[Parsers](./parsers.md)** provide utility functions (`load_json`, `render_yaml`, `load_toml`, etc.) to parse and format structured data within handlers or converters.
- **[Plugin](./plugin.md)** allows external packages or modules to attach new commands to an `Application` without modifying the core application code.

## When to Use Which Concept

| Goal / Requirement | Recommended Concept | Concept Page |
|---|---|---|
| Single-action CLI tool (like `cat` or `head`) | `Application` + `@app.entrypoint` | [Application](./application.md) |
| Multi-action CLI tool (like `git` or `kubectl`) | `Application` + `@app.command` | [Application](./application.md) / [Command](./command.md) |
| Accept required or optional positional input | `Argument` | [Argument](./argument.md) |
| Accept optional named flags, toggles, or key-value settings | `Option` | [Option](./option.md) |
| Define flags that apply to *all* commands in the CLI | Global `Option` on `Application` | [Option](./option.md#global-and-local-options) |
| Persist user settings to a TOML file across runs | `Config` + `ConfigSchema` | [Config](./config.md) |
| Parse or produce JSON, YAML, or TOML data within a command | `parsers` helpers | [Parsers](./parsers.md) |
| Package reusable commands across teams or projects | `Plugin` | [Plugin](./plugin.md) |

:::info[Explicit Architecture]
`quickli` avoids hidden magic and silent assumptions. Resource definitions (`Argument`, `Option`, `ConfigField`) explicitly declare types, defaults, converters, and validators so that help text, parsing, and signature binding remain completely deterministic.
:::

:::tip[Separation of Execution Models]
When executing a CLI, `Application.run()` executes the selected command and returns its string result without printing or calling `sys.exit()`. This makes unit testing straightforward. For production binaries, `Application.main()` wraps `run()` with standard output formatting, structured error handling, and process exit codes. See the **[Application](./application.md#execution-models-run-vs-main)** documentation for details.
:::

:::note[Where to Start]
If you are new to `quickli`, start with the **[Getting Started](../getting-started.md)** guide to build your first CLI, then reference these concept pages to explore advanced capabilities.
:::

## Concept Index

- **[Application](./application.md)** — Root CLI container, registration APIs, global options, and execution models.
- **[Command](./command.md)** — Command authoring, docstrings, subcommands, signature binding, and validation.
- **[Argument](./argument.md)** — Positional inputs, converters, built-in validators, and metavar formatting.
- **[Option](./option.md)** — Short/long options, boolean flags, repeatable flags/values, local vs global scope.
- **[Config](./config.md)** — Native TOML configuration files, field validation, auto-initialization, and schema JSON.
- **[Parsers](./parsers.md)** — Format helpers for JSON, YAML, and TOML serialization and deserialization.
- **[Plugin](./plugin.md)** — Plugin contract, registration lifecycle, duplicate protection, and error handling.

