"""Shell completion tests for Windows shells (PowerShell).

These tests cover completion script generation for PowerShell,
which is the primary shell on Windows systems.

On Linux and macOS these tests are skipped because PowerShell is not
the native shell on those platforms.
"""

from __future__ import annotations

import sys
import unittest

from quickli import Application, generate_powershell_completion
from quickli.shell_completion import SUPPORTED_SHELLS


@unittest.skipUnless(sys.platform == "win32", "PowerShell completion tests target Windows only")
class PowerShellCompletionTests(unittest.TestCase):
    def test_generate_powershell_completion_includes_app_name(self) -> None:
        script = generate_powershell_completion("myapp", [])

        self.assertIn("myapp", script)

    def test_generate_powershell_completion_includes_all_command_names(self) -> None:
        script = generate_powershell_completion("myapp", ["greet", "version", "deploy"])

        self.assertIn("'greet'", script)
        self.assertIn("'version'", script)
        self.assertIn("'deploy'", script)

    def test_generate_powershell_completion_uses_register_argument_completer(self) -> None:
        script = generate_powershell_completion("myapp", ["greet"])

        self.assertIn("Register-ArgumentCompleter", script)
        self.assertIn("-Native", script)

    def test_generate_powershell_completion_uses_where_object_filter(self) -> None:
        script = generate_powershell_completion("myapp", ["greet"])

        self.assertIn("Where-Object", script)
        self.assertIn("$wordToComplete", script)

    def test_generate_powershell_completion_produces_completion_result(self) -> None:
        script = generate_powershell_completion("myapp", ["greet"])

        self.assertIn("CompletionResult", script)

    def test_generate_powershell_completion_empty_command_list(self) -> None:
        script = generate_powershell_completion("myapp", [])

        self.assertIn("Register-ArgumentCompleter", script)
        self.assertIn("myapp", script)

    def test_generate_powershell_completion_includes_comment_header(self) -> None:
        script = generate_powershell_completion("myapp", [])

        self.assertIn("# PowerShell completion for myapp", script)


@unittest.skipUnless(sys.platform == "win32", "PowerShell completion tests target Windows only")
class ApplicationShellCompletionWindowsTests(unittest.TestCase):
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

    def test_run_shell_completion_powershell_returns_script(self) -> None:
        app = self._make_app()

        result = app.run(["shell-completion", "powershell"])

        self.assertIsInstance(result, str)
        self.assertIn("demo", result)
        self.assertIn("'greet'", result)
        self.assertIn("'version'", result)

    def test_run_shell_completion_pwsh_alias_returns_script(self) -> None:
        app = self._make_app()

        result = app.generate_completion("pwsh")

        self.assertIsInstance(result, str)
        self.assertIn("Register-ArgumentCompleter", result)

    def test_generate_completion_powershell_contains_app_name(self) -> None:
        app = self._make_app()

        result = app.generate_completion("powershell")

        self.assertIn("demo", result)

    def test_generate_completion_raises_for_unsupported_shell(self) -> None:
        app = self._make_app()

        with self.assertRaises(ValueError) as ctx:
            app.generate_completion("cmd")

        self.assertIn("cmd", str(ctx.exception))
        self.assertIn("powershell", str(ctx.exception))

    def test_shell_completion_appears_in_help_output(self) -> None:
        app = self._make_app()

        help_output = app.render_help()

        self.assertIn("shell-completion", help_output)

    def test_supported_shells_constant_contains_powershell(self) -> None:
        self.assertIn("powershell", SUPPORTED_SHELLS)


if __name__ == "__main__":
    unittest.main()
