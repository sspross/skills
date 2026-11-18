# skills

Personal agent skills, installable with [skills.sh](https://www.skills.sh/) or any tool that reads the `skills/<name>/SKILL.md` layout:

```sh
npx skills add sspross/skills
```

## Skills

Each entry is the skill's own `description`, copied verbatim.

- **[acceptance-test](skills/acceptance-test/SKILL.md)**: Acceptance-test a spec pull request by using its running test version from outside. A fresh tester agent gets the spec and its tickets, exercises each promised behaviour in a browser (else HTTP or CLI), and posts its findings as comments on the pull request. Use when the user wants a spec PR or feature tested, or when another skill needs an acceptance test.

- **[bring](skills/bring/SKILL.md)**: Read and edit the user's Bring! shopping lists (getbring.com). Use when the user wants to see, add to, check off, or remove items from their shopping list ("Einkaufsliste").

- **[land](skills/land/SKILL.md)**: Take approved tickets to one reviewable pull request. `/land` dispatches agents across the ticket frontier, a PR per ticket onto an integration branch, then one spec PR for review; `/land pr <number>` dispatches agents to address the review comments on it. The run is unattended; it orchestrates only, never writes the code itself.

- **[minifax](skills/minifax/SKILL.md)**: Send something to a MiniFax, the thermal printer that prints messages on paper. Use when the user wants text, a todo list, or an image printed on their MiniFax or someone else's.

- **[template-sync](skills/template-sync/SKILL.md)**: Bring a project generated from the cookiecutter-django template up to date. Finds what changed upstream since the project's baseline, decides per topic how to adopt it, and opens one PR. Run from the project root.

- **[test-diet](skills/test-diet/SKILL.md)**: Put a project's test suite on a diet - profile it, prune low-value tests, consolidate unit tests into integration tests, trim e2e to golden journeys. One run, one PR.
