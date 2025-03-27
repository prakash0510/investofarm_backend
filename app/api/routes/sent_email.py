from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth_service import auth_required
from app.core.database import get_db
from app.services.email_service import sent_otp_email, verify_otp

router = APIRouter(prefix="/api", tags=["Email Sent"])


@router.get("/send_otp")
async def get_project(email:str):
    response =  await sent_otp_email(email)

    return response

@router.get("/verify_otp")
async def otp_verification(email:str, otp: str):
    response =  await verify_otp(email, otp)

    return response

