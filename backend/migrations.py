"""
© 2025 NipunAI. All Rights Reserved.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import DATABASE_URL
from src.models.user import Base as UserBase
from src.models.subscription import Base as SubscriptionBase

# Initialize PostgreSQL Database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_migrations():
    print("🔄 Applying Database Migrations...")
    UserBase.metadata.create_all(bind=engine)
    SubscriptionBase.metadata.create_all(bind=engine)
    print("✅ Migrations Applied Successfully.")

if __name__ == "__main__":
    run_migrations()
