from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import auth_required
from app.core.database import get_db

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("/")
def get_notifications(user_data: dict = Depends(auth_required), db_func=Depends(get_db)):
    cursor = db_func.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Notification")
    notifications = cursor.fetchall()

    return {"data": {"notifications": notifications}}
