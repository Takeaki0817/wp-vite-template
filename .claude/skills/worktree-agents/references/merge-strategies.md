# Merge Strategies Reference

## Strategy Selection

| Scenario | Strategy | Command |
|----------|----------|---------|
| No conflicts detected | Sequential | `merge_assistant.py merge --strategy sequential` |
| Few conflicts | Sequential with stops | Same as above, stops at conflict |
| Many conflicts | Interactive | Manual merge with assistance |

## Sequential Merge

When `merge_assistant.py analyze` shows `conflict_free: true`:

```bash
# Dry run first
python scripts/merge_assistant.py merge --dry-run

# Execute merges
python scripts/merge_assistant.py merge --strategy sequential
```

Process:
1. Checkout target branch
2. Merge each task branch in recommended order
3. If conflict, abort and stop
4. Report results

## Conflict Resolution Patterns

### Non-Overlapping Changes
Different sections of same file:
```
<<<<<<< HEAD
function featureA() { }
=======
function featureB() { }
>>>>>>> branch
```
Resolution: Keep both.

### Competing Implementations
```
<<<<<<< HEAD
const auth = jwt.verify(token);
=======
const auth = validateWithDb(token);
>>>>>>> branch
```
Resolution: Choose more complete, or combine if needed.

### Import Conflicts
```
<<<<<<< HEAD
import { a } from './a';
=======
import { b } from './b';
>>>>>>> branch
```
Resolution: Merge all imports.

## Manual Resolution Workflow

1. Analyze: `python scripts/merge_assistant.py analyze`
2. Review overlapping files
3. Merge in recommended order:
   ```bash
   git checkout main
   git merge wt-agent/task-1
   # resolve if needed
   git add . && git commit
   ```
4. Use resolve helper: `python scripts/merge_assistant.py resolve`

## Post-Merge Verification

```bash
# Run tests
npm test  # or project test command

# Build
npm run build
```

## Rollback

```bash
# Undo last merge (before push)
git reset --hard HEAD~1

# Start over
git checkout main
git reset --hard <base-commit>
```
