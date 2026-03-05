"""
FastAPI Application Entry Point.

This is the file that Uvicorn runs to start your API server.
Think of it as the "ignition key" — it creates the app and connects the routes.

This file is intentionally small. Its only job is:
  1. Create the FastAPI app object
  2. Register the routes (endpoints) from routes.py

The actual endpoint logic lives in routes.py.
The actual data handling lives in storage.py.
The actual validation rules live in models.py.

This separation keeps each file focused on ONE job:
  main.py   → "Start the app"
  routes.py → "Handle requests"
  models.py → "Validate data"
  storage.py → "Store data"

To run this server:
  cd src/backend
  uvicorn api.main:app --reload

  Breaking that command down:
  - uvicorn         → the server program
  - api.main        → look inside the api/ folder, find main.py
  - :app            → use the variable called 'app' in that file
  - --reload        → auto-restart when you save changes (dev only)
"""

from fastapi import FastAPI
from api.routes import router

# Create the FastAPI application
# This 'app' object is what Uvicorn looks for (api.main:app)
app = FastAPI(
    title="Expense Tracker API",
    description="A simple API to manage personal expenses. Built as a learning project.",
    version="0.1.0"
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
