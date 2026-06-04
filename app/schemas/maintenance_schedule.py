from pydantic import BaseModel
from datetime import datetime

class CreateMaintenanceSchedule(BaseModel):
    vehicle_id :int
    maintenance_start:datetime
    maintenance_end:datetime
    description:str

class MaintenanceScheduleResponse(BaseModel):
    id:int

