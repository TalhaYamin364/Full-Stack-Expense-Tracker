"""
In-memory storage for expenses.

This is a temporary solution before we add a real database (SQLite) in Phase 3.
Think of this like a Python list that holds dictionaries - similar to how
your CLI stored expenses, but now accessible to the API.
"""

from typing import List, Dict, Optional

# This will hold all expenses in memory (resets when server restarts)
expenses: List[Dict] = []

# Counter to generate unique IDs for each expense
next_id: int = 1


def add_expense(amount: float, category: str, description: str = "") -> Dict:
    """
    Add a new expense to storage.
    
    Args:
        amount: The expense amount (e.g., 45.50)
        category: The expense category (e.g., "Food", "Transport")
        description: Optional description of the expense
    
    Returns:
        The created expense with its assigned ID
    """
    global next_id
    
    expense = {
        "id": next_id,
        "amount": amount,
        "category": category,
        "description": description
    }
    
    expenses.append(expense)
    next_id += 1
    
    # Console logging to see what's happening
    print(f"✅ Added expense: ID={expense['id']}, Amount=${amount}, Category={category}")
    
    return expense


def get_all_expenses() -> List[Dict]:
    """
    Get all expenses from storage.
    
    Returns:
        List of all expense dictionaries
    """
    print(f"📋 Retrieved {len(expenses)} expenses")
    return expenses


def get_expense_by_id(expense_id: int) -> Optional[Dict]:
    """
    Find a specific expense by its ID.
    
    Args:
        expense_id: The ID of the expense to find
    
    Returns:
        The expense dictionary if found, None otherwise
    """
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None


def delete_expense(expense_id: int) -> bool:
    """
    Delete an expense from storage.
    
    Args:
        expense_id: The ID of the expense to delete
    
    Returns:
        True if deleted, False if not found
    """
    global expenses
    
    for i, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            deleted = expenses.pop(i)
            print(f"🗑️  Deleted expense: ID={deleted['id']}, Amount=${deleted['amount']}")
            return True
    
    return False
