---
description: "Load when reviewing any file in this project — defines the structured code review checklist for Copilot and manual reviews."
applyTo: "src/**"
---

# Code Review Checklist

Run through every section below before marking a review complete. Do not skip sections because they seem unlikely — surface anything that doesn't pass.

---

## 1. Cross-file Consistency

- [ ] Any new DB column in `db_models.py` has a matching field in the relevant Pydantic schema in `models.py`
- [ ] Any new field exposed in a response schema is actually populated by the route in `routes.py`
- [ ] If a new model is added to `db_models.py`, it is imported in `main.py` so `Base.metadata.create_all()` and Alembic autogenerate both see it
- [ ] If a new table is added, a corresponding Alembic migration has been generated (not just relying on `create_all()`)

---

## 2. API Design Decisions

These are established conventions for this project — flag any deviation:

| Convention | Check |
|---|---|
| Money fields use `Numeric(10, 2)` / `Decimal`, never `float` | ✅ / ❌ |
| Timestamps use `func.now()` (DB-side), not `datetime.utcnow` | ✅ / ❌ |
| Partial updates use `PATCH` + `model_dump(exclude_unset=True)`, not `PUT` | ✅ / ❌ |
| Successful deletes return `204 No Content` with no body | ✅ / ❌ |
| All route `id` path params validated with `Path(gt=0)` | ✅ / ❌ |
| All route functions have explicit Python return type annotations | ✅ / ❌ |
| Pydantic response models use `model_config = ConfigDict(from_attributes=True)` | ✅ / ❌ |

---

## 3. Security (OWASP-relevant)

- [ ] No raw SQL strings constructed from user input — all DB queries go through SQLAlchemy ORM
- [ ] No plaintext passwords stored or logged anywhere
- [ ] No secrets, tokens, or credentials hardcoded in any file
- [ ] Input validation present at the API boundary (Pydantic schemas handle this — confirm they're applied)
- [ ] No `print()` statements that could leak sensitive data in logs

---

## 4. General

- [ ] No debug artifacts (`print()`, commented-out code, `TODO` left unresolved)
- [ ] All new functions/methods have return type annotations
- [ ] No unused imports
- [ ] PR title follows convention: `[phaseN] short description`