# Claude 适配：两套方案

| | 方案 A：claude.ai / Desktop | 方案 B：Claude Code |
|---|---|---|
| 主 Agent | 无 Agent 概念，用 Project Instructions 代替 | `agents/ai-rd-assistant.md` 子代理 |
| Skills 导入 | 逐个上传 ZIP | 插件一次安装 12 个 |
| 构建脚本 | `scripts/build_claude_skills.py` | `scripts/build_claude_plugin.py` |
| 编排 | Claude 按 description 自动触发，Skills 相互独立 | 同左，另有子代理承载主控指令 |

两套方案共用 `skills/*` 作为唯一源文件。构建前先运行 `python scripts/validate_skills.py`。构建时检查：name 小写连字符且 ≤64 字符、不含 `anthropic`/`claude`；description 1–1024 字符；不含 XML 标签。

## 方案 A：claude.ai / Claude Desktop

```bash
python scripts/build_claude_skills.py
```

输出 `dist/claude-skills/`：12 个 `<skill>.zip`（根目录仅一个 `<skill>/` 文件夹）和 `PROJECT-INSTRUCTIONS.md`。

1. Settings → Capabilities，开启 Code execution and file creation 与 Skills。
2. Skills → Upload skill，上传 ZIP。至少 `ai-rd-workflow.zip`、`intent-router.zip`，其余按需（上传越多，元数据占用上下文越多）。
3. 新建 Project，把 `PROJECT-INSTRUCTIONS.md` 全文粘贴到 Project Instructions，在该 Project 中做研发任务。

限制：claude.ai 不能整包导入 Agent，Skills 之间无硬编排。

## 方案 B：Claude Code 插件

仓库根目录即插件：`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`agents/ai-rd-assistant.md`、`skills/`。修改 `skills/` 或 `agent/` 后重新生成并提交：

```bash
python scripts/build_claude_plugin.py
```

安装（用户侧）：

```
/plugin marketplace add lksharing0208/ai-rd-assistant
/plugin install ai-rd-assistant@ai-rd-assistant
```

本地测试：`/plugin marketplace add ./`。

仅需项目级 Skills（无子代理）：`python scripts/build_claude_skills.py --layout project`，写入 `.claude/skills/`。
