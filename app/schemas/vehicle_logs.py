from pydantic import BaseModel

class CreateVehiclelogs(BaseModel):
    vehicle_id:int
    employee_id:int
    department_id:int

class VehiclelogsResponse(BaseModel):
    id:int

