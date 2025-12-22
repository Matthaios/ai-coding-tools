# Node.js Clean Architecture Structure

## Recommended Folder Structure

```
src/
├── domain/                    # Innermost layer - enterprise business rules
│   ├── entities/              # Core business objects
│   │   ├── User.ts
│   │   ├── Post.ts
│   │   └── Comment.ts
│   ├── value-objects/         # Immutable domain primitives
│   │   ├── Email.ts
│   │   ├── UserId.ts
│   │   └── Slug.ts
│   ├── errors/                # Domain-specific errors
│   │   ├── InvalidEmailError.ts
│   │   └── InsufficientPermissionsError.ts
│   └── services/              # Domain services (pure business logic)
│       └── PasswordHasher.ts  # Interface only, impl in infrastructure
│
├── application/               # Use cases layer
│   ├── use-cases/             # Application business rules
│   │   ├── user/
│   │   │   ├── CreateUser.ts
│   │   │   ├── GetUserById.ts
│   │   │   └── UpdateUserProfile.ts
│   │   └── post/
│   │       ├── CreatePost.ts
│   │       ├── PublishPost.ts
│   │       └── GetPostsByAuthor.ts
│   ├── ports/                 # Interfaces for infrastructure
│   │   ├── repositories/
│   │   │   ├── IUserRepository.ts
│   │   │   └── IPostRepository.ts
│   │   ├── services/
│   │   │   ├── IPasswordHasher.ts
│   │   │   ├── IEmailService.ts
│   │   │   └── ITokenService.ts
│   │   └── providers/
│   │       └── IDateProvider.ts
│   └── dtos/                  # Data transfer objects
│       ├── requests/
│       │   ├── CreateUserRequest.ts
│       │   └── CreatePostRequest.ts
│       └── responses/
│           ├── UserResponse.ts
│           └── PostResponse.ts
│
├── infrastructure/            # Frameworks & drivers layer
│   ├── persistence/           # Database implementations
│   │   ├── mongodb/
│   │   │   ├── models/
│   │   │   │   ├── UserModel.ts
│   │   │   │   └── PostModel.ts
│   │   │   ├── repositories/
│   │   │   │   ├── MongoUserRepository.ts
│   │   │   │   └── MongoPostRepository.ts
│   │   │   └── connection.ts
│   │   └── redis/
│   │       └── CacheRepository.ts
│   ├── services/              # External service implementations
│   │   ├── BcryptPasswordHasher.ts
│   │   ├── JwtTokenService.ts
│   │   └── SendGridEmailService.ts
│   ├── providers/
│   │   └── SystemDateProvider.ts
│   └── web/                   # Express/HTTP layer
│       ├── express/
│       │   ├── app.ts
│       │   ├── middleware/
│       │   │   ├── authMiddleware.ts
│       │   │   ├── errorHandler.ts
│       │   │   └── rateLimiter.ts
│       │   ├── routes/
│       │   │   ├── userRoutes.ts
│       │   │   └── postRoutes.ts
│       │   └── controllers/
│       │       ├── UserController.ts
│       │       └── PostController.ts
│       └── validators/        # Request validation (Joi, Zod, etc.)
│           ├── userValidators.ts
│           └── postValidators.ts
│
├── main/                      # Composition root
│   ├── server.ts              # Entry point
│   ├── config/
│   │   └── index.ts           # Environment configuration
│   └── container/             # Dependency injection
│       ├── index.ts
│       └── factories/
│           ├── userUseCases.ts
│           └── postUseCases.ts
│
└── shared/                    # Cross-cutting concerns
    ├── types/
    ├── utils/
    └── constants/
```

## Layer Implementation Examples

### Domain Layer

```typescript
// domain/entities/User.ts
// ✅ CORRECT: Pure entity, no framework dependencies
import { Email } from '../value-objects/Email';
import { UserId } from '../value-objects/UserId';

export class User {
  private constructor(
    public readonly id: UserId,
    public readonly email: Email,
    public readonly name: string,
    private passwordHash: string,
    public readonly createdAt: Date
  ) {}

  static create(email: string, name: string, passwordHash: string): User {
    return new User(
      UserId.generate(),
      Email.create(email),  // Validates email format
      name,
      passwordHash,
      new Date()
    );
  }

  canEditPost(post: Post): boolean {
    return post.authorId.equals(this.id);
  }

  verifyPassword(hash: string): boolean {
    return this.passwordHash === hash;
  }
}
```

### Application Layer

```typescript
// application/use-cases/user/CreateUser.ts
// ✅ CORRECT: Use case with interface dependencies only
import { User } from '@/domain/entities/User';
import { IUserRepository } from '../ports/repositories/IUserRepository';
import { IPasswordHasher } from '../ports/services/IPasswordHasher';
import { CreateUserRequest } from '../dtos/requests/CreateUserRequest';
import { UserResponse } from '../dtos/responses/UserResponse';

export class CreateUser {
  constructor(
    private readonly userRepo: IUserRepository,
    private readonly passwordHasher: IPasswordHasher
  ) {}

  async execute(request: CreateUserRequest): Promise<UserResponse> {
    // Check if user exists
    const existing = await this.userRepo.findByEmail(request.email);
    if (existing) {
      throw new UserAlreadyExistsError(request.email);
    }

    // Hash password
    const hash = await this.passwordHasher.hash(request.password);

    // Create user entity
    const user = User.create(request.email, request.name, hash);

    // Persist
    await this.userRepo.save(user);

    // Return DTO (not the entity!)
    return UserResponse.fromEntity(user);
  }
}
```

### Ports (Interfaces)

```typescript
// application/ports/repositories/IUserRepository.ts
import { User } from '@/domain/entities/User';
import { UserId } from '@/domain/value-objects/UserId';

export interface IUserRepository {
  save(user: User): Promise<void>;
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  delete(id: UserId): Promise<void>;
}

// application/ports/services/IPasswordHasher.ts
export interface IPasswordHasher {
  hash(password: string): Promise<string>;
  compare(password: string, hash: string): Promise<boolean>;
}
```

### Infrastructure Layer

```typescript
// infrastructure/persistence/mongodb/repositories/MongoUserRepository.ts
// ✅ CORRECT: Implements interface, handles all DB details
import { IUserRepository } from '@/application/ports/repositories/IUserRepository';
import { User } from '@/domain/entities/User';
import { UserModel } from '../models/UserModel';

export class MongoUserRepository implements IUserRepository {
  async save(user: User): Promise<void> {
    await UserModel.findByIdAndUpdate(
      user.id.value,
      this.toDocument(user),
      { upsert: true }
    );
  }

  async findById(id: UserId): Promise<User | null> {
    const doc = await UserModel.findById(id.value);
    return doc ? this.toEntity(doc) : null;
  }

  private toDocument(user: User) {
    return {
      _id: user.id.value,
      email: user.email.value,
      name: user.name,
      passwordHash: user.passwordHash,
      createdAt: user.createdAt
    };
  }

  private toEntity(doc: any): User {
    // Reconstruct entity from database document
    return User.reconstitute(/* ... */);
  }
}
```

### Controllers (Interface Adapters)

```typescript
// infrastructure/web/express/controllers/UserController.ts
// ✅ CORRECT: Controller only handles HTTP translation
import { Request, Response, NextFunction } from 'express';
import { CreateUser } from '@/application/use-cases/user/CreateUser';
import { CreateUserRequest } from '@/application/dtos/requests/CreateUserRequest';

export class UserController {
  constructor(private readonly createUser: CreateUser) {}

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      // Translate HTTP request to DTO
      const request: CreateUserRequest = {
        email: req.body.email,
        name: req.body.name,
        password: req.body.password
      };

      // Execute use case
      const response = await this.createUser.execute(request);

      // Translate to HTTP response
      res.status(201).json(response);
    } catch (error) {
      next(error);
    }
  }
}
```

### Dependency Injection

```typescript
// main/container/index.ts
import { CreateUser } from '@/application/use-cases/user/CreateUser';
import { MongoUserRepository } from '@/infrastructure/persistence/mongodb/repositories/MongoUserRepository';
import { BcryptPasswordHasher } from '@/infrastructure/services/BcryptPasswordHasher';
import { UserController } from '@/infrastructure/web/express/controllers/UserController';

export function createContainer() {
  // Infrastructure
  const userRepo = new MongoUserRepository();
  const passwordHasher = new BcryptPasswordHasher();

  // Use cases
  const createUser = new CreateUser(userRepo, passwordHasher);

  // Controllers
  const userController = new UserController(createUser);

  return { userController };
}

// main/server.ts
import express from 'express';
import { createContainer } from './container';

const app = express();
const container = createContainer();

app.post('/users', (req, res, next) => 
  container.userController.create(req, res, next)
);
```

## Testing Strategy

```typescript
// Unit test for use case - no real infrastructure needed
describe('CreateUser', () => {
  it('creates a user with hashed password', async () => {
    const mockRepo: IUserRepository = {
      save: jest.fn(),
      findByEmail: jest.fn().mockResolvedValue(null),
      // ...
    };
    const mockHasher: IPasswordHasher = {
      hash: jest.fn().mockResolvedValue('hashed'),
      compare: jest.fn(),
    };

    const useCase = new CreateUser(mockRepo, mockHasher);
    
    const result = await useCase.execute({
      email: 'test@example.com',
      name: 'Test User',
      password: 'password123'
    });

    expect(mockHasher.hash).toHaveBeenCalledWith('password123');
    expect(mockRepo.save).toHaveBeenCalled();
  });
});
```

## Common Anti-Patterns

```typescript
// ❌ WRONG: Use case directly using Mongoose
export class CreateUser {
  async execute(request) {
    const user = new UserModel(request);  // VIOLATION: Framework in use case
    await user.save();
  }
}

// ❌ WRONG: Controller with business logic
app.post('/users', async (req, res) => {
  // VIOLATION: Business rule in controller
  if (req.body.password.length < 8) {
    return res.status(400).json({ error: 'Password too short' });
  }
  // VIOLATION: Direct DB access
  await mongoose.model('User').create(req.body);
});

// ❌ WRONG: Entity with database dependency
class User {
  async save() {
    await mongoose.model('User').updateOne(/* ... */);  // VIOLATION!
  }
}
```
