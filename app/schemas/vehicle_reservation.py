from pydantic import BaseModel
from datetime import datetime

class CreateVehicleReservation(BaseModel):
    vehicle_id:int
    employee_id:int
    department_id:int

class VehicleReservationResponse(BaseModel):
    id:int
    vehicle_id:int
    employee_id:int
    department_id:int

class VehicleReservationUpdate(BaseModel):
    id:int