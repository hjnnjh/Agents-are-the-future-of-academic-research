# VITEPRESS CONFIG KNOWLEDGE BASE

**Context:** Site Configuration & Theme
**Parent:** ../../AGENTS.md
**Generated:** 2026-02-14

## OVERVIEW
VitePress core configuration. Controls navigation, sidebar, theme, and build plugins.

## STRUCTURE
```
.vitepress/
├── config.mts          # CENTRAL: Nav, Sidebar, SEO, Plugins
├── theme/
│   ├── index.ts        # Theme entry (imports custom.css)
│   └── custom.css      # Global styles (Academic Blue #3B82F6)
└── cache/              # Build cache (ignore in git)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| **Add Nav Item** | `config.mts` → `themeConfig.nav` | Main header links |
| **Update Sidebar** | `config.mts` → `themeConfig.sidebar` | Category-based structure |
| **Change Theme Color** | `theme/custom.css` → `--vp-c-brand-1` | Academic Blue #3B82F6 |
| **Add Plugin** | `config.mts` → `vite.plugins` | Current: `vitepress-plugin-mermaid` |
| **SEO Settings** | `config.mts` → `head` | Meta tags, favicon |

## CONVENTIONS
- **Sidebar Ordering**: Articles in ascending chronological order (oldest first). Use `reversed: false`.
- **Link Validation**: `ignoreDeadLinks: false` enforces all internal links must be valid.
- **Academic Blue**: `#3B82F6` is the primary brand color. Do not change without design approval.
- **Mermaid Integration**: Configured via `vitepress-plugin-mermaid`. Supports 7 diagram types.
- **Typography**: 1.8x line-height for readability in `custom.css`.

## ANTI-PATTERNS
- **Do NOT** modify `config.mts` without testing build (`npm run build`).
- **Do NOT** add global CSS outside `theme/custom.css`. Centralize styles.
- **Do NOT** hardcode absolute URLs in navigation. Use relative paths.
- **Do NOT** disable `ignoreDeadLinks`. Broken links = build failure by design.

## KEY CONFIG VALUES
```typescript
// config.mts critical settings
base: '/Agents-are-the-future-of-academic-research/'  // GitHub Pages path
ignoreDeadLinks: false                                // Enforce link validity
markdown.math: true                                   // MathJax support
vite.plugins: [MermaidPlugin()]                       // Diagram support
```

## NOTES
- **Build Output**: `docs/.vitepress/dist/` (deployed to GitHub Pages)
- **Cache**: `.vitepress/cache/` is gitignored. Safe to delete if build fails.
- **Favicon**: Located at `docs/public/favicon.ico`. Referenced in `config.mts` head.
