"""Public package interface for quickli."""

from quickli.argument import Argument
from quickli.application import Application
from quickli.command import Command, Subcommand
from quickli.config import Config, ConfigField, ConfigIssue, ConfigSchema
from quickli.config import add_auto_init_config, generate_schema_json, validate_config
from quickli.exceptions import CLIError, CommandExecutionError, CommandNotFoundError
from quickli.exceptions import CommandRegistrationError, ConfigError, ConfigValidationError
from quickli.exceptions import PluginLoadError
from quickli.option import Option
from quickli.parsers import load_json, load_toml, load_yaml, render_json, render_toml, render_yaml
from quickli.plugin import Plugin
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
    "Config",
    "ConfigError",
    "ConfigField",
    "ConfigIssue",
    "ConfigSchema",
    "ConfigValidationError",
    "Option",
    "Plugin",
    "PluginLoadError",
    "add_auto_init_config",
    "load_json",
    "load_toml",
    "load_yaml",
    "render_json",
    "render_toml",
    "render_yaml",
    "generate_schema_json",
    "validate_config",
    "SUPPORTED_SHELLS",
    "generate_bash_completion",
    "generate_powershell_completion",
    "generate_zsh_completion",
    "directory_path",
    "file_path",
    "number_range",
    "positive_number",
]
