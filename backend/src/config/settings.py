"""
© 2025 NipunAI. All Rights Reserved.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default to PostgreSQL if not set in .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/nipunai")
