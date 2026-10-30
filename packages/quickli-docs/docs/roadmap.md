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

## Stability and fix release outline

The next stabilization release should improve developer experience without replacing existing
APIs. This is a release checklist, not a declaration of 1.0 stability.

1. **Audit the current contract**
   - Compare specifications, core documentation, and the official documentation package
     against implementation and tests.
   - Correct examples that refer to nonexistent `register_command`, `Option.metavar`, or
     `ConfigField.description` APIs.
   - Correct validator factory usage, positional defaults, JSON output envelopes, and
     `run()` versus `main()` behavior.
   - Remove contradictory TOML-only configuration claims.
2. **Harden configuration**
   - Preserve YAML, JSON, and TOML support and explicit format selection.
   - Report invalid document shapes, syntax, encoding, and file access errors clearly.
   - Offer opt-in `Application(config=..., auto_init_config=True)` registration of `init`,
     plus explicit `app.init_config()` when automatic command registration is disabled.
   - Preserve existing configuration files and existing command registration behavior.
3. **Make the documentation executable**
   - Provide automatic application, command, and nested `--help`/`-h`, preserving
     explicit aliases and escaped values; allow opt-out through `auto_help=False`.
   - Expand command registration, arguments, value options, flags, and validation examples.
   - Explain schema defaults, nested configuration limits, and explicit CLI overrides.
   - Provide standard-library logging and application packaging guides, including
     standalone binaries and containers.
   - Use ordered steps for workflows, highlighted code, and admonitions for limitations.
4. **Validate and review before publishing**
   - Run regression tests on Python 3.12, 3.13, and 3.14.
   - Run Ruff, build Python distributions, and build the Docusaurus site.
   - Resolve the existing core build warning: `pyproject.toml` names `README.md`, but
     `packages/core/README.md` is absent. Verify the packaged project description.
   - Exercise documented examples and inspect errors, stdout, stderr, and exit codes.
   - Review backward compatibility, security findings, and release notes.
   - Obtain maintainer/user acceptance before declaring the release ready.

:::note[Implemented versus planned]
Nested subcommands, automatic help flags, explicit plugin loading, combined short flags,
shell completion, and multi-format configuration already exist. Future work below extends
them; it does not describe missing baseline support.
:::

## Following priorities

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