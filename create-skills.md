# Creating Claude Code Skills: Complete Guide

This guide provides comprehensive instructions for creating, organizing, and managing Claude Code skills in this repository. Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tools.

## Table of Contents

1. [What Are Skills?](#what-are-skills)
2. [Skill Anatomy](#skill-anatomy)
3. [Core Principles](#core-principles)
4. [Skill Structure](#skill-structure)
5. [Creating a Skill: Step-by-Step](#creating-a-skill-step-by-step)
6. [Writing SKILL.md](#writing-skillmd)
7. [Organizing Resources](#organizing-resources)
8. [Progressive Disclosure Patterns](#progressive-disclosure-patterns)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)
11. [Validation and Packaging](#validation-and-packaging)
12. [Repository Management](#repository-management)

---

## What Are Skills?

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. They transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

### When to Create a Skill

Create a skill when you need Claude to:
- Follow specific, repeatable procedures
- Work with specialized tools or file formats
- Apply domain-specific knowledge consistently
- Use company-specific templates or guidelines
- Execute complex workflows that benefit from structured guidance

---

## Skill Anatomy

Every skill consists of a required `SKILL.md` file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

---

## Core Principles

### 1. Concise is Key

**The context window is a public good.** Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Does this paragraph justify its token cost?"

**Prefer concise examples over verbose explanations.**

### 2. Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

- **High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.
- **Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.
- **Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### 3. Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words recommended)
3. **Bundled resources** - As needed by Claude (Unlimited because scripts can be executed without reading into context window)

---

## Skill Structure

### Required: SKILL.md

Every skill must have a `SKILL.md` file at the root of the skill directory.

#### YAML Frontmatter (Required)

The frontmatter must be valid YAML and contain exactly two required fields:

```yaml
---
name: skill-name
description: Comprehensive description of what the skill does and when to use it. Include both what the skill does AND specific triggers/contexts for when to use it. This is the primary triggering mechanism.
---
```

**Frontmatter Guidelines:**

- `name`: Use lowercase, hyphens for spaces (e.g., `clean-architecture-advisor`, `pdf-processor`)
- `description`: This is critical—it's the only thing Claude reads to determine when to use the skill
  - Include **what** the skill does
  - Include **when** to use it (specific triggers, contexts, file types, etc.)
  - Include **all "when to use" information here**—not in the body (the body is only loaded after triggering)
  - Example: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
- **Do not include any other fields** in YAML frontmatter

#### Markdown Body (Required)

The body contains instructions and guidance for using the skill. Only loaded AFTER the skill triggers.

**Writing Guidelines:**
- Always use **imperative/infinitive form** ("Create documents", "Extract text", "Validate input")
- Keep SKILL.md body under 500 lines to minimize context bloat
- Focus on procedural instructions and workflow guidance
- Move detailed reference material to `references/` files
- Include clear navigation to bundled resources

### Optional: Bundled Resources

#### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

**When to include:**
- When the same code is being rewritten repeatedly
- When deterministic reliability is needed
- When operations are fragile and error-prone

**Examples:**
- `scripts/rotate_pdf.py` for PDF rotation tasks
- `scripts/generate_api_client.py` for API client generation
- `scripts/format_code.py` for code formatting

**Benefits:**
- Token efficient (can be executed without loading into context)
- Deterministic and reliable
- Reusable across projects

**Note:** Scripts may still need to be read by Claude for patching or environment-specific adjustments.

**Best Practices:**
- Test all scripts before including them
- Include clear docstrings and parameter descriptions
- Make scripts idempotent when possible
- Handle errors gracefully with clear error messages

#### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

**When to include:**
- For documentation that Claude should reference while working
- For detailed schemas, APIs, or domain knowledge
- For company policies, templates, or guidelines
- For information that's too large for SKILL.md

**Examples:**
- `references/api_docs.md` for API specifications
- `references/schema.md` for database schemas
- `references/brand_guidelines.md` for company branding
- `references/workflows.md` for detailed workflow documentation

**Use cases:**
- Database schemas and relationships
- API documentation and specifications
- Domain knowledge and business rules
- Company policies and procedures
- Detailed workflow guides
- Framework-specific patterns

**Benefits:**
- Keeps SKILL.md lean
- Loaded only when Claude determines it's needed
- Enables progressive disclosure

**Best Practices:**
- If files are large (>10k words), include grep search patterns in SKILL.md
- Avoid duplication: Information should live in either SKILL.md or references files, not both
- Prefer references files for detailed information unless it's truly core to the skill
- For files longer than 100 lines, include a table of contents at the top
- Keep references one level deep from SKILL.md (all reference files should link directly from SKILL.md)

#### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

**When to include:**
- When the skill needs files that will be used in the final output
- For templates, boilerplate, or sample files
- For images, icons, fonts, or other media

**Examples:**
- `assets/logo.png` for brand assets
- `assets/template.html` for HTML templates
- `assets/frontend-template/` for React boilerplate
- `assets/font.ttf` for typography
- `assets/slides.pptx` for PowerPoint templates

**Use cases:**
- Templates and boilerplate code
- Images, icons, and media files
- Fonts and typography
- Sample documents that get copied or modified
- Configuration files

**Benefits:**
- Separates output resources from documentation
- Enables Claude to use files without loading them into context
- Maintains consistency across outputs

### What NOT to Include

A skill should only contain essential files that directly support its functionality. **Do NOT create extraneous documentation or auxiliary files**, including:

- ❌ README.md
- ❌ INSTALLATION_GUIDE.md
- ❌ QUICK_REFERENCE.md
- ❌ CHANGELOG.md
- ❌ LICENSE.txt (unless required by bundled resources)
- ❌ Any other auxiliary documentation

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxiliary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc.

---

## Creating a Skill: Step-by-Step

### Step 1: Understand the Skill with Concrete Examples

**Skip this step only when the skill's usage patterns are already clearly understood.**

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

**Questions to ask:**
- "What functionality should this skill support?"
- "Can you give some examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"
- "What are the different variations or edge cases?"

**Conclude this step when there is a clear sense of the functionality the skill should support.**

### Step 2: Plan Reusable Skill Contents

Analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

**Example analysis:**

**PDF Editor Skill:**
- Rotating a PDF requires re-writing the same code each time
- → Include `scripts/rotate_pdf.py`

**Frontend Webapp Builder Skill:**
- Writing a frontend webapp requires the same boilerplate HTML/React each time
- → Include `assets/frontend-template/` with boilerplate files

**BigQuery Skill:**
- Querying BigQuery requires re-discovering the table schemas each time
- → Include `references/schema.md` documenting table schemas

**Create a list of reusable resources to include: scripts, references, and assets.**

### Step 3: Initialize the Skill

When creating a new skill from scratch, create the directory structure:

```bash
mkdir -p skill-name/{scripts,references,assets}
touch skill-name/SKILL.md
```

**Or use a template structure:**

```
skill-name/
├── SKILL.md
├── scripts/
│   └── .gitkeep  (optional)
├── references/
│   └── .gitkeep  (optional)
└── assets/
    └── .gitkeep  (optional)
```

### Step 4: Edit the Skill

#### Start with Reusable Resources

Begin implementation with the reusable resources identified: `scripts/`, `references/`, and `assets/` files.

**For scripts:**
- Write and test the code
- Ensure it works correctly
- Add clear documentation
- Test with a representative sample if there are many similar scripts

**For references:**
- Extract detailed information from SKILL.md
- Organize by domain, framework, or use case
- Add table of contents for long files
- Ensure clear navigation from SKILL.md

**For assets:**
- Gather templates, images, or other files
- Organize in logical subdirectories if needed
- Ensure files are ready for use

**Clean up:**
- Delete any example files not needed for the skill
- Remove empty directories if not used

#### Update SKILL.md

**Frontmatter:**
```yaml
---
name: your-skill-name
description: Comprehensive description including what it does and when to use it. List specific triggers, file types, contexts, or use cases. This is the primary triggering mechanism.
---
```

**Body Structure:**
1. **Overview** - Brief introduction to the skill
2. **Core Principles** - Fundamental concepts or rules
3. **Workflows** - Step-by-step procedures
4. **Examples** - Concrete usage examples
5. **Resources** - Links to bundled resources with clear descriptions of when to use them
6. **Guidelines** - Best practices and constraints

**Writing Style:**
- Use imperative/infinitive form
- Be concise and direct
- Focus on procedural knowledge
- Link to references for detailed information
- Include concrete examples

### Step 5: Package the Skill (Optional)

If you need to distribute the skill as a `.skill` file:

1. **Validate** the skill structure
2. **Package** into a `.skill` file (which is a zip file with a `.skill` extension)

```bash
# Manual packaging
cd skill-name
zip -r ../skill-name.skill .
```

**Validation checklist:**
- ✅ YAML frontmatter format is valid
- ✅ `name` and `description` fields are present
- ✅ Description includes "what" and "when to use"
- ✅ All referenced files exist
- ✅ No extraneous documentation files
- ✅ Directory structure is correct

### Step 6: Iterate

After testing the skill, iterate based on real usage:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

---

## Writing SKILL.md

### Frontmatter Best Practices

**Good Description Example:**
```yaml
description: Experienced senior developer assistant for planning, reviewing, and refactoring React and Node.js projects using Clean Architecture principles. Use when (1) planning a new project's folder structure and layers, (2) reviewing existing code for architectural violations, (3) refactoring monolithic code toward Clean Architecture, (4) identifying Dependency Rule violations, (5) designing use cases, entities, and interfaces, or (6) setting up proper separation between frontend and backend concerns.
```

**Why it's good:**
- Clearly states what the skill does
- Lists specific triggers with numbered examples
- Covers multiple use cases
- Helps Claude understand when to activate the skill

**Bad Description Example:**
```yaml
description: Helps with architecture
```

**Why it's bad:**
- Too vague
- No triggers or use cases
- Claude won't know when to use it

### Body Structure

#### 1. Overview Section

Brief introduction that sets context:

```markdown
# Skill Name

Act as a [role] helping [primary function]. This skill provides [key capabilities].
```

#### 2. Core Principles

Fundamental concepts, rules, or constraints:

```markdown
## Core Principles

### Principle Name
**Key rule or concept**

- Important point 1
- Important point 2
```

#### 3. Workflows

Step-by-step procedures organized by use case:

```markdown
## Workflow: Use Case Name

When [trigger condition]:

1. **Step 1** → What to do
2. **Step 2** → What to do next
3. **Step 3** → Final step
```

#### 4. Examples

Concrete usage examples:

```markdown
## Examples

- Example 1: Brief description
- Example 2: Brief description
```

#### 5. Resources

Clear navigation to bundled resources:

```markdown
## Resources

- **API Documentation**: See [references/api_docs.md](references/api_docs.md) for complete API reference
- **Database Schema**: See [references/schema.md](references/schema.md) for table structures
- **Templates**: Use files in `assets/templates/` for boilerplate code
```

#### 6. Guidelines

Best practices, constraints, and response style:

```markdown
## Guidelines

- Guideline 1
- Guideline 2
- Guideline 3
```

### Writing Style Guidelines

1. **Use imperative/infinitive form:**
   - ✅ "Create documents", "Extract text", "Validate input"
   - ❌ "The skill creates documents", "You should extract text"

2. **Be concise:**
   - Prefer short, direct sentences
   - Remove unnecessary words
   - Use bullet points for lists

3. **Focus on procedural knowledge:**
   - What to do, not why (unless the why is non-obvious)
   - Step-by-step instructions
   - Concrete examples over abstract explanations

4. **Link to references:**
   - Don't duplicate detailed information
   - Use clear links with context about when to read them
   - Example: "For detailed API reference, see [references/api_docs.md](references/api_docs.md)"

---

## Organizing Resources

### Scripts Organization

**Structure:**
```
scripts/
├── process_pdf.py
├── generate_client.py
└── format_code.py
```

**Naming:**
- Use descriptive, action-oriented names
- Use snake_case for Python scripts
- Use kebab-case for other scripts if preferred

**Documentation:**
- Include docstrings with purpose and parameters
- Document expected inputs and outputs
- Include usage examples in comments if helpful

### References Organization

**Pattern 1: By Domain**
```
references/
├── finance.md
├── sales.md
├── product.md
└── marketing.md
```

**Pattern 2: By Framework/Variant**
```
references/
├── aws.md
├── gcp.md
└── azure.md
```

**Pattern 3: By Feature**
```
references/
├── api_docs.md
├── schema.md
└── workflows.md
```

**Best Practices:**
- Keep files focused (one domain, one framework, one feature)
- Include table of contents for files >100 lines
- Link directly from SKILL.md
- Avoid deeply nested references (one level deep maximum)

### Assets Organization

**Structure:**
```
assets/
├── templates/
│   ├── react-app/
│   └── node-api/
├── images/
│   └── logo.png
└── fonts/
    └── brand-font.ttf
```

**Naming:**
- Use descriptive directory names
- Keep file names clear and consistent
- Organize by type or purpose

---

## Progressive Disclosure Patterns

### Pattern 1: High-Level Guide with References

Keep core workflow in SKILL.md, move details to references:

```markdown
# PDF Processing

## Quick Start

Extract text with pdfplumber:
[code example]

## Advanced Features

- **Form filling**: See [references/FORMS.md](references/FORMS.md) for complete guide
- **API reference**: See [references/REFERENCE.md](references/REFERENCE.md) for all methods
- **Examples**: See [references/EXAMPLES.md](references/EXAMPLES.md) for common patterns
```

### Pattern 2: Domain-Specific Organization

Organize by domain to avoid loading irrelevant context:

```markdown
## Resources

- **Finance metrics**: See [references/finance.md](references/finance.md) for revenue, billing metrics
- **Sales data**: See [references/sales.md](references/sales.md) for opportunities, pipeline
- **Product analytics**: See [references/product.md](references/product.md) for API usage, features
```

### Pattern 3: Conditional Details

Show basic content, link to advanced:

```markdown
## Creating Documents

Use docx-js for new documents. See [references/DOCX-JS.md](references/DOCX-JS.md).

## Editing Documents

For simple edits, modify the XML directly.

**For tracked changes**: See [references/REDLINING.md](references/REDLINING.md)
**For OOXML details**: See [references/OOXML.md](references/OOXML.md)
```

### Pattern 4: Framework Variants

Support multiple frameworks without bloating SKILL.md:

```markdown
## Deployment

Choose your cloud provider:

- **AWS**: See [references/aws.md](references/aws.md) for AWS deployment patterns
- **GCP**: See [references/gcp.md](references/gcp.md) for GCP deployment patterns
- **Azure**: See [references/azure.md](references/azure.md) for Azure deployment patterns
```

**Key Guidelines:**
- Keep SKILL.md under 500 lines
- Split content when approaching this limit
- Reference files directly from SKILL.md
- Describe clearly when to read each reference
- Avoid deeply nested references (one level deep)

---

## Best Practices

### Description Writing

✅ **Do:**
- Include both "what" and "when to use"
- List specific triggers, file types, or contexts
- Use numbered examples for clarity
- Be comprehensive but concise

❌ **Don't:**
- Write vague descriptions
- Put "when to use" information only in the body
- Assume Claude will infer use cases

### Content Organization

✅ **Do:**
- Keep SKILL.md focused on procedural instructions
- Move detailed reference material to `references/`
- Use progressive disclosure
- Link clearly to bundled resources

❌ **Don't:**
- Duplicate information between SKILL.md and references
- Include everything in SKILL.md
- Create deeply nested reference structures
- Include extraneous documentation files

### Resource Management

✅ **Do:**
- Test all scripts before including
- Organize references by domain/framework/feature
- Use clear, descriptive file names
- Include table of contents for long reference files

❌ **Don't:**
- Include untested scripts
- Create overly complex directory structures
- Duplicate assets unnecessarily
- Include files not directly used by the skill

### Writing Style

✅ **Do:**
- Use imperative/infinitive form
- Be concise and direct
- Focus on procedural knowledge
- Include concrete examples

❌ **Don't:**
- Use passive voice
- Include verbose explanations
- Duplicate what Claude already knows
- Write abstract descriptions

---

## Common Patterns

### Pattern 1: File Format Handler

**Structure:**
```
file-format-skill/
├── SKILL.md
├── scripts/
│   ├── read_format.py
│   ├── write_format.py
│   └── convert_format.py
└── references/
    └── format_spec.md
```

**SKILL.md sections:**
- Overview of format
- Reading files
- Writing files
- Conversion workflows
- References to format specification

### Pattern 2: Framework Advisor

**Structure:**
```
framework-advisor/
├── SKILL.md
└── references/
    ├── patterns.md
    ├── best_practices.md
    └── common_issues.md
```

**SKILL.md sections:**
- Core principles
- Project structure
- Common workflows
- Links to patterns and best practices

### Pattern 3: Code Generator

**Structure:**
```
code-generator/
├── SKILL.md
├── scripts/
│   └── generate.py
└── assets/
    └── templates/
        ├── component.tsx
        └── api-route.ts
```

**SKILL.md sections:**
- Generation workflow
- Template usage
- Customization options
- Examples

### Pattern 4: Domain Expert

**Structure:**
```
domain-expert/
├── SKILL.md
└── references/
    ├── domain_concepts.md
    ├── schemas.md
    └── workflows.md
```

**SKILL.md sections:**
- Domain overview
- Core concepts
- Common tasks
- Links to detailed references

---

## Validation and Packaging

### Validation Checklist

Before packaging or committing a skill, validate:

- [ ] YAML frontmatter is valid
- [ ] `name` field is present and uses kebab-case
- [ ] `description` field is present and comprehensive
- [ ] Description includes "what" and "when to use"
- [ ] All files referenced in SKILL.md exist
- [ ] No extraneous documentation files (README, CHANGELOG, etc.)
- [ ] Directory structure is correct
- [ ] Scripts are tested and working
- [ ] Reference files are properly linked
- [ ] SKILL.md body is under 500 lines (or justified if longer)

### Packaging

To create a distributable `.skill` file:

```bash
# Navigate to skill directory
cd skill-name

# Create zip file with .skill extension
zip -r ../skill-name.skill .

# Or use a script if available
scripts/package_skill.py skill-name
```

The `.skill` file is a zip archive with a `.skill` extension that maintains the directory structure.

---

## Repository Management

### Repository Structure

Organize skills in this repository:

```
ai-coding-tools/
├── skills/
│   ├── skill-name-1/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   ├── skill-name-2/
│   │   └── ...
│   └── ...
├── create-skills.md (this file)
└── README.md
```

### Naming Conventions

- **Skill directories**: Use kebab-case (e.g., `clean-architecture-advisor`)
- **Skill names**: Match directory name in frontmatter
- **Script files**: Use snake_case for Python, kebab-case for others
- **Reference files**: Use kebab-case with descriptive names

### Version Control

- Commit each skill as a complete unit
- Include clear commit messages describing the skill
- Tag releases if distributing skills externally
- Keep skills independent (no cross-skill dependencies)

### Documentation

- This `create-skills.md` serves as the master guide
- Each skill is self-contained and doesn't need separate documentation
- README.md can provide repository overview and skill index

### Skill Index

Consider maintaining a skill index in README.md:

```markdown
## Available Skills

- **clean-architecture-advisor** - Planning and reviewing React/Node.js projects with Clean Architecture
- **skill-name-2** - Description
- **skill-name-3** - Description
```

---

## Quick Reference

### Minimal Skill Structure

```
skill-name/
└── SKILL.md
```

**Minimal SKILL.md:**
```yaml
---
name: skill-name
description: What it does. Use when [specific triggers].
---

# Skill Name

[Instructions here]
```

### Complete Skill Structure

```
skill-name/
├── SKILL.md
├── scripts/
│   └── process.py
├── references/
│   └── docs.md
└── assets/
    └── template.html
```

### Description Template

```yaml
description: [What the skill does]. Use when [specific trigger 1], [specific trigger 2], [specific trigger 3], or [other use cases].
```

### SKILL.md Template

```markdown
---
name: skill-name
description: [Comprehensive description with triggers]
---

# Skill Name

[Brief overview]

## Core Principles

[Fundamental concepts]

## Workflows

[Step-by-step procedures]

## Resources

- **Reference**: See [references/file.md](references/file.md) for [purpose]
- **Scripts**: Use `scripts/script.py` for [purpose]
- **Assets**: Use files in `assets/` for [purpose]

## Examples

[Concrete examples]

## Guidelines

[Best practices and constraints]
```

---

## Additional Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Agent Skills Specification](https://agentskills.io)
- [How to Create Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

---

## Summary

Creating effective skills requires:

1. **Clear understanding** of use cases and triggers
2. **Comprehensive description** in frontmatter (what + when)
3. **Concise instructions** in SKILL.md body
4. **Progressive disclosure** using references and assets
5. **Tested resources** (scripts, references, assets)
6. **Iterative improvement** based on real usage

Remember: Skills extend Claude's capabilities with specialized knowledge. Keep them focused, well-organized, and efficient with context usage.

