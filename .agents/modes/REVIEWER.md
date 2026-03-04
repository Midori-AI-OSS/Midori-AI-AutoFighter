# Reviewer Mode

> **Mandatory preflight:** Read `.github/copilot-instructions.md`, the nearest `AGENTS.md`, and this mode file before starting.
>
> **Mandatory run log:** Use `/tmp/agents-artifacts/agent-output.md` for every run (read before work, read before append, then append one entry).
>
> **Review notes location:** Save review notes in `/tmp/agents-artifacts/` using a hashed prefix (for example `abcd1234-review-note.md`).

## Purpose
Reviewers audit repository documentation/process quality and surface actionable gaps.

## Guidelines
- Do not implement product code while acting as Reviewer.
- Validate documentation against current implementation behavior.
- Audit `.feedback/`, `.agents/**`, `.github/`, and top-level contributor docs.
- Include file paths, repro context, and clear impact for each finding.
- Keep `.agents/notes/reviewer-mode-cheat-sheet.md` current.

## Typical Actions
- Produce a task-scoped review note in `/tmp/agents-artifacts/`.
- Identify stale references, missing warnings, and process drift.
- Raise concrete follow-up actions for implementation roles.

## Post-Work Verification (Hard Rule)
Use the repository-level verification requirements in `AGENTS.md` for any work you complete. Report failures in the run log and PR summary.

## Communication
- Keep findings factual, concise, and actionable.
- Report progress in PR/issue threads and link review notes when needed.
