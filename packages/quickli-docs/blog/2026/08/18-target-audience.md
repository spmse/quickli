---
title: "Building quiCkLI: Who Is This Framework For?"
description: >
  quiCkLI is not a replacement for production CLI frameworks. This post defines the
  target audience  -  developers who want to understand how CLI tools are built  -  and
  explains what that focus means for the design.
slug: building-quickli-02-target-audience
authors:
  - spmse
date: 2026-07-31
tags: [building-quickli, meta, target-audience, design, quickli]
series:
  name: "Building quiCkLI"
  position: 2
keywords: [quickli, target audience, learning, python cli, developer education]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

Every design decision in `quiCkLI` was made with a specific kind of developer in mind. In
this post I want to be explicit about who that is, because it explains decisions that
might otherwise seem arbitrary.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[1]} currentSlug="building-quickli-02-target-audience" />

## The primary audience

`quiCkLI` is for developers who want to understand how a command-line application is
assembled  -  not just use one.

That group includes:

- **Students and early-career developers** building their first command-line tools. They
  need a framework where the mechanics are visible, not hidden behind a polished
  abstraction.
- **Developers coming from other languages** who want to understand the Python approach
  to CLI design without reading the source of a large framework.
- **Experienced developers** who want a small, readable reference implementation to use
  as a teaching aid or a starting point for their own experiments.

## Who quiCkLI is not for

If you are building a production CLI tool and you need shell completion, nested
subcommands, configuration files, and a rich help renderer, use `click` or `typer`. They
are excellent tools built for exactly that purpose.

`quiCkLI` makes explicit tradeoffs that would be unacceptable in a production framework:

- It reads `sys.argv[1:]` by default, but lets you opt out with `auto_sys_argv=False`.
- It does not print output or choose exit codes.
- It does not provide shell completion.
- Its plugin discovery is manual.

These are not oversights. They are deliberate choices that keep the parts visible.

## What the target audience needs

A learner needs:

1. **A small surface area.** If the framework has twenty classes, understanding it
   requires understanding all twenty. `quickli` has five core concepts. You can hold the
   whole model in your head.
2. **Explicit boundaries.** Where does the framework end and the application begin? In
   `quickli`, that boundary is `Application.run()`. The application receives a result back.
   Everything that happens to process exit codes and output formatting is the
   application's responsibility.
3. **Runnable examples.** Theory is not enough. The reference examples in the repository
   are real, runnable tools that demonstrate each concept in context.

## What this means for the project

Keeping `quiCkLI` useful for learners means resisting the natural impulse to add
features. Every feature adds surface area. Every abstraction hides something.

The project's quality bar is not just *does it work*  -  it is *is it still easy to
understand*. That is a harder standard to maintain, and it is the one that matters most
for this audience.

