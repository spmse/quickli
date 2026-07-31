---
title: "Building quiCkLI: Why I Started a Minimal CLI Framework"
description: >
  Why build another CLI framework? This first post in the Building quiCkLI series
  explores the motivation behind the project, what problem it solves for learners, and
  the design principles that guide every decision.
slug: building-quickli-01-motivation
authors:
  - spmse
date: 2026-08-06
tags: [building-quickli, meta, motivation, design, quickli, open-source]
series:
  name: "Building quiCkLI"
  position: 1
keywords: [quickli, open source, python cli framework, motivation, design philosophy]
---

import BlogSeriesNavigation from '@site/src/components/BlogSeriesNavigation';
import { blogSeries } from '@site/src/data/blogSeries';

There are already excellent Python CLI frameworks. `argparse` is in the standard library.
`click` is polished and widely used. `typer` generates interfaces from type annotations.
If these exist, why build another one?

This post answers that question honestly. It is the first in a series about the
development of `quiCkLI`  -  what it is, why it exists, and where it is going.

{/* truncate */}

<BlogSeriesNavigation series={blogSeries[1]} currentSlug="building-quickli-01-motivation" />

## The gap I wanted to fill

I wanted a framework I could point a learner at and say: *all the important parts are
visible here*. When I tried to explain how a CLI application works using an existing
framework, I kept running into the same problem. The framework was good at hiding
complexity  -  which is great for production code  -  but that same hiding made it hard to
understand what was actually happening.

`click`, for example, uses a layered decorator model that works beautifully in practice
but abstracts away how arguments are collected, how defaults are resolved, and how
subcommands are dispatched. That abstraction is valuable. It is also precisely what makes
it hard to learn from.

I did not want to replace any of these tools. I wanted to build something that could serve
as a reference implementation  -  a framework small enough that a developer could read the
entire source in an afternoon and understand how a CLI is assembled from first principles.

## What "minimal" means here

`quickli` is not minimal because it has fewer features. It is minimal in the sense that
every part of the design is deliberate and visible.

- The application container owns registration and dispatch. That boundary is explicit.
- Arguments are positional and ordered. Options are named. Those are different things.
- Conversion and validation are separate steps, and they happen before the handler runs.
- The framework returns results to the caller. It does not print output, handle exit
  codes, or read `sys.argv` automatically.

Each of these decisions was made because it keeps the mechanics of a CLI visible to
someone learning how they work.

## The guiding question

For every feature I considered adding to `quickli`, I asked the same question: *does this
make the framework easier to learn from, or does it make it more powerful at the cost of
making it harder to understand?*

That question has kept `quickli` small. It has also forced me to be explicit about what
the framework is not trying to do.

## What comes next

The next post in this series looks at who `quiCkLI` is for  -  the target audience, and
what I am hoping they get out of using it.

📖 [Part 2: Who Is quiCkLI For? →](/blog/building-quickli-02-target-audience)
