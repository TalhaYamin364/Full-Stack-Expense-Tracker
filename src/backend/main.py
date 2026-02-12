"""
Expense Tracker Application

A simple command-line application for tracking personal expenses.
Users can add expenses, view all expenses, calculate totals, and filter by category.

This module demonstrates:
- Functional programming with map() and filter()
- User input handling and validation
- Basic data management with dictionaries and lists
"""

from typing import List, Dict, Iterator, Any, Union

# Menu option constants
OPTION_ADD = "1"
OPTION_LIST = "2"
OPTION_TOTAL = "3"
OPTION_FILTER = "4"
OPTION_EXIT = "5"


def add_expense(expenses: List[Dict[str, Any]], amount: float, category: str) -> None:
    """
    Add a new expense to the expenses list.

    Args:
        expenses: List of expense dictionaries to append to
        amount: The monetary amount of the expense
        category: The category of the expense (e.g., 'food', 'transport')

    Returns:
        None (modifies the expenses list in place)
    """
    expenses.append({"amount": amount, "category": category})
    print(f"✓ Expense of ${amount:.2f} added to '{category}' category.")


def print_expenses(
    expenses: Union[List[Dict[str, Any]], Iterator[Dict[str, Any]]],
) -> None:
    """
    Print all expenses in a formatted manner.

    Args:
        expenses: List of expense dictionaries or an iterator of expenses

    Returns:
        None (prints to console)
    """
    # Convert to list if it's an iterator (from filter())
    expense_list = list(expenses) if not isinstance(expenses, list) else expenses

    if not expense_list:
        print("No expenses to display.")
        return

    # Print header
    print(f"\n{'Amount':<15} {'Category':<20}")
    print("-" * 35)

    # Print each expense with formatting
    for expense in expense_list:
        amount = expense["amount"]
        category = expense["category"]
        print(f"${amount:<14.2f} {category:<20}")

    print("-" * 35)


def total_expenses(expenses: List[Dict[str, Any]]) -> float:
    """
    Calculate the total sum of all expenses.

    Uses the map() function to extract amounts and sum() to calculate total.

    Args:
        expenses: List of expense dictionaries

    Returns:
        The total sum of all expense amounts
    """
    return sum(map(lambda expense: expense["amount"], expenses))


def filter_expenses_by_category(
    expenses: List[Dict[str, Any]], category: str
) -> Iterator[Dict[str, Any]]:
    """
    Filter expenses by a specific category.

    Uses the filter() function to return only expenses matching the category.
    Note: Returns an iterator, not a list.

    Args:
        expenses: List of expense dictionaries
        category: The category to filter by (case-insensitive)

    Returns:
        An iterator of expense dictionaries matching the category
    """
    # Make comparison case-insensitive for better user experience
    return filter(
        lambda expense: expense["category"].lower() == category.lower(), expenses
    )


def get_valid_amount() -> float:
    """
    Prompt user for a valid expense amount with input validation.

    Continues prompting until a valid positive number is entered.

    Returns:
        A valid positive float amount
    """
    while True:
        try:
            amount = float(input("Enter amount: $"))
            if amount <= 0:
                print("Error: Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Error: Please enter a valid number.")


def get_valid_category() -> str:
    """
    Prompt user for a valid category name.

    Ensures the category is not empty and strips whitespace.

    Returns:
        A valid non-empty category string
    """
    while True:
        category = input("Enter category: ").strip()
        if not category:
            print("Error: Category cannot be empty.")
            continue
        return category


def display_menu() -> None:
    """
    Display the main menu options to the user.

    Returns:
        None (prints to console)
    """
    print("\n" + "=" * 40)
    print("       EXPENSE TRACKER")
    print("=" * 40)
    print(f"{OPTION_ADD}. Add an expense")
    print(f"{OPTION_LIST}. List all expenses")
    print(f"{OPTION_TOTAL}. Show total expenses")
    print(f"{OPTION_FILTER}. Filter expenses by category")
    print(f"{OPTION_EXIT}. Exit")
    print("=" * 40)


def main() -> None:
    """
    Main function to run the Expense Tracker application.

    Provides a menu-driven interface for managing expenses. Runs in a loop
    until the user chooses to exit.

    Returns:
        None
    """
    # Initialize empty list to store all expenses
    expenses = []

    # Main application loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == OPTION_ADD:
            # Add a new expense with validated input
            amount = get_valid_amount()
            category = get_valid_category()
            add_expense(expenses, amount, category)

        elif choice == OPTION_LIST:
            # Display all expenses
            print("\nAll Expenses:")
            print_expenses(expenses)

        elif choice == OPTION_TOTAL:
            # Calculate and display total expenses
            total = total_expenses(expenses)
            print(f"\nTotal Expenses: ${total:.2f}")

            # Show count of expenses
            print(f"Number of expenses: {len(expenses)}")

        elif choice == OPTION_FILTER:
            # Filter and display expenses by category
            if not expenses:
                print("\nNo expenses to filter.")
                continue

            category = input("Enter category to filter: ").strip()
            print(f"\nExpenses for '{category}':")

            # Get filtered expenses and display
            filtered_expenses = filter_expenses_by_category(expenses, category)
            print_expenses(filtered_expenses)

        elif choice == OPTION_EXIT:
            # Exit the application
            print("\n" + "=" * 40)
            print("Thank you for using Expense Tracker!")
            print(f"Total expenses tracked: {len(expenses)}")
            if expenses:
                print(f"Total amount: ${total_expenses(expenses):.2f}")
            print("=" * 40)
            break

        else:
            # Handle invalid menu choices
            print("\n⚠ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
