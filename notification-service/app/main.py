# notification-service/main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

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

# Dummy in-memory storage for notifications
notifications = [
    {"id": 1, "message": "Your payment was successful!", "recipient": "user1@example.com", "notification_type": "email"},
    {"id": 2, "message": "New transaction alert: $50 deposited.", "recipient": "user2@example.com", "notification_type": "SMS"},
    {"id": 3, "message": "Account verification needed.", "recipient": "user3@example.com", "notification_type": "email"},
]

# Models
class NotificationRequest(BaseModel):
    message: str
    recipient: str
    notification_type: str  # e.g., "email", "sms", "push"

class NotificationResponse(BaseModel):
    id: int
    message: str
    recipient: str
    notification_type: str

# Endpoints

@app.post("/send-notification", response_model=NotificationResponse)
async def send_notification(notification: NotificationRequest):
    # Generate a dummy notification ID and store the notification
    notification_id = len(notifications) + 1
    new_notification = {
        "id": notification_id,
        "message": notification.message,
        "recipient": notification.recipient,
        "notification_type": notification.notification_type,
    }
    notifications.append(new_notification)
    return new_notification

@app.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications():
    """Retrieve all sent notifications."""
    return notifications

@app.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: int):
    """Retrieve a single notification by ID."""
    notification = next((n for n in notifications if n["id"] == notification_id), None)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.get("/api/health")
async def health_check():
    return JSONResponse(content={"status": "Notification Service is running!"}, status_code=200)
