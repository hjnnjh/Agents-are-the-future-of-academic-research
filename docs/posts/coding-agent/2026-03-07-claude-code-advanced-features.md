---
title: "Claude Code 进阶功能速览"
date: 2026-03-07
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - worktree
  - agent-teams
  - remote-control
difficulty: intermediate
summary: "Claude Code 远不止于代码编辑。本文速览 Git Worktree 并行开发、Agent Teams 多实例协作、Remote Control 移动端控制等进阶功能，并附上官方文档入口，供读者按需深入。"
featured: false
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

# Claude Code 进阶功能速览

::: info 本文概览

- 🎯 **目标读者**：已熟悉 Claude Code 基础用法，希望了解更多能力边界的用户
- ⏱️ **阅读时间**：约 10 分钟
- 📚 **知识要点**：Git Worktree 并行开发、Agent Teams 协作、Remote Control、其他值得关注的功能
:::

前面几篇文章覆盖了 Claude Code 的记忆系统、MCP、Subagent、Skills、Hooks。Claude Code 还有不少其他功能，本文挑几个值得了解的做个速览，感兴趣可以去[官方文档](https://code.claude.com/docs/zh-CN/)看完整介绍。

---

## Git Worktree：并行开发的基础设施

多个 Claude 会话同时修改同一套文件，必然产生冲突。Git Worktree 可以解决这个问题——它允许同一仓库拥有多个独立工作目录，各自对应独立的 Git 分支，但共享同一份历史记录。

Claude Code 原生集成了 Worktree 支持。最简单的用法：

```bash
# 在独立 worktree 中启动 Claude（自动创建分支 worktree-feature-auth）
claude --worktree feature-auth

# 同时在另一个终端处理 bug 修复，完全不冲突
claude --worktree hotfix-login-500
```

Worktree 目录默认创建在 `.claude/worktrees/<name>/`，建议将其加入 `.gitignore`。

退出会话时，Claude Code 会根据是否有变更决定如何处理：无变更则自动清理，有变更则提示保留或丢弃。

Worktree 和 Subagent 组合使用效果很好：在自定义 Subagent 的 frontmatter 中设置 `isolation: worktree`，每个 Subagent 就会在独立的 Worktree 中运行，并行修改文件而互不干扰：

```yaml
---
name: feature-developer
description: 并行开发新功能的专用 agent
isolation: worktree
---
```

也可以直接告诉 Claude："请使用 worktrees 让 agents 并行工作"，Claude 会自动安排。

---

## Agent Teams：多实例协作（实验性）

::: warning 实验性功能
Agent Teams 目前是实验性功能，默认关闭，API 和行为可能变化。
:::

Subagent 是在主会话的子上下文中运行的；Agent Teams 走得更远——每个 Teammate 是完全独立的 Claude Code 实例，有自己的上下文窗口，Teammate 之间可以直接互发消息。

启用方式：

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
# 或在 settings.json 中配置
```

启用后，直接用自然语言组建团队：

```
创建一个 agent 团队审查这个 PR。派生三名审查者：
一名专注安全影响，一名检查性能，一名验证测试覆盖率。
```

Claude（作为 Team Lead）会自动创建共享任务列表、派生 Teammate 会话、协调工作并汇总结果。Teammate 之间的任务认领使用文件锁机制防止竞争。

**与 Subagent 的区别**：

| 维度 | Subagent | Agent Teams |
|------|----------|------------|
| 运行方式 | 主会话的子上下文 | 完全独立的 Claude Code 实例 |
| 队员间通信 | 不支持 | 支持直接互发消息 |
| 适用场景 | 并行完成独立任务 | 需要讨论、辩论、互相验证的复杂任务 |
| 稳定性 | 稳定 | 实验性 |

典型场景：多角度代码审查、多假设并行调试（让 Agent 互相质疑对方的结论）、前后端并行开发。

---

## Remote Control：用手机控制你的 Claude

在办公室启动了一个重构任务，但需要去开会或通勤——Remote Control 让你用手机（通过 Claude App 或 `claude.ai/code`）继续控制本地运行的 Claude Code 会话。

::: info
注意：Claude Code 进程始终运行在你的本地机器上，远程设备只是一个"窗口"。这与"云端运行"的 Claude Code on the Web 不同。
:::

启动方式：

```bash
# 方法一：直接启动远程会话
claude remote-control

# 方法二：在已有会话中启用
/remote-control
# 或简写
/rc
```

执行后终端会显示一个会话 URL 和可选的 QR 码，用手机扫码或直接打开 URL 即可接入。建议先用 `/rename` 给会话起个描述性名字，在多任务管理时便于识别。

几个实际用法：

- 出门前启动大规模测试，路上用手机查看进度
- 会议中发现线上 bug，不需要打开电脑就能让 Claude 修复
- 长时间代码生成任务，远程看看跑到哪了

限制：每个本地会话同时只支持一个远程连接；本地终端必须保持开启；网络中断超过约 10 分钟会话超时，需重新运行命令。目前为 Max 和 Pro 计划用户的功能。

---

## 其他值得关注的功能（速览）

以下是几个值得了解的能力，可按需深入：

### `/batch`：大规模并行变更

Claude Code 内置的 `/batch` 命令可以将大型变更任务（如迁移框架、批量重构）自动分解为多个独立单元，每个单元在独立的 git worktree 中并行执行，最终分别开 PR：

```bash
/batch migrate src/ from class components to hooks
```

适合需要横跨大量文件的重复性变更，是手动多开会话的自动化替代。

### 计划模式（Plan Mode）与 Checkpointing

按 `Shift+Tab` 进入计划模式：Claude 只读不写，先给出完整实施计划供你审阅，批准后才开始执行。

```bash
/rewind   # 或 /checkpoint，双击 Esc
```

`/rewind` 可以将代码和对话回退到之前某个时间点，类似"时光机"。

### 思维深度控制（Effort Level）

Sonnet 4.6 和 Opus 4.6 支持自适应推理，可通过环境变量或 settings.json 控制推理深度：

```bash
export CLAUDE_CODE_EFFORT_LEVEL=low|medium|high
```

在 prompt 或 SKILL.md 中包含关键词 `ultrathink` 可触发单次高强度推理模式。

### Claude Code on the Web + Teleport

无需本地环境，直接在 Anthropic 管理的云端虚拟机上运行 Claude Code：

```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

已启动的云端任务可以通过 `claude --teleport` 拉回本地终端继续操作，会话历史完整保留。

### 任务列表（Task List）

处理复杂多步骤任务时，Claude 会自动创建任务看板跟踪进度。`Ctrl+T` 切换显示，任务状态跨 context compaction 持久化。

---

## 小结

本文介绍的这些功能，有的已经稳定可用（Worktree、Remote Control），有的仍是实验性（Agent Teams），有的可能等你读到这篇文章时已经改了不少。

建议直接看官方文档获取最新信息：

- [Claude Code 官方文档（中文）](https://code.claude.com/docs/zh-CN/)
- [功能更新 Changelog](https://code.claude.com/docs/en/changelog)
- [功能总览](https://code.claude.com/docs/en/features-overview)

迭代速度很快，直接看官方更新比等第三方文章更靠谱。
