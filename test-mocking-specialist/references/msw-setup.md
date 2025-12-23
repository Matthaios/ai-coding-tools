# Mock Service Worker (MSW) Setup Guide

Complete guide to setting up MSW for API mocking in tests.

## Table of Contents
1. [Why MSW](#why-msw)
2. [Installation](#installation)
3. [Basic Setup](#basic-setup)
4. [Writing Handlers](#writing-handlers)
5. [Test Integration](#test-integration)
6. [Advanced Patterns](#advanced-patterns)
7. [Debugging](#debugging)

---

## Why MSW

MSW intercepts requests at the **network level**, not at the fetch/axios level:

```
Your Code → fetch() → MSW Intercepts → Mock Response
                ↓
         (fetch still runs)
```

### Benefits Over Mocking Fetch

| MSW | Mocking Fetch |
|-----|---------------|
| Real fetch/axios code runs | Fetch code is replaced |
| Headers, parsing tested | Headers, parsing skipped |
| Same mocks work everywhere | Different mocks per HTTP lib |
| Error handling tested | Error handling may be skipped |
| Realistic network behavior | Simplified behavior |

---

## Installation

```bash
npm install msw --save-dev
```

---

## Basic Setup

### 1. Create Handlers

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  // GET request
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' }
    ]);
  }),

  // GET with params
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'User ' + params.id
    });
  }),

  // POST request
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: 'new-id', ...body },
      { status: 201 }
    );
  }),

  // DELETE request
  http.delete('/api/users/:id', () => {
    return new HttpResponse(null, { status: 204 });
  })
];
```

### 2. Create Server (Node/Tests)

```typescript
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### 3. Setup File for Vitest

```typescript
// test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from '../src/mocks/server';

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));

// Reset handlers after each test
afterEach(() => server.resetHandlers());

// Clean up after all tests
afterAll(() => server.close());
```

### 4. Configure Vitest

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    setupFiles: ['./test/setup.ts'],
  }
});
```

---

## Writing Handlers

### Response Types

```typescript
import { http, HttpResponse } from 'msw';

// JSON response
http.get('/api/data', () => {
  return HttpResponse.json({ key: 'value' });
});

// Text response
http.get('/api/text', () => {
  return HttpResponse.text('Plain text response');
});

// Binary/Blob response
http.get('/api/file', () => {
  return HttpResponse.arrayBuffer(buffer);
});

// No content
http.delete('/api/item/:id', () => {
  return new HttpResponse(null, { status: 204 });
});
```

### Request Data

```typescript
http.post('/api/submit', async ({ request }) => {
  // JSON body
  const json = await request.json();
  
  // Form data
  const formData = await request.formData();
  
  // Text body
  const text = await request.text();
  
  // Headers
  const authHeader = request.headers.get('Authorization');
  
  // URL and search params
  const url = new URL(request.url);
  const page = url.searchParams.get('page');
  
  return HttpResponse.json({ received: json });
});
```

### URL Parameters

```typescript
// Path parameters
http.get('/api/users/:userId/posts/:postId', ({ params }) => {
  const { userId, postId } = params;
  return HttpResponse.json({ userId, postId });
});

// Query parameters
http.get('/api/search', ({ request }) => {
  const url = new URL(request.url);
  const query = url.searchParams.get('q');
  const page = url.searchParams.get('page') || '1';
  
  return HttpResponse.json({
    query,
    page: parseInt(page),
    results: []
  });
});
```

### Error Responses

```typescript
// 404 Not Found
http.get('/api/users/:id', ({ params }) => {
  if (params.id === 'unknown') {
    return HttpResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }
  return HttpResponse.json({ id: params.id, name: 'User' });
});

// 500 Server Error
http.get('/api/data', () => {
  return HttpResponse.json(
    { error: 'Internal server error' },
    { status: 500 }
  );
});

// Network Error (connection failed)
http.get('/api/unreachable', () => {
  return HttpResponse.error();
});
```

### Response Headers

```typescript
http.get('/api/data', () => {
  return HttpResponse.json(
    { data: 'value' },
    {
      status: 200,
      headers: {
        'X-Custom-Header': 'custom-value',
        'Cache-Control': 'no-cache'
      }
    }
  );
});
```

### Delayed Responses

```typescript
import { delay, http, HttpResponse } from 'msw';

http.get('/api/slow', async () => {
  await delay(2000); // 2 second delay
  return HttpResponse.json({ data: 'finally' });
});

// Realistic network delay
http.get('/api/realistic', async () => {
  await delay('real'); // Random realistic delay
  return HttpResponse.json({ data: 'value' });
});
```

---

## Test Integration

### Override Handlers Per Test

```typescript
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('handles API error', async () => {
  // Override default handler for this test
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json(
        { error: 'Service unavailable' },
        { status: 503 }
      );
    })
  );

  const result = await fetchUsers();
  
  expect(result.error).toBe('Service unavailable');
});

test('handles empty response', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json([]);
    })
  );

  const result = await fetchUsers();
  
  expect(result).toEqual([]);
});

// Note: server.resetHandlers() in afterEach restores defaults
```

### One-Time Handlers

```typescript
import { http, HttpResponse } from 'msw';

test('handles retry after failure', async () => {
  let callCount = 0;
  
  server.use(
    http.get('/api/data', () => {
      callCount++;
      if (callCount === 1) {
        return HttpResponse.json({ error: 'Temporary' }, { status: 500 });
      }
      return HttpResponse.json({ success: true });
    })
  );

  const result = await fetchWithRetry('/api/data');
  
  expect(callCount).toBe(2);
  expect(result.success).toBe(true);
});
```

### Testing Request Bodies

```typescript
import { http, HttpResponse } from 'msw';

test('sends correct request body', async () => {
  let capturedBody: any;
  
  server.use(
    http.post('/api/users', async ({ request }) => {
      capturedBody = await request.json();
      return HttpResponse.json({ id: '1' }, { status: 201 });
    })
  );

  await createUser({ name: 'Alice', email: 'alice@example.com' });
  
  expect(capturedBody).toEqual({
    name: 'Alice',
    email: 'alice@example.com'
  });
});
```

---

## Advanced Patterns

### Dynamic Responses Based on State

```typescript
// handlers.ts
let users = [
  { id: '1', name: 'Alice' }
];

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json(users);
  }),

  http.post('/api/users', async ({ request }) => {
    const newUser = await request.json();
    const user = { id: String(users.length + 1), ...newUser };
    users.push(user);
    return HttpResponse.json(user, { status: 201 });
  }),

  http.delete('/api/users/:id', ({ params }) => {
    users = users.filter(u => u.id !== params.id);
    return new HttpResponse(null, { status: 204 });
  })
];

// Reset state between tests
export function resetUsers() {
  users = [{ id: '1', name: 'Alice' }];
}
```

### GraphQL Support

```typescript
import { graphql, HttpResponse } from 'msw';

export const handlers = [
  graphql.query('GetUser', ({ variables }) => {
    return HttpResponse.json({
      data: {
        user: {
          id: variables.id,
          name: 'User ' + variables.id
        }
      }
    });
  }),

  graphql.mutation('CreateUser', async ({ variables }) => {
    return HttpResponse.json({
      data: {
        createUser: {
          id: 'new-id',
          name: variables.input.name
        }
      }
    });
  })
];
```

### Passthrough Requests

```typescript
import { http, passthrough } from 'msw';

export const handlers = [
  // Let this request pass through to real server
  http.get('/api/health', () => {
    return passthrough();
  }),

  // Conditionally passthrough
  http.get('/api/data', ({ request }) => {
    if (request.headers.get('X-Real-Request')) {
      return passthrough();
    }
    return HttpResponse.json({ mock: true });
  })
];
```

---

## Debugging

### Logging Requests

```typescript
// In setup
server.listen({
  onUnhandledRequest: 'warn' // or 'error' to fail tests
});
```

### Debug Handler

```typescript
http.get('/api/debug', ({ request }) => {
  console.log('Request URL:', request.url);
  console.log('Headers:', Object.fromEntries(request.headers));
  
  return HttpResponse.json({ debug: true });
});
```

### Common Issues

**1. Handler not matching:**
```typescript
// Make sure URL matches exactly
http.get('/api/users')     // matches /api/users
http.get('/api/users/')    // matches /api/users/ (trailing slash)
http.get('*/api/users')    // matches any origin
```

**2. Request body already consumed:**
```typescript
// Can only read body once
http.post('/api/data', async ({ request }) => {
  const body = await request.json();
  // const body2 = await request.json(); // ERROR!
  
  // Clone if you need to read twice
  const cloned = request.clone();
  const body1 = await request.json();
  const body2 = await cloned.json();
});
```

**3. Async handler issues:**
```typescript
// Must return Response, not Promise<void>
http.get('/api/data', async () => {
  await someAsyncSetup();
  return HttpResponse.json({ data: 'value' });
  // Don't forget the return!
});
```

---

## Best Practices

1. **Use `onUnhandledRequest: 'error'`** to catch missing handlers
2. **Reset handlers in afterEach** to prevent test pollution
3. **Override handlers per test** for error scenarios
4. **Keep default handlers happy-path** in the handlers file
5. **Test error handling** by overriding with error responses
6. **Capture request bodies** to verify correct API usage
7. **Use realistic delays** to test loading states
