from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth_service import auth_required
from app.core.database import get_db
from app.schemas.feedback import ReviewSchema
from app.services.feedback_service import post_review

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@router.post("/")
async def post_feedback(review: ReviewSchema, user_data: dict = Depends(auth_required), db: Session = Depends(get_db)):
    projects =  await post_review(review, db)

    return projects

