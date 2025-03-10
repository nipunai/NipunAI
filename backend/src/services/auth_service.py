"""
© 2025 NipunAI. All Rights Reserved.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.services.jwt_handler import create_access_token, verify_access_token
from src.config.database import get_db
from src.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(email: str, password: str, role: str = "enterprise_user", db: Session = Depends(get_db)):
    """Register a new user with hashed password and store in PostgreSQL."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create new user entry
    new_user = User(email=email, hashed_password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "email": new_user.email, "role": new_user.role}


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token if credentials are valid."""
    # Fetch user from DB
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

    # Generate JWT token
    return create_access_token({"email": user.email, "role": user.role})


def get_current_user(token: str = Depends(verify_access_token), db: Session = Depends(get_db)):
    """Retrieve current user from the database based on the JWT token."""
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from DB
    user = db.query(User).filter(User.email == payload.get("email")).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
