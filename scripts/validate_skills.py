#!/usr/bin/env python3
"""Validate Skill folder names and SKILL.md front matter using Python stdlib only."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*)(.*)$")


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")

    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("front matter is not closed")

    lines = text[4:end].splitlines()
    result: dict[str, str] = {}
    index = 0

    while index < len(lines):
        line = lines[index]
        index += 1

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        match = FIELD_RE.match(line)
        if not match:
            continue

        key, value = match.groups()
        value = value.strip()

        if value in {">", "|", ">-", "|-"}:
            block_lines: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if candidate.strip() and not candidate[0].isspace():
                    break
                if candidate.strip():
                    block_lines.append(candidate.strip())
                index += 1
            separator = "\n" if value.startswith("|") else " "
            value = separator.join(block_lines)
        else:
            value = value.strip("\"'")

        result[key] = value

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
        relative_path = skill_file.relative_to(ROOT)

        try:
            metadata = parse_front_matter(skill_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative_path}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "")

        if not NAME_RE.fullmatch(folder):
            errors.append(f"{relative_path}: invalid folder name '{folder}'")
        if not name:
            errors.append(f"{relative_path}: missing name")
        elif name != folder:
            errors.append(f"{relative_path}: name '{name}' != folder '{folder}'")
        if not description.strip():
            errors.append(f"{relative_path}: missing description")

        if name in seen:
            errors.append(f"duplicate skill name '{name}': {seen[name]} and {relative_path}")
        elif name:
            seen[name] = relative_path

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill validation passed: {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
