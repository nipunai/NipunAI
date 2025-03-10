#!/bin/bash

echo "🚀 Starting NipunAI Backend Setup..."

# Step 1: Ensure virtual environment exists and activate it
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

source venv/bin/activate
echo "✅ Virtual environment activated."

# Step 2: Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python dependencies installed."

# Step 3: Check & Install PostgreSQL
if ! command -v psql &> /dev/null
then
    echo "🔧 Installing PostgreSQL..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
fi

# Step 4: Check & Install MongoDB
if ! command -v mongod &> /dev/null
then
    echo "🔧 Installing MongoDB..."
    sudo apt update
    sudo apt install -y mongodb
    sudo systemctl start mongodb
    sudo systemctl enable mongodb
fi

echo "✅ PostgreSQL and MongoDB installed."

# Step 5: Apply Database Migrations
if [ -f "backend/migrations.py" ]; then
    echo "🔄 Running database migrations..."
    python backend/migrations.py
    echo "✅ Database migrations applied."
else
    echo "⚠️ Migrations script not found. Skipping..."
fi

# Step 6: Free Port 8000 if Already in Use
if lsof -i :8000 >/dev/null; then
    echo "⚠️ Port 8000 is in use. Stopping the process..."
    kill -9 $(lsof -t -i :8000)
    echo "✅ Port 8000 is now free."
fi

# Step 7: Set PYTHONPATH
export PYTHONPATH=$(pwd)/src
echo "✅ Setup completed. To start FastAPI manually, use the following commands:"

echo ""
echo "🔹 Activate virtual environment:"
echo "    source venv/bin/activate"
echo ""
echo "🔹 Run FastAPI server manually:"
echo "    uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""

