"""
Pydantic models for the Expense Tracker API.

These models define the "shape" of data going IN and OUT of our API.
Think of them like SQL table definitions — they say:
  - What fields exist
  - What data types they must be
  - Which fields are required vs optional
  - What validation rules apply

Pydantic automatically:
  - Rejects bad data (amount = "banana" → error)
  - Converts compatible types (amount = "45.5" → 45.5)
  - Generates clear error messages for the user
  - Shows up in FastAPI's auto-generated docs (/docs)

Why separate models for Create vs Response?
  - CREATE: The user provides amount + category. They do NOT provide an ID
    (we generate it). So the "input" model has no ID field.
  - RESPONSE: When we send data back, we include the ID we assigned.
    So the "output" model HAS an ID field.
  - UPDATE: The user might want to change just the amount, or just the
    category. So all fields are optional.

This is a very common API pattern you'll see everywhere.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ExpenseCreate(BaseModel):
    """
    Model for CREATING a new expense (what the user sends TO our API).
    
    The user must provide amount and category.
    Description is optional (defaults to empty string).
    
    Notice: No 'id' field here — we generate that in storage.py.
    
    Field() lets us add extra validation rules and documentation:
      - gt=0 means "greater than 0" (no negative or zero amounts)
      - min_length=1 means "at least 1 character" (no empty strings)
      - examples=[...] shows sample values in the API docs
    """
    amount: float = Field(
        ...,  # ... means "this field is required" (no default value)
        gt=0,  # Must be greater than 0 — no $0 or negative expenses
        description="The expense amount in dollars",
        examples=[45.50, 12.99, 100.00]
    )
    category: str = Field(
        ...,  # Required
        min_length=1,  # Can't be empty string
        description="The expense category (e.g., Food, Transport, Entertainment)",
        examples=["Food", "Transport", "Entertainment"]
    )
    description: str = Field(
        default="",  # Optional — defaults to empty string if not provided
        description="Optional description of the expense",
        examples=["Lunch at cafe", "Uber to office"]
    )


class ExpenseUpdate(BaseModel):
    """
    Model for UPDATING an existing expense (partial update).
    
    ALL fields are optional here. The user sends only what they want to change.
    For example, to just fix the amount: {"amount": 50.00}
    The category and description stay the same.
    
    This is like: UPDATE expenses SET amount = 50.00 WHERE id = 3
    (only updates the columns you specify)
    """
    amount: Optional[float] = Field(
        default=None,  # None means "not provided" — don't update this field
        gt=0,  # If provided, must be greater than 0
        description="New amount (only provide if changing)",
        examples=[50.00]
    )
    category: Optional[str] = Field(
        default=None,
        min_length=1,
        description="New category (only provide if changing)",
        examples=["Groceries"]
    )
    description: Optional[str] = Field(
        default=None,
        description="New description (only provide if changing)",
        examples=["Updated description"]
    )


class ExpenseResponse(BaseModel):
    """
    Model for the expense data we send BACK to the user (API response).
    
    This includes the ID that we generated — the user needs this to
    update or delete a specific expense later.
    
    Think of it like a SELECT * FROM expenses — you get all columns back,
    including the auto-generated primary key (id).
    """
    id: int = Field(
        description="Unique identifier for the expense (auto-generated)"
    )
    amount: float = Field(
        description="The expense amount in dollars"
    )
    category: str = Field(
        description="The expense category"
    )
    description: str = Field(
        description="Description of the expense"
    )
