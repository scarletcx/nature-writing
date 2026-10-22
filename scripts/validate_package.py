#!/usr/bin/env python3
"""Validate the nature-writing skill package.

Checks required files, frontmatter, version, corpus indexes, and local
Markdown links. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MIN_REFERENCES = 15
MIN_FIGURE_REFERENCES = 12
MIN_EXTRACTS = 7

REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "FIGURE-SKILL.md",
    "_framework.md",
    "README.md",
    "references/README.md",
    "figure-references/README.md",
)

DOC_FILES = (
    "README.md",
    "NOTICE.md",
    "skills/nature-writing/README.md",
    "skills/nature-writing/SKILL.md",
    "skills/nature-writing/FIGURE-SKILL.md",
    "skills/nature-writing/references/README.md",
    "skills/nature-writing/figure-references/README.md",
)

LINK_RE = re.compile(r"\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    parent = ""
    for raw in parts[1].splitlines():
        if not raw.strip():
            continue
        if raw.startswith((" ", "\t")) and parent:
            key, _, value = raw.strip().partition(":")
            data[f"{parent}.{key.strip()}"] = value.strip().strip('"').strip("'")
            continue
        key, _, value = raw.partition(":")
        parent = key.strip()
        data[parent] = value.strip().strip('"').strip("'")
    return data


def check_links(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for target in LINK_RE.findall(line):
            target = target.strip()
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0].strip()
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path}: broken local link -> {target}")


def build_report(repo_root: Path) -> dict:
    skill_dir = repo_root / "skills" / "nature-writing"
    errors: list[str] = []

    for relative in REQUIRED_SKILL_FILES:
        path = skill_dir / relative
        if not path.exists():
            errors.append(f"missing required file: {path}")

    for relative in ("LICENSE", "NOTICE.md"):
        if not (repo_root / relative).exists():
            errors.append(f"missing required file: {repo_root / relative}")

    skill_md = skill_dir / "SKILL.md"
    frontmatter: dict[str, str] = {}
    if skill_md.exists():
        frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if frontmatter.get("name") != "nature-writing":
            errors.append("SKILL.md frontmatter name must be nature-writing")
        if not frontmatter.get("description"):
            errors.append("SKILL.md frontmatter description is empty")
        if frontmatter.get("license") != "MIT":
            errors.append("SKILL.md frontmatter license must be MIT")
        if frontmatter.get("metadata.version") != "5.0.0":
            errors.append("SKILL.md metadata.version must be 5.0.0")
        lines = skill_md.read_text(encoding="utf-8").splitlines()
        title = next((line for line in lines if line.startswith("# ")), "")
        if "v5" not in title:
            errors.append("SKILL.md must have a v5 title")

    references = sorted((skill_dir / "references").glob("[0-9][0-9]-*.md"))
    figure_references = sorted((skill_dir / "figure-references").glob("[0-9][0-9]-*.md"))
    extracts = sorted((skill_dir / "extracts").glob("[0-9][0-9]-*.md"))

    if len(references) < MIN_REFERENCES:
        errors.append(f"expected {MIN_REFERENCES} reference files, found {len(references)}")
    if len(figure_references) < MIN_FIGURE_REFERENCES:
        errors.append(
            f"expected {MIN_FIGURE_REFERENCES} figure reference files, "
            f"found {len(figure_references)}"
        )
    if len(extracts) < MIN_EXTRACTS:
        errors.append(f"expected {MIN_EXTRACTS} extract files, found {len(extracts)}")

    index_files = (
        skill_dir / "references" / "README.md",
        skill_dir / "figure-references" / "README.md",
    )
    for path in index_files:
        if path.exists() and "44 篇" not in path.read_text(encoding="utf-8"):
            errors.append(f"{path}: index should describe 44 papers")

    figure_skill = skill_dir / "FIGURE-SKILL.md"
    if figure_skill.exists():
        figure_text = figure_skill.read_text(encoding="utf-8")
        if "44 篇" not in figure_text or "07-ai-methods.md" not in figure_text:
            errors.append("FIGURE-SKILL.md should reference the 44-paper corpus")

    skill_readme = skill_dir / "README.md"
    if skill_readme.exists():
        readme_text = skill_readme.read_text(encoding="utf-8")
        for needle in ("44 篇", "scarletcx/nature-writing", "NOTICE.md"):
            if needle not in readme_text:
                errors.append(f"skills/nature-writing/README.md missing: {needle}")
        if "archive/SKILL.v3.md" in readme_text:
            errors.append("skills/nature-writing/README.md references a missing archive file")

    for relative in DOC_FILES:
        path = repo_root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "/Users/" in text or "/Applications/" in text:
            errors.append(f"{path}: contains an absolute local path")
        check_links(path, errors)

    return {
        "ok": not errors,
        "repo_root": str(repo_root),
        "skill_dir": str(skill_dir),
        "version": frontmatter.get("metadata.version", ""),
        "counts": {
            "references": len(references),
            "figure_references": len(figure_references),
            "extracts": len(extracts),
        },
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the nature-writing package.")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root (default: the parent of scripts/).",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    args = parser.parse_args(argv)

    report = build_report(Path(args.repo_root).resolve())
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        counts = report["counts"]
        print("nature-writing package check")
        print(f"Repository: {report['repo_root']}")
        print(
            "Files: "
            f"{counts['references']} writing references, "
            f"{counts['figure_references']} figure references, "
            f"{counts['extracts']} corpus extracts"
        )
        if report["ok"]:
            print("OK: package structure and local links are valid")
        else:
            for error in report["errors"]:
                print(f"ERROR: {error}", file=sys.stderr)

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
