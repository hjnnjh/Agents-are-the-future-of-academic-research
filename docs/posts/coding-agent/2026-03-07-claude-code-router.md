---
title: "Claude Code Router (CCR) 使用指南 (Part 3)"
date: 2026-03-07
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - ccr
  - claude-code-router
  - model-routing
  - configuration
difficulty: intermediate
summary: "Claude Code Router（CCR）是一个本地代理工具，能够将 Claude Code 的请求按规则分发给不同的模型和 API Provider。通过路由规则，你可以让复杂推理任务走高性能模型，让后台任务走廉价本地模型，不需要修改 Claude Code 本体。"
featured: false
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

:::tip 选读
本文为 Part 3 选读内容，适合有一定 Claude Code 使用经验、希望进一步控制模型选择和 API 成本的读者。如果你刚完成基础安装，建议先阅读 [Part 1](/posts/coding-agent/2026-02-26-claude-code-intro) 和 [Part 2](/posts/coding-agent/2026-03-07-claude-code-zcf)。
:::

## CCR 是什么

![CCR banner](/img/coding-agent/ccr-banner.png)

[Claude Code Router](https://github.com/musistudio/claude-code-router)（简称 CCR）是一个运行在本地的透明代理工具。它在 Claude Code 和远端 API 之间插入一层路由层：Claude Code 将请求发送给 CCR 的本地端口（默认 `localhost:3456`），CCR 根据你预设的规则决定将请求转发给哪个模型，再把结果原样返回给 Claude Code。

整个过程对 Claude Code 透明，不需要修改源代码，也不需要用非官方补丁。

CCR 要解决的问题是：Claude Code 默认只用单一模型，但不同任务对模型的要求差异很大。写一个简单函数和做架构推理，用同一个高价模型不划算。CCR 让你可以按需分配：

| 任务类型 | 适合模型 | 典型场景 |
|----------|----------|----------|
| 常规代码编写 | 中等价位模型（如 DeepSeek） | 日常编码、Bug 修复 |
| 后台任务 | 本地模型（如 Ollama） | 文件索引、格式化 |
| 深度推理 | 高性能推理模型 | Plan 模式、架构设计 |
| 超长上下文 | 长上下文专用模型（如 Gemini） | 阅读大型代码库 |

---

## 安装

确保已安装 Claude Code，然后全局安装 CCR：

```bash
npm install -g @musistudio/claude-code-router
```

安装完成后，`ccr` 命令即可使用。

---

## 配置

CCR 的配置文件位于 `~/.claude-code-router/config.json`。下面是一个典型配置：

```json
{
  "API_TIMEOUT_MS": 600000,
  "Providers": [
    {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/chat/completions",
      "api_key": "sk-xxx",
      "models": ["deepseek-chat", "deepseek-reasoner"],
      "transformer": {
        "use": ["deepseek"],
        "deepseek-chat": {
          "use": ["tooluse"]
        }
      }
    },
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "sk-xxx",
      "models": ["google/gemini-2.5-pro-preview", "anthropic/claude-sonnet-4"],
      "transformer": {
        "use": ["openrouter"]
      }
    },
    {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/v1/chat/completions",
      "api_key": "ollama",
      "models": ["qwen2.5-coder:latest"]
    }
  ],
  "Router": {
    "default": "deepseek,deepseek-chat",
    "background": "ollama,qwen2.5-coder:latest",
    "think": "deepseek,deepseek-reasoner",
    "longContext": "openrouter,google/gemini-2.5-pro-preview",
    "longContextThreshold": 60000
  }
}
```

配置分为两个核心部分：

### Providers（供应商）

每个 Provider 代表一个 API 服务，需要配置：

- `name`：供应商标识符
- `api_base_url`：Chat Completions 接口地址
- `api_key`：API 密钥
- `models`：该供应商下可用的模型列表
- `transformer`（可选）：请求/响应格式转换器

**内置 Transformer 一览**

CCR 内置了几种适配器，处理不同供应商的 API 格式差异：

| Transformer | 适用场景 |
|-------------|----------|
| `deepseek` | DeepSeek API 格式适配 |
| `gemini` | Gemini API 格式适配 |
| `openrouter` | OpenRouter API 适配（含 Provider 路由） |
| `tooluse` | 针对特定模型优化 Tool Call |
| `maxtoken` | 设置最大输出 Token 数 |
| `reasoning` | 处理模型返回的 `reasoning_content` 字段 |
| `enhancetool` | 对工具调用参数增加容错处理 |

### Router（路由规则）

路由规则决定了哪类请求走哪个模型，格式为 `"供应商名,模型名"`：

| 路由键 | 含义 |
|--------|------|
| `default` | 默认模型，所有未匹配的请求走这里 |
| `background` | 后台任务，适合使用廉价或本地模型 |
| `think` | 推理任务（Plan 模式），适合使用推理模型 |
| `longContext` | 长上下文任务（超出 `longContextThreshold` token） |
| `webSearch` | 需要联网搜索的任务 |

---

## 启动与使用

配置好后，用 `ccr code` 代替 `claude` 启动 Claude Code：

```bash
ccr code
```

CCR 会在后台启动本地代理服务，然后拉起 Claude Code。修改配置后需要重启：

```bash
ccr restart
```

:::info
如果你希望在当前 Shell 直接用 `claude` 命令（而不是 `ccr code`），可以运行以下命令激活环境变量，让 `claude` 也通过 CCR 路由：

```bash
eval "$(ccr activate)"
```

将这行加入 `~/.zshrc` 或 `~/.bashrc` 可以让配置持久生效。
:::

---

## 动态切换模型

在 Claude Code 会话中，可以用 `/model` 命令临时切换当前使用的模型，无需重启：

```
/model deepseek,deepseek-reasoner
```

格式为 `/model 供应商名,模型名`。任务中途发现需要更强的模型时比较方便。

---

## 管理工具

### Web UI（ccr ui）

如果你不想手动编辑 JSON，可以用内置 Web UI 来管理配置：

```bash
ccr ui
```

命令会打开一个本地网页，提供可视化的配置编辑界面。

### CLI 交互式管理（ccr model）

也可以用交互式 CLI 来查看和切换当前配置的模型：

```bash
ccr model
```

该命令提供菜单式界面，支持查看当前路由配置、切换各路由槽的模型、新增 Provider 和模型，不需要手动编辑 JSON 文件。

---

## 路由切换辅助工具：CCRS

CCR 自带的 `ccr model` 命令能完成大部分配置管理，但如果你需要**在不同路由预设之间快速切换**（比如"全部走官方 Claude"和"按任务分发给多个供应商"两套配置），每次在菜单里逐项调整还是有点麻烦。

为此，笔者写了 [Claude Code Router Switch](https://github.com/hjnnjh/claude-code-router-switch)（CCRS），一个补充 CCR 的轻量管理脚本，主要做路由配置的**预设保存和一键恢复**。

功能包括：

- 格式化表格展示当前路由配置（路由键 / 供应商 / 模型）
- 交互式菜单修改路由，支持整体切换（所有路由槽换同一个模型）和单路由调整
- 预设管理：把当前路由配置保存为快照，随时恢复，不用重新逐项配置
- 自动同步：修改后自动重启 CCR 服务并更新 `~/.claude/settings.json`

**安装：**

```bash
git clone https://github.com/hjnnjh/claude-code-router-switch
cd claude-code-router-switch
chmod +x install.sh && ./install.sh
```

安装完成后，`ccrswitch` 命令即可全局使用：

```bash
ccrswitch
```

如果你维护了多套路由策略（比如科研计算密集时用推理模型，日常编码用轻量模型），预设功能可以在它们之间一键切换，省去重新配置的工作。

---

## 与 zcf 联动

[zcf](/posts/coding-agent/2026-03-07-claude-code-zcf) 集成了 CCR 的管理功能，分两部分：

**一、CCR 服务管理（`npx zcf ccr`）**

zcf 提供了 CCR 管理菜单，包含常用操作：

```bash
npx zcf ccr    # 进入 CCR 管理菜单
# 或：npx zcf 后在主菜单选择 "R. CCR Management"
```

菜单里可以初始化配置、启动/停止/重启服务、打开 Web UI（`http://localhost:3456/ui`）、查看运行状态，把 `ccr start`、`ccr restart`、`ccr ui` 等命令集中到一处。

**二、配置切换（`npx zcf cs`）**

zcf 的配置切换功能内置了"CCR Proxy"作为专属配置类型，与直连官方 API、第三方 Provider 等并列：

```bash
npx zcf cs    # 在菜单中选择 "CCR Proxy" 切换
```

切换操作会更新 `~/.claude/settings.json` 中的 Profile，之后直接运行 `claude` 命令重启 Claude Code 即可生效——**无需使用 `ccr code`**，Claude Code 会自动通过 CCR 代理路由请求。

:::tip
`ccr code` 适合只使用 CCR 的场景（一条命令同时启动服务和 Claude Code）；而 zcf 的配置切换方案更适合在多个 Provider 之间灵活切换，在需要 CCR 时切过去，不需要时随时切回官方 API。
:::

---

## 对学术科研用户的价值

成本控制方面，论文数据分析脚本的编写往往不需要动用最贵的 Claude Opus。把 `default` 路由设为 DeepSeek 或其他性价比高的模型，遇到复杂架构问题再临时切换，API 开销能降不少。

`background` 路由可以指向 Ollama 运行的本地模型，让文件索引、格式化等轻量后台任务零成本运行。`longContext` 路由在处理大型代码库或长文档时自动切换至 Gemini 等支持百万 Token 上下文的模型，避免截断导致的分析偏差。`think` 路由配合 DeepSeek R1 或其他推理模型，Plan 模式下的架构设计和复杂调试会有更充分的推理过程。

---

## 小结

CCR 是一个轻量的路由层，让你对模型选择有更细粒度的控制。如果你有多个 API Provider 账号，或者想在性能和成本之间做取舍，可以试试。

> **项目地址**: https://github.com/musistudio/claude-code-router
