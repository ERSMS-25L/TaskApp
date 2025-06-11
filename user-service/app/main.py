import os
import json
import firebase_admin
from firebase_admin import credentials
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

# Firebase initialization
cred = None
cred_path = os.getenv("FIREBASE_CREDENTIALS")
cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

if cred_path and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
elif cred_json:
    try:
        cred = credentials.Certificate(json.loads(cred_json))
    except Exception:
        pass

if cred:
    firebase_admin.initialize_app(cred)
else:
    # Initialize with default credentials if service account not provided
    firebase_admin.initialize_app()

@app.get("/")
def read_root():
    return {"message": "User Service is up and running!"}

@app.get("/api/health")
def health_check():
    return JSONResponse(content={"status": "User Service is running!"}, status_code=200)

# Include the user routes
app.include_router(user_router, prefix="/api", tags=["users"])
