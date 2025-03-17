from pydantic import BaseModel, conint
class ReviewSchema(BaseModel):
    User_ID: int
    Rating: conint(ge=1, le=5)  
    User_Comment: str