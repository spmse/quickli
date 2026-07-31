---
title: "Building quiCkLI: Using AI as a Development Partner"
description: >
  How AI tools were used during the development of quiCkLI — what helped, what didn't,
  and what it means for a project that values transparency and explicit design decisions.
slug: building-quickli-03-ai-in-development
authors:
  - name: quiCkLI contributors
    url: https://github.com/spmse/quickli
date: 2025-09-15
draft: true
tags: [meta, ai, development, quickli, open-source]
series:
  name: "Building quiCkLI"
  position: 3
keywords: [quickli, AI development, GitHub Copilot, open source, transparency]
---

`quiCkLI` was built with AI assistance. I want to be transparent about what that means
in practice — not to celebrate it or apologize for it, but because transparency about
process matters in an educational project.

<!-- truncate -->

## The role of AI in this project

AI tools — primarily GitHub Copilot — were used throughout the development of `quiCkLI`
in several ways:

- **Drafting specifications.** Most of the design documents in `specs/` were written
  collaboratively with an AI assistant. I provided the design intent; the AI helped
  structure it into readable technical documents.
- **Writing tests.** Many unit tests were drafted by the AI from the specification text
  or from the implementation. I reviewed and adjusted each test to make sure it tested
  the right behavior.
- **Documentation.** The initial versions of concept pages, guides, and blog posts were
  drafted with AI help. All of them were reviewed and edited before being published.
- **Code review.** The AI flagged potential issues in code review passes that I used as
  a starting point for my own review.

## What worked well

For a small, well-scoped project like `quiCkLI`, AI assistance accelerates the mechanical
parts of the work — writing boilerplate tests, structuring documents, drafting first
versions of explanations — without replacing the parts that require judgment.

The design decisions in `quiCkLI` — what to include, what to exclude, where to draw the
abstraction boundary — were made by a human. The AI generated text and code; I decided
what was correct.

## What required careful attention

AI tools are confident even when they are wrong. I encountered several cases where:

- Generated code compiled and ran but had subtle behavioral differences from what I
  intended.
- Documentation was fluent but described behavior that did not match the implementation.
- Tests passed but did not actually verify the behavior I cared about.

In a learning-focused project, these problems are especially important to catch. If the
documentation says one thing and the code does another, the learner learns the wrong
thing.

My response was to treat AI output as a high-quality first draft that always required
review, not as a finished artifact.

## Transparency as a project value

`quiCkLI` is an educational project. It values transparency — not just in the code, but
in the process. Using AI assistance is increasingly normal in software development. Being
honest about it, and about what that means for the quality and authorship of the work, is
part of the project's intellectual honesty.

If you are using `quiCkLI` as a learning tool, the same principle applies: understand
what the tools you use are doing, not just that they work.

## Next

The final post in this series looks at the future of `quiCkLI` — what is planned, what
might not happen, and what I have learned from the process so far.

📖 [Part 4: Future Plans and Lessons Learned →](/blog/building-quickli-04-future-plans)
