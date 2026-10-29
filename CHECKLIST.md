# 📋 Project Execution Checklist & Git Roadmap

This document is our living tracker. It breaks down all upcoming tasks into bite-sized steps with checkboxes and clearly indicates **when to commit and push to GitHub**.

---

## 🚀 Phase 1: Authentication & Security Foundation

### Part A: Foundation & Business Logic (Completed)
- [x] **Database Engine & Connection Pool** (`app/backend/database/database.py`)
- [x] **Session Dependency `get_db()` with generator lifecycle** (`app/backend/database/dependencies.py`)
- [x] **User SQLAlchemy ORM Model** (`app/backend/models/user.py`)
- [x] **Pydantic Validation Schemas / DTOs** (`app/backend/schema/user.py`)
- [x] **Password Hashing & Verification with Bcrypt** (`app/backend/utils/security.py`)
- [x] **JWT Minting & Decoding with Jose/HS256** (`app/backend/utils/security.py`)
- [x] **Auth Service: Registration & Login Business Logic** (`app/backend/services/auth_service.py`)

---

### Part B: Wire HTTP Endpoints & Verification (CURRENT MILESTONE)
- [x] **Step 6.1: Wire `POST /auth/register`** (`app/backend/routes/auth.py`)
  - Accept `RegisterRequest`, call `auth_service.register_user(db, request)`.
  - Handle duplicate email (`ValueError` -> `400 Bad Request`).
  - Return `201 Created` with `UserResponse`.
- [x] **Step 6.2: Wire `POST /auth/login`** (`app/backend/routes/auth.py`)
  - Accept `LoginRequest`, call `auth_service.authenticate_user(db, request)`.
  - Handle invalid credentials (`ValueError` -> `401 Unauthorized`).
  - Return `200 OK` with `TokenResponse` (`access_token`, `refresh_token`).
- [x] **Step 6.3: Implement `POST /auth/refresh`** (`app/backend/routes/auth.py`)
  - Add refresh logic to `auth_service.py`.
  - Validate refresh token, check `"type": "refresh"`.
  - Return fresh `TokenResponse` with a new access token.
- [x] **Step 6.4: Add Health Check Endpoint** (`app/backend/main.py`)
  - Add simple `@app.get("/health")` returning `{"status": "ok"}`.
- [x] **Step 6.5: End-to-End Smoke Test & Database Verification**
  - Applied Alembic migrations cleanly.
  - Verified Register -> Login -> Refresh against PostgreSQL with 100% success.

---

### 📦 GITHUB COMMIT MILESTONE 1 (Push to GitHub Here!)
> **Milestone Goal:** Complete, working Authentication Engine (Registration + Login + JWT Tokens).
>
> **Git Commands to Run:**
> ```bash
> # 1. Verify .env is NOT staged
> git status
> 
> # 2. Stage all completed code
> git add app/ CHECKLIST.md AUTH_PROGRESS_SUMMARY.md
> 
> # 3. Commit with clean conventional message
> git commit -m "feat(auth): complete user registration, login, and jwt dual-token endpoints"
> 
> # 4. Push to remote repository
> git push origin main
> ```

---

## 🛡️ Phase 2: Auth Guard & User Profile

- [ ] **Step 7.1: Implement `get_current_user` Dependency** (`app/backend/dependencies/auth.py`)
  - Extract Bearer token via `OAuth2PasswordBearer(tokenUrl="/auth/login")`.
  - Decode token, validate expiration and `sub` claim.
  - Query DB for user; raise `401 Unauthorized` if not found.
- [ ] **Step 7.2: Add Protected Route `GET /auth/me`**
  - Uses `Depends(get_current_user)`.
  - Returns current logged-in user profile.
- [ ] **Step 7.3: Add Password Reset / Change Endpoint** (Optional/Recommended)

---

### 📦 GITHUB COMMIT MILESTONE 2 (Push to GitHub Here!)
> **Milestone Goal:** Reusable Auth Guard dependency protecting private endpoints.
>
> **Git Commands:**
> ```bash
> git add app/ CHECKLIST.md
> git commit -m "feat(auth): add get_current_user auth guard and /auth/me endpoint"
> git push origin main
> ```

---

## 💰 Phase 3: Financial Domain (Accounts & Transactions)

- [ ] **Step 8.1: Bank Accounts Model & Schemas**
  - Types: Checking, Savings, Credit Card, Investment.
  - CRUD endpoints: `POST /accounts`, `GET /accounts`.
  - Ensure users can **only** view their own accounts (`user_id` scoping).
- [ ] **Step 8.2: Categories & Tags**
  - Income vs Expense categories (Groceries, Rent, Salary, Entertainment).
- [ ] **Step 8.3: Transactions Engine**
  - Inflows, Outflows, and Internal Account Transfers.
  - Running balance updates.
- [ ] **Step 8.4: CSV Bank Statement Importer**
  - Parse bank CSV files, de-duplicate transactions, and auto-categorize.

---

### 📦 GITHUB COMMIT MILESTONE 3 (Push to GitHub Here!)
> **Milestone Goal:** Core Financial Management MVP (Accounts, Transactions, CSV Import).
>
> **Git Commands:**
> ```bash
> git add app/ CHECKLIST.md
> git commit -m "feat(finance): add accounts, transactions, and csv import engine"
> git push origin main
> ```

---

## 📊 Phase 4: Intelligence & Analytics

- [ ] **Step 9.1: Net Worth Calculation Engine** (Assets minus Liabilities).
- [ ] **Step 9.2: Monthly Cash Flow Analytics** (Total Income vs Total Expenses).
- [ ] **Step 9.3: Spending Breakdown by Category** (Pie chart / JSON aggregation).

---

## ⚠️ Pre-Push Git Safety Checklist (Always Check!)
1. Run `git status` — confirm `.env` is **never** listed under staged changes.
2. Confirm Docker PostgreSQL is running without schema errors.
3. Keep commit messages clear using conventional prefixes (`feat:`, `fix:`, `docs:`, `refactor:`).
