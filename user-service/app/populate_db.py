import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Base  # Import your User model and Base

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite_user.db")

# Create a new SQLite engine
engine = create_engine(DATABASE_URL)

# Drop all tables and recreate them to ensure schema is up to date
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Dummy data to insert (without passwords, firebase_uid will be None for dummy users)
dummy_users = [
    User(username="john_doe", email="john@example.com", firebase_uid=None),
    User(username="jane_smith", email="jane@example.com", firebase_uid=None),
    User(username="alice_johnson", email="alice@example.com", firebase_uid=None),
    User(username="bob_brown", email="bob@example.com", firebase_uid=None),
]

# Iterate through the dummy users and add them to the session
for user in dummy_users:
    try:
        session.add(user)
        session.commit()  # Commit after each insert to check for uniqueness
    except IntegrityError:
        session.rollback()  # Rollback the session on error
        print(f"User with email {user.email} already exists, skipping.")

# Close the session
session.close()

print("Dummy data added successfully!")
