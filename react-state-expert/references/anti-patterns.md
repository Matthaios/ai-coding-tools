# React State Anti-Patterns

## Table of Contents
1. [Derived State Anti-Pattern](#1-derived-state-anti-pattern)
2. [useState for Non-Render Values](#2-usestate-for-non-render-values)
3. [Redundant State](#3-redundant-state)
4. [Boolean Flag Explosion](#4-boolean-flag-explosion)
5. [Cascading useEffects](#5-cascading-useeffects)

---

## 1. Derived State Anti-Pattern

### The Problem
Using `useState` + `useEffect` to calculate values that can be derived from existing state.

### How to Recognize
```typescript
// BAD: useState + useEffect combo for derived values
const [orders, setOrders] = useState<Order[]>([]);
const [total, setTotal] = useState(0);

useEffect(() => {
  const newTotal = orders.reduce((sum, order) => sum + order.price * order.quantity, 0);
  setTotal(newTotal);
}, [orders]);
```

### The Fix
Calculate directly in render:
```typescript
// GOOD: Derive state directly
const [orders, setOrders] = useState<Order[]>([]);
const total = orders.reduce((sum, order) => sum + order.price * order.quantity, 0);
```

### When to Use useMemo
Only for expensive calculations:
```typescript
// For expensive computations, use useMemo
const expensiveTotal = useMemo(() => {
  return performComplexCalculation(orders);
}, [orders]);
```

---

## 2. useState for Non-Render Values

### The Problem
Using `useState` for values that don't affect the UI, causing unnecessary re-renders.

### How to Recognize
```typescript
// BAD: Timer ID doesn't need to trigger re-renders
const [timerId, setTimerId] = useState<NodeJS.Timeout | null>(null);

const startTimer = () => {
  const id = setInterval(() => {/* ... */}, 1000);
  setTimerId(id); // Causes re-render!
};

const stopTimer = () => {
  if (timerId) clearInterval(timerId);
  setTimerId(null); // Causes re-render!
};
```

### The Fix
Use `useRef` for values that don't affect rendering:
```typescript
// GOOD: useRef doesn't trigger re-renders
const timerIdRef = useRef<NodeJS.Timeout | null>(null);

const startTimer = () => {
  timerIdRef.current = setInterval(() => {/* ... */}, 1000);
};

const stopTimer = () => {
  if (timerIdRef.current) clearInterval(timerIdRef.current);
  timerIdRef.current = null;
};
```

### Common Non-Render Values
- Timer/interval IDs
- Previous values for comparison
- Subscription references
- Animation frame IDs
- Scroll positions (when not displayed)

---

## 3. Redundant State

### The Problem
Storing entire objects when only an ID is needed, duplicating data that exists elsewhere.

### How to Recognize
```typescript
// BAD: Duplicating hotel data
const [hotels, setHotels] = useState<Hotel[]>([]);
const [selectedHotel, setSelectedHotel] = useState<Hotel | null>(null);

// When selecting:
const handleSelect = (hotel: Hotel) => {
  setSelectedHotel(hotel); // Stores entire object, can become stale!
};
```

### The Fix
Store IDs, derive objects:
```typescript
// GOOD: Store ID, derive the object
const [hotels, setHotels] = useState<Hotel[]>([]);
const [selectedHotelId, setSelectedHotelId] = useState<string | null>(null);

// Derive the selected hotel
const selectedHotel = hotels.find(h => h.id === selectedHotelId) ?? null;

// When selecting:
const handleSelect = (hotelId: string) => {
  setSelectedHotelId(hotelId);
};
```

### Why This Matters
- If `hotels` updates (price change, availability), `selectedHotel` stays in sync
- Single source of truth
- Simpler state to manage
- Prevents stale data bugs

---

## 4. Boolean Flag Explosion

### The Problem
Multiple boolean states that are mutually exclusive, leading to impossible states.

### How to Recognize
```typescript
// BAD: These booleans can be in impossible combinations
const [isLoading, setIsLoading] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
const [isError, setIsError] = useState(false);

// Possible impossible state: isLoading && isSuccess && isError === all true
```

### The Fix
Use explicit status enum (finite states):
```typescript
// GOOD: Mutually exclusive states
type Status = 'idle' | 'loading' | 'success' | 'error';
const [status, setStatus] = useState<Status>('idle');

// Derive booleans if needed for compatibility
const isLoading = status === 'loading';
const isSuccess = status === 'success';
const isError = status === 'error';
```

### Advanced: Type States (Discriminated Unions)
When different states have different data:
```typescript
type RequestState = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: Result[] }
  | { status: 'error'; error: string };

const [state, setState] = useState<RequestState>({ status: 'idle' });

// TypeScript enforces that data exists only in success state
if (state.status === 'success') {
  console.log(state.data); // TypeScript knows data exists
}
```

---

## 5. Cascading useEffects

### The Problem
Multiple useEffects that trigger each other, creating hard-to-debug chains.

### How to Recognize
```typescript
// BAD: Cascading effects - hard to trace execution
const [destination, setDestination] = useState('');
const [flightResults, setFlightResults] = useState<Flight[]>([]);
const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
const [hotelResults, setHotelResults] = useState<Hotel[]>([]);

// Effect 1: Search flights when destination changes
useEffect(() => {
  if (destination) {
    searchFlights(destination).then(setFlightResults);
  }
}, [destination]);

// Effect 2: Auto-select first flight
useEffect(() => {
  if (flightResults.length > 0) {
    setSelectedFlight(flightResults[0]);
  }
}, [flightResults]);

// Effect 3: Search hotels when flight selected
useEffect(() => {
  if (selectedFlight) {
    searchHotels(selectedFlight.destination).then(setHotelResults);
  }
}, [selectedFlight]);
```

### The Fix
Use a reducer with explicit events and a single effect:
```typescript
// GOOD: Centralized logic with reducer
type State = {
  status: 'idle' | 'searching-flights' | 'searching-hotels' | 'complete';
  destination: string;
  flightResults: Flight[];
  selectedFlight: Flight | null;
  hotelResults: Hotel[];
};

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SEARCH_STARTED':
      return { ...state, status: 'searching-flights', destination: action.destination };
    case 'FLIGHTS_RECEIVED':
      return { 
        ...state, 
        status: 'searching-hotels', 
        flightResults: action.flights,
        selectedFlight: action.flights[0] 
      };
    case 'HOTELS_RECEIVED':
      return { ...state, status: 'complete', hotelResults: action.hotels };
    default:
      return state;
  }
}

// Single effect that reacts to status
useEffect(() => {
  if (state.status === 'searching-flights') {
    searchFlights(state.destination).then(flights => 
      dispatch({ type: 'FLIGHTS_RECEIVED', flights })
    );
  } else if (state.status === 'searching-hotels' && state.selectedFlight) {
    searchHotels(state.selectedFlight.destination).then(hotels =>
      dispatch({ type: 'HOTELS_RECEIVED', hotels })
    );
  }
}, [state.status, state.destination, state.selectedFlight]);
```

### Benefits of Single Effect Pattern
- Clear execution order
- Easier to debug
- Events capture intent
- Testable reducer logic
- No race conditions from multiple effects

---

## Quick Reference

| Anti-Pattern | Recognition | Solution |
|--------------|-------------|----------|
| Derived State | useState + useEffect for calculations | Calculate in render |
| Non-Render Values | useState for timer IDs, refs | useRef |
| Redundant State | Storing objects instead of IDs | Store ID, derive object |
| Boolean Explosion | Multiple mutually exclusive booleans | Status enum / discriminated union |
| Cascading Effects | Chain of useEffects triggering each other | Reducer + single effect |
