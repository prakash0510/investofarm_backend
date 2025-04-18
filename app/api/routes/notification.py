from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import auth_required
from app.core.database import get_db

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("/")
def get_notifications(user_data: dict = Depends(auth_required), db_func=Depends(get_db)):
    cursor = db_func.cursor(dictionary=True)
    user_id = user_data.get("id")
    cursor.execute(f"SELECT * FROM Notification where User_ID ={user_id}")
    notifications = cursor.fetchall()
    if notifications:
        return {"data": {"notifications": notifications}}
    return {"data": {}}
