"""Unit tests for the quickli plugin contract and Application.load_plugin()."""

from __future__ import annotations

import unittest

from quickli import Application, Plugin, PluginLoadError


class _GreetPlugin(Plugin):
    """A minimal valid plugin for test purposes."""

    @property
    def name(self) -> str:
        return "greet-plugin"

    @property
    def description(self) -> str:
        return "Adds a greet command."

    def register(self, application: Application) -> None:
        @application.command(help_text="Greets a user by name.")
        def greet(name: str) -> str:
            return f"hello {name}"


class _FaultyPlugin(Plugin):
    """A plugin whose register method raises an unexpected exception."""

    @property
    def name(self) -> str:
        return "faulty-plugin"

    @property
    def description(self) -> str:
        return "Always fails on register."

    def register(self, application: Application) -> None:
        raise RuntimeError("intentional failure")


class _DuplicateCommandPlugin(Plugin):
    """A plugin that tries to register a command already present in the application."""

    @property
    def name(self) -> str:
        return "duplicate-plugin"

    @property
    def description(self) -> str:
        return "Attempts to register an already-registered command."

    def register(self, application: Application) -> None:
        @application.command(name="greet", help_text="Duplicate.")
        def greet(name: str) -> str:
            return f"hi {name}"


class _EmptyNamePlugin(Plugin):
    """A plugin with an empty name, which is invalid."""

    @property
    def name(self) -> str:
        return ""

    @property
    def description(self) -> str:
        return "Has an empty name."

    def register(self, application: Application) -> None:
        pass


class PluginContractTests(unittest.TestCase):
    """Tests that the Plugin abstract base class enforces the correct contract."""

    def test_plugin_cannot_be_instantiated_without_implementing_abstract_methods(self) -> None:
        with self.assertRaises(TypeError):
            Plugin()  # type: ignore[abstract]

    def test_concrete_plugin_exposes_name(self) -> None:
        plugin = _GreetPlugin()
        self.assertEqual(plugin.name, "greet-plugin")

    def test_concrete_plugin_exposes_description(self) -> None:
        plugin = _GreetPlugin()
        self.assertEqual(plugin.description, "Adds a greet command.")


class ApplicationLoadPluginTests(unittest.TestCase):
    """Tests for Application.load_plugin()."""

    def _make_app(self) -> Application:
        return Application(name="demo")

    def test_load_plugin_registers_commands(self) -> None:
        app = self._make_app()
        app.load_plugin(_GreetPlugin())
        self.assertIn("greet", app.commands)

    def test_load_plugin_tracks_loaded_plugins(self) -> None:
        app = self._make_app()
        plugin = _GreetPlugin()
        app.load_plugin(plugin)
        self.assertIn(plugin, app.plugins)

    def test_plugins_property_returns_copy(self) -> None:
        app = self._make_app()
        app.load_plugin(_GreetPlugin())
        first_call = app.plugins
        second_call = app.plugins
        self.assertIsNot(first_call, second_call)

    def test_plugins_property_is_empty_when_no_plugins_loaded(self) -> None:
        app = self._make_app()
        self.assertEqual(app.plugins, [])

    def test_load_plugin_raises_when_name_is_empty(self) -> None:
        app = self._make_app()
        with self.assertRaises(PluginLoadError) as ctx:
            app.load_plugin(_EmptyNamePlugin())
        self.assertIn("empty", str(ctx.exception).lower())

    def test_load_plugin_raises_when_plugin_already_loaded(self) -> None:
        app = self._make_app()
        app.load_plugin(_GreetPlugin())
        with self.assertRaises(PluginLoadError) as ctx:
            app.load_plugin(_GreetPlugin())
        self.assertIn("greet-plugin", str(ctx.exception))

    def test_load_plugin_wraps_unexpected_register_exception(self) -> None:
        app = self._make_app()
        with self.assertRaises(PluginLoadError) as ctx:
            app.load_plugin(_FaultyPlugin())
        self.assertIn("faulty-plugin", str(ctx.exception))
        self.assertIn("intentional failure", str(ctx.exception))

    def test_load_plugin_propagates_plugin_load_error_from_register(self) -> None:
        class _DirectLoadErrorPlugin(Plugin):
            @property
            def name(self) -> str:
                return "direct-error-plugin"

            @property
            def description(self) -> str:
                return "Raises PluginLoadError directly."

            def register(self, application: Application) -> None:
                raise PluginLoadError("explicit load error")

        app = self._make_app()
        with self.assertRaises(PluginLoadError) as ctx:
            app.load_plugin(_DirectLoadErrorPlugin())
        self.assertEqual(str(ctx.exception), "explicit load error")

    def test_load_plugin_wraps_command_registration_error(self) -> None:
        app = self._make_app()

        @app.command(name="greet")
        def greet(name: str) -> str:
            return f"hello {name}"

        with self.assertRaises(PluginLoadError):
            app.load_plugin(_DuplicateCommandPlugin())

    def test_failed_plugin_is_not_added_to_loaded_list(self) -> None:
        app = self._make_app()
        try:
            app.load_plugin(_FaultyPlugin())
        except PluginLoadError:
            pass
        self.assertEqual(len(app.plugins), 0)

    def test_multiple_plugins_can_be_loaded(self) -> None:
        class _InfoPlugin(Plugin):
            @property
            def name(self) -> str:
                return "info-plugin"

            @property
            def description(self) -> str:
                return "Adds an info command."

            def register(self, application: Application) -> None:
                @application.command(help_text="Shows version info.")
                def info() -> str:
                    return "quickli 0.1.0"

        app = self._make_app()
        app.load_plugin(_GreetPlugin())
        app.load_plugin(_InfoPlugin())
        self.assertEqual(len(app.plugins), 2)
        self.assertIn("greet", app.commands)
        self.assertIn("info", app.commands)


if __name__ == "__main__":
    unittest.main()
