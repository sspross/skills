# skills

Personal agent skills, installable with [skills.sh](https://www.skills.sh/) or any tool that reads the `skills/<name>/SKILL.md` layout:

```sh
npx skills add sspross/skills
```

## Skills

Each entry is the skill's own `description`, copied verbatim.

- **[land](skills/land/SKILL.md)**: Take approved tickets to one reviewable pull request. `/land` dispatches agents across the ticket frontier, a PR per ticket onto an integration branch, then one spec PR for review; `/land pr <number>` dispatches agents to address review comments. Orchestrates only, never writes the code itself.

- **[restate-repo](skills/restate-repo/SKILL.md)**: Reissue the repository so it states only what is currently true. Deletes stale documentation, dead code and comments that restate the code, and corrects claims the implementation contradicts. `/restate-repo` runs all three passes; `/restate-repo comments` runs the comments pass alone.
