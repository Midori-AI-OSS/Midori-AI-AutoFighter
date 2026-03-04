# Frontend Contributor Instructions

> **MANDATORY:** Before touching files under `frontend/`, read `.github/copilot-instructions.md`, the repository `AGENTS.md`, and your mode document in `.agents/modes/`.

## Agent Run Log (Hard Rule)
Use `/tmp/agents-artifacts/agent-output.md` for every run.

Required behavior:
- Read the log before work.
- Read it again before appending.
- Append one entry per run.
- Create the file if missing.

Required fields:
- timestamp
- role/mode
- scope/files
- intent
- actions taken
- results
- blockers/next step

## Workflow Expectations
- Keep this guidance aligned with root `AGENTS.md` and active `.agents/` docs.
- Use Bun for Node tooling:
  - `bun install`
  - `bun run dev`
  - `bun run build`
- Use focused, reviewable commits.

## UI / UX Standards (Hard Rules)
- Preserve the established visual language and interaction patterns.
- Reuse shared primitives before creating new local styles/components.
- Search existing components, CSS primitives, and tokens first.
- Accessibility is mandatory (semantic labels, keyboard flow, focus visibility).
- Reduced-motion support is mandatory where motion exists.
- Visual-system changes require explicit Lead Developer approval.
- Avoid drive-by UI redesigns unrelated to the task.

## Svelte Conventions
- Prefer idiomatic Svelte patterns (`$:` reactivity, stores, component props).
- Keep files under about 300 lines when practical; split complex components.
- Keep styles component-scoped unless extracted as shared primitives.

## Post-Work Verification (Hard Rule)
Run and report frontend checks:

```bash
cd frontend && bun run lint
```

Rules:
- Running these commands is mandatory.
- Failures do not block reporting completion, but must be documented in run log and PR summary.
- If your frontend change depends on backend behavior, also run the root-level backend/typecheck smoke checks from `AGENTS.md`.

## Review Checklist
- Confirm UI changes respect existing backend/frontend data contracts.
- Confirm reuse-first behavior for components/styles/tokens.
- Document process gaps for Manager-mode follow-up.
