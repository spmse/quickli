"""Option resource definitions for quickli."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from quickli.validators import Validator, validator_descriptions


Converter = Callable[[str], object]


@dataclass(frozen=True, slots=True)
class Option:
    """Describes one named command option."""

    name: str
    short_name: str | None = None
    help_text: str = ""
    required: bool = False
    default: object | None = None
    is_flag: bool = False
    multiple: bool = False
    converter: Converter = str
    validators: tuple[Validator, ...] = ()

    def __post_init__(self) -> None:
        normalized_name = self.name.strip().lstrip("-")
        if not normalized_name:
            raise ValueError("Option name cannot be empty.")

        normalized_short_name = self.short_name
        if normalized_short_name is not None:
            normalized_short_name = normalized_short_name.strip().lstrip("-")
            if len(normalized_short_name) != 1:
                raise ValueError("Option short_name must be one character.")

        default = self.default
        if self.is_flag and default is None:
            default = False
        if self.multiple and self.is_flag and default is False:
            default = 0
        if self.multiple and not self.is_flag and default is None:
            default = []

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "short_name", normalized_short_name)
        object.__setattr__(self, "help_text", self.help_text.strip())
        object.__setattr__(self, "validators", tuple(self.validators))
        if self.multiple and not self.is_flag:
            object.__setattr__(self, "default", list(default))
        else:
            object.__setattr__(self, "default", default)
        if self.is_flag:
            object.__setattr__(self, "converter", bool)

    @property
    def destination(self) -> str:
        """Returns the handler keyword name for the option."""
        return self.name.replace("-", "_")

    @property
    def long_token(self) -> str:
        """Returns the canonical long-form option token."""
        return f"--{self.name}"

    @property
    def short_token(self) -> str | None:
        """Returns the short-form option token when configured."""
        if self.short_name is None:
            return None
        return f"-{self.short_name}"

    @property
    def takes_value(self) -> bool:
        """Returns whether the option requires a following value."""
        return not self.is_flag

    def convert(self, value: str) -> object:
        """Converts raw CLI text into the value passed to the handler."""
        try:
            converted_value = self.converter(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid value for option '{self.long_token}': {value}") from error
        return self.validate(converted_value)

    def validate(self, value: object | None) -> object | None:
        """Validates a converted or default value."""
        if value is None:
            return None

        validated_value = value
        for validator in self.validators:
            try:
                validated_value = validator(validated_value)
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid value for option '{self.long_token}': {error}"
                ) from error
        return validated_value

    def initial_value(self) -> object | None:
        """Returns a fresh default value for parsing."""
        if self.multiple and not self.is_flag:
            return [self.validate(item) for item in list(self.default or [])]
        return self.validate(self.default)

    @property
    def validator_descriptions(self) -> list[str]:
        """Returns user-facing validator descriptions when available."""
        return validator_descriptions(self.validators)
