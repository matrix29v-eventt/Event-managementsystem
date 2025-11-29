# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from datetime import timedelta

# from app.db import get_db
# from app.crud.crud import get_client_by_email, verify_password # Need to adjust get_client_by_email later
# from app.schemas.schemas import Token, Login
# from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# from app.models.models import Client

# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"]
# )

# @router.post("/token", response_model=Token)
# def login_for_access_token(
#     form_data: Login, # Using Login schema instead of OAuth2PasswordRequestForm for simplicity
#     db: Session = Depends(get_db)
# ):
#     """
#     Authenticate a client and return an access token.
#     """
#     client: Client = get_client_by_email(db, email=form_data.email)
    
#     if not client or not verify_password(form_data.password, client.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     # Subject 'sub' is the email, 'role' is for authorization
#     access_token = create_access_token(
#         data={"sub": client.email, "role": client.role},
#         expires_delta=access_token_expires
#     )
    
#     return {"access_token": access_token, "token_type": "bearer"}

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.crud import crud 
from app.db import get_db
from app.models.models import Client

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_client(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        client_id: int = payload.get("client_id") # Get ID from payload
        if email is None or role is None or client_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, role=role, client_id=client_id)
    except JWTError:
        raise credentials_exception
    
    client = crud.get_client_by_email(db, email=token_data.email)
    if client is None:
        raise credentials_exception
    return client

def role_required(required_role: str):
    def role_checker(current_client: Client = Depends(get_current_client)):
        if current_client.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized. Requires role: {required_role}"
            )
        return current_client
    return role_checker

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: schemas.Login, 
    db: Session = Depends(get_db)
):
    client: Client = crud.get_client_by_email(db, email=form_data.email)
    
    if not client or not crud.verify_password(form_data.password, client.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 💡 FIX: Include client_id in the token payload
    access_token = create_access_token(
        data={"sub": client.email, "role": client.role, "client_id": client.id},
        expires_delta=access_token_expires
    )
    
    # 💡 FIX: Return client_id in the response body
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "client_id": client.id
    }