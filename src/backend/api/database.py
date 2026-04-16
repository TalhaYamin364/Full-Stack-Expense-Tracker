"""
Database Configuration — SQLAlchemy + SQLite Setup.

This file creates the "connection" between Python and the SQLite database.
Think of it like opening a connection in any SQL tool (DBeaver, pgAdmin, etc.)
but in code.

Three things happen here:
  1. create_engine()  → Connects to the database file
  2. SessionLocal()   → Creates "sessions" for running queries
  3. Base             → The parent class all our table models inherit from

What is a Session?
  In SQL tools, you open a connection and run queries against it.
  A SQLAlchemy Session is the same concept:
    - Open a session
    - Run queries (SELECT, INSERT, UPDATE, DELETE)
    - Commit the changes (like clicking "Execute" in your SQL tool)
    - Close the session

  Every API request gets its own session — this prevents requests
  from interfering with each other.

What is Base?
  Base is a parent class from SQLAlchemy. When we define a table like:
    class Expense(Base):
        __tablename__ = "expenses"
        id = Column(Integer, primary_key=True)

  SQLAlchemy knows this class represents a database table because
  it inherits from Base. Base keeps track of ALL our table classes
  so it can create them with Base.metadata.create_all().
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ─── DATABASE URL ──────────────────────────────────────────
# sqlite:///  = use SQLite (file-based database)
# ./expenses.db = store the database file in the current directory
#   (this will be src/backend/expenses.db when we run the server)
#
# Compare to other databases:
#   PostgreSQL: "postgresql://user:pass@localhost:5432/mydb"
#   MySQL:      "mysql://user:pass@localhost:3306/mydb"
#   SQLite:     "sqlite:///./expenses.db"  (no user/pass needed!)
DATABASE_URL = "sqlite:///./expenses.db"

# ─── ENGINE ────────────────────────────────────────────────
# The engine is the "starting point" of SQLAlchemy.
# It manages the actual connection to the database file.
#
# connect_args={"check_same_thread": False}
#   This is SQLite-specific. SQLite normally only allows one thread
#   to use a connection at a time. Our FastAPI server handles multiple
#   requests, so we need to allow cross-thread access.
#   (PostgreSQL/MySQL don't need this setting.)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ─── SESSION FACTORY ───────────────────────────────────────
# sessionmaker creates a "factory" that produces database sessions.
# Each time we call SessionLocal(), we get a new session.
#
# autocommit=False → We control when changes are saved (explicit commit)
# autoflush=False  → We control when Python objects sync to the DB
#
# This is like preparing a template for database connections:
#   session = SessionLocal()   ← open a connection
#   session.query(...)         ← run queries
#   session.commit()           ← save changes
#   session.close()            ← close connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ─── BASE CLASS ────────────────────────────────────────────
# All our database table classes will inherit from this Base.
# This tells SQLAlchemy: "this Python class is a database table."
#
# class Expense(Base):    ← SQLAlchemy knows this is a table
# class User(Base):       ← SQLAlchemy knows this is a table too
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session to each API request.

    FastAPI's "Dependency Injection" system calls this function
    automatically for any route that needs a database session.

    How it works:
      1. Creates a new session (like opening a SQL connection)
      2. Gives it to the route function (via `yield`)
      3. After the route finishes, closes the session (via `finally`)

    The `yield` keyword makes this a "generator" — it pauses at yield,
    lets the route do its work, then continues to the finally block.

    This pattern ensures sessions are ALWAYS closed, even if an error
    occurs. You'll see this called "dependency injection" — FastAPI
    automatically provides the database session to any route that asks for it.

    Usage in routes:
      @router.get("/")
      def list_expenses(db: Session = Depends(get_db)):
          # 'db' is automatically created and closed by get_db()
          ...

    In SQL terms: this is like a connection pool that opens and closes
    connections for each query, preventing connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
