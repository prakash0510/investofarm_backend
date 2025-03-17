import asyncio
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.core.utilities import fetch_data



async def get_all_projects(db_func: Session = Depends(get_db)):
    """Fetch all active projects and news asynchronously."""
    projects = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Project")
    news = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM News")
    crops = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Crop")
    crop_expenses = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Crop_Expenses")

    return {"projects": projects, "news": news, "crops": crops, "crop_expenses": crop_expenses}  
