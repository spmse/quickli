---
title: "Erste Schritte mit quiCkLI: Multi-Command-Anwendungen"
description: >
  Baue ein kubectl-ähnliches CLI mit mehreren benannten Befehlen, gemeinsamen globalen
  Optionen, eigenen Validatoren und expliziter Fehlerbehandlung. Der abschließende Teil
  der Einstiegsreihe zeigt, wie alle quickli-Bausteine zusammenpassen.
slug: quickli-tutorial-03-multi-command-cli
authors:
  - spmse
date: 2026-08-20
tags: [tutorial, quickli, python, cli, multi-command, commands]
series:
  name: "Erste Schritte mit quiCkLI"
  position: 3
keywords: [quickli, multi-command CLI, app.command, CommandExecutionError, python tutorial]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

In den ersten beiden Teilen dieser Reihe hast du ein Begrüßungstool und einen
Datei-Viewer gebaut. In diesem abschließenden Artikel kombinierst du alles Gelernte
und baust `pyk5l`, eine kubectl-ähnliche Multi-Command-Anwendung.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[0]} currentSlug="quickli-tutorial-03-multi-command-cli" />

## Was du bauen wirst

```bash
$ python app.py get pods
$ python app.py get pods --output json --namespace ops
$ python app.py describe pod api-7d4f5f6b89-l2xq9
$ python app.py logs api-7d4f5f6b89-l2xq9 --tail 5 --timestamps
$ python app.py apply manifests/web-pod.yaml --dry-run
```

## `@app.command` vs. `@app.entrypoint`

Bisher hast du `@app.entrypoint` verwendet, das einen einzelnen Handler für die gesamte
Anwendung registriert. Für mehrere Befehle verwendest du stattdessen `@app.command`:

```python
@app.command(
    name="get",
    help_text="Ressourcen im ausgewählten Namespace auflisten.",
    arguments=[...],
    options=[...],
)
def get(resource: str, ...) -> str:
    ...
```

Der `name`-Parameter wird zum ersten Token in der Kommandozeile. Wenn `name` weggelassen
wird, wird der Funktionsname verwendet. Du kannst so viele Befehle registrieren, wie du
benötigst.

## Eigene Validator-Factories

quickli enthält eingebaute Validatoren (`file_path`, `positive_number` und weitere),
aber du kannst eigene nach demselben Muster schreiben:

```python
def one_of(*choices: str):
    allowed = tuple(choices)
    description = "eines von: " + ", ".join(allowed)

    def validate(value: object) -> object:
        if value not in allowed:
            raise ValueError(f"Erwartet eines von: {', '.join(allowed)}")
        return value

    validate.description = description
    return validate
```

Eine Validator-Factory gibt ein Callable zurück, das:
1. Den konvertierten Wert empfängt.
2. Den Wert unverändert zurückgibt, wenn er gültig ist.
3. `ValueError` mit einer klaren Nachricht auslöst, wenn nicht.

## `CommandExecutionError`

`CommandExecutionError` ist für erwartete, domänenspezifische Fehler:

```python
def _find_pod(name: str, namespace: str) -> Pod:
    for pod in PODS:
        if pod.namespace == namespace and pod.name == name:
            return pod
    raise CommandExecutionError(
        f"Pod '{name}' wurde im Namespace '{namespace}' nicht gefunden."
    )
```

Diese Ausnahme propagiert unverändert aus `Application.run()`. Deine Anwendung kann sie
abfangen und in einen Exit-Code umwandeln.

## Globale Optionen, die alle Befehle teilen

Deklariere Optionen einmalig auf `Application`. Jeder Handler, der sie benötigt,
deklariert denselben Parameternamen:

```python
app = Application(
    name="pyk5l",
    global_options=[
        Option("namespace", short_name="n", default="default"),
        Option("output", short_name="o", default="table",
               validators=[one_of("table", "json", "wide")]),
        Option("verbose", short_name="v", is_flag=True),
    ],
)
```

## Was du gelernt hast

- `@app.command` registriert benannte Befehle in einer Multi-Command-Anwendung.
- Eigene Validator-Factories folgen demselben Muster wie eingebaute Validatoren.
- `CommandExecutionError` signalisiert erwartete domänenspezifische Fehler.
- Auf `Application` deklarierte globale Optionen sind für jeden Handler verfügbar.

## Die vollständigen quiCkLI-Bausteine

| Baustein | Zweck |
|---|---|
| `Application` | Wurzel-Container; verwaltet Dispatch und Registrierung |
| `Command` | Benannte Operation (registriert über `@app.command`) |
| `Argument` | Positionaler, geordneter Input |
| `Option` | Benannter Input; Schalter, wiederholbare Werte, Konverter, Validatoren |
| `Plugin` | Wiederverwendbares Befehls-Bundle, das in eine Anwendung geladen wird |

Lies die [Konzept-Referenz](/docs/concepts/quickli-concepts) für die vollständige
API-Dokumentation oder erkunde die [Implementierungsleitfäden](/docs/guides) für
schrittweise Anleitungen.
