---
sidebar_position: 2
description: Application is the root container of every quiCkLI CLI.
keywords: [quickli, application, entrypoint, command registration, run]
---

# Application

`Application` is the root CLI container in `quickli`. It sits at the top of the concept
hierarchy: everything else — commands, arguments, options, and plugins — is registered
against an `Application` instance.

```
Application   ← you are here
├── Command
├── Command
└── Plugin
```

## What it owns

- command registration
- optional root entrypoint registration
- application-level global options
- command dispatch from input tokens
- application and command help rendering

## Execution model

`Application.run(argv)` accepts explicit command-line tokens and returns the selected
handler result (or generated help text).

- It does **not** read `sys.argv` itself.
- It does **not** print output by default.
- It does **not** choose process exit codes.

That boundary keeps runtime behavior explicit in your executable wrapper.

## Registration API

`Application` offers decorator APIs for command registration:

- `@app.command(...)` for named commands in a multi-command CLI
- `@app.entrypoint(...)` for a commandless root flow

When both exist, command names take precedence, and the entrypoint acts as fallback.

## Single-action tool example

Use `@app.entrypoint` when your tool does exactly one thing and does not need named
subcommands.

```python
from quickli import Application, Argument

app = Application(name="greet")


@app.entrypoint(arguments=[Argument("name")])
def main(name: str) -> str:
    return f"Hello, {name}!"


print(app.run(["Alice"]))  # Hello, Alice!
```

## Multi-command tool example

Use `@app.command` when your tool exposes several distinct actions, such as `build`,
`deploy`, and `clean`.

```python
from quickli import Application

app = Application(name="mytool")


@app.command(help_text="Build the project.")
def build() -> str:
    return "building…"


@app.command(help_text="Clean build artefacts.")
def clean() -> str:
    return "cleaning…"


print(app.run(["build"]))  # building…
```

## Tips

:::tip Single action vs. multiple commands
Use `@app.entrypoint` for a single-action tool (like `cat` or `head`) and `@app.command`
for a multi-action tool (like `git` or `kubectl`). You can always add commands later — the
entrypoint acts as a fallback when no command name matches.
:::

:::tip Wrapping `run()` in an executable
`Application.run()` returns a string result. Printing and exit-code handling belong to your
`main()` wrapper so that the application stays independently testable.

```python
import sys


def main() -> None:
    result = app.run(sys.argv[1:])
    print(result)


if __name__ == "__main__":
    main()
```
:::

## Where to go next

- Add **[Commands](./command.md)** to give your application named actions.
- Add **[Arguments](./argument.md)** and **[Options](./option.md)** to accept input.
- Use **[Plugins](./plugin.md)** to load reusable command sets without modifying the core.
