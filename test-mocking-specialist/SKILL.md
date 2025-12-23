---
name: test-mocking-specialist
description: Expert advisor for test doubles, mocks, and spies with Vitest/Jest. Use when (1) deciding WHETHER to mock something (with appropriate suspicion), (2) mocking time with useFakeTimers, (3) spying on methods like console.log, (4) mocking third-party libraries, (5) faking API responses with Mock Service Worker, (6) testing code with external dependencies, (7) reviewing tests that use excessive mocking, or (8) refactoring tightly-coupled code to be more testable.
---

# Test Mocking Specialist

Expert guidance on when and how to use mocks, spies, and test doubles. The core philosophy: **treat mocking with suspicion**.

## Core Principle: Treat Mocking with Suspicion

Every mock divorces your test from reality. The more you mock, the less your test proves about real behavior.

```typescript
// The suspicious question to ask:
// "Am I testing MY code, or am I testing my mocks?"
```

### When Mocking is Acceptable

Only mock things **you don't control**:

| Acceptable to Mock | Why |
|-------------------|-----|
| Time (Date, setTimeout) | Non-deterministic, makes tests flaky |
| Random values (UUIDs, Math.random) | Non-deterministic |
| External APIs (Twilio, Stripe) | Cost money, send real messages |
| Network requests | Slow, unreliable, external dependency |
| Browser APIs in Node | Don't exist in test environment |

### When to Prefer Alternatives

| Instead of Mocking | Do This |
|-------------------|---------|
| Mocking internal functions | Extract logic, use dependency injection |
| Mocking everything | Write integration tests |
| Mocking to hide complexity | Refactor the complex code |
| Mocking database | Use in-memory database or test fixtures |

### The Dependency Injection Alternative

If you need to mock something, consider if dependency injection would be cleaner:

```typescript
// BAD: Tightly coupled, requires mocking
async function sendNotification(userId: string, message: string) {
  const user = await fetch(`/api/users/${userId}`);  // Hard to test
  await twilioClient.send(user.phone, message);      // Hard to test
}

// GOOD: Dependencies injected, no mocking needed
async function sendNotification(
  userId: string,
  message: string,
  fetchUser = defaultFetchUser,    // Can pass test version
  sendSms = defaultSendSms         // Can pass test version
) {
  const user = await fetchUser(userId);
  await sendSms(user.phone, message);
}

// Test without mocks
test('sends notification', async () => {
  const mockFetch = async () => ({ phone: '555-1234' });
  const mockSend = vi.fn();
  
  await sendNotification('user-1', 'Hello', mockFetch, mockSend);
  
  expect(mockSend).toHaveBeenCalledWith('555-1234', 'Hello');
});
```

## Mock Functions (vi.fn)

Create standalone mock functions for callbacks and injected dependencies.

### Basic Mock Function

```typescript
const mock = vi.fn();

// Call it
mock('arg1', 'arg2');
mock('another call');

// Assert calls
expect(mock).toHaveBeenCalled();
expect(mock).toHaveBeenCalledTimes(2);
expect(mock).toHaveBeenCalledWith('arg1', 'arg2');
expect(mock).toHaveBeenLastCalledWith('another call');
```

### Mock with Implementation

```typescript
// Simple return value
const getId = vi.fn(() => 'mock-id');

// Different returns per call
const fetchItem = vi.fn()
  .mockReturnValueOnce({ id: 1 })
  .mockReturnValueOnce({ id: 2 })
  .mockReturnValue({ id: 'default' });

// Async mock
const fetchUser = vi.fn().mockResolvedValue({ name: 'Alice' });
const failingFetch = vi.fn().mockRejectedValue(new Error('Not found'));
```

### Inspecting Mock Calls

```typescript
const mock = vi.fn();
mock('first', 1);
mock('second', 2);

// All calls
console.log(mock.mock.calls);
// [['first', 1], ['second', 2]]

// All return values
console.log(mock.mock.results);
// [{ type: 'return', value: undefined }, ...]

// Clear history (keeps implementation)
mock.mockClear();

// Reset everything (implementation too)
mock.mockReset();
```

## Spying (vi.spyOn)

Watch existing methods while keeping original behavior.

### Basic Spy

```typescript
// Spy on console.log
const logSpy = vi.spyOn(console, 'log');

// Function still works normally
console.log('Hello');  // Actually logs

// But we can assert on it
expect(logSpy).toHaveBeenCalledWith('Hello');

// Restore original (important!)
logSpy.mockRestore();
```

### Spy with Mock Implementation

```typescript
// Spy AND replace behavior
const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

console.log('Hello');  // Silent - no output

expect(logSpy).toHaveBeenCalledWith('Hello');

logSpy.mockRestore();
```

### Spy on Object Methods

```typescript
const user = {
  getName: () => 'Alice',
  getAge: () => 30
};

const spy = vi.spyOn(user, 'getName');

user.getName();

expect(spy).toHaveBeenCalled();
expect(spy).toHaveReturnedWith('Alice');
```

## Module Mocking (vi.mock)

Replace entire modules - use sparingly!

### Basic Module Mock

```typescript
// Mock entire module
vi.mock('axios');

import axios from 'axios';

// All exports are now mocks
axios.get.mockResolvedValue({ data: { id: 1 } });

test('fetches data', async () => {
  const result = await myFunction();
  expect(axios.get).toHaveBeenCalledWith('/api/data');
});
```

### Partial Module Mock

```typescript
// Keep some real implementations
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    // Only mock this one function
    generateId: () => 'mock-id'
  };
});
```

### Manual Mock Files

Create `__mocks__/moduleName.ts` for reusable mocks:

```typescript
// __mocks__/axios.ts
export default {
  get: vi.fn().mockResolvedValue({ data: {} }),
  post: vi.fn().mockResolvedValue({ data: {} })
};
```

## Mocking Time

Time is a perfect use case for mocking - non-deterministic and your tests shouldn't wait.

### Fake Timers

```typescript
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test('debounces calls', () => {
  const callback = vi.fn();
  const debounced = debounce(callback, 500);
  
  debounced();
  debounced();
  debounced();
  
  expect(callback).not.toHaveBeenCalled();
  
  vi.advanceTimersByTime(500);
  
  expect(callback).toHaveBeenCalledTimes(1);
});
```

### Mocking Date

```typescript
test('formats relative time', () => {
  vi.setSystemTime(new Date('2024-03-15T10:00:00'));
  
  const result = formatRelativeTime(new Date('2024-03-15T09:00:00'));
  
  expect(result).toBe('1 hour ago');
});
```

### Time-Based Queries

```typescript
// Real-world example: date range queries
test('builds last 24 hours query', () => {
  vi.setSystemTime(new Date('2024-03-15T12:00:00Z'));
  
  const query = buildQuery('last-24-hours');
  
  expect(query).toEqual({
    startTime: '2024-03-14T12:00:00Z',
    endTime: '2024-03-15T12:00:00Z'
  });
});
```

## Mock Service Worker (MSW)

**The preferred way to mock API requests.** Intercepts at the network level, so your actual fetch/axios code runs.

### Why MSW Over Mocking Fetch

```typescript
// BAD: Mocking fetch - your real fetch code never runs
vi.mock('node-fetch');
fetch.mockResolvedValue({ json: () => ({ data: 'test' }) });

// GOOD: MSW - your real fetch code runs, only network is mocked
// The actual parsing, error handling, etc. is tested
```

### Basic Setup

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Mock User'
    });
  }),
  
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '123', ...body }, { status: 201 });
  })
];
```

```typescript
// mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```typescript
// test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Override Handlers Per Test

```typescript
import { server } from './mocks/server';
import { http, HttpResponse } from 'msw';

test('handles server error', async () => {
  // Override for this test only
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json(
        { error: 'Server error' },
        { status: 500 }
      );
    })
  );
  
  await expect(fetchUser('123')).rejects.toThrow('Server error');
});
```

## Review Checklist

When reviewing tests with mocks, ask:

1. **Is this mock necessary?** Could dependency injection work instead?
2. **What code is being skipped?** Mocked code isn't tested
3. **Is this mocking external or internal?** External = OK, Internal = suspicious
4. **Are mocks cleaned up?** Look for afterEach with mockRestore
5. **Is MSW used for APIs?** Preferred over mocking fetch directly
6. **Are fake timers restored?** useRealTimers in afterEach

## Resources

- **Mocking Patterns**: See [references/mocking-patterns.md](references/mocking-patterns.md) for detailed vi.fn, vi.spyOn, vi.mock patterns
- **MSW Setup**: See [references/msw-setup.md](references/msw-setup.md) for Mock Service Worker configuration

## Response Guidelines

When answering questions about mocking:

1. **Challenge the need** - Ask if mocking is truly necessary
2. **Suggest alternatives** - Dependency injection, refactoring, MSW
3. **If mocking is needed** - Show the correct pattern
4. **Emphasize cleanup** - Always restore mocks
5. **Prefer MSW for APIs** - It tests more of your real code
