"""Unit tests for JSON/YAML rendering and loading helpers."""

from __future__ import annotations

import unittest

from quickli import core_json_or_yaml_loading, core_json_or_yaml_rendering


class CoreJsonOrYamlTests(unittest.TestCase):
    def test_render_json_returns_indented_sorted_output(self) -> None:
        result = core_json_or_yaml_rendering({"name": "Ada", "active": True}, format_name="json")

        self.assertEqual(result, '{\n  "active": true,\n  "name": "Ada"\n}')

    def test_load_json_parses_payload(self) -> None:
        result = core_json_or_yaml_loading('{"name":"Ada","count":2}', format_name="json")

        self.assertEqual(result, {"name": "Ada", "count": 2})

    def test_load_json_raises_value_error_for_invalid_payload(self) -> None:
        with self.assertRaises(ValueError):
            core_json_or_yaml_loading("{invalid json}", format_name="json")

    def test_render_yaml_serializes_nested_dict_and_list(self) -> None:
        value = {
            "kind": "Config",
            "metadata": {"name": "demo", "enabled": True},
            "ports": [8080, 9090],
        }

        result = core_json_or_yaml_rendering(value, format_name="yaml")

        self.assertEqual(
            result,
            "\n".join(
                [
                    "kind: Config",
                    "metadata:",
                    "  name: demo",
                    "  enabled: true",
                    "ports:",
                    "  - 8080",
                    "  - 9090",
                ]
            ),
        )

    def test_load_yaml_parses_nested_mapping(self) -> None:
        value = """
kind: Pod
metadata:
  name: web-preview
  namespace: default
spec:
  replicas: 2
""".strip()

        result = core_json_or_yaml_loading(value, format_name="yaml")

        self.assertEqual(
            result,
            {
                "kind": "Pod",
                "metadata": {"name": "web-preview", "namespace": "default"},
                "spec": {"replicas": 2},
            },
        )

    def test_loading_without_format_detects_json_and_yaml(self) -> None:
        json_result = core_json_or_yaml_loading('{"hello":"world"}')
        yaml_result = core_json_or_yaml_loading("hello: world")

        self.assertEqual(json_result, {"hello": "world"})
        self.assertEqual(yaml_result, {"hello": "world"})

    def test_load_yaml_rejects_invalid_indentation(self) -> None:
        value = "kind: Pod\n  metadata:\n    name: demo"

        with self.assertRaises(ValueError):
            core_json_or_yaml_loading(value, format_name="yaml")

    def test_render_or_load_rejects_unsupported_format(self) -> None:
        with self.assertRaises(ValueError):
            core_json_or_yaml_rendering({"hello": "world"}, format_name="toml")
        with self.assertRaises(ValueError):
            core_json_or_yaml_loading("hello = 'world'", format_name="toml")


if __name__ == "__main__":
    unittest.main()
