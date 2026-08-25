# Branch: comments

Comments and docstrings only. Every executable token, identifier, literal,
string and formatting byte leaves this pass unchanged. A rename that "makes a
comment unnecessary" is refactoring and belongs to a different task.

## Machine-read lines stay

Some comment-shaped lines are read by tools, and all of them are kept:

- linter and formatter directives (`# noqa`, `# type: ignore`,
  `// eslint-disable`, `/* prettier-ignore */`, `# fmt: off`, `# isort: skip`)
- interpreter and compiler directives (shebangs, encoding declarations,
  `"use strict"`, `# frozen_string_literal`, coverage pragmas)
- licence and copyright headers the project or its dependencies require
- doc-generator markup on published surfaces (see Docstrings)
- build, IDE and CI annotations (region markers, `// AUTO-GENERATED`,
  source-map hints)

A comment you cannot classify counts as machine-read and stays.

## The keep test

A comment survives when deleting it would lose information that the code,
types, tests and referenced documentation do not already carry, and that
information is one of:

- a concurrency, ordering or lifetime invariant
- a security constraint
- a protocol quirk or documented external-system behavior
- units, boundary conditions or value ranges that are easy to misuse
- the intent of a regex or a non-obvious algorithm
- a framework or runtime constraint that cannot be inferred locally
- why a surprising choice is deliberate ("looks wrong, is right, because…")

Everything else goes:

- restatements of what the code does
- section banners and decorative separators
- implementation history ("previously", "changed to", "now uses")
- commented-out code
- explanations an ADR or README already owns: reference it when the constraint
  is load-bearing, otherwise delete
- thinking-out-loud ("not sure if this is needed", "might be able to simplify")
- TODOs that are done, abandoned or not actionable; a real, current, actionable
  TODO stays

A kept comment is condensed to its minimal present-tense form. The
`TODO(cleanup-audit):` marker is the only text this pass writes.

## Docstrings

- **Published surfaces** (exports, doc-generator input, package manifests, and
  whatever the project's convention names): follow that convention and correct
  factual staleness.
- **Internal and private code**: the keep test above. A docstring that restates
  the signature goes.

What counts as published follows the implementation, not what a docstring
claims about itself.

## Verification

The gate: strip all comments and docstrings from the base branch and from the
cleanup branch (a language-appropriate tool, or an AST comparison), and confirm
the two stripped trees are **identical**. A difference means code moved:
revert it.

Then re-run the baseline, doc builds and docstring-enforcing linters included.
A new failure traced to a deleted machine-read line is fixed by restoring that
line.
