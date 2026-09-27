# Personal Finance Intelligence System: Architecture & Progress Summary

This document summarizes everything covered so far, the conceptual hurdles and "stuck points" we broke down, the current status of the codebase, and the concrete roadmap ahead.

---

## 1. Executive Summary & Philosophy

The project is built as a **Pragmatic Modular Monolith**[Traditional Monolith + Microservices = Mini-service Architecture] in Python/FastAPI without enterprise bloat. 
The core philosophy is a **strict 4-layer unidirectional flow**:

```
[ HTTP Request ]
       │
       ▼
1. Routers (app/backend/routes/)
   - HTTP parsing, route parameters, status codes, dependency injection (`db`, `current_user`).
   - Input/output shape enforced via Pydantic schemas.
       │
       ▼
2. Services (app/backend/services/)
   - Pure business logic (password hashing, user creation, OAuth verification, financial calculations).
   - Zero HTTP concerns (no `Request` or `Response` objects here).
       │
       ▼
3. Database & Models (app/backend/models/ & database/)
   - SQLAlchemy ORM models, queries, unit of work (commits/rollbacks).
       │
       ▼
[ PostgreSQL 18.4 (Docker) ]
```

---

## 2. What We Have Built & Finalized

### A. Pydantic Validation Layer (`app/backend/schema/user.py`)
- **`RegisterRequest`:** Enforces `EmailStr` and an OWASP-compliant password constraint (`min_length=8, max_length=128`). Includes a clean `@field_validator` verifying that `confirm_password == password`.
- **`LoginRequest`:** Clean inbound schema for user email and password credentials.
- **`TokenResponse`:** Complete dual-token outbound payload where the access token is used to authorize and access the protected resources and the refresh token is used to  refresh the access token (`access_token`, `refresh_token`, `token_type = "bearer"`).
- **`RefreshTokenRequest`:** Inbound schema accepting `{ "refresh_token": "..." }` when access tokens expire.
- **`TokenPayload`:** Internal DTO using standard RFC 7519 naming (`sub: str | None = None`) to safely validate claims decoded from JWTs.
- **`UserResponse`:** Public user representation with `ConfigDict(from_attributes=True)` enabling direct serialization from SQLAlchemy ORM entities.

### B. Database Connection & Session Management (`app/backend/database/`)
- **Engine Resilience (`database.py`):** Added `pool_pre_ping=True` to `create_engine` to prevent dropped TCP connection errors on idle cloud databases.
- **Session Lifecycle Dependency (`dependencies.py`):** Created `get_db()` with a generator pattern:
  - Opens `SessionLocal()`
  - Yields session to FastAPI route dependencies
  - Guarantees `db.close()` inside a `try ... finally` block
  - Strongly typed with `Generator[Session, None, None]` for IDE autocompletion.

### C. FastAPI Application Structure (`app/backend/main.py` & `routes/auth.py`)
- **Cleaned `main.py`:** Removed unused `engine` and `Base` imports, ensuring Alembic remains the single authority for schema migrations.
- **Route Namespacing:** Configured `APIRouter(prefix="/auth", tags=["Auth"])` for predictable URLs and organized OpenAPI (`/docs`) groupings.
- **`def` vs `async def` Alignment:** Transitioned database-backed route handlers to standard synchronous `def` so FastAPI safely offloads blocking `psycopg2` calls to background worker threadpools.

### D. Configuration & Security Infrastructure (`config.py` & `utils/security.py`)
- **JWT Configuration (`config.py`):** Added `SECRET_KEY`, `ALGORITHM` (HS256), `ACCESS_TOKEN_EXPIRE_MINUTES` (30m), and `REFRESH_TOKEN_EXPIRE_DAYS` (30d) with safe environment variable parsing and defaults.
- **Password Security (`utils/security.py`):**
  - `hash_password`: One-way hashing using `bcrypt.gensalt()` and `bcrypt.hashpw()`, converting UTF-8 strings to bytes and back.
  - `verify_password`: Constant-time hash verification using `bcrypt.checkpw()`, protected with error handling to safely return `False` on corrupted hashes without throwing unhandled exceptions.
- **Token Minting & Verification (`utils/security.py`):**
  - `create_access_token`: Generates signed JWTs with UTC expiration and `"type": "access"` stamp.
  - `create_refresh_token`: Generates longer-lived signed JWTs with `"type": "refresh"` stamp.
  - Both functions use `to_encode = data.copy()` to preserve immutability and prevent side-effect pollution of caller data.
  - `decode_token`: Decodes and mathematically verifies JWT signatures and expiration times using `jose.jwt.decode`. Catches `JWTError` safely and returns `dict | None` to insulate callers from unexpected decoding crashes. Explicitly enforces allowed `algorithms=[ALGORITHM]` to protect against algorithm confusion (`alg=none`) attacks.

---

## 3. Where We Were Stuck & Key Conceptual Hurdles Resolved

During our discussions, we tackled several critical real-world architectural dilemmas:

| Hurdle / Question | Why It Was a Blocker | How We Solved It |
| :--- | :--- | :--- |
| **Password Regex Over-restriction** | The initial regex rejected valid passwords containing spaces, dashes, or special characters generated by password managers. | Replaced strict regex with `min_length=8, max_length=128`. The 128-char limit prevents bcrypt CPU exhaustion (DoS). |
| **The "JWT Trap" (Statelessness vs Revocation)** | Pure JWTs cannot be revoked if a user is banned, logs out, or loses a laptop—the token remains valid until expiry. | Adopted **Dual-Token Architecture**: Short-lived (15 min) Access Tokens verified mathematically in memory + Long-lived (30 day) Refresh Tokens verified against the DB. |
| **"Why do we need 3 separate token classes?"** | Confusion about having `TokenResponse`, `RefreshTokenRequest`, and `TokenPayload`. | Clarified **Inbound vs Outbound vs Internal**: `TokenResponse` is outbound to client; `RefreshTokenRequest` is inbound body to `/refresh`; `TokenPayload` validates raw decoded JWT dictionaries. |
| **OAuth vs `password_hash` Database Constraint** | Google OAuth never provides user passwords. Current `models/user.py` has `password_hash: nullable=False`, which crashes OAuth signups. | Recognized that `password_hash` must become `nullable=True` (or use a separate `oauth_accounts` table) to support OAuth and email/password side by side. |
| **"WTF is a Connection Pool? Does idle state cost money?"** | Doubts about what connections physically are and whether keeping connections open drains cloud budget. | Demystified: Connections are real TCP network sockets. In PostgreSQL, each socket reserves 5–15MB of RAM. `pool_pre_ping=True` does not cost extra money and only tests the socket with a 0.05ms `SELECT 1` when a request arrives. |
| **The FastAPI `async def` Trap** | Writing `async def` on routes using synchronous `psycopg2` freezes the single-threaded asyncio event loop on slow queries. | Clarified that synchronous SQLAlchemy routes should use standard `def`, allowing FastAPI to automatically run them on separate threadpool workers. |
| **Bcrypt Salt & One-Way Blender** | Misconception that passwords are "encrypted" and confusion over where the salt is stored in the DB. | Clarified that hashing is one-way (unreversible) and bcrypt automatically embeds the salt directly inside the 60-character hash string. |
| **`os.getenv()` Type Trap** | `os.getenv()` always returns `str`, which crashes `timedelta(minutes=...)` with `TypeError`, and improper parenthesis placement treated the default as an `int(x, base)` base. | Corrected to `int(os.getenv("KEY", default_val))` so defaults live inside `getenv` and are cast to numbers. |
| **In-Place Dictionary Mutation (`data.copy()`)** | Modifying input dictionary arguments directly causes unexpected side-effects across caller scopes. | Enforced `to_encode = data.copy()` in token generators to keep functions pure and prevent argument mutation. |

---

## 4. Current Repository Status

| File | Status | Notes |
| :--- | :--- | :--- |
| [schema/user.py](file:///home/shreyes/personal_finance_intelligence/app/backend/schema/user.py) | **Complete** | All registration, login, token, and user DTOs defined. |
| [database/database.py](file:///home/shreyes/personal_finance_intelligence/app/backend/database/database.py) | **Complete** | `create_engine` configured with `pool_pre_ping=True`. |
| [database/dependencies.py](file:///home/shreyes/personal_finance_intelligence/app/backend/database/dependencies.py) | **Complete** | `get_db()` typed and managing session lifecycle. |
| [config.py](file:///home/shreyes/personal_finance_intelligence/app/backend/config.py) | **Complete** | Database and JWT settings configured with safe fallbacks. |
| [main.py](file:///home/shreyes/personal_finance_intelligence/app/backend/main.py) | **Needs 1 small tweak** | Ready; needs a top-level `@app.get("/health")` endpoint added. |
| [routes/auth.py](file:///home/shreyes/personal_finance_intelligence/app/backend/routes/auth.py) | **Skeleton ready** | Route structure defined with prefix and tags; waiting for service layer. |
| [utils/security.py](file:///home/shreyes/personal_finance_intelligence/app/backend/utils/security.py) | **Complete** | Password hashing/verification, token minting, and `decode_token` complete. |
| `app/backend/services/` | **Pending** | Needs `auth_service.py` to hold business logic. |

---

## 5. What Else Can Be Done: Actionable Roadmap

Following our established sequence, here are the concrete upcoming tasks:

```
[Step 4: Security Utilities] (COMPLETE)
   ├── 4.1: Password hashing (hash_password, verify_password) -> [DONE]
   ├── 4.2: JWT minting (create_access_token, create_refresh_token) -> [DONE]
   └── 4.3: JWT decoding & verification (decode_token) -> [DONE]
       │
       ▼
[Step 5: Authentication Service] Implement services/auth_service.py (NEXT)
   ├── 5.1: Duplicate email check
   ├── 5.2: User entity creation & password hash storage
   └── 5.3: User credential authentication & token generation
       │
       ▼
[Step 6: Endpoints] Wire routes/auth.py
   ├── 6.1: Real POST /auth/register
   ├── 6.2: Real POST /auth/login
   └── 6.3: Real POST /auth/refresh
       │
       ▼
[Step 7: Auth Guard Dependency]
   └── Implement get_current_user dependency to protect future financial routes
       │
       ▼
[Step 8: Domain Modules]
   ├── Accounts (checking, savings, credit cards)
   ├── Categories & Subcategories
   ├── Transactions & Transfer pairs
   └── CSV Import & Net Worth derivation
```
