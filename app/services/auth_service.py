from fastapi import Depends, HTTPException, Header
import jwt
import os
from dotenv import load_dotenv
import json
from cryptography.fernet import Fernet
from app.core.config import settings


ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key().decode()
fernet = Fernet(ENCRYPTION_KEY.encode())

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
token_blacklist_set = set()

def auth_required(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    try:
        token = authorization.split(" ")[1]
        if token in token_blacklist_set:
            raise HTTPException(status_code=401, detail="Token has been invalidated")
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        decrypted_data = decrypt_data(decoded_token["data"])
        user_id = decrypted_data.get("id")
        return decrypted_data
        # return decrypt_data(decoded_token["data"])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def decrypt_data(encrypted_data: str) -> dict:
    return json.loads(fernet.decrypt(encrypted_data.encode()).decode())


def encrypt_data(data: dict) -> str:
    json_data = json.dumps(data).encode()
    return fernet.encrypt(json_data).decode()



def token_blacklist(token: str):
    """
    Decodes JWT token and returns the payload.
    """
    try:
       token_blacklist_set.add(token)
    except Exception as e:
        return None


def decode_jwt(token: str):
    """
    Decodes JWT token and returns the payload.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception as e:
        return None
