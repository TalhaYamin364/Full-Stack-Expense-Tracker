## What Changed
<!-- Describe the changes made in this PR. Be specific — what files were touched and what behavior changed. -->

## Why
<!-- Explain the reasoning. What problem does this solve, or what does it build toward in the project? -->

## Plan Reference
<!-- Copy the relevant section from 6-Month-SE-Transition-Plan.md that this PR maps to. -->

**Phase / Week:**
<!-- e.g. Phase 1 — Week 3-4: Databases & ORMs -->

**Goal:**
<!-- e.g. Understand relational databases and how ORMs bridge code and SQL -->

**Concepts / Hands-On tasks addressed in this PR:**
<!-- Paste the specific bullet points from the plan that this PR satisfies -->
-

## Testing Done
<!-- Manual testing only for now. Describe what you verified. -->

- [ ] Server started successfully (`../../venv/bin/python -m uvicorn api.main:app --reload`)
- [ ] Affected endpoints tested via Swagger UI (`/docs`)
- [ ] Existing endpoints still work — no regressions

## Checklist

- [ ] Code is consistent across related files (routes, models, schemas, etc.)
- [ ] No debug `print()` statements or leftover commented-out code
- [ ] PR title follows convention: `[phaseN] short description` (e.g. `[phase1] Add User model`)

## Reviews

- [ ] Tagged `@github-copilot` as reviewer
- [ ] Requested mentor review (if ready for feedback)
