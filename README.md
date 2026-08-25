# skills

Personal agent skills, installable with [skills.sh](https://www.skills.sh/) or any tool that reads the `skills/<name>/SKILL.md` layout:

```sh
npx skills add sspross/skills
```

## Skills

- **[restate-repo](skills/restate-repo/SKILL.md)**: reissue the repository so it states only what is currently true, the way a restatement reissues a published record to correct it. `/restate-repo` runs three passes over the whole repository (documentation and ADRs, dead code and spent feature flags, then comments and docstrings); `/restate-repo comments` runs the comments pass alone. User-invoked only.
