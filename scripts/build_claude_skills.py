#!/usr/bin/env python3
"""Build Claude-importable Skill ZIPs (one ZIP per skill) from skills/*.

Claude (claude.ai / Claude Desktop) requires each uploaded ZIP to contain exactly
one skill folder at its root:  <skill-name>/SKILL.md [+ references/scripts/assets].
Use --layout project to write Claude Code project-level skills to .claude/skills/.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skills import parse_front_matter  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".git")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = ("anthropic", "claude")
MAX_NAME, MAX_DESC = 64, 1024
MAIN_SKILL = "ai-rd-workflow"
MAIN_REFERENCES = {
    "agent-instructions.md": ROOT / "agent" / "instructions.md",
    "agent-manifest.yaml": ROOT / "agent" / "manifest.yaml",
    "skill-routing.yaml": ROOT / "config" / "skill-routing.yaml",
    "low-token-orchestration.md": ROOT / "docs" / "LOW-TOKEN-ORCHESTRATION.md",
}


def check_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        meta = parse_front_matter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{skill_dir.name}: {exc}"]
    name, desc = meta.get("name", ""), meta.get("description", "")
    if not NAME_RE.fullmatch(name) or len(name) > MAX_NAME:
        errors.append(f"{skill_dir.name}: name must be lowercase-hyphen, <= {MAX_NAME} chars")
    if any(word in name for word in RESERVED):
        errors.append(f"{skill_dir.name}: name must not contain reserved words {RESERVED}")
    if not desc.strip() or len(desc) > MAX_DESC:
        errors.append(f"{skill_dir.name}: description must be 1-{MAX_DESC} chars (now {len(desc)})")
    if re.search(r"<[^>]+>", name + desc):
        errors.append(f"{skill_dir.name}: name/description must not contain XML tags")
    return errors


def stage_skill(source: Path, parent: Path) -> Path:
    target = parent / source.name
    shutil.copytree(source, target, ignore=IGNORE)
    if source.name == MAIN_SKILL:  # 保证主控 Skill 的 references 引用闭合
        refs = target / "references"
        refs.mkdir(exist_ok=True)
        for name, path in MAIN_REFERENCES.items():
            if not path.is_file():
                raise FileNotFoundError(f"missing Agent source: {path}")
            shutil.copy2(path, refs / name)
    return target


def zip_skill(folder: Path, output: Path) -> None:
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(folder.parent).as_posix())
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if archive.testzip() or f"{folder.name}/SKILL.md" not in names:
            raise RuntimeError(f"invalid ZIP: {output}")
        if {n.split("/", 1)[0] for n in names} != {folder.name}:
            raise RuntimeError(f"ZIP must contain only the '{folder.name}/' root folder")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", choices=["zip", "project"], default="zip")
    parser.add_argument("--output", type=Path, default=None, help="default: dist/claude-skills or .claude/skills")
    parser.add_argument("--only", nargs="*", help="build only these skill names")
    args = parser.parse_args()

    skills = [d for d in sorted(SKILLS_DIR.iterdir()) if (d / "SKILL.md").is_file()]
    if args.only:
        skills = [d for d in skills if d.name in args.only]
    errors = [e for d in skills for e in check_skill(d)]
    if errors or not skills:
        print("Claude skill check failed:\n" + "\n".join(f"- {e}" for e in errors or ["no skills found"]), file=sys.stderr)
        return 1

    try:
        if args.layout == "project":
            out = (args.output or ROOT / ".claude" / "skills").resolve()
            out.mkdir(parents=True, exist_ok=True)
            for d in skills:
                shutil.rmtree(out / d.name, ignore_errors=True)
                stage_skill(d, out)
            print(f"Installed {len(skills)} skills to {out}")
        else:
            out = (args.output or ROOT / "dist" / "claude-skills").resolve()
            out.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="claude-skills-") as tmp:
                for d in skills:
                    zip_skill(stage_skill(d, Path(tmp)), out / f"{d.name}.zip")
            print(f"Built {len(skills)} ZIPs in {out}")
    except (OSError, RuntimeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
