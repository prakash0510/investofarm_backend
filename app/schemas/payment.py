from pydantic import BaseModel, conint
class PaymentSchema(BaseModel):
    User_ID: int
    Project_ID:int
    Payment_Date: str
    Payment_Amount: str
    Payment_ID: str
    Order_ID: str
    Payment_Mode: str
    Payment_Status: str