"""
API Routes (Endpoints) for the Expense Tracker.

This file maps HTTP requests to Python functions.
Each function handles one specific action:

  HTTP Method + URL            →  What it does
  ──────────────────────────────────────────────
  GET    /expenses             →  List all expenses
  GET    /expenses/{id}        →  Get one expense by ID
  POST   /expenses             →  Create a new expense
  PATCH  /expenses/{id}        →  Partially update an expense
  DELETE /expenses/{id}        →  Delete an expense (returns 204)

This is the "controller" layer — it sits between the user and the database:
  User Request → routes.py (validate + route) → database (via SQLAlchemy) → Response

Each function:
  1. Receives the request (FastAPI parses it automatically)
  2. Validates the data (using our Pydantic models)
  3. Uses SQLAlchemy to query/modify the database
  4. Returns a response with the right HTTP status code

HTTP Status Codes (the ones we use):
  200 = OK (successful GET or PATCH)
  201 = Created (successful POST — something new was made)
  204 = No Content (successful DELETE — nothing to send back)
  404 = Not Found (the expense ID doesn't exist)
  422 = Unprocessable Entity (validation failed — e.g., negative amount)

  Think of status codes like return values for HTTP:
  200s = "It worked"
  400s = "You made a mistake" (bad request, not found, etc.)
  500s = "Server broke" (bugs in our code)

What changed from the in-memory version?
  Before: routes called storage.py functions (Python list)
  Now:    routes use SQLAlchemy to talk to SQLite database

  The key new concept is "Dependency Injection":
    db: Session = Depends(get_db)
  This tells FastAPI: "Before running this route, call get_db()
  to create a database session, and pass it to me as 'db'."
  After the route finishes, the session is automatically closed.
"""

from fastapi import APIRouter, HTTPException, Depends, Path, Response, Body
from sqlalchemy.orm import Session
from typing import List

# Import our Pydantic models (API validation) and SQLAlchemy model (database table)
from api.models import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from api.db_models import Expense
from api.database import get_db


# Create a router — this groups related endpoints together
# main.py will mount this router at the /expenses prefix
router = APIRouter()


# ─── CREATE ─────────────────────────────────────────────
@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(expense_data: ExpenseCreate, db: Session = Depends(get_db)):
    """
    Create a new expense.

    SQL equivalent:
      INSERT INTO expenses (amount, category, description)
      VALUES (45.50, 'Food', 'Lunch at cafe');

    Step by step:
      1. Create an Expense object (like preparing an INSERT statement)
      2. db.add() — stage the insert (like adding to a transaction)
      3. db.commit() — execute the transaction (like clicking "Execute")
      4. db.refresh() — reload the object to get the auto-generated ID
    """
    # Create a new Expense row — this is like writing INSERT INTO ...
    new_expense = Expense(
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description
    )

    db.add(new_expense)       # Stage the INSERT (add to transaction)
    db.commit()               # Execute the transaction (write to disk)
    db.refresh(new_expense)   # Reload to get the auto-generated ID

    print(f"📨 POST /expenses → Created expense ID={new_expense.id}")
    return new_expense


# ─── READ ALL ───────────────────────────────────────────
@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(db: Session = Depends(get_db)):
    """
    Get all expenses.

    SQL equivalent:
      SELECT * FROM expenses;

    db.query(Expense).all() does exactly that:
      - query(Expense) = "FROM expenses"
      - .all()         = "SELECT * (return all rows)"
    """
    all_expenses = db.query(Expense).all()
    print(f"📨 GET /expenses → Returning {len(all_expenses)} expenses")
    return all_expenses


# ─── READ ONE ───────────────────────────────────────────
@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int = Path(gt=0), db: Session = Depends(get_db)):
    """
    Get a single expense by its ID.

    SQL equivalent:
      SELECT * FROM expenses WHERE id = 3;

    db.query(Expense).filter(Expense.id == expense_id).first() breaks down as:
      - query(Expense)                   = "FROM expenses"
      - .filter(Expense.id == expense_id) = "WHERE id = 3"
      - .first()                          = "LIMIT 1" (returns one row or None)
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")

    print(f"📨 GET /expenses/{expense_id} → Found expense")
    return expense


# ─── UPDATE ─────────────────────────────────────────────
@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int = Path(gt=0), expense_data: ExpenseUpdate = Body(), db: Session = Depends(get_db)):
    """
    Partially update an existing expense.

    Why PATCH instead of PUT?
      PUT = replace the ENTIRE resource (must send all fields)
      PATCH = modify PART of the resource (send only changed fields)
      Since our ExpenseUpdate model has all optional fields, PATCH is correct.

    SQL equivalent:
      UPDATE expenses SET amount = 50.00 WHERE id = 3;

    With SQLAlchemy, you:
      1. Query the row (SELECT ... WHERE id = 3)
      2. Modify the Python object's attributes
      3. Commit — SQLAlchemy detects the changes and writes an UPDATE

    This is called "dirty tracking" — SQLAlchemy watches for attribute
    changes on objects and automatically generates UPDATE statements.
    """
    # Step 1: Find the expense (SELECT * FROM expenses WHERE id = ?)
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")

    # Step 2: Update only the fields that were provided
    # model_dump(exclude_unset=True) returns a dict of ONLY the fields the user sent.
    # For example, {"amount": 50.00} if the user only sent amount.
    # This replaces the old manual if/else chain and scales automatically
    # when new columns are added — no code change needed.
    update_data = expense_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    # Step 3: Commit the changes (SQLAlchemy generates the UPDATE SQL)
    db.commit()
    db.refresh(expense)   # Reload to get the latest data from DB

    print(f"📨 PATCH /expenses/{expense_id} → Updated expense")
    return expense


# ─── DELETE ─────────────────────────────────────────────
@router.delete("/{expense_id}", status_code=204, response_class=Response)
def delete_expense(expense_id: int = Path(gt=0), db: Session = Depends(get_db)):
    """
    Delete an expense by its ID.

    Returns 204 No Content on success — REST convention for deletes.
    There's no body to return when something has been deleted.

    SQL equivalent:
      DELETE FROM expenses WHERE id = 3;

    With SQLAlchemy:
      1. Find the row
      2. db.delete(expense) — mark it for deletion
      3. db.commit() — execute the DELETE
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")

    db.delete(expense)    # Mark for deletion
    db.commit()           # Execute the DELETE

    print(f"📨 DELETE /expenses/{expense_id} → Deleted")

    # 204 No Content — no body returned
    return None
