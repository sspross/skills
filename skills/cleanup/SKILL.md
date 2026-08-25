---
name: cleanup
description: Delete what the repository no longer needs. Two branches, picked by argument: `/cleanup comments` (comments and docstrings only, code untouched) and `/cleanup repo` (documentation, ADRs, dead code, spent feature flags).
disable-model-invocation: true
---

# cleanup

Git history, closed PRs and closed issues are the **archive**. The working tree
describes what the repository is *now*. This skill deletes the rest.

Deletion is the tool. A line is either justified or gone; rewriting is reserved
for condensing a line that earns its place.

## Branch

The argument picks one. Read that file, follow it, and apply this file's process
to it. With no argument, ask which branch.

| argument | scope | file |
| --- | --- | --- |
| `comments` | comments and docstrings, in every language; executable tokens stay byte-identical | [`COMMENTS.md`](COMMENTS.md) |
| `repo` | documentation, ADRs, dead code, spent feature flags | [`REPO.md`](REPO.md) |

## Guardrails

Both branches hold these.

1. **Behavior stays identical.** The scope is deletion and factual correction.
   The single carve-out is the feature-flag rule in `REPO.md`.
2. **The implementation is the source of truth.** A claim is verified against
   what runs: code, configuration, tests, schemas and interfaces, build and CI
   definitions, deployment manifests, runtime wiring. Another document
   corroborates a finding; it never establishes one.
3. **Uncertainty keeps the line.** Investigate against the implementation
   first. Still unresolved: leave it in place and **flag** it.
4. **Cleaning is separate from refactoring.** Renames, redesigns,
   reorganisation, new abstractions and bug fixes belong to a different task.
5. **The project's own instructions win.** A `CLAUDE.md`, `AGENTS.md` or
   contributing guide that states a comment, docstring or documentation policy
   overrides anything below it. Read it before the first edit.

## Baseline

Before the first edit, run the repository's tests, linters, type checks and doc
builds. Record the results. **Only failures new against this baseline belong to
the cleanup**; pre-existing failures stay untouched.

## Flag

A line you can neither justify nor refute stays where it is, marked in place
with `TODO(cleanup-audit): <what could not be verified>` (or the project's
existing marker convention), and listed in the summary. Existing
`TODO(cleanup-audit):` markers are open flags and survive the pass.

## Out of scope

A pass surfaces problems it does not fix: bugs, unsafe behavior, bad names,
tangled logic, API redesigns, architectural trouble, migration consolidation.
Leave the implementation as it stands and report the location. A comment that
is only necessary because the code is unclear stays, and the code becomes a
follow-up.

## Commits

Work on a branch, one commit per pass. Split a commit by directory when its
diff is too large to review in one sitting.

## Summary

Report exactly this, and stop:

- what was deleted or factually corrected, with counts and locations, grouped
  by category
- lines condensed, or redirected to an ADR or doc that already holds the reason
- flags raised (each also marked in place)
- out-of-scope findings and recommended follow-ups
- the verification the branch demanded, and the baseline comparison
