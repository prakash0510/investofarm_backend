import asyncio
from app.core.database import get_db
from app.core.utilities import post_data
from sqlalchemy.orm import Session
from app.schemas.feedback import ReviewSchema
from fastapi import Depends, HTTPException

async def post_review(review:ReviewSchema, db_func: Session = Depends(get_db)):
    """Fetch all active projects and news asynchronously."""
    try:
        sql_query = "INSERT INTO Feedback (Rating, User_Comment, User_ID) VALUES (%s, %s, %s)"
        values = (review.Rating, review.User_Comment, review.User_ID)

        # Run post_data function in a thread to avoid blocking
        response = await asyncio.to_thread(post_data, db_func, sql_query, values)

        if not response["success"]:
            raise HTTPException(status_code=500, detail=response["error"])
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 