from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from database import Base


class Task(Base):
    """Database model for a task."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime, default=None)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, nullable=False)
