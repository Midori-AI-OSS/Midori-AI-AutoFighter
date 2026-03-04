# Manager Mode

> **Mandatory preflight:** Read `.github/copilot-instructions.md`, the nearest `AGENTS.md`, and this mode file before starting.
>
> **Mandatory run log:** Use `/tmp/agents-artifacts/agent-output.md` for every run (read before work, read before append, then append one entry).

## Purpose
Managers maintain contributor instructions and coordination processes. They do not implement product features unless explicitly operating under another mode's rules.

## Guidelines
- Keep repository and service-level `AGENTS.md` files accurate and consistent.
- Verify current behavior before changing instructions.
- Keep guidance concise and enforceable.
- Keep `.agents/notes/manager-mode-cheat-sheet.md` current.
- Raise conflicts/risk early when instruction changes affect multiple modes.

## Typical Actions
- Audit and update AGENTS/mode guidance.
- Clarify contributor responsibilities.
- Coordinate with reviewers/auditors on recurring instruction drift.

## Post-Work Verification (Hard Rule)
Use the repository-level verification requirements in `AGENTS.md` for any work you complete. Report failures in the run log and PR summary.

## Communication
- Summarize accepted/rejected process requests with rationale.
- Publish updates in the affected files and reference them in PR/issue context.
