#!/usr/bin/env python3
"""
Project Instructions Generator

Generates CLAUDE.md and .claude/rules/*.md files from project analysis.

Usage:
    python generate_instructions.py <analysis_json> [--extensions-json FILE] [--output-dir DIR] [--dry-run]

Output:
    Creates CLAUDE.md and .claude/rules/*.md files in the specified output directory.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional


def generate_claude_md(analysis: dict, extensions: Optional[dict] = None) -> str:
    """Generate CLAUDE.md content from analysis."""
    lines = []

    tech_stack = analysis.get("technology_stack", {})
    recommendations = analysis.get("recommendations", {})
    existing_docs = analysis.get("existing_docs", [])

    # Header
    lines.append("# Project Instructions")
    lines.append("")

    # Project Overview
    lines.append("## Overview")
    lines.append("")

    primary = tech_stack.get("primary", "Unknown")
    frameworks = tech_stack.get("frameworks", [])

    if frameworks:
        lines.append(f"This is a {primary} project using {', '.join(frameworks)}.")
    else:
        lines.append(f"This is a {primary} project.")
    lines.append("")

    # Import existing documentation
    if existing_docs:
        readme_doc = next((d for d in existing_docs if "readme" in d["path"].lower()), None)
        if readme_doc:
            lines.append(f"See @{readme_doc['path']} for detailed project documentation.")
            lines.append("")

    # Build and Test Commands
    lines.append("## Build and Test Commands")
    lines.append("")

    # Detect package manager and add commands
    if tech_stack.get("primary") in ["node", "typescript", "nextjs"]:
        lines.append("```bash")
        lines.append("# Install dependencies")
        lines.append("npm install")
        lines.append("")
        lines.append("# Run development server")
        lines.append("npm run dev")
        lines.append("")
        lines.append("# Run tests")
        lines.append("npm test")
        lines.append("")
        lines.append("# Build for production")
        lines.append("npm run build")
        lines.append("```")
    elif tech_stack.get("primary") == "python":
        lines.append("```bash")
        lines.append("# Install dependencies")
        if "poetry" in tech_stack.get("tools", []):
            lines.append("poetry install")
        elif "pipenv" in tech_stack.get("tools", []):
            lines.append("pipenv install")
        else:
            lines.append("pip install -r requirements.txt")
        lines.append("")
        lines.append("# Run tests")
        lines.append("pytest")
        lines.append("")
        lines.append("# Run linter")
        lines.append("ruff check .")
        lines.append("```")
    elif tech_stack.get("primary") == "go":
        lines.append("```bash")
        lines.append("# Build")
        lines.append("go build ./...")
        lines.append("")
        lines.append("# Run tests")
        lines.append("go test ./...")
        lines.append("")
        lines.append("# Run linter")
        lines.append("golangci-lint run")
        lines.append("```")
    elif tech_stack.get("primary") == "rust":
        lines.append("```bash")
        lines.append("# Build")
        lines.append("cargo build")
        lines.append("")
        lines.append("# Run tests")
        lines.append("cargo test")
        lines.append("")
        lines.append("# Run linter")
        lines.append("cargo clippy")
        lines.append("```")
    else:
        lines.append("<!-- TODO: Add build and test commands -->")
    lines.append("")

    # Code Style
    lines.append("## Code Style")
    lines.append("")

    if tech_stack.get("primary") in ["node", "typescript", "nextjs"]:
        lines.append("- Use ESLint and Prettier for formatting")
        lines.append("- Follow existing patterns in the codebase")
        lines.append("- Prefer functional components and hooks (React)")
    elif tech_stack.get("primary") == "python":
        lines.append("- Follow PEP 8 style guidelines")
        lines.append("- Use type hints for function signatures")
        lines.append("- Use ruff for linting and formatting")
    elif tech_stack.get("primary") == "go":
        lines.append("- Follow Go formatting conventions (gofmt)")
        lines.append("- Use meaningful variable and function names")
        lines.append("- Handle errors explicitly")
    elif tech_stack.get("primary") == "rust":
        lines.append("- Follow Rust formatting conventions (rustfmt)")
        lines.append("- Use descriptive error types")
        lines.append("- Prefer explicit error handling over unwrap()")
    else:
        lines.append("- Follow existing patterns in the codebase")
        lines.append("- Keep code readable and well-documented")
    lines.append("")

    # Architecture notes (if any key directories exist)
    key_dirs = analysis.get("directory_structure", {}).get("key_dirs", {})
    if key_dirs:
        lines.append("## Architecture")
        lines.append("")
        for dir_name, info in key_dirs.items():
            if info.get("exists"):
                lines.append(f"- `{dir_name}/`: <!-- TODO: Describe purpose -->")
        lines.append("")

    # Extensions section
    if extensions:
        # Installed Skills
        installed_skills = extensions.get("installed_skills", [])
        if installed_skills:
            lines.append("## Available Skills")
            lines.append("")
            for skill in installed_skills[:5]:  # Limit to 5
                lines.append(f"- **{skill['name']}**: {skill.get('description', 'No description')[:100]}")
            lines.append("")

        # MCPs
        available_mcps = extensions.get("available_mcps", [])
        if available_mcps:
            lines.append("## Available MCPs")
            lines.append("")
            for mcp in available_mcps:
                lines.append(f"- **{mcp['name']}**: Use `mcp__{mcp['name']}__*` tools")
            lines.append("")

        # Subagent recommendations
        subagent_recs = extensions.get("subagent_recommendations", [])
        if subagent_recs:
            lines.append("## Subagent Usage")
            lines.append("")
            lines.append("Use subagents for efficient task execution:")
            lines.append("")
            for rec in subagent_recs[:3]:  # Limit to 3
                lines.append(f"- **{rec['type']}**: {rec.get('recommendation', '')}")
            lines.append("")

    return "\n".join(lines)


def generate_rule_file(rule_name: str, globs: list, tech_stack: dict) -> str:
    """Generate a rule file with appropriate globs and content."""
    lines = []

    # Frontmatter with globs
    lines.append("---")
    lines.append(f"globs: {json.dumps(globs)}")
    lines.append("---")
    lines.append("")

    # Content based on rule type
    if rule_name == "testing.md":
        lines.append("# Testing Conventions")
        lines.append("")
        lines.append("## Test Structure")
        lines.append("")
        lines.append("- Group related tests using describe blocks")
        lines.append("- Use clear, descriptive test names")
        lines.append("- Follow Arrange-Act-Assert pattern")
        lines.append("")
        lines.append("## Mocking")
        lines.append("")
        lines.append("- Mock external dependencies")
        lines.append("- Keep mocks minimal and focused")
        lines.append("")

    elif rule_name == "frontend.md":
        lines.append("# Frontend Conventions")
        lines.append("")
        lines.append("## Component Structure")
        lines.append("")
        if "react" in tech_stack.get("frameworks", []):
            lines.append("- Use functional components with hooks")
            lines.append("- Keep components small and focused")
            lines.append("- Extract reusable logic into custom hooks")
        else:
            lines.append("- Follow component-based architecture")
            lines.append("- Keep components small and focused")
        lines.append("")
        lines.append("## Styling")
        lines.append("")
        lines.append("- Follow existing styling patterns in the project")
        lines.append("- Use consistent naming conventions")
        lines.append("")

    elif rule_name == "api.md":
        lines.append("# API Conventions")
        lines.append("")
        lines.append("## Endpoint Design")
        lines.append("")
        lines.append("- Use RESTful naming conventions")
        lines.append("- Return consistent response formats")
        lines.append("- Handle errors with appropriate status codes")
        lines.append("")
        lines.append("## Validation")
        lines.append("")
        lines.append("- Validate all input data")
        lines.append("- Return clear error messages")
        lines.append("")

    elif rule_name == "backend.md":
        lines.append("# Backend Conventions")
        lines.append("")
        lines.append("## Code Organization")
        lines.append("")
        lines.append("- Separate business logic from infrastructure")
        lines.append("- Use dependency injection where appropriate")
        lines.append("")
        lines.append("## Error Handling")
        lines.append("")
        lines.append("- Use custom error types")
        lines.append("- Log errors with appropriate context")
        lines.append("")

    elif rule_name == "database.md":
        lines.append("# Database Conventions")
        lines.append("")
        lines.append("## Schema Design")
        lines.append("")
        lines.append("- Use descriptive table and column names")
        lines.append("- Define appropriate indexes")
        lines.append("")
        lines.append("## Migrations")
        lines.append("")
        lines.append("- Keep migrations small and reversible")
        lines.append("- Test migrations before applying")
        lines.append("")

    elif rule_name == "documentation.md":
        lines.append("# Documentation Conventions")
        lines.append("")
        lines.append("## Markdown Style")
        lines.append("")
        lines.append("- Use clear, concise language")
        lines.append("- Include code examples where helpful")
        lines.append("- Keep documentation up to date")
        lines.append("")

    else:
        lines.append(f"# {rule_name.replace('.md', '').replace('-', ' ').title()}")
        lines.append("")
        lines.append("<!-- TODO: Add specific conventions for this context -->")
        lines.append("")

    return "\n".join(lines)


def generate_instructions(
    analysis: dict,
    extensions: Optional[dict] = None,
    output_dir: Optional[str] = None,
    dry_run: bool = False
) -> dict:
    """Generate all instruction files."""
    results = {
        "claude_md": None,
        "rules": {},
        "output_dir": output_dir,
    }

    tech_stack = analysis.get("technology_stack", {})
    recommendations = analysis.get("recommendations", {})

    # Generate CLAUDE.md
    claude_md_content = generate_claude_md(analysis, extensions)
    results["claude_md"] = claude_md_content

    # Generate rule files
    for rule_rec in recommendations.get("suggested_rules", []):
        rule_file = rule_rec["file"]
        globs = rule_rec["globs"]
        rule_content = generate_rule_file(rule_file, globs, tech_stack)
        results["rules"][rule_file] = rule_content

    # Write files if not dry run
    if not dry_run and output_dir:
        output_path = Path(output_dir)

        # Write CLAUDE.md
        claude_md_path = output_path / "CLAUDE.md"
        claude_md_path.write_text(claude_md_content)
        print(f"Created: {claude_md_path}", file=sys.stderr)

        # Create .claude/rules directory
        rules_dir = output_path / ".claude" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)

        # Write rule files
        for rule_file, content in results["rules"].items():
            rule_path = rules_dir / rule_file
            rule_path.write_text(content)
            print(f"Created: {rule_path}", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate CLAUDE.md and .claude/rules/*.md files"
    )
    parser.add_argument("analysis_json", help="Path to analysis JSON file from analyze_project.py")
    parser.add_argument("--extensions-json", help="Path to extensions JSON file from discover_extensions.py")
    parser.add_argument("--output-dir", "-o", help="Output directory for generated files")
    parser.add_argument("--dry-run", action="store_true", help="Print content without writing files")

    args = parser.parse_args()

    # Load analysis
    try:
        with open(args.analysis_json) as f:
            analysis = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading analysis file: {e}", file=sys.stderr)
        sys.exit(1)

    # Load extensions if provided
    extensions = None
    if args.extensions_json:
        try:
            with open(args.extensions_json) as f:
                extensions = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load extensions file: {e}", file=sys.stderr)

    # Use project root from analysis if no output dir specified
    output_dir = args.output_dir or analysis.get("project_root")

    result = generate_instructions(analysis, extensions, output_dir, args.dry_run)

    if args.dry_run:
        print("=== CLAUDE.md ===")
        print(result["claude_md"])
        print()
        for rule_file, content in result["rules"].items():
            print(f"=== .claude/rules/{rule_file} ===")
            print(content)
            print()
    else:
        print(json.dumps({
            "claude_md_path": str(Path(output_dir) / "CLAUDE.md"),
            "rules_created": list(result["rules"].keys()),
        }, indent=2))


if __name__ == "__main__":
    main()
