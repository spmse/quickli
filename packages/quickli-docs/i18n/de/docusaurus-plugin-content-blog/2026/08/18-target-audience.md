---
title: "quiCkLI entwickeln: Für wen ist dieses Framework?"
description: >
  quiCkLI ist kein Ersatz für produktive CLI-Frameworks. Dieser Beitrag definiert die
  Zielgruppe  -  Entwickler, die verstehen wollen, wie CLI-Tools gebaut werden  -  und
  erklärt, was dieser Fokus für das Design bedeutet.
slug: building-quickli-02-target-audience
authors:
  - spmse
date: 2026-08-18
tags: [building-quickli, meta, target-audience, design, quickli]
series:
  name: "quiCkLI entwickeln"
  position: 2
keywords: [quickli, zielgruppe, lernen, python cli, entwicklerbildung]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

Jede Designentscheidung in `quiCkLI` wurde mit einer bestimmten Art von Entwickler im
Sinn getroffen. In diesem Beitrag möchte ich explizit darüber sprechen, wer das ist,
denn es erklärt Entscheidungen, die sonst willkürlich wirken könnten.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[1]} currentSlug="building-quickli-02-target-audience" />

## Die primäre Zielgruppe

`quiCkLI` ist für Entwickler, die verstehen wollen, wie eine Kommandozeilenanwendung
zusammengesetzt wird  -  nicht nur, wie man eine verwendet.

Diese Gruppe umfasst:

- **Studierende und Berufsanfänger**, die ihre ersten Kommandozeilentools bauen. Sie
  brauchen ein Framework, bei dem die Mechanik sichtbar ist, nicht hinter einer
  polierten Abstraktion verborgen.
- **Entwickler, die aus anderen Sprachen kommen** und den Python-Ansatz zum CLI-Design
  verstehen wollen, ohne den Quellcode eines großen Frameworks lesen zu müssen.
- **Erfahrene Entwickler**, die eine kleine, lesbare Referenzimplementierung als
  Lehrmittel oder Ausgangspunkt für eigene Experimente nutzen möchten.

## Für wen quiCkLI nicht geeignet ist

Wenn du ein produktives CLI-Tool baust und Shell-Vervollständigung, verschachtelte
Unterbefehle, Konfigurationsdateien und einen umfangreichen Hilfe-Renderer benötigst,
verwende `click` oder `typer`. Sie sind ausgezeichnete Tools, die genau für diesen Zweck
entwickelt wurden.

`quiCkLI` trifft bewusste Kompromisse, die in einem produktiven Framework inakzeptabel
wären:

- Es liest `sys.argv` nicht automatisch.
- Es druckt keine Ausgabe und wählt keine Exit-Codes.
- Es bietet keine Shell-Vervollständigung.
- Die Plugin-Erkennung ist manuell.

Das sind keine Versehen. Es sind bewusste Entscheidungen, die die Teile sichtbar halten.

## Was die Zielgruppe braucht

Ein Lernender braucht:

1. **Eine kleine Oberfläche.** Wenn das Framework zwanzig Klassen hat, erfordert das
   Verständnis, alle zwanzig zu kennen. `quickli` hat fünf Kernkonzepte.
2. **Explizite Grenzen.** Wo endet das Framework und wo beginnt die Anwendung? In
   `quickli` ist diese Grenze `Application.run(argv)`.
3. **Ausführbare Beispiele.** Theorie reicht nicht. Die Referenzbeispiele im Repository
   sind echte, ausführbare Tools.

## Was das für das Projekt bedeutet

`quiCkLI` für Lernende nützlich zu halten bedeutet, dem natürlichen Impuls zu
widerstehen, Funktionen hinzuzufügen. Jede Funktion vergrößert die Oberfläche. Jede
Abstraktion verbirgt etwas.

Der Qualitätsmaßstab des Projekts ist nicht nur *funktioniert es*  -  sondern *ist es noch
einfach zu verstehen*.

## Als Nächstes

Der nächste Beitrag untersucht, wie KI-Tools während der Entwicklung eingesetzt wurden
und was diese Erfahrung gelehrt hat.

📖 [Teil 3: KI in der Entwicklung von quiCkLI →](/blog/building-quickli-03-ai-in-development)
