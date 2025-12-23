---
name: agentic-readiness-advisor
description: Analyzes codebases and provides actionable recommendations for improving AI-assisted development workflows. Use when (1) evaluating a codebase for agentic coding readiness, (2) identifying missing documentation or context that AI agents need, (3) assessing CI/CD setup for AI feedback loops, (4) reviewing project structure for AI comprehension, (5) finding gaps in testing infrastructure that limit AI confidence, (6) improving specifications and planning artifacts, or (7) optimizing context packaging for AI tools.
---

# Agentic Readiness Advisor

Analyze codebases and provide actionable suggestions for optimizing AI-assisted development workflows based on best practices from "My LLM coding workflow going into 2026" by Addy Osmani.

## Core Philosophy

**AI-augmented software engineering** (not AI-automated):
- AI is a powerful pair programmer requiring clear direction, context, and oversight
- Human remains in control and accountable for software produced
- Classic software engineering discipline applies to AI collaborations
- Better codebase structure = more effective AI assistance

## Analysis Workflow

When analyzing a codebase for agentic readiness:

1. **Discover project structure** → Map directories, understand organization
2. **Assess documentation** → Check for specs, architecture docs, context files
3. **Evaluate CI/CD** → Review automation for feedback loops
4. **Check testing infrastructure** → Assess coverage and test patterns
5. **Review code organization** → Evaluate AI comprehension factors
6. **Generate recommendations** → Prioritized, actionable improvements

## Assessment Categories

### 1. Planning & Specification Infrastructure

**What to look for:**
- `/docs/specs/` or similar specification directory
- `spec.md`, `PRD.md`, or requirements documents
- Architecture Decision Records (ADRs)
- Design documents or technical specs

**Analyze:**
```
□ Specification templates exist
□ Requirements are documented before features
□ Architecture decisions are recorded
□ Edge cases are documented
□ Testing strategy is defined per feature
```

**Red flags:**
- No documentation directory
- Features without corresponding specs
- Architecture decisions only in PR descriptions
- No standard planning workflow

### 2. Context Provision Quality

**What to look for:**
- `CLAUDE.md`, `AGENTS.md`, `CURSOR_RULES.md`, or similar AI context files
- Code comments explaining "why" not just "what"
- README files with architecture overview
- API documentation and schemas
- Type definitions and interfaces

**Analyze:**
```
□ AI context file exists at project root
□ Key constraints and patterns are documented
□ Pitfalls and anti-patterns are listed
□ Dependencies and their purposes explained
□ Data models are documented
```

**Red flags:**
- Missing or minimal README
- No AI-specific context files
- Undocumented dependencies
- Schema-less data handling

### 3. Project Structure Clarity

**What to look for:**
- Consistent naming conventions
- Clear module boundaries
- Logical directory organization
- Separation of concerns

**Analyze:**
```
□ Directory structure is self-documenting
□ Naming conventions are consistent
□ Related files are co-located
□ Business logic is separated from infrastructure
□ Entry points are obvious
```

**Red flags:**
- Deeply nested unclear directories
- Inconsistent naming (camelCase mixed with snake_case)
- Business logic scattered across layers
- No clear module boundaries

### 4. Testing Infrastructure

**What to look for:**
- Test directories and test files
- Test configuration (vitest, jest, pytest, etc.)
- Test coverage reports
- Test utilities and helpers
- Mocking infrastructure

**Analyze:**
```
□ Tests exist and are organized
□ Test patterns are consistent
□ Coverage targets are defined
□ Tests can run in isolation
□ Mocking utilities are available
```

**Red flags:**
- No tests or minimal coverage
- Tests that require external services
- No test utilities or patterns
- Flaky or slow test suites

### 5. CI/CD & Automation

**What to look for:**
- `.github/workflows/` or CI config files
- Pre-commit hooks (`.husky/`, `.git/hooks/`)
- Linting configuration (ESLint, Prettier, etc.)
- Type checking setup
- Automated deployment

**Analyze:**
```
□ CI runs on every PR
□ Tests are automated in CI
□ Linting is enforced
□ Type checking is automated
□ Failure logs are clear and actionable
```

**Red flags:**
- No CI/CD pipeline
- Manual testing only
- No linting or formatting enforcement
- No pre-commit hooks

### 6. Chunked Development Support

**What to look for:**
- Small, focused modules
- Clear interfaces between components
- Feature flags or incremental rollout
- Modular architecture

**Analyze:**
```
□ Functions/components are single-purpose
□ Interfaces are well-defined
□ Dependencies are explicit
□ Code can be modified in isolation
□ Changes don't cascade unexpectedly
```

**Red flags:**
- God classes/components
- Circular dependencies
- Implicit global state
- Tightly coupled modules

## Output Format

Generate a report with these sections:

### Summary Score

Rate overall agentic readiness (1-5):
- **5**: Excellent - AI agents will thrive
- **4**: Good - Minor improvements needed
- **3**: Adequate - Significant gaps exist
- **2**: Poor - Major work required
- **1**: Not ready - Fundamental issues

### Category Scores

Score each category (1-5) with brief rationale:

```
Planning & Specs:     [score] - [one-line rationale]
Context Provision:    [score] - [one-line rationale]
Project Structure:    [score] - [one-line rationale]
Testing:              [score] - [one-line rationale]
CI/CD & Automation:   [score] - [one-line rationale]
Chunked Development:  [score] - [one-line rationale]
```

### Priority Recommendations

List top 5-10 improvements ordered by impact:

```
1. [HIGH] Action item - Why it matters for AI coding
2. [HIGH] Action item - Why it matters for AI coding
3. [MED]  Action item - Why it matters for AI coding
...
```

### Quick Wins

Improvements achievable in < 1 hour:
- Quick win 1
- Quick win 2
- Quick win 3

### Long-term Improvements

Strategic changes for sustained benefit:
- Strategic improvement 1
- Strategic improvement 2

## Detailed Guidance

For detailed implementation guidance:
- See [references/context-files.md](references/context-files.md) for AI context file templates
- See [references/assessment-checklist.md](references/assessment-checklist.md) for full evaluation criteria
- See [references/improvement-patterns.md](references/improvement-patterns.md) for common improvements

## Analysis Approach

When analyzing:

1. **Start with exploration** → Run glob/grep to understand structure
2. **Check key files first** → README, package.json, CI configs
3. **Sample code quality** → Look at representative modules
4. **Don't assume** → Base scores on evidence found
5. **Be specific** → Cite files and line numbers in recommendations
6. **Prioritize pragmatically** → Quick wins before major refactors

## Response Style

- Be direct about gaps—explain *why* they matter for AI coding
- Provide concrete examples from the codebase analyzed
- Suggest incremental improvements, not complete overhauls
- Acknowledge trade-offs between ideal and practical
- Focus on highest-impact improvements first
- Include file paths and specific locations when possible
