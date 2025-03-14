"""
© 2025 NipunAI. All Rights Reserved.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    return {"message": "List of users"}
