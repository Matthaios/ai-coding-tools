# Playwright Configuration Reference

Complete guide to playwright.config.ts options.

## Table of Contents
1. [Basic Configuration](#basic-configuration)
2. [Test Options](#test-options)
3. [Browser Options](#browser-options)
4. [Projects](#projects)
5. [Web Server](#web-server)
6. [Reporters](#reporters)
7. [Advanced Options](#advanced-options)

---

## Basic Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Directory containing test files
  testDir: './tests',
  
  // Pattern for test files
  testMatch: '**/*.spec.ts',
  
  // Ignore patterns
  testIgnore: '**/helpers/**',
  
  // Output directory for artifacts
  outputDir: 'test-results',
});
```

---

## Test Options

### Timeouts

```typescript
export default defineConfig({
  // Global timeout per test (default: 30000ms)
  timeout: 60000,
  
  // Timeout for expect assertions (default: 5000ms)
  expect: {
    timeout: 10000,
  },
  
  // Timeout for page.goto (default: 30000ms)
  use: {
    navigationTimeout: 15000,
    actionTimeout: 10000,
  },
});
```

### Retries

```typescript
export default defineConfig({
  // Retry failed tests (0 = no retries)
  retries: process.env.CI ? 2 : 0,
  
  // Report slow tests
  reportSlowTests: {
    max: 5,
    threshold: 30000,
  },
});
```

### Parallelization

```typescript
export default defineConfig({
  // Run tests in parallel
  fullyParallel: true,
  
  // Number of workers
  workers: process.env.CI ? 1 : undefined,  // undefined = auto
  
  // Limit workers to percentage of CPUs
  // workers: '50%',
  
  // Forbid test.only in CI
  forbidOnly: !!process.env.CI,
});
```

---

## Browser Options

### Use Options

```typescript
export default defineConfig({
  use: {
    // Base URL for page.goto('/')
    baseURL: 'http://localhost:3000',
    
    // Browser viewport
    viewport: { width: 1280, height: 720 },
    
    // Run in headless mode
    headless: true,
    
    // Ignore HTTPS errors
    ignoreHTTPSErrors: true,
    
    // Extra HTTP headers
    extraHTTPHeaders: {
      'Accept-Language': 'en-US',
    },
    
    // HTTP credentials
    httpCredentials: {
      username: 'user',
      password: 'pass',
    },
    
    // Geolocation
    geolocation: { longitude: 12.4924, latitude: 41.8902 },
    permissions: ['geolocation'],
    
    // Locale and timezone
    locale: 'en-US',
    timezoneId: 'America/New_York',
    
    // Color scheme
    colorScheme: 'dark',  // 'light', 'dark', 'no-preference'
    
    // JavaScript enabled
    javaScriptEnabled: true,
    
    // User agent
    userAgent: 'Custom User Agent',
  },
});
```

### Artifacts

```typescript
export default defineConfig({
  use: {
    // Screenshots
    screenshot: 'only-on-failure',  // 'on', 'off', 'only-on-failure'
    
    // Videos
    video: 'retain-on-failure',  // 'on', 'off', 'retain-on-failure', 'on-first-retry'
    
    // Traces (for debugging)
    trace: 'retain-on-failure',  // 'on', 'off', 'retain-on-failure', 'on-first-retry'
  },
  
  // Preserve output on failure
  preserveOutput: 'failures-only',  // 'always', 'never', 'failures-only'
});
```

---

## Projects

Run tests across multiple configurations:

```typescript
export default defineConfig({
  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Mobile browsers
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
    
    // Tablet
    {
      name: 'tablet',
      use: { ...devices['iPad (gen 7)'] },
    },
  ],
});
```

### Project-Specific Settings

```typescript
projects: [
  {
    name: 'chromium',
    use: { 
      browserName: 'chromium',
      viewport: { width: 1920, height: 1080 },
      video: 'on',
    },
    testDir: './tests/desktop',
    testMatch: /desktop\.spec\.ts/,
    retries: 3,
  },
  {
    name: 'api-tests',
    testDir: './tests/api',
    use: {
      // No browser needed for API tests
    },
  },
]
```

### Dependent Projects

```typescript
projects: [
  {
    name: 'setup',
    testMatch: /global\.setup\.ts/,
  },
  {
    name: 'chromium',
    dependencies: ['setup'],  // Run setup first
    use: { ...devices['Desktop Chrome'] },
  },
]
```

---

## Web Server

Auto-start dev server before tests:

```typescript
export default defineConfig({
  webServer: {
    // Command to start server
    command: 'npm run dev',
    
    // Wait for this URL to be ready
    url: 'http://localhost:3000',
    
    // Or wait for specific port
    // port: 3000,
    
    // Timeout for server startup
    timeout: 120000,
    
    // Reuse existing server in dev
    reuseExistingServer: !process.env.CI,
    
    // Pipe stdout/stderr
    stdout: 'pipe',
    stderr: 'pipe',
    
    // Environment variables
    env: {
      NODE_ENV: 'test',
    },
  },
});
```

### Multiple Servers

```typescript
export default defineConfig({
  webServer: [
    {
      command: 'npm run dev',
      url: 'http://localhost:3000',
    },
    {
      command: 'npm run api',
      url: 'http://localhost:4000',
    },
  ],
});
```

---

## Reporters

### Built-in Reporters

```typescript
export default defineConfig({
  reporter: [
    // Console list output
    ['list'],
    
    // HTML report
    ['html', { outputFolder: 'playwright-report' }],
    
    // JSON output
    ['json', { outputFile: 'results.json' }],
    
    // JUnit XML
    ['junit', { outputFile: 'results.xml' }],
    
    // Dots only
    ['dot'],
    
    // Line per test
    ['line'],
    
    // GitHub Actions annotations
    ['github'],
  ],
});
```

### Conditional Reporters

```typescript
export default defineConfig({
  reporter: process.env.CI 
    ? [['github'], ['html']]
    : [['list'], ['html']],
});
```

### HTML Reporter Options

```typescript
reporter: [
  ['html', {
    outputFolder: 'playwright-report',
    open: 'never',  // 'always', 'never', 'on-failure'
  }],
],
```

---

## Advanced Options

### Global Setup/Teardown

```typescript
export default defineConfig({
  // Run before all tests
  globalSetup: require.resolve('./global-setup'),
  
  // Run after all tests
  globalTeardown: require.resolve('./global-teardown'),
});
```

```typescript
// global-setup.ts
export default async function globalSetup() {
  // Database seeding, authentication, etc.
  process.env.AUTH_TOKEN = 'test-token';
}
```

### Storage State (Authentication)

```typescript
// Setup project saves auth state
projects: [
  {
    name: 'setup',
    testMatch: /auth\.setup\.ts/,
  },
  {
    name: 'authenticated',
    dependencies: ['setup'],
    use: {
      // Reuse auth state
      storageState: 'playwright/.auth/user.json',
    },
  },
]
```

```typescript
// auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'user@example.com');
  await page.fill('[name=password]', 'password');
  await page.click('button[type=submit]');
  
  await page.waitForURL('/dashboard');
  
  // Save authentication state
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

### Snapshot Options

```typescript
export default defineConfig({
  expect: {
    // Snapshot comparison options
    toHaveScreenshot: {
      maxDiffPixels: 10,
      maxDiffPixelRatio: 0.02,
      threshold: 0.2,
      animations: 'disabled',
    },
    
    // Snapshot update mode
    toMatchSnapshot: {
      maxDiffPixelRatio: 0.02,
    },
  },
  
  // Snapshot directory
  snapshotDir: './snapshots',
  
  // Snapshot path template
  snapshotPathTemplate: '{testDir}/__snapshots__/{testFilePath}/{arg}{ext}',
});
```

### Environment Variables

```typescript
export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
  },
});

// Run with different URL:
// BASE_URL=https://staging.example.com npx playwright test
```

---

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          
      - name: Install dependencies
        run: npm ci
        
      - name: Install Playwright browsers
        run: npx playwright install --with-deps
        
      - name: Run Playwright tests
        run: npx playwright test
        
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Config for CI

```typescript
export default defineConfig({
  // Fail fast in CI
  forbidOnly: !!process.env.CI,
  
  // Retry in CI only
  retries: process.env.CI ? 2 : 0,
  
  // Single worker in CI (more stable)
  workers: process.env.CI ? 1 : undefined,
  
  // Extra artifacts in CI
  use: {
    trace: process.env.CI ? 'on-first-retry' : 'off',
    video: process.env.CI ? 'on-first-retry' : 'off',
  },
});
```
