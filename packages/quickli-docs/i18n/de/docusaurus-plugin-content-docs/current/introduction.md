---
id: introduction
title: Einleitung
sidebar_position: 1
description: Lerne, warum quickli existiert und was das Framework bereitstellt.
keywords: [quickli, python cli, kommandozeilen-framework, einleitung, lernframework]
---

import { MinimalExample } from '@site/src/components/QuickliExamples';

# Einleitung

quiCkLI ist ein **minimales Lern-Framework** für den Aufbau von Python-Kommandozeilen-
Interfaces. Es stellt eine kleine Menge expliziter Bausteine bereit, ohne die Kommandozeile
hinter einer großen Abstraktionsschicht zu verbergen.

## Warum quickli?

Viele CLI-Frameworks sind darauf ausgelegt, jedes mögliche Problem zu lösen. Das ist für
große Anwendungen nützlich, kann aber die Grundlagen schwer erkennbar machen. quickli
verfolgt einen kleineren Ansatz, damit Entwickler lernen können, wie ein CLI zusammengesetzt
wird:

- `Application` verwaltet Registrierung und Dispatch.
- `Command` repräsentiert eine benannte Operation.
- `Argument` beschreibt positionalen Input.
- `Option` beschreibt benannten Input und Schalter.
- Konverter und Validatoren wandeln Text in geprüfte Werte um.

Das Framework ist bewusst abhängigkeitsarm und hält die Bibliotheksgrenze sichtbar.
`Application.run()` gibt weiterhin Handler-Ergebnisse an den Aufrufer zurück, während
`Application.main()` eine Standardhülle für `sys.argv`, Ausgabe, strukturierte
Laufzeitfehler und Exit-Codes bereitstellt.

## Ein kleines Beispiel

Die folgende befehlslose Anwendung akzeptiert JSON- oder YAML-Text und normalisiert ihn
zu JSON:

<MinimalExample />

Die nächste Seite zeigt, wie quickli installiert und ein vollständiges Beispiel
ausgeführt wird.

## Nächste Schritte

Lies die [quiCkLI-Konzepte](./concepts/quickli-concepts.md), um zu verstehen,
wie `Application`, `Command`, `Argument`, `Option` und `Plugin` zusammenwirken.

Die [Entwicklungs-Roadmap](./roadmap.md) beschreibt die nächsten geplanten Schritte.
