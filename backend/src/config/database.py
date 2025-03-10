"""
© 2025 NipunAI. All Rights Reserved.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch database URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
