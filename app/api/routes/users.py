from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from app.core.database import get_db

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")  # Load from .env
ALGORITHM = "HS256"

# Request model for user signup & login
class UserSignupRequest(BaseModel):
    Name: str
    Email: EmailStr
    Mobile_Number: str
    City: str
    State: str
    Pincode: str
    Password: str

class UserLoginRequest(BaseModel):
    Email: EmailStr
    Password: str

def hash_password(password: str) -> str:
    """Hash the user's password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify hashed password with user input password."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_jwt_token(user_id: int, email: str) -> str:
    """Generate JWT token for user authentication."""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
def signup(user: UserSignupRequest, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)

    # Check if email already exists
    cursor.execute("SELECT * FROM User WHERE Email = %s", (user.Email,))
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.Password)

    # Insert user into DB
    insert_query = """
        INSERT INTO User (Name, Email, Mobile_Number, City, State, Pincode, Password, Is_Active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (user.Name, user.Email, user.Mobile_Number, user.City, user.State, user.Pincode, hashed_password, True)

    cursor.execute(insert_query, values)
    db.commit()

    user_id = cursor.lastrowid
    token = create_jwt_token(user_id, user.Email)

    cursor.close()
    return {"message": "User created successfully", "token": token}

@router.post("/login")
def login(user: UserLoginRequest, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)

    # Check if user exists
    cursor.execute("SELECT ID, Email, Password FROM User WHERE Email = %s", (user.Email,))
    user_record = cursor.fetchone()

    if not user_record:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(user.Password, user_record["Password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate JWT token
    token = create_jwt_token(user_record["ID"], user_record["Email"])

    cursor.close()
    return {"message": "Login successful", "token": token}
