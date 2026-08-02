"""Project specific exceptions used by the CLI framework."""

from __future__ import annotations

from collections.abc import Mapping


class CLIError(Exception):
    """Base exception for framework level errors."""

    default_code = "cli_error"
    default_category = "runtime_error"
    default_exit_code = 1

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        category: str | None = None,
        exit_code: int | None = None,
        details: Mapping[str, object] | None = None,
        original_error: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.default_code
        self.category = category or self.default_category
        self.exit_code = self.default_exit_code if exit_code is None else exit_code
        self.details = dict(details or {})
        self.original_error = original_error

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict[str, object]:
        """Returns a machine-readable representation of the error."""
        payload: dict[str, object] = {
            "type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "category": self.category,
            "exit_code": self.exit_code,
        }
        if self.details:
            payload["details"] = dict(self.details)
        if self.original_error is not None:
            payload["cause"] = {
                "type": self.original_error.__class__.__name__,
                "message": str(self.original_error),
            }
        return payload


class CommandRegistrationError(CLIError):
    """Raised when a command cannot be registered safely."""

    default_code = "command_registration_error"
    default_category = "internal_error"


class CommandNotFoundError(CLIError):
    """Raised when a user tries to execute an unknown command."""

    default_code = "command_not_found"
    default_category = "input_error"
    default_exit_code = 2


class CommandExecutionError(CLIError):
    """Raised when a command cannot be executed with the provided input."""

    default_code = "command_execution_error"
    default_category = "input_error"
    default_exit_code = 2


class UserCodeError(CLIError):
    """Raised when user-provided quickli callbacks fail at runtime."""

    default_code = "user_code_error"
    default_category = "runtime_error"

    def __init__(
        self,
        message: str,
        *,
        original_error: BaseException,
        details: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
            original_error=original_error,
        )


class InternalCLIError(CLIError):
    """Raised when quickli encounters an unexpected internal runtime error."""

    default_code = "internal_cli_error"
    default_category = "internal_error"


class PluginLoadError(CLIError):
    """Raised when a plugin cannot be loaded or registered successfully."""

    default_code = "plugin_load_error"
    default_category = "internal_error"


class ConfigError(CLIError):
    """Base exception for configuration file errors."""

    default_code = "config_error"
    default_category = "input_error"


class ConfigValidationError(ConfigError):
    """Raised when a configuration file fails schema validation."""

    default_code = "config_validation_error"
