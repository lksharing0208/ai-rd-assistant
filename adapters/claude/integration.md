# Claude / Claude Code Adapter

## 映射原则
本仓库的 Agent Manifest 和 Skills 是统一源文件。Claude Code 运行时文件由此映射生成，不应反向把平台专属字段写入通用 Skill。

## Skills
将仓库中的：
- `skills/<skill-name>/SKILL.md`

映射到 Claude Code 项目级：
- `.claude/skills/<skill-name>/SKILL.md`

保留 Skill 的 YAML Front Matter 和 Markdown 正文。references、scripts、assets 按需复制到对应 Skill 目录，并使用相对路径。

## Agent
将：
- `agent/instructions.md`
- `agent/manifest.yaml`

转换为 Claude Code Subagent 文件：
- `.claude/agents/ai-rd-assistant.md`

生成文件需要 Claude Code 支持的 YAML Front Matter（例如 name、description、model、tools）和 Markdown 指令。不要把本仓库 manifest 的全部字段原样复制到 Claude frontmatter。

## 低 Token 行为
- 由 intent-router 选择 Skill。
- 通过 Skills 字段或 Agent 指令引用专项能力。
- 不预加载全部 references。
- 本地工具权限以 Claude Code settings 和用户授权为准。

## 注意
此文件是适配说明，不是 Claude Code 可直接加载的 Subagent 文件。

## 打包与导入
Skills 的 ZIP 打包（claude.ai 导入）和 `.claude/skills` 安装由 `scripts/build_claude_skills.py` 完成，步骤见 `adapters/claude/README.md`。
