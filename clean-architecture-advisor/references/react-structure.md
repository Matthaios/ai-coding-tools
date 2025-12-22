# React Clean Architecture Structure

## Recommended Folder Structure

```
src/
├── domain/                    # Innermost layer - pure business logic
│   ├── entities/              # Core business objects
│   │   ├── User.ts
│   │   ├── Product.ts
│   │   └── Order.ts
│   ├── value-objects/         # Immutable domain primitives
│   │   ├── Email.ts
│   │   ├── Money.ts
│   │   └── UserId.ts
│   └── services/              # Domain services (stateless business logic)
│       └── PricingService.ts
│
├── application/               # Use cases layer
│   ├── use-cases/             # Application-specific business rules
│   │   ├── CreateOrder.ts
│   │   ├── GetUserProfile.ts
│   │   └── ProcessPayment.ts
│   ├── ports/                 # Interfaces for outer layers
│   │   ├── repositories/      # Data access contracts
│   │   │   ├── IUserRepository.ts
│   │   │   └── IOrderRepository.ts
│   │   └── services/          # External service contracts
│   │       ├── IPaymentGateway.ts
│   │       └── IEmailService.ts
│   └── dtos/                  # Data transfer objects for use cases
│       ├── CreateOrderDTO.ts
│       └── UserProfileDTO.ts
│
├── infrastructure/            # Implementations of ports
│   ├── repositories/          # Actual data access
│   │   ├── ApiUserRepository.ts
│   │   └── LocalStorageCartRepository.ts
│   ├── services/              # External service implementations
│   │   ├── StripePaymentGateway.ts
│   │   └── SendGridEmailService.ts
│   └── http/                  # API client configuration
│       └── apiClient.ts
│
├── presentation/              # React-specific layer
│   ├── components/            # Presentational components (pure UI)
│   │   ├── Button/
│   │   ├── Card/
│   │   └── Modal/
│   ├── containers/            # Connected components (state-aware)
│   │   ├── UserProfileContainer.tsx
│   │   └── OrderListContainer.tsx
│   ├── hooks/                 # Custom React hooks
│   │   ├── useUser.ts
│   │   └── useOrders.ts
│   ├── pages/                 # Route-level components
│   │   ├── HomePage.tsx
│   │   └── CheckoutPage.tsx
│   ├── context/               # React context providers
│   │   └── AuthContext.tsx
│   └── viewmodels/            # UI state transformation
│       └── OrderListViewModel.ts
│
├── main/                      # Composition root
│   ├── App.tsx
│   ├── di/                    # Dependency injection setup
│   │   └── container.ts
│   └── routes.tsx
│
└── shared/                    # Cross-cutting utilities
    ├── types/
    ├── utils/
    └── constants/
```

## Layer Rules

### Domain Layer
```typescript
// ✅ CORRECT: Pure entity with business logic
// domain/entities/Order.ts
export class Order {
  constructor(
    public readonly id: string,
    public readonly items: OrderItem[],
    public readonly status: OrderStatus
  ) {}

  get total(): Money {
    return this.items.reduce(
      (sum, item) => sum.add(item.subtotal),
      Money.zero()
    );
  }

  canBeCancelled(): boolean {
    return this.status === OrderStatus.Pending;
  }
}

// ❌ WRONG: Entity with framework dependency
import { useState } from 'react';  // VIOLATION!
import axios from 'axios';          // VIOLATION!
```

### Application Layer
```typescript
// ✅ CORRECT: Use case with injected dependencies
// application/use-cases/CreateOrder.ts
export class CreateOrder {
  constructor(
    private orderRepo: IOrderRepository,
    private paymentGateway: IPaymentGateway
  ) {}

  async execute(dto: CreateOrderDTO): Promise<Order> {
    const order = Order.create(dto.items, dto.userId);
    await this.paymentGateway.charge(order.total);
    await this.orderRepo.save(order);
    return order;
  }
}

// ❌ WRONG: Use case with concrete implementation
import { ApiOrderRepository } from '../infrastructure/repositories';  // VIOLATION!
```

### Presentation Layer
```typescript
// ✅ CORRECT: Component receives data, has no business logic
// presentation/components/OrderSummary.tsx
interface Props {
  total: string;
  itemCount: number;
  canCheckout: boolean;
  onCheckout: () => void;
}

export const OrderSummary: React.FC<Props> = ({
  total, itemCount, canCheckout, onCheckout
}) => (
  <div>
    <p>{itemCount} items - {total}</p>
    <button disabled={!canCheckout} onClick={onCheckout}>
      Checkout
    </button>
  </div>
);

// ❌ WRONG: Component with business logic
export const OrderSummary = ({ order }) => {
  // VIOLATION: Business logic in component
  const canCheckout = order.items.length > 0 && 
    order.total.amount > order.minimumOrder;
  
  // VIOLATION: Direct API call in component
  const handleCheckout = async () => {
    await fetch('/api/orders', { method: 'POST', body: order });
  };
};
```

## Dependency Injection Pattern

```typescript
// main/di/container.ts
import { CreateOrder } from '@/application/use-cases/CreateOrder';
import { ApiOrderRepository } from '@/infrastructure/repositories/ApiOrderRepository';
import { StripePaymentGateway } from '@/infrastructure/services/StripePaymentGateway';

export const createContainer = () => {
  const orderRepo = new ApiOrderRepository();
  const paymentGateway = new StripePaymentGateway();
  
  return {
    createOrder: new CreateOrder(orderRepo, paymentGateway),
    // ... other use cases
  };
};

// Usage in React
const container = createContainer();
<AppContext.Provider value={container}>
  <App />
</AppContext.Provider>
```

## Testing Strategy

| Layer | Test Type | Dependencies |
|-------|-----------|--------------|
| Domain | Unit tests | None - pure functions |
| Application | Unit tests | Mocked ports (interfaces) |
| Infrastructure | Integration tests | Real APIs, databases |
| Presentation | Component tests | Mocked use cases |
