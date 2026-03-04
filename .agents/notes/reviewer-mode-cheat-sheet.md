# Reviewer Mode Cheat Sheet

Quick reference for contributors auditing documentation quality.

## Key Responsibilities

- Read existing review notes in `.agents/review/` and add a new hashed note.
- Audit `.feedback/`, planning docs, notes directories, `.agents/**` instructions, `.github/` configs, and top-level docs.
- Record findings in a new review note with a random hash filename:

```bash
openssl rand -hex 4  # e.g., abcd1234
```

- Do not modify code while acting in Reviewer mode.
- Maintain this cheat sheet with durable preferences gathered during audits.

## Finding Conventions

- Write clear issue titles and actionable descriptions.
- Include reproduction context, file paths, and expected behavior.
- Capture unresolved questions explicitly for follow-up.

## Useful Links

- Full mode guidance: [`REVIEWER.md`](../modes/REVIEWER.md)
