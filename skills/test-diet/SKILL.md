---
name: test-diet
description: Put a project's test suite on a diet - profile it, prune low-value tests, consolidate unit tests into integration tests, trim e2e to golden journeys. One run, one PR.
disable-model-invocation: true
---

Reduce the suite's runtime while the core stays tested. Integration-first: a test earns its place by exercising a real flow through real seams. Muscle stays, fat goes. Each run walks the whole suite and converges: stateless, idempotent, safe to repeat.

Work on a fresh branch. The suite is green after every commit, and runtime is remeasured after every stage.

## 1. Discover

Map the landscape: every test entry point (make targets, package scripts, CI), the test directories per kind (unit, integration, e2e), and the coverage tooling. Coverage missing: set it up config-level (`coverage.py`, `vitest --coverage`). Setup fails: declare **judgment-only mode** for that suite, meaning every deletion candidate goes to the borderline checklist and nothing is auto-deleted.

Derive **the core**, the flows that must stay tested, from project docs (CONTEXT.md, README architecture, CLAUDE.md). No such docs: write your assumed core flows into the PR body for the user to veto.

Done when: every entry point named, coverage measurable or judgment-only declared per suite, core flows listed.

## 2. Profile (commit 1)

Run the full suite instrumented: per-test durations (`--durations`, reporter timings), total wall time, coverage baseline. Rank test files by cost (runtime x count). This ranking orders all later work; the baseline numbers open the PR body.

Commit whatever the instrumentation added (coverage config). Done when: every suite ran, timings and baseline captured.

## 3. Quick wins (commit 2)

Apply the config-level speedups the profile exposes: build prerequisites no test needs, tracing or video armed for whole runs, missing parallelization, per-test setup that can be per-session. Config-level only (flags, prereqs, fixture scope); the build system keeps its shape.

Done when: every profile-exposed overhead is applied or rejected with a reason in the report, suite green, runtime remeasured.

## 4. Prune (commit 3)

Judge every test against the value criteria below. Deletions split in two:

- **Hard-criteria**: subsumed or tautological, and the coverage diff after deletion shows zero loss. Delete now.
- **Borderline**: everything needing judgment. Goes to the checklist in the PR body with a one-line rationale each, code untouched.

Delete only green tests. A flaky test is a diet item of its own (cost without signal): fix it when the cause is shallow (timing, ordering); otherwise borderline, marked *flaky* with the observed failure.

Done when: every test in the suite is accounted for as kept, deleted, consolidated (next stage), or borderline.

## 5. Consolidate (commit 4)

Implementation-coupled unit tests hold their value hostage: the behavior matters, but the test breaks on refactors instead of bugs. Free it: write one integration test driving the same behavior through the real flow, then delete the unit tests it replaces. Replacement and deletions land in the same commit, coverage diff showing no loss.

Done when: no implementation-coupled cluster remains without its replacement.

## 6. Golden journeys (commit 5)

Reshape e2e into a few long journeys, each traversing many features in one browser session. An e2e test exists only for what no lower layer can reach: real rendering, focus, viewport, static serving. Everything else it asserts moves down a layer or goes.

Run every e2e test you touch. No browser in this environment: e2e changes become proposal-only checklist items instead of commits.

Done when: each journey green, each surviving e2e test justified by a browser-only behavior.

## 7. Deliver

Open one PR. Body: runtime before and after per stage, per-commit summary, deletion rationale, the borderline checklist, assumed core flows (if drafted), and structural follow-ups the run stayed out of (test tiers, build-system reshaping). Follow-up happens as normal PR comments on this branch.

## Value criteria

A test earns its place by exercising a core flow or a real seam. Against that bar:

- **Subsumed**: every behavior it checks is also exercised by a surviving broader test. Delete.
- **Implementation-coupled**: asserts private structure (internal calls, mock interactions, call order). Consolidate (stage 5).
- **Tautological**: re-asserts the framework, trivial getters, constants. Delete.
- **Pin**: a doc names it as enforcing an invariant ("enforced by a test"), or it guards a documented domain rule. Keep, always: a pin is muscle whatever it looks like.
