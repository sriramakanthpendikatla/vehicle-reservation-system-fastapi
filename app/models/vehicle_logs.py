from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , DateTime
from enum import Enum
from app.database import Base
from datetime import datetime

class Action(str,Enum):
        CREATED = "CREATED"
        RESERVED = "RESERVED"
        CHECKED_OUT = "CHECKED_OUT"
        CHECKED_IN = "CHECKED_IN"
        CANCELLED ="CANCELLED"
        MAINTENANCE_STARTED = "MAINTENANCE_STARTED"
        MAINTENANCE_COMPLETED = "MAINTENANCE_COMPLETED"
        OVERDUE = "OVERDUE"

class Vehicle_logs(Base):
    __tablename__ = "vehicle_logs"
    id = Column(Integer,primary_key=True)
    vehicle_id =Column(Integer, ForeignKey("vehicles.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"),nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    timestamp = Column(DateTime, default=datetime.utcfromtimestamp,nullable=False)
    action=Column(SQLEnum(Action),nullable=False)