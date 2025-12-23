---
name: vitest-expert
description: Expert advisor for unit testing with Vitest. Use when (1) setting up Vitest configuration and environments, (2) writing unit tests for functions, reducers, or utilities, (3) handling async testing with promises, (4) using asymmetric matchers for flexible assertions, (5) testing code with random values like UUIDs or timestamps, (6) choosing between toBe, toEqual, and toBeCloseTo, (7) debugging flaky or failing tests, or (8) optimizing the testing feedback loop.
---

# Vitest Expert

Expert guidance for writing effective, maintainable unit tests with Vitest. Focus on fast feedback loops, proper assertions, and testing pure logic extracted from components.

## Core Principles

### 1. Fast Feedback Loop
Tests should tell you quickly when something breaks. Use Vitest's watch mode and UI for immediate visual feedback as you develop.

```bash
# Watch mode (default)
npx vitest

# Visual UI for better feedback
npx vitest --ui

# Single run (CI/CD)
npx vitest run
```

### 2. Test Pure Functions
Extract logic from your view layer into pure functions. A reducer is just a function that takes state and action, returns new state - trivially testable without mounting components.

```typescript
// BAD: Logic buried in component
function Counter() {
  const [count, setCount] = useState(0);
  const increment = () => setCount(c => c + 1);
  // ...
}

// GOOD: Logic extracted, easily testable
function counterReducer(state, action) {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + 1 };
    default: return state;
  }
}

// Test is trivial
test('increment increases count', () => {
  const state = { count: 0 };
  const result = counterReducer(state, { type: 'increment' });
  expect(result.count).toBe(1);
});
```

### 3. Meaningful Error Messages
Structure tests so failures are obvious. Use descriptive test names and appropriate matchers.

```typescript
// BAD: Cryptic failure
expect(result).toBe(true);

// GOOD: Clear failure message
expect(user.isActive).toBe(true);
// Or even better with custom message context
expect(result).toEqual(expect.objectContaining({
  status: 'active',
  permissions: expect.arrayContaining(['read'])
}));
```

## Assertion Patterns

### Equality Types

Choose the right equality check:

| Matcher | Use For | Example |
|---------|---------|---------|
| `toBe` | Primitives, same reference | `expect(1 + 1).toBe(2)` |
| `toEqual` | Object/array value equality | `expect([1, 2]).toEqual([1, 2])` |
| `toBeCloseTo` | Floating point numbers | `expect(0.1 + 0.2).toBeCloseTo(0.3)` |

```typescript
// Primitives: use toBe
expect(2 + 2).toBe(4);
expect(status).toBe('active');

// Objects/Arrays: use toEqual (value comparison)
expect({ a: 1 }).toEqual({ a: 1 }); // PASS
expect({ a: 1 }).toBe({ a: 1 });    // FAIL - different references

// Floating point: use toBeCloseTo
expect(0.1 + 0.2).toBe(0.3);        // FAIL - JavaScript floats
expect(0.1 + 0.2).toBeCloseTo(0.3); // PASS
```

### Asymmetric Matchers

Use when you don't care about exact values - essential for testing code with generated IDs, timestamps, or partial objects:

```typescript
// Testing objects with generated UUIDs
const item = createItem({ name: 'Test' });

// BAD: Brittle - fails on any ID
expect(item).toEqual({ id: 'abc-123', name: 'Test' });

// GOOD: Flexible - ID just needs to be a string
expect(item).toEqual({
  id: expect.any(String),
  name: 'Test'
});

// Partial object matching
expect(response).toEqual(expect.objectContaining({
  status: 'success',
  // Don't care about other fields
}));

// Array containing specific items
expect(permissions).toEqual(expect.arrayContaining(['read', 'write']));

// String patterns
expect(error.message).toEqual(expect.stringContaining('not found'));
expect(id).toEqual(expect.stringMatching(/^user-\d+$/));
```

### Common Matchers Quick Reference

```typescript
// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThanOrEqual(10);

// Strings
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');

// Arrays
expect(arr).toContain(item);
expect(arr).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('nested.key', 'value');

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('specific message');
expect(() => fn()).toThrow(CustomError);
```

## Async Testing

### Awaiting Promises

```typescript
// Direct await (most common)
test('fetches user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});

// Using resolves/rejects (cleaner for simple cases)
test('resolves to user', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ name: 'Alice' });
});

test('rejects with error', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('User not found');
});
```

### Testing Callbacks

```typescript
test('calls callback with result', () => {
  const callback = vi.fn();
  processData(data, callback);
  
  expect(callback).toHaveBeenCalledWith(expect.objectContaining({
    status: 'complete'
  }));
});
```

## Testing Reducers

Redux reducers (or useReducer logic) are ideal for unit testing - pure functions with clear inputs and outputs:

```typescript
import { itemsReducer, addItem, removeItem } from './itemsSlice';

describe('itemsReducer', () => {
  const initialState = { items: [], filter: 'all' };

  test('adds item with generated ID', () => {
    const action = addItem({ name: 'New Item' });
    const result = itemsReducer(initialState, action);
    
    expect(result.items).toHaveLength(1);
    expect(result.items[0]).toEqual({
      id: expect.any(String),  // UUID generated internally
      name: 'New Item',
      completed: false
    });
  });

  test('removes item by ID', () => {
    const stateWithItem = {
      items: [{ id: '123', name: 'Test', completed: false }],
      filter: 'all'
    };
    
    const result = itemsReducer(stateWithItem, removeItem('123'));
    expect(result.items).toHaveLength(0);
  });
});
```

## Configuration

### Basic vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Global test settings
    globals: true,  // Use describe, test, expect without imports
    
    // Environment for component tests
    environment: 'jsdom',  // or 'happy-dom'
    
    // Setup files run before each test file
    setupFiles: ['./test/setup.ts'],
    
    // Include patterns
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    
    // Coverage configuration
    coverage: {
      provider: 'v8',  // or 'istanbul'
      reporter: ['text', 'html'],
      exclude: ['node_modules', 'test/**']
    }
  }
});
```

### Per-File Environment Override

```typescript
// @vitest-environment jsdom
// This comment at top of file overrides config

import { render } from '@testing-library/react';
// Now document and window are available
```

## Resources

- **Assertion Patterns**: See [references/assertion-patterns.md](references/assertion-patterns.md) for complete matcher reference
- **Async Testing**: See [references/async-testing.md](references/async-testing.md) for promises, timers, and callbacks

## Response Guidelines

When answering questions or reviewing tests:

1. **Check equality types** - Is toBe vs toEqual appropriate?
2. **Look for brittleness** - Are tests failing on generated IDs or timestamps?
3. **Suggest asymmetric matchers** - When exact values don't matter
4. **Extract pure logic** - Move testable logic out of components
5. **Recommend the UI** - `vitest --ui` for better feedback loop
