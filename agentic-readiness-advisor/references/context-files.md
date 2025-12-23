# AI Context File Templates

Templates and examples for creating effective AI context files that improve agentic coding workflows.

## Table of Contents

1. [CLAUDE.md / AGENTS.md Template](#claudemd--agentsmd-template)
2. [Spec Template](#spec-template)
3. [Architecture Context](#architecture-context)
4. [API Context](#api-context)
5. [Testing Context](#testing-context)

---

## CLAUDE.md / AGENTS.md Template

Place at project root to provide AI agents with essential context.

```markdown
# Project Context for AI Agents

## Project Overview
[1-2 sentences describing what this project does]

## Tech Stack
- **Frontend**: [framework, version]
- **Backend**: [framework, version]
- **Database**: [type, name]
- **Key Libraries**: [list major dependencies]

## Project Structure
```
src/
├── components/    # React components
├── hooks/         # Custom hooks
├── services/      # API layer
├── utils/         # Shared utilities
└── types/         # TypeScript types
```

## Key Patterns

### [Pattern Name]
[Brief description of pattern used in this project]

Example:
```typescript
// Example code showing the pattern
```

## Constraints & Rules

- **DO**: [Things to always do]
- **DO NOT**: [Anti-patterns to avoid]
- **PREFER**: [Preferred approaches]

## Common Pitfalls

1. **[Pitfall Name]**: [What goes wrong and how to avoid it]
2. **[Pitfall Name]**: [What goes wrong and how to avoid it]

## Testing Approach

- Unit tests: [location, framework]
- Integration tests: [location, framework]
- E2E tests: [location, framework]

Run tests: `[command]`

## Build & Deploy

- Development: `[command]`
- Production build: `[command]`
- Deploy: `[process description]`

## Environment Variables

Required variables (see `.env.example`):
- `API_URL`: [description]
- `DATABASE_URL`: [description]
```

---

## Spec Template

Use for new features before implementation.

```markdown
# Feature: [Feature Name]

## Status: [Draft/In Review/Approved]

## Overview

[2-3 sentences describing the feature]

## Requirements

### Functional Requirements
- [ ] FR1: [Requirement]
- [ ] FR2: [Requirement]

### Non-Functional Requirements
- [ ] NFR1: [Performance, security, etc.]

## User Stories

As a [user type], I want to [action] so that [benefit].

## Technical Design

### Data Models
```typescript
interface FeatureData {
  id: string;
  // ...
}
```

### API Changes
- `POST /api/feature` - [description]
- `GET /api/feature/:id` - [description]

### Component Structure
```
components/
└── Feature/
    ├── Feature.tsx
    ├── Feature.test.tsx
    └── useFeature.ts
```

## Edge Cases

1. **[Edge case]**: [How to handle]
2. **[Edge case]**: [How to handle]

## Testing Strategy

- Unit tests for: [list]
- Integration tests for: [list]
- E2E tests for: [list]

## Open Questions

- [ ] [Question needing resolution]

## Implementation Tasks

1. [ ] [Task 1]
2. [ ] [Task 2]
3. [ ] [Task 3]
```

---

## Architecture Context

Document for explaining system architecture to AI agents.

```markdown
# Architecture Overview

## System Diagram

```
[ASCII diagram or description of system components]
```

## Layer Responsibilities

### Presentation Layer
- Location: `src/components/`, `src/pages/`
- Responsibility: UI rendering, user interaction
- Dependencies: Application layer only

### Application Layer
- Location: `src/services/`, `src/hooks/`
- Responsibility: Business logic orchestration
- Dependencies: Domain layer only

### Domain Layer
- Location: `src/domain/`, `src/types/`
- Responsibility: Core business rules
- Dependencies: None

### Infrastructure Layer
- Location: `src/api/`, `src/db/`
- Responsibility: External system integration
- Dependencies: Application layer interfaces

## Key Decisions

### [Decision Name]
**Context**: [Why decision was needed]
**Decision**: [What was decided]
**Consequences**: [Trade-offs and implications]

## Boundaries

### Module Boundaries
- `auth/` - Authentication and authorization
- `users/` - User management
- `products/` - Product catalog

### API Boundaries
- Internal APIs: `src/api/internal/`
- External APIs: `src/api/external/`

## Data Flow

1. User action triggers component event
2. Component calls service method
3. Service orchestrates domain logic
4. Repository handles data persistence
5. Response flows back through layers
```

---

## API Context

Document for API endpoints and contracts.

```markdown
# API Reference

## Base URL
- Development: `http://localhost:3000/api`
- Production: `https://api.example.com`

## Authentication
[Describe auth mechanism]

## Endpoints

### [Resource Name]

#### GET /resource
**Description**: [What it does]

**Query Parameters**:
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| limit | number | No | Max results |

**Response**:
```json
{
  "data": [],
  "pagination": {}
}
```

**Errors**:
- 400: Invalid parameters
- 401: Unauthorized

#### POST /resource
**Description**: [What it does]

**Body**:
```json
{
  "field": "value"
}
```

**Response**: 201 Created

## Error Format

All errors return:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

## Rate Limits
- [Describe rate limiting]
```

---

## Testing Context

Document for test patterns and utilities.

```markdown
# Testing Guide

## Test Organization

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/            # End-to-end tests
└── utils/          # Test utilities
```

## Running Tests

```bash
# All tests
npm test

# Unit tests only
npm run test:unit

# With coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

## Test Utilities

### Render Helper
```typescript
import { render } from '@/tests/utils';

// Provides all necessary providers
render(<Component />);
```

### Mock Factories
```typescript
import { createMockUser } from '@/tests/factories';

const user = createMockUser({ name: 'Test' });
```

### API Mocking
```typescript
import { server } from '@/tests/mocks/server';
import { rest } from 'msw';

server.use(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json({ users: [] }));
  })
);
```

## Test Patterns

### Component Tests
```typescript
describe('Component', () => {
  it('renders correctly', () => {
    render(<Component />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    render(<Component />);
    await user.click(screen.getByRole('button'));
    expect(screen.getByText('Clicked')).toBeInTheDocument();
  });
});
```

### Hook Tests
```typescript
describe('useHook', () => {
  it('returns expected value', () => {
    const { result } = renderHook(() => useHook());
    expect(result.current.value).toBe(expected);
  });
});
```

## Coverage Requirements
- Minimum: 80% overall
- Critical paths: 100%
```
