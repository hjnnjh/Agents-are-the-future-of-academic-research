---
title: "Claude Code 介绍与安装 (Part 1)"
date: 2026-02-26
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - installation
  - beginner
  - setup
difficulty: beginner
summary: "Claude Code 是 Anthropic 推出的 AI 编程助手，能直接在终端、IDE 和浏览器中读取代码、编辑文件、执行命令。本文带你从零完成安装配置，迈出 Coding Agent 实践的第一步。"
featured: true
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

# Claude Code 介绍与安装 (Part 1)

::: info 本文概览

- 🎯 **目标读者**: 对 Coding Agent 感兴趣、想上手 Claude Code 的入门者
- ⏱️ **阅读时间**: 约 12 分钟
- 📚 **知识要点**: Claude Code 是什么、能做什么、各平台安装方法、账号认证、核心配置文件体系
:::

## 什么是 Claude Code？

在上一章，我们了解了 LLM Agent 的基本概念——它不只是一个聊天机器人，而是一个能**自主规划、调用工具、循环执行**的智能体。那么，当这个 Agent 专门为编程任务而设计时，它会变成什么样子？

**Claude Code** 就是这个问题的答案。

Claude Code 是 Anthropic 推出的 **AI 编程助手**（Agentic Coding Tool）。它不是一个简单的代码补全工具——它能读取你的整个代码库，理解项目结构，编辑文件，执行终端命令，甚至与 Git、IDE 等开发工具深度集成。你只需用自然语言描述需求，它就能帮你完成从代码编写到提交部署的全流程。

用一句话概括：**Claude Code 是你的 AI 结对编程伙伴**。

### Claude Code 的核心能力

| 能力 | 说明 |
|------|------|
| 🧠 **代码理解** | 自动分析整个代码库，理解项目架构、依赖关系和代码逻辑 |
| ✏️ **文件编辑** | 跨文件读写代码，支持创建、修改、重构等操作 |
| 💻 **命令执行** | 直接在终端运行构建、测试、Git 等命令 |
| 🔧 **工具集成** | 通过 MCP 协议连接外部工具和数据源（如 Jira、Slack、数据库） |
| 🌐 **多平台运行** | 终端 CLI、VS Code、JetBrains IDE、桌面应用、浏览器——随处可用 |

## 安装 Claude Code

Claude Code 支持 macOS、Linux 和 Windows 三大平台。下面按平台介绍安装方法。

### 系统要求

在安装之前，确认你的环境满足以下条件：

| 项目 | 要求 |
|------|------|
| **操作系统** | macOS 13.0+ / Windows 10 1809+ / Ubuntu 20.04+ / Debian 10+ |
| **内存** | 4 GB 以上 |
| **网络** | 需要互联网连接 |
| **Shell** | Bash、Zsh、PowerShell 或 CMD |
| **Windows 额外要求** | 需安装 [Git for Windows](https://git-scm.com/downloads/win) |

### macOS / Linux 安装

推荐使用官方原生安装脚本，一行命令搞定：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

如果你使用 Homebrew，也可以通过 Homebrew 安装：

```bash
brew install --cask claude-code
```

::: tip 两种方式的区别
- **原生安装**：自动后台更新，始终保持最新版本（推荐）
- **Homebrew 安装**：不会自动更新，需要手动运行 `brew upgrade claude-code`
:::

### Windows 安装

Windows 下有三种安装方式：

**方式一：PowerShell 安装（推荐）**

首先安装 [Git for Windows](https://git-scm.com/downloads/win)，然后在 PowerShell 中运行：

```powershell
irm https://claude.ai/install.ps1 | iex
```

**方式二：WinGet 安装**

```powershell
winget install Anthropic.ClaudeCode
```

**方式三：CMD 安装**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

::: warning Windows 用户注意
Claude Code 在 Windows 上依赖 Git Bash 来执行命令。如果安装后 Claude Code 找不到 Git Bash，可以在设置中手动指定路径：

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```
:::

### 验证安装

安装完成后，打开终端验证：

```bash
claude --version
```

如果看到版本号输出，说明安装成功。还可以运行更全面的检查：

```bash
claude doctor
```

`claude doctor` 会检查你的安装状态、网络连接、认证配置等，帮助排查潜在问题。

## 核心配置文件

Claude Code 的行为可以通过配置文件来定制。本文先介绍最核心的权限与行为配置文件 `settings.json`，其余配置文件（如 `CLAUDE.md`、MCP 等）将在后续文章中详细讲解。

### settings.json：行为与权限配置

`settings.json` 控制 Claude Code 的运行行为，比如权限策略、环境变量、更新频道等。它有层级体系：

| 层级 | 路径 | 用途 |
|------|------|------|
| **用户级** | `~/.claude/settings.json` | 个人全局偏好 |
| **项目级** | `.claude/settings.json` | 团队共享配置 |
| **项目本地** | `.claude/settings.local.json` | 个人项目配置（自动 gitignore） |

一个实用的 `settings.json` 示例：

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(python *)",
      "Bash(git diff *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "ANTHROPIC_MODEL": "claude-sonnet-4-6"
  }
}
```

这个配置做了三件事：
1. **允许** Claude Code 直接运行 pytest、python 和 git diff，无需每次确认
2. **禁止**读取 `.env` 和 `secrets/` 目录，防止泄露敏感信息
3. 将默认模型设为 Claude Sonnet（速度更快、成本更低）

::: warning 权限规则优先级
deny 规则优先于 allow 规则。即使你允许了 `Read(*)`，只要 deny 了 `Read(./.env)`，Claude Code 就绝对不会读取 `.env` 文件。
:::

## 账号认证

Claude Code 需要付费账号才能使用。目前支持以下几种认证方式：

### 方式一：Claude 订阅账号（推荐）

最简单的方式。如果你已经有 Claude Pro 或 Max 订阅：

1. 在终端运行 `claude`
2. 浏览器会自动打开登录页面
3. 用你的 Claude.ai 账号登录
4. 完成！

![Claude Code 界面演示](/img/coding-agent/claude-code-demo.gif)

*使用 Claude Pro 账号登录后的 Claude Code 交互界面*

::: info 订阅方案
Claude Code 需要 **Pro**（$20/月）或 **Max**（$100/月起）订阅，免费版不包含 Claude Code 功能。具体价格请参考 [Claude 官方定价](https://claude.com/pricing)。
:::

### 方式二：Anthropic Console（API 按量计费）

如果你更倾向按 Token 用量付费：

1. 在 [Anthropic Console](https://console.anthropic.com/) 注册账号
2. 充值 API 额度
3. 运行 `claude`，选择 Console 账号登录

首次登录时，Console 会自动创建一个"Claude Code"工作空间来追踪用量。

### 方式三：第三方 API 服务商（国内推荐）

如果你没有 Anthropic 官方账号，或者希望在国内网络环境下更稳定地使用 Claude Code，可以通过第三方 API 服务商接入。通过这种方式，你不仅可以使用 Claude 原版模型，还能在 Claude Code 中接入其他模型，比如国产大模型（MiniMax-M2.5、GLM-4.7）、Gemini 3.1 Pro、GPT-5.3 Codex 等——只要服务商提供兼容 Anthropic API 格式的接口即可。以下介绍两个主流方案。

**MiniMax**

1. 在 [MiniMax 开发者平台](https://platform.minimaxi.com/user-center/basic-information/interface-key) 注册账号并获取 API Key
2. 编辑 `~/.claude/settings.json`，添加以下配置：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<你的 MiniMax API Key>",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1,
    "ANTHROPIC_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_SMALL_FAST_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.5"
  }
}
```

3. 打开终端运行 `claude` 即可开始使用

更多详情参考 [MiniMax 官方指南](https://platform.minimax.io/docs/coding-plan/claude-code)。

**GLM（智谱清言）**

1. 在 [智谱开放平台](https://open.bigmodel.cn) 注册账号
2. 在 [API Keys 页面](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) 创建 API Key
3. 编辑 `~/.claude/settings.json`，添加以下配置：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<你的智谱 API Key>",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1
  }
}
```

4. 编辑 `~/.claude.json`（注意不是 `settings.json`），添加：

```json
{
  "hasCompletedOnboarding": true
}
```

5. 打开新的终端窗口，运行 `claude` 即可开始使用

GLM 默认模型映射为 GLM-4.7（对应 Sonnet/Opus）和 GLM-4.5-Air（对应 Haiku）。更多详情参考 [GLM 官方指南](https://docs.bigmodel.cn/cn/guide/develop/claude#claude-code)。

::: warning 注意事项
使用第三方 API 服务商前，请确保系统环境变量中**没有**设置 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL`，否则环境变量会覆盖配置文件，导致配置不生效。
:::

::: tip 学术用户建议
对于国内学术用户，推荐使用 **MiniMax** 或 **GLM** 的 API 服务，网络连接更稳定，且支持人民币支付。如果你有海外网络条件，也可以选择 **Claude Pro 订阅**或 **Console API 按量计费**。
:::

## 第一次使用

安装和认证完成后，让我们来跑通第一个完整流程。

### 启动 Claude Code

进入你的项目目录，启动 Claude Code：

```bash
cd /path/to/your/project
claude
```

你会看到一个欢迎界面，显示会话信息和最近的对话记录。

### 基本交互

Claude Code 的交互方式非常直观——直接用自然语言对话即可：

```
这个项目的目录结构是怎样的？
```

```
帮我在 src/utils/ 下创建一个日期格式化工具函数
```

```
运行一下测试看看有没有问题
```

Claude Code 会根据你的指令自动执行对应操作。在修改文件或执行命令之前，它会先展示计划并征求你的确认。

### 常用命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `claude` | 启动交互模式 | `claude` |
| `claude "任务"` | 执行单次任务 | `claude "修复构建错误"` |
| `claude -p "问题"` | 单次查询后退出 | `claude -p "解释这个函数"` |
| `claude -c` | 继续上次对话 | `claude -c` |
| `claude commit` | 创建 Git 提交 | `claude commit` |
| `/help` | 查看帮助 | 在交互模式中输入 |
| `/clear` | 清除对话历史 | 在交互模式中输入 |
| `Ctrl+C` 或 `exit` | 退出 | — |

## IDE 集成

Claude Code 的 IDE 集成分为两种形式：

- **CLI 内部集成**：在 Claude Code 的交互模式中，通过 `/ide` 命令将 CLI 与本地 IDE 建立连接，让 Claude 能够感知当前打开的文件、光标位置、诊断信息等上下文，实现更精准的代码辅助。
- **IDE 插件**：在 IDE 内安装官方扩展，直接在编辑器界面中唤起 Claude Code，支持内联 Diff 预览、`@` 提及文件等可视化功能。

### CLI 内部集成（`/ide` 命令）

在交互模式中输入 `/ide`，即可选择要连接的 IDE：

![/ide 命令界面](/img/coding-agent/ide-extension.png)

连接成功后，Claude Code 可以读取 IDE 中当前打开的文件和选中内容，无需手动复制粘贴代码片段。

### VSCode / Cursor

1. 打开 VSCode，进入扩展市场（`Cmd+Shift+X`）
2. 搜索 "Claude Code"
3. 安装 Anthropic 官方扩展
4. 打开命令面板（`Cmd+Shift+P`），输入 "Claude Code"，选择 **Open in New Tab**

![VSCode 扩展界面](/img/coding-agent/vscode-extension.png)

VSCode/Cursor 扩展支持内联 Diff 预览、`@` 提及文件、方案审查等功能，体验比纯终端更加直观。此外，插件还支持**选中内容精确引用**：在编辑器中选中代码片段后，按 `Option+K`（macOS自定义快捷键）即可将选中内容直接引用到对话中，无需手动复制，让上下文传递更加精准高效。

### JetBrains IDE

支持 IntelliJ IDEA、PyCharm、WebStorm 等全系 JetBrains IDE：

1. 打开 Settings → Plugins → Marketplace
2. 搜索 "Claude Code"
3. 安装并重启 IDE

### 桌面应用

如果你不习惯终端操作，Anthropic 还提供了独立的桌面应用：

- **macOS**: 从[官方下载页](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect)下载 DMG 安装
- **Windows**: 从[官方下载页](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect)下载安装程序

桌面应用支持可视化 Diff 审查、多会话并行等功能。

## 更新与卸载

### 更新

- **原生安装**：自动后台更新，无需手动操作。也可以手动触发：`claude update`
- **Homebrew**：`brew upgrade claude-code`
- **WinGet**：`winget upgrade Anthropic.ClaudeCode`

### 卸载

**macOS / Linux（原生安装）**：

```bash
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Homebrew**：

```bash
brew uninstall --cask claude-code
```

**WinGet**：

```powershell
winget uninstall Anthropic.ClaudeCode
```

如需清除配置文件（设置、会话历史等）：

```bash
rm -rf ~/.claude
rm ~/.claude.json
```

## 小结

本文介绍了 Claude Code 的核心定位、安装配置和配置体系：

- **Claude Code 是什么**：一个能理解代码库、编辑文件、执行命令的 AI 编程助手
- **安装方法**：macOS/Linux 一行命令，Windows 需要先装 Git for Windows
- **账号认证**：支持 Claude 订阅、Console API、第三方 API 服务商（MiniMax、GLM）三种方式
- **核心配置**：`settings.json` 控制权限和行为（更多配置文件将在后续文章介绍）
- **基本使用**：用自然语言描述需求，Claude Code 自动执行

安装完成后，你就拥有了一个强大的 AI 编程伙伴。下一篇文章，我们将深入介绍 Claude Code 的核心配置文件 `CLAUDE.md` 以及进阶使用技巧。

::: tip 下一步
后续文章将深入介绍 Claude Code 的日常使用技巧、CLAUDE.md 配置、MCP 集成等进阶内容，敬请期待。
:::

## 参考资料

- [Claude Code 官方文档](https://code.claude.com/docs/en/overview)
- [Claude Code 快速入门](https://code.claude.com/docs/en/quickstart)
- [Claude Code 安装指南](https://code.claude.com/docs/en/getting-started)
- [Claude 订阅方案](https://claude.com/pricing)
- [MiniMax Claude Code 接入指南](https://platform.minimax.io/docs/coding-plan/claude-code)
- [GLM Claude Code 接入指南](https://docs.bigmodel.cn/cn/guide/develop/claude#claude-code)
