# Reviewer Mode Cheat Sheet

Quick reference for contributors auditing documentation quality.

## Key Responsibilities
- Read preflight docs before work.
- Save review notes in `/tmp/agents-artifacts/` with hashed prefixes.
- Audit `.feedback/`, `.agents/**`, `.github/`, and top-level contributor docs.
- Include clear file paths, impact, and reproduction context.
- Keep findings actionable and scoped.

## Note Naming
```bash
openssl rand -hex 4  # e.g., abcd1234
# save as /tmp/agents-artifacts/abcd1234-review-note.md
```

## Useful Links
- Full mode guidance: [`REVIEWER.md`](../modes/REVIEWER.md)
