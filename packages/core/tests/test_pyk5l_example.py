"""Unit tests for the complex pyk5l example application."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def load_pyk5l_module():
    root = Path(__file__).resolve().parents[1]
    src_path = str(root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    module_path = root / "examples" / "complex" / "pyk5l" / "app.py"
    spec = importlib.util.spec_from_file_location("pyk5l_example", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the pyk5l example module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Pyk5lExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_pyk5l_module()
        cls.manifest_path = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "complex"
            / "pyk5l"
            / "manifests"
            / "web-pod.yaml"
        )

    def test_get_pods_respects_global_namespace_option(self) -> None:
        result = self.module.app.run(["--namespace", "ops", "get", "pods"])

        self.assertIn("jobs-8b4f68c79-rh2vs", result)
        self.assertNotIn("api-7d4f5f6b89-l2xq9", result)

    def test_get_services_uses_kubectl_style_resource_argument(self) -> None:
        result = self.module.app.run(["get", "services", "--service-type", "NodePort"])

        self.assertIn("web", result)
        self.assertNotIn("api  ", result)

    def test_logs_respects_tail_and_strips_timestamps_by_default(self) -> None:
        result = self.module.app.run(["logs", "web-6b5dd6cb6f-ptm8k", "--tail", "2"])

        self.assertIn("rendered home page", result)
        self.assertIn("rendered status page", result)
        self.assertNotIn("2026-05-03T", result)

    def test_apply_reads_manifest_summary(self) -> None:
        result = self.module.app.run(["apply", str(self.manifest_path), "--dry-run"])

        self.assertIn("Mode:        dry-run", result)
        self.assertIn("Resource:    Pod/web-preview", result)
        self.assertIn("Namespace:   default", result)

    def test_describe_uses_kubectl_style_resource_and_name_arguments(self) -> None:
        result = self.module.app.run(["describe", "pod", "api-7d4f5f6b89-l2xq9"])

        self.assertIn("Name:        api-7d4f5f6b89-l2xq9", result)
        self.assertIn("Namespace:   default", result)
