# DOCS KNOWLEDGE BASE

**Context:** Content Source & Configuration
**Parent:** ../AGENTS.md
**Generated:** 2026-02-14

## OVERVIEW
Core content directory for the VitePress blog. Contains articles, static assets, and site configuration.

## STRUCTURE
```
docs/
├── .vitepress/       # Config, theme, build output
├── posts/            # Blog posts ({category}/YYYY-MM-DD-slug.md)
├── categories/       # Index pages for 5 main categories
└── public/           # Static assets (TRANSITION: img/ → images/YYYY/)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Write Post** | `posts/{category}/` | Use `YYYY-MM-DD-slug.md` format |
| **Add Image (Legacy)** | `public/img/` | Ref as `/img/name.png` |
| **Add Image (New)** | `public/images/2025/` | Year-based organization |
| **Edit Sidebar** | `.vitepress/config.mts` | Update `sidebar` object |
| **Customize CSS** | `.vitepress/theme/custom.css` | Academic Blue theme (#3B82F6) |

## CONVENTIONS
- **Frontmatter**: REQUIRED. `title`, `date`, `categories` (from 5 allowed), `tags`, `difficulty`, `summary`.
- **Headings**: Use H2 (`##`) for top-level sections. H1 reserved for title.
- **Components**: Use `:::info`, `:::tip` containers instead of blockquotes for alerts.
- **Links**: Relative paths (`../posts/{category}/...`). `ignoreDeadLinks: false` enforces validity.
- **Images**: TRANSITION PERIOD. Legacy in `public/img/`, new in `public/images/YYYY/`. Choose one path strategy per article.

## ANTI-PATTERNS
- **No HTML**: Avoid raw `<img>` or `<div>`. Use Markdown/Vue syntax.
- **No Absolute Paths**: Do not use `C:/Users/...` or full URLs for internal content.
- **No Dead Links**: Build will FAIL if links are broken.
- **No Mixed Image Paths**: Choose `/img/` OR `/images/2025/` per article. Don't mix.

## CATEGORIES (5 ALLOWED)
1. `agent-basics` — LLM Agent concepts, architecture, mechanisms
2. `coding-agent` — Claude Code, OpenCode usage guides
3. `research-cases` — Real applications in literature/data/writing
4. `tools-comparison` — Agent tool evaluations
5. `insights` — Experience summaries, lessons learned
