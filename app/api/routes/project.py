from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.services.auth_service import auth_required
from app.core.database import get_db
from app.services.project import get_all_projects, get_project_details

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/")
async def get_project(user_data: dict = Depends(auth_required), db_func: Session=Depends(get_db)):
    user_id = user_data.get("id")
    projects =  await get_all_projects(user_id, db_func)

    return projects


@router.get("/project-id")
async def get_project(project_id: int = Query(..., description="ID of the project"),user_data: dict = Depends(auth_required), db_func: Session=Depends(get_db)):
    projects =  await get_project_details(project_id, db_func)

    return projects

