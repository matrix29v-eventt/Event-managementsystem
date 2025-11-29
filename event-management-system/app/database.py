from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection string
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Manu@79@localhost:5432/eventdb"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# ✅ Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
