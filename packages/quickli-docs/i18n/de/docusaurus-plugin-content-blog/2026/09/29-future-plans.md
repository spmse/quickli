---
title: "quiCkLI entwickeln: Zukunftspläne und Lerneffekte"
description: >
  Der letzte Beitrag der Reihe „quiCkLI entwickeln". Was für das Projekt geplant ist,
  was möglicherweise nicht umgesetzt wird, und was der Entwicklungsprozess über den Bau
  von Bildungssoftware gelehrt hat.
slug: building-quickli-04-future-plans
authors:
  - spmse
date: 2026-09-29
draft: true
tags: [building-quickli, meta, roadmap, lessons-learned, quickli, open-source]
series:
  name: "quiCkLI entwickeln"
  position: 4
keywords: [quickli, roadmap, zukunftspläne, lerneffekte, open source python]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

Dies ist der letzte Beitrag der Reihe *quiCkLI entwickeln*. Ich möchte ehrlich auf das
Bevorstehende für das Projekt blicken und darauf, was ich aus dem Bau gelernt habe.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[1]} currentSlug="building-quickli-04-future-plans" />

## Was geplant ist

Die [Entwicklungs-Roadmap](/docs/roadmap) beschreibt die kurz- und mittelfristigen
Prioritäten im Detail. Das Gesamtbild:

**Kurzfristig:**
- Release-Bereitschaft: konsistente Versionierung, verifizierte Distributionen,
  PyPI-Veröffentlichung.
- Exit-Code-Wrapper  -  `Application.run()` bleibt die Bibliotheks-API, aber ein kleiner,
  optionaler ausführbarer Wrapper für Ausgabe, Fehler und Exit-Codes wird bereitgestellt.
- Bessere Fehler bei unbekannten Befehlen und sauberere Unterbefehl-Komposition.

**Mittelfristig:**
- Konfigurationsdatei-Unterstützung mit einem expliziten Vorrangmodell.
- Shell-Vervollständigung, generiert aus registrierten Befehlen und Optionen.
- Automatische Plugin-Erkennung über `importlib.metadata`-Einstiegspunkte.
- Kombinierte Kurz-Flags, wenn sie ohne mehrdeutiges Parsen hinzugefügt werden können.

## Was möglicherweise nicht passiert

Nicht jedes geplante Element wird umgesetzt. Der Umfang des Projekts ist bewusst schmal.
Wenn eine Funktion Komplexität hinzufügt, ohne das Lernerlebnis zu verbessern, wird sie
verschoben oder fallen gelassen.

## Lerneffekte

### Spezifikations-zuerst-Entwicklung funktioniert

Die Designdokumente vor dem Code zu schreiben, zwang mich, klar darüber nachzudenken,
was ich wollte und warum. Mehrere Funktionen, die ich ursprünglich geplant hatte, wurden
gestrichen, nachdem ich versucht hatte, eine klare Spezifikation für sie zu schreiben,
und es nicht konnte.

### Tests sind Dokumentation

Die Unit-Tests für `quickli` sind explizit, verhaltensbezogen und lesbar. Sie
dokumentieren, was das Framework tatsächlich tut. Wenn ich eine Lücke in den Tests fand,
fand ich eine Lücke in der Spezifikation.

### Kleine Projekte brauchen Wartungsdisziplin

Ein Projekt kann klein sein und trotzdem Schulden anhäufen. Ich fand mehrere Stellen, wo
die Dokumentation ein früheres Design beschrieb oder wo ein Test nicht das testete, was
sein Name vermuten ließ. Die Disziplin, Implementierung, Tests und Dokumentation
aufeinander abgestimmt zu halten, ist schwieriger als jedes einzeln zu schreiben.

### KI-Tools sind in der Mitte am nützlichsten

KI-Unterstützung war am nützlichsten in der Mitte einer Aufgabe  -  nachdem die
Designabsicht klar war und vor dem abschließenden Überprüfungsdurchgang.

## Abschließender Gedanke

`quiCkLI` existiert, weil ich ein CLI-Framework wollte, das lesbar genug ist, um davon
zu lernen. Ob es dieses Ziel erreicht, bleibt letztendlich den Nutzern zu beurteilen.
Wenn du davon lernst oder es als Ausgangspunkt für deine eigenen Experimente nutzt, würde
ich mich über Feedback freuen.

Der Quellcode befindet sich unter [github.com/spmse/quickli](https://github.com/spmse/quickli).
Rückmeldungen, Fragen und Beiträge sind willkommen.
