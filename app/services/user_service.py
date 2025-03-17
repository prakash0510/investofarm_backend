import secrets
import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserSignup
from app.core.security import hash_password
import sys

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("🔥 Debug: This is a test log message!")
# print("🔥 This is a test print", file=sys.stdout)
sys.stdout.flush()

def create_user(db: Session, user_data: UserSignup):
    # Check if email already exists
    logging.debug("🔥 This is a test print")
    sys.stdout.flush()
    logging.debug("🛠 create_user() function called")
    if db.query(User).filter(User.Email == user_data.email).first():
        print("hello")
        sys.stdout.flush()
        return {"error": "Email already exists"}

    hashed_password = hash_password(user_data.password)
    
    # Generate a unique secret key for the user
    try:
        user_secret_key = secrets.token_hex(32)
        print("🔥 This is a test print", file=sys.stdout)
        sys.stdout.flush()
    except Exception as e:
        print(f"❌ Error generating secret key: {e}")
        sys.stdout.flush()

    print(f"Create_user {user_secret_key}\n\n\\n\n\n")
    sys.stdout.flush()

    new_user = User(
        Name=user_data.name,
        Email=user_data.email,
        Mobile_Number=user_data.mobile_number,
        City=user_data.city,
        State=user_data.state,
        Pincode=user_data.pincode,
        Password=hashed_password,
        Secret_Key=user_secret_key
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"Create_user ✅ User Created: {new_user.__dict__}")
    sys.stdout.flush()
    return new_user

def get_user_by_email(db: Session, email: str):
    """Fetch user details by email."""
    return db.query(User).filter(User.Email == email).first()