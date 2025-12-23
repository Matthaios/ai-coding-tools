# Testing Library Selectors Guide

Complete reference for choosing and using the right selectors.

## Table of Contents
1. [Selector Priority](#selector-priority)
2. [Query Variants](#query-variants)
3. [Role Queries](#role-queries)
4. [Text Queries](#text-queries)
5. [Form Queries](#form-queries)
6. [TestId Queries](#testid-queries)
7. [Common Patterns](#common-patterns)
8. [Troubleshooting](#troubleshooting)

---

## Selector Priority

Use the most accessible selector available. This order reflects what users actually interact with:

### Priority 1: Accessible to Everyone

```typescript
// Roles - accessible to mouse, keyboard, and screen readers
screen.getByRole('button', { name: 'Submit' })
screen.getByRole('textbox', { name: 'Email' })
screen.getByRole('link', { name: 'Home' })

// Labels - how users identify form fields
screen.getByLabelText('Password')
```

### Priority 2: Semantic Queries

```typescript
// Placeholder text
screen.getByPlaceholderText('Enter email')

// Text content
screen.getByText('Welcome back!')

// Alt text (images)
screen.getByAltText('Company logo')

// Title attribute
screen.getByTitle('Close')
```

### Priority 3: Test IDs (Last Resort)

```typescript
// Only when nothing else works
screen.getByTestId('custom-dropdown')
```

---

## Query Variants

Each query type has 6 variants:

| Prefix | Returns | On Not Found | Use Case |
|--------|---------|--------------|----------|
| `getBy` | Element | Throws | Element must exist |
| `getAllBy` | Element[] | Throws | Multiple elements must exist |
| `queryBy` | Element \| null | Returns null | Check non-existence |
| `queryAllBy` | Element[] | Returns [] | Multiple might not exist |
| `findBy` | Promise<Element> | Throws (after timeout) | Async appearance |
| `findAllBy` | Promise<Element[]> | Throws (after timeout) | Async multiple |

### When to Use Each

```typescript
// getBy - Element must exist right now
const button = screen.getByRole('button');

// queryBy - Check element doesn't exist
expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

// findBy - Wait for element to appear
const modal = await screen.findByRole('dialog');

// getAllBy - Multiple elements exist
const items = screen.getAllByRole('listitem');
expect(items).toHaveLength(3);

// queryAllBy - Check count including zero
expect(screen.queryAllByRole('listitem')).toHaveLength(0);

// findAllBy - Wait for multiple to appear
const results = await screen.findAllByRole('article');
```

---

## Role Queries

### Common ARIA Roles

```typescript
// Buttons
screen.getByRole('button', { name: 'Submit' })
screen.getByRole('button', { name: /submit/i })  // Regex for flexibility

// Links
screen.getByRole('link', { name: 'Go to Home' })

// Inputs
screen.getByRole('textbox', { name: 'Email' })        // <input type="text">
screen.getByRole('textbox', { name: 'Description' })  // <textarea>
screen.getByRole('spinbutton', { name: 'Quantity' })  // <input type="number">
screen.getByRole('checkbox', { name: 'Accept' })
screen.getByRole('radio', { name: 'Option A' })
screen.getByRole('combobox', { name: 'Country' })     // <select>
screen.getByRole('searchbox', { name: 'Search' })     // <input type="search">

// Structure
screen.getByRole('heading', { name: 'Welcome' })
screen.getByRole('heading', { level: 1 })             // <h1>
screen.getByRole('list')
screen.getByRole('listitem')
screen.getByRole('table')
screen.getByRole('row')
screen.getByRole('cell')

// Interactive
screen.getByRole('dialog')
screen.getByRole('menu')
screen.getByRole('menuitem')
screen.getByRole('tab')
screen.getByRole('tabpanel')
screen.getByRole('alert')
screen.getByRole('progressbar')

// Navigation
screen.getByRole('navigation')
screen.getByRole('main')
screen.getByRole('banner')          // <header>
screen.getByRole('contentinfo')     // <footer>
```

### Role Options

```typescript
// Filter by name (accessible name)
screen.getByRole('button', { name: 'Submit' })
screen.getByRole('button', { name: /submit/i })  // Case insensitive

// Check state
screen.getByRole('button', { pressed: true })
screen.getByRole('checkbox', { checked: true })
screen.getByRole('button', { expanded: true })
screen.getByRole('textbox', { selected: true })

// Heading level
screen.getByRole('heading', { level: 2 })  // <h2>

// Hidden elements (normally excluded)
screen.getByRole('button', { hidden: true })
```

### Finding Accessible Names

Accessible name comes from (in priority order):
1. `aria-label` attribute
2. `aria-labelledby` reference
3. Associated `<label>` element
4. Text content
5. `title` attribute
6. `alt` text (for images)

```html
<!-- All have accessible name "Close" -->
<button aria-label="Close">X</button>
<button><span aria-hidden="true">X</span> Close</button>
<label>Close <button>X</button></label>
<button title="Close">X</button>
```

---

## Text Queries

### getByText

```typescript
// Exact match
screen.getByText('Hello World')

// Substring match
screen.getByText('Hello', { exact: false })

// Regex
screen.getByText(/hello/i)  // Case insensitive
screen.getByText(/^hello/)  // Starts with
screen.getByText(/world$/)  // Ends with

// Function matcher
screen.getByText((content, element) => {
  return content.startsWith('Item') && element.tagName === 'LI';
})
```

### Text in Specific Elements

```typescript
// Match text within specific element type
screen.getByText('Submit', { selector: 'button' })
screen.getByText('Title', { selector: 'h1' })

// Ignore certain elements
screen.getByText('Content', { ignore: 'script, style' })
```

---

## Form Queries

### getByLabelText

```typescript
// <label>Email <input /></label>
screen.getByLabelText('Email')

// <label for="email">Email</label> <input id="email" />
screen.getByLabelText('Email')

// <label id="email-label">Email</label> <input aria-labelledby="email-label" />
screen.getByLabelText('Email')

// Selector specificity
screen.getByLabelText('Email', { selector: 'input' })
```

### getByPlaceholderText

```typescript
// <input placeholder="Enter your email" />
screen.getByPlaceholderText('Enter your email')
screen.getByPlaceholderText(/email/i)
```

### getByDisplayValue

```typescript
// Current input value
screen.getByDisplayValue('current text')

// Select current option
screen.getByDisplayValue('Selected Option')
```

---

## TestId Queries

### Adding Test IDs

```typescript
// In component
<div data-testid="custom-component">
  Complex content
</div>

// In test
screen.getByTestId('custom-component')
```

### When to Use

Use test IDs when:
- No semantic HTML applies
- Element has no accessible name
- CSS classes/structure are unstable
- Complex custom components

```typescript
// Chart with no text content
<div data-testid="revenue-chart" role="img" aria-label="Revenue chart">
  <canvas />
</div>

// Custom dropdown with complex internals
<div data-testid="country-selector">
  {/* Complex implementation */}
</div>
```

### Configure Custom Attribute

```typescript
// In test setup
import { configure } from '@testing-library/react';

configure({ testIdAttribute: 'data-my-test-id' });

// Now use your attribute
<div data-my-test-id="component">
```

---

## Common Patterns

### Finding by Multiple Criteria

```typescript
// Button with specific text that's enabled
const submitButton = screen.getByRole('button', { 
  name: 'Submit',
  // Note: can't filter by enabled directly, check separately
});
expect(submitButton).toBeEnabled();

// Specific input in a form
const form = screen.getByRole('form');
within(form).getByLabelText('Email');
```

### Scoping Queries with within

```typescript
import { within } from '@testing-library/react';

// Get specific section first
const sidebar = screen.getByRole('complementary');
const mainNav = within(sidebar).getByRole('navigation');

// Query within that section
const homeLink = within(mainNav).getByRole('link', { name: 'Home' });
```

### Matching Partial Text

```typescript
// Product name includes dynamic price
screen.getByText(/iPhone/);  // Matches "iPhone 15 Pro - $999"

// Starts with
screen.getByText(/^Error:/);

// Ends with
screen.getByText(/\d+ items$/);

// Case insensitive
screen.getByText(/submit/i);
```

### Handling Dynamic Content

```typescript
// Text that changes
const counter = screen.getByRole('status');
expect(counter).toHaveTextContent('0');

// After action
await user.click(incrementButton);
expect(counter).toHaveTextContent('1');
```

---

## Troubleshooting

### Element Not Found

```typescript
// Debug the DOM
screen.debug();

// See what roles exist
import { logRoles } from '@testing-library/react';
logRoles(container);

// Check if element exists with queryBy
const element = screen.queryByRole('button');
console.log('Element:', element);
```

### Multiple Elements Found

```typescript
// Use getAllBy when multiple expected
const buttons = screen.getAllByRole('button');
expect(buttons).toHaveLength(3);

// Or be more specific
screen.getByRole('button', { name: 'Submit' });

// Or scope to container
const modal = screen.getByRole('dialog');
within(modal).getByRole('button', { name: 'Confirm' });
```

### Hidden Elements

```typescript
// Elements with display:none or visibility:hidden are excluded
// Include them with:
screen.getByRole('button', { hidden: true });

// Or use queryByTestId which doesn't check visibility
screen.getByTestId('hidden-element');
```

### Async Elements

```typescript
// Element appears after async operation
// BAD: Immediately fails
screen.getByText('Loaded');

// GOOD: Waits for appearance
await screen.findByText('Loaded');

// With custom timeout
await screen.findByText('Loaded', {}, { timeout: 5000 });
```

---

## Best Practices Summary

1. **Prefer role queries** - Most accessible and stable
2. **Use name option** - Narrows down when multiple match
3. **Regex for flexibility** - `/submit/i` over `'Submit'`
4. **within for scoping** - Query within sections
5. **queryBy for non-existence** - Check element doesn't exist
6. **findBy for async** - Wait for elements to appear
7. **testId as last resort** - Only when nothing else works
