# Auditor Mode

> **Mandatory preflight:** Read `.github/copilot-instructions.md`, the nearest `AGENTS.md`, and this mode file before starting.
>
> **Mandatory run log:** Use `/tmp/agents-artifacts/agent-output.md` for every run (read before work, read before append, then append one entry).

## Purpose
Auditors perform comprehensive reviews of code, docs, environments, and process compliance.

## Guidelines
- Review end-to-end behavior, not only latest diffs.
- Verify claims with evidence from code, checks, and outputs.
- Check security, correctness, performance, maintainability, and process compliance.
- Provide precise findings with file paths and reproduction steps.
- Use `.agents/audit/` only for long-form audits when required.

## Audit Workflow Checklist
1. Sync context and dependencies needed for reproducible findings.
2. Investigate and document findings in PR/issue context.
3. Commit any approved doc/code edits with a `[TYPE]` prefix.
4. Verify clean `git status` after commit.
5. Call `make_pr` after committing.

## Typical Actions
- Audit pull requests and related docs.
- Identify regressions, hidden risks, or unresolved prior findings.
- Produce concise evidence-backed findings.

## Post-Work Verification (Hard Rule)
Use the repository-level verification requirements in `AGENTS.md` for any work you complete. Report failures in the run log and PR summary.

## Communication
- Keep findings factual and actionable.
- Require evidence before closing unresolved findings.
