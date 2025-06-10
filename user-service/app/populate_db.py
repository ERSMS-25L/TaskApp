import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Base  # Import your User model and Base

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite_user.db")

# Create a new SQLite engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Dummy data to insert (without passwords)
dummy_users = [
    User(username='john_doe', email='john@example.com'),
    User(username='jane_smith', email='jane@example.com'),
    User(username='alice_johnson', email='alice@example.com'),
    User(username='bob_brown', email='bob@example.com'),
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
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Base  # Import your User model and Base

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite_user.db")

# Create a new SQLite engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Dummy data to insert (without passwords)
dummy_users = [
    User(username='john_doe', email='john@example.com'),
    User(username='jane_smith', email='jane@example.com'),
    User(username='alice_johnson', email='alice@example.com'),
    User(username='bob_brown', email='bob@example.com'),
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
