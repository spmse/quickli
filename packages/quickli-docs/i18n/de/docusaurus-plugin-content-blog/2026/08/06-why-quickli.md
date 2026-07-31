---
title: "quiCkLI entwickeln: Warum ich ein minimales CLI-Framework gebaut habe"
description: >
  Warum noch ein weiteres CLI-Framework? Dieser erste Beitrag der Reihe „quiCkLI
  entwickeln" erklärt die Motivation hinter dem Projekt, welches Problem es für Lernende
  löst und welche Designprinzipien jede Entscheidung leiten.
slug: building-quickli-01-motivation
authors:
  - spmse
date: 2026-08-06
draft: true
tags: [building-quickli, meta, motivation, design, quickli, open-source]
series:
  name: "quiCkLI entwickeln"
  position: 1
keywords: [quickli, open source, python cli framework, motivation, designphilosophie]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

Es gibt bereits ausgezeichnete Python-CLI-Frameworks. `argparse` ist in der
Standardbibliothek. `click` ist ausgereift und weit verbreitet. `typer` generiert
Interfaces aus Typ-Annotationen. Wenn diese existieren, warum dann noch eines bauen?

Dieser Beitrag beantwortet diese Frage ehrlich. Er ist der erste einer Reihe über die
Entwicklung von `quiCkLI`  -  was es ist, warum es existiert und wohin es geht.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[1]} currentSlug="building-quickli-01-motivation" />

## Die Lücke, die ich füllen wollte

Ich wollte ein Framework, auf das ich einen Lernenden zeigen und sagen könnte: *Alle
wichtigen Teile sind hier sichtbar.* Wenn ich versuchte, mit einem bestehenden Framework
zu erklären, wie eine CLI-Anwendung funktioniert, stieß ich immer wieder auf dasselbe
Problem. Das Framework war gut darin, Komplexität zu verbergen  -  was für Produktionscode
großartig ist  -  aber genau dieses Verbergen machte es schwer zu verstehen, was tatsächlich
passiert.

Ich wollte keines dieser Tools ersetzen. Ich wollte etwas bauen, das als
Referenzimplementierung dienen kann  -  ein Framework, das klein genug ist, dass ein
Entwickler den gesamten Quellcode an einem Nachmittag lesen und verstehen kann, wie ein
CLI aus ersten Prinzipien zusammengesetzt wird.

## Was „minimal" hier bedeutet

`quickli` ist nicht minimal, weil es weniger Funktionen hat. Es ist minimal in dem Sinn,
dass jeder Teil des Designs bewusst und sichtbar ist.

- Der Anwendungs-Container verwaltet Registrierung und Dispatch. Diese Grenze ist explizit.
- Argumente sind positional und geordnet. Optionen sind benannt. Das sind verschiedene
  Dinge.
- Konvertierung und Validierung sind separate Schritte, die vor dem Handler stattfinden.
- Das Framework gibt Ergebnisse an den Aufrufer zurück. Es druckt keine Ausgabe,
  behandelt keine Exit-Codes und liest `sys.argv` nicht automatisch.

Jede dieser Entscheidungen wurde getroffen, weil sie die Mechanik einer CLI für jemanden
sichtbar lässt, der lernt, wie sie funktioniert.

## Die leitende Frage

Für jede Funktion, die ich in `quickli` hinzuzufügen überlegte, stellte ich dieselbe
Frage: *Macht das das Framework einfacher, davon zu lernen, oder macht es es mächtiger
auf Kosten des Verständnisses?*

Diese Frage hat `quickli` klein gehalten.

## Was als Nächstes kommt

Der nächste Beitrag in dieser Reihe befasst sich damit, für wen `quiCkLI` gedacht ist  -
die Zielgruppe und was ich hoffe, dass sie aus der Verwendung mitnehmen.

📖 [Teil 2: Für wen ist quiCkLI? →](/de/blog/building-quickli-02-target-audience)
