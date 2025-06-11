from pydantic import BaseModel
from typing import Optional


class DonationRequest(BaseModel):
    amount: int  # Amount in cents (e.g., 1000 = $10.00)
    currency: str = "usd"
    donor_email: Optional[str] = None
    donor_name: Optional[str] = None
    description: Optional[str] = "Donation"


class DonationResponse(BaseModel):
    payment_url: str
    session_id: str
    amount: int
    currency: str
