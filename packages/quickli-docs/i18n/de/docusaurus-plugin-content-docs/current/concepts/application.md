---
sidebar_position: 2
description: Application ist der Wurzel-Container jeder quiCkLI-CLI.
keywords: [quickli, application, entrypoint, befehlsregistrierung, run]
---

# Application

`Application` ist der Wurzel-CLI-Container in `quickli`. Er steht an der Spitze der
Konzepthierarchie: Alles andere — Befehle, Argumente, Optionen und Plugins — wird bei
einer `Application`-Instanz registriert.

```
Application   ← du bist hier
├── Command
├── Command
└── Plugin
```

## Was er verwaltet

- Befehlsregistrierung
- Optionale Root-Einstiegspunkt-Registrierung
- Anwendungsweite globale Optionen
- Befehls-Dispatch aus Eingabe-Token
- Anwendungs- und Befehls-Hilfe-Rendering

## Ausführungsmodell

`Application.run()` dispatcht den ausgewählten Befehl und gibt das Handler-Ergebnis
(oder generierten Hilfstext) zurück.

- Er liest `sys.argv[1:]` **standardmäßig**, wenn er ohne Argumente aufgerufen wird.
- Übergib eine explizite Liste zum Überschreiben: `app.run(["greet", "Ada"])`.
- Setze `auto_sys_argv=False` bei der Konstruktion, um stattdessen immer eine leere Liste zu verwenden.
- Er gibt **standardmäßig keine** Ausgabe aus.
- Er wählt **keine** Prozess-Exit-Codes.

Die Ausgabe- und Exit-Code-Verantwortung bleibt bei deinem ausführbaren Wrapper.

## Registrierungs-API

`Application` bietet Dekorator-APIs für die Befehlsregistrierung:

- `@app.command(...)` für benannte Befehle in einem Multi-Command-CLI
- `@app.entrypoint(...)` für einen befehlslosen Root-Ablauf

Wenn beide existieren, haben Befehlsnamen Vorrang, und der Einstiegspunkt wirkt als
Fallback.

## Beispiel für ein Einzelaktions-Tool

Verwende `@app.entrypoint`, wenn dein Tool genau eine Aktion ausführt und keine benannten
Unterbefehle benötigt.

```python
from quickli import Application, Argument

app = Application(name="greet")


@app.entrypoint(arguments=[Argument("name")])
def main(name: str) -> str:
    return f"Hello, {name}!"


print(app.run(["Alice"]))  # Hello, Alice!
```

## Beispiel für ein Multi-Command-Tool

Verwende `@app.command`, wenn dein Tool mehrere verschiedene Aktionen bereitstellt, etwa
`build`, `deploy` und `clean`.

```python
from quickli import Application

app = Application(name="mytool")


@app.command(help_text="Projekt bauen.")
def build() -> str:
    return "building…"


@app.command(help_text="Build-Artefakte bereinigen.")
def clean() -> str:
    return "cleaning…"


print(app.run(["build"]))  # building…
```

## Tipps

:::tip Einzelaktion vs. mehrere Befehle
Verwende `@app.entrypoint` für ein Einzelaktions-Tool (wie `cat` oder `head`) und
`@app.command` für ein Multi-Aktions-Tool (wie `git` oder `kubectl`). Du kannst jederzeit
Befehle hinzufügen — der Einstiegspunkt wirkt als Fallback, wenn kein Befehlsname passt.
:::

:::tip `run()` in einem Wrapper aufrufen
`Application.run()` liest `sys.argv[1:]` standardmäßig und gibt einen String zurück.
Ausgabe und Exit-Code-Behandlung gehören in deinen `main()`-Wrapper, damit die Anwendung
unabhängig testbar bleibt.

```python
if __name__ == "__main__":
    print(app.run())
```

Übergib eine explizite Liste, um den Standard zu überschreiben: `app.run(["greet", "Ada"])`.
Setze `auto_sys_argv=False` bei der Konstruktion, um das automatische Lesen vollständig zu
deaktivieren.
:::

## Wie geht es weiter?

- Füge **[Commands](./command.md)** hinzu, um deiner Anwendung benannte Aktionen zu geben.
- Füge **[Arguments](./argument.md)** und **[Options](./option.md)** hinzu, um Eingaben anzunehmen.
- Verwende **[Plugins](./plugin.md)**, um wiederverwendbare Befehlssets zu laden, ohne den Kern zu ändern.
