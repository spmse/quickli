---
sidebar_position: 1
description: Overview of quiCkLI's core concepts and how they relate to each other.
keywords: [quickli, concepts, application, command, argument, option, plugin, hierarchy]
---

# quiCkLI Concepts

`quickli` is built from a small set of explicit concepts. Each concept has its own
documentation page so the model can evolve without overcrowding one document.

## Concept pages

- [Application](./application.md)
- [Command](./command.md)
- [Argument](./argument.md)
- [Option](./option.md)
- [Parsers](./parsers.md)
- [Plugin](./plugin.md)
- [Configuration Files](./config.md)
- [Comparing Click, argparse, and quickli](../comparison/overview.md)

## How the concepts fit together

Every `quickli` CLI has a single `Application` at its root. Commands live inside the
application. Each command owns its arguments and options. Plugins attach additional commands
to an existing application without changing its core.

```
Application
├── global options          ← named flags/values available to every command
├── Command "build"
│   ├── Argument "target"   ← required positional input
│   └── Option  "--output"  ← optional named input
├── Command "deploy"
│   ├── Subcommand "dev"
│   └── Subcommand "prod"
└── Plugin "metrics"
    └── Command "stats"
```

In a typical flow:

1. Create an `Application`.
2. Register one or more `Command` handlers (or a single root `entrypoint`).
3. Define each command's `Argument` and `Option` resources.
4. Run the application with command-line tokens (`argv`).

## When to use which concept

| You want to… | Use… |
|---|---|
| Build a tool with a single action | `Application` + `@app.entrypoint` |
| Build a tool with multiple actions | `Application` + `@app.command` |
| Accept positional input like a file path | `Argument` |
| Accept a named flag or setting | `Option` |
| Add behavior from a separate package | `Plugin` |
| Persist user settings between runs | `Config` |
| Parse or produce JSON, YAML, or TOML | `parsers` helpers |

:::note[Not sure where to start?]
Read [Getting Started](../getting-started.md) first, then come back here to explore the
individual concepts in detail.
:::
