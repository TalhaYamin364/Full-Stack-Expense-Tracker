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

The original CLI expense tracker is located at:
`/Users/talha.yamin/Adept Projects/Adept-Projects/Expense Tracker/main.py`

**Original Features:**
- Add expense (amount + category)
- List all expenses
- Calculate total expenses
- Filter expenses by category

**Target Features (CRUD Operations):**
- **C**reate: Add new expense
- **R**ead: List expenses, filter by category, get totals
- **U**pdate: Edit existing expense
- **D**elete: Remove expense

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
├── .gitignore          # Git ignore rules
├── backend/            # FastAPI backend (Phase 1)
│   └── (empty - to be built)
└── frontend/           # Flask frontend (Phase 2), later React
    └── (empty - to be built)
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
