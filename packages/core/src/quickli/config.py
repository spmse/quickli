"""Configuration file handling for quickli applications.

This module provides tools for reading, writing, and validating TOML configuration
files.  The design is intentionally minimal: it covers the common cases that CLI
tools need without adding external dependencies.

Typical usage
-------------
Define a schema, create a ``Config`` object pointing to a file, then call
``add_auto_init_config`` to create the file on first run or load it on subsequent
runs::

    from pathlib import Path
    from quickli.config import Config, ConfigField, ConfigSchema, add_auto_init_config

    schema = ConfigSchema(fields=[
        ConfigField("log_level", value_type=str, required=False, default="info"),
        ConfigField("retries", value_type=int, required=False, default=3),
    ])

    config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
    data = add_auto_init_config(config)
    print(data["log_level"])

Validation
----------
Use ``validate_config`` to inspect a loaded configuration and receive a structured
list of issues before deciding how to proceed::

    from quickli.config import validate_config

    issues = validate_config(config)
    for issue in issues:
        print(f"[{issue.severity}] {issue.field}: {issue.message}")
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from quickli.exceptions import ConfigError, ConfigValidationError
from quickli.validators import Validator


@dataclass(frozen=True, slots=True)
class ConfigField:
    """Describes one expected field in a configuration file.

    Parameters
    ----------
    name:
        The field name as it appears in the TOML file.
    value_type:
        The Python type the field value must have after TOML parsing.
        Accepted types are ``str``, ``int``, ``float``, ``bool``, ``list``,
        and ``dict``.  Boolean fields must use ``value_type=bool``; they are
        never treated as integers.
    required:
        When ``True`` and the field is absent from the file, validation
        reports an error.  Defaults to ``True``.
    default:
        The default value written to a new file by ``add_auto_init_config``.
        An absent field with a default is not treated as an error during
        validation.
    help_text:
        A short human-readable description shown in generated documentation.
    validators:
        An optional tuple of validator callables.  Each callable receives the
        field value and must return it (possibly coerced) or raise
        ``ValueError`` with a user-facing message.

    Examples
    --------
    >>> ConfigField("log_level", value_type=str, required=False, default="info")
    ConfigField(name='log_level', ...)

    >>> ConfigField("retries", value_type=int, required=True)
    ConfigField(name='retries', ...)
    """

    name: str
    value_type: type = str
    required: bool = True
    default: object = None
    help_text: str = ""
    validators: tuple[Validator, ...] = ()

    def __post_init__(self) -> None:
        normalized = self.name.strip()
        if not normalized:
            raise ValueError("ConfigField name cannot be empty.")
        object.__setattr__(self, "name", normalized)
        object.__setattr__(self, "help_text", self.help_text.strip())
        object.__setattr__(self, "validators", tuple(self.validators))


@dataclass(frozen=True, slots=True)
class ConfigSchema:
    """Defines the expected structure of a configuration file.

    A schema is a collection of ``ConfigField`` objects.  Pass a schema to
    ``Config`` to enable automatic validation when loading a file and to let
    ``add_auto_init_config`` write sensible defaults on first run.

    Parameters
    ----------
    fields:
        A sequence of ``ConfigField`` objects describing each expected key.
        Duplicate field names raise ``ValueError``.

    Examples
    --------
    >>> schema = ConfigSchema(fields=[
    ...     ConfigField("host", value_type=str, default="localhost"),
    ...     ConfigField("port", value_type=int, default=8080),
    ... ])
    """

    fields: tuple[ConfigField, ...]

    def __post_init__(self) -> None:
        fields_tuple = tuple(self.fields)
        names = [f.name for f in fields_tuple]
        duplicates = {n for n in names if names.count(n) > 1}
        if duplicates:
            raise ValueError(
                f"Duplicate field names in ConfigSchema: {', '.join(sorted(duplicates))}"
            )
        object.__setattr__(self, "fields", fields_tuple)

    @property
    def field_names(self) -> frozenset[str]:
        """Returns the set of all field names defined in this schema."""
        return frozenset(f.name for f in self.fields)

    def validate(self, data: dict[str, object]) -> list[str]:
        """Validates *data* against this schema.

        Returns a list of human-readable error strings.  An empty list means
        the data satisfies all field constraints.  This method does not raise;
        it always returns the complete list of problems found.

        Parameters
        ----------
        data:
            A flat or nested dict as returned by ``tomllib.load``.
        """
        errors: list[str] = []
        for field in self.fields:
            if field.name not in data:
                if field.required and field.default is None:
                    errors.append(f"Required field '{field.name}' is missing.")
                continue

            value = data[field.name]
            if not _type_matches(value, field.value_type):
                errors.append(
                    f"Field '{field.name}' expects {field.value_type.__name__} "
                    f"but got {type(value).__name__}."
                )
                continue

            for validator in field.validators:
                try:
                    validator(value)
                except (TypeError, ValueError) as exc:
                    errors.append(f"Field '{field.name}': {exc}")

        return errors


@dataclass(frozen=True, slots=True)
class ConfigIssue:
    """A single issue found during configuration validation.

    Attributes
    ----------
    field:
        The name of the configuration field that triggered the issue, or an
        empty string for schema-level issues.
    message:
        A human-readable description of the problem.
    severity:
        Either ``"error"`` for blocking problems or ``"warning"`` for
        non-critical concerns such as unrecognised fields.

    Examples
    --------
    >>> issue = ConfigIssue(field="retries", message="must be > 0", severity="error")
    >>> print(f"[{issue.severity}] {issue.field}: {issue.message}")
    [error] retries: must be > 0
    """

    field: str
    message: str
    severity: str


class Config:
    """Manages a TOML configuration file with optional schema validation.

    ``Config`` combines a file path with an optional ``ConfigSchema``.  Its
    ``load`` and ``save`` methods handle reading and writing the TOML file.
    Passing a schema enables automatic validation when the file is loaded.

    Parameters
    ----------
    path:
        Path to the TOML configuration file.  Tilde expansion is applied
        automatically.
    schema:
        Optional schema that defines the expected fields and types.  When
        provided, ``load`` raises ``ConfigValidationError`` for hard errors
        such as missing required fields or type mismatches.

    Examples
    --------
    Load a config file and validate it::

        from pathlib import Path
        from quickli.config import Config, ConfigField, ConfigSchema

        schema = ConfigSchema(fields=[
            ConfigField("host", value_type=str, default="localhost"),
            ConfigField("port", value_type=int, default=8080),
        ])
        config = Config(path=Path("~/.myapp/config.toml"), schema=schema)
        data = config.load()

    Save a dict to a config file::

        config.save({"host": "example.com", "port": 9000})
    """

    def __init__(
        self,
        path: str | Path,
        schema: ConfigSchema | None = None,
    ) -> None:
        self._path = Path(path).expanduser()
        self._schema = schema
        self._data: dict[str, object] = {}

    @property
    def path(self) -> Path:
        """The resolved absolute path of the configuration file."""
        return self._path

    @property
    def schema(self) -> ConfigSchema | None:
        """The schema used to validate this configuration, or ``None``."""
        return self._schema

    @property
    def data(self) -> dict[str, object]:
        """A copy of the currently loaded configuration data.

        Returns an empty dict when the file has not been loaded yet.
        """
        return dict(self._data)

    def load(self) -> dict[str, object]:
        """Loads and returns configuration from the TOML file.

        When a schema is configured, this method validates the loaded data and
        raises ``ConfigValidationError`` when required fields are missing or
        values have the wrong type.

        Raises
        ------
        ConfigError
            When the file does not exist or cannot be parsed as valid TOML.
        ConfigValidationError
            When schema validation fails after a successful file read.
        """
        if not self._path.exists():
            raise ConfigError(f"Configuration file not found: {self._path}")

        try:
            with open(self._path, "rb") as fh:
                loaded: dict[str, object] = tomllib.load(fh)
        except tomllib.TOMLDecodeError as exc:
            raise ConfigError(f"Failed to parse configuration file '{self._path}': {exc}") from exc

        self._data = loaded

        if self._schema is not None:
            errors = self._schema.validate(self._data)
            if errors:
                bullet_list = "\n".join(f"  - {e}" for e in errors)
                raise ConfigValidationError(f"Configuration validation failed:\n{bullet_list}")

        return dict(self._data)

    def save(self, data: dict[str, object]) -> None:
        """Serialises *data* and writes it to the configuration file.

        Parent directories are created automatically when they do not exist.

        Parameters
        ----------
        data:
            A dict containing the configuration values to persist.  Supported
            value types are ``str``, ``int``, ``float``, ``bool``, ``list``
            (of scalars), and ``dict`` (one level of nesting as a TOML table).
            ``None`` values are silently skipped.

        Raises
        ------
        TypeError
            When *data* contains a value of an unsupported type.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)
        content = _render_toml(data)
        self._path.write_text(content, encoding="utf-8")
        self._data = dict(data)


def add_auto_init_config(config: Config) -> dict[str, object]:
    """Creates a configuration file with defaults when absent; loads it when present.

    This helper is designed for application startup code or a dedicated
    ``config init`` command.  It follows two branches:

    - **File absent**: writes a new file populated with default values defined
      in the schema, then returns those defaults.
    - **File present**: calls ``config.load()`` and returns the loaded data.

    When no schema is attached to *config*, an absent file is created empty and
    the function returns ``{}``.

    Parameters
    ----------
    config:
        A ``Config`` instance pointing to the desired file location.

    Returns
    -------
    dict
        The configuration data that is now active: either freshly written
        defaults or the values loaded from the existing file.

    Raises
    ------
    ConfigError
        When the existing file cannot be read or parsed.
    ConfigValidationError
        When the existing file fails schema validation.

    Examples
    --------
    ::

        from pathlib import Path
        from quickli.config import Config, ConfigField, ConfigSchema, add_auto_init_config

        schema = ConfigSchema(fields=[
            ConfigField("log_level", value_type=str, required=False, default="info"),
            ConfigField("retries", value_type=int, required=False, default=3),
        ])

        config = Config(path=Path.home() / ".myapp" / "config.toml", schema=schema)
        data = add_auto_init_config(config)
        # data == {"log_level": "info", "retries": 3} on first run
    """
    if config.path.exists():
        return config.load()

    if config.schema is None:
        config.save({})
        return {}

    defaults: dict[str, object] = {
        field.name: field.default for field in config.schema.fields if field.default is not None
    }
    config.save(defaults)
    return defaults


def validate_config(config: Config) -> list[ConfigIssue]:
    """Inspects a ``Config`` object and returns all detected issues.

    Unlike ``Config.load``, this function never raises.  It returns a
    structured list of ``ConfigIssue`` objects so that the caller can choose
    how to present or handle each finding.

    Issue severities:

    - ``"error"`` — hard problem that will likely cause failures at runtime,
      e.g. a required field is missing or a value has the wrong type.
    - ``"warning"`` — non-critical concern, e.g. an unrecognised field that
      may indicate a typo.

    When no schema is attached to *config*, this function always returns an
    empty list.

    Parameters
    ----------
    config:
        A ``Config`` instance.  The data inspected is whatever is currently in
        ``config.data``; call ``config.load()`` first when inspecting a file.

    Returns
    -------
    list[ConfigIssue]
        All issues found, or an empty list when the configuration looks clean.

    Examples
    --------
    ::

        from quickli.config import Config, ConfigSchema, ConfigField, validate_config

        schema = ConfigSchema(fields=[
            ConfigField("host", value_type=str, default="localhost"),
            ConfigField("port", value_type=int, default=8080),
        ])

        config = Config(path="app.toml", schema=schema)
        config.load()

        issues = validate_config(config)
        for issue in issues:
            print(f"[{issue.severity}] {issue.field}: {issue.message}")
    """
    if config.schema is None:
        return []

    issues: list[ConfigIssue] = []
    data = config.data

    for field in config.schema.fields:
        if field.name not in data:
            if field.required and field.default is None:
                issues.append(
                    ConfigIssue(
                        field=field.name,
                        message="required field is missing",
                        severity="error",
                    )
                )
            continue

        value = data[field.name]
        if not _type_matches(value, field.value_type):
            issues.append(
                ConfigIssue(
                    field=field.name,
                    message=(
                        f"expected {field.value_type.__name__} but got {type(value).__name__}"
                    ),
                    severity="error",
                )
            )
            continue

        for validator in field.validators:
            try:
                validator(value)
            except (TypeError, ValueError) as exc:
                issues.append(
                    ConfigIssue(
                        field=field.name,
                        message=str(exc),
                        severity="error",
                    )
                )

    known_names = config.schema.field_names
    for key in data:
        if key not in known_names:
            issues.append(
                ConfigIssue(
                    field=key,
                    message="unrecognised field not defined in schema",
                    severity="warning",
                )
            )

    return issues


# ---------------------------------------------------------------------------
# Internal TOML serialisation helpers
# ---------------------------------------------------------------------------


def _render_toml(data: dict[str, object]) -> str:
    """Serialises *data* to a TOML-formatted string.

    Supports one level of nested ``dict`` values, which are written as TOML
    table headers.  ``None`` values are silently omitted.  Raises ``TypeError``
    for unsupported value types.
    """
    lines: list[str] = []
    deferred: list[tuple[str, dict[str, object]]] = []

    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, dict):
            deferred.append((key, value))
        else:
            lines.append(f"{key} = {_toml_scalar(value)}")

    for section_key, section_data in deferred:
        lines.append(f"\n[{section_key}]")
        for k, v in section_data.items():
            if v is None:
                continue
            if isinstance(v, dict):
                raise TypeError(
                    f"Nested tables deeper than one level are not supported "
                    f"by the built-in TOML writer (key: '{section_key}.{k}')."
                )
            lines.append(f"{k} = {_toml_scalar(v)}")

    content = "\n".join(lines)
    return content + "\n" if content else "\n"


def _toml_scalar(value: object) -> str:
    """Converts a Python scalar to its TOML literal representation."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    if isinstance(value, list):
        items = ", ".join(_toml_scalar(item) for item in value)
        return f"[{items}]"
    raise TypeError(f"Unsupported value type for TOML serialisation: {type(value).__name__}")


def _type_matches(value: object, expected_type: type) -> bool:
    """Returns ``True`` when *value* is an instance of *expected_type*.

    Handles the Python quirk where ``bool`` is a subclass of ``int``: a
    ``bool`` value is *not* accepted when ``expected_type`` is ``int``, and an
    ``int`` value is *not* accepted when ``expected_type`` is ``bool``.
    """
    if type(value) is bool:
        return expected_type is bool
    if expected_type is bool:
        return False
    return isinstance(value, expected_type)
