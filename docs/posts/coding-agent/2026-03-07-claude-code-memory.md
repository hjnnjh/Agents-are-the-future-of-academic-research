---
title: "Claude Code 记忆系统详解"
date: 2026-03-07
author: "博客作者"
categories:
  - coding-agent
tags:
  - claude-code
  - memory
  - CLAUDE.md
  - configuration
difficulty: intermediate
summary: "本文详细介绍 Claude Code 记忆系统：CLAUDE.md 的六层层级结构、编写实践、@imports 模块化拆分，以及自动记忆（MEMORY.md）机制，让 Claude Code 持续记住你的项目规范和偏好。"
featured: false
---

::: warning AI 含量说明
本文由 AI (Claude) 辅助生成，内容经过人工审核与编辑。部分描述可能存在简化表述，请读者结合实际使用体验参考。
:::

# Claude Code 记忆系统详解

::: info 本文概览

- 🎯 **目标读者**：已完成 Claude Code 基础安装、希望让 Claude 更好地理解项目上下文的用户
- ⏱️ **阅读时间**：约 18 分钟
- 📚 **知识要点**：CLAUDE.md 层级结构与写法、@imports 模块化、自动记忆（MEMORY.md）、快捷记忆技巧
:::

## 为什么需要记忆系统？

Claude Code 的每次会话都从一个**全新的上下文窗口**开始。它不记得上次你告诉它"这个项目用 ruff 格式化，不用 black"，也不知道你的数据文件放在哪个目录，更不清楚你的提交规范。

如果没有记忆系统，你需要在每次会话开始时重复说明这些基础信息，既浪费时间，又占用上下文空间。

Claude Code 的记忆系统通过两种机制解决这个问题：

| 机制 | 形式 | 谁来写 | 适合存储什么 |
|------|------|--------|-------------|
| **CLAUDE.md 文件** | Markdown 指令文件 | 你 | 项目规范、技术栈、工作流约定等稳定信息 |
| **自动记忆（MEMORY.md）** | 自动生成的笔记 | Claude 自己 | 调试经验、代码习惯、临时发现等动态信息 |

两者互补：CLAUDE.md 是你主动写给 Claude 的"项目手册"，MEMORY.md 是 Claude 在工作中自己记下的"学习笔记"。

---

## CLAUDE.md：你写给 Claude 的项目手册

### 什么是 CLAUDE.md？

CLAUDE.md 是一个 Markdown 格式的指令文件。Claude Code 在每次会话启动时会自动读取它，并将其内容注入到系统提示中——这意味着你写在里面的每一条规则，Claude 从会话第一秒就知道。

### 六层层级结构

Claude Code 不只读取单一的 CLAUDE.md，而是支持**六层层级**，每一层服务于不同范围和目的：

```
层级 1（最宽泛）  托管策略        /Library/Application Support/ClaudeCode/CLAUDE.md (macOS)
                                   /etc/claude-code/CLAUDE.md (Linux)
层级 2           用户全局        ~/.claude/CLAUDE.md
层级 3           项目级          ./CLAUDE.md（项目根目录，随 git 提交）
层级 4           项目本地        ./CLAUDE.local.md（自动被 .gitignore，个人配置）
层级 5           模块化规则      ./.claude/rules/*.md（按文件类型或功能拆分）
层级 6（最具体）  子目录级        子目录内的 CLAUDE.md（按需加载）
```

**优先级规则：更具体的指令覆盖更宽泛的指令。** 例如，用户全局的 CLAUDE.md 里写了"使用 4 空格缩进"，但项目 CLAUDE.md 写了"使用 2 空格缩进"，那在这个项目里，2 空格缩进生效。

**加载时机：**
- 层级 1～5 的文件在会话启动时**完整加载**
- 子目录中的 CLAUDE.md 在 Claude 访问该目录时**按需加载**，不会在启动时占用上下文

### 各层的使用场景

**用户全局（`~/.claude/CLAUDE.md`）**：适合存储跨项目的个人偏好，例如：
- 默认语言（"请始终用中文回复"）
- 通用代码风格（"提交信息遵循 Conventional Commits 规范"）
- 个人习惯（"修改文件前先告诉我你的计划"）

**项目级（`./CLAUDE.md`）**：团队共享的项目规范，通过 git 同步给所有协作者，例如：
- 项目架构说明
- 构建/测试命令
- 代码规范和禁止事项
- 常用路径说明

**项目本地（`./CLAUDE.local.md`）**：不提交到 git 的个人配置，例如：
- 个人的本地路径配置
- 临时测试指令
- 个人习惯覆盖（不想让团队共享的设置）

**模块化规则（`./.claude/rules/*.md`）**：将指令拆分为专题文件，仅在相关场景下生效（下文详述）。

---

## 如何编写好的 CLAUDE.md？

### 快速起点：使用 `/init` 命令

如果你不知道从哪里开始，在 Claude Code 会话中运行 `/init`：

```
/init
```

Claude 会自动分析你的代码库结构，生成一个初始 CLAUDE.md，包含它检测到的构建命令、测试指令和项目约定。如果 CLAUDE.md 已存在，`/init` 会建议改进而不是直接覆盖。

生成后，在此基础上补充 Claude **无法自行发现**的信息（如团队约定、项目背景、禁止操作等）。

### 内容组织建议

一个实用的项目 CLAUDE.md 通常包含以下几部分：

```markdown
# 项目概述
这是一个 Python 数据分析项目，用于处理气候数据集。使用 uv 管理依赖。

## 环境与构建
- Python 3.11+，用 uv 管理虚拟环境
- 运行测试：`uv run pytest`
- 格式化：`uv run ruff format .`
- 类型检查：`uv run mypy src/`

## 目录结构
- `src/`：核心代码
- `data/raw/`：原始数据（不提交 git）
- `notebooks/`：探索性 Jupyter Notebook
- `results/`：输出结果

## 代码规范
- 所有公共函数必须有类型注解和 docstring
- 变量命名用下划线分隔，不用缩写
- 数据处理函数放在 `src/processing/` 下

## 禁止操作
- 不要修改 `data/raw/` 下的原始文件
- 不要直接操作数据库，使用 `src/db/` 下的封装
- 提交前必须通过所有测试

## Git 规范
提交信息格式：`type(scope): message`
类型：feat, fix, docs, refactor, test, chore
```

### 写作技巧

**用命令式，不用描述式。** Claude 对具体指令的遵从率远高于模糊表述：

```markdown
# 差：这个项目喜欢简洁的代码风格
# 好：函数长度不超过 50 行；每个文件只做一件事
```

**控制文件长度。** 每个 CLAUDE.md 文件建议**不超过 200 行**。文件越长，上下文消耗越多，Claude 的遵从率也会下降。如果内容增长过大，用 `@imports` 或 `.claude/rules/` 拆分。

**定期维护。** 过时或相互矛盾的指令会让 Claude 随机选择其中一条遵循。建议每隔一段时间审查一遍，删除不再适用的规则。

### 快速添加记忆：`#` 前缀

在 Claude Code 对话中，以 `#` 开头输入内容，可以快速将这条信息添加为记忆：

```
# 这个项目的 conftest.py 在 tests/ 目录下，不在项目根目录
```

Claude 会询问你希望将其保存在哪个记忆文件中（全局 CLAUDE.md 还是项目 CLAUDE.md）。这是在对话过程中随时补充规则的最快方式。

---

## 模块化拆分：@imports 与 .claude/rules/

当 CLAUDE.md 内容增长到需要拆分时，有两种方式：

### 方式一：@imports 语法

在 CLAUDE.md 中使用 `@path/to/file` 语法引入外部文件：

```markdown
# ./CLAUDE.md

# 导入团队共享的 Python 规范
@.claude/rules/python-conventions.md

# 导入个人快捷配置
@~/.claude/my-shortcuts.md
```

被导入的文件会在会话启动时随主 CLAUDE.md 一起展开加载。支持相对路径和绝对路径，支持递归嵌套（最深 5 层）。

### 方式二：.claude/rules/ 目录（按范围生效）

在 `.claude/rules/` 下创建专题文件，可以通过 glob 模式将规则限定于特定文件类型或目录：

```
.claude/rules/
├── python.md          # 针对 *.py 文件的规范
├── notebooks.md       # 针对 *.ipynb 文件的规范
└── data-pipeline.md   # 针对 src/pipeline/ 目录的规范
```

规则文件示例（`python.md`）：

```markdown
---
globs: "**/*.py"
---

# Python 代码规范

- 使用 `pathlib.Path` 而不是 `os.path`
- 数值计算优先用 numpy 向量化，避免 Python 层循环
- 所有数据加载函数返回 `pd.DataFrame`，不返回裸 list
```

`globs` 字段支持标准 glob 语法。未指定 globs 的规则文件对所有文件生效。

::: tip 大型项目的分支策略
在 `main` 分支维护稳定的核心 CLAUDE.md，在 feature 分支上按需添加特定规则文件，避免主分支上的合并冲突。
:::

---

## 自动记忆：Claude 给自己记笔记

### 什么是自动记忆？

自动记忆是 Claude Code 的一项实验性功能。启用后，Claude 会在工作过程中自动将有价值的信息记录下来，比如它发现的构建命令、调试过程中的关键发现、你的代码习惯偏好等——这些信息无需你手动整理，Claude 自己决定什么值得记、记在哪里。

自动记忆是**本地存储**的，不会上传到云端，不会跨设备同步。同一个 git 仓库下的所有目录共享同一份自动记忆。

### 目录结构

每个项目的自动记忆存储在：

```
~/.claude/projects/<project-path>/memory/
├── MEMORY.md          # 索引文件（入口）
├── debugging.md       # 调试经验（示例主题文件）
├── patterns.md        # 代码模式发现
└── api-conventions.md # API 使用约定
```

**`MEMORY.md`** 是索引文件，会在每次会话启动时自动加载**前 200 行**。它记录了哪些信息存在哪个主题文件里，作为整个记忆库的导航。

**主题文件**（如 `debugging.md`）不在启动时加载，Claude 在需要时按需读取。这个设计保证了记忆库的增长不会占用启动时的上下文。

### MEMORY.md vs CLAUDE.md：如何分工？

| | CLAUDE.md | MEMORY.md |
|---|---|---|
| **编写者** | 你 | Claude 自动写 |
| **内容** | 稳定的规范和约定 | 动态发现的经验和模式 |
| **加载时机** | 启动时完整加载 | 前 200 行启动加载，其余按需 |
| **适合存储** | 团队规范、技术约束 | 调试洞察、偏好发现 |
| **需要维护** | 是（定期审查） | 较少（Claude 自动管理） |

两者配合使用：CLAUDE.md 告诉 Claude "规则是什么"，MEMORY.md 帮 Claude 记住"之前遇到过什么"。

::: info 自动记忆的激活
自动记忆功能目前在 Claude Code 中默认启用。你可以在 `/settings` 中查看和管理记忆相关配置。
:::

---

## 实践建议：学术科研用户

科研项目通常有数据路径复杂、实验版本众多、代码写完就少碰等特点，用 CLAUDE.md 记录这些信息会比较有用。

**一个科研项目的 CLAUDE.md 模板：**

```markdown
# 科研项目：气候数据分析

## 环境
- Python 3.11，用 conda 管理环境（环境名：climate-analysis）
- 运行实验：`python src/run_experiment.py --config configs/`
- 数据处理：`python src/preprocess.py`

## 数据目录说明
- `data/raw/`：原始观测数据，**绝对不能修改**
- `data/processed/`：预处理后的数据
- `results/`：实验输出，文件名格式为 `{experiment_name}_{date}.csv`

## 实验管理
- 每个实验对应一个 `configs/` 下的 YAML 配置文件
- 实验结果用 MLflow 追踪，不要直接打印到 stdout
- 随机种子统一设为 42（除非有特殊原因）

## 依赖
- 数值计算：numpy, scipy
- 数据处理：pandas, xarray（处理 NetCDF 格式）
- 可视化：matplotlib, cartopy（地图）
- 机器学习：scikit-learn（不用 PyTorch/TensorFlow）

## 注意事项
- 不要在 notebook 里写业务逻辑，notebook 只用于可视化和探索
- 处理大型 NetCDF 文件时注意内存，用 chunks 参数分块加载
```

---

## 小结

Claude Code 的记忆系统提供了以下几种机制：

| 工具 | 核心价值 |
|------|---------|
| **项目 CLAUDE.md** | 让 Claude 了解项目规范，避免每次重复说明 |
| **用户 CLAUDE.md** | 跨项目的个人偏好，一次设置全局生效 |
| **项目本地 CLAUDE.md** | 个人私有配置，不污染团队共享文件 |
| **@imports** | 拆分大型 CLAUDE.md，保持文件可读性 |
| **.claude/rules/** | 按文件类型或目录设置精细化规则 |
| **自动记忆 MEMORY.md** | Claude 自动积累的工作经验，无需手动维护 |
| **# 前缀快速记忆** | 对话中随时补充规则，最低摩擦 |

建议的起步路径：用 `/init` 生成初始 CLAUDE.md，然后根据实际使用中 Claude 犯错或理解偏差的地方，逐步补充和完善。

::: tip 下一步
下一篇文章将介绍 **MCP（Model Context Protocol）**，让 Claude Code 连接外部工具和数据源的标准协议，支持网页搜索、数据库查询等操作。
:::

## 参考资料

- [Claude Code 官方文档：记忆系统](https://code.claude.com/docs/en/memory)
- [CLAUDE.md 记忆系统深度解析 - SFEIR Institute](https://institute.sfeir.com/en/claude-code/claude-code-memory-system-claude-md/deep-dive/)
- [You (probably) don't understand Claude Code memory](https://joseparreogarcia.substack.com/p/claude-code-memory-explained)
