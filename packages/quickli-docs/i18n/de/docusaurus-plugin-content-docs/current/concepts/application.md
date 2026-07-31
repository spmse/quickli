---
sidebar_position: 2
---

# Application

`Application` ist der Wurzel-CLI-Container in `quickli`.

## Was er verwaltet

- Befehlsregistrierung
- Optionale Root-Einstiegspunkt-Registrierung
- Anwendungsweite globale Optionen
- Befehls-Dispatch aus Eingabe-Token
- Anwendungs- und Befehls-Hilfe-Rendering

## Ausführungsmodell

`Application.run(argv)` akzeptiert explizite Kommandozeilen-Token und gibt das
ausgewählte Handler-Ergebnis (oder generierten Hilfstext) zurück.

- Er liest `sys.argv` **nicht** selbst.
- Er gibt **standardmäßig keine** Ausgabe aus.
- Er wählt **keine** Prozess-Exit-Codes.

Diese Grenze hält das Laufzeitverhalten in deinem ausführbaren Wrapper explizit.

## Registrierungs-API

`Application` bietet Dekorator-APIs für die Befehlsregistrierung:

- `@app.command(...)` für benannte Befehle in einem Multi-Command-CLI
- `@app.entrypoint(...)` für einen befehlslosen Root-Ablauf

Wenn beide existieren, haben Befehlsnamen Vorrang, und der Einstiegspunkt wirkt als
Fallback.
