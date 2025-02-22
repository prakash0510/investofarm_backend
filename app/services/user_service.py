from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserSignup
from app.core.security import hash_password

def create_user(db: Session, user_data: UserSignup):
    # Check if email already exists
    if db.query(User).filter(User.Email == user_data.email).first():
        return {"error": "Email already exists"}

    hashed_password = hash_password(user_data.password)

    new_user = User(
        Name=user_data.name,
        Email=user_data.email,
        Mobile_Number=user_data.mobile_number,
        City=user_data.city,
        State=user_data.state,
        Pincode=user_data.pincode,
        Password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
