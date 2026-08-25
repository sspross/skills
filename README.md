# skills

Personal agent skills, installable with [skills.sh](https://www.skills.sh/) or any tool that reads the `skills/<name>/SKILL.md` layout:

```sh
npx skills add sspross/skills
```

## Skills

- **[cleanup](skills/cleanup/SKILL.md)**: delete what the repository no longer needs, so the working tree describes only its current state. Two branches picked by argument: `/cleanup comments` touches comments and docstrings only and leaves every executable token byte-identical, `/cleanup repo` cleans documentation, ADRs, dead code and spent feature flags. User-invoked only.
