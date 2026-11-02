---
id: roadmap
title: Development Roadmap
sidebar_position: 3
description: Planned steps for the next stages of quickli development.
---

# Development Roadmap

quickli is an Alpha project. This roadmap describes the next planned steps rather than
promising fixed delivery dates. Each step will be implemented, tested, documented, and
reviewed before it is treated as complete.

:::note[Implemented versus planned]
Nested subcommands, automatic help flags, explicit plugin loading, combined short flags,
shell completion, and multi-format configuration already exist. Future work below extends
them; it does not describe missing baseline support.
:::

## Future priorities

- Layered configuration with an explicit file/environment/CLI precedence model.
- Shell completion for arguments and options, beyond registered top-level commands.
- Plugin discovery, beyond explicit `app.load_plugin(...)`.
- Clearer unknown-command errors.

For example, `app.run(["--help"])` and `app.run(["command", "-h"])` already return help
without executing handlers. Unknown-command error refinements remain separate work.

## How priorities are chosen

The project favors changes that improve the learning experience and keep the core small.
New behavior should have a written specification, focused unit tests, runnable examples, and
updated documentation. Planned items may be reordered as feedback and implementation risks
become clearer.