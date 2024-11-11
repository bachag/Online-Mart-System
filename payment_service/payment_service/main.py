from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel
from payment_service import crud, schemas
from payment_service.db import create_db_and_tables, get_session
from payment_service.schemas import PaymentCreate, PaymentResponse, PaymentList, PaymentDetail

from typing import List
from contextlib import asynccontextmanager
import stripe
from payment_service.settings import STRIPE_API_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET

stripe.api_key = str(STRIPE_API_KEY)  # Set the API key

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Call create_db_and_tables to ensure the tables are created
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/payment", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_session)):
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),
            currency="usd",
            metadata={'order_id': payment.order_id},
            automatic_payment_methods={'enabled': True}
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_payment = crud.create_payment(db, payment)
    db_payment.client_secret = intent.client_secret
    return db_payment


@app.get("/payment/{payment_id}", response_model=PaymentDetail)
def get_payment_by_id(payment_id: int, db: Session = Depends(get_session)):
    payment = crud.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.get("/payment", response_model=List[PaymentList])
def get_payment(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_payment(db, skip, limit)

@app.put("/payment/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_session)):
    updated_payment = crud.update_payment(db, payment_id, payment)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment

@app.delete("/payment/{payment_id}", response_model=PaymentResponse)
async def delete_payment(payment_id: int, db: Session = Depends(get_session)):
    deleted_payment = crud.delete_payment(db, payment_id)
    if not deleted_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return deleted_payment
