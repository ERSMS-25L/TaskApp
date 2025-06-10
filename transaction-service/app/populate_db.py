import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Transaction, Base

# Get the database URL from environment variables or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite_transaction.db")

# Create a new SQLite engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Dummy data to insert
dummy_transactions = [
    Transaction(amount=100.50, type='credit', user_id=1),
    Transaction(amount=50.75, type='debit', user_id=2),
    Transaction(amount=200.00, type='credit', user_id=1),
    Transaction(amount=150.25, type='debit', user_id=3),
]

# Add the dummy transactions to the session
session.add_all(dummy_transactions)

# Commit the session
session.commit()

# Close the session
session.close()

print("Dummy data added successfully!")
