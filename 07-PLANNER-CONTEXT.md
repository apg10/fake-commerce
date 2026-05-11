# 07-PLANNER-CONTEXT.md

## Human/Local Model Collaboration

Human role: Project planner and review authority.

Local model role: Focused coding worker that implements scoped microtasks, runs validation, updates allowed context files, and commits only after tests pass.

Cloud model role: Reviewer, architect, prompt designer, and quality-control layer that audits worker output before the next task or push.

## Safe Coding Patterns

- Work through small backend/frontend microtasks.
- Each task must define allowed files, forbidden files, validation command, and commit rule.
- Run tests before claiming success.
- Commit only after validation passes.
- Never use `git add .`.
- Never modify files outside the allowed task scope.
- Do not mark future tasks as complete.
- Do not write speculative status in context files.
- Stop immediately if tests fail or the working tree is dirty unexpectedly.
- Backend work must stay under BE-* tasks.
- Frontend work must stay under FE-* tasks.
- Do not start database, cart, order, payment, or frontend work until the corresponding task is explicitly assigned.

## Current Backend Capabilities

- Health endpoint:
  - `GET /health` → `200 {"status": "ok"}`

- Product schemas:
  - `ProductBase`
  - `ProductCreate`
  - `ProductUpdate`
  - `ProductRead`

- Product API:
  - `POST /products` → create product, `201`
  - `GET /products` → list products
  - `GET /products/{product_id}` → retrieve product, `200/404`
  - `PATCH /products/{product_id}` → partial update, `200/404/422`
  - `DELETE /products/{product_id}` → hard delete, `204/404`

- Product list features:
  - `is_active` filtering
  - `limit` pagination parameter, validated from 1 to 100
  - `offset` pagination parameter, validated as `>= 0`

- Category schemas:
  - `CategoryBase`
  - `CategoryCreate`
  - `CategoryUpdate`
  - `CategoryRead`

- Category API:
  - `POST /categories` → create category, `201`
  - `GET /categories` → list categories
  - `GET /categories/{category_id}` → retrieve category, `200/404`
  - `PATCH /categories/{category_id}` → partial update, `200/404/422`
  - `DELETE /categories/{category_id}` → hard delete, `204/404`

- Category update behavior:
  - Uses `CategoryUpdate`
  - Uses `model_dump(exclude_unset=True)`
  - Preserves omitted fields
  - Rejects empty name through Pydantic validation

- Storage:
  - In-memory only for routes
  - SQLAlchemy installed and configured
  - SQLite configured (backend/app/db/session.py)
  - engine, SessionLocal, get_db available
  - Smoke tests pass (backend/tests/test_db_session.py)
  - No tables or models yet
  - No tables or models in production
  - Not wired into main.py or routes
  - No persistence
  - No service layer
  - No repository layer
  - .gitignore updated (REPO-A2)
  - Declarative base available: backend.app.db.base.Base
  - Product SQLAlchemy model available: backend.app.models.product.Product
  - Category SQLAlchemy model available: backend.app.models.category.Category
  - No tables created in production.

## Current Validation Status

Latest known validation: **92 passed in 0.82s** (python -m pytest backend/tests -q)

### Completed Tasks

- BE-005-A3: Category SQLAlchemy model added. python -m pytest backend/tests -q → 86 passed. ✅
- BE-005-A4: Model metadata sanity tests added (6 tests). python -m pytest backend/tests -q → 92 passed. ✅

### Next Recommended Task

- Assign next task from task queue.