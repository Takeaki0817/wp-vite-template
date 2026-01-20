#!/usr/bin/env python3
"""
Progress Monitor for Worktree Agents.

Usage:
    python progress_monitor.py [--watch] [--json] [--interval <seconds>]

Monitors:
    - Agent task status (from completion markers)
    - Branch commit progress
    - Test/build results
    - Overall completion percentage
"""

import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime


def run_git(args: list[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    """Run a git command."""
    return subprocess.run(
        ["git"] + args,
        capture_output=True, text=True, cwd=cwd
    )


def get_repo_root() -> Path:
    """Get repository root."""
    result = run_git(["rev-parse", "--show-toplevel"])
    return Path(result.stdout.strip())


def load_state() -> Optional[dict]:
    """Load worktree agent state."""
    repo_root = get_repo_root()

    # Check for state file
    for wt_dir in [".worktree-agents", "worktrees"]:
        state_file = repo_root / wt_dir / "state.json"
        if state_file.exists():
            return json.loads(state_file.read_text())

    return None


def check_worktree_status(worktree_path: str, base_commit: str) -> dict:
    """Check status of a single worktree."""
    wt_path = Path(worktree_path)

    if not wt_path.exists():
        return {"status": "missing", "exists": False}

    status = {"exists": True}

    # Get commit count ahead of base
    result = run_git([
        "rev-list", "--count",
        f"{base_commit}..HEAD"
    ], cwd=str(wt_path))

    if result.returncode == 0:
        status["commits_ahead"] = int(result.stdout.strip())
    else:
        status["commits_ahead"] = 0

    # Get latest commit info
    result = run_git([
        "log", "-1", "--format=%H|%s|%cr"
    ], cwd=str(wt_path))

    if result.returncode == 0 and result.stdout.strip():
        parts = result.stdout.strip().split("|")
        if len(parts) >= 3:
            status["latest_commit"] = {
                "hash": parts[0][:8],
                "message": parts[1][:60],
                "relative_time": parts[2],
            }

    # Check for uncommitted changes
    result = run_git(["status", "--porcelain"], cwd=str(wt_path))
    status["uncommitted_changes"] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

    # Check for marker files
    done_marker = wt_path / ".agent-done"
    failed_marker = wt_path / ".agent-failed"

    if done_marker.exists():
        status["status"] = "completed"
        try:
            status["completion_info"] = json.loads(done_marker.read_text())
        except (json.JSONDecodeError, Exception):
            status["completion_info"] = {"message": done_marker.read_text().strip()}
    elif failed_marker.exists():
        status["status"] = "failed"
        try:
            status["failure_info"] = json.loads(failed_marker.read_text())
        except (json.JSONDecodeError, Exception):
            status["failure_info"] = {"message": failed_marker.read_text().strip()}
    elif status["commits_ahead"] > 0 or status["uncommitted_changes"] > 0:
        status["status"] = "in_progress"
    else:
        status["status"] = "pending"

    return status


def detect_verification_commands(repo_root: Path) -> dict:
    """Detect test/build commands from project configuration."""
    commands = {}

    # Check package.json
    pkg_json = repo_root / "package.json"
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text())
            scripts = pkg.get("scripts", {})
            if "test" in scripts:
                commands["test"] = "npm test"
            if "build" in scripts:
                commands["build"] = "npm run build"
            if "lint" in scripts:
                commands["lint"] = "npm run lint"
        except json.JSONDecodeError:
            pass

    # Check Makefile
    makefile = repo_root / "Makefile"
    if makefile.exists():
        content = makefile.read_text()
        if "test:" in content:
            commands["test"] = "make test"
        if "build:" in content:
            commands["build"] = "make build"

    # Check pyproject.toml
    pyproject = repo_root / "pyproject.toml"
    if pyproject.exists():
        commands["test"] = "pytest"

    # Check Cargo.toml
    cargo = repo_root / "Cargo.toml"
    if cargo.exists():
        commands["test"] = "cargo test"
        commands["build"] = "cargo build"

    return commands


def run_verification(worktree_path: str, commands: dict) -> dict:
    """Run verification commands in worktree."""
    results = {}

    for name, cmd in commands.items():
        try:
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                cwd=worktree_path,
                timeout=300  # 5 minute timeout
            )
            results[name] = {
                "success": result.returncode == 0,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            results[name] = {"success": False, "error": "timeout"}
        except Exception as e:
            results[name] = {"success": False, "error": str(e)}

    return results


def get_progress_report(run_verification_checks: bool = False) -> dict:
    """Generate comprehensive progress report."""
    state = load_state()

    if not state:
        return {"error": "No worktree agent state found. Run setup first."}

    repo_root = get_repo_root()
    verification_commands = detect_verification_commands(repo_root)

    report = {
        "timestamp": datetime.now().isoformat(),
        "base_branch": state["base_branch"],
        "base_commit": state["base_commit"][:8],
        "created_at": state["created_at"],
        "total_tasks": len(state["tasks"]),
        "verification_commands": verification_commands,
        "tasks": [],
        "summary": {
            "completed": 0,
            "in_progress": 0,
            "pending": 0,
            "failed": 0,
        },
    }

    for task in state["tasks"]:
        task_status = check_worktree_status(
            task["worktree_path"],
            state["base_commit"]
        )

        task_report = {
            "task_id": task["task_id"],
            "task_name": task["task_name"],
            "branch": task["branch_name"],
            "worktree": task["worktree_path"],
            **task_status,
        }

        # Run verification if requested and task is completed
        if run_verification_checks and task_status.get("status") == "completed":
            task_report["verification"] = run_verification(
                task["worktree_path"],
                verification_commands
            )

        report["tasks"].append(task_report)

        # Update summary
        status = task_status.get("status", "pending")
        if status in report["summary"]:
            report["summary"][status] += 1

    # Calculate overall progress
    total = report["total_tasks"]
    completed = report["summary"]["completed"]
    report["summary"]["progress_percent"] = round(completed / total * 100, 1) if total > 0 else 0

    return report


def format_progress_display(report: dict) -> str:
    """Format progress report for terminal display."""
    lines = []

    lines.append("=" * 60)
    lines.append("WORKTREE AGENTS PROGRESS")
    lines.append("=" * 60)
    lines.append(f"Base: {report['base_branch']} ({report['base_commit']})")
    lines.append(f"Started: {report['created_at']}")
    lines.append("")

    # Summary bar
    summary = report["summary"]
    progress = summary["progress_percent"]
    bar_width = 40
    filled = int(bar_width * progress / 100)
    bar = "#" * filled + "-" * (bar_width - filled)
    lines.append(f"Progress: [{bar}] {progress}%")
    lines.append(f"Completed: {summary['completed']}/{report['total_tasks']}")
    lines.append(f"In Progress: {summary['in_progress']} | Pending: {summary['pending']} | Failed: {summary['failed']}")
    lines.append("")

    # Task details
    lines.append("-" * 60)
    for task in report["tasks"]:
        status_icon = {
            "completed": "[OK]",
            "in_progress": "[..]",
            "pending": "[  ]",
            "failed": "[XX]",
            "missing": "[??]",
        }.get(task.get("status", "unknown"), "[??]")

        commits = task.get("commits_ahead", 0)
        changes = task.get("uncommitted_changes", 0)

        lines.append(f"{status_icon} {task['task_name'][:45]}")
        lines.append(f"     Branch: {task['branch']}")
        lines.append(f"     Commits: {commits} | Uncommitted: {changes}")

        if task.get("latest_commit"):
            commit = task["latest_commit"]
            msg = commit['message'][:35] + "..." if len(commit['message']) > 35 else commit['message']
            lines.append(f"     Latest: {msg} ({commit['relative_time']})")

        if task.get("failure_info"):
            lines.append(f"     Error: {task['failure_info'].get('message', 'Unknown error')[:50]}")

        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Monitor worktree agent progress")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch mode")
    parser.add_argument("--interval", "-i", type=int, default=30, help="Watch interval (seconds)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--verify", "-v", action="store_true", help="Run verification checks")

    args = parser.parse_args()

    if args.watch:
        try:
            while True:
                report = get_progress_report(args.verify)

                # Clear screen
                print("\033[2J\033[H", end="")

                if args.json:
                    print(json.dumps(report, indent=2, ensure_ascii=False))
                else:
                    print(format_progress_display(report))

                # Check if all done
                if report.get("summary", {}).get("progress_percent", 0) == 100:
                    print("\nAll tasks completed!")
                    break

                if report.get("summary", {}).get("failed", 0) > 0:
                    print("\nSome tasks failed. Check status for details.")

                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    else:
        report = get_progress_report(args.verify)

        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(format_progress_display(report))


if __name__ == "__main__":
    main()
