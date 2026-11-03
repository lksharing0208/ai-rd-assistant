# ai-rd-assistant
AI研发助手



my-skill/
├── SKILL.md                  # 必须：Skill 主文件，包含元数据和执行指令
├── scripts/                  # 可选：可执行脚本
│   ├── validate.py
│   └── execute.sh
├── references/               # 可选：参考文档
│   ├── architecture.md
│   └── development-guide.md
├── assets/                   # 可选：模板、静态资源
│   ├── templates/
│   └── examples/
└── agents/                   # 可选：Agent 配置
    └── openai.yaml           # OpenAI 专属配置（外观、依赖等）
