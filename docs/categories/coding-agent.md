# 💻 Coding Agent 实践

上一章我们讨论了 LLM Agent 的理论基础——它们如何思考、如何记忆、如何协作。但理论终归要落地。当你打开终端，面对一个真实的科研编程任务时，选择哪个 Coding Agent？怎样安装配置？如何让它真正理解你的意图？这些才是决定生产力的关键问题。

本章聚焦于**实际操作**。我们将以 Claude Code、OpenCode 等主流 Coding Agent 为对象，从零开始，手把手带你走完从安装到精通的全过程。

## 本章涵盖的内容

### 🔧 环境搭建与基础配置

- **下载与安装**：各平台（macOS / Linux / Windows）的安装流程与常见问题排查
- **接入第三方 API**：如何在Claude Code/OpenCode中配置 Anthropic、OpenAI、OpenRouter 等不同的 API Providers，以及一些进阶配置方法（比如模型路由工具Claude Code Router的使用方法）
- **开发环境集成**：与 VS Code、JetBrains IDE、Neovim 等编辑器的协同配置

### 📖 基础使用方法

- **核心交互模式**：自然语言指令、代码生成、文件编辑、终端命令执行
- **项目上下文管理**：`CLAUDE.md`、`AGENTS.md` 等配置文件的编写技巧，让 Agent 真正理解你的项目
- **常用工作流**：代码编写、Bug 修复、代码审查、Git 操作等日常场景的最佳实践

### 🚀 进阶使用技巧

- **MCP（Model Context Protocol）**：连接外部工具与数据源，让 Agent 的能力边界不再局限于代码编辑
- **多 Agent 编排**：利用 Sub-agent、Worktree 等机制并行处理复杂任务
- **Hooks 与自动化**：通过事件钩子实现自动格式化、自动测试等流水线式操作
- **Agent Skills 与自定义指令**：如何通过 Skills 扩展 Agent 能力，打造专属工作流

### 🔬 学术科研场景实战

- **数据处理与分析**：用 Coding Agent 快速编写数据清洗、统计分析、可视化脚本
- **论文辅助工具开发**：构建文献管理、实验记录、结果可视化等研究工具
- **实验自动化**：从参数扫描到结果收集，用 Agent 搭建端到端的实验流水线

### ⚖️ 工具对比与选型

- **Claude Code vs Cursor vs OpenCode**：功能特性、使用体验、适用场景的横向对比
- **API 模型选择指南**：不同模型（Claude Opus / Sonnet / Haiku、GPT、Gemini）在编程任务中的表现差异
- **成本与效率权衡**：Token 用量优化、模型降级策略、本地模型方案

---

无论你是刚接触 Coding Agent 的新手，还是想要进一步挖掘其潜力的资深用户，本章都将为你提供可直接落地的操作指南。

## 文章列表

- [Claude Code 介绍与安装 (Part 1)](/posts/coding-agent/2026-02-26-claude-code-intro) — Claude Code 是什么、各平台安装方法、账号认证与第三方 API 接入
- [Claude Code 配置进阶：zcf 工具介绍 (Part 2)](/posts/coding-agent/2026-03-07-claude-code-zcf) — 一键完成 Claude Code 环境初始化，涵盖工作流、MCP 服务、CCR 路由配置
- [Claude Code Router (CCR) 使用指南 (Part 3)](/posts/coding-agent/2026-03-07-claude-code-router) — 本地模型路由代理工具，按任务类型分配不同模型，灵活控制成本与性能
- [将 GitHub Copilot 订阅接入 Claude Code (Part 4)](/posts/coding-agent/2026-03-07-claude-code-copilot-api) — 通过 copilot-api 本地代理复用 Copilot 订阅驱动 Claude Code，附风险说明
