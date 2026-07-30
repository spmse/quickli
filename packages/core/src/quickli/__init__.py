"""Public package interface for quickli."""

from quickli.argument import Argument
from quickli.application import Application
from quickli.command import Command
from quickli.config import Config, ConfigField, ConfigIssue, ConfigSchema
from quickli.config import add_auto_init_config, generate_schema_json, validate_config
from quickli.exceptions import CLIError, CommandExecutionError, CommandNotFoundError
from quickli.exceptions import CommandRegistrationError, ConfigError, ConfigValidationError
from quickli.option import Option
from quickli.validators import directory_path, file_path, number_range, positive_number

__all__ = [
    "Argument",
    "Application",
    "CLIError",
    "Command",
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
    "add_auto_init_config",
    "directory_path",
    "file_path",
    "generate_schema_json",
    "number_range",
    "positive_number",
    "validate_config",
]
