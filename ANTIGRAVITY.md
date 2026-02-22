# ANTIGRAVITY.md

## Antigravity Workflow Orchestration

### 1. Plan & Artifact First
- Enter plan mode and generate a structural Artifact for ANY non-trivial task (3+ steps or architectural decisions).
- If a process fails repeatedly, STOP, re-evaluate the context, and generate a new plan.
- Write detailed specs upfront in `tasks/todo.md` to reduce ambiguity before writing any code.

### 2. Multi-Agent Delegation
- Utilize Antigravity's multi-agent capabilities to keep the primary context window clean.
- Offload parallel tasks (e.g., API research, backend logic, UI component creation) to separate sub-agents.
- Assign one specific domain per agent for focused and isolated execution.

### 3. Self-Improvement Loop
- After ANY correction from the user, immediately update `tasks/lessons.md` with the failure pattern and the correct approach.
- Review `tasks/lessons.md` at the start of every session to prevent repeating past mistakes in this specific project.

### 4. Autonomous Verification & Browser Actuation
- Never mark a task complete without proving it works.
- Use Antigravity's browser actuation capabilities to visually and functionally verify UI changes, and run end-to-end tests autonomously.
- Point at logs, run unit tests, and demonstrate correctness without waiting for user prompts.

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky, leverage Antigravity's reasoning capabilities to evaluate alternative architectural approaches before committing.
- Skip this for simple, obvious fixes – don't over-engineer. Challenge your own work before presenting the Artifact.

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it autonomously. Don't ask for step-by-step hand-holding.
- Analyze logs, error traces, and failing tests, then resolve the root cause directly.
- Utilize browser actuation or automated tests to confirm the bug is truly squashed before reporting back to the user. Zero context switching required.

## Task Management

1. **Plan First**: Write the initial plan to `tasks/todo.md` with checkable items.
2. **Verify Plan**: Request user approval before starting implementation.
3. **Track Progress**: Mark items complete in real-time as you go.
4. **Document Results**: Add a concise review section to `tasks/todo.md` upon completion.
5. **Capture Lessons**: Ruthlessly update `tasks/lessons.md` after any debugging sessions.

## Core Principles & Infrastructure Rules

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **Execution Environment**: Always explicitly state the execution environment (Local or Remote) before suggesting or running any commands.
- **Destructive Actions**: Preface any action that modifies, overwrites, or deletes infrastructure/server settings with a "⚠️ Warning" and a clear explanation. Require explicit approval.
- **Separation of Concerns**: Strictly separate "confirmation" commands (e.g., checking current state or logs) from "execution" commands (e.g., applying changes to infrastructure).
- **No IP Guessing**: Never use automatic exploration or guessing for server IPs during deployment or setup. Always confirm and fix the target IP address before proceeding.
- **Language**: All output including Walkthroughs, task descriptions in `todo.md`, lessons, Artifacts, and chat communications MUST be entirely in Japanese (日本語).
