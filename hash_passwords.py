   # hash_passwords.py
from passlib.context import CryptContext

   # Initialize the password hashing context
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

   # List of users with plain passwords
   users = [
       ('user1', 'user1@example.com', 'password1'),
       ('user2', 'user2@example.com', 'password2'),
       ('user3', 'user3@example.com', 'password3'),
   ]

   # Hash the passwords
   hashed_users = [(username, email, pwd_context.hash(password)) for username, email, password in users]

   # Print the SQL insert statements
   for username, email, hashed_password in hashed_users:
       print(f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{hashed_password}');")