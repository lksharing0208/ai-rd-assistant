# ai-rd-assistant
AI研发助手
# AI Skill 标准目录结构规范

**文档名称：** AI Skill 标准目录结构规范  
**文档版本：** v1.0  
**适用范围：** ChatGPT、Claude、Gemini、DeepSeek、Qwen 等 AI 平台  
**文档类型：** 技术规范

---

## 1. 设计目标

建立统一、标准化、可复用的 Skill 目录结构，支持不同 AI 模型和 Agent 平台共享核心 Skill 能力。

设计目标：

1. 统一 Skill 文件组织结构。
2. 统一 Skill 元数据和指令规范。
3. 支持独立 Skill，相互引用和组合调用。
4. 支持脚本执行和自动化任务。
5. 支持参考文档和资源文件管理。
6. 支持不同 AI 平台的配置适配。
7. 支持 Skill 的独立开发、测试、维护和版本管理。
8. 支持跨模型迁移和复用。

核心原则：

**核心指令统一、业务能力独立、资源按需加载、平台配置隔离。**

---

## 2. 标准目录结构

### 2.1 基础目录结构

```text
my-skill/
├── SKILL.md                  # 必须：Skill 主定义文件
├── scripts/                  # 可选：可执行脚本
│   ├── validate.py
│   └── execute.sh
├── references/               # 可选：参考文档
│   ├── architecture.md
│   └── development-guide.md
├── assets/                   # 可选：模板和静态资源
│   ├── templates/
│   └── examples/
└── agents/                   # 可选：平台专属配置
    └── openai.yaml
```

### 2.2 目录定义

| 目录/文件 | 是否必须 | 主要职责 |
|---|---|---|
| `SKILL.md` | 必须 | Skill 元数据、能力定义、执行指令 |
| `scripts/` | 可选 | 自动化脚本、数据处理、校验程序 |
| `references/` | 可选 | 技术规范、业务文档、知识资料 |
| `assets/` | 可选 | 模板、配置样例、静态资源 |
| `agents/` | 可选 | AI 平台专属配置 |
| `agents/openai.yaml` | 可选 | OpenAI 平台展示信息及依赖配置 |

---

## 3. SKILL.md 文件规范

### 3.1 文件职责

`SKILL.md` 是 Skill 的核心定义文件，负责：

- 定义 Skill 身份和能力。
- 声明 Skill 触发条件。
- 定义输入和输出。
- 约束执行流程。
- 定义业务规则。
- 引用其他 Skill 和参考资料。
- 规定异常处理机制。

### 3.2 标准文件结构

```markdown
---
name: my-skill
description: >
  Skill 功能描述。
  明确适用场景、触发条件和核心能力。
---

# My Skill

## 1. 角色定位

定义当前 Skill 的职责和能力边界。

## 2. 触发条件

定义什么情况下需要调用当前 Skill。

## 3. 输入要求

定义执行任务所需的输入信息。

## 4. 执行流程

定义标准执行步骤。

## 5. 执行规范

定义执行过程中的业务规则和技术约束。

## 6. 输出要求

定义最终交付内容及格式。

## 7. 异常处理

定义输入缺失、执行失败和异常情况的处理方式。

## 8. Skill 引用

定义需要协作调用的其他 Skill。

## 9. 参考资料

引用 references/ 中的相关文档。
```

### 3.3 元数据规范

| 字段 | 必须 | 说明 |
|---|---|---|
| `name` | 是 | Skill 唯一名称 |
| `description` | 是 | Skill 功能及触发条件描述 |

命名规则：

- 使用小写英文。
- 单词之间使用 `-`。
- 名称具有明确业务含义。
- 同一 Skill 体系内不得重复。

示例：

```yaml
---
name: intent-router
description: >
  负责识别用户意图、判断任务类型、
  选择对应角色和 Skill 执行链路。
---
```

---

## 4. scripts 目录规范

### 4.1 目录职责

`scripts/` 用于存放 Skill 执行过程中需要调用的程序。

适用场景：

- 文件处理。
- 数据转换。
- 数据校验。
- 自动化执行。
- API 调用。
- 代码分析。
- 测试执行。

### 4.2 目录结构

```text
scripts/
├── validate.py
├── execute.py
├── parser.py
└── utils.py
```

### 4.3 开发规范

1. 脚本应具有明确的功能边界。
2. 避免将大量业务规则直接写入脚本。
3. 支持必要的参数输入。
4. 统一异常处理。
5. 明确执行结果和错误信息。
6. 不得在脚本中硬编码密码、Token 等敏感信息。
7. 必须在 SKILL.md 中说明脚本用途和调用方式。

---

## 5. references 目录规范

### 5.1 目录职责

`references/` 用于存放 Skill 执行所需的知识文档和规范资料。

适用场景：

- 技术架构说明。
- 业务规则。
- 开发规范。
- API 文档。
- 数据库规范。
- 设计标准。
- 操作手册。

### 5.2 目录结构

```text
references/
├── architecture.md
├── development-guide.md
├── business-rules.md
├── api-reference.md
└── examples.md
```

### 5.3 引用规范

在 `SKILL.md` 中使用相对路径引用：

```markdown
## 参考资料

执行任务前，根据实际需要读取：

- `references/architecture.md`
- `references/development-guide.md`
- `references/business-rules.md`
```

规范要求：

1. 参考资料与 Skill 核心指令分离。
2. 避免重复维护相同内容。
3. 使用相对路径。
4. 按任务需要加载资料。
5. 保持文档内容与 Skill 版本一致。

---

## 6. assets 目录规范

### 6.1 目录职责

`assets/` 用于存放 Skill 执行过程中需要使用的静态资源。

### 6.2 目录结构

```text
assets/
├── templates/
│   ├── requirement-template.md
│   └── report-template.md
├── examples/
│   ├── input-example.json
│   └── output-example.json
└── config/
    └── default-config.yaml
```

### 6.3 使用规范

- 模板文件与执行逻辑分离。
- 示例文件用于输入输出参考。
- 配置文件不得包含敏感信息。
- 静态资源使用相对路径引用。

---

## 7. agents 目录规范

### 7.1 目录职责

`agents/` 用于存放特定 AI 平台所需的适配配置。

核心原则：

**Skill 核心能力不依赖特定模型，平台差异通过适配配置处理。**

### 7.2 目录结构

```text
agents/
├── openai.yaml
├── claude.yaml
├── gemini.yaml
└── deepseek.yaml
```

以上文件仅作为跨平台扩展设计示例，不代表所有平台均原生支持这些配置文件。

### 7.3 OpenAI 配置示例

```yaml
interface:
  display_name: "My Skill"
  short_description: "Skill 功能简介"
  default_prompt: "使用当前 Skill 完成指定任务"

dependencies:
  tools: []
```

注意：

`agents/openai.yaml` 属于平台适配配置，不替代 `SKILL.md`，具体字段以目标平台的实际规范为准。

---

## 8. Skill 之间的引用规范

### 8.1 设计原则

多个 Skill 可以通过明确的调用规则组成完整工作流。

例如：

```text
intent-router
      |
      v
requirement-analysis
      |
      v
architecture-design
      |
      v
code-implementation
      |
      v
code-review
      |
      v
test-design
```

### 8.2 引用方式

在 Skill 的 `SKILL.md` 中声明协作关系：

```markdown
## Skill 协作

根据任务类型调用以下 Skill：

- intent-router：负责用户意图识别。
- requirement-analysis：负责需求分析。
- architecture-design：负责架构设计。
- code-implementation：负责代码实现。
- code-review：负责代码审查。
- test-design：负责测试设计。

调用约束：

1. 仅调用与当前任务相关的 Skill。
2. 不重复执行已经完成的工作。
3. 明确上下游输入输出。
4. 共享必要的任务上下文。
5. 避免循环引用。
6. 当前 Skill 无法完成的任务交由对应 Skill 处理。
```

注意：文件中声明引用关系不等于自动执行。实际调用需要由 Agent、平台编排器或运行环境负责。

---

## 9. 完整 Skill 项目结构

推荐采用以下结构组织大型 Skill 项目：

```text
skills/
│
├── intent-router/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── intent-classifier.py
│   ├── references/
│   │   └── intent-rules.md
│   ├── assets/
│   │   └── intent-mapping.yaml
│   └── agents/
│       └── openai.yaml
│
├── requirement-analysis/
│   ├── SKILL.md
│   ├── references/
│   │   └── requirement-template.md
│   └── assets/
│       └── requirement-template.md
│
├── architecture-design/
│   ├── SKILL.md
│   ├── references/
│   │   └── architecture-standard.md
│   └── assets/
│       └── architecture-template.md
│
├── code-implementation/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── code-validator.py
│   └── references/
│       └── development-guide.md
│
├── code-review/
│   ├── SKILL.md
│   └── references/
│       └── review-checklist.md
│
└── test-design/
    ├── SKILL.md
    └── references/
        └── test-standard.md
```

---

## 10. 跨模型兼容规范

### 10.1 文件兼容性

| 文件类型 | ChatGPT | Claude | 统一设计建议 |
|---|---|---|---|
| SKILL.md | 支持对应 Skill 规范 | 支持对应 Skill 规范 | 统一核心内容 |
| scripts/ | 取决于执行环境 | 取决于执行环境 | 统一脚本 |
| references/ | 支持按需读取 | 支持按需读取 | 统一文档 |
| assets/ | 取决于平台加载能力 | 取决于平台加载能力 | 统一资源 |
| agents/openai.yaml | OpenAI 专属配置 | 不通用 | 平台隔离 |

### 10.2 统一设计方案

采用：

```text
统一 Skill 核心规范
        |
        v
    SKILL.md
        |
        +----------------+
        |                |
        v                v
    scripts/         references/
        |                |
        +-------+--------+
                |
                v
          assets/
                |
                v
        平台适配配置
                |
       +--------+--------+
       |        |        |
       v        v        v
    ChatGPT  Claude   Gemini
```

设计要求：

1. 业务规则统一。
2. 核心指令统一。
3. 文件结构统一。
4. 平台专属能力独立适配。
5. 不将特定平台工具调用语法写入通用业务规则。
6. 平台不支持的功能通过适配层处理。

---

## 11. Skill 质量管理规范

每个 Skill 应满足以下要求：

| 检查项 | 检查要求 |
|---|---|
| 元数据 | 必须包含 name、description |
| 命名 | 符合统一命名规范 |
| 职责 | 具有明确的能力边界 |
| 触发条件 | 能够明确判断适用场景 |
| 输入 | 定义必要输入信息 |
| 输出 | 定义交付格式 |
| 执行流程 | 具有完整执行步骤 |
| 引用 | 引用路径正确 |
| 脚本 | 脚本可执行、异常可处理 |
| 安全 | 不包含明文敏感信息 |
| 兼容性 | 不依赖未声明的平台专属能力 |

---

## 12. 最终标准

统一 Skill 体系遵循以下标准：

| 规范 | 标准要求 |
|---|---|
| 核心文件 | SKILL.md |
| 元数据 | YAML Frontmatter |
| 文件格式 | Markdown、YAML、JSON、Python、Shell |
| 目录结构 | scripts、references、assets、agents |
| 文件引用 | 相对路径 |
| Skill 命名 | 小写英文 + 连字符 |
| 能力划分 | 一个 Skill 聚焦一类职责 |
| Skill 协作 | 显式声明、由 Agent 编排 |
| 模型适配 | 核心统一、配置隔离 |
| 资源加载 | 按需加载 |
| 质量管理 | 标准化校验 |

### 最终设计原则

1. 一个 Skill 只负责一类明确的业务能力。
2. SKILL.md 是 Skill 的核心入口。
3. scripts 存放执行代码。
4. references 存放知识和规范。
5. assets 存放模板和静态资源。
6. agents 存放平台适配配置。
7. Skill 之间通过明确的接口和调用规则协作。
8. Agent 负责意图识别、任务拆分和 Skill 调度。
9. 不同 AI 模型复用统一的 Skill 核心内容。
10. 平台差异由适配层处理。

**最终采用：一套 Skill 核心规范 + 多平台适配配置 + Agent 统一调度的架构。**


---

## 13. AI 研发助手 Agent 与低 Token 编排

本项目使用统一主 Agent + Intent Router + 专项 Skills 组织研发能力。默认启用低 Token 模式：先识别意图，再加载一个主 Skill；只有任务需要时才加载辅助 Skill、references 和模板。

### 13.1 统一 Agent 源文件
- `agent/manifest.yaml`：任务等级、路由策略、上下文和安全策略。
- `agent/instructions.md`：模型无关的主 Agent 指令。
- `config/skill-routing.yaml`：意图到主/辅助 Skill 的映射。

### 13.2 任务等级
| 等级 | 任务 | 默认编排 |
|---|---|---|
| S0 | 简单问答 | 直接回答，不加载专项 Skill |
| S1 | 单一研发任务 | 1 个主 Skill |
| S2 | 跨模块/需要验证 | 1 个主 Skill + 必要辅助，通常不超过 3 个 |
| S3 | 全链路/高风险任务 | 分阶段按需加载，阶段间传递短摘要 |

### 13.3 Skills 路由
| 任务 | 主 Skill |
|---|---|
| 意图识别 | intent-router |
| 需求分析 | requirement-analysis |
| 项目源码理解 | project-analysis |
| 架构设计 | architecture-design |
| API 设计 | api-design |
| 数据库设计 | database-design |
| 代码实现 | code-implementation |
| 代码重构 | code-refactoring |
| 代码审查 | code-review |
| 测试设计 | test-design |
| 文档/Git 交付 | project-delivery |

### 13.4 低 Token 约束
1. 不预加载全部 Skills、references 或整个仓库。
2. 先按意图选一个主 Skill，再按依赖加载辅助 Skill。
3. 标准任务通常最多加载 3 个 Skills。
4. 优先按路径、符号、Diff 和短摘要读取上下文。
5. 同一文件、查询和分析结果不得无故重复处理。
6. 复杂任务分阶段执行，只传递 facts、files、decisions、risks、pending 等短摘要。
7. Token 优化不能跳过必要的测试、安全检查、项目规范或用户要求。

### 13.5 平台适配
统一能力定义放在 `agent/` 和 `skills/`；平台差异放在 `adapters/`。适配说明不等于平台原生可执行配置，具体运行仍需目标 Runtime 提供对应工具和权限。

### 13.6 校验
在仓库根目录执行：

```bash
python scripts/validate_skills.py
```

该脚本检查 Skill Front Matter、名称与目录一致性、重复名称和 description。

详细规范见：
- `docs/LOW-TOKEN-ORCHESTRATION.md`
- `docs/SKILL-GENERATION-RULES.md`

---

## 14. ChatGPT Plugin Adapter（单一插件 + 单主 Agent + 多 Skills）

本项目通过 `adapters/chatgpt/` 将统一 Agent 源配置转换为 ChatGPT 可识别的单一插件包。插件显示名称固定为 **AI 研发助手**，主控工作流为 `ai-rd-workflow`，其余 `skills/*` 均作为同一插件内的专项能力，不分别创建插件。

### 14.1 核心文件

- `adapters/chatgpt/plugin.json`：插件身份、版本、展示名称和默认提示词模板。
- `adapters/chatgpt/agents/openai.yaml`：ChatGPT Agent 展示信息、默认提示词和隐式调用策略。
- `skills/ai-rd-workflow/SKILL.md`：唯一主控 Agent 工作流。
- `skills/<name>/SKILL.md`：专项 Skills。
- `scripts/validate_chatgpt_plugin.py`：插件 Adapter 校验。
- `scripts/build_chatgpt_plugin.py`：生成单一 ChatGPT 插件 ZIP。

### 14.2 构建命令

在仓库根目录执行：

```bash
python scripts/validate_skills.py
python scripts/validate_chatgpt_plugin.py
python scripts/build_chatgpt_plugin.py
```

默认输出：`dist/ai-rd-assistant-chatgpt-v1.2.0.zip`。

ZIP 根目录必须直接包含 `plugin.json`、`agents/openai.yaml` 和 `skills/`，不得只压缩单个 Skill 目录。构建时会将统一 Agent 源配置复制到主控 Skill 的 `references/`，确保包内引用完整。

详细说明见 `docs/CHATGPT-PLUGIN-ADAPTER.md` 和 `adapters/chatgpt/README.md`。
