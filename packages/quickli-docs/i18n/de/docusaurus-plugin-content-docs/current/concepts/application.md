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

`Application.run()` dispatcht den ausgewählten Befehl und gibt das Handler-Ergebnis
(oder generierten Hilfstext) zurück.

- Er liest `sys.argv[1:]` **standardmäßig**, wenn er ohne Argumente aufgerufen wird.
- Übergib eine explizite Liste zum Überschreiben: `app.run(["greet", "Ada"])`.
- Setze `auto_sys_argv=False` bei der Konstruktion, um stattdessen immer eine leere Liste zu verwenden.
- Er gibt **standardmäßig keine** Ausgabe aus.
- Er wählt **keine** Prozess-Exit-Codes.

`Application.main(argv=None)` ergänzt darüber die Standardhülle für ausführbare Programme.

- Er liest `sys.argv[1:]`, wenn `argv` weggelassen wird.
- Er gibt normale Befehlsresultate aus.
- Er wandelt Laufzeitfehler in strukturierte quickli-Fehler um.
- Er liefert prozessfreundliche Exit-Codes zurück.

Diese Aufteilung hält die Bibliotheksnutzung explizit und gibt ausführbaren Anwendungen
trotzdem eine einfache Standardlaufzeit.

## Registrierungs-API

`Application` bietet Dekorator-APIs für die Befehlsregistrierung:

- `@app.command(...)` für benannte Befehle in einem Multi-Command-CLI
- `@app.entrypoint(...)` für einen befehlslosen Root-Ablauf

Wenn beide existieren, haben Befehlsnamen Vorrang, und der Einstiegspunkt wirkt als
Fallback.
