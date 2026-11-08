"""Integration tests for the three toolbox example applications."""

from __future__ import annotations

import contextlib
import importlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner


EXAMPLE_DIR = Path(__file__).resolve().parents[1] / "examples" / "complex" / "toolbox"
CORE_SRC = Path(__file__).resolve().parents[1] / "src"

for import_path in (str(CORE_SRC), str(EXAMPLE_DIR)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

quickli_app = importlib.import_module("quickli_app")
click_app = importlib.import_module("click_app")
argparse_app = importlib.import_module("argparse_app")


class ToolboxExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_quickli_toolbox_commands(self) -> None:
        source, destination = self._prepare_source()
        output = io.StringIO()
        error = io.StringIO()

        self.assertEqual(
            quickli_app.app.main(
                ["cp", str(source), str(destination)],
                stdout=output,
                stderr=error,
            ),
            0,
        )
        self.assertEqual(destination.read_text(encoding="utf-8"), "source contents")
        self.assertIn(f"Copied {source} to {destination}", output.getvalue())

        directory = self.root / "nested" / "directory"
        self._assert_quickli_output(
            ["mkdir", str(directory)],
            f"Created directory {directory}",
        )
        self.assertTrue(directory.is_dir())

        touched_file = self.root / "new-file"
        self._assert_quickli_output(
            ["touch", str(touched_file)],
            f"Touched {touched_file}",
        )
        self.assertTrue(touched_file.is_file())
        self._assert_quickli_output(["echo", "hello toolbox"], "hello toolbox")

    def test_click_toolbox_commands(self) -> None:
        source, destination = self._prepare_source()
        runner = CliRunner()

        result = runner.invoke(click_app.toolbox, ["cp", str(source), str(destination)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(destination.read_text(encoding="utf-8"), "source contents")
        self.assertIn(f"Copied {source} to {destination}", result.output)

        result = runner.invoke(
            click_app.toolbox, ["mkdir", str(self.root / "nested" / "directory")]
        )
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((self.root / "nested" / "directory").is_dir())

        result = runner.invoke(click_app.toolbox, ["touch", str(self.root / "new-file")])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue((self.root / "new-file").is_file())

        result = runner.invoke(click_app.toolbox, ["echo", "hello toolbox"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, "hello toolbox\n")

    def test_argparse_toolbox_commands(self) -> None:
        source, destination = self._prepare_source()

        output = self._run_argparse(["cp", str(source), str(destination)])
        self.assertEqual(destination.read_text(encoding="utf-8"), "source contents")
        self.assertIn(f"Copied {source} to {destination}", output)

        self._run_argparse(["mkdir", str(self.root / "nested" / "directory")])
        self.assertTrue((self.root / "nested" / "directory").is_dir())
        self._run_argparse(["touch", str(self.root / "new-file")])
        self.assertTrue((self.root / "new-file").is_file())
        self.assertEqual(self._run_argparse(["echo", "hello toolbox"]), "hello toolbox\n")

    def _prepare_source(self) -> tuple[Path, Path]:
        source = self.root / "source.txt"
        destination = self.root / "copy.txt"
        source.write_text("source contents", encoding="utf-8")
        return source, destination

    def _assert_quickli_output(self, argv: list[str], expected: str = "") -> None:
        output = io.StringIO()
        error = io.StringIO()
        self.assertEqual(
            quickli_app.app.main(argv, stdout=output, stderr=error),
            0,
            error.getvalue(),
        )
        self.assertEqual(output.getvalue().strip(), expected)

    @staticmethod
    def _run_argparse(argv: list[str]) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            argparse_app.main(argv)
        return output.getvalue()
