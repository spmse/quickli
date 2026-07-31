---
id: guide-multi-command-cli
title: "Anleitung 6: CLI mit mehreren Befehlen (pyk5l)"
sidebar_position: 7
description: >
  Erstelle mit quickli eine kubectl-ähnliche CLI mit mehreren Befehlen. Lerne benannte
  Befehle mit @app.command, globale Optionen für alle Befehle, eigene Validatoren und
  CommandExecutionError für fachliche Fehler kennen.
keywords: [quickli, tutorial, multi-command, kubectl, commands, global options, validators]
---

# Anleitung 6: CLI mit mehreren Befehlen (pyk5l)

Diese Anleitung erstellt `pyk5l`, eine kubectl-ähnliche CLI, die zeigt, wie `quickli` eine
realistische Anwendung mit mehreren Befehlen verarbeitet. Sie kombiniert globale
Optionen, Validatoren, Konverter und wiederholbare Optionen aus den vorherigen Anleitungen.

Du lernst:
- mit `@app.command` **mehrere benannte Befehle** zu registrieren
- **globale Optionen** über alle Befehle hinweg zu teilen
- **eigene Validator-Fabriken** (`one_of`, `label_selector`) zu schreiben
- bei erwarteten fachlichen Fehlern `CommandExecutionError` auszulösen
- komplexe Logik in private Hilfsfunktionen aufzuteilen

Der vollständige Quelltext dieses Beispiels befindet sich im Repository unter
[`packages/core/examples/complex/pyk5l/app.py`](https://github.com/spmse/quickli/blob/main/packages/core/examples/complex/pyk5l/app.py).

## Überblick

`pyk5l` stellt vier Befehle bereit:

| Befehl | Funktion |
|---|---|
| `get` | Pods oder Services in einem Namespace auflisten |
| `describe` | Detaillierte Informationen zu einem benannten Pod anzeigen |
| `logs` | Aktuelle Logzeilen eines Pods ausgeben |
| `apply` | Ein Manifest vor einer simulierten Anwendung anzeigen |

Globale Optionen (`--context`, `--namespace`, `--output`, `--verbose`) gelten für jeden
Befehl.

## Die Anwendung einrichten

```python
app = Application(
    name="pyk5l",
    description="A minimal kubectl-like CLI built with quickli.",
    global_options=[
        Option("context", short_name="c", default="dev-cluster", help_text="Cluster context."),
        Option("namespace", short_name="n", default="default", help_text="Namespace to target."),
        Option(
            "output",
            short_name="o",
            default="table",
            validators=[one_of("table", "json", "wide")],
            help_text="Output mode for list commands.",
        ),
        Option("verbose", short_name="v", is_flag=True, help_text="Print execution context."),
    ],
)
```

Globale Optionen werden einmal auf `Application` deklariert. Jeder Command-Handler
erhält sie als Parameter; er muss lediglich den Parameter mit dem richtigen Namen
deklarieren.

## Eigene Validatoren

### `one_of`

```python
def one_of(*choices: str):
    allowed = tuple(choices)
    description = "one of: " + ", ".join(allowed)

    def validate(value: object) -> object:
        if value not in allowed:
            raise ValueError(f"Expected one of: {', '.join(allowed)}")
        return value

    validate.description = description
    return validate
```

`one_of` ist eine Validator-Fabrik: Sie gibt eine Funktion zurück, die prüft, ob ein
Wert zu den erlaubten Auswahlmöglichkeiten gehört. Mit `validate.description` stellst
du eine menschenlesbare Beschreibung bereit, die quickli in Fehlermeldungen und der
Hilfeausgabe verwendet.

### `label_selector`

```python
def label_selector():
    description = "label selector in key=value form"

    def validate(value: object) -> object:
        if not isinstance(value, str) or "=" not in value:
            raise ValueError("Expected a selector in key=value form")
        key, selected_value = value.split("=", 1)
        if not key or not selected_value:
            raise ValueError("Expected a selector in key=value form")
        return value

    validate.description = description
    return validate
```

`label_selector` prüft, ob der Wert dem Format `key=value` entspricht. Der Validator
prüft nur die Form, nicht ob Schlüssel oder Wert sinnvoll sind — dafür ist die Anwendung
zuständig.

## Befehle registrieren

### `get`

```python
@app.command(
    name="get",
    help_text="List resources in the selected namespace.",
    arguments=[
        Argument(
            "resource",
            help_text="Resource kind to list, for example pods or services.",
            validators=[GET_RESOURCE_VALIDATOR],
        )
    ],
    options=[
        Option(
            "selector",
            short_name="l",
            multiple=True,
            validators=[label_selector()],
            help_text="Filter pods with one or more label selectors.",
        ),
        ...
    ],
)
def get(resource: str, ..., context: str = "dev-cluster", namespace: str = "default", ...) -> str:
    ...
```

`@app.command` unterscheidet sich von `@app.entrypoint` durch das Argument `name`. Der
Befehlsname ist das erste Token nach dem Programmnamen:

```bash
python app.py get pods
python app.py get services --output json
```

Der Parameter `name` ist optional. Wenn er fehlt, verwendet quickli den Funktionsnamen.

### `CommandExecutionError`

```python
def _find_pod(name: str, namespace: str) -> Pod:
    for pod in PODS:
        if pod.namespace == namespace and pod.name == name:
            return pod
    raise CommandExecutionError(f"Pod '{name}' was not found in namespace '{namespace}'.")
```

`CommandExecutionError` signalisiert einen erwarteten fachlichen Fehler. quickli verpackt
ihn nicht; die Anwendung kann ihn am Aufrufort abfangen und in einen Exit-Code oder eine
für Benutzer geeignete Meldung umwandeln.

## Ausführen

Klone das Repository und starte es mit einem Beispielmanifest:

```bash
cd packages/core/examples/complex/pyk5l

# Pods auflisten
python app.py get pods

# Pods in einem bestimmten Namespace auflisten
python app.py get pods --namespace ops

# Nach Label filtern
python app.py get pods --selector app=api

# Als JSON ausgeben
python app.py get pods --output json

# Einen Pod beschreiben
python app.py describe pod api-7d4f5f6b89-l2xq9

# Logs ausgeben
python app.py logs api-7d4f5f6b89-l2xq9 --tail 3 --timestamps

# Ein Manifest anwenden (Dry Run)
python app.py apply manifests/web-pod.yaml --dry-run

# Kontextinformationen anzeigen
python app.py get services --verbose
```

## Welche Designprinzipien dieses Beispiel zeigt

1. **Ein Handler pro Befehl** — jeder Handler erledigt eine Aufgabe und erhält seine
   Eingaben direkt als typisierte Parameter.
2. **Validatoren an der Grenze** — die gesamte Eingabevalidierung erfolgt über
   registrierte Validatoren, nicht im Handler.
3. **Hilfsfunktionen für die Darstellung** — private `_render_*`-Funktionen halten die
   Handlerlogik lesbar.
4. **`CommandExecutionError` für fachliche Fehler** — fachliche Fehler verwenden einen
   expliziten Ausnahmetyp statt eines speziellen Rückgabewerts.

## Zusammenfassung

Du hast nun die gesamte Bandbreite der `quickli`-Funktionen gesehen:

- `Application`, `Command`, `Argument`, `Option`
- `@app.entrypoint` und `@app.command`
- Globale Optionen, die von mehreren Befehlen geteilt werden
- Eingebaute Validatoren: `file_path`, `directory_path`, `positive_number`
- Eigene Validator-Fabriken
- Konverter: `int`, `Path`
- Wiederholbare Optionen: `multiple=True`
- `CommandExecutionError` für fachliche Fehler

Lies die [Konzeptreferenz](../concepts/quickli-concepts.md) für die vollständige API-
Dokumentation oder sieh dir den [Blog](../../blog) für vertiefende Beiträge zu einzelnen
Funktionen an.
