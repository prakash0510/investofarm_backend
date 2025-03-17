from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth_service import auth_required
from app.core.database import get_db
# from models.project import Project
from app.services.project import get_all_projects

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
def get_project(user_data: dict = Depends(auth_required), db_func: Session=Depends(get_db)):
    cursor = db_func.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Project")
    existing_user = cursor.fetchall()

    return {
        "message": existing_user
    }
