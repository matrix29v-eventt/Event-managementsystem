from sqlalchemy import create_engine
# 💡 FIX: Updated import path to sqlalchemy.orm for V2 compatibility
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)

# SessionLocal will be used in routers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency: each request gets a fresh database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()