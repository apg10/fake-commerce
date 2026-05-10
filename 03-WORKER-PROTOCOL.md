# 03-WORKER-PROTOCOL.md
## Local Coding Worker Protocol
Strict rules for local file operations:
1. Work only on files listed as allowed in the safe task queue
2. Read only files you are allowed to read or edit
3. Avoid files that might contain credentials, secrets, or sensitive data
4. Never read or write to payment gateway integration files, environment config, or generated artifact directories
5. Never create documentation unless it's required by the context or requested explicitly
6. Write only the allowed output example files that match the safe local model task queue
7. Stop after the current task scope is complete and report honestly
8. Never claim validation without running it
9. Run only the local backend and frontend tests relevant to the files edited
10. Use the safe local model task queue pattern unless explicitly allowed by the user to work on all files