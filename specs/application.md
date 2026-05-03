# Application Specification

## Purpose

The application resource represents the installed CLI program.
It owns the command registry and acts as the single entry point for command execution.

## Responsibilities

- Maintain a unique registry of commands.
- Optionally expose a single application-level entrypoint without commands.
- Expose a declarative registration API.
- Route user input to the selected command.
- Render plain-text help output.
- Render command output in different formats such as plain text, JSON, YAML
- Aggregate command help into application-level help output.
- Parse application-level global options before command dispatch.

## Technical Notes

- The current implementation is intentionally minimal.
- Command lookup is string-based.
- Applications may run as commandless CLIs through a root entrypoint.
- Commands can define explicit argument and option resources.
- Applications can define explicit global option resources.
- Execution supports positional string arguments and named options.
- Options currently support `--long value`, `--long=value`, and `-s value` forms.
- Flags are represented as boolean options.
- Arguments and options may convert raw string input through callables.
- Help output includes generated usage, argument descriptions, and option descriptions.
- Global and local options are rendered separately in help output.
- Global options may appear before or after the command name.
- When both commands and an application entrypoint exist, command names take precedence and the entrypoint acts as a fallback.
- The resource must remain dependency-light and compatible with Python 3.12 to 3.14.

## Future Extensions

- Typed argument conversion beyond booleans and raw strings.
- Command Groups and Subcommands (nested commands)
- Nested command groups.
- Shell completion.
- Config-driven application setup.
