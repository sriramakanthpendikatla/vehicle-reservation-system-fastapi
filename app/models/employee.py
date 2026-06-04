from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , Date ,BigInteger
from enum import Enum
from app.database import Base
from datetime import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    addharcard = Column(BigInteger,unique=True,nullable=False)
    name = Column(String , nullable=False)
    department_id = Column(Integer , ForeignKey("departments.id"))
    driving_license_date = Column(Date, nullable=False)
    vehicle_quota = Column(Integer,nullable=True)