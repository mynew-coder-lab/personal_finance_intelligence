# Personal Finance Intelligence — Project Execution Checklist

> **Purpose:** This document is the single source of truth for the application's implementation roadmap.
>
> The AI coding agent must follow this checklist in order. It must not independently introduce, skip, or reprioritize product features.
>
> **Implementation rule:** Complete a task → Verify it → Update documentation → Update this checklist → Move to the next task.

---

# Project Execution Rules

These rules apply to every phase.

## 1. Implementation workflow

For every numbered implementation step, follow this sequence:

1. **Inspect:** Read the relevant existing code and understand its dependencies.
2. **Implement:** Write the actual feature using the existing architecture.
3. **Verify:** Run tests and verify successful, unsuccessful, and edge-case scenarios.
4. **Fix:** Resolve implementation or test failures before proceeding.
5. **Document:** Update all four documentation files.
6. **Track:** Update this checklist to reflect the actual completion status.
7. **Summarise:** Report what changed, what was tested, and what comes next.

Do not move to the next numbered step until the current step is implemented and verified.

## 2. Mandatory documentation updates

After every completed implementation step, update:

| File | Responsibility |
|---|---|
| `docs/LEARNING_NOTES.md` | Explain what was implemented, why, how it works, execution flow, affected files, and design decisions. |
| `docs/TERMINOLOGY.md` | Explain new technical concepts and how they are used in this project. |
| `docs/PRACTICE.md` | Add conceptual, code-reading, coding, debugging, and modification exercises at Easy, Medium, and Hard levels. |
| `docs/PROJECT_STATUS.md` | Track completed, in-progress, pending, and unverified work, test results, known issues, and next steps. |

Do not recreate these files. Update their existing contents.

Exercises must be based on the actual implemented code. Do not provide solutions unless requested.

## 3. Technical constraints

- Backend: Python + FastAPI.
- Database: PostgreSQL.
- ORM: SQLAlchemy 2.x ORM.
- Validation: Pydantic.
- Migrations: Alembic.
- Authentication: Existing bcrypt and JWT implementation.
- Containerization: Existing Docker configuration.

Rules:

- Preserve the existing modular architecture.
- Do not replace SQLAlchemy ORM with SQLAlchemy Core.
- Reuse existing components wherever possible.
- Do not introduce unnecessary dependencies.
- Do not delete existing migrations.
- Do not commit secrets or `.env` files.
- Do not claim a feature or test is complete unless it has actually been verified.
- Do not create placeholder implementations and mark them complete.

## 4. Scope control

The following roadmap defines the planned MVP.

Do not independently add:
- Machine learning models.
- AI financial assistants.
- Investment portfolio tracking.
- Budget management.
- Recurring payment management.
- Bank API integrations.
- Frontend dashboards.
- Additional analytics features.

These are outside the current checklist scope. They may be considered in a future roadmap, but must not be implemented without explicit approval.

If a technical dependency is genuinely necessary but missing from the checklist, explain why and request approval before expanding the scope.

## 5. Git safety

Git milestones are checkpoints for reviewing and preparing commits.

- Inspect `git status` before staging.
- Never stage `.env`, credentials, or secrets.
- Use conventional commit messages.
- Never push to GitHub without explicit permission.
- Ask before destructive database operations, database resets, or dropping tables.

---

# Phase 1: Authentication & Security Foundation

<badge color="success">Completed</badge>

## Part A — Foundation & Business Logic

- [x] **Step 1.1: Database Engine & Connection Pool**
  - File: `app/backend/database/database.py`
  - Configure PostgreSQL connection and SQLAlchemy engine.

- [x] **Step 1.2: Database Session Dependency**
  - File: `app/backend/database/dependencies.py`
  - Implement `get_db()` with proper generator lifecycle.

- [x] **Step 1.3: User ORM Model**
  - File: `app/backend/models/user.py`
  - Define the user database model.

- [x] **Step 1.4: User Validation Schemas**
  - File: `app/backend/schema/user.py`
  - Define Pydantic request and response schemas.

- [x] **Step 1.5: Password Hashing & Verification**
  - File: `app/backend/utils/security.py`
  - Implement bcrypt hashing and verification.

- [x] **Step 1.6: JWT Minting & Decoding**
  - File: `app/backend/utils/security.py`
  - Implement JWT generation and decoding using Jose/HS256.

- [x] **Step 1.7: Authentication Service**
  - File: `app/backend/services/auth_service.py`
  - Implement registration and login business logic.

## Part B — HTTP Endpoints & Verification

- [x] **Step 2.1: User Registration Endpoint**
  - File: `app/backend/routes/auth.py`
  - Endpoint: `POST /auth/register`
  - Accept `RegisterRequest`.
  - Call `auth_service.register_user(db, request)`.
  - Handle duplicate email with `400 Bad Request`.
  - Return `201 Created` with `UserResponse`.

- [x] **Step 2.2: User Login Endpoint**
  - File: `app/backend/routes/auth.py`
  - Endpoint: `POST /auth/login`
  - Accept `LoginRequest`.
  - Call `auth_service.authenticate_user(db, request)`.
  - Handle invalid credentials with `401 Unauthorized`.
  - Return `200 OK` with `TokenResponse`.
  - Include `access_token` and `refresh_token`.

- [x] **Step 2.3: Refresh Token Endpoint**
  - File: `app/backend/routes/auth.py`
  - Endpoint: `POST /auth/refresh`
  - Validate the refresh token.
  - Validate the `"type": "refresh"` claim.
  - Return a fresh `TokenResponse` with a new access token.

- [x] **Step 2.4: Health Check Endpoint**
  - File: `app/backend/main.py`
  - Endpoint: `GET /health`
  - Return `{"status": "ok"}`.

- [x] **Step 2.5: Authentication Smoke Test**
  - Apply Alembic migrations.
  - Verify registration, login, and refresh against PostgreSQL.
  - Confirm the complete authentication flow works.

## Git Milestone 1 — Authentication Engine

<badge color="success">Completed</badge>

Goal: Working registration, login, and JWT token endpoints.

Suggested commit:

`feat(auth): complete registration, login, and jwt token endpoints`

---

# Phase 2: Authentication Guard & User Profile

<badge color="info">Next implementation phase</badge>

**Goal:** Establish reusable authentication protection for all future private endpoints.

- [x] **Step 3.1: Implement `get_current_user` Dependency**
  - File: `app/backend/database/dependencies.py`
  - Use `OAuth2PasswordBearer(tokenUrl="/auth/login")`.
  - Extract the Bearer token from the request.
  - Decode the JWT using the existing security utilities.
  - Validate token expiration.
  - Validate the `sub` claim.
  - Retrieve the corresponding user from PostgreSQL.
  - Return the authenticated user.
  - Raise `401 Unauthorized` for invalid, expired, malformed, or unrecognized tokens.
  - Ensure the dependency can be reused by future protected endpoints.

- [x] **Step 3.2: Implement Protected User Profile Endpoint**
  - File: `app/backend/routes/auth.py`
  - Endpoint: `GET /auth/me`
  - Protect the endpoint using `Depends(get_current_user)`.
  - Return the authenticated user's profile.
  - Do not allow users to retrieve another user's profile.
  - Use the existing response schema where appropriate.

- [x] **Step 3.3: Verify Authentication Guard**
  - Test a valid access token.
  - Test a missing token.
  - Test an invalid token.
  - Test an expired token.
  - Test a token with an invalid or missing subject.
  - Test a token referring to a nonexistent user.
  - Verify `/auth/me` returns only the authenticated user's information.

- [ ] **Step 3.4: Password Reset / Change**
  - Status: Optional / Recommended.
  - First inspect the existing authentication implementation.
  - Identify whether the requirement is password change for authenticated users or password recovery.
  - Do not implement email-based recovery or introduce additional infrastructure without approval.
  - Implement only after clarifying the required scope.

## Git Milestone 2 — Reusable Authentication Guard

Goal: Complete and verify the reusable authentication dependency and protected `/auth/me` endpoint.

Suggested commit:

`feat(auth): add current user dependency and protected profile endpoint`

---

# Phase 3: Financial Domain — Accounts & Transactions

**Goal:** Build the core financial management functionality.

All financial records must be associated with the authenticated user. Users must never access or modify another user's financial data.

## Step 4.1: Bank Accounts Model & Schemas

- [x] Inspect existing account ORM model, schemas, migrations, and database relationships.
- [x] Support the following account types:
  - Checking
  - Savings
  - Credit Card
  - Investment
- [x] Implement `POST /accounts`.
  - Create a financial account for the authenticated user.
  - Validate incoming data.
  - Associate the account with the current user's ID.
- [x] Implement `GET /accounts`.
  - Return accounts belonging only to the authenticated user.
- [x] Ensure ownership checks are enforced at the database query/service layer.
- [x] Handle invalid input and database errors appropriately.
- [x] Add tests for account creation, retrieval, validation, and cross-user access.

**Completion criteria:**
- Users can create accounts.
- Users can retrieve their own accounts.
- Users cannot access another user's accounts.
- Relevant tests pass.

## Step 4.2: Categories & Tags

- [x] Inspect existing category ORM model and database relationships.
- [x] Support income and expense categories.
- [x] Include the planned example categories:
  - Groceries
  - Rent
  - Salary
  - Entertainment
- [x] Define the relationship between categories and transactions.
- [x] Ensure category ownership or shared-category behaviour is explicitly defined before implementation.
- [x] Prevent invalid category assignments.
- [x] Add appropriate validation and tests.

**Completion criteria:**
- Income and expense categories can be represented.
- Categories can be associated with transactions.
- Category assignment is validated.
- Relevant tests pass.

## Step 4.3: Transactions Engine

- [ ] Inspect existing transaction ORM model and relationships.
- [ ] Implement transaction creation and retrieval functionality.
- [ ] Support:
  - Inflows (money received).
  - Outflows (money spent).
  - Internal account transfers.
- [ ] Associate transactions with the authenticated user.
- [ ] Validate account ownership before allowing a transaction.
- [ ] Validate transaction amounts and required fields.
- [ ] Implement running balance updates.
- [ ] Ensure transfers correctly affect both source and destination accounts.
- [ ] Use database transactions where multiple related operations must succeed or fail together.
- [ ] Prevent inconsistent balances and partial transfers.
- [ ] Add tests for income, expenses, transfers, invalid accounts, and cross-user access.

**Completion criteria:**
- Income and expense transactions work.
- Internal transfers work.
- Account balances are updated consistently.
- Invalid transactions are rejected.
- Relevant tests pass.

## Step 4.4: CSV Bank Statement Importer

- [ ] Inspect the transaction creation and category assignment logic before implementation.
- [ ] Implement CSV file parsing.
- [ ] Validate file format and required columns.
- [ ] Parse transaction dates, amounts, descriptions, and available metadata.
- [ ] Associate imported transactions with the correct authenticated user's account.
- [ ] Prevent duplicate transactions.
- [ ] Implement auto-categorization using the existing category system.
- [ ] Handle malformed rows and invalid values safely.
- [ ] Report successful imports, skipped duplicates, and rejected rows.
- [ ] Add tests for valid CSV files, malformed files, duplicate records, and invalid data.

**Completion criteria:**
- Valid CSV files can be imported.
- Duplicate transactions are handled safely.
- Imported records belong to the correct user and account.
- Auto-categorization works using the existing categories.
- Import errors are handled predictably.
- Relevant tests pass.

## Git Milestone 3 — Core Financial Management MVP

Goal: Complete the following:

- Account management.
- Categories and tags.
- Transactions and internal transfers.
- CSV statement importing.

Suggested commit:

`feat(finance): implement accounts transactions and csv importer`

---

# Phase 4: Intelligence & Analytics

**Goal:** Provide useful financial summaries using the existing financial data.

Do not introduce machine learning or AI features in this phase.

## Step 5.1: Net Worth Calculation Engine

- [ ] Inspect account types and transaction balance logic.
- [ ] Define how assets and liabilities are represented using existing account data.
- [ ] Calculate net worth:

  `Net Worth = Total Assets - Total Liabilities`

- [ ] Ensure account balances are interpreted consistently.
- [ ] Scope calculations to the authenticated user.
- [ ] Handle empty accounts and zero balances.
- [ ] Add tests for positive, negative, and zero net worth scenarios.

**Completion criteria:**
- Net worth is calculated from the user's financial data.
- Assets and liabilities are treated consistently.
- Users cannot retrieve another user's net worth.
- Relevant tests pass.

## Step 5.2: Monthly Cash Flow Analytics

- [ ] Implement monthly income aggregation.
- [ ] Implement monthly expense aggregation.
- [ ] Calculate total income versus total expenses.
- [ ] Support the required monthly grouping.
- [ ] Ensure calculations use the correct transaction dates and types.
- [ ] Scope results to the authenticated user.
- [ ] Add tests for different months, empty periods, and mixed transactions.

**Completion criteria:**
- Monthly income is calculated correctly.
- Monthly expenses are calculated correctly.
- Results are isolated by user.
- Relevant tests pass.

## Step 5.3: Spending Breakdown by Category

- [ ] Aggregate expense transactions by category.
- [ ] Calculate category-wise spending totals.
- [ ] Provide JSON output suitable for pie-chart visualization.
- [ ] Ensure the aggregation uses the correct date period.
- [ ] Scope results to the authenticated user.
- [ ] Handle transactions without categories appropriately.
- [ ] Add tests for multiple categories, empty results, and date filtering.

**Completion criteria:**
- Category-wise expense aggregation works.
- Output is suitable for pie-chart visualization.
- Results are isolated by user.
- Relevant tests pass.

---

# Final Verification & Project Completion

- [ ] Verify all completed API endpoints.
- [ ] Verify authentication and authorization.
- [ ] Verify cross-user data isolation.
- [ ] Verify account balance consistency.
- [ ] Verify transaction and transfer correctness.
- [ ] Verify CSV import and duplicate handling.
- [ ] Verify analytics calculations.
- [ ] Run the complete automated test suite.
- [ ] Verify Alembic migrations from a clean test database.
- [ ] Verify Docker-based application startup.
- [ ] Review error handling and validation.
- [ ] Review environment-variable and secret handling.
- [ ] Update all four documentation files.
- [ ] Update this checklist to reflect the actual final state.

---

# Implementation Progress Tracking

The coding agent must keep these files synchronized:

| File | Purpose |
|---|---|
| `CHECKLIST.md` | Authoritative feature roadmap and completion tracking. |
| `docs/LEARNING_NOTES.md` | Detailed learning material for implemented functionality. |
| `docs/TERMINOLOGY.md` | Technical vocabulary and explanations. |
| `docs/PRACTICE.md` | Exercises based on the actual implementation. |
| `docs/PROJECT_STATUS.md` | Current implementation status, tests, issues, and next steps. |

## Definition of Done

A numbered checklist item can be marked `[x]` only when:

1. The feature has been implemented.
2. Its relevant tests have been executed.
3. Identified failures have been fixed or explicitly documented.
4. Its actual behaviour has been verified.
5. All four documentation files have been updated.
6. The project status reflects the real implementation state.

If any condition is incomplete, leave the checkbox unchecked.

---

# Next Action for the Coding Agent

The initial codebase inspection and creation of the four documentation files have already been completed.

Do not repeat the initial analysis.

1. Inspect the current codebase and existing documentation.
2. Confirm the status of Phase 1.
3. Start with **Phase 2 — Step 3.1: Implement `get_current_user` Dependency** if it is not already complete.
4. Follow the implementation workflow.
5. Continue through the numbered checklist in order.
6. Do not implement features outside this roadmap without approval.

**The roadmap decides WHAT to build. The existing codebase decides HOW to build it. The four documentation files explain WHAT was actually built and help the developer understand it.**