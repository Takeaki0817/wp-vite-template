# Memory Hierarchy Guide

## Overview

Claude Code uses a hierarchical memory system that loads instructions based on context.

## Memory Levels

### Level 1: ~/.claude/CLAUDE.md (Global)
- **Loaded**: Always, for all projects
- **Use for**: Personal preferences, global coding conventions
- **Priority**: Lowest (overridden by project-level)

### Level 2: CLAUDE.md (Project Root)
- **Loaded**: Always when working in project
- **Use for**: Project-wide instructions, build commands, core conventions
- **Priority**: Medium

### Level 3: .claude/rules/*.md (Conditional)
- **Loaded**: Only when glob patterns match current file context
- **Use for**: File-type or directory-specific rules
- **Priority**: Highest (most specific)

## Content Placement Decision Matrix

| Content Type | Always Needed? | Placement |
|--------------|----------------|-----------|
| Build commands | Yes | CLAUDE.md |
| Test commands | Yes | CLAUDE.md |
| Code style (universal) | Yes | CLAUDE.md |
| Architecture overview | Yes | CLAUDE.md |
| Test conventions | When testing | .claude/rules/testing.md |
| Frontend patterns | When frontend | .claude/rules/frontend.md |
| API conventions | When API | .claude/rules/api.md |
| Database rules | When DB | .claude/rules/database.md |

## Token Budget Guidelines

| File | Target | Max |
|------|--------|-----|
| CLAUDE.md | 100-200 lines | 300 lines |
| Individual rule file | 30-50 lines | 100 lines |
| Total rules/ | 200-300 lines | 500 lines |

## @import Syntax

Reference existing documentation instead of duplicating:

```markdown
# Project Overview

See @README.md for detailed documentation.
See @CONTRIBUTING.md for contribution guidelines.
```

## Glob Pattern in Rules

```yaml
---
globs: ["**/*.test.*", "**/*.spec.*"]
---

# Testing Conventions
...
```

## Priority Resolution

When multiple rules apply, more specific globs take priority:
1. `src/components/Button.tsx` matches both `**/*.tsx` and `src/components/**`
2. Rules from `src/components/**` will be applied

## Optimization Strategies

### 1. Keep CLAUDE.md Lean
- Only essential, always-needed information
- Reference external docs with @imports
- Move conditional content to rules/

### 2. Use Specific Globs
- Avoid overly broad patterns like `**/*`
- Target specific directories or file types
- Combine related patterns in one rule file

### 3. Avoid Duplication
- Information should exist in ONE place only
- Either in CLAUDE.md OR in a rule file
- Use @imports for shared content

### 4. Progressive Detail
- CLAUDE.md: High-level overview
- rules/: Detailed, context-specific guidance
