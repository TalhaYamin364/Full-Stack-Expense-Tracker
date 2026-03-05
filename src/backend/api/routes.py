"""
API Routes (Endpoints) for the Expense Tracker.

This file maps HTTP requests to Python functions.
Each function handles one specific action:

  HTTP Method + URL            →  What it does
  ──────────────────────────────────────────────
  GET    /expenses             →  List all expenses
  GET    /expenses/{id}        →  Get one expense by ID
  POST   /expenses             →  Create a new expense
  PUT    /expenses/{id}        →  Update an existing expense
  DELETE /expenses/{id}        →  Delete an expense

This is the "controller" layer — it sits between the user and storage:
  User Request → routes.py (validate + route) → storage.py (data) → Response

Each function:
  1. Receives the request (FastAPI parses it automatically)
  2. Validates the data (using our Pydantic models)
  3. Calls the appropriate storage function
  4. Returns a response with the right HTTP status code

HTTP Status Codes (the ones we use):
  200 = OK (successful GET or PUT)
  201 = Created (successful POST — something new was made)
  404 = Not Found (the expense ID doesn't exist)

  Think of status codes like return values for HTTP:
  200s = "It worked"
  400s = "You made a mistake" (bad request, not found, etc.)
  500s = "Server broke" (bugs in our code)
"""

from fastapi import APIRouter, HTTPException
from typing import List

# Import our models (validation rules) and storage (data functions)
from api.models import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from api import storage


# Create a router — this groups related endpoints together
# main.py will mount this router at the /expenses prefix
router = APIRouter()


# ─── CREATE ─────────────────────────────────────────────
@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(expense_data: ExpenseCreate):
    """
    Create a new expense.
    
    The user sends JSON like: {"amount": 45.50, "category": "Food"}
    FastAPI automatically:
      1. Parses the JSON from the request body
      2. Validates it against ExpenseCreate (amount > 0? category not empty?)
      3. Converts it into an ExpenseCreate object
      4. Passes it to this function as 'expense_data'
    
    If validation fails, FastAPI returns a 422 error automatically —
    we don't need to write any validation code here!
    """
    # Call storage to save the expense
    # expense_data.amount, .category, .description come from the validated model
    new_expense = storage.add_expense(
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description
    )
    
    print(f"📨 POST /expenses → Created expense ID={new_expense['id']}")
    return new_expense


# ─── READ ALL ───────────────────────────────────────────
@router.get("/", response_model=List[ExpenseResponse])
def list_expenses():
    """
    Get all expenses.
    
    Returns a JSON array of all expenses.
    response_model=List[ExpenseResponse] tells FastAPI the response
    will be a list of ExpenseResponse objects.
    
    This is like: SELECT * FROM expenses
    """
    all_expenses = storage.get_all_expenses()
    print(f"📨 GET /expenses → Returning {len(all_expenses)} expenses")
    return all_expenses


# ─── READ ONE ───────────────────────────────────────────
@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    """
    Get a single expense by its ID.
    
    The {expense_id} in the URL is a "path parameter" — FastAPI extracts it
    automatically. If someone visits /expenses/3, expense_id = 3.
    
    This is like: SELECT * FROM expenses WHERE id = 3
    
    If the expense doesn't exist, we return a 404 Not Found error.
    """
    expense = storage.get_expense_by_id(expense_id)
    
    if expense is None:
        # HTTPException sends back an error response with the status code
        # The 'detail' message is what the user sees in the JSON response
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
    
    print(f"📨 GET /expenses/{expense_id} → Found expense")
    return expense


# ─── UPDATE ─────────────────────────────────────────────
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_data: ExpenseUpdate):
    """
    Update an existing expense (partial update).
    
    This combines a path parameter (expense_id from the URL) with
    a request body (expense_data from the JSON).
    
    The user only needs to send the fields they want to change:
      PUT /expenses/3  with body {"amount": 50.00}
      → Only updates the amount, keeps category and description the same
    
    This is like: UPDATE expenses SET amount = 50.00 WHERE id = 3
    """
    updated_expense = storage.update_expense(
        expense_id=expense_id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description
    )
    
    if updated_expense is None:
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
    
    print(f"📨 PUT /expenses/{expense_id} → Updated expense")
    return updated_expense


# ─── DELETE ─────────────────────────────────────────────
@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    """
    Delete an expense by its ID.
    
    Returns a confirmation message if deleted.
    Returns 404 if the expense doesn't exist.
    
    This is like: DELETE FROM expenses WHERE id = 3
    """
    success = storage.delete_expense(expense_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Expense with ID {expense_id} not found")
    
    print(f"📨 DELETE /expenses/{expense_id} → Deleted")
    
    # Return a simple confirmation message
    return {"message": f"Expense {expense_id} deleted successfully"}
