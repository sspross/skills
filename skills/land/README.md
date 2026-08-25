# land

`land` takes a set of approved tickets and gives you back one pull request to
review. It orchestrates: it dispatches the agents that write the code, merges
what they land, and never writes the implementation itself.

## The arc it sits in

A feature travels one arc, and each step is a skill:

1. **Understand**: `/grilling`, `/research`, `/grill-with-docs`, `/prototype`.
   Talk until you and the agent hold the same picture.
2. **Spec**: `/to-spec` publishes that picture to the issue tracker as one
   issue.
3. **Split**: `/to-tickets` breaks the spec into tracer-bullet tickets. Each is
   a thin end-to-end slice that ships on its own, and each declares the tickets
   that block it.
4. **Land**: `/land <spec>`. This skill.
5. **Iterate**: `/land pr <number>` on the review comments, until you merge.

Steps 1 to 3, plus `/implement`, come from Matt Pocock's engineering skills;
`/setup-matt-pocock-skills` configures a repo for them. `land` is steps 4 and 5.

## The gap it fills

After `/to-tickets` you have a dependency graph of issues, every one of them
ready for an agent. What you do not have is anything that runs it.

`/implement` does one ticket. It does not know about the other twelve, which of
them are unblocked, or what to do when one goes red. Driving that by hand means:
read the tickets, work out what can start now, open a terminal per ticket, wait,
merge, work out what just became unblocked, repeat. That bookkeeping is the
reason a finished ticket set sits unstarted.

`land` is the bookkeeping:

- reads the **frontier**, every ticket whose blockers are all done
- dispatches one agent per frontier ticket at once, each in its own worktree,
  each running `/implement`
- merges what comes back green, recomputes the frontier, dispatches the next
  round
- reports a failed ticket's blocked chain and carries the other chains forward
- opens one pull request at the end, then sweeps the branches, worktrees and
  issues the run created

## One pull request to review

Every ticket still gets its own pull request, so each slice stays reviewable on
its own. Those target an **integration branch**, and `land` merges them itself
once they are green: that merge is what releases the tickets they blocked.

```
main
 └── spec/<name>              the integration branch, land owns it
      ├── ticket-1 PR   ──►   land merges it, once green
      ├── ticket-2 PR   ──►   land merges it, once green
      └── ticket-3 PR   ──►   land merges it, once green

spec/<name> ──► main          one PR, yours to review and yours to merge
```

Your review surface is that last pull request and nothing else. `/land pr
<number>` runs on it alone.

## Unattended

Once `/land` is invoked you are out of it until the spec pull request is open.
It decides the forks itself, and a question it would have put to you goes into
the final report instead. There is no confirmation step between rounds.

The exception is a ticket blocked on you personally: a credential, a product
decision, something no agent can derive. That chain stops and is reported, and
the rest of the run carries on.

## Before you run it

- The repo needs `docs/agents/issue-tracker.md`, which says where tickets live
  and how they are addressed. `/setup-matt-pocock-skills` writes it.
- Start `/land` in a fresh context. It reads the tracker, not your conversation,
  so a `/clear` straight after `/to-tickets` costs you nothing.
- It wants a machine it may work on unsupervised: parallel worktrees, branches
  pushed, ticket pull requests merged. Run it where that is fine, a VM or a
  dev box, not on a checkout someone else is using.
- It is user-invoked only. Nothing fires it but you typing `/land`.
