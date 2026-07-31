---
title: "Getting Started with quiCkLI: Multi-Command Applications"
description: >
  Build a kubectl-like CLI with multiple named commands, shared global options, custom
  validators, and explicit error handling. This final part of the Getting Started series
  shows how all the quickli primitives fit together.
slug: quickli-tutorial-03-multi-command-cli
authors:
  - name: quiCkLI contributors
    url: https://github.com/spmse/quickli
date: 2025-08-15
draft: true
tags: [tutorial, quickli, python, cli, multi-command, commands]
series:
  name: "Getting Started with quiCkLI"
  position: 3
keywords: [quickli, multi-command CLI, app.command, CommandExecutionError, python tutorial]
---

In the first two parts of this series you built a greeting tool and a file viewer. In this
final article you will combine everything you have learned to build `pyk5l`, a
kubectl-like multi-command application.

By the end you will understand every primitive in `quickli` and how they fit together in
a realistic application.

<!-- truncate -->

## What you will build

```bash
python app.py get pods
python app.py get pods --output json --namespace ops
python app.py describe pod api-7d4f5f6b89-l2xq9
python app.py logs api-7d4f5f6b89-l2xq9 --tail 5 --timestamps
python app.py apply manifests/web-pod.yaml --dry-run
```

## `@app.command` vs `@app.entrypoint`

Until now you used `@app.entrypoint`, which registers a single handler for the whole
application. When you need multiple commands, use `@app.command` instead:

```python
@app.command(
    name="get",
    help_text="List resources in the selected namespace.",
    arguments=[...],
    options=[...],
)
def get(resource: str, ...) -> str:
    ...
```

The `name` parameter becomes the first token on the command line. Omitting `name` uses
the function name. You can register as many commands as you need.

## Custom validator factories

quickli ships with built-in validators (`file_path`, `positive_number`, and others), but
you can write your own using the same pattern:

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

A validator factory returns a callable that:
1. Receives the converted value.
2. Returns the value unchanged if it is valid.
3. Raises `ValueError` with a clear message if it is not.

Setting `validate.description` provides the text that appears in help and error output.

## `CommandExecutionError`

`CommandExecutionError` is for expected domain-level failures — not programming errors:

```python
def _find_pod(name: str, namespace: str) -> Pod:
    for pod in PODS:
        if pod.namespace == namespace and pod.name == name:
            return pod
    raise CommandExecutionError(
        f"Pod '{name}' was not found in namespace '{namespace}'."
    )
```

This exception propagates unchanged out of `Application.run()`. Your application wrapper
can catch it and turn it into an exit code:

```python
import sys
try:
    print(app.run(sys.argv[1:]))
except quickli.CommandExecutionError as error:
    print(f"Error: {error}", file=sys.stderr)
    sys.exit(1)
```

## Global options shared across commands

Declare options once on `Application`. Every command handler that needs them declares the
same parameter name:

```python
app = Application(
    name="pyk5l",
    global_options=[
        Option("namespace", short_name="n", default="default"),
        Option("output", short_name="o", default="table",
               validators=[one_of("table", "json", "wide")]),
        Option("verbose", short_name="v", is_flag=True),
    ],
)

@app.command(name="get", ...)
def get(resource: str, namespace: str = "default", output: str = "table",
        verbose: bool = False) -> str:
    ...

@app.command(name="describe", ...)
def describe(resource: str, name: str, namespace: str = "default",
             verbose: bool = False, output: str = "table") -> str:
    ...
```

quickli matches global option names to parameter names for each command.

## Full source

The complete example is at
[`packages/core/examples/complex/pyk5l/app.py`](https://github.com/spmse/quickli/blob/main/packages/core/examples/complex/pyk5l/app.py).
Try it:

```bash
git clone https://github.com/spmse/quickli.git
cd quickli
pip install -e packages/core
cd packages/core/examples/complex/pyk5l
python app.py get pods
```

## What you learned

- `@app.command` registers named commands in a multi-command application.
- Custom validator factories follow the same pattern as built-in validators.
- `CommandExecutionError` signals expected domain-level failures.
- Global options declared on `Application` are available to every command handler.

## The complete quiCkLI primitives

| Primitive | Purpose |
|---|---|
| `Application` | Root container; owns dispatch and registration |
| `Command` | Named operation (registered via `@app.command`) |
| `Argument` | Positional, ordered input |
| `Option` | Named input; flags, repeatable values, converters, validators |
| `Plugin` | Reusable command bundle loaded into an application |

Read the [concept reference](/docs/concepts/quickli-concepts) for the full API or explore
the [implementation guides](/docs/guides) to follow along with each example in detail.
