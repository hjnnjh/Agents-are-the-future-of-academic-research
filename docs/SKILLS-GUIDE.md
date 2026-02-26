# Skills 使用指南

本指南帮助你快速上手项目集成的 12 个 Claude Code Skills,提升博客创作效率。

## 🎯 按场景选择 Skills

### 场景 1: 我有 Word/PDF 笔记,想转换为博客文章

**推荐工作流**:

```bash
# Step 1: 转换文档格式
/markdown-tools --input research-notes.docx --output docs/posts/2025/draft.md

# Step 2: 优化语言风格
/beautiful-prose --input docs/posts/2025/draft.md --style technical

# Step 3: 事实检查
/fact-checker --input docs/posts/2025/draft.md --auto-fix true

# Step 4: 生成 PDF 版本(可选)
/pdf-creator --input docs/posts/2025/draft.md --template default
```

**涉及 Skills**: markdown-tools, beautiful-prose, fact-checker, pdf-creator

---

### 场景 2: 我要写一篇深度技术研究文章

**推荐工作流**:

```bash
# Step 1: AI 辅助研究和写作
/content-research-writer --topic "Coding Agent 在学术研究中的应用" --depth deep --sources 10

# Step 2: 优化提示词(如果需要迭代改进)
/prompt-optimizer --prompt "扩展 Agent 工作流章节" --task-type writing

# Step 3: 添加流程图
/mermaid-tools --type flowchart --description "Agent 工作流程: 需求分析->任务规划->执行->反馈"

# Step 4: 语言润色
/beautiful-prose --style academic

# Step 5: 事实验证
/fact-checker --strict true --check-code true
```

**涉及 Skills**: content-research-writer, prompt-optimizer, mermaid-tools, beautiful-prose, fact-checker

---

### 场景 3: 我要写 Coding Agent 教程

**推荐工作流**:

```bash
# Step 1: 创建 CLI 演示动画
/cli-demo-generator --script tutorial-demo.yaml --output demo.gif

# Step 2: 生成架构图
/mermaid-tools --type sequence --description "Claude Code 与工具的交互流程"

# Step 3: 优化代码示例(在文章中)
# (手动编写代码,然后验证)

# Step 4: 语言风格优化
/beautiful-prose --style tutorial --target-audience beginner

# Step 5: 最终检查
/fact-checker --check-code true --check-links true
```

**涉及 Skills**: cli-demo-generator, mermaid-tools, beautiful-prose, fact-checker

---

### 场景 4: 定期维护博客项目

**推荐工作流**:

```bash
# Step 1: 整理文档结构
/docs-cleaner --path docs/posts --mode all --backup true

# Step 2: 生成变更日志
/changelog-generator --from v1.0.0 --to HEAD --output CHANGELOG.md

# Step 3: 审查 skills 质量
/skill-reviewer --skill .claude/skills/* --output skills-review.md

# Step 4: 提取/更新设计系统(如有设计稿)
/ui-designer --image new-design.png --framework vitepress --generate-theme true
```

**涉及 Skills**: docs-cleaner, changelog-generator, skill-reviewer, ui-designer

---

## 📚 Skills 快速参考

### 按频率排序

#### 🔥 每天使用

| Skill | 命令 | 核心功能 |
|-------|------|----------|
| markdown-tools | `/markdown-tools` | 文档格式转换 |
| mermaid-tools | `/mermaid-tools` | 生成图表 |
| fact-checker | `/fact-checker` | 事实验证 |

#### 📅 每周使用

| Skill | 命令 | 核心功能 |
|-------|------|----------|
| content-research-writer | `/content-research-writer` | AI 研究写作 |
| beautiful-prose | `/beautiful-prose` | 语言润色 |
| pdf-creator | `/pdf-creator` | 生成 PDF |
| docs-cleaner | `/docs-cleaner` | 文档整理 |

#### 📆 按需使用

| Skill | 命令 | 核心功能 |
|-------|------|----------|
| prompt-optimizer | `/prompt-optimizer` | 优化提示词 |
| cli-demo-generator | `/cli-demo-generator` | CLI 演示 |
| ui-designer | `/ui-designer` | 设计系统提取 |
| changelog-generator | `/changelog-generator` | 变更日志 |
| skill-reviewer | `/skill-reviewer` | Skills 审查 |

---

## 🎓 进阶技巧

### 技巧 1: 组合 Skills 形成管道

```bash
# 一键从 Word 到发布就绪
/markdown-tools --input note.docx --output temp.md && \
/beautiful-prose --input temp.md --output polished.md && \
/fact-checker --input polished.md --auto-fix true && \
/pdf-creator --input polished.md
```

### 技巧 2: 创建自定义工作流别名

```bash
# 在 package.json 中添加
{
  "scripts": {
    "publish-flow": "run-s convert polish check pdf",
    "convert": "/markdown-tools --input $INPUT --output temp.md",
    "polish": "/beautiful-prose --input temp.md",
    "check": "/fact-checker --input temp.md",
    "pdf": "/pdf-creator --input temp.md"
  }
}
```

### 技巧 3: 批量处理

大多数 skills 支持批量处理:

```bash
# 批量转换
/markdown-tools --batch-config convert-config.json

# 批量生成 PDF
/pdf-creator --batch posts-list.txt

# 批量事实检查
/fact-checker --path docs/posts/**/*.md
```

---

## ⚙️ 配置最佳实践

### 1. 项目级配置

创建 `.claude/config.json`:

```json
{
  "defaults": {
    "author": "张三",
    "language": "zh-CN",
    "categories": ["coding-agent"],
    "outputDir": "docs/posts/2025"
  },
  "skills": {
    "markdown-tools": {
      "imageDir": "docs/public/images/2025"
    },
    "beautiful-prose": {
      "defaultStyle": "technical",
      "targetAudience": "intermediate"
    },
    "fact-checker": {
      "autoFix": true,
      "strict": false
    }
  }
}
```

### 2. Skill 配置

每个 skill 的 `config.js` 可进一步定制,详见各 skill 文档。

---

## 🐛 常见问题

### Q1: Skill 找不到?

**解决方案**:
```bash
# 检查 skills 目录
ls .claude/skills/

# 重新加载 skills
claude reload-skills
```

### Q2: 参数不清楚?

**解决方案**:
```bash
# 查看 skill 帮助
/<skill-name> --help

# 或查看文档
cat .claude/skills/<skill-name>/SKILL.md
```

### Q3: 输出格式不符合预期?

**解决方案**:
- 检查 skill 配置文件
- 使用 `--dry-run` 参数预览
- 查看示例和文档

### Q4: 性能问题?

**解决方案**:
- 大文件使用 `--batch` 模式
- 启用缓存配置
- 限制搜索深度和范围

---

## 📖 学习路径

### 初学者(第 1 周)

1. ✅ 熟悉 **markdown-tools** - 导入已有内容
2. ✅ 掌握 **mermaid-tools** - 为文章添加图表
3. ✅ 使用 **fact-checker** - 基础质量保证

### 进阶者(第 2-3 周)

4. ✅ 学习 **content-research-writer** - AI 辅助写作
5. ✅ 掌握 **beautiful-prose** - 语言优化
6. ✅ 了解 **pdf-creator** - 多格式输出
7. ✅ 使用 **cli-demo-generator** - 教程增强

### 高级用户(第 4 周+)

8. ✅ 深入 **prompt-optimizer** - 提示词工程
9. ✅ 掌握 **docs-cleaner** - 项目维护
10. ✅ 使用 **ui-designer** - 主题定制
11. ✅ 学习 **changelog-generator** - 版本管理
12. ✅ 精通 **skill-reviewer** - 质量保证

---

## 🔗 相关资源

---

## 💡 最佳实践

### 1. 渐进式采用

不要一次使用所有 skills,逐步引入:

- 第 1 周: 3 个基础 skills
- 第 2-3 周: 再添加 4 个
- 第 4 周+: 全面掌握所有 skills

### 2. 工作流模板化

为常见任务创建固定工作流,减少决策疲劳。

### 3. 定期维护

- 每周运行 `/docs-cleaner`
- 每月审查 `/skill-reviewer`
- 按版本生成 `/changelog-generator`

### 4. 持续学习

- 阅读各 skill 的完整文档
- 尝试高级参数
- 探索 skills 组合使用

---

**祝你创作愉快!** ✨
