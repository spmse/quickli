"""Shell completion script generators for quickli applications."""

from __future__ import annotations


SUPPORTED_SHELLS = ("bash", "zsh", "powershell")


def generate_bash_completion(app_name: str, command_names: list[str]) -> str:
    """Generates a bash completion script for the given application.

    The returned string should be sourced in a bash session or added to
    ``~/.bash_completion`` or ``/etc/bash_completion.d/``.

    Args:
        app_name: The name of the CLI application (used as the ``complete`` target).
        command_names: The list of top-level command names to complete.

    Returns:
        A bash completion script as a plain string.

    Example::

        script = generate_bash_completion("myapp", ["greet", "version"])
        print(script)
    """
    func_name = "_" + app_name.replace("-", "_").replace(" ", "_") + "_completion"
    commands = " ".join(command_names)
    return (
        f"# bash completion for {app_name}\n"
        f"{func_name}() {{\n"
        f'    local cur="${{COMP_WORDS[COMP_CWORD]}}"\n'
        f'    local commands="{commands}"\n'
        f'    if [ "${{COMP_CWORD}}" -eq 1 ]; then\n'
        f'        COMPREPLY=($(compgen -W "${{commands}}" -- "${{cur}}"))\n'
        f"    fi\n"
        f"}}\n"
        f"complete -F {func_name} {app_name}"
    )


def generate_zsh_completion(app_name: str, commands: dict[str, str]) -> str:
    """Generates a zsh completion script for the given application.

    The returned string should be placed in a file named ``_<app_name>`` on the
    ``$fpath`` or sourced directly in ``~/.zshrc``.

    Args:
        app_name: The name of the CLI application.
        commands: A mapping of command name to its description.

    Returns:
        A zsh completion script as a plain string.

    Example::

        script = generate_zsh_completion("myapp", {"greet": "Greet a user.", "version": ""})
        print(script)
    """
    func_name = "_" + app_name.replace("-", "_").replace(" ", "_")
    command_specs = "\n".join(
        f"        '{name}:{desc if desc else 'No description provided.'}'"
        for name, desc in commands.items()
    )
    commands_block = f"\n{command_specs}\n    " if command_specs else ""
    return (
        f"# zsh completion for {app_name}\n"
        f"#compdef {app_name}\n\n"
        f"{func_name}() {{\n"
        f"    local -a commands\n"
        f"    commands=({commands_block})\n"
        f"    _describe 'command' commands\n"
        f"}}\n\n"
        f"{func_name}"
    )


def generate_powershell_completion(app_name: str, command_names: list[str]) -> str:
    """Generates a PowerShell completion script for the given application.

    The returned string should be added to the PowerShell profile (``$PROFILE``)
    or dot-sourced in a session.

    Args:
        app_name: The name of the CLI application.
        command_names: The list of top-level command names to complete.

    Returns:
        A PowerShell completion script as a plain string.

    Example::

        script = generate_powershell_completion("myapp", ["greet", "version"])
        print(script)
    """
    commands_str = ", ".join(f"'{name}'" for name in command_names)
    return (
        f"# PowerShell completion for {app_name}\n"
        f"Register-ArgumentCompleter -Native -CommandName {app_name} -ScriptBlock {{\n"
        f"    param($wordToComplete, $commandAst, $cursorPosition)\n"
        f'    @({commands_str}) | Where-Object {{ $_ -like "$wordToComplete*" }}'
        f" | ForEach-Object {{\n"
        f"        [System.Management.Automation.CompletionResult]::new("
        f"$_, $_, 'ParameterValue', $_)\n"
        f"    }}\n"
        f"}}"
    )
