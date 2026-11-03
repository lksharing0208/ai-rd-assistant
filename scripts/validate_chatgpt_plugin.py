#!/usr/bin/env python3
"""Validate the ChatGPT Plugin Adapter source files without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_DIR = ROOT / "adapters" / "chatgpt"
MANIFEST_FILE = ADAPTER_DIR / "plugin.json"
AGENT_FILE = ADAPTER_DIR / "agents" / "openai.yaml"
MAIN_SKILL = ROOT / "skills" / "ai-rd-workflow" / "SKILL.md"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*['\"]?([^\r\n'\"#]+?)['\"]?\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def main() -> int:
    try:
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return fail(f"cannot read plugin manifest: {exc}")

    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        return fail("plugin.json must declare the Agent Plugins 1.0 schema")
    if manifest.get("name") != "ai-rd-assistant":
        return fail("plugin.json name must remain ai-rd-assistant")
    if not SEMVER_RE.fullmatch(str(manifest.get("version", ""))):
        return fail("plugin.json version must be strict SemVer")

    forbidden = {"skills", "mcpServers", "apps", "interface"} & set(manifest)
    if forbidden:
        return fail(f"portable plugin.json must not declare top-level fields: {sorted(forbidden)}")

    openai = manifest.get("extensions", {}).get("com.openai", {})
    interface = openai.get("interface", {})
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            return fail(f"plugin interface.{field} must be a non-empty string")

    if len(interface["shortDescription"]) > 30:
        return fail("plugin interface.shortDescription must be at most 30 characters")
    if not isinstance(interface.get("capabilities"), list) or any(
        not isinstance(value, str) or not value.strip() for value in interface["capabilities"]
    ):
        return fail("plugin interface.capabilities must be an array of non-empty strings")

    prompts = interface.get("defaultPrompt")
    if not (
        isinstance(prompts, str) and prompts.strip()
        or isinstance(prompts, list) and 1 <= len(prompts) <= 3
        and all(isinstance(value, str) and value.strip() for value in prompts)
    ):
        return fail("plugin interface.defaultPrompt must be a string or an array of 1-3 non-empty strings")

    try:
        agent_text = AGENT_FILE.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return fail(f"cannot read root Agent configuration: {exc}")

    expected_agent = {
        "display_name": "AI 研发助手",
        "short_description": "低 Token 研发全流程助手",
    }
    for key, expected in expected_agent.items():
        value = yaml_scalar(agent_text, key)
        if value != expected:
            return fail(f"agents/openai.yaml {key} must be '{expected}'")

    if yaml_scalar(agent_text, "default_prompt") is None:
        return fail("agents/openai.yaml must define interface.default_prompt")
    if not re.search(r"^\s*allow_implicit_invocation:\s*(true|false)\s*$", agent_text, re.MULTILINE):
        return fail("agents/openai.yaml must define policy.allow_implicit_invocation as a YAML boolean")

    if not MAIN_SKILL.is_file():
        return fail("missing skills/ai-rd-workflow/SKILL.md")
    if "name: ai-rd-workflow" not in MAIN_SKILL.read_text(encoding="utf-8").split("---", 2)[1]:
        return fail("main Skill front matter name must be ai-rd-workflow")

    required_sources = [
        ROOT / "agent" / "instructions.md",
        ROOT / "agent" / "manifest.yaml",
        ROOT / "config" / "skill-routing.yaml",
        ROOT / "docs" / "LOW-TOKEN-ORCHESTRATION.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_sources if not path.is_file()]
    if missing:
        return fail(f"missing Agent source files required by the package builder: {missing}")

    print(
        "ChatGPT Plugin Adapter validation passed: "
        f"{manifest['name']} v{manifest['version']} / {interface['displayName']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
