"""Integration tests for the quickli plugin system.

These tests verify that a plugin can register commands that are
fully dispatched through Application.run() from end to end.
"""

from __future__ import annotations

import unittest

from quickli import Application, Argument, Option, Plugin, PluginLoadError


class _CounterPlugin(Plugin):
    """Plugin that registers a count command with an option and an argument."""

    @property
    def name(self) -> str:
        return "counter-plugin"

    @property
    def description(self) -> str:
        return "Adds a count command that repeats a word."

    def register(self, application: Application) -> None:
        @application.command(
            help_text="Repeats a word N times.",
            arguments=[Argument("word")],
            options=[Option("times", short_name="n", converter=int, default=1)],
        )
        def count(word: str, times: int = 1) -> str:
            return " ".join([word] * times)


class _UpperPlugin(Plugin):
    """Plugin that registers an upper command."""

    @property
    def name(self) -> str:
        return "upper-plugin"

    @property
    def description(self) -> str:
        return "Adds an upper command that converts text to uppercase."

    def register(self, application: Application) -> None:
        @application.command(
            help_text="Converts text to uppercase.",
            arguments=[Argument("text")],
        )
        def upper(text: str) -> str:
            return text.upper()


class PluginIntegrationTests(unittest.TestCase):
    """End-to-end tests that verify a loaded plugin works through Application.run()."""

    def setUp(self) -> None:
        self.app = Application(name="demo", description="Integration test app")
        self.app.load_plugin(_CounterPlugin())

    def test_plugin_command_runs_with_positional_argument(self) -> None:
        result = self.app.run(["count", "hello"])
        self.assertEqual(result, "hello")

    def test_plugin_command_runs_with_option(self) -> None:
        result = self.app.run(["count", "hi", "--times", "3"])
        self.assertEqual(result, "hi hi hi")

    def test_plugin_command_runs_with_short_option(self) -> None:
        result = self.app.run(["count", "hey", "-n", "2"])
        self.assertEqual(result, "hey hey")

    def test_plugin_command_appears_in_help_output(self) -> None:
        help_text = self.app.render_help()
        self.assertIn("count", help_text)

    def test_multiple_plugins_commands_are_independently_callable(self) -> None:
        self.app.load_plugin(_UpperPlugin())
        count_result = self.app.run(["count", "x", "-n", "2"])
        upper_result = self.app.run(["upper", "hello"])
        self.assertEqual(count_result, "x x")
        self.assertEqual(upper_result, "HELLO")

    def test_plugin_command_appears_in_commands_registry(self) -> None:
        self.assertIn("count", self.app.commands)

    def test_loading_same_plugin_twice_raises_plugin_load_error(self) -> None:
        with self.assertRaises(PluginLoadError):
            self.app.load_plugin(_CounterPlugin())

    def test_plugin_metadata_is_accessible(self) -> None:
        plugin = self.app.plugins[0]
        self.assertEqual(plugin.name, "counter-plugin")
        self.assertEqual(plugin.description, "Adds a count command that repeats a word.")

    def test_global_option_and_plugin_command_interact_correctly(self) -> None:
        class _VerboseCountPlugin(Plugin):
            @property
            def name(self) -> str:
                return "verbose-count-plugin"

            @property
            def description(self) -> str:
                return "Adds a count command aware of a global verbose option."

            def register(self, application: Application) -> None:
                @application.command(
                    help_text="Repeats a word N times.",
                    arguments=[Argument("word")],
                    options=[Option("times", short_name="n", converter=int, default=1)],
                )
                def count(word: str, times: int = 1, verbose: bool = False) -> str:
                    result = " ".join([word] * times)
                    if verbose:
                        result = f"[verbose] {result}"
                    return result

        app = Application(
            name="demo",
            global_options=[Option("verbose", short_name="v", is_flag=True)],
        )
        app.load_plugin(_VerboseCountPlugin())

        result = app.run(["--verbose", "count", "hello"])
        self.assertEqual(result, "[verbose] hello")


if __name__ == "__main__":
    unittest.main()
