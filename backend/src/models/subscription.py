"""
© 2025 NipunAI. All Rights Reserved.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base  # Import the same Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_type = Column(String)  # Free, Pro, Enterprise
    use_case = Column(String)  # Climate, Remote Sensing, etc.

    user = relationship("User", back_populates="subscriptions")

