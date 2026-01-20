#!/usr/bin/env python3
"""
Git Worktree Manager for Parallel Agent Implementation.

Usage:
    python worktree_manager.py setup <tasks.json> [--base-branch <name>] [--worktree-dir <path>]
    python worktree_manager.py list
    python worktree_manager.py status
    python worktree_manager.py cleanup [--force] [--keep-branches]

Commands:
    setup    - Create worktrees for all tasks
    list     - List active worktrees
    status   - Show worktree status with branch info
    cleanup  - Remove all worktrees and optionally branches
"""

import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


DEFAULT_WORKTREE_DIR = ".worktree-agents"
DEFAULT_BRANCH_PREFIX = "wt-agent/"


def run_git(args: list[str], cwd: Optional[str] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command."""
    cmd = ["git"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{result.stderr}")
    return result


def get_repo_root() -> Path:
    """Get the repository root directory."""
    result = run_git(["rev-parse", "--show-toplevel"])
    return Path(result.stdout.strip())


def get_current_branch() -> str:
    """Get current branch name."""
    result = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    return result.stdout.strip()


def get_current_commit() -> str:
    """Get current commit hash."""
    result = run_git(["rev-parse", "HEAD"])
    return result.stdout.strip()


def load_config(repo_root: Path) -> dict:
    """Load configuration from .worktree-agents.json if exists."""
    config_path = repo_root / ".worktree-agents.json"
    if config_path.exists():
        return json.loads(config_path.read_text())
    return {}


def setup_worktrees(tasks_file: str, base_branch: Optional[str] = None,
                    worktree_dir: Optional[str] = None, force: bool = False) -> dict:
    """Create worktrees for all tasks."""
    repo_root = get_repo_root()
    config = load_config(repo_root)

    # Load tasks
    tasks_path = Path(tasks_file)
    if not tasks_path.exists():
        return {"error": f"Tasks file not found: {tasks_file}"}

    tasks_data = json.loads(tasks_path.read_text())
    tasks = tasks_data.get("tasks", [])

    if not tasks:
        return {"error": "No tasks found in tasks file"}

    # Determine directories and branches
    wt_dir = Path(worktree_dir or config.get("worktree_dir", DEFAULT_WORKTREE_DIR))
    if not wt_dir.is_absolute():
        wt_dir = repo_root / wt_dir

    branch_prefix = config.get("branch_prefix", DEFAULT_BRANCH_PREFIX)

    # Create or use base branch
    current_commit = get_current_commit()
    if base_branch:
        # Create base branch from current HEAD if it doesn't exist
        result = run_git(["branch", "--list", base_branch], check=False)
        if not result.stdout.strip():
            run_git(["branch", base_branch])
    else:
        base_branch = get_current_branch()

    # Create worktree directory
    wt_dir.mkdir(parents=True, exist_ok=True)

    # Create state file
    state = {
        "created_at": datetime.now().isoformat(),
        "base_branch": base_branch,
        "base_commit": current_commit,
        "worktree_dir": str(wt_dir),
        "branch_prefix": branch_prefix,
        "tasks": [],
    }

    results = []
    for task in tasks:
        task_id = task["id"]
        branch_name = f"{branch_prefix}{task['branch_name']}"
        worktree_path = wt_dir / task_id

        try:
            # Remove existing worktree if force
            if force and worktree_path.exists():
                run_git(["worktree", "remove", "--force", str(worktree_path)], check=False)
                run_git(["branch", "-D", branch_name], check=False)

            # Create worktree with new branch
            run_git([
                "worktree", "add",
                "-b", branch_name,
                str(worktree_path),
                base_branch
            ])

            task_state = {
                "task_id": task_id,
                "task_name": task["name"],
                "task_description": task.get("description", ""),
                "branch_name": branch_name,
                "worktree_path": str(worktree_path),
                "status": "ready",
            }
            state["tasks"].append(task_state)
            results.append({
                "task_id": task_id,
                "status": "created",
                "worktree": str(worktree_path),
                "branch": branch_name,
            })

        except RuntimeError as e:
            results.append({
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
            })

    # Save state
    state_file = wt_dir / "state.json"
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))

    return {
        "worktree_dir": str(wt_dir),
        "base_branch": base_branch,
        "base_commit": current_commit[:8],
        "tasks_created": len([r for r in results if r["status"] == "created"]),
        "tasks_failed": len([r for r in results if r["status"] == "failed"]),
        "results": results,
        "state_file": str(state_file),
    }


def list_worktrees() -> dict:
    """List all worktrees managed by this tool."""
    repo_root = get_repo_root()

    # Get git worktree list
    result = run_git(["worktree", "list", "--porcelain"])

    worktrees = []
    current = {}

    for line in result.stdout.split('\n'):
        if line.startswith('worktree '):
            if current:
                worktrees.append(current)
            current = {"path": line[9:]}
        elif line.startswith('HEAD '):
            current["head"] = line[5:]
        elif line.startswith('branch '):
            current["branch"] = line[7:].replace("refs/heads/", "")
        elif line == "detached":
            current["detached"] = True

    if current:
        worktrees.append(current)

    # Filter to our managed worktrees
    config = load_config(repo_root)
    wt_dir = config.get("worktree_dir", DEFAULT_WORKTREE_DIR)

    managed = [w for w in worktrees if wt_dir in w.get("path", "")]

    return {
        "total_worktrees": len(worktrees),
        "managed_worktrees": len(managed),
        "worktrees": managed,
    }


def get_status() -> dict:
    """Get detailed status of all managed worktrees."""
    repo_root = get_repo_root()
    config = load_config(repo_root)
    wt_dir = Path(config.get("worktree_dir", DEFAULT_WORKTREE_DIR))

    if not wt_dir.is_absolute():
        wt_dir = repo_root / wt_dir

    state_file = wt_dir / "state.json"
    if not state_file.exists():
        return {"error": "No worktree state found. Run setup first."}

    state = json.loads(state_file.read_text())

    status = []
    for task in state["tasks"]:
        wt_path = Path(task["worktree_path"])

        if not wt_path.exists():
            task_status = {"status": "missing"}
        else:
            # Get commit count vs base
            try:
                result = run_git([
                    "rev-list", "--count",
                    f"{state['base_commit']}..HEAD"
                ], cwd=str(wt_path))
                commit_count = int(result.stdout.strip())
            except Exception:
                commit_count = 0

            # Check for uncommitted changes
            result = run_git(["status", "--porcelain"], cwd=str(wt_path), check=False)
            has_changes = bool(result.stdout.strip())

            # Check for completion markers
            done_marker = wt_path / ".agent-done"
            failed_marker = wt_path / ".agent-failed"

            if done_marker.exists():
                agent_status = "completed"
            elif failed_marker.exists():
                agent_status = "failed"
            elif commit_count > 0 or has_changes:
                agent_status = "in_progress"
            else:
                agent_status = "ready"

            task_status = {
                "status": agent_status,
                "commits_ahead": commit_count,
                "has_uncommitted_changes": has_changes,
            }

        status.append({
            "task_id": task["task_id"],
            "task_name": task["task_name"],
            "branch": task["branch_name"],
            "worktree": task["worktree_path"],
            **task_status,
        })

    return {
        "base_branch": state["base_branch"],
        "base_commit": state["base_commit"][:8],
        "created_at": state["created_at"],
        "tasks": status,
    }


def cleanup(force: bool = False, keep_branches: bool = False) -> dict:
    """Remove all managed worktrees and optionally branches."""
    repo_root = get_repo_root()
    config = load_config(repo_root)
    wt_dir = Path(config.get("worktree_dir", DEFAULT_WORKTREE_DIR))

    if not wt_dir.is_absolute():
        wt_dir = repo_root / wt_dir

    state_file = wt_dir / "state.json"
    if not state_file.exists():
        return {"error": "No worktree state found."}

    state = json.loads(state_file.read_text())

    results = []
    for task in state["tasks"]:
        wt_path = task["worktree_path"]
        branch = task["branch_name"]

        try:
            # Remove worktree
            args = ["worktree", "remove", wt_path]
            if force:
                args.insert(2, "--force")
            run_git(args, check=False)

            # Optionally delete branch
            if not keep_branches:
                run_git(["branch", "-D", branch], check=False)

            results.append({
                "task_id": task["task_id"],
                "status": "removed",
            })
        except Exception as e:
            results.append({
                "task_id": task["task_id"],
                "status": "failed",
                "error": str(e),
            })

    # Remove state file and directory
    try:
        state_file.unlink()
        if wt_dir.exists() and not any(wt_dir.iterdir()):
            wt_dir.rmdir()
    except Exception:
        pass

    # Prune worktree metadata
    run_git(["worktree", "prune"], check=False)

    return {
        "removed": len([r for r in results if r["status"] == "removed"]),
        "failed": len([r for r in results if r["status"] == "failed"]),
        "branches_deleted": not keep_branches,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Git Worktree Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Create worktrees for tasks")
    setup_parser.add_argument("tasks_file", help="Path to tasks.json")
    setup_parser.add_argument("--base-branch", "-b", help="Base branch name")
    setup_parser.add_argument("--worktree-dir", "-d", help="Worktree directory")
    setup_parser.add_argument("--force", "-f", action="store_true")

    # List command
    subparsers.add_parser("list", help="List worktrees")

    # Status command
    subparsers.add_parser("status", help="Show worktree status")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Remove worktrees")
    cleanup_parser.add_argument("--force", "-f", action="store_true")
    cleanup_parser.add_argument("--keep-branches", action="store_true")

    args = parser.parse_args()

    if args.command == "setup":
        result = setup_worktrees(
            args.tasks_file,
            args.base_branch,
            args.worktree_dir,
            args.force
        )
    elif args.command == "list":
        result = list_worktrees()
    elif args.command == "status":
        result = get_status()
    elif args.command == "cleanup":
        result = cleanup(args.force, args.keep_branches)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
