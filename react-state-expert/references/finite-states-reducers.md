# Finite States & Reducers

## Table of Contents
1. [Combining Related State](#1-combining-related-state)
2. [Finite States (Status Enums)](#2-finite-states-status-enums)
3. [Type States (Discriminated Unions)](#3-type-states-discriminated-unions)
4. [useReducer Fundamentals](#4-usereducer-fundamentals)
5. [Context + Reducer Pattern](#5-context--reducer-pattern)
6. [Step-Based Flows](#6-step-based-flows)
7. [Testing Reducers](#7-testing-reducers)

---

## 1. Combining Related State

### When to Combine
Combine state when values are:
- Updated together frequently
- Logically related (same domain)
- Part of the same form or entity

### Before
```typescript
const [coffeeType, setCoffeeType] = useState('');
const [size, setSize] = useState('medium');
const [sugar, setSugar] = useState(0);
const [milk, setMilk] = useState(false);
```

### After
```typescript
interface CoffeeOrder {
  type: string;
  size: string;
  sugar: number;
  milk: boolean;
}

const [coffee, setCoffee] = useState<CoffeeOrder>({
  type: '',
  size: 'medium',
  sugar: 0,
  milk: false
});

// Update with previous value to avoid closure issues
const updateCoffee = (field: keyof CoffeeOrder, value: any) => {
  setCoffee(prev => ({ ...prev, [field]: value }));
};
```

### Important: Use Previous Value
Always use the callback form to avoid stale closure issues:
```typescript
// BAD: May use stale coffee value
setCoffee({ ...coffee, type: 'latte' });

// GOOD: Always uses current value
setCoffee(prev => ({ ...prev, type: 'latte' }));
```

---

## 2. Finite States (Status Enums)

### Replace Boolean Flags
```typescript
// Before: Multiple booleans
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);

// After: Single status
type Status = 'idle' | 'loading' | 'error' | 'success';
const [status, setStatus] = useState<Status>('idle');

// Derive booleans for backward compatibility
const isLoading = status === 'loading';
```

### Benefits
- Impossible to be in multiple states simultaneously
- Self-documenting code
- Easier conditional rendering
- Better type safety

### Pattern for Conditional Rendering
```typescript
// Clear, explicit rendering based on status
{status === 'idle' && <SearchForm />}
{status === 'loading' && <Spinner />}
{status === 'success' && <Results />}
{status === 'error' && <ErrorMessage />}
```

---

## 3. Type States (Discriminated Unions)

### When to Use
When different states have different associated data.

### Basic Pattern
```typescript
type FlightState = 
  | { status: 'idle'; flightOptions: null; error: null }
  | { status: 'loading'; flightOptions: null; error: null }
  | { status: 'success'; flightOptions: Flight[]; error: null }
  | { status: 'error'; flightOptions: null; error: string };
```

### With Common Properties (Intersection)
```typescript
// Common fields + discriminated union for status-specific fields
type FlightData = {
  destination: string;
  departure: string;
  arrival: string;
  passengers: number;
} & (
  | { status: 'idle'; flightOptions: null; error: null }
  | { status: 'loading'; flightOptions: null; error: null }
  | { status: 'success'; flightOptions: Flight[]; error: null }
  | { status: 'error'; flightOptions: null; error: string }
);
```

### TypeScript Enforces Correctness

**At write time** - Can't forget required fields:
```typescript
// TypeScript error: Property 'flightOptions' is missing
setState({ status: 'success', error: null }); 

// Correct:
setState({ status: 'success', flightOptions: flights, error: null });
```

**At read time** - Narrowing based on status:
```typescript
if (state.status === 'success') {
  // TypeScript knows flightOptions is Flight[], not null
  state.flightOptions.map(flight => ...);
}
```

---

## 4. useReducer Fundamentals

### When to Use useReducer
- State logic is complex
- Multiple values update together
- Next state depends on previous state
- You want testable business logic

### Basic Structure
```typescript
type State = {
  status: 'idle' | 'loading' | 'success' | 'error';
  data: Item[] | null;
  error: string | null;
};

type Action = 
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: Item[] }
  | { type: 'FETCH_ERROR'; payload: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, status: 'loading', error: null };
    case 'FETCH_SUCCESS':
      return { ...state, status: 'success', data: action.payload };
    case 'FETCH_ERROR':
      return { ...state, status: 'error', error: action.payload };
    default:
      return state;
  }
}

// Usage
const [state, dispatch] = useReducer(reducer, initialState);
dispatch({ type: 'FETCH_START' });
```

### State-First Switch (Advanced)
For complex flows, switch on state first:
```typescript
function reducer(state: State, action: Action): State {
  switch (state.status) {
    case 'idle':
      if (action.type === 'SEARCH') {
        return { ...state, status: 'loading', query: action.query };
      }
      return state;
    
    case 'loading':
      if (action.type === 'RESULTS') {
        return { ...state, status: 'success', data: action.data };
      }
      if (action.type === 'ERROR') {
        return { ...state, status: 'error', error: action.error };
      }
      return state;
    
    // ... other states
  }
}
```

---

## 5. Context + Reducer Pattern

### Setup
```typescript
// Define context type
type BookingContextType = {
  state: BookingState;
  dispatch: React.Dispatch<BookingAction>;
};

// Create context
const BookingContext = createContext<BookingContextType | null>(null);

// Provider component
function BookingProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(bookingReducer, initialState);
  
  return (
    <BookingContext.Provider value={{ state, dispatch }}>
      {children}
    </BookingContext.Provider>
  );
}

// Custom hook for consuming
function useBooking() {
  const context = useContext(BookingContext);
  if (!context) {
    throw new Error('useBooking must be used within BookingProvider');
  }
  return context;
}
```

### Usage in Components
```typescript
function SearchForm() {
  const { state, dispatch } = useBooking();
  
  const handleSubmit = (data: SearchData) => {
    dispatch({ type: 'SEARCH', payload: data });
  };
  
  return <form onSubmit={handleSubmit}>...</form>;
}
```

### React 19: use() Hook
```typescript
// Modern approach with use()
import { use } from 'react';

function SearchForm() {
  const { dispatch } = use(BookingContext);
  // ...
}
```

### Performance Note
Context causes re-renders for all consumers when value changes. For frequently updating state, consider third-party libraries (Zustand, XState Store) that offer fine-grained subscriptions.

---

## 6. Step-Based Flows

### Linear Steps (Simple)
```typescript
const steps = ['search', 'results', 'confirm', 'complete'] as const;
type Step = typeof steps[number];

const [stepIndex, setStepIndex] = useState(0);
const currentStep = steps[stepIndex];

const nextStep = () => setStepIndex(i => Math.min(i + 1, steps.length - 1));
const prevStep = () => setStepIndex(i => Math.max(i - 1, 0));
```

### Non-Linear Steps (Graph-Based)
For flows where navigation isn't strictly linear:
```typescript
const stepGraph = {
  search: { next: 'loading' },
  loading: { next: 'results', back: 'search' },
  results: { next: 'confirm', back: 'search' }, // Skip loading on back
  confirm: { next: 'complete', back: 'results' },
  complete: {} // Terminal state
} as const;

type Step = keyof typeof stepGraph;
const [currentStep, setCurrentStep] = useState<Step>('search');

const nextStep = () => {
  const next = stepGraph[currentStep].next;
  if (next) setCurrentStep(next);
};

const prevStep = () => {
  const back = stepGraph[currentStep].back;
  if (back) setCurrentStep(back);
};
```

### Preventing Invalid Transitions
```typescript
function reducer(state: State, action: Action): State {
  // Only allow back from specific states
  if (action.type === 'BACK') {
    switch (state.status) {
      case 'results':
        return { ...state, status: 'search' };
      case 'confirm':
        return { ...state, status: 'results' };
      default:
        return state; // Ignore back in other states
    }
  }
  // ...
}
```

---

## 7. Testing Reducers

### Why Test Reducers
- Pure functions: same input always produces same output
- No mocking required
- Test business logic independently from UI
- Tests remain valid even if UI changes

### Basic Pattern
```typescript
import { bookingReducer, initialState } from './bookingReducer';

describe('bookingReducer', () => {
  it('transitions to loading on search', () => {
    const state = bookingReducer(initialState, { 
      type: 'SEARCH', 
      payload: { destination: 'Tokyo' } 
    });
    
    expect(state.status).toBe('loading');
    expect(state.searchParams.destination).toBe('Tokyo');
  });
  
  it('transitions to success with data', () => {
    const loadingState = { ...initialState, status: 'loading' };
    const mockFlights = [{ id: '1', airline: 'Test Air' }];
    
    const state = bookingReducer(loadingState, {
      type: 'RESULTS',
      payload: mockFlights
    });
    
    expect(state.status).toBe('success');
    expect(state.flightOptions).toEqual(mockFlights);
  });
});
```

### Testing Full Flows
```typescript
it('completes full booking flow', () => {
  let state = initialState;
  
  // Search
  state = bookingReducer(state, { type: 'SEARCH', payload: { destination: 'Tokyo' } });
  expect(state.status).toBe('loading');
  
  // Receive results
  state = bookingReducer(state, { type: 'RESULTS', payload: mockFlights });
  expect(state.status).toBe('success');
  
  // Select flight
  state = bookingReducer(state, { type: 'SELECT_FLIGHT', payload: 'flight-1' });
  expect(state.selectedFlightId).toBe('flight-1');
  
  // Confirm
  state = bookingReducer(state, { type: 'CONFIRM' });
  expect(state.status).toBe('confirmed');
});
```

### Testing Invalid Transitions
```typescript
it('ignores back action from search state', () => {
  const state = bookingReducer(initialState, { type: 'BACK' });
  expect(state).toEqual(initialState); // No change
});
```
