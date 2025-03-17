from sqlalchemy.orm import Session
from app.models.project import Project
from app.core.database import get_db
from fastapi import Depends

def get_all_projects(db_func: Session=Depends(get_db)):
    """Fetch all active projects from the database."""
    return db_func.query(Project).filter(Project.Status == "active").all()
