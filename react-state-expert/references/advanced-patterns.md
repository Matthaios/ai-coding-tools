# Advanced State Patterns

## Table of Contents
1. [Data Normalization](#1-data-normalization)
2. [Branded Types for IDs](#2-branded-types-for-ids)
3. [Undo/Redo with Events](#3-undoredo-with-events)
4. [Third-Party State Libraries](#4-third-party-state-libraries)
5. [URL as State](#5-url-as-state)
6. [Server State with TanStack Query](#6-server-state-with-tanstack-query)
7. [useSyncExternalStore](#7-usesyncexternalstore)
8. [FormData for Simple Forms](#8-formdata-for-simple-forms)

---

## 1. Data Normalization

### The Problem with Nested Data
```typescript
// Nested structure - hard to update, poor performance
type Itinerary = {
  reservations: {
    id: string;
    passengers: {
      id: string;
      name: string;
      visitedCountries: string[];
    }[];
  }[];
};
```

Problems:
- Deep updates require spreading at every level
- Finding items requires nested searches
- Updates cascade to parent components

### Normalized Structure
```typescript
type NormalizedItinerary = {
  reservations: { id: string; flightNumber: string }[];
  passengers: { id: string; reservationId: string; name: string }[];
  visitedCountries: { id: string; passengerId: string; country: string }[];
};
```

### Lookup Comparison
```typescript
// Nested: O(n * m) lookups
const passenger = itinerary.reservations
  .find(r => r.id === '123')?.passengers
  .find(p => p.id === 'john');

// Normalized: O(n) or O(1) with Map
const passenger = itinerary.passengers
  .find(p => p.reservationId === '123' && p.id === 'john');

// Even better with object/Map
const passengerMap = new Map(passengers.map(p => [p.id, p]));
const passenger = passengerMap.get('john');
```

### Updating Normalized Data
```typescript
// Delete destination and related todos
case 'DELETE_DESTINATION':
  return {
    ...state,
    destinations: state.destinations.filter(d => d.id !== action.id),
    todos: state.todos.filter(t => t.destinationId !== action.id)
  };
```

---

## 2. Branded Types for IDs

### The Problem
String IDs can be accidentally mixed up:
```typescript
// Nothing stops us from passing wrong ID type
const selectFlight = (flightId: string) => { ... };
selectFlight(hotelId); // Compiles but wrong!
```

### Branded Types Solution
```typescript
// Create branded types
type Brand<T, B> = T & { __brand: B };

type DestinationId = Brand<string, 'DestinationId'>;
type TodoId = Brand<string, 'TodoId'>;
type FlightId = Brand<string, 'FlightId'>;

// Now TypeScript enforces correct ID types
type Todo = {
  id: TodoId;
  destinationId: DestinationId;
  text: string;
};

// Creating branded IDs
const createDestinationId = (): DestinationId => 
  crypto.randomUUID() as DestinationId;

// Type errors prevent mistakes
const selectFlight = (flightId: FlightId) => { ... };
selectFlight(destinationId); // TypeScript error!
```

### Runtime Behavior
At runtime, branded types are just strings. The branding is purely for TypeScript's type system.

---

## 3. Undo/Redo with Events

### Core Principle
Events are the source of truth. Current state = replaying all events.

### State Structure
```typescript
type State = {
  // Current data
  destinations: Destination[];
  todos: Todo[];
  
  // Event history
  events: Action[];      // All actions that led to current state
  undos: Action[];       // Actions that were undone (for redo)
};
```

### Undo Implementation
```typescript
case 'UNDO':
  if (state.events.length === 0) return state;
  
  // Get all events except the last one
  const eventsToReplay = state.events.slice(0, -1);
  const undoneEvent = state.events[state.events.length - 1];
  
  // Replay all events from initial state
  let newState = initialState;
  for (const event of eventsToReplay) {
    newState = reducer(newState, event);
  }
  
  return {
    ...newState,
    events: eventsToReplay,
    undos: [...state.undos, undoneEvent]
  };
```

### Redo Implementation
```typescript
case 'REDO':
  if (state.undos.length === 0) return state;
  
  const eventToRedo = state.undos[state.undos.length - 1];
  const remainingUndos = state.undos.slice(0, -1);
  
  // Apply the redone event
  const redoneState = reducer(state, eventToRedo);
  
  return {
    ...redoneState,
    events: [...state.events, eventToRedo],
    undos: remainingUndos
  };
```

### Recording Events
```typescript
// All other actions should record themselves
default:
  const newState = actualReducer(state, action);
  return {
    ...newState,
    events: [...state.events, action],
    undos: [] // Clear redo stack on new action
  };
```

---

## 4. Third-Party State Libraries

### When to Use
- Context re-renders are causing performance issues
- Need fine-grained subscriptions
- Complex subscription patterns
- Want to reduce boilerplate

### Store-Based (Zustand, XState Store)
Centralized state with controlled updates:

```typescript
import { createStore } from '@xstate/store';

const bookingStore = createStore({
  context: { 
    step: 'search',
    destination: '',
    flightOptions: null 
  },
  on: {
    updateDestination: (ctx, event: { destination: string }) => ({
      ...ctx,
      destination: event.destination
    }),
    setFlights: (ctx, event: { flights: Flight[] }) => ({
      ...ctx,
      step: 'results',
      flightOptions: event.flights
    })
  }
});

// Usage in component - fine-grained subscription
const destination = useSelector(bookingStore, state => state.context.destination);

// Trigger updates
bookingStore.trigger.updateDestination({ destination: 'Tokyo' });
```

### Atomic (Jotai-style)
Individual pieces of reactive state:

```typescript
import { createAtom } from '@xstate/store';

const countAtom = createAtom(0);
const doubleAtom = createAtom((get) => get(countAtom) * 2);

// Usage - only re-renders when specific atom changes
const count = useSelector(countAtom);
const double = useSelector(doubleAtom);

// Update
countAtom.set(prev => prev + 1);
```

### Choosing Store vs Atomic
- **Store**: Complex logic, controlled transitions, business rules
- **Atomic**: Simple reactive values, derived state, frequent updates

---

## 5. URL as State

### Benefits
- Shareable/bookmarkable URLs
- Browser back/forward navigation works
- State survives page refresh
- Deep linking support

### Using nuqs
```typescript
import { useQueryState, parseAsBoolean, parseAsStringEnum } from 'nuqs';

// String parameters
const [destination, setDestination] = useQueryState('destination');

// Boolean with default
const [oneWay, setOneWay] = useQueryState(
  'oneWay', 
  parseAsBoolean.withDefault(false)
);

// Enum
const [sortOrder, setSortOrder] = useQueryState(
  'sort',
  parseAsStringEnum(['asc', 'desc']).withDefault('asc')
);
```

### URL Updates
- `setDestination('Tokyo')` updates URL to `?destination=Tokyo`
- Changes are debounced and use `replaceState` (no history spam)
- Values persist across navigation

### Multi-Step Forms with URL
```typescript
type View = 'search' | 'results' | 'confirm';
const [view, setView] = useQueryState(
  'view',
  parseAsStringEnum(['search', 'results', 'confirm']).withDefault('search')
);

// URL preserves form state AND current step
// ?view=results&destination=Tokyo&departure=2024-01-15
```

---

## 6. Server State with TanStack Query

### The Problem with useState + useEffect
```typescript
// Manual approach - lots of boilerplate
const [data, setData] = useState(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);

useEffect(() => {
  let cancelled = false;
  setIsLoading(true);
  
  fetchFlights(params)
    .then(data => {
      if (!cancelled) setData(data);
    })
    .catch(err => {
      if (!cancelled) setError(err);
    })
    .finally(() => {
      if (!cancelled) setIsLoading(false);
    });
    
  return () => { cancelled = true; };
}, [params]);
```

### TanStack Query Solution
```typescript
import { useQuery } from '@tanstack/react-query';

const { data, isLoading, error } = useQuery({
  queryKey: ['flights', destination, date],
  queryFn: () => fetchFlights({ destination, date }),
  staleTime: 5 * 60 * 1000, // Cache for 5 minutes
});
```

### Key Features
- **Caching**: Instant results for repeated queries
- **Background refetching**: Keep data fresh
- **Automatic retries**: Handle transient failures
- **Request deduplication**: Multiple components, one request
- **Loading/error states**: Built-in status management

### Setup Required
```typescript
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  );
}
```

---

## 7. useSyncExternalStore

### When to Use
Subscribing to external data sources (not React state):
- Browser APIs (online/offline, window size)
- Third-party stores
- WebSocket connections
- External subscriptions

### Basic Pattern
```typescript
import { useSyncExternalStore } from 'react';

function useOnlineStatus() {
  return useSyncExternalStore(
    // Subscribe function
    (callback) => {
      window.addEventListener('online', callback);
      window.addEventListener('offline', callback);
      return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
      };
    },
    // Get client snapshot
    () => navigator.onLine,
    // Get server snapshot (for SSR)
    () => true // Assume online during SSR
  );
}
```

### Benefits Over useState + useEffect
- Handles hydration mismatches automatically
- No race conditions
- Proper cleanup
- Concurrent rendering safe

### External Store Example
```typescript
// Flight updates store
const flightStore = {
  flights: [],
  listeners: new Set<() => void>(),
  
  subscribe(callback: () => void) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  },
  
  getSnapshot() {
    return this.flights;
  },
  
  update(newFlights: Flight[]) {
    this.flights = newFlights;
    this.listeners.forEach(cb => cb());
  }
};

// Usage
const flights = useSyncExternalStore(
  flightStore.subscribe.bind(flightStore),
  flightStore.getSnapshot.bind(flightStore),
  () => [] // Server snapshot
);
```

---

## 8. FormData for Simple Forms

### Why Use FormData
- HTML forms already store state
- Less useState boilerplate
- Works with server actions
- Native browser feature

### Basic Pattern
```typescript
function SimpleForm() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const data = {
      firstName: formData.get('firstName') as string,
      lastName: formData.get('lastName') as string,
    };
    
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="firstName" />
      <input name="lastName" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### With Zod Validation
```typescript
import { z } from 'zod';

const formSchema = z.object({
  firstName: z.string().min(1, 'Required'),
  lastName: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email'),
});

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
  const rawData = Object.fromEntries(formData.entries());
  
  const result = formSchema.safeParse(rawData);
  
  if (!result.success) {
    console.log('Errors:', result.error.flatten());
    return;
  }
  
  console.log('Valid data:', result.data);
};
```

### React 19 useActionState
```typescript
import { useActionState } from 'react';

function FormWithAction() {
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData: FormData) => {
      // This runs on the server (or client)
      const result = await submitForm(formData);
      return result;
    },
    null // Initial state
  );

  return (
    <form action={formAction}>
      <input name="email" />
      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
}
```

### When to Use useState vs FormData
- **useState**: Live validation, dependent fields, complex interactions
- **FormData**: Simple forms, server actions, minimal client state
