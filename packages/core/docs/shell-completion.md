# Shell Completion

quiCkLI can generate shell completion scripts for **bash**, **zsh**, and **PowerShell**.
Shell completion lets users press <kbd>Tab</kbd> to auto-complete command names in their
terminal.

## Enabling Shell Completion

Pass `shell_completion=True` when constructing your `Application` to register the
built-in `shell-completion` command automatically.

```python
from quickli import Application

app = Application(name="myapp", shell_completion=True)


@app.command(help_text="Greets a user.")
def greet(name: str) -> str:
    return f"hello {name}"


@app.command(help_text="Shows the version.")
def version() -> str:
    return "0.1.0"
```

With `shell_completion=True` the application registers a `shell-completion` command that
accepts a shell name and prints the appropriate completion script to standard output.

## Generating Completion Scripts

### bash

```bash
myapp shell-completion bash >> ~/.bash_completion
source ~/.bash_completion
```

Or, for a system-wide installation:

```bash
myapp shell-completion bash | sudo tee /etc/bash_completion.d/myapp
```

### zsh

```zsh
myapp shell-completion zsh >> ~/.zshrc
source ~/.zshrc
```

Or place the script in a directory on `$fpath` as `_myapp`.

### PowerShell

```powershell
myapp shell-completion powershell >> $PROFILE
. $PROFILE
```

## Using `generate_completion` Directly

You can also call `Application.generate_completion(shell)` in your own runner script:

```python
import sys
from quickli import Application

app = Application(name="myapp", shell_completion=True)

# In a custom entry point that reads sys.argv:
if len(sys.argv) == 3 and sys.argv[1] == "shell-completion":
    print(app.generate_completion(sys.argv[2]))
    sys.exit(0)
```

## Standalone Generator Functions

The generator functions are also available as standalone helpers when you need more
control over how and when the script is produced.

```python
from quickli import generate_bash_completion, generate_zsh_completion
from quickli import generate_powershell_completion

bash_script = generate_bash_completion("myapp", ["greet", "version"])
zsh_script = generate_zsh_completion("myapp", {"greet": "Greet a user.", "version": ""})
ps_script = generate_powershell_completion("myapp", ["greet", "version"])
```

## Supported Shells

The `SUPPORTED_SHELLS` constant lists all recognised shell names:

```python
from quickli import SUPPORTED_SHELLS

print(SUPPORTED_SHELLS)  # ('bash', 'zsh', 'powershell')
```

Passing an unsupported shell name to `generate_completion` raises `ValueError`.

## Notes

- The `shell-completion` command itself appears in the generated completion list.
  This is intentional: users can complete `shell-completion` just like any other command.
- The `pwsh` alias is accepted as a synonym for `powershell` when calling
  `generate_completion` directly.
- The generated scripts complete top-level command names only.
  Argument and option completion within commands is not yet supported.
