# AI Coding Workflow Setup Guide
## Based on "My LLM coding workflow going into 2026" by Addy Osmani

> **Reference:** [Article Link](https://addyo.substack.com/p/my-llm-coding-workflow-going-into)

This guide provides an actionable checklist for incrementally improving your AI-assisted coding setup. Use it as a reference to systematically enhance your workflow over time.

---

## 🎯 Core Philosophy

- **AI-augmented software engineering** (not AI-automated)
- Treat LLM as a powerful pair programmer requiring clear direction, context, and oversight
- Stay in control and accountable for the software produced
- Apply classic software engineering discipline to AI collaborations

---

## 1. Planning & Specification Workflow

### 1.1 Specification Creation Process
- [ ] **Establish a spec-first workflow**: Always create a detailed specification before coding
- [ ] **Create a `spec.md` template** for new projects containing:
  - [ ] Requirements section
  - [ ] Architecture decisions
  - [ ] Data models
  - [ ] Testing strategy
  - [ ] Edge cases documentation
- [ ] **Practice iterative requirement gathering**: Use AI to ask questions until requirements are fleshed out
- [ ] **Compile comprehensive specs** that form the foundation for development

### 1.2 Project Planning
- [ ] **Generate project plans** using reasoning-capable models
- [ ] **Break implementation into logical, bite-sized tasks** or milestones
- [ ] **Create mini "design docs"** or project plans with AI assistance
- [ ] **Iterate on plans**: Edit and ask AI to critique/refine until coherent and complete
- [ ] **Only proceed to coding** after spec and plan are complete
- [ ] **Practice "waterfall in 15 minutes"**: Rapid structured planning phase

### 1.3 Planning Tools & Templates
- [ ] Create reusable spec templates for different project types
- [ ] Document your planning workflow for consistency
- [ ] Set up a standard location for specs (e.g., `/docs/specs/`)

---

## 2. Iterative Development & Chunking

### 2.1 Task Breakdown Strategy
- [ ] **Break projects into iterative steps or tickets** - one at a time
- [ ] **Avoid monolithic outputs**: Never ask AI for large, all-at-once code generation
- [ ] **Focus prompts**: Implement one function, fix one bug, add one feature at a time
- [ ] **Work through plan sequentially**: "Let's implement Step 1 from the plan", then Step 2, etc.
- [ ] **Test each chunk** before moving to the next

### 2.2 Chunked Workflow Implementation
- [ ] **Create structured "prompt plan" files** containing sequences of prompts for each task
- [ ] **Use tools that support chunked workflow** (e.g., Cursor can execute prompts one by one)
- [ ] **Carry forward context** incrementally as you build
- [ ] **Stop and split** if AI produces inconsistent or duplicated code
- [ ] **Practice small loops**: Greatly reduce chance of catastrophic errors

### 2.3 Test-Driven Development Integration
- [ ] **Write or generate tests for each piece** as you go
- [ ] **Test each iteration** before moving forward
- [ ] **Use TDD approach** with AI assistance

---

## 3. Context & Guidance Management

### 3.1 Context Provision Strategy
- [ ] **Feed AI all necessary information**:
  - [ ] Code it should modify or refer to
  - [ ] Project's technical constraints
  - [ ] Known pitfalls or preferred approaches
  - [ ] Relevant API documentation
- [ ] **Use modern context tools**:
  - [ ] Claude Projects mode (import entire GitHub repo)
  - [ ] IDE assistants (Cursor, Copilot) with open files
  - [ ] MCP tools like Context7
  - [ ] Manual copying of important codebase pieces or API docs

### 3.2 Context Packaging Techniques
- [ ] **Perform "brain dump"** before coding:
  - [ ] High-level goals and invariants
  - [ ] Examples of good solutions
  - [ ] Warnings about approaches to avoid
  - [ ] Reference implementations when needed
- [ ] **Provide official docs** for niche libraries or new APIs
- [ ] **Automate context packaging**:
  - [ ] Experiment with tools like `gitingest` or `repo2txt`
  - [ ] Generate `output.txt` bundles of key source files
  - [ ] Selectively include relevant code portions
  - [ ] Explicitly tell AI what NOT to focus on (to save tokens)

### 3.3 Claude Skills & Reusable Instructions
- [ ] **Explore Claude Skills** for durable, reusable instructions
- [ ] **Package instructions, scripts, and domain expertise** into modular capabilities
- [ ] **Create team knowledge workflows** that encode repeatable procedures
- [ ] **Use community-curated Skills collections** (e.g., frontend-design skill)
- [ ] **Document workarounds** until more tools support Skills officially

### 3.4 Guidance in Prompts
- [ ] **Use comments and rules inside prompts**:
  - [ ] "Here is the current implementation of X. We need to extend it to do Y, but be careful not to break Z."
- [ ] **Provide explicit warnings** about naive solutions that are too slow
- [ ] **Share reference implementations** from elsewhere when needed
- [ ] **Configure system instructions** for project-specific rules
- [ ] **Write down explicit rules** for the AI to follow

### 3.5 Code Review & Documentation
- [ ] **Review AI-generated code** before accepting
- [ ] **Ask AI to explain its code** or rationale behind fixes
- [ ] **Use AI as research assistant**: Ask for options or trade-off comparisons
- [ ] **Document changes**: "Changed X to Y to prevent Z (as per spec)"

---

## 4. Testing & Automation Infrastructure

### 4.1 CI/CD Setup
- [ ] **Establish robust continuous integration** for repositories using AI coding
- [ ] **Automated tests run on every commit or PR**
- [ ] **Code style checks enforced** (ESLint, Prettier, etc.)
- [ ] **Staging deployment available** for any new branch
- [ ] **Let AI trigger CI** and evaluate results
- [ ] **Feed failure logs back to AI**: "The integration tests failed with XYZ, let's debug this"
- [ ] **Create collaborative bug-fixing loops** with quick feedback

### 4.2 Code Quality Automation
- [ ] **Include linter output in prompts** when AI writes non-compliant code
- [ ] **Copy linter errors into chat**: "please address these issues"
- [ ] **Set up automated code quality checks**:
  - [ ] Linters
  - [ ] Type checkers
  - [ ] Formatting tools
- [ ] **Make AI aware of tool outputs** (failing tests, lint warnings)

### 4.3 AI Agent Integration
- [ ] **Use AI coding agents** that refuse to mark tasks "done" until all tests pass
- [ ] **Set up code review bots** (AI or otherwise) as additional filters
- [ ] **Treat reviewer feedback as prompts** for improvement
- [ ] **Experiment with AI-on-AI code reviews** (one model reviewing another)

### 4.4 Quality Gates
- [ ] **Bolster quality gates** around AI code contribution:
  - [ ] More tests
  - [ ] More monitoring
  - [ ] AI-on-AI code reviews
- [ ] **Create virtuous cycle**: AI writes code → automation catches issues → AI fixes → repeat
- [ ] **Ensure strong automation** to keep AI honest

---

## 5. Learning & Skill Development

### 5.1 Continuous Learning Practices
- [ ] **Treat every AI coding session as learning opportunity**
- [ ] **Review AI code** to learn new idioms and solutions
- [ ] **Debug AI mistakes** to deepen understanding
- [ ] **Ask AI to explain code** or rationale behind fixes
- [ ] **Use AI as encyclopedic mentor** for research

### 5.2 Skill Amplification
- [ ] **Strengthen software engineering fundamentals** (AI amplifies existing skills)
- [ ] **Focus on high-level skills**:
  - [ ] System design
  - [ ] Managing complexity
  - [ ] Knowing what to automate vs hand-code
- [ ] **Be more rigorous about planning**
- [ ] **Be more conscious of architecture**
- [ ] **Practice "managing" the AI** as a very fast but somewhat naïve coder

### 5.3 Balanced Practice
- [ ] **Periodically code without AI** to keep raw skills sharp
- [ ] **Avoid Dunning-Kruger effect**: Don't let AI make you think you've built something great until it falls apart
- [ ] **Continue honing craft** while using AI to accelerate
- [ ] **Stay intentional** about skill development

---

## 6. Tool & Workflow Setup

### 6.1 IDE & Editor Configuration
- [ ] **Set up AI coding assistant** (Cursor, GitHub Copilot, Claude Code, etc.)
- [ ] **Configure system instructions** for project-specific rules
- [ ] **Set up file watching** and context inclusion
- [ ] **Customize AI behavior** for your coding style

### 6.2 Version Control Integration
- [ ] **Ensure proper git workflow** with AI-generated code
- [ ] **Review all AI changes** before committing
- [ ] **Use meaningful commit messages** (document what AI changed and why)
- [ ] **Set up branch protection** if using AI agents for PRs

### 6.3 Context Management Tools
- [ ] **Explore and set up context management tools**:
  - [ ] `gitingest` or `repo2txt` for codebase dumps
  - [ ] MCP tools like Context7
  - [ ] Claude Projects mode
- [ ] **Create scripts** for automated context packaging
- [ ] **Document context requirements** for different types of tasks

### 6.4 Prompt Management
- [ ] **Create prompt templates** for common tasks
- [ ] **Document effective prompt patterns**
- [ ] **Build library of reusable prompts**
- [ ] **Version control your prompts** and templates

---

## 7. Project Structure & Organization

### 7.1 Documentation Structure
- [ ] **Create `/docs/specs/` directory** for specifications
- [ ] **Maintain project plans** in accessible location
- [ ] **Document architecture decisions**
- [ ] **Keep testing strategy documented**

### 7.2 Code Organization
- [ ] **Establish clear project structure** that AI can understand
- [ ] **Use consistent naming conventions**
- [ ] **Maintain clear module boundaries**
- [ ] **Document code organization** for AI context

### 7.3 Workflow Documentation
- [ ] **Document your AI coding workflow**
- [ ] **Create onboarding guide** for team members
- [ ] **Maintain best practices document**
- [ ] **Share learnings** with team

---

## 8. Monitoring & Quality Assurance

### 8.1 Code Review Process
- [ ] **Review all AI-generated code** before merging
- [ ] **Use automated code review tools**
- [ ] **Establish review checklist** for AI code
- [ ] **Document common AI mistakes** to watch for

### 8.2 Performance Monitoring
- [ ] **Monitor AI-generated code performance**
- [ ] **Track bug rates** in AI vs human-written code
- [ ] **Measure productivity improvements**
- [ ] **Adjust workflow** based on metrics

### 8.3 Feedback Loops
- [ ] **Create feedback mechanisms** for AI improvements
- [ ] **Document what works and what doesn't**
- [ ] **Iterate on prompt quality**
- [ ] **Refine context provision** based on results

---

## 9. Team Collaboration

### 9.1 Knowledge Sharing
- [ ] **Share effective prompts** with team
- [ ] **Document AI coding patterns** that work
- [ ] **Create shared prompt library**
- [ ] **Establish team standards** for AI usage

### 9.2 Collaboration Tools
- [ ] **Set up shared Claude Skills** or equivalent
- [ ] **Create team knowledge base** for AI workflows
- [ ] **Use collaborative tools** for prompt development
- [ ] **Establish code review practices** for AI code

---

## 10. Advanced Techniques

### 10.1 Multi-Model Strategies
- [ ] **Experiment with using multiple models** for different tasks
- [ ] **Use reasoning models** for planning
- [ ] **Use codegen models** for implementation
- [ ] **Try AI-on-AI reviews** (one model reviewing another)

### 10.2 Specialized Workflows
- [ ] **Create domain-specific workflows** (e.g., frontend, backend, data science)
- [ ] **Develop specialized prompts** for different types of tasks
- [ ] **Build reusable components** for common patterns
- [ ] **Experiment with autonomous agents** for grunt work

### 10.3 Future-Proofing
- [ ] **Stay updated on new AI coding tools**
- [ ] **Experiment with emerging paradigms**
- [ ] **Adapt workflow** as tools improve
- [ ] **Contribute to community** best practices

---

## 📝 Implementation Priority

### Phase 1: Foundation (Start Here)
1. Create spec-first workflow
2. Set up basic CI/CD
3. Configure AI coding assistant
4. Establish code review process

### Phase 2: Optimization
1. Implement chunked development workflow
2. Set up context management tools
3. Create prompt templates
4. Enhance testing infrastructure

### Phase 3: Advanced
1. Explore Claude Skills or equivalent
2. Set up multi-model strategies
3. Implement AI-on-AI reviews
4. Build specialized workflows

---

## 🎯 Success Metrics

Track your progress by measuring:
- [ ] Time saved in development
- [ ] Code quality metrics (bug rates, test coverage)
- [ ] Consistency of AI outputs
- [ ] Reduction in manual fixes needed
- [ ] Team adoption and satisfaction

---

## 📚 Additional Resources

- [ ] Read "The AI-Native Software Engineer" (mentioned in article)
- [ ] Explore community-curated Skills collections
- [ ] Join AI coding workflow discussions
- [ ] Experiment with new tools as they emerge

---

## 🔄 Regular Review

- [ ] **Monthly**: Review and update this checklist
- [ ] **Quarterly**: Assess workflow effectiveness
- [ ] **Ongoing**: Document new learnings and patterns

---

*Last updated: Based on "My LLM coding workflow going into 2026" by Addy Osmani*
*Remember: AI coding assistants are incredible force multipliers, but the human engineer remains the director of the show.*

