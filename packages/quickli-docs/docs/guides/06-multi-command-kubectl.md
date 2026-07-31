---
id: guide-multi-command-cli
title: "Guide 6: Multi-Command CLI (pyk5l)"
sidebar_position: 7
description: >
  Build a kubectl-like multi-command CLI with quickli. Learn named commands with
  @app.command, global options shared across commands, custom validators, and
  CommandExecutionError for domain-level errors.
keywords: [quickli, tutorial, multi-command, kubectl, commands, global options, validators]
---

# Guide 6: Multi-Command CLI (pyk5l)

This guide builds `pyk5l`, a kubectl-like CLI that demonstrates how `quickli` handles a
realistic multi-command application. It combines everything from the earlier guides —
global options, validators, converters, and repeatable options — across multiple named
commands.

You will learn how to:
- register **multiple named commands** with `@app.command`
- share **global options** across all commands
- write **custom validator factories** (`one_of`, `label_selector`)
- raise `CommandExecutionError` for expected domain-level failures
- split complex logic into private helper functions

The full source for this example is in the repository at
[`packages/core/examples/complex/pyk5l/app.py`](https://github.com/spmse/quickli/blob/main/packages/core/examples/complex/pyk5l/app.py).

## Overview

`pyk5l` provides four commands:

| Command | What it does |
|---|---|
| `get` | List pods or services in a namespace |
| `describe` | Show detailed information about a named pod |
| `logs` | Print recent log lines from a pod |
| `apply` | Preview a manifest before a simulated apply |

Global options (`--context`, `--namespace`, `--output`, `--verbose`) apply to every
command.

## Application setup

```python
app = Application(
    name="pyk5l",
    description="A minimal kubectl-like CLI built with quickli.",
    global_options=[
        Option("context", short_name="c", default="dev-cluster", help_text="Cluster context."),
        Option("namespace", short_name="n", default="default", help_text="Namespace to target."),
        Option(
            "output",
            short_name="o",
            default="table",
            validators=[one_of("table", "json", "wide")],
            help_text="Output mode for list commands.",
        ),
        Option("verbose", short_name="v", is_flag=True, help_text="Print execution context."),
    ],
)
```

Global options are declared once on `Application`. Every command handler receives them as
parameters — the handler simply declares the parameter with the right name.

## Custom validators

### `one_of`

```python
def one_of(*choices: str):
    allowed = tuple(choices)
    description = "one of: " + ", ".join(allowed)

    def validate(value: object) -> object:
        if value not in allowed:
            raise ValueError(f"Expected one of: {', '.join(allowed)}")
        return value

    validate.description = description
    return validate
```

`one_of` is a validator factory: it returns a function that checks whether the value is
one of the allowed choices. Setting `validate.description` provides a human-readable
string that quickli uses in error messages and help output.

### `label_selector`

```python
def label_selector():
    description = "label selector in key=value form"

    def validate(value: object) -> object:
        if not isinstance(value, str) or "=" not in value:
            raise ValueError("Expected a selector in key=value form")
        key, selected_value = value.split("=", 1)
        if not key or not selected_value:
            raise ValueError("Expected a selector in key=value form")
        return value

    validate.description = description
    return validate
```

`label_selector` validates that the value matches a `key=value` format. The validator
only checks the shape of the input, not whether the key or value are meaningful — that is
the application's responsibility.

## Registering commands

### `get`

```python
@app.command(
    name="get",
    help_text="List resources in the selected namespace.",
    arguments=[
        Argument(
            "resource",
            help_text="Resource kind to list, for example pods or services.",
            validators=[GET_RESOURCE_VALIDATOR],
        )
    ],
    options=[
        Option(
            "selector",
            short_name="l",
            multiple=True,
            validators=[label_selector()],
            help_text="Filter pods with one or more label selectors.",
        ),
        ...
    ],
)
def get(resource: str, ..., context: str = "dev-cluster", namespace: str = "default", ...) -> str:
    ...
```

`@app.command` differs from `@app.entrypoint` by accepting a `name` argument. The
command name is the first token after the program name on the command line:

```bash
python app.py get pods
python app.py get services --output json
```

The `name` parameter is optional; when omitted, quickli uses the function name.

### `CommandExecutionError`

```python
def _find_pod(name: str, namespace: str) -> Pod:
    for pod in PODS:
        if pod.namespace == namespace and pod.name == name:
            return pod
    raise CommandExecutionError(f"Pod '{name}' was not found in namespace '{namespace}'.")
```

`CommandExecutionError` signals an expected, domain-level failure. quickli does not wrap
it — the application can catch it at the call site and convert it to an exit code or a
user-facing message.

## Run it

Clone the repository and run with a sample manifest:

```bash
cd packages/core/examples/complex/pyk5l

# List pods
python app.py get pods

# List pods in a specific namespace
python app.py get pods --namespace ops

# Filter by label
python app.py get pods --selector app=api

# Output as JSON
python app.py get pods --output json

# Describe a pod
python app.py describe pod api-7d4f5f6b89-l2xq9

# Print logs
python app.py logs api-7d4f5f6b89-l2xq9 --tail 3 --timestamps

# Apply a manifest (dry run)
python app.py apply manifests/web-pod.yaml --dry-run

# Show context information
python app.py get services --verbose
```

## Design principles this example demonstrates

1. **One handler per command** — each handler does one thing and receives its inputs
   directly as typed parameters.
2. **Validators at the boundary** — all input validation happens via registered validators,
   not in the handler body.
3. **Helper functions for rendering** — private `_render_*` functions keep the handler
   logic readable.
4. **`CommandExecutionError` for domain errors** — domain-level failures use an explicit
   exception type, not a special return value.

## Summary

You have now seen the full range of `quickli` features:

- `Application`, `Command`, `Argument`, `Option`
- `@app.entrypoint` and `@app.command`
- Global options shared across commands
- Built-in validators: `file_path`, `directory_path`, `positive_number`
- Custom validator factories
- Converters: `int`, `Path`
- Repeatable options: `multiple=True`
- `CommandExecutionError` for domain errors

Explore the [concept reference](../concepts/quickli-concepts.md) for the complete API
documentation, or check the [blog](../../blog) for deeper dives into specific features.
