"""Application object that coordinates commands and execution."""

from __future__ import annotations

from collections.abc import Iterable
from inspect import getdoc
from typing import Callable

from quickli.argument import Argument
from quickli.command import Command
from quickli.exceptions import CommandNotFoundError, CommandRegistrationError
from quickli.option import Option


class Application:
    """Minimal application container for registering and executing commands."""

    def __init__(
        self,
        name: str,
        description: str = "",
        global_options: Iterable[Option] | None = None,
    ) -> None:
        self.name = name
        self.description = description.strip()
        self._commands: dict[str, Command] = {}
        self._entrypoint: Command | None = None
        self._global_options = tuple(global_options or ())
        self._global_option_parser = Command(
            name="__global__",
            handler=lambda **_: None,
            options=self._global_options,
        )

    @property
    def commands(self) -> dict[str, Command]:
        """Exposes a copy of the registered commands."""
        return dict(self._commands)

    @property
    def global_options(self) -> tuple[Option, ...]:
        """Exposes the registered global options."""
        return self._global_options

    @property
    def entrypoint_command(self) -> Command | None:
        """Returns the application entrypoint when configured."""
        return self._entrypoint

    def register(
        self,
        handler: Callable[..., object],
        *,
        name: str | None = None,
        help_text: str = "",
        arguments: Iterable[Argument] | None = None,
        options: Iterable[Option] | None = None,
    ) -> Callable[..., object]:
        """Registers a function as a command and returns the original handler."""
        command_name = (name or handler.__name__).strip().replace("_", "-")
        resolved_help_text = help_text.strip() or (getdoc(handler) or "").strip()
        if not command_name:
            raise CommandRegistrationError("Command name cannot be empty.")
        if command_name in self._commands:
            raise CommandRegistrationError(f"Command '{command_name}' is already registered.")

        command_options = tuple(options or ())
        self._validate_option_overlap(command_options)

        self._commands[command_name] = Command(
            name=command_name,
            handler=handler,
            help_text=resolved_help_text,
            arguments=tuple(arguments or ()),
            options=command_options,
        )
        return handler

    def command(
        self,
        name: str | None = None,
        *,
        help_text: str = "",
        arguments: Iterable[Argument] | None = None,
        options: Iterable[Option] | None = None,
    ) -> Callable[[Callable[..., object]], Callable[..., object]]:
        """Decorator for registering commands declaratively."""

        def decorator(handler: Callable[..., object]) -> Callable[..., object]:
            return self.register(
                handler,
                name=name,
                help_text=help_text,
                arguments=arguments,
                options=options,
            )

        return decorator

    def register_entrypoint(
        self,
        handler: Callable[..., object],
        *,
        help_text: str = "",
        arguments: Iterable[Argument] | None = None,
        options: Iterable[Option] | None = None,
    ) -> Callable[..., object]:
        """Registers the application-level handler used when no command is selected."""
        if self._entrypoint is not None:
            raise CommandRegistrationError("Application entrypoint is already registered.")

        resolved_help_text = help_text.strip() or (getdoc(handler) or "").strip()
        entrypoint_options = tuple(options or ())
        self._validate_option_overlap(entrypoint_options)
        self._entrypoint = Command(
            name="",
            handler=handler,
            help_text=resolved_help_text,
            arguments=tuple(arguments or ()),
            options=entrypoint_options,
        )
        return handler

    def entrypoint(
        self,
        *,
        help_text: str = "",
        arguments: Iterable[Argument] | None = None,
        options: Iterable[Option] | None = None,
    ) -> Callable[[Callable[..., object]], Callable[..., object]]:
        """Decorator for registering the application-level handler."""

        def decorator(handler: Callable[..., object]) -> Callable[..., object]:
            return self.register_entrypoint(
                handler,
                help_text=help_text,
                arguments=arguments,
                options=options,
            )

        return decorator

    def run(self, argv: Iterable[str] | None = None) -> object:
        """Executes the selected command or returns help when no command is given."""
        arguments = list(argv or [])
        if not arguments:
            if self._entrypoint is not None:
                return self._invoke_entrypoint([], [])
            return self.render_help()

        leading_global_tokens, remaining_arguments = self._consume_leading_global_tokens(arguments)
        if not remaining_arguments:
            if self._entrypoint is not None:
                return self._invoke_entrypoint([], leading_global_tokens)
            return self.render_help()

        command_name, *command_args = remaining_arguments
        if command_name not in self._commands:
            if self._entrypoint is not None:
                return self._invoke_entrypoint(remaining_arguments, leading_global_tokens)
            raise CommandNotFoundError(f"Unknown command: {command_name}")

        command = self._commands[command_name]
        trailing_global_tokens, local_command_args = self._split_global_tokens(
            command,
            command_args,
        )
        global_tokens = [*leading_global_tokens, *trailing_global_tokens]
        _, global_keyword_arguments = self._global_option_parser.parse_options_only(global_tokens)
        positionals, local_keyword_arguments = command.parse(local_command_args)
        merged_keyword_arguments = dict(global_keyword_arguments)
        merged_keyword_arguments.update(local_keyword_arguments)
        return command.invoke(positionals, merged_keyword_arguments)

    def render_help(self) -> str:
        """Builds a plain-text help output for the current application."""
        if self._entrypoint is not None and not self._commands:
            return self._render_entrypoint_help()

        lines: list[str] = [f"Usage: {self.name} <command> [arguments]"]
        if self.description:
            lines.extend(["", self.description])
        if not self._commands:
            lines.extend(["", "No commands registered."])
            return "\n".join(lines)

        if self._entrypoint is not None:
            lines.extend(["", "Application Entry Point:"])
            for line in self._render_entrypoint_help().splitlines():
                lines.append(f"  {line}" if line else "")

        lines.extend(["", "Commands:"])
        detailed_blocks: list[str] = []
        for command in sorted(self._commands.values(), key=lambda item: item.name):
            description = command.help_text or "No description provided."
            lines.append(f"  {command.name:<16}{description}")

            detailed_blocks.append(self._render_command_help(command))

        global_option_lines = self._global_option_parser._render_option_lines()
        if global_option_lines:
            lines.extend(["", "Global Options:", *global_option_lines])

        if detailed_blocks:
            lines.extend(["", "Command Details:"])
            for block in detailed_blocks:
                for line in block.splitlines():
                    lines.append(f"  {line}" if line else "")
                lines.append("")

            if lines[-1] == "":
                lines.pop()

        return "\n".join(lines)

    def _render_command_help(self, command: Command) -> str:
        usage_prefix = self.name
        if self._global_options:
            usage_prefix = (
                f"{usage_prefix} {' '.join(self._global_option_parser.option_usage_parts())}"
            )

        command_help = command.render_help(usage_prefix)
        if not self._global_options:
            return command_help

        global_option_lines = self._global_option_parser._render_option_lines()
        if not global_option_lines:
            return command_help

        return command_help + "\n\nGlobal Options:\n" + "\n".join(global_option_lines)

    def _validate_option_overlap(self, command_options: tuple[Option, ...]) -> None:
        global_destinations = {option.destination for option in self._global_options}
        for option in command_options:
            if option.destination in global_destinations:
                raise CommandRegistrationError(
                    f"Option destination '{option.destination}' conflicts with a global option."
                )

    def _consume_leading_global_tokens(
        self,
        arguments: list[str],
    ) -> tuple[list[str], list[str]]:
        global_tokens: list[str] = []
        option_map = self._build_option_map(self._global_options)
        index = 0
        while index < len(arguments):
            token = arguments[index]
            if token == "--":
                return global_tokens, arguments[index + 1 :]
            if not token.startswith("-") or token == "-":
                break

            option, inline_value = self._resolve_known_option(token, option_map)
            if option is None:
                break

            global_tokens.append(token)
            if option.takes_value and inline_value is None:
                index += 1
                if index >= len(arguments):
                    raise CommandNotFoundError("Missing command name after global options.")
                global_tokens.append(arguments[index])
            index += 1

        return global_tokens, arguments[index:]

    def _split_global_tokens(
        self,
        command: Command,
        arguments: list[str],
    ) -> tuple[list[str], list[str]]:
        global_tokens: list[str] = []
        local_tokens: list[str] = []
        global_option_map = self._build_option_map(self._global_options)
        local_option_map = self._build_option_map(command.options)
        index = 0
        while index < len(arguments):
            token = arguments[index]
            if token == "--":
                local_tokens.extend(arguments[index:])
                break

            if token.startswith("-") and token != "-":
                global_option, global_inline_value = self._resolve_known_option(
                    token,
                    global_option_map,
                )
                if global_option is not None:
                    global_tokens.append(token)
                    if global_option.takes_value and global_inline_value is None:
                        index += 1
                        if index >= len(arguments):
                            raise CommandRegistrationError(f"Option '{token}' requires a value.")
                        global_tokens.append(arguments[index])
                    index += 1
                    continue

                local_option, local_inline_value = self._resolve_known_option(
                    token,
                    local_option_map,
                )
                local_tokens.append(token)
                if (
                    local_option is not None
                    and local_option.takes_value
                    and local_inline_value is None
                ):
                    index += 1
                    if index < len(arguments):
                        local_tokens.append(arguments[index])
                index += 1
                continue

            local_tokens.append(token)
            index += 1

        return global_tokens, local_tokens

    def _invoke_entrypoint(
        self,
        arguments: list[str],
        leading_global_tokens: list[str],
    ) -> object:
        if self._entrypoint is None:
            raise CommandNotFoundError("Application entrypoint is not registered.")

        trailing_global_tokens, local_arguments = self._split_global_tokens(
            self._entrypoint,
            arguments,
        )
        global_tokens = [*leading_global_tokens, *trailing_global_tokens]
        _, global_keyword_arguments = self._global_option_parser.parse_options_only(global_tokens)
        positionals, local_keyword_arguments = self._entrypoint.parse(local_arguments)
        merged_keyword_arguments = dict(global_keyword_arguments)
        merged_keyword_arguments.update(local_keyword_arguments)
        return self._entrypoint.invoke(positionals, merged_keyword_arguments)

    def _render_entrypoint_help(self) -> str:
        if self._entrypoint is None:
            return f"Usage: {self.name} <command> [arguments]"

        usage_prefix = self.name
        if self._global_options:
            usage_prefix = (
                f"{usage_prefix} {' '.join(self._global_option_parser.option_usage_parts())}"
            )

        entrypoint_help = self._entrypoint.render_help(usage_prefix)
        if not self._global_options:
            if self.description:
                return entrypoint_help + "\n\n" + self.description
            return entrypoint_help

        global_option_lines = self._global_option_parser._render_option_lines()
        if not global_option_lines:
            return entrypoint_help

        if self.description:
            entrypoint_help = entrypoint_help + "\n\n" + self.description
        return entrypoint_help + "\n\nGlobal Options:\n" + "\n".join(global_option_lines)

    def _build_option_map(self, options: tuple[Option, ...]) -> dict[str, Option]:
        option_map: dict[str, Option] = {}
        for option in options:
            option_map[option.long_token] = option
            if option.short_token is not None:
                option_map[option.short_token] = option
        return option_map

    def _resolve_known_option(
        self,
        token: str,
        option_map: dict[str, Option],
    ) -> tuple[Option | None, str | None]:
        option_token = token
        inline_value: str | None = None
        if token.startswith("--") and "=" in token:
            option_token, inline_value = token.split("=", 1)

        option = option_map.get(option_token)
        return option, inline_value
