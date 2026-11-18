---
name: acceptance-test
description: Acceptance-test a spec pull request by using its running test version from outside. A fresh tester agent gets the spec and its tickets, exercises each promised behaviour in a browser (else HTTP or CLI), and posts its findings as comments on the pull request. Use when the user wants a spec PR or feature tested, or when another skill needs an acceptance test.
argument-hint: "a spec pull request number"
---

# acceptance-test

A **black-box** check of a spec pull request: one **tester** uses the running
test version the way a user would and reports which promised behaviours it could
confirm. It reports and posts; fixing belongs to whoever called this skill.

You are the dispatcher. The tester is a separate agent with a fresh context, so
that it knows what was asked and nothing about how it was built.

## 1. Gather the tester's input

With no pull request number, ask for one.

- **The spec**: the spec issue the pull request implements and every ticket
  under it, fetched as `docs/agents/issue-tracker.md` describes. Take the issue
  bodies as written.
- **The test version**: its URL and login. The pull request body names them.
  Check the URL answers. When it does not, start the test version on the pull
  request's branch with the command the project's `CLAUDE.md` or `AGENTS.md`
  names, from the main checkout, and use the URL and login it prints.

A project that names no test version has nothing to test from outside: report
`not testable: no test version` and stop.

Done when you hold the spec issue, every ticket, a URL that answers, and a
login.

## 2. Dispatch the tester

One tester per spec, a fresh agent without your conversation: the test version
is one instance with one database, and one tester walks it in order.

Its prompt carries exactly this:

- the spec issue and ticket bodies, verbatim
- the URL, the login, and the pull request number
- the *Tester brief* below, verbatim

Everything the implementing agents wrote stays out: ticket pull request bodies,
commit messages, diffs, your own summary of the work.

## 3. Report

Relay the tester's summary: the counts per state, and the link to each finding.

## Tester brief

You are the **tester** of a spec. You judge it as a user of the running product:
through the browser first, through HTTP or the command line where a behaviour
has no page. The product's own surface and the project's user-facing docs are
your only sources; the source code and the diff stay closed.

Use the browser tooling this environment offers. With no browser available, test
over HTTP and say so in the summary.

**Build the checklist first.** List every behaviour the spec and its tickets
promise, one line each, before you open the product. That list is the scope.

**Exercise every line.** For each behaviour, do what a user would do and compare
what happens with what was promised. Watch the browser console and the HTTP
responses while you do. Each line ends in one state:

- **passed**: you saw the promised behaviour
- **failed**: the spec promises it and you saw something else
- **unclear**: the spec does not say what should happen, so you cannot judge
- **not testable**: nothing about it is observable from outside

Something clearly broken that no line promises is a finding too, in the state
**outside spec**.

**Post one comment per finding** on the pull request, for every failed, unclear
and outside-spec line:

```
**Acceptance test: failed** — <the behaviour, one line>

Ticket: #<n>
Steps: <what you did, numbered, exact enough to repeat>
Expected: <what the spec promises, quoted>
Observed: <what happened, with console or HTTP errors>
```

The first line names the state: `failed`, `unclear` or `outside spec`.

**Then post one summary comment**, starting `**Acceptance test: summary**`: the
whole checklist with each line's state, how you tested (browser, HTTP, CLI), and
the accounts and records you created. Leave that data in place; the user tests
on the same instance next.

You are done when every checklist line has a state, every finding has its
comment, and the summary is posted. Return the summary and the finding links.
