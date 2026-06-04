from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , DateTime
from enum import Enum
from app.database import Base
from datetime import datetime


class Maintenance_schedule(Base):
    __tablename__ = "maintenace_schedules"

    id = Column(Integer, primary_key=True)
    vehicle_id =Column(Integer, ForeignKey("vehicles.id"))
    maintenance_start=Column(DateTime,nullable=False)
    maintenance_end=Column(DateTime,nullable=True)
    description=Column(String,nullable=False)