"""Public package interface for quickli."""

from quickli.argument import Argument
from quickli.application import Application
from quickli.command import Command
from quickli.exceptions import CLIError, CommandExecutionError, CommandNotFoundError
from quickli.exceptions import CommandRegistrationError, PluginLoadError
from quickli.option import Option
from quickli.plugin import Plugin
from quickli.validators import directory_path, file_path, number_range, positive_number

__all__ = [
    "Argument",
    "Application",
    "CLIError",
    "Command",
    "CommandExecutionError",
    "CommandNotFoundError",
    "CommandRegistrationError",
    "Option",
    "Plugin",
    "PluginLoadError",
    "directory_path",
    "file_path",
    "number_range",
    "positive_number",
]
