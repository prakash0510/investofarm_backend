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


from pydantic import BaseModel, EmailStr
from fastapi import Form

class UserSignupRequest(BaseModel):
    Name: str
    Email: EmailStr
    Mobile_Number: int
    City: str
    State: str
    Pincode: int
    Password: str

    @classmethod
    def as_form(
        cls,
        Name: str = Form(...),
        Email: EmailStr = Form(...),
        Mobile_Number: int = Form(...),
        City: str = Form(...),
        State: str = Form(...),
        Pincode: int = Form(...),
        Password: str = Form(...)
    ):
        return cls(
            Name=Name,
            Email=Email,
            Mobile_Number=Mobile_Number,
            City=City,
            State=State,
            Pincode=Pincode,
            Password=Password
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
        from_attributes = True  # Allows ORM model conversion


