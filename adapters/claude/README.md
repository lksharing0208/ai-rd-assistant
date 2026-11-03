# Claude Skills 导入说明

将 `skills/*` 打包为 Claude 可导入的 Skill。核心内容不变，仅做打包适配。

## 1. 构建

```bash
python scripts/validate_skills.py
python scripts/build_claude_skills.py
```

输出 `dist/claude-skills/<skill-name>.zip`，共 12 个，每个 ZIP 根目录只有一个 `<skill-name>/` 文件夹，内含 `SKILL.md` 及 references/scripts/assets。

构建检查（Claude 要求）：name 为小写连字符且 ≤64 字符、不含 `anthropic`/`claude`；description 1–1024 字符；name/description 不含 XML 标签。

`ai-rd-workflow` 构建时自动把 `agent/`、`config/skill-routing.yaml`、`docs/LOW-TOKEN-ORCHESTRATION.md` 复制进其 `references/`，保证引用闭合。

## 2. 导入 claude.ai / Claude Desktop

1. Settings → Capabilities，开启 Code execution and file creation 和 Skills。
2. Skills → Upload skill，逐个上传 ZIP。
3. 至少上传 `ai-rd-workflow.zip` 和 `intent-router.zip`，其余专项 Skill 按需上传。
4. 在对话中描述研发任务，Claude 会按 description 自动触发；`ai-rd-workflow` 作为主控入口。

注意：claude.ai 中各 Skill 相互独立，Skill 间的"调用"由 Claude 按任务自行加载，没有硬编排。上传的 Skill 数量越多，元数据占用上下文越多，按需上传。

## 3. Claude Code 项目级

```bash
python scripts/build_claude_skills.py --layout project
```

写入 `.claude/skills/<skill-name>/`。仅构建部分：`--only code-review test-design`。

Subagent 文件（`.claude/agents/ai-rd-assistant.md`）见 `integration.md`，需手工按 Claude Code frontmatter 转换，本脚本不生成。
