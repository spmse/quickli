"""Shell completion tests for Linux shells (bash and zsh).

These tests cover completion script generation for bash and zsh,
which are the primary shells on Linux and macOS systems.

On Windows these tests are skipped because bash and zsh are not
the native shells on that platform.
"""

from __future__ import annotations

import sys
import unittest

from quickli import Application, generate_bash_completion, generate_zsh_completion
from quickli.shell_completion import SUPPORTED_SHELLS


@unittest.skipIf(sys.platform == "win32", "bash and zsh are not native on Windows")
class BashCompletionTests(unittest.TestCase):
    def test_generate_bash_completion_includes_app_name(self) -> None:
        script = generate_bash_completion("myapp", [])

        self.assertIn("myapp", script)

    def test_generate_bash_completion_includes_all_command_names(self) -> None:
        script = generate_bash_completion("myapp", ["greet", "version", "deploy"])

        self.assertIn("greet", script)
        self.assertIn("version", script)
        self.assertIn("deploy", script)

    def test_generate_bash_completion_uses_safe_function_name(self) -> None:
        script = generate_bash_completion("my-app", ["cmd"])

        self.assertIn("_my_app_completion", script)

    def test_generate_bash_completion_registers_complete_directive(self) -> None:
        script = generate_bash_completion("myapp", ["cmd"])

        self.assertIn("complete -F _myapp_completion myapp", script)

    def test_generate_bash_completion_empty_command_list(self) -> None:
        script = generate_bash_completion("myapp", [])

        self.assertIn('local commands=""', script)
        self.assertIn("complete -F _myapp_completion myapp", script)

    def test_generate_bash_completion_uses_compgen(self) -> None:
        script = generate_bash_completion("myapp", ["greet"])

        self.assertIn("compgen", script)
        self.assertIn("COMPREPLY", script)


@unittest.skipIf(sys.platform == "win32", "bash and zsh are not native on Windows")
class ZshCompletionTests(unittest.TestCase):
    def test_generate_zsh_completion_includes_compdef_header(self) -> None:
        script = generate_zsh_completion("myapp", {})

        self.assertIn("#compdef myapp", script)

    def test_generate_zsh_completion_includes_app_name(self) -> None:
        script = generate_zsh_completion("myapp", {})

        self.assertIn("myapp", script)

    def test_generate_zsh_completion_includes_all_command_names(self) -> None:
        script = generate_zsh_completion(
            "myapp",
            {"greet": "Greet a user.", "version": "Show version."},
        )

        self.assertIn("greet", script)
        self.assertIn("version", script)

    def test_generate_zsh_completion_includes_command_descriptions(self) -> None:
        script = generate_zsh_completion("myapp", {"greet": "Greet a user."})

        self.assertIn("Greet a user.", script)

    def test_generate_zsh_completion_uses_fallback_for_empty_description(self) -> None:
        script = generate_zsh_completion("myapp", {"greet": ""})

        self.assertIn("No description provided.", script)

    def test_generate_zsh_completion_uses_describe_builtin(self) -> None:
        script = generate_zsh_completion("myapp", {"greet": "Greet a user."})

        self.assertIn("_describe", script)

    def test_generate_zsh_completion_uses_safe_function_name(self) -> None:
        script = generate_zsh_completion("my-app", {})

        self.assertIn("_my_app", script)

    def test_generate_zsh_completion_empty_command_dict(self) -> None:
        script = generate_zsh_completion("myapp", {})

        self.assertIn("#compdef myapp", script)
        self.assertIn("_describe", script)


@unittest.skipIf(sys.platform == "win32", "bash and zsh are not native on Windows")
class ApplicationShellCompletionLinuxTests(unittest.TestCase):
    def _make_app(self) -> Application:
        app = Application(name="demo", shell_completion=True)

        @app.command(help_text="Greets a user.")
        def greet(name: str) -> str:
            return f"hello {name}"

        @app.command(help_text="Shows the version.")
        def version() -> str:
            return "0.1.0"

        return app

    def test_shell_completion_command_is_registered(self) -> None:
        app = Application(name="demo", shell_completion=True)

        self.assertIn("shell-completion", app.commands)

    def test_shell_completion_command_is_not_registered_by_default(self) -> None:
        app = Application(name="demo")

        self.assertNotIn("shell-completion", app.commands)

    def test_run_shell_completion_bash_returns_script(self) -> None:
        app = self._make_app()

        result = app.run(["shell-completion", "bash"])

        self.assertIsInstance(result, str)
        self.assertIn("demo", result)
        self.assertIn("greet", result)
        self.assertIn("version", result)

    def test_run_shell_completion_zsh_returns_script(self) -> None:
        app = self._make_app()

        result = app.run(["shell-completion", "zsh"])

        self.assertIsInstance(result, str)
        self.assertIn("#compdef demo", result)
        self.assertIn("greet", result)
        self.assertIn("version", result)

    def test_generate_completion_bash_contains_app_name(self) -> None:
        app = self._make_app()

        result = app.generate_completion("bash")

        self.assertIn("demo", result)

    def test_generate_completion_zsh_contains_compdef_header(self) -> None:
        app = self._make_app()

        result = app.generate_completion("zsh")

        self.assertIn("#compdef demo", result)

    def test_generate_completion_raises_for_unsupported_shell(self) -> None:
        app = self._make_app()

        with self.assertRaises(ValueError) as ctx:
            app.generate_completion("fish")

        self.assertIn("fish", str(ctx.exception))
        self.assertIn("bash", str(ctx.exception))

    def test_shell_completion_appears_in_help_output(self) -> None:
        app = self._make_app()

        help_output = app.render_help()

        self.assertIn("shell-completion", help_output)

    def test_supported_shells_constant_contains_bash_and_zsh(self) -> None:
        self.assertIn("bash", SUPPORTED_SHELLS)
        self.assertIn("zsh", SUPPORTED_SHELLS)


if __name__ == "__main__":
    unittest.main()
