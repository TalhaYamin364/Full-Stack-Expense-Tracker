---
description: "Use when working on backend files — FastAPI routes, SQLAlchemy models, Pydantic schemas, database config, or any file in src/backend/. Covers file roles, ORM patterns, API design decisions, and known tech debt."
applyTo: "src/backend/**"
---

# Backend Context

## File Roles

| File | Responsibility |
|---|---|
| `database.py` | SQLAlchemy engine, `SessionLocal` factory, `get_db()` dependency, `Base` declaration |
| `db_models.py` | SQLAlchemy ORM table definitions (maps Python classes → DB tables) |
| `models.py` | Pydantic validation models (API request/response layer — separate from ORM) |
| `routes.py` | All API endpoints (CRUD operations via SQLAlchemy) |
| `main.py` | App entry point — creates tables on startup via `Base.metadata.create_all()` |
| `storage.py` | Legacy in-memory CRUD — **not imported anywhere**, kept as reference only |

## SQLAlchemy Patterns

- **Session per request:** `db: Session = Depends(get_db)` injects a DB session into each route and closes it automatically after. Never share sessions across requests.
- **ORM vs Pydantic separation:** `db_models.py` defines what's in the database; `models.py` defines what the API accepts and returns. They are intentionally separate.
- **ORM compatibility:** Pydantic response models use `model_config = ConfigDict(from_attributes=True)` to read from SQLAlchemy objects.

## API Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Money type | `Numeric(10, 2)` / `Decimal` | `Float` has IEEE 754 precision errors — never use for financial data |
| Timestamps | `func.now()` (DB-side) | More reliable than Python-side `datetime.utcnow` — doesn't depend on app server clock |
| Update method | `PATCH` not `PUT` | `PUT` requires sending all fields; `PATCH` is for partial updates with optional fields |
| Delete response | `204 No Content` | REST convention — successful delete has no body to return |
| ID validation | `Path(gt=0)` on all `expense_id` params | Rejects 0/negative IDs at validation layer (422) before hitting the DB |
| Update logic | `model_dump(exclude_unset=True)` | Avoids manual `if field is not None` checks; scales automatically when columns are added |

## Known Tech Debt

| Item | Severity | Plan |
|---|---|---|
| `storage.py` has no legacy header comment | Low | Fix before Phase 2 |
| `print()` used for logging throughout | Low | Replace with `logging` module in Phase 3 (Week 13-14) |
| Error handling is 404-only — no DB exceptions caught | Medium | Phase 3 (Week 13-14) |
| `tests/` is empty | Low | Phase 3 (Week 17-18) |

When reviewing code that touches any of the above, call it out explicitly:
- `storage.py` — flag if anything imports it
- `print()` — flag any new `print()` added
- New routes — flag if added without any error handling

## Alembic Checklist

Run through this whenever a migration file is involved:

- [ ] New migration generated after any model change — not relying on `create_all()` alone
- [ ] `upgrade()` and `downgrade()` both implemented — `downgrade()` must not be `pass`
- [ ] `alembic upgrade head` runs cleanly
- [ ] `alembic downgrade -1` runs cleanly
- [ ] Running `alembic upgrade head` twice is a no-op (idempotency confirmed)
- [ ] `render_as_batch=True` set in both `run_migrations_offline()` and `run_migrations_online()` in `env.py` — required for SQLite ALTER support
- [ ] `PRAGMA foreign_keys=ON` enabled in engine config — SQLite ignores FK constraints otherwise
- [ ] Timestamp columns with `NOT NULL` have a `server_default` in the migration — omitting it breaks raw SQL inserts

## Phase 1 Remaining

- [ ] Add `User` model with `has_many Expenses` relationship (nullable `user_id` FK on `Expense` — Phase 3 auth will enforce it)
- [ ] Set up Alembic for database migrations (basics)
- [ ] Verify Alembic idempotency: run `alembic upgrade head` twice, confirm clean exit on second run
- [ ] Add return type annotations to all route functions (`-> ExpenseResponse`, `-> list[ExpenseResponse]`, `-> Response`)

## Mentor Review — Answered

| # | Question | Answer | Where documented |
|---|---|---|---|
| 1 | Should routes have explicit return type annotations? | Yes — additive, improves IDE support and intent clarity. FastAPI still uses `response_model=` at runtime. | Phase 1 Remaining above; implement in `routes.py` |
| 2 | How to relate users to expenses / data isolation? | Two-phase: Phase 1 adds schema (User model + nullable `user_id` FK). Phase 3 Week 15-16 adds JWT auth + query filter by `current_user.id`. Return 404 (not 403) on cross-user access to avoid leaking resource existence. | `phase-1-backend.md` + `phase-3-design-auth-testing.md` |
| 3 | Alembic idempotency — will running twice fail? | No. Alembic tracks revisions in `alembic_version`; skips already-applied migrations. Never delete a migration file after it has been applied. | `phase-1-backend.md` Migration Safety block |
| 4 | Migration safety: failure, concurrent runs, mid-run crash? | SQLite has no transactional DDL — back up before every migration. `alembic downgrade -1` to roll back. | `phase-1-backend.md` Migration Safety block |
