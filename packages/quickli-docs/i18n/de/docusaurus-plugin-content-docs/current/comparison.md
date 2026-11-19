---
title: quickli, Click und argparse im Vergleich
description: Vergleiche Python-CLI-Bibliotheken und finde die passende Lösung für dein Projekt.
keywords: [quickli, click, argparse, vergleich, python, cli]
---

# quickli, Click und argparse im Vergleich

`quickli`, [Click](https://click.palletsprojects.com/) und Pythons integriertes
[`argparse`](https://docs.python.org/3/library/argparse.html) helfen dir beim Erstellen von
Kommandozeilen-Interfaces, treffen aber unterschiedliche Abwägungen. `quickli` ist ein
kleines, explizites Framework; Click ist eine funktionsreiche Bibliothek von Drittanbietern;
und `argparse` ist ein in Python enthaltener Parser.

## Funktionsvergleich

| Funktion | quickli | Click | argparse |
|---|---|---|---|
| Installation | Das Paket `quickli` installieren | Das Paket `click` installieren | In der Python-Standardbibliothek enthalten |
| Typische API | Ressourcen wie `Application`, `Command`, `Argument` und `Option` | Decorators wie `@click.command()` und `@click.option()` | Einen `ArgumentParser` erstellen, Argumente hinzufügen und anschließend parsen |
| Mehrere Befehle | Befehlsregistrierung der Application und verschachtelte Unterbefehle | Befehle und Gruppen, einschließlich verschachtelter Gruppen | Subparser können Unterbefehle ausführen |
| Hilfe | Generierte Hilfe für Application, Befehle und verschachtelte Befehle; automatische Optionen `--help` und `-h` | Generierte Befehlshilfe mit konfigurierbaren Hilfeoptionen | Generierte Parser-Hilfe, normalerweise mit `-h` und `--help` |
| Konvertierung und Validierung | Explizite Konverter und Validatoren für Argument- und Optionsressourcen | Parametertypen, Callbacks und in das Parametersystem integrierte Validierung | Typen, Aktionen und benutzerdefinierte Validierung im Anwendungscode |
| Zusätzliche Funktionen | Globale Optionen, Erzeugung von Shell-Vervollständigungen, Konfigurationsunterstützung und ein expliziter Plugin-Vertrag | Umfangreiche Funktionen für Prompts, Terminal, Kontext, Tests und Vervollständigung | Flexible Parsing-Grundbausteine; Verhalten auf höherer Ebene wird normalerweise von der Anwendung zusammengestellt |

`quickli` und Click bieten beide ein Framework zum Definieren und Zusammensetzen von
Befehlen. Ihre APIs unterscheiden sich: quickli beschreibt Eingaben mit expliziten
Ressourcenobjekten, während Clicks Decorators Befehlsparameter und Optionen mit dem Handler
verbinden. Zum Beispiel:

```python
# quickli
@app.command(
    arguments=[Argument("name")],
    options=[Option("loud", is_flag=True)],
)
def greet(name: str, loud: bool = False) -> str:
    ...
```

```python
# Click
@click.command()
@click.argument("name")
@click.option("--loud", is_flag=True)
def greet(name: str, loud: bool) -> None:
    ...
```

Mit argparse wird ein ähnlicher Befehl aus Parser-Aufrufen zusammengestellt:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--loud", action="store_true")
args = parser.parse_args()
```

Die Beispiele zeigen den Deklarationsstil und keine vollständigen Anwendungen. Insbesondere
stellt `quickli.Application.main()` eine ausführbare Shell bereit, während
`Application.run()` das Handler-Ergebnis direkt an den Aufrufer zurückgibt.

## Eine `toolbox` mit vier Befehlen

Betrachte eine kleine `toolbox`-Anwendung, die das Kopieren von Dateien, das Erstellen von
Verzeichnissen, das Anlegen von Dateien und die Textausgabe verbindet:

```text
toolbox cp SOURCE DESTINATION
toolbox mkdir PATH
toolbox touch PATH
toolbox echo TEXT
```

Angenommen, die gewöhnlichen Python-Operationsfunktionen
`copy_file(source, destination)`, `make_directory(path)`, `touch_file(path)` und
`echo_text(text)` sind in `operations.py` definiert. Sie führen die Operation aus und geben
eine Nachricht als String zurück. Die Beispiele konzentrieren sich darauf, wie jede
Bibliothek dieselben Befehle zusammenstellt und ausführt.

Mit quickli registrierst du die Funktionen mit expliziten Argumentressourcen. Die Anwendung
stellt Befehlsrouting und ausführbare Hilfe bereit:

```python
from quickli import Application, Argument

from operations import copy_file, echo_text, make_directory, touch_file

app = Application(name="toolbox", description="Datei- und Textwerkzeuge.")

app.register(
    copy_file,
    name="cp",
    arguments=[Argument("source"), Argument("destination")],
)
app.register(
    make_directory,
    name="mkdir",
    arguments=[Argument("path")],
)
app.register(touch_file, name="touch", arguments=[Argument("path")])
app.register(echo_text, name="echo", arguments=[Argument("text")])

if __name__ == "__main__":
    raise SystemExit(app.main())
```

Mit Click organisiert eine Gruppe die Unterbefehle, und Decorators deklarieren die Parameter
jedes Befehls:

```python
import click

from operations import copy_file, echo_text, make_directory, touch_file

@click.group()
def toolbox():
    """Datei- und Textwerkzeuge."""

@toolbox.command()
@click.argument("source")
@click.argument("destination")
def cp(source, destination):
    click.echo(copy_file(source, destination))

@toolbox.command()
@click.argument("path")
def mkdir(path):
    click.echo(make_directory(path))

@toolbox.command()
@click.argument("path")
def touch(path):
    click.echo(touch_file(path))

@toolbox.command()
@click.argument("text")
def echo(text):
    click.echo(echo_text(text))

if __name__ == "__main__":
    toolbox()
```

Mit argparse erstellst du für jeden Unterbefehl einen Parser und leitest die geparsten
Argumente anschließend explizit an die entsprechende Operation weiter:

```python
import argparse

from operations import copy_file, echo_text, make_directory, touch_file

parser = argparse.ArgumentParser(prog="toolbox", description="Datei- und Textwerkzeuge.")
commands = parser.add_subparsers(dest="command", required=True)

cp_parser = commands.add_parser("cp", help="Eine Datei kopieren.")
cp_parser.add_argument("source")
cp_parser.add_argument("destination")
cp_parser.set_defaults(
    run=lambda args: print(copy_file(args.source, args.destination))
)

mkdir_parser = commands.add_parser("mkdir", help="Ein Verzeichnis erstellen.")
mkdir_parser.add_argument("path")
mkdir_parser.set_defaults(run=lambda args: print(make_directory(args.path)))

touch_parser = commands.add_parser("touch", help="Eine Datei erstellen oder ihren Zeitstempel aktualisieren.")
touch_parser.add_argument("path")
touch_parser.set_defaults(run=lambda args: print(touch_file(args.path)))

echo_parser = commands.add_parser("echo", help="Text ausgeben.")
echo_parser.add_argument("text")
echo_parser.set_defaults(run=lambda args: print(echo_text(args.text)))

args = parser.parse_args()
args.run(args)
```

Jedes Design unterstützt diesen Befehlsbaum und generierte Hilfe, aber die Struktur der
Anwendung unterscheidet sich mit zunehmendem Umfang:

| Thema | quickli | Click | argparse |
|---|---|---|---|
| Einen Befehl hinzufügen | Einen Handler und seine `Argument`-/`Option`-Ressourcen bei der Application registrieren | Einen dekorierten Callback zur Befehlsgruppe hinzufügen | Einen Subparser erstellen, Eingaben hinzufügen und den Dispatch-Handler festlegen |
| Dispatch | Von `Application.run()` oder `Application.main()` übernommen | Durch den Aufruf der Gruppe übernommen | Anwendungscode ruft den vom Parser ausgewählten Handler auf |
| Aus einem anderen Modul erweitern | Importierte Handler registrieren oder ein `Plugin` laden | Befehle zu einer Gruppe hinzufügen oder an sie anhängen | Beim Zusammenstellen der Anwendung Subparser hinzufügen oder die Parser-Konfiguration in Anwendungscode auslagern |

Dieses größere Beispiel verdeutlicht die Abwägung: quickli und Click bieten eine
anwendungsweite Befehlsorganisation, während argparse der Anwendung direkte Kontrolle darüber
gibt, wie Parsing und Handler verbunden werden.

Die [vollständigen ausführbaren Anwendungen](https://github.com/spmse/quickli/tree/main/packages/core/examples/complex/toolbox)
verwenden dieselben Dateioperationen. Ihre
[Integrationstests](https://github.com/spmse/quickli/blob/main/packages/core/tests/test_toolbox_examples.py)
testen alle vier Befehle mit temporären Dateien und Verzeichnissen.

## Welche Bibliothek sollte ich wählen?

- **Wähle quickli**, wenn du ein kleines Framework mit expliziten Befehls- und
  Eingabedefinitionen, generierter Hilfe und einer einheitlichen Struktur für eine wachsende
  CLI möchtest. Es eignet sich auch für Projekte, die quicklis integrierte Konzepte für
  Konfiguration, Vervollständigung oder Plugins nutzen möchten.
- **Wähle Click**, wenn du ein ausgereiftes, umfangreiches CLI-Toolkit benötigst, insbesondere
  wegen der besseren Unterstützung für Terminalinteraktionen, Prompts, Befehlskontexte, Tests
  und des großen Ökosystems. Es ist eine gute Wahl für ausgearbeitete,
  benutzerorientierte Kommandozeilenanwendungen.
- **Wähle argparse**, wenn dein CLI unkompliziert ist und du eine Abhängigkeit aus der
  Standardbibliothek mit direkter Kontrolle über das Parserverhalten bevorzugst. Es passt oft
  gut zu Skripten, internen Werkzeugen und Projekten, die kein eigenes CLI-Framework benötigen.

Diese Bibliotheken sind keine direkten Ersetzungen füreinander. Berücksichtige die Komplexität,
die dein CLI heute benötigt, wie viel Framework-Verhalten du bereitstellen lassen möchtest,
und ob du explizite Ressourcendeklarationen, Decorators oder eine direkte Parserkonfiguration
bevorzugst.
