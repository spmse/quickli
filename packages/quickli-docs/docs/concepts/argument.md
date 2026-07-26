---
sidebar_position: 4
---

# Argument

`Argument` describes a positional input value for a command.

## Core behavior

- Arguments are positional and ordered.
- They may be required or optional.
- An argument becomes optional when it has a default value.
- A converter can transform raw text before handler invocation.
- Validators can check converted values.

## Typical usage

Use arguments for required command context, such as paths, identifiers, or target names:

- source file path
- resource name
- numeric input for an operation

If required arguments are missing, command execution fails with a deterministic error.
