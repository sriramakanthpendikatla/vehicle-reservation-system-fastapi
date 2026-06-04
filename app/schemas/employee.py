from pydantic import BaseModel, ConfigDict
from datetime import date


class CreateEmployee(BaseModel):
    name: str
    addharcard: int
    department_id: int
    driving_license_date: date
    vehicle_quota: int


class EmployeeResponse(BaseModel):
    id: int
    name: str
    addharcard: int
    department_id: int
    driving_license_date: date
    vehicle_quota: int

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdate(BaseModel):
    name: str
    addharcard: int
    department_id: int
    driving_license_date: date
    vehicle_quota: int