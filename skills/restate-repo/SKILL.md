---
name: restate-repo
description: Reissue the repository so it states only what is currently true. Deletes stale documentation, dead code and comments that restate the code, and corrects claims the implementation contradicts. `/restate-repo` runs all three passes; `/restate-repo comments` runs the comments pass alone.
disable-model-invocation: true
---

# restate-repo

A **restatement**: the repository reissued so it states only what is currently
true, the way a restatement reissues a published record to correct it. Git
history, closed PRs and closed issues are the **archive**; the working tree
describes what the repository is *now*, and this restatement deletes the rest.

Deletion is the tool. A line is either justified or gone; rewriting is reserved
for condensing a line that earns its place.

## Passes

`/restate-repo` runs all three, in order, one commit each:

1. **Documentation** — docs, READMEs, ADRs, anything the repo says about
   itself. [`DOCS-AND-CODE.md`](DOCS-AND-CODE.md)
2. **Code** — dead code, spent feature flags. Same file.
3. **Comments** — every comment and docstring in the repository.
   [`COMMENTS.md`](COMMENTS.md)

`/restate-repo comments` starts at Pass 3 and stops there. With code out of scope
the diff is small, provable and quick to review; reach for it when a full pass
is more change than you want to take on at once.

When a Pass 2 deletion falsifies a documentation claim Pass 1 kept, correct
that document in the Pass 2 commit.

## Delegation

The session running this skill is the orchestrator: it owns the passes, the
commits, the gates and the summary. Work with a clear rule and a bounded scope
goes to subagents, one per directory or document: verifying a document's claims
against the implementation, applying the keep test to a directory's comments,
grepping deleted symbols for live references. The orchestrator decides what
goes out, whether a subagent edits or only reports, and which model each
subagent runs on. A cheaper model carries rule-checking and searches; a call
that needs judgment (a flag, whether an ADR is still in effect, a deletion that
falsifies a kept claim, every comment in Pass 3) stays on a stronger model or
with the orchestrator. This skill names no provider and no model; use what the
environment offers.

## Guardrails

1. **Behavior stays identical.** The scope is deletion and factual correction.
   The single carve-out is the feature-flag rule in `DOCS-AND-CODE.md`.
2. **The implementation is the source of truth.** A claim is verified against
   what runs: code, configuration, tests, schemas and interfaces, build and CI
   definitions, deployment manifests, runtime wiring. Another document
   corroborates a finding; it never establishes one.
3. **Uncertainty keeps the claim.** A documentation or code claim you cannot
   settle against the implementation stays in place, **flagged**. Comments
   take the opposite default; `COMMENTS.md` states it.
4. **Cleaning is separate from refactoring.** Renames, redesigns,
   reorganisation, new abstractions and bug fixes belong to a different task.
5. **The project's own instructions win.** A `CLAUDE.md`, `AGENTS.md` or
   contributing guide that states a comment, docstring or documentation policy
   overrides anything below it. Read it before the first edit.

Resolve every conflict toward the implementation: keep what it supports, delete
the rest, hedge nothing. When neither side can be verified, keep both and flag
the ambiguity.

## Baseline

Before the first edit, run the repository's tests, linters, type checks and doc
builds. Record the results. **Only failures new against this baseline belong to
the restatement**; pre-existing failures stay untouched.

## Flag

A line you can neither justify nor refute stays where it is, marked in place
with `TODO(cleanup-audit): <what could not be verified>` (or the project's
existing marker convention), and listed in the summary. Existing
`TODO(cleanup-audit):` markers are open flags and survive the pass.

## Out of scope

A pass surfaces problems it does not fix: bugs, unsafe behavior, bad names,
tangled logic, API redesigns, architectural trouble, migration consolidation.
Leave the implementation as it stands and report the location. Unclear code
becomes a follow-up; its comments take the same test as every other.

## Commits

Work on a branch, one commit per pass. Split a commit by directory when its
diff is too large to review in one sitting.

## Verification

Two gates, each tied to a pass, so a comments-only run gets the second exactly
as a full run does.

- **Zero live references** (Passes 1–2): every symbol, file, feature, flag and
  term you deleted greps to zero live references across the repository, and the
  list of what you grepped goes in the summary. Confirm that generated,
  registered, plugin-loaded and convention-discovered components still resolve.
- **Stripped-source identity** (Pass 3): strip all comments and docstrings from
  the commit before Pass 3 and from the Pass 3 commit (a language-appropriate
  tool, or an AST comparison) and confirm the two stripped trees are
  **identical**. A difference means code moved: revert it.

Then re-run the baseline, doc builds and docstring-enforcing linters included.
A new failure means a deletion was wrong: restore what you deleted, rather than
adjusting behavior to fit. A failure traced to a deleted machine-read line is
fixed by restoring that line.

## Summary

Report exactly this, and stop:

- what was deleted or factually corrected, with counts and locations, grouped
  by category
- lines condensed, or redirected to an ADR or doc that already holds the reason
- flags raised (each also marked in place)
- out-of-scope findings and recommended follow-ups
- both gates, and the baseline comparison
