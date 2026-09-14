---
sidebar_position: 5
description: Option beschreibt eine benannte, reihenfolgeunabhängige Eingabe, die das Befehls- oder Anwendungsverhalten ändert.
keywords: [quickli, option, flag, kurzalias, kombinierte flags, wiederholbar, globale optionen, lokale optionen, validatoren]
---

# Option

`Option` beschreibt eine benannte, reihenfolgeunabhängige Eingabe, die das Verhalten eines Befehls oder der gesamten Anwendung verändert. Optionen können **lokal** für einen bestimmten **[Command](./command.md)** oder **global** für die gesamte **[Application](./application.md)** deklariert werden.

```
Application
├── global_options   ← für jeden Befehl verfügbar (z. B. --verbose, --config)
└── Command
    └── Option       ← lokale Option (du bist hier)
```

## Options-Eigenschaften

Beim Erstellen einer `Option` kannst du die folgenden Eigenschaften konfigurieren:

| Eigenschaft | Typ | Standard | Beschreibung |
|---|---|---|---|
| `name` | `str` | Erforderlich | Optionsname, auf den über CLI-Flags wie `--output` und Handler-Parameter wie `output` zugegriffen wird. |
| `help_text` | `str \| None` | `None` | Menschlich lesbare Erklärung in der Hilfeausgabe. |
| `short_name` | `str \| None` | `None` | Einzelzeichen-Kurzalias (z. B. `"o"` für `-o`). |
| `required` | `bool` | `False` | Ob die Option vom Aufrufer explizit angegeben werden muss. |
| `default` | `Any` | `None` | Standardwert, wenn die Option weggelassen wird. (Standard für `is_flag=True` ist `False`). |
| `is_flag` | `bool` | `False` | Bei `True` wird die Option als boolescher Schalter ohne Wertargument behandelt. |
| `converter` | `Callable \| None` | `None` | Umwandlungs-Callable vor der Validierung. |
| `validators` | `list[Callable] \| None` | `None` | Prüffunktionen nach der Konvertierung. |
| `multiple` | `bool` | `False` | Bei `True` kann die Option auf der Kommandozeile wiederholt werden. |
| `metavar` | `str \| None` | `None` | Benutzerdefinierter Platzhaltertext in Usage-Zeilen und Hilfeseiten (z. B. `metavar="PATH"`). |

## Unterstützte CLI-Syntaxformen

`quickli` unterstützt standardmäßige POSIX- und GNU-CLI-Optionssyntax out-of-the-box:

- **Lange Option mit Leerzeichen**: `--output out.json`
- **Lange Option mit Gleichheitszeichen**: `--output=out.json`
- **Kurze Option mit Leerzeichen**: `-o out.json`
- **Kombinierte Kurzflags**: `-vxf` (äquivalent zu `-v -x -f`, wenn alle Kurzoptionen boolesche Flags sind)

## Boolesche Flags vs. Wertoptionen

### Beispiel für Wertoptionen

```python
from quickli import Application, Option

app = Application(name="demo")

@app.command(
    options=[Option("output", short_name="o", default="out.txt")],
)
def export_data(output: str = "out.txt") -> str:
    return f"saving to {output}"

print(app.run(["export-data", "--output", "report.pdf"]))  # saving to report.pdf
print(app.run(["export-data", "-o", "report.pdf"]))        # saving to report.pdf
print(app.run(["export-data", "--output=report.pdf"]))    # saving to report.pdf
```

### Beispiel für boolesche Flags

```python
@app.command(
    options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Debug-Modus aktivieren."),
    ],
)
def status(verbose: bool = False) -> str:
    return "Status: OK (debug enabled)" if verbose else "Status: OK"

print(app.run(["status"]))             # Status: OK
print(app.run(["status", "--verbose"])) # Status: OK (debug enabled)
print(app.run(["status", "-v"]))       # Status: OK (debug enabled)
```

:::info[Kombinierte Kurzflags]
Werden mehrere Einzelzeichen-Flags zusammen übergeben (z. B. `-abc`), trennt `quickli` diese in einzelne Flags (`-a`, `-b`, `-c`), vorausgesetzt, alle Kurzoptionen sind als Flags registriert (`is_flag=True`).
:::

## Wiederholbare Optionen (`multiple=True`)

`Option` unterstützt zwei unterschiedliche Arten wiederholbaren Verhaltens:

### 1. Wiederholbare Wertoptionen (Listen)

Ist `multiple=True` bei einer Wertoption (`is_flag=False`), sammeln wiederholte Aufrufe konvertierte Werte in einer Python-`list`:

```python
@app.command(
    options=[
        Option("tag", short_name="t", multiple=True, help_text="Tag-Label hinzufügen."),
    ],
)
def tag_item(tag: list[str] | None = None) -> str:
    tags = tag or []
    return f"Applied tags: {', '.join(tags)}"

print(app.run(["tag-item", "--tag", "web", "-t", "v1.0", "--tag", "prod"]))
# Rückgabe: Applied tags: web, v1.0, prod
```

### 2. Wiederholbare Flag-Optionen (Anzahl)

Ist `multiple=True` bei einem booleschen Flag (`is_flag=True`), sammeln wiederholte Flags eine Ganzzahl der Vorkommen (z. B. `-v`, `-vv`, `-v -v -v`):

```python
@app.command(
    options=[
        Option("verbose", short_name="v", is_flag=True, multiple=True),
    ],
)
def run_job(verbose: int = 0) -> str:
    return f"Log verbosity level: {verbose}"

print(app.run(["run-job", "-v"]))     # Log verbosity level: 1
print(app.run(["run-job", "-vvv"]))   # Log verbosity level: 3
```

:::warning[Rückgabetypen wiederholbarer Flags]
Ein Standard-Flag (`is_flag=True`, `multiple=False`) gibt ein `bool` zurück. Ein wiederholbares Flag (`is_flag=True`, `multiple=True`) gibt ein `int` mit der Vorkommensanzahl zurück.
:::

## Globale und lokale Optionen

Optionen können als **lokal** für einen Befehl oder **global** für die Anwendung registriert werden:

```python
app = Application(
    name="demo",
    global_options=[
        Option("config", short_name="c", help_text="Pfad zur Konfigurationsdatei."),
        Option("quiet", short_name="q", is_flag=True, help_text="Ausgabe unterdrücken."),
    ],
)

@app.command(
    options=[
        Option("format", short_name="f", default="json", help_text="Lokale Format-Option."),
    ],
)
def process(format: str = "json", config: str | None = None, quiet: bool = False) -> str:
    return f"format={format}, config={config}, quiet={quiet}"

# Globale Optionen können VOR oder NACH dem Befehlsnamen platziert werden:
print(app.run(["--config", "settings.toml", "process", "-f", "yaml"]))
print(app.run(["process", "-f", "yaml", "--config", "settings.toml", "-q"]))
```

:::note[Platzierung globaler Optionen]
`quickli` filtert globale Optionen flexibel, unabhängig davon, ob der Benutzer sie vor dem Befehlsnamen (`mycli -q process`) oder nach dem Befehlsnamen (`mycli process -q`) platziert.
:::

## Konverter und integrierte Validatoren

Optionen unterstützen Typkonvertierung und Validierung auf dieselbe Weise wie **[Argument](./argument.md)**:

```python
from pathlib import Path
from quickli import Application, Option
from quickli import file_path, positive_number

app = Application(name="demo")

@app.command(
    options=[
        Option(
            "file",
            short_name="f",
            converter=Path,
            validators=[file_path],
            metavar="PATH",
            help_text="Eingabedateipfad.",
        ),
        Option(
            "retries",
            short_name="r",
            converter=int,
            validators=[positive_number],
            default=3,
            help_text="Wiederholungsanzahl.",
        ),
    ],
)
def sync(file: Path | None = None, retries: int = 3) -> str:
    file_name = file.name if file else "none"
    return f"Syncing {file_name} with max {retries} retries"
```

## Wie geht es weiter?

- Vergleiche Optionen mit positionalen Eingaben in **[Argument](./argument.md)**.
- Siehe, wie Optionen an Handler gebunden werden in **[Command](./command.md)**.
- Erfahre, wie anwendungsweite Optionen in **[Application](./application.md)** konfiguriert werden.
- Speichere permanente Einstellungen auf der Festplatte mit **[Config](./config.md)**.

