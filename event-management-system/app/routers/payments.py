# app/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.auth import get_current_client, role_required
from app.notifications import send_payment_receipt

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/my-payments", response_model=List[schemas.Payment])
def read_my_payments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_client),
):
    return crud.get_payments_by_client(db, client_id=current_user.id)


# POLICY: Admin Only (Creation/Processing)
@router.post("/", response_model=schemas.Payment, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),  # Requires admin role
):
    db_payment = crud.create_payment(db=db, payment=payment)

    try:
        db_event = crud.get_event(db, payment.event_id)
        if db_event:
            db_client = crud.get_client(db, db_event.client_id)
            if db_client:
                send_payment_receipt(
                    client_email=db_client.email,
                    client_name=db_client.name,
                    payment_id=db_payment.id,
                    event_name=db_event.name,
                    amount=payment.amount,
                    method=payment.method,
                    status=payment.status,
                )
    except Exception as e:
        print(f"Failed to send payment notification: {e}")

    return db_payment


# POLICY: Admin Only (Read All/Management)
@router.get("/", response_model=List[schemas.Payment])
def read_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),  # Requires admin role
):
    payments = crud.get_payments(db, skip=skip, limit=limit)
    return payments


# POLICY: Admin Only (Read Single)
@router.get("/{payment_id}", response_model=schemas.Payment)
def read_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),  # Requires admin role
):
    db_payment = crud.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.put("/{payment_id}", response_model=schemas.Payment)
def update_payment(
    payment_id: int,
    payment: schemas.PaymentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),
):
    db_payment = crud.update_payment(
        db, payment_id, payment.model_dump(exclude_unset=True)
    )
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),
):
    if not crud.delete_payment(db, payment_id):
        raise HTTPException(status_code=404, detail="Payment not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
