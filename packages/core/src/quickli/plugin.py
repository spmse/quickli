"""Plugin contract and base class for the quickli plugin system."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from quickli.application import Application


class Plugin(ABC):
    """Abstract base class that defines the contract every quickli plugin must implement.

    A plugin extends a :class:`~quickli.Application` instance by registering commands,
    options, or other resources without modifying the core package.

    Minimal example::

        import quickli

        class GreetPlugin(quickli.Plugin):
            @property
            def name(self) -> str:
                return "greet-plugin"

            @property
            def description(self) -> str:
                return "Adds a greet command to the application."

            def register(self, application: quickli.Application) -> None:
                @application.command(help_text="Greets a user.")
                def greet(name: str) -> str:
                    return f"hello {name}"
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique, human-readable identifier for this plugin.

        The name is used in error messages and diagnostic output.
        It must not be empty.
        """

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description of what this plugin provides.

        The description is used in help output and diagnostic messages.
        """

    @abstractmethod
    def register(self, application: Application) -> None:
        """Register this plugin's commands and resources against *application*.

        This method is called once when the plugin is loaded.  It should add
        commands, options, or any other resources that this plugin provides.
        Raise :class:`~quickli.exceptions.PluginLoadError` to signal an
        unrecoverable loading failure.

        :param application: The :class:`~quickli.Application` instance to extend.
        """
