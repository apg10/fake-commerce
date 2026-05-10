# Project Overview

## 1. Project Overview

- **Name**: fake‑commerce‑backend
- **Purpose**: Controlled full‑stack fake e‑commerce project used for testing local coding models with OpenCode/Ollama.
- **Backend‑first**: Backend logic exists first and the frontend is added later.
- **Micro‑task discipline**: Each change is a small, well‑scoped task with explicit allowed/forbidden files, a validation command, and a commit rule.

## 2. Current Tech Stack

- FastAPI
- Python 3.11 (Pydantic v2)
- Pytest
- SQLAlchemy (planned for later stages)
- SQLite (planned for later stages)
- React/Vite (planned for later stages)
- Google Stitch (visual/UI reference for future stages)
- Mock payments first – Stripe/Wompi/PayU will be added sequentially.

## 3. Current Backend State

- **BE‑001**: Base FastAPI application with a `/health` endpoint that returns `{"status":"ok"}`.
- **Pydantic schemas** for products already exist in `backend/app/schemas/product.py` and are fully tested in `backend/tests/test_product_schemas.py`.
- **Routes**: The product route skeleton (`backend/app/routes/products.py`) is present but may still be incomplete or subject to change depending on the current task.
- **Tests**: `backend/tests/test_product_routes.py` tests the product API; they currently pass.

## 4  Working Method

The project progresses through small micro‑tasks. Each micro‑task specifies:

1. **Task ID** – a unique identifier.
2. **Goal** – what the task is trying to achieve.
3. **Allowed files** – the files a worker may modify or create.
4. **Forbidden files** – files that must remain untouched.
5. **Validation command** – the command a worker must run to confirm the task.
6. **Commit rule** – conditions under which a commit is allowed.

After performing the work, the worker returns a final response that follows the prescribed format used for reviews, audits, and hand‑offs.

## 5. Worker Rules

- **No over‑construction** – do not add functionality beyond what the task explicitly requires.
- **Do not advance future phases** – keep the architecture as defined by the current task.
- **File scope** – only files listed as allowed may be modified.
- **No documentation edits** unless the task says so.
- **No WebFetch/WebSearch** – all information must come from the repository.
- **Test validation only** – a worker may claim success only after running the validation command.
- **Commit only when permitted** – obey the commit rule and run tests first.
- **No `git add .` or `git push`.**

## 6. Current Model Workflow

- **Qwen 3.6 35B (A3B Q4_K_M)** – performs coding micro‑tasks.
- **Qwen 14B** – produces documentation, reports, hand‑offs, and audits.
- **GPT‑OSS** – carries out diff audits and project‑report building.
- **Codex/GPT** – handles architecture decisions, prompt design, and final reviews.

## 7 Validation Standard 

The primary validation command :
```
python -m pytest backend/tests -q
```
- **All tests must pass** before a commit is allowed.
- **Dependency/environment issues** cause a failure until resolved.
- `/health` must remain functional and unchanged.

## 8‐‐ Git Standard

- **Commit rules**‑ Only‑to‑the‑specified‑files.
- **Commit must

**…