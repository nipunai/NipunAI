"""
© 2025 NipunAI. All Rights Reserved.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.subscription import Subscription
from src.services.auth_service import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/")
def create_subscription(plan_type: str, use_case: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] not in ["admin", "enterprise_user"]:
        raise HTTPException(status_code=403, detail="Only enterprise users can subscribe")
    
    new_subscription = Subscription(user_id=user["id"], plan_type=plan_type, use_case=use_case)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

@router.get("/{subscription_id}")
def get_subscription(subscription_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.user_id != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this subscription")
    return subscription
