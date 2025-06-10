from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Transaction
from database import get_db

router = APIRouter()

class TransactionCreate(BaseModel):
    amount: float
    type: str
    user_id: int

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    user_id: int

    class Config:
        orm_mode = True

@router.post("/transactions/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/transactions/", response_model=list[TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()  # Fetch all transactions
    return transactions
