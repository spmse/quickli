# Command Specification

## Purpose

The command resource wraps one callable and provides a stable execution contract for
the application.

## Responsibilities

- Store the public command name.
- Store user-facing help text.
- Store argument and option resource definitions.
- Validate the handler call signature before execution.
- Parse command line tokens into positional arguments and option values.
- Generate detailed help output from the registered resources.
- Delegate execution to the underlying callable.

## Technical Notes

- Commands are registered under unique names.
- Names are normalized from function names by replacing underscores with hyphens.
- Validation uses Python signature binding after parsing resource values.
- Unknown options and missing required resources raise execution errors.
- Help output exposes generated usage and resource metadata such as required and default values.
- Help text falls back to the handler docstring when no explicit `help_text` is given.
- Local options are parsed after the command name.
- Repeatable options can accumulate multiple values.
- Global options may be filtered out from the command token stream before local parsing.

## Future Extensions

- Async command execution.
- Structured command result objects.
- Repeated arguments.
- Combined short flags.
