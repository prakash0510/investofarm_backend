from fastapi import Depends, HTTPException, Header
import jwt
import os
from dotenv import load_dotenv
import json
from cryptography.fernet import Fernet


ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key().decode()
fernet = Fernet(ENCRYPTION_KEY.encode())

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def auth_required(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    try:
        token = authorization.split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
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