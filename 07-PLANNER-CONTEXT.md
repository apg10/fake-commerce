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