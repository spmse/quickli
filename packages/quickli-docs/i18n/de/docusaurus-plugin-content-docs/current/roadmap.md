---
id: roadmap
title: Entwicklungs-Roadmap
sidebar_position: 3
description: Geplante Schritte für die nächsten Entwicklungsphasen von quickli.
---

# Entwicklungs-Roadmap

quickli ist ein Alpha-Projekt. Diese Roadmap beschreibt die nächsten geplanten Schritte,
ohne feste Liefertermine zu versprechen. Jeder Schritt wird implementiert, getestet,
dokumentiert und überprüft, bevor er als abgeschlossen gilt.

## Kurzfristige Prioritäten

1. **Release-Bereitschaft**
   - Versionierung und Release-Artefakte aus dem Release-Tag ableiten.
   - Das Paket unter Python 3.12, 3.13 und 3.14 verifizieren.
   - Dieselben getesteten Distributionen auf PyPI veröffentlichen und Release-Nachweise an GitHub anhängen.
2. **Ausführungsgrenze der Laufzeit**
   - Eine kleine, explizite Hülle für `sys.argv`, Ausgabe, Fehler und Exit-Codes bereitstellen.
   - `Application.run(tokens)` als API auf Bibliotheksebene beibehalten.
3. **Vollständigere Befehlskomposition**
   - Verschachtelte Subcommands und klarere Fehlermeldungen für unbekannte Befehle evaluieren.
   - Die aktuellen kleinen Abstraktionen für Befehle, Argumente und Optionen beibehalten.

## Nachfolgende Prioritäten

- Konfigurationsdateien mit einem expliziten Vorrangmodell
- Shell-Completion aus registrierten Befehlen und Optionen generieren
- Eine bewusste API zum Laden und Registrieren von Plugins
- Kombinierte kurze Schalter, sofern sie hinzugefügt werden können, ohne das Parsen mehrdeutig zu machen

## Auswahl der Prioritäten

Das Projekt bevorzugt Änderungen, die das Lernerlebnis verbessern und den Kern klein halten.
Neues Verhalten sollte eine schriftliche Spezifikation, fokussierte Unit-Tests, ausführbare
Beispiele und eine aktualisierte Dokumentation haben. Geplante Punkte können aufgrund von
Feedback und klarer werdenden Implementierungsrisiken neu geordnet werden.
