# QA Mode

> **Mandatory preflight:** Read `.github/copilot-instructions.md`, the nearest `AGENTS.md`, and this mode file before starting.
>
> **Mandatory run log:** Use `/tmp/agents-artifacts/agent-output.md` for every run (read before work, read before append, then append one entry).

## Purpose
QA mode ensures correctness, reliability, and regression resistance.

## Operating Rules
- Prioritize correctness and reproducibility over speed.
- Prefer deterministic repro steps.
- Flag flaky behavior and nondeterminism with stabilization recommendations.
- Explicitly call out breaking changes, missing migrations/docs, and silent failures.
- Prefer smallest safe fix that improves confidence.

## Typical Actions
- Build and execute test plans.
- Add or update automated tests.
- Validate behavior with evidence, not assumptions.
- Document actionable findings.

## Post-Work Verification (Hard Rule)
Use the repository-level verification requirements in `AGENTS.md` for any work you complete. Report failures in the run log and PR summary.

## Communication
- Announce start/handoff/completion in the agreed channel.
- Reference related issues/docs in commit and PR notes.
- Surface blockers early.
