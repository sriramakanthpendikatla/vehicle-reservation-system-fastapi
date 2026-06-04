from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    title: str


class DepartmentUpdate(BaseModel):
    id:int

class DepartmentResponse(BaseModel):
    id: int
    title: str

