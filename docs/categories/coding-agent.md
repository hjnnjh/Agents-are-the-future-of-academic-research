# 💻 Coding Agent 实践

上一章我们讨论了 LLM Agent 的理论基础——它们如何思考、如何记忆、如何协作。但理论终归要落地。当你打开终端，面对一个真实的科研编程任务时，选择哪个 Coding Agent？怎样安装配置？如何让它真正理解你的意图？这些才是决定生产力的关键问题。

本章以 **Claude Code** 为核心，系统介绍从零安装到生产级进阶的完整路径——涵盖环境搭建、核心系统原理、扩展能力配置，以及实际工作流中的进阶用法。

## 本章涵盖的内容

### 🔧 环境搭建与 API 配置（Part 1–4）

- **安装与认证**：macOS / Linux / Windows 各平台安装流程，Anthropic 账号认证与 API 接入
- **zcf 一键初始化**：用 zcf 工具自动完成工作流、MCP 服务、CCR 路由的全套配置
- **CCR 模型路由**：本地代理工具 Claude Code Router，按任务类型将请求分发至不同模型，灵活控制成本与性能
- **Copilot 订阅复用**：通过 copilot-api 本地代理，将 GitHub Copilot 订阅接入 Claude Code

### 🧠 核心系统深度解析

- **记忆系统**：CLAUDE.md 六层层级体系、`@imports` 模块化规则、`.claude/rules/` 目录、跨会话自动记忆 MEMORY.md
- **MCP（Model Context Protocol）**：连接外部工具与数据源的协议原理、`claude mcp add` 配置方式、常用服务推荐
- **Subagent**：内置与自定义 Subagent、并行任务模式、配合 CCR 实现差异化模型路由

### 🚀 扩展能力

- **Skills**：从基础纯文本指令型到含脚本的进阶 Skill，`$ARGUMENTS` 参数、`context: fork` 隔离执行、Skills 组合工作流，以及 openskills、vercel-labs/skills 等 npm 管理工具
- **Hooks**：18 种生命周期事件、确定性脚本触发机制、`UserPromptSubmit` 强制技能评估、`PostToolUse` 代码质量门控

### ⚡ 进阶功能速览

- **Git Worktree**：并行开发的文件隔离基础，配合 Subagent `isolation: worktree` 实现无冲突并行
- **Agent Teams**：多个独立 Claude Code 实例协作，支持队员间直接通信（实验性功能）
- **Remote Control**：用手机或浏览器远程控制本地 Claude Code 会话
- **其他**：Plan Mode、Checkpointing、`/batch` 大规模并行变更、Claude Code on the Web 等

---

无论你是刚接触 Coding Agent 的新手，还是已经在用、希望进一步挖掘潜力的用户，本章都提供可直接落地的操作指南。

## 文章列表

- [Claude Code 介绍与安装 (Part 1)](/posts/coding-agent/2026-02-26-claude-code-intro) — Claude Code 是什么、各平台安装方法、账号认证与第三方 API 接入
- [Claude Code 配置进阶：zcf 工具介绍 (Part 2)](/posts/coding-agent/2026-03-07-claude-code-zcf) — 一键完成 Claude Code 环境初始化，涵盖工作流、MCP 服务、CCR 路由配置
- [Claude Code Router (CCR) 使用指南 (Part 3)](/posts/coding-agent/2026-03-07-claude-code-router) — 本地模型路由代理工具，按任务类型分配不同模型，灵活控制成本与性能
- [将 GitHub Copilot 订阅接入 Claude Code (Part 4)](/posts/coding-agent/2026-03-07-claude-code-copilot-api) — 通过 copilot-api 本地代理复用 Copilot 订阅驱动 Claude Code，附风险说明
- [Claude Code 记忆系统详解](/posts/coding-agent/2026-03-07-claude-code-memory) — CLAUDE.md 六层层级体系、写法最佳实践、@imports 模块化与自动记忆 MEMORY.md
- [MCP：让 Claude Code 连接外部世界](/posts/coding-agent/2026-03-07-claude-code-mcp) — MCP 工作原理、配置命令、常用服务推荐（Context7、Playwright、GitHub 等）
- [Subagent：Claude Code 的并行任务引擎](/posts/coding-agent/2026-03-07-claude-code-subagent) — 内置与自定义 Subagent、并行任务实践、配合 CCR 实现差异化模型路由
- [Claude Code Skills：打造你的专属 AI 技能包](/posts/coding-agent/2026-03-07-claude-code-skills) — 从基础到进阶的 Skill 使用方法，含脚本型 Skill 实例、组合工作流、本项目 14 个 Skills 全览
- [Claude Code Hooks：用确定性保证自动化工作流](/posts/coding-agent/2026-03-07-claude-code-hooks) — Hooks 工作原理、18 个事件类型、项目实例 skill-eval-local.sh 解析、everything-claude-code Hooks 示例
- [Claude Code 进阶功能速览](/posts/coding-agent/2026-03-07-claude-code-advanced-features) — Git Worktree 并行开发、Agent Teams 多实例协作、Remote Control 移动端控制及其他功能速览
