#!/usr/bin/env python3
"""
Parse specification files or task lists into parallelizable tasks.

Usage:
    python parse_specification.py <input_file> [--output tasks.json]

Supports:
    - Markdown specification files with ## sections
    - Task lists (- [ ] format or numbered)
    - YAML/JSON task definitions

Output:
    JSON with task definitions including:
    - id, name, description
    - dependencies (if any)
    - estimated_complexity
    - branch_name (auto-generated slug)
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import Optional
from collections import defaultdict


def parse_markdown_spec(content: str) -> list[dict]:
    """Parse markdown specification into tasks."""
    tasks = []

    # Pattern 1: Task list items (- [ ] or - [x])
    task_pattern = r'^[-*]\s*\[[ x]\]\s*(.+)$'

    # Pattern 2: Numbered list (must start line, avoid matching mid-sentence)
    numbered_pattern = r'^\d+\.\s+(.+)$'

    # Pattern 3: Section headers as tasks (## Task: ...)
    section_pattern = r'^##\s+(?:Task\s*\d*:?\s*)?(.+)$'

    lines = content.split('\n')
    task_id = 0
    has_task_list = False

    # First pass: check if there are task list items or numbered lists
    for line in lines:
        if re.match(task_pattern, line) or re.match(numbered_pattern, line):
            has_task_list = True
            break

    for i, line in enumerate(lines):
        # Check for task list items
        match = re.match(task_pattern, line)
        if match:
            task_id += 1
            task_name = match.group(1).strip()
            tasks.append({
                "id": f"task-{task_id}",
                "name": task_name,
                "description": extract_task_description(lines, i),
                "dependencies": extract_dependencies(task_name, tasks),
                "complexity": estimate_complexity(task_name),
                "branch_name": slugify(task_name),
            })
            continue

        # Check for numbered list (only if no task list items found)
        if not has_task_list or not any(re.match(task_pattern, l) for l in lines):
            match = re.match(numbered_pattern, line)
            if match:
                task_id += 1
                task_name = match.group(1).strip()
                tasks.append({
                    "id": f"task-{task_id}",
                    "name": task_name,
                    "description": extract_task_description(lines, i),
                    "dependencies": extract_dependencies(task_name, tasks),
                    "complexity": estimate_complexity(task_name),
                    "branch_name": slugify(task_name),
                })
                continue

        # Check for section headers only if no task lists found
        if not has_task_list:
            match = re.match(section_pattern, line, re.IGNORECASE)
            if match:
                section_name = match.group(1).strip()
                # Skip common non-task sections
                skip_sections = ['overview', 'introduction', 'requirements',
                               'dependencies', 'setup', 'configuration', 'notes',
                               'tasks', 'todo', 'summary', 'background', 'context',
                               'description', 'goals', 'objectives', 'scope',
                               'other', 'misc', 'miscellaneous', 'appendix']
                if section_name.lower() not in skip_sections:
                    task_id += 1
                    tasks.append({
                        "id": f"task-{task_id}",
                        "name": section_name,
                        "description": extract_section_content(lines, i),
                        "dependencies": [],
                        "complexity": "medium",
                        "branch_name": slugify(section_name),
                    })

    return tasks


def extract_task_description(lines: list[str], start_idx: int) -> str:
    """Extract description following a task item."""
    description_lines = []
    indent_pattern = r'^(\s{2,}|\t)'

    for line in lines[start_idx + 1:]:
        if re.match(indent_pattern, line) or (line.strip() and not line.startswith(('-', '*', '#', '\d'))):
            if line.strip() and not re.match(r'^[-*]\s*\[', line) and not re.match(r'^\d+\.', line):
                description_lines.append(line.strip())
            else:
                break
        else:
            break

    return ' '.join(description_lines[:3])  # Limit to 3 lines


def extract_section_content(lines: list[str], start_idx: int) -> str:
    """Extract content under a section header."""
    content_lines = []

    for line in lines[start_idx + 1:]:
        if line.startswith('##'):
            break
        if line.strip():
            content_lines.append(line.strip())

    return ' '.join(content_lines[:5])  # Limit to 5 lines


def extract_dependencies(task_name: str, existing_tasks: list[dict]) -> list[str]:
    """Detect dependencies based on task name keywords."""
    dependencies = []

    # Keywords that suggest dependency on other tasks
    dependency_keywords = {
        'test': ['implement', 'create', 'add', 'build'],
        'integrate': ['implement', 'create', 'add'],
        'document': ['implement', 'create'],
        'deploy': ['test', 'build'],
        'refactor': ['implement', 'create'],
    }

    task_lower = task_name.lower()
    for keyword, deps in dependency_keywords.items():
        if keyword in task_lower:
            for existing in existing_tasks:
                for dep in deps:
                    if dep in existing['name'].lower():
                        dependencies.append(existing['id'])

    return list(set(dependencies))


def estimate_complexity(task_name: str) -> str:
    """Estimate task complexity from name."""
    high_complexity = ['refactor', 'migrate', 'redesign', 'architecture', 'overhaul', 'rewrite']
    low_complexity = ['fix', 'update', 'rename', 'add comment', 'typo', 'bump', 'minor']

    task_lower = task_name.lower()

    if any(kw in task_lower for kw in high_complexity):
        return 'high'
    if any(kw in task_lower for kw in low_complexity):
        return 'low'
    return 'medium'


def slugify(text: str) -> str:
    """Convert text to branch-safe slug."""
    # Remove special characters, replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug[:50]  # Limit length


def analyze_parallelism(tasks: list[dict]) -> dict:
    """Analyze which tasks can run in parallel."""
    # Build dependency graph
    dep_graph = {t['id']: set(t.get('dependencies', [])) for t in tasks}

    # Find independent tasks (no dependencies)
    independent = [t['id'] for t in tasks if not t.get('dependencies')]

    # Group tasks by dependency level
    levels = []
    remaining = set(dep_graph.keys())
    resolved = set()

    while remaining:
        # Find tasks whose dependencies are all resolved
        level = [t for t in remaining if dep_graph[t].issubset(resolved)]
        if not level:
            # Circular dependency or error - force progress
            level = list(remaining)[:1]
        levels.append(level)
        resolved.update(level)
        remaining -= set(level)

    return {
        "independent_tasks": independent,
        "execution_levels": levels,
        "max_parallelism": max(len(level) for level in levels) if levels else 0,
    }


def parse_json_spec(content: str) -> list[dict]:
    """Parse JSON specification."""
    data = json.loads(content)
    tasks = data.get('tasks', data) if isinstance(data, dict) else data

    # Ensure required fields
    result = []
    for i, task in enumerate(tasks):
        if isinstance(task, str):
            task = {"name": task}

        result.append({
            "id": task.get("id", f"task-{i+1}"),
            "name": task.get("name", f"Task {i+1}"),
            "description": task.get("description", ""),
            "dependencies": task.get("dependencies", []),
            "complexity": task.get("complexity", "medium"),
            "branch_name": task.get("branch_name", slugify(task.get("name", f"task-{i+1}"))),
        })

    return result


def parse_specification(input_path: str) -> dict:
    """Main parsing function."""
    path = Path(input_path)

    if not path.exists():
        return {"error": f"File not found: {input_path}"}

    content = path.read_text()

    # Detect format and parse
    if path.suffix == '.json':
        try:
            tasks = parse_json_spec(content)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON: {e}"}
    else:
        # Assume markdown
        tasks = parse_markdown_spec(content)

    if not tasks:
        return {"error": "No tasks found in specification"}

    parallelism = analyze_parallelism(tasks)

    return {
        "source_file": str(path.resolve()),
        "task_count": len(tasks),
        "tasks": tasks,
        "parallelism": parallelism,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse specification into parallelizable tasks"
    )
    parser.add_argument("input_file", help="Specification file (markdown, json)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    args = parser.parse_args()

    result = parse_specification(args.input_file)
    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Tasks written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
