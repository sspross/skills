# Branch: repo

Two passes, one commit each: documentation, then code. When a code deletion in
Pass 2 falsifies a documentation claim Pass 1 kept, correct that document in
the Pass 2 commit.

Resolve every conflict toward the implementation: keep what it supports, delete
the rest, hedge nothing. When neither side can be verified, keep both and flag
the ambiguity.

## Pass 1: documentation

`docs/`, `README.md`, `CONTEXT.md`, `CLAUDE.md`, `AGENTS.md`, ADRs, and
whatever else the repository documents itself with. Verify every factual claim:
keep what the implementation supports, delete what it contradicts, flag what it
cannot settle.

Stale by definition:

- prose changelogs and "we used to…", "as of v2 we now…" language
- notes for migrations that are finished
- TODOs that are done, abandoned or no longer actionable
- descriptions of features that were removed
- setup and deployment instructions that no longer run
- explanations a more authoritative place already owns

### ADRs

An ADR keeps a decision currently in effect, stated in present tense: what we
do, why, and the constraint that makes the obvious alternative wrong. A decision
that is current but worded stale gets the minimal correction that makes it true.

These go: ADRs for decisions no longer in effect, decision journals,
chronological appendices, dated update sections ("Update 2024-03:"), and the
story of how the team arrived here. History earns its place only as a
constraint that still applies and prevents a likely regression.

## Pass 2: code

Delete code you have verified dead:

- unused functions, classes, modules and constants
- superseded versioned duplicates (`my_function_v3` beside `my_function_v4`)
- commented-out blocks
- obsolete compatibility paths
- migration-only code once the migration is finished

"Unused" is a claim about the whole repository. Before it holds, account for
indirect reach: reflection, string-based registration, dynamic imports, plugin
systems, framework conventions, templates, shell invocation, generated code,
configuration-driven entry points, convention-based discovery.

### Framework migrations

Numbered schema and data migrations tracked against database state are the
framework's authoritative record and run on every fresh install. They stay,
unedited, however long the history. Squashing changes behavior and needs
deployment coordination, so it belongs in the summary as a recommended
follow-up.

### Feature flags

The one permitted deviation from "behavior stays identical", in this shape
only: a flag whose value is provably the same in **every** current environment
collapses to that value, and the dead branch goes. A value that differs
anywhere, or that you cannot verify everywhere, keeps the flag and raises a
flag.

Flags serving a current purpose stay: kill switches, staged rollout, customer
entitlements, operational controls, compatibility support.

### Comments

Apply [`COMMENTS.md`](COMMENTS.md) to the code this pass touches.

## Verification

The gate: every symbol, file, feature, flag and term you deleted greps to zero
live references across the repository, and the list of what you grepped goes in
the summary. Confirm that generated, registered, plugin-loaded and
convention-discovered components still resolve.

Then re-run the baseline. A new failure means a deletion was wrong: restore
what you deleted, rather than adjusting behavior to fit.
