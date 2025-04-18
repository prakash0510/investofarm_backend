import asyncio
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.core.utilities import fetch_data




async def get_project_details(project_id: int, db_func: Session = Depends(get_db)):
    
    project = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Project where ID="+str(project_id))

    return project


async def get_all_projects(user_id, db_func: Session = Depends(get_db)):
    """Fetch all active projects and news asynchronously."""
    
    projects = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Project")
    news = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM News")
    crops = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Crop")
    crop_expenses = await asyncio.to_thread(fetch_data, db_func, "SELECT * FROM Crop_Expenses")
    transactions = await asyncio.to_thread(fetch_data, db_func, f"SELECT p.Name, t.id,t.user_id,t.project_id,t.payment_date,t.payment_amount,t.payment_id,t.payment_status FROM Payment t JOIN Project p ON t.project_id = p.id WHERE t.user_id = {user_id};")
    grouped = {}
    total_completed_amount = 0
    project_wise_totals = {}
    for row in transactions:
        project_name = row['Name'].strip()
        project_id = row['project_id']

        if project_name not in grouped:
            grouped[project_name] = []

        grouped[project_name].append(row)

        if row['payment_amount'] is not None and row['payment_status'] == 'Completed':
            total_completed_amount += row['payment_amount']

            if project_name not in project_wise_totals:
                project_wise_totals[project_name] = {
                    "name": project_name,
                    "invested_amount": 0,
                    "project_id": project_id
                }

            project_wise_totals[project_name]["invested_amount"] += row['payment_amount']
    project_wise_totals_list = list(project_wise_totals.values())
    transactions_list = [{project: items} for project, items in grouped.items()]
    

    return {"projects": projects, "news": news, "crops": crops, "crop_expenses": crop_expenses,"transactions":grouped,"total_invested_amount": total_completed_amount,"all_transactions": transactions,"invested_project": project_wise_totals_list}  
