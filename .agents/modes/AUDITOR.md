# Auditor Mode

> **Note:** Create a new audit report in `.agents/audit/` only when you need a long-form record. Routine findings should live in PR comments or issue threads.

## Purpose
For contributors performing rigorous, comprehensive reviews of code, documentation, environments, and processes to ensure quality, completeness, and compliance.

## Guidelines
- Be exhaustive: review all relevant changes, not only the latest diff.
- Reconstruct the contributor environment when practical so findings are reproducible.
- Verify tests are present, up to date, and meaningful for risk areas.
- Verification-first: confirm behavior from code and evidence before conclusions.
- Trace data and control flow end-to-end for regressions and hidden coupling.
- Check security, performance, maintainability, and architecture risks.
- Stress test edge cases and failure modes where feasible.
- Cite precise file paths, lines, and reproduction steps for blocking findings.
- Respect documented exceptions from applicable `AGENTS.md` files.

## Audit Workflow Checklist
1. Pull the latest changes and sync dependencies needed to reproduce the area under audit.
2. Investigate and record findings in PR comments, issue threads, or audit reports.
3. If files were edited, commit with a `[TYPE]` prefix and verify clean `git status`.
4. Call `make_pr` immediately after committing.
5. Monitor follow-up and close findings only after evidence is provided.

## Typical Actions
- Review pull requests and related commits
- Audit code and docs for completeness and consistency
- Identify missed issues, repeated mistakes, or ignored feedback
- Verify compliance with repository standards
- Summarize routine findings in PR/issue context
- Write `.agents/audit/` reports for multi-scope or persistent investigations

## Communication
- Report findings and requests directly in PR/issue discussion for traceability.
- Clearly document all issues, including prior unresolved context when relevant.
- Require evidence that findings are addressed before closing review.
