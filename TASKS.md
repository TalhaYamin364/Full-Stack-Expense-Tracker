# TASKS

## Project Setup & Structure

- [ ] **Restructure project folders**
  ```
  docs/
  artifacts/
  TASKS.md
  src/
     backend/
     frontend/
  tests/
     backend/
     frontend/
  ```
  - Nest frontend and backend into an `src/` folder instead of individual folders
  - Add `tests/` folder for custom tests (backend & frontend)

- [ ] **Update AGENTS.md**
  - Fill with strengths and current experience level
  - Include business-oriented knowledge

---

## Phase 1: FastAPI Backend (CURRENT - NOT STARTED)

- [ ] Set up basic FastAPI project structure
- [ ] Hardcode some responses (no database yet)
- [ ] Basic stubbing for initial endpoints
- [ ] Verify backend runs and responds correctly

---

## Phase 2: Flask Frontend

- [ ] Set up Flask app with plain HTML templates
- [ ] No CSS needed (keep it simple)
- [ ] Add JavaScript only where necessary
- [ ] **Key Goal:** Verify Flask app can make calls and receive responses all the way through to FastAPI backend

---

## Documentation & Session Logs

- [ ] Keep work logs in `docs/`
- [ ] Create a separate `sessions/` folder for session logs
  - Separate from AGENTS.md
  - Supports progressive disclosure for AI context management
- [ ] Research **RALF loops** for keeping context window clean

---

## Notes

- This file doesn't need to be committed to the repository
- Session logs help maintain growing windows of context for AI assistance
