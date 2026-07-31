---
sidebar_position: 5
---

# Option

`Option` beschreibt eine benannte Eingabe, die das Verhalten eines Befehls verändert.

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
