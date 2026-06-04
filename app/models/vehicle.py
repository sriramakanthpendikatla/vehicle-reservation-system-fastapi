from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , DateTime
from enum import Enum
from app.database import Base
from datetime import datetime
from app.models.vehicle_status import *



class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    number = Column(String,unique=True,nullable=False)
    status = Column(SQLEnum(Vehicle_status),default=Vehicle_status.AVAILABLE,nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"),nullable=False)
    current_odometer  = Column(Integer,default=0)
    maintenance_intervel = Column(Integer,nullable=False)
    maintenance_atkms = Column(Integer,nullable=False)