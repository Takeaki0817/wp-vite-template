# Task Agent Prompt Template

Use this template when spawning sub-agents with the Task tool.

## Template

```
You are implementing a specific task in an isolated git worktree.

## Your Task
{task_name}

## Description
{task_description}

## Working Directory
IMPORTANT: All your work must be done in this worktree:
{worktree_path}

You are on branch: {branch_name}

## Implementation Guidelines

1. Stay in your worktree: All file operations must use paths within {worktree_path}
2. Make atomic commits: Commit logical units of work with clear messages
3. Follow project conventions: Match existing code style and patterns
4. Write tests: Add tests for new functionality if the project has tests

## Verification Requirements

Before marking complete, ensure:
1. All changes are committed
2. Tests pass: {test_command}
3. Build succeeds: {build_command}

## Completion Protocol

When finished:
1. Ensure all changes are committed
2. Run verification commands
3. Create completion marker:
   echo '{{"status": "completed", "commits": N}}' > {worktree_path}/.agent-done

If you encounter blocking issues:
1. Document the issue
2. Create failure marker:
   echo '{{"status": "failed", "reason": "description"}}' > {worktree_path}/.agent-failed

## Context
Base branch: {base_branch}
Other parallel tasks (do not modify their code):
{other_tasks}
```

## Variable Reference

| Variable | Source | Example |
|----------|--------|---------|
| {task_name} | tasks.json | "Implement authentication" |
| {task_description} | tasks.json | "Add JWT-based auth..." |
| {worktree_path} | worktree_manager.py output | "/project/.worktree-agents/task-1" |
| {branch_name} | worktree_manager.py output | "wt-agent/implement-auth" |
| {test_command} | Auto-detected or config | "npm test" |
| {build_command} | Auto-detected or config | "npm run build" |
| {base_branch} | state.json | "main" |
| {other_tasks} | state.json | "- task-2: Add payments..." |

## Spawning Example

```python
# Load state
state = json.loads(Path(".worktree-agents/state.json").read_text())

for task in state["tasks"]:
    other_tasks = "\n".join([
        f"- {t['task_id']}: {t['task_name']}"
        for t in state["tasks"] if t["task_id"] != task["task_id"]
    ])

    prompt = TEMPLATE.format(
        task_name=task["task_name"],
        task_description=task.get("task_description", ""),
        worktree_path=task["worktree_path"],
        branch_name=task["branch_name"],
        test_command="npm test",  # or detected command
        build_command="npm run build",
        base_branch=state["base_branch"],
        other_tasks=other_tasks,
    )

    # Use Task tool with run_in_background: true
```
