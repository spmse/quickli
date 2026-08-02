---
sidebar_position: 4
description: Argument beschreibt einen erforderlichen positionalen Eingabewert für einen Befehl.
keywords: [quickli, argument, positional, erforderlich, optional, converter, validator]
---

# Argument

`Argument` beschreibt einen positionalen Eingabewert für einen Befehl. Argumente gehören
zu einem Befehl (oder Subcommand) und werden in der Reihenfolge aufgelöst, in der sie
deklariert wurden.

```
Application
└── Command
    └── Argument   ← du bist hier
```

## Grundlegendes Verhalten

- Argumente sind positional und geordnet.
- Sie können erforderlich oder optional sein.
- Ein Argument wird optional, sobald es einen Standardwert besitzt.
- Ein Konverter kann Rohtext vor dem Aufruf des Handlers umwandeln.
- Validatoren können konvertierte Werte prüfen.

## Einfaches Beispiel

```python
from quickli import Application, Argument

app = Application(name="demo")


@app.command(
    help_text="Zeichen in einem Wort zählen.",
    arguments=[Argument("word")],
)
def count(word: str) -> str:
    return str(len(word))


print(app.run(["count", "hello"]))  # 5
```

## Optionales Argument mit Standardwert

```python
from quickli import Application, Argument

app = Application(name="demo")


@app.command(
    help_text="Einen Nutzer begrüßen.",
    arguments=[Argument("name", default="World")],
)
def greet(name: str = "World") -> str:
    return f"Hello, {name}!"


print(app.run(["greet"]))           # Hello, World!
print(app.run(["greet", "Alice"]))  # Hello, Alice!
```

## Argument mit Konverter

Übergib ein `converter`-Callable, um den Rohstring vor der Weitergabe an den Handler
umzuwandeln.

```python
from quickli import Application, Argument

app = Application(name="demo")


@app.command(
    help_text="Eine Zahl verdoppeln.",
    arguments=[Argument("value", converter=int)],
)
def double(value: int) -> str:
    return str(value * 2)


print(app.run(["double", "7"]))  # 14
```

## Typische Verwendung

Verwende Argumente für den erforderlichen Kontext eines Befehls, zum Beispiel Pfade,
Bezeichner oder Zielnamen:

- Quellpfad
- Ressourcenname
- numerische Eingabe für eine Operation

Fehlen erforderliche Argumente, schlägt die Befehlsausführung mit einem deterministischen
Fehler fehl.

## Tipps

:::tip Argument vs. Option
Verwende ein `Argument`, wenn der Wert das *Subjekt* des Befehls ist — das, worauf der
Befehl wirkt (ein Dateipfad, ein Name, eine ID). Verwende eine `Option`, wenn der Wert
*verändert, wie* der Befehl sich verhält (ein Format, ein Ausführlichkeitsgrad, ein
Schalter).

```
# Argument: Die Datei ist das, worauf der Befehl wirkt
cat myfile.txt

# Option: Das Format verändert, wie die Ausgabe aussieht
cat --format json myfile.txt
```
:::

:::tip Reihenfolge ist wichtig
Argumente werden positional in der Reihenfolge abgeglichen, in der sie deklariert wurden.
Platziere erforderliche Argumente vor optionalen, um die Befehlssignatur vorhersehbar zu
halten.
:::

## Wie geht es weiter?

- Verwende **[Options](./option.md)** für benannte, reihenfolgeunabhängige Eingaben.
- Geh zurück zu **[Command](./command.md)**, um die vollständige Befehlsstruktur zu sehen.
