---
sidebar_position: 1
description: Überblick über die Kernkonzepte von quiCkLI und wie sie zusammenhängen.
keywords: [quickli, konzepte, application, command, argument, option, plugin, hierarchie]
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
- [Konfigurationsdateien](./config.md)

## Wie die Konzepte zusammenpassen

Jede `quickli`-CLI hat eine einzige `Application` als Wurzel. Befehle leben innerhalb der
Anwendung. Jeder Befehl besitzt seine Argumente und Optionen. Plugins hängen zusätzliche
Befehle an eine bestehende Anwendung an, ohne den Kern zu ändern.

```
Application
├── globale Optionen        ← benannte Flags/Werte, die jedem Befehl zur Verfügung stehen
├── Command "build"
│   ├── Argument "target"   ← erforderliche positionelle Eingabe
│   └── Option  "--output"  ← optionale benannte Eingabe
├── Command "deploy"
│   ├── Subcommand "dev"
│   └── Subcommand "prod"
└── Plugin "metrics"
    └── Command "stats"
```

In einem typischen Ablauf:

1. Eine `Application` erstellen.
2. Einen oder mehrere `Command`-Handler registrieren (oder einen einzelnen Root-`entrypoint`).
3. Die `Argument`- und `Option`-Ressourcen jedes Befehls definieren.
4. Die Anwendung mit Kommandozeilen-Token (`argv`) ausführen.

## Wann welches Konzept verwenden

| Du möchtest… | Verwende… |
|---|---|
| Ein Tool mit einer einzigen Aktion bauen | `Application` + `@app.entrypoint` |
| Ein Tool mit mehreren Aktionen bauen | `Application` + `@app.command` |
| Positionelle Eingaben wie einen Dateipfad annehmen | `Argument` |
| Ein benanntes Flag oder eine Einstellung annehmen | `Option` |
| Verhalten aus einem separaten Paket hinzufügen | `Plugin` |
| Benutzereinstellungen zwischen Ausführungen speichern | `Config` |
| Strukturierte Daten als JSON, YAML oder TOML lesen/schreiben | `parsers`-Helfer |

:::tip Nicht sicher, wo du anfangen sollst?
Lies zuerst [Erste Schritte](../getting-started.md) und schau dann hier nach, um die
einzelnen Konzepte im Detail zu erkunden.
:::
