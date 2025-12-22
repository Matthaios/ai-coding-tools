#!/usr/bin/env python3
"""
Check project status and display summary of PRDs and tasks.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def find_task_files(project_dir: Path):
    """Find all task list files."""
    tasks_dir = project_dir / "tasks"
    if not tasks_dir.exists():
        return []

    return list(tasks_dir.glob("TASKS-*.md"))


def parse_task_file(task_file: Path):
    """Parse a task file and extract task information."""
    content = task_file.read_text()

    tasks = []
    current_main_task = None

    # Pattern to match task lines: - [ ] TASK-ID-XXX: Description [status]
    task_pattern = re.compile(r'- \[([ x])\] TASK-(\w+)-(\d+):\s*(.+?)(?:\s+\[(\w+)\])?$', re.MULTILINE)

    for match in task_pattern.finditer(content):
        checked = match.group(1) == 'x'
        prd_id = match.group(2)
        task_num = match.group(3)
        description = match.group(4).strip()
        status = match.group(5) or ('done' if checked else 'pending')

        task_id = f"TASK-{prd_id}-{task_num}"
        tasks.append({
            'id': task_id,
            'prd_id': prd_id,
            'description': description,
            'status': status,
            'file': task_file.name
        })

    return tasks


def find_prd_files(project_dir: Path):
    """Find all PRD files."""
    prds_dir = project_dir / "prds"
    if not prds_dir.exists():
        return []

    return list(prds_dir.glob("PRD-*.md"))


def get_status_summary(project_dir: Path):
    """Get overall project status summary."""
    task_files = find_task_files(project_dir)
    prd_files = find_prd_files(project_dir)

    all_tasks = []
    for task_file in task_files:
        tasks = parse_task_file(task_file)
        all_tasks.extend(tasks)

    # Count by status
    status_counts = defaultdict(int)
    for task in all_tasks:
        status_counts[task['status']] += 1

    total_tasks = len(all_tasks)
    done_tasks = status_counts.get('done', 0)
    completion = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return {
        'total_prds': len(prd_files),
        'total_tasks': total_tasks,
        'pending': status_counts.get('pending', 0),
        'in_progress': status_counts.get('in_progress', 0),
        'done': done_tasks,
        'blocked': status_counts.get('blocked', 0),
        'cancelled': status_counts.get('cancelled', 0),
        'completion': round(completion, 1),
        'tasks': all_tasks
    }


def print_status_summary(summary: dict):
    """Print formatted status summary."""
    print("\n" + "="*60)
    print("PROJECT STATUS SUMMARY")
    print("="*60)
    print(f"\n📋 PRDs: {summary['total_prds']}")
    print(f"📝 Total Tasks: {summary['total_tasks']}")
    print(f"\nStatus Breakdown:")
    print(f"  ⏳ Pending:     {summary['pending']}")
    print(f"  🔄 In Progress:  {summary['in_progress']}")
    print(f"  ✅ Done:        {summary['done']}")
    print(f"  🚫 Blocked:     {summary['blocked']}")
    print(f"  ❌ Cancelled:   {summary['cancelled']}")
    print(f"\n📊 Completion: {summary['completion']}%")

    # Show pending tasks
    pending = [t for t in summary['tasks'] if t['status'] == 'pending']
    if pending:
        print(f"\n⏳ Pending Tasks ({len(pending)}):")
        for task in pending[:10]:  # Show first 10
            print(f"  - {task['id']}: {task['description'][:60]}...")
        if len(pending) > 10:
            print(f"  ... and {len(pending) - 10} more")

    # Show in-progress tasks
    in_progress = [t for t in summary['tasks'] if t['status'] == 'in_progress']
    if in_progress:
        print(f"\n🔄 In Progress Tasks ({len(in_progress)}):")
        for task in in_progress:
            print(f"  - {task['id']}: {task['description'][:60]}...")

    # Show blocked tasks
    blocked = [t for t in summary['tasks'] if t['status'] == 'blocked']
    if blocked:
        print(f"\n🚫 Blocked Tasks ({len(blocked)}):")
        for task in blocked:
            print(f"  - {task['id']}: {task['description'][:60]}...")

    print("\n" + "="*60)


def main():
    """Main status check function."""
    project_root = os.getcwd()
    project_dir = Path(project_root) / ".project"

    if not project_dir.exists():
        print("❌ Project not initialized. Run init_project.py first.")
        return

    summary = get_status_summary(project_dir)
    print_status_summary(summary)


if __name__ == "__main__":
    main()

