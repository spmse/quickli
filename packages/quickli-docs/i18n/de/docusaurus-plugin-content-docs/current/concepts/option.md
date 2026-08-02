---
sidebar_position: 5
description: Option beschreibt eine benannte, reihenfolgeunabhängige Eingabe, die das Befehlsverhalten ändert.
keywords: [quickli, option, flag, benannt, global, lokal, wiederholbar]
---

# Option

`Option` beschreibt eine benannte Eingabe, die das Verhalten eines Befehls verändert.
Optionen gehören zu einem Befehl (lokale Optionen) oder zur `Application` selbst (globale
Optionen).

```
Application
├── globale Optionen   ← für jeden Befehl verfügbar
└── Command
    └── Option         ← du bist hier (lokale Option)
```

## Unterstützte Formen

- lange Form: `--output value`
- lange Zuweisungsform: `--output=value`
- kurze Form: `-o value`

## Grundlegende Funktionen

- Standardwerte
- erforderliche Optionen
- boolesche Schalter (`is_flag=True`)
- Konverter für Werte, die keine Schalter sind
- Validatoren für konvertierte Werte
- wiederholbare Werte (`multiple=True`)

Wiederholbare Optionen, die keine Schalter sind, sammeln Werte in einer Liste. Wiederholbare
Schalter sammeln die Anzahl ihrer Vorkommen.

## Lokale und globale Optionen

Optionen können für Befehle (lokal) oder auf Anwendungsebene (global) definiert werden.
Globale Optionen können vor oder nach dem Befehlsnamen erscheinen.

## Einfaches Optionsbeispiel

```python
from quickli import Application, Argument, Option

app = Application(name="demo")


@app.command(
    help_text="Text in eine Datei schreiben.",
    arguments=[Argument("text")],
    options=[Option("output", short_name="o", default="out.txt")],
)
def write(text: str, output: str = "out.txt") -> str:
    return f"schreibe '{text}' nach {output}"


print(app.run(["write", "hello"]))                      # schreibe 'hello' nach out.txt
print(app.run(["write", "hello", "--output", "a.txt"]))  # schreibe 'hello' nach a.txt
```

## Beispiel für einen booleschen Schalter

```python
from quickli import Application, Option

app = Application(name="demo")


@app.command(
    help_text="Versionsinformationen ausgeben.",
    options=[Option("verbose", short_name="v", is_flag=True)],
)
def version(verbose: bool = False) -> str:
    if verbose:
        return "demo version 1.0.0 (debug build)"
    return "demo 1.0.0"


print(app.run(["version"]))             # demo 1.0.0
print(app.run(["version", "--verbose"]))  # demo version 1.0.0 (debug build)
print(app.run(["version", "-v"]))        # demo version 1.0.0 (debug build)
```

## Beispiel für eine wiederholbare Option

```python
from quickli import Application, Option

app = Application(name="demo")


@app.command(
    help_text="Eine Ressource taggen.",
    options=[Option("tag", short_name="t", multiple=True)],
)
def tag_resource(tag: list[str] | None = None) -> str:
    labels = tag or []
    return f"tags: {', '.join(labels)}"


print(app.run(["tag-resource", "--tag", "a", "--tag", "b"]))  # tags: a, b
```

## Beispiel für eine globale Option

```python
from quickli import Application, Option

app = Application(
    name="demo",
    global_options=[Option("verbose", short_name="v", is_flag=True)],
)


@app.command(help_text="Projekt bauen.")
def build(verbose: bool = False) -> str:
    return f"building… (verbose={verbose})"


print(app.run(["--verbose", "build"]))  # building… (verbose=True)
print(app.run(["build", "--verbose"]))  # building… (verbose=True)
```

## Tipps

:::tip Argument vs. Option
Verwende ein `Argument` für das primäre Subjekt des Befehls (worauf er wirkt). Verwende
eine `Option` für alles, was *verändert, wie* der Befehl sich verhält — Ausgabeformat,
Ausführlichkeitsgrad, ein Schalter oder ein sekundäres Ziel.
:::

:::tip Lokale vs. globale Optionen
Definiere eine Option als **lokal**, wenn sie nur für einen Befehl sinnvoll ist (wie
`--output` für einen Schreibbefehl). Definiere sie als **global**, wenn sie für jeden
Befehl in der Anwendung gelten soll (wie `--verbose` oder `--config`).
:::

:::tip Schalter für An/Aus-Umschalter
Verwende `is_flag=True`, wenn die Option einen booleschen Schalter darstellt, der keinen
Wert annimmt. Das Vorhandensein des Flags setzt es auf `True`; sein Fehlen lässt es auf
`False`.
:::

## Wie geht es weiter?

- Verwende **[Arguments](./argument.md)** für positionelle, geordnete Eingaben.
- Geh zurück zu **[Command](./command.md)**, um zu sehen, wie Optionen und Argumente zusammenpassen.
- Siehe **[Application](./application.md)**, um zu erfahren, wie globale Optionen deklariert werden.
