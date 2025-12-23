# Mocking Patterns Reference

Detailed reference for vi.fn, vi.spyOn, and vi.mock patterns in Vitest.

## Table of Contents
1. [Mock Functions (vi.fn)](#mock-functions-vifn)
2. [Spying (vi.spyOn)](#spying-vispyon)
3. [Module Mocking (vi.mock)](#module-mocking-vimock)
4. [Timer Mocking](#timer-mocking)
5. [Cleanup Patterns](#cleanup-patterns)
6. [Common Scenarios](#common-scenarios)

---

## Mock Functions (vi.fn)

### Creating Mock Functions

```typescript
// Empty mock (no-op)
const mock = vi.fn();

// Mock with return value
const getId = vi.fn(() => 'mock-id-123');

// Mock with implementation
const calculate = vi.fn((a, b) => a + b);
```

### Configuring Return Values

```typescript
const mock = vi.fn();

// Always return same value
mock.mockReturnValue('always');

// Return different values on successive calls
mock.mockReturnValueOnce('first')
    .mockReturnValueOnce('second')
    .mockReturnValue('rest');

mock(); // 'first'
mock(); // 'second'
mock(); // 'rest'
mock(); // 'rest'
```

### Async Mock Functions

```typescript
// Resolve with value
const fetchUser = vi.fn().mockResolvedValue({ id: 1, name: 'Alice' });

// Resolve differently per call
const fetchData = vi.fn()
  .mockResolvedValueOnce({ page: 1 })
  .mockResolvedValueOnce({ page: 2 });

// Reject with error
const failingFetch = vi.fn().mockRejectedValue(new Error('Network error'));

// Reject once, then succeed
const retryableFetch = vi.fn()
  .mockRejectedValueOnce(new Error('Retry'))
  .mockResolvedValue({ success: true });
```

### Mock Implementation

```typescript
// Full implementation
const complexMock = vi.fn().mockImplementation((input) => {
  if (input > 10) return 'large';
  if (input > 0) return 'small';
  return 'zero';
});

// One-time implementation
const mock = vi.fn()
  .mockImplementationOnce(() => 'first behavior')
  .mockImplementation(() => 'default behavior');
```

### Asserting Mock Calls

```typescript
const mock = vi.fn();
mock('arg1', 'arg2');
mock('second call');

// Was called
expect(mock).toHaveBeenCalled();
expect(mock).toHaveBeenCalledTimes(2);

// Called with specific arguments
expect(mock).toHaveBeenCalledWith('arg1', 'arg2');
expect(mock).toHaveBeenLastCalledWith('second call');
expect(mock).toHaveBeenNthCalledWith(1, 'arg1', 'arg2');

// Not called with
expect(mock).not.toHaveBeenCalledWith('never called');
```

### Inspecting Mock State

```typescript
const mock = vi.fn((x) => x * 2);
mock(5);
mock(10);

// All calls with arguments
mock.mock.calls;        // [[5], [10]]

// All results
mock.mock.results;      // [{ type: 'return', value: 10 }, { type: 'return', value: 20 }]

// Last call
mock.mock.lastCall;     // [10]

// Invocation order (for multiple mocks)
mock.mock.invocationCallOrder;  // [1, 2]
```

---

## Spying (vi.spyOn)

### Basic Spying

```typescript
const obj = {
  method: (x: number) => x * 2
};

const spy = vi.spyOn(obj, 'method');

// Original still works
expect(obj.method(5)).toBe(10);

// But we can assert
expect(spy).toHaveBeenCalledWith(5);
expect(spy).toHaveReturnedWith(10);
```

### Spying on Console

```typescript
// Spy and silence
const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

// Run code that logs
myFunction();

// Assert
expect(logSpy).toHaveBeenCalledWith('Expected message');
expect(errorSpy).not.toHaveBeenCalled();

// Restore
logSpy.mockRestore();
errorSpy.mockRestore();
```

### Spying on Getters/Setters

```typescript
const obj = {
  _value: 0,
  get value() { return this._value; },
  set value(v) { this._value = v; }
};

// Spy on getter
const getSpy = vi.spyOn(obj, 'value', 'get').mockReturnValue(42);
expect(obj.value).toBe(42);

// Spy on setter
const setSpy = vi.spyOn(obj, 'value', 'set');
obj.value = 100;
expect(setSpy).toHaveBeenCalledWith(100);
```

### Spying on Prototypes

```typescript
class User {
  save() { /* ... */ }
}

const saveSpy = vi.spyOn(User.prototype, 'save').mockImplementation(() => {});

const user = new User();
user.save();

expect(saveSpy).toHaveBeenCalled();
saveSpy.mockRestore();
```

---

## Module Mocking (vi.mock)

### Auto-Mocking Entire Module

```typescript
// All exports become mocks
vi.mock('axios');

import axios from 'axios';

// Configure the mocks
axios.get.mockResolvedValue({ data: { id: 1 } });
axios.post.mockResolvedValue({ data: { success: true } });
```

### Factory Function

```typescript
vi.mock('./database', () => ({
  connect: vi.fn().mockResolvedValue(true),
  query: vi.fn().mockResolvedValue([]),
  disconnect: vi.fn()
}));
```

### Partial Mocking

```typescript
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    // Only mock specific exports
    generateId: vi.fn(() => 'mock-id'),
    // Keep real implementations for the rest
  };
});
```

### Mocking Default Exports

```typescript
// Named export
vi.mock('./config', () => ({
  getConfig: vi.fn(() => ({ apiUrl: 'http://mock' }))
}));

// Default export
vi.mock('./logger', () => ({
  default: vi.fn()
}));

// ES module default
vi.mock('./service', () => {
  return {
    default: {
      fetch: vi.fn()
    }
  };
});
```

### Hoisting Behavior

```typescript
// vi.mock is hoisted to top of file automatically
// This works even though import comes first

import { myFunction } from './module';

vi.mock('./module', () => ({
  myFunction: vi.fn()
}));

// But you can't use variables from above
const mockValue = 'test';
vi.mock('./module', () => ({
  getValue: vi.fn(() => mockValue)  // ERROR: mockValue not defined
}));

// Use vi.hoisted for that
const { mockValue } = vi.hoisted(() => ({
  mockValue: 'test'
}));

vi.mock('./module', () => ({
  getValue: vi.fn(() => mockValue)  // Works!
}));
```

---

## Timer Mocking

### Setup and Teardown

```typescript
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});
```

### Controlling Time

```typescript
// Advance by milliseconds
vi.advanceTimersByTime(1000);

// Run next timer only
vi.runOnlyPendingTimers();

// Run all timers
vi.runAllTimers();

// Advance to next timer
vi.advanceTimersToNextTimer();

// Get pending timer count
vi.getTimerCount();
```

### Mocking Date

```typescript
// Set specific date
vi.setSystemTime(new Date('2024-01-15T10:30:00'));

// Now Date returns mocked time
new Date();  // 2024-01-15T10:30:00
Date.now();  // 1705314600000

// Advance real time too
vi.advanceTimersByTime(60000);
new Date();  // 2024-01-15T10:31:00
```

### Timer Options

```typescript
vi.useFakeTimers({
  // Only fake these
  toFake: ['setTimeout', 'setInterval'],
  
  // Start at specific time
  now: new Date('2024-01-01'),
  
  // Don't advance automatically
  shouldAdvanceTime: false
});
```

---

## Cleanup Patterns

### Per-Test Cleanup

```typescript
afterEach(() => {
  // Clear mock call history
  vi.clearAllMocks();
  
  // Reset mocks to initial state (removes implementations)
  vi.resetAllMocks();
  
  // Restore original implementations
  vi.restoreAllMocks();
  
  // Reset timers
  vi.useRealTimers();
});
```

### Individual Mock Cleanup

```typescript
const mock = vi.fn().mockReturnValue('test');

// Clear call history only
mock.mockClear();

// Reset to empty mock
mock.mockReset();

// Restore original (for spies)
const spy = vi.spyOn(obj, 'method');
spy.mockRestore();
```

### Cleanup Hierarchy

```
mockClear()   - Clears calls and results
    ↓
mockReset()   - mockClear() + removes implementation
    ↓
mockRestore() - mockReset() + restores original (spies only)
```

---

## Common Scenarios

### Testing Error Handling

```typescript
vi.mock('./api');

import { fetchUser } from './api';
import { loadUser } from './userService';

test('handles API error gracefully', async () => {
  fetchUser.mockRejectedValue(new Error('Network error'));
  
  const result = await loadUser('123');
  
  expect(result).toEqual({
    error: 'Failed to load user',
    user: null
  });
});
```

### Testing Retry Logic

```typescript
const fetchData = vi.fn()
  .mockRejectedValueOnce(new Error('Fail 1'))
  .mockRejectedValueOnce(new Error('Fail 2'))
  .mockResolvedValue({ success: true });

const result = await fetchWithRetry(fetchData, 3);

expect(fetchData).toHaveBeenCalledTimes(3);
expect(result).toEqual({ success: true });
```

### Testing Event Handlers

```typescript
test('calls handler on event', () => {
  const handler = vi.fn();
  const emitter = new EventEmitter();
  
  emitter.on('data', handler);
  emitter.emit('data', { value: 42 });
  
  expect(handler).toHaveBeenCalledWith({ value: 42 });
});
```

### Testing Callbacks

```typescript
test('processes items with callback', async () => {
  const onProgress = vi.fn();
  
  await processItems(['a', 'b', 'c'], onProgress);
  
  expect(onProgress).toHaveBeenCalledTimes(3);
  expect(onProgress.mock.calls).toEqual([
    [{ item: 'a', index: 0 }],
    [{ item: 'b', index: 1 }],
    [{ item: 'c', index: 2 }]
  ]);
});
```

### Mocking Environment Variables

```typescript
const originalEnv = process.env;

beforeEach(() => {
  vi.resetModules();
  process.env = { ...originalEnv };
});

afterEach(() => {
  process.env = originalEnv;
});

test('uses API key from env', async () => {
  process.env.API_KEY = 'test-key';
  
  // Re-import module to pick up new env
  const { createClient } = await import('./client');
  const client = createClient();
  
  expect(client.apiKey).toBe('test-key');
});
```

---

## Best Practices Summary

1. **Prefer vi.fn() for callbacks** - Clean, explicit
2. **Use vi.spyOn for existing methods** - Preserves original by default
3. **Use vi.mock sparingly** - It mocks everything, easy to over-mock
4. **Always clean up** - Use afterEach with restore/reset
5. **Partial mock when possible** - Keep real implementations where safe
6. **Use async matchers** - mockResolvedValue over mockImplementation
7. **Check call order** - Use toHaveBeenNthCalledWith for sequences
