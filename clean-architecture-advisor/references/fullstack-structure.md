# Fullstack Monorepo Clean Architecture

## Recommended Structure

```
project-root/
├── packages/
│   ├── core/                      # Shared domain logic (framework-agnostic)
│   │   ├── src/
│   │   │   ├── entities/          # Business entities
│   │   │   │   ├── User.ts
│   │   │   │   ├── Order.ts
│   │   │   │   └── Product.ts
│   │   │   ├── value-objects/     # Domain primitives
│   │   │   │   ├── Email.ts
│   │   │   │   ├── Money.ts
│   │   │   │   └── UserId.ts
│   │   │   ├── services/          # Domain services
│   │   │   │   └── PricingService.ts
│   │   │   ├── errors/            # Domain errors
│   │   │   │   └── DomainError.ts
│   │   │   └── index.ts           # Public exports
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── shared/                    # Shared types and utilities
│   │   ├── src/
│   │   │   ├── types/             # Shared TypeScript types
│   │   │   │   ├── api.ts         # API request/response types
│   │   │   │   └── common.ts
│   │   │   ├── validation/        # Shared validation schemas
│   │   │   │   └── schemas.ts
│   │   │   └── utils/
│   │   │       └── formatting.ts
│   │   └── package.json
│   │
│   ├── backend/                   # Node.js API
│   │   ├── src/
│   │   │   ├── application/       # Use cases
│   │   │   │   ├── use-cases/
│   │   │   │   │   ├── user/
│   │   │   │   │   └── order/
│   │   │   │   ├── ports/         # Repository/service interfaces
│   │   │   │   │   ├── repositories/
│   │   │   │   │   └── services/
│   │   │   │   └── dtos/
│   │   │   ├── infrastructure/    # External implementations
│   │   │   │   ├── persistence/
│   │   │   │   │   ├── postgres/
│   │   │   │   │   └── redis/
│   │   │   │   ├── services/
│   │   │   │   └── web/
│   │   │   │       ├── express/
│   │   │   │       │   ├── app.ts
│   │   │   │       │   ├── controllers/
│   │   │   │       │   ├── middleware/
│   │   │   │       │   └── routes/
│   │   │   │       └── graphql/   # Alternative API layer
│   │   │   └── main/
│   │   │       ├── server.ts
│   │   │       └── container/
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── frontend/                  # React application
│       ├── src/
│       │   ├── application/       # Frontend use cases
│       │   │   ├── use-cases/     # UI-specific business logic
│       │   │   │   ├── AddToCart.ts
│       │   │   │   └── Checkout.ts
│       │   │   └── ports/         # API client interfaces
│       │   │       └── IApiClient.ts
│       │   ├── infrastructure/    # Implementation details
│       │   │   ├── api/           # API client implementation
│       │   │   │   └── HttpApiClient.ts
│       │   │   └── storage/       # Local storage, IndexedDB
│       │   │       └── CartStorage.ts
│       │   ├── presentation/      # React components
│       │   │   ├── components/
│       │   │   ├── containers/
│       │   │   ├── pages/
│       │   │   ├── hooks/
│       │   │   └── context/
│       │   └── main/
│       │       ├── App.tsx
│       │       └── container/
│       ├── package.json
│       └── tsconfig.json
│
├── package.json                   # Workspace root
├── pnpm-workspace.yaml            # Or lerna.json, nx.json
└── tsconfig.base.json
```

## Shared Core Package

The `core` package contains pure domain logic usable by both frontend and backend:

```typescript
// packages/core/src/entities/Order.ts
import { Money } from '../value-objects/Money';
import { OrderItem } from './OrderItem';

export class Order {
  constructor(
    public readonly id: string,
    public readonly items: OrderItem[],
    public readonly status: OrderStatus
  ) {}

  get subtotal(): Money {
    return this.items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.zero()
    );
  }

  get tax(): Money {
    return this.subtotal.multiply(0.1); // 10% tax
  }

  get total(): Money {
    return this.subtotal.add(this.tax);
  }

  canAddItem(): boolean {
    return this.status === OrderStatus.Draft && this.items.length < 100;
  }

  canCheckout(): boolean {
    return this.items.length > 0 && this.subtotal.isGreaterThan(Money.cents(100));
  }
}
```

## Using Core in Backend

```typescript
// packages/backend/src/application/use-cases/order/CreateOrder.ts
import { Order } from '@project/core';  // Import from shared core
import { IOrderRepository } from '../../ports/repositories/IOrderRepository';

export class CreateOrder {
  constructor(private readonly orderRepo: IOrderRepository) {}

  async execute(userId: string): Promise<Order> {
    const order = Order.createDraft(userId);
    await this.orderRepo.save(order);
    return order;
  }
}
```

## Using Core in Frontend

```typescript
// packages/frontend/src/presentation/hooks/useCart.ts
import { Order, Money } from '@project/core';  // Same entities!
import { useCartState } from '../context/CartContext';

export function useCart() {
  const { order, updateOrder } = useCartState();

  const canCheckout = order.canCheckout();  // Use domain logic directly
  const total = order.total;                // Consistent calculation

  const addItem = (productId: string, quantity: number) => {
    if (!order.canAddItem()) {
      throw new Error('Cannot add more items');
    }
    // ... update logic
  };

  return { order, total, canCheckout, addItem };
}
```

## Workspace Configuration

```json
// package.json (root)
{
  "name": "project-root",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "dev:backend": "pnpm --filter backend dev",
    "dev:frontend": "pnpm --filter frontend dev"
  }
}

// packages/backend/package.json
{
  "name": "@project/backend",
  "dependencies": {
    "@project/core": "workspace:*",
    "@project/shared": "workspace:*"
  }
}

// packages/frontend/package.json
{
  "name": "@project/frontend",
  "dependencies": {
    "@project/core": "workspace:*",
    "@project/shared": "workspace:*"
  }
}
```

## API Contract Sharing

```typescript
// packages/shared/src/types/api.ts
// Shared API types ensure frontend/backend consistency

export interface CreateOrderRequest {
  items: Array<{
    productId: string;
    quantity: number;
  }>;
}

export interface OrderResponse {
  id: string;
  status: string;
  items: OrderItemResponse[];
  subtotal: number;
  tax: number;
  total: number;
}

// packages/backend/src/infrastructure/web/controllers/OrderController.ts
import { CreateOrderRequest, OrderResponse } from '@project/shared';

export class OrderController {
  async create(req: Request<CreateOrderRequest>): Promise<OrderResponse> {
    // Type-safe request handling
  }
}

// packages/frontend/src/infrastructure/api/OrderApiClient.ts
import { CreateOrderRequest, OrderResponse } from '@project/shared';

export class OrderApiClient {
  async createOrder(request: CreateOrderRequest): Promise<OrderResponse> {
    return this.http.post('/orders', request);
  }
}
```

## Dependency Flow

```
                    ┌─────────────────────────┐
                    │       @project/core     │
                    │    (Pure Domain Logic)  │
                    └───────────┬─────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ @project/shared │   │ @project/backend│   │@project/frontend│
│   (Types, DTOs) │   │    (Node.js)    │   │    (React)      │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └─────────────────────┴─────────────────────┘
                        Both import from
                        core and shared
```

## Benefits of This Structure

1. **Single source of truth** for business logic
2. **Type safety** across the entire stack
3. **Consistent calculations** (e.g., pricing logic)
4. **Easier testing** - core has no dependencies
5. **Independent deployment** - each package builds separately
6. **Clear boundaries** - imports show dependencies explicitly

## Testing Strategy

```
packages/
├── core/
│   └── src/__tests__/           # Unit tests (no mocks needed)
│       ├── entities/
│       └── value-objects/
├── backend/
│   └── src/
│       ├── application/__tests__/  # Use case tests (mock ports)
│       └── infrastructure/__tests__/ # Integration tests
└── frontend/
    └── src/
        ├── application/__tests__/  # Use case tests
        └── presentation/__tests__/ # Component tests
```
