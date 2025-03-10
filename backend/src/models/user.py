"""
© 2025 NipunAI. All Rights Reserved.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="enterprise_user")  # Super Admin, Enterprise Admin, Enterprise User
    is_active = Column(Boolean, default=True)

    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
