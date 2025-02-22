from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile_number: str
    city: str
    state: str
    pincode: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
