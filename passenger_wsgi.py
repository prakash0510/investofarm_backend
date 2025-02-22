import sys
import os

# Add project path
sys.path.insert(0, os.path.dirname(__file__))

# Import FastAPI app
from app.main import app  

# WSGI handler for Passenger
from mangum import Mangum
handler = Mangum(app)
