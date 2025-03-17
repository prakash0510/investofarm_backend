from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import secrets

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    Mobile_Number = Column(String, nullable=False)
    City = Column(String, nullable=False)
    State = Column(String, nullable=False)
    Pincode = Column(String, nullable=False)
    Password = Column(String, nullable=False)
    Secret_Key = Column(String, nullable=False)
    Is_Active = Column(Boolean, default=True)
