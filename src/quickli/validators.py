"""Built-in validators for quickli resources."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from numbers import Real
from pathlib import Path


Validator = Callable[[object], object]


@dataclass(frozen=True, slots=True)
class ValidatorSpec:
    """Callable validator with user-facing help metadata."""

    validator: Validator
    description: str

    def __call__(self, value: object) -> object:
        return self.validator(value)


def file_path(*, exists: bool | None = True) -> Validator:
    """Validates that a value represents a file path.

    The validator coerces the value to ``Path`` before validation.

    - ``exists=True``: path must exist and be a file.
    - ``exists=False``: path must not exist.
    - ``exists=None``: path may exist or not, but if it exists it must be a file.
    """

    def validate(value: object) -> Path:
        path = _coerce_path(value)
        if path.exists():
            if not path.is_file():
                raise ValueError(f"Expected a file path but received a directory: {path}")
            if exists is False:
                raise ValueError(f"File path must not exist yet: {path}")
            return path

        if exists is True:
            raise ValueError(f"File does not exist: {path}")
        return path

    return ValidatorSpec(validate, _path_description("file", exists))


def directory_path(*, exists: bool | None = True) -> Validator:
    """Validates that a value represents a directory path.

    The validator coerces the value to ``Path`` before validation.

    - ``exists=True``: path must exist and be a directory.
    - ``exists=False``: path must not exist.
    - ``exists=None``: path may exist or not, but if it exists it must be a directory.
    """

    def validate(value: object) -> Path:
        path = _coerce_path(value)
        if path.exists():
            if not path.is_dir():
                raise ValueError(f"Expected a directory path but received a file: {path}")
            if exists is False:
                raise ValueError(f"Directory path must not exist yet: {path}")
            return path

        if exists is True:
            raise ValueError(f"Directory does not exist: {path}")
        return path

    return ValidatorSpec(validate, _path_description("directory", exists))


def positive_number() -> Validator:
    """Validates that a numeric value is strictly greater than zero."""

    def validate(value: object) -> object:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"Expected a numeric value but received: {value}")
        if value <= 0:
            raise ValueError(f"Expected a positive number but received: {value}")
        return value

    return ValidatorSpec(validate, "positive number")


def number_range(
    *,
    min_value: Real | None = None,
    max_value: Real | None = None,
) -> Validator:
    """Validates that a numeric value falls within an inclusive range."""
    if min_value is None and max_value is None:
        raise ValueError("number_range requires at least one boundary.")

    def validate(value: object) -> object:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"Expected a numeric value but received: {value}")
        if min_value is not None and value < min_value:
            raise ValueError(f"Expected a number >= {min_value} but received: {value}")
        if max_value is not None and value > max_value:
            raise ValueError(f"Expected a number <= {max_value} but received: {value}")
        return value

    return ValidatorSpec(validate, _range_description(min_value, max_value))


def validator_descriptions(validators: tuple[Validator, ...]) -> list[str]:
    """Returns user-facing validator descriptions when available."""
    descriptions: list[str] = []
    for validator in validators:
        description = getattr(validator, "description", None)
        if isinstance(description, str) and description:
            descriptions.append(description)
    return descriptions


def _coerce_path(value: object) -> Path:
    if isinstance(value, Path):
        return value
    if value is None:
        raise ValueError("Path value cannot be empty.")
    return Path(str(value))


def _path_description(path_kind: str, exists: bool | None) -> str:
    if exists is True:
        return f"existing {path_kind} path"
    if exists is False:
        return f"new {path_kind} path"
    return f"{path_kind} path"


def _range_description(
    min_value: Real | None,
    max_value: Real | None,
) -> str:
    if min_value is not None and max_value is not None:
        return f"number in range {min_value}..{max_value}"
    if min_value is not None:
        return f"number >= {min_value}"
    return f"number <= {max_value}"
