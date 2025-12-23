---
name: playwright-expert
description: Expert advisor for end-to-end testing with Playwright. Use when (1) setting up Playwright in a new project, (2) rapidly covering legacy code with recorded tests, (3) writing reliable page locators, (4) visual regression testing with screenshots, (5) mocking APIs with HAR files, (6) configuring cross-browser testing, (7) debugging flaky E2E tests, (8) setting up Playwright in CI/CD, or (9) deciding between Playwright and component tests.
---

# Playwright Expert

Expert guidance for end-to-end browser testing with Playwright. Focus on rapid coverage for legacy code and reliable, maintainable tests.

## When to Use Playwright

| Use Playwright For | Use Component Tests For |
|-------------------|------------------------|
| Full user flows | Individual components |
| Legacy code coverage | New feature development |
| Cross-browser testing | Framework-specific behavior |
| Visual regression | Logic and state |
| Real network testing | Mocked API scenarios |

## Quick Start

### Installation

```bash
# Initialize Playwright
npm init playwright@latest

# This will:
# - Install @playwright/test
# - Download browsers
# - Create playwright.config.ts
# - Add example tests
# - Create GitHub Actions workflow
```

### First Test

```typescript
// tests/homepage.spec.ts
import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('/');
  
  await expect(page).toHaveTitle(/My App/);
  await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
});
```

### Running Tests

```bash
# Run all tests
npx playwright test

# Run with UI
npx playwright test --ui

# Run specific file
npx playwright test tests/login.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode
npx playwright test --debug
```

## Test Recording (Rapid Coverage)

**The fastest way to cover legacy apps.** Record user actions, get working tests.

### Recording a Test

```bash
# Start recorder
npx playwright codegen http://localhost:3000

# Opens browser + inspector
# - Click around your app
# - Code generated in real-time
# - Copy to test file
```

### Recording Workflow

1. Start your dev server
2. Run `npx playwright codegen <url>`
3. Interact with your app
4. Copy generated code to test file
5. Clean up selectors (improve them)
6. Add assertions

### Record from Test File

```typescript
test('record new test', async ({ page }) => {
  await page.goto('/');
  await page.pause();  // Opens inspector for recording
});
```

## Locators

### Priority (Like Testing Library)

```typescript
// Best: Role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('link', { name: 'Home' })

// Good: Text-based
page.getByText('Welcome back')
page.getByLabel('Password')
page.getByPlaceholder('Enter email')

// Acceptable: Test IDs
page.getByTestId('custom-widget')

// Last resort: CSS selectors
page.locator('.submit-btn')
page.locator('#email-input')
```

### Locator Methods

```typescript
// Text content
page.getByText('Hello')           // Contains text
page.getByText('Hello', { exact: true })  // Exact match

// Form elements
page.getByLabel('Email')          // Associated label
page.getByPlaceholder('Search')   // Placeholder text

// Semantic roles
page.getByRole('button')
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { level: 1 })

// Test ID
page.getByTestId('hero-section')

// Alt text
page.getByAltText('Company logo')

// Title attribute
page.getByTitle('Close dialog')
```

### Filtering and Chaining

```typescript
// Filter by text
page.getByRole('listitem').filter({ hasText: 'Product A' })

// Filter by child
page.getByRole('listitem').filter({ 
  has: page.getByRole('button', { name: 'Buy' }) 
})

// Chain locators
page.getByRole('article').getByRole('heading')

// Nth element
page.getByRole('listitem').nth(0)
page.getByRole('listitem').first()
page.getByRole('listitem').last()
```

## Actions

### Clicking

```typescript
await page.getByRole('button', { name: 'Submit' }).click();

// Double click
await page.getByRole('button').dblclick();

// Right click
await page.getByRole('button').click({ button: 'right' });

// Force click (bypasses actionability checks)
await page.getByRole('button').click({ force: true });
```

### Typing

```typescript
// Type text
await page.getByLabel('Email').fill('user@example.com');

// Type slowly (like real user)
await page.getByLabel('Email').pressSequentially('user@example.com');

// Clear and type
await page.getByLabel('Email').clear();
await page.getByLabel('Email').fill('new@example.com');

// Press keys
await page.keyboard.press('Enter');
await page.keyboard.press('Control+A');
```

### Selecting

```typescript
// Select by value
await page.getByLabel('Country').selectOption('usa');

// Select by label text
await page.getByLabel('Country').selectOption({ label: 'United States' });

// Multiple selection
await page.getByLabel('Tags').selectOption(['tag1', 'tag2']);
```

### Checkboxes and Radio

```typescript
// Check
await page.getByLabel('Accept terms').check();

// Uncheck
await page.getByLabel('Subscribe').uncheck();

// Set specific state
await page.getByLabel('Remember me').setChecked(true);
```

## Assertions

```typescript
// Visibility
await expect(page.getByText('Welcome')).toBeVisible();
await expect(page.getByText('Error')).toBeHidden();

// Enabled/Disabled
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('button')).toBeDisabled();

// Checked
await expect(page.getByRole('checkbox')).toBeChecked();

// Text content
await expect(page.getByRole('alert')).toHaveText('Success');
await expect(page.getByRole('alert')).toContainText('Success');

// Attribute
await expect(page.getByRole('link')).toHaveAttribute('href', '/home');

// Count
await expect(page.getByRole('listitem')).toHaveCount(5);

// Page
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveTitle('Dashboard | App');
```

## Visual Testing (Screenshots)

### Basic Screenshot

```typescript
test('homepage looks correct', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});
```

### Element Screenshot

```typescript
test('button styles correct', async ({ page }) => {
  await page.goto('/');
  const button = page.getByRole('button', { name: 'Submit' });
  await expect(button).toHaveScreenshot('submit-button.png');
});
```

### Update Screenshots

```bash
# Update all screenshots
npx playwright test --update-snapshots

# Update specific test
npx playwright test login.spec.ts --update-snapshots
```

### Screenshot Options

```typescript
await expect(page).toHaveScreenshot('page.png', {
  fullPage: true,           // Capture entire page
  maxDiffPixels: 100,       // Allow small differences
  maxDiffPixelRatio: 0.02,  // 2% different pixels OK
  mask: [page.getByTestId('dynamic-content')],  // Ignore areas
  animations: 'disabled',   // Disable animations first
});
```

## API Mocking

### Using HAR Files

Record real API responses and replay them:

```bash
# Record HAR file
npx playwright open --save-har=api.har http://localhost:3000

# Use in tests
```

```typescript
test.use({
  // Replay from HAR file
  har: 'api.har'
});

test('uses recorded API responses', async ({ page }) => {
  await page.goto('/');
  // All API calls served from HAR
  await expect(page.getByText('Data loaded')).toBeVisible();
});
```

### Inline Mocking

```typescript
test('handles API error', async ({ page }) => {
  // Mock before navigation
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' })
    });
  });
  
  await page.goto('/users');
  await expect(page.getByText('Failed to load users')).toBeVisible();
});
```

### Dynamic Responses

```typescript
test('handles different responses', async ({ page }) => {
  let callCount = 0;
  
  await page.route('**/api/data', route => {
    callCount++;
    if (callCount === 1) {
      route.fulfill({ status: 500 });
    } else {
      route.fulfill({ 
        status: 200,
        body: JSON.stringify({ data: 'success' })
      });
    }
  });
  
  await page.goto('/');
  // First load fails, retry succeeds
});
```

## Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  
  // Timeout per test
  timeout: 30000,
  
  // Assertion timeout
  expect: { timeout: 5000 },
  
  // Retry failed tests
  retries: process.env.CI ? 2 : 0,
  
  // Parallel workers
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter
  reporter: [
    ['html'],
    ['list']
  ],
  
  use: {
    // Base URL
    baseURL: 'http://localhost:3000',
    
    // Browser options
    headless: true,
    viewport: { width: 1280, height: 720 },
    
    // Artifacts
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
  },
  
  // Browser projects
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
  
  // Dev server
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Debugging

### Pause Execution

```typescript
test('debug this', async ({ page }) => {
  await page.goto('/');
  
  await page.pause();  // Opens inspector
  
  // Continue after debugging
});
```

### Trace Viewer

```bash
# Run with trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Console Logs

```typescript
// Listen to console
page.on('console', msg => console.log(msg.text()));

// Listen to errors
page.on('pageerror', err => console.log(err.message));
```

## Resources

- **Configuration**: See [references/configuration.md](references/configuration.md) for detailed config options
- **Locators Guide**: See [references/locators-guide.md](references/locators-guide.md) for selector patterns

## Response Guidelines

When answering Playwright questions:

1. **Suggest recording** - For new tests, start with codegen
2. **Check locators** - Are they using role/text over CSS?
3. **Check waits** - Playwright auto-waits, explicit waits rarely needed
4. **Check assertions** - Using expect() with await?
5. **Suggest HAR mocking** - For reliable, fast API tests
