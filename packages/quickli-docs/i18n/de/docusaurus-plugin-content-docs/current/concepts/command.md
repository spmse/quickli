---
sidebar_position: 3
---

# Command

`Command` repräsentiert eine ausführbare Operation in einer CLI.
`Subcommand` erbt von `Command` und wird für verschachtelte Befehlsbäume verwendet.

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

## Beispiel für verschachtelte Subcommands

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
