#!/usr/bin/env python3
"""
Extension Discovery for Claude Code Projects

Discovers available Skills, MCPs, and recommends Subagent usage patterns
based on project analysis.

Usage:
    python discover_extensions.py [--project-root PATH] [--output FILE]

Output:
    JSON with: installed_skills, available_mcps, subagent_recommendations
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional
import re

# Default paths
SKILLS_DIR = Path.home() / ".claude" / "skills"
MCP_CONFIG_PATHS = [
    Path.home() / ".mcp.json",
    Path(".mcp.json"),
]

# Subagent types and their use cases
SUBAGENT_TYPES = {
    "Explore": {
        "description": "Fast codebase exploration",
        "tools": ["Glob", "Grep", "Read", "LS"],
        "triggers": [
            "Large codebase (>500 files)",
            "Unfamiliar code exploration",
            "Pattern search across multiple files",
        ],
    },
    "Plan": {
        "description": "Implementation planning",
        "tools": ["Read-only exploration tools"],
        "triggers": [
            "Multi-file feature implementation",
            "Architectural changes",
            "Complex refactoring",
        ],
    },
    "Bash": {
        "description": "Command execution",
        "tools": ["Bash"],
        "triggers": [
            "Git operations",
            "Build and test commands",
            "System operations",
        ],
    },
    "general-purpose": {
        "description": "Complex multi-step tasks",
        "tools": ["All tools"],
        "triggers": [
            "Research tasks",
            "Multi-step workflows",
            "Tasks requiring multiple tool types",
        ],
    },
}


def discover_skills() -> list:
    """Discover installed skills in ~/.claude/skills/."""
    skills = []

    if not SKILLS_DIR.exists():
        return skills

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            content = skill_md.read_text()

            # Parse YAML frontmatter
            frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)

                # Extract name
                name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
                name = name_match.group(1).strip() if name_match else skill_dir.name

                # Extract description
                desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
                description = desc_match.group(1).strip() if desc_match else ""

                skills.append({
                    "name": name,
                    "path": str(skill_dir),
                    "description": description[:200] + "..." if len(description) > 200 else description,
                })
        except IOError:
            continue

    return skills


def discover_mcps(project_root: Optional[Path] = None) -> list:
    """Discover available MCP servers from config files."""
    mcps = []
    checked_paths = []

    # Add project-specific path if provided
    if project_root:
        MCP_CONFIG_PATHS.insert(0, project_root / ".mcp.json")

    for config_path in MCP_CONFIG_PATHS:
        checked_paths.append(str(config_path))
        if not config_path.exists():
            continue

        try:
            with open(config_path) as f:
                config = json.load(f)

            servers = config.get("mcpServers", {})
            for name, server_config in servers.items():
                mcps.append({
                    "name": name,
                    "config_path": str(config_path),
                    "command": server_config.get("command", ""),
                    "args": server_config.get("args", []),
                })
        except (json.JSONDecodeError, IOError):
            continue

    return mcps


def recommend_subagents(analysis: Optional[dict] = None) -> list:
    """Recommend subagent usage based on project analysis."""
    recommendations = []

    # Default recommendations
    recommendations.append({
        "type": "Explore",
        "info": SUBAGENT_TYPES["Explore"],
        "recommendation": "Use for initial codebase exploration and pattern discovery",
        "example_prompt": "Explore the codebase to understand the authentication flow",
    })

    recommendations.append({
        "type": "Plan",
        "info": SUBAGENT_TYPES["Plan"],
        "recommendation": "Use before implementing multi-file features",
        "example_prompt": "Plan the implementation of a new API endpoint",
    })

    # Add recommendations based on analysis
    if analysis:
        total_files = analysis.get("directory_structure", {}).get("total_files", 0)

        if total_files > 1000:
            recommendations.append({
                "type": "Explore",
                "info": SUBAGENT_TYPES["Explore"],
                "recommendation": f"Large codebase ({total_files} files) - strongly recommend Explore agent for navigation",
                "priority": "high",
            })

        tech_stack = analysis.get("technology_stack", {})
        if tech_stack.get("frameworks"):
            recommendations.append({
                "type": "general-purpose",
                "info": SUBAGENT_TYPES["general-purpose"],
                "recommendation": f"For complex tasks involving {', '.join(tech_stack['frameworks'])}",
                "example_prompt": "Research and implement best practices for this framework",
            })

    return recommendations


def generate_skill_recommendations(analysis: Optional[dict] = None, installed_skills: list = None) -> list:
    """Generate recommendations for skills to use or install."""
    recommendations = []
    installed_names = {s["name"] for s in (installed_skills or [])}

    if not analysis:
        return recommendations

    tech_stack = analysis.get("technology_stack", {})
    frameworks = tech_stack.get("frameworks", [])

    # Map frameworks to potentially useful skills
    skill_suggestions = {
        "react": ["frontend-design", "component-builder"],
        "nextjs": ["frontend-design", "nextjs-patterns"],
        "fastapi": ["api-design", "python-patterns"],
        "django": ["django-patterns", "api-design"],
        "express": ["api-design", "node-patterns"],
    }

    for framework in frameworks:
        suggested = skill_suggestions.get(framework, [])
        for skill_name in suggested:
            if skill_name in installed_names:
                recommendations.append({
                    "skill": skill_name,
                    "status": "installed",
                    "reason": f"Useful for {framework} development",
                })
            else:
                recommendations.append({
                    "skill": skill_name,
                    "status": "suggested",
                    "reason": f"Consider installing for {framework} development",
                })

    return recommendations


def discover_extensions(project_root: Optional[str] = None, analysis: Optional[dict] = None) -> dict:
    """Main discovery function."""
    root = Path(project_root).resolve() if project_root else None

    # Discover installed skills
    installed_skills = discover_skills()

    # Discover MCPs
    available_mcps = discover_mcps(root)

    # Get subagent recommendations
    subagent_recommendations = recommend_subagents(analysis)

    # Get skill recommendations
    skill_recommendations = generate_skill_recommendations(analysis, installed_skills)

    return {
        "installed_skills": installed_skills,
        "available_mcps": available_mcps,
        "subagent_recommendations": subagent_recommendations,
        "skill_recommendations": skill_recommendations,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Discover available Skills, MCPs, and Subagent patterns"
    )
    parser.add_argument("--project-root", help="Path to project root directory")
    parser.add_argument("--analysis", help="Path to analysis JSON file from analyze_project.py")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    # Load analysis if provided
    analysis = None
    if args.analysis:
        try:
            with open(args.analysis) as f:
                analysis = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load analysis file: {e}", file=sys.stderr)

    result = discover_extensions(args.project_root, analysis)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Discovery results written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
