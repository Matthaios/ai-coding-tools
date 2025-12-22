#!/usr/bin/env python3
"""
Initialize project task management structure.

Creates .project/ directory structure and configuration file.
Updates .gitignore to exclude project management files.
"""

import os
import json
from pathlib import Path
from datetime import datetime


def create_project_structure(project_root: str = "."):
    """Create .project directory structure."""
    project_dir = Path(project_root) / ".project"

    # Create directories
    prds_dir = project_dir / "prds"
    tasks_dir = project_dir / "tasks"

    prds_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)

    # Create .gitkeep files
    (prds_dir / ".gitkeep").touch()
    (tasks_dir / ".gitkeep").touch()

    return project_dir


def create_config(project_dir: Path, project_name: str = None):
    """Create project configuration file."""
    config_path = project_dir / ".project-config.json"

    if config_path.exists():
        print(f"Config file already exists at {config_path}")
        return config_path

    config = {
        "project_name": project_name or Path(project_dir.parent).name,
        "initialized": datetime.now().isoformat(),
        "task_id_counter": 0,
        "prd_id_counter": 0,
        "ignore_patterns": [
            ".project/tasks/**/node_modules",
            ".project/tasks/**/__pycache__",
            ".project/tasks/**/.env",
            ".project/tasks/**/dist",
            ".project/tasks/**/build"
        ]
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Created config file at {config_path}")
    return config_path


def update_gitignore(project_root: str = "."):
    """Update .gitignore to exclude .project directory."""
    gitignore_path = Path(project_root) / ".gitignore"

    ignore_entry = "\n# Project management files\n.project/\n"

    if not gitignore_path.exists():
        gitignore_path.write_text(ignore_entry)
        print(f"Created .gitignore with project exclusion")
        return

    content = gitignore_path.read_text()

    if ".project/" in content:
        print(".project/ already in .gitignore")
        return

    # Append if not present
    with open(gitignore_path, "a") as f:
        f.write(ignore_entry)

    print(f"Updated .gitignore to exclude .project/")


def main():
    """Main initialization function."""
    project_root = os.getcwd()

    print(f"Initializing project management in {project_root}")

    # Create directory structure
    project_dir = create_project_structure(project_root)
    print(f"Created project directory structure at {project_dir}")

    # Create config file
    project_name = input("Enter project name (or press Enter to use directory name): ").strip()
    if not project_name:
        project_name = None

    create_config(project_dir, project_name)

    # Update .gitignore
    update_gitignore(project_root)

    print("\n✅ Project management initialized successfully!")
    print(f"\nDirectory structure:")
    print(f"  {project_dir}/")
    print(f"    prds/     - Product Requirement Documents")
    print(f"    tasks/    - Task lists and task files")
    print(f"    .project-config.json - Configuration")


if __name__ == "__main__":
    main()

