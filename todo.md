# Agentic Readiness Skills Roadmap

This document lists the agents/skills needed to help developers set up each element of agentic readiness for their codebases. Each skill will be an expert in a specific area of the AI-assisted development workflow.

## Current Skills Inventory

| Skill | Focus Area |
|-------|------------|
| agentic-readiness-advisor | Analyzes codebases and identifies gaps |
| clean-architecture-advisor | Project structure and dependency rules |
| code-quality-enforcer | ESLint rules, Husky, lint-staged |
| component-testing-expert | React component testing with Testing Library |
| github-actions-architect | CI/CD workflows and automation |
| playwright-expert | E2E testing |
| project-orchestrator | PRD creation and task management |
| react-state-expert | State management patterns |
| test-mocking-specialist | MSW, mocking strategies |
| vitest-expert | Unit testing |

---

## Skills to Build

### Priority 1: Critical Gaps

#### 1. ai-context-architect
**Expert at:** Creating and maintaining AI context files that help AI agents understand codebases

- Writing effective `CLAUDE.md`, `AGENTS.md`, `CURSOR_RULES.md` files
- Structuring context files for different project types
- Documenting project constraints, patterns, and anti-patterns
- Writing "why" comments in code that guide AI understanding
- Context packaging techniques (what to include, what to exclude)
- Documenting data models and schemas for AI comprehension
- Creating architecture overviews that AI can navigate
- Maintaining context files as projects evolve

---

#### 2. spec-writing-advisor
**Expert at:** Creating specifications and planning documents before coding

- Writing feature specifications that guide AI implementation
- Creating `spec.md` templates for different feature types
- Documenting requirements with acceptance criteria
- Iterative requirement gathering using AI assistance
- Writing edge cases and error scenarios
- Creating Architecture Decision Records (ADRs)
- Documenting data models and API contracts in specs
- Linking specs to implementation tasks

---

#### 3. tdd-chunking-advisor
**Expert at:** Breaking work into AI-friendly chunks with test-driven development

- Breaking features into iterative, testable steps
- Writing tests before implementation with AI assistance
- Creating "prompt plans" - sequences of prompts for features
- Designing interfaces and contracts before implementation
- Managing context across chunked development sessions
- When to stop and split if AI produces inconsistent code
- Carrying forward context incrementally
- Verifying each chunk before moving forward

---

#### 4. code-prompt-engineer
**Expert at:** Writing effective prompts for code generation and modification

- Prompt templates for common coding tasks
- Providing context effectively in prompts
- Warning AI about approaches to avoid
- Sharing reference implementations in prompts
- Iterating on prompts when output isn't right
- Task-specific prompt patterns (bug fix, feature, refactor)
- Including constraints and rules in prompts
- Multi-step prompt workflows

---

### Priority 2: Important Enhancements

#### 5. ai-code-reviewer
**Expert at:** Reviewing AI-generated code and establishing review processes

- What to look for in AI-generated code
- Common AI coding mistakes and how to spot them
- Establishing review checklists for AI code
- AI-on-AI code review patterns (one model reviewing another)
- Asking AI to explain its code and rationale
- Treating reviewer feedback as prompts for improvement
- Code review bots and automated review
- Documenting common AI mistakes to watch for

---

#### 6. typescript-strictness-expert
**Expert at:** TypeScript configuration and type safety for AI-friendly code

- Configuring strict TypeScript settings
- Type-safe patterns that help AI understand code
- Discriminated unions and type narrowing
- Branded types for domain modeling
- Error handling with typed errors
- Generic patterns that AI can follow
- Avoiding `any` and `unknown` misuse
- Type guards and assertion functions

---

#### 7. git-workflow-advisor
**Expert at:** Version control workflows optimized for AI-assisted development

- Branch protection rules for AI agent PRs
- Meaningful commit messages for AI changes
- PR templates that document AI involvement
- Review processes for AI-generated PRs
- Git hooks that work with AI coding
- Managing AI-generated changesets
- Rollback strategies for AI changes
- Commit organization for AI sessions

---

#### 8. api-documentation-expert
**Expert at:** Creating API documentation that AI agents can use effectively

- OpenAPI/Swagger specification writing
- API endpoint documentation patterns
- Request/response schema documentation
- Error code documentation
- Authentication documentation
- Example requests and responses
- API versioning documentation
- GraphQL schema documentation

---

### Priority 3: Advanced Capabilities

#### 9. ci-feedback-optimizer
**Expert at:** Optimizing CI/CD for fast AI feedback loops

- Making CI failure logs actionable for AI
- Creating virtuous cycles: AI writes → CI catches → AI fixes
- Feeding test failures back to AI effectively
- Clear error messages that AI can interpret
- Staging deployments for AI-generated branches
- Quality gates that work with AI coding
- Monitoring AI code in production
- Automated rollback triggers

---

#### 10. team-ai-collaboration-advisor
**Expert at:** Team practices for AI-assisted development

- Sharing effective prompts across team
- Creating shared prompt libraries
- Team standards for AI usage
- Knowledge sharing workflows
- Onboarding team members to AI coding
- Documenting AI coding patterns that work
- Collaborative AI coding sessions
- Code ownership with AI contributions

---

#### 11. context-packaging-automator
**Expert at:** Automating context packaging for AI tools

- Using tools like `gitingest` and `repo2txt`
- Creating scripts for automated context packaging
- Selectively including relevant code portions
- Generating codebase bundles for AI context
- MCP tools and Claude Projects integration
- What to explicitly exclude from context
- Context size optimization
- Dynamic context based on task type

---

#### 12. learning-feedback-advisor
**Expert at:** Using AI coding sessions for continuous learning

- Reviewing AI code to learn new idioms
- Debugging AI mistakes to deepen understanding
- Using AI as encyclopedic mentor
- Avoiding over-reliance (Dunning-Kruger with AI)
- Periodically coding without AI
- Strengthening fundamentals through AI use
- Documentation of learnings from AI sessions
- Skill amplification strategies

---

## Coverage Matrix

How these skills map to the agentic-readiness-advisor assessment categories:

| Assessment Category | Skills Covering It |
|--------------------|-------------------|
| Planning & Specs | spec-writing-advisor, project-orchestrator |
| Context & Documentation | ai-context-architect, api-documentation-expert |
| Project Structure | clean-architecture-advisor |
| Testing Infrastructure | vitest-expert, component-testing-expert, playwright-expert, test-mocking-specialist, tdd-chunking-advisor |
| CI/CD & Automation | github-actions-architect, code-quality-enforcer, ci-feedback-optimizer |
| Code Quality | code-quality-enforcer, typescript-strictness-expert, ai-code-reviewer |
| Dev Workflow | git-workflow-advisor, team-ai-collaboration-advisor |

---

## Implementation Order

### Phase 1: Foundation (Build First)
1. ai-context-architect - Most critical gap
2. spec-writing-advisor - Planning before coding
3. tdd-chunking-advisor - Core workflow improvement

### Phase 2: Quality (Build Second)
4. code-prompt-engineer - Better AI interactions
5. ai-code-reviewer - Verify AI output
6. typescript-strictness-expert - Type safety

### Phase 3: Workflow (Build Third)
7. git-workflow-advisor - Version control
8. api-documentation-expert - API context
9. ci-feedback-optimizer - Faster feedback

### Phase 4: Team & Advanced (Build Last)
10. team-ai-collaboration-advisor - Team practices
11. context-packaging-automator - Automation
12. learning-feedback-advisor - Continuous improvement

---

## Notes

- Each skill should follow the pattern established in `create-skills.md`
- Skills should have a SKILL.md with YAML frontmatter (name, description)
- Include references/ directory for detailed guidance
- Keep SKILL.md under 500 lines, use references for detail
- Skills should be actionable, not just informational
- Focus on "how to implement" not just "what is good"
