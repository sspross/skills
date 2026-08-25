# skills

Personal agent skills, installable with [skills.sh](https://www.skills.sh/) or any tool that reads the `skills/<name>/SKILL.md` layout:

```sh
npx skills add sspross/skills
```

## Skills

- **[cleanup](skills/cleanup/SKILL.md)**: delete what the repository no longer needs, so the working tree describes only its current state. `/cleanup` runs three passes over the whole repository (documentation and ADRs, dead code and spent feature flags, then comments and docstrings); `/cleanup comments` runs the comments pass alone. User-invoked only.
