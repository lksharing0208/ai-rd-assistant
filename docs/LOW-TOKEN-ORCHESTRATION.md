# 低 Token Agent 与 Skills 编排规范

## 1. 设计目标
默认使用最少必要上下文完成任务。节省 Token 不得削弱正确性、安全、项目约束和用户明确要求。

## 2. 组件职责
- Agent：唯一主控，识别意图、分配任务、管理上下文、质量门禁和交付。
- Intent Router：选择一个主 Skill 和必要辅助 Skills。
- Skill：承载单一、可复用的专业流程。
- Adapter：将统一定义映射到模型/平台原生上下文和工具格式。
- MCP/Tool：提供外部能力；权限由 Runtime 执行控制。
- Workflow：仅用于多阶段任务，管理顺序、状态和交接。

## 3. 复杂度分级
| 级别 | 任务 | 编排 |
|---|---|---|
| S0 | 简单问答 | 直接回答，0 个专项 Skills |
| S1 | 单一能力 | 1 个主 Skill |
| S2 | 跨模块或需要验证 | 1 个主 Skill + 必要辅助，通常总计 2-3 个 |
| S3 | 全链路或高风险 | 分阶段加载，阶段间传递短摘要 |

## 4. 渐进加载
- L0：读取用户意图、Agent 路由表和已知项目摘要。
- L1：加载主 Skill 的 SKILL.md。
- L2：仅在主 Skill 依赖或质量门禁要求时加载辅助 Skill。
- L3：需要专业细节时再读取 references、模板和更多源码。
- 禁止默认预加载全部 Skills、全部 references 或整个仓库。

## 5. 项目上下文策略
1. 优先使用用户已提供文件和本轮已读取资料。
2. 从项目入口、目录摘要、Diff、符号搜索开始缩小范围。
3. 只读取当前任务直接相关文件及必要上下文。
4. 记录短摘要：项目约定、相关路径、关键符号、已确认事实、未决问题。
5. 后续阶段复用摘要；文件变化或证据不足时才重新读取。
6. 不复制大段源码到阶段交接内容。

## 6. 防重复规则
- 同一文件同一任务只读取一次，除非版本变化或上下文截断。
- 同一个问题由一个主 Skill 负责分析，辅助 Skill 只补充专业检查。
- 不重复执行相同查询、测试或工具调用。
- S3 任务按阶段输出增量结果，不重复汇总全部历史。
- 用户已明确给出的信息不得再次询问。

## 7. 上下文交接格式
阶段之间只传递以下短摘要：
- task：本阶段目标
- facts：确认过的事实
- files：相关文件路径/符号
- decisions：已做决定
- risks：已识别风险
- pending：剩余问题
- next：下一步动作

## 8. 路由参考
| 意图 | 主 Skill | 可能辅助 |
|---|---|---|
| 需求 | requirement-analysis | project-analysis |
| 项目理解 | project-analysis | architecture-design |
| 架构 | architecture-design | project-analysis |
| API | api-design | database-design |
| 数据库 | database-design | api-design |
| 实现 | code-implementation | project-analysis、test-design |
| 重构 | code-refactoring | project-analysis、test-design |
| Review | code-review | project-analysis |
| 测试 | test-design | code-review |
| 文档/Git 交付 | project-delivery | project-analysis、code-review |

## 9. 输出控制
- 默认先给结论，再给必要依据和下一步。
- 只输出与任务相关的文件、风险和验证结果。
- 用户要求完整设计、完整代码或完整文件时，不因 Token 模式省略交付内容。
- 严格区分已执行、已验证、未执行和阻塞。
