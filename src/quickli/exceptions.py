"""Project specific exceptions used by the CLI framework."""


class CLIError(Exception):
    """Base exception for framework level errors."""


class CommandRegistrationError(CLIError):
    """Raised when a command cannot be registered safely."""


class CommandNotFoundError(CLIError):
    """Raised when a user tries to execute an unknown command."""


class CommandExecutionError(CLIError):
    """Raised when a command cannot be executed with the provided input."""
