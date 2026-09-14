---
sidebar_position: 2
description: Application is the root container and execution manager of every quiCkLI CLI.
keywords: [quickli, application, entrypoint, command registration, run, main, global options, shell completion]
---

# Application

`Application` is the root CLI container and execution manager in `quickli`. It sits at the top of the concept hierarchy: everything else — commands, global options, plugins, and execution options — is registered against or configured within an `Application` instance.

```
Application   ← you are here
├── global_options
├── Command / Subcommand
├── Entrypoint (fallback / single-action)
└── Plugin
```

## What Application Owns

- **Command Registry**: Manages registered **[Command](./command.md)** objects and prevents duplicate command names.
- **Root Entrypoint**: Supports single-action CLIs via `@app.entrypoint`.
- **Global Options**: Defines application-wide **[Option](./option.md)** flags/values available to all commands.
- **Command Dispatch**: Parses `argv` tokens, matches commands/subcommands, and binds arguments and options to handlers.
- **Help Rendering**: Automatically generates structured help text for the application and all registered commands.
- **Shell Completion**: Optionally generates tab-completion scripts for `bash`, `zsh`, and `powershell`.
- **Execution Lifecycles**: Provides `run()` for library/testing use and `main()` for executable CLIs.

## Application Construction Parameters

When instantiating `Application`, you can customize several core behaviors:

```python
from quickli import Application, Option

app = Application(
    name="mytool",
    description="A multi-purpose developer CLI.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
    shell_completion=True,
    auto_sys_argv=True,
    error_handler=None,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | `"app"` | The binary/application name used in help text and usage lines. |
| `description` | `str \| None` | `None` | Short description shown at the top of application help output. |
| `global_options` | `list[Option] \| None` | `None` | List of global **[Option](./option.md)** definitions available to all commands. |
| `shell_completion` | `bool` | `False` | When `True`, automatically registers a built-in `shell-completion` command. |
| `auto_sys_argv` | `bool` | `True` | When `True`, `run()` reads `sys.argv[1:]` by default when `argv` is `None`. |
| `error_handler` | `Callable \| None` | `None` | Optional error callback that can inspect or adapt exceptions before `main()` renders them. |

## Command Registration Methods

`Application` supports four distinct ways to author and register commands:

### 1. Decorator Registration (`@app.command`)

The most common way to register named commands in multi-command tools.

```python
from quickli import Application, Argument, Option

app = Application(name="demo")

@app.command(
    name="greet",
    help_text="Greet a user by name.",
    arguments=[Argument("name")],
    options=[Option("shout", is_flag=True)],
)
def greet_user(name: str, shout: bool = False) -> str:
    msg = f"Hello, {name}!"
    return msg.upper() if shout else msg
```

### 2. Imperative Command Registration (`app.register_command`)

Useful when commands are constructed dynamically or created in separate modules using the `Command` class.

```python
from quickli import Application, Command, Argument

app = Application(name="demo")

build_cmd = Command(
    name="build",
    help_text="Build the target artefact.",
    arguments=[Argument("target")],
    handler=lambda target: f"building {target}…",
)

app.register_command(build_cmd)
```

### 3. Root Entrypoint Registration (`@app.entrypoint`)

Used for single-action tools (like `cat` or `head`) that do not require command names.

```python
from quickli import Application, Argument

app = Application(name="quickhead")

@app.entrypoint(
    arguments=[Argument("file_path")],
)
def main_action(file_path: str) -> str:
    return f"Reading top lines of {file_path}"

print(app.run(["notes.txt"]))
```

:::note[Command Precedence with Entrypoints]
When an `Application` defines both commands and a root entrypoint, input tokens matching a registered command name dispatch to that command. If no command name matches, the tokens fallback to the root entrypoint.
:::

### 4. Plugin Registration (`app.load_plugin`)

Used to attach external command modules via the **[Plugin](./plugin.md)** contract.

```python
from quickli import Application, Plugin

class AuditPlugin(Plugin):
    @property
    def name(self) -> str:
        return "audit"
    
    @property
    def description(self) -> str:
        return "Security audit commands"

    def register(self, application: Application) -> None:
        @application.command(help_text="Run security check.")
        def check() -> str:
            return "audit passed"

app = Application(name="demo")
app.load_plugin(AuditPlugin())
```

## Global Options

Global options apply across the entire application and can be passed before or after the command name:

```python
app = Application(
    name="demo",
    global_options=[
        Option("config", short_name="c", help_text="Path to configuration file."),
        Option("verbose", short_name="v", is_flag=True, help_text="Verbose logging."),
    ],
)

@app.command(help_text="Perform deployment.")
def deploy(config: str | None = None, verbose: bool = False) -> str:
    return f"deploying (config={config}, verbose={verbose})"

# Both token orders are valid:
print(app.run(["--verbose", "deploy", "-c", "app.toml"]))
print(app.run(["deploy", "-c", "app.toml", "--verbose"]))
```

:::info[Global Option Availability]
Global options are automatically injected into handler signatures when the handler accepts parameters matching the global option names. See **[Option](./option.md#global-and-local-options)** for more details.
:::

## Execution Models: `run()` vs `main()`

`Application` explicitly separates library-level command execution from executable entrypoints:

```
                  ┌──────────────────────┐
                  │  sys.argv / input    │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   app.run(argv)                   app.main(argv, format)
┌──────────────────────┐        ┌───────────────────────────┐
│ - Pure execution     │        │ - Calls run()             │
│ - Returns string/text│        │ - Prints stdout           │
│ - No print or exit   │        │ - Handles exit codes      │
│ - Ideal for testing  │        │ - Supports JSON output    │
└──────────────────────┘        └───────────────────────────┘
```

### `Application.run(argv=None)`

Runs the command dispatch loop and returns the string output or help text.

- **Arguments**: `argv` (`list[str] | None`). If `None` and `auto_sys_argv=True`, reads `sys.argv[1:]`.
- **Side effects**: None (does not print to stdout/stderr and does not terminate the process).
- **Return value**: The return value of the matched command handler (coerced to string) or generated help text.

```python
# Pure string execution — ideal for unit tests:
output = app.run(["greet", "Alice"])
assert output == "Hello, Alice!"
```

### `Application.main(argv=None, output_format="text")`

Provides an executable wrapper suitable for CLI binaries (`if __name__ == "__main__":`).

- **Output handling**: Prints successful results directly to standard output.
- **Exit codes**: Returns `0` on success, or non-zero error exit codes on failure.
- **Machine-readable output**: Pass `output_format="json"` to emit JSON payloads for automated agents or scripts.
- **Error transformation**: Converts unhandled exceptions into structured `UserCodeError` or `InternalCLIError` instances.

```python
if __name__ == "__main__":
    app.main()
```

#### JSON Output Format Example

```python
app.main(argv=["greet", "Alice"], output_format="json")
# Outputs JSON payload:
# {"status": "success", "result": "Hello, Alice!"}
```

## Built-in Shell Completion

When constructed with `shell_completion=True`, the `Application` automatically registers a `shell-completion` command:

```python
app = Application(name="mycli", shell_completion=True)

# Generate completion script programmatically:
bash_script = app.generate_completion("bash")
zsh_script = app.generate_completion("zsh")
ps_script = app.generate_completion("powershell")
```

Users can generate shell completion scripts directly from the CLI:

```bash
mycli shell-completion bash > /etc/bash_completion.d/mycli
```

:::tip[Testing Shell Completion]
The standalone completion generators `generate_bash_completion`, `generate_zsh_completion`, and `generate_powershell_completion` are also available from top-level `quickli`.
:::

## Custom Error Handlers

You can pass a custom `error_handler` callback to `Application` to process or format exceptions before `main()` outputs them:

```python
def log_and_format_error(error: Exception) -> str | None:
    print(f"[LOG] CLI error encountered: {error}")
    return f"Custom Error Message: {error}"

app = Application(name="demo", error_handler=log_and_format_error)
```

## Where to Go Next

- Define named actions using **[Command](./command.md)** and **[Subcommand](./command.md#nested-subcommands)**.
- Accept positional arguments using **[Argument](./argument.md)**.
- Accept flags and options using **[Option](./option.md)**.
- Persist settings across runs with **[Config](./config.md)**.
- Modularize your application with **[Plugin](./plugin.md)**.

