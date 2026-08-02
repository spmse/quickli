---
title: "Getting Started with quiCkLI: Designing CLI Applications"
description: "The challenges, opportunities, and caveats involved in designing a CLI application."
authors: [spmse]
date: 2026-07-31
tags: [getting-started, quickli, cli, design]
keywords: [cli design, python cli, quickli, command-line applications]
---

Designing a CLI is more than mapping strings to functions. You need to decide how users
discover commands, provide values, recover from mistakes, and compose tools in scripts.

{/* truncate */}

quiCkLI makes these decisions explicit: applications own dispatch, commands describe
operations, and arguments and options describe inputs. That simplicity is useful, but it
also means the caller still owns process output and exit codes.

:::note

Treat the boundary between the framework and the executable wrapper as a design decision,
not an implementation detail.

:::
