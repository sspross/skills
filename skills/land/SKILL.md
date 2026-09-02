---
name: land
description: Take approved tickets to one reviewable pull request. `/land` dispatches agents across the ticket frontier, a PR per ticket onto an integration branch, then one spec PR for review; `/land pr <number>` dispatches agents to address the review comments on it. The run is unattended; it orchestrates only, never writes the code itself.
argument-hint: "a spec issue, ticket numbers, or `pr <number>`"
disable-model-invocation: true
---

# land

Tickets in, one reviewable pull request out. You are the **orchestrator**: you
dispatch agents that write the code, you merge what they land, and you keep
dispatching until every ticket is accounted for. The implementation is theirs to
write.

## Unattended

From the invocation to the open spec pull request, the run is **unattended**.
Every fork in the road is yours to decide, and a question you would have put to
the user goes in the final report instead.

One exception: a ticket blocked on the user themselves, a credential, a product
decision, something no agent can derive. That chain stops and is reported, and
the rest of the run carries on.

## Entry points

- **`/land [spec or ticket numbers]`**: take the tickets from `/to-tickets` to
  one pull request. See *Landing tickets*.
- **`/land pr <number>`**: address the review comments on the spec pull
  request. See *Landing review comments*.

Both run the same dispatch rules. With no argument, ask which tickets.

## The tracker

`docs/agents/issue-tracker.md` says where tickets live and how they are
addressed. Read it first. When it is missing, tell the user to run
`/setup-matt-pocock-skills` and stop.

## Branches

One **integration branch** per spec, cut from the default branch before the
first dispatch and named for the spec. Everything the run produces lands there:

- each ticket branch is cut from the integration branch, and its pull request
  targets the integration branch
- you merge a ticket's pull request once it is green, because that is what
  releases the tickets it blocked
- the spec's own pull request goes from the integration branch to the default
  branch at the end: the run's one review surface, and **the user's to merge**

## Dispatch rules

- **One agent, one ticket.** An agent's whole job is one ticket, start to
  finish: branch, implement, guardrails green, one pull request closing the
  issue (`Closes #<n>`).
- **Each agent runs `/implement`.** That skill owns how the work is done. Your
  dispatch prompt names the ticket, the branch and the integration branch to
  target, and leaves `/implement` unrestated.
- **Tests are integration-first.** A new test drives a whole flow through real
  seams; implementation details stay untested. This line goes in every dispatch
  prompt; `/test-diet` prunes what slips through anyway.
- **The self-review is the gate.** `/implement` ends on `/code-review`; the
  agent fixes what that review finds before it opens its pull request. It is the
  only reading a ticket pull request gets before you merge it.
- **Worktree isolation is mandatory for a parallel round.** Pass
  `isolation: "worktree"` on every agent you dispatch alongside another: two
  agents in one checkout corrupt each other's work.
- **You pick each agent's model.** A capable general model carries an ordinary
  ticket; the strongest model available carries the hardest ones: a wide
  refactor, or a ticket several others are blocked by. This skill names no
  provider and no model; use what the environment offers.
- **The project's guardrails are the bar.** Its `CLAUDE.md` or `AGENTS.md` names
  them (lint, format, test, precommit). Every agent runs them green before
  opening its pull request; a red guardrail is a blocked ticket, not a PR.
- **A round above roughly six tickets goes to the `Workflow` tool** instead of
  loose agents: this skill is your authorisation to call it.

## Landing tickets

### 1. Read the frontier

Fetch the tickets. Each declares what **blocks** it. The **frontier** is every
ticket whose blockers are all done: those, and only those, can start now.

State the frontier before dispatching: the tickets going out this round, and
what stays behind waiting. It is a log line, not a gate.

### 2. Dispatch the round

Every frontier ticket goes out at once, one agent each, under the dispatch
rules. Each agent returns its pull request URL, or the reason it could not
finish.

### 3. Advance

Merge the round's green pull requests into the integration branch, then
recompute the frontier: a landed ticket releases the tickets it blocked.
Dispatch the next round.

A ticket that failed keeps its dependents blocked. Report that chain, leave it,
and carry the other chains forward. One stuck ticket does not stop the run.

Repeat until the frontier is empty.

### 4. Open the spec pull request

Run the project's guardrails once on the integration branch as a whole: the
slices were green apart, and this is the first time they are green together.

Then open one pull request, integration branch into the default branch. Its body
carries what the spec set out to do, the ticket pull requests that built it, and
anything reported blocked. This is the pull request the user reviews and merges.

### 5. Sweep

Leave nothing behind that the run created:

- delete each merged ticket branch, locally and on the remote
- remove every worktree the run made
- close the issues whose work merged, and close pull requests superseded by the
  integration branch
- delete the integration branch once its pull request is merged; while it is
  open, branch and pull request stay

The sweep deletes what is provably merged; anything else stays and goes in the
report.

## Landing review comments

### 1. Read the comments

Fetch the spec pull request's review comments, unresolved threads included.
Group them by what they ask for, not by who wrote them: several comments about
one mistake are one piece of work.

Comments that ask a question rather than a change go to the user, who answers
them.

### 2. Dispatch

One agent carries every grouped change: guardrails green, pushed to the
integration branch, and a reply on each thread it addressed saying what changed.
A review too large for one agent goes in rounds, one agent on the branch at a
time.

### 3. Report

What was addressed, what was left and why, and which threads now await the
user. Once the user has merged the spec pull request, sweep as in step 5.

## When your context fills

Call `/handoff` and name what remains: the tickets not yet dispatched, the pull
requests open, the chains reported blocked, and the integration branch. The next
orchestrator starts by reading the tracker, so the handoff carries the state the
tracker cannot.

## Done

Every ticket ends in one of two states, and the run reports which:

- merged into the integration branch, its issue closed
- blocked, with the reason and what would unblock it

No ticket is left unaccounted for. The run ends with one open spec pull request
and a swept repository.
