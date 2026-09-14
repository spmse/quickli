---
sidebar_position: 2
description: Application ist der Wurzel-Container und Ausführungsmanager jeder quiCkLI-CLI.
keywords: [quickli, application, entrypoint, befehlsregistrierung, run, main, globale optionen, shell completion]
---

# Application

`Application` ist der Wurzel-CLI-Container und Ausführungsmanager in `quickli`. Er steht an der Spitze der Konzepthierarchie: Alles andere — Befehle, globale Optionen, Plugins und Ausführungseinstellungen — wird bei einer `Application`-Instanz registriert oder konfiguriert.

```
Application   ← du bist hier
├── global_options
├── Command / Subcommand
├── Entrypoint (Fallback / Einzelaktion)
└── Plugin
```

## Was Application verwaltet

- **Befehlsregistrierung**: Verwaltet registrierte **[Command](./command.md)**-Objekte und verhindert doppelte Befehlsnamen.
- **Root-Einstiegspunkt**: Unterstützt Einzelaktions-CLIs über `@app.entrypoint`.
- **Globale Optionen**: Definiert anwendungsweite **[Option](./option.md)**-Flags/Werte, die für alle Befehle verfügbar sind.
- **Befehls-Dispatch**: Parst `argv`-Token, ordnet Befehle/Subcommands zu und bindet Argumente und Optionen an Handler.
- **Hilfe-Rendering**: Generiert automatisch strukturierte Hilfetexte für die Anwendung und alle registrierten Befehle.
- **Shell-Vervollständigung**: Generiert optional Tab-Vervollständigungsskripte für `bash`, `zsh` und `powershell`.
- **Ausführungsmodelle**: Bietet `run()` für Bibliotheks-/Testzwecke und `main()` für ausführbare CLIs.

## Anwendungskonstruktionsparameter

Bei der Instanziierung von `Application` kannst du mehrere Kernverhalten anpassen:

```python
from quickli import Application, Option

app = Application(
    name="mytool",
    description="Ein Mehrzweck-Entwickler-CLI.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Ausführliche Ausgabe aktivieren."),
    ],
    shell_completion=True,
    auto_sys_argv=True,
    error_handler=None,
)
```

| Parameter | Typ | Standard | Beschreibung |
|---|---|---|---|
| `name` | `str` | `"app"` | Der Anwendungsname, der in Hilfetexten und Usage-Zeilen verwendet wird. |
| `description` | `str \| None` | `None` | Kurze Beschreibung, die oben in der Anwendungshilfe angezeigt wird. |
| `global_options` | `list[Option] \| None` | `None` | Liste globaler **[Option](./option.md)**-Definitionen, die für alle Befehle gelten. |
| `shell_completion` | `bool` | `False` | Bei `True` wird automatisch ein integrierter `shell-completion`-Befehl registriert. |
| `auto_sys_argv` | `bool` | `True` | Bei `True` liest `run()` standardmäßig `sys.argv[1:]`, wenn `argv` gleich `None` ist. |
| `error_handler` | `Callable \| None` | `None` | Optionaler Fehler-Callback zur Überprüfung oder Anpassung von Ausnahmen vor der Ausgabe in `main()`. |

## Befehlsregistrierungs-Methoden

`Application` unterstützt vier verschiedene Wege zum Erstellen und Registrieren von Befehlen:

### 1. Dekorator-Registrierung (`@app.command`)

Der gebräuchlichste Weg zur Registrierung benannter Befehle in Multi-Command-Tools.

```python
from quickli import Application, Argument, Option

app = Application(name="demo")

@app.command(
    name="greet",
    help_text="Begrüße einen Benutzer namentlich.",
    arguments=[Argument("name")],
    options=[Option("shout", is_flag=True)],
)
def greet_user(name: str, shout: bool = False) -> str:
    msg = f"Hello, {name}!"
    return msg.upper() if shout else msg
```

### 2. Imperative Befehlsregistrierung (`app.register_command`)

Nützlich, wenn Befehle dynamisch erstellt oder in separaten Modulen mit der `Command`-Klasse definiert werden.

```python
from quickli import Application, Command, Argument

app = Application(name="demo")

build_cmd = Command(
    name="build",
    help_text="Ziel-Artefakt bauen.",
    arguments=[Argument("target")],
    handler=lambda target: f"building {target}…",
)

app.register_command(build_cmd)
```

### 3. Root-Einstiegspunkt-Registrierung (`@app.entrypoint`)

Verwendet für Einzelaktions-Tools (wie `cat` oder `head`), die keine Befehlsnamen benötigen.

```python
from quickli import Application, Argument

app = Application(name="quickhead")

@app.entrypoint(
    arguments=[Argument("file_path")],
)
def main_action(file_path: str) -> str:
    return f"Reading top lines of {file_path}"

print(app.run(["notes.txt"]))
```

:::note[Befehlsvorrang bei Einstiegspunkten]
Wenn eine `Application` sowohl Befehle als auch einen Root-Einstiegspunkt definiert, werden Eingabe-Token, die einem registrierten Befehlsnamen entsprechen, an diesen Befehl weitergeleitet. Passt kein Befehlsname, greift der Root-Einstiegspunkt als Fallback.
:::

### 4. Plugin-Registrierung (`app.load_plugin`)

Verwendet zum Anhängen externer Befehlsmodule über den **[Plugin](./plugin.md)**-Vertrag.

```python
from quickli import Application, Plugin

class AuditPlugin(Plugin):
    @property
    def name(self) -> str:
        return "audit"
    
    @property
    def description(self) -> str:
        return "Sicherheitsaudit-Befehle"

    def register(self, application: Application) -> None:
        @application.command(help_text="Sicherheitsprüfung ausführen.")
        def check() -> str:
            return "audit passed"

app = Application(name="demo")
app.load_plugin(AuditPlugin())
```

## Globale Optionen

Globale Optionen gelten für die gesamte Anwendung und können vor oder nach dem Befehlsnamen übergeben werden:

```python
app = Application(
    name="demo",
    global_options=[
        Option("config", short_name="c", help_text="Pfad zur Konfigurationsdatei."),
        Option("verbose", short_name="v", is_flag=True, help_text="Ausführliches Logging."),
    ],
)

@app.command(help_text="Deployment ausführen.")
def deploy(config: str | None = None, verbose: bool = False) -> str:
    return f"deploying (config={config}, verbose={verbose})"

# Beide Token-Reihenfolgen sind gültig:
print(app.run(["--verbose", "deploy", "-c", "app.toml"]))
print(app.run(["deploy", "-c", "app.toml", "--verbose"]))
```

:::info[Verfügbarkeit globaler Optionen]
Globale Optionen werden automatisch in Handler-Signaturen injiziert, wenn der Handler Parameter akzeptiert, deren Namen mit den globalen Optionen übereinstimmen. Siehe **[Option](./option.md#globale-und-lokale-optionen)** für weitere Details.
:::

## Ausführungsmodelle: `run()` vs. `main()`

`Application` trennt Bibliotheks-Befehlsausführung explizit von ausführbaren Einstiegspunkten:

### `Application.run(argv=None)`

Führt die Befehlsausführungsschleife aus und gibt das Ergebnis oder den Hilfetext als String zurück.

- **Argumente**: `argv` (`list[str] | None`). Wenn `None` und `auto_sys_argv=True`, wird `sys.argv[1:]` gelesen.
- **Nebeneffekte**: Keine (druckt nicht auf stdout/stderr und beendet den Prozess nicht).
- **Rückgabewert**: Rückgabewert des gematchten Befehlshandlers (in String umgewandelt) oder generierter Hilfetext.

```python
# Reine String-Ausführung — ideal für Unit-Tests:
output = app.run(["greet", "Alice"])
assert output == "Hello, Alice!"
```

### `Application.main(argv=None, output_format="text")`

Bietet eine ausführbare Hülle für CLI-Binärdateien (`if __name__ == "__main__":`).

- **Ausgabehandhabung**: Druckt erfolgreiche Ergebnisse direkt auf die Standardausgabe.
- **Exit-Codes**: Liefer `0` bei Erfolg oder Fehler-Exit-Codes bei Fehlschlägen zurück.
- **Maschinenlesbare Ausgabe**: Übergib `output_format="json"`, um JSON-Payloads für automatisierte Agenten oder Skripte auszugeben.
- **Fehlerbehandlung**: Wandelt unbehandelte Ausnahmen in strukturierte `UserCodeError`- oder `InternalCLIError`-Instanzen um.

```python
if __name__ == "__main__":
    app.main()
```

#### JSON-Ausgabeformat-Beispiel

```python
app.main(argv=["greet", "Alice"], output_format="json")
# Gibt JSON-Payload aus:
# {"status": "success", "result": "Hello, Alice!"}
```

## Integrierte Shell-Vervollständigung

Wenn `shell_completion=True` gesetzt ist, registriert die `Application` automatisch einen `shell-completion`-Befehl:

```python
app = Application(name="mycli", shell_completion=True)

# Vervollständigungsskript programmgesteuert generieren:
bash_script = app.generate_completion("bash")
zsh_script = app.generate_completion("zsh")
ps_script = app.generate_completion("powershell")
```

Benutzer können Shell-Vervollständigungsskripte direkt aus der CLI generieren:

```bash
mycli shell-completion bash > /etc/bash_completion.d/mycli
```

:::tip[Shell-Vervollständigung testen]
Die eigenständigen Generatoren `generate_bash_completion`, `generate_zsh_completion` und `generate_powershell_completion` sind auch direkt über das Hauptpaket `quickli` verfügbar.
:::

## Benutzerdefinierte Fehler-Handler

Du kannst einen benutzerdefinierten `error_handler`-Callback an `Application` übergeben, um Ausnahmen zu verarbeiten oder zu formatieren, bevor `main()` sie ausgibt:

```python
def log_and_format_error(error: Exception) -> str | None:
    print(f"[LOG] CLI-Fehler aufgetreten: {error}")
    return f"Benutzerdefinierter Fehler: {error}"

app = Application(name="demo", error_handler=log_and_format_error)
```

## Wie geht es weiter?

- Definiere benannte Aktionen mit **[Command](./command.md)** und **[Subcommand](./command.md#verschachtelte-subcommands)**.
- Akzeptiere positionale Eingaben mit **[Argument](./argument.md)**.
- Akzeptiere Flags und Optionen mit **[Option](./option.md)**.
- Speichere Einstellungen dauerhaft mit **[Config](./config.md)**.
- Modularisiere deine Anwendung mit **[Plugin](./plugin.md)**.

