# Use the official Python 3.9 image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and the dummy data script
COPY ./app /app

# Copy Alembic configuration files
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# Copy the dummy data population script into the container
COPY ./app/populate_db.py /app/populate_db.py  

# Install required packages
RUN pip install fastapi uvicorn sqlalchemy psycopg2 passlib[bcrypt] alembic

# Command to run the dummy data population script followed by the FastAPI app
CMD ["sh", "-c", "python populate_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
