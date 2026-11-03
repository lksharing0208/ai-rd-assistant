---
name: intent-router
description: 当用户提出软件需求、项目分析、架构设计、API/数据库、代码实现、重构、Review、测试、文档或 Git 交付任务时使用；负责低 Token 意图分类、任务分级和专项 Skill 路由。
---

# Intent Router

## 目标
把用户请求映射为一个主 Skill 和必要辅助 Skills，避免无关加载。

## 路由规则
| 意图 | 主 Skill | 辅助 Skill（按需） |
|---|---|---|
| 需求拆解、验收标准 | requirement-analysis | project-analysis（涉及现有系统时） |
| 仓库结构、源码调用链、项目规范 | project-analysis | architecture-design（需要方案时） |
| 架构、模块划分、技术方案 | architecture-design | project-analysis（现状不清楚时） |
| API、请求响应、接口契约 | api-design | database-design（涉及持久化时） |
| DDL、索引、SQL、事务 | database-design | api-design（涉及接口契约时） |
| 新功能、Bug 修复 | code-implementation | project-analysis；test-design（涉及可验证逻辑时） |
| 重构、代码整理 | code-refactoring | project-analysis；test-design |
| Diff / PR 审查 | code-review | project-analysis（项目规范缺失时） |
| 测试计划、测试用例、回归 | test-design | code-review（需审查变更时） |
| 文档生成、Git 交付 | project-delivery | project-analysis（需读取源码时） |

## 任务分级
- S0：简单解释、单点问答。无需加载专项 Skill。
- S1：一个明确能力。只加载一个主 Skill。
- S2：跨模块或需要验证。加载一个主 Skill，按需加载 1-2 个辅助 Skill。
- S3：全链路或高风险任务。分阶段加载，不一次性加载所有 Skills。

## 执行规则
1. 优先遵循用户明确指定的 Skill、阶段、目录和输出格式。
2. 先选主 Skill，再判断辅助 Skill 的必要性。
3. 标准任务最多 3 个 Skills；超过时按阶段拆解并用短摘要交接。
4. 不调用两个 Skills 重复分析同一范围。
5. 仅在涉及现有项目且上下文不足时加载 project-analysis。
6. 不因“完整流程”默认加载所有 Skills；用户明确要求全链路时逐阶段启用。
7. 路由声明不等于自动执行，实际执行依赖当前 Runtime 的加载和工具能力。

## 输出
必要时只说明任务级别、主 Skill、必要辅助 Skill 和本阶段目标；不输出内部分类推理。
