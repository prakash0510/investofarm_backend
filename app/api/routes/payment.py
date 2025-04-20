from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import auth_required
from app.core.database import get_db
from app.services.payment import update_payment
from app.schemas.payment import PaymentSchema

router = APIRouter(prefix="/api/payment-update", tags=["Payment"])


@router.post("/")
async def get_notifications(payment: PaymentSchema,user_details: dict = Depends(auth_required), db_func=Depends(get_db)):
    payment = await update_payment(payment, db_func)
    if payment:
        return {"data": "Payment updated successfully"}
    return {"data": {}}
