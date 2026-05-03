# Argument Specification

## Purpose

An argument is a required input value that is passed positionally to a command.

## Current Status

- Arguments are modeled as dedicated metadata objects.
- The current implementation can convert raw string values before calling the handler.
- Each argument stores a public name, help text, required flag, optional default, and
- optional metavar.
- Arguments may also define a conversion callable.
- Arguments may also define one or more validators.
- Validation is driven by the argument definition and the handler signature.
- Validator metadata may be surfaced in generated help output.

## Technical Notes

- Support required and optional positional arguments.
- Support conversion through callables such as `int`.
- Support validation through callables that run after conversion.
- Built-in validators include file paths, directory paths, positive numbers, and number ranges.
- Missing required arguments raise deterministic execution errors.
- Extra positional input currently raises an execution error.

## Future Extensions

- Support repeated positional arguments.
- Support richer usage and validation messages.

## Risks

- Early over-modeling could make the API harder to learn.
- Delaying explicit argument objects too long could make future parsing changes harder.
