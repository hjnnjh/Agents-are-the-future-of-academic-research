import { defineConfig } from 'vitepress'
import type { DefaultTheme } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// https://vitepress.dev/reference/site-config
export default withMermaid(defineConfig({
  title: "Coding Agent for Research",
  description: "LLM Agent（尤其是 Coding Agent）在学术研究中的应用经验分享",

  // 部署配置
  // 如果部署到 GitHub Pages 项目站点，需要设置 base
  base: '/Agents-are-the-future-of-academic-research/',

  // 语言配置
  lang: 'zh-CN',

  // 主题配置
  themeConfig: {
    // 网站标题
    siteTitle: 'Coding Agent for Research',

    // 导航菜单
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/posts/2026/' },
      {
        text: '分类',
        items: [
          { text: 'Agent 基础', link: '/categories/agent-basics' },
          { text: 'Coding Agent', link: '/categories/coding-agent' },
          { text: '学术案例', link: '/categories/research-cases' },
          { text: '工具对比', link: '/categories/tools-comparison' },
          { text: '经验心得', link: '/categories/insights' }
        ]
      },
      { text: '关于', link: '/about/' }
    ],

    // 侧边栏
    sidebar: {
      '/posts/': [
        {
          text: '2026 年',
          collapsed: false,
          items: [
            { text: 'LLM Agent 到底是什么？', link: '/posts/2026/2026-02-13-llm-agent-basics' },
            { text: 'Agent Skills 使用入门', link: '/posts/2026/2026-02-10-agent-skills-intro' }
          ]
        }
      ],
      '/categories/': [
        {
          text: '文章分类',
          items: [
            { text: 'Agent 基础', link: '/categories/agent-basics' },
            { text: 'Coding Agent 实践', link: '/categories/coding-agent' },
            { text: '学术科研案例', link: '/categories/research-cases' },
            { text: '工具对比评测', link: '/categories/tools-comparison' },
            { text: '经验心得分享', link: '/categories/insights' }
          ]
        }
      ]
    },

    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/hjnnjh/Agents-are-the-future-of-academic-research' }
    ],

    // 页脚
    footer: {
      message: '基于 VitePress 构建 | 内容采用 CC BY-NC-SA 4.0 许可',
      copyright: 'Copyright © 2025-present'
    },

    // 搜索配置
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换'
                }
              }
            }
          }
        }
      }
    },

    // 文档页脚
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    // 最后更新时间
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'full',
        timeStyle: 'short'
      }
    },

    // 大纲配置
    outline: {
      level: [2, 3],
      label: '本页目录'
    },

    // 编辑链接
    editLink: {
      pattern: 'https://github.com/hjnnjh/Agents-are-the-future-of-academic-research/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    },

    // 返回顶部文字
    returnToTopLabel: '返回顶部',

    // 外部链接图标
    externalLinkIcon: true,

    // 深色模式切换
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',

    // 侧边栏菜单标签
    sidebarMenuLabel: '菜单',
  },

  // Markdown 配置
  markdown: {
    // 代码块主题
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    },

    // 代码块行号
    lineNumbers: true,

    // 数学公式支持 (需要安装 markdown-it-mathjax3)
    math: true,

    // 配置 markdown-it
    config: (md) => {
      // 可以在这里添加自定义的 markdown-it 插件
    }
  },

  // Head 配置
  head: [
    // Favicon
    ['link', { rel: 'icon', href: '/favicon.ico' }],

    // Meta 标签
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }],

    // Open Graph
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Coding Agent for Research' }],
    ['meta', { property: 'og:description', content: 'LLM Agent 在学术研究中的应用经验分享' }],

    // Twitter Card
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
  ],

  // 构建配置
  srcDir: './',
  outDir: './.vitepress/dist',
  cacheDir: './.vitepress/cache',

  // 忽略死链接检查（开发阶段可以启用）
  ignoreDeadLinks: false,

  // 最后更新时间戳
  lastUpdated: true,

  // 清理 URL（移除 .html 后缀）
  cleanUrls: true,

  // sitemap 配置
  sitemap: {
    hostname: 'https://hjnnjh.github.io/Agents-are-the-future-of-academic-research'
  },

  // Mermaid 配置
  mermaid: {
    // https://mermaid.js.org/config/setup/modules/mermaidAPI.html#mermaidapi-configuration-defaults
  },
  mermaidPlugin: {
    class: 'mermaid'
  }
}))
