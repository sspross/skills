#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["cookiecutter"]
# ///
"""Render a project's cookiecutter template at its baseline and at HEAD, and diff the two.

Run from the project root. Prints a JSON report; the renders land in the output directory.
"""

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path

from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter
from jinja2 import TemplateError

DEFAULT_TEMPLATE = "https://github.com/sspross/cookiecutter-django.git"
MARKER = Path(".template.json")
RENDERED_ROOT = "{{ cookiecutter.project_slug }}"
GENERATED_MARKER_FILE = "manage.py"
MAX_CANDIDATES = 30
LOCKFILES = ("uv.lock", "poetry.lock", "package-lock.json")


def main():
    args = _parse_args()
    marker = json.loads(MARKER.read_text()) if MARKER.exists() else {}
    template_url = args.template or marker.get("template", DEFAULT_TEMPLATE)
    context = marker.get("context") or _context_from_project()

    out = Path(args.out or tempfile.mkdtemp(prefix="template-sync-")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    clone = out / "template"
    _git("clone", "-q", template_url, str(clone))
    head = _rev_parse(clone, "HEAD")

    candidates, skipped_candidates = [], []
    if args.base:
        base, base_source = _rev_parse(clone, args.base), "argument"
    elif marker.get("commit"):
        base, base_source = marker["commit"], "marker"
    else:
        candidates, skipped_candidates = _rank_baselines(clone, context, out)
        base, base_source = candidates[0]["commit"], "inferred"

    _render(clone, base, context, out / "base")
    _render(clone, head, context, out / "head")

    patch = out / "upstream.patch"
    patch.write_text(_diff("base", "head", cwd=out))
    commits = _git(
        "-C", str(clone), "log", "--reverse", "--format=%h %ad %s", "--date=short",
        f"{base}..{head}", "--", RENDERED_ROOT,
    ).splitlines()

    new_marker = {"template": template_url, "commit": head, "context": context}
    (out / "new-marker.json").write_text(json.dumps(new_marker, indent=2) + "\n")
    print(json.dumps({
        "base": base,
        "base_source": base_source,
        "head": head,
        "up_to_date": not patch.read_text(),
        "commits": commits,
        "candidates": candidates[:3],
        "skipped_candidates": skipped_candidates,
        "context": context,
        "out": str(out),
    }, indent=2))


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="template commit to diff from, overrides the marker")
    parser.add_argument("--template", help="template repository URL or path")
    parser.add_argument("--out", help="output directory, default is a new temp directory")
    return parser.parse_args()


def _context_from_project():
    context = {"project_slug": tomllib.loads(Path("pyproject.toml").read_text())["project"]["name"]}
    readme = Path("README.md")
    if readme.exists() and (title := re.match(r"# (.+)", readme.read_text())):
        context["project_name"] = title.group(1).strip()
    remote = _git("remote", "get-url", "origin", check=False)
    if owner := re.search(r"github\.com[:/]([^/]+)/", remote):
        context["github_owner"] = owner.group(1)
    return context


def _rank_baselines(clone, context, out):
    """Rank template commits by how closely their render matches the commit that added the project.

    Returns the ranked candidates and the commits skipped because they do not render.
    """
    added = _git(
        "log", "--diff-filter=A", "--reverse", "--format=%H %aI", "--", GENERATED_MARKER_FILE
    ).splitlines()
    if not added:
        raise SystemExit(f"No commit adds {GENERATED_MARKER_FILE}: not generated from this template.")
    generation_commit, generated_at = added[0].split()

    snapshot = out / "generated"
    snapshot.mkdir()
    archive = subprocess.run(["git", "archive", generation_commit], check=True, capture_output=True)
    subprocess.run(["tar", "-x", "-C", str(snapshot)], input=archive.stdout, check=True)
    _remove_lockfiles(snapshot)

    commits = _git(
        "-C", str(clone), "log", f"--until={generated_at}", f"-{MAX_CANDIDATES}", "--format=%H"
    ).splitlines()
    ranked, skipped = [], []
    scratch = out / "candidate"
    for commit in commits:
        try:
            _render(clone, commit, context, scratch)
            _remove_lockfiles(scratch)
            ranked.append({"commit": commit, "changed_lines": _changed_lines(scratch, snapshot)})
        except (CookiecutterException, TemplateError) as error:
            skipped.append({"commit": commit, "error": f"{type(error).__name__}: {error}"})
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    shutil.rmtree(snapshot)
    if not commits:
        raise SystemExit(f"No template commit predates the project ({generated_at}).")
    if not ranked:
        failures = "\n".join(f"{failure['commit']}: {failure['error']}" for failure in skipped)
        raise SystemExit(f"No candidate template commit renders:\n{failures}")
    return sorted(ranked, key=lambda candidate: candidate["changed_lines"]), skipped


def _render(clone, commit, context, target):
    _git("-C", str(clone), "checkout", "-q", commit)
    with tempfile.TemporaryDirectory() as rendered:
        cookiecutter(
            str(clone), no_input=True, extra_context=context, output_dir=rendered, accept_hooks=False
        )
        shutil.move(str(next(Path(rendered).iterdir())), target)


def _remove_lockfiles(tree):
    for name in LOCKFILES:
        for lockfile in tree.rglob(name):
            lockfile.unlink()


def _changed_lines(left, right):
    shortstat = _diff(left, right, "--shortstat")
    return sum(int(count) for count in re.findall(r"(\d+) (?:insertion|deletion)", shortstat))


def _diff(left, right, *options, cwd=None):
    # --no-index exits 1 when the trees differ.
    return subprocess.run(
        ["git", "diff", "--no-index", *options, str(left), str(right)],
        capture_output=True, text=True, cwd=cwd,
    ).stdout


def _rev_parse(clone, rev):
    return _git("-C", str(clone), "rev-parse", rev).strip()


def _git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check).stdout


if __name__ == "__main__":
    main()
