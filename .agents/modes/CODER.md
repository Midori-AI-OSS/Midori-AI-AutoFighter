# Coder Mode

> **Mandatory preflight:** Read `.github/copilot-instructions.md`, the nearest `AGENTS.md`, and this mode file before starting.
>
> **Mandatory run log:** Use `/tmp/agents-artifacts/agent-output.md` for every run (read before work, read before append, then append one entry).

## Purpose
Coders implement, refactor, and review code with a focus on maintainable, high-quality changes.

## Guidelines
- Follow repository coding standards and tooling requirements.
- Verification-first: confirm current behavior before changing code.
- Keep diffs focused and easy to review.
- Add or update tests when change risk requires it.
- Keep docstrings accurate and avoid unnecessary long-form docs.
- Reuse existing UI/components/styles before creating new patterns.

## Typical Actions
- Implement features and bug fixes.
- Refactor for clarity and maintainability.
- Run focused verification and document outcomes.

## Prohibited Actions
- Do not modify `.feedback/`.
- Do not modify `.agents/audit/` unless operating in Auditor mode.

## Post-Work Verification (Hard Rule)
Use the repository-level verification requirements in `AGENTS.md` for any work you complete. Report failures in the run log and PR summary.

## Communication
- Announce start/progress/completion in the agreed channel.
- Include intent, outcome, and verification notes in PR/issue context.
