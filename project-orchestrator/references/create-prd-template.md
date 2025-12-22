# PRD Creation Template

This template guides the creation of Product Requirement Documents (PRDs) for features and changes.

## PRD Structure

### 1. Title and Overview
- **Feature Name**: Clear, descriptive name
- **PRD ID**: Unique identifier (e.g., `AUTH`, `PAYMENT`)
- **Date Created**: Creation date
- **Status**: Draft, Review, Approved, In Progress, Complete
- **Overview**: 2-3 sentence summary of what this feature does

### 2. Problem Statement
- **What problem does this solve?**
- **Why is this needed now?**
- **What happens if we don't build this?**

### 3. Target Users
- **Primary Users**: Who will use this feature?
- **User Personas**: Specific user types or roles
- **User Stories**: "As a [user], I want [goal] so that [benefit]"

### 4. Requirements

#### Functional Requirements
- **Must Have**: Core functionality that must be implemented
- **Should Have**: Important but not critical features
- **Nice to Have**: Enhancements that can be added later

#### Non-Functional Requirements
- **Performance**: Response times, throughput, scalability
- **Security**: Authentication, authorization, data protection
- **Usability**: User experience, accessibility, mobile support
- **Reliability**: Uptime, error handling, recovery
- **Compatibility**: Browser support, device support, API versions

### 5. Success Criteria
- **How will we know this is successful?**
- **Metrics**: KPIs, user engagement, performance targets
- **Acceptance Criteria**: Specific conditions that must be met

### 6. Dependencies and Constraints
- **Technical Dependencies**: APIs, services, libraries
- **Business Dependencies**: Other features, teams, approvals
- **Constraints**: Time, budget, technical limitations
- **Risks**: Potential blockers or issues

### 7. Out of Scope
- **What explicitly will NOT be included?**
- **Future Considerations**: Features deferred to later phases

### 8. Design and Technical Notes
- **UI/UX Considerations**: Design requirements, mockups
- **Technical Approach**: Architecture, patterns, technologies
- **Integration Points**: APIs, services, databases

## PRD Creation Process

### Step 1: Gather Information
Ask the user:
1. What feature or change needs to be built?
2. Who is the target user/audience?
3. What problem does this solve?
4. What are the key requirements?
5. Are there any constraints or dependencies?
6. What defines success for this feature?

### Step 2: Reference Existing Codebase
- Examine relevant files mentioned by user
- Understand current architecture and patterns
- Identify integration points
- Note existing similar features

### Step 3: Structure the PRD
- Fill in each section systematically
- Be specific and actionable
- Include concrete examples
- Reference existing code when relevant

### Step 4: Review and Refine
- Ensure all sections are complete
- Verify requirements are clear and testable
- Check for consistency
- Confirm success criteria are measurable

## Example PRD Sections

### Example: User Authentication Feature

**Title**: User Authentication System
**PRD ID**: AUTH
**Overview**: Implement secure user authentication allowing users to register, login, and manage their accounts.

**Problem Statement**:
Users currently cannot create accounts or access personalized features. We need a secure authentication system to enable user-specific functionality.

**Target Users**:
- New users wanting to create accounts
- Existing users needing to log in
- Administrators managing user accounts

**Functional Requirements**:
- User registration with email and password
- Email verification
- Login with email/password
- Password reset functionality
- Session management
- Logout

**Success Criteria**:
- Users can successfully register and verify email
- Login success rate > 95%
- Password reset emails delivered within 2 minutes
- Zero security vulnerabilities in authentication flow

## Best Practices

1. **Be Specific**: Avoid vague requirements. Use concrete examples.
2. **Think User-First**: Focus on user needs and outcomes.
3. **Consider Edge Cases**: What happens when things go wrong?
4. **Define Success**: How will we measure success?
5. **Document Decisions**: Explain why certain choices were made.
6. **Keep It Updated**: PRDs are living documents. Update as requirements evolve.

