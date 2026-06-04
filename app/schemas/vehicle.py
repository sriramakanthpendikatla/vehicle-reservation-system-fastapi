from pydantic import BaseModel
from enum import Enum
from app.models.vehicle_status import *

class CreateVehicle(BaseModel):
    type:str
    number:str
    department_id:int
    maintenance_intervel:int
    maintenance_atkms:int

class VehicleResponse(BaseModel):
    id:int
    type:str
    number:str
    department_id:int
    maintenance_intervel:int
    maintenance_atkms:int

class VehicleUpdate(BaseModel):
    type:str
    number:str
    department_id:int



