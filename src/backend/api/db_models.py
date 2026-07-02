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

from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base


class User(Base):
    """
    The 'users' table in our database.

    This is the SQLAlchemy equivalent of:

      CREATE TABLE users (
          id              INTEGER PRIMARY KEY AUTOINCREMENT,
          email           VARCHAR NOT NULL UNIQUE,
          hashed_password VARCHAR NOT NULL,
          created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
      );

    Why store hashed_password and not password?
      Never store plaintext passwords. A hash is a one-way transformation:
      "mysecret" → "$2b$12$...". You can verify a login attempt by hashing
      the incoming password and comparing, but you can never reverse it.
      Actual hashing logic (bcrypt) is added in Phase 3 (auth week).

    Relationship to Expense:
      One User has many Expenses. The FK lives on the Expense side
      (expenses.user_id → users.id), same as in a SQL schema.
      The relationship() below lets you write:
        user.expenses  → list of all Expense rows for that user
    """

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        nullable=False,
        unique=True,   # No two users can share an email — enforced at DB level
        index=True     # Index for fast lookups by email at login
    )

    hashed_password = Column(
        String,
        nullable=False
        # Plaintext passwords are never stored. Phase 3 adds bcrypt hashing.
    )

    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False
    )

    # SQLAlchemy relationship — not a DB column, just a Python convenience.
    # Lets you do: user.expenses → [Expense, Expense, ...]
    # back_populates="user" means Expense.user points back here.
    expenses = relationship("Expense", back_populates="user")


class Expense(Base):
    """
    The 'expenses' table in our database.

    This is the SQLAlchemy equivalent of:

      CREATE TABLE expenses (
          id          INTEGER PRIMARY KEY AUTOINCREMENT,
          amount      DECIMAL(10,2) NOT NULL,
          category    VARCHAR NOT NULL,
          description VARCHAR DEFAULT '',
          created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          user_id     INTEGER REFERENCES users(id)
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

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,  # Nullable for now — Phase 3 auth will enforce this.
        index=True      # Index for fast lookups by user once auth is added.
        # Why nullable? We don't have auth yet, so we can't assign expenses
        # to a real user. Making it nullable avoids having to seed a dummy
        # user just to insert expenses during development.
        # When Phase 3 adds JWT auth, every new expense will have a user_id.
    )

    # Relationship back to User — lets you do: expense.user → User object
    # back_populates="expenses" means User.expenses points back here.
    user = relationship("User", back_populates="expenses")
