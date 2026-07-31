---
title: "Building quiCkLI: Why Python, Not Rust or Go?"
description: "Why quiCkLI is built in Python and what Rust and Go would change."
authors: [spmse]
date: 2026-09-08
draft: true
tags: [building-quickli, quickli, python, rust, go]
keywords: [python, rust, go, cli framework, quickli]
---

Python makes the implementation easy to read, experiment with, and connect to the ecosystem
where many automation and operations scripts already live. Rust and Go offer different
trade-offs in startup time, distribution, safety, and deployment.

{/* truncate */}

For an educational framework, readability and iteration are part of the product. That does
not make Python universally best; it makes Python a deliberate fit for this project’s goals.
