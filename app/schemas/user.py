# from pydantic import BaseModel, EmailStr

# class UserSignup(BaseModel):
#     name: str
#     email: EmailStr
#     password: str
#     mobile_number: int
#     city: str
#     state: str
#     pincode: int

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str
# from pydantic import BaseModel, EmailStr

# class UserSignup(BaseModel):
#     name: str
#     email: EmailStr
#     mobile_number: str
#     city: str
#     state: str
#     pincode: str
#     password: str

# class UserResponse(BaseModel):
#     ID: int
#     Name: str
#     Email: EmailStr
#     Mobile_Number: str
#     City: str
#     State: str
#     Pincode: str


from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import re

class UserSignupRequest(BaseModel):
    Name: str = Field(..., min_length=2, max_length=50, example="John Doe")
    Email: EmailStr = Field(..., example="user@example.com")
    Mobile_Number: str = Field(..., pattern=r"^[6-9]\d{9}$", example="9876543210") 
    City: str = Field(..., min_length=2, max_length=50, example="Bangalore")
    State: str = Field(..., min_length=2, max_length=50, example="Karnataka")
    Pincode: str = Field(..., pattern=r"^\d{6}$", example="400001")  
    Password: str = Field(..., min_length=6, max_length=20, example="Test@123")



async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    for error in errors:
        field = error["loc"][-1]
        if field == "Mobile_Number":
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid phone number. Please enter a valid 10-digit number starting with 6-9."},
            )
        elif field == "Pincode":
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid Pincode. It must be a 6-digit number."},
            )
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input. Please check your request data."},
    )

class UserLoginRequest(BaseModel):
    Email: EmailStr
    Password: str

    @classmethod
    def as_form(cls, Email: EmailStr = Form(...), Password: str = Form(...)):
        return cls(Email=Email, Password=Password)

class UserDetailsResponse(BaseModel):
    ID: int
    Name: str
    Email: EmailStr
    Mobile_Number: str
    City: str
    State: str
    Pincode: str

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    ID: int
    Name: str
    Email: EmailStr

    class Config:
        from_attributes = True  

class UpdatePasswordRequest(BaseModel):
    email: str
    password: str


class AddBankAccountdRequest(BaseModel):
    User_ID: int
    Bank_Name: str
    Account_Number: str
    IFSC_Code: str

class AddNomineedRequest(BaseModel):
    User_ID: int
    Name: str
    Relation: str
    Unique_ID: str





