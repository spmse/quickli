---
title: "quiCkLI entwickeln: KI als Entwicklungspartner"
description: >
  Wie KI-Tools bei der Entwicklung von quiCkLI eingesetzt wurden – was geholfen hat,
  was nicht, und was das für ein Projekt bedeutet, das Transparenz und explizite
  Designentscheidungen wertschätzt.
slug: building-quickli-03-ai-in-development
authors:
  - name: quiCkLI contributors
    url: https://github.com/spmse/quickli
date: 2025-09-15
draft: true
tags: [meta, ki, entwicklung, quickli, open-source]
series:
  name: "quiCkLI entwickeln"
  position: 3
keywords: [quickli, KI-Entwicklung, GitHub Copilot, open source, transparenz]
---

`quiCkLI` wurde mit KI-Unterstützung entwickelt. Ich möchte transparent darüber sein,
was das in der Praxis bedeutet – nicht um es zu feiern oder mich dafür zu entschuldigen,
sondern weil Transparenz über den Prozess in einem Bildungsprojekt wichtig ist.

<!-- truncate -->

## Die Rolle der KI in diesem Projekt

KI-Tools – hauptsächlich GitHub Copilot – wurden während der gesamten Entwicklung von
`quiCkLI` auf verschiedene Arten eingesetzt:

- **Spezifikationen entwerfen.** Die meisten Designdokumente in `specs/` wurden
  kollaborativ mit einem KI-Assistenten geschrieben. Ich lieferte die Designabsicht;
  die KI half, sie in lesbare technische Dokumente zu strukturieren.
- **Tests schreiben.** Viele Unit-Tests wurden von der KI aus dem Spezifikationstext
  oder der Implementierung entworfen. Ich überprüfte und passte jeden Test an, um
  sicherzustellen, dass er das richtige Verhalten testet.
- **Dokumentation.** Die ersten Versionen der Konzeptseiten, Leitfäden und Blogbeiträge
  wurden mit KI-Hilfe entworfen. Alle wurden vor der Veröffentlichung überprüft und
  bearbeitet.
- **Code-Review.** Die KI wies auf potenzielle Probleme in Code-Review-Durchläufen hin,
  die ich als Ausgangspunkt für meine eigene Überprüfung nutzte.

## Was gut funktioniert hat

Für ein kleines, klar abgegrenztes Projekt wie `quiCkLI` beschleunigt KI-Unterstützung
die mechanischen Teile der Arbeit – Boilerplate-Tests schreiben, Dokumente strukturieren,
erste Versionen von Erklärungen entwerfen – ohne die Teile zu ersetzen, die Urteilsvermögen
erfordern.

Die Designentscheidungen in `quiCkLI` – was einzuschließen, was auszuschließen, wo die
Abstraktionsgrenze zu ziehen – wurden von einem Menschen getroffen. Die KI generierte
Text und Code; ich entschied, was korrekt war.

## Was sorgfältige Aufmerksamkeit erforderte

KI-Tools sind selbstsicher, auch wenn sie falsch liegen. Ich stieß auf mehrere Fälle, in
denen:

- Generierter Code kompilierte und lief, aber subtile Verhaltensunterschiede zu dem
  hatte, was ich beabsichtigte.
- Dokumentation flüssig war, aber Verhalten beschrieb, das nicht mit der Implementierung
  übereinstimmte.
- Tests bestanden, aber das Verhalten, das mir wichtig war, nicht tatsächlich
  verifizierten.

In einem lernorientierten Projekt sind diese Probleme besonders wichtig zu erkennen.
Wenn die Dokumentation eine Sache sagt und der Code eine andere tut, lernt der Lernende
die falsche Sache.

Meine Reaktion war, KI-Output als qualitativ hochwertigen ersten Entwurf zu behandeln,
der immer einer Überprüfung bedarf – nicht als fertiges Artefakt.

## Transparenz als Projektwert

`quiCkLI` ist ein Bildungsprojekt. Es schätzt Transparenz – nicht nur im Code, sondern
im Prozess. KI-Unterstützung zu nutzen ist in der Softwareentwicklung zunehmend normal.
Ehrlich darüber zu sein und darüber, was das für die Qualität und Autorenschaft der Arbeit
bedeutet, ist Teil der intellektuellen Redlichkeit des Projekts.

## Als Nächstes

Der letzte Beitrag dieser Reihe befasst sich mit der Zukunft von `quiCkLI` – was geplant
ist, was möglicherweise nicht passiert, und was ich aus dem Prozess gelernt habe.

📖 [Teil 4: Zukunftspläne und Lerneffekte →](/de/blog/building-quickli-04-future-plans)
