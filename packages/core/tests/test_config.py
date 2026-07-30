"""Unit tests for the configuration file handling module."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from quickli.config import (
    Config,
    ConfigField,
    ConfigIssue,
    ConfigSchema,
    _render_toml,
    _toml_scalar,
    _type_matches,
    add_auto_init_config,
    validate_config,
)
from quickli.exceptions import ConfigError, ConfigValidationError
from quickli.validators import positive_number


# ---------------------------------------------------------------------------
# ConfigField
# ---------------------------------------------------------------------------


class ConfigFieldTests(unittest.TestCase):
    def test_name_is_stripped(self) -> None:
        field = ConfigField("  host  ")
        self.assertEqual(field.name, "host")

    def test_empty_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            ConfigField("")

    def test_whitespace_only_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            ConfigField("   ")

    def test_defaults(self) -> None:
        field = ConfigField("host")
        self.assertIs(field.value_type, str)
        self.assertTrue(field.required)
        self.assertIsNone(field.default)
        self.assertEqual(field.help_text, "")
        self.assertEqual(field.validators, ())

    def test_help_text_is_stripped(self) -> None:
        field = ConfigField("x", help_text="  description  ")
        self.assertEqual(field.help_text, "description")

    def test_validators_are_stored_as_tuple(self) -> None:
        v = positive_number()
        field = ConfigField("count", value_type=int, validators=[v])
        self.assertEqual(field.validators, (v,))

    def test_custom_value_type_and_default(self) -> None:
        field = ConfigField("retries", value_type=int, required=False, default=3)
        self.assertIs(field.value_type, int)
        self.assertFalse(field.required)
        self.assertEqual(field.default, 3)


# ---------------------------------------------------------------------------
# ConfigSchema
# ---------------------------------------------------------------------------


class ConfigSchemaTests(unittest.TestCase):
    def _simple_schema(self) -> ConfigSchema:
        return ConfigSchema(
            fields=[
                ConfigField("host", value_type=str, required=True),
                ConfigField("port", value_type=int, required=True),
                ConfigField("debug", value_type=bool, required=False, default=False),
            ]
        )

    def test_field_names_property(self) -> None:
        schema = self._simple_schema()
        self.assertEqual(schema.field_names, {"host", "port", "debug"})

    def test_duplicate_field_names_raise(self) -> None:
        with self.assertRaises(ValueError):
            ConfigSchema(
                fields=[
                    ConfigField("host"),
                    ConfigField("host"),
                ]
            )

    def test_validate_returns_empty_for_valid_data(self) -> None:
        schema = self._simple_schema()
        errors = schema.validate({"host": "localhost", "port": 5432, "debug": False})
        self.assertEqual(errors, [])

    def test_validate_reports_missing_required_field(self) -> None:
        schema = self._simple_schema()
        errors = schema.validate({"port": 5432})
        self.assertEqual(len(errors), 1)
        self.assertIn("host", errors[0])
        self.assertIn("missing", errors[0])

    def test_validate_does_not_report_missing_optional_with_default(self) -> None:
        schema = self._simple_schema()
        errors = schema.validate({"host": "localhost", "port": 5432})
        self.assertEqual(errors, [])

    def test_validate_reports_type_mismatch(self) -> None:
        schema = self._simple_schema()
        errors = schema.validate({"host": "localhost", "port": "not-a-number", "debug": False})
        self.assertEqual(len(errors), 1)
        self.assertIn("port", errors[0])
        self.assertIn("int", errors[0])

    def test_validate_bool_not_accepted_as_int(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("count", value_type=int)])
        errors = schema.validate({"count": True})
        self.assertEqual(len(errors), 1)
        self.assertIn("count", errors[0])

    def test_validate_int_not_accepted_as_bool(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("flag", value_type=bool)])
        errors = schema.validate({"flag": 1})
        self.assertEqual(len(errors), 1)
        self.assertIn("flag", errors[0])

    def test_validate_reports_validator_failure(self) -> None:
        schema = ConfigSchema(
            fields=[ConfigField("workers", value_type=int, validators=[positive_number()])]
        )
        errors = schema.validate({"workers": -1})
        self.assertEqual(len(errors), 1)
        self.assertIn("workers", errors[0])

    def test_validate_accepts_valid_validator(self) -> None:
        schema = ConfigSchema(
            fields=[ConfigField("workers", value_type=int, validators=[positive_number()])]
        )
        errors = schema.validate({"workers": 4})
        self.assertEqual(errors, [])

    def test_validate_collects_all_errors(self) -> None:
        schema = self._simple_schema()
        errors = schema.validate({})
        # host and port are required, debug has a default so it's fine
        self.assertEqual(len(errors), 2)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


class ConfigTests(unittest.TestCase):
    def _write_toml(self, directory: str, filename: str, content: str) -> Path:
        path = Path(directory) / filename
        path.write_text(content, encoding="utf-8")
        return path

    def test_path_is_resolved(self) -> None:
        config = Config(path="/tmp/test.toml")
        self.assertIsInstance(config.path, Path)

    def test_data_is_empty_before_load(self) -> None:
        config = Config(path="/tmp/test.toml")
        self.assertEqual(config.data, {})

    def test_schema_property(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("x")])
        config = Config(path="/tmp/test.toml", schema=schema)
        self.assertIs(config.schema, schema)

    def test_load_reads_toml_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", 'host = "localhost"\nport = 5432\n')
            config = Config(path=path)
            data = config.load()
            self.assertEqual(data["host"], "localhost")
            self.assertEqual(data["port"], 5432)

    def test_load_raises_when_file_missing(self) -> None:
        config = Config(path="/nonexistent/path/config.toml")
        with self.assertRaises(ConfigError):
            config.load()

    def test_load_raises_on_invalid_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", "this is not toml ===\n")
            config = Config(path=path)
            with self.assertRaises(ConfigError):
                config.load()

    def test_load_validates_against_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", 'host = "localhost"\n')
            schema = ConfigSchema(
                fields=[
                    ConfigField("host", value_type=str),
                    ConfigField("port", value_type=int),
                ]
            )
            config = Config(path=path, schema=schema)
            with self.assertRaises(ConfigValidationError):
                config.load()

    def test_load_succeeds_when_schema_is_satisfied(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", 'host = "localhost"\nport = 5432\n')
            schema = ConfigSchema(
                fields=[
                    ConfigField("host", value_type=str),
                    ConfigField("port", value_type=int),
                ]
            )
            config = Config(path=path, schema=schema)
            data = config.load()
            self.assertEqual(data["host"], "localhost")

    def test_load_updates_data_property(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", 'key = "value"\n')
            config = Config(path=path)
            config.load()
            self.assertEqual(config.data["key"], "value")

    def test_save_writes_toml_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path)
            config.save({"host": "localhost", "port": 9000})
            self.assertTrue(path.exists())
            content = path.read_text(encoding="utf-8")
            self.assertIn('host = "localhost"', content)
            self.assertIn("port = 9000", content)

    def test_save_creates_parent_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "subdir" / "nested" / "config.toml"
            config = Config(path=path)
            config.save({"key": "value"})
            self.assertTrue(path.exists())

    def test_save_updates_data_property(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path)
            config.save({"key": "value"})
            self.assertEqual(config.data["key"], "value")

    def test_save_and_load_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path)
            original = {"name": "test", "count": 5, "enabled": True}
            config.save(original)
            loaded = config.load()
            self.assertEqual(loaded, original)

    def test_data_returns_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", 'key = "value"\n')
            config = Config(path=path)
            config.load()
            result = config.data
            result["extra"] = "injected"
            self.assertNotIn("extra", config.data)

    def test_save_skips_none_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path)
            config.save({"host": "localhost", "port": None})
            content = path.read_text(encoding="utf-8")
            self.assertIn("host", content)
            self.assertNotIn("port", content)

    def test_load_raises_config_validation_error_with_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_toml(tmpdir, "config.toml", 'port = "wrong"\n')
            schema = ConfigSchema(fields=[ConfigField("port", value_type=int)])
            config = Config(path=path, schema=schema)
            with self.assertRaises(ConfigValidationError) as ctx:
                config.load()
            self.assertIn("port", str(ctx.exception))

    def test_save_with_nested_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path)
            config.save({"database": {"host": "localhost", "port": 5432}})
            content = path.read_text(encoding="utf-8")
            self.assertIn("[database]", content)
            self.assertIn('host = "localhost"', content)
            self.assertIn("port = 5432", content)


# ---------------------------------------------------------------------------
# add_auto_init_config
# ---------------------------------------------------------------------------


class AddAutoInitConfigTests(unittest.TestCase):
    def _schema_with_defaults(self) -> ConfigSchema:
        return ConfigSchema(
            fields=[
                ConfigField("log_level", value_type=str, required=False, default="info"),
                ConfigField("retries", value_type=int, required=False, default=3),
            ]
        )

    def test_creates_file_with_defaults_when_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path, schema=self._schema_with_defaults())
            data = add_auto_init_config(config)
            self.assertTrue(path.exists())
            self.assertEqual(data["log_level"], "info")
            self.assertEqual(data["retries"], 3)

    def test_loads_existing_file_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            path.write_text('log_level = "debug"\nretries = 5\n', encoding="utf-8")
            config = Config(path=path, schema=self._schema_with_defaults())
            data = add_auto_init_config(config)
            self.assertEqual(data["log_level"], "debug")
            self.assertEqual(data["retries"], 5)

    def test_creates_empty_file_when_no_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path)
            data = add_auto_init_config(config)
            self.assertTrue(path.exists())
            self.assertEqual(data, {})

    def test_creates_parent_dirs_for_new_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nested" / "dir" / "config.toml"
            config = Config(path=path, schema=self._schema_with_defaults())
            add_auto_init_config(config)
            self.assertTrue(path.exists())

    def test_raises_config_validation_error_for_invalid_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            path.write_text('retries = "bad"\n', encoding="utf-8")
            schema = ConfigSchema(fields=[ConfigField("retries", value_type=int)])
            config = Config(path=path, schema=schema)
            with self.assertRaises(ConfigValidationError):
                add_auto_init_config(config)

    def test_fields_without_defaults_are_excluded_from_new_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            schema = ConfigSchema(
                fields=[
                    ConfigField("name", value_type=str, required=True),
                    ConfigField("retries", value_type=int, required=False, default=3),
                ]
            )
            config = Config(path=path, schema=schema)
            data = add_auto_init_config(config)
            self.assertNotIn("name", data)
            self.assertEqual(data["retries"], 3)


# ---------------------------------------------------------------------------
# validate_config
# ---------------------------------------------------------------------------


class ValidateConfigTests(unittest.TestCase):
    def _make_config(self, data: dict[str, object], schema: ConfigSchema | None = None) -> Config:
        """Creates a Config with pre-loaded data without touching the filesystem."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "config.toml"
            config = Config(path=path, schema=schema)
            config.save(data)
            config._data = dict(data)  # noqa: SLF001 - bypass load for isolated testing
            return config

    def test_returns_empty_list_when_no_schema(self) -> None:
        config = self._make_config({"x": 1})
        self.assertEqual(validate_config(config), [])

    def test_returns_empty_list_for_valid_data(self) -> None:
        schema = ConfigSchema(
            fields=[
                ConfigField("host", value_type=str),
                ConfigField("port", value_type=int),
            ]
        )
        config = self._make_config({"host": "localhost", "port": 5432}, schema=schema)
        self.assertEqual(validate_config(config), [])

    def test_reports_missing_required_field_as_error(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("host", value_type=str, required=True)])
        config = self._make_config({}, schema=schema)
        issues = validate_config(config)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].field, "host")
        self.assertEqual(issues[0].severity, "error")

    def test_reports_type_mismatch_as_error(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("port", value_type=int)])
        config = self._make_config({"port": "8080"}, schema=schema)
        issues = validate_config(config)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")
        self.assertIn("port", issues[0].field)

    def test_reports_validator_failure_as_error(self) -> None:
        schema = ConfigSchema(
            fields=[ConfigField("workers", value_type=int, validators=[positive_number()])]
        )
        config = self._make_config({"workers": 0}, schema=schema)
        issues = validate_config(config)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "error")

    def test_reports_unknown_field_as_warning(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("host", value_type=str)])
        config = self._make_config({"host": "localhost", "typo_field": "oops"}, schema=schema)
        issues = validate_config(config)
        warning_fields = [i.field for i in issues if i.severity == "warning"]
        self.assertIn("typo_field", warning_fields)

    def test_returns_config_issue_instances(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("host", value_type=str, required=True)])
        config = self._make_config({}, schema=schema)
        issues = validate_config(config)
        self.assertIsInstance(issues[0], ConfigIssue)
        self.assertIsInstance(issues[0].field, str)
        self.assertIsInstance(issues[0].message, str)
        self.assertIsInstance(issues[0].severity, str)

    def test_reports_multiple_issues(self) -> None:
        schema = ConfigSchema(
            fields=[
                ConfigField("host", value_type=str, required=True),
                ConfigField("port", value_type=int, required=True),
            ]
        )
        config = self._make_config({"extra": "unknown"}, schema=schema)
        issues = validate_config(config)
        severities = [i.severity for i in issues]
        self.assertIn("error", severities)
        self.assertIn("warning", severities)

    def test_does_not_skip_type_checking_for_bool_vs_int(self) -> None:
        schema = ConfigSchema(fields=[ConfigField("count", value_type=int)])
        config = self._make_config({"count": True}, schema=schema)
        issues = validate_config(config)
        error_issues = [i for i in issues if i.severity == "error"]
        self.assertEqual(len(error_issues), 1)

    def test_skips_optional_fields_with_defaults_when_absent(self) -> None:
        schema = ConfigSchema(
            fields=[ConfigField("timeout", value_type=int, required=False, default=30)]
        )
        config = self._make_config({}, schema=schema)
        issues = validate_config(config)
        self.assertEqual(issues, [])


# ---------------------------------------------------------------------------
# _render_toml (internal helper)
# ---------------------------------------------------------------------------


class RenderTomlTests(unittest.TestCase):
    def test_renders_string(self) -> None:
        self.assertIn('name = "alice"', _render_toml({"name": "alice"}))

    def test_renders_integer(self) -> None:
        self.assertIn("count = 42", _render_toml({"count": 42}))

    def test_renders_float(self) -> None:
        self.assertIn("ratio = 1.5", _render_toml({"ratio": 1.5}))

    def test_renders_true(self) -> None:
        self.assertIn("enabled = true", _render_toml({"enabled": True}))

    def test_renders_false(self) -> None:
        self.assertIn("debug = false", _render_toml({"debug": False}))

    def test_renders_list(self) -> None:
        result = _render_toml({"tags": ["a", "b"]})
        self.assertIn("tags =", result)
        self.assertIn('"a"', result)
        self.assertIn('"b"', result)

    def test_skips_none_values(self) -> None:
        result = _render_toml({"host": "localhost", "port": None})
        self.assertNotIn("port", result)
        self.assertIn("host", result)

    def test_renders_nested_table(self) -> None:
        result = _render_toml({"database": {"host": "localhost", "port": 5432}})
        self.assertIn("[database]", result)
        self.assertIn('host = "localhost"', result)
        self.assertIn("port = 5432", result)

    def test_renders_empty_dict(self) -> None:
        result = _render_toml({})
        self.assertIsInstance(result, str)

    def test_raises_for_deeply_nested_dict(self) -> None:
        with self.assertRaises(TypeError):
            _render_toml({"a": {"b": {"c": 1}}})

    def test_string_with_quotes_is_escaped(self) -> None:
        result = _render_toml({"msg": 'say "hello"'})
        self.assertIn('\\"hello\\"', result)

    def test_output_ends_with_newline(self) -> None:
        result = _render_toml({"x": 1})
        self.assertTrue(result.endswith("\n"))


# ---------------------------------------------------------------------------
# _toml_scalar
# ---------------------------------------------------------------------------


class TomlScalarTests(unittest.TestCase):
    def test_bool_true(self) -> None:
        self.assertEqual(_toml_scalar(True), "true")

    def test_bool_false(self) -> None:
        self.assertEqual(_toml_scalar(False), "false")

    def test_integer(self) -> None:
        self.assertEqual(_toml_scalar(42), "42")

    def test_float(self) -> None:
        self.assertEqual(_toml_scalar(3.14), "3.14")

    def test_string(self) -> None:
        self.assertEqual(_toml_scalar("hello"), '"hello"')

    def test_string_with_backslash(self) -> None:
        self.assertIn("\\\\", _toml_scalar("a\\b"))

    def test_string_with_newline(self) -> None:
        self.assertIn("\\n", _toml_scalar("line1\nline2"))

    def test_list_of_strings(self) -> None:
        result = _toml_scalar(["a", "b"])
        self.assertEqual(result, '["a", "b"]')

    def test_list_of_integers(self) -> None:
        result = _toml_scalar([1, 2, 3])
        self.assertEqual(result, "[1, 2, 3]")

    def test_unsupported_type_raises(self) -> None:
        with self.assertRaises(TypeError):
            _toml_scalar(object())


# ---------------------------------------------------------------------------
# _type_matches
# ---------------------------------------------------------------------------


class TypeMatchesTests(unittest.TestCase):
    def test_str_matches_str(self) -> None:
        self.assertTrue(_type_matches("hello", str))

    def test_int_matches_int(self) -> None:
        self.assertTrue(_type_matches(42, int))

    def test_float_matches_float(self) -> None:
        self.assertTrue(_type_matches(1.5, float))

    def test_bool_matches_bool(self) -> None:
        self.assertTrue(_type_matches(True, bool))

    def test_bool_does_not_match_int(self) -> None:
        self.assertFalse(_type_matches(True, int))

    def test_int_does_not_match_bool(self) -> None:
        self.assertFalse(_type_matches(1, bool))

    def test_str_does_not_match_int(self) -> None:
        self.assertFalse(_type_matches("42", int))

    def test_none_does_not_match_str(self) -> None:
        self.assertFalse(_type_matches(None, str))

    def test_list_matches_list(self) -> None:
        self.assertTrue(_type_matches([1, 2], list))

    def test_dict_matches_dict(self) -> None:
        self.assertTrue(_type_matches({"a": 1}, dict))


# ---------------------------------------------------------------------------
# Public API import smoke test
# ---------------------------------------------------------------------------


class PublicApiTests(unittest.TestCase):
    def test_symbols_exported_from_package(self) -> None:
        import quickli

        self.assertTrue(hasattr(quickli, "Config"))
        self.assertTrue(hasattr(quickli, "ConfigField"))
        self.assertTrue(hasattr(quickli, "ConfigSchema"))
        self.assertTrue(hasattr(quickli, "ConfigIssue"))
        self.assertTrue(hasattr(quickli, "ConfigError"))
        self.assertTrue(hasattr(quickli, "ConfigValidationError"))
        self.assertTrue(hasattr(quickli, "add_auto_init_config"))
        self.assertTrue(hasattr(quickli, "validate_config"))


if __name__ == "__main__":
    unittest.main()
