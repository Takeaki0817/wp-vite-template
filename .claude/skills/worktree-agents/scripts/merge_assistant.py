#!/usr/bin/env python3
"""
Merge Assistant for Worktree Agents.

Usage:
    python merge_assistant.py analyze
    python merge_assistant.py merge [--strategy <sequential|interactive>] [--target <branch>]
    python merge_assistant.py resolve <task_id>

Commands:
    analyze   - Analyze branches for conflicts and suggest merge order
    merge     - Execute merge with specified strategy
    resolve   - Help resolve conflicts for a specific task branch
"""

import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional
from collections import defaultdict


def run_git(args: list[str], cwd: Optional[str] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command."""
    result = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        raise RuntimeError(f"Git failed: {result.stderr}")
    return result


def get_repo_root() -> Path:
    """Get repository root."""
    result = run_git(["rev-parse", "--show-toplevel"])
    return Path(result.stdout.strip())


def load_state() -> Optional[dict]:
    """Load worktree agent state."""
    repo_root = get_repo_root()
    for wt_dir in [".worktree-agents", "worktrees"]:
        state_file = repo_root / wt_dir / "state.json"
        if state_file.exists():
            return json.loads(state_file.read_text())
    return None


def get_branch_files(branch: str, base_commit: str) -> set[str]:
    """Get files modified in branch since base commit."""
    result = run_git([
        "diff", "--name-only",
        f"{base_commit}..{branch}"
    ], check=False)

    if result.returncode == 0:
        return set(result.stdout.strip().split('\n')) - {''}
    return set()


def analyze_conflicts(state: dict) -> dict:
    """Analyze potential conflicts between task branches."""
    base_commit = state["base_commit"]
    tasks = state["tasks"]

    # Get files modified by each branch
    branch_files = {}
    for task in tasks:
        branch = task["branch_name"]
        files = get_branch_files(branch, base_commit)
        branch_files[task["task_id"]] = {
            "branch": branch,
            "task_name": task["task_name"],
            "files": list(files),
            "file_count": len(files),
        }

    # Find overlapping files
    file_to_branches = defaultdict(list)

    for task_id, info in branch_files.items():
        for file in info["files"]:
            file_to_branches[file].append(task_id)

    # Files modified by multiple branches
    overlapping_files = {
        file: branches
        for file, branches in file_to_branches.items()
        if len(branches) > 1
    }

    # Build conflict list
    conflicts = []
    for file, branches in overlapping_files.items():
        conflicts.append({
            "file": file,
            "branches": branches,
            "severity": "high" if len(branches) > 2 else "medium",
        })

    # Calculate merge order (branches with fewer conflicts first)
    branch_conflict_count = defaultdict(int)
    for conflict in conflicts:
        for branch in conflict["branches"]:
            branch_conflict_count[branch] += 1

    # Sort tasks by conflict count (ascending)
    merge_order = sorted(
        tasks,
        key=lambda t: branch_conflict_count.get(t["task_id"], 0)
    )

    return {
        "branch_files": branch_files,
        "potential_conflicts": conflicts,
        "overlapping_files_count": len(overlapping_files),
        "conflict_free": len(conflicts) == 0,
        "recommended_merge_order": [t["task_id"] for t in merge_order],
        "merge_strategy": "sequential" if len(conflicts) == 0 else "interactive",
    }


def try_merge(source_branch: str, target_branch: str,
              message: Optional[str] = None) -> dict:
    """Attempt to merge source into target."""
    # Checkout target
    result = run_git(["checkout", target_branch], check=False)
    if result.returncode != 0:
        return {"success": False, "error": f"Failed to checkout target branch: {result.stderr}"}

    # Try merge
    merge_args = ["merge", source_branch, "--no-edit"]
    if message:
        merge_args.extend(["-m", message])

    result = run_git(merge_args, check=False)

    if result.returncode == 0:
        return {"success": True, "message": "Merge completed successfully"}

    # Check for conflicts
    if "CONFLICT" in result.stdout or "CONFLICT" in result.stderr:
        # Get conflicted files
        status = run_git(["status", "--porcelain"], check=False)
        conflicted = [
            line[3:] for line in status.stdout.split('\n')
            if line.startswith('UU ') or line.startswith('AA ') or line.startswith('DD ')
        ]

        return {
            "success": False,
            "has_conflicts": True,
            "conflicted_files": conflicted,
            "message": "Merge has conflicts that need resolution",
        }

    return {"success": False, "error": result.stderr}


def abort_merge() -> None:
    """Abort current merge."""
    run_git(["merge", "--abort"], check=False)


def sequential_merge(state: dict, analysis: dict, target_branch: Optional[str] = None,
                     dry_run: bool = False) -> dict:
    """Perform sequential merge of all task branches."""
    base_branch = state["base_branch"]
    target = target_branch or base_branch
    merge_order = analysis["recommended_merge_order"]

    # Map task IDs to branch names and names
    task_branches = {t["task_id"]: t["branch_name"] for t in state["tasks"]}
    task_names = {t["task_id"]: t["task_name"] for t in state["tasks"]}

    if dry_run:
        return {
            "dry_run": True,
            "target_branch": target,
            "merge_order": [
                {"task_id": tid, "branch": task_branches.get(tid), "task_name": task_names.get(tid)}
                for tid in merge_order
            ],
            "conflict_free": analysis["conflict_free"],
        }

    results = []
    successful = 0

    for task_id in merge_order:
        branch = task_branches.get(task_id)
        if not branch:
            continue

        # Try merge
        merge_result = try_merge(branch, target, f"Merge {task_id}: {task_names.get(task_id, '')}")

        if merge_result["success"]:
            successful += 1
            results.append({
                "task_id": task_id,
                "branch": branch,
                "status": "merged",
            })
            # Update target to current HEAD for next merge
            target = "HEAD"
        elif merge_result.get("has_conflicts"):
            # Abort and stop
            abort_merge()
            results.append({
                "task_id": task_id,
                "branch": branch,
                "status": "conflict",
                "conflicted_files": merge_result.get("conflicted_files", []),
            })

            # Checkout back to base
            run_git(["checkout", base_branch], check=False)

            return {
                "completed": successful,
                "total": len(merge_order),
                "stopped_at": task_id,
                "reason": "conflict",
                "results": results,
                "next_steps": [
                    f"Resolve conflicts manually: git checkout {base_branch} && git merge {branch}",
                    "After resolving, run merge_assistant.py merge again to continue",
                ],
            }
        else:
            results.append({
                "task_id": task_id,
                "branch": branch,
                "status": "failed",
                "error": merge_result.get("error"),
            })

    return {
        "completed": successful,
        "total": len(merge_order),
        "all_merged": successful == len(merge_order),
        "results": results,
    }


def get_conflict_suggestions(conflicted_files: list[str], task_context: dict) -> dict:
    """Generate suggestions for resolving conflicts."""
    suggestions = {}

    for file in conflicted_files:
        file_suggestions = [
            f"Review changes in {file} from both branches",
            "Consider the task goals when deciding which changes to keep:",
        ]

        for task_id, info in task_context.items():
            file_suggestions.append(f"  - {task_id}: {info.get('task_name', 'Unknown task')}")

        file_suggestions.extend([
            "",
            "Resolution patterns:",
            "1. Keep both changes if they modify different sections",
            "2. Prefer the more complete implementation",
            "3. Combine logic if both changes are needed",
            "",
            f"After resolving: git add {file}",
        ])

        suggestions[file] = file_suggestions

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Merge Assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyze command
    subparsers.add_parser("analyze", help="Analyze branches for conflicts")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Execute merge")
    merge_parser.add_argument(
        "--strategy", "-s",
        choices=["sequential", "interactive"],
        default="sequential"
    )
    merge_parser.add_argument("--target", "-t", help="Target branch")
    merge_parser.add_argument("--dry-run", action="store_true")

    # Resolve command
    resolve_parser = subparsers.add_parser("resolve", help="Help resolve conflicts")
    resolve_parser.add_argument("task_id", nargs="?", help="Task ID with conflicts")

    args = parser.parse_args()

    state = load_state()
    if not state:
        print(json.dumps({"error": "No worktree state found. Run worktree_manager.py setup first."}, indent=2))
        sys.exit(1)

    if args.command == "analyze":
        analysis = analyze_conflicts(state)
        print(json.dumps(analysis, indent=2, ensure_ascii=False))

    elif args.command == "merge":
        analysis = analyze_conflicts(state)

        if args.dry_run:
            result = sequential_merge(state, analysis, args.target, dry_run=True)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.strategy == "sequential":
            result = sequential_merge(state, analysis, args.target)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({
                "message": "Interactive merge requires manual intervention",
                "analysis": analysis,
                "instructions": [
                    "1. Review conflicts in analysis",
                    "2. Merge branches one at a time using git merge",
                    "3. Resolve conflicts as they occur",
                    "4. Use 'resolve' command for assistance",
                ],
            }, indent=2, ensure_ascii=False))

    elif args.command == "resolve":
        # Get current conflicts
        status = run_git(["status", "--porcelain"], check=False)
        conflicted = [
            line[3:] for line in status.stdout.split('\n')
            if line.startswith('UU ') or line.startswith('AA ') or line.startswith('DD ')
        ]

        if not conflicted:
            print(json.dumps({"message": "No conflicts to resolve"}, indent=2))
        else:
            # Build task context
            task_context = {}
            if args.task_id:
                task = next((t for t in state["tasks"] if t["task_id"] == args.task_id), None)
                if task:
                    task_context[args.task_id] = task
            else:
                for task in state["tasks"]:
                    task_context[task["task_id"]] = task

            suggestions = get_conflict_suggestions(conflicted, task_context)

            print(json.dumps({
                "conflicted_files": conflicted,
                "suggestions": suggestions,
                "commands": {
                    "view_diff": "git diff --name-only --diff-filter=U",
                    "abort_merge": "git merge --abort",
                    "continue_after_resolve": "git add <resolved-files> && git commit",
                },
            }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
