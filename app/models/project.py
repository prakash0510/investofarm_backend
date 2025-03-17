from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = "Project"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Location = Column(String(255), nullable=False)
    Area = Column(String(255), nullable=False)
    Min_Investment = Column(Integer, nullable=False)
    Tenure = Column(String(50), nullable=False)
    Description = Column(Text, nullable=True)
    Intro = Column(Text, nullable=True)
    Image_URL = Column(String(255), nullable=True)
    Status = Column(String(50), nullable=False, default="active")
    Created_At = Column(DateTime, default=datetime.utcnow)
    Updated_At = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
