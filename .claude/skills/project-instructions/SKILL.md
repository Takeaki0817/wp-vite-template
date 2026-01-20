---
name: project-instructions
description: プロジェクト指示の自動生成スキル。「CLAUDE.mdを作成」「プロジェクト指示を生成」「.claude/rulesを設定」「プロジェクトメモリを最適化」「Claude Code用にプロジェクトを分析」「create project instructions」「generate CLAUDE.md」「setup claude rules」「optimize project memory」などの要求時に使用。新規・既存プロジェクト両対応。サブエージェント・Skills・MCPの自動探索と推奨機能付き。
---

# Project Instructions Generator

メモリ効率の良い CLAUDE.md と .claude/rules/*.md を自動生成するスキル。

## Overview

Claude Code のメモリ階層を活用し、コンテキスト効率を最大化するプロジェクト指示を生成する。

**生成物:**
- `CLAUDE.md`: 常時ロードされるプロジェクト全体の指示
- `.claude/rules/*.md`: 条件付きロードされるファイルタイプ別ルール

**自動探索:**
- インストール済み Skills
- 利用可能な MCP サーバー
- 推奨サブエージェントパターン

## Workflow

```
1. Analyze project structure
   └─> Run scripts/analyze_project.py

2. Discover extensions
   └─> Run scripts/discover_extensions.py

3. Generate instructions
   └─> Run scripts/generate_instructions.py

4. Review and customize
   └─> Edit generated files as needed
```

### New Project vs Existing Project

**New project:**
1. Run full analysis
2. Generate all files
3. Customize templates

**Existing project (has CLAUDE.md):**
1. Run analysis
2. Review recommendations
3. Merge or update existing files

## Analysis Phase

### Step 1: Analyze Project Structure

```bash
python scripts/analyze_project.py <project_root> --output analysis.json
```

**Detects:**
- Technology stack (package.json, pyproject.toml, go.mod, etc.)
- Directory structure and patterns
- Existing documentation (README, CONTRIBUTING)
- File type distribution

**Output example:**
```json
{
  "technology_stack": {
    "primary": "typescript",
    "frameworks": ["react", "nextjs"]
  },
  "recommendations": {
    "suggested_rules": [
      {"file": "frontend.md", "globs": ["src/components/**"]}
    ]
  }
}
```

### Step 2: Discover Extensions

```bash
python scripts/discover_extensions.py --project-root <path> --analysis analysis.json
```

**Discovers:**
- Installed skills in `~/.claude/skills/`
- MCP servers from `.mcp.json` or `~/.mcp.json`
- Recommended subagent patterns

## Generation Phase

### Step 3: Generate Instructions

```bash
python scripts/generate_instructions.py analysis.json --extensions-json extensions.json --output-dir <project_root>
```

**Creates:**
- `CLAUDE.md` at project root
- `.claude/rules/*.md` based on detected patterns

**Dry run preview:**
```bash
python scripts/generate_instructions.py analysis.json --dry-run
```

## Content Placement Guide

### What Goes in CLAUDE.md (Always Loaded)

- Build and test commands
- Universal code style conventions
- Architecture overview
- @imports for existing documentation
- Available Skills and MCPs

### What Goes in .claude/rules/ (Conditionally Loaded)

| Rule File | Globs | Content |
|-----------|-------|---------|
| `testing.md` | `**/*.test.*`, `**/*.spec.*` | Test conventions, mocking patterns |
| `frontend.md` | `src/components/**`, `*.tsx` | Component patterns, styling |
| `api.md` | `src/api/**`, `**/routes/**` | API design, validation |
| `database.md` | `**/models/**`, `**/migrations/**` | Schema patterns, migration rules |
| `documentation.md` | `**/*.md`, `docs/**` | Documentation style |

## Token Budget

Keep files concise:

| File | Target | Max |
|------|--------|-----|
| CLAUDE.md | 100-200 lines | 300 lines |
| Individual rule | 30-50 lines | 100 lines |
| Total rules/ | 200-300 lines | 500 lines |

## Subagent Recommendations

Based on project size and complexity:

| Subagent | When to Recommend |
|----------|-------------------|
| **Explore** | Large codebase (>500 files), unfamiliar code navigation |
| **Plan** | Multi-file features, architectural changes |
| **Bash** | Git operations, build/test commands |
| **general-purpose** | Complex multi-step workflows |

Example instruction to add:
```markdown
## Subagent Usage
- Use Explore agent for navigating unfamiliar code areas
- Use Plan agent before implementing multi-file features
```

## Context Efficiency Tips

1. **Use @imports** - Reference docs instead of duplicating:
   ```markdown
   See @README.md for detailed documentation.
   ```

2. **Specific globs** - Avoid broad patterns:
   - Good: `src/components/**/*.tsx`
   - Avoid: `**/*.tsx`

3. **No duplication** - Content in ONE place only

4. **Progressive detail** - Overview in CLAUDE.md, details in rules/

## Resources

### Scripts
- `scripts/analyze_project.py` - Project structure analysis
- `scripts/discover_extensions.py` - Skills/MCP/Subagent discovery
- `scripts/generate_instructions.py` - File generation

### References
- `references/glob-patterns.md` - Glob pattern syntax and examples
- `references/memory-hierarchy.md` - Memory system details
- `references/technology-templates.md` - Stack-specific templates
