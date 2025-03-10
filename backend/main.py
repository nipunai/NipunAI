"""
© 2025 NipunAI. All Rights Reserved.
"""

import os
from fastapi import FastAPI
from src.api import auth
from src.api import users  # Fix import issue
from src.api import subscriptions, climate, remote_sensing
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(climate.router)
app.include_router(remote_sensing.router)

@app.get("/")
def root():
    return {"message": "Welcome to NipunAI Backend"}


