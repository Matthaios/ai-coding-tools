# Component Testing Patterns

Common patterns and solutions for React component testing.

## Table of Contents
1. [Form Testing](#form-testing)
2. [Async Operations](#async-operations)
3. [State Management](#state-management)
4. [User Interactions](#user-interactions)
5. [Error Handling](#error-handling)
6. [Accessibility Testing](#accessibility-testing)
7. [Custom Render Utilities](#custom-render-utilities)

---

## Form Testing

### Basic Form Submission

```typescript
test('submits form with user input', async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  
  render(<ContactForm onSubmit={handleSubmit} />);
  
  // Fill form fields
  await user.type(screen.getByLabelText('Name'), 'Alice');
  await user.type(screen.getByLabelText('Email'), 'alice@example.com');
  await user.type(screen.getByLabelText('Message'), 'Hello there');
  
  // Submit
  await user.click(screen.getByRole('button', { name: 'Send' }));
  
  // Verify
  expect(handleSubmit).toHaveBeenCalledWith({
    name: 'Alice',
    email: 'alice@example.com',
    message: 'Hello there'
  });
});
```

### Form Validation

```typescript
test('shows validation errors on invalid input', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);
  
  // Submit empty form
  await user.click(screen.getByRole('button', { name: 'Login' }));
  
  // Check for error messages
  expect(screen.getByText('Email is required')).toBeInTheDocument();
  expect(screen.getByText('Password is required')).toBeInTheDocument();
  
  // Invalid email format
  await user.type(screen.getByLabelText('Email'), 'invalid');
  await user.click(screen.getByRole('button', { name: 'Login' }));
  
  expect(screen.getByText('Invalid email format')).toBeInTheDocument();
});
```

### Disabled Submit Until Valid

```typescript
test('submit disabled until form valid', async () => {
  const user = userEvent.setup();
  render(<RegistrationForm />);
  
  const submitButton = screen.getByRole('button', { name: 'Register' });
  
  // Initially disabled
  expect(submitButton).toBeDisabled();
  
  // Fill required fields
  await user.type(screen.getByLabelText('Username'), 'alice');
  await user.type(screen.getByLabelText('Password'), 'password123');
  await user.type(screen.getByLabelText('Confirm Password'), 'password123');
  
  // Now enabled
  expect(submitButton).toBeEnabled();
});
```

### Select and Checkbox

```typescript
test('handles select and checkbox', async () => {
  const user = userEvent.setup();
  render(<PreferencesForm />);
  
  // Select option
  await user.selectOptions(
    screen.getByRole('combobox', { name: 'Country' }),
    'USA'
  );
  
  // Toggle checkbox
  const newsletter = screen.getByRole('checkbox', { name: 'Subscribe' });
  expect(newsletter).not.toBeChecked();
  
  await user.click(newsletter);
  expect(newsletter).toBeChecked();
  
  // Radio buttons
  await user.click(screen.getByRole('radio', { name: 'Dark mode' }));
  expect(screen.getByRole('radio', { name: 'Dark mode' })).toBeChecked();
});
```

---

## Async Operations

### Loading States

```typescript
test('shows loading then data', async () => {
  render(<UserProfile userId="123" />);
  
  // Loading state shown first
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
  
  // Wait for data
  await screen.findByText('Alice');
  
  // Loading state gone
  expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
});
```

### waitFor for Complex Conditions

```typescript
test('updates count after async operation', async () => {
  render(<Counter />);
  
  await user.click(screen.getByRole('button', { name: 'Increment' }));
  
  // Wait for async update
  await waitFor(() => {
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### waitForElementToBeRemoved

```typescript
test('removes item after delete', async () => {
  const user = userEvent.setup();
  render(<TodoList items={[{ id: '1', text: 'Task 1' }]} />);
  
  const item = screen.getByText('Task 1');
  await user.click(screen.getByRole('button', { name: 'Delete' }));
  
  // Wait for removal
  await waitForElementToBeRemoved(item);
  
  expect(screen.queryByText('Task 1')).not.toBeInTheDocument();
});
```

### Testing Debounced Input

```typescript
test('searches after debounce', async () => {
  vi.useFakeTimers();
  const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
  
  render(<SearchInput />);
  
  await user.type(screen.getByRole('searchbox'), 'query');
  
  // No results yet (debounced)
  expect(screen.queryByText(/results/i)).not.toBeInTheDocument();
  
  // Advance past debounce time
  vi.advanceTimersByTime(500);
  
  // Now results appear
  await screen.findByText(/results for "query"/i);
  
  vi.useRealTimers();
});
```

---

## State Management

### Testing with Redux

```typescript
// test-utils.tsx
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { rootReducer } from './store';

function renderWithStore(
  ui: React.ReactElement,
  { preloadedState = {}, store = configureStore({ 
    reducer: rootReducer, 
    preloadedState 
  }) } = {}
) {
  function Wrapper({ children }) {
    return <Provider store={store}>{children}</Provider>;
  }
  return { ...render(ui, { wrapper: Wrapper }), store };
}

// Usage
test('displays user from store', () => {
  renderWithStore(<UserBadge />, {
    preloadedState: { user: { name: 'Alice', role: 'Admin' } }
  });
  
  expect(screen.getByText('Alice')).toBeInTheDocument();
  expect(screen.getByText('Admin')).toBeInTheDocument();
});
```

### Testing Context

```typescript
function renderWithTheme(ui, { theme = 'light' } = {}) {
  return render(
    <ThemeProvider value={theme}>
      {ui}
    </ThemeProvider>
  );
}

test('applies dark theme styles', () => {
  renderWithTheme(<ThemedButton>Click</ThemedButton>, { theme: 'dark' });
  
  const button = screen.getByRole('button');
  expect(button).toHaveClass('dark-theme');
});
```

### Testing Local State

```typescript
test('toggles between edit and view mode', async () => {
  const user = userEvent.setup();
  render(<EditableField initialValue="Hello" />);
  
  // View mode
  expect(screen.getByText('Hello')).toBeInTheDocument();
  expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
  
  // Enter edit mode
  await user.click(screen.getByRole('button', { name: 'Edit' }));
  
  // Edit mode
  expect(screen.getByRole('textbox')).toHaveValue('Hello');
  
  // Save
  await user.clear(screen.getByRole('textbox'));
  await user.type(screen.getByRole('textbox'), 'World');
  await user.click(screen.getByRole('button', { name: 'Save' }));
  
  // Back to view mode
  expect(screen.getByText('World')).toBeInTheDocument();
});
```

---

## User Interactions

### Click Events

```typescript
test('handles click events', async () => {
  const handleClick = vi.fn();
  const user = userEvent.setup();
  
  render(<Button onClick={handleClick}>Click me</Button>);
  
  await user.click(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalledTimes(1);
  
  // Double click
  await user.dblClick(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalledTimes(3);
});
```

### Keyboard Navigation

```typescript
test('supports keyboard navigation', async () => {
  const user = userEvent.setup();
  render(<TabList items={['Tab 1', 'Tab 2', 'Tab 3']} />);
  
  // Focus first tab
  screen.getByRole('tab', { name: 'Tab 1' }).focus();
  
  // Arrow key navigation
  await user.keyboard('{ArrowRight}');
  expect(screen.getByRole('tab', { name: 'Tab 2' })).toHaveFocus();
  
  await user.keyboard('{ArrowRight}');
  expect(screen.getByRole('tab', { name: 'Tab 3' })).toHaveFocus();
  
  // Wrap around
  await user.keyboard('{ArrowRight}');
  expect(screen.getByRole('tab', { name: 'Tab 1' })).toHaveFocus();
});
```

### Hover Events

```typescript
test('shows tooltip on hover', async () => {
  const user = userEvent.setup();
  render(<Tooltip content="Help text"><button>?</button></Tooltip>);
  
  // Tooltip not visible initially
  expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
  
  // Hover to show
  await user.hover(screen.getByRole('button'));
  expect(screen.getByRole('tooltip')).toHaveTextContent('Help text');
  
  // Unhover to hide
  await user.unhover(screen.getByRole('button'));
  await waitForElementToBeRemoved(() => screen.queryByRole('tooltip'));
});
```

### Drag and Drop

```typescript
test('reorders items via drag and drop', async () => {
  const user = userEvent.setup();
  render(<SortableList items={['A', 'B', 'C']} />);
  
  const itemA = screen.getByText('A');
  const itemC = screen.getByText('C');
  
  // Simulate drag
  await user.pointer([
    { keys: '[MouseLeft>]', target: itemA },
    { target: itemC },
    { keys: '[/MouseLeft]' }
  ]);
  
  // Check new order
  const items = screen.getAllByRole('listitem');
  expect(items[0]).toHaveTextContent('B');
  expect(items[1]).toHaveTextContent('C');
  expect(items[2]).toHaveTextContent('A');
});
```

---

## Error Handling

### Error Boundaries

```typescript
// Silence React error boundary console output
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (args[0]?.includes('Error boundary')) return;
    originalError.call(console, ...args);
  };
});
afterAll(() => {
  console.error = originalError;
});

test('shows fallback on error', () => {
  const ThrowError = () => { throw new Error('Test error'); };
  
  render(
    <ErrorBoundary fallback={<div>Something went wrong</div>}>
      <ThrowError />
    </ErrorBoundary>
  );
  
  expect(screen.getByText('Something went wrong')).toBeInTheDocument();
});
```

### API Errors

```typescript
test('shows error message on API failure', async () => {
  // Mock API to fail
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ error: 'Server error' }, { status: 500 });
    })
  );
  
  render(<UserList />);
  
  await screen.findByText('Failed to load users');
  expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
});
```

---

## Accessibility Testing

### Basic Accessibility Check

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('has no accessibility violations', async () => {
  const { container } = render(<Form />);
  
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Focus Management

```typescript
test('manages focus correctly', async () => {
  const user = userEvent.setup();
  render(<Modal trigger={<button>Open</button>} />);
  
  // Open modal
  await user.click(screen.getByRole('button', { name: 'Open' }));
  
  // Focus should be inside modal
  const modal = screen.getByRole('dialog');
  expect(modal).toContainElement(document.activeElement);
  
  // Close modal
  await user.click(screen.getByRole('button', { name: 'Close' }));
  
  // Focus should return to trigger
  expect(screen.getByRole('button', { name: 'Open' })).toHaveFocus();
});
```

---

## Custom Render Utilities

### Full Provider Wrapper

```typescript
// test/test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '../theme';
import { createTestStore } from './createTestStore';

interface Options extends RenderOptions {
  preloadedState?: object;
  route?: string;
  queryClient?: QueryClient;
}

export function renderApp(ui: React.ReactElement, {
  preloadedState = {},
  route = '/',
  queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  }),
  ...options
}: Options = {}) {
  const store = createTestStore(preloadedState);
  
  function Wrapper({ children }) {
    return (
      <QueryClientProvider client={queryClient}>
        <Provider store={store}>
          <MemoryRouter initialEntries={[route]}>
            <ThemeProvider>
              {children}
            </ThemeProvider>
          </MemoryRouter>
        </Provider>
      </QueryClientProvider>
    );
  }
  
  return {
    ...render(ui, { wrapper: Wrapper, ...options }),
    store,
    queryClient
  };
}

// Re-export
export * from '@testing-library/react';
export { renderApp as render };
```

### Usage

```typescript
import { render, screen } from '../test/test-utils';

test('shows user profile page', async () => {
  render(<App />, {
    route: '/profile/123',
    preloadedState: {
      auth: { user: { id: '123', name: 'Alice' } }
    }
  });
  
  expect(await screen.findByText('Alice')).toBeInTheDocument();
});
```
