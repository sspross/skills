---
name: template-sync
description: Bring a project generated from the cookiecutter-django template up to date. Finds what changed upstream since the project's baseline, decides per topic how to adopt it, and opens one PR. Run from the project root.
argument-hint: "optional template commit to use as baseline"
disable-model-invocation: true
---

# template-sync

The **upstream** is the template repository. The **baseline** is the upstream commit the project last caught up with. A sync carries the upstream's intent into the project, adapted to what the project has become since. It is a judgment call per change, never a blind merge: the project is the authority on its own code, and the upstream is a proposal.

The session owns the decisions, the commits and the PR. Reading one topic against the project may go to a subagent; the verdict stays here.

## 1. Render

Start from a clean working tree on a fresh branch `template-sync/<date>`. Then run, from the project root:

```sh
uv run --script <skill-dir>/scripts/template_diff.py [--base <commit>]
```

It clones the upstream, renders it at the baseline and at HEAD with the project's values, skips hooks so both renders are deterministic, and prints a JSON report. In the report's `out` directory: `base/`, `head/`, `upstream.patch`, `template/` (the upstream clone) and `new-marker.json`.

The baseline comes from `--base`, else from `.template.json` in the project, else it is inferred: the upstream commit whose render best matches the commit that added `manage.py`. An inferred baseline is a claim to check: `candidates` should show a clear winner. State it in the PR body.

`up_to_date: true`: report that and stop. The script exiting with "not generated from this template": report that and stop.

Done when: the report exists and the baseline is trusted.

## 2. Triage

`commits` holds every upstream commit that touched the rendered project. Read each one (`git -C <out>/template show`) for its intent. Group them into **topics**: one intent, usually one commit, sometimes a run of them (a bump and its follow-up fix). A later commit can undo an earlier one, so `upstream.patch`, the net change, decides what a topic is today; the commits only explain why.

Give each topic one verdict, after reading the project code it touches:

- **adopt**: the project wants this and it fits.
- **adapt**: the project wants the intent, but in a different shape.
- **skip**: the project already has it, solved it differently, or removed that part on purpose. Check `git log` on the project before calling a missing file an oversight.
- **ask**: adopting it could harm production data or running deployments, or it needs a product decision. Skip it in this run and put the question in the PR body.

Done when: every commit in `commits` belongs to a topic and every topic has a verdict with a one-line reason.

## 3. Apply

Work the adopt and adapt topics in dependency order, one commit per topic, with the upstream commit hashes in the message.

For a file on both sides, three-way merge the upstream change into it, then resolve what conflicts:

```sh
git merge-file <project-file> <out>/base/<path> <out>/head/<path>
```

Copy new files from `head/`. These kinds of files need their own handling:

- **Migrations**: never copy. Change the models, then run `makemigrations`, because the project's migration graph is its own. A change to the user model or to an existing table goes to **ask** when the project holds production data.
- **Dependencies**: `uv add`, or the frontend's package manager, instead of merging lockfiles. Keep whichever version is higher.
- **Generated files**: regenerate with the project's command (`make schema`).
- **ADRs**: a new upstream ADR takes the project's next free number, and links to it follow. An edited upstream ADR applies only if the project still holds that decision.
- **Docs and `CLAUDE.md`**: merge by meaning. Keep the project's own language and domain.

Collect every change a person must make outside the repo: new env vars, GitHub secrets, deploy settings, one-off commands.

Finish with a commit that copies `new-marker.json` to `.template.json`, so the next sync starts at this upstream HEAD and skipped topics stay decided.

Done when: every adopt and adapt topic is committed and `make test`, `make lint` and `make precommit` pass.

## 4. Review

Push and open one PR, body written with `/pr`. It carries:

- The baseline and upstream HEAD, and how the baseline was found.
- A table of every topic: verdict, reason, upstream commits.
- The **ask** questions.
- The manual steps from outside the repo.

Done when: the PR is open and its table accounts for every commit from the report.
