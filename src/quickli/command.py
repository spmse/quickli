"""Command primitives for the framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from inspect import Signature, signature
from typing import Callable

from quickli.argument import Argument
from quickli.exceptions import CommandExecutionError, CommandRegistrationError
from quickli.option import Option


CommandHandler = Callable[..., object]


@dataclass(slots=True)
class Command:
    """Represents one executable CLI command."""

    name: str
    handler: CommandHandler
    help_text: str = ""
    arguments: tuple[Argument, ...] = field(default_factory=tuple)
    options: tuple[Option, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self.name = self.name.strip().replace("_", "-")
        self.help_text = self.help_text.strip()
        self.arguments = tuple(self.arguments)
        self.options = tuple(self.options)
        self._validate_resources()

    @property
    def signature(self) -> Signature:
        """Returns the handler signature for validation and future introspection."""
        return signature(self.handler)

    @property
    def usage(self) -> str:
        """Returns a usage fragment for help output."""
        parts = [*self.option_usage_parts()]
        if self.name:
            parts.insert(0, self.name)

        for argument in self.arguments:
            argument_usage = argument.display_name
            if not argument.required:
                argument_usage = f"[{argument_usage}]"
            parts.append(argument_usage)

        return " ".join(parts)

    def option_usage_parts(self) -> list[str]:
        """Returns usage fragments for the command options."""
        parts: list[str] = []
        for option in self.options:
            option_usage = option.long_token
            if option.takes_value:
                option_usage = f"{option_usage} {self._option_value_name(option)}"
            if not option.required:
                option_usage = f"[{option_usage}]"
            parts.append(option_usage)
        return parts

    def render_help(self, application_name: str) -> str:
        """Builds detailed help output for the command."""
        lines = [f"Usage: {application_name} {self.usage}"]
        if self.help_text:
            lines.extend(["", self.help_text])

        argument_lines = self._render_argument_lines()
        if argument_lines:
            lines.extend(["", "Arguments:", *argument_lines])

        option_lines = self._render_option_lines()
        if option_lines:
            lines.extend(["", "Options:", *option_lines])

        return "\n".join(lines)

    def execute(self, tokens: list[str]) -> object:
        """Executes the command with parsed positional arguments and options."""
        positionals, keyword_arguments = self.parse(tokens)
        return self.invoke(positionals, keyword_arguments)

    def invoke(
        self,
        positionals: list[object | None],
        keyword_arguments: dict[str, object | None],
    ) -> object:
        """Invokes the underlying handler with already parsed values."""
        try:
            self.signature.bind(*positionals, **keyword_arguments)
        except TypeError as error:
            raise CommandExecutionError(str(error)) from error

        return self.handler(*positionals, **keyword_arguments)

    def parse(
        self,
        tokens: list[str],
    ) -> tuple[list[object | None], dict[str, object | None]]:
        """Parses a token list into positional arguments and keyword options."""
        positional_tokens: list[str] = []
        keyword_arguments = self._build_initial_keyword_arguments(self.options)

        seen_options: set[str] = set()
        option_map = self._build_option_map()
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token == "--":
                positional_tokens.extend(tokens[index + 1 :])
                break

            if token.startswith("-") and token != "-":
                option, inline_value = self._resolve_option(token, option_map)
                seen_options.add(option.destination)

                if option.is_flag:
                    if inline_value is not None:
                        raise CommandExecutionError(
                            f"Flag option '{token}' does not accept a value."
                        )
                    if option.multiple:
                        current_value = keyword_arguments.get(option.destination, 0)
                        keyword_arguments[option.destination] = int(current_value) + 1
                    else:
                        keyword_arguments[option.destination] = True
                    index += 1
                    continue

                if inline_value is None:
                    index += 1
                    if index >= len(tokens):
                        raise CommandExecutionError(f"Option '{token}' requires a value.")
                    inline_value = tokens[index]

                try:
                    converted_value = option.convert(inline_value)
                except ValueError as error:
                    raise CommandExecutionError(str(error)) from error
                if option.multiple:
                    current_values = keyword_arguments.get(option.destination)
                    if current_values is None:
                        current_values = []
                        keyword_arguments[option.destination] = current_values
                    current_values.append(converted_value)
                else:
                    keyword_arguments[option.destination] = converted_value
                index += 1
                continue

            positional_tokens.append(token)
            index += 1

        self._ensure_required_options(seen_options)
        return self._bind_arguments(positional_tokens), keyword_arguments

    def _build_option_map(self) -> dict[str, Option]:
        option_map: dict[str, Option] = {}
        for option in self.options:
            option_map[option.long_token] = option
            if option.short_token is not None:
                option_map[option.short_token] = option
        return option_map

    def parse_options_only(
        self,
        tokens: list[str],
    ) -> tuple[list[str], dict[str, object | None]]:
        """Parses options until the first non-option token and returns the remainder."""
        keyword_arguments = self._build_initial_keyword_arguments(self.options)
        seen_options: set[str] = set()
        option_map = self._build_option_map()
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token == "--":
                return tokens[index + 1 :], keyword_arguments
            if not token.startswith("-") or token == "-":
                break

            option, inline_value = self._resolve_option(token, option_map)
            seen_options.add(option.destination)

            if option.is_flag:
                if inline_value is not None:
                    raise CommandExecutionError(f"Flag option '{token}' does not accept a value.")
                if option.multiple:
                    current_value = keyword_arguments.get(option.destination, 0)
                    keyword_arguments[option.destination] = int(current_value) + 1
                else:
                    keyword_arguments[option.destination] = True
                index += 1
                continue

            if inline_value is None:
                index += 1
                if index >= len(tokens):
                    raise CommandExecutionError(f"Option '{token}' requires a value.")
                inline_value = tokens[index]

            try:
                converted_value = option.convert(inline_value)
            except ValueError as error:
                raise CommandExecutionError(str(error)) from error

            if option.multiple:
                current_values = keyword_arguments.get(option.destination)
                if current_values is None:
                    current_values = []
                    keyword_arguments[option.destination] = current_values
                current_values.append(converted_value)
            else:
                keyword_arguments[option.destination] = converted_value
            index += 1

        self._ensure_required_options(seen_options)
        return tokens[index:], keyword_arguments

    def _resolve_option(
        self,
        token: str,
        option_map: dict[str, Option],
    ) -> tuple[Option, str | None]:
        option_token = token
        inline_value: str | None = None
        if token.startswith("--") and "=" in token:
            option_token, inline_value = token.split("=", 1)

        option = option_map.get(option_token)
        if option is None:
            raise CommandExecutionError(f"Unknown option: {token}")

        return option, inline_value

    def _ensure_required_options(self, seen_options: set[str]) -> None:
        for option in self.options:
            if option.required and option.destination not in seen_options:
                raise CommandExecutionError(f"Missing required option: {option.long_token}")

    def _bind_arguments(self, positional_tokens: list[str]) -> list[object | None]:
        if not self.arguments:
            return positional_tokens

        bound_arguments: list[object | None] = []
        for index, argument in enumerate(self.arguments):
            if index < len(positional_tokens):
                try:
                    bound_arguments.append(argument.convert(positional_tokens[index]))
                except ValueError as error:
                    raise CommandExecutionError(str(error)) from error
                continue

            if argument.required:
                raise CommandExecutionError(f"Missing required argument: {argument.name}")

            try:
                bound_arguments.append(argument.validate(argument.default))
            except ValueError as error:
                raise CommandExecutionError(str(error)) from error

        if len(positional_tokens) > len(self.arguments):
            raise CommandExecutionError("Received too many positional arguments.")

        return bound_arguments

    def _validate_resources(self) -> None:
        argument_names = [argument.name for argument in self.arguments]
        if len(argument_names) != len(set(argument_names)):
            raise CommandRegistrationError("Argument names must be unique within a command.")

        option_names = [option.name for option in self.options]
        destinations = [option.destination for option in self.options]
        short_names = [option.short_name for option in self.options if option.short_name]
        if len(option_names) != len(set(option_names)):
            raise CommandRegistrationError("Option names must be unique within a command.")
        if len(destinations) != len(set(destinations)):
            raise CommandRegistrationError("Option destinations must be unique within a command.")
        if len(short_names) != len(set(short_names)):
            raise CommandRegistrationError("Option short names must be unique within a command.")

    def _render_argument_lines(self) -> list[str]:
        lines: list[str] = []
        for argument in self.arguments:
            label = argument.display_name
            details = self._resource_details(
                required=argument.required,
                default=argument.default,
                validator_descriptions=argument.validator_descriptions,
            )
            description = argument.help_text or "No description provided."
            if details:
                description = f"{description} {details}"
            lines.append(f"  {label:<18}{description}")
        return lines

    def _render_option_lines(self) -> list[str]:
        lines: list[str] = []
        for option in self.options:
            label = option.long_token
            if option.short_token is not None:
                label = f"{label}, {option.short_token}"
            if option.takes_value:
                label = f"{label} {self._option_value_name(option)}"

            details = self._resource_details(
                required=option.required,
                default=option.default,
                is_flag=option.is_flag,
                multiple=option.multiple,
                validator_descriptions=option.validator_descriptions,
            )
            description = option.help_text or "No description provided."
            if details:
                description = f"{description} {details}"
            lines.append(f"  {label:<18}{description}")
        return lines

    def _option_value_name(self, option: Option) -> str:
        return option.destination.upper()

    def _build_initial_keyword_arguments(
        self,
        options: tuple[Option, ...],
    ) -> dict[str, object | None]:
        keyword_arguments: dict[str, object | None] = {}
        for option in options:
            initial_value = option.initial_value()
            if initial_value is not None:
                keyword_arguments[option.destination] = initial_value
            elif option.is_flag:
                keyword_arguments[option.destination] = False
        return keyword_arguments

    def _resource_details(
        self,
        *,
        required: bool,
        default: object | None,
        is_flag: bool = False,
        multiple: bool = False,
        validator_descriptions: list[str] | None = None,
    ) -> str:
        details: list[str] = []
        if required:
            details.append("required")
        if default is not None and not is_flag:
            details.append(f"default: {default}")
        if is_flag:
            details.append("flag")
        if multiple:
            details.append("repeatable")
        if validator_descriptions:
            details.append("expects: " + ", ".join(validator_descriptions))
        if not details:
            return ""
        return "[" + "; ".join(details) + "]"
