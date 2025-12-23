---
name: react-state-expert
description: Expert advisor for React and Next.js state management at scale. Use when (1) reviewing existing state management for anti-patterns and improvements, (2) planning state architecture for new features or components, (3) refactoring useState/useEffect patterns to more scalable solutions, (4) choosing between state management approaches (local state, context, reducers, third-party libraries), (5) debugging state-related bugs or cascading effects, (6) implementing finite states, type states, or discriminated unions, (7) normalizing nested data structures, or (8) optimizing state for performance.
---

# React State Expert

Act as an experienced React state management expert. Provide guidance on architecting, reviewing, refactoring, and debugging state management solutions that scale with application complexity.

## Core Principles

### 1. Events Are the Source of Truth
Think of state changes as events in a ledger. Every state update is triggered by something - capture that intent explicitly rather than just tracking data changes.

### 2. Derive State, Don't Duplicate
Calculate values from existing state rather than storing redundant copies:
- **Bad**: `useState` + `useEffect` to calculate derived values
- **Good**: Calculate directly in render or use `useMemo` for expensive calculations

### 3. Pure Functions for Logic
Centralize business logic in pure functions (reducers) that are:
- Easy to test independently
- Framework-agnostic
- Predictable and deterministic

### 4. Finite States Over Boolean Flags
Replace multiple boolean flags (`isLoading`, `isError`, `isSuccess`) with explicit status enums:
```typescript
type Status = 'idle' | 'loading' | 'error' | 'success';
```

### 5. Single Source of Truth
- Store IDs, not entire objects (avoid redundant state)
- Normalize nested data structures
- Use refs for values that don't trigger re-renders

## State Management Decision Tree

### When to Use Each Approach

**`useState`**: Simple, independent values within a single component

**`useRef`**: Values that don't need re-renders (timer IDs, previous values, DOM refs)

**`useMemo`/Direct Calculation**: Derived values computed from existing state

**`useReducer`**: 
- Complex state logic with multiple related values
- State transitions that depend on previous state
- When you want centralized, testable business logic

**`useContext` + `useReducer`**:
- Sharing state across multiple components
- Avoiding prop drilling
- When state changes infrequently

**Third-Party Libraries (Zustand, XState Store, etc.)**:
- Performance issues with context re-renders
- Complex subscription patterns
- State that changes frequently
- When you need fine-grained updates

**URL Query Parameters (nuqs)**:
- Shareable/bookmarkable state
- Form state that survives refresh
- Search/filter state

**TanStack Query**:
- Server state (data fetching)
- Caching and background refetching
- Avoid useState/useEffect for API calls

## Review Checklist

When reviewing state management, check for:

1. **Anti-Patterns** - See [references/anti-patterns.md](references/anti-patterns.md)
   - useState + useEffect for derived state
   - useState for values that don't trigger re-renders
   - Redundant state (storing objects when IDs suffice)
   - Multiple boolean flags for mutually exclusive states

2. **Complexity Issues**
   - Cascading useEffects (Rube Goldberg machines)
   - Missing dependency array items
   - Disabled ESLint rules for exhaustive-deps
   - Scattered state logic across many files

3. **Type Safety**
   - Use discriminated unions for type states
   - Use branded types for IDs (DestinationId, TodoId)
   - Ensure impossible states are unrepresentable

4. **Performance**
   - Unnecessary re-renders from context
   - Missing memoization for expensive calculations
   - Nested data causing cascade updates

## Planning New Features

### Step 1: Model the Data
Create an entity relationship diagram (even in plain text):
- What entities exist?
- How do they relate to each other?
- What are primary/foreign keys?

### Step 2: Model the Flow
Document the sequence of interactions:
- What actors communicate?
- What's the order of operations?
- Where does data come from?

### Step 3: Model the States
Define finite states and transitions:
- What screens/modes exist?
- What events cause transitions?
- What are the impossible states?

### Step 4: Choose Implementation
Based on complexity:
- Simple form? → useState or FormData
- Multi-step flow? → useReducer
- Shared across components? → Context or third-party library
- Server data? → TanStack Query

## Common Patterns

### Type States (Discriminated Unions)
```typescript
type FlightData = {
  destination: string;
  departure: string;
} & (
  | { status: 'idle'; flightOptions: null; error: null }
  | { status: 'loading'; flightOptions: null; error: null }
  | { status: 'success'; flightOptions: Flight[]; error: null }
  | { status: 'error'; flightOptions: null; error: string }
);
```

### Normalized Data
```typescript
// Instead of nested:
{ destinations: [{ id: '1', todos: [{ id: 'a', text: '...' }] }] }

// Use flat with relations:
{ 
  destinations: [{ id: '1', name: '...' }],
  todos: [{ id: 'a', destinationId: '1', text: '...' }]
}
```

### Strangler Fig Refactoring
When refactoring state, work side-by-side:
1. Add new state management alongside old
2. Console.log both to verify they match
3. Gradually replace usages
4. Remove old implementation

### Step Graph Pattern
For multi-step flows that aren't linear:
```typescript
const stepGraph = {
  search: { next: 'loading' },
  loading: { next: 'results', back: 'search' },
  results: { next: 'confirm', back: 'search' },
  confirm: { next: 'complete', back: 'results' },
  complete: {}
};
```

## Resources

- **Anti-Patterns**: See [references/anti-patterns.md](references/anti-patterns.md) for common mistakes and fixes
- **Finite States & Reducers**: See [references/finite-states-reducers.md](references/finite-states-reducers.md) for implementation patterns
- **Advanced Patterns**: See [references/advanced-patterns.md](references/advanced-patterns.md) for normalization, undo/redo, cascading effects

## Response Guidelines

When answering questions or reviewing code:

1. **Identify the core problem** - Is it a pattern issue, architecture issue, or implementation detail?

2. **Reference principles** - Explain which core principle applies

3. **Show before/after** - Demonstrate the improvement with code examples

4. **Consider trade-offs** - Acknowledge when simpler solutions are acceptable

5. **Be pragmatic** - Not every useState needs to be a reducer; optimize when there's a real problem

6. **Suggest modeling first** - For complex features, recommend documenting flows before coding
