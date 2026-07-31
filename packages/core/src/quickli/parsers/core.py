"""Explicit JSON, YAML, and TOML parsing and rendering helpers."""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass


_INTEGER_PATTERN = re.compile(r"^-?(0|[1-9][0-9]*)$")
_FLOAT_PATTERN = re.compile(r"^-?(0|[1-9][0-9]*)\.[0-9]+$")
@dataclass(frozen=True, slots=True)
class _YamlLine:
    indent: int
    content: str
    line_number: int


def render_json(value: object) -> str:
    """Render Python data as deterministic, indented JSON."""
    return json.dumps(value, indent=2, sort_keys=True)


def load_json(value: str) -> object:
    """Load JSON text into Python data."""
    if not isinstance(value, str):
        raise ValueError("Expected a string payload for JSON loading.")
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON input: {error.msg}.") from error


def render_yaml(value: object) -> str:
    """Render Python data as minimal YAML."""
    return _render_yaml(value)


def load_yaml(value: str) -> object:
    """Load minimal YAML text into Python data."""
    if not isinstance(value, str):
        raise ValueError("Expected a string payload for YAML loading.")
    return _load_yaml(value)


def load_toml(value: str) -> dict[str, object]:
    """Load TOML text into a dictionary."""
    if not isinstance(value, str):
        raise ValueError("Expected a string payload for TOML loading.")
    try:
        return dict(tomllib.loads(value))
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"Invalid TOML input: {error.msg}.") from error


def render_toml(value: dict[str, object]) -> str:
    """Render a dictionary as minimal TOML with one level of tables."""
    if not isinstance(value, dict):
        raise TypeError("TOML rendering expects a dictionary.")

    lines: list[str] = []
    sections: list[tuple[str, dict[str, object]]] = []
    for key, item in value.items():
        if isinstance(item, dict):
            sections.append((str(key), item))
        else:
            lines.append(f"{key} = {_render_toml_scalar(item)}")
    for key, section in sections:
        lines.append("") if lines else None
        lines.append(f"[{key}]")
        for field, item in section.items():
            if isinstance(item, dict):
                raise TypeError("TOML rendering supports only one level of tables.")
            lines.append(f"{field} = {_render_toml_scalar(item)}")
    return "\n".join(lines)


def _render_toml_scalar(value: object) -> str:
    if value is None:
        raise TypeError("TOML does not support None values.")
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(_render_toml_scalar(item) for item in value) + "]"
    raise TypeError(f"Unsupported TOML value type: {type(value).__name__}.")


def _render_yaml(value: object, indent: int = 0) -> str:
    if isinstance(value, dict):
        return _render_yaml_mapping(value, indent)
    if isinstance(value, list):
        return _render_yaml_sequence(value, indent)
    return _render_yaml_scalar(value)


def _render_yaml_mapping(value: dict[object, object], indent: int) -> str:
    if not value:
        return "{}"

    lines: list[str] = []
    for key, item in value.items():
        key_text = _render_yaml_key(key)
        prefix = " " * indent
        if _is_yaml_scalar(item):
            lines.append(f"{prefix}{key_text}: {_render_yaml_scalar(item)}")
            continue
        lines.append(f"{prefix}{key_text}:")
        lines.append(_render_yaml(item, indent + 2))
    return "\n".join(lines)


def _render_yaml_sequence(value: list[object], indent: int) -> str:
    if not value:
        return "[]"

    lines: list[str] = []
    for item in value:
        prefix = " " * indent
        if _is_yaml_scalar(item):
            lines.append(f"{prefix}- {_render_yaml_scalar(item)}")
            continue
        lines.append(f"{prefix}-")
        lines.append(_render_yaml(item, indent + 2))
    return "\n".join(lines)


def _render_yaml_key(value: object) -> str:
    if not isinstance(value, str):
        value = str(value)
    if _needs_quoting(value):
        return json.dumps(value)
    return value


def _render_yaml_scalar(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, str):
        value = str(value)
    if _needs_quoting(value):
        return json.dumps(value)
    return value


def _needs_quoting(value: str) -> bool:
    if value == "":
        return True
    if value[0].isspace() or value[-1].isspace():
        return True
    if value.startswith(("-", "?", ":", "@", "`", "!", "&", "*")):
        return True
    if value in {"true", "false", "null", "~", "[]", "{}"}:
        return True
    if _INTEGER_PATTERN.match(value) or _FLOAT_PATTERN.match(value):
        return True
    return any(character in value for character in (":", "#", "\n", "\r"))


def _is_yaml_scalar(value: object) -> bool:
    return value is None or isinstance(value, (bool, int, float, str))


def _load_yaml(value: str) -> object:
    lines = _prepare_yaml_lines(value)
    if not lines:
        return None

    index = 0
    if lines[0].content == "---":
        index = 1
        if index >= len(lines):
            return None

    parsed, index = _parse_yaml_block(lines, index, lines[index].indent)
    if index != len(lines):
        line = lines[index]
        raise ValueError(f"Unexpected YAML content at line {line.line_number}.")
    return parsed


def _prepare_yaml_lines(value: str) -> list[_YamlLine]:
    lines: list[_YamlLine] = []
    for line_number, raw_line in enumerate(value.splitlines(), start=1):
        if not raw_line.strip():
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if raw_line[:indent].count("\t"):
            raise ValueError(f"Tab indentation is not supported (line {line_number}).")

        stripped = raw_line[indent:]
        if stripped.startswith("#"):
            continue

        content = _strip_inline_comment(stripped).strip()
        if not content:
            continue
        lines.append(_YamlLine(indent=indent, content=content, line_number=line_number))
    return lines


def _strip_inline_comment(value: str) -> str:
    result: list[str] = []
    in_single_quote = False
    in_double_quote = False
    index = 0
    while index < len(value):
        character = value[index]
        if character == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            result.append(character)
            index += 1
            continue
        if character == '"' and not in_single_quote:
            previous = value[index - 1] if index > 0 else ""
            if previous != "\\":
                in_double_quote = not in_double_quote
            result.append(character)
            index += 1
            continue
        if (
            character == "#"
            and not in_single_quote
            and not in_double_quote
            and (index == 0 or value[index - 1].isspace())
        ):
            break
        result.append(character)
        index += 1
    return "".join(result).rstrip()


def _parse_yaml_block(
    lines: list[_YamlLine],
    index: int,
    indent: int,
) -> tuple[object, int]:
    if index >= len(lines):
        raise ValueError("Unexpected end of YAML input.")

    if lines[index].indent < indent:
        line = lines[index]
        raise ValueError(f"Unexpected dedent at line {line.line_number}.")

    if lines[index].content.startswith("-"):
        return _parse_yaml_sequence(lines, index, indent)
    return _parse_yaml_mapping(lines, index, indent)


def _parse_yaml_sequence(
    lines: list[_YamlLine],
    index: int,
    indent: int,
) -> tuple[list[object], int]:
    items: list[object] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ValueError(f"Unexpected indentation in YAML sequence at line {line.line_number}.")
        if not line.content.startswith("-"):
            break

        item_text = line.content[1:].strip()
        index += 1

        if item_text:
            items.append(_parse_yaml_scalar(item_text))
            continue

        if index >= len(lines) or lines[index].indent <= indent:
            items.append(None)
            continue

        nested_item, index = _parse_yaml_block(lines, index, lines[index].indent)
        items.append(nested_item)
    return items, index


def _parse_yaml_mapping(
    lines: list[_YamlLine],
    index: int,
    indent: int,
) -> tuple[dict[str, object], int]:
    mapping: dict[str, object] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ValueError(f"Unexpected indentation in YAML mapping at line {line.line_number}.")
        if line.content.startswith("-"):
            break

        key_text, _, value_text = line.content.partition(":")
        if not _:
            raise ValueError(f"Invalid YAML mapping entry at line {line.line_number}.")

        key = _parse_yaml_key(key_text.strip())
        value_fragment = value_text.strip()
        index += 1

        if value_fragment:
            mapping[key] = _parse_yaml_scalar(value_fragment)
            continue

        if index < len(lines) and lines[index].indent > indent:
            nested_value, index = _parse_yaml_block(lines, index, lines[index].indent)
            mapping[key] = nested_value
        else:
            mapping[key] = None
    return mapping, index


def _parse_yaml_key(value: str) -> str:
    parsed = _parse_yaml_scalar(value)
    return parsed if isinstance(parsed, str) else str(parsed)


def _parse_yaml_scalar(value: str) -> object:
    lowered = value.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value == "{}":
        return {}
    if value == "[]":
        return []
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        try:
            return json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid YAML double-quoted string: {error.msg}.") from error
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1].replace("''", "'")
    if _INTEGER_PATTERN.match(value):
        return int(value)
    if _FLOAT_PATTERN.match(value):
        return float(value)
    return value
