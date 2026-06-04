from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum
from enum import Enum
from app.database import Base

class Department(Base):
    __tablename__ = "departments"
 
    id =Column(Integer, primary_key=True)
    title = Column(String , nullable=False)
