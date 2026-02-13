# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-14
**Commit:** ef16499
**Branch:** main
**Stack:** VitePress 1.5.0 (Vue 3, TS), GitHub Pages, 16 Claude Skills

## OVERVIEW
Static technical blog sharing Coding Agent applications in academic research. Single-module VitePress architecture with no backend. Core asset: 16 AI Skills in `.claude/skills/` for content production workflow.

## STRUCTURE
```
.
├── docs/                 # Content source & VitePress config
│   ├── .vitepress/       # Site config (config.mts), theme (custom.css, index.ts)
│   ├── posts/            # Blog articles (STRICT: {category}/YYYY-MM-DD-slug.md)
│   ├── categories/       # 5 category index pages (ascending order)
│   └── public/           # Static assets (img/ for legacy, images/YYYY/ for new)
├── .claude/skills/       # 16 AI Skills (mermaid-tools, fact-checker, etc.)
└── .github/workflows/    # CI/CD (deploy.yml)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Site Config** | `docs/.vitepress/config.mts` | Nav, Sidebar, SEO, Mermaid plugin |
| **Global Styles** | `docs/.vitepress/theme/custom.css` | Academic Blue (#3B82F6), 1.8x line-height |
| **New Article** | `docs/posts/{category}/` | MANDATORY: `YYYY-MM-DD-slug.md`, frontmatter validation |
| **Images (Legacy)** | `docs/public/img/` | Reference as `/img/...`. BEING MIGRATED to `/images/YYYY/` |
| **Images (New)** | `docs/public/images/2025/` | Year-based organization for long-term scalability |
| **AI Skills** | `.claude/skills/{skill-name}/SKILL.md` | 16 atomic modules for content production |
| **CI/CD** | `.github/workflows/deploy.yml` | Build & Deploy to GH Pages |

## SHARED RESOURCES
| Resource | Purpose | Dependents |
|----------|---------|------------|
| `docs/.vitepress/config.mts` | Central config: nav, sidebar, Mermaid plugin | All pages |
| `docs/.vitepress/theme/custom.css` | Global styles: Academic Blue, typography | All pages |
| `.claude/skills/` | Reusable AI logic for content workflow | Claude Code tool |

## CONVENTIONS
- **Writing Style**: Simple explanations for complex concepts. No jargon overload.
- **Article Ordering**: Ascending chronological (oldest first) in categories & sidebar. Homepage uses reverse order.
- **Frontmatter**: MANDATORY. `title`, `date`, `categories` (from 5 allowed), `tags`, `difficulty`, `summary`.
- **Links**: Relative paths. `ignoreDeadLinks: false` enforces validity.
- **Images**: TRANSITION PERIOD. Legacy in `public/img/`, new in `public/images/YYYY/`. Reference as `/img/...` or `/images/YYYY/...`.
- **Containers**: Use `:::info`, `:::warning`, `:::tip` over raw HTML.
- **Academic Blue**: `#3B82F6` (primary theme color).

## ANTI-PATTERNS (THIS PROJECT)
- **Do NOT** place images in root `/img/`. Use `docs/public/img/` or `docs/public/images/YYYY/`.
- **Do NOT** create posts outside `docs/posts/{category}/`. No flat structure.
- **Do NOT** modify `package.json` without updating `docs/SKILLS-GUIDE.md`.
- **Do NOT** use `Makefile`. All ops via `npm scripts`.
- **Do NOT** skip frontmatter. Build WILL fail.
- **Do NOT** use absolute file paths in content.
- **Do NOT** use raw HTML (`<img>`, `<div>`). Use Markdown/VitePress containers.

## CATEGORIES (5 ALLOWED)
1. `agent-basics` — LLM Agent concepts, architecture, mechanisms
2. `coding-agent` — Claude Code, OpenCode usage guides
3. `research-cases` — Real applications in literature/data/writing
4. `tools-comparison` — Agent tool evaluations
5. `insights` — Experience summaries, lessons learned

## COMMANDS
```bash
npm run dev          # Dev server (http://localhost:5173)
npm run build        # Production build -> docs/.vitepress/dist
npm run preview      # Preview production build
```

## NOTES
- **Scripts directory**: `package.json` references `scripts/new-post.js` but directory doesn't exist. Use AI Skills instead.
- **Image path migration**: Active transition from `img/` to `images/YYYY/`. Update references gradually.
