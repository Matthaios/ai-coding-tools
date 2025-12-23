# Vitest Assertion Patterns

Complete reference for Vitest/Jest assertion matchers and patterns.

## Table of Contents
1. [Equality Matchers](#equality-matchers)
2. [Truthiness Matchers](#truthiness-matchers)
3. [Number Matchers](#number-matchers)
4. [String Matchers](#string-matchers)
5. [Array & Iterable Matchers](#array--iterable-matchers)
6. [Object Matchers](#object-matchers)
7. [Exception Matchers](#exception-matchers)
8. [Asymmetric Matchers](#asymmetric-matchers)
9. [Snapshot Testing](#snapshot-testing)
10. [Custom Matchers](#custom-matchers)

---

## Equality Matchers

### toBe - Reference Equality
Use for primitives and when checking same object reference.

```typescript
// Primitives - works as expected
expect(2 + 2).toBe(4);
expect('hello').toBe('hello');
expect(true).toBe(true);
expect(null).toBe(null);

// Objects - checks reference, not value
const obj = { a: 1 };
const sameRef = obj;
const diffRef = { a: 1 };

expect(obj).toBe(sameRef);      // PASS - same reference
expect(obj).toBe(diffRef);      // FAIL - different reference
```

### toEqual - Deep Value Equality
Use for objects and arrays to compare values.

```typescript
// Objects
expect({ a: 1, b: 2 }).toEqual({ a: 1, b: 2 });  // PASS

// Nested objects
expect({ 
  user: { name: 'Alice', age: 30 } 
}).toEqual({ 
  user: { name: 'Alice', age: 30 } 
});  // PASS

// Arrays
expect([1, 2, 3]).toEqual([1, 2, 3]);  // PASS

// Order matters for arrays
expect([1, 2, 3]).toEqual([3, 2, 1]);  // FAIL
```

### toStrictEqual - Strict Deep Equality
Like toEqual but also checks:
- undefined properties
- array sparseness
- object types (class instances)

```typescript
// undefined properties matter
expect({ a: 1 }).toEqual({ a: 1, b: undefined });       // PASS
expect({ a: 1 }).toStrictEqual({ a: 1, b: undefined }); // FAIL

// Class instances must match
class User { constructor(public name: string) {} }
expect(new User('Alice')).toEqual({ name: 'Alice' });       // PASS
expect(new User('Alice')).toStrictEqual({ name: 'Alice' }); // FAIL
```

### toBeCloseTo - Floating Point
Essential for floating point comparisons due to IEEE 754 precision issues.

```typescript
// JavaScript floating point problem
expect(0.1 + 0.2).toBe(0.3);        // FAIL! (0.30000000000000004)
expect(0.1 + 0.2).toBeCloseTo(0.3); // PASS

// Specify precision (number of decimal digits)
expect(0.1 + 0.2).toBeCloseTo(0.3, 5);  // 5 decimal places
expect(10.005).toBeCloseTo(10, 2);       // Within 0.01
```

---

## Truthiness Matchers

```typescript
// Null and Undefined
expect(null).toBeNull();
expect(undefined).toBeUndefined();
expect(value).toBeDefined();        // Not undefined

// Truthy/Falsy
expect('hello').toBeTruthy();       // truthy values
expect(0).toBeFalsy();              // falsy values

// Falsy values in JavaScript:
// false, 0, '', null, undefined, NaN

// Prefer specific matchers for clarity
expect(result).toBe(true);          // Better than toBeTruthy() for booleans
expect(list.length).toBe(0);        // Better than toBeFalsy() for empty
```

---

## Number Matchers

```typescript
// Comparisons
expect(10).toBeGreaterThan(5);
expect(10).toBeGreaterThanOrEqual(10);
expect(5).toBeLessThan(10);
expect(5).toBeLessThanOrEqual(5);

// NaN
expect(NaN).toBeNaN();

// Infinity
expect(Infinity).toBe(Infinity);
expect(-Infinity).toBe(-Infinity);
```

---

## String Matchers

```typescript
// Substring
expect('hello world').toContain('world');

// Regex
expect('hello world').toMatch(/world/);
expect('user-123').toMatch(/^user-\d+$/);

// Length
expect('hello').toHaveLength(5);
```

---

## Array & Iterable Matchers

```typescript
const arr = [1, 2, 3, 4, 5];

// Contains element
expect(arr).toContain(3);

// Length
expect(arr).toHaveLength(5);

// Contains subset (order doesn't matter)
expect(arr).toEqual(expect.arrayContaining([3, 1]));  // PASS
expect(arr).toEqual(expect.arrayContaining([6]));     // FAIL

// Exact match with specific order
expect(arr).toEqual([1, 2, 3, 4, 5]);
```

---

## Object Matchers

```typescript
const user = { 
  id: 123, 
  name: 'Alice', 
  email: 'alice@example.com',
  settings: { theme: 'dark' }
};

// Has property
expect(user).toHaveProperty('name');
expect(user).toHaveProperty('name', 'Alice');

// Nested property
expect(user).toHaveProperty('settings.theme');
expect(user).toHaveProperty('settings.theme', 'dark');
expect(user).toHaveProperty(['settings', 'theme'], 'dark');

// Contains subset of properties
expect(user).toMatchObject({ name: 'Alice' });
expect(user).toMatchObject({ 
  name: 'Alice',
  settings: { theme: 'dark' }
});
```

---

## Exception Matchers

```typescript
// Function throws any error
expect(() => throwingFn()).toThrow();

// Throws with specific message
expect(() => throwingFn()).toThrow('specific message');
expect(() => throwingFn()).toThrow(/pattern/);

// Throws specific error type
expect(() => throwingFn()).toThrow(ValidationError);

// Async functions
await expect(asyncThrowingFn()).rejects.toThrow();
await expect(asyncThrowingFn()).rejects.toThrow('message');
```

---

## Asymmetric Matchers

Use when you don't need exact matches - essential for generated values.

### expect.any(Constructor)
Matches any value of the given type.

```typescript
expect({ id: 'abc-123', count: 5 }).toEqual({
  id: expect.any(String),
  count: expect.any(Number)
});

// Works with constructors
expect(new Date()).toEqual(expect.any(Date));
expect(() => {}).toEqual(expect.any(Function));
```

### expect.anything()
Matches anything except null and undefined.

```typescript
expect({ value: 'something' }).toEqual({
  value: expect.anything()
});
```

### expect.stringContaining(string)

```typescript
expect({ message: 'Error: file not found' }).toEqual({
  message: expect.stringContaining('not found')
});
```

### expect.stringMatching(regexp)

```typescript
expect({ id: 'user-12345' }).toEqual({
  id: expect.stringMatching(/^user-\d+$/)
});
```

### expect.arrayContaining(array)
Array contains all elements (order independent, can have extras).

```typescript
expect(['a', 'b', 'c', 'd']).toEqual(
  expect.arrayContaining(['b', 'd'])  // PASS
);

expect(['a', 'b']).toEqual(
  expect.arrayContaining(['a', 'b', 'c'])  // FAIL - missing 'c'
);
```

### expect.objectContaining(object)
Object has at least these properties.

```typescript
const user = { id: 1, name: 'Alice', email: 'a@b.com', age: 30 };

expect(user).toEqual(expect.objectContaining({
  name: 'Alice',
  email: expect.stringContaining('@')
}));
// PASS - doesn't care about id and age
```

### Combining Asymmetric Matchers

```typescript
// Complex nested structure
expect(response).toEqual({
  status: 'success',
  data: expect.objectContaining({
    users: expect.arrayContaining([
      expect.objectContaining({
        id: expect.any(String),
        email: expect.stringMatching(/@/)
      })
    ])
  }),
  meta: {
    timestamp: expect.any(Number),
    requestId: expect.stringMatching(/^req-/)
  }
});
```

### expect.not Variants

```typescript
expect(['a', 'b']).toEqual(
  expect.not.arrayContaining(['c'])  // PASS - doesn't contain 'c'
);

expect('hello').toEqual(
  expect.not.stringContaining('goodbye')  // PASS
);
```

---

## Snapshot Testing

Useful for development but treat with caution - easy to blindly update.

### Inline Snapshots
Stores snapshot in the test file itself.

```typescript
test('user object shape', () => {
  const user = createUser('Alice');
  
  expect(user).toMatchInlineSnapshot(`
    {
      "id": Any<String>,
      "name": "Alice",
      "createdAt": Any<Date>,
    }
  `);
});
```

### File Snapshots
Stores in `__snapshots__` directory.

```typescript
test('component renders correctly', () => {
  const result = renderToString(<Button>Click</Button>);
  expect(result).toMatchSnapshot();
});
```

### Updating Snapshots

```bash
# Update all snapshots
npx vitest -u

# Update snapshots for specific test file
npx vitest path/to/test.ts -u
```

**Warning:** Don't blindly update snapshots. Review changes carefully.

---

## Custom Matchers

### Extending expect

```typescript
// test/setup.ts
import { expect } from 'vitest';

expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be within range ${floor} - ${ceiling}`
          : `expected ${received} to be within range ${floor} - ${ceiling}`,
    };
  },
});

// Usage
test('value is in range', () => {
  expect(50).toBeWithinRange(1, 100);
});
```

### TypeScript Declaration

```typescript
// types/vitest.d.ts
import 'vitest';

interface CustomMatchers<R = unknown> {
  toBeWithinRange(floor: number, ceiling: number): R;
}

declare module 'vitest' {
  interface Assertion<T = any> extends CustomMatchers<T> {}
  interface AsymmetricMatchersContaining extends CustomMatchers {}
}
```

---

## Best Practices

1. **Choose specific matchers** - `toBe(true)` over `toBeTruthy()` for booleans
2. **Use asymmetric matchers** for generated values (IDs, timestamps)
3. **Prefer toEqual for objects** - toBe only checks reference
4. **Use toBeCloseTo for floats** - Never toBe with decimals
5. **Avoid snapshot overuse** - Too easy to update blindly
6. **Match the error type** when testing exceptions
