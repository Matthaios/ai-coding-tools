# Task Generation Template

This template guides breaking down PRDs into actionable, trackable tasks with subtasks.

## Task Breakdown Principles

### Granularity
- Each task should be completable in one focused session (1-4 hours)
- Tasks should be specific enough that completion is clear
- Subtasks break down complex tasks into smaller steps

### Task Structure
- **Main Tasks**: Major feature components or phases (numbered 1, 2, 3...)
- **Subtasks**: Specific implementation steps (numbered 1.1, 1.2, 2.1...)
- **Task IDs**: Unique identifier format `TASK-{PRD-ID}-{NUMBER}`

### Task Components
Each task should include:
- **ID**: Unique identifier
- **Description**: Clear, actionable description
- **Status**: pending, in_progress, done, blocked, cancelled
- **Dependencies**: Other tasks that must complete first
- **Acceptance Criteria**: How to verify completion

## Task Generation Process

### Step 1: Analyze PRD
- Read through entire PRD
- Identify major components or phases
- Note dependencies between components
- Understand technical requirements

### Step 2: Create Main Tasks
Group work into logical phases:
1. **Setup/Configuration**: Environment, dependencies, project structure
2. **Core Implementation**: Main feature development
3. **Integration**: Connecting with existing systems
4. **Testing**: Unit tests, integration tests, E2E tests
5. **Documentation**: Code comments, user docs, API docs
6. **Deployment**: Build, deploy, monitoring

### Step 3: Break Down into Subtasks
For each main task, create specific subtasks:
- **Setup tasks**: Install packages, configure tools, create files
- **Implementation tasks**: Write specific functions, components, APIs
- **Testing tasks**: Write test cases, run tests, fix issues
- **Documentation tasks**: Write docs, update README, add comments

### Step 4: Assign Task IDs
- Format: `TASK-{PRD-ID}-{NUMBER}`
- Sequential numbering: 001, 002, 003...
- Maintain consistency across task lists

### Step 5: Identify Dependencies
- Mark tasks that depend on others
- Order tasks logically
- Note blocking relationships

## Task List Format

```markdown
# Task List: {PRD Title}

**PRD**: [PRD-{ID}.md](.project/prds/PRD-{ID}.md)
**Generated**: {Date}
**Status**: {Overall Status}

## Progress Summary
- Total Tasks: {X}
- Pending: {Y}
- In Progress: {Z}
- Done: {A}
- Blocked: {B}
- Completion: {C}%

## Tasks

### 1. {Main Task Name}

- [ ] TASK-{ID}-001: {Task Description} [pending]
  - [ ] Subtask 1.1: {Subtask description}
  - [ ] Subtask 1.2: {Subtask description}
  - [ ] Subtask 1.3: {Subtask description}

- [ ] TASK-{ID}-002: {Task Description} [pending]
  - [ ] Subtask 2.1: {Subtask description}
  - [ ] Subtask 2.2: {Subtask description}

### 2. {Next Main Task}

- [ ] TASK-{ID}-003: {Task Description} [pending]
  - [ ] Subtask 3.1: {Subtask description}
  - [ ] Subtask 3.2: {Subtask description}
```

## Task Categories

### Setup Tasks
- Environment configuration
- Dependency installation
- Project structure creation
- Configuration files
- Database setup

### Implementation Tasks
- Feature development
- API endpoints
- UI components
- Business logic
- Data models
- Integration code

### Testing Tasks
- Unit test writing
- Integration test creation
- E2E test setup
- Test execution
- Bug fixes from tests

### Documentation Tasks
- Code comments
- API documentation
- User guides
- README updates
- Architecture docs

### Deployment Tasks
- Build configuration
- Deployment scripts
- Environment setup
- Monitoring setup
- Rollback procedures

## Example Task Breakdown

### Example: User Authentication Feature

**PRD ID**: AUTH

```markdown
### 1. Project Setup and Configuration

- [ ] TASK-AUTH-001: Set up authentication project structure [pending]
  - [ ] Create auth module directory structure
  - [ ] Install authentication dependencies (bcrypt, jwt, etc.)
  - [ ] Configure environment variables
  - [ ] Set up database schema for users

### 2. User Registration

- [ ] TASK-AUTH-002: Implement user registration endpoint [pending]
  - [ ] Create registration route handler
  - [ ] Add input validation
  - [ ] Hash password with bcrypt
  - [ ] Save user to database
  - [ ] Return success response

- [ ] TASK-AUTH-003: Implement email verification [pending]
  - [ ] Generate verification token
  - [ ] Send verification email
  - [ ] Create verification endpoint
  - [ ] Update user status on verification

### 3. User Login

- [ ] TASK-AUTH-004: Implement login endpoint [pending]
  - [ ] Create login route handler
  - [ ] Validate credentials
  - [ ] Generate JWT token
  - [ ] Return token to client
  - [ ] Handle invalid credentials

### 4. Password Management

- [ ] TASK-AUTH-005: Implement password reset [pending]
  - [ ] Create password reset request endpoint
  - [ ] Generate reset token
  - [ ] Send reset email
  - [ ] Create reset password endpoint
  - [ ] Update password in database
```

## Best Practices

1. **Start Small**: Break large tasks into smaller, manageable pieces
2. **Be Specific**: Each task should have a clear, actionable description
3. **Test Early**: Include testing tasks throughout, not just at the end
4. **Consider Dependencies**: Order tasks to respect dependencies
5. **Include Verification**: Each task should have clear acceptance criteria
6. **Update Regularly**: Keep task status current as work progresses

## Task Status Guidelines

- **pending**: Not started, ready to begin
- **in_progress**: Currently being worked on
- **done**: Completed and verified
- **blocked**: Cannot proceed due to dependency or issue
- **cancelled**: No longer needed or replaced

Update status immediately when:
- Starting work on a task → `in_progress`
- Completing a task → `done`
- Encountering a blocker → `blocked`
- Deciding not to do a task → `cancelled`

