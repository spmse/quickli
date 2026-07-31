---
title: "Building quiCkLI: Future Plans and Lessons Learned"
description: >
  The final post in the Building quiCkLI series. What is planned for the project,
  what might not happen, and what the development process has taught about building
  educational software.
slug: building-quickli-04-future-plans
authors:
  - name: quiCkLI contributors
    url: https://github.com/spmse/quickli
date: 2025-09-22
draft: true
tags: [meta, roadmap, lessons-learned, quickli, open-source]
series:
  name: "Building quiCkLI"
  position: 4
keywords: [quickli, roadmap, future plans, lessons learned, open source python]
---

This is the final post in the *Building quiCkLI* series. I want to look honestly at what
is ahead for the project and what I have learned from building it.

<!-- truncate -->

## What is planned

The [development roadmap](/docs/roadmap) describes the near-term and following priorities
in detail. The high-level picture:

**Near term:**
- Release readiness: consistent versioning, verified distributions, PyPI publication.
- Explicit `sys.argv` / exit code wrapper — keeping `Application.run(tokens)` as the
  library API, but providing a small, optional executable wrapper.
- Better unknown-command errors and cleaner subcommand composition.

**Following:**
- Configuration file support with an explicit precedence model.
- Shell completion generated from registered commands and options.
- Automatic plugin discovery via `importlib.metadata` entry points.
- Combined short flags, if they can be added without making parsing ambiguous.

## What might not happen

Not every planned item will be implemented. The project's scope is intentionally narrow.
If a feature adds complexity without improving the learning experience, it will be
deferred or dropped.

The items most at risk are the ones that require significant parser changes — combined
short flags and nested subcommands. Both are feasible, but both risk making the
framework harder to understand. I will implement them only if I can do so without
obscuring the core mechanics.

## Lessons learned

### Specification-first development works

Writing the design documents before the code forced me to think clearly about what I
wanted and why. Several features I originally planned were dropped after I tried to
write a clear specification for them and could not.

### Tests are documentation

The unit tests for `quickli` are explicit, behavioral, and readable. They document what
the framework actually does. When I found a gap in the tests, I found a gap in the
specification.

### Small projects need maintenance discipline

A project can be small and still accumulate debt. I found several places where the
documentation described a previous design, or where a test was not testing what its name
suggested. The discipline of keeping implementation, tests, and documentation aligned is
harder than writing any of them individually.

### AI tools are fastest in the middle

AI assistance was most useful in the middle of a task — once the design intent was clear,
and before the final review pass. It was least useful at the beginning (when I needed to
think carefully about what I was building) and at the end (when I needed to verify that
the output was correct).

## Closing thought

`quiCkLI` exists because I wanted a CLI framework that was readable enough to learn from.
Whether it achieves that goal is ultimately for its users to judge. If you are learning
from it, or using it as a starting point for your own experiments, I would be glad to
hear what you find.

The source is at [github.com/spmse/quickli](https://github.com/spmse/quickli). Feedback,
questions, and contributions are welcome.
