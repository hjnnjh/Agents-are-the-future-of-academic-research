---
title: "Claude Code Skills：打造你的专属 AI 技能包"
date: 2026-03-07
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - skills
  - workflow
  - automation
difficulty: intermediate
summary: "Skills 是 Claude Code 最具扩展性的能力之一，允许你把专业指令、工作流约定乃至 Shell 脚本打包成可复用的「技能」，随时按需激活。本文从创建第一个 Skill 到包含真实脚本的进阶用法，再到多 Skill 组合工作流，全面介绍 Skills 的使用方法，并以本项目实际使用的 Skill 为例。"
featured: false
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

# Claude Code Skills：打造你的专属 AI 技能包

::: info 本文概览

- 🎯 **目标读者**：希望扩展 Claude Code 能力、打造专属工作流的用户
- ⏱️ **阅读时间**：约 18 分钟
- 📚 **知识要点**：Skill 文件格式、触发方式、从基础到进阶的用法、包含脚本的 Skill、Skills 组合工作流
:::

## 什么是 Skills？

想象你雇了一位全能助手，但每次让他做"数据分析报告"时，都要重新解释一遍：用什么格式、检查哪些指标、如何输出……这很低效。

**Skills** 解决的就是这个问题。Skill 是一个打包好的指令集——你把某类任务的完整操作流程、输出规范、工具约束都写在一个文件里，之后只需一句 `/skill-name` 就能激活，Claude 会按你设定的专业流程工作，无需重复解释。

官方对 Skills 的定位是：**"教会 Claude 以可重复的方式完成特定任务"**。

### Skills vs CLAUDE.md：如何选择？

| | CLAUDE.md | Skill |
|---|---|---|
| **加载时机** | 每次会话启动时全部加载 | 按需加载（相关任务时激活） |
| **Token 消耗** | 始终占用上下文 | 仅激活时占用 |
| **适合存储** | 几乎对所有任务都相关的规范 | 特定工作流的专业指令 |
| **典型内容** | 代码风格、禁止操作、项目结构 | 数据分析流程、文章审查规范、报告生成 |

**判断标准**：如果某条规则几乎每次任务都用到，放 CLAUDE.md；如果只在特定工作流中需要，做成 Skill，按需激活。

---

## Skill 文件格式

一个 Skill 就是一个目录，核心文件是 `SKILL.md`：

```
.claude/skills/
└── my-skill/
    ├── SKILL.md          # 必须，主指令文件
    ├── scripts/          # 可选，可执行脚本
    ├── templates/        # 可选，输出模板
    └── config.js         # 可选，配置文件
```

### 标准 SKILL.md 格式

```yaml
---
name: my-skill-name
description: 当用户需要……时激活此技能（这是 Claude 决定是否自动激活的依据）
allowed-tools: Read, Grep, Glob    # 可选，限制该 Skill 可以使用的工具
disable-model-invocation: false    # 可选，true 则只能手动触发
context: fork                      # 可选，在独立子代理中执行
---

# Skill 名称

## 执行步骤

...（具体指令）

## 输出格式

...（期望的输出结构）
```

### `description` 字段：最关键的字段

每次对话中，Claude 会用约 100 tokens 扫描所有 Skill 的 `description` 字段，判断是否与当前任务相关——相关则自动加载完整 Skill 内容。

**description 的写法直接决定自动激活的准确率**。建议用"当……时"或"适用于……场景"的句式，从 Claude 的决策视角描述触发条件，而非只说功能：

```yaml
# 差：审查博客文章的内容质量
description: 内容审查工具

# 好：当用户需要审查文章、检测敏感信息、发布前质量检查时使用
description: 当需要审查博客文章内容、检测敏感信息泄露、进行发布前最终检查时激活
```

---

## 触发方式

Skills 有两种触发方式：

### 自动触发（模型调用）

Claude 在理解你的任务后，自动识别相关 Skill 并加载。这是最常见的方式——你不需要记住 Skill 名字，Claude 会自己决定。

*注：本博客项目通过 [Hooks](/posts/coding-agent/2026-03-07-claude-code-hooks) 进一步强化了这个机制：每次任务提交前，Hook 强制 Claude 评估所有可用 Skill，确保自动激活不被遗漏。*

### 手动触发（Slash 命令）

在 Claude Code 交互模式中输入 `/` 加 Skill 名称直接调用：

```
/content-reviewer --input docs/posts/my-article.md
/changelog-generator --from v1.0.0 --to HEAD
/mermaid-tools --type flowchart --description "用户登录流程..."
```

`$ARGUMENTS` 占位符接收 `/skill-name` 后跟的所有参数文本。

---

## 基础：纯文本指令型 Skill

纯文本型 Skill 是最简单的形式——只有文字指令，没有脚本。Claude 阅读指令后直接按要求操作。

### 示例：content-reviewer（本项目实际使用）

这是本项目 `.claude/skills/content-reviewer/SKILL.md` 的核心内容：

```markdown
# Content Reviewer Skill

## 约束（重要）

- **禁止使用** Edit、Write、NotebookEdit 等任何文件修改工具
- **只能使用** Read、Glob、Grep 等只读工具
- 输出结构化审查报告，由主 Agent 决定是否执行修改

## 审查项目

### 1. 敏感信息泄露
- API Key、Token、密码等凭据
- 个人隐私信息（邮箱、手机号）
- 内部系统 URL

### 2. 质量问题
- 占位符文本（TODO、FIXME、Lorem ipsum）
- 未完成的章节或段落
- 与文章标题不匹配的内容

## 输出格式

输出标准化的审查报告，包含问题位置、严重程度、修改建议。
```

**关键设计**：这个 Skill 通过明确写出"禁止使用写入工具"，在指令层面实现了只读约束，将审查和修改职责分离，避免审查 Agent 直接改动文件而绕过人工确认。

---

## 中级：带 $ARGUMENTS 参数的 Skill

`$ARGUMENTS` 让 Skill 能接收用户在 slash 命令后输入的参数，实现动态化调用。

### 示例：修复指定 Issue

```yaml
---
name: fix-issue
description: 当需要修复特定 GitHub Issue 时使用，传入 Issue 编号
---

请修复 GitHub Issue #$ARGUMENTS，遵循以下规范：

1. 先用 Bash 工具查看 Issue 详情：`gh issue view $ARGUMENTS`
2. 找到与 Issue 相关的代码文件
3. 实现修复，为边界情况添加测试
4. 生成符合 Conventional Commits 规范的 commit message：`fix: 修复 #$ARGUMENTS - <问题描述>`

修复完成后，输出变更摘要。
```

调用方式：

```
/fix-issue 1234
```

Claude 会将 `$ARGUMENTS` 替换为 `1234`，然后执行完整的 Issue 修复流程。

---

## 进阶：包含脚本代码的 Skill

包含脚本的 Skill 是最强大的形式。SKILL.md 中的代码片段是**参考实现**——Claude 阅读这些代码后理解处理逻辑，然后通过 Bash 工具执行真实命令，或者调用 `scripts/` 目录下预置的脚本文件。

### 示例：changelog-generator（本项目实际使用）

这个 Skill 通过在 SKILL.md 中内嵌完整的 Node.js 实现代码，让 Claude 理解完整的处理流程：

**调用方式**：
```
/changelog-generator --from v1.0.0 --to HEAD
```

**SKILL.md 中的核心实现逻辑**：

```javascript
const { execSync } = require('child_process')
const fs = require('fs')

function getGitCommits(from, to) {
  const range = from ? `${from}..${to}` : to
  const format = '%H%n%an%n%ae%n%ai%n%s%n%b%n==END=='

  const output = execSync(
    `git log ${range} --pretty=format:"${format}"`,
    { encoding: 'utf-8' }
  )

  return output.split('==END==').filter(Boolean).map(block => {
    const [hash, author, email, date, subject, ...body] = block.trim().split('\n')
    return { hash: hash.substring(0, 7), author, date: new Date(date), subject }
  })
}

function groupByType(commits) {
  const typeMap = {
    feat:     { title: '✨ 新功能', commits: [] },
    fix:      { title: '🐛 错误修复', commits: [] },
    docs:     { title: '📝 文档', commits: [] },
    refactor: { title: '♻️ 重构', commits: [] },
    perf:     { title: '⚡ 性能优化', commits: [] },
    chore:    { title: '🔧 配置', commits: [] }
  }
  commits.forEach(c => {
    const match = c.subject.match(/^(\w+)(?:\([^)]+\))?: /)
    const type = match ? match[1] : 'other'
    if (typeMap[type]) typeMap[type].commits.push(c)
  })
  return typeMap
}
```

**Claude 的实际执行过程**：

1. 读取 SKILL.md 中的逻辑描述和代码参考
2. 通过 Bash 工具执行 `git log` 命令获取提交历史
3. 解析 Conventional Commits 格式（feat/fix/docs 等类型）
4. 按类型分组，生成标准 Markdown Changelog
5. 写入 `CHANGELOG.md`

**输出示例**：

```markdown
# Changelog

## [1.2.0] - 2026-03-07

### ✨ 新功能

- 添加 MCP 集成文章 (a1b2c3d) @作者

### 📝 文档

- 更新侧边栏导航配置 (d4e5f6g) @作者

---

**Full Changelog**: [v1.1.0...v1.2.0](https://github.com/...)
```

### 脚本型 Skill 的两种实现方式

**方式一：SKILL.md 中的代码作为参考逻辑**

Claude 阅读代码理解处理流程，然后自己通过 Bash 工具实现相同逻辑。适合代码逻辑清晰、Claude 能自行翻译执行的场景。

**方式二：预置真实脚本（推荐复杂场景）**

在 `scripts/` 目录放置真实可执行脚本，Claude 直接调用：

```
.claude/skills/my-skill/
├── SKILL.md          # 描述流程，说明调用 scripts/run.sh
└── scripts/
    └── run.sh        # 真实可执行脚本
```

SKILL.md 中写明：
```markdown
## 执行

运行 `.claude/skills/my-skill/scripts/run.sh $ARGUMENTS`
收集输出并格式化报告。
```

这种方式确保脚本逻辑由预置代码控制，Claude 只负责调用和格式化输出。

::: tip 脚本依赖处理
如果脚本需要 npm 依赖（如 Puppeteer、gifsicle），在 SKILL.md 中声明依赖并添加安装步骤，Claude 会在执行前检查并提示安装：

```markdown
## 前置依赖
确保已安装：`npm install puppeteer`
```
:::

---

## 进阶：Skills 之间的组合工作流

单个 Skill 处理单类任务，多个 Skill 组合成完整工作流。本项目 README 中记录了三条实战工作流：

### 工作流 1：从笔记到发布

```
/markdown-tools        →  将 Word/PDF 笔记转为 Markdown
/content-research-writer →  基于主题深度研究，扩充内容
/beautiful-prose       →  润色文章语言，提升可读性
/fact-checker          →  验证技术事实和链接有效性
/pdf-creator           →  导出为专业 PDF（支持中文+数学公式）
```

### 工作流 2：技术文章创作

```
/prompt-optimizer      →  优化写作思路和结构
/mermaid-tools         →  生成架构图和流程图
/cli-demo-generator    →  录制终端操作演示（GIF/SVG）
/docs-cleaner          →  整理文档结构，修复损坏链接
/fact-checker          →  发布前最终验证
```

### 工作流 3：项目发版维护

```
/changelog-generator   →  从 Git 历史生成发布说明
/docs-cleaner          →  清理文档、更新过时内容
/skill-reviewer        →  审查 Skill 文件质量
```

**调用方式**：依次手动触发每个 Skill，或在 prompt 中明确告诉 Claude 按顺序执行这些步骤。

---

## 在 Claude Code 中创建和管理 Skill

### 创建 Skill

**方法一：手动创建文件**

```bash
# 在项目目录（团队共享）
mkdir -p .claude/skills/my-skill
touch .claude/skills/my-skill/SKILL.md

# 或者在用户全局目录（所有项目可用）
mkdir -p ~/.claude/skills/my-skill
touch ~/.claude/skills/my-skill/SKILL.md
```

编辑 SKILL.md，填写 frontmatter 和指令内容。

**方法二：在 Claude Code 中用 `/agents` 命令辅助生成**

在交互模式中输入 `/agents`，Claude 会引导你描述 Skill 的用途并自动生成 SKILL.md 骨架。

### 存放位置与作用域

| 位置 | 作用范围 | 适用场景 |
|------|---------|---------|
| `.claude/skills/`（项目根目录） | 当前项目 | 项目专属 Skill，可提交 git 与团队共享 |
| `~/.claude/skills/` | 所有项目 | 个人通用 Skill（如润色工具、代码审查） |

Claude Code 启动时自动扫描这两个目录，无需额外注册。

### 查看可用 Skill

在 Claude Code 交互模式中，输入 `/` 触发自动补全，会列出所有可用的 Skill 和命令。

### 从社区安装 Skill

官方和社区维护了多个 Skill 仓库：

| 仓库 | 内容 |
|------|------|
| [anthropics/skills](https://github.com/anthropics/skills/) | 官方示例（Web 测试、MCP 生成等） |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 精选社区 Skill 列表 |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Playwright 测试、竞品分析等 |
| [obra/superpowers](https://github.com/anthropics/skills) | 20+ 生产级 Skill（TDD、调试等） |

安装方式：

```bash
# 克隆仓库后复制目标 Skill 目录
git clone https://github.com/anthropics/skills.git
cp -r skills/skills/playwright-testing ~/.claude/skills/
```

---

## 实用 npm 工具：批量管理 Skills

手动克隆 + 复制 Skill 的方式适合偶尔安装，但社区涌现出了更高效的 npm CLI 工具，让 Skill 的安装、更新、管理像 npm 包管理一样顺滑。

### openskills：跨 Agent 的通用 Skill 安装器

[openskills](https://github.com/numman-ali/openskills) 是一个开源 CLI 工具，将 Anthropic 的 Skills 系统延伸到所有主流 AI 编程助手——Claude Code、Cursor、Windsurf、Aider、Codex 等，同时完全兼容 Claude Code 原生的 SKILL.md 格式和 `.claude/skills/` 目录结构。

::: info 本项目的 Hook 就用到了它
本博客项目的 `skill-eval-local.sh` Hook 通过 `npx openskills list` 列出所有已安装 Skill，并注入到 Claude 的系统提示中，实现每次任务前的自动技能评估。详见 [Hooks 文章](/posts/coding-agent/2026-03-07-claude-code-hooks)。
:::

**核心工作原理**：openskills 会在 `AGENTS.md` 中生成标准化的 `<available_skills>` XML 块，非 Claude Code 工具（如 Cursor）也能通过这个文件识别和使用 Skill。

**常用命令**：

```bash
# 安装 Anthropic 官方技能包（到项目级 .claude/skills/）
npx openskills install anthropics/skills

# 安装到全局（所有项目可用）
npx openskills install anthropics/skills --global

# 安装到跨 Agent 通用目录（.agent/skills/，Cursor 等也能识别）
npx openskills install anthropics/skills --universal

# 安装单个 Skill（如只要 pdf 工具）
npx openskills install anthropics/skills/pdf

# 列出所有已安装 Skill（skill-eval-local.sh Hook 用的就是这个）
npx openskills list

# 更新所有 Skill 到最新版本
npx openskills update

# 更新 AGENTS.md（让非 Claude Code 工具也能识别 Skill）
npx openskills sync

# 读取指定 Skill 的完整内容（供 Agent 按需加载）
npx openskills read pdf

# 删除指定 Skill
npx openskills remove pdf
```

**与 Claude Code 的差异对比**：

| 维度 | Claude Code 原生 | openskills |
|------|-----------------|------------|
| Skill 格式 | SKILL.md | 完全相同 |
| 安装目录 | `.claude/skills/` | 相同（默认） |
| 支持的 Agent | Claude Code | Claude Code + Cursor 等 37+ 个 |
| 跨 Agent 同步 | 不支持 | `sync` 生成 AGENTS.md |
| 批量更新 | 手动 | `npx openskills update` |

---

### `npx skills`：开放 Skill 生态的统一入口

[vercel-labs/skills](https://github.com/vercel-labs/skills) 是另一个功能强大的 Skill 管理 CLI，对应的技能发现网站是 **[skills.sh](https://skills.sh)**。与 openskills 侧重兼容性不同，`skills` 更聚焦于 Skill 生态的发现与分发——支持从任意 GitHub 仓库安装技能，并用符号链接（symlink）保持单一来源，便于一键更新。

```bash
# 列出仓库中的可用 Skill
npx skills add vercel-labs/agent-skills --list

# 安装到 Claude Code（项目级）
npx skills add vercel-labs/agent-skills -a claude-code

# 全局安装指定 Skill
npx skills add vercel-labs/agent-skills --skill react-best-practices -g -a claude-code

# 同时安装到多个 Agent
npx skills add vercel-labs/agent-skills -a claude-code -a opencode

# 查看已安装的所有 Skill
npx skills list

# 搜索 Skill（支持关键词过滤）
npx skills find typescript

# 检查更新
npx skills check

# 更新所有 Skill
npx skills update

# 创建新 Skill 模板
npx skills init my-skill
```

**Vercel 团队维护的 `agent-skills` 技能集**（`vercel-labs/agent-skills`）质量尤其高，包含：

| Skill | 描述 |
|-------|------|
| `react-best-practices` | 40+ 条 React/Next.js 性能优化规则，覆盖 Bundle 优化、数据获取、重渲染等 8 个类别 |
| `web-design-guidelines` | 100+ 条 UI 最佳实践，涵盖无障碍、性能、UX、深色模式、国际化等 11 个类别 |
| `react-native-guidelines` | 16 条 React Native 最佳实践，含 FlashList、Reanimated、Expo 等移动端关键场景 |
| `composition-patterns` | React 组合模式指南，解决 boolean prop 泛滥问题 |
| `vercel-deploy-claimable` | 一键将项目部署到 Vercel，自动检测 40+ 框架，返回预览链接和所有权转让链接 |

```bash
# 快速体验：安装 Vercel 的 React 最佳实践 Skill
npx skills add vercel-labs/agent-skills --skill react-best-practices -a claude-code -g -y
```

---

### 两个工具的选用建议

| 场景 | 推荐工具 |
|------|---------|
| 主要使用 Claude Code，偶尔需要列出 Skill | `openskills`（与项目 Hook 集成更顺畅） |
| 同时使用多个 Agent（Claude Code + Cursor 等） | `openskills --universal` |
| 从 GitHub 仓库发现和安装社区 Skill | `npx skills`（生态更丰富，有 skills.sh 目录） |
| 想用 Vercel 高质量前端开发 Skill | `npx skills add vercel-labs/agent-skills` |

---

## 本项目的 14 个 Skills 全览

本博客项目在 `.claude/skills/` 目录下维护了 14 个 Skill，分为四类：

| 类别 | Skill | 功能 |
|------|-------|------|
| **写作与内容** | markdown-tools | Word/PDF 转 Markdown，提取图片 |
| | mermaid-tools | 自然语言生成 7 种 Mermaid 图表 |
| | content-research-writer | 多源研究型文章撰写（含引用） |
| | beautiful-prose | 4 种风格语言润色 |
| | prompt-optimizer | EARS 方法优化 AI 提示词 |
| **文档与自动化** | changelog-generator | Git 历史生成规范 Changelog |
| | docs-cleaner | 批量整理文档结构、修复链接 |
| | pdf-creator | Markdown → 专业 PDF（中文+公式） |
| **设计与展示** | ui-designer | 设计图提取配色，生成 CSS/SCSS |
| | cli-demo-generator | 生成终端录屏演示（GIF/SVG/MP4） |
| **质量保证** | fact-checker | 技术事实验证、链接检查 |
| | skill-reviewer | Skill 文档质量审查与评分 |
| **审查（只读）** | content-reviewer | 内容安全审查（禁止写入工具） |
| | markdown-reviewer | Markdown 格式规范检查（只读） |

审查类 Skill 的设计值得特别关注：`content-reviewer` 和 `markdown-reviewer` 明确声明禁止使用 Edit/Write 工具，只能读取，强制实现"审查-修改"职责分离，确保审查结果由人工确认后再决定是否修改。

---

## 进阶技巧

### 使用 `ultrathink` 开启深度推理

在 SKILL.md 正文中任意位置包含单词 `ultrathink`，该 Skill 激活时 Claude 会启用扩展思维模式，适合需要深度分析和规划的复杂任务：

```markdown
请对以下实验数据进行深度分析（ultrathink），包括：
- 异常值检测与原因推断
- 与预期理论值的偏差分析
...
```

### 用 `context: fork` 隔离 Skill 执行

在 frontmatter 中设置 `context: fork`，该 Skill 激活时会在独立的 Subagent 上下文中执行，结果只返回给主对话，不污染主上下文：

```yaml
---
name: deep-analysis
description: 对大型代码库进行深度分析
context: fork
---
```

适合需要读取大量文件、分析结果可能很长的任务——Subagent 的独立上下文可以容纳更多内容，而主对话保持清洁。

---

## 对学术科研用户的 Skill 设计建议

科研场景中，几类常见的重复性工作特别适合做成 Skill：

**数据分析报告 Skill**：
```markdown
## 数据分析流程

1. 加载数据：读取 data/processed/*.csv，检查 shape 和数据类型
2. 统计分析：均值、标准差、分布、缺失值比率
3. 异常值处理：报告异常值位置，不自动删除
4. 输出：生成 results/analysis_report.md，附带 Matplotlib 可视化代码
```

**实验配置对比 Skill**：
```markdown
对比 configs/ 目录下多个实验配置，生成对比表格，标注关键参数差异和预期影响。
```

这类 Skill 把"每次实验都需要重复的分析流程"固化下来，下次只需 `/analyze-data`，Claude 就按既定流程工作，保证结果一致性。

---

## 小结

Skills 是 Claude Code 从"通用助手"升级为"专业团队"的关键扩展机制：

| 层次 | 形式 | 典型用途 |
|------|------|---------|
| **基础** | 纯文本指令型 | 审查规范、角色约束、输出格式 |
| **中级** | 带 $ARGUMENTS 参数 | 按编号修复 Issue、按主题生成报告 |
| **进阶** | 含脚本逻辑 | Changelog 生成、PDF 导出、终端录屏 |
| **高级** | Skills 组合工作流 | 从笔记到发布的全流程自动化 |

从一个解决你最频繁重复的问题的 Skill 开始——哪怕只是把"每次都要重复说明的数据分析规范"写成一个 Skill，你就会发现这是 Claude Code 中投入产出比最高的配置之一。

::: tip 与 Hooks 配合
本博客项目的 [skill-eval-local.sh Hook](/posts/coding-agent/2026-03-07-claude-code-hooks) 在每次任务提交时自动列出所有 Skill 并强制 Claude 评估，确保相关 Skill 不被遗漏。如果你的项目积累了多个 Skill，结合类似的 Hook 可以让自动激活更加可靠。
:::

## 参考资料

- [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills)
- [anthropics/skills 官方示例仓库](https://github.com/anthropics/skills/)
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
