---
name: code-quality-enforcer
description: Expert advisor for automated code quality enforcement. Use when (1) writing custom ESLint rules for project-specific standards, (2) setting up pre-commit hooks with Husky, (3) configuring lint-staged for targeted linting, (4) convincing teams to adopt quality gates, (5) using AST exploration for custom rules, (6) automating code formatting with Prettier, (7) designing testable architecture patterns, or (8) gradually introducing standards to a legacy codebase.
---

# Code Quality Enforcer

Expert guidance for automating code standards and quality gates. Core philosophy: **let automation be the enforcer, not people**.

## Core Principles

### 1. Automation Over Manual Review

Systems should enforce rules so humans don't have to be the bad guy. Nobody wants to be the person who constantly blocks PRs for formatting issues.

```
BAD:  "Hey, you forgot to format this file again..."
GOOD: PR fails automatically, author fixes before review
```

### 2. Gradual Adoption

Don't flip the switch on 100 new lint rules overnight. Add rules:
- After incidents ("We had a bug because of X, let's prevent it")
- One at a time
- With team buy-in

### 3. Lead by Example

If you want standards adopted:
- Follow them yourself first
- Show the benefits through your own code
- Make it easy to comply (auto-fix, clear error messages)

### 4. Don't Make It Painful

If your pre-commit hooks take 5 minutes, people will use `--no-verify`. Keep checks:
- Fast (lint changed files only)
- Focused (format and lint, not full test suite)
- Fixable (auto-fix when possible)

## Pre-Commit Hooks with Husky

### Installation

```bash
# Install Husky
npm install -D husky

# Initialize
npx husky init

# This creates:
# - .husky/ directory
# - .husky/pre-commit hook
# - "prepare": "husky" in package.json
```

### Basic Pre-Commit Hook

```bash
# .husky/pre-commit
npm run lint
npm run format:check
```

### With lint-staged (Recommended)

Only lint/format files that changed - much faster:

```bash
npm install -D lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts,jsx,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,css}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

### Installation for New Team Members

The `prepare` script runs automatically after `npm install`:

```json
{
  "scripts": {
    "prepare": "husky"
  }
}
```

## Custom ESLint Rules

### Why Custom Rules?

- Enforce project-specific conventions
- Prevent recurring bugs
- Auto-fix common mistakes
- Replace manual code review comments

### Understanding the AST

ESLint parses code into an Abstract Syntax Tree. Explore at [astexplorer.net](https://astexplorer.net):

```javascript
// This code:
console.log("hello");

// Becomes:
{
  type: "ExpressionStatement",
  expression: {
    type: "CallExpression",
    callee: {
      type: "MemberExpression",
      object: { type: "Identifier", name: "console" },
      property: { type: "Identifier", name: "log" }
    },
    arguments: [{ type: "Literal", value: "hello" }]
  }
}
```

### Basic Rule Structure

```javascript
// eslint-rules/no-console-log.js
module.exports = {
  meta: {
    type: 'problem',            // or 'suggestion', 'layout'
    docs: {
      description: 'Disallow console.log',
    },
    fixable: 'code',            // Enable auto-fix
    schema: [],                 // Rule options
  },
  
  create(context) {
    return {
      // Visit CallExpression nodes
      CallExpression(node) {
        if (
          node.callee.type === 'MemberExpression' &&
          node.callee.object.name === 'console' &&
          node.callee.property.name === 'log'
        ) {
          context.report({
            node,
            message: 'Unexpected console.log',
            fix(fixer) {
              // Auto-fix: remove the statement
              return fixer.remove(node.parent);
            }
          });
        }
      }
    };
  }
};
```

### Using Custom Rules

```javascript
// eslint.config.js
import noConsoleLog from './eslint-rules/no-console-log.js';

export default [
  {
    plugins: {
      custom: {
        rules: {
          'no-console-log': noConsoleLog
        }
      }
    },
    rules: {
      'custom/no-console-log': 'error'
    }
  }
];
```

### Example: Prefer Custom API

```javascript
// eslint-rules/prefer-api-client.js
// Enforce using our apiClient over raw fetch

module.exports = {
  meta: {
    type: 'suggestion',
    docs: {
      description: 'Prefer apiClient over fetch',
    },
    fixable: 'code',
  },
  
  create(context) {
    return {
      CallExpression(node) {
        if (node.callee.name === 'fetch') {
          context.report({
            node,
            message: 'Use apiClient instead of fetch for API calls',
            fix(fixer) {
              return fixer.replaceText(node.callee, 'apiClient.fetch');
            }
          });
        }
      }
    };
  }
};
```

## Testable Architecture Patterns

Good architecture makes testing easier. Bad architecture makes you mock everything.

### Dependency Injection with Defaults

```typescript
// BAD: Hard to test, must mock fetch
async function getUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

// GOOD: Easy to test, no mocking needed
async function getUser(
  id: string,
  fetcher = fetch  // Inject with default
) {
  const res = await fetcher(`/api/users/${id}`);
  return res.json();
}

// Test without mocking
test('getUser returns user', async () => {
  const mockFetcher = async () => ({
    json: async () => ({ id: '1', name: 'Alice' })
  });
  
  const user = await getUser('1', mockFetcher);
  expect(user.name).toBe('Alice');
});
```

### Separate View from State

```typescript
// Export both connected and pure versions
export function UserListUI({ users, onDelete }) {
  return (
    <ul>
      {users.map(u => (
        <li key={u.id}>
          {u.name}
          <button onClick={() => onDelete(u.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}

// Connected version uses hooks
export function UserList() {
  const users = useSelector(selectUsers);
  const dispatch = useDispatch();
  return (
    <UserListUI 
      users={users} 
      onDelete={(id) => dispatch(deleteUser(id))} 
    />
  );
}

// Test the UI without Redux
test('renders users', () => {
  render(<UserListUI users={[{ id: '1', name: 'Alice' }]} onDelete={() => {}} />);
  expect(screen.getByText('Alice')).toBeInTheDocument();
});
```

### Single Source of Truth for Data

```typescript
// BAD: Transform data in multiple places
// Component A transforms API response one way
// Component B transforms it differently
// Bugs when they get out of sync

// GOOD: Transform once at the boundary
async function fetchUsers(): Promise<User[]> {
  const res = await apiClient.get('/users');
  return normalizeUsers(res.data);  // Single transformation
}

// Every component gets the same shape
```

## Change Management

### Introducing Standards to a Team

1. **Start with yourself** - Follow the standard in your own code
2. **Show the benefit** - "This rule would have caught bug #123"
3. **Add after incidents** - "Let's add a rule to prevent this"
4. **Auto-fix when possible** - Reduce friction
5. **One rule at a time** - Don't overwhelm

### Dealing with Resistance

```
"These rules are too strict"
→ Make them warnings first, errors later

"Pre-commit is too slow"  
→ Use lint-staged to only check changed files

"I need to bypass this"
→ Add eslint-disable with required comment explaining why
```

### Handling Legacy Code

```javascript
// eslint.config.js

export default [
  // Strict rules for new code
  {
    files: ['src/**/*.ts'],
    rules: {
      'no-console': 'error',
    }
  },
  
  // Relaxed for legacy (with TODO to fix)
  {
    files: ['legacy/**/*.js'],
    rules: {
      'no-console': 'warn',  // Warn, don't block
    }
  }
];
```

## Complete Setup Example

### 1. Install Dependencies

```bash
npm install -D husky lint-staged eslint prettier
npx husky init
```

### 2. Configure lint-staged

```json
// package.json
{
  "scripts": {
    "prepare": "husky",
    "lint": "eslint . --fix",
    "format": "prettier --write ."
  },
  "lint-staged": {
    "*.{js,ts,jsx,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,css,yml}": [
      "prettier --write"
    ]
  }
}
```

### 3. Configure Pre-Commit Hook

```bash
# .husky/pre-commit
npx lint-staged
```

### 4. Configure ESLint

```javascript
// eslint.config.js
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    plugins: { '@typescript-eslint': typescript },
    rules: {
      'no-console': 'warn',
      'no-unused-vars': 'error',
    }
  }
];
```

### 5. Configure Prettier

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

## Resources

- **ESLint Rules**: See [references/eslint-rules.md](references/eslint-rules.md) for custom rule patterns
- **Git Hooks**: See [references/git-hooks.md](references/git-hooks.md) for Husky configuration
- **Architecture**: See [references/testable-architecture.md](references/testable-architecture.md) for DI patterns

## Response Guidelines

When advising on code quality:

1. **Check automation first** - Is there a hook/CI for this?
2. **Suggest lint-staged** - Don't lint all files every commit
3. **Recommend gradual adoption** - Don't flip 100 rules at once
4. **Emphasize auto-fix** - Reduce friction
5. **Consider testability** - Would DI help?
