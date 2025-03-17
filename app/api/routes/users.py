from pydantic import BaseModel, EmailStr
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.core.config import settings 
from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter, Response, Request, APIRouter, HTTPException, Depends, Header
import json
from cryptography.fernet import Fernet
from app.services.auth_service import decrypt_data, encrypt_data


router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


class UserSignupRequest(BaseModel):
    Name: str
    Email: EmailStr
    Mobile_Number: int
    City: str
    State: str
    Pincode: int
    Password: str

class UserLoginRequest(BaseModel):
    Email: EmailStr
    Password: str

class UserDetailsResponse(BaseModel):
    ID: int
    Name: str
    Email: EmailStr
    Mobile_Number: str
    City: str
    State: str
    Pincode: str
    
def hash_password(password: str) -> str:
    """Hash the user's password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify hashed password with user input password."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))



def create_jwt_token(user_id, email, expires_delta=None):
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    payload = encrypt_data({"id": user_id, "email": email, "exp": expire.timestamp()})
    return jwt.encode({"data": payload}, SECRET_KEY, algorithm="HS256")


def create_refresh_token(user_id):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = encrypt_data({"id": user_id, "exp": expire.timestamp()})
    return jwt.encode({"data": payload}, SECRET_KEY, algorithm="HS256")



@router.post("/signup")
def signup(user: UserSignupRequest, db=Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)
        db.start_transaction()  

        cursor.execute("SELECT * FROM User WHERE Email = %s", (user.Email,))
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.Password)

        insert_query = """
            INSERT INTO User (Name, Email, Mobile_Number, City, State, Pincode, Password, Is_Active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user.Name, user.Email, user.Mobile_Number, user.City, user.State,
            user.Pincode, hashed_password, True  
        )
        cursor.execute(insert_query, values)

        db.commit()

        cursor.close()
        return {"message": "User created successfully", "user": user.dict()}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

    finally:
        cursor.close()


@router.post("/login")
def login(user: dict, response: Response, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT ID, Name, Email, Password FROM User WHERE Email = %s", (user["Email"],))
    user_record = cursor.fetchone()
    cursor.close()

    if not user_record or not verify_password(user["Password"], user_record["Password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_jwt_token(user_record["ID"], user_record["Email"])
    refresh_token = create_refresh_token(user_record["ID"])

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"message": "Login successful", "access_token": access_token, "refresh_token":refresh_token,"user": {"id": user_record["ID"], "email": user_record["Email"]}}



@router.post("/refresh-token")
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user_data = decrypt_data(decoded_token["data"])
        new_access_token = create_jwt_token(user_data["id"], user_data.get("email"))
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")



