# 13-CLOUD-DECISION.md
## Scope Validation
- Local model can modify safe backend and frontend files if they match the current allowed task from the safe local model task queue
- Local model can modify a few safe test files when explicitly allowed by the human, otherwise run backend tests and frontend component tests as needed
- Local model can modify safe UI files if they match the current allowed task
- Local model must stop and ask for cloud review before writing payment gateway code, payment confirmation flows, generated secret files, backend config files, and payment-related files
- Local model can create or update safe frontend and backend files that are explicitly allowed by the current safe local model task
- Local model can modify project context and worker safe output example files
- Local model must not modify backend migrations, frontend package.json, design/stitch files, secrets files, and payment files unless explicitly instructed during payment integration phase