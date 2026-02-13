# AGENT-BASICS CATEGORY KNOWLEDGE BASE

**Context:** Core Agent Concepts Content
**Parent:** ../../../AGENTS.md
**Generated:** 2026-02-14

## OVERVIEW
High-quality articles explaining LLM Agent fundamentals: architecture, memory, context engineering, multi-agent collaboration, and evaluation.

## STRUCTURE
```
agent-basics/
├── 2026-02-13-llm-agent-basics.md              # Foundation: Components & workflow
├── 2026-02-14-agent-memory-systems.md          # Memory types & implementation
├── 2026-02-15-context-engineering.md           # Context window optimization
├── 2026-02-16-multi-agent-collaboration.md     # Agent coordination patterns
└── 2026-02-17-agent-evaluation.md              # Metrics & benchmarks
```

## CONVENTIONS
- **Filename Format**: STRICT `YYYY-MM-DD-slug.md`. Determines sidebar order (ascending chronological).
- **Frontmatter**: MANDATORY fields: `title`, `date`, `categories: [agent-basics]`, `tags`, `difficulty`, `summary`.
- **Difficulty Levels**: `beginner`, `intermediate`, `advanced`. Used for reader filtering.
- **Content Style**: 
  - Explain complex concepts in simple terms.
  - Use Mermaid diagrams for architecture (e.g., Agent workflow, memory hierarchy).
  - Include practical examples, not just theory.
  - Chinese-English spacing following "盘古之白" standard.
- **Containers**: Use `:::info 本文概览` for TOC, `:::warning AI 含量说明` for compliance.

## ANTI-PATTERNS
- **Do NOT** use abstract jargon without explanation. Target audience: researchers new to AI.
- **Do NOT** skip frontmatter validation. Build will fail.
- **Do NOT** mix difficulty levels within same article. Choose one and stick to it.
- **Do NOT** create articles outside YYYY-MM-DD format. Sidebar ordering depends on it.

## CONTENT THEMES
1. **Foundation**: Agent components, perception-decision-action loop
2. **Memory**: Short-term, long-term, retrieval strategies
3. **Context**: Window optimization, compression, RAG integration
4. **Collaboration**: Multi-agent patterns, communication protocols
5. **Evaluation**: Metrics, benchmarks, real-world performance

## NOTES
- **Chronological Order**: Articles sorted oldest → newest in sidebar. Do NOT reverse.
- **Image Assets**: Store in `docs/public/images/2025/`. Reference as `/images/2025/filename.png`.
- **Cross-References**: Use relative links to other categories (e.g., `../coding-agent/2026-XX-XX-title.md`).
