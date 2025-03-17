from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth_service import auth_required
from app.core.database import get_db
from app.services.project import get_all_projects

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/")
async def get_project(user_data: dict = Depends(auth_required), db_func: Session=Depends(get_db)):
    projects =  await get_all_projects(db_func)

    return projects

