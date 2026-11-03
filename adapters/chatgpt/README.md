# ChatGPT Plugin Adapter

本目录定义 ChatGPT Agent Plugin 的平台适配源文件。它不会复制或拆分业务 Skills，而是把统一 Agent 源配置与仓库 Skills 打包成一个插件。

## 源配置映射

| 统一源文件 | ChatGPT 插件包位置 | 用途 |
|---|---|---|
| `agent/instructions.md` | `skills/ai-rd-workflow/references/agent-instructions.md` | 主 Agent 行为指令 |
| `agent/manifest.yaml` | `skills/ai-rd-workflow/references/agent-manifest.yaml` | 任务等级、加载和安全策略 |
| `config/skill-routing.yaml` | `skills/ai-rd-workflow/references/skill-routing.yaml` | 意图与专项 Skill 路由 |
| `docs/LOW-TOKEN-ORCHESTRATION.md` | `skills/ai-rd-workflow/references/low-token-orchestration.md` | 低 Token 编排规范 |
| `adapters/chatgpt/plugin.json` | `plugin.json` | 插件身份、展示名称和默认提示词 |
| `adapters/chatgpt/agents/openai.yaml` | `agents/openai.yaml` | ChatGPT Agent 展示和隐式调用策略 |
| `skills/*/SKILL.md` | `skills/*/SKILL.md` | 专项能力 |

## 构建

在仓库根目录执行：

```bash
python scripts/validate_skills.py
python scripts/validate_chatgpt_plugin.py
python scripts/build_chatgpt_plugin.py
```

默认生成：

`dist/ai-rd-assistant-chatgpt-v1.2.0.zip`

ZIP 直接以 `plugin.json`、`agents/` 和 `skills/` 为根目录，不额外套一层 `api-design/` 或 `ai-rd-assistant/skills/api-design/`。

## 识别规则

- `plugin.json` 的 `extensions.com.openai.interface.displayName` 决定插件显示名称：**AI 研发助手**。
- 根目录 `agents/openai.yaml` 提供 Agent 展示信息、默认提示词和隐式调用策略。
- `skills/ai-rd-workflow/SKILL.md` 是唯一主控工作流入口。
- `skills/<skill-name>/SKILL.md` 是插件内独立能力模块，不是独立插件。
- 统一 Agent 指令通过构建脚本放入主控 Skill 的 `references/`，运行时不需要复制多份业务规则。

## 注意

`agents/openai.yaml` 是 Agent 插件包的可选元数据配置，不等于独立运行进程或工具服务器。实际任务编排由主控 Skill 指令定义；MCP/外部工具只有在插件包显式配置且 Runtime 已授权时才可用。
