---
title: "MCP：让 Claude Code 连接外部世界"
date: 2026-03-07
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - mcp
  - model-context-protocol
  - tools
difficulty: intermediate
summary: "MCP（Model Context Protocol）是 AI 工具连接外部服务的标准接口。本文介绍 MCP 的工作原理、Claude Code 中的配置方法、常用 MCP 服务推荐，以及适合学术科研用户的工具组合。"
featured: false
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

# MCP：让 Claude Code 连接外部世界

::: info 本文概览

- 🎯 **目标读者**：希望让 Claude Code 连接外部工具和服务的用户
- ⏱️ **阅读时间**：约 15 分钟
- 📚 **知识要点**：MCP 工作原理、配置命令、常用 MCP 服务、学术科研推荐
:::

## MCP 是什么？

把 Claude Code 想象成一台电脑主机。它本身很强大，但如果没有外设接口，就只能靠自己内置的能力工作——不能上网、不能操作浏览器、不能读数据库、不能查 GitHub 上的 Issue。

**MCP（Model Context Protocol）** 就是为 AI 工具设计的"USB-C 接口"标准。只要服务商按照 MCP 规范实现了一个服务端（MCP Server），Claude Code 就能像插入外设一样即插即用，获得这个服务提供的全部能力。

截至 2026 年，官方 MCP 注册表已收录超过 3,000 个社区服务，从网络搜索、浏览器自动化，到数据库查询、论文检索，覆盖了绝大多数开发和研究场景。

---

## MCP 的工作原理

### 客户端-服务端架构

MCP 采用标准的客户端-服务端模型：

```mermaid
graph LR
    A["Claude Code<br/>（MCP 客户端）"] <-->|MCP 协议| B["MCP Server<br/>（工具封装层）"]
    B <-->|原生 API| C["外部服务<br/>（GitHub / 数据库 / 浏览器...）"]
```

- **Claude Code**：作为 MCP 客户端，向 MCP Server 发送工具调用请求
- **MCP Server**：封装了外部服务的访问逻辑，对外暴露标准化的"工具"列表
- **外部服务**：GitHub、数据库、网络搜索引擎等真实服务

这个设计的好处是**标准化**：Claude Code 只需要支持一种协议（MCP），就能与所有兼容服务通信，不需要为每个服务单独适配。

### 传输模式

MCP 支持三种传输模式：

| 模式 | 适用场景 | 特点 |
|------|----------|------|
| **stdio** | 本地 MCP Server（最常见） | Claude Code 以子进程方式启动 Server，通过标准输入输出通信，延迟最低（< 5ms） |
| **SSE** | 远程 HTTP Server | 适合团队共享的远程服务 |
| **Streamable HTTP** | 云端托管 Server | 适合企业级集中部署 |

对于个人用户，绝大多数情况下使用 **stdio** 模式即可。

### MCP Server 能提供什么？

每个 MCP Server 可以向 Claude Code 暴露三类资源：

- **Tools（工具）**：Claude 可以主动调用的操作，如"搜索网页"、"查询数据库"、"截图"
- **Resources（资源）**：可以通过 `@` 引用的数据，如文件、API 响应，类似于在对话中提及文件
- **Prompts（提示词模板）**：以 `/` 开头的快捷命令，出现在命令列表中

---

## 在 Claude Code 中配置 MCP

### 核心命令

Claude Code 提供了一套完整的 MCP 管理命令：

```bash
# 添加 MCP Server
claude mcp add <server-name> [options] -- <command>

# 列出已配置的 Server
claude mcp list

# 查看指定 Server 的详情
claude mcp get <server-name>

# 删除 Server
claude mcp remove <server-name>
```

在 Claude Code 交互模式中，可以用 `/mcp` 查看当前所有 Server 的连接状态。

### 配置作用域

MCP Server 有三个作用域，决定它对谁可见：

| 作用域 | 参数 | 配置存储位置 | 适用场景 |
|--------|------|-------------|---------|
| **local**（默认）| 无需参数 | `~/.claude.json` | 当前项目，仅对你自己可见 |
| **project** | `--scope project` | 项目根目录 `.mcp.json` | 当前项目，团队成员共享 |
| **user** | `--scope user` | `~/.claude.json` | 跨项目通用，仅对你自己可见 |

`project` 作用域的配置存储在 `.mcp.json` 文件中，这个文件应该提交到 git，让团队所有成员共享相同的工具配置。

### 添加 MCP Server 示例

**添加网络搜索能力（stdio 模式）：**

```bash
claude mcp add open-websearch -- npx -y @open-websearch/mcp
```

**添加 GitHub 集成（带环境变量）：**

```bash
claude mcp add github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here \
  -- npx -y @modelcontextprotocol/server-github
```

**添加 Context7 文档查询（用户级，所有项目可用）：**

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
```

**使用 HTTP 传输（远程 Server）：**

```bash
claude mcp add --transport http paypal https://mcp.paypal.com/mcp
```

### 直接用 JSON 配置

如果你有多个 Server 需要批量配置，也可以用 `claude mcp add-json` 命令直接写入 JSON：

```bash
claude mcp add-json context7 '{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp@latest"]
}'
```

或者直接编辑 `~/.claude.json` 中的 `mcpServers` 字段。

::: warning 配置文件格式
JSON 不允许尾随逗号，这是最常见的配置错误之一。如果 MCP Server 无法启动，先用 JSON 校验工具检查配置文件格式。
:::

---

## 常用 MCP 服务介绍

### Context7：实时文档查询

**用途**：查询各类库的最新文档和代码示例，解决 Claude 知识截止日期问题。

当你问 Claude Code "怎么用最新版 pandas 读取 Parquet 文件"，它有可能给出过时的 API。接入 Context7 后，Claude 能实时拉取库的官方文档，给出准确的答案。

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
```

**安装后使用**：在对话中直接提问时，Claude 会自动调用 Context7 查询文档，无需额外操作。

### Playwright：浏览器自动化

**用途**：让 Claude Code 控制浏览器，实现网页操作、截图、表单填写、数据抓取等。

科研场景下的典型用法：自动从学术数据库下载数据、抓取期刊网站上的文献信息、自动化提交实验结果。

```bash
claude mcp add --scope user playwright -- npx -y @playwright/mcp@latest
```

**安装后使用**：在对话中描述网页操作任务，Claude 会调用浏览器完成。例如："帮我打开 arXiv，搜索 'diffusion model protein structure'，把前 10 篇结果的标题和链接列出来。"

### GitHub MCP Server：仓库管理

**用途**：直接在 Claude Code 中管理 GitHub 仓库——查看 Issue、PR、代码、提交记录等。

```bash
claude mcp add github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=your_pat_here \
  -- npx -y @modelcontextprotocol/server-github
```

**安装后使用**：让 Claude 直接操作 GitHub，如"把这个 Bug 修复提成一个 PR"、"看看这个 repo 的 open issues 里有没有和性能相关的"。

### Serena：语义级代码分析

**用途**：提供比普通文件读取更深层的代码理解——符号查找、引用分析、跨文件关系图谱，特别适合大型代码库。

```bash
claude mcp add --scope user serena -- uvx --from serena-mcp serena-mcp
```

**安装后使用**：在分析或重构大型项目时，Serena 能帮 Claude 更精准地定位代码，减少不必要的全文件读取。

### DeepWiki：GitHub 仓库深度阅读

**用途**：对任意 GitHub 仓库生成深度理解报告，适合快速上手陌生代码库。

```bash
claude mcp add --scope user deepwiki -- npx -y @mcp-deepwiki/mcp@latest
```

**安装后使用**：让 Claude 分析开源项目时，DeepWiki 能提供比直接读代码更系统的架构理解。

### Zotero MCP：文献管理集成

**用途**：直接访问 Zotero 文献库，让 Claude Code 读取论文内容、笔记和标注。

**安装后使用**：科研工作中，可以让 Claude 根据你的 Zotero 文献库回答问题、提取特定论文的关键结论。

---

## 使用 MCP 的技巧

### 在对话中引用 MCP 资源

配置好 MCP Server 后，在对话中输入 `@`，会弹出自动补全菜单，可以看到来自 MCP Server 的可引用资源（类似引用本地文件）。

### 使用 MCP 提示词命令

部分 MCP Server 会注册提示词命令，在对话中输入 `/` 可以看到所有可用命令，格式为 `/mcp__服务名__命令名`。

### MCP Tool Search（工具搜索）

当你配置了大量 MCP Server 时，所有工具的描述可能占用大量上下文。Claude Code 支持 **MCP Tool Search**：当 MCP 工具描述超过上下文窗口的 10% 时，自动切换为按需加载模式，只在需要时才将相关工具载入上下文。这个功能对配置了 10 个以上 MCP Server 的用户非常实用。

---

## 学术科研用户的 MCP 推荐组合

对于科研工作者，以下这套 MCP 组合覆盖了大多数日常需求：

| MCP | 解决的问题 |
|-----|-----------|
| **Context7** | 查询数据分析库（numpy、pandas、scipy 等）的最新 API |
| **Playwright** | 自动抓取文献、下载数据集、操作在线工具 |
| **GitHub MCP** | 管理科研代码的 Issue 和 PR，追踪同行的开源工作 |
| **Zotero MCP** | 将文献管理与代码编写打通，让 Claude 理解你的研究背景 |

**一次性安装命令（用户级，所有项目可用）：**

```bash
# Context7：文档查询
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest

# Playwright：浏览器自动化
claude mcp add --scope user playwright -- npx -y @playwright/mcp@latest

# GitHub：仓库管理（需替换 Token）
claude mcp add --scope user github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token \
  -- npx -y @modelcontextprotocol/server-github
```

::: tip 用 zcf 批量安装
如果你已经使用 [zcf 工具](/posts/coding-agent/2026-03-07-claude-code-zcf)，它内置了常用 MCP 的批量注册功能，初始化时可以一键完成上述配置，无需逐条执行命令。
:::

---

## 安全注意事项

- **API Token 用环境变量传递**，不要直接硬编码在配置文件中：

  ```bash
  # 推荐：用 -e 参数传入
  claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN -- ...

  # 不推荐：直接写死 Token
  claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxx -- ...
  ```

- **区分作用域**：敏感 Token 配置在 `user` 或 `local` 作用域，不要用 `project` 作用域（否则 Token 会随 `.mcp.json` 提交到 git）

- **MCP Prompt Injection 风险**：MCP Server 返回的内容可能包含试图操控 Claude 行为的恶意指令，对来自不可信 MCP 源的内容保持警惕

---

## 小结

MCP 让 Claude Code 能够访问外部服务和数据源：

- **原理**：标准化的客户端-服务端协议，Claude Code 作为客户端，连接各类 MCP Server
- **配置**：`claude mcp add` 命令，三种作用域（local/project/user），stdio 是最常用模式
- **推荐工具**：Context7（文档）、Playwright（浏览器）、GitHub（仓库）、Serena（代码分析）

MCP 生态仍在快速发展，官方注册表已有数千个服务可用。可以根据自己的工作流需求选择合适的 MCP 组合。

::: tip 下一步
下一篇文章将介绍 **Subagent（子代理）**，Claude Code 内置的并行任务执行机制，让多个子代理同时处理不同子任务。
:::

## 参考资料

- [Claude Code 官方文档：MCP 集成](https://code.claude.com/docs/en/mcp)
- [Model Context Protocol 规范](https://docs.claude.com/en/docs/mcp)
- [Claude Code MCP 配置指南 - MCPcat](https://mcpcat.io/guides/adding-an-mcp-server-to-claude-code/)
- [MCP Servers 推荐列表 - claudefa.st](https://claudefa.st/blog/tools/mcp-extensions/best-addons)
