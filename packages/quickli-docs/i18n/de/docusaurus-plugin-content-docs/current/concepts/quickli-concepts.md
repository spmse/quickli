---
sidebar_position: 1
description: Umfassende Übersicht über die Kernkonzepte von quiCkLI und deren Zusammenspiel.
keywords: [quickli, konzepte, application, command, argument, option, config, parsers, plugin, hierarchie]
---

# quiCkLI Konzepte

`quickli` basiert auf einer kleinen Gruppe expliziter, modularer Konzepte. Jedes Konzept repräsentiert einen fokussierten Baustein in deiner CLI-Architektur — ohne spekulative Abstraktionen oder versteckte Magie.

```
Application
├── global_options           ← anwendungsweite Flags/Werte
├── Command "build"
│   ├── Argument "target"    ← erforderliche positionale Eingabe
│   └── Option "--output"    ← benanntes lokales Flag oder Einstellung
├── Command "env"
│   └── Subcommand "create"  ← verschachtelte Aktion unter einem Elternbefehl
├── Plugin "metrics"
│   └── Command "stats"      ← externe Befehle, die über das Plugin-Interface eingebunden werden
├── Config                   ← permanente TOML-Konfiguration, die beim Start geladen wird
└── Parsers                  ← Format-Helfer (JSON, YAML, TOML) innerhalb von Handlern
```

## Kernkonzepthierarchie

Jede `quickli`-CLI besitzt eine einzelne **[Application](./application.md)**-Instanz an der Wurzel.

- **[Application](./application.md)** verwaltet die Befehlsregistrierung, verarbeitet globale Optionen, leitet Token an Befehle weiter und steuert das Ausführungsmodell (`run()` vs. `main()`).
- **[Command](./command.md)** kapselt eine einzelne CLI-Operation. Befehle definieren positionale **[Argument](./argument.md)**-Ressourcen und benannte **[Option](./option.md)**-Ressourcen und können verschachtelte **[Subcommand](./command.md#verschachtelte-subcommands)**-Bäume enthalten.
- **[Argument](./argument.md)** repräsentiert erforderliche oder optionale positionale Eingaben in fester Reihenfolge.
- **[Option](./option.md)** repräsentiert benannte, reihenfolgeunabhängige Eingaben (wie `--verbose` oder `--output=file.txt`). Optionen können **lokal** für einen Befehl oder **global** für die gesamte Anwendung sein.
- **[Config](./config.md)** verwaltet dauerhafte TOML-Einstellungen auf der Festplatte und validiert diese beim Start mithilfe von `ConfigSchema`.
- **[Parsers](./parsers.md)** bieten Hilfsfunktionen (`load_json`, `render_yaml`, `load_toml` etc.) zum Parsen und Formatieren strukturierter Daten.
- **[Plugin](./plugin.md)** ermöglicht es externen Paketen oder Modulen, neue Befehle an eine `Application` anzuhängen, ohne den Kerncode zu verändern.

## Wann welches Konzept verwendet werden sollte

| Ziel / Anforderung | Empfohlenes Konzept | Konzeptseite |
|---|---|---|
| CLI-Tool mit einer einzelnen Aktion (wie `cat` oder `head`) | `Application` + `@app.entrypoint` | [Application](./application.md) |
| CLI-Tool mit mehreren Aktionen (wie `git` oder `kubectl`) | `Application` + `@app.command` | [Application](./application.md) / [Command](./command.md) |
| Positionale Eingaben (z. B. Dateipfade) akzeptieren | `Argument` | [Argument](./argument.md) |
| Benannte Flags, Schalter oder Schlüssel-Wert-Einstellungen akzeptieren | `Option` | [Option](./option.md) |
| Flags definieren, die für *alle* Befehle gelten | Globale `Option` an der `Application` | [Option](./option.md#globale-und-lokale-optionen) |
| Benutzereinstellungen in einer TOML-Datei dauerhaft speichern | `Config` + `ConfigSchema` | [Config](./config.md) |
| JSON, YAML oder TOML-Daten innerhalb von Befehlen verarbeiten | `parsers`-Helfer | [Parsers](./parsers.md) |
| Wiederverwendbare Befehlssätze in Paketen auslagern | `Plugin` | [Plugin](./plugin.md) |

:::info[Explizite Architektur]
`quickli` vermeidet versteckte Magie und implizite Annahmen. Ressourcendefinitionen (`Argument`, `Option`, `ConfigField`) deklarieren Typen, Standardwerte, Konverter und Validatoren explizit, sodass Hilfetexte, Parsing und Signaturbindung vollständig deterministisch bleiben.
:::

:::tip[Trennung der Ausführungsmodelle]
Beim Ausführen einer CLI führt `Application.run()` den ausgewählten Befehl aus und gibt dessen String-Ergebnis zurück, ohne Ausgaben zu drucken oder `sys.exit()` aufzurufen. Das macht Unit-Tests denkbar einfach. Für ausführbare Programme ergänzt `Application.main()` `run()` um Standardausgabe-Formatierung, strukturierte Fehlerbehandlung und Prozess-Exit-Codes. Siehe die **[Application](./application.md#ausführungsmodelle-run-vs-main)**-Dokumentation für Details.
:::

:::note[Wo anfangen?]
Wenn du neu bei `quickli` bist, beginne mit der Anleitung **[Erste Schritte](../getting-started.md)**, um deine erste CLI zu bauen, und kehre dann hierher zurück, um die einzelnen Konzepte im Detail zu erkunden.
:::

## Konzeptindex

- **[Application](./application.md)** — Wurzel-CLI-Container, Registrierungs-APIs, globale Optionen und Ausführungsmodelle.
- **[Command](./command.md)** — Befehlserstellung, Docstrings, Subcommands, Signaturbindung und Validierung.
- **[Argument](./argument.md)** — Positionale Eingaben, Konverter, integrierte Validatoren und Metavar-Formatierung.
- **[Option](./option.md)** — Kurz-/Langoptionen, Boolesche Flags, wiederholbare Flags/Werte, lokaler vs. globaler Scope.
- **[Config](./config.md)** — Native TOML-Konfigurationsdateien, Feldvalidierung, Auto-Initialisierung und Schema-JSON.
- **[Parsers](./parsers.md)** — Format-Helfer für JSON-, YAML- und TOML-Serialisierung und -Deserialisierung.
- **[Plugin](./plugin.md)** — Plugin-Vertrag, Registrierungslebenszyklus, Duplikatschutz und Fehlerbehandlung.

