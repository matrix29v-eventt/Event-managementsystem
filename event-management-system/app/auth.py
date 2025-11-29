from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models.models import Client
from app.schemas.schemas import TokenData
from app.crud.crud import get_client_by_email # Need to adjust get_client_by_email later
from app.db import get_db

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone 


load_dotenv()

# Configuration from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2PasswordBearer for dependency injection in routers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token") 

# --- Token Management ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    
    # 💡 FIX: Use timezone-aware 'now' instead of utcnow()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # JWT 'exp' claim expects a timestamp (integer), so we use .timestamp()
    to_encode.update({"exp": expire.timestamp()}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependencies for Authorization ---

async def get_current_client(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Decodes and validates the JWT, returning the associated Client object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # 'sub' is standard for subject
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception
    
    # Retrieve the client from the database
    client = get_client_by_email(db, email=token_data.email)
    if client is None:
        raise credentials_exception
    return client

# --- Role-based Authorization Dependency ---

def role_required(required_role: str):
    """
    Dependency to check if the current user has the required role.
    Usage: Depends(role_required("admin"))
    """
    def role_checker(current_client: Client = Depends(get_current_client)):
        if current_client.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized. Requires role: {required_role}"
            )
        return current_client
    return role_checker