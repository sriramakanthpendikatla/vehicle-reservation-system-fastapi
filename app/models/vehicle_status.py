from sqlalchemy import Column,Integer,String,ForeignKey,Enum as SQLEnum , DateTime
from enum import Enum
from app.database import Base
from datetime import datetime

class Vehicle_status(str,Enum):
    AVAILABLE="AVAILABLE"
    RESERVED="RESERVED"
    IN_USE="IN_USE"
    MAINTENANCE="MAINTENANCE"
    OVERDUE="OVERDUE"
    OUT_OF_SERVICE="OUT_OF_SERVICE"