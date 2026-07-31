"""Unit tests for JSON/YAML rendering and loading helpers."""

from __future__ import annotations

import unittest

from quickli import load_json, load_toml, load_yaml
from quickli import render_json, render_toml, render_yaml


class ParserTests(unittest.TestCase):
    def test_render_json_returns_indented_sorted_output(self) -> None:
        result = render_json({"name": "Ada", "active": True})

        self.assertEqual(result, '{\n  "active": true,\n  "name": "Ada"\n}')

    def test_load_json_parses_payload(self) -> None:
        result = load_json('{"name":"Ada","count":2}')

        self.assertEqual(result, {"name": "Ada", "count": 2})

    def test_load_json_raises_value_error_for_invalid_payload(self) -> None:
        with self.assertRaises(ValueError):
            load_json("{invalid json}")

    def test_render_yaml_serializes_nested_dict_and_list(self) -> None:
        value = {
            "kind": "Config",
            "metadata": {"name": "demo", "enabled": True},
            "ports": [8080, 9090],
        }

        result = render_yaml(value)

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

        result = load_yaml(value)

        self.assertEqual(
            result,
            {
                "kind": "Pod",
                "metadata": {"name": "web-preview", "namespace": "default"},
                "spec": {"replicas": 2},
            },
        )

    def test_loading_json_and_yaml_uses_explicit_functions(self) -> None:
        json_result = load_json('{"hello":"world"}')
        yaml_result = load_yaml("hello: world")

        self.assertEqual(json_result, {"hello": "world"})
        self.assertEqual(yaml_result, {"hello": "world"})

    def test_load_yaml_rejects_invalid_indentation(self) -> None:
        value = "kind: Pod\n  metadata:\n    name: demo"

        with self.assertRaises(ValueError):
            load_yaml(value)

    def test_toml_round_trip(self) -> None:
        value = {"name": "Ada", "active": True, "server": {"port": 8080}}
        rendered = render_toml(value)

        self.assertEqual(load_toml(rendered), value)

    def test_toml_render_rejects_deep_tables(self) -> None:
        with self.assertRaises(TypeError):
            render_toml({"server": {"tls": {"enabled": True}}})


if __name__ == "__main__":
    unittest.main()
