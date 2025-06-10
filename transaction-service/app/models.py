from sqlalchemy import Column, Integer, Float, String
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)
    user_id = Column(Integer)
