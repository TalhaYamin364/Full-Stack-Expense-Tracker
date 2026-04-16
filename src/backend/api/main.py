"""
FastAPI Application Entry Point.

This is the file that Uvicorn runs to start your API server.
Think of it as the "ignition key" — it creates the app and connects the routes.

This file is intentionally small. Its only job is:
  1. Create the FastAPI app object
  2. Create database tables (if they don't exist yet)
  3. Register the routes (endpoints) from routes.py

The actual endpoint logic lives in routes.py.
The actual database config lives in database.py.
The actual table definitions live in db_models.py.
The actual validation rules live in models.py.

This separation keeps each file focused on ONE job:
  main.py      → "Start the app"
  routes.py    → "Handle requests"
  models.py    → "Validate data" (Pydantic — API layer)
  db_models.py → "Define tables" (SQLAlchemy — database layer)
  database.py  → "Connect to DB"

To run this server:
  cd src/backend
  ../../venv/bin/python -m uvicorn api.main:app --reload

  Breaking that command down:
  - ../../venv/bin/python  → use the project's venv Python directly
      (conda base overrides `source venv/bin/activate`, so we bypass it)
  - -m uvicorn             → run uvicorn as a module
  - api.main               → look inside the api/ folder, find main.py
  - :app                   → use the variable called 'app' in that file
  - --reload               → auto-restart when you save changes (dev only)
"""

from fastapi import FastAPI
from api.routes import router
from api.database import engine
from api.db_models import Expense  # noqa: F401 — imported so SQLAlchemy knows about it

# ─── CREATE DATABASE TABLES ────────────────────────────────
# This is the equivalent of running:
#   CREATE TABLE IF NOT EXISTS expenses (...);
#
# Base.metadata contains info about ALL table classes that inherit from Base.
# create_all() checks what tables exist in the database and creates any
# that are missing. It does NOT modify existing tables (that's what
# Alembic migrations are for — we'll learn that later).
#
# We import db_models.Expense above so that SQLAlchemy's Base.metadata
# knows the Expense table exists. Without that import, create_all()
# would have nothing to create.
from api.database import Base
Base.metadata.create_all(bind=engine)
print("✅ Database tables created (or already exist)")

# Create the FastAPI application
# This 'app' object is what Uvicorn looks for (api.main:app)
app = FastAPI(
    title="Expense Tracker API",
    description="A simple API to manage expenses. Built as a learning project.",
    version="0.2.0"
)

# Register our routes with the app
# prefix="/expenses" means all routes in router start with /expenses
# So a route defined as "/" in routes.py becomes "/expenses"
# And a route defined as "/{expense_id}" becomes "/expenses/{expense_id}"
app.include_router(router, prefix="/expenses", tags=["Expenses"])


# A simple root endpoint to verify the server is running
# Visit http://localhost:8000/ to see this message
@app.get("/")
def root():
    """Health check — confirms the API is running."""
    return {"message": "Expense Tracker API is running!", "docs": "/docs"}
