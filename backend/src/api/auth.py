"""
© 2025 NipunAI. All Rights Reserved.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.services.auth_service import register_user, authenticate_user, get_current_user
from src.services.jwt_handler import verify_access_token
from src.config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    email: str
    password: str
    role: str = "enterprise_user"  # Default role

class UserLogin(BaseModel):
    email: str
    password: str

def check_admin(user: dict = Depends(verify_access_token)):
    """Restrict access to admin users only."""
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only!"
        )
    return user

def require_admin(user: dict = Depends(verify_access_token)):
    """Ensure only admin users can access certain routes."""
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_enterprise_user(user: dict = Depends(verify_access_token)):
    """Ensure only enterprise users can access certain routes."""
    if user["role"] not in ["admin", "enterprise_user"]:
        raise HTTPException(status_code=403, detail="Enterprise access required")
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    return register_user(user.email, user.password, user.role, db=db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(user.email, user.password, db=db)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_route(user: dict = Depends(verify_access_token)):  
    """Get details of the currently logged-in user."""
    return {"email": user["email"], "role": user["role"]}

@router.get("/admin")
def admin_route(user: dict = Depends(check_admin)):
    """Restricted route for admin users."""
    return {"message": "Welcome, Admin!"}

