"""Unit tests for the minimal application container."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from quickli import Application, Argument, Option, directory_path, file_path
from quickli import number_range, positive_number
from quickli.exceptions import CommandExecutionError, CommandNotFoundError
from quickli.exceptions import CommandRegistrationError


class ApplicationTests(unittest.TestCase):
    def test_run_executes_registered_command(self) -> None:
        app = Application(name="demo")

        @app.command(help_text="Greets a user.")
        def greet(name: str) -> str:
            return f"hello {name}"

        result = app.run(["greet", "Ada"])

        self.assertEqual(result, "hello Ada")

    def test_run_executes_application_entrypoint_without_commands(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(arguments=[Argument("name")])
        def greet(name: str) -> str:
            return f"hello {name}"

        result = app.run(["Ada"])

        self.assertEqual(result, "hello Ada")

    def test_run_executes_application_entrypoint_with_no_arguments(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(arguments=[Argument("path", required=False, default=".")])
        def show(path: str = ".") -> str:
            return path

        result = app.run([])

        self.assertEqual(result, ".")

    def test_run_returns_help_when_no_command_is_provided(self) -> None:
        app = Application(name="demo", description="Example application")

        output = app.run([])

        self.assertIn("Usage: demo <command> [arguments]", output)
        self.assertIn("No commands registered.", output)

    def test_render_help_for_commandless_application_uses_entrypoint_usage(self) -> None:
        app = Application(name="demo", description="Example application")

        @app.entrypoint(
            help_text="Greets a user.",
            arguments=[Argument("name", help_text="Name to greet.")],
            options=[Option("uppercase", short_name="u", is_flag=True)],
        )
        def greet(name: str, uppercase: bool = False) -> str:
            return name.upper() if uppercase else name

        output = app.render_help()

        self.assertIn("Usage: demo [--uppercase] NAME", output)
        self.assertIn("Greets a user.", output)
        self.assertIn("Name to greet. [required]", output)

    def test_command_names_take_precedence_over_entrypoint(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(arguments=[Argument("value")])
        def fallback(value: str) -> str:
            return f"fallback:{value}"

        @app.command(name="show")
        def show() -> str:
            return "command"

        result = app.run(["show"])

        self.assertEqual(result, "command")

    def test_entrypoint_is_used_when_no_command_matches(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(arguments=[Argument("value")])
        def fallback(value: str) -> str:
            return f"fallback:{value}"

        @app.command(name="show")
        def show() -> str:
            return "command"

        result = app.run(["other"])

        self.assertEqual(result, "fallback:other")

    def test_global_option_is_applied_to_entrypoint(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("verbose", short_name="v", is_flag=True)],
        )

        @app.entrypoint(arguments=[Argument("path")])
        def show(path: str, verbose: bool = False) -> tuple[str, bool]:
            return path, verbose

        result = app.run(["README.md", "--verbose"])

        self.assertEqual(result, ("README.md", True))

    def test_duplicate_entrypoint_registration_raises_error(self) -> None:
        app = Application(name="demo")

        @app.entrypoint()
        def first() -> str:
            return "first"

        with self.assertRaises(CommandRegistrationError):

            @app.entrypoint()
            def second() -> str:
                return "second"

    def test_argument_validator_checks_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            file_path_value = root / "notes.txt"
            file_path_value.write_text("hello", encoding="utf-8")

            app = Application(name="demo")

            @app.entrypoint(arguments=[Argument("target", validators=[file_path()])])
            def read(target: Path) -> Path:
                return target

            result = app.run([str(file_path_value)])

            self.assertEqual(result, file_path_value)

    def test_argument_validator_rejects_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing = Path(tmp_dir) / "missing.txt"
            app = Application(name="demo")

            @app.entrypoint(arguments=[Argument("target", validators=[file_path()])])
            def read(target: Path) -> Path:
                return target

            with self.assertRaises(CommandExecutionError):
                app.run([str(missing)])

    def test_option_validator_checks_existing_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            app = Application(name="demo")

            @app.entrypoint(options=[Option("path", validators=[directory_path()])])
            def show(path: Path | None = None) -> Path | None:
                return path

            result = app.run(["--path", str(root)])

            self.assertEqual(result, root)

    def test_option_validator_rejects_file_for_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            file_path_value = root / "notes.txt"
            file_path_value.write_text("hello", encoding="utf-8")
            app = Application(name="demo")

            @app.entrypoint(options=[Option("path", validators=[directory_path()])])
            def show(path: Path | None = None) -> Path | None:
                return path

            with self.assertRaises(CommandExecutionError):
                app.run(["--path", str(file_path_value)])

    def test_directory_validator_allows_missing_path_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "new-dir"
            app = Application(name="demo")

            @app.entrypoint(arguments=[Argument("path", validators=[directory_path(exists=None)])])
            def create(path: Path) -> Path:
                return path

            result = app.run([str(target)])

            self.assertEqual(result, target)

    def test_option_default_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            app = Application(name="demo")

            @app.entrypoint(options=[Option("path", default=root, validators=[directory_path()])])
            def show(path: Path | None = None) -> Path | None:
                return path

            result = app.run([])

            self.assertEqual(result, root)

    def test_positive_number_validator_accepts_positive_values(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(
            arguments=[Argument("count", converter=int, validators=[positive_number()])]
        )
        def show(count: int) -> int:
            return count

        result = app.run(["5"])

        self.assertEqual(result, 5)

    def test_positive_number_validator_rejects_zero(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(
            arguments=[Argument("count", converter=int, validators=[positive_number()])]
        )
        def show(count: int) -> int:
            return count

        with self.assertRaises(CommandExecutionError):
            app.run(["0"])

    def test_number_range_validator_accepts_in_range_values(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(
            options=[
                Option(
                    "limit",
                    converter=int,
                    validators=[number_range(min_value=1, max_value=10)],
                )
            ]
        )
        def show(limit: int | None = None) -> int | None:
            return limit

        result = app.run(["--limit", "7"])

        self.assertEqual(result, 7)

    def test_number_range_validator_rejects_out_of_range_values(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(
            options=[
                Option(
                    "limit",
                    converter=int,
                    validators=[number_range(min_value=1, max_value=10)],
                )
            ]
        )
        def show(limit: int | None = None) -> int | None:
            return limit

        with self.assertRaises(CommandExecutionError):
            app.run(["--limit", "20"])

    def test_help_includes_validator_metadata(self) -> None:
        app = Application(name="demo")

        @app.entrypoint(
            arguments=[Argument("path", validators=[file_path()])],
            options=[Option("limit", converter=int, validators=[positive_number()])],
        )
        def show(path: Path, limit: int | None = None) -> tuple[Path, int | None]:
            return path, limit

        output = app.render_help()

        self.assertIn("expects: existing file path", output)
        self.assertIn("expects: positive number", output)

    def test_command_help_falls_back_to_docstring(self) -> None:
        app = Application(name="demo")

        @app.command()
        def show() -> str:
            """Shows generated command help text."""
            return "ok"

        output = app.render_help()

        self.assertIn("Shows generated command help text.", output)

    def test_entrypoint_help_falls_back_to_docstring(self) -> None:
        app = Application(name="demo")

        @app.entrypoint()
        def show() -> str:
            """Shows generated entrypoint help text."""
            return "ok"

        output = app.render_help()

        self.assertIn("Shows generated entrypoint help text.", output)

    def test_duplicate_command_name_raises_error(self) -> None:
        app = Application(name="demo")

        @app.command(name="build")
        def build() -> str:
            return "ok"

        with self.assertRaises(CommandRegistrationError):
            app.register(build, name="build")

    def test_unknown_command_raises_error(self) -> None:
        app = Application(name="demo")

        with self.assertRaises(CommandNotFoundError):
            app.run(["missing"])

    def test_invalid_argument_count_is_wrapped(self) -> None:
        app = Application(name="demo")

        @app.command()
        def greet(name: str) -> str:
            return f"hello {name}"

        with self.assertRaises(CommandExecutionError):
            app.run(["greet"])

    def test_command_uses_argument_and_option_resources(self) -> None:
        app = Application(name="demo")

        @app.command(
            name="cat",
            arguments=[Argument("path", help_text="File path to read.")],
            options=[
                Option(
                    "number",
                    short_name="n",
                    help_text="Show line numbers.",
                    is_flag=True,
                )
            ],
        )
        def cat(path: str, number: bool = False) -> tuple[str, bool]:
            return path, number

        result = app.run(["cat", "README.md", "--number"])

        self.assertEqual(result, ("README.md", True))

    def test_option_with_value_is_passed_as_keyword_argument(self) -> None:
        app = Application(name="demo")

        @app.command(
            arguments=[Argument("path")],
            options=[Option("encoding", short_name="e", default="utf-8")],
        )
        def read(path: str, encoding: str = "utf-8") -> tuple[str, str]:
            return path, encoding

        result = app.run(["read", "notes.txt", "--encoding", "latin-1"])

        self.assertEqual(result, ("notes.txt", "latin-1"))

    def test_required_option_must_be_present(self) -> None:
        app = Application(name="demo")

        @app.command(options=[Option("format", required=True)])
        def render(format: str) -> str:
            return format

        with self.assertRaises(CommandExecutionError):
            app.run(["render"])

    def test_optional_argument_uses_default_value(self) -> None:
        app = Application(name="demo")

        @app.command(arguments=[Argument("target", required=False, default="world")])
        def hello(target: str = "world") -> str:
            return f"hello {target}"

        result = app.run(["hello"])

        self.assertEqual(result, "hello world")

    def test_help_mentions_registered_argument_and_option_resources(self) -> None:
        app = Application(name="demo")

        @app.command(
            help_text="Prints a file.",
            arguments=[Argument("path")],
            options=[Option("number", short_name="n", is_flag=True)],
        )
        def cat(path: str, number: bool = False) -> tuple[str, bool]:
            return path, number

        output = app.render_help()

        self.assertIn("Usage: demo cat [--number] PATH", output)
        self.assertIn("Arguments:", output)
        self.assertIn("PATH", output)
        self.assertIn("Options:", output)
        self.assertIn("--number, -n", output)

    def test_help_includes_required_and_default_metadata(self) -> None:
        app = Application(name="demo")

        @app.command(
            name="read",
            help_text="Reads a file.",
            arguments=[Argument("path", help_text="Input file path.")],
            options=[
                Option("encoding", short_name="e", default="utf-8", help_text="Text encoding."),
                Option("format", required=True, help_text="Output format."),
            ],
        )
        def read(
            path: str,
            encoding: str = "utf-8",
            format: str | None = None,
        ) -> tuple[str, str, str | None]:
            return path, encoding, format

        output = app.render_help()

        self.assertIn("Usage: demo read [--encoding ENCODING] --format FORMAT PATH", output)
        self.assertIn("Input file path. [required]", output)
        self.assertIn("Text encoding. [default: utf-8]", output)
        self.assertIn("Output format. [required]", output)

    def test_unknown_option_raises_error(self) -> None:
        app = Application(name="demo")

        @app.command(options=[Option("number", short_name="n", is_flag=True)])
        def cat(number: bool = False) -> bool:
            return number

        with self.assertRaises(CommandExecutionError):
            app.run(["cat", "--missing"])

    def test_argument_converter_transforms_input(self) -> None:
        app = Application(name="demo")

        @app.command(arguments=[Argument("count", converter=int)])
        def repeat(count: int) -> int:
            return count

        result = app.run(["repeat", "3"])

        self.assertEqual(result, 3)

    def test_option_converter_transforms_input(self) -> None:
        app = Application(name="demo")

        @app.command(options=[Option("limit", converter=int, default=10)])
        def head(limit: int = 10) -> int:
            return limit

        result = app.run(["head", "--limit", "5"])

        self.assertEqual(result, 5)

    def test_argument_converter_error_is_wrapped(self) -> None:
        app = Application(name="demo")

        @app.command(arguments=[Argument("count", converter=int)])
        def repeat(count: int) -> int:
            return count

        with self.assertRaises(CommandExecutionError):
            app.run(["repeat", "three"])

    def test_option_converter_error_is_wrapped(self) -> None:
        app = Application(name="demo")

        @app.command(options=[Option("limit", converter=int)])
        def head(limit: int) -> int:
            return limit

        with self.assertRaises(CommandExecutionError):
            app.run(["head", "--limit", "many"])

    def test_repeatable_local_option_collects_values(self) -> None:
        app = Application(name="demo")

        @app.command(options=[Option("include", short_name="i", multiple=True)])
        def show(include: list[str] | None = None) -> list[str] | None:
            return include

        result = app.run(["show", "--include", "README.md", "-i", "docs/usage.md"])

        self.assertEqual(result, ["README.md", "docs/usage.md"])

    def test_repeatable_flag_counts_occurrences(self) -> None:
        app = Application(name="demo")

        @app.command(options=[Option("verbose", short_name="v", is_flag=True, multiple=True)])
        def show(verbose: int = 0) -> int:
            return verbose

        result = app.run(["show", "-v", "--verbose", "-v"])

        self.assertEqual(result, 3)

    def test_global_option_is_parsed_before_command(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("verbose", short_name="v", is_flag=True)],
        )

        @app.command(arguments=[Argument("path")])
        def show(path: str, verbose: bool = False) -> tuple[str, bool]:
            return path, verbose

        result = app.run(["--verbose", "show", "README.md"])

        self.assertEqual(result, ("README.md", True))

    def test_repeatable_global_option_collects_values(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("config", short_name="c", converter=int, multiple=True)],
        )

        @app.command()
        def show(config: list[int] | None = None) -> list[int] | None:
            return config

        result = app.run(["--config", "1", "-c", "2", "show"])

        self.assertEqual(result, [1, 2])

    def test_global_option_is_parsed_after_command(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("verbose", short_name="v", is_flag=True)],
        )

        @app.command(arguments=[Argument("path")])
        def show(path: str, verbose: bool = False) -> tuple[str, bool]:
            return path, verbose

        result = app.run(["show", "README.md", "--verbose"])

        self.assertEqual(result, ("README.md", True))

    def test_global_option_can_be_interleaved_with_local_options(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("verbose", short_name="v", is_flag=True)],
        )

        @app.command(
            arguments=[Argument("path")],
            options=[Option("encoding", short_name="e")],
        )
        def show(
            path: str,
            encoding: str | None = None,
            verbose: bool = False,
        ) -> tuple[str, str | None, bool]:
            return path, encoding, verbose

        result = app.run(["show", "README.md", "--verbose", "--encoding", "utf-8"])

        self.assertEqual(result, ("README.md", "utf-8", True))

    def test_repeatable_global_option_can_be_parsed_after_command(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("config", short_name="c", converter=int, multiple=True)],
        )

        @app.command()
        def show(config: list[int] | None = None) -> list[int] | None:
            return config

        result = app.run(["show", "--config", "1", "-c", "2"])

        self.assertEqual(result, [1, 2])

    def test_global_and_local_help_are_rendered_separately(self) -> None:
        app = Application(
            name="demo",
            global_options=[
                Option(
                    "verbose",
                    short_name="v",
                    is_flag=True,
                    help_text="Global verbosity.",
                )
            ],
        )

        @app.command(
            help_text="Print a file.",
            arguments=[Argument("path")],
            options=[Option("number", short_name="n", is_flag=True, help_text="Local numbering.")],
        )
        def cat(path: str, number: bool = False, verbose: bool = False) -> tuple[str, bool, bool]:
            return path, number, verbose

        output = app.render_help()

        self.assertIn("Global Options:", output)
        self.assertIn("Global verbosity. [flag]", output)
        self.assertIn("Local numbering. [flag]", output)
        self.assertIn("Usage: demo [--verbose] cat [--number] PATH", output)

    def test_global_and_local_option_conflict_raises_error(self) -> None:
        app = Application(
            name="demo",
            global_options=[Option("verbose", short_name="v", is_flag=True)],
        )

        with self.assertRaises(CommandRegistrationError):

            @app.command(options=[Option("verbose", short_name="q", is_flag=True)])
            def show(verbose: bool = False) -> bool:
                return verbose


if __name__ == "__main__":
    unittest.main()
