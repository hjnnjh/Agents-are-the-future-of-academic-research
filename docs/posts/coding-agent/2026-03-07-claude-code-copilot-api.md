---
title: "将 GitHub Copilot 订阅接入 Claude Code (Part 4)"
date: 2026-03-07
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - github-copilot
  - copilot-api
  - api-proxy
difficulty: intermediate
summary: "copilot-api 是一个将 GitHub Copilot 接口转换为 OpenAI/Anthropic 兼容格式的本地代理，让已有 Copilot 订阅的用户可以直接用它驱动 Claude Code。本文介绍其安装配置、Claude Code 接入方式以及使用时的注意事项。"
featured: false
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

:::tip 选读
本文为 Part 4 选读内容。如果你是 Claude Code 新用户，建议先阅读 [Part 1](/posts/coding-agent/2026-02-26-claude-code-intro) 完成基础安装；如需灵活管理多个 API Provider，可搭配 [Part 2（zcf）](/posts/coding-agent/2026-03-07-claude-code-zcf) 和 [Part 3（CCR）](/posts/coding-agent/2026-03-07-claude-code-router) 阅读。
:::

## 这是什么

[copilot-api](https://github.com/caozhiyuan/copilot-api) 是一个本地代理服务，通过逆向工程暴露 GitHub Copilot 的内部接口，并将其转换为 **OpenAI Chat Completions** 和 **Anthropic Messages** 兼容格式。支持这两种 API 的工具（包括 Claude Code）都可以通过它使用 GitHub Copilot 作为后端模型。

如果你已经有 GitHub Copilot 订阅（个人版、企业版或教育版），可以用这个工具复用订阅来驱动 Claude Code，不需要额外买 Anthropic API 额度。

---

## ⚠️ 重要风险说明

开始之前，请了解以下风险：

:::danger 合规与账号安全
**这是逆向工程产物，不受 GitHub 官方支持，随时可能失效。**

GitHub 的滥用检测系统会监控异常的自动化请求。大量快速请求可能触发警告，极端情况下可能导致 Copilot 访问被暂停。

请在使用前自行审阅：
- [GitHub 可接受使用政策](https://docs.github.com/site-policy/acceptable-use-policies/github-acceptable-use-policies)
- [GitHub Copilot 使用条款](https://docs.github.com/site-policy/github-terms/github-terms-for-additional-products-and-features#github-copilot)

**请合理控制使用频率，避免触发账号限制。**
:::

---

## 前提条件

- **Bun >= 1.2.x**（运行时依赖，需提前安装）
- **GitHub 账号** + **有效的 GitHub Copilot 订阅**（个人版、企业版或教育版均支持）

---

## 安装与启动

可以通过 `npx` 直接运行，不用本地安装：

```bash
npx @jeffreycao/copilot-api@latest start
```

服务默认监听 `localhost:4141`，启动时控制台会打印 Usage Dashboard 的链接。

### 常用启动参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--port` / `-p` | 监听端口 | 4141 |
| `--account-type` / `-a` | 账号类型：`individual`、`business`、`enterprise` | individual |
| `--rate-limit` / `-r` | 请求间最小间隔（秒） | 无 |
| `--wait` / `-w` | 触达速率限制时等待而不是报错 | false |
| `--manual` | 手动审批每条请求 | false |
| `--github-token` / `-g` | 直接传入 GitHub Token（免交互认证） | 无 |
| `--claude-code` / `-c` | 生成 Claude Code 启动命令并复制到剪贴板 | false |

**企业或学校账号示例：**

```bash
npx @jeffreycao/copilot-api@latest start --account-type business
```

**限速防触发示例（请求间隔 30 秒，超限时等待）：**

```bash
npx @jeffreycao/copilot-api@latest start --rate-limit 30 --wait
```

---

## 认证流程

首次启动会触发 GitHub OAuth 认证：程序输出一个设备码和验证 URL，在浏览器中打开该 URL 并输入设备码完成授权。认证信息保存在 `~/.local/share/copilot-api/`，后续启动不用重复认证。

如需在非交互环境（如服务器）中使用，可先运行 `auth` 子命令生成 Token，再以 `--github-token` 参数传入：

```bash
# 步骤 1：交互式生成并保存 Token
npx @jeffreycao/copilot-api@latest auth

# 步骤 2：以 Token 方式启动（无需交互）
npx @jeffreycao/copilot-api@latest start --github-token ghp_YOUR_TOKEN_HERE
```

---

## 接入 Claude Code

有两种方式把 Claude Code 接到本地代理。

### 方式一：交互式配置（推荐首次使用）

在启动时加上 `--claude-code` 标志：

```bash
npx @jeffreycao/copilot-api@latest start --claude-code
```

程序会引导你选择主模型和后台轻量模型，配置完成后自动生成一条包含所有必要环境变量的启动命令并复制到剪贴板。在新终端窗口粘贴运行即可。

### 方式二：持久化配置（推荐日常使用）

在项目根目录创建 `.claude/settings.json`，写入以下内容：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:4141",
    "ANTHROPIC_AUTH_TOKEN": "dummy",
    "ANTHROPIC_MODEL": "gpt-5.2",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "gpt-5.2",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gpt-5-mini",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

各字段说明：

- `ANTHROPIC_BASE_URL`：将 Claude Code 的请求指向本地代理（`localhost:4141`）
- `ANTHROPIC_AUTH_TOKEN`：代理在本地运行，填 `dummy` 占位即可
- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_SONNET_MODEL`：主力模型名，可通过访问 `http://localhost:4141/v1/models` 查询当前可用的 Copilot 模型列表
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`：后台轻量任务使用的模型，建议填写较快速的小模型
- `DISABLE_NON_ESSENTIAL_MODEL_CALLS` / `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`：减少 Claude Code 的非必要后台请求，有助于节省 Copilot 配额

下图为 Pro 订阅下的可用模型示例：

![copilot-api 可用模型列表（Pro 订阅）](/img/coding-agent/copilot-api-models.png)

:::warning 注意：Copilot 对模型有上下文限制
GitHub Copilot 对部分模型的上下文窗口做了裁剪。例如 Claude Opus 4.6 通过 Copilot 访问时上下文窗口缩减至 **128K**，官方 API 是 200K。处理大型代码库或长文档时注意这个差异。
:::

:::info
`.claude/settings.json` 放在项目根目录时仅对当前项目生效。如需全局生效，将文件放至 `~/.claude/settings.json`。注意全局配置会影响所有项目，切换回官方 API 时需要手动恢复。
:::

配置完成后，确保 copilot-api 代理已在后台运行，然后正常启动 Claude Code 即可：

```bash
# 终端 1：启动代理
npx @jeffreycao/copilot-api@latest start

# 终端 2：启动 Claude Code（会自动读取 settings.json 配置）
claude
```

---

## 用量监控

启动服务后，控制台会输出 Usage Dashboard 的 URL：

```
http://localhost:4141/usage-viewer?endpoint=http://localhost:4141/usage
```

打开后可以查看 Copilot 配额使用情况（Chat 和 Completions 的剩余量、消耗统计等）。

也可以不启动服务，直接在终端查询配额：

```bash
npx @jeffreycao/copilot-api@latest check-usage
```

---

## 对学术科研用户的价值

GitHub 为学生和开源贡献者提供 [Copilot 免费计划或教育优惠](https://github.com/features/copilot/plans)。有 Copilot 订阅的用户可以通过 copilot-api 复用到 Claude Code，减少对 Anthropic API 账号的依赖。官方 Claude API 额度紧张时，copilot-api 也可以作为临时替代，结合 [CCR 的路由规则](/posts/coding-agent/2026-03-07-claude-code-router) 将部分任务切流到 Copilot 后端。

不过要注意局限性：Copilot 的配额和模型选择受订阅计划限制，部分模型的上下文窗口有裁剪（如 Claude Opus 4.6 缩减至 128K）。需要高并发、超长上下文或特定推理模型的任务，直连官方 API 更靠谱。逆向工程工具的稳定性也不如官方 SDK。

---

## 小结

copilot-api 给有 Copilot 订阅的用户多了一条接入 Claude Code 的路径，本地跑个代理、配几行环境变量就行。

但别忘了：这是逆向工程工具，有违反服务条款的风险，用不好可能影响 GitHub 账号。建议配合限速参数保守使用，当作官方 API 的补充，别拿来当主力。

> **项目地址**: https://github.com/caozhiyuan/copilot-api
