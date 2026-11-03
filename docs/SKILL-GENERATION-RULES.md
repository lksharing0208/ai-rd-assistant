# Agent 与 Skill 生成规则

## Agent
Agent 只定义角色、目标、边界、输入输出、策略和 Skill 编排，不重复写入每个领域的完整 SOP。

## Skill
每个 Skill 只负责一种稳定专业能力，至少包含：
- YAML Front Matter：name、description
- Goal：能力目标
- Procedure：执行步骤
- Rules：约束和禁止事项
- Output / Quality Gates：交付和质量标准

## 低 Token 规则
1. description 应短且清晰，明确触发条件。
2. Skill 正文只保留完成任务所需的核心指令。
3. 长规范、详细示例和大模板放 references/assets，按需读取。
4. Skill 之间声明依赖，不复制彼此正文。
5. 默认一个主 Skill，辅助 Skill 按需加入。
6. 不在 Agent 中重复所有 Skill 的检查清单。
7. 同一文件、问题或工具操作不得无故重复处理。
8. 不因节约 Token 跳过关键规范、测试、安全和授权。

## 跨模型
- SKILL.md 保存模型无关的核心能力。
- 平台差异只写入 adapters/。
- 不在通用 Skill 中硬编码厂商私有 API 或私有工具格式。
- 适配器负责上下文格式、Tool Calling、MCP 和输出 Schema 的映射。

## 质量校验
- frontmatter name 与目录名一致。
- name 唯一，description 非空且可触发。
- 引用路径存在。
- 不包含密钥或个人凭证。
- 用实际任务样例验证路由、加载、输出和边界行为。
