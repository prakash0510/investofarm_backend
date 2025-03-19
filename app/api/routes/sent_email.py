from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth_service import auth_required
from app.core.database import get_db
from app.services.email_service import sent_otp_email

router = APIRouter(prefix="/api/send_otp", tags=["Email Sent"])


@router.get("/")
async def get_project(email:str):
    response =  await sent_otp_email(email)

    return response

