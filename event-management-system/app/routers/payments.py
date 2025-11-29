# app/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.auth import get_current_client, role_required

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# POLICY: Admin Only (Creation/Processing)
@router.post("/", response_model=schemas.Payment, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: schemas.PaymentCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin")) # Requires admin role
):
    return crud.create_payment(db=db, payment=payment)

# POLICY: Admin Only (Read All/Management)
@router.get("/", response_model=List[schemas.Payment])
def read_payments(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin")) # Requires admin role
):
    payments = crud.get_payments(db, skip=skip, limit=limit)
    return payments

# POLICY: Admin Only (Read Single)
@router.get("/{payment_id}", response_model=schemas.Payment)
def read_payment(
    payment_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin")) # Requires admin role
):
    db_payment = crud.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

# Add PUT/DELETE endpoints here and protect them with role_required("admin")