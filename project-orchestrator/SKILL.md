---
name: project-orchestrator
description: Project management orchestrator for AI-assisted development workflows. Manages PRD creation, task breakdown, progress tracking, and project planning. Use when (1) initializing project task management system, (2) creating new PRDs for features or changes, (3) generating task lists from PRDs, (4) checking project status and pending tasks, (5) updating task status (in progress, done, blocked), (6) planning new changes or features, (7) organizing tasks with IDs and subfolders, or (8) managing project documentation and task tracking.
---

# Project Orchestrator

Act as a project management orchestrator helping manage AI-assisted development workflows through structured PRD creation, task breakdown, and progress tracking.

## Core Principles

### Project Structure
All project management files are organized under `.project/` directory:
- `.project/prds/` - Product Requirement Documents
- `.project/tasks/` - Task lists and individual task files
- `.project/tasks/{task-id}/` - Subfolders for each task (optional, for complex tasks)
- `.project/.project-config.json` - Project configuration and metadata

### Task Identification
- Each task has a unique ID format: `TASK-{PRD-ID}-{NUMBER}` (e.g., `TASK-AUTH-001`)
- PRDs use format: `PRD-{FEATURE-NAME}.md` (e.g., `PRD-user-authentication.md`)
- Task lists use format: `TASKS-{PRD-ID}.md` (e.g., `TASKS-AUTH.md`)

### Status Tracking
Tasks can have the following statuses:
- `pending` - Not started
- `in_progress` - Currently being worked on
- `done` - Completed
- `blocked` - Blocked by dependencies or issues
- `cancelled` - Cancelled or no longer needed

## Workflow: Initialize Project

When initializing project task management for the first time:

1. **Check if already initialized** → Look for `.project/` directory
2. **Create directory structure**:
   ```
   .project/
   ├── prds/
   ├── tasks/
   └── .project-config.json
   ```
3. **Create `.project-config.json`** with:
   - Project name
   - Initialization date
   - Task ID counter
   - Ignore patterns (what should be excluded from task management)
4. **Update `.gitignore`** → Add `.project/` to ignore list (or specific patterns)
5. **Confirm initialization** → Inform user of setup completion

**Script**: Use `scripts/init_project.py` to automate initialization.

## Workflow: Create PRD

When user wants to create a new Product Requirement Document:

1. **Gather requirements** → Ask targeted questions:
   - What feature or change needs to be built?
   - Who is the target user/audience?
   - What problem does this solve?
   - What are the key requirements?
   - Are there any constraints or dependencies?
   - What defines success for this feature?

2. **Reference existing codebase** → If user mentions files, examine them for context

3. **Generate PRD** → Use template from `references/create-prd-template.md`:
   - Title and Overview
   - Problem Statement
   - Target Users
   - Requirements (functional and non-functional)
   - Success Criteria
   - Dependencies and Constraints
   - Out of Scope

4. **Save PRD** → Save to `.project/prds/PRD-{feature-name}.md`

5. **Generate unique PRD ID** → Use format like `AUTH`, `PAYMENT`, etc. based on feature

6. **Offer to generate tasks** → Ask if user wants to generate task list from PRD

## Workflow: Generate Tasks from PRD

When generating tasks from a PRD:

1. **Read PRD file** → Load the PRD from `.project/prds/`

2. **Break down into tasks** → Use template from `references/generate-tasks-template.md`:
   - Create main tasks (numbered 1, 2, 3...)
   - Create subtasks (numbered 1.1, 1.2, 2.1...)
   - Each task should be:
     - Specific and actionable
     - Testable/verifiable
     - Small enough to complete in one session

3. **Assign task IDs** → Format: `TASK-{PRD-ID}-{NUMBER}` (e.g., `TASK-AUTH-001`)

4. **Set initial status** → All tasks start as `pending`

5. **Create task list file** → Save to `.project/tasks/TASKS-{PRD-ID}.md` with:
   - PRD reference
   - Task list with IDs, descriptions, and status
   - Progress summary

6. **Optionally create task subfolders** → For complex tasks, create `.project/tasks/{task-id}/` directories

## Workflow: Check Project Status

When user asks about project status or pending tasks:

1. **Scan task files** → Read all `TASKS-*.md` files in `.project/tasks/`

2. **Aggregate status**:
   - Count tasks by status
   - List pending tasks
   - List in-progress tasks
   - Show completion percentage

3. **Display summary**:
   ```
   Project Status:
   - Total PRDs: X
   - Total Tasks: Y
   - Pending: Z
   - In Progress: A
   - Done: B
   - Blocked: C
   - Completion: D%
   ```

4. **List pending tasks** → Show task IDs, descriptions, and which PRD they belong to

## Workflow: Update Task Status

When marking tasks as done or updating status:

1. **Locate task** → Find task in appropriate `TASKS-*.md` file by ID

2. **Update status** → Change status marker:
   - `- [ ]` → `- [x]` for done
   - Add status label: `[pending]`, `[in_progress]`, `[done]`, `[blocked]`, `[cancelled]`

3. **Update progress summary** → Recalculate completion percentages

4. **Confirm update** → Inform user of status change

5. **Check dependencies** → If task is done, check if any blocked tasks can now proceed

## Workflow: Plan New Change

When user wants to plan a new change or feature:

1. **Understand the change** → Ask clarifying questions:
   - Is this a new feature or modification to existing?
   - Does it relate to existing PRDs?
   - What's the scope?

2. **Check existing PRDs** → List relevant PRDs that might be affected

3. **Create new PRD or update existing**:
   - If new feature → Create new PRD
   - If modification → Update existing PRD or create related PRD

4. **Generate tasks** → Follow "Generate Tasks from PRD" workflow

5. **Check for conflicts** → Ensure new tasks don't conflict with existing in-progress work

## Workflow: Organize Tasks

When managing task organization:

1. **Task subfolders** → For complex tasks, create `.project/tasks/{task-id}/` with:
   - Implementation notes
   - Related files
   - Test results
   - Documentation

2. **Task linking** → Reference related tasks in task descriptions

3. **PRD linking** → Link tasks back to their PRD in task descriptions

## File Formats

### PRD Format
See `assets/templates/prd-template.md` for PRD structure.

### Task List Format
See `assets/templates/task-list-template.md` for task list structure.

### Task Format
Each task entry:
```markdown
- [ ] TASK-{ID}-{NUMBER}: {Task Description} [status]
  - Subtask 1
  - Subtask 2
```

## Resources

- **PRD Template**: See [references/create-prd-template.md](references/create-prd-template.md) for PRD creation guidance
- **Task Generation Template**: See [references/generate-tasks-template.md](references/generate-tasks-template.md) for task breakdown patterns
- **Init Script**: Use `scripts/init_project.py` to initialize project structure
- **Status Script**: Use `scripts/check_status.py` to check project status programmatically
- **Templates**: See `assets/templates/` for PRD and task list templates

## Guidelines

### When Creating PRDs
- Ask specific, targeted questions
- Reference existing codebase when relevant
- Be thorough but concise
- Include success criteria

### When Generating Tasks
- Break down into small, actionable items
- Each task should be completable in one session
- Include both implementation and testing tasks
- Consider dependencies between tasks

### When Tracking Status
- Always update task status immediately after completion
- Keep progress summaries accurate
- Notify user of significant status changes
- Check for blocked tasks that can be unblocked

### When Organizing
- Use consistent naming conventions
- Keep task IDs unique and traceable
- Link related tasks and PRDs
- Maintain clear folder structure

## Response Style

When orchestrating projects:
- Be proactive in suggesting next steps
- Show clear progress indicators
- Ask clarifying questions when scope is unclear
- Provide summaries after major operations
- Always confirm before making structural changes

When checking status:
- Provide clear, visual summaries
- Highlight urgent or blocked items
- Show completion percentages
- List actionable next steps

