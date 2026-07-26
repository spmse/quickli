---
sidebar_position: 1
---

# quiCkLI Concepts

`quickli` is built from a small set of explicit concepts. Each concept has its own
documentation page so the model can evolve without overcrowding one document.

## Concept pages

- [Application](./application.md)
- [Command](./command.md)
- [Argument](./argument.md)
- [Option](./option.md)
- [Plugin](./plugin.md)

## How the concepts fit together

In a typical flow:

1. create an `Application`
2. register one or more `Command` handlers
3. define each command's `Argument` and `Option` resources
4. run the application with command-line arguments (`argv` tokens)
