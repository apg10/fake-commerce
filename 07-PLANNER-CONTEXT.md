# 07-PLANNER-CONTEXT.md
## Human/Local Model Collaboration
Human role: Project planner and review authority
Local model: Backend and frontend worker that creates safe example files and runs safe commands
Cloud model: Reviewer that evaluates worker output before allowing the local model to commit

## Safe Coding Patterns
- Use local backend and frontend tests to validate files worked on
- Create worker safe output example files that match the allowed task scope
- Stop after the current task scope is complete and report honestly
- Never write any backend code until BE-00x is completed and validated
- Never write any frontend code until FE-00x is completed and validated
- Use the safe local model task queue and never touch files outside it

## Current Backend Capabilities
- Health endpoint: GET /health → 200 {status: ok}
- Products CRUD: POST /products (201), GET /products (is_active filter, limit/offset pagination), GET /products/{product_id} (200/404), PATCH /products/{product_id} (200/404/422), DELETE /products/{product_id} (204/404)
- Category schemas: CategoryBase, CategoryCreate, CategoryUpdate, CategoryRead (name min_length=1, optional fields, from_attributes=True)
- Category routes: POST /categories (201), GET /categories (200), GET /categories/{category_id} (200/404), PATCH /categories/{category_id} (200/404/422), DELETE /categories/{category_id} (204/404)
- Category API now supports create, list, retrieve, partial update, and delete.
- PATCH uses CategoryUpdate model_dump(exclude_unset=True) for partial updates
- In-memory storage only, no database
- Pydantic v2 schemas: ProductCreate, ProductUpdate, ProductRead with validation (price > 0, stock >= 0, name min_length=1)
- GET /products supports optional is_active (bool), limit (1-100), offset (>=0) query parameters

## Current Risks
- In-memory storage: data lost on restart
- No response metadata (total count) for pagination
- No soft delete (hard delete only)
- No cart, order, or payment support yet
- No DELETE endpoint for categories yet

## Next Recommended Microtask
- BE-003-A2: Category basic in-memory routes (POST /categories, GET /categories, GET /categories/{category_id})

## Tasks That Should NOT Be Started Yet
- BE-002-A8 or beyond (not defined)
- BE-003-A3 (patch/delete) - must wait for BE-003-A2 to complete first
- Tasks that depend on categories not being implemented (cart, orders with categories, etc.)
- BE-100 cart, BE-110 orders, BE-120 payments

## Blockers
- None
