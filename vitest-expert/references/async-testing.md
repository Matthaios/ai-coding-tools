# Async Testing Patterns

Complete guide to testing asynchronous code with Vitest.

## Table of Contents
1. [Async/Await Pattern](#asyncawait-pattern)
2. [Resolves and Rejects](#resolves-and-rejects)
3. [Callbacks](#callbacks)
4. [Timers and Delays](#timers-and-delays)
5. [Polling and Retries](#polling-and-retries)
6. [Common Pitfalls](#common-pitfalls)

---

## Async/Await Pattern

The most common and readable approach for testing async code.

### Basic Usage

```typescript
test('fetches user data', async () => {
  const user = await fetchUser(1);
  
  expect(user).toEqual({
    id: 1,
    name: 'Alice'
  });
});
```

### Multiple Async Operations

```typescript
test('processes data pipeline', async () => {
  const rawData = await fetchRawData();
  const processed = await processData(rawData);
  const saved = await saveToDatabase(processed);
  
  expect(saved.status).toBe('success');
});
```

### Parallel Async Operations

```typescript
test('fetches multiple users', async () => {
  const [user1, user2, user3] = await Promise.all([
    fetchUser(1),
    fetchUser(2),
    fetchUser(3)
  ]);
  
  expect(user1.name).toBe('Alice');
  expect(user2.name).toBe('Bob');
  expect(user3.name).toBe('Charlie');
});
```

---

## Resolves and Rejects

Cleaner syntax for simple promise assertions.

### Testing Successful Resolution

```typescript
// With resolves
test('resolves to user data', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'Alice' });
});

// Equivalent to
test('resolves to user data', async () => {
  const result = await fetchUser(1);
  expect(result).toEqual({ id: 1, name: 'Alice' });
});
```

### Testing Rejection

```typescript
// Testing that a promise rejects
test('rejects with not found error', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('User not found');
});

// Testing specific error type
test('rejects with ValidationError', async () => {
  await expect(validateInput(null)).rejects.toThrow(ValidationError);
});

// Testing error properties
test('rejects with detailed error', async () => {
  await expect(fetchUser(-1)).rejects.toMatchObject({
    message: 'User not found',
    code: 'NOT_FOUND'
  });
});
```

### Why Use Rejects Over Try/Catch

```typescript
// BAD: Easy to forget assertion if promise resolves
test('should reject', async () => {
  try {
    await shouldFail();
    // If we get here, test should fail but doesn't!
  } catch (error) {
    expect(error.message).toBe('expected error');
  }
});

// GOOD: Test fails if promise resolves
test('should reject', async () => {
  await expect(shouldFail()).rejects.toThrow('expected error');
});

// ALSO GOOD: Explicit fail
test('should reject', async () => {
  try {
    await shouldFail();
    expect.fail('Should have thrown');
  } catch (error) {
    expect(error.message).toBe('expected error');
  }
});
```

---

## Callbacks

Testing callback-based async code.

### With Mock Functions

```typescript
test('calls callback with result', async () => {
  const callback = vi.fn();
  
  await processAsync(data, callback);
  
  expect(callback).toHaveBeenCalledTimes(1);
  expect(callback).toHaveBeenCalledWith(null, expect.objectContaining({
    status: 'success'
  }));
});
```

### Converting Callbacks to Promises

```typescript
// Utility to promisify callbacks
function promisify(fn) {
  return (...args) => new Promise((resolve, reject) => {
    fn(...args, (err, result) => {
      if (err) reject(err);
      else resolve(result);
    });
  });
}

test('legacy callback function', async () => {
  const readFileAsync = promisify(legacyReadFile);
  const content = await readFileAsync('file.txt');
  expect(content).toContain('expected content');
});
```

---

## Timers and Delays

Control time in tests for deterministic results.

### Fake Timers

```typescript
import { vi, beforeEach, afterEach } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test('debounces input', async () => {
  const callback = vi.fn();
  const debounced = debounce(callback, 1000);
  
  debounced('a');
  debounced('ab');
  debounced('abc');
  
  // Callback not called yet
  expect(callback).not.toHaveBeenCalled();
  
  // Advance time by 1 second
  vi.advanceTimersByTime(1000);
  
  // Now callback was called once with final value
  expect(callback).toHaveBeenCalledTimes(1);
  expect(callback).toHaveBeenCalledWith('abc');
});
```

### Testing setTimeout

```typescript
test('delays execution', async () => {
  const callback = vi.fn();
  
  delayedCall(callback, 5000);
  
  expect(callback).not.toHaveBeenCalled();
  
  vi.advanceTimersByTime(4999);
  expect(callback).not.toHaveBeenCalled();
  
  vi.advanceTimersByTime(1);
  expect(callback).toHaveBeenCalledTimes(1);
});
```

### Testing setInterval

```typescript
test('polls at regular intervals', () => {
  const callback = vi.fn();
  
  startPolling(callback, 1000);
  
  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledTimes(1);
  
  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledTimes(2);
  
  vi.advanceTimersByTime(3000);
  expect(callback).toHaveBeenCalledTimes(5);
});
```

### Run All Timers

```typescript
test('completes all pending timers', () => {
  const callback = vi.fn();
  
  setTimeout(callback, 1000);
  setTimeout(callback, 2000);
  setTimeout(callback, 3000);
  
  vi.runAllTimers();
  
  expect(callback).toHaveBeenCalledTimes(3);
});
```

### Mocking Date/Time

```typescript
test('formats current date', () => {
  // Set a specific date
  vi.setSystemTime(new Date('2024-01-15T10:00:00'));
  
  const formatted = formatCurrentDate();
  
  expect(formatted).toBe('January 15, 2024');
});

test('calculates age correctly', () => {
  vi.setSystemTime(new Date('2024-06-15'));
  
  const age = calculateAge(new Date('1990-06-15'));
  
  expect(age).toBe(34);
});
```

---

## Polling and Retries

Testing code that waits for conditions.

### waitFor Pattern

```typescript
import { waitFor } from '@testing-library/react';

test('eventually updates state', async () => {
  const { getByText } = render(<AsyncComponent />);
  
  // Will retry until condition passes or timeout
  await waitFor(() => {
    expect(getByText('Loaded')).toBeInTheDocument();
  });
});
```

### Custom Retry Logic

```typescript
async function waitForCondition(
  condition: () => boolean,
  timeout = 5000,
  interval = 100
): Promise<void> {
  const start = Date.now();
  
  while (!condition()) {
    if (Date.now() - start > timeout) {
      throw new Error('Timeout waiting for condition');
    }
    await new Promise(r => setTimeout(r, interval));
  }
}

test('waits for external state', async () => {
  startAsyncProcess();
  
  await waitForCondition(() => getProcessStatus() === 'complete');
  
  expect(getProcessResult()).toBe('success');
});
```

---

## Common Pitfalls

### Forgetting await

```typescript
// BAD: Test passes even if promise rejects!
test('should work', () => {
  expect(asyncFn()).resolves.toBe('value');
  // Missing await - test completes before promise settles
});

// GOOD
test('should work', async () => {
  await expect(asyncFn()).resolves.toBe('value');
});
```

### Not Handling Rejection

```typescript
// BAD: Unhandled promise rejection
test('handles error', async () => {
  const result = await mightFail();  // If this throws, test fails cryptically
  expect(result).toBeDefined();
});

// GOOD: Explicit error handling
test('handles error', async () => {
  await expect(mightFail()).resolves.toBeDefined();
});
```

### Race Conditions with Fake Timers

```typescript
// BAD: Mixing real and fake time
test('async with timers', async () => {
  vi.useFakeTimers();
  
  const promise = fetchWithTimeout();  // Uses real network!
  vi.advanceTimersByTime(5000);
  
  await promise;  // Hangs - network uses real time
});

// GOOD: Mock the network too
test('async with timers', async () => {
  vi.useFakeTimers();
  
  // Mock the async part
  vi.mocked(fetch).mockResolvedValue(mockResponse);
  
  const promise = fetchWithTimeout();
  vi.advanceTimersByTime(5000);
  
  await promise;
});
```

### Timer Leaks Between Tests

```typescript
// BAD: Timer from one test affects another
test('first test', () => {
  vi.useFakeTimers();
  setTimeout(() => { /* side effect */ }, 1000);
  // Forgot to restore real timers
});

test('second test', async () => {
  await delay(100);  // Uses fake timers from previous test!
});

// GOOD: Always restore in afterEach
afterEach(() => {
  vi.useRealTimers();
  vi.clearAllTimers();
});
```

---

## Best Practices

1. **Always await** async assertions with resolves/rejects
2. **Use fake timers** for deterministic time-based tests
3. **Clean up timers** in afterEach to prevent test pollution
4. **Prefer resolves/rejects** over try/catch for cleaner code
5. **Set specific dates** with vi.setSystemTime for date-dependent logic
6. **Mock network calls** when using fake timers
7. **Use waitFor** for UI that updates asynchronously
