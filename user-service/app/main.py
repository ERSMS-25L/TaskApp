import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db  # Ensure get_db is defined in your database file
from routes import router as user_router  # Import the user routes

app = FastAPI()

# Fetch the allowed origins from an environment variable, with a default fallback
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite_user.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Required for SQLite
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "User Service is up and running!"}

@app.get("/api/health")
def health_check():
    return JSONResponse(content={"status": "User Service is running!"}, status_code=200)

# Include the user routes
app.include_router(user_router, prefix="/api", tags=["users"])
