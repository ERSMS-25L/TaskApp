import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from models import Task, Base

# Get the database URL from environment variables or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite_task.db")

# Create a new SQLite engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Dummy data to insert
dummy_tasks = [
    Task(
        title="Buy groceries",
        description="Milk, Eggs, Bread",
        due_date=datetime.utcnow() + timedelta(days=1),
        user_id=1,
    ),
    Task(
        title="Finish report",
        description="Complete the financial report",
        due_date=datetime.utcnow() + timedelta(days=2),
        user_id=2,
    ),
]

# Add the dummy tasks to the session
session.add_all(dummy_tasks)

# Commit the session
session.commit()

# Close the session
session.close()

print("Dummy tasks added successfully!")
