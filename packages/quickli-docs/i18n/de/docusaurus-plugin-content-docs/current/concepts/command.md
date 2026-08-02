---
sidebar_position: 3
description: Command repräsentiert eine ausführbare Aktion in einer quiCkLI-CLI.
keywords: [quickli, command, subcommand, handler, registrierung]
---

# Command

`Command` repräsentiert eine ausführbare Operation in einer CLI. Befehle leben direkt in
einer `Application` und sind der wichtigste Weg, benannte Aktionen für den Nutzer
bereitzustellen.

```
Application
└── Command   ← du bist hier
    ├── Argument
    ├── Option
    └── Subcommand
        ├── Argument
        └── Option
```

`Subcommand` erbt von `Command` und wird für verschachtelte Befehlsbäume verwendet. Er
verhält sich identisch zu einem `Command`, ist aber unter einem übergeordneten Befehl und
nicht direkt unter der `Application` eingehängt.

## Bestandteile eines Befehls

- ein öffentlicher Befehlsname
- Hilfetext (explizit angegeben oder aus einem Docstring abgeleitet)
- Definitionen positionaler Argumente
- Definitionen benannter Optionen
- optionale Definitionen verschachtelter Subcommands
- ein aufrufbares Handler-Objekt

## Verantwortlichkeiten

Ein Befehl parst die zu ihm gehörenden Tokens, validiert die geparsten Werte anhand der
Ressourcendefinitionen, bindet Werte an die Handler-Signatur und führt den Handler aus.

## Namensverhalten

Befehle werden unter eindeutigen Namen registriert. Funktionsnamen werden durch das
Ersetzen von Unterstrichen durch Bindestriche normalisiert, sofern kein Name ausdrücklich
angegeben wurde.

## Einfaches Befehlsbeispiel

```python
from quickli import Application, Argument, Option

app = Application(name="demo")


@app.command(
    help_text="Jemanden begrüßen.",
    arguments=[Argument("name")],
    options=[Option("shout", is_flag=True)],
)
def greet(name: str, shout: bool = False) -> str:
    msg = f"Hello, {name}!"
    return msg.upper() if shout else msg


print(app.run(["greet", "Alice"]))            # Hello, Alice!
print(app.run(["greet", "Alice", "--shout"]))  # HELLO, ALICE!
```

## Beispiel für verschachtelte Subcommands

Verwende `Subcommand`, wenn ein Befehl natürlich weitere Aktionen gruppiert, etwa
`env create` und `env delete`.

```python
from quickli import Application, Argument, Subcommand

app = Application(name="demo")


@app.command(
    name="env",
    subcommands=[
        Subcommand(
            name="create",
            arguments=[Argument("name")],
            handler=lambda name: f"created:{name}",
        )
    ],
)
def env() -> str:
    return "env"


print(app.run(["env", "create", "dev"]))
```

## Tipps

:::tip Command vs. Subcommand
Verwende einen Top-Level-`@app.command` für voneinander unabhängige Aktionen wie `build`
und `clean`. Verwende einen `Subcommand`, wenn Aktionen logisch einen gemeinsamen
Namensraum teilen, z. B. `env create`, `env list` und `env delete`.
:::

:::tip Hilfetext aus Docstrings
Wenn du kein `help_text` übergibst, verwendet `quickli` automatisch den Docstring der
Funktion. Dadurch bleibt der Handler-Code selbst dokumentierend.

```python
@app.command()
def build() -> str:
    """Das Projekt bauen und ein Release-Artefakt erzeugen."""
    return "building…"
```
:::

## Wie geht es weiter?

- Füge **[Arguments](./argument.md)** hinzu, um positionelle Eingaben anzunehmen.
- Füge **[Options](./option.md)** hinzu, um benannte Flags und Werte anzunehmen.
- Geh zurück zu **[Application](./application.md)**, um zu verstehen, wie Befehle weitergeleitet werden.
