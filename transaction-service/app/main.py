import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import router  # Importing the router

app = FastAPI()

# Fetch the allowed origins from an environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for transactions
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Transaction Service is up and running!"}

@app.get("/api/health")
def health_check():
    return JSONResponse(content={"status": "Transaction Service is running!"}, status_code=200)
