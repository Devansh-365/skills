#!/usr/bin/env python3
"""Validate this repository's skill packages.

Structural checks only: package layout, frontmatter shape, Markdown fence
balance, and local link targets. Does not prescribe prose style.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("error: PyYAML is required (python -m pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
REQUIRED_FRONTMATTER = {"name", "description"}


def display(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, Any] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{display(path)}: missing opening YAML frontmatter delimiter")
        return None
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        errors.append(f"{display(path)}: missing closing YAML frontmatter delimiter")
        return None
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        errors.append(f"{display(path)}: invalid YAML: {error}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{display(path)}: frontmatter must be a YAML mapping")
        return None
    return data


def validate_fences(path: Path, text: str, errors: list[str]) -> None:
    active: str | None = None
    active_line = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        family = match.group(1)[0]
        if active is None:
            active, active_line = family, line_number
        elif active == family:
            active, active_line = None, 0
    if active is not None:
        errors.append(f"{display(path)}:{active_line}: unclosed Markdown code fence")


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    for line_number, line in enumerate(text.splitlines(), 1):
        for match in LINK_RE.finditer(line):
            target = match.group(1).strip().split(maxsplit=1)[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            if not target_path.exists():
                errors.append(f"{display(path)}:{line_number}: broken local link: {target}")


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{display(skill_dir)}: missing SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(skill_md, text, errors)
    if frontmatter is not None:
        missing = REQUIRED_FRONTMATTER - frontmatter.keys()
        if missing:
            errors.append(f"{display(skill_md)}: missing frontmatter keys: {sorted(missing)}")
        name = frontmatter.get("name")
        if isinstance(name, str) and not NAME_RE.match(name):
            errors.append(f"{display(skill_md)}: name must be lowercase-hyphenated: {name!r}")
        if isinstance(name, str) and name != skill_dir.name:
            errors.append(
                f"{display(skill_md)}: frontmatter name {name!r} must match directory {skill_dir.name!r}"
            )

    validate_fences(skill_md, text, errors)
    validate_links(skill_md, text, errors)


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"error: {display(SKILLS_DIR)} does not exist", file=sys.stderr)
        return 2

    errors: list[str] = []
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"error: no skill packages found under {display(SKILLS_DIR)}", file=sys.stderr)
        return 2

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"\n{len(errors)} error(s) across {len(skill_dirs)} skill package(s)", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_dirs)} skill package(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
