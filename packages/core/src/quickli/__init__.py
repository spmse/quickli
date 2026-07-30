"""Public package interface for quickli."""

from quickli.argument import Argument
from quickli.application import Application
from quickli.command import Command, Subcommand
from quickli.exceptions import CLIError, CommandExecutionError, CommandNotFoundError
from quickli.exceptions import CommandRegistrationError
from quickli.option import Option
from quickli.shell_completion import (
    SUPPORTED_SHELLS,
    generate_bash_completion,
    generate_powershell_completion,
    generate_zsh_completion,
)
from quickli.validators import directory_path, file_path, number_range, positive_number

__all__ = [
    "Argument",
    "Application",
    "CLIError",
    "Command",
    "Subcommand",
    "CommandExecutionError",
    "CommandNotFoundError",
    "CommandRegistrationError",
    "Option",
    "SUPPORTED_SHELLS",
    "generate_bash_completion",
    "generate_powershell_completion",
    "generate_zsh_completion",
    "directory_path",
    "file_path",
    "number_range",
    "positive_number",
]
