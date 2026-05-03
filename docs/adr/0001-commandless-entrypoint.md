# ADR 0001: Support Commandless Applications Through a Root Entrypoint

## Status

Accepted

## Context

quickli aims to stay small, educational, and useful for everyday command-line tools.
Many common CLIs such as `cat`, `ls`, `mkdir`, or `head` do not expose subcommands.
They operate directly from the application root and still need the same capabilities as a
subcommand-based interface:

- positional arguments
- named options
- generated help output
- conversion and validation
- consistent error handling

The original application model centered on explicit commands. That worked for tools such
as `git version`, but it added unnecessary ceremony for single-purpose programs. A user
had to define a command even when the executable only had one action.

We needed a design that supports both styles without splitting the programming model into
two unrelated APIs.

## Decision

quickli supports a root-level application handler through `Application.entrypoint(...)`.

The root entrypoint uses the same resource model as named commands:

- `Argument` for positional input
- `Option` for named input
- `converter` for type conversion
- `validators` for post-conversion checks

The application may therefore run in one of two modes:

1. commandless mode through a registered root entrypoint
2. multi-command mode through one or more registered commands

Global options continue to belong to `Application` and can be used with either mode.

## Options Considered

### Option 1: Require Explicit Commands For Every CLI

Benefits:

- one conceptual execution path
- slightly simpler dispatcher implementation

Risks:

- poor fit for classic Unix-style tools
- unnecessary boilerplate for simple applications
- examples become harder to teach because even `cat`-like tools must pretend to be
  subcommand-based

### Option 2: Add A Separate Single-Command API Unrelated To Commands

Benefits:

- commandless applications can look minimal
- multi-command applications remain unchanged

Risks:

- duplicated concepts and parsing logic
- inconsistent help and validation behavior between APIs
- higher documentation burden because users must choose between two distinct models

### Option 3: Reuse The Command Model At The Application Root

Benefits:

- one resource model for both commandless and multi-command CLIs
- examples stay small without losing features
- help, validation, and conversion remain consistent

Risks:

- application dispatch becomes slightly more complex
- documentation must explain when to choose `entrypoint(...)` versus `command(...)`

## Consequences

Positive consequences:

- quickli can model classic tools naturally
- examples such as `cat`, `ls`, `mkdir`, and `head` map directly to the framework
- validation and help output work the same way at the root and command levels
- the public API stays small because users learn one resource model

Tradeoffs:

- `Application.run(...)` must decide whether to dispatch to a command or the root
  entrypoint
- help rendering must describe both commandless and multi-command applications clearly

Follow-up consequences:

- documentation should clearly recommend `entrypoint(...)` for single-purpose tools
- future plugin work must define how plugins interact with commandless applications

## Examples

Commandless application:

```python
from quickli import Application, Argument, file_path

app = Application(name="quickcat")


@app.entrypoint(arguments=[Argument("source", validators=[file_path()])])
def quickcat(source):
    return source.read_text(encoding="utf-8")
```

Multi-command application:

```python
from quickli import Application

app = Application(name="demo")


@app.command(name="version")
def version():
    return "0.1.0"
```