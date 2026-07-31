---
sidebar_position: 1
description: Die wichtigsten Konzepte des quiCkLI-Frameworks im Überblick.
keywords: [quickli, konzepte, application, command, argument, option, plugin]
---

# quiCkLI-Konzepte

`quickli` ist aus einer kleinen Menge expliziter Konzepte aufgebaut. Jedes Konzept hat
seine eigene Dokumentationsseite, damit das Modell weiterentwickelt werden kann, ohne ein
einziges Dokument zu überfüllen.

## Konzeptseiten

- [Application](./application.md)
- [Command](./command.md)
- [Argument](./argument.md)
- [Option](./option.md)
- [Parsers](./parsers.md)
- [Plugin](./plugin.md)

## Wie die Konzepte zusammenpassen

In einem typischen Ablauf:

1. Eine `Application` erstellen
2. Einen oder mehrere `Command`-Handler registrieren
3. Die `Argument`- und `Option`-Ressourcen jedes Befehls definieren
4. Die Anwendung mit Kommandozeilen-Argumenten (`argv`-Token) ausführen
