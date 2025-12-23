# GitHub Actions Workflow Patterns

Common workflow patterns and configurations.

## Table of Contents
1. [Job Patterns](#job-patterns)
2. [Trigger Patterns](#trigger-patterns)
3. [Environment Patterns](#environment-patterns)
4. [Deployment Patterns](#deployment-patterns)
5. [Reusable Workflows](#reusable-workflows)

---

## Job Patterns

### Sequential Jobs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

### Parallel Jobs

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  # Waits for all parallel jobs
  deploy:
    needs: [lint, test, build]
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

### Fan-Out/Fan-In

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Setup complete"

  # Fan out
  test-unit:
    needs: setup
    runs-on: ubuntu-latest
    steps: [...]

  test-integration:
    needs: setup
    runs-on: ubuntu-latest
    steps: [...]

  test-e2e:
    needs: setup
    runs-on: ubuntu-latest
    steps: [...]

  # Fan in
  report:
    needs: [test-unit, test-integration, test-e2e]
    runs-on: ubuntu-latest
    steps:
      - run: echo "All tests passed"
```

### Conditional Jobs

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env staging

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env production
```

---

## Trigger Patterns

### Push with Path Filters

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'
      - '!src/**/*.md'  # Ignore markdown
```

### Pull Request Types

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
    branches: [main]
```

### Manual Dispatch with Inputs

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      
      version:
        description: 'Version to deploy'
        required: false
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env ${{ inputs.environment }} --version ${{ inputs.version }}
```

### Scheduled Runs

```yaml
on:
  schedule:
    # Every day at midnight UTC
    - cron: '0 0 * * *'
    
    # Every Monday at 9am UTC
    - cron: '0 9 * * 1'
    
    # Every 6 hours
    - cron: '0 */6 * * *'
```

### Cross-Workflow Triggers

```yaml
# Triggered when another workflow completes
on:
  workflow_run:
    workflows: ["Build"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - run: deploy
```

---

## Environment Patterns

### Using Environments

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: deploy --env staging
        env:
          API_KEY: ${{ secrets.STAGING_API_KEY }}

  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: deploy --env production
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
```

### Environment Protection Rules

Configure in Settings > Environments:
- Required reviewers
- Wait timer
- Deployment branches

### Dynamic Environment Names

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    steps:
      - run: deploy
```

---

## Deployment Patterns

### Blue-Green Deployment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to inactive slot
        run: deploy --slot inactive
      
      - name: Health check
        run: curl --fail https://inactive.example.com/health
      
      - name: Swap slots
        run: swap-slots
```

### Canary Deployment

```yaml
jobs:
  deploy-canary:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to 10% of traffic
        run: deploy --traffic 10
      
      - name: Monitor for 10 minutes
        run: sleep 600
      
      - name: Check error rate
        run: check-error-rate --threshold 0.01
      
      - name: Full rollout
        run: deploy --traffic 100
```

### Rollback Pattern

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Backup current version
        run: backup-current-version
      
      - name: Deploy new version
        id: deploy
        run: deploy --version ${{ github.sha }}
      
      - name: Health check
        id: health
        run: curl --fail https://example.com/health
        continue-on-error: true
      
      - name: Rollback on failure
        if: steps.health.outcome == 'failure'
        run: rollback-to-backup
```

---

## Reusable Workflows

### Defining Reusable Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - run: deploy
        env:
          DEPLOY_KEY: ${{ secrets.deploy_key }}
```

### Calling Reusable Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
    secrets:
      deploy_key: ${{ secrets.STAGING_DEPLOY_KEY }}

  deploy-production:
    needs: deploy-staging
    uses: ./.github/workflows/deploy.yml
    with:
      environment: production
    secrets:
      deploy_key: ${{ secrets.PRODUCTION_DEPLOY_KEY }}
```

### Composite Actions

```yaml
# .github/actions/setup/action.yml
name: 'Setup Project'
description: 'Setup Node.js and install dependencies'

runs:
  using: 'composite'
  steps:
    - uses: actions/checkout@v4
      shell: bash
    
    - uses: actions/setup-node@v4
      with:
        node-version: 20
        cache: 'npm'
    
    - run: npm ci
      shell: bash
```

```yaml
# Usage
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/setup
      - run: npm test
```

---

## Matrix Patterns

### Basic Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

### Matrix with Include/Exclude

```yaml
strategy:
  matrix:
    node: [18, 20]
    os: [ubuntu-latest, windows-latest]
    exclude:
      - node: 18
        os: windows-latest
    include:
      - node: 22
        os: ubuntu-latest
        experimental: true
```

### Dynamic Matrix

```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          echo 'matrix=["a", "b", "c"]' >> $GITHUB_OUTPUT

  test:
    needs: prepare
    strategy:
      matrix:
        item: ${{ fromJson(needs.prepare.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing ${{ matrix.item }}"
```

---

## Security Patterns

### Minimal Permissions

```yaml
permissions:
  contents: read
  pull-requests: write

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint
```

### OIDC for Cloud Authentication

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/deploy
          aws-region: us-east-1
      
      - run: aws s3 sync dist/ s3://bucket/
```
