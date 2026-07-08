# Full-Stack Expense Tracker

**Project:** Learning project — converting a Python CLI app into a 3-tier web application.  
**Owner:** Talha Yamin | Analytics Engineer (4 yrs) → Software Engineer  
**Strengths:** SQL (deep), Python (comfortable), dbt, Airflow. Learning: web dev, APIs, SE patterns.  
**Target roles:** Data Engineer, Backend Developer, Full-Stack Developer.

---

## Current State

**Phase 1 — Backend (95% complete)**
- FastAPI + SQLAlchemy + SQLite fully operational. All CRUD endpoints tested.
- Remaining: User model + relationships, Alembic migrations.

**Phase 2 — Frontend (not started)**
- Flask/Jinja2 first (port 5000), then React SPA (port 3000). Both share the FastAPI backend.

**Phases 3–6** — Software design, auth, testing, CI/CD, deployment. Not started.

---

## Architecture

```
Flask (5000) ──┐
               ├──► FastAPI (8000) ──► SQLite (expenses.db)
React (3000) ──┘
```

---

## Running the Server

```bash
cd src/backend
../../venv/bin/python -m uvicorn api.main:app --reload
```

> Conda base overrides venv activation. Always use the full venv path above — do not use bare `uvicorn` or `python -m uvicorn`.

---

## Standing Orders

- Explain *why*, not just *what* — learning SE patterns, not just syntax
- Work step by step; verify each step before proceeding
- One clarifying question at a time
- Check consistency across related files when making changes
- Think through something carefully, present the decision to me, then confirm it's the right one before implementing it. Always run the test and edge case scenarios, and also inform me of such scenarios so that I am aware of the nuances in my projects.

---

## PR Workflow

**Cadence:** ~2 PRs per week. Each PR = one logical unit of work (e.g. "Add User model", "Set up Alembic", "Flask base template").

**Branch naming:**

| Prefix | Use |
|---|---|
| `feature/<description>` | New functionality |
| `fix/<description>` | Bug fixes |
| `docs/<description>` | Documentation, learning tracker updates |

**Branch protection on `main` (strict — Option B):**
- 1 approval required before merge
- Stale reviews dismissed when new commits are pushed
- No admin bypass — reviews are mandatory, no exceptions

**Reviewers:**
- Tag `@github-copilot` manually on every PR (not auto-assigned)
- Request mentor review when the work is ready for feedback — don't wait until perfect

**PR template:** `.github/PULL_REQUEST_TEMPLATE.md` auto-populates every PR with: what changed, why, plan reference (relevant section from `6-Month-SE-Transition-Plan.md`), manual testing checklist, and review checkboxes.

**CI/CD note:** Automated test runs on PRs (GitHub Actions) are Phase 3 work. For now, all testing is manual via Swagger UI.

---

## Deeper Context

Auto-loads when working in relevant directories:
- `src/backend/**` → `.github/instructions/backend.instructions.md`
- `src/frontend/**` → `.github/instructions/frontend.instructions.md`
- `tests/**` → `.github/instructions/tests.instructions.md`
