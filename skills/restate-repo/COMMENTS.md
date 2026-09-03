# Pass 3: comments

Comments and docstrings across the whole repository. Every executable token,
identifier, literal, string and formatting byte leaves this pass unchanged. A
rename that "makes a comment unnecessary" is refactoring and belongs to a
different task.

## The default is zero

Code is self-explanatory: names, signatures, types and tests carry what it
does. A comment must earn its place; the burden of proof is on the comment,
never on the deletion. Expect to delete most comment lines in a typical
repository; a pass that shortens comments and keeps them has not run this
pass.

## Machine-read lines stay

Some comment-shaped lines are read by tools, and all of them are kept:

- linter and formatter directives (`# noqa`, `# type: ignore`,
  `// eslint-disable`, `// biome-ignore`, `/* prettier-ignore */`, `# fmt: off`)
- interpreter and compiler directives (shebangs, encoding declarations,
  `"use strict"`, PEP 723 script blocks, `// @vitest-environment`, coverage
  pragmas)
- licence and copyright headers the project or its dependencies require
- build, IDE and CI annotations (region markers, `// AUTO-GENERATED`,
  source-map hints)

Machine-read is a closed list: a line is on it because a tool reads it, not
because nobody could classify it.

## What earns its place

A comment survives only when it states one of these, and the code, types,
tests and referenced documentation do not already state it:

- a concurrency, ordering or lifetime invariant
- a security boundary
- a workaround for an upstream bug or a platform quirk, with its reference
- a measured number or a boundary condition behind a constant
- a value that must stay in lockstep with another file, naming that file
- the why behind a choice that looks wrong and is right

Everything else goes. In particular:

- what the code does, what a function returns, what a parameter or field is
- module and file headers that summarise the module, its responsibilities or
  its place in the architecture
- narration of steps inside a body
- section banners and decorative separators
- implementation history, tracker labels, closed issue numbers as history
- explanations a doc, ADR or `CLAUDE.md` already owns: one line naming the
  doc where the constraint is load-bearing, otherwise nothing
- commented-out code, thinking-out-loud, done TODOs

A kept comment is condensed to one or two lines at the spot it guards, present
tense, the constraint and nothing around it. A six-line comment with one
constraint in it becomes one line.

## Docstrings

A docstring is a comment and takes the same test. A function's name and
signature are its documentation; a docstring that describes them goes,
exported or not. A docstring that ends up in a generated artifact (an OpenAPI
description, a doc site) takes the same test, and the artifact is regenerated
after the pass.

A body that is only a docstring keeps a one-line docstring, because replacing
it with `pass` would change the code.

## Tests

A test's name is its documentation. Its docstring goes, and so do step
comments (arrange, act, assert). A test keeps one line only when it pins a
regression whose cause is invisible from the assertion (an upstream bug id, a
race the setup provokes).

## Judgment stays on the strong model

Sorting a comment into "earns its place" or "goes" is judgment, not rule
checking. Dispatch the pass to subagents by directory, and run them on the
strongest model available; a cautious model applying a keep test keeps
everything.

## Review before the commit

After the subagents report, rank the files by remaining comment lines and read
the top ten by hand. Each survivor must name one item from "What earns its
place"; a survivor that describes or narrates goes in this review. A file whose
comment count barely moved was skipped, not judged.

The gate for this pass is stripped-source identity, in `SKILL.md`.
