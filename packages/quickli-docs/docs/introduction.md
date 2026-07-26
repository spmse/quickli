---
id: introduction
title: Introduction
sidebar_position: 1
description: Learn why quickli exists and what the framework provides.
---

import { MinimalExample } from '@site/src/components/QuickliExamples';

# Introduction

quiCkLI is an **educational minimal framework lite** for building Python command-line
interfaces. It provides a small set of explicit building blocks without hiding the command
line behind a large abstraction layer.

## Why quickli?

Many CLI frameworks are designed to solve every possible problem. That is useful for large
applications, but it can make the fundamentals difficult to see. quickli takes a smaller
approach so that developers can learn how a CLI is assembled:

- `Application` owns registration and dispatch.
- `Command` represents a named operation.
- `Argument` describes positional input.
- `Option` describes named input and flags.
- Converters and validators turn text into checked values.

The framework is intentionally dependency-light and returns handler results to the caller.
It does not decide how to print output, handle process-level errors, or select exit codes.
Those responsibilities remain visible in the application that uses quickli.

## A small example

The following commandless application accepts a name and returns a greeting:

<MinimalExample />

The next page shows how to install quickli and run a complete example.