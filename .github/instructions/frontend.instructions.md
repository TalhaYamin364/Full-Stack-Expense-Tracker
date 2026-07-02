---
description: "Use when working on frontend files — Flask templates, Jinja2 views, React components, or any file in src/frontend/. Covers architecture intent and frontend-backend integration approach."
applyTo: "src/frontend/**"
---

# Frontend Context

## Architecture Intent

Two frontends coexist, sharing the same FastAPI backend at `localhost:8000`:

| Frontend | Port | Stack | Status |
|---|---|---|---|
| Flask | 5000 | Flask + Jinja2 templates | Phase 2 — not started |
| React | 3000 | React + JavaScript SPA | Phase 2 (later) — not started |

Build order: Flask first (simpler, Python-based, good for learning HTTP/HTML fundamentals), then React as a separate SPA once JS fundamentals are covered.

## Integration Pattern

Both frontends communicate with the FastAPI backend via HTTP — Flask uses `requests` server-side, React uses `fetch`/axios client-side. Neither frontend has its own data layer; all persistence goes through the API.

## Phase 2 Plan

- Week 5-6: Flask app + Jinja2 templates (add/view expenses)
- Week 7-8: JavaScript fundamentals
- Week 9-10: React basics
- Week 11-12: React + FastAPI integration (full SPA)
