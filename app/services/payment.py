import asyncio
from app.core.database import get_db
from app.core.utilities import post_data
from sqlalchemy.orm import Session
from app.schemas.payment import PaymentSchema
from fastapi import Depends, HTTPException

async def update_payment(payment: PaymentSchema, db_func: Session = Depends(get_db)):
    """Fetch all active projects and news asynchronously."""
    try:
        print(payment)
        sql_query = "INSERT INTO Payment (User_ID, Project_ID, Payment_Date, Payment_Amount,Payment_ID, Order_ID, Payment_Mode, Payment_Status) VALUES (%s, %s, %s,%s, %s, %s,%s, %s)"
        values = (payment.User_ID, payment.Project_ID, payment.Payment_Date, payment.Payment_Amount, payment.Payment_ID, payment.Order_ID, payment.Payment_Mode, payment.Payment_Status)

        response = await asyncio.to_thread(post_data, db_func, sql_query, values)

        if not response["success"]:
            raise HTTPException(status_code=500, detail=response["error"])
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 