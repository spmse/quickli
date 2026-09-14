---
sidebar_position: 4
description: Argument beschreibt einen erforderlichen oder optionalen positionalen Eingabewert für einen Befehl.
keywords: [quickli, argument, positional, erforderlich, optional, converter, validators, metavar, file_path, number_range]
---

# Argument

`Argument` beschreibt einen positionalen Eingabewert für einen **[Command](./command.md)** oder **[Subcommand](./command.md#verschachtelte-subcommands)**. Argumente werden in der festen Reihenfolge abgeglichen, in der sie in der Befehlsdefinition deklariert wurden.

```
Application
└── Command
    └── Argument   ← du bist hier
```

## Argument-Eigenschaften

Beim Definieren eines `Argument` kannst du mehrere Eigenschaften konfigurieren:

| Eigenschaft | Typ | Standard | Beschreibung |
|---|---|---|---|
| `name` | `str` | Erforderlich | Interner Parametername, der an die Signatur der Handler-Funktion gebunden wird. |
| `help_text` | `str \| None` | `None` | Beschreibung, die in der Befehlshilfe angezeigt wird. |
| `required` | `bool` | `True` | Ob das positionale Argument angegeben werden muss. Bei gesetztem `default` automatisch `False`. |
| `default` | `Any` | `None` | Ersatzwert, falls ein optionales positionales Argument weggelassen wird. |
| `converter` | `Callable \| None` | `None` | Umwandlungsfunktion für das rohe String-Token vor Validierung und Ausführung. |
| `validators` | `list[Callable] \| None` | `None` | Prüffunktionen, die auf den konvertierten Wert angewendet werden. |
| `metavar` | `str \| None` | `None` | Benutzerdefinierter Platzhaltername in Usage-Zeilen und Hilfelisten. |

## Erforderliche vs. optionale Argumente

Positionale Argumente sind standardmäßig **erforderlich**. Sie werden **optional**, sobald ein `default`-Wert angegeben wird:

```python
from quickli import Application, Argument

app = Application(name="demo")

@app.command(
    help_text="Einen Benutzer mit optionalem Ersatznamen begrüßen.",
    arguments=[
        Argument("greeting", help_text="Begrüßungswort."),
        Argument("name", default="World", help_text="Name des Empfängers."),
    ],
)
def greet(greeting: str, name: str = "World") -> str:
    return f"{greeting}, {name}!"

print(app.run(["greet", "Hello"]))          # Hello, World!
print(app.run(["greet", "Hello", "Alice"]))  # Hello, Alice!
```

:::warning[Reihenfolge positionaler Argumente]
Argumente werden fortlaufend von links nach rechts abgeglichen. Platziere alle erforderlichen positionalen Argumente *vor* optionalen positionalen Argumenten, um ein deterministisches Token-Parsing zu gewährleisten.
:::

## Typ-Konverter

Standardmäßig werden Token als rohe Strings an Handler übergeben. Übergib ein `converter`-Callable (wie `int`, `float`, `Path` oder eine benutzerdefinierte Funktion), um das Token automatisch umzuwandeln:

```python
from pathlib import Path
from quickli import Application, Argument

app = Application(name="demo")

@app.command(
    help_text="Zeilenanzahl einer Datei berechnen.",
    arguments=[
        Argument("file", converter=Path, help_text="Zieldateipfad."),
    ],
)
def count_lines(file: Path) -> str:
    lines = len(file.read_text().splitlines())
    return f"{file.name} has {lines} lines"
```

## Integrierte und benutzerdefinierte Validatoren

`quickli` exportiert mehrere integrierte Validatoren, die nach der Typkonvertierung ausgeführt werden:

- `file_path`: Prüft, ob der Pfad existiert und eine Datei ist.
- `directory_path`: Prüft, ob der Pfad existiert und ein Verzeichnis ist.
- `positive_number`: Prüft, ob ein numerischer Wert strikt größer als 0 ist.
- `number_range(min_val, max_val)`: Prüft, ob ein numerischer Wert im Bereich `[min_val, max_val]` liegt.

### Beispiel mit integrierten Validatoren

```python
from pathlib import Path
from quickli import Application, Argument
from quickli import file_path, number_range

app = Application(name="demo")

@app.command(
    help_text="Zieldatei mit bestimmter Thread-Anzahl verarbeiten.",
    arguments=[
        Argument("path", converter=Path, validators=[file_path], metavar="FILE"),
        Argument("threads", converter=int, validators=[number_range(1, 16)], metavar="N"),
    ],
)
def process(path: Path, threads: int) -> str:
    return f"Processing {path.name} with {threads} threads"

print(app.run(["process", "README.md", "4"]))
```

### Beispiel für benutzerdefinierte Validatoren

```python
def validate_even_number(val: int) -> bool:
    if val % 2 != 0:
        raise ValueError("Wert muss eine gerade Zahl sein")
    return True

@app.command(
    arguments=[Argument("amount", converter=int, validators=[validate_even_number])],
)
def split(amount: int) -> str:
    return f"Half is {amount // 2}"
```

:::info[Validator-Metadaten im Hilfetext]
Integrierte Validatoren reichern die Befehlshilfe automatisch an, indem sie erwartete Einschränkungen (z. B. `[1..16]`) neben der Beschreibung darstellen.
:::

## Benutzerdefinierte Metavar-Formatierung

Verwende `metavar`, um anzupassen, wie das positionale Argument in generierten Usage-Strings und Hilfeseiten erscheint:

```python
@app.command(
    arguments=[Argument("target_url", metavar="URL")],
)
def fetch(target_url: str) -> str:
    return f"fetching {target_url}"
```

Usage-Zeile: `Usage: demo fetch URL`

## Leitfaden: Argument vs. Option

:::tip[Entscheidung zwischen Argument und Option]
- Verwende ein **`Argument`** für das primäre **Subjekt** oder Ziel der Operation — das Kern-Objekt, auf das der Befehl wirkt (z. B. einen Quellpfad, eine Benutzer-ID oder einen Projektnamen).
- Verwende eine **`Option`** für Einstellungen oder Flags, die die **Ausführung verändern** (z. B. Ausgabeformat, Log-Level oder Dry-Run-Schalter).
:::

## Wie geht es weiter?

- Erfahre mehr über benannte Eingaben und Flags in **[Option](./option.md)**.
- Siehe, wie Argumente an Befehle gebunden werden in **[Command](./command.md)**.
- Verwende **[Parsers](./parsers.md)** in Konvertern für komplexe String-Eingaben wie JSON oder YAML.

