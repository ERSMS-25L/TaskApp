from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import User
from database import get_db  # Make sure to define this in your database file

router = APIRouter()

@router.post("/users/", response_model=dict)
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if the user already exists
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Username or email already registered.")
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Hash the password before saving
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user_id": new_user.id, "username": new_user.username, "email": new_user.email}

@router.get("/users/", response_model=List[dict])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]

@router.get("/users/{user_id}", response_model=dict)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}
