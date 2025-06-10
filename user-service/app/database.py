from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the DATABASE_URL from environment variables or use a default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db/user_db")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
