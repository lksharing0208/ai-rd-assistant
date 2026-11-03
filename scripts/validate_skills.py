#!/usr/bin/env python3
"""Validate Skill folder names and SKILL.md front matter using Python stdlib only."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("front matter is not closed")

    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def main() -> int:
    if not SKILLS_DIR.exists():
        print("ERROR: skills/ directory not found")
        return 2

    errors: list[str] = []
    seen: dict[str, Path] = {}
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))

    if not skill_files:
        errors.append("no skills/*/SKILL.md files found")

    for skill_file in skill_files:
        folder = skill_file.parent.name
        try:
            metadata = parse_front_matter(skill_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{skill_file.relative_to(ROOT)}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not NAME_RE.fullmatch(folder):
            errors.append(f"{skill_file.relative_to(ROOT)}: invalid folder name '{folder}'")
        if not name:
            errors.append(f"{skill_file.relative_to(ROOT)}: missing name")
        elif name != folder:
            errors.append(f"{skill_file.relative_to(ROOT)}: name '{name}' != folder '{folder}'")
        if not description or description in {">", "|"}:
            errors.append(f"{skill_file.relative_to(ROOT)}: missing description")
        if name in seen:
            errors.append(f"duplicate skill name '{name}': {seen[name]} and {skill_file}")
        else:
            seen[name] = skill_file

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill validation passed: {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
