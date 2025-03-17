from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectResponse(BaseModel):
    id: int
    Name: str
    Location: str
    Area: str
    Min_Investment: int
    Tenure: str
    Description: Optional[str]
    Intro: Optional[str]
    Image_URL: Optional[str]
    Status: str
    Created_At: datetime
    Updated_At: datetime

    class Config:
        from_attributes = True  # ORM Mode
