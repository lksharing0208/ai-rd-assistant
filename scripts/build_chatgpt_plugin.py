#!/usr/bin/env python3
"""Build one ChatGPT Plugin ZIP from the unified Agent source and Skills."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ADAPTER_DIR = ROOT / "adapters" / "chatgpt"


def run_validation() -> None:
    commands = [
        [sys.executable, str(ROOT / "scripts" / "validate_skills.py")],
        [sys.executable, str(ROOT / "scripts" / "validate_chatgpt_plugin.py")],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True)


def copy_skill_sources(package_root: Path) -> int:
    target_skills = package_root / "skills"
    target_skills.mkdir(parents=True, exist_ok=True)
    count = 0

    for source in sorted(SKILLS_DIR.iterdir()):
        if not source.is_dir() or not (source / "SKILL.md").is_file():
            continue
        destination = target_skills / source.name
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".git"),
        )
        count += 1

    if count == 0:
        raise RuntimeError("no skills/*/SKILL.md files found")

    # 将统一 Agent 源配置复制到主控 Skill 的 references，确保打包后引用仍然闭合。
    references = target_skills / "ai-rd-workflow" / "references"
    references.mkdir(parents=True, exist_ok=True)
    reference_sources = {
        "agent-instructions.md": ROOT / "agent" / "instructions.md",
        "agent-manifest.yaml": ROOT / "agent" / "manifest.yaml",
        "skill-routing.yaml": ROOT / "config" / "skill-routing.yaml",
        "low-token-orchestration.md": ROOT / "docs" / "LOW-TOKEN-ORCHESTRATION.md",
    }
    for target_name, source_path in reference_sources.items():
        if not source_path.is_file():
            raise FileNotFoundError(f"required Agent source is missing: {source_path}")
        shutil.copy2(source_path, references / target_name)

    return count


def build_archive(output: Path) -> tuple[int, int]:
    manifest = json.loads((ADAPTER_DIR / "plugin.json").read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="ai-rd-assistant-chatgpt-") as temporary:
        package_root = Path(temporary) / "package"
        package_root.mkdir()

        shutil.copy2(ADAPTER_DIR / "plugin.json", package_root / "plugin.json")
        shutil.copy2(ADAPTER_DIR / "agents" / "openai.yaml", package_root / "agents" / "openai.yaml")
        shutil.copy2(ADAPTER_DIR / "README.md", package_root / "README.md")
        skill_count = copy_skill_sources(package_root)

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(package_root.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(package_root).as_posix())

    with zipfile.ZipFile(output, "r") as archive:
        bad_file = archive.testzip()
        if bad_file:
            raise RuntimeError(f"ZIP integrity check failed at {bad_file}")
        names = set(archive.namelist())
        if "plugin.json" not in names or "agents/openai.yaml" not in names:
            raise RuntimeError("ZIP root must contain plugin.json and agents/openai.yaml")
        if "skills/ai-rd-workflow/SKILL.md" not in names:
            raise RuntimeError("ZIP is missing the main Agent workflow Skill")
        if any(name.startswith("ai-rd-assistant/") for name in names):
            raise RuntimeError("ZIP must not contain an extra enclosing directory")

    print(f"Built: {output}")
    print(f"Plugin: {manifest['extensions']['com.openai']['interface']['displayName']}")
    print(f"Version: {manifest['version']}")
    print(f"Skills: {skill_count}")
    print("ZIP root: plugin.json, agents/openai.yaml, README.md, skills/")
    return skill_count, output.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="ZIP output path; defaults to dist/ai-rd-assistant-chatgpt-v<version>.zip",
    )
    args = parser.parse_args()

    try:
        run_validation()
        manifest = json.loads((ADAPTER_DIR / "plugin.json").read_text(encoding="utf-8"))
        output = args.output or (
            ROOT / "dist" / f"ai-rd-assistant-chatgpt-v{manifest['version']}.zip"
        )
        build_archive(output.resolve())
    except (OSError, ValueError, subprocess.CalledProcessError, RuntimeError, KeyError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
