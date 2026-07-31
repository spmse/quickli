---
title: "Single-Purpose CLIs vs Multi-Command Applications"
description: "When to build focused tools like ls and mkdir, and when to build applications like git or kubectl."
authors: [spmse]
date: 2026-10-01
draft: true
tags: [general, quickli, cli, architecture]
keywords: [single purpose cli, multi command cli, git, kubectl, docker, terraform]
---

`ls`, `mkdir`, and `chown` each do one job and compose naturally through the shell. `git`,
`kubectl`, `docker`, and `terraform` provide a shared vocabulary across many related
operations.

{/* truncate */}

The choice affects discoverability, completion, configuration, help output, release shape,
and how users compose automation. quiCkLI supports both styles so the application structure
can follow the problem rather than a framework fashion.

:::tip

Start with a single-purpose command when the domain is narrow. Introduce subcommands when
shared concepts, options, and lifecycle justify a common application surface.

:::
