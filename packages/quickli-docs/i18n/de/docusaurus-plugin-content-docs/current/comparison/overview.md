---
sidebar_position: 1
description: Überblick über den Vergleich von Click, argparse und quickli mit kleinen CLI-Beispielen für einzelne Aufgaben.
keywords: [quickli, click, argparse, vergleich, cli framework, beispiele]
---

# Vergleichsübersicht

Dieser Abschnitt vergleicht, wie die drei Ansätze kleine, einheitlich aufgebaute Befehlszeilen-Tools
wie `head`, `tail`, `cat`, `ls`, `mkdir`, `rm`, `rmdir` und `cut` behandeln.

Die Beispiele sind bewusst klein gehalten, damit die Unterschiede in der Code-Struktur sichtbar
bleiben und nicht hinter Framework-Komplexität verschwinden.

## Was dieser Vergleich fokussiert

- wie viel Code nötig ist, um dieselbe kleine CLI auszudrücken
- wie viel Setup nötig ist, bevor das Tool nutzbar ist
- wie leicht sich die Implementation lesbar und wartbar halten lässt
- wie natürlich mehrere kleine Werkzeuge später zu einer größeren CLI zusammengeführt werden können

## Kurz gesagt

- `argparse` ist die leichteste Option für sehr kleine Werkzeuge und hält die Implementierung nah
  an der Standardbibliothek.
- `click` ist die ergonomischste Wahl, wenn du eine polierte CLI-Erfahrung und einen glatteren Weg
  zu einer größeren Befehlsstruktur willst.
- `quickli` bietet eine klare, explizite Architektur, die noch leicht genug für kleine Werkzeuge
  ist und dir einen praktischen Weg bietet, von einem einfachen Skript zu einer strukturierteren
  Anwendung zu wachsen.

## Beispiel-Implementierungen

Die Beispiel-Quellen liegen im gemeinsamen Beispiele-Ordner des Repositories:

- [quickli-Beispiel](https://github.com/spmse/quickli/tree/main/packages/core/examples/comparison/quickli_example.py)
- [argparse-Beispiel](https://github.com/spmse/quickli/tree/main/packages/core/examples/comparison/argparse_example.py)
- [click-Beispiel](https://github.com/spmse/quickli/tree/main/packages/core/examples/comparison/click_example.py)

## Entwicklererfahrung und Wartbarkeit

Die drei Ansätze unterscheiden sich auch darin, wie sie sich über die Zeit anfühlen. Ein kleines
Skript mag mit jedem von ihnen gut funktionieren, aber die Unterschiede werden sichtbar, sobald die
CLI wächst oder mehrere Personen an ihr arbeiten.

| Aspekt | argparse | click | quickli |
| --- | --- | --- | --- |
| Anfangsgeschwindigkeit | Sehr schnell für kleine Skripte, weil es direkt die Standardbibliothek nutzt. | Schnell, sobald das Decorator-Muster vertraut ist. | Etwas strukturierter zu Beginn, aber das App-Modell bleibt leicht verständlich. |
| Lesbarkeit | Nah an reinem Python und leicht verständlich, aber bei größeren Befehlsbäumen repetitiv. | Kurz und deklarativ; Befehle und Optionen bleiben gut lesbar. | Explizit und architektonisch; die Trennung zwischen Anwendung, Befehlen und Optionen ist klar. |
| Wartbarkeit | Gut für ein einzelnes Skript, aber die manuelle Organisation wird bei wachsender Funktionalität schnell unübersichtlich. | Stark für befehlsorientierte CLIs, weil das Verhalten organisiert und auffindbar bleibt. | Stark, wenn du von Anfang an ein klares internes Modell willst und die CLI weiterentwickeln möchtest. |
| Entwickler-Ergonomie | Minimal, aber du schreibst oft mehr Glue-Code selbst. | Hervorragende Hilfsausgaben, Fehlerfälle und CLI-Konventionen direkt mit dabei. | Gute Balance zwischen expliziter Struktur und leichter Implementierung. |

In der Praxis ist `argparse` oft die einfachste Wahl, wenn du die kleinste mögliche Abhängigkeitsfläche
wolltest und das Problem klein bleibt. `click` bietet meist die beste Alltags-Erfahrung für
Maintainer und Nutzer. `quickli` ist eine starke Wahl, wenn du möchtest, dass der Code klar und
strukturiert bleibt, ohne übermäßig framework-lastig zu wirken.

## Lernkurve für Anfänger

Wenn du neu in der Programmierung, in Python oder in der CLI-Entwicklung bist, ist die beste Wahl
oft diejenige, die zu deinem derzeitigen Vertrauen und deinen langfristigen Zielen passt.

- `argparse` ist der zugänglichste Einstieg, wenn du die Grundlagen des Parsens von Argumenten
  lernen willst, ohne eine weitere Abstraktionsebene einzuführen. Es ist auch eine gute Wahl,
  wenn du verstehen willst, wie eine CLI direkt aus der Standardbibliothek aufgebaut wird.
- `click` ist oft leichter für Anfänger, sobald sie die Grundlagen von Python-Funktionen und
  Decorators verstanden haben, weil es eine polierte CLI-Erfahrung mit weniger Boilerplate bietet.
  Es ist besonders hilfreich, wenn du lernen willst, wie befehlsorientierte Anwendungen aufgebaut
  werden, ohne jedes Detail selbst zusammenzuschrauben.
- `quickli` ist eine gute Wahl, wenn du nicht nur lernen willst, wie man Argumente parst, sondern
  auch, wie man eine kleine Anwendung um Befehle, Optionen und eine klarere Gesamtarchitektur
  herum strukturiert. Es passt besonders gut zu Lernenden, die sich Gewohnheiten aneignen wollen,
  die über ein einzelnes Skript hinaus skalieren.

Für jemanden, der gerade erst anfängt, ist `argparse` oft der sanfteste erste Schritt. Für jemanden,
der die Grundlagen schon verstanden hat und eine poliertere und wartbarere CLI-Erfahrung will,
können `click` oder `quickli` als lohnender erscheinen, wenn das Projekt wächst.

## Migration und Integrationsaufwand

Wenn du von mehreren kleinen, einzelfokussierten CLIs ausgehst, hängt die Migrationskosten weniger
von der einzelnen Parser-Bibliothek ab als davon, wie viel Struktur du erhalten willst.

- Eine Menge `argparse`-basierter Werkzeuge kann zu einem übergeordneten Parser zusammengeführt
  werden, aber die Integrationsarbeit ist meist manuell und individuell.
- Ein Satz `click`-basierter Werkzeuge lässt sich natürlicher zu einer einzigen Befehlsgruppe
  zusammenfassen, besonders wenn die Werkzeuge bereits eine klare befehlsorientierte Struktur
  haben.
- Ein `quickli`-basierter Satz lässt sich konzeptionell besonders gut zusammensetzen, weil die
  Anwendungsstruktur und die Befehlsgrenzen explizit sind und der Übergang zu einer gemeinsamen
  Anwendung daher bewusst statt improvisiert wirkt.

In der Praxis ist der leichteste Migrationsweg meist der, der bereits zur Ziel-Form der finalen CLI
passt. Wenn du einen einzelnen, polierten Einstiegspunkt mit mehreren Unterbefehlen willst, ist
`click` oft die beste Wahl. Wenn du eine einfache, explizite und gut weiterentwickelbare Anwendung
willst, ist `quickli` oft die sinnvollste Lösung.
