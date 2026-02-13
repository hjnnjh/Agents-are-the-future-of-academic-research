# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-13
**Stack:** VitePress 1.5+ (Vue 3, TS), GitHub Pages, Claude Skills

## OVERVIEW
Static technical blog sharing Coding Agent applications in academic research. Single-module VitePress architecture with no backend.

## STRUCTURE
```
.
├── docs/                 # Content source & VitePress config
│   ├── .vitepress/       # Site config, theme, & build logic
│   ├── posts/            # Blog articles (YYYY/MM/DD-slug.md)
│   ├── categories/       # Category index pages
│   └── public/           # Static assets (images)
├── .claude/skills/       # 12+ Custom AI agent skills
└── .github/workflows/    # CI/CD (deploy.yml)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Site Config** | `docs/.vitepress/config.mts` | Nav, Sidebar, SEO, Mermaid |
| **Theme/Styles** | `docs/.vitepress/theme/` | Custom CSS (`custom.css`), Layouts |
| **New Article** | `docs/posts/{YYYY}/` | Follow naming: `YYYY-MM-DD-slug.md` |
| **Static Assets** | `docs/public/img/` | Reference as `/img/...` in MD |
| **AI Skills** | `.claude/skills/` | Tool definitions & logic |
| **CI/CD** | `.github/workflows/deploy.yml` | Build & Deploy to GH Pages |

## CONVENTIONS
- **Frontmatter**: MANDATORY. Must include `title`, `date`, `categories` (from 5 allowed), `tags`.
- **Links**: Use relative paths for internal links. `ignoreDeadLinks: false` enforces validity.
- **Images**: Place in `docs/public/img/`. Reference via absolute path `/img/filename.png` in Markdown.
- **Components**: Use VitePress containers (`:::info`) over raw HTML.
- **Colors**: "Academic Blue" (`#3B82F6`) is the primary theme color.

## ANTI-PATTERNS (THIS PROJECT)
- **Do NOT** place images in root `/img/`. Use `docs/public/img/`.
- **Do NOT** create posts outside `docs/posts/YYYY/`.
- **Do NOT** modify `package.json` scripts without updating `docs/SKILLS-GUIDE.md`.
- **Do NOT** use `Makefile`. Use `npm scripts`.

## COMMANDS
```bash
npm run dev          # Start local dev server (http://localhost:5173)
npm run build        # Production build -> docs/.vitepress/dist
npm run preview      # Preview production build
```

## KNOWN ISSUES
- `scripts/new-post.js` is missing (referenced in `package.json`).
- `docs/index.md` has broken link to 2025 posts (actual: 2026).
- Redundant `img/` directory in root (cleanup needed).
