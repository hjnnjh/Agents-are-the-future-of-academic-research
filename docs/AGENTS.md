# DOCS KNOWLEDGE BASE

**Context:** Content Source & Configuration
**Parent:** ../AGENTS.md

## OVERVIEW
Core content directory for the VitePress blog. Contains articles, static assets, and site configuration.

## STRUCTURE
```
docs/
├── .vitepress/       # Config, theme, build output
├── posts/            # Blog posts (YYYY/MM/DD-slug.md)
├── categories/       # Index pages for 5 main categories
└── public/           # Static assets (images, favicon)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Write Post** | `posts/{YYYY}/` | Use `YYYY-MM-DD-slug.md` format |
| **Add Image** | `public/img/` | Ref as `/img/name.png` |
| **Edit Sidebar** | `.vitepress/config.mts` | Update `sidebar` object |
| **Customize CSS** | `.vitepress/theme/custom.css` | Academic Blue theme |

## CONVENTIONS
- **Frontmatter**: REQUIRED. `title`, `date`, `categories` (from list), `tags`, `summary`.
- **Headings**: Use H2 (`##`) for top-level sections. H1 is reserved for title.
- **Components**: Use `:::info`, `:::tip` containers instead of blockquotes for alerts.
- **Links**: Use relative paths (`../posts/2026/...`) for internal links.

## ANTI-PATTERNS
- **No HTML**: Avoid raw `<img>` or `<div>`. Use Markdown/Vue syntax.
- **No Absolute Paths**: Do not use `C:/Users/...` or full URLs for internal content.
- **No Dead Links**: Build will FAIL if links are broken (`ignoreDeadLinks: false`).

## CATEGORIES
1. `agent-basics`
2. `coding-agent`
3. `research-cases`
4. `tools-comparison`
5. `insights`
