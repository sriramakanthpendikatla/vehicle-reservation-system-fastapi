from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , DateTime
from enum import Enum
from app.database import Base
from datetime import datetime

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer,primary_key=True)
    reservation_id =Column(Integer, ForeignKey("vechile_reservations.id"))
    start_odometer = Column(Integer, nullable=True)
    end_odometer = Column(Integer, nullable=True)
    fuel_level_before=Column(Integer, nullable=True)
    fuel_level_after= Column(Integer, nullable=True)
    check_out_time = Column(DateTime,default=datetime.utcnow,nullable=False)
    check_in_time = Column(DateTime, nullable=True)
    trip_start = Column(DateTime,default=datetime.utcnow,nullable=False)
    expected_end_time = Column(DateTime,nullable=False)
    actual_end_time = Column(DateTime,nullable=True)
