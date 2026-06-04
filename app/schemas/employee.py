from pydantic import BaseModel
from datetime import datetime

class CreateEmployee(BaseModel):
    name:str
    addharcard:int
    department_id:int
    driving_license_date:datetime
    vehicle_quota:int

class EmployeeResponse(BaseModel):
    id:int
    name:str
    addharcard:int
    department_id:int
    driving_license_date:datetime
    vehicle_quota:int



class EmployeeUpdate(BaseModel):
    name:str
    addharcard:int
    department_id:int
    driving_license_date:datetime
    vehicle_quota:int