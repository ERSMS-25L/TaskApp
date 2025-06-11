# notification-service/main.py
import os
import requests

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()
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
notifications = []

# URL of the task service to check for upcoming deadlines
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://task-service:8000")


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


async def fetch_due_tasks(days: int = 1):
    """Fetch tasks that are due within a given number of days from the task service."""
    url = f"{TASK_SERVICE_URL}/api/tasks/due_soon/?days={days}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


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


@app.post("/send-deadline-reminders", response_model=List[NotificationResponse])
async def send_deadline_reminders(days: int = 1):
    """Fetch tasks due soon and create notifications for them."""
    due_tasks = await fetch_due_tasks(days)
    created = []
    for task in due_tasks:
        notification_id = len(notifications) + 1
        message = f"Task '{task['title']}' is due on {task['due_date']}"
        new_notification = {
            "id": notification_id,
            "message": message,
            "recipient": f"user{task['user_id']}@example.com",
            "notification_type": "email",
        }
        notifications.append(new_notification)
        created.append(new_notification)
    return created


@app.post("/send-email-notification")
def send_email_notification(message: str, subject: str, recipient: str):
    r = requests.post(
        os.getenv("MAILGUN_URL"),
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": os.getenv(
                "MAILGUN_FROM",
                "Task App <postmaster@sandbox5455a55c8dd84d8c9b693c73d48de8d1.mailgun.org>",
            ),
            "to": recipient,
            "subject": subject,
            "text": message,
        },
    )
    if r.status_code == 200:
        return JSONResponse(
            content={"message": "Email sent successfully"}, status_code=200
        )
    else:
        raise HTTPException(
            status_code=r.status_code,
            detail=f"Failed to send email: {r.text}",
        )


@app.get("/api/health")
async def health_check():
    return JSONResponse(
        content={"status": "Notification Service is running!"}, status_code=200
    )
