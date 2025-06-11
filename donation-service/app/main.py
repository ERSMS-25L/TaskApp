# donation-service/main.py
import os
import stripe
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import DonationRequest, DonationResponse

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_...")


@app.post("/donate", response_model=DonationResponse)
async def create_donation_link(donation: DonationRequest):
    """Create a Stripe payment link for donation."""
    try:
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": donation.currency,
                        "product_data": {
                            "name": donation.description or "Donation",
                        },
                        "unit_amount": donation.amount,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=os.getenv(
                "DONATION_SUCCESS_URL", "http://localhost:3000/success"
            ),
            cancel_url=os.getenv("DONATION_CANCEL_URL", "http://localhost:3000/cancel"),
            customer_email=donation.donor_email,
            metadata={
                "donor_name": donation.donor_name or "",
                "description": donation.description or "Donation",
            },
        )

        return DonationResponse(
            payment_url=checkout_session.url,
            session_id=checkout_session.id,
            amount=donation.amount,
            currency=donation.currency,
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/get-charity-links")
async def get_charity_links():
    charity_links = [
        {
            "name": "Friends of Animals",
            "url": "https://interland3.donorperfect.net/weblink/WebLink.aspx?name=E344259&id=3",
        },
        {
            "name": "Childhood Cancer Research Trust",
            "url": "https://childhoodcancerresearchtrust.org/product/donation/",
        },
        {
            "name": "WWF",
            "url": "https://gifts.worldwildlife.org/gift-center/one-time-donation?srsltid=AfmBOooBqiPbFOMVbuyhrH1kQYEQUGbKufESEBoYo3GkGhODCLOg91hE",
        },
    ]
    return JSONResponse(content=charity_links, status_code=200)


@app.get("/api/health")
async def health_check():
    return JSONResponse(
        content={"status": "Donation Service is running!"}, status_code=200
    )
