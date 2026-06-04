from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , DateTime
from enum import Enum
from app.database import Base
from datetime import datetime


class Vechile_reservation(Base):
    __tablename__ = "vechile_reservations"

    id = Column(Integer, primary_key=True)
    vehicle_id =Column(Integer, ForeignKey("vehicles.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    reservation_start =Column(DateTime,default=datetime.utcnow,nullable=False)
    reservation_end =Column(DateTime,nullable=True)