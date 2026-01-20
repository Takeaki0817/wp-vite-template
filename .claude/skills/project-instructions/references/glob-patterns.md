# Glob Patterns Reference

## Basic Syntax

| Pattern | Meaning | Example Match |
|---------|---------|---------------|
| `*` | Any characters except `/` | `*.ts` → `file.ts` |
| `**` | Any characters including `/` | `**/*.ts` → `src/lib/file.ts` |
| `?` | Single character | `file?.ts` → `file1.ts` |
| `{a,b}` | Either a or b | `*.{ts,tsx}` → `file.ts`, `file.tsx` |
| `[abc]` | Character class | `file[123].ts` → `file1.ts` |

## Common Patterns by Purpose

### Testing Files
```
**/*.test.*      # All test files (any extension)
**/*.spec.*      # All spec files
__tests__/**     # Jest test directory
tests/**         # tests directory
test/**          # test directory
```

### Frontend
```
src/components/**    # React/Vue components
src/pages/**         # Page components
src/app/**           # Next.js app directory
*.tsx                # TypeScript React files
*.jsx                # JavaScript React files
*.vue                # Vue single-file components
*.svelte             # Svelte components
```

### Backend/API
```
src/api/**           # API directory
**/routes/**         # Route handlers
**/controllers/**    # Controllers
src/services/**      # Service layer
src/lib/**           # Library code
```

### Database
```
**/models/**         # Model definitions
**/migrations/**     # Database migrations
**/*schema*          # Schema files
prisma/**            # Prisma files
```

### Configuration
```
*.config.*           # Config files
**/config/**         # Config directory
.env*                # Environment files
```

### Documentation
```
**/*.md              # All markdown
docs/**              # Docs directory
*.mdx                # MDX files
```

## Technology-Specific Patterns

### TypeScript/JavaScript
```yaml
globs: ["*.ts", "*.tsx", "*.js", "*.jsx"]
```

### Python
```yaml
globs: ["*.py", "**/*.py"]
```

### Go
```yaml
globs: ["*.go", "**/*.go"]
```

### Rust
```yaml
globs: ["*.rs", "src/**/*.rs"]
```

## Best Practices

1. **Use brace expansion** for similar patterns:
   - Good: `*.{ts,tsx}`
   - Avoid: Two separate rules for `*.ts` and `*.tsx`

2. **Be specific** to avoid over-matching:
   - Good: `src/components/**/*.tsx`
   - Avoid: `**/*.tsx` (may match test files)

3. **Combine patterns** when they share rules:
   - Good: `globs: ["**/*.test.*", "**/*.spec.*", "__tests__/**"]`

4. **Order matters**: More specific patterns should be in separate rule files
