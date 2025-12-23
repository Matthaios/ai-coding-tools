---
name: github-actions-architect
description: Expert advisor for designing CI/CD workflows with GitHub Actions. Use when (1) creating new workflow files from scratch, (2) optimizing build times with caching, (3) parallelizing jobs for faster feedback, (4) setting up branch protection rules, (5) generating and storing artifacts like coverage reports, (6) debugging failing workflows, (7) configuring npm ci vs npm install, (8) setting up test matrix strategies, or (9) automating deployments.
---

# GitHub Actions Architect

Expert guidance for designing efficient, maintainable CI/CD workflows with GitHub Actions.

## Core Principles

### 1. Automation Over Manual Review

Let systems enforce rules so humans don't have to be the bad guy. Tests, linting, and builds should catch problems automatically.

### 2. Fast Feedback Loops

Optimize for speed. Developers should know if their PR is good within minutes, not hours.

### 3. Fail Fast, Fail Clearly

When something fails, it should be obvious what and why. Separate concerns into distinct jobs.

## Workflow Anatomy

```yaml
# .github/workflows/ci.yml
name: CI                        # Workflow name (shows in UI)

on:                             # Triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                           # One or more jobs
  test:                         # Job ID
    runs-on: ubuntu-latest      # Runner OS
    steps:                      # Sequential steps
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
```

## Essential Patterns

### Basic Test Workflow

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'           # Built-in npm caching
      
      - run: npm ci              # Clean install from lockfile
      - run: npm test
```

### Parallel Jobs (Faster Feedback)

Split jobs so you can see what failed at a glance:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm test

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run build
```

### npm ci vs npm install

| Command | Use Case |
|---------|----------|
| `npm ci` | CI/CD - clean install from package-lock.json |
| `npm install` | Development - may update lockfile |

```yaml
# GOOD: npm ci for CI
- run: npm ci

# BAD: npm install can cause inconsistencies
- run: npm install
```

## Caching

### Built-in Node Caching

The simplest approach - use the `cache` option:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'      # Also supports 'yarn', 'pnpm'
```

### Manual Cache (More Control)

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      npm-${{ runner.os }}-
```

### What to Cache

| Cache | Don't Cache |
|-------|-------------|
| `~/.npm` (npm cache) | `node_modules` (npm ci deletes it) |
| `~/.pnpm-store` | Build outputs |
| `~/.cache/Cypress` | Temporary files |
| Playwright browsers | |

### Cache Key Strategy

```yaml
# Best: Hash of lockfile (changes when deps change)
key: npm-${{ hashFiles('**/package-lock.json') }}

# With OS (for native dependencies)
key: npm-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}

# Fallback keys (partial cache hit)
restore-keys: |
  npm-${{ runner.os }}-
  npm-
```

## Artifacts

Store files from builds for later download or use.

### Upload Coverage Report

```yaml
- run: npm test -- --coverage

- uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: coverage/
    retention-days: 30
```

### Upload Build Output

```yaml
- run: npm run build

- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/
```

### Download Artifact in Later Job

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/
      - run: deploy dist/
```

## Branch Protection

Require checks to pass before merging:

1. Go to **Settings > Branches > Branch protection rules**
2. Add rule for `main`
3. Enable **Require status checks to pass**
4. Select your workflow jobs

```yaml
# Jobs must pass for the PR to be mergeable
jobs:
  test:      # <- Select this in branch protection
  lint:      # <- And this
  build:     # <- And this
```

## Matrix Strategies

Test across multiple configurations:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
      fail-fast: false           # Don't cancel other runs on failure
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Multi-OS Matrix

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]

runs-on: ${{ matrix.os }}
```

### Include/Exclude

```yaml
strategy:
  matrix:
    node-version: [18, 20]
    os: [ubuntu-latest, windows-latest]
    exclude:
      - node-version: 18
        os: windows-latest       # Skip Node 18 on Windows
    include:
      - node-version: 22
        os: ubuntu-latest        # Add Node 22 on Ubuntu only
```

## Job Dependencies

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    steps: [...]

  build:
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: [lint, test, build]   # Wait for all three
    runs-on: ubuntu-latest
    steps: [...]
```

## Conditional Execution

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps: [...]

  test:
    steps:
      - run: npm run e2e
        if: github.event_name == 'pull_request'
```

## Environment Variables and Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: production
    
    steps:
      - run: npm run deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DEPLOY_URL: ${{ vars.DEPLOY_URL }}
```

### Setting Secrets

1. Go to **Settings > Secrets and variables > Actions**
2. Add repository secrets
3. Reference with `${{ secrets.SECRET_NAME }}`

## Triggers

### Common Triggers

```yaml
on:
  # Push to specific branches
  push:
    branches: [main, develop]
    paths:
      - 'src/**'               # Only when src changes
      - '!src/**/*.md'         # Except markdown
  
  # Pull requests
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
  
  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]
  
  # Scheduled
  schedule:
    - cron: '0 0 * * *'        # Daily at midnight UTC
```

## Complete Example

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: 'npm' }
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: [lint, typecheck, test, build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/
      - run: echo "Deploy dist/ here"
```

## Resources

- **Workflow Patterns**: See [references/workflow-patterns.md](references/workflow-patterns.md) for more examples
- **Caching Strategies**: See [references/caching-strategies.md](references/caching-strategies.md) for optimization

## Response Guidelines

When answering workflow questions:

1. **Check caching** - Is npm cache enabled?
2. **Check npm ci** - Using npm ci, not npm install?
3. **Suggest parallelization** - Can jobs run in parallel?
4. **Check artifacts** - Are important outputs preserved?
5. **Suggest branch protection** - Are checks required for merge?
