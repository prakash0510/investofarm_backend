#for mac run it by chmod +x run.sh
# ./run.sh

#!/bin/bash

# cd "$(dirname "$0")"

# echo "Activating virtual environment..."
# # source venv/bin/activate

# echo "Installing dependencies from requirements.txt..."
# pip install --upgrade pip
# pip install -r requirements.txt

# echo "Starting FastAPI application..."
# uvicorn app.main:app --reload

# for windows run it by run.bat

# @echo off
# cd /d %~dp0

# echo Activating virtual environment...
# call venv\Scripts\activate

# echo Installing dependencies from requirements.txt...
# pip install --upgrade pip
# pip install -r requirements.txt

# echo Starting FastAPI application...
# uvicorn main:app --reload

#!/bin/bash

# Navigate to project directory
cd "$(dirname "$0")"

echo "Activating virtual environment..."
source env/bin/activate 

echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

