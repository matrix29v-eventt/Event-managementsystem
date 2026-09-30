from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.crud import crud
from app.db import get_db
from app.models.models import Client
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.Login, db: Session = Depends(get_db)):
    client: Client = crud.get_client_by_email(db, email=form_data.email)

    if not client or not crud.verify_password(
        form_data.password, client.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": client.email, "role": client.role, "client_id": client.id},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client_id": client.id,
    }
