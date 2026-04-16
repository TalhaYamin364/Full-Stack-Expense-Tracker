"""
SQLAlchemy Database Models — Table Definitions.

These classes define the STRUCTURE of our database tables.
Each class = one table. Each attribute = one column.

Compare to SQL:
  class Expense(Base)         →  CREATE TABLE expenses (...)
  id = Column(Integer, ...)   →  id INTEGER PRIMARY KEY AUTOINCREMENT
  amount = Column(Numeric, ...)→  amount DECIMAL(10,2) NOT NULL

Why is this separate from models.py?
  models.py   = Pydantic models = API validation (what comes IN/OUT)
  db_models.py = SQLAlchemy models = database schema (what gets STORED)

  They look similar but serve different purposes:
  - Pydantic checks: "Is this a valid API request?"
  - SQLAlchemy defines: "What does the database table look like?"

  In SQL terms:
  - Pydantic = input validation (like CHECK constraints on forms)
  - SQLAlchemy = DDL (CREATE TABLE, column types, foreign keys)

Naming Convention:
  We use 'Expense' for the SQLAlchemy model (the table).
  Pydantic models use 'ExpenseCreate', 'ExpenseResponse', etc.
  This keeps them easy to tell apart.
"""

from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func
from api.database import Base


class Expense(Base):
    """
    The 'expenses' table in our database.

    This is the SQLAlchemy equivalent of:

      CREATE TABLE expenses (
          id          INTEGER PRIMARY KEY AUTOINCREMENT,
          amount      DECIMAL(10,2) NOT NULL,
          category    VARCHAR NOT NULL,
          description VARCHAR DEFAULT '',
          created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
      );

    Each instance of this class represents ONE ROW in the table.
    For example:
      expense = Expense(amount=45.50, category="Food", description="Lunch")
      ↓ is the same as ↓
      INSERT INTO expenses (amount, category, description) VALUES (45.50, 'Food', 'Lunch');
    """

    # __tablename__ tells SQLAlchemy what to call this table in the database.
    # Without it, SQLAlchemy would use the class name "Expense" — but we
    # want "expenses" (plural, lowercase) to follow SQL naming conventions.
    __tablename__ = "expenses"

    # ─── COLUMNS ───────────────────────────────────────────
    # Each Column() maps to a column in the SQL table.
    #
    # Column(Type, constraints...)
    #   Type        = Integer, Float, String, Boolean, DateTime, etc.
    #   primary_key = this is the PRIMARY KEY (auto-incremented by SQLite)
    #   nullable    = can this column be NULL? (False = NOT NULL)
    #   default     = default value if not provided
    #   index       = create an index on this column (faster lookups)

    id = Column(
        Integer,
        primary_key=True,   # PRIMARY KEY — auto-incremented by SQLite
        index=True          # Creates an index for faster lookups by ID
    )

    amount = Column(
        Numeric(10, 2),     # DECIMAL(10,2) — fixed-point, not floating-point
        nullable=False      # NOT NULL — every expense must have an amount
        # Why Numeric instead of Float?
        #   Float has precision errors: 0.1 + 0.2 = 0.30000000000000004
        #   Numeric(10, 2) stores exact values up to 99,999,999.99
        #   Always use fixed-point types for money. Same as DECIMAL in SQL.
    )

    category = Column(
        String,
        nullable=False,     # NOT NULL — every expense must have a category
        index=True          # Index for faster filtering by category
    )

    description = Column(
        String,
        default=""          # DEFAULT '' — if not provided, use empty string
    )

    created_at = Column(
        DateTime,
        default=func.now(),  # DB-side DEFAULT CURRENT_TIMESTAMP
        nullable=False
        # Why func.now() instead of datetime.utcnow?
        #   func.now() = database generates the timestamp (like DEFAULT CURRENT_TIMESTAMP)
        #   datetime.utcnow = Python generates the timestamp on the app server
        #   DB-side is more reliable — doesn't depend on the app server's clock.
    )
