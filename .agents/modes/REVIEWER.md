# Reviewer Mode

> **Note:** Save review notes in `.agents/review/` with random hash prefixes from `openssl rand -hex 4` (example: `abcd1234-review-note.md`).

## Purpose
For contributors who audit repository documentation to keep it accurate and current. Reviewers identify outdated or missing information, validate cross-file consistency, and surface follow-up work for implementation roles.

## Guidelines
- **Do not implement code changes while acting as Reviewer.**
- Read existing files in `.agents/review/` and write a new hashed review note per review pass.
- Review `.feedback/`, planning docs, notes directories, `.agents/**` instructions, `.github/` configs, and top-level docs.
- Validate links, filenames, and processes end-to-end against current implementation.
- Flag process gaps, risky directions, and missing warnings that could cause breakage.
- Include reproduction steps, file paths, and context in every finding.
- Maintain `.agents/notes/reviewer-mode-cheat-sheet.md` with durable preferences.
- Log unresolved ambiguity as explicit clarification questions.

## Typical Actions
- Add a new review note in `.agents/review/`
- Audit instruction and workflow docs for drift
- Check CI/workflow config consistency
- Re-review prior findings to ensure follow-through

## Communication
- Coordinate in review notes, PR comments, and issue threads so progress is visible.
- Keep findings factual, actionable, and scoped.
