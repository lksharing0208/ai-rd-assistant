#!/usr/bin/env python3
"""Generate the Claude Code plugin files at the repository root.

The repo root IS the plugin: skills/ (source of truth) + agents/ + .claude-plugin/.
Generated files are committed so users can install directly from GitHub:
  /plugin marketplace add lksharing0208/ai-rd-assistant
  /plugin install ai-rd-assistant@ai-rd-assistant
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_claude_skills import MAIN_REFERENCES, MAIN_SKILL, ROOT, SKILLS_DIR, check_skill  # noqa: E402

PLUGIN_NAME = "ai-rd-assistant"
DESCRIPTION = "面向真实软件项目的低 Token 研发助手：单主 Agent + 12 个专项 Skills，按需编排。"
AGENT_DESCRIPTION = (
    "面向真实软件项目的研发主 Agent。处理需求分析、源码理解、架构/API/数据库设计、"
    "代码实现、重构、审查、测试和交付；先判断任务等级，按需加载专项 Skills。"
)
AUTHOR = {"name": "AI 研发助手项目"}
REPO = "https://github.com/lksharing0208/ai-rd-assistant"


def version() -> str:
    data = json.loads((ROOT / "adapters" / "chatgpt" / "plugin.json").read_text(encoding="utf-8"))
    return data["version"]  # 与 ChatGPT 插件保持同一版本号


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    skills = [d for d in sorted(SKILLS_DIR.iterdir()) if (d / "SKILL.md").is_file()]
    errors = [e for d in skills for e in check_skill(d)]
    if errors or not skills:
        print("Check failed:\n" + "\n".join(f"- {e}" for e in errors or ["no skills found"]), file=sys.stderr)
        return 1

    ver = version()
    # 主控 Skill 的 references 需随仓库提交，保证从 GitHub 安装后引用闭合
    refs = SKILLS_DIR / MAIN_SKILL / "references"
    refs.mkdir(exist_ok=True)
    for name, path in MAIN_REFERENCES.items():
        shutil.copy2(path, refs / name)

    instructions = (ROOT / "agent" / "instructions.md").read_text(encoding="utf-8").split("\n", 1)[1].strip()
    agent = (
        "---\n"
        f"name: {PLUGIN_NAME}\n"
        f"description: {AGENT_DESCRIPTION}\n"
        "model: inherit\n"
        "---\n\n"
        "# AI 研发助手\n\n"
        f"{instructions}\n\n"
        "## Skills\n"
        "可用 Skills：" + "、".join(d.name for d in skills) + "。\n"
        "先用 `ai-rd-workflow` 的任务分级和路由表选择主 Skill，再按需加载辅助 Skill。\n"
    )
    (ROOT / "agents").mkdir(exist_ok=True)
    (ROOT / "agents" / f"{PLUGIN_NAME}.md").write_text(agent, encoding="utf-8")

    write_json(ROOT / ".claude-plugin" / "plugin.json", {
        "name": PLUGIN_NAME, "version": ver, "description": DESCRIPTION,
        "author": AUTHOR, "homepage": REPO, "repository": REPO,
        "keywords": ["software-development", "agent", "skills", "code-review", "low-token"],
    })
    write_json(ROOT / ".claude-plugin" / "marketplace.json", {
        "name": PLUGIN_NAME, "owner": AUTHOR,
        "plugins": [{
            "name": PLUGIN_NAME, "source": "./",
            "description": DESCRIPTION, "version": ver,
        }],
    })
    print(f"Plugin {PLUGIN_NAME} v{ver}: {len(skills)} skills + 1 agent (repo root)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
