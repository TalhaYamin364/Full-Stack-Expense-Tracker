# AGENTS.MD - AI Assistant Context Document

> **Purpose:** This file helps AI assistants (like GitHub Copilot) understand the project context, history, and next steps when returning to this project.

---

## Project Overview

**Project Name:** Full-Stack Expense Tracker  
**Owner:** Talha Yamin  
**Created:** January 2026  
**Primary Goal:** Learn full-stack development by converting a simple Python CLI expense tracker into a 3-tier web application.

---

## Developer Context

**Skill Level:** Beginner  
- Understands basic Python syntax
- New to APIs, backend frameworks, databases, and frontend development
- Learning step-by-step, needs clear explanations

# TODO: Add knowledge here
```
    1. Fill with strengths and current experience level.
    2. Even include business oriented knowledge.
   5. Phase 1: FastAPI Backend (CURRENT - NOT STARTED)- [ ] Hardcode some responses if those are needed since there is no database added at the moment. Some basic stubbing will be needed to be done at the beginning.
   6. Phase 2: Flask Frontend - Expectation for the front end. Plain HTML, no need to worry about css. Maybe some javascript. We need to check if the flask app makes the call and recieves that call all the way to the back of the stack on fast api.
   7. Keep work logs in the docs, or have a session log each time we work.
   8. Make it seperate from agents.md and have a seperate folder of sessions log - This is normally called progressive disclosure for AIs and growing windows of context. 
   9. Look into Ralf loops - related to above and keeping context window as clean as possible.

**Learning Objectives:**
1. Understand what APIs are and how they work
2. Learn FastAPI for building backend services
3. Learn Flask for simple frontend templating
4. Understand ORMs (SQLAlchemy) and database persistence
5. Eventually learn React for modern frontend development

---

## Architecture Plan (3-Tier)

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                  (Flask + HTML Templates)                    │
│                   Later: React Frontend                      │
│                      Port: 5000                              │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP Requests (API Calls)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│                       (FastAPI)                              │
│              Business Logic + API Endpoints                  │
│                      Port: 8000                              │
└─────────────────────────┬───────────────────────────────────┘
                          │ Database Queries (via ORM)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                               │
│                  (SQLite + SQLAlchemy)                       │
│                   expenses.db file                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Original Application Reference

The CLI expense tracker has two versions in `src/backend/`:

1. **expense_tracker_simple.py** (~54 lines)
   - Minimal implementation for learning
   - Basic functionality without validation
   
2. **main.py** (~229 lines) - CURRENT REFERENCE
   - Production-quality code with validation
   - Enhanced UX with formatted output
   - Type hints and comprehensive docstrings
   - Input validation for amounts and categories
   - Case-insensitive category filtering

**Current Features:**
- Add expense with validated amount and category
- List all expenses in formatted table
- Calculate total expenses with count
- Filter expenses by category (case-insensitive)
- User-friendly menu with error handling

**Target Features (CRUD Operations):**
- **C**reate: Add new expense ✓ (already implemented in CLI)
- **R**ead: List expenses, filter by category, get totals ✓ (already implemented)
- **U**pdate: Edit existing expense (NEW - add to API)
- **D**elete: Remove expense (NEW - add to API)

---

## Development Phases

### Phase 1: FastAPI Backend (CURRENT - NOT STARTED)
- [ ] Create basic FastAPI server
- [ ] Convert Python functions to API endpoints
- [ ] Add console logging when expenses are added
- [ ] Test endpoints with browser/curl

### Phase 2: Flask Frontend
- [ ] Create Flask app with HTML templates
- [ ] Build forms to add/view expenses
- [ ] Connect Flask to FastAPI backend
- [ ] Verify data flows from frontend → backend (console logs)

### Phase 3: Database Integration
- [ ] Add SQLAlchemy ORM
- [ ] Create Expense model
- [ ] Set up SQLite database
- [ ] Replace in-memory storage with database

### Phase 4: React Frontend (Future)
- [ ] Set up React project
- [ ] Replace Flask frontend with React
- [ ] Connect React to FastAPI

---

## Project Structure

```
Full-Stack Expense Tracker/
├── AGENTS.MD           # This file - AI context
├── README.md           # Human-readable project overview
├── TASKS.md            # Current tasks and progress tracking
├── .gitignore          # Git ignore rules
├── docs/               # Documentation and session logs
│   ├── README.md       # Docs overview
│   └── sessions/       # Progressive disclosure - session-by-session logs
├── src/                # Source code
│   ├── backend/        # FastAPI backend (Phase 1)
│   │   ├── main.py                      # Full CLI version (229 lines)
│   │   └── expense_tracker_simple.py    # Simple CLI version (54 lines)
│   └── frontend/       # Flask frontend (Phase 2), later React
├── tests/              # Test files
│   ├── backend/        # Backend tests
│   └── frontend/       # Frontend tests
├── artifacts/          # Build outputs, generated files
└── venv/               # Python virtual environment (gitignored)
```

---

## Key Decisions Made

| Decision | Choice | Reason |
|----------|--------|--------|
| Backend Framework | FastAPI | Modern, auto-docs, type hints, good for learning |
| Frontend (Initial) | Flask + HTML | Simple, Python-based, easy to understand |
| Frontend (Later) | React | Industry standard, component-based |
| ORM | SQLAlchemy | Works with FastAPI, industry standard |
| Database | SQLite | File-based, no setup required, perfect for learning |

---

## Notes for AI Assistants

When helping with this project:
1. **Explain concepts simply** - User is learning, avoid jargon without explanation
2. **Go step by step** - Don't jump ahead or make assumptions
3. **Show the "why"** - Explain purpose of code, not just what it does
4. **Test incrementally** - Verify each step works before moving on
5. **Console logging** - Add print statements to show data flow

---

## Session Log

### Session 1 - January 22, 2026
- Created project folder structure
- Created AGENTS.MD, README.md, .gitignore
- Established 3-tier architecture plan
- Next: Begin Phase 1 - FastAPI Backend

### Session 2 - February 2, 2026
- Updated AGENTS.MD with detailed developer context
- Created folders: `src/`, `tests/`, `artifacts/`
- Clarified skill level: Strong in SQL/Python/DBT, learning web development
- Career goal: Data Engineer, Backend Developer, or Full-Stack Developer
- Timeline: Few months, job search active
- Reviewed existing CLI code: Two versions (simple & full)
- Next: Set up virtual environment, begin Phase 1 (FastAPI backend)
