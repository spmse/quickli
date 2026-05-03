"""Argument resource definitions for quickli."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from quickli.validators import Validator, validator_descriptions


Converter = Callable[[str], object]


@dataclass(frozen=True, slots=True)
class Argument:
    """Describes one positional command argument."""

    name: str
    help_text: str = ""
    required: bool = True
    default: object | None = None
    metavar: str | None = None
    converter: Converter = str
    validators: tuple[Validator, ...] = ()

    def __post_init__(self) -> None:
        normalized_name = self.name.strip().replace("_", "-")
        if not normalized_name:
            raise ValueError("Argument name cannot be empty.")

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "help_text", self.help_text.strip())
        object.__setattr__(self, "validators", tuple(self.validators))
        if self.metavar is not None:
            object.__setattr__(self, "metavar", self.metavar.strip())

    @property
    def display_name(self) -> str:
        """Returns the user-facing token used in help text."""
        if self.metavar:
            return self.metavar
        return self.name.replace("-", "_").upper()

    def convert(self, value: str) -> object:
        """Converts raw CLI text into the value passed to the handler."""
        try:
            converted_value = self.converter(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid value for argument '{self.name}': {value}") from error
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
                raise ValueError(f"Invalid value for argument '{self.name}': {error}") from error
        return validated_value

    @property
    def validator_descriptions(self) -> list[str]:
        """Returns user-facing validator descriptions when available."""
        return validator_descriptions(self.validators)
