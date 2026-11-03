# ChatGPT Plugin Adapter 设计与打包规范

## 1. 目标

在不改变统一 Agent 源配置和业务 Skills 的前提下，生成 ChatGPT 可识别的单一插件包。

采用：

```text
统一 Agent 源配置
  agent/manifest.yaml
  agent/instructions.md
          |
          v
ChatGPT Plugin Adapter
  adapters/chatgpt/plugin.json
  adapters/chatgpt/agents/openai.yaml
          |
          v
单一 AI 研发助手插件
  plugin.json
  agents/openai.yaml
  skills/ai-rd-workflow/SKILL.md
  skills/<specialized-skill>/SKILL.md
```

## 2. 三类配置的职责

| 文件 | 职责 | 是否作为插件识别入口 |
|---|---|---|
| `agent/manifest.yaml` | 统一 Agent 的任务等级、Skills 加载、上下文和安全策略 | 否，属于模型无关源配置 |
| `agent/instructions.md` | 统一主 Agent 的行为指令 | 否，由 Adapter 映射到主控 Skill |
| `plugin.json` | 插件唯一标识、版本、描述和 ChatGPT 展示信息 | 是，必须位于 ZIP 根目录 |
| `agents/openai.yaml` | Agent 展示信息、默认提示词和隐式调用策略 | 是，Agent 元数据入口 |
| `skills/ai-rd-workflow/SKILL.md` | 唯一主控工作流：意图识别、任务分级、路由和阶段管理 | 是，主控指令入口 |
| `skills/<name>/SKILL.md` | 独立专项能力 | 否，属于同一插件中的多个 Skills |

插件名由 `plugin.json` 的 OpenAI interface.displayName 决定；Skill 名由对应 SKILL.md 的 frontmatter.name 决定。不能把专项目录直接当作完整插件上传。

## 3. 单主 Agent 与 Skills

本项目只配置一个主控 Agent：`ai-rd-workflow`。

主控 Agent 负责：
1. 识别研发意图并判断 S0-S3 复杂度。
2. 选择一个主 Skill。
3. 只有必要时加载辅助 Skills，标准任务通常不超过 3 个。
4. 控制分阶段执行、质量门禁和上下文摘要。
5. 汇总并准确交付结果。

`intent-router` 是可复用的意图路由能力，不是另一个主 Agent。其余 Skills 也都只是能力模块，不单独创建插件。

## 4. 文件映射

构建时执行以下映射：

- `agent/instructions.md` → 主控 Skill 的 `references/agent-instructions.md`
- `agent/manifest.yaml` → 主控 Skill 的 `references/agent-manifest.yaml`
- `config/skill-routing.yaml` → 主控 Skill 的 `references/skill-routing.yaml`
- `docs/LOW-TOKEN-ORCHESTRATION.md` → 主控 Skill 的 `references/low-token-orchestration.md`
- `adapters/chatgpt/plugin.json` → 插件根目录 `plugin.json`
- `adapters/chatgpt/agents/openai.yaml` → 插件根目录 `agents/openai.yaml`
- `skills/*` → 插件根目录 `skills/*`

插件包不直接把 `agent/manifest.yaml` 解释为平台原生 Agent，也不依赖它自动注册运行时对象；主控指令通过可识别的 `ai-rd-workflow` Skill 承载。

## 5. ZIP 根目录规范

正确结构：

```text
ai-rd-assistant-chatgpt.zip
├── plugin.json
├── agents/
│   └── openai.yaml
├── README.md
└── skills/
    ├── ai-rd-workflow/
    │   ├── SKILL.md
    │   └── references/
    │       ├── agent-instructions.md
    │       ├── agent-manifest.yaml
    │       ├── skill-routing.yaml
    │       └── low-token-orchestration.md
    ├── intent-router/
    │   └── SKILL.md
    ├── requirement-analysis/
    │   └── SKILL.md
    └── ...
```

必须满足：

1. ZIP 根目录直接包含 `plugin.json`，不能只有 `skills/api-design/`。
2. 根目录必须有 `agents/openai.yaml`，用于暴露 Agent 展示与调用配置。
3. 必须包含 `skills/ai-rd-workflow/SKILL.md` 主控工作流。
4. 所有专项 Skills 放在 `skills/<skill-name>/SKILL.md`。
5. 一个 ZIP 只打包一个插件，不为每个 Skill 创建插件。
6. `plugin.json` 使用 Agent Plugins 1.0 Schema；平台插件通过固定的 `skills/` 目录发现 Skills，不在便携清单中额外声明顶层 `skills`、`mcpServers`、`apps` 或 `interface`。
7. 不打包 Git 元数据、缓存、密钥、虚拟环境和无关目录。

## 6. 构建和验证

```bash
python scripts/validate_skills.py
python scripts/validate_chatgpt_plugin.py
python scripts/build_chatgpt_plugin.py
```

构建脚本会：
- 校验统一 Skill Front Matter。
- 校验 ChatGPT 插件清单和 Agent YAML。
- 校验主控工作流和所有引用源文件。
- 将统一 Agent 源配置映射到主控 Skill references。
- 复制全部专项 Skills，生成一个根目录正确的 ZIP。
- 检查 ZIP 完整性并输出插件名、版本和 Skill 数量。

## 7. 常见识别问题

| 现象 | 常见原因 | 修正 |
|---|---|---|
| 插件名称显示为 `api-design` | 上传的是 `skills/api-design` 目录或单 Skill ZIP | 上传完整插件 ZIP，确保根目录有 `plugin.json` |
| 只看到一个 Skill | ZIP 只包含一个 Skill 目录 | 由构建脚本打包整个 `skills/` |
| 没有 Agent 展示/配置 | 缺少根目录 `agents/openai.yaml` | 使用 Adapter 生成的 Agent 元数据 |
| Agent 有名称但不按流程调度 | 缺少 `ai-rd-workflow` 主控 Skill 或路由指令 | 检查主控 Skill 和引用文件 |
| 提示无可用工具 | 插件只有指令和 Skills，没有 MCP 工具连接 | 仅在需要外部动作时接入真实 MCP 服务 |

## 8. 能力边界

Agent 元数据用于描述 Agent 的展示和调用策略；主控 Skill 承载执行指令；专项 Skills 提供按需能力。单靠 ZIP 不能凭空创建 OpenAI Agents SDK 运行时代象、远程服务或 MCP 工具。需要这些能力时，必须有真实 Runtime、工具实现和授权配置。

当前 Adapter 是 Skills-only ChatGPT 插件，不声明虚构 MCP endpoint，也不打包访问凭证。
