"""
© 2025 NipunAI. All Rights Reserved.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/remote-sensing", tags=["Remote Sensing"])

@router.get("/")
def get_satellite_data():
    return {"message": "Remote sensing satellite data"}
