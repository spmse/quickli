---
sidebar_position: 3
description: Command repräsentiert eine ausführbare Operation und Subcommand-Hierarchie in einer quiCkLI-CLI.
keywords: [quickli, command, subcommand, handler, erstellung, registrierung, signaturbindung, docstrings]
---

# Command

`Command` repräsentiert eine einzelne ausführbare Operation in einer CLI-Anwendung. Befehle werden bei einer **[Application](./application.md)** registriert und besitzen positionale **[Argument](./argument.md)**-Definitionen, benannte **[Option](./option.md)**-Definitionen und optionale verschachtelte **[Subcommand](#verschachtelte-subcommands)**-Bäume.

```
Application
└── Command   ← du bist hier
    ├── Argument
    ├── Option
    └── Subcommand
        ├── Argument
        └── Option
```

## Befehlseigenschaften

Ein `Command`-Objekt enthält die folgenden expliziten Attribute:

| Eigenschaft | Typ | Standard | Beschreibung |
|---|---|---|---|
| `name` | `str` | Erforderlich | Öffentlicher Aufrufname (z. B. `"build"`). Wird automatisch aus Funktionsnamen abgeleitet, falls weggelassen. |
| `help_text` | `str \| None` | `None` | Menschlich lesbarer Hilfetext. Wenn `None`, wird der Docstring der Handler-Funktion verwendet. |
| `arguments` | `list[Argument]` | `[]` | Definitionen positionaler Argumente. |
| `options` | `list[Option]` | `[]` | Definitionen benannter lokaler Optionen. |
| `subcommands` | `list[Subcommand]` | `[]` | Definitionen verschachtelter Unterbefehle. |
| `handler` | `Callable` | Erforderlich | Die Python-Funktion, die ausgeführt wird, wenn der Befehl gematcht wird. |

## Wege zum Erstellen und Registrieren von Befehlen

`quickli` unterstützt drei explizite Wege zur Definition und Registrierung von Befehlen:

### 1. Erstellung per Dekorator (`@app.command`)

Das Dekorator-Muster ist der prägnanteste Weg, Befehle direkt neben Handler-Funktionen zu definieren:

```python
from quickli import Application, Argument, Option

app = Application(name="demo")

@app.command(
    name="deploy",
    help_text="Ein Anwendungsziel deployen.",
    arguments=[Argument("target")],
    options=[Option("env", short_name="e", default="production")],
)
def deploy_app(target: str, env: str = "production") -> str:
    return f"Deploying {target} to {env}"

print(app.run(["deploy", "web-api", "-e", "staging"]))
```

### 2. Eigenständige Klasseninstanzierung (`Command`-Instanz)

Du kannst `Command`-Objekte direkt instanziieren, etwa in modularen Codebasen, in denen Befehle über verschiedene Module hinweg definiert sind:

```python
from quickli import Application, Command, Argument, Option

# Modul: commands/build.py
def build_handler(target: str, release: bool = False) -> str:
    mode = "release" if release else "debug"
    return f"Building {target} ({mode})"

build_command = Command(
    name="build",
    help_text="Das Quellprojekt kompilieren.",
    arguments=[Argument("target")],
    options=[Option("release", is_flag=True)],
    handler=build_handler,
)

# Modul: main.py
app = Application(name="demo")
app.register_command(build_command)

print(app.run(["build", "core", "--release"]))
```

### 3. Hilfetext aus Docstrings

Wenn `help_text` weggelassen wird, verwendet `quickli` automatisch den Docstring der Handler-Funktion für die Hilfegenerierung:

```python
from quickli import Application

app = Application(name="demo")

@app.command()
def test() -> str:
    """Alle automatisierten Unit-Tests im Workspace ausführen."""
    return "tests passed"

print(app.run(["test", "--help"]))
```

:::tip[Docstrings halten Code selbstdokumentierend]
Die Verwendung von Docstrings für `help_text` vermeidet Duplikation zwischen Code-Dokumentation und CLI-Hilfebildschirmen.
:::

## Normalisierung von Befehlsnamen

Wird `@app.command()` ohne explizites `name`-Argument verwendet, normalisiert `quickli` Python-Funktionsnamen, indem Unterstriche (`_`) durch Bindestriche (`-`) ersetzt werden:

```python
@app.command()
def list_users() -> str:  # Registrierter Befehlsname: "list-users"
    return "user listing"

print(app.run(["list-users"]))
```

:::note[Explizite Namen überschreiben die Normalisierung]
Wenn du `name="list_users"` explizit an `@app.command()` übergibst, wird genau dieser String als CLI-Befehlsname verwendet.
:::

## Parameter-Bindung & Validierung

Bei der Ausführung parst `quickli` Token in positionale Argumente und Optionen und gleicht diese mit den Parametern der Handler-Funktion ab:

1. **Token-Parsing**: Positionale Token füllen **[Argument](./argument.md)**-Definitionen in Deklarationsreihenfolge. Benannte Token füllen **[Option](./option.md)**-Definitionen.
2. **Konvertierung & Validierung**: Rohe Strings durchlaufen Konverter (z. B. `int`, `Path`) und Validatoren (z. B. `file_path`, `number_range`).
3. **Signaturbindung**: Geparste Werte werden an übereinstimmende Funktionsparameter gebunden. Fehlen erforderliche Argumente oder werden unbekannte Optionen übergeben, wird ein `CommandExecutionError` ausgelöst.

```python
from quickli import Application, Argument, Option

app = Application(name="demo")

@app.command(
    arguments=[Argument("count", converter=int)],
    options=[Option("label", default="item")],
)
def repeat(count: int, label: str = "item") -> str:
    return ", ".join([label] * count)

print(app.run(["repeat", "3", "--label", "hello"]))  # hello, hello, hello
```

:::info[Parameterzuordnung der Signatur]
Handler-Parameternamen **müssen** exakt mit den definierten `Argument`- und `Option`-Ressourcennamen übereinstimmen.
:::

## Verschachtelte Subcommands

`Subcommand` erbt alle Fähigkeiten von `Command` und ermöglicht verschachtelte Befehlsbäume (z. B. `git remote add` oder `kubectl config view`):

```python
from quickli import Application, Command, Subcommand, Argument, Option

app = Application(name="cloud")

@app.command(
    name="env",
    help_text="Cloud-Umgebungen verwalten.",
    subcommands=[
        Subcommand(
            name="create",
            help_text="Eine neue Umgebung erstellen.",
            arguments=[Argument("env_name")],
            options=[Option("region", default="us-east-1")],
            handler=lambda env_name, region="us-east-1": f"Created {env_name} in {region}",
        ),
        Subcommand(
            name="delete",
            help_text="Eine Umgebung löschen.",
            arguments=[Argument("env_name")],
            handler=lambda env_name: f"Deleted {env_name}",
        ),
    ],
)
def env_root() -> str:
    return "Use 'cloud env --help' to list subcommands."

print(app.run(["env", "create", "staging", "--region", "eu-central-1"]))
```

:::tip[Subcommand-Scope]
Subcommands erben globale Optionen der **[Application](./application.md)**, aber lokale Optionen gehören spezifisch zu dem Befehl oder Subcommand, an dem sie deklariert wurden.
:::

## Wie geht es weiter?

- Lerne, wie positionale Eingaben in **[Argument](./argument.md)** funktionieren.
- Lerne mehr über Flags, wiederholbare Werte und Kurzaliase in **[Option](./option.md)**.
- Erfahre, wie globale Optionen in **[Application](./application.md)** konfiguriert werden.
- Verarbeite strukturierte Daten mit **[Parsers](./parsers.md)**.
- Binde wiederverwendbare Befehlssätze über **[Plugin](./plugin.md)** ein.

