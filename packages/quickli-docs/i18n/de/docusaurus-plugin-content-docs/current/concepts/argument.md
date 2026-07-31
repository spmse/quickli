---
sidebar_position: 4
---

# Argument

`Argument` beschreibt einen positionalen Eingabewert für einen Befehl.

## Grundlegendes Verhalten

- Argumente sind positional und geordnet.
- Sie können erforderlich oder optional sein.
- Ein Argument wird optional, sobald es einen Standardwert besitzt.
- Ein Konverter kann Rohtext vor dem Aufruf des Handlers umwandeln.
- Validatoren können konvertierte Werte prüfen.

## Typische Verwendung

Verwende Argumente für den erforderlichen Kontext eines Befehls, zum Beispiel Pfade,
Bezeichner oder Zielnamen:

- Quellpfad
- Ressourcenname
- numerische Eingabe für eine Operation

Fehlen erforderliche Argumente, schlägt die Befehlsausführung mit einem deterministischen
Fehler fehl.
