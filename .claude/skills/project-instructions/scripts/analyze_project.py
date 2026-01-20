#!/usr/bin/env python3
"""
Project Analyzer for CLAUDE.md Generation

Analyzes project structure and outputs a JSON summary with recommendations
for memory-efficient project instructions.

Usage:
    python analyze_project.py <project_root> [--max-depth N] [--output FILE]

Output:
    JSON with: technology_stack, directory_structure, file_patterns,
    existing_docs, recommendations
"""

import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Optional

# Technology detection patterns
TECH_MARKERS = {
    # JavaScript/TypeScript
    "package.json": {"stack": "node", "details": ["npm", "javascript"]},
    "tsconfig.json": {"stack": "typescript", "details": ["typescript"]},
    "next.config.js": {"stack": "nextjs", "details": ["react", "nextjs"]},
    "next.config.mjs": {"stack": "nextjs", "details": ["react", "nextjs"]},
    "vite.config.ts": {"stack": "vite", "details": ["vite"]},
    "vite.config.js": {"stack": "vite", "details": ["vite"]},
    # Python
    "pyproject.toml": {"stack": "python", "details": ["python"]},
    "setup.py": {"stack": "python", "details": ["python"]},
    "requirements.txt": {"stack": "python", "details": ["python", "pip"]},
    "Pipfile": {"stack": "python", "details": ["python", "pipenv"]},
    "poetry.lock": {"stack": "python", "details": ["python", "poetry"]},
    # Go
    "go.mod": {"stack": "go", "details": ["go"]},
    "go.sum": {"stack": "go", "details": ["go"]},
    # Rust
    "Cargo.toml": {"stack": "rust", "details": ["rust", "cargo"]},
    # Ruby
    "Gemfile": {"stack": "ruby", "details": ["ruby", "bundler"]},
    # Java/Kotlin
    "pom.xml": {"stack": "java", "details": ["java", "maven"]},
    "build.gradle": {"stack": "java", "details": ["java", "gradle"]},
    "build.gradle.kts": {"stack": "kotlin", "details": ["kotlin", "gradle"]},
    # Docker
    "Dockerfile": {"stack": "docker", "details": ["docker"]},
    "docker-compose.yml": {"stack": "docker", "details": ["docker", "compose"]},
    "docker-compose.yaml": {"stack": "docker", "details": ["docker", "compose"]},
}

# Framework detection in package.json
PACKAGE_JSON_FRAMEWORKS = {
    "react": "react",
    "vue": "vue",
    "angular": "angular",
    "svelte": "svelte",
    "express": "express",
    "fastify": "fastify",
    "nestjs": "nestjs",
    "@nestjs/core": "nestjs",
    "next": "nextjs",
    "nuxt": "nuxt",
    "gatsby": "gatsby",
}

# Documentation files to detect
DOC_FILES = [
    "README.md", "README", "readme.md",
    "CONTRIBUTING.md", "CONTRIBUTING",
    "CHANGELOG.md", "CHANGELOG",
    "LICENSE", "LICENSE.md",
    "ARCHITECTURE.md", "DESIGN.md",
    "API.md", "USAGE.md",
    "docs/", "documentation/",
]

# Directory patterns for rule recommendations
DIR_PATTERNS = {
    "src/components": {"rule": "frontend.md", "globs": ["src/components/**", "*.tsx", "*.jsx"]},
    "src/pages": {"rule": "frontend.md", "globs": ["src/pages/**"]},
    "src/app": {"rule": "frontend.md", "globs": ["src/app/**"]},
    "src/api": {"rule": "api.md", "globs": ["src/api/**", "**/routes/**"]},
    "src/services": {"rule": "backend.md", "globs": ["src/services/**"]},
    "src/lib": {"rule": "backend.md", "globs": ["src/lib/**"]},
    "src/utils": {"rule": "backend.md", "globs": ["src/utils/**"]},
    "tests": {"rule": "testing.md", "globs": ["tests/**", "**/*.test.*", "**/*.spec.*"]},
    "test": {"rule": "testing.md", "globs": ["test/**", "**/*.test.*", "**/*.spec.*"]},
    "__tests__": {"rule": "testing.md", "globs": ["__tests__/**", "**/*.test.*"]},
    "models": {"rule": "database.md", "globs": ["**/models/**", "**/*schema*"]},
    "migrations": {"rule": "database.md", "globs": ["**/migrations/**"]},
    "prisma": {"rule": "database.md", "globs": ["prisma/**"]},
    "docs": {"rule": "documentation.md", "globs": ["docs/**", "**/*.md"]},
}

# File extensions for pattern detection
FILE_EXTENSIONS = {
    ".ts": "typescript",
    ".tsx": "typescript-react",
    ".js": "javascript",
    ".jsx": "javascript-react",
    ".py": "python",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".md": "markdown",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
}


def detect_technology_stack(root: Path) -> dict:
    """Detect technology stack from marker files."""
    detected = {"primary": None, "languages": set(), "frameworks": set(), "tools": set()}

    for marker, info in TECH_MARKERS.items():
        marker_path = root / marker
        if marker_path.exists():
            if detected["primary"] is None:
                detected["primary"] = info["stack"]
            detected["languages"].add(info["stack"])
            detected["tools"].update(info["details"])

    # Check package.json for frameworks
    package_json = root / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                for dep, framework in PACKAGE_JSON_FRAMEWORKS.items():
                    if dep in deps:
                        detected["frameworks"].add(framework)
        except (json.JSONDecodeError, IOError):
            pass

    # Check pyproject.toml for Python frameworks
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            if "fastapi" in content.lower():
                detected["frameworks"].add("fastapi")
            if "django" in content.lower():
                detected["frameworks"].add("django")
            if "flask" in content.lower():
                detected["frameworks"].add("flask")
        except IOError:
            pass

    # Convert sets to lists for JSON serialization
    detected["languages"] = list(detected["languages"])
    detected["frameworks"] = list(detected["frameworks"])
    detected["tools"] = list(detected["tools"])

    return detected


def analyze_directory_structure(root: Path, max_depth: int = 4) -> dict:
    """Analyze directory structure up to max_depth."""
    structure = {"directories": [], "key_dirs": {}, "total_files": 0}

    for dir_pattern, rule_info in DIR_PATTERNS.items():
        check_path = root / dir_pattern
        if check_path.exists() and check_path.is_dir():
            structure["key_dirs"][dir_pattern] = {
                "exists": True,
                "suggested_rule": rule_info["rule"],
                "suggested_globs": rule_info["globs"],
            }

    # Walk directory tree up to max_depth
    def walk_limited(path: Path, current_depth: int):
        if current_depth > max_depth:
            return
        try:
            for item in path.iterdir():
                if item.name.startswith(".") and item.name not in [".claude"]:
                    continue
                if item.name in ["node_modules", "__pycache__", "venv", ".venv", "dist", "build", ".git"]:
                    continue
                if item.is_dir():
                    rel_path = str(item.relative_to(root))
                    if current_depth <= 2:  # Only include top-level directories
                        structure["directories"].append(rel_path)
                    walk_limited(item, current_depth + 1)
                else:
                    structure["total_files"] += 1
        except PermissionError:
            pass

    walk_limited(root, 0)
    return structure


def count_file_patterns(root: Path, max_depth: int = 4) -> dict:
    """Count files by extension."""
    patterns = defaultdict(int)

    def walk_limited(path: Path, current_depth: int):
        if current_depth > max_depth:
            return
        try:
            for item in path.iterdir():
                if item.name.startswith("."):
                    continue
                if item.name in ["node_modules", "__pycache__", "venv", ".venv", "dist", "build", ".git"]:
                    continue
                if item.is_dir():
                    walk_limited(item, current_depth + 1)
                else:
                    ext = item.suffix.lower()
                    if ext in FILE_EXTENSIONS:
                        patterns[FILE_EXTENSIONS[ext]] += 1
                    elif ext:
                        patterns[ext] += 1
        except PermissionError:
            pass

    walk_limited(root, 0)
    return dict(patterns)


def find_existing_docs(root: Path) -> list:
    """Find existing documentation files."""
    docs = []
    for doc in DOC_FILES:
        doc_path = root / doc
        if doc_path.exists():
            docs.append({
                "path": doc,
                "is_directory": doc_path.is_dir(),
                "size": doc_path.stat().st_size if doc_path.is_file() else None,
            })
    return docs


def check_existing_claude_config(root: Path) -> dict:
    """Check for existing CLAUDE.md or .claude/ configuration."""
    config = {"claude_md": False, "claude_dir": False, "rules": []}

    if (root / "CLAUDE.md").exists():
        config["claude_md"] = True

    claude_dir = root / ".claude"
    if claude_dir.exists():
        config["claude_dir"] = True
        rules_dir = claude_dir / "rules"
        if rules_dir.exists():
            config["rules"] = [f.name for f in rules_dir.glob("*.md")]

    return config


def generate_recommendations(tech_stack: dict, structure: dict, patterns: dict, docs: list) -> dict:
    """Generate recommendations for CLAUDE.md and rules."""
    recommendations = {
        "claude_md_sections": [],
        "suggested_rules": [],
        "glob_patterns": {},
        "imports": [],
    }

    # Always recommend these sections
    recommendations["claude_md_sections"] = [
        "Project Overview",
        "Build and Test Commands",
        "Code Style Conventions",
    ]

    # Add technology-specific sections
    if tech_stack.get("primary"):
        recommendations["claude_md_sections"].append(f"{tech_stack['primary'].title()} Specific Guidelines")

    # Suggest rules based on directory structure
    for dir_name, info in structure.get("key_dirs", {}).items():
        if info.get("exists"):
            rule = info["suggested_rule"]
            if rule not in [r["file"] for r in recommendations["suggested_rules"]]:
                recommendations["suggested_rules"].append({
                    "file": rule,
                    "globs": info["suggested_globs"],
                    "reason": f"Found {dir_name}/ directory",
                })

    # Suggest imports for existing docs
    for doc in docs:
        if not doc["is_directory"] and doc["path"].endswith(".md"):
            recommendations["imports"].append({
                "path": doc["path"],
                "suggestion": f"@{doc['path']}",
            })

    # Generate glob patterns based on file patterns
    if patterns.get("typescript") or patterns.get("typescript-react"):
        recommendations["glob_patterns"]["typescript"] = ["*.ts", "*.tsx", "src/**/*.ts"]
    if patterns.get("python"):
        recommendations["glob_patterns"]["python"] = ["*.py", "**/*.py"]
    if patterns.get("go"):
        recommendations["glob_patterns"]["go"] = ["*.go", "**/*.go"]

    return recommendations


def analyze_project(root_path: str, max_depth: int = 4) -> dict:
    """Main analysis function."""
    root = Path(root_path).resolve()

    if not root.exists():
        return {"error": f"Path does not exist: {root_path}"}

    if not root.is_dir():
        return {"error": f"Path is not a directory: {root_path}"}

    # Run all analyses
    tech_stack = detect_technology_stack(root)
    structure = analyze_directory_structure(root, max_depth)
    patterns = count_file_patterns(root, max_depth)
    docs = find_existing_docs(root)
    existing_config = check_existing_claude_config(root)
    recommendations = generate_recommendations(tech_stack, structure, patterns, docs)

    return {
        "project_root": str(root),
        "technology_stack": tech_stack,
        "directory_structure": structure,
        "file_patterns": patterns,
        "existing_docs": docs,
        "existing_claude_config": existing_config,
        "recommendations": recommendations,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze project structure for CLAUDE.md generation"
    )
    parser.add_argument("project_root", help="Path to project root directory")
    parser.add_argument("--max-depth", type=int, default=4, help="Maximum directory depth to analyze")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    result = analyze_project(args.project_root, args.max_depth)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Analysis written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
