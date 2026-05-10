# 00-PLAN.md

# Master Plan — Modern E-commerce Platform

## 1. Product Goal

Build a modern full-stack e-commerce platform with a clean FastAPI backend, React/Vite frontend, Google Stitch-driven visual direction, cart, checkout, order flow, payment architecture, and a basic admin panel.

The MVP must be good enough for:

- Professional demo.
- Portfolio presentation.
- Reuse as a base for real small-business e-commerce projects.
- Future payment gateway integration.
- Future adaptation into client-specific stores.

The system must be developed incrementally through small, bounded tasks.

---

## 2. Base Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite for local development
- Pydantic
- Pytest

### Frontend

- React
- Vite
- React Router
- Modern CSS or Tailwind if explicitly introduced later
- Components guided by Google Stitch design references

### Design

- Google Stitch for visual direction
- Internal design tokens for colors, spacing, typography, cards, buttons, product grids, and checkout flow

### Payments

- Mock payment provider first
- Placeholder architecture for real providers later
- Possible future providers: Stripe, Wompi, PayU
- No real credentials during MVP development

---

## 3. Operating Model

The project must be developed with a planner-worker-reviewer loop.

### Human / Chat Planner

The human user and the cloud planning chat define:

- Product direction
- Architecture
- Development phases
- Task boundaries
- Allowed files
- Forbidden scope
- Acceptance criteria
- Review decisions

### Local Qwen Worker

The local Qwen model executes only one bounded task at a time.

The local worker must:

- Read local context first when instructed.
- Modify only allowed files.
- Avoid future phases.
- Avoid external research.
- Avoid WebFetch and WebSearch.
- Avoid invented validation.
- Run tests when possible.
- Report honestly.
- Stop after the assigned task.

### Review Loop

After each task:

1. Qwen reports files changed, tests run, result, blockers, and next task.
2. The user brings the result back to chat.
3. The chat reviews scope, quality, validation, and next step.
4. The next task is approved only after review.

---

## 4. Development Rule

Never ask Qwen to build the whole e-commerce at once.

Bad instruction:

```text
Build the complete e-commerce.
```

Good instruction:

```text
Execute BE-001 only. Create the backend foundation and /health endpoint. Do not implement products, cart, orders, payments, frontend, or admin.
```

Each task must be small enough to inspect and validate.

---

# PHASE 0 — Context and Guardrails

## Goal

Prepare the repository so the local model can work safely and consistently.

## Main Files

- 00-PLAN.md
- 01-HANDOFF.md
- 03-WORKER-PROTOCOL.md
- 04-UI-BRIEF.md
- 07-PLANNER-CONTEXT.md
- 09-LOCAL-MODEL-TASK-QUEUE.md
- 10-AGENT-COMMUNICATION-PROTOCOL.md
- 13-CLOUD-DECISION.md

## Expected Result

The repository contains persistent context explaining:

- What is being built.
- What the MVP includes.
- What is out of scope.
- How tasks are assigned.
- How Qwen must behave.
- How validation must be reported.
- When cloud/planner review is required.

## Status

Context setup is in progress.

The task queue file has been corrected and should be used as the source of truth for scoped local-model tasks.

---

# PHASE 1 — Backend Foundation

## Goal

Create the minimal FastAPI backend foundation.

## Main Task

### BE-001 — Backend Foundation with /health Endpoint

Expected files:

- backend/app/main.py
- backend/app/core/config.py
- backend/app/routes/health.py
- backend/tests/test_health.py
- requirements.txt
- pyproject.toml

Required behavior:

```text
GET /health -> {"status": "ok"}
```

Validation:

- Run pytest if dependencies are available.
- Confirm /health response through test client.

Forbidden in this phase:

- Products
- Cart
- Orders
- Payments
- Frontend
- Admin
- Authentication

Exit criteria:

- Backend imports without errors.
- /health test passes.
- Backend structure is clean and minimal.

---

# PHASE 2 — Product Catalog Backend

## Goal

Create a functional product catalog backend.

## Main Tasks

### BE-002 — Product Model, Schemas, CRUD and Routes

Expected files:

- backend/app/models/product.py
- backend/app/schemas/product.py
- backend/app/crud/product.py
- backend/app/routes/products.py

Product fields:

- id
- name
- slug
- description
- price
- stock
- image_url
- category
- is_active
- created_at
- updated_at

Expected endpoints:

- POST /products
- GET /products
- GET /products/{id}
- GET /products/slug/{slug}
- PATCH /products/{id}
- DELETE /products/{id}

### BE-003 — Product Tests and Seed Data

Required tests:

- Create product
- List products
- Get product by id
- Reject negative price
- Reject negative stock
- Handle inactive product

Exit criteria:

- Product tests pass.
- No cart or order logic exists yet.

---

# PHASE 3 — Frontend Foundation

## Goal

Create a clean React/Vite frontend foundation.

## Main Task

### FE-001 — React/Vite Foundation

Expected structure:

- frontend/src/main.jsx
- frontend/src/App.jsx
- frontend/src/routes/
- frontend/src/pages/
- frontend/src/components/
- frontend/src/services/api/
- frontend/src/styles/

Required behavior:

- Basic app shell.
- Initial routing structure.
- Base layout.
- API client placeholder.
- Global styles.
- Home/store placeholder.

Forbidden in this phase:

- Real cart
- Real checkout
- Payments
- Advanced admin

Exit criteria:

- Frontend starts or validates if dependencies are available.
- Structure is ready for Stitch-inspired UI.

---

# PHASE 4 — Google Stitch UI Direction

## Goal

Convert the visual direction from Google Stitch into reusable project guidance.

## Main Task

### UI-001 — Stitch Prompts and Design Tokens

Expected files/directories:

- 04-UI-BRIEF.md
- design/stitch/prompts/
- design/stitch/screens/
- design/tokens/

Must define:

- Visual style
- Colors
- Spacing
- Typography
- Product cards
- Storefront layout
- Checkout feel
- Admin feel

Exit criteria:

- UI direction exists before heavy UI implementation.
- Stitch references are organized.
- No generated Stitch export files are treated as source code unless explicitly reviewed.

---

# PHASE 5 — Storefront

## Goal

Create the customer-facing shopping experience.

## Main Tasks

### FE-002 — Product Listing

Must implement:

- Product grid
- Product card
- Loading state
- Empty state
- API client integration or controlled placeholder

### FE-003 — Product Detail Page

Must implement:

- Product detail page
- Product image
- Product price
- Product description
- Stock display
- Add-to-cart placeholder

Exit criteria:

- User can browse products visually.
- Cart does not need to be fully functional yet.

---

# PHASE 6 — Cart

## Goal

Create a functional cart flow.

## Main Tasks

### CART-001 — Cart Backend

Must implement:

- Add item
- Update quantity
- Remove item
- Cart totals
- Product existence validation
- Quantity > 0 validation
- Stock validation

### CART-002 — Cart Frontend

Must implement:

- Cart page or drawer
- Quantity controls
- Remove item
- Subtotal
- Total
- Checkout navigation

Exit criteria:

- User can add products and see totals.
- Backend prevents invalid quantities and stock overflow.

---

# PHASE 7 — Orders

## Goal

Convert cart into order.

## Main Task

### ORDER-001 — Orders Backend

Must implement:

- Order model
- OrderItem model
- Create order from cart
- Validate stock before order creation
- Freeze price_at_purchase
- Reduce stock after valid order
- Order statuses: pending, paid, cancelled, failed

Exit criteria:

- Order can be created from cart.
- Stock is reduced correctly.
- Purchase price is frozen.

---

# PHASE 8 — Payments

## Goal

Create clean payment architecture before integrating real providers.

## Main Tasks

### PAY-001 — Mock Payment Provider

Must implement:

- Payment model
- Payment provider interface
- Mock provider
- Start payment
- Simulate success/failure
- Update order/payment status

### PAY-002 — Real Payment Provider Placeholder Architecture

Expected files:

- backend/app/services/payments/base.py
- backend/app/services/payments/mock_provider.py
- backend/app/services/payments/stripe_provider.py
- backend/app/services/payments/wompi_provider.py
- docs/payments/

Rules:

- Do not use real credentials.
- Do not create .env files with real keys.
- Do not make real payment calls yet.
- Keep mock provider as default.

Exit criteria:

- The system can simulate payments.
- The architecture can accept a real provider later.

---

# PHASE 9 — Admin Panel

## Goal

Create a basic admin panel to operate the store.

## Main Task

### ADMIN-001 — Basic Admin Panel

Must implement:

- Admin dashboard shell
- Product list/admin table
- Order list/admin table
- Basic order status display
- Basic product management UI

Forbidden for now:

- Complex roles
- Real authentication
- Advanced analytics
- Multi-warehouse inventory

Exit criteria:

- Admin can view/manage basic products and orders.
- The panel is simple and functional.

---

# PHASE 10 — Hardening and Demo

## Goal

Make the project presentable.

## Main Tasks

### TST-001 — Strong Integration Tests

Must cover:

- Product flow
- Cart flow
- Order flow
- Stock validation
- Mock payment flow
- Critical frontend flows if available

### DOC-001 — README and Demo Flow

Must document:

- What the project is
- Stack
- How to run backend
- How to run frontend
- How to run tests
- Demo flow
- Payment mock flow
- Current limitations
- Future roadmap

Exit criteria:

- Project is demo-ready.
- README is clear.
- Core flows are tested or limitations are explicitly documented.

---

# Validation Strategy

Validation must be honest.

Qwen must never claim:

- Tests passed
- Server started
- Endpoint worked
- Build succeeded
- Payment worked
- Frontend rendered

unless the relevant command was actually run or the result was actually observed.

If validation was not run, Qwen must say so clearly.

Accepted validation examples:

```text
pytest
python -m pytest
npm test
npm run build
manual review
documentation-only task, no tests run
```

---

# Task Report Format

Every Qwen task must end with:

1. Files created or updated
2. What changed
3. Tests or commands run
4. Result
5. Blockers, if any
6. Recommended next task

---

# Current Next Task

After this plan is persisted, the next implementation task is:

```text
BE-001 — Backend foundation with /health endpoint
```

Before starting BE-001, confirm that:

- 00-PLAN.md exists.
- 09-LOCAL-MODEL-TASK-QUEUE.md exists.
- 03-WORKER-PROTOCOL.md exists.
- OpenCode is using the correct local model.
- WebFetch/WebSearch are not used.
