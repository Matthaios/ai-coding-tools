---
name: component-testing-expert
description: Expert advisor for React component testing with Testing Library. Use when (1) setting up component test infrastructure with Vitest, (2) writing user-centric tests instead of testing implementation details, (3) choosing between selectors (getByRole, getByText, getByTestId), (4) handling async DOM updates with waitFor, (5) creating custom render functions with providers, (6) testing forms, inputs, buttons, and lists, (7) debugging test isolation issues, (8) adding accessibility testing with jest-axe, or (9) deciding what to test at component level vs unit level.
---

# Component Testing Expert

Expert guidance for testing React components with Testing Library. Core philosophy: **test from the user's perspective, not implementation details**.

## Core Principles

### 1. Test User Behavior, Not Implementation

Your tests should resemble how users interact with your app, not how it's built internally.

```typescript
// BAD: Testing implementation details
expect(component.state.isOpen).toBe(true);
expect(wrapper.find('InternalDropdown').props().visible).toBe(true);

// GOOD: Testing user experience
expect(screen.getByRole('listbox')).toBeVisible();
expect(screen.getByText('Option 1')).toBeInTheDocument();
```

### 2. Selector Priority

Use the most accessible selector available:

| Priority | Selector | When to Use |
|----------|----------|-------------|
| 1 | `getByRole` | **Preferred** - accessible to everyone |
| 2 | `getByLabelText` | Form fields with labels |
| 3 | `getByPlaceholderText` | When label isn't visible |
| 4 | `getByText` | Non-interactive content |
| 5 | `getByDisplayValue` | Current input values |
| 6 | `getByAltText` | Images |
| 7 | `getByTitle` | Title attributes |
| 8 | `getByTestId` | **Last resort** - when nothing else works |

```typescript
// Best: Accessible, works with screen readers
screen.getByRole('button', { name: 'Submit' });
screen.getByRole('textbox', { name: 'Email' });
screen.getByRole('checkbox', { name: 'Accept terms' });

// Good: Form-specific
screen.getByLabelText('Email');
screen.getByPlaceholderText('Enter your email');

// Acceptable: Content-based
screen.getByText('Welcome back!');

// Last resort: Test ID
screen.getByTestId('complex-widget');
```

### 3. Query Variants

| Prefix | Returns | Throws on Missing | Use Case |
|--------|---------|-------------------|----------|
| `getBy` | Element | Yes | Element should exist |
| `queryBy` | Element or null | No | Element might not exist |
| `findBy` | Promise<Element> | Yes (after timeout) | Async appearance |

```typescript
// Element must exist right now
const button = screen.getByRole('button');

// Element might not exist
const error = screen.queryByText('Error message');
expect(error).not.toBeInTheDocument();

// Element will appear after async operation
const result = await screen.findByText('Data loaded');
```

### 4. User Events Over Fire Events

`userEvent` simulates real user behavior; `fireEvent` triggers DOM events directly.

```typescript
import userEvent from '@testing-library/user-event';

// Setup user event instance
const user = userEvent.setup();

// BAD: Direct event, not realistic
fireEvent.click(button);
fireEvent.change(input, { target: { value: 'hello' } });

// GOOD: Simulates real user typing
await user.click(button);
await user.type(input, 'hello');  // Triggers focus, keydown, keyup per char
```

User events include:
- `user.click()` - Focus + click
- `user.dblClick()` - Double click
- `user.type()` - Focus + keydown/keyup per character
- `user.clear()` - Select all + delete
- `user.selectOptions()` - Select dropdown options
- `user.tab()` - Tab navigation

## Basic Test Structure

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
  test('increments count when button clicked', async () => {
    // Arrange
    const user = userEvent.setup();
    render(<Counter initialCount={0} />);
    
    // Act
    const button = screen.getByRole('button', { name: /increment/i });
    await user.click(button);
    
    // Assert
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

## Async Testing

### waitFor - Waiting for Conditions

```typescript
import { render, screen, waitFor } from '@testing-library/react';

test('loads data after fetch', async () => {
  render(<DataLoader />);
  
  // Wait for element to appear
  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});

// Or use findBy (combines getBy + waitFor)
test('loads data after fetch', async () => {
  render(<DataLoader />);
  
  const result = await screen.findByText('Data loaded');
  expect(result).toBeInTheDocument();
});
```

### waitForElementToBeRemoved

```typescript
test('hides loading spinner when done', async () => {
  render(<AsyncComponent />);
  
  // Spinner appears first
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
  
  // Wait for it to disappear
  await waitForElementToBeRemoved(() => screen.queryByRole('progressbar'));
  
  // Data is now shown
  expect(screen.getByText('Data ready')).toBeInTheDocument();
});
```

## Custom Render with Providers

Most apps need context providers (Redux, Router, Theme). Create a custom render:

```typescript
// test/test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from './theme';
import { createStore } from './store';

interface CustomRenderOptions extends RenderOptions {
  preloadedState?: Partial<RootState>;
  route?: string;
}

function customRender(
  ui: React.ReactElement,
  {
    preloadedState = {},
    route = '/',
    ...renderOptions
  }: CustomRenderOptions = {}
) {
  window.history.pushState({}, 'Test page', route);
  
  const store = createStore(preloadedState);
  
  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </BrowserRouter>
      </Provider>
    );
  }
  
  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    store
  };
}

// Re-export everything
export * from '@testing-library/react';
export { customRender as render };
```

Usage:
```typescript
import { render, screen } from '../test/test-utils';

test('shows user profile', () => {
  render(<UserProfile />, {
    preloadedState: { user: { name: 'Alice' } }
  });
  
  expect(screen.getByText('Alice')).toBeInTheDocument();
});
```

## Test Isolation

### The Problem: Shared State

```typescript
// BAD: Tests pollute each other
describe('ItemList', () => {
  test('adds item', async () => {
    render(<ItemList />);
    await user.type(input, 'Item 1');
    await user.click(addButton);
    expect(screen.getByText('Item 1')).toBeInTheDocument();
  });
  
  test('starts empty', () => {
    render(<ItemList />);  // Still has 'Item 1' from previous test!
    expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
  });
});
```

### Solutions

**1. Isolate with custom render:**
```typescript
// Fresh store per render
function customRender(ui, options) {
  const store = createStore();  // New store each time
  return render(<Provider store={store}>{ui}</Provider>, options);
}
```

**2. Test component + state wrapper:**
```typescript
// Export both connected and unconnected
export function ItemListUI({ items, addItem }) { /* pure view */ }
export function ItemList() {
  const items = useSelector(selectItems);
  const dispatch = useDispatch();
  return <ItemListUI items={items} addItem={(i) => dispatch(add(i))} />;
}

// Test the UI component directly with props
test('renders items', () => {
  render(<ItemListUI items={['A', 'B']} addItem={vi.fn()} />);
  expect(screen.getAllByRole('listitem')).toHaveLength(2);
});
```

## Common Patterns

### Testing Forms

```typescript
test('submits form with entered data', async () => {
  const onSubmit = vi.fn();
  const user = userEvent.setup();
  
  render(<ContactForm onSubmit={onSubmit} />);
  
  await user.type(screen.getByLabelText('Name'), 'Alice');
  await user.type(screen.getByLabelText('Email'), 'alice@example.com');
  await user.click(screen.getByRole('button', { name: 'Submit' }));
  
  expect(onSubmit).toHaveBeenCalledWith({
    name: 'Alice',
    email: 'alice@example.com'
  });
});
```

### Testing Disabled States

```typescript
test('button disabled until form valid', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);
  
  const submitButton = screen.getByRole('button', { name: 'Login' });
  
  // Initially disabled
  expect(submitButton).toBeDisabled();
  
  // Fill required fields
  await user.type(screen.getByLabelText('Email'), 'test@example.com');
  await user.type(screen.getByLabelText('Password'), 'password123');
  
  // Now enabled
  expect(submitButton).toBeEnabled();
});
```

### Testing Lists

```typescript
test('renders list of items', () => {
  render(<TodoList items={['Task 1', 'Task 2', 'Task 3']} />);
  
  const items = screen.getAllByRole('listitem');
  expect(items).toHaveLength(3);
  expect(items[0]).toHaveTextContent('Task 1');
});

test('adds item to list', async () => {
  const user = userEvent.setup();
  render(<TodoList items={[]} />);
  
  await user.type(screen.getByRole('textbox'), 'New task');
  await user.click(screen.getByRole('button', { name: 'Add' }));
  
  expect(screen.getByText('New task')).toBeInTheDocument();
});
```

### Testing Error States

```typescript
test('shows validation error', async () => {
  const user = userEvent.setup();
  render(<EmailInput />);
  
  const input = screen.getByLabelText('Email');
  await user.type(input, 'invalid-email');
  await user.tab();  // Blur to trigger validation
  
  expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
  expect(input).toHaveAttribute('aria-invalid', 'true');
});
```

## Debugging

### screen.debug()

```typescript
test('debugging', () => {
  render(<MyComponent />);
  
  // Print entire DOM
  screen.debug();
  
  // Print specific element
  screen.debug(screen.getByRole('button'));
  
  // With more output
  screen.debug(undefined, 30000);  // More characters
});
```

### logRoles

```typescript
import { logRoles } from '@testing-library/react';

test('finding roles', () => {
  const { container } = render(<MyComponent />);
  logRoles(container);
  // Prints all ARIA roles in the component
});
```

## Resources

- **Selectors Guide**: See [references/selectors-guide.md](references/selectors-guide.md) for selector examples and priorities
- **Testing Patterns**: See [references/testing-patterns.md](references/testing-patterns.md) for common patterns
- **Accessibility Testing**: See [references/accessibility-testing.md](references/accessibility-testing.md) for jest-axe setup

## Response Guidelines

When answering questions about component tests:

1. **Check selectors** - Are they using accessible queries?
2. **Check async handling** - Are findBy/waitFor used appropriately?
3. **Check user events** - Is userEvent used instead of fireEvent?
4. **Check isolation** - Could tests pollute each other?
5. **Suggest splitting** - Would unit testing the logic be easier?
