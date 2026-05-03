# Option Specification

## Purpose

An option is an optional named input that changes command behavior.

## Current Status

- Options are implemented as dedicated metadata objects.
- The initial implementation supports long-form names, optional short aliases, required
	options, default values, and boolean flags.
- Options may also define a conversion callable for non-flag values.
- Options may be marked as repeatable.
- Options may also define one or more validators.
- Validator metadata may be surfaced in generated help output.

## Technical Notes

- Support long-form options such as `--output value`.
- Support `--option=value` and `-o value` forms.
- Treat flags as boolean options that do not require a value.
- Support conversion through callables such as `int` or `pathlib.Path`.
- Support repeatable options through `multiple=True`.
- Support validation through callables that run after conversion.
- Built-in validators include file paths, directory paths, positive numbers, and number ranges.
- Validate option definitions before runtime.

## Future Extensions

- Combined short flags such as `-abc`.
- Option groups and mutually exclusive sets.

## Repeatable Option Behavior

- Repeatable non-flag options accumulate converted values in a list.
- Repeatable flags accumulate occurrence counts as integers.
- Repeatable options can be defined as global or local options.

## Risks

- Option parsing is one of the easiest places to add accidental complexity.
- A premature plugin API for options could freeze poor abstractions.
