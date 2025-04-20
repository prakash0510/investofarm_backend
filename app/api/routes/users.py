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
from app.services.auth_service import decrypt_data, encrypt_data, decode_jwt, token_blacklist
from app.services.auth_service import auth_required
from app.schemas.user import AddBankAccountdRequest, AddNomineedRequest, UpdatePasswordRequest, UserSignupRequest
import mysql.connector
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


# class UserSignupRequest(BaseModel):
#     Name: str
#     Email: EmailStr
#     Mobile_Number: int
#     City: str
#     State: str
#     Pincode: int
#     Password: str

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
            return {"data":"Email already registered"}

        hashed_password = hash_password(user.Password)

        insert_query = """
            INSERT INTO User (Name, Email, Mobile_Number, City, State, Pincode, Password, Is_Active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user.Name, user.Email, user.Mobile_Number, user.City, user.State,
            user.Pincode, hashed_password, True  
        )
        cursor.execute(insert_query, values)

        db.commit()

        cursor.close()
        return {"message": "User created successfully", "user": user.dict()}

    except mysql.connector.errors.IntegrityError as e:
        if "Duplicate entry" in str(e):
            if "Mobile_Number" in str(e):
                return {"data":"Mobile already registered"}
            elif "Email" in str(e):
                return {"data":"Email already Exists"}
        raise HTTPException(status_code=500, detail="Signup failed due to a server error")
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

    finally:
        cursor.close()


@router.post("/login")
def login(user: dict, response: Response, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE Email = %s", (user["Email"],))
    user_record = cursor.fetchone()
    cursor.close()

    if not user_record or not verify_password(user["Password"], user_record["Password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_jwt_token(user_record["ID"], user_record["Email"])
    refresh_token = create_refresh_token(user_record["ID"])
    user_record.pop("Password", None)
    user_record.pop("Is_Active", None)
    user_record.pop("Role", None)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"message": "Login successful", "access_token": access_token, "refresh_token":refresh_token,"user": user_record}




@router.get("/logout")
def logout(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token missing")

    token = auth_header.split(" ")[1]  

    # Decode token
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_blacklist(token)


    return {"success": True, "message": "Logged out successfully"}



@router.put("/update-password")
def update_password(data: UpdatePasswordRequest, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT ID, Password FROM User WHERE Email = %s", (data.email,))
    user_record = cursor.fetchone()

    if not user_record:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_new_password = hash_password(data.password)

    cursor.execute("UPDATE User SET Password = %s WHERE ID = %s", (hashed_new_password, user_record["ID"]))
    db.commit()
    cursor.close()

    return {"message": "Password updated successfully"}


@router.post("/add-bank-details")
def add_bank_details(data: AddBankAccountdRequest, user_data: dict = Depends(auth_required), db=Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)

        insert_query = """
                INSERT INTO Bank_Details (User_ID, Bank_Name, IFSC_Code, Account_Number)
                VALUES (%s, %s, %s, %s)
        """
        values = (data.User_ID, data.Bank_Name, data.IFSC_Code, data.Account_Number)
        cursor.execute(insert_query, values)

        db.commit()

        return {"message": "Bank Account added successfully"}
    except Exception as e:
        db.rollback()  
        return {"data":f"Failed to add bank account: {str(e)}"}


@router.post("/add-nominee-details")
def add_bank_details(data: AddNomineedRequest, user_data: dict = Depends(auth_required), db=Depends(get_db)):
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Nominee_Details WHERE Unique_ID = %s", (data.Unique_ID,))
        existing_data = cursor.fetchone()
        if existing_data:
            return {"message": f"Nominee already exists with this Unique ID {data.Unique_ID}"}

        insert_query = """
                INSERT INTO Nominee_Details (User_ID, Name, Relation, Unique_ID)
                VALUES (%s, %s, %s, %s)
        """
        values = (data.User_ID, data.Name, data.Relation, data.Unique_ID)
        cursor.execute(insert_query, values)

        db.commit()

        return {"message": "Nominee added successfully"}
    except Exception as e:
        db.rollback()  
        return {"data":f"Failed to add Nominee: {str(e)}"}


@router.post("/google-login")
async def google_login(request: Request, response: Response, db=Depends(get_db)):
    try:
        body = await request.json()
        token = body.get("id_token")

        if not token:
            raise HTTPException(status_code=400, detail="Missing id_token")

        # Specify the CLIENT_ID of the app that accesses the backend
        # CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        CLIENT_ID = "220724747894-9rns853pmgavt1ik84r66caq4qng2k84.apps.googleusercontent.com"

        # Verify the token
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)

        # Extract email and user info
        email = idinfo['email']
        name = idinfo.get('name', '')
        sub = idinfo['sub']
        return {"email": f"{idinfo['email']}","name":f"{idinfo.get('name', '')}"}

        # Check if user exists
        # cursor = db.cursor(dictionary=True)
        # cursor.execute("SELECT ID, Email FROM User WHERE Email = %s", (email,))
        # user_record = cursor.fetchone()

        # if not user_record:
        #     # If not found, create a new user
        #     insert_query = """
        #     INSERT INTO User (Name, Email, Mobile_Number, City, State, Pincode, Password, Is_Active)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        #     """
        #     values = (
        #         name, email, "", "", "",
        #         "", "", True  
        #     )
        #     cursor.execute(insert_query, values)
        #     # cursor.execute(
        #     #     "INSERT INTO User (Name, Email, Is_Active) VALUES (%s, %s, %s)",
        #     #     (name, email, True)
        #     # )
        #     db.commit()
        #     user_id = cursor.lastrowid
        # else:
        #     user_id = user_record["ID"]

        # cursor.close()

        # access_token = create_jwt_token(user_id, email)
        # refresh_token = create_refresh_token(user_id)

        # response.set_cookie(
        #     key="refresh_token",
        #     value=refresh_token,
        #     httponly=True,
        #     secure=True,
        #     samesite="Lax"
        # )

        # return {
        #     "message": "Google login successful",
        #     "access_token": access_token,
        #     "refresh_token": refresh_token,
        #     "user": {"id": user_id, "email": email}
        # }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))