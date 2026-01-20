# Technology Templates

## TypeScript/React

### CLAUDE.md
```markdown
# Project Instructions

## Overview
React/TypeScript web application.

## Commands
npm install    # Install dependencies
npm run dev    # Development server
npm test       # Run tests
npm run build  # Production build

## Code Style
- Functional components with hooks
- TypeScript strict mode
- ESLint + Prettier formatting
```

### Suggested Rules
- `frontend.md`: globs `["src/components/**", "*.tsx"]`
- `testing.md`: globs `["**/*.test.*", "__tests__/**"]`

---

## Python/FastAPI

### CLAUDE.md
```markdown
# Project Instructions

## Overview
FastAPI backend application.

## Commands
poetry install  # Install dependencies
poetry run pytest  # Run tests
poetry run uvicorn main:app --reload  # Dev server

## Code Style
- Type hints for all functions
- PEP 8 formatting with ruff
- Pydantic models for validation
```

### Suggested Rules
- `api.md`: globs `["app/api/**", "**/routes/**"]`
- `testing.md`: globs `["tests/**", "**/*_test.py"]`
- `database.md`: globs `["app/models/**", "alembic/**"]`

---

## Go

### CLAUDE.md
```markdown
# Project Instructions

## Overview
Go application.

## Commands
go build ./...       # Build
go test ./...        # Run tests
golangci-lint run    # Lint

## Code Style
- Standard Go formatting (gofmt)
- Explicit error handling
- Package-level documentation
```

### Suggested Rules
- `testing.md`: globs `["**/*_test.go"]`

---

## Rust

### CLAUDE.md
```markdown
# Project Instructions

## Overview
Rust application.

## Commands
cargo build      # Build
cargo test       # Run tests
cargo clippy     # Lint
cargo fmt        # Format

## Code Style
- Explicit error handling (no unwrap in production)
- Descriptive error types
- Documentation comments for public APIs
```

### Suggested Rules
- `testing.md`: globs `["**/tests/**", "**/*_test.rs"]`

---

## Next.js

### CLAUDE.md
```markdown
# Project Instructions

## Overview
Next.js application with App Router.

## Commands
npm install    # Install dependencies
npm run dev    # Development (localhost:3000)
npm test       # Run tests
npm run build  # Production build

## Code Style
- Server Components by default
- Use 'use client' only when needed
- Colocation of related files
```

### Suggested Rules
- `frontend.md`: globs `["src/app/**", "src/components/**"]`
- `api.md`: globs `["src/app/api/**"]`
- `testing.md`: globs `["**/*.test.*", "__tests__/**"]`

---

## Monorepo (Turborepo)

### CLAUDE.md
```markdown
# Project Instructions

## Overview
Monorepo with multiple packages.

## Commands
pnpm install           # Install all dependencies
pnpm build             # Build all packages
pnpm test              # Run all tests
pnpm --filter=<pkg>    # Run command in specific package

## Structure
- apps/: Application packages
- packages/: Shared packages

## Code Style
- Shared configs in packages/config
- Consistent patterns across packages
```

### Suggested Rules
- `frontend.md`: globs `["apps/web/**", "packages/ui/**"]`
- `backend.md`: globs `["apps/api/**", "packages/core/**"]`
- `testing.md`: globs `["**/*.test.*", "**/*.spec.*"]`

---

## Django

### CLAUDE.md
```markdown
# Project Instructions

## Overview
Django web application.

## Commands
pip install -r requirements.txt  # Install
python manage.py runserver       # Dev server
python manage.py test            # Run tests
python manage.py migrate         # Apply migrations

## Code Style
- Class-based views preferred
- Type hints for functions
- Django coding style guide
```

### Suggested Rules
- `api.md`: globs `["**/views.py", "**/serializers.py"]`
- `database.md`: globs `["**/models.py", "**/migrations/**"]`
- `testing.md`: globs `["**/tests/**", "**/test_*.py"]`
