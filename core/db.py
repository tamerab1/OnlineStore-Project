# Database configuration and session manager
import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE, echo=False)

# Create a configured "Session" Class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()
print("Finished Loading DB..")

@contextmanager
def get_db_session():
    """
    Context manager for database sessions (Bonus A implementation).
    Ensures safe session handling: commit on success, rollback on error, and always close.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Database error occurred: {e}")
        raise
    finally:
        session.close()

def get_db_fastapi():
    # Dependency generator for FastAPI routes.
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
