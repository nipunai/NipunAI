"""
© 2025 NipunAI. All Rights Reserved.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/climate", tags=["Climate Modeling"])

@router.get("/")
def get_climate_data():
    return {"message": "Climate modeling data"}
