<template>
  <div class="home-page">
    <CharacterCanvas />

    <!-- ===== Hero Section ===== -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="hero-title-gradient">Coding Agent</span>
          <br />
          <span class="hero-title-gradient">for Research</span>
        </h1>
        <p class="hero-tagline">Coding Agent 在学术研究中的应用经验分享</p>
        <div class="hero-actions">
          <a class="hero-btn hero-btn-primary" href="/Agents-are-the-future-of-academic-research/posts/agent-basics/2026-02-13-llm-agent-basics">
            开始阅读
          </a>
          <a class="hero-btn hero-btn-secondary" href="/Agents-are-the-future-of-academic-research/about/">
            关于本站
          </a>
        </div>
      </div>
      <div class="hero-fade" />
    </section>

    <!-- ===== Features Section ===== -->
    <section class="features-section">
      <div class="section-container">
        <div class="features-grid">
          <a
            v-for="feature in features"
            :key="feature.title"
            :href="withBase(feature.link)"
            class="feature-card"
          >
            <span class="feature-icon">{{ feature.icon }}</span>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.details }}</p>
          </a>
        </div>
      </div>
    </section>

    <!-- ===== Articles Section ===== -->
    <section class="articles-section">
      <div class="section-container">
        <blockquote class="articles-quote">
          <p><em>不要温和地走进那个良夜</em></p>
          <footer>-- 迪兰·托马斯（Dylan Thomas）</footer>
        </blockquote>

        <h2 class="section-title">最新文章</h2>
        <div class="articles-list">
          <a
            v-for="article in articles"
            :key="article.link"
            :href="withBase(article.link)"
            class="article-item"
          >
            <span class="article-title">{{ article.title }}</span>
            <span class="article-date">{{ article.date }}</span>
          </a>
        </div>
      </div>
    </section>

    <!-- ===== Footer Section ===== -->
    <section class="footer-section">
      <div class="section-container">
        <h2 class="section-title">参与贡献</h2>
        <p class="footer-text">如果你也在学术研究中使用 Coding Agent，欢迎：</p>
        <div class="contribute-list">
          <div class="contribute-item">
            <span class="contribute-label">分享经验</span>
            <span class="contribute-desc">提交你的实践案例</span>
          </div>
          <div class="contribute-item">
            <span class="contribute-label">讨论交流</span>
            <span class="contribute-desc">在 Issue 中提出问题</span>
          </div>
          <div class="contribute-item">
            <span class="contribute-label">Star 支持</span>
            <span class="contribute-desc">如果觉得有用，请给个 Star</span>
          </div>
        </div>

        <div class="contact-info">
          <a href="https://github.com/hjnnjh" class="contact-link" target="_blank" rel="noopener">
            GitHub: @hjnnjh
          </a>
          <span class="contact-link">
            Email: jinnan_huang@stu.xjtu.edu.cn
          </span>
        </div>

        <div class="footer-bottom">
          Built with VitePress and Claude Code
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { withBase } from 'vitepress'
import CharacterCanvas from './CharacterCanvas.vue'

const features = [
  {
    icon: '\u{1F916}',
    title: 'Agent 基础',
    details: '深入理解 LLM Agent 的核心概念、架构原理和工作机制，为实践应用打下坚实基础',
    link: '/categories/agent-basics',
  },
  {
    icon: '\u{1F4BB}',
    title: 'Coding Agent 实践',
    details: 'Claude Code, OpenCode 等工具的深度使用技巧，提升编程效率的最佳实践',
    link: '/categories/coding-agent',
  },
  {
    icon: '\u{1F52C}',
    title: '学术科研案例',
    details: 'Coding Agent 在文献调研、数据分析、论文写作等学术场景中的真实应用案例',
    link: '/categories/research-cases',
  },
  {
    icon: '\u{1F6E0}\uFE0F',
    title: '工具对比评测',
    details: '主流 Coding Agent 工具的横向对比、性能评测和选型建议',
    link: '/categories/tools-comparison',
  },
  {
    icon: '\u{1F4A1}',
    title: '经验心得分享',
    details: '实践总结、踩坑记录、技巧分享，帮助你少走弯路',
    link: '/categories/insights',
  },
  {
    icon: '\u{1F680}',
    title: '我的常用 Skills',
    details: '集成 academic-research-writer, prompt-optimizer 等学术研究场景常用 Skills，全面提升学术写作效率',
    link: '/SKILLS-GUIDE',
  },
]

const articles = [
  { title: 'Claude Code 进阶功能速览', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-advanced-features' },
  { title: 'Claude Code Hooks：用确定性保证自动化工作流', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-hooks' },
  { title: 'Claude Code Skills：打造你的专属 AI 技能包', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-skills' },
  { title: 'Subagent：Claude Code 的并行任务引擎', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-subagent' },
  { title: 'MCP：让 Claude Code 连接外部世界', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-mcp' },
  { title: 'Claude Code 记忆系统详解', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-memory' },
  { title: '将 GitHub Copilot 订阅接入 Claude Code (Part 4)', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-copilot-api' },
  { title: 'Claude Code Router (CCR) 使用指南 (Part 3)', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-router' },
  { title: 'Claude Code 配置进阶：zcf 工具介绍 (Part 2)', date: '2026-03-07', link: '/posts/coding-agent/2026-03-07-claude-code-zcf' },
  { title: 'Claude Code 介绍与安装 (Part 1)', date: '2026-02-26', link: '/posts/coding-agent/2026-02-26-claude-code-intro' },
  { title: 'Agent 评估', date: '2026-02-17', link: '/posts/agent-basics/2026-02-17-agent-evaluation' },
  { title: '多 Agent 协作', date: '2026-02-16', link: '/posts/agent-basics/2026-02-16-multi-agent-collaboration' },
  { title: '上下文工程', date: '2026-02-15', link: '/posts/agent-basics/2026-02-15-context-engineering' },
  { title: 'Agent 的记忆系统', date: '2026-02-14', link: '/posts/agent-basics/2026-02-14-agent-memory-systems' },
  { title: 'LLM Agent 简介', date: '2026-02-13', link: '/posts/agent-basics/2026-02-13-llm-agent-basics' },
]
</script>

<style scoped>
/* ===== Page-level unified background ===== */
.home-page {
  /* Light mode page colors */
  --home-bg: #e8ecf4;
  --home-bg-soft: #d8dee8;
  --home-text-1: #1e293b;
  --home-text-2: rgba(30, 41, 59, 0.7);
  --home-text-3: rgba(30, 41, 59, 0.5);
  --home-divider: rgba(30, 41, 59, 0.1);
  --home-brand-1: #3B82F6;

  position: relative;
  background-color: var(--home-bg);
}

/* ===== Hero Section ===== */
.hero-section {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;

  /* Light mode hero specific */
  --hero-tagline: rgba(30, 41, 59, 0.6);
  --hero-btn-secondary-bg: rgba(0, 0, 0, 0.04);
  --hero-btn-secondary-color: rgba(30, 41, 59, 0.7);
  --hero-btn-secondary-border: rgba(0, 0, 0, 0.1);
  --hero-btn-secondary-hover: rgba(0, 0, 0, 0.08);
}


.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 0 24px;
  max-width: 800px;
}

.hero-title {
  font-family: "Fira Code", "JetBrains Mono", "Consolas", monospace;
  font-size: 4rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 24px;
  letter-spacing: -0.02em;
}

.hero-title-gradient {
  background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-tagline {
  font-size: 1.25rem;
  color: var(--hero-tagline);
  margin: 0 0 40px;
  font-weight: 400;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-btn {
  display: inline-flex;
  align-items: center;
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.hero-btn-primary {
  background: linear-gradient(135deg, #3B82F6, #6366F1);
  color: #fff;
}

.hero-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

.hero-btn-secondary {
  background: var(--hero-btn-secondary-bg);
  color: var(--hero-btn-secondary-color);
  border: 1px solid var(--hero-btn-secondary-border);
}

.hero-btn-secondary:hover {
  background: var(--hero-btn-secondary-hover);
  transform: translateY(-2px);
}

.hero-fade {
  display: none;
}

/* ===== Shared Section Styles ===== */
.section-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 32px;
  color: var(--home-text-1);
  border: none;
  padding: 0;
}

/* ===== Features Section ===== */
.features-section {
  position: relative;
  z-index: 1;
  padding: 80px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.feature-card {
  display: block;
  padding: 28px 24px;
  border-radius: 12px;
  background: var(--home-bg-soft);
  border: 1px solid rgba(59, 130, 246, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
}

.feature-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--home-text-1);
  margin: 0 0 8px;
}

.feature-desc {
  font-size: 0.9rem;
  color: var(--home-text-2);
  line-height: 1.6;
  margin: 0;
}

/* ===== Articles Section ===== */
.articles-section {
  position: relative;
  z-index: 1;
  padding: 0 0 80px;
}

.articles-quote {
  border-left: 4px solid var(--home-brand-1);
  padding: 16px 24px;
  margin: 0 0 48px;
  background: var(--home-bg-soft);
  border-radius: 4px;
}

.articles-quote p {
  margin: 0 0 4px;
  color: var(--home-text-2);
  font-size: 1rem;
}

.articles-quote footer {
  color: var(--home-text-3);
  font-size: 0.875rem;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.article-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.article-item:hover {
  background: var(--home-bg-soft);
  border-left-color: var(--home-brand-1);
}

.article-title {
  font-size: 0.95rem;
  color: var(--home-text-1);
  font-weight: 500;
}

.article-date {
  font-size: 0.8rem;
  color: var(--home-text-3);
  font-family: "Fira Code", "JetBrains Mono", monospace;
  flex-shrink: 0;
  margin-left: 24px;
}

/* ===== Footer Section ===== */
.footer-section {
  position: relative;
  z-index: 1;
  padding: 64px 0 80px;
  border-top: 1px solid var(--home-divider);
}

.footer-text {
  color: var(--home-text-2);
  margin: 0 0 24px;
}

.contribute-list {
  display: flex;
  gap: 32px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.contribute-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contribute-label {
  font-weight: 600;
  color: var(--home-text-1);
  font-size: 0.95rem;
}

.contribute-desc {
  color: var(--home-text-3);
  font-size: 0.85rem;
}

.contact-info {
  display: flex;
  gap: 32px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.contact-link {
  color: var(--home-text-2);
  font-size: 0.9rem;
  text-decoration: none;
}

.contact-link:hover {
  color: var(--home-brand-1);
}

.footer-bottom {
  color: var(--home-text-3);
  font-size: 0.85rem;
  padding-top: 24px;
  border-top: 1px solid var(--home-divider);
}

/* ===== Responsive ===== */
@media (max-width: 1023px) {
  .hero-title {
    font-size: 3rem;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-tagline {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .article-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .article-date {
    margin-left: 0;
  }

  .contribute-list {
    flex-direction: column;
    gap: 16px;
  }

  .contact-info {
    flex-direction: column;
    gap: 12px;
  }
}

/* ===== Reduced Motion ===== */
@media (prefers-reduced-motion: reduce) {
  .feature-card:hover,
  .hero-btn:hover {
    transform: none;
  }
}
</style>

<!-- Non-scoped styles for dark mode (needs to target .dark on <html>) -->
<style>
.dark .home-page {
  --home-bg: #0f1020;
  --home-bg-soft: rgba(255, 255, 255, 0.04);
  --home-text-1: #F1F5F9;
  --home-text-2: rgba(241, 245, 249, 0.6);
  --home-text-3: rgba(241, 245, 249, 0.4);
  --home-divider: rgba(255, 255, 255, 0.08);
  --home-brand-1: #60A5FA;
}

.dark .hero-section {
  --hero-tagline: rgba(241, 245, 249, 0.6);
  --hero-btn-secondary-bg: rgba(255, 255, 255, 0.06);
  --hero-btn-secondary-color: rgba(241, 245, 249, 0.8);
  --hero-btn-secondary-border: rgba(255, 255, 255, 0.1);
  --hero-btn-secondary-hover: rgba(255, 255, 255, 0.1);
}

.dark .hero-section .hero-title-gradient {
  background: linear-gradient(135deg, #60A5FA 0%, #818CF8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
